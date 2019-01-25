#########################
# 						#
#		SONINT			#
#						#
#		v 0.1			#
#		2017			#
#	Sonar Visualiation	#
#						#
#########################

# the purpose of these function is to help visualize wcd data 
# probably need to move the plotter function from MCP in here
#
# first function is a resampling of a watercolumn ping to a 4k array
# so qt can display it
# in the future this method will also work as a zoom

import numpy as np 
import numpy.polynomial.polynomial as poly
import sys

osname = sys.platform

if osname == 'linux':

	sys.path.append('/home/huxrules/SeepIntelPro/MASTEREXPLODER/MISC/build/lib.linux-x86_64-3.6')

elif osname == 'darwin':
	sys.path.append('/Users/huxrules/MASTER_EXPLODER/git_me/MASTEREXPLODER/MISC/build/lib.macosx-10.12-x86_64-3.6')


import astros


def vis4kWCDPing(wcd_angle_array, wcd_range_array, wcd_data_array, maxdepth = "", maxrange = ""):

	#print(maxdepth, maxrange)
	# this function is designed for one ping to be passed to it
	# mcp will have to pull the needed ping out of the db and send it 
	#to this function

	# ok first we need to find the longest axis for the wcd file
	# so lets find maximum range, and port and starboard ranges

	wcd_data_array[wcd_data_array >127 ] = 127
	wcd_data_array[wcd_data_array < -128] = 127

	if not maxrange:
		maxrange = np.amin(wcd_range_array)
		#print("max range {}".format(maxrange))
		maxPortAngle = np.amin(wcd_angle_array)
		#print("maxPortAngle {}".format(maxPortAngle))
		maxStbdAngle = np.amax(wcd_angle_array)
		#print("maxStbdAngle {}".format(maxStbdAngle))
		portSwathRange = (np.sin(np.radians(maxPortAngle))) * maxrange
		stbdSwathRange = (np.sin(np.radians(maxStbdAngle))) * maxrange

		kRatio = 1080/1920
		pingRatio = abs(maxrange) / (abs(portSwathRange) + abs(stbdSwathRange))

		distanceTo4kPixel = 0

		if pingRatio <= kRatio:
			distanceTo4kPixel = np.amax([abs(portSwathRange), abs(stbdSwathRange)]) / 960 # half of 1920
			

		else:
			distanceTo4kPixel = abs(maxrange) / 1080

		maxPixelCountX = 1920
		maxPixelCountY = 1080

	else:

		totalRange = (abs(maxrange) * 2) 
		maxdepth = abs(maxdepth)
		kRatio = 1080/1920
		pingRatio = maxdepth/ totalRange

		distanceTo4kPixel = 0

		WCDbuffer = int(max(totalRange,maxdepth) * 0.05)

		if pingRatio <= kRatio:
			distanceTo4kPixel = abs((maxrange) + WCDbuffer )/ 960 # half of 1920
			axisflag = 0
		#print(distanceTo4kPixel)

		else:

			distanceTo4kPixel = abs((maxdepth) + WCDbuffer) / 1080
			axisflag = 1

		if axisflag == 0:
			maxPixelCountY = int(round((maxdepth + WCDbuffer) / distanceTo4kPixel))
			maxPixelCountX = 1920

		elif axisflag == 1:
			#maxPortAngle = np.amin(wcd_angle_array)
		#print("maxPortAngle {}".format(maxPortAngle))
			#maxStbdAngle = np.amax(wcd_angle_array)
		#print("maxStbdAngle {}".format(maxStbdAngle))
			#portSwathRange = (np.sin(np.radians(maxPortAngle))) * maxrange
			#stbdSwathRange = (np.sin(np.radians(maxStbdAngle))) * maxrange
			maxPixelCountX = int(round((totalRange + WCDbuffer) / distanceTo4kPixel))
			maxPixelCountY = 1080

		#print("pixel count X {}, pixel count y {} axisFlag {}".format(maxPixelCountX,maxPixelCountY,axisflag))






	maxSonarData = np.amax(wcd_data_array)
	minSonarData = np.amin(wcd_data_array)
	avgSonarData = np.average(wcd_data_array)
	meanSonarData = np.mean(wcd_data_array)
	histSonarData = np.histogram(wcd_data_array)



	#print("Sonar data stats: max {} min {} median {} mean {} ".format(maxSonarData,minSonarData,avgSonarData,meanSonarData))
	#print(histSonarData)

	

	

	


	# need to find the range and distance to every pixel in a 4k screen with
	# 0,0 being right between the 1920 and 1921 pixel

	distanceFromCenter = np.empty([1,maxPixelCountX], dtype="float64")
	depthFromTop = np.empty([maxPixelCountY,1], dtype="float64")

	for x in range(0,maxPixelCountX):
			distanceFromCenter[0,x] = ((x + 0.5) - round(maxPixelCountX/2)) * distanceTo4kPixel #starts from zero and gets the center of each all the way till the end.
	
	for x in range(0,maxPixelCountY):
	#for x in range(0,1080):
		depthFromTop[x,0] = (x - maxPixelCountY + 0.5) * distanceTo4kPixel



	range4kArray = np.resize(distanceFromCenter,[maxPixelCountY,maxPixelCountX])
	depthFromTopArray = np.tile(depthFromTop,maxPixelCountX)

	distanceArra = (np.sqrt( np.square(range4kArray) + np.square(depthFromTopArray))) * -1
	angleArra = np.degrees(np.arctan(range4kArray/depthFromTopArray))

	distanceArray = np.array(distanceArra , dtype="float64")
	angleArray = np.array(angleArra, dtype="float64")

	angleTupleArray = []
	angleStartArray = []
	angleEndArray = []
	
	for i in range(0,len(wcd_angle_array)):
		if i == 0:
			tempTuple = (wcd_angle_array[i] + 1) , ((wcd_angle_array[i] + wcd_angle_array[i+1]) / 2)
			angleTupleArray.append(tempTuple)
			angleStartArray.append(tempTuple[0])
			angleEndArray.append(tempTuple[1])


		elif 1 <= i <= (len(wcd_angle_array)-2): 
			tempTuple = ((wcd_angle_array[i-1] + wcd_angle_array[i]) / 2 , (wcd_angle_array[i] + wcd_angle_array[i+1]) / 2 )
			angleTupleArray.append(tempTuple)
			angleStartArray.append(tempTuple[0])
			angleEndArray.append(tempTuple[1])

		elif i == (len(wcd_angle_array)-1):
			tempTuple = ((wcd_angle_array[i-1] + wcd_angle_array[i]) / 2 , (wcd_angle_array[i] - 1))
			angleTupleArray.append(tempTuple)
			angleStartArray.append(tempTuple[0])
			angleEndArray.append(tempTuple[1])

	depthTupleArray = []
	depthStartArray=[]
	depthEndArray=[]

	for i in range(0,len(wcd_range_array)):
		if i == 0:
			tempTuple = (0 , (wcd_range_array[i] + wcd_range_array[i+1]) / 2)
			depthTupleArray.append(tempTuple)
			depthStartArray.append(tempTuple[0])
			depthEndArray.append(tempTuple[1])

		elif 1 <= i <= (len(wcd_range_array)-2): 
			tempTuple = ((wcd_range_array[i-1] + wcd_range_array[i]) / 2 , (wcd_range_array[i] + wcd_range_array[i+1]) / 2 )
			depthTupleArray.append(tempTuple)
			depthStartArray.append(tempTuple[0])
			depthEndArray.append(tempTuple[1])

		elif i == (len(wcd_range_array)-1):
			tempTuple = ((wcd_range_array[i-1] + wcd_range_array[i]) / 2 , (wcd_range_array[i] - 1))
			depthTupleArray.append(tempTuple)
			depthStartArray.append(tempTuple[0])
			depthEndArray.append(tempTuple[1])
	
	angleStartArray = np.array(angleStartArray, dtype="float64")
	angleEndArray = np.array(angleEndArray, dtype="float64")
	depthStartArray = np.array(depthStartArray, dtype="float64")
	depthEndArray = np.array(depthEndArray, dtype="float64")
	projectedArray = np.full([maxPixelCountY,maxPixelCountX], 127, dtype="float64" )


	projectedArray = astros.bats(angleStartArray, angleEndArray, depthStartArray, depthEndArray, wcd_data_array, distanceArray, angleArray, projectedArray)


	return(projectedArray)
	#return(projectedArray, angleStartArray, depthStartArray)











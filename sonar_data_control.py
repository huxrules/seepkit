#########################
# 						#
#	MASTER CONTROL		#
#	PROGRAM				#
#		v 0.2			#
#		2017			#
#	Sonar Data Ripper	#
#						#
#########################

# new in version 3_1
# write to database directly when wcd data read
# preparing for multiprocessing of wcd reads
# write to database xyz 88 data




import all_reader3 as all_reader
import seepkit_predict as SKP
import numpy as np
import time
import SONINT_vis3 as Vis3
import matplotlib.pyplot as plt
import binascii
import pickle
import multiprocessing
import queue
import traceback
import uuid


import multiPROC




def AllFileEngine(allFileString,csvOut):

	#this will be the engine that kicks off AllSix Bytes and steers the program to
	#appropriate function from all_reader

	#so first we will open the files

	csvFile = open(csvOut, 'w')
	allFile = open(allFileString,'rb')

	print("Working on, ", allFileString)

	# we will figure out the file size

	allFile.seek(0,2) # to the end
	allFileSize = allFile.tell() #whats the position
	allFile.seek(0,0) #to the start

	allCurrentLocation = allFile.tell()

	#begin the loop

	while allCurrentLocation < allFileSize:

		#unlike other file formats the all and wcd just start with the packets
		# errorCode doesnt really do anything
		
		allFile, dataTuple, errorCode = all_reader.AllSixBytes(allFile)

		#the DataTuple consists of size, the number two, and the packet type 
		packetType = dataTuple[2]
		packetSize = dataTuple[0]

		# there is probably a better way to do this but for now.....

		if packetType == 49: #the PUSStatus Datagram

			allFile, returnDataTuple, errorCode = all_reader.PUStatusOutput(allFile, packetSize)

		elif packetType == 51: # the Extra Parameters Datagram

			allFile, returnDataTuple, errorCode = all_reader.ExtraParammetersDatagram(allFile, packetSize)		

		elif packetType == 65: # Attitude Datagram

			allFile, returnDataTuple, errorCode = all_reader.AttitudeDatagram(allFile, packetSize)

		elif packetType == 67: # Clock Datagram

			allFile, returnDataTuple, errorCode = all_reader.ClockDatagram(allFile, packetSize)

		elif packetType == 68: #Depth Datagram

			allFile, returnDataTuple, errorCode = all_reader.DepthDatagram(allFile, packetSize)

		elif packetType == 71: #surface Sound Speed

			allFile, returnDataTuple, errorCode = all_reader.SurfaceSoundSpeed(allFile, packetSize)

		elif packetType == 72: #Heading Datagram

			allFile, returnDataTuple, errorCode = all_reader.HeadingDatagram(allFile, packetSize)

		elif packetType == 73: #Multibeam Parameters Start

			allFile, returnDataTuple, errorCode = all_reader.MultibeamParameters(allFile, packetSize)

		elif packetType == 78: #Raw Range and Beam Angle

			allFile, returnDataTuple, errorCode = all_reader.RawRangeAndBeamAngleDatagram(allFile, packetSize)

		elif packetType == 80: #Position Datagram

			allFile, returnDataTuple, errorCode = all_reader.PositionDatagram(allFile, packetSize)

			lattitudePosition = float(returnDataTuple[5]) / float(20000000)
			longitudePosition = float(returnDataTuple[6]) / float(10000000)

			csvFile.write('{0},{1}\n'.format(longitudePosition,lattitudePosition)) #wonder why i did this the fancy way

		elif packetType == 82: #Runtime Parameters

			allFile, returnDataTuple, errorCode = all_reader.RuntimeParametersDatagram(allFile, packetSize)

		elif packetType == 85: #Sound Speed Datagram

			allFile, returnDataTuple, errorCode = all_reader.SoundSpeedProfileDatagram(allFile, packetSize)

		elif packetType == 87: #Kongsberg Marine SSP output Datagram

			allFile, returnDataTuple, errorCode = all_reader.KongsbergMaritimeSSPoutputDatagram(allFile, packetSize)

		elif packetType == 88: #XYZ_88_Datagram

			allFile, returnDataTuple, errorCode = all_reader.XYZ_88_Datagram(allFile, packetSize)

		elif packetType == 89: #Seabed Imange Data 89

			# note this one returns and extra "sampleList" we need to work on this one
			allFile, returnDataTuple, sampleList, errorCode = all_reader.SeabedImageData89Datagram(allFile,packetSize)

		elif packetType == 105: #Multibeam Parameters End (same as Multibeam Parameters start)

			allFile, returnDataTuple, errorCode = all_reader.MultibeamParameters(allFile, packetSize)

		elif packetType == 107: #Water Column Datagram

			# note this one returns and extra "sampleList" we need to work on this one
			allFile, returnDataTuple, sampleList, errorCode = all_reader.WaterColumnDatagram(allFile, packetSize)

		elif packetType == 110: #Network Attitude Velocity

			allFile, returnDataTuple, errorCode = all_reader.NetworkAttitudeVelocityDatagram(allFile, packetSize)

		elif packetType == 112: #Multibeam Parameters Remote(same as Multibeam Parameters start)

			allFile, returnDataTuple, errorCode = all_reader.MultibeamParameters(allFile, packetSize)

		else:
			#need to make a skipper function 
			#for now
			skipBytes = packetSize - 2
			allFile.seek(skipBytes, 1)

		allCurrentLocation = allFile.tell()

	allFile.close()
	csvFile.close()

	return()

def AllFileEnginePosition(allFileString,csvOut):

	#this will be the engine that kicks off AllSix Bytes and steers the program to
	#appropriate function from all_reader

	

	#so first we will open the files



	csvFile = open(csvOut, 'w')
	allFile = open(allFileString,'rb')

	#listOfPacketTypes = all_reader.PacketMapper(allFile)
	#print listOfPacketTypes

	print("Working on, ", allFileString)

	# we will figure out the file size

	allFile.seek(0,2) # to the end
	allFileSize = allFile.tell() #whats the position
	allFile.seek(0,0) #to the start

	allCurrentLocation = allFile.tell()
	#print allCurrentLocation

	#begin the loop

	while allCurrentLocation < allFileSize:

		#print allFile.tell()
		#unlike other file formats the all and wcd just start with the packets
		# errorCode doesnt really do anything
		
		allFile, dataTuple, errorCode = all_reader.AllSixBytes(allFile)

		#print dataTuple

		#the DataTuple consists of size, the number two, and the packet type 
		packetType = dataTuple[2]
		packetSize = dataTuple[0]

		# there is probably a better way to do this but for now.....
		packetFinishPosition = allCurrentLocation + packetSize - 2

		if packetFinishPosition > allFileSize:
			print("end of file is too short")
			allCurrentLocation = allFileSize

		elif packetType == 0 and packetSize == 0:
			print("zero packet type error")
			allCurrentLocation = allFileSize

		elif packetType == 80: #Position Datagram

			allFile, returnDataTuple, errorCode = all_reader.PositionDatagram(allFile, packetSize)

			lattitudePosition = float(returnDataTuple[5]) / float(20000000)
			longitudePosition = float(returnDataTuple[6]) / float(10000000)

			csvFile.write('{0},{1}\n'.format(longitudePosition,lattitudePosition)) #wonder why i did this the fancy way
			#print('{0},{1}\n'.format(longitudePosition,lattitudePosition))
			allCurrentLocation = allFile.tell()

		else: 

			skipBytes = packetSize - 2
			allFile.seek(skipBytes,1)
			allCurrentLocation = allFile.tell()

		

		

	allFile.close()
	csvFile.close()

	return()




def wcd_reader_with_model(wcdFileString, procnum): 

	#infile = x.rstrip()


	try:
		dualSwathFlag = 0
		pingmode = 'none'
		TXPulseForm = 'none'
		DualSwath = 'none'

		line_name = wcdFileString.split(".wcd")[0].split("/")[-1]
		file_name = wcdFileString

			
		fileObject = open(wcdFileString,'rb')

		packetMap = all_reader.PacketMapper(fileObject)
		packetMapPosition =0
		fileObject.seek(0,0)
		
		continuation = 0
		
		print("Working on, ", wcdFileString)

		# we will figure out the file size

		fileObject.seek(0,2) # to the end
		fileObjectSize = fileObject.tell() #whats the position
		
		#print fileObjectSize
		fileObject.seek(0,0) #to the start

		fileCurrentLocation = fileObject.tell()

		#begin the loop
		
		allXList = []
		allYList = []
		allWCDsamples = []
		mcpXList = []
		mcpYList = []
		mcpSampleList = []
		xList = []
		yList = []
		WCDsamples = []
		WCDping = []
		proctype = 0
		pingmode = 'none'
		TXPulseForm = 'none'
		DaulSwath = 'none'
		MaxStripList = []
		lineHist = np.full(50,0, dtype="float64")
		lineEdges = []
		pingAndPredictResults = []

		PredictClass = SKP.WCDPredictor()

		while fileCurrentLocation < fileObjectSize:
		
			fileObject, dataTuple, errorCode = all_reader.AllSixBytes(fileObject)

				#the DataTuple consists of size, the number two, and the packet type 
			packetType = dataTuple[2]
			#print packetType
			packetSize = dataTuple[0]

				# there is probably a better way to do this but for now.....

			if packetType == 49: #the PUSStatus Datagram

				fileObject, returnDataTuple, errorCode = all_reader.PUStatusOutput(fileObject, packetSize)

			elif packetType == 51: # the Extra Parameters Datagram

				fileObject, returnDataTuple, errorCode = all_reader.ExtraParammetersDatagram(fileObject, packetSize)		

			elif packetType == 65: # Attitude Datagram

				fileObject, returnDataTuple, errorCode = all_reader.AttitudeDatagram(fileObject, packetSize)

			elif packetType == 67: # Clock Datagram

				fileObject, returnDataTuple, errorCode = all_reader.ClockDatagram(fileObject, packetSize)

			elif packetType == 68: #Depth Datagram

				fileObject, returnDataTuple, errorCode = all_reader.DepthDatagram(fileObject, packetSize)

			elif packetType == 71: #surface Sound Speed

				fileObject, returnDataTuple, errorCode = all_reader.SurfaceSoundSpeed(fileObject, packetSize)

			elif packetType == 72: #Heading Datagram

				fileObject, returnDataTuple, errorCode = all_reader.HeadingDatagram(fileObject, packetSize)

			elif packetType == 73: #Multibeam Parameters Start

				fileObject, returnDataTuple, errorCode = all_reader.MultibeamParameters(fileObject, packetSize)

			elif packetType == 78: #Raw Range and Beam Angle

				fileObject, returnDataTuple, errorCode = all_reader.RawRangeAndBeamAngleDatagram(fileObject, packetSize)

			elif packetType == 80: #Position Datagram

				fileObject, returnDataTuple, errorCode = all_reader.PositionDatagram(fileObject, packetSize)

		
				#cur, conn = SDS.WriteToPosition(cur, conn, lineUUID, returnDataTuple)

			elif packetType == 82: #Runtime Parameters

				fileObject, returnDataTuple, errorCode, pingmode, TXPulseForm, DualSwath = all_reader.RuntimeParametersDatagram(fileObject, packetSize)

			elif packetType == 85: #Sound Speed Datagram

				fileObject, returnDataTuple, errorCode = all_reader.SoundSpeedProfileDatagram(fileObject, packetSize)

			elif packetType == 87: #Kongsberg Marine SSP output Datagram

				fileObject, returnDataTuple, errorCode = all_reader.KongsbergMaritimeSSPoutputDatagram(fileObject, packetSize)

			elif packetType == 88: #XYZ_88_Datagram

				fileObject, dataTupleFirst, depth, acrosstrack, alongtrack, \
				detectionwindow, quality, BAIadjust, detection, realtime_cleaning,\
				reflectivity, errorCode = all_reader.XYZ_88_Datagram(fileObject, packetSize)

				cur, conn = SDS.WriteToBathyPing(cur, conn, dataTupleFirst, depth, acrosstrack, alongtrack, detectionwindow, quality, BAIadjust, detection, realtime_cleaning,reflectivity, lineUUID)

			elif packetType == 89: #Seabed Imange Data 89

				# note this one returns and extra "sampleList" we need to work on this one
					fileObject, returnDataTuple, sampleList, errorCode = all_reader.SeabedImageData89Datagram(fileObject,packetSize)

			elif packetType == 105: #Multibeam Parameters End (same as Multibeam Parameters start)

				fileObject, returnDataTuple, errorCode = all_reader.MultibeamParameters(fileObject, packetSize)

			elif packetType == 107: #Water Column Datagram

				
					
				fileObject, packetSize, packetMap, packetMapPosition, continuation, xList, yList, \
							WCDsamples, pingNumber, transmitPingTilt, timeseconds = all_reader.WaterColumnDatagram_ForWCD(fileObject, \
							packetSize, packetMap, packetMapPosition, \
							continuation, xList, yList, WCDsamples)
						
				if continuation == 0:


					tempindex = 0 
					maxdepth = []
					maxdistance = []
					testmaxrange = []
					averageTransPingTilt = np.average(transmitPingTilt)

					#test to see if its a possible forst or second of a dual swath, 0 is the first, 1 is the second

					if DualSwath == 'Fixed' or DualSwath == 'Dynamic':
						if dualSwathFlag == 0:
							CurrentSwathFlag = dualSwathFlag
							dualSwathFlag = 1
						elif dualSwathFlag == 1:
							CurrentSwathFlag = dualSwathFlag
							dualSwathFlag = 0

					elif DualSwath == 'off':
						CurrentSwathFlag =0
						dualSwathFlag =0

					else:
						CurrentSwathFlag =0
						dualSwathFlag =0	

					for i in range(len(yList)):
						testrange = yList[i][-1]
						testangle = xList[i]
						temp_depth = abs((np.cos(np.deg2rad(testangle))) * testrange)
						temp_range = abs((np.sin(np.deg2rad(testangle))) * testrange)
						tst_temp_range = ((np.sin(np.deg2rad(testangle))) * testrange)

						maxdepth.append(temp_depth)
						maxdistance.append(temp_range)
						testmaxrange.append(tst_temp_range)
						tempindex +=1

					maxdepthping = np.max(maxdepth)
					maxrangeping = np.max(maxdistance)
					tstminrangeping = np.min(testmaxrange)
					tstmaxrangeping = np.max(testmaxrange)

					WCDping.append(pingNumber)
					pickledWCDSamples = pickle.dumps(WCDsamples)
					maxY =  max(yList,key = len) # this first trickery reads all the Y (ranges) in the list and returns the longest list
					negmaxY = [-x for x in maxY] # negmax is all the the maximum Y made negative duh

					currentAngleArray = np.array(xList, dtype="float64")    # making arrays from both datasets
					currentRangeArray = np.array(negmaxY, dtype = "float64")

					PredictClass,predictionValue = WCDPingMaster(WCDsamples, pickledWCDSamples,
												currentAngleArray , currentRangeArray, lineUUID, 
												pingNumber, maxdepthping, maxrangeping, 
												averageTransPingTilt, timeseconds, 
												CurrentSwathFlag, pingmode, TXPulseForm, DualSwath,PredictClass)
					if predictionValue > 0.5:
						pingAndPredictResults.append([line_name, pingNumber,predictionValue])					



			elif packetType == 110: #Network Attitude Velocity

				fileObject, returnDataTuple, errorCode = all_reader.NetworkAttitudeVelocityDatagram(fileObject, packetSize)

			elif packetType == 112: #Multibeam Parameters Remote(same as Multibeam Parameters start)

				fileObject, returnDataTuple, errorCode = all_reader.MultibeamParameters(fileObject, packetSize)

			else:
					#need to make a skipper function 
					#for now
				skipBytes = packetSize - 2
				fileObject.seek(skipBytes, 1)

			fileCurrentLocation = fileObject.tell()
			packetMapPosition += 1

		fileObject.close()

		if len(WCDping) > 0:
			# combine 
			return(pingAndPredictResults) #processType, linename, finalProcessNumber,lineUUID
		else:
			print(line_name + " did not have any water column pings")
			
			return([])
	except:
		errorTrace = traceback.format_exc()
		errorString = "#"*60 + "\n" + "LINE LOAD ERROR" "\n" + line_name + "\n" + errorTrace + "\n" + "#"*60
		print(errorString)

def WCDPingMaster(WCDSamples, pickledWCDSamples, currentAngleArray ,
				 currentRangeArray, lineUUID, pingNumber, maxdepthping, 
				 maxrangeping, averageTransPingTilt, timeseconds, 
				 CurrentSwathFlag, pingmode, TXPulseForm, DualSwath, PredictClass):
		
	
		npYArray, npXArray, npDataArray = WCDNumpyArray(currentAngleArray,currentRangeArray, WCDSamples)
		currentWCDArray = npDataArray / 2
		currentPingUUID = pingUUID
		currentPingmaxdepth = maxdepthping
		currentPingmaxrange = maxrangeping
		try:	
			ProjA = Vis3.vis4kWCDPing(currentAngleArray, currentRangeArray, currentWCDArray, currentPingmaxdepth,currentPingmaxrange )
			"""
			print("ping projected")
			print(type(ProjA))
			temphist, lineEdges = np.histogram(ProjA, bins=50, range=(-128, 126))
			print("#### proj A histogram #####")
			print(temphist)
			print("####proj A hist edges ####")
			print(lineEdges)"""
			pickledWCDProj = pickle.dumps(ProjA)

		except:
			errorTrace = traceback.format_exc()
			errorString = "#"*60 + "\n" + "MCP PROJECTION GENERATOR ERROR" "\n" + str(lineUUID) + "\n" + pingNumber+ "\n" + errorTrace + "\n" + "#"*60
			print(errorString)	
		
		PredictionValue = PredictClass.run_prediction(ProjA)
		PredictionValue = PredictionValue[0][0]



		return(PredictClass, PredictionValue)



def WCDNumpyArray(npXArray, npYArray, WCDsamples): 

	#this requires an entire ping of water column data to be read
	#basically this makes the wcd data array all the same size per angle
	# as its read through the file it has differing angles
	# a similar treatment is done to range

	#maxY =  max(yList,key = len) # this first trickery reads all the Y (ranges) in the list and returns the longest list
	#negmaxY = [-x for x in maxY] # negmax is all the the maximum Y made negative duh
	lenMaxY = len(npYArray) #length 
	lenX = len(npXArray)

	
	npDataArray = np.full((lenX,lenMaxY), 254, dtype="int16") # makes the empty array that we will later partially fill with data 
	#this value is 254 because we later divide by 2 (127) and later want to blank this data
	#####
	######
	########
	####### crap this has caused problems! Also should just be a single signed int (one byte!)

	#npXArray = np.array(xList, dtype="float64")    # making arrays from both datasets
	#npYArray = np.array(negmaxY, dtype = "float64")
	


	#print npYArray
	#print npDataArray.shape

	arrayPosX = 0
	arrayPosY = 0

	for samp in WCDsamples:    # this little douple loop reads the angle by angle wcd data (samp)
		#print len(samp)		# and then writes it to the empty npDataArray
		

		for i in range(0,len(samp)):  # populated the array one column at a time
			#print i

			npDataArray[arrayPosX,i] = samp[i]
		
		arrayPosX +=1


	"""temphist, lineEdges = np.histogram(npDataArray, bins=50, range=(-128, 126))
	print("#### numpyarray histogram #####")
	print(temphist)
	print("####numpy hist edges ####")
	print(lineEdges)"""
	return(npYArray, npXArray, npDataArray)


if __name__ == "__main__":

	pass










		

	


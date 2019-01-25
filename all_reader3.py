##########################################
#            All_READER 	             #
#              VER 0.1                   #
#                                        #
##########################################

import struct

def TestOpen():
	alltest = open("/Users/huxrules/MASTER_EXPLODER/GIT_ME/MASTEREXPLODER/TEST_DATA/0053_20140322_045759_EX1402L2_MB.all","rb")
	return(alltest)

def AllSixBytes(fileobject):
	
	errorcode = 0
	binarydata = fileobject.read(6)
	dataTuple = struct.unpack('<IBB', binarydata)

	#print dataTuple

	if dataTuple[1] == 2:
		errorcode = 0
		return(fileobject, dataTuple, errorcode)
	else:
		errorcode = 1
		return(fileobject, dataTuple, errorcode)

def MultibeamParameters(fileobject,packetSize):

	#start  049h 73d
	#end 069h
	#remote info 070h
	errorcode = 0 #initalize the error code

	binarydata = fileobject.read(16)
	dataTupleFirst = struct.unpack('<HLLHHH',binarydata)
	


	asciiLooper = packetSize - 21 #the 18 bytes already read plus the three at the end
								# if the file contains the 00h byte (the pad byte)
								# it will come out as an ascii null and we can 
								# trim that later

	asciiText = ""

	#thgis portion reads the ascii parts one character at a time as we dont
	#know the size to construct a proper struct command
	#asciiText ends up being a big block of ascii text

	for i in range(0,asciiLooper):
		asciiRead = fileobject.read(1)
		asciiTemp = struct.unpack('<c',asciiRead)
		asciiChar = asciiTemp[0].decode('UTF-8')
		#print(asciiChar[0].decode('UTF-8'))
		asciiText += asciiChar
		

	asciiSplit = asciiText.split(',') #splits the ascii content by comma
									#this might be a problem in the future
									#as a comma could end up in a string somewhere
	asciiSplit.pop() #removes the last and hopefully empty part of the list

	asciiTuple = tuple(asciiSplit) #makes a tuple so we can put all the tuples together
									#at the end

	#probably need a disctionary generator here

	binarydata = fileobject.read(3)
	dataTupleTwo = struct.unpack('<BH',binarydata)

	if dataTupleTwo[0] != 3:

		errorcode = 1

	dataTuple = dataTupleFirst + asciiTuple + dataTupleTwo

	return(fileobject,dataTuple,errorcode)

def DepthDatagram(fileobject,packetSize):

	#44h is the datagram type for the DepthDatagram

	errorcode = 0

	binarydata = fileobject.read(28)
	dataTupleFirst = struct.unpack('<HIIHHHHHBBBBHH',binarydata)

	#How many repeat cycles?

	repeatCycle = (packetsize - 28 - 4)/ 16
	cycledata =[]

	if repeatCycle % 16 != 0:
		errorcode = 1

	else:
		for x in range(0,repeatCycle):
			binarydata = fileobject.read(16)
			dataTupleCycle = struct.unpack('<hhhhHHBBbB',binarydata)
			cycledata.append(dataTupleCycle)

	binarydata = fileobject.read(4)
	dataTupleSecond = struct.unpack('<bBh',binarydata)

	dataTuple = dataTupleFirst + tuple(cycledata) + dataTupleSecond 

	#alltest.seek(5)
	#binarydata = alltest.read(839)
	# checksum = sum(bytearray(binarydata))
	#the above works to check the checksum, which is interesting
	# should we add it
	
	return(fileobject,dataTuple,errorcode)

def XYZ_88_Datagram(fileObject,packetSize):

	# datagram is type 58h or 88d
	# single repreat cycle on this one

	errorCode = 0

	binarydata = fileObject.read(34)
	dataTupleFirst = struct.unpack('<HII4HfHHf4B',binarydata)

	cycleData= []
	repeatCycle = dataTupleFirst[8]

	depth = []
	acrosstrack = []
	alongtrack = []
	detectionwindow = []
	quality = []
	BAIadjust = []
	detection = []
	realtime_cleaning = []
	reflectivity = []

	for x in range(0,repeatCycle):
		binaryData = fileObject.read(20)
		dataTupleCycle = struct.unpack('<fffHBbBbh',binaryData)

		#for x in range(0,9):
		#	cycleData.append(dataTupleCycle[x]) #reads each value from the tuple which is always 9 long
		depth.append(dataTupleCycle[0])
		acrosstrack.append(dataTupleCycle[1])
		alongtrack.append(dataTupleCycle[2])
		detectionwindow.append(dataTupleCycle[3])
		quality.append(dataTupleCycle[4])
		BAIadjust.append(dataTupleCycle[5])
		detection.append(dataTupleCycle[6])
		realtime_cleaning.append(dataTupleCycle[7])
		reflectivity.append(dataTupleCycle[8])

	binaryData = fileObject.read(4)
	dataTupleTwo = struct.unpack('<BBH',binaryData)

	#dataTuple = dataTupleFirst

	return(fileObject, dataTupleFirst, depth, acrosstrack, alongtrack, detectionwindow, quality, BAIadjust, detection, realtime_cleaning, reflectivity, errorCode)
	

def RuntimeParametersDatagram(fileobject,packetSize):

	# datagram is always type 52h, 82d

	errorcode = 0

	binarydata = fileobject.read(50)
	dataTuple = struct.unpack('<HIIHH6B5Hb5BH4BHhBBH',binarydata)

	binaryMode = dataTuple[9]

	# please refer to the python bitwise operators notes

	#Ping Mode
	pingmode = 'none'
	TXPulseForm = 'none'
	DualSwath = 'none'


	if (binaryMode & 0b00000111) == 0:
		#print("Ping Mode is very shallow")
		pingmode = 'veryshallow'

	elif (binaryMode & 0b00000111) == 1:
		#print("Ping Mode is shallow")
		pingmode = 'shallow'

	elif (binaryMode & 0b00000111) == 2:
		#print("Ping Mode is medium")
		pingmode = 'medium'

	elif (binaryMode & 0b00000111) == 3:
		#print("Ping Mode is deep")
		pingmode = 'deep'

	elif (binaryMode & 0b00000111) == 4:
		#print("Ping Mode is very deep")
		pingmode = 'verydeep'

	elif (binaryMode & 0b00000111) == 5:
		#print("Ping Mode is very deep")
		pingmode = 'extradeep'

	#TX Pulse Form

	if (binaryMode & 0b00110000) == 0:
		#print("TX Pulse form is CW")
		TXPulseForm = 'CW'

	elif (binaryMode & 0b00110000) == 16:
		#print("TX Pulse Form is Mixed")
		TXPulseForm = 'Mixed'

	elif (binaryMode & 0b00110000) == 32:
		#print("TX Pulse Form is FM")
		TXPulseForm = 'FM'

	#Dual Swath

	if (binaryMode & 0b11000000) == 0:
		#print("Dual Swath is off")
		DualSwath = 'off'

	elif (binaryMode & 0b11000000) == 64:
		#print("Dual Swath is fixed")
		DualSwath = 'Fixed'

	elif (binaryMode & 0b11000000) == 128:
		#print("Dual Swath is dynamic")
		DualSwath = 'Dynamic'


	return(fileobject,dataTuple,errorcode, pingmode, TXPulseForm, DualSwath)

def SoundSpeedProfileDatagram(fileObject,packetSize):

	# datagram is always 55h 85d

	errorCode = 0

	binaryData = fileObject.read(26)
	dataTupleFirst = struct.unpack('<HIIHHIIHH',binaryData)

	repeatCycle = dataTupleFirst[7] 
	
	cycleData = []

	for x in range(0,repeatCycle):
			binaryData = fileObject.read(8)
			dataTupleCycle = struct.unpack('<II',binaryData)
			cycleData.append(dataTupleCycle[0]) 
			cycleData.append(dataTupleCycle[1])
	

	# DAMM SPARE BYTE AGAIN!
	binaryData = fileObject.read(1)
	spareByteTest = struct.unpack('<B',binaryData)

	if spareByteTest[0] == 0:
		binarydata = fileObject.read(3)
		dataTupleTwo = struct.unpack('<BH',binarydata)

	else:
		binaryData = fileObject.read(2)
		checkSum = struct.unpack('<H',binaryData)
		dataTupleTwo = spareByteTest + checkSum

	dataTuple = dataTupleFirst + tuple(cycleData) + dataTupleTwo

	return(fileObject, dataTuple, errorCode)

def PositionDatagram(fileObject,packetSize):

	#datagram is always 50h 80d

	errorCode = 0

	binaryData = fileObject.read(32)
	dataTupleFirst = struct.unpack('<HIIHHii4HBB',binaryData)

	#we have an unknown ascii block here, the actual 
	#nav string put into the system
	#figure it out by packetSize - 32 - 3 (end) -2 (bytes stripped from six bytes)

	asciiBlockSize = packetSize - 32 - 3 - 2

	asciiText = ""

	for i in range(0,asciiBlockSize):
		asciiRead = fileObject.read(1)
		asciiTemp = struct.unpack('<s',asciiRead)
		asciiChar = asciiTemp[0].decode('UTF-8')
		asciiText+=asciiChar[0]

	

	binaryData = fileObject.read(3)
	dataTupleTwo = struct.unpack('<BH',binaryData)

	dataTuple = dataTupleFirst + tuple([asciiText])+ dataTupleTwo

	return(fileObject, dataTuple, errorCode)

def NetworkAttitudeVelocityDatagram(fileObject,packetSize):

	#datagram is allways 6Eh, 110d

	errorCode = 0

	#starts reading the normal first 18 bytes

	binaryData = fileObject.read(18)
	dataTupleFirst = struct.unpack('<HII3HbB',binaryData)

	#get the numbers of entries for the repeat cycle

	repeatCycle = dataTupleFirst[5] 
	
	#initalize cycle Data
	cycleData = []

	#run the cycle - note this one also includes a but of ascii data in it

	for x in range(0,repeatCycle):
		
		asciiText = "" #init at the start of every loop

		binaryData = fileObject.read(11)
		dataTupleCycle = struct.unpack('<H3hHB',binaryData)
			
		for x in range(0,6):
			cycleData.append(dataTupleCycle[x]) #reads each value from the tuple which is always 6 long

		for i in range(0,dataTupleCycle[5]):			#this is the ascii part
			asciiRead = fileObject.read(1)				#it is borrowed from the other parts of the 
			asciiTemp = struct.unpack('<s',asciiRead)
			asciiChar = asciiTemp[0].decode('UTF-8')	#script it can include binary data
			asciiText+=asciiChar[0]						#future versions will have to read what type
														#of input datagram it is and splice if needed
		cycleData.append(asciiText)		#just appends the entire loop together

	# DAMM SPARE BYTE AGAIN!
	binaryData = fileObject.read(1)    # this reads ahead and then we will test
	spareByteTest = struct.unpack('<B',binaryData)

	if spareByteTest[0] == 0:				# the spare fucking byte is there
		binarydata = fileObject.read(3)
		dataTupleTwo = struct.unpack('<BH',binarydata)

	else:									#the spare byte isnt there like a good fricking fileformat
		binaryData = fileObject.read(2)
		checkSum = struct.unpack('<H',binaryData)
		dataTupleTwo = spareByteTest + checkSum

	dataTuple = dataTupleFirst + tuple(cycleData)+ dataTupleTwo  # add them all up

	return(fileObject, dataTuple, errorCode)

def RawRangeAndBeamAngleDatagram(fileObject,packetSize):

	#raw range and beam angle 78 datagram 4Eh 78d

	# this crazy asshole has two repeat cycles

	errorCode = 0

	#starts reading the normal first 18 bytes

	binaryData = fileObject.read(30)
	dataTupleFirst = struct.unpack('<HII6HfI',binaryData)

	numberTransmitSectors = dataTupleFirst[6]
	numberRecieverBeams = dataTupleFirst[7]

	#first repeat cycle 

	cycleData= []

	for x in range(0,numberTransmitSectors):
		binaryData = fileObject.read(24)
		dataTupleCycle = struct.unpack('<hH3fHBBf',binaryData)

		for x in range(0,9):
			cycleData.append(dataTupleCycle[x]) #reads each value from the tuple which is always 9 long

	for x in range(0,numberRecieverBeams):
		binaryData = fileObject.read(16)
		dataTupleCycleTwo = struct.unpack('<hBBHBbfhbB',binaryData)

		for x in range(0,10):
			cycleData.append(dataTupleCycleTwo[x]) #reads each value from the tuple which is always 10long

	binaryData = fileObject.read(4)
	dataTupleTwo = struct.unpack('<BBH',binaryData)

	dataTuple = dataTupleFirst + tuple(cycleData)+ dataTupleTwo  # add them all up

	return(fileObject, dataTuple, errorCode)

def SeabedImageData89Datagram(fileObject,packetSize):

	# seabed image data 59h 89d

	# this crazy asshole has two repeat cycles or a cycle in a cyle?
	# looks like it give out info about the samples in the first loop
	# then we read the samples in the second loop?  Its really bad


	errorCode = 0

	#our normal opening bytes
	# the number of valid beams is the last integer

	binaryData = fileObject.read(30)
	dataTupleFirst = struct.unpack('<HIIHHfHhh3H',binaryData)

	numberValidBeams = dataTupleFirst[11]

	cycleData= []
	sampleMap = []
	sampleList = []

	#this first loop reads info on the samples
	# I assume loop is akin to a ping
	# it does have a byte that we need to inspect bit by bit to 
	# get information on if it was rejected
	#which is shiiiiiiittty

	for x in range(0,numberValidBeams):
		binaryData = fileObject.read(6)
		dataTupleCycle = struct.unpack('<bBHH',binaryData)

		for x in range(0,4):
			cycleData.append(dataTupleCycle[x]) #reads each value for the tupe
			
		sampleMap.append(dataTupleCycle[2])#we are building a "map" of 
												# the number of sample for each ping

	#this second loop reads the length of the sampleMap
	# then loops again reading the samples for each ping - getting the length 
	#fro sampleMap
	# i think this is how it works this file format if garbage
	# then it builds a list of lists containing the sample values

	#print sampleMap

	for x in range(0,len(sampleMap)):

		tempList = []
		
		for y in range(0,sampleMap[x]):

			binaryData = fileObject.read(2)
			dataTupleCycleTwo = struct.unpack('<h',binaryData)
			tempList.append(dataTupleCycleTwo[0])

		sampleList.append(tempList)

	binaryData = fileObject.read(4)
	dataTupleTwo = struct.unpack('<BBH',binaryData)

	dataTuple = dataTupleFirst + tuple(cycleData)+ dataTupleTwo 

	return(fileObject,dataTuple,sampleList,errorCode) 
	# so this one returns a bunch of
	# stuff and thats not standard
	# lets just keep it like this for now but in the future we might 
	# need to think of what we are doing

def HeadingDatagram(fileObject, packetSize):

	#heading is always 048h or 72d for normal people
	errorCode = 0

	# begin reading the first 16 bytes

	binaryData = fileObject.read(16)
	dataTupleFirst = struct.unpack('<HIIHHH',binaryData)

	# of course we have another cycler in this one

	repeatCycle = dataTupleFirst[5]

	cycleData= []

	for x in range(0,repeatCycle):
		binaryData = fileObject.read(4)
		dataTupleCycle = struct.unpack('<HH',binaryData)

		cycleData.append(dataTupleCycle[0])
		cycleData.append(dataTupleCycle[1])

		#clearly we are just making a tuple to get this packet read
		#in the future we might want to make a list here 

	binaryData = fileObject.read(4)
	dataTupleTwo = struct.unpack('<BBH',binaryData)

	dataTuple = dataTupleFirst + tuple(cycleData)+ dataTupleTwo 

	return(fileObject,dataTuple,errorCode) 

def AttitudeDatagram(fileObject, packetSize):

	#"A" type datagram 041h or 65d

	errorCode = 0

	# this datagram just has once cycler

	binaryData = fileObject.read(16)
	dataTupleFirst = struct.unpack('<HIIHHH',binaryData)

	repeatCycle = dataTupleFirst[5]

	cycleData= []

	for x in range(0,repeatCycle):
		binaryData = fileObject.read(12)
		dataTupleCycle = struct.unpack('<HHhhhH',binaryData)

		for x in range(0,6):
			cycleData.append(dataTupleCycle[x]) #reads each value from the tuple which is always 10longcycleData.append(dataTupleCycle[0])
		
	binaryData = fileObject.read(4)
	dataTupleTwo = struct.unpack('<BBH',binaryData)

	#the first value in dataTupleTwo is one of these status bytes

	dataTuple = dataTupleFirst + tuple(cycleData)+ dataTupleTwo 

	return(fileObject,dataTuple,errorCode) 



def ClockDatagram(fileObject, packetSize):

	# C clock datagram is 043h 67d
	# just a straightforward one finally

	#rewind test
	fileObject.seek(-1,1)
	datagramTypeTestBin = fileObject.read(1)
	datagramTestTuple = struct.unpack('<B',datagramTypeTestBin)

	errorCode = [0]

	#tessting a datagram test function.
	#if we were to use this i suggest the error code becomes a list

	if datagramTestTuple[0] != 67: errorCode[0] = 10
	fileObject.seek(-1,1)

	#in addition I have added a rewind to capture the 
	#entire bbytes between the start identifier 
	#and the end so we can calc a check sum
	#this is experimental but the method should work the same as
	#the others

	binaryData = fileObject.read(27)
	dataTuple = struct.unpack('<BHIIHHIIBBH',binaryData)

	#do the checksum test for fun
	
	testTuple = struct.pack('<BHIIHHIIB',*dataTuple[0:9])

	checksum = sum(bytearray(testTuple))

	#print checksum, " ", dataTuple[10]
	
	if checksum != dataTuple[10]: errorCode.append('5')

	#all that above worked 
	#to keep it the same as the others I add these two parts

	dataTuple = dataTuple[1:]
	errorCode = 0


	return(fileObject,dataTuple,errorCode) 

def PUStatusOutput(fileObject, packetSize):

	# this is a dataoputput packet
	# 31h or 49d
	errorCode = 0

	binaryData = fileObject.read(86)
	dataTuple = struct.unpack('<HII4H6I5bBH3hHIhBB3bBHBBH3hbBH',binaryData)

	return(fileObject,dataTuple,errorCode) 

def PacketMapper(fileObject):

	import collections

	# this is a potential future expansion
	# probably should write this to a file I guess
	# this is just experimental gto see what packets we have

	fileObject.seek(0,0)
	fileObject.seek(0,2)
	lengthOfFile = fileObject.tell()
	fileObject.seek(0,0)

	filepos = 0


	listOfPacketTypes = []
	firstSite = 0

	
	while filepos < lengthOfFile:

		fileObject, dataTuple, error = AllSixBytes(fileObject)
		filePosCycle = []
		tempList = []
		
		if dataTuple[2] == 107:
			startPos = fileObject.tell()
			fileObject.seek(10,1)
			binarydata = fileObject.read(8)
			pingTuple = struct.unpack("<HHHH",binarydata)
			tempList =( dataTuple[0] , dataTuple[2], startPos, pingTuple[0], pingTuple[2], pingTuple[3])
			#print tempList
			fileObject.seek(-18,1)
			listOfPacketTypes.append(tempList)
			
		else:
			tempList =( dataTuple[0] , dataTuple[2], fileObject.tell(), 0, 0, 0)
			listOfPacketTypes.append(tempList)
		#filePosCycle.append(fileObject.tell())
		#print filePosCycle
		#dataTuple = dataTuple + tuple([filePosCycle[0]])
		
		# uncomment this to search for a type of packet
		#if dataTuple[2] == 71: #and firstSite == 0:
		#	print " ################################################"
		#	print '{},{},{},{}'.format(*dataTuple)
		#	print "################################################"
		#	firstSite = 666
		#print dataTuple[0]," ",dataTuple[1]," ",dataTuple[2]," ",dataTuple


		skipBytes = dataTuple[0]
		
		fileObject.seek(-2,1)
		
		fileObject.seek(skipBytes,1)
		filepos = fileObject.tell()
		#print filepos
	
	#we are going to try to see if we have all the packet types.
	

	#dictOfPacketTypes = collections.Counter(listOfPacketTypes)
	
	
	#listOfPacketKeys = dictOfPacketTypes.keys()

	#listOfAllPacketTypes = []	
	#uncomment this out to add up all the packet types
	#for x in range(0,len(listOfPacketKeys)):

	#	if listOfPacketKeys[x] in listOfAllPacketTypes:
	#		pass
	#	else: 
	#		listOfAllPacketTypes.append(listOfPacketKeys[x])

	#print sorted(listOfAllPacketTypes)


	#print collections.Counter(listOfPacketTypes)

	return(listOfPacketTypes)

def WaterColumnDatagram(fileObject, packetSize):

	# k datagram is always 6Bh or 107d

	errorCode = 0

	# this datagram has two cyclers 
	# the second cycler has samples in it, unlike the seabed imange that
	# where all the samples came at the end

	# read the first chunk
	binaryData = fileObject.read(38)
	dataTupleFirst = struct.unpack('<HII8HIhBbB3B',binaryData)

	# the 
	numberOfDatagrams = dataTupleFirst[5]
	numberOfTransmitSectors = dataTupleFirst[7]
	numberOfBeams = dataTupleFirst[9]

	
	dataListSecond = []
	dataListThird = []
	mapList = []
	sampleMap = []
	sampleList = []

	
	for x in range(0,numberOfTransmitSectors):
		binaryData = fileObject.read(6)
		dataTupleCycle = struct.unpack('<hHBB',binaryData)
		
		for y in range(0,4):
			dataListSecond.append(dataTupleCycle[y])

 		
	for x in range(0,numberOfBeams):
		binaryData = fileObject.read(10)
		dataTupleCycle = struct.unpack('<h3HBB',binaryData)
		mapList.append(dataTupleCycle[2])
		
		for y in range(0,6):
			dataListThird.append(dataTupleCycle[y])

		tempList = []

		for z in range(0,dataTupleCycle[2]):

			binaryData = fileObject.read(1)
			dataSampleTuple = struct.unpack('<b',binaryData)
			tempList.append(dataSampleTuple[0])

		sampleList.append(tempList)

	# DAMM SPARE BYTE AGAIN!
	binaryData = fileObject.read(1)    # this reads ahead and then we will test
	spareByteTest = struct.unpack('<B',binaryData)

	if spareByteTest[0] == 0:				# the spare fucking byte is there
		binarydata = fileObject.read(3)
		dataTupleFinal = struct.unpack('<BH',binarydata)

	else:									#the spare byte isnt there like a good fricking fileformat
		binaryData = fileObject.read(2)
		checkSum = struct.unpack('<H',binaryData)
		dataTupleFinal = spareByteTest + checkSum

	dataTuple = dataTupleFirst + tuple(dataListSecond) + tuple(dataListThird) + dataTupleFinal
	#dataTuple = dataTupleFirst + tuple(dataListThird) + dataTupleFinal

	return(fileObject,dataTuple,sampleList,errorCode) 

def WaterColumnDatagram_ForWCD(fileObject, packetSize, packetMap, packetMapPosition, continuation, angleList, rangeList, sampleList):
														 	
	errorCode= 0
	pingNumber = packetMap[packetMapPosition][3]
	# k datagram is always 6Bh or 
	#ok the tricky bit about this reader is the data can be split betewwn several
	# datagrams and we arent sure if they are continous
	
	# so  packet mapper needs to be run
	# this will produce a list of lists that give the starting point of the packet
	# (actually two bytes in) so packet mapper produces:
	# size of packet, type of packet, position in file, ping number, number of datagrams, current datagram
	
	# where are we in the packet map and what data are we looking at?
#	if len(packetMap) != 0:
		
#		mapLocation = packetMap[packetMapPosition]
#		nextMapedPacket = packetMap[packetMapPosition + 1] # this will fail at the end of the file
		
#	else:
#		print 'needs to run packet mapper to use this function'
		
	#im going to define the packet reader first then the logic comes later

	def WaterColumnDataCapture(fileObject,packetMap,packetMapPosition,continuation, angleList, rangeList, sampleList):
		#this has been modified to read the angles
		# and calculate the ranges 
		# for this datagra
		# logjc afterwards will append them to existing 
		# lists if needed
		# it also makes a list of lists for the samples
		# read the first chunk
		
		#unlike other rippers we are going to make sure we are in the right spot first
		# as the file object might not be in the right spot due to notmrunning allsix bytes
		tempFilePos = packetMap[packetMapPosition][2]
		fileObject.seek(tempFilePos)
		#print packetMap[packetMapPosition][2]
		#print fileObject.tell()
		
		binaryData = fileObject.read(38)
		dataTupleFirst = struct.unpack('<HII8HIhBbB3B',binaryData)
		TEMP_TIME_MIDNIGHT = dataTupleFirst[2] / 100
		# the 
		####added shit here
		TEMP_PING_COUNTER = dataTupleFirst[3]
		#numberOfDatagrams = dataTupleFirst[5]
		
		numberOfTransmitSectors = dataTupleFirst[7]
		#print numberOfTransmitSectors
		numberOfBeams = dataTupleFirst[9]
		soundSpeed = dataTupleFirst[10] * 0.1
		sampleDetectionFrequency = dataTupleFirst[11] * 0.01
		#print("sample detection freq", sampleDetectionFrequency)
		#print("SoundSpeed", soundSpeed)
	
		transmitListSecond = []
		dataListThird = []
		mapList = []
		sampleMap = []
		transmitPingTilt = []
		
		
		
		#listtest = range(0,8)
		#print(range(0,numberOfTransmitSectors))
		#print(listtest)
		for x in range(0, numberOfTransmitSectors):
			#print x
			binaryData = fileObject.read(6)
			dataTupleCycle = struct.unpack('<hHBB',binaryData)
			pingtilt = dataTupleCycle[0] * 0.01
			transmitPingTilt.append(pingtilt)
			pingTransSector = dataTupleCycle[2]
			#print('$$$$ TRANSMIT DATA $$$$ ping {},time {}, transmit sectors {}, tilt {}, transmit Sector {}'.format(TEMP_PING_COUNTER, TEMP_TIME_MIDNIGHT ,numberOfTransmitSectors, pingtilt, pingTransSector))
			dataListSecond =[]
			
			for y in range(0,4):
				dataListSecond.append(dataTupleCycle[y])
		
			transmitListSecond.append(dataListSecond)

 		
		for x in range(0,numberOfBeams):
			binaryData = fileObject.read(10)
			dataTupleCycle = struct.unpack('<h3HBB',binaryData)
			mapList.append(dataTupleCycle[2])
			angleList.append(dataTupleCycle[0] * .01) #find the angle
		
			for y in range(0,6):
				dataListThird.append(dataTupleCycle[y])
		
			tempList = []
			tempRange = []
			#tempList.append(dataTupleCycle[0])
		
			for z in range(0,dataTupleCycle[2]):

				binaryData = fileObject.read(1)
				dataSampleTuple = struct.unpack('<b',binaryData)
				tempList.append(dataSampleTuple[0]) #supposedly in 0.5 db format
				tempRange.append((z * (1 / sampleDetectionFrequency) * soundSpeed))
				
			rangeList.append(tempRange)
			sampleList.append(tempList)
			
		# DAMM SPARE BYTE AGAIN!
		binaryData = fileObject.read(1)    # this reads ahead and then we will test
		spareByteTest = struct.unpack('<B',binaryData)

		if spareByteTest[0] == 0:				# the spare fucking byte is there
			binarydata = fileObject.read(3)
			dataTupleFinal = struct.unpack('<BH',binarydata)

		else:									#the spare byte isnt there like a good fricking fileformat
			binaryData = fileObject.read(2)
			checkSum = struct.unpack('<H',binaryData)
			dataTupleFinal = spareByteTest + checkSum
		
		#print sampleList
		#print len(sampleList)
		#print len(rangeList)
		return(fileObject,angleList,rangeList,sampleList,transmitPingTilt, TEMP_TIME_MIDNIGHT) 
		
#lets think of some conditions
	# first this functiin has been called because 
	# mcp wants a wcd packet read
	# but we might have a continuatikn flag set so lets see if there is a flag and then run
	# the reader	
	
	def packetForcaster(packetMap,packetMapPosition,keepReading, continuation): 
		
		if packetMapPosition < len(packetMap) - 1 :

			#print("position", packetMapPosition)
			#print(len(packetMap))

			
			nextPosition = packetMapPosition + 1
			nextPacketType = packetMap[nextPosition][1]
			nextPacketPing = packetMap[nextPosition][3]
			#print "next packet position", nextPosition
			
			moarPackets = packetMap[packetMapPosition][4]  > packetMap[packetMapPosition][5]
			#print "moar packets", packetMap[packetMapPosition][4], packetMap[packetMapPosition][5], moarPackets, nextPacketType

			
			if nextPacketType == 107 and moarPackets:
				#print "first logic"
				keepReading = True
				continuation = 1
			
			elif nextPacketType == 107 and packetMap[packetMapPosition][4]  == packetMap[packetMapPosition][5]:
				#print "second logic"
				keepReading = False
				continuation = 0
				
			elif nextPacketType != 107:
				#print "third logic"
				if packetMap[packetMapPosition][4] == packetMap[packetMapPosition][5]:
					#print "fourth logic"
					keepReading = False
					continuation = 0
					#print "contuniation",continuation
				else:
					#print "fifth logic"
					keepReading = False
					continuation = 1

			
			
			else:
				
				keepReading = False
				#print ("logic failure in packetforecaster", packetMapPosition)
				
		else:
				#print "sixth logic"
				keepReading = False
				continuation = 0

		return(packetMap, packetMapPosition, keepReading, continuation)
	
	
	#down at the bottom is the part of the scrips that runs the rest
	# the first time this function is called the continuation is set at 0
	# and therefore the wcd ping is "new"
	# so all of the 
	
		
	keepReading = True
			
		
	while keepReading == True:
	
		if continuation == 0: #no flag - and therefore the first read
			
			angleList = []
			rangeList=[]
			sampleList = []
			fileObject, angleList, rangeList, sampleList, transmitPingTilt, timeseconds = WaterColumnDataCapture(fileObject,packetMap,packetMapPosition,continuation,angleList, rangeList, sampleList)
			
			packetMap, packetMapPosition, keepReading, continuation = packetForcaster(packetMap, packetMapPosition, keepReading,continuation)
			
			if keepReading == True:
			
				packetMapPosition += 1
			
			
		
			
		
		elif continuation == 1: # this means there was a inturrupting packet
			
			fileObject, angleList, rangeList, sampleList, transmitPingTilt, timeseconds = WaterColumnDataCapture(fileObject, packetMap, packetMapPosition, continuation, angleList, rangeList, sampleList)
			
			packetMap, packetMapPosition, keepReading, continuation = packetForcaster(packetMap,packetMapPosition, keepReading, continuation)
			
			if keepReading == True:
				packetMapPosition += 1
			
		
				
	
		else:
		
			print("continuation needs to be 1 or 0")
	#our logic to keep reading packets or return to wcd engine as finished or
	# to read an interrupting packet	
			
	return(fileObject, packetSize, packetMap, packetMapPosition, continuation, angleList, rangeList, sampleList ,pingNumber, transmitPingTilt, timeseconds) 
	

def KongsbergMaritimeSSPoutputDatagram(fileObject, packetSize):

	# datagram is always 057h or 87d

	errorCode = 0

	# this datagram has one cycler
	#and a spare byte
	# because the cycled part is a strung I'm just going to extend it 
	# to also copy the byte if it is there


	# read the first chunk
	binaryData = fileObject.read(14)
	dataTupleFirst = struct.unpack('<HIIHH',binaryData)
	
	cycleAscii = ""

	repeatCycle = packetSize - 2 - 14 - 3 #the two bytes from AllSix, the first part, and the end bytes

	for x in range(0,repeatCycle):
		binaryData = fileObject.read(1)
		dataTupleCycle = struct.unpack('<s',binaryData)
		cycleAscii += dataTupleCycle[0]

	binarydata = fileObject.read(3)
	dataTupleFinal = struct.unpack('<BH',binarydata)
	
	dataTuple = dataTupleFirst + tuple([cycleAscii]) + dataTupleFinal

	return(fileObject, dataTuple, errorCode)

def ExtraParammetersDatagram(fileObject, packetSize):

	# datagram is always 033h or 51d

	errorCode = 0

	# this datagram has one cycler
	#and a spare byte
	# because the cycled part is a string I'm just going to extend it 
	# to also copy the byte if it is there


	# read the first chunk
	binaryData = fileObject.read(16)
	dataTupleFirst = struct.unpack('<HII3H',binaryData)
	
	cycleAscii = ""

	repeatCycle = packetSize - 2 - 16 - 4 #the two bytes from AllSix, the first part, and the end bytes

	for x in range(0,repeatCycle):
		binaryData = fileObject.read(1)
		dataTupleCycle = struct.unpack('<s',binaryData)
		cycleAscii += dataTupleCycle[0]

	binarydata = fileObject.read(4)
	dataTupleFinal = struct.unpack('<BBH',binarydata)
	
	dataTuple = dataTupleFirst + tuple([cycleAscii]) + dataTupleFinal

	return(fileObject, dataTuple, errorCode)

def SurfaceSoundSpeed(fileObject, packetSize):

	errorCode = 0
	#datagram is always 47h or 71d
	# it has one looper

	binaryData = fileObject.read(16)
	dataTupleFirst = struct.unpack('<HII3H',binaryData)

	cycleData = []


	for x in range(0,dataTupleFirst[5]):
		binaryData = fileObject.read(4)
		dataTupleCycle = struct.unpack('<HH',binaryData)
		cycleData.append(dataTupleCycle[0])
		cycleData.append(dataTupleCycle[1])

	binarydata = fileObject.read(4)
	dataTupleFinal = struct.unpack('<BBH',binarydata)

	dataTuple = dataTupleFirst + tuple(cycleData) + dataTupleFinal

	return(fileObject, dataTuple, errorCode)


def FileLooper(inFiles):

	inputFiles = open(inFiles,'r')
	listOfAllPacketTypes = [] #pretty stupid to have to initalize this here but whatevs

	for x in inputFiles:

		y = x.rstrip()
		dataFile = open(y,'rb')
		#print y
		listOfAllPacketTypes = PacketMapper(dataFile,listOfAllPacketTypes)






















































































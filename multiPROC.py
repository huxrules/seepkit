import sys
import traceback
import numpy
import multiprocessing
import queue
from time import sleep

import sonar_data_control as SDC



def multiprocessLineLoad(args):
	filestring,proc = args
	
	try:
		print("#### STARTING {}#####".format(proc))
		c = SDC.wcd_reader_with_model(filestring, proc)
		print("###### Worker {} Returns!#####".format(proc))
		print(c)
		#if there is an output file it would go here
	except:
		errorTrace = traceback.format_exc()
		errorString = "#"*60 + "\n" + "LINE LOAD ERROR - MULTIPROCESSLINELOAD" "\n" + filestring + "\n" + errorTrace + "\n" + "#"*60
		print(errorString)	

def createProcesses(fileList, output):

		numberOfFiles = len(fileList)


			#self.threadpool = QtCore.QThreadPool()
		"""
			selffileArray = []

			lineStatus = "New"
			dataAvailable = "water Column"

			for i in range(0,self.numberoffiles):
				self.fileProgressList = [i,self.Loadfiles[i], self.currentProjectUUID, lineStatus, dataAvailable, 0,0,0,0,0,0,0,0,0,0,0,0,'nolineuuid',0,0,0] # 0 process number, 1 filename, 2 projectUUID, 3 linestatus, 4 dataAvailable,5 prog readfile,6 end readfile,7 prog preproject,8 end preproject,9 prog sideview,10 end sideview,11 prog tripwire,12 end tripwire, 13 read flag, 14 preprocess flag, 15 sideviewflag, 16 tripwire flag, 17 line uuid)  
				self.fileArray.append(self.fileProgressList)																								# 18 prog hist, 19 hist end, 20 hist flag
		"""
		#manager = multiprocessing.Manager()
		#ErrorQ = manager.Queue()
		commands = []
		procNum = 0
		for i in fileList:
				commands.append([i,procNum])
				procNum +=1 
		print(commands)
		filereaderpool = multiprocessing.Pool(processes = 4, maxtasksperchild = 1)
		for x in filereaderpool.imap(multiprocessLineLoad, commands):
			print(x)

		#while True:
		#		sleep(2)
		#		if not results.ready():
		#			print("######## standing by for any errors ########")
		#		elif results.ready():
		#			print(results.get())
		#			break




from skimage.transform import resize

import numpy
import traceback


"""
import os


import sys
osname = sys.platform

if osname == 'linux':

	sys.path.append('/home/huxrules/SeepIntelPro/MASTEREXPLODER/MCP')

elif osname == 'darwin':
	sys.path.append('/Users/huxrules/MASTER_EXPLODER/GIT_ME/MASTEREXPLODER/MCP')
	#tensorboard = TensorBoard(log_dir="/Users/huxrules/MASTER_EXPLODER/GIT_ME/MASTEREXPLODER/MISC/logs/{}".format(time()))"""

import mcp3 as MCP
import sonar_data_store3 as SDS 

class WCDPredictor(object):

	def __init__(self):
		"""
		import keras.backend as K
		import tensorflow as tf

		num_cores = 2
		config = tf.ConfigProto(intra_op_parallelism_threads=num_cores,\
		inter_op_parallelism_threads=num_cores, allow_soft_placement=True,\
		device_count = {'CPU' : 1, 'GPU' : 0})
		session = tf.Session(config=config)
		K.set_session(session)"""

		from keras.models import model_from_json


  

		json_file = open('../models/classifier_series_1_series_2.json') 
		loaded_model_json = json_file.read() 
		json_file.close() 
		self.classifier = model_from_json(loaded_model_json) 
		self.classifier.load_weights('../models/classifier_series_1_series2.h5') 


	
		#opt = keras.optimizers.Adam( lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
		#self.classifier.compile(optimizer = opt, loss = 'binary_crossentropy', metrics = ['accuracy'])

	def run_prediction(self,WCDArray):
		WCD4DArray = numpy.zeros((1,300,300,1))
		WCDArray[WCDArray < -129] = -128
		WCDArray[WCDArray > 126] = 0
		WCDArray = numpy.flipud((WCDArray) )
		WCDArray = resize(WCDArray, (300, 300), anti_aliasing = True)
		WCD3DArray = numpy.expand_dims(WCDArray, axis = 3)
		WCD3DArray = numpy.asarray(WCD3DArray, dtype='float32')
		WCD4DArray[0] = WCD3DArray
		result = self.classifier.predict(WCD4DArray)
		return(result)





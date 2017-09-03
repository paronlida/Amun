#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info('powerS:OK')
#---------------------------------------------------------------------
#relevants

class powerS(obj):
	def __init__(self,parent,info,preId,objid):
		obj.__init__(self,parent,info,preId,objid)
		#zero------------------------------------------------
		self.tStatus=0
		self.status=0
		#-----------------------------------------------------

	def compose(self, to):
		if to=='agentS':#setup
			msg=self.index+',s'
		elif to=='agent':#cmd
			msg=self.index+',c,'+str(self.tStatus)
		elif to=='client':
			msg=self.clientAddr+','+str(self.auto)+','+str(self.status)
		return msg

	def process (self, _input):
		logger.debug(self.name +' process')
		try:
			if int(_input[0]) in [0,1]:
				self.tStatus=int(_input[0])
			else:
				raise ValueError
			self.agent.send(self.compose('agent'))
		except ValueError:
			#log
			pass

	def aProcessor(self, _input):
		try:
			if int(_input[0]) in [0,1]:
				self.status=int(_input[0])
			else:
				raise ValueError
			self.informAll()
		except ValueError:
			#log
			pass

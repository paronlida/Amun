#import
import importlib
import logging
import threading
import infra.config as config

obj=importlib.import_module(config.obj).amunobj

logger = logging.getLogger('mainLogger')
logger.info('window:OK')
#------------------------------------------------------------------------------------------
class window(obj):
	def __init__(self,parent,info,preId,objid):
		obj.__init__(self,parent,info,preId,objid)
		#zero------------------------------------------------
		self._blen=0
		self._win=0
		self._mode=1
		self.winislvl=0
		self.winshlvl=0
		self.blnislvl=0
		self.blnshlvl=0
		self.cmdid=0
		self.condition=None
		self._weight=50
		self.speed=0
		#-----------------------------------------------------
		
	@property
	def weight(self):
		return self._weight
	@weight.setter
	def weight(self,value):
		try:
			if value>= 0 or value <=100:
				self._auto=value
			else:
				raise ValueError
		except ValueError:
			logger.error('Value Error')

	def status(self):
		self.cmd= 'obj,'+self.index+','+str(self.cmdid)+',s'
		self.client.send(self.cmd)

	def cmdidgen(self):
		if self.cmdid==9:
			self.cmdid=1
		else:
			self.cmdid=self.cmdid+1

	def rellvl (self, change):
		if self._mode == 1:
			self.blnrellvl(change)
		elif self._mode == 2:
			self.winrellvl(change)

	def winrellvl(self,change):
		if change > 0 and self.winislvl==100:
			pass #change to eliminate negatie
		elif change < 0 and self.winislvl==0:
			pass
		else:
			self.winshlvl=change*self._weight+self.winislvl
			logger.debug('shlvl '+str(self.winshlvl))
			self.cmdidgen()
			self.winabslvl(self.winshlvl,self.cmdid)
			self.condition=threading.Condition()
			self.condition.acquire()
			logger.debug('will wait')
			self.condition.wait(200)
			logger.debug('resume')
			self.condition.release()

	def winabslvl(self,value,cmdid):
		try:
			if value>= 0 or value <=100:
				logger.debug(cmdid)
				self.winshlvl=value
				self.cmd= 'obj,'+self.index+',d,'+str(cmdid)+','+str(self.winshlvl)
				self.client.send(self.cmd)
			else:
				raise ValueError		
		except ValueError:
			logger.error('Value Error')

	def blnrellvl(self,change):
		if change > 0 and self.blnislvl==100:
			pass #change to eliminate negatie
		elif change < 0 and self.blnislvl==0:
			pass
		else:
			self.blnshlvl=change*self._weight+self.blnislvl
			logger.debug('shlvl '+str(self.blnshlvl))
			self.cmdidgen()
			self.blnabslvl(self.blnshlvl,self.cmdid)
			self.condition=threading.Condition()
			self.condition.acquire()
			logger.debug('will wait')
			self.condition.wait(200)
			logger.debug('resume')
			self.condition.release()

	def blnabslvl(self,value, cmdid):
		try:
			if value>= 0 or value <=100:
				logger.debug(cmdid)
				self.blnshlvl=value
				self.cmd= 'obj,'+self.index+',b,'+str(cmdid)+','+str(self.blnshlvl)
				self.client.objCmd(self.cmd)
			else:
				raise ValueError		
		except ValueError:
			logger.error('Value Error')

	def feedback (self,cmdid,typ,lvl):
		logger.debug('cmdid:'+str(cmdid)+', typ:'+str(typ)+', lvl:'+str(lvl))
		if cmdid == self.cmdid:
			logger.debug('got'+str(cmdid))
			self.condition.acquire()
			self.condition.notify()
			logger.debug('notify')
			self.condition.release()
		elif cmdid == 0:
			pass
		else :
			logger.warning('nonmatching cmdid')
		try:
			if typ=='b':
				if lvl>= 0 or lvl <=100:
					self.blnislvl=lvl
				else:
					raise ValueError
			elif typ=='d':
				if lvl>= 0 or lvl <=100:
					self.winislvl=lvl
				else:
					raise ValueError
		except ValueError:
			logger.error('Value Error')

	def process (self, _input):
		logger.info('window process')
		try:
			if int(_input[0]) in [0,1]: #client -> mode, target
				self.auto=int(_input[0])
			else:
				pass #####################raise error
			self.blnabslvl(int(_input[1]),0)
			self.parent.objlists[0][0].update()############fix to do only when changing mode
			self.informAll()
		except ValueError: #correct error type
			pass

	def aProcessor(self, _input):
		self.feedback(int(_input[1]),int(_input[2]),int(_input[3]),int(_input[4]),int(_input[5]))
		self.informAll()
''' 
self._mode: mode for auto brightness 1=blinders, 2=window
'''



#import
import importlib
import logging
import threading
import infra.config as config

wcom=importlib.import_module(config.wcom)
gvar=importlib.import_module(config.gvar)
protocols=importlib.import_module(config.protocols)
logger = logging.getLogger('mainLogger')
#---------------------------------------------------------------------
class user(object): 
	def __init__(self,path):
		#user	
		self.filePath=path	#user file as spcified in the structure file
		self.myfile=importlib.import_module(self.filePath)
		self.configs=self.myfile.configs	#read the configs dict
		self.name=self.configs['name']
		self.logId='user-'+self.name+': '
		self.admin=self.configs['admin']
		self.ruleFileName=self.name+'Rules'
		self.events=events(self) #create events list
		#
		#rooms setup
		self.roomlist=gvar.rooms
		self.roomsid=self.configs['rooms']
		self.rooms={}
		for roomid in self.roomsid:
			self.rooms[str(roomid)]=self.roomlist[roomid]
			self.roomlist[roomid].adduser(self) #add user to the room object
		self.clientcreate='s,,,'+str(self.name)+','+str(self.admin)
		for room in self.roomsid:
			self.clientcreate=self.clientcreate+self.rooms[str(room)].roomstring
		#"s,,,1,My room,1,,l,1,main light,,l,2,small light,,a,2,small light";
		#logger.info(self.logId+self.clientcreate)
		#
		self.rulesupdate()
		self.server=wcom.server(self,dict(port=self.configs['port']))
		logger.info(self.logId+'ready')
		print(self.clientcreate)
		

	def rulesupdate(self):#read,compile and excute rules from user file
		self.rules=importlib.import_module(self.filePath).rules
		compiler=compile(self.rules,self.ruleFileName,'exec')
		#try:
		exec(compiler, globals(), locals())
		#except NameError:
		#	logger.error(self.logId+'NameError: compile error')
		

	def process(self,caller,_input): ########################################why not use a director?
		if _input[0]=='s':#setup
			self.server.send(self.clientcreate)
		elif _input[0]=='c':#command
			self.rooms[_input[1]].process(self,_input[2:])
		elif _input[0]=='u':#update
			self.statusUpdate()

	def inform(self,msg): #inform both user and ruleswatcher
		self.nmsg='i,,,'+msg #new message
		self.server.send(self.nmsg)

	def statusUpdate(self): #################################################why not directly inform?
		for room in self.roomsid:
			self.rooms[str(room)].inform(self)

	def shutdown(self):
		pass
#--------------------------------------------------------------------------------------------------
class root(user):
	def __init__(self):
		self.name='root'
		self.admin=True
		self.director=director(self)
		#self.events=events(self)
		self.server=wcom.server(self,dict(port=1000))
		self.rules=importlib.import_module(config.rootRules)
		#terminal port
		self.runstat=1
		threading.Thread(target=self.read).start()
		
	def process(self,_input):
		self.director.direct(_input,admin)

	def manProcess(self,_input):
		self.input=_input
		print('man will do')
		compiled=compile(self.input,self.ruleFileName,'exec')
		#exec(compiled)	#suspended till proper try-except
		

	#terminal port	
	def read(self):
		logger.info('reader starts')
		while self.runstat == 1:
			self._input=input('>>')
			self.test(self._input.split(','))
			#self.director.direct(self._input.split(','),True)

	def test(self, _input):
		gvar.agents[2].objCmd(_input[0]+',0,'+_input[1])
		#gvar.agents[2].objCmd('12,c,0,'+_input[0]+','+_input[1])
	def output(self,output): #what the ...?
		print(output)


	def shutdown(self): #exit flag
		self.runstat=0
#----------------------------------------------------------------------------------------------------
class events(object): 
	def __init__(self,parent):
		self.parent=parent
		self.events=[None]*100

		
	def new(self,_input):
		self._input=_input
		self.typ=_input[0]
		self._time=_input[1]
		self.index=chkfree()
		print(self.index)		
		try:
			if self.typ=='1':
				self.tofloat=time.mktime(time.strptime(self._input[1],"%y:%m:%d:%H:%M:%S"))
				self.after=self.tofloat-time.mktime(time.localtime())
				
			elif self.typ=='2':
				self.after=int(self._time)
		except ValueError:				
			logger.error('wrong time format')
		try:
			if self.after<=0:
				raise ValueError
			self.ev=threading.Timer(self.after,self.execute)
			self.ev.start()
			self.events[self.index]=self.ev
		except ValueError:
			logger.error('wrong schedule value')
		except AttributeError:
			logger.error('wrong schedule type')


	def index(self):
		return self.index

	
	def execute(self):
		self.parent.director.direct(self._input[2:])
		self.event[self.index]=None
		print(self.index)


	def chkfree(self):
		for i in range(100):
			if self.event[i] == None:
				break
				return i


	def timetill(self):
		pass


	def when(self):
		pass


	def _delay(self):
		pass


	def cancel(self):
		pass
#--------------------------------------------------------------------------
class director (object): #that goes into the process method, or?
	def __init__(self, parent):		
		self.parent=parent
		pass
			
	def direct(self,_input,admin):
		try:
			self._input=_input
			self.len=len(self._input)
			if self._input[0]=='p':
				if self._input[1] == 'seth':
					protocols.shutdown(False)
				elif self._input[1]=='ra':
					if not b_ra:
						ra()
						self.ra=True
				else:
					logger.error('unknown protocol')

			elif self._input[0]=='c':
				try:
					self.parent.rooms[int(self._input[1])].process(2,self._input[2:])
				except (IndexError,ValueError):
					logger.error('wrong address')

			elif self._input[0]=='0':
				if admin:
					logger.debug(self._input)
					self.parent.manProcess(inputstr)

			elif self._input[0]=='s':
				if self.len<5:
					raise IndexError
				logger.debug(self._input)
				self.event.new(self,self._input[1:])
			else:
				logger.error('unknown command type')
		except IndexError:
			logger.error('unknown command format')
#-----------------------------------------------------------------
logger.info('user:OK')

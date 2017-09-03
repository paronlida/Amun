import sched, time
import threading
num=[0,1]
list=[0,1]

for i in num:
	list[i] = threading.Condition()


def customer(a,b):
	print('SOMETHING',a,b)
	prd1(a,b)

def prd1(a,b):
	#list[a].acquire()
	while True:
		if input()==b:
			break
	print('notify')
	#list[a].notify() # signal that a new item is available
	#list[a].release()
def mai():
	list[0].acquire()
	list[1].acquire()	
	#list[a].release()
	cat=threading.Thread(target=customer,args=(1,'c'))
	cat.start()
	dog=threading.Thread(target=customer,args=(0,'d'))
	dog.start()
	print('pause')
	cat.join(10)
	dog.join()
	#list[0].wait() # sleep until item becomes available
	#list[1].wait() # sleep until item becomes available
	#list[0].release()
	#list[1].release()
	print('resume')
	print('here')
threading.Thread(target=mai).start()

'''
t=time.strptime("16:10:8:12:50:00", "%y:%m:%d:%H:%M:%S")

#print(time.strftime("%w:%H:%M:%S", time.localtime()))

def dit():
	a=s.enterabs(time.mktime(time.strptime("16:10:8:14:20:00", "%y:%m:%d:%H:%M:%S")), 1, print,argument=('one',))
	b=s.enter(5, 2, print, argument=('two',))
	c=s.enter(5, 1, print, argument=('three',))

s = sched.scheduler(time.time, time.sleep)
se=threading.Thread(target=s.run)
se.setDaemon(False)
dit()

se.start()




class scheduler (object):
	def __init__(self, parent):
		self.director = director(self)
		self.s = sched.scheduler(time.time, time.sleep)
		self.renew()
		self.th=threading.Thread(target=self.s.run,kwargs={'blocking': False})
		self.th.setDaemon(True)
		self.th.start()

	def renew(self):
		self.dummy=self.s.enter(99, 1, self.renew)
		logger.logger.debug('renewing dummy event')
		
	def schedule(self,inputstr):
		self._input=inputstr.split(',')	
		if self._input[0]=='2':
			logger.logger.debug('delay func')
			self.s.enter(int(self._input[1]), int(self._input[2]), self.director.direct, argument=(self._input[3:],))
			#self.s.enter(int(self._input[1]), int(self._input[2]), self.director.direct, argument=(self._input[3:],))
		elif self._input[0]=='1':
			logger.logger.debug(self._input)
			self.s.enterabs(self._input[1],time.strptime(self._input[2],"%y:%m:%d:%H:%M:%S"),self.director.direct, argument=(self._input[3:],))
		elif self._input[0]=='0':
			logger.logger.debug(self._input)
			self.director.direct(self._input[1:])
		else:
			logger.logger.error('unknown command type') 
t='16:10:9:12::00'
tim=time.mktime(time.strptime(t,"%y:%m:%d:%H:%M:%S"))
diff=tim-time.mktime(time.localtime())
print (diff)'''





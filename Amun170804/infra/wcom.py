import logging
import socket
import threading

logger = logging.getLogger('mainLogger')
comm = logging.getLogger('commLogger')


class server(object):
	def __init__(self,parent,info):
		self.parent=parent
		self.caller=2
		self.info=info
		#self.name=self.info['name']
		self.ip ='192.168.0.10'
		self.port=self.info['port']
		self.connected=False
		self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.logger_id='client:'+ str(self.port)+' '
		logger.info(self.logger_id)
		self.s.bind((self.ip,self.port))	
		self.up()
		
		
				
	def up(self):
		self.thread = threading.Thread(target=self.rcvcom)
		self.thread.setDaemon(True)
		self.thread.start()

	def rcvcom(self):
		self.s.listen(1)
		while True:
			self.conn, self.addr = self.s.accept()
			logger.info(self.logger_id+'connection established')
			self.connected=True
			self.rfile = self.conn.makefile()
			while True:
				try:
					self.data = self.rfile.readline().strip()
					if not self.data:
						break;
					comm.debug('from:'+str(self.port)+' msg:'+self.data)
					self.incom=threading.Thread(target=self.parent.process, args=(self.caller,self.data.split(','),))
					self.incom.start()
				except ConnectionResetError:
					break
					
			self.connected=False
			logger.warning(self.logger_id+'connection lost')

	def send(self,msg):
		self.msg=msg+'\n'
		try:
			comm.debug('to:'+str(self.port)+' msg:'+msg)
			self.conn.sendall(self.msg.encode())
		except AttributeError:
			logger.debug(self.logger_id+'client not connected')
		except BrokenPipeError:
			logger.debug(self.logger_id+'client not connected')


	def shutdown(self):
		#if self.connected:
		#	self.s.shutdown(socket.SHUT_RDWR)
		self.s.close()

	def statusUpdate(self,caller): ###############create class for esp and re write
		pass

class port(object):
	def __init__(self,parent,info):
		self.parent=parent
		self.caller=2
		self.info=info
		#self.name=self.info['name']
		self.ip ='192.168.0.10'
		self.port=self.info['port']
		self.connected=False
		#self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#self.logger_id='client:'+ str(self.port)+' '
		logger.info(self.logger_id)
		#self.s.bind((self.ip,self.port))	
		#self.up()

		


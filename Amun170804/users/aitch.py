configs=dict(name='aitch', usrid=1,admin=True, port=1001,rooms=[0,1])

rules='''

logger.info(self.logId+'rules updated')

def rule(self,msg):
	self.input=msg.split(',')
	if(input[0]=='1' and input[0]=='1' and input[0]=='1'):
		pass

'''


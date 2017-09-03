import logging

class amunobj(object):
	def __init__(self,parent,info,preId,objid):
		self.parent=parent
		self.info=info
		self.preId=str(preId)
		self.preStr=self.info['preStr']
		self.name=self.info['name']
		self.objid=objid
		self.auto=0
		self.agent=self.parent.agents[self.info['agent']]
		self.index=str(self.info['agent_index'])
		self.agent.insert(self,self.index)
		self.clientAddr=self.preId+','+str(self.objid)
		self.objstring=',,'+self.preStr+','+str(self.objid)+','+self.name
		
	def status(self): #get status from agent by sending setup cmd
		self.agent.send(self.compose('agentS'))

	def inform(self,caller): #inform caller
		caller.inform(str(self.parent.id)+','+self.compose('client'))
		
	#inform all users of the current status
	def informAll(self):
		self.parent.informAll(self.compose('client'))

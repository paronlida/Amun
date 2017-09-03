#import
import importlib
import logging
import subprocess
import infra.config as config
gvar=importlib.import_module(config.gvar)
structure=importlib.import_module(config.structure)
agent=importlib.import_module(config.agent).agent
user=importlib.import_module(config.user)
server=importlib.import_module(config.wcom).server
room=importlib.import_module(config.room).room
logger = logging.getLogger('mainLogger')
#-------------------------------------------------------------------------------
b_ra=False
rooms=gvar.rooms
users=gvar.users
agents=gvar.agents

def ra():
	cmd="adb kill-server"
	p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=False)
	(output, err) = p.communicate()
	logger.debug(output.decode())
	cmd= "adb start-server"
	p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=False)
	(output, err) = p.communicate()
	logger.info(output.decode())
	#agents
	for gnt in structure.agents:
		agents.append(agent(gnt))
	#room construct
	for index in range(0,structure.rooms):
		_room=structure.roomlis(index)
		rooms.append(room(_room,index,agents))
	config.roomlist=rooms
	#users
	for usr in structure.users:
		users.append(user.user(usr))
	

		
def shutdown(self):
	for room in gvar.rooms:
		print('shutting')
		room.shutdown(False)
	cmd="adb kill-server"
	p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=False)
	(output, err) = p.communicate()
	logger.debug(output.decode())
	for agent in gvar.agents:
		agent.shutdown()
	for user in gvar.users:
		user.shutdown()
	exit()
#-------------------------------------------------------------------------------------
logger.info('Protocols:OK')

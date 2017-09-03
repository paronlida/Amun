
usr1=dict(usrFile='users.aitch')
other=dict(name='other', usrid=2,admin=False, port=1002,rooms=[0,1])
users=['users.aitch']


esp1=dict(agentId='0', port=151)
esp2=dict(agentId='1', port=160)
esp3=dict(agentId='2', port=170)
agents=[esp1,esp2,esp3]
#_______________________________________________________________________________________________

rooms=2 

def roomlis(index):
	if (index==0):
		#lights----------------
		light1= dict(typ='light',name='main light', cls=1,agent=0,agent_index='13')
		light2= dict(typ='light',name='RGB Strip', cls=1,agent=0,agent_index='12')
		light3= dict(typ='light',name='RGB Strip', cls=1,agent=0,agent_index='14')
		light4= dict(typ='light',name='RGB Strip', cls=1,agent=0,agent_index='16')
		#windows--------------
		window1= dict(typ='window',name='right window',agent=1,agent_index='13')
		window2= dict(typ='window',name='left window',agent=1,agent_index='14')
		#ir
		_tv= dict(typ='ir',sub='tv', name="TV", agent=0, case="1",agent_index='12',dct=1)
		#adb
		_adb= dict(typ='adb',device='montoya',ip='192.168.0.16',port=5555,dct=1,name='Fire Stick')
		#powerS
		ps1= dict(typ='powersupply',name='powersupply1',agent=0,agent_index='4')
		#regs
		_brightness= dict(typ='brightness',agent=1,c_index=1)
		_agents=[0]
		_objects = [window1,window2,light1,light2,light3,light4,_tv,_adb,ps1]
		_sensors=[_brightness]
		room= dict(name='myroom')
		
	elif (index==1):
		
		light1= dict(typ='light',name='mainlight',cls=1,agent=0,agent_index=1)
		window1= dict(typ='window',name='main window',agent=0,agent_index='14')
		window2= dict(typ='window',name='side window',agent=0,agent_index='14')
		_brightness= dict(typ='brightness',agent=0,c_index=1)
		_agents=[0]
		_objects = [window1,window2,light1]
		_sensors=[_brightness]
		room=dict(name='kitchen',owner=1)
	
	else:
		_objects = []
		_sensors=[]
		room=dict(name='generic',owner=1)
	
	_room=dict(info=room,objects=_objects,sensors=_sensors)
	return _room	
#_____________________________________________________________________________________________________________



#_____________________________________________________________________________________________________________





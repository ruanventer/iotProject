
import time
import sys
import json
import pprint
import uuid
from uuid import getnode as get_mac


try:
	import ibmiotf.application
	import ibmiotf.device
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device


def myAppEventCallback(event):
	print("Received live data from %s (%s) sent at %s: %s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), json.dumps(event.data)))
		

#####################################
#FILL IN THESE DETAILS
#####################################     
organization = "4scvcb"
deviceType = "Pi2"
deviceId = "b827eb827356"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "4*Y6fkx_yMvobT)(iQ"

##API TOKEN AND KEY
authkey = "a-4scvcb-yt6xwr4nxa"
authtoken = "C1m6j2FJV+L*OGGyDo"
# Initialize the application client.

def myAppEventCallback(event):
	str = "%s event '%s' received from device [%s]: %s"
	print(str % (event.format, event.event, event.device, json.dumps(event.data)))
	
	
try:
	#appOptions = {"org": organization, "id": deviceId,"auth-method": authMethod, "auth-key" : authkey, "auth-token":authtoken }
	appOptions = {"org": organization, "type": deviceType, "id": deviceId,"auth-key" : authkey, "auth-method": "apikey", "auth-token": authtoken}
  
	options = {
		"org": organization,
		"type": deviceType,
		"id": deviceId,
		"auth-method": "apikey",
		"auth-token": authtoken,
		"auth-key" : authkey
	}
except Exception as e:
	print(str(e))
	sys.exit()



  
# Connect and configuration the application
# - subscribe to live data from the device we created, specifically to "greeting" events
# - use the myAppEventCallback method to process events
appCli = ibmiotf.application.Client(options)
appCli.connect()
appCli.deviceEventCallback = myAppEventCallback
appCli.subscribeToDeviceEvents(deviceType, deviceId)

	
while(True):
	

	##appCli.subscribeToDeviceEvents(deviceType="Pi2", deviceId="b827eb827356", event="intruderstatus")
	
	command = input("Enter the command: ")

	if command == 'lighton1':
		print ("Turning Light 1 ON")
		command = 'null'
		try:
			appCli = ibmiotf.application.Client(options)
			#device = appCli.api.getDevice(deviceType, deviceId)
			#print(device)
			appCli.connect()
			print ("here")
			
			commandData = { 'LightON1' : 1 }
			
			appCli.publishCommand(deviceType, deviceId, "on1","json", commandData)
			appCli.publishEvent(deviceType, deviceId,"status","json", commandData)
			x=0
  
			##while(x<1):
			##	appCli.deviceEventCallback = myAppEventCallback
			##	appCli.subscribeToDeviceEvents(event="lightstatus")
			##	x=x+1
	
		except Exception as e:
			print ("Connect attempt failed: "+str(e))
			sys.exit()


	elif command == 'lightoff1':
		print ("Turning Light 1 OFF")
		try:
			appCli = ibmiotf.application.Client(appOptions)
			appCli.connect()
			commandData={'LightOFF1' : 0}
		
			appCli.publishCommand(deviceType, deviceId, "off1","json", commandData)
			appCli.publishEvent(deviceType, deviceId,"status","json", commandData)
			y=0
			while(y<1):
				appCli.deviceEventCallback = myAppEventCallback
				appCli.subscribeToDeviceEvents(event="lightstatus")
				y=y+1
		
			
		except Exception as e:
			print ("Connect attempt failed: "+str(e))
			sys.exit()

	elif command == 'lighton2':
		print ("Turning Light 2 ON")
		command = 'null'
		try:
			appCli = ibmiotf.application.Client(options)
			#device = appCli.api.getDevice(deviceType, deviceId)
			#print(device)
			appCli.connect()
			print ("here")
			
			commandData = { 'LightON2' : 1 }
			
			appCli.publishCommand(deviceType, deviceId, "on2","json", commandData)
			#print ("here2")
			appCli.publishEvent(deviceType, deviceId,"status","json", commandData)
			#print ("here3")
			x=0
			while(x<1):
				appCli.deviceEventCallback = myAppEventCallback
				appCli.subscribeToDeviceEvents(event="status")
				x=x+1

		except Exception as e:
			print ("Connect attempt failed: "+str(e))
			sys.exit()

	elif command == 'lightoff2':
		print ("Turning Light 2 OFF")
		try:
			appCli = ibmiotf.application.Client(appOptions)
			appCli.connect()
			commandData={'LightOFF2' : 0}
		
			appCli.publishCommand(deviceType, deviceId, "off2","json", commandData)
			appCli.publishEvent(deviceType, deviceId,"status","json", commandData)
			y=0
			while(y<1):
				appCli.deviceEventCallback = myAppEventCallback
				appCli.subscribeToDeviceEvents(event="status")
				y=y+1
		
			
		except Exception as e:
			print ("Connect attempt failed: "+str(e))
			sys.exit()

	else:
		print ("Not a valid command")
appCli.disconnect()


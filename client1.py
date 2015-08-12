
import time
import sys
import pprint
import uuid
from uuid import getnode as get_mac

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_UP)
ls='OFF'

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
	print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

def myCommandCallback(cmd):
  print(cmd)
#  print("Command received: %s" % cmd.payload)
  if cmd.command == "on1":
	print("Turning Light 1 ON")
	GPIO.output(3,1)
	deviceCli.connect()
	dataL = { 'LightStatus 1': ls1, 'LightStatus 2': ls2 }
	deviceCli.publishEvent("lightstatus", "json", dataL)

  elif cmd.command == "off1":  
    print("Turning Light 1 OFF")
    GPIO.output(3,0)

  elif cmd.command == "on2":  
    print("Turning Light 2 ON")
    GPIO.output(13,1)

  elif cmd.command == "off2":  
    print("Turning Light 2 OFF")
    GPIO.output(13,0)	

  print("End of Event")       
#####################################
#FILL IN THESE DETAILS
#####################################     
organization = "4scvcb"
deviceType = "Pi2"
deviceId = "b827eb827356"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "4*Y6fkx_yMvobT)(iQ"

# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print(str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
deviceCli.commandCallback = myCommandCallback
#x=0
GPIO.output(13,0)
GPIO.output(3,0)
while(1):
	lightStatus1=GPIO.input(7)
	if lightStatus1==0:
		ls1='ON'
	else:
		ls1='OFF'
	lightStatus2=GPIO.input(15)
	if lightStatus2==0:
		ls2='ON'
	else:
		ls2='OFF'
	intruder=GPIO.input(11)
	dataL = { 'LightStatus 1': ls1, 'LightStatus 2': ls2 }
	#deviceCli.publishEvent("lightstatus", "json", dataL)
	print(dataL)
	
	if intruder==1:
		dataI = { 'Intruder': intruder}
		deviceCli.publishEvent("instruderstatus", "json", dataI)
		print(dataI)
	
	time.sleep(2)
		

# Disconnect the device and application from the cloud
deviceCli.disconnect()
#appCli.disconnect()


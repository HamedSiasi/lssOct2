
from C027 import *
from C030 import *
from Odin import *

#--------------------------------------------------------------------------
#                          LSS Configuration
#--------------------------------------------------------------------------
DeviceReportingIntervals = 120 
DeviceSafeMovement = 500
debuging = False
gDevice  = None
gDeviceID = ['8','9']
gDeviceType = ['c030','odin']
#dict = {}
dict = {'8': 0, '9': 0} #demo


#--------------------------------------------------------------------------
#                    Lifetime Security Service
#--------------------------------------------------------------------------
def isNewReport(deviceID):
	if (dict[deviceID] != gDevice.RawDataId[0]):
		dict[deviceID] = gDevice.RawDataId[0]
		return True
	return False


def elapsedTime():
	global gDevice
	now = datetime.datetime.fromtimestamp(time.time())
	last = datetime.datetime.fromtimestamp(gDevice.PosixTime[0][0])
	#print ("current time:   %s" %now)
	#print ("last report:    %s" %last)
	elapsed = time.time() - gDevice.PosixTime[0][0]
	return "%.2f" %(abs(elapsed))




def postDB(rawDataId , riskScore):
	#print (rawDataId)
	#print (riskScore)
	try:
		response  = requests.post("http://151.9.34.99/webservice/svmhandler.php", data={'RawDataId': rawDataId, 'RiskScore': riskScore})
		if (response.text == "RC 000"):
			pass
		else:
			print (response.text)
			print "postDB ERROR"
	except Exception, ee:
		print(str(ee))



def postStatus(deviceID , status):
	#print (deviceID)
	#print (status)
	try:
		response  = requests.post("http://151.9.34.99/webservice/svmhandler.php?Action=status", data={'DeviceId': deviceID, 'DeviceStatus': status})
		if (response.text == "RC 000"):
			pass
		else:
			print (response.text)
			print "postStatus ERROR"
	except Exception, ee:
		print(str(ee))















def securityAgent():
	global gDeviceID, gDeviceType, gDevice
	for i in range(len(gDeviceID)):
		try:
			print "\nID:%s Type:%s" %(gDeviceID[i],gDeviceType[i])
			if(gDeviceType[i] == "c027"):  gDevice = C027Class(gDeviceID[i])
			elif(gDeviceType[i] == "c030"):gDevice = C030Class(gDeviceID[i])
			elif(gDeviceType[i] == "odin"):gDevice = OdinClass(gDeviceID[i])
			else:
				print "ERROR! unknown deviceType!\n\n"
				break
			#---------------------------------------------------------------------------------------------------------
			#                    Checking Device Object Status
			#---------------------------------------------------------------------------------------------------------
			if(gDevice == None):
				print "ERROR! gDevice"
				break
			if(gDevice.pDataBase == 0):
				print "ERROR! pDataBase"
				break
			#Device.deviceDebug(debuging)
			elapsed = elapsedTime()
			#if(elapsed >= DeviceReportingIntervals):
			if(elapsed <= DeviceReportingIntervals): ##just for test
			##--------------------------------------------------------------------------------------------------------
			##                            DEVICE_OFFLINE
			##--------------------------------------------------------------------------------------------------------

				print " R:(%s) ID:(%s %s) T:(%s) (OFFLINE)"  %(gDevice.pDataBase, gDeviceID[i], gDeviceType[i], elapsed)
				postStatus(gDeviceID[i], 0) # DB OFFline
				postDB(gDevice.pDataBase, 4.99) # DB DeviceTotalRisk
			else:
			##---------------------------------------------------------------------------------------------------------
			##                            DEVICE_ONLINE
			##---------------------------------------------------------------------------------------------------------
				postStatus(gDeviceID[i], 1) # DB ONline
				if(isNewReport(gDeviceID[i])):
					gDevice.RiskAnalysis()
					gDevice.TotalRiskAnalysis()
					postDB(gDevice.pDataBase, gDevice.total_Risk)
				else:
					print " R:(%s) ID:(%s %s) T:(%s) (ONLINE)"  %(gDevice.pDataBase, gDeviceID[i], gDeviceType[i], elapsed)

		except Exception, syserr:
			print(str(syserr))
			postDB(gDevice.pDataBase, 4.90)
		finally:
			if(gDevice):
				gDevice.reset()
			time.sleep(0.1)
		#try
	#for
#agent




def deviceListAgent():
	global gDeviceID, gDeviceType
	del gDeviceID[:]
	del gDeviceType[:]
	url = "http://151.9.34.99/webservice/assetviewer.php?Action=deviceList"
	#print(url)
	response  = requests.get(url)
	if (response.status_code == 200):
		obj = json.loads(response.content)
		for raw in obj["Devices"]:
			gDeviceID.append(str(raw["DeviceId"]))
			gDeviceType.append(str(raw["DeviceType"]))
			dict [str(raw["DeviceId"])] = 0
		if(len(gDeviceID) != len(gDeviceType)): print "ERROR! deviceList API"
		if(len(gDeviceID) == 0):                print "ERROR! deviceList API gDeviceID"
		if(len(gDeviceType) == 0):              print "ERROR! deviceList API gDeviceType"
		#print(gDeviceID)
		#print(gDeviceType)
	else:
		print(response.status_code)
		print("deviceList API Failed :((\n\n")
	#if-else
#deviceListAgent





def main():
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	while True:
		try:
			#deviceListAgent() #productionCode
			securityAgent()
		except Exception as e:
			print str(e)
		finally:
			time.sleep(0.1)



if __name__ == "__main__":
    main()

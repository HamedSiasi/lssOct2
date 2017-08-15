#print(__doc__)
#!/usr/bin/python
from sklearn.svm import SVR
import numpy as np
import requests
import time
import json
import os
import warnings
import datetime
import pylab as pl
import sys
from tabulate import tabulate
import gpxpy.geo
import pdb
from sklearn.preprocessing import StandardScaler


#myAssets = ["IMEI","IMSI","Latitude","Longitude","RX","TX","Wakeup","Watchdog","Battery"]
RawDataId            = []
IMEI                 = []
IMSI                 = []
Latitude             = []
Longitude            = []
RX                   = []
TX                   = []
Wakeup               = []
Watchdog             = []
Battery              = []
POSIXTIME            = []
relativeTime         = []
TX_ready             = []
TIME_ready_TX        = []
RX_ready             = []
TIME_ready_RX        = []




def reset():
	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,POSIXTIME,relativeTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX 
	del RawDataId[:]
	del IMEI[:]
	del IMSI[:]
	del Latitude[:]
	del Longitude[:]
	del RX[:]
	del TX[:]
	del Wakeup[:]
	del Watchdog[:]
	del Battery[:]
	del POSIXTIME[:]
	del relativeTime[:]
	del TX_ready[:]
	del TIME_ready_TX[:]
	del RX_ready[:]
	del TIME_ready_RX[:]


dict = {'1': 0, '2': 0, '3': 0}

def isNew(deviceID):
	global RawDataId
	retval = False
	if (dict[deviceID] != RawDataId[0]):
		dict[deviceID] = RawDataId[0]
		return True
	return retval



def getDB(deviceID):
	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,POSIXTIME,relativeTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX    
	url = "http://151.9.34.99/webservice/assetviewer.php?DeviceId=" + deviceID + "&Action=assets"
	response  = requests.get(url)
	if (response.status_code == 200):
		json_obj = json.loads(response.content)
		for raw in json_obj:
			RawDataId.append(  int(raw["RawDataId"]))   
			IMEI.append(       int(raw["IMEI"]))
			IMSI.append(       int(raw["IMSI"]))
			Latitude.append(   float(raw["Latitude"]))  #North South [-90,90]
			Longitude.append(  float(raw["Longitude"])) #West East [-180,180]
			RX.append(         int(raw["RX"]))
			TX.append(         int(raw["TX"]))
			Wakeup.append(     int(raw["Wakeup"]))
			Watchdog.append(   int(raw["Watchdog"]))
			Battery.append(    float(raw["Battery"]))
			POSIXTIME.append( [long(raw["RawDataDateCreated"])] )
	else:
		print "ERROR"

	for i in range(len(POSIXTIME)):
		relativeTime.append(((POSIXTIME[i][0])-(POSIXTIME[len(POSIXTIME)-1][0])))

	for i in range(len(TX)-1):
		if(TX[i+1] <= TX[i]):
			TX_ready.append(TX[i])
			TIME_ready_TX.append(relativeTime[i])
		else:
			break

	for j in range(len(RX)-1):
		if(RX[j+1] <= RX[j]):
			RX_ready.append(RX[j])
			TIME_ready_RX.append(relativeTime[j])
		else:
			break

	#RX_ready = StandardScaler().fit_transform(RX_ready)
	#TX_ready = StandardScaler().fit_transform(TX_ready)
	#TIME_ready_RX = StandardScaler().fit_transform(TIME_ready_RX)
	#TIME_ready_TX = StandardScaler().fit_transform(TIME_ready_TX)
	return RawDataId[0]




def elapsedTime():
	now = datetime.datetime.fromtimestamp(time.time())
	last = datetime.datetime.fromtimestamp(POSIXTIME[0][0])
	#print ("current time:   %s" %now)
	#print ("last report:    %s" %last)
	elapsed = time.time() - POSIXTIME[0][0]
	return "%.2f" %elapsed




def postDB(rawDataId , riskScore):
	try:
		response  = requests.post("http://151.9.34.99/webservice/svmhandler.php", data={'RawDataId': rawDataId, 'RiskScore': riskScore})
		if (response.text == "RC 000"):
			return "OK"
		else:
			return "ERROR"
	except Exception, ee:
		print(str(ee))
		return "ERROR"





def postStatus(deviceID , status):
	try:
		response  = requests.post("http://151.9.34.99/webservice/svmhandler.php?Action=status", data={'DeviceId': deviceID, 'DeviceStatus': status})
		if (response.text == "RC 000"):
			return "OK"
		else:
			return "ERROR"
	except Exception, ee:
		print(str(ee))
		return "ERROR"





def compareAssets():
	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,POSIXTIME,relativeTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX 
	risk = 0.0
	IMEI_STATUS     = "OK"
	IMSI_STATUS     = "OK"
	movement_status = "OK"
	RX_STATUS       = "OK"
	TX_STATUS       = "OK"
	Wakeup_STATUS   = "OK"
	Watchdog_STATUS = "OK"
	Battery_STATUS  = "OK"

	IMEI_COMPARE     = IMEI[0]-IMEI[1] 
	IMSI_COMPARE     = IMSI[0]-IMSI[1] 
	RX_COMPARE       = RX[0]-RX[1] 
	TX_COMPARE       = TX[0]-TX[1] 
	Wakeup_COMPARE   = Wakeup[0]-Wakeup[1] 
	Watchdog_COMPARE = Watchdog[0]-Watchdog[1] 
	Battery_COMPARE  = Battery[0]-Battery[1] 
	movement = gpxpy.geo.haversine_distance(Latitude[1], Longitude[1], Latitude[0], Longitude[0])

	if(IMEI_COMPARE):
		IMEI_STATUS = "POTENTIAL RISK"
		if (risk<=4.5):risk = 4.511
	if(IMSI_COMPARE):
		IMSI_STATUS = "POTENTIAL RISK"
		if (risk<=4.1):risk = 4.122
	if(movement>500):
		movement_status = "POTENTIAL RISK"
		if (risk<=4.3):risk = 4.331
	if(RX_COMPARE <= 0):
		RX_STATUS = "POTENTIAL RISK"
		if (risk<=4.2):risk = 4.242
	if(TX_COMPARE <= 0):
		TX_STATUS = "POTENTIAL RISK"
		if (risk<=4.2):risk = 4.253
	if(Wakeup_COMPARE != 1):
		Wakeup_STATUS = "POTENTIAL RISK"
		if (risk<=4.6):risk = 4.664
	if(Watchdog_COMPARE):
		Watchdog_STATUS = "POTENTIAL RISK"
		if (risk<=3.8):risk = 3.881
	if(Battery_COMPARE>=1):
		Battery_STATUS = "POTENTIAL RISK"
		if (risk<=3.1):risk = 4.192

	print("\n")
	print(  tabulate([['IMEI', IMEI[0], IMEI[1], IMEI_COMPARE, IMEI_STATUS], 
					['IMSI', IMSI[0], IMSI[1], IMSI_COMPARE, IMSI_STATUS], 
					['Latitude', Latitude[0], Latitude[1], movement, movement_status], 
					['Longitude', Longitude[0], Longitude[1], movement, movement_status], 
					['RX', RX[0], RX[1], RX_COMPARE, RX_STATUS], 
					['TX', TX[0], TX[1], TX_COMPARE, TX_STATUS], 
					['Wakeup', Wakeup[0], Wakeup[1], Wakeup_COMPARE, Wakeup_STATUS], 
					['Watchdog', Watchdog[0], Watchdog[1], Watchdog_COMPARE, Watchdog_STATUS], 
					['Battery', Battery[0], Battery[1], Battery_COMPARE,  Battery_STATUS]], 
					headers=['ASSET', 'ACTUAL READING', 'PREVIOUS READING', 'DELTA', 'STATUS'], tablefmt="rst") )
	return risk






def runMachineLearning():
	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,POSIXTIME,relativeTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX 
	try:
		print("MachineLearning")

		RX_prediction        = []
		TX_prediction        = []
		Battery_prediction   = []

		Time_historyRX = (np.delete(np.array(TIME_ready_RX), [0])).reshape(len(np.array(TIME_ready_RX))-1, 1)
		Time_historyTX = (np.delete(np.array(TIME_ready_TX), [0])).reshape(len(np.array(TIME_ready_TX))-1, 1)

		RXmodel = SVR(kernel='linear', C=0.01, epsilon=0.1)
		RXX = np.delete(RX_ready,[0])
		RXmodel.fit( Time_historyRX , RXX )
		RX_prediction.append(RXmodel.predict(TIME_ready_RX[0]))
		print("RX behavioral model OK!")

		TXmodel =  SVR(kernel='linear', C=0.01, epsilon=0.1)
		TXX = np.delete(TX_ready,[0])
		#print(TXX)
		#print(Time_historyTX)
		TXmodel.fit( Time_historyTX , TXX )
		TX_prediction.append(TXmodel.predict(TIME_ready_TX[0]))
		print("TX behavioral model OK!")

		RX_Delta      = (abs((RX[0]-RX_prediction[0][0])/(RX_ready[0])))*100
		TX_Delta      = (abs((TX[0]-TX_prediction[0][0])/(TX_ready[0])))*100
		RX_risk = RX_Delta/27
		TX_risk = TX_Delta/27
		print(  tabulate([['RX', RX_ready[0], RX_prediction[0], RX_Delta, RX_risk], 
						['TX', TX_ready[0], TX_prediction[0], TX_Delta, TX_risk]], 
						headers=['ASSET', 'ACTUAL READING', 'PREDICTION', 'DELTA PERCENTAGE', 'RISK'], tablefmt="rst") )
		return "%.3f" %(RX_risk + TX_risk)

	except Exception, e:
		print(str(e))
		return "3.19"



def lssAgent():
	risk = 0.0
	rd = ["2"]
	while True:
		for i in range(len(rd)):
			try:
				reset()
				riskDB = getDB(rd[i])
				if (riskDB == "ERROR"):
					print("getDB ERROR !!!")

				elapsed = elapsedTime()
				if (elapsed is None):
					print("elapsed time ERROR !!!")

				if(float(elapsed)>=120):
					#************************************************** DEVICE_OFFLINE *******************************************************
					print "\nRawID:(%s) ID:(%s) ElasedTime:(%s) Status:(OFFLINE)"  %(riskDB,rd[i],elapsed)
					if(postStatus(rd[i],"0") == "ERROR"):
						print("postStatus ERROR(1) !!!")
					if (postDB(riskDB, 3.99) == "ERROR"): 
						print("postDB ERROR(1) !!!")

				else:
					#**************************************************** DEVICE_ONLINE ******************************************************
					if(postStatus(rd[i],"1") == "ERROR"):
						print("postStatus ERROR(2) !!!")
					if(isNew(rd[i])):
						risk = compareAssets()#range[4, 4.8]
						if(risk == 0.0): 
							risk = runMachineLearning()#range[0, 2.5]
							if (float(risk) > 5): 
								risk = 5 
						if(postDB(riskDB, risk) == "ERROR"): 
							print("postDB ERROR(2) !!!")
						print "\nRawID:(%s) ID:(%s) ElasedTime:(%s) Status:(ONLINE) RisckScore(%s)\n\n"  %(riskDB,rd[i],elapsed,risk)
					else:
						print "RawID:(%s) ID:(%s) Status:(ONLINE)"  %(riskDB,rd[i])
						#sys.stdout.write('.')
			except Exception, e:
				print(str(e))
				if(postDB(riskDB, 4.90) == "ERROR"):
					print("postDB ERROR(3) !!!")

			time.sleep(20)
		#for
	#while
#def



def main():
	warnings.filterwarnings("ignore", category=DeprecationWarning) 
	try:
		lssAgent()
	except Exception, e:
		print(str(e))


if __name__ == "__main__":
    main()

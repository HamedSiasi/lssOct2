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
import random
from random import randint
from termcolor import colored
from sklearn import preprocessing


#global names
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
PTime                = []
TIME                 = []
RPTime               = []
TX_ready             = []
TIME_ready_TX        = []
RX_ready             = []
TIME_ready_RX        = []
IMEI_prediction      = []
IMSI_prediction      = []
Latitude_prediction  = []
Longitude_prediction = []
RX_prediction        = []
TX_prediction        = []
Wakeup_prediction    = []
Watchdog_prediction  = []
Battery_prediction   = []




def reset():
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
	del PTime[:]
	del TIME[:]
	del RPTime[:]
	del TX_ready[:]
	del TIME_ready_TX[:]
	del RX_ready[:]
	del TIME_ready_RX[:]
	del IMEI_prediction[:]
	del IMSI_prediction[:]
	del Latitude_prediction[:]
	del Longitude_prediction[:]
	del RX_prediction[:]
	del TX_prediction[:]
	del Wakeup_prediction[:]
	del Watchdog_prediction[:]
	del Battery_prediction[:]




dict = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}





def isNew(deviceID):
	global RawDataId
	retval = False
	if (dict[deviceID] != RawDataId[0]):
		dict[deviceID] = RawDataId[0]
		return True
	return retval







def getDB(deviceID):
	retval = 0.0

	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,PTime,RPTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX,StandardTX,StandardRX,StandardBattery,StandardTime    
	url = "http://151.9.34.99/webservice/assetviewer.php?DeviceId=" + deviceID + "&Action=assets"
	#print(url)
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
			PTime.append( [long(raw["RawDataDateCreated"])] )

		for i in range(len(PTime)):
			RPTime.append(((PTime[i][0])-(PTime[len(PTime)-1][0])))

		#print(len(RX))
		#print(len(TX))
		#print(len(Battery))
		#print(len(RPTime))

		StandardRX = preprocessing.scale(RX)
		StandardTX = preprocessing.scale(TX)
		StandardBattery = preprocessing.scale(Battery)
		StandardTime = preprocessing.scale(RPTime)

		#print(StandardBattery)
		#print(len(StandardRX))
		#print(len(StandardTX))
		#print(len(StandardBattery))
		#print(len(StandardTime))

		for i in range(len(StandardTX)-1):
			if(StandardTX[i+1] <= StandardTX[i]):
				TX_ready.append(StandardTX[i])
				TIME_ready_TX.append(StandardTime[i])
			else:
				break

		for j in range(len(StandardRX)-1):
			if(StandardRX[j+1] <= StandardRX[j]):
				RX_ready.append(StandardRX[j])
				TIME_ready_RX.append(StandardTime[j])
			else:
				break

		#print(len(TX_ready))
		#print(len(TIME_ready_TX))
		#print(len(RX_ready))
		#print(len(TIME_ready_RX))

		retval = RawDataId[0]

	else:
		print(response.status_code)
		print "ERROR"

	return retval







def elapsedTime():
	now = datetime.datetime.fromtimestamp(time.time())
	last = datetime.datetime.fromtimestamp(PTime[0][0])
	#print ("current time:   %s" %now)
	#print ("last report:    %s" %last)
	elapsed = time.time() - PTime[0][0]
	return "%.2f" %(abs(elapsed))







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







def runMachineLearning():
	print("ML")
	#print(len(StandardRX))
	#print(len(StandardTX))
	#print(len(StandardBattery))
	#print(len(StandardTime))

	RX_risk = 0
	TX_risk = 0
	Battery_risk = 0

	Time_historyRX = (np.delete(np.array(TIME_ready_RX), [0])).reshape(len(np.array(TIME_ready_RX))-1, 1) 
	#print(Time_historyRX)
	RX_prediction.append(SVR(kernel='linear',C=0.00001,gamma='auto',epsilon=0.00001,tol=0.0001).fit(Time_historyRX,np.delete(RX_ready,[0])).predict(TIME_ready_RX[0]))
	#print(RX_prediction)


	Time_historyTX = (np.delete(np.array(TIME_ready_TX), [0])).reshape(len(np.array(TIME_ready_TX))-1, 1) 
	#print(Time_historyTX)
	TX_prediction.append(SVR(kernel='linear',C=0.00001,gamma='auto',epsilon=0.00001,tol=0.0001).fit(Time_historyTX,np.delete(TX_ready,[0])).predict(TIME_ready_TX[0]))
	#print(TX_prediction)


	Time_historyB = (np.delete(np.array(StandardTime), [0])).reshape(len(np.array(StandardTime))-1, 1)
	#print(Time_historyB)
	Battery_prediction.append(SVR(kernel='linear',C=0.00001,gamma='auto',epsilon=0.00001,tol=0.0001).fit(Time_historyB,np.delete(StandardBattery,[0])).predict(StandardTime[0]))
	#print(Battery_prediction)


	RX_Delta = (abs((StandardRX[0]-RX_prediction[0][0])/(RX[0])))*100
	TX_Delta = (abs((StandardTX[0]-TX_prediction[0][0])/(TX[0])))*100
	Battery_Delta = (abs((StandardBattery[0]-Battery_prediction[0][0])/(Battery[0])))*100

	RX_risk = RX_Delta/20
	TX_risk = TX_Delta/20
	Battery_risk = Battery_Delta/20

	print tabulate([['RX', StandardRX[0], RX_prediction[0], RX_Delta, RX_risk], 
					['TX', StandardTX[0], TX_prediction[0], TX_Delta, TX_risk],  
					['Battery', StandardBattery[0], Battery_prediction[0],  Battery_Delta, Battery_risk]], 
					headers=['ASSET', 'ACTUAL READING', 'PREDICTION', 'DELTA PERCENTAGE', 'RISK'], tablefmt="rst")

	return "%.3f" %(RX_risk + TX_risk + Battery_risk)











def compareAssets():
	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,PTime,RPTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX 
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
		if (risk<=4.511):risk = 4.511
	if(IMSI_COMPARE):
		IMSI_STATUS = "POTENTIAL RISK"
		if (risk<=4.122):risk = 4.122
	if(movement>500):
		movement_status = "POTENTIAL RISK"
		if (risk<=4.331):risk = 4.331
	if(RX_COMPARE <= 0):
		RX_STATUS = "POTENTIAL RISK"
		if (risk<=4.242):risk = 4.242
	if(abs(TX_COMPARE) > 900):
		TX_STATUS = "POTENTIAL RISK"
		if (risk<=4.253):risk = 4.253
	if(Wakeup_COMPARE != 1):
		Wakeup_STATUS = "POTENTIAL RISK"
		if (risk<=4.664):risk = 4.664
	if(Watchdog_COMPARE):
		Watchdog_STATUS = "POTENTIAL RISK"
		if (risk<=3.881):risk = 3.881
	if(abs(Battery_COMPARE)>=1):
		Battery_STATUS = "POTENTIAL RISK"
		if (risk<=4.192):risk = 4.192
	if(RX[0] > 2*RX[1]):
		if (risk<=4.112):risk = 4.112
	if(TX[0] > 2*TX[1]):
		if (risk<=4.221):risk = 4.221

	print("\n")
	Plat = Latitude[0]
	Plog = Longitude[0]
	PRX = RX[1]+46+randint(0, 9) 
	PTX = TX[1]+103+randint(0, 9)
	PBattery = Battery[1]-random.uniform(0.0, 0.1)

	print(  tabulate([['IMEI',    IMEI[0],      IMEI[1],       IMEI_COMPARE,      " ",           " ",                         IMEI_STATUS], 
					['IMSI',      IMSI[0],      IMSI[1],       IMSI_COMPARE,      " ",           " ",                         IMSI_STATUS], 
					['Latitude',  Latitude[0],  Latitude[1],   movement,          Plat,          abs(Plat-Latitude[0]) ,      movement_status], 
					['Longitude', Longitude[0], Longitude[1],  movement,          Plog,          abs(Plog-Longitude[0]),      movement_status], 
					['RX',        RX[0],        RX[1],         RX_COMPARE,        PRX ,          abs(PRX-RX[0]),              RX_STATUS], 
					['TX',        TX[0],        TX[1],         TX_COMPARE,        PTX ,          abs(PTX-TX[0]),              TX_STATUS], 
					['Wakeup',    Wakeup[0],    Wakeup[1],     Wakeup_COMPARE,    Wakeup[0]+1 ,  abs(Wakeup[0]+1-Wakeup[0]),  Wakeup_STATUS], 
					['Watchdog',  Watchdog[0],  Watchdog[1],   Watchdog_COMPARE,  " ",           " ",                         Watchdog_STATUS], 
					['Battery',   Battery[0],   Battery[1],    Battery_COMPARE,   abs(PBattery), abs(PBattery-Battery[0]),               Battery_STATUS]], 
					headers=['ASSET', 'ACTUAL READING', 'PREVIOUS READING', 'READING DELTA', 'PREDICTION', 'PREDICTION DELTA', 'STATUS'], tablefmt="rst") )

	#return "%.3f" %(risk+random.uniform(0.100, 0.199))
	return risk








def lssAgent():
	rd = ["7"]

	while True:
		for i in range(len(rd)):
			try:
				risk = 0.0
				riskDB = 0
				reset()
				riskDB = getDB(rd[i])
				if (riskDB == 0):
					print("getDB ERROR !!!")

				elapsed = elapsedTime()
				if (elapsed is None):
					print("elapsed time ERROR !!!")

				if(float(elapsed)>=120):
					###########################################################
					#                   DEVICE_OFFLINE
					###########################################################

					print "\nRawID:(%s) ID:(%s) ElasedTime:(%s) Status:(OFFLINE)"  %(riskDB,rd[i],elapsed)
					if(postStatus(rd[i],"0") == "ERROR"):
						print("postStatus ERROR(1) !!!")
					if (postDB(riskDB, 4.99) == "ERROR"): 
						print("postDB ERROR(1) !!!")

				else:
					###########################################################
					#                   DEVICE_ONLINE 
					###########################################################

					if(postStatus(rd[i],"1") == "ERROR"):
						print("postStatus ERROR(2) !!!")

					if(isNew(rd[i])):
						#risk = compareAssets()
						print("Assets risck: %s" %str(risk))
						if(risk == 0.0): 
							#risk = "%.3f" %(random.uniform(0.1, 1.1))
							risk = runMachineLearning()
							print("ML risk: %s" %str(risk))

						if(postDB(riskDB, risk) == "ERROR"): 
							print("postDB ERROR(2) !!!")

						print "\nRawID:(%s) ID:(%s) ElasedTime:(%s) Status:(ONLINE) RisckScore(%s)\n\n"  %(riskDB,rd[i],elapsed,risk)
					else:
						print "RawID:(%s) ID:(%s) ElasedTime:(%s) Status:(ONLINE)"  %(riskDB,rd[i],elapsed)
						
			except Exception, e:
				print(str(e))
				if(postDB(riskDB, 4.90) == "ERROR"):
					print("postDB ERROR(3) !!!")

			time.sleep(3)
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
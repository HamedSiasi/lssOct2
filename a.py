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
PTime            = []
RPTime         = []
TX_ready             = []
TIME_ready_TX        = []
RX_ready             = []
TIME_ready_RX        = []
StandardRX                   = []
StandardTX                   = []
StandardBattery              = []
StandardTime         = []
RX_prediction=[]
TX_prediction=[]
Battery_prediction=[]



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
	del PTime[:]
	del RPTime[:]
	del TX_ready[:]
	del TIME_ready_TX[:]
	del RX_ready[:]
	del TIME_ready_RX[:]
	del StandardRX[:]
	del StandardTX[:]
	del StandardBattery[:]
	del StandardTime[:]
	del RX_prediction[:]
	del TX_prediction[:]
	del Battery_prediction[:]



def getDB(deviceID):
	global RawDataId,IMEI,IMSI,Latitude,Longitude,RX,TX,Wakeup,Watchdog,Battery,POSIXTIME,relativeTime,TX_ready,TIME_ready_TX,RX_ready,TIME_ready_RX,StandardTX,StandardRX,StandardBattery,StandardTime    
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
	else:
		print "ERROR"

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

	print(StandardBattery)
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

	return RawDataId[0]






def runMachineLearning():
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






def main():
	warnings.filterwarnings("ignore", category=DeprecationWarning) 
	try:
		reset()
		getDB("5")
		print(runMachineLearning())
	except Exception, e:
		print(str(e))


if __name__ == "__main__":
    main()
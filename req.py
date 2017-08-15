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
TIME                 = []
relativeTime         = []
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
	del POSIXTIME[:]
	del TIME[:]
	del relativeTime[:]
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


dict = {'1': 0, '2': 0, '3': 0}

def isNew(deviceID):
	retval = False
	if (dict[deviceID] != RawDataId[0]):
		dict[deviceID] = RawDataId[0]
		return True
	return retval



def getDB(deviceID):
	url = "http://151.9.34.99/webservice/assetviewer.php?DeviceId=" + deviceID + "&Action=assets"
	#print (url)
	response  = requests.get(url)
	if (response.status_code == 200):
		json_obj = json.loads(response.content)
		#json_size = len(json_obj)
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
	#print (deviceID)
	#print (status)
	try:
		response  = requests.post("http://151.9.34.99/webservice/svmhandler.php?Action=status", data={'DeviceId': deviceID, 'DeviceStatus': status})
		#print (response.text)
		if (response.text == "RC 000"):
			return "OK"
		else:
			return "ERROR"
	except Exception, ee:
		print(str(ee))
		return "ERROR"





def compareAssets():
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
	if(movement>1000):
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
	if(Battery_COMPARE):
		Battery_STATUS = "POTENTIAL RISK"
		if (risk<=3.1):risk = 3.192
	#reporting
	#file=open('./log.txt','a')
	#file.write(  tabulate([['IMEI', IMEI[0], IMEI[1], IMEI_COMPARE, IMEI_STATUS], 
	#				['IMSI', IMSI[0], IMSI[1], IMSI_COMPARE, IMSI_STATUS], 
	#				['Latitude', Latitude[0], Latitude[1], movement, movement_status], 
	#				['Longitude', Longitude[0], Longitude[1], movement, movement_status], 
	#				['RX', RX[0], RX[1], RX_COMPARE, RX_STATUS], 
	#				['TX', TX[0], TX[1], TX_COMPARE, TX_STATUS], 
	#				['Wakeup', Wakeup[0], Wakeup[1], Wakeup_COMPARE, Wakeup_STATUS], 
	#				['Watchdog', Watchdog[0], Watchdog[1], Watchdog_COMPARE, Watchdog_STATUS], 
	#				['Battery', Battery[0], Battery[1], Battery_COMPARE,  Battery_STATUS]], 
	#				headers=['ASSET', 'ACTUAL READING', 'PREVIOUS READING', 'DELTA', 'STATUS'], tablefmt="rst") )
	#file.close()
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
	RX_risk = 0
	TX_risk = 0
	Battery_risk = 0

	print ("1\n")
	Time_historyRX = (np.delete(np.array(TIME_ready_RX), [0])).reshape(len(np.array(TIME_ready_RX))-1, 1) 
	print ("1\n")
	RX_prediction.append(SVR(kernel='linear',C=0.00001,gamma='auto',epsilon=0.00001,tol=0.0001).fit(Time_historyRX ,np.delete(RX_ready,[0])).predict(TIME_ready_RX[0]))

	print ("2\n")
	Time_historyTX = (np.delete(np.array(TIME_ready_TX), [0])).reshape(len(np.array(TIME_ready_TX))-1, 1) 
	print ("2\n")
	TX_prediction.append(SVR(kernel='linear',C=0.00001,gamma='auto',epsilon=0.00001,tol=0.0001).fit(Time_historyTX ,np.delete(TX_ready,[0])).predict(TIME_ready_TX[0]))

	print ("3\n")
	Time_history = (np.delete(np.array(relativeTime), [0])).reshape(len(np.array(relativeTime))-1, 1)
	print ("3\n")
	Battery_prediction.append(SVR(kernel='linear',C=0.00001,gamma='auto',epsilon=0.00001,tol=0.0001).fit(Time_history,np.delete(Battery,[0])).predict(relativeTime[0]))

	RX_Delta = (abs((RX[0]-RX_prediction[0][0])/(RX[0])))*100
	TX_Delta = (abs((TX[0]-TX_prediction[0][0])/(TX[0])))*100
	Battery_Delta = (abs((Battery[0]-Battery_prediction[0][0])/(Battery[0])))*100

	RX_risk = RX_Delta/20
	TX_risk = TX_Delta/20
	Battery_risk = Battery_Delta/20

	#file=open('./log.txt', 'a')
	#file.write(  tabulate([['RX', RX[0], RX_prediction[0], RX_Delta, RX_risk], 
	#				['TX', TX[0], TX_prediction[0], TX_Delta, TX_risk],  
	#				['Battery', Battery[0], Battery_prediction[0],  Battery_Delta, Battery_risk]], 
	#				headers=['ASSET', 'ACTUAL READING', 'PREDICTION', 'DELTA PERCENTAGE', 'RISK'], tablefmt="rst") )
	#file.close()
	print(  tabulate([['RX', RX[0], RX_prediction[0], RX_Delta, RX_risk], 
					['TX', TX[0], TX_prediction[0], TX_Delta, TX_risk],  
					['Battery', Battery[0], Battery_prediction[0],  Battery_Delta, Battery_risk]], 
					headers=['ASSET', 'ACTUAL READING', 'PREDICTION', 'DELTA PERCENTAGE', 'RISK'], tablefmt="rst") )

	return "%.3f" %(RX_risk + TX_risk + Battery_risk)





def graphAgainstTime(asset, label, predictionArray):
	str1 = "  "+ label + " prediction"
	str2 = "  "+ label + " actual device reading"
	#prepare dicretory
	myPath = "LSS " + datetime.datetime.now().strftime("%I %M%p %B %d %Y")
	if not os.path.exists(myPath):
		os.makedirs(myPath)
	# Plot the History
	fig = pl.figure()
	TIME = np.array(POSIXTIME)
	assetHistory = (np.delete(asset, [0])).reshape(len(asset)-1, 1)
	timeHistory = (np.delete(TIME, [0])).reshape(len(TIME)-1, 1)
	#print(len(assetHistory))
	#print(len(timeHistory))
	pl.plot(timeHistory, assetHistory, linestyle='--', marker='o', c='b', label=label)
	# Plot the Prediction and Actual device reading
	pl.scatter(TIME[0], predictionArray[0], c='r')
	pl.annotate(str1, xy=(TIME[0][0], predictionArray[0][0]), xytext=(TIME[0][0], predictionArray[0][0]),fontsize=10,)
	pl.scatter(TIME[0], asset[0], c='r')
	pl.annotate(str2, xy=(TIME[0][0], asset[0]), xytext=(TIME[0][0], asset[0]),fontsize=10,)
	pl.plot([TIME[0][0],TIME[0][0] ], [predictionArray[0], asset[0]], c='r')
	#prepare image
	title = "u-blox SVR ("+label+")"
	pl.xlabel('unixTime', fontsize=14)
	pl.ylabel(label, fontsize=14)
	pl.title(title)
	pl.grid(True)
	#prepare file
	filename = myPath+"/"+label+".png"
	pl.savefig(filename)# dpi=500
	pl.show()
	pl.close(fig)




def graph():
	graphAgainstTime(IMEI, "IMEI", IMEI_prediction)#1
	graphAgainstTime(IMSI, "IMSI", IMSI_prediction)#2
	graphAgainstTime(Latitude, "Latitude", Latitude_prediction)#3
	graphAgainstTime(Longitude, "Longitude", Longitude_prediction)#4
	graphAgainstTime(RX, "RX", RX_prediction)#5
	graphAgainstTime(TX, "TX", TX_prediction)#6
	graphAgainstTime(Wakeup, "Wakeup", Wakeup_prediction)#7
	graphAgainstTime(Watchdog, "Watchdog", Watchdog_prediction)#8
	graphAgainstTime(Battery, "Battery", Battery_prediction)#9

	


def lssAgent():
	warnings.filterwarnings("ignore", category=DeprecationWarning) 
	risk = 0.0
	rd = ["1","2","3"]

	while True:
		for i in range(len(rd)):
			reset()
			try:
				riskDB = getDB(rd[i])
				elapsed = elapsedTime()
				if(float(elapsed)>=330):
					#****************** DEVICE_OFFLINE **********************
					print "RawID:(%s) ID:(%s) Status:(OFFLINE)"  %(riskDB,rd[i])
					postStatus(rd[i],"0")
					postDB(riskDB, 4.99)
				else:
					#****************** DEVICE_ONLINE ***********************
					postStatus(rd[i],"1")
					if(isNew(rd[i])):
						risk = compareAssets()                      #range[4, 4.8]
						if(risk == 0): risk = runMachineLearning()  #range[0, 2.5]
						postDB(riskDB, risk)
						print "RawID:(%s) ID:(%s) ElasedTime:(%s) Status:(ONLINE) RisckScore(%s)"  %(riskDB,rd[i],elapsed,risk)
					else:
						print "RawID:(%s) ID:(%s) Status:(ONLINE)"  %(riskDB,rd[i])
			except Exception, e:
				print(str(e))
				postDB(riskDB, 4.90)

			time.sleep(10)



def main():
	try:
		lssAgent()
	except Exception, e:
		print(str(e))


if __name__ == "__main__":
    main()
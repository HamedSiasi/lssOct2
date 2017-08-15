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
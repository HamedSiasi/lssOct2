
#!/usr/bin/python

import json
import MySQLdb

global db, cursor
db = MySQLdb.connect("localhost","root","ubx@MLB2016","lss")
cursor = db.cursor()

def closeDB():
	db.close()


def version():
	cursor.execute("SELECT VERSION()")
	data = cursor.fetchone()
	print "Database version : %s " % data


def main():
    version()
    read("3")
    closeDB()


def read(deviceID):
	print(deviceID)
	cursor.execute("SELECT * FROM RawData WHERE DeviceId = '%s'" %(deviceID) )
	data = cursor.fetchone()
	print(data[2])

	j = json.loads(data[2])
	print j['a2']
	#results = cursor.fetchall()
	#print(results)
	#for row in results:
	#	IMEI = row[0]
	#	IMSI = row[1]
	#	Latitude = row[2]
	#	Longitude = row[3]
	#	RXC = row[4]
	#	TXC = row[5]
	#	Wakeup = row[6]
	#	Watchdog = row[7]
	#	Battery = row[8]
	#	print "IMEI:%s  IMSI:%s  Latitude:%d  Longitude:%s  RXC:%d  TXC:%d  Wakeup:%d  Watchdog:%d  Battery:%d" %(IMEI,IMSI,Latitude,Longitude,RXC,TXC,Wakeup,Watchdog,Battery)

if __name__ == "__main__":
    main()
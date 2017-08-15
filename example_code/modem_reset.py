#! / usr / bin / env python
import sys
import time
import traceback
import logging

from loggerinitializer import *

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Defaults

BUS = ModbusClient(method='rtu', port='/dev/pic',baudrate=115200,timeout=0.5 ,stopbits=1, parity='N', bytesize=8)
connection = BUS.connect()
#logging.debug("[ModemReset] Modbus connection status: %s" %connection)
print connection

#logging.info("[ModemReset] Turning off the Modem ...")
print "[ModemReset] Turning off the Modem ..."
rq = BUS.write_coil(96, False)
#logging.debug("[ModemReset] %s" %rq)
print rq
               
#logging.info("[ModemReset] Turning on the Modem ...")
print "[ModemReset] Turning on the Modem ..."
rq = BUS.write_coil(96, True)
#logging.debug("[ModemReset] %s" %rq)
print rq
time.sleep(5)
BUS.close()




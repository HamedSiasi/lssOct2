#!/usr/bin/env python
  
import sys
import os
import serial
import time
from loggerinitializer import *

def AT(command):
               try:
                              time.sleep(0.1)
                              ser = serial.Serial(port='/dev/modem',baudrate=115200, timeout=1)        
                              print ser.portstr         # check which port was really used                                     
                                             
                              ser.write (command) # write a string
                              time.sleep(0.2)
                              ser.close() # close port
               except:
                              try:
                                             time.sleep(0.2)
                                             ser = serial.Serial(port='/dev/pic',baudrate=115200, timeout=1)                                             
                                             #logging.debug("[LED_E3] %s" %ser )                                            
                                             if state:
                                                            PresetSingle = LED_E3_ON + stCRC(LED_E3_ON)
                                             else:
                                                            PresetSingle = LED_E3_OFF + stCRC(LED_E3_OFF)
                                                            
                                             ser.write (PresetSingle)
                                             time.sleep(0.2)
                                             ser.close()
                              except:
                                             logging.error("[LED_E3  ERROR]  ERROR !!!") 

#!/usr/bin/env python
import socket
import logging
import urllib2, urllib
import datetime

from sq import *
from loggerinitializer import *


class MyException(Exception):
    pass
    

miab_method = 'POST'
#miab_method = 'GET'                        
   
   
   
   
   
                              
                              
def miab():
               #print miab_method
               if miab_method == "GET":
                              try:
                                             req = urllib2.Request("http://www.acotelnet.com/miab.php")
                                             r = urllib2.urlopen(req,None, 15)                                    
                                             code = r.code                               
                                             info = r.info()
                                             logging.debug(info)
                                             timestamp = r.read()
                                             #print info
                                             #print timestamp                                                                                           
                                             if code==200:
                                                            logging.debug("[miab_get] code: %s  timestamp: %s" %(code,timestamp) ) 
                                                            return "OK"
                                             else:
                                                            logging.error("[miab_get] code:%s ---> KO !!! (point:14)" %code)
                                                            return "KO" 

                              except urllib2.URLError as e:
                                             logging.error("[miab_get] %s  --->  KO !!! (point:15)"  %type(e))  
                                             return "KO"
                              
                              except socket.timeout as e:  
                                             logging.error("[miab_get] %s  --->  KO !!! (point:16)"  %type(e)) 
                                             return "KO"
                                             
               
               
               else:
                              try:
                                             con_type = str(select_db("general_table", "connection_type"))
                                             
                                             if  con_type == "ETH":
                                                            status_data = dict(
                                                                           host =                                  str(select_db("general_table", "host")),
                                                                           mac =                                  str(select_db("general_table", "mac")),
                                                                           connection_type =              str(con_type), 
                                                                           message =                          str(select_db("general_table", "message")) 
                                                                                          )
                                                                                          
                                                                                          
                                                                           
                                             elif con_type == "VPN":
                                                            status_data = dict(
                                                                           host =                                  str(select_db("general_table", "host")),
                                                                           mac =                                  str(select_db("general_table", "mac")),
                                                                           connection_type =              str(con_type), 
                                                                           eth_ip  =                              str(select_db("adsl_table", "eth_ip")),
                                                                           vpn_ip  =                             str(select_db("adsl_table", "vpn_ip")),
                                                                           message =                          str(select_db("general_table", "message")) 
                                                                                          )
                                                                                          
                                                                                          
                                                                           
                                             elif con_type == "GPRS":
                                                            status_data = dict(
                                                                           host =                                  str(select_db("general_table", "host")),
                                                                           mac =                                  str(select_db("general_table", "mac")),
                                                                           connection_type =              str(con_type), 
                                                                           gprs_ip =                             str(select_db("modem_table", "gprs_ip")),
                                                                           modem_status =                str(select_db("modem_table", "modem_status")),
                                                                           modem_signal_quality =   str(select_db("modem_table", "modem_signal_quality")),
                                                                           modem_register_status =  str(select_db("modem_table", "modem_register_status")),
                                                                           modem_imei =                   str(select_db("modem_table", "modem_imei")),
                                                                           modem_imsi =                   str(select_db("modem_table", "modem_imsi")),
                                                                           message =                          str(select_db("general_table", "message")) 
                                                                                          )
                                                                                          
                                                                                          
                                                                           
                                             else:
                                                            status_data = dict(
                                                                           host =                                  str(select_db("general_table", "host")),
                                                                           mac =                                  str(select_db("general_table", "mac")),
                                                                           connection_type =              str(con_type), 
                                                                           message =                          str(select_db("general_table", "message")) 
                                                                                          )
                              
                              
                              

                                             url = 'http://www.acotelnet.com/miab.php'
                                             data = urllib.urlencode(status_data)
                                             logging.info( "POST miab ---> |%s|" %data.replace("&","|") )
                                             req = urllib2.Request(url, data)
                                             response = urllib2.urlopen(req)
                                             code = response.code
                                             info = response.info()
                                             read = response.read()
                                             #print code
                                             #print info
                                             #print read
                                             logging.info("POST miab <--- %s" %code)
                                             logging.debug("[miab_post] read: %s" %read)
               
                                             if code==200:
                                                            return "OK"
                                             else:
                                                            logging.error("[miab_post] code: %s ---> KO !!!" %code)
                                                            return "KO"                              
                              
                              
                              except urllib2.URLError as e:               
                                             logging.error("[miab_post] %s  --->  KO !!! (point:15)"  %type(e))  
                                             return "KO"
                              
                              
                              except socket.timeout as e:                 
                                             logging.error("[miab_post] %s  --->  KO !!! (point:16)"  %type(e)) 
                                             return "KO"
           
                                  
#miab()           
#HAMED_SIASI 
#14 MAGGIO 2015
                       

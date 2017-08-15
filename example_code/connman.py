#!/usr/bin/env python
import sys, os, time, syslog, threading, logging, dbus

from loggerinitializer import *
init_logger()


#---------------------------------------------------------------
#              Hamed Siasi
#              Start coding: 30/03/2015  ANEVDUE 756
#              v1.0: 14/04/2015
#              v2.0: 15/06/2015
#
#---------------------------------------------------------------

from date import *
from eth import *
from miab import *
from vpn import *
from gprs import *
from LED_serial import *
from sq import *





global STATE, TIMER, vpn_problem_counter
STATE = "START"
TIMER = 1
vpn_problem_counter = 0
    
    
    
           
           
             
def START():
               logging.info("")
               logging.info("STATE ----> START")
               global STATE  
               update_db("general_table", "host", host() ) #DB
               update_db("general_table", "serial_code", serial_code() ) #DB 
               update_db("general_table", "mac", mac() ) #DB   
               #--- eth up ---
               counter = 0
               while True:
                              if eth_up() == "OK":
                                             time.sleep(7)
                                             update_db("general_table", "connection_type","ETH") #DB
                                             update_db("adsl_table", "eth_ip",eth_ip()) #DB
                                             update_db("adsl_table", "eth_ip_method",ip_method('Eth')) #DB
                                             update_db("adsl_table", "vpn_ip","---") #DB
                                             update_db("ports_table", "eth_1194",check_1194()) #DB
                                             update_db("ports_table", "eth_123",check_123()) #DB
                                             update_db("ports_table", "eth_80",check_80()) #DB
                                             update_db("adsl_table", "dns1_ip",dns1_ip()) #DB
                                             update_db("adsl_table", "dns2_ip",dns2_ip()) #DB
                                             update_db("adsl_table", "gateway",Gateway_ip()) #DB
                                             
                                             mydate = date()
                                             #logging.info("mydate: %s"  %mydate)
                                             if mydate != "KO":
                                                            update_db("general_table", "last_check", mydate  ) #DB
                                                            update_db("adsl_table", "last_check", mydate  ) #DB
                                                            update_db("ports_table", "last_check", mydate  ) #DB
             
                                                         
#                                             dump_general_table() 
#                                             dump_adsl_table()
#                                             dump_ports_table()
                                             break
                              elif (counter<2):
                                             counter += 1
                                             logging.debug("[START] %s try to eth_up failed ! Retry in 2s" %counter)
                                             time.sleep(1)
                                             continue
                              else:
                                             logging.debug("[START] %s try to eth_up failed !!!" %counter)
                                             STATE = "NEED_GPRS"
                                             return
               #--- GET via eth ---
               counter = 0
               while True:
                              if miab() == "OK":
                                             LED_E3(True)
                                             time.sleep(0.2)
                                             LED_E3(True)
                                             time.sleep(0.2)
                                             LED_E3(True)
                                             time.sleep(0.2)
                                             break
                              elif (counter<2):
                                             try:
                                                            eth_down()#eth down
                                                            time.sleep(1)
                                                            eth_up()#eth up
                                                            time.sleep(15)
                                             except:
                                                            logging.error("[START] Impossible to reset eth !!! (point:1)")
                                                            
                                             counter += 1
                                             logging.debug("[START] %s try to miab_eth failed ! Retry in 6s" %counter)
                                             continue
                              else:
                                             LED_E3(False)
                                             time.sleep(0.3)
                                             LED_E3(False)
                                             logging.debug("[START] %s try to miab_eth failed !!!" %counter)
                                             eth_down()
                                             time.sleep(0.3)
                                             STATE = "NEED_GPRS"
                                             return
               #--- VPN UP ---
               counter = 0
               while True:
                              if vpn_up() == "OK":
                                             update_db("general_table", "connection_type","VPN") #DB
                                             update_db("adsl_table", "vpn_ip",vpn_ip() ) #DB
                                             update_db("adsl_table", "vpn_ip_method", ip_method('Vpn')) #DB
                                             update_db("ports_table", "vpn_123",check_123()) #DB
                                             update_db("ports_table", "vpn_80",check_80()) #DB
                                             
                                             mydate = date()
                                             #logging.info("mydate: %s"  %mydate)
                                             if mydate != "KO":
                                                            update_db("general_table", "last_check", mydate ) #DB
                                                            update_db("adsl_table", "last_check", mydate ) #DB
                                                            update_db("ports_table", "last_check", mydate ) #DB
                                                            
                                                            
                                                                                                         

#                                             dump_adsl_table()
#                                             dump_ports_table()

                                             STATE = "CONNECTED_VPN"
                                             return
                              elif (counter<2):
                                             counter += 1
                                             logging.debug("[START] %s try to vpn_up failed ! Retry in 3s" %counter)
                                             try:
                                                            date()
                                                            #logging.info("---> |%s|"  %date() )
                                             except:
                                                            logging.error("[START] Impossible to set date from miab !!! (point:2)")                                                            
                                             time.sleep(3)
                                             continue
                              else:
                                             logging.debug("[START] %s try to vpn_up failed !!!" %counter)
                                             eth_down()
                                             STATE = "NEED_GPRS"
                                             return
               

   
   
               
               
               
               
               
               
               



def NEED_GPRS():
               logging.info("")
               logging.info("STATE ---> NEED_GPRS")
               global STATE
               #--------------------------------- GPRS UP ----------------------------------------
               counter = 0
               while True:
                              if gprs_up() == "OK":
                                             time.sleep(7)
                                             update_db("general_table", "connection_type","GPRS") #DB
                                             update_db("modem_table", "gprs_ip", gprs_ip() ) #DB
                                             update_db("modem_table", "gprs_ip_method", ip_method('Modem') ) #DB
                                             update_db("ports_table", "gprs_123",check_123()) #DB
                                             update_db("ports_table", "gprs_80",check_80()) #DB
                                             
                                             mydate = date()
                                             #logging.info("mydate: %s"  %mydate)
                                             if mydate != "KO":
                                                            update_db("general_table", "last_check", mydate ) #DB
                                                            update_db("modem_table", "last_check", mydate ) #DB
                                                            update_db("ports_table", "last_check", mydate ) #DB
                                                            
                                                            
                                                                                                         
#                                             dump_modem_table()
#                                             dump_ports_table()

                                             break
                              elif (counter<2):
                                             counter += 1
                                             logging.debug("[NEED_GPRS] %s try to gprs_up failed ! Retry in 3s" %counter)
                                             time.sleep(3)
                                             continue
                              else:
                                             logging.debug("[NEED_GPRS] %s try to gprs_up failed !!!" %counter)
                                             logging.debug("Total refreshing in 30s ...")
                                             LEDS_OFF()
                                             time.sleep(1)
                                             LEDS_OFF()
                                             time.sleep(30)
                                             STATE = "START"
                                             return
               #----------------------- miab GET via GPRS ------------------------------------
               counter = 0
               while True:
                              if miab() == "OK":
                                             #miab OK
                                             LED_E3(True)
                                             time.sleep(0.1)
                                             LED_GbE(False)
                                             time.sleep(0.1)
                                             LED_GPRS(True)
                                             time.sleep(0.1)
                                             LED_E3(True)
                                             time.sleep(0.1)
                                             LED_GbE(False)
                                             time.sleep(0.1)
                                             LED_GPRS(True)
                                             time.sleep(0.1)
                                             LED_E3(True)
                                             time.sleep(30) #wait then go to first check of gprs
                                             STATE = "CONNECTED_GPRS"
                                             return
                              elif (counter<2):
                                             #miab NO
                                             time.sleep(0.1)
                                             gprs_up() 
                                             time.sleep(6)            
                                             counter += 1
                                             logging.debug("[NEED_GPRS] %s try to miab_gprs failed ! Retry in 3s" %counter)
                                             continue
                              else:
                                             #miab NO for 3 time
                                             LEDS_OFF()
                                             time.sleep(0.5)
                                             LEDS_OFF()
                                             logging.debug("[NEED_GPRS] %s try to miab_gprs failed !!!" %counter)
                                             logging.debug("Total refreshing in 30s ...")
                                             time.sleep(30)
                                             STATE = "START"
                                             return














def CONNECTED_VPN():
               logging.info("")
               logging.info("STATE ---> CONNECTED_VPN")
               global STATE, vpn_problem_counter
               #-------------------------------------------- check vpn ------------------------------------
               time.sleep(1)
               counter = 0
               while True:
                              if vpn_check() == "OK":
                                             LED_E3(True)
                                             time.sleep(1)
                                             LED_E3(True)
                                             time.sleep(1)
                                             LED_E3(True)
                                             
                                             vpn_problem_counter = 0
                                             update_db("adsl_table", "vpn_ip", vpn_ip() ) #DB
                                             update_db("adsl_table", "vpn_ip_method", ip_method('Vpn') ) #DB
                                             update_db("ports_table", "vpn_123",check_123()) #DB
                                             update_db("ports_table", "vpn_80",check_80()) #DB
                                             
                                             mydate = date()
                                             #logging.info("mydate: %s"  %mydate)
                                             if mydate != "KO":
                                                            update_db("adsl_table", "last_check", mydate ) #DB
                                                            update_db("ports_table", "last_check", mydate ) #DB
                                                            
                                                            
#                                             dump_general_table() 
#                                             dump_adsl_table()
#                                             dump_ports_table()

                                             time.sleep(60) # 10 min
                                             STATE = "CONNECTED_VPN"
                                             return
                                             
                              elif (counter<2):
                                             counter += 1
                                             logging.debug("[CONNECTED_VPN] %s try to vpn_check failed ! Retry in 3s" %counter)
                                             time.sleep(1)
                                             continue
                                             
                              else:
                                             logging.debug("[CONNECTED_VPN] %s try to vpn_check failed !!!" %counter)
                                             vpn_problem_counter += 1
                                             
                                             try:
                                                            eth_down()
                                                            LEDS_OFF()
                                                            time.sleep(1)
                                                            LEDS_OFF()
                                             except:
                                                            logging.error("[CONNECTED_VPN] impossible to eth_down(point:3)")
                                             
                                             
                                             if (vpn_problem_counter<10):
                                                            logging.info("Total refreshing in 30s ... vpn_problem_counter: %s" %vpn_problem_counter)
                                                            update_db("general_table", "connection_type","NONE") #DB
                                                            time.sleep(30)
                                                            STATE = "START"
                                                            return
                                             else:
                                                            logging.error("[CONNECTED_VPN] VPN PROBLEM ----> NEED_GPRS \n\n\n")
                                                            update_db("general_table", "connection_type","NONE") #DB
                                                            STATE = "NEED_GPRS"
                                                            return


















def CONNECTED_GPRS():
               logging.info("")
               logging.info("STATE ---> CONNECTED_GPRS")
               global STATE, TIMER
               TIMER += 1 #Refreshing timer
               #-------------------------------------------- check gprs ------------------------------------------
               counter = 0
               while True:
                              if gprs_check() == "OK":
                                             if(TIMER>14):
                                                            #time to refresh the system to check if eth0 is up again
                                                            time.sleep(3)
                                                            logging.info("STATE  ---->  START")
                                                            TIMER = 1
                                                            try:
                                                                           eth_down()
                                                                           time.sleep(1)
                                                                           gprs_down()
                                                                           time.sleep(1)
                                                            except:
                                                                           logging.error("[CONNECTED_GPRS] ERROR (point:4)")
                                                                           
                                                            STATE = "START"
                                                            return
                                             else:
                                                            #check miab to verify if gprs is really up
                                                            time.sleep(1)
                                                            counter_miab = 0
                                                            while True:
                                                                           if miab() == "OK":
                                                                                          #miab:OK => OK
                                                                                          LED_E3(True)
                                                                                          time.sleep(1)
                                                                                          LED_E3(True)
                                                                                          time.sleep(1)
                                                                                          LED_E3(True)
                                                                                          
                                                                                          logging.debug("[CONNECTED_GPRS] gprs_check: OK ... TIMER:%s",TIMER)
                                                                                          update_db("modem_table", "gprs_ip", gprs_ip() ) #DB
                                                                                          update_db("modem_table", "gprs_ip_method", ip_method('Modem') ) #DB
                                                                                          update_db("ports_table", "gprs_123",check_123()) #DB
                                                                                          update_db("ports_table", "gprs_80",check_80()) #DB
                                                                                          
                                                                                          mydate = date()
                                                                                          #logging.info("mydate: %s"  %mydate)
                                                                                          if mydate != "KO":
                                                                                                         update_db("modem_table", "last_check", mydate ) #DB
                                                                                                         update_db("ports_table", "last_check", mydate ) #DB
                                                                                                         
                                                                                                         
#                                                                                          dump_general_table()                
#                                                                                          dump_modem_table()
#                                                                                          dump_ports_table()

                                                                                          time.sleep(60) #10 min sleep
                                                                                          STATE = "CONNECTED_GPRS"
                                                                                          return
                                                                           elif (counter_miab<2):
                                                                                          LED_E3(False)
                                                                                          time.sleep(0.5)
                                                                                          LED_E3(False)
                                                                                          time.sleep(0.5)
                                                                                          LED_E3(False)
                                                                                          #miab:KO =>  Try again
                                                                                          gprs_up()
                                                                                          counter_miab += 1
                                                                                          logging.debug("[CONNECTED_GPRS] %s try to miab_gprs failed ! Retry in 3s" %counter_miab)
                                                                                          time.sleep(5)
                                                                                          continue
                                                                           else:
                                                                                          #miab:KO  =>  Shutting down gprs go to total refreshing
                                                                                           LEDS_OFF()
                                                                                           time.sleep(1)
                                                                                           LEDS_OFF()
                                                                                           logging.debug("[CONNECTED_GPRS] %s try to gprs_check failed !!!" %counter)
                                                                                           gprs_down()
                                                                                           logging.debug("Total refreshing in 30s ...")
                                                                                           update_db("general_table", "connection_type","NONE") #DB
                                                                                           time.sleep(30)
                                                                                           STATE = "START"
                                                                                           return                                                                           
                              elif (counter<3):
                                             #gprs_check:KO => Try again
                                             counter += 1
                                             logging.debug("[CONNECTED_GPRS] %s try to gprs_check failed ! Retry in 3s" %counter)
                                             time.sleep(3)
                                             continue
                              else:
                                             #gprs_check:KO => Shutting down gprs go to total refreshing
                                             logging.debug("[CONNECTED_GPRS] %s try to gprs_check failed !!!" %counter)
                                             gprs_down()
                                             LEDS_OFF()
                                             time.sleep(0.5)
                                             LEDS_OFF()
                                             logging.debug("Total refreshing in 30s ...")
                                             update_db("general_table", "connection_type","NONE") #DB
                                             time.sleep(30)
                                             STATE = "START"
                                             return





    
  
  
  
  
  
  
    
    
               
               
def FSM_RUN():
               # -------------------------------- Finite State Machine (FSM) ------------------------------------------
               global STATE, TIMER
               while True:
                              if STATE == "START": 
                                             try:
                                                            update_db("general_table", "message","START") #DB                                                          
                                                            LEDS_OFF()
                                                            #cleaning ...
                                                            time.sleep(0.1)
                                                            eth_down()
                                                            time.sleep(0.1)
                                                            gprs_down()
                                                            time.sleep(0.1)
                                                            LEDS_OFF()
                                                            time.sleep(0.1)
                                                            
                                                            #Start FSM ...
                                                            START()
                                             except Exception, e:
                                                            update_db("general_table", "message","ERROR") #DB
                                                            update_db("general_table", "last_check",date()) #DB                                                          
                                                            logging.error("[FSM ERROR] START ERROR ----> %s !!!" %str(e) )
                                                            LEDS_OFF()
                                                            STATE = "ERROR"
                                                            time.sleep(60)
                                                            continue
                                                                
                                                                    
                                                                    
                                                                      
                                                                      
                                                                                        
                              elif STATE == "NEED_GPRS":
                                             try:
                                                            update_db("general_table", "message","NEED_GPRS") #DB                                                             
                                                            LEDS_OFF()
                                                            time.sleep(0.2)
                                                            LEDS_OFF() 
                                                            time.sleep(0.2) 
                                                            NEED_GPRS()
                                             except Exception, e:
                                                            update_db("general_table", "message","ERROR") #DB
                                                            update_db("general_table", "last_check",date()) #DB
                                                            logging.error("[FSM ERROR] NEED_GPRS ERROR ---> %s !!!" %str(e) )
                                                            LEDS_OFF()
                                                            STATE = "ERROR"
                                                            time.sleep(60)
                                                            continue
                               
                               
                               
                               
                               
                                                                       
                              elif STATE == "CONNECTED_VPN":
                                             try:
                                                            update_db("general_table", "message","CONNECTED_VPN") #DB                                                           
                                                            LED_GPRS(False)
                                                            time.sleep(0.2)
                                                            LED_GbE(True)
                                                            time.sleep(0.2)
                                                            LED_GPRS(False)
                                                            time.sleep(0.2)
                                                            LED_GbE(True)
                                                            time.sleep(0.3)
                                                            LED_GbE(True)
                                                            time.sleep(0.1)
                                                            
                                                            CONNECTED_VPN()
                                             except Exception, e:
                                                            update_db("general_table", "message","ERROR") #DB
                                                            update_db("general_table", "last_check",date()) #DB                                                            
                                                            logging.error("[FSM ERROR] CONNECTED_VPN ERROR ---> %s !!!" %str(e) )
                                                            LEDS_OFF()
                                                            STATE = "ERROR"
                                                            time.sleep(60)
                                                            continue
                              
                              
                              
                              
                              
                                                                       
                              elif STATE == "CONNECTED_GPRS": 
                                             try:
                                                            update_db("general_table", "message","CONNECTED_GPRS") #DB                                                           
                                                            LED_GbE(False)
                                                            time.sleep(0.2)
                                                            LED_GPRS(True)
                                                            time.sleep(0.3)
                                                            LED_GbE(False)
                                                            time.sleep(0.2)
                                                            LED_GPRS(True)
                                                            time.sleep(0.2)
                                                            LED_GPRS(True)
                                                            time.sleep(0.1)
                                                            
                                                            CONNECTED_GPRS()
                                             except Exception, e:
                                                            update_db("general_table", "message","ERROR") #DB
                                                            update_db("general_table", "last_check",date()) #DB
                                                            logging.error("[FSM ERROR] CONNECTED_GPRS ERROR ---> %s !!!" %str(e) )
                                                            LEDS_OFF()
                                                            STATE = "ERROR"
                                                            time.sleep(60)
                                                            continue
                              
                                                           
                                                           
                                                           
                                                           
                                                           
                              else: #---unknown state---
                                             logging.error("[FSM ERROR] unknown state !!! (point:10)")
                                             LEDS_OFF()
                                             try:
                                                            os.system("/etc/init.d/network-manager status")
                                                            os.system("/etc/init.d/dbus status")
                                             except Exception, e:
                                                            logging.error("[FSM ERROR] sys error ---> %s !!!" %str(e) )
                                                            
                                             STATE = "START"
                                             time.sleep(60)
                                             continue
                              
                              
 

 








                              
#------------------------------------------- Daemonize ---------------------------------------
def writePidFile():
    pidd = str(os.getpid())
    syslog.syslog(syslog.LOG_INFO, 'connman [PID] - %s -' % pidd)
    logging.info("connman pid: %s ----> /var/run/connman.pid" %pidd)
    f = open('/var/run/connman.pid', 'w')
    f.write(pidd)
    f.close()


def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # Perform first fork.
    try:
        pid = os.fork( )
        if pid > 0:
	#    writePidFile(str(pid))
            sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid( )
    # Perform second fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # The process is now daemonized, redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush( )
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno( ), sys.stdin.fileno( ))
    os.dup2(so.fileno( ), sys.stdout.fileno( ))
    os.dup2(se.fileno( ), sys.stderr.fileno( ))

def _example_main ( ):
               writePidFile()
               FSM_RUN()
               syslog.syslog(syslog.LOG_INFO, 'connman - Close Main() -')


#------------------------------------------------ main ------------------------------------
if __name__ == "__main__":
	daemonize('/dev/null','/tmp/connman.log','/tmp/connman.log')
    	_example_main( )




#              HAMED_SIASI 
#              14 MAGGIO 2015
#              TGHDIM BE MOLAM HOSSEIN







 
 
 
 
            
               
               



                             


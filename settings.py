#! /usr/bin/env python3
# coding: utf-8


""" LbGate settings, global variables"""


import time
import copy
import socket

import fct
import gpio
import alarm


HTTPD_PORT = 8444
MAX_NODE_ERRORS = 10000
HOSTNAME = "Unknown"
API_KEY = ""
SMS_IDS = []
EMAIL_IDS = []
LIGHT_BEETLE_IS_ENABLED = False

def init():
    global HOSTNAME
    global API_KEY
    global SMS_IDS
    global EMAIL_IDS
    global LIGHT_BEETLE_IS_ENABLED
    if socket.gethostname() == "frdom":
        HOSTNAME = "Frenes"
        API_KEY = "sQDe2Zt1ei2tWi7eebsj3J8jHGLaDOI3"
        SMS_IDS = ["146", "147", "148", "149"]
        EMAIL_IDS = ["150"]
        LIGHT_BEETLE_IS_ENABLED = False
    if socket.gethostname() == "btdom":
        HOSTNAME = "Bourdilot"
        API_KEY = "sQDe2Zt1ei2tWi7eebsj3J8jHGLaDOI3"
        SMS_IDS = ["146", "147", "148", "149"]
        EMAIL_IDS = ["150"]
        LIGHT_BEETLE_IS_ENABLED = True

def sms_url_get(smsid):
    global API_KEY
    global HOSTNAME
    return ('http://127.0.0.1:8080/core/api/jeeApi.php?'
           'apikey='+API_KEY+'&'
           'type=cmd&id='+smsid+'&title=Jeedom_'+HOSTNAME+'&message=')
def email_url_get(emailid):
    global API_KEY
    global HOSTNAME
    return ('http://127.0.0.1:8080/core/api/jeeApi.php?'
            'apikey='+API_KEY+'&'
            'type=cmd&id='+emailid+'&title=Jeedom_'+HOSTNAME+'&message=')


run_loop = 0
log_msg = ""

def run():
    """
        Cycle execution to update log file
    """
    global HOSTNAME
    global run_loop
    global log_msg
    try:
        flog = open("/dev/shm/lbGate.settings", "w")
        msg = "###########################\n"
        msg = msg + "### " + HOSTNAME + " " + time.strftime('%Y/%m/%d %H:%M:%S') + " ###\n"
        msg = msg + "ALARM: enabled: " + str(alarm.is_enabled()) + " triggered: " + str(alarm.is_triggered()) + " timeout: " + str(alarm.timeout_get()) + " stopped: " + str(alarm.is_stopped()) + " sum: " + str(alarm.sum()) + "\n"
        msg = msg + "GPIO: buzzer: " + str(gpio.buzzer_get()) + "\n"
        msg = msg + "      move0: " + str(gpio.move0_get()) + " move1: " + str(gpio.move1_get()) + " move2: " + str(gpio.move2_get()) + "\n"
        msg = msg + "      move3: " + str(gpio.move3_get()) + " move4: " + str(gpio.move4_get()) + " move5: " + str(gpio.move5_get()) + "\n"
        msg = msg + "      move6: " + str(gpio.move6_get()) + " move7: " + str(gpio.move7_get()) + "\n"
        msg = msg + "      rack: " + str(gpio.rack_get()) + " light: " + str(gpio.light_get()) + " ups_in: " + str(gpio.ups_in_get()) + " rf: " + str(gpio.rf_get()) + "\n"
        msg = msg + "      ups0: " + str(gpio.ups0_get()) + " ups1: " + str(gpio.ups1_get()) + " ups2: " + str(gpio.ups2_get()) + "\n"
        msg = msg + "- run_loop = " + str(run_loop) + "\n"
        log_msg = msg
        flog.write(msg)
        flog.close()
    except Exception as ex:
        fct.log_exception(ex)
    run_loop = run_loop + 1


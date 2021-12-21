#! /usr/bin/env python3
# coding: utf-8


""" LbGate settings, global variables"""


import time
import copy

import fct
import gpio
import alarm


HTTPD_PORT = 8444
MAX_NODE_ERRORS = 10000
SMS_URL1 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
           'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
           'type=cmd&id=167&title=Jeedom_Bourdilot&message=')
SMS_URL2 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
           'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
           'type=cmd&id=168&title=Jeedom_Bourdilot&message=')
SMS_URL3 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
           'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
           'type=cmd&id=165&title=Jeedom_Bourdilot&message=')
SMS_URL4 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
           'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
           'type=cmd&id=166&title=Jeedom_Bourdilot&message=')
EMAIL_URL1 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
             'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
             'type=cmd&id=169&title=Jeedom_Bourdilot&message=')
EMAIL_URL2 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
             'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
             'type=cmd&id=170&title=Jeedom_Bourdilot&message=')
EMAIL_URL3 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
             'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
             'type=cmd&id=171&title=Jeedom_Bourdilot&message=')
EMAIL_URL4 = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
             'apikey=eqQ5X8TgSwbkHRAuTpFJsAlGVOFauBOt&'
             'type=cmd&id=172&title=Jeedom_Bourdilot&message=')

ALARM_NAME_URL = ('http://127.0.0.1:8080/core/api/jeeApi.php?'
                  'plugin=virtual&apikey=xxxxxxxx&'
                  'type=virtual&id=xxx&value=')

run_loop = 0
log_msg = ""

def run():
    """
        Cycle execution to update log file
    """
    global run_loop
    global log_msg
    try:
        flog = open("/dev/shm/lbGate.settings", "w")
        msg = "###########################\n"
        msg = msg + "### " + time.strftime('%Y/%m/%d %H:%M:%S') + " ###\n"
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


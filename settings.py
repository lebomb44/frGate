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
LIGHT_BEETLE_IS_ENABLED = False
ALARM_NAME = dict()

def init():
    global HOSTNAME
    global LIGHT_BEETLE_IS_ENABLED
    global ALARM_NAME
    if socket.gethostname() == "frdom":
        HOSTNAME = "Frenes"
        LIGHT_BEETLE_IS_ENABLED = False
        ALARM_NAME["move0"] = "NotUsed0"
        ALARM_NAME["move1"] = "NotUsed1"
        ALARM_NAME["move2"] = "Petit Salon"
        ALARM_NAME["move3"] = "Avant"
        ALARM_NAME["move4"] = "Move Etage"
        ALARM_NAME["move5"] = "NotUsed2"
        ALARM_NAME["move6"] = "Move Couloir"
        ALARM_NAME["move7"] = "Move Petit Salon"
    if socket.gethostname() == "btdom":
        HOSTNAME = "Bourdilot"
        LIGHT_BEETLE_IS_ENABLED = True
        ALARM_NAME["move0"] = "Move Bas"
        ALARM_NAME["move1"] = "Move Haut"
        ALARM_NAME["move2"] = "Avant"
        ALARM_NAME["move3"] = "Arriere"
        ALARM_NAME["move4"] = "NotUsed0"
        ALARM_NAME["move5"] = "NotUsed1"
        ALARM_NAME["move6"] = "NotUsed2"
        ALARM_NAME["move7"] = "NotUsed3"


run_loop = 0
log_msg = ""

def run():
    """
        Cycle execution to update log file
    """
    global HOSTNAME
    global ALARM_NAME
    global run_loop
    global log_msg
    try:
        flog = open("/dev/shm/lbGate.settings", "w")
        msg = "###########################\n"
        msg = msg + "### " + HOSTNAME + " " + time.strftime('%Y/%m/%d %H:%M:%S') + " ###\n"
        msg = msg + "ALARM: enabled: " + str(alarm.is_enabled()) + " triggered: " + str(alarm.is_triggered()) + " timeout: " + str(alarm.timeout_get()) + " stopped: " + str(alarm.is_stopped()) + " sum: " + str(alarm.sum()) + "\n"
        msg = msg + "GPIO: buzzer: " + str(gpio.buzzer_get()) + "\n"
        msg = msg + "      " + ALARM_NAME["move0"] + ": " + str(gpio.move0_get()) + ", " + ALARM_NAME["move1"] + ": " + str(gpio.move1_get()) + ", " + ALARM_NAME["move2"] + ": " + str(gpio.move2_get()) + "\n"
        msg = msg + "      " + ALARM_NAME["move3"] + ": " + str(gpio.move3_get()) + ", " + ALARM_NAME["move4"] + ": " + str(gpio.move4_get()) + ", " + ALARM_NAME["move5"] + ": " + str(gpio.move5_get()) + "\n"
        msg = msg + "      " + ALARM_NAME["move6"] + ": " + str(gpio.move6_get()) + ", " + ALARM_NAME["move7"] + ": " + str(gpio.move7_get()) + "\n"
        msg = msg + "      rack: " + str(gpio.rack_get()) + " light: " + str(gpio.light_get()) + " ups_in: " + str(gpio.ups_in_get()) + " rf: " + str(gpio.rf_get()) + "\n"
        msg = msg + "      ups0: " + str(gpio.ups0_get()) + " ups1: " + str(gpio.ups1_get()) + " ups2: " + str(gpio.ups2_get()) + "\n"
        msg = msg + "- run_loop = " + str(run_loop) + "\n"
        log_msg = msg
        flog.write(msg)
        flog.close()
    except Exception as ex:
        fct.log_exception(ex)
    run_loop = run_loop + 1


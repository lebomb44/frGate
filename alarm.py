#! /usr/bin/env python3
# coding: utf-8


""" Alarm management """


import copy
import time
import socket
import subprocess

import settings
import fct
import gpio

alarm_is_enabled = False
alarm_is_enabled_by_hw = False
alarm_triggered = False
alarm_timeout = 0
alarm_stopped = False
alarm_status = dict()
alarm_initial_status = dict()
alarm_sum = False

def init():
    global alarm_is_enabled
    global alarm_is_enabled_by_hw
    global alarm_triggered
    global alarm_timeout
    global alarm_stopped
    global alarm_sum
    alarm_is_enabled = False
    alarm_is_enabled_by_hw = gpio.rf_get()
    alarm_triggered = False
    alarm_timeout = 0
    alarm_stopped = False
    alarm_status = dict()
    alarm_initial_status = dict()
    alarm_sum = False
    gpio.buzzer_off()
    gpio.light_off()

def run():
    global alarm_is_enabled
    global alarm_is_enabled_by_hw
    global alarm_triggered
    global alarm_timeout
    global alarm_stopped
    global alarm_status
    global alarm_initial_status
    global alarm_sum
    """
        Cycle execution to poll on sensors
    """
    if alarm_is_enabled_by_hw != gpio.rf_get():
        alarm_is_enabled_by_hw = gpio.rf_get()
        if alarm_is_enabled_by_hw == True:
            enable()
        else:
            disable()
    try:
        alarm_status["move0"] = gpio.move0_get()
        alarm_status["move1"] = gpio.move1_get()
        alarm_status["move2"] = gpio.move2_get()
        alarm_status["move3"] = gpio.move3_get()
        alarm_status["move4"] = gpio.move4_get()
        alarm_status["move5"] = gpio.move5_get()
        alarm_status["move6"] = gpio.move6_get()
        alarm_status["move7"] = gpio.move7_get()
        alarm_sum = True
        for sensor_name, sensor_value in alarm_status.items():
            alarm_sum = alarm_sum & sensor_value

        if alarm_is_enabled is True:
            if alarm_triggered is True:
                if 10*60 < alarm_timeout:
                    gpio.buzzer_off()
                    if alarm_stopped is False:
                        fct.send_alert("BUZZER stopped")
                        alarm_stopped = True
                else:
                    alarm_timeout = alarm_timeout + 1
                    # Turn on the buzzer
                    gpio.buzzer_on()
            else:
                diff_found = False
                msg = ""
                for sensor_name, sensor_value in alarm_status.items():
                    if sensor_value != alarm_initial_status[sensor_name]:
                        diff_found = True
                        msg = msg + " " + sensor_name
                if diff_found is True:
                    alarm_triggered = True
                    alarm_timeout = 0
                    alarm_stopped = False
                    gpio.buzzer_on()
                    fct.send_alert("ALARM started:" + msg)
                else:
                    gpio.buzzer_off()
        else:
            alarm_initial_status = copy.deepcopy(alarm_status)
            gpio.buzzer_off()
    except Exception as ex:
        fct.log_exception(ex)


def enable():
    global alarm_is_enabled
    init()
    alarm_is_enabled = True
    gpio.light_on()
    if settings.LIGHT_BEETLE_IS_ENABLED is True:
        try:
            ip = socket.gethostbyname("galerie")
            subprocess.run("sudo -u jeedom ssh root@" + ip + " \"echo \\\"beetleTemp lightMode set 3\n\\\" > /dev/ttyACM0\"", shell=True, check=False, timeout=2.0)
        except:
            pass
    fct.log("Alarm enabled")


def disable():
    global alarm_is_enabled
    init()
    alarm_is_enabled = False
    gpio.light_off()
    if settings.LIGHT_BEETLE_IS_ENABLED is True:
        try:
            ip = socket.gethostbyname("galerie")
            subprocess.run("sudo -u jeedom ssh root@" + ip + " \"echo \\\"beetleTemp lightMode set 0\n\\\" > /dev/ttyACM0\"", shell=True, check=False, timeout=2.0)
        except:
            pass
    fct.log("Alarm disabled")


def is_enabled():
    global alarm_is_enabled
    return alarm_is_enabled


def is_enabled_by_hw():
    global alarm_is_enabled_by_hw
    return alarm_is_enabled_by_hw


def is_triggered():
    global alarm_triggered
    return alarm_triggered


def timeout_get():
    global alarm_timeout
    return alarm_timeout


def is_stopped():
    global alarm_stopped
    return alarm_stopped


def sum():
    global alarm_sum
    return alarm_sum

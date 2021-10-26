#! /usr/bin/env python3
# coding: utf-8


""" Alarm management """


import copy
import time

import fct
import gpio

alarm_is_enabled = False
alarm_triggered = False
alarm_timeout = 0
alarm_stopped = False
alarm_sum = False

def init():
    global alarm_is_enabled
    global alarm_triggered
    global alarm_timeout
    global alarm_stopped
    global alarm_sum
    alarm_is_enabled = False
    alarm_triggered = False
    alarm_timeout = 0
    alarm_stopped = False
    alram_sum = False
    gpio.buzzer_off()
    gpio.light_off()

def run():
    global alarm_is_enabled
    global alarm_triggered
    global alarm_timeout
    global alarm_stopped
    global alarm_sum
    """
        Cycle execution to poll on sensors
    """
    try:
        alarm_sum = gpio.move0_get() & gpio.move1_get() & gpio.move2_get() & gpio.move3_get() & gpio.move4_get() & gpio.move5_get()
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
                if alarm_sum is True:
                    alarm_triggered = True
                    alarm_timeout = 0
                    alarm_stopped = False
                    gpio.buzzer_on()
                    fct.send_alert("ALARM started")
                else:
                    gpio.buzzer_off()
        else:
            gpio.buzzer_off()
    except Exception as ex:
        fct.log_exception(ex)


def enable():
    global alarm_is_enabled
    init()
    alarm_is_enabled = True
    gpio.light_on()


def disable():
    init()


def is_enabled():
    global alarm_is_enabled
    return alarm_is_enabled


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

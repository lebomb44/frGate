#! /usr/bin/env python3
# coding: utf-8


""" LbGate basic functions """


from __future__ import print_function
import time
import traceback
from six.moves import urllib
import requests

import settings
import myconfig
import alarm
import lbemail


sms = None

def log(msg):
    """ Print message with a time header """
    print(time.strftime('%Y/%m/%d %H:%M:%S: ') + msg)


def log_exception(ex, msg="ERROR Exception"):
    """ Print exception with a time header """
    log(msg + ": " + str(ex))
    log(traceback.format_exc())


def http_request(url):
    """ Do HTTP request to the URL """
    try:
        log("URL call: " + url)
        requests.get(url, timeout=1.0)
    except requests.exceptions.RequestException as ex:
        log("ERROR http_request: " + str(ex))


def send_sms(msg):
    """ Send SMS message """
    global sms
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send SMS: " + msg)
    for phone in myconfig.SMS:
        sms.sendto(phone, msg)


def send_email(msg):
    """ Send e-mail """
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send EMAIL: " + msg)
    for email in myconfig.EMAIL:
        lbemail.sendto(email, msg, msg)


def send_alert(msg):
    """ Send a global alert (SMS + E-mail) """
    send_sms(msg)
    send_email(msg)


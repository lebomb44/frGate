#! /usr/bin/env python3
# coding: utf-8


""" LbGate basic functions """


from __future__ import print_function
import time
import traceback
from six.moves import urllib
import requests

import settings


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
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send SMS: " + msg)
    for smsid in settings.SMS_IDS:
        http_request(settings.sms_url_get(smsid) + urllib.parse.quote(msg))


def send_email(msg):
    """ Send e-mail """
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send EMAIL: " + msg)
    for emailid in settings.EMAIL_IDS:
        http_request(settings.email_url_get(emailid) + urllib.parse.quote(msg))


def send_alert(msg):
    """ Send a global alert (SMS + E-mail) """
    send_sms(msg)
    send_email(msg)

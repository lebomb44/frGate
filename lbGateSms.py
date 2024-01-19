#! /usr/bin/env python3
# coding: utf-8


""" LbGate main """


import http.server
import threading
import signal
import sys
import time
import json
import io
import fcntl
import os
import queue
import urllib.parse

import myconfig

HTTPD_PORT = 8445

def log(msg):
    """ Print message with a time header """
    print(time.strftime('%Y/%m/%d %H:%M:%S: ') + msg)


def log_exception(ex, msg="ERROR Exception"):
    """ Print exception with a time header """
    log(msg + ": " + str(ex))
    log(traceback.format_exc())

def send_sms(msg):
    """ Send SMS message """
    global sms
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send SMS: " + msg)
    for phone in myconfig.SMS:
        sms.sendto(phone, msg)

class Sms(threading.Thread):
    """ Class for a serial port """
    def __init__(self, name):
        self.dict = dict()
        self.dict["port"] = "/dev/" + name
        self.dict["node_name"] = name
        self.dict["signal_quality"] = 0
        self.dict["open_cnt"] = 0
        self.dict["nb_config"] = 0
        self.dict["nb_loop"] = 0
        self.dict["is_loop_enabled"] = True
        self.fd_port = io.IOBase()
        self.line = ""
        self.smsqueue = queue.Queue(1000)
        self.read_iter = 0
        threading.Thread.__init__(self, name=name)


    def run(self):
        """ Cyclic execution to poll for received characters """
        self.dict["nb_loop"] = 1
        while self.dict["is_loop_enabled"] is True:
            try:
                #log("DEBUG: " + self.dict["node_name"] + " loop " + str(loop_nb))
                if self.is_open() is False:
                    self.open()
                    time.sleep(1.0)
                if self.is_open() is True:
                    line = ""
                    cserial = " "
                    read_iter_ = 0
                    while (len(cserial) > 0) and (self.dict["is_loop_enabled"] is True):
                        try:
                            cserial = self.fd_port.read(1)
                            if cserial is None:
                                cserial = ""
                            else:
                                cserial = cserial.decode(encoding='utf-8', errors='ignore')
                            if len(cserial) > 0:
                                read_iter_ = read_iter_ + 1
                                if ord(cserial) == 0:
                                    cserial = ""
                            else:
                                cserial = ""
                            if (self.line != "") and (cserial == "\n" or cserial == "\r"):
                                line = self.line
                                self.line = ""
                                # log("DEBUG New line create=" + line)
                                break
                            else:
                                if (cserial != "\n") and (cserial != "\r"):
                                    self.line = self.line + cserial
                        except Exception as ex:
                            self.line = ""
                            cserial = ""
                            log_exception(ex, msg="ERROR while decoding data on " + self.dict["node_name"])
                            self.close()
                    if read_iter_ > self.read_iter:
                        self.read_iter = read_iter_
                    if line != "":
                        line_array = line.split(" ")
                        #log("DEBUG: line_array=" + str(line_array))
                        if len(line_array) == 2:
                            if line_array[0] == "+CSQ:":
                                try:
                                    self.dict["signal_quality"] = int(round(float(line_array[1].replace(",","."))))
                                except Exception as ex:
                                    self.dict["signal_quality"] = 0
                                    log_exception(ex)
                    if self.dict["nb_loop"] % 50000 == 0:
                        self.config()
                    if self.dict["nb_loop"] % 1000 == 0:
                        if self.smsqueue.empty() is False:
                            try:
                                msg = self.smsqueue.get()
                                if msg != '':
                                    self.write(msg)
                            except Exception as ex:
                                log_exception(ex)
                else:
                    self.dict["signal_quality"] = 0
            except Exception as ex:
                log_exception(ex)
                self.close()
            self.dict["nb_loop"] += 1
            if self.dict["nb_loop"] >= 1000000:
                self.dict["nb_loop"] = 0
            time.sleep(0.001)


    def stop(self):
        """ Stop polling loop """
        log("Stopping " + self.dict["node_name"] + " thread...")
        self.dict["is_loop_enabled"] = False
        time.sleep(1.0)
        log("Closing " + self.dict["node_name"] + " node...")
        if self.is_open() is True:
            self.fd_port.close()


    def is_open(self):
        """ Check if serial port is already open """
        try:
            ret = fcntl.fcntl(self.fd_port, fcntl.F_GETFD)
            return ret >= 0
        except:
            return False


    def open(self):
        """ Open the serial port """
        try:
            log("Opening " + self.dict["node_name"])
            self.fd_port = open(self.dict["port"], "rb+", buffering=0)
            fd_port = self.fd_port.fileno()
            flag = fcntl.fcntl(fd_port, fcntl.F_GETFL)
            fcntl.fcntl(fd_port, fcntl.F_SETFL, flag | os.O_NONBLOCK)
            self.dict["open_cnt"] += 1
            self.dict["nb_config"] = 0
            self.dict["signal_quality"] = 0
        except Exception as ex:
            log_exception(ex)


    def close(self):
        """ Close the serial port """
        try:
            if self.is_open() is True:
                log("Closing " + self.dict["node_name"])
                self.fd_port.close()
            self.dict["signal_quality"] = 0
        except Exception as ex:
            log_exception(ex)


    def write(self, msg):
        """ Write the serial port if already open """
        try:
            if self.is_open() is True:
                self.fd_port.write((msg + "\r").encode('utf-8'))
                #log("DEBUG: Write serial to node " + self.dict["node_name"] + ": " + msg)
                self.fd_port.flush()
        except Exception as ex:
            log_exception(ex)


    def config(self):
        """ Configure modem """
        try:
            self.smsqueue.put_nowait('ATZ')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('AT+CMGF=1')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('AT+CSCA="+33695000695"')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('AT+CSQ')
            self.smsqueue.put_nowait('')
            self.dict["nb_config"] += 1
        except Exception as ex:
            log_exception(ex)


    def sendto(self, phone, msg):
        """ Send SMS message to phone number """
        try:
            msg = urllib.parse.unquote_plus(msg)
            self.smsqueue.put_nowait('AT+CMGS="' + str(phone) + '"')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait(str(msg) + "\x1A")
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
        except Exception as ex:
            log_exception(ex)


    def callto(self, phone):
        """ Send SMS message to phone number """
        try:
            self.smsqueue.put_nowait('ATD' + str(phone) + ';')
            for i in range(0,30):
                self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('ATH')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
        except Exception as ex:
            log_exception(ex)


class CustomHandler(http.server.BaseHTTPRequestHandler):
    """ Custom HTTP handler """
    def ok200(self, resp, content_type='text/plain'):
        """ Return OK page """
        try:
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            if content_type == 'text/plain':
                self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())
            else:
                self.wfile.write((resp).encode())
            self.wfile.flush()
        except Exception as ex:
            log_exception(ex)

    def error404(self, resp):
        """ Return page not found """
        try:
            self.send_response(404)
            self.end_headers()
            self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())
            self.wfile.flush()
        except Exception as ex:
            log_exception(ex)

    def log_message(self, format, *args):
        """ Overwrite default log function """
        return

    def do_GET(self):
        """ Callback on HTTP GET request """
        url_tokens = self.path.split('/')
        url_tokens_len = len(url_tokens)
        #log(str(url_tokens))
        if url_tokens_len > 1:
            api = url_tokens[1]
            if api == "api":
                if url_tokens_len > 2:
                    node = url_tokens[2]
                    if node == "sms":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "sendto":
                                if url_tokens_len == 6:
                                    sms.sendto(url_tokens[4], url_tokens[5])
                                    self.ok200("Sending SMS to " + url_tokens[4] + ": " + url_tokens[5])
                                else:
                                    self.error404("Bad number of argment for command sms.sendto")
                            elif url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    send_sms(url_tokens[4])
                                    self.ok200("Sending SMS to all : " + url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command send_sms")
                            elif url_tokens[3] == "json":
                                try:
                                    self.ok200(json.dumps(sms.dict, sort_keys=True, indent=4), content_type="application/json")
                                except:
                                    self.error404("Bad json dump of 'sms' node")
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    else:
                        self.error404("Bad node: " + node)
                else:
                    self.error404("Command too short: " + api)
            else:
                self.error404("Bad location: " + api)
        else:
            self.error404("Url too short")


httpserver = http.server.ThreadingHTTPServer(("", settings.HTTPD_PORT), CustomHandler)

sms=Sms("ttyUSB0")

def exit():
    """ Stop HTTP server, stop serial threads and monitoring thread """
    global httpserver
    log("Stopping HTTP server")
    httpserver.server_close()
    sms.stop()
    time.sleep(2.0)


def signal_term_handler(signal_, frame_):
    """ Capture Ctrl+C signal and exit program """
    log('Got SIGTERM, exiting...')
    exit()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    sms.start()
    log("Serving at port " + str(HTTPD_PORT))
    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        exit()


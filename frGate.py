#! /usr/bin/env python3
# coding: utf-8


""" LbGate main """


import http.server
import threading
import signal
import sys
import time
import json

import gpio
import settings
import fct
import alarm

class Monitoring(threading.Thread):
    """ Monitoring class """
    def __init__(self, name):
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        """ Cyclic execution for polling on alarm, move and settings """
        loop_nb = 1
        while self.is_loop_enabled is True:
            #fct.log("DEBUG: Monitoring loop " + str(loop_nb))
            if loop_nb % 10 == 0:
                alarm.run()
                settings.run()
            loop_nb += 1
            if loop_nb >= 1000000:
                loop_nb = 0
            time.sleep(0.1)

    def stop(self):
        """ Stop monitoring thread """
        fct.log("Stopping Monitoring thread...")
        self.is_loop_enabled = False
        time.sleep(1.0)


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
        except Exception as ex:
            fct.log_exception(ex)

    def error404(self, resp):
        """ Return page not found """
        try:
            self.send_response(404)
            self.end_headers()
            self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())
        except Exception as ex:
            fct.log_exception(ex)

    def log_message(self, format, *args):
        """ Overwrite default log function """
        return

    def do_GET(self):
        """ Callback on HTTP GET request """
        url_tokens = self.path.split('/')
        url_tokens_len = len(url_tokens)
        fct.log(str(url_tokens))
        if url_tokens_len > 1:
            api = url_tokens[1]
            if api == "api":
                if url_tokens_len > 2:
                    node = url_tokens[2]
                    if node == "lbgate":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "alarm":
                                if url_tokens_len > 4:
                                    if url_tokens[4] == "enable":
                                        alarm.enable()
                                        self.ok200("Alarm is enabled: ")
                                    elif url_tokens[4] == "disable":
                                        alarm.disable()
                                        self.ok200("Alarm is disabled")
                                    else:
                                        try:
                                            token_nbs = range(5, url_tokens_len)
                                            node_point = settings.alarm
                                            for token_index in token_nbs:
                                                node_point = node_point[url_tokens[token_index]]
                                            self.ok200(json.dumps(node_point, sort_keys=True, indent=4), content_type="application/json")
                                        except:
                                            self.error404("Bad path in 'alarm'")
                                else:
                                    self.ok200("Alarm is = " + str(alarm.is_enabled()) +
                                               "\nTrigger = " + str(alarm.is_triggered()) +
                                               "\nTimer = " + str(alarm.timeout_get()) +
                                               "\nStop = " + str(alarm.is_stopped()) +
                                               "\nSum = " + str(alarm.sum()))
                            elif url_tokens[3] == "gpio":
                                if url_tokens_len > 4:
                                    if url_tokens[4] == "buzzer":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "on":
                                                gpio.buzzer_on()
                                                self.ok200("BUZZER ON")
                                            elif url_tokens[5] == "off":
                                                gpio.buzzer_off()
                                                self.ok200("BUZZER OFF")
                                            elif url_tokens[5] == "json":
                                                self.ok200(json.dumps({"buzzer": gpio.buzzer_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD BUZZER")
                                        else:
                                            self.ok200(str(gpio.buzzer_get()))
                                    elif url_tokens[4] == "move0":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move0": gpio.move0_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE0")
                                        else:
                                            self.ok200(str(gpio.move0_get()))
                                    elif url_tokens[4] == "move1":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move1": gpio.move1_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE1")
                                        else:
                                            self.ok200(str(gpio.move1_get()))
                                    elif url_tokens[4] == "move2":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move2": gpio.move2_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE2")
                                        else:
                                            self.ok200(str(gpio.move2_get()))
                                    elif url_tokens[4] == "move3":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move3": gpio.move3_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE3")
                                        else:
                                            self.ok200(str(gpio.move3_get()))
                                    elif url_tokens[4] == "move4":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move4": gpio.move4_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE4")
                                        else:
                                            self.ok200(str(gpio.move4_get()))
                                    elif url_tokens[4] == "move5":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move5": gpio.move5_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE5")
                                        else:
                                            self.ok200(str(gpio.move5_get()))
                                    elif url_tokens[4] == "rack":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"rack": gpio.rack_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD RACK")
                                        else:
                                            self.ok200(str(gpio.rack_get()))
                                    elif url_tokens[4] == "light":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "on":
                                                gpio.light_on()
                                                self.ok200("LIGHT ON")
                                            elif url_tokens[5] == "off":
                                                gpio.light_off()
                                                self.ok200("LIGHT OFF")
                                            elif url_tokens[5] == "json":
                                                self.ok200(json.dumps({"light": gpio.light_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD LIGHT")
                                        else:
                                            self.ok200(str(gpio.light_get()))
                                    elif url_tokens[4] == "ups0":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "on":
                                                gpio.ups0_on()
                                                self.ok200("UPS0 ON")
                                            elif url_tokens[5] == "off":
                                                gpio.ups0_off()
                                                self.ok200("UPS0 OFF")
                                            elif url_tokens[5] == "json":
                                                self.ok200(json.dumps({"ups0": gpio.ups0_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD UPS0")
                                        else:
                                            self.ok200(str(gpio.ups0_get()))
                                    elif url_tokens[4] == "ups1":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "on":
                                                gpio.ups1_on()
                                                self.ok200("UPS1 ON")
                                            elif url_tokens[5] == "off":
                                                gpio.ups1_off()
                                                self.ok200("UPS1 OFF")
                                            elif url_tokens[5] == "json":
                                                self.ok200(json.dumps({"ups1": gpio.ups1_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD UPS1")
                                        else:
                                            self.ok200(str(gpio.ups1_get()))
                                    elif url_tokens[4] == "ups2":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "on":
                                                gpio.ups2_on()
                                                self.ok200("UPS2 ON")
                                            elif url_tokens[5] == "off":
                                                gpio.ups2_off()
                                                self.ok200("UPS2 OFF")
                                            elif url_tokens[5] == "json":
                                                self.ok200(json.dumps({"ups2": gpio.ups2_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD UPS2")
                                        else:
                                            self.ok200(str(gpio.ups2_get()))
                                    else:
                                        self.error404("BAD GPIO")
                                else:
                                    self.ok200("GPIO TEXT")
                            elif url_tokens[3] == "json":
                                try:
                                    token_nbs = range(4, url_tokens_len)
                                    node_point = settings.acq
                                    for token_index in token_nbs:
                                        node_point = node_point[url_tokens[token_index]]
                                    self.ok200(json.dumps(node_point, sort_keys=True, indent=4), content_type="application/json")
                                except:
                                    self.error404("Bad path in 'acq'")
                            elif url_tokens[3] == "sendsms":
                                if url_tokens_len > 4:
                                    self.ok200("Sending SMS: " + url_tokens[4])
                                    fct.send_sms(url_tokens[4])
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.ok200(settings.log_msg)
                    else:
                        self.error404("Bad node: " + node)
                else:
                    self.error404("Command too short: " + api)
            else:
                self.error404("Bad location: " + api)
        else:
            self.error404("Url too short")


monitoring = Monitoring("Monitoring")
httpserver = http.server.HTTPServer(("", settings.HTTPD_PORT), CustomHandler)


def exit():
    """ Stop HTTP server, stop serial threads and monitoring thread """
    global monitoring
    global httpserver
    fct.log("Stopping HTTP server")
    httpserver.server_close()
    monitoring.stop()
    time.sleep(2.0)


def signal_term_handler(signal_, frame_):
    """ Capture Ctrl+C signal and exit program """
    fct.log('Got SIGTERM, exiting...')
    exit()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    gpio.init()
    alarm.init()
    monitoring.start()
    fct.log("Serving at port " + str(settings.HTTPD_PORT))
    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        exit()


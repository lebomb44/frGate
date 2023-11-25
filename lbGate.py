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
import lbsms
import lbemail

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
            if loop_nb % 600 == 0:
                alarm.update_status()
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
                                        self.ok200("ALARM ENABLED")
                                    elif url_tokens[4] == "disable":
                                        alarm.disable()
                                        self.ok200("ALARM DISABLED")
                                    elif url_tokens[4] == "json":
                                        self.ok200(json.dumps({"enabled": alarm.is_enabled(), "triggered": alarm.is_triggered(), "timeout": alarm.timeout_get(), "stopped": alarm.is_stopped(), "sum": alarm.sum()}, sort_keys=True, indent=4), content_type="application/json")
                                    else:
                                        self.error404("BAD ALARM")
                                else:
                                    self.ok200("\nAlarm is = " + str(alarm.is_enabled()) +
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
                                    elif url_tokens[4] == "move6":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move6": gpio.move6_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE6")
                                        else:
                                            self.ok200(str(gpio.move6_get()))
                                    elif url_tokens[4] == "move7":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"move7": gpio.move7_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD MOVE7")
                                        else:
                                            self.ok200(str(gpio.move7_get()))
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
                                    elif url_tokens[4] == "ups_in":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"ups_in": gpio.ups_in_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD UPS_IN")
                                        else:
                                            self.ok200(str(gpio.ups_in_get()))
                                    elif url_tokens[4] == "rf":
                                        if url_tokens_len > 5:
                                            if url_tokens[5] == "json":
                                                self.ok200(json.dumps({"rf": gpio.rf_get()}, sort_keys=True, indent=4), content_type="application/json")
                                            else:
                                                self.error404("BAD RF")
                                        else:
                                            self.ok200(str(gpio.rf_get()))
                                    elif url_tokens[4] == "json":
                                        self.ok200(json.dumps({"buzzer": gpio.buzzer_get(),
                                                               "move0": gpio.move0_get(), "move1": gpio.move1_get(), "move2": gpio.move2_get(), "move3": gpio.move3_get(), "move4": gpio.move4_get(), "move5": gpio.move5_get(), "move6": gpio.move6_get(), "move7": gpio.move7_get(),
                                                               "rack": gpio.rack_get(), "light": gpio.light_get(), "ups_in": gpio.ups_in_get(), "rf": gpio.rf_get(),
                                                               "ups0": gpio.ups0_get(), "ups1": gpio.ups1_get(), "ups2": gpio.ups2_get()},
                                                               sort_keys=True, indent=4), content_type="application/json")
                                    else:
                                        self.error404("BAD GPIO")
                                else:
                                    self.ok200("\nGPIO: buzzer: " + str(gpio.buzzer_get()) + "\n"
                                               "      move0: " + str(gpio.move0_get()) + " move1: " + str(gpio.move1_get()) + " move2: " + str(gpio.move2_get()) + "\n" +
                                               "      move3: " + str(gpio.move3_get()) + " move4: " + str(gpio.move4_get()) + " move5: " + str(gpio.move5_get()) + "\n" +
                                               "      move6: " + str(gpio.move6_get()) + " move7: " + str(gpio.move7_get()) + "\n" +
                                               "      rack: " + str(gpio.rack_get()) + " light: " + str(gpio.light_get()) + " ups_in: " + str(gpio.ups_in_get()) + " rf: " + str(gpio.rf_get()) + "\n" +
                                               "      ups0: " + str(gpio.ups0_get()) + " ups1: " + str(gpio.ups1_get()) + " ups2: " + str(gpio.ups2_get()) + "\n")
                            elif url_tokens[3] == "sendsms":
                                if url_tokens_len > 4:
                                    self.ok200("Sending SMS: " + url_tokens[4])
                                    fct.send_sms(url_tokens[4])
                            elif url_tokens[3] == "json":
                                self.ok200(json.dumps({"alarm": {"enabled": alarm.is_enabled(), "triggered": alarm.is_triggered(), "timeout": alarm.timeout_get(), "stopped": alarm.is_stopped(), "sum": alarm.sum()},
                                                       "gpio": {"buzzer": gpio.buzzer_get(),
                                                                "move0": gpio.move0_get(), "move1": gpio.move1_get(), "move2": gpio.move2_get(), "move3": gpio.move3_get(), "move4": gpio.move4_get(), "move5": gpio.move5_get(), "move6": gpio.move6_get(), "move7": gpio.move7_get(),
                                                                "rack": gpio.rack_get(), "light": gpio.light_get(), "ups_in": gpio.ups_in_get(), "rf": gpio.rf_get(),
                                                                "ups0": gpio.ups0_get(), "ups1": gpio.ups1_get(), "ups2": gpio.ups2_get()},
                                                      },
                                                      sort_keys=True, indent=4), content_type="application/json")
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.ok200(settings.log_msg)
                    elif node == "sms":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "sendto":
                                if url_tokens_len == 6:
                                    sms.sendto(url_tokens[4], url_tokens[5])
                                    self.ok200("Sending SMS to " + url_tokens[4] + ": " + url_tokens[5])
                                else:
                                    self.error404("Bad number of argment for command sms.sendto")
                            elif url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    fct.send_sms(url_tokens[4])
                                    self.ok200("Sending SMS to all : " + url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command fct.send_sms")
                            elif url_tokens[3] == "json":
                                try:
                                    self.ok200(json.dumps(sms.dict, sort_keys=True, indent=4), content_type="application/json")
                                except:
                                    self.error404("Bad json dump of 'sms' node")
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    elif node == "email":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "sendto":
                                if url_tokens_len == 7:
                                    lbemail.sendto(url_tokens[4], url_tokens[5], url_tokens[6])
                                    self.ok200("Sending email to " + url_tokens[4] + ", Object: " + url_tokens[5] + ", Message: " + url_tokens[6])
                                else:
                                    self.error404("Bad number of argment for command lbemail.sendto")
                            elif url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    fct.send_email(url_tokens[4])
                                    self.ok200("Sending email to all : " + url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command fct.send_email")
                            else:
                                self.error404("Bad command for node " + node + ": " + url_tokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    elif node == "alert":
                        if url_tokens_len > 3:
                            if url_tokens[3] == "send":
                                if url_tokens_len == 5:
                                    fct.send_alert(url_tokens[4])
                                    self.ok200("Sending alert to all : " + url_tokens[4])
                                else:
                                    self.error404("Bad number of argment for command fct.send_alert")
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


monitoring = Monitoring("Monitoring")
httpserver = http.server.ThreadingHTTPServer(("", settings.HTTPD_PORT), CustomHandler)

sms=lbsms.Sms("sms")
fct.sms = sms

def exit():
    """ Stop HTTP server, stop serial threads and monitoring thread """
    global monitoring
    global httpserver
    fct.log("Stopping HTTP server")
    httpserver.server_close()
    monitoring.stop()
    sms.stop()
    time.sleep(2.0)


def signal_term_handler(signal_, frame_):
    """ Capture Ctrl+C signal and exit program """
    fct.log('Got SIGTERM, exiting...')
    exit()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    settings.init()
    gpio.init()
    alarm.init()
    sms.start()
    monitoring.start()
    fct.log("Serving at port " + str(settings.HTTPD_PORT))
    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        exit()


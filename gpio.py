import RPi.GPIO as GPIO

######################################################### 
##                 Pin header allocation               ##
######################################################### 
# |      3V3 |      3V3 |  1 |  2 | 5V       | 5V       |
# |          |    GPIO2 |  3 |  4 | 5V       | 5V       |
# |          |    GPIO3 |  5 |  6 | Ground   | GND      |
# |          |    GPIO4 |  7 |  8 | GPIO14   | TX       |
# |      GND |   Ground |  9 | 10 | GPIO15   | RX       |
# |    UPS 2 |   GPIO17 | 11 | 12 | GPIO18   |          |
# |    UPS 0 |   GPIO27 | 13 | 14 | Ground   | GND      |
# |    UPS 1 |   GPIO22 | 15 | 16 | GPIO23   | UPS In   |
# |      3V3 |      3V3 | 17 | 18 | GPIO24   | Move 1   |
# |   Buzzer |   GPIO10 | 19 | 20 | Ground   | GND      |
# |          |    GPIO9 | 21 | 22 | GPIO25   | Rack     |
# |    Light |   GPIO11 | 23 | 24 | GPIO8    | Move 0   |
# |      GND |   Ground | 25 | 26 | GPIO7    | RF       |
# |          |    ID_SD | 27 | 28 | ID_SC    |          |
# |          |    GPIO5 | 29 | 30 | Ground   | GND      |
# |          |    GPIO6 | 31 | 32 | GPIO12   | Move 5   |
# |          |   GPIO13 | 33 | 34 | Ground   | GND      |
# |   Move 7 |   GPIO19 | 35 | 36 | GPIO16   | Move 4   |
# |   Move 6 |   GPIO26 | 37 | 38 | GPIO20   | Move 3   |
# |      GND |   Ground | 39 | 40 | GPIO21   | Move 2   |
######################################################### 

BUZZER_PIN = 19
MOVE0_PIN = 24
MOVE1_PIN = 18
MOVE2_PIN = 40
MOVE3_PIN = 38
MOVE4_PIN = 36
MOVE5_PIN = 32
MOVE6_PIN = 37
MOVE7_PIN = 35
RACK_PIN = 22
LIGHT_PIN = 23
UPS0_PIN = 13
UPS1_PIN = 15
UPS2_PIN = 11
UPS_IN_PIN = 16
RF_PIN = 26
TX_PIN = 8
RX_PIN = 10

def init():
    global BUZZER_PIN
    global MOVE0_PIN
    global MOVE1_PIN
    global MOVE2_PIN
    global MOVE3_PIN
    global MOVE4_PIN
    global MOVE5_PIN
    global MOVE6_PIN
    global MOVE7_PIN
    global RACK_PIN
    global LIGHT_PIN
    global UPS0_PIN
    global UPS1_PIN
    global UPS2_PIN
    global RF_PIN
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    buzzer_off()
    GPIO.setup(MOVE0_PIN, GPIO.IN)
    GPIO.setup(MOVE1_PIN, GPIO.IN)
    GPIO.setup(MOVE2_PIN, GPIO.IN)
    GPIO.setup(MOVE3_PIN, GPIO.IN)
    GPIO.setup(MOVE4_PIN, GPIO.IN)
    GPIO.setup(MOVE5_PIN, GPIO.IN)
    GPIO.setup(MOVE6_PIN, GPIO.IN)
    GPIO.setup(MOVE7_PIN, GPIO.IN)
    GPIO.setup(RACK_PIN, GPIO.IN)
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    light_off()
    GPIO.setup(UPS0_PIN, GPIO.OUT)
    ups0_off()
    GPIO.setup(UPS1_PIN, GPIO.OUT)
    ups1_off()
    GPIO.setup(UPS2_PIN, GPIO.OUT)
    ups2_off()
    GPIO.setup(UPS_IN_PIN, GPIO.IN)
    GPIO.setup(RF_PIN, GPIO.IN)


def buzzer_on():
    global BUZZER_PIN
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzzer_off():
    global BUZZER_PIN
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def buzzer_get():
    global BUZZER_PIN
    return bool(GPIO.input(BUZZER_PIN))

def move0_get():
    global MOVE0_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE0_PIN)))
    return status

def move1_get():
    global MOVE1_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE1_PIN)))
    return status

def move2_get():
    global MOVE2_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE2_PIN)))
    return status

def move3_get():
    global MOVE3_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE3_PIN)))
    return status

def move4_get():
    global MOVE4_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE4_PIN)))
    return status

def move5_get():
    global MOVE5_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE5_PIN)))
    return status

def move6_get():
    global MOVE6_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE6_PIN)))
    return status

def move7_get():
    global MOVE7_PIN
    status = False
    for i in range(0, 10):
        status = status or (not bool(GPIO.input(MOVE7_PIN)))
    return status

def rack_get():
    global RACK_PIN
    return not bool(GPIO.input(RACK_PIN))

def light_on():
    global LIGHT_PIN
    GPIO.output(LIGHT_PIN, GPIO.HIGH)

def light_off():
    global LIGHT_PIN
    GPIO.output(LIGHT_PIN, GPIO.LOW)

def light_get():
    global LIGHT_PIN
    return bool(GPIO.input(LIGHT_PIN))

def ups0_on():
    global UPS0_PIN
    GPIO.output(UPS0_PIN, GPIO.HIGH)

def ups0_off():
    global UPS0_PIN
    GPIO.output(UPS0_PIN, GPIO.LOW)

def ups0_get():
    global UPS0_PIN
    return bool(GPIO.input(UPS0_PIN))

def ups1_on():
    global UPS1_PIN
    GPIO.output(UPS1_PIN, GPIO.HIGH)

def ups1_off():
    global UPS1_PIN
    GPIO.output(UPS1_PIN, GPIO.LOW)

def ups1_get():
    global UPS1_PIN
    return bool(GPIO.input(UPS1_PIN))

def ups2_on():
    global UPS2_PIN
    GPIO.output(UPS2_PIN, GPIO.HIGH)

def ups2_off():
    global UPS2_PIN
    GPIO.output(UPS2_PIN, GPIO.LOW)

def ups2_get():
    global UPS2_PIN
    return bool(GPIO.input(UPS2_PIN))

def ups_in_get():
    global UPS_IN_PIN
    return not bool(GPIO.input(UPS_IN_PIN))

def rf_get():
    global RF_PIN
    return not bool(GPIO.input(RF_PIN))

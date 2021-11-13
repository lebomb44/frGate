import RPi.GPIO as GPIO

BUZZER_PIN = 24
MOVE0_PIN = 19
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
    return bool(GPIO.input(MOVE0_PIN))

def move1_get():
    global MOVE1_PIN
    return bool(GPIO.input(MOVE1_PIN))

def move2_get():
    global MOVE2_PIN
    return bool(GPIO.input(MOVE2_PIN))

def move3_get():
    global MOVE3_PIN
    return bool(GPIO.input(MOVE3_PIN))

def move4_get():
    global MOVE4_PIN
    return bool(GPIO.input(MOVE4_PIN))

def move5_get():
    global MOVE5_PIN
    return bool(GPIO.input(MOVE5_PIN))

def move6_get():
    global MOVE6_PIN
    return bool(GPIO.input(MOVE6_PIN))

def move7_get():
    global MOVE7_PIN
    return bool(GPIO.input(MOVE7_PIN))

def rack_get():
    global RACK_PIN
    return bool(GPIO.input(RACK_PIN))

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

def rf_get():
    global RF_PIN
    return bool(GPIO.input(RF_PIN))

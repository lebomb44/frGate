import RPi.GPIO as GPIO

BUZZER_PIN = 1
MOVE0_PIN = 2
MOVE1_PIN = 3
MOVE2_PIN = 4
MOVE3_PIN = 5
MOVE4_PIN = 6
MOVE5_PIN = 7
RACK_PIN = 8
HEATER_PIN = 9
UPS0_PIN = 10
UPS1_PIN = 11
UPS2_PIN = 12


def init():
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
    GPIO.setup(RACK_PIN, GPIO.IN)
    GPIO.setup(HEATER_PIN, GPIO.OUT)
    heater_off()
    GPIO.setup(UPS0_PIN, GPIO.OUT)
    ups0_off()
    GPIO.setup(UPS1_PIN, GPIO.OUT)
    ups1_off()
    GPIO.setup(UPS2_PIN, GPIO.OUT)
    ups2_off()
    GPIO.setup(UPS3_PIN, GPIO.OUT)
    ups3_off()


def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def move0_get():
    return GPIO.input(MOVE0_PIN)

def move1_get():
    return GPIO.input(MOVE0_PIN)

def move2_get():
    return GPIO.input(MOVE0_PIN)

def move3_get():
    return GPIO.input(MOVE0_PIN)

def move4_get():
    return GPIO.input(MOVE0_PIN)

def move5_get():
    return GPIO.input(MOVE0_PIN)

def rack_get():
    return GPIO.input(RACK_PIN)

def heater_on():
    GPIO.output(HEATER_PIN, GPIO.HIGH)

def heater_off():
    GPIO.output(HEATER_PIN, GPIO.LOW)

def ups0_on():
    GPIO.output(UPS0_PIN, GPIO.HIGH)

def ups0_off():
    GPIO.output(UPS0_PIN, GPIO.LOW)

def ups1_on():
    GPIO.output(UPS1_PIN, GPIO.HIGH)

def ups1_off():
    GPIO.output(UPS1_PIN, GPIO.LOW)

def ups2_on():
    GPIO.output(UPS2_PIN, GPIO.HIGH)

def ups2_off():
    GPIO.output(UPS2_PIN, GPIO.LOW)

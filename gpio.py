import RPi.GPIO as GPIO

BUZZER_PIN = 1
MOVE0_PIN = 2
MOVE1_PIN = 3
MOVE2_PIN = 4
MOVE3_PIN = 5
MOVE4_PIN = 6
MOVE5_PIN = 7

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

# GPIO
import RPi.GPIO as GPIO

# Classes
from classes.config import config

class Light:

    def __init__(self):
        # Set Modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # Define lights
        self.buzzer = int(config.get('SENSORS', 'buzzer'))
        # Setup Lights
        GPIO.setup(self.buzzer, GPIO.OUT)
        self.buzz = GPIO.PWM(self.buzzer, 50)

    def on(self):
        self.buzz.start(50)

    def off(self):
        self.buzz.stop()
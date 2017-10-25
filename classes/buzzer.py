# GPIO
import RPi.GPIO as GPIO

# Classes
from classes.config import config

class Buzzer:

    def __init__(self):
        # Set Modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # Define lights
        self.green = int(config.get('LIGHTS', 'green'))
        self.yellow = int(config.get('LIGHTS', 'yellow'))
        self.red = int(config.get('LIGHTS', 'red'))
        # Setup Lights
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.yellow, GPIO.OUT)
        GPIO.setup(self.red, GPIO.OUT)

    def on(self, light):
        print("power on for GPIO " + str(light))
        GPIO.output(light, True)
        self.state = True

    def off(self, light):
        print("power off for GPIO " + str(light))
        GPIO.output(light, False)
        self.state = False

    def clear(self):
        GPIO.cleanup()

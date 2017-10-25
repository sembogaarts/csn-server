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
        self.green = str(config.get('LIGHTS', 'green'))
        self.yellow = str(config.get('LIGHTS', 'yellow'))
        self.red = str(config.get('LIGHTS', 'red'))
        # Setup Lights
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.yellow, GPIO.OUT)
        GPIO.setup(self.red, GPIO.OUT)

    def on(self, light):
        print("power on for GPIO " + str(self.GPIOPin))
        GPIO.output(light, True)
        self.state = True

    def off(self, light):
        print("power off for GPIO " + str(self.GPIOPin))
        GPIO.output(light, False)
        self.state = False

    def toggle(self, light):
        if light.state:
            light.off()
        else:
            light.on()

    def clear(self):
        GPIO.cleanup()

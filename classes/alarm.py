from classes.light import Light
import time

class Alarm:

    def __init__(self):
        self.light = Light()

    def boot(self):
        self.light.on(self.light.red)
        self.light.on(self.light.yellow)
        self.light.on(self.light.green)
        time.sleep(1)
        self.light.off(self.light.red)
        self.light.off(self.light.yellow)
        self.light.off(self.light.green)

    def start(self):
        self.light.on(self.light.red)

    def stop(self):
        self.light.off(self.light.red)
from classes.light import Light

class Alarm:

    def __init__(self):
        self.light = Light()

    def start(self):
        self.light.on(self.light.red)

    def stop(self):
        self.light.off(self.light.red)
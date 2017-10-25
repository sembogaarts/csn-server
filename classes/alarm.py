from classes.light import Light
from classes.client import Client
import time
from threading import Timer

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

        self.heartbeat = Timer(5.0, self.check)
        self.heartbeat.start()

    def check(self):
        print('Checking clients...')
        self.danger = False
        self.clients = Client.all()
        for client in self.clients:
            if client['online'] == 0:
                print('CLIENT ' + client['name'] + ' IS OFFLINE!')
                self.danger = True
        if self.danger:
            self.start()
        else:
            print('All systems are neutral')
            self.stop()


    def start(self):
        self.light.on(self.light.red)

    def stop(self):
        self.light.off(self.light.red)
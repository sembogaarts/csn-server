from classes.light import Light
from classes.buzzer import Buzzer
from classes.database import Database
from classes.client import Client
from threading import Timer
import time

class Alarm:

    def __init__(self):
        self.light = Light()
        self.buzzer = Buzzer()

    def boot(self):
        Client.resetClients()
        self.light.on(self.light.red)
        self.light.on(self.light.yellow)
        self.light.on(self.light.green)
        time.sleep(1)
        self.light.off(self.light.red)
        self.light.off(self.light.yellow)
        self.light.off(self.light.green)
        self.check()

    def clientsAreOnline(self):
        # Create DB Instance
        db = Database()
        # Check if there are any clients offline
        result = db.fetchAll("SELECT * FROM clients WHERE online = 0")
        # Return the result
        if len(result) == 0:
            print("[ALARM] All clients are up and running")
            return True
        else:
            print("[ALARM] Some clients seem to be offline")
            self.light.on(self.light.yellow)
            return False

    def check(self):
        # Check if all the clients are online
        if self.clientsAreOnline():
            self.stop()
            try:
                self.retryTimer.cancel()
            except:
                print('No instance')
            self.light.on(self.light.green)
        else:
            # Retry in 10 seconds before running the alarm...
            self.light.off(self.light.green)
            self.retryTimer = Timer(10, self.waitToReconnect).start()

    def waitToReconnect(self):
        # Check if all the clients are online
        if not self.clientsAreOnline():
            print("[ALARM] Still no activity, running the alarm!")
            self.start()
        # Turn off the yellow light
        self.light.off(self.light.yellow)

    def start(self):
        self.light.on(self.light.red)
        self.buzzer.on()

    def stop(self):
        self.buzzer.off()
        self.light.off(self.light.red)
        self.light.off(self.light.yellow)
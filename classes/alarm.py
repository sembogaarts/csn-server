from classes.light import Light
from classes.database import Database
from threading import Timer
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
        self.check()

    def clientsAreOnline(self):
        # Create DB Instance
        db = Database()
        # Check if there are any clients offline
        result = db.fetchAll("SELECT * FROM clients WHERE online = 0")
        # Return the result
        if len(result) == 0:
            print("[ALARM] All clients are up and running!")
            return True
        else:
            print("[ALARM] Some clients seem to be offline, retrying...")
            self.light.on(self.light.yellow)
            return False

    def check(self):
        # Check if all the clients are online
        if self.clientsAreOnline():
            self.stop()
        else:
            # Retry in 10 seconds before running the alarm...
            Timer(10, self.waitToReconnect).start()

    def waitToReconnect(self):
        # Check if all the clients are online
        if not self.clientsAreOnline():
            print("[ALARM] Still no activity, running the alarm!")
            self.start()
        # Turn off the yellow light
        self.light.off(self.light.yellow)

    def start(self):
        self.light.on(self.light.red)

    def stop(self):
        self.light.off(self.light.red)
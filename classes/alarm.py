from classes.light import Light
from classes.client import Client
import time
from apscheduler.schedulers.background import BlockingScheduler

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
        # scheduler = BlockingScheduler()
        #
        # alarmSwitch = scheduler.add_job(self.check, 'interval', seconds=5)
        #
        # scheduler.start()

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
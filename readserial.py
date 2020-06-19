from threading import Thread
import time
from cfg import *
from Connect import connect
import random
import time

class readserial():
    def __init__(self, Serial):
        self.serialConnection = Serial
        self.rawdata = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.savedata = False
        self.datafile = None
        self.oldtime = '-1'

    def serialread(self):  # retrieve data
        time.sleep(0.5)
        #self.rawdata = self.serialConnection.readline().decode('utf-8').strip('\r\n').split(',')
        self.rawdata = [random.random(0,100),random.random(0,100),random.random(0,100),random.random(0,100),random.random(0,100),random.random(0,100)]
        if self.savedata == True and self.oldtime != self.rawdata[0]:
            self.datafile.write(','.join(self.rawdata) + '\n')
            self.oldtime = self.rawdata[0]

readserial(False)


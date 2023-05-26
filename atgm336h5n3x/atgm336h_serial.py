"""
    * Author: nipun.dhananjaya@gmail.com
    * Created: 25.05.2023
"""

import serial
from time import time

class ATGM336H_Serial():
    def __init__(self):
        self.ser = None
        self.is_available = False
        self.data = {"GNGLL": None, "GPGSA": None, 
                     "BDGSA": None, "GPGSV": None, 
                     "GNGGA": None, "BDGSV": None, 
                     "GNRMC": None, "GNVTG": None, 
                     "GNZDA": None, "GPTXT": None}

    def connect(self, dev:str = '/dev/ttyUSB0', baud_rate:int = 9600, timeout:int = 1):
        try:
            self.ser = serial.Serial(dev, baud_rate, timeout=timeout)
            self.is_available = self.ser.is_open
            print("ATGM336H device is connected!\n")
            return 1
        except:
            print("ERROR: Could not connect with the device!")
            return 0
        
    def disconnect(self):
        try:
            self.ser.close()
            self.is_available = self.ser.is_open
            if not self.is_available:
                print("Device is disconnected!")
            return 1
        except:
            print("Error: Could not disconnect the device!")
            return 0
        
    def read_data(self, msg_type:str, timeout:int = 1, raw_data=False):
        t_start = time()
        found = False
        data = None
        while (time() - t_start) < timeout:
            if not raw_data:
                line = self.ser.readline().decode('ascii')[:-2].split(',')
                if line[0] == msg_type:
                    data = line[1:]
                    last = data[-1]
                    data.remove(last)
                    data.append(last.split('*')[0])
                    found = True
                    break
            else:
                line = self.ser.readline().decode('ascii')
                if line[:6] == msg_type:
                    data = line
                    found = True
                    break
        if found:
            return data
        else:
            return False


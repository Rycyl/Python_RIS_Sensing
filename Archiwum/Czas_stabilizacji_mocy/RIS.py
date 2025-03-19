import serial
import time
#import sys
#import os
import numpy as np
#import json
#from enum import Enum


class RIS:
    def __init__(self, port, id = 0, timeout = 10, baudrate = 115200):
        self.ser = serial.Serial(port, baudrate = baudrate, timeout = timeout)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.id = id
        self.timeout = timeout
        self.c_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
        
    def __repr__(self):
        return f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}"

    def set_pattern(self, pattern):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(bytes(f"!{pattern}\n", 'utf-8'))
        start_time = time.time()
        while True:
            response = self.ser.readline().decode('utf-8').strip()
            #print(response)
            if response == "#OK":
                self.c_pattern = pattern
                return True
            if time.time() - start_time > self.timeout:
                return False

    
    def reset(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(b"!Reset\n")
        start_time = time.time()
        while True:
            response = self.ser.readline().decode('utf-8').strip()
            #print(response)
            split_response = response.split("\n")
            for response in split_response:
                if response == "#READY!":
                    self.c_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
                    return True
            if time.time() - start_time > self.timeout:
                return False
    
    def read_pattern(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(b"?Pattern\n")
        start_time = time.time()
        while True:
            response = self.ser.readline().decode('utf-8').strip()
            #print(response)
            if response.startswith("#"):
                return response[1:]
            if time.time() - start_time > self.timeout:
                return "TIMEOUT"

    #Reszta do dorobiena jak będzie czas / potrzeba



        
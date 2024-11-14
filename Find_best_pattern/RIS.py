import serial
import time
#import sys
#import os
import numpy as np
#import json
#from enum import Enum

class Virtual_RIS():
    def __init__(self, port, id = 0, timeout = 10, baudrate = 115200):
        self.c_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
        return

    def set_pattern(self, pattern, ack_on = True):
        self.c_pattern = pattern
        if ack_on:
            #print(f"Pattern {pattern} set")
            time.sleep(0.22)
        else:
            pass
        return
    
    def reset(self):
        self.c_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
        time.sleep(0.5)
        return

    def read_pattern(self):
        return self.c_pattern

class Physical_RIS():
    def __init__(self, port, id = 0, timeout = 10, baudrate = 115200):
        self.ser = serial.Serial(port, baudrate = baudrate, timeout = timeout)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.id = id
        self.timeout = timeout
        self.c_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
        print(f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}")
        return
            
        
    def __repr__(self):
        return f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}"

    def set_pattern(self, pattern, ack_on = True):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(bytes(f"!{pattern}\n", 'utf-8'))
        if (ack_on):
            start_time = time.time()
            while True:
                response = self.ser.readline().decode('utf-8').strip()
                #print(response)
                if response == "#OK":
                    self.c_pattern = pattern
                    #print(f"Pattern {pattern} set")
                    return True
                if time.time() - start_time > self.timeout:
                    return False
        else:
            time.sleep(0.002)

    
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



class RIS:
    def __init__(self, port, id=0, timeout=10, baudrate=115200, phy_device = True):
        if phy_device:
            try:
                print("Attempting to connect to Physical RIS...")
                self.ris = Physical_RIS(port, id=id, timeout=timeout, baudrate=baudrate)
                self.is_physical = True
                print("Connected to Physical RIS.")
            except Exception as e:
                print(f"Physical RIS connection failed: {e}")
                choice = input("Create virtual RIS? [Y/n]: ")
                if choice.lower() == 'y':
                    self.ris = Virtual_RIS(port, id=id, timeout=timeout, baudrate=baudrate)
                    self.is_physical = False
                    print("Virtual RIS created.")
                else:
                    print("Exiting...")
                    exit()
        else:
            self.ris = Virtual_RIS(port, id=id, timeout=timeout, baudrate=baudrate)
            self.is_physical = False
            print("Virtual RIS created.")

    def __getattr__(self, name):
        return getattr(self.ris, name)


        
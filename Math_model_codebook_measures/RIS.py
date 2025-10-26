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
    def __init__(self, port, id = 0, timeout = 10, baudrate = 115200, set_wait_time = None):
        self.ser = serial.Serial(port, baudrate = baudrate, timeout = timeout)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.id = id
        self.timeout = timeout
        self.set_wait_time = set_wait_time
        self.c_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
        self.reset()
        print(f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}")
        return
            
        
    def __repr__(self):
        return f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}"

    def set_pattern(self, pattern):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(bytes(f"!{pattern}\n", 'utf-8'))
        if self.set_wait_time is None:
            start_time = time.time()
            while True:
                response = self.ser.readline().decode('utf-8').strip()
                #print(response)
                if response == "#OK":
                    self.c_pattern = pattern
                    #print(f"Pattern {pattern} set")
                    #return True
                    return time.time() - start_time
                if time.time() - start_time > self.timeout:
                    return False
        else:
            time.sleep(self.set_wait_time)

    
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
    def __init__(self, port, id=0, timeout=10, baudrate=115200, phy_device = True, set_wait_time = None):
        if phy_device:
            try:
                print("Attempting to connect to Physical RIS...")
                self.ris = Physical_RIS(port, id=id, timeout=timeout, baudrate=baudrate, set_wait_time=set_wait_time)
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


if __name__ == "__main__":
    ris = RIS("COM5")
    ris.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
    time.sleep(5)
    ris.set_pattern("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    time.sleep(5)
    ris.set_pattern("0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00")
    time.sleep(5)
    ris.set_pattern("0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF")
    time.sleep(5)
    ris.set_pattern("0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    time.sleep(5)
    ris.set_pattern("0x5555555555555555555555555555555555555555555555555555555555555555")
    time.sleep(5)
    ris.set_pattern("0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000")
    time.sleep(5)
    ris.set_pattern("0x0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF")
    time.sleep(5)
    ris.set_pattern("0xAAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555")
    time.sleep(5)
    ris.set_pattern("0x5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA")
    time.sleep(5)
    ris.set_pattern("0xCCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333")
    time.sleep(5)
    ris.set_pattern("0x000000003FFC3FFC300C300C33CC33CC33CC33CC300C300C3FFC3FFC00000000")
    time.sleep(5)
    ris.set_pattern("0x00007FFE40025FFA500A57EA542A55AA55AA542A57EA500A5FFA40027FFE0000")




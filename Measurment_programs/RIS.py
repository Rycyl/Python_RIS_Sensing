import serial
import time
#import sys
#import os
import numpy as np
#import json
#from enum import Enum
import socket

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

import serial
import socket
import time


class Physical_RIS:
    def __init__(
        self,
        port,
        id=0,
        timeout=10,
        baudrate=115200,
        set_wait_time=None,
        use_socket=False,
        socket_host="192.168.8.10",
        socket_port=5000
    ):
        

        # --- Basic params ---
        self.id = id
        self.timeout = timeout
        self.set_wait_time = set_wait_time
        self.c_pattern = "0x" + "0" * 64
        # --- Socket params ---
        self.use_socket = use_socket
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.sock = None
        if self.use_socket:
            self._connect_socket()
            print("RIS podłączony przez sieć Ethernet")
        else:
            # --- RIS UART ---
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            self.ser.flushInput()
            self.ser.flushOutput()
            self.reset()
            print(f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}")

    # ------------------------------------------------------------------

    def __repr__(self):
        return f"RIS zostal podlaczony do portu {self.ser.port} z id = {self.id}"

    # ------------------------------------------------------------------
    # SOCKET HANDLING
    # ------------------------------------------------------------------

    def _connect_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.socket_host, self.socket_port))
            print(f"Socket connected to {self.socket_host}:{self.socket_port}")
        except socket.error as e:
            print(f"Socket connection error: {e}")
            self.sock = None

    def sent_pattern_via_socket(self, pattern):
        if self.sock is None:
            self._connect_socket()
            if self.sock is None:
                return False

        try:
            message = f"!{pattern}\n"
            self.sock.sendall(message.encode("utf-8"))

            start_time = time.time()
            while True:
                response = self.sock.recv(1024).decode("utf-8").strip()
                if response:
                    return response

                if time.time() - start_time > self.timeout:
                    return False

        except socket.error as e:
            print(f"Socket communication error: {e}")
            self.sock = None
            return False

    # ------------------------------------------------------------------
    # RIS CONTROL
    # ------------------------------------------------------------------

    def set_pattern(self, pattern):
        

        if self.use_socket:
            start_time = time.time()
            response = self.sent_pattern_via_socket(pattern)

            while True:
                if response == "#OK":
                    self.c_pattern = pattern
                    return True

                if time.time() - start_time > self.timeout:
                    return False
        else:
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.write(bytes(f"!{pattern}\n", "utf-8"))

            if self.set_wait_time is None:
                start_time = time.time()
                while True:
                    response = self.ser.readline().decode("utf-8").strip()
                    if response == "#OK":
                        self.c_pattern = pattern
                        return True
                    if time.time() - start_time > self.timeout:
                        return False
            else:
                time.sleep(self.set_wait_time)
                self.c_pattern = pattern
                return self.set_wait_time

    # ------------------------------------------------------------------

    def reset(self):
        try:
            self.ser.write(b"!RESET\n")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------------

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        try:
            if self.ser:
                try:
                    self.ser.close()
                except Exception:
                    pass
        except:
            pass

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

    def __del__(self):
        self.close()
 




class RIS:
    def __init__(self, port, id=0, timeout=10, baudrate=115200, phy_device = True, set_wait_time = None, use_socket=False):
        if phy_device:
            try:
                print("Attempting to connect to Physical RIS...")
                self.ris = Physical_RIS(port, id=id, timeout=timeout, baudrate=baudrate, set_wait_time=set_wait_time, use_socket=use_socket)
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
    ris = RIS("", use_socket=True)
    ris.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
    print("0x0000000000000000000000000000000000000000000000000000000000000000")
    # time.sleep(5)
    ris.set_pattern("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    print("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    # time.sleep(5)
    ris.set_pattern("0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00")
    print("0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00")
    # time.sleep(5)
    ris.set_pattern("0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF")
    print("0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF")
    # time.sleep(5)
    ris.set_pattern("0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # time.sleep(5)
    ris.set_pattern("0x5555555555555555555555555555555555555555555555555555555555555555")
    print("0x5555555555555555555555555555555555555555555555555555555555555555")
    # time.sleep(5)
    ris.set_pattern("0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000")
    print("0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000")
    # time.sleep(5)
    ris.set_pattern("0x0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF")
    print("0x0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF")
    # time.sleep(5)
    ris.set_pattern("0xAAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555")
    print("0xAAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555")
    # time.sleep(5)
    ris.set_pattern("0x5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA")
    print("0x5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA")
    # time.sleep(5)
    ris.set_pattern("0xCCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333")
    print("0xCCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333")
    # time.sleep(5)
    ris.set_pattern("0x000000003FFC3FFC300C300C33CC33CC33CC33CC300C300C3FFC3FFC00000000")
    print("0x000000003FFC3FFC300C300C33CC33CC33CC33CC300C300C3FFC3FFC00000000")
    # time.sleep(5)
    ris.set_pattern("0x00007FFE40025FFA500A57EA542A55AA55AA542A57EA500A5FFA40027FFE0000")
    print("0x00007FFE40025FFA500A57EA542A55AA55AA542A57EA500A5FFA40027FFE0000")




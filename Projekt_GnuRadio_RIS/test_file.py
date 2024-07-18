import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Controller import Controller
import serial.tools.list_ports
from RIS import RIS
from enum import Enum


ris = RIS(port="/dev/ttyUSB0")

for i in serial.tools.list_ports.comports():
    print(i)
    if ris.port == i.device:
        print("port is busy")

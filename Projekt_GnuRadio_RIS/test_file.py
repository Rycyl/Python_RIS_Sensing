import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from Controller import Controller
import serial.tools.list_ports
from RIS import RIS
from enum import Enum

from RIS_patern_dictionary import RIS_pattern_dictionary
from RIS_patern_dictionary import RIS_pattern_names

pattern = RIS_pattern_names.All_elements_turn_off.value
print(pattern)

print(RIS_pattern_dictionary(pattern))
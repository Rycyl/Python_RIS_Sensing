from serial import Serial
import time
import json

try:
    with open ("config.json") as config_f:
       config = json.load(config_f)
       ris_port = config["RIS_PORT"]
       ris_set_time = config["RIS_SET_TIME"]
       ris = Serial(ris_port, 115200)
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()

def reset_RIS():
    ris.write(bytes('!Reset\n', 'utf-8'))
    time.sleep(ris_set_time)
    while ris.in_waiting:
        response = ris.readline().decode('utf-8').rstrip()
        print(f"Response from resetting RIS: {response}")
        time.sleep(0.1)
        
def set_BT_key(key : str):
    ris.write(bytes(f'!BT-Key={key}', 'utf-8'))
    # Wait long enough or check ris.NumBytesAvailable for becoming non-zero
    time.sleep(2)
    response = ris.readline().decode('utf-8').rstrip()
    print(f"Response from setting a new Static Pass Key: {response}")
    
def set_pattern(pattern):
    ris.write(bytes(f"!{pattern}\n", 'utf-8'))
    time.sleep(ris_set_time)
    
def read_EXT_voltage() -> float:
    ris.write(bytes('?Vext\n', 'utf-8'))
    externalVoltage = float(ris.readline().decode('utf-8').rstrip())
    print(f"External supply voltage: {externalVoltage}")
    return externalVoltage

def read_pattern():
    ris.write(bytes('?Pattern\n', 'utf-8'))
    time.sleep(ris_set_time)
    while ris.in_waiting:
        response = ris.readline().decode('utf-8').rstrip()
        print(f"Response from resetting RIS: {response}")
        time.sleep(ris_set_time)
        
            


    
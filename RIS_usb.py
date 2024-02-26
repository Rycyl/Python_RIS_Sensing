from serial import Serial
import time

try:
    with open ("config.json") as config_f:
       ris_port = config_f["RIS_PORT"]
       ris = Serial(ris_port, 115200)
    
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()

def reset_RIS():
    ris.writeline('!Reset')
    time.sleep(1)
    while ris.NumBytesAvailable > 0:
        response = ris.readline().decode('utf-8').rstrip()
        print(f"Response from resetting RIS: {response}")
        time.sleep(0.1)
        
def set_BT_key(key : str):
    ris.writeline(f'!BT-Key={key}')
    # Wait long enough or check ris.NumBytesAvailable for becoming non-zero
    time.sleep(5)
    response = ris.readline().decode('utf-8').rstrip()
    print(f"Response from setting a new Static Pass Key: {response}")
    
def set_pattern(pattern : str):
    ris.writeline(f"!{pattern}")
    currentPattern = ris.readline()
    print(f"Current pattern {currentPattern}");
    
def read_EXT_voltage() -> float:
    ris.writeline('?Vext')
    externalVoltage = float(ris.readline().decode('utf-8').rstrip())
    print(f"External supply voltage: {externalVoltage}")
    return externalVoltage

def read_pattern():
    ris.writeline('?Pattern')
    currentPattern = ris.readline().decode('utf-8').rstrip()
    print(f"Current pattern: {currentPattern}")
    return currentPattern
        
            


    
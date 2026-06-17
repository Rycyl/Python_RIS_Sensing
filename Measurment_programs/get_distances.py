import serial
from numpy import average
import time
import re
import numpy as np

def save_to_file(data_array, file_name):
    with open (file_name, "+a") as f:
        for datum in data_array:
            f.write(datum)
            f.write("\n")
        f.close()

class UWB_module():
    def __init__(self, port = '/dev/ttyACM0', b_rate = 115200, no_of_lines = 100, max_attempts = 500):
        self.uwb_dev = serial.Serial(port, b_rate)
        self.uwb_dev.reset_input_buffer()
        self.uwb_dev.reset_output_buffer()
        #self.uwb_dev.write("deca?") # Nie wiem co to dokładnie robi ale w kodzie źródłowym aplikacji jest
        self.no_of_lines = no_of_lines
        self.max_attempts = max_attempts


    def get_uwb_data(self):
        #self.uwb_dev.reset_input_buffer()
        mc = []
        ma = []
        attempts = 0
        prev_ma_no = "0"
        prev_mc_no = "0"
        while True:
            read = self.uwb_dev.readline().decode('utf-8', errors='ignore').strip()
            read = read.split(" ")
            if read[0]==('mc') and len(mc) < self.no_of_lines and read[-3] != prev_mc_no:
                mc.append(read)
                prev_mc_no = read[-3]
            elif read[0]==('ma') and len(ma) < self.no_of_lines and read[-3] != prev_ma_no:
                ma.append(read)
                prev_ma_no = read[-3]
            attempts += 1
            if (len(mc) == self.no_of_lines and len(ma) == self.no_of_lines):
                break
        return mc, ma
    
    def process_data(self, data):
        ret_data = [[], [], [], []]
        # [RANGE0[], RANGE1[], RANGE2[], RANGE3[]]
        for datum in data:
            for i in range(4):
                ret_data[i].append(int(datum[i+2],16))
        return ret_data
    
    def avg(self, data):
        ret = []
        for datum in data:
            dat = sorted(datum)
            dat = dat[2:-2]
            dat = average(dat)
            ret.append(dat)
        return ret


    def get_distances(self):
        mc, ma = self.get_uwb_data()
        tag_distances_lists, anchor_distances_lists = (self.process_data(mc), self.process_data(ma))
        calc_dist_tag = self.avg(tag_distances_lists)
        calc_dist_anchor = self.avg(anchor_distances_lists)
        return calc_dist_tag, calc_dist_anchor
        
    
class UWB_module_DWM1001():
    def __init__(self, port = '/dev/ttyACM0', b_rate = 115200, timeout = 1):
        '''
        Object to handle connection with UWB MDEK1001 set
        port can be set as needed, default is for linux
        '''
        try:
            t0 = time.time()
            self.uwb_dev = serial.Serial(port, b_rate, timeout=timeout)
            self.uwb_dev.reset_input_buffer()
            self.uwb_dev.reset_output_buffer()
            attempts = 0
            init_attempts = 10  # adjust as needed
            # self.uwb_dev.write(b'les\r')
            while attempts < init_attempts:
                raw = self.uwb_dev.readline()  # returns bytes or b''
                # print(raw)
                if len(raw):
                    print("BREAKING", raw)
                    break
                self.uwb_dev.write(b'les\r')
                attempts += 1
                time.sleep(0.5)

            if attempts >= init_attempts:
                raise RuntimeError(f"No response from device after {init_attempts} attempts")

            print("INIT DONE t=", time.time()-t0)
            self.line = None
        except Exception as e:
            print("!!!!!!Not working properly, see error:")
            print(f"Error:: {e}")
            exit()

    def close_conn(self):
        if self.uwb_dev.is_open:
            self.uwb_dev.write(b'\r')
            self.uwb_dev.close()
            print("Connection to UWB closed")

    def __exit__(self):
            self.close_conn()

    def read_line(self, save_to_file = False, dump_file = 'UWB_dump.txt'):
        """
        Read lines from tag
        """
        max_no_of_lines = 1
        self.line = []
        try:
            line = [] 
            #print("Reading UWB data... (Ctrl+C to stop)")
            while len(line)<50:
                line = self.uwb_dev.readline().decode('utf-8').strip()
                #print(line)
            if save_to_file:
                #print("Line collected, saving to file")
                save_to_file(line, dump_file)
            self.line = line
        except serial.SerialException as e:
            print(f"SERIAL ERROR:: {e}")
    
    def parse_line(self, *device_ids):
        """
        Parses the line containing the message and returns
        the distances of the specified devices.

        Returns:
            *device_distances, tag_loc
        """

        self.read_line()

        distances = {}

        pattern = re.compile(r'([0-9A-F]{4})\[(.*?)\]=([-\d.]+)')

        for match in pattern.finditer(self.line):
            dev_id = match.group(1)
            dist = float(match.group(3))
            distances[dev_id] = dist

        return [distances.get(dev) for dev in device_ids]

if __name__ == "__main__":
    devs = ["9D15", "D599", "0F83", "4F96"]
    uwb = UWB_module_DWM1001()
    while True:
        line = uwb.parse_line(*devs)
        print(line)
    #while(True):
        #print(uwb.parse_line(*devs))

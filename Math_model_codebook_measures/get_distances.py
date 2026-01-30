import serial
from numpy import average
import time

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
        
    
class New_UWB_module():
    def __init__(self, port = 'dev/ttyACM0', b_rate = 115200, timeout = 1):
        try:
            self.uwb_dev = serial.Serial(port, b_rate, timeout)
            self.uwb_dev.reset_input_buffer()
            self.uwb_dev.reset_output_buffer()
        except:
            print("NIE DZIAŁA AAAAAAAAAAAAAAAAAAAAAAAA")
            return
        


    def read_cont(self, save_to_file = False, dump_file = 'UWB_dump.txt'):
        lines_to_save = []
        max_no_of_lines = 1000

        try: 
            self.uwb_dev.write(b'\r\r')
            time.sleep(1)

            self.uwb_dev.write(b'lec\r')

            print("Reading UWB data continuously... (Ctrl+C to stop)")

            while True:
                line = self.uwb_dev.readline().decode('utf-8').strip()

                if line:
                    print("Raw line::")
                    print(line)

                    if save_to_file:
                        lines_to_save.append(line)
                        if len(lines_to_save) >= max_no_of_lines:
                            print("\nMax data collected, Stopping data collection and saveing to file")
                            save_to_file(lines_to_save, dump_file)
                            break
        except serial.SerialException as e:
            print(f"SERIAL ERROR:: {e}")
        except KeyboardInterrupt:
            print(f"\nKeyboardInterrupt, Stopping data collection and saving to {dump_file}")
            save_to_file(lines_to_save, dump_file)
        finally:
            if self.uwb_dev.is_open:
                self.uwb_dev.write(b'\r')
                self.uwb_dev.close()
                print("Connection to UWB closed")
    
if __name__ == "__main__":
    uwb = New_UWB_module()
    uwb.read_cont(save_to_file=True)

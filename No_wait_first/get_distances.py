import serial


class UWB_module():
    def __init__(self, port = '/dev/ttyACM0', b_rate = 115200, no_of_lines = 10, max_attempts = 40):
        self.uwb_dev = serial.Serial(port, b_rate)
        self.uwb_dev.reset_input_buffer()
        self.uwb_dev.reset_output_buffer()
        self.uwb_dev.write("deca?") # Nie wiem co to dokładnie robi ale w kodzie źródłowym aplikacji jest
        self.no_of_lines = no_of_lines
        self.max_attempts = max_attempts


    def get_uwb_data(self):
        #self.uwb_dev.reset_input_buffer()
        mr = []
        ma = []
        attempts = 0
        while True:
            read = self.uwb_dev.readline().decode('utf-8', errors='ignore').strip()
            if read.startswith('mr') and len(mr) < self.no_of_lines:
                mr.append(read)
            elif read.startswith('ma') and len(ma) < self.no_of_lines:
                ma.append(read)
            attempts += 1
            if (len(mr) == self.no_of_lines and len(ma) == self.no_of_lines):
                break
        return mr, ma
    
    def process_data(self, data):
        ret_data = [[], [], [], []]
        # [RANGE0[], RANGE1[], RANGE2[], RANGE3[]]
        for datum in data:
            segmented_datum = datum.split(" ")
            for i in range(4):
                ret_data[i].append(float('0x' + segmented_datum[i+2]))
        return ret_data
    

    def get_distances(self):
        mr, ma = self.get_uwb_data()
        tag_distances_lists, anchor_distances_lists = (self.process_data(mr), self.process_data(ma))
        calc_dist_tag = [sum(sorted(values)[1:-1]) for values in zip(*tag_distances_lists)]
        calc_dist_anchor = [sum(sorted(values)[1:-1]) for values in zip(*anchor_distances_lists)]
        return calc_dist_tag, calc_dist_anchor
        
    

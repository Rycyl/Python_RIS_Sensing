import serial


class UWB_module():
    def __init__(self, port = '/dev/ttyACM0', b_rate = 115200, no_of_lines = 10, max_attempts = 20):
        self.uwb_dev = serial.Serial(port, b_rate)
        self.uwb_dev.reset_input_buffer()
        self.uwb_dev.reset_output_buffer()
        self.uwb_dev.write("deca?") # Nie wiem co to dokładnie robi ale w kodzie źródłowym aplikacji jest
        self.no_of_lines = no_of_lines
        self.max_attempts = max_attempts


    def get_data(self):
        self.uwb_dev.reset_input_buffer()
        lines = []
        attempts = 0
        while len(lines) < self.no_of_lines and attempts < self.max_attempts:
            read = self.uwb_dev.readline().decode('utf-8', errors='ignore').strip()
            if read.startswith("mc"):
                lines.append(read)
            attempts += 1
        return lines

    def get_distances(self):
        lines = self.get_data()
        distances = []
        for line in lines:
            data = line.split(" ")
            data = data[2:6]
            data = [int('0x'+d) for d in data]
            distances.append(data)
        calc_dist = [sum(sorted(values)[1:-1]) for values in zip(*distances)]
        return calc_dist
        
    

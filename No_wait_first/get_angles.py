import serial


class UWB_module():
    def __init__(self, port = '/dev/ttyACM0', b_rate = 115200):
        self.uwb_dev = serial.Serial(port, b_rate)
        self.uwb_dev.reset_input_buffer()
        self.uwb_dev.reset_output_buffer()
        self.uwb_dev.write("deca?") # Nie wiem co to dokładnie robi ale w kodzie źródłowym aplikacji jest


    def get_distances(self, no_of_lines = 10, max_attempts = 20):
        self.uwb_dev.reset_input_buffer()
        lines = []
        attempts = 0
        while len(lines) < no_of_lines and attempts < max_attempts:
            read = self.uwb_dev.readline().decode('utf-8', errors='ignore').strip()
            if read.startswith("mc"):
                lines.append(read)
            attempts += 1
        return lines

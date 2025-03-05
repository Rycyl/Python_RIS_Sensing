from analyzer_sensing import Analyzer
from generator import Generator
from RIS import RIS
from element_by_element import sing_pat_per_run
from config_obj import Config
from file_creator import create_file
import time


if __name__ == "__main__":
    Conf = Config()
    phy_device_input = True

    analyzer = Analyzer(Conf, phy_device_input)
    generator = Generator(Conf, phy_device_input)
    ris = RIS(port='/dev/ttyUSB0', phy_device=phy_device_input)
    print("RIS done")

    meas_file_name = "test"
    code_book_file = "Codebook.csv"

    meas_file = create_file(meas_file_name)
    print("create file done")
    meas_obj = sing_pat_per_run(ris, analyzer, generator, meas_file, code_book_file)
    print("obj done")

    #time.sleep(10) time for evacutation
    meas_obj.start_measure()

    exit()
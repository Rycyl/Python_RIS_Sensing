import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time

try:
    with open ("config_sensing.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        freq = config['CENTRAL_FREQ']
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        swepnt = config["SWEEP_POINTS"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
        detector = config["DETECTOR"]
        sweptime = config["SWEEP_TIME"]
        # More modes will be add later.
        if config["GENERATOR_MODE"] == "CW":
            generator_mode = enums.FreqMode.CW
        else: 
            generator_mode = enums.FreqMode.CW
        config_f.close()
except FileNotFoundError:
    print("File with configuration doesn't exist.")
    exit()

try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
    
def find_best_pattern(bsweptime = sweptime, banalyzer_mode = analyzer_mode, bdetector = detector, bswepnt = swepnt, bgenerator_amplitude = generator_amplitude):
    generator.meas_prep(True, generator_mode, bgenerator_amplitude, freq)
    # power = {}
    power = []
    analyzer_sensing.meas_prep(freq, bsweptime, span, banalyzer_mode, bdetector, revlevel, rbw, bswepnt)
    for pattern in patterns_data:
        RIS_usb.set_pattern(pattern["HEX"])
        p = analyzer_sensing.trace_get()
        power.append(p)
    for i in range(0, len(power)):
        print("pattern id:: ", i, " = ",power[i])
    best_index = power.index(max(power))
    worst_index = power.index(min(power))
    best_pattern = patterns_data[best_index]
    worst_pattern = patterns_data[worst_index]
    print(best_pattern["DESC"], max(power))
    print(worst_pattern["DESC"], min(power))
    return best_pattern, worst_pattern

def time_mesurment(best_pattern, worst_pattern):
    generator.meas_prep(True, generator_mode, -140.0, freq)
    time.sleep(0.1)
    with open(trace_file, 'a+') as file:
        file.write("Noise") 
        file.write(',')
        file.close()  # CLose the file
    analyzer_sensing.meas_prep(freq, sweptime, span, analyzer_mode, detector, revlevel, rbw, swepnt) #tu można wsadzić funkcję która zrobi poziom szumu zamiast poprostu szum ale no
    noise_avre = analyzer_sensing.trace_get_vect_fx()
    RIS_usb.set_pattern(worst_pattern["HEX"])
    with open(trace_file, 'a+') as file:
        file.write(worst_pattern["DESC"]) 
        file.write(',')
        file.close()  # CLose the file
    #analyzer_sensing.meas_prep(freq, sweptime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    generator.meas_prep(True, generator_mode, generator_amplitude, freq)
    time.sleep(0.1)
    pat_1_avre = analyzer_sensing.trace_get_vect_fx()
    RIS_usb.set_pattern(best_pattern["HEX"])
    with open(trace_file, 'a+') as file:
        file.write(best_pattern["DESC"]) 
        file.write(',')
        file.close()  # CLose the file
    #analyzer_sensing.meas_prep(freq, sweptime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    pat_2_avre = analyzer_sensing.trace_get_vect_fx()
    pat1_to_noise = pat_1_avre - noise_avre
    pat_2_to_pat_1 = pat_2_avre - pat_1_avre
    print('Avre_noise = ', noise_avre)
    print('Pat_1_pow_avre = ', pat_1_avre)
    print('Pat_2_pow_avre = ', pat_2_avre)
    return pat1_to_noise, pat_2_to_pat_1
    
if __name__ == "__main__":
    time.sleep(20)
    RIS_usb.reset_RIS()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    flag_1 = 0
    flag_2 = 0
    out_of_range_flag = 0
    best_pattern, worst_pattern = find_best_pattern(bsweptime = 50E-3, banalyzer_mode= "WRITe", bdetector= "SAMP", bgenerator_amplitude= -10 )
    #generator.meas_prep(True, generator_mode, -140.0, freq)
    i = 0
    while(True):
        i+=1
        with open(trace_file, 'a+') as file:
            file.write("pomiar " + str(i) + ",")
            file.write("Gen_pwr,")
            file.write(str(generator_amplitude) + ",")
            file.write(str(time.ctime(time.time()))) 
            file.write('\n')
            file.close()  # CLose the file
        p1_t_n, p2_t_p1 = time_mesurment(best_pattern, worst_pattern)
        if(p1_t_n > 1):
            generator_amplitude -= 2
        elif(p1_t_n < 0.5):
            if(generator_amplitude < -10):
                generator_amplitude += 1
            else:
                print("Can't reach the reciver. Exiting.")
                #break
                time.sleep(30)
        if(p2_t_p1 < 5):
            if(flag_1):
                flag_2 = 1
                out_of_range_flag += 1
            else:
                flag_1 = 1
        else:
            flag_1 = 0
            flag_2 = 0
            out_of_range_flag = 0
        if(flag_1 and flag_2):
            #time.sleep(5)
            best_pattern, worst_pattern = find_best_pattern(bsweptime = 50E-3, banalyzer_mode= "WRITe", bdetector= "SAMP", bgenerator_amplitude= -10 )
        #if(out_of_range_flag > 10):
        #    print("Can't find the best pattern. Exiting.")
            #break
        #    time.sleep(30)

    #print(best_pattern, worst_pattern)
    # generator.meas_prep(True, generator_mode, -135.0, freq)
    # time_mesurment(best_pattern, worst_pattern)
    analyzer_sensing.meas_close()
    generator.meas_close()
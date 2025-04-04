import ast
import time
import pickle
from bitstring import BitArray
import os
import numpy as np

class Result:
    def __init__(self, idx, pattern):
        self.idx = int(idx)  # Index of the result
        self.pattern = BitArray(hex=pattern)  # Bit pattern
        self.powers = []  # List to store power measurements
        self.Tx_Angle = []  # List to store transmission angles
        self.Rx_Angle = []  # List to store reception angles
        self.a_values = []  # List to store values of a
        self.b_values = []  # List to store values of b
        self.c_values = []  # List to store values of c
        self.x_values = []  # List to store values of x
        self.y_values = []  # List to store values of y

    def add_measure(self, power, tx_angle, rx_angle, a, b, c, x, y):
        self.powers.append(float(power))  # Add power measurement
        self.Rx_Angle.append(float(tx_angle))  # Add transmission angle
        self.Tx_Angle.append(float(rx_angle))  # Add reception angle
        self.a_values.append(float(a))  # Add value of a
        self.b_values.append(float(b))  # Add value of b
        self.c_values.append(float(c))  # Add value of c
        self.x_values.append(float(x))  # Add value of x
        self.y_values.append(float(y))  # Add value of y

    def __repr__(self):
        return (f"Result(idx={self.idx}, pattern={self.pattern}, powers={self.powers}, "
                f"Tx_Angle={self.Tx_Angle}, Rx_Angle={self.Rx_Angle}, "
                f"a_values={self.a_values}, b_values={self.b_values}, "
                f"c_values={self.c_values}, x_values={self.x_values}, y_values={self.y_values})")

class Results:
    def __init__(self, dumpfile="results.pkl", resultfilename="Big_codebook_measure"):
        self.results = []
        self.load_results(dumpfile, resultfilename)

    def add_result(self, result):
        if isinstance(result, Result):
            self.results.append(result)
        else:
            raise ValueError("Only objects of type Result can be added.")

    def dump_class_to_file(self, dumpfile):
        # Serializacja obiektu do pliku
        with open(dumpfile, 'wb') as file:
            pickle.dump(self, file)
        print("Results class dumpted to a file: ", dumpfile)

    def calc_angle_distances(self, filename): #np.average(data, axis=1)
        ret = []
        with open(filename, 'r', encoding='utf-8') as file:
            # Wczytaj wszystkie linie z pliku
            lines = file.readlines()
        # Przetwórz każdą linię, dzieląc dane na podstawie znaku ';'
        data = [line.strip().split(';') for line in lines]
        #print(data)
        for line in lines:
            #make a list from file data
            data = line.strip().split(';')
            if data[0] == "N":
                continue     
            #split for idx and pat | the rest                   
            rest_data = data[3:-1]
            for i in range(len(rest_data)):
                rest_data[i] = float(rest_data[i])
            if rest_data not in ret:
                ret.append(rest_data)
        ret_vals = np.average(ret, axis=0)
        return ret_vals

    def load_results(self, dumpfile, resultfilename):
        print("results loading....")
        try:
            with open(dumpfile, 'rb') as file:
                loaded_object = pickle.load(file)
            self.results = loaded_object.results
            print("Results loaded")
        except:
            directory_path = os.path.dirname(os.path.abspath(__file__))
            for filename in os.listdir(directory_path):
                # Sprawdzenie, czy nazwa pliku zaczyna się od "Big_codebook"
                print("checking file:",filename)
                if filename.startswith(resultfilename) and filename.endswith(".csv"):
                    # Pełna ścieżka do pliku
                    file_path = os.path.join(directory_path, filename)
                    # Otwórz wyniki
                    print("Reading: ",file_path)
                    angles_distances = self.calc_angle_distances(file_path)
                    print(angles_distances)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # Wczytaj wszystkie linie z pliku
                        lines = file.readlines()
                    # Przetwórz każdą linię, dzieląc dane na podstawie znaku ';'
                    data = [line.strip().split(';') for line in lines]
                    #print(data)
                    for line in lines:
                        #make a list from file data
                        data = line.strip().split(';')
                        if data[0] == "N":
                            continue     
                        #split for idx and pat | the rest                   
                        core_data = [data[0], data[1]]
                        rest_data = [data[2], *angles_distances]
                        #check if pattern exist in results   
                        result_founded_in_results = False                     
                        for i in range(len(self.results)):
                            if self.results[i].idx == int(data[0]):
                                #only add measure
                                self.results[i].add_measure(*rest_data)
                                result_founded_in_results = True
                                break
                        if not (result_founded_in_results):    
                            #create new Result()
                            result = Result(*core_data)
                            result.add_measure(*rest_data)
                            self.add_result(result=result)
                                
            print("results loaded")
            self.dump_class_to_file(dumpfile)
        return
            
# Create class instance
results_instance = Results()
print(results_instance)
############################################
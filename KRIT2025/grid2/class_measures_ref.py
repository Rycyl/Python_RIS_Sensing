import ast
import time
import pickle
from bitstring import BitArray
import os
import numpy as np

class Result_Ref:
    def __init__(self, idx):
        self.idx = int(idx)  # Index of the result
        #self.pattern = BitArray(hex=pattern)  # Bit pattern
        self.powers = []  # List to store power measurements
        self.Tx_Angle = []  # List to store transmission angles
        self.Rx_Angle = []  # List to store reception angles
        self.a_values = []  # List to store values of a
        self.b_values = []  # List to store values of b
        self.c_values = []  # List to store values of c
        self.x_values = []  # List to store values of x
        self.y_values = []  # List to store values of y

    def __repr__(self):
        return(f"angle_RX {self.Rx_Angle}")


    def add_measure(self, power, tx_angle, rx_angle, a, c, x, y, b):
        self.powers.append(float(power))  # Add power measurement
        self.Rx_Angle.append(float(tx_angle))  # Add transmission angle
        self.Tx_Angle.append(float(rx_angle))  # Add reception angle
        self.a_values.append(float(a))  # Add value of a
        self.b_values.append(float(b))  # Add value of b
        self.c_values.append(float(c))  # Add value of c
        self.x_values.append(float(x))  # Add value of x
        self.y_values.append(float(y))  # Add value of y

    def add_pattern_to_idx(self):
        pass

    def __repr__(self):
        return (f"Result(idx={self.idx}, powers={self.powers}, "
                f"Tx_Angle={self.Tx_Angle}, Rx_Angle={self.Rx_Angle}, "
                f"a_values={self.a_values}, b_values={self.b_values}, "
                f"c_values={self.c_values}, x_values={self.x_values}, y_values={self.y_values})")

class Results_Ref:
    def __init__(self, dumpfile="ref_results.pkl", resultfilename="Ref_power"):
        self.results = []
        self.load_results(dumpfile, resultfilename)

    def sort_by_RX(self):
            # Ensure that all relevant attributes are NumPy arrays
            for result in self.results:
                result.Rx_Angle = np.array(result.Rx_Angle)
                result.Tx_Angle = np.array(result.Tx_Angle)
                result.a_values = np.array(result.a_values)
                result.b_values = np.array(result.b_values)
                result.c_values = np.array(result.c_values)
                result.powers = np.array(result.powers)
                result.x_values = np.array(result.x_values)
                result.y_values = np.array(result.y_values)

            # Now perform the sorting
            sorted_indices = np.argsort(self.results[0].Rx_Angle)
            
            for i in range(len(self.results)):
                self.results[i].Rx_Angle = self.results[i].Rx_Angle[sorted_indices]
                self.results[i].Tx_Angle = self.results[i].Tx_Angle[sorted_indices]
                self.results[i].a_values = self.results[i].a_values[sorted_indices]
                self.results[i].b_values = self.results[i].b_values[sorted_indices]
                self.results[i].c_values = self.results[i].c_values[sorted_indices]
                self.results[i].powers = self.results[i].powers[sorted_indices]
                self.results[i].x_values = self.results[i].x_values[sorted_indices]
                self.results[i].y_values = self.results[i].y_values[sorted_indices]

    def add_result(self, result):
        if isinstance(result, Result_Ref):
            self.results.append(result)
        else:
            raise ValueError("Only objects of type Result can be added.")

    def dump_class_to_file(self, dumpfile):
        # Serializacja obiektu do pliku
        with open(dumpfile, 'wb') as file:
            pickle.dump(self, file)
        print("Results class dumpted to a file: ", dumpfile)


    def load_results(self, dumpfile, resultfilename):
        print("results loading....")
        try:
            print("picle try")
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
                        core_data = [data[0]]
                        rest_data = data[2:-1]
                        #check if pattern exist in results   
                        result_founded_in_results = False
                        if int(data[0]) < 1000:                     
                            for i in range(len(self.results)):
                                if self.results[i].idx == int(data[0]):
                                    #only add measure
                                    self.results[i].add_measure(*rest_data)
                                    result_founded_in_results = True
                                    break
                            if not (result_founded_in_results):    
                                #create new Result()
                                result = Result_Ref(*core_data)
                                result.add_measure(*rest_data)
                                self.add_result(result=result)                
            print("results loaded")
            self.sort_by_RX()
            self.dump_class_to_file(dumpfile)
            print("results dumped to file")
        return
            
# Create class instance
results_instance = Results_Ref()
results_instance.dump_class_to_file("ref_results.pkl")
print(results_instance)
############################################
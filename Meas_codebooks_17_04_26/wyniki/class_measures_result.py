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
        self.d_values = []  # List to store values of d
        self.e_values = []  # List to store values of e
        self.f_values = []  # List to store values of f
        self.trace = []     # List to store whole trace from measurement

    def __repr__(self):
        return(f"angle_RX {self.Rx_Angle}")

    def add_measure(self, power, tx_angle, rx_angle, a,b,c,d,e,f,trace,garbage=None):
        #garbage is usually an empty element on list - artifact of loading .csv with "";"" at the line end
        self.powers.append(float(power))  # Add power measurement
        self.Rx_Angle.append(90-float(rx_angle))  # Add transmission angle
        self.Tx_Angle.append(float(tx_angle))  # Add reception angle
        self.a_values.append(float(a))  # Add value of a
        self.b_values.append(float(b))  # Add value of b
        self.c_values.append(float(c))  # Add value of c
        self.d_values.append(float(d))  # Add value of d
        self.e_values.append(float(e))  # Add value of e
        self.f_values.append(float(f))  # Add value of f
        self.trace.append(trace)

    def add_pattern_to_idx(self):
        pass

    def __repr__(self):
        return (f"Result(idx={self.idx}, powers={self.powers}, "
                f"Tx_Angle={self.Tx_Angle}, Rx_Angle={self.Rx_Angle}, "
                f"a_values={self.a_values}, b_values={self.b_values}, "
                f"c_values={self.c_values}, d_values={self.d_values}, e_values={self.e_values}, f_values={self.f_values})")

class Results:
    def __init__(self, dumpfile="results.pkl", resultfilename=""):
        self.results = []
        self.maxs = []
        self.mins = []
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
            result.d_values = np.array(result.d_values)
            result.e_values = np.array(result.e_values)
            result.f_values = np.array(result.f_values)
            result.trace = np.array(result.trace)

        for min_result in self.mins:
            min_result.Rx_Angle = np.array(min_result.Rx_Angle)
            min_result.Tx_Angle = np.array(min_result.Tx_Angle)
            min_result.a_values = np.array(min_result.a_values)
            min_result.b_values = np.array(min_result.b_values)
            min_result.c_values = np.array(min_result.c_values)
            min_result.powers = np.array(min_result.powers)
            min_result.d_values = np.array(min_result.d_values)
            min_result.e_values = np.array(min_result.e_values)
            min_result.f_values = np.array(min_result.f_values)
            min_result.trace = np.array(min_result.trace)

        for max_result in self.maxs:
            max_result.Rx_Angle = np.array(max_result.Rx_Angle)
            max_result.Tx_Angle = np.array(max_result.Tx_Angle)
            max_result.a_values = np.array(max_result.a_values)
            max_result.b_values = np.array(max_result.b_values)
            max_result.c_values = np.array(max_result.c_values)
            max_result.powers = np.array(max_result.powers)
            max_result.d_values = np.array(max_result.d_values)
            max_result.e_values = np.array(max_result.e_values)
            max_result.f_values = np.array(max_result.f_values)
            max_result.trace = np.array(max_result.trace)
            
        # Now perform the sorting
        sorted_indices = np.argsort(self.results[0].Rx_Angle)

        for i in range(len(self.results)):
            self.results[i].Rx_Angle = self.results[i].Rx_Angle[sorted_indices]
            self.results[i].Tx_Angle = self.results[i].Tx_Angle[sorted_indices]
            self.results[i].a_values = self.results[i].a_values[sorted_indices]
            self.results[i].b_values = self.results[i].b_values[sorted_indices]
            self.results[i].c_values = self.results[i].c_values[sorted_indices]
            self.results[i].powers = self.results[i].powers[sorted_indices]
            self.results[i].d_values = self.results[i].d_values[sorted_indices]
            self.results[i].e_values = self.results[i].e_values[sorted_indices]
            self.results[i].f_values = self.results[i].f_values[sorted_indices]
            self.results[i].trace = self.results[i].trace[sorted_indices]

        for i in range(len(self.mins)):
            self.mins[i].Rx_Angle = self.mins[i].Rx_Angle[sorted_indices]
            self.mins[i].Tx_Angle = self.mins[i].Tx_Angle[sorted_indices]
            self.mins[i].a_values = self.mins[i].a_values[sorted_indices]
            self.mins[i].b_values = self.mins[i].b_values[sorted_indices]
            self.mins[i].c_values = self.mins[i].c_values[sorted_indices]
            self.mins[i].powers = self.mins[i].powers[sorted_indices]
            self.mins[i].d_values = self.mins[i].d_values[sorted_indices]
            self.mins[i].e_values = self.mins[i].e_values[sorted_indices]
            self.mins[i].f_values = self.mins[i].f_values[sorted_indices]
            self.mins[i].trace = self.mins[i].trace[sorted_indices]

        for i in range(len(self.maxs)):
            self.maxs[i].Rx_Angle = self.maxs[i].Rx_Angle[sorted_indices]
            self.maxs[i].Tx_Angle = self.maxs[i].Tx_Angle[sorted_indices]
            self.maxs[i].a_values = self.maxs[i].a_values[sorted_indices]
            self.maxs[i].b_values = self.maxs[i].b_values[sorted_indices]
            self.maxs[i].c_values = self.maxs[i].c_values[sorted_indices]
            self.maxs[i].powers = self.maxs[i].powers[sorted_indices]
            self.maxs[i].d_values = self.maxs[i].d_values[sorted_indices]
            self.maxs[i].e_values = self.maxs[i].e_values[sorted_indices]
            self.maxs[i].f_values = self.maxs[i].f_values[sorted_indices]
            self.maxs[i].trace = self.maxs[i].trace[sorted_indices]

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
            rest_data = data[3:-2]
            for i in range(len(rest_data)):
                rest_data[i] = float(rest_data[i])
            if rest_data not in ret:
                ret.append(rest_data)
        ret_vals = np.average(ret, axis=0)
        return ret_vals

    def load_results(self, dumpfile, resultfilename):
        print("results loading....")
        try:
            print("picle try")
            with open(dumpfile, 'rb') as file:
                loaded_object = pickle.load(file)
            self.results = loaded_object.results
            self.maxs=loaded_object.maxs
            self.mins=loaded_object.mins
            print("Results loaded")
        except:
            directory_path = os.path.dirname(os.path.abspath(__file__))
            for filename in os.listdir(directory_path):
                # Sprawdzenie, czy nazwa pliku zaczyna się od "Big_codebook"
                #print("checking file:",filename)
                if filename.startswith(resultfilename) and filename.endswith(".csv"):
                    # Pełna ścieżka do pliku
                    file_path = os.path.join(directory_path, filename)
                    # Otwórz wyniki
                    print("Reading: ",file_path)
                    #angles_distances = self.calc_angle_distances(file_path)
                    #print(angles_distances)
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
                        rest_data = data[2:]
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
                                result = Result(*core_data)
                                result.add_measure(*rest_data)
                                self.add_result(result=result)
                        elif int(data[0]) >= 1000 and int(data[0]) < 2000:
                            for i in range(len(self.maxs)):
                                if self.maxs[i].idx == int(data[0]):
                                    #only add measure
                                    self.maxs[i].add_measure(*rest_data)
                                    self.maxs[i].add_pattern_to_idx(core_data[1])
                                    result_founded_in_results = True
                                    break
                            if not (result_founded_in_results):    
                                #create new Result()
                                result = Result(*core_data)
                                result.add_measure(*rest_data)
                                self.maxs.append(result)
                        else:
                            for i in range(len(self.mins)):
                                if self.mins[i].idx == int(data[0]):
                                    #only add measure
                                    self.mins[i].add_measure(*rest_data)
                                    self.mins[i].add_pattern_to_idx(core_data[1])
                                    result_founded_in_results = True
                                    break
                            if not (result_founded_in_results):    
                                #create new Result()
                                result = Result(*core_data)
                                result.add_measure(*rest_data)
                                self.mins.append(result)
                            
            self.sort_by_RX()                    
            print("results loaded")
            self.dump_class_to_file(dumpfile)
            print("results dumped to file")
        return

if __name__=="__main__":       
    # Create class instance
    results_instance = Results()
    results_instance.dump_class_to_file("results.pkl")
    #print(results_instance)
    ############################################
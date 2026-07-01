import ast
import time
import pickle
from bitstring import BitArray
import os
import numpy as np

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW

def mw_to_dbm(x):
    dbm=10*np.log10(x)
    return dbm

def linear_mean(x):
    ret_val = dbm_to_mw(x)
    ret_val = np.mean(ret_val)
    ret_val = mw_to_dbm(ret_val)
    return ret_val


class Trace:
    def __init__(self, trace):
        self.trace = np.array(trace)
  
    # def get_truncaded_trace(self, start=224, stop=1824, step=2): #return trace without noise carriers at the sides
    #     return self.trace[start:stop:step]

    def get_truncaded_trace(self, start=224, stop=1824, step=2, middle=1024):
        indices = np.arange(start, stop, step)
        mask = (indices != middle-1) & (indices != middle)
        return self.trace[indices[mask]]

    def get_carriers_by_idx(self, idx):
        #idx is a list of indexes
        t = self.get_truncaded_trace()
        return t[idx]

    def get_mean(self, start=None, stop=None, step=None):
        if start and stop and step:
            temp = self.get_truncaded_trace(start, stop, step)
        else:
            temp = self.get_truncaded_trace()
        return(np.mean(temp))

    def get_max(self, start=None, stop=None, step=None):
        if start and stop and step:
            temp = self.get_truncaded_trace(start, stop, step)
        else:
            temp = self.get_truncaded_trace()
        return(np.max(temp)) 

    def get_min(self, start=None, stop=None, step=None):
        if start and stop and step:
            temp = self.get_truncaded_trace(start, stop, step)
        else:
            temp = self.get_truncaded_trace()
        return(np.min(temp)) 

    def get_mean_by_idx(self, idx, start=None, stop=None, step=None):
        #idx is a list of indexes
        if start and stop and step:
            temp = self.get_truncaded_trace(start, stop, step)
        else:
            temp = self.get_truncaded_trace()
        temp = temp[idx]
        return(np.mean(temp))

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
        self.traces = []    # List to store whole traces from measurement

    def __repr__(self):
        return(f"angle_RX {self.Rx_Angle}")
     
    def get_truncaded_traces(self): #return traces without noise carriers at the sides
        truncaded_traces = np.array()
        for trace in self.traces:
            np.append(truncaded_traces, trace[224:1824:2])
        return truncaded_traces

    def get_rx_pos_in_xy(self):
        y = np.cos(np.deg2rad(self.Rx_Angle)) * self.c_values
        x = np.sin(np.deg2rad(self.Rx_Angle)) * self.c_values
        for i in range (len(x)):
            with np.printoptions(precision=1, suppress=True):
                print("POS ", i)
                print(x[i],y[i],[self.Rx_Angle[i]])
        # input()
        return x, y

    # def trace_mean_idx(self, idxs=None):
    #     if idxs == None:
    #         input("WARNING, none idxs given to do trace mean, press anything to continue")
    #     truncaded_traces = self.truncade_traces()
    #     means = [np.mean(trace[10:20]) for trace in truncaded_traces]
    #     return np.array(means)

    def add_measure(self, power, tx_angle, rx_angle, a,b,c,d,e,f,traces,garbage=None,garbage2=None):
        #garbage is usually an empty element on list - artifact of loading .csv with "";"" at the line end
        self.powers.append(float(power))  # Add power measurement
        self.Rx_Angle.append(float(rx_angle))  # Add transmission angle
        self.Tx_Angle.append(float(tx_angle))  # Add reception angle
        self.a_values.append(float(a))  # Add value of a
        self.b_values.append(float(b))  # Add value of b
        self.c_values.append(float(c))  # Add value of c
        self.d_values.append(float(d))  # Add value of d
        self.e_values.append(float(e))  # Add value of e
        self.f_values.append(float(f))  # Add value of f
        arr = np.fromstring(traces.strip('[]'), sep=',').astype(np.float32)
        self.traces.append(Trace(arr))

    def add_pattern_to_idx(self):
        pass

    def __repr__(self):
        return (f"Result(idx={self.idx}, powers={self.powers}, "
                f"Tx_Angle={self.Tx_Angle}, Rx_Angle={self.Rx_Angle}, "
                f"a_values={self.a_values}, b_values={self.b_values}, "
                f"c_values={self.c_values}, d_values={self.d_values}, e_values={self.e_values}, f_values={self.f_values})")

class Results:
    def __init__(self, dumpfile="results.pkl", resultfilename="", load_results=True, directory_path=None, dump=False):
        self.results = []
        self.maxs = []
        self.mins = []
        self.dump=dump
        if load_results:
            self.load_results(dumpfile, resultfilename, directory_path)

    def get_maxs_list_for_RX(self, Rx_Angle):
        ret_results = []
        for res in self.maxs:
            if res.Rx_Angle[0] == Rx_Angle:
                ret_results.append(res)
        return ret_results

    def get_max_for_RX(self, Rx_Angle):
        max_list = self.get_maxs_list_for_RX(Rx_Angle=Rx_Angle)
        maxsy = []
        for m in max_list:
            maxsy.append(m.traces[0].get_mean_by_idx(list(range(10,21))))
        return np.max(maxsy)

    def sort_by_RX(self):
        if not self.results:
            return

        ref = self.results[0] # Ref Result object
        ref.c_values = np.array(ref.c_values) # c_values is? numpy array
        # get sorting order by c
        sorted_indices = np.argsort(ref.c_values, kind="stable")

        def get_sortable_attrs(result, expected_len):
            """
            retrieves the attributes of the Result object that:
            - are not private,
            - are not methods,
            - can be converted to numpy arrays,
            - are the same length as c_values.
            """
            sortable_attrs = []

            for attr_name, attr_value in vars(result).items():
                # omit private
                if attr_name.startswith("_"):
                    continue

                # omit callable (methods)
                if callable(attr_value):
                    continue

                try:
                    arr = np.array(attr_value)
                    if len(arr) == expected_len:
                        sortable_attrs.append(attr_name)

                except TypeError:
                    continue

            return sortable_attrs

        def sort_result(result, sorted_indices):
            expected_len = len(sorted_indices)
            attrs = get_sortable_attrs(result, expected_len)

            for attr in attrs:
                values = np.array(getattr(result, attr))
                setattr(result, attr, values[sorted_indices])

        # Sortowanie results
        for result in self.results:
            sort_result(result, sorted_indices)

        # Sortowanie mins, jeśli mają zgodne długości
        for min_result in self.mins:
            sort_result(min_result, sorted_indices)

        # Sortowanie maxs, jeśli mają zgodne długości
        for max_result in self.maxs:
            sort_result(max_result, sorted_indices)

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

    def load_results(self, dumpfile, resultfilename, directory_path=None):
        print("results loading....")
        try:
            self.load_picle_results(dumpfile)
        except Exception as e:
            print("STATUS of PICLE is NEGATIVE")
            print("Error:", repr(e))
            print("Loading CSVs")
            decision = input("load .CSVs? (y/n)")
            if decision == 'y':
                self.load_csv_results(resultfilename,directory_path)
            else:
                exit()
        self.sort_by_RX()                    
        print("results loaded")
        if self.dump:
            self.dump_class_to_file(dumpfile)
            print("results dumped to file")

    def load_picle_results(self, dumpfile):
        print("picle try")
        with open(dumpfile, 'rb') as file:
            loaded_object = pickle.load(file)
            print("Picle loaded")
        self.results = loaded_object.results
        self.maxs=loaded_object.maxs
        self.mins=loaded_object.mins
        print("Results loaded")
    
    def load_csv_results(self, resultfilename,directory_path):
        print("pickle failed")
        if directory_path == None:
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
                    if int(data[0]) < 100000:                     
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
                    elif int(data[0]) < 200000 and int(data[0]) >= 100000:
                        for i in range(len(self.maxs)):
                            if self.maxs[i].idx == int(data[0]):
                                #only add measure
                                self.maxs[i].add_measure(*rest_data)
                                #self.mins[i].add_pattern_to_idx(core_data[1])
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
                                #self.maxs[i].add_pattern_to_idx(core_data[1])
                                result_founded_in_results = True
                                break
                        if not (result_founded_in_results):    
                            #create new Result()
                            result = Result(*core_data)
                            result.add_measure(*rest_data)
                            self.mins.append(result)
        return


    
    def get_traces_by_rx(self, res=None):
        """
        Grupowanie po (RX_angle, c_value)

        Zwraca:
        grouped_traces: [group_index, trace_index, subcarrier_index]
        keys: [(rx, c_value), ...]
        """
        if res is None:
            res = self.results

        rx_map = {}

        for result in res:
            for i in range(len(result.Rx_Angle)):
                rx = int(result.Rx_Angle[i], )  # stabilizacja floata
                c_val = result.c_values[i]

                key = (rx, c_val)  

                trace = result.traces[i].get_truncaded_trace()

                if key not in rx_map:
                    rx_map[key] = []
                rx_map[key].append(trace)

        # sortowanie po rx, potem po c_value
        sorted_keys = sorted(rx_map.keys(), key=lambda x: (x[0], x[1]))

        grouped_traces = [np.array(rx_map[key]) for key in sorted_keys]

        return np.array(grouped_traces), np.array(sorted_keys, dtype=object)


    def get_minimums_by_rx(self):
        """
        calculates trace of minimum power for each localisation
        return: mins, RX_angles
        """
        rx_traces = self.get_traces_by_rx()
        mins = np.min(rx_traces[0], axis=1)
        return mins, rx_traces[1]
    
    def get_maximums_by_rx(self):
        """
        calculates trace of maximum power for each localisation
        return: maxs, RX_angles
        """
        rx_traces = self.get_traces_by_rx()
        maxs = np.max(rx_traces[0], axis=1)
        return maxs, rx_traces[1]

    def get_means_by_rx(self):
        """
        calculates mean traces for each localisation
        return: maxs, RX_angles
        """
        rx_traces = self.get_traces_by_rx()
        traces = dbm_to_mw(rx_traces[0])
        means = np.mean(traces, axis=1)
        means = mw_to_dbm(means)
        return means, rx_traces[1]

    def get_means_for_patterns_by_rx(self):
        """ 
        calculates mean value of traces for each pattern for each localisation
        return: maxs, RX_angles
        """
        rx_traces = self.get_traces_by_rx()
        rx_traces = dbm_to_mw(rx_traces[0])
        means = np.mean(rx_traces, axis=2)
        means = mw_to_dbm(means)
        return means, rx_traces[1]

    def get_maxs_from_maxs_by_rx(self):
        rx_traces = self.get_traces_by_rx(self.maxs)
        maxs = np.max(rx_traces[0], axis=1)
        #maxs = np.max(maxs, axis=1)
        return maxs, rx_traces[1]

    def get_mins_from_mins_by_rx(self):
        rx_traces = self.get_traces_by_rx(self.mins)
        maxs = np.min(rx_traces[0], axis=1)
        #maxs = np.min(maxs, axis=1)
        return maxs, rx_traces[1]

    def get_linear_avg_by_rx(self):
        rx_traces = self.get_traces_by_rx()
        traces = dbm_to_mw(rx_traces[0])
        means = np.mean(traces, axis=1)
        means = mw_to_dbm(means)
        return means, rx_traces[1]

if __name__=="__main__":       
    # Create class instance
    results_instance = Results(resultfilename="All_measurements_merged.csv")
    results_instance.dump_class_to_file("results.pkl")
    pass
    # testb = results_instance.get_linear_avg_by_rx()
    pass
    pass
    #print(results_instance)
    ############################################
import random
import csv

def read_all_SWT(self): #czyta wszystkie swt z pliku z tracami Virt_anal_trace_data.csv
    SWTs = []
    return SWTs #tablica wszystkich swt z pliku

class Traces:
    def __init__(self, SWT=1.1):
        self.SWT = SWT  # Initialize SWT with a default value of 1.1
        self.Trace_list = []  # Initialize an empty list of traces
        self.load_traces("Virt_anal_trace_data.csv")

    def add_trace(self, trace):
        """Add a new trace (list) to the Trace_list."""
        if isinstance(trace, list):
            self.Trace_list.append(trace)
        else:
            raise ValueError("Trace must be a list.")

    def return_trace(self):
        n = random.randint(0, len(self.Trace_list)-1)
        return self.Trace_list[n]

    def load_traces(self, trace_file_name):
        with open(trace_file_name, 'r') as f:
            trace_reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC, quotechar= '|')
            found_swt = False
            for row in trace_reader:
                if found_swt and row[0] == 'SWT':
                    break
                elif row[0] == 'SWT' and row[1] == self.SWT:
                    found_swt = True
                    continue
                if found_swt:
                    self.add_trace(row)
        return 1



# Example usage:
if __name__ == "__main__":
    traces = Traces(SWT=1.1)
    print(traces.return_trace())
    

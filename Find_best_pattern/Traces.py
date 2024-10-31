import random


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
        n = random.randint(len(trace))
        return trace[n]

    def load_traces(trace_file_name):
        

# Example usage:
if __name__ == "__main__":
    traces = Traces(SWT=5)
    

"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import requests
#import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, no_of_samples = 1000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[]
            
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.no_of_samples = no_of_samples
        self.samples = np.zeros(no_of_samples, dtype = np.complex64)
        self.itr = 0
        self.avr_power = 0 #mozna zamienic na wektor i dopisywac nowe wartosci do niego
        
    def calc_power(self):
        po = 0
        for s in self.samples:
            mag = np.abs(s)
            #print(mag)
            po += np.square(mag)
        power = np.sqrt(po/self.no_of_samples)
        #power = 10*np.log10(power/10e-3)
        self.itr = 0
        self.samples = np.zeros(self.no_of_samples, dtype = np.complex64)
        return power
        
    def send_power(self):
        url = "http://192.168.8.184:8000/receive"
        data = {"source": "Rx","power": self.avr_power}
        r = requests.post(url, json=data)
    
    def work(self, input_items, output_items):
        #print(input_items[0].shape)
        for i in range(input_items[0].shape[0]):
            self.samples[self.itr] = input_items[0][i]
            self.itr += 1
            if(self.itr == self.no_of_samples):
               self.avr_power = self.calc_power()
               #print(self.avr_power)
        
        return 0 #len(output_items[0])

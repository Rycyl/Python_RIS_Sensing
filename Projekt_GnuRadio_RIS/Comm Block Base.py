"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import requests

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, C_freq = 5e9, samp_rate = 5e6, ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Send status', # will show up in GRC
            in_sig=[],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.C_freq = C_freq
        self.samp_rate = samp_rate

    def status(self):
        url = "http://192.168.8.184:8000/receive"
        data = {"source": "Rx","status": "Is working", "Reciving at": self.C_freq, "Sample Rate": self.samp_rate}
        r = requests.post(url, json=data)

    def work(self, input_items, output_items):#, input_items, output_items):
        return 1

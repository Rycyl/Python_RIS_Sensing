import time
from bitstring import BitArray

def load_code_book(codebook):
    codes = []
    with open(codebook, "r") as f:
        lines = f.readlines()
        for line in lines:
            codes.append(BitArray(hex=line))
        f.close()
    return codes

code_book = "Codebook.csv"

print(load_code_book(codebook=code_book))
import ast
import time
import pickle
from bitstring import BitArray

class Pattern:
    def __init__(self, idx, pattern, angles):
        self.idx = int(idx)
        self.pattern = BitArray(hex=pattern)
        self.angles = angles

    def __repr__(self):
        return f"Pattern(number={self.idx}, pat='{self.pattern}', angle={self.angles[0]}, total pattern angles: {len(self.angles)}"

class Codebook:
    def __init__(self, dumpfile="codebook.pkl", filename="Codebook.csv"):
        self.patterns = []
        self.load_codebook(dumpfile, filename)

    def add_pattern(self, pattern):
        if isinstance(pattern, Pattern):
            self.patterns.append(pattern)
        else:
            raise ValueError("Only objects of type Pattern can be added.")

    def dump_class_to_file(self, dumpfile):
        # Serializacja obiektu do pliku
        with open(dumpfile, 'wb') as file:
            pickle.dump(self, file)
        print("Codebook class dumpted to a file: ", dumpfile)

    def load_codebook(self, dumpfile, filename):
        print("codebook loading....")
        try:
            with open(dumpfile, 'rb') as file:
                loaded_object = pickle.load(file)
            self.patterns = loaded_object.patterns
            print("codebook loaded")
        except:
            # Otwórz codebook
            with open(filename, 'r', encoding='utf-8') as file:
                # Wczytaj wszystkie linie z pliku
                lines = file.readlines()
            # Przetwórz każdą linię, dzieląc dane na podstawie znaku ';'
            data = [line.strip().split(';') for line in lines]
            for line in lines:
                data = line.strip().split(';')
                angles = ast.literal_eval(data[2]) #zamien str z katami na liste
                pattern = Pattern(idx=data[0], pattern=data[1], angles=angles)
                self.add_pattern(pattern)
            print("codebook loaded")
            self.dump_class_to_file(dumpfile)
        return
            
# Create class instance and load the data
# codebook_instance  = Codebook()
# i = 0
# for x in codebook_instance.patterns:
#     for angle in x.angles:
#         if (angle[0]==-49):
#             i+=1
#             break
# print(i)
# print(codebook_instance.patterns[1])
# print(len(codebook_instance.patterns))

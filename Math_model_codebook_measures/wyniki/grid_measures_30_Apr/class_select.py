from class_codebook import *
from class_measures_result import *

def load_results_from_file(selected, I = -49, PHI_S_STEP = 1):
    results = Results()
    codebook = Codebook()
    print("source data loaded")
    currtent_pattern = None

    selected = Selected(PHI_S_STEP)
    i = I
    phi_s = []
    s = 0
    while s<360:
        phi_s.append(s)
        s+= PHI_S_STEP 
    
    for d in range(0, 90):
        phi_s_found = False
        used_patterns = [0] * 919
        print("D=", d)
        selected.selected.append(Select(i,d))
        for x in codebook.patterns:
            if used_patterns[x.idx] != 1:
                for a in x.angles:
                    if used_patterns[x.idx] == 1:
                        break
                    if (a[0] == i and a[1] == d and a[2] in phi_s):
                        selected.selected[-1].add_pat_idx(a[2], x.idx,  results.results[x.idx].powers)
                        used_patterns[x.idx] = 1
                
            else:
                continue         
    # selected.dump_class_to_file(dumpfile=dumpfile)
    return selected

class Selected:
    def __init__(self, phi_s_step):
        self.selected = []
        self.phi_s_step = phi_s_step

    def dump_class_to_file(self, dumpfile):
        # Serializacja obiektu do pliku
        with open(dumpfile, 'wb') as file:
            pickle.dump(self, file)
        print("Results class dumpted to a file: ", dumpfile)

    def load_from_file(self, dumpfile):
        try:
            with open(dumpfile, 'rb') as file:
                loaded_object = pickle.load(file)
            self.selected = loaded_object.selected
            print("pikle loaded")
        except:
            print("error while pikle loading")
            pass

class Select:
    def __init__(self,i,d):
        self.i = i
        self.d = d
        self.s = []
        self.pat_idx = []
        self.powers = []
        self.maxs = []
        self.maxs_idx = []

    def add_pat_idx(self, s, idx, pows):
        self.s.append(s)
        self.pat_idx.append(idx)
        self.powers.append(pows)

    def show(self):
        print("i = ", self.i, " d = ", self.d)
        for j in range(len(self.s)):
            print(f"For shift = {self.s[j]}, pat_idx = {self.pat_idx[j]}")
    
    def show_pows(self):
        print("i = ", self.i, " d = ", self.d, "len = ", len(self.powers))
        for x in self.powers:
            print([f"{value:.3f}" for value in x])
    
    def find_max(self):
        if self.powers != []:
            array = np.array(self.powers)
            max_values = np.max(array, axis=0)
            max_indices = np.argmax(array, axis=0)
            for l in range(len(max_indices)):
                max_indices[l] = self.pat_idx[max_indices[l]]
            self.maxs  = (max_values)
            self.maxs_idx = (max_indices)
        return
        

if __name__=="__main__":
    dumpfile_base = "wybrane_paterny_pk_metod_s_step_"
    
    #selected.load_from_file(dumpfile)
    PHI_S_STEPS = [1,30,45,90,180,360]
    for phi_s in PHI_S_STEPS:
        print("S", phi_s)
        selected = Selected(PHI_S_STEPS)
        selected = load_results_from_file(selected, PHI_S_STEP=phi_s)
        for s in selected.selected:
           s.find_max()
        dumpfile = dumpfile_base + str(phi_s) + ".pkl"
        selected.dump_class_to_file(dumpfile=dumpfile)
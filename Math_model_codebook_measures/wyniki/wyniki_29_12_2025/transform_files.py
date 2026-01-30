import os
import ast
import numpy as np
from class_measures_result import Results
from power_in_position_teams_rework import power_in_position
from pattern_characteristic import pattern_characteristic
from hamming import hamming_plot




def transform_files():
    dir = os.getcwd()
    files_in_dir = os.listdir(dir)
    useful_files = [file for file in files_in_dir if  "29_Dec_2025" in file and file.endswith(".csv") and not "Edited" in file]

    for file in useful_files:
        exit_file_mean = "Edited_mean_" + file
        exit_file_spec = "Edited_spec_" + file
        with open(file, "r") as f:
            lines = f.readlines()
            f.close()
        with open(exit_file_mean, "w+") as efm:
            with open(exit_file_spec, "w+") as efs:
                header = lines.pop(0)
                efm.write(header)
                efs.write(header)
                for line in lines:
                    splited_line = line.split(";")
                    trace = splited_line[2]
                    trace = ast.literal_eval(trace)
                    trunced_trace = trace[224:1824:2]
                    lin_trace = [10**(x/10) for x in trunced_trace]
                    Power = np.mean(lin_trace)
                    Specific_values = np.mean(lin_trace[10:20])
                    Power = 10*np.log10(Power)
                    Specific_values = 10*np.log10(Specific_values)
                    efm.write(f"{splited_line[0]}; {splited_line[1]}; {Power}; {splited_line[3]}; {splited_line[4]}; {splited_line[5]}; {splited_line[6]}; {splited_line[7]}; {splited_line[8]}; {splited_line[9]};")
                    efm.write("\n")
                    efs.write(f"{splited_line[0]}; {splited_line[1]}; {Specific_values}; {splited_line[3]}; {splited_line[4]}; {splited_line[5]}; {splited_line[6]}; {splited_line[7]}; {splited_line[8]}; {splited_line[9]};")
                    efs.write("\n")
                efm.close()
                efs.close()
        print(f"File {file} done!!")
    print("All done :)")

def crate_results(file_name_pattern):
    typ = type(file_name_pattern)
    if typ == str:
        dumpfile = file_name_pattern + ".pkl"
        res = Results(dumpfile, file_name_pattern)
        return res
    elif typ == list:
        for file in file_name_pattern:
            dumpfile = file + ".pkl"
            res = Results(dumpfile, file)
            return res

def load_patts_with_rotation_pk():
    file = "NEW_PK_codebook.csv"
    list_of_azimuths = []
    prev_azimuth = None
    Temp = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.split(";")
            if prev_azimuth is None or prev_azimuth != data[-1]:
                if len(Temp):
                    list_of_azimuths.append(Temp)
                Temp = []
                Temp.append(data[1])
                prev_azimuth = data[-1]
            else:
                Temp.append(data[1])
        list_of_azimuths.append(Temp)
        f.close()
    return list_of_azimuths



            
if __name__ == "__main__":
    l = load_patts_with_rotation_pk()
    for x in l:
        for y in x:
            print(y)
        print("##############################")
    # file_patern = ["Edited_mean_Mesure_Eu_16_29_Dec_2025", "Edited_mean_Mesure_Eu_16_f_64_29_Dec_2025", "Edited_mean_Mesure_Eu_64_29_Dec_2025", "Edited_mean_Mesure_PK_29_Dec_2025", "Edited_spec_Mesure_Eu_16_29_Dec_2025", "Edited_spec_Mesure_Eu_16_f_64_29_Dec_2025", "Edited_spec_Mesure_Eu_64_29_Dec_2025", "Edited_spec_Mesure_PK_29_Dec_2025"]
    # #result_list = crate_results(file_name_pattern=file_patern)
    # for file in file_patern:
    #     print(file)
    #     results = crate_results(file)
    #     power_in_position(results, file)
    #     pattern_characteristic(results, file)
    #     hamming_plot(results, file)

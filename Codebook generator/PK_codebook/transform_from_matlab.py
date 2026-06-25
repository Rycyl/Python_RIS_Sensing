from bitstring import BitArray

file_name = 'Arranged_codebook.csv'
exit_file = 'Arranged_codebook_test.csv'

i = 0

lines_to_write = []

with open(file_name, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line_list = line.split(';')
        pattern = line_list[0]
        meta_data = line_list[1]
        bit_pattern = BitArray('0b'+pattern)
        exit_line = f"{i};{bit_pattern.hex};{meta_data}"
        i += 1 #increment pat id
        lines_to_write.append(exit_line)
    f.close()

with open(exit_file, 'w+') as f:
    f.writelines(lines_to_write)
    f.close()



# lines_to_write = []
# i = 0
# with open(file_name, 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line_list = line.split(";")
#         pattern = line_list[0]
#         Tx_angles = line_list[1]
#         Rx_angles = line_list[2]
#         Phases = line_list[3]
#         bit_array_pattern = BitArray('0b'+pattern)
#         if Tx_angles.startswith("["):
#             Tx_angles = Tx_angles[1:-1]
#         Tx_angles = Tx_angles.split()
#         Tx_angles_list = [int(angle) for angle in Tx_angles]
#         if Rx_angles.startswith('['):
#             Rx_angles = Rx_angles[1:-1]
#         Rx_angles = Rx_angles.split()
#         Rx_angles_list = [int(angle) for angle in Rx_angles]
#         if Phases.startswith('['):
#             Phases = Phases[1:-2]
#         Phases = Phases.split()
#         Phases_list = [int(phase) for phase in Phases]
#         exit_line = [i, bit_array_pattern, Tx_angles_list, Rx_angles_list, Phases_list]
#         i += 1
#         lines_to_write.append(exit_line)
#     f.close()

# with open(exit_file, 'w+') as f:
#     for l in lines_to_write:
#         f.write(f"{l[0]};{l[1]};{l[2]};{l[3]};{l[4]}\n")
#     f.close()
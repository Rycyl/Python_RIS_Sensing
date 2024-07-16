def file_write_single_power(iteration, pattern, power):
    with open(trace_file, 'a+') as file:
        file.write("pomiar " + str(iteration) + ",")
        file.write(str(time.ctime(time.time())) + ",")
        file.write("Pattern,")
        file.write("0x" + pattern)
        file.write("Rec_PWR,")
        file.write(str(power) + ",")
        file.write('\n')
        file.close()  # CLose the file

def file_write_trace_power(iteration, pattern, power):
    with open(trace_file, 'a+') as file:
        file.write("pomiar " + str(iteration) + ",")
        file.write(str(time.ctime(time.time())) + ",")
        file.write("Pattern,")
        file.write("0x" + pattern)
        file.write("Rec_PWR,")
        for x in power:
            file.write(str(x) + ",")
        file.write('\n')
        file.close()  # CLose the file
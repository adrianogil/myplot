import sys
from dateutil.parser import parse
import matplotlib.pyplot as plt
import pylab
import subprocess

def plot_data(data, suffix, stats_plot_folder, plot_name):
    xs = []
    ys = []

    xs_data = ""
    ys_data = ""

    initial_time = data[0]['time']

    last_value = -10000

    for p in data:

        x_value = (p['time'] - initial_time).total_seconds()
        xs.append(x_value)
        if xs_data == "":
            xs_data = str(x_value)
        else:
            xs_data = xs_data + ", " + str(x_value)

        avg_value = p['value'];
        ys.append(avg_value)
        if ys_data == "":
            ys_data = str(avg_value)
        else:
            ys_data = ys_data + ", " + str(avg_value)


    placeholder_data = {}
    placeholder_data["PLACEHOLDER_NAME" + suffix] = plot_name
    placeholder_data["PLACEHOLDER_X_DATA" + suffix] = xs_data
    placeholder_data["PLACEHOLDER_Y_DATA" + suffix] = ys_data
    placeholder_data["PLACEHOLDER_PLOT_TITLE"] = "Packet Size (bytes)"

    index_path = stats_plot_folder + "/index.html"
    index_lines = []

    with open(index_path, 'r') as f:
        index_lines = f.readlines()

    for i in range(0, len(index_lines)):
        for d in placeholder_data:
            if index_lines[i].find(d) != -1:
                index_lines[i] = index_lines[i].replace(d, placeholder_data[d])

    with open(index_path, 'w') as f:
        for l in index_lines:
            f.write(l)

def filter_log(source_log, stats_plot_folder):
    with open(source_log) as f:
        lines = f.readlines()

    battery_level_data = []
    battery_temp_data = []
    net_buffer_size = []
    net_buffer_size_acc = []

    net_buffer_size_acc_value = 0.0

    current_time = ""

    for line in lines:

        if line.find("JLog: Buffer Size: ") != -1:
            for i in range(7, len(line)):
                if line[i-7:i] == "I Unity":
                    current_time = parse(line[:18].strip())
                elif line > 19 and line[i-19:i] == "JLog: Buffer Size: ":
                    buffer_size_value = float(line[i:].strip())
                    if buffer_size_value != 0:
                        net_buffer_size.append({"time" : current_time, "value" : buffer_size_value})
                        net_buffer_size_acc_value = net_buffer_size_acc_value + buffer_size_value
                        net_buffer_size_acc.append({"time" : current_time, "value" : net_buffer_size_acc_value})
        # if line.find("JLog: Bat Level: ") != -1:
        #     for i in range(7, len(line)):
        #         if line[i-7:i] == "I Unity":
        #             current_time = parse(line[:18].strip())
        #         elif line > 17 and line[i-17:i] == "JLog: Bat Level: ":
        #             battery_level_data.append({"time" : current_time, "value" : 100.0*float(line[i:].strip())})
        # elif line.find("JLog: Bat Temp: ") != -1:
        #     for i in range(7, len(line)):
        #         if line[i-7:i] == "I Unity":
        #             current_time = parse(line[:18].strip())
        #         elif line > 16 and line[i-16:i] == "JLog: Bat Temp: ":
        #             battery_temp_data.append({"time" : current_time, "value" : float(line[i:].strip())})

    # plot_data(battery_level_data, "_1", stats_plot_folder, "'Battery Level'")
    # plot_data(battery_temp_data, "_2", stats_plot_folder, "'Battery Temperature'")
    plot_data(net_buffer_size, "_1", stats_plot_folder, "'Buffer Size'")
    # plot_data(net_buffer_size_acc, "_2", stats_plot_folder, "'Buffer Size Acc'")

    index_path = stats_plot_folder + "/index.html"
    open_index_cmd = "open " + index_path
    subprocess.check_output(open_index_cmd, shell=True)


filter_log(sys.argv[1], sys.argv[2])
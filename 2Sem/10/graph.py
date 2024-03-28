import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LinearLocator

def create_graph_paper(xcells, ycells):
    Fig = plt.figure(figsize=(fig_width*fig_scale, fig_height*fig_scale))
    Ax = Fig.add_subplot()

    Ax.xaxis.set_major_locator(MaxNLocator(xcells))
    Ax.yaxis.set_major_locator(MaxNLocator(ycells))
    Ax.xaxis.set_minor_locator(LinearLocator(xcells*10))
    Ax.yaxis.set_minor_locator(LinearLocator(ycells*10))
    Ax.set_xticks([i for i in range(xcells)])
    Ax.set_yticks([i for i in range(ycells)])

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    return Fig, Ax


all_files = [["silicon_forward.csv", "silicon_reverse.csv"],
             ["germanium_forward.csv", "germanium_reverse.csv"]]
fig_scale = 1.3
fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
plot_width = 28; plot_height = 20 # Size of graph paper in cm
xoffset = int(plot_width / 2)
yoffset = int(plot_height / 2)

U_r = []; I_r = []
U_f = []; I_f = []


for pair in all_files:
    forward = open(pair[0], "r")
    reverse = open(pair[1], "r")
    
    for line in forward:
        line = line.split(",")
        U_f.append(float(line[0]))
        I_f.append(float(line[1]))

    print("reverse")
    for line in reverse:
        line = line.split(",")
        U_r.append(float(line[0]))
        I_r.append(float(line[1]))

    U_r.sort(); I_r.sort()
    U_f.sort(); I_f.sort()


    Fig = plt.figure()
    Ax = Fig.add_subplot()
    plt.plot(U_f, I_f)
    plt.plot(U_r, I_r, color="black")
    plt.show()





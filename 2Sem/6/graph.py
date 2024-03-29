import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LinearLocator

x = []; y = []
fig_scale = 1.3
fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
plot_width = 28; plot_height = 20 # Size of graph paper in cm

def proccess_data (file, x, y):
    for line in file:
        line = line.split(',')
        x.append(float(line[0]))
        y.append(float(line[1]))

def create_graph_paper(xcells, ycells):
    Fig = plt.figure(figsize=(fig_width*fig_scale, fig_height*fig_scale))
    Ax = Fig.add_subplot()

    Ax.xaxis.set_major_locator(MaxNLocator(xcells))
    Ax.yaxis.set_major_locator(MaxNLocator(ycells))
    Ax.xaxis.set_minor_locator(LinearLocator(xcells*10))
    Ax.yaxis.set_minor_locator(LinearLocator(ycells*10))
    Ax.set_xticks([i for i in range(ycells)])
    Ax.set_yticks([i for i in range(xcells)])

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    return Fig, Ax

if __name__ == "__main__":
    file = open("data_hb.csv")
    proccess_data(file, x, y)
    for i in range(len(x)):
        print(x[i], y[i])
    print("hi main")
    Fig, Ax = plt.subplots()
    plt.plot(x, y)

    plt.show()

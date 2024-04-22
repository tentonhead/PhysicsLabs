import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator

fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
file = "data.csv"

d = 0.5 #mm
S = 80 #mm^2
ε0 = 8.85 * 10**-12 #Ф/м
ε0 *= 10**9

def get_data (file, x, y):
    for line in file:
        line = line.split(',')
        x.append(float(line[0]))
        y.append(float(line[1]))

def pair_point_method(x_list, y_list):
    angle = 0
    pairs = int(len(x_list)/2)
    for i in range(pairs):
        angle += ((y_list[i+pairs] - y_list[i]))\
            / (x_list[i+pairs] - x_list[i])
    return angle / pairs

def add_spaces_to_sides(string, num_before_dot, num_after_dot):
    left_len = len(string.split('.')[0]) 
    right_len = len(string.split('.')[1]) 
    if  left_len < num_before_dot:
        string = (num_before_dot-left_len)*" " + string
    if  right_len < num_after_dot:
        string = string + (num_after_dot-right_len)*'0'
    return string

if __name__ == "__main__":
    print(ε0)
    t = []; C =[]
    data = open(file, "r")
    get_data(data, t, C)
    t = np.array(t)
    C = np.array(C)

    ε = (C*d)/(ε0*S)
    one_by_ε = 1/ε
    '''
    for i in range(len(t)):
        print(t[i], C[i])
    '''
    Fig = plt.figure(figsize=(fig_width, fig_height))
    Ax = Fig.add_subplot()

    mult = 10**-1
    xmin = 30; xmax = 125.0
    ymin = 0.2*mult; ymax = 2*mult
    Ax.xaxis.set_major_locator(MultipleLocator(5))
    Ax.xaxis.set_minor_locator(LinearLocator(int(xmax-xmin)*2))
    Ax.yaxis.set_major_locator(MultipleLocator(0.1*mult))
    Ax.yaxis.set_minor_locator(LinearLocator(180))
    Ax.text(xmin-2.5, ymax+1*mult, "1/ε")
    Ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= "График 1: 1/ε = f(t)")

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    Ax.plot(1+0.005, ymin, ">k", transform=Ax.get_yaxis_transform(),
            clip_on=False)
    Ax.plot(xmin, 1+0.0075, "^k", transform=Ax.get_xaxis_transform(),
            clip_on=False)

    plt.scatter(t, one_by_ε, color="black", s=10)
    #plt.plot(t, one_by_ε, color="black")
    plt.show()
    plt.savefig("graph.png")

    output_file = open("output.csv", "w")
    output_file.write("| t, ℃  | C, нФ |  ε, 1/мм  | 1/ε, мм  |\n")
    output_file.write("+-------+-------+-----------+----------+\n")

    for i in range(len(t)):
        ti = str(t[i]); Ci = str(C[i])
        εi = str(ε[i].round(6)); one_by_εi = str(one_by_ε[i].round(6))
        ti = add_spaces_to_sides(ti, 3, 1)
        Ci = add_spaces_to_sides(Ci, 2, 2)
        εi = add_spaces_to_sides(εi, 2, 6)
        one_by_εi = add_spaces_to_sides(one_by_εi, 0, 6)

        output_file.write(f"| {ti} | {Ci} | {εi} | {one_by_εi} |\n")

    data.close()
    output_file.close()
    

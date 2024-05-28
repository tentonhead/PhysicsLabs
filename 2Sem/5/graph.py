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


def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom
    return A, B, C


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
    Fig1 = plt.figure(figsize=(fig_width, fig_height))
    Ax1 = Fig1.add_subplot()

    mult = 10
    xmin = 30; xmax = 125.0
    ymin = 5.0; ymax = 25

    Ax1.xaxis.set_major_locator(MultipleLocator(5))
    Ax1.xaxis.set_minor_locator(LinearLocator(int(xmax-xmin)*2))
    Ax1.yaxis.set_major_locator(MultipleLocator(0.1*mult))
    Ax1.yaxis.set_minor_locator(LinearLocator(180))
    Ax1.text(xmin-2.5, ymax+1*mult, "hi ε")
    Ax1.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= "График 1: зависимость ε от температуры")

    Ax1.grid(which='major', color='c', lw = 1)
    Ax1.grid(which='minor', color='c', lw = 0.25)

    Ax1.plot(1+0.005, ymin, ">k", transform=Ax1.get_yaxis_transform(),
            clip_on=False)
    Ax1.plot(xmin, 1+0.0075, "^k", transform=Ax1.get_xaxis_transform(),
            clip_on=False)

    f = 32
    a, b, c = calc_parabola_vertex(t[f],ε[f], t[f+1],ε[f+1], t[f+2],ε[f+2])
    top_x = np.linspace(t[f], t[f+2])
    top_y = a*top_x*top_x + b*top_x + c
    xof = 0; yof = 0

    plt.scatter(t, ε, color="black", s=10)
    plt.plot(top_x+xof, top_y+yof, color="black")
    plt.plot(t[:f+1], ε[:f+1], color="black")
    plt.plot(t[f+2:], ε[f+2:], color="black")
    #plt.savefig("graph1.png")
    #plt.show()

    Fig2 = plt.figure(figsize=(fig_width, fig_height))
    Ax2 = Fig2.add_subplot()

    mult = 10**-1
    xmin = 96; xmax = 125.0
    ymin = 0.4*mult; ymax = 1*mult
    Ax2.xaxis.set_major_locator(MultipleLocator(2))
    Ax2.xaxis.set_minor_locator(LinearLocator(int(xmax-xmin)*10))
    Ax2.yaxis.set_major_locator(MultipleLocator(0.05*mult))
    Ax2.yaxis.set_minor_locator(LinearLocator(180))
    Ax2.text(xmin-2.5, ymax+1*mult, "1/ε")
    Ax2.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= "График 2: зависимость 1/ε от температуры")

    Ax2.grid(which='major', color='c', lw = 1)
    Ax2.grid(which='minor', color='c', lw = 0.25)

    Ax2.plot(1+0.005, ymin, ">k", transform=Ax2.get_yaxis_transform(),
            clip_on=False)
    Ax2.plot(xmin, 1+0.0075, "^k", transform=Ax2.get_xaxis_transform(),
            clip_on=False)

    plt.scatter(t, one_by_ε, color="black", s=10)
    #plt.plot(t, one_by_ε, color="black")
    #plt.savefig("graph2.png")
    #plt.show()

    A = pair_point_method(t[-6:], one_by_ε[-6:])
    print(t[-6:])

    print(1/A)
    b = 0
    for i in range(6):
        b += (t[i]+273.15) - A / ε[i]
        print(b)
    print(b/6)
    print("--------")
    av_t = np.average(t[-6:]) +273.15
    av_1byε = np.average(one_by_ε[-6:])
    print("<t> =", av_t, "<1/ε =", av_1byε)
    b = av_1byε - A* av_t
    print(b)
    print("A =", A)
    print(-b/A)
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
    

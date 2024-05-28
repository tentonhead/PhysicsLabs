from re import X
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator

def get_data (file, x, y, z):
    for line in file:
        line = line.split(',')
        x.append(float(line[1]))
        y.append(float(line[2]))
        z.append(float(line[3]))

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

fig_width = 8.3; fig_height = 11.7 # Size of A4 paper in inches
file = "data.csv"

l = 1.00 #mm
h = 1.00 #mm
d =  7.00 * 10**3 #mm

if __name__ == "__main__":
    data = open(file, "r")
    t  = []
    Rm = []
    Rs = []
    get_data(data, t, Rm, Rs)
    t  = np.array(t)
    Rm = np.array(Rm)
    Rs = np.array(Rs)

    print("Table 1")
    for i in range(len(t)):
        print(t[i], Rm[i], Rs[i])

    T = t + 273.15
    one_by_T = 1/T
    lnRs = np.emath.log(Rs)
    Fig = plt.figure(figsize=(fig_width, fig_height))
    Ax1 = plt.subplot(211)

    # Set them manualy
    xstep = 5.0
    ystep = 0.01
    xmin = 295.0; xmax = 340.0
    ymin = 1.12; ymax = 1.30
    xmult = 2; ymult = 1000

    Xlabels = [""]
    for i in range(int(xmin)*10, int(xmax)*10+1, int(xstep)*5):
        if i % 10 == 0:
            Xlabels.append(str(int(i/10)))
        else:
            Xlabels.append("")

    Ax1.xaxis.set_major_locator(MultipleLocator(xstep/2))
    Ax1.xaxis.set_minor_locator(LinearLocator(int((xmax-xmin)*xmult)))
    Ax1.yaxis.set_major_locator(MultipleLocator(ystep))
    Ax1.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin)*ymult)))

    Ax1.text(xmin-2.5, ymax+0.01, r'$R_m$')
    Ax1.text(xmax+1.5, ymin-0.0075, r'T')
    Ax1.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= r'График 1: зависимость $R_m$ от T')

    Ax1.grid(which='major', color='c', lw = 1)
    Ax1.grid(which='minor', color='c', lw = 0.25)

    Ax1.plot(1+0.005, ymin, ">k", transform=Ax1.get_yaxis_transform(),
            clip_on=False)
    Ax1.plot(xmin, 1+0.0075, "^k", transform=Ax1.get_xaxis_transform(),
            clip_on=False)

    Ax1.set_xticklabels(Xlabels)

    #plt.plot   (T, Rm, color="black")
    plt.scatter(T, Rm, color="black", s=10)

    Ax2 = plt.subplot(212)
    xstep = 0.00005
    ystep = 0.2
    xmin = 0.00295; xmax = 0.00340
    ymin = 0.0; ymax = 2.0
    xmult = 200000; ymult = 50

    Ax2.xaxis.set_major_locator(MultipleLocator(xstep))
    Ax2.xaxis.set_minor_locator(LinearLocator(int((xmax-xmin)*xmult)))
    Ax2.yaxis.set_major_locator(MultipleLocator(ystep))
    Ax2.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin)*ymult)))

    Ax2.text(xmin-0.000025, ymax+0.1, r'$ln(R_s)$')
    Ax2.text(xmax+0.000001, ymin-0.2, r'1/T')
    Ax2.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= r'График 2: зависимость $ln(R_s)$ от f = 1/T')

    Ax2.grid(which='major', color='c', lw = 1)
    Ax2.grid(which='minor', color='c', lw = 0.25)

    Ax2.plot(1+0.005, ymin, ">k", transform=Ax2.get_yaxis_transform(),
            clip_on=False)
    Ax2.plot(xmin, 1+0.0075, "^k", transform=Ax2.get_xaxis_transform(),
            clip_on=False)

    #Ax2.set_xticklabels(Xlabels)
    plt.scatter(one_by_T, lnRs, color="black", s=10)
    #plt.savefig("graph1and2.png")
    plt.show()

    output_file = open("table1.csv", "w")
    output_file.write(
            "| t, ℃  |Rm, кОм|Rs, кОм|  T, K  | 1/T,K^-1 |  ln(Rs)  |\n"
            )
    output_file.write(
            "+-------+-------+-------+--------+----------+----------+\n"
            )

    for i in range(len(t)):
        ti = str(t[i]); Rmi = str(Rm[i])
        Rsi = str(Rs[i]); Ti = str(T[i]) 
        one_by_Ti = str(one_by_T[i].round(6))
        lnRsi = str(lnRs[i].round(6))
        ti        = add_spaces_to_sides(ti, 3, 0)
        Rmi       = add_spaces_to_sides(Rmi, 1, 3)
        Rsi       = add_spaces_to_sides(Rsi, 1, 3)
        Ti        = add_spaces_to_sides(Ti, 3, 2)
        one_by_Ti = add_spaces_to_sides(one_by_Ti, 1, 6)
        lnRsi     = add_spaces_to_sides(lnRsi, 1, 6)

        output_file.write(
                f"| {ti} | {Rmi} | {Rsi} | {Ti} | {one_by_Ti} | {lnRsi} |\n"
                )
    output_file.close()
    

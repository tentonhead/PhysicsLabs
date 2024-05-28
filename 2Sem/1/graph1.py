import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator

def get_data (file, x, y):
    for line in file:
        line = line.split(',')
        x.append(float(line[0]))
        y.append(float(line[1]))


def add_spaces_to_sides(string, num_before_dot, num_after_dot):
    left_len = len(string.split('.')[0]) 
    right_len = len(string.split('.')[1]) 
    if  left_len < num_before_dot:
        string = (num_before_dot-left_len)*" " + string
    if  right_len < num_after_dot:
        string = string + (num_after_dot-right_len)*'0'
    return string


def pair_point_method(x_list, y_list):
    output_file = open("table3.csv", "w")
    output_file.write("| № | ΔI, мА | ΔU_||, B | σ, (Ом*м)^-1|\n")
    output_file.write("+---+--------+----------+-------------+\n")

    angle = 0
    pairs = int(len(x_list)/2)
    print("pairs", pairs)
    σ_avr = 0
    for i in range(pairs):
        
        dU = (x_list[i+pairs] - x_list[i])
        dI = ((y_list[i+pairs] - y_list[i]))
        print("---\n", "i", i, "i+p", i+pairs,
             f"ΔI={dI} ΔU={dU} x[i]={x_list[i]} y[i]={y_list[i]}")
        angle += dI / dU
        Ui = round(dU, 3)
        Ii = round(dI, 3)
        σi = (l/S) * (Ii/Ui)
        σ_avr += σi 
        Ui = add_spaces_to_sides(str(Ui), 2, 3)
        Ii = add_spaces_to_sides(str(Ii), 1, 3)
        σi = add_spaces_to_sides(str(round(σi, 6)), 2, 3)
        output_file.write(f"| {i} | {Ii} | {Ui} | {σi} |\n")
    print("<σ> =",σ_avr/pairs)
    output_file.write("| σ-<σ>, (Ом*м)^-1| (σ-<σ>)^2, (Ом*м)^-1 |\n")
    output_file.write("+-----------------+---+------------------+\n")
    for i in range(pairs):
        dU = (x_list[i+pairs] - x_list[i])
        dI = ((y_list[i+pairs] - y_list[i]))
        Ui = dU#round(dU, 3)
        Ii = dI#round(dI, 3)
        σi = (l/S) * (Ii/Ui)
        print("σi = ", σi)
        output_file.write(f"| {σi-σ_avr} | {(σi-σ_avr)**2} |\n")
    output_file.close()
    return angle / pairs


def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom
    return A, B, C

fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
file = "data1.csv"

l = 1.00 #mm
h = 1.00 #mm
d =  7.00 * 10**3 #mm
S = d*h

if __name__ == "__main__":
    print("l/S", l/S)
    file = open(file, "r")
    U = []; I = []
    get_data(file, I, U)
    U = np.array(U); I = np.array(I)
    print("Table 1")
    for i in range(len(U)):
        print(U[i], I[i])

    Fig = plt.figure(figsize=(fig_width, fig_height))
    Ax = Fig.add_subplot()

    step = 0.2
    xmin = 0.0; xmax = 6.4
    ymin = 0.0; ymax = 3.2
    mult = 25

    print("x", int((xmax-xmin)*mult))
    print("y", int((ymax-ymin)*mult))
    Ax.xaxis.set_major_locator(MultipleLocator(step*2))
    Ax.xaxis.set_minor_locator(LinearLocator(int((xmax-xmin)*mult)))
    Ax.yaxis.set_major_locator(MultipleLocator(step))
    Ax.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin)*mult*2)))
    Ax.text(xmin-0.1, ymax+0.1, "I")
    Ax.text(xmax+0.1, ymin-0.1, r'U$_|$$_|$')
    Ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= r'График 1: зависимость I от $U_|$$_|$')

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    Ax.plot(1+0.005, ymin, ">k", transform=Ax.get_yaxis_transform(),
            clip_on=False)
    Ax.plot(xmin, 1+0.0075, "^k", transform=Ax.get_xaxis_transform(),
            clip_on=False)

    plt.plot   (U, I, color="black")
    plt.scatter(U, I, color="black", s=10)
    ##plt.show()
    plt.savefig("graph1.png")
    pair_point_method(U, I)
    

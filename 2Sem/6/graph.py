import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator
from math import pi as PI

fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
file = "data_xy.csv"

PI = round(PI, 4)
μ0 = 1.257 *(10**-6) # in metres
#μ0_full = 1.257

R1 = 100 # Om
R2 = 11000 # Om
C = 0.27 * (10**-6)# Ф
r_mid = 11 * (10**-3)# mm to m
S = 54 * (10**-6)# mm^2 to m^2
n1 = 100
n2 = 100

ax = 0.5
ay = 0.5
xc = 1.2
yo = 1.2


def proccess_data (file, x, y):
    for line in file:
        line = line.split(',')
        x.append(float(line[0]))
        y.append(float(line[1]))


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
        string = string + (num_after_dot-right_len)*' '
    return string


if __name__ == "__main__":
    x = []; y = []
    print("PI =", PI)
    Mx = (n1 * ax) / (2*PI*r_mid*R1); Mx = round(Mx, 4) 
    My = (R2 * C * ay) / (S*n2); My = round(My, 4)

    file = open("data_xy.csv")
    proccess_data(file, x, y)

    x = np.array(x) / 10
    y = np.array(y) /10
    H = Mx*x
    B = My*y

    Fig1 = plt.figure(figsize=(fig_width, fig_height))
    Ax1 = Fig1.add_subplot()

    mult = 10**-2
    xmin = 0.0; xmax = 32.0
    ymin = 0.0; ymax = 1.0
    Ax1.xaxis.set_major_locator(MultipleLocator(1))
    Ax1.xaxis.set_minor_locator(LinearLocator(int(xmax-xmin)*10))
    Ax1.yaxis.set_major_locator(MultipleLocator(5*mult))
    Ax1.yaxis.set_minor_locator(LinearLocator(int(ymax-ymin)*200))
    Ax1.text(xmin-1.5, ymax+2*mult, "B, ")#Тл")
    Ax1.text(xmax+0.5, ymin-3.2*mult, "H, ")#Aм")
    Ax1.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    Ax1.set(title= "График 1: B(H) - основная кривая намагничивания")

    Ax1.grid(which='major', color='c', lw = 1)
    Ax1.grid(which='minor', color='c', lw = 0.25)

    Ax1.plot(1+0.005, ymin, ">k", transform=Ax1.get_yaxis_transform(),
            clip_on=False)
    Ax1.plot(xmin, 1+0.0075, "^k", transform=Ax1.get_xaxis_transform(),
            clip_on=False)

    plt.scatter(H, B, color="black", s=10)


    μ = (1 / μ0) * (B/H)

    Fig2 = plt.figure(figsize=(fig_width, fig_height))
    Ax2 = Fig2.add_subplot()

    xmin = 0.0; xmax = 40.0
    ymin = 20000.0; ymax = 32000.0
    Ax2.xaxis.set_major_locator(MultipleLocator(2))
    Ax2.xaxis.set_minor_locator(LinearLocator(int(xmax-xmin)*5))
    Ax2.yaxis.set_major_locator(MultipleLocator(1000))
    Ax2.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin)/100)))
    Ax2.text(xmin-1.5, ymax+500, "μ")#Тл")
    Ax2.text(xmax+1, ymin-400, "H, A/м")
    Ax2.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
    Ax2.set(title= r'График 2: $\mu(H)$ - изменения магитной проницаемости')

    Ax2.grid(which='major', color='c', lw = 1)
    Ax2.grid(which='minor', color='c', lw = 0.25)

    Ax2.plot(1+0.005, 0, ">k", transform=Ax1.get_yaxis_transform(),
            clip_on=False)
    Ax2.plot(xmin, 1+0.0075, "^k", transform=Ax1.get_xaxis_transform(),
            clip_on=False)

    plt.scatter(H, μ, color="black", s=10)

    #plt.plot(t, one_by_ε, color="black")
    plt.savefig("graph_BH.pdf", format="pdf")
    plt.savefig("graph_MuH.pdf", format="pdf")
    plt.show()

    output_file = open("output.csv", "w")
    output_file.write("|  x,дел |  y,дел | H, A/м  | B, T  |     μ     |\n")
    output_file.write("+--------+--------+---------+-------+-----------+\n")

    for i in range(len(x)):
        xi = str(x[i])
        yi = str(y[i])
        Hi = str(H[i].round(3))
        Bi = str(B[i].round(3))
        μi = str(μ[i].round(3))
        xi = add_spaces_to_sides(xi, 2, 3)
        yi = add_spaces_to_sides(yi, 2, 3)
        Hi = add_spaces_to_sides(Hi, 2, 4)
        Bi = add_spaces_to_sides(Bi, 1, 3)
        μi = add_spaces_to_sides(μi, 1, 3)
        output_file.write(f"| {xi} | {yi} | {Hi} | {Bi} | {μi} |\n")

    file.close()
    output_file.close()
    

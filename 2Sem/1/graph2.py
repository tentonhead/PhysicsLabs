import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator

def get_data (file, x, y, z):
    for line in file:
        line = line.split(',')
        x.append(float(line[0]))
        y.append(float(line[1]))
        z.append(float(line[2]))

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

fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
file = "data2.csv"

l = 1.00 #mm
h = 1.00 #mm
d =  7.00 * 10**3 #mm

if __name__ == "__main__":
    file = open(file, "r")
    B = []; U = []; I = []
    get_data(file, I, U, B)
    B = np.array(B); U = np.array(U); I = np.array(I)
    print("Table 1")
    print("I\tU\tB")
    for i in range(len(U)):
        print(f"{I[i]}    {U[i]}    {B[i]}")

    Fig = plt.figure(figsize=(fig_width, fig_height))
    Ax = Fig.add_subplot()

    step = 0.02
    xmin = 0.0; xmax = 0.5
    ymin = 0.0; ymax = 140.0
    mult = 500

    print("x", int((xmax-xmin)*mult))
    print("y", int((ymax-ymin)*mult))
    Ax.xaxis.set_major_locator(MultipleLocator(step))
    Ax.xaxis.set_minor_locator(LinearLocator(int((xmax-xmin)*mult)))
    Ax.yaxis.set_major_locator(MultipleLocator(step*mult))
    Ax.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin))))
    Ax.text(xmin-0.015, ymax+2.0, "U ")
    Ax.text(xmax+0.015, ymin-4, r'B')
    Ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= r'График 2: зависимость ХЭДС от величины магнитной индукции U  = U (B)')

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)
    Ax.plot(1+0.005, ymin, ">k", transform=Ax.get_yaxis_transform(),
            clip_on=False)
    Ax.plot(xmin, 1+0.0075, "^k", transform=Ax.get_xaxis_transform(),
            clip_on=False)
    plt.plot   (B, U, color="black")
    plt.scatter(B, U, color="black", s=10)
    #plt.show()
    plt.savefig("graph2.png")

    '''
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
    output_file.close()
'''
    

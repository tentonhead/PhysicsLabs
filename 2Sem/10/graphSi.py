import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator
import numpy.linalg as linal


fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
files = ["silicon_forward.csv", "silicon_reverse.csv"]

def proccess_data (file, x, y):
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

def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
		'''
		Adapted and modifed to get the unknowns for defining a parabola:
		http://stackoverflow.com/questions/717762/how-to-calculate-the-vertex-of-a-parabola-given-three-points
		'''

		denom = (x1-x2) * (x1-x3) * (x2-x3);
		A     = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom;
		B     = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom;
		C     = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom;

		return A,B,C

Uf = []; If = []
Ur = []; Ir = []

if __name__ == "__main__":
    forward_bias = open(files[0], "r")
    reverse_bias = open(files[1], "r")
    proccess_data(forward_bias, Uf, If)
    proccess_data(reverse_bias, Ur, Ir)
    
    Uf = np.array(Uf); If = np.array(If) 
    Ur = np.array(Ur); Ir = np.array(Ir) 
    Uf_orig = Uf; If_orig = If; Ur_orig = Ur; Ir_orig = Ir

    print(10*'-')

    Fig = plt.figure(figsize=(fig_width, fig_height))
    Ax = Fig.add_subplot()

    xmin = -10.0; xmax = 10.0
    ymin = -12.0; ymax = 12.0
    Ax.xaxis.set_major_locator(MultipleLocator(1))
    Ax.xaxis.set_minor_locator(LinearLocator(int(xmax-xmin)*10))
    Ax.xaxis.tick_bottom()
    Ax.yaxis.set_major_locator(MultipleLocator(1))
    Ax.yaxis.set_minor_locator(LinearLocator(int(ymax-ymin)*10))
    Ax.yaxis.tick_right()
    Ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= "График 1: ВАХ кремниевого диода")

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    Ax.spines["bottom"].set_position('center')
    Ax.spines["left"].set_position('center')
    Ax.spines["right"].set_position('center')
    Ax.plot(1, 0, ">k", transform=Ax.get_yaxis_transform(), clip_on=False)
    Ax.plot(0, 1, "^k", transform=Ax.get_xaxis_transform(), clip_on=False)

    Uf_labels = [str(i/10) for i in range(11)]
    Ur_labels = [str(i) for i in range(-11, 0, 1)]
    Uf_labels[0] = "0"
    Uf_labels[-1] = r'Uпр, В'
    Ur_labels[1] = r'Uоб, В'
    If_labels = [str(i) for i in range(0, 13)]
    Ir_labels = [str(i) for i in range(-13, 0)]
    Ir_labels[1] = ' '; Ir_labels[2] = 'Iоб, мкА'
    If_labels[-1] = ' '; If_labels[-2] = 'Iпр, мА'


    Ax.set_xticklabels(Ur_labels+Uf_labels)
    Ax.set_yticklabels(Ir_labels+If_labels)

    Uf*=10
    Ir *= 100

    A, B, C = calc_parabola_vertex(Uf[5], If[5],\
                                   Uf[6], If[6],\
                                   Uf[7], If[7])
    Uf_x = np.linspace(Uf[5], Uf[7])
    Uf_y = A * Uf_x**2 + B * Uf_x + C

    plt.scatter(Uf, If, color="black", s = 15)
    plt.scatter(Ur, Ir, color="black", s = 15)
    plt.plot(Uf[:6], If[:6], color="black")
    plt.plot(Uf_x, Uf_y, color="black")
    plt.plot(Uf[7:], If[7:], color="black")
    plt.plot(Ur, Ir, color="black")

    idiots_coefficient = 6.6#-4.55
    angle_forward = pair_point_method(Uf[-1:-5:-1], If[-1:-5:-1])
    xf_tan = np.linspace(min(Uf), max(Uf))
    yf_tan = xf_tan * angle_forward
    xf = []; yf = []
    for i in range(len(xf_tan)):
        if yf_tan[i] >= -0.15:
            xf.append(xf_tan[i])
            yf.append(yf_tan[i])

    dummy_coeficient = -3.6
    angle_reverse = pair_point_method(Ur[-1:-9:-1], Ir[-1:-9:-1])
    xr_tan = np.linspace(min(Ur), max(Ur))
    yr_tan = xr_tan * angle_reverse# - idiots_coefficient

    xr = np.array(xr_tan)
    yr = np.array(yr_tan) + dummy_coeficient

    plt.plot(xf_tan+idiots_coefficient, yf_tan, color="black", linestyle="--")
    plt.plot(xr_tan, yr_tan, color="black", linestyle="--")

    plt.show()

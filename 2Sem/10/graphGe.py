import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator


fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
files = ["germanium_forward.csv", "germanium_reverse.csv"]

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
            title= "График 2: ВАХ германиевого диода")

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    Ax.spines["bottom"].set_position('center')
    Ax.spines["left"].set_position('center')
    Ax.spines["right"].set_position('center')
    Ax.plot(1, 1, ">k", transform=Ax.get_yaxis_transform(), clip_on=False)
    Ax.plot(0, 1, "^k", transform=Ax.get_xaxis_transform(), clip_on=False)

    Uf_labels = [str(i/10) for i in range(11)]
    Ur_labels = [str(i) for i in range(-11, 0, 1)]
    Uf_labels[0] = "0"
    Uf_labels[-1] = r'Uпр, В'
    Ur_labels[1] = r'Uоб, В'
    I_labels = [str(i) for i in range(-13, 13)]
    I_labels[1] = ' '; I_labels[2] = 'Iоб, мкА'
    I_labels[-1] = ' '; I_labels[-2] = 'Iпр, мА'


    Ax.set_xticklabels(Ur_labels+Uf_labels)
    Ax.set_yticklabels(I_labels)

    Uf*=10
    parabola_x = np.linspace(0, 1)
    parabola_y = 4 * parabola_x*parabola_x - 4

    #plt.scatter(Uf, If, color="red")
    plt.plot(Uf, If, color="black")
    plt.plot(parabola_x-1, parabola_y, color="black") 
    plt.plot(Ur[1:], Ir[1:], color="black")

    idiots_coefficient = -4.55
    angle_forward = pair_point_method(Uf[-1:-5:-1], If[-1:-5:-1])
    xf_tan = np.linspace(min(Uf), max(Uf))
    yf_tan = xf_tan * angle_forward + idiots_coefficient

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

    plt.plot(xf, yf, color="black", linestyle="--")
    plt.plot(xr, yr, color="black", linestyle="--")


    #Uft = [0.0, 0.01] + [i/100 for i in range(5, 750, 5)]
    Uft = [i/1000 for i in range(0, 680, 20)]
    Uft = np.array(Uft)
    print(Uft)

    Is = 3.6*10**-8 #-3.6
    e = 1.6*10**-19
    k = 1.38*10**-23
    T = 294

    Ift = Is * (np.exp((e*Uft)/(k*T)) - 1)# /1000

    print("    Uft\tIft")
    for i in range(len(Uft)):
        print(f"{i}, {Uft[i]}, {Ift[i]}")
    #plt.scatter(Uft*10, Ift, color="red")
    plt.plot(Uft*10, Ift, color="black", linestyle="-.")

    itc = idiots_theory_coefficient = 4.65
    angle_forward = pair_point_method(Uft[20:24], Ift[20:24])
    xft_tan = np.linspace(min(Uft), max(Uft))
    yft_tan = xft_tan * angle_forward#+ idiots_theory_coefficient
    plt.plot(xft_tan+itc, yft_tan, color="black", linestyle="--")

    dtc = dummy_theory_coefficient = -3.6
    Urt = [i/100 for i in range(0, -680, -20)]
    Urt = np.array(Urt)
    Irt = -Is * (np.exp((e*Urt)/(k*T)) - 1)# /1000
    plt.plot(Urt-0.2, Irt+dtc, color="black", linestyle="-.")

    print("    Urt\tIrt")
    for i in range(len(Urt)):
        print(f"{i}, {Urt[i]}, {Irt[i]}")

    angle_reverse = pair_point_method(Urt[-1:-24:-1], Irt[-1:-24:-1])
    xrt_tan = np.linspace(min(Urt), max(Urt))
    yrt_tan = xrt_tan * angle_reverse#+ idiots_theory_coefficient
    #plt.plot(xrt_tan-0.2, yrt_tan+dtc, color="red", linestyle="--")

    plt.savefig("graphGe.png")
    plt.show()

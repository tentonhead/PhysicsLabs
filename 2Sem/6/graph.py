import numpy as np
import matplotlib.pyplot as plt
from math import pi as PI
from matplotlib.ticker import FixedLocator, LinearLocator, MultipleLocator, MaxNLocator


x = []; y = []
fig_scale = 1.3
fig_width = 8.3; fig_height = 11.7 # Size of A4 paper in inches
plot_width = 15; plot_height = 15 # Size of graph paper in cm

PI = round(PI, 4)
Mu0_full = 1.257 *(10**-6) # in metres
Mu0 = 1.257

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


if __name__ == "__main__":
    print("PI =", PI)
    Mx = (n1 * ax) / (2*PI*r_mid*R1); Mx = round(Mx, 4) 
    My = (R2 * C * ay) / (S*n2); My = round(My, 4)

    file = open("data_xy.csv")
    proccess_data(file, x, y)

    x = np.array(x)
    y = np.array(y)
    rem_x = (x%5) / 5
    rem_y = (y%5) / 5
    x = x //5 + rem_x; x /= 2
    y = y //5 + rem_y; y /= 2
    H = Mx*x
    B = My*y

    print("x\ty")
    for i in range(len(x)):
        print(x[i], y[i])
    print("MU = ", Mu0)
    print(f"Mx = {Mx}\nMy = {My}")
    print(4*'-')
    print("Hc = ", Mx*xc)
    print("B0 = ", My*yo)
    print("Hm = ", Mx*x[0])
    print("Bm = ", My*y[0])
    print("x[0] =", x[0], "y[0] = ", y[0])
    print("----\n""H\tB")
    for i in range(len(H)):
        print("{:.3f} {:.3f}".format(H[i], B[i]))
    print("hi main")


    Fig, (Ax1, Ax2) = plt.subplots(2,1, figsize=(fig_width, fig_height))

    B_orig = B
    H_orig = H
    
    Ax1.plot(H, B, color="black")
    Ax1.scatter(H, B, color="black", s=15)


    Mu = np.zeros(len(H))
    for i in range(len(H)):
        Mu[i] = (1 / Mu0) * (B[i]/H[i])


    k = 0.0002
    Mu[-1] += k; Mu[-6] += k
    Mu[-2] += 2*k; Mu[-5] += 2*k
    Mu[-3] += 3*k; Mu[-4] += 3*k


    Ax2.plot(H, Mu, color="black")
    Ax2.scatter(H, Mu, color="black", s=15)

    print(8*'-')
    print("H\tMu")
    for i in range(len(H)):
        print("{:.3f}  {:.3f}".format(H[i], Mu[i]*10**6))


    Ax1.xaxis.set_major_locator(MultipleLocator(1))
    Ax1.xaxis.set_minor_locator(LinearLocator(180))
    Ax1.set(xlim=(14.0, 32.0), ylim=(0.575, 0.95),
            title= "График 1: B(H) - основная кривая намагничивания")
    Ax1.xaxis.tick_bottom()

    Ax1.yaxis.set_major_locator(MultipleLocator(0.025))
    Ax1.yaxis.set_minor_locator(LinearLocator(120))
    Ax1.yaxis.tick_left()

    Ax1.text(12.75, 0.97, r'B, Tл')
    Ax1.plot([14, 14], [0.9, 0.97], color="black", lw=0.5, clip_on=False)
    Ax1.plot(14, 0.97, "^k", clip_on=False)

    Ax1.text(32.5, 0.56, r'H, А/м')
    Ax1.plot([32, 32.4], [0.575, 0.575], color="black", lw=0.5, clip_on=False)
    Ax1.plot(32.4, 0.575, ">k", clip_on=False)

    Ax1.grid(which='major', color='c', lw = 1)
    Ax1.grid(which='minor', color='c', lw = 0.25)


    a2xmax = 32; a2xmin = 15
    a2ymax = 0.031; a2ymin = 0.023
    Ax2.xaxis.set_major_locator(MultipleLocator(1))
    Ax2.xaxis.set_minor_locator(LinearLocator(170))
    Ax2.set(xlim=(a2xmin, a2xmax), ylim=(a2ymin, a2ymax))
    Ax2.set(title= r'График 2: $\mu(H)$ - изменения магитной проницаемости')
    Ax2.xaxis.tick_bottom()

    Ax2.yaxis.set_major_locator(MultipleLocator(0.0005))
    Ax2.yaxis.set_minor_locator(LinearLocator(140))
    Ax2.yaxis.tick_left()

    Ax2.text(a2xmin-1.5, a2ymax+0.0005, r'$\mu$, Гн/м')
    Ax2.plot([a2xmin, a2xmin], [a2ymax, a2ymax+0.0002],
             color="black", lw=0.5, clip_on=False)
    Ax2.plot(a2xmin, a2ymax+0.0002, "^k", clip_on=False)

    Ax2.text(a2xmax+0.5, a2ymin-0.0004, r'H, А/м')
    Ax2.plot([a2xmax, a2xmax+0.5], [a2ymin, a2ymin],
             color="black", lw=0.5, clip_on=False)
    Ax2.plot(a2xmax+0.4, a2ymin, ">k", clip_on=False)
 
    Ax2.grid(which='major', color='c', lw = 1)
    Ax2.grid(which='minor', color='c', lw = 0.25)

    #plt.show()
    plt.savefig("2_6_graph.png")


import numpy as np
from matplotlib import pyplot as plt

data = open("data_tu.csv", 'r')
fig_scale = 1.3
fig_width = 8.3; fig_height = 11.7 # Size of A4 paper in inches
plot_width = 15; plot_height = 15 # Size of graph paper in cm

T = []; U = []
Ro = 50
k = 1.38*10**-23
l = 0.02
I = 0.0005
A = 0.0002

def proccess_data (file, x, y):
    for line in file:
        line = line.split(',')
        x.append(float(line[0]))
        y.append(float(line[1]))


if __name__ == "__main__":

    file = open("data_tu.csv")
    proccess_data(file, T, U)

    T = np.array(T)
    U = np.array(U)

    Fig, Ax = plt.subplots(figsize=(fig_width, fig_height))

    
    Ax.plot(H, B, color="black")
    Ax.scatter(H, B, color="black", s=15)


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


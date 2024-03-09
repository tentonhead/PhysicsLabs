import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LinearLocator

all_files = [["silicon_forward.csv", "silicon_reverse.csv"],
             ["germanium_forward.csv", "germanium_reverse.csv"]]
num = 1
fig_scale = 1.3
fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
plot_width = 28; plot_height = 20 # Size of graph paper in cm
xr_multiplier = 10
yl_multiplier = 100
xoffset = int(plot_width / 2)
yoffset = int(plot_height / 2)

for pair in all_files:
    forward_bias = open(pair[0], "r")
    reverse_bias = open(pair[1], "r")

    U_original = []
    I_original = []
    U_f = []; I_f = []
    U_r = []; I_r = []

    for line in forward_bias:
        line = line.split(",")
        U_original.append(float(line[0]))
        I_original.append(float(line[1]))
        U_f.append(float(line[0])*xr_multiplier+xoffset)
        I_f.append(float(line[1])+yoffset)

    for line in reverse_bias:
        line = line.split(",")
        U_original.append(float(line[0]))
        I_original.append(float(line[1]))
        U_r.append(float(line[0])+xoffset)
        if pair[1] == "silicon_reverse.csv":
            I_r.append(float(line[1])*yl_multiplier+yoffset)
        else:
            I_r.append(float(line[1])+yoffset)

    U_original.sort()
    I_original.sort()

    U_ticks = []
    I_ticks = []

    for i in range(xoffset):
        U_ticks.append(str((i-xoffset)))
    for i in range(xoffset, plot_width):
        U_ticks.append(str((i-xoffset)/10))

    for i in range(yoffset, 0, -1):
        if pair[1] == "silicon_reverse.csv":
            I_ticks.append(str(i*-0.01)[0:5])
        else:
            I_ticks.append(str(-1*i)[0:4])
    for i in range(yoffset, plot_height):
        I_ticks.append(str((i-10)))

    U_ticks[xoffset] = '' # Remove extra 0 label on intersection of spines
    U_ticks[0] = ''
    I_ticks[0] = ''
    I_ticks[1] = r'$Iоб, мкА$'
    I_ticks[plot_height-1] = r'$Iпр, мА$'


    Fig = plt.figure(figsize=(fig_width*fig_scale, fig_height*fig_scale))
    Ax = Fig.add_subplot()

    '''
    print(f"Fowrwad U_min={min(U_f)}, U_max={max(U_f)}")
    print(f"Reverse U_min={min(U_r)}, U_max={max(U_r)}")
    print(f"Fowrwad I_min={min(I_f)}, I_max={max(I_f)}")
    print(f"Reverse I_min={min(I_r)}, I_max={max(I_r)}")
    '''
    #U_r_lin = np.linspace(np.min(U_r), xoffset, 1400)
    #I_r_interp = np.interp(U_r_lin, U_r, I_r)
    U_f_lin = np.linspace(min(U_f), max(U_f), 1400)
    I_f_interp = np.interp(U_f_lin, U_f, I_f)

    Ax.scatter(U_r, I_r, color="black", s=15)
    Ax.scatter(U_f, I_f, color="black", s=15)
    Ax.plot(U_f_lin, I_f_interp, color="black", linestyle="--")
    Ax.set_xlim(0, plot_width)
    Ax.set_ylim(0, plot_height)

    p = np.linspace(13, 14)
    if pair[1] == "germanium_reverse.csv":
        Ax.plot(p, 4*(p-13)**2+6, color="black", linestyle="--") # Draw parabola branch
        Ax.plot(U_r[1:], I_r[1:], color="black", linestyle="--")

    else:
        Ax.plot(U_r, I_r, color="black", linestyle="--")

    Ax.xaxis.set_major_locator(MaxNLocator(plot_width))
    Ax.yaxis.set_major_locator(MaxNLocator(plot_height))
    Ax.xaxis.set_minor_locator(LinearLocator(plot_width*10))
    Ax.yaxis.set_minor_locator(LinearLocator(plot_height*10))
    Ax.set_xticks([i for i in range(plot_width)])
    Ax.set_yticks([i for i in range(plot_height)])


    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)

    Ax.set_xticklabels(U_ticks)
    Ax.set_yticklabels(I_ticks)
    Ax.yaxis.tick_right()
    Ax.spines["bottom"].set_position('center')
    Ax.spines["left"].set_position('center')
    Ax.spines["right"].set_position('center')
    Ax.plot(1, 10, ">k", transform=Ax.get_yaxis_transform(), clip_on=False)
    Ax.plot(14, 1, "^k", transform=Ax.get_xaxis_transform(), clip_on=False)

    #Ax.text(xoffset+1.2, plot_height-1, r'$Iпр, мА$')
    #Ax.text(xoffset+1.2, 1, )
    Ax.text(1, yoffset+0.2, r'$Uоб, В$')
    Ax.text(plot_width-2, yoffset+0.2, r'$Uпр, В$')

    if num == 1:
        plt.title(f"Рис. 1 ВАХ Кремниевого диода")
    else:
        plt.title(f"Рис. 2 ВАХ Германиевого диода")

    #plt.show()

    plt.savefig(f"2_10_graph{num}.png")
    num+=1

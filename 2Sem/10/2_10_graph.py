import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LinearLocator
import numpy.linalg as linal


all_files = [["silicon_forward.csv", "silicon_reverse.csv"],
             ["germanium_forward.csv", "germanium_reverse.csv"]]
fig_scale = 1.3
fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
plot_width = 28; plot_height = 20 # Size of graph paper in cm
xoffset = int(plot_width / 2)
yoffset = int(plot_height / 2)
xr_multiplier = 10
yl_multiplier = 100
graph_index = 1


for pair in all_files:
    forward_bias = open(pair[0], "r")
    reverse_bias = open(pair[1], "r")

    U_f = []; I_f = []
    U_r = []; I_r = []

    for line in forward_bias:
        line = line.split(",")
        U_f.append(float(line[0])*xr_multiplier+xoffset)
        I_f.append(float(line[1])+yoffset)

    for line in reverse_bias:
        line = line.split(",")
        U_r.append(float(line[0])+xoffset)
        if pair[1] == "silicon_reverse.csv":
            I_r.append(float(line[1])*yl_multiplier+yoffset)
        else:
            I_r.append(float(line[1])+yoffset)


    Fig = plt.figure(figsize=(fig_width*fig_scale, fig_height*fig_scale))
    Ax = Fig.add_subplot()

    U_f_lin = np.linspace(np.min(U_f), np.max(U_f), 1400)
    I_f_interp = np.interp(U_f_lin, U_f, I_f)

    Ax.scatter(U_r, I_r, color="black", s=15)
    Ax.scatter(U_f, I_f, color="black", s=15)
    Ax.set_xlim(0, plot_width); Ax.set_ylim(0, plot_height)
    Ax.plot(U_f_lin, I_f_interp, color="black")



    xf_tangent = U_f[-1:-3:-1]; yf_tangent = I_f[-1:-3:-1]
    xr_tangent = U_r[-1:-3:-1]; yr_tangent = I_r[-1:-3:-1]
    ans1 = np.polyfit(xf_tangent, yf_tangent, 1)
    ans2 = np.polyfit(xr_tangent, yr_tangent, 1)

    if pair[1] == "germanium_reverse.csv":
        p = np.linspace(13, 14)
        Ax.plot(p, 4*(p-13)**2+6, color="black") # Draw parabola branch
        Ax.plot(U_r[1:], I_r[1:], color="black")
        xf_tangent = np.linspace(4, 9, 5)
        yf_tangent = xf_tangent*ans1[0] + ans1[1]
        xr_tangent = np.linspace(-9, -1, 5)
        yr_tangent = xr_tangent*ans2[0] + ans2[1]
        xr_tangent += xoffset+1; yr_tangent += yoffset-4
        yf_tangent += 3*yoffset
        plt.plot(xr_tangent, yr_tangent, color="red")
    else:
        Ax.plot(U_r, I_r, color="black")
        xf_tangent = np.linspace(7, 9, 20)
        yf_tangent = xf_tangent*ans1[0] + ans1[1]+85.4
    ###print(xr_tangent, yr_tangent)
    print("forward----")
    print(xf_tangent, yf_tangent)
    print(10*'-')


    xf_tangent += xoffset; yf_tangent -= yoffset

    '''
    print("solution")
    print(ans1, ans2)
    '''
    
    #print(xf_tangent); print(yf_tangent)
    plt.plot(xf_tangent, yf_tangent, color="red")


    Ax.xaxis.set_major_locator(MaxNLocator(plot_width))
    Ax.yaxis.set_major_locator(MaxNLocator(plot_height))
    Ax.xaxis.set_minor_locator(LinearLocator(plot_width*10))
    Ax.yaxis.set_minor_locator(LinearLocator(plot_height*10))
    Ax.set_xticks([i for i in range(plot_width)])
    Ax.set_yticks([i for i in range(plot_height)])

    Ax.grid(which='major', color='c', lw = 1)
    Ax.grid(which='minor', color='c', lw = 0.25)


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
            I_ticks.append(str(i*-1)[0:4])
    for i in range(yoffset, plot_height):
        I_ticks.append(str((i-10)))

    U_ticks[xoffset] = '' # Remove extra 0 label on intersection of spines
    U_ticks[0] = ''
    I_ticks[0] = ''
    I_ticks[1] = r'$Iоб, мкА$'
    I_ticks[plot_height-1] = r'$Iпр, мА$'

    Ax.set_xticklabels(U_ticks)
    Ax.set_yticklabels(I_ticks)
    Ax.yaxis.tick_right()


    Ax.spines["bottom"].set_position('center')
    Ax.spines["left"].set_position('center')
    Ax.spines["right"].set_position('center')
    Ax.plot(1, 10, ">k", transform=Ax.get_yaxis_transform(), clip_on=False)
    Ax.plot(14, 1, "^k", transform=Ax.get_xaxis_transform(), clip_on=False)

    Ax.text(1, yoffset+0.2, r'$Uоб, В$')
    Ax.text(plot_width-2, yoffset+0.2, r'$Uпр, В$')

    if graph_index == 1:
        plt.title(f"Рис. 1 ВАХ Кремниевого диода")
    else:
        plt.title(f"Рис. 2 ВАХ Германиевого диода")

    plt.show()

    #plt.savefig(f"2_10_graph{num}.png")
    graph_index+=1

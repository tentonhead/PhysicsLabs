import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LinearLocator

def pair_point_method(x_list, y_list):
    angle = 0
    pairs = int(len(x_list)/2)
    for i in range(pairs):
        angle += ((y_list[i+pairs] - y_list[i]))\
            / (x_list[i+pairs] - x_list[i])
    return angle / pairs
        

files = ["silicon_forward.csv", "silicon_reverse.csv"]
fig_scale = 1.3
fig_width = 11.7; fig_height = 8.3 # Size of A4 paper in inches
plot_width = 28; plot_height = 20 # Size of graph paper in cm
xoffset = int(plot_width / 2)
yoffset = int(plot_height / 2)
xr_multiplier = 10
yl_multiplier = 100
graph_index = 1

U_f = []; I_f = []
U_r = []; I_r = []

forward_bias = open(files[0], "r")
reverse_bias = open(files[1], "r")

for line in forward_bias:
    line = line.split(",")
    U_f.append(float(line[0])*xr_multiplier+xoffset)
    I_f.append(float(line[1])+yoffset)

for line in reverse_bias:
    line = line.split(",")
    U_r.append(float(line[0])+xoffset)
    I_r.append(float(line[1])*yl_multiplier+yoffset)


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
f_angle = pair_point_method(xf_tangent, yf_tangent)

Ax.plot(U_r, I_r, color="black")
xf_tangent = np.linspace(7.05, 9)
yf_tangent = xf_tangent*ans1[0] + ans1[1]+85.4
###print(xr_tangent, yr_tangent)
print("reverse----")
print(xr_tangent, yr_tangent)
print(10*'-')
xf_tangent += xoffset; yf_tangent -= yoffset
#print(xf_tangent); print(yf_tangent)
plt.plot(xf_tangent, yf_tangent, color="black", linestyle="--")

Ax.xaxis.set_major_locator(MaxNLocator(plot_width))
Ax.yaxis.set_major_locator(MaxNLocator(plot_height))
Ax.xaxis.set_minor_locator(LinearLocator(plot_width*10))
Ax.yaxis.set_minor_locator(LinearLocator(plot_height*10))
Ax.set_xticks([i for i in range(plot_width)])
Ax.set_yticks([i for i in range(plot_height)])

Ax.grid(which='major', color='c', lw = 1)
Ax.grid(which='minor', color='c', lw = 0.25)

U_ticks = [str(i-xoffset) for i in range(xoffset)]
U_ticks.extend(str((i-xoffset)/10) for i in range(xoffset, plot_width))
I_ticks = [str(i*-0.01)[0:5] for i in range(yoffset, 0, -1)]

I_ticks.extend([str(i-10)for i in range(yoffset, plot_height)])

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

Ax.text(7.5+xoffset, yoffset+0.2, r'$Uотс$')

plt.title(f"Рис. 1 ВАХ Кремниевого диода")

#plt.show()

plt.savefig("2_10_graph_silicon.png")

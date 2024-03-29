import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LinearLocator
import numpy.linalg as linal


def pair_point_method(x_list, y_list):
    angle = 0
    pairs = int(len(x_list)/2)
    for i in range(pairs):
        angle += ((y_list[i+pairs] - y_list[i]))\
            / (x_list[i+pairs] - x_list[i])
    return angle / pairs
        

files = ["germanium_forward.csv", "germanium_reverse.csv"]
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
    I_r.append(float(line[1])+yoffset)


Fig = plt.figure(figsize=(fig_width*fig_scale, fig_height*fig_scale))
Ax = Fig.add_subplot()

U_f_lin = np.linspace(np.min(U_f), np.max(U_f), 1400)
I_f_interp = np.interp(U_f_lin, U_f, I_f)

Ax.scatter(U_r, I_r, color="black", s=15)
Ax.scatter(U_f, I_f, color="black", s=15)
Ax.set_xlim(0, plot_width); Ax.set_ylim(0, plot_height)
Ax.plot(U_f_lin, I_f_interp, color="black")

p = np.linspace(13, 14)
Ax.plot(p, 4*(p-13)**2+6, color="black") # Draw parabola branch
Ax.plot(U_r[1:], I_r[1:], color="black")

xf_tangent = U_f[-1:-7:-1]; yf_tangent = I_f[-1:-7:-1]
xr_tangent = U_r[-1:-9:-1]; yr_tangent = I_r[-1:-9:-1]
ans1 = np.polyfit(xf_tangent, yf_tangent, 1)
ans2 = np.polyfit(xr_tangent, yr_tangent, 1)
f_angle = pair_point_method(xf_tangent, yf_tangent)
r_angle = pair_point_method(xr_tangent, yr_tangent)

xf_tangent = np.linspace(3.1, 9, 59)
yf_tangent = xf_tangent*f_angle + yoffset - 3.8

xr_tangent = np.linspace(-9, 0, 9)
yr_tangent = xr_tangent*r_angle + yoffset -3.6

xf_tangent += xoffset; xr_tangent += xoffset
print("reverse----")
print(xr_tangent, yr_tangent)
print(10*'-')
plt.plot(xf_tangent, yf_tangent, color="black", linestyle="--")
plt.plot(xr_tangent, yr_tangent, color="black", linestyle="--")


U_ft = []; I_ft = []
U_rt = []; I_rt = []
for line in open("germanium_theory.csv"):
    line = line.split(',') #Ufor    Urev    Ifor    Urev    
    U_ft.append(float(line[0])*2*xr_multiplier+xoffset)
    I_ft.append(float(line[2])+yoffset)
    U_rt.append(float(line[1])+xoffset)
    I_rt.append(float(line[3])+yoffset)

plt.plot(U_ft, I_ft, color="black", linestyle="-.")
plt.plot(U_rt, I_rt, color="black", linestyle="-.")

xft_tangent = U_ft[3:5]; yft_tangent = I_ft[3:5]
ans1 = np.polyfit(xft_tangent, yft_tangent, 1)
ft_angle = pair_point_method(xft_tangent, yft_tangent)
print("ft_angle= ", ft_angle)
print("ans1[1] =", ans1[1])

xft = np.linspace(3.85, 5)
yft = xft*ft_angle - 2*yoffset
xft += xoffset-1

xrt = np.linspace(xoffset, xoffset-1)
yrt = [3.4+yoffset-7]* len(xrt)

plt.plot(xft, yft, color="black", linestyle="--")
plt.plot(xrt, yrt, color="black", linestyle="--")
print("forward----")
print(xft, yft)
print(10*'-')

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
I_ticks = [str(i*-1)[0:4] for i in range(yoffset, 0, -1)]
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

Ax.text(4+xoffset, yoffset+0.2, r'$Uотс$')
Ax.text(xoffset-0.5, yoffset-4.2, r'$Is$')

plt.title(f"Рис. 2 ВАХ Германиевого диода")

#plt.show()

plt.savefig(f"2_10_graph_germanium.png")

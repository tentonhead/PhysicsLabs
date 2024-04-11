import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import ln

def pair_point_method(x_list, y_list):
    angle = 0
    pairs = int(len(x_list)/2)
    for i in range(pairs):
        angle += ((y_list[i+pairs] - y_list[i]))\
            / (x_list[i+pairs] - x_list[i])
    return angle / pairs

file = open("data.csv")

x = []
y = []
for line in file:
    line = line.split(",")
    x.append(float(line[3]))
    y.append(float(line[4]))

T_reverse = np.array(x)
LnRs = np.array(y)
T_reve

Fig, Ax = plt.subplots()

plt.plot(x, y)
plt.show()


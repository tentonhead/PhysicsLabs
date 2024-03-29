import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy.linalg as linal

all_files = [["2_10/silicon_forward.csv", "2_10/silicon_reverse.csv"],
             ["2_10/germanium_forward.csv", "2_10/germanium_reverse.csv"]]

fwd = [i for i in open("10/silicon_forward.csv", 'r')]
bwd = [i for i in open("10/silicon_reverse.csv", 'r')]

xr = []; yr = []
xl = []; yl = []

for line in fwd:
    line = line.split(',')
    xr.append(float(line[0]))
    yr.append(float(line[1]))

for line in bwd:
    line = line.split(',')
    xl.append(float(line[0]))
    yl.append(float(line[1]))

fig, ax = plt.subplots()



#ax1+b=y1
#ax1+b=y1

x = xl+xr; x.sort()
y = yl+yr; y.sort()
a = np.array(x[-1:-2])
b = np.array(y[-1:-2])
print(linal.solve(a, b))
plt.plot(xr, yr)
plt.scatter(xr, yr, color="black")





plt.show()

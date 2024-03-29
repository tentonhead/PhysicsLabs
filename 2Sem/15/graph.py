import numpy
from matplotlib import pyplot

data = open("data_tu.csv", 'r')
x = []; y = []

for line in data:
    line = line.split(",")
    x.append(float(line[0]))
    y.append(float(line[1]))

print(x, y)


import math

PI = math.pi
R1 = 100
R2 = 11000
C = 0.27
r_mid = 11.00
S = 54
n1 = 100
n2 = 100
ax = 0.5
ay = 0.5

x0 = 1.2
y0 = 1.2

file = open("data_xy.csv", "r")
Mx = (n1*ax) / (2*PI*r_mid*R1)
My = (R2*C*ay) / (S*n2)
print(Mx, My)

H = []
B = []

H0 = Mx * x0
B0 = My * y0

print(H0, B0)

HB_file = open("data_hb.csv", "w")

for line in file:
    line = line.split(",")
    H.append(float(line[0])*Mx)
    B.append(float(line[1])*My)

for i in range(len(H)):
    HB_file.write(f"{H[i]}, {B[i]}\n")



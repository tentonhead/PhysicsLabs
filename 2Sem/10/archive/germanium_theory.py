import numpy as np
files = ["germanium_forward.csv", "germanium_reverse.csv"]

U_f = []; I_f = []
U_r = []; I_r = []

forward_bias = open(files[0], "r")
reverse_bias = open(files[1], "r")

for line in forward_bias:
    line = line.split(",")
    U_f.append(float(line[0]))
    I_f.append(float(line[1]))

for line in reverse_bias:
    line = line.split(",")
    U_r.append(float(line[0]))
    I_r.append(float(line[1]))

U_ft = []; I_ft = []
U_rt = []; I_rt = []

Is = -3.6
e = -1.6 * 10**-19
k = 8.617 * 10**-5
T = 294 # K
print("e =", e, "k =", k)
'''
U_ft = np.array(U_f)
I_ft = Is * (np.exp((e*U_ft)/(k*T))- 1)
'''

print("U\tI")
for i in range(len(I_f)):
    U = U_f[i]
    U_ft.append(U_f[i])
    I = Is * (np.exp(e * U)/(k*T) - 1)
    I_f.append(I)
    print(F"{U}\t{I}")

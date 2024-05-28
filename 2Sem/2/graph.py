import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator

def get_data (file, x, y, z):
    for line in file:
        line = line.split(',')
        x.append(float(line[1]))
        y.append(float(line[2]))
        z.append(float(line[3]))

def pair_point_method(x_list, y_list, k, filename):
    file = open(filename, 'w')
    file.write("Y, X, alpha\n")
    sum = 0
    pairs = int(len(x_list)/2)
    for i in range(pairs):
        y = y_list[i+pairs] - y_list[i]
        x = x_list[i+pairs] - x_list[i]
        angle = k * (y/x) 
        sum += angle
        file.write("{}, {}, {}\n".format(y, x, angle))
    avg = sum/pairs
    file.write("The average is {}\n".format(avg))

    file.write("alpha-<alpha>, (alpha-<alpha>)^2\n")
    print("AAAAAA")
    for i in range(pairs):
        y = y_list[i+pairs] - y_list[i]
        x = x_list[i+pairs] - x_list[i]
        angle = round(k * (y/x), 6) 
        dif = angle - round(avg, 6) 
        dif2 = dif * dif
        print(angle, dif, dif2)

        file.write("{}, {}\n".format(dif, dif2))
    file.close()
    return avg

def add_spaces_to_sides(string, num_before_dot, num_after_dot):
    left_len = len(string.split('.')[0]) 
    right_len = len(string.split('.')[1]) 
    if  left_len < num_before_dot:
        string = (num_before_dot-left_len)*" " + string
    if  right_len < num_after_dot:
        string = string + (num_after_dot-right_len)*'0'
    return string


def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom
    return A, B, C

fig_width = 8.3; fig_height = 11.7 # Size of A4 paper in inches
file = "data.csv"

if __name__ == "__main__":
    data = open(file, "r")
    t  = []
    Rm = []
    Rs = []
    get_data(data, t, Rm, Rs)
    t  = np.array(t)
    Rm = np.array(Rm)
    Rs = np.array(Rs)

    print("Table 1\n", 11*'-')
    for i in range(len(t)):
        print(t[i], Rm[i], Rs[i])
    print(11*'-')

    T = t + 273.15
    one_by_T = 1/T
    lnRs = np.emath.log(Rs)

    print("T min, max:", min(T), max(T))
    print("Rm min, max:", min(Rm), max(Rm))
    print("ln(Rs) min, max:", min(lnRs), max(lnRs))
    print(11*'-')

    Fig = plt.figure(figsize=(fig_width, fig_height))
    Ax1 = plt.subplot(211)

    # Set them manualy
    conv = 1000 # from kOms to Oms
    xstep = 5.0
    ystep = 0.02*conv
    xmin = 270.0; xmax = 340.0
    ymin = 1.00*conv; ymax = 1.30*conv
    xmult = 2; ymult = 1000/conv

    Ax1.xaxis.set_major_locator(MultipleLocator(xstep))
    Ax1.xaxis.set_minor_locator(LinearLocator(int((xmax-xmin)*xmult)))
    Ax1.yaxis.set_major_locator(MultipleLocator(ystep))
    Ax1.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin)*ymult)))

    Ax1.text(xmin-2.5, ymax+0.01, r'$R_m$')
    Ax1.text(xmax+1.5, ymin-0.0075, r'T')
    Ax1.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= r'График 1: зависимость $R_m$ от T')

    Ax1.grid(which='major', color='c', lw = 1)
    Ax1.grid(which='minor', color='c', lw = 0.25)

    Ax1.plot(1+0.005, ymin, ">k", transform=Ax1.get_yaxis_transform(),
            clip_on=False)
    Ax1.plot(xmin, 1+0.0075, "^k", transform=Ax1.get_xaxis_transform(),
            clip_on=False)


    #plt.plot   (T, Rm, color="black")
    tzero_x = 2 * [273.15]
    tzero_y = [i for i in range(1000, 1080, 40)]
    plt.plot(tzero_x, tzero_y, "--", color="black", lw=1)

    Rm = Rm*conv
    print(Rm)
    print("Pairs for calculating the angle")
    xpair = [T[1], T[3]]+list(T[6:])
    ypair = [Rm[1], Rm[3]]+list(Rm[6:])
    for i in range(len(xpair)):
        print(i+1, xpair[i], ypair[i])
    print(11*'-')

    R0 = 1033

    alpha = pair_point_method(xpair, ypair, 1/R0, "pair_point1.csv")
    print("The avg angle is", alpha)

    print(10*'-')
    mid = 0
    for i in range(len(xpair)):
        ans = ypair[i] - alpha*xpair[i]
        print(ans)
        mid += ans
    mid = mid/len(xpair)
    print("MID =", mid)
    print(10*'-')

    x = np.array([i for i in range(int(xmin), int(xmax), 5)])
    plt.plot(x, alpha*x+mid, 'k--')

    plt.scatter(T, Rm, color="black", s=10)

    Ax2 = plt.subplot(212)
    xstep = 0.00005
    ystep = 0.2
    xmin = 0.00295; xmax = 0.00340
    ymin = 0.0; ymax = 1.8
    xmult = 200000; ymult = 50

    Ax2.xaxis.set_major_locator(MultipleLocator(xstep))
    Ax2.xaxis.set_minor_locator(LinearLocator(int((xmax-xmin)*xmult)))
    Ax2.yaxis.set_major_locator(MultipleLocator(ystep))
    Ax2.yaxis.set_minor_locator(LinearLocator(int((ymax-ymin)*ymult)))

    Ax2.text(xmin-0.000025, ymax+0.1, r'$ln(R_s)$')
    Ax2.text(xmax+0.000001, ymin-0.2, r'1000/T')
    Ax2.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
            title= r'График 2: зависимость $ln(R_s)$ от f = 1/T')

    Ax2.grid(which='major', color='c', lw = 1)
    Ax2.grid(which='minor', color='c', lw = 0.25)

    Ax2.plot(1+0.005, ymin, ">k", transform=Ax2.get_yaxis_transform(),
            clip_on=False)
    Ax2.plot(xmin, 1+0.0075, "^k", transform=Ax2.get_xaxis_transform(),
            clip_on=False)

    gamma = pair_point_method(one_by_T, lnRs, 1,"pair_point2.csv")

    X2labels = [""]
    for i in range(int(xmin*100_000), int(xmax*100_000)+int(xstep*100_000),
                   int(xstep*100_000)):
        #print(i)
        X2labels.append(str(i))
    Ax2.set_xticklabels(X2labels)

    plt.scatter(one_by_T, lnRs, color="black", s=10)
    #plt.savefig("graph1and2.png")
    plt.show()

    output_file = open("table1.csv", "w")
    output_file.write(
            "| t, ℃  |Rm, кОм|Rs, кОм|  T, K  | 1/T,K^-1 |  ln(Rs)  |\n"
            )
    output_file.write(
            "+-------+-------+-------+--------+----------+----------+\n"
            )

    for i in range(len(t)):
        ti = str(t[i]); Rmi = str(Rm[i])
        Rsi = str(Rs[i]); Ti = str(T[i]) 
        one_by_Ti = str(one_by_T[i].round(6))
        lnRsi = str(lnRs[i].round(6))
        ti        = add_spaces_to_sides(ti, 3, 0)
        Rmi       = add_spaces_to_sides(Rmi, 1, 3)
        Rsi       = add_spaces_to_sides(Rsi, 1, 3)
        Ti        = add_spaces_to_sides(Ti, 3, 2)
        one_by_Ti = add_spaces_to_sides(one_by_Ti, 1, 6)
        lnRsi     = add_spaces_to_sides(lnRsi, 1, 6)

        output_file.write(
                f"| {ti} | {Rmi} | {Rsi} | {Ti} | {one_by_Ti} | {lnRsi} |\n"
                )
    output_file.close()
    

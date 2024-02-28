import numpy as np
import matplotlib.pyplot as plot
from matplotlib.ticker import MaxNLocator, LinearLocator


files = ["3V.csv", "4V.csv", "5V.csv", "6V.csv", "7V.csv"]
plot_height = 20
plot_width = 30 #28
inch = 2.54
i = 1

for file in files:
    File = open(file)

    data = [line for line in File]
    xaxis = []
    yaxis = []

    for line in data:
        row = line.split('\t')
        xaxis.append(float(row[0]))
        yaxis.append(float(row[1]))

    Figure, Axes = plot.subplots()
    Figure.set_size_inches(plot_width/inch, plot_height/inch)

    Axes.minorticks_on()

    Axes.set(xlim=(0, 2.8), ylim=(80, 720))
    Axes.xaxis.set_major_locator(MaxNLocator(plot_width))
    Axes.yaxis.set_major_locator(MaxNLocator(plot_height))
#    Axes.set_xticks([0, 2.8, 0.1])
#    Axes.set_yticks([75, 725, 25]
    Axes.xaxis.set_minor_locator(LinearLocator(plot_width*10))
    Axes.yaxis.set_minor_locator(LinearLocator(plot_height*10))

    Axes.grid(which='major', color='c', lw = 1)
    Axes.grid(which='minor', color='c', lw = 0.25)

    title_start = "Рис."+str(i)+" График зависимости "
    title_end = " При "+ r'$U_a$ = '+ files[i-1][0] + "B"
    Axes.set_title(title_start + r'$I_a (I_L)$'+title_end)
    i+=1

    plot.plot(xaxis, yaxis, 'o', markerfacecolor='k', color='w')

#    plot.grid(color='c')

    xlinspaced = np.linspace(min(xaxis), max(xaxis), 2800)
    yinterpolated = np.interp(xlinspaced, xaxis, yaxis)

    plot.plot(xlinspaced, yinterpolated, color='k', alpha=0.5)
#    plot.plot(xaxis, yaxis, color='r', alpha=0.5)


    File.close()


plot.show()

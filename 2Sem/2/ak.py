import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.array([i for i in range(10)])
    plt.plot(x, 3*x)
    plt.show()

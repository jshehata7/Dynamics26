import numpy as np
import matplotlib.pyplot as plt

n = 1000
alpha = np.random.uniform(0, 1)

def W(x, al):
    return 2**(-n * al) * np.cos(x*(2**n))

x = np.linspace(-np.pi, np.pi, 100)

plt.plot(x, W(x, alpha))

plt.show()
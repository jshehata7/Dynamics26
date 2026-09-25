import numpy as np
import matplotlib.pyplot as plt

# Goal: T(f0) => T(T(f0)) => ... T(...(f0)) = 0

def T(lam, x, y, g): 
    result = np.zeros(M)
    for j in range(M):
        result[j] = np.sin(2*np.pi*x[j]) + lam * np.trapezoid(g / (1 + (x[j]-y)**2), y)
    return result

M = 100
iter = 10
lams = np.linspace(0, 1, 9)

fn = [
    lambda y: y * 0, 
    lambda y: np.sin(y), 
    lambda y: y * 1
]
labels = [
    "0",
    "sin(y)",
    "y"
]

for z in range(len(fn)):

    all_errors = []
    f = fn[z]
    for k in range(lams.size):

        errors = []
        lam = lams[k]
        tol = 1e-6
        x = np.linspace(-1, 1, M)
        y = np.linspace(-1, 1, M)

        i = 0
        hprev = f(y)
        while(i < iter):

            h = T(lam, x, y, hprev)
            # print(h)
            # print(hprev)
            # print(h.shape)
            # print(hprev.shape)

            errors.append(np.max(np.abs(h - hprev)))
            if (np.max(np.abs(h - hprev)) < tol):
                break
            else:
                hprev = h
                i += 1

        all_errors.append(errors)

    for k in range(len(all_errors)):
        plt.semilogy(all_errors[k], label=f"lambda={lams[k]:.2f}")

    plt.xlabel('Iteration number (n)')
    plt.ylabel('Error in sup-norm')
    plt.title(f'f(y) = {labels[z]}')
    plt.legend()
    plt.show()
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def tokamak(t, v, m, p):
    x,y = v
    dx = 0 if x < 0 else ((1 - m*x)*(x**(3/2)) - (x**(1/2))*y)
    dy = p*(x-1)*y

    return [dx, dy]

p, q = 20, 1/4
v0 = 1,1
t_span = (0, 1000)
t_eval = np.linspace(*t_span, 100000)

t_sol = np.array(0)
params = p, q



x_c0 = np.array(0)
y_c0 = np.array(0)

sol = solve_ivp(
    tokamak, t_span, v0,
    args=params,
    t_eval=t_eval, rtol=1e-9, atol=1e-12, method='Radau'
)

# print(sol)
plt.plot(sol.y[0], sol.y[1])
plt.show()
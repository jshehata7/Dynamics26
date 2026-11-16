
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def tokamak(t, v, p, q):
    x,y = v
    dx = 0 if x < 0 else ((1 - q*x)*(x**(3/2)) - (x**(1/2))*y)
    dy = p*(x-1)*y
    return [dx, dy]

p, q = 100, 1/4
v0 = 1,1
t_span = (0, 30)
t_eval = np.linspace(*t_span, 5000)
params = p, q

sol = solve_ivp(
    tokamak, t_span, v0,
    args=params,
    t_eval=t_eval, 
    atol=[1e-10, 1e-60]
)
# print(sol.status, sol.message)

plt.plot(sol.t, sol.y[0])
plt.xlabel('t')
plt.ylabel('x(t)')
plt.suptitle(rf'1e: Sawtooth Oscillations ($\rho = {p}$)')
plt.show()

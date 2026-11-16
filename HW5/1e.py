
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
t_eval = np.linspace(*t_span, 50000)
params = p, q

sol = solve_ivp(
    tokamak, t_span, v0,
    args=params,
    t_eval=t_eval, 
    atol=[1e-10, 1e-60]
)
# print(sol.status, sol.message)

fig = plt.figure(figsize=(12,5))

ax1 = fig.add_subplot(1,2,1)   
ax1.plot(sol.t, sol.y[0])
ax1.set_xlabel('t')
ax1.set_ylabel('x(t)')
ax1.set_title(rf'Sawtooth Oscillations')

ax2 = fig.add_subplot(1,2,2)
ax2.plot(sol.y[0], sol.y[1])
ax2.set_xlabel('x(t)')
ax2.set_ylabel('y(t)')
ax2.set_title(rf'Phase Portrait')

fig.suptitle(rf"1e: Tomalak ($\rho = {p}$)")
plt.show()

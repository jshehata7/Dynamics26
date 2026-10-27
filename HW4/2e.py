import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.integrate import solve_ivp

# Watt centrifugal governor system
def vishnegradskii(t, v, a, b, c):
    x,y,z = v
    dx = y
    dy = np.sin(x)*(z**2 * np.cos(x) - 1) - c*y
    dz = a*(np.cos(x) - b)

    return [dx, dy, dz]

# a = alpha, b = beta, c = epsilon, v0 = initial condition, t_eval = times to evaluate ODE
delta = 0.01

a, b = 2, 0.5
c0 = 2*a*b*np.sqrt(b)
mults = [0.55, 0.7, 0.85, 1.0, 1.15, 1.3, 1.45]

# v0 = np.array([np.arccos(b), 0, np.sqrt(1/b)])  ---> don't use equilibrium as initial condition
v0 = 1,1,1
t_span = (0, 1000)
t_eval = np.linspace(*t_span, 100000) 

sols = []
t_sol = np.array(0)
x_sols = []
y_sols = []
z_sols = []

x_c0 = np.array(0)
y_c0 = np.array(0)
z_c0 = np.array(0)

for m in mults:
    params = a, b, c0*m
    sol = solve_ivp(
            vishnegradskii, t_span, v0,
            args=params,
            t_eval=t_eval, rtol=1e-9, atol=1e-12, method="DOP853"
        )

    # Save c0 seperately & together
    if (m == 1.0):
        x_c0 = sol.y[0,:]
        y_c0 = sol.y[1,:]
        z_c0 = sol.y[2,:]
        t_sol = sol.t

    x_sol = sol.y[0,:]
    y_sol = sol.y[1,:]
    z_sol = sol.y[2,:]
    sols.append(sol)
    x_sols.append(x_sol)
    y_sols.append(y_sol)
    z_sols.append(z_sol)

n = len(sols)

# 2e_i
fig1 = plt.figure(figsize=(16, 5), constrained_layout=True)
ax = fig1.add_subplot(1,3,1)
ay = fig1.add_subplot(1,3,2)
az = fig1.add_subplot(1,3,3)

colors = plt.cm.coolwarm(np.linspace(0, 1, n))  # blue (small ε) -> red (large ε)

for i in range(n):
    eps = c0 * mults[i]
    is_c0 = np.isclose(mults[i], 1.0)

    # Label with ε value and the multiplier; make the c0 curve stand out
    label = rf"$\varepsilon = {eps:.3f}$ ({mults[i]:.2f}$\varepsilon_0$)" + (r" = $\varepsilon_0$" if is_c0 else "")
    lw = 2.5 if is_c0 else 1.2

    ax.plot(t_sol, x_sols[i], color=colors[i], lw=lw, label=label)
    ay.plot(t_sol, y_sols[i], color=colors[i], lw=lw)
    az.plot(t_sol, z_sols[i], color=colors[i], lw=lw)

ax.set_title("x(t)")
ay.set_title("y(t)")
az.set_title("z(t)")
for a_ in (ax, ay, az):
    a_.set_xlabel("t")
    a_.grid(alpha=0.3)

handles, labels = ax.get_legend_handles_labels()
fig1.suptitle(r"2e: Unstable equilibrium as $\varepsilon$ decreases through $\varepsilon_0$", fontsize=14)
fig1.legend(handles, labels, loc="outside right center", title=r"$\varepsilon$ (blue = below $\varepsilon_0$)")


# 2e_ii
fig2 = plt.figure(figsize=(12, 5))
a2 = fig2.add_subplot(1,1,1, projection='3d') # Enters the 3D domain
a2.plot(x_sols[3], y_sols[3], z_sols[3], color='purple', label='3D Line')

a2.set_xlabel('X Axis')
a2.set_ylabel('Y Axis')
a2.set_zlabel('Z Axis')
a2.set_title('2e: Attracting Limit Cycle')

plt.show()
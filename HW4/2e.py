import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from scipy.integrate import solve_ivp

# Watt centrifugal governor system
def vishnegradskii(t, v, a, b, c):
    x,y,z = v
    dx = y
    dy = np.sin(x)*(z**2 * np.cos(x) - 1) - c*y
    dz = a*(np.cos(x) - b)

    return [dx, dy, dz]

# a = alpha, b = beta, c = epsilon, v0 = initial condition, t_eval = times to evaluate ODE
rng = np.random.default_rng()
delta = 0.01

a, b = 2, 0.5
c0 = 2*a*b*np.sqrt(b)
mults = [0.5, 0.7, 0.85, 0.95, 1.0, 1.05, 1.15, 1.3, 1.5]

v0 = np.array([np.arccos(b), 0, np.sqrt(1/b)]) + delta
t_span = (0, 1000)
t_eval = np.linspace(*t_span, 1000) 

sols = {}

for m in mults:
    c = m*c0
    params = a, b, c

    sol = solve_ivp(
        vishnegradskii, t_span, v0,
        args=params,
        t_eval=t_eval
    )
    if (sol.success):
        sols.update({c: sol})

# ---- plotting: all ε on one set of x, y, z panels ----
norm = colors.TwoSlopeNorm(vcenter=1, vmin=min(mults), vmax=max(mults))
cmap = cm.coolwarm                           # blue = below ε₀, red = above

fig, axs = plt.subplots(1, 3, figsize=(16, 4), sharex=True)

for m, sol in sols.items():

    for k, ax in enumerate(axs):
        ax.plot(sol.t, sol.y[k], color=cmap(norm(m)), lw=1)

for ax, name in zip(axs, ['x', 'y', 'z']):
    ax.set_title(f'{name} vs t')
    ax.set_xlabel('t')
    ax.set_ylabel(name)

sm = cm.ScalarMappable(norm=norm, cmap=cmap)
fig.colorbar(sm, ax=axs, label='ε / ε₀')
fig.canvas.manager.set_window_title("As ε decreases through ε₀, Equilibrium Becomes Unstable")
plt.show()


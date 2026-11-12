import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import root

def rossler(t, s, a, b, c):
    x, y, z = s
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x-c)
    return [dx, dy, dz]

def cross_section(t, s, a, b, c):
    x, y, z = s
    return y

def ivp_solver(ic):

    t = (0, 30)
    return solve_ivp(
        rossler, t, ic,
        args=params,
        t_eval=np.linspace(*t, 500),
        rtol = 1e-9
    ).y

cross_section.direction = -1

s0 = (1,1,1)
a,b,c  = 0.2, 0.2, 5.7
params = a,b,c
t_span = (0, 1500)
t_eval = np.linspace(*t_span, 100000) 

sol = solve_ivp(
    rossler, t_span, s0,
    args=params,
    t_eval=t_eval,
    events=cross_section
)

# -31500:0 chooses the tail points starting from the end -- ignores the effects of the "transient"
x,y,z = sol.y[:, -30000:]
xN,yN,zN = sol.y_events[0].T[:, -250:]

xn  = xN[:-1]
xn_1 = xN[1:]

Qcof = np.polyfit(xN, zN, 10)
Pcof = np.polyfit(xn, xn_1, 10)
Qfit = np.polyval(Qcof, xN)
Pfit = np.polyval(Pcof, xn)

P = lambda x: np.polyval(Pcof, x)
P1 = lambda x: P(x) - x              # P(x) - x
P2 = lambda x: P(P(x)) - x           # P(P(x)) - x
P3 = lambda x: P(P(P(x))) - x        # P(P(P(x))) - x

# Find x0 guesses
x_span = np.linspace(min(xN), max(xN), 1000)
plt.plot(x_span, P1(x_span), label='P1')
plt.plot(x_span, P2(x_span), label='P2')
plt.plot(x_span, P3(x_span), label='P3')
plt.plot(x_span, np.linspace(0, 0, 1000), label ='x=0')
plt.legend()
plt.show()

x1_0 = -7.2
x2_0 = [-8.2, -4.7]
x3_0 = [-8.9, -8.6, -6.4, -5.3, -3.6, -2.9]
# x2_0 = [-8.2, -7.2, -4.7]
# x3_0 = [-8.9, -8.6, -7.2, -6.4, -5.3, -3.6, -2.9]

x1zeros = root(P1, x1_0).x
x2zeros = root(P2, x2_0).x
x3zeros = root(P3, x3_0).x
z1 = np.polyval(Qcof, x1zeros)
z2 = np.polyval(Qcof, x2zeros)
z3 = np.polyval(Qcof, x3zeros)

len2 = z2.size
len3 = z3.size

ic1 = (x1zeros[0], 0, z1[0])
ic2 = []
ic3 = []

for i in range(len2):
    ic2.append((x2zeros[i], 0, z2[i]))
for j in range(len3):
    ic3.append((x3zeros[j], 0, z3[j]))        

sol1 = ivp_solver(ic1)
sol2 = []
sol3 = []

for i in range(len2):
    sol2.append(ivp_solver(ic2[i]))
for j in range(len3):
    sol3.append(ivp_solver(ic3[j]))

# fig1 = plt.figure(figsize=(5, 5))
# fig2 = plt.figure(figsize=(12, 5))
# fig3 = plt.figure(figsize=(12, 5))
fig4 = plt.figure(figsize=(18, 5))

# # 2a
# ax1 = fig1.add_subplot(1,1,1, projection='3d')       # Enters the 3D domain
# ax1.plot(x, y, z, color='purple')
# ax1.set_xlabel('x')
# ax1.set_ylabel('y')
# ax1.set_zlabel('z')
# ax1.set_title('2a: Numeric Solution for Rossler System')

# # 2c
# ax2 = fig2.add_subplot(1,2,1)       
# ax2.scatter(xN, zN, color='purple', marker='*')
# ax2.set_xlabel('x')
# ax2.set_ylabel('z')
# ax2.set_title('2c: xn vs. zn')

# ax3 = fig2.add_subplot(1,2,2)      
# ax3.scatter(xn, xn_1, color='purple', marker='*')
# ax3.set_xlabel('x')
# ax3.set_ylabel('x')
# ax3.set_title('2c: xn vs. xn+1')

# # 2d
# ax4 = fig3.add_subplot(1,2,1)     
# ax4.scatter(xN, zN, color='purple', marker='*', label='zn')
# ax4.scatter(xN, Qfit, color='r', marker='*', label='Q(xn)')  
# ax4.set_xlabel('x')
# ax4.set_ylabel('z')
# ax4.set_title('xn vs. zn')
# ax4.legend()

# ax4 = fig3.add_subplot(1,2,2)  
# ax4.scatter(xn, xn_1, color='purple', marker='*', label='xn_1')
# ax4.scatter(xn, Pfit, color='r', marker='*', label='P(xn)')      
# ax4.set_xlabel('x')
# ax4.set_ylabel('x')
# ax4.set_title('xn vs. xn+1')
# ax4.legend()
# fig3.suptitle('2d: Interpolation (degree 10)')

# 2f
ax5 = fig4.add_subplot(1,3,1, projection='3d')       # Enters the 3D domain
ax5.plot(sol1[0], sol1[1], sol1[2])
ax5.set_xlabel('x')
ax5.set_ylabel('y')
ax5.set_zlabel('z')
ax5.set_title('Periodic Oscillations: Period = 1')

ax5 = fig4.add_subplot(1,3,2, projection='3d')       # Enters the 3D domain
for i in range(len2):
    ax5.plot(sol2[i][0], sol2[i][1], sol2[i][2])
ax5.set_xlabel('x')
ax5.set_ylabel('y')
ax5.set_zlabel('z')
ax5.set_title('Periodic Oscillations: Period = 2')

ax5 = fig4.add_subplot(1,3,3, projection='3d')       # Enters the 3D domain
for j in range(len3):
    ax5.plot(sol3[j][0], sol3[j][1], sol3[j][2])
ax5.set_xlabel('x')
ax5.set_ylabel('y')
ax5.set_zlabel('z')
ax5.set_title('Periodic Oscillations: Period = 3')

plt.show()

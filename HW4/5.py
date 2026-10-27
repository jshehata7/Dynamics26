import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def system(t, s, a, b, c):
    xD, yD, zD, xR, yR, zR = s

    eX = xR-xD
    eY = yR-yD
    eZ = zR-zD

    u1 = -eX + eZ
    u2 = -eY * (1+a)
    u3 = -eZ - (eX*zR + (xD-c)*eZ)

    # Driver
    dxD = -yD - zD
    dyD = xD + a*yD
    dzD = b + zD*(xD-c)

    # Response
    dxR = -yR - zR + u1
    dyR = xR + a*yR + u2
    dzR = b + zR*(xR-c) + u3

    return [dxD, dyD, dzD, dxR, dyR, dzR]

# eq = (5.693, 28.46, -28.46)
d0 = (1,1,1)
r0 = (5,5,5)
s0 = [*d0, *r0]

a,b,c  = 0.2, 0.2, 5.7
params = a,b,c
t_span = (0, 1000)
t_eval = np.linspace(*t_span, 100000) 

sol = solve_ivp(
    system, t_span, s0,
    args=params,
    t_eval=t_eval
)

x,y,z    = sol.y[0:3, -31500:]
xx,yy,zz = sol.y[3:6, -31500:]


fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(1,2,1, projection='3d') # Enters the 3D domain
ax1.plot(x, y, z, color='purple', label='3D Line')

ax1.set_xlabel('X Axis')
ax1.set_ylabel('Y Axis')
ax1.set_zlabel('Z Axis')
ax1.set_title('5a: Numeric Solution for Driver System')


ax2 = fig.add_subplot(1,2,2, projection='3d') # Enters the 3D domain
ax2.plot(xx, yy, zz, color='green', label='3D Line')

ax2.set_xlabel('X Axis')
ax2.set_ylabel('Y Axis')
ax2.set_zlabel('Z Axis')
ax2.set_title('5d: Numeric Solution for Response System')

plt.show()
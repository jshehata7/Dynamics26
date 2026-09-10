# With matplot
import numpy as np
import matplotlib.pyplot as plt

# Create grid of points
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Define functions (HERE, must set fn's to 0 (easy here as we're only interested in nullclines))
F1 = -Y + X*(1 - X**2 - Y**2)
F2 =  X + Y*(1 - X**2 - Y**2)

# Plot both on same axes using level 0 contour -- have to assign contours to variables so labels show up
plt.figure(figsize=(6, 6))
c1 = plt.contour(X, Y, F1, levels=[0], label='f1 = -y + x(1 - x^2 - y^2)', colors='red')
c2 = plt.contour(X, Y, F2, levels=[0], label='f2 =  x + y(1 - x^2 - y^2)', colors='blue')

# Fix styling
plt.grid(True, linestyle='--', alpha=0.6)       # Adds grid background
plt.axhline(0, color='black', linewidth=0.5)    # Adds x-axis
plt.axvline(0, color='black', linewidth=0.5)    # Adds y-axis
plt.title("6c: Nullclines Plot")

# 'Proper Method -- Uses variable unpacking for contours'
# Extract the lables to make them appear
# h1, _ = c1.legend_elements()
# h2, _ = c2.legend_elements()

# Cleaner approach -- uses a dummy plot to create labels
plt.plot([], [], color='red', label='f1 = -y + x(1 - x^2 - y^2)')
plt.plot([], [], color='blue', label='f2 = -y + x(1 - x^2 - y^2)')

plt.legend(
    # Related to 'Proper' method
    # [h1[0], h2[0]], ['f1 = -y + x(1 - x^2 - y^2)', 'f2 = x + y(1 - x^2 - y^2)']
)
plt.show()



"""
# With sympy
from sympy import symbols, plot_implicit

# Define symbol variabls
x, y = symbols('x, y')

# Define (implicit) functions
f1 = -y + x*(1 - x**2 - y**2)
f2 =  x + y*(1 - x**2 - y**2)

# Set plots -- sympy won't show labels
p1 = plot_implicit(f1, (x, -5, 5), (y, -5, 5), line_color='red' , label = 'f1 = -y + x(1 - x^2 - y^2)', show=False)
p2 = plot_implicit(f2, (x, -5, 5), (y, -5, 5), line_color='blue', label = 'f2 =  x + y(1 - x^2 - y^2)', show=False)

# Combine plots
p1.extend(p2)
p1.title = 'Plots: f1 = red, f2 = blue (1 = top eqn, 2 = bottom eqn)'

# Render combined plot
p1.legend = True
p1.show()
"""
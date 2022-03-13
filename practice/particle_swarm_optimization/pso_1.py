"""
PSO algorithm inspired from the following blog: https://towardsdatascience.com/particle-swarm-optimization-visually-explained-46289eeb2e14

Date: 19/02/22
"""
from csv import writer
from pickle import OBJ
from timeit import repeat
from turtle import color
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ImageMagickWriter
import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    "Defines objective function"
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x**2)**2

# Compute and plit the function in 3D within [0.5,0.5]
x, y = np.array(np.meshgrid(np.linspace(-5,5,100), np.linspace(-5,5,100)))
z = f(x,y)

x_min = x.ravel()[z.argmin()]
y_min = y.ravel()[z.argmin()]

# Hyper-parameter of the algorithm
c1 = 0.1; c2 = 0.1
w = 0.9

# Create particles
n_particles = 20
np.random.seed(100)
X = np.random.rand(2, n_particles) * 5
V = np.random.randn(2, n_particles) * 0.1

# Initialize data
pbest = X
pbest_obj = f(X[0], X[1])
gbest = pbest[:, pbest_obj.argmin()]
gbest_obj = pbest_obj.min()

def update():
    "Funtion to do one iteration of particle swarm optimization"
    global V, X, pbest, pbest_obj, gbest, gbest_obj

    # Update paramters
    r1, r2 = np.random.rand(2)
    V = w * V + c1*r1*(pbest - X) + c2*r2*(gbest.reshape(-1,1) - X)
    X += V
    obj = f(X[0], X[1])
    pbest[:, (pbest_obj >= obj)] = X[:, (pbest_obj >= obj)]
    pbest_obj = np.array([pbest_obj, obj]).min(axis=0)
    gbest = pbest[:, pbest_obj.argmin()]
    gbest_obj = pbest_obj.min()

# Construct and plot contour plot
fig, ax = plt.subplots(figsize=(8,6))
fig.set_tight_layout(True)
img = ax.imshow(z, extent=[0, 5, 0, 5], origin='lower', cmap='viridis', alpha=0.5)
fig.colorbar(img, ax=ax)
ax.plot([x_min], [y_min], marker='x', markersize=5, color="white")
contours =  ax.contour(x, y, z, 10, colors='black', alpha=0.4)
ax.clabel(contours, inline=True, fontsize=8, fmt='%.0f')
pbest_plot = ax.scatter(pbest[0], pbest[1], marker='o', color='black', alpha=0.5)
p_plot = ax.scatter(X[0], X[1], marker='o', color='blue', alpha=0.5)
p_arrow = ax.quiver(X[0], X[1], V[0], V[1], color='blue', width=0.005, angles='xy', scale_units='xy', scale=1)
gbest_plot = plt.scatter([gbest[0]], [gbest[1]], marker='*', s=100, color='black', alpha=0.4)
ax.set_xlim([0,5])
ax.set_ylim([0,5])

def animate(i):
    "Steps of PSO: algorithm update and show in plot"
    title = 'Iteration {:02d}'.format(i)
    # Update params
    update()
    # Set picture
    ax.set_title(title)
    pbest_plot.set_offsets(pbest.T)
    p_plot.set_offsets(X.T)
    p_arrow.set_offsets(X.T)
    p_arrow.set_UVC(V[0], V[1])
    gbest_plot.set_offsets(gbest.reshape(1,-1))
    return ax, pbest_plot, p_plot, p_arrow, gbest_plot

anim = FuncAnimation(fig, animate, frames=list(range(1,50)), interval=500, blit=False, repeat=True)
plt.show()

print("PSO found best solution at f({}) = {}".format(gbest, gbest_obj))
print("Global optimal at f({}) = {}".format([x_min, y_min], f(x_min, y_min)))

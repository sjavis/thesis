#!/usr/bin/env python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mim
import matplotlib.patheffects as mpe
import json
import pyutils.latexify as lt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# Plot parameters
dt = 0.06
de = 0.02
ar = 0.9
ldx = 0#.008

cmap = 'Greys_r'
mec = 'k'
ms = 6
lw = 1.5
tau_len = 1.5


# Make potential
peaks = [[-3., -1.414, 0., 1., 1.],
         [-2., 1.414, 0., 1., 1.],
         [-1., 0.07, 1.25, 1., 1.],
         [-0.8, 0.12, -1.25, 1., 0.5],
         [0.5, 0.07, 0, 1., 1.]]
def energy(x, y):
    e = np.zeros_like(x)
    for peak in peaks:
        e += peak[0] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
    return e
def gradient(x, y):
    x = np.array(x)
    y = np.array(y)
    g = np.zeros((x.size, 2))
    for peak in peaks:
        g[:,0] -= peak[0] * 2*(x-peak[1])/peak[3] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
        g[:,1] -= peak[0] * 2*(y-peak[2])/peak[4] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
    return g

dx = 2.25
y0 = 0.2
xlim = (-dx, dx)
ylim = (y0-dx*ar, y0+dx*ar)
# xlim =[0.3,0.6]
# ylim =[0.6,1.3]
x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
e = energy(x, y)

# fig = plt.figure(frameon=False, figsize=0.8*np.array([xlim[1]-xlim[0], ylim[1]-ylim[0]]))
fig = lt.figure(0.3, ar, frameon=False)
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
plt.contourf(x, y, e, cmap=cmap, levels=10)
ax.set_xticks([])
ax.set_yticks([])


# Plot minima
min1 = np.array([-1.42, 0.048])
min2 = np.array([1.42, 0.048])
ts1 = [0.518, 0.98]
plt.scatter(min1[0], min1[1], c='b', s=50, zorder=2)
plt.scatter(min2[0], min2[1], c='b', s=50, zorder=2)
plt.scatter(ts1[0], ts1[1], c='r', s=50, zorder=2)
plt.plot([min1[0],min2[0]], [min1[1],min2[1]], 'k--', zorder=1)

# Circular arc
r = 1.8
x0 = (min1 + min2) / 2
h = np.sqrt(r**2 - np.linalg.norm(min1-min2)**2/4)
x0[1] = x0[1] + h
xarc = np.linspace(min1[0], min2[0], 100)
yarc_fn = lambda x: x0[1] - np.sqrt(r**2 - (x-x0[0])**2)
plt.plot(xarc, yarc_fn(xarc), 'k-', zorder=1)
plt.plot([ts1[0],ts1[0]], [ts1[1],yarc_fn(ts1[0])], 'k:', zorder=1)

plt.text(0.6, 0.3, '$d_0$')


plt.savefig(f'metric.png', dpi=500)
# plt.show()

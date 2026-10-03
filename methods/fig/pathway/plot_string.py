#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

import pyutils.latexify as lt
lt.update_width('thesis')

import sys; sys.path.insert(0, '..')
import style


def plot_energy(ax):
    x, y = np.mgrid[-1:1:51j, -1:1:51j]
    # e = 1 / ((x-0.6)**2 + 0.3*(y-0.4)**2 + 0.1)\
    #   + 1.5 / ((x+0.6)**2 + 0.3*(y-0.4)**2 + 0.1)\
    #   + 0.2 / ((x+0.6)**2 + 0.3*(y+0.4)**2 + 0.1)\
    #   + 0.2 / ((x-0.6)**2 + 0.3*(y+0.4)**2 + 0.1)\
    #   - 1   / (1*(x-0.05)**2 + 0.05*(y-0.6)**2 + 0.08)\
    #   - 0.5 / (5*(x-0.05)**2   + 0.5*(y+1.0)**2 + 0.1)
    r = np.sqrt(4*x**2 + (y-1)**2)
    r0 = 1.8
    dr = 0.5
    e = 1/(((r - r0)/dr)**2 + 1) + 1/((x-0.5)**2+(y-0.4)**2 + 1) + 1.3/((x+0.5)**2+(y-0.4)**2 + 1) - 1/(x**2+(y-0.4)**2 + 1)
    # e = ((r - r0)/dr)**2 + 1/((x-0.7)**2+(y-0.4)**2 + 1) + 1/((x+0.7)**2+(y-0.4)**2 + 1)
    ax.contourf(x, y, e, cmap='gray')
    ax.set_xticks([])
    ax.set_yticks([])


def plot_string(ax):
    x1 = np.array([-0.82, 0.38])
    x2 = np.array([ 0.82, 0.38])
    t = np.linspace(0, 1, 5)
    string1 = x1*(1-t[:,np.newaxis]) + x2*t[:,np.newaxis]
    ax.plot([x1[0],x2[0]], [x1[1],x2[1]], 'ko--')
    ax.plot(string1[1:-1,0], string1[1:-1,1], ls='none', marker='o', c=style.c0)

    t2 = np.array([0, 0.15, 0.5, 0.85, 1])
    string2 = np.zeros((len(t2), 2))
    string2[:,0] = string1[:,0]
    string2[:,1] = string1[:,1] - 0.6*(1-4*(t2-0.5)**2)
    n_interp = 41
    t_interp = np.linspace(0, 1, n_interp)
    s2_interp = x1*(1-t_interp[:,np.newaxis]) + x2*t_interp[:,np.newaxis]
    s2_interp[:,1] = s2_interp[:,1] - 0.6*(1-4*(t_interp-0.5)**2)
    string2 = s2_interp[[0, int(0.2*n_interp), int(0.5*n_interp), int(0.8*n_interp), -1]]
    ax.plot(s2_interp[:,0], s2_interp[:,1], 'k--')
    ax.plot(string2[1:-1,0], string2[1:-1,1], ls='none', marker='o', c=style.c1)

    dstring = np.array([[ 0.00, 0.00],
                        [-0.28,-0.18],
                        [-0.38,-0.45],
                        [ 0.28,-0.18],
                        [ 0.00, 0.00]])
    for i in np.arange(1, len(string1)-1):
        ax.arrow(string1[i,0], string1[i,1], dstring[i,0], dstring[i,1], width=0.02, color='k', length_includes_head=True)
        base = string1[i] + dstring[i]
        diff = string2[i] - base
        ax.arrow(base[0], base[1], diff[0], diff[1], width=0.02, color='k', length_includes_head=True)


w = 0.4
h = 0.4
fig = lt.figure(w, h/w)
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])

plot_energy(ax)
plot_string(ax)

plt.savefig('string.png', dpi=500)

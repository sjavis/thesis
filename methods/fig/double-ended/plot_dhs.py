#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

import pyutils.latexify as lt
lt.update_width('thesis')

import sys; sys.path.insert(0, '..')
import style


def plot_energy(ax):
    x, y = np.mgrid[-1:1:51j, -1:1:51j]
    r = np.sqrt(4*x**2 + (y-1)**2)
    r0 = 1.8
    dr = 0.5
    e = 1.0 / (((r - r0)/dr)**2 + 1) \
      + 1.0 / ((x-0.5)**2 + (y-0.4)**2 + 1) \
      + 1.3 / ((x+0.5)**2 + (y-0.4)**2 + 1) \
      - 1.0 / (x**2       + (y-0.4)**2 + 1)
    ax.contourf(x, y, e, cmap='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')


def plot_dhs(ax):
    x1 = np.array([-0.82, 0.38])
    x2 = np.array([ 0.82, 0.38])
    dr1 = [0.1, 0.1, 0.1]
    dr2 = [0.2, 0.1, 0.2]
    theta1 = [20, 15, 15]
    theta2 = [-20, -15, -15]
    x1_path = np.zeros((len(theta1)+1, 2))
    x2_path = np.zeros((len(theta2)+1, 2))
    x1d_path = np.zeros((len(theta1), 2))
    x2d_path = np.zeros((len(theta2), 2))
    x1_path[0] = x1
    x2_path[0] = x2
    for i in range(len(theta1)):
        x1d_path[i] = x2_path[i] + (1-dr1[i])*(x1_path[i] - x2_path[i])
        rot_mat1 = np.array([[np.cos(theta1[i]*np.pi/180), -np.sin(theta1[i]*np.pi/180)], [np.sin(theta1[i]*np.pi/180), np.cos(theta1[i]*np.pi/180)]])
        x1_path[i+1] = np.matmul(rot_mat1, x1d_path[i]-x2_path[i]) + x2_path[i]
        x2d_path[i] = x1_path[i+1] + (1-dr2[i])*(x2_path[i] - x1_path[i+1])
        rot_mat2 = np.array([[np.cos(theta2[i]*np.pi/180), -np.sin(theta2[i]*np.pi/180)], [np.sin(theta2[i]*np.pi/180), np.cos(theta2[i]*np.pi/180)]])
        x2_path[i+1] = np.matmul(rot_mat2, x2d_path[i]-x1_path[i+1]) + x1_path[i+1]
    for i in range(len(theta1)):
        plt.plot([x1_path[i,0],x2_path[i,0],x1_path[i+1,0]], [x1_path[i,1],x2_path[i,1],x1_path[i+1,1]], 'k--')
        r = np.linalg.norm(x1d_path[i]-x2_path[i]) / 10
        ax.add_patch(FancyArrowPatch(x1d_path[i], x1_path[i+1], connectionstyle=f'arc3,rad={r}', arrowstyle=f'Simple, tail_width=1, head_width=4, head_length=8', color='k'))
        r = np.linalg.norm(x2d_path[i]-x1_path[i+1]) / 10
        ax.add_patch(FancyArrowPatch(x2d_path[i], x2_path[i+1], connectionstyle=f'arc3,rad={-r}', arrowstyle=f'Simple, tail_width=1, head_width=4, head_length=8', color='k'))
    plt.plot([x1_path[-1,0],x2_path[-1,0]], [x1_path[-1,1],x2_path[-1,1]], 'k--')
    plt.plot(x1_path[:,0], x1_path[:,1], marker='o', ls='none', c=style.c0)
    plt.plot(x2_path[:,0], x2_path[:,1], marker='o', ls='none', c=style.c1)


w = 0.4
h = 0.4
fig = lt.figure(w, h/w)
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])

plot_energy(ax)
plot_dhs(ax)

plt.savefig('dhs.png', dpi=500)

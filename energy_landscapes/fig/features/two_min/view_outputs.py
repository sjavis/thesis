#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


def energy(x, y, peaks):
    e = 0
    for peak in peaks:
        dx = (x - peak[1]) / peak[3]
        dy = (y - peak[2]) / peak[4]
        e += peak[0] * np.exp(-dx**2 - dy**2);
    return e


def plot_energy(peaksfile, xlim, ylim, ax=plt.gca()):
    peaks = np.loadtxt(peaksfile, skiprows=1)
    x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
    e = energy(x, y, peaks)
    ax.contourf(x, y, e, cmap='gray')
    ax.set_aspect('equal')

def plot_path(pathfile):
    path = np.loadtxt(pathfile)
    plt.plot(path[:,0], path[:,1], c='r', marker='s', mec='k')

xlim = [-2, 2]
ylim = [-0.8, 1.3]
plot_energy('peaks.txt', xlim, ylim)
plot_path('path.txt')
plt.show()

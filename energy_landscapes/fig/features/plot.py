#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
import pyutils.latexify as lt


def energy(x, y, peaks):
    e = 0
    for peak in peaks:
        dx = (x - peak[1]) / peak[3]
        dy = (y - peak[2]) / peak[4]
        e += peak[0] * np.exp(-dx**2 - dy**2);
    return e


def plot_energy(direc, lim, ax=None):
    if (ax is None): ax = plt.gca()
    peaks = np.loadtxt(direc+'/peaks.txt', skiprows=1)
    xlim, ylim = lim
    x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
    e = energy(x, y, peaks)
    cnt = ax.contourf(x, y, e, cmap='gray')
    for c in cnt.collections:
        c.set_edgecolor('face')
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

def plot_features(direc, ax=None):
    if (ax is None): ax = plt.gca()
    pathfile = direc + '/path.txt'
    minfile = direc + '/minima.txt'
    tsfile = direc + '/transitions.txt'
    if (os.path.exists(pathfile)):
        path = np.loadtxt(pathfile, ndmin=2)
        ax.plot(path[:,0], path[:,1], ls='-', c='k')
        ax.plot(path[:,0], path[:,1], ls='-', c='w')
    if (os.path.exists(minfile)):
        minima = np.loadtxt(minfile, ndmin=2)
        ax.plot(minima[:,0], minima[:,1], ls='none', marker='o', c='tab:blue')
    if (os.path.exists(tsfile)):
        ts = np.loadtxt(tsfile, ndmin=2)
        ax.plot(ts[:,0], ts[:,1], ls='none', marker='s', c='tab:red')

d0 = 0.01
dh = 0.04
dw = 0.06
wa = 0.56
wb = 0.56
wc = 0.36
ha = 0.35
hb = 0.35
hc = ha + hb + dh
w = 2*d0 + 2*dw + wa + wc
h = 2*d0 + hc
xa = d0 + dw
xb = d0 + dw
xc = d0 + 2*dw + wa
ya = d0 + dh + hb
yb = d0
yc = d0

fig = lt.figure(0.65, h/w)

fig.text(xa/w, (ya+ha)/h, '(a)', ha='right', va='top')
axa = plt.axes((xa/w, ya/h, wa/w, ha/h))
alim = [[-2, 2], [-1, 1.5]]
plot_energy('two_min', alim, axa)
plot_features('two_min', axa)

fig.text(xb/w, (yb+hb)/h, '(b)', ha='right', va='top')
axb = plt.axes((xb/w, yb/h, wb/w, hb/h))
blim = [[-2.7, 2.1], [-1.5, 1.5]]
plot_energy('bifurcation', blim, axb)
plot_features('bifurcation', axb)

fig.text(xc/w, (yc+hc)/h, '(c)', ha='right', va='top')
axc = plt.axes((xc/w, yc/h, wc/w, hc/h))
cdx = 2.8
cx0 = 0.1
cdy = cdx * hc/wc
clim = [[-cdx/2-cx0, cdx/2-cx0], [-cdy/2, cdy/2]]
plot_energy('multi_step', clim, axc)
plot_features('multi_step', axc)

lt.savefig('../features.pdf', fig)

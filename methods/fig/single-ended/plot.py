#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

import pyutils.latexify as lt
lt.update_width('thesis')

import sys; sys.path.insert(0, '..')
import style


def plot_ci(ax=None):
    if (ax is None): ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    
    kx = 1
    ky = 1
    tau_theta = 20
    e_fn = lambda x, y: kx*x**2 - ky*y**2
    g_fn = lambda x, y: np.array([2*kx*x, -2*ky*y])
    x, y = np.mgrid[-1:1:21j, -1:1:21j]
    e = e_fn(x, y)
    cnt = ax.contourf(x, y, e, cmap='gray')
    for c in cnt.collections:
        c.set_edgecolor("face")

    x_ar, y_ar = np.mgrid[-1:1:10j, -1:1:10j]
    g = g_fn(x_ar, y_ar)
    tau = np.array([-np.sin(tau_theta*np.pi/180), np.cos(tau_theta*np.pi/180)])
    f = - g + 2*(g[0]*tau[0] + g[1]*tau[1])*tau[:,np.newaxis,np.newaxis]
    f_dir = f / np.linalg.norm(f, axis=0)
    ax.quiver(x_ar, y_ar, f_dir[0], f_dir[1], color='k', scale=15)
    
    dtau = 0.8 * tau
    tau0 = -dtau/2
    ctau = style.c0
    ax.arrow(tau0[0], tau0[1], dtau[0], dtau[1], width=0.02, length_includes_head=True, color=ctau)
    ax.text(dtau[0]/2, dtau[1]/2, r'$\bm{\hat{\tau}}$', c=ctau, fontsize=12)


def plot_dimer(ax=None):
    if (ax is None): ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])

    xc = 1.5
    yc = -2
    dx = 1
    dy = 1
    e_fn = lambda x, y: (x/dx+xc)**2 - (y/dy+yc)**2
    g_fn = lambda x, y: np.array([2/dx*(x/dx+xc), -2/dy*(y/dy+yc)])
    x, y = np.mgrid[-1:1:21j, -1:1:21j]
    e = e_fn(x, y)
    cnt = ax.contourf(x, y, e, cmap='gray')
    for c in cnt.collections:
        c.set_edgecolor("face")

    tau = np.array([-0.5, 0.5])
    x0 = np.array([0,0])
    x1 = tau
    x2 = -tau
    ax.plot([x1[0],x2[0]], [x1[1],x2[1]], 'k-o', ms=10)
    ax.plot(x0[0], x0[1], 'ko', ms=5)
    ax.text(x0[0]+0.05, x0[1]+0.05, r'$\bm{x}_0$', c='k', fontsize=12)
    ax.text(x1[0]-0.25, x1[1]+0.1 , r'$\bm{x}_1$', c='k', fontsize=12)
    ax.text(x2[0]+0.1 , x2[1]+0.05, r'$\bm{x}_2$', c='k', fontsize=12)

    fscale = 15
    f0 = -g_fn(x0[0], x0[1]) / fscale
    f1 = -g_fn(x1[0], x1[1]) / fscale
    f2 = -g_fn(x2[0], x2[1]) / fscale
    ar_width = 0.02
    ar_color = style.c0
    ax.arrow(x0[0], x0[1], f0[0], f0[1], width=ar_width, color=ar_color)
    ax.arrow(x1[0], x1[1], f1[0], f1[1], width=ar_width, color=ar_color)
    ax.arrow(x2[0], x2[1], f2[0], f2[1], width=ar_width, color=ar_color)
    ax.text(x0[0]+f0[0], x0[1]+f0[1]+0.1 , r'$\bm{F}_0$', c=ar_color, fontsize=12, ha='right')
    ax.text(x1[0]+f1[0], x1[1]+f1[1]-0.05, r'$\bm{F}_1$', c=ar_color, fontsize=12, va='top')
    ax.text(x2[0]+f2[0], x2[1]+f2[1]+0.1 , r'$\bm{F}_2$', c=ar_color, fontsize=12, ha='right')

    fr = (f1 - f2) - tau * np.dot(f1-f2, tau) / (tau[0]**2 + tau[1]**2)
    fr_color = style.c1
    ax.arrow(x1[0], x1[1], fr[0], fr[1], width=ar_width, color=fr_color)
    ax.text(x1[0]+fr[0]+0.1, x1[1]+fr[1], r'$\bm{F}_\mathrm{R}$', c=fr_color, fontsize=12)


w = 0.4
h = w
dw = 0.49 - w
dh = 0.01
wtot = 1
htot = h + 2*dh

fig = lt.figure(0.8, htot/wtot)
ax1 = fig.add_axes([dw/wtot, dh/htot, w/wtot, h/htot])
ax2 = fig.add_axes([(2*dw+w)/wtot, dh/htot, w/wtot, h/htot])
fig.text(0.5*dw/wtot, 1, '(a)', ha='center', va='top')
fig.text(0.5*(1+dw)/wtot, 1, '(b)', ha='center', va='top')

plot_ci(ax1)
plot_dimer(ax2)
lt.savefig('../single-ended.pdf')

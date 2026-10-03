#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyutils.mpl_ext import autoscale_based_on
import pyutils.latexify as lt
lt.update_width('thesis')


def plot_liquid(ax, state):
    grid = [90, 1, 90]
    grid_cutoff = int(0.66*grid[2])
    s = np.s_[:,int(grid[1]/2)]
    phi = np.loadtxt(f"data/{state.lower().replace(' ','')}.txt").reshape(grid)
    solid = np.loadtxt("data/solid.txt").reshape(grid)
    phi = phi[:,:,1:grid_cutoff]
    solid = solid[:,:,[0]]
    solid_extent = [-0.5, grid[0]-0.5, -3, 0]
    ax.imshow(phi[s].T, origin='lower', cmap='Blues')
    ax.imshow(solid[s].T, origin='lower', extent=solid_extent, cmap='gray')
    ax.contour(phi[s].T, levels=[0], colors='k')
    ax.axhline(0, c='k', lw=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.annotate(state, [0.5*grid[0],0.9*grid_cutoff], ha='center', va='top')


def load_times(method):
    df = pd.read_csv('data/times.txt', sep='\t', index_col=0)
    n = df.columns.to_numpy(dtype=float)
    times = df.loc[method].to_numpy()
    speedup = times[0] / times
    return n, speedup


def plot_speedup(ax, methods):
    colors = ['C0', 'C1', 'C2', 'C3']
    lines = []
    for i in range(len(methods)):
        nproc, speedup = load_times(methods[i])
        lines.append( ax.plot(nproc, speedup, c=colors[i], label=f'\\texttt{{{methods[i]}}}')[0] )
    ax.plot(nproc, nproc, 'k--', zorder=0)
    # autoscale_based_on(ax, lines)
    ax.legend(loc='best', framealpha=0)
    ax.loglog()
    ax.set_xlabel('$N$')


fig = lt.figure(1, 0.6)
h1 = 0.38
h2 = 0.56
gs1 = fig.add_gridspec(1, 3, left=0.05, right=0.99, bottom=1-h1, top=1, wspace=0.1)
gs2 = fig.add_gridspec(1, 3, left=0.1, right=0.99, bottom=0.1, top=h2, wspace=0.15)

ax_a1 = fig.add_subplot(gs1[0,0])
ax_a2 = fig.add_subplot(gs1[0,1])
ax_a3 = fig.add_subplot(gs1[0,2])
plot_liquid(ax_a1, 'State 1')
plot_liquid(ax_a2, 'TS')
plot_liquid(ax_a3, 'State 2')

ax_b = fig.add_subplot(gs2[0,0])
ax_c = fig.add_subplot(gs2[0,1])
ax_d = fig.add_subplot(gs2[0,2])
plot_speedup(ax_b, ["blockGradient", "procGradient", "gradient", "energy"])
plot_speedup(ax_c, ["GradDescent", "Lbfgs", "Fire", "Anneal"])
plot_speedup(ax_d, ["Bitss", "Neb-4", "Neb-16"])
ax_b.set_ylabel('Speed up')
ax_c.set_yticklabels([])
ax_d.set_yticklabels([])

# Subfig labels
fig.text(0.01, 1-0.02, '(a)', ha='left', va='top')
fig.text(0.02, h2, '(b)', ha='left', va='bottom')
fig.text(0.38, h2, '(c)', ha='left', va='bottom')
fig.text(0.687, h2, '(d)', ha='left', va='bottom')

# plt.show()
lt.savefig('../parallel.pdf', dpi=500)

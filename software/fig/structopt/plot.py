#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
import pyutils.latexify as lt
lt.update_width('thesis')

def schematic(ax):
    w = 0.15
    r = 0.5
    r_in = 0.3
    l_bond = 0.1
    lw = 0.5
    # Get outline
    t0 = np.arcsin(w/r)
    tarc = np.linspace(t0, np.pi/2-t0, 20)
    xarc = r * np.cos(tarc)
    yarc = r * np.sin(tarc)
    xtr = np.concatenate([[1], xarc, [w]])
    ytr = np.concatenate([[w], yarc, [1]])
    xout = np.concatenate([xtr, -ytr, -xtr,  ytr, [xtr[0]]])
    yout = np.concatenate([ytr,  xtr, -ytr, -xtr, [ytr[0]]])
    # Inner ring
    t = np.linspace(0, 2*np.pi, 40)
    xin = r_in * np.cos(t)
    yin = r_in * np.sin(t)
    # Bonding sites
    for ibond in range(4):
        x0 = (1-l_bond)*np.cos(ibond*np.pi/2) + w*np.sin(ibond*np.pi/2)
        y0 = (1-l_bond)*np.sin(ibond*np.pi/2) - w*np.cos(ibond*np.pi/2)
        rect = patches.Rectangle([x0,y0], l_bond, 2*w, fc='grey', angle=90*ibond)
        ax.add_patch(rect)
    # Plot
    ax.plot(xout, yout, lw=lw, c='k')
    ax.plot(xin,  yin,  lw=lw, c='k')
    # Labels
    arrow_args = {'arrowstyle':'<->', 'shrinkA':0, 'shrinkB':0}
    ax.annotate('$t$', [0,0.5*(1-l_bond+r)], ha='center', va='center')
    ax.annotate('', [1-2*l_bond,-w], [1-2*l_bond,w], arrowprops=arrow_args)
    ax.annotate('$w$', [1-3*l_bond,0], ha='right', va='center')
    ax.annotate('', [0,0], [r_in,0], arrowprops=arrow_args)
    ax.annotate(r'$r_\mathrm{in}$', [r_in/2,-0.02], ha='center', va='top')
    ax.annotate('', [0,0], [-r/1.414,r/1.414], arrowprops=arrow_args)
    ax.annotate(r'$r_\mathrm{out}$', [-r/2.3,r/2.7], ha='left', va='bottom')
    # Axes
    ax.set_axis_off()
    ax.set_aspect('equal')


def show_state(ax, state, tri):
    view = 15 * np.pi/180
    x = state[:,0]*np.cos(view) - state[:,1]*np.sin(view)
    y = state[:,0]*np.sin(view) + state[:,1]*np.cos(view)
    z = state[:,2]
    ax.plot_trisurf(x, y, z, triangles=tri, cmap=plt.cm.coolwarm, vmin=-0.2, vmax=0.2)
    ax.view_init(15, 0)
    ax.set_axis_off()
    ax.patch.set_alpha(0)
    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))


def initial_structure(axes):
    states = np.loadtxt('data/state1/states.txt').reshape([3,-1,3])
    tri = np.loadtxt('data/state1/tlist.txt')
    show_state(axes[0], states[0], tri)
    show_state(axes[1], states[1], tri)


def final_structure(axes):
    states = np.loadtxt('data/state2/states.txt').reshape([3,-1,3])
    tri = np.loadtxt('data/state2/tlist.txt')
    show_state(axes[0], states[0], tri)
    show_state(axes[1], states[2], tri)
    show_state(axes[2], states[1], tri)


def read_energies():
    files = sorted(glob.glob(f'{os.getcwd()}/data/pop-energy-*.txt'))
    energies = []
    for f in files:
        e = np.loadtxt(f)
        # Detect results that seem to have not converged adequately
        i_min = np.nanargmin(e)
        e_min2 = np.nanmin(e[e!=e[i_min]])
        # if (e[i_min] < 10*e_min2): e[i_min] = np.nan
        # if (e[i_min] < 0): e[i_min] = np.nan
        energies.append(e)
    energies = np.array(energies)
    for i in np.arange(len(energies)-2,0,-1):
        energies[i,energies[i]<np.min(energies[i+1])] = np.inf
    return energies


def plot_parameter(ax, param, i_best):
    generations = np.arange(1, len(param)+1)
    for i, p_gen in enumerate(param):
        gen = np.full_like(p_gen, generations[i])
        ax.scatter(gen, p_gen, s=2, c='gray')
    best = np.take_along_axis(param, i_best[:,np.newaxis], axis=1)
    ax.plot(generations, best)


def plot_barrier(ax):
    energies = read_energies()
    i_best = np.nanargmin(energies, axis=1)
    plot_parameter(ax, 1/energies, i_best)
    ax.semilogy()
    ax.set_ylim(ymin=1e-6)
    ax.set_ylabel('Energy barrier')
    ax.set_xlabel('Generations')


def plot_params(axes):
    # Read parameters
    files = sorted(glob.glob(f'{os.getcwd()}/data/pop-{"[0-9]"*4}.txt'))
    parameters = []
    for f in files:
        parameters.append(np.loadtxt(f))
    parameters = np.array(parameters)
    # Get best states in each generation
    energies = read_energies()
    i_best = np.nanargmin(energies, axis=1)
    # Plot
    for i in range(len(axes)):
        plot_parameter(axes[i], parameters[:,:,i], i_best)
    # Axes
    axes[0].set_xticklabels([])
    axes[1].set_xticklabels([])
    axes[2].set_xlabel('Generations')
    axes[3].set_xlabel('Generations')
    axes[0].set_ylabel('$w$')
    axes[1].set_ylabel('$t$')
    axes[2].set_ylabel('$r_\mathrm{out}$')
    axes[3].set_ylabel('$r_\mathrm{in}$')


fig = lt.figure(1, 0.85)

h1 = 0.3
w1 = 0.35
h2 = 0.44
h2space = 0.05
h3 = 0.5
h3space1 = -0.09
h3space2 = -0.15

ax_a = fig.add_axes([0, 1-h1, w1, h1])
schematic(ax_a)

gs1 = fig.add_gridspec(1, 2, left=w1-0.2, right=1.2, bottom=1-h3space1-h3, top=1-h3space1, wspace=-0.6)
ax_b1 = fig.add_subplot(gs1[0,0], projection='3d')
ax_b2 = fig.add_subplot(gs1[0,1], projection='3d')
initial_structure([ax_b1, ax_b2])

gs3 = fig.add_gridspec(1, 3, left=-0.2, right=1.2, bottom=h3space2, top=h3+h3space2, wspace=-0.6)
ax_e1 = fig.add_subplot(gs3[0,0], projection='3d')
ax_e2 = fig.add_subplot(gs3[0,1], projection='3d')
ax_e3 = fig.add_subplot(gs3[0,2], projection='3d')
final_structure([ax_e1, ax_e2, ax_e3])

gs2 = fig.add_gridspec(2, 3, left=0.09, right=0.999, bottom=1-h1-h2+h2space, top=1-h1, wspace=0.3, hspace=0.08)
ax_c = fig.add_subplot(gs2[:,0])
ax_d1 = fig.add_subplot(gs2[0,1])
ax_d2 = fig.add_subplot(gs2[0,2])
ax_d3 = fig.add_subplot(gs2[1,1])
ax_d4 = fig.add_subplot(gs2[1,2])
plot_barrier(ax_c)
plot_params([ax_d1, ax_d2, ax_d3, ax_d4])

# Subfigure labels
fig.text(0.05, 0.98, '(a)', ha='left', va='top')
fig.text(0.4, 0.98, '(b)', ha='left', va='top')
fig.text(0.02, 1-h1, '(c)', ha='center', va='bottom')
fig.text(0.38, 1-h1, '(d)', ha='center', va='bottom')
fig.text(0.04, 0.22, '(e)', ha='center', va='top')

fig.text(0.54, 0.96, 'State 1', ha='center', va='top')
fig.text(0.83, 0.96, 'State 2', ha='center', va='top')

fig.text(0.19, 0.2, 'State 1', ha='center', va='top')
fig.text(0.5, 0.2, 'TS', ha='center', va='top')
fig.text(0.81, 0.2, 'State 2', ha='center', va='top')

# plt.show()
lt.savefig('../structopt.png', dpi=500)

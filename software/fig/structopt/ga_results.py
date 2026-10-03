#/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

outdir = "outputs"

def read_energies():
    files = sorted(glob.glob(f'{os.getcwd()}/{outdir}/pop-energy-*.txt'))
    energies = []
    for f in files:
        e = np.loadtxt(f)
        # Detect results that seem to have not converged adequately
        i_min = np.nanargmin(e)
        e_min2 = np.nanmin(e[e!=e[i_min]])
        # if (e[i_min] < 10*e_min2): e[i_min] = np.nan
        # if (e[i_min] < 0): e[i_min] = np.nan
        energies.append(e)
    return np.array(energies)


def read_parameters():
    files = sorted(glob.glob(f'{os.getcwd()}/{outdir}/pop-{"[0-9]"*4}.txt'))
    parameters = []
    for f in files:
        parameters.append(np.loadtxt(f))
    return np.array(parameters)


def plot_parameter(ax, param, i_best):
    generations = np.arange(1, len(param)+1)
    for i, p_gen in enumerate(param):
        gen = np.full_like(p_gen, generations[i])
        ax.scatter(gen, p_gen, s=2, c='gray')
    best = np.take_along_axis(param, i_best[:,np.newaxis], axis=1)
    ax.plot(generations, best)


energies = read_energies()
parameters = read_parameters()
i_best = np.nanargmin(energies, axis=1)

fig = plt.figure(figsize=(8,4))
axes = fig.subplot_mosaic('ABC;ADE')

ax = axes['A']
plot_parameter(ax, 1/energies, i_best)
ax.semilogy()
ax.set_ylim(ymin=1e-6)
ax.set_ylabel('Energy barrier')
ax.set_xlabel('Generations')

param_labels = ['Width', 'Thickness', 'Out radius', 'In radius']
for i in range(4):
    ax = list(axes.values())[i+1]
    plot_parameter(ax, parameters[:,:,i], i_best)
    # ax.set_ylim(0, 1)
    ax.set_ylabel(param_labels[i])
    if (i>=2): ax.set_xlabel('Generations')

plt.tight_layout()
# plt.savefig("ga_results.png")
plt.show()

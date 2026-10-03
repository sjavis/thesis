#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

outdir = 'outputs'
datdir = 'data'
gen = 4
state_num = 17

data = np.loadtxt(f"{outdir}/pop-states-{gen:04d}-{state_num:04d}.txt").reshape([3,-1,3])
params = np.loadtxt(f'{outdir}/pop-{gen:04d}.txt', skiprows=state_num, max_rows=1)
tri = np.loadtxt(f'{datdir}/width-{params[0]:.6f}-outRad-{params[2]:.6f}-inRad-{params[3]:.6f}/tlist.txt')
print(np.max(tri), data.shape)
print(params)

fig = plt.figure(constrained_layout=True)

for i, state in enumerate(data):
    ax = fig.add_subplot(1,3,i+1, projection='3d')
    view = 15 * np.pi/180
    x = state[:,0]*np.cos(view) - state[:,1]*np.sin(view)
    y = state[:,0]*np.sin(view) + state[:,1]*np.cos(view)
    z = state[:,2]
    ax.plot_trisurf(x, y, z, triangles=tri, cmap=plt.cm.coolwarm, vmin=-0.2, vmax=0.2)
    ax.view_init(15, 0)
    ax.set_axis_off()
    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))

fig.subplots_adjust(wspace=0, hspace=0)
# plt.tight_layout()
plt.show()

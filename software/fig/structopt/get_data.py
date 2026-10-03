#!/usr/bin/env python3
import os
import glob
import numpy as np

basedir = '/home/sam/phd/ellib_testing/structure_optimisation'

# Get parameters and energies
os.system('mkdir -p data')
for f in glob.glob(basedir+r'/outputs/pop-[0-9]*.txt'):
    os.system('cp '+f+' data/')
for f in glob.glob(basedir+r'/outputs/pop-energy-[0-9]*.txt'):
    os.system('cp '+f+' data/')

# Get first and last states
gen = [0, 19]
for i in [0, 1]:
    os.system(f'mkdir -p data/state{i+1}')
    # Number of the best state
    i_best = np.argmin(np.loadtxt(f'data/pop-energy-{gen[i]:04d}.txt'))
    if (i==1): i_best = 22
    # Get the triangulation
    params = np.loadtxt(f'data/pop-{gen[i]:04d}.txt', skiprows=i_best, max_rows=1)
    datdir = f'width-{params[0]:.6f}-outRad-{params[2]:.6f}-inRad-{params[3]:.6f}'
    os.system(f'cp {basedir}/data/{datdir}/tlist.txt data/state{i+1}/tlist.txt')
    # Get the states
    os.system(f'cp {basedir}/outputs/pop-states-{gen[i]:04d}-{i_best:04d}.txt data/state{i+1}/states.txt')

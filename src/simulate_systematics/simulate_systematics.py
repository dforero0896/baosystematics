#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
def generate_random_vetomask(ndensity, box_size=2500, remove_fraction=0.05, seed=42, ofile='vetomask', nholes=100):
    np.random.seed(seed)
    ofile+='_s%s_nbar%.4e.dat'%(seed, ndensity)
    volume=box_size**3
    nmax = ndensity * volume * remove_fraction
    nmax_per_hole = nmax / nholes
    mean_hole_volume = nmax_per_hole / ndensity
    mean_hole_area = mean_hole_volume / box_size
    mean_hole_side = mean_hole_area**(1./2)
    volumes = []
    mask_coords = []
    with open(ofile, 'w') as out:
        for _ in range(nholes):
            x1, y1 = box_size * np.random.random(2)
            #width_x, width_y = np.random.normal(mean_hole_side, np.sqrt(nholes), 2)
            width_hole_width = 10**np.round(np.log10(mean_hole_side))
            width_x, width_y = 2 * width_hole_width * np.random.random(2) + mean_hole_side - width_hole_width
            volumes.append(width_x * width_y * box_size)
            for patch in pbc_patches((x1, width_x, y1, width_y), boundaries=(0, box_size, 0, box_size)):
                mask_coords.append(list(patch))
        mask_coords=np.array(mask_coords)
        np.savetxt(out, mask_coords, fmt = '%.3f %.3f %.3f %.3f')
    remove_fraction_true = sum(volumes)/volume
    print(remove_fraction_true)

def generate_random_angmask(ndensity, box_size=2500, volume_fraction=0.5, mean_completeness=0.9, std_completeness=0.05, seed=2, ofile='angmask', nholes=40):
    np.random.seed(seed)
    ofile+='_s%s_nbar%.4e.dat'%(seed, ndensity)
    volume=box_size**3
    nmax = ndensity * volume * volume_fraction
    nmax_per_hole = nmax / nholes
    mean_hole_volume = nmax_per_hole / ndensity
    mean_hole_area = mean_hole_volume / box_size
    mean_hole_side = mean_hole_area**(1./2)
    volumes = []
    mask_coords = []
    with open(ofile, 'w') as out:
        for _ in range(nholes):
            x1, y1 = box_size * np.random.random(2)
            #width_x, width_y = np.random.normal(mean_hole_side, np.sqrt(nholes), 2)
            width_hole_width = 10**np.round(np.log10(mean_hole_side))
            width_x, width_y = 2 * width_hole_width * np.random.random(2) + mean_hole_side - width_hole_width
            volumes.append(width_x * width_y * box_size)
            hole_completeness = np.random.normal(mean_completeness, std_completeness)
            while hole_completeness >= 1:
                hole_completeness = np.random.normal(mean_completeness, std_completeness)
            for patch in pbc_patches((x1, width_x, y1, width_y), boundaries=(0, box_size, 0, box_size)):
                patch.append(hole_completeness)
                mask_coords.append(patch)
        mask_coords=np.array(mask_coords)
        np.savetxt(out, mask_coords, fmt = '%.3f %.3f %.3f %.3f %.3f')
    remove_fraction_true = sum(volumes)/volume
    print(remove_fraction_true)

def pbc_patches(coords, boundaries=(0, 2500, 0, 2500)):
    x1, width_x, y1, width_y = coords
    xmin, xmax, ymin, ymax = boundaries
    x_size = xmax - xmin
    y_size = ymax - ymin
    out_patches = []
    areas=[]
    for i in [0, x_size]:
        for k in [0, y_size]:
            new_x1 = x1 - i
            new_y1 = y1 - k
            new_coords = np.clip([new_x1, new_x1 + width_x, new_y1, new_y1 + width_y], xmin, xmax)
            new_xsize, new_ysize = new_coords[1]-new_coords[0], new_coords[3]-new_coords[2]
            if(new_xsize == 0 or new_ysize == 0):
                continue
            out_patches.append(list(new_coords))
    return out_patches
  
def plot_mask(coords, box_size=2500, fig=None, color='k'):
    if not fig:
        fig = plt.figure(figsize=(10,10))
    plt.xlim(0, box_size)
    plt.ylim(0, box_size)
    import matplotlib.patches as pat
    for line in coords:
        p=pat.Rectangle((line[0], line[2]), line[1]-line[0], line[3]-line[2], fill=True, color=color)
        plt.gca().add_patch(p)
    plt.show()


if __name__ == '__main__':
    generate_random_vetomask(3.976980e-4)
    generate_random_angmask(3.976980e-4)
    fig = plt.figure()
    plot_mask(np.loadtxt('vetomask_s42_nbar3.9770e-04.dat'), fig=fig)    
    plot_mask(np.loadtxt('angmask_s42_nbar3.9770e-04.dat'), color='b', fig=fig)    

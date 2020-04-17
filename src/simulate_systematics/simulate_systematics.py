#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
def generate_random_vetomask(ndensity, box_size=2500, remove_fraction=0.05, seed=42, ofile='vetomask', nholes=100, x_sampler=np.random.random, y_sampler=np.random.random):
    np.random.seed(seed)
    if not y_sampler:
        y_sampler=x_sampler
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
            x1, y1 = (box_size-mean_hole_side) * x_sampler(), (box_size-mean_hole_side) * y_sampler()
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

def generate_random_angmask(ndensity, box_size=2500, volume_fraction=0.5, mean_completeness=0.9, std_completeness=0.05, seed=2, ofile='angmask', nholes=40, x_sampler = np.random.random, y_sampler=np.random.random):
    np.random.seed(seed)
    if not y_sampler:
        y_sampler=x_sampler
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
        for hole in range(nholes):
            #width_x, width_y = np.random.normal(mean_hole_side, np.sqrt(nholes), 2)
            width_hole_width = 10**np.round(np.log10(mean_hole_side))
            width_x, width_y = 2 * width_hole_width * np.random.random(2) + mean_hole_side - width_hole_width
            #x1, y1 = (box_size-np.array(width_x, width_y)) * np.random.random(2)
            x1, y1 = (box_size-mean_hole_side) * x_sampler(), (box_size-mean_hole_side) * y_sampler()
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
def generate_grid_angmask(ndensity, box_size=2500, volume_fraction=0.5, mean_completeness=0.8, std_completeness=0.2, seed=2, ofile='angmask_grid', nholes=40, comp_func=None, noise=True):
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
    x1_s = np.arange(0, box_size, mean_hole_side)
    y1_s = np.copy(x1_s)
    if comp_func:
        print("Using completeness function.")
        if noise : ran = np.random.normal(0, 0.2)
        else : ran=0
        tmp_comp_func = comp_func
        comp_func = (lambda y, x: tmp_comp_func(y+0.5*mean_hole_side,x+0.5*mean_hole_side) + ran)
#        xx, yy = np.meshgrid(x1_s, y1_s)
#        c=plt.pcolormesh(xx, yy, comp_func(yy, xx))
#        plt.colorbar(c)
    else: comp_func = lambda y, x: np.random.normal(mean_completeness, std_completeness)
    for x in x1_s:
        for y in y1_s:
            width_hole_width = 10**np.round(np.log10(mean_hole_side))
            width_x, width_y = 2 * width_hole_width * np.random.random(2) + mean_hole_side - width_hole_width
            width_x, width_y = mean_hole_side, mean_hole_side
            hole_completeness = comp_func(y,x) #np.random.normal(mean_completeness, std_completeness)
            while hole_completeness >= 1 or hole_completeness <= 0.5:
                hole_completeness = comp_func(y,x) #np.random.normal(mean_completeness, std_completeness)
            #for patch in pbc_patches((x, width_x, y, width_y), boundaries=(0, box_size, 0, box_size)):
            #    patch.append(hole_completeness)
            #    mask_coords.append(patch)
            mask_coords.append([x, x+width_x, y, y+width_y, hole_completeness])
    mask_coords=np.array(mask_coords)
    np.savetxt(ofile, mask_coords, fmt = '%.3f %.3f %.3f %.3f %.3f')

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

def intersect(patch_a, patch_b):
    return (((patch_a[1] > patch_b[0]) and (patch_a[3] > patch_b[2])) or ((patch_b[1] > patch_a[0]) and (patch_b[3] > patch_a[2])))
  
def plot_mask(coords, box_size=2500, fig=None, color='k'):
    if not fig:
        fig = plt.figure(figsize=(10,10))
    plt.xlim(0, box_size)
    plt.ylim(0, box_size)
    plt.gca().set_aspect(aspect=1)
    import matplotlib.patches as pat
    for line in coords:
        if len(line)>4: alpha = line[4]/2
        else: alpha=None
        p=pat.Rectangle((line[0], line[2]), line[1]-line[0], line[3]-line[2], fill=True, color=color, edgecolor=color, alpha=alpha)
        plt.gca().add_patch(p)
    plt.gca().add_patch(p)
    plt.show()


if __name__ == '__main__':
### FOR BOX 1
# Uniform mask
#    generate_random_vetomask(3.976980e-4, ofile='masks/vetomask')
#    generate_random_angmask(3.976980e-4, ofile='masks/angmask', seed=2)
# Uniform corner
#    generate_random_angmask(3.976980e-4, ofile='masks/angmask_corner', seed=2, box_size=1250, volume_fraction=0.5)
#    generate_random_vetomask(3.976980e-4, ofile='masks/vetomask_corner', seed=42, box_size=1250, remove_fraction=0.2)
# Triangular mask
#    generate_random_angmask(3.976980e-4, ofile='masks/angmask_triangle', seed=2, volume_fraction=0.5, x_sampler=lambda : np.random.triangular(0, 0.9, 1), y_sampler=None)
#    generate_random_vetomask(3.976980e-4, ofile='masks/vetomask_triangle', seed=42, remove_fraction=0.05, x_sampler=lambda : np.random.triangular(0, 0.9, 1), y_sampler=None)
# Grid mask
    generate_grid_angmask(3.976980e-4, ofile='masks/angmask_grid_function_rand', seed=2, comp_func=(lambda y, x: -1.6e-7*((x-1250)**2 + (y-1250)**2) + 1), nholes=100, noise=False)
    generate_grid_angmask(3.976980e-4, ofile='masks/angmask_grid_function', seed=2, comp_func=(lambda y, x: -1.6e-7*((x-1250)**2 + (y-1250)**2) + 1), nholes=100, noise=True)

### FOR BOX 5
#    generate_random_vetomask(1.976125e-04, ofile='masks/vetomask')
#    generate_random_angmask(1.976125e-04, ofile='masks/angmask', seed=2)
    fig = plt.figure()
    plot_mask(np.loadtxt('masks/angmask_grid_function_s2_nbar3.9770e-04.dat'), fig=fig)    
#    plot_mask(np.loadtxt('masks/vetomask_triangle_s42_nbar3.9770e-04.dat'), color='b', fig=fig)    

'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''
import numpy as np


def rounda(n, d):
    return (n + d // 2) // d

def np_velocity(system):
    
    (vely, velx) = np.gradient(system.space)

    for i in xrange(system.tot_cells_x):
        for j in xrange(system.tot_cells_y):
            velx[i, j] = -system.k * velx[i, j] / system.porosity
            vely[i, j] = -system.k * vely[i, j] / system.porosity
    
    #system.set_velocity(velx, vely)
    return velx, vely

def calculate_velocity(system):
    velx = np.zeros((system.tot_cells_x, system.tot_cells_y))
    vely = np.zeros((system.tot_cells_x, system.tot_cells_y))
    
    constant = system.k / system.porosity

    for i in xrange(1, system.tot_cells_x - 1):
        for j in xrange(1, system.tot_cells_y - 1):
            velx[i, j] = -constant * (system.space[i, j + 1] - system.space[i, j]) / system.cell_spacing
            vely[i, j] = -constant * (system.space[i + 1, j] - system.space[i, j]) / system.cell_spacing
    return velx, vely




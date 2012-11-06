'''
Created on 19/10/2012

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np


def rounda(nume, deno):
    return (nume + deno // 2) // deno


def calculate_courant(spacing,velx,vely):
    return np.sqrt(0.5)*spacing/(np.sqrt(np.power(np.max(velx),2) + np.power(np.max(vely),2)))

def calculate_velocity(n_x, n_y, spacing, scalar_field):
    
    velx = np.zeros((n_x, n_y))
    vely = np.zeros((n_x, n_y))
    
    constant = -1.0

    for i in xrange(1, n_y - 1):
        for j in xrange(1, n_x - 1):
            velx[i, j] =  constant * (scalar_field[i, j + 1 ] - scalar_field[i, j - 1]) / (spacing * 2.0)
            vely[i, j] =  constant * (scalar_field[i + 1, j ] - scalar_field[i - 1, j]) / (spacing * 2.0)
    
    #velx[:,0] = (velx[:,1] - velx[:,0]) / spacing
    #vely[0,:] = (vely[1,:] - vely[0,:]) / spacing
    print vely
    return velx, vely

def generate_scalar_field(n_x, n_y, scalar_field):
    for j in xrange(n_x):
        scalar_field[:,j] = np.linspace(0, n_x-1, n_x)
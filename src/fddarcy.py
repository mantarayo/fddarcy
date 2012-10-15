#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Created on 14/10/2012

@author: Ivan Marin
@email: ispmarin@gmail.com
'''
#import argparse
#import shapely.geometry as shp
import sys
import numpy as np

import output


def round(n,d):
   return (n + d // 2) // d


class node():
    """
    docstring
    """
    def __init__(self,k,head):
        self.k = k
        self.head = head
        self.fixed = 0

class system_def():
    """
    """
    def __init__(self,dimx, dimy, cell_spacing, init_head, k, porosity):

        self.dimx = dimx
        self.dimy = dimy
        self.cell_spacing = cell_spacing
        self.tot_cells_x = int(round(self.dimx , self.cell_spacing) + 1) # for the boundary conditions
        self.tot_cells_y = int(round(self.dimy , self.cell_spacing) + 1) # for the boundary conditions
        self.space = np.ones((self.tot_cells_x, self.tot_cells_y)) * init_head
        self.init_head = init_head
        self.k = k 
        self.porosity = porosity
        self.velx = np.zeros((self.tot_cells_x, self.tot_cells_y))
        self.vely = np.zeros((self.tot_cells_x, self.tot_cells_y))
        print self.tot_cells_x, self.tot_cells_y

    def fixed_boundary_conditions(self,head_up, head_down):
        self.space[0,:] = head_up
        self.space[self.tot_cells_x-1,:] = head_down

    def line_boundary_conditions(self, head_up, head_down):
        self.space[0,:] = np.linspace(head_down,head_up,self.tot_cells_x)
        self.space[self.tot_cells_x-1,:] = head_down
    
    def set_velocity(self, velx, vely):
        self.velx = velx
        self.vely = vely

class calculations():
    """
    """
    def __init__(self,max_iter, limit_convergence, system):
        self.max_iter = max_iter
        self.tolerance = limit_convergence
        self.system = system
    

    def do_it(self):
       iter_n = 0
       prev_head = (self.system.init_head + 1) * 1000
       onespacing = 1.0/4.0
       print onespacing 
       while (iter_n < self.max_iter):
           for i in xrange(1,self.system.tot_cells_x - 1):
               for j in xrange(1,self.system.tot_cells_y - 1):
                   self.system.space[i,j] =  onespacing  * \
                   (self.system.space[i-1,j] + self.system.space[i,j-1] + self.system.space[i+1,j] + self.system.space[i,j+1] )
           self.system.space[:,0] = self.system.space[:,1]
           self.system.space[:,self.system.tot_cells_x -1] = self.system.space[:,self.system.tot_cells_x-2] #for boundary conditions copied from inside to the bourders after the run

           iter_n = iter_n+1
           if iter_n % 5 == 0:
               now_head = np.max(self.system.space[1:self.system.tot_cells_x-1,:])
               print "iter ", iter_n, now_head, prev_head - now_head
               if abs(prev_head -  now_head) < self.tolerance: 
                    break
               else:
                    prev_head = now_head 

            
def velocity(system):
    
    (vely,velx) =  np.gradient(system.space)

    for i in xrange(system.tot_cells_x):
        for j in xrange(system.tot_cells_y):
            velx[i,j] = -system.k * velx[i,j] / system.porosity
            vely[i,j] = -system.k * vely[i,j] / system.porosity
    
    system.set_velocity(velx, vely)


def calculate_velocity(system):
    velx = np.zeros((system.tot_cells_x, system.tot_cells_y))
    vely = np.zeros((system.tot_cells_x, system.tot_cells_y))
    
    constant = system.k / system.porosity

    for i in xrange(1, system.tot_cells_x -1):
        for j in xrange(1, system.tot_cells_y - 1):
            velx[i,j] = -constant * (system.space[i,j+1] - system.space[i,j])/system.cell_spacing
            vely[i,j] = -constant * (system.space[i+1,j] - system.space[i,j])/system.cell_spacing
    return velx, vely


class particle()

class random_walk():
    """
    """

    def __init__(self,seed, deltaT, particle_num, DL, DT)
        self.seed = seed
        self.deltaT = deltaT
        self.particle_num = particle_num
        self.DL = DL
        self.DT = DT
    


def main():
   
    size_x = 10
    size_y = 10
    cell_spacing = .25 
    initial_head = 1
    hydraulic_conduct = 10
    porosity = 0.15
    max_iter = 5000
    limit_conver = 1e-3
    system = system_def(size_x, size_y, cell_spacing, initial_head, hydraulic_conduct, porosity)
    #system.fixed_boundary_conditions(100,50)
    system.line_boundary_conditions(100,50)
    
    calculate = calculations(max_iter, limit_conver,system)
    calculate.do_it()
    
    
    plotter = output.plotter(system.tot_cells_x, system.tot_cells_y, 10, system.space)
    plotter.plot_head('screen')
    
    velx, vely = calculate_velocity(system)
    plotter.plot_velocity(velx,vely)
    velocity(system)
    plotter.plot_velocity(system.velx, system.vely)

if __name__ == "__main__":
    sys.exit(main())


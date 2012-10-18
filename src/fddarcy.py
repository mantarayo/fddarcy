#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Created on 14/10/2012

@author: Ivan Marin
@email: ispmarin@gmail.com
'''
# import argparse

import sys
import numpy as np
import output
import aux_func
import random_walk
import flow
import advection



class system_def():
    """
    """
    def __init__(self, dimx, dimy, cell_spacing, init_head, k, porosity, w):

        self.dimx = dimx
        self.dimy = dimy
        self.cell_spacing = cell_spacing
        self.tot_cells_x = int(aux_func.rounda(self.dimx , self.cell_spacing) + 1)  # for the boundary conditions
        self.tot_cells_y = int(aux_func.rounda(self.dimy , self.cell_spacing) + 1)  # for the boundary conditions
        self.space = np.ones((self.tot_cells_x, self.tot_cells_y)) * init_head
        self.init_head = init_head
        self.k = k 
        self.porosity = porosity
        self.w = w
        self.velx = np.zeros((self.tot_cells_x, self.tot_cells_y))
        self.vely = np.zeros((self.tot_cells_x, self.tot_cells_y))
        print self.tot_cells_x, self.tot_cells_y

    def fixed_boundary_conditions(self, head_up, head_down):
        self.space[0, :] = head_up
        self.space[self.tot_cells_x - 1, :] = head_down

    def line_boundary_conditions(self, head_up, head_down):
        self.space[0, :] = np.linspace(head_down, head_up, self.tot_cells_x)
        self.space[self.tot_cells_x - 1, :] = head_down
    
    def set_velocity(self, velx, vely):
        self.velx = velx
        self.vely = vely


def main():
   
    size_x = 20
    size_y = 20
    cell_spacing = .25
    initial_head = 95
    hydraulic_conduct = 10
    porosity = 0.15
    max_iter = 5000
    max_iter_time = 10
    limit_conver = 1e-3
    w = 1.9
    high_head = 100
    low_head = 90
    background_concentration = 0
    num_isolines = 10
    
    system = system_def(size_x, size_y, cell_spacing, initial_head, hydraulic_conduct, porosity, w)
    system.fixed_boundary_conditions(high_head,low_head)
    
    calculate = flow.calculations(max_iter, limit_conver, system)
    calculate.do_it_SOR(w)
    velx, vely = aux_func.calculate_velocity(system)
    
    deltaT = aux_func.calculate_courant(system.cell_spacing, velx, vely)
    print "deltaT ", deltaT
    adv = advection.advection(deltaT, velx, vely, background_concentration, max_iter_time, system)
    adv.fixed_boundary_conditions(1, 0)
    adv.do_it_conc()
    
    plotter = output.plotter(system.tot_cells_x, system.tot_cells_y, num_isolines)
    plotter.plot_head('screen', system.space)
    plotter.plot_velocity(velx, vely)
    plotter.plot_head('screen', adv.c1)
    
    seed = 1
    total_time = 100
    particle_num =  100
    DL = 0.01
    DT=0.001
    init_position = (size_x/2, 1)
    randd = random_walk.random_walk(seed, deltaT, max_iter_time, particle_num, DL, DT, init_position, system)
    randd.do_the_walk()
    plotter.plot_head_random(randd,system)
    
if __name__ == "__main__":
    sys.exit(main())


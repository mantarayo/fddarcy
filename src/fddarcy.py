#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Created on 14/10/2012

@author: Ivan Marin
@email: ispmarin@gmail.com
'''
# import argparse
# import shapely.geometry as shp
import sys
import numpy as np
#import matplotlib.pyplot as plt
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
   
    size_x = 10
    size_y = 10
    cell_spacing = .25
    initial_head = 90
    hydraulic_conduct = 10
    porosity = 0.15
    max_iter = 5000
    limit_conver = 1e-3
    w = 0.5
    system = system_def(size_x, size_y, cell_spacing, initial_head, hydraulic_conduct, porosity, w)
    system.fixed_boundary_conditions(100,90)
    #system.line_boundary_conditions(100, 50)
    
    calculate = flow.calculations(max_iter, limit_conver, system)
    #calculate.do_it_SOR(w)
    calculate.do_it_gauss_seidel()
    aux_func.calculate_velocity(system)
    
    plotter = output.plotter(system.tot_cells_x, system.tot_cells_y, 10, system.space)
    plotter.plot_head('screen')
    
    velx, vely = aux_func.calculate_velocity(system)

    deltaT = system.cell_spacing / (np.sqrt(2.0 * (np.max(velx)**2 + np.max(vely)**2)))
    print deltaT
    adv = advection.advection(deltaT, velx, vely, 0.0, 1000, system)
    adv.fixed_boundary_conditions(1, 0)
    adv.do_it_conc()


    plotter = output.plotter(system.tot_cells_x, system.tot_cells_y, 10, adv.c1)
    plotter.plot_head('screen')

#    randomguy = random_walk.random_walk(1, 0.25, 2000, 100 ,0.10, 0.010, (20,20), system)
#    randomguy.do_the_walk()
#    plotter.plot_head_random(randomguy)
    #velx, vely = calculate_velocity(system)
    #plotter.plot_velocity(velx, vely)
    #velocity(system)
    #plotter.plot_velocity(system.velx, system.vely)

if __name__ == "__main__":
    sys.exit(main())


#! /usr/bin/env python3.2
# -*- coding: utf-8 -*-

'''
Created on 07/03/2011

@author: ispmarin
'''
import argparse
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
    def __init__(self,dimx, dimy, cell_spacing, init_head):

        self.dimx = dimx
        self.dimy = dimy
        self.cell_spacing = cell_spacing
        self.tot_cells_x = int(round(self.dimx , self.cell_spacing) + 1) # for the boundary conditions
        self.tot_cells_y = int(round(self.dimy , self.cell_spacing) + 1) # for the boundary conditions
        self.space = np.ones((self.tot_cells_x, self.tot_cells_y)) * init_head
        self.init_head = init_head
        print self.tot_cells_x, self.tot_cells_y

    def boundary_conditions(self,head_up, head_down):
        self.space[0,:] = head_up
        self.space[self.tot_cells_x-1,:] = head_down


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
           

           iter_n = iter_n+1
           if iter_n % 5 == 0:
               now_head = np.max(self.system.space[1:self.system.tot_cells_x-1,:])
               print "iter ", iter_n, now_head, prev_head - now_head
               if abs(prev_head -  now_head) < self.tolerance: 
                    break
               else:
                    prev_head = now_head 

            


def main():
    size_x = 100
    size_y = 100
    cell_spacing = .5 
    initial_head = 50
    max_iter = 44500
    limit_conver = 1e-3
    system = system_def(size_x, size_y, cell_spacing, initial_head)
    system.boundary_conditions(100,50)
    calculate = calculations(max_iter, limit_conver,system)
    calculate.do_it()
    
    
    plotter = output.plotter(system.tot_cells_x, system.tot_cells_y, 10, system.space)
    plotter.plot_head('screen')


if __name__ == "__main__":
    sys.exit(main())

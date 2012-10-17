'''
Created on 2012-10-17

@author: ivsip
'''

import numpy as np

class advection(object):
    '''
    classdocs
    '''


    def __init__(self,deltaT, velx, vely, background_c, max_iter, system):
        '''
        Constructor
        '''
        self.deltaT = deltaT
        self.velx = velx
        self.vely = vely
        self.max_iter = max_iter
        self.concentration = np.ones((system.tot_cells_x, system.tot_cells_y)) * background_c
        self.tot_cells_x = system.tot_cells_x
        self.tot_cells_y = system.tot_cells_y
        self.cell_spacing = system.cell_spacing
    
    def line_boundary_conditions(self, conc_up, conc_down):
        self.space[0, :] = np.linspace(conc_down, conc_up, self.tot_cells_x)
        self.space[self.tot_cells_x - 1, :] = conc_down
        
        
    def do_it_conc(self):
        iter_n = 0

        print "advecting..."
        while (iter_n < self.max_iter):
            for i in xrange(1, self.tot_cells_x - 1):
                for j in xrange(1, self.tot_cells_y - 1):
                    self.concentration[i,j] = self.concentration[i,j] - self.deltaT * ( self.velx[i,j]*(self.concentration[i,j]/self.cell_spacing) + 
                                                                                      self.vely[i,j]*(self.concentration[i,j]/self.cell_spacing)  )
            self.concentration[:, 0] = self.concentration[:, 1]
            self.concentration[:, self.tot_cells_x - 1] = self.concentration[:, self.tot_cells_x - 2]  # for boundary conditions copied from inside to the bourders after the run

            iter_n = iter_n + 1
        print self.concentration
        print "advected"

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
        self.c1 = np.ones((system.tot_cells_x, system.tot_cells_y)) * background_c
        self.c2 = np.ones((system.tot_cells_x, system.tot_cells_y)) * background_c
        self.tot_cells_x = system.tot_cells_x
        self.tot_cells_y = system.tot_cells_y
        self.cell_spacing = system.cell_spacing
    
    def line_boundary_conditions(self, conc_up, conc_down):
        self.c1[0, :] = np.linspace(conc_down, conc_up, self.tot_cells_x)
        self.c1[self.tot_cells_x - 1, :] = conc_down
    def fixed_boundary_conditions(self, head_up, head_down):
        self.c1[0, :] = head_up
        self.c1[self.tot_cells_x - 1, :] = head_down
        
        
    def do_it_conc(self):
        iter_n = 0
        onespacing = 1.0/4.0
        print "advecting..."
        while (iter_n < self.max_iter):
            for i in xrange(1, self.tot_cells_x - 1):
                for j in xrange(1, self.tot_cells_y - 1):
                    
                    self.c2[i,j] = onespacing * (self.c1[i+1,j] + self.c1[i-1,j] + self.c1[i,j+1] + self.c1[i,j-1]) - \
                    (self.deltaT/(2*self.cell_spacing))*(self.velx[i,j]*(self.c1[i+1,j] - self.c1[i-1,j]) + self.vely[i,j]*(self.c1[i,j+1] - self.c1[i,j-1]))
                    
            self.c2[:, 0] = self.c2[:, 1]
            self.c2[:, self.tot_cells_x - 1] = self.c2[:, self.tot_cells_x - 2]  # for boundary conditions copied from inside to the bourders after the run
            
            self.c1 = self.c2
            
            iter_n = iter_n + 1
        #print self.c1
        print "advected"

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
        self.max_time_steps = max_iter
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
        time_step = 0
        onespacing = 1.0/4.0
        courant = 0.5 * self.deltaT / self.cell_spacing 
        print "advecting..."
        while (time_step <= self.max_time_steps):
            for i in xrange(1, self.tot_cells_x - 1):
                for j in xrange(1, self.tot_cells_y - 1):
                    self.c2[i,j] = onespacing * (self.c1[i+1,j] + self.c1[i-1,j] + self.c1[i,j+1] + self.c1[i,j-1]) - \
                    courant*(self.velx[i,j]*(self.c1[i+1,j] - self.c1[i-1,j]) + self.vely[i,j]*(self.c1[i,j+1] - self.c1[i,j-1]))
            
            #print courant*self.velx[i,j]*(self.c1[i+1,j] - self.c1[i-1,j]), self.vely[i,j]*(self.c1[i,j+1] - self.c1[i,j-1])*courant
            #self.c2[:,0] = self.c2[:,self.tot_cells_x - 2]
            #self.c2[:,self.tot_cells_x -1] = self.c2[:,1]        
            #self.c2[:, 0] = self.c2[:, 1]
            #self.c2[:, self.tot_cells_x - 1] = self.c2[:, self.tot_cells_x - 2]  # for boundary conditions copied from inside to the bourders after the run
            
            self.c1 = self.c2
            
            time_step = time_step + 1#self.deltaT
            
            self.c1[0,:] = 0 #after the first time step, there's no more injection of concentration 
            self.c1[self.tot_cells_x - 1,:] = 0
        
            print "time step ", time_step
        #print self.c1
        print "advected"

'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np

class advection(object):
    '''
    classdocs
    '''


    def __init__(self,deltaT, velx, vely, background_c, max_iter, workhorse):
        '''
        Constructor
        '''
        self.deltaT = deltaT
        self.velx = velx
        self.vely = vely
        self.max_time_steps = max_iter
        #self.c1 = np.ones((workhorse.n_x, workhorse.n_y)) * background_c
        self.conc = np.ones((workhorse.n_x, workhorse.n_y)) * background_c
        self.n_x = workhorse.n_x
        self.n_y = workhorse.n_y
        self.spacing = workhorse.spacing
    
    def line_boundary_conditions(self, conc_up, conc_down):
        self.conc[0, :] = np.linspace(conc_down, conc_up, self.n_x)
        self.conc[self.n_x - 1, :] = conc_down
        
    def fixed_boundary_conditions(self, head_up, head_down):
        self.conc[0, :] = head_up
        self.conc[self.n_x - 1, :] = head_down
        
    def advect_step(self, extern_conc):
        onespacing = 1.0/4.0
        courant = 0.5 * self.deltaT / self.spacing 
        #print "advecting..."
        
        for i in xrange(1, self.n_x - 1):
            for j in xrange(1, self.n_y - 1):
                self.conc[i,j] = onespacing * (extern_conc[i+1,j] + extern_conc[i-1,j] + extern_conc[i,j+1] + extern_conc[i,j-1]) - \
                courant*(self.velx[i,j]*(extern_conc[i,j+1] - extern_conc[i,j-1]) + self.vely[i,j]*(extern_conc[i+1,j] - extern_conc[i-1,j]))
            
        extern_conc = self.conc

            
            
            
            
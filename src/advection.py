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
        self.courant = 0.5 * self.deltaT / self.spacing 
        print "max_time_steps ", self.max_time_steps, "courant ", self.courant
        if np.abs(self.courant) > 1:
            print "WARNING: Courant number larger than 1"
            
        
    def line_boundary_conditions(self, conc_up, conc_down):
        self.conc[0, :] = np.linspace(conc_down, conc_up, self.n_x)
        self.conc[self.n_x - 1, :] = conc_down
        
    def fixed_boundary_conditions(self, head_up, head_down, head_left, head_right):
        self.conc[0, :] = head_up
        self.conc[self.n_x - 1, :] = head_down
        self.conc[:,0] = head_left
        self.conc[:,self.n_y - 1] = head_right
    
    def set_region_bc(self, x_ini, y_ini, x_end, y_end, conc):
        pos_x_ini = int(x_ini / self.spacing)
        pos_y_ini = int(y_ini / self.spacing)
        pos_x_end = int(x_end / self.spacing)
        pos_y_end = int(y_end / self.spacing)
        
        #print x_ini, y_ini, x_end, y_end, pos_x_ini, pos_y_ini, pos_x_end, pos_y_end
        
        for i in xrange(pos_y_ini, pos_y_end):
            for j in xrange(pos_x_ini, pos_x_end):
                self.conc[i,j] = conc
                
        
        
    def advect_step(self):
        for i in xrange(1, self.n_x - 1):
            for j in xrange(1, self.n_y - 1):
                self.conc[i,j] =  (self.conc[i+1,j] + self.conc[i-1,j] + self.conc[i,j+1] + self.conc[i,j-1])/4. - \
                self.courant * (self.velx[i,j]*(self.conc[i+1,j] - self.conc[i-1,j]) + self.vely[i,j]*(self.conc[i,j+1] - self.conc[i,j-1]))
            
        
    def advect_step_numpy(self):
        self.conc[1:-1, 1:-1] = (self.conc[2:, 1:-1] + self.conc[:-2, 1:-1]+ self.conc[1:-1, 2:] +  self.conc[1:-1, :-2] )/4. - \
        self.courant * ( self.velx[1:-1,1:-1] *(self.conc[2:,1:-1] - self.conc[:-2,1:-1]  ) + self.vely[1:-1,1:-1]*( self.conc[1:-1,2:] - self.conc[1:-1,:-2]  )   )
        
            
            
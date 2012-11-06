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
        self.c1 = np.ones((workhorse.n_x, workhorse.n_y)) * background_c
        self.c2 = np.ones((workhorse.n_x, workhorse.n_y)) * background_c
        self.n_x = workhorse.n_x
        self.n_y = workhorse.n_y
        self.spacing = workhorse.spacing
    
    def line_boundary_conditions(self, conc_up, conc_down):
        self.c1[0, :] = np.linspace(conc_down, conc_up, self.n_x)
        self.c1[self.n_x - 1, :] = conc_down
        
    def fixed_boundary_conditions(self, concentration_up, concentration_down):
        self.c1[0, :] = concentration_up
        self.c1[self.n_x - 1, :] = concentration_down
        
        
    def do_it_conc(self):
        time_step = 0
        onespacing = 1.0/4.0
        courant = 0.5 * self.deltaT / self.spacing 
        print "advecting..."
        
        while (time_step <= self.max_time_steps):
            for i in xrange(1, self.n_x - 1):
                for j in xrange(1, self.n_y - 1):
                    self.c2[i,j] = onespacing * (self.c1[i+1,j] + self.c1[i-1,j] + self.c1[i,j+1] + self.c1[i,j-1]) - \
                    courant*(self.velx[i,j]*(self.c1[i,j+1] - self.c1[i,j-1]) + self.vely[i,j]*(self.c1[i+1,j] - self.c1[i-1,j]))
            
            #print courant*self.velx[i,j]*(self.c1[i+1,j] - self.c1[i-1,j]), self.vely[i,j]*(self.c1[i,j+1] - self.c1[i,j-1])*courant
            #self.c2[:,0] = self.c2[:,self.n_x - 2]
            #self.c2[:,self.n_x -1] = self.c2[:,1]        
            #self.c2[:, 0] = self.c2[:, 1]
            #self.c2[:, self.n_x - 1] = self.c2[:, self.n_x - 2]  # for boundary conditions copied from inside to the bourders after the run
            
            self.c1 = self.c2
            
            time_step = time_step + 1
            
            #self.c1[0,:] = 0 #after the first time step, there's no more injection of concentration 
            #self.c1[self.n_x - 1,:] = 0
        
            print "time step ", time_step
        #print self.c2
        print "advected"

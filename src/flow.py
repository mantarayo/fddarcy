'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np

class flow_calc():
    """
    """
    def __init__(self, max_iter, limit_convergence, flow_system):
        self.max_time_steps = max_iter
        self.tolerance = limit_convergence
        self.flow_system = flow_system
        self.prev_head = (self.flow_system.init_head + 1) * 1000
        self.error = 0
    def do_it_gauss_seidel(self):
        iter_n = 0
        onespacing = 1.0 / 4.0

        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.flow_system.n_y - 1):
                for j in xrange(1, self.flow_system.n_x - 1):
                    self.flow_system.scalar_field[i, j] = onespacing * \
                    (self.flow_system.scalar_field[i - 1, j] + self.flow_system.scalar_field[i, j - 1] 
                     + self.flow_system.scalar_field[i + 1, j] + self.flow_system.scalar_field[i, j + 1])
             
            self.flow_system.scalar_field[:,0] = self.flow_system.scalar_field[:,self.flow_system.n_x - 2]
            self.flow_system.scalar_field[:,self.flow_system.n_x -1] = self.flow_system.scalar_field[:,1]
                    
            #self.flow_system.space[:, 0] = self.flow_system.space[:, 1]
            #self.flow_system.space[:, self.flow_system.n_x - 1] = self.flow_system.space[:, self.flow_system.n_x - 2]  # for boundary conditions copied from inside to the bourders after the run

            iter_n = iter_n + 1
            
            if iter_n % 5 == 0:
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                    
    def do_it_SOR(self, w):
        iter_n = 0
        onespacing = 1.0 / 4.0
        error = 0
        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.flow_system.n_x - 1):
                for j in xrange(1, self.flow_system.n_y - 1):
                    self.flow_system.scalar_field[i, j] =  self.flow_system.scalar_field[i,j] + w * (onespacing * \
                    (self.flow_system.scalar_field[i - 1, j] + self.flow_system.scalar_field[i, j - 1] + 
                     self.flow_system.scalar_field[i + 1, j] + self.flow_system.scalar_field[i, j + 1] - 
                     4.0 * self.flow_system.scalar_field[i,j]))
             
            self.flow_system.scalar_field[:,0] = self.flow_system.scalar_field[:,self.flow_system.n_x - 2]
            self.flow_system.scalar_field[:,self.flow_system.n_x -1] = self.flow_system.scalar_field[:,1]        
            #self.flow_system.space[:, 0] = self.flow_system.space[:, 1]
            #self.flow_system.space[:, self.flow_system.n_x - 1] = self.flow_system.space[:, self.flow_system.n_x - 2]  # for boundary conditions copied from inside to the bourders after the run

            iter_n = iter_n + 1
            
            if iter_n % 5 == 0:
                print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    print "total iterations: ", iter_n, "error ", self.error
                    break
                    
                    
    def check_convergence(self):
        now_head = np.max(self.flow_system.scalar_field[1:self.flow_system.n_x - 1, :])
        
        self.error = abs(self.prev_head - now_head)
        if  self.error < self.tolerance: 
            print "converged!", self.error
            return 1
        else:
            self.prev_head = now_head 
            return 0
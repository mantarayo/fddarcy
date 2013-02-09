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
        self.error_matrix = np.zeros((self.flow_system.n_x, self.flow_system.n_y))
        self.error = 0
        
    def do_it_gauss_seidel(self):
        iter_n = 0
        onespacing = 1.0 / 4.0
        print "range", self.flow_system.n_y , self.flow_system.n_x 
        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.flow_system.n_y - 1 ):
                for j in xrange(1, self.flow_system.n_x - 1 ):
                    self.flow_system.scalar_field[i, j] = onespacing * \
                    (self.flow_system.scalar_field[i - 1, j] + self.flow_system.scalar_field[i, j - 1] 
                     + self.flow_system.scalar_field[i + 1, j] + self.flow_system.scalar_field[i, j + 1])
            
                    
            #Toroidal conditions
            #self.flow_system.scalar_field[:,0] = self.flow_system.scalar_field[:,self.flow_system.n_x - 2]
            #self.flow_system.scalar_field[:,self.flow_system.n_x -1] = self.flow_system.scalar_field[:,1]
                    
            
            iter_n = iter_n + 1
            
            if iter_n % 5 == 0:
                print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                    
    def do_it_SOR(self, w):
        iter_n = 0
        onespacing = 1.0 / 4.0
        
        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.flow_system.n_x -1):
                for j in xrange(1, self.flow_system.n_y -1):
                    self.flow_system.scalar_field[i, j] =  self.flow_system.scalar_field[i,j] + w * (onespacing * \
                    (self.flow_system.scalar_field[i - 1, j] + self.flow_system.scalar_field[i, j - 1] + 
                     self.flow_system.scalar_field[i + 1, j] + self.flow_system.scalar_field[i, j + 1] - 
                     4.0 * self.flow_system.scalar_field[i,j]))
             
            
            iter_n = iter_n + 1
            
            if iter_n % 10 == 0:
                print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                    
                    
    def check_convergence(self):
        self.error_matrix = np.abs(self.flow_system.scalar_field - self.error_matrix)
        self.error = np.max(np.max(self.error_matrix))
        
        if  self.error < self.tolerance: 
            print "converged!", self.error
            return 1
        else:
            return 0
'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np
from scipy import weave


class flow_calc():
    """
    """
    def __init__(self, max_iter, limit_convergence, flow_system):
        self.max_time_steps = max_iter
        self.tolerance = limit_convergence
        self.flow = flow_system
        self.error_matrix = np.zeros((self.flow.n_x, self.flow.n_y))
        self.error = 0
        
    def do_it_gauss_seidel(self):
        iter_n = 0
        onespacing = 1.0 / 4.0
        print "range", self.flow.n_y , self.flow.n_x 
        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.flow.n_y - 1 ):
                for j in xrange(1, self.flow.n_x - 1 ):
                    self.flow.scalar_field[i, j] = onespacing * \
                    (self.flow.scalar_field[i - 1, j] + self.flow.scalar_field[i, j - 1] 
                     + self.flow.scalar_field[i + 1, j] + self.flow.scalar_field[i, j + 1])
            
                    
            #Toroidal conditions
            self.flow.scalar_field[:,0] = self.flow.scalar_field[:,self.flow.n_x - 2]
            self.flow.scalar_field[:,self.flow.n_x -1] = self.flow.scalar_field[:,1]
                    
            
            iter_n = iter_n + 1
            
            if iter_n % 10 == 0:
                #print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                
    def jacobi_numpy(self): #HOLY COW 
        iter_n = 0
        #print "range", self.flow.n_y , self.flow.n_x 
        
        while (iter_n < self.max_time_steps):
            self.flow.scalar_field[1:-1, 1:-1] = (self.flow.scalar_field[2:, 1:-1]
                                                          + self.flow.scalar_field[:-2, 1:-1]+
                                                          self.flow.scalar_field[1:-1, 2:] +
                                                          self.flow.scalar_field[1:-1, :-2] )/4.
                                                          
            
            self.flow.scalar_field[:,0] = self.flow.scalar_field[:,self.flow.n_x - 2]
            self.flow.scalar_field[:,self.flow.n_x -1] = self.flow.scalar_field[:,1]
            
            iter_n = iter_n + 1
            
            if iter_n % 10 == 0:
                #print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
            
    def jacobi_weaver(self): #NOT WORKING
        iter_n = 0
        #print "range", self.flow.n_y , self.flow.n_x 
        field = self.flow.scalar_field
        while (iter_n < self.max_time_steps):
            expr = "field[1:-1, 1:-1] = (field[2:, 1:-1] "\
                                                          "+ field[:-2, 1:-1]+"\
                                                          "field[1:-1, 2:] +"\
                                                          "field[1:-1, :-2] )/4."                                       
            
            weave.blitz(expr, check_size=0)
            
            field[:,0] = field[:,self.flow.n_x - 2]
            field[:,self.flow.n_x -1] = field[:,1]
            
            iter_n = iter_n + 1
            
            if iter_n % 10 == 0:
                #print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    self.flow.scalar_field = field
                    print "total iterations: ", iter_n
                    break
                
            
    def do_it_SOR(self, w):
        iter_n = 0
        onespacing = 1.0 / 4.0
        
        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.flow.n_x -1):
                for j in xrange(1, self.flow.n_y -1):
                    self.flow.scalar_field[i, j] =  self.flow.scalar_field[i,j] + w * (onespacing * \
                    (self.flow.scalar_field[i - 1, j] + self.flow.scalar_field[i, j - 1] + 
                     self.flow.scalar_field[i + 1, j] + self.flow.scalar_field[i, j + 1] - 
                     4.0 * self.flow.scalar_field[i,j]))
             
            
            iter_n = iter_n + 1
            
            if iter_n % 10 == 0:
                print "iteration ", iter_n, "error ", self.error
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                    
                    
    def check_convergence(self):
        self.error_matrix = np.abs(self.flow.scalar_field - self.error_matrix)
        self.error = np.max(np.max(self.error_matrix))
        
        if  self.error < self.tolerance: 
            print "converged!", self.error
            return 1
        else:
            return 0
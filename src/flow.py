'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np

class calculations():
    """
    """
    def __init__(self, max_iter, limit_convergence, system):
        self.max_time_steps = max_iter
        self.tolerance = limit_convergence
        self.system = system
        self.prev_head = (self.system.init_head + 1) * 1000

    def do_it_gauss_seidel(self):
        iter_n = 0
        onespacing = 1.0 / 4.0

        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.system.tot_cells_x - 1):
                for j in xrange(1, self.system.tot_cells_y - 1):
                    self.system.space[i, j] = onespacing * \
                    (self.system.space[i - 1, j] + self.system.space[i, j - 1] + self.system.space[i + 1, j] + self.system.space[i, j + 1])
             
            self.system.space[:,0] = self.system.space[:,self.system.tot_cells_x - 2]
            self.system.space[:,self.system.tot_cells_x -1] = self.system.space[:,1]
                    
            #self.system.space[:, 0] = self.system.space[:, 1]
            #self.system.space[:, self.system.tot_cells_x - 1] = self.system.space[:, self.system.tot_cells_x - 2]  # for boundary conditions copied from inside to the bourders after the run

            iter_n = iter_n + 1
            
            if iter_n % 5 == 0:
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                    
    def do_it_SOR(self, w):
        iter_n = 0
        onespacing = 1.0 / 4.0

        while (iter_n < self.max_time_steps):
            for i in xrange(1, self.system.tot_cells_x - 1):
                for j in xrange(1, self.system.tot_cells_y - 1):
                    self.system.space[i, j] =  self.system.space[i,j] + w * (onespacing * \
                    (self.system.space[i - 1, j] + self.system.space[i, j - 1] + self.system.space[i + 1, j] + self.system.space[i, j + 1] - 4.0 * self.system.space[i,j]))
             
            self.system.space[:,0] = self.system.space[:,self.system.tot_cells_x - 2]
            self.system.space[:,self.system.tot_cells_x -1] = self.system.space[:,1]        
            #self.system.space[:, 0] = self.system.space[:, 1]
            #self.system.space[:, self.system.tot_cells_x - 1] = self.system.space[:, self.system.tot_cells_x - 2]  # for boundary conditions copied from inside to the bourders after the run

            iter_n = iter_n + 1
            
            if iter_n % 5 == 0:
                if self.check_convergence():
                    print "total iterations: ", iter_n
                    break
                    
                    
    def check_convergence(self):
        now_head = np.max(self.system.space[1:self.system.tot_cells_x - 1, :])
        print abs(self.prev_head - now_head)
        
        if abs(self.prev_head - now_head) < self.tolerance: 
            print "converged!", abs(self.prev_head - now_head)
            return 1
        else:
            self.prev_head = now_head 
            return 0
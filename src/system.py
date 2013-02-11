'''
Created on 19/10/2012

@author: ispmarin
'''
import aux_func
import phreeqc_interface
import numpy as np

class system_def():
    """
    """
    def __init__(self, dim_x, dim_y, spacing, init_head, k, porosity):

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.spacing = spacing
        self.n_x = int(aux_func.rounda(self.dim_x , self.spacing) + 1)  # for the boundary conditions
        self.n_y = int(aux_func.rounda(self.dim_y , self.spacing) + 1)  # for the boundary conditions
        self.scalar_field = np.ones((self.n_x, self.n_y)) * init_head
        self.init_head = init_head
        self.k = k 
        self.porosity = porosity
        self.geochemistry  = [[] * self.n_x for x in xrange(self.n_y)]
        print "Dimensions x ", self.dim_x, " y ", self.dim_y," n pts x ", self.n_x," n pts y ", self.n_y
        
    def fixed_boundary_conditions(self, head_up, head_down, head_left, head_right):
        self.scalar_field[0, :] = head_up
        self.scalar_field[self.n_x - 1, :] = head_down
        self.scalar_field[:,0] = head_left
        self.scalar_field[:,self.n_y - 1] = head_right
        
    def line_boundary_conditions(self, head_up, head_down, head_left, head_right):
        self.scalar_field[0, :] = np.linspace(head_down, head_up, self.n_x)
        self.scalar_field[self.n_x - 1, :] = head_down
        self.scalar_field[:,0] = head_left
        self.scalar_field[:,self.n_y - 1] = head_right
        
    def set_geochemistry(self, phreeqc_input_file):
        for i in xrange(self.n_y):
            for j in xrange(self.n_x):
                self.geochemistry[i].append( phreeqc_interface.phreeqc_interface(phreeqc_input_file))
                
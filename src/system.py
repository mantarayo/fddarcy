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
        self.geochemistry  = [[] * dim_x for x in xrange(dim_y)]
        
    def fixed_boundary_conditions(self, concentration_up, concentration_down):
        self.scalar_field[0, :] = concentration_up
        self.scalar_field[self.n_x - 1, :] = concentration_down

    def line_boundary_conditions(self, head_up, head_down):
        self.scalar_field[0, :] = np.linspace(head_down, head_up, self.n_x)
        self.scalar_field[self.n_x - 1, :] = head_down
    
    def set_geochemistry(self, phreeqc_input_file):
        for i in xrange(self.dim_y):
            for j in xrange(self.dim_x):
                self.geochemistry[i].append( phreeqc_interface.phreeqc_interface(phreeqc_input_file))
                
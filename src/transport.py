'''
Created on 07/02/2013

@author: ispmarin
'''

import advection
import phreeqc_interface

class transport_reaction(object):
    
    def __init__(self, n_components):
        self.n_components = n_components
        
    
    def time_step(self, advection_field):
        advection_field.advection_step()
        
        
        


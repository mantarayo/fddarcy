'''
Created on 07/02/2013

@author: ispmarin
'''

import numpy as np

class transport_reaction(object):
    
    def __init__(self):
       pass
   
    def transport_only(self, advection):
        
        for t in xrange(advection.max_time_steps):     
            advection.advect_step_numpy()
            t = t + 1
        
    
    def transport_only_old(self, advection_field):
        
        for t in xrange(advection_field.max_time_steps):     
            advection_field.advect_step()
            t = t + 1
        
    
    def transport_geochemistry(self, advection_field, geochemistry, workhorse):
        conc = np.zeros((workhorse.n_x, workhorse.n_y))
        keys = geochemistry[0][0].get_selected_output()
        
        for t in xrange(self.max_time_steps):
            for ke in keys:
                for i in xrange(workhorse.n_y):
                    for j in xrange(workhorse.n_x):
                        conc[i][j] = geochemistry[i][j].get_selected_output()[ke][0]
    
                advection_field.advect_step_numpy(conc)
                
                for i in xrange(workhorse.n_y):
                    for j in xrange(workhorse.n_x):
                        geochemistry[i][j].run_model()
                        
            t = t + 1
        
        


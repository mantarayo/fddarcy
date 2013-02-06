'''
Created on 22/10/2012

@author: Ivan Marin
@contact: ispmarin@gmail.com
'''
#import copy
#import textwrap
#import time

import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod

class phreeqc_conc(object):
    '''
    classdocs
    '''

    def __init__(self, phreeqc_input_file):
        '''
        Constructor
        '''
        self.phreeqc = phreeqc_mod.IPhreeqc()
        self.phreeqc.load_database(r"/home/ispmarin/src/lib/phreeqc-2.18.3/database/phreeqc.dat")
        self.phreeqc.run_string(self.load_ph_file(phreeqc_input_file))
        
        print self.phreeqc.get_selected_output_array()

    def solution_modify(self, concentration):
        modify_the_solution = """
        MODIFY 1
           -totals 
               CO2   1.0
            RUN_CELLS 1
        END
        """
        return modify_the_solution
    def make_selected_output(self,components):
        """
        Build SELECTED_OUTPUT data block
        General? NO!
        """

    
    def get_selected_output(self,phreeqc):
        """Return calculation result as dict.
    
        Header entries are the keys and the columns
        are the values as lists of numbers.
        """
        
        output = phreeqc.get_selected_output_array()

        header = output[0]
        conc = {}
        
        for head in header:
            conc[head] = []
            
        for row in output[1:]: #is it necessary to do the [1:]?
            for col, head in enumerate(header):
                conc[head].append(row[col])
        
        return conc
    
    def load_ph_file(self, phreeqc_input_file):
        
        ph_file = open(phreeqc_input_file, 'r').read()
        
        return ph_file
        
    def geochem_run(self):
        
        conc = self.get_selected_output(self.phreeqc)
        all_names = conc.keys()
        names = [name for name in all_names if name not in ('cb', 'H', 'O')]
        modify = []
        modify.append("SOLUTION_MODIFY %d" % 0)
        modify.append("\t-cb      %e" % conc['cb'][0])
        modify.append("\t-total_h %f" % conc['H'][0])
        modify.append("\t-total_o %f" % conc['O'][0])
        modify.append("\t-totals")
        for name in names:
            modify.append("\t\t%s\t%f" % (name, conc[name][0]))
        modify.append("RUN_CELLS; -cells 0\n" )
        cmd = '\n'.join(modify)
        self.phreeqc.run_string(cmd)
        conc = self.get_selected_output(self.phreeqc)
        
        return conc
       
        
   
        
        

'''
Created on 22/10/2012

@author: Ivan Marin
@contact: ispmarin@gmail.com
'''
import copy
import textwrap
import time

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
        self.phreeqc.load_database(r"/home/ispmarin/src/laval/phreeqc-2.18.3/database/phreeqc.dat")
        print self.load_ph_file(phreeqc_input_file)
        self.phreeqc.run_string(self.load_ph_file(phreeqc_input_file))
        
        #solution initialization
        components = self.phreeqc.get_component_list()
        selected_output = self.make_selected_output(components)
        self.phreeqc.run_string(selected_output)
        phc_string = "RUN_CELLS; -cells 0\n"
        self.phreeqc.run_string(phc_string)
        
    
    def make_selected_output(self,components):
        """
        Build SELECTED_OUTPUT data block
        General? NO!
        """
        
        headings = "-headings    cb    H    O    "
        
        for i in range(len(components)):
            headings += components[i] + "\t"
            
        selected_output = """
        SELECTED_OUTPUT
            -reset false
        USER_PUNCH
        """
        
        selected_output += headings + "\n"
        #
        # charge balance, H, and O
        #
        code = '10 w = TOT("water")\n'
        code += '20 PUNCH CHARGE_BALANCE, TOTMOLE("H"), TOTMOLE("O")\n'
        #
        # All other elements
        #
        lino = 30
        
        for component in components:
            code += '%d PUNCH w*TOT(\"%s\")\n' % (lino, component)
            lino += 10
        
        selected_output += code
        
        return selected_output
    
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
       
        
        
        
        
        
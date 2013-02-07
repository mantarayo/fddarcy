'''
Created on 22/10/2012

@author: Ivan Marin
@contact: ispmarin@gmail.com
'''
#import copy
#import textwrap
#import time
import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod

class phreeqc_interface(object):
    '''
    classdocs
    '''

    def __init__(self, phreeqc_input_file):
        '''
        Constructor
        '''
        self.phreeqc = phreeqc_mod.IPhreeqc()
        self.phreeqc.load_database(r"/home/ispmarin/src/lib/phreeqc-2.18.3/database/phreeqc.dat")
        self.phreeqc.run_string(open(phreeqc_input_file, 'r').read())
        self.phreeqc.run_string(self.set_selected_output())
        self.run_model()
        self.all_names = self.get_selected_output().keys()
        
        
    def run_model(self):
        phc_string = "RUN_CELLS; -cells 1\n"
        self.phreeqc.run_string(phc_string)
        
    def set_selected_output(self):
        """
        Build SELECTED_OUTPUT data block
        """
        components = self.phreeqc.get_component_list()
        
        
        headings = "-headings    cb    H    O    "
        for i in range(len(components)):
            headings += components[i] + "\t"
        selected_output = """
        SELECTED_OUTPUT
            -reset false
            -high_precision
        USER_PUNCH
        """
        selected_output += headings + "\n"
        
        code = '10 PUNCH CHARGE_BALANCE, TOTMOLE("H"), TOTMOLE("O")\n'
        lino = 20
        for component in components:
            code += '%d PUNCH TOT(\"%s\")\n' % (lino, component)
            lino += 10
        selected_output += code
        return selected_output
    
    def get_selected_output(self):
        """Return calculation result as dict.
    
        Header entries are the keys and the columns
        are the values as lists of numbers.
        """
        output = self.phreeqc.get_selected_output_array()

        header = output[0]
        conc = {}
        
        for head in header:
            conc[head] = []
            
        for row in output[1:]: #is it necessary to do the [1:]?
            for col, head in enumerate(header):
                conc[head].append(row[col])
        
        print conc
        return conc
        
    def geochem_modify(self, transp_conc):
   
        names = [name for name in self.all_names if name not in ('cb', 'H', 'O')]
        modify = []
        modify.append("SOLUTION_MODIFY %d" % 1)
        modify.append("\t-cb      %e" % transp_conc['cb'][0])
        modify.append("\t-total_h %f" % transp_conc['H'][0])
        modify.append("\t-total_o %f" % transp_conc['O'][0])
        modify.append("\t-totals")
        for name in names:
            modify.append("\t\t%s\t%f" % (name, transp_conc[name][0]))
        modify.append("RUN_CELLS; -cells 0\n" )
        cmd = '\n'.join(modify)
        self.phreeqc.run_string(cmd)
        transp_conc = self.get_selected_output()
        
        return transp_conc
    
    #def to_transport(self, transp_conc):
        
        
       
        
   
        
        

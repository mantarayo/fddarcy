'''
Created on 22/10/2012

@author: Ivan Marin
@contact: ispmarin@gmail.com
'''
import copy
import textwrap
import time

class phreeqc_interface(object):
    '''
    classdocs
    '''

    def __init__(self,):
        '''
        Constructor
        '''
        
        MODE = 'dll' # 'dll' or 'com'

        if MODE == 'com':
            import phreeqpy.iphreeqc.phreeqc_com as phreeqc_mod
        elif MODE == 'dll':
            import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod
        else:
            raise Exception('Mode "%s" is not defined use "com" or "dll".' % MODE)
        
        
        

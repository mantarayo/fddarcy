'''
Created on 15/10/2012

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

class plotter(object):
    '''
    Class to plot the results
    '''
    
    def __init__(self, tot_cells_x, tot_cells_y,  num_isoline):
        '''
        Constructor
        '''
        
        self.dim_x = tot_cells_x 
        self.dim_y = tot_cells_y
        self.num_isolines = num_isoline
        
        
    def plot_velocity(self, velx, vely):
        
          
        fig0 = plt.figure()
        ax = fig0.add_subplot(111)
        ax.quiver(velx, vely, angles='xy')
        
        plt.show()
        
    def test_velocity(self):
        X,Y = np.meshgrid( np.arange(0,10,.2),np.arange(0,10,.2) )
        U = X
        V = Y 
        fig0 = plt.figure()
        ax = fig0.add_subplot(111)
        ax.quiver(U, V, anglex='xy')
        
    
    def plot_head(self, plot_type, matrix):
        '''
        Plot the head
        '''
        
        print('plotting...')
                
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        
        #formatter = FuncFormatter(lambda x,pos: ("%.2e"%x).replace(".",","))
        formatter = FuncFormatter(lambda x, pos: ("%g"%x).replace(".",","))

        fig0 = plt.figure()
        fig0.suptitle("Carga (m)")
        ax = fig0.add_subplot(111)
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        cs = ax.contourf(matrix, self.num_isolines)
        cs2 = ax.contour(matrix, self.num_isolines, linewidths=0.6, colors='black')
        ax.clabel(cs2, inline=1,fontsize=8)
        fig0.colorbar(cs,format=formatter)
        
        if plot_type == 'file':
            save_name1 = '_head_' + str(self.low_head_lines) +  '.pdf'
            plt.savefig(save_name1,  facecolor='w', edgecolor='w',
                        format='pdf',bbox_inches='tight')
        elif plot_type == 'screen':
            plt.show()
        else:
            print('No plot for you.')
        plt.close()
        
    def plot_head_random(self, randomguy,system):
        """
        """
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #for i in xrange(randomguy.total_time):
        for j in xrange(randomguy.particle_num):
            ax.plot(randomguy.particle_time_step[randomguy.total_time - 1][j][0], randomguy.particle_time_step[randomguy.total_time - 1][j][1], 'o')
            #ax.plot(randomguy.particle_time_step[0][j][0], randomguy.particle_time_step[0][j][1], 'o')
        
        cs = ax.contourf(system.space, self.num_isolines)
        cs2 = ax.contour(system.space, self.num_isolines, linewidths=0.6, colors='black')
        plt.show()

'''
Created on 16/03/2011

@author: ispmarin
'''
#import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
#import numpy as np
#from mpl_toolkits.mplot3d import  Axes3D


class plotter(object):
    '''
    Class to plot the results
    '''
    
    def __init__(self, tot_cells_x, tot_cells_y,  num_isoline, space):
        '''
        Constructor
        '''
        
        self.dim_x = tot_cells_x 
        self.dim_y = tot_cells_y
        self.num_isolines = num_isoline
        self.a = space
        
    def plot_velocity(self, velx, vely):
        
          
        fig0 = plt.figure()
        ax = fig0.add_subplot(111)
        ax.quiver(velx, vely)
        
        plt.show()
        
      
    
    def plot_head(self, plot_type):
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
        cs = ax.contourf(self.a, self.num_isolines)
        cs2 = ax.contour(self.a, self.num_isolines, linewidths=0.6, colors='black')
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
        
    def plot_head_random(self, randomguy):
        """
        """
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #for i in xrange(randomguy.total_time):
        for j in xrange(randomguy.particle_num):
            ax.plot(randomguy.particle_time_step[randomguy.total_time - 1][j][0], randomguy.particle_time_step[randomguy.total_time - 1][j][1], 'o')
            #ax.plot(randomguy.particle_time_step[0][j][0], randomguy.particle_time_step[0][j][1], 'o')
        
        cs = ax.contourf(self.a, self.num_isolines)
        cs2 = ax.contour(self.a, self.num_isolines, linewidths=0.6, colors='black')
        plt.show()

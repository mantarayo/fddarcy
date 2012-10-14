'''
Created on 16/03/2011

@author: ispmarin
'''
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from mpl_toolkits.mplot3d import  Axes3D


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
        
    def plot_velocity(self, element_list, uniform_flow, aquifer):
        
          
        (velx,vely) =  np.gradient(self.a, self.sample_distance_x, self.sample_distance_y)
        
        fig0 = plt.figure()
        ax = fig0.add_subplot(111)
        
        k_surf = np.zeros([self.len_x, self.len_y], dtype=float)
        
        Q = ax.quiver(self.X,self.Y, -velx, -vely )
        
        fig1= plt.figure(2)
        ax2 = Axes3D(fig1)
        surf = ax2.plot_surface(self.X,self.Y, k_surf, cmap=matplotlib.cm.jet, alpha=0.3)
        #surf = ax2.plot_surface(self.X,self.Y,vely, cmap=matplotlib.cm.jet, alpha=0.3)
        fig1.colorbar(surf, shrink=0.5, aspect=5)
        
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
        

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
    
    def __init__(self, n_x, n_y,  num_isolines):
        '''
        Constructor
        '''
        
        self.dim_x = n_x 
        self.dim_y = n_y
        self.num_isolines = num_isolines
        
        
        
    def plot_head_random(self, randomguy, scalar_field):
        """
        """
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #for i in xrange(randomguy.total_time):
        for j in xrange(randomguy.particle_num):
            ax.plot(randomguy.particle_time_step[randomguy.total_time - 1][j][0], randomguy.particle_time_step[randomguy.total_time - 1][j][1], 'o')
            #ax.plot(randomguy.particle_time_step[0][j][0], randomguy.particle_time_step[0][j][1], 'o')
        
        ax.contourf(scalar_field, self.num_isolines)
        ax.contour(scalar_field, self.num_isolines, linewidths=0.6, colors='black')
        plt.show()



    def plot_scalar(self,scalar_field, num_isolines, dim_x, dim_y, spacing, n_x, n_y):

        plt.rcParams['contour.negative_linestyle'] = 'solid'

        formatter = FuncFormatter(lambda x, pos: ("%g"%x).replace(".",","))

        x_axis = np.linspace(0,dim_x,num=n_x)
        y_axis = np.linspace(0,dim_y,num=n_y)
        
        fig0 = plt.figure()
        ax = fig0.add_subplot(111)
        cs = ax.contourf(x_axis, y_axis, scalar_field, num_isolines)
        ax.contour(x_axis, y_axis,scalar_field, num_isolines, linewidths=0.6, colors='black')
        fig0.colorbar(cs,format=formatter)

        plt.show()
        plt.close()

    def plot_velocity(self,velx, vely, dim_x, dim_y, n_x, n_y):
        
        x_axis = np.linspace(0,dim_x,num=n_x)
        y_axis = np.linspace(0,dim_y,num=n_y)
        fig0 = plt.figure()
        ax = fig0.add_subplot(111)
        ax.quiver(x_axis, y_axis, velx, vely, angles='xy')
        plt.show()
        plt.close()

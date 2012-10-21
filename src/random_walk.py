'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate 


def rounda(nume, deno):
    return (nume + deno // 2) // deno

class random_walk():
    """
    """

    def __init__(self, seed, deltaT, total_time, particle_num, DL, DT, init_position, spacing, velx, vely, n_x, n_y, scalar_field, dim_x, dim_y):
        self.seed = seed
        self.deltaT = deltaT
        self.total_time = total_time
        self.particle_num = particle_num
        self.DL = DL
        self.DT = DT
        self.spacing = spacing
        self.n_x = n_x
        self.n_y = n_y
        self.particle_list = []
        self.particle_time_step = []
        self.scalar_field = scalar_field
        self.velx = velx
        self.vely = vely
        self.dim_x = dim_x
        self.dim_y= dim_y
        for i in xrange(self.particle_num):
            self.particle_list.append(init_position)
     
    def do_the_walk(self):
        time = 0

        fig = plt.figure()
        ax = fig.add_subplot(111)
        #ax.contourf(self.scalar_field, 10)
        #ax.contour(self.scalar_field, 10, linewidths=0.6, colors='black')
        for i in xrange(self.particle_num):
            ax.plot(self.particle_list[i][0], self.particle_list[i][1], 'o-')

        print "doing the random walk"
        while time <= self.total_time:
            for i in xrange(self.particle_num):
                XL = np.random.standard_normal()
                XT = np.random.standard_normal()
                
                x_axis = np.linspace(0,self.dim_x,num=self.n_x)
                y_axis = np.linspace(0,self.dim_y,num=self.n_y)
                
                inter_velx = scipy.interpolate.RectBivariateSpline(x_axis, y_axis, self.velx)
                inter_vely = scipy.interpolate.RectBivariateSpline(x_axis, y_axis, self.vely)               
                vx = inter_velx.ev(self.particle_list[i][0], self.particle_list[i][1])
                vy = inter_vely.ev(self.particle_list[i][0], self.particle_list[i][1])
                modv = np.sqrt(vx ** 2 + vy ** 2) 

                
                x = self.particle_list[i][0] + vx * self.deltaT + np.sqrt(2.0 * self.DL * self.deltaT) * XL * (vx / modv) - np.sqrt(2.0 * self.DT * self.deltaT) * XT * (vy / modv)
                y = self.particle_list[i][1] + vy * self.deltaT + np.sqrt(2.0 * self.DL * self.deltaT) * XL * (vy / modv) - np.sqrt(2.0 * self.DT * self.deltaT) * XT * (vx / modv)
                
   
                if x >= self.dim_x or y >= self.dim_y or x < 0  or y < 0:  # reached the borders
                    print "break!"
                    break
                
                self.particle_list[i] = (x, y)
                print "x, y", x, y, vx, vy, vx * self.deltaT, vy * self.deltaT
 
            self.particle_time_step.append(self.particle_list)
            time = time + 1
        
        
        for i in xrange(self.particle_num):
            ax.plot(self.particle_list[i][0], self.particle_list[i][1], 'o')
       
        plt.show()
        print "finished the random walk"

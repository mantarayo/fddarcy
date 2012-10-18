'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''

import numpy as np
import aux_func

class random_walk():
    """
    """

    def __init__(self, seed, deltaT, total_time, particle_num, DL, DT, init_position, system):
        self.seed = seed
        self.deltaT = deltaT
        self.total_time = total_time
        self.particle_num = particle_num
        self.DL = DL
        self.DT = DT
        self.cell_spacing = system.cell_spacing
        self.velx, self.vely = aux_func.calculate_velocity(system)
        
        self.particle_list = []
        self.system = system
        self.particle_time_step = []
        for i in xrange(self.particle_num):
            self.particle_list.append(init_position)
    
    def do_the_walk(self):
        time = 0
        print "doing the random walk"
        while time <= self.total_time:
            for i in xrange(self.particle_num):
                XL = np.random.random()
                XT = np.random.random()

                index_i = aux_func.rounda(self.particle_list[i][0], self.cell_spacing)
                index_j = aux_func.rounda(self.particle_list[i][1], self.cell_spacing)
                
                if index_i >= self.system.tot_cells_x - 1 or index_j >= self.system.tot_cells_y - 1 or index_i <= 0 or index_j <= 0:  # reached the borders
                    break
                
                print "index_i, index_j", index_i, index_j
                
                vx = self.velx[index_i, index_j]
                vy = self.vely[index_i, index_j]
                modv = np.sqrt(vx ** 2 + vy ** 2) 
                
                x = self.particle_list[i][0] + vx * self.deltaT + np.sqrt(2.0 * self.DL * self.deltaT) * XL * (vx / modv) - np.sqrt(2.0 * self.DT * self.deltaT) * XT * (vy / modv)
                y = self.particle_list[i][1] + vy * self.deltaT + np.sqrt(2.0 * self.DL * self.deltaT) * XL * (vy / modv) - np.sqrt(2.0 * self.DT * self.deltaT) * XT * (vx / modv)
                
                print self.particle_list[i][0], self.particle_list[i][1]
                self.particle_list[i] = (x, y)
 
            self.particle_time_step.append(self.particle_list)
            time = time + 1
        print "finished the random walk"

'''
Created on 2012-10-17

@author: Ivan Marin
@email: ispmarin@gmail.com
'''
import sys
import random_walk
import output
import flow
import aux_func
import system
import advection
#import phreeqc_interface
import transport


def main():

    dim_x = 20
    dim_y = 20
    spacing = 0.125
    num_isolines = 20
    init_head = 1
    k = 1
    porosity = 1
    head_up = 1
    head_down = 0
    head_left = 0
    head_right = 0
    max_iter = 9500
    limit_convergence = 1e-5
    deltaT = 0.125#aux_func.calculate_courant(spacing, velx, vely)
    background_c = 0
    #w = 1.8

    workhorse = system.system_def(dim_x, dim_y, spacing, init_head, k, porosity)
    workhorse.fixed_boundary_conditions(head_up, head_down,head_left, head_right )   
    #workhorse.set_geochemistry('xylene.phrq')
    
    
    darcy = flow.flow_calc(max_iter, limit_convergence, workhorse)
    #darcy.do_it_gauss_seidel()
    #darcy.jacobi_numpy()
    darcy.jacobi_weaver(1)
    
    velx, vely = aux_func.calculate_velocity(workhorse.n_x, workhorse.n_y, spacing, workhorse.scalar_field, workhorse.k/workhorse.porosity)
    
    adv = advection.advection(deltaT, velx, vely, background_c, max_iter, workhorse)
    #adv.fixed_boundary_conditions(1, 0, 0, 0)
    adv.set_region_bc(dim_x/2,dim_y/2 , (dim_x+2)/2, (dim_y+2)/2, 3)
    
    
    transport_stuff = transport.transport_reaction()
    transport_stuff.transport_only(adv)
    #transport_stuff.transport_geochemistry(adv, workhorse.geochemistry, workhorse)
    
    plotter = output.plotter(workhorse.n_x, workhorse.n_y, num_isolines)
    plotter.plot_scalar(workhorse.scalar_field, num_isolines, dim_x, dim_y, spacing, workhorse.n_x, workhorse.n_y, "Head")
    plotter.plot_velocity(velx, vely, dim_x, dim_y, workhorse.n_x, workhorse.n_y)
    plotter.plot_scalar(adv.conc, num_isolines, dim_x, dim_y, spacing, workhorse.n_x, workhorse.n_y, "Concetration")
    

#    deltaT = 0.5#calculate_courant(spacing, velx, vely)
#    print deltaT
#    seed = 1
#    max_iter_time = 20
#    particle_num =  10
#    DL = 0.1
#    DT=0.01
#    init_position = (1, 1)
#    randd = random_walk.random_walk(seed, deltaT, max_iter_time, particle_num, 
#                                    DL, DT, init_position, spacing, velx, vely, workhorse.n_x, workhorse.n_y,workhorse.scalar_field, dim_x, dim_y)
#    randd.do_the_walk()
#    #plotter.plot_head_random(randd,scalar_field)
    
if __name__ == "__main__":
    sys.exit(main())

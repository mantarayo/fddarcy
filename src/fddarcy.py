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
import phreeqc_conc


def main():

    dim_x = 30
    dim_y = 30
    spacing = 0.25
    num_isolines = 10
    init_head = 0
    k = 1
    porosity = 1
    w = 1.9
    head_up = 100
    head_down = 80
    
    workhorse = system.system_def(dim_x, dim_y, spacing, init_head, k, porosity)
    workhorse.fixed_boundary_conditions(head_up, head_down)   

    
    #freak = phreeqc_conc.phreeqc_conc('calcite.ph')
    #freak = phreeqc_conc.phreeqc_conc('input.dat')    
    #conc = freak.geochem_run()
    
    #print conc
    max_iter = 1000
    limit_convergence = 1e-3
    
    darcy = flow.flow_calc(max_iter, limit_convergence, workhorse)
    darcy.do_it_SOR(w)
    

    plotter = output.plotter(workhorse.n_x, workhorse.n_y, num_isolines)
    plotter.plot_scalar(workhorse.scalar_field, num_isolines, dim_x, dim_y, spacing, workhorse.n_x, workhorse.n_y)
    
    velx, vely = aux_func.calculate_velocity(workhorse.n_x, workhorse.n_y, spacing, workhorse.scalar_field)
    plotter.plot_velocity(velx, vely, dim_x, dim_y, workhorse.n_x, workhorse.n_y)
    

    deltaT = 0.5#calculate_courant(spacing, velx, vely)
    print deltaT
    seed = 1
    max_iter_time = 20
    particle_num =  10
    DL = 0.1
    DT=0.01
    init_position = (1, 1)
    randd = random_walk.random_walk(seed, deltaT, max_iter_time, particle_num, 
                                    DL, DT, init_position, spacing, velx, vely, workhorse.n_x, workhorse.n_y,workhorse.scalar_field, dim_x, dim_y)
    randd.do_the_walk()
    #plotter.plot_head_random(randd,scalar_field)
    
    deltaT = aux_func.calculate_courant(spacing, velx, vely)
    background_c = 0
    max_iter = 10
    adv = advection.advection(deltaT, velx, vely, background_c, max_iter, workhorse)
    adv.fixed_boundary_conditions(1, 0)
    adv.do_it_conc()
    plotter.plot_scalar(adv.c2, num_isolines, dim_x, dim_y, spacing, workhorse.n_x, workhorse.n_y)
    

    
if __name__ == "__main__":
    sys.exit(main())

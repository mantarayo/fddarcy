DATABASE phreeqc.dat                 # contains the PWP calcite rate
RATES
 Calcit2 # simplified rate...
 -start
 10 rate = 10^-6.91 - 10^-1.52 * (tot("Ca"))^2   # mmol/cm2/s
 20 save 1 * rate * time                         # integrate in moles/L
 -end
SOLUTION 1
 temp 10; pH 6 charge; C 1 CO2(g) -1.5
EQUILIBRIUM_PHASES 1
 CO2(g) -1.5

KINETICS 1
 Calcit2; formula CaCO3; -m0 1; -step 30000 in 20
INCREMENTAL_REACTIONS

USER_GRAPH
 -head time Ca pH; -axis_titles "Time / 1000s" "Ca / mM" "pH"
 -start
 10 graph_x total_time/1e3; 20 graph_y tot("Ca")*1e3; 30 graph_sy -la("H+")
 -end
END

                                    # Simulation 2, using the parent PWP rate...
USE solution 1; USE equilibrium_phases 1
KINETICS 1
 Calcite; -m0 1; -parms 10 0.67; -step 30000 in 20
END

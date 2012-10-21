# fddarcy: Finite Difference Darcy #

Ivan Marin
ispmarin@gmail.com
14-Oct-2012 Québec

This is a simple finite difference solver for Darcy equation (actually the continuity equation in the form of a Laplace Equation). It has only two boundary conditions, one at the top and one at the bottom, with fixed heads. It also uses the imaginary boundary notes for that. 

The model includes a FD solver with central difference for estationary flow, a random walk for the advection-diffusion equation and a finite difference LAX scheme for the advection equation. 

## Output ##

The output uses matplotlib and the output.py, a simplified version of my output routines used in pyaem.

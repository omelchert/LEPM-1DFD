import sys; sys.path.append('../../../src/')
from domain import *
from detector import *
from opticalAbsorption import *
from stressWavePropagation1DSLDE import *
import matplotlib.pyplot as plt

def main():
     # SIMULATION PARAMETERS 
     Nt = 50000
     zMax, Nz = 9.55, 8600        

     # SET LAYER STRUCTURE OF MEDIUM
     # LayerNo: ((zMin, zMax), (c, rho, mua))
     # Units: [c]=mm/mus, [rho]=mg/mm, [mua]=1/mm
     # (1) PMMA, (2) Glue, (3) PVDF, (4) Ink, (5) Glass
     layers = {
         1: ((0.000, 5.500), (2.77, 1.18, 0.000)), 
         2: ((4.980, 5.020), (2.50, 1.00, 0.000)), 
         3: ((4.995, 5.005), (2.25, 1.78, 0.000)), 
         4: ((5.500, 5.550), (1.80, 1.00, 100.0)), 
         5: ((5.550, 9.550), (5.60, 2.23, 0.000))  
     }

     # INSTANCE OF COMPUTATIONAL DOMAIN
     Glob = Domain((0.,zMax), Nz)
     # INSTANCE OF DETECOR FOR MONITORING OBSERVABLES
     Det  = PiezoTransducer(Glob, (4.995,5.005))

     # ASSIGN LAYER PROPERTIES TO COMPUTATIONAL DOMAIN
     for no, (zR, (c, rho, mu)) in \
             sorted(layers.iteritems()):
         Glob.setProperty(Glob.v, zR, c) 
         Glob.setProperty(Glob.rho, zR, rho)                 
         Glob.setProperty(Glob.mua, zR, mu)

     # OPTICAL ABSORPTION
     p0 = absorbLaserBeam(Glob)

     # ACOUSTIC PROPAGATION
     p = propagateStressWaveSLDE(
         (p0, Glob.v, Glob.rho, Glob.dz ), Det.measure,Nt)

     # DISPLAY RESULTS 
     plt.plot(Det.t,Det.U/max(Det.U))
     plt.title('Response of piezoelectric sensing layer')
     plt.xlabel('t (mu s)')
     plt.ylabel('U(t) (arb. units)')
     plt.show()


main()

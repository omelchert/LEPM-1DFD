import sys; sys.path.append('../../../src/')
from opticalAbsorption import *
from stressWavePropagation1DSLDE import *
from myDetector import *
from domain import *
from timeDomainFilter import *

def setDomain():
        # computational domain parameters 
        zMax = 9.55
        Nz = 8600
        # parameters for optical absorption 
        Gamma = 1. 
        I0 = 1.
        tp = 0.01
        # detector position
        zDet = 5.

        # instance of computational domain
        Glob = Domain((0.,zMax), Nz)
        # instance of detecor for monitoring observables
        #Det  = PiezoTransducer(Glob, (4.995,5.005))
        Det = StressMonitor(Glob)

        # set layer structure of medium in format:
        # LayerNo: ((zMin, zMax), (c, rho, mua))
        # Units: [c] = km/s = mm/mus, [rho] = kg/dm3 = mg/mm, [mua] = 1/mm
        layers = {
            1: ((0.000, 5.500), (2.77, 1.18, 0.000)), # PMMA layer
            2: ((4.980, 5.020), (2.50, 1.00, 0.000)), # Glue layer
            3: ((4.995, 5.005), (2.25, 1.78, 0.000)), # PVDF
            4: ((5.500, 5.550), (1.80, 1.00, 100.0)), # Ink
            5: ((5.550, 9.550), (5.60, 2.23, 0.000))  # Glass
        }

        # assign layer properties to computational domain
        for no, (zRange, (c, rho, mu)) in sorted(layers.iteritems()):
            Glob.setWaveVelocity(zRange, c) 
            Glob.setDensity(zRange, rho)                 
            Glob.setAbsorbingLayer(zRange, mu)
        
        return Glob, Det


def main():
        Nt = 25000
        Gamma = 1.0
        I0 = 1.0
        d = 0.05 

        Glob,Det = setDomain()
        p0 = absorbLaserBeam(Glob,Gamma,I0,d)

        p = propagateStressWaveSLDE((p0, Glob.v, Glob.rho, Glob.dz ),Det.measure,Nt)



main()

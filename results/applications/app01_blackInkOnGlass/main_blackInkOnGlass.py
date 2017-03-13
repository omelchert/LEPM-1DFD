import sys; sys.path.append('../../../src/')
from opticalAbsorption import *
from stressWavePropagation1DSLDE import *
from detector import *
from domain import *
from timeDomainFilter import *
from domain2svg import *

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
        Det  = PiezoTransducer(Glob, (4.995,5.005))

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

#        svg(layers,'./data/domain.svg')
#        exit()
        # assign layer properties to computational domain
        for no, (zRange, (c, rho, mu)) in sorted(layers.iteritems()):
            Glob.setWaveVelocity(zRange, c) 
            Glob.setDensity(zRange, rho)                 
            Glob.setAbsorbingLayer(zRange, mu)
        
        return Glob, Det


def main():
        Nt = 70000
        Gamma = 1.0
        I0 = 1.0
        d = 0.05 
        a = 0.0012

        Glob,Det = setDomain()
        p0 = absorbLaserBeam(Glob,Gamma,I0,d)

        p = propagateStressWaveSLDE((p0, Glob.v, Glob.rho, Glob.dz ),Det.measure,Nt)

        t, p, ps = Det.t, Det.U, Det.Us
        (pLP, tau, omega) = Filter(t,p).lowPass(a)
        n1 = 1./max(p)
        n2 = 1./max(pLP)
        n3 = 1./max(ps)
        for i in range(len(t)):
                print t[i], n1*p[i], n2*pLP[i], n3*ps[i]

        print "# dt    =", t[1]-t[0]
        print "# tau   =", tau
        print "# omega =", omega


main()

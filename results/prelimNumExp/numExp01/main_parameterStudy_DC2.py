import sys; sys.path.append('../../../src/')
from opticalAbsorption import *
from stressWavePropagation1DSLDE import *
from detector import *
from domain import *
from domain2svg import *

def setDomain():
        """intialize computational domain

        Set layered structure of computational domain 

        Args: (None) 

        Returns:
            Glob (object): data structure holding properties of domain
        """
        dDet = 0.025 # width of sensing layer

        # computational domain parameters 
        zR, Nz = (-dDet, 1.), 3000
        zDetR = (-dDet, 0.0)

        # set layer structure of medium in format:
        # LayerNo: ((zMin, zMax), (c, rho))
        # Units: [c] = km/s = mm/mus, [rho] = kg/dm3 = mg/mm
        layers = {
            0: (   zR, (1.50, 1.00)), 
            1: (zDetR, (2.30, 1.82))
        }

        svg(layers,'./data/domain_noBL.svg')

        # instance of computational domain
        Glob = Domain(zR, Nz)
        # instance of detecor for monitoring observables
        Det  = PiezoTransducer(Glob, zDetR)

        # assign layer properties to computational domain
        for no, (zRange, (c, rho)) in sorted(layers.iteritems()):
            Glob.setProperty(Glob.v,zRange, c) 
            Glob.setProperty(Glob.rho,zRange, rho)                 

        return Glob, Det


def main():

        # configure computational domain
        Glob, Det = setDomain()

        # determine number of timesteps  
        Nt = int(3.*max(Glob.v)/Glob.dz/0.3)

        # set initial acoustic stress distribution
        p0 = deltaPulse(Glob,(0.40,0.45))
        # propagate stress wave and detect signal
        p = propagateStressWaveSLDE((p0, Glob.v, Glob.rho, Glob.dz ),Det.measure,Nt)

        Det.dumpSignal()


main()

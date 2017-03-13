import sys
import numpy as np

class PiezoTransducer(object):
    """Piezoelectric transducer data structure
    """
    def __init__(self,Glob,(zMin,zMax),h=1.):
        """initial instance of PiezoTransducer class

        Args:
            Glob (data structure): data structure holding domain configuration 
            (zMin, zMax) (tuple, floats): boundary locations of sensing layer 
            h (float): effective piezoelectric parameter  

        Note: 
            in case of mechanically free setup with open-circuit boundary 
            condition, the effective piezoelectric parameter reads
            h = d / (eT sD),
            wherein d is the piezoelectric strain constant, eT is the dielectric 
            coefficient, and sD is the mechanical compliance (see Refs. [1,2]).

        Refs:
            [1] PVDF piezoelectric polymer
                Ueberschlag, P.
                Sensor Review, 21 (2001) 118-126

            [2] PVDF piezoelectric polymers: characterization and application 
                to thermal energy harvesting
                Gusarov, B. 
                Universite Grenoble Alpes (2015)

        """
        self.dz = Glob.dz
        self.zIdMin = max(1,Glob._z2i(zMin))
        self.zIdMax = Glob._z2i(zMax)
        self.E = np.zeros(self.zIdMax-self.zIdMin)
        self.h = h
        self.t = []
        self.U = []
        self.Us = []

    def measure(self,n,dt,u,tau):
        """method implementing measurement at time instant
        
        Implements finite-difference approximation to state equation for
        direct piezoelectric effect.

        Args:
            n (int): current time step
            dt (float): increment between consequtive times steps
            u (numpy array, ndim=1): velocity profile
            p (numpy array, ndim=1): acoustic stress profile
        
        """
        C = dt/self.dz
        E0 = self.E 
        h = self.h
        zL, zH = self.zIdMin, self.zIdMax

        # evolve electric field within transducer
        self.E[:] = E0[:] - h*C*(u[zL-1:zH-1]-u[zL:zH])

        # determine potential difference across transducer 
        dU = -np.trapz(self.E,dx=self.dz)

        self.t.append(n*dt)
        self.U.append(dU)
        self.Us.append(tau[self.zIdMax])

    def dumpField(self,fName=None):
        """method writing field configuration to file

        Args: 
            fName (str, optional): optional output file-path. If none is given,
                sys.stdout is used instead

        """
        fStream = open(fName,'w') if fName else sys.stdout 
        fStream.write("# (z) (E) \n")
        for i in range(len(self.E)):
            fStream.write("%lf %lf\n"%(self.dz*(self.zIdMin+i),self.E[i]))

    def dumpSignal(self,fName=None):
        """method writing transducer response to file

        Args: 
            fName (str, optional): optional output file-path. If none is given,
                sys.stdout is used instead

        """
        fStream = open(fName,'w') if fName else sys.stdout 
        fStream.write("# (t) (p) \n")
        for i in range(len(self.U)):
            fStream.write("%lf %lf\n"%(self.t[i],self.U[i]))

# EOF: detector.py 

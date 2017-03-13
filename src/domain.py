import sys
import numpy as np


class Domain(object):
    """Data structure for 1D computational domain

    """
    def __init__(self,(zMin,zMax),Nz=1000):
        """initialize instance of 1D Domain

        Args:
            (zMin,zMax) (tuple, floats): boundary points of the 1D domain
            (Nz) (int, default=1000): number of mesh-points for 1D grid 

        """
        (self.z,self.dz) = np.linspace(zMin,zMax,Nz,retstep=True,endpoint=False)
        self.mua = np.zeros(Nz)
        self.rho = np.zeros(Nz)
        self.v  = np.ones(Nz)

    def _z2i(self,zVal):
        """private method returning array index for provided zValue

        Note: zVal must be contained inside 1D domain
        """
        return int((zVal-self.z[0])/self.dz)
    
    def _idxSet(self,zMin,zMax):
        """private method returning boolean mask for provided z-range 

        Note: zMin, zMax must be contained inside 1D domain 
        """
        return np.logical_and( self.z >= zMin, self.z <= zMax)

    def setProperty(self,q,(zMin,zMax),qVal):
        """method that sets properties of domain parameters

        Args:
            q (numpy array, ndim=1): array holding local material property
            (zMin,zMax) (tuple, floats): modification range
            qVal (float): sets q in (zMin,zMax) to qVal
        """
        q[self._idxSet(zMin,zMax)] = qVal

    def setAbsorbingLayer(self,zRange,mua):
        """convenience method to modify local absorption coefficient"""
        self.setProperty(self.mua, zRange, mua)

    def setWaveVelocity(self,zRange,c):
        """convenience method to modify local sonic speed"""
        self.setProperty(self.v, zRange, c)

    def setDensity(self,zRange, rho):
        """convenience method to modify local density"""
        self.setProperty(self.rho, zRange, rho)

    def dumpConfiguration(self,fName=None):
        """method writing domain configuration to file

        Args: 
            fName (str, optional): optional output file-path. If none is given,
                sys.stdout is used instead

        """
        if fName:
            fStream = open(fName,'w')
        else:
            fStream = sys.stdout
                
        fStream.write("# i, z[i], mu[i], v[i], rho[i]\n")
        for i in range(self.z.size):
            fStream.write("%d %lf %lf %lf %lf\n"%
                (i, self.z[i],self.mua[i],self.v[i],self.rho[i]))


    def listCoeffs(self):
         """method listing characteristic coefficients 
         
         Implements method that writes local impedance, transmission and 
         absorption coefficients for right-travelling waves to stdout

         """
         z = self.z
         Z = self.v*self.rho
         Ct = lambda i: 2*Z[i]/(Z[i]+Z[i+1]) 
         Cr = lambda i: (Z[i+1]-Z[i])/(Z[i]+Z[i+1]) 
         print "# i, z[i], Z[i], Ct[i], Cr[i]"
         for i in range(1,z.size-1,1):
                 print i, z[i], Z[i], Ct(i), Cr(i) 


# EOF: domain.py

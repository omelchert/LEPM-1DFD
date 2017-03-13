import sys
import numpy as np

class PiezoTransducer(object):

    def __init__(self,Glob,(zMin,zMax),h=1.):
        self.dz = Glob.dz
        self.zIdMin = max(1,Glob._z2i(zMin))
        self.zIdMax = Glob._z2i(zMax)
        self.E = np.zeros(self.zIdMax-self.zIdMin)
        self.h = h
        self.t = []
        self.p = []
        self.pS = []

    def measure(self,n,dt,u,tau):
        C = dt/self.dz
        E0 = self.E 
        h = self.h
        zL, zH = self.zIdMin, self.zIdMax

        # evolve electric field within transducer
        self.E[:] = E0[:] - h*C*(u[zL-1:zH-1]-u[zL:zH])

        # determine potential difference across transducer 
        dU = -np.trapz(self.E,dx=self.dz)

        self.t.append(n*dt)
        self.p.append(dU)
        self.pS.append(tau[self.zIdMax])

    def dumpField(self,fName=None):
        fStream = open(fName,'w') if fName else sys.stdout 
        fStream.write("# (z) (E) \n")
        for i in range(len(self.E)):
            fStream.write("%lf %lf\n"%(self.dz*(self.zIdMin+i),self.E[i]))

    def dumpSignal(self,fName=None):
          fStream = open(fName,'w') if fName else sys.stdout 
          n1 = 1./max(self.p)
          n2 = 1./max(self.pS)
          fStream.write("# (t) (U) (pS) \n")
          for i in range(len(self.p)):
              fStream.write("%lf %lf %lf\n"%(self.t[i],n1*self.p[i],n2*self.pS[i]))



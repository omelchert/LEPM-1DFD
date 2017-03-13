import sys
import numpy as np


class StressMonitor(object):

    def __init__(self,Glob):
            self.z = Glob.z
            self.dz = Glob.dz
            self.I = range(0,self.z.size,5)
            self.stress = dict()

    def measure(self,n,dt,u,tau):
         if n==0:
            print len(self.I),
            for zi in self.z[self.I]:
                print zi,
            print
         elif n%50==0:
            print n*dt,
            for i in self.I: 
                print tau[i],
            print



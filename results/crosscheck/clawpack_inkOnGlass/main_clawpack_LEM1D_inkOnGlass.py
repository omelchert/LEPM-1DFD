import sys
import numpy as np
from clawpack import pyclaw
from clawpack import riemann

class Globals(object):
        pass
        
def convolveIniStressGauss(x,p0,d):

    def pulseKernelGauss(t,td):
        return np.exp(-(t-t[t.size/2])**2/(td/2)**2)

    def convolve(p,kernel):
        return np.convolve(kernel,p,mode='same')/kernel.sum()

    return convolve(p0, pulseKernelGauss(x,d))

class Detector(object):
    def __init__(self,posMask,width):
        self.posMask = posMask
        self.width = width
        self.t = []
        self.p = []

    def measure(self,tCurr,p):
        pAv = np.trapz(p[self.posMask])
        self.t.append(tCurr)
        self.p.append(pAv)


def lowPassFilter(t,s0,tau):
    s = np.copy(s0)
    dt = t[1]-t[0]
    a = dt/(tau + dt)

    for i in range(1,s.size):
        s[i] = a*s[i] + (1.-a)*s[i-1]  

    return s 


def iniSourceVolume():
        
        xMin = -0.5
        xMax = 10.0
        Nx = 5000
        Gamma = 1.
        f0 = 1.

        Glob = Globals()

        Glob.domain = pyclaw.Domain([xMin], [xMax], [Nx])
        Glob.solver = pyclaw.ClawSolver1D(riemann.acoustics_variable_1D)
        Glob.state = pyclaw.State(Glob.domain,2,2)
        Glob.solution = pyclaw.Solution(Glob.state, Glob.domain)

        Glob.x = Glob.domain.grid.p_centers[0]
        Glob.dx = Glob.domain.grid.delta[0]
        Glob.inRange = lambda (a,b): np.logical_and(Glob.x<=b,Glob.x>=a)

        Glob.solver.bc_lower[0] = pyclaw.BC.extrap
        Glob.solver.bc_upper[0] = pyclaw.BC.extrap
        Glob.solver.aux_bc_lower[0] = pyclaw.BC.extrap
        Glob.solver.aux_bc_upper[0] = pyclaw.BC.extrap

        layers = {
            0: ((-0.50, 10.00), (0.343, 0.01, 0.000)), # surrounding "air" 
            1: ((0.000, 5.500), (2.77, 1.7, 0.000)), # PMMA layer
            2: ((4.980, 5.020), (2.50, 1.00, 0.000)), # Glue layer
            3: ((4.995, 5.005), (2.25, 1.78, 0.000)), # PVDF
            4: ((5.500, 5.550), (1.80, 1.00, 100.0)), # Ink
            5: ((5.550, 9.550), (5.60, 2.63, 0.000))  # Glass
        }


        Glob.mua = np.zeros(Glob.x.size) 
        for no, (zR, (c, rho, mu)) in sorted(layers.iteritems()):
            Glob.solution.state.aux[0, Glob.inRange(zR)] = rho
            Glob.solution.state.aux[1, Glob.inRange(zR)] = c
            Glob.mua[Glob.inRange(zR)] = mu

        Glob.solver.dt_initial=Glob.dx*0.3/max(Glob.solution.state.aux[1,:])
        
        Glob.state.q[0,:] = Gamma*f0*Glob.mua*np.exp(-np.cumsum(Glob.mua*Glob.dx))
        #p0 = Gamma*f0*Glob.mua*np.exp(-np.cumsum(Glob.mua*Glob.dx))
        #Glob.state.q[0,:] = convolveIniStressGauss(Glob.x,p0,0.03)
        Glob.state.q[1,:] = 0.

        xDMin, xDMax = 4.995, 5.005
        Det = Detector(Glob.inRange((xDMin,xDMax)) ,xDMax-xDMin)

        return Glob, Det



def main():
        
        Glob, Det = iniSourceVolume()

        Nt = 7000
        for i in range(Nt):
            Glob.solver.evolve_to_time(Glob.solution)
            Det.measure(i*Glob.solver.dt, Glob.solution.state.q[0])
        

        tau = 0.0495148463455
        pLP = lowPassFilter(Det.t,Det.p,tau)
        n1 = 1./max(Det.p)
        n2 = 1./max(pLP)
        for i in range(len(Det.t)):
            print Det.t[i], n1*Det.p[i], n2*pLP[i]

        print "# dt    =", Glob.solver.dt
        print "# tau   =", tau
        print "# omega =", 1./tau 


main()

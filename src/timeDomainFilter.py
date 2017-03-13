import numpy as np

class Filter(object):
    """Data structure for filter 

    """
    def __init__(self,t,s0):
        """initialize instance of filter class

        Args:
            t (array): time samples
            s0 (array): input signal recorded at time instants
        """
        self.t = np.asarray(t)
        self.dt = self.t[1]-self.t[0]
        self.s0 = np.asarray(s0)

    def lowPass(self,a):
        """low pass filter

        Implements simple low pass filter to mimic effect of experimental 
        setup on recorded signal 

        Args: 
            a (float): smoothing parameter characterizing low pass filter

        Returns:
            s (array): output signal 
            tau (array): characteristic time-constant of low-pass filter
            omega (array): characteristic cut-off frequency of low-pass filter
        """
        s = np.zeros(self.s0.size)
        tau = self.dt*(1.-a)/a 
        omega = 1./tau

        s[0] = self.s0[0]
        for i in range(1,s.size):
            s[i] = a*self.s0[i] + (1.-a)*s[i-1]  
        return s, tau, omega

# EOF: timeDomainFilter.py

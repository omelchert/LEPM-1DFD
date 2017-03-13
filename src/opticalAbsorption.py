import numpy as np

def absorbLaserBeam(Glob,Gamma=1.0,I0=1.0,d=0.05):
    """absorb laser beam

    Implements absorption of laser beam within 1D computational domain

    Args:
        Glob (data structure): data structure holding domain properties
        Gamma (float, default=1): Grueneisen parameter that determines
            conversion of absorbed energy to acoustic stress
        I0 (float, default=1): initial laser fluence
        d (float, default=0.05): gaussian smoothing width

    Returns:
        p0 (numpy array, ndim=1): initial acoustic stress profile

    Notes:
        If there are more than 1 absorbing layer, conversion of absorbed
        energy to acoustic stress is assumed to occur homogeneously with 
        maximal efficiency (Grueneisenparameter Gamma=1).

        Optical absorption following Eq. (2) of Ref. [1]

        Implements gaussian smoothing, to smooth out discontinuities in 
        intial stress profile (beneficial in using the finite-difference 
        scheme, not needed by high-resolution finite-volume method)

    Refs:
        [1] Pulsed optoacoustic characterization of layered media
            Paltauf, G and Schmidt-Kloiber, H
            J. Appl. Phys., 88 (2000) 1624

    """
    def convolveIniStressGauss(Glob,p0,td):

        def pulseKernelGauss(t,td):
            return np.exp(-(t-t[t.size/2])**2/(td/2)**2)

        def convolve(p,kernel):
            return np.convolve(kernel,p,mode='same')/kernel.sum()

        return convolve(p0, pulseKernelGauss(Glob.z,td))

    p0 = Gamma*I0*Glob.mua*np.exp(-np.cumsum(Glob.mua*Glob.dz))
    return convolveIniStressGauss(Glob,p0,d)

def deltaPulse(Glob,zRange,Gamma=1.0,f0=1.0):
    """initial acoustic stress profile

    Implements initial acuostic stress profile with 1/e width specified by
    the width of the absorbing layer

    Args:
        Glob (data structure): data structure holding domain properties
        zRange (tuple or array): sequence of z points describing beginning and
            end of absorbing layer (example: zRange = (zBegin,zEnd))
        Gamma (float, default=1): Grueneisen parameter that determines
            conversion of absorbed energy to acoustic stress
        f0 (float, default=1): initial laser fluence

    Returns:
        p0 (numpy array, ndim=1): initial acoustic stress profile

    Notes:
        Shockwave initial conditions in the acoustic propagation algorithm 
        might cause numerical artefacts in the observables. Remedy: if the 
        absorption coefficient is nonzero in a small range $z \in [z_p, z_p+
        \delta]$ only, one might use a simple Gaussian function with peak 
        intensity $f_0$, $1/e$ extension of $\delta$, and centered at $z=z_p + 
        \delta/2$, instead. Albeit this does not properly model the exponential 
        attenuation of laser fluence, it allows to study the principal 
        distortion of pressure profiles upon propagation.
    """
    zMin, zMax = min(zRange), max(zRange) 
    z0, d = (zMax + zMin)/2, (zMin - zMax)/2
    return Gamma*f0*np.exp(-(Glob.z-z0)**2/d/d)

def absorbBeam(Glob,Gamma=1.,f0=1.):
    """absorb laser beam

    Implements absorption of laser beam within 1D computational domain

    Args:
        Glob (data structure): data structure holding domain properties
        Gamma (float, default=1): Grueneisen parameter that determines
            conversion of absorbed energy to acoustic stress
        f0 (float, default=1): initial laser fluence

    Returns:
        p0 (numpy array, ndim=1): initial acoustic stress profile
        fRemain (float): remaining laser intensity after absorbtion by the 1D
            computational domain

    Notes:
        If there are more than 1 absorbing layer, conversion of absorbed
        energy to acoustic stress is assumed to occur homogeneously with 
        maximal efficiency (Grueneisenparameter Gamma=1).

        Optical absorption following Eq. (2) of Ref. [1]

    Refs:
        [1] Pulsed optoacoustic characterization of layered media
            Paltauf, G and Schmidt-Kloiber, H
            J. Appl. Phys., 88 (2000) 1624

    """
    fz = f0*np.exp(-np.cumsum(Glob.mua*Glob.dz))
    return Gamma*Glob.mua*fz, fz[-1] 

# EOF: opticalAbsorption.py

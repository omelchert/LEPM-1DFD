1. INTRODUCTION

LEPM_1DFD implements a one-dimensional finite-difference (1DFD) code for 
piecewise homogeneous, linear elastic and piezoelectric materials (LEPM)

We designed it to study the response of a piezoelectric polyvinylidenflourid
(PVDF) transducer to optoacoustic (OA) pressure waves in the acoustic nearfield
prior to thermal relaxation of the OA source volume. The assumption of
nearfield conditions, i.e.\ the absence of acoustic diffraction, allows to
treat the problem using a one-dimensional numerical approach.  Therein, the
computational domain is modeled as an inhomogeneous elastic medium,
characterized by its local wave velocities and densities, allowing to explore
the effect of stepwise impedance changes on the stress wave propagation.  The
transducer is modeled as a thin piezoelectric ``sensing'' layer and the
electromechanical coupling is accomplished by means of the respective linear
constituting equations.  Considering a low-pass characteristic of the full
experimental setup, we obtain the resulting transducer signal.  Complementing
transducer signals measured in a controlled laboratory experiment with
numerical simulations that result from a model of the experimental setup, we
find that, bearing in mind the apparent limitations of the one-dimensional
approach, the simulated transducer signals can be used very well to predict and
interpret the experimental findings.


2. DEPENDENCIES

LEPM_1DFD requires the functionality of NumPy, a fundamental package for
scientific computing (see www.numpy.org).


3. LICENSE

BSD 3-Clause License


4. ACKNOWLEDGEMENTS

O. Melchert acknowledges support from the VolkswagenStiftung within the
Nieders\"achsisches Vorab program in the framework of the project Hybrid
Numerical Optics. 


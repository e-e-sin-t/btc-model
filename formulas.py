from datetime import *
from math import *

# Parameters

base_d = date(2010, 10, 7)
base_p = 0.0575

peak_d = date(2021, 11, 10)
peak_supercycle_p = 20000
peak_cycle_p = 68000

n_cycles = 6
n_periods = n_cycles-0.5

# Formulas

def model_p(t):
    return e_e_p(sin_p(asin_p(supercycle_ln_ln_p(t)) + e_e_dp(cycle_ln_ln_dp(t))))

def supercycle_ln_ln_p(t):
    b = ln_ln_p(base_p)
    a = ln_ln_p(peak_supercycle_p) - b
    return a * tri_ln_t(t) + b

def cycle_ln_ln_dp(t):
    dp_sc = ln_ln_dp(0)
    dp_c = ln_ln_dp(1 - asin_ln_ln_p(peak_supercycle_p))
    b = (dp_sc + dp_c)/2
    a = dp_c - b
    n = n_periods
    return a * sin(2*pi*n * (asin_ln_t(t) - 1/(4*n))) + b

def resistance_asin_ln_ln_p(t):
    return asin_p(supercycle_ln_ln_p(t)) + asin_ln_ln_p(peak_cycle_p) - asin_ln_ln_p(peak_supercycle_p)

# Sub-formulas

def time_d(d):    return ((d - base_d).days + 1)/365.0
def date_t(t):    return base_d + timedelta(floor(365*t - 1))
def ln_t(t):      return log(t)+6 if t <= peak_t() else 2*peak_ln_t() - (log(2*peak_t() - t) + 6)
def e_t(t):       return exp(t-6)

def peak_t():     return time_d(peak_d)
def peak_ln_t():  return ln_t(peak_t())

def asin_ln_t(t): return 2/pi * asin(ln_t(t)/peak_ln_t()) if t <= peak_t() else 2 - 2/pi * asin(2 - ln_t(t)/peak_ln_t())
def sin_ln_t(t):  return peak_ln_t() * sin(pi/2 * t)
def tri_ln_t(t):  return (2/pi * asin(sin(pi/peak_ln_t() * ln_t(t) - pi/2)) + 1)/2

def ln_p(p):      return log(p)+3
def ln_ln_p(p):   return ln_p(ln_p(p))
def e_p(p):       return exp(p-3)
def e_e_p(p):     return e_p(e_p(p))

def asin_p(p):       return 2/pi * asin(p/ln_ln_p(peak_cycle_p))
def asin_ln_ln_p(p): return asin_p(ln_ln_p(p))
def sin_p(p):        return ln_ln_p(peak_cycle_p) * sin(pi/2 * p)

def ln_dp(dp):    return ln_p(dp + 0.1)
def ln_ln_dp(dp): return ln_p(ln_dp(dp))
def e_e_dp(dp):   return e_e_p(dp) - 0.1

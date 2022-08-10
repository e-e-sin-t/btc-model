from datetime import *
from math import *

class model:
    # Parameters

    def __init__(m, name):
        m.name = name

        m.base_d = date(2010, 10, 7)
        m.base_p = 0.0575

        m.peak_d = date(2021, 11, 10)
        m.peak_t = m.time_d(m.peak_d)
        m.peak_ln_t = log(m.peak_t)+6

        m.peak_super_p = 20000
        m.peak_cycle_p = 68000

        m.n_cycles = 6
        m.n_periods = m.n_cycles - 0.5

    # Formulas

    def p(m,t):
        return m.exp_exp_p(m.sin_p(m.asin_p(m.super_ln_ln_p_s(t)) + m.exp_exp_dp(m.cycle_ln_ln_dp(t))))

    def super_ln_ln_p_s(m,t):
        b = m.ln_ln_p(m.base_p)
        a = m.ln_ln_p(m.peak_super_p) - b
        return a * m.tri_ln_t(t) + b

    def super_asin_ln_ln_p_r(m,t):
        return m.asin_p(m.super_ln_ln_p_s(t)) + m.asin_ln_ln_p(m.peak_cycle_p) - m.asin_ln_ln_p(m.peak_super_p)

    def cycle_ln_ln_dp(m,t):
        dp_sc = m.ln_ln_dp(0)
        dp_c = m.ln_ln_dp(1 - m.asin_ln_ln_p(m.peak_super_p))
        b = (dp_sc + dp_c)/2
        a = dp_c - b
        n = m.n_periods
        return a * sin(2*pi*n * (m.asin_ln_t(t) - 1/(4*n))) + b

    # Sub-formulas

    def ln_p(m,p):         return log(p)+3
    def ln_ln_p(m,p):      return m.ln_p(m.ln_p(p))
    def exp_p(m,p):        return exp(p-3)
    def exp_exp_p(m,p):    return m.exp_p(m.exp_p(p))

    def asin_p(m,p):       return 2/pi * asin(p/m.ln_ln_p(m.peak_cycle_p))
    def asin_ln_ln_p(m,p): return m.asin_p(m.ln_ln_p(p))
    def sin_p(m,p):        return m.ln_ln_p(m.peak_cycle_p) * sin(pi/2 * p)

    def ln_dp(m,dp):       return m.ln_p(dp + 0.1)
    def ln_ln_dp(m,dp):    return m.ln_p(m.ln_dp(dp))
    def exp_exp_dp(m,dp):  return m.exp_exp_p(dp) - 0.1

    def time_d(m,d):       return ((d - m.base_d).days + 1)/365.0
    def date_t(m,t):       return m.base_d + timedelta(floor(365*t - 1))
    def ln_t(m,t):         return log(t)+6
    def exp_t(m,t):        return exp(t-6)

    def sin_ln_t(m,t):     return m.peak_ln_t * sin(pi/2 * t)
    def tri_ln_t(m,t):     return (2/pi * asin(sin(pi*m.ln_t(t)/m.peak_ln_t - pi/2)) + 1)/2

    def asin_ln_t(m,t):
        a = m.ln_t(t)/m.peak_ln_t
        n, r = floor(a), a % 1
        return n + 2/pi*asin(r) if n % 2 == 0 else n+1 - 2/pi*asin(1-r)

# Models

class naive_model(model):
    def __init__(m): super().__init__('naive')

class mirror_model(model):
    def __init__(m): super().__init__('mirror')

    def ln_t(m,t):
        a = t/m.peak_t
        n, r = floor(a), a % 1
        return m.peak_ln_t*n + (log(m.peak_t*r)+6 if r > 0 else 0) if n % 2 == 0 else m.peak_ln_t*(n+1) - (log(m.peak_t*(1-r)) + 6)

class converge_model(model):
    def __init__(m): super().__init__('converge')

models = (naive_model(), mirror_model(), converge_model())

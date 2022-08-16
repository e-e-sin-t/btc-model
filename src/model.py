from datetime import *
from math import *

class model:
    # parameters
    def __init__(m, name='basic'):
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

    # price in linear (p,t) coordinates
    def p(m,t):
        return m.exp_exp_p(m.sin_p(m.asin_p(m.p_s(m.ln_t(t))) + m.dp_c(m.asin_ln_t(t))))

    # supercycle support triangle wave in (ln(t), ln(ln(p))) coordinates
    def p_s(m,t,p=None):
        b = m.ln_ln_p(m.base_p)
        a = m.ln_ln_p(p or m.peak_super_p) - b
        return a*(2/pi*asin(sin(pi*t/m.peak_ln_t - pi/2)) + 1)/2 + b

    # supercycle resistance wave in (ln(t), ln(ln(p))) coordinates
    def p_r(m,t):
        return m.asin_p(m.p_s(t)) + m.asin_ln_ln_p(m.peak_cycle_p) - m.asin_ln_ln_p(m.peak_super_p)

    # cycle sine wave delta from supercycle support in (asin(ln(t)), asin(ln(ln(p)))) coordinates
    def dp_c(m,t):
        dp_sc = m.ln_ln_dp(0)
        dp_c = m.ln_ln_dp(1 - m.asin_ln_ln_p(m.peak_super_p))
        b = (dp_sc + dp_c)/2
        a = dp_c - b
        n = m.n_periods
        return m.exp_exp_dp(a*sin(2*pi*n*(t - 1/(4*n))) + b)

    # sub-formulas

    def ln_p(m,p):         return log(p)+3
    def ln_ln_p(m,p):      return m.ln_p(m.ln_p(p))
    def exp_p(m,p):        return exp(p-3)
    def exp_exp_p(m,p):    return m.exp_p(m.exp_p(p))

    def asin_p(m,p):       return 2/pi * asin(p/m.ln_ln_p(m.peak_cycle_p))
    def asin_ln_ln_p(m,p): return m.asin_p(m.ln_ln_p(p))
    def sin_p(m,p):        return m.ln_ln_p(m.peak_cycle_p) * sin(pi/2*p)

    def ln_dp(m,dp):       return m.ln_p(dp + 0.1)
    def ln_ln_dp(m,dp):    return m.ln_p(m.ln_dp(dp))
    def exp_exp_dp(m,dp):  return m.exp_exp_p(dp) - 0.1

    def time_d(m,d):       return ((d - m.base_d).days + 1)/365.0
    def date_t(m,t):       return m.base_d + timedelta(floor(365*t-1))
    def ln_t(m,t):         return log(t)+6
    def e_t(m,t):          return exp(t-6)
    def sin_t(m,t):        return m.peak_ln_t * sin(pi/2*t)
    def asin_ln_t(m,t):    return m.asin_t(m.ln_t(t))

    def asin_t(m,t):
        a = t/m.peak_ln_t
        n, r = floor(a), a % 1
        if n % 2 == 0:
            return n + 2/pi*asin(r)
        else:
            return n+1 - 2/pi*asin(1-r)

class mirror_model(model):
    def __init__(m): super().__init__('mirror')

    # reverse logarithmic time after peak
    def ln_t(m,t):
        a = t/m.peak_t
        n, r = floor(a), a % 1
        if n % 2 == 0:
            return m.peak_ln_t*n + (log(m.peak_t*r)+6 if r > 0 else 0)
        else:
            return m.peak_ln_t*(n+1) - (log(m.peak_t*(1-r)) + 6)

models = (model(), mirror_model())

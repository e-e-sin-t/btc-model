#!/usr/bin/python3

import csv
from datetime import *
from model import *

base_p_ixic_s = 2200
base_p_ixic_r = 2700
peak_p_ixic_s = 9750
peak_p_ixic_r = 16000

# CSV files

def read_price_csv(s):
    f = csv.reader(open("data/"+s+"-price.csv"))
    next(f)
    return {datetime.strptime(l[0], "%Y-%m-%d").date(): float(l[1]) for l in f}

p_btc, p_ixic = read_price_csv('btc'), read_price_csv('ixic')

def write_csv(s,v):
    f = csv.writer(open(s, "w"))
    f.writerow(v[0].keys())
    for r in v:
        l = []
        for k in v[0].keys():
            if r.get(k) is None:
                l.append("")
            elif isinstance(r[k], float):
                l.append("%.4f" % r[k])
            else:
                l.append(str(r[k]))
        f.writerow(l)

# EMA

def ema(v, i, k_ema, k_p, k_t='asin(ln(t))', w=0.005):
    dt = v[i][k_t] - v[i-1][k_t]
    if i == 0 or dt >= w:
        return v[i][k_p]
    else:
        return v[i-1][k_ema]*(w-dt)/w + v[i][k_p]*dt/w

# APYs

apys = (0.10, 0.30, 0.50, 0.70, 0.85)
p_apy = {apy: None for apy in apys}
p_apy[0.85] = 20000

def apy_p(m,p):
    t0 = m.time_d(m.peak_d - timedelta(1))
    p0 = m.exp_exp_p(m.p_s(m.ln_t(t0),p))
    return pow(p/p0, 365)-1

m = model()
for p in range(1, m.peak_cycle_p):
    apy = apy_p(m,p)
    for y in apys:
        if p_apy[y] is None and apy > y:
            p_apy[y] = p

# Model data

def model_data(m):
    end_date = m.base_d + timedelta(4*(m.peak_d - m.base_d).days)
    dates = (m.base_d + timedelta(n) for n in range((end_date - m.base_d).days))

    v = []
    for d in dates:
        r = {'d': d}
        v.append(r)

        # time (t)
        r['t'] = m.time_d(r['d'])
        r['ln(t)'] = m.ln_t(r['t'])
        r['asin(ln(t))'] = m.asin_t(r['ln(t)'])

        # price history (p)
        if d in p_btc:
            r['p'] = p_btc[d]
            r['ln(p)'] = m.ln_p(r['p'])
            r['ln(ln(p))'] = m.ln_p(r['ln(p)'])
            r['asin(ln(ln(p)))'] = m.asin_p(r['ln(ln(p))'])

        # supercycle support (p_s)
        r['ln(ln(p_s))'] = m.p_s(r['ln(t)'])
        r['asin(ln(ln(p_s)))'] = m.asin_p(r['ln(ln(p_s))'])
        r['ln(p_s)'] = m.exp_p(r['ln(ln(p_s))'])
        r['p_s'] = m.exp_p(r['ln(p_s)'])

        # supercycle resistance (p_r)
        r['asin(ln(ln(p_r)))'] = m.p_r(r['ln(t)'])
        r['ln(ln(p_r))'] = m.sin_p(r['asin(ln(ln(p_r)))'])
        r['ln(p_r)'] = m.exp_p(r['ln(ln(p_r))'])
        r['p_r'] = m.exp_p(r['ln(p_r)'])

        # price delta from supercycle support (dp)
        if d in p_btc:
            r['dp'] = r['asin(ln(ln(p)))'] - r['asin(ln(ln(p_s)))']
            r['ln(dp)'] = m.ln_dp(r['dp'])
            r['ln(ln(dp))'] = m.ln_p(r['ln(dp)'])

        # model (m)
        r['p_m'] = m.p(r['t'])
        r['ln(p_m)'] = m.ln_p(r['p_m'])
        r['ln(ln(p_m))'] = m.ln_p(r['ln(p_m)'])
        r['asin(ln(ln(p_m)))'] = m.asin_p(r['ln(ln(p_m))'])
        if d in p_btc:
            r['dp_m'] = r['asin(ln(ln(p_m)))'] - r['asin(ln(ln(p_s)))']
            r['ln(dp_m)'] = m.ln_dp(r['dp_m'])
            r['ln(ln(dp_m))'] = m.ln_p(r['ln(dp_m)'])

        # apy
        for apy in apys:
            k = 'p_apy_'+str(floor(100*apy))+'%'
            if r['t'] < m.peak_t:
                r[k] = m.exp_exp_p(m.p_s(r['ln(t)'], p=p_apy[apy]))
            else:
                r[k] = p_apy[apy] * pow(1+apy, r['t']-m.peak_t)

        # price delta percentage between supercycle support and resistance (dp%)
        if d in p_btc:
            percent_dp = lambda dp: (dp - m.ln_ln_dp(0)) / (m.ln_ln_dp(1 - m.asin_ln_ln_p(m.peak_super_p)) - m.ln_ln_dp(0))
            r['dp%'] = percent_dp(r['ln(ln(dp))'])
            r['ema(dp%)'] = ema(v, len(v)-1, 'ema(dp%)', 'dp%')
            r['dp_m%'] = percent_dp(r['ln(ln(dp_m))'])

        # ixic price (p_ixic)
        if d in p_ixic:
            r['p_ixic'] = p_ixic[d]
            r['ln(p_ixic)'] = log(r['p_ixic'])

        # ixic support (p_ixic_s)
        r['p_ixic_s'] = exp((log(peak_p_ixic_s) - log(base_p_ixic_s))/m.peak_t * r['t'] + log(base_p_ixic_s))
        r['ln(p_ixic_s)'] = log(r['p_ixic_s'])

        # ixic resistance (p_ixic_r)
        r['p_ixic_r'] = exp((log(peak_p_ixic_r) - log(base_p_ixic_r))/m.peak_t * r['t'] + log(base_p_ixic_r))
        r['ln(p_ixic_r)'] = log(r['p_ixic_r'])

        # ixic delta (dp_ixic)
        if d in p_btc:
            r['dp_ixic'] = r['ln(p_ixic)'] - r['ln(p_ixic_s)']
            r['dp_ixic%'] = r['dp_ixic'] / (r['ln(p_ixic_r)'] - r['ln(p_ixic_s)'])
            r['ema(dp_ixic%)'] = ema(v, len(v)-1, 'ema(dp_ixic%)', 'dp_ixic%')
            r['dp%-dp_ixic%'] = r['dp%']-r['dp_ixic%']
            r['ema(dp%-dp_ixic%)'] = ema(v, len(v)-1, 'ema(dp%-dp_ixic%)', 'dp%-dp_ixic%', w=0.01)

    return v

for m in models:
    write_csv("data/"+m.name+"-model.csv", model_data(m))

# Cycle stats

m = model()
v = []
for n in range(m.n_cycles):
    r = {'n': n}
    v.append(r)

    # base time (t_b)
    r['asin(ln(t_b))'] = n/(m.n_cycles-0.5)
    r['ln(t_b)'] = m.sin_t(r['asin(ln(t_b))'])
    r['t_b'] = m.e_t(r['ln(t_b)'])
    r['d_b'] = m.date_t(r['t_b'])

    # base price (p_b)
    r['p_b'] = m.p(r['t_b'])
    r['ln(p_b)'] = m.ln_p(r['p_b'])
    r['ln(ln(p_b))'] = m.ln_p(r['ln(p_b)'])
    r['asin(ln(ln(p_b)))'] = m.asin_p(r['ln(ln(p_b))'])

    # peak time (t_p)
    r['asin(ln(t_p))'] = (n+0.5)/(m.n_cycles-0.5)
    r['ln(t_p)'] = m.sin_t(r['asin(ln(t_p))'])
    r['t_p'] = m.e_t(r['ln(t_p)'])
    r['d_p'] = m.date_t(r['t_p'])

    # peak price (p_p)
    r['p_p'] = m.p(r['t_p'])
    r['ln(p_p)'] = m.ln_p(r['p_p'])
    r['ln(ln(p_p))'] = m.ln_p(r['ln(p_p)'])
    r['asin(ln(ln(p_p)))'] = m.asin_p(r['ln(ln(p_p))'])

    if len(v) > 1:
        q = v[-2]

        # end time (t_e)
        q['t_e'] = r['t_b']
        q['ln(t_e)'] = r['ln(t_b)']
        q['asin(ln(t_e))'] = r['asin(ln(t_b))']

        # end price (p_e)
        q['p_e'] = r['p_b']
        q['ln(p_e)'] = r['ln(p_b)']
        q['ln(ln(p_e))'] = r['ln(ln(p_b))']
        q['asin(ln(ln(p_e)))'] = r['asin(ln(ln(p_b)))']

write_csv("data/cycle.csv", v)

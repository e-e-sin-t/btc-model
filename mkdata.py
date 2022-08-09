#!/usr/bin/python3

import csv
from datetime import *
from formulas import *

base_p_ixic_s = 2200
base_p_ixic_r = 2700
peak_p_ixic_s = 9750
peak_p_ixic_r = 16000

end_date = base_d + timedelta(2*(peak_d - base_d).days)

def ema(v, i, k_ema, k_p, k_t='asin(ln(t))', w=0.005):
    dt = v[i][k_t] - v[i-1][k_t]
    if i == 0 or dt >= w:
        return v[i][k_p]
    else:
        return v[i-1][k_ema]*(w-dt)/w + v[i][k_p]*dt/w

p_of_d = {}
price_csv = csv.reader(open("price.csv"))
next(price_csv)
for line in price_csv:
    p_of_d[datetime.strptime(line[0], "%Y-%m-%d").date()] = {'btc': float(line[1]), 'ixic': float(line[2])}

v = []
for d in (base_d + timedelta(n) for n in range((end_date - base_d).days)):
    r = {'d': d}
    v.append(r)

    # time (t)
    r['t'] = time_d(r['d'])
    r['ln(t)'] = ln_t(r['t'])
    r['asin(ln(t))'] = asin_ln_t(r['t'])

    # price history (p)
    if d in p_of_d:
        r['p'] = p_of_d[d]['btc']
        r['ln(p)'] = ln_p(r['p'])
        r['ln(ln(p))'] = ln_p(r['ln(p)'])
        r['asin(ln(ln(p)))'] = asin_p(ln_ln_p(r['p']))

    # supercycle support (p_s)
    r['ln(ln(p_s))'] = supercycle_ln_ln_p(r['t'])
    r['asin(ln(ln(p_s)))'] = asin_p(r['ln(ln(p_s))'])
    r['ln(p_s)'] = e_p(r['ln(ln(p_s))'])
    r['p_s'] = e_p(r['ln(p_s)'])

    # cycle resistance (p_r)
    r['asin(ln(ln(p_r)))'] = resistance_asin_ln_ln_p(r['t'])
    r['ln(ln(p_r))'] = sin_p(r['asin(ln(ln(p_r)))'])
    r['ln(p_r)'] = e_p(r['ln(ln(p_r))'])
    r['p_r'] = e_p(r['ln(p_r)'])

    # price delta (dp)
    if d in p_of_d:
        r['dp'] = r['asin(ln(ln(p)))'] - r['asin(ln(ln(p_s)))']
        r['ln(dp)'] = ln_dp(r['dp'])
        r['ln(ln(dp))'] = ln_p(r['ln(dp)'])


    # model (m)
    r['p_m'] = model_p(r['t'])
    r['ln(p_m)'] = ln_p(r['p_m'])
    r['ln(ln(p_m))'] = ln_p(r['ln(p_m)'])
    r['asin(ln(ln(p_m)))'] = asin_p(r['ln(ln(p_m))'])
    if d in p_of_d:
        r['dp_m'] = r['asin(ln(ln(p_m)))'] - r['asin(ln(ln(p_s)))']
        r['ln(dp_m)'] = ln_dp(r['dp_m'])
        r['ln(ln(dp_m))'] = ln_p(r['ln(dp_m)'])

    # price delta percentage (dp%)
    if d in p_of_d:
        percent_dp = lambda dp: (dp - ln_ln_dp(0)) / (ln_ln_dp(1 - asin_ln_ln_p(peak_supercycle_p)) - ln_ln_dp(0))
        r['dp%'] = percent_dp(r['ln(ln(dp))'])
        r['ema(dp%)'] = ema(v, len(v)-1, 'ema(dp%)', 'dp%')
        r['dp_m%'] = percent_dp(r['ln(ln(dp_m))'])

    # ixic price (p_ixic)
    if d in p_of_d:
        r['p_ixic'] = p_of_d[d]['ixic']
        r['ln(p_ixic)'] = log(r['p_ixic'])

    # ixic support (p_ixic_s)
    r['p_ixic_s'] = exp((log(peak_p_ixic_s) - log(base_p_ixic_s))/peak_t() * r['t'] + log(base_p_ixic_s))
    r['ln(p_ixic_s)'] = log(r['p_ixic_s'])

    # ixic resistance (p_ixic_r)
    r['p_ixic_r'] = exp((log(peak_p_ixic_r) - log(base_p_ixic_r))/peak_t() * r['t'] + log(base_p_ixic_r))
    r['ln(p_ixic_r)'] = log(r['p_ixic_r'])

    # ixic delta (dp_ixic)
    if d in p_of_d:
        r['dp_ixic'] = r['ln(p_ixic)'] - r['ln(p_ixic_s)']
        r['dp_ixic%'] = r['dp_ixic'] / (r['ln(p_ixic_r)'] - r['ln(p_ixic_s)'])
        r['ema(dp_ixic%)'] = ema(v, len(v)-1, 'ema(dp_ixic%)', 'dp_ixic%')
        r['dp%-dp_ixic%'] = r['dp%']-r['dp_ixic%']
        r['ema(dp%-dp_ixic%)'] = ema(v, len(v)-1, 'ema(dp%-dp_ixic%)', 'dp%-dp_ixic%', w=0.01)

s = v[0].keys()
f = csv.writer(open("data.csv", "w"))
f.writerow(s)

for r in v:
    l = []
    for k in s:
        if not r.get(k):
            l.append("")
        elif isinstance(r[k], float):
            l.append("%.4f" % r[k])
        else:
            l.append(str(r[k]))
    f.writerow(l)

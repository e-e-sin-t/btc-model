#!/usr/bin/python3

import csv
from datetime import *
from formulas import *

base_ixic_p_s = 2000
peak_ixic_p_s = 9500
peak_ixic_p_r = 16200
base_ixic_p_r = exp(log(base_ixic_p_s) + log(peak_ixic_p_r) - log(peak_ixic_p_s))

end_date = base_d + timedelta(2*(peak_d - base_d).days)

def ema(v,k,n=30):
    return v[-1][k]/n + v[-2]['ema('+k+')']*(n-1)/n if len(v) > 1 else v[-1][k] if len(v) == 1 else None

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
        r['ln(ln(dp))%'] = (r['ln(ln(dp))'] - ln_ln_dp(0)) / (ln_ln_dp(1 - asin_ln_ln_p(peak_supercycle_p)) - ln_ln_dp(0))
        r['ema(ln(ln(dp))%)'] = ema(v, 'ln(ln(dp))%')

    # market price (ixic)
    if d in p_of_d:
        # ixic price (ixic_p)
        r['ixic_p'] = p_of_d[d]['ixic']
        r['ln(ixic_p)'] = log(r['ixic_p'])

        # ixic support (ixic_p_s)
        r['ixic_p_s'] = exp((log(peak_ixic_p_s) - log(base_ixic_p_s))/peak_t() * r['t'] + log(base_ixic_p_s))
        r['ln(ixic_p_s)'] = log(r['ixic_p_s'])

        # ixic resistance (ixic_p_r)
        r['ixic_p_r'] = exp((log(peak_ixic_p_r) - log(base_ixic_p_r))/peak_t() * r['t'] + log(base_ixic_p_r))
        r['ln(ixic_p_r)'] = log(r['ixic_p_r'])

        # ixic delta (ixic_dp)
        r['ixic_dp'] = r['ln(ixic_p)'] - r['ln(ixic_p_s)']

        # ixic delta percentage (ixic_dp%)
        r['ixic_dp%'] = r['ixic_dp'] / (log(base_ixic_p_r) - log(base_ixic_p_s))
        r['ema(ixic_dp%)'] = ema(v, 'ixic_dp%')

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

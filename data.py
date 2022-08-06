#!/usr/bin/python3

import csv
from datetime import *
from formulas import *

base_ixic_p_s = 2000
peak_ixic_p_s = 9500
peak_ixic_p_r = 16200
base_ixic_p_r = exp(log(base_ixic_p_s) + log(peak_ixic_p_r) - log(peak_ixic_p_s))

end_date = base_d + timedelta(2*(peak_d - base_d).days)

def write_csv(path, rows):
    cols = rows[0].keys()

    f = csv.writer(open(path, "w"))
    f.writerow(cols)

    for row in rows:
        line = []
        for col in cols:
            if col not in row:
                line.append("")
            elif isinstance(row[col], float):
                line.append("%.4f" % row[col])
            else:
                line.append(str(row[col]))
        f.writerow(line)

# Load prices

prices = {}
price_csv = csv.reader(open("price.csv"))
next(price_csv)
for line in price_csv:
    prices[datetime.strptime(line[0], "%Y-%m-%d").date()] = {'btc': float(line[1]), 'ixic': float(line[2])}

# Data points

rows = []
for d in (base_d + timedelta(n) for n in range((end_date - base_d).days)):
    r = {'d': d}
    rows.append(r)

    # time (t)
    r['t'] = time_d(r['d'])
    r['ln(t)'] = ln_t(r['t'])
    r['asin(ln(t))'] = asin_ln_t(r['t'])

    # price history (p)
    if d in prices:
        r['p'] = prices[d]['btc']
        r['ln(p)'] = ln_p(r['p'])
        r['ln(ln(p))'] = ln_ln_p(r['p'])
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
    if d in prices:
        r['dp'] = r['asin(ln(ln(p)))'] - r['asin(ln(ln(p_s)))']
        r['ln(dp)'] = ln_dp(r['dp'])
        r['ln(ln(dp))'] = ln_p(r['ln(dp)'])

    # model (m)
    r['p_m'] = model_p(r['t'])
    r['ln(p_m)'] = ln_p(r['p_m'])
    r['ln(ln(p_m))'] = ln_p(r['ln(p_m)'])
    r['asin(ln(ln(p_m)))'] = asin_p(r['ln(ln(p_m))'])
    if d in prices:
        r['dp_m'] = r['asin(ln(ln(p_m)))'] - r['asin(ln(ln(p_s)))']
        r['ln(dp_m)'] = ln_dp(r['dp_m'])
        r['ln(ln(dp_m))'] = ln_p(r['ln(dp_m)'])

    # price delta percentage (dp%)
    if d in prices:
        r['ln(ln(dp))%'] = (r['ln(ln(dp))'] - ln_ln_dp(0)) / (ln_ln_dp(1 - asin_ln_ln_p(peak_supercycle_p)) - ln_ln_dp(0))
        r['ln(ln(dp_m))%'] = (r['ln(ln(dp_m))'] - ln_ln_dp(0)) / (ln_ln_dp(1 - asin_ln_ln_p(peak_supercycle_p)) - ln_ln_dp(0))

    # market price (ixic_p)
    if d in prices:
        r['ixic_p'] = prices[d]['ixic']
        r['ln(ixic_p)'] = log(r['ixic_p'])
        r['ixic_p_s'] = exp((log(peak_ixic_p_s) - log(base_ixic_p_s))/peak_t() * r['t'] + log(base_ixic_p_s))
        r['ln(ixic_p_s)'] = log(r['ixic_p_s'])
        r['ixic_p_r'] = exp((log(peak_ixic_p_r) - log(base_ixic_p_r))/peak_t() * r['t'] + log(base_ixic_p_r))
        r['ln(ixic_p_r)'] = log(r['ixic_p_r'])
        r['ixic_dp'] = r['ln(ixic_p)'] - r['ln(ixic_p_s)']
        r['ixic_dp%'] = r['ixic_dp'] / (log(base_ixic_p_r) - log(base_ixic_p_s))
        r['ixic_diff_dp%'] = r['ln(ln(dp))%'] - r['ixic_dp%']

write_csv("data.csv", rows)

# Cycle stats

def cycle_n(n):
    r = {'n': n}

    # base time (t_b)
    r['asin(ln(t_b))'] = n/n_periods
    r['ln(t_b)'] = sin_ln_t(r['asin(ln(t_b))'])
    r['t_b'] = e_t(r['ln(t_b)'])
    r['d_b'] = date_t(r['t_b'])

    # base price (p_b)
    r['p_b'] = model_p(r['t_b'])
    r['ln(p_b)'] = ln_p(r['p_b'])
    r['ln(ln(p_b))'] = ln_p(r['ln(p_b)'])
    r['asin(ln(ln(p_b)))'] = asin_p(r['ln(ln(p_b))'])

    # peak time (t_p)
    r['asin(ln(t_p))'] = (n+0.5)/n_periods
    r['ln(t_p)'] = sin_ln_t(r['asin(ln(t_p))'])
    r['t_p'] = e_t(r['ln(t_p)'])
    r['d_p'] = date_t(r['t_p'])

    # peak price (p_p)
    r['p_p'] = model_p(r['t_p'])
    r['ln(p_p)'] = ln_p(r['p_p'])
    r['ln(ln(p_p))'] = ln_p(r['ln(p_p)'])
    r['asin(ln(ln(p_p)))'] = asin_p(r['ln(ln(p_p))'])

    return r

write_csv("cycle.csv", [cycle_n(n) for n in range(n_cycles)])

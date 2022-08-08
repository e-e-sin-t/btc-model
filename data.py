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

def write_csv(path, rows):
    cols = rows[0].keys()

    f = csv.writer(open(path, "w"))
    f.writerow(cols)

    for row in rows:
        line = []
        for col in cols:
            if not row.get(col):
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

# Write data points

v_d = []
for d in (base_d + timedelta(n) for n in range((end_date - base_d).days)):
    r = {'d': d}
    v_d.append(r)

    # time (t)
    r['t'] = time_d(r['d'])
    r['ln(t)'] = ln_t(r['t'])
    r['asin(ln(t))'] = asin_ln_t(r['t'])

    # price history (p)
    if d in prices:
        r['p'] = prices[d]['btc']
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
        r['ema(ln(ln(dp))%)'] = ema(v_d, 'ln(ln(dp))%')

    # market price (ixic)
    if d in prices:
        # ixic price (ixic_p)
        r['ixic_p'] = prices[d]['ixic']
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
        r['ema(ixic_dp%)'] = ema(v_d, 'ixic_dp%')
        r['ixic_diff_dp%'] = r['ln(ln(dp))%'] - r['ixic_dp%']
        r['ema(ixic_diff_dp%)'] = ema(v_d, 'ixic_diff_dp%', 365)

write_csv("data.csv", v_d)

# Write cycle stats

v_c = []
for n in range(n_cycles):
    r = {'n': n}
    v_c.append(r)

    # model base time (t_m_b)
    r['asin(ln(t_m_b))'] = n/n_periods
    r['ln(t_m_b)'] = sin_ln_t(r['asin(ln(t_m_b))'])
    r['t_m_b'] = e_t(r['ln(t_m_b)'])
    r['d_m_b'] = date_t(r['t_m_b'])

    # model base price (p_m_b)
    r['p_m_b'] = model_p(r['t_m_b'])
    r['ln(p_m_b)'] = ln_p(r['p_m_b'])
    r['ln(ln(p_m_b))'] = ln_p(r['ln(p_m_b)'])
    r['asin(ln(ln(p_m_b)))'] = asin_p(r['ln(ln(p_m_b))'])

    # model peak time (t_m_p)
    r['asin(ln(t_m_p))'] = (n+0.5)/n_periods
    r['ln(t_m_p)'] = sin_ln_t(r['asin(ln(t_m_p))'])
    r['t_m_p'] = e_t(r['ln(t_m_p)'])
    r['d_m_p'] = date_t(r['t_m_p'])

    # model peak price (p_m_p)
    r['p_m_p'] = model_p(r['t_m_p'])
    r['ln(p_m_p)'] = ln_p(r['p_m_p'])
    r['ln(ln(p_m_p))'] = ln_p(r['ln(p_m_p)'])
    r['asin(ln(ln(p_m_p)))'] = asin_p(r['ln(ln(p_m_p))'])

for n in range(n_cycles):
    r = v_c[n]

    v = (s for s in
        v_d if 'p' in s and
        v_c[n]['d_m_b'] <= s['d'] and
        (s['d'] < v_c[n+1]['d_m_b'] if n != (n_cycles-1) else True))
    r_p = max(v, key=lambda s: s['p'])

    # actual peak time (t_p)
    r['d_p'] = r_p['d']
    r['t_p'] = time_d(r['d_p'])
    r['ln(t_p)'] = ln_t(r['t_p'])
    r['asin(ln(t_p))'] = asin_ln_t(r['t_p'])

    # actual peak price (p_p)
    r['p_p'] = r_p['p']
    r['ln(p_p)'] = ln_p(r['p_p'])
    r['ln(ln(p_p))'] = ln_p(r['ln(p_p)'])
    r['asin(ln(ln(p_p)))'] = asin_p(r['ln(ln(p_p))'])

write_csv("cycle.csv", v_c)

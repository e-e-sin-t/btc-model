#!/usr/bin/python3

import csv
from datetime import *
from formulas import *

end_date = date(2026, 1, 1)

prices = {}
price_csv = csv.reader(open("price.csv"))
next(price_csv)
for line in price_csv:
    prices[datetime.strptime(line[0], "%Y-%m-%d").date()] = float(line[1])

rows = []
d = base_date
while d < end_date:
    r = {}

    # time (t)
    r['d'] = d
    r['t'] = year(r['d'])
    r['ln(t)'] = ln_t(r['t'])
    r['asin(ln(t))'] = asin_ln_t(r['t'])

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

    # model (m)
    r['p_m'] = model_p(r['t'])
    r['ln(p_m)'] = ln_p(r['p_m'])
    r['ln(ln(p_m))'] = ln_p(r['ln(p_m)'])
    r['asin(ln(ln(p_m)))'] = asin_p(r['ln(ln(p_m))'])
    r['dp_m'] = r['asin(ln(ln(p_m)))'] - r['asin(ln(ln(p_s)))']
    r['ln(dp_m)'] = ln_dp(r['dp_m'])
    r['ln(ln(dp_m))'] = ln_p(r['ln(dp_m)'])

    # price history (p)
    if d in prices:
        r['p'] = prices[d]
        r['ln(p)'] = ln_p(r['p'])
        r['ln(ln(p))'] = ln_ln_p(r['p'])
        r['asin(ln(ln(p)))'] = asin_p(ln_ln_p(r['p']))

        # price delta (dp)
        r['dp'] = r['asin(ln(ln(p)))'] - r['asin(ln(ln(p_s)))']
        r['ln(dp)'] = ln_dp(r['dp'])
        r['ln(ln(dp))'] = ln_p(r['ln(dp)'])

    rows.append(r)
    d += timedelta(1)

cols = rows[0].keys()

data_csv = csv.writer(open("data.csv", "w"))
data_csv.writerow(cols)

for row in rows:
    line = []
    for col in cols:
        if col not in row:
            line.append("")
        elif isinstance(row[col], float):
            line.append("%.4f" % row[col])
        else:
            line.append(str(row[col]))
    data_csv.writerow(line)

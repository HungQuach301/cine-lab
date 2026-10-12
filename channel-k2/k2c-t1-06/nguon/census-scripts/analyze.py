"""Cluster C - official Census data. Run: /opt/cine/bin/python -I analyze.py <pylib> <rawdir>"""
import sys, json, datetime
sys.path.insert(0, sys.argv[1]); RAW = sys.argv[2]
import openpyxl, xlrd
out = {}

def nrc_annual(fn):
    ws = openpyxl.load_workbook(f"{RAW}/{fn}", data_only=True, read_only=True)["Annual"]
    d = {}
    for i, r in enumerate(ws.iter_rows(values_only=True), start=1):
        if isinstance(r[0], int):
            num = lambda v: v if isinstance(v, (int, float)) else None
            d[r[0]] = dict(row=i, total=num(r[1]), u1=num(r[2]), u2_4=num(r[3]), u5p=num(r[4]))
    return d

def pct(a, b): return round(100 * a / b, 2)

for key, fn in [("completions", "comps_cust.xlsx"), ("starts", "starts_cust.xlsx"), ("permits", "permits_cust.xlsx")]:
    d = nrc_annual(fn)
    yrs = [y for y in d if d[y]["u2_4"] is not None]
    pk = max(yrs, key=lambda y: d[y]["u2_4"])
    pk5 = max([y for y in d if d[y]["u5p"] is not None], key=lambda y: d[y]["u5p"])
    lo = min(yrs, key=lambda y: d[y]["u2_4"])
    res = dict(first_year_2_4=min(yrs), last_year=max(yrs),
               peak_2_4=(pk, d[pk]["u2_4"], f"Annual!D{d[pk]['row']}"),
               min_2_4=(lo, d[lo]["u2_4"], f"Annual!D{d[lo]['row']}"),
               peak_5p=(pk5, d[pk5]["u5p"], f"Annual!E{d[pk5]['row']}"),
               years={})
    for y in sorted(d):
        r = d[y]
        if r["u2_4"] is None: continue
        res["years"][y] = dict(row=r["row"], total=r["total"], u1=r["u1"], u2_4=r["u2_4"], u5p=r["u5p"],
                               share_2_4_pct=pct(r["u2_4"], r["total"]), share_5p_pct=pct(r["u5p"], r["total"]))
    # early-1970s average share: sum(2-4, 1970..1974)/sum(total, 1970..1974)
    e = [y for y in range(1970, 1975) if y in res["years"]]
    if e:
        res["share_2_4_1970_74_pooled_pct"] = pct(sum(d[y]["u2_4"] for y in e), sum(d[y]["total"] for y in e))
        res["share_5p_1970_74_pooled_pct"] = pct(sum(d[y]["u5p"] for y in e), sum(d[y]["total"] for y in e))
        res["avg_2_4_1970_74_thousands"] = round(sum(d[y]["u2_4"] for y in e) / len(e), 2)
    res["ratio_2025_vs_peak_2_4_pct"] = pct(d[2025]["u2_4"], d[pk]["u2_4"])
    out[key] = res

# 2026 YTD completions/starts NSA (Jan-Aug)
for key, fn in [("completions_2026ytd", "comps_cust.xlsx"), ("starts_2026ytd", "starts_cust.xlsx")]:
    ws = openpyxl.load_workbook(f"{RAW}/{fn}", data_only=True, read_only=True)["Not Seasonally Adjusted"]
    tot = {"2026": [0, 0, 0], "2025": [0, 0, 0]}
    for r in ws.iter_rows(values_only=True):
        if isinstance(r[0], datetime.datetime) and r[0].year in (2025, 2026) and r[0].month <= 8:
            t = tot[str(r[0].year)]; t[0] += r[1]; t[1] += r[3]; t[2] += r[4]
    out[key] = {k: dict(total=round(v[0], 1), u2_4=round(v[1], 1), u5p=round(v[2], 1)) for k, v in tot.items()}

# BPS annual state file (US row)
for line in open(f"{RAW}/st2025a.txt"):
    f = line.strip().split(",")
    if len(f) > 4 and f[1] == "US":
        out["bps_2025_us"] = dict(u1_bldgs=int(f[5]), u1_units=int(f[6]), u2_bldgs=int(f[8]), u2_units=int(f[9]),
            u34_bldgs=int(f[11]), u34_units=int(f[12]), u5p_bldgs=int(f[14]), u5p_units=int(f[15]),
            value_2_thousand_usd=int(f[10]), value_34_thousand_usd=int(f[13]))
        b = out["bps_2025_us"]; tot = b["u1_units"] + b["u2_units"] + b["u34_units"] + b["u5p_units"]
        b["total_units"] = tot; b["u2_4_units"] = b["u2_units"] + b["u34_units"]
        b["share_2_4_pct"] = pct(b["u2_4_units"], tot)

# SOC Characteristics: MF units completed by units per building (US block)
def chars_us(fn, ncols):
    sh = xlrd.open_workbook(f"{RAW}/{fn}").sheet_by_index(0)
    rows = {}
    for r in range(8, sh.nrows):
        v = sh.cell_value(r, 0)
        if v == "RSE/SE":
            rows["RSE/SE"] = [sh.cell_value(r, c) for c in range(1, ncols)]; break
        if isinstance(v, float): rows[int(v)] = dict(xls_row=r + 1, vals=[sh.cell_value(r, c) for c in range(1, ncols)])
    return sh.name, rows
name, mfu = chars_us("mfu_unitsperbldg_cust.xls", 17)
labels = ["total", "2u(pre1999=2-4)", "3-4u", "5-9u", "10-19u", "20-29u", "30-49u", "50+u"]
comps = out["completions"]["years"]
mf = {}
for y, rec in mfu.items():
    if y == "RSE/SE": mf["RSE_2025_pct"] = dict(zip(labels, rec[:8])); continue
    v = dict(zip(labels, rec["vals"][:8])); n = lambda x: x if isinstance(x, float) else 0.0
    small24 = n(v["2u(pre1999=2-4)"]) + n(v["3-4u"]); small519 = n(v["5-9u"]) + n(v["10-19u"])
    mf[y] = dict(xls_row=rec["xls_row"], **v, two_to_four=small24, five_to_nineteen=small519,
                 share_5_19_of_MF_pct=pct(small519, v["total"]),
                 share_5_19_of_all_completions_pct=pct(small519, comps[y]["total"]) if y in comps else None)
out["chars_mfu_sheet"] = name; out["chars_mfu"] = mf
pk519 = max([y for y in mf if isinstance(y, int)], key=lambda y: mf[y]["five_to_nineteen"])
out["chars_peak_5_19"] = (pk519, mf[pk519]["five_to_nineteen"])

name, mfb = chars_us("mfb_floors_cust.xls", 9)
out["chars_mfb_floors"] = {y: (r if y == "RSE/SE" else dict(xls_row=r["xls_row"], vals=r["vals"])) for y, r in mfb.items() if y == "RSE/SE" or y >= 2013}
name, mfuf = chars_us("mfu_floors_cust.xls", 9)
out["chars_mfu_floors"] = {y: (r if y == "RSE/SE" else dict(xls_row=r["xls_row"], vals=r["vals"])) for y, r in mfuf.items() if y == "RSE/SE" or y >= 2013}

# ACS 2024 1-year, table-based summary file
def acs(fn, geo="0100000US"):
    lines = open(f"{RAW}/{fn}").read().splitlines(); hdr = lines[0].split("|")
    for l in lines[1:]:
        f = l.split("|")
        if f[0] == geo: return {h: int(x) for h, x in zip(hdr[1:], f[1:])}
a = acs("acsdt1y2024-b25024.dat"); E = lambda i: a[f"B25024_E{i:03d}"]; M = lambda i: a[f"B25024_M{i:03d}"]
tot = E(1)
b24 = dict(total=(tot, M(1)), one_det=E(2), one_att=E(3), two=(E(4), M(4)), three_four=(E(5), M(5)),
           five_nine=(E(6), M(6)), ten_19=(E(7), M(7)), twenty_49=E(8), fifty_plus=E(9), mobile=E(10), boat_rv=E(11))
b24["two_to_four"] = E(4) + E(5); b24["five_to_19"] = E(6) + E(7)
for k, idx in [("two", [4]), ("three_four", [5]), ("two_to_four", [4, 5]), ("five_nine", [6]), ("ten_19", [7]),
               ("five_to_19", [6, 7]), ("two_to_19", [4, 5, 6, 7]), ("twenty_plus", [8, 9]), ("one_unit", [2, 3])]:
    b24[f"share_{k}_pct"] = pct(sum(E(i) for i in idx), tot)
out["acs_b25024_us_2024"] = b24

c = acs("acsdt1y2024-b25127.dat"); C = lambda i: c[f"B25127_E{i:03d}"]
periods = ["2020+", "2000-2019", "1980-1999", "1960-1979", "1940-1959", "pre-1940"]
own_start = [3, 10, 17, 24, 31, 38]; rent_start = [46, 53, 60, 67, 74, 81]
by = {}
for p, o, r in zip(periods, own_start, rent_start):
    # offset +2 = "2 to 4", +3 = "5 to 19", +1 = "1 unit"; o is the period subtotal
    by[p] = dict(all=C(o) + C(r), one=C(o + 1) + C(r + 1), two_four=C(o + 2) + C(r + 2), five_19=C(o + 3) + C(r + 3),
                 two_four_renter=C(r + 2), two_four_owner=C(o + 2))
t24 = sum(v["two_four"] for v in by.values()); t519 = sum(v["five_19"] for v in by.values())
for p in by:
    by[p]["share_of_2_4_stock_pct"] = pct(by[p]["two_four"], t24)
    by[p]["share_of_5_19_stock_pct"] = pct(by[p]["five_19"], t519)
    by[p]["share_2_4_within_period_pct"] = pct(by[p]["two_four"], by[p]["all"])
out["acs_b25127_us_2024_occupied"] = dict(total_occupied=C(1), total_2_4_occ=t24, total_5_19_occ=t519,
    renter_share_of_2_4_occ_pct=pct(sum(v["two_four_renter"] for v in by.values()), t24), by_period=by,
    two_four_built_2000_or_later_pct=pct(by["2020+"]["two_four"] + by["2000-2019"]["two_four"], t24),
    two_four_built_before_1960_pct=pct(by["pre-1940"]["two_four"] + by["1940-1959"]["two_four"], t24))
# sanity: subtotal check
chk = sum(C(i) for i in own_start + rent_start)
out["acs_b25127_check_sum_periods_eq_total"] = (chk, C(1))
json.dump(out, open(sys.argv[3], "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k not in ("chars_mfu",)}, indent=1, default=str)[:20000])

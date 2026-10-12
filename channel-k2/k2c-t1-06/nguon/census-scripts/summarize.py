import json, sys
o = json.load(open(sys.argv[1]))
for k in ("completions", "starts", "permits"):
    r = o[k]; Y = r["years"]
    print(f"\n## {k}: 2-4 first yr {r['first_year_2_4']}, peak {r['peak_2_4']}, min {r['min_2_4']}, 5+ peak {r['peak_5p']}")
    print(" pooled 1970-74 share 2-4:", r.get("share_2_4_1970_74_pooled_pct"), " 5+:", r.get("share_5p_1970_74_pooled_pct"), " avg 2-4/yr:", r.get("avg_2_4_1970_74_thousands"), " 2025/peak %:", r["ratio_2025_vs_peak_2_4_pct"])
    for y in ["1970","1971","1972","1973","1974","1979","1985","1990","2000","2006","2010","2020","2021","2022","2023","2024","2025"]:
        if y in Y: v=Y[y]; print(f"  {y} row{v['row']}: tot {v['total']} 1u {v['u1']} 2-4 {v['u2_4']} 5+ {v['u5p']} | sh2-4 {v['share_2_4_pct']}% sh5+ {v['share_5p_pct']}%")
for k in ("completions_2026ytd","starts_2026ytd","bps_2025_us","chars_peak_5_19","acs_b25024_us_2024","acs_b25127_us_2024_occupied","acs_b25127_check_sum_periods_eq_total"):
    print("\n##", k, json.dumps(o[k]))
m = o["chars_mfu"]
print("\n## chars_mfu (thousands): yr total 2u 3-4 5-9 10-19 | 2-4 5-19 sh5-19ofMF sh5-19ofAll")
for y in ["1972","1973","1979","1985","1990","1998","1999","2000","2006","2010","2015","2020","2023","2024","2025"]:
    v=m[y]; print(" ",y,v["xls_row"],v["total"],v["2u(pre1999=2-4)"],v["3-4u"],v["5-9u"],v["10-19u"],"|",v["two_to_four"],v["five_to_nineteen"],v["share_5_19_of_MF_pct"],v["share_5_19_of_all_completions_pct"])
print("RSE", m["RSE_2025_pct"])
print("\n## mfb floors (bldgs, thousands: total, 1-2, 3, 4+, pct...)")
for y,v in o["chars_mfb_floors"].items(): print(" ",y,v)
print("\n## mfu floors (units)")
for y,v in o["chars_mfu_floors"].items(): print(" ",y,v)

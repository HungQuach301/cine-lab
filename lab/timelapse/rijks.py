"""Tra ảnh Rijksmuseum (Linked Art, không cần khoá): tiêu đề, năm, tác giả, quyền, ảnh IIIF. Ghi tạm ngoài git."""
import json, sys, re, requests
from pathlib import Path
OUT = Path.home() / ".cache/cine-timelapse/photo"
H = {"Accept": "application/ld+json", "User-Agent": "cine-lab-research/1.0"}

def walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: yield v
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o: yield from walk(v, key)

def info(uri):
    j = requests.get(uri, headers=H, timeout=60).json()
    names = [n.get("content") for n in j.get("identified_by", []) if n.get("type") == "Name"]
    date = next(iter(walk(j.get("produced_by", {}), "begin_of_the_begin")), "")
    makers = [c.get("_label") or c.get("id") for c in walk(j.get("produced_by", {}), "carried_out_by") for c in (c if isinstance(c, list) else [c])]
    rights = [s.get("id") for s in walk(j, "subject_to") for s in (s if isinstance(s, list) else [s]) if isinstance(s, dict)]
    rights += [c.get("id") for r in walk(j, "classified_as") for c in (r if isinstance(r, list) else [r]) if isinstance(c, dict) and "creativecommons" in str(c.get("id"))]
    vis = [v.get("id") for v in j.get("shows", [])]
    img = None
    for v in vis:
        try:
            vj = requests.get(v, headers=H, timeout=60).json()
            ap = [a.get("id") for a in walk(vj, "access_point") for a in (a if isinstance(a, list) else [a]) if isinstance(a, dict)]
            if ap: img = ap[0]; break
        except Exception: pass
    ident = [n.get("content") for n in j.get("identified_by", []) if n.get("type") == "Identifier"]
    return dict(uri=uri, id=ident[:1], title=(names or [""])[0], date=date, makers=makers[:2], rights=list(dict.fromkeys(rights))[:3], img=img)

if __name__ == "__main__":
    q = sys.argv[1]
    s = requests.get("https://data.rijksmuseum.nl/search/collection", params=dict(title=q, type="photograph"), headers=H, timeout=60).json()
    for it in s.get("orderedItems", [])[: int(sys.argv[2]) if len(sys.argv) > 2 else 12]:
        try: print(json.dumps(info(it["id"]), ensure_ascii=False))
        except Exception as e: print("ERR", it["id"], type(e).__name__)

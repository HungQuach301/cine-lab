"""V5b-1 · bước 3 gói cảnh xương sống thời gian (cần build_rasters.py + build_vectors.py trước).
Hai tầng (chủ dự án duyệt 16/10, Y1–Y7):
 TẦNG ĐẦY ĐỦ — La Línea: mỗi phần toà Catastro mọc đúng năm xây (dateOfConstruction), cao = số tầng × 3,0 m.
 TẦNG CHUẨN  — Gibraltar (không có năm xây mở): toà hiện có (OSM) đứng theo MỐC bằng chứng, KHÔNG nội suy năm:
    1704 vùng phố trong tường (bản in LoC 2016646782, 1705, vẽ thành phố bị chiếm 1704 + tường thành OSM) → GHOST; 1987 (Landsat 5 TM, đất + không phủ thực vật) → khối đặc;
    đất khai hoang 1987→2026 (Sentinel-2 15/04/2026) → 2026.
 GHOST: vùng định cư có bằng chứng nhưng không biết toà cụ thể → khối mờ (ghi "reconstructed from <nguồn, năm>"):
    Gibraltar phố trong tường từ 1704; La Línea lõi phố c.1900 (ảnh LoC 2025710366 + vị trí toà Catastro còn đứng xây ≤ 1930).
 MẶT NƯỚC THEO NĂM: đất hiện nay chỉ có từ năm có bằng chứng: phần đường băng lấn vịnh 1941–1943 (HMGoG 199/2018);
    bờ trước 1941 dựng lại (đường Line Wall + bãi vịnh, ≈); đất mới 1987→2026 = khác biệt Landsat 1987 / Sentinel-2 2026.
Ra $K2TL_CACHE/scene/<tên>/pack/: terrain.f32, ground_nat.jpg, ground_urb.jpg, years.png, buildings.json, roads.json, trees.f32, heroes.json, lines.json, meta.json"""
import argparse, json, math, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
import cv2
from build_rasters import SCENES, CACHE

# --- dữ kiện có nguồn (claims T3 + nguồn tra trong phiên; xem reports/V5B1-BAO-CAO.md §7)
POP = [[1753, 1816], [1767, 2710], [1777, 3201], [1787, 3386], [1791, 2890], [1814, 10136], [1834, 15002], [1844, 15823], [1871, 18695],
       [1878, 18014], [1881, 18381], [1891, 19100], [1901, 20355], [1911, 19120], [1921, 18061], [1931, 17405], [1951, 20845], [1961, 21636],
       [1970, 24672], [1981, 26479], [1991, 26703], [2001, 27495], [2012, 32194], [2022, 37936]]   # Census of Gibraltar 2022 Report, Table 1 (usually-resident)
OLD_TOWN = [(-610, -650), (-470, -560), (-300, -600), (-230, -760), (-260, -1100), (-330, -1500), (-400, -1800), (-600, -1800), (-640, -1300)]   # ≈ phố trong tường 1705
OLD_BAY = [(-640, -3200), (-600, -1800), (-610, -650), (-380, -300), (-300, 250), (-260, 600)]   # chỉ áp cho N ≤ 600 (eo đất); phía bắc dùng bờ Landsat 1987   # ≈ bờ vịnh trước khai hoang (Line Wall → bãi eo đất)
RUNWAY_RECL_N = (-140, 140)   # dải khai hoang cho đường băng lấn vịnh 1941–1943 (N quanh tim đường băng N≈0)
STEP = 10.0

def poly_mask(shape, ext, poly, step=STEP):
    e0, n0, e1, n1 = ext; im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([((e - e0) / step, (n1 - n) / step) for e, n in poly], fill=1); return np.array(im, bool)

def raster_polys(shape, ext, polys, vals, step=STEP, init=0, mode="min"):
    """Đốt đa giác vào lưới; mode min: giữ giá trị nhỏ nhất (năm sớm nhất)."""
    e0, n0, e1, n1 = ext; out = np.full(shape, init, np.float32)
    order = np.argsort(vals)[::-1] if mode == "min" else np.argsort(vals)
    im = Image.new("F", (shape[1], shape[0]), init); d = ImageDraw.Draw(im)
    for i in order:
        p = polys[i]
        if len(p) >= 3: d.polygon([((e - e0) / step, (n1 - n) / step) for e, n in p], fill=float(vals[i]))
    return np.array(im, np.float32)

def west_of(poly_line, E, N):
    """True nếu điểm nằm phía tây đường bờ cũ (nội suy E của đường theo N)."""
    pl = np.array(poly_line, float); o = np.argsort(pl[:, 1]); pl = pl[o]
    eL = np.interp(N, pl[:, 1], pl[:, 0], left=np.nan, right=np.nan)
    return np.where(np.isnan(eL), False, E < eL)

def area(p):
    p = np.asarray(p); return 0.5 * abs(np.dot(p[:, 0], np.roll(p[:, 1], 1)) - np.dot(p[:, 1], np.roll(p[:, 0], 1)))

def main(name):
    S = SCENES[name]; src = CACHE / "scene" / name; out = src / "pack"; out.mkdir(parents=True, exist_ok=True)
    M = json.loads((src / "meta_rasters.json").read_text()); ext = M["ext"]; e0, n0, e1, n1 = ext
    dsm = np.load(src / "r_dsm10.npy"); H_, W_ = dsm.shape
    X, Y = np.meshgrid(np.arange(e0, e1 + 1e-6, STEP), np.arange(n1, n0 - 1e-6, -STEP))
    land26 = np.load(src / "r_land26.npy"); land87 = np.load(src / "r_land87.npy"); ndvi = np.load(src / "r_ndvi.npy"); ndvi87 = np.load(src / "r_ndvi87.npy")
    # ---- làm sạch mặt nạ đất: bỏ đốm nước nhỏ trong đất, giữ đê/kè (nhánh mảnh) nhưng bỏ tàu (đốm đất nhỏ rời bờ)
    def clean(L, min_land=60, min_water=400):
        lab, n = ndimage.label(L); sz = ndimage.sum(L, lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.nonzero(sz >= min_land)[0])
        lw, nw = ndimage.label(~keep); szw = ndimage.sum(~keep, lw, range(1, nw + 1)); water = np.isin(lw, 1 + np.nonzero(szw >= min_water)[0])
        return ~water
    # nhựa đường (đường băng, sân đỗ) có NIR thấp như nước → thêm điều kiện độ cao DSM cho 2026 và dải đường băng OSM cho 1987
    V0 = json.loads((src / "v_osm.json").read_text())
    rwp = [a["p"] for a in V0["aeroway"] if a["t"].get("aeroway") in ("runway", "taxiway", "apron")]
    rwm = np.zeros(dsm.shape, bool)
    for p in rwp:
        im = Image.new("L", (W_, H_), 0); ImageDraw.Draw(im).line([((e - e0) / STEP, (n1 - n) / STEP) for e, n in p], fill=1, width=7); rwm |= np.array(im, bool)
    # tàu lớn ngoài biển có NIR như đất: bỏ mảng đất rời có DSM trung bình < 0,5 m (Copernicus làm phẳng mặt biển = 0) và < 5 ha
    lab_, nl_ = ndimage.label(land26); szl = ndimage.sum(land26, lab_, range(1, nl_ + 1)); mh = ndimage.mean(dsm, lab_, range(1, nl_ + 1))
    ships = np.isin(lab_, 1 + np.nonzero((szl < 500) & (mh < 0.5))[0])
    land26 = (land26 & ~ships) | (dsm > 1.2) | rwm; land87 = land87 | rwm
    land26c, land87c = clean(land26), clean(land87)
    sea87 = ~land87c; dsea87 = ndimage.distance_transform_edt(~sea87) * STEP
    new = land26c & ~land87c & (dsea87 <= 1.0) | (land26c & ~land87c & (dsm < 20))
    new = ndimage.binary_opening(new, iterations=2) & land26c
    labn, nn_ = ndimage.label(new); szn = ndimage.sum(new, labn, range(1, nn_ + 1)); touch = ndimage.maximum(ndimage.binary_dilation(sea87, iterations=2), labn, range(1, nn_ + 1))
    new = np.isin(labn, 1 + np.nonzero((szn >= 200) & (touch > 0))[0])   # V5b-1b: khai hoang = mảng ≥ 2 ha giáp biển 1987 (nhựa sân đỗ NIR thấp không phải 'đất mới')
    # năm có đất (bằng chứng sớm nhất): 0 = luôn là đất; 1941 = khai hoang đường băng (đủ năm 1943); 1987; 2026; 9999 = nước
    landY = np.where(land26c, 0, 9999).astype(np.float32)
    westold = west_of(OLD_BAY, X, Y)
    pre87 = land87c & land26c & westold
    landY[pre87] = 1987
    rw = pre87 & (Y > RUNWAY_RECL_N[0]) & (Y < RUNWAY_RECL_N[1]) & (X > -1400)
    landY[rw] = 1941
    landY[new] = 2026
    # V5b-1b: vùng "chưa có đất" trước 1941/1987 phải NỐI LIỀN biển (nhiễu Landsat tạo ao lẻ giữa đất liền ở năm cũ — lỗi thấy ở khung 1916)
    wet = landY != 0; wet = ndimage.binary_opening(wet, iterations=2) | (landY == 9999)
    lab_w, _ = ndimage.label(wet); sea_id = np.bincount(lab_w[landY == 9999].ravel()).argmax() if (landY == 9999).any() else 0
    orphan = (landY > 0) & (landY < 9999) & (lab_w != sea_id); landY[orphan] = 0
    print("đất theo năm: bỏ", int(orphan.sum()), "ô khai hoang không nối biển")
    # ---- toà nhà
    V = json.loads((src / "v_osm.json").read_text()); C = json.loads((src / "v_catastro.json").read_text())
    oldtown = poly_mask(dsm.shape, ext, OLD_TOWN)
    def at(a, e, n):
        c = int(np.clip((e - e0) / STEP, 0, W_ - 1)); r = int(np.clip((n1 - n) / STEP, 0, H_ - 1)); return a[r, c]
    # DTM: trong vùng có toà, mở hình thái DSM (bỏ khối nhà còn trong DSM Copernicus)
    allpolys = [b["p"] for b in V["building"]] + [p["p"] for p in C]
    bmask = raster_polys(dsm.shape, ext, allpolys, np.ones(len(allpolys)), init=0) > 0
    bzone = ndimage.binary_dilation(bmask, iterations=4)
    dtm = dsm.copy(); op = ndimage.grey_opening(dsm, size=(9, 9)); dtm[bzone] = np.minimum(dsm, op)[bzone]
    dtm = np.where(land26c, np.maximum(dtm, 1.2), np.minimum(dtm, -12.0))   # V5b-1b: đất ≥ 1,2 m (mức LOD thô hạ 0,6 m không chạm mặt nước y = 0)   # đáy biển −12 m: mặt nước y = 0 không z-fight ở xa (lỗi lượt 2)
    dtm = ndimage.gaussian_filter(dtm, 0.8)
    # vùng lõi La Línea c.1900 (ghost): toà Catastro còn đứng xây ≤ 1930 → giãn 60 m, đóng 120 m
    old = [p["p"] for p in C if 0 < p["y"] <= 1930]
    core = raster_polys(dsm.shape, ext, old, np.ones(len(old))) > 0
    core = ndimage.binary_closing(ndimage.binary_dilation(core, iterations=6), iterations=12) & land26c & (Y > 300)
    lab, nl = ndimage.label(core); sz = ndimage.sum(core, lab, range(1, nl + 1)); core = np.isin(lab, 1 + np.nonzero(sz >= 2000)[0])   # chỉ lõi liền ≥ 20 ha (bỏ đốm toà cũ rời rạc)
    B = []; stat = dict(lalinea=0, gib=0, ghost_ll=0, ghost_gib=0, gib_1987=0, gib_2026=0, gib_levels=0, gib_dsmh=0)
    for p in C:
        ring = p["p"];
        if len(ring) < 3 or area(ring) < 6: continue
        cx, cy = np.mean(ring, 0); y = p["y"] or 0
        if y == 0: continue   # 14 toà không có năm: không mọc (không đoán)
        ghost = 1900 if (y > 1900 and at(core, cx, cy)) else 0
        roof = 1 if (p["f"] <= 2 and y < 1960 and area(ring) < 250) else 0   # mái ngói dốc: nhà thấp trước 1960 (thủ tục, không có dữ liệu mái)
        B.append([int(y), ghost, round(p["f"] * 3.0 + (0.9 if roof == 0 else 0), 1), round(float(at(dtm, cx, cy)), 2), roof, 0, ring])
        stat["lalinea"] += 1; stat["ghost_ll"] += ghost > 0
    # đường sống núi Rock: E của điểm cao nhất mỗi hàng (N −5000…−450) → phân sườn tây/đông
    rows = [(n, float(X[0][np.argmax(np.where((X[0] > -1500) & (X[0] < 1500), dsm[int((n1 - n) / STEP)], -1e9))])) for n in range(-5000, -440, 50)]
    RN, RE = np.array([r[0] for r in rows], float), np.array([r[1] for r in rows], float); RE = ndimage.median_filter(RE, 5)
    ridgeE = lambda n: float(np.interp(n, RN, RE))
    catbox = np.array([np.mean(p["p"], 0) for p in C])
    from scipy.spatial import cKDTree
    kd = cKDTree(catbox)
    for b in V["building"]:
        ring = b["p"][:-1] if b["p"][0] == b["p"][-1] else b["p"]
        if len(ring) < 3 or area(ring) < 6: continue
        cx, cy = np.mean(ring, 0)
        if cy > -120 and kd.query([cx, cy])[0] < 25: continue   # phía Tây Ban Nha: Catastro thay OSM
        if cy > 450: continue                                  # bắc biên giới, ngoài phủ Catastro: bỏ (không có năm)
        lv = b["t"].get("building:levels"); hgt = b["t"].get("height")
        if hgt: h = float(str(hgt).split()[0]); stat["gib_levels"] += 1
        elif lv: h = float(lv) * 3.1; stat["gib_levels"] += 1
        else:
            ex = float(at(dsm, cx, cy) - at(op, cx, cy)); h = float(np.clip(ex * 0.85, 4, 45)) if ex > 4 else 9.0; stat["gib_dsmh"] += 1
        ly = at(landY, cx, cy)
        if ly == 2026: y = 2026; stat["gib_2026"] += 1
        elif at(ndvi87, cx, cy) < 0.25 or ly == 1987: y = 1987; stat["gib_1987"] += 1
        else: y = 2026; stat["gib_2026"] += 1
        if ly == 1941 and y < 1941: y = 1987
        ghost = 1704 if at(oldtown, cx, cy) else 0
        if not ghost and ly == 0 and cy < -450 and cx < ridgeE(cy): ghost = 1880   # sườn tây Rock trên đất sẵn có: ảnh LoC 94512284 (J. Laurent, 1860–80)
        stat["ghost_gib"] += ghost > 0; stat["ghost_1880"] = stat.get("ghost_1880", 0) + (ghost == 1880)
        roof = 1 if (ghost and h <= 16 and area(ring) < 400) else 0
        B.append([y, ghost, round(h, 1), round(float(at(dtm, cx, cy)), 2), roof, 1, ring]); stat["gib"] += 1
    # ---- đường: năm = năm sớm nhất của toà trong 60 m (La Línea), mốc vùng (Gibraltar); trục biên giới có từ ảnh c.1900
    urbY = raster_polys(dsm.shape, ext, [b[6] for b in B], [b[1] if b[1] else b[0] for b in B], init=9999)
    urbY = ndimage.grey_erosion(urbY, size=(9, 9))   # lan 40 m: nền phố quanh toà
    roads = []
    WID = dict(trunk=10, primary=9, secondary=8, tertiary=7, residential=6, living_street=5, unclassified=5, service=3.5, pedestrian=5, trunk_link=6, primary_link=6, secondary_link=5, tertiary_link=5,
               track=3.0, path=1.8, footway=2.0, steps=2.0, cycleway=2.0)   # V5b-1b: lối mòn/đường bộ (OSM) — vẽ như đất/đá, không vỉa hè
    for r in V["highway"]:
        hw = r["t"].get("highway")
        if hw not in WID or r["t"].get("tunnel") == "yes": continue
        p = np.array(r["p"]); nm = r["t"].get("name", "")
        # năm theo TỪNG ĐỈNH (đường dài qua nhiều khu không lấy năm sớm nhất cả tuyến): năm đô thị tại đỉnh, không sớm hơn năm có đất
        ys = []
        for e, n in p:
            y = float(at(urbY, e, n)); ly = float(at(landY, e, n))
            if y >= 9999: y = 2026 if ly >= 2026 else 1987
            if 0 < ly < 9999: y = max(y, ly)
            if nm.startswith("Winston Churchill") or nm.startswith("Avenida 20 de Abril"): y = min(y, 1890)   # trục qua vùng trung lập: có trong ảnh LoC c.1900 (hiện xong trước mốc)
            ys.append(int(y))
        roads.append(dict(p=r["p"], w=float(r["t"].get("width", WID[hw])) if str(r["t"].get("width", "")).replace(".", "").isdigit() else WID[hw], y=ys, c=hw))
    # ---- mặt đất: S2 thật (đô thị) + nền tự nhiên (vùng đô thị 2026 được vá bằng màu đất cát/cây bụi lân cận, Telea)
    tci = np.load(src / "r_s2tci.npy").clip(0, 255).astype(np.uint8)
    # vùng nhân tạo 2026 ngoài toà/đường: sân bay (đường băng, đường lăn, sân đỗ — có từ 1941 theo HMGoG), khu đất OSM (dân cư, công nghiệp, quân sự…)
    AER = [a for a in V["aeroway"] if a["t"].get("aeroway") in ("runway", "taxiway", "apron", "terminal", "hangar", "aerodrome")]
    aer = np.zeros(dsm.shape, bool)
    for a in AER:
        im = Image.new("L", (W_, H_), 0); dr = ImageDraw.Draw(im); pts = [((e - e0) / STEP, (n1 - n) / STEP) for e, n in a["p"]]
        if a["t"].get("aeroway") in ("apron", "terminal", "hangar", "aerodrome") and len(pts) > 2: dr.polygon(pts, fill=1)
        else: dr.line(pts, fill=1, width=6 if a["t"].get("aeroway") == "runway" else 3)
        aer |= np.array(im, bool)
    LU = [a["p"] for a in V["area"] if a["t"].get("landuse") in ("residential", "industrial", "commercial", "military", "construction", "brownfield", "garages", "retail", "railway", "landfill") or a["t"].get("leisure") in ("pitch", "stadium", "sports_centre", "marina")]
    lum = raster_polys(dsm.shape, ext, LU, np.ones(len(LU))) > 0
    rwl = np.zeros(dsm.shape, bool)
    for a in AER:
        if a["t"].get("aeroway") == "runway":
            im = Image.new("L", (W_, H_), 0); ImageDraw.Draw(im).line([((e - e0) / STEP, (n1 - n) / STEP) for e, n in a["p"]], fill=1, width=5); rwl |= np.array(im, bool)
    urbY = np.where(rwl & (urbY > 1941), 1941, urbY)                       # đường băng: 1941 (HMGoG 177/2023)
    urbY = np.where(aer & ~rwl & (urbY > 1987), np.maximum(1987, np.where(landY < 9999, landY, 1987)), urbY)   # sân đỗ/đường lăn/nhà ga: chưa có mốc riêng → 1987 (Landsat)
    lu_y = ndimage.grey_erosion(np.where((urbY < 9999) & ~aer & ~rwl, urbY, 9999), size=(31, 31))   # khu đất: năm của TOÀ gần nhất trong 150 m (V5b-1b: không lấy năm đường băng 1941 → sân bóng hiện đại không hiện năm 1941)
    urbY = np.where(lum & (urbY >= 9999), np.where(lu_y < 9999, lu_y, np.where(landY >= 1987, landY, 1987)), urbY)
    urb26 = (urbY < 9999) | ndimage.binary_dilation(bmask, iterations=2) | aer | lum
    print("aer px", int(aer.sum()), "lum px", int(lum.sum()), "urb26 px", int(urb26.sum())); Image.fromarray((np.stack([urb26, aer, land26c], -1) * 255).astype(np.uint8)).save(src / "dbg_urb26.png")
    # biển → màu đất gần nhất (để vá không kéo màu nước vào đất), rồi vá vùng nhân tạo ở 40 m
    known = land26c & ~urb26
    _, (ri, ci) = ndimage.distance_transform_edt(~known, return_indices=True)
    base_ = tci[ri, ci]; base_ = np.where(urb26[..., None] & land26c[..., None], tci, base_)
    small = cv2.resize(base_, (W_ // 4, H_ // 4), interpolation=cv2.INTER_AREA); ms = cv2.resize((urb26 & land26c).astype(np.uint8), (W_ // 4, H_ // 4), interpolation=cv2.INTER_NEAREST)
    ms = cv2.dilate(ms, np.ones((3, 3), np.uint8))
    nat = cv2.inpaint(cv2.cvtColor(small, cv2.COLOR_RGB2BGR), ms, 12, cv2.INPAINT_TELEA); nat = cv2.cvtColor(nat, cv2.COLOR_BGR2RGB)
    nat = cv2.resize(nat, (W_, H_), interpolation=cv2.INTER_CUBIC)
    nat = np.where(urb26[..., None], nat, tci)
    Image.fromarray(nat).save(out / "ground_nat.jpg", quality=93); Image.fromarray(tci).save(out / "ground_urb.jpg", quality=93)
    np.savez_compressed(src / "r_state.npz", dtm=dtm.astype(np.float32), landY=landY, urbY=urbY, urb26=urb26, land26=land26c, land87=land87c, lum=lum, aer=aer, rwl=rwl)   # V5b-1b: cho build_classes
    def enc(a):
        a = np.clip(a, 0, 9999).astype(np.uint16); return (a >> 8).astype(np.uint8), (a & 255).astype(np.uint8)
    uh, ul = enc(urbY); lh, ll = enc(landY)
    Image.fromarray(np.stack([uh, ul, lh, ll], -1), "RGBA").save(out / "years.png")
    # ---- địa hình: lưới 20 m (mesh) Float32, hàng 0 = bắc
    t20 = dtm[::2, ::2].astype(np.float32); t20.tofile(out / "terrain.f32")
    # ---- cây: NDVI cao, ngoài vùng đô thị 2026 → tự nhiên (luôn có); cây OSM trong phố → năm đô thị
    rng = np.random.default_rng(7); T = []
    # cây tự nhiên: NDVI cao NGOÀI vùng nhân tạo + ngoài bãi bằng eo đất (cỏ sân bay/sân bóng không phải cây): chỉ sườn dốc > 4° hoặc vùng OSM rừng/bụi
    WOOD = [a["p"] for a in V["area"] if a["t"].get("natural") in ("wood", "scrub", "heath") or a["t"].get("landuse") in ("forest", "orchard")]
    wood = raster_polys(dsm.shape, ext, WOOD, np.ones(len(WOOD))) > 0
    gy_, gx_ = np.gradient(dtm, STEP); slope = np.degrees(np.arctan(np.hypot(gx_, gy_)))
    veg = (ndvi > 0.45) & land26c & ~urb26 & (dtm > 1.5) & ((slope > 4) | wood)
    rr, cc = np.nonzero(veg[::2, ::2]); sel = rng.random(len(rr)) < np.clip((ndvi[::2, ::2][rr, cc] - 0.40) * 3.0, 0, 0.9)
    for r_, c_ in zip(rr[sel], cc[sel]):
        e = e0 + c_ * 20 + rng.uniform(-9, 9); n = n1 - r_ * 20 + rng.uniform(-9, 9)
        T += [e, n, float(rng.uniform(3.0, 8.0)), 0.0]
        if ndvi[::2, ::2][r_, c_] > 0.6: e2, n2 = e + rng.uniform(-8, 8), n + rng.uniform(-8, 8); T += [e2, n2, float(rng.uniform(2.5, 6.0)), 0.0]   # maquis dày: thêm cây con
    for e, n in V["tree"]:
        ly_ = float(at(landY, e, n)); ty = float(min(at(urbY, e, n), 2026))
        if 0 < ly_ < 9999: ty = max(ty, ly_ + 2)   # V5b-1b: cây trên đất khai hoang không mọc trước khi có đất (lỗi V5b-1: cây "nổi trên biển" năm cũ)
        if ly_ >= 9999: continue
        T += [e, n, float(rng.uniform(5, 9)), ty]
    np.array(T, np.float32).tofile(out / "trees.f32")
    # ---- hero: Tower of Homage (OSM 950058970 + 23 m, Ministry for Heritage), tường lâu đài (OSM barrier=city_wall), đường băng (OSM 157316482: 1798 × 45 m)
    H = dict(tower=None, castle_walls=[], runway=None, thresholds=[], citywalls=[])
    import geo as _g; _O = _g.utm(*S["origin_ll"]); _e, _n = _g.utm(-5.3481492, 36.1556310)   # V5b-1b: trạm biên giới (OSM node 5029266974, barrier=border_control)
    H["gate"] = [round(float(_e - _O[0]), 1), round(float(_n - _O[1]), 1)]
    for b in V["building"]:
        if b["id"] == "950058970": H["tower"] = dict(p=b["p"][:-1], h=23.0, base=float(min(at(dtm, e, n) for e, n in b["p"])), area_m2=round(area(b["p"][:-1]), 1))
    for w in V["wall"]:
        if w["t"].get("name", "").startswith("Moorish Castle"): H["castle_walls"].append(w["p"])
        elif w["t"].get("historic") == "citywalls" or w["t"].get("barrier") == "city_wall": H["citywalls"].append(w["p"])
    for a in V["aeroway"]:
        if a["id"] == "157316482": H["runway"] = dict(p=a["p"], w=45.0, len_osm=1798)
        if a["t"].get("runway") == "displaced_threshold": H["thresholds"].append(a["p"])
    # ---- tuyến bay thật: Winston Churchill Avenue (gộp các đoạn primary/trunk theo hướng bắc)
    seg = [r["p"] for r in V["highway"] if r["t"].get("name", "").startswith("Winston Churchill") and r["t"].get("highway") in ("primary", "trunk", "tertiary", "secondary", "residential", "unclassified") and r["t"].get("tunnel") != "yes"]   # V5b-1b: gồm đoạn mặt đường qua đường băng (OSM ghi 'residential' — trước đây bị bỏ, tuyến nội suy lệch ~25 m)
    pts = np.array([q for s in seg for q in s]); pts = pts[np.argsort(pts[:, 1])]
    lines = dict(wca=pts.tolist())
    meta = dict(name=name, ext=ext, step_terrain=20.0, terrain_shape=list(t20.shape), ground_shape=[H_, W_], pop=POP, stat=stat,
                n_buildings=len(B), n_roads=len(roads), n_trees=len(T) // 4, origin_ll=S["origin_ll"], s2=S["s2"], ls=S["ls"],
                landY_counts={str(k): int((landY == k).sum()) for k in (0, 1941, 1987, 2026)}, tower_area_m2=H["tower"]["area_m2"] if H["tower"] else None)
    (out / "buildings.json").write_text(json.dumps(B, separators=(",", ":"))); (out / "roads.json").write_text(json.dumps(roads, separators=(",", ":")))
    (out / "heroes.json").write_text(json.dumps(H)); (out / "lines.json").write_text(json.dumps(lines)); (out / "meta.json").write_text(json.dumps(meta, indent=1))
    dbg = np.zeros((H_, W_, 3), np.uint8); dbg[landY == 0] = (120, 120, 120); dbg[landY == 1941] = (255, 200, 0); dbg[landY == 1987] = (0, 160, 255); dbg[landY == 2026] = (255, 60, 60)
    dbg[core] = dbg[core] // 2 + np.array([0, 120, 0], np.uint8); dbg[oldtown] = dbg[oldtown] // 2 + np.array([120, 0, 120], np.uint8)
    Image.fromarray(dbg).save(src / "dbg_years.png"); print(json.dumps(meta, indent=1)[:1500])

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--name", default="gib"); a.add_argument("--ao", action="store_true"); a.add_argument("--far", action="store_true"); a.add_argument("--cls", action="store_true"); o = a.parse_args(); main(o.name)

def bake_ao(name, res=4.0, box=(-2400, -4800, 1400, 4400)):
    """Nướng sẵn AO tiếp đất của toà theo NĂM (kỹ thuật 'AO tĩnh theo quãng năm'): R = độ tối (0..255), G/B = năm sớm nhất toà gây tối.
    Shader chỉ áp AO ở điểm ảnh có năm ≤ uYear → không có bóng của toà chưa mọc. Ra pack/ao.png + meta ao_box/ao_res."""
    src = CACHE / "scene" / name; out = src / "pack"; B = json.loads((out / "buildings.json").read_text())
    e0, n0, e1, n1 = box; W_, H_ = int((e1 - e0) / res), int((n1 - n0) / res)
    occ = Image.new("F", (W_, H_), 9999.0); d = ImageDraw.Draw(occ)
    for b in sorted(B, key=lambda b: -(b[1] or b[0])):
        d.polygon([((e - e0) / res, (n1 - n) / res) for e, n in b[6]], fill=float(b[1] or b[0]))
    Y = np.array(occ, np.float32); m = (Y < 9999).astype(np.float32)
    ao = np.clip(ndimage.gaussian_filter(m, 2.2) * 1.6, 0, 1) * (1 - m)   # tối quanh chân toà, không tô lên mái
    yr = ndimage.grey_erosion(Y, size=(9, 9))
    hi, lo = (np.clip(yr, 0, 9999).astype(np.uint16) >> 8).astype(np.uint8), (np.clip(yr, 0, 9999).astype(np.uint16) & 255).astype(np.uint8)
    Image.fromarray(np.stack([(ao * 255).astype(np.uint8), hi, lo], -1), "RGB").save(out / "ao.png")
    M = json.loads((out / "meta.json").read_text()); M.update(ao_box=list(box), ao_res=res); (out / "meta.json").write_text(json.dumps(M, indent=1))
    print("ao", W_, H_)

if __name__ == "__main__" and "--ao" in __import__("sys").argv:
    bake_ao("gib")

def build_far(name, step=150.0, box=(-22000, -12500, 22000, 26000)):
    """Vòng địa hình XA (đường chân trời: Sierra Carbonera, bờ vịnh Algeciras): DSM Copernicus + màu Sentinel-2 150 m, vùng đô thị
    (NDVI thấp + sáng) vá bằng màu tự nhiên lân cận để thành phố hiện đại không lộ ở năm cũ (ở 8–20 km, trong sương)."""
    import geo
    S = SCENES[name]; out = CACHE / "scene" / name / "pack"; OE, ON = map(float, geo.utm(*S["origin_ll"]))
    e0, n0, e1, n1 = box; xs = np.arange(e0, e1 + 1e-6, step); ys = np.arange(n1, n0 - 1e-6, -step); X, Y = np.meshgrid(xs, ys)
    lon, lat = geo.utm_inv(X + OE, Y + ON)
    dsm = geo.Raster(CACHE / "dem/cop_n36w006.tif").sample(lon, lat, order=1).astype(np.float32)
    f = CACHE / "s2/a0415/visual.tif"; r = geo.Raster(f); w = r.window_for(OE + e0, ON + n0, OE + e1, ON + n1); r = geo.Raster(f, window=w)
    k = int(step // 10); a = r.a[: (r.a.shape[0] // k) * k, : (r.a.shape[1] // k) * k].reshape(r.a.shape[0] // k, k, r.a.shape[1] // k, k, 3).mean((1, 3))
    r.a = a; r.dx *= k; r.dy *= k; r.half = 0.5
    tci = r.sample(X + OE, Y + ON, order=1).clip(0, 255)
    land = dsm > 0.8
    gr = tci.mean(-1); urb = land & (gr > 120) & (tci[..., 1] < tci[..., 0] * 1.05)
    known = land & ~urb; _, (ri, ci) = ndimage.distance_transform_edt(~known, return_indices=True)
    nat = np.where(urb[..., None], ndimage.gaussian_filter(tci[ri, ci], (2, 2, 0)), tci)
    nat = np.where(land[..., None], nat, tci)
    Image.fromarray(nat.astype(np.uint8)).save(out / "far.jpg", quality=90)
    np.where(land, np.maximum(dsm, 0.8), -20.0).astype(np.float32).tofile(out / "far.f32")
    M = json.loads((out / "meta.json").read_text()); M.update(far_box=list(box), far_step=step, far_shape=list(dsm.shape), far_urban_px=int(urb.sum())); (out / "meta.json").write_text(json.dumps(M, indent=1))
    print("far", dsm.shape, "urban px", int(urb.sum()))

if __name__ == "__main__" and "--far" in __import__("sys").argv:
    build_far("gib")

# ---------------------------------------------------------------------------------------------------------------------------------
# V5b-1b · PHÂN LỚP NỀN (cổng 16/10 TRƯỢT: "nền vệ tinh 10 m mờ, loang ở cận/trung cảnh"). Ảnh vệ tinh/NDVI/OSM CHỈ để PHÂN LỚP;
# terrain.js tô vật liệu thủ tục theo lớp ở < 2 km, vệ tinh chỉ còn cho > 2 km. Ra pack/cls.png (10 m, đọc nearest):
#   R = lớp TỰ NHIÊN (trạng thái trước đô thị hoá — dùng cho năm < năm đô thị của điểm), G = lớp ĐÔ THỊ 2026,
#   B = khoảng cách tới biển theo bờ 1987 (m, ≤ 255), A = khoảng cách tới biển theo bờ 2026 (m, ≤ 255).
# Lớp: 1 cát bãi · 2 cỏ khô · 3 bụi maquis · 4 đá vôi · 5 ruộng/vườn · 6 nhựa · 7 nền lát đô thị · 8 sân thể thao · 9 bãi đỗ
#      10 bê tông cảng/công nghiệp · 11 đất trống/công trường · 12 cỏ công viên · 13 đồng cỏ (eo đất trước đô thị hoá)
# Quy tắc (không bịa nội dung: lớp tự nhiên ở vùng nay là đô thị = đồng cỏ/cát theo độ cao + khoảng cách bờ — khớp ảnh LoC 2025710366
# c.1900 "Neutral ground": đồng cỏ tối có lối mòn sáng, bãi cát dọc bờ — là PHONG CÁCH HOÁ, ghi trong báo cáo).
CLS = dict(sand=1, dry=2, scrub=3, rock=4, farm=5, asph=6, paved=7, pitch=8, park_=9, port=10, bare=11, lawn=12, meadow=13)

def build_classes(name):
    src = CACHE / "scene" / name; out = src / "pack"; M = json.loads((src / "meta_rasters.json").read_text()); ext = M["ext"]; e0, n0, e1, n1 = ext
    Z = np.load(src / "r_state.npz"); dtm, landY, urb26, land26, land87 = Z["dtm"], Z["landY"], Z["urb26"], Z["land26"], Z["land87"]
    ndvi = np.load(src / "r_ndvi.npy"); tci = np.load(src / "r_s2tci.npy"); H_, W_ = dtm.shape
    X, Y = np.meshgrid(np.arange(e0, e1 + 1e-6, STEP), np.arange(n1, n0 - 1e-6, -STEP))
    gy_, gx_ = np.gradient(dtm, STEP); slope = np.degrees(np.arctan(np.hypot(gx_, gy_)))
    d26 = ndimage.distance_transform_edt(land26) * STEP; d87 = ndimage.distance_transform_edt(land87 | (landY == 0) & land26) * STEP
    bright = tci.mean(-1)
    V = json.loads((src / "v_osm.json").read_text())
    def burn(pred):
        P = [a["p"] for a in V["area"] if pred(a["t"])]; return raster_polys(dtm.shape, ext, P, np.ones(len(P))) > 0 if P else np.zeros(dtm.shape, bool)
    o_beach = burn(lambda t: t.get("natural") in ("beach", "sand")); o_rock = burn(lambda t: t.get("natural") in ("bare_rock", "cliff", "scree"))
    o_scrub = burn(lambda t: t.get("natural") in ("scrub", "heath", "wood") or t.get("landuse") == "forest")
    o_farm = burn(lambda t: t.get("landuse") in ("farmland", "orchard", "allotments", "farmyard", "vineyard"))
    o_pitch = burn(lambda t: t.get("leisure") in ("pitch", "stadium", "sports_centre", "track"))
    o_park = burn(lambda t: t.get("amenity") == "parking" or t.get("landuse") == "garages")
    o_port = burn(lambda t: t.get("landuse") in ("industrial", "port", "railway", "landfill") or t.get("leisure") == "marina")
    o_bare = burn(lambda t: t.get("landuse") in ("construction", "brownfield", "greenfield"))
    o_lawn = burn(lambda t: t.get("landuse") in ("grass", "recreation_ground", "cemetery", "village_green") or t.get("leisure") in ("park", "garden", "playground"))
    o_meadow = burn(lambda t: t.get("landuse") == "meadow" or t.get("natural") == "grassland")
    rock_zone = (dtm > 25) | (slope > 12)
    o_mil = burn(lambda t: t.get("landuse") == "military"); bz = Z["urbY"] < 9999   # gần toà (≤ 40 m): khu quân sự trống (Upper Rock) KHÔNG coi là phố
    urb26 = urb26 & ~(o_mil & ~bz)
    # ---- lớp tự nhiên (mọi điểm đất)
    nat = np.full(dtm.shape, CLS["meadow"], np.uint8)
    nat[(ndvi < 0.30) & ~rock_zone] = CLS["dry"]
    nat[rock_zone & (ndvi >= 0.36)] = CLS["scrub"]; nat[rock_zone & (ndvi >= 0.22) & (ndvi < 0.36)] = CLS["dry"]
    nat[rock_zone & (ndvi < 0.22)] = CLS["rock"]; nat[(slope > 38) | o_rock] = CLS["rock"]; nat[o_scrub & (slope <= 38)] = CLS["scrub"]
    nat[~rock_zone & (ndvi >= 0.5) & ~urb26] = CLS["scrub"]
    nat[urb26 & ~rock_zone] = CLS["meadow"]; nat[bz & rock_zone & (slope <= 38)] = CLS["dry"]   # sườn nay là phố: NDVI thấp do mái nhà, không phải đá   # nay là đô thị, đất thấp: đồng cỏ (ảnh LoC c.1900) — shader xen cỏ khô theo nhiễu
    sandy = (~rock_zone) & ((d87 <= 45) | (d26 <= 45) & (landY == 0)) | o_beach
    nat[sandy] = CLS["sand"]; nat[(landY >= 1987) & (landY < 9999)] = CLS["bare"]   # đất khai hoang: nền đổ, trống
    nat[o_farm] = CLS["farm"]
    # ---- lớp đô thị 2026
    urb = nat.copy(); u = urb26 & land26
    urb[u] = CLS["paved"]; urb[u & (ndvi > 0.42)] = CLS["lawn"]
    for k, m in (("lawn", o_lawn), ("bare", o_bare), ("port", o_port), ("park_", o_park), ("pitch", o_pitch)): urb[m & land26] = CLS[k]
    urb[Z["aer"] & land26] = CLS["asph"]; urb[o_beach] = CLS["sand"]
    urb[~u & ~(o_lawn | o_pitch | o_park | o_port | o_bare)] = nat[~u & ~(o_lawn | o_pitch | o_park | o_port | o_bare)]
    nat[~land26 & ~land87] = 0; urb[~land26] = 0
    img = np.stack([nat, urb, np.clip(d87, 0, 255).astype(np.uint8), np.clip(d26, 0, 255).astype(np.uint8)], -1)
    Image.fromarray(img, "RGBA").save(out / "cls.png")
    pal = np.array([[30, 60, 110], [230, 210, 160], [180, 170, 100], [60, 100, 40], [200, 195, 180], [170, 140, 70], [60, 60, 65], [170, 165, 155], [60, 150, 60], [90, 90, 100], [140, 140, 140], [150, 110, 80], [90, 170, 80], [130, 150, 70]], np.uint8)
    Image.fromarray(np.concatenate([pal[nat], pal[urb]], 1)).save(src / "dbg_cls.png")
    cnt = {k: [int((nat == v).sum()), int((urb == v).sum())] for k, v in CLS.items()}
    Mp = json.loads((out / "meta.json").read_text()); Mp["cls"] = dict(names=CLS, count_nat_urb=cnt); (out / "meta.json").write_text(json.dumps(Mp, indent=1)); print("cls", cnt)

if __name__ == "__main__" and "--cls" in __import__("sys").argv:
    build_classes("gib")

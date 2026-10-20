// V7-PILOT T3 (19/10/2026) · CẢNH TIMELAPSE "XƯƠNG SỐNG" (luật hình TL-1…TL-6): MỘT điểm máy cao cố định (hoặc trôi ≤ 2 % khung/giây), THỜI GIAN chạy liên tục
//  theo đường cong opt.time (tl7.timeline) — nhà mọc/sập theo năm (city.js aYear + lớp ghost), chiến tuyến 1730 mọc, trại + công sự vây hãm 1779–83 dựng lên/rút
//  (data/eo-dat-v7.json, nguồn + bậc), hàng rào 1909, đường băng mọc qua đường rồi lấn vịnh (uRecl), tàu ra vào theo năm, ngày–đêm thật, khói theo sự kiện.
//  Dùng đường ống V6 bản SẢN XUẤT như t3s.js (bóng khít khung, SSAO, chỉnh màu V6, người có khớp, khói giả thể tích).
//  Khung sạch (§12.1 + TL-4): overlay CHỈ bộ đếm (năm / tháng / ngày / ngày-giờ theo tốc độ thời gian). Nguồn + bậc: meta (log), không lên hình.
import { makeCamPath } from '../campath.js';
import { footprints, town1782, units, smoke } from '../layers.js';
import { makeFleet, lineFormation } from '../ships.js';
import { life, chimneysFrom } from '../life.js';
import { flags } from '../props.js';
import { timeline, win, crossings, camps, lamps, fence, driftPct, yearRate } from '../tl7.js';
import { ruins } from '../ruins.js';
import { rng } from '../core.js';
import { shipFlags, rims } from '../phe.js';   // V7B: cờ tàu + viền màu phe (việc 2)
import { phaseMaps } from '../layers.js';

export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };
export const GRADE = { vib: 0.78 };
export const V6 = { sunK: 1.1, hemiK: 1.2, grade: [1.0, 0.35, 0.6], wave: 1.8 };
export const META = { cau: 'v7p', vai: 'co-che', nam: null };
const RZ_T = 1781.278;   // 12/4/1781 10:45 — pháo TBN bắn vào phố (S062); phố 'THE RUINS' (Drinkwater 1786) từ đây

// V7C (việc 1, NC-D1): CÁCH A đóng gói thành tuỳ chọn cảnh opt.nc — không khai (hoặc nc: false / nc.off) → đúng đường V7B (up.js KHÔNG nạp: nó thay fog_fragment toàn cục);
//  khai opt.nc = { bake | bakes: [{dir, wY: [năm đầu, năm cuối], fire?}], bushes, water, haze, tex, … } → bọc như design/k2v/tl/nc/ncA.js (NC-CPU) — cùng thứ tự preBuild → cảnh → postBuild.
export async function build(ctx) {
  const P = ctx.opt && ctx.opt.nc;
  if (!P || P.off) return buildCore(ctx);
  const { preBuild, postBuild } = await import('../nc/up.js');
  const pre = await preBuild(ctx, P), SC = await buildCore(ctx), post = await postBuild(ctx, SC, P, pre), apply0 = SC.apply;
  SC.apply = (st, t) => { apply0(st, t); post.update(st, t); };
  SC.meta = Object.assign({}, SC.meta, { nc: post.meta });
  globalThis.NC = { ctx, SC, post };
  return SC;
}

export async function buildCore(ctx) {
  const { THREE, terr, scene } = ctx, o = ctx.opt || {}, fps = 24, DUR = o.dur, hAt = (e, n) => Math.max(0, terr.hAt(e, n));
  if (!(DUR > 0)) throw new Error('t3tl: thiếu opt.dur');
  const TL = timeline(o.time, { tz: o.tz ?? null }), Y0 = Math.min(...[0, DUR / 2, DUR].map(TL.year)), Ymin = (() => { let m = 1e9, M = -1e9; for (let t = 0; t <= DUR; t += 0.05) { const y = TL.year(t); m = Math.min(m, y); M = Math.max(M, y); } return [m, M]; })();
  const inR = (a, b) => Ymin[1] >= a && Ymin[0] <= b;   // shot có đi qua cửa sổ năm [a, b] không
  const D = await ctx.loadJSON('/k2v/tl/data/eo-dat-v7.json'), src = [], log = { lop: [] };
  const lines = ctx.lines || {};
  // ---------- phố theo cửa sổ năm ----------
  // gói (pack): OSM 2026 + Catastro theo năm xây + ghost 1704 (V5b-1) + ghost c.1880/c.1900 — liền mạch 1704 → 2026 qua shader aYear. Cửa sổ 1779–1783,6: phố Drinkwater 1786
  //  (ghost SH + công sự + lấp ước tính); trước 12/4/1781 vùng 'THE RUINS' còn NGUYÊN (khối lấp dựng như nhà), từ 12/4/1781 thành phế tích (ruins.js).
  let TOWN = null, INT = null, G43 = null; const W1782 = [1779.0, 1783.6];
  if (o.town !== false && inR(...W1782)) {
    TOWN = await town1782(ctx, { ruinsZone: true, hidPack: false }); src.push(TOWN.src, TOWN.INFILL_SRC, TOWN.RUINS_SRC);
    const RZ = (await ctx.loadJSON('/k2v/tl/data/ruins-zone-1782.json')).zone_enu, pip = (p, r) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > p[1]) !== (r[j][1] > p[1]) && p[0] < (r[j][0] - r[i][0]) * (p[1] - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; };
    // PHỐ SẬP DẦN: khối lấp trong vùng 'THE RUINS' chia 8 nhóm (tất định theo chỉ số) sập lần lượt 15/4 → giữa 6/1781 (pháo kích 4–6/1781, S062–S063; trạng thái 'RUINS' của plan 1786
    //  — ngày từng nhóm là ƯỚC TÍNH); 5 nhà gần Spanish Church cháy đêm 13→14/4/1781 rồi sập (S063: 4–5 nhà cháy; vị trí ước tính) — o.burn
    if (TOWN.RU) TOWN.RU.group.visible = false;
    const cen = (r) => [r[6].reduce((a, q) => a + q[0], 0) / r[6].length, r[6].reduce((a, q) => a + q[1], 0) / r[6].length];
    const IRall = (await ctx.loadJSON(`${ctx.base}layers/infill1782.json`)).records.filter((r) => pip(cen(r), RZ)), key = (r) => Math.round(cen(r)[0] * 7 + cen(r)[1] * 13);
    const BURN = o.burn ? IRall.slice().sort((a, b) => Math.hypot(cen(a)[0] - o.burn.at[0], cen(a)[1] - o.burn.at[1]) - Math.hypot(cen(b)[0] - o.burn.at[0], cen(b)[1] - o.burn.at[1])).slice(0, o.burn.n).map(key) : [];
    const grpOf = (r) => (BURN.includes(key(r)) ? -1 : ((key(r) % 8) + 8) % 8);
    INT = []; for (const gi of [-1, 0, 1, 2, 3, 4, 5, 6, 7]) { const R = IRall.filter((r) => grpOf(r) === gi); if (!R.length) continue;
      const fp = await footprints([{ file: 'infill1782', ghostDesat: 0.08, years: [1700, 2100], keep: (r) => pip(cen(r), RZ) && grpOf(r) === gi }], ctx); scene.add(fp.group);
      const ru = ruins(fp.list[0].recs, ctx, { seed: 1781 + gi }); scene.add(ru.group);
      INT.push({ fp, ru, tc: gi < 0 ? o.burn.t1 : RZ_T + 0.012 + gi * (1781.45 - RZ_T - 0.012) / 7, recs: R }); }
    if (o.burn) { const BR = INT.find((x) => x.tc === o.burn.t1); if (BR) { o.fires = (o.fires || []).concat(BR.recs.map((r) => ({ at: cen(r), wY: [o.burn.t0, o.burn.t1 + 0.0004], size: 26 })));
      o.smoke = (o.smoke || []).concat(BR.recs.map((r, i) => ({ at: [cen(r)[0], 10, cen(r)[1]], wY: [o.burn.t0, o.burn.t1 + 0.004], n: 12, size: 34, rise: 80, drift: [-1.6, 0.6], period: 0.3, seed: 700 + i, alpha: 0.9, dark: true }))); } }
    log.lop.push({ lop: 'pho1782', nguon: 'Drinkwater 1786 Plan of the Batteries (ghost SH) + lấp ước tính + vùng RUINS', bac: 'bậc 1 bố cục; lấp + phế tích: ước tính', cua_so: W1782 });
  }
  if (o.town !== false && inR(1939, 1946)) { G43 = await footprints([{ file: 'ghost1943', ghostDesat: 0.08 }], ctx); scene.add(G43.group); log.lop.push({ lop: 'ghost1943', nguon: 'AMS M981 1943', bac: 'bậc 1' }); }
  const roads0 = ctx.roads ? ctx.roads.mesh.visible : true;
  // ---------- Línea 1730 (mọc tây → đông), công sự tiền phương 1779–83, trại ----------
  const LNsegs = [];
  if (o.linea !== false && inR(1729, 1811)) { const { fortify, wallRing } = await import('../fort.js'); const LL = await ctx.loadJSON(`${ctx.base}layers/lines1782.json`), recs0 = [];
    for (const l of LL.lines.filter((x) => x.loai === 'chien_tuyen')) for (let i = 0; i < l.pts.length - 1; i++) { const a = l.pts[i], b = l.pts[i + 1], hs = [a, b].map(([e, n]) => terr.hAt(e, n)), lo = Math.max(0.3, Math.min(...hs)), hi = Math.max(0.3, ...hs);
      recs0.push([0, 0, 5.5 + (hi - lo), lo, 0, 1, wallRing([a, b], 3, 3), 0]); }
    recs0.sort((a, b) => a[6][0][0] - b[6][0][0]);
    for (const r of recs0) { const f = fortify([r], ctx, { thick: 2.0, batter: 0.12, embr: 9, gunEvery: 2, garita: true, seed: 71, face: [0, -1] }); scene.add(f.group); LNsegs.push(f.group); }
    if (TOWN && TOWN.LN) TOWN.LN.group.visible = false;   // town1782 cũng dựng Línea — dùng bản mọc theo năm của cảnh
    log.lop.push({ lop: 'linea1730', w: D.linea.w, nguon: D.linea.nguon, bac: D.linea.bac }); }
  let WORKS = null;
  if (o.works !== false && inR(1779.6, 1783.5)) { const { frontLines } = await import('../layers.js'); const L = await ctx.loadJSON(`${ctx.base}layers/lines1782_tp.json`);
    WORKS = frontLines(L.lines.map((l) => ({ pts: l.pts, side: 'es', w: 16, berm: 2.4, trench: 1, stone: '#b49a74', band: false, grow: [0, 1] })), ctx); scene.add(WORKS.group);
    const FT = await footprints([{ file: 'fort1782_tp', fort: true, h: 4, years: [1700, 2100] }], ctx); scene.add(FT.group); WORKS.FT = FT;
    log.lop.push({ lop: 'cong_su_tien_phuong', w: D.cong_su_tien_phuong.w, nguon: D.cong_su_tien_phuong.nguon, bac: D.cong_su_tien_phuong.bac }); }
  let CAMP = null;
  const CFL = []; if (o.campFlags && inR(1779.5, 1783.3)) for (const t of D.trai) { const a = t.pts[0], b = t.pts[t.pts.length - 1], d = Math.hypot(b[0] - a[0], b[1] - a[1]), k = Math.max(1, Math.round(d / 380));   // V7B: cờ trung đoàn (Cruz de Borgoña) dọc mỗi dãy trại TBN, ≈ 380 m một cờ; trại Pháp cờ trắng
    for (let i = 0; i <= k; i++) { const u = i / k, at = [a[0] + (b[0] - a[0]) * u - (b[1] - a[1]) / d * 50, a[1] + (b[1] - a[1]) * u + (b[0] - a[0]) / d * 50]; const G = flags([{ at, pole: 10, w: 4.0, scale: 1.5, kind: t.side === 'fr' ? 'fr_white' : 'burgundy', toward: 110, phase: i * 0.9 }], ctx); scene.add(G.group); CFL.push({ G, t }); } }
  if (CFL.length) log.lop.push({ lop: 'co_trai', n: CFL.length, nguon: 'cờ trung đoàn bộ binh TBN mang Cruz de Borgoña (thế kỷ 18) — bậc 3 mẫu; vị trí/số cờ minh hoạ (bậc 5); cỡ 4 × 2 m × 1,5', bac: 'bậc 3–5' });
  if (o.camps !== false && inR(1779.5, 1783.3)) { CAMP = camps(D.trai, ctx, o.campRows ? { hangLoi: true } : {}); scene.add(CAMP.group);   // 35 % lều theo cửa sổ 1779 (≈ 14 000 quân), phần còn lại theo cửa sổ 1782 (≈ 40 000)
    log.lop.push({ lop: 'trai', so_leu: CAMP.n, nguon: D.trai[0].nguon, bac: D.trai[0].bac }); }
  // ---------- hàng rào 1909 ----------
  let FEN = null; if (o.fence !== false && lines.border && inR(1908.9, 2027)) { FEN = fence(lines.border, ctx, { w: D.hang_rao_1909.w }); scene.add(FEN.group); log.lop.push({ lop: 'hang_rao_1909', nguon: D.hang_rao_1909.nguon, bac: D.hang_rao_1909.bac }); }
  // ---------- đường băng + đất lấn vịnh mọc dần (heroes.js/terrain.js uRecl) ----------
  ctx.U.uRecl.value = o.recl === false ? 0 : 1;
  // ---------- cờ trên Tower of Homage: Borgoña 1506–1704, Union từ 4/8/1704 ----------
  // V7B (việc 2): o.co = [{at: 'tower' | [E, N], kind, scale ≤ 1,5, pole, w, toward, on, off (năm), hoist: [[năm, 0..1], …]}] — cờ theo nguồn mẫu (props.js), hạ–kéo theo năm
  const CO = []; if (o.co) { const H = await ctx.loadJSON(`${ctx.base}heroes.json`), tw = H.tower, tc = [tw.p.reduce((a, q) => a + q[0], 0) / tw.p.length, tw.p.reduce((a, q) => a + q[1], 0) / tw.p.length];
    for (const f of o.co) { const tower = f.at === 'tower', G = flags([{ at: tower ? tc : f.at, base: tower ? tw.base + tw.h : f.base, pole: f.pole || 9, w: f.w || 6.0, toward: f.toward ?? 120, kind: f.kind, scale: f.scale || 1, phase: CO.length * 0.7 }], ctx); scene.add(G.group); CO.push({ f, G }); }
    log.lop.push({ lop: 'co_v7b', n: CO.length, mau: [...new Set(o.co.map((f) => f.kind))], scale_max: Math.max(...o.co.map((f) => Math.min(1.5, f.scale || 1))), nguon: 'mẫu cờ: props.js (nguồn ở V7B §2); vị trí cột: Line Wall/bastion theo ghost SH 1782, lâu đài theo heroes.json; cỡ ước 6 × 3 m × scale', bac: 'mẫu: bậc 3; cỡ/cột: bậc 4–5' }); }
  const hoistAt = (f, Y) => { if (!f.hoist) return 1; const H = f.hoist; if (Y <= H[0][0]) return H[0][1]; for (let i = 1; i < H.length; i++) if (Y <= H[i][0]) { const u = (Y - H[i - 1][0]) / (H[i][0] - H[i - 1][0]); return H[i - 1][1] + (H[i][1] - H[i - 1][1]) * u; } return H[H.length - 1][1]; };
  let FLB = null, FLU = null; if (!o.co && o.flags !== false && inR(1506, 2027)) { const H = await ctx.loadJSON(`${ctx.base}heroes.json`), tw = H.tower, c = [tw.p.reduce((a, q) => a + q[0], 0) / tw.p.length, tw.p.reduce((a, q) => a + q[1], 0) / tw.p.length];
    const sp = { at: c, base: tw.base + tw.h, pole: 9, w: 6.0, toward: 120 }; FLB = flags([Object.assign({ kind: 'burgundy' }, sp)], ctx); FLU = flags([Object.assign({ kind: 'union1707' }, sp)], ctx); scene.add(FLB.group, FLU.group);
    log.lop.push({ lop: 'co', nguon: D.co.nguon, bac: 'mẫu cờ: bậc 3–4; cột: minh hoạ' }); }
  // ---------- nhịp vây hãm (khói theo giây cảnh khi bộ đếm đi qua năm vây) ----------
  const SMK = [].concat(o.smoke || []);
  if (o.sieges) { const H = await ctx.loadJSON(`${ctx.base}heroes.json`), tw = H.tower.p[0];
    for (const s of D.vay_ham.danh_sach) for (const tc of crossings(TL, s.nam, DUR).filter((x) => TL.year(x + 0.02) > TL.year(x - 0.02))) SMK.push(   // chỉ khi thời gian chạy XUÔI
      { at: [tw[0] - 40, 95, tw[1] - 60], t: [tc - 0.05, tc + 1.6], n: 18, size: 130, rise: 200, drift: [-3, 1], period: 0.45, seed: 300 + s.stt, alpha: 0.9, fire: 0.5 },
      { at: [-470, 14, -1300], t: [tc, tc + 1.5], n: 16, size: 150, rise: 180, drift: [-3, 1], period: 0.42, seed: 330 + s.stt, alpha: 0.85 },
      { at: [-430, 10, -1000], t: [tc + 0.1, tc + 1.5], n: 14, size: 120, rise: 160, drift: [-3, 1], period: 0.4, seed: 360 + s.stt, alpha: 0.8 },
      { at: [-650, 10, -1250], t: [tc + 0.05, tc + 1.4], n: 12, size: 110, rise: 140, drift: [-3, 1], period: 0.38, seed: 390 + s.stt, alpha: 0.8, fire: 0.6 });   // V7P lượt 2: nhịp lớn hơn (lượt 1: khói nhỏ, khó đọc ở 2,2 km)
    log.lop.push({ lop: 'nhip_vay_ham', so: D.vay_ham.danh_sach.length, nguon: D.vay_ham.nguon, bac: 'thời điểm: bậc 2; vị trí khói: minh hoạ' }); }
  // khói theo năm (wY) → đổi sang giây cảnh tại các điểm đường cong đi qua
  //  (mọi khoảng giây mà năm nằm trong cửa sổ — đường cong tua ngược có thể đi qua cùng một năm nhiều lần; khoảng < 0,25 s bỏ: chạy qua quá nhanh, khói không kịp hiện)
  const ivals = (w) => { const out = []; let a = null; for (let f = 0; f <= Math.round(DUR * fps) + 1; f++) { const t = f / fps, y = TL.year(Math.min(t, DUR)), on = y >= w[0] && y <= w[1] && t <= DUR; if (on && a == null) a = t; if (!on && a != null) { if (t - a >= 0.25) out.push([a, t]); a = null; } } return out; };
  const smk = SMK.flatMap((s) => (s.t ? [s] : ivals(s.wY).map(([a, b], i) => Object.assign({}, s, { t: [a, b + (i >= 0 ? 0.6 : 0)], seed: (s.seed || 5) + i * 17 }))));
  const SM = smk.length ? smoke(smk.map((s) => Object.assign({ zone: 'path' }, s)), ctx) : null; if (SM) scene.add(SM.group);
  // ---------- tàu / hạm đội theo năm (path theo năm thập phân) ----------
  const FLEETS = [], SF = [], RIM = []; for (const f of o.fleets || []) { const S = f.list || lineFormation(f); const F = makeFleet(ctx.U, S.map((s, i) => Object.assign({ heading: f.heading ?? 0, t: f.wY, v6: true, side: -1, burning: !!f.burning, flag: f.soai != null && i === f.soai }, s, f.path ? { path: f.path.map(([y, de, dn]) => [y, s.at[0] + de, s.at[1] + dn]) } : {}))); F.group.traverse((m) => { if (m.isMesh) ctx.maskify(m.material, ctx.U, 1); }); scene.add(F.group); FLEETS.push(F);
    if (f.phe) { if (f.co !== false) SF.push(shipFlags(F, f.phe, ctx, { scale: f.coScale ?? 1.5 })); if (!o.rimPhe || o.rimPhe.includes(f.phe)) F.list.forEach((x, i) => RIM.push({ phe: f.phe, a: x.sp.kind === 'line' || x.sp.kind === 'battery' ? 60 : 46, b: x.sp.kind === 'line' || x.sp.kind === 'battery' ? 32 : 26, y0: 0.8, pos: () => (x.g.visible ? [x.g.position.x, -x.g.position.z, x.g.rotation.y] : null) })); } }
  if (SF.length) log.lop.push({ lop: 'co_tau', n: SF.reduce((a, x) => a + x.n, 0), scale: SF[0].scale, co_m: [SF[0].w, SF[0].h], nguon: 'Red Ensign 1707–1800 (Order in Council 21/7/1707) · cờ hải quân TBN trắng + huy hiệu 1701–1785 (FOTW es1701/es1785) · Pháp: cờ trắng', bac: 'mẫu bậc 3; cỡ ≈ 8 × 4 m bậc 4; phe của từng đoàn theo nguồn sự kiện (S054/S055/S062/S065)' });
  ctx.ships.group.visible = o.ships !== false;
  // ---------- lớp sống theo cửa sổ năm ----------
  const LIVES = []; for (const L0 of o.lives || []) { const fix = (w) => Object.assign({}, w, { pts: typeof w.line === 'string' ? (w.line === 'WCA' ? lines.wca : L0.lines[w.line]) : w.line });
    const recs = TOWN ? TOWN.FP.list.flatMap((l) => l.recs) : [];
    const LF = life({ era: L0.era, seed: L0.seed || 1704, walkers: (L0.walkers || []).map(fix), crowds: (L0.crowds || []).map(fix), birds: L0.birds, boats: L0.boats, chimney: L0.chimney && recs.length ? { at: chimneysFrom(recs, L0.chimney), drift: [-1.4, 0.4] } : undefined }, ctx);
    scene.add(LF.group); LIVES.push({ LF, wY: L0.wY, speed: L0.speed || 1 }); }
  const TR = o.units && o.units.length ? units(o.units, ctx) : null; if (TR) scene.add(TR.group);
  let NG = null; if (o.ngua && inR(1779.5, 1783.3)) { const { horseLines } = await import('../ngua.js'); NG = horseLines(o.ngua, ctx); scene.add(NG.group);   /* V7C (việc 2d): ngựa kỵ binh trại 1779 (S048 "12 squadrons of horse") */
    log.lop.push({ lop: 'ngua_trai', n: NG.n, nguon: 'S048 Drinkwater 1786: 10/1779 quân TBN có 12 squadrons of horse', bac: 'số: bậc 2 (+ cỡ đội ≈ 120 bậc 5); vị trí hàng ngựa: bậc 5; hình: bậc 4–5' }); }
  let ST = null; if (o.pho2026 && inR(1990, 2027)) { const { streetLife } = await import('../duong2026.js'); ST = await streetLife(ctx, o.pho2026); log.lop.push(ST.log); }   /* V7C (việc 2e): cây/đèn/xe đỗ phố 2026 */
  let CSK = null; if (o.casks) { const c = o.casks, R0 = rng(1780), g = new THREE.CylinderGeometry(0.42, 0.42, 1.0, 8).rotateZ(Math.PI / 2), m = new THREE.MeshLambertMaterial({ color: 0x7a5534 }); ctx.maskify(m, ctx.U, 1);   // V7B: thùng tiếp tế chất trên Old Mole (S054 — đoàn mang lương thực; số/vị trí minh hoạ bậc 5)
    const im = new THREE.InstancedMesh(g, m, c.n), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), Yx = new THREE.Vector3(0, 1, 0), P = []; im.castShadow = im.receiveShadow = true;
    for (let i = 0; i < c.n; i++) { const row = Math.floor(i / 30), col = i % 30, lay = Math.floor(row / 3); P.push({ e: c.at[0] + (col - 15) * 1.1 + (R0() - 0.5) * 0.2, n: c.at[1] + (row % 3 - 1) * 1.0 + Math.floor(row / 3) * 0.0 + (lay ? 0.5 : 0), y: lay * 0.82, k: R0() }); }
    scene.add(im); CSK = { im, P, update(Y) { const k = win(Y, c.wY); P.forEach((x, i) => { const on = x.k < k; m4.compose(new THREE.Vector3(x.e, Math.max(terr.hAt(x.e, x.n), 0.5) + 0.42 + x.y, -x.n), q.setFromAxisAngle(Yx, 0.1), new THREE.Vector3(on ? 1 : 0, on ? 1 : 0, on ? 1 : 0)); im.setMatrixAt(i, m4); }); im.instanceMatrix.needsUpdate = true; } };
    log.lop.push({ lop: 'thung_tiep_te', n: c.n, nguon: 'S054 (đoàn Rodney mang lương thực)', bac: 'số/vị trí/hình: minh hoạ (bậc 5)' }); }
  if (o.units) for (const u of o.units) if (u.side && u.rim !== false && u.at && (!o.rimPhe || o.rimPhe.includes(u.side))) {   /* V7C (V7B-D4): opt.rimPhe = ['es'] → bỏ viền quanh tàu/quân Anh */ const rows = u.rows || 3, cols = u.cols || 24; RIM.push({ phe: u.side, at: u.at, a: cols * 0.9 * (u.sx || 1) / 2 + 6, b: rows * 1.3 * (u.sz || 1) / 2 + 6, rot: (90 - (u.heading || 0)) * Math.PI / 180 + Math.PI / 2, on: () => { const d = u.day || [-1e9, 1e9]; return CUR.Y >= d[0] && CUR.Y <= d[1]; } }); }
  const CUR = { Y: 0 }; const RM = RIM.length ? rims(RIM, ctx) : null; if (RM) { scene.add(RM.group); log.lop.push({ lop: 'vien_phe', n: RM.n, mau: 'BIBLE §11.1 (Anh #b03a2e, TBN #c9a227, Pháp #2e5c8a)', khi: 'máy > 1 km (mờ dần 800 → 1 200 m)', bac: 'dấu kiểu bản đồ (không phải vật trong cảnh)' }); }
  let FAD = null; if (o.faden) { FAD = await phaseMaps([{ url: `${ctx.base}layers/faden1783-v7b.png`, box: (await ctx.loadJSON(`${ctx.base}layers/faden1783-v7b.json`)).box, years: { on: -1e9 }, step: 25, lift: 1.5, opacity: o.faden.op ?? 0.88 }], ctx); scene.add(FAD.group);
    log.lop.push({ lop: 'faden1783_phu', t: o.faden.t, nguon: 'Faden 1783 (Yale 2046612, PD) nắn bằng 3 GCP (RMS 12,5 m trong vùng; ≤ 250 m ngoài) — scripts/k2tl/v7b_faden.py', bac: 'bậc 1 (tư liệu phủ khớp địa hình, TL-4)' }); }
  // ---------- đèn đêm (2026: đường OSM ≥ cấp phố; mép đường băng ICAO ≤ 60 m; lửa) ----------
  let LMP = null; if (o.lamps || (o.fires && o.fires.length)) { const specs = [], RD = o.lamps ? await ctx.loadJSON(`${ctx.base}roads.json`) : [], H = await ctx.loadJSON(`${ctx.base}heroes.json`), box = (o.lamps && o.lamps.box) || [-1e9, -1e9, 1e9, 1e9];
    const P = []; for (const r of RD) { if (!['trunk', 'primary', 'secondary', 'tertiary', 'residential', 'unclassified', 'living_street'].includes(r.c)) continue; const st = ['trunk', 'primary', 'secondary'].includes(r.c) ? 30 : 38; let acc = st / 2;
      for (let i = 0; i < r.p.length - 1; i++) { const a = r.p[i], b = r.p[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]); while (acc < l) { const u = acc / l, e = a[0] + (b[0] - a[0]) * u + (-(b[1] - a[1]) / l) * (r.w / 2 + 1.5), n = a[1] + (b[1] - a[1]) * u + ((b[0] - a[0]) / l) * (r.w / 2 + 1.5); if (e > box[0] && e < box[2] && n > box[1] && n < box[3] && terr.hAt(e, n) > 0.5) P.push([e, n]); acc += st; } acc -= l; } }
    specs.push({ pts: P, kind: 'pho', w: { on: 1950 } });
    const rw = H.runway.p, hw = H.runway.w / 2 + 1.5, R = []; for (let i = 0; i < rw.length - 1; i++) { const a = rw[i], b = rw[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]); for (let s = 0; s < l; s += 58) { const u = s / l, e = a[0] + (b[0] - a[0]) * u, n = a[1] + (b[1] - a[1]) * u; R.push([e, n + hw], [e, n - hw]); } }
    if (o.lamps) { specs.push({ pts: R, kind: 'rw', w: { on: 1955 }, gain: 0.9 });
      for (const th of H.thresholds) for (let k = -4; k <= 4; k++) specs.push({ pts: [[th[th.length - 1][0], th[th.length - 1][1] + k * 5]], kind: 'th', w: { on: 1955 } }); } else specs.length = 0;
    for (const f of o.fires || []) specs.push({ pts: [f.at], kind: 'fire', size: (f.size || 40) * 3,   /* quầng lửa đọc được ở 1–2 km */ w: f.wY ? { on: f.wY[0], off0: f.wY[1] } : null });
    LMP = lamps(specs, ctx); scene.add(LMP.group); log.lop.push({ lop: 'den_dem', n: LMP.n, nguon: 'đèn đường dọc đường OSM 2026 (cách 30–38 m) · đèn mép đường băng ICAO Annex 14 (≤ 60 m) · lửa: theo cảnh', bac: 'đèn đường: bậc 5 (kiểu đèn minh hoạ; cần ảnh 2020s đối chiếu) · đèn đường băng: bậc 3 (chuẩn ICAO)' }); }
  ctx.maskHide = [].concat(RM ? [RM.group] : [], FAD ? [FAD.group] : [], SM ? [SM.group] : [], LIVES.flatMap((x) => (x.LF.smokeGroup ? [x.LF.smokeGroup] : [])), LMP ? [LMP.group] : []);
  // ---------- máy: điểm cố định / trôi chậm (keys tuyệt đối [E, cao, N]) ----------
  const path = makeCamPath(o.cam.map((k) => ({ t: k.t, p: k.p.slice(), l: k.l.slice(), fov: k.fov ?? 40 })));
  const drift = driftPct(path, 0, DUR);
  if (o.hideCampTrees && ctx.trees && ctx.trees.hideWhere) { const dl = (e, n, a, b) => { const dx = b[0] - a[0], dn = b[1] - a[1], L2 = dx * dx + dn * dn || 1, u = Math.max(0, Math.min(1, ((e - a[0]) * dx + (n - a[1]) * dn) / L2)); return Math.hypot(e - a[0] - dx * u, n - a[1] - dn * u); };
    log.lop.push({ lop: 'cay_an_trai', n: ctx.trees.hideWhere((e, n) => D.trai.some((t) => dl(e, n, t.pts[0], t.pts[t.pts.length - 1]) < 110)) }); }   /* V7B: cây bụi hiện nay (NDVI 2026) trong dải trại ± 110 m ẩn khi có trại — bậc 5 */
  if (o.treeBox && ctx.trees && ctx.trees.hideWhere) { const b = o.treeBox; ctx.trees.hideWhere((e, n) => e > b[0] && e < b[2] && n > b[1] && n < b[3]); }   /* V7B: cây sát máy cận (C3) ẩn */
  const tree0 = o.hideOldTrees && ctx.trees && ctx.trees.hideWhere ? ctx.trees.hideWhere((e, n) => e > -800 && e < -150 && n > -1950 && n < -640 && terr.hAt(e, n) < 70) : 0;
  // ---------- trạng thái mỗi khung ----------
  function state(tt) { const year = TL.year(tt), sun = TL.sun(tt), night = o.night === false ? 0 : Math.max(0, Math.min(1, (-sun.el - 1) / 7));
    return { year, day: 0.5, cam: path.at(tt), spp: o.spp || 2, phase: 'tl', preset: 'timelapse', vai: o.vai || 'co-che', hero: null, noi: o.noi || 'eo_dat', sun, dayCycle: true, night,
      winNight: year >= 1950 ? night : 0, moon: o.moon, clock: { s: TL.label(tt) } }; }
  function apply(st, tt) { const Y = st.year, T = tt ?? 0;
    const in82 = Y >= W1782[0] && Y <= W1782[1];
    if (TOWN) { for (const g of [TOWN.FP.group, TOWN.GD && TOWN.GD.group, TOWN.LM && TOWN.LM.group].filter(Boolean)) g.visible = in82; if (TOWN.KB) TOWN.KB.group.visible = Y >= 1773;   // Line Wall + tường Charles V có suốt thời kỳ (giữ); King's Bastion xây 1773
      if (INT) for (const g of INT) { g.fp.group.visible = in82 && Y < g.tc; g.ru.group.visible = in82 && Y >= g.tc; if (g.fp.group.visible) g.fp.list[0].city.update(ctx.cam); }
      ctx.terr.uni.uGhostOn.value = in82 ? 1 : 0; if (ctx.roads) ctx.roads.mesh.visible = in82 ? false : roads0; ctx.city.group.visible = !in82;
      if (in82) TOWN.FP.update(Math.min(Math.max(Y, 1779.01), 1782.99), ctx.cam); }
    if (G43) G43.update(Y, ctx.cam);
    if (LNsegs.length) { const k = win(Y, D.linea.w), n = Math.round(k * LNsegs.length); LNsegs.forEach((g, i) => { g.visible = i < n; }); }
    if (WORKS) { const k = win(Y, D.cong_su_tien_phuong.w); for (const l of WORKS.list) { for (const m of l.mats) m.userData.uGrow.value = k * l.len + 0.01; for (const ms of l.meshes) ms.visible = k > 0.001; } WORKS.FT.group.visible = k > 0.6; }
    if (CAMP) CAMP.update(Y);
    if (FEN) FEN.update(Y);
    if (FLB) { FLB.group.visible = Y >= 1506 && Y < 1704.59; FLU.group.visible = Y >= 1704.59; FLB.update(T); FLU.update(T); }
    for (const { f, G } of CO) { G.group.visible = Y >= (f.on ?? -1e9) && Y < (f.off ?? 1e9); if (G.group.visible) G.update(T, hoistAt(f, Y)); }
    for (const { G, t } of CFL) { const k = t.w2 ? t.frac * win(Y, t.w) + (1 - t.frac) * win(Y, t.w2) : win(Y, t.w); G.group.visible = k > 0.15; if (G.group.visible) G.update(T); }
    for (const x of SF) x.update(T);
    CUR.Y = Y;
    if (FAD) { const [a, b] = o.faden.t, fd = o.faden.fade ?? 0.4, k = Math.max(0, Math.min(1, (T - a) / fd, (b - T) / fd)); for (const l of FAD.list) { l.m.opacity = k * (o.faden.op ?? 0.88); l.mesh.visible = k > 0.005; } }
    if (o.pre1704town && Y >= 1309 && Y < 1704) ctx.U.uYear.value = 1704.2;   // V7B: phố trước 1704 — dùng lớp tái dựng 1705 làm đại diện (bậc 5; phố trong tường thời Trung cổ có nhưng chưa có bản đồ trước 1704)
    for (const F of FLEETS) F.update(Y);
    const z = SM ? (SM.update(T), SM.zones(T)) : [];
    for (const L of LIVES) { const k = win(Y, L.wY); L.LF.group.visible = k > 0.5; if (k > 0.5) L.LF.update(T * L.speed, z); }
    if (TR) TR.update(Y, z, T);
    if (NG) NG.update(Y);
    if (ST) ST.update(Y);
    if (CSK) CSK.update(Y);
    if (LMP) LMP.update(st.night || 0, Y, T);
    if (RM) { for (const F of FLEETS) F.update(Y); RM.update(ctx.cam.position); } }
  function overlay(tt, st, T) { T.chrome(tt, { s: st.clock.s }, 0, null, null, null); }
  const N = Math.round(DUR * fps);
  const glog = () => ({ frames: [...Array(N).keys()].filter((f) => f % 6 === 0).map((f) => { const t = f / fps, c = path.at(t); return { f, t: +t.toFixed(3), pos: c.p.map((x) => +x.toFixed(1)), look: c.l.map((x) => +x.toFixed(1)), fov: +c.fov.toFixed(2), year: +TL.year(t).toFixed(4), agl: +(c.p[1] - hAt(c.p[0], c.p[2])).toFixed(1), nhan: TL.label(t) }; }),
    shots: [{ preset: 'timelapse', vai: o.vai || 'co-che', t: [0, DUR], drift_pct_s: drift, year_rate_max: +yearRate(TL, 0, DUR).toFixed(2) }] });
  return { N, fps, state, apply, overlay, path, grammarLog: glog, camLog: glog, anchors: {},
    namKhung: (st) => Object.assign({}, TOWN && st.year >= W1782[0] && st.year <= W1782[1] ? TOWN.namMax(st.year) : {}, G43 ? G43.namMax(st.year) : {}),
    meta: Object.assign({ shot: o.shot, diem_may: o.diem || null, cuts: [], cu: [{ preset: 'timelapse', vai: o.vai || 'co-che', t: [0, DUR] }], drift_pct_s: drift, nam: [+Ymin[0].toFixed(3), +Ymin[1].toFixed(3)],
      year_rate_max: +yearRate(TL, 0, DUR).toFixed(2), nguon_lop: src, lop: log.lop, cay_an: tree0, leu: CAMP ? CAMP.n : 0, quan: TR ? TR.stat() : null }, META, { noi: [[0, 99, o.noi || 'eo_dat']] }),
    troops: () => (TR ? TR.stat() : null), song: () => null,
    lopKhoi: () => ({ xay: [ctx.city.group, ctx.heroes.group, TOWN && TOWN.FP.group, TOWN && TOWN.GD && TOWN.GD.group, TOWN && TOWN.LM && TOWN.LM.group, TOWN && TOWN.KB && TOWN.KB.group, TOWN && TOWN.LN && TOWN.LN.group, G43 && G43.group, WORKS && WORKS.group, WORKS && WORKS.FT && WORKS.FT.group].concat(INT ? INT.flatMap((g) => [g.fp.group, g.ru.group]) : [], LNsegs).filter(Boolean),
      trai: CAMP ? [CAMP.group] : [], quan: TR ? [TR.group] : [] }),   /* V7B (việc 3): lớp đo tỉ lệ khối xây dựng / trại / quân trong khung (page.js classMask) */ smokeZones: () => (SM ? SM.zones(0) : []) };
}

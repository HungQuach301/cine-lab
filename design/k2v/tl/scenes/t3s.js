// G1b T3 (18/10/2026) · CẢNH 3D TỔNG QUÁT cho animatic + bản sản xuất toàn tập "Why Gibraltar Was Besieged 14 Times": MỘT mô-đun, mọi tham số từ opt của shot
//  (scripts/k2/hist… không; sinh bởi channel-k2/k2c-t3-01/g1b/mk_ep_g1b.py từ bảng shot vay-ham/treatment.json). Dùng đúng đường ống V6 bản SẢN XUẤT (llvmpipe: bóng khít khung,
//  SSAO hai tầng, chỉnh màu V6, người có khớp, khói giả thể tích) như vinh6/eo6/toan6/pho6/bo6.
//  · Lớp nhà theo mốc: base = gói cảnh theo năm (OSM 2026, Catastro La Línea theo năm xây, ghost c.1900/1880, 1987); town '1782' = town1782 (Drinkwater 1786 + lấp ước tính +
//    vùng 'THE RUINS OF GIBRALTAR'); '1704' = ghost1704 + fort1704 (plan 1705); '1943' = ghost1943 (AMS M981). Không lớp nào có năm > năm bộ đếm (NC-H5a qua namKhung).
//  · Máy: opt.cams = danh sách CÚ nối bằng CẮT (Q37: mỗi cú ≤ 6 s → không khoảng > 6 s không biến cố); mỗi cú một preset ngữ pháp (push-in, line = bay dọc tuyến,
//    orbit, lateral-parallax, top-down-rise, neo). Toạ độ ENU (m) quanh origin gói; độ cao [E, h, N] là h TRÊN MẶT ĐẤT (rel), trừ khi cú khai abs: true.
//  · Lớp sống (F3: ≥ 3 vật chuyển động): life (người có khớp đi dọc tuyến, đám đông, chim, thuyền, khói bếp), units (khối quân = người xếp hàng), smoke (khói giả thể tích),
//    fleet (hàng tàu theo nguồn), ships theo thời kỳ (gói). Không người trong vùng khói (zones), như cảnh V6.
//  · KHUNG SẠCH (§12.1): overlay CHỈ bộ đếm năm/ngày-giờ; chip nơi + số/câu trích do lớp 2D (scripts/k2/lib/k2.js, p.sach) vẽ theo đặc tả tập — cảnh KHÔNG vẽ dòng nguồn/phương pháp/nhãn AI.
//    Nguồn + bậc căn cứ từng lớp vẫn ghi trong meta (log) để kiểm bằng máy.
import { alongLine, grammar, grammarLog, pushIn, lateral, topDownRise, orbitKeys, neo, ALT_MAX } from '../campath.js';
import { footprints, town1782, units, smoke, frontLines, arrows } from '../layers.js';
import { fortify, wallRing } from '../fort.js';
import { boundaryRibbons } from '../overlay3d.js';
import { makeFleet, lineFormation } from '../ships.js';
import { life, chimneysFrom, freePath } from '../life.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };   // như cảnh V6 (V5b-2d C2-9: vách bắc + đỉnh 412 m theo ảnh PD LoC 2025710362)
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };
export const GRADE = { vib: 0.78 };
export const V6 = { sunK: 1.1, hemiK: 1.2, grade: [1.0, 0.35, 0.6], wave: 1.8 };
export const META = { cau: 'g1b', vai: 'co-che', nam: null };
// tuyến có tên (ENU m, đo từ OSM của gói — xem pho6.js/toan6.js/lines.json)
const LINES = {
  MAIN: [[-409, -1811], [-410, -1700], [-425, -1620], [-435, -1571], [-441, -1543], [-448, -1521], [-450, -1505], [-447, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880], [-417, -788]],
  LINEST: [[-560, -1700], [-552, -1500], [-548, -1350], [-546, -1200], [-545, -1050], [-548, -930]],
  GPR: [[-550, -1207], [-468, -1207], [-468, -1126], [-550, -1126], [-550, -1207]],
};
export async function build(ctx) {
  const { THREE, terr, scene } = ctx, o = ctx.opt || {}, fps = 24, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), DUR = o.dur;
  if (!(DUR > 0)) throw new Error('t3s: thiếu opt.dur');
  if (o.lines) Object.assign(LINES, o.lines);
  if (o.wca !== false && ctx.lines && ctx.lines.wca) LINES.WCA = ctx.lines.wca;
  const line = (x) => (typeof x === 'string' ? LINES[x] : x);
  ctx.ships.group.visible = o.ships !== false;
  // ---- năm (cố định hoặc track — timelapse 0e / 5j: mốc bằng chứng, không nội suy năm giữa mốc → bước theo mốc) ----
  const YT = o.yearAt || [[0, o.year]];
  const yearAt = (t) => { let y = YT[0][1]; for (const [tt, yy] of YT) if (t >= tt - 1e-6) y = yy; return y; };
  // ---- lớp nhà ----
  let TOWN = null, FP = null; const src = [];
  if (o.town === '1782') { TOWN = await town1782(ctx, Object.assign({ ruinsZone: true }, o.townOpt || {})); src.push(TOWN.src, TOWN.INFILL_SRC, TOWN.RUINS_SRC); }
  const extra = [].concat(o.town === '1704' ? [{ file: 'ghost1704', ghostDesat: 0.08 }, { file: 'fort1704', fort: true, h: 8 }] : [], o.town === '1943' ? [{ file: 'ghost1943', ghostDesat: 0.08 }] : [], o.layers || []);
  if (extra.length) { FP = await footprints(extra, ctx); scene.add(FP.group); FP.list.forEach((l) => src.push(l.src)); if (o.hidePack) ctx.city.group.visible = false; }
  // cây NDVI/OSM 2026 trong phố cổ ẩn ở mốc không có nguồn vườn/cây (như town1782): hộp [e0, n0, e1, n1], dưới 70 m
  if (o.hideTrees && ctx.trees && ctx.trees.hideWhere) { const [e0, n0, e1, n1] = o.hideTrees; ctx.trees.hideWhere((e, n) => e > e0 && e < e1 && n > n0 && n < n1 && terr.hAt(e, n) < 70); }
  // Línea de Contravalación (TBN, 1730–35; ghost SH từ Drinkwater 1786, lớp lines1782 chien_tuyen) — tường đá thấp 5,5 m như town1782; lineaAt = [[t, phần đã xây 0..1]] (mọc từ tây sang đông)
  let LN = null, lineaN = 0, LNsegs = [];
  if (o.linea) { const LL = await ctx.loadJSON(`${ctx.base}layers/lines1782.json`), recs0 = [];
    for (const l of LL.lines.filter((x) => x.loai === 'chien_tuyen')) for (let i = 0; i < l.pts.length - 1; i++) { const a = l.pts[i], b = l.pts[i + 1], hs = [a, b].map(([e, n]) => terr.hAt(e, n)), lo = Math.max(0.3, Math.min(...hs)), hi = Math.max(0.3, ...hs);
      recs0.push([0, 0, 5.5 + (hi - lo), lo, 0, 1, wallRing([a, b], 3, 3), 0]); }
    recs0.sort((a, b) => a[6][0][0] - b[6][0][0]); lineaN = recs0.length;
    LNsegs = recs0.map((r) => { const f = fortify([r], ctx, { thick: 2.0, batter: 0.12, embr: 9, gunEvery: 2, garita: true, seed: 71, face: [0, -1] }); scene.add(f.group); return f.group; });
    src.push('Línea de Contravalación: Drinkwater 1786 (ghost SH)'); }
  const lineaFrac = (tt) => { if (!o.lineaAt) return 1; let v = o.lineaAt[0][1]; for (const [a, b] of o.lineaAt) if (tt >= a - 1e-6) v = b; return v; };
  const FR = o.front ? frontLines(o.front, ctx) : null; if (FR) scene.add(FR.group);
  const AR = o.arrows ? arrows(o.arrows, ctx) : null; if (AR) scene.add(AR.group);
  // boundary trace: dải hai bên ranh giới OSM, màu theo SỐ toà mỗi bên theo năm (border.json toa_dung — như presets.js)
  let RIB = null, BJ = null; if (o.ribbons && ctx.lines && ctx.lines.border) { RIB = boundaryRibbons(ctx.lines.border, hAt, ctx.U); scene.add(RIB.group); BJ = await ctx.loadJSON(`${ctx.base}border.json`); LINES.BORDER = ctx.lines.border; }
  if (ctx.lines && ctx.lines.border) LINES.BORDER = ctx.lines.border;
  // ---- máy: các cú nối bằng cắt ----
  const shots = []; let t = 0;
  const P = (q, abs) => (abs ? q.slice() : [q[0], hAt(q[0], q[2]) + q[1], q[2]]);
  for (const [i, c] of (o.cams || []).entries()) {
    const t0 = t, t1 = i === o.cams.length - 1 ? DUR : t + c.dur, vai = c.vai || o.vai || 'co-che'; t = t1;
    let s;
    if (c.k === 'push') s = pushIn({ vai, from: P(c.from, c.abs), to: P(c.to, c.abs), look: P(c.look, c.abs), t0, t1, hold: c.hold ?? Math.min(1.0, (t1 - t0) * 0.25), fov: c.fov ?? 40, fov1: c.fov1 });
    else if (c.k === 'line') { const L = line(c.line); if (c.type && c.h > ALT_MAX[c.type]) throw new Error(`t3s ${o.shot}: bay ${c.h} m > ALT_MAX.${c.type}`);
      const K = alongLine(L, { s0: c.s0, s1: c.s1, t0, t1, h: Array.isArray(c.h) ? c.h : [c.h, c.h], look: c.look ?? 200, dip: c.dip ?? 40, dt: 0.2, hAt }).map((k) => Object.assign(k, { fov: c.fov ?? 40, l: [k.l[0] + (c.east || 0), k.l[1], k.l[2] + (c.north || 0)] }));
      s = { preset: 'fly-' + (c.type || 'pho'), vai, t: [t0, t1], keys: K, phases: [{ kind: 'fly', t: [t0, t1] }], route: { line: L, type: c.type || 'pho', nguon: c.nguon || 'OSM' } }; }
    else if (c.k === 'orbit') { const K = orbitKeys({ c: c.c, r: c.r, h: c.h, a0: c.a0, a1: c.a1, t0, t1, fov: c.fov ?? 38, hAt, look: c.lookUp || 0, prof: 'ease' }); s = { preset: 'orbit', vai, t: [t0, t1], keys: K, phases: [{ kind: 'orbit', t: [t0, t1] }] }; }
    else if (c.k === 'lateral') s = lateral({ vai, c: c.c, yaw: c.yaw, dist: c.dist, len: c.len, h: c.h, t0, t1, fov: c.fov ?? 30, hAt });
    else if (c.k === 'top') s = topDownRise({ vai, c: c.c, h0: c.h0, h1: c.h1, t0, t1, yaw0: c.yaw0 ?? 0, yaw1: c.yaw1 ?? 12, fov: c.fov ?? 40, hAt });
    else if (c.k === 'neo') s = neo({ vai, pose: c.pose, t0, t1, hAt, breathe: c.breathe ?? 0.12 });
    else throw new Error(`t3s ${o.shot}: cú máy "${c.k}" chưa hỗ trợ`);
    shots.push(s);
  }
  // nối bằng cắt: các mốc trùng thời điểm ở ranh cú → dời mốc đầu cú sau +1 ms (grammar cấm trùng)
  for (let i = 1; i < shots.length; i++) for (const k of shots[i].keys) if (Math.abs(k.t - shots[i].t[0]) < 1e-3) k.t = +(k.t + 0.002).toFixed(4);
  const G = grammar(shots, [], { cuts: true });
  // ---- lớp sống ----
  const recs = (TOWN ? TOWN.FP.list.flatMap((l) => l.recs) : []).concat(FP ? FP.list.flatMap((l) => l.recs) : []);
  const L0 = o.life || {};
  const fix = (w) => Object.assign({}, w, { pts: w.free === false || !recs.length ? line(w.line || w.pts) : freePath(line(w.line || w.pts), recs) });
  const LF = life({ seed: o.seed || 1704, walkers: (L0.walkers || []).map(fix), crowds: (L0.crowds || []).map(fix), birds: L0.birds, boats: L0.boats,
    chimney: L0.chimney && recs.length ? { at: chimneysFrom(recs, L0.chimney), drift: [-1.4, 0.4] } : undefined }, ctx); scene.add(LF.group);
  const TR = o.units && o.units.length ? units(o.units, ctx) : null; if (TR) scene.add(TR.group);
  const H = (h, m) => h + m / 60;
  const SM = o.smoke && o.smoke.length ? smoke(o.smoke.map((s) => Object.assign({}, s, { t: s.t || [0, 99] })), ctx) : null; if (SM) scene.add(SM.group);
  let FL = null; if (o.fleet) { const F = lineFormation(Object.assign({}, o.fleet)); FL = makeFleet(ctx.U, F.map((s) => Object.assign(s, { heading: o.fleet.heading ?? 0 }))); scene.add(FL.group); FL.group.traverse((m) => { if (m.isMesh) ctx.maskify(m.material, ctx.U, 1); }); }
  ctx.maskHide = [].concat(SM ? [SM.group] : [], LF.smokeGroup ? [LF.smokeGroup] : []);
  // ---- thời gian / mặt trời / bộ đếm ----
  const D = o.date || [Math.floor(o.year), 6, 15, 11, 11.5];   // [năm, tháng, ngày, giờ đầu, giờ cuối] — giờ địa phương mặt trời
  const hoursAt = (tt) => D[3] + (D[4] - D[3]) * tt / DUR;
  const smokeT = (tt) => (o.smokeClock ? hoursAt(tt) : tt);
  function state(tt) { const hh = hoursAt(tt), jd = jdLocal(D[0], D[1], D[2], hh, { julian: !!o.julian }), ph = G.phaseAt(tt);
    return { year: yearAt(tt), day: 0.5, cam: G.path.at(tt), spp: o.spp || 2, phase: ph.kind, preset: ph.shot ? ph.shot.preset : 'g1b', vai: ph.shot ? ph.shot.vai : 'co-che', hero: null, noi: o.noi || 'thanh_pho',
      hours: hh, clock: clockLabel(jd, { dual: !!o.dual, time: o.counter === 'clock' || o.counter === 'clockdual' }), sun: sunPos(jd), dayCycle: !!o.dayCycle }; }
  let troops = null, song = null;
  const cnt = BJ ? BJ.toa_dung.nam : null, atY = (arr, y) => { let v = arr[0][1]; for (const [Y, n] of arr) if (Y <= y) v = n; return v; }, MX = cnt ? Math.log10(Math.max(...cnt['0'].map((r) => r[1]), ...cnt['1'].map((r) => r[1]))) : 1;
  function apply(st, tt) { const T0 = tt ?? 0; if (LNsegs.length) { const k = Math.round(lineaFrac(T0) * lineaN); LNsegs.forEach((g, i) => { g.visible = i < k; }); }
    if (FR) FR.update(T0); if (AR) AR.update(T0); if (RIB) RIB.setValues(Math.log10(atY(cnt['0'], st.year)) / MX, Math.log10(atY(cnt['1'], st.year)) / MX, 0.55);
    if (TOWN) TOWN.update(st.year, ctx.cam); if (FP) FP.update(st.year, ctx.cam); if (FL) FL.update(st.hours); const z = SM ? (SM.update(smokeT(tt ?? 0)), SM.zones(smokeT(tt ?? 0))) : [];
    troops = TR ? TR.update(st.day, z, tt ?? 0) : null; song = LF.update(tt ?? 0, z); }
  function overlay(tt, st, T) {
    const ctr = o.counter === 'clock' || o.counter === 'clockdual' ? { s: st.clock.s, sub: o.counter === 'clockdual' ? st.clock.sub : undefined } : o.counter && typeof o.counter === 'object' ? (o.counter.at ? { s: o.counter.at.reduce((a, [t0, s]) => (tt >= t0 ? s : a), o.counter.at[0][1]) } : o.counter) : Math.floor(st.year);
    T.chrome(tt, ctr, o.pin && tt >= o.pin[0] && tt <= o.pin[1] ? 1 : 0, null, null, null);
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, yearAt, { hAt });
  const cuts = shots.slice(1).map((s) => +s.t[0].toFixed(3));
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: o.anchors || {},
    namKhung: (st) => Object.assign({}, TOWN ? TOWN.namMax(st.year) : {}, FP ? FP.namMax(st.year) : {}),
    meta: Object.assign({ shot: o.shot, cuts, cu: shots.map((s) => ({ preset: s.preset, vai: s.vai, t: s.t })), lop_nha: o.town || 'goi-theo-nam', nguon_lop: src, nguon: o.nguon || null, bac: o.bac || null,
      quan: TR ? TR.stat() : null, town: TOWN ? TOWN.stat() : null }, META, { nam: o.year, noi: [[0, 99, o.noi || 'thanh_pho']] }),
    troops: () => troops, song: () => song, smokeZones: () => (SM ? SM.zones(0) : []) };
}

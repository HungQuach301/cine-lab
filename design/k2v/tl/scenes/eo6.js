// V6 (lệnh P1 chủ dự án 18/10, phương án A): VÂY HÃM — giữ ≈ 29 000 quân (cỏ trống 34,1 % chấp nhận, KHÔNG trại Faden); MÁY CHÉO đưa PHỐ + LÍNEA + HÀO vào cùng khung;
//  quân = đội hình người thật (people.js); khói giả thể tích; ánh sáng V6. Bản gốc: eo1782.js (V5b-2d, giữ nguyên).
// ĐOẠN THỬ · CẢNH (e) — EO ĐẤT 13/9/1782 ~10:32 · VÂY HÃM (V5b-2d, lệnh C2-1 mục 1 chủ dự án 18/10; trước: V5b-2b-T AC1 + AD3, V5b-2c V0).
//  Chiến tuyến Tây Ban Nha theo nguồn: Línea de Contravalación + Fort San Felipe / Santa Bárbara (ghost SH do_tin cao/vừa, Drinkwater 1786, Línea RMS 4,2 m);
//  khẩu đội tiền phương số 15/17 + paralela + hào giao thông (ghost SH do_tin THẤP, ±160–380 m) CHỈ ở hậu cảnh xa, nhãn "approx."; vườn GARDENS của đồn trú trên
//  eo đất (Drinkwater 1786, số hoá V5b-2d, do_tin thấp) cùng hậu cảnh. KHỐI QUÂN kiểu bản đồ quân sự (đội hình hàng × cột, màu phe B6) sau Línea — số lượng,
//  cách xếp MINH HOẠ; cờ Cruz de Borgoña (cờ quân TBN 1506–1843) minh hoạ vị trí.
//  KHÓI PHÁO dọc tuyến: 10:25 "las flotantes, las baterías y esplanadas de tierra … rompieron á un tiempo el fuego" (Montero 1860, p. 360 — claim S067);
//  gió sáng "a gentle breeze from the north-west" (Drinkwater 1785, p. 295) → khói trôi về ĐÔNG-NAM (về phía Rock), ra xa khối quân (vùng khói chính xác, 'path').
//  Máy: thấp (22 m), sau tuyến phía bắc, nhìn chéo nam-đông-nam, ống kính dài (fov 26°): khối quân + Línea tiền cảnh, công sự tiền phương + khói trung/hậu cảnh,
//  vách bắc Rock + phố (Landport → King's Bastion) hậu cảnh — cỏ trống ≤ 1/3. Không người trong vùng khói (units/life nhận zones).
import { lateral, grammar, grammarLog } from '../campath.js';
import { town1782, units, frontLines, footprints, smoke } from '../layers.js';
import { life } from '../life.js';
import { flags, gardens } from '../props.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };   // V5b-2d (C2-9): vách bắc sắc hơn + đỉnh 412 m theo ảnh PD LoC 2025710362 (terrain.js)
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };   // V5b-2c (I5) giữ
export const GRADE = { vib: 0.78 };   // V6: S-curve + tách tông làm giảm bão hoà → vibrance 0,62 → 0,78 (đo lại: trung vị ≥ 0,40)
export const V6 = { sunK: 1.1, hemiK: 1.2, grade: [1.0, 0.35, 0.6] };
export const META = { cau: 'lateral-parallax', vai: 'co-che', noi: [[0, 99, 'eo_dat']], nam: 1782 };
export async function build(ctx) {
  const { terr, scene, THREE } = ctx, fps = 24, DUR = 4.0, hAt = (e, n) => Math.max(0, terr.hAt(e, n));
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx);
  const L = (await ctx.loadJSON(`${ctx.base}layers/lines1782.json`)).lines.find((l) => l.id === 'T1782-01');   // Línea (do_tin cao)
  const F = (await ctx.loadJSON(`${ctx.base}layers/fort1782.json`)).records.map((r) => r[6]).filter((ring) => ring.reduce((s, q) => s + q[1], 0) / ring.length > 800);   // 2 pháo đài TBN
  const cen = (r) => [r.reduce((s, q) => s + q[0], 0) / r.length, r.reduce((s, q) => s + q[1], 0) / r.length];
  const len = L.pts.slice(1).reduce((s, q, i) => s + Math.hypot(q[0] - L.pts[i][0], q[1] - L.pts[i][1]), 0);
  // KHỐI QUÂN (minh hoạ): 6 tuyến tiểu đoàn sau Línea (cách tường 32 … 192 m về bắc), mỗi khối 9 hàng × 30 người (≈ 27 × 12 m), cách 41 m dọc tuyến — TỔNG ≈ 29 000 người < ước tính quân vây 33 000 (Montero) – 40 000 (Drinkwater) (S065); số khối/cách xếp minh hoạ
  const U = [];
  for (let rk = 0; rk < 6; rk++) for (let s = 30 + rk * 15; s < 760; s += 41) U.push({ pts: L.pts, s, off: 32 + rk * 32, rows: 9, cols: 30, side: 'es', day: [0, 99], seed: 11 + rk * 40 + Math.round(s) });
  for (const r of F) { const [e, n] = cen(r); U.push({ at: [e - 12, n + 40], heading: 90, rows: 6, cols: 22, side: 'es', day: [0, 99], seed: 3 }, { at: [e + 14, n + 62], heading: 90, rows: 6, cols: 22, side: 'es', day: [0, 99], seed: 4 }); }
  const TR = units(U, ctx); scene.add(TR.group);
  // cờ: một cờ mỗi khối tuyến đầu (đứng trước khối), + trên hai pháo đài — gió NW → cờ bay về đông-nam (135°)
  const atLine = (s, off) => { let i = 1, acc = 0; for (; i < L.pts.length; i++) { const sl = Math.hypot(L.pts[i][0] - L.pts[i - 1][0], L.pts[i][1] - L.pts[i - 1][1]); if (acc + sl >= s) break; acc += sl; }
    const a = L.pts[i - 1], b = L.pts[Math.min(i, L.pts.length - 1)], d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1, u = (s - acc) / l; return [a[0] + d[0] * u - d[1] / l * off, a[1] + d[1] * u + d[0] / l * off]; };
  const FG = flags(U.filter((u) => u.pts && u.off === 32).map((u, i) => ({ at: atLine(u.s, 32 - 7), pole: 6.5, w: 2.4, kind: 'burgundy', toward: 135, phase: i * 0.7 }))
    .concat(F.map((r) => ({ at: cen(r), pole: 13, w: 4.8, kind: 'burgundy', toward: 135 }))), ctx); scene.add(FG.group);
  const mid = L.pts[Math.floor(L.pts.length / 2)];
  // CÔNG SỰ TIỀN PHƯƠNG 1782 (ghost SH do_tin thấp, ±160–380 m — SH §140: chỉ hậu cảnh kèm "approx.") — gờ đất + khẩu đội đất có pháo; khói khẩu đội số 15/17
  const TP = (await ctx.loadJSON(`${ctx.base}layers/lines1782_tp.json`)).lines;
  const FW = frontLines(TP.map((l) => ({ pts: l.pts, side: 'es', grow: [1700, 1701], w: 18, berm: 3.4, band: false, stone: '#c2aa7c', trench: 1 })), ctx);   // V6: gờ đất cát + rãnh hào tối scene.add(FW.group);
  const FT = await footprints([{ file: 'fort1782_tp', fort: true, h: 4.5, fortOpt: { embr: 6, garita: false, face: [0, -1], seed: 81 } }], ctx); scene.add(FT.group);
  // vườn GARDENS của đồn trú dưới vách bắc (Drinkwater 1786: ô luống + nhà vườn; do_tin thấp ±370 m, hậu cảnh) — KHÔNG cây (bản đồ không vẽ cây ở đây)
  const EX = await ctx.loadJSON(`${ctx.base}layers/extra1782.json`), GD = gardens(EX.features.filter((f) => f.vung === 'giua'), ctx, { seed: 23 }); scene.add(GD.group);
  // KHÓI PHÁO: (a) các bastion/khẩu đội của Línea (mỗi ~110 m, phía nam tường 16 m); (b) khẩu đội tiền phương 15/17 — trôi đông-nam theo gió NW
  const SMS = [];
  for (let s = 60; s < len - 40; s += 110) { const p = atLine(s, -16); SMS.push({ at: [p[0], 7, p[1]], t: [-1, 99], n: 18, size: 25, rise: 30, drift: [1.4, -2.2], period: 1.4 + 0.15 * (SMS.length % 4), seed: 300 + SMS.length, alpha: 0.95, zone: 'path' }); }
  const bat = TP.filter((l) => l.id === 'T1782-03' || l.id === 'T1782-04').flatMap((l) => [l.pts[0], l.pts[Math.floor(l.pts.length / 2)], l.pts[l.pts.length - 1]]);
  bat.forEach(([e, n], i) => SMS.push({ at: [e, 5, n - 10], t: [-1, 99], n: 12, size: 24, rise: 30, drift: [1.6, -2.4], period: 1.6 + 0.2 * (i % 3), seed: 340 + i, alpha: 0.8, zone: 'path' }));
  const SMK = smoke(SMS, ctx); scene.add(SMK.group); ctx.maskHide = [SMK.group];
  // máy: thấp 22 m, ≈ 230 m bắc Línea (đầu tây, gần Fort San Felipe), nhìn nam-đông-nam (phương vị ≈ 172°), trượt ngang 60 m (parallax khối quân ↔ Rock)
  // V6: ỐNG DÀI 15° (dọc) từ sau khối quân (≈ 140 m bắc hàng cuối, cao 32 m), nhìn nam-tây nam THẲNG VÀO PHỐ: nén eo đất thành các lớp — khối quân (người đọc được 15–25 px)
  //  → Línea + cờ → khẩu đội/paralela/hào (approx.) + khói → PHỐ (Moorish Castle, Line Wall, Old Mole) dưới chân Rock; trượt ngang 50 m. Chọn theo số đo mặt nạ
  //  (máy cao chéo đã thử: cỏ trống 40–46 %, nội dung 5–10 % → loại). Bản V5b-2d: máy thấp 22 m nhìn nam-đông nam (eo1782.js).
  const sh = ctx.opt.cam6 ? lateral(Object.assign({ vai: 'co-che', t0: 0, t1: DUR, hAt }, ctx.opt.cam6)) : lateral({ vai: 'co-che', c: [-430, -40, -950], yaw: 263.1, dist: 2303, len: 50, h: 32, t0: 0, t1: DUR, fov: 15, hAt });
  // lớp sống (F3, C2-7): người ĐƠN chỉ trong 150 m quanh máy (lính đi lại sau tuyến), hải âu, thuyền pháo TBN trong vịnh phía tây eo đất (minh hoạ)
  const LF = life({ seed: 1782, walkers: [{ pts: L.pts.map(([e, n]) => [e, n + 140]), n: 90, width: 18, near: 150, colors: ['#e8e2d2', '#d9d2c0', '#5b4a3a', '#c9b48a'] }],
    birds: { c: [-250, 1050], r: 160, h: 45, n: 12 }, boats: [{ pts: [[-760, 1150], [-900, 800], [-820, 450], [-700, 760]], len: 12, speed: 3.2, s0: 0.1 }, { pts: [[-650, 300], [-820, 650], [-980, 1050]], len: 10, speed: 2.6, s0: 0.5, sail: true }] }, ctx);
  scene.add(LF.group);
  const G = grammar([sh]), H0 = 10 + 30 / 60;
  function state(t) { const hh = H0 + t * (1 / 60), jd = jdLocal(1782, 9, 13, hh); return { year: 1782.7, day: 0.5, cam: G.path.at(t), spp: 2, phase: G.phaseAt(t).kind, preset: 'lateral-parallax', vai: 'co-che', hero: null, noi: 'eo_dat', hours: hh, clock: clockLabel(jd), sun: sunPos(jd) }; }
  let troops = null, song = null;
  function apply(st, t) { TOWN.update(st.year, ctx.cam); FW.update(st.year); SMK.update(t ?? 0); const z = SMK.zones(t ?? 0); troops = TR.update(st.day, z); song = LF.update(t ?? 0, z); FG.update(t ?? 0); GD.update(ctx.cam); }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  function overlay(t, st, T, proj) {
    T.chrome(t, { s: st.clock.s }, 0, null, { lines: [{ s: 'Works, gardens: approx. · ~29,000 troops, uniforms, flags: illustrative', a: Math.max(0, Math.min(1, t / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Isthmus of Gibraltar');
    T.ghostSrc(t, [-1, DUR + 1], 'Lines: reconstructed from J. Drinkwater, Plan of the Batteries, 1782');
    T.card(t, [0.4, DUR + 0.5], 'Spanish lines open fire, 10:25', 'Línea de Contravalación · Montero 1860', proj(V([mid[0], 6, mid[1]])));
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt });
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: { linea: [mid[0], 6, mid[1]] }, namKhung: (st) => TOWN.namMax(st.year), smokeZones: () => SMK.zones(0),
    meta: Object.assign({ quan: TR.stat(), co: FG.n, khoi: SMS.length, vuon: GD.stat, town: TOWN.stat(), doPx: { khoi: [27, 12], quan: U.map((u) => { const p = u.pts ? atLine(u.s, u.off) : u.at; return [p[0], hAt(p[0], p[1]), p[1]]; }) } }, META), troops: () => troops, song: () => song };
}

// ĐOẠN THỬ V5b-2b-T · CẢNH (c) — EO ĐẤT 13/9/1782 (lệnh AC1 + AD3 chủ dự án 17/10): Línea de Contravalación + Fort San Felipe / Santa Bárbara (ghost SH, Drinkwater 1786,
//  Línea RMS 4,2 m) + KHỐI QUÂN instanced (M2 rút gọn) đứng sau tường chắn phía bắc tuyến — vị trí dọc tuyến đã nắn, SỐ LƯỢNG và CÁCH XẾP là MINH HOẠ (ghi trên hình);
//  inset Tây Âu (đường bờ Natural Earth) chấm Gibraltar + tuyến đoàn tiếp tế từ Anh (SƠ ĐỒ, ba đoàn 1780–82 — claims S054–S056); vai "cơ chế" (lateral chậm).
//  Không khói ở cảnh này (không có nguồn vị trí khẩu đội trên bộ đủ tin — dải tiền phương do_tin thấp không dùng); không người trong khói (layers.units tự kiểm).
import { lateral, grammar, grammarLog } from '../campath.js';
import { town1782, units, frontLines, footprints, smoke } from '../layers.js';
import { life } from '../life.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export const TERRAIN = { cliff: true };
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.42, 0.62, 0.92], fogC: [0.46, 0.65, 0.91] };   // trời Địa Trung Hải sáng tháng 9: chân trời xanh hơn (S 0,33 → 0,46)   // V5b-2c (I5): bóng đổ bớt xám-lam, ánh dội đất ấm (0,74: không cháy sáng)
export const GRADE = { vib: 0.62 };   // V5b-2c (I5): vibrance 0,35 → 0,62 (vữa/đá nhạt lên màu; màu đã đậm gần như giữ)
export const META = { cau: 'lateral-parallax', vai: 'co-che', noi: [[0, 99, 'eo_dat']], nam: 1782 };
export async function build(ctx) {
  const { terr, scene, THREE } = ctx, fps = 24, DUR = 4.0, hAt = (e, n) => Math.max(0, terr.hAt(e, n));
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx);
  const L = (await ctx.loadJSON(`${ctx.base}layers/lines1782.json`)).lines.find((l) => l.id === 'T1782-01');   // Línea (do_tin cao)
  const F = (await ctx.loadJSON(`${ctx.base}layers/fort1782.json`)).records.map((r) => r[6]).filter((ring) => ring.reduce((s, q) => s + q[1], 0) / ring.length > 800);   // 2 pháo đài TBN (bắc eo đất)
  const cen = (r) => [r.reduce((s, q) => s + q[0], 0) / r.length, r.reduce((s, q) => s + q[1], 0) / r.length];
  const len = L.pts.slice(1).reduce((s, q, i) => s + Math.hypot(q[0] - L.pts[i][0], q[1] - L.pts[i][1]), 0);
  const U = [];
  for (let k = 0; k < 9; k++) U.push({ pts: L.pts, s: 160 + k * (len - 320) / 8, off: 34, rows: 6, cols: 30, side: 'es', day: [0, 99], seed: 11 + k });
  for (const r of F) { const [e, n] = cen(r); U.push({ at: [e - 12, n + 8], heading: 90, rows: 4, cols: 18, side: 'es', day: [0, 99], seed: 3 }, { at: [e + 14, n - 6], heading: 90, rows: 4, cols: 18, side: 'es', day: [0, 99], seed: 4 }); }
  const TR = units(U, ctx); scene.add(TR.group);
  const mid = L.pts[Math.floor(L.pts.length / 2)];
  // V5b-2c (V0 c, I3): máy hạ thấp + sát tuyến (≈ 150 m bắc Línea, cao 32 m): khối quân cao ≥ 6 px ở 1080p, Línea + quân tiền cảnh, vách bắc Rock (đã làm sắc) hậu cảnh
  // V5b-2c: CÔNG SỰ TIỀN PHƯƠNG 1782 (ghost SH do_tin thấp, sai số ≥ 160 m — SH §140 cho dùng ở hậu cảnh kèm "approx.") — hào/khẩu đội đất + 4 đồn nhỏ; khói khẩu đội
  //  số 15/17 (T1782-03/04) — vị trí ±160 m, ghi trên hình "Forward works & smoke: approx."
  const TP = (await ctx.loadJSON(`${ctx.base}layers/lines1782_tp.json`)).lines;
  const FW = frontLines(TP.map((l) => ({ pts: l.pts, side: 'es', grow: [1700, 1701], w: 13, berm: 2.6, band: false })), ctx); scene.add(FW.group);
  const FT = await footprints([{ file: 'fort1782_tp', fort: true, h: 4.5, fortOpt: { embr: 7, gunEvery: 2, garita: false, face: [0, -1], seed: 81 } }], ctx); scene.add(FT.group);
  const bat = TP.filter((l) => l.id === 'T1782-03' || l.id === 'T1782-04').flatMap((l) => [l.pts[0], l.pts[Math.floor(l.pts.length / 2)], l.pts[l.pts.length - 1]]);
  const SMK = smoke(bat.map(([e, n], i) => ({ at: [e, 6, n], t: [-1, 99], n: 12, size: 26, rise: 14, drift: [-2.5, 0.6], period: 1.6 + 0.2 * (i % 3), seed: 300 + i, alpha: 0.7 })), ctx); scene.add(SMK.group); ctx.maskHide = [SMK.group];
  // máy: từ đông-bắc tuyến (cao 70 m) nhìn tây-nam DỌC Línea — tuyến + khối quân chéo khung (mặt đông được nắng 10:32), công sự tiền phương + vách bắc Rock bên trái, vịnh + Algeciras phải
  const sh = lateral({ vai: 'co-che', c: [180, 120, -250], yaw: -90, dist: 1370, len: 90, h: 30, t0: 0, t1: DUR, fov: 36, hAt });   // từ bắc Línea (≈ 170 m) nhìn nam: Línea + khối quân tiền cảnh, công sự tiền phương + khói trung cảnh, vách bắc Rock hậu cảnh (góc 'Gibraltar từ chiến tuyến TBN')
  // lớp sống (F3): lính TBN đi lại sau tuyến (áo trắng bộ binh TBN thế kỷ 18 — minh hoạ), hải âu, thuyền pháo TBN trong vịnh phía tây eo đất (minh hoạ)
  const LF = life({ seed: 1782, walkers: [{ pts: L.pts.map(([e, n]) => [e, n + 40]), n: 70, width: 14, colors: ['#e8e2d2', '#d9d2c0', '#5b4a3a', '#c9b48a'] }],
    birds: { c: [150, 650], r: 160, h: 55, n: 12 }, boats: [{ pts: [[-760, 1150], [-900, 800], [-820, 450], [-700, 760]], len: 12, speed: 3.2, s0: 0.1 }, { pts: [[-650, 300], [-820, 650], [-980, 1050]], len: 10, speed: 2.6, s0: 0.5, sail: true }] }, ctx);
  scene.add(LF.group);   // từ phía bắc tuyến nhìn thẳng nam (góc 'Gibraltar từ chiến tuyến TBN'): khối quân + Línea tiền cảnh, vách bắc Rock hậu cảnh
  const G = grammar([sh]), H0 = 10 + 30 / 60;
  function state(t) { const hh = H0 + t * (1 / 60), jd = jdLocal(1782, 9, 13, hh); return { year: 1782.7, day: 0.5, cam: G.path.at(t), spp: 2, phase: G.phaseAt(t).kind, preset: 'lateral-parallax', vai: 'co-che', hero: null, noi: 'eo_dat', hours: hh, clock: clockLabel(jd), sun: sunPos(jd) }; }
  let troops = null;
  let song = null;
  function apply(st, t) { TOWN.update(st.year, ctx.cam); troops = TR.update(st.day, []); FW.update(st.year); song = LF.update(t ?? 0, SMK.zones(t ?? 0)); SMK.update(t ?? 0); }   // cảnh này không có khói (vùng khói rỗng)
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  function overlay(t, st, T, proj) {
    T.chrome(t, { s: st.clock.s }, 0, null, { lines: [{ s: 'Forward works: approx. · troops, boats: illustrative', a: Math.max(0, Math.min(1, t / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Isthmus of Gibraltar');
    T.ghostSrc(t, [-1, DUR + 1], 'Lines: reconstructed from J. Drinkwater, Plan of the Batteries, 1782');
    T.card(t, [0.4, DUR + 0.5], 'Spanish lines, built 1730–35', 'Línea de Contravalación', proj(V([mid[0], 6, mid[1]])));
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt });
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: { linea: [mid[0], 6, mid[1]] }, namKhung: (st) => TOWN.namMax(st.year),
    meta: Object.assign({ quan: TR.stat() }, META), troops: () => troops, song: () => song };
}

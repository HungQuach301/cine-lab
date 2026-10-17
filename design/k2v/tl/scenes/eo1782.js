// ĐOẠN THỬ V5b-2b-T · CẢNH (c) — EO ĐẤT 13/9/1782 (lệnh AC1 + AD3 chủ dự án 17/10): Línea de Contravalación + Fort San Felipe / Santa Bárbara (ghost SH, Drinkwater 1786,
//  Línea RMS 4,2 m) + KHỐI QUÂN instanced (M2 rút gọn) đứng sau tường chắn phía bắc tuyến — vị trí dọc tuyến đã nắn, SỐ LƯỢNG và CÁCH XẾP là MINH HOẠ (ghi trên hình);
//  inset Tây Âu (đường bờ Natural Earth) chấm Gibraltar + tuyến đoàn tiếp tế từ Anh (SƠ ĐỒ, ba đoàn 1780–82 — claims S054–S056); vai "cơ chế" (lateral chậm).
//  Không khói ở cảnh này (không có nguồn vị trí khẩu đội trên bộ đủ tin — dải tiền phương do_tin thấp không dùng); không người trong khói (layers.units tự kiểm).
import { lateral, grammar, grammarLog } from '../campath.js';
import { town1782, units } from '../layers.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

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
  for (let k = 0; k < 9; k++) U.push({ pts: L.pts, s: 160 + k * (len - 320) / 8, off: 24, rows: 4, cols: 30, side: 'es', day: [0, 99], seed: 11 + k });
  for (const r of F) { const [e, n] = cen(r); U.push({ at: [e - 12, n + 8], heading: 90, rows: 4, cols: 18, side: 'es', day: [0, 99], seed: 3 }, { at: [e + 14, n - 6], heading: 90, rows: 4, cols: 18, side: 'es', day: [0, 99], seed: 4 }); }
  const TR = units(U, ctx); scene.add(TR.group);
  const mid = L.pts[Math.floor(L.pts.length / 2)];
  const sh = lateral({ vai: 'co-che', c: [250, 60, 300], yaw: -90, dist: 1150, len: 110, h: 110, t0: 0, t1: DUR, fov: 34, hAt });   // từ phía bắc tuyến nhìn thẳng nam (góc 'Gibraltar từ chiến tuyến TBN'): khối quân + Línea tiền cảnh, vách bắc Rock hậu cảnh
  const G = grammar([sh]), H0 = 10 + 30 / 60;
  function state(t) { const hh = H0 + t * (1 / 60), jd = jdLocal(1782, 9, 13, hh); return { year: 1782.7, day: 0.5, cam: G.path.at(t), spp: 2, phase: G.phaseAt(t).kind, preset: 'lateral-parallax', vai: 'co-che', hero: null, noi: 'eo_dat', hours: hh, clock: clockLabel(jd), sun: sunPos(jd) }; }
  let troops = null;
  function apply(st) { TOWN.update(st.year, ctx.cam); troops = TR.update(st.day, []); }   // cảnh này không có khói (vùng khói rỗng)
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  function overlay(t, st, T, proj) {
    T.chrome(t, { s: st.clock.s }, 0, null, { lines: [{ s: 'Troop blocks: illustrative', a: Math.max(0, Math.min(1, t / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Isthmus of Gibraltar');
    T.ghostSrc(t, [-1, DUR + 1], 'Lines: reconstructed from J. Drinkwater, Plan of the Batteries, 1782');
    T.card(t, [0.4, DUR + 0.5], 'Spanish lines, built 1730–35', 'Línea de Contravalación', proj(V([mid[0], 6, mid[1]])));
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt });
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: { linea: [mid[0], 6, mid[1]] }, namKhung: (st) => TOWN.namMax(st.year),
    meta: Object.assign({ quan: TR.stat() }, META), troops: () => troops };
}

// ĐOẠN THỬ V5b-2b-T · CẢNH (b) — 3D PHỐ GIBRALTAR 1782 CÓ NHÀ (lệnh AE 17/10: ghost 1782 thật của phiên SH, KHÔNG dùng phố 2026 thay).
// Phố: 22 khối phố + 13 toà của Drinkwater 1786 "Plan of the Batteries … 13 Sept 1782" (RMS phố 21 m, LOO 33 m), 2 tầng chuẩn mốc (bản đồ ghi "RUINS" → cận dưới);
// bastion/Line Wall theo cùng bản đồ; nửa đông phố cổ bản đồ không vẽ viền → trống (không bịa). Máy: bay thấp ≈ 70 m dọc tim Main Street (OSM; phố Calle Real cũ,
// cùng trục trên bản đồ 1782), nhìn trước-xuống, lệch về phía tây (phần có dữ liệu) — vai "hệ quả" (phố sau đợt pháo 4/1781). Mặt trời: sáng 13/9/1782 (M6).
import { alongLine, grammar, grammarLog, ALT_MAX } from '../campath.js';
import { town1782, units } from '../layers.js';
import { jdLocal, sunPos } from '../sun.js';
import { life, chimneysFrom, freePath } from '../life.js';

export const TERRAIN = { cliff: true };
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };   // trời Địa Trung Hải sáng tháng 9: chân trời xanh hơn (S 0,33 → 0,46)   // V5b-2c (I5): bóng đổ bớt xám-lam, ánh dội đất ấm (0,74: không cháy sáng)
export const GRADE = { vib: 0.62 };   // V5b-2c (I5): vibrance 0,35 → 0,62 (vữa/đá nhạt lên màu; màu đã đậm gần như giữ)
export const META = { cau: 'fly-pho', vai: 'he-qua', noi: [[0, 99, 'thanh_pho']], nam: 1782, ghost: 'ghost-1782 (SH @ 54185b3)' };
const MAIN = [[-409, -1811], [-410, -1700], [-425, -1620], [-435, -1571], [-441, -1543], [-448, -1521], [-450, -1505], [-447, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880], [-417, -788]];
export async function build(ctx) {
  const { terr } = ctx, fps = 24, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), DUR = 8.0, H = 70;
  if (H > ALT_MAX.pho) throw new Error('bay phố > ALT_MAX.pho');
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx);
  // dọc tim tuyến, nhìn trước 230 m và lệch 45 m về phía tây (vịnh) để khung là phần phố bản đồ có vẽ
  // V5b-2c (I3): phố đã lấp ước tính cả mé đông → nhìn trước-xuống dốc hơn, lệch nhẹ về ĐÔNG (phố dày chiếm ≥ 50 % khung, mặt nước ≤ 1/3)
  const K = alongLine(MAIN, { s0: 160, s1: 620, t0: 0, t1: DUR, h: [H, H - 4], look: 200, dip: 64, dt: 0.25, hAt }).map((k) => Object.assign(k, { fov: 42, l: [k.l[0] + 35, k.l[1], k.l[2]] }));
  // LỚP SỐNG (F3): người đi dọc Main Street (lính áo đỏ đồn trú + dân — minh hoạ), hải âu, khói bếp
  const recs = TOWN.FP.list.flatMap((l) => (l.kind === 'ghost' ? l.recs : []));
  const LF = life({ seed: 1786, walkers: [{ pts: freePath(MAIN, TOWN.FP.list.flatMap((l) => l.recs)), n: 90, width: 3, colors: ['#b03a2e', '#a8402e', '#e7e0cf', '#5e4a38', '#3d4a5a'] }], birds: { c: [-430, -1300], r: 170, h: 70, n: 14 },
    chimney: { at: chimneysFrom(recs, 24), drift: [-1.4, 0.4] } }, ctx); ctx.scene.add(LF.group);
  const GP = [-505, -1165], TR = units([[-22, -14], [14, -14], [-22, 12], [14, 12]].map(([de, dn], i) => ({ at: [GP[0] + de, GP[1] + dn], heading: 270, rows: 6, cols: 26, side: 'gb', day: [0, 99], seed: 21 + i })), ctx); ctx.scene.add(TR.group);   // đồn trú trên Grand Parade (minh hoạ) ctx.maskHide = LF.smokeGroup ? [LF.smokeGroup] : [];
  const shot = { preset: 'fly-pho', vai: 'he-qua', t: [0, DUR], keys: K, phases: [{ kind: 'fly', t: [0, DUR] }], route: { line: MAIN, type: 'pho', nguon: 'OSM Main Street ways 172387187 + 250867611' } };
  const G = grammar([shot]), path = G.path, sun = sunPos(jdLocal(1782, 9, 13, 10.6));
  function state(t) { const ph = G.phaseAt(t); return { year: 1782.7, cam: path.at(t), spp: 2, phase: ph.kind, preset: 'fly-pho', vai: 'he-qua', hero: null, noi: 'thanh_pho', sun }; }
  let song = null;
  function apply(st, t) { TOWN.update(st.year, ctx.cam); song = LF.update(t ?? 0, []); TR.update(0.5, []); }
  function overlay(t, st, T) {
    T.chrome(t, 1782, 0, null, { lines: [{ s: 'Houses: 2-storey standard for 1782 (estimated)', a: Math.max(0, Math.min(1, (t - 0.3) / 0.35, (5.6 - t) / 0.35)) }, { s: TOWN.INFILL_SRC + ' · people: illustrative', a: Math.max(0, Math.min(1, (t - 0.3) / 0.35, (DUR + 1 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Main Street, Gibraltar');
    T.ghostSrc(t, [-1, DUR + 1], TOWN.src);
    T.card(t, [1.4, 5.4], 'Main Street, 1782 · blocks from the siege plan', 'Positions within ~21 m · east side not on the plan: estimated', null);
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt, line: MAIN });
  return { N, fps, state, apply, overlay, path, grammarLog: glog, camLog: glog, anchors: { main_street: [-445, 20, -1400] }, namKhung: (st) => TOWN.namMax(st.year), meta: META, song: () => song };
}

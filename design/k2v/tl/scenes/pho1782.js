// ĐOẠN THỬ V5b-2b-T · CẢNH (b) — 3D PHỐ GIBRALTAR 1782 CÓ NHÀ (lệnh AE 17/10: ghost 1782 thật của phiên SH, KHÔNG dùng phố 2026 thay).
// Phố: 22 khối phố + 13 toà của Drinkwater 1786 "Plan of the Batteries … 13 Sept 1782" (RMS phố 21 m, LOO 33 m), 2 tầng chuẩn mốc (bản đồ ghi "RUINS" → cận dưới);
// bastion/Line Wall theo cùng bản đồ; nửa đông phố cổ bản đồ không vẽ viền → trống (không bịa). Máy: bay thấp ≈ 70 m dọc tim Main Street (OSM; phố Calle Real cũ,
// cùng trục trên bản đồ 1782), nhìn trước-xuống, lệch về phía tây (phần có dữ liệu) — vai "hệ quả" (phố sau đợt pháo 4/1781). Mặt trời: sáng 13/9/1782 (M6).
import { alongLine, grammar, grammarLog, ALT_MAX } from '../campath.js';
import { town1782 } from '../layers.js';
import { jdLocal, sunPos } from '../sun.js';

export const META = { cau: 'fly-pho', vai: 'he-qua', noi: [[0, 99, 'thanh_pho']], nam: 1782, ghost: 'ghost-1782 (SH @ 54185b3)' };
const MAIN = [[-409, -1811], [-410, -1700], [-425, -1620], [-435, -1571], [-441, -1543], [-448, -1521], [-450, -1505], [-447, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880], [-417, -788]];
export async function build(ctx) {
  const { terr } = ctx, fps = 24, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), DUR = 8.0, H = 70;
  if (H > ALT_MAX.pho) throw new Error('bay phố > ALT_MAX.pho');
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx);
  // dọc tim tuyến, nhìn trước 230 m và lệch 45 m về phía tây (vịnh) để khung là phần phố bản đồ có vẽ
  const K = alongLine(MAIN, { s0: 160, s1: 620, t0: 0, t1: DUR, h: [H, H - 4], look: 230, dip: 50, dt: 0.25, hAt }).map((k) => Object.assign(k, { fov: 40, l: [k.l[0] - 45, k.l[1], k.l[2]] }));
  const shot = { preset: 'fly-pho', vai: 'he-qua', t: [0, DUR], keys: K, phases: [{ kind: 'fly', t: [0, DUR] }], route: { line: MAIN, type: 'pho', nguon: 'OSM Main Street ways 172387187 + 250867611' } };
  const G = grammar([shot]), path = G.path, sun = sunPos(jdLocal(1782, 9, 13, 10.6));
  function state(t) { const ph = G.phaseAt(t); return { year: 1782.7, cam: path.at(t), spp: 2, phase: ph.kind, preset: 'fly-pho', vai: 'he-qua', hero: null, noi: 'thanh_pho', sun }; }
  function apply(st) { TOWN.update(st.year, ctx.cam); }
  function overlay(t, st, T) {
    T.chrome(t, 1782, 0, null, { lines: [{ s: 'Houses: 2-storey standard for 1782 (estimated)', a: Math.max(0, Math.min(1, (t - 0.3) / 0.35, (5.6 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Main Street, Gibraltar');
    T.ghostSrc(t, [-1, DUR + 1], TOWN.src);
    T.card(t, [1.4, 5.4], 'Main Street, 1782 · blocks from the siege plan', 'Positions within ~21 m · east side not drawn on the plan', null);
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt, line: MAIN });
  return { N, fps, state, apply, overlay, path, grammarLog: glog, camLog: glog, anchors: { main_street: [-445, 20, -1400] }, namKhung: (st) => TOWN.namMax(st.year), meta: META };
}

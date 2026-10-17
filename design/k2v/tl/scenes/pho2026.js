// ĐOẠN THỬ V5b-2b-T · CẢNH (b) — 3D PHỐ GIBRALTAR CÓ NHÀ. Lệnh: phố 1782 bằng ghost của phiên SH (channel-k2/k2c-t3-01/ghost/1782/*.geojson, nhánh sh-ghost);
// nhánh đó CHƯA có khi dựng (git fetch origin sh-ghost: không có ref, 17/10) → dựng bằng PHỐ 2026 (OSM, nhà thật, chiều cao ước từ DSM — gói cảnh V5b-1),
// ghi rõ TRÊN HÌNH (dòng phương pháp) và trong báo cáo; KHÔNG tự vẽ ghost (việc của SH). Khi có ghost: đổi opt.layers = [{file: 'ghost1782', …}] + năm 1782.
// Máy: bay thấp ≈ 70 m dọc tim Main Street (OSM ways 172387187 + 250867611, lệch tim ≤ 15 m, HH2 phố ≤ 120 m), nhìn trước-xuống — vai "hệ quả".
import { alongLine, grammar, grammarLog, ALT_MAX } from '../campath.js';

export const META = { cau: 'fly-pho', vai: 'he-qua', noi: [[0, 99, 'thanh_pho']], nam: 2026, ghost: false, ly_do: 'sh-ghost chưa có ghost 1782 khi dựng' };
// tim Main Street (ENU m, từ OSM — đo trong phiên: đầu nam (−409, −1811) → bắc (−417, −788))
const MAIN = [[-409, -1811], [-410, -1700], [-425, -1620], [-435, -1571], [-441, -1543], [-448, -1521], [-450, -1505], [-447, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880], [-417, -788]];
export async function build(ctx) {
  const { terr } = ctx, fps = 24, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), DUR = 8.0, H = 70;
  if (H > ALT_MAX.pho) throw new Error('bay phố > ALT_MAX.pho');
  const K = alongLine(MAIN, { s0: 180, s1: 640, t0: 0, t1: DUR, h: [H, H - 4], look: 230, dip: 52, dt: 0.25, hAt }).map((k) => Object.assign(k, { fov: 40 }));
  const shot = { preset: 'fly-pho', vai: 'he-qua', t: [0, DUR], keys: K, phases: [{ kind: 'fly', t: [0, DUR] }], route: { line: MAIN, type: 'pho', nguon: 'OSM Main Street ways 172387187 + 250867611' } };
  const G = grammar([shot]), path = G.path;
  function state(t) { const ph = G.phaseAt(t); return { year: 2026, cam: path.at(t), spp: 2, phase: ph.kind, preset: 'fly-pho', vai: 'he-qua', hero: null, noi: 'thanh_pho' }; }
  function overlay(t, st, T) {
    T.chrome(t, 2026, 0, null, { lines: [{ s: 'Shown: Gibraltar today · 1782 street plan not yet digitised', a: Math.max(0, Math.min(1, t / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Main Street, Gibraltar');
    T.card(t, [1.2, 5.2], 'Main Street · every building drawn from map data', 'Map data from OpenStreetMap (ODbL)', null);
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 2026, { hAt, line: MAIN });
  return { N, fps, state, overlay, path, grammarLog: glog, camLog: glog, anchors: { main_street: [-445, 20, -1400] }, namKhung: () => ({ osm_2026: 2026 }), meta: META };
}

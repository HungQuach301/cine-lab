// V5b-2a · CUỘN MINH HOẠ 6 PRESET ngữ pháp máy (KK1) trên gói cảnh Gibraltar — mỗi cú 4,5 s, nối bằng CẮT; KHÔNG phải phim (không thẻ dữ kiện).
// Mỗi cú khai vai (cơ chế / bước ngoặt / hệ quả), năm chạy ≤ 10 năm/s, tốc độ góc ≤ 90 °/s; log: render.js --campath (grammarLog).
//  1 push-in giữ hơi → Tower of Homage · 2 boundary trace dọc biên giới OSM (hai bên tô theo số toà đang đứng) · 3 follow-object xe A-lite trên WCA 1941
//  4 lateral parallax trước La Línea · 5 top-down rise trên giao lộ đường băng (1937 → 1945: đường băng xuất hiện) · 6 vertigo (dolly zoom) quanh tháp
import { pushIn, boundaryTrace, follow, lateral, topDownRise, vertigo, grammar, grammarLog, lineLen } from '../campath.js';
import { boundaryRibbons, makeMover } from '../overlay3d.js';
import { ease } from '../core.js';
export async function build(ctx) {
  const { THREE, terr, heroes, lines, track, scene, maskify, U } = ctx, fps = 24, hAt = terr.hAt, D = 4.5;
  const bins = new Map(); for (const [e, n] of lines.wca) { const k = Math.round(n / 20); if (!bins.has(k)) bins.set(k, []); bins.get(k).push(e); }
  const WCA = [...bins.entries()].sort((a, b) => a[0] - b[0]).map(([k, es]) => [es.reduce((s, v) => s + v, 0) / es.length, k * 20]);
  const BORDER = lines.border, BJ = await (await fetch(ctx.base + 'border.json')).json();
  const TW = heroes.towerC, TT = [TW[0], heroes.towerTop.y, TW[1]], LL = [320, 15, 1650];
  const T = (i) => [i * D, i * D + D - 1 / fps];
  const mover = makeMover(WCA, hAt, { kind: 'car', color: 0x5a2a24 }); scene.add(mover.group); mover.group.traverse((o) => o.isMesh && maskify(o.material, U, 1));
  const shots = [
    pushIn({ vai: 'co-che', from: [TW[0] - 430, 230, TW[1] - 380], to: [TW[0] - 150, 105, TW[1] - 130], look: TT, t0: T(0)[0], t1: T(0)[1], hold: 1.3, fov: 34, fov1: 30 }),
    boundaryTrace({ vai: 'he-qua', line: BORDER, type: 'eo_dat', nguon: BJ.nguon, s0: 40, s1: lineLen(BORDER) - 40, t0: T(1)[0], t1: T(1)[1], h: 95, look: 320, dip: 95, fov: 44, hAt }),
    follow({ vai: 'co-che', objAt: (t) => mover.at(300 - 11 * (t - T(2)[0]), -1, -2.4), t0: T(2)[0], t1: T(2)[1], back: 26, up: 11, side: 6, lookAhead: 30, fov: 40 }),
    lateral({ vai: 'he-qua', c: [LL[0] - 150, 10, LL[2] - 500], yaw: 72, dist: 720, len: 420, h: 110, t0: T(3)[0], t1: T(3)[1], fov: 30, hAt }),
    topDownRise({ vai: 'buoc-ngoat', c: [0, 0, 0], h0: 260, h1: 1300, t0: T(4)[0], t1: T(4)[1], yaw0: 0, yaw1: 18, fov: 42, hAt }),
    vertigo({ vai: 'buoc-ngoat', c: [TW[0], 14, TW[1]], yaw: 35, pitch: 14, d0: 230, d1: 560, w: 85, t0: T(5)[0], t1: T(5)[1], hAt }),
  ];
  const rib = boundaryRibbons(BORDER, hAt, U); scene.add(rib.group);
  const G = grammar(shots, [], { cuts: true }), path = G.path, N = Math.round(6 * D * fps);
  const year = track([[0, 1883], [T(0)[1], 1900], [T(1)[0], 1960], [T(1)[1], 2004], [T(2)[0], 1941.2], [T(2)[1], 1942.4], [T(3)[0], 1990], [T(3)[1], 2026], [T(4)[0], 1937], [T(4)[1], 1945], [T(5)[0], 1980], [T(5)[1], 2020]]);
  const cnt = BJ.toa_dung.nam, at = (arr, y) => { let v = arr[0][1]; for (const [Y, n] of arr) if (Y <= y) v = n; return v; }, MX = Math.log10(Math.max(...cnt['0'].map((r) => r[1]), ...cnt['1'].map((r) => r[1])));
  function state(t) { const ph = G.phaseAt(t); return { year: year(t), cam: path.at(t), spp: G.sppAt(t), phase: ph.kind, preset: ph.shot && ph.shot.preset, vai: ph.shot && ph.shot.vai, hero: ph.shot && ph.shot.preset === 'push-in' ? 'tower' : null, dim: 0, pin: 0, pinZoom: 0 }; }
  function apply(st, t) {
    heroes.update(st.year); heroes.hi.runway.value = 0; heroes.rwFrame.visible = false; heroes.hi.tower.value = st.preset === 'push-in' || st.preset === 'vertigo' ? 0.5 : 0; heroes.towerHull.visible = false;
    if (st.preset === 'follow-object') mover.place(mover.at(300 - 11 * (t - T(2)[0]), -1, -2.4)); else mover.group.visible = false;
    if (st.preset === 'boundary-trace') { const k = ease((t - T(1)[0]) / 0.4) * ease((T(1)[1] - t) / 0.4); rib.setValues(Math.log10(at(cnt['0'], st.year)) / MX, Math.log10(at(cnt['1'], st.year)) / MX, 0.55 * k); } else rib.setValues(0, 0, 0);
  }
  function overlay(t, st, Tx) {
    const idx = st.preset === 'boundary-trace' ? `La Línea ${at(cnt['0'], st.year).toLocaleString('en-US')} · Gibraltar ${at(cnt['1'], st.year).toLocaleString('en-US')} buildings` : null;
    Tx.chrome(t, st.year, 0, idx, { lines: [{ s: `preset ${st.preset} · vai ${st.vai}`, a: 1 }] });
  }
  const glog = () => grammarLog(G, N, fps, year, { hAt });
  return { N, fps, state, apply, overlay, path, year, grammarLog: glog, camLog: glog, cues: {} };
}

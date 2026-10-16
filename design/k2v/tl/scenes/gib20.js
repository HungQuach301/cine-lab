// ĐOẠN THỬ V5b-1 · GIBRALTAR ↔ LA LÍNEA (1704 → 2026). Dữ kiện trên hình lấy từ channel-k2/k2c-t3-01/tienky/claims.json (C17, C33)
// + nguồn tra trong phiên (Census of Gibraltar 2022 Bảng 1; Ministry for Heritage; HMGoG 199/2018). Ngôn ngữ hình (chủ dự án 16/10):
//  S1 0–3,2 mở toàn cảnh (glide) · S2 3,2–7,4 glide → zoom-in Tower of Homage (×≥ 5)
//  · V5b-2a: 7,8–22,8 MỘT CÚ LIÊN HOÀN (campath.js lienHoan, vai "bước ngoặt"): bay thấp ≈ 100 m dọc Winston Churchill Ave (OSM, ≤ 15 m) + ảnh LoC neo
//    → speed ramp → orbit 5 s quanh giao lộ đường băng (MỐC ĐINH 1941 năm dừng 12,4–14,2 s, phóng 1,45×) → crane up → rise-and-reveal La Línea + vịnh
//  · màn kết 22,8–24,5 (24,5 s: năm ≤ 10 năm/s trong cú liên hoàn).
import { lienHoan, grammar, grammarLog, lineLen } from '../campath.js';
import { ease } from '../core.js';
export async function build(ctx) {
  const { THREE, M, terr, heroes, lines, track } = ctx, fps = 24, hAt = terr.hAt;
  // tim tuyến Winston Churchill Ave: gộp hai chiều xe (gom theo N mỗi 20 m, lấy trung bình E)
  const raw = lines.wca, bins = new Map(); for (const [e, n] of raw) { const k = Math.round(n / 20); if (!bins.has(k)) bins.set(k, []); bins.get(k).push(e); }
  const WCA = [...bins.entries()].sort((a, b) => a[0] - b[0]).map(([k, es]) => [es.reduce((s, v) => s + v, 0) / es.length, k * 20]);
  const TW = heroes.towerC, TOP = heroes.towerTop;
  // V5b-1b (cổng 16/10 TRƯỢT: khung trống, quét 226 °/s): máy nhìn vào NỘI DUNG (phố trong tường + tàu, tháp + phố cổ, La Línea, giao lộ + phố),
  // ống kính dài hơn ở đoạn bay tuyến/mốc đinh (nén phố), tốc độ góc ≤ 90 °/s (đo campath.json). Năm 7,0 s = 1882 (cận tháp thấy phố sườn tây mốc 1880 mọc quanh lâu đài), 7,8 s = 1895 để đoạn bay thấy La Línea c.1900.
  // V5b-2a (JJ1/KK1, chủ dự án duyệt 16/10): đoạn 7,8–14,1 s thay bằng MỘT CÚ LIÊN HOÀN — bay thấp dọc Winston Churchill Ave (tuyến OSM thật, ≤ 120 m so mặt đất,
  // nhìn về La Línea) → speed ramp → ORBIT quanh giao lộ đường băng × WCA + trạm biên giới (5 s, năm dừng 1941 trong orbit, hero ≥ 25 % khung) → crane up trung cảnh
  // → rise-and-reveal La Línea + vịnh. Mọi pha của cú: năm ≤ 10 năm/s (đoạn 20 s cũ không chứa nổi 1896 → 2026 ở nhịp đó → đoạn thử dài 24,5 s; reports/V5B2A-BAO-CAO.md §4).
  const year = track([[0, 1704], [3.5, 1757], [6.2, 1850], [7.0, 1882], [7.8, 1896], [10.8, 1925], [11.6, 1933], [12.4, 1941], [14.2, 1941], [16.6, 1964], [17.8, 1976], [22.8, 2026], [24.5, 2026]]);
  const LL = [320, 15, 1650];   // tâm nhìn La Línea (đích bay tuyến)
  const CEN = [0, 4, 0];        // giao lộ đường băng × Winston Churchill Ave (gốc toạ độ)
  const PIN = [12.4, 14.2];
  const lh = lienHoan({ vai: 'buoc-ngoat', hAt,
    route: { line: WCA, type: 'eo_dat', nguon: 'OSM Winston Churchill Avenue (tim tuyến gộp hai chiều, gib20.js)' },
    fly: { s0: 100, s1: 340, t: [7.8, 10.8], h: [104, 96], target: LL, r: 520, pitch: 0.12, fov: 26 },
    ramp: { t1: 11.6, k: 2.4 },
    orbit: { c: [0, 2, 0], r: 100, h: 40, look: 12, a0: -92, a1: -248, t1: 16.6, fov: 32, heroId: 'crossing' },
    crane: { t1: 17.8, h: 240, fov: 32, l: [-60, 30, -500] },
    reveal: { keys: [{ t: 19.4, p: [-700, 620, 420], l: [-80, 0, -60], fov: 31 }, { t: 21.1, p: [-1800, 1450, 220], l: [-130, 0, 250], fov: 32 }, { t: 22.8, p: [-2600, 2080, 60], l: [-150, 0, 350], fov: 33 }] },
    pin: PIN });
  const free = [
    { t: 0.0, p: [-1650, 470, -1700], l: [-430, 60, -1180], fov: 30 },
    { t: 1.6, p: [-1450, 430, -1480], l: [-420, 62, -1150], fov: 30 },
    { t: 3.2, p: [-1200, 380, -1300], l: [-380, 70, -1090], fov: 32 },
    { t: 4.8, p: [-780, 330, -1300], l: [-220, 92, -930], fov: 35 },
    { t: 6.0, p: [-360, 215, -1170], l: [-140, 98, -850], fov: 35 },
    { t: 7.0, p: [-200, 165, -1010], l: [-130, 98, -825], fov: 36 },
    { t: 7.4, p: [-195, 140, -740], l: [-10, 20, -240], fov: 28 },
    { t: 24.5, p: [-2760, 2160, 50], l: [-150, 0, 355], fov: 33 },   // màn kết: trôi chậm (không đứng yên)
  ];
  const G = grammar([lh], free);
  const path = G.path;
  const POP = M.pop, LAST = POP[POP.length - 1];
  const popAt = (y) => { if (y < POP[0][0]) return null; for (let i = 1; i < POP.length; i++) if (y <= POP[i][0]) { const [y0, a] = POP[i - 1], [y1, b] = POP[i]; return Math.exp(Math.log(a) + (Math.log(b) - Math.log(a)) * (y - y0) / (y1 - y0)); } return LAST[1]; };
  const fmt = (n) => Math.round(n).toLocaleString('en-US');
  const pinK = (t) => ease((t - (PIN[0] - 0.1)) / 0.35) * ease((PIN[1] + 0.3 - t) / 0.4);
  function state(t) {
    const y = year(t), c = path.at(t), pk = pinK(t), ph = G.phaseAt(t);
    // SPP theo trạng thái (KK1): bay nhanh SPP1 · orbit/mốc đinh/cận hero SPP4 · còn lại SPP2; ngoài cú liên hoàn: cận tháp 6,3–7,3 s SPP4
    let spp = ph.shot ? G.sppAt(t) : ((t > 6.3 && t < 7.3) ? 4 : 2);
    const hero = ph.shot && ['orbit', 'pin', 'crane'].includes(ph.kind) ? 'crossing' : (t > 4.8 && t < 7.4 ? 'tower' : null);
    return { year: y, cam: c, spp, dim: pk * 0.45, pin: pk, pinZoom: ease((t - PIN[0]) / 0.3) * ease((PIN[1] - t) / 0.35), phase: ph.kind, preset: ph.shot ? ph.shot.preset : null, vai: ph.shot ? ph.shot.vai : null, hero };
  }
  function apply(st, t) {
    heroes.hi.runway.value = st.pin; heroes.rwFrame.visible = st.pin > 0.01; heroes.rwFrameMat.opacity = 0.85 * st.pin; heroes.update(st.year);
    const hk = ease((t - 4.8) / 0.5) * ease((7.9 - t) / 0.5); heroes.hi.tower.value = 0.7 * hk; heroes.towerHull.visible = false;
  }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  const END = 22.8;
  function overlay(t, st, T, proj) {
    // chỉ số dân: NỘI SUY "≈" khi năm đang chạy (V5b-2a: không loé số đếm 1–2 khung khi năm đi qua năm điều tra); từ năm điều tra cuối (2022) hiện SỐ ĐẾM + dòng nguồn (role index_src)
    const p = popAt(st.year), counted = st.year >= LAST[0];
    const idx = p ? (counted ? `${fmt(LAST[1])} residents (${LAST[0]})` : '≈ ' + fmt(p) + ' residents') : null;
    const srcA = counted ? Math.max(0, Math.min(1, (st.year - LAST[0]) / 1.5)) : 0;
    const ma = Math.max(Math.max(0, Math.min(1, (4.6 - t) / 0.35)), Math.max(0, Math.min(1, (t - END) / 0.35)));
    const end = t > 10;
    // HH3: dòng phương pháp đầu phim thứ hai "≈ = interpolated between counts" — hiện từ khi chỉ số "≈" xuất hiện (1753 ≈ 3,3 s) tới 6,0 s (trong 6 s đầu, TL-Q5e)
    const la = Math.max(0, Math.min(1, (t - 3.2) / 0.35, (6.0 - t) / 0.35));
    const lines = end ? [{ s: '© OpenStreetMap contributors · Copernicus Sentinel data 2026', a: ma }]
      : [{ s: 'No AI imagery · Census · Catastro · Landsat 5', a: ma }, { s: '≈ = interpolated between counts', a: la }];
    T.chrome(t, st.year, st.pinZoom, idx, { lines, bottom: end }, srcA > 0 ? { s: `Count: Census of Gibraltar ${LAST[0]}, Table 1`, a: srcA } : null);
    T.card(t, [0.1, 3.1], '1704 · British and Dutch forces capture Gibraltar', 'Gibraltar National Museum', null);
    T.tag(t, [3.3, 4.7], 'reconstructed from LoC print, 1705', proj(V([-450, 30, -1150])));
    T.card(t, [4.8, 7.9], 'Tower of Homage · stands 23 metres tall', 'Ministry for Heritage, Gibraltar', proj(TOP));
    T.tag(t, [6.7, 7.7], 'reconstructed from LoC photo, 1860–80', proj(V([-330, 60, -960])));
    // V5b-2a (K: thẻ ảnh 2,96 s < 3 s): cửa sổ 3,4 s → hiện ≈ 3,37 s; neo trên đồng trung lập phía trước đường bay
    T.photo(t, [7.9, 11.3], ctx.photo, 'c. 1900 · The neutral ground, before the runway', 'V.B. Cumbo · LoC · muted houses: reconstructed', proj(V([12, 3, 150])));
    T.card(t, [12.2, 15.6], '1941 · A runway is built across the only road', 'HM Government of Gibraltar, 2023', proj(V([-45, 5, -4])));
  }
  const N = Math.round(24.5 * fps);
  const glog = () => Object.assign(grammarLog(G, N, fps, year, { hAt, line: WCA, focus: { tower: [TW[0], 100, TW[1]], crossing: CEN, lalinea: LL } }), { wca_len_m: lineLen(WCA) });
  return { N, fps, state, apply, overlay, path, year, wca: WCA, grammarLog: glog, camLog: glog,
    cues: { pin: PIN, photo: [7.9, 11.3], cards: [0.1, 4.8, 7.9, 12.2], reveal: [17.8, 22.8], line: [7.8, 10.8], orbit: [11.6, 16.6], end: [END, 24.5] } };
}

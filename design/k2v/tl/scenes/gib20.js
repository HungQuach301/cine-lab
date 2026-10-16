// ĐOẠN THỬ V5b-1 · GIBRALTAR ↔ LA LÍNEA 20 s (1704 → 2026). Dữ kiện trên hình lấy từ channel-k2/k2c-t3-01/tienky/claims.json (C17, C33)
// + nguồn tra trong phiên (Census of Gibraltar 2022 Bảng 1; Ministry for Heritage; HMGoG 199/2018). Ngôn ngữ hình (chủ dự án 16/10):
//  S1 0–3,2 mở toàn cảnh (glide) · S2 3,2–7,4 glide → zoom-in Tower of Homage (×≥ 5) · S3 7,8–10,8 bay dọc Winston Churchill Ave (tuyến OSM thật, ≤ 15 m)
//  + ảnh LoC "Neutral ground" neo điểm 3D · S4 10,8–14,4 quay sang + MỐC ĐINH 1941 (năm dừng 12,1–14,0 s, phóng 1,45×, đường băng sáng + viền, phần còn lại mờ)
//  · S5 14,4–20 reveal kéo lùi (×≥ 5) trong lúc 1941 → 2026; màn kết 18,6–20.
import { alongLine, makeCamPath, camLog, lineLen } from '../campath.js';
import { ease } from '../core.js';
export async function build(ctx) {
  const { THREE, M, terr, heroes, lines, track } = ctx, fps = 24, N = 480, hAt = terr.hAt;
  // tim tuyến Winston Churchill Ave: gộp hai chiều xe (gom theo N mỗi 20 m, lấy trung bình E)
  const raw = lines.wca, bins = new Map(); for (const [e, n] of raw) { const k = Math.round(n / 20); if (!bins.has(k)) bins.set(k, []); bins.get(k).push(e); }
  const WCA = [...bins.entries()].sort((a, b) => a[0] - b[0]).map(([k, es]) => [es.reduce((s, v) => s + v, 0) / es.length, k * 20]);
  const TW = heroes.towerC, TOP = heroes.towerTop;
  // V5b-1b (cổng 16/10 TRƯỢT: khung trống, quét 226 °/s): máy nhìn vào NỘI DUNG (phố trong tường + tàu, tháp + phố cổ, La Línea, giao lộ + phố),
  // ống kính dài hơn ở đoạn bay tuyến/mốc đinh (nén phố), tốc độ góc ≤ 90 °/s (đo campath.json). Năm 7,0 s = 1882 (cận tháp thấy phố sườn tây mốc 1880 mọc quanh lâu đài), 7,8 s = 1895 để đoạn bay thấy La Línea c.1900.
  const year = track([[0, 1704], [3.5, 1757], [6.2, 1850], [7.0, 1882], [7.8, 1895], [10.8, 1932], [12.1, 1941], [14.0, 1941], [14.5, 1946], [17.6, 1995], [18.9, 2026], [20, 2026]]);
  const LL = [320, 15, 1650];   // tâm nhìn La Línea
  const flight = alongLine(WCA, { s0: 25, s1: 400, t0: 7.8, t1: 10.8, h: [300, 270], look: 260, dip: 32, dt: 0.2, hAt }).map((k, i, A) => {
    const u = i / (A.length - 1), d = [LL[0] - k.p[0], LL[2] - 200 * u - k.p[2]], dl = Math.hypot(...d), r = 520;   // nhìn về La Línea, điểm nhìn cách máy 520 m (tiếp tuyến Hermite êm)
    return Object.assign(k, { l: [k.p[0] + d[0] / dl * r, k.p[1] - 0.25 * r, k.p[2] + d[1] / dl * r], fov: 21 }); });
  const keys = [
    { t: 0.0, p: [-1650, 470, -1700], l: [-430, 60, -1180], fov: 30 },
    { t: 1.6, p: [-1450, 430, -1480], l: [-420, 62, -1150], fov: 30 },
    { t: 3.2, p: [-1200, 380, -1300], l: [-380, 70, -1090], fov: 32 },
    { t: 4.8, p: [-780, 330, -1300], l: [-220, 92, -930], fov: 35 },
    { t: 6.0, p: [-360, 215, -1170], l: [-140, 98, -850], fov: 35 },
    { t: 7.0, p: [-200, 165, -1010], l: [-130, 98, -825], fov: 36 },
    { t: 7.4, p: [-245, 190, -800], l: [-110, 90, -480], fov: 33 },
    ...flight,
    { t: 11.5, p: [-190, 170, -330], l: [30, 5, 260], fov: 26 },
    { t: 12.3, p: [-150, 76, -235], l: [20, 2, 200], fov: 26 },   // MỐC ĐINH: chéo qua đường băng + hàng xe ở chắn, La Línea phía sau
    { t: 13.2, p: [-120, 72, -248], l: [22, 2, 205], fov: 26 },
    { t: 14.1, p: [-85, 85, -265], l: [25, 4, 215], fov: 26 },
    { t: 15.0, p: [10, 420, -800], l: [20, 10, 420], fov: 27 },
    { t: 16.5, p: [-900, 1100, -1300], l: [-80, 0, 500], fov: 30 },
    { t: 18.6, p: [-2500, 2050, -250], l: [-150, 0, 300], fov: 33 },
    { t: 20.0, p: [-2750, 2200, 50], l: [-150, 0, 350], fov: 33 },
  ];
  const path = makeCamPath(keys);
  const CEN = [0, 4, 0];   // giao lộ đường băng × đường (gốc toạ độ)
  const POP = M.pop;
  const popAt = (y) => { if (y < POP[0][0]) return null; for (let i = 1; i < POP.length; i++) if (y <= POP[i][0]) { const [y0, a] = POP[i - 1], [y1, b] = POP[i]; return Math.exp(Math.log(a) + (Math.log(b) - Math.log(a)) * (y - y0) / (y1 - y0)); } return POP[POP.length - 1][1]; };
  const fmt = (n) => Math.round(n).toLocaleString('en-US');
  const pinK = (t) => ease((t - 12.0) / 0.35) * ease((14.3 - t) / 0.4);
  function state(t) {
    const y = year(t), c = path.at(t), pk = pinK(t);
    let spp = 2; if ((t > 6.3 && t < 7.3) || (t > 12.0 && t < 14.3)) spp = 4; if (t > 7.9 && t < 10.9) spp = 1;   // SPP cao ở cận hero/mốc đinh, thấp khi bay nhanh dọc tuyến
    return { year: y, cam: c, spp, dim: pk * 0.45, pin: pk, pinZoom: ease((t - 12.1) / 0.3) * ease((14.0 - t) / 0.35) };
  }
  function apply(st, t) {
    heroes.hi.runway.value = st.pin; heroes.rwFrame.visible = st.pin > 0.01; heroes.rwFrameMat.opacity = 0.85 * st.pin; heroes.update(st.year);
    const hk = ease((t - 4.8) / 0.5) * ease((7.9 - t) / 0.5); heroes.hi.tower.value = 0.7 * hk; heroes.towerHull.visible = false;
  }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  function overlay(t, st, T, proj) {
    const p = popAt(st.year), cen = POP.find((r) => Math.abs(r[0] - st.year) < 0.5);
    const idx = p ? (cen ? '' : '≈ ') + fmt(cen ? cen[1] : p) + ' residents' : null;
    const ma = Math.max(Math.max(0, Math.min(1, (4.6 - t) / 0.35)), Math.max(0, Math.min(1, (t - 18.6) / 0.35)));
    const ms = t < 10 ? 'No AI imagery · Census · Catastro · Landsat 5' : '© OpenStreetMap contributors · Copernicus Sentinel data 2026';
    T.chrome(t, st.year, st.pinZoom, idx, { a: ma, s: ms, bottom: t > 10 });
    T.card(t, [0.1, 3.1], '1704 · British and Dutch forces capture Gibraltar', 'Gibraltar National Museum', null);
    T.tag(t, [3.3, 4.7], 'reconstructed from LoC print, 1705', proj(V([-450, 30, -1150])));
    T.card(t, [4.8, 7.9], 'Tower of Homage · stands 23 metres tall', 'Ministry for Heritage, Gibraltar', proj(TOP));
    T.tag(t, [6.7, 7.7], 'reconstructed from LoC photo, 1860–80', proj(V([-330, 60, -960])));
    T.photo(t, [8.0, 11.0], ctx.photo, 'c. 1900 · The neutral ground, before the runway', 'V.B. Cumbo · LoC · muted houses: reconstructed', proj(V([15, 3, 260])));
    T.card(t, [12.1, 15.2], '1941 · A runway is built across the only road', 'HM Government of Gibraltar, 2023', proj(V([-45, 5, -4])));
  }
  return { N, fps, state, apply, overlay, path, year, wca: WCA,
    camLog: () => Object.assign(camLog(path, N, fps, year, { line: WCA, focus: { tower: [TW[0], 100, TW[1]], crossing: CEN } }), { wca_len_m: lineLen(WCA) }),
    cues: { pin: [12.1, 14.0], photo: [8.0, 11.0], cards: [0.1, 4.8, 8.0, 12.1], reveal: [14.4, 20], line: [7.8, 10.8] } };
}

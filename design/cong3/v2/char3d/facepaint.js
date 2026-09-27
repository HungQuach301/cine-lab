// Cổng 3 v3 — C′: MẶT VẼ TAY trên texture phủ đầu 3D (quyết định chủ dự án, điểm 1 vòng 2).
// Texture chiếu từ phía trước lên UV của CHÍNH lưới đầu (u = 0,5 + x/0,84, v = y; x, y theo H, hệ đầu: y = 0 cằm, 1 đỉnh sọ),
// nên mặt đi theo hình học đầu (không trượt khi quay) và nhận ánh sáng cảnh (Lambert, không bóng).
// Nền texture TRẮNG = không đổi màu da (màu đỉnh của khối đầu giữ tông, AO); nét vẽ chỉ nhân màu (tối/ấm hơn) ở vùng mặt,
// thoải về trắng ở rìa → không có đường nối. Nửa sau đầu gán về một điểm trắng.
// Nét: cọ mềm có rung, nhiều lớp mỏng — chất tranh sơn của hướng C; thay nếp nhăn và khe miệng khắc vào hình học
// (vòng 2: khe miệng khắc thành rãnh "như sẹo", da mịn đều "như sáp" — lỗi L3).
import * as THREE from '../../shared/node_modules/three/build/three.module.js';

export const FACE_UV = { halfW: 0.42 };   // x ∈ [−0,42, 0,42] H ↔ u ∈ [0, 1]
const N = 1024;
const px = (x) => (x / (2 * FACE_UV.halfW) + 0.5) * N, py = (y) => (1 - y) * N;

function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

// Nét cọ: chuỗi chấm tròn mềm dọc đường cong, rung ngang nhẹ, độ dày thon hai đầu.
function stroke(g, R, pts, w, color, alpha, jit = 0.25) {
  const P = pts.map(([x, y]) => [px(x), py(y)]);
  let L = 0; const seg = []; for (let i = 0; i < P.length - 1; i++) { const l = Math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]); seg.push(l); L += l; }
  const n = Math.max(4, Math.ceil(L / (w * 0.35)));
  for (let k = 0; k <= n; k++) {
    let s = (k / n) * L, i = 0; while (i < seg.length - 1 && s > seg[i]) { s -= seg[i]; i++; }
    const t = seg[i] ? s / seg[i] : 0, x = P[i][0] + (P[i + 1][0] - P[i][0]) * t, y = P[i][1] + (P[i + 1][1] - P[i][1]) * t;
    const taper = Math.sin(Math.PI * Math.min(1, Math.max(0, k / n)) * 0.9 + 0.15), r = Math.max(0.6, w * taper * (0.85 + 0.3 * R()));
    const jx = (R() - 0.5) * w * jit, jy = (R() - 0.5) * w * jit;
    const gr = g.createRadialGradient(x + jx, y + jy, 0, x + jx, y + jy, r);
    gr.addColorStop(0, `rgba(${color},${alpha})`); gr.addColorStop(1, `rgba(${color},0)`);
    g.fillStyle = gr; g.beginPath(); g.arc(x + jx, y + jy, r, 0, Math.PI * 2); g.fill();
  }
}
function blot(g, x, y, r, color, alpha) { const X = px(x), Y = py(y), rr = r / (2 * FACE_UV.halfW) * N;
  const gr = g.createRadialGradient(X, Y, 0, X, Y, rr); gr.addColorStop(0, `rgba(${color},${alpha})`); gr.addColorStop(1, `rgba(${color},0)`); g.fillStyle = gr; g.beginPath(); g.arc(X, Y, rr, 0, Math.PI * 2); g.fill(); }
const mir = (pts) => pts.map(([x, y]) => [-x, y]);

// Biểu cảm (đợt vá A2+, V5): thông số dùng chung cho nét vẽ và lông mày sợi 3D (cast3d.js) để hai lớp cùng chuyển.
//  browIn: nâng đầu trong mày (H); browOut: nâng đuôi mày; knit: kéo đầu trong mày vào giữa; corner: dịch khoé miệng (+ lên);
//  press: mím môi (0–1, môi mỏng lại); chin: căng cằm (nếp "da cam"); wet: mắt ngấn nước; lidDrop: mí trên sụp (nét mi hạ xuống).
export const EXPR = {
  neutral:   { browIn: 0.000, browOut: 0.000, knit: 0.000, corner: 0.004, press: 0.2, chin: 0.0, wet: 0.0, lidDrop: 0.000, smile: 0.0, tear: 0 },
  sad_smile: { browIn: 0.040, browOut: -0.012, knit: 0.006, corner: 0.042, press: 0.6, chin: 0.0, wet: 0.6, lidDrop: 0.010, smile: 1.0, tear: 0 },
  choked:    { browIn: 0.055, browOut: -0.020, knit: 0.020, corner: -0.032, press: 1.0, chin: 1.0, wet: 1.0, lidDrop: 0.006, smile: 0.0, tear: 1 },
};

// E = tâm nhãn cầu [x, y, z] (H), dùng chung với khối đầu để nét mi khớp đúng mí.
export function paintFace(isIda, E, seed = 7, expr = 'neutral') {
  const X = EXPR[expr] || EXPR.neutral;
  const cv = document.createElement('canvas'); cv.width = cv.height = N; const g = cv.getContext('2d'); const R = rng(seed);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, N, N);
  const both = (pts, ...a) => { stroke(g, R, pts, ...a); stroke(g, R, mir(pts), ...a); };
  const fill = (pts, color, alpha) => { g.fillStyle = `rgba(${color},${alpha})`; g.beginPath(); pts.forEach(([x, y], k) => (k ? g.lineTo(px(x), py(y)) : g.moveTo(px(x), py(y)))); g.closePath(); g.fill(); };
  // 1) Lớp da: vệt cọ rất nhạt theo cơ mặt (phá chất "sáp").
  for (let i = 0; i < 260; i++) {
    const x = (R() - 0.5) * 0.56, y = 0.18 + R() * 0.72, a = (x > 0 ? 1 : -1) * (0.4 + R() * 0.5), l = 0.03 + R() * 0.05;
    const warm = R() < 0.6; stroke(g, R, [[x, y], [x + Math.cos(a) * l, y - Math.sin(a) * l * 0.6]], 5 + R() * 7, warm ? '214,160,140' : '190,160,160', 0.05 + R() * 0.05, 0.4);
  }
  // 2) Sắc độ: má ấm thấp và rộng (V5: bỏ mảng tím hốc mắt — cộng bóng khối thành "vết bầm"), mũi đỏ nhẹ.
  for (const s of [1, -1]) blot(g, s * (isIda ? 0.18 : 0.19), isIda ? 0.36 : 0.33, isIda ? 0.09 : 0.085, '226,130,124', isIda ? 0.34 : 0.26);
  if (isIda) for (const s of [1, -1]) blot(g, s * 0.25, 0.47, 0.07, '246,210,190', 0.22);      // nâng sáng ấm vùng sau gò má
  blot(g, 0, isIda ? 0.44 : 0.38, 0.045, '220,140,130', 0.16);
  // 3) Mắt: nét mi trên đậm (hạ theo lidDrop), mí dưới, nếp mí; Ida đuôi mắt cụp.
  const ex = E[0], ey = E[1] - X.lidDrop, er = isIda ? 0.06 : 0.066;
  both([[ex - er, ey + 0.004], [ex - er * 0.3, ey + (isIda ? 0.016 : 0.028)], [ex + er * 0.4, ey + (isIda ? 0.014 : 0.026)], [ex + er * 1.05, ey - (isIda ? 0.006 : 0.0)], [ex + er * 1.35, ey + (isIda ? 0.008 : 0.0)]], isIda ? 6.5 : 5, '40,24,24', 0.95, 0.12);
  both([[ex - er * 0.8, ey - 0.028], [ex, ey - 0.036], [ex + er * 0.8, ey - 0.026]], 2.5, '120,74,70', 0.5, 0.2);
  if (X.wet > 0) { both([[ex - er * 0.7, ey - 0.03], [ex, ey - 0.037], [ex + er * 0.7, ey - 0.029]], 2.2, '200,110,110', 0.35 * X.wet, 0.1);   // viền mi dưới đỏ
    for (const s of [1, -1]) blot(g, s * (ex + er * 0.1), ey - 0.03, 0.006, '255,255,255', 0.6 * X.wet); }                               // ngấn nước
  if (isIda) {
    both([[ex - er * 0.9, ey + 0.034], [ex, ey + 0.045], [ex + er, ey + 0.024]], 3.4, '118,78,72', 0.65, 0.2);                           // nếp da trên mí
    for (const k of [0, 1]) both([[ex - er * 0.7, ey - 0.048 - k * 0.016], [ex, ey - 0.056 - k * 0.018], [ex + er * 0.8, ey - 0.044 - k * 0.014]], 2, '125,82,78', 0.55, 0.25);   // nếp dưới mắt (nét, không mảng)
    for (const a of [-0.55, -0.25, 0.05, 0.35]) both([[ex + er * 1.05, ey - 0.004], [ex + er * 1.05 + 0.055 * Math.cos(a), ey - 0.004 + 0.055 * Math.sin(a)]], 1.8, '118,76,72', 0.7, 0.3);   // chân chim
  }
  // 4) Lông mày: cung mảnh có hình (Ida: xám bạc, cong nữ tính); biểu cảm nâng đầu trong / kéo vào.
  const bw = isIda ? '96,88,88' : '90,64,52';
  const browPts = (isIda ? [[0.045, 0.655], [0.12, 0.676], [0.19, 0.668], [0.235, 0.64]] : [[0.055, 0.60], [0.13, 0.607], [0.215, 0.586]]).map(([x, y], k, a) => {
    const t = k / (a.length - 1); return [x - X.knit * (1 - t), y + X.browIn * (1 - t) + X.browOut * t]; });
  both(browPts, isIda ? 7 : 7, bw, 0.95, 0.3);
  if (X.knit > 0.003) for (const s of [1, -1]) stroke(g, R, [[s * 0.022, 0.655], [s * 0.026, 0.625]], 2, '140,95,88', 0.45 * X.knit / 0.01, 0.2);   // nếp dọc giữa mày
  // 5) Mũi: bóng cánh mũi và lỗ mũi — vẽ, không khắc sâu.
  for (const s of [1, -1]) blot(g, s * 0.03, isIda ? 0.40 : 0.354, 0.016, '120,70,64', 0.45);
  // 6) Miệng: môi có hình (cung Cupid, môi dưới đầy hơn), khe môi mềm; mím (press) làm môi mỏng; khoé theo biểu cảm.
  const my = isIda ? 0.267 : 0.256, mw = isIda ? 0.098 : 0.066, c = X.corner, thin = (1 - 0.55 * X.press) * (isIda ? 0.62 : 1);
  if (isIda) {
    fill([[-mw, my + c * 0.25], [-0.055, my + 0.014 * thin + c * 0.3], [-0.014, my + 0.02 * thin], [0, my + 0.016 * thin], [0.014, my + 0.02 * thin], [0.055, my + 0.014 * thin + c * 0.3], [mw, my + c * 0.25], [0, my + 0.002]], '160,88,90', 0.62);   // môi trên
    fill([[-mw * 0.92, my + c * 0.25], [0, my - 0.001], [mw * 0.92, my + c * 0.25], [0.06, my - 0.02 * thin + c * 0.3], [0, my - 0.026 * thin], [-0.06, my - 0.02 * thin + c * 0.3]], '172,100,100', 0.55);   // môi dưới
    stroke(g, R, [[-0.045, my - 0.02 * thin], [0, my - 0.027 * thin], [0.045, my - 0.02 * thin]], 2, '240,190,176', 0.35, 0.1);                  // sáng mép môi dưới
    for (const x of [-0.035, -0.018, 0.018, 0.035]) stroke(g, R, [[x, my + 0.03], [x * 1.05, my + 0.05]], 1.5, '130,86,80', 0.5, 0.2);   // nếp dọc môi trên (tuổi)
  } else { blot(g, 0, my + 0.018, 0.058, '200,120,115', 0.28); blot(g, 0, my - 0.018, 0.05, '205,130,120', 0.30); }
  stroke(g, R, [[-mw, my + c], [-mw * 0.45, my + 0.002 + c * 0.35], [0, my], [mw * 0.45, my + 0.002 + c * 0.35], [mw, my + c]], 3.4, '80,38,40', 0.8, 0.12);
  if (X.smile > 0) { both([[ex - er * 0.8, ey - 0.022], [ex, ey - 0.03], [ex + er * 0.9, ey - 0.02]], 3, '130,80,76', 0.55 * X.smile, 0.15);   // mí dưới nâng (cười thật)
    for (const s of [1, -1]) blot(g, s * 0.17, 0.43, 0.06, '205,120,112', 0.18 * X.smile); }                                                          // gò má nâng, ửng
  if (X.smile > 0) both([[mw - 0.004, my + c + 0.03], [mw + 0.012, my + c + 0.004], [mw + 0.006, my + c - 0.02]], 3, '130,82,76', 0.6 * X.smile, 0.15);   // ngoặc cười ở khoé   // nếp má khi cười
  if (X.chin > 0) { for (let k = 0; k < 18; k++) blot(g, (R() - 0.5) * 0.08, 0.15 + R() * 0.05, 0.006, '160,110,100', 0.25 * X.chin);   // cằm "da cam" khi nghẹn
    stroke(g, R, [[-0.05, 0.205], [0, 0.198], [0.05, 0.205]], 2.2, '150,100,92', 0.4 * X.chin, 0.2); }
  // 7) Tuổi (Ida): nếp trán (biểu cảm buồn: cong lên giữa), rãnh mũi–má rõ, rãnh khoé miệng xuống cằm, đồi mồi. Cas: tàn nhang.
  if (isIda) {
    const lift = X.browIn * 1.5;
    for (const yy of [0.735, 0.772, 0.808]) for (const s of [1, -1]) stroke(g, R, [[s * 0.02, yy + lift], [s * 0.12, yy + 0.004 + lift * 0.3], [s * 0.24, yy - 0.006]], 2.6, '130,88,82', 0.5, 0.3);
    both([[0.07, 0.43], [0.098, 0.34], [0.118 + c * 0.3, 0.275 + c]], 5, '120,76,72', 0.66, 0.22);          // rãnh mũi–má
    both([[mw + 0.012, my + c - 0.006], [0.1, 0.19], [0.108, 0.13]], 3.6, '125,82,76', 0.55, 0.25);           // rãnh khoé miệng xuống cằm
    // tóc bạc chải ngược ở thái dương, lộ dưới vành mũ (nhân màu nên dùng xám lạnh)
    for (let k = 0; k < 16; k++) for (const s of [1, -1]) { const o = k * 0.006; stroke(g, R, [[s * (0.29 + o), 0.84], [s * (0.33 + o), 0.72], [s * (0.36 + o * 0.6), 0.6]], 2.2, '150,150,160', 0.35, 0.5); }
    for (const [sx, sy, sr] of [[0.24, 0.44, 0.006], [-0.2, 0.38, 0.005], [0.17, 0.3, 0.004]]) blot(g, sx, sy, sr, '170,130,110', 0.3);   // V5: đồi mồi nhỏ (đốm to đọc thành vết bầm)
  } else {
    for (let i = 0; i < 14; i++) { const s = R() < 0.5 ? 1 : -1; blot(g, s * (0.12 + R() * 0.12), 0.34 + R() * 0.1, 0.006 + R() * 0.004, '180,120,90', 0.35); }
  }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; t.needsUpdate = true;
  // Lớp phát sáng (emissive): texture nhân màu không làm sáng hơn da được → ánh ướt mi dưới, nước mắt vẽ ở đây (đen = không phát).
  const cg = document.createElement('canvas'); cg.width = cg.height = N; const gg = cg.getContext('2d'); gg.fillStyle = '#000'; gg.fillRect(0, 0, N, N);
  if (X.wet > 0) for (const s2 of [1, -1]) stroke(gg, R, [[s2 * (ex - er * 0.6), ey - 0.031], [s2 * ex, ey - 0.036], [s2 * (ex + er * 0.6), ey - 0.03]], 2.2, '255,236,220', 0.8 * X.wet, 0.05);
  if (X.tear > 0) stroke(gg, R, [[-(ex - er * 0.55), ey - 0.04], [-(ex - er * 0.7), ey - 0.09], [-(ex - er * 0.6), ey - 0.15]], 3, '255,230,210', 0.55 * X.tear, 0.1);   // một giọt nước mắt má phải
  const tg = new THREE.CanvasTexture(cg); tg.colorSpace = THREE.SRGBColorSpace; tg.needsUpdate = true; t.userData = { glint: tg };
  return t;
}

// Gán UV chiếu trước cho lưới đầu (toạ độ đỉnh đang theo mét, H = sheet.H_m). Mặt sau (z < 0,02 H) → điểm trắng góc (0,01; 0,99).
export function faceUV(geo, H) {
  const p = geo.attributes.position, uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) { const x = p.getX(i) / H, y = p.getY(i) / H, z = p.getZ(i) / H;
    const f = z > 0.02; uv[i * 2] = f ? x / (2 * FACE_UV.halfW) + 0.5 : 0.01; uv[i * 2 + 1] = f ? y : 0.99; }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
}

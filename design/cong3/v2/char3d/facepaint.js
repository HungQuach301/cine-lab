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

// E = tâm nhãn cầu [x, y, z] (H), dùng chung với khối đầu để nét mi khớp đúng mí.
export function paintFace(isIda, E, seed = 7) {
  const cv = document.createElement('canvas'); cv.width = cv.height = N; const g = cv.getContext('2d'); const R = rng(seed);
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, N, N);
  const both = (pts, ...a) => { stroke(g, R, pts, ...a); stroke(g, R, mir(pts), ...a); };
  // 1) Lớp da: vệt cọ rất nhạt, hướng theo cơ mặt (phá chất "sáp" của màu đỉnh mịn).
  for (let i = 0; i < 260; i++) {
    const x = (R() - 0.5) * 0.56, y = 0.18 + R() * 0.72, a = (x > 0 ? 1 : -1) * (0.4 + R() * 0.5), l = 0.03 + R() * 0.05;
    const warm = R() < 0.5; stroke(g, R, [[x, y], [x + Math.cos(a) * l, y - Math.sin(a) * l * 0.6]], 5 + R() * 7, warm ? '214,160,140' : '176,150,168', 0.05 + R() * 0.05, 0.4);
  }
  // 2) Sắc độ: má ấm, hốc mắt lạnh, mũi đỏ nhẹ.
  for (const s of [1, -1]) { blot(g, s * (isIda ? 0.2 : 0.19), isIda ? 0.40 : 0.33, isIda ? 0.07 : 0.085, '226,150,140', isIda ? 0.20 : 0.26);
    blot(g, s * E[0], E[1] + 0.01, 0.075, '150,130,170', 0.16); }
  blot(g, 0, isIda ? 0.44 : 0.38, 0.045, '220,140,130', 0.16);
  // 3) Mắt: nét mi trên đậm (đọc hướng nhìn dù mí che), mí dưới nhạt; Ida mí trên nặng, đuôi cụp.
  const ex = E[0], ey = E[1], er = isIda ? 0.06 : 0.066;
  both([[ex - er, ey + 0.004], [ex - er * 0.3, ey + (isIda ? 0.016 : 0.028)], [ex + er * 0.4, ey + (isIda ? 0.014 : 0.026)], [ex + er * 1.05, ey - (isIda ? 0.012 : 0.0)]], isIda ? 4.5 : 5, '52,34,32', 0.85, 0.12);
  both([[ex - er * 0.8, ey - 0.028], [ex, ey - 0.036], [ex + er * 0.8, ey - 0.026]], 2.5, '120,80,76', 0.35, 0.2);
  if (isIda) both([[ex - er * 0.9, ey + 0.032], [ex, ey + 0.042], [ex + er, ey + 0.022]], 3, '150,100,90', 0.35, 0.2);   // nếp da trên mí
  // 4) Lông mày.
  const bw = isIda ? '150,140,132' : '90,64,52';
  both(isIda ? [[0.045, 0.655], [0.12, 0.672], [0.19, 0.664], [0.235, 0.638]] : [[0.055, 0.60], [0.13, 0.607], [0.215, 0.586]], isIda ? 5 : 7, bw, isIda ? 0.75 : 0.85, 0.35);
  // 5) Mũi: bóng cánh mũi và lỗ mũi — vẽ, không khắc sâu.
  for (const s of [1, -1]) blot(g, s * 0.03, isIda ? 0.40 : 0.354, 0.016, '120,70,64', 0.45);
  // 6) Miệng: khe môi là nét mềm (không rãnh), môi hồng nhạt; Ida khoé hơi trễ, Cas khoé hơi nhếch.
  const my = isIda ? 0.267 : 0.256;
  blot(g, 0, my + 0.018, isIda ? 0.06 : 0.058, '200,120,115', 0.28); blot(g, 0, my - 0.018, isIda ? 0.055 : 0.05, '205,130,120', 0.30);
  stroke(g, R, [[-(isIda ? 0.08 : 0.068), my - (isIda ? 0.008 : -0.004)], [-0.035, my + 0.002], [0, my], [0.035, my + 0.002], [isIda ? 0.08 : 0.068, my - (isIda ? 0.008 : -0.004)]], 3.2, '96,50,48', 0.6, 0.15);
  // 7) Tuổi (Ida): nếp trán, chân chim, rãnh mũi–má, rãnh khoé miệng — nét mảnh, nhạt, đứt quãng; đồi mồi.
  if (isIda) {
    for (const yy of [0.735, 0.772, 0.808]) for (const s of [1, -1]) stroke(g, R, [[s * 0.02, yy], [s * 0.12, yy + 0.004], [s * 0.24, yy - 0.006]], 2.2, '150,100,92', 0.28, 0.3);
    for (const a of [-0.45, -0.1, 0.25]) both([[0.232, 0.577], [0.232 + 0.05 * Math.cos(a), 0.577 + 0.05 * Math.sin(a)]], 1.8, '150,100,92', 0.30, 0.3);
    both([[0.075, 0.43], [0.10, 0.34], [0.122, 0.27]], 3.5, '160,105,95', 0.32, 0.25);
    both([[0.095, 0.24], [0.11, 0.18], [0.118, 0.13]], 2.8, '160,105,95', 0.26, 0.25);
    both([[0.075, 0.52], [0.15, 0.505], [0.21, 0.522]], 3, '165,120,125', 0.22, 0.25);    // bọng dưới mắt
    for (const [sx, sy, sr] of [[0.27, 0.66, 0.016], [0.24, 0.44, 0.011], [-0.29, 0.58, 0.014], [-0.2, 0.38, 0.009]]) blot(g, sx, sy, sr, '170,130,110', 0.35);
  } else {
    for (let i = 0; i < 14; i++) { const s = R() < 0.5 ? 1 : -1; blot(g, s * (0.12 + R() * 0.12), 0.34 + R() * 0.1, 0.006 + R() * 0.004, '180,120,90', 0.35); }   // tàn nhang
  }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; t.needsUpdate = true;
  return t;
}

// Gán UV chiếu trước cho lưới đầu (toạ độ đỉnh đang theo mét, H = sheet.H_m). Mặt sau (z < 0,02 H) → điểm trắng góc (0,01; 0,99).
export function faceUV(geo, H) {
  const p = geo.attributes.position, uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) { const x = p.getX(i) / H, y = p.getY(i) / H, z = p.getZ(i) / H;
    const f = z > 0.02; uv[i * 2] = f ? x / (2 * FACE_UV.halfW) + 0.5 : 0.01; uv[i * 2 + 1] = f ? y : 0.99; }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
}

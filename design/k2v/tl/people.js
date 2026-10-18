// K2V tl · V6 (V2D-1, PT4 §8.1) · NGƯỜI LOW-POLY CÓ KHỚP thay "trụ hộp" (thân + mũ) ở mọi cảnh 3D bay.
//  Một lưới người ≈ 1,72 m (hướng trước = +X cục bộ, phải = +Z, đứng trên y = 0): giày, ống chân (ghệt/bít tất), đùi (quần ống túm), áo khoác có VẠT SAU mở trước
//  (lộ gi-lê), thân, dây đeo chéo, cổ tay áo, tay buông tự nhiên (hơi dang 5°), cổ, đầu, tóc buộc sau gáy, MŨ TRICORN (một lưới liền: chóp + vành bẻ lên ba phía, có độ dày).
//  Biến thể: 'order' (lính đứng súng dựng bên phải — tay phải giữ súng), 'march' (súng vác vai trái), 'civ' (không súng), 'woman' (váy dài + khăn choàng), 'sailor' (mũ tròn).
//  CHU KỲ ĐI trong shader (đùi + ống chân + tay quay quanh hông/vai, thân nhấp nhô, đầu quay khi đứng): pha, biên độ (0 đứng – 1 đi), tần số bước mỗi người —
//  bóng đổ dùng cùng biến dạng (customDepthMaterial). Màu theo PHẦN × màu từng người (áo, quần, ống chân, phụ: dây đeo/cổ tay/viền) + tông da.
//  LOD: người cao < lodPx điểm ảnh dùng lưới thô (≈ 60 tam giác) — cùng màu, cùng chu kỳ; không phóng to người (luật C2-7).
//  Quân phục 1782 (VẬT MANG DỮ KIỆN): bảng màu ở UNIFORMS kèm nguồn — xem báo cáo V6 §2; chỗ chưa có nguồn chi tiết ghi "illustrative" trên hình.
import { THREE, rng, maskify } from './core.js';

// ---------- bảng màu (sRGB) ----------
//  gb_inf: bộ binh Anh 1782 — áo đỏ, gi-lê/quần trắng-ngà, ghệt đen, dây đeo trắng (Royal Warrant 1768; tranh J. S. Copley "The Siege and Relief of Gibraltar" 1783–91, PD)
//  gb_art: pháo binh Hoàng gia — áo lam đậm, viền đỏ, quần trắng (Royal Warrant 1768: Royal Artillery blue faced red)
//  es_inf: bộ binh Tây Ban Nha — áo trắng, viền màu trung đoàn (Reglamento 1768; Clonard, Historia orgánica… 1851–62, bản khắc PD) — viền màu theo khối: minh hoạ
//  fr_inf: bộ binh Pháp — áo trắng, viền màu (Règlement 1779) — minh hoạ
//  civ / woman / sailor: dân thường, thuỷ thủ — tông vải tự nhiên (minh hoạ)
export const UNIFORMS = {
  gb_inf: { coat: ['#9b2a22', '#a3302a', '#8f251f'], small: ['#e3dccb', '#d9d1bd'], legs: ['#26221e'], acc: ['#ece6d8'], hat: '#1c1916', hair: ['#e2dccf', '#cfc6b5', '#3b2c22'] },
  gb_art: { coat: ['#262f49', '#2b3552', '#222a40'], small: ['#e3dccb'], legs: ['#26221e'], acc: ['#a8392c'], hat: '#1c1916', hair: ['#e2dccf', '#3b2c22'] },
  es_inf: { coat: ['#e6e1d5', '#ddd8cb', '#ece8de'], small: ['#e6e1d5', '#d8d2c2'], legs: ['#2a2622', '#e2ddd0'], acc: ['#2f4f8f', '#a8392c', '#2f5f3a', '#c9a227', '#1d1d1d'], hat: '#1c1916', hair: ['#e2dccf', '#3b2c22', '#2a2019'] },
  fr_inf: { coat: ['#e6e1d5', '#e0dbcf'], small: ['#e6e1d5'], legs: ['#2a2622'], acc: ['#2e5c8a', '#6b1e2b', '#c9a227'], hat: '#1c1916', hair: ['#e2dccf', '#3b2c22'] },
  civ: { coat: ['#5e4a38', '#6b5a48', '#45392f', '#7a6a52', '#3c4a5c', '#8a7a62'], small: ['#c8bca4', '#a8977a', '#d9d0bc', '#7a6a52'], legs: ['#d9d2c0', '#5b4a3a', '#3a3029'], acc: ['#e8e2d2', '#b8402f', '#d9d0bc'], hat: '#2a231d', hair: ['#3b2c22', '#2a2019', '#5a4632', '#8a7a62'] },
  woman: { coat: ['#7a5a48', '#5e4a58', '#4a5a6a', '#8a6a4a', '#3c3a34'], small: ['#6b5040', '#4e4a5a', '#7a6a52', '#5a4632', '#8a7a62'], legs: ['#3a3029'], acc: ['#e8e2d2', '#d9d0bc', '#c8b48a'], hat: '#e8e2d2', hair: ['#3b2c22', '#2a2019', '#5a4632'] },
  sailor: { coat: ['#2b3552', '#3a4560', '#262f49'], small: ['#e3dccb', '#c8bca4'], legs: ['#d9d2c0'], acc: ['#e3dccb', '#b8402f'], hat: '#1c1916', hair: ['#3b2c22', '#2a2019'] },
};
const SKIN = ['#c9a08a', '#b89078', '#a88068', '#d4b09c', '#9c7a62'];   // tông da dịu (ACES + vibrance đẩy cam)

// ---------- dựng lưới ----------
// part: 0 áo · 1 gi-lê/quần (đồ lót ngoài) · 2 ống chân · 3 phụ (dây đeo, cổ tay, viền) · 4 da · 5 mũ · 6 giày · 7 gỗ báng súng · 8 kim loại · 9 tóc
// swing: 0 cứng · 1 chân phải · 2 chân trái · 3 tay phải · 4 tay trái · 5 đầu (quay quanh cổ) · 6 ống chân phải (gối) · 7 ống chân trái
function builder() {
  const P = [], N = [], A = [], S = [];
  const tri = (a, b, c, part, sw) => { const n = new THREE.Vector3().subVectors(b, a).cross(new THREE.Vector3().subVectors(c, a)).normalize(); for (const v of [a, b, c]) { P.push(v.x, v.y, v.z); N.push(n.x, n.y, n.z); A.push(part); S.push(sw); } };
  const quad = (a, b, c, d, part, sw) => { tri(a, b, c, part, sw); tri(a, c, d, part, sw); };
  // lăng trụ ellip cụt: tâm (x, z), y0..y1, bán trục (rx0, rz0) → (rx1, rz1), n cạnh, cung [a0, a1] (mở = vạt áo), nắp
  function prism({ x = 0, z = 0, y0, y1, rx0, rz0, rx1 = rx0, rz1 = rz0, n = 8, a0 = 0, a1 = Math.PI * 2, cap0 = true, cap1 = true, dx1 = 0, part, sw = 0, rot = 0 }) {
    const full = Math.abs(a1 - a0 - Math.PI * 2) < 1e-6, m = full ? n : n, ring = (y, rx, rz, ox) => [...Array(m + (full ? 0 : 1)).keys()].map((i) => { const a = a0 + (a1 - a0) * i / m + rot; return new THREE.Vector3(x + ox + Math.cos(a) * rx, y, z + Math.sin(a) * rz); });
    const r0 = ring(y0, rx0, rz0, 0), r1 = ring(y1, rx1, rz1, dx1), k = r0.length;
    for (let i = 0; i < (full ? k : k - 1); i++) { const j = (i + 1) % k; quad(r0[i], r0[j], r1[j], r1[i], part, sw); if (!full) quad(r0[j], r0[i], r1[i], r1[j], part, sw); }
    const c0 = new THREE.Vector3(x, y0, z), c1 = new THREE.Vector3(x + dx1, y1, z);
    if (full && cap0) for (let i = 0; i < k; i++) tri(c0, r0[(i + 1) % k], r0[i], part, sw);
    if (full && cap1) for (let i = 0; i < k; i++) tri(c1, r1[i], r1[(i + 1) % k], part, sw);
  }
  function box(cx, cy, cz, sx, sy, sz, part, sw = 0, ry = 0, rz = 0) {   // hộp có xoay quanh Y rồi Z (độ)
    const e = new THREE.Euler(0, ry, rz, 'YZX'), c = new THREE.Vector3(cx, cy, cz), V = (x, y, z) => new THREE.Vector3(x * sx / 2, y * sy / 2, z * sz / 2).applyEuler(e).add(c);
    const v = [V(-1, -1, -1), V(1, -1, -1), V(1, 1, -1), V(-1, 1, -1), V(-1, -1, 1), V(1, -1, 1), V(1, 1, 1), V(-1, 1, 1)];
    quad(v[0], v[3], v[2], v[1], part, sw); quad(v[4], v[5], v[6], v[7], part, sw); quad(v[0], v[1], v[5], v[4], part, sw); quad(v[3], v[7], v[6], v[2], part, sw); quad(v[1], v[2], v[6], v[5], part, sw); quad(v[0], v[4], v[7], v[3], part, sw);
  }
  function sphere(cx, cy, cz, r, sy, part, sw, nU = 8, nV = 5) {
    const pt = (u, v) => { const th = u / nU * Math.PI * 2, ph = v / nV * Math.PI; return new THREE.Vector3(cx + Math.sin(ph) * Math.cos(th) * r, cy + Math.cos(ph) * r * sy, cz + Math.sin(ph) * Math.sin(th) * r); };
    for (let v = 0; v < nV; v++) for (let u = 0; u < nU; u++) { const a = pt(u, v), b = pt(u + 1, v), c = pt(u + 1, v + 1), d = pt(u, v + 1); if (v === 0) tri(a, c, d, part, sw); else if (v === nV - 1) tri(a, b, c, part, sw); else quad(a, b, c, d, part, sw); }
  }
  const geo = () => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3));
    g.setAttribute('aPart', new THREE.Float32BufferAttribute(A, 1)); g.setAttribute('aSw', new THREE.Float32BufferAttribute(S, 1)); g.computeBoundingSphere(); return g; };
  return { tri, quad, prism, box, sphere, geo, count: () => P.length / 9 };
}

// tricorn: chóp thấp + vành bẻ lên 3 phía (một lưới liền, dày 1,5 cm); mũi trước hướng +X
function tricorn(b, y, sw) {
  b.prism({ y0: y, y1: y + 0.075, rx0: 0.098, rz0: 0.088, rx1: 0.09, rz1: 0.08, n: 10, part: 5, sw });
  const n = 18, R = (a) => 0.17 + 0.03 * Math.cos(3 * a), H = (a) => 0.055 + 0.045 * Math.max(0, Math.cos(3 * (a - Math.PI / 3)));   // vành tam giác bo, ba "mũi" ở 0°, ±120°; nếp bẻ cao giữa các mũi
  for (let i = 0; i < n; i++) { const a0 = i / n * Math.PI * 2, a1 = (i + 1) / n * Math.PI * 2;
    const p = (a, r, h) => new THREE.Vector3(Math.cos(a) * r, y + h, Math.sin(a) * r);
    const i0 = p(a0, 0.095, 0.005), i1 = p(a1, 0.095, 0.005), o0 = p(a0, R(a0), H(a0)), o1 = p(a1, R(a1), H(a1)), t0 = p(a0, R(a0) - 0.015, H(a0) + 0.012), t1 = p(a1, R(a1) - 0.015, H(a1) + 0.012);
    b.quad(i0, o0, o1, i1, 5, sw); b.quad(i1, t1, t0, i0, 5, sw); b.quad(o0, t0, t1, o1, 1, sw); }   // mép vành: viền lace — màu gi-lê/quần (lính: trắng-ngà; dân: vải nâu)
}
function bodyMesh(kind, lod) {
  const b = builder(), arm = (side) => {   // side +1 phải (+Z), −1 trái
    const sw = side > 0 ? 3 : 4, z = 0.215 * side, holds = (kind === 'order' && side > 0) || (kind === 'march' && side < 0);
    if (holds) {   // tay giữ súng: 'order' tay phải duỗi xuống cạnh báng; 'march' tay trái gập đỡ báng trên vai
      if (kind === 'order') { b.prism({ x: 0.02, z: z + 0.03 * side, y0: 1.12, y1: 1.43, rx0: 0.05, rz0: 0.05, rx1: 0.058, rz1: 0.058, n: 6, part: 0, sw: 0 }); b.prism({ x: 0.04, z: z + 0.06 * side, y0: 0.9, y1: 1.13, rx0: 0.042, rz0: 0.042, rx1: 0.05, rz1: 0.05, n: 6, part: 0, sw: 0 });
        b.box(0.05, 0.86, z + 0.07 * side, 0.07, 0.09, 0.05, 4, 0); }
      else { b.prism({ x: 0.0, z: z, y0: 1.14, y1: 1.43, rx0: 0.05, rz0: 0.05, rx1: 0.058, rz1: 0.058, n: 6, part: 0, sw: 0 }); b.box(0.09, 1.16, z * 0.9, 0.2, 0.08, 0.08, 0, 0, 0, 0.3); b.box(0.17, 1.2, z * 0.85, 0.07, 0.08, 0.06, 4, 0); }
      return; }
    const o = 0.05 * side;   // tay buông hơi dang
    b.prism({ x: 0.0, z: z, y0: 1.13, y1: 1.43, rx0: 0.048, rz0: 0.048, rx1: 0.058, rz1: 0.058, n: lod ? 4 : 6, dx1: 0, part: 0, sw });   // cánh tay trên
    b.prism({ x: 0.03, z: z + o, y0: 0.87, y1: 1.14, rx0: 0.04, rz0: 0.04, rx1: 0.048, rz1: 0.048, n: lod ? 4 : 6, dx1: -0.03, part: 0, sw });   // cẳng tay (hơi ra trước)
    if (!lod) b.prism({ x: 0.03, z: z + o, y0: 0.88, y1: 0.95, rx0: 0.052, rz0: 0.052, n: 6, part: 3, sw });   // cổ tay áo (viền)
    b.box(0.035, 0.82, z + o, 0.06, 0.09, 0.045, 4, sw); };
  const legs = kind !== 'woman';
  if (legs) for (const side of [1, -1]) { const z = 0.095 * side, sw = side > 0 ? 1 : 2, sl = side > 0 ? 6 : 7;
    b.box(0.045, 0.035, z, 0.25, 0.07, 0.1, 6, sl);   // giày
    b.prism({ x: 0, z, y0: 0.06, y1: 0.5, rx0: 0.052, rz0: 0.05, rx1: 0.066, rz1: 0.062, n: lod ? 4 : 6, part: 2, sw: sl });   // ống chân (ghệt/bít tất)
    b.prism({ x: 0, z, y0: 0.48, y1: 0.95, rx0: 0.07, rz0: 0.068, rx1: 0.09, rz1: 0.088, n: lod ? 4 : 6, part: 1, sw }); }   // đùi (quần ống túm)
  else { b.prism({ y0: 0.02, y1: 0.98, rx0: 0.26, rz0: 0.27, rx1: 0.15, rz1: 0.14, n: lod ? 6 : 10, part: 1, sw: 0 }); for (const side of [1, -1]) b.box(0.12, 0.03, 0.08 * side, 0.12, 0.06, 0.08, 6, 0); }
  // thân + áo khoác: thân ellip; vạt sau mở trước (cung 50°–310° quanh +X là trước → mở ở phía trước)
  b.prism({ y0: 0.93, y1: 1.44, rx0: 0.12, rz0: 0.165, rx1: 0.13, rz1: 0.205, n: lod ? 6 : 10, part: kind === 'woman' ? 0 : 0, sw: 0 });
  if (legs && !lod && kind !== 'sailor') b.prism({ y0: 0.52, y1: 0.98, rx0: 0.2, rz0: 0.24, rx1: 0.135, rz1: 0.175, n: 9, a0: 0.75, a1: Math.PI * 2 - 0.75, cap0: false, cap1: false, part: 0, sw: 0 });   // vạt áo
  if (legs && lod && kind !== 'sailor') b.prism({ y0: 0.6, y1: 0.98, rx0: 0.17, rz0: 0.21, rx1: 0.135, rz1: 0.175, n: 6, part: 0, sw: 0 });
  if (!lod) { b.box(0.118, 1.15, 0, 0.03, 0.42, 0.15, kind === 'woman' ? 3 : 1, 0);   // gi-lê lộ trước / yếm khăn
    if (kind === 'order' || kind === 'march') { b.box(0.0, 1.17, 0, 0.27, 0.05, 0.045, 3, 0, 0, 0.82); b.box(0.0, 1.17, 0, 0.27, 0.05, 0.045, 3, 0, 0, -0.82); b.box(-0.02, 1.0, -0.17, 0.16, 0.13, 0.07, 3, 0); }   // dây đeo chéo + hộp đạn (trái-sau)
    if (kind === 'woman') b.prism({ y0: 1.3, y1: 1.46, rx0: 0.15, rz0: 0.22, rx1: 0.12, rz1: 0.2, n: 10, part: 3, sw: 0 }); }   // khăn choàng vai
  for (const s of [1, -1]) arm(s);
  b.prism({ y0: 1.43, y1: 1.53, rx0: 0.05, rz0: 0.05, n: lod ? 4 : 6, part: 4, sw: 5 });   // cổ
  b.sphere(0.012, 1.615, 0, 0.098, 1.18, 4, 5, lod ? 6 : 9, lod ? 4 : 6);   // đầu
  if (!lod) { b.sphere(-0.03, 1.64, 0, 0.096, 1.12, 9, 5, 8, 4); if (kind !== 'woman') b.box(-0.11, 1.53, 0, 0.04, 0.12, 0.04, 9, 5); }   // tóc + đuôi tóc buộc
  if (kind === 'woman') b.prism({ x: -0.02, y0: 1.62, y1: 1.74, rx0: 0.115, rz0: 0.11, rx1: 0.09, rz1: 0.085, n: 8, part: 3, sw: 5 });   // mũ vải (mob cap, màu phụ: vải trắng)
  else if (kind === 'sailor') { b.prism({ y0: 1.69, y1: 1.79, rx0: 0.1, rz0: 0.095, rx1: 0.095, rz1: 0.09, n: 10, part: 5, sw: 5 }); b.prism({ y0: 1.69, y1: 1.705, rx0: 0.16, rz0: 0.155, n: 12, part: 5, sw: 5 }); }
  else if (lod) { b.prism({ y0: 1.69, y1: 1.77, rx0: 0.15, rz0: 0.15, rx1: 0.1, rz1: 0.1, n: 3, part: 5, sw: 5 }); }
  else tricorn(b, 1.685, 5);
  if (kind === 'order') { b.box(0.07, 0.74, 0.3, 0.05, 1.42, 0.04, 7, 0); b.box(0.07, 1.6, 0.3, 0.025, 0.36, 0.025, 8, 0); }   // súng dựng bên phải + lưỡi lê
  if (kind === 'march') { b.box(0.02, 1.68, -0.24, 0.05, 1.42, 0.04, 7, 0, 0, -0.18); b.box(0.15, 2.45, -0.24, 0.022, 0.34, 0.022, 8, 0, 0, -0.18); }   // súng vác vai trái, nghiêng ra sau
  return b.geo();
}

// ---------- vật liệu: màu theo phần + biến dạng chu kỳ đi ----------
const DEFORM = `
  { float ph = aV.x + 6.2831853 * uT * aV.z, g = aV.y, sw = aSw; float s = sin(ph);
  vec3 p = transformed;
  float ang = 0.0; vec3 piv = vec3(0.0);
  if (sw > 0.5 && sw < 2.5) { ang = (sw < 1.5 ? 1.0 : -1.0) * s * 0.42 * g; piv = vec3(0.0, 0.94, 0.0); }
  else if (sw > 5.5 && sw < 7.5) { float sd = sw < 6.5 ? 1.0 : -1.0; ang = sd * s * 0.42 * g; piv = vec3(0.0, 0.94, 0.0); }
  else if (sw > 2.5 && sw < 4.5) { ang = (sw < 3.5 ? -1.0 : 1.0) * s * 0.32 * g + (1.0 - g) * 0.03 * sin(uT * 1.3 + aV.x); piv = vec3(0.0, 1.42, 0.0); }
  if (abs(ang) > 0.0) { vec3 q = p - piv; float c = cos(ang), si = sin(ang); p = piv + vec3(q.x * c - q.y * si, q.x * si + q.y * c, q.z); }
  // gối: ống chân gập thêm khi chân ra sau (pha âm của đùi cùng bên)
  if (sw > 5.5 && sw < 7.5) { float sd = sw < 6.5 ? 1.0 : -1.0, k = max(0.0, -sd * s) * 0.55 * g; vec3 kp = vec3(sin(ang) * 0.46, 0.94 - cos(ang) * 0.46, 0.0); vec3 q = p - kp; float c = cos(-k), si = sin(-k);
    p = kp + vec3(q.x * c - q.y * si, q.x * si + q.y * c, q.z); }
  // đầu quay nhìn quanh khi đứng
  if (sw > 4.5 && sw < 5.5) { float a = (1.0 - g) * 0.45 * sin(uT * 0.35 + aV.x * 3.1) + g * 0.08 * sin(uT * 0.6 + aV.x); float c = cos(a), si = sin(a); p = vec3(p.x * c + p.z * si, p.y, -p.x * si + p.z * c); }
  p.y += g * 0.028 * abs(cos(ph));
  transformed = p; } `;
function patch(sh, U, depth) {
  sh.uniforms.uT = U.uT;
  sh.vertexShader = sh.vertexShader.replace('#include <common>', `#include <common>
    uniform float uT; attribute float aPart; attribute float aSw; attribute vec4 aV; attribute vec3 aC0; attribute vec3 aC1; attribute vec3 aC2; attribute vec3 aC3; attribute vec3 aSk;
    ${depth ? '' : 'varying float vPart; varying float vHair; varying vec3 vC0; varying vec3 vC1; varying vec3 vC2; varying vec3 vC3; varying vec3 vSk;'}`)
    .replace('#include <beginnormal_vertex>', '#include <beginnormal_vertex>\n')
    .replace('#include <begin_vertex>', `#include <begin_vertex>
    ${DEFORM}
    ${depth ? '' : 'vPart = aPart; vHair = aV.w; vC0 = aC0; vC1 = aC1; vC2 = aC2; vC3 = aC3; vSk = aSk;'}`);
  if (!depth) {
    // pháp tuyến biến dạng: tính lại objectNormal trước defaultnormal (begin_vertex đứng sau defaultnormal trong lambert → dùng biến nn qua chèn ở beginnormal)
    sh.vertexShader = sh.vertexShader.replace('#include <beginnormal_vertex>\n', `#include <beginnormal_vertex>
    { float ph = aV.x + 6.2831853 * uT * aV.z, g = aV.y, sw = aSw, s = sin(ph), ang = 0.0;
      if (sw > 0.5 && sw < 2.5) ang = (sw < 1.5 ? 1.0 : -1.0) * s * 0.42 * g; else if (sw > 5.5 && sw < 7.5) ang = (sw < 6.5 ? 1.0 : -1.0) * s * 0.42 * g; else if (sw > 2.5 && sw < 4.5) ang = (sw < 3.5 ? -1.0 : 1.0) * s * 0.32 * g;
      float c = cos(ang), si = sin(ang); objectNormal = vec3(objectNormal.x * c - objectNormal.y * si, objectNormal.x * si + objectNormal.y * c, objectNormal.z); }`);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
      varying float vPart; varying float vHair; varying vec3 vC0; varying vec3 vC1; varying vec3 vC2; varying vec3 vC3; varying vec3 vSk;`)
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', `vec3 pc = vPart < 0.5 ? vC0 : vPart < 1.5 ? vC1 : vPart < 2.5 ? vC2 : vPart < 3.5 ? vC3 : vPart < 4.5 ? vSk : vPart < 5.5 ? vec3(0.012, 0.010, 0.008) : vPart < 6.5 ? vec3(0.010, 0.008, 0.006) : vPart < 7.5 ? vec3(0.13, 0.065, 0.03) : vPart < 8.5 ? vec3(0.32, 0.33, 0.34) : mix(vec3(0.045, 0.03, 0.02), vec3(0.62, 0.6, 0.55), vHair);   // tóc: aV.w 0 tối … 1 rắc bột
      vec4 diffuseColor = vec4( pc, opacity );`);
  }
}
export function makeKit(ctx) {
  const U = ctx.U, kinds = ['order', 'march', 'civ', 'woman', 'sailor'], G = {};
  for (const k of kinds) G[k] = [bodyMesh(k, false), bodyMesh(k, true)];
  const mat = () => { const m = new THREE.MeshLambertMaterial({ color: 0xffffff }); m.onBeforeCompile = (sh) => patch(sh, U, false); m.customProgramCacheKey = () => 'ppl6'; maskify(m, U, 1); return m; };
  const dmat = () => { const m = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }); m.onBeforeCompile = (sh) => patch(sh, U, true); m.customProgramCacheKey = () => 'ppl6d'; return m; };
  return { G, mat, dmat, tris: Object.fromEntries(kinds.map((k) => [k, [G[k][0].attributes.position.count / 3, G[k][1].attributes.position.count / 3]])) };
}

// ---------- tập người: n vị trí do bên gọi cập nhật mỗi khung (set) → tự chia lưới chi tiết / thô theo cỡ điểm ảnh ----------
//  opt: kind, n, lodPx (mặc định 22 px), U (để có uT)
export function makeSet(kit, ctx, { kind = 'civ', n, lodPx = 22 } = {}) {
  const group = new THREE.Group(), meshes = [0, 1].map((l) => { const g = kit.G[kind][l].clone();
    for (const [k, d] of [['aV', 4], ['aC0', 3], ['aC1', 3], ['aC2', 3], ['aC3', 3], ['aSk', 3]]) g.setAttribute(k, new THREE.InstancedBufferAttribute(new Float32Array(n * d), d));
    const m = new THREE.InstancedMesh(g, kit.mat(), n); m.customDepthMaterial = kit.dmat(); m.castShadow = true; m.receiveShadow = true; m.count = 0; m.frustumCulled = false; group.add(m); return m; });
  const st = new Array(n);   // trạng thái mỗi người: {look, v:[ph, g, f, 0], c:[c0,c1,c2,c3], sk}
  const cvt = (hex, k = 1) => { const c = new THREE.Color(hex); return [c.r * k, c.g * k, c.b * k]; };
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), Y = new THREE.Vector3(0, 1, 0), v = new THREE.Vector3(), sc = new THREE.Vector3();
  let used = [0, 0];
  return { group, meshes, kind,
    // gán diện mạo người i (một lần): uniform = khoá UNIFORMS, R = rng, opt {acc: chỉ số màu phụ cố định cho cả khối, gait, freq}
    look(i, uni, R, o = {}) { const P = UNIFORMS[uni] || UNIFORMS.civ, pick = (a) => a[Math.floor(R() * a.length)], k = 0.9 + 0.18 * R();
      const hairPowder = /inf|art/.test(uni) && R() < 0.75;
      st[i] = { v: [R() * 6.283, o.gait ?? 0, o.freq ?? (0.85 + 0.3 * R()), hairPowder ? 1 : (R() < 0.3 ? 0.25 : 0)], c0: cvt(pick(P.coat), k), c1: cvt(pick(P.small), 0.92 + 0.12 * R()), c2: cvt(pick(P.legs)), c3: cvt(o.acc != null ? P.acc[o.acc % P.acc.length] : pick(P.acc)), sk: cvt(pick(SKIN)) }; },
    setGait(i, g, f) { st[i].v[1] = g; if (f) st[i].v[2] = f; },
    // đặt người i: vị trí ENU [e, y, n], hướng (rad, từ Đông ngược chiều kim đồng hồ), hiện/ẩn, cỡ — gọi begin() trước, end() sau
    begin() { used = [0, 0]; },
    put(i, e, y, n_, hd, show = true, k = 1) { if (!show) return; const cam = ctx.cam, d = cam ? Math.hypot(e - cam.position.x, y - cam.position.y, -n_ - cam.position.z) : 0;
      const px = cam ? 1.75 * k * (ctx.H || 1080) / (2 * Math.tan(cam.fov * Math.PI / 360) * Math.max(d, 1)) : 99, l = px < lodPx ? 1 : 0, M = meshes[l], j = used[l]++;
      v.set(e, y, -n_); q.setFromAxisAngle(Y, hd); sc.set(k, k * (0.96 + 0.08 * ((i * 0.618) % 1)), k); m4.compose(v, q, sc); M.setMatrixAt(j, m4);
      const s = st[i], g = M.geometry.attributes; g.aV.setXYZW(j, ...s.v); g.aC0.setXYZ(j, ...s.c0); g.aC1.setXYZ(j, ...s.c1); g.aC2.setXYZ(j, ...s.c2); g.aC3.setXYZ(j, ...s.c3); g.aSk.setXYZ(j, ...s.sk);
      return px; },
    end() { for (let l = 0; l < 2; l++) { const M = meshes[l]; M.count = used[l]; M.instanceMatrix.needsUpdate = true; for (const k of ['aV', 'aC0', 'aC1', 'aC2', 'aC3', 'aSk']) M.geometry.attributes[k].needsUpdate = true; } return used[0] + used[1]; },
    stat: () => ({ chi_tiet: used[0], tho: used[1] }) };
}

// màu cũ (A-lite, theo phe/khối) → bảng quân phục V6
export function uniOf(sp) {
  if (sp.uni) return sp.uni; if (sp.side === 'es') return 'es_inf'; if (sp.side === 'fr') return 'fr_inf'; if (sp.side === 'gb') return 'gb_inf';
  const c = (sp.color || '').toLowerCase(); if (['#2f3d5c', '#3b4a66', '#262f49', '#2b3552'].includes(c)) return 'gb_art'; if (['#a8392c', '#b03a2e', '#a8402e', '#9b2a22'].includes(c)) return 'gb_inf';
  return 'civ';
}
const ORD = { gb_inf: 'gb_inf', gb_art: 'gb_art', es_inf: 'es_inf', fr_inf: 'fr_inf' };
// người đi bộ / đám đông: màu áo cũ → (kiểu lưới, bảng): đỏ → lính Anh không súng (đi lại trong phố), lam → pháo binh, còn lại dân thường (20 % nữ khi cho phép)
export function walkerLook(col, R, women = true) { const c = (col || '').toLowerCase();
  if (['#b03a2e', '#a8402e', '#a8392c', '#9b2a22', '#b8402f'].includes(c)) return ['civ', 'gb_inf'];
  if (['#2f3d5c', '#3b4a66', '#3b4a5c', '#262f49'].includes(c)) return ['civ', 'gb_art'];
  return women && R() < 0.2 ? ['woman', 'woman'] : ['civ', 'civ']; }
export { ORD };

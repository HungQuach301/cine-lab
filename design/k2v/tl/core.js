// K2V · XƯƠNG SỐNG THỜI GIAN (tl) — đồ nghề chung (V5b-1, 16/10/2026). Toạ độ cảnh: x = Đông, y = cao, z = −Bắc (m quanh gốc gói cảnh).
// Chỉ IMPORT mã có sẵn (three.js của design/cong3/shared, post.js); không sửa design/k2v/*.js hiện có (T2 đang dựng).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
export { THREE };
export const cl = (u) => Math.max(0, Math.min(1, u));
export const ease = (u) => { u = cl(u); return u * u * (3 - 2 * u); };
export const lerp = (a, b, u) => a + (b - a) * u;
export const V3 = (e, y, n) => new THREE.Vector3(e, y, -n);   // ENU → three
// nội suy theo mốc [[t, v], …] (tuyến tính từng đoạn) — dùng cho năm theo thời gian
export function track(K) { return (t) => { if (t <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (t <= K[i][0]) { const [t0, a] = K[i - 1], [t1, b] = K[i]; return a + (b - a) * (t - t0) / Math.max(1e-6, t1 - t0); } return K[K.length - 1][1]; }; }
// năm mã hoá 16 bit trong 2 kênh 8 bit (hi, lo) — khớp build_scene.py enc()
export const GLSL_YEAR = `float decYear(vec2 hl){ return floor(hl.x * 255.0 + 0.5) * 256.0 + floor(hl.y * 255.0 + 0.5); }`;
export const loadJSON = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error('không tải được ' + u); return r.json(); };
export const loadF32 = async (u) => new Float32Array(await (await fetch(u)).arrayBuffer());
export const loadImg = (u) => new Promise((ok, ko) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => ko(new Error('ảnh ' + u)); im.src = u; });
export async function tex(u, { srgb = true, nearest = false, flipY = true } = {}) {
  const im = await loadImg(u); const t = new THREE.Texture(im); t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  t.flipY = flipY; t.anisotropy = 8; if (nearest) { t.magFilter = t.minFilter = THREE.NearestFilter; t.generateMipmaps = false; } t.needsUpdate = true; return t;
}
// băm xác định (không Math.random: khung tất định)
export function rng(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
export const GLSL_NOISE = `
float h21(vec2 p){ p = fract(p * vec2(233.34, 851.73)); p += dot(p, p + 23.45); return fract(p.x * p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(h21(i), h21(i + vec2(1, 0)), f.x), mix(h21(i + vec2(0, 1)), h21(i + vec2(1, 1)), f.x), f.y); }
float fbm(vec2 p){ float a = 0.5, s = 0.0; for (int i = 0; i < 4; i++){ s += a * vn(p); p = p * 2.03 + 17.1; a *= 0.5; } return s; }`;

// Kết cấu nhiễu NƯỚNG SẴN (kỹ thuật tối ưu V5b-1: thay fbm thủ tục 4 tầng trong shader bằng 1 lần lấy mẫu; lặp liền mép, có mipmap).
// R, G, B, A = fbm 4 tầng ở 4 tần số khác nhau (pha khác nhau) — đọc bằng texture(tNoise, p).r … ; tất định (rng cố định).
let _noise = null;
export function noiseTex(N = 256) {
  if (_noise) return _noise; const R = rng(91), d = new Uint8Array(N * N * 4);
  const lat = (g) => { const L = new Float32Array(g * g); for (let i = 0; i < g * g; i++) L[i] = R(); return L; };
  const vn = (L, g, x, y) => { const xi = Math.floor(x) % g, yi = Math.floor(y) % g, xf = x - Math.floor(x), yf = y - Math.floor(y), sx = xf * xf * (3 - 2 * xf), sy = yf * yf * (3 - 2 * yf);
    const a = L[yi * g + xi], b = L[yi * g + (xi + 1) % g], c = L[((yi + 1) % g) * g + xi], e = L[((yi + 1) % g) * g + (xi + 1) % g]; return (a + (b - a) * sx) * (1 - sy) + (c + (e - c) * sx) * sy; };
  for (let ch = 0; ch < 4; ch++) { const base = [4, 8, 16, 32][ch], layers = [0, 1, 2, 3].map((o) => ({ g: base << o, L: lat(base << o) }));
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { let s = 0, a = 0.5, n = 0;
      for (const { g, L } of layers) { s += a * vn(L, g, x / N * g, y / N * g); n += a; a *= 0.5; } d[(y * N + x) * 4 + ch] = Math.round(255 * s / n); } }
  const t = new THREE.DataTexture(d, N, N, THREE.RGBAFormat); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.magFilter = THREE.LinearFilter; t.minFilter = THREE.LinearMipmapLinearFilter; t.generateMipmaps = true; t.needsUpdate = true;
  return (_noise = t);
}

// V5b-1b · mặt nạ NỘI DUNG (đo "≥ 40 % khung là nội dung có nghĩa"): khi uMask = 1, vật liệu xuất màu cờ (1 = nội dung: toà, hero, tường, đường, xe/người; 0 = nền)
// V5b-2a: hid > 0 = id hero (kênh B = hid/255) — đo hero_pct theo id ở page.js contentMask
// V6: uMask = 2 → LƯỢT PHÁP TUYẾN cho SSAO (light6.js): vật liệu có pháp tuyến xuất pháp tuyến không gian nhìn; vật liệu không pháp tuyến (Basic, Sprite) bị bỏ khỏi lượt
// V6 bước 7: uMask = 3 → LƯỢT ALBEDO (diffuseColor tuyến tính, không chiếu sáng/sương) cho bản Cycles (export6.js)
export const N6 = (mat) => (mat.isMeshLambertMaterial || mat.isMeshStandardMaterial || mat.isMeshPhongMaterial) ? 'if (uMask > 2.5) gl_FragColor = vec4(diffuseColor.rgb, 1.0); else if (uMask > 1.5) gl_FragColor = vec4(normalize(normal) * 0.5 + 0.5, 1.0); else ' : 'if (uMask > 2.5) gl_FragColor = vec4(diffuseColor.rgb, 1.0); else if (uMask > 1.5) discard; else ';
export function maskify(mat, U, v, hid = 0) {
  if (mat.userData.masked) return; mat.userData.masked = true; const prev = mat.onBeforeCompile;
  const key0 = mat.customProgramCacheKey ? mat.customProgramCacheKey() : (prev ? prev.toString() : ''); mat.customProgramCacheKey = () => key0 + '|mask' + v + '|h' + hid;   // khoá bộ đệm chương trình: không để vật liệu khác dùng nhầm shader (lỗi phát hiện 16/10)
  mat.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r); sh.uniforms.uMask = U.uMask;
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uMask;')
      .replace('#include <dithering_fragment>', `#include <dithering_fragment>\n ${N6(mat)}if (uMask > 0.5) gl_FragColor = vec4(${v ? '1.0, 0.0, ' + (hid / 255).toFixed(6) : '0.0, 0.0, 0.0'}, 1.0);`); };
  mat.needsUpdate = true;
}

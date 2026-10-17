// K2V tl · LUT A "k2-a-thep-lanh" (V5a, chủ dự án chọn A) áp trong grade() của đường ống post.js — CHỈ lên cảnh 3D tự nhiên;
// chữ, thẻ, ảnh sepia vẽ sau ở lớp 2D nên không qua LUT (lệnh 16/10: không áp sepia). .cube 33³ → Data3DTexture (lọc tuyến tính).
import { THREE } from './core.js';
export async function loadCube(url) {
  const t = await (await fetch(url)).text(); let N = 0; const v = [];
  for (const ln of t.split('\n')) { const s = ln.trim(); if (!s || s[0] === '#') continue; if (s.startsWith('LUT_3D_SIZE')) { N = +s.split(/\s+/)[1]; continue; } if (/^[A-Z_]/.test(s)) continue; v.push(...s.split(/\s+/).map(Number)); }
  if (v.length !== N * N * N * 3) throw new Error(`LUT lỗi: ${v.length / 3} điểm ≠ ${N}³`);
  const d = new Uint8Array(N * N * N * 4); for (let i = 0; i < N * N * N; i++) { d[i * 4] = Math.round(Math.min(1, Math.max(0, v[i * 3])) * 255); d[i * 4 + 1] = Math.round(Math.min(1, Math.max(0, v[i * 3 + 1])) * 255); d[i * 4 + 2] = Math.round(Math.min(1, Math.max(0, v[i * 3 + 2])) * 255); d[i * 4 + 3] = 255; }
  const tx = new THREE.Data3DTexture(d, N, N, N); tx.format = THREE.RGBAFormat; tx.type = THREE.UnsignedByteType; tx.minFilter = tx.magFilter = THREE.LinearFilter;
  tx.wrapS = tx.wrapT = tx.wrapR = THREE.ClampToEdgeWrapping; tx.unpackAlignment = 1; tx.needsUpdate = true; return { tex: tx, N };
}
// .cube: R chạy nhanh nhất → toạ độ texture (r, g, b) = (x, y, z)
export const GRADE_GLSL = `
uniform highp sampler3D tLut; uniform float uLutK, uLutN, uVig, uAA, uLutMode, uVib;
vec3 aaS(vec2 p){ return pow(tonemap(max(texture(tAcc, p).rgb, 0.0)), vec3(1.0 / 2.2)); }
vec3 aaFilter(vec3 c, vec2 uv){ vec2 px = 1.0 / res; vec3 a = aaS(uv + vec2(px.x, 0.0)), b = aaS(uv - vec2(px.x, 0.0)), d = aaS(uv + vec2(0.0, px.y)), e = aaS(uv - vec2(0.0, px.y));
  vec3 W3 = vec3(0.299, 0.587, 0.114); float lc = dot(c, W3), la = dot(a, W3), lb = dot(b, W3), ld = dot(d, W3), le = dot(e, W3);
  float mx = max(lc, max(max(la, lb), max(ld, le))), mn = min(lc, min(min(la, lb), min(ld, le))), rg = mx - mn; if (rg < max(0.07, mx * 0.16)) return c;
  float h = abs(la + lb - 2.0 * lc), v = abs(ld + le - 2.0 * lc); vec3 bl = h > v ? (a + b) * 0.5 : (d + e) * 0.5; return mix(c, bl, clamp(rg * 1.6, 0.0, 0.55)); }
vec3 grade(vec3 c, vec2 uv){
  if (uAA > 0.5) c = aaFilter(c, uv);   // khung SPP1 (bay nhanh): lọc cạnh như k2v V3 E6b
  vec3 q = clamp(c, 0.0, 1.0) * ((uLutN - 1.0) / uLutN) + 0.5 / uLutN; float Y0 = dot(c, vec3(0.2126, 0.7152, 0.0722));
  // V5b-1b: uLutMode 1 = LUT chỉ áp vùng tối (làm lạnh nhẹ bóng), vùng trung/sáng giữ nguyên → không làm nhạt
  float wl = uLutMode > 0.5 ? 1.0 - smoothstep(0.10, 0.42, Y0) : 1.0; c = mix(c, texture(tLut, q).rgb, uLutK * wl);
  // vibrance (bù phần ACES làm nhạt): tăng bão hoà màu nhạt nhiều hơn màu đã đậm, giữ độ sáng
  { float Y = dot(c, vec3(0.2126, 0.7152, 0.0722)), s = max(c.r, max(c.g, c.b)) - min(c.r, min(c.g, c.b)); c = max(mix(vec3(Y), c, 1.0 + uVib * (1.0 - s)), 0.0); }
  vec2 d = (uv - 0.5) * vec2(1.0, 0.82); c *= mix(1.0, 1.0 - uVig, smoothstep(0.30, 0.78, length(d)));
  return c; }`;

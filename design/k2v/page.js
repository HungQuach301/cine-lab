// KÊNH 2 · trang render cho module hình k2v (map, chart3d, photo). Driver: scripts/k2/hero.js (tự chọn trang này khi design/k2v/<tệp>.js tồn tại).
// Cùng đường ống hậu kỳ với design/ll-hero/k2page.js (tone map ACES, grade, grain, tích luỹ SPP có jitter) + điểm neo màn hình có che khuất:
//   anchors: {tên: Vector3 | () => Vector3 | null}; null = bị che (mặt sau địa cầu…) → ghi thấy = 0.
// Thư viện địa lý (d3-array, d3-geo, topojson-client: bản UMD trong design/k2v/node_modules) nạp khi module khai báo `export const NEEDS = ['geo']`.
// Tài sản ngoài git (Blue Marble, ảnh LoC, trang PDF) phục vụ qua /cache/… (hero.js ánh xạ tới $K2V_CACHE).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { GRADES } from '/ll-hero/kit.js';
import { loadCube } from './tl/lut.js';   // V5b-2b (V5B2A §8.7): LUT A cho module k2v — CHỈ khi cảnh khai opt.lut (mặc định tắt: khung cũ không đổi)

const GRADE = `
uniform float gCanvas, gVig, gLift, gSat; uniform vec3 gShadowTint, gHiTint;
uniform float uAA;
uniform highp sampler3D tLut; uniform float uLutOn, uLutK, uLutN, uLutMode, uVib;
// V3 (E6b): lọc khử răng cưa cho khung dựng SPP1 (relief, máy > spp1Km): phát hiện cạnh theo độ chênh sáng 4 lân cận, trộn về trung bình lân cận theo độ mạnh cạnh.
// Đặt trong grade() của trang k2v (đọc được tAcc/res), không sửa post.js dùng chung với LL.
vec3 aaS(vec2 p){ return pow(tonemap(max(texture(tAcc, p).rgb, 0.0)), vec3(1.0 / 2.2)); }
vec3 aaFilter(vec3 c, vec2 uv){ vec2 px = 1.0 / res; vec3 a = aaS(uv + vec2(px.x, 0.0)), b = aaS(uv - vec2(px.x, 0.0)), d = aaS(uv + vec2(0.0, px.y)), e = aaS(uv - vec2(0.0, px.y));
  vec3 W3 = vec3(0.299, 0.587, 0.114); float lc = dot(c, W3), la = dot(a, W3), lb = dot(b, W3), ld = dot(d, W3), le = dot(e, W3);
  float mx = max(lc, max(max(la, lb), max(ld, le))), mn = min(lc, min(min(la, lb), min(ld, le))), rg = mx - mn;
  if (rg < max(0.07, mx * 0.16)) return c;   /* chỉ cạnh tương phản cao (mép vật, viền, tuyến); vân địa hình nhẹ giữ nguyên */
  float h = abs(la + lb - 2.0 * lc), v = abs(ld + le - 2.0 * lc); vec3 blur = h > v ? (a + b) * 0.5 : (d + e) * 0.5;   /* trộn theo hướng vuông góc với cạnh */
  return mix(c, blur, clamp(rg * 1.6, 0.0, 0.55)); }
float ch21(vec2 p){ p = fract(p*vec2(233.34, 851.73)); p += dot(p, p+23.45); return fract(p.x*p.y); }
float cvn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
  return mix(mix(ch21(i), ch21(i+vec2(1,0)), f.x), mix(ch21(i+vec2(0,1)), ch21(i+vec2(1,1)), f.x), f.y); }
vec3 grade(vec3 c, vec2 uv){
  if (uAA > 0.5) c = aaFilter(c, uv);
  float L = dot(c, vec3(0.2126,0.7152,0.0722));
  c = mix(vec3(L), c, gSat);
  float sh = 1.0 - smoothstep(0.0, 0.45, L), hi = smoothstep(0.55, 1.0, L);
  c += gShadowTint * sh * gLift;
  c = mix(c, c * gHiTint, hi * 0.5);
  vec2 p = uv * res;
  float weave = sin(p.x * 2.09) * sin(p.y * 2.09 + 1.3 * sin(p.x * 0.05));
  float tooth = cvn(p / 7.0) - 0.5;
  float midw = 4.0 * L * (1.0 - L);
  c *= 1.0 + gCanvas * (0.55 * weave + 0.9 * tooth) * (0.35 + 0.65 * midw);
  if (uLutOn > 0.5) {   // LUT A (uLutMode 1: chỉ vùng tối) + vibrance — như design/k2v/tl/lut.js (V5b-1b, chọn bằng số đo)
    vec3 qq = clamp(c, 0.0, 1.0) * ((uLutN - 1.0) / uLutN) + 0.5 / uLutN; float Y0 = dot(c, vec3(0.2126, 0.7152, 0.0722));
    float wl = uLutMode > 0.5 ? 1.0 - smoothstep(0.10, 0.42, Y0) : 1.0; c = mix(c, texture(tLut, qq).rgb, uLutK * wl);
    float Y = dot(c, vec3(0.2126, 0.7152, 0.0722)), s = max(c.r, max(c.g, c.b)) - min(c.r, min(c.g, c.b)); c = max(mix(vec3(Y), c, 1.0 + uVib * (1.0 - s)), 0.0); }
  vec2 q = (uv - 0.5) * vec2(1.0, 0.82);
  c *= mix(1.0, 1.0 - gVig, smoothstep(0.28, 0.75, length(q)));
  return c;
}`;
const LUT0 = () => { const t = new THREE.Data3DTexture(new Uint8Array(8 * 4).fill(255), 2, 2, 2); t.needsUpdate = true; return t; };   // ô trống khi tắt LUT (sampler phải có kết cấu)
// tông riêng cho đồ hoạ thông tin k2v: ít vân vải (chữ/viền sắc), vignette nhẹ
const K2V_GRADES = {
  info: { gCanvas: 0.004, gVig: 0.22, gLift: 0.015, gSat: 1.0, gShadowTint: [0.30, 0.38, 0.95], gHiTint: [1.0, 0.99, 0.96] },
  map: { gCanvas: 0.003, gVig: 0.16, gLift: 0.0, gSat: 1.0, gShadowTint: [0.30, 0.38, 0.95], gHiTint: [1.0, 1.0, 1.0] },
  archive: { gCanvas: 0.010, gVig: 0.30, gLift: 0.02, gSat: 0.9, gShadowTint: [0.45, 0.38, 0.32], gHiTint: [1.03, 0.98, 0.90] },
};
const classic = (src) => new Promise((ok, ko) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = () => ko(new Error('không nạp được ' + src)); document.head.appendChild(s); });
let pipe, cur, cfg;
window.setup = async (c) => {
  cfg = c; const [file, name] = c.hero.split('/');
  const mod = await import(`./${file}.js`); const H = mod.HEROES[name]; if (!H) throw new Error('không có cảnh ' + c.hero);
  if ((mod.NEEDS || []).includes('geo') && !window.d3) {
    for (const p of ['d3-array/dist/d3-array.min.js', 'd3-geo/dist/d3-geo.min.js', 'topojson-client/dist/topojson-client.min.js']) await classic('/k2v/node_modules/' + p);
  }
  const renderer = createRenderer(c.W, c.H);   // module có thể khai TONE (GLSL tonemap riêng, vd. relief giữ bảng màu bản đồ); mặc định ACES như cũ renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const lut = c.opt && c.opt.lut ? await loadCube('/cache/lut/' + c.opt.lut + '.cube') : null;   // .cube ở $K2V_CACHE/lut (scripts/k2tl/fetch_sources.py chép cùng tệp)
  const uniforms = { tLut: { value: lut ? lut.tex : LUT0() }, uLutOn: { value: lut ? 1 : 0 }, uLutK: { value: (c.opt || {}).lutK ?? 1 }, uLutN: { value: lut ? lut.N : 2 }, uLutMode: { value: (c.opt || {}).lutMode ?? 1 }, uVib: { value: lut ? ((c.opt || {}).vib ?? 0.35) : 0 }, uAA: { value: 0 }, gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, c.W, c.H, { exposure: 1.0, gradeGLSL: GRADE, uniforms, ...(mod.TONE ? { toneGLSL: mod.TONE } : {}) });
  cur = await H({ W: c.W, H: c.H, dur: c.dur, v: c.variant || 'a', opt: c.opt || {}, renderer });
  const gr = (c.opt && c.opt.grade) || cur.grade || 'info', g = typeof gr === 'string' ? (K2V_GRADES[gr] || GRADES[gr]) : gr, u = pipe.outMat.uniforms;
  if (c.opt && c.opt.exposure) cur.exposure = c.opt.exposure;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
  return { ok: true, maxTex: renderer.capabilities.maxTextureSize };
};
window.renderFrame = async (f) => { const t = f / 24; cur.update(t, f); pipe.outMat.uniforms.uExp.value = cur.exposure ?? 1.0; const n = cur.sppNow || cfg.spp || 1; pipe.outMat.uniforms.uAA.value = cur.sppNow === 1 && (cfg.spp || 1) > 1 ? 1 : 0;   /* V3 (E6b): module có thể hạ SPP cho khung này (relief máy xa) → bật lọc khử răng cưa */
  return { ms: pipe.accumulate(cur.scene, cur.cam, n, cur.onSample || null) }; };
window.finalize = (f) => pipe.finalize(f);
window.anchorsAt = () => { if (!cur.anchors) return null; const out = {}, v = new THREE.Vector3();
  for (const [k, a] of Object.entries(cur.anchors)) { const p = typeof a === 'function' ? a() : a; if (!p) { out[k] = [0, 0, 0]; continue; } v.copy(p).project(cur.cam);
    const vis = v.z < 1 && v.z > -1 && Math.abs(v.x) <= 1.05 && Math.abs(v.y) <= 1.05 ? 1 : 0; out[k] = [+((v.x + 1) / 2).toFixed(4), +((1 - v.y) / 2).toFixed(4), vis]; }
  return out; };

// KÊNH 2 · trang render cho module hình k2v (map, chart3d, photo). Driver: scripts/k2/hero.js (tự chọn trang này khi design/k2v/<tệp>.js tồn tại).
// Cùng đường ống hậu kỳ với design/ll-hero/k2page.js (tone map ACES, grade, grain, tích luỹ SPP có jitter) + điểm neo màn hình có che khuất:
//   anchors: {tên: Vector3 | () => Vector3 | null}; null = bị che (mặt sau địa cầu…) → ghi thấy = 0.
// Thư viện địa lý (d3-array, d3-geo, topojson-client: bản UMD trong design/k2v/node_modules) nạp khi module khai báo `export const NEEDS = ['geo']`.
// Tài sản ngoài git (Blue Marble, ảnh LoC, trang PDF) phục vụ qua /cache/… (hero.js ánh xạ tới $K2V_CACHE).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { GRADES } from '/ll-hero/kit.js';

const GRADE = `
uniform float gCanvas, gVig, gLift, gSat; uniform vec3 gShadowTint, gHiTint;
float ch21(vec2 p){ p = fract(p*vec2(233.34, 851.73)); p += dot(p, p+23.45); return fract(p.x*p.y); }
float cvn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
  return mix(mix(ch21(i), ch21(i+vec2(1,0)), f.x), mix(ch21(i+vec2(0,1)), ch21(i+vec2(1,1)), f.x), f.y); }
vec3 grade(vec3 c, vec2 uv){
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
  vec2 q = (uv - 0.5) * vec2(1.0, 0.82);
  c *= mix(1.0, 1.0 - gVig, smoothstep(0.28, 0.75, length(q)));
  return c;
}`;
// tông riêng cho đồ hoạ thông tin k2v: ít vân vải (chữ/viền sắc), vignette nhẹ
const K2V_GRADES = {
  info: { gCanvas: 0.004, gVig: 0.22, gLift: 0.015, gSat: 1.0, gShadowTint: [0.30, 0.38, 0.95], gHiTint: [1.0, 0.99, 0.96] },
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
  const renderer = createRenderer(c.W, c.H); renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, c.W, c.H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  cur = await H({ W: c.W, H: c.H, dur: c.dur, v: c.variant || 'a', opt: c.opt || {}, renderer });
  const gr = (c.opt && c.opt.grade) || cur.grade || 'info', g = typeof gr === 'string' ? (K2V_GRADES[gr] || GRADES[gr]) : gr, u = pipe.outMat.uniforms;
  if (c.opt && c.opt.exposure) cur.exposure = c.opt.exposure;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
  return { ok: true, maxTex: renderer.capabilities.maxTextureSize };
};
window.renderFrame = async (f) => { const t = f / 24; cur.update(t, f); pipe.outMat.uniforms.uExp.value = cur.exposure ?? 1.0; return { ms: pipe.accumulate(cur.scene, cur.cam, cfg.spp || 1, cur.onSample || null) }; };
window.finalize = (f) => pipe.finalize(f);
window.anchorsAt = () => { if (!cur.anchors) return null; const out = {}, v = new THREE.Vector3();
  for (const [k, a] of Object.entries(cur.anchors)) { const p = typeof a === 'function' ? a() : a; if (!p) { out[k] = [0, 0, 0]; continue; } v.copy(p).project(cur.cam);
    const vis = v.z < 1 && v.z > -1 && Math.abs(v.x) <= 1.05 && Math.abs(v.y) <= 1.05 ? 1 : 0; out[k] = [+((v.x + 1) / 2).toFixed(4), +((1 - v.y) / 2).toFixed(4), vis]; }
  return out; };

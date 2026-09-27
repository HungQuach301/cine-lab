// Cine Lab · Cổng 3 vòng 1 · Hướng mỹ thuật C — "Painted Glow" (luminist / tonalist).
// Trang cho shared/render_still.js. Khung: s1_opening, s5_shadows.
// Tuỳ chọn --args: {"nopaint":1} bỏ lớp vẽ; {"measure":1} đo tỷ lệ key : tràn tại vách (s5), in ra console.
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '../shared/post.js';
import { createPaint } from './paint.js';
import { buildS5, U as U5 } from './s5.js';
import { buildS1 } from './s1.js';

let W, H, cfg, renderer, pipe, paint, sheets, cur = null;

// Grade trong không gian hiển thị (sau tone map): cong mềm vùng tối về tím-xanh, vùng sáng ngả kem;
// vân canvas rất nhẹ (tĩnh theo khung); làm tối mép kiểu tranh (vignette elip mềm).
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
  // vân canvas: sợi ngang/dọc ~3 px + nhấp nhô thô của lớp lót
  vec2 p = uv * res;
  float weave = sin(p.x * 2.09) * sin(p.y * 2.09 + 1.3 * sin(p.x * 0.05));
  float tooth = cvn(p / 7.0) - 0.5;
  float midw = 4.0 * L * (1.0 - L);
  c *= 1.0 + gCanvas * (0.55 * weave + 0.9 * tooth) * (0.35 + 0.65 * midw);
  vec2 q = (uv - 0.5) * vec2(1.0, 0.82);
  c *= mix(1.0, 1.0 - gVig, smoothstep(0.28, 0.75, length(q)));
  return c;
}`;

async function build(name) {
  if (name === 's5_shadows') {
    const r = await buildS5(sheets[0], sheets[1], cfg.dbg || {});
    return { ...r, grade: { gCanvas: 0.012, gVig: 0.30, gLift: 0.018, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [0.985, 0.995, 1.02] },
      paintP: { rNear: 7.0, rFar: 9.0, dNear: 6, dFar: 12, impScale: 0.5, stroke: 0.045, preAmp: 0.16, wob: 3.5, preLen: 46, preWid: 6 } };
  }
  if (name === 's1_opening') {
    const r = await buildS1(sheets[0], H, cfg.dbg || {});
    return { ...r, grade: { gCanvas: 0.012, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.975, 0.93] },
      paintP: { rNear: 3.0, rFar: 6.5, dNear: 30, dFar: 400, impScale: 0.4, stroke: 0.035, halation: 0.16, bloomWide: 0.07 } };
  }
  throw new Error('khung không có: ' + name);
}

// Dựng cảnh (tài sản, hình học, biên dịch shader) thuộc thiết lập của shot → làm trong setup (driver đo riêng setup_s).
// renderFrame chỉ đo phần render một khung: tích luỹ mẫu + lớp vẽ + pass cuối.
const built = {};
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  sheets = await Promise.all(['model-sheet/ida.json', 'model-sheet/cas.json'].map((p) => fetch('/' + p).then((r) => r.json())));
  renderer = createRenderer(W, H);
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 },
    gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  const only = c.frame ? [c.frame] : ['s1_opening', 's5_shadows'];
  for (const name of only) { try {
    const b = built[name] = await build(name); renderer.compile(b.scene, b.cam);
    // khởi động: 1 mẫu + lớp vẽ để tải texture, biên dịch shader, cấp phát RT (chi phí một lần mỗi shot, không phải mỗi khung)
    b.paint = createPaint(renderer, W, H, pipe, { ...b.paintP, ...(c.paint || {}) });
    pipe.accumulate(b.scene, b.cam, 1, b.onSample); b.paint.apply(b.scene, b.cam); readOne(b.paint.outRT); pipe.finalize(0);
  } catch (e) { console.log('setup ' + name + ': ' + e.message); } }
};

window.renderFrame = async (name, samples) => {
  cur = built[name] || (built[name] = await build(name));
  const g = cur.grade, u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat;
  u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
  paint = cur.paint || (cur.paint = createPaint(renderer, W, H, pipe, { ...cur.paintP, ...(cfg.paint || {}) }));
  const t0 = performance.now();
  const ms = pipe.accumulate(cur.scene, cur.cam, samples, cur.onSample);
  if (cfg.prof) { renderer.getContext().finish(); readOne(pipe.accRT); }
  const t1 = performance.now();
  if (cfg.prof) paint.setProf(true);
  if (!cfg.nopaint) paint.apply(cur.scene, cur.cam); else paint.bypass();
  if (cfg.prof) { readOne(paint.outRT); console.log(`PROF accum ${(t1 - t0).toFixed(0)} ms, paint ${(performance.now() - t1).toFixed(0)} ms ` + JSON.stringify(Object.fromEntries(Object.entries(paint.prof).map(([k, v]) => [k, Math.round(v)])))); }
  if (cfg.where && cur.chIda) { const v = new THREE.Vector3(); cur.chIda.root.getWorldPosition(v); const d = v.distanceTo(cur.cam.position); v.project(cur.cam); console.log('IDA px ' + ((v.x * 0.5 + 0.5) * W).toFixed(0) + ',' + ((0.5 - v.y * 0.5) * H).toFixed(0) + ' dist ' + d.toFixed(1)); }
  if (cfg.measure && name === 's5_shadows') console.log('MEASURE ' + JSON.stringify(measureS5(samples)));
  return { accum_ms: ms };
};
window.finalize = (f) => pipe.finalize(f);
const _one = new Float32Array(4);
function readOne(rt) { renderer.readRenderTargetPixels(rt, 0, 0, 1, 1, _one); }

// Đo tỷ lệ key : tràn tại vách trong (tuyến tính, trước tone map): render lại với (a) đủ đèn, (b) tắt đèn lồng.
// Vùng đo: dải vách lộ sáng (không bị người che) ở hai bên và phía trên hai bóng.
function measureS5(samples) {
  const { scene, cam, onSample, spot } = cur;
  const rt = pipe.accRT; const px = new Float32Array(W * H * 4);
  const read = () => { renderer.readRenderTargetPixels(rt, 0, 0, W, H, px); return px.slice(); };
  // chiếu điểm thế giới → pixel
  const pix = (x, y, z) => { const v = new THREE.Vector3(x, y, z).project(cam); return [Math.round((v.x * 0.5 + 0.5) * W), Math.round((v.y * 0.5 + 0.5) * H)]; };
  const lum = (a, x, y) => { let s = 0, n = 0; for (let dy = -4; dy <= 4; dy++) for (let dx = -4; dx <= 4; dx++) { const i = ((y + dy) * W + x + dx) * 4; s += 0.2126 * a[i] + 0.7152 * a[i + 1] + 0.0722 * a[i + 2]; n++; } return s / n; };
  const pts = { wall_lit_L: [-1.3, 1.2, 0.001], wall_lit_R: [1.3, 1.0, 0.001], wall_lit_mid_high: [0.0, 2.9, 0.001], wall_top: [0, 3.6, 0.001], wall_in_shadow_Ida_head: [-0.62, 2.35, 0.001], wall_in_shadow_Cas_head: [0.62, 1.95, 0.001] };
  const spr = []; scene.traverse((o) => { if (o.isSprite && o.visible) { spr.push(o); o.visible = false; } }); // quầng trong không khí không phải ánh sáng trên vách
  pipe.accumulate(scene, cam, samples, onSample); const full = read();
  U5.uKeyOn.value = 0; spot.visible = false;
  pipe.accumulate(scene, cam, samples, onSample); const fill = read();
  U5.uKeyOn.value = 1; spot.visible = true;
  U5.uFillOn.value = 0;
  pipe.accumulate(scene, cam, samples, onSample); const key = read();
  U5.uFillOn.value = 1;
  const out = {};
  for (const [k, p] of Object.entries(pts)) { const [x, y] = pix(...p); out[k] = { px: [x, y], full: lum(full, x, y), key_only: lum(key, x, y), spill_only_lantern_off: lum(fill, x, y) }; }
  spr.forEach((o) => (o.visible = true));
  // khôi phục ảnh đầy đủ cho finalize
  pipe.accumulate(scene, cam, samples, onSample); if (!cfg.nopaint) paint.apply(scene, cam);
  return out;
}

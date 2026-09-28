// W3 (Cổng 5, mặt Ida A1) — trang ảnh thử cổng mặt. Driver: design/cong5/mat/still.js (gốc phục vụ = design/).
// Dựng ĐÚNG khung face_ida của Cổng 4 lần 3 (v2/shots.js buildCloseIda, cùng grade, phơi sáng 0,12, lớp vẽ C, DOF) và chỉ thêm:
//   cfg.fl   : { mode, ... } → ánh sáng cận mặt design/cong5/layout/facelight.js (dội/viền của nguồn có thật); bỏ trống = như lần 3.
//   cfg.expose: phơi sáng ghi đè; "auto" = fl.exposure() (không cháy da).
// Khung: face_ida (cfg.dbg như run_mat.sh của Cổng 4).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { createPaint } from '/cong3/dir-C/paint.js';
import { createDOF } from '/cong3/shared/dof.js';
import { buildCloseIda } from '/cong3/v2/shots.js';
import { createFaceLight } from '/cong5/layout/facelight.js';

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
const G = { gCanvas: 0.012, gVig: 0.28, gLift: 0.02, gSat: 1.0, gShadowTint: [0.40, 0.32, 0.90], gHiTint: [1.0, 0.975, 0.93] };   // = GRADES.face_ida

let W, H, cfg, renderer, pipe, cur, fl, info = {};
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  const mod = await import('/cong3/v2/char3d/cast3d.js');
  const ida = await fetch('/cong3/model-sheet/ida.json').then((r) => r.json());
  renderer = createRenderer(W, H); renderer.shadowMap.type = THREE.PCFShadowMap;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  cur = await buildCloseIda(ida, (s, o) => mod.buildCharacter(s, { ...o, ...(c.charOpts || {}) }), mod.update || null, 0, { ...(c.dbg || {}), face: true });
  if (c.fl) { fl = createFaceLight(cur.scene, c.fl); info.fl = fl.update(cur.chars[0], cur.cam, {}); }
  cur.paint = createPaint(renderer, W, H, pipe, cur.paintP);
  const u = pipe.outMat.uniforms;
  u.gCanvas.value = G.gCanvas; u.gVig.value = G.gVig; u.gLift.value = G.gLift; u.gSat.value = G.gSat; u.gShadowTint.value.set(...G.gShadowTint); u.gHiTint.value.set(...G.gHiTint);
  u.uExp.value = c.expose === 'auto' ? fl.exposure() : (c.expose ?? 0.12); info.exposure = u.uExp.value;
};
window.renderFrame = async (name, samples) => {
  const ms = pipe.accumulate(cur.scene, cur.cam, samples, cur.onSample);
  if (!cfg.nopaint) cur.paint.apply(cur.scene, cur.cam); else cur.paint.bypass();
  if (cur.dof && !cfg.nopaint) { if (!cur.dofFx) cur.dofFx = createDOF(renderer, W, H, pipe); cur.dofFx.apply(cur.paint.outRT.texture, cur.paint.gRT.texture, cur.dof); }
  return { accum_ms: ms, prof_ms: info };
};
window.finalize = (f) => pipe.finalize(f);

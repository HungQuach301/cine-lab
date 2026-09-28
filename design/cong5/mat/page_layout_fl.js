// W3 (Cổng 5) — trang THỬ facelight.js trên shot layout thật (không sửa file của P/W1/W2). Driver: design/cong5/mat/still.js.
// --args {"shot":"s37","f":<khung phim toàn cục, mặc định giữa shot>,"fl":{"mode":"gas"|"lantern"|"elec", ...},"keyE":<số, tuỳ chọn>,"expose":"auto"|số}
// Dựng shot đúng như design/cong5/layout/page.js (cùng grade, lớp vẽ), rồi gắn facelight lên Ida sau mỗi update(). Không có "fl" = như layout hiện tại.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { createPaint } from '/cong3/dir-C/paint.js';
import { SHOTS } from '/cong5/layout/film.js';
import { GRADE_WARM } from '/cong5/layout/sets.js';
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
let W, H, cfg, renderer, pipe, cur, shot, fl, info = {};
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  const mod = await import('/cong3/v2/char3d/cast3d.js');
  const [ida, cas] = await Promise.all(['/cong3/model-sheet/ida.json', '/cong3/model-sheet/cas.json'].map((p) => fetch(p).then((r) => r.json())));
  renderer = createRenderer(W, H); renderer.shadowMap.type = THREE.PCFShadowMap;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  shot = SHOTS.find((s) => s.id === c.shot); if (!shot) throw new Error('không có shot ' + c.shot);
  cur = await shot.build({ THREE, sheets: { ida, cas }, W, H, mkChar: (sheet, opts) => mod.buildCharacter(sheet, opts), upd: mod.update || null, dbg: {} });
  if (c.fl) fl = createFaceLight(cur.scene, c.fl);
  cur.paint = createPaint(renderer, W, H, pipe, { ...(cur.paintP || {}) });
  const g = cur.grade || GRADE_WARM, u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
};
window.renderFrame = async (name, samples) => {
  const f = cfg.f ?? Math.round((shot.t0 + shot.t1) / 2 * 24), T = f / 24, t = T - shot.t0;
  cur.update(t, T, f);
  if (fl) info.fl = fl.update(cur.named.ida, cur.cam, { keyE: cfg.keyE });
  const u = pipe.outMat.uniforms;
  u.uExp.value = cfg.expose === 'auto' && fl ? fl.exposure() : typeof cfg.expose === 'number' ? cfg.expose : (typeof cur.exposure === 'function' ? cur.exposure(t, T) : (cur.exposure ?? 1.0));
  info.exposure = u.uExp.value; info.f = f;
  const ms = pipe.accumulate(cur.scene, cur.cam, samples, cur.onSample || null);
  cur.paint.apply(cur.scene, cur.cam);
  return { accum_ms: ms, prof_ms: info };
};
window.finalize = (f) => pipe.finalize(f);

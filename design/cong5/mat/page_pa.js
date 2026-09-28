// W3 (Cổng 5 v2) — trang dựng KHUNG THỬ phương án dàn dựng lại câu cao trào L4 (1:32–1:48). Driver: design/cong5/mat/still.js.
// Dựng ĐÚNG bộ cảnh của một shot layout (sets, đèn khí/đèn lồng/điện, facelight nếu shot có, grade, lớp vẽ) ở thời điểm phim T,
// rồi chỉ GHI ĐÈ MÁY (và tuỳ chọn biểu cảm/kiểu mặt Ida). Không thêm đèn: mọi nguồn là của bộ cảnh (luật thế giới v0.5).
// --args {"shot":"s37","T":<giây phim>,"cam":{"pos":[x,y,z],"look":[x,y,z],"mm":50} | {"rel":{"yaw":…,"dist":…,"y":…,"drop":…},"mm":85},
//         | {"joint":"wrist_R"|"head","off":[dx,dy,dz],"lookOff":[…],"mm":50},
//         "charOpts":{"idaStyle":"aa"|"ai"}, "expr":<biểu cảm>, "exp":<phơi sáng ghi đè | "shot">, "expMul":<nhân phơi sáng shot>, "paint":{…}, "hide":"<part>"}
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { createPaint } from '/cong3/dir-C/paint.js';
import { SHOTS } from '/cong5/layout/film.js';
import { GRADE_WARM } from '/cong5/layout/sets.js';
import { faceCam } from '/cong5/layout/common.js';
import { fovOf } from '/cong5/layout/util.js';

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
let W, H, cfg, renderer, pipe, cur, shot, info = {};
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  const mod = await import('/cong3/v2/char3d/cast3d.js');
  const [ida, cas] = await Promise.all(['/cong3/model-sheet/ida.json', '/cong3/model-sheet/cas.json'].map((p) => fetch(p).then((r) => r.json())));
  renderer = createRenderer(W, H); renderer.shadowMap.type = THREE.PCFShadowMap;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  shot = SHOTS.find((s) => s.id === c.shot); if (!shot) throw new Error('không có shot ' + c.shot);
  cur = await shot.build({ THREE, sheets: { ida, cas }, W, H, upd: mod.update || null, dbg: c.dbg || {},
    mkChar: (sheet, opts) => mod.buildCharacter(sheet, sheet.id.startsWith('CHR-ida') ? { ...opts, ...(c.expr ? { expr: c.expr } : {}), ...(c.charOpts || {}) } : opts) });
  if (c.hide) cur.named.ida.root.traverse((m) => { if (m.isMesh && m.userData.part === c.hide) m.visible = false; });
  cur.paint = createPaint(renderer, W, H, pipe, { ...(cur.paintP || {}), ...(c.paint || {}) });
  const g = cur.grade || GRADE_WARM, u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
};
window.renderFrame = async (name, samples) => {
  const T = cfg.T ?? (shot.t0 + shot.t1) / 2, f = Math.round(T * 24), t = T - shot.t0;
  cur.update(t, T, f);
  const cam = cur.cam, c = cfg.cam;
  if (c && c.rel) faceCam(cam, cur.named.ida, { fov: fovOf(c.mm ?? 85), ...c.rel });
  else if (c && c.joint) {   // máy bám khớp của Ida: vị trí = khớp + off (m, hệ thế giới), nhìn vào khớp + lookOff
    const j = new THREE.Vector3(); cur.named.ida.joints[c.joint].getWorldPosition(j);
    cam.fov = fovOf(c.mm ?? 50); cam.position.copy(j).add(new THREE.Vector3(...c.off)); cam.lookAt(j.clone().add(new THREE.Vector3(...(c.lookOff || [0, 0, 0])))); cam.updateProjectionMatrix(); }
  else if (c && c.pos) { cam.fov = fovOf(c.mm ?? 35); cam.position.set(...c.pos); cam.lookAt(new THREE.Vector3(...c.look)); cam.updateProjectionMatrix(); }
  cam.updateMatrixWorld(true);
  const u = pipe.outMat.uniforms, e0 = typeof cur.exposure === 'function' ? cur.exposure(t, T) : (cur.exposure ?? 1.0);
  u.uExp.value = typeof cfg.exp === 'number' ? cfg.exp : e0 * (cfg.expMul ?? 1);
  info = { T, f, exposure: +u.uExp.value.toFixed(4), cam: cam.position.toArray().map((v) => +v.toFixed(2)) };
  const ms = pipe.accumulate(cur.scene, cam, samples, cur.onSample || null);
  cur.paint.apply(cur.scene, cam);
  return { accum_ms: ms, prof_ms: info };
};
window.finalize = (f) => pipe.finalize(f);

// BẢN GỠ LỖI của v2/page.js (chỉ dùng trong char2d): thêm cfg.hide (ẩn lớp tranh theo tên), cfg.only, cfg.cam (dịch máy).
// Cổng 3 v2 — trang render chung (driver: shared/render_still.js hoặc shared/render_seq.js).
// --args: {"char": "base" | "3d" | "2d"}  (module dựng nhân vật: shared/cast.js | v2/char3d/cast3d.js | v2/char2d/cast2d.js)
//         {"nopaint": 1} bỏ lớp vẽ (để đo nhấp nháy của lớp vẽ); {"shot": "..."} dựng sẵn một shot trong setup.
// Khung: a_close_ida | b_cas_bird | c_s5_wide | walk@<số khung>
// Module nhân vật PHẢI xuất: buildCharacter(sheet, opts) (cùng API shared/cast.js) và có thể xuất update(ch, camera) (gọi trước mỗi mẫu).
import * as THREE from '../../shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '../../shared/post.js';
import { createPaint } from '../../dir-C/paint.js';
import { buildS5 } from '../s5.js';
import { buildCloseIda, buildCasBird, buildWalk } from '../shots.js';

const CHAR = { base: '../../shared/cast.js', '2d': './cast2d.js' };
// Grade hướng C (chép từ dir-C/scene.js để dùng chung, không đổi).
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
const GRADES = {
  a_close_ida: { gCanvas: 0.012, gVig: 0.28, gLift: 0.02, gSat: 1.0, gShadowTint: [0.40, 0.32, 0.90], gHiTint: [1.0, 0.975, 0.93] },
  b_cas_bird: { gCanvas: 0.012, gVig: 0.30, gLift: 0.02, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [1.0, 0.98, 0.94] },
  c_s5_wide: { gCanvas: 0.012, gVig: 0.30, gLift: 0.018, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [0.985, 0.995, 1.02] },
  walk: { gCanvas: 0.012, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.975, 0.93] },
};
// Phơi sáng theo shot (máy quay), cùng một thế giới đèn: cận mặt sát ngọn lửa phải đóng khẩu; cảnh đêm xa đèn phải mở khẩu.
const EXPOSE = { a_close_ida: 0.30, b_cas_bird: 2.6, c_s5_wide: 1.0, walk: 1.05 };
const S5_PAINT = { rNear: 7.0, rFar: 9.0, dNear: 6, dFar: 12, impScale: 0.5, stroke: 0.045, preAmp: 0.16, wob: 3.5, preLen: 46, preWid: 6 };

let W, H, cfg, renderer, pipe, sheets, mod; const built = {};
async function build(shot) {
  const mkChar = (sheet, opts) => mod.buildCharacter(sheet, opts), upd = mod.update || null;
  if (shot === 'a_close_ida') return buildCloseIda(sheets[0], mkChar, upd);
  if (shot === 'b_cas_bird') return buildCasBird(sheets[1], mkChar, upd);
  if (shot === 'walk') return buildWalk(sheets[0], mkChar, upd);
  if (shot === 'c_s5_wide') { const r = await buildS5(sheets[0], sheets[1], cfg.dbg || {}, mkChar, upd); return { ...r, chars: [r.chIda, r.chCas], paintP: S5_PAINT }; }
  throw new Error('shot không có: ' + shot);
}
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  mod = await import(CHAR[c.char || 'base']);
  sheets = await Promise.all(['model-sheet/ida.json', 'model-sheet/cas.json'].map((p) => fetch('/' + p).then((r) => r.json())));
  renderer = createRenderer(W, H);
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  if (c.shot) { const b = built[c.shot] = await build(c.shot); dbgApply(b); b.paint = createPaint(renderer, W, H, pipe, b.paintP); renderer.compile(b.scene, b.cam);
    pipe.accumulate(b.scene, b.cam, 1, b.onSample); if (!cfg.nopaint) b.paint.apply(b.scene, b.cam); pipe.finalize(0); } // khởi động (biên dịch shader, cấp RT) — chi phí một lần mỗi shot
};
function dbgApply(b) {
  for (const ch of b.chars || []) ch.root.traverse((o) => { if (!o.isMesh) return;
    if (cfg.hide && cfg.hide.some((n) => o.name.startsWith(n))) o.visible = false;
    if (cfg.only && o.userData.card2d && !cfg.only.some((n) => o.name.startsWith(n))) o.visible = false;
    if (cfg.showProxy && o.userData.proxy) { o.material = new THREE.MeshLambertMaterial({ color: '#88aaff' }); } });
  if (cfg.cam) { b.cam.position.add(new THREE.Vector3(...cfg.cam)); if (cfg.look) b.cam.lookAt(...cfg.look); }
  if (cfg.camAbs) { const o = b.onSample; const set = () => { b.cam.position.set(...cfg.camAbs); b.cam.lookAt(...cfg.look); b.cam.updateMatrixWorld(); };
    b.onSample = (i, n, j) => { set(); if (o) o(i, n, j); set(); for (const ch of b.chars || []) if (mod.update) mod.update(ch, b.cam); }; set(); }
  if (cfg.lookAtJoint) { const ch = b.chars[cfg.lookAtJoint[0]]; const p = new THREE.Vector3(); ch.joints[cfg.lookAtJoint[1]].getWorldPosition(p); console.log('JOINT', JSON.stringify(p)); }
  if (cfg.fov) { b.cam.fov = cfg.fov; b.cam.updateProjectionMatrix(); }
}
window.renderFrame = async (name, samples) => {
  const [shot, fs] = name.split('@'); const f = fs ? +fs : 0;
  const cur = built[shot] || (built[shot] = await build(shot));
  if (!cur.paint) cur.paint = createPaint(renderer, W, H, pipe, cur.paintP);
  const g = GRADES[shot], u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
  u.uExp.value = (cfg.expose && cfg.expose[shot]) || EXPOSE[shot];
  if (cur.setFrame) cur.setFrame(f);
  const ms = pipe.accumulate(cur.scene, cur.cam, samples, cur.onSample);
  if (!cfg.nopaint) cur.paint.apply(cur.scene, cur.cam); else cur.paint.bypass();
  return { accum_ms: ms };
};
window.finalize = (f) => pipe.finalize(f);

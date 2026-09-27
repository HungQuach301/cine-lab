// Cine Lab · Cổng 4 — trang render ANIMATIC (previs). Driver: design/cong4/animatic/render_film.js.
// Mỗi shot dựng trong một trang riêng (s1 sửa ShaderChunk sương toàn cục; s5/s6 dùng chung uniform U) → không nhiễm chéo giữa các bộ.
// Chất lượng previs: 960×540, 1 mẫu, không DOF, lớp vẽ C giữ (nhận diện phong cách), grain chung của đường ống.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { createPaint } from '/cong3/dir-C/paint.js';
import { SHOTS } from './film.js';
import { GRADE_WARM } from './sets.js';

// Grade hướng C (chép từ v2/page.js — không đổi).
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

window.listShots = () => SHOTS.map(({ build, ...m }) => m);
let W, H, cfg, renderer, pipe, sheets, mod, cur, shot;
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  mod = await import('/cong3/v2/char3d/cast3d.js');
  const [ida, cas] = await Promise.all(['/cong3/model-sheet/ida.json', '/cong3/model-sheet/cas.json'].map((p) => fetch(p).then((r) => r.json())));
  sheets = { ida, cas };
  renderer = createRenderer(W, H); renderer.shadowMap.type = THREE.PCFShadowMap;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  shot = SHOTS.find((s) => s.id === c.shot); if (!shot) throw new Error('không có shot ' + c.shot);
  const ctx = { THREE, sheets, W, H, mkChar: (sheet, opts) => mod.buildCharacter(sheet, opts), upd: mod.update || null, dbg: c.dbg || {} };
  cur = await shot.build(ctx);
  cur.paint = createPaint(renderer, W, H, pipe, { ...(cur.paintP || {}) });
  const g = cur.grade || GRADE_WARM, u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
  return { t0: shot.t0, t1: shot.t1 };
};
// name = khung phim toàn cục (số nguyên). Trả thời gian tích luỹ.
window.renderFrame = async (fGlobal) => {
  const T = fGlobal / 24, t = T - shot.t0;
  cur.update(t, T, fGlobal);
  pipe.outMat.uniforms.uExp.value = typeof cur.exposure === 'function' ? cur.exposure(t, T) : (cur.exposure ?? 1.0);
  const ms = pipe.accumulate(cur.scene, cur.cam, 1, cur.onSample || null);
  if (!cfg.nopaint) cur.paint.apply(cur.scene, cur.cam); else cur.paint.bypass();
  return { accum_ms: ms };
};
window.finalize = (f) => pipe.finalize(f);
// Chỉ đặt trạng thái khung (không render) — để xuất lại dữ liệu chuyển động đúng trạng thái đã render (hàm update tất định).
window.stepFrame = (fGlobal) => { const T = fGlobal / 24; cur.update(T - shot.t0, T, fGlobal); if (cur.onSample) cur.onSample(0, 1, [0, 0]); };

// Dữ liệu chuyển động cho checks (RUN.md 3.2, 3.4): góc khớp bake (character_part), gốc (character_root), máy quay, và track màn hình
// (điểm ảnh video, gốc trên-trái) cho đầu và hai cổ tay — null khi khuất (tia từ máy chạm vật khác trước) hoặc ngoài khung.
const JOINTS = ['spine', 'neck', 'head', 'shoulder_L', 'elbow_L', 'wrist_L', 'shoulder_R', 'elbow_R', 'wrist_R', 'hip_L', 'knee_L', 'hip_R', 'knee_R'];
const ray = new THREE.Raycaster();
window.frameMeta = () => {
  const out = { rot: {}, root: {}, track: {}, cam: [cur.cam.position.x, cur.cam.position.y, cur.cam.position.z] };
  cur.scene.updateMatrixWorld(true); cur.cam.updateMatrixWorld(true);
  const occluders = []; cur.scene.traverse((o) => { if (o.isMesh && o.visible && o.material && !o.material.transparent && o.material.colorWrite !== false) occluders.push(o); });
  for (const [name, ch] of Object.entries(cur.named || {})) {
    if (!ch.root.visible || !ch.root.parent) continue;
    for (const j of JOINTS) { const o = ch.joints[j]; if (o) out.rot[`${name}/${j}.rot`] = [o.rotation.x, o.rotation.y, o.rotation.z].map((v) => +v.toFixed(5)); }
    out.root[`${name}/root.loc`] = [ch.root.position.x, ch.root.position.y, ch.root.position.z].map((v) => +v.toFixed(4));
    const palm = -ch.sheet.parts.hand.palm_length * ch.H * 0.55;   // giữa lòng bàn tay (vùng có chi tiết), không lấy khớp cổ tay (mép tay áo)
    const pts = { head: ch.joints.head.localToWorld(new THREE.Vector3(0, 0.62 * ch.H, 0.25 * ch.H)), hand_L: ch.joints.wrist_L.localToWorld(new THREE.Vector3(0, palm, 0)), hand_R: ch.joints.wrist_R.localToWorld(new THREE.Vector3(0, palm, 0)) };
    for (const [k, p] of Object.entries(pts)) {
      const ndc = p.clone().project(cur.cam); let v = null;
      if (ndc.z < 1 && Math.abs(ndc.x) <= 1 && Math.abs(ndc.y) <= 1) {
        const d = p.distanceTo(cur.cam.position); ray.set(cur.cam.position, p.clone().sub(cur.cam.position).normalize()); ray.far = d + 0.2;
        const hit = ray.intersectObjects(occluders, false)[0];
        if (!hit || hit.distance > d - 0.06) v = [+((ndc.x + 1) / 2 * W).toFixed(2), +((1 - ndc.y) / 2 * H).toFixed(2)];
      }
      out.track[`${name}/${k}`] = v;
    }
  }
  return out;
};

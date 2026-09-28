// Cine Lab · Cổng 4 — trang render ANIMATIC (previs). Driver: design/cong5/layout/render_film.js.
// Mỗi shot dựng trong một trang riêng (s1 sửa ShaderChunk sương toàn cục; s5/s6 dùng chung uniform U) → không nhiễm chéo giữa các bộ.
// Chất lượng previs: 960×540, 1 mẫu, không DOF, lớp vẽ C giữ (nhận diện phong cách), grain chung của đường ống.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { createPaint } from '/cong3/dir-C/paint.js';
import { SHOTS, EVENTS } from './film.js';
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
window.listEvents = () => EVENTS;
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
  // chẩn đoán (chỉ dùng khi --dbg): ẩn một bộ phận / tắt phát sáng của nhân vật
  if (c.dbg && (c.dbg.hide || c.dbg.noEmissive || c.dbg.front || c.dbg.noShadow)) for (const ch of Object.values(cur.named || {})) ch.root.traverse((o) => { if (!o.isMesh) return;
    if (c.dbg.hide && o.userData.part === c.dbg.hide) o.visible = false; if (c.dbg.front && o.material) o.material.side = THREE.FrontSide; if (c.dbg.noShadow) o.receiveShadow = false; if (c.dbg.noEmissive && o.material && 'emissiveIntensity' in o.material) o.material.emissiveIntensity = 0; });
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

// ================= C3 (RUN.md 3.6, 3.6.2 — v1.4): mặt nạ bộ phận + views, từ CHÍNH trang render này =================
// Cách tính theo công cụ tham chiếu reports/checks-v1.4/dryrun/k_views.js (phiên K) và exportParts của Cổng 3 (design/cong3/v2/page.js):
// mặt nạ = phần NHÌN THẤY của bộ phận (vật liệu ID phẳng; mọi vật khác tô đen nhưng vẫn ghi độ sâu), render thật ở scale× khung.
const PART_MAP = { head: ['head'], torso: ['torso'], upper_arm: ['upper_arm'], forearm: ['forearm'], thigh: ['thigh', 'thigh_skin'], shin: ['shin', 'shin_trouser'] };
window.hasChar = (who) => !!(cur.named && cur.named[who] && cur.named[who].root.visible && cur.named[who].root.parent);
window.exportC3 = async (f, scale, who = 'ida', side = 'L') => {
  window.stepFrame(f);
  const ch = cur.named[who], J = ch.joints, Hh = ch.H, S = side, D2R = Math.PI / 180, R2D = 180 / Math.PI, keys = Object.keys(PART_MAP);
  const partOf = {}; for (const [k, v] of Object.entries(PART_MAP)) for (const t of v) partOf[t] = k;
  cur.scene.updateMatrixWorld(true); cur.cam.updateMatrixWorld(true);
  const Wp = (o, l = [0, 0, 0]) => o.localToWorld(new THREE.Vector3(...l));
  const bones = () => ({ head: [Wp(J.head), Wp(J.head, [0, Hh, 0])], torso: [Wp(J.spine), Wp(J.neck)],
    upper_arm: [Wp(J['shoulder_' + S]), Wp(J['elbow_' + S])], forearm: [Wp(J['elbow_' + S]), Wp(J['wrist_' + S])],
    thigh: [Wp(J['hip_' + S]), Wp(J['knee_' + S])], shin: [Wp(J['knee_' + S]), Wp(J['ankle_' + S])] });
  const toRoot = (v) => ch.root.worldToLocal(v.clone()); const now = bones();
  const camW = cur.cam.getWorldPosition(new THREE.Vector3()), tc = now.torso[0].clone().add(now.torso[1]).multiplyScalar(0.5);
  const c = toRoot(camW).sub(toRoot(tc)); const view = -Math.atan2(c.x, c.z) * R2D, elev = Math.atan2(c.y, Math.hypot(c.x, c.z)) * R2D;
  const saved = Object.fromEntries(Object.entries(J).map(([k, j]) => [k, j.rotation.clone()]));
  for (const j of Object.values(J)) j.rotation.set(0, 0, 0);
  for (const [n, [x, y, z]] of Object.entries(ch.sheet.poses.turnaround.joints || {})) if (J[n]) J[n].rotation.set(x * D2R, y * D2R, z * D2R, 'XYZ');
  ch.root.updateMatrixWorld(true); const ref = bones();
  for (const [k, r] of Object.entries(saved)) J[k].rotation.copy(r); ch.root.updateMatrixWorld(true);
  const fwd = cur.cam.getWorldDirection(new THREE.Vector3()), zc = (p) => p.clone().sub(camW).dot(fwd), zHead = zc(Wp(J.head, [0, 0.5 * Hh, 0]));
  const v = new THREE.Vector3(), box = new THREE.Box3();
  // Cổng 5: vật che tô đen GIỮ ĐÚNG mặt hiển thị như ảnh render (FrontSide/BackSide/DoubleSide). Bản cũ tô đen hai mặt → mặt phẳng một mặt
  // nằm giữa máy và nhân vật (máy đặt sau mặt tiền, vd s27) bị cắt mặt sau trong ảnh render nhưng lại che kín nhân vật trong mặt nạ.
  const blacks = [THREE.FrontSide, THREE.BackSide, THREE.DoubleSide].map((sd) => new THREE.MeshBasicMaterial({ color: 0x000000, side: sd }));
  const blackOf = (o) => { const m0 = Array.isArray(o.material) ? o.material[0] : o.material; return blacks[m0 && m0.side != null ? m0.side : 0]; };
  const black = blacks[2];
  const idMat = keys.map((k, i) => new THREE.MeshBasicMaterial({ color: new THREE.Color((i + 1) * 30 / 255, 0, 0), side: THREE.DoubleSide }));
  const saveM = [], owner = new Map(), vis0 = new Map(), body = new Set(), blackM = new Map(); ch.root.traverse((o) => { if (o.isMesh) body.add(o); });
  cur.scene.traverse((o) => {
    if (o.isSprite || o.isPoints || o.isLine) { saveM.push([o, 'v', o.visible]); o.visible = false; return; }
    if (!o.isMesh) return; saveM.push([o, 'm', o.material]); saveM.push([o, 'v', o.visible]);
    let vis = o.visible; for (let p = o.parent; p; p = p.parent) vis = vis && p.visible; vis0.set(o, vis);
    const k = body.has(o) ? partOf[o.userData.part] : undefined; let ok = !!k;
    if (ok && k !== 'head' && k !== 'torso') { o.geometry.computeBoundingBox(); box.copy(o.geometry.boundingBox).applyMatrix4(o.matrixWorld); box.getCenter(v); ch.root.worldToLocal(v); ok = (v.x > 0) === (S === 'L'); }
    owner.set(o, ok ? k : null); if (!ok) blackM.set(o, blackOf(o));
    // Cổng 5: vật trong suốt không thuộc nhân vật (tấm sương, kính, quầng) không che trong ảnh render → không được che trong mặt nạ (tô đen đục thì che oan, vd s27)
    const m0 = Array.isArray(o.material) ? o.material[0] : o.material;
    if (!ok && !body.has(o) && m0 && (m0.transparent || m0.depthWrite === false || (m0.opacity ?? 1) < 1)) vis0.set(o, false);
  });
  const bg = cur.scene.background, fog = cur.scene.fog; cur.scene.background = new THREE.Color(0); cur.scene.fog = null;
  const sm = renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate = false;
  const shot1 = (w, h, bodyOnly) => {
    for (const [o, k] of owner) { o.material = k ? idMat[keys.indexOf(k)] : (blackM.get(o) || black); o.visible = vis0.get(o) && (!bodyOnly || body.has(o)); }
    const rt = new THREE.WebGLRenderTarget(w, h, { depthBuffer: true }), px = new Uint8Array(w * h * 4);
    renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(cur.scene, cur.cam);
    renderer.readRenderTargetPixels(rt, 0, 0, w, h, px); renderer.setRenderTarget(null); rt.dispose(); return px;
  };
  const cnt = (px) => { const n = Object.fromEntries(keys.map((k) => [k, 0])); for (let j = 0; j < px.length; j += 4) { const id = Math.round(px[j] / 30); if (id >= 1 && id <= keys.length) n[keys[id - 1]]++; } return n; };
  const visN = cnt(shot1(W, H, false)), alone = cnt(shot1(W, H, true));
  const w = W * scale, h = H * scale, big = shot1(w, h, false);
  renderer.shadowMap.autoUpdate = sm; cur.scene.background = bg; cur.scene.fog = fog;
  for (let i = saveM.length - 1; i >= 0; i--) { const [o, k, val] = saveM[i]; if (k === 'v') o.visible = val; else o.material = val; }
  const parts = {};
  for (const k of keys) {
    const [a, b] = now[k], mid = a.clone().add(b).multiplyScalar(0.5);
    const P = (d) => d.clone().sub(fwd.clone().multiplyScalar(d.dot(fwd))).length();
    const fs_ = P(now[k][1].clone().sub(now[k][0])) / Math.max(P(ref[k][1].clone().sub(ref[k][0])), 1e-9);
    parts[k] = { foreshorten: +fs_.toFixed(4), hidden: alone[k] ? +Math.max(0, 1 - visN[k] / alone[k]).toFixed(4) : 1,
      depth: +(zc(k === 'head' ? Wp(J.head, [0, 0.5 * Hh, 0]) : mid) / zHead).toFixed(4) };
  }
  const id = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) { const src = (h - 1 - y) * w * 4, dst = y * w; for (let x = 0; x < w; x++) id[dst + x] = Math.round(big[src + x * 4] / 30); }
  const out = {}, count = {};
  const cv = new OffscreenCanvas(w, h), g = cv.getContext('2d'), img = g.createImageData(w, h), d32 = new Uint32Array(img.data.buffer);
  for (let i = 0; i < keys.length; i++) {
    let n = 0; for (let j = 0; j < id.length; j++) { const on = id[j] === i + 1; d32[j] = on ? 0xffffffff : 0x00000000; n += on; }
    g.putImageData(img, 0, 0); const ab = await (await cv.convertToBlob({ type: 'image/png' })).arrayBuffer();
    let bin = ''; const u8 = new Uint8Array(ab); for (let j = 0; j < u8.length; j += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(j, j + 0x8000));
    out[keys[i]] = btoa(bin); count[keys[i]] = n;
  }
  return { w, h, parts: out, count, views: { view_deg: +view.toFixed(2), elev_deg: +elev.toFixed(2), parts } };
};

// W4 · cửa mặt Ida lượt 2 — trang KHUNG THỬ PA1 (bản sao design/cong5/mat/page_pa.js của W3, thêm 3 việc; không sửa trang gốc):
//  1. Ida 'bl' (nạp trước glb) — hoặc 'aa' / 'ai' qua charOpts để so cùng khung.
//  2. "l11":{"elev":17.5,"az":25} → GHI ĐÈ vị trí đèn khí L11 CHỈ trong khung thử (đã duyệt: nâng 15–20°, lệch ~25° khỏi trục máy),
//     giữ khoảng cách tới mặt. L11 = đèn điểm (không phải facelight) gần mặt Ida nhất. Không thêm đèn. Layout/facelight không đổi.
//  3. "export":1 → trả về (trong timing.json, page_prof_ms) glb của Ida (GLTFExporter, vật liệu tối giản theo part) + máy + mọi đèn,
//     để dựng lại cùng khung trong Blender EEVEE (blender/eevee_frame.py).
// --args như page_pa.js + {"l11":{…}, "export":1}
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
  if ((c.charOpts?.idaStyle ?? 'bl') === 'bl') await mod.preloadIdaBL(c.glb ? new URL(c.glb, location.href).href : undefined);   // "glb": thử bản glb khác (đường dẫn tính từ design/)
  const charOpts = { idaStyle: 'bl', ...(c.charOpts || {}) };
  const [ida, cas] = await Promise.all(['/cong3/model-sheet/ida.json', '/cong3/model-sheet/cas.json'].map((p) => fetch(p).then((r) => r.json())));
  renderer = createRenderer(W, H); renderer.shadowMap.type = THREE.PCFShadowMap;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  shot = SHOTS.find((s) => s.id === c.shot); if (!shot) throw new Error('không có shot ' + c.shot);
  cur = await shot.build({ THREE, sheets: { ida, cas }, W, H, upd: mod.update || null, dbg: c.dbg || {},
    mkChar: (sheet, opts) => mod.buildCharacter(sheet, sheet.id.startsWith('CHR-ida') ? { ...opts, ...(c.expr ? { expr: c.expr } : {}), ...charOpts } : opts) });
  cur.paint = createPaint(renderer, W, H, pipe, { ...(cur.paintP || {}), ...(c.paint || {}) });
  const g = cur.grade || GRADE_WARM, u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
};

function faceCenter(ch) { const c = new THREE.Vector3(0, 0.42 * ch.H, 0.30 * ch.H); ch.joints.head.localToWorld(c); return c; }
function moveL11(cam, spec) {
  const ida = cur.named.ida, c = faceCenter(ida); let L = null, dmin = 1e9;
  cur.scene.traverse((o) => { if (o.isPointLight && !o.userData.faceLight && o.intensity > 0) { const d = o.getWorldPosition(new THREE.Vector3()).distanceTo(c); if (d < dmin) { dmin = d; L = o; } } });
  if (!L) return null;
  const p0 = L.getWorldPosition(new THREE.Vector3()), v0 = p0.clone().sub(c), dist = v0.length();
  const Y = new THREE.Vector3(0, 1, 0), toCam = cam.getWorldPosition(new THREE.Vector3()).sub(c); toCam.y = 0; toCam.normalize();
  const hK = v0.clone(); hK.y = 0; hK.normalize();
  const side = Math.sign(new THREE.Vector3().crossVectors(toCam, hK).y || 1);
  const h = toCam.clone().applyAxisAngle(Y, side * (spec.az ?? 25) * Math.PI / 180), e = (spec.elev ?? 17.5) * Math.PI / 180;
  const dir = h.multiplyScalar(Math.cos(e)).addScaledVector(Y, Math.sin(e)).normalize();
  const pw = c.clone().addScaledVector(dir, dist);
  L.parent.updateWorldMatrix(true, false); L.position.copy(L.parent.worldToLocal(pw.clone())); L.updateMatrixWorld(true);
  const ang = (a, b) => +(a.angleTo(b) * 180 / Math.PI).toFixed(1), el = (v) => +(Math.asin(v.clone().normalize().y) * 180 / Math.PI).toFixed(1);
  return { name: L.name || '(L11)', dist: +dist.toFixed(3), before: { elev: el(v0), offCamAxisDeg: ang(new THREE.Vector3(v0.x, 0, v0.z), toCam) }, after: { elev: el(dir), offCamAxisDeg: ang(new THREE.Vector3(dir.x, 0, dir.z), toCam) },
    pos0: p0.toArray().map((x) => +x.toFixed(3)), pos1: pw.toArray().map((x) => +x.toFixed(3)) };
}

async function exportIda(cam) {
  const base = '/cong3/shared/node_modules/three/', threeURL = new URL(base + 'build/three.module.js', location.href).href;
  const src = (await (await fetch(base + 'examples/jsm/exporters/GLTFExporter.js')).text()).replace(/from\s*'three'/g, `from '${threeURL}'`);
  const { GLTFExporter } = await import(URL.createObjectURL(new Blob([src], { type: 'text/javascript' })));
  const ida = cur.named.ida.root; ida.updateMatrixWorld(true);
  const grp = new THREE.Group(); const swaps = [];
  ida.traverse((o) => { if (!o.isMesh || !o.visible) return;
    const g = o.geometry.clone(); g.applyMatrix4(o.matrixWorld); for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'color', 'uv'].includes(k)) g.deleteAttribute(k);
    g.morphAttributes = {};
    const src = Array.isArray(o.material) ? o.material[0] : o.material;
    const m = new THREE.MeshStandardMaterial({ color: src.color ? src.color.clone() : new THREE.Color(1, 1, 1), vertexColors: !!g.attributes.color, name: (o.userData.part || 'x') + '|' + (src.color ? src.color.getHexString() : 'ffffff'),
      ...(o.userData.part === 'eyes' && src.map ? { map: src.map } : {}), metalness: src.metalness ?? 0, roughness: src.roughness ?? 1 });
    const mm = new THREE.Mesh(g, m); mm.name = (o.userData.part || 'x'); grp.add(mm); });
  const glb = await new GLTFExporter().parseAsync(grp, { binary: true });
  const b64 = btoa(Array.from(new Uint8Array(glb), (x) => String.fromCharCode(x)).join(''));
  const lights = []; cur.scene.updateMatrixWorld(true);
  cur.scene.traverse((o) => { if (o.isLight && o.visible) { const p = o.getWorldPosition(new THREE.Vector3());
    lights.push({ type: o.type, pos: p.toArray(), color: o.color.toArray(), intensity: o.intensity, distance: o.distance ?? 0, decay: o.decay ?? 2, face: !!o.userData.faceLight,
      ground: o.groundColor ? o.groundColor.toArray() : null, castShadow: !!o.castShadow,
      dir: o.isDirectionalLight || o.isSpotLight ? o.target.getWorldPosition(new THREE.Vector3()).sub(p).normalize().toArray() : null, angle: o.angle ?? null }); } });
  return { glb_b64: b64, head: { matrixWorld: cur.named.ida.joints.head.matrixWorld.toArray(), H: cur.named.ida.H }, cam: { matrixWorld: cam.matrixWorld.toArray(), fov: cam.fov, aspect: cam.aspect }, lights, bg: cur.scene.background?.isColor ? cur.scene.background.toArray() : null };
}

window.renderFrame = async (name, samples) => {
  const T = cfg.T ?? (shot.t0 + shot.t1) / 2, f = Math.round(T * 24), t = T - shot.t0;
  cur.update(t, T, f);
  const cam = cur.cam, c = cfg.cam;
  if (c && c.rel) faceCam(cam, cur.named.ida, { fov: fovOf(c.mm ?? 85), ...c.rel });
  else if (c && c.pos) { cam.fov = fovOf(c.mm ?? 35); cam.position.set(...c.pos); cam.lookAt(new THREE.Vector3(...c.look)); cam.updateProjectionMatrix(); }
  cam.updateMatrixWorld(true);
  const l11 = cfg.l11 ? moveL11(cam, cfg.l11) : null;
  const u = pipe.outMat.uniforms, e0 = typeof cur.exposure === 'function' ? cur.exposure(t, T) : (cur.exposure ?? 1.0);
  u.uExp.value = typeof cfg.exp === 'number' ? cfg.exp : e0 * (cfg.expMul ?? 1);
  info = { T, f, exposure: +u.uExp.value.toFixed(4), cam: cam.position.toArray().map((v) => +v.toFixed(2)), l11, face: cur.named.ida.face?.getFace?.() };
  if (cfg.export) info.export = await exportIda(cam);
  const ms = pipe.accumulate(cur.scene, cam, samples, cur.onSample || null);
  cur.paint.apply(cur.scene, cam);
  return { accum_ms: ms, prof_ms: info };
};
window.finalize = (f) => pipe.finalize(f);

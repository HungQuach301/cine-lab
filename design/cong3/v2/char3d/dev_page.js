// Trang thử riêng của cách (1): turnaround / cận mặt / cận tay dưới đèn studio trung tính (không phải shot so sánh).
// node shared/render_still.js --page v2/char3d/dev_page.js --frame <tên> --out v2/char3d/dev --samples 4 --w 960 --h 540
//   --args '{"who":"ida|cas","view":"sheet|face|hands|back","pose":"turnaround"}'
import * as THREE from '../../shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '../../shared/post.js';
import { buildCharacter } from './cast3d.js';

let W, H, cfg, renderer, pipe, scene, cam;
const mat = (role, color, part, extra = {}) => {
  if (role === 'flame') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(20) });
  if (role === 'glass') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb85a').multiplyScalar(3), transparent: true, opacity: 0.7, depthWrite: false });
  return new THREE.MeshLambertMaterial({ color: new THREE.Color(color), side: THREE.DoubleSide, ...extra });
};
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  const sheet = await fetch('/model-sheet/' + (c.who || 'ida') + '.json').then((r) => r.json());
  renderer = createRenderer(W, H); pipe = createPipeline(renderer, W, H, { exposure: 1.0 });
  scene = new THREE.Scene(); scene.background = new THREE.Color('#5a5660');
  scene.add(new THREE.HemisphereLight('#b8c0e0', '#403830', 0.9));
  const key = new THREE.DirectionalLight('#ffe2c0', 2.4); key.position.set(2, 3, 3); key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.left = -2; key.shadow.camera.right = 2; key.shadow.camera.top = 3; key.shadow.camera.bottom = -1; key.shadow.bias = -0.0005; key.shadow.normalBias = 0.01; scene.add(key);
  const rim = new THREE.DirectionalLight('#a0b0ff', 1.0); rim.position.set(-2, 2, -3); scene.add(rim);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), new THREE.MeshLambertMaterial({ color: '#6a6660' })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const view = c.view || 'sheet', pose = sheet.poses[c.pose || 'turnaround'];
  const t0 = performance.now();
  const mk = (x, ry) => { const ch = buildCharacter(sheet, { material: mat, detail: c.detail || 32 }); ch.setPose(pose); ch.root.position.x = x; ch.root.rotation.y = ry;
    if (pose.root_y_m) ch.root.position.y = pose.root_y_m; ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); scene.add(ch.root); return ch; };
  const hh = sheet.H_m * sheet.total_height_H;
  cam = new THREE.PerspectiveCamera(30, W / H, 0.05, 100);
  if (view === 'body') { mk(0, c.ry ?? 0.35); cam.fov = 26; cam.position.set(0, hh * 0.55, 3.6); cam.lookAt(0, hh * 0.5, 0); }
  else if (view === 'sheet') { mk(-0.9, 0); mk(0, Math.PI / 2); mk(0.9, Math.PI); cam.fov = 30; cam.position.set(0, hh * 0.55, 4.6); cam.lookAt(0, hh * 0.5, 0); }
  else {
    const ch = mk(0, c.ry ?? 0.5); ch.root.updateMatrixWorld(true);
    const tgt = new THREE.Vector3(); (view === 'hands' ? ch.joints.wrist_L : ch.joints.head).getWorldPosition(tgt);
    if (view !== 'hands') tgt.y += sheet.H_m * (c.ty ?? 0.5);
    if (c.nohat) ch.root.traverse((o) => { if (o.isMesh && /hat|cap|bobble/.test(o.userData.part)) o.visible = false; });
    const d = c.d ?? (view === 'hands' ? 0.9 : 0.62); const a = c.cam ?? 0.3;
    cam.fov = 22; cam.position.set(tgt.x + Math.sin(a) * d, tgt.y + (c.camY ?? 0.05), tgt.z + Math.cos(a) * d); cam.lookAt(tgt);
    if (view === 'hands') { const a2 = c.cam ?? 0; cam.position.set(tgt.x + Math.sin(a2) * d, tgt.y + (c.camY ?? 0.0), tgt.z + Math.cos(a2) * d); cam.lookAt(tgt); }
    if (view === 'light') { const a1 = new THREE.Vector3(), b1 = new THREE.Vector3(); ch.joints.wrist_L.getWorldPosition(a1); ch.joints.wrist_R.getWorldPosition(b1); a1.add(b1).multiplyScalar(0.5); cam.fov = c.fov ?? 12; cam.position.set(-1.15, 3.17, 3.55); cam.lookAt(a1); }
    if (view === 'back') { cam.position.set(tgt.x - 0.6, tgt.y + 0.1, tgt.z - 1.5); cam.lookAt(tgt); }
  }
  cam.updateProjectionMatrix();
  scene.traverse((o) => { if (o.name === 'hand_L') { const q = new THREE.Quaternion(); o.getWorldQuaternion(q); const f = (v) => v.applyQuaternion(q).toArray().map((a) => a.toFixed(2)).join(',');
    console.log('hand_L x(palm=-x):', f(new THREE.Vector3(1, 0, 0)), ' -y(fingers):', f(new THREE.Vector3(0, -1, 0)), ' z(thumb side):', f(new THREE.Vector3(0, 0, 1)), 'scale', o.scale.x); } });
  if (c.dbg) { const seen = {}; scene.traverse((o) => { if (o.isMesh && o.userData.part) { const b = new THREE.Box3().setFromObject(o); const k = o.userData.part; if (!seen[k]) seen[k] = [9, -9]; seen[k][0] = Math.min(seen[k][0], b.min.y); seen[k][1] = Math.max(seen[k][1], b.max.y); } });
    console.log(JSON.stringify(Object.fromEntries(Object.entries(seen).map(([k, v]) => [k, v.map((a) => +a.toFixed(3))])))); }
  window._build_ms = performance.now() - t0; console.log('build ms', window._build_ms.toFixed(0));
  let nv = 0; scene.traverse((o) => { if (o.isMesh) nv += o.geometry.attributes.position.count; }); console.log('verts', nv);
};
window.renderFrame = async (name, samples) => ({ accum_ms: pipe.accumulate(scene, cam, samples) });
window.finalize = (f) => pipe.finalize(f);

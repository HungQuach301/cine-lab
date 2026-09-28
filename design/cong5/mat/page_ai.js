// W3 (Cổng 5 v2, mặt Ida A-i) — trang thử STUDIO của đầu điêu khắc + rig (không phải khung phim). Driver: design/cong5/mat/still.js.
// --args {"expr":"neutral|sad_smile|strained|choked","face":{kênh: trọng số},"vis":"A|E|O|MBP|FV|L","cam":<rad quanh đầu>,"d":<m>,"ty":<H>,
//         "camY":<m>,"nohat":1,"light":"studio|elec|gas","idaStyle":"ai|aa","exp":<phơi sáng>}
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { buildCharacter } from '/cong3/v2/char3d/cast3d.js';
import { FACE_PRESETS, VISEMES, mixW } from '/cong3/v2/char3d/facerig.js';

let W, H, cfg, renderer, pipe, scene, cam;
const mat = (role, color, part, extra = {}) => new THREE.MeshLambertMaterial({ color: new THREE.Color(color), side: THREE.DoubleSide, ...extra });
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  const sheet = await fetch('/cong3/model-sheet/ida.json').then((r) => r.json());
  renderer = createRenderer(W, H); pipe = createPipeline(renderer, W, H, { exposure: c.exp ?? 1.0 });
  scene = new THREE.Scene(); scene.background = new THREE.Color('#4a4650');
  const L = c.light || 'studio';
  if (L === 'studio') {
    scene.add(new THREE.HemisphereLight('#b8c0e0', '#403830', 0.9));
    const key = new THREE.DirectionalLight('#ffe2c0', 2.4); key.position.set(2, 3, 3); key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -1, right: 1, top: 2.5, bottom: 0.5 }); key.shadow.bias = -0.0005; key.shadow.normalBias = 0.01; scene.add(key);
    const rim = new THREE.DirectionalLight('#a0b0ff', 1.0); rim.position.set(-2, 2, -3); scene.add(rim);
  } else {   // một đèn điểm gần (đèn điện trắng lạnh / đèn khí hổ phách) + trời đêm yếu — kiểm "mắt đỏ, ma" dưới đèn điện (s39)
    scene.add(new THREE.HemisphereLight('#304060', '#201810', 0.25));
    const p = new THREE.PointLight(L === 'elec' ? '#dfe8ff' : '#ffb060', 6, 0, 2); p.position.set(0.5, 2.1, 0.9); p.castShadow = true; p.shadow.mapSize.set(1024, 1024); p.shadow.bias = -0.0006; p.shadow.normalBias = 0.02; scene.add(p);
  }
  const ch = buildCharacter(sheet, { material: mat, detail: c.detail || 36, faceQ: c.faceQ ?? 1.4, expr: c.expr, idaStyle: c.idaStyle, gaze: c.gaze || [0, -0.02] });
  ch.setPose(sheet.poses[c.pose || 'turnaround']); ch.root.rotation.y = c.ry ?? 0;
  if (c.face || c.vis) ch.setFace(mixW(FACE_PRESETS[c.expr] || {}, c.face || {}, VISEMES[c.vis] || {}));
  ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  if (c.nohat) ch.root.traverse((o) => { if (o.isMesh && /hat/.test(o.userData.part)) o.visible = false; });
  if (c.hide) ch.root.traverse((o) => { if (o.isMesh && new RegExp(c.hide).test(o.userData.part)) o.visible = false; });   // chẩn đoán
  scene.add(ch.root); ch.root.updateMatrixWorld(true);
  const tgt = new THREE.Vector3(); ch.joints.head.getWorldPosition(tgt); tgt.y += sheet.H_m * (c.ty ?? 0.5);
  const d = c.d ?? 0.62, a = c.cam ?? 0.3;
  cam = new THREE.PerspectiveCamera(c.fov ?? 22, W / H, 0.05, 100); cam.position.set(tgt.x + Math.sin(a) * d, tgt.y + (c.camY ?? 0.03), tgt.z + Math.cos(a) * d); cam.lookAt(tgt); cam.updateProjectionMatrix();
};
window.renderFrame = async (name, samples) => ({ accum_ms: pipe.accumulate(scene, cam, samples) });
window.finalize = (f) => pipe.finalize(f);

// Model sheet Ida & Cas — trang render cho shared/render_still.js.
// Khung: '<ida|cas>_<view>' (turnaround: front, q34, side, back) hoặc '<ida|cas>_pose_<tên tư thế>';
// tiền tố 'sil_' = silhouette đen đặc trên nền trắng (kiểm C2), không hậu kỳ.
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { buildCharacter, buildLadder } from '../shared/cast.js';
import { buildGasLamp } from '../shared/props.js';
import { createPipeline, createRenderer } from '../shared/post.js';

let W, H, renderer, pipe, scene, cam, chars = {}, sil = false, ground, backdrop, keyL;
const VIEW = { front: 0, q34: -38, side: 90, back: 180 };
const POSE_VIEW = { walk_ladder: 90, warm_hands: 70, crouch_lantern: 60, look_shadows: -30, shadow_bird: 180, look_lantern: -30, hold_ladder: 70, warm_hands_copy: 70, half_raised: 150 };

window.setup = async (cfg) => {
  W = cfg.W; H = cfg.H;
  const [ida, cas] = await Promise.all(['model-sheet/ida.json', 'model-sheet/cas.json'].map((p) => fetch('/' + p).then((r) => r.json())));
  renderer = createRenderer(W, H);
  scene = new THREE.Scene();
  chars.ida = buildCharacter(ida, { detail: 28 }); chars.cas = buildCharacter(cas, { detail: 28 });
  // Nền studio: phông xám ấm cong, đèn key/fill/rim trung tính (không phải ánh sáng phim).
  backdrop = new THREE.Mesh(new THREE.PlaneGeometry(20, 12), new THREE.MeshStandardMaterial({ color: '#8f8a84', roughness: 1 }));
  backdrop.position.set(0, 3, -3); backdrop.receiveShadow = true; scene.add(backdrop);
  ground = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), new THREE.MeshStandardMaterial({ color: '#9a948d', roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  scene.add(new THREE.HemisphereLight('#dfe6ee', '#5b544d', 0.9));
  keyL = new THREE.DirectionalLight('#fff4e6', 2.4); keyL.position.set(3, 5, 4); keyL.castShadow = true;
  keyL.shadow.mapSize.set(2048, 2048); Object.assign(keyL.shadow.camera, { left: -2, right: 2, top: 3, bottom: -1, near: 0.1, far: 20 }); keyL.shadow.bias = -0.0005; scene.add(keyL);
  const rim = new THREE.DirectionalLight('#dbe8ff', 1.2); rim.position.set(-3, 3, -4); scene.add(rim);
  const aspect = W / H, vh = 2.15;
  cam = new THREE.OrthographicCamera(-vh * aspect / 2, vh * aspect / 2, vh / 2, -vh / 2, 0.1, 50);
  cam.position.set(0, 0.95, 10); cam.lookAt(0, 0.95, 0);
  pipe = createPipeline(renderer, W, H, { exposure: 1.0 });
};

let extraProps = [], wallStage = false;
// Dàn đạo cụ theo ngữ cảnh (pose.stage): cột đèn khí phía trước, thang tựa cột; khung nhìn cao hơn khi có cột đèn.
function setView(vh, camY) { const a = W / H; Object.assign(cam, { left: -vh * a / 2, right: vh * a / 2, top: vh / 2, bottom: -vh / 2 }); cam.position.set(0, camY, 10); cam.lookAt(0, camY, 0); cam.updateProjectionMatrix(); }
window.renderFrame = async (name, samples) => {
  sil = name.startsWith('sil_'); const n = sil ? name.slice(4) : name;
  const [who, ...rest] = n.split('_'); const key = rest.join('_');
  for (const c of Object.values(chars)) c.root.parent && c.root.parent.remove(c.root);
  for (const p of extraProps) p.parent && p.parent.remove(p); extraProps = [];
  const ch = chars[who];
  let yaw = 0, st = {};
  const holder = new THREE.Group(); scene.add(holder); extraProps.push(holder); holder.add(ch.root);
  if (key.startsWith('pose_')) { const p = key.slice(5), pose = ch.sheet.poses[p]; ch.setPose(pose); st = pose.stage || {}; yaw = st.view ?? POSE_VIEW[p] ?? 0;
    if (pose.root_y_m) ch.root.position.y += pose.root_y_m;
    if (st.lamp_z != null) { const lamp = buildGasLamp({ height: 3.4 }); lamp.position.set(0, 0, st.lamp_z); holder.add(lamp); }
    if (st.ladder_lean) { const lad = buildLadder(1.8, 0.34, 6, (r, c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.8 }), '#8a6a45');
      lad.position.set(0, 0, -0.35); lad.rotation.x = 0.36; holder.add(lad); ch.root.position.z = -0.08; }
    if (p === 'hold_ladder') { const lad = buildLadder(1.8, 0.34, 6, (r, c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.8 }), '#8a6a45'); lad.position.set(0, 0, 0.40); lad.rotation.x = -0.10; holder.add(lad); }
  } else { ch.setPose(ch.sheet.poses.turnaround); yaw = VIEW[key] ?? 0; }
  holder.rotation.y = yaw * Math.PI / 180; ch.root.rotation.y = 0; holder.updateMatrixWorld(true);
  // Canh khung tự động theo hộp bao người + đạo cụ (không cắt đạo cụ), giữ tỷ lệ cố định cho turnaround.
  if (key.startsWith('pose_')) { const bb = new THREE.Box3().setFromObject(holder), sz = bb.getSize(new THREE.Vector3()), c = bb.getCenter(new THREE.Vector3());
    const vh = Math.max(2.15, sz.y * 1.12, (Math.max(sz.x, sz.z) * 1.15) / (W / H)); const a = W / H;
    Object.assign(cam, { left: -vh * a / 2, right: vh * a / 2, top: vh / 2, bottom: -vh / 2 }); cam.position.set(c.x, c.y, 10); cam.lookAt(c.x, c.y, 0); cam.updateProjectionMatrix();
  } else setView(2.15, 0.95);
  wallStage = !!st.wall_shadow;
  if (wallStage) { // tường vôi phía trước Cas (theo hướng mặt nhân vật) + nguồn điểm phía sau-trên: bóng chim hiện trên tường
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(4, 3.2), new THREE.MeshLambertMaterial({ color: 0xffffff })); wall.receiveShadow = true;
    wall.position.set(0, 1.6, 0.55); wall.rotation.y = Math.PI; holder.add(wall);
    const L = new THREE.PointLight(0xffffff, 60, 0, 2); L.position.set(-3.0, 2.0, -1.6); L.castShadow = true; L.shadow.mapSize.set(2048, 2048); L.shadow.bias = -0.0005; holder.add(L);
    holder.updateMatrixWorld(true);
    // trung cảnh nửa người trên (như khung b): canh giữa đôi tay và bóng chim trên tường
    const hw = new THREE.Vector3(); chars.cas.joints.wrist_R.getWorldPosition(hw); const lw = new THREE.Vector3(); L.getWorldPosition(lw);
    const wz = new THREE.Vector3(); wall.getWorldPosition(wz); const k = (wz.z - lw.z) / (hw.z - lw.z); const sh = lw.clone().add(hw.clone().sub(lw).multiplyScalar(k));
    const cx = (hw.x + sh.x) / 2, cy = hw.y - 0.25, a2 = W / H, vh = Math.max(1.6, (Math.abs(hw.x - sh.x) + 0.9) / a2);
    Object.assign(cam, { left: -vh * a2 / 2, right: vh * a2 / 2, top: vh / 2, bottom: -vh / 2 }); cam.position.set(cx, cy, 10); cam.lookAt(cx, cy, 0); cam.updateProjectionMatrix();
  }
  if (sil) return { accum_ms: 0 };
  const ms = pipe.accumulate(scene, cam, samples);
  return { accum_ms: ms };
};

const BLACK = new THREE.MeshBasicMaterial({ color: 0x000000 });
window.finalize = (f) => {
  if (!sil) return pipe.finalize(f);
  // Silhouette: chỉ nhân vật + đạo cụ, tô đen đặc, nền trắng, không grain.
  if (wallStage) { // silhouette có ngữ cảnh: nhân vật đen đặc; tường sáng nhận bóng chim; không grain
    const hid = [backdrop, ground]; hid.forEach((m) => (m.visible = false)); const saved = [];
    chars.cas.root.traverse((o) => { if (o.isMesh) { saved.push([o, o.material]); o.material = BLACK; } });
    const amb = scene.children.filter((o) => o.isLight && o.parent === scene); amb.forEach((l) => (l.visible = false));
    renderer.setRenderTarget(null); renderer.setClearColor(0xffffff, 1); renderer.clear(); renderer.render(scene, cam);
    saved.forEach(([o, m]) => (o.material = m)); amb.forEach((l) => (l.visible = true)); hid.forEach((m) => (m.visible = true));
    const gl = renderer.getContext(); const px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const rgb = new Uint8Array(W * H * 3); for (let i = 0, j = 0; i < px.length; i += 4, j += 3) { const v = px[i] > 110 ? 255 : 0; rgb[j] = rgb[j + 1] = rgb[j + 2] = v; }
    let bin = ''; for (let i = 0; i < rgb.length; i += 0x8000) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + 0x8000)); return btoa(bin);
  }
  const hidden = [backdrop, ground]; hidden.forEach((m) => (m.visible = false));
  scene.overrideMaterial = BLACK; renderer.setRenderTarget(null); renderer.setClearColor(0xffffff, 1); renderer.clear();
  renderer.render(scene, cam); scene.overrideMaterial = null; hidden.forEach((m) => (m.visible = true));
  const gl = renderer.getContext(); const px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
  const rgb = new Uint8Array(W * H * 3); for (let i = 0, j = 0; i < px.length; i += 4, j += 3) { rgb[j] = px[i]; rgb[j + 1] = px[i + 1]; rgb[j + 2] = px[i + 2]; }
  let bin = ''; for (let i = 0; i < rgb.length; i += 0x8000) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + 0x8000));
  return btoa(bin);
};

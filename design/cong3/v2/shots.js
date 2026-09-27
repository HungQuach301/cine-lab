// Cổng 3 v2 — ba shot mới theo hướng C "Painted Glow" (bối cảnh, ánh sáng CHUNG cho mọi cách làm nhân vật).
//  a_close_ida : cận mặt Ida đứng trên thang, hơ tay trên lồng đèn khí (cảnh 1/3). Key = ngọn lửa đèn khí (ấm, gần);
//                fill = trời xanh chạng vạng (lạnh, từ trên/sau → viền lạnh). DOF thật bằng jitter khẩu độ.
//  b_cas_bird  : trung cảnh Cas làm chim bóng trên tường nhà kho, dưới ngọn khí số 11 (cảnh 4, trước khi cột điện cuối bật).
//  walk        : Ida vác thang đi qua 2 cột đèn khí (máy tĩnh), 4 s = 96 khung; bóng người đổi phía khi qua mỗi cột (luật thế giới 2).
// Nhân vật do module ngoài dựng (mkChar), nhận vật liệu từ cảnh qua opts.material(role, color, part, extra) để cùng một ánh sáng.
// Đơn vị mét, y lên. Đèn khí: lửa ở y ≈ 3,17 m (buildGasLamp height 3,4).
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { buildGasLamp } from '../shared/props.js';
import { buildLadder } from '../shared/cast.js';
import { walkPose, WALK } from '../shared/anim.js';
import { limewashTex, flagTex, glowSprite, planarUV, rng, canvasTex, blotches } from '../dir-C/common.js';

const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
export const GAS = { color: '#ffae5c', cd: 9.0, glass: 0.10 };        // đèn khí: cường độ (cd), bán kính jitter nguồn trong lồng kính (m)
const flickAt = (f) => 1 + 0.04 * (0.6 * Math.sin(f * 0.21) + 0.4 * Math.sin(f * 0.083 + 1.3));   // lửa thở ±4 % (luật 2)

function charMat(role, color, part, extra = {}) {
  if (role === 'flame') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) });
  if (role === 'glass') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb85a').multiplyScalar(4.0), transparent: true, opacity: 0.7, depthWrite: false });
  return new THREE.MeshLambertMaterial({ color: new THREE.Color(color), side: THREE.DoubleSide, ...extra });
}
const lamMat = (o) => new THREE.MeshLambertMaterial(o);

// Trời chạng vạng / đêm: bán cầu lớn tô gradient (không nhận fog, không bóng).
function skyDome(stops) {
  const tex = canvasTex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([t, c]) => gr.addColorStop(t, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); }, { repeat: false });
  const m = new THREE.Mesh(new THREE.SphereGeometry(400, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2 + 0.2), new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide, fog: false, depthWrite: false }));
  m.userData.noG = false; return m;
}
// Dãy nhà giản lược (khối, mái dốc, cửa sổ ấm lác đác) — nền xa.
function rowHouses(R, x0, x1, z, depthMin, colorBase, winChance, winColor) {
  const g = new THREE.Group(); let x = x0;
  const wall = lamMat({ color: colorBase }), roof = lamMat({ color: '#2a2433' }), win = new THREE.MeshBasicMaterial({ color: new THREE.Color(winColor).multiplyScalar(1.6) });
  while (x < x1) {
    const w = 3.4 + R() * 3, h = 5 + R() * 5, d = depthMin + R() * 3;
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wall); b.position.set(x + w / 2, h / 2, z - d / 2); g.add(b);
    const r = new THREE.Mesh(new THREE.CylinderGeometry(0.01, d * 0.72, 2.0 + R() * 1.4, 4, 1), roof); r.rotation.y = Math.PI / 4; r.scale.set(w / d, 1, 1); r.position.set(x + w / 2, h + 1.0, z - d / 2); g.add(r);
    if (R() < 0.7) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.4, 1.3, 0.4), roof); c.position.set(x + w * (0.2 + 0.6 * R()), h + 1.6, z - d / 2); g.add(c); }
    for (let wy = 1.2; wy < h - 0.8; wy += 1.7) for (let wx = 0.7; wx < w - 0.5; wx += 1.3) {
      const on = R() < winChance; const q = new THREE.Mesh(new THREE.PlaneGeometry(0.55, 0.85), on ? win : lamMat({ color: '#1e1a24' })); q.position.set(x + wx, wy, z + 0.02); g.add(q);
    }
    x += w + 0.05;
  }
  return g;
}
function addLamp(scene, pos, frame, { shadow = true, mapSize = 1024 } = {}) {
  const lamp = buildGasLamp({ height: 3.4, mat: (role, c) => role === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) })
    : role === 'glass' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc070').multiplyScalar(2.6), transparent: true, opacity: 0.55, depthWrite: false }) : lamMat({ color: c }) });
  lamp.position.copy(pos); scene.add(lamp); lamp.updateMatrixWorld(true);
  const fp = new THREE.Vector3(); lamp.userData.flame.getWorldPosition(fp);
  const L = new THREE.PointLight(GAS.color, GAS.cd * flickAt(frame), 0, 2); L.position.copy(fp);
  if (shadow) { L.castShadow = true; L.shadow.mapSize.set(mapSize, mapSize); L.shadow.bias = -0.0006; L.shadow.normalBias = 0.02; L.shadow.camera.near = 0.08; }
  scene.add(L);
  const gc = glowSprite('#ffc57a', 1.6, 0.6); gc.position.copy(fp); scene.add(gc);
  const gw = glowSprite('#ff9a4a', 0.22, 3.2); gw.position.copy(fp); scene.add(gw);
  lamp.traverse((o) => { if (o.isMesh) { o.castShadow = o.material.type !== 'MeshBasicMaterial'; o.receiveShadow = true; } });
  return { lamp, L, fp };
}
const hal = (i, b) => { let f = 1, r = 0; while (i > 0) { f /= b; r += f * (i % b); i = Math.floor(i / b); } return r; };
function jitterLights(lights, i, n, radius) {
  for (const { L, fp } of lights) { if (n <= 1) { L.position.copy(fp); continue; }
    L.position.set(fp.x + (hal(i + 1, 2) - 0.5) * radius, fp.y + (hal(i + 1, 3) - 0.5) * radius, fp.z + (hal(i + 1, 5) - 0.5) * radius); }
}
function readyChar(ch, scene) { ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); ch.root.userData.imp = 1; scene.add(ch.root); return ch; }

// ---------------- a) cận mặt Ida ----------------
export async function buildCloseIda(ida, mkChar, upd, frame = 0) {
  const scene = new THREE.Scene(); const R = rng(31);
  scene.add(skyDome([[0, '#2c2d5c'], [0.55, '#5b4a78'], [0.82, '#b0708a'], [1, '#d99a86']]));
  scene.fog = new THREE.Fog('#6a5680', 18, 120);
  const bg = rowHouses(R, -40, 40, -22, 6, '#4e4358', 0.12, '#ffb35a'); scene.add(bg);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), lamMat({ color: '#3a3240' })); ground.rotation.x = -Math.PI / 2; scene.add(ground);
  scene.add(new THREE.HemisphereLight('#7c78c0', '#2a2030', 0.55));
  const rim = new THREE.DirectionalLight('#9aa0e8', 0.55); rim.position.set(-3, 5, -6); scene.add(rim);          // trời sáng phía sau lưng Ida → viền lạnh
  const lamps = [addLamp(scene, new THREE.Vector3(0, 0, 0), frame, { mapSize: 2048 })];
  const far = addLamp(scene, new THREE.Vector3(-9, 0, -8), frame, { shadow: false });                                // ngọn đèn xa, nhoè hậu cảnh
  // thang tựa cột, Ida đứng trên thang, mặt quay vào lồng đèn (+z → đèn ở z=+0,5 so với Ida)
  const lad = buildLadder(1.8, 0.34, 6, (r, c) => lamMat({ color: c }), '#8a6a45'); lad.position.set(0, 0, -0.85); lad.rotation.x = 0.36; scene.add(lad);
  const ch = readyChar(mkChar(ida, { material: charMat, detail: 36 }), scene);
  const pose = ida.poses.warm_hands_ladder; ch.setPose(pose); ch.root.position.set(0, pose.root_y_m, -0.58); ch.root.updateMatrixWorld(true);
  // máy quay: ngang tầm mặt, lệch 40° về phải-trước, 60 mm (FOV dọc ~22°)
  const head = new THREE.Vector3(); ch.joints.head.getWorldPosition(head); head.y += 0.12;
  const cam = new THREE.PerspectiveCamera(17, 16 / 9, 0.05, 500);   // ~85 mm
  const base = head.clone().add(new THREE.Vector3(1.55, 0.02, 1.35)); cam.position.copy(base); cam.lookAt(head.clone().add(new THREE.Vector3(0.14, -0.08, 0.22)));
  const focusD = base.distanceTo(head), aperture = 0.018;                                                            // bán kính khẩu độ ~f/2,8 tương đương
  const fwd = new THREE.Vector3(), right = new THREE.Vector3(), up = new THREE.Vector3(); cam.getWorldDirection(fwd); right.crossVectors(fwd, Y).normalize(); up.crossVectors(right, fwd);
  const focusP = base.clone().add(fwd.clone().multiplyScalar(focusD));
  const onSample = (i, n) => {
    if (upd) upd(ch, cam);
    jitterLights(lamps, i, n, GAS.glass);
    if (n > 1) { const a = 2 * Math.PI * hal(i + 1, 2), r = aperture * Math.sqrt(hal(i + 1, 3)); cam.position.copy(base).addScaledVector(right, Math.cos(a) * r).addScaledVector(up, Math.sin(a) * r); cam.lookAt(focusP); }
  };
  if (upd) upd(ch, cam);
  return { scene, cam, onSample, chars: [ch], paintP: { rNear: 2.5, rFar: 6.0, dNear: 1.2, dFar: 25, impScale: 0.35, stroke: 0.035, halation: 0.14, bloomWide: 0.06 } };
}

// ---------------- b) Cas làm chim bóng ----------------
export async function buildCasBird(cas, mkChar, upd, frame = 0) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#0d0c16');
  scene.add(skyDome([[0, '#0f1030'], [0.7, '#1f1c40'], [1, '#2e2548']]));
  const wallTex = limewashTex(41, { metres: 6, grime: true, brick: 0.06 });
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(12, 7), lamMat({ color: '#ffffff', map: wallTex })); wall.position.set(0, 3.5, 0); wall.receiveShadow = true; planarUV(wall.geometry, X, Y, 6, [0.3, 0]); scene.add(wall);
  const plinth = new THREE.Mesh(new THREE.BoxGeometry(12, 0.42, 0.08), lamMat({ color: '#8d877f' })); plinth.position.set(0, 0.21, 0.04); plinth.receiveShadow = true; scene.add(plinth);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(14, 12), lamMat({ color: '#ffffff', map: flagTex(7, { metres: 4 }) })); ground.rotation.x = -Math.PI / 2; ground.position.z = 6; planarUV(ground.geometry, X, Z, 4, [0, 0]); ground.receiveShadow = true; scene.add(ground);
  scene.add(new THREE.HemisphereLight('#3a3c78', '#15121c', 0.30));
  const lamps = [addLamp(scene, new THREE.Vector3(-1.0, 0, 4.5), frame, { mapSize: 2048 })];
  // cột điện kiểu mới cạnh tường, CHƯA bật (tấm kính tối) — cảnh 4 trước khi khối cuối chuyển
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.09, 7, 16), lamMat({ color: '#3f434c' })); post.position.set(2.4, 3.5, 1.1); post.castShadow = true; scene.add(post);
  const panel = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.5, 0.12), lamMat({ color: '#2c2f38' })); panel.position.set(2.4, 7.0, 1.1); scene.add(panel);
  const ch = readyChar(mkChar(cas, { material: charMat, detail: 32 }), scene);
  ch.setPose(cas.poses.shadow_bird); ch.root.position.set(0.15, 0, 0.95); ch.root.rotation.y = Math.PI + 0.15; ch.root.updateMatrixWorld(true);
  // máy quay: 3/4 sau-phải Cas, ngang ngực người lớn, thấy Cas và chim trên tường
  const cam = new THREE.PerspectiveCamera(30, 16 / 9, 0.05, 500);
  cam.position.set(2.1, 1.4, 3.3); cam.lookAt(0.5, 1.45, 0.3);
  const onSample = (i, n) => { if (upd) upd(ch, cam); jitterLights(lamps, i, n, GAS.glass); };
  if (upd) upd(ch, cam);
  return { scene, cam, onSample, chars: [ch], paintP: { rNear: 3.0, rFar: 6.0, dNear: 2, dFar: 20, impScale: 0.4, stroke: 0.04, halation: 0.12, bloomWide: 0.06 } };
}

// ---------------- walk: Ida vác thang qua 2 cột đèn ----------------
export const WALK_SHOT = { frames: 96, x0: 3.7, lampsX: [2.3, -0.9], z: 0.4 };
export async function buildWalk(ida, mkChar, upd) {
  const scene = new THREE.Scene(); const R = rng(53);
  scene.add(skyDome([[0, '#1d1f4a'], [0.6, '#3c3566'], [0.88, '#7a5a80'], [1, '#a8708a']]));
  scene.fog = new THREE.Fog('#4a4068', 14, 90);
  const street = new THREE.Mesh(new THREE.PlaneGeometry(40, 12), lamMat({ color: '#ffffff', map: flagTex(3, { metres: 4 }) })); street.rotation.x = -Math.PI / 2; street.position.z = 1; planarUV(street.geometry, X, Z, 1.6, [0, 0]); street.receiveShadow = true; scene.add(street);
  // mặt tiền dãy nhà sát phố (vôi), cửa sổ tối/ấm, cửa gỗ
  const fac = new THREE.Mesh(new THREE.PlaneGeometry(40, 6.2), lamMat({ color: '#ffffff', map: limewashTex(61, { metres: 8, grime: true, brick: 0.08, base: '#cfc6ba' }) })); fac.position.set(0, 3.1, -2.6);
  const eave = new THREE.Mesh(new THREE.BoxGeometry(40, 0.25, 0.5), lamMat({ color: '#2a2433' })); eave.position.set(0, 6.3, -2.45); scene.add(eave); planarUV(fac.geometry, X, Y, 8, [0, 0]); fac.receiveShadow = true; scene.add(fac);
  for (let x = -12; x < 14; x += 2.6) { const on = R() < 0.3;
    const w = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 1.1), on ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb35a').multiplyScalar(1.3) }) : lamMat({ color: '#241f2a' })); w.position.set(x, R() < 0.5 ? 4.6 : 3.2, -2.58); scene.add(w); }
  for (let x = -10; x < 12; x += 5.2) { const d = new THREE.Mesh(new THREE.BoxGeometry(1.0, 2.1, 0.08), lamMat({ color: '#4a3226' })); d.position.set(x + 1.3, 1.05, -2.56); d.receiveShadow = true; scene.add(d); }
  const roofs = rowHouses(R, -30, 30, -9, 5, '#4a4058', 0.1, '#ffb35a'); scene.add(roofs);
  scene.add(new THREE.HemisphereLight('#5c5aa8', '#221b2a', 0.35));
  const lamps = WALK_SHOT.lampsX.map((x) => addLamp(scene, new THREE.Vector3(x, 0, -1.1), 0));
  const ch = readyChar(mkChar(ida, { material: charMat, detail: 28 }), scene);
  const base = ida.poses.walk_ladder;
  // máy tĩnh: ngang 1,5 m, 35 mm tương đương (FOV dọc 38°), hơi chéo
  const cam = new THREE.PerspectiveCamera(38, 16 / 9, 0.05, 500);
  cam.position.set(0.9, 1.6, 8.6); cam.lookAt(0.9, 2.2, 0);
  let fNow = 0;
  const setT = (t) => {
    const p = walkPose(t, base); ch.setPose(p);
    ch.root.position.set(WALK_SHOT.x0 - WALK.speed_mps * t, p.root_y_m, WALK_SHOT.z); ch.root.rotation.y = -Math.PI / 2; ch.root.updateMatrixWorld(true);
  };
  // Motion blur: mỗi mẫu một thời điểm trong màn trập 180° (1/48 s), thứ tự bắt đầu từ giữa; đèn jitter; lửa thở theo khung.
  const onSample = (i, n) => {
    const off = n <= 1 ? 0 : (((i + (n >> 1)) % n) + 0.5) / n - 0.5;
    setT((fNow + 0.5 * off) / 24);
    if (upd) upd(ch, cam);
    jitterLights(lamps, i, n, GAS.glass);
  };
  const setFrame = (f) => { fNow = f; for (const l of lamps) l.L.intensity = GAS.cd * flickAt(f); setT(f / 24); if (upd) upd(ch, cam); };
  setFrame(0);
  return { scene, cam, onSample, setFrame, chars: [ch], paintP: { rNear: 3.0, rFar: 6.5, dNear: 3, dFar: 40, impScale: 0.4, stroke: 0.04, halation: 0.14, bloomWide: 0.06 } };
}

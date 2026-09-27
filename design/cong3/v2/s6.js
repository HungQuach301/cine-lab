// Cổng 3 v3 — khung phong cách cảnh 6 (hai khung, cùng một bộ phố):
//  d_s6_alley: Ida đứng trong CON NGÕ KHUẤT ĐÈN ĐIỆN dưới cửa sổ nhà Cas (luật thế giới 3.4, 3.5). Nguồn ấm duy nhất: đèn lồng trên bậu cửa sổ
//              (trong phòng Cas), tia chỉ lọt qua ô cửa → SpotLight có bóng, nón vừa khung cửa. Nguồn cao nên bóng Ida NGẮN, NHẠT, đổ xuống nền,
//              ngả ra xa tường. Ánh điện ngoài phố chỉ lọt vào miệng ngõ, giảm theo hàm mũ độ sâu (shader chung với s5, uMouthZ/uSpillL).
//  e_ending:   Toàn cảnh phố trắng dưới đèn điện (tràn phẳng, KHÔNG bóng, luật 2) và MỘT ô cửa vàng: cửa sổ nhà Cas. Ida nhỏ ở miệng ngõ.
// Không đèn giả: mọi ánh sáng có nguồn trong hình (cột đèn điện, ô cửa, bầu trời đêm).
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { limewashTex, flagTex, glowSprite, planarUV, rng } from '../dir-C/common.js';
import { U, patch } from './s5.js';

const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
const lam = (o) => patch(new THREE.MeshLambertMaterial(o));
export const ALLEY = { halfW: 0.85, mouthZ: 6.0, backZ: -9, winY: 4.3, winZ: 0.0, winW: 0.8, winH: 1.0 };
const WARM = new THREE.Color('#ffae5c');

function charMat(role, color, extra = {}) {
  if (role === 'flame') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) });
  if (role === 'glass') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb85a').multiplyScalar(4.0), transparent: true, opacity: 0.7, depthWrite: false });
  const c = new THREE.Color(color); if (role === 'hair') c.multiplyScalar(0.45);
  return lam({ color: c, side: THREE.DoubleSide, ...extra });
}
function sky() {
  const cv = document.createElement('canvas'); cv.width = 8; cv.height = 512; const g = cv.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 512); gr.addColorStop(0, '#0b0d22'); gr.addColorStop(0.7, '#1a1c3c'); gr.addColorStop(1, '#2c2a4a'); g.fillStyle = gr; g.fillRect(0, 0, 8, 512);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.SphereGeometry(400, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2 + 0.2), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide, fog: false, depthWrite: false }));
}
const box = (w, h, d, mat, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; return m; };

// Phố: trục x dọc mặt tiền (z = mouthZ là mép mặt tiền), ngõ cắt vuông góc đi vào −z giữa hai khối nhà.
function buildStreet(scene, R) {
  const A = ALLEY;
  const wallT = limewashTex(71, { metres: 6, grime: true, brick: 0.07, base: '#e4ddd0' });
  const wall = lam({ color: '#ffffff', map: wallT });
  // hai vách ngõ (mặt quay vào ngõ), cao 7 m
  for (const sx of [-1, 1]) {
    const w = new THREE.Mesh(new THREE.PlaneGeometry(A.mouthZ - A.backZ, 7), wall); w.rotation.y = -sx * Math.PI / 2;
    w.position.set(sx * A.halfW, 3.5, (A.mouthZ + A.backZ) / 2); planarUV(w.geometry, X, Y, 6, [sx * 0.3, 0]); w.receiveShadow = true; w.castShadow = sx > 0; scene.add(w);   // vách trái có ô cửa: không đổ bóng (khẩu độ do tường phòng vô hình lo)
  }
  const back = new THREE.Mesh(new THREE.PlaneGeometry(A.halfW * 2, 7), wall); back.position.set(0, 3.5, A.backZ); back.receiveShadow = true; scene.add(back);
  // nền đá ngõ + phố
  const flag = lam({ color: '#ffffff', map: flagTex(9, { metres: 4 }) });
  const g1 = new THREE.Mesh(new THREE.PlaneGeometry(A.halfW * 2, A.mouthZ - A.backZ), flag); g1.rotation.x = -Math.PI / 2; g1.position.set(0, 0, (A.mouthZ + A.backZ) / 2); planarUV(g1.geometry, X, Z, 2.5, [0, 0]); g1.receiveShadow = true; scene.add(g1);
  const g2 = new THREE.Mesh(new THREE.PlaneGeometry(140, 16), flag); g2.rotation.x = -Math.PI / 2; g2.position.set(0, -0.005, A.mouthZ + 8); planarUV(g2.geometry, X, Z, 2.5, [0, 0]); g2.receiveShadow = true; scene.add(g2);
  // mặt tiền hai bên ngõ (z = mouthZ, quay ra phố) + dãy nhà đối diện (z = mouthZ + 14, quay vào)
  // Dãy nhà: từng nếp nhà (rộng 4–7 m, cao 5,5–8,5 m), mặt tiền vôi, mái dốc tối, ống khói; cửa sổ tối, trừ MỘT ô vàng (gold).
  const LW = [0, 1, 2, 3].map((k) => lam({ color: '#ffffff', map: limewashTex(91 + k * 13, { metres: 6, grime: true, brick: 0.05, base: k % 2 ? '#e2dccd' : '#ece6da' }) }));
  const roofM = lam({ color: '#2a2433' }), darkWin = lam({ color: '#2a2a36' }), doorM = lam({ color: '#4a3226' });
  const houses = (x0, x1, z, face, seed, gold, minHNear) => {
    const Rh = rng(seed); let x = x0; const ry = face < 0 ? Math.PI : 0;
    while (x < x1 - 0.5) {
      const w = Math.min(x1 - x, 4 + Rh() * 3), near = minHNear && Math.abs(x + w / 2 - minHNear[0]) < 4;
      const h = near ? minHNear[1] : 5.5 + Rh() * 3, d = 7, cx = x + w / 2;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), LW[Math.floor(Rh() * 4)]);
      m.position.set(cx, h / 2, z); m.rotation.y = ry; planarUV(m.geometry, X, Y, 9.5, [x * 0.1, 0]); m.receiveShadow = true; scene.add(m);   // chu kỳ texture > chiều cao nhà: không lộ đường nối
      const r = new THREE.Mesh(new THREE.CylinderGeometry(0.01, d * 0.72, 2.2 + Rh() * 1.2, 4, 1), roofM); r.rotation.y = Math.PI / 4; r.scale.set(w / d, 1, 1);
      r.position.set(cx, h + 1.1, z - face * d / 2); scene.add(r);
      if (Rh() < 0.75) scene.add(box(0.45, 1.4, 0.45, roofM, x + w * (0.2 + 0.6 * Rh()), h + 1.5, z - face * d * 0.4));
      for (let wx = x + 1.0; wx < x + w - 0.6; wx += 1.9) for (let wy = 2.0; wy < h - 1.0; wy += 2.3) {
        if (gold && Math.abs(wx - gold[0]) < 1.0 && Math.abs(wy - gold[1]) < 1.2) continue;   // chỗ của ô vàng
        const win = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 1.1), darkWin); win.position.set(wx, wy, z + face * 0.01); win.rotation.y = ry; scene.add(win);
      }
      if (Rh() < 0.6) scene.add(box(1.0, 2.1, 0.08, doorM, x + w * 0.5, 1.05, z + face * 0.04));
      x += w;
    }
    if (gold) { const g = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 1.1), new THREE.MeshBasicMaterial({ color: WARM.clone().multiplyScalar(1.6) })); g.position.set(gold[0], gold[1], z + face * 0.03); g.rotation.y = ry; scene.add(g);
      scene.add(box(0.96, 1.26, 0.04, lam({ color: '#3a2e2a' }), gold[0], gold[1], z + face * 0.005)); }
  };
  houses(-60, -A.halfW, A.mouthZ, 1, 81, [-2.0, 4.3], [-3.0, 7.2]);   // ô vàng: phòng góc nhà Cas (cùng phòng với cửa sổ trên ngõ)
  houses(A.halfW, 60, A.mouthZ, 1, 83, null, [3.0, 7.2]);
  houses(-60, 60, A.mouthZ + 14, -1, 85, null, null);
  // cột đèn điện ngoài phố: đầu đèn trắng lạnh (phát sáng), ánh tràn phẳng do shader (uEo) mô tả — không bóng
  const posts = [];
  for (const x of [-21, -9, 3.5, 16, 28]) {
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.09, 6.5, 16), lam({ color: '#3f434c' })); p.position.set(x, 3.25, A.mouthZ + 2.2); scene.add(p);
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.18, 0.3), new THREE.MeshBasicMaterial({ color: new THREE.Color('#e8f0ff').multiplyScalar(6) })); head.position.set(x, 6.55, A.mouthZ + 2.2); scene.add(head);
    const gl = glowSprite('#dfe8ff', 0.5, 2.2); gl.position.copy(head.position); scene.add(gl); posts.push(head);
  }
  // CỬA SỔ NHÀ CAS trên vách trái của ngõ: khung tối, lòng cửa phát sáng ấm (thấy từ ngõ)
  const winFrame = box(0.12, A.winH + 0.16, A.winW + 0.16, lam({ color: '#3a2e2a' }), -A.halfW - 0.02, A.winY, A.winZ); scene.add(winFrame);
  const pane = new THREE.Mesh(new THREE.PlaneGeometry(A.winW, A.winH), new THREE.MeshBasicMaterial({ color: WARM.clone().multiplyScalar(2.2) }));
  pane.position.set(-A.halfW + 0.045, A.winY, A.winZ); pane.rotation.y = Math.PI / 2; scene.add(pane);
  const sill = box(0.22, 0.06, A.winW + 0.2, lam({ color: '#6e645a' }), -A.halfW + 0.08, A.winY - A.winH / 2 - 0.03, A.winZ); scene.add(sill);
  return { posts, pane };
}

export async function buildS6(ida, cas, dbg = {}, mkChar, charUpdate, which = 'alley') {
  const A = ALLEY, R = rng(66);
  const scene = new THREE.Scene(); scene.add(sky()); scene.fog = new THREE.Fog('#1a1c34', 30, 140);
  buildStreet(scene, R);

  // Nguồn ấm: đèn lồng trên bậu, TRONG phòng, sát ô cửa; tia chỉ lọt qua ô cửa → hướng xuống ngõ.
  const lp = new THREE.Vector3(-A.halfW - 0.1, A.winY - A.winH / 2 + 0.2, A.winZ);   // ngọn lửa đèn lồng đặt trên bậu, sát mép trong ô cửa
  const spot = new THREE.SpotLight(WARM, (dbg.winI ?? 8.0), 0, 0.95, 0.4, 2);
  spot.position.copy(lp); spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.camera.near = 0.2; spot.shadow.camera.far = 12; spot.shadow.bias = -0.0004; spot.shadow.normalBias = 0.02;
  const tgt = new THREE.Object3D(); tgt.position.set(A.halfW * 0.6, 0.6, A.winZ + 0.6); scene.add(tgt); spot.target = tgt; scene.add(spot);
  // Ô cửa là khẩu độ: phần vách quanh cửa (trong phòng) không có trong cảnh, nên chặn tia bằng một "tường phòng" vô hình chỉ đổ bóng.
  const room = new THREE.Group();
  const aperture = (w, h, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.03, h, w), new THREE.MeshBasicMaterial({ colorWrite: false })); m.position.set(-A.halfW - 0.02, y, z); m.castShadow = true; room.add(m); };
  aperture(4, 4, A.winY + A.winH / 2 + 2, A.winZ); aperture(4, 4, A.winY - A.winH / 2 - 2, A.winZ);
  aperture(2, A.winH, A.winY, A.winZ + A.winW / 2 + 1); aperture(2, A.winH, A.winY, A.winZ - A.winW / 2 - 1);
  scene.add(room);

  // Uniform shader chung (s5): tắt phần omni đèn lồng (tia chỉ qua ô cửa → SpotLight thật lo), bật ánh điện phẳng.
  U.uKeyOn.value = 0; U.uFillOn.value = 1; U.uSide.value.set(0, 0, 0); U.uBounce.value.set(0, 0, 0);
  U.uEo.value.set('#d4e2f4').multiplyScalar(dbg.eo ?? 4.2);
  if (which === 'alley') { U.uMouthZ.value = A.mouthZ; U.uSpillL.value = 0.9; U.uDeep.value = 0.004; }
  else { U.uMouthZ.value = A.mouthZ; U.uSpillL.value = 1.2; U.uDeep.value = 0.004; }
  // Dội ấm rất nhẹ từ khoảng nền được ô cửa rọi (điểm không bóng, sát nền dưới cửa) — nguồn là mảng nền sáng có thật trong hình.
  const bounce = new THREE.PointLight(WARM, dbg.bounce ?? 0.35, 0, 2); bounce.position.set(0.1, 0.15, A.winZ + 0.4); scene.add(bounce);

  const glow = glowSprite('#ffb060', 0.35, 1.6); glow.position.set(-A.halfW + 0.1, A.winY, A.winZ); scene.add(glow);

  const mk = (sheet, pose, pos, yaw) => {
    const ch = mkChar(sheet, { material: (role, color, part, extra) => charMat(role, color, extra), detail: which === 'alley' ? 28 : 16 });
    ch.setPose(pose); ch.root.position.set(...pos); ch.root.rotation.y = yaw; ch.root.updateMatrixWorld(true);
    ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); ch.root.userData.imp = 1; scene.add(ch.root);
    for (const k of Object.keys(ch.props || {})) { const p = ch.props[k]; if (p && p.parent && !p.visible) p.parent.remove(p); }
    return ch;
  };
  const ps = ida.poses.look_shadows;
  // cảnh 6: Ida đứng dưới cửa sổ, hơi lệch ra xa tường, ngửa nhìn lên ô cửa; tay đặt lên ngực
  const chIda = which === 'alley' ? mk(ida, ps, [0.45, 0, A.winZ + 1.0], dbg.yaw ?? Math.atan2(-1, -0.8))
    : mk(ida, ps, [0.0, 0, A.mouthZ - 0.6], Math.PI - 0.2);
  if (charUpdate) charUpdate(chIda, null);

  let cam;
  if (which === 'alley') {
    cam = new THREE.PerspectiveCamera(dbg.fov ?? 60, 16 / 9, 0.05, 400);
    cam.position.set(...(dbg.camPos || [0.25, 1.0, -3.4])); cam.lookAt(...(dbg.camLook || [-0.25, 2.3, 1.0]));
  } else {
    cam = new THREE.PerspectiveCamera(dbg.fov ?? 50, 16 / 9, 0.1, 600);
    cam.position.set(...(dbg.camPos || [4.5, 5.2, A.mouthZ + 13.2])); cam.lookAt(...(dbg.camLook || [-1.2, 3.4, A.mouthZ]));
  }
  const hal = (i, b) => { let f = 1, r = 0; while (i > 0) { f /= b; r += f * (i % b); i = Math.floor(i / b); } return r; };
  const onSample = (i, n) => {   // đèn lồng jitter trong khối kính ~10 cm → bóng mềm
    if (charUpdate) charUpdate(chIda, cam);
    if (n <= 1) { spot.position.copy(lp); return; }
    spot.position.set(lp.x + (hal(i + 1, 2) - 0.5) * 0.1, lp.y + (hal(i + 1, 3) - 0.5) * 0.1, lp.z + (hal(i + 1, 5) - 0.5) * 0.1);
  };
  return { scene, cam, onSample, chIda, chars: [chIda] };
}

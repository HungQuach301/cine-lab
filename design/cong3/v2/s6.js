// Cổng 3 v3 — khung phong cách cảnh 6 (hai khung, cùng một bộ phố):
//  d_s6_alley: Ida đứng trong CON NGÕ KHUẤT ĐÈN ĐIỆN dưới cửa sổ nhà Cas (luật thế giới 3.4, 3.5). Nguồn ấm duy nhất: đèn lồng trên bậu cửa sổ
//              (trong phòng Cas), tia chỉ lọt qua ô cửa → SpotLight có bóng, nón vừa khung cửa. Nguồn cao nên bóng Ida NGẮN, NHẠT, đổ xuống nền,
//              ngả ra xa tường. Ánh điện ngoài phố chỉ lọt vào miệng ngõ, giảm theo hàm mũ độ sâu (shader chung với s5, uMouthZ/uSpillL).
//  e_ending:   Toàn cảnh phố trắng dưới đèn điện (tràn phẳng, KHÔNG bóng, luật 2) và MỘT ô cửa vàng: cửa sổ nhà Cas. Ida nhỏ ở miệng ngõ.
// Không đèn giả: mọi ánh sáng có nguồn trong hình (cột đèn điện, ô cửa, bầu trời đêm).
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { limewashTex, flagTex, glowSprite, planarUV, rng } from '../dir-C/common.js';
import { U, patch } from './s5.js';
import { cobbleTex, groundPlane, facadeTex, wallUV, windowUnit, electricLamp, paintedSky } from './street.js';

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
// Đợt vá A2+ (V1, V2, V3): mặt tiền vữa/gạch vẽ tay có chất liệu, cửa sổ có khung–song–bậu–lanh tô, cửa gỗ có bậc, vỉa hè đá phiến + bó vỉa,
// lòng đường ĐÁ LÁT (luật thế giới), cột đèn điện thời kỳ thẳng, vách ngõ cao bằng mái (hết "mái lơ lửng"), trời vẽ.
function buildStreet(scene, R, which) {
  const A = ALLEY, WALL_H = 7.4;
  const FT = [0, 1, 2, 3].map((k) => lam({ color: '#ffffff', map: facadeTex(91 + k * 13, { metres: 6, base: ['#e7e2d6', '#e0dacd', '#e9e4da', '#dcd6ca'][k], courseAt: [3.2, 6.1] }) }));
  const alleyT = lam({ color: '#ffffff', map: facadeTex(71, { metres: 6, base: '#d6cfc2', courseAt: [] }) });
  const matC = (c) => lam({ color: c });
  const emit = (k) => (tex) => new THREE.MeshBasicMaterial({ map: tex, color: new THREE.Color('#ffffff').multiplyScalar(k), fog: true });
  // hai vách ngõ (mặt quay vào ngõ), cao bằng mái nhà hai bên; mép trên có gờ tối
  for (const sx of [-1, 1]) {
    const geo = wallUV(new THREE.PlaneGeometry(A.mouthZ - A.backZ, WALL_H), 6, sx * 2.3);
    const w = new THREE.Mesh(geo, alleyT); w.rotation.y = -sx * Math.PI / 2;
    w.position.set(sx * A.halfW, WALL_H / 2, (A.mouthZ + A.backZ) / 2); w.receiveShadow = true; w.castShadow = sx > 0; scene.add(w);   // vách trái có ô cửa: không đổ bóng (khẩu độ do tường phòng vô hình lo)
    scene.add(box(0.25, 0.18, A.mouthZ - A.backZ, matC('#3a3440'), sx * (A.halfW + 0.05), WALL_H + 0.09, (A.mouthZ + A.backZ) / 2));
  }
  // ống thoát nước trên vách phải, cửa sau cuối ngõ
  const pipe = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, WALL_H, 10), matC('#4a4a50')); pipe.position.set(A.halfW - 0.06, WALL_H / 2, -2.4); scene.add(pipe);
  const back = new THREE.Mesh(wallUV(new THREE.PlaneGeometry(A.halfW * 2, WALL_H), 6), alleyT); back.position.set(0, WALL_H / 2, A.backZ); back.receiveShadow = true; scene.add(back);
  scene.add(box(0.9, 2.0, 0.08, matC('#3e2e24'), 0, 1.0, A.backZ + 0.04));
  // đá lát (ngõ + lòng phố) và vỉa hè đá phiến có bó vỉa trước mặt tiền
  const cob = lam({ color: '#ffffff', map: cobbleTex(9) });
  scene.add(groundPlane(A.halfW * 2, A.mouthZ - A.backZ, cob, 3, { cz: (A.mouthZ + A.backZ) / 2 }));
  scene.add(groundPlane(160, 18, cob, 3, { cz: A.mouthZ + 1.6 + 9, y: -0.14 }));
  const flag = lam({ color: '#ffffff', map: flagTex(9, { metres: 4 }) });
  for (const [x0, x1] of [[-80, -A.halfW], [A.halfW, 80]]) scene.add(groundPlane(x1 - x0, 1.6, flag, 4, { cx: (x0 + x1) / 2, cz: A.mouthZ + 0.8 }));
  scene.add(groundPlane(A.halfW * 2, 1.6, cob, 3, { cz: A.mouthZ + 0.8 }));
  scene.add(box(160, 0.15, 0.2, matC('#9d968c'), 0, -0.07, A.mouthZ + 1.6));                                   // bó vỉa
  // Dãy nhà: từng nếp nhà (rộng 4–7 m), mặt tiền vữa/gạch, cửa sổ có khung; mái dốc, ống khói. Ô vàng = phòng góc nhà Cas.
  const roofM = matC('#2c2834'), doorM = matC('#4a3226'), stepM = matC('#a39b8f');
  const houses = (x0, x1, z, face, seed, gold, minHNear) => {
    const Rh = rng(seed); let x = x0; const ry = face < 0 ? Math.PI : 0;
    while (x < x1 - 0.5) {
      const w = Math.min(x1 - x, 4 + Rh() * 3), near = minHNear && Math.abs(x + w / 2 - minHNear[0]) < 4;
      const h = near ? minHNear[1] : 6 + Rh() * 2.5, d = 7, cx = x + w / 2;
      const m = new THREE.Mesh(wallUV(new THREE.PlaneGeometry(w, h), 6, x), FT[Math.floor(Rh() * 4)]);
      m.position.set(cx, h / 2, z); m.rotation.y = ry; m.receiveShadow = true; scene.add(m);
      scene.add(box(w + 0.02, 0.22, 0.35, matC('#d8d2c6'), cx, h - 0.11, z + face * 0.17));                    // phào mái
      const r = new THREE.Mesh(new THREE.CylinderGeometry(0.01, d * 0.72, 2.4 + Rh() * 1.2, 4, 1), roofM); r.rotation.y = Math.PI / 4; r.scale.set(w / d, 1, 1);
      r.position.set(cx, h + 1.2, z - face * d / 2); scene.add(r);
      if (Rh() < 0.8) { const chx = x + w * (0.2 + 0.6 * Rh()); scene.add(box(0.5, 1.5, 0.5, matC('#6a5a52'), chx, h + 1.6, z - face * d * 0.35));
        for (const o of [-0.12, 0.12]) { const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.09, 0.3, 10), matC('#8a5a44')); pot.position.set(chx + o, h + 2.5, z - face * d * 0.35); scene.add(pot); } }
      for (let wx = x + 1.0; wx < x + w - 0.6; wx += 1.9) for (const wy of [2.1, 4.3, 6.4]) {
        if (wy > h - 1.0) continue;
        if (gold && Math.abs(wx - gold[0]) < 1.0 && Math.abs(wy - gold[1]) < 1.2) continue;   // chỗ của ô vàng
        const kind = which === 'ending' ? (Rh() < 0.75 ? 'cold' : 'dark') : (Rh() < 0.5 ? 'cold' : 'dark');
        const u = windowUnit(0.82, 1.25, kind, matC, emit(kind === 'cold' ? 1.25 : 1.0), Math.floor(Rh() * 1e6)); u.position.set(wx, wy, z); u.rotation.y = ry; scene.add(u);
      }
      if (Rh() < 0.6) { const dx = x + w * 0.5; scene.add(box(1.0, 2.2, 0.1, doorM, dx, 1.1, z + face * 0.05)); scene.add(box(1.3, 0.15, 0.4, stepM, dx, 0.075, z + face * 0.2));
        scene.add(box(1.2, 0.12, 0.08, matC('#cfc8bb'), dx, 2.3, z + face * 0.04)); }
      x += w;
    }
    if (gold) { const u = windowUnit(0.82, 1.25, 'gold', matC, emit(1.9), 3); u.position.set(gold[0], gold[1], z); u.rotation.y = ry; scene.add(u);
      const gl = glowSprite('#ffae5c', 0.35, 2.2); gl.position.set(gold[0], gold[1], z + face * 0.4); scene.add(gl); }
  };
  houses(-60, -A.halfW, A.mouthZ, 1, 81, [-2.0, 4.3], [-3.0, WALL_H]);   // ô vàng: phòng góc nhà Cas (cùng phòng với cửa sổ trên ngõ)
  houses(A.halfW, 60, A.mouthZ, 1, 83, null, [3.0, WALL_H]);
  houses(-60, 60, A.mouthZ + 16, -1, 85, null, null);
  // cột đèn điện thời kỳ ở mép bó vỉa, tay treo vươn ra lòng phố; ánh tràn phẳng do shader (uEo) — không bóng
  const posts = [];
  const bulbM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#eef3ff').multiplyScalar(9) });
  for (const x of [-22, -9.5, 5.8, 18, 30]) {
    const L = electricLamp(6.2, matC, bulbM); L.group.position.set(x, 0, A.mouthZ + 1.75); L.group.rotation.y = -Math.PI / 2; scene.add(L.group);
    L.group.updateMatrixWorld(true); const hp = L.head.clone().applyMatrix4(L.group.matrixWorld);
    const gl = glowSprite('#dfe8ff', 0.55, 2.6); gl.position.copy(hp); scene.add(gl); posts.push(hp);
  }
  // CỬA SỔ NHÀ CAS trên vách trái của ngõ: khung, song, bậu (thấy từ ngõ); lòng kính ấm
  const cw = windowUnit(A.winW, A.winH, 'gold', matC, emit(2.4), 5); cw.position.set(-A.halfW + 0.002, A.winY, A.winZ); cw.rotation.y = Math.PI / 2; scene.add(cw);
  return { posts };
}

export async function buildS6(ida, cas, dbg = {}, mkChar, charUpdate, which = 'alley') {
  const A = ALLEY, R = rng(66);
  const scene = new THREE.Scene();
  // Trời vẽ theo color script (cảnh 6: phố trắng dưới đèn điện; trời đêm tím–xanh, chân trời hửng ánh phố); sương lạnh = phối cảnh không khí.
  const skyM = paintedSky([[0, '#121831'], [0.5, '#262e4d'], [0.8, '#4a5373'], [1, '#7d8aa6']], { seed: 61, haze: '#aeb9cc', hazeA: which === 'ending' ? 0.45 : 0.25 });
  if (which === 'alley') skyM.material.color.setScalar(0.08);   // phơi sáng ngõ ×4 cho ánh cửa sổ: trời giữ đúng độ sáng tương đối (không cháy thành mảng xanh)
  scene.add(skyM);
  if (which === 'alley') scene.add(new THREE.HemisphereLight('#3c4666', '#1a1620', 0.12));   // ánh trời đêm rất yếu: tường ngõ hiện chất liệu
  scene.fog = which === 'ending' ? new THREE.Fog('#a3aec2', 10, 95) : new THREE.Fog('#10131f', 9, 55);
  buildStreet(scene, R, which);

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
  if (which === 'alley') { U.uMouthZ.value = A.mouthZ; U.uSpillL.value = 1.5; U.uDeep.value = 0.004; }
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
    : mk(ida, ps, [0.3, 0, A.mouthZ + 0.5], dbg.yaw ?? Math.atan2(-2.3, -0.5));   // A2+: đứng ngay miệng ngõ trên vỉa hè (dưới ánh điện), ngửa nhìn ô vàng
  if (charUpdate) charUpdate(chIda, null);

  let cam;
  if (which === 'alley') {
    cam = new THREE.PerspectiveCamera(dbg.fov ?? 60, 16 / 9, 0.05, 400);
    cam.position.set(...(dbg.camPos || [0.25, 1.0, -3.4])); cam.lookAt(...(dbg.camLook || [-0.25, 2.3, 1.0]));
  } else {
    cam = new THREE.PerspectiveCamera(dbg.fov ?? 48, 16 / 9, 0.1, 600);
    cam.position.set(...(dbg.camPos || [3.4, 2.1, A.mouthZ + 8.5])); cam.lookAt(...(dbg.camLook || [-0.9, 3.4, A.mouthZ]));
  }
  const hal = (i, b) => { let f = 1, r = 0; while (i > 0) { f /= b; r += f * (i % b); i = Math.floor(i / b); } return r; };
  const onSample = (i, n) => {   // đèn lồng jitter trong khối kính ~10 cm → bóng mềm
    if (charUpdate) charUpdate(chIda, cam);
    if (n <= 1) { spot.position.copy(lp); return; }
    spot.position.set(lp.x + (hal(i + 1, 2) - 0.5) * 0.1, lp.y + (hal(i + 1, 3) - 0.5) * 0.1, lp.z + (hal(i + 1, 5) - 0.5) * 0.1);
  };
  return { scene, cam, onSample, chIda, chars: [chIda] };
}

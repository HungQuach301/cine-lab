// Cổng 3 v2 — cảnh 5 khung rộng (quyết định 2A), dựa trên dir-C/s5.js. Thêm: (1) hàm dựng nhân vật tiêm từ ngoài (so 2 cách làm nhân vật
// trong cùng một cảnh, cùng ánh sáng); (2) ÁNH DỘI ẤM TỪ HAI VÁCH BÊN của hốc (vách vôi được đèn lồng rọi, hắt sáng lên sườn người) → viền sáng tách
// người khỏi bóng (đánh giá độc lập: người quá tối, hoà vào bóng). Đúng luật thế giới: nguồn là vách bên có thật trong hình.
// Ánh sáng "vẽ" nhưng đúng quang học (luật thế giới 2–3):
//  • Đèn lồng = SpotLight có bóng (trong nón hướng vào vách) + phần bù omni KHÔNG bóng ngoài nón (tiêm vào shader),
//    tổng lại là một nguồn điểm; vị trí jitter trong khối kính ~12 cm theo từng mẫu → bóng mềm thật.
//  • Ánh điện ngoài phố = ánh tràn phẳng, không bóng đổ; lọt vào hốc giảm theo hàm mũ độ sâu (vùng khuất đèn điện).
//  • Dội ấm rất nhẹ (vách vôi phản xạ) làm bóng không đen tuyệt đối.
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { limewashTex, flagTex, glowSprite, planarUV, rng, ShiftCam, canvasTex, blotches } from '../dir-C/common.js';

const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
export const BAY = { halfW: 1.6, spring: 2.4, depth: 4.0 }; // rộng 3,2 m, cao 4,0 m, sâu 4,0 m
export const LANTERN_Z = 3.0;       // cách vách trong 3,0 m
export const PEOPLE_Z = 1.0;        // cách vách 1,0 m

export const U = {
  uLP: { value: new THREE.Vector3() }, uLC: { value: new THREE.Color() }, uLDir: { value: new THREE.Vector3(0, 0, -1) },
  uCone: { value: 0 }, uPen: { value: 0 },
  uEo: { value: new THREE.Color() }, uMouthZ: { value: BAY.depth }, uSpillL: { value: 0.32 },
  uBounce: { value: new THREE.Color() }, uDeep: { value: 0.0035 }, uKeyOn: { value: 1 }, uFillOn: { value: 1 },
  uSide: { value: new THREE.Color() }, uHalfW: { value: 1.6 },
};

const DECL = `varying vec3 vW;
uniform vec3 uLP, uLC, uLDir, uEo, uBounce, uSide; uniform float uCone, uPen, uMouthZ, uSpillL, uKeyOn, uFillOn, uDeep, uHalfW;`;
const BODY = `{
  vec3 nW = normalize((vec4(normal, 0.0) * viewMatrix).xyz);
  vec3 dL = uLP - vW; float d2 = max(dot(dL, dL), 1e-4); vec3 l = dL * inversesqrt(d2);
  float ndl = max(dot(nW, l), 0.0);
  float comp = 1.0 - smoothstep(uCone, uPen, dot(-l, uLDir));
  float lid = 1.0 - smoothstep(0.707, 0.799, -l.y);                        // 5A: nắp đèn lồng chắn tia lên trên ~45–53° (sin) so với phương ngang
  vec3 E = uKeyOn * uLC * ndl / max(d2, 0.01) * comp * lid;               // phần omni ngoài nón (không bóng)
  float depthIn = max(0.0, uMouthZ - vW.z);
  float vis = exp(-depthIn / uSpillL);
  float ao = 1.0 - 0.22 * exp(-max(vW.y, 0.0) / 0.10) * (1.0 - abs(nW.y));   // bóng tiếp xúc rất nhẹ chân tường/chân vật
  vis = max(vis, uDeep * (0.6 + 0.4 * smoothstep(0.0, uMouthZ, vW.z)));    // tràn lạnh rất yếu dội từ phố vào sâu trong hốc
  vec3 eo = uEo * mix(vec3(1.0), vec3(0.93, 0.96, 1.04), smoothstep(0.5, 5.0, vW.y));   // phẳng; lên cao hơi lạnh hơn một chút (vẽ không khí)
  E += uFillOn * eo * vis * (0.78 + 0.22 * nW.y) * ao;                     // ánh điện phẳng
  float inB = 1.0 - smoothstep(uMouthZ - 0.6, uMouthZ + 0.2, vW.z);
  E += uFillOn * uKeyOn * uBounce * inB * (0.7 + 0.3 * max(nW.z, 0.0)) / (1.0 + 0.12 * d2);  // dội ấm từ vách/nền
  E += uFillOn * uKeyOn * uBounce * 2.2 * inB * max(0.0, -nW.y);   // 5A: vòm trần không nhận tia trực tiếp, chỉ dội ấm từ nền đá và vách được rọi
  // Dội ấm từ hai vách bên (x = ±uHalfW): mặt quay về vách nào nhận sáng tỉ lệ độ rọi của vách đó (đèn lồng → vách: 1/d²), giảm theo khoảng cách tới vách.
  // Chỉ bề mặt quay ra hai bên (|n.x| lớn — viền người) nhận nhiều → viền ấm; mặt tường bên tự nhận rất ít (n.x hướng vào trong).
  for (int k = 0; k < 2; k++) {
    float sx = k == 0 ? -1.0 : 1.0;
    vec3 wp = vec3(sx * uHalfW, clamp(vW.y, 0.3, 2.2), clamp(vW.z, 0.2, uMouthZ));
    vec3 dw = wp - uLP; float ew = uKeyOn / max(dot(dw, dw), 0.3);                       // độ rọi đèn lồng trên vách bên
    float face = max(0.0, sx * nW.x);                                                     // mặt quay về phía vách
    float dist = abs(wp.x - vW.x);
    E += uFillOn * uSide * ew * face / (1.0 + 2.5 * dist * dist) * inB;
  }
  reflectedLight.directDiffuse += E * BRDF_Lambert(material.diffuseColor);
}`;
export function patch(mat) {
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, U);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vW;')
      .replace('#include <fog_vertex>', '#include <fog_vertex>\n  vW = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + DECL)
      .replace('#include <lights_fragment_end>', '#include <lights_fragment_end>\n' + BODY);
  };
  mat.customProgramCacheKey = () => 'dirC-s5';
  return mat;
}
const lam = (o) => patch(new THREE.MeshLambertMaterial(o));

// Vật liệu nhân vật: giữ màu model sheet (quan hệ sáng–tối), lửa/kính phát sáng HDR.
function charMat(role, color, extra = {}) {
  if (role === 'flame') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(40) });
  if (role === 'glass') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb85a').multiplyScalar(5.0), transparent: true, opacity: 0.75, depthWrite: false });
  const c = new THREE.Color(color);
  if (role === 'hair') c.multiplyScalar(0.45);   // tóc xám trung tính (giá trị trung bình): gáy không đọc nhầm thành mặt dưới ánh ấm
  return lam({ color: c, side: THREE.DoubleSide, ...extra });
}

// Tóc phủ gáy (chi tiết trang trí gắn khớp đầu, vỏ 1,02× sọ — không đổi đường bao): khi quay lưng, gáy đọc là tóc, không đọc nhầm thành mặt.
export function addHair(ch, sheet) {
  const H = sheet.H_m, hd = sheet.parts.head, isIda = sheet.id.startsWith('CHR-ida');
  const col = new THREE.Color(isIda ? sheet.local_colors.hair : '#5a4034').multiplyScalar(isIda ? 0.45 : 1);
  const g = new THREE.SphereGeometry(0.5, 40, 24, Math.PI - 0.35, Math.PI + 0.7, 0.05, Math.PI * (isIda ? 0.84 : 0.72));
  const m = new THREE.Mesh(g, lam({ color: col, side: THREE.DoubleSide }));
  m.scale.set(hd.width_front * 1.02 * H, hd.length * 1.02 * H, hd.width_side * 1.02 * H); m.position.y = hd.length * H / 2;
  m.castShadow = true; m.receiveShadow = true; ch.joints.head.add(m);
}

// Đá cuội ngoài phố: viên tròn dẹt, mạch tối mềm.
function cobbleTex(seed) {
  const R = rng(seed);
  return canvasTex(1024, 1024, (g, w, h) => {
    g.fillStyle = 'rgb(118,115,111)'; g.fillRect(0, 0, w, h);
    const ppm = w / 3, cs = 0.12 * ppm;
    for (let y = 0, r = 0; y < h + cs; y += cs * 0.9, r++) for (let x = (r % 2) * cs / 2; x < w + cs; x += cs) {
      const k = 0.94 + R() * 0.1, c = [140 * k, 138 * k, 134 * k].map((v) => v | 0);
      const gr = g.createRadialGradient(x - cs * 0.1, y - cs * 0.12, 0, x, y, cs * 0.55);
      gr.addColorStop(0, `rgb(${c.map((v) => Math.min(255, v * 1.07) | 0)})`); gr.addColorStop(1, `rgb(${c.map((v) => v * 0.9 | 0)})`);
      g.fillStyle = gr; g.beginPath(); g.ellipse(x + (R() - 0.5) * cs * 0.1, y, cs * 0.46, cs * 0.40, R(), 0, Math.PI * 2); g.fill();
    }
    blotches(g, w, h, R, 40, [[70, 66, 62], [170, 166, 160]], 0.2 * ppm, 0.7 * ppm, 0.04, 0.1);
  });
}

export async function buildS5(ida, cas, dbg = {}, mkChar, charUpdate) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#0b0a0c');
  const { halfW, spring, depth } = BAY; const rA = halfW;

  const wallTex = limewashTex(11, { metres: 4, grime: true, brick: 0.045 });
  const facTex = limewashTex(23, { metres: 6, grime: true, brick: 0.11, base: '#e6e1d8' });
  const floorTex = flagTex(5, { metres: 4 });
  const wallMat = lam({ color: '#ffffff', map: wallTex });
  const vaultMat = lam({ color: '#f4efe6', map: limewashTex(12, { metres: 4, grime: false, brick: 0.035 }) });
  const facMat = lam({ color: '#f2f1ee', map: facTex });
  const floorMat = lam({ color: '#ffffff', map: floorTex });
  const stoneMat = lam({ color: '#b9b2a8' });
  const ironMat = lam({ color: '#4a4e57' });

  const archShape = (hw, sp, withHole) => {
    const s = new THREE.Shape(); s.moveTo(-hw, 0); s.lineTo(-hw, sp); s.absarc(0, sp, hw, Math.PI, 0, true); s.lineTo(hw, 0); s.lineTo(-hw, 0); return s;
  };
  // Vách trong (z = 0)
  { const g = new THREE.ShapeGeometry(archShape(halfW, spring), 48); planarUV(g, X, Y, 4, [2, 0]);
    const m = new THREE.Mesh(g, wallMat); m.receiveShadow = true; scene.add(m); }
  // Hai vách bên (x = ±1,6), mặt quay vào trong
  for (const sx of [-1, 1]) {
    const g = new THREE.PlaneGeometry(depth, spring, 8, 6); g.rotateY(-sx * Math.PI / 2); g.translate(sx * halfW, spring / 2, depth / 2);
    planarUV(g, Z, Y, 4, [sx * 1.3, 0]);
    const m = new THREE.Mesh(g, wallMat); m.receiveShadow = true; scene.add(m);
  }
  // Vòm cuốn (nửa trụ), mặt trong
  { const g = new THREE.CylinderGeometry(rA, rA, depth, 64, 6, true, -Math.PI / 2, Math.PI); g.rotateX(-Math.PI / 2); g.translate(0, spring, depth / 2);
    planarUV(g, Z, X, 4, [0, 2.5]);
    const m = new THREE.Mesh(g, new THREE.MeshLambertMaterial()); m.material = vaultMat; vaultMat.side = THREE.BackSide; m.receiveShadow = true; scene.add(m); }
  // Mặt tiền nhà kho (z = 4) có lỗ vòm; gờ đá quanh vòm; nền đá trong + ngoài
  { const s = new THREE.Shape(); s.moveTo(-14, 0); s.lineTo(14, 0); s.lineTo(14, 12); s.lineTo(-14, 12); s.lineTo(-14, 0);
    s.holes.push(archShape(halfW, spring)); const g = new THREE.ShapeGeometry(s, 48); g.translate(0, 0, depth); planarUV(g, X, Y, 6, [0.4, 0]);
    scene.add(new THREE.Mesh(g, facMat)); }
  { // vòm đá cuốn: 15 viên nêm (có viên khoá), chân vòm đá góc so le; hơi xám ấm hơn vôi
    const R = rng(77); const n = 15, r0 = halfW, r1 = halfW + 0.30;
    for (let i = 0; i < n; i++) {
      const a0 = Math.PI * i / n + 0.006, a1 = Math.PI * (i + 1) / n - 0.006, key = i === (n - 1) / 2;
      const rr = r1 + (key ? 0.08 : 0) + (i % 2) * 0.03;
      const s = new THREE.Shape(); s.moveTo(Math.cos(a0) * r0, Math.sin(a0) * r0); s.lineTo(Math.cos(a0) * rr, Math.sin(a0) * rr);
      s.lineTo(Math.cos(a1) * rr, Math.sin(a1) * rr); s.lineTo(Math.cos(a1) * r0, Math.sin(a1) * r0);
      const g = new THREE.ExtrudeGeometry(s, { depth: 0.05, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.012, bevelSegments: 1 }); g.translate(0, spring, depth - 0.02);
      const k = 0.92 + R() * 0.12; scene.add(new THREE.Mesh(g, lam({ color: new THREE.Color('#c9c1b4').multiplyScalar(k) })));
    }
    for (const sx of [-1, 1]) for (let j = 0, y = 0.42; j < 5; j++) {
      const h = 0.36 + (j % 2) * 0.04, w = j % 2 ? 0.34 : 0.48;
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, h - 0.02, 0.06), lam({ color: new THREE.Color('#c4bcb0').multiplyScalar(0.93 + R() * 0.1) }));
      b.position.set(sx * (halfW + w / 2), y + h / 2, depth + 0.01); scene.add(b); y += h; if (y > spring - 0.1) break;
    }
    // má cửa (lòng miệng vòm) 0,3 m đá
    for (const sx of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.02, spring, 0.30), stoneMat); b.position.set(sx * (halfW - 0.01), spring / 2, depth - 0.15); scene.add(b); }
    // chân tường: gờ đá sẫm 0,42 m chạy dọc mặt tiền (neo khối nhà xuống đất)
    for (const sx of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(12, 0.42, 0.08), lam({ color: '#8d877f' })); b.position.set(sx * (halfW + 6), 0.21, depth + 0.02); scene.add(b); }
  }
  { // nền: đá lát trong hốc; đá cuội ngoài phố (đường phân chia ở ngưỡng)
    const g = new THREE.PlaneGeometry(3.2, 4.0); g.rotateX(-Math.PI / 2); g.translate(0, 0, 2.0); planarUV(g, X, Z, 4, [2, 0]);
    const m = new THREE.Mesh(g, floorMat); m.receiveShadow = true; scene.add(m);
    const cob = cobbleTex(9);
    const g2 = new THREE.PlaneGeometry(30, 14); g2.rotateX(-Math.PI / 2); g2.translate(0, 0, 4 + 7); planarUV(g2, X, Z, 3, [0, 0]);
    scene.add(new THREE.Mesh(g2, lam({ color: '#ffffff', map: cob })));
  }
  { // ngưỡng đá ở miệng vòm
    const b = new THREE.Mesh(new THREE.BoxGeometry(halfW * 2 + 0.1, 0.05, 0.32), stoneMat); b.position.set(0, 0.025, depth + 0.06); b.receiveShadow = true; scene.add(b); }
  { // ống thoát nước gang bên trái mặt tiền (ngoài vòm, ánh điện phẳng, không bóng đổ)
    const px = -3.3;
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 12, 16), ironMat); p.position.set(px, 6, depth + 0.09); scene.add(p);
    for (let y = 1.1; y < 10; y += 1.8) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.065, 0.065, 0.06, 16), ironMat); c.position.set(px, y, depth + 0.09); scene.add(c); }
    const shoe = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 0.25, 16), ironMat); shoe.position.set(px, 0.12, depth + 0.14); shoe.rotation.x = 0.5; scene.add(shoe);
  }
  { // cột điện kiểu mới (đã bật, tấm kính ở trên khung hình): thân gang thon đứng trước mặt tiền, bên phải
    const postMat = lam({ color: '#565b66' });
    const g = new THREE.CylinderGeometry(0.06, 0.09, 7, 20); const m = new THREE.Mesh(g, postMat); m.position.set(3.45, 3.5, 4.9); scene.add(m);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.19, 0.9, 20), postMat); base.position.set(3.45, 0.45, 4.9); scene.add(base);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.03, 8, 20), postMat); ring.rotation.x = Math.PI / 2; ring.position.set(3.45, 0.92, 4.9); scene.add(ring);
  }
  { // vòng sắt buộc hàng (ngoài vòm)
    const r = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.012, 8, 20), ironMat); r.position.set(2.45, 1.05, depth + 0.03); scene.add(r);
  }

  // Nhân vật: quay lưng về máy (nhìn −z), Ida trái (−x), Cas phải (+x), cách vách ~1 m.
  const mk = (sheet, pose, x, yaw) => {
    const ch = mkChar(sheet, { material: (role, color, part, extra) => charMat(role, color, extra), patch, detail: 20 });
    ch.setPose(sheet.poses[pose]); ch.root.position.set(x, 0, PEOPLE_Z); ch.root.rotation.y = Math.PI + yaw; ch.root.updateMatrixWorld(true);
    ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
    ch.root.userData.imp = 1; scene.add(ch.root); return ch;
  };
  const chIda = mk(ida, 'look_shadows', -0.42, 0.30);
  const chCas = mk(cas, 'half_raised', 0.40, -0.25);
  if (charUpdate) { charUpdate(chIda, null); charUpdate(chCas, null); }
  // đèn lồng trên nền đá
  const lanternH = ida.props.lantern.height_H * ida.H_m;
  const lan = chIda.props.lantern; if (lan.parent) lan.parent.remove(lan);
  lan.position.set(0.05, 0, LANTERN_Z); lan.rotation.y = 0.5; scene.add(lan); lan.userData.imp = 1;
  lan.traverse((o) => { if (o.isMesh) { o.castShadow = false; o.receiveShadow = false; } });
  lan.updateMatrixWorld(true);
  const flameP = new THREE.Vector3(); lan.userData.lightAnchor.getWorldPosition(flameP);

  // Đèn: SpotLight có bóng hướng vào vách
  const I0 = 5.2; // cd
  // Lửa thở ±4 %, chu kỳ chậm (luật 2): hệ số theo số khung phim; khung tĩnh = khung 0 → 1,0.
  const flickAt = (f) => 1 + 0.04 * (0.6 * Math.sin(f * 0.21) + 0.4 * Math.sin(f * 0.083 + 1.3));
  const flick = flickAt(0);
  const warm = new THREE.Color('#ffae5c');
  // 5A: nón đèn từ −10° tới +49° so với phương ngang (trục ngẩng 19,5°, nửa góc 29,5°) — nắp chắn tia lên cao; vòm và đỉnh vách chỉ nhận dội ấm.
  const spot = new THREE.SpotLight(warm, I0 * flick, 0, 0.515, 0.15, 2);
  spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.camera.near = 0.05; spot.shadow.camera.far = 9;
  spot.shadow.bias = -0.0004; spot.shadow.normalBias = 0.015; spot.shadow.radius = 2;
  const target = new THREE.Object3D(); target.position.set(0, flameP.y + LANTERN_Z * Math.tan(19.5 * Math.PI / 180), 0); scene.add(target); spot.target = target;
  spot.position.copy(flameP); scene.add(spot);
  if (dbg.noshadow) spot.castShadow = false;
  if (dbg.nospot) spot.intensity = 0;
  const cone = Math.cos(spot.angle), pen = Math.cos(spot.angle * (1 - spot.penumbra));
  U.uCone.value = cone; U.uPen.value = pen;
  U.uLC.value.copy(warm).multiplyScalar(I0 * flick);
  U.uEo.value.set('#d4e2f4').multiplyScalar(5.0);   // ánh điện ngoài phố (trắng lạnh hơi xanh), irradiance
  U.uBounce.value.set('#ff9a52').multiplyScalar(0.065);
  U.uSide.value.set('#ffb070').multiplyScalar(dbg.side ?? 0.55);   // hệ số hắt của vách vôi (albedo ~0,8 × hình học), hiệu chỉnh bằng mắt + số đo tách người/bóng
  U.uHalfW.value = halfW;
  const setLamp = (p) => { spot.position.copy(p); U.uLP.value.copy(p); U.uLDir.value.copy(target.position).sub(p).normalize(); spot.updateMatrixWorld(); };
  setLamp(flameP);

  // Quầng sáng trong không khí quanh đèn (khuếch tán, không phải bóng)
  const glowCore = glowSprite('#ffc57a', 2.4, 0.55); glowCore.position.copy(flameP); scene.add(glowCore);
  const glowWide = glowSprite('#ff9a4a', 0.34, 3.4); glowWide.position.copy(flameP).add(new THREE.Vector3(0, 0.25, 0)); scene.add(glowWide);
  const glowAir = glowSprite('#ff8a40', 0.10, 5.5); glowAir.position.set(0, 1.1, 2.2); scene.add(glowAir);   // không khí ấm trong hốc

  // Máy quay: ngang tầm 1,3 m, lùi ra ngoài vòm để mép khung thấy mặt tiền trắng (xem README: lý do lệch brief).
  // Khung "tranh trong tranh": máy ngang, dịch ống kính lên (đường đứng thẳng), thấy trọn vòm trong mặt tường trắng.
  const cam = new ShiftCam(42, 16 / 9, 0.1, 80, 0.25);
  cam.position.set(0.25, 1.35, 10.5); cam.lookAt(0.25, 1.35, 0);
  if (dbg.briefcam) { // biến thể đúng chữ brief: 1,5 m sau đèn, ngang 1,3 m, FOV 40° (khung nằm trọn trong vòm — để P so sánh)
    cam.fov = 40; cam.shiftY = 0.12; cam.position.set(0.1, 1.3, LANTERN_Z + 1.5); cam.lookAt(0.1, 1.3, 0); cam.updateProjectionMatrix(); }

  // v3 (6B): TRUNG CẢNH — máy qua vai 3/4 sau-phải, cạnh đèn lồng (không chắn tia), nhìn hai người và bóng của họ trên vách.
  // Đầu/má tách khỏi bóng nền nhờ (1) đèn lồng dưới đất sau lưng hai người chiếu viền lên má, gáy, mép mũ (nguồn có trong truyện),
  // (2) dội ấm từ vách bên (uSide). Không thêm đèn giả.
  if (dbg.medium) {
    const m = dbg.medium === true || dbg.medium === 1 ? {} : dbg.medium;
    cam.fov = m.fov ?? 38; cam.shiftY = 0; cam.position.set(...(m.pos || [1.35, 1.0, 2.7])); cam.lookAt(...(m.look || [-0.1, 1.0, 0.8])); cam.updateProjectionMatrix();
  }

  // Jitter nguồn trong khối kính (~12 cm) theo mẫu: dãy Halton(2,3) riêng, tâm tại ngọn lửa
  const hal = (i, b) => { let f = 1, r = 0; while (i > 0) { f /= b; r += f * (i % b); i = Math.floor(i / b); } return r; };
  const onSample = (i, n) => {
    if (charUpdate) { charUpdate(chIda, cam); charUpdate(chCas, cam); }
    if (n <= 1) { setLamp(flameP); return; }
    const u = hal(i + 1, 2) - 0.5, v = hal(i + 1, 3) - 0.5, w = hal(i + 1, 5) - 0.5;
    setLamp(flameP.clone().add(new THREE.Vector3(u * 0.12, v * 0.12, w * 0.12)));
  };
  return { scene, cam, onSample, spot, lan, chIda, chCas, flameP, lanternH };
}

// Cine Lab · Cổng 4 — ANIMATIC: bộ cảnh bọc quanh cảnh đã khoá ở Cổng 3 (s1, s5, s6) + tường chim bóng (chép b_cas_bird) + phòng Cas (previs mới).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { buildS1 } from '/cong3/v2/s1.js';
import { buildS5, LANTERN_Z, PEOPLE_Z } from '/cong3/v2/s5.js';
import { buildS6, ALLEY } from '/cong3/v2/s6.js';
import { buildGasLamp } from '/cong3/shared/props.js';
import { buildLantern } from '/cong3/shared/cast.js';
import { cobbleTex, groundPlane, electricLamp, paintedSky, windowUnit } from '/cong3/v2/street.js';
import { limewashTex, glowSprite, planarUV, rng } from '/cong3/dir-C/common.js';
import { GAS, ELEC, lamMat, flickAt, contactBlob } from './sets.js';
import { rng as rngU } from '/cong3/dir-C/common.js';

// ================= THÀNH PHỐ (s1) =================
// mode: 'dusk' (0:00 — các chấm hổ phách hiện dần), 'wave' (0:30 — sóng trắng lan từ quảng trường xuống dốc), 'night' (2:10 — cả thành phố trắng, một ô vàng).
export async function buildCitySet(ctx, mode) {
  const r = await buildS1(ctx.sheets.ida, ctx.H, {}, ctx.mkChar);
  const { scene, cam } = r;
  const sprites = []; scene.traverse((o) => { if (o.isSprite) sprites.push(o); });
  // chấm hổ phách ở các phố khác (cặp lõi 1,5 m + quầng 10 m)
  const others = sprites.filter((s) => Math.abs(s.scale.x - 1.5) < 0.01 || Math.abs(s.scale.x - 10) < 0.01);
  const pairs = []; for (const s of others) { let p = pairs.find((q) => Math.abs(q.x - s.position.x) < 0.01 && Math.abs(q.z - s.position.z) < 0.01); if (!p) { p = { x: s.position.x, z: s.position.z, list: [] }; pairs.push(p); } p.list.push(s); }
  const R = rngU(77); pairs.forEach((p) => { p.k = R(); });
  // tấm kính cột điện trên Ostler (BoxGeometry 0,9 × 0,12 × 0,55) và mặt đồng hồ
  const panels = [], faces = [];
  scene.traverse((o) => { if (!o.isMesh) return; const pa = o.geometry.parameters || {};
    if (o.geometry.type === 'BoxGeometry' && Math.abs(pa.width - 0.9) < 1e-3 && Math.abs(pa.height - 0.12) < 1e-3) panels.push(o);
    if (o.geometry.type === 'CircleGeometry' && Math.abs(pa.radius - 0.6) < 1e-3) faces.push(o); });
  // BoxGeometry của tấm kính đã dịch trong hình học (translate) → lấy tâm hình học thế giới
  const panelPos = panels.map((m) => { m.geometry.computeBoundingBox(); const c = m.geometry.boundingBox.getCenter(new THREE.Vector3()); m.updateMatrixWorld(true); return c.applyMatrix4(m.matrixWorld); });
  const sq = new THREE.Vector3(0, 0, 4); const order = panelPos.map((p, i) => [p.distanceTo(sq), i]).sort((a, b) => a[0] - b[0]).map((x) => x[1]);
  const whites = panelPos.map((p) => { const L = new THREE.PointLight('#e3eaff', 0, 60, 1.0); L.position.copy(p).add(new THREE.Vector3(0, -0.3, 0)); scene.add(L);
    const s1 = glowSprite('#e8eeff', 0, 5.0), s2 = glowSprite('#dfe6ff', 0, 16); s1.position.copy(p); s2.position.copy(p); scene.add(s1, s2); return { L, s1, s2 }; });
  const setWhite = (w, e) => { w.L.intensity = 260 * e * Math.min(1, Math.max(0.12, w.L.position.distanceTo(cam.position) / 90)); w.s1.material.color.set('#e8eeff').multiplyScalar(3.0 * e); w.s2.material.color.set('#dfe6ff').multiplyScalar(0.28 * e); };
  // quảng trường: 4 tấm kính quanh quảng trường (bật cùng lúc, trước Ostler)
  const sqW = [[-12, 6.5, -4], [12, 6.5, -2], [-12, 6.5, 14], [12, 6.5, 16]].map((p) => { const L = new THREE.PointLight('#e3eaff', 0, 60, 1.0); L.position.set(...p); scene.add(L);
    const s1 = glowSprite('#e8eeff', 0, 5.0), s2 = glowSprite('#dfe6ff', 0, 16); s1.position.set(...p); s2.position.set(...p); scene.add(s1, s2); return { L, s1, s2 }; });
  const faceOn = () => faces.forEach((f) => { f.material = new THREE.MeshBasicMaterial({ color: new THREE.Color('#f2f4ff').multiplyScalar(2.4) }); });
  let hemi = null; scene.traverse((o) => { if (o.isHemisphereLight) hemi = o; });
  const cam0 = cam.position.clone(), look = new THREE.Vector3(10, 0, -71);
  if (mode === 'night') {
    faceOn();
    // trời đêm: thay trời chạng vạng bằng trời vẽ đêm; sương tối lạnh; đèn ráng chiều tắt
    scene.traverse((o) => { if (o.isMesh && o.material && o.material.type === 'ShaderMaterial' && o.geometry.type === 'SphereGeometry') o.visible = false;
      if (o.isDirectionalLight) o.intensity = 0; if (o.isPointLight && o.color.getHexString().startsWith('ffa2')) o.intensity = 0; if (o.isSpotLight) o.intensity = 0; });
    scene.add(paintedSky([[0, '#0b0f26'], [0.5, '#1a2040'], [0.82, '#343c62'], [1, '#6c7898']], { seed: 5, haze: '#c8d2e6', hazeA: 0.5 }));
    scene.fog.color.setRGB(0.42, 0.46, 0.62); if (hemi) { hemi.color.set('#b8c2e0'); hemi.groundColor.set('#3a3a4a'); hemi.intensity = 1.1; }
    // mọi chấm hổ phách thành trắng phẳng; kính đèn khí Ostler tắt; cửa sổ ấm → lạnh
    for (const s of sprites) { const c = s.material.color; if (c.r > c.b * 1.3) { const k = Math.max(c.r, c.g, c.b) * 0.55; s.material.color.setRGB(k * 0.9, k * 0.95, k); } }
    scene.traverse((o) => { if (o.isMesh && o.material && o.material.type === 'MeshBasicMaterial' && o.material.color && o.material.color.r > 3 && o.material.color.b < o.material.color.r * 0.5) o.material = new THREE.MeshBasicMaterial({ color: new THREE.Color('#3a3c4a') });
      if (o.isMesh && o.material && o.material.vertexColors && o.material.type === 'MeshBasicMaterial') { const col = o.geometry.attributes.color; for (let i = 0; i < col.count; i++) { const r0 = col.getX(i), g0 = col.getY(i), b0 = col.getZ(i); if (r0 > b0 * 1.5) { const L = 0.2126 * r0 + 0.7152 * g0 + 0.0722 * b0; col.setXYZ(i, L * 0.9, L * 0.96, L * 1.08); } } col.needsUpdate = true; } });
    whites.forEach((w) => setWhite(w, 1)); sqW.forEach((w) => setWhite(w, 1));
    // trắng tràn cả thành phố: dải chấm trắng dọc các phố khác (thay chấm hổ phách thưa)
    for (const p of pairs) for (const s of p.list) s.visible = true;
    const R2 = rngU(9); for (let i = 0; i < 260; i++) { const x = (R2() - 0.5) * 520, z = -40 - R2() * 560; const s = glowSprite('#e6ecff', 1.6, 4.0); s.position.set(x, 4 + 0.03 * Math.min(z, 0), z); scene.add(s); }
    // MỘT ô cửa vàng (nhà Cas): chọn một ô cửa thật của thành phố gần giữa khung (lưới cửa sổ gộp: mỗi ô 6 đỉnh)
    let winMesh = null; scene.traverse((o) => { if (o.isMesh && o.material && o.material.vertexColors && o.material.type === 'MeshBasicMaterial') winMesh = o; });
    if (winMesh) { const pos = winMesh.geometry.attributes.position, col = winMesh.geometry.attributes.color; cam.updateMatrixWorld(true);
      let best = -1, bd = 1e9; const c = new THREE.Vector3();
      for (let k = 0; k + 5 < pos.count; k += 6) { c.set(0, 0, 0); for (let q = 0; q < 6; q++) c.add(new THREE.Vector3(pos.getX(k + q), pos.getY(k + q), pos.getZ(k + q))); c.multiplyScalar(1 / 6);
        const d = c.distanceTo(cam0); if (d < 60 || d > 130) continue; const n = c.clone().project(cam); const e = Math.hypot(n.x - 0.12, n.y + 0.05); if (n.z < 1 && e < bd) { bd = e; best = k; } }
      if (best >= 0) { for (let q = 0; q < 6; q++) col.setXYZ(best + q, 3.4, 1.9, 0.8); col.needsUpdate = true;
        c.set(0, 0, 0); for (let q = 0; q < 6; q++) c.add(new THREE.Vector3(pos.getX(best + q), pos.getY(best + q), pos.getZ(best + q))); c.multiplyScalar(1 / 6);
        const gg = glowSprite('#ffae5c', 1.2, 3.0); gg.position.copy(c); scene.add(gg); } }
  }
  const update = (t, T) => {
    if (mode === 'dusk') {   // chấm hổ phách hiện dần (người thắp đèn ở các phố khác); máy đẩy chậm
      const k = 0.15 + 0.85 * Math.min(1, t / 3.6); for (const p of pairs) for (const s of p.list) s.visible = p.k < k;
      cam.position.copy(cam0).lerp(look, 0.05 * easeT(t / 4)); cam.lookAt(look);
    } else if (mode === 'wave') {
      faceOn(); const sw = (t0) => sOn(T - t0);
      sqW.forEach((w) => setWhite(w, sw(30.2)));
      order.forEach((i, n) => setWhite(whites[i], sw(31.4 + n * 1.5)));
    } else { cam.position.copy(cam0).lerp(look, 0.04 * easeT(t / 4)); cam.lookAt(look); }
  };
  return { scene, cam, update, chars: [r.chIda], named: {}, paintP: { rNear: 3.0, rFar: 6.5, dNear: 30, dFar: 400, impScale: 0.4, stroke: 0.035, halation: 0.16, bloomWide: 0.07 } };
}
const easeT = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
const sOn = (d) => { if (d < 0) return 0; if (d < 0.08) return 1; if (d < 0.16) return 0; if (d < 0.26) return 1; if (d < 0.34) return 0.05; return Math.min(1, (d - 0.34) / 0.1); };

// ================= TƯỜNG CHIM BÓNG (cảnh 4) — chép bố cục b_cas_bird (Cổng 3) + Ida, đèn lồng, cột điện bật =================
// Tường z = 0 (nhìn +z); Cas (0,15; 0; 0,95) quay vào tường; đèn khí L11 (−2,2; 0; 4,2); cột điện (2,6; 0; 1,6) tay vươn về tường.
export function buildWallSet(ctx) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#0d0c16');
  scene.add(paintedSky([[0, '#0f1030'], [0.7, '#1f1c40'], [1, '#2e2548']], { seed: 3, haze: '#6a6a8a', hazeA: 0.2 }));
  const wallTex = limewashTex(41, { metres: 6, grime: true, brick: 0.06 });
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(12, 7), lamMat({ color: '#ffffff', map: wallTex })); wall.position.set(0, 3.5, 0); wall.receiveShadow = true;
  planarUV(wall.geometry, new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 1, 0), 6, [0.3, 0]); scene.add(wall);
  const plinth = new THREE.Mesh(new THREE.BoxGeometry(12, 0.42, 0.08), lamMat({ color: '#8d877f' })); plinth.position.set(0, 0.21, 0.04); plinth.receiveShadow = true; scene.add(plinth);
  scene.add(groundPlane(14, 12, lamMat({ color: '#ffffff', map: cobbleTex(7) }), 3, { cz: 6 }));
  const hemi = new THREE.HemisphereLight('#3a3c78', '#15121c', 0.30); scene.add(hemi);
  const whiteHemi = new THREE.HemisphereLight('#dfe6ff', '#8a8e9c', 0); scene.add(whiteHemi);
  const glassM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc070').multiplyScalar(2.6), transparent: true, opacity: 0.55, depthWrite: false, side: THREE.DoubleSide });
  const lamp = buildGasLamp({ height: 3.4, mat: (role, c) => role === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) }) : role === 'glass' ? glassM : lamMat({ color: c }) });
  lamp.position.set(-2.2, 0, 4.2); scene.add(lamp); lamp.updateMatrixWorld(true);
  lamp.traverse((m) => { if (m.isMesh) { m.castShadow = m.castShadow && m.material.type !== 'MeshBasicMaterial'; m.receiveShadow = true; } });
  const fp = new THREE.Vector3(); lamp.userData.flame.getWorldPosition(fp);
  const gasL = new THREE.PointLight(GAS.color, GAS.cd, 0, 2); gasL.position.copy(fp); gasL.castShadow = true; gasL.shadow.mapSize.set(1024, 1024); gasL.shadow.bias = -0.0006; gasL.shadow.normalBias = 0.02; gasL.shadow.camera.near = 0.08; scene.add(gasL);
  const gc = glowSprite('#ffc57a', 1.6, 0.6), gw = glowSprite('#ff9a4a', 0.22, 3.2); gc.position.copy(fp); gw.position.copy(fp); scene.add(gc, gw);
  const bulbM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9aa0b4').multiplyScalar(0.3) });
  const E = electricLamp(6.2, (c) => lamMat({ color: c }), bulbM); E.group.position.set(2.6, 0, 1.9); E.group.rotation.y = Math.PI / 2 + 0.25; scene.add(E.group);
  E.group.updateMatrixWorld(true); const hp = E.head.clone().applyMatrix4(E.group.matrixWorld);
  const eL = new THREE.PointLight(ELEC.color, 0, 34, 1.2); eL.position.copy(hp); scene.add(eL);
  const eg = glowSprite('#dfe8ff', 0, 2.6); eg.position.copy(hp); scene.add(eg);
  // Đèn lồng của Ida: nguồn ấm nhỏ có bóng, bám điểm neo lửa của đèn lồng (cast.js)
  const lanL = new THREE.PointLight('#ffa050', 0, 0, 2); lanL.castShadow = true; lanL.shadow.mapSize.set(1024, 1024); lanL.shadow.bias = -0.0006; lanL.shadow.normalBias = 0.02; lanL.shadow.camera.near = 0.03; scene.add(lanL);
  const setState = ({ gas = 1, elec = 0, lantern = 0, lanternPos = null }, f) => {
    gasL.intensity = GAS.cd * gas * flickAt(f); gc.material.color.set('#ffc57a').multiplyScalar(1.6 * gas); gw.material.color.set('#ff9a4a').multiplyScalar(0.22 * gas);
    eL.intensity = ELEC.cd * 0.35 * elec; bulbM.color.set('#9aa0b4').multiplyScalar(0.3).lerp(new THREE.Color('#eef3ff').multiplyScalar(9), elec); eg.material.color.set('#dfe8ff').multiplyScalar(0.55 * elec);
    whiteHemi.intensity = 0.8 * elec;
    lanL.intensity = lantern * 1.9 * flickAt(f + 40); if (lanternPos) lanL.position.copy(lanternPos);
  };
  return { scene, setState, fp };
}

// ================= HỐC CỬA (s5) và NGÕ (s6) =================
export async function buildBaySet(ctx, dbg = {}) {
  const r = await buildS5(ctx.sheets.ida, ctx.sheets.cas, dbg, ctx.mkChar, ctx.upd);
  return r;
}
export async function buildAlleySet(ctx, dbg = {}) {
  const r = await buildS6(ctx.sheets.ida, ctx.sheets.cas, dbg, ctx.mkChar, ctx.upd, 'alley');
  return r;
}

// ================= PHÒNG CAS (cảnh 6, 2:25) — previs mới =================
// Phòng 3,6 × 3,4 m, vữa vôi; cửa sổ ở vách z = −1,8 (bậu có đèn lồng); Cas đứng giữa bậu và vách đối diện (z = +1,6), gần đèn hơn → chim to, mềm.
export function buildRoomSet(ctx) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#050406');
  const wm = lamMat({ color: '#ffffff', map: limewashTex(57, { metres: 4, grime: true, brick: 0.02, base: '#e2d8c6' }) });
  const plane = (w, h, pos, ry, mat = wm) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat); m.position.set(...pos); m.rotation.y = ry; m.receiveShadow = true; scene.add(m); return m; };
  plane(3.6, 2.8, [0, 1.4, 1.6], Math.PI);                  // vách đối diện (nhận chim)
  plane(3.6, 2.8, [0, 1.4, -1.8], 0);                       // vách cửa sổ
  plane(3.4, 2.8, [-1.8, 1.4, -0.1], Math.PI / 2); plane(3.4, 2.8, [1.8, 1.4, -0.1], -Math.PI / 2);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 3.4), lamMat({ color: '#6a5244' })); fl.rotation.x = -Math.PI / 2; fl.position.z = -0.1; fl.receiveShadow = true; scene.add(fl);
  const ce = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 3.4), lamMat({ color: '#d8cdb8' })); ce.rotation.x = Math.PI / 2; ce.position.set(0, 2.8, -0.1); scene.add(ce);
  const win = windowUnit(0.8, 1.0, 'dark', (c) => lamMat({ color: c }), (tex) => new THREE.MeshBasicMaterial({ map: tex, color: new THREE.Color('#9aa4c4').multiplyScalar(0.7) }), 5);
  win.position.set(0.2, 1.55, -1.79); scene.add(win);
  const sill = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.06, 0.3), lamMat({ color: '#8a6a50' })); sill.position.set(0.2, 0.95, -1.66); scene.add(sill);
  const bed = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.45, 1.9), lamMat({ color: '#6a5a6a' })); bed.position.set(1.3, 0.22, 0.4); bed.castShadow = true; bed.receiveShadow = true; scene.add(bed);
  const lan = buildLantern(0.26, (r, c) => r === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff0c8').multiplyScalar(20) }) : r === 'glass' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc56b').multiplyScalar(3), transparent: true, opacity: 0.7, depthWrite: false }) : lamMat({ color: c }));
  lan.position.set(0.2, 0.98, -1.62); scene.add(lan); lan.updateMatrixWorld(true); lan.traverse((o) => { if (o.isMesh) o.castShadow = false; });
  const fp = new THREE.Vector3(); lan.userData.lightAnchor.getWorldPosition(fp);
  // bậu 0,95 m; Cas gần đèn → chim to, mềm
  const L = new THREE.PointLight('#ffa050', 2.4, 0, 2); L.position.copy(fp); L.castShadow = true; L.shadow.mapSize.set(1024, 1024); L.shadow.bias = -0.0006; L.shadow.normalBias = 0.02; L.shadow.camera.near = 0.05; scene.add(L);
  const g = glowSprite('#ffc070', 1.2, 0.5); g.position.copy(fp); scene.add(g);
  scene.add(new THREE.HemisphereLight('#3a2a28', '#120c0a', 0.08));
  return { scene, L, fp };
}

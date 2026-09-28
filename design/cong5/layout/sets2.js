// Cine Lab · Cổng 4 — ANIMATIC: bộ cảnh bọc quanh cảnh đã khoá ở Cổng 3 (s1, s5, s6) + tường chim bóng (chép b_cas_bird) + phòng Cas (previs mới).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { buildS1 } from '/cong3/v2/s1.js';
import { buildS5, LANTERN_Z, PEOPLE_Z } from '/cong3/v2/s5.js';
import { buildS6, ALLEY } from '/cong3/v2/s6.js';
import { buildGasLamp } from '/cong3/shared/props.js';
import { buildLantern, buildLadder } from '/cong3/shared/cast.js';
import { cobbleTex, groundPlane, electricLamp, paintedSky, windowUnit } from '/cong3/v2/street.js';
import { limewashTex, glowSprite, planarUV, rng } from '/cong3/dir-C/common.js';
import { GAS, ELEC, lamMat, flickAt, contactBlob, nightSky, elecGlare, houses, ladderOf } from './sets.js';
import { buildEndWallFrame, makeKit, END } from './sets_end.js';
import { patch as patchS5 } from '/cong3/v2/s5.js';
import { rng as rngU } from '/cong3/dir-C/common.js';

// ================= THÀNH PHỐ (s1) =================
// mode: 'dusk' (0:00 — các chấm hổ phách hiện dần), 'wave' (0:30 — sóng trắng lan từ quảng trường xuống dốc), 'night' (2:10 — cả thành phố trắng, một ô vàng).
export async function buildCitySet(ctx, mode, tm = {}) {   // tm: { square, t0 } — mốc bật (giây phim) từ bảng thời gian film.js
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
  if (mode === 'night' || mode === 'wave') {
    if (mode === 'night') faceOn();
    // trời đêm: thay trời chạng vạng bằng trời vẽ đêm; sương tối lạnh; đèn ráng chiều tắt
    scene.traverse((o) => { if (o.isMesh && o.material && o.material.type === 'ShaderMaterial' && o.geometry.type === 'SphereGeometry') o.visible = false;
      if (o.isDirectionalLight) o.intensity = 0; if (mode === 'night' && o.isPointLight && o.color.getHexString().startsWith('ffa2')) o.intensity = 0; if (mode === 'night' && o.isSpotLight) o.intensity = 0; });
    if (mode === 'wave') {   // v2: 0:30 đã là đêm (AI mù hỏi "bình minh?" vì chân trời hồng) — trời xanh đen, không hồng; đèn khí và cửa sổ ấm giữ nguyên
      scene.add(paintedSky([[0, '#05071a'], [0.5, '#0d1230'], [0.82, '#1c2448'], [1, '#2c3658']], { seed: 5, haze: '#3a4466', hazeA: 0.35 }));
      scene.fog.color.setRGB(0.16, 0.18, 0.3); if (hemi) { hemi.color.set('#39406e'); hemi.groundColor.set('#15121c'); hemi.intensity = 0.55; }
    }
    if (mode === 'night') {
    // Cổng 5 (continuity C4, world-rules v0.5 — quyết định chủ dự án): trời đêm XANH ĐEN CÓ SAO như s10, KHÔNG quầng sáng chân trời; sương xa tối xanh.
    scene.add(nightSky(5));
    scene.fog.color.setRGB(0.05, 0.06, 0.14); if (hemi) { hemi.color.set('#8a94b8'); hemi.groundColor.set('#2a2a38'); hemi.intensity = 0.8; }
    // mọi chấm hổ phách thành trắng phẳng; kính đèn khí Ostler tắt; cửa sổ ấm → lạnh
    for (const s of sprites) { const c = s.material.color; if (c.r > c.b * 1.3) { const k = Math.max(c.r, c.g, c.b) * 0.55; s.material.color.setRGB(k * 0.9, k * 0.95, k); } }
    scene.traverse((o) => { if (o.isMesh && o.material && o.material.type === 'MeshBasicMaterial' && o.material.color && o.material.color.r > 3 && o.material.color.b < o.material.color.r * 0.5) o.material = new THREE.MeshBasicMaterial({ color: new THREE.Color('#3a3c4a') });
      if (o.isMesh && o.material && o.material.vertexColors && o.material.type === 'MeshBasicMaterial') { const col = o.geometry.attributes.color; for (let i = 0; i < col.count; i++) { const r0 = col.getX(i), g0 = col.getY(i), b0 = col.getZ(i); if (r0 > b0 * 1.5) { const L = 0.2126 * r0 + 0.7152 * g0 + 0.0722 * b0; col.setXYZ(i, L * 0.9, L * 0.96, L * 1.08); } } col.needsUpdate = true; } });
    if (mode === 'night') { whites.forEach((w) => setWhite(w, 1)); sqW.forEach((w) => setWhite(w, 1)); }
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
  }
  const update = (t, T) => {
    if (mode === 'dusk') {   // chấm hổ phách hiện dần (người thắp đèn ở các phố khác); máy đẩy chậm
      const k = 0.15 + 0.85 * Math.min(1, t / 3.6); for (const p of pairs) for (const s of p.list) s.visible = p.k < k;
      cam.position.copy(cam0).lerp(look, 0.05 * easeT(t / 4)); cam.lookAt(look);
    } else if (mode === 'wave') {
      faceOn(); const sw = (t0) => sOn(T - t0);
      sqW.forEach((w) => setWhite(w, sw(tm.square ?? 30.2)));
      order.forEach((i, n) => setWhite(whites[i], tm.skipLast && n >= order.length - tm.skipLast ? 0 : sw((tm.t0 ?? 30) + 0.9 + n * 0.8)));   // v2: khối cuối (đoạn cáp cuối) chưa bật
    } else { cam.position.copy(cam0).lerp(look, 0.04 * easeT(t / 4)); cam.lookAt(look); }
  };
  return { scene, cam, update, chars: [r.chIda], named: {}, paintP: { rNear: 3.0, rFar: 6.5, dNear: 30, dFar: 400, impScale: 0.4, stroke: 0.035, halation: 0.16, bloomWide: 0.07 } };
}
const easeT = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
const sOn = (d) => { if (d < 0) return 0; if (d < 0.08) return 1; if (d < 0.16) return 0; if (d < 0.26) return 1; if (d < 0.34) return 0.05; return Math.min(1, (d - 0.34) / 0.1); };

// ================= TƯỜNG CHIM BÓNG (cảnh 4) — chép bố cục b_cas_bird (Cổng 3) + Ida, đèn lồng, cột điện bật =================
// Tường z = 0 (nhìn +z); Cas (0,15; 0; 0,95) quay vào tường; đèn khí L11 (−2,2; 0; 4,2); cột điện (2,6; 0; 1,6) tay vươn về tường.
// Cổng 5 (V3 + nối với bộ phố W1): tường chim là HÔNG NAM nhà kho, CÙNG địa lý với cuối phố của bộ phố (sets_end.buildEndWallFrame — hệ tường
// chim trùng hệ bộ này): Cas (0,15; 0,95) = casSpot (10,35; −7,15) bộ phố; L11 (−2,2; 4,2) = L11 (8; −3,9). Bên TRÁI Cas: hốc cửa (x = −8) rồi góc
// trong + mặt cuối phố (x = −15,2) và phố rẽ; bên PHẢI: cột điện phố chính (3,3; 3,9), đầu hồi căn đầu dãy bắc (x = 4,8), dãy bắc (z = 2,5); sau lưng máy: phố chính (dãy nam z = 13,7).
export const WALL = { bayX: END.bayWorldX - END.OFF_X, faceX: END.FACE_X - END.OFF_X, northX0: END.houseX0N - END.OFF_X, northZ: -5.6 - END.FLANK_Z, southZ: 5.6 - END.FLANK_Z, post: [END.wallPost.x - END.OFF_X, END.wallPost.z - END.FLANK_Z] };
export function buildWallSet(ctx, o = {}) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#0d0c16');
  scene.add(nightSky(31));   // v2: trời đêm có sao (dấu hiệu đêm khi thấy đỉnh cột điện)
  scene.fog = new THREE.Fog('#0c1024', 26, 150);   // như bộ phố: xa là tối xanh
  const wallTex = limewashTex(41, { metres: 6, grime: true, brick: 0.06 });
  const kit = makeKit(houses);
  const endW = buildEndWallFrame(scene, kit, { faceMat: lamMat({ color: '#ffffff', map: wallTex }) });   // gồm cả cột điện phố chính trong sân (B1)
  // phố chính (như bộ phố): dãy bắc từ đầu hồi (x_w 1,8) mặt nhìn +z; dãy nam (z_w 13,7) mặt nhìn −z — mặt tiền trắng phẳng (phố chính đã có điện)
  const litFT = [0, 1, 2, 3].map((k) => lamMat({ color: '#ffffff', map: kit.FT[k].map, emissive: new THREE.Color('#9aa2b8'), emissiveIntensity: 0.32, emissiveMap: kit.FT[k].map }));
  houses(scene, WALL.northX0, 90, WALL.northZ, 1, 81, kit.winKind, litFT, kit.matC, kit.emit);
  houses(scene, WALL.faceX + 1, 90, WALL.southZ, -1, 83, kit.winKind, litFT, kit.matC, kit.emit);
  scene.add(groundPlane(106, WALL.southZ - WALL.northZ, lamMat({ color: '#ffffff', map: cobbleTex(7) }), END.cobbleTile, { cx: 37.8, cz: (WALL.southZ + WALL.northZ) / 2, y: -0.003 }));
  for (const x of [18.8, 46.8, 74.8]) { const s1 = glowSprite('#eef3ff', 1.2, 1.2), s2 = glowSprite('#cfdcff', 0.10, 9); s1.position.set(x, 6.0, 12.0); s2.position.copy(s1.position); scene.add(s1, s2); }   // cột điện phố chính xa (đã sáng)
  for (let k = 0; k < 5; k++) { const s = glowSprite('#cdd6ee', 0.05, 26); s.scale.y *= 0.4; s.position.set(30 + k * 12, 2.5, 8 + (k - 2) * 1.5); scene.add(s); }   // sương sáng lạnh xa trên phố chính
  const hemi = new THREE.HemisphereLight('#3a3c78', '#15121c', 0.30); scene.add(hemi);
  const whiteHemi = new THREE.HemisphereLight('#dfe6ff', '#8a8e9c', 0); scene.add(whiteHemi);
  const glassM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc070').multiplyScalar(2.6), transparent: true, opacity: 0.55, depthWrite: false, side: THREE.DoubleSide });
  const lamp = buildGasLamp({ height: 3.4, mat: (role, c) => role === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) }) : role === 'glass' ? glassM : lamMat({ color: c }) });
  lamp.position.set(-2.2, 0, 4.2); scene.add(lamp); lamp.updateMatrixWorld(true);
  // Cổng 5 (continuity C1): thang của Ida tựa phía bắc cột L11 như bộ phố (ladderAt: chân z −4,75 → z_w 3,35; nghiêng 0,36 rad về cột) — có mặt suốt cảnh 4.
  { const lad = ladderOf(); lad.position.set(-2.2, 0, 3.35); lad.rotation.x = 0.36; lad.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } }); scene.add(lad); }
  lamp.traverse((m) => { if (m.isMesh) { m.castShadow = m.castShadow && m.material.type !== 'MeshBasicMaterial'; m.receiveShadow = true; } });
  const fp = new THREE.Vector3(); lamp.userData.flame.getWorldPosition(fp);
  const gasL = new THREE.PointLight(GAS.color, GAS.cd, 0, 2); gasL.position.copy(fp); gasL.castShadow = true; gasL.shadow.mapSize.set(1024, 1024); gasL.shadow.bias = -0.0006; gasL.shadow.normalBias = 0.02; gasL.shadow.camera.near = 0.08; scene.add(gasL);
  const gc = glowSprite('#ffc57a', 1.6, 0.6), gw = glowSprite('#ff9a4a', 0.22, 3.2); gc.position.copy(fp); gw.position.copy(fp); scene.add(gc, gw);
  // Đèn lồng của Ida: nguồn ấm nhỏ có bóng, bám điểm neo lửa của đèn lồng (cast.js)
  const lanL = new THREE.PointLight('#ffa050', 0, 0, 2); lanL.castShadow = true; lanL.shadow.mapSize.set(1024, 1024); lanL.shadow.bias = -0.0006; lanL.shadow.normalBias = 0.02; lanL.shadow.camera.near = 0.03; scene.add(lanL);
  // B1 (chủ dự án): ánh làm tan chim = vũng sáng TẦM NGẮN của cột điện phố chính trong sân (sets_end, tầm 8,5 m) — tường chim trong vũng, góc L11 ngoài vũng.
  // Không còn trắng tràn toàn cục (v2/v1 dùng whiteHemi 1,8 làm trắng cả góc L11 — trái cảnh 5). Tràn nền 0,054 = mức góc tối của bộ phố (cornerFill 0,06 × 0,9).
  const setState = ({ gas = 1, elec = 0, lantern = 0, lanternPos = null, fillK = 1 }, f) => {
    gasL.intensity = GAS.cd * gas * flickAt(f); gc.material.color.set('#ffc57a').multiplyScalar(1.6 * gas); gw.material.color.set('#ff9a4a').multiplyScalar(0.22 * gas);
    endW.post.set(elec * fillK);
    whiteHemi.intensity = 0.054;
    lanL.intensity = lantern * 1.9 * flickAt(f + 40); if (lanternPos) lanL.position.copy(lanternPos);
  };
  return { scene, setState, fp };
}

// ================= HỐC CỬA (s5) và NGÕ (s6) =================
export async function buildBaySet(ctx, dbg = {}, o = {}) {
  const r = await buildS5(ctx.sheets.ida, ctx.sheets.cas, dbg, ctx.mkChar, ctx.upd);
  if (o.street !== false) addBayStreet(r.scene, o);
  return r;
}
// Cổng 5 (V3/s42): bộ hốc cửa Cổng 3 (khoá) chỉ có mặt tiền + nền đá → nhìn từ trong hốc ra vòm thấy nền đen. Bọc thêm PHỐ TRẮNG bên ngoài:
// dãy nhà đối diện (z = 17, mặt nhìn −z), nền đá kéo dài, trời sao, bóng đèn cột điện xa. Vật liệu dùng patch của s5 → nhận ÁNH ĐIỆN PHẲNG
// đúng như mặt tiền nhà kho (uEo, không bóng), không thêm nguồn sáng nào chiếu vào hốc.
// Địa lý (khớp bộ phố): hốc ở hông nhà kho, tâm x = 2,2 thế giới → hệ hốc: x_b = x − 2,2; z_b = z + 12,1. Trước vòm: sân lát 2,5 m, rồi vỉa hè + lòng phố;
// dãy bắc (z_b 6,5, từ x_b 12,8 — đầu hồi nhìn −x), dãy nam bên kia phố (z_b 17,7, mặt nhìn −z); L11 + thang ở (5,8; 8,2) — o.l11On: lửa còn cháy (cảnh 5 trước 1:52).
export function addBayStreet(scene, o = {}) {
  // Cổng 5 (continuity N4): bộ khoá s5 có một cột điện gang (x 3,45; z 4,9) cạnh vòm — không tồn tại ở địa lý chốt (s27, s35, s41 không có) → ẩn.
  scene.traverse((m) => { if (m.isMesh && Math.abs(m.position.x - 3.45) < 0.01 && Math.abs(m.position.z - 4.9) < 0.01) m.visible = false; });
  const P = (o) => patchS5(new THREE.MeshLambertMaterial(o));
  const kit = makeKit(houses); const FT = kit.FT.map((m) => P({ color: '#ffffff', map: m.map })); const matC = (c) => P({ color: c });
  houses(scene, -34, 40, 17.7, -1, 83, kit.winKind, FT, matC, kit.emit);
  houses(scene, 12.8, 40, 6.5, 1, 81, kit.winKind, FT, matC, kit.emit);
  { const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(7, 0); sh.lineTo(7, 7.4); sh.lineTo(3.5, 10); sh.lineTo(0, 7.4); sh.lineTo(0, 0);
    const geo = new THREE.ShapeGeometry(sh); planarUV(geo, new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 1, 0), 6, [0.2, 0]); const m = new THREE.Mesh(geo, FT[2]); m.rotation.y = -Math.PI / 2; m.position.set(12.8, 0, 6.5 - 7); scene.add(m); }
  { const lamp = buildGasLamp({ height: 3.4, mat: (role, c) => role === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(o.l11On ? 30 : 0.02) }) : role === 'glass' ? new THREE.MeshBasicMaterial({ color: o.l11On ? new THREE.Color('#ffc070').multiplyScalar(2.6) : new THREE.Color('#7c809a').multiplyScalar(0.12), transparent: true, opacity: 0.55, depthWrite: false }) : P({ color: c }) });
    lamp.position.set(5.8, 0.12, 8.2); lamp.rotation.y = Math.PI / 4; scene.add(lamp);
    const lad = buildLadder(1.8, 0.34, 6, (r, c) => P({ color: c }), '#8a6a45'); lad.position.set(5.8, 0.12, 7.35); lad.rotation.x = 0.36; scene.add(lad); }
  const g = new THREE.PlaneGeometry(80, 40); g.rotateX(-Math.PI / 2); g.translate(0, -0.002, 18 + 20); planarUV(g, new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 1), END.cobbleTile, [0, 0]);
  scene.add(new THREE.Mesh(g, P({ color: '#ffffff', map: cobbleTex(9) })));
  scene.add(nightSky(29));
  for (const x of [-9, 9]) { const s1 = glowSprite('#eef3ff', 1.4, 1.1), s2 = glowSprite('#cfdcff', 0.12, 7); s1.position.set(x, 6.3, 12.5); s2.position.copy(s1.position); scene.add(s1, s2); }
}
export async function buildAlleySet(ctx, dbg = {}) {
  const r = await buildS6(ctx.sheets.ida, ctx.sheets.cas, dbg, ctx.mkChar, ctx.upd, 'alley');
  // (c) đá lát ngõ: bộ khoá s6 trải cobbleTex 3 m trên 3 m (viên 0,11–0,17 m, cận s46 đọc thành chấm bi) → lặp 1,25× ⇒ 0,09–0,14 m như các bộ khác (END.cobbleTile).
  const seen = new Set(); r.scene.traverse((m) => { if (m.isMesh && m.material && m.material.map && m.rotation.x < -1.5 && !seen.has(m.material.map)) { seen.add(m.material.map); m.material.map.repeat.set(3 / END.cobbleTile, 3 / END.cobbleTile); m.material.map.needsUpdate = true; } });
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

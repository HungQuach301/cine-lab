// Cine Lab · Cổng 3 — bộ dựng nhân vật dùng chung (Ida, Cas) từ model sheet JSON.
// Mọi hướng mỹ thuật dùng CHUNG khung xương và tỷ lệ này (luật C3); mỗi hướng chỉ đổi vật liệu và mức chi tiết
// qua opts.material(role, colorHex, part) và opts.detail.
// Quy ước: y lên, nhân vật nhìn +z, đơn vị mét. Chi mặc định chỉ xuống −y. Độ dài bộ phận = khoảng cách hai tâm khớp.
// Góc khớp (độ, Euler XYZ): vai/hông rx âm = đưa ra trước; khuỷu rx âm = gập; gối rx dương = gập;
// spine/neck rx dương = cúi về trước; vai trái rz dương = dang ra ngoài (vai phải: rz âm).
import * as THREE from './node_modules/three/build/three.module.js';

const D2R = Math.PI / 180;

function defaultMaterial(role, color) {
  const emissive = role === 'flame' || role === 'glass';
  const m = new THREE.MeshStandardMaterial({
    color, roughness: role === 'tin' ? 0.45 : 0.85, metalness: role === 'tin' ? 0.5 : 0,
    transparent: role === 'glass', opacity: role === 'glass' ? 0.55 : 1,
  });
  if (emissive) { m.emissive = new THREE.Color(color); m.emissiveIntensity = role === 'flame' ? 3.0 : 0.9; }
  return m;
}

export function buildCharacter(sheet, opts = {}) {
  const H = sheet.H_m, P = sheet.parts, C = sheet.local_colors, J = sheet.joints_default;
  const seg = opts.detail ?? 24;
  const matFn = opts.material ?? defaultMaterial;
  const isIda = sheet.id.startsWith('CHR-ida');
  const cache = new Map();
  const mat = (role, color, part) => {
    const k = role + '|' + color + '|' + (part || '');
    if (!cache.has(k)) cache.set(k, matFn(role, color, part));
    return cache.get(k);
  };
  const joints = {}, parts = [], props = {};
  const tag = (m, part) => { m.userData.part = part; m.castShadow = true; m.receiveShadow = true; parts.push(m); return m; };
  const group = (name, parent, x = 0, y = 0, z = 0) => { const g = new THREE.Group(); g.name = name; g.position.set(x, y, z); parent.add(g); joints[name] = g; return g; };

  // Đoạn chi thon từ khớp xuống −y: trụ dài đúng len (giữa 2 tâm khớp) + bi khớp 2 đầu (bi không thuộc mặt nạ đo).
  function limb(parent, len, w0, w1, role, color, part) {
    const g = new THREE.Group(); parent.add(g);
    const cyl = new THREE.Mesh(new THREE.CylinderGeometry(w0 / 2, w1 / 2, len, seg, 1), mat(role, color, part));
    cyl.position.y = -len / 2; tag(cyl, part); g.add(cyl);
    const b0 = new THREE.Mesh(new THREE.SphereGeometry(w0 / 2, seg, seg / 2), mat(role, color, part + '_joint'));
    tag(b0, part + '_joint'); g.add(b0);
    const b1 = new THREE.Mesh(new THREE.SphereGeometry(w1 / 2, seg, seg / 2), mat(role, color, part + '_joint'));
    b1.position.y = -len; tag(b1, part + '_joint'); g.add(b1);
    return g;
  }
  const lathe = (pts, role, color, part, phi0 = 0, phiL = Math.PI * 2, zScale = 1) => {
    const g = new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), seg * 2, phi0, phiL);
    g.scale(1, 1, zScale); g.computeVertexNormals();
    const m = new THREE.Mesh(g, mat(role, color, part)); m.material.side = THREE.DoubleSide; return tag(m, part);
  };

  // ---------- khung xương ----------
  const root = new THREE.Group(); root.name = sheet.id;
  const ankleH = (isIda ? 0.12 : 0.10) * H;
  const hipY = ankleH + (P.shin.length + P.thigh.length) * H;
  const pelvis = group('pelvis', root, 0, hipY, 0);
  const spine = group('spine', pelvis);
  const tL = P.torso.length * H;
  const neck = group('neck', spine, 0, tL, 0);
  const headG = group('head', neck, 0, P.neck.length * H, 0);
  const shY = tL - J.shoulder_offset_from_torso_top_H * H, shX = J.shoulder_spacing_H * H / 2;
  const hipX = J.hip_joint_spacing_H * H / 2;
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1;
    const sh = group('shoulder_' + s, spine, sx * shX, shY, 0);
    const el = group('elbow_' + s, sh, 0, -P.upper_arm.length * H, 0);
    const wr = group('wrist_' + s, el, 0, -P.forearm.length * H, 0);
    const hp = group('hip_' + s, pelvis, sx * hipX, 0, 0);
    const kn = group('knee_' + s, hp, 0, -P.thigh.length * H, 0);
    group('ankle_' + s, kn, 0, -P.shin.length * H, 0);
    void wr;
  }

  // ---------- thân ----------
  const tw = P.torso;
  if (isIda) {
    // Áo khoác phần trên: tiết diện elip, eo nhẹ, vai tròn.
    lathe([[0.001, -0.05 * H], [tw.hip_width / 2 * H, 0.02 * H], [tw.waist_width / 2 * H, 0.85 * H], [tw.shoulder_width / 2 * 0.86 * H, 1.55 * H],
      [tw.shoulder_width / 2 * 0.80 * H, 1.86 * H], [0.34 * H, tL], [0.001, tL + 0.02 * H]], 'coat', C.coat, 'torso', 0, Math.PI * 2, tw.depth_ratio);
    // Cổ áo đứng.
    const collar = lathe([[0.20 * H, tL - 0.05 * H], [0.22 * H, tL + 0.22 * H], [0.24 * H, tL + 0.30 * H]], 'coat', C.coat, 'collar');
    spine.add(collar);
  } else {
    // Áo len rộng, vai xệ, gấu xệ tới hông.
    lathe([[0.001, -0.12 * H], [tw.hip_width / 2 * 1.18 * H, -0.10 * H], [tw.waist_width / 2 * 1.25 * H, 0.6 * H], [tw.shoulder_width / 2 * 0.95 * H, 1.25 * H],
      [0.30 * H, tL - 0.02 * H], [0.001, tL + 0.02 * H]], 'sweater', C.sweater, 'torso', 0, Math.PI * 2, tw.depth_ratio * 1.1);
    const rib = new THREE.Mesh(new THREE.TorusGeometry(0.18 * H, 0.05 * H, 8, seg), mat('sweater', C.sweater, 'collar'));
    rib.rotation.x = Math.PI / 2; rib.position.y = tL - 0.02 * H; tag(rib, 'collar');
    spine.add(rib);
  }
  // Gắn mesh thân (lathe tạo ở trên) vào spine.
  for (const m of parts.filter((m) => !m.parent)) spine.add(m);

  // Vạt áo Ida: 4 vạt (2 trước bám đùi, 2 sau bám hông) — xẻ tà sau, hở nhẹ trước.
  const coatPanels = [];
  if (isIda) {
    const waistY = 0.45 * H, hemY = sheet.costume.coat.hem_height_H * H - hipY;
    const rTop = tw.waist_width / 2 * 1.08 * H, rHem = sheet.costume.coat.hem_width_H / 2 * H;
    const prof = [[rTop, waistY], [rTop * 1.05, waistY - 0.4 * H], [(rTop + rHem) / 2, (waistY + hemY) / 2], [rHem, hemY]];
    const gapF = -0.04, gapB = 0.07; // vạt trước chồng mép nhẹ (áo khép), xẻ tà sau
    const defs = [
      { name: 'front_L', phi0: gapF, phiL: Math.PI / 2 - gapF, follow: 'hip_L', k: 0.6 },
      { name: 'back_L', phi0: Math.PI / 2, phiL: Math.PI / 2 - gapB, follow: 'back', k: 0.35 },
      { name: 'back_R', phi0: Math.PI + gapB, phiL: Math.PI / 2 - gapB, follow: 'back', k: 0.35 },
      { name: 'front_R', phi0: 1.5 * Math.PI, phiL: Math.PI / 2 - gapF, follow: 'hip_R', k: 0.6 },
    ];
    for (const d of defs) {
      const pivot = new THREE.Group(); pivot.name = 'coat_' + d.name;
      const px = d.follow === 'hip_L' ? hipX : d.follow === 'hip_R' ? -hipX : 0;
      pivot.position.set(px, waistY, 0); pelvis.add(pivot);
      const m = lathe(prof.map(([r, y]) => [r, y - waistY]), 'coat', C.coat, 'coat_' + d.name, d.phi0, d.phiL, 0.82);
      m.position.x = -px; pivot.add(m);
      // Lót áo (mặt trong) màu khác, hơi nhỏ hơn — thấy khi vạt tung.
      const lin = lathe(prof.map(([r, y]) => [r * 0.985, y - waistY]), 'lining', C.coat_lining, 'coat_lining', d.phi0, d.phiL, 0.80);
      lin.position.x = -px; pivot.add(lin);
      coatPanels.push({ pivot, ...d });
    }
    // Thắt lưng.
    const belt = new THREE.Mesh(new THREE.TorusGeometry(tw.waist_width / 2 * 1.02 * H, 0.05 * H, 6, seg), mat('boots', C.boots, 'belt'));
    belt.rotation.x = Math.PI / 2; belt.scale.set(1, tw.depth_ratio, 1); belt.position.y = 0.55 * H; tag(belt, 'belt'); spine.add(belt);
  }

  // ---------- cổ, đầu, mặt ----------
  limb(neck, P.neck.length * H, P.neck.width_front * H, P.neck.width_front * 1.05 * H, 'skin', C.skin, 'neck');
  const hd = P.head;
  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.5, seg * 2, seg), mat('skin', C.skin, 'head'));
  skull.scale.set(hd.width_front * H, hd.length * H, hd.width_side * H); skull.position.y = hd.length * H / 2; tag(skull, 'head'); headG.add(skull);
  // Hàm/cằm: Ida cằm dài hơn, Cas má tròn.
  const jaw = new THREE.Mesh(new THREE.SphereGeometry(0.5, seg, seg / 2), mat('skin', C.skin, 'head'));
  jaw.scale.set(hd.width_front * (isIda ? 0.70 : 0.86) * H, 0.55 * H, hd.width_side * 0.78 * H); jaw.position.set(0, 0.30 * H, (isIda ? 0.06 : 0.0) * H); tag(jaw, 'head'); headG.add(jaw);
  const nose = new THREE.Mesh(new THREE.ConeGeometry((isIda ? 0.075 : 0.07) * H, P.nose.length * H, 12), mat('skin', C.skin, 'nose'));
  nose.rotation.x = isIda ? 1.75 : Math.PI / 2; nose.position.set(0, (isIda ? 0.50 : 0.46) * H, hd.width_side / 2 * H + P.nose.length / 2 * H * 0.7); tag(nose, 'nose'); headG.add(nose);
  if (!isIda) { const tip = new THREE.Mesh(new THREE.SphereGeometry(0.07 * H, 12, 8), mat('skin', C.skin, 'nose')); tip.position.copy(nose.position).add(new THREE.Vector3(0, 0, 0.05 * H)); tag(tip, 'nose'); headG.add(tip); }
  for (const sx of [1, -1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry((isIda ? 0.045 : 0.055) * H, 10, 8), mat('eyes', '#1b1616', 'eyes'));
    eye.scale.set(1, isIda ? 0.55 : 1, 0.6); eye.position.set(sx * 0.17 * H, 0.60 * H, hd.width_side / 2 * H * 0.93); tag(eye, 'eyes'); headG.add(eye);
    const brow = new THREE.Mesh(new THREE.CapsuleGeometry(0.018 * H, 0.12 * H, 4, 8), mat('hair', isIda ? C.hair : '#5a4034', 'brow'));
    brow.rotation.z = Math.PI / 2 - sx * (isIda ? 0.22 : 0.16); brow.position.set(sx * 0.17 * H, 0.70 * H, hd.width_side / 2 * H * 0.92); tag(brow, 'brow'); headG.add(brow); // đuôi mày cụp: hiền, buồn
    const earS = isIda ? 0.16 : P.ears.size_H;
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.5, 12, 8), mat('skin', C.skin, 'ear'));
    ear.scale.set(0.08 * H, earS * H, earS * 0.75 * H); ear.position.set(sx * hd.width_front / 2 * H * 0.98, 0.52 * H, -0.02 * H);
    ear.rotation.y = sx * (isIda ? 0.2 : P.ears.angle_out_deg * D2R); ear.rotation.z = -sx * 0.15; tag(ear, 'ear'); headG.add(ear);
  }
  if (isIda) {
    const hs = sheet.costume.hat;
    const bun = new THREE.Mesh(new THREE.SphereGeometry(sheet.costume.hair.bun_diameter_H / 2 * H, 16, 12), mat('hair', C.hair, 'hair'));
    bun.position.set(0, 0.62 * H, -hd.width_side / 2 * H * 0.95); tag(bun, 'hair'); headG.add(bun);
    const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.5, seg, seg / 2, 0, Math.PI * 2, 0, Math.PI * 0.40), mat('hair', C.hair, 'hair')); hairCap.rotation.x = -0.35; // chân tóc lùi khỏi trán
    hairCap.scale.set(hd.width_front * 1.04 * H, hd.length * 1.02 * H, hd.width_side * 1.04 * H); hairCap.position.y = hd.length * H / 2 + 0.01 * H; tag(hairCap, 'hair'); headG.add(hairCap);
    // Tóc phủ kín nửa sau sọ (vòng 1: gáy trần + búi tròn sáng bị đọc nhầm thành khuôn mặt khi quay lưng — B, C phát hiện).
    const backHair = new THREE.Mesh(new THREE.SphereGeometry(0.5, seg, seg / 2, Math.PI, Math.PI, 0, Math.PI * 0.80), mat('hair', C.hair, 'hair'));
    backHair.scale.set(hd.width_front * 1.05 * H, hd.length * 1.03 * H, hd.width_side * 1.05 * H); backHair.position.y = hd.length * H / 2 + 0.01 * H; tag(backHair, 'hair'); headG.add(backHair);
    // Mũ phớt: vành hẹp, cụp trước; chóp có rãnh.
    const hat = new THREE.Group(); hat.position.y = 0.86 * H; hat.rotation.x = 0.08; headG.add(hat);
    const br = hs.brim_diameter_H / 2 * H;
    // Vành mũ: vòng nhiều lớp bán kính để cụp mềm (trước cụp nhiều, sau cụp ít).
    const brimG = new THREE.RingGeometry(hd.width_front * 0.50 * H, br, seg * 3, 8); brimG.rotateX(-Math.PI / 2);
    const pos = brimG.attributes.position; const r0 = hd.width_front * 0.50 * H;
    for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), z = pos.getZ(i) * 1.12, r = Math.hypot(x, pos.getZ(i)); const f = (r - r0) / (br - r0);
      const front = 0.5 + 0.5 * (z / Math.max(1e-6, Math.hypot(x, z))); pos.setZ(i, z); pos.setY(i, -f * f * H * (0.03 + 0.11 * front * front)); }
    const brim = new THREE.Mesh(brimG, mat('hat', C.hat, 'hat')); brim.material.side = THREE.DoubleSide;
    brimG.computeVertexNormals(); tag(brim, 'hat'); hat.add(brim);
    const crown = lathe([[hd.width_front * 0.56 * H, 0], [hd.width_front * 0.55 * H, hs.crown_height_H * 0.7 * H], [hd.width_front * 0.46 * H, hs.crown_height_H * H], [0.001, hs.crown_height_H * 0.9 * H]], 'hat', C.hat, 'hat', 0, Math.PI * 2, 1.12);
    hat.add(crown);
    const band = new THREE.Mesh(new THREE.CylinderGeometry(hd.width_front * 0.565 * H, hd.width_front * 0.565 * H, 0.09 * H, seg * 2, 1, true), mat('boots', C.boots, 'hat'));
    band.scale.z = 1.12; band.position.y = 0.06 * H; tag(band, 'hat'); hat.add(band);
  } else {
    const cs = sheet.costume.cap;
    const cap = new THREE.Group(); cap.position.y = 0.66 * H; headG.add(cap);
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.5, seg * 2, seg, 0, Math.PI * 2, 0, Math.PI * 0.55), mat('cap', C.cap, 'cap'));
    dome.scale.set(hd.width_front * 1.08 * H, cs.height_H * 1.55 * H, hd.width_side * 1.06 * H); tag(dome, 'cap'); cap.add(dome);
    const cuff = new THREE.Mesh(new THREE.TorusGeometry(hd.width_front * 0.54 * H, cs.cuff_H / 2 * H, 10, seg * 2), mat('cap', C.cap, 'cap'));
    cuff.rotation.x = Math.PI / 2; cuff.scale.set(1, hd.width_side / hd.width_front, 1); cuff.position.y = 0.02 * H; tag(cuff, 'cap'); cap.add(cuff);
    const bob = new THREE.Mesh(new THREE.IcosahedronGeometry(cs.bobble_diameter_H / 2 * H, 2), mat('bobble', C.bobble, 'bobble'));
    const bp = bob.geometry.attributes.position; const br0 = cs.bobble_diameter_H / 2 * H; for (let i = 0; i < bp.count; i++) { const x = bp.getX(i) / br0, y = bp.getY(i) / br0, z = bp.getZ(i) / br0; const f = 1 + 0.07 * Math.sin(9 * x + 2) * Math.sin(9 * y + 1) * Math.sin(9 * z + 3); bp.setXYZ(i, bp.getX(i) * f, bp.getY(i) * f, bp.getZ(i) * f); } // nhiễu theo vị trí: đỉnh trùng nhau dịch như nhau, không nứt
    bob.geometry.computeVertexNormals(); bob.position.y = cs.height_H * 0.78 * H + cs.bobble_diameter_H * 0.35 * H; tag(bob, 'bobble'); cap.add(bob);
    // Tóc lún phún dưới mũ, sau gáy.
    const tuft = new THREE.Mesh(new THREE.SphereGeometry(0.5, 12, 8), mat('hair', '#5a4034', 'hair'));
    tuft.scale.set(hd.width_front * 0.9 * H, 0.25 * H, 0.5 * H); tuft.position.set(0, 0.62 * H, -hd.width_side * 0.38 * H); tag(tuft, 'hair'); headG.add(tuft);
  }

  // ---------- tay ----------
  const hands = {};
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1;
    const sleeveRole = isIda ? 'coat' : 'sweater', sleeveCol = isIda ? C.coat : C.sweater;
    const ua = P.upper_arm, fa = P.forearm;
    limb(joints['shoulder_' + s], ua.length * H, ua.width_front * (isIda ? 1 : 1.25) * H, ua.width_front * 0.92 * (isIda ? 1 : 1.25) * H, sleeveRole, sleeveCol, 'upper_arm');
    const faG = limb(joints['elbow_' + s], fa.length * H, fa.width_front * (isIda ? 1 : 1.3) * H, fa.width_front * (isIda ? 1.05 : 1.45) * H, sleeveRole, sleeveCol, 'forearm');
    if (!isIda) { // tay áo trùm quá cổ tay
      const cuff = new THREE.Mesh(new THREE.CylinderGeometry(fa.width_front * 0.75 * H, fa.width_front * 0.78 * H, sheet.costume.sweater.sleeve_over_hand_H * H, seg, 1, true), mat('sweater', C.sweater, 'sleeve_cuff'));
      cuff.material.side = THREE.DoubleSide; cuff.position.y = -fa.length * H - sheet.costume.sweater.sleeve_over_hand_H / 2 * H; tag(cuff, 'sleeve_cuff'); faG.add(cuff);
    }
    // Bàn tay: lòng bàn tay quay vào thân (−sx·x), ngón xoè theo trục z, ngón cái ở phía trước (+z).
    const hp = P.hand, wr = joints['wrist_' + s];
    const hand = new THREE.Group(); hand.name = 'hand_' + s; wr.add(hand);
    const palm = new THREE.Mesh(new THREE.CapsuleGeometry(0.06 * H, hp.palm_length * H - 0.12 * H, 4, 10), mat('skin', C.skin, 'hand'));
    palm.scale.set(1, 1, hp.palm_width / 0.12); palm.position.y = -hp.palm_length / 2 * H; tag(palm, 'hand'); hand.add(palm);
    const fingers = [];
    for (let i = 0; i < 4; i++) {
      const base = new THREE.Group(); base.position.set(0, -hp.palm_length * H * 0.92, (0.75 - i * 0.5) * hp.palm_width / 2 * H); hand.add(base);
      const fl = hp.finger_length * H * [0.92, 1.0, 0.95, 0.78][i];
      const f = new THREE.Mesh(new THREE.CapsuleGeometry(0.036 * H, fl, 4, 8), mat('skin', C.skin, 'hand')); f.position.y = -fl / 2; tag(f, 'hand'); base.add(f);
      fingers.push(base);
    }
    const thumbB = new THREE.Group(); thumbB.position.set(0, -0.08 * H, hp.palm_width / 2 * H * 0.9); hand.add(thumbB);
    const th = new THREE.Mesh(new THREE.CapsuleGeometry(0.04 * H, hp.thumb_length * H, 4, 8), mat('skin', C.skin, 'hand')); th.position.y = -hp.thumb_length / 2 * H; tag(th, 'hand'); thumbB.add(th);
    hands[s] = { hand, fingers, thumb: thumbB, sx };
  }

  // ---------- chân ----------
  for (const s of ['L', 'R']) {
    const th = P.thigh, sh = P.shin, ft = P.foot;
    const legRole = isIda ? 'trousers' : 'trousers', legCol = isIda ? '#2e2a2b' : C.trousers;
    limb(joints['hip_' + s], th.length * H, th.width_front * H, th.width_front * 0.88 * H, legRole, legCol, 'thigh');
    const shinG = limb(joints['knee_' + s], sh.length * H, sh.width_front * H, sh.width_front * 0.85 * H, isIda ? 'trousers' : 'skin', isIda ? legCol : C.skin, 'shin');
    if (!isIda) { // ống quần tới trên cổ chân 0,25 H
      const tl = sh.length * H - sheet.costume.trousers.hem_above_ankle_H * H;
      const tr = new THREE.Mesh(new THREE.CylinderGeometry(sh.width_front * 0.72 * H, sh.width_front * 0.66 * H, tl, seg, 1), mat('trousers', C.trousers, 'shin_trouser'));
      tr.position.y = -tl / 2; tag(tr, 'shin_trouser'); shinG.add(tr);
    }
    const an = joints['ankle_' + s];
    const boot = new THREE.Group(); an.add(boot);
    const sole = new THREE.Mesh(new THREE.CapsuleGeometry(ft.width / 2 * H, ft.length * H - ft.width * H, 4, 12), mat('boots', C.boots, 'foot'));
    sole.rotation.x = Math.PI / 2; sole.scale.set(1, 1, ft.height / ft.width); sole.position.set(0, -ankleH + ft.height / 2 * H * 0.6, ft.length * H * 0.28); tag(sole, 'foot'); boot.add(sole);
    const cuffB = new THREE.Mesh(new THREE.CylinderGeometry(ft.width * 0.55 * H, ft.width * 0.6 * H, ft.height * 1.2 * H, seg), mat('boots', C.boots, 'foot'));
    cuffB.position.y = -ankleH + ft.height * 0.6 * H; tag(cuffB, 'foot'); boot.add(cuffB);
  }

  // ---------- đạo cụ ----------
  const lantern = buildLantern(sheet.props?.lantern?.height_H ? sheet.props.lantern.height_H * H : 0.245, mat);
  props.lantern = lantern;
  if (isIda) { props.ladder = buildLadder(sheet.props.ladder.length_H * H, sheet.props.ladder.width_H * H, sheet.props.ladder.rungs, mat, C.ladder); }
  if (isIda) { // sào mồi: thanh gỗ mảnh, đầu mồi đồng có ngọn lửa nhỏ
    const L = sheet.props.pole.length_H * H, pole = new THREE.Group(); pole.name = 'pole';
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.014, L, 8), mat('ladder', C.ladder, 'pole')); shaft.position.y = L / 2; shaft.castShadow = true; pole.add(shaft);
    const tip = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.02, 0.09, 8), mat('tin', '#9a7a4a', 'pole')); tip.position.y = L + 0.03; tip.castShadow = true; pole.add(tip);
    const fl = new THREE.Mesh(new THREE.SphereGeometry(0.016, 8, 6), mat('flame', '#fff0c8', 'flame')); fl.scale.set(0.8, 1.8, 0.8); fl.position.y = L + 0.1; pole.add(fl);
    pole.userData = { length: L, gripFrac: 0.3 }; props.pole = pole;
  }

  const character = { root, joints, parts, props, hands, coatPanels, H, sheet, hipY };
  character.setPose = (pose) => applyPose(character, pose);
  applyPose(character, sheet.poses.turnaround);
  return character;
}

export function buildLantern(h, mat) {
  mat = mat || ((r, c) => defaultMaterial(r, c));
  const g = new THREE.Group(); g.name = 'lantern';
  const w = h * 0.58, tin = '#8e8a80';
  const post = (x, z) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(h * 0.02, h * 0.02, h * 0.62, 6), mat('tin', tin, 'lantern')); m.position.set(x, h * 0.40, z); m.castShadow = true; g.add(m); };
  for (const [x, z] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) post(x * w / 2, z * w / 2);
  const base = new THREE.Mesh(new THREE.CylinderGeometry(w * 0.62, w * 0.72, h * 0.10, 4), mat('tin', tin, 'lantern')); base.rotation.y = Math.PI / 4; base.position.y = h * 0.05; base.castShadow = true; g.add(base);
  const cap = new THREE.Mesh(new THREE.ConeGeometry(w * 0.78, h * 0.22, 4), mat('tin', tin, 'lantern')); cap.rotation.y = Math.PI / 4; cap.position.y = h * 0.82; cap.castShadow = true; g.add(cap);
  const chim = new THREE.Mesh(new THREE.CylinderGeometry(h * 0.05, h * 0.06, h * 0.08, 8), mat('tin', tin, 'lantern')); chim.position.y = h * 0.95; g.add(chim);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(h * 0.12, h * 0.018, 6, 16), mat('tin', tin, 'lantern')); ring.position.y = h * 1.06; g.add(ring);
  const glass = new THREE.Mesh(new THREE.BoxGeometry(w * 0.96, h * 0.60, w * 0.96), mat('glass', '#ffc56b', 'lantern_glass')); glass.position.y = h * 0.40; g.add(glass);
  const flame = new THREE.Mesh(new THREE.SphereGeometry(h * 0.06, 10, 8), mat('flame', '#fff0c8', 'flame')); flame.scale.set(0.8, 1.8, 0.8); flame.position.y = h * 0.36; g.add(flame);
  const anchor = new THREE.Object3D(); anchor.position.y = h * 0.37; g.add(anchor);
  g.userData = { lightAnchor: anchor, height: h, handleY: h * 1.06 };
  return g;
}

export function buildLadder(len, width, rungs, mat, color) {
  const g = new THREE.Group(); g.name = 'ladder';
  const rail = (x) => { const m = new THREE.Mesh(new THREE.BoxGeometry(width * 0.08, len, width * 0.12), mat('ladder', color, 'ladder')); m.position.set(x, len / 2, 0); m.castShadow = true; g.add(m); };
  rail(width / 2); rail(-width / 2);
  for (let i = 1; i <= rungs; i++) { const m = new THREE.Mesh(new THREE.CylinderGeometry(width * 0.035, width * 0.035, width, 8), mat('ladder', color, 'ladder')); m.rotation.z = Math.PI / 2; m.position.y = len * i / (rungs + 1); m.castShadow = true; g.add(m); }
  return g;
}

function applyPose(ch, pose) {
  const { joints, hands, H } = ch;
  for (const j of Object.values(joints)) j.rotation.set(0, 0, 0);
  ch.root.position.y = (pose.root_y_H || 0) * H;
  for (const [name, [x, y, z]] of Object.entries(pose.joints || {})) {
    const j = joints[name]; if (!j) continue;
    j.rotation.set(x * D2R, y * D2R, z * D2R, 'XYZ');
  }
  // Vạt áo: vạt trước theo gập hông; vạt sau loe ra sau theo gập hông trung bình.
  const hipFlex = (s) => -(joints['hip_' + s].rotation.x);
  for (const p of ch.coatPanels) {
    if (p.follow === 'back') { const f = Math.max(0, (hipFlex('L') + hipFlex('R')) / 2); p.pivot.rotation.x = p.k * f; }
    else { const s = p.follow.slice(-1); p.pivot.rotation.x = -Math.min(0.8, p.k * Math.max(0, hipFlex(s))); } // vạt trước theo đùi, tối đa ~46°
  }
  for (const s of ['L', 'R']) {
    const hp = (pose.hands || {})[s] || { spread: 0.1, curl: 0.4 };
    const h = hands[s];
    h.fingers.forEach((f, i) => {
      f.rotation.set(0, 0, 0);
      f.rotation.x = -(1.5 - i) * 0.30 * (hp.spread ?? 0.1);        // xoè trong mặt phẳng lòng bàn tay (dấu âm: ngón 0 ở +z xoè về +z — sửa lỗi vòng 1, agent 3D phát hiện)
      f.rotation.z = -h.sx * (hp.curl ?? 0.4) * 1.45;                 // gập vào lòng bàn tay (lòng quay vào thân)
    });
    h.thumb.rotation.set(-0.5 - 0.6 * (hp.spread ?? 0.1), 0, -h.sx * (hp.curl ?? 0.4) * 0.9);
    if (hp.thumb_cross) h.thumb.rotation.set(-1.45, 0, 0); // ngón cái dựng theo trục +z của bàn tay (khi xoay cổ tay 90° = dựng đứng: đầu chim)
  }
  // Đạo cụ theo tư thế.
  const want = new Set(pose.props || []);
  const lan = ch.props.lantern, lad = ch.props.ladder;
  if (lan.parent) lan.parent.remove(lan);
  if (lad && lad.parent) lad.parent.remove(lad);
  const pl_ = ch.props.pole; if (pl_ && pl_.parent) pl_.parent.remove(pl_);
  if (want.has('lantern_belt')) { const pl = joints.pelvis; pl.add(lan); lan.position.set(ch.sheet.parts.torso.hip_width / 2 * 1.02 * H, 0.35 * H - lan.userData.handleY, 0.10 * H); lan.rotation.set(0, 0.4, 0); }
  if (want.has('lantern_hand_R')) { ch.root.add(lan); ch._hangLantern = true; } // treo theo trọng lực tại điểm nắm (tính sau khi cập nhật ma trận)
  if (want.has('lantern_ground_front')) { ch.root.add(lan); lan.position.set(0, -ch.root.position.y, 1.05 * H); lan.rotation.set(0, 0.3, 0); }
  if (want.has('ladder_shoulder') && lad) { const sp = joints.spine; sp.add(lad); lad.position.set(-0.55 * H, ch.sheet.parts.torso.length * H + 0.05 * H, -0.3 * H); lad.rotation.set(-(90 - 28) * D2R, 0.18, -0.10); lad.translateY(-lad.children[0].geometry.parameters.height * 0.55); }
  if (want.has('pole_hand_R') && pl_) { const wr = joints.wrist_R; wr.add(pl_); pl_.position.set(0, -ch.sheet.parts.hand.palm_length * H * 0.55, 0); pl_.rotation.set(Math.PI, 0, 0); pl_.translateY(-pl_.userData.length * pl_.userData.gripFrac); } // sào theo trục ngón tay, nắm ở 30% thân sào
  ch.root.updateMatrixWorld(true);
  // Treo đèn lồng: giữ đèn thẳng đứng theo trọng lực khi treo tay/thắt lưng.
  if (ch._hangLantern && want.has('lantern_hand_R')) {
    // Điểm nắm = giữa lòng bàn tay phải (thế giới) → quai đèn tại đó, đèn thõng thẳng xuống, quay mặt theo nhân vật.
    const grip = new THREE.Vector3(0, -ch.sheet.parts.hand.palm_length * H * 0.6, 0); joints.wrist_R.localToWorld(grip);
    const rootInv = new THREE.Matrix4().copy(ch.root.matrixWorld).invert(); grip.applyMatrix4(rootInv);
    const rq = new THREE.Quaternion(); ch.root.getWorldQuaternion(rq);
    lan.position.set(grip.x, grip.y - lan.userData.handleY, grip.z); lan.quaternion.identity(); lan.rotateY(0.4); ch.root.updateMatrixWorld(true);
  } else ch._hangLantern = false;
  if (lan.parent && want.has('lantern_belt')) {
    const q = new THREE.Quaternion(); lan.parent.getWorldQuaternion(q); lan.quaternion.copy(q.invert()); lan.rotateY(0.4); ch.root.updateMatrixWorld(true);
  }
}

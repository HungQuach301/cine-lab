// Cine Lab · Cổng 5 LAYOUT — CUỐI PHỐ OSTLER (V3). GÓI W2 giữ file này. W1 dùng qua buildStreetSet (x0 < 0) của sets.js, không sửa.
// Lỗi V3 (chủ dự án): cuối phố là một tường trống (0:52 s23, 1:04 s27, 1:40 s37w). Bản này dựng CUỐI PHỐ có chiều sâu, không đổi luật thế giới:
//   • nhà kho tường vôi (luật mục 1) — mặt dài có gờ mái, mái ngói đá đen, hai chòi thông gió trên nóc, cửa kéo hàng tầng trên + xà tời,
//     cửa sổ cao có song; HỐC CỬA BỐC HÀNG hình vòm sâu 4 m ngay trên mặt tường (gieo cho cảnh 5);
//   • GÓC NHÀ: mặt tường dừng ở một góc có thật; sau góc, một NGÕ CONG rẽ trái (phố cong — luật mục 1), hai dãy nhà theo cung;
//   • hậu cảnh NHIỀU LỚP: 5 dải mái nhà xa (35–230 m) có ống khói, vài ô cửa sổ; giữa các lớp là SƯƠNG sáng lạnh của các phố đã bật điện
//     (thành phố đã trắng sau 0:34 — luật mục 1 "sóng trắng"), nên mỗi lớp mái in bóng trên một lớp sương sáng hơn → chiều sâu không khí.
// Không nguồn sáng mới nào chiếu lên nhân vật: sương là sprite cộng (không chiếu sáng), cửa sổ tự phát sáng yếu; ánh sáng cảnh giữ nguyên.
//
// HỆ TOẠ ĐỘ "NHÀ KHO" (cục bộ): mặt tường ở z = 0, nhìn ra +z; x chạy dọc mặt tường, +x = PHẢI màn hình khi đứng nhìn vào tường.
// Góc nhà ở x = xL (trái); ngõ cong nằm sau góc (x < xL, đi về −z rồi rẽ trái về −x); hậu cảnh ở −z (sau nhà kho).
//
// API (W1 dùng cho s23 qua buildStreetSet; W2 dùng cho bộ tường chim, bộ hốc cửa):
//   buildStreetEnd(scene, o)            — gọi tự động bởi sets.js khi x0 < 0. Đặt nhà kho tại x = END.FACE_X (bộ phố), mặt nhìn +x.
//                                          o: { sky, x0, x1, matC, FT, winKind, emit, houses } (sets.js truyền). Tuỳ chọn thêm:
//                                          o.endOpts = { corner, bayX, far: true|false, fogGlow: 0…2 } (mặc định END).
//                                          Trả endInfo = { group, warehouse, bayWorld: {x, z}, cornerWorld: {x, z}, toWorld(v) }.
//   buildWarehouse(parent, kit, w)      — nhà kho ở hệ cục bộ. w = { xL, xR, H, bayX, bayHalf, spring, depth, faceMat, roof: true, bay: true }.
//   buildLane(parent, kit, l)           — ngõ cong sau góc. l = { xL, W, R, seed }.
//   buildFarCity(parent, l)             — 5 lớp mái xa + sương. l = { zs, span, seed, glow, winK }.
//   makeKit(houses, { night })          — bộ vật liệu mặt tiền/cửa sổ như sets.js (cho các bộ không qua buildStreetSet).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { limewashTex, glowSprite, planarUV, rng } from '/cong3/dir-C/common.js';
import { facadeTex, windowUnit, cobbleTex } from '/cong3/v2/street.js';

const lamMat = (o) => new THREE.MeshLambertMaterial(o);
const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
// Tham số mặc định (bộ phố): mặt nhà kho ở x = −5 (thế giới), góc nhà ở z = +2 (thế giới) → cục bộ xL = −2; hốc cửa tâm z = −4,6 (thế giới) → cục bộ 4,6.
// Chỗ Cas làm chim (W1 s24/s24c đặt Cas ở z = −2,2 thế giới) nằm giữa góc nhà và hốc cửa: tường vôi trơn.
export const END = { FACE_X: -5, xL: -2.0, xR: 34, H: 8.0, bayX: 4.6, bayHalf: 1.6, spring: 2.4, depth: 4.0, laneW: 6.0, laneR: 16 };

export function makeKit(houses, { night = true } = {}) {
  const matC = (c) => lamMat({ color: c });
  const emit = (k) => (tex) => new THREE.MeshBasicMaterial({ map: tex, color: new THREE.Color('#ffffff').multiplyScalar(k), fog: true });
  const FT = [0, 1, 2, 3].map((k) => lamMat({ color: '#ffffff', map: facadeTex(91 + k * 13, { metres: 6, base: ['#e7e2d6', '#e0dacd', '#e9e4da', '#dcd6ca'][k], courseAt: [3.2, 6.1] }) }));
  const winKind = (Rh) => (Rh() < (night ? 0.07 : 0.16) ? 'gold' : 'dark');
  return { matC, emit, FT, winKind, houses };
}

// Gộp nhiều hình (không chỉ số, chỉ position + normal) thành một — giảm số vật thể cho SwiftShader.
function merge(geos) {
  const parts = geos.map((g) => (g.index ? g.toNonIndexed() : g));
  let n = 0; for (const g of parts) n += g.attributes.position.count;
  const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3); let o = 0;
  for (const g of parts) { if (!g.attributes.normal) g.computeVertexNormals(); pos.set(g.attributes.position.array, o * 3); nor.set(g.attributes.normal.array, o * 3); o += g.attributes.position.count; }
  const out = new THREE.BufferGeometry(); out.setAttribute('position', new THREE.BufferAttribute(pos, 3)); out.setAttribute('normal', new THREE.BufferAttribute(nor, 3)); return out;
}
const archShape = (cx, hw, sp) => { const s = new THREE.Shape(); s.moveTo(cx - hw, 0); s.lineTo(cx - hw, sp); s.absarc(cx, sp, hw, Math.PI, 0, true); s.lineTo(cx + hw, 0); s.lineTo(cx - hw, 0); return s; };

// ================= NHÀ KHO (cục bộ) =================
export function buildWarehouse(parent, kit, w = {}) {
  const { xL = END.xL, xR = END.xR, H = END.H, bayX = END.bayX, bayHalf = END.bayHalf, spring = END.spring, depth = END.depth } = w;
  const g = new THREE.Group(); g.name = 'warehouse'; parent.add(g);
  const R = rng(w.seed ?? 211);
  const faceMat = w.faceMat || lamMat({ color: '#ffffff', map: limewashTex(41, { metres: 6, grime: true, brick: 0.06 }) });
  const stone = lamMat({ color: '#c4bcb0' }), stoneD = lamMat({ color: '#8d877f' }), slate = lamMat({ color: '#2c2834', side: THREE.DoubleSide }), wood = lamMat({ color: '#4a3226' }), iron = lamMat({ color: '#3a3e46' });
  const add = (geo, mat, cast = false) => { const m = new THREE.Mesh(geo, mat); m.receiveShadow = true; m.castShadow = cast; g.add(m); return m; };
  const box = (sx, sy, sz, mat, x, y, z, cast = false) => { const m = add(new THREE.BoxGeometry(sx, sy, sz), mat, cast); m.position.set(x, y, z); return m; };
  const hasBay = w.bay !== false;
  // mặt tường (có lỗ vòm)
  { const s = new THREE.Shape(); s.moveTo(xL, 0); s.lineTo(xR, 0); s.lineTo(xR, H); s.lineTo(xL, H); s.lineTo(xL, 0);
    if (hasBay) s.holes.push(archShape(bayX, bayHalf, spring));
    const geo = new THREE.ShapeGeometry(s, 48); planarUV(geo, X, Y, 6, [0.3, 0]); add(geo, faceMat); }
  // gờ chân tường (trừ lòng vòm)
  const plinth = (a, b) => { if (b - a > 0.05) box(b - a, 0.42, 0.08, stoneD, (a + b) / 2, 0.21, 0.04); };
  if (hasBay) { plinth(xL, bayX - bayHalf - 0.3); plinth(bayX + bayHalf + 0.3, xR); } else plinth(xL, xR);
  // gờ mái + mái dốc (lên về −z) + nóc
  box(xR - xL + 0.3, 0.32, 0.42, lamMat({ color: '#d8d2c6' }), (xL + xR) / 2, H - 0.16, 0.12);
  const run = 7.0, rise = 4.2, slope = Math.hypot(run, rise);
  if (w.roof !== false) {
    const roof = add(new THREE.PlaneGeometry(xR - xL + 0.4, slope), slate); roof.rotation.x = -Math.PI / 2 + Math.atan2(rise, run); roof.position.set((xL + xR) / 2, H + rise / 2, -run / 2 + 0.2);
    // mặt hồi ở góc nhà (tam giác vôi) + tường bên
    const sideW = 14; const side = new THREE.Shape(); side.moveTo(0, 0); side.lineTo(0, H); side.lineTo(-run, H + rise); side.lineTo(-sideW, H); side.lineTo(-sideW, 0); side.lineTo(0, 0);
    const sg = new THREE.ShapeGeometry(side); planarUV(sg, X, Y, 6, [1.1, 0]); const sm = add(sg, faceMat); sm.rotation.y = -Math.PI / 2; sm.position.set(xL, 0, 0);   // cục bộ −x → −z; mặt nhìn −x (về ngõ)
    const back = add(new THREE.PlaneGeometry(xR - xL + 0.4, Math.hypot(sideW - run, rise)), slate); back.rotation.x = -Math.PI / 2 - Math.atan2(rise, sideW - run); back.position.set((xL + xR) / 2, H + rise / 2, -run - (sideW - run) / 2);
    // hai chòi thông gió trên nóc (mái chóp) — bóng dáng nhà kho
    for (const vx of [xL + (xR - xL) * 0.28, xL + (xR - xL) * 0.66]) {
      box(1.5, 1.3, 1.5, lamMat({ color: '#bdb6aa' }), vx, H + rise + 0.55, -run, true);
      for (let k = 0; k < 4; k++) box(1.52, 0.06, 0.02, iron, vx, H + rise + 0.3 + k * 0.22, -run + 0.76);   // nan chớp
      const cap = add(new THREE.ConeGeometry(1.25, 0.9, 4), slate, true); cap.rotation.y = Math.PI / 4; cap.position.set(vx, H + rise + 1.65, -run);
    }
    // ống khói nhỏ ở đầu hồi
    box(0.7, 1.8, 0.7, lamMat({ color: '#6a5a52' }), xL + 1.2, H + rise * 0.55 + 0.9, -run * 0.55, true);
  }
  // cửa kéo hàng tầng trên + xà tời (nhận diện nhà kho), không chữ
  const hx = hasBay ? bayX : (xL + xR) / 2;
  box(1.5, 2.1, 0.08, wood, hx, H - 2.25, 0.03); for (const dx of [-0.36, 0.36]) box(0.04, 2.0, 0.1, lamMat({ color: '#35241c' }), hx + dx, H - 2.25, 0.06);
  box(1.8, 0.14, 0.2, stone, hx, H - 1.15, 0.08); box(0.16, 0.16, 1.2, wood, hx, H - 0.55, 0.55, true);
  const rope = add(new THREE.CylinderGeometry(0.012, 0.012, 1.6, 6), lamMat({ color: '#6b5a44' })); rope.position.set(hx, H - 1.35, 1.05);
  add(new THREE.TorusGeometry(0.07, 0.015, 6, 12), iron).position.set(hx, H - 2.2, 1.05);
  // cửa sổ cao có song (tối) — nhịp đều trên mặt tường
  for (let x = xL + 2.4; x < xR - 1.5; x += 4.2) {
    if (Math.abs(x - hx) < 1.9) continue;
    const u = windowUnit(0.9, 1.1, 'dark', (c) => lamMat({ color: c }), (tex) => new THREE.MeshBasicMaterial({ map: tex, color: new THREE.Color('#ffffff').multiplyScalar(0.9), fog: true }), Math.floor(R() * 1e6));
    u.position.set(x, H - 2.3, 0); g.add(u);
    for (const dx of [-0.2, 0, 0.2]) box(0.025, 1.1, 0.03, iron, x + dx, H - 2.3, 0.1);
  }
  // ống thoát nước gang ở góc nhà và giữa tường
  for (const px of [xL + 0.25, (xL + xR) / 2 + 3.1]) { const p = add(new THREE.CylinderGeometry(0.055, 0.055, H, 12), iron); p.position.set(px, H / 2, 0.1); }
  // HỐC CỬA BỐC HÀNG (vòm sâu `depth`): vòm đá cuốn + lòng hốc (vách trong, hai vách bên, vòm, nền đá) — không đèn trong hốc
  let bayInfo = null;
  if (hasBay) {
    const r0 = bayHalf, r1 = bayHalf + 0.3, n = 15;
    const vs = []; for (let i = 0; i < n; i++) { const a0 = Math.PI * i / n + 0.006, a1 = Math.PI * (i + 1) / n - 0.006, rr = r1 + (i === 7 ? 0.08 : 0) + (i % 2) * 0.03;
      const s = new THREE.Shape(); s.moveTo(Math.cos(a0) * r0, Math.sin(a0) * r0); s.lineTo(Math.cos(a0) * rr, Math.sin(a0) * rr); s.lineTo(Math.cos(a1) * rr, Math.sin(a1) * rr); s.lineTo(Math.cos(a1) * r0, Math.sin(a1) * r0);
      const eg = new THREE.ExtrudeGeometry(s, { depth: 0.05, bevelEnabled: false }); eg.translate(bayX, spring, -0.01); vs.push(eg); }
    for (const sx of [-1, 1]) for (let j = 0, y = 0.42; j < 5; j++) { const h = 0.36 + (j % 2) * 0.04, ww = j % 2 ? 0.34 : 0.48; const bg = new THREE.BoxGeometry(ww, h - 0.02, 0.06); bg.translate(bayX + sx * (bayHalf + ww / 2), y + h / 2, 0.01); vs.push(bg); y += h; if (y > spring - 0.1) break; }
    add(merge(vs), stone);
    // lòng hốc: vôi như vách ngoài nhưng albedo hạ (thay cho che khuất ánh tràn — bộ phố dùng ánh bán cầu toàn cục, không có che khuất): luật 3.4, hốc khuất điện
    const inner = lamMat({ color: '#5e5a54', map: limewashTex(12, { metres: 4, grime: true, brick: 0.04 }) });
    { const bg = new THREE.ShapeGeometry(archShape(bayX, bayHalf, spring), 32); planarUV(bg, X, Y, 4, [0, 0]); add(bg, inner).position.z = -depth; }
    for (const sx of [-1, 1]) { const pg = new THREE.PlaneGeometry(depth, spring); pg.rotateY(-sx * Math.PI / 2); pg.translate(bayX + sx * bayHalf, spring / 2, -depth / 2); add(pg, inner); }
    { const cg = new THREE.CylinderGeometry(bayHalf, bayHalf, depth, 32, 1, true, -Math.PI / 2, Math.PI); cg.rotateX(-Math.PI / 2); cg.translate(bayX, spring, -depth / 2);
      const vm = inner.clone(); vm.side = THREE.BackSide; add(cg, vm); }
    { const fg = new THREE.PlaneGeometry(bayHalf * 2, depth); fg.rotateX(-Math.PI / 2); fg.translate(bayX, 0.004, -depth / 2); add(fg, lamMat({ color: '#3e3a36' })); }
    box(bayHalf * 2 + 0.1, 0.05, 0.32, stone, bayX, 0.025, 0.06);
    bayInfo = { x: bayX, halfW: bayHalf, spring, depth };
  }
  return { group: g, bay: bayInfo, xL, xR, H };
}

// ================= NGÕ CONG sau góc nhà (cục bộ) =================
// Tâm ngõ bắt đầu ở (xL − W/2, 0), đi về −z rồi RẼ TRÁI (về −x) theo cung bán kính R — phố cong, không thấy điểm cuối.
export function buildLane(parent, kit, l = {}) {
  const { xL = END.xL, W = END.laneW, R = END.laneR, seed = 57 } = l;
  const g = new THREE.Group(); g.name = 'lane'; parent.add(g);
  const C = new THREE.Vector3(xL - W / 2 - R, 0, 0);
  const cob = lamMat({ color: '#ffffff', map: cobbleTex(13) });
  { const gg = new THREE.PlaneGeometry(90, 90); gg.rotateX(-Math.PI / 2); gg.translate(xL - 45, -0.004, -45 + 6); planarUV(gg, X, Z, 3, [0, 0]); const m = new THREE.Mesh(gg, cob); m.receiveShadow = true; g.add(m); }
  const seg = (radius, a0, a1, faceIn, sd) => {
    const step = 6.5 / radius; let k = 0;
    for (let a = a0; a < a1 - 1e-3; a += step, k++) {
      const am = Math.min(a + step / 2, a1), p = new THREE.Vector3(C.x + radius * Math.cos(am), 0, C.z - radius * Math.sin(am));
      const n = new THREE.Vector3(Math.cos(am), 0, -Math.sin(am)).multiplyScalar(faceIn ? -1 : 1);
      const hg = new THREE.Group(); hg.position.copy(p); hg.rotation.y = Math.atan2(n.x, n.z); g.add(hg);
      kit.houses(hg, -3.35, 3.35, 0, 1, sd + k * 7, kit.winKind, kit.FT, kit.matC, kit.emit);
    }
  };
  seg(R + W / 2, 0.55, Math.PI / 2 + 0.9, true, seed);          // bờ ngoài (phía nhà kho), mặt quay vào tâm cung
  seg(R - W / 2, 0.0, Math.PI / 2 + 0.9, false, seed + 300);    // bờ trong, mặt quay ra
  return { group: g, C };
}

// ================= HẬU CẢNH NHIỀU LỚP (cục bộ, về −z) =================
// Mỗi lớp: một dải nhà (khối + mái hồi + ống khói) gộp một vật thể; vài ô cửa (ấm hiếm, lạnh nhiều hơn vì thành phố đã trắng).
// Giữa hai lớp: sương sáng lạnh (sprite cộng, KHÔNG chiếu sáng) — ánh điện các phố xa hắt vào hơi nước.
export function buildFarCity(parent, l = {}) {
  const zs = l.zs || [-34, -58, -92, -145, -230], span = l.span || [120, 160, 220, 300, 420], R = rng(l.seed ?? 907), glowK = l.glow ?? 1;
  const g = new THREE.Group(); g.name = 'farCity'; parent.add(g);
  const cols = ['#3b3a48', '#34344a', '#2d2f46', '#282b44', '#23263f'];
  zs.forEach((z0, li) => {
    const geos = [], wins = [], half = span[li] / 2; let x = -half;
    while (x < half) {
      const w = 5 + R() * 8, h = 6 + R() * (li < 2 ? 8 : 12) + (R() < 0.08 ? 10 : 0), d = 8, zz = z0 - R() * 6;
      const b = new THREE.BoxGeometry(w, h, d); b.translate(x + w / 2, h / 2, zz); geos.push(b);
      const rh = 1.5 + R() * 2.5, rs = new THREE.Shape(); rs.moveTo(-w / 2, 0); rs.lineTo(w / 2, 0); rs.lineTo(0, rh); rs.lineTo(-w / 2, 0);
      if (R() < 0.6) { const rg = new THREE.ExtrudeGeometry(rs, { depth: d, bevelEnabled: false }); rg.translate(x + w / 2, h, zz - d / 2); geos.push(rg); }
      else { const rg = new THREE.ExtrudeGeometry(rs, { depth: w, bevelEnabled: false }); rg.rotateY(Math.PI / 2); rg.translate(x + w / 2 - w / 2, h, zz); geos.push(rg); }
      for (let c = 0, nc = R() < 0.8 ? 1 + (R() * 2 | 0) : 0; c < nc; c++) { const cg = new THREE.BoxGeometry(0.6, 1.6 + R(), 0.6); cg.translate(x + w * (0.2 + 0.6 * R()), h + rh * 0.6 + 0.6, zz + (R() - 0.5) * 3); geos.push(cg); }
      if (li < 4) for (let k = 0, nw = (w / 2.5) | 0; k < nw; k++) for (let fy = 2.2; fy < h - 1; fy += 2.6) { const q = R(); if (q < 0.1) wins.push([x + 1.2 + k * 2.5, fy, zz + d / 2 + 0.05, q < 0.025 ? 'gold' : 'cold']); }
      if (li === 1 && R() < 0.12) { const sp = new THREE.CylinderGeometry(0.0, 1.4, 9, 6); sp.translate(x + w / 2, h + 4.5, zz); geos.push(sp); }   // một chóp tháp thỉnh thoảng (không biểu tượng tôn giáo, không chữ)
      x += w + (R() < 0.25 ? 2 + R() * 6 : 0);
    }
    const m = new THREE.Mesh(merge(geos), lamMat({ color: cols[li] })); m.receiveShadow = false; g.add(m);
    if (wins.length) { const wg = []; for (const [wx, wy, wz, k] of wins) { const q = new THREE.PlaneGeometry(0.8, 1.1); q.translate(wx, wy, wz); wg.push([q, k]); }
      for (const kind of ['gold', 'cold']) { const list = wg.filter((v) => v[1] === kind).map((v) => v[0]); if (!list.length) continue;
        const mm = new THREE.Mesh(merge(list), new THREE.MeshBasicMaterial({ color: new THREE.Color(kind === 'gold' ? '#ffb45c' : '#dfe6f4').multiplyScalar(kind === 'gold' ? 1.3 : 0.7), fog: true })); g.add(mm); } }
    // sương sáng giữa lớp này và lớp sau: dải sprite thấp, lạnh
    if (glowK > 0) for (let k = 0; k < 7; k++) { const s = glowSprite('#cdd6ee', 0.05 * glowK * (1 + li * 0.35), 30 + li * 14); s.position.set(-half + (k + 0.5) * span[li] / 7 + (R() - 0.5) * 8, 2 + li * 1.5, z0 - 10 - li * 6); s.scale.y *= 0.45; g.add(s); }
  });
  return { group: g };
}

// ================= BỘ PHỐ: gắn cuối phố vào buildStreetSet (sets.js gọi) =================
export function buildStreetEnd(scene, o) {
  const e = { ...END, ...(o.endOpts || {}) };
  const kit = { matC: o.matC, FT: o.FT, winKind: o.winKind, emit: o.emit, houses: o.houses };
  // nhóm cục bộ: mặt tường (cục bộ z = 0, nhìn +z) → thế giới x = FACE_X nhìn +x; cục bộ +x → thế giới −z (bắc = phải màn hình khi nhìn xuôi dốc)
  const G = new THREE.Group(); G.position.set(e.FACE_X, 0, 0); G.rotation.y = Math.PI / 2; scene.add(G);
  const wh = buildWarehouse(G, kit, { xL: e.xL, xR: e.xR, H: e.H, bayX: e.bayX, bayHalf: e.bayHalf, spring: e.spring, depth: e.depth });
  const lane = buildLane(G, kit, { xL: e.xL, W: e.laneW, R: e.laneR });
  if (e.far !== false) buildFarCity(G, { glow: e.fogGlow ?? 1 });
  G.updateMatrixWorld(true);
  const toWorld = (v) => v.clone().applyMatrix4(G.matrixWorld);
  const bw = toWorld(new THREE.Vector3(e.bayX, 0, 0)), cw = toWorld(new THREE.Vector3(e.xL, 0, 0));
  return { group: G, warehouse: wh, lane, bayWorld: { x: bw.x, z: bw.z }, cornerWorld: { x: cw.x, z: cw.z }, toWorld };
}

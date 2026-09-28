// Cine Lab · Cổng 5 LAYOUT — CUỐI PHỐ OSTLER (V3). GÓI W2 giữ file này. W1 dùng qua buildStreetSet (x0 < 0) của sets.js, không sửa.
// Lỗi V3 (chủ dự án): cuối phố là một tường trống (0:52 s23, 1:04 s27, 1:40 s37w). Bản này dựng CUỐI PHỐ có chiều sâu, không đổi luật thế giới:
//   • NHÀ KHO tường vôi hình chữ L (luật mục 1): MẶT CUỐI PHỐ (x = −5, chắn cuối phố) + HÔNG NAM chạy dọc phía bắc đoạn cuối phố (z = −8,1,
//     lùi 2,5 m sau mặt tiền dãy bắc) = TƯỜNG CHIM (cảnh 4) có HỐC CỬA BỐC HÀNG vòm sâu 4 m (cảnh 5). Gờ mái + máng nước, mái ngói đá đen,
//     chòi thông gió trên nóc, cửa kéo hàng tầng trên + xà tời, cửa sổ cao có song, ống thoát nước, gờ chân tường;
//   • GÓC NGỌN 11: L11 (8; −3,9) đứng trước hông nhà kho, lùi 7 m sau góc căn nhà đầu dãy bắc (x = 15) — ngoài vũng sáng cột điện phố chính (luật v0.4);
//   • PHỐ RẼ TRÁI: ở góc nam mặt cuối phố (z = +2), phố rẽ sang trái khung (về +z), CONG và DỐC XUỐNG (5 %), hai dãy nhà theo cung;
//   • hậu cảnh NHIỀU LỚP: dải mái nhà xa (35–230 m) sau nhà kho và cuối phố rẽ, ống khói, vài ô cửa; SƯƠNG sáng lạnh sát mặt phố giữa các lớp
//     (sprite cộng, không chiếu sáng, KHÔNG làm sáng trời — luật v0.4 "Đêm").
// Không nguồn sáng mới nào chiếu lên nhân vật; ánh sáng cảnh giữ nguyên.
//
// HỆ "TƯỜNG CHIM" (wall frame — cũng là hệ của bộ tường chim sets2.buildWallSet): hông nhà kho ở z = 0 nhìn +z (nam); x_w = x − 10,2; z_w = z + 8,1
// (x, z: thế giới bộ phố). +x_w = PHẢI màn hình khi đứng nhìn vào tường chim. Trong hệ này: Cas (0,15; 0,95), L11 (−2,2; 4,2) — đúng bố cục b_cas_bird.
// HỆ "NHÀ KHO" cục bộ của buildWarehouse: mặt tường z = 0 nhìn +z, x dọc tường.
//
// ĐỊA LÝ CHỐT (thế giới bộ phố):
//   mặt cuối phố x = −5, từ góc nam z = +2 tới góc trong z = −8,1; hông nam z = −8,1, từ x = −5 tới x = 15 (giáp đầu hồi căn đầu dãy bắc);
//   dãy nhà bắc bắt đầu x = 15 (houseX0N); dãy nam giữ −4; sân trước hông (x −5 … 15, z −8,1 … −5,6) lát đá;
//   Cas làm chim ở casSpot (10,35; −7,15): cách tường 0,95 m, cách L11 4,0 m; L11 cách tường 4,2 m;
//   hốc cửa: tâm x = 2,2 (rộng 3,2 m, sâu 4 m) — cách chỗ Cas 8,15 m về bên TRÁI (nhìn vào tường), "a few steps along the wall".
//
// API:
//   buildStreetEnd(scene, o)  — sets.js gọi khi x0 < 0 (TRƯỚC khi dựng hai dãy nhà). o: { sky, x0, x1, matC, FT, winKind, emit, houses, endOpts }.
//       endOpts (tuỳ chọn) = { far: true|false, fogGlow: 0…2 }. Trả endInfo = { group, houseX0N, houseX0S, casSpot: [x, z], bayWorld: {x, z},
//       cornerWorld: {x, z}, faceX, flankZ, toWorld(v_w) (hệ tường chim → thế giới) }.
//   buildEndWallFrame(W, kit, o) — toàn bộ cuối phố trong hệ tường chim (nhóm W). o = { faceMat, far, fogGlow }.
//   buildWarehouse(parent, kit, w) — một mặt nhà kho ở hệ cục bộ. w = { xL, xR, H, bayX, bayHalf, spring, depth, faceMat, roof, bay, side }.
//   buildLane(parent, kit, l)      — phố rẽ cong, dốc (hệ cục bộ mặt cuối phố). l = { xL, W, R, slope, seed }.
//   buildFarCity(parent, l)        — dải mái xa + sương. l = { zs, span, seed, glow, drop }.
//   makeKit(houses, { night })     — bộ vật liệu mặt tiền/cửa sổ như sets.js.  wallFromWorld([x, z]) — đổi toạ độ; END — hằng số.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { limewashTex, glowSprite, planarUV, rng, flagTex } from '/cong3/dir-C/common.js';
import { facadeTex, windowUnit, cobbleTex, electricLamp } from '/cong3/v2/street.js';
import { elecGlare, ELEC } from './sets.js';   // chỉ dùng lúc gọi hàm (vòng import sets.js ↔ sets_end.js an toàn)

const lamMat = (o) => new THREE.MeshLambertMaterial(o);
const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
// B1 (quyết định chủ dự án sau Cổng 5, AUTHORSHIP @2591e4d): cột điện phố chính (bật 1:04,4) ĐẶT TRONG SÂN trước hông nhà kho, tầm vũng sáng ngắn;
// chỗ Cas làm chim dời sang đông 3,95 m. Tường chim nằm trong vũng sáng của cột; góc L11 (cách đầu đèn ≈ 9,6 m) ngoài tầm → tối tới khi P5 bật.
// Dãy bắc lùi tới x = 18,5 để sân đủ chỗ cho cột + máy (đầu hồi căn đầu dãy cách Cas 4,2 m).
export const END = { OFF_X: 10.2, FLANK_Z: -8.1, FACE_X: -5, cornerZ: 2.0, houseX0N: 18.5, houseX0S: -4, bayWorldX: 2.2, casSpot: [14.3, -7.15],
  wallPost: { x: 17.0, z: -5.9, range: 8.5, ry: Math.PI / 2 + 0.35, cd: 30 },   // cột: chân (17,0; −5,9); tay vươn về tường; PointLight tầm 8,5 m, suy giảm 1,2, không bóng (luật 2)
  cobbleTile: 2.4,   // (c) đá lát: texture cobbleTex 3 m → trải trên 2,4 m ⇒ viên 0,09–0,14 m (TB ≈ 0,11 m ≈ 1/14,5 chiều cao Ida)
  H: 8.0, bayHalf: 1.6, spring: 2.4, depth: 4.0, laneW: 6.0, laneR: 16, slope: 0.05 };
export const wallFromWorld = ([x, z]) => [x - END.OFF_X, z - END.FLANK_Z];

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
  const { xL = -10, xR = 10, H = END.H, bayX = 0, bayHalf = END.bayHalf, spring = END.spring, depth = END.depth } = w;
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
  // gờ mái + máng nước (gang) + mái dốc (lên về −z) + nóc
  box(xR - xL + 0.3, 0.32, 0.42, lamMat({ color: '#d8d2c6' }), (xL + xR) / 2, H - 0.16, 0.12);
  const gut = add(new THREE.CylinderGeometry(0.07, 0.07, xR - xL + 0.3, 10), iron); gut.rotation.z = Math.PI / 2; gut.position.set((xL + xR) / 2, H + 0.05, 0.38);
  const run = 7.0, rise = 4.2, slope = Math.hypot(run, rise);
  if (w.roof !== false) {
    const roof = add(new THREE.PlaneGeometry(xR - xL + 0.4, slope), slate); roof.rotation.x = -Math.PI / 2 + Math.atan2(rise, run); roof.position.set((xL + xR) / 2, H + rise / 2, -run / 2 + 0.2);
    // mặt hồi ở góc nhà (tam giác vôi) + tường bên — cục bộ −x → −z; mặt nhìn −x
    const sideW = 14; const side = new THREE.Shape(); side.moveTo(0, 0); side.lineTo(0, H); side.lineTo(-run, H + rise); side.lineTo(-sideW, H); side.lineTo(-sideW, 0); side.lineTo(0, 0);
    if (w.side !== false) { const sg = new THREE.ShapeGeometry(side); planarUV(sg, X, Y, 6, [1.1, 0]); const sm = add(sg, faceMat); sm.rotation.y = -Math.PI / 2; sm.position.set(xL, 0, 0); }
    const back = add(new THREE.PlaneGeometry(xR - xL + 0.4, Math.hypot(sideW - run, rise)), slate); back.rotation.x = -Math.PI / 2 - Math.atan2(rise, sideW - run); back.position.set((xL + xR) / 2, H + rise / 2, -run - (sideW - run) / 2);
    // hai chòi thông gió trên nóc (mái chóp) — bóng dáng nhà kho
    for (const vx of [xL + (xR - xL) * 0.22, xL + (xR - xL) * 0.55]) {
      box(1.5, 1.3, 1.5, lamMat({ color: '#bdb6aa' }), vx, H + rise + 0.55, -run, true);
      for (let k = 0; k < 4; k++) box(1.52, 0.06, 0.02, iron, vx, H + rise + 0.3 + k * 0.22, -run + 0.76);   // nan chớp
      const cap = add(new THREE.ConeGeometry(1.25, 0.9, 4), slate, true); cap.rotation.y = Math.PI / 4; cap.position.set(vx, H + rise + 1.65, -run);
    }
    if (w.side !== false) box(0.7, 1.8, 0.7, lamMat({ color: '#6a5a52' }), xL + 1.2, H + rise * 0.55 + 0.9, -run * 0.55, true);   // ống khói ở đầu hồi
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
  // ống thoát nước gang: ở góc nhà và giữa tường
  for (const px of [xL + 0.25, (xL + xR) / 2 + 3.1, xR - 0.25]) { const p = add(new THREE.CylinderGeometry(0.055, 0.055, H, 12), iron); p.position.set(px, H / 2, 0.1); }
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

// ================= PHỐ RẼ (hệ cục bộ MẶT CUỐI PHỐ): sau góc nam, đi về −z rồi CONG TRÁI (về −x cục bộ = +z thế giới), DỐC XUỐNG =================
// Tâm đường bắt đầu ở (xL − W/2, 0); tâm cung C = (xL − W/2 − R, 0). Mặt phố (dải cong) hạ theo chiều dài cung (slope); nhà hai bên hạ theo.
export function buildLane(parent, kit, l = {}) {
  const { xL = -END.cornerZ, W = END.laneW, R = END.laneR, slope = END.slope, seed = 57 } = l;
  const g = new THREE.Group(); g.name = 'lane'; parent.add(g);
  const C = new THREE.Vector2(xL - W / 2 - R, 0);
  const P = (r, a) => new THREE.Vector3(C.x + r * Math.cos(a), 0, C.y - r * Math.sin(a));
  const y = (a) => -slope * R * a;
  { const n = 40, a1 = Math.PI / 2 + 0.9, pos = [], uv = [], idx = [];
    for (let i = 0; i <= n; i++) { const a = a1 * i / n; for (const [k, r] of [[0, R - W / 2 - 1], [1, R + W / 2 + 1.2]]) { const p = P(r, a); pos.push(p.x, y(a) - 0.004, p.z); uv.push(k * (W + 2.2) / END.cobbleTile, R * a / END.cobbleTile); } }
    for (let i = 0; i < n; i++) { const q = 2 * i; idx.push(q, q + 1, q + 2, q + 1, q + 3, q + 2); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); geo.setIndex(idx); geo.computeVertexNormals();
    const m = new THREE.Mesh(geo, lamMat({ color: '#ffffff', map: cobbleTex(13), side: THREE.DoubleSide })); m.receiveShadow = true; g.add(m); }
  const seg = (radius, a0, a1, faceIn, sd) => {
    const step = 6.5 / radius; let k = 0;
    for (let a = a0; a < a1 - 1e-3; a += step, k++) {
      const am = Math.min(a + step / 2, a1), p = P(radius, am);
      const n = new THREE.Vector3(Math.cos(am), 0, -Math.sin(am)).multiplyScalar(faceIn ? -1 : 1);
      const hg = new THREE.Group(); hg.position.set(p.x, y(am), p.z); hg.rotation.y = Math.atan2(n.x, n.z); g.add(hg);
      kit.houses(hg, -3.35, 3.35, 0, 1, sd + k * 7, kit.winKind, kit.FT, kit.matC, kit.emit);
    }
  };
  seg(R + W / 2, 0.55, Math.PI / 2 + 0.9, true, seed);          // bờ ngoài (phía nhà kho), mặt quay vào tâm cung
  seg(R - W / 2, 0.0, Math.PI / 2 + 0.9, false, seed + 300);    // bờ trong, mặt quay ra
  return { group: g, C };
}

// ================= HẬU CẢNH NHIỀU LỚP (cục bộ, về −z) =================
// Mỗi lớp: một dải nhà (khối + mái hồi + ống khói) gộp một vật thể; vài ô cửa (ấm hiếm, lạnh nhiều hơn vì thành phố đã trắng).
// Giữa hai lớp: sương sáng lạnh sát mặt phố (sprite cộng, KHÔNG chiếu sáng, không lên trời). drop = hạ nền theo khoảng cách (phố dốc xuống).
export function buildFarCity(parent, l = {}) {
  const zs = l.zs || [-34, -58, -92, -145, -230], span = l.span || [120, 160, 220, 300, 420], R = rng(l.seed ?? 907), glowK = l.glow ?? 1, drop = l.drop ?? 0.03;
  const g = new THREE.Group(); g.name = 'farCity'; parent.add(g);
  const cols = ['#3b3a48', '#34344a', '#2d2f46', '#282b44', '#23263f'];
  zs.forEach((z0, li) => {
    const geos = [], wins = [], half = span[li] / 2; let x = -half; const y0 = drop * z0;
    while (x < half) {
      const w = 5 + R() * 8, h = 6 + R() * (li < 2 ? 8 : 12) + (R() < 0.08 ? 10 : 0), d = 8, zz = z0 - R() * 6;
      const b = new THREE.BoxGeometry(w, h + 10, d); b.translate(x + w / 2, y0 + (h - 10) / 2, zz); geos.push(b);
      const rh = 1.5 + R() * 2.5, rs = new THREE.Shape(); rs.moveTo(-w / 2, 0); rs.lineTo(w / 2, 0); rs.lineTo(0, rh); rs.lineTo(-w / 2, 0);
      if (R() < 0.6) { const rg = new THREE.ExtrudeGeometry(rs, { depth: d, bevelEnabled: false }); rg.translate(x + w / 2, y0 + h, zz - d / 2); geos.push(rg); }
      else { const rg = new THREE.ExtrudeGeometry(rs, { depth: w, bevelEnabled: false }); rg.rotateY(Math.PI / 2); rg.translate(x, y0 + h, zz); geos.push(rg); }
      for (let c = 0, nc = R() < 0.8 ? 1 + (R() * 2 | 0) : 0; c < nc; c++) { const cg = new THREE.BoxGeometry(0.6, 1.6 + R(), 0.6); cg.translate(x + w * (0.2 + 0.6 * R()), y0 + h + rh * 0.6 + 0.6, zz + (R() - 0.5) * 3); geos.push(cg); }
      if (li < 4) for (let k = 0, nw = (w / 2.5) | 0; k < nw; k++) for (let fy = 2.2; fy < h - 1; fy += 2.6) { const q = R(); if (q < 0.1) wins.push([x + 1.2 + k * 2.5, y0 + fy, zz + d / 2 + 0.05, q < 0.025 ? 'gold' : 'cold']); }
      if (li === 1 && R() < 0.12) { const sp = new THREE.CylinderGeometry(0.0, 1.4, 9, 6); sp.translate(x + w / 2, y0 + h + 4.5, zz); geos.push(sp); }   // chóp tháp thỉnh thoảng (không biểu tượng, không chữ)
      x += w + (R() < 0.25 ? 2 + R() * 6 : 0);
    }
    const m = new THREE.Mesh(merge(geos), lamMat({ color: cols[li] })); g.add(m);
    if (wins.length) { const wg = []; for (const [wx, wy, wz, k] of wins) { const q = new THREE.PlaneGeometry(0.8, 1.1); q.translate(wx, wy, wz); wg.push([q, k]); }
      for (const kind of ['gold', 'cold']) { const list = wg.filter((v) => v[1] === kind).map((v) => v[0]); if (!list.length) continue;
        g.add(new THREE.Mesh(merge(list), new THREE.MeshBasicMaterial({ color: new THREE.Color(kind === 'gold' ? '#ffb45c' : '#dfe6f4').multiplyScalar(kind === 'gold' ? 1.3 : 0.7), fog: true }))); } }
    if (glowK > 0) for (let k = 0; k < 7; k++) { const s = glowSprite('#cdd6ee', 0.05 * glowK * (1 + li * 0.35), 30 + li * 14); s.position.set(-half + (k + 0.5) * span[li] / 7 + (R() - 0.5) * 8, y0 + 2 + li * 1.2, z0 - 10 - li * 6); s.scale.y *= 0.4; g.add(s); }
  });
  return { group: g };
}

// ================= CUỐI PHỐ TRONG HỆ TƯỜNG CHIM (dùng chung: bộ phố dời nhóm; bộ tường chim đặt nhóm ở gốc) =================
export function buildEndWallFrame(W, kit, o = {}) {
  const e = END, fx = e.FACE_X - e.OFF_X, fz = -e.FLANK_Z;   // mặt cuối phố trong hệ tường: x_w = −15,2; góc trong z_w = 0
  const faceMat = o.faceMat || lamMat({ color: '#ffffff', map: limewashTex(41, { metres: 6, grime: true, brick: 0.06 }) });
  // (1) HÔNG NAM = tường chim + hốc cửa (hệ tường: z_w = 0), từ góc trong (x_w −15,2) tới đầu hồi căn đầu dãy bắc (x_w 1,8)
  const flank = buildWarehouse(W, kit, { xL: fx, xR: e.houseX0N - e.OFF_X, H: e.H, bayX: e.bayWorldX - e.OFF_X, faceMat, side: false });
  // (2) MẶT CUỐI PHỐ (chắn cuối phố, nhìn +x thế giới), góc nam ở z = cornerZ; không hốc cửa (hốc ở hông); phố rẽ sau góc nam
  const E = new THREE.Group(); E.position.set(fx, 0, fz); E.rotation.y = Math.PI / 2; W.add(E);   // cục bộ x → −z thế giới
  buildWarehouse(E, kit, { xL: -e.cornerZ, xR: -e.FLANK_Z, H: e.H, faceMat, bay: false, seed: 223 });
  buildLane(E, kit, { xL: -e.cornerZ, W: e.laneW, R: e.laneR, slope: e.slope });
  // (3) đầu hồi căn nhà đầu dãy bắc (x = 15), nhìn về −x (về sân trước hông nhà kho)
  { const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(7, 0); sh.lineTo(7, 7.4); sh.lineTo(3.5, 10); sh.lineTo(0, 7.4); sh.lineTo(0, 0);
    const geo = new THREE.ShapeGeometry(sh); planarUV(geo, X, Y, 6, [0.2, 0]); const m = new THREE.Mesh(geo, kit.FT[2]); m.rotation.y = -Math.PI / 2; m.position.set(e.houseX0N - e.OFF_X, 0, -5.6 + fz - 7); m.receiveShadow = true; W.add(m);
    const u = windowUnit(0.82, 1.25, 'dark', kit.matC, kit.emit(1.0), 71); u.rotation.y = -Math.PI / 2; u.position.set(e.houseX0N - e.OFF_X, 4.3, -5.6 + fz - 3.5); W.add(u); }
  // (4) sân trước hông: đá lát (x −5 … 12, z −8,1 … −5,6)
  { const fg = new THREE.PlaneGeometry(e.houseX0N - e.FACE_X, 2.5 + 0.2); fg.rotateX(-Math.PI / 2); fg.translate((fx + e.houseX0N - e.OFF_X) / 2, 0.004, 1.25); planarUV(fg, X, Z, END.cobbleTile, [0, 0]);
    const m = new THREE.Mesh(fg, lamMat({ color: '#ffffff', map: cobbleTex(9) })); m.receiveShadow = true; W.add(m); }
  // (4b) B1: cột điện phố chính trong sân (hệ tường chim), tắt mặc định; post.set(e) bật (0…1) — bóng đèn, loá, PointLight tầm ngắn.
  let post = null;
  if (o.post !== false) {
    const wp = e.wallPost, px = wp.x - e.OFF_X, pz = wp.z - e.FLANK_Z;
    const bulbM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9aa0b4').multiplyScalar(0.3) });
    const Ep = electricLamp(6.2, (c) => lamMat({ color: c }), bulbM); Ep.group.position.set(px, 0, pz); Ep.group.rotation.y = wp.ry; W.add(Ep.group);
    Ep.group.updateMatrixWorld(true); const hp = Ep.head.clone().applyMatrix4(Ep.group.matrixWorld);
    const Lp = new THREE.PointLight(ELEC.color, 0, wp.range, 1.2); Lp.position.copy(hp); W.add(Lp);
    const gl = glowSprite('#dfe8ff', 0, 2.6); gl.position.copy(hp); W.add(gl); const gz = elecGlare(hp); W.add(...gz.list);
    post = { group: Ep.group, light: Lp, head: hp, set: (k) => { Lp.intensity = wp.cd * k; bulbM.color.set('#9aa0b4').multiplyScalar(0.3).lerp(new THREE.Color('#eef3ff').multiplyScalar(9), k); gl.material.color.set('#dfe8ff').multiplyScalar(0.55 * k); gz.set(k); } };
  }
  // (5) hậu cảnh: sau nhà kho (bắc + tây) và cuối phố rẽ (nam, dốc xuống)
  if (o.far !== false) {
    const B = new THREE.Group(); B.position.set(fx, 0, 0); B.rotation.y = Math.PI / 4; W.add(B); buildFarCity(B, { glow: o.fogGlow ?? 1 });   // sau góc nhà kho (tây-bắc)
    const L = new THREE.Group(); L.rotation.y = Math.PI / 2; L.position.set(0, 0, 0); E.add(L); L.position.set(e.cornerZ - 10, 0, 0);
    buildFarCity(L, { zs: [-40, -75, -130], span: [90, 140, 220], seed: 911, glow: o.fogGlow ?? 1, drop: 0.06 });   // cuối phố rẽ
  }
  return { flank, post };
}

// ================= BỘ PHỐ: gắn cuối phố vào buildStreetSet (sets.js gọi, trước khi dựng hai dãy nhà) =================
export function buildStreetEnd(scene, o) {
  const kit = { matC: o.matC, FT: o.FT, winKind: o.winKind, emit: o.emit, houses: o.houses };
  const W = new THREE.Group(); W.position.set(END.OFF_X, 0, END.FLANK_Z); scene.add(W);
  const r = buildEndWallFrame(W, kit, { far: o.endOpts?.far, fogGlow: o.endOpts?.fogGlow });
  W.updateMatrixWorld(true);
  const toWorld = (v) => v.clone().applyMatrix4(W.matrixWorld);
  const wallPost = { x: END.wallPost.x, z: END.wallPost.z, range: END.wallPost.range, ry: END.wallPost.ry, set: r.post ? r.post.set : () => {}, group: r.post?.group, light: r.post?.light };
  return { group: W, warehouse: r.flank, faceX: END.FACE_X, flankZ: END.FLANK_Z, houseX0N: END.houseX0N, houseX0S: END.houseX0S, casSpot: END.casSpot.slice(), wallPost,
    bayWorld: { x: END.bayWorldX, z: END.FLANK_Z }, cornerWorld: { x: END.FACE_X, z: END.cornerZ }, toWorld };
}

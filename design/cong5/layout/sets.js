// Cine Lab · Cổng 5 LAYOUT (tách từ Cổng 4) — BỘ PHỐ OSTLER: GÓI W1 giữ file này (trừ sets_end.js của W2).
// (gốc) Cổng 4 — ANIMATIC (previs). Bộ dựng cảnh bằng tài sản 3D đã khoá ở Cổng 3.
// Không tạo thiết kế mới: cột đèn khí (shared/props.js), cột điện, mặt tiền, cửa sổ, đá lát, trời vẽ (v2/street.js), thang, đèn lồng (shared/cast.js).
// Phần previs thêm (ghi rõ trong SHOTLIST.md): bố cục phố thẳng phẳng (bản khoá là phố cong, dốc nhẹ ở s1), cột đồng hồ quảng trường chép từ s1,
// đồng hồ bỏ túi dựng theo kích thước model sheet (props.watch) — chưa có trang đạo cụ.
//
// Hệ toạ độ bộ phố: trục phố dọc x. Nhà kho (cuối phố, xuống dốc) ở −x; quảng trường + đồng hồ ở +x.
// Đèn khí ở mép bó vỉa bắc (z = −3,9); cột điện mép nam (z = +3,9), vị trí theo s1 (giữa cặp đèn 1–2, 3–4, 5–6, 7–8, 9–10 và cạnh nhà kho).
// Máy quay đặt phía nam (z > 0) nhìn về bắc → +x là PHẢI màn hình. Ida đi từ phải sang trái (về nhà kho) suốt cảnh 1–3.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { buildGasLamp } from '/cong3/shared/props.js';
import { buildLadder } from '/cong3/shared/cast.js';
import { cobbleTex, groundPlane, facadeTex, wallUV, windowUnit, electricLamp, paintedSky } from '/cong3/v2/street.js';
import { limewashTex, flagTex, glowSprite, rng } from '/cong3/dir-C/common.js';
import { buildStreetEnd } from './sets_end.js';

export const GRADE_WARM = { gCanvas: 0.012, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.975, 0.93] };
export const GRADE_COLD = { gCanvas: 0.012, gVig: 0.24, gLift: 0.02, gSat: 0.95, gShadowTint: [0.30, 0.32, 0.90], gHiTint: [0.98, 0.995, 1.03] };
export const GAS = { color: '#ffae5c', cd: 9.0 };
export const ELEC = { color: '#e3eaff', cd: 60.0 };
export const lamMat = (o) => new THREE.MeshLambertMaterial(o);
export const LAMP_X = (i) => 8 + (11 - i) * 14;           // đèn khí số i (1…11): 1 gần quảng trường (x = 148), 11 cạnh nhà kho (x = 8)
export const LAMP_Z = -3.9, POST_Z = 3.9, WALK_Z = -2.3;
export const POST_IDX = [0.5, 2.5, 4.5, 6.5, 8.5, 9.8];    // như s1 (chỉ số đèn tính từ 0)
export const POST_X = POST_IDX.map((s) => 8 + (10 - s) * 14);
export const CLOCK = { x: 176, z: 0.5, h: 6.6 };
// Mốc bật cột tường chim (giây phim) — shots_w1.js gán = common.WALL_POST_ON khi nạp (tránh vòng import sets ↔ common). null = luôn tắt.
export let WALL_POST_T = null;
// (c) Tỷ lệ đá lát theo người (quyết định chủ dự án sau Cổng 5): cobbleTex (Cổng 3, khoá) vẽ viên 0,11–0,17 m × hàng 0,105 m trên 3 m.
// Trải lên nền với COBBLE_M = 2,6 m/lần lặp → viên ngang 0,095–0,147 m (TB 0,121 m ≈ 1/13,7 chiều cao Ida 1,66 m = 6,45 H), hàng 0,091 m.
// Đá phiến vỉa hè: flagTex vẽ tấm 0,45–0,95 m trên 4 m → FLAG_M = 3,0 m → tấm 0,34–0,71 m (hết đọc "cuội to" cạnh người).
// W2: sets_end.js dùng cobbleTex riêng — nên trải theo cùng COBBLE_M để nền cuối phố khớp.
export const COBBLE_M = 2.6, FLAG_M = 3.0;
// B1 (quyết định chủ dự án sau Cổng 5): cột điện phố chính dời vào sân trước hông nhà kho, tầm vũng sáng ~6 m, khuất sau góc nhà khi nhìn từ phố.
// Dùng endInfo.wallPost {x, z, range} nếu sets_end.js (W2) trả về; nếu chưa thì dùng số dự phòng của P.
export const B1_FALLBACK = { wallPost: { x: 15.4, z: -6.2, range: 6 }, casSpot: [14.3, -7.15] };
export const setWallPostOn = (t) => { WALL_POST_T = t; };
const switchOnT = (d) => { if (d < 0) return 0; if (d < 0.08) return 1; if (d < 0.16) return 0; if (d < 0.26) return 1; if (d < 0.34) return 0.05; return Math.min(1, (d - 0.34) / 0.1); };   // = common.switchOn
export const flickAt = (f) => 1 + 0.04 * (0.6 * Math.sin(f * 0.21) + 0.4 * Math.sin(f * 0.083 + 1.3));   // lửa thở ±4 % (luật 2)

export function charMat(role, color, part, extra = {}) {
  if (role === 'flame') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) });
  if (role === 'glass') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb85a').multiplyScalar(4.0), transparent: true, opacity: 0.7, depthWrite: false });
  return new THREE.MeshLambertMaterial({ color: new THREE.Color(color), side: THREE.DoubleSide, ...extra });
}
export const ladderOf = () => buildLadder(1.8, 0.34, 6, (r, c) => lamMat({ color: c }), '#8a6a45');

// Đồng hồ bỏ túi (sheet props.watch): mặt vạch không chữ số, 2 kim; trả group + setHands(phút, giờ theo độ).
export function buildWatch(r = 0.026) {
  const g = new THREE.Group(); g.name = 'watch';
  const brass = lamMat({ color: '#a8844a' }), black = new THREE.MeshBasicMaterial({ color: '#141418' });
  const face = new THREE.Mesh(new THREE.CircleGeometry(r * 0.9, 40), lamMat({ color: '#efe8da' })); face.position.z = 0.0046; g.add(face);   // trước mặt vỏ (vỏ dày 8 mm, tâm 0)
  const cs = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.008, 32).rotateX(Math.PI / 2), brass); g.add(cs);
  const crown = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.14, r * 0.14, r * 0.3, 12), brass); crown.position.y = r * 1.1; g.add(crown);
  const bow = new THREE.Mesh(new THREE.TorusGeometry(r * 0.28, r * 0.05, 6, 16), brass); bow.position.y = r * 1.4; g.add(bow);
  for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2; const b = new THREE.Mesh(new THREE.PlaneGeometry(r * 0.07, r * 0.2), black); b.position.set(Math.sin(a) * r * 0.72, Math.cos(a) * r * 0.72, 0.0049); b.rotation.z = -a; g.add(b); }
  const hand = (len, w) => { const h = new THREE.Mesh(new THREE.PlaneGeometry(w, len).translate(0, len / 2 - len * 0.1, 0), black); h.position.z = 0.0052; g.add(h); return h; };
  const mh = hand(r * 0.78, r * 0.06), hh = hand(r * 0.5, r * 0.09);
  g.userData.setHands = (minDeg, hourDeg) => { mh.rotation.z = -minDeg * Math.PI / 180; hh.rotation.z = -hourDeg * Math.PI / 180; };
  return g;
}

// Cột đồng hồ điện công cộng (luật thế giới mục 1; chép bố cục s1): cột sắt ~6 m, mặt kính mờ Ø1,2 m, 12 vạch đen, 2 kim đen.
export function buildClock() {
  const iron = lamMat({ color: '#2a2a30' }), g = new THREE.Group();
  g.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.26, 6, 16).translate(0, 3, 0), iron), { castShadow: true }));
  g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 0.8, 16).translate(0, 0.4, 0), iron));
  const head = new THREE.Group(); head.position.y = CLOCK.h; g.add(head);
  const faceMat = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9f9bb8').multiplyScalar(0.35) });
  const black = new THREE.MeshBasicMaterial({ color: '#141418' }), hands = [];
  for (const s of [1, -1]) {
    const face = new THREE.Mesh(new THREE.CircleGeometry(0.6, 48), faceMat); face.position.z = s * 0.14; if (s < 0) face.rotation.y = Math.PI; head.add(face);
    for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2; const bar = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.16), black);
      bar.position.set(Math.sin(a) * 0.48 * s, Math.cos(a) * 0.48, s * 0.145); bar.rotation.z = -a * s; if (s < 0) bar.rotation.y = Math.PI; head.add(bar); }
    const hand = (len, w) => { const p = new THREE.Group(); p.position.z = s * 0.15; if (s < 0) p.rotation.y = Math.PI; head.add(p);
      const h = new THREE.Mesh(new THREE.PlaneGeometry(w, len).translate(0, len / 2 - 0.04, 0), black); p.add(h); return h; };
    hands.push([hand(0.52, 0.035), hand(0.34, 0.05)]);
  }
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(0.64, 0.64, 0.28, 48, 1, true).rotateX(Math.PI / 2), iron); head.add(rim);
  const cap = new THREE.Mesh(new THREE.SphereGeometry(0.18, 12, 8), iron); cap.position.y = 0.75; head.add(cap);
  const bell = new THREE.Mesh(new THREE.SphereGeometry(0.16, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), lamMat({ color: '#7a6a4a' })); bell.position.y = 0.95; head.add(bell);
  const glow = glowSprite('#eef2ff', 0.0, 2.6); head.add(glow);
  g.userData = {
    head,
    setHands: (minDeg, hourDeg) => { for (const [m, h] of hands) { m.rotation.z = -minDeg * Math.PI / 180; h.rotation.z = -hourDeg * Math.PI / 180; } },
    setOn: (k) => { faceMat.color.set('#9f9bb8').multiplyScalar(0.35).lerp(new THREE.Color('#f2f4ff').multiplyScalar(2.2), k); glow.material.color.set('#eef2ff').multiplyScalar(0.5 * k); },
  };
  return g;
}

// v2: trời ĐÊM có sao (canvas): đỉnh gần đen xanh, chân trời xanh đậm hửng ánh phố; sao nhỏ — dấu hiệu đêm rõ trong mọi shot sau khi điện bật.
export function nightSky(seed = 23) {
  const R = rng(seed), cv = document.createElement('canvas'); cv.width = 4096; cv.height = 2048; const g = cv.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 2048); gr.addColorStop(0, '#04050c'); gr.addColorStop(0.55, '#0a0f24'); gr.addColorStop(0.85, '#18203f'); gr.addColorStop(1, '#2a3354');
  g.fillStyle = gr; g.fillRect(0, 0, 4096, 2048);
  for (let i = 0; i < 2600; i++) { const y = Math.pow(R(), 1.6) * 1800, x = R() * 4096, r = 0.45 + R() * (R() < 0.05 ? 1.1 : 0.5), a = 0.35 + R() * 0.65 * (1 - y / 2048);   // sao nhỏ (bản đầu to như bông tuyết ở tiêu cự dài)
    g.fillStyle = `rgba(${220 + R() * 35 | 0},${225 + R() * 30 | 0},255,${a.toFixed(2)})`; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.SphereGeometry(400, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2 + 0.15), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide, fog: false, depthWrite: false, color: new THREE.Color(1.6, 1.6, 1.6) }));
}
// Loá đèn điện: quầng lạnh rộng + vệt loá ngang (nguồn điện thấy được, gắt — khác hẳn đèn khí ấm)
export function elecGlare(pos) {
  const core = glowSprite('#f4f7ff', 0, 1.2), halo = glowSprite('#cfdcff', 0, 6.0), streak = glowSprite('#dbe4ff', 0, 1.0);
  streak.scale.set(7.0, 0.22, 1); for (const sp of [core, halo, streak]) { sp.position.copy(pos); }
  return { list: [core, halo, streak], set: (e) => { core.material.color.set('#f4f7ff').multiplyScalar(5.0 * e); halo.material.color.set('#cfdcff').multiplyScalar(0.45 * e); streak.material.color.set('#dbe4ff').multiplyScalar(1.4 * e); } };
}

// Dãy nhà (chép cách dựng của s6.buildStreet: nếp nhà 4–7 m, mặt tiền vữa/gạch vẽ, cửa sổ có khung, cửa gỗ, mái, ống khói).
export function houses(scene, x0, x1, z, face, seed, winKind, FT, matC, emit) {
  const Rh = rng(seed); let x = x0; const ry = face < 0 ? Math.PI : 0;
  const roofM = matC('#2c2834'), doorM = matC('#4a3226'), stepM = matC('#a39b8f');
  const box = (w, h, d, mat, px, py, pz) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(px, py, pz); m.receiveShadow = true; scene.add(m); return m; };
  const wins = [];
  while (x < x1 - 0.5) {
    const w = Math.min(x1 - x, 4 + Rh() * 3), h = 6 + Rh() * 2.5, d = 7, cx = x + w / 2;
    const m = new THREE.Mesh(wallUV(new THREE.PlaneGeometry(w, h), 6, x), FT[Math.floor(Rh() * FT.length)]); m.position.set(cx, h / 2, z); m.rotation.y = ry; m.receiveShadow = true; scene.add(m);
    box(w + 0.02, 0.22, 0.35, matC('#d8d2c6'), cx, h - 0.11, z + face * 0.17);
    const r = new THREE.Mesh(new THREE.CylinderGeometry(0.01, d * 0.72, 2.4 + Rh() * 1.2, 4, 1), roofM); r.rotation.y = Math.PI / 4; r.scale.set(w / d, 1, 1); r.position.set(cx, h + 1.2, z - face * d / 2); scene.add(r);
    if (Rh() < 0.8) box(0.5, 1.5, 0.5, matC('#6a5a52'), x + w * (0.2 + 0.6 * Rh()), h + 1.6, z - face * d * 0.35);
    for (let wx = x + 1.0; wx < x + w - 0.6; wx += 1.9) for (const wy of [2.1, 4.3, 6.4]) {
      if (wy > h - 1.0) continue;
      const kind = winKind(Rh);
      const u = windowUnit(0.82, 1.25, kind, matC, emit(kind === 'gold' ? 1.6 : kind === 'cold' ? 1.1 : 1.0), Math.floor(Rh() * 1e6)); u.position.set(wx, wy, z); u.rotation.y = ry; scene.add(u); wins.push(u);
    }
    if (Rh() < 0.6) { const dx = x + w * 0.5; box(1.0, 2.2, 0.1, doorM, dx, 1.1, z + face * 0.05); box(1.3, 0.15, 0.4, stepM, dx, 0.075, z + face * 0.2); }
    x += w;
  }
  return wins;
}

// ================= CỔNG 5 (W1): CHIỀU SÂU — SƯỜN ĐỒI, LỚP NHÀ SAU, QUẢNG TRƯỜNG, DÃY NHÀ XA =================
// Luật thế giới mục 1: Ostler là phố "dốc nhẹ, cong". Bản code giữ lòng phố thẳng, phẳng trong đoạn diễn (x = 0…160) để KHÔNG phá
// hệ toạ độ chung (LAMP_X, LAMP_Z, POST_X, WALK_Z, ladderAt, vị trí nhân vật của W2). Dốc và cong được đọc qua cái bao quanh phố:
//  • phố men sườn đồi: phía bắc (−z) là sườn lên → nhà lớp sau đứng trên thềm cao dần, mái + ống khói chồng lớp trên mái dãy trước;
//    phía nam (+z) là sườn xuống → lớp sau thấp, chỉ lộ ở xa;
//  • cả sườn lên dần về đầu dốc (+x, quảng trường), cùng độ dốc 3,5 % như s1 (groundY) → đường mái lớp sau dâng dần khi nhìn lên phố;
//  • sau quảng trường, dãy nhà xa xếp bậc lên đồi theo một cung (phố tiếp tục cong về bắc) → nhìn lên phố không còn chân trời phẳng;
//  • sương theo shot (o.fog) cho tele/toàn cảnh: lớp xa nhạt dần theo không khí.
export const SLOPE = 0.035;
export const hillY = (x) => SLOPE * (Math.min(x, 330) - 80);   // cao độ tương đối của sườn theo trục phố (x = 80 ≈ giữa phố)
// Mái hai dốc (lăng trụ tam giác) dài L theo x cục bộ, sâu D theo z, cao h; đáy y = 0 (chép cách dựng mái của s1.roofGeo, bỏ mái chóp).
function gableGeo(L, D, h, over = 0.25) {
  const hx = L / 2 + over, hz = D / 2 + over;
  const v = [-hx, 0, hz, hx, 0, hz, hx, h, 0, -hx, 0, hz, hx, h, 0, -hx, h, 0, hx, 0, -hz, -hx, 0, -hz, -hx, h, 0, hx, 0, -hz, -hx, h, 0, hx, h, 0,
    -L / 2, 0, -D / 2, -L / 2, 0, D / 2, -L / 2, h, 0, L / 2, 0, D / 2, L / 2, 0, -D / 2, L / 2, h, 0];
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(v), 3)); g.computeVertexNormals(); return g;
}
// Một dãy khối nhà lớp sau dọc trục cục bộ x (a0 → a1), mặt tiền nhìn ra +z cục bộ; đặt vào `parent` (Group có thể xoay/dời).
// base(a) = cao độ nền tại toạ độ a (m); bend(a) = lệch z theo a (tạo cung). Khối kéo dài xuống 12 m dưới nền (che khe hở sườn).
function massRow(parent, { a0, a1, z = 0, base = () => 0, bend = () => 0, seed = 1, hMin = 7, hMax = 10.5, d = 7, lit = 0.08, mats }) {
  const R = rng(seed); let a = a0;
  while (a < a1 - 0.5) {
    const w = Math.min(a1 - a, 4 + R() * 3.5), h = hMin + R() * (hMax - hMin), ca = a + w / 2, b = base(ca), zc = z + bend(ca), rot = Math.atan(-(bend(ca + 0.5) - bend(ca - 0.5)));
    const g = new THREE.Group(); g.position.set(ca, b, zc); g.rotation.y = rot; parent.add(g);
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h + 12, d), mats.wall[Math.floor(R() * mats.wall.length)]); body.position.set(0, (h - 12) / 2, -d / 2); g.add(body);
    const rh = 2.2 + R() * 1.6, roof = new THREE.Mesh(gableGeo(w, d, rh), mats.roof[Math.floor(R() * mats.roof.length)]); roof.position.set(0, h, -d / 2); g.add(roof);
    const nc = R() < 0.35 ? 2 : 1; for (let k = 0; k < nc; k++) { const ch = new THREE.Mesh(new THREE.BoxGeometry(0.55, 1.4 + R() * 0.9, 0.55), mats.chim); ch.position.set((R() - 0.5) * w * 0.7, h + rh * 0.55 + 0.5, -d * (0.25 + 0.5 * R())); g.add(ch);
      if (R() < 0.5) { const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 0.45, 6), mats.pot); pot.position.set(ch.position.x + 0.1, ch.position.y + ch.geometry.parameters.height / 2 + 0.2, ch.position.z); g.add(pot); } }
    for (let wy = 2.2; wy < h - 0.8; wy += 2.2) for (let wx = -w / 2 + 1.0; wx < w / 2 - 0.6; wx += 1.9) {   // ô cửa: tối (khung tối trên tường) hoặc vàng
      const on = R() < lit, win = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 1.2), on ? mats.winLit : mats.winDark); win.position.set(wx, wy, 0.02); g.add(win); }
    a += w;
  }
}
function depthMats(night) {
  const L = (c) => new THREE.MeshLambertMaterial({ color: c });
  return { wall: (night ? ['#8f8a86', '#9c958c', '#86807c', '#a39a8e'] : ['#b9ada4', '#c4b7a8', '#a99d98', '#c9bcaa']).map(L), roof: ['#2c2834', '#35303c', '#3b2f2e'].map(L),
    chim: L('#6a5a52'), pot: L('#8a5a44'), winDark: L('#34343f'), winLit: new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb35a').multiplyScalar(night ? 1.3 : 1.1) }) };
}
// Lớp sau hai bên phố + quảng trường có nhà bao + dãy nhà xa lên đồi sau quảng trường. xa, xb: đoạn phố đang dựng.
function buildDepth(scene, o, xa, xb, matC, FT, winKind, emit) {
  const night = o.sky !== 'dusk', M = depthMats(night), lo = Math.max(xa - 20, -4), hi = Math.min(xb + 20, 164);
  const depth = new THREE.Group(); depth.name = 'depth'; scene.add(depth);
  if (hi > lo) {
    massRow(depth, { a0: lo, a1: hi, z: -13.6, base: (x) => 2.6 + hillY(x), seed: 501, hMin: 7, hMax: 10, lit: night ? 0.07 : 0.12, mats: M });    // bắc, thềm 1
    massRow(depth, { a0: lo - 6, a1: hi + 6, z: -23.5, base: (x) => 6.4 + hillY(x), seed: 502, hMin: 7.5, hMax: 11, lit: night ? 0.06 : 0.1, mats: M });   // bắc, thềm 2
    massRow(depth, { a0: lo - 10, a1: hi + 10, z: -34, base: (x) => 10.5 + hillY(x), seed: 503, hMin: 8, hMax: 12, lit: 0.05, mats: M });   // bắc, thềm 3 (đỉnh đồi)
    const south = new THREE.Group(); south.rotation.y = Math.PI; depth.add(south);   // nam: mặt tiền nhìn về −z (về phố); a → −x sau khi xoay
    massRow(south, { a0: -hi, a1: -lo, z: -13.6, base: (a) => -2.2 + hillY(-a), seed: 504, hMin: 7, hMax: 9.5, lit: night ? 0.07 : 0.12, mats: M });
  }
  if (xb > 150) {
    // quảng trường (x 162…202, z ±20): nhà bao ba phía, mặt tiền chi tiết như phố (houses)
    houses(scene, 162, 202, -20, 1, 85, winKind, FT, matC, emit); houses(scene, 162, 202, 20, -1, 87, winKind, FT, matC, emit);
    const east = new THREE.Group(); east.position.set(202, 0, 0); east.rotation.y = -Math.PI / 2; scene.add(east); houses(east, -20, 20, 0, 1, 89, winKind, FT, matC, emit);
    for (const [s, a, b] of [[1, -20, -5.6], [-1, 5.6, 20]]) { const g = new THREE.Group(); g.position.set(162, 0, 0); g.rotation.y = Math.PI / 2; scene.add(g); houses(g, a, b, 0, 1, 90 + s, winKind, FT, matC, emit); }
    const flag = lamMat({ color: '#ffffff', map: flagTex(13, { metres: 4 }) });   // vỉa hè quanh quảng trường
    scene.add(groundPlane(40, 3.0, flag, FLAG_M, { cx: 182, cz: -18.5, y: 0.1 }), groundPlane(40, 3.0, flag, FLAG_M, { cx: 182, cz: 18.5, y: 0.1 }));
    // dãy nhà xa sau quảng trường: bậc lên đồi, xếp theo cung (phố cong tiếp về bắc) — các dãy dọc trục z, mặt nhìn về −x (về phố)
    // xoay −90°: cục bộ (a, z) → thế giới (x = −z, z = a); mặt tiền (+z cục bộ) nhìn về −x. Bắc (a < 0) cao hơn nam: sườn đồi.
    const far = new THREE.Group(); far.rotation.y = -Math.PI / 2; depth.add(far);
    [[214, 0.5, 511], [230, 3.0, 512], [250, 6.0, 513], [276, 9.5, 514], [310, 13.5, 515]].forEach(([X, up, sd], k) =>
      massRow(far, { a0: -80 - 14 * k, a1: 60 + 10 * k, z: -X, base: (a) => hillY(X) + up - 0.05 * a, bend: (a) => -(0.0025 * a * a + 0.04 * a), seed: sd, hMin: 8, hMax: 11 + k, lit: (night ? 0.05 : 0.09) * (o.farLit ?? 1), mats: M }));   // o.farLit: s08 tele = 0 (cửa sáng còn thấy khi khối nhà đã chìm vào sương → "ô cửa lơ lửng giữa trời")
  }
  return depth;
}

// ================= BỘ PHỐ OSTLER =================
// o.sky: 'dusk' | 'night'; o.x0/x1: đoạn phố dựng (tiết kiệm); o.shadowLamps: chỉ số đèn khí có bóng (1–2 ngọn gần hành động);
// o.shadowPosts: [] (đèn điện KHÔNG bóng — luật 2). Trả { scene, lamps[], posts[], clock, setState(stateFn, f) }.
// Cổng 5 (W1): o.fog = [gần, xa] (m) — sương theo shot (tele/toàn cảnh cần xa hơn để lớp nhà xa còn đọc được); o.depth === false → bỏ lớp sau.
export function buildStreetSet(o = {}) {
  const scene = new THREE.Scene(), R = rng(401);
  const x0 = o.x0 ?? -12, x1 = o.x1 ?? 190;
  const sky = o.sky !== 'dusk' ? nightSky() : paintedSky(o.sky === 'dusk' ? [[0, '#1d2150'], [0.55, '#3c3566'], [0.85, '#7a5a80'], [1, '#b07a8a']] : [[0, '#0e1230'], [0.55, '#1f2548'], [0.85, '#3a3f66'], [1, '#5a5f86']], { seed: 17, haze: '#b8a8c4', hazeA: 0.3 });
  scene.add(sky);
  const [fogN, fogF] = o.fog || [25, 140];
  scene.fog = new THREE.Fog(o.sky === 'dusk' ? '#4a4068' : '#0c1024', fogN, fogF);   // v2: sương đêm tối (xa là tối, không phải trắng như ban ngày)
  const hemi = new THREE.HemisphereLight(o.sky === 'dusk' ? '#5c5aa8' : '#2c3260', '#120e18', o.sky === 'dusk' ? 0.35 : 0.16); scene.add(hemi);
  const whiteHemi = new THREE.HemisphereLight('#dfe6ff', '#8a8e9c', 0.0); scene.add(whiteHemi);   // ánh điện tràn phẳng (tăng theo số khối đã bật quanh máy)
  const matC = (c) => lamMat({ color: c });
  const emit = (k) => (tex) => new THREE.MeshBasicMaterial({ map: tex, color: new THREE.Color('#ffffff').multiplyScalar(k), fog: true });
  const FT = [0, 1, 2, 3].map((k) => lamMat({ color: '#ffffff', map: facadeTex(91 + k * 13, { metres: 6, base: ['#e7e2d6', '#e0dacd', '#e9e4da', '#dcd6ca'][k], courseAt: [3.2, 6.1] }) }));
  // nền: đá lát lòng phố + vỉa hè đá phiến + bó vỉa
  const cobT = cobbleTex(9), flagT = flagTex(9, { metres: 4 });
  // (c) o.groundSoft = px: nền nhoè thay DOF cho INSERT tiêu cự dài (s06, s09w). 100 mm lấy nét 0,32 m → nền cách 1–2 m có vòng nhoè ≈ 1/3 khung
  // (quang học thật); previs không có DOF nên viên đá sắc nét đọc thành "chấm bi". Lấy mẫu kết cấu xuống px/lần lặp. Cổng 7 thay bằng DOF thật.
  const soft = (t, px) => { const cv = document.createElement('canvas'); cv.width = cv.height = px; cv.getContext('2d').drawImage(t.image, 0, 0, px, px);
    const n = new THREE.CanvasTexture(cv); n.colorSpace = THREE.SRGBColorSpace; n.wrapS = n.wrapT = THREE.RepeatWrapping; return n; };
  const cob = lamMat({ color: '#ffffff', map: o.groundSoft ? soft(cobT, o.groundSoft) : cobT }), flag = lamMat({ color: '#ffffff', map: o.groundSoft ? soft(flagT, o.groundSoft) : flagT });   // (c): trải theo COBBLE_M, FLAG_M
  const L = x1 - x0, cx = (x0 + x1) / 2;
  scene.add(groundPlane(L, 7.2, cob, COBBLE_M, { cx, cz: 0 }));
  for (const s of [-1, 1]) { scene.add(groundPlane(L, 2.0, flag, FLAG_M, { cx, cz: s * 4.6, y: 0.12 }));
    const kerb = new THREE.Mesh(new THREE.BoxGeometry(L, 0.14, 0.2), matC('#9d968c')); kerb.position.set(cx, 0.06, s * 3.65); kerb.receiveShadow = true; scene.add(kerb); }
  // quảng trường (+x): khoảng đá lát rộng
  if (x1 > 150) scene.add(groundPlane(44, 40, cob, COBBLE_M, { cx: 182, cz: 0, y: 0.005 }));   // W1: cổng 150 (trước 165) — mọi shot nhìn tới đầu phố đều thấy quảng trường
  // nhà hai bên; cửa sổ: chạng vạng → vài ô vàng; đêm → phần lớn tối, vài ô vàng
  const winKind = (Rh) => (Rh() < (o.sky === 'dusk' ? 0.16 : 0.07) ? 'gold' : 'dark');   // v2: đêm — phần lớn cửa sổ tối
  // nhà kho cuối phố: tường vôi trắng chắn ngang (−x)
  // Cổng 5 (V3): phần CUỐI PHỐ (nhà kho, phố cong, ngã rẽ, dãy nhà xa, sương) nằm ở sets_end.js — GÓI W2 giữ. W1 chỉ gọi, không sửa.
  // W1: gọi TRƯỚC khi dựng hai dãy nhà để sets_end.js có thể báo nơi dãy nhà phố chính dừng (endInfo.houseX0 / houseX0N / houseX0S, mặc định −4)
  // và vị trí Cas (endInfo.casSpot = [x, z]) cho s24, s24c.
  const endInfo = x0 < 0 ? buildStreetEnd(scene, { ...o, x0, x1, matC, FT, winKind, emit, houses }) : null;
  const hN = Math.max(x0, endInfo?.houseX0N ?? endInfo?.houseX0 ?? -4), hS = Math.max(x0, endInfo?.houseX0S ?? endInfo?.houseX0 ?? -4);
  houses(scene, hN, Math.min(x1, 162), -5.6, 1, 81, winKind, FT, matC, emit);
  houses(scene, hS, Math.min(x1, 162), 5.6, -1, 83, winKind, FT, matC, emit);
  const depth = o.depth === false ? null : buildDepth(scene, o, Math.max(x0, Math.min(hN, hS)), x1, matC, FT, winKind, emit);   // Cổng 5 (W1): lớp sau, quảng trường, dãy nhà xa
  // đèn khí 11 ngọn (props.js), lồng kính quay mặt kính về lòng phố
  const glassOn = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc070').multiplyScalar(2.6), transparent: true, opacity: 0.55, depthWrite: false, side: THREE.DoubleSide });
  const lamps = [];
  for (let i = 1; i <= 11; i++) {
    const x = LAMP_X(i); if (x < x0 - 2 || x > x1 + 2) { lamps.push(null); continue; }
    const glassM = glassOn.clone(), flameM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(30) });
    const lamp = buildGasLamp({ height: 3.4, mat: (role, c) => role === 'flame' ? flameM : role === 'glass' ? glassM : lamMat({ color: c }) });
    lamp.position.set(x, 0.12, LAMP_Z); lamp.rotation.y = Math.PI / 4; scene.add(lamp); lamp.updateMatrixWorld(true);
    const fp = new THREE.Vector3(); lamp.userData.flame.getWorldPosition(fp);
    const Lt = new THREE.PointLight(GAS.color, 0, 0, 2); Lt.position.copy(fp);
    if ((o.shadowLamps || []).includes(i)) { Lt.castShadow = true; Lt.shadow.mapSize.set(512, 512); Lt.shadow.bias = -0.0006; Lt.shadow.normalBias = 0.02; Lt.shadow.camera.near = 0.08; }
    scene.add(Lt);
    const gc = glowSprite('#ffc57a', 1.6, 0.6), gw = glowSprite('#ff9a4a', 0.22, 3.2); gc.position.copy(fp); gw.position.copy(fp); scene.add(gc, gw);
    lamp.traverse((m) => { if (m.isMesh) { m.castShadow = m.castShadow && m.material.type !== 'MeshBasicMaterial'; m.receiveShadow = true; } });
    lamps.push({ i, lamp, L: Lt, fp, glassM, flameM, gc, gw, x });
  }
  // cột điện (street.js) mép nam, tay vươn ra lòng phố
  const posts = [];
  POST_X.forEach((x, k) => {
    if (x < x0 - 2 || x > x1 + 2) { posts.push(null); return; }
    const bulbM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9aa0b4').multiplyScalar(0.3) });
    const E = electricLamp(6.2, matC, bulbM); E.group.position.set(x, 0.12, POST_Z); E.group.rotation.y = Math.PI / 2; scene.add(E.group);
    E.group.updateMatrixWorld(true); const hp = E.head.clone().applyMatrix4(E.group.matrixWorld);
    const Lt = new THREE.PointLight(ELEC.color, 0, o.sky === 'dusk' ? 34 : 20, o.sky === 'dusk' ? 1.2 : 1.4); Lt.position.copy(hp); scene.add(Lt);   // v2 đêm: vũng sáng có tầm (≈ 20 m) → góc ngọn 11 còn tối khi phố chính đã trắng   // không bóng (luật 2)
    const gl = glowSprite('#dfe8ff', 0.0, 2.6); gl.position.copy(hp); scene.add(gl); const gz = elecGlare(hp); scene.add(...gz.list);
    posts.push({ k, x, E, L: Lt, bulbM, gl, hp, gz });
  });
  // cột điện ở quảng trường (bật cùng đồng hồ)
  // Q-W2-3 (P): cột điện PHỐ CHÍNH cạnh góc nhà kho = cột bật lúc 1:04 (WALL_POST_ON) của bộ tường chim (sets2.WALL.post, hệ tường (3,3; 3,9)
  // → thế giới (13,5; −4,2), xoay π/2 + 0,35). Không thuộc POST_X (POST_X giữ nguyên). Chỉ dựng khi đoạn phố có cuối phố (endInfo).
  // B1 (sau Cổng 5): cột dời vào sân trước hông nhà kho (endInfo.wallPost hoặc B1_FALLBACK), tầm sáng = range (~6 m) → góc L11 (cách ~8 m) ngoài vũng.
  // PointLight bật theo cột (tầm ngắn, không đổ bóng, không vào trắng tràn toàn cục); o.wallPostLight === false để tắt ánh (giữ bóng đèn + loá).
  let wallPost = null;
  if (endInfo) {
    const W = endInfo.wallPost || B1_FALLBACK.wallPost;
    const bulbM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9aa0b4').multiplyScalar(0.3) });
    const E = electricLamp(6.2, matC, bulbM);
    E.group.position.set(W.x, 0.12, W.z); E.group.rotation.y = Math.PI / 2 + 0.35; scene.add(E.group);   // tay vươn về tường chim (−z), hơi về phía Cas (−x)
    E.group.updateMatrixWorld(true); const hp = E.head.clone().applyMatrix4(E.group.matrixWorld);
    const Lt = new THREE.PointLight(ELEC.color, 0, W.range ?? 6, 1.2); Lt.position.copy(hp); scene.add(Lt);
    const gl = glowSprite('#dfe8ff', 0.0, 2.6); gl.position.copy(hp); scene.add(gl); const gz = elecGlare(hp); scene.add(...gz.list);
    wallPost = { E, L: Lt, bulbM, gl, gz, hp, x: W.x, z: W.z, range: W.range ?? 6, fromEnd: !!endInfo.wallPost };
  }
  const squarePosts = [];
  if (x1 > 150) for (const [px, pz] of [[166, 8], [166, -8], [188, 9], [188, -9]]) {
    const bulbM = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9aa0b4').multiplyScalar(0.3) });
    const E = electricLamp(6.2, matC, bulbM); E.group.position.set(px, 0, pz); E.group.rotation.y = pz > 0 ? Math.PI / 2 : -Math.PI / 2; scene.add(E.group);
    E.group.updateMatrixWorld(true); const hp = E.head.clone().applyMatrix4(E.group.matrixWorld);
    const Lt = new THREE.PointLight(ELEC.color, 0, o.sky === 'dusk' ? 34 : 20, o.sky === 'dusk' ? 1.2 : 1.4); Lt.position.copy(hp); scene.add(Lt);   // v2 đêm: vũng sáng có tầm (≈ 20 m) → góc ngọn 11 còn tối khi phố chính đã trắng
    const gl = glowSprite('#dfe8ff', 0.0, 2.6); gl.position.copy(hp); scene.add(gl); const gz = elecGlare(hp); scene.add(...gz.list);
    squarePosts.push({ E, L: Lt, bulbM, gl, gz, hp });
  }
  let clock = null;
  if (x1 > 150) { clock = buildClock(); clock.position.set(CLOCK.x, 0, CLOCK.z); clock.rotation.y = -Math.PI / 2; scene.add(clock); clock.userData.setHands(0, 0); }
  // Vệt tối tiếp xúc dưới chân (luật 2: dưới ánh điện chỉ còn vệt mờ dưới chân) — gắn theo nhân vật trong film.js.
  // Trạng thái sáng theo khung: st = { gas: i → mức 0…1 (0 tắt, 1 sáng, 0,35 nhạt), post: k → 0…1, square: 0…1, flick: f }
  function setState(st, f) {
    const fl = flickAt(f);
    for (const l of lamps) { if (!l) continue; const g = st.gas(l.i) ?? 0;
      l.L.intensity = GAS.cd * g * fl * (st.gasLight ? st.gasLight(l.i) : 1); l.flameM.color.set('#fff2d0').multiplyScalar(g > 0.01 ? 30 * g : 0.02);
      if (g > 0.01) l.glassM.color.set('#ffc070').multiplyScalar(0.3 + 2.3 * g); else l.glassM.color.set('#7c809a').multiplyScalar(0.12); l.glassM.opacity = g > 0.01 ? 0.55 : 0.5;
      l.gc.material.color.set('#ffc57a').multiplyScalar(1.6 * g); l.gw.material.color.set('#ff9a4a').multiplyScalar(0.22 * g); }
    let white = 0;
    for (const p of posts) { if (!p) continue; const e = st.post(p.k) ?? 0;
      p.L.intensity = ELEC.cd * e; p.bulbM.color.set('#9aa0b4').multiplyScalar(0.3).lerp(new THREE.Color('#eef3ff').multiplyScalar(9), e); p.gl.material.color.set('#dfe8ff').multiplyScalar(0.55 * e); p.gz.set(e); white = Math.max(white, e * (st.nearPost ? st.nearPost(p) : 1)); }
    if (wallPost) { const e = st.wallPost !== undefined ? st.wallPost : (WALL_POST_T === null || f === undefined ? 0 : switchOnT(f / 24 - WALL_POST_T));
      wallPost.L.intensity = o.wallPostLight === false ? 0 : ELEC.cd * e; wallPost.bulbM.color.set('#9aa0b4').multiplyScalar(0.3).lerp(new THREE.Color('#eef3ff').multiplyScalar(9), e);
      wallPost.gl.material.color.set('#dfe8ff').multiplyScalar(0.55 * e); wallPost.gz.set(e); }
    const sq = st.square ?? 0;
    for (const p of squarePosts) { p.L.intensity = ELEC.cd * sq; p.bulbM.color.set('#9aa0b4').multiplyScalar(0.3).lerp(new THREE.Color('#eef3ff').multiplyScalar(9), sq); p.gl.material.color.set('#dfe8ff').multiplyScalar(0.55 * sq); p.gz.set(sq); }
    if (clock) clock.userData.setOn(st.clock ?? 0);
    whiteHemi.intensity = (st.whiteFill ?? white) * 0.9;   // trắng tràn phẳng (mức v1). v2 thử 0,32 ban đêm → ở 0:40–0:42 bóng dài của đèn khí L7 còn nguyên, trái kịch bản; trả về 0,9. Dấu hiệu đêm nay do trời sao + sương tối
  }
  return { scene, lamps, posts, squarePosts, clock, setState, hemi, whiteHemi, endInfo, depth, wallPost };
}

// Vệt tối tiếp xúc (decal mờ dưới chân) — dùng cho mọi bộ ngoài phố.
export function contactBlob(r = 0.45, a = 0.55) {
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const g = cv.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, `rgba(0,0,0,${a})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(cv);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(r * 2, r * 2), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, color: '#000000', fog: false }));
  m.rotation.x = -Math.PI / 2; m.renderOrder = 2; return m;
}

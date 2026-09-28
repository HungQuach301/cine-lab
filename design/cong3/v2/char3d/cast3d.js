// Cine Lab · Cổng 3 v2 · CÁCH (1) — NHÂN VẬT 3D NÂNG CẤP (hướng C "Painted Glow").
// Cùng API với shared/cast.js: buildCharacter(sheet, opts) → { root, joints, props, hands, parts, H, sheet, setPose }.
// Cách làm:
//  • Dùng NGUYÊN khung xương, applyPose, đạo cụ của shared/cast.js (import, gọi, rồi gỡ toàn bộ hình khối cũ).
//  • Hình khối mới điêu khắc bằng SDF (sdf.js): đầu, thân, ủng, mũ, tóc, bàn tay… là lưới liền, pháp tuyến từ gradient.
//  • Tay áo, chân, váy: ống liền da CPU (LBS) qua khuỷu/gối/hông → không còn trụ + bi ghép; tính lại mỗi setPose.
//    Mỗi đoạn đo C3 là một mesh riêng nằm đúng giữa hai tâm khớp (upper_arm, forearm, thigh, shin), mép chung ở khớp.
//  • Bề mặt: màu gốc model sheet × map loang nét cọ × màu đỉnh (AO lấy từ SDF, má ấm, hốc mắt lạnh) + normalMap sợi/len;
//    mọi vật liệu qua opts.material(role, color, part, extra) → cảnh quyết định ánh sáng (Lambert, không bóng nhựa).
//  • Bàn tay: lòng bàn tay điêu khắc + 4 ngón × 3 đốt + ngón cái 2 đốt; gập phân bổ qua 3 khớp. Phóng to: HAND_SCALE.
import * as THREE from '../../shared/node_modules/three/build/three.module.js';
import { buildCharacter as baseBuild } from '../../shared/cast.js';
import { ell, sph, cap, rbox, smin, smax, gauss, sstep, fbm, vnoise, sculpt, patch, tube, gridGeo, CpuSkin, len3 } from './sdf.js';
import { paintMap, normalMap } from './tex3d.js';
import { paintFace, faceUV, EXPR } from './facepaint.js';

// Phóng to bàn tay + ngón (không thuộc C3; trần cho phép 1,3×). Cas: tối đa để chim bóng thành hình cánh. Ida: vừa đủ cho cận cảnh.
export const HAND_SCALE = { ida: 1.15, cas: 1.3 };
// Búi tóc Ida phóng 1,3× so với model sheet (0,42 H → 0,55 H) để đọc rõ trong silhouette nghiêng.
export const BUN_SCALE = 1.3;
// Cổng 5 (W3): lọn tóc bạc thái dương (A1) — 'temple' = ngắn, dày, ở thái dương (đề xuất W3); 'long' = bản v1.2 (buông tới má). opts.idaWisps ghi đè.
export const IDA_WISPS = 'temple';
// Màu thứ cấp mới (chi tiết được phép thêm để sửa lỗi đọc giới tính/tuổi) — chờ chủ dự án duyệt.
export const EXTRA_COLORS = { ida_scarf: '#8e5c5a', ida_skirt: '#4a3a44', ida_stockings: '#3a3235', cas_hair: '#5a4034', lips_ida: '#b98a82', nail: '#ecd2c4' };

const D2R = Math.PI / 180;

function defaultMaterial(role, color, part, extra = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: 1, metalness: 0, side: THREE.DoubleSide, ...extra });
}

// Hướng tròn (x, z) quanh trục y: φ = 0 → +z.
const phiOf = (x, z) => Math.atan2(x, z);

export function buildCharacter(sheet, opts = {}) {
  const ch = baseBuild(sheet, opts);
  const H = sheet.H_m, P = sheet.parts, C = sheet.local_colors, J = sheet.joints_default;
  const isIda = sheet.id.startsWith('CHR-ida');
  const q = Math.max(0.55, Math.min(1.15, (opts.detail ?? 28) / 32));   // hệ số độ mịn lưới theo gợi ý của cảnh
  const R = (n) => Math.max(6, Math.round(n * q));
  const matFn = opts.material ?? defaultMaterial;
  const joints = ch.joints;

  // ---- gỡ hình khối cũ (giữ khung xương, nhóm vạt áo, đạo cụ) ----
  for (const m of ch.parts) if (m.parent) m.parent.remove(m);
  ch.parts.length = 0;
  const baseSetPose = ch.setPose;
  baseSetPose({ joints: {}, props: [], hands: {} });   // tư thế nghỉ (mọi khớp 0) để dựng + ghi bind
  const root = ch.root;

  // ---- vật liệu ----
  const mcache = new Map();
  // normalMap chỉ cho len đan và tóc (thấy được sau lớp vẽ); da, dạ, vải, da thuộc chỉ dùng map loang (rẻ hơn, bớt vi chi tiết kiểu CG).
  const TEX = { skin: ['skin', null, 0], coat: ['cloth', null, 0], lining: ['lining', null, 0], hat: ['felt', null, 0],
    hair: ['hair', 'hair', 0.9], boots: ['leather', null, 0], sweater: ['knit', 'knit', 1.0], cap: ['knit', 'knit', 1.0], bobble: ['knit', 'knit', 1.2],
    trousers: ['cloth', null, 0], scarf: ['knit', 'knit', 0.9], skirt: ['cloth', null, 0], rib: ['knit', 'rib', 1.0], eyes: null };
  const M = (role, color, part, texRole) => {
    const tr = TEX[texRole ?? role]; const key = role + '|' + color + '|' + (texRole ?? role);
    if (!mcache.has(key)) {
      const extra = { vertexColors: true };
      if (tr) { extra.map = paintMap(tr[0], 3); if (tr[1]) { extra.normalMap = normalMap(tr[1], 5); extra.normalScale = new THREE.Vector2(tr[2], tr[2]); } }
      mcache.set(key, matFn(role === 'rib' ? 'sweater' : role, color, part, extra));
    }
    return mcache.get(key);
  };
  const parts = ch.parts;
  const ensureColor = (g) => { if (!g.attributes.color) { const n = g.attributes.position.count; g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(n * 3).fill(1), 3)); } return g; };
  const add = (parent, geo, role, color, part, texRole) => {
    const m = new THREE.Mesh(ensureColor(geo), M(role, color, part, texRole));
    m.userData.part = part; m.castShadow = true; m.receiveShadow = true; parent.add(m); parts.push(m); return m;
  };
  // Màu đỉnh: AO từ SDF (tối ở nếp, hốc) + hàm màu riêng.
  const aoCol = (sdf, k, fn) => (x, y, z, n) => {
    let occ = 0; for (const [h, w] of [[0.02, 0.5], [0.05, 0.3], [0.1, 0.2]]) occ += w * Math.max(0, (h - sdf(x + n[0] * h, y + n[1] * h, z + n[2] * h)) / h);
    const a = 1 - k * Math.min(1, occ); const c = fn ? fn(x, y, z, n) : [1, 1, 1];
    return [c[0] * a, c[1] * a, c[2] * (a * 0.9 + 0.1)];   // bóng AO hơi lạnh (tím) — pha màu kiểu tranh
  };

  const skin = new CpuSkin(root);
  let hatPivot = null;
  const skinned = [];   // [mesh, weightFn]

  // =============================== ĐẦU ===============================
  const hd = P.head, headG = joints.head;
  const E = isIda ? [0.145, 0.575, 0.298] : [0.155, 0.495, 0.33];   // tâm nhãn cầu (H, hệ đầu: y=0 cằm, 1 đỉnh sọ, z mặt)
  const ER = isIda ? 0.058 : 0.062;
  const front = (z, z0) => sstep(z0, z0 + 0.1, z);
  // Nếp nhăn Ida: rãnh 2D chiếu lên mặt trước (x, y), mặt nạ theo z.
  const g2 = (ax, y, pts, w) => { let d = 1e9; for (let i = 0; i < pts.length - 1; i++) { const [a0, a1] = pts[i], [b0, b1] = pts[i + 1]; const bx = b0 - a0, by = b1 - a1; const h = Math.max(0, Math.min(1, ((ax - a0) * bx + (y - a1) * by) / (bx * bx + by * by))); d = Math.min(d, Math.hypot(ax - a0 - bx * h, y - a1 - by * h)); } return gauss(d, w); };
  function idaWrinkle(x, y, z) {
    if (z < 0.12) return 0;
    const ax = Math.abs(x), fm = front(z, 0.14); let w = 0;
    for (const [yy, dd] of [[0.735, 0.0045], [0.772, 0.0055], [0.808, 0.0045]]) w += dd * gauss(y - yy - 0.10 * ax * ax, 0.0075) * sstep(0.30, 0.10, ax);
    w += 0.004 * gauss(ax - 0.028, 0.006) * gauss(y - 0.655, 0.028);                                   // nếp cau mày
    for (const a of [-0.45, -0.1, 0.25]) w += 0.003 * g2(ax, y, [[0.228, 0.577], [0.228 + 0.06 * Math.cos(a), 0.577 + 0.06 * Math.sin(a)]], 0.009);   // vết chân chim
    w += 0.006 * g2(ax, y, [[0.07, 0.522], [0.15, 0.505], [0.215, 0.525]], 0.008);                      // bọng dưới mắt
    w -= 0.004 * g2(ax, y, [[0.08, 0.542], [0.15, 0.53], [0.20, 0.545]], 0.012);
    w += 0.008 * g2(ax, y, [[0.078, 0.425], [0.105, 0.33], [0.122, 0.27]], 0.016);                     // rãnh mũi–má
    w -= 0.007 * g2(ax, y, [[0.115, 0.42], [0.14, 0.32], [0.15, 0.24]], 0.02);                          // má sệ bên ngoài rãnh
    w += 0.005 * g2(ax, y, [[0.108, 0.215], [0.118, 0.13]], 0.011);                                       // rãnh khoé miệng xuống cằm
    w -= 0.010 * gauss(Math.hypot(ax - 0.17, y - 0.16), 0.05);                                          // hàm sệ nhẹ
    return w * fm;
  }
  function headSDF(x, y, z) {
    const ax = Math.abs(x);
    let d;
    if (isIda) {
      d = ell(x, y, z, [0, 0.59, -0.03], [0.385, 0.41, 0.44]);   // đỉnh sọ ≈ 1,0 H (C3: đầu = cằm → đỉnh sọ)
      d = smin(d, ell(x, y, z, [0, 0.40, 0.09], [0.30, 0.34, 0.31]), 0.12);
      d = smin(d, sph(x, y, z, [0, 0.105, 0.25], 0.085), 0.10);
      d = smin(d, cap(ax, y, z, [0.26, 0.36, -0.02], [0.12, 0.11, 0.21], 0.055), 0.10);
      d = smin(d, ell(ax, y, z, [0.215, 0.49, 0.25], [0.085, 0.05, 0.08]), 0.09);              // gò má cao (V5: hoà mềm hơn)
      d += 0.003 * gauss(Math.hypot(ax - 0.23, y - 0.36), 0.06) * front(z, 0.15);             // má hóp dưới gò (V5: nông lại — bóng khối từng đọc thành vết bầm)
      d = smin(d, cap(ax, y, z, [0.02, 0.662, 0.39], [0.22, 0.652, 0.31], 0.035, 0.025), 0.05); // cung mày
      d = smax(d, -ell(ax, y, z, [E[0], E[1] + 0.008, 0.375], [0.092, 0.066, 0.07]), 0.04);     // hốc mắt
      const lid = sph(ax, y, z, E, ER + 0.008);
      d = smin(d, smax(lid, -(y - (E[1] + 0.009 - 0.03 * (ax - E[0]))), 0.014), 0.02);          // mí trên nặng (tuổi), đuôi cụp
      d = smin(d, smax(lid, y - (E[1] - 0.036), 0.01), 0.012);                                  // mí dưới
      d = smin(d, cap(ax, y, z, [0.09, 0.616, 0.345], [0.21, 0.598, 0.305], 0.018), 0.03);        // nếp da chùng trên mí
      d = smin(d, cap(x, y, z, [0, 0.625, 0.37], [0, 0.47, 0.465], 0.030, 0.038), 0.04);        // sống mũi dài
      d = smin(d, sph(x, y, z, [0, 0.535, 0.44], 0.032), 0.03);                                 // gồ mũi
      d = smin(d, sph(x, y, z, [0, 0.435, 0.49], 0.040), 0.035);                                 // đầu mũi
      d = smin(d, sph(x, y, z, [0, 0.41, 0.478], 0.032), 0.03);                                // khoằm xuống
      d = smin(d, sph(ax, y, z, [0.046, 0.415, 0.435], 0.034), 0.03);                             // cánh mũi
      d = smax(d, -ell(ax, y, z, [0.025, 0.397, 0.455], [0.013, 0.008, 0.018]), 0.008);         // lỗ mũi
      d = smin(d, ell(x, y, z, [0, 0.29, 0.345], [0.07, 0.022, 0.03]), 0.05);                    // môi trên mỏng (mềm, không tạo gờ khuất tia chiếu)
      d = smin(d, ell(x, y, z, [0, 0.245, 0.33], [0.06, 0.02, 0.03]), 0.05);                     // môi dưới (lùi, mềm)
      // C′ (vòng 3): khe miệng và nếp nhăn KHÔNG khắc vào hình học nữa (L3: rãnh khoé miệng như sẹo) — vẽ trên texture mặt (facepaint.js).
    } else {
      d = ell(x, y, z, [0, 0.57, -0.04], [0.45, 0.43, 0.48]);
      d = smin(d, ell(x, y, z, [0, 0.36, 0.07], [0.37, 0.33, 0.37]), 0.14);
      d = smin(d, sph(ax, y, z, [0.19, 0.31, 0.27], 0.13), 0.09);                               // má tròn trẻ con
      d = smin(d, sph(x, y, z, [0, 0.12, 0.23], 0.10), 0.10);                                   // cằm nhỏ
      d = smax(d, -ell(ax, y, z, [E[0], E[1] + 0.005, 0.415], [0.09, 0.075, 0.06]), 0.05);
      const lid = sph(ax, y, z, E, ER + 0.006);
      d = smin(d, smax(lid, -(y - (E[1] + 0.032)), 0.01), 0.012);
      d = smin(d, smax(lid, y - (E[1] - 0.045), 0.01), 0.012);
      d = smin(d, cap(x, y, z, [0, 0.50, 0.40], [0, 0.40, 0.45], 0.028, 0.034), 0.04);
      d = smin(d, sph(x, y, z, [0, 0.38, 0.455], 0.048), 0.035);                                // mũi nhỏ tròn
      d = smin(d, sph(ax, y, z, [0.036, 0.366, 0.44], 0.028), 0.025);
      d = smax(d, -ell(ax, y, z, [0.02, 0.352, 0.462], [0.011, 0.007, 0.014]), 0.006);
      d = smin(d, ell(x, y, z, [0, 0.272, 0.408], [0.066, 0.019, 0.028]), 0.03);
      d = smin(d, ell(x, y, z, [0, 0.238, 0.398], [0.056, 0.021, 0.03]), 0.03);
      // C′: khe miệng vẽ trên texture mặt.
    }
    return d;
  }
  // C′: má, mũi, môi, hốc mắt, mi, nếp nhăn, đồi mồi chuyển sang texture vẽ tay (facepaint.js); màu đỉnh chỉ giữ trán sáng vàng + AO.
  const skinTone = (x, y, z, n) => { const brow = gauss(y - 0.78, 0.12) * front(z, 0.1);
    // Cổng 5 (W3, A1): mặt dưới hàm/cằm quay xuống cổ áo và thân → tối dần (che khuất bởi cổ áo), mặt không còn sáng đều tới tận mép hàm như mặt nạ
    const occ = isIda && n ? 0.30 * sstep(-0.15, -0.75, n[1]) * sstep(0.34, 0.12, y) : 0;
    return [(1 + 0.02 * brow) * (1 - occ), (1 + 0.02 * brow) * (1 - occ * 1.05), 1 - occ * 0.9]; };
  const hq = isIda ? (opts.faceQ ?? 1) : 0.8;   // Cổng 4: cận mặt có thể tăng mật độ lưới đầu (biến dạng mịn)
  add(headG, sculpt(headSDF, { c: [0, 0.48, 0.02], r: [0.45, 0.6, 0.6], nu: R(112 * hq), nv: R(84 * hq), scale: H, uv: [6, 3], gradE: 0.002, warp: [0.4, 0.62], eps: 2e-5,
    color: aoCol(headSDF, 0.22, skinTone) }), 'skin', C.skin, 'head');
  // Cổng 4 (Việc 1): MẶT BIẾN DẠNG. UV chiếu trước gán ở tư thế trung tính, SAU ĐÓ dịch đỉnh theo biểu cảm → lớp vẽ C′ bám lưới
  // (nét mày, mi, khoé miệng đi cùng khối da). Nét vẽ chỉ giữ phần không phải hình khối: ngấn nước, nước mắt, nếp cười, nếp cằm, nếp giữa mày.
  const XP = EXPR[opts.expr] || EXPR.neutral, X0 = EXPR.neutral;
  const exprDisp = (x, y, z) => {
    const fm = sstep(0.1, 0.3, z); if (fm <= 0) return [0, 0, 0];
    const ax = Math.abs(x), sx = x < 0 ? -1 : 1, gp = (cx, cy, r) => gauss(Math.hypot(ax - cx, y - cy), r), as = 1 + (XP.asym || 0) * sx;   // mặt thật lệch hai bên
    const my = isIda ? 0.267 : 0.256, mw = isIda ? 0.098 : 0.066, dc = (XP.corner - X0.corner) * as, sm = XP.smile * as, pr = Math.max(0, XP.press - X0.press);
    let dx = 0, dy = 0, dz = 0, k;
    k = gp(mw, my, 0.042); dy += dc * k; dz -= 0.3 * Math.abs(dc) * k; dx += sx * 0.25 * Math.max(0, dc) * k;      // khoé miệng (cười: lên, ra ngoài)
    k = gp(0.165, 0.40, 0.065); dy += 0.018 * sm * k; dz += 0.012 * sm * k;                                      // gò má nâng khi cười
    k = gauss(ax, 0.045) * gauss(y - my - 0.022, 0.018); dy -= 0.005 * pr * k; dz -= 0.004 * pr * k;              // mím: môi trên vào
    k = gauss(ax, 0.05) * gauss(y - my + 0.024, 0.02); dy += 0.006 * pr * k; dz -= 0.002 * pr * k;                // môi dưới lên
    k = gp(0, 0.145, 0.055); dy += 0.012 * XP.chin * k; dz += 0.008 * XP.chin * k;                               // cằm đẩy lên (nghẹn)
    k = gp(0.05, 0.66, 0.05); dy += XP.browIn * (2 - as) * k; dx -= sx * XP.knit * k; dz += 0.3 * XP.knit * k;               // đầu trong mày
    k = gp(0.21, 0.645, 0.05); dy += XP.browOut * k;                                                              // đuôi mày
    k = gauss(ax, 0.1) * gauss(y - 0.75, 0.06); dy += 0.5 * XP.browIn * k;                                        // trán giữa kéo lên theo
    // mí: xoay quanh tâm nhãn cầu (giữ khoảng cách tới mắt, không để nhãn cầu xuyên mí); mí trên sụp, mí dưới nâng khi cười
    const Y = y - E[1], Z = z - E[2], rr = Math.hypot(ax - E[0], Y, Z), shell = gauss(rr - ER - 0.01, 0.018) * gauss(ax - E[0], 0.07);
    const th = (XP.lidDrop - X0.lidDrop) / ER * sstep(-0.005, 0.015, Y) * shell - 0.008 * sm / ER * sstep(0.005, -0.015, Y) * shell;
    if (th) { const c = Math.cos(th), s_ = Math.sin(th); dy += (Y * c - Z * s_) - Y; dz += (Y * s_ + Z * c) - Z; }
    return [dx * fm, dy * fm, dz * fm];
  };
  { const hm = parts[parts.length - 1], geo = hm.geometry; faceUV(geo, H);   // C′: mặt vẽ tay, UV chiếu trước trên chính lưới đầu → đi theo đầu, không trượt
    if (opts.expr && opts.expr !== 'neutral') {
      const pa = geo.attributes.position, nA = geo.attributes.normal, n0 = geo.clone(); n0.computeVertexNormals();
      for (let i = 0; i < pa.count; i++) { const d = exprDisp(pa.getX(i) / H, pa.getY(i) / H, pa.getZ(i) / H); if (d[0] || d[1] || d[2]) pa.setXYZ(i, pa.getX(i) + d[0] * H, pa.getY(i) + d[1] * H, pa.getZ(i) + d[2] * H); }
      const n1 = geo.clone(); n1.computeVertexNormals(); const a0 = n0.attributes.normal, a1 = n1.attributes.normal;   // pháp tuyến: gradient SDF + (lưới sau − lưới trước)
      for (let i = 0; i < pa.count; i++) { const v = new THREE.Vector3(nA.getX(i) + a1.getX(i) - a0.getX(i), nA.getY(i) + a1.getY(i) - a0.getY(i), nA.getZ(i) + a1.getZ(i) - a0.getZ(i)).normalize(); nA.setXYZ(i, v.x, v.y, v.z); }
      pa.needsUpdate = nA.needsUpdate = true; geo.computeBoundingSphere();
    }
    const fm = paintFace(isIda, E, 7, opts.expr, { mesh: true });
    hm.material = matFn('skin', C.skin, 'head', { map: fm, vertexColors: true, emissive: new THREE.Color('#ffffff'), emissiveMap: fm.userData.glint, emissiveIntensity: opts.glint ?? 5.0 });
    // Cổng 4: bỏ vệt tím ở má — nơi ánh sáng tới da nghiêng lạnh (trời, viền), đưa sắc ánh sáng về xám ấm; ánh đèn khí (ấm) không đổi.
    const mat = hm.material, prev = mat.onBeforeCompile, warm = opts.skinWarm ?? 0.7;
    mat.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r);
      sh.fragmentShader = sh.fragmentShader.replace('vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;',
        `vec3 dSk = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse; vec3 alb = max(diffuseColor.rgb, vec3(1e-3)); vec3 eSk = dSk / alb;
         float lSk = dot(eSk, vec3(0.2126, 0.7152, 0.0722)), cSk = smoothstep(0.0, 0.25, (eSk.b - eSk.r) / max(lSk, 1e-5));
         eSk = mix(eSk, lSk * vec3(1.06, 1.0, 0.92), ${warm.toFixed(3)} * cSk);
         vec3 outgoingLight = eSk * alb + totalEmissiveRadiance;`); };
    const pk = mat.customProgramCacheKey?.bind(mat); mat.customProgramCacheKey = () => (pk ? pk() : '') + '|skinWarm' + warm; }
  // Nhãn cầu (màu đỉnh: lòng trắng xỉn, tròng, con ngươi) — nhìn hơi xuống.
  const eyeTex = (() => {   // tròng mắt vẽ trên canvas (UV cầu: +z ở u = 0,25, v = 0,5)
    const cv = document.createElement('canvas'); cv.width = 256; cv.height = 128; const g = cv.getContext('2d');
    g.fillStyle = isIda ? '#7a6e66' : '#a8998e'; g.fillRect(0, 0, 256, 128);   // v1.2: lòng trắng Ida xỉn hơn (bớt "mắt phát sáng" khi mặt tối)
    const cx = 64, cy = 64, ri = isIda ? 21 : 25;
    const gr = g.createRadialGradient(cx, cy, ri * 0.3, cx, cy, ri); gr.addColorStop(0, isIda ? (C.eyes || '#5a4636') : '#5a3a26'); gr.addColorStop(0.85, isIda ? '#3f3128' : '#3e2616'); gr.addColorStop(1, '#241c1a');   // v1.2: tròng Ida nâu theo sheet (bản cũ xanh xám đọc thành mắt xanh)
    g.fillStyle = gr; g.beginPath(); g.ellipse(cx, cy, ri, ri, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#0d0a0a'; g.beginPath(); g.arc(cx, cy, ri * 0.42, 0, Math.PI * 2); g.fill();
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace;
    // V5: điểm sáng phản chiếu (catchlight) vẽ trên lớp phát sáng — mắt "búp bê" khi thiếu nó (kiểm mù lần 1)
    const cc = document.createElement('canvas'); cc.width = 256; cc.height = 128; const c2 = cc.getContext('2d'); c2.fillStyle = '#000'; c2.fillRect(0, 0, 256, 128);
    c2.fillStyle = '#fff'; c2.beginPath(); c2.ellipse(cx + ri * 0.3, cy - ri * 0.35, ri * 0.2, ri * 0.16, 0, 0, Math.PI * 2); c2.fill();
    const tc = new THREE.CanvasTexture(cc); tc.colorSpace = THREE.SRGBColorSpace; t.userData = { glint: tc }; return t;
  })();
  for (const sx of [1, -1]) {
    const eg = new THREE.SphereGeometry(ER * H, R(20), R(14));
    const e = new THREE.Mesh(ensureColor(eg), matFn('eyes', '#ffffff', 'eyes', { map: eyeTex, vertexColors: true, emissive: new THREE.Color('#ffffff'), emissiveMap: eyeTex.userData.glint, emissiveIntensity: (opts.glint ?? 5.0) * 3 }));
    e.userData.part = 'eyes'; e.castShadow = true; e.receiveShadow = true; headG.add(e); parts.push(e);
    e.position.set(sx * E[0] * H, E[1] * H, E[2] * H); e.rotation.set((isIda ? 0.1 : 0.04) + (opts.gaze?.[1] ?? 0), -sx * 0.05 + (opts.gaze?.[0] ?? 0), 0);   // Cổng 4: opts.gaze [ngang, dọc] (rad) — ánh mắt có điểm nhìn
  }
  // Lông mày: sợi thon dọc cung mày.
  const strandGeo = (pts, rad, nu, nv) => {
    const curve = new THREE.CatmullRomCurve3(pts.map((p) => new THREE.Vector3(...p)), false, 'centripetal'); const fr = curve.computeFrenetFrames(nv, false);
    const pos = new Float32Array((nu + 1) * (nv + 1) * 3), uv = new Float32Array((nu + 1) * (nv + 1) * 2); let k = 0;
    for (let j = 0; j <= nv; j++) { const s = j / nv, c = curve.getPointAt(s), N = fr.normals[j], B = fr.binormals[j];
      for (let i = 0; i <= nu; i++, k++) { const a = 2 * Math.PI * i / nu, [rw, rh] = rad(s, a); pos.set([c.x + N.x * Math.cos(a) * rw + B.x * Math.sin(a) * rh, c.y + N.y * Math.cos(a) * rw + B.y * Math.sin(a) * rh, c.z + N.z * Math.cos(a) * rw + B.z * Math.sin(a) * rh], k * 3); uv.set([i / nu, s * 4], k * 2); } }
    const g = gridGeo(pos, null, uv, null, nu, nv);
    // hướng pháp tuyến ra ngoài
    const n0 = g.attributes.normal, c0 = curve.getPointAt(0.5), mid = (Math.round(nv / 2)) * (nu + 1);
    const dx = pos[mid * 3] - c0.x, dy = pos[mid * 3 + 1] - c0.y, dz = pos[mid * 3 + 2] - c0.z;
    if (dx * n0.getX(mid) + dy * n0.getY(mid) + dz * n0.getZ(mid) < 0) { const ix = g.index.array; for (let i = 0; i < ix.length; i += 3) { const t = ix[i + 1]; ix[i + 1] = ix[i + 2]; ix[i + 2] = t; } g.computeVertexNormals(); }
    return g;
  };
  function onFace(x, y) { let z = 0.9; for (let it = 0; it < 80; it++) { const v = headSDF(x, y, z); if (Math.abs(v) < 1e-5) break; z -= v * 0.7; } return z; }
  const browCol = isIda ? '#5e5552' : EXTRA_COLORS.cas_hair;   // V5: mày Ida xám đậm (sợi màu tóc bạc đè mất nét mày vẽ)
  for (const sx of [1, -1]) {
    const pts = isIda ? [[0.045, 0.655, 0.405], [0.12, 0.672, 0.395], [0.19, 0.664, 0.355], [0.235, 0.638, 0.315]] : [[0.055, 0.60, 0.43], [0.13, 0.607, 0.425], [0.215, 0.586, 0.39]];
    // Cổng 4: lông mày sợi dịch theo CÙNG trường biến dạng của lưới đầu (thay cho dịch tay theo EXPR)
    const g = strandGeo(pts.map(([x, y]) => { const z = onFace(x, y) + 0.003, d = exprDisp(sx * x, y, z); return [(sx * x + d[0]) * H, (y + d[1]) * H, (z + d[2]) * H]; }), (s) => { const t = Math.sin(Math.PI * Math.min(1, 0.25 + s)); return [(isIda ? 0.010 : 0.015) * H * t, 0.004 * H]; }, 6, 10);
    add(headG, g, 'hair', browCol, 'brow');
  }
  // Tai: elip dẹt, lõm hố tai, vành cuộn.
  const earH = isIda ? 0.30 : P.ears.size_H, earOut = isIda ? 0.18 : P.ears.angle_out_deg * D2R;
  for (const sx of [1, -1]) {
    const g = new THREE.SphereGeometry(1, R(22), R(18)); const pa = g.attributes.position;
    for (let i = 0; i < pa.count; i++) {
      let x = pa.getX(i), y = pa.getY(i), z = pa.getZ(i); const r = Math.hypot(y, z);
      x *= 0.22; if (x > 0) x -= 0.32 * Math.max(0, 1 - (r / 0.78) ** 2) * (0.6 + 0.4 * sstep(-0.6, 0.3, y));   // hố tai
      const wz = 0.62 + 0.18 * sstep(-0.8, 0.6, y) - (y < -0.5 ? 0.08 : 0);                                        // trên rộng, dái nhỏ
      pa.setXYZ(i, x * earH * 0.5 * H, y * earH * 0.5 * H, z * wz * earH * 0.5 * H);
    }
    g.computeVertexNormals(); if (sx < 0) { g.scale(-1, 1, 1); const ix = g.index.array; for (let i = 0; i < ix.length; i += 3) { const t = ix[i + 1]; ix[i + 1] = ix[i + 2]; ix[i + 2] = t; } g.computeVertexNormals(); }
    // Bản lề tai ở mép trước (dính má) → mép sau vểnh ra ngoài theo góc model sheet (đọc được trong silhouette sau lưng).
    const wz0 = 0.8 * earH * 0.5; g.translate(0, 0, -wz0 * H);
    const hinge = new THREE.Group(); hinge.position.set(sx * hd.width_front / 2 * H * 0.93, (isIda ? 0.56 : 0.50) * H, (isIda ? 0.08 : 0.06) * H); headG.add(hinge);
    hinge.rotation.set(0, -sx * earOut, -sx * 0.10);
    add(hinge, g, 'skin', C.skin, 'ear');
    if (isIda) {   // A1 (Cổng 4, sheet v1.2): đôi khuyên tai nhỏ ở dái tai — hạt tròn kim loại, bắt ánh đèn (dấu hiệu nữ nhìn được từ trước)
      const ringM = new THREE.MeshStandardMaterial({ color: '#c9a466', metalness: 0.85, roughness: 0.28, emissive: new THREE.Color('#5a4424'), emissiveIntensity: 0.25 });
      const stud = new THREE.Mesh(new THREE.SphereGeometry(0.022 * H, 14, 10), ringM); stud.position.set(sx * 0.02 * H, -0.125 * H, -0.09 * H);
      const drop = new THREE.Mesh(new THREE.SphereGeometry(0.03 * H, 14, 10), ringM); drop.position.set(sx * 0.022 * H, -0.172 * H, -0.09 * H);
      for (const m of [stud, drop]) { m.userData.part = 'earring'; m.castShadow = false; m.receiveShadow = false; hinge.add(m); parts.push(m); }
    }
  }

  // =============================== TÓC / MŨ ===============================
  if (isIda) {
    const hc = [0, 0.59, -0.03], hr = [0.385, 0.41, 0.44];
    const thMax = (ph) => { const c = Math.cos(ph); return c > 0 ? 1.50 - 0.50 * c : 1.50 + 0.95 * Math.pow(-c, 1.3); };
    const bunC = [0, 0.50, -0.56];
    const bax = [0, -0.25, -1]; const bl = len3(...bax); const BA = bax.map((v) => v / bl);
    const hairSDF = (x, y, z) => {
      const dx = x - hc[0], dy = y - hc[1], dz = z - hc[2], th = Math.acos(Math.max(-1, Math.min(1, dy / (len3(dx, dy, dz) || 1)))), ph = Math.atan2(dx, dz);
      const edge = 1 - sstep(thMax(ph) - 0.22, thMax(ph) + 0.02, th);
      // sợi chải về búi: góc phương vị quanh trục búi
      const px = x - bunC[0], py = y - bunC[1], pz = z - bunC[2]; const dp = px * BA[0] + py * BA[1] + pz * BA[2];
      const qx = px - BA[0] * dp, qy = py - BA[1] * dp, qz = pz - BA[2] * dp; const az = Math.atan2(qx, qy * 0.97 - qz * 0.24);
      const strands = 0.0045 * Math.abs(Math.sin(az * 34 + 1.5 * fbm(x * 8, y * 8, z * 8, 2, 3)));
      return ell(x, y, z, hc, hr) - (0.006 + 0.03 * edge) + strands;
    };
    add(headG, patch(hairSDF, { c: hc, t0: 0.75, nu: R(84), nv: R(24), phA: -Math.PI, phB: Math.PI, th: (u, ph) => thMax(ph), scale: H, uv: [8, 2],
      color: (x, y, z, n, u, v) => { const k = 1 - 0.25 * sstep(0.7, 1, v); return [k, k, k * 1.02]; } }), 'hair', C.hair, 'hair');
    // Búi tóc to: cuộn xoắn.
    const bunR = sheet.costume.hair.bun_diameter_H / 2 * (sheet.costume.hair.bun_scale ?? BUN_SCALE);
    const bunSDF = (x, y, z) => {
      const px = x - bunC[0], py = y - bunC[1], pz = z - bunC[2];
      const a = Math.atan2(px, py), rho = Math.hypot(px, py);
      const coil = 0.012 * Math.abs(Math.sin(a * 1 + rho * 48 - pz * 10)) + 0.004 * Math.abs(Math.sin(a * 30));
      let d = ell(x, y, z, bunC, [bunR, bunR * 0.88, bunR * 0.8]) + coil;
      return smin(d, ell(x, y, z, [0, 0.52, -0.42], [0.2, 0.17, 0.13]), 0.06);
    };
    add(headG, sculpt(bunSDF, { c: bunC, r: [bunR, bunR, bunR], nu: R(40), nv: R(26), scale: H, uv: [3, 2], color: aoCol(bunSDF, 0.5) }), 'hair', C.hair, 'hair');
    // A1 (Cổng 4, sheet v1.2): vài lọn tóc mềm thoát khỏi búi — 3 lọn mỗi bên thái dương buông cong trước tai, 2 lọn ở gáy.
    const wisp = (pts, w) => strandGeo(pts.map(([x, y, z]) => [x * H, y * H, z * H]), (t) => [w * H * Math.sin(Math.PI * Math.min(1, 0.15 + t)), w * 0.7 * H], 5, 14);
    // Cổng 5 (W3): lọn ở THÁI DƯƠNG (đuôi dừng ở y ≈ 0,53 H, không buông xuống má), dày hơn (0,015–0,019 H), tách khỏi da — lọn mảnh dài áp sát má từng đọc như vết xước ở góc nghiêng
    //   Hai phương án (P chọn — ĐỔI SỐ ĐO B1 0°, xem reports/m2/cong5/w3/BAO-CAO-W3.md): 'temple' (mặc định, ngắn ở thái dương) | 'long' (v1.2, buông tới má).
    const wispMode = opts.idaWisps ?? IDA_WISPS;
    const WISP_PTS = wispMode === 'long'
      ? { w: [0.011, 0.009, 0.008], dy: [0, -0.035, 0.03], pts: [[0.335, 0.67, 0.12], [0.372, 0.59, 0.17], [0.365, 0.51, 0.2], [0.382, 0.45, 0.17]] }
      : { w: [0.019, 0.016, 0.015], dy: [0, -0.03, 0.03], pts: [[0.338, 0.70, 0.12], [0.380, 0.64, 0.165], [0.394, 0.58, 0.19], [0.41, 0.535, 0.175]] };
    for (const sx of [1, -1]) for (const [k, dz] of [[0, 0], [1, 0.03], [2, -0.035]])
      add(headG, wisp(WISP_PTS.pts.map(([x, y, z]) => [sx * x, y + WISP_PTS.dy[k], z + dz]), WISP_PTS.w[k]), 'hair', C.hair, 'hair');
    for (const sx of [1, -1]) add(headG, wisp([[sx * 0.09, 0.42, -0.33], [sx * 0.12, 0.33, -0.31], [sx * 0.105, 0.25, -0.28]], 0.012), 'hair', C.hair, 'hair');
    // Mũ phớt mềm: chóp có rãnh giữa và hai vết bóp trước; vành cụp trước, mép cuộn; băng mũ.
    const hs = sheet.costume.hat; const hat = new THREE.Group(); hat.position.y = 0.86 * H; hat.rotation.x = 0.08;
    const ch_ = hs.crown_height_H, rx0 = hd.width_front * 0.56, rz0 = rx0 * 1.12;
    // Cổng 4: bản lề mũ ở mép sau băng mũ → pose.hat_back (0–1) hất vành lên, mũ ngả ra sau (cử chỉ đẩy mũ trước câu thoại 1:50)
    hatPivot = new THREE.Group(); hatPivot.position.set(0, 0.86 * H, -rz0 * H); headG.add(hatPivot); hatPivot.add(hat); hat.position.set(0, 0, rz0 * H);
    const crownSDF = (x, y, z) => {
      const f = 1 - 0.16 * sstep(0, ch_, y);
      const ds = (Math.hypot(x / (rx0 * f), z / (rz0 * f)) - 1) * rx0 * f;
      const dent = 0.075 * gauss(x, 0.07) * sstep(-rz0 * 0.9, -rz0 * 0.2, z) * (1 - 0.3 * sstep(0.2, 0.5, z)) + 0.05 * gauss(Math.hypot(Math.abs(x) - 0.2, z - 0.30), 0.09) * sstep(ch_ * 0.4, ch_, y);
      return smax(smax(ds + 0.04 * gauss(Math.hypot(Math.abs(x) - 0.2, z - 0.32), 0.09) * sstep(ch_ * 0.3, ch_, y), y - ch_ + dent, 0.1), -(y + 0.03), 0.02);
    };
    add(hat, sculpt(crownSDF, { c: [0, ch_ * 0.45, 0], r: [rx0, ch_, rz0], nu: R(60), nv: R(28), scale: H, uv: [4, 2], color: aoCol(crownSDF, 0.5) }), 'hat', C.hat, 'hat');
    const br = hs.brim_diameter_H / 2, r0 = rx0 * 0.98, nb = R(72), nr = R(7);
    const bpos = [], buv = [];
    const brimY = (x, z) => { const r = Math.hypot(x, z / 1.12); const f = Math.max(0, (r - r0) / (br - r0)); const fr = 0.5 + 0.5 * (z / Math.max(1e-6, Math.hypot(x, z))); return -f * f * (0.03 + 0.13 * fr * fr) + 0.012 * Math.sin(3 * Math.atan2(x, z)) * f; };
    for (let j = 0; j <= nr; j++) for (let i = 0; i <= nb; i++) { const a = 2 * Math.PI * i / nb - Math.PI, r = r0 + (br - r0) * j / nr; const x = Math.sin(a) * r, z = Math.cos(a) * r * 1.12; bpos.push(x * H, brimY(x, z) * H, z * H); buv.push(i / nb * 6, j / nr); }
    const bg = gridGeo(new Float32Array(bpos), null, new Float32Array(buv), null, nb, nr); add(hat, bg, 'hat', C.hat, 'hat');
    const rim = []; for (let i = 0; i <= 48; i++) { const a = 2 * Math.PI * i / 48 - Math.PI, x = Math.sin(a) * br, z = Math.cos(a) * br * 1.12; rim.push([x * H, (brimY(x, z) - 0.004) * H, z * H]); }
    add(hat, strandGeo(rim, () => [0.016 * H, 0.012 * H], 5, R(64)), 'hat', C.hat, 'hat');
    const band = tube({ y0: 0.12 * H, y1: 0.0, nu: R(64), nv: 3, rad: (s, ph) => [Math.hypot(Math.sin(ph) * rx0, Math.cos(ph) * rz0) * 1.018 * H] });
    add(hat, band, 'boots', C.boots, 'hat');
    add(hat, sculpt((x, y, z) => ell(x, y, z, [0, 0, 0], [0.02, 0.06, 0.09]), { c: [0, 0, 0], r: [0.03, 0.06, 0.09], nu: 12, nv: 8, scale: H }), 'boots', C.boots, 'hat').position.set(rx0 * 1.02 * H, 0.06 * H, -0.12 * H);
  } else {
    // Mũ len: vòm có sọc đan, gấp mép, quả bông cao, tròn, xù len.
    const cs = sheet.costume.cap; const capG = new THREE.Group(); capG.position.y = 0.69 * H; headG.add(capG);
    const cr = [hd.width_front * 0.555, cs.height_H * 0.92, hd.width_side * 0.545];
    const capSDF = (x, y, z) => {
      const ph = Math.atan2(x, z); const ribs = 0.006 * Math.abs(Math.sin(ph * 26));
      const t = Math.max(0, y) / cr[1], taper = 1 - 0.22 * t * t;                                   // vòm hơi thuôn về đỉnh (mũ len, không tròn như sọ)
      const gather = 0.02 * sstep(cr[1] * 0.6, cr[1], y) * Math.abs(Math.sin(ph * 5));
      const d = (Math.hypot(x / (cr[0] * taper), (z + 0.02) / (cr[2] * taper)) - 1) * cr[0] * taper;
      return smax(smax(d, ell(x, y, z, [0, 0, -0.02], [cr[0] * 1.3, cr[1], cr[2] * 1.3]), 0.08) + ribs + gather, -(y + 0.02), 0.02);
    };
    add(capG, sculpt(capSDF, { c: [0, cr[1] * 0.3, -0.02], r: cr, nu: R(64), nv: R(28), scale: H, uv: [9, 3], color: aoCol(capSDF, 0.4) }), 'cap', C.cap, 'cap');
    const cuff = tube({ y0: (cs.cuff_H * 0.95) * H, y1: -0.05 * H, nu: R(72), nv: R(8),
      rad: (s, ph) => { const b = Math.sin(Math.PI * s); return [(Math.hypot(Math.sin(ph) * cr[0], Math.cos(ph) * cr[2]) * (1.02 + 0.09 * Math.pow(b, 0.6)) + 0.006 * Math.abs(Math.sin(ph * 36)) * b) * H, 0, -0.02 * H]; } });
    add(capG, cuff, 'cap', C.cap, 'cap', 'rib');
    const bobR = cs.bobble_diameter_H / 2;
    const bobSDF = (x, y, z) => {
      const n1 = fbm(x * 30, y * 30, z * 30, 2, 11), n2 = vnoise(x * 70, y * 70, z * 70, 17);
      return len3(x, y, z) - bobR - 0.028 * Math.max(0, n1) - 0.012 * n2 + 0.01 * Math.abs(n1);
    };
    const bob = add(capG, sculpt(bobSDF, { c: [0, 0, 0], r: [bobR, bobR, bobR], nu: R(44), nv: R(30), scale: H, uv: [3, 2], color: aoCol(bobSDF, 0.6) }), 'bobble', C.bobble, 'bobble');
    bob.position.y = (cr[1] + bobR * 0.95) * H;
    // chỗ túm len dưới quả bông (eo thắt) → quả bông tách khỏi vòm, đọc là quả bông mũ, không phải búi tóc
    add(capG, tube({ y0: (cr[1] + bobR * 0.35) * H, y1: (cr[1] - 0.06) * H, nu: R(20), nv: 5, rad: (ss, ph) => [(0.045 + 0.05 * ss * ss + 0.006 * Math.abs(Math.sin(ph * 8))) * H] }), 'cap', C.cap, 'cap', 'rib');
    // Tóc ngắn: gáy + thái dương, mép lởm chởm.
    const hc = [0, 0.57, -0.04], hr = [0.45, 0.43, 0.48];
    const thMax = (ph) => { const c = Math.cos(ph); return (c > 0 ? 1.55 - 0.62 * c : 1.55 + 0.85 * Math.pow(-c, 1.1)) + 0.05 * Math.sin(ph * 23); };
    const hairSDF = (x, y, z) => {
      const dx = x - hc[0], dy = y - hc[1], dz = z - hc[2], th = Math.acos(Math.max(-1, Math.min(1, dy / (len3(dx, dy, dz) || 1)))), ph = Math.atan2(dx, dz);
      const edge = 1 - sstep(thMax(ph) - 0.2, thMax(ph) + 0.02, th);
      const tuft = 0.008 * Math.max(0, fbm(x * 20, y * 26, z * 20, 2, 5));
      return ell(x, y, z, hc, hr) - (0.004 + 0.022 * edge) - tuft + 0.003 * Math.abs(Math.sin(ph * 40));
    };
    add(headG, patch(hairSDF, { c: hc, t0: 0.8, nu: R(80), nv: R(22), phA: -Math.PI, phB: Math.PI, th: (u, ph) => thMax(ph), scale: H, uv: [8, 2],
      color: (x, y, z, n, u, v) => { const k = 1 - 0.3 * sstep(0.75, 1, v); return [k, k, k]; } }), 'hair', EXTRA_COLORS.cas_hair, 'hair');
  }

  // =============================== CỔ ===============================
  const nL = P.neck.length, nW = P.neck.width_front / 2;
  add(joints.neck, tube({ y0: (nL + 0.22) * H, y1: -0.12 * H, nu: R(28), nv: R(10), uv: [2, 1],
    rad: (s, ph, y) => { const yy = y / H; const tend = isIda ? 0.018 * gauss(Math.abs(ph) - 0.45, 0.16) * sstep(nL + 0.1, 0, yy) : 0;
      const ring = isIda ? 0.004 * Math.sin(yy * 70) * gauss(ph, 0.9) : 0;
      return [(nW * (1 + 0.1 * Math.cos(ph) ** 2) + tend + ring + (isIda ? 0 : 0.01)) * H, 0, (isIda ? 0.03 : 0.01) * H]; },
    // Cổng 5 (W3, A1): cổ Ida nằm trong lòng cổ áo đứng, dưới bóng cằm → da tối (che khuất); khe dưới cằm đọc là bóng, không phải "cột cổ" hồng
    color: isIda ? (s) => { const a = 0.42 + 0.12 * (1 - s); return [a, a * 0.96, a * 0.95]; } : undefined }), 'skin', C.skin, 'neck');

  // =============================== THÂN ===============================
  const tw = P.torso, tL = tw.length;
  const shX = J.shoulder_spacing_H / 2, shY = tL - J.shoulder_offset_from_torso_top_H, hipX = J.hip_joint_spacing_H / 2;
  if (isIda) {
    const coatFold = (x, y, z) => {
      const ph = Math.atan2(x, z); let f = 0;
      f += 0.009 * Math.sin(ph * 16 + 0.5 * fbm(x * 3, y * 3, z * 3, 2, 1)) * gauss(y - 0.66, 0.1);                 // bouffant trên thắt lưng
      f += 0.012 * Math.sin(ph * 11 + 1.1) * sstep(0.5, 0.05, y);                                                   // loe dưới thắt lưng
      f += 0.007 * Math.sin(x * 26 + 0.7) * sstep(0.2, -0.3, z) * gauss(y - 1.1, 0.35);                              // nếp dọc lưng
      f += 0.006 * Math.sin((y - 1.6 * Math.abs(x)) * 22) * sstep(0.35, 0.6, Math.abs(x)) * gauss(y - 1.45, 0.25);    // nếp chéo nách
      f += 0.006 * gauss(x - 0.05, 0.012) * sstep(0.2, 0.3, z) - 0.004 * gauss(x - 0.02, 0.035) * sstep(0.2, 0.3, z); // mép khép áo + nẹp
      return f;
    };
    const torsoSDF = (x, y, z) => {
      const ax = Math.abs(x);
      let d = ell(x, y, z, [0, 1.42, 0], [0.60, 0.52, 0.42]);
      d = smin(d, ell(x, y, z, [0, 0.85, 0], [0.53, 0.55, 0.35]), 0.25);
      d = smin(d, ell(x, y, z, [0, 0.25, 0], [0.64, 0.48, 0.40]), 0.25);
      d = smin(d, cap(ax, y, z, [0.10, 1.93, -0.04], [shX, 1.80, -0.05], 0.14, 0.15), 0.18);
      d = smin(d, ell(x, y, z, [0, 1.62, -0.14], [0.46, 0.34, 0.28]), 0.15);
      d = smin(d, ell(x, y, z, [0, 1.86, -0.17], [0.22, 0.16, 0.14]), 0.14);                         // gồ gáy–vai (dáng người già, cổ đưa ra trước)
      d = smin(d, ell(ax, y, z, [0.19, 1.30, 0.24], [0.17, 0.15, 0.14]), 0.14);
      d = smin(d, cap(x, y, z, [0, 1.8, -0.02], [0, 2.05, 0], 0.2), 0.1);
      d = smax(d, Math.max(-(y + 0.05), y - (tL + 0.02)), 0.03);   // C3: thân chỉ trong khoảng như bản gốc (−0,05 H … tL + 0,02 H)
      return d + coatFold(x, y, z);
    };
    add(joints.spine, sculpt(torsoSDF, { c: [0, 1.0, 0], r: [0.8, 1.3, 0.6], nu: R(76), nv: R(62), scale: H, uv: [5, 6], color: aoCol(torsoSDF, 0.5) }), 'coat', C.coat, 'torso');
    // Cổ áo đứng — Cổng 5 (W3, A1 mục 1): bỏ trụ trơn "cổ ma-nơ-canh" (kiểm mù lần 3). Giữ ý v1.2 (dựng cao, che cổ trần dài), màu áo/lót.
    //  • Mép trên CONG theo đường hàm: độ cao mép ở mỗi hướng φ tính từ CHÍNH hình đầu (tia dọc từ dưới lên gặp SDF đầu, trừ khe 1 cm) →
    //    mép nằm sát ngay dưới cằm và đường hàm, dâng lên hai bên tới góc hàm, sau gáy cao vừa. Mép không cắt ngang má, không lộ khe cổ.
    //  • Loe từ chân lên mép (vải đứng tách khỏi cổ); NẾP GẤP vải dồn ở hai bên trước (chỗ cằm đè), mép gợn theo nếp.
    //  • Mép cuộn dày (viền tròn) + lót trong tối dần vào trong → mép có độ dày, bắt sáng mềm, không phải lưỡi dao.
    //  • Da CPU: phần trên theo khớp ĐẦU (0,9) → khi quay/cúi đầu, đường cong mép vẫn khớp đường hàm (không đâm xuyên, không lộ khe).
    const CL = { base: tL - 0.08, low: tL + 0.24, side: tL + 0.50, back: tL + 0.46, rb: 0.228, rf: 0.28, rs: 0.325, rbk: 0.29, gap: 0.035, tuck: 0.10, wHead: 0.9 };
    const aph = (ph) => Math.abs(Math.atan2(Math.sin(ph), Math.cos(ph)));
    const clFold = (ph, t) => { const a = aph(ph), m = 0.35 + 0.9 * gauss(a - 0.85, 0.45);   // nếp dồn dưới hai góc hàm (cằm đè cổ áo), thưa ở sau
      return Math.pow(t, 0.7) * m * (0.012 * Math.sin(8 * ph + 0.7 + 0.8 * t) + 0.007 * Math.sin(13 * ph + 2.1 - 1.5 * t)); };   // t: 0 chân → 1 mép
    const clR = (ph) => { const a = aph(ph); const rs = CL.rf + (CL.rs - CL.rf) * sstep(0.1, 1.2, a); return rs + (CL.rbk - rs) * sstep(1.6, 2.9, a); };
    const NRIM = 180, RIM = new Float32Array(NRIM + 1);
    { const raw = [];
      for (let i = 0; i < NRIM; i++) { const ph = 2 * Math.PI * i / NRIM, a = aph(ph), r = clR(ph) + clFold(ph, 1) + 0.02, x = Math.sin(ph) * r, z = Math.cos(ph) * r - 0.01;
        const cap_ = CL.side - (CL.side - CL.back) * sstep(1.7, 2.9, a); let top = cap_;
        // nửa trước: điểm thấp nhất của đầu ở cùng x, trên mọi độ sâu từ mép trở ra trước (không để mép che ngang mặt khi nhìn gần chính diện); nửa sau: tia dọc
        let low = 1e9; for (let zz = z - 0.04; zz < (a < 1.5 ? z + 0.32 : z - 0.03); zz += 0.012) for (let yh = -0.12; yh < Math.min(low, 0.62); yh += 0.005) if (headSDF(x, yh, zz) < CL.gap) { low = yh; break; }
        if (low < 1e8) top = Math.min(cap_, tL + nL + low - 0.01 + CL.tuck * gauss(a, 0.45));   // hệ đầu: gốc ở (0, tL + nL, 0) hệ thân; ở trước mép luồn SAU cằm (cằm che mép)
        raw.push(Math.max(CL.low, top)); }
      // co (min ±16°) rồi làm mượt (Gauss ±24°): đường mép dâng đều từ dưới cằm lên góc hàm, không gãy khúc, và không vượt lên trên đường hàm
      const ero = raw.map((_, i) => { let m = 1e9; for (let k = -8; k <= 8; k++) m = Math.min(m, raw[(i + k + NRIM) % NRIM]); return m; });
      for (let i = 0; i < NRIM; i++) { let v = 0, ws = 0; for (let k = -12; k <= 12; k++) { const w = Math.exp(-k * k / 40); v += w * ero[(i + k + NRIM) % NRIM]; ws += w; } RIM[i] = v / ws; }
      RIM[NRIM] = RIM[0]; if (opts.dbgRim) console.log("RIM", JSON.stringify(Array.from(RIM).filter((v, i) => i % 10 === 0).map((v) => +(v - tL).toFixed(3)))); }
    const clTop = (ph) => { const u = ((ph / (2 * Math.PI)) % 1 + 1) % 1 * NRIM, i = Math.floor(u), f = u - i; return RIM[i] + (RIM[i + 1] - RIM[i]) * f + 0.1 * clFold(ph, 1); };   // mép gợn rất nhẹ theo nếp
    const clRad = (k) => (s, ph) => { const t = 1 - s, top = clTop(ph), y = CL.base + (top - CL.base) * t;
      const r = (CL.rb + (clR(ph) - CL.rb) * Math.pow(t, 1.4) + clFold(ph, t)) * k;
      return [r * H, 0, -0.01 * H, (y - (CL.side + (CL.base - CL.side) * s)) * H]; };   // dy: y thật − y tuyến tính của tube
    // đường nối của ống (φ = 0 của tube) đặt ra SAU gáy: dựng với φ + π rồi xoay hình π quanh trục dọc (dz đổi dấu theo)
    const back = (fn) => (s, ph) => { const v = fn(s, ph + Math.PI); if (v.length > 2) v[2] = -v[2]; return v; };
    const clCol = (s, ph) => { const t = 1 - s, f = clFold(ph, t) / Math.max(1e-3, t); const a = 1 - 14 * Math.max(0, -f) * t - 0.25 * (1 - sstep(0.0, 0.5, t)); return [a, a, a * 0.95 + 0.05]; };
    const clLin = (s) => { const a = 0.28 + 0.24 * sstep(0.35, 0.0, s); return [a, a * 0.96, a * 0.93]; };   // lót: tối, tối dần vào trong lòng cổ áo (bóng kín) — mép lót sáng từng đọc thành "lỗ"
    const collarMeshes = [];
    for (const [k, role] of [[1, 'coat'], [0.955, 'lining']]) collarMeshes.push(add(joints.spine, tube({ y0: CL.side * H, y1: CL.base * H, nu: R(96), nv: R(14), uv: [3, 1],
      rad: back(clRad(k)), color: role === 'coat' ? (s, ph) => clCol(s, ph + Math.PI) : clLin }).rotateY(Math.PI), role, role === 'coat' ? C.coat : C.coat_lining, 'collar'));
    { const pts = []; for (let i = 0; i <= 96; i++) { const ph = Math.PI + 2 * Math.PI * i / 96, r = (clR(ph) + clFold(ph, 1)) * 0.978; pts.push([Math.sin(ph) * r * H, clTop(ph) * H, (Math.cos(ph) * r - 0.01) * H]); }
      collarMeshes.push(add(joints.spine, strandGeo(pts, () => [0.022 * H, 0.017 * H], 6, R(120)), 'coat', C.coat, 'collar')); }   // mép cuộn
    // chuyển sang hệ gốc nghỉ + trọng số da (chân: thân; mép: 0,9 đầu)
    { root.updateMatrixWorld(true); const toRoot = new THREE.Matrix4().copy(root.matrixWorld).invert().multiply(joints.spine.matrixWorld);
      const bSp = skin.bone(joints.spine), bHd = skin.bone(headG), sp0 = new THREE.Vector3(); joints.spine.getWorldPosition(sp0); root.worldToLocal(sp0);
      for (const m of collarMeshes) { joints.spine.remove(m); m.geometry.applyMatrix4(toRoot); root.add(m);
        const pa = m.geometry.attributes.position, W = [];
        for (let v = 0; v < pa.count; v++) { const yy = (pa.getY(v) - sp0.y) / H, w = CL.wHead * sstep(tL + 0.02, tL + 0.26, yy); W.push(w > 1e-4 ? [[bSp, 1 - w], [bHd, w]] : [[bSp, 1]]); }
        skinned.push([m, W]); } }
    // Khăn quàng len quấn cổ hai vòng + đuôi buông trước ngực trái.
    const loop = (y0, tilt, r0) => { const pts = []; for (let i = 0; i <= 14; i++) { const a = 2 * Math.PI * i / 14; pts.push([Math.sin(a) * r0 * H, (y0 + tilt * Math.cos(a)) * H, (Math.cos(a) * r0 * 0.95 + 0.02) * H]); } return pts; };
    const scarfRad = (w, t) => (s, a) => [w * H * (1 + 0.18 * Math.sin(s * 47)), t * H];
    for (const [y0, tilt, r0] of [[tL + 0.05, -0.05, 0.285], [tL + 0.17, -0.03, 0.272]]) {
      const pts = loop(y0, tilt, r0);
      add(joints.spine, strandGeo(pts, scarfRad(0.07, 0.042), R(8), R(44)), 'scarf', EXTRA_COLORS.ida_scarf, 'scarf');
    }
    add(joints.spine, strandGeo([[0.10, tL + 0.02, 0.30], [0.16, tL - 0.20, 0.40], [0.20, tL - 0.45, 0.44], [0.21, tL - 0.72, 0.44]].map(([x, y, z]) => [x * H, y * H, z * H]),
      (s) => [(0.085 + 0.03 * s) * H, 0.022 * H], R(10), R(24)), 'scarf', EXTRA_COLORS.ida_scarf, 'scarf');
    add(joints.spine, sculpt((x, y, z) => sph(x, y, z, [0, 0, 0], 0.07) + 0.01 * Math.abs(Math.sin(Math.atan2(x, y) * 5)), { c: [0, 0, 0], r: [0.08, 0.08, 0.08], nu: 16, nv: 10, scale: H }), 'scarf', EXTRA_COLORS.ida_scarf, 'scarf')
      .position.set(0.11 * H, (tL + 0.02) * H, 0.29 * H);
    // Khuy áo.
    for (const y of [1.72, 1.42, 1.12, 0.82]) add(joints.spine, new THREE.SphereGeometry(0.035 * H, 10, 6).scale(1, 1, 0.5), 'boots', C.boots, 'button').position.set(0.07 * H, y * H, torsoFront(y) * H);
    function torsoFront(y) { let z = 0.6; for (let it = 0; it < 30; it++) { const s = torsoSDF(0.07, y, z); if (Math.abs(s) < 1e-4) break; z -= s * 0.8; } return z + 0.008; }
    // Thắt lưng + khoá.
    add(joints.spine, tube({ y0: 0.62 * H, y1: 0.48 * H, nu: R(64), nv: 3, rad: (s, ph) => { const x = Math.sin(ph), z = Math.cos(ph); let t = 0.3; for (let it = 0; it < 25; it++) { const v = torsoSDF(x * t, 0.55, z * t); t -= v * 0.8; } return [t * H + 0.012 * H]; } }), 'boots', C.boots, 'belt');
    add(joints.spine, new THREE.TorusGeometry(0.045 * H, 0.012 * H, 6, 12).scale(1, 1.2, 1), 'tin', '#8a7a5a', 'belt').position.set(-0.03 * H, 0.55 * H, 0.39 * H);
    // Vạt áo dưới eo (4 vạt, xẻ tà sau) có nếp dọc sâu dần xuống gấu + lót.
    const hipY = ch.hipY / H;
    const waistY = 0.45, hemY = sheet.costume.coat.hem_height_H - hipY;
    const rTop = tw.waist_width / 2 * 1.10, rHem = sheet.costume.coat.hem_width_H / 2;
    const prof = (y) => { const t = (waistY - y) / (waistY - hemY); return rTop + (rHem - rTop) * (0.25 * t + 0.75 * t * t * (1.2 - 0.2 * t)); };
    for (const p of ch.coatPanels) {
      const px = p.pivot.position.x / H;
      for (const [k, role] of [[0, 'coat'], [1, 'lining']]) {
        const nu = R(26), nv = R(20); const pos = new Float32Array((nu + 1) * (nv + 1) * 3), uv = new Float32Array((nu + 1) * (nv + 1) * 2), col = new Float32Array((nu + 1) * (nv + 1) * 3); let n = 0;
        for (let j = 0; j <= nv; j++) { const t = j / nv, y = waistY + (hemY - waistY) * t;
          for (let i = 0; i <= nu; i++, n++) { const ph = p.phi0 + p.phiL * i / nu;
            const amp = 0.012 + 0.06 * t * t, fold = Math.sin(ph * 9 + 0.6 * Math.sin(y * 1.7)) * 0.7 + 0.3 * Math.sin(ph * 17 + 1.3 + y) + 0.25 * fbm(ph * 2, y * 1.5, 0, 2, 9);
            const r = prof(y) + amp * fold - k * 0.014;
            pos.set([(Math.sin(ph) * r - px) * H, (y - waistY) * H, Math.cos(ph) * r * 0.82 * H], n * 3); uv.set([ph * r * 2, t * 3], n * 2);
            const a = 1 - 0.28 * Math.max(0, -fold) * (0.3 + t); col.set([a, a, a * 0.95 + 0.05], n * 3); } }
        const g = gridGeo(pos, null, uv, col, nu, nv);
        if (k === 1) { const ix = g.index.array; for (let i = 0; i < ix.length; i += 3) { const t = ix[i + 1]; ix[i + 1] = ix[i + 2]; ix[i + 2] = t; } g.computeVertexNormals(); }
        add(p.pivot, g, role, role === 'coat' ? C.coat : C.coat_lining, 'coat_' + p.name);
      }
    }
  } else {
    const swFold = (x, y, z) => {
      const ph = Math.atan2(x, z); let f = 0;
      f += 0.013 * Math.sin(y * 26 + 2 * Math.sin(ph * 3)) * sstep(0.55, 0.1, y) * (0.6 + 0.4 * Math.sin(ph * 2 + 1));   // len chùng trên gấu
      f += 0.008 * Math.sin(ph * 7 + 0.4) * gauss(y - 0.9, 0.35);
      f += 0.006 * Math.abs(Math.sin(ph * 40)) * sstep(0.08, 0.0, y);                                                      // bo gấu
      return f;
    };
    const torsoSDF = (x, y, z) => {
      const ax = Math.abs(x);
      let d = ell(x, y, z, [0, 0.62, 0], [0.64, 0.78, 0.40]);
      d = smin(d, ell(x, y, z, [0, 1.08, 0.02], [0.62, 0.36, 0.38]), 0.2);
      d = smin(d, cap(ax, y, z, [0.10, 1.42, -0.02], [shX + 0.08, 1.24, -0.02], 0.16, 0.17), 0.2);
      d = smin(d, cap(x, y, z, [0, 1.3, 0], [0, 1.52, 0], 0.17), 0.1);
      d = smax(d, -(y + 0.07 - 0.03 * sstep(0.3, 0.6, ax)), 0.05);
      d += 0.025 * sstep(0.06, -0.06, y);   // bo gấu thắt nhẹ
      d = smax(d, y - (tL + 0.02), 0.03);    // C3: không vượt tâm khớp cổ quá bản gốc
      return d + swFold(x, y, z);
    };
    add(joints.spine, sculpt(torsoSDF, { c: [0, 0.7, 0], r: [0.8, 1.0, 0.55], nu: R(72), nv: R(58), scale: H, uv: [9, 4], color: aoCol(torsoSDF, 0.5) }), 'sweater', C.sweater, 'torso');
    add(joints.spine, tube({ y0: (tL + 0.08) * H, y1: (tL - 0.1) * H, nu: R(48), nv: 6, rad: (s, ph) => [(0.19 + 0.015 * Math.sin(Math.PI * s) + 0.004 * Math.abs(Math.sin(ph * 30))) * H, 0, 0.0] }), 'sweater', C.sweater, 'collar', 'rib');
    // Đáy quần (mông) dưới gấu áo len.
    const seat = (x, y, z) => ell(x, y, z, [0, -0.04, -0.02], [0.42, 0.22, 0.28]);
    add(joints.pelvis, sculpt(seat, { c: [0, -0.04, -0.02], r: [0.42, 0.22, 0.28], nu: R(40), nv: R(20), scale: H }), 'trousers', C.trousers, 'pelvis');
  }

  // =============================== TAY (ống da liền qua khuỷu) ===============================
  const upX = (p) => { const v = new THREE.Vector3(); p.getWorldPosition(v); return v; };
  const armDefs = [];
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1, sh = joints['shoulder_' + s], el = joints['elbow_' + s];
    const ua = P.upper_arm.length, fa = P.forearm.length;
    const o = upX(sh); const bS = skin.bone(sh), bE = skin.bone(el);
    const rU = isIda ? P.upper_arm.width_front / 2 * 1.12 : P.upper_arm.width_front / 2 * 1.32, rF = isIda ? P.forearm.width_front / 2 * 1.22 : P.forearm.width_front / 2 * 1.45;
    const radius = (yy) => { // yy: H dưới vai (âm)
      const t = -yy; if (t <= ua) return rU + (rU * 0.92 - rU) * (t / ua) ** 1.5; return rU * 0.92 + (rF - rU * 0.92) * Math.min(1, (t - ua) / fa) + (isIda ? 0.02 * sstep(ua + fa - 0.2, ua + fa, t) : 0.03 * sstep(ua + fa * 0.5, ua + fa, t));
    };
    const fold = (yy, ph) => {
      const t = -yy, ef = gauss(t - ua, 0.22);
      let f = -0.03 * ef * Math.max(0, Math.cos(ph)) * (0.5 + 0.5 * Math.sin(t * 55));            // nếp nén trong khuỷu (mặt trước)
      f += 0.014 * Math.sin(ph * 3 + t * 14 * sx) * sstep(0.1, 0.4, t) * (0.6 + 0.4 * Math.sin(t * 5 + ph));   // nếp xoắn dọc ống tay
      f += 0.012 * Math.sin(ph * 2 - t * 9) * gauss(t - 0.25, 0.2);                                  // nếp kéo từ nách
      if (!isIda) f += 0.012 * Math.sin(t * 40) * sstep(ua + fa - 0.4, ua + fa, t);               // len chùng ở cổ tay
      return f;
    };
    const mk = (t0, t1, part, bone) => {
      const g = tube({ y0: -t0 * H, y1: -t1 * H, nu: R(22), nv: R(Math.max(6, (t1 - t0) * 16)), uv: [2, (t1 - t0) * 2],
        rad: (ss, ph, y) => { const yy = y / H; return [(radius(yy) + fold(yy, ph)) * H]; },
        color: (ss, ph, x, y) => { const yy = y / H, f = fold(yy, ph); const a = 1 - 6 * Math.max(0, -f); return [a, a, a * 0.95 + 0.05]; } });
      g.translate(o.x, o.y, o.z);
      const m = add(root, g, isIda ? 'coat' : 'sweater', isIda ? C.coat : C.sweater, part);
      const S = g.attributes.s.array, W = [];
      for (let v = 0; v < S.length; v++) { const t = t0 + (t1 - t0) * S[v]; const w = sstep(ua - 0.16, ua + 0.16, t); W.push(w <= 0 ? [[bS, 1]] : w >= 1 ? [[bE, 1]] : [[bS, 1 - w], [bE, w]]); }
      skinned.push([m, W]);
      return m;
    };
    mk(0, ua, 'upper_arm'); mk(ua, ua + fa, 'forearm');
    // Chỏm vai và khuỷu (khối tròn cứng) lấp chỗ LBS xẹp.
    const capR = radius(0) * 0.96;
    add(sh, sculpt((x, y, z) => ell(x, y, z, [0, 0, 0], [capR, capR * 1.05, capR * 0.95]), { c: [0, 0, 0], r: [capR, capR, capR], nu: R(24), nv: R(14), scale: H }), isIda ? 'coat' : 'sweater', isIda ? C.coat : C.sweater, 'upper_arm_joint');
    const eR = radius(-ua) * 0.9;
    add(el, sculpt((x, y, z) => ell(x, y, z, [0, 0, 0], [eR, eR, eR]), { c: [0, 0, 0], r: [eR, eR, eR], nu: R(20), nv: R(12), scale: H }), isIda ? 'coat' : 'sweater', isIda ? C.coat : C.sweater, 'forearm_joint');
    // Cổ tay áo: Ida — măng sét lật; Cas — tay áo len trùm quá cổ tay, bo len, miệng loe.
    if (isIda) {
      add(el, tube({ y0: (-fa + 0.16) * H, y1: (-fa - 0.02) * H, nu: R(30), nv: 4, rad: (ss) => [(rF + 0.035 + 0.01 * ss) * H] }), 'coat', C.coat, 'sleeve_cuff');
      add(el, tube({ y0: (-fa - 0.02) * H, y1: (-fa + 0.10) * H, nu: R(30), nv: 2, rad: () => [(rF + 0.012) * H] }), 'lining', C.coat_lining, 'sleeve_cuff');
    } else {
      const ov = sheet.costume.sweater.sleeve_over_hand_H;
      const rr = (ss) => (rF + 0.03 + 0.012 * Math.sin(ss * Math.PI)) * H;
      add(el, tube({ y0: (-fa + 0.02) * H, y1: (-fa - ov) * H, nu: R(34), nv: R(8), rad: (ss, ph) => [rr(ss) + 0.004 * H * Math.abs(Math.sin(ph * 14))] }), 'sweater', C.sweater, 'sleeve_cuff', 'rib');
      add(el, tube({ y0: (-fa - ov) * H, y1: (-fa + 0.05) * H, nu: R(34), nv: 2, rad: (ss) => [rr(1 - ss) * 0.9] }), 'sweater', '#5e3029', 'sleeve_cuff', 'rib');
    }
    armDefs.push({ s, sx });
  }

  // =============================== BÀN TAY ===============================
  const hp = P.hand, HS = hp.scale ?? (isIda ? HAND_SCALE.ida : HAND_SCALE.cas);   // model sheet (2A) thắng hằng số
  const fingerJ = {};
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1, h = ch.hands[s]; h.hand.scale.setScalar(HS);
    const pl = hp.palm_length, pw = hp.palm_width, th = isIda ? 0.10 : 0.105;
    const palmSDF = (x, y, z) => {
      const dx = x * sx;   // dx > 0: mu bàn tay (ra ngoài), < 0: lòng bàn tay
      let d = rbox(dx, y, z, [0, -pl * 0.55, 0], [th / 2, pl * 0.42, pw / 2 * 0.98], 0.045);
      d = smin(d, cap(dx, y, z, [0, 0.03, 0], [0, -0.1, 0], 0.052, 0.05), 0.05);                           // cổ tay
      d = smin(d, ell(dx, y, z, [-0.035, -0.15, pw * 0.26], [0.05, 0.1, 0.07]), 0.05);                    // gò ngón cái
      d = smin(d, ell(dx, y, z, [-0.03, -0.24, -pw * 0.28], [0.04, 0.12, 0.06]), 0.05);                   // gò út
      for (let i = 0; i < 4; i++) d = smin(d, sph(dx, y, z, [0.022, -pl * 0.9, (0.75 - i * 0.5) * pw / 2], 0.036), 0.03); // khớp đốt ngón (mu)
      if (isIda) for (let i = 0; i < 4; i++) d -= 0.004 * gauss(Math.hypot(dx - th / 2, 0) , 0.04) * gauss(z - (0.75 - i * 0.5) * pw / 2 * (0.3 + 0.7 * (-y / pl)), 0.008) * sstep(-0.05, -0.25, y); // gân mu tay
      return d;
    };
    add(h.hand, sculpt(palmSDF, { c: [0, -pl * 0.5, 0], r: [0.1, pl * 0.8, pw * 0.7], nu: R(30), nv: R(22), scale: H, uv: [2, 2], gradE: 0.002,
      color: aoCol(palmSDF, 0.35, (x) => (x * sx < 0 ? [1.03, 0.95, 0.93] : [1, 1, 1])) }), 'skin', C.skin, 'hand');
    // Ngón: 3 đốt (gần 0,45 · giữa 0,30 · xa 0,25), gốc là nhóm ngón của khung gốc (MCP), thêm khớp PIP, DIP.
    const fr = isIda ? 0.034 : 0.036, fw = isIda ? 1.1 : 1.5;   // fw: bề rộng ngón trong mặt phẳng lòng tay / bề dày (Cas: ngón dẹt rộng → bóng cánh liền)
    const phal = (L, r0, r1, knuckle, tip) => {
      const f = (x, y, z) => { const dx = x * sx;
        let d = cap(dx * 1.08 * fw, y, z, [0, -0.006, 0], [0, -L + (tip ? r1 : 0.004), 0], r0 * fw, r1 * fw) / fw;
        if (knuckle) d = smin(d, sph(dx, y, z, [0.012, -0.004, 0], r0 * 0.95), 0.012);
        if (isIda && !tip) d = smin(d, sph(dx, y, z, [0.006, -L, 0], r1 * 1.08), 0.01);                     // đốt sưng (tuổi)
        if (tip) d = smin(d, rbox(dx, y, z, [r1 * 0.72, -L * 0.62, 0], [0.004, L * 0.3, r1 * 0.7], 0.004), 0.006);  // móng
        d += 0.0025 * Math.abs(Math.sin(y * 120)) * gauss(dx - r0, 0.01) * (isIda ? 1 : 0.4) * gauss(y + L * 0.05, 0.02); // nếp da trên khớp
        return d; };
      return sculpt(f, { c: [0, -L * 0.5, 0], r: [r0 * 1.5, L * 0.8, r0 * 1.5], nu: R(12), nv: R(10), scale: H, gradE: 0.002,
        color: aoCol(f, 0.3, (x, y, z, n) => (tip && x * sx > 0.4 * r1 && y < -L * 0.3) ? [1.06, 0.99, 0.98] : [1, 1, 1]) });
    };
    const fj = [];
    h.fingers.forEach((base, i) => {
      const fl = hp.finger_length * [0.92, 1.0, 0.95, 0.78][i], L = [fl * 0.45, fl * 0.30, fl * 0.25], rs = fr * [1.0, 1.04, 1.0, 0.88][i];
      add(base, phal(L[0], rs, rs * 0.92, true, false), 'skin', C.skin, 'hand');
      const pip = new THREE.Group(); pip.position.y = -L[0] * H; base.add(pip);
      add(pip, phal(L[1], rs * 0.92, rs * 0.84, false, false), 'skin', C.skin, 'hand');
      const dip = new THREE.Group(); dip.position.y = -L[1] * H; pip.add(dip);
      add(dip, phal(L[2], rs * 0.84, rs * 0.74, false, true), 'skin', C.skin, 'hand');
      fj.push({ base, pip, dip });
    });
    const tl = hp.thumb_length, tr = fr * 1.12;
    add(h.thumb, phal(tl * 0.55, tr, tr * 0.93, true, false), 'skin', C.skin, 'hand');
    const tip = new THREE.Group(); tip.position.y = -tl * 0.55 * H; h.thumb.add(tip);
    add(tip, phal(tl * 0.45, tr * 0.93, tr * 0.8, false, true), 'skin', C.skin, 'hand');
    fingerJ[s] = { fj, tip, sx };
  }

  // =============================== CHÂN (ống da liền qua gối) ===============================
  const th_ = P.thigh.length, sh_ = P.shin.length;
  for (const s of ['L', 'R']) {
    const sx = s === 'L' ? 1 : -1, hpJ = joints['hip_' + s], kn = joints['knee_' + s];
    const o = upX(hpJ); const bH = skin.bone(hpJ), bK = skin.bone(kn);
    const legLayer = (rad, role, color, segs, texRole) => segs.map(([t0, t1, part]) => {
      const g = tube({ y0: -t0 * H, y1: -t1 * H, nu: R(18), nv: R(Math.max(5, (t1 - t0) * 10)), uv: [2, (t1 - t0) * 2], rad: (ss, ph, y) => [rad(-y / H, ph) * H] });
      g.translate(o.x, o.y, o.z); const m = add(root, g, role, color, part, texRole);
      const S = g.attributes.s.array, W = [];
      for (let v = 0; v < S.length; v++) { const t = t0 + (t1 - t0) * S[v]; const w = sstep(th_ - 0.14, th_ + 0.14, t); W.push(w <= 0 ? [[bH, 1]] : w >= 1 ? [[bK, 1]] : [[bH, 1 - w], [bK, w]]); }
      skinned.push([m, W]); return m;
    });
    if (isIda) {
      const rad = (t, ph) => { const k = t <= th_ ? 0.20 - 0.05 * t / th_ : 0.15 - 0.055 * (t - th_) / sh_; return k + 0.02 * gauss(t - th_ - 0.35, 0.2) * Math.max(0, -Math.cos(ph)); }; // bắp chân
      legLayer(rad, 'trousers', EXTRA_COLORS.ida_stockings, [[-0.1, 0, 'thigh_joint'], [0, th_, 'thigh'], [th_, th_ + sh_, 'shin'], [th_ + sh_, th_ + sh_ + 0.05, 'shin_joint']], 'skirt');
    } else {
      const radS = (t, ph) => { const k = t <= th_ ? 0.125 - 0.03 * t / th_ : 0.095 - 0.03 * (t - th_) / sh_; return k + 0.02 * gauss(t - th_, 0.08) + 0.01 * gauss(t - th_ - 0.3, 0.15) * Math.max(0, -Math.cos(ph)); }; // gối lộ
      legLayer(radS, 'skin', C.skin, [[-0.05, th_, 'thigh_skin'], [th_, th_ + sh_, 'shin'], [th_ + sh_, th_ + sh_ + 0.03, 'shin_joint']]);
      const hem = th_ + sh_ - sheet.costume.trousers.hem_above_ankle_H;
      const radT = (t, ph) => (t <= th_ ? 0.175 - 0.02 * t / th_ : 0.155 - 0.012 * (t - th_) / (hem - th_)) + 0.008 * Math.sin(t * 30 + ph * 2) * sstep(0.2, 0.5, t) + 0.01 * sstep(hem - 0.06, hem, t);
      legLayer(radT, 'trousers', C.trousers, [[-0.12, 0, 'thigh_joint'], [0, th_, 'thigh'], [th_, hem, 'shin_trouser']]);
    }
  }
  // Váy dài (Ida) lộ dưới gấu áo khoác: ống da theo chậu + hai hông, xếp nếp dọc.
  if (isIda) {
    const pel = joints.pelvis, o = upX(pel), bP = skin.bone(pel), bL = skin.bone(joints.hip_L), bR = skin.bone(joints.hip_R);
    const yTop = 0.30, yHem = 0.42 - ch.hipY / H;   // hệ chậu (H)
    const g = tube({ y0: yTop * H, y1: yHem * H, nu: R(48), nv: R(18), uv: [5, 3],
      rad: (ss, ph) => { const r = 0.50 + 0.30 * ss ** 1.3, pleat = 0.022 * Math.sin(ph * 14 + 0.8 * Math.sin(ss * 5)) * sstep(0.1, 0.6, ss); return [(r + pleat) * H, 0, 0]; },
      color: (ss, ph) => { const f = Math.sin(ph * 14 + 0.8 * Math.sin(ss * 5)); const a = 1 - 0.18 * Math.max(0, -f) * sstep(0.1, 0.6, ss); return [a, a, a]; } });
    // độ dày trước–sau
    const pa = g.attributes.position; for (let i = 0; i < pa.count; i++) pa.setZ(i, pa.getZ(i) * 0.80);
    g.computeVertexNormals(); g.translate(o.x, o.y, o.z);
    const m = add(root, g, 'skirt', EXTRA_COLORS.ida_skirt, 'skirt');
    const pa2 = g.attributes.position, W = [];
    for (let v = 0; v < pa2.count; v++) { const x = pa2.getX(v) - o.x, y = (pa2.getY(v) - o.y) / H, rr = Math.hypot(x, pa2.getZ(v)) || 1;
      const f = 0.85 * sstep(0.1, -1.6, y), sL = Math.max(0, Math.min(1, 0.5 + 0.9 * x / rr)); W.push([[bP, 1 - f], [bL, f * sL], [bR, f * (1 - sL)]].filter((e) => e[1] > 1e-4)); }
    skinned.push([m, W]);
  }

  // =============================== ỦNG ===============================
  const ft = P.foot, ankleH = (isIda ? 0.12 : 0.10);
  for (const s of ['L', 'R']) {
    const an = joints['ankle_' + s];
    const a = ankleH, L = ft.length, Wd = ft.width / 2, toeR = isIda ? 0.12 : 0.165, shaftTop = isIda ? 0.16 : 0.02;
    const bootSDF = (x, y, z) => {
      const fh = ft.height * (isIda ? 0.85 : 0.60), yc = -a + fh * 0.5, ky = Wd / (fh * 0.5), Y = yc + (y - yc) * ky;   // mặt cắt elip dẹt theo chiều cao ủng (sheet)
      let d = ell(x, y, z, [0, -a + fh * 0.48, -0.08], [Wd * 0.85, fh * 0.5, 0.15]);
      d = smin(d, cap(x, Y, z, [0, yc, 0.0], [0, yc - 0.01, L * 0.56], Wd * 0.92, toeR) / ky, 0.08);
      d = smin(d, ell(x, y, z, [0, -a + fh * 0.42, L * 0.6], [toeR * 1.05, fh * 0.42, toeR * 1.1]), 0.06);
      d = smin(d, cap(x, y, z, [0, -a + 0.1, -0.03], [0, shaftTop, -0.03], Wd * 0.8, Wd * 0.78), 0.08);
      d = smin(d, rbox(x, y, z, [0, -a + 0.03, L * 0.25], [Wd * 0.98, 0.03, L * 0.5], 0.028), 0.01);   // đế lộ viền
      d = smax(d, -(y + a), 0.01);
      d += 0.004 * Math.sin(z * 60) * gauss(y + a - fh * 0.8, 0.05) * sstep(0.1, 0.3, z);                // nếp gập mũi ủng
      return d;
    };
    add(an, sculpt(bootSDF, { c: [0, -a + 0.14, L * 0.2], r: [Wd * 1.3, 0.4, L * 0.7], nu: R(36), nv: R(22), scale: H, uv: [3, 2],
      color: aoCol(bootSDF, 0.4, (x, y) => (y < -a + 0.06 ? [0.62, 0.6, 0.6] : [1, 1, 1])) }), 'boots', C.boots, 'foot');
  }

  // ---- da CPU: ghi bind ở tư thế nghỉ ----
  skin.captureBind();
  for (const [m, W] of skinned) skin.add(m, W);

  // ---- tư thế: gốc applyPose → ngón 3 khớp → da CPU ----
  function fingerPose(pose) {
    for (const s of ['L', 'R']) {
      const hp_ = (pose.hands || {})[s] || { spread: 0.1, curl: 0.4 }, F = fingerJ[s], sx = F.sx, curl = hp_.curl ?? 0.4, spread = hp_.spread ?? 0.1;
      F.fj.forEach(({ base, pip, dip }, i) => {
        // LƯU Ý: shared/cast.js đặt rotation.x = (1,5 − i)·0,30·spread → ngón 0 (phía +z) quay về −z: "xoè" thành KHÉP (lỗi dấu, làm cánh chim bóng thành que).
        // Ở đây đảo dấu để spread = xoè thật; biên độ theo nhân vật (Cas cần quạt rộng thành cánh).
        base.rotation.x = -(1.5 - i) * (isIda ? 0.22 : 0.27) * spread;
        base.rotation.z = -sx * (0.05 + curl * 0.95) * (1 + 0.08 * i);   // út gập hơn một chút (tự nhiên)
        pip.rotation.set(0, 0, -sx * (0.12 + curl * 1.25));
        dip.rotation.set(0, 0, -sx * (0.06 + curl * 0.75));
      });
      F.tip.rotation.set(0, 0, hp_.thumb_cross ? 0 : -sx * (0.1 + curl * 0.6));
    }
  }
  ch.setPose = (pose) => { baseSetPose(pose); fingerPose(pose);
    if (hatPivot) { const t = pose.hat_back ?? opts.hatBack ?? 0; hatPivot.rotation.x = -0.34 * t; hatPivot.position.y = (0.86 + 0.015 * t) * H; }
    root.updateMatrixWorld(true); skin.update(); };
  ch.hatPivot = hatPivot; ch.hipY = ch.hipY; ch.handScale = HS; ch.cpuSkin = skin;
  ch.setPose(sheet.poses.turnaround);
  return ch;
}

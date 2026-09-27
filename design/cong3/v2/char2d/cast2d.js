// Cine Lab · Cổng 3 v2 · Cách (2) — NHÂN VẬT TRANH 2D CÓ KHUNG XƯƠNG, NHẬN ÁNH SÁNG THẬT CỦA CẢNH.
// Cùng API với shared/cast.js: buildCharacter(sheet, opts) → { root, joints, props, hands, parts, H, sheet, setPose } + update(ch, camera).
//
// Cách dựng:
//  • KHUNG XƯƠNG, TƯ THẾ, ĐẠO CỤ: gọi thẳng shared/cast.js (không đổi độ dài bộ phận đo C3, cùng tên khớp, cùng applyPose).
//    Thân 3D gốc của shared/cast.js được giữ làm VẬT ĐỔ BÓNG VÔ HÌNH (không ghi màu, không ghi độ sâu, vẫn đổ bóng) —
//    bóng người trên tường/nền luôn đúng hình dù lớp tranh quay về máy quay. Thêm vật đổ bóng cho chi tiết mới (váy, khăn,
//    búi to, ngón 3 đốt, bàn tay phóng to) để bóng khớp với tranh.
//  • LỚP TRANH (mỗi lớp gắn vào khớp, quay về máy quay quanh trục xương, cập nhật trong update() trước MỖI MẪU):
//    – đầu, thân: "tranh theo góc nhìn" — vẽ lại bằng mã cho góc nhìn cần (bước 4° ngang / 6° dọc), lưu đệm, chọn tranh
//      gần nhất có trễ (không trộn hai tranh → không nhoè đôi nét mặt) — xem paint2d.js;
//    – tay, chân, cổ, ngón, lòng/mu bàn tay, ủng, vạt áo + váy: "dải tranh" chạy dọc chuỗi khớp (liền qua khuỷu/gối,
//      không hở khớp), bề rộng tính từ mặt cắt elip của bộ phận theo hướng nhìn; vạt áo/váy ôm theo hai chân khi bước.
//  • ÁNH SÁNG: mọi lớp dùng vật liệu của cảnh (opts.material) + normalMap suy từ bản đồ độ cao vẽ kèm → đèn khí, đèn lồng,
//    ánh điện, viền dội của cảnh chiếu lên tranh như lên khối thật.
//  • ĐỘ SÂU: mỗi điểm ảnh của lớp tranh ghi độ sâu = mặt phẳng thẻ + độ nhô (kênh alpha của normalMap) → các lớp cắt nhau
//    như khối (tay trước/sau thân đúng), không phải xếp chồng phẳng.
//  • RÌA MỀM: ngưỡng alpha đổi theo từng mẫu (0,3–0,7) → sau tích luỹ, rìa lớp tranh mềm theo độ dốc alpha vẽ sẵn.
import * as THREE from '../../shared/node_modules/three/build/three.module.js';
import { buildCharacter as buildBase } from '../../shared/cast.js';
import { paintView, paintRibbon, viewBasis, snap } from './paint2d.js';
import { DESIGNS, COLORS, ribbonDesigns, prepare } from './designs.js';

export const HAND_SCALE = { ida: 1.15, cas: 1.30 };   // bàn tay + ngón (không thuộc C3; trần cho phép 1,3×)
const PROP_PARTS = new Set(['lantern', 'lantern_glass', 'flame', 'ladder', 'pole']);
const SHADOW_ONLY = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false, side: THREE.DoubleSide });
const U_AT = { value: 0.5 };                                      // ngưỡng alpha theo mẫu (chung mọi lớp tranh)
const VIEW_STEP = { yaw: 4 * Math.PI / 180, pitch: 6 * Math.PI / 180 };
let SEQ = 0;                                                      // bộ đếm lời gọi update (dãy Weyl → trộn theo mẫu)
const frac = (x) => x - Math.floor(x);

function defaultMaterial(role, color, part, extra = {}) {
  if (role === 'flame') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff2d0').multiplyScalar(20) });
  if (role === 'glass') return new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc56b').multiplyScalar(3), transparent: true, opacity: 0.6, depthWrite: false });
  return new THREE.MeshLambertMaterial({ color, side: THREE.DoubleSide, ...extra });
}

// Vá shader vật liệu của cảnh: ghi độ sâu từng điểm ảnh theo độ nhô + ngưỡng alpha theo mẫu. Giữ nguyên vá của cảnh (s5).
function patchCard(mat) {
  const prev = mat.onBeforeCompile, prevKey = mat.customProgramCacheKey;
  const had = prev && prev !== THREE.Material.prototype.onBeforeCompile;
  mat.onBeforeCompile = (sh, r) => {
    if (had) prev.call(mat, sh, r);
    sh.uniforms.uAT = U_AT;
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute vec2 aBulge; varying vec2 vBulge;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\n  vBulge = aBulge;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec2 vBulge; uniform float uAT; uniform mat4 projectionMatrix;')
      .replace('#include <alphatest_fragment>', 'if (diffuseColor.a < uAT) discard;')
      .replace(/}\s*$/, `  { float hb = texture2D(normalMap, vNormalMapUv).a;
    vec3 pv = -vViewPosition + normalize(vViewPosition) * (vBulge.x + vBulge.y * hb);
    vec4 cp = projectionMatrix * vec4(pv, 1.0); gl_FragDepth = clamp(cp.z / cp.w * 0.5 + 0.5, 0.0, 1.0); }
}`);
  };
  const base = had && prevKey ? prevKey.call(mat) : '';
  mat.customProgramCacheKey = () => base + '|card2d-v1';
  mat.needsUpdate = true;
  return mat;
}

// ---------------- lưới thẻ động (dải hoặc tứ giác) ----------------
class CardMesh {
  constructor(nRows, material, name) {
    const g = new THREE.BufferGeometry(), nv = nRows * 2;
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(nv * 3), 3).setUsage(THREE.DynamicDrawUsage));
    g.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(nv * 3), 3).setUsage(THREE.DynamicDrawUsage));
    g.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(nv * 2), 2).setUsage(THREE.DynamicDrawUsage));
    g.setAttribute('aBulge', new THREE.BufferAttribute(new Float32Array(nv * 2), 2).setUsage(THREE.DynamicDrawUsage));
    const idx = []; for (let k = 0; k < nRows - 1; k++) { const a = 2 * k, b = a + 1, c = a + 2, d = a + 3; idx.push(a, b, c, b, d, c); }
    g.setIndex(idx);
    g.boundingSphere = new THREE.Sphere(new THREE.Vector3(), 1e4);
    this.mesh = new THREE.Mesh(g, material); this.mesh.name = name; this.mesh.frustumCulled = false;
    this.mesh.userData.noG = true; this.mesh.userData.card2d = true; this.mesh.castShadow = false; this.mesh.receiveShadow = false;
    this.n = nRows;
  }
  // rows: [{L, R (Vector3), nrm (Vector3), v, b0, b1}]; flipU: đảo u (giữ chiều quấn tam giác)
  write(rows, flipU = false) {
    const g = this.mesh.geometry, P = g.attributes.position.array, N = g.attributes.normal.array, T = g.attributes.uv.array, B = g.attributes.aBulge.array;
    for (let k = 0; k < this.n; k++) {
      const r = rows[Math.min(k, rows.length - 1)], o = 6 * k, t = 4 * k;
      P[o] = r.L.x; P[o + 1] = r.L.y; P[o + 2] = r.L.z; P[o + 3] = r.R.x; P[o + 4] = r.R.y; P[o + 5] = r.R.z;
      N[o] = N[o + 3] = r.nrm.x; N[o + 1] = N[o + 4] = r.nrm.y; N[o + 2] = N[o + 5] = r.nrm.z;
      T[t] = flipU ? 1 : 0; T[t + 1] = r.v; T[t + 2] = flipU ? 0 : 1; T[t + 3] = r.v;
      B[t] = r.b0; B[t + 1] = r.b1; B[t + 2] = r.b0; B[t + 3] = r.b1;
    }
    for (const a of ['position', 'normal', 'uv', 'aBulge']) g.attributes[a].needsUpdate = true;
  }
}

const _v = () => new THREE.Vector3();
const tmpM = new THREE.Matrix4();
// Điểm và trục của một khung (Object3D) trong hệ gốc nhân vật.
function frameIn(o, rootInv) {
  tmpM.multiplyMatrices(rootInv, o.matrixWorld); const e = tmpM.elements;
  return { o: new THREE.Vector3(e[12], e[13], e[14]), x: new THREE.Vector3(e[0], e[1], e[2]), y: new THREE.Vector3(e[4], e[5], e[6]), z: new THREE.Vector3(e[8], e[9], e[10]) };
}
const at = (F, x, y, z) => F.o.clone().addScaledVector(F.x, x).addScaledVector(F.y, y).addScaledVector(F.z, z);

// Dải tranh qua các hàng {c, A, B, v, cover?, coverR?}: bề rộng = hình chiếu mặt cắt elip (A, B) lên phương ngang màn hình.
function ribbonRows(rows, cam) {
  const out = [], n = rows.length;
  for (let k = 0; k < n; k++) {
    const r = rows[k];
    const p = rows[Math.max(0, k - 1)].c, q = rows[Math.min(n - 1, k + 1)].c;
    const T = _v().subVectors(q, p); if (T.lengthSq() < 1e-12) T.set(0, -1, 0); T.normalize();
    const V = _v().subVectors(cam, r.c).normalize();
    let S = _v().crossVectors(T, V);
    if (S.lengthSq() < 1e-8) S = _v().crossVectors(T, Math.abs(T.y) < 0.9 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(1, 0, 0));
    S.normalize();
    let hw = Math.hypot(r.A.dot(S), r.B.dot(S));
    const Vp = V.clone().addScaledVector(T, -V.dot(T)); if (Vp.lengthSq() < 1e-8) Vp.copy(V); Vp.normalize();
    let bulge = Math.hypot(r.A.dot(Vp), r.B.dot(Vp));
    if (r.cover) for (const cq of r.cover) { const d = _v().subVectors(cq, r.c); hw = Math.max(hw, Math.abs(d.dot(S)) + r.coverR); bulge = Math.max(bulge, d.dot(Vp) + r.coverR); }
    const nrm = _v().crossVectors(S, T).normalize();
    out.push({ L: r.c.clone().addScaledVector(S, -hw), R: r.c.clone().addScaledVector(S, hw), nrm, v: r.v, b0: 0, b1: bulge, S });
  }
  return out;
}

// ---------------- tranh theo góc nhìn (đầu, thân) ----------------
class ViewCard {
  constructor(key, design, joint, Hm, res, mkMat) {
    this.key = key; this.design = design; this.joint = joint; this.Hm = Hm; this.res = res; this.cache = new Map(); this.order = [];
    this.card = new CardMesh(2, null, key); this.card.mesh.visible = false; this.mkMat = mkMat; this.mat = null;
  }
  variant(yi, pi) {
    const k = yi + ',' + pi;
    if (this.cache.has(k)) return this.cache.get(k);
    const V = viewBasis(yi * VIEW_STEP.yaw, pi * VIEW_STEP.pitch);
    const f = this.design.frame, r = paintView(this.design, V, { c: f.c, size: f.size, W: this.res });
    const cx = f.c[0] * V.R[0] + f.c[1] * V.R[1] + f.c[2] * V.R[2], cy = f.c[0] * V.U[0] + f.c[1] * V.U[1] + f.c[2] * V.U[2];
    const vr = { V, map: r.map, nmap: r.nmap, zmin: r.zmin, zmax: r.zmax, cx, cy };
    this.cache.set(k, vr); this.order.push(k);
    if (this.order.length > 18) { const old = this.order.shift(); const o = this.cache.get(old); o.map.dispose(); o.nmap.dispose(); this.cache.delete(old); }
    if (!this.mat) { this.mat = this.mkMat(vr.map, vr.nmap); this.card.mesh.material = this.mat; }
    return vr;
  }
  update(rootInv, camW, rnd) {
    const F = frameIn(this.joint, rootInv), Hm = this.Hm;
    // hướng máy quay trong hệ khớp (đơn vị H), tính từ tâm khung tranh
    const inv = new THREE.Matrix4().copy(this.joint.matrixWorld).invert();
    const cl = camW.clone().applyMatrix4(inv).multiplyScalar(1 / Hm);
    const c = this.design.frame.c; const d = new THREE.Vector3(cl.x - c[0], cl.y - c[1], cl.z - c[2]).normalize();
    const yaw = Math.atan2(d.x, d.z), pitch = Math.asin(THREE.MathUtils.clamp(d.y, -1, 1));
    const fy = yaw / VIEW_STEP.yaw, fp = THREE.MathUtils.clamp(pitch, -1.0, 1.0) / VIEW_STEP.pitch;
    // chọn tranh gần nhất, có trễ (hysteresis): máy tĩnh (kể cả rung khẩu độ DOF) → một tranh duy nhất, không nhoè đôi;
    // máy/nhân vật chuyển động → đổi tranh khi lệch quá 0,75 bước (4° / 6°) — nét lệch ~1 px ở cỡ khung đi bộ.
    if (!this.cur || Math.abs(fy - this.cur[0]) > 0.75 || Math.abs(fp - this.cur[1]) > 0.75) this.cur = [Math.round(fy), Math.round(fp)];
    const [yi, pi] = this.cur;
    const vr = this.variant(yi, pi); this.card.mesh.visible = true;
    this.mat.map = vr.map; this.mat.normalMap = vr.nmap;
    const V = vr.V, s = this.design.frame.size / 2;
    const toW = (x, y) => at(F, (x * V.R[0] + y * V.U[0]) * Hm, (x * V.R[1] + y * V.U[1]) * Hm, (x * V.R[2] + y * V.U[2]) * Hm);
    const nrm = _v().copy(F.x).multiplyScalar(V.F[0]).addScaledVector(F.y, V.F[1]).addScaledVector(F.z, V.F[2]).normalize();
    const b0 = vr.zmin * Hm, b1 = (vr.zmax - vr.zmin) * Hm;
    this.card.write([
      { L: toW(vr.cx - s, vr.cy - s), R: toW(vr.cx + s, vr.cy - s), nrm, v: 0, b0, b1 },
      { L: toW(vr.cx - s, vr.cy + s), R: toW(vr.cx + s, vr.cy + s), nrm, v: 1, b0, b1 },
    ]);
  }
}

// ---------------- dựng nhân vật ----------------
export function buildCharacter(sheet, opts = {}) {
  const isIda = sheet.id.startsWith('CHR-ida'), who = isIda ? 'ida' : 'cas';
  const Hm = sheet.H_m, P = sheet.parts, J = sheet.joints_default;
  const userMat = opts.material || defaultMaterial;
  const detail = opts.detail ?? 24, hi = detail >= 34;
  // 1) khung xương + đạo cụ + thân 3D gốc (thân → vật đổ bóng vô hình; đạo cụ → vật liệu của cảnh)
  const base = buildBase(sheet, { detail: 14, material: (role, color, part) => (PROP_PARTS.has(part) ? userMat(role, color, part) : SHADOW_ONLY) });
  const { root, joints } = base;
  const proxies = [];
  const markProxy = (o) => o.traverse((m) => { if (m.isMesh && m.material === SHADOW_ONLY) { m.userData.proxy = true; m.castShadow = true; m.receiveShadow = false; proxies.push(m); } });
  markProxy(root);
  const addProxy = (parent, geo, pos, rot, scl) => { const m = new THREE.Mesh(geo, SHADOW_ONLY); if (pos) m.position.set(...pos); if (rot) m.rotation.set(...rot); if (scl) m.scale.set(...scl); parent.add(m); m.userData.proxy = true; m.castShadow = true; proxies.push(m); return m; };
  const HS = HAND_SCALE[who];

  // 2) bàn tay: phóng to, ngón 3 đốt (vật đổ bóng khớp với tranh)
  const fingerRig = {};
  for (const s of ['L', 'R']) {
    const h = base.hands[s]; h.hand.scale.setScalar(HS);
    const fr = [], hp = P.hand;
    h.fingers.forEach((f, i) => {
      for (const c of f.children) if (c.isMesh) c.visible = false;
      const fl = hp.finger_length * Hm * [0.92, 1.0, 0.95, 0.78][i], rf = (isIda ? 0.036 : 0.038) * Hm * [1, 1, 0.97, 0.9][i];
      const L = [0.45, 0.30, 0.25].map((k) => k * fl);
      const mid = new THREE.Group(); mid.position.y = -L[0]; f.add(mid);
      const dist = new THREE.Group(); dist.position.y = -L[1]; mid.add(dist);
      const tip = new THREE.Object3D(); tip.position.y = -L[2]; dist.add(tip);
      [[f, L[0], rf], [mid, L[1], rf * 0.94], [dist, L[2], rf * 0.86]].forEach(([par, l, r]) => addProxy(par, new THREE.CapsuleGeometry(r, Math.max(1e-4, l - r), 3, 8), [0, -l / 2, 0]));
      fr.push({ base: f, mid, dist, tip, r: rf, L });
    });
    for (const c of h.thumb.children) if (c.isMesh) c.visible = false;
    const tl = hp.thumb_length * Hm, rt = (isIda ? 0.042 : 0.044) * Hm;
    const tmid = new THREE.Group(); tmid.position.y = -tl * 0.55; h.thumb.add(tmid);
    const ttip = new THREE.Object3D(); ttip.position.y = -tl * 0.45; tmid.add(ttip);
    addProxy(h.thumb, new THREE.CapsuleGeometry(rt, tl * 0.55 - rt, 3, 8), [0, -tl * 0.275, 0]);
    addProxy(tmid, new THREE.CapsuleGeometry(rt * 0.9, tl * 0.45 - rt * 0.9, 3, 8), [0, -tl * 0.225, 0]);
    fingerRig[s] = { fingers: fr, thumb: { base: h.thumb, mid: tmid, tip: ttip, r: rt }, hand: h.hand, sx: h.sx };
  }

  // 3) vật đổ bóng cho chi tiết thứ cấp
  const head = joints.head, spine = joints.spine, pelvis = joints.pelvis;
  head.traverse((m) => { // búi/quả bông cũ → thay bằng khối khớp với tranh
    if (!m.isMesh) return;
    if (isIda && m.userData.part === 'hair' && m.geometry.type === 'SphereGeometry' && m.position.z < 0 && m.geometry.parameters.radius < 0.2 * Hm * 1.5 && m.scale.x === 1) { m.position.set(0, 0.50 * Hm, -0.52 * Hm); m.scale.set(0.26 / (sheet.costume.hair.bun_diameter_H / 2), 0.215 / (sheet.costume.hair.bun_diameter_H / 2), 0.20 / (sheet.costume.hair.bun_diameter_H / 2)); }
  });
  if (isIda) {
    const hipY = base.hipY, hemY = sheet.costume.coat.hem_height_H * Hm - hipY, botY = 0.10 - hipY;
    // váy: nón cụt từ gấu áo tới gần mắt cá (bóng người đọc thành váy dài)
    addProxy(pelvis, new THREE.CylinderGeometry(0.64 * Hm, 0.74 * Hm, hemY - botY + 0.04, 20, 1), [0, (hemY + botY) / 2, 0], null, [1, 1, 0.85]);
    // khăn choàng quanh vai + nút trước ngực
    addProxy(spine, new THREE.SphereGeometry(1, 20, 12), [0, 1.74 * Hm, -0.02 * Hm], null, [0.74 * Hm, 0.28 * Hm, 0.47 * Hm]);
    addProxy(spine, new THREE.SphereGeometry(1, 12, 8), [0, 1.30 * Hm, 0.40 * Hm], null, [0.11 * Hm, 0.09 * Hm, 0.08 * Hm]);
  } else {
    head.traverse((m) => { if (m.isMesh && m.userData.part === 'bobble') { m.position.y = 1.20 * Hm - 0.66 * Hm; m.scale.setScalar(0.205 / (sheet.costume.cap.bobble_diameter_H / 2));
      // bóng quả bông phải "xù len" (khác búi tóc trơn): gai sợi ngẫu nhiên trên khối
      const g = new THREE.IcosahedronGeometry(sheet.costume.cap.bobble_diameter_H / 2 * Hm, 3), pa = g.attributes.position;
      for (let i = 0; i < pa.count; i++) { const x = pa.getX(i), y = pa.getY(i), z = pa.getZ(i); const f = 1 + 0.16 * Math.max(0, Math.sin(x * 900 + 1) * Math.sin(y * 870 + 2) * Math.sin(z * 910 + 3)) ** 0.5; pa.setXYZ(i, x * f, y * f, z * f); }
      g.computeVertexNormals(); m.geometry = g; } });
    for (const x of [1, -1]) addProxy(head, new THREE.SphereGeometry(1, 10, 8), [0.475 * x * Hm, 0.46 * Hm, -0.06 * Hm], [0, -0.62 * x, 0], [0.05 * Hm, 0.155 * Hm, 0.115 * Hm]); // tai vểnh
  }

  // 4) vật liệu lớp tranh
  const mkMat = (map, nmap, part) => patchCard(userMat('card', '#ffffff', part || 'card2d', { map, normalMap: nmap, normalScale: new THREE.Vector2(1, 1), side: THREE.DoubleSide }));
  const cards = [];

  // 5) đầu, thân: tranh theo góc nhìn
  const D = DESIGNS[who];
  const headD = prepare(D.head(), snap), torsoD = prepare(D.torso(), snap);
  const vHead = new ViewCard('head2d', headD, head, Hm, isIda ? (hi ? 1024 : 512) : (hi ? 768 : 512), (a, b) => mkMat(a, b, 'head'));
  const vTorso = new ViewCard('torso2d', torsoD, spine, Hm, hi ? 1024 : 512, (a, b) => mkMat(a, b, 'torso'));
  root.add(vHead.card.mesh); root.add(vTorso.card.mesh);

  // 6) dải tranh
  const RD = ribbonDesigns(isIda, hi, sheet);
  const texCache = {};
  const ribTex = (k) => (texCache[k] || (texCache[k] = paintRibbon(RD[k])));
  const ribbons = [];
  const addRibbon = (name, texKey, nRows, rowsFn, opt = {}) => {
    const t = ribTex(texKey), mat = mkMat(t.map, t.nmap, name);
    const cm = new CardMesh(nRows, mat, name); root.add(cm.mesh);
    const r = { name, cm, rowsFn, texKey, mat, ...opt }; ribbons.push(r); return r;
  };
  const Hs = (x) => x * Hm;
  // chuỗi hàng từ danh sách {j: tên khớp | Object3D, y (H), r (H), d (tỷ lệ sâu), sc (nhân tỷ lệ khung)}
  const chainRows = (defs) => {
    let acc = 0; const vs = [0];
    for (let k = 1; k < defs.length; k++) { acc += Math.abs(defs[k].len ?? 0.1); vs.push(acc); }
    return (rootInv) => defs.map((d, k) => {
      const F = frameIn(typeof d.j === 'string' ? joints[d.j] : d.j, rootInv);
      const sx = d.sc ? 1 : 1 / F.x.length(), sz = d.sc ? 1 : 1 / F.z.length();
      const c = at(F, 0, Hs(d.y), Hs(d.z || 0));
      return { c, A: F.x.clone().multiplyScalar(Hs(d.r) * sx), B: F.z.clone().multiplyScalar(Hs(d.r) * (d.d ?? 1) * sz), v: vs[k] / acc };
    });
  };
  // cánh tay (liền vai → khuỷu → cổ tay; Cas: tay áo trùm qua cổ tay)
  for (const s of ['L', 'R']) {
    const ua = P.upper_arm.length, fa = P.forearm.length;
    const defs = isIda ? [
      { j: 'shoulder_' + s, y: 0.07, r: 0.19 }, { j: 'shoulder_' + s, y: 0, r: 0.19, len: 0.07 }, { j: 'shoulder_' + s, y: -ua * 0.5, r: 0.18, len: ua * 0.5 },
      { j: 'shoulder_' + s, y: -ua, r: 0.165, len: ua * 0.5 }, { j: 'elbow_' + s, y: -fa * 0.12, r: 0.155, len: fa * 0.12 }, { j: 'elbow_' + s, y: -fa * 0.55, r: 0.15, len: fa * 0.43 },
      { j: 'elbow_' + s, y: -fa * 0.97, r: 0.165, len: fa * 0.42 }, { j: 'elbow_' + s, y: -fa * 1.04, r: 0.17, len: fa * 0.07 },
    ] : [
      { j: 'shoulder_' + s, y: 0.07, r: 0.16 }, { j: 'shoulder_' + s, y: 0, r: 0.16, len: 0.07 }, { j: 'shoulder_' + s, y: -ua * 0.5, r: 0.155, len: ua * 0.5 },
      { j: 'shoulder_' + s, y: -ua, r: 0.15, len: ua * 0.5 }, { j: 'elbow_' + s, y: -fa * 0.12, r: 0.145, len: fa * 0.12 }, { j: 'elbow_' + s, y: -fa * 0.55, r: 0.145, len: fa * 0.43 },
      { j: 'elbow_' + s, y: -fa, r: 0.15, len: fa * 0.45 }, { j: base.hands[s].hand, y: -0.06 / HS, r: 0.155, len: 0.06 }, { j: base.hands[s].hand, y: -sheet.costume.sweater.sleeve_over_hand_H / HS, r: 0.16, len: 0.12 },
    ];
    addRibbon('arm_' + s, 'sleeve', defs.length, chainRows(defs));
  }
  // chân
  for (const s of ['L', 'R']) {
    const th = P.thigh.length, sh = P.shin.length;
    const defs = isIda ? [
      { j: 'hip_' + s, y: 0.1, r: 0.2 }, { j: 'hip_' + s, y: -th * 0.5, r: 0.18, len: th * 0.5 + 0.1 }, { j: 'hip_' + s, y: -th, r: 0.16, len: th * 0.5 },
      { j: 'knee_' + s, y: -sh * 0.5, r: 0.135, len: sh * 0.5 }, { j: 'knee_' + s, y: -sh * 0.98, r: 0.12, len: sh * 0.48 },
    ] : [
      { j: 'hip_' + s, y: 0.08, r: 0.16 }, { j: 'hip_' + s, y: -th * 0.5, r: 0.15, len: th * 0.5 + 0.08 }, { j: 'hip_' + s, y: -th, r: 0.14, len: th * 0.5 },
      { j: 'knee_' + s, y: -sh * 0.45, r: 0.135, len: sh * 0.45 }, { j: 'knee_' + s, y: -(sh - sheet.costume.trousers.hem_above_ankle_H), r: 0.135, len: sh * 0.55 - sheet.costume.trousers.hem_above_ankle_H },
      { j: 'knee_' + s, y: -(sh - sheet.costume.trousers.hem_above_ankle_H) - 0.005, r: 0.1, len: 0.005 }, { j: 'knee_' + s, y: -sh, r: 0.095, len: sheet.costume.trousers.hem_above_ankle_H },
    ];
    // v tại gấu quần của Cas phải khớp tranh (0,80)
    addRibbon('leg_' + s, 'leg', defs.length, chainRows(defs));
    // ủng: cổ ủng (đứng) + thân ủng (gót → mũi)
    const ft = P.foot, ankH = (isIda ? 0.12 : 0.10);
    addRibbon('shaft_' + s, 'shaft', 3, chainRows([{ j: 'ankle_' + s, y: 0.36, r: ft.width * 0.5 }, { j: 'ankle_' + s, y: 0.1, r: ft.width * 0.52, len: 0.26 }, { j: 'ankle_' + s, y: -ankH + ft.height * 0.3, r: ft.width * 0.55, len: 0.2 }]));
    addRibbon('boot_' + s, 'boot', 4, (rootInv) => {
      const F = frameIn(joints['ankle_' + s], rootInv), L = ft.length;
      const pts = [[-0.24 * L, -ankH + ft.height * 0.5], [0.1 * L, -ankH + ft.height * 0.5], [0.45 * L, -ankH + ft.height * 0.45], [0.74 * L, -ankH + ft.height * 0.36]];
      const ws = [0.9, 1.0, 1.0, 0.8];
      return pts.map(([zz, yy], k) => ({ c: at(F, 0, Hs(yy), Hs(zz)), A: F.x.clone().normalize().multiplyScalar(Hs(ft.width * 0.5 * ws[k])), B: F.y.clone().normalize().multiplyScalar(Hs(ft.height * 0.5 * (k === 3 ? 0.8 : 1))), v: k / 3 }));
    });
  }
  // cổ
  addRibbon('neck', 'neck', 3, chainRows([{ j: 'neck', y: -0.08, r: P.neck.width_front * 0.55 }, { j: 'neck', y: P.neck.length * 0.6, r: P.neck.width_front * 0.52, len: P.neck.length * 0.68 }, { j: 'head', y: 0.22, r: P.neck.width_front * 0.5, len: 0.34 }]));
  // vạt áo + váy (Ida): ôm hông, theo hai chân khi bước
  if (isIda) {
    const hipY = base.hipY / Hm, hem = sheet.costume.coat.hem_height_H - hipY, bot = 0.10 / Hm - hipY;
    const lv = [0.55, 0.30, 0.0, -0.4, -0.8, -1.2, -1.6, hem, hem - 0.01, (hem + bot) / 2, bot];
    const aa = [0.58, 0.64, 0.70, 0.78, 0.85, 0.92, 0.99, 1.05, 0.64, 0.69, 0.74].map((a, k) => a * (k < 8 ? 1 : 1));
    const bb = aa.map((a, k) => a * (k < 8 ? 0.82 : 0.85));
    const vHem = 0.8, vv = lv.map((y, k) => (k < 8 ? vHem * (lv[0] - y) / (lv[0] - hem) : vHem + (1 - vHem) * (hem - y) / (hem - bot)));
    const th = P.thigh.length, sh = P.shin.length, legR = 0.2;
    const legPt = (s, drop, rootInv) => { const F = drop <= th ? frameIn(joints['hip_' + s], rootInv) : frameIn(joints['knee_' + s], rootInv); return at(F, 0, -Hs(drop <= th ? drop : Math.min(sh, drop - th)), 0); };
    addRibbon('skirt', 'skirt', lv.length, (rootInv) => {
      const F = frameIn(pelvis, rootInv);
      return lv.map((y, k) => {
        const w = Math.min(1, Math.max(0, (0.3 - y) / 1.3)) * 0.85;
        const pl = legPt('L', -y, rootInv), pr = legPt('R', -y, rootInv), mid = pl.clone().add(pr).multiplyScalar(0.5);
        const c0 = at(F, 0, Hs(y), 0), c = c0.clone().lerp(mid, w);
        return { c, A: F.x.clone().multiplyScalar(Hs(aa[k])), B: F.z.clone().multiplyScalar(Hs(bb[k])), v: vv[k], cover: y < 0 ? [pl, pr] : null, coverR: Hs(legR + 0.08) };
      });
    });
  }
  // bàn tay: lòng/mu (chọn theo phía nhìn), 4 ngón 3 đốt, ngón cái 2 đốt
  const hands2d = {};
  for (const s of ['L', 'R']) {
    const rig = fingerRig[s], hp = P.hand, h = rig.hand;
    // lòng bàn tay nằm trong mặt phẳng y–z của khung tay: bề rộng theo z, bề dày theo x (khung tay đã mang tỷ lệ HS)
    const palmY = [0.03, -hp.palm_length * 0.5, -hp.palm_length * 0.97], palmW = [0.46, 0.52, 0.5];
    const pr = addRibbon('palm_' + s, 'palm', 3, (rootInv) => { const F = frameIn(h, rootInv);
      return palmY.map((y, k) => ({ c: at(F, 0, Hs(y), 0), A: F.z.clone().multiplyScalar(Hs(hp.palm_width * palmW[k])), B: F.x.clone().multiplyScalar(Hs(hp.palm_width * palmW[k] * 0.34)), v: k / 2 })); },
      { hand: s, alt: 'back' });
    const fr = rig.fingers.map((f, i) => addRibbon('finger_' + s + i, 'finger', 5, (rootInv) => {
      const ext = 0.04 * Hm, Ls = [ext, f.L[0], f.L[1], f.L[2]], tot = Ls.reduce((a, b) => a + b), rr = [1.04, 1.0, 0.94, 0.86, 0.78];
      const Fs = [f.base, f.base, f.mid, f.dist, f.tip].map((o) => frameIn(o, rootInv));
      let acc = 0;
      return Fs.map((F, k) => { if (k) acc += Ls[k - 1];
        return { c: k === 0 ? at(F, 0, ext, 0) : F.o.clone(), A: F.x.clone().multiplyScalar(f.r * rr[k]), B: F.z.clone().multiplyScalar(f.r * rr[k] * 1.1), v: acc / tot }; });
    }, { hand: s, alt: 'fingerBack' }));
    const t = rig.thumb;
    const trb = addRibbon('thumb_' + s, 'finger', 4, (rootInv) => {
      const tl = hp.thumb_length * Hm, Fb = frameIn(t.base, rootInv), Fm = frameIn(t.mid, rootInv), Ft = frameIn(t.tip, rootInv), r = t.r;
      return [[at(Fb, 0, 0.03 * Hm, 0), Fb, 0], [at(Fb, 0, -tl * 0.25, 0), Fb, 0.25], [Fm.o.clone(), Fm, 0.6], [Ft.o.clone(), Ft, 1]]
        .map(([c, F, v], k) => ({ c, A: F.x.clone().multiplyScalar(r * [1.1, 1.05, 0.95, 0.85][k]), B: F.z.clone().multiplyScalar(r * [1.15, 1.1, 1.0, 0.9][k]), v }));
    }, { hand: s, alt: 'fingerBack' });
    hands2d[s] = { palm: pr, fingers: fr, thumb: trb };
  }

  const ch = { root, joints, parts: base.parts, props: base.props, hands: base.hands, coatPanels: base.coatPanels, H: base.H, sheet, hipY: base.hipY,
    _2d: { who, vHead, vTorso, ribbons, proxies, fingerRig, texCache, RD, mkMat, HS } };
  // tư thế: dùng applyPose gốc, rồi chia độ gập ngón cho 3 đốt (tổng gập như bản gốc, nhưng cong mềm)
  ch.setPose = (pose) => {
    base.setPose(pose);
    for (const s of ['L', 'R']) {
      const hp = (pose.hands || {})[s] || { spread: 0.1, curl: 0.4 }, rig = fingerRig[s], sx = rig.sx, curl = hp.curl ?? 0.4;
      rig.fingers.forEach((f) => { f.base.rotation.z = -sx * curl * 0.75; f.mid.rotation.set(0, 0, -sx * curl * 1.0); f.dist.rotation.set(0, 0, -sx * curl * 0.7); });
      rig.thumb.mid.rotation.set(0, 0, hp.thumb_cross ? 0 : -sx * curl * 0.6);
      // thumb_cross (chim bóng): hai ngón cái nghiêng vào giữa (+y khung tay = phía tay kia) cho chạm đầu nhau → MỘT cái đầu chim,
      // đốt ngoài hơi quặp làm mỏ. Chỉ đổi khớp ngón (không thuộc khung xương đo C3).
      if (hp.thumb_cross) { rig.thumb.base.rotation.x -= 0.62; rig.thumb.mid.rotation.x = -0.35; }
    }
    root.updateMatrixWorld(true);
  };
  ch.setPose(sheet.poses.turnaround);
  return ch;
}

// Gọi trước mỗi mẫu: dựng lại mọi lớp tranh theo máy quay hiện tại.
export function update(ch, camera) {
  const X = ch._2d; if (!X || !camera) return;
  const { root } = ch;
  root.updateMatrixWorld(true);
  const rootInv = new THREE.Matrix4().copy(root.matrixWorld).invert();
  const camW = new THREE.Vector3(); camera.updateMatrixWorld(); camera.getWorldPosition(camW);
  const camL = camW.clone().applyMatrix4(rootInv);
  SEQ++;
  const rnd = [frac(SEQ * 0.6180339887 + 0.13), frac(SEQ * 0.7548776662 + 0.41)];
  U_AT.value = 0.3 + 0.4 * frac(SEQ * 0.5698402910 + 0.27);
  X.vHead.update(rootInv, camW, rnd); X.vTorso.update(rootInv, camW, rnd);
  // lòng hay mu bàn tay quay về máy (lòng bàn tay nhìn theo −sx·x của khung tay)
  const palmSide = {};
  for (const s of ['L', 'R']) { const F = frameIn(X.fingerRig[s].hand, rootInv); const n = F.x.clone().normalize().multiplyScalar(-X.fingerRig[s].sx); palmSide[s] = n.dot(_v().subVectors(camL, F.o)) > 0; }
  for (const r of X.ribbons) {
    const rows = ribbonRows(r.rowsFn(rootInv), camL);
    if (r.alt) { const key = palmSide[r.hand] ? r.texKey : r.alt; const t = X.texCache[key] || (X.texCache[key] = paintRibbon(X.RD[key])); r.mat.map = t.map; r.mat.normalMap = t.nmap; }
    r.cm.write(rows);
  }
  // cờ bóng (cảnh có thể bật castShadow cho mọi mesh sau khi dựng)
  root.traverse((o) => { if (!o.isMesh) return; if (o.userData.card2d) { o.castShadow = false; o.receiveShadow = false; } else if (o.userData.proxy) { o.castShadow = true; o.receiveShadow = false; } });
}

export { buildLantern, buildLadder } from '../../shared/cast.js';

// R&D City Timelapse 3D — cảnh thử Amsterdam 30 s (lab, độc lập với design/).
// Toà nhà = một BufferGeometry duy nhất; mỗi đỉnh mang năm xây (aYear), chiều cao (aH), cờ đỉnh mái (aTop):
// vertex shader nâng toà nhà theo uYear, nên 76 nghìn toà nhà chỉ tốn một lệnh vẽ (+ một lệnh cho bóng).
// Chữ trên hình (bộ đếm, thẻ) vẽ ở lớp 2D sau khi chụp khung WebGL; đo tương phản WCAG trên điểm ảnh thật.
import * as THREE from '/three/build/three.module.js';

const P = window.TL = window.TL || {};
const W = P.W || 960, H = P.H || 540, FPS = 24, N = P.frames || 720;
const S = H / 1080;                                   // hệ số cỡ chữ so với khung 1080p

// ---------- thời gian → năm, máy quay ----------
// 4 yếu tố ngôn ngữ hình (bổ sung chủ dự án 15/10 22:47):
//  E2 bay dọc phố theo hình học thật 8,5–12,8 s (tim đường Damrak, NWB) → E1 MỐC ĐINH 1655 12,8–16,4 s (năm dừng 13,0–14,8 s)
//  → E4a ảnh lịch sử neo điểm 3D 17,6–20,6 s → E3 reveal kéo lùi 20,6–24,0 s → glide/zoom-in 24–27 s → E4b then/now 27–30 s
export const FX = { E2: [8.5, 12.8], E1: [12.8, 16.4], E4a: [17.6, 20.6], E3: [20.6, 24.0], E4b: [26.0, 29.0] };
const YK = [[0, 1275], [4, 1350], [8.5, 1500], [12.5, 1630], [13.0, 1655], [14.8, 1655], [16, 1690], [18.0, 1886], [20.6, 1900], [24, 2026], [30, 2026]];
const lerpK = (K, t) => { for (let i = 1; i < K.length; i++) if (t <= K[i][0]) { const [t0, a] = K[i - 1], [t1, b] = K[i]; const u = (t - t0) / (t1 - t0); return a + (b - a) * u; } return K[K.length - 1][1]; };
const yearAt = (t) => lerpK(YK, t);
// toạ độ three: x = đông, y = cao, z = −bắc (m, gốc tại Dam). Cung điện: tâm ENU (−104, 11) → three (−104, ·, −11)
const PZ = P.pose || null;   // góc máy giải từ điểm khống chế (calib_photo.py)
const enu = (v) => [v[0], v[2], -v[1]];
const BASE = 1.8;   // cốt chân Cung điện trong 3DBAG (b3_h_maaiveld ≈ 1,8 m NAP): lời giải điểm khống chế lấy chân toà = 0
const lift = (v) => [v[0], v[1] + BASE, v[2]];
const POSE = PZ ? { pos: lift(enu(PZ.cam_enu)), look: lift(enu(PZ.look_enu)), up: enu(PZ.up_enu), fov: PZ.fov_v_deg } : null;
const DIR = POSE ? (() => { const d = POSE.look.map((v, i) => v - POSE.pos[i]); const n = Math.hypot(...d); return d.map((v) => v / n); })() : [0, 0, -1];
const DMK = (P.damrak || []).map(([e, n], i, A) => [e, 72 - 20 * i / Math.max(1, A.length - 1), -n]);   // tim đường Damrak, bắc → nam
const orb = (deg, h) => { const r = 168, q = deg * Math.PI / 180; return [-104 + r * Math.cos(q), h, -(11 + r * Math.sin(q))]; };
const PAL = [-104, 20, -11];
const CAM = [ // t, vị trí, điểm nhìn
  [0, [900, 1500, -3300], [0, 0, -100]],
  [4, [650, 650, -1600], [200, 0, -300]],
  [7.6, [470, 150, -700], [330, 20, -420]],
  ...(DMK.length ? [[8.5, DMK[0], DMK[2]], [9.7, DMK[2], DMK[4]], [10.9, DMK[4], DMK[6]], [12.0, DMK[6], PAL]] : []),
  [12.8, orb(10, 75), PAL], [14.0, orb(-15, 82), PAL], [15.4, orb(-45, 88), PAL], [16.6, orb(-80, 120), PAL],
  [18.2, [-420, 260, 360], [-104, 10, -11]],
  [20.6, [-1100, 700, 900], [-150, 0, -50]],
  [24.0, [-2600, 1900, 2400], [0, 0, -200]],
  [25.3, [-1000, 520, 800], [-140, 15, 0]],
  [26.3, POSE ? POSE.pos.map((v, i) => v - 150 * DIR[i] + (i === 1 ? 25 : 0)) : [-242, 17, 213], POSE ? POSE.look : PAL],
  [27.0, POSE ? POSE.pos : [-174, 2, 80], POSE ? POSE.look : PAL],
];
const cr = (p0, p1, p2, p3, u) => { const u2 = u * u, u3 = u2 * u; return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3); };
function crAt(t) {
  let i = 0; while (i < CAM.length - 2 && t > CAM[i + 1][0]) i++;
  const k = (j) => CAM[Math.max(0, Math.min(CAM.length - 1, j))];
  const u0 = Math.min(1, Math.max(0, (t - CAM[i][0]) / (CAM[i + 1][0] - CAM[i][0])));
  const u = u0 * u0 * (3 - 2 * u0) * 0.5 + u0 * 0.5;   // nửa êm nửa đều: không dừng hẳn ở mốc (máy luôn chuyển động)
  const v = (idx) => [0, 1, 2].map((d) => cr(k(i - 1)[idx][d], k(i)[idx][d], k(i + 1)[idx][d], k(i + 2)[idx][d], u));
  return { pos: v(1), look: v(2), up: [0, 1, 0] };
}
const mix3 = (a, b, e) => a.map((v, i) => v + (b[i] - v) * e);
function camAt(t) {
  if (!POSE || t < 26.3) { const c = crAt(t); c.pos[1] = Math.max(2, c.pos[1]); return c; }
  if (t < 27.0) { const c = crAt(26.3), u = (t - 26.3) / 0.7, e = 1 - Math.pow(1 - u, 3);      // chậm dần vào đúng góc ảnh
    return { pos: mix3(c.pos, POSE.pos, e), look: mix3(c.look, POSE.look, e), up: mix3([0, 1, 0], POSE.up, e) }; }
  if (t <= 28.6) return { pos: POSE.pos, look: POSE.look, up: POSE.up };                       // khoá góc khi ảnh chồng
  const u = Math.min(1, (t - 28.6) / 1.4), e = u * u * (3 - 2 * u), push = DIR.map((v) => v * 14 * e);   // sau khi hoà: đẩy nhẹ vào
  return { pos: POSE.pos.map((v, i) => v + push[i]), look: POSE.look.map((v, i) => v + push[i]), up: POSE.up };
}

// ---------- dữ liệu nguồn ----------
const POP = [ // năm, dân số, nguồn ngắn (trên hình), trạng thái kiểm
  [1622, 104932, 'city count 1622', 'thứ cấp'],
  [1795, 217024, 'census 1795', 'thứ cấp'],
  [1899, 510853, 'CBS census 1899', 'sơ cấp'],
  [1959, 872428, 'O&S Amsterdam', 'thứ cấp'],
  [2026, 941927, 'CBS StatLine', 'sơ cấp'],
];
function popAt(y) {
  if (y < POP[0][0]) return null;
  for (let i = 1; i < POP.length; i++) if (y <= POP[i][0]) { const [y0, a] = POP[i - 1], [y1, b] = POP[i]; const u = (y - y0) / (y1 - y0); return Math.exp(Math.log(a) + (Math.log(b) - Math.log(a)) * u); }
  return POP[POP.length - 1][1];
}
const CARDS = [
  { t: [0.4, 3.8], kind: 'hook', text: 'Watch for 1655: a town hall becomes a palace', src: 'Standing buildings, by year built · BAG register' },
  { t: [4.2, 7.8], kind: 'event', text: '1275 · First written record: people “at the Amstel dam”', src: 'Toll privilege of Floris V, 27 Oct 1275 · Amsterdam City Archives' },
  { t: [8.6, 12.4], kind: 'why', text: 'WHY HERE · River boats met sea ships at the dam', src: 'Primary source pending · flight path: Damrak axis (NWB)' },
  { t: [13.0, 16.3], kind: 'pin', text: '1655 · Town hall completed — today’s Royal Palace', src: 'Year: BAG register, building 0363100012167579' },
];

// ---------- dựng cảnh ----------
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(1); renderer.setSize(W, H);
renderer.shadowMap.enabled = !!P.shadows; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const SKY = new THREE.Color('#cfd9e3');
scene.background = SKY; scene.fog = new THREE.Fog(SKY, 2500, 9000);
const camera = new THREE.PerspectiveCamera(POSE ? POSE.fov : 38, W / H, 1.0, 20000);
scene.add(new THREE.HemisphereLight('#e8f0ff', '#5b5040', 1.15));
const sun = new THREE.DirectionalLight('#fff1dc', 2.3);
sun.position.set(-2200, 2600, 1600); sun.target.position.set(0, 0, 0); scene.add(sun, sun.target);
if (P.shadows) { sun.castShadow = true; const sc = sun.shadow.camera; sc.left = -3800; sc.right = 3800; sc.top = 3800; sc.bottom = -3800; sc.near = 100; sc.far = 9000; sun.shadow.mapSize.set(P.shadowRes || 4096, P.shadowRes || 4096); sun.shadow.bias = -0.0006; sun.shadow.normalBias = 1.5; }

const D = P.data;
const GROUND = new THREE.Color('#b9b79a'), WATER = new THREE.Color('#5f8fa6');
const groundMat = new THREE.MeshLambertMaterial({ color: GROUND.clone() }), waterMat = new THREE.MeshLambertMaterial({ color: WATER.clone(), polygonOffset: true, polygonOffsetFactor: -2 });
const FXON = P.fx !== false;   // tắt để đo giờ máy tăng thêm của 4 yếu tố
// địa hình (Copernicus GLO-30, đã mở hình thái để bỏ nhà): lưới 50 m
{
  const { x0, y0, step, nx, ny, z } = D.dem;
  const g = new THREE.PlaneGeometry((nx - 1) * step, (ny - 1) * step, nx - 1, ny - 1);
  g.rotateX(-Math.PI / 2);
  const pos = g.attributes.position;
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const vi = j * nx + i;                      // PlaneGeometry: hàng 0 ở phía −z sau khi xoay = bắc
    const north = (ny - 1 - j) * step + y0;     // hàng j của lưới DEM tăng theo bắc
    const zz = z[(ny - 1 - j) * nx + i];
    pos.setY(vi, Math.min(1.2, Math.max(-1.5, zz * (P.demScale ?? 0.3))) - 0.6);   // DSM Copernicus: thành phố phẳng → nén nhiễu nhà còn sót
  }
  g.translate(x0 + (nx - 1) * step / 2, 0, -(y0 + (ny - 1) * step / 2));
  g.computeVertexNormals();
  const m = new THREE.Mesh(g, groundMat);
  m.receiveShadow = !!P.shadows; scene.add(m);
}
// mặt nước BGT
{
  const pos = [];
  for (const poly of D.w) {
    const rings = poly.map((r) => { const v = []; for (let i = 0; i < r.length; i += 2) v.push(new THREE.Vector2(r[i], r[i + 1])); return v; });
    const outer = rings[0]; if (THREE.ShapeUtils.isClockWise(outer)) outer.reverse();
    const holes = rings.slice(1).map((h) => (THREE.ShapeUtils.isClockWise(h) ? h : h.reverse()));
    const tris = THREE.ShapeUtils.triangulateShape(outer, holes); const all = outer.concat(...holes);
    for (const t of tris) for (const k of t) pos.push(all[k].x, 0.9, -all[k].y);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, waterMat);
  m.receiveShadow = !!P.shadows; m.renderOrder = 1; scene.add(m);
}
// toà nhà
const ERA = (y) => (y < 1800 ? [0.62, 0.36, 0.27] : y < 1945 ? [0.74, 0.55, 0.40] : [0.86, 0.85, 0.82]);
let nBuild = 0, nVert = 0;
const buildMat = new THREE.MeshLambertMaterial({ vertexColors: true });
const uni = { uYear: { value: 1275 }, uFlash: { value: 6.0 }, uHi: { value: 0 }, uDim: { value: 0 }, uCut: { value: 0 }, uSolo: { value: 0 } };
const growGLSL = `
  attribute float aYear; attribute float aH; attribute float aTop; attribute float aG; attribute float aHi; varying float vHi; attribute float aCut; varying float vCut;
  uniform float uYear; uniform float uFlash; uniform float uSolo; varying float vFlash;
  float growK(){ float d = uYear - aYear + 4.0; if (aYear < 1.0) return 0.0; float u = clamp(d / 4.0, 0.0, 1.0);
    return u < 1.0 ? (1.0 - pow(1.0 - u, 3.0)) * 1.06 - 0.06 * u * u : 1.0; }`;
const growPos = `
  float gk = growK(); if (uSolo > 0.5 && aHi < 0.5) gk = 0.0;
  transformed.y = aG + aTop * aH * gk - (gk <= 0.0 ? 40.0 : 0.0);`;
buildMat.onBeforeCompile = (sh) => {
  Object.assign(sh.uniforms, uni);
  sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\n' + growGLSL).replace('#include <begin_vertex>', '#include <begin_vertex>\n' + growPos + '\n vFlash = clamp(1.0 - (uYear - aYear + 4.0) / uFlash, 0.0, 1.0) * step(aYear - 4.0, uYear); vHi = aHi; vCut = aCut;');
  sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying float vFlash; varying float vHi; varying float vCut; uniform float uHi; uniform float uDim; uniform float uCut;').replace('#include <dithering_fragment>', '#include <dithering_fragment>\n if (vCut * uCut > 0.5) discard;\n gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(1.0, 0.86, 0.45), vFlash * 0.55);\n if (vHi > 0.5) gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(1.0, 0.80, 0.38), 0.45 * uHi) + 0.12 * uHi;\n else { float l = dot(gl_FragColor.rgb, vec3(0.299, 0.587, 0.114)); gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(l), 0.55 * uDim) * (1.0 - 0.38 * uDim); }');
};
const depthMat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking });
depthMat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, uni); sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\n' + growGLSL.replace('varying float vFlash;', '').replace('varying float vHi;', '')).replace('#include <begin_vertex>', '#include <begin_vertex>\n' + growPos + '\n vCut = aCut;');
  sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying float vCut; uniform float uCut;').replace('void main() {', 'void main() {\n if (vCut * uCut > 0.5) discard;'); };
let PALACE = null; const CUTINFO = [];
function buildCity(B, copies) {
  const pos = [], nor = [], col = [], yr = [], hh = [], top = [], gg = [], hi = [], cut = [];
  const CP = POSE ? [POSE.pos[0], -POSE.pos[2]] : null;   // điểm đứng máy ảnh 1886 (ENU)
  for (let c = 0; c < copies; c++) {
    const ox = (c % 3) * 7200 - (copies > 1 ? 7200 : 0), oz = Math.floor(c / 3) * 6200;
    for (const [y, h, g0, r] of B) {
      if (!y || y === 1005) continue;            // 1005 = năm giữ chỗ của BAG ("không rõ"): loại, ghi trong báo cáo
      const v = []; for (let i = 0; i < r.length; i += 2) v.push(new THREE.Vector2(r[i] + ox, r[i + 1] - oz));
      let cxx = 0, cyy = 0; for (const q of v) { cxx += q.x; cyy += q.y; } cxx /= v.length; cyy /= v.length;
      const isHi = c === 0 && y === 1655 && Math.hypot(cxx + 104.4, cyy - 11.1) < 6 ? 1 : 0;   // Cung điện (BAG 0363100012167579)
      if (isHi) PALACE = { v: v.map((q) => q.clone()), h, g: g0 };
      let isCut = 0;   // toà hiện nay chứa điểm đứng máy ảnh 1886 → cắt bỏ trong nhịp then/now
      if (CP && c === 0 && Math.hypot(cxx - CP[0], cyy - CP[1]) < 120) { let inn = false; for (let i = 0, j = v.length - 1; i < v.length; j = i++) { const a = v[i], b = v[j]; if ((a.y > CP[1]) !== (b.y > CP[1]) && CP[0] < (b.x - a.x) * (CP[1] - a.y) / (b.y - a.y) + a.x) inn = !inn; } isCut = inn ? 1 : 0; if (inn) CUTINFO.push({ year: y, h }); }
      if (THREE.ShapeUtils.isClockWise(v)) v.reverse();
      const e = ERA(y), jit = 0.92 + ((y * 7919 + v.length * 31) % 17) / 100;
      const C = e.map((x) => Math.min(1, x * jit)), R = [0.78, 0.42, 0.33].map((x) => x * jit);
      const gz = Math.max(-1, Math.min(5, g0));
      const push = (p, n, t, cc) => { pos.push(p.x, 0, -p.y); nor.push(...n); col.push(...cc); yr.push(y); hh.push(h); top.push(t); gg.push(gz); hi.push(isHi); cut.push(isCut); };
      for (let i = 0; i < v.length; i++) {        // tường
        const a = v[i], b = v[(i + 1) % v.length], dx = b.x - a.x, dy = b.y - a.y, l = Math.hypot(dx, dy) || 1, n = [dy / l, 0, dx / l];
        push(a, n, 0, C); push(b, n, 0, C); push(b, n, 1, C); push(a, n, 0, C); push(b, n, 1, C); push(a, n, 1, C);   // (b0−a0)×(b1−a0) ∥ pháp tuyến ngoài
      }
      const tris = THREE.ShapeUtils.triangulateShape(v, []);   // mái phẳng (LoD1.2); toà cổ mái đỏ gạch
      const rc = y < 1945 ? R : C.map((x) => x * 0.9);
      for (const t of tris) for (const k of [t[0], t[1], t[2]]) push(v[k], [0, 1, 0], 1, rc);
      nBuild++;
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.setAttribute('aYear', new THREE.Float32BufferAttribute(yr, 1));
  g.setAttribute('aH', new THREE.Float32BufferAttribute(hh, 1)); g.setAttribute('aTop', new THREE.Float32BufferAttribute(top, 1)); g.setAttribute('aG', new THREE.Float32BufferAttribute(gg, 1)); g.setAttribute('aHi', new THREE.Float32BufferAttribute(hi, 1)); g.setAttribute('aCut', new THREE.Float32BufferAttribute(cut, 1));
  g.boundingSphere = new THREE.Sphere(new THREE.Vector3(0, 0, 0), 1e6);
  nVert = pos.length / 3;
  const m = new THREE.Mesh(g, buildMat); m.customDepthMaterial = depthMat; m.castShadow = m.receiveShadow = !!P.shadows; m.frustumCulled = false;
  scene.add(m);
}
buildCity(D.b, P.copies || 1);
// viền phát sáng của toà mốc đinh: vỏ lộn (BackSide) nở 2,2 m quanh khối Cung điện
let hull = null;
if (PALACE) {
  const sh = new THREE.Shape(PALACE.v); const cx = PALACE.v.reduce((a, q) => a + q.x, 0) / PALACE.v.length, cy = PALACE.v.reduce((a, q) => a + q.y, 0) / PALACE.v.length;
  const eg = new THREE.ExtrudeGeometry(sh, { depth: PALACE.h + 2.2, bevelEnabled: false }); eg.rotateX(-Math.PI / 2);
  eg.translate(-cx, 0, cy); const sc = 1 + 2.2 / 40; eg.scale(sc, 1, sc); eg.translate(cx, Math.max(-1, Math.min(5, PALACE.g)) - 0.5, -cy);
  hull = new THREE.Mesh(eg, new THREE.MeshBasicMaterial({ color: '#ffd166', side: THREE.BackSide, transparent: true, opacity: 0, depthWrite: false }));
  hull.visible = false; scene.add(hull);
}
const ease = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
function pinAt(t) {   // E1: sáng + viền 12,9–16,3 s; phần còn lại mờ nhẹ
  const k = FXON ? ease((t - 12.9) / 0.4) * ease((16.3 - t) / 0.5) : 0;
  uni.uHi.value = k; uni.uDim.value = k;
  groundMat.color.copy(GROUND).multiplyScalar(1 - 0.32 * k); waterMat.color.copy(WATER).multiplyScalar(1 - 0.32 * k);
  if (hull) { hull.visible = k > 0.01; hull.material.opacity = 0.85 * k; }
  return k;
}

// lớp cơ chế "why here": dòng Amstel (đi xuống bắc tới Dam), tàu biển từ IJ theo Damrak, con đập
const mech = new THREE.Group(); scene.add(mech);
const pathTube = (pts, color) => {
  const curve = new THREE.CatmullRomCurve3(pts.map(([e, n]) => new THREE.Vector3(e, 4, -n)));
  const m = new THREE.Mesh(new THREE.TubeGeometry(curve, 120, 9, 8, false), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0 }));
  m.userData.curve = curve; mech.add(m); return m;
};
const amstel = pathTube([[746, -1458], [567, -723], [43, -641], [-77, -340], [0, -40]], '#3fa9e0');
const damrak = pathTube([[558, 935], [508, 591], [234, 292], [20, 60]], '#1f6fb0');
const dam = new THREE.Mesh(new THREE.BoxGeometry(150, 14, 34), new THREE.MeshLambertMaterial({ color: '#d2683c', transparent: true, opacity: 0 }));
dam.position.set(10, 7, 0); dam.rotation.y = 0.35; mech.add(dam);
const boats = [];
for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new THREE.ConeGeometry(22, 70, 4), new THREE.MeshLambertMaterial({ color: i < 3 ? '#f2f2f2' : '#ffd166', transparent: true, opacity: 0 }));
  b.rotation.x = Math.PI / 2; boats.push(b); mech.add(b); }
const ring = new THREE.Mesh(new THREE.RingGeometry(60, 70, 64), new THREE.MeshBasicMaterial({ color: '#ffd166', transparent: true, opacity: 0, side: THREE.DoubleSide }));
ring.rotation.x = -Math.PI / 2; ring.position.set(10, 3, 0); mech.add(ring);
function mechAt(t) {
  const a = Math.min(1, Math.max(0, (t - 8.4) / 0.6)) * Math.min(1, Math.max(0, (12.9 - t) / 0.6));
  for (const m of [amstel, damrak]) m.material.opacity = 0.85 * a;
  dam.material.opacity = a; dam.scale.y = 0.2 + 0.8 * Math.min(1, Math.max(0, (t - 9.0) / 0.6));
  boats.forEach((b, i) => { const curve = (i < 3 ? amstel : damrak).userData.curve; const u = ((t * 0.09 + i / 3) % 1) * 0.95; const p = curve.getPointAt(u), q = curve.getPointAt(Math.min(1, u + 0.01));
    b.position.copy(p).setY(10); b.lookAt(q.x, 10, q.z); b.rotateX(Math.PI / 2); b.material.opacity = a; });
  const k = (((t - 9.3) % 1.6) + 1.6) % 1.6 / 1.6; ring.scale.setScalar(0.6 + k * 1.6); ring.material.opacity = a * (1 - k) * (t > 9.3 ? 1 : 0);
}

// ---------- lớp 2D ----------
const out = document.createElement('canvas'); out.width = W; out.height = H; document.body.appendChild(out);
const g2 = out.getContext('2d', { willReadFrequently: true });
const FONT = '"DejaVu Sans", "Liberation Sans", Arial, sans-serif';
const fmtN = (n) => Math.round(n).toLocaleString('en-US');
const TXT = [];
const RECTS = [];   // hình chữ nhật chữ + nền chữ của khung (đo ngân sách chữ); anchored = thẻ neo vào công trình   // nhật ký chữ để đo tương phản: {s px@1080, box, color}
function text(s, x, y, px, color, opts = {}) {
  g2.font = `${opts.w || 700} ${Math.round(px * S)}px ${FONT}`; g2.textAlign = opts.align || 'left'; g2.textBaseline = 'alphabetic';
  if (opts.halo) { g2.lineJoin = 'round'; g2.lineWidth = Math.max(2, px * S * 0.16); g2.strokeStyle = 'rgba(10,14,20,0.85)'; g2.strokeText(s, x, y); }
  g2.fillStyle = color; g2.fillText(s, x, y);
  const m = g2.measureText(s), w = m.width, x0 = opts.align === 'right' ? x - w : opts.align === 'center' ? x - w / 2 : x;
  RECTS.push({ r: [x0, y - m.actualBoundingBoxAscent, x0 + w, y + m.actualBoundingBoxDescent], anchored: !!opts.anchored || !!plate.anch });
  TXT.push({ s, px, cap: Math.round(px * 0.72), box: [x0, y - m.actualBoundingBoxAscent, x0 + w, y + m.actualBoundingBoxDescent], color, alpha: opts.alpha ?? 1 });
}
function plate(x0, y0, x1, y1, a, anchored) { RECTS.push({ r: [x0, y0, x1, y1], anchored: !!anchored || !!plate.anch }); g2.fillStyle = `rgba(12,16,22,${0.78 * a})`; const r = 14 * S; g2.beginPath(); g2.roundRect(x0, y0, x1 - x0, y1 - y0, r); g2.fill(); }
const wordsOK = (s) => s.replace(/[·—–:“”]/g, ' ').split(/\s+/).filter(Boolean).length;
// ---------- lớp chữ theo NGÂN SÁCH CHỮ (chủ dự án 15/10 23:04) ----------
// thường trực: NĂM (dưới-trái) + CHỈ SỐ (trên-phải), mỗi cái 1 dòng; nhãn phương pháp + nguồn dữ liệu chỉ 0–5 s và màn kết;
// tối đa 1 thẻ cùng lúc ở dải dưới (ngoài vùng giữa 20–80 %), dòng phụ = nguồn của chính thẻ; thẻ neo công trình được ở vùng giữa.
const INTRO = [0, 4.2], OUTRO = [29.0, 30];
const fade = (t, a, b, k = 0.35) => Math.max(0, Math.min(1, (t - a) / k, (b - t) / k));
function card(t, c, title, src, anchored) {   // thẻ dải dưới (hoặc neo): tiêu đề 52 px + nguồn 38 px
  const a = fade(t, c[0], c[1]); if (a <= 0) return;
  g2.globalAlpha = a;
  const xl = anchored ? 36 * S : (YBOX.x1 || 0) + 24 * S, avail = W - 36 * S - xl;   // dải dưới: bên phải hộp năm
  let tp = 44; g2.font = `700 ${Math.round(tp * S)}px ${FONT}`; let w1 = g2.measureText(title).width;
  if (w1 + 64 * S > avail) { tp = Math.max(38, tp * (avail - 64 * S) / w1); g2.font = `700 ${Math.round(tp * S)}px ${FONT}`; w1 = g2.measureText(title).width; }
  g2.font = `500 ${Math.round(38 * S)}px ${FONT}`; const w2 = g2.measureText(src).width;
  const w = Math.min(avail, Math.max(w1, w2) + 56 * S), hgt = 122 * S;
  if (Math.max(w1, w2) + 64 * S > avail + 1) console.error('thẻ tràn', title);
  let cx = Math.min(W - 36 * S - w / 2, Math.max(xl + w / 2, W / 2)), y1 = H - 40 * S, y0 = y1 - hgt;
  if (anchored) { const v = anchored.clone().project(camera), ax = (v.x + 1) / 2 * W, ay = (1 - v.y) / 2 * H;
    cx = Math.min(W - 36 * S - w / 2, Math.max(36 * S + w / 2, ax)); y1 = Math.max(hgt + 36 * S, Math.min(H * 0.62, ay - 60 * S)); y0 = y1 - hgt;
    g2.strokeStyle = '#ffd166'; g2.lineWidth = 4 * S; g2.beginPath(); g2.moveTo(cx, y1); g2.lineTo(ax, ay); g2.stroke();
    g2.fillStyle = '#ffd166'; g2.beginPath(); g2.arc(ax, ay, 8 * S, 0, 7); g2.fill(); plate.anch = true; }
  plate(cx - w / 2, y0, cx + w / 2, y1, 1);
  g2.fillStyle = '#ffd166'; g2.fillRect(cx - w / 2, y0, 8 * S, hgt);
  text(title, cx, y0 + 56 * S, tp, '#ffffff', { align: 'center', alpha: a });
  text(src, cx, y0 + 102 * S, 38, '#c9d3dd', { align: 'center', w: 500, alpha: a });
  plate.anch = false; g2.globalAlpha = 1;
}
const PALTOP = new THREE.Vector3(-104, 36, -11);
const YBOX = {};
function overlay(t, year) {
  TXT.length = 0; RECTS.length = 0;
  if (FXON) thenNowPhoto(t);   // ảnh then/now nằm DƯỚI lớp chữ thường trực
  const y = Math.floor(year);
  // NĂM — 1 dòng 96 px; mốc đinh: dừng + phóng 1,6×, vàng
  const zk = FXON ? ease((t - 12.95) / 0.3) * ease((15.15 - t) / 0.35) : 0, zs = 1 + 0.45 * zk, ys = String(y);   // 1,45×: đỉnh hộp vẫn ngoài vùng giữa (≥ 80 % cao)
  g2.font = `700 ${Math.round(96 * zs * S)}px ${FONT}`; const wy = g2.measureText(ys).width;
  YBOX.x1 = 36 * S + wy + 48 * zs * S;
  plate(36 * S, H - 40 * S - 114 * zs * S, YBOX.x1, H - 40 * S, 1);
  if (zk > 0.01) { g2.strokeStyle = `rgba(255,209,102,${zk})`; g2.lineWidth = 5 * S; g2.strokeRect(36 * S, H - 40 * S - 114 * zs * S, wy + 48 * zs * S, 114 * zs * S); }
  text(ys, 36 * S + 24 * zs * S, H - 40 * S - 22 * zs * S, 96 * zs, zk > 0.5 ? '#ffd166' : '#ffffff');
  // CHỈ SỐ (dân số) — 1 dòng; "≈" khi nội suy; nguồn chỉ hiện khi đúng năm có số đếm; trước số đếm đầu tiên: ẩn
  const p = popAt(year);
  if (p) {
    const q = POP.find((r) => Math.abs(r[0] - year) < 2.5), ps = (q ? '' : '≈ ') + fmtN(q ? q[1] : p) + ' people';
    g2.font = `700 ${Math.round(64 * S)}px ${FONT}`; const wp = g2.measureText(ps).width;
    let ww = wp; if (q) { g2.font = `500 ${Math.round(38 * S)}px ${FONT}`; ww = Math.max(wp, g2.measureText('Source: ' + q[2]).width); }
    plate(W - 36 * S - ww - 52 * S, 36 * S, W - 36 * S, 36 * S + (q ? 150 : 100) * S, 1);
    text(ps, W - 62 * S, 36 * S + 74 * S, 64, '#ffffff', { align: 'right' });
    if (q) text('Source: ' + q[2], W - 62 * S, 36 * S + 126 * S, 38, '#c9d3dd', { align: 'right', w: 500 });
  }
  // nhãn phương pháp + nguồn dữ liệu: chỉ đầu phim và màn kết
  const ia = Math.max(fade(t, INTRO[0] - 1, INTRO[1]), fade(t, OUTRO[0], OUTRO[1] + 1));
  if (ia > 0) { const L1 = 'No AI imagery · 3DBAG · Kadaster · Copernicus DEM';   // 1 dòng; nguồn đầy đủ + giấy phép ở mô tả/bình luận ghim
    g2.globalAlpha = ia; g2.font = `600 ${Math.round(38 * S)}px ${FONT}`; const w1 = g2.measureText(L1).width;
    plate(36 * S, 36 * S, 36 * S + w1 + 48 * S, 36 * S + 72 * S, 1);
    text(L1, 60 * S, 36 * S + 50 * S, 38, '#ffffff', { w: 600, alpha: ia }); g2.globalAlpha = 1; }
  // thẻ: tối đa 1 tại một thời điểm
  for (const c of CARDS) if (t >= c.t[0] && t <= c.t[1]) card(t, c.t, c.text, c.src, c.kind === 'pin' && FXON ? PALTOP : null);
  if (FXON) { callout(t); thenNow(t); }
}
// E4a: ảnh lịch sử thật làm chú thích neo vào điểm 3D (góc tây-bắc đỉnh tường Cung điện = góc gần trong ảnh); ảnh không có nền chữ, chú thích 2 dòng
const ANCHOR = new THREE.Vector3(-133.2, 31, -52.3);
function callout(t) {
  const PH = P.photoImg, c = [17.6, 20.6]; if (!PH || t < c[0] || t > c[1]) return;
  const a = fade(t, c[0], c[1]);
  const v = ANCHOR.clone().project(camera); if (v.z > 1) return;
  const ax = (v.x + 1) / 2 * W, ay = (1 - v.y) / 2 * H;
  const T1 = '1886 · The palace from the northwest', T2 = 'Photo: anonymous · Rijksmuseum RP-F-00-568 · CC0';
  g2.font = `700 ${Math.round(44 * S)}px ${FONT}`; const wt1 = g2.measureText(T1).width; g2.font = `500 ${Math.round(38 * S)}px ${FONT}`; const wt2 = g2.measureText(T2).width;
  const ih = 300 * S, iw = ih * PH.width / PH.height, cw = Math.max(wt1, wt2) + 48 * S;
  const x1 = W - 36 * S, x0 = x1 - Math.max(iw, cw), py0 = 230 * S, cy0 = py0 + ih + 12 * S, cy1 = cy0 + 116 * S;
  g2.globalAlpha = a;
  g2.strokeStyle = '#ffd166'; g2.lineWidth = 4 * S; g2.beginPath(); g2.moveTo(x1 - iw, py0 + ih / 2); g2.lineTo(ax, ay); g2.stroke();
  const k = (t * 1.2) % 1; g2.beginPath(); g2.arc(ax, ay, (10 + 26 * k) * S, 0, 7); g2.strokeStyle = `rgba(255,209,102,${a * (1 - k)})`; g2.stroke();
  g2.fillStyle = '#ffd166'; g2.beginPath(); g2.arc(ax, ay, 9 * S, 0, 7); g2.fill();
  g2.drawImage(PH, x1 - iw, py0, iw, ih); g2.strokeStyle = '#ffd166'; g2.lineWidth = 3 * S; g2.strokeRect(x1 - iw, py0, iw, ih);
  plate.anch = true; plate(x1 - cw, cy0, x1, cy1, 1);
  text(T1, x1 - cw + 24 * S, cy0 + 52 * S, 44, '#ffffff', { alpha: a }); text(T2, x1 - cw + 24 * S, cy0 + 98 * S, 38, '#c9d3dd', { w: 500, alpha: a });
  plate.anch = false; g2.globalAlpha = 1;
}
// E4b: then/now — ảnh 1886 chồng đúng góc máy (giải từ điểm khống chế), rồi hoà sang cảnh 3D cùng góc; 1 thẻ ở dải dưới
function thenNowPhoto(t) {
  const PH = P.photoImg; if (!PH || !POSE || t < 26.8) return;
  const ap = Math.min(1, Math.max(0, (t - 26.8) / 0.4)) * (1 - ease((t - 27.6) / 0.8));
  const ph = H, pw = ph * PH.width / PH.height, px = (W - pw) / 2;
  if (ap > 0.001) { g2.globalAlpha = ap; g2.filter = 'sepia(0.25)'; g2.drawImage(PH, px, 0, pw, ph); g2.filter = 'none'; g2.globalAlpha = 1;
    g2.strokeStyle = `rgba(255,209,102,${ap})`; g2.lineWidth = 3 * S; g2.strokeRect(px, 0, pw, ph); }
}
function thenNow(t) {
  if (!P.photoImg || !POSE || t < 26.0) return;
  card(t, [26.0, 29.0], (t < 27.9) ? 'THEN · 1886' : 'NOW · 2026 — the 1899 building cut away', 'Rijksmuseum RP-F-00-568 (CC0) · camera from 7 control points', null);
}
// ngân sách chữ: % diện tích khung bị chữ + nền chữ phủ (hợp các hình chữ nhật, lưới 4 px);
// vùng giữa = hình chữ nhật 20–80 % rộng × 20–80 % cao; chữ neo vào công trình được miễn
function textBudget() {
  const g = 4, nx = Math.ceil(W / g), ny = Math.ceil(H / g), m = new Uint8Array(nx * ny);
  for (const { r: [x0, y0, x1, y1], anchored } of RECTS) {
    for (let j = Math.max(0, Math.floor(y0 / g)); j < Math.min(ny, Math.ceil(y1 / g)); j++)
      for (let i = Math.max(0, Math.floor(x0 / g)); i < Math.min(nx, Math.ceil(x1 / g)); i++) m[j * nx + i] |= anchored ? 2 : 1;
  }
  let all = 0, cen = 0, cenN = 0;
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const v = m[j * nx + i]; if (v) all++;
    if (i >= nx * 0.2 && i < nx * 0.8 && j >= ny * 0.2 && j < ny * 0.8) { cenN++; if (v & 1) cen++; } }
  return { pct: +(100 * all / (nx * ny)).toFixed(1), center_unanchored_pct: +(100 * cen / cenN).toFixed(1), blocks: RECTS.length };
}
function contrast() {   // WCAG trên điểm ảnh thật: nền = trung vị viền hộp; chữ = phân vị 95 % trong hộp
  const lum = (r, g, b) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }).reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
  return TXT.filter((e) => e.alpha >= 0.95).map((e) => {
    const [x0, y0, x1, y1] = e.box.map(Math.round), X0 = Math.max(0, x0 - 4), Y0 = Math.max(0, y0 - 4), X1 = Math.min(W - 1, x1 + 4), Y1 = Math.min(H - 1, y1 + 4);
    const d = g2.getImageData(X0, Y0, X1 - X0 + 1, Y1 - Y0 + 1).data, w = X1 - X0 + 1, h = Y1 - Y0 + 1, L = [], I = [];
    for (let x = 0; x < w; x++) for (const yy of [0, h - 1]) { const i = (yy * w + x) * 4; L.push(lum(d[i], d[i + 1], d[i + 2])); }
    for (let yy = 3; yy < h - 3; yy++) for (let x = 3; x < w - 3; x++) { const i = (yy * w + x) * 4; I.push(lum(d[i], d[i + 1], d[i + 2])); }
    L.sort((a, b) => a - b); I.sort((a, b) => a - b);
    const bg = L[Math.floor(L.length / 2)], ft = I[Math.floor(I.length * 0.97)];
    return { s: e.s.slice(0, 40), px1080: e.px, words: wordsOK(e.s), ratio: +((Math.max(bg, ft) + 0.05) / (Math.min(bg, ft) + 0.05)).toFixed(2) };
  });
}

let gl0 = renderer.getContext();
P.info = () => ({ cut: CUTINFO, palace: !!PALACE, buildings: nBuild, vertices: nVert, tris: nVert / 3, maxTex: gl0.getParameter(gl0.MAX_TEXTURE_SIZE), renderer: gl0.getParameter(gl0.getExtension('WEBGL_debug_renderer_info')?.UNMASKED_RENDERER_WEBGL ?? gl0.RENDERER) });
P.debugPose = (yr, alpha, solo) => { uni.uSolo.value = solo ? 1 : 0;   // kiểm căn góc: dựng ở năm yr, máy đúng POSE, chồng ảnh alpha
  uni.uYear.value = yr; uni.uCut.value = yr > 2000 ? 1 : 0; camera.position.set(...POSE.pos); camera.up.set(...POSE.up); camera.lookAt(...POSE.look); mechAt(0); pinAt(0);
  renderer.render(scene, camera); g2.drawImage(renderer.domElement, 0, 0);
  const PH = P.photoImg, pw = H * PH.width / PH.height; g2.globalAlpha = alpha; g2.drawImage(PH, (W - pw) / 2, 0, pw, H); g2.globalAlpha = 1;
  const v = ANCHOR.clone().project(camera); return { img: out.toDataURL('image/jpeg', 0.95).slice(23), anchor: [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H] };
};
P.budgetAll = () => Array.from({ length: N }, (_, f) => { const t = f / FPS, c = camAt(t); camera.position.set(...c.pos); camera.up.set(...c.up); camera.lookAt(...c.look); camera.updateMatrixWorld(); g2.clearRect(0, 0, W, H); overlay(t, yearAt(t)); return textBudget(); });
P.drawFrame = (f, measure) => {
  const t = f / FPS, year = yearAt(t);
  uni.uYear.value = year;
  const c = camAt(t); camera.position.set(...c.pos); camera.up.set(...c.up); camera.lookAt(...c.look);
  mechAt(t); pinAt(t); uni.uCut.value = FXON && t >= 26.3 ? 1 : 0;
  const t0 = performance.now();
  renderer.render(scene, camera);
  g2.drawImage(renderer.domElement, 0, 0);
  // vi-nhét + hạt nhẹ (ổn định theo khung)
  const vg = g2.createRadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, H * 0.95); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.28)'); g2.fillStyle = vg; g2.fillRect(0, 0, W, H);
  const t1 = performance.now();
  overlay(t, year);
  const r = { f, year: Math.floor(year), gl_ms: +(t1 - t0).toFixed(1) };
  r.budget = textBudget();
  if (measure) r.text = contrast();
  r.img = out.toDataURL('image/jpeg', 0.95).slice(23);
  return r;
};
P.camPath = () => Array.from({ length: N }, (_, f) => { const t = f / FPS, c = camAt(t); return { f, year: +yearAt(t).toFixed(2), pos: c.pos.map((v) => +v.toFixed(2)), look: c.look.map((v) => +v.toFixed(2)) }; });
P.ready = true;

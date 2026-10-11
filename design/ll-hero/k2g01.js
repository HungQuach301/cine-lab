// KÊNH 2 · ngách G · tập thử K2G-01 "Steel" — 8 BỘ CẢNH 3D (G2). Nhận diện theo channel-k2/NHAN-DIEN.md:
//   "mô hình kỹ thuật sống": sa bàn khối, ánh công nghiệp, MỘT màu nhấn cam #F08A4B cho thứ đang được giải thích, xanh lục lam #3CC2B0 cho dòng "bình thường"/sạch,
//   hổ phách #F2C14E cho dự báo; nền mực #0F1722. Không logo, không mặt người, không cờ hay biểu tượng quốc gia/dân tộc.
//   G2 (chủ dự án 11/10): KHÔNG nướng chữ vào ảnh 3D — mọi chữ vẽ ở lớp 2D (scripts/k2/lib) bám theo `anchors` (toạ độ màn hình mỗi khung, scripts/k2/hero.js ghi anchors.json),
//   nên cỡ chữ đo được (LL Q5/Q6) và đọc được trên điện thoại. Máy quay khai trong đặc tả: opt.cam = [{u: 0..1 (phần thời lượng), p: [x,y,z], l: [x,y,z], mm}].
//   Vân vật liệu (gạch, tôn sóng, bê tông, gỉ) cho mặt nhà và nội thất; bờ sông có kè đá, đá hộc, bến, sà lan, cây trụi.
//   valley   thung lũng sông (Braddock): nhà máy ven sông, 2 tuyến ray, sông, cầu giàn, thị trấn; opt.tod dusk|night|blue|day, opt.barges (sà lan đêm), khu lò cốc tổ ong (x ≈ −130).
//   ingots   sa bàn số: thỏi = 10 Mt; opt.piles [{x, z, n, us, cols, rows, grow}] (grow = giây mọc; −1 = có sẵn).
//   chain    bản đồ tuyến giản lược: quặng → ray → tàu Hồ Lớn → ray → Pittsburgh; cốc Connellsville; đá vôi. opt.draw {ore, boat, rail, coke, lime: [t0, t1]}, opt.full, opt.own (giây sáng vòng sở hữu cốc).
//   furnace  xưởng Bessemer: lò chuyển nghiêng rót thép vào thùng, tia lửa, cầu trục, bóng người. opt.pour [t0, t1].
//   trade    sa bàn thương mại: bệ sản lượng 2025, nhà máy mới mọc (opt.mills), cung xuất khẩu (opt.arcs), tường thuế Mỹ (opt.wall), cổng EU (opt.gate), khối dự báo (opt.proj).
//   port     cảng thép + hải quan: tàu, cẩu giàn, cuộn thép, cổng hải quan có thanh chắn (opt.lift), xe tải; opt.tod day|dusk, opt.gate 'us'|'eu' (màu cổng).
//   mill     nhà máy thép hiện đại ban ngày: xưởng lò hồ quang (mở một bên), bãi phế + cẩu nam châm, dây cán phôi; opt.hot (phôi đỏ chạy), opt.arc (cường độ hồ quang).
//   north    phương bắc giờ xanh: tháp khử hydro, nhà điện phân, lò hồ quang, tua-bin gió; opt.site = công trường (khung thép + cẩu tháp, chưa vận hành).
import { THREE, useScene, figure, dust, camRig, box, cyl, std, glowSprite, rng, ease, lerp, canvasTex } from './kit.js';

const C = { ink: '#0F1722', text: '#EEF1F4', steel: '#9AA7B5', orange: '#F08A4B', teal: '#3CC2B0', amber: '#F2C14E' };
const GRADE_K2 = { gCanvas: 0.0, gVig: 0.24, gLift: 0.025, gSat: 0.92, gShadowTint: [0.22, 0.34, 0.62], gHiTint: [1.02, 1.0, 0.97] };
const GRADE_K2_WARM = { gCanvas: 0.0, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.26, 0.33, 0.6], gHiTint: [1.05, 0.99, 0.92] };
const GRADE_K2_DAY = { gCanvas: 0.0, gVig: 0.18, gLift: 0.015, gSat: 0.95, gShadowTint: [0.2, 0.3, 0.5], gHiTint: [1.02, 1.0, 0.98] };
const basic = (color, o = {}) => new THREE.MeshBasicMaterial({ color, ...o });
const V3 = (a) => new THREE.Vector3(...a);
// máy quay: opt.cam (u 0..1) hoặc mặc định của cảnh
function rigOf(W, H, dur, opt, def) { const K = (opt.cam || def).map((k) => ({ t: k.u * dur, p: k.p, l: k.l, mm: k.mm || 32 })); return camRig(W, H, K.length > 1 ? K : [K[0], { ...K[0], t: dur }]); }
function skyDome(scene, stops, r = 300) {
  const s = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, map: canvasTex(8, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([u, c]) => gr.addColorStop(u, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); }) }));
  scene.add(s); return s;
}
const fogOf = (scene, color, d) => { useScene(scene); scene.fog = new THREE.FogExp2(color, d); scene.background = new THREE.Color(color); };
const softTex = () => canvasTex(128, 128, (g, w, h) => { const gr = g.createRadialGradient(64, 64, 2, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.4, 'rgba(255,255,255,0.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });

// ---------- vân vật liệu (canvas, lặp) ----------
const rep = (t, a, b) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(a, b); t.anisotropy = 4; return t; };
function brickTex(seed = 3, base = '#5a3428') { const R = rng(seed); return canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = '#2b211d'; g.fillRect(0, 0, w, h); const bw = 64, bh = 22;
  for (let y = 0, r = 0; y < h; y += bh, r++) for (let x = -(r % 2) * bw / 2; x < w; x += bw) { const k = 0.75 + R() * 0.45, c = new THREE.Color(base).multiplyScalar(k);
    g.fillStyle = '#' + c.getHexString(); g.fillRect(x + 2, y + 2, bw - 4, bh - 4); if (R() < 0.18) { g.fillStyle = 'rgba(10,8,8,0.25)'; g.fillRect(x + 2, y + 2, bw - 4, bh - 4); } }
  for (let i = 0; i < 60; i++) { const x = R() * w, gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(15,12,12,0.0)'); gr.addColorStop(0.5, 'rgba(15,12,12,0.22)'); gr.addColorStop(1, 'rgba(15,12,12,0)'); g.fillStyle = gr; g.fillRect(x, 0, 6 + R() * 20, h); } }); }
function corrTex(seed = 5, base = '#7d8590', rust = 0.2) { const R = rng(seed); return canvasTex(256, 256, (g, w, h) => {
  for (let x = 0; x < w; x++) { const v = 0.75 + 0.25 * Math.sin(x / w * Math.PI * 16), c = new THREE.Color(base).multiplyScalar(v); g.fillStyle = '#' + c.getHexString(); g.fillRect(x, 0, 1, h); }
  for (let i = 0; i < 90 * rust; i++) { const x = R() * w, y = R() * h, r = 4 + R() * 30, gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(120,64,30,0.35)'); gr.addColorStop(1, 'rgba(120,64,30,0)'); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  for (let y = 0; y < h; y += 64) { g.fillStyle = 'rgba(0,0,0,0.35)'; g.fillRect(0, y, w, 2); } }); }
function concTex(seed = 7, base = '#6d6c68') { const R = rng(seed); return canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h); for (let i = 0; i < 5000; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '20,20,18' : '200,198,190'},${0.04 + R() * 0.08})`; g.fillRect(R() * w, R() * h, 1 + R() * 4, 1 + R() * 4); }
  for (let i = 0; i < 14; i++) { const x = R() * w, y = R() * h, r = 30 + R() * 90, gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(30,26,22,0.18)'); gr.addColorStop(1, 'rgba(30,26,22,0)'); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  g.strokeStyle = 'rgba(20,20,20,0.45)'; g.lineWidth = 2; for (let i = 0; i <= w; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }); }
function stoneTex(seed = 9) { const R = rng(seed); return canvasTex(512, 256, (g, w, h) => {
  g.fillStyle = '#2a2a28'; g.fillRect(0, 0, w, h); for (let y = 0, r = 0; y < h; y += 32, r++) for (let x = -(r % 2) * 40; x < w; x += 80) { const v = 70 + R() * 50 | 0; g.fillStyle = `rgb(${v},${v - 4},${v - 10})`; g.fillRect(x + 2, y + 2, 76, 28); } }); }
function gridTex(bg = '#121b28', rep0 = 6) { return rep(canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); for (let i = 0; i <= w; i += 32) { g.strokeStyle = i % 128 ? 'rgba(154,167,181,0.07)' : 'rgba(154,167,181,0.2)'; g.lineWidth = i % 128 ? 1 : 2; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }), rep0, rep0); }
const M = { brick: null };
function mats() { if (M.brick) return M; const tex = (t, a, b) => rep(t, a, b);
  M.brick = std('#ffffff', { map: tex(brickTex(3), 2, 2), roughness: 0.95 }); M.brick2 = std('#ffffff', { map: tex(brickTex(8, '#4a3a33'), 2, 2), roughness: 0.95 });
  M.corr = std('#ffffff', { map: tex(corrTex(5), 3, 1), roughness: 0.55, metalness: 0.35 }); M.corrRust = std('#ffffff', { map: tex(corrTex(6, '#6b6660', 1.0), 3, 1), roughness: 0.7, metalness: 0.25 });
  M.corrBlue = std('#ffffff', { map: tex(corrTex(12, '#6f8396', 0.05), 4, 1), roughness: 0.5, metalness: 0.35 });
  M.conc = std('#ffffff', { map: tex(concTex(7), 6, 6), roughness: 0.95 }); M.stone = std('#ffffff', { map: tex(stoneTex(9), 8, 1), roughness: 1 });
  M.iron = std('#2b2f36', { roughness: 0.75, metalness: 0.3 }); M.dark = std('#23272e', { roughness: 0.85 }); return M; }
// mặt khối có vân lặp theo kích thước (UV theo mét)
function tbox(w, h, d, mat, x, y, z, parent, k = 0.2) { const g = new THREE.BoxGeometry(w, h, d), uv = g.attributes.uv, n = g.attributes.normal;
  for (let i = 0; i < uv.count; i++) { const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)); const su = ax > 0.5 ? d : w, sv = ay > 0.5 ? d : h; uv.setXY(i, uv.getX(i) * su * k, uv.getY(i) * sv * k); }
  const m = new THREE.Mesh(g, mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; (parent || window.__scene).add(m); return m; }
// khói/hơi nước bốc lên (chuỗi sprite lặp theo thời gian)
function plume(scene, x, y, z, { n = 14, color = '#c9ced8', op = 0.32, rise = 0.9, drift = 0.35, size = 2.2, seed = 3 } = {}) {
  const R = rng(seed), tex = softTex(), S = [];
  for (let i = 0; i < n; i++) { const m = new THREE.SpriteMaterial({ map: tex, color, transparent: true, opacity: 0, depthWrite: false }); const s = new THREE.Sprite(m); scene.add(s); S.push({ s, ph: i / n, j: R() }); }
  const update = (t) => S.forEach(({ s, ph, j }) => { const u = (ph + t * 0.06 * rise) % 1; s.position.set(x + u * 9 * drift + Math.sin(t * 0.4 + j * 6) * 0.3, y + u * 9 * rise, z - u * 2); s.scale.setScalar(size * (0.5 + u * 2.2)); s.material.opacity = op * Math.sin(Math.PI * Math.min(1, u * 1.15)) * (0.7 + 0.3 * j); });
  update(0); return { update };
}
function sparks(scene, R, n = 600, color = '#ffc067', size = 0.09) { const pos = new Float32Array(n * 3), seed = [...Array(n)].map(() => [R(), R(), R(), R()]); const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const pts = new THREE.Points(g, new THREE.PointsMaterial({ color, size, transparent: true, opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending })); scene.add(pts);
  return (t, o, k = 1) => { pts.material.opacity = 0.95 * k; seed.forEach(([a, b, c, d], i) => { const u = (t * (0.6 + a * 0.8) + d) % 1, ang = a * 6.28, sp = 3 + b * 6; pos[i * 3] = o.x + Math.cos(ang) * sp * u * 0.8; pos[i * 3 + 1] = o.y + (2 + c * 5) * u - 7.8 * u * u; pos[i * 3 + 2] = o.z + Math.sin(ang) * sp * u * 0.6; }); g.attributes.position.needsUpdate = true; }; }
// ánh sáng theo giờ: dusk (chạng vạng), night, blue (giờ xanh), day
const TOD = {
  dusk: { fog: '#1b2233', fd: 0.0085, sky: [[0, '#0b1222'], [0.36, '#1c2a46'], [0.46, '#4a4560'], [0.495, '#c8784a'], [0.505, '#e39654'], [0.53, '#202434'], [1, '#0e121b']], hemi: ['#7f8fc0', '#2a2418', 2.6], sun: ['#ffb383', 2.4, [-120, 30, -160]], lit: 1, grade: GRADE_K2_WARM, exp: 1.35 },
  night: { fog: '#0d1320', fd: 0.0095, sky: [[0, '#05080f'], [0.4, '#0b1222'], [0.49, '#1c2438'], [0.51, '#141a26'], [1, '#080b12']], hemi: ['#4a5a86', '#1a140e', 1.3], sun: ['#8fa8d8', 0.7, [80, 60, -120]], lit: 1.4, grade: GRADE_K2_WARM, exp: 1.5 },
  blue: { fog: '#1d2a3e', fd: 0.0075, sky: [[0, '#0a1430'], [0.38, '#1e3460'], [0.47, '#4f6a96'], [0.5, '#8aa3c4'], [0.52, '#2a3446'], [1, '#121820']], hemi: ['#9ab4e0', '#3a4256', 2.6], sun: ['#a9c2ee', 1.2, [60, 50, -80]], lit: 0.8, grade: GRADE_K2, exp: 1.25 },
  day: { fog: '#9fb2c8', fd: 0.0042, sky: [[0, '#4d77a8'], [0.4, '#8fb0d4'], [0.5, '#d9e2ea'], [0.52, '#b7c3cc'], [1, '#6e7a84']], hemi: ['#cfe0ff', '#5a5040', 2.2], sun: ['#fff1dc', 3.2, [-80, 120, 60]], lit: 0.15, grade: GRADE_K2_DAY, exp: 1.0 },
};
function lightTod(scene, T, ext = 140) { scene.add(new THREE.HemisphereLight(...T.hemi)); const sun = new THREE.DirectionalLight(T.sun[0], T.sun[1]); sun.position.set(...T.sun[2]); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext * 0.7, bottom: -ext * 0.7, far: 500 }); sun.shadow.bias = -0.0004; scene.add(sun); return sun; }
// cây trụi (thân + chùm nón thưa), instanced
function trees(scene, pts, R, col = '#262a24') { const tr = new THREE.CylinderGeometry(0.12, 0.2, 3, 5); tr.translate(0, 1.5, 0); const cr = new THREE.IcosahedronGeometry(1.4, 0); cr.translate(0, 3.6, 0);
  const A = new THREE.InstancedMesh(tr, std('#2a221c', { roughness: 1 }), pts.length), B = new THREE.InstancedMesh(cr, std(col, { roughness: 1, flatShading: true }), pts.length), Mx = new THREE.Matrix4();
  pts.forEach(([x, y, z], i) => { const s = 0.7 + R() * 0.7; Mx.compose(V3([x, y, z]), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, R() * 6, 0)), V3([s, s * (0.8 + R() * 0.5), s])); A.setMatrixAt(i, Mx); B.setMatrixAt(i, Mx); });
  A.castShadow = B.castShadow = true; scene.add(A, B); }

// ======================= valley =======================
function blastFurnace(parent, x, z, s, mt) {
  const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g); const shell = std('#4d535c', { roughness: 0.6, metalness: 0.35 });
  const prof = [[0, 0], [2.0, 0], [2.0, 2.2], [2.5, 3.2], [2.5, 7.0], [1.6, 11.5], [1.2, 12.5], [1.2, 13.2], [0, 13.2]].map(([a, b]) => new THREE.Vector2(a * s, b * s));
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 28), shell); body.castShadow = body.receiveShadow = true; g.add(body);
  for (let k = 0; k < 6; k++) { const r = new THREE.Mesh(new THREE.TorusGeometry(2.52 * s, 0.07 * s, 6, 40), mt.dark); r.rotation.x = Math.PI / 2; r.position.y = (3.6 + k * 0.62) * s; g.add(r); }
  box(5.6 * s, 0.25 * s, 5.6 * s, mt.dark, 0, 7.4 * s, 0, g); for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) box(0.25 * s, 7.4 * s, 0.25 * s, mt.dark, a * 2.6 * s, 3.7 * s, b * 2.6 * s, g);
  for (let k = 0; k < 4; k++) { const u = cyl(0.22 * s, 0.22 * s, 4.6 * s, mt.dark, (k - 1.5) * 0.7 * s, 15.4 * s, 0, g, 10); u.rotation.z = (k - 1.5) * 0.12; }
  const dc = cyl(0.45 * s, 0.45 * s, 9 * s, mt.dark, 3.8 * s, 12 * s, 0, g, 12); dc.rotation.z = -0.55;
  for (let k = 0; k < 3; k++) { const st = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [1.25, 0], [1.25, 10.5], [0.9, 11.6], [0, 12.0]].map(([a, b]) => new THREE.Vector2(a * s, b * s)), 20), std('#5b6168', { roughness: 0.55, metalness: 0.3 })); st.position.set((-4.2 - k * 2.8) * s, 0, -3 * s); st.castShadow = true; g.add(st); }
  const skip = box(0.9 * s, 0.5 * s, 18 * s, mt.dark, 0, 6.5 * s, 9 * s, g); skip.rotation.x = 0.68;
  tbox(7 * s, 3.2 * s, 5 * s, mt.brick, 0, 1.6 * s, 3.8 * s, g, 0.35);   // nhà đúc gang (gạch)
  box(1.2 * s, 0.8 * s, 0.2 * s, basic('#ff9a3c'), 0, 1.0 * s, 6.35 * s, g);
  const gl = glowSprite('#ff8a30', 1.0, 6 * s); gl.position.set(0, 1.2 * s, 7.2 * s); g.add(gl);
  const pl = new THREE.PointLight('#ff8a3a', 60, 26 * s, 1.6); pl.position.set(0, 1.5 * s, 8 * s); g.add(pl);
  return { g, glow: gl, light: pl, top: () => g.localToWorld(V3([0, 14 * s, 0])) };
}
function shed(parent, mt, x, z, w, d, h, rot = 0, lit = 0.4, wall) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = rot; parent.add(g);
  tbox(w, h, d, wall || mt.brick, 0, h / 2, 0, g, 0.35); const n = Math.floor(w / 3), roof = std('#596069', { roughness: 0.7, metalness: 0.2 });
  for (let i = 0; i < n; i++) { const r = box(3.0, 0.15, d, roof, -w / 2 + 1.5 + i * 3, h + 0.7, 0, g); r.rotation.z = 0.42; box(0.1, 1.1, d * 0.96, std('#2a2620', { emissive: '#ff9a46', emissiveIntensity: lit * 0.8 }), -w / 2 + 2.9 + i * 3, h + 0.55, 0, g); }
  for (let i = 0; i < n * 2; i++) for (const yy of [0.35, 0.62]) box(0.55, 0.7, 0.05, std('#1d1a17', { emissive: '#ffa34d', emissiveIntensity: lit * (0.5 + 0.5 * ((i * 7 + yy * 10) % 3 > 1)) }), -w / 2 + 0.9 + i * 1.5, h * yy, d / 2 + 0.03, g);
  return g;
}
async function valley({ W, H, dur, opt }) {
  const T = TOD[opt.tod || 'dusk'], mt = mats(); const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, T.fog, T.fd); skyDome(scene, T.sky); const R = rng(11);
  const riverZ = (x) => 6 * Math.sin(x * 0.035) + 2 * Math.sin(x * 0.11 + 1);
  const hY = (x, z) => { const dz = Math.abs(z - riverZ(x)); let y = dz < 9 ? -0.6 : Math.pow(Math.min(1, (dz - 9) / 70), 1.35) * 34 + 3 * Math.sin(x * 0.07 + z * 0.05) * Math.min(1, (dz - 9) / 20);
    if (dz > 9 && dz < 26 && z > riverZ(x)) y = Math.min(y, 1.2 + (dz - 9) * 0.05); return y; };
  const tg = new THREE.PlaneGeometry(520, 300, 260, 150); tg.rotateX(-Math.PI / 2); const P = tg.attributes.position, col = [];
  const cLow = new THREE.Color(opt.tod === 'day' ? '#4a5040' : '#1d2620'), cHi = new THREE.Color(opt.tod === 'day' ? '#6a6a58' : '#38403a'), cMud = new THREE.Color('#3a3026');
  for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i), y = hY(x, z); P.setY(i, y); const dz = Math.abs(z - riverZ(x)); const k = Math.min(1, Math.max(0, y / 30)); const c = cLow.clone().lerp(cHi, k); if (dz > 8 && dz < 11.5) c.lerp(cMud, 0.7); col.push(c.r, c.g, c.b); }
  tg.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); tg.computeVertexNormals();
  const terr = new THREE.Mesh(tg, std('#ffffff', { vertexColors: true, roughness: 1 })); terr.receiveShadow = true; scene.add(terr);
  const water = new THREE.Mesh(new THREE.PlaneGeometry(520, 300), std(opt.tod === 'day' ? '#3b5368' : '#15202e', { roughness: 0.16, metalness: 0.7 })); water.rotation.x = -Math.PI / 2; water.position.y = -0.25; scene.add(water);
  // gợn sóng: vệt sáng mảnh trôi trên mặt nước
  const rip = new THREE.InstancedMesh(new THREE.PlaneGeometry(1.6, 0.05), basic(opt.tod === 'day' ? '#c9d6e2' : '#7d8ca6', { transparent: true, opacity: 0.35, depthWrite: false }), 260); const ripS = [];
  for (let i = 0; i < 260; i++) ripS.push([-140 + R() * 280, (R() - 0.5) * 14, R()]); scene.add(rip);
  // kè đá + đá hộc dọc bờ gần, bến gỗ
  const bz = (x) => riverZ(x) + 15;
  for (let x = -150; x < 150; x += 6) { const z0 = riverZ(x) + 9.6, z1 = riverZ(x + 6) + 9.6, a = Math.atan2(z1 - z0, 6); const w = tbox(6.1, 2.2, 0.8, mt.stone, x + 3, 0.3, (z0 + z1) / 2, scene, 0.5); w.rotation.y = -a; }
  const rock = new THREE.InstancedMesh(new THREE.DodecahedronGeometry(0.5, 0), std('#4b4a46', { roughness: 1, flatShading: true }), 700), Mx = new THREE.Matrix4();
  for (let i = 0; i < 700; i++) { const x = -150 + R() * 300, side = R() < 0.6 ? 1 : -1, z = riverZ(x) + side * (8.6 + R() * 1.6); const s = 0.4 + R() * 1.1; Mx.compose(V3([x, -0.3 + R() * 0.3, z]), new THREE.Quaternion().setFromEuler(new THREE.Euler(R() * 3, R() * 3, R() * 3)), V3([s, s * 0.7, s])); rock.setMatrixAt(i, Mx); }
  rock.receiveShadow = rock.castShadow = true; scene.add(rock);
  const wood = std('#3a2c22', { roughness: 0.95 });
  for (const x of [-48, 4, 36]) { const z = riverZ(x) + 8.8; box(3, 0.25, 7, wood, x, 0.9, z - 2.5); for (const dx of [-1.3, 1.3]) for (const dz of [-5.5, -2.5, 0.5]) cyl(0.12, 0.12, 2.4, wood, x + dx, -0.2, z + dz, scene, 6); }
  // sà lan than (ban ngày neo đậu; đêm Homestead: đoàn sà lan trôi)
  const barges = [];
  for (let i = 0; i < (opt.barges ? 3 : 5); i++) { const g = new THREE.Group(); const x = -70 + i * 26, z = riverZ(x) + (opt.barges ? 0 : 5.5); g.position.set(x, -0.1, z); g.rotation.y = -Math.atan(0.21 * Math.cos(x * 0.035)) * 0;
    tbox(12, 1.2, 3.6, mt.corrRust, 0, 0.3, 0, g, 0.4); const coal = box(11, 0.7, 3.0, std('#141414', { roughness: 1 }), 0, 1.1, 0, g); coal.scale.y = opt.barges ? 0.2 : 1;
    if (opt.barges && i === 0) { tbox(4, 2.4, 3.2, mt.corr, 3, 2.0, 0, g, 0.4); const lamp = glowSprite('#ffd08a', 0.9, 1.6); lamp.position.set(3, 3.6, 1.8); g.add(lamp); }
    scene.add(g); barges.push({ g, x0: x }); }
  // nhà máy trên bậc ven sông gần
  const mill = new THREE.Group(); scene.add(mill);
  const BF = [-14, -2, 10].map((x, i) => blastFurnace(mill, x, bz(x), 0.85 + 0.08 * (i % 2), mt));
  shed(mill, mt, 26, bz(26) + 2, 24, 12, 8, 0.05, 0.5 * T.lit); shed(mill, mt, -36, bz(-36) + 3, 30, 14, 9, -0.04, 0.35 * T.lit, mt.brick2); shed(mill, mt, 2, bz(2) + 15, 40, 10, 6, 0, 0.25 * T.lit, mt.corrRust);
  tbox(8, 5, 6, mt.brick2, 44, 2.5, bz(44) + 4, mill, 0.35);   // nhà điện
  const stacks = [];
  for (const [x, dz, h] of [[18, 8, 26], [21, 8, 26], [24, 8, 26], [-28, 10, 22], [-25, 10, 22]]) { const st = cyl(0.7, 1.0, h, mt.brick, x, h / 2, bz(x) + dz, mill, 14); st.castShadow = true; box(0.6, 0.3, 0.6, basic('#ff3b2a'), x, h + 0.2, bz(x) + dz, mill); stacks.push([x, h, bz(x) + dz]); }
  const plumes = stacks.map(([x, h, z], i) => plume(scene, x, h + 0.5, z, { seed: 5 + i, op: opt.tod === 'day' ? 0.4 : 0.26, size: 2.4, color: opt.tod === 'day' ? '#d8dde4' : '#c9ced8' }));
  BF.forEach((b, i) => plumes.push(plume(scene, [-14, -2, 10][i], 13.5, bz([-14, -2, 10][i]), { seed: 20 + i, color: '#e0c6b2', op: 0.22, size: 1.8 })));
  const refl = []; const streak = softTex();
  for (const x of [-14, -2, 10]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 18), basic('#ff8a3a', { map: streak, transparent: true, opacity: 0.35 * T.lit, depthWrite: false, blending: THREE.AdditiveBlending })); m.rotation.x = -Math.PI / 2; m.position.set(x, -0.2, riverZ(x) + 2); scene.add(m); refl.push(m); }
  // hai tuyến ray (tà vẹt + ray) dọc bậc ven sông; đoàn toa
  const railM = std('#6f7782', { metalness: 0.6, roughness: 0.4 }), tieG = new THREE.BoxGeometry(0.35, 0.12, 2.4), ties = new THREE.InstancedMesh(tieG, wood, 2 * 300); let ti = 0;
  for (const off of [27, 31]) for (let x = -150; x < 150; x += 4) { const z0 = riverZ(x) + off, z1 = riverZ(x + 4) + off, a = Math.atan2(z1 - z0, 4);
    for (const s of [-0.7, 0.7]) { const r = box(4.05, 0.12, 0.09, railM, x + 2, 0.78, (z0 + z1) / 2 + s); r.rotation.y = -a; }
    for (const k of [0, 2]) if (ti < 600) { Mx.compose(V3([x + k, 0.66, riverZ(x + k) + off]), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, -a, 0)), V3([1, 1, 1])); ties.setMatrixAt(ti++, Mx); } }
  ties.count = ti; ties.receiveShadow = true; scene.add(ties);
  const cars = [], cars2 = [];
  for (let i = 0; i < 16; i++) { const c = new THREE.Group(); tbox(3.2, 1.3, 2.0, mt.corrRust, 0, 1.5, 0, c, 0.5); box(3.0, 0.3, 1.8, std('#5a3a2a'), 0, 2.25, 0, c); for (const w of [-1, 1]) cyl(0.35, 0.35, 2.1, M.iron, w * 1.1, 0.85, 0, c, 10).rotation.x = Math.PI / 2; scene.add(c); cars.push(c); }
  for (let i = 0; i < 8; i++) { const c = new THREE.Group(); tbox(3.6, 1.8, 2.0, i ? mt.corr : M.iron, 0, 1.75, 0, c, 0.5); if (!i) { cyl(0.45, 0.45, 2.5, M.iron, 0.2, 2.9, 0, c, 10); } scene.add(c); cars2.push(c); }
  const loco = glowSprite('#fff0c8', 0.9, 2.2); scene.add(loco);
  // cầu giàn
  const br = new THREE.Group(); br.position.set(46, 0, riverZ(46)); br.rotation.y = Math.PI / 2 + 0.25; scene.add(br); const bm = std('#545b63', { metalness: 0.4, roughness: 0.6 });
  box(46, 0.6, 5, bm, 0, 6, 0, br); for (const s of [-2.4, 2.4]) { box(46, 0.3, 0.3, bm, 0, 11, s, br); for (let i = -11; i <= 11; i++) { const d = box(0.25, 5.6, 0.25, bm, i * 2, 8.5, s, br); d.rotation.z = (i % 2 ? 0.38 : -0.38); } }
  for (const x of [-12, 12]) tbox(2.6, 6.5, 6, mt.stone, x, 3, 0, br, 0.5);
  // thị trấn bên kia sông (nhà gạch/gỗ) + cửa sổ ấm
  const houseG = new THREE.BoxGeometry(1.6, 1.4, 1.4), roofG = new THREE.ConeGeometry(1.25, 0.9, 4); roofG.rotateY(Math.PI / 4);
  const NH = 460, hs = new THREE.InstancedMesh(houseG, std('#ffffff', { map: rep(brickTex(21, '#6a5446'), 0.5, 0.5), roughness: 0.95 }), NH), rf = new THREE.InstancedMesh(roofG, std('#2b2d33'), NH);
  const winPts = []; const q = new THREE.Quaternion(), e = new THREE.Euler(), housePts = [];
  for (let i = 0; i < NH; i++) { const x = -130 + R() * 260, dz = 12 + R() * 34, z = riverZ(x) - dz; const y = hY(x, z);
    e.set(0, R() * 0.6 - 0.3, 0); q.setFromEuler(e); Mx.compose(V3([x, y + 0.7, z]), q, V3([1, 1, 1])); hs.setMatrixAt(i, Mx); Mx.compose(V3([x, y + 1.85, z]), q, V3([1, 1, 1])); rf.setMatrixAt(i, Mx);
    if (R() < 0.55) winPts.push(x + 0.4, y + 0.8, z + 0.72); housePts.push([x, y, z]); }
  hs.castShadow = hs.receiveShadow = true; scene.add(hs, rf);
  const wg = new THREE.BufferGeometry(); wg.setAttribute('position', new THREE.Float32BufferAttribute(winPts, 3));
  scene.add(new THREE.Points(wg, new THREE.PointsMaterial({ color: '#ffc47a', size: 0.35, transparent: true, opacity: 0.95 * Math.min(1, T.lit), depthWrite: false })));
  const church = new THREE.Group(); church.position.set(-20, hY(-20, riverZ(-20) - 30), riverZ(-20) - 30); scene.add(church); tbox(4, 4, 7, mt.brick2, 0, 2, 0, church, 0.4); cyl(0.01, 1.4, 5, mt.dark, 0, 8.5, -3, church, 4); tbox(1.8, 6, 1.8, mt.brick2, 0, 3, -3, church, 0.4);
  // cây trụi rải trên sườn đồi và bờ xa
  const TP = []; for (let i = 0; i < 520; i++) { const x = -200 + R() * 400, side = R() < 0.65 ? -1 : 1, dz = 10 + R() * 90, z = riverZ(x) + side * dz; if (side > 0 && dz < 40) continue; TP.push([x, hY(x, z), z]); }
  trees(scene, TP, R, opt.tod === 'day' ? '#4a4a3a' : '#262a24');
  // khu lò cốc tổ ong (Connellsville, dựng tách ở x ≈ −130 trên bậc gần): dãy vòm gạch, miệng lò đỏ, khói thấp
  const coke = new THREE.Group(); coke.position.set(-132, 0, bz(-132) + 4); scene.add(coke); const dome = new THREE.SphereGeometry(1.5, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2); const ovens = [];
  for (let r = 0; r < 2; r++) for (let i = 0; i < 26; i++) { const x = -26 + i * 2.05, z = r * 4.4; const d = new THREE.Mesh(dome, mt.brick); d.position.set(x, 0.9, z); d.castShadow = d.receiveShadow = true; coke.add(d); tbox(2.05, 0.9, 3.4, mt.brick2, x, 0.45, z, coke, 0.4);
    const mouth = box(0.7, 0.55, 0.05, basic('#ff7a2a'), x, 0.55, z + (r ? 1.72 : -1.72), coke); ovens.push(mouth); }
  const cokeGlow = new THREE.PointLight('#ff7a30', 40, 30, 1.6); cokeGlow.position.set(0, 2, 6.5); coke.add(cokeGlow);
  const cokePl = [-20, -6, 8, 20].map((x, i) => plume(scene, -132 + x, 2.2, bz(-132) + 6, { seed: 40 + i, op: 0.16, size: 2.0, rise: 0.7, drift: 0.6, color: '#b9b2aa' }));
  for (let x = -30; x <= 30; x += 3) for (const z of [-3.6, 8]) { const p = box(0.2, 1.8, 0.2, wood, x, 0.9, z, coke); }
  // ánh sáng
  lightTod(scene, T, 160);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [-46, 30, -52], l: [-4, 4, 16], mm: 28 }, { u: 1, p: [-38, 25, -44], l: [-2, 5, 16], mm: 30 }]);
  const dst = dust(scene, [0, 6, 20], [120, 16, 60], 300, 7, opt.tod === 'day' ? '#e8e4dc' : '#ffcf9e');
  const anchors = { furnace: () => BF[1].top(), furnaceL: () => BF[0].top(), works: V3([26, 10, bz(26) + 2]), railA: V3([-20, 1.5, riverZ(-20) + 27]), railB: V3([-8, 1.5, riverZ(-8) + 31]),
    river: V3([-30, 0, riverZ(-30)]), town: V3([-10, 16, riverZ(-10) - 34]), coke: V3([-132, 3.5, bz(-132) + 4]), bridge: V3([46, 12, riverZ(46)]), barge: () => barges[0].g.position.clone().add(V3([0, 2.5, 0])), stack: V3([21, 27, bz(21) + 8]) };
  const update = (t, f) => { rig.at(t); plumes.forEach((p) => p.update(t)); cokePl.forEach((p) => p.update(t)); dst.update(t);
    BF.forEach((b, i) => { const k = 1 + 0.08 * Math.sin(f * 0.37 + i * 2) + 0.05 * Math.sin(f * 0.13 + i); b.light.intensity = 60 * k * T.lit; b.glow.material.opacity = Math.min(1, 0.9 * k * T.lit); refl[i].material.opacity = 0.2 * k * T.lit; });
    ovens.forEach((o, i) => { o.material.color.setRGB(1, 0.42 + 0.1 * Math.sin(t * 2 + i), 0.15); }); cokeGlow.intensity = 40 * (1 + 0.1 * Math.sin(t * 3));
    ripS.forEach(([x, z, ph], i) => { const xx = ((x + t * 1.2 + 140) % 280) - 140; Mx.compose(V3([xx, -0.2, riverZ(xx) + z]), new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI / 2, 0, 0)), V3([1, 1, 1])); rip.setMatrixAt(i, Mx); }); rip.instanceMatrix.needsUpdate = true;
    cars.forEach((c, i) => { const x = -70 + i * 3.6 + t * 1.6, z = riverZ(x) + 27, z2 = riverZ(x + 1) + 27; c.position.set(x, 0, z); c.rotation.y = -Math.atan2(z2 - z, 1); });
    cars2.forEach((c, i) => { const x = 90 - i * 3.9 - t * 2.2, z = riverZ(x) + 31, z2 = riverZ(x + 1) + 31; c.position.set(x, 0, z); c.rotation.y = -Math.atan2(z2 - z, 1); if (!i) loco.position.set(x - 2, 2.2, z); });
    barges.forEach(({ g, x0 }, i) => { if (opt.barges) { const x = x0 - 40 + t * 0.9; g.position.set(x, -0.1, riverZ(x) + 1); } }); };
  return { scene, cam: rig.cam, update, grade: T.grade, exposure: T.exp, anchors };
}

// ======================= ingots =======================
async function ingots({ W, H, dur, opt }) {
  const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.006);
  const floor = box(200, 0.2, 200, std('#ffffff', { map: gridTex('#121b28', 7), roughness: 0.85 }), 0, -0.1, 0); floor.receiveShadow = true;
  const ing = new THREE.BoxGeometry(1.6, 0.5, 0.7); ing.translate(0, 0.25, 0);
  const steelTex = rep(canvasTex(256, 128, (g, w, h) => { const R = rng(31); g.fillStyle = '#8e9aa8'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '40,46,54' : '220,228,236'},${0.05 + R() * 0.08})`; g.fillRect(R() * w, R() * h, 2 + R() * 18, 1); } }), 1, 1);
  const mSteel = std('#ffffff', { map: steelTex, roughness: 0.38, metalness: 0.55 }), mUS = std(C.orange, { roughness: 0.45, metalness: 0.25, emissive: '#5a2a10', emissiveIntensity: 0.6 });
  const pile = (n, cols, rows, ox, oz) => { const L = []; for (let i = 0; i < n; i++) { const layer = Math.floor(i / (cols * rows)), j = i % (cols * rows); const c = j % cols, r = Math.floor(j / cols); L.push([ox + (c - (cols - 1) / 2) * 1.75 + (layer % 2 ? 0.12 : 0), layer * 0.52, oz + ((rows - 1) / 2 - r) * 0.85]); } return L; };
  const PL = (opt.piles || [{ x: -16, z: 0, n: 19, us: 9, cols: 3, rows: 3, grow: -1 }, { x: 8, z: -2, n: 185, us: 8, cols: 5, rows: 4, grow: 1 }]).map((p) => ({ ...p, pts: pile(p.n, p.cols, p.rows, p.x, p.z) }));
  const N = PL.reduce((a, p) => a + p.n, 0);
  const steelIM = new THREE.InstancedMesh(ing, mSteel, N), usIM = new THREE.InstancedMesh(ing, mUS, N); steelIM.castShadow = usIM.castShadow = steelIM.receiveShadow = usIM.receiveShadow = true;
  scene.add(steelIM, usIM); const Mx = new THREE.Matrix4(), Z = new THREE.Matrix4().makeScale(0, 0, 0);
  PL.forEach((p) => box(p.cols * 1.75 + 1.6, 0.25, p.rows * 0.85 + 1.6, std('#1a2433', { roughness: 0.6 }), p.x, 0.0, p.z));
  const place = (t) => { let k = 0; PL.forEach((p) => p.pts.forEach((q, i) => { const g = p.grow < 0 ? 1 : ease((t - p.grow - i * Math.min(0.018, 2.5 / p.n)) / 0.45); const isUS = i < p.us;
    Mx.makeTranslation(q[0], q[1] + (1 - g) * 3, q[2]); if (g <= 0) Mx.copy(Z); steelIM.setMatrixAt(k, isUS ? Z : Mx); usIM.setMatrixAt(k, isUS ? Mx : Z); k++; }));
    steelIM.instanceMatrix.needsUpdate = usIM.instanceMatrix.needsUpdate = true; };
  scene.add(new THREE.HemisphereLight('#7f93b8', '#1a2230', 1.6));
  const keyL = new THREE.SpotLight('#ffffff', 2600, 160, 0.7, 0.6, 1.4); keyL.position.set(-18, 40, 28); keyL.target.position.set(0, 0, 0); keyL.castShadow = true; keyL.shadow.mapSize.set(2048, 2048); scene.add(keyL, keyL.target);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.9); rim.position.set(30, 12, -40); scene.add(rim);
  const warm = new THREE.PointLight(C.orange, 30, 22, 1.5); warm.position.set(PL[0].x + 2, 4, PL[0].z + 4); scene.add(warm);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [-25, 5.5, 12], l: [-16, 2.5, 0], mm: 36 }, { u: 1, p: [-15, 15, 31], l: [-2, 3.5, -1], mm: 30 }]);
  const dst = dust(scene, [0, 6, 0], [50, 12, 30], 220, 7, '#b9c6d6');
  const anchors = {}; PL.forEach((p, i) => { const top = Math.ceil(p.n / (p.cols * p.rows)) * 0.52; anchors['pile' + i] = V3([p.x, top + 0.6, p.z]); anchors['base' + i] = V3([p.x, 0, p.z + p.rows * 0.43 + 0.8]); anchors['us' + i] = V3([p.x, 0.5, p.z + p.rows * 0.43]); });
  const update = (t) => { rig.at(t); place(t); dst.update(t); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.1, anchors };
}

// ======================= chain =======================
const LLp = ([lon, lat]) => [(lon + 84) * Math.cos(44 * Math.PI / 180) * 69 / 50, -(lat - 44) * 69 / 50];
const LAKES = {
  superior: [[-92.1, 46.7], [-91.2, 46.9], [-90.4, 46.6], [-89.4, 46.9], [-88.4, 47.2], [-87.6, 46.5], [-86.6, 46.45], [-85.4, 46.75], [-84.6, 46.5], [-84.6, 46.95], [-84.9, 47.6], [-85.8, 47.95], [-86.7, 48.7], [-88.3, 48.8], [-89.3, 48.1], [-90.3, 47.7], [-91.6, 47.1]],
  michigan: [[-85.4, 45.9], [-86.2, 45.8], [-87.3, 45.6], [-87.6, 44.9], [-87.8, 44.1], [-87.9, 43.0], [-87.8, 42.3], [-87.5, 41.75], [-86.9, 41.65], [-86.4, 42.2], [-86.25, 43.0], [-86.45, 43.8], [-86.1, 44.6], [-85.6, 45.2], [-85.0, 45.75]],
  huron: [[-84.7, 45.9], [-84.0, 46.0], [-83.0, 46.1], [-81.6, 46.1], [-80.6, 45.9], [-80.0, 45.2], [-80.6, 44.6], [-81.3, 44.9], [-81.7, 44.3], [-81.7, 43.3], [-82.4, 43.0], [-82.7, 43.7], [-83.5, 43.9], [-83.4, 44.6], [-83.3, 45.1], [-84.2, 45.6]],
  erie: [[-83.45, 41.75], [-82.8, 41.5], [-81.7, 41.5], [-80.6, 41.95], [-79.9, 42.15], [-79.05, 42.75], [-79.4, 42.85], [-80.5, 42.55], [-81.6, 42.65], [-82.5, 42.05], [-83.15, 42.05]],
  ontario: [[-79.8, 43.3], [-79.2, 43.25], [-78.0, 43.35], [-76.8, 43.4], [-76.2, 43.6], [-76.4, 44.1], [-77.4, 43.9], [-78.8, 43.9], [-79.5, 43.65]],
};
async function chain({ W, H, dur, opt }) {
  const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.004); const R = rng(17);
  // nền đất: lưới bản đồ + vân địa hình nhẹ (vertex), vùng mỏ quặng và vùng than tô đậm
  const lg = new THREE.PlaneGeometry(64, 44, 128, 88); lg.rotateX(-Math.PI / 2); const P = lg.attributes.position;
  for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i); P.setY(i, 0.12 * Math.sin(x * 0.9 + z * 0.4) * Math.sin(z * 0.7) + (x > 4 && z > 4 ? 0.25 * Math.max(0, Math.sin(x * 0.5) * Math.cos(z * 0.6)) : 0)); }
  lg.computeVertexNormals(); const land = new THREE.Mesh(lg, std('#ffffff', { map: rep(canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = '#3a4a5e'; g.fillRect(0, 0, w, h); const R2 = rng(4); for (let i = 0; i < 3000; i++) { g.fillStyle = `rgba(${R2() < 0.5 ? '20,30,40' : '120,140,160'},0.05)`; g.fillRect(R2() * w, R2() * h, 3, 3); } for (let i = 0; i <= w; i += 64) { g.strokeStyle = 'rgba(220,230,240,0.14)'; g.lineWidth = 1; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }), 2, 2), roughness: 0.9 }));
  land.position.set(-4, -0.1, -2); land.receiveShadow = true; scene.add(land);
  const lakeM = std('#0c1a2c', { roughness: 0.12, metalness: 0.4 });
  for (const pts of Object.values(LAKES)) { const sh = new THREE.Shape(pts.map((p) => { const [x, z] = LLp(p); return new THREE.Vector2(x, -z); }));
    const g = new THREE.ExtrudeGeometry(sh, { depth: 0.14, bevelEnabled: false }); g.rotateX(-Math.PI / 2); const m = new THREE.Mesh(g, lakeM); m.position.y = 0.04; scene.add(m);
    const lg2 = new THREE.BufferGeometry().setFromPoints(pts.concat([pts[0]]).map((p) => { const [x, z] = LLp(p); return new THREE.Vector3(x, 0.2, z); })); scene.add(new THREE.Line(lg2, new THREE.LineBasicMaterial({ color: '#9fc3e0' }))); }
  // sông Ohio/Monongahela/Allegheny giản lược quanh Pittsburgh
  const riv = (pts) => { const cv = new THREE.CatmullRomCurve3(pts.map((p) => { const [x, z] = LLp(p); return new THREE.Vector3(x, 0.16, z); })); scene.add(new THREE.Mesh(new THREE.TubeGeometry(cv, 80, 0.06, 6, false), basic('#6f9cc6'))); };
  riv([[-79.6, 41.2], [-79.8, 40.8], [-80.0, 40.44]]); riv([[-79.9, 39.6], [-79.95, 40.0], [-80.0, 40.44]]); riv([[-80.0, 40.44], [-80.3, 40.6], [-80.7, 40.65], [-81.0, 40.4]]);
  const route = (pts, y = 0.38) => new THREE.CatmullRomCurve3(pts.map((p) => { const [x, z] = LLp(p); return new THREE.Vector3(x, y, z); }), false, 'catmullrom', 0.2);
  const RT = { ore: route([[-92.9, 47.45], [-92.4, 47.1], [-92.05, 46.78]]),
    boat: route([[-92.0, 46.8], [-90.0, 47.25], [-87.5, 47.6], [-85.6, 46.95], [-84.4, 46.45], [-83.9, 45.95], [-82.9, 45.3], [-82.4, 44.0], [-82.45, 43.1], [-82.65, 42.35], [-82.6, 41.95], [-81.6, 41.85], [-80.6, 42.0]], 0.32),
    rail: route([[-80.6, 41.95], [-80.4, 41.4], [-80.2, 40.9], [-80.0, 40.44]]), coke: route([[-79.6, 40.02], [-79.8, 40.25], [-80.0, 40.44]]), lime: route([[-78.3, 40.55], [-78.9, 40.5], [-79.5, 40.45], [-80.0, 40.44]]) };
  const COL = { ore: C.orange, boat: C.orange, rail: C.orange, coke: C.amber, lime: C.steel };
  const tubes = Object.entries(RT).map(([k, cv]) => { const r = k === 'boat' ? 0.13 : 0.11; const g = new THREE.TubeGeometry(cv, 240, r, 8, false); const m = new THREE.Mesh(g, basic(COL[k])); scene.add(m);
    const gl = new THREE.Mesh(new THREE.TubeGeometry(cv, 240, r * 3.2, 8, false), basic(COL[k], { transparent: true, opacity: 0.16, depthWrite: false, blending: THREE.AdditiveBlending })); scene.add(gl); return { k, g, gl: gl.geometry, n: g.index.count, cv }; });
  const node = (p, c, r = 0.32) => { const [x, z] = LLp(p); const m = cyl(r, r, 0.5, basic(c), x, 0.32, z, scene, 24); const s = glowSprite(c, 0.9, 1.6); s.position.set(x, 0.62, z); scene.add(s); return { m, s, v: V3([x, 0.4, z]) }; };
  const ND = { ore: node([-92.9, 47.45], C.orange), duluth: node([-92.05, 46.78], C.steel, 0.22), erie: node([-80.6, 41.95], C.steel, 0.22), coke: node([-79.6, 40.02], C.amber), lime: node([-78.3, 40.55], C.steel, 0.24), pitt: node([-80.0, 40.44], C.text, 0.42) };
  // mỏ lộ thiên (bậc), lò cốc nhỏ, nhà máy nhỏ ở Pittsburgh: chi tiết khối trên bản đồ
  const [ox, oz] = LLp([-92.9, 47.45]); for (let k = 0; k < 4; k++) { const r = new THREE.Mesh(new THREE.TorusGeometry(0.5 + k * 0.28, 0.08, 4, 24), std('#7a5a44', { roughness: 1 })); r.rotation.x = Math.PI / 2; r.position.set(ox - 0.9, 0.1 - k * 0.02, oz - 0.6); scene.add(r); }
  const [cx, cz] = LLp([-79.6, 40.02]); for (let i = 0; i < 8; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6, 0, 6.3, 0, 1.6), std('#6a3a28')); d.position.set(cx + 0.6 + i * 0.22, 0.1, cz + 0.5); scene.add(d); }
  const [px, pz] = LLp([-80.0, 40.44]); for (let i = 0; i < 5; i++) { cyl(0.08, 0.1, 0.9 + (i % 2) * 0.3, std('#4d535c'), px - 0.7 + i * 0.3, 0.5, pz + 0.7, scene, 8); } box(1.6, 0.4, 0.6, std('#5a3428'), px - 0.2, 0.25, pz + 1.1);
  const own = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.07, 8, 48), basic(C.amber, { transparent: true, opacity: 0 })); own.rotation.x = Math.PI / 2; own.position.set(cx, 0.4, cz); scene.add(own);
  const ownGl = glowSprite(C.amber, 0, 4.5); ownGl.position.set(cx, 0.5, cz); scene.add(ownGl);
  const boat = new THREE.Group(); box(0.9, 0.18, 0.22, std('#c4ccd6'), 0, 0.44, 0, boat); box(0.18, 0.2, 0.2, std('#e6eaef'), 0.32, 0.62, 0, boat); scene.add(boat);
  const trainA = new THREE.Group(); for (let i = 0; i < 4; i++) box(0.28, 0.14, 0.16, std(i ? '#6a5040' : '#2a2e35'), -i * 0.32, 0.45, 0, trainA); scene.add(trainA);
  scene.add(new THREE.HemisphereLight('#a9bad8', '#1a2230', 2.2));
  const sun = new THREE.DirectionalLight('#dfe8ff', 2.2); sun.position.set(-20, 40, 20); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 30, bottom: -30 }); scene.add(sun);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [-10, 17, 15], l: [-5.5, 0, -1.5], mm: 28 }, { u: 1, p: [-6, 14.5, 14.5], l: [-3, 0, -0.5], mm: 29 }]);
  const D = opt.full ? {} : (opt.draw || { ore: [0, 0.18 * dur], boat: [0.12 * dur, 0.62 * dur], rail: [0.55 * dur, 0.78 * dur], coke: [0.7 * dur, 0.9 * dur], lime: [0.85 * dur, 0.97 * dur] });
  const anchors = { ore: ND.ore.v, duluth: ND.duluth.v, lakes: V3(LLp([-87.6, 47.9]).reduce((a, v, i) => (a[i ? 2 : 0] = v, a), [0, 0.3, 0])), erie: ND.erie.v, coke: ND.coke.v, lime: ND.lime.v, pitt: ND.pitt.v,
    rail1: () => RT.ore.getPointAt(0.5), rail2: () => RT.rail.getPointAt(0.5), boat: () => boat.position.clone() };
  const update = (t) => { rig.at(t);
    tubes.forEach((tb) => { const w = D[tb.k]; const u = opt.full ? 1 : w ? ease((t - w[0]) / Math.max(0.01, w[1] - w[0])) : 0; const k = Math.floor(u * tb.n / 6) * 6; tb.g.setDrawRange(0, k); tb.gl.setDrawRange(0, k); });
    const wb = D.boat || [0, 1]; const ub = opt.full ? (t / dur) % 1 : Math.min(0.999, Math.max(0, (t - wb[0]) / Math.max(0.01, wb[1] - wb[0]))); const p = RT.boat.getPointAt(ub), p2 = RT.boat.getPointAt(Math.min(1, ub + 0.002)); boat.position.copy(p).setY(0); boat.rotation.y = -Math.atan2(p2.z - p.z, p2.x - p.x);
    const wr = D.rail || [0, 1]; const ur = opt.full ? ((t / dur) * 1.7) % 1 : Math.min(0.999, Math.max(0, (t - wr[0]) / Math.max(0.01, wr[1] - wr[0]))); const q = RT.rail.getPointAt(ur), q2 = RT.rail.getPointAt(Math.min(1, ur + 0.01)); trainA.position.copy(q).setY(0); trainA.rotation.y = -Math.atan2(q2.z - q.z, q2.x - q.x);
    const ow = opt.own === undefined ? 1e9 : opt.own; const uo = ease((t - ow) / 0.8); own.material.opacity = uo; ownGl.material.opacity = 0.6 * uo * (0.85 + 0.15 * Math.sin(t * 3)); own.scale.setScalar(1 + 0.05 * Math.sin(t * 2.4)); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.05, anchors };
}

// ======================= furnace =======================
async function furnace({ W, H, dur, opt }) {
  const mt = mats(); const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, '#151a22', 0.028); const R = rng(4);
  tbox(90, 0.2, 70, mt.conc, 0, -0.1, 0, scene, 0.15);
  for (let x = -24; x <= 24; x += 8) for (const z of [-10, 12]) tbox(0.8, 18, 0.8, mt.iron, x, 9, z, scene, 0.5);
  for (let x = -24; x <= 24; x += 8) { box(0.5, 0.6, 22, mt.iron, x, 18, 1); for (let k = -5; k <= 5; k++) { const d = box(0.15, 2.4, 0.15, mt.iron, x, 17, 1 + k * 2); d.rotation.x = k % 2 ? 0.6 : -0.6; } }
  tbox(56, 12, 0.6, mt.brick, 0, 6, -10.6, scene, 0.3); tbox(0.6, 12, 24, mt.brick, -28, 6, 1, scene, 0.3);   // tường gạch nội thất
  box(52, 1.2, 1.0, std('#5a4a2a', { roughness: 0.7 }), 0, 14.5, -9); box(52, 1.2, 1.0, std('#5a4a2a'), 0, 14.5, 11);
  const crane = new THREE.Group(); box(1.4, 1.6, 21, std('#6b5a2c', { roughness: 0.6, metalness: 0.2 }), 0, 15.6, 1, crane); box(2.4, 1.4, 2.4, mt.iron, 0, 14.4, -2, crane); scene.add(crane); cyl(0.04, 0.04, 6, std('#1b1b1b'), 0, 11.0, -2, crane, 6);
  for (let x = -20; x <= 20; x += 8) { box(5, 6, 0.1, basic('#5a7aa6', { transparent: true, opacity: 0.22 }), x, 9.5, -10.25); for (let k = 1; k < 4; k++) box(5, 0.08, 0.12, mt.iron, x, 6.5 + k * 1.5, -10.2); }
  // ánh sáng lọt qua cửa sổ cao (dải sương)
  for (let x = -20; x <= 20; x += 8) { const sh = new THREE.Mesh(new THREE.PlaneGeometry(4, 16), basic('#8fb0e6', { transparent: true, opacity: 0.05, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })); sh.position.set(x + 2, 6, -4); sh.rotation.set(0.5, 0, 0.2); scene.add(sh); }
  const conv = new THREE.Group(); conv.position.set(-2, 5.2, -1); scene.add(conv);
  const prof = [[0, -3.0], [1.4, -2.9], [2.2, -2.2], [2.5, -0.8], [2.4, 0.8], [1.9, 2.0], [1.2, 2.8], [0.95, 3.25], [0.85, 3.3]].map(([a, b]) => new THREE.Vector2(a, b));
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 36), std('#ffffff', { map: rep(corrTex(44, '#4a4f57', 0.8), 6, 2), roughness: 0.5, metalness: 0.5 })); body.castShadow = true; conv.add(body);
  for (const y of [-1.6, -0.2, 1.2]) { const r = new THREE.Mesh(new THREE.TorusGeometry(2.48 - Math.abs(y) * 0.12, 0.09, 6, 40), std('#23262b')); r.rotation.x = Math.PI / 2; r.position.y = y; conv.add(r); }
  const trun = cyl(0.45, 0.45, 7.6, std('#23262b', { metalness: 0.4 }), 0, 0, 0, conv); trun.rotation.x = Math.PI / 2;
  for (const z of [-4.1, 4.1]) tbox(1.0, 5.0, 0.8, mt.brick, -2, 2.5, -1 + z, scene, 0.4);
  const mouthGlow = glowSprite('#ffb04a', 1.0, 5); conv.add(mouthGlow); mouthGlow.position.set(0, 3.5, 0);
  const ladle = new THREE.Group(); ladle.position.set(3.6, 0, -1); scene.add(ladle);
  const lb = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [1.5, 0], [1.75, 2.6], [1.85, 2.7], [0, 2.7]].map(([a, b]) => new THREE.Vector2(a, b)), 28), std('#ffffff', { map: rep(corrTex(45, '#3a3d42', 1), 4, 1), roughness: 0.6, metalness: 0.4 })); lb.castShadow = true; ladle.add(lb);
  cyl(1.68, 1.68, 0.05, basic('#ffcf6a'), 0, 2.45, 0, ladle, 28); const mGlow = glowSprite('#ff9a3a', 0.95, 6); mGlow.position.set(0, 3.2, 0); ladle.add(mGlow);
  const stream = cyl(0.22, 0.32, 1, basic('#ffd27a'), 0, 0, 0, scene, 10); const spk = sparks(scene, R, 700);
  // ingot molds và gang thỏi phía trước (chi tiết sàn)
  for (let i = 0; i < 7; i++) { tbox(0.9, 1.6, 0.9, mt.iron, 9 + i * 1.3, 0.8, 4.5, scene, 0.6); }
  for (let i = 0; i < 40; i++) { const b = box(1.4, 0.3, 0.5, std('#3d3a36', { roughness: 0.9 }), -14 + R() * 6, 0.15 + Math.floor(i / 10) * 0.3, 5 + (i % 10) * 0.55); b.rotation.y = R() * 0.1; }
  const men = [[-8, 3, 0.6], [7.5, 2.0, -0.9], [9, 4.5, -1.4]].map(([x, z, ry], i) => { const f = figure({ color: '#15130f', scale: 1.05 }); f.root.position.set(x, 0, z); f.root.rotation.y = ry; scene.add(f.root); f.set({ armR: i === 0 ? -0.6 : -0.2, armL: -0.15 }); const rl = new THREE.PointLight('#ff9a4a', 5, 4, 1.8); rl.position.set(x + 0.6, 1.5, z - 0.8); scene.add(rl); return f; });
  scene.add(new THREE.HemisphereLight('#4d6290', '#1a120c', 1.4));
  const cold = new THREE.DirectionalLight('#8fb0e6', 1.8); cold.position.set(-10, 20, -30); scene.add(cold);
  const fillW = new THREE.PointLight('#ffb070', 60, 30, 1.5); fillW.position.set(8, 6, 8); scene.add(fillW);
  const hot = new THREE.PointLight('#ff8a32', 260, 40, 1.7); hot.position.set(2, 6, 1); hot.castShadow = true; hot.shadow.mapSize.set(1024, 1024); scene.add(hot);
  const hot2 = new THREE.PointLight('#ffb050', 90, 18, 1.6); hot2.position.set(3.6, 3.6, 0); scene.add(hot2);
  const dst = dust(scene, [1, 6, 0], [20, 10, 12], 400, 9, '#ffcc99');
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [13, 4.0, 12.5], l: [0, 4.2, -1.5], mm: 28 }, { u: 1, p: [10.5, 3.6, 10.5], l: [0.5, 4.0, -1.5], mm: 30 }]);
  const pw = opt.pour || [0, dur]; const mouthW = V3([0, 0, 0]);
  const anchors = { converter: () => conv.localToWorld(V3([0, 3.6, 0])), ladle: V3([3.6, 3.4, -1]), men: V3([8.2, 2.2, 1]) };
  const update = (t, f) => { rig.at(t); dst.update(t);
    const tilt = lerp(0.35, 1.18, ease((t - pw[0]) / Math.max(0.1, pw[1] - pw[0]) * 1.6)); conv.rotation.z = -tilt; conv.updateMatrixWorld(true);
    const pour = tilt > 0.9 ? Math.min(1, (tilt - 0.9) / 0.15) : 0; mouthW.copy(conv.localToWorld(V3([0, 3.3, 0])));
    const bot = V3([3.6, 2.5, -1]); const mid = mouthW.clone().add(bot).multiplyScalar(0.5); stream.position.copy(mid); stream.scale.set(pour, mouthW.distanceTo(bot), pour); stream.lookAt(bot); stream.rotateX(Math.PI / 2); stream.visible = pour > 0.02;
    spk(t, bot.clone().setY(2.7), pour); const fl = 1 + 0.1 * Math.sin(f * 0.9) + 0.06 * Math.sin(f * 0.37); hot.intensity = 260 * fl * (0.5 + 0.5 * pour); hot2.intensity = 90 * fl * pour; mGlow.material.opacity = 0.9 * fl * (0.3 + 0.7 * pour); mouthGlow.material.opacity = 0.85 * fl;
    crane.position.x = lerp(-6, 4, ease(t / dur)); men[0].set({ armR: -0.6 + 0.15 * Math.sin(t * 1.3), armL: -0.15 }); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2_WARM, exposure: 1.0, anchors };
}

// ======================= trade =======================
async function trade({ W, H, dur, opt }) {
  const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.0065); const R = rng(29);
  box(220, 0.2, 220, std('#ffffff', { map: gridTex('#121b28', 7), roughness: 0.85 }), 0, -0.1, 0).receiveShadow = true;
  const steelTex = rep(canvasTex(256, 256, (g, w, h) => { const R2 = rng(3); g.fillStyle = '#8e9aa8'; g.fillRect(0, 0, w, h); for (let i = 0; i < 1200; i++) { g.fillStyle = `rgba(${R2() < 0.5 ? '40,46,54' : '220,228,236'},0.07)`; g.fillRect(R2() * w, R2() * h, 1, 3 + R2() * 20); } }), 1, 3);
  const ped = (x, z, mt, col) => { const h = mt / 100; const g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g);
    const m = box(5, h, 5, std(col === 'tex' ? '#ffffff' : col, { map: col === 'tex' ? steelTex : null, roughness: 0.4, metalness: 0.45 }), 0, h / 2, 0, g); m.castShadow = m.receiveShadow = true; box(5.6, 0.3, 5.6, std('#223044'), 0, 0.15, 0, g); return { g, h, x, z }; };
  const CN = ped(-14, -6, 960.8, 'tex'), US = ped(16, 4, 81.9, 'tex'), EU = ped(6, -16, 126.0, 'tex');
  // nền kinh tế mới nổi: nhà máy nhỏ mọc (opt.mills = giây bắt đầu)
  const mills = []; for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2 + R() * 0.2, r = 30 + R() * 10, x = Math.cos(a) * r - 4, z = Math.sin(a) * r * 0.8 - 2; if (Math.hypot(x - 16, z - 4) < 9 || Math.hypot(x - 6, z + 16) < 9) continue;
    const g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g); box(2.6, 1.2, 1.6, std('#5d6874', { roughness: 0.6 }), 0, 0.6, 0, g); cyl(0.18, 0.22, 2.6, std('#4d535c'), 0.8, 1.3, -0.4, g, 8); const gl = glowSprite(C.orange, 0, 1.6); gl.position.set(0.8, 2.8, -0.4); g.add(gl); mills.push({ g, gl, d: R() }); }
  const arcs = []; const ends = [[22, 14], [30, -4], [10, 22], [-2, 24], [26, -22], [-30, 18], [-34, -14]];
  ends.forEach(([x, z], i) => { const a = new THREE.Vector3(-14, CN.h * 0.6, -6), b = new THREE.Vector3(x, 0.2, z), m = a.clone().add(b).multiplyScalar(0.5).setY(CN.h * 0.75 + 4);
    const cv = new THREE.QuadraticBezierCurve3(a, m, b); const g = new THREE.TubeGeometry(cv, 120, 0.09 + 0.05 * (i === 0), 8, false); const mesh = new THREE.Mesh(g, basic(C.orange)); scene.add(mesh); arcs.push({ g, n: g.index.count, cv }); });
  const pk = arcs.map(() => { const s = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.25, 0.3), std(C.orange, { emissive: '#5a2a10' })); scene.add(s); return s; });
  const wallM = new THREE.MeshStandardMaterial({ color: C.orange, emissive: '#5a2a10', transparent: true, opacity: 0, roughness: 0.3, side: THREE.DoubleSide, depthWrite: false });
  const wall = new THREE.Mesh(new THREE.CylinderGeometry(6.5, 6.5, 4.2, 48, 1, true), wallM); wall.position.set(16, 2.1, 4); scene.add(wall);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(6.5, 0.06, 6, 64), basic(C.orange, { transparent: true, opacity: 0 })); ring.rotation.x = Math.PI / 2; ring.position.set(16, 4.2, 4); scene.add(ring);
  const gate = new THREE.Group(); gate.position.set(6, 0, -9.5); scene.add(gate); const gm = std(C.teal, { roughness: 0.4, emissive: '#0f3a34', emissiveIntensity: 0.6, transparent: true, opacity: 0 });
  for (const x of [-3.2, 3.2]) box(0.5, 5, 0.5, gm, x, 2.5, 0, gate); box(6.9, 0.5, 0.5, gm, 0, 5, 0, gate);
  const prM = new THREE.LineDashedMaterial({ color: C.amber, dashSize: 0.5, gapSize: 0.35, transparent: true, opacity: 0 }); const pe = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(5, 7.45, 5)), prM); pe.computeLineDistances(); pe.position.set(-24, 3.725, 4); scene.add(pe);
  const peF = box(5, 7.45, 5, basic(C.amber, { transparent: true, opacity: 0, depthWrite: false }), -24, 3.725, 4);
  scene.add(new THREE.HemisphereLight('#7f93b8', '#1a2230', 1.8));
  const keyL = new THREE.SpotLight('#ffffff', 4200, 200, 0.75, 0.6, 1.4); keyL.position.set(-10, 55, 40); keyL.castShadow = true; keyL.shadow.mapSize.set(2048, 2048); scene.add(keyL);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.8); rim.position.set(30, 14, -40); scene.add(rim);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [27, 11, 27], l: [0, 5, -4], mm: 26 }, { u: 1, p: [24, 12.5, 28], l: [-1, 5, -4], mm: 25 }]);
  const at = (k) => (opt[k] === undefined ? 1e9 : opt[k]);   // khoá không khai = ẩn
  const anchors = { china: V3([-14, CN.h + 0.6, -6]), us: V3([16, US.h + 0.6, 4]), eu: V3([6, EU.h + 0.6, -16]), proj: V3([-24, 7.9, 4]), gate: V3([6, 5.6, -9.5]), wall: V3([16, 4.6, 10.4]), arc: () => arcs[0].cv.getPointAt(0.5), mills: V3([-30, 2, 20]) };
  const update = (t) => { rig.at(t);
    arcs.forEach((a, i) => { const u = ease((t - at('arcs') - i * 0.25) / 2.0); a.g.setDrawRange(0, Math.floor(u * a.n / 6) * 6); const v = ((t * 0.18 + i * 0.13) % 1); pk[i].visible = u >= 1; pk[i].position.copy(a.cv.getPointAt(v)); });
    const uw = ease((t - at('wall')) / 1.0); wallM.opacity = (0.16 + 0.05 * Math.sin(t * 1.4)) * uw; ring.material.opacity = uw; wall.scale.y = Math.max(0.01, uw); wall.position.y = 2.1 * uw;
    const ug = ease((t - at('gate')) / 1.0); gm.opacity = ug; const up = ease((t - at('proj')) / 1.0); prM.opacity = up; peF.material.opacity = 0.08 * up;
    mills.forEach((m, i) => { const u = ease((t - at('mills') - m.d * 2.4) / 0.6); m.g.scale.set(1, Math.max(0.001, u), 1); m.gl.material.opacity = 0.8 * u; }); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.1, anchors };
}

// ======================= port =======================
async function port({ W, H, dur, opt }) {
  const T = TOD[opt.tod || 'day'], mt = mats(); const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, T.fog, T.fd * 0.8); skyDome(scene, T.sky); const R = rng(33);
  const water = new THREE.Mesh(new THREE.PlaneGeometry(600, 400), std(opt.tod === 'day' ? '#2f4a5e' : '#14202d', { roughness: 0.15, metalness: 0.7 })); water.rotation.x = -Math.PI / 2; water.position.y = -0.8; scene.add(water);
  tbox(240, 2, 90, mt.conc, 0, -0.5, 45, scene, 0.08);   // bãi cảng bê tông (mép nước z = 0)
  for (let x = -118; x < 120; x += 4) box(0.4, 0.5, 0.4, std('#c8a83a', { roughness: 0.6 }), x, 0.75, 1.2);   // cọc buộc tàu
  for (let x = -120; x < 120; x += 10) box(0.25, 0.05, 40, basic('#d8d2b0'), x, 0.52, 40);   // vạch sơn bãi
  // tàu hàng rời neo bến
  const ship = new THREE.Group(); ship.position.set(-10, -0.8, -12); scene.add(ship);
  const hull = new THREE.Shape(); hull.moveTo(-60, -9); hull.lineTo(52, -9); hull.quadraticCurveTo(66, 0, 52, 9); hull.lineTo(-60, 9); hull.closePath();
  const hg = new THREE.ExtrudeGeometry(hull, { depth: 9, bevelEnabled: false }); hg.rotateX(-Math.PI / 2); const hm = new THREE.Mesh(hg, std('#ffffff', { map: rep(corrTex(51, '#3c4652', 0.6), 12, 1), roughness: 0.6, metalness: 0.4 })); hm.castShadow = true; ship.add(hm);
  box(112, 0.4, 17.6, std('#5a2e26'), -4, 0.4, 0, ship); box(118, 0.3, 18.2, std('#8a3b2e'), -4, 1.5, 0, ship);
  for (let i = 0; i < 6; i++) { tbox(13, 1.6, 13, mt.corrRust, -46 + i * 16, 9.8, 0, ship, 0.25); }
  tbox(12, 14, 16, std('#e3e6ea', { roughness: 0.6 }), -56, 16, 0, ship, 0.3); for (let k = 0; k < 4; k++) box(12.2, 0.6, 16.2, basic('#1c2430'), -56, 11 + k * 3, 0, ship);
  cyl(1.4, 1.6, 7, std('#2a2f36'), -60, 26, 0, ship, 14);
  // cẩu giàn bờ (STS) chạy dọc ray
  const cranes = []; const cm = std('#c8cdd3', { roughness: 0.5, metalness: 0.4 }), cmA = std(C.orange, { roughness: 0.5 });
  for (let k = 0; k < 3; k++) { const g = new THREE.Group(); g.position.set(-40 + k * 34, 0.5, 6); scene.add(g);
    for (const x of [-5, 5]) for (const z of [-6, 10]) box(0.9, 28, 0.9, cm, x, 14, z, g); box(11, 1.4, 1.4, cm, 0, 26, -6, g); box(11, 1.4, 1.4, cm, 0, 26, 10, g);
    box(2.2, 2.2, 66, k === 1 ? cmA : cm, 0, 30, -12, g); const tr = new THREE.Group(); g.add(tr); box(3, 2, 3, std('#3a3f46'), 0, 28.4, 0, tr); const sp = new THREE.Group(); tr.add(sp); cyl(0.05, 0.05, 1, std('#111'), 0, 0, 0, sp, 4); const hook = box(3, 0.6, 1.6, std('#e0b43a'), 0, 0, 0, sp);
    cranes.push({ g, tr, sp, hook, ph: k * 2.1 }); }
  // cuộn thép trên bãi (instanced) + phôi tấm + xe tải
  const coilG = new THREE.CylinderGeometry(1.0, 1.0, 1.2, 24); coilG.rotateX(Math.PI / 2); const coilM = std('#ffffff', { map: rep(canvasTex(256, 64, (g, w, h) => { g.fillStyle = '#7a848f'; g.fillRect(0, 0, w, h); for (let x = 0; x < w; x += 3) { g.fillStyle = `rgba(30,34,40,${0.1 + (x % 9) / 40})`; g.fillRect(x, 0, 1, h); } }), 3, 1), roughness: 0.35, metalness: 0.7 });
  const NC = 220, coils = new THREE.InstancedMesh(coilG, coilM, NC), Mx = new THREE.Matrix4(); let ci = 0;
  for (let b = 0; b < 4; b++) for (let r = 0; r < 5; r++) for (let c = 0; c < 11 && ci < NC; c++) { Mx.compose(V3([-60 + b * 22 + c * 2.0, 1.5, 24 + r * 1.6]), new THREE.Quaternion(), V3([1, 1, 1])); coils.setMatrixAt(ci++, Mx); }
  coils.count = ci; coils.castShadow = coils.receiveShadow = true; scene.add(coils);
  const slabG = new THREE.BoxGeometry(6, 0.35, 1.6), slabs = new THREE.InstancedMesh(slabG, std('#ffffff', { map: rep(corrTex(55, '#5a524c', 1), 1, 1), roughness: 0.8, metalness: 0.3 }), 60);
  for (let i = 0; i < 60; i++) { Mx.compose(V3([36 + (i % 3) * 7, 0.7 + Math.floor(i / 12) * 0.36, 22 + (Math.floor(i / 3) % 4) * 2.2]), new THREE.Quaternion(), V3([1, 1, 1])); slabs.setMatrixAt(i, Mx); } slabs.castShadow = true; scene.add(slabs);
  // cổng hải quan: nhà kiểm soát, mái che, làn xe, thanh chắn
  const gc = opt.gate === 'eu' ? C.teal : C.orange; const gate = new THREE.Group(); gate.position.set(20, 0.5, 58); scene.add(gate);
  tbox(30, 0.6, 9, std('#d6d9dd', { roughness: 0.5 }), 0, 7, 0, gate, 0.2); for (const x of [-14, -5, 5, 14]) tbox(0.7, 7, 0.7, mt.conc, x, 3.5, 0, gate, 0.4); box(30.2, 0.5, 0.2, basic(gc), 0, 6.6, 4.6, gate);
  for (const x of [-9.5, 0, 9.5]) { tbox(2.2, 2.8, 3, mt.corrBlue, x, 1.4, 0, gate, 0.4); box(1.6, 0.9, 0.05, std('#16202a', { emissive: '#9fc7e8', emissiveIntensity: 0.6 }), x, 2.0, 1.53, gate); }
  const bars = [-4.8, 4.8].map((x) => { const p = new THREE.Group(); p.position.set(x - 2.4, 1.0, 2.4); gate.add(p); box(4.4, 0.18, 0.18, basic(gc), 2.2, 0, 0, p); for (let k = 0; k < 4; k++) box(0.5, 0.2, 0.2, basic('#f0f0f0'), 0.6 + k * 1.1, 0, 0.01, p); return p; });
  tbox(60, 2.4, 1.0, mt.conc, -45, 1.2, 58, scene, 0.3); tbox(60, 2.4, 1.0, mt.conc, 85, 1.2, 58, scene, 0.3);   // tường rào cảng
  for (let x = -70; x < 70; x += 3) { box(0.06, 3, 0.06, std('#7a838c'), x, 3.9, 58); } box(140, 0.06, 0.06, std('#7a838c'), 0, 5.3, 58);
  const trucks = []; for (let i = 0; i < 4; i++) { const g = new THREE.Group(); scene.add(g); tbox(2.4, 2.6, 2.6, mt.corrBlue, 0, 1.8, 3.8, g, 0.4); box(2.4, 0.5, 9, std('#2b2f36'), 0, 0.9, -1.2, g); const c = cyl(1.0, 1.0, 1.2, coilM, 0, 2.2, -1, g, 18); c.rotation.x = Math.PI / 2; trucks.push({ g, d: i * 14 }); }
  // đèn cao cột (ban đêm/chạng vạng)
  const lamps = []; for (const [x, z] of [[-70, 30], [-20, 34], [30, 34], [80, 30], [10, 70]]) { cyl(0.25, 0.35, 26, std('#6a7078'), x, 13, z, scene, 8); const gl = glowSprite('#ffd7a0', opt.tod === 'day' ? 0 : 0.9, 4); gl.position.set(x, 26.5, z); scene.add(gl); if (opt.tod !== 'day') { const pl = new THREE.PointLight('#ffd0a0', 120, 60, 1.6); pl.position.set(x, 25, z); scene.add(pl); } lamps.push(gl); }
  // đồi và thành phố xa (khối) sau cảng
  for (let i = 0; i < 70; i++) { const h = 3 + R() * 16; tbox(4 + R() * 8, h, 4 + R() * 8, std(opt.tod === 'day' ? '#8e98a4' : '#2a3240', { roughness: 0.9 }), -160 + R() * 320, h / 2, 110 + R() * 60, scene, 0.3); }
  lightTod(scene, T, 140);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [60, 22, 110], l: [10, 4, 40], mm: 30 }, { u: 1, p: [40, 18, 104], l: [6, 4, 40], mm: 32 }]);
  const dst = dust(scene, [0, 8, 40], [140, 16, 80], 200, 13, opt.tod === 'day' ? '#f0eee8' : '#ffd9a8');
  const lift = opt.lift === undefined ? 1e9 : opt.lift;
  const anchors = { crane: () => cranes[1].g.localToWorld(V3([0, 31.5, -12])), ship: V3([-20, 12, -12]), coils: V3([-38, 3, 27]), gate: V3([20, 8.2, 58]), slabs: V3([43, 3, 25]), truck: () => trucks[0].g.position.clone().add(V3([0, 3.5, 0])) };
  const update = (t) => { rig.at(t); dst.update(t);
    cranes.forEach((c) => { const u = (Math.sin(t * 0.35 + c.ph) + 1) / 2; c.tr.position.z = lerp(-36, 6, u); c.sp.position.y = 28.4 - lerp(4, 18, (Math.sin(t * 0.7 + c.ph) + 1) / 2); c.sp.children[0].scale.y = 28.4 - c.sp.position.y; c.sp.children[0].position.y = (28.4 - c.sp.position.y) / 2; });
    const ul = ease((t - lift) / 1.2); bars.forEach((b) => { b.rotation.z = ul * 1.3; });
    trucks.forEach((k, i) => { const s = ((t * 3.2 + k.d) % 56) - 8; const zz = i % 2 ? 62 + s : 60; const xx = i % 2 ? 24.8 : 15.2 - 0; k.g.position.set(i % 2 ? 24.8 : 15.2, 0.5, i % 2 ? 20 + ((t * 2.6 + k.d) % 60) : 80 - ((t * 2.6 + k.d) % 60)); k.g.rotation.y = i % 2 ? 0 : Math.PI; }); };
  return { scene, cam: rig.cam, update, grade: T.grade, exposure: T.exp, anchors };
}

// ======================= mill (hiện đại, ban ngày) =======================
async function mill({ W, H, dur, opt }) {
  const T = TOD[opt.tod || 'day'], mt = mats(); const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, T.fog, T.fd * (opt.inside ? 3 : 1)); skyDome(scene, T.sky); const R = rng(41);
  tbox(320, 1, 240, mt.conc, 0, -0.5, 0, scene, 0.06);
  // xưởng lò hồ quang: khung cao, tôn sóng, mở mặt nam (z+) để thấy bên trong
  const shop = new THREE.Group(); scene.add(shop); const SW = 60, SD = 30, SH = 30;
  tbox(SW, SH, 0.6, mt.corrBlue, 0, SH / 2, -SD / 2, shop, 0.12); tbox(0.6, SH, SD, mt.corrBlue, -SW / 2, SH / 2, 0, shop, 0.12); tbox(0.6, SH, SD, mt.corrBlue, SW / 2, SH / 2, 0, shop, 0.12);
  tbox(SW, 0.6, SD + 2, std('#9aa3ad', { roughness: 0.6, metalness: 0.3 }), 0, SH + 2.5, 0, shop, 0.1); for (const s of [-1, 1]) { const r = tbox(SW, 0.5, SD / 2 + 3, std('#8a939d', { roughness: 0.6, metalness: 0.3 }), 0, SH + 1.4, s * SD / 4, shop, 0.1); r.rotation.x = s * -0.18; }
  tbox(SW, 8, 0.6, mt.corrBlue, 0, SH - 4, SD / 2, shop, 0.12);   // diềm trên mặt mở
  for (let x = -SW / 2; x <= SW / 2; x += 10) { box(0.9, SH, 0.9, std('#4a5560', { metalness: 0.4 }), x, SH / 2, SD / 2); box(0.9, SH, 0.9, std('#4a5560', { metalness: 0.4 }), x, SH / 2, -SD / 2 + 0.6); }
  for (let x = -SW / 2 + 4; x < SW / 2; x += 6) box(3, 1.2, 0.1, basic('#cfe2f0', { transparent: true, opacity: 0.5 }), x, SH - 1.5, -SD / 2 + 0.35);   // dải kính mái
  // sàn thao tác + lò hồ quang (vỏ, nắp, 3 điện cực), thùng rót, cầu trục
  tbox(30, 6, 18, mt.conc, -6, 3, -4, shop, 0.2); for (let x = -20; x < 9; x += 1.5) box(0.08, 1.1, 0.08, std('#e0b43a'), x, 6.55, 5);
  box(30, 0.08, 0.08, std('#e0b43a'), -6, 7.1, 5);
  const eaf = new THREE.Group(); eaf.position.set(-8, 6, -4); shop.add(eaf);
  const shellE = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 3.8, 3.8, 36), std('#ffffff', { map: rep(corrTex(61, '#4a4f57', 0.6), 6, 1), roughness: 0.5, metalness: 0.5 })); shellE.position.y = 1.9; shellE.castShadow = true; eaf.add(shellE);
  for (let k = 0; k < 18; k++) { const p = cyl(0.12, 0.12, 3.6, std('#6a7480', { metalness: 0.6 }), Math.cos(k / 18 * 6.28) * 4.3, 1.9, Math.sin(k / 18 * 6.28) * 4.3, eaf, 6); }
  const roof = new THREE.Mesh(new THREE.SphereGeometry(4.3, 32, 10, 0, 6.3, 0, 0.75), std('#3a3f46', { roughness: 0.6, metalness: 0.4 })); roof.position.y = 3.2; eaf.add(roof);
  const elec = [0, 1, 2].map((k) => cyl(0.38, 0.38, 9, std('#2a2a2a', { roughness: 0.4, metalness: 0.2 }), Math.cos(k * 2.09) * 1.2, 9.5, Math.sin(k * 2.09) * 1.2, eaf, 12));
  box(1.2, 1.0, 7, std('#4a5560', { metalness: 0.4 }), 0, 13.5, 2.5, eaf); box(1.2, 10, 1.2, std('#4a5560', { metalness: 0.4 }), 0, 9, 6, eaf);
  const arcGl = glowSprite('#fff2c8', 1, 7); arcGl.position.set(0, 4.6, 0); eaf.add(arcGl); const arcL = new THREE.PointLight('#ffd2a0', 300, 50, 1.6); arcL.position.set(0, 7, 0); eaf.add(arcL);
  const arcRim = new THREE.PointLight('#ff8a3a', 90, 30, 1.6); arcRim.position.set(0, 3, 5); eaf.add(arcRim);
  const spk = sparks(scene, R, 500, '#ffd27a', 0.12);
  const crane = new THREE.Group(); scene.add(crane); box(2.2, 2.2, SD - 2, std(C.orange, { roughness: 0.5 }), 0, SH - 6, 0, crane); box(3, 2, 3, std('#3a3f46'), 0, SH - 7.6, 0, crane);
  const bucket = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 1.8, 3, 20, 1, true), std('#4a4f57', { metalness: 0.5, roughness: 0.6, side: THREE.DoubleSide })); crane.add(bucket);
  // bãi phế: đống thép phế (instanced mảnh), cẩu nam châm
  const scrapG = new THREE.BoxGeometry(1, 0.3, 0.6), scrapIM = new THREE.InstancedMesh(scrapG, std('#ffffff', { map: rep(corrTex(66, '#6a5a4c', 1.4), 1, 1), roughness: 0.9, metalness: 0.3 }), 1400), Mx = new THREE.Matrix4();
  for (let i = 0; i < 1400; i++) { const h = Math.random() < 0 ? 0 : 0; const a = R() * 6.28, rr = Math.sqrt(R()) * 11, x = 52 + Math.cos(a) * rr * 1.4, z = 10 + Math.sin(a) * rr, y = Math.max(0, (1 - rr / 11) * 6 * (0.7 + 0.3 * R())); const s = 0.6 + R() * 2.2;
    Mx.compose(V3([x, y, z]), new THREE.Quaternion().setFromEuler(new THREE.Euler(R() * 3, R() * 3, R() * 3)), V3([s, 0.6 + R(), 0.6 + R()])); scrapIM.setMatrixAt(i, Mx); }
  scrapIM.castShadow = scrapIM.receiveShadow = true; scene.add(scrapIM);
  const mag = new THREE.Group(); mag.position.set(52, 0, 10); scene.add(mag); for (const z of [-14, 14]) for (const x of [-16, 16]) box(0.8, 16, 0.8, std('#6a7480'), x, 8, z, mag); box(34, 1.2, 1.2, std('#6a7480'), 0, 16, -14, mag); box(34, 1.2, 1.2, std('#6a7480'), 0, 16, 14, mag);
  const magB = new THREE.Group(); mag.add(magB); box(1.6, 1.6, 30, std(C.orange, { roughness: 0.5 }), 0, 17, 0, magB); const disc = cyl(1.6, 1.6, 0.6, std('#2a2e35', { metalness: 0.6 }), 0, 8, 0, magB, 20); const rope = cyl(0.05, 0.05, 8, std('#111'), 0, 12.5, 0, magB, 4);
  // dây chuyền đúc liên tục/cán: bàn con lăn ngoài trời, phôi tấm chạy (opt.hot), chồng phôi nguội
  const line = new THREE.Group(); line.position.set(-10, 0, 36); scene.add(line); for (let x = -40; x <= 40; x += 1.2) cyl(0.25, 0.25, 3.2, std('#5a636e', { metalness: 0.6 }), x, 1.2, 0, line, 10).rotation.x = Math.PI / 2;
  box(82, 0.8, 4, std('#3a4048'), 0, 0.5, 0, line); tbox(30, 9, 10, mt.corrBlue, 46, 4.5, 0, line, 0.15);
  const slabM = std('#ff7a2a', { emissive: '#ff5a10', emissiveIntensity: 1.6, roughness: 0.6 }); const hotSlab = box(8, 0.5, 2.2, slabM, 0, 1.75, 0, line); const hsL = new THREE.PointLight('#ff7a2a', 80, 14, 1.6); line.add(hsL);
  const coldSlabs = new THREE.InstancedMesh(new THREE.BoxGeometry(8, 0.45, 2.2), std('#ffffff', { map: rep(corrTex(57, '#5c5550', 1.2), 1, 1), roughness: 0.85, metalness: 0.3 }), 48);
  for (let i = 0; i < 48; i++) { Mx.compose(V3([-30 + (i % 4) * 9, 0.25 + Math.floor(i / 16) * 0.46, 46 + (Math.floor(i / 4) % 4) * 2.6]), new THREE.Quaternion(), V3([1, 1, 1])); coldSlabs.setMatrixAt(i, Mx); } coldSlabs.castShadow = true; scene.add(coldSlabs);
  // ống khói + lọc bụi (baghouse), bồn, đường ống
  const stacks = []; for (const [x, z, h] of [[-44, -26, 46], [-38, -26, 46]]) { const s = cyl(1.6, 2.0, h, std('#c8ccd0', { roughness: 0.6 }), x, h / 2, z, scene, 18); for (const y of [h - 4, h - 7]) box(3.4, 0.6, 3.4, basic('#c43a2a'), x, y, z); stacks.push([x, h, z]); }
  tbox(22, 14, 12, mt.corr, -50, 7, -2, scene, 0.15); for (let i = 0; i < 6; i++) cyl(1, 1, 8, std('#9aa3ad', { metalness: 0.4 }), -58 + i * 3.2, 18, -2, scene, 12);
  const duct = cyl(1.4, 1.4, 34, std('#9aa3ad', { metalness: 0.4 }), -24, 26, -10, scene, 14); duct.rotation.z = Math.PI / 2;
  const plumes = stacks.map(([x, h, z], i) => plume(scene, x, h + 0.6, z, { seed: 70 + i, op: opt.tod === 'day' ? 0.32 : 0.24, size: 3.2, color: '#e8ecf0' }));
  for (let i = 0; i < 6; i++) { const tk = cyl(3, 3, 9, std('#d8dde2', { roughness: 0.5, metalness: 0.3 }), 70 + (i % 3) * 7.5, 4.5, -30 + Math.floor(i / 3) * 8, scene, 24); }
  // bãi xe, hàng rào, cây ven nhà máy
  const TP = []; for (let i = 0; i < 160; i++) { const x = -150 + R() * 300, z = 70 + R() * 60; TP.push([x, 0, z]); } for (let i = 0; i < 90; i++) TP.push([-150 + R() * 300, 0, -80 - R() * 50]); trees(scene, TP, R, opt.tod === 'day' ? '#3e5a3a' : '#22301f');
  lightTod(scene, T, 120);
  if (opt.inside) { const il = new THREE.PointLight('#dfe8ff', 120, 80, 1.4); il.position.set(0, SH - 4, 0); scene.add(il); }
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [40, 22, 90], l: [0, 8, 10], mm: 30 }, { u: 1, p: [20, 20, 86], l: [-4, 8, 10], mm: 32 }]);
  const dst = dust(scene, [-8, 10, -4], [30, 14, 16], 260, 19, '#ffe3b8');
  const hot = opt.hot === undefined ? true : !!opt.hot, arcK = opt.arc === undefined ? 1 : opt.arc;
  const anchors = { meltshop: V3([0, SH + 3, 0]), eaf: () => eaf.localToWorld(V3([0, 5, 0])), scrap: V3([52, 7, 10]), slabs: V3([-16, 1.5, 50]), line: () => hotSlab.getWorldPosition(V3([0, 0, 0])).add(V3([0, 1, 0])), stack: V3([-41, 48, -26]), mag: () => disc.getWorldPosition(V3([0, 0, 0])) };
  const update = (t, f) => { rig.at(t); dst.update(t); plumes.forEach((p) => p.update(t));
    const fl = arcK * (0.75 + 0.25 * Math.abs(Math.sin(f * 1.7) * Math.sin(f * 0.53 + 1))); arcL.intensity = 300 * fl; arcRim.intensity = 90 * fl; arcGl.material.opacity = Math.min(1, fl); arcGl.scale.setScalar(7 * (0.8 + 0.3 * fl));
    elec.forEach((e, k) => { e.position.y = 9.5 + 0.15 * Math.sin(t * 2 + k); }); spk(t, eaf.localToWorld(V3([0, 4.8, 2.5])), 0.6 * arcK);
    crane.position.set(lerp(-26, 10, (Math.sin(t * 0.2) + 1) / 2), 0, 0); bucket.position.set(0, SH - 12, 0);
    const um = (Math.sin(t * 0.45) + 1) / 2; magB.position.x = lerp(-10, 10, um); disc.position.y = 8 + 4 * Math.abs(Math.sin(t * 0.9)); rope.scale.y = (17 - disc.position.y) / 8; rope.position.y = (17 + disc.position.y) / 2;
    hotSlab.visible = hot; hsL.intensity = hot ? 80 : 0; const sx = ((t * 3.0) % 70) - 35; hotSlab.position.x = sx; hsL.position.set(sx, 3, 1); };
  return { scene, cam: rig.cam, update, grade: T.grade, exposure: T.exp * (opt.inside ? 0.9 : 1), anchors };
}

// ======================= north =======================
async function north({ W, H, dur, opt }) {
  const T = TOD[opt.tod || 'blue'], mt = mats(); const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, T.fog, 0.008); skyDome(scene, T.sky); const R = rng(23);
  const tg = new THREE.PlaneGeometry(420, 320, 170, 130); tg.rotateX(-Math.PI / 2); const P = tg.attributes.position; const hY = (x, z) => { const d = Math.hypot(x, z + 10); return d < 40 ? 0 : Math.pow((d - 40) / 160, 1.6) * 40 * (0.6 + 0.4 * Math.sin(x * 0.03 + 1)); };
  for (let i = 0; i < P.count; i++) P.setY(i, hY(P.getX(i), P.getZ(i)) + 0.15 * Math.sin(P.getX(i) * 1.3) * Math.sin(P.getZ(i) * 1.1));
  tg.computeVertexNormals(); const snow = new THREE.Mesh(tg, std('#c9d3e0', { roughness: 0.92 })); snow.receiveShadow = true; scene.add(snow);
  // đường nội bộ (bê tông xám trên tuyết) và bãi
  tbox(140, 0.1, 8, mt.conc, 0, 0.05, 30, scene, 0.1); tbox(8, 0.1, 80, mt.conc, -18, 0.06, 0, scene, 0.1);
  const cone = new THREE.ConeGeometry(1.1, 4.2, 7); cone.translate(0, 2.1, 0); const NT = 1000, pines = new THREE.InstancedMesh(cone, std('#1c2b26', { roughness: 1 }), NT); const Mx = new THREE.Matrix4();
  for (let i = 0; i < NT; i++) { let x, z; do { x = -200 + R() * 400; z = -160 + R() * 220; } while (Math.hypot(x, z + 10) < 50); const s = 0.7 + R() * 0.8; Mx.compose(V3([x, hY(x, z) - 0.2, z]), new THREE.Quaternion(), V3([s, s * (0.9 + R() * 0.4), s])); pines.setMatrixAt(i, Mx); }
  pines.castShadow = true; scene.add(pines);
  const plant = new THREE.Group(); scene.add(plant); const dark = std('#2d343d', { roughness: 0.8 });
  const site = !!opt.site; const glowK = site ? 0 : 1;
  // tháp khử trực tiếp (hoàn thiện hoặc khung đang dựng)
  if (!site) { cyl(2.6, 2.9, 34, std('#ffffff', { map: rep(corrTex(81, '#7c8794', 0.1), 4, 4), roughness: 0.45, metalness: 0.45 }), -6, 17, -14, plant, 32); }
  else { for (let k = 0; k < 8; k++) { const y = k * 4 + 2; box(8, 0.3, 8, std('#6a7480'), -6, y, -14, plant); } }
  box(8, 0.4, 8, dark, -6, 22, -14, plant); box(8, 0.4, 8, dark, -6, 30, -14, plant);
  for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { box(0.35, 34, 0.35, dark, -6 + a * 3.8, 17, -14 + b * 3.8, plant); for (let y = 4; y < 34; y += 6) { const d = box(0.15, 6.4, 0.15, dark, -6 + a * 3.8, y + 3, -14 + b * 3.8, plant); d.rotation.x = 0.7 * (b > 0 ? 1 : -1); } }
  if (!site) { const pipeH = cyl(0.5, 0.5, 24, std('#9aa7b5', { metalness: 0.5, roughness: 0.35 }), 6, 18, -14, plant, 12); pipeH.rotation.z = Math.PI / 2; for (const y of [6, 14, 26]) { const r = new THREE.Mesh(new THREE.TorusGeometry(2.75, 0.12, 6, 40), basic(C.teal)); r.rotation.x = Math.PI / 2; r.position.set(-6, y, -14); plant.add(r); } }
  // nhà điện phân: dãy nhà dài
  for (let k = 0; k < 4; k++) { const z = -2 + k * 6; if (site && k > 1) { for (let x = 8; x <= 36; x += 4) { box(0.3, 5, 0.3, std('#6a7480'), x, 2.5, z - 2); box(0.3, 5, 0.3, std('#6a7480'), x, 2.5, z + 2); } box(30, 0.3, 0.3, std('#6a7480'), 22, 5, z - 2); continue; }
    tbox(30, 5, 4, mt.corrBlue, 22, 2.5, z, plant, 0.2); box(30, 0.25, 0.08, basic(C.teal), 22, 3.6, z + 2.05, plant); for (let i = 0; i < 14; i++) box(0.9, 0.5, 0.05, std('#16202f', { emissive: '#7fe0d2', emissiveIntensity: site ? 0.05 : 0.55 }), 8.5 + i * 2.1, 2.2, z + 2.04, plant); }
  // bồn hydro (cầu), trạm biến áp
  for (let i = 0; i < 3; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(3, 24, 16), std('#e3e8ee', { roughness: 0.4, metalness: 0.3 })); s.position.set(44 + i * 7.5, 4.5, -14); s.castShadow = true; plant.add(s); for (const a of [0, 1, 2, 3]) box(0.25, 3, 0.25, dark, 44 + i * 7.5 + Math.cos(a * 1.57) * 2.2, 1.5, -14 + Math.sin(a * 1.57) * 2.2, plant); }
  for (let i = 0; i < 6; i++) { box(2, 2.4, 1.6, std('#7a838c', { metalness: 0.4 }), 44 + i * 3, 1.2, 8, plant); box(0.2, 6, 0.2, dark, 44 + i * 3, 4, 10, plant); }
  // xưởng lò hồ quang
  tbox(26, 14, 16, mt.corrBlue, -30, 7, 6, plant, 0.15); for (let i = 0; i < 12; i++) box(1.1, 0.45, 0.08, std('#1d1a17', { emissive: '#ff9a46', emissiveIntensity: 1.2 * glowK }), -41 + i * 2, 12.6, 14.05, plant);
  const eafGlow = glowSprite('#ff9040', 0.75 * glowK, 9); eafGlow.position.set(-30, 12, 15.5); scene.add(eafGlow); const eafL = new THREE.PointLight('#ff8a3a', 80 * glowK, 30, 1.6); eafL.position.set(-30, 8, 18); scene.add(eafL);
  for (let i = 0; i < 90; i++) { const b = box(0.6 + R() * 1.6, 0.3 + R() * 0.7, 0.4 + R(), std(R() < 0.5 ? '#5a4234' : '#6c6a66', { roughness: 0.95 }), -40 + R() * 12, 0.3 + R() * 1.5, 18 + R() * 8); b.rotation.set(R(), R() * 3, R()); }
  // công trường: cẩu tháp, đống vật liệu, lán, đèn công trường
  const tcr = []; if (site) for (const [x, z, h] of [[-14, -4, 44], [14, -16, 40], [30, 16, 38]]) { const g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g); for (let y = 0; y < h; y += 2) { box(1.6, 0.12, 0.12, std(C.amber), 0, y, 0.8, g); box(1.6, 0.12, 0.12, std(C.amber), 0, y, -0.8, g); } for (const a of [-0.8, 0.8]) for (const b of [-0.8, 0.8]) box(0.14, h, 0.14, std(C.amber), a, h / 2, b, g);
    const jib = new THREE.Group(); jib.position.y = h; g.add(jib); box(34, 1.0, 1.0, std(C.amber), 8, 0, 0, jib); box(6, 2, 2, std('#6a7480'), -10, -0.8, 0, jib); const tr = cyl(0.04, 0.04, 14, std('#111'), 18, -7, 0, jib, 4); box(1.2, 0.8, 0.8, std('#e0b43a'), 18, -14, 0, jib); tcr.push({ jib, ph: R() * 6 }); }
  if (site) { for (let i = 0; i < 40; i++) box(6, 0.3, 0.3, std('#7a6a5a'), -50 + (i % 8) * 0.4, 0.2 + Math.floor(i / 8) * 0.35, 40 + (i % 8) * 0.4); for (let i = 0; i < 6; i++) tbox(6, 2.6, 2.4, mt.corr, 40 + i * 6.4, 1.3, 34, scene, 0.4);
    for (const [x, z] of [[-30, 30], [10, 30], [40, 0]]) { cyl(0.15, 0.15, 10, dark, x, 5, z, scene, 6); const gl = glowSprite('#fff4d8', 0.9, 3); gl.position.set(x, 10.4, z); scene.add(gl); const pl = new THREE.PointLight('#fff0d0', 60, 40, 1.6); pl.position.set(x, 10, z); scene.add(pl); } }
  const turbines = [];
  for (let k = 0; k < 9; k++) { const x = -120 + k * 30, z = -130 + (k % 2) * 14, y = hY(x, z);
    const g = new THREE.Group(); g.position.set(x, y, z); scene.add(g); cyl(0.5, 0.9, 30, std('#e3e8ee', { roughness: 0.5 }), 0, 15, 0, g, 12); box(1.4, 1.2, 3, std('#e3e8ee'), 0, 30, 0.6, g);
    const rot = new THREE.Group(); rot.position.set(0, 30, 2.2); g.add(rot); for (let b = 0; b < 3; b++) { const arm = new THREE.Group(); box(0.5, 14, 0.15, std('#eef1f4'), 0, 7, 0, arm); arm.rotation.z = b * 2.094; rot.add(arm); }
    const red = glowSprite('#ff3b2a', 0.9, 2.2); red.position.set(0, 31, 0.6); g.add(red); turbines.push({ rot, red, ph: R() * 6 }); }
  // đường dây điện cao thế vào khu điện phân
  for (let k = 0; k < 6; k++) { const x = 60 + k * 22, z = -40 - k * 14; const g = new THREE.Group(); g.position.set(x, hY(x, z), z); scene.add(g); for (const a of [-1, 1]) { const l = box(0.25, 18, 0.25, dark, a * 1.5, 9, 0, g); l.rotation.z = -a * 0.08; } box(7, 0.3, 0.3, dark, 0, 16, 0, g); }
  lightTod(scene, T, 150);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [26, 12, 70], l: [-6, 12, -6], mm: 30 }, { u: 1, p: [10, 14, 58], l: [-8, 13, -8], mm: 32 }]);
  const dst = dust(scene, [-6, 10, 10], [80, 24, 50], 600, 21, '#e6f0ff');
  const anchors = { shaft: V3([-6, 36, -14]), electro: V3([22, 6, 10]), eaf: V3([-30, 15, 6]), turbines: V3([-30, 45, -130]), site: V3([-14, 46, -4]), tanks: V3([51, 8, -14]) };
  const update = (t, f) => { rig.at(t); dst.update(t * 3); turbines.forEach((tb) => { tb.rot.rotation.z = tb.ph + t * 0.9; tb.red.material.opacity = (Math.floor(t * 0.8 + tb.ph) % 2) ? 0.9 : 0.15; });
    const k = 1 + 0.08 * Math.sin(f * 0.5); eafL.intensity = 80 * k * glowK; eafGlow.material.opacity = 0.7 * k * glowK; tcr.forEach((c) => { c.jib.rotation.y = c.ph + 0.25 * Math.sin(t * 0.15 + c.ph); }); };
  return { scene, cam: rig.cam, update, grade: T.grade, exposure: T.exp, anchors };
}

export const HEROES = { valley, ingots, chain, furnace, trade, port, mill, north };

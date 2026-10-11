// KÊNH 2 · ngách G · tập thử K2G-01 "Steel" — CẢNH 3D MẪU (G1, nháp 960×540). Nhận diện theo channel-k2/NHAN-DIEN.md:
//   "mô hình kỹ thuật sống": sa bàn khối giản lược, ánh công nghiệp lạnh, MỘT màu nhấn cam an toàn #F08A4B cho thứ đang được giải thích,
//   xanh lục lam #3CC2B0 cho dòng "bình thường"/sạch, hổ phách #F2C14E cho dự báo; nền mực #0F1722; chữ Inter. Không logo, không mặt người, không biểu tượng dân tộc.
//   Dùng chung lõi LL (kit.js: hình học, máy quay, bụi, canvasTex; page.js: hậu kỳ) — KHÔNG sửa kit.js; bảng màu hậu kỳ riêng (GRADE_K2) truyền dạng object.
//   valley   thung lũng sông chạng vạng: nhà máy thép ven sông (lò cao, lò gió nóng, nhà xưởng mái răng cưa, ống khói), hai tuyến ray + sông, cầu giàn, thị trấn trên đồi. (móc / kết)
//   ingots   sa bàn số: thỏi thép = 10 Mt; 1950 (thế giới 189, Mỹ 87,8 cam) cạnh 2025 (thế giới 1 849, Mỹ 81,9 cam). (móc, huyền thoại vs hồ sơ #1)
//   chain    bản đồ tuyến (giản lược): quặng Minnesota → tàu qua Hồ Lớn → ray → Pittsburgh; than cốc Connellsville; theo lời Carnegie 1920. (tầng 1)
//   furnace  trong xưởng Bessemer: lò chuyển nghiêng rót thép lỏng vào thùng, tia lửa, cầu trục, bóng người có ánh viền. (tầng 1)
//   trade    sa bàn thương mại: bệ sản lượng, cung xuất khẩu TQ 131,2 Mt, tường thuế 50 % (Mỹ), cổng hạn ngạch EU, dư thừa 745 Mt PROJECTION. (tầng 2)
//   north    tầng 3: phương bắc giờ xanh — tháp khử hydro, nhà điện phân, lò hồ quang điện, tua-bin gió, rừng thông tuyết; nhãn CO₂ theo tuyến. (tầng 3)
import { THREE, useScene, figure, dust, camRig, box, cyl, lam, std, glowSprite, rng, ease, lerp, canvasTex } from './kit.js';

const C = { ink: '#0F1722', text: '#EEF1F4', steel: '#9AA7B5', orange: '#F08A4B', teal: '#3CC2B0', amber: '#F2C14E' };
// hậu kỳ riêng kênh 2: không vân vải (gCanvas 0), tối viền nhẹ, bóng ngả xanh mực, sáng trung tính
const GRADE_K2 = { gCanvas: 0.0, gVig: 0.24, gLift: 0.025, gSat: 0.92, gShadowTint: [0.22, 0.34, 0.62], gHiTint: [1.02, 1.0, 0.97] };
const GRADE_K2_WARM = { gCanvas: 0.0, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.26, 0.33, 0.6], gHiTint: [1.05, 0.99, 0.92] };
const basic = (color, o = {}) => new THREE.MeshBasicMaterial({ color, ...o });
const add = (scene, o) => { scene.add(o); return o; };
function skyDome(scene, stops, r = 260) {
  const s = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, map: canvasTex(8, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([u, c]) => gr.addColorStop(u, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); }) }));
  scene.add(s); return s;
}
// nhãn nổi trên vật thể (sprite chữ Inter, nền mực trong mờ, gạch màu nhấn bên trái). lines: [{t, size, color, weight}]
function label(lines, { accent = C.orange, w = 1024, scale = 1, bg = 'rgba(15,23,34,0.78)', dashed = false } = {}) {
  const pad = 34, lh = lines.map((l) => (l.size || 44) * 1.28), h = Math.ceil(lh.reduce((a, b) => a + b, 0) + pad * 1.4);
  const tex = canvasTex(w, h, (g) => {
    g.fillStyle = bg; g.fillRect(0, 0, w, h);
    g.fillStyle = accent; if (dashed) { for (let y = 0; y < h; y += 22) g.fillRect(0, y, 10, 12); } else g.fillRect(0, 0, 10, h);
    let y = pad * 0.7; lines.forEach((l, i) => { g.font = `${l.weight || 600} ${l.size || 44}px "${l.display === false ? 'Inter' : 'Inter Display'}", Inter, sans-serif`; g.fillStyle = l.color || C.text; g.textBaseline = 'top'; g.fillText(l.t, pad, y); y += lh[i]; });
  });
  const m = new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, fog: false }); const sp = new THREE.Sprite(m);
  sp.scale.set(scale * w / 256, scale * h / 256, 1); sp.renderOrder = 10; return sp;
}
const softTex = () => canvasTex(128, 128, (g, w, h) => { const gr = g.createRadialGradient(64, 64, 2, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.4, 'rgba(255,255,255,0.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
// khói/hơi nước bốc lên từ ống khói: chuỗi sprite lặp theo thời gian (chuyển động liên tục)
function plume(scene, x, y, z, { n = 14, color = '#c9ced8', op = 0.32, rise = 0.9, drift = 0.35, size = 2.2, seed = 3 } = {}) {
  const R = rng(seed), tex = softTex(), S = [];
  for (let i = 0; i < n; i++) { const m = new THREE.SpriteMaterial({ map: tex, color, transparent: true, opacity: 0, depthWrite: false }); const s = new THREE.Sprite(m); scene.add(s); S.push({ s, ph: i / n, j: R() }); }
  const update = (t) => S.forEach(({ s, ph, j }) => { const u = (ph + t * 0.06 * rise) % 1; s.position.set(x + u * 9 * drift + Math.sin(t * 0.4 + j * 6) * 0.3, y + u * 9 * rise, z - u * 2); s.scale.setScalar(size * (0.5 + u * 2.2)); s.material.opacity = op * Math.sin(Math.PI * Math.min(1, u * 1.15)) * (0.7 + 0.3 * j); });
  update(0); return { update };
}
const fogOf = (scene, color, d) => { useScene(scene); scene.fog = new THREE.FogExp2(color, d); scene.background = new THREE.Color(color); };

// ===== valley: thung lũng sông, nhà máy thép chạng vạng =====
function blastFurnace(parent, x, z, s = 1, R) {
  const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g); const shell = std('#4d535c', { roughness: 0.6, metalness: 0.35 }), dark = std('#2a2e35', { roughness: 0.8 });
  const prof = [[0, 0], [2.0, 0], [2.0, 2.2], [2.5, 3.2], [2.5, 7.0], [1.6, 11.5], [1.2, 12.5], [1.2, 13.2], [0, 13.2]].map(([a, b]) => new THREE.Vector2(a * s, b * s));
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 28), shell); body.castShadow = body.receiveShadow = true; g.add(body);
  for (let k = 0; k < 6; k++) { const r = new THREE.Mesh(new THREE.TorusGeometry(2.52 * s, 0.07 * s, 6, 40), dark); r.rotation.x = Math.PI / 2; r.position.y = (3.6 + k * 0.62) * s; g.add(r); }   // đai thân lò
  box(5.6 * s, 0.25 * s, 5.6 * s, dark, 0, 7.4 * s, 0, g); for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) box(0.25 * s, 7.4 * s, 0.25 * s, dark, a * 2.6 * s, 3.7 * s, b * 2.6 * s, g);   // sàn thao tác + cột
  for (let k = 0; k < 4; k++) { const u = cyl(0.22 * s, 0.22 * s, 4.6 * s, dark, (k - 1.5) * 0.7 * s, 15.4 * s, 0, g, 10); u.rotation.z = (k - 1.5) * 0.12; }   // ống khí lên
  const dc = cyl(0.45 * s, 0.45 * s, 9 * s, dark, 3.8 * s, 12 * s, 0, g, 12); dc.rotation.z = -0.55;   // ống dẫn khí xuống
  for (let k = 0; k < 3; k++) { const st = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [1.25, 0], [1.25, 10.5], [0.9, 11.6], [0, 12.0]].map(([a, b]) => new THREE.Vector2(a * s, b * s)), 20), std('#5b6168', { roughness: 0.55, metalness: 0.3 })); st.position.set((-4.2 - k * 2.8) * s, 0, -3 * s); st.castShadow = true; g.add(st); }   // lò gió nóng
  const skip = box(0.9 * s, 0.5 * s, 18 * s, dark, 0, 6.5 * s, 9 * s, g); skip.rotation.x = 0.68;   // cầu trượt nạp liệu
  const tap = basic('#ff9a3c'); box(1.2 * s, 0.8 * s, 0.2 * s, tap, 0, 1.0 * s, 2.06 * s, g);   // miệng ra gang
  const gl = glowSprite('#ff8a30', 1.0, 6 * s); gl.position.set(0, 1.2 * s, 3.2 * s); g.add(gl);
  const pl = new THREE.PointLight('#ff8a3a', 60, 26 * s, 1.6); pl.position.set(0, 1.5 * s, 4 * s); g.add(pl);
  return { g, glow: gl, light: pl };
}
function shed(parent, x, z, w, d, h, rot = 0, lit = 0.4) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = rot; parent.add(g);
  const wall = std('#3b4048', { roughness: 0.9 }), roof = std('#596069', { roughness: 0.7, metalness: 0.2 });
  box(w, h, d, wall, 0, h / 2, 0, g); const n = Math.floor(w / 3);
  for (let i = 0; i < n; i++) { const r = box(3.0, 0.15, d, roof, -w / 2 + 1.5 + i * 3, h + 0.7, 0, g); r.rotation.z = 0.42; box(0.1, 1.1, d * 0.96, std('#2a2620', { emissive: '#ff9a46', emissiveIntensity: lit * 0.8 }), -w / 2 + 2.9 + i * 3, h + 0.55, 0, g); }   // mái răng cưa, kính cửa mái ánh lò mờ
  for (let i = 0; i < n * 2; i++) for (const yy of [0.35, 0.62]) box(0.55, 0.7, 0.05, std('#1d1a17', { emissive: '#ffa34d', emissiveIntensity: lit * (0.5 + 0.5 * ((i * 7 + yy * 10) % 3 > 1)) }), -w / 2 + 0.9 + i * 1.5, h * yy, d / 2 + 0.03, g);   // ô cửa sổ nhỏ
  return g;
}
async function valley({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, '#1b2233', 0.0085);
  skyDome(scene, [[0, '#0b1222'], [0.36, '#1c2a46'], [0.46, '#4a4560'], [0.495, '#c8784a'], [0.505, '#e39654'], [0.53, '#202434'], [1, '#0e121b']]);
  const R = rng(11);
  // địa hình: thung lũng sông uốn theo trục x; đồi hai bên (vertex color theo độ cao)
  const riverZ = (x) => 6 * Math.sin(x * 0.035) + 2 * Math.sin(x * 0.11 + 1);
  const tg = new THREE.PlaneGeometry(420, 260, 210, 130); tg.rotateX(-Math.PI / 2); const P = tg.attributes.position, col = [];
  for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i), dz = Math.abs(z - riverZ(x));
    let y = dz < 9 ? -0.6 : Math.pow(Math.min(1, (dz - 9) / 70), 1.35) * 34 + 3 * Math.sin(x * 0.07 + z * 0.05) * Math.min(1, (dz - 9) / 20);
    if (dz > 9 && dz < 26 && z > riverZ(x)) y = Math.min(y, 1.2 + (dz - 9) * 0.05);   // bậc ven sông phía gần: đất bằng cho nhà máy
    P.setY(i, y); const k = Math.min(1, Math.max(0, y / 30)); const c = new THREE.Color('#1d2620').lerp(new THREE.Color('#38403a'), k); col.push(c.r, c.g, c.b); }
  tg.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); tg.computeVertexNormals();
  const terr = new THREE.Mesh(tg, std('#ffffff', { vertexColors: true, roughness: 1 })); terr.receiveShadow = true; scene.add(terr);
  const water = new THREE.Mesh(new THREE.PlaneGeometry(420, 260), std('#15202e', { roughness: 0.18, metalness: 0.65 })); water.rotation.x = -Math.PI / 2; water.position.y = -0.25; scene.add(water);
  // vệt phản chiếu cam trên mặt nước dưới các lò (sprite dẹt cộng sáng)
  const streak = softTex(); const refl = [];
  for (const x of [-14, -2, 10]) { const m = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 18), basic('#ff8a3a', { map: streak, transparent: true, opacity: 0.35, depthWrite: false, blending: THREE.AdditiveBlending })); m.rotation.x = -Math.PI / 2; m.position.set(x, -0.2, riverZ(x) + 2); scene.add(m); refl.push(m); }
  // nhà máy trên bậc ven sông gần (z > sông)
  const mill = new THREE.Group(); scene.add(mill); const bz = (x) => riverZ(x) + 15;
  const BF = [-14, -2, 10].map((x, i) => blastFurnace(mill, x, bz(x), 0.85 + 0.08 * (i % 2), R));
  shed(mill, 26, bz(26) + 2, 24, 12, 8, 0.05, 0.5); shed(mill, -36, bz(-36) + 3, 30, 14, 9, -0.04, 0.35); shed(mill, 2, bz(2) + 15, 40, 10, 6, 0, 0.25);
  const stacks = [];
  for (const [x, dz, h] of [[18, 8, 26], [21, 8, 26], [24, 8, 26], [-28, 10, 22], [-25, 10, 22]]) { cyl(0.7, 1.0, h, std('#40454c', { roughness: 0.8 }), x, h / 2, bz(x) + dz, mill, 14); box(0.6, 0.3, 0.6, basic('#ff3b2a'), x, h + 0.2, bz(x) + dz, mill); stacks.push([x, h, bz(x) + dz]); }
  const plumes = stacks.map(([x, h, z], i) => plume(scene, x, h + 0.5, z, { seed: 5 + i, op: 0.26, size: 2.4 }));
  BF.forEach((b, i) => plumes.push(plume(scene, [-14, -2, 10][i], 13.5, bz([-14, -2, 10][i]), { seed: 20 + i, color: '#e0c6b2', op: 0.22, size: 1.8 })));
  // hai tuyến ray dọc bậc ven sông + đoàn toa quặng
  const railM = std('#6f7782', { metalness: 0.6, roughness: 0.4 });
  for (const off of [27, 31]) for (let x = -120; x < 120; x += 4) { const z0 = riverZ(x) + off, z1 = riverZ(x + 4) + off, a = Math.atan2(z1 - z0, 4);
    for (const s of [-0.7, 0.7]) { const r = box(4.05, 0.12, 0.09, railM, x + 2, 0.75, (z0 + z1) / 2 + s); r.rotation.y = -a; } }
  const train = new THREE.Group(); scene.add(train); const cars = [];
  for (let i = 0; i < 16; i++) { const c = new THREE.Group(); box(3.2, 1.3, 2.0, std('#3a2c25', { roughness: 0.9 }), 0, 1.5, 0, c); box(3.0, 0.3, 1.8, std('#5a3a2a'), 0, 2.25, 0, c); train.add(c); cars.push(c); }
  // cầu giàn qua sông
  const br = new THREE.Group(); br.position.set(46, 0, riverZ(46)); br.rotation.y = Math.PI / 2 + 0.25; scene.add(br); const bm = std('#545b63', { metalness: 0.4, roughness: 0.6 });
  box(46, 0.6, 5, bm, 0, 6, 0, br); for (const s of [-2.4, 2.4]) { box(46, 0.3, 0.3, bm, 0, 11, s, br); for (let i = -11; i <= 11; i++) { const d = box(0.25, 5.6, 0.25, bm, i * 2, 8.5, s, br); d.rotation.z = (i % 2 ? 0.38 : -0.38); } }
  for (const x of [-12, 12]) box(2.6, 6.5, 6, std('#3e3b38'), x, 3, 0, br);
  // thị trấn trên sườn đồi bên kia sông: nhà nhỏ instanced + cửa sổ ấm
  const houseG = new THREE.BoxGeometry(1.6, 1.4, 1.4), roofG = new THREE.ConeGeometry(1.25, 0.9, 4); roofG.rotateY(Math.PI / 4);
  const NH = 420, hs = new THREE.InstancedMesh(houseG, std('#4b4a4a', { roughness: 0.95 }), NH), rf = new THREE.InstancedMesh(roofG, std('#2b2d33'), NH);
  const winPts = []; const M = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler();
  for (let i = 0; i < NH; i++) { const x = -110 + R() * 220, dz = 12 + R() * 34, z = riverZ(x) - dz; const y = Math.pow(Math.min(1, (dz - 9) / 70), 1.35) * 34 + 3 * Math.sin(x * 0.07 + z * 0.05) * Math.min(1, (dz - 9) / 20);
    e.set(0, R() * 0.6 - 0.3, 0); q.setFromEuler(e); M.compose(new THREE.Vector3(x, y + 0.7, z), q, new THREE.Vector3(1, 1, 1)); hs.setMatrixAt(i, M); M.compose(new THREE.Vector3(x, y + 1.85, z), q, new THREE.Vector3(1, 1, 1)); rf.setMatrixAt(i, M);
    if (R() < 0.55) winPts.push(x + 0.4, y + 0.8, z + 0.72); }
  hs.castShadow = hs.receiveShadow = true; scene.add(hs, rf);
  const wg = new THREE.BufferGeometry(); wg.setAttribute('position', new THREE.Float32BufferAttribute(winPts, 3));
  scene.add(new THREE.Points(wg, new THREE.PointsMaterial({ color: '#ffc47a', size: 0.35, transparent: true, opacity: 0.95, depthWrite: false })));
  // ánh sáng: trời chạng vạng + mặt trời thấp sau đồi + ánh lò cam
  scene.add(new THREE.HemisphereLight('#7f8fc0', '#2a2418', 2.6));
  const sun = new THREE.DirectionalLight('#ffb383', 2.4); sun.position.set(-120, 30, -160); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -90, right: 90, top: 60, bottom: -60, far: 400 }); scene.add(sun);
  const K = { a: [{ t: 0, p: [-46, 30, -52], l: [-4, 4, 16], mm: 28 }, { t: dur, p: [-38, 25, -44], l: [-2, 5, 16], mm: 30 }],
              b: [{ t: 0, p: [70, 8, 60], l: [0, 8, 14], mm: 28 }, { t: dur, p: [52, 10, 52], l: [-6, 8, 14], mm: 32 }] }[v] || null;
  const rig = camRig(W, H, K);
  const update = (t, f) => { rig.at(t); plumes.forEach((p) => p.update(t));
    BF.forEach((b, i) => { const k = 1 + 0.08 * Math.sin(f * 0.37 + i * 2) + 0.05 * Math.sin(f * 0.13 + i); b.light.intensity = 60 * k; b.glow.material.opacity = 0.9 * k; refl[i].material.opacity = 0.2 * k; });
    cars.forEach((c, i) => { const x = -70 + i * 3.6 + t * 1.6, z = riverZ(x) + 27, z2 = riverZ(x + 1) + 27; c.position.set(x, 0, z); c.rotation.y = -Math.atan2(z2 - z, 1); }); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2_WARM, exposure: 1.35 };
}

// ===== ingots: sa bàn thỏi thép (1 thỏi = 10 Mt) =====
async function ingots({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, C.ink, 0.006);
  const grid = canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = '#121b28'; g.fillRect(0, 0, w, h); for (let i = 0; i <= w; i += 32) { g.strokeStyle = i % 128 ? 'rgba(154,167,181,0.08)' : 'rgba(154,167,181,0.2)'; g.lineWidth = i % 128 ? 1 : 2; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } });
  grid.wrapS = grid.wrapT = THREE.RepeatWrapping; grid.repeat.set(6, 6);
  const floor = box(160, 0.2, 160, std('#ffffff', { map: grid, roughness: 0.85 }), 0, -0.1, 0); floor.receiveShadow = true;
  const ing = new THREE.BoxGeometry(1.6, 0.5, 0.7); ing.translate(0, 0.25, 0);
  const mSteel = std('#8e9aa8', { roughness: 0.38, metalness: 0.55 }), mUS = std(C.orange, { roughness: 0.45, metalness: 0.25, emissive: '#5a2a10', emissiveIntensity: 0.6 });
  // xếp thỏi thành khối: cols × rows mỗi lớp; trả danh sách vị trí theo thứ tự (lớp dưới trước)
  const pile = (n, cols, rows, ox, oz) => { const L = []; for (let i = 0; i < n; i++) { const layer = Math.floor(i / (cols * rows)), j = i % (cols * rows); const c = j % cols, r = Math.floor(j / cols); L.push([ox + (c - (cols - 1) / 2) * 1.75 + (layer % 2 ? 0.12 : 0), layer * 0.52, oz + ((rows - 1) / 2 - r) * 0.85]);   /* hàng 0 ở phía trước: phần của Mỹ (lớp đáy, hàng trước) luôn thấy */ } return L; };
  const P50 = pile(19, 3, 3, -16, 0), P25 = pile(185, 5, 4, 8, -2);
  const N = P50.length + P25.length, us = new Set([...Array(9).keys()].concat([...Array(8).keys()].map((k) => P50.length + k)));   // Mỹ: 87,8 → 9 thỏi; 81,9 → 8 thỏi (làm tròn tới 10 Mt)
  const steelIM = new THREE.InstancedMesh(ing, mSteel, N), usIM = new THREE.InstancedMesh(ing, mUS, N); steelIM.castShadow = usIM.castShadow = steelIM.receiveShadow = usIM.receiveShadow = true;
  scene.add(steelIM, usIM); const ALL = P50.concat(P25), M = new THREE.Matrix4(), Z = new THREE.Matrix4().makeScale(0, 0, 0);
  const place = (t) => { ALL.forEach((p, i) => { const grow = i < P50.length ? 1 : ease((t - 1.0 - (i - P50.length) * 0.018) / 0.5); const isUS = us.has(i);
      M.makeTranslation(p[0], p[1] + (1 - grow) * 3, p[2]); if (grow <= 0) M.copy(Z);
      steelIM.setMatrixAt(i, isUS ? Z : M); usIM.setMatrixAt(i, isUS ? M : Z); }); steelIM.instanceMatrix.needsUpdate = usIM.instanceMatrix.needsUpdate = true; };
  // bệ tên năm + nhãn số (số nổi trên vật thể)
  box(7, 0.25, 4.2, std('#1a2433', { roughness: 0.6 }), -16, 0.0, 0); box(10, 0.25, 5, std('#1a2433', { roughness: 0.6 }), 8, 0.0, -2);
  const L1 = label([{ t: '1950', size: 72, color: C.text }, { t: 'World 189 Mt', size: 40, color: C.steel }, { t: 'U.S. 87.8 Mt  ·  46%', size: 44, color: C.orange }], { scale: 2.8 }); L1.position.set(-16, 6.8, 0); scene.add(L1);
  const L2 = label([{ t: '2025', size: 72, color: C.text }, { t: 'World 1,849 Mt', size: 40, color: C.steel }, { t: 'U.S. 81.9 Mt  ·  4%', size: 44, color: C.orange }], { scale: 2.8 }); L2.position.set(8, 11.0, -2); scene.add(L2);
  const key = label([{ t: '1 bar = 10 million tonnes of crude steel', size: 34, color: C.steel, weight: 500, display: false }, { t: 'Sources: USGS Data Series 140; worldsteel, World Steel in Figures 2026', size: 26, color: '#7f8b99', weight: 400, display: false }], { accent: C.steel, w: 1400, scale: 2.4 }); key.position.set(-5, 1.6, 9.5); scene.add(key);
  scene.add(new THREE.HemisphereLight('#7f93b8', '#1a2230', 1.6));
  const keyL = new THREE.SpotLight('#ffffff', 2600, 140, 0.6, 0.6, 1.4); keyL.position.set(-18, 36, 26); keyL.target.position.set(0, 0, 0); keyL.castShadow = true; keyL.shadow.mapSize.set(2048, 2048); scene.add(keyL, keyL.target);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.9); rim.position.set(30, 12, -40); scene.add(rim);
  const warm = new THREE.PointLight(C.orange, 30, 22, 1.5); warm.position.set(-14, 4, 4); scene.add(warm);
  const K = { a: [{ t: 0, p: [-25, 5.5, 12], l: [-16, 2.5, 0], mm: 36 }, { t: dur, p: [-15, 15, 31], l: [-2, 3.5, -1], mm: 30 }] }[v] || null;
  const rig = camRig(W, H, K); const dst = dust(scene, [0, 6, 0], [40, 12, 30], 220, 7, '#b9c6d6');
  const update = (t) => { rig.at(t); place(t); dst.update(t); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.1 };
}

// ===== chain: bản đồ tuyến giản lược (lon/lat → mặt phẳng; 1 đv = 50 dặm) =====
const LL = ([lon, lat]) => [(lon + 84) * Math.cos(44 * Math.PI / 180) * 69 / 50, -(lat - 44) * 69 / 50];
const LAKES = {   // đường bờ giản lược (đủ nhận ra, không dùng đo đạc)
  superior: [[-92.1, 46.7], [-91.2, 46.9], [-90.4, 46.6], [-89.4, 46.9], [-88.4, 47.2], [-87.6, 46.5], [-86.6, 46.45], [-85.4, 46.75], [-84.6, 46.5], [-84.6, 46.95], [-84.9, 47.6], [-85.8, 47.95], [-86.7, 48.7], [-88.3, 48.8], [-89.3, 48.1], [-90.3, 47.7], [-91.6, 47.1]],
  michigan: [[-85.4, 45.9], [-86.2, 45.8], [-87.3, 45.6], [-87.6, 44.9], [-87.8, 44.1], [-87.9, 43.0], [-87.8, 42.3], [-87.5, 41.75], [-86.9, 41.65], [-86.4, 42.2], [-86.25, 43.0], [-86.45, 43.8], [-86.1, 44.6], [-85.6, 45.2], [-85.0, 45.75]],
  huron: [[-84.7, 45.9], [-84.0, 46.0], [-83.0, 46.1], [-81.6, 46.1], [-80.6, 45.9], [-80.0, 45.2], [-80.6, 44.6], [-81.3, 44.9], [-81.7, 44.3], [-81.7, 43.3], [-82.4, 43.0], [-82.7, 43.7], [-83.5, 43.9], [-83.4, 44.6], [-83.3, 45.1], [-84.2, 45.6]],
  erie: [[-83.45, 41.75], [-82.8, 41.5], [-81.7, 41.5], [-80.6, 41.95], [-79.9, 42.15], [-79.05, 42.75], [-79.4, 42.85], [-80.5, 42.55], [-81.6, 42.65], [-82.5, 42.05], [-83.15, 42.05]],
  ontario: [[-79.8, 43.3], [-79.2, 43.25], [-78.0, 43.35], [-76.8, 43.4], [-76.2, 43.6], [-76.4, 44.1], [-77.4, 43.9], [-78.8, 43.9], [-79.5, 43.65]],
};
async function chain({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, C.ink, 0.004);
  const grid = canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = '#3a4a5e'; g.fillRect(0, 0, w, h); for (let i = 0; i <= w; i += 64) { g.strokeStyle = 'rgba(220,230,240,0.16)'; g.lineWidth = 1; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } });
  grid.wrapS = grid.wrapT = THREE.RepeatWrapping; grid.repeat.set(4, 4);
  const land = box(60, 0.6, 40, std('#ffffff', { map: grid, roughness: 0.9 }), -4, -0.3, -2); land.receiveShadow = true;
  const lakeM = std('#0c1a2c', { roughness: 0.12, metalness: 0.4 }), shoreM = basic('#9fc3e0');
  for (const pts of Object.values(LAKES)) { const sh = new THREE.Shape(pts.map((p) => { const [x, z] = LL(p); return new THREE.Vector2(x, -z); }));
    const g = new THREE.ExtrudeGeometry(sh, { depth: 0.12, bevelEnabled: false }); g.rotateX(-Math.PI / 2); const m = new THREE.Mesh(g, lakeM); m.position.y = 0.02; scene.add(m);
    const lg = new THREE.BufferGeometry().setFromPoints(pts.concat([pts[0]]).map((p) => { const [x, z] = LL(p); return new THREE.Vector3(x, 0.16, z); })); scene.add(new THREE.Line(lg, new THREE.LineBasicMaterial({ color: shoreM.color }))); }
  // tuyến (theo lời Carnegie): quặng: mỏ → cảng hồ (ray) → tàu qua Superior, Soo, Huron, St Clair/Detroit, Erie → cảng Erie → ray → Pittsburgh
  const route = (pts, y = 0.35) => new THREE.CatmullRomCurve3(pts.map((p) => { const [x, z] = LL(p); return new THREE.Vector3(x, y, z); }), false, 'catmullrom', 0.2);
  const ORE_RAIL = route([[-92.9, 47.45], [-92.4, 47.1], [-92.05, 46.78]]);
  const BOAT = route([[-92.0, 46.8], [-90.0, 47.25], [-87.5, 47.6], [-85.6, 46.95], [-84.4, 46.45], [-83.9, 45.95], [-82.9, 45.3], [-82.4, 44.0], [-82.45, 43.1], [-82.65, 42.35], [-82.6, 41.95], [-81.6, 41.85], [-80.6, 42.0]], 0.3);
  const RAIL2 = route([[-80.6, 41.95], [-80.4, 41.4], [-80.2, 40.9], [-80.0, 40.44]]);
  const COKE = route([[-79.6, 40.02], [-79.8, 40.25], [-80.0, 40.44]]);
  const tubes = [[ORE_RAIL, C.orange, 0.11], [BOAT, C.orange, 0.13], [RAIL2, C.orange, 0.11], [COKE, C.amber, 0.11]].map(([cv, c, r]) => {
    const g = new THREE.TubeGeometry(cv, 240, r, 8, false); const m = new THREE.Mesh(g, basic(c)); scene.add(m); const gl = new THREE.Mesh(new THREE.TubeGeometry(cv, 240, r * 3.2, 8, false), basic(c, { transparent: true, opacity: 0.16, depthWrite: false, blending: THREE.AdditiveBlending })); scene.add(gl); return { g, gl: gl.geometry, n: g.index.count }; });
  const node = (p, c, r = 0.32) => { const [x, z] = LL(p); const m = cyl(r, r, 0.5, basic(c), x, 0.3, z, scene, 24); const s = glowSprite(c, 0.9, 1.6); s.position.set(x, 0.6, z); scene.add(s); return m; };
  node([-92.9, 47.45], C.orange); node([-92.05, 46.78], C.steel, 0.22); node([-80.6, 41.95], C.steel, 0.22); node([-79.6, 40.02], C.amber); node([-80.0, 40.44], C.text, 0.42);
  const boat = new THREE.Group(); box(0.9, 0.18, 0.22, std('#c4ccd6'), 0, 0.42, 0, boat); box(0.18, 0.2, 0.2, std('#e6eaef'), 0.32, 0.6, 0, boat); scene.add(boat);
  const lab = (lines, p, opt, dy = 2.2, dx = 0) => { const s = label(lines, opt); const [x, z] = LL(p); s.position.set(x + dx, dy, z); scene.add(s); return s; };
  const LB = [
    lab([{ t: 'Iron ore', size: 50 }, { t: '1.5 t per ton of steel', size: 34, color: C.orange, weight: 500 }], [-92.9, 47.45], { scale: 1.43 }, 2.4, -2.2),
    lab([{ t: 'Rail ≈ 100 mi to the Lakes', size: 34, weight: 500, color: C.steel }], [-92.3, 46.4], { scale: 1.30, accent: C.steel }, 1.4, -1.2),
    lab([{ t: 'Lake boats', size: 46 }, { t: 'hundreds of miles', size: 34, color: C.steel, weight: 500 }], [-87.6, 47.9], { scale: 1.43 }, 2.0),
    lab([{ t: 'Rail ≈ 150 mi', size: 34, weight: 500, color: C.steel }], [-79.4, 41.3], { scale: 1.30, accent: C.steel }, 1.4, 1.6),
    lab([{ t: 'Coke · Connellsville', size: 42 }, { t: '1.5 t coal · 50-odd mi', size: 34, color: C.amber, weight: 500 }], [-79.3, 39.7], { scale: 1.30, accent: C.amber }, 1.6, 2.2),
    lab([{ t: 'PITTSBURGH', size: 54 }, { t: '+ 1 t limestone · 150 mi', size: 32, color: C.steel, weight: 500 }], [-80.0, 40.44], { scale: 1.43, accent: C.text }, 2.6, -2.8),
  ];
  const src = label([{ t: 'Route as described by Andrew Carnegie, Autobiography (1920). Simplified map.', size: 28, color: '#8a96a4', weight: 400, display: false }], { accent: C.steel, w: 1500, scale: 2.86 });
  scene.add(src);
  scene.add(new THREE.HemisphereLight('#a9bad8', '#1a2230', 2.2));
  const sun = new THREE.DirectionalLight('#dfe8ff', 2.2); sun.position.set(-20, 40, 20); sun.castShadow = true; scene.add(sun);
  const K = { a: [{ t: 0, p: [-10, 17, 15], l: [-5.5, 0, -1.5], mm: 28 }, { t: dur, p: [-6, 14.5, 14.5], l: [-3, 0, -0.5], mm: 29 }] }[v] || null;
  const rig = camRig(W, H, K);
  const update = (t) => { rig.at(t);
    const seq = [[0, 0.18], [0.12, 0.62], [0.55, 0.78], [0.7, 0.9]];   // tuần tự: ray mỏ → tàu → ray → cốc
    tubes.forEach((tb, i) => { const u = ease((t / dur - seq[i][0]) / (seq[i][1] - seq[i][0])); const k = Math.floor(u * tb.n / 6) * 6; tb.g.setDrawRange(0, k); tb.gl.setDrawRange(0, k); });
    const ub = Math.min(0.999, Math.max(0, (t / dur - 0.12) / 0.5)); const p = BOAT.getPointAt(ub), p2 = BOAT.getPointAt(Math.min(1, ub + 0.002)); boat.position.copy(p).setY(0); boat.rotation.y = -Math.atan2(p2.z - p.z, p2.x - p.x);
    LB.forEach((s, i) => { s.material.opacity = ease((t / dur - [0.02, 0.06, 0.25, 0.62, 0.72, 0.8][i]) / 0.08); });
  };
  src.position.set(-4.5, 0.8, 10.5);
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.05 };
}

// ===== furnace: xưởng Bessemer, lò chuyển rót thép =====
async function furnace({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, '#151a22', 0.03); const R = rng(4);
  const conc = canvasTex(512, 512, (g, w, h) => { g.fillStyle = '#3a3a38'; g.fillRect(0, 0, w, h); for (let i = 0; i < 2600; i++) { g.fillStyle = `rgba(${R() < 0.5 ? 20 : 90},${R() < 0.5 ? 20 : 85},${R() < 0.5 ? 18 : 80},${0.08 + R() * 0.12})`; g.fillRect(R() * w, R() * h, 2 + R() * 6, 2 + R() * 6); } g.strokeStyle = 'rgba(15,15,15,0.5)'; g.lineWidth = 2; for (let i = 0; i <= w; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } });
  conc.wrapS = conc.wrapT = THREE.RepeatWrapping; conc.repeat.set(8, 8);
  box(80, 0.2, 60, std('#ffffff', { map: conc, roughness: 0.95 }), 0, -0.1, 0).receiveShadow = true;
  const iron = std('#2b2f36', { roughness: 0.75, metalness: 0.3 }), brick = std('#4a2c22', { roughness: 0.95 });
  for (let x = -24; x <= 24; x += 8) for (const z of [-10, 12]) { box(0.8, 18, 0.8, iron, x, 9, z); }   // cột
  for (let x = -24; x <= 24; x += 8) { box(0.5, 0.6, 22, iron, x, 18, 1); for (let k = -5; k <= 5; k++) { const d = box(0.15, 2.4, 0.15, iron, x, 17, 1 + k * 2); d.rotation.x = k % 2 ? 0.6 : -0.6; } }   // giàn mái
  box(52, 1.2, 1.0, std('#5a4a2a', { roughness: 0.7 }), 0, 14.5, -9); box(52, 1.2, 1.0, std('#5a4a2a'), 0, 14.5, 11);   // đường ray cầu trục
  const crane = new THREE.Group(); box(1.4, 1.6, 21, std('#6b5a2c', { roughness: 0.6, metalness: 0.2 }), 0, 15.6, 1, crane); box(2.4, 1.4, 2.4, iron, 0, 14.4, -2, crane); scene.add(crane);
  const hook = cyl(0.04, 0.04, 6, std('#1b1b1b'), 0, 11.0, -2, crane, 6);
  for (let x = -20; x <= 20; x += 8) { const w = box(5, 6, 0.1, basic('#5a7aa6', { transparent: true, opacity: 0.22 }), x, 11, -10.4); }   // cửa sổ cao (ánh lạnh)
  // lò chuyển Bessemer: thân quả lê (lathe), trục ngang, bệ gạch; nghiêng rót
  const conv = new THREE.Group(); conv.position.set(-2, 5.2, -1); scene.add(conv);
  const prof = [[0, -3.0], [1.4, -2.9], [2.2, -2.2], [2.5, -0.8], [2.4, 0.8], [1.9, 2.0], [1.2, 2.8], [0.95, 3.25], [0.85, 3.3]].map(([a, b]) => new THREE.Vector2(a, b));
  const shellM = std('#3d424a', { roughness: 0.5, metalness: 0.5 }); const body = new THREE.Mesh(new THREE.LatheGeometry(prof, 36), shellM); body.castShadow = true; conv.add(body);
  for (const y of [-1.6, -0.2, 1.2]) { const r = new THREE.Mesh(new THREE.TorusGeometry(2.48 - Math.abs(y) * 0.12, 0.09, 6, 40), std('#23262b')); r.rotation.x = Math.PI / 2; r.position.y = y; conv.add(r); }
  const trun = cyl(0.45, 0.45, 7.6, std('#23262b', { metalness: 0.4 }), 0, 0, 0, conv); trun.rotation.x = Math.PI / 2;
  for (const z of [-4.1, 4.1]) box(1.0, 5.0, 0.8, brick, -2, 2.5, -1 + z);
  const mouthGlow = glowSprite('#ffb04a', 1.0, 5); conv.add(mouthGlow); mouthGlow.position.set(0, 3.5, 0);
  // dòng thép lỏng + thùng rót
  const ladle = new THREE.Group(); ladle.position.set(3.6, 0, -1); scene.add(ladle);
  const lb = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [1.5, 0], [1.75, 2.6], [1.85, 2.7], [0, 2.7]].map(([a, b]) => new THREE.Vector2(a, b)), 28), std('#33363b', { roughness: 0.6, metalness: 0.4 })); lb.castShadow = true; ladle.add(lb);
  const melt = cyl(1.68, 1.68, 0.05, basic('#ffcf6a'), 0, 2.45, 0, ladle, 28); const mGlow = glowSprite('#ff9a3a', 0.95, 6); mGlow.position.set(0, 3.2, 0); ladle.add(mGlow);
  const streamM = basic('#ffd27a'); const stream = cyl(0.22, 0.32, 1, streamM, 0, 0, 0, scene, 10);
  const sparks = (() => { const n = 700, pos = new Float32Array(n * 3), seed = [...Array(n)].map(() => [R(), R(), R(), R()]); const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    const pts = new THREE.Points(g, new THREE.PointsMaterial({ color: '#ffc067', size: 0.09, transparent: true, opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending })); scene.add(pts);
    return (t, origin) => { seed.forEach(([a, b, c, d], i) => { const u = (t * (0.6 + a * 0.8) + d) % 1; const ang = a * 6.28, sp = 3 + b * 6; pos[i * 3] = origin.x + Math.cos(ang) * sp * u * 0.8; pos[i * 3 + 1] = origin.y + (2 + c * 5) * u - 4.9 * u * u * 1.6; pos[i * 3 + 2] = origin.z + Math.sin(ang) * sp * u * 0.6; }); g.attributes.position.needsUpdate = true; }; })();
  // người vận hành (bóng, không mặt), ánh viền cam
  const men = [[-8, 3, 0.6], [7.5, 2.0, -0.9], [9, 4.5, -1.4]].map(([x, z, ry], i) => { const f = figure({ color: '#15130f', scale: 1.05 }); f.root.position.set(x, 0, z); f.root.rotation.y = ry; scene.add(f.root); f.set({ armR: i === 0 ? -0.6 : -0.2, armL: -0.15 }); const rl = new THREE.PointLight('#ff9a4a', 5, 4, 1.8); rl.position.set(x + 0.6, 1.5, z - 0.8); scene.add(rl); return f; });
  // ánh sáng: miệng lò cam rất mạnh, cửa sổ cao lạnh, nền lạnh
  scene.add(new THREE.HemisphereLight('#4d6290', '#1a120c', 1.4));
  const cold = new THREE.DirectionalLight('#8fb0e6', 1.8);
  const fillW = new THREE.PointLight('#ffb070', 60, 30, 1.5); fillW.position.set(8, 6, 8); scene.add(fillW); cold.position.set(-10, 20, -30); scene.add(cold);
  const hot = new THREE.PointLight('#ff8a32', 260, 40, 1.7); hot.position.set(2, 6, 1); hot.castShadow = true; hot.shadow.mapSize.set(1024, 1024); scene.add(hot);
  const hot2 = new THREE.PointLight('#ffb050', 90, 18, 1.6); hot2.position.set(3.6, 3.6, 0); scene.add(hot2);
  const dst = dust(scene, [1, 6, 0], [20, 10, 12], 400, 9, '#ffcc99');
  const K = { a: [{ t: 0, p: [13, 4.0, 12.5], l: [0, 4.2, -1.5], mm: 28 }, { t: dur, p: [10.5, 3.6, 10.5], l: [0.5, 4.0, -1.5], mm: 30 }] }[v] || null;
  const rig = camRig(W, H, K);
  const update = (t, f) => { rig.at(t); dst.update(t);
    const tilt = lerp(0.95, 1.18, ease(t / dur)); conv.rotation.z = -tilt;   // nghiêng sang phải, miệng hướng thùng rót
    const mouth = new THREE.Vector3(0, 3.3, 0).applyMatrix4(conv.matrixWorld.compose(conv.position, new THREE.Quaternion().setFromEuler(conv.rotation), new THREE.Vector3(1, 1, 1)));
    const top = mouth.clone(), bot = new THREE.Vector3(3.6, 2.5, -1); const mid = top.clone().add(bot).multiplyScalar(0.5); stream.position.copy(mid); stream.scale.set(1, top.distanceTo(bot), 1); stream.lookAt(bot); stream.rotateX(Math.PI / 2);
    sparks(t, bot.clone().setY(2.7)); const fl = 1 + 0.1 * Math.sin(f * 0.9) + 0.06 * Math.sin(f * 0.37); hot.intensity = 260 * fl; hot2.intensity = 90 * fl; mGlow.material.opacity = 0.9 * fl; mouthGlow.material.opacity = 0.85 * fl;
    crane.position.x = lerp(-6, 4, ease(t / dur)); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2_WARM, exposure: 1.0 };
}

// ===== trade: sa bàn thương mại 2025–2026 =====
async function trade({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, C.ink, 0.007);
  const grid = canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = '#121b28'; g.fillRect(0, 0, w, h); for (let i = 0; i <= w; i += 32) { g.strokeStyle = i % 128 ? 'rgba(154,167,181,0.07)' : 'rgba(154,167,181,0.18)'; g.lineWidth = i % 128 ? 1 : 2; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } });
  grid.wrapS = grid.wrapT = THREE.RepeatWrapping; grid.repeat.set(6, 6);
  box(200, 0.2, 200, std('#ffffff', { map: grid, roughness: 0.85 }), 0, -0.1, 0).receiveShadow = true;
  // bệ sản lượng 2025 (chiều cao ∝ Mt; 100 Mt = 1 đv): TQ 960,8 · EU 126,0 · Mỹ 81,9 (worldsteel 2026)
  const ped = (x, z, mt, name, col) => { const h = mt / 100; const g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g);
    const m = box(5, h, 5, std(col, { roughness: 0.4, metalness: 0.45 }), 0, h / 2, 0, g); m.castShadow = m.receiveShadow = true; box(5.6, 0.3, 5.6, std('#223044'), 0, 0.15, 0, g);
    const L = label([{ t: name, size: 50 }, { t: `${mt.toLocaleString('en-US', { minimumFractionDigits: 1 })} Mt crude steel, 2025`, size: 32, color: C.steel, weight: 500, display: false }], { scale: 2.64, accent: C.steel }); L.position.set(0, Math.max(h + 1.8, 7.2), 0); g.add(L); return { g, h }; };
  const CN = ped(-14, -6, 960.8, 'China', '#8e9aa8'), US = ped(16, 4, 81.9, 'United States', '#8e9aa8'), EU = ped(6, -16, 126.0, 'European Union', '#8e9aa8');
  // cung xuất khẩu TQ 2025: 131,2 Mt (dày) — tới "thị trường thế giới" (không chỉ đích cụ thể)
  const arcs = []; const ends = [[22, 14], [30, -4], [10, 22], [-2, 24], [26, -22]];
  ends.forEach(([x, z], i) => { const a = new THREE.Vector3(-14, CN.h * 0.6, -6), b = new THREE.Vector3(x, 0.2, z), m = a.clone().add(b).multiplyScalar(0.5).setY(CN.h * 0.75 + 4);
    const cv = new THREE.QuadraticBezierCurve3(a, m, b); const g = new THREE.TubeGeometry(cv, 120, 0.09 + 0.05 * (i === 0), 8, false); const mesh = new THREE.Mesh(g, basic(C.orange)); scene.add(mesh); arcs.push({ g, n: g.index.count, cv }); });
  const exL = label([{ t: 'China steel exports, 2025', size: 44 }, { t: '131.2 Mt · record', size: 56, color: C.orange }, { t: 'OECD Steel Outlook 2026', size: 28, color: '#7f8b99', weight: 400, display: false }], { scale: 2.97 }); exL.position.set(4, 13.5, 2); scene.add(exL);
  // tường thuế quanh bệ Mỹ (kính cam mờ) + cổng hạn ngạch EU
  const wallM = new THREE.MeshStandardMaterial({ color: C.orange, emissive: '#5a2a10', transparent: true, opacity: 0.16, roughness: 0.3, side: THREE.DoubleSide, depthWrite: false });
  const wall = new THREE.Mesh(new THREE.CylinderGeometry(6.5, 6.5, 4.2, 48, 1, true), wallM); wall.position.set(16, 2.1, 4); scene.add(wall);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(6.5, 0.06, 6, 64), basic(C.orange)); ring.rotation.x = Math.PI / 2; ring.position.set(16, 4.2, 4); scene.add(ring);
  const tL = label([{ t: 'U.S. Section 232 tariff', size: 40 }, { t: '50% on steel', size: 54, color: C.orange }, { t: 'as of Oct 2026', size: 28, color: C.steel, weight: 500, display: false }], { scale: 2.64 }); tL.position.set(24, 3.2, 8); scene.add(tL);
  const gate = new THREE.Group(); gate.position.set(6, 0, -9.5); scene.add(gate); for (const x of [-3.2, 3.2]) box(0.5, 5, 0.5, std(C.teal, { roughness: 0.4, emissive: '#0f3a34', emissiveIntensity: 0.6 }), x, 2.5, 0, gate); box(6.9, 0.5, 0.5, std(C.teal, { emissive: '#0f3a34', emissiveIntensity: 0.6 }), 0, 5, 0, gate);
  const gL = label([{ t: 'EU quota from 1 July 2026', size: 38 }, { t: '18.3 Mt / year', size: 50, color: C.teal }, { t: '50% duty above quota', size: 34, color: C.steel, weight: 500, display: false }], { scale: 2.64, accent: C.teal }); gL.position.set(-1.5, 7.6, -9.5); scene.add(gL);
  // dư thừa công suất 2028 (dự báo): khối nét đứt hổ phách bên cạnh TQ
  const prM = new THREE.LineDashedMaterial({ color: C.amber, dashSize: 0.5, gapSize: 0.35 }); const pe = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(5, 7.45, 5)), prM); pe.computeLineDistances(); pe.position.set(-24, 3.725, 4); scene.add(pe);
  const pL = label([{ t: 'PROJECTION · OECD', size: 32, color: C.amber, display: false }, { t: 'Global excess capacity', size: 40 }, { t: '745 Mt by 2028', size: 50, color: C.amber }], { scale: 2.49, accent: C.amber, dashed: true }); pL.position.set(-24, 10, 4); scene.add(pL);
  scene.add(new THREE.HemisphereLight('#7f93b8', '#1a2230', 1.8));
  const keyL = new THREE.SpotLight('#ffffff', 4200, 180, 0.7, 0.6, 1.4); keyL.position.set(-10, 50, 40); keyL.castShadow = true; keyL.shadow.mapSize.set(2048, 2048); scene.add(keyL);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.8); rim.position.set(30, 14, -40); scene.add(rim);
  const K = { a: [{ t: 0, p: [27, 11, 27], l: [0, 5, -4], mm: 26 }, { t: dur, p: [24, 12.5, 28], l: [-1, 5, -4], mm: 25 }] }[v] || null;
  const rig = camRig(W, H, K);
  const update = (t) => { rig.at(t); arcs.forEach((a, i) => { const u = ease((t - 0.3 - i * 0.25) / 2.0); a.g.setDrawRange(0, Math.floor(u * a.n / 6) * 6); }); wallM.opacity = 0.18 + 0.05 * Math.sin(t * 1.4); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.1 };
}

// ===== north: tầng 3 — hydro, điện, lò hồ quang (giờ xanh phương bắc) =====
async function north({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, '#1d2a3e', 0.009); const R = rng(23);
  skyDome(scene, [[0, '#0a1430'], [0.38, '#1e3460'], [0.47, '#4f6a96'], [0.5, '#8aa3c4'], [0.52, '#2a3446'], [1, '#121820']]);
  const tg = new THREE.PlaneGeometry(400, 300, 160, 120); tg.rotateX(-Math.PI / 2); const P = tg.attributes.position;
  for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i); const d = Math.hypot(x, z + 10); P.setY(i, d < 40 ? 0 : Math.pow((d - 40) / 160, 1.6) * 40 * (0.6 + 0.4 * Math.sin(x * 0.03 + 1))); }
  tg.computeVertexNormals(); const snow = new THREE.Mesh(tg, std('#c9d3e0', { roughness: 0.92 })); snow.receiveShadow = true; scene.add(snow);
  // rừng thông (nón instanced)
  const cone = new THREE.ConeGeometry(1.1, 4.2, 7); cone.translate(0, 2.1, 0); const NT = 900, pines = new THREE.InstancedMesh(cone, std('#1c2b26', { roughness: 1 }), NT); const M = new THREE.Matrix4();
  for (let i = 0; i < NT; i++) { let x, z; do { x = -180 + R() * 360; z = -150 + R() * 200; } while (Math.hypot(x, z + 10) < 46); const d = Math.hypot(x, z + 10); const y = Math.pow(Math.max(0, d - 40) / 160, 1.6) * 40 * (0.6 + 0.4 * Math.sin(x * 0.03 + 1)); const s = 0.7 + R() * 0.8; M.compose(new THREE.Vector3(x, y - 0.2, z), new THREE.Quaternion(), new THREE.Vector3(s, s * (0.9 + R() * 0.4), s)); pines.setMatrixAt(i, M); }
  pines.castShadow = true; scene.add(pines);
  const plant = new THREE.Group(); scene.add(plant); const clad = std('#5d6874', { roughness: 0.6, metalness: 0.3 }), dark = std('#2d343d', { roughness: 0.8 });
  // tháp khử trực tiếp (shaft) + giàn + ống
  cyl(2.6, 2.9, 34, std('#7c8794', { roughness: 0.45, metalness: 0.45 }), -6, 17, -14, plant, 32); box(8, 0.4, 8, dark, -6, 22, -14, plant); box(8, 0.4, 8, dark, -6, 30, -14, plant);
  for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) box(0.35, 34, 0.35, dark, -6 + a * 3.8, 17, -14 + b * 3.8, plant);
  const pipeH = cyl(0.5, 0.5, 24, std('#9aa7b5', { metalness: 0.5, roughness: 0.35 }), 6, 18, -14, plant, 12); pipeH.rotation.z = Math.PI / 2;
  const tealBand = basic(C.teal); for (const y of [6, 14, 26]) { const r = new THREE.Mesh(new THREE.TorusGeometry(2.75, 0.12, 6, 40), tealBand); r.rotation.x = Math.PI / 2; r.position.set(-6, y, -14); plant.add(r); }
  // nhà điện phân: dãy nhà dài, dải đèn xanh lục lam
  for (let k = 0; k < 4; k++) { const z = -2 + k * 6; box(30, 5, 4, clad, 22, 2.5, z, plant); box(30, 0.25, 0.08, basic(C.teal), 22, 3.6, z + 2.05, plant); for (let i = 0; i < 14; i++) box(0.9, 0.5, 0.05, std('#16201f', { emissive: '#7fe0d2', emissiveIntensity: 0.55 }), 8.5 + i * 2.1, 2.2, z + 2.04, plant); }
  // xưởng lò hồ quang điện: nhà cao, cửa thông gió hắt cam, đống thép phế
  box(26, 14, 16, std('#4a535d', { roughness: 0.7 }), -30, 7, 6, plant); for (let i = 0; i < 12; i++) box(1.1, 0.45, 0.08, std('#1d1a17', { emissive: '#ff9a46', emissiveIntensity: 1.2 }), -41 + i * 2, 12.6, 14.05, plant);   // khe thông gió
  const eafGlow = glowSprite('#ff9040', 0.75, 9); eafGlow.position.set(-30, 12, 15.5); scene.add(eafGlow); const eafL = new THREE.PointLight('#ff8a3a', 80, 30, 1.6); eafL.position.set(-30, 8, 18); scene.add(eafL);
  for (let i = 0; i < 70; i++) { const b = box(0.6 + R() * 1.6, 0.3 + R() * 0.7, 0.4 + R(), std(R() < 0.5 ? '#5a4234' : '#6c6a66', { roughness: 0.95 }), -40 + R() * 12, 0.3 + R() * 1.5, 18 + R() * 8); b.rotation.set(R(), R() * 3, R()); }
  // tua-bin gió trên đồi + đường dây
  const turbines = [];
  for (let k = 0; k < 7; k++) { const x = -90 + k * 30, z = -120 + (k % 2) * 14, d = Math.hypot(x, z + 10), y = Math.pow(Math.max(0, d - 40) / 160, 1.6) * 40 * (0.6 + 0.4 * Math.sin(x * 0.03 + 1));
    const g = new THREE.Group(); g.position.set(x, y, z); scene.add(g); cyl(0.5, 0.9, 30, std('#e3e8ee', { roughness: 0.5 }), 0, 15, 0, g, 12); box(1.4, 1.2, 3, std('#e3e8ee'), 0, 30, 0.6, g);
    const rot = new THREE.Group(); rot.position.set(0, 30, 2.2); g.add(rot); for (let b = 0; b < 3; b++) { const bl = box(0.5, 14, 0.15, std('#eef1f4'), 0, 7, 0, new THREE.Group()); const arm = bl.parent; arm.rotation.z = b * 2.094; rot.add(arm); }
    const red = glowSprite('#ff3b2a', 0.9, 2.2); red.position.set(0, 31, 0.6); g.add(red); turbines.push({ rot, red, ph: R() * 6 }); }
  // nhãn CO₂ theo tuyến (worldsteel, dữ liệu 2024) — số nổi trên vật thể
  const l1 = label([{ t: 'Scrap → electric arc furnace', size: 40 }, { t: '≈ 0.69 t CO₂ per t steel', size: 46, color: C.orange }], { scale: 3.40 }); l1.position.set(-30, 19, 8); scene.add(l1);
  const l2 = label([{ t: 'Hydrogen-reduced iron (HYBRIT pilot, 2021)', size: 36 }, { t: 'industrial scale: timelines under review', size: 32, color: C.teal, weight: 500, display: false }], { scale: 3.40, accent: C.teal }); l2.position.set(-6, 39, -14); scene.add(l2);
  const l3 = label([{ t: 'Blast furnace route: ≈ 2.34 t CO₂ per t', size: 34, color: C.steel, weight: 500, display: false }, { t: 'worldsteel, 2024 data', size: 26, color: '#7f8b99', weight: 400, display: false }], { scale: 3.40, accent: C.steel }); l3.position.set(24, 9, 8); scene.add(l3);
  scene.add(new THREE.HemisphereLight('#8aa6d6', '#2a3040', 0.9));
  const moon = new THREE.DirectionalLight('#a9c2ee', 0.9); moon.position.set(60, 50, -80); moon.castShadow = true; moon.shadow.mapSize.set(2048, 2048); Object.assign(moon.shadow.camera, { left: -80, right: 80, top: 60, bottom: -60, far: 300 }); scene.add(moon);
  const K = { a: [{ t: 0, p: [26, 12, 70], l: [-6, 12, -6], mm: 30 }, { t: dur, p: [10, 14, 58], l: [-8, 13, -8], mm: 32 }] }[v] || null;
  const rig = camRig(W, H, K); const dst = dust(scene, [-6, 10, 10], [60, 20, 40], 500, 21, '#e6f0ff');   // tuyết lất phất
  const update = (t, f) => { rig.at(t); dst.update(t * 3); turbines.forEach((tb) => { tb.rot.rotation.z = tb.ph + t * 0.9; tb.red.material.opacity = (Math.floor(t * 0.8 + tb.ph) % 2) ? 0.9 : 0.15; }); const k = 1 + 0.08 * Math.sin(f * 0.5); eafL.intensity = 80 * k; eafGlow.material.opacity = 0.7 * k; };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.05 };
}

export const HEROES = { valley, ingots, chain, furnace, trade, north };

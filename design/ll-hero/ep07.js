// Last Lamplighters · Tập 7 "When Computers Were People" — CẢNH ĐINH 3D (dựng riêng, không lặp bố cục cảnh đinh tập trước).
//   airfield  ngoài trời: phòng thí nghiệm thấp bên sân bay lúc chạng vạng, dải cửa sổ dài của phòng tính toán, nhà chứa máy bay và ống hầm gió in bóng trên trời;
//             tháp văn phòng hôm nay ở bên kia đường. a: đẩy máy vào dải cửa sổ (móc câu) · b: người thắp đèn thắp cột đèn cạnh cửa sổ, đèn bàn trong phòng bừng theo (ngọn lửa trao qua ô kính)
//             c: cầu nối 09 (cửa sổ tắt, máy lia sang tháp, một tầng bừng sáng) · d: kết (cột đèn cuối, máy cẩu lên thấy cả hai toà nhà)
//   pool      trong phòng tính toán 1940s: hàng bàn gỗ, máy tính cơ có xe chạy, giấy kẻ ô, thước tính, đèn bàn chao xanh, bảng đen, máy đọc phim áp kế.
//             a: lia dọc một hàng (opt.n: số ghế có người) · b: cận một bàn (xe máy tính nhảy bậc, đường đồ thị vẽ dần; opt.orbit: quỹ đạo; opt.stack: chồng giấy cao dần)
//             c: góc cao cẩu lên (opt.grow: phòng đầy dần người; opt.empty: đèn bàn tắt dần) · d: vách ngăn hai phòng giống hệt nhau · e: nhìn qua khung cửa hẹp từ hành lang tối
//   relay     phòng máy rơ-le 1947: hai dãy tủ rơ-le cao, đèn báo nhấp nháy, bàn đọc băng đục lỗ có băng chạy, người vận hành (bóng). a: dọc hành lang tủ · b: cận đầu đọc băng
//   tower     văn phòng tầng cao hôm nay, đêm: bàn có hai màn hình mã hiện dần, đèn bàn ấm, hàng bàn trống, ánh phố ngoài kính.
//             a: từ ngoài mặt kính đẩy vào · b: qua vai, màn hình mã (opt.check: giây dòng mã được đánh dấu, con trỏ dừng) · c: toàn sàn, bàn đầu hàng trống, đèn tắt
//   ladder    góc phố đêm: cái thang của người thắp đèn tựa vào cột đèn; máy hạ từ ngọn đèn xuống bậc dưới cùng chìm trong bóng (câu hỏi bậc đầu).
import { THREE, useScene, gasLamp, figure, dust, camRig, box, cyl, lam, std, glowSprite, rng, ease, lerp, canvasTex } from './kit.js';

const fogOf = (scene, color, d) => { useScene(scene); scene.fog = new THREE.FogExp2(color, d); scene.background = new THREE.Color(color); };
const basic = (color, o = {}) => new THREE.MeshBasicMaterial({ color, ...o });

// nhân viên tính toán 1940s (bóng vô danh, không mặt): búi tóc sau gáy, vai hẹp; tư thế ngồi
function computerWoman({ color = '#1b1512', scale = 0.92, rim = null } = {}) {
  const f = figure({ seated: true, scale, color }); const m = lam(color);
  const bun = new THREE.Mesh(new THREE.SphereGeometry(0.07 * scale, 12, 10), m); bun.position.set(0, 1.18 * scale, -0.1 * scale); f.root.add(bun);
  for (const a of [f.armL, f.armR]) { const sh = new THREE.Mesh(new THREE.SphereGeometry(0.075 * scale, 12, 10), m); a.add(sh); const hd = new THREE.Mesh(new THREE.SphereGeometry(0.045 * scale, 10, 8), lam('#6a5040')); hd.position.set(0, -0.62 * scale, 0); a.add(hd); }   /* vai tròn, bàn tay sáng: bớt dáng khối trụ (Q27 lần 4) */
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.1 * scale, 0.025 * scale, 8, 20), lam('#d8cfb8')); collar.rotation.x = Math.PI / 2; collar.position.set(0, 1.03 * scale, 0); f.root.add(collar);
  if (rim) { const r = new THREE.PointLight(rim, 0.9, 1.4, 2); r.position.set(0, 1.4 * scale, -0.5 * scale); f.root.add(r); }
  return f;
}

// mặt bàn phím máy tính cơ (kết cấu: lưới phím số 10 cột × 8 hàng, phím tròn kem trên nền sắt)
const keysTex = () => canvasTex(256, 200, (g, w, h) => { g.fillStyle = '#3a3d42'; g.fillRect(0, 0, w, h);
  for (let c = 0; c < 10; c++) for (let r = 0; r < 8; r++) { g.fillStyle = c % 2 ? '#d8cfb6' : '#cbbf9f'; g.beginPath(); g.arc(14 + c * 24.5, 14 + r * 24, 8, 0, 7); g.fill(); g.fillStyle = '#5a5244'; g.font = '10px DejaVu Sans'; g.fillText(String(8 - r), 10 + c * 24.5, 18 + r * 24); } });
const slideTex = () => canvasTex(512, 32, (g, w, h) => { g.fillStyle = '#efe6cf'; g.fillRect(0, 0, w, h); g.strokeStyle = '#2a241c'; g.lineWidth = 1;
  for (let i = 0; i < 120; i++) { const x = 8 + Math.log10(1 + i * 0.075) * 470; g.beginPath(); g.moveTo(x, 0); g.lineTo(x, i % 10 ? 7 : 13); g.stroke(); g.beginPath(); g.moveTo(x, h); g.lineTo(x, h - (i % 10 ? 7 : 13)); g.stroke(); } });
const chalkTex = () => canvasTex(1024, 384, (g, w, h) => { g.fillStyle = '#1f2a22'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(230,230,215,0.75)'; g.fillStyle = 'rgba(230,230,215,0.8)'; g.lineWidth = 3;
  g.font = 'italic 34px DejaVu Serif'; const L = ['C  =  L / (q S)', 'q = ½ ρ V²', 'M = V / a', 'Δp = p₁ − p₂', 'Σ Cₙ Δx']; L.forEach((s, i) => g.fillText(s, 40 + (i % 2) * 470, 70 + Math.floor(i / 2) * 110));
  g.beginPath(); for (let x = 0; x <= 300; x += 4) { const y = 300 - 120 * Math.exp(-((x - 150) ** 2) / 4000); x ? g.lineTo(640 + x, y) : g.moveTo(640, y); } g.stroke(); g.beginPath(); g.moveTo(630, 330); g.lineTo(960, 330); g.moveTo(640, 340); g.lineTo(640, 160); g.stroke(); });

// tờ giấy kẻ ô có đường đồ thị vẽ dần (kết cấu vẽ lại khi u đổi)
function graphSheet(orbit = false) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 384; const g = c.getContext('2d'); const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  let last = -1;
  const draw = (u) => { u = Math.max(0, Math.min(1, u)); if (Math.abs(u - last) < 0.004) return; last = u;
    g.fillStyle = '#f1ead6'; g.fillRect(0, 0, 512, 384);
    for (let i = 0; i <= 512; i += 16) { g.strokeStyle = i % 80 ? 'rgba(90,140,120,0.35)' : 'rgba(60,110,95,0.7)'; g.lineWidth = i % 80 ? 1 : 1.6; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 384); g.stroke(); }
    for (let j = 0; j <= 384; j += 16) { g.strokeStyle = j % 80 ? 'rgba(90,140,120,0.35)' : 'rgba(60,110,95,0.7)'; g.lineWidth = j % 80 ? 1 : 1.6; g.beginPath(); g.moveTo(0, j); g.lineTo(512, j); g.stroke(); }
    g.strokeStyle = '#2a2a3a'; g.lineWidth = 3.2; g.beginPath();
    if (orbit) { g.arc(256, 200, 30, 0, 7); g.fillStyle = '#5a6d8a'; g.fill(); g.beginPath(); const n = Math.floor(240 * u);
      for (let k = 0; k <= n; k++) { const a = -Math.PI / 2 + (k / 240) * Math.PI * 2, x = 256 + 200 * Math.cos(a) - 60, y = 200 + 120 * Math.sin(a); k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
    else { const n = Math.floor(60 * u); for (let k = 0; k <= n; k++) { const x = 40 + k * 7.2, y = 330 - 230 * (1 - Math.exp(-k / 18)) + 14 * Math.sin(k * 0.5) * Math.exp(-k / 25); k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
      g.fillStyle = '#2a2a3a'; for (let k = 0; k <= n; k += 6) { const x = 40 + k * 7.2, y = 330 - 230 * (1 - Math.exp(-k / 18)) + 14 * Math.sin(k * 0.5) * Math.exp(-k / 25); g.fillRect(x - 4, y - 4, 8, 8); } }
    tex.needsUpdate = true; };
  draw(0); return { tex, draw };
}

// bàn tính toán: mặt gỗ, máy tính cơ (xe chạy), giấy kẻ ô, thước tính, đèn bàn chao xanh, ghế + người (tuỳ)
function computeDesk(parent, x, z, { person = true, lampOn = true, hero = false, orbit = false, seed = 1, pc } = {}) {
  const R = rng(seed), d = new THREE.Group(); d.position.set(x, 0, z); parent.add(d);
  const wood = std('#6b4528', { roughness: 0.65 }), dark = std('#3a2414');
  box(1.5, 0.05, 0.8, wood, 0, 0.76, 0, d); box(0.06, 0.74, 0.74, dark, -0.7, 0.37, 0, d); box(0.06, 0.74, 0.74, dark, 0.7, 0.37, 0, d); box(1.36, 0.3, 0.04, dark, 0, 0.6, -0.36, d);
  // máy tính cơ
  const calc = new THREE.Group(); calc.position.set(0.25, 0.79, 0.02); d.add(calc); const steel = std('#4a4e55', { metalness: 0.5, roughness: 0.45 });
  box(0.42, 0.13, 0.34, steel, 0, 0.065, 0, calc); const top = box(0.36, 0.02, 0.26, std('#ffffff', { map: keysTex(), roughness: 0.6 }), 0, 0.135, 0.02, calc); top.rotation.x = -0.18;
  const carriage = box(0.56, 0.07, 0.09, std('#5d6168', { metalness: 0.55, roughness: 0.4 }), 0, 0.17, -0.16, calc);
  const dial = box(0.5, 0.025, 0.02, basic('#e9dfc4'), 0, 0.19, -0.115, carriage); dial.rotation.x = -0.4;
  // giấy, thước, kính lúp, bút chì
  const gs = graphSheet(orbit); const sheet = box(0.42, 0.004, 0.31, std('#ffffff', { map: gs.tex, roughness: 0.9 }), -0.35, 0.786, 0.08, d); sheet.rotation.y = 0.12 + (R() - 0.5) * 0.1;
  const rule = box(0.5, 0.012, 0.035, std('#ffffff', { map: slideTex(), roughness: 0.5 }), -0.3, 0.792, 0.3, d); rule.rotation.y = -0.05;
  cyl(0.004, 0.004, 0.17, std('#c99a3a'), -0.08, 0.792, 0.22, d).rotation.z = Math.PI / 2;
  const lens = new THREE.Mesh(new THREE.TorusGeometry(0.04, 0.006, 8, 24), std('#22201c', { metalness: 0.4 })); lens.rotation.x = Math.PI / 2; lens.position.set(-0.52, 0.79, -0.12); d.add(lens);
  // đèn bàn chao xanh
  cyl(0.06, 0.07, 0.02, std('#2c2a26', { metalness: 0.5 }), 0.6, 0.79, -0.25, d); cyl(0.008, 0.008, 0.34, std('#2c2a26', { metalness: 0.5 }), 0.6, 0.96, -0.25, d);
  const shade = cyl(0.05, 0.13, 0.11, std('#2f5e43', { side: THREE.DoubleSide, roughness: 0.5 }), 0.55, 1.12, -0.2, d); shade.rotation.z = 0.35;
  const bulbGlow = glowSprite('#ffc985', 0.9, 0.35); bulbGlow.position.set(0.53, 1.07, -0.19); d.add(bulbGlow);
  const pool = hero ? new THREE.PointLight('#ffc27e', 0, 3.2, 1.6) : null; if (pool) { pool.position.set(0.45, 1.05, -0.12); d.add(pool); }
  if (hero) {   /* đạo cụ bàn chính: ống bút chì, xấp phiếu tính, tách cà phê, sổ ghi */
    const cup = cyl(0.035, 0.03, 0.09, std('#5a6a5a', { roughness: 0.6 }), -0.62, 0.83, -0.22, d); for (let i = 0; i < 4; i++) { const pc = cyl(0.004, 0.004, 0.16, std(i % 2 ? '#c99a3a' : '#8a5a2a'), -0.62 + (i - 1.5) * 0.012, 0.9, -0.22, d); pc.rotation.z = (i - 1.5) * 0.12; }
    for (let i = 0; i < 9; i++) { const s = box(0.3, 0.004, 0.21, std(i % 3 ? '#eae2cc' : '#e2d6b4'), 0.05 + (i % 2) * 0.006, 0.785 + i * 0.005, -0.2, d); s.rotation.y = (i % 4 - 1.5) * 0.04; }
    cyl(0.04, 0.035, 0.07, std('#e8e4da', { roughness: 0.4 }), 0.62, 0.815, 0.18, d); box(0.22, 0.012, 0.3, std('#3a4a5e'), -0.66, 0.79, 0.25, d).rotation.y = 0.3;
    const fillW = new THREE.PointLight('#ffb070', 3.5, 4, 1.5); fillW.position.set(-0.9, 1.3, 0.9); d.add(fillW); }
  // ghế + người
  box(0.44, 0.04, 0.42, dark, 0, 0.46, 0.62, d); box(0.44, 0.45, 0.04, dark, 0, 0.7, 0.84, d);
  let p = null; if (person) { p = computerWoman({ scale: 0.92 + R() * 0.05, ...(pc ? { color: pc } : {}) }); p.root.position.set(0, 0.0, 0.66); p.root.rotation.y = Math.PI; d.add(p.root); }
  const ph = R() * 6.28;
  const set = (t, f, { lamp = lampOn ? 1 : 0, plot = 0 } = {}) => {
    bulbGlow.material.opacity = 0.9 * lamp; bulbGlow.visible = lamp > 0.01; if (pool) pool.intensity = 14 * lamp * (1 + 0.02 * Math.sin(f * 0.37));   /* Q27 nháp: cận bàn quá tối */
    shade.material.emissive = new THREE.Color('#1c3a28').multiplyScalar(lamp * 0.6);
    const step = Math.floor((t * 2.2 + ph) % 8); carriage.position.x = -0.12 + step * 0.03 + 0.004 * Math.sin(t * 40 + ph);   // xe nhảy bậc khi nhân
    if (p) p.set({ armR: -1.05 + 0.1 * Math.sin(t * 7 + ph), armL: -0.95 + 0.05 * Math.sin(t * 2 + ph), headTilt: 0.35 + 0.05 * Math.sin(t * 0.7 + ph) });
    if (hero) gs.draw(plot);
  };
  return { group: d, set, sheet, calc, person: p };
}

// ===== airfield: phòng thí nghiệm bên sân bay, chạng vạng → đêm =====
async function airfield({ W, H, dur, v, opt = {} }) {
  const night = v === 'c' || v === 'd';
  const scene = new THREE.Scene(); fogOf(scene, night ? '#1a1f30' : '#2f2a3c', 0.012);
  const sky = new THREE.Mesh(new THREE.SphereGeometry(220, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, map: canvasTex(8, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h);
    if (night) { gr.addColorStop(0, '#0b1024'); gr.addColorStop(0.44, '#1f2848'); gr.addColorStop(0.5, '#3e3a58'); gr.addColorStop(0.53, '#1c1a26'); }
    else { gr.addColorStop(0, '#16203c'); gr.addColorStop(0.38, '#3d3a62'); gr.addColorStop(0.47, '#b06a4e'); gr.addColorStop(0.5, '#e09a5a'); gr.addColorStop(0.53, '#3a2a2e'); }
    gr.addColorStop(1, '#14121a'); g.fillStyle = gr; g.fillRect(0, 0, w, h); }) })); scene.add(sky);
  const R = rng(17);
  // mặt đất: bãi cỏ khô, lối đi lát đá trước toà nhà, đường nhựa bên kia
  box(160, 0.1, 160, std('#2c3026', { roughness: 1 }), 0, -0.05, 0); box(40, 0.06, 2.4, std('#5a554e', { roughness: 0.9 }), 0, 0.02, 2.6); box(160, 0.07, 7, std('#26262b', { roughness: 0.95 }), 0, 0.02, 9.5);
  for (let i = -6; i < 7; i++) box(1.6, 0.075, 0.12, basic('#8d8678'), i * 4, 0.03, 9.5);   // vạch đường
  // toà phòng thí nghiệm một tầng, dài, mái bằng có gờ; dải cửa sổ (cửa sổ giữa là phòng tính toán)
  const lab = new THREE.Group(); scene.add(lab); const wall = std('#a49a86', { roughness: 0.92 }), trim = std('#d9cfba');
  box(26, 1.4, 0.3, wall, 0, 0.7, -0.15, lab); box(26, 1.05, 0.3, wall, 0, 3.675, -0.15, lab);   // mặt tiền: dải dưới, dải trên (ô cửa thật, thấy phòng bên trong)
  for (let i = 0; i <= 9; i++) box(i === 0 || i === 9 ? 1.3 : 0.65, 1.75, 0.3, wall, -12.375 + i * 2.75 + (i === 0 ? -0.3 : i === 9 ? 0.3 : 0), 2.275, -0.15, lab);
  box(0.3, 4.2, 9, wall, -13, 2.1, -4.5, lab); box(0.3, 4.2, 9, wall, 13, 2.1, -4.5, lab); box(26, 4.2, 0.3, wall, 0, 2.1, -9, lab); box(26, 0.3, 9, wall, 0, 4.05, -4.5, lab);
  box(26.6, 0.4, 9.6, trim, 0, 4.35, -4.5, lab); box(26.2, 0.25, 0.2, trim, 0, 0.9, 0.05, lab);
  const winM = [], WIN = []; const glassLit = '#f2b56a';
  for (let i = 0; i < 9; i++) {
    const x = -11 + i * 2.75, lit = i >= 2 && i <= 6; WIN.push({ x, lit });
    const m = basic(lit ? glassLit : '#151720', { transparent: true, opacity: lit ? 0.08 : 0.92, depthWrite: false }); winM.push(m);
    box(2.1, 1.7, 0.04, m, x, 2.25, 0.02, lab); box(2.3, 0.12, 0.25, trim, x, 1.35, 0.1, lab); box(2.3, 0.1, 0.14, trim, x, 3.15, 0.06, lab);
    box(0.06, 1.7, 0.08, std('#2b2620'), x, 2.25, 0.05, lab); box(2.1, 0.05, 0.08, std('#2b2620'), x, 2.7, 0.05, lab);
  }

  // phòng tính toán sau dải cửa sổ (thấy qua kính): sàn, tường sau sáng, hàng bàn, người, đèn bàn
  const room = new THREE.Group(); room.position.set(0, 0, -0.35); scene.add(room);
  box(25, 0.05, 8.2, std('#4a3424'), 0, 0.92, -4.1, room); box(25, 3.0, 0.1, std('#cbb38a'), 0, 2.45, -8.3, room); box(25, 0.1, 8.2, std('#b9a27e'), 0, 3.85, -4.1, room);
  box(5, 1.5, 0.05, std('#ffffff', { map: chalkTex(), roughness: 0.95 }), -1, 2.5, -8.2, room);
  const roomLamps = [], desks = [];
  for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) {
    const dx = -5.4 + c * 2.1, dz = -1.4 - r * 1.9; const dk = new THREE.Group(); dk.position.set(dx, 0.92, dz); room.add(dk);
    box(1.3, 0.05, 0.65, std('#5a3a22'), 0, 0.74, 0, dk); box(0.3, 0.12, 0.24, std('#4a4e55', { metalness: 0.5 }), 0.25, 0.83, 0, dk);
    const w = computerWoman({ scale: 0.9 }); w.root.position.set(0, 0, 0.55); w.root.rotation.y = Math.PI; dk.add(w.root); desks.push(w);
    const gl = glowSprite('#ffd08e', 0.8, 0.5); gl.position.set(0.5, 1.12, -0.15); dk.add(gl); roomLamps.push(gl);
  }
  const roomLight = new THREE.PointLight('#ffc888', 0, 18, 1.2); roomLight.position.set(-2, 3.4, -3); room.add(roomLight);
  const roomLight2 = new THREE.PointLight('#ffc888', 0, 12, 1.2); roomLight2.position.set(4, 3.2, -1.5); room.add(roomLight2);
  // đèn bàn sát cửa sổ (đèn nhận lửa qua ô kính): chao xanh, quầng, đèn điểm riêng
  const handLamp = new THREE.Group(); handLamp.position.set(3.0, 0.92, -0.75); room.add(handLamp);
  box(1.3, 0.05, 0.6, std('#5a3a22'), 0, 0.74, 0, handLamp); cyl(0.008, 0.008, 0.34, std('#2c2a26'), 0.4, 0.93, 0.1, handLamp);
  const hShade = cyl(0.05, 0.13, 0.11, std('#2f5e43', { side: THREE.DoubleSide }), 0.35, 1.08, 0.12, handLamp); hShade.rotation.z = 0.35;
  const hGlow = glowSprite('#ffcf8a', 1.0, 0.55); hGlow.position.set(0.33, 1.04, 0.13); handLamp.add(hGlow);
  const hLight = new THREE.PointLight('#ffc07a', 0, 4, 1.5); hLight.position.set(0.3, 1.0, 0.2); handLamp.add(hLight);
  // nhà chứa máy bay mái vòm + ống hầm gió (bóng trên trời), cột gió
  const hangar = new THREE.Mesh(new THREE.CylinderGeometry(9, 9, 22, 32, 1, false, 0, Math.PI), std('#4b4a52', { roughness: 0.8, side: THREE.DoubleSide })); hangar.rotation.z = Math.PI / 2; hangar.rotation.y = Math.PI / 2; hangar.position.set(-24, 0, -26); scene.add(hangar);
  box(18, 8.6, 0.3, std('#3b3a42'), -24, 4.3, -15.2);
  const tunnel = new THREE.Group(); tunnel.position.set(22, 0, -34); scene.add(tunnel); const tm = std('#5a5862', { roughness: 0.7, metalness: 0.2 });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(7, 1.1, 12, 40), tm); ring.position.set(0, 8, 0); tunnel.add(ring);
  const tube = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 7, 26, 32, 1, true), tm); tube.rotation.z = Math.PI / 2; tube.position.set(-13, 8, 0); tunnel.add(tube);
  box(30, 1.2, 4, tm, -6, 0.6, 0, tunnel);
  const sock = cyl(0.04, 0.04, 6, std('#2a2a2a'), 18, 3, -10); const sockC = cyl(0.25, 0.08, 1.4, lam('#c66a34'), 18.7, 5.7, -10); sockC.rotation.z = Math.PI / 2;
  // đèn đường băng (chấm xa) và dãy đèn trên đường
  for (let i = 0; i < 26; i++) { const s = glowSprite(i % 2 ? '#9fc4ff' : '#ffd38a', 0.7, 0.35); s.position.set(-40 + i * 3.2, 0.3, -48); scene.add(s); }
  // tháp văn phòng hôm nay, bên kia đường: lưới cửa sổ, một tầng sẽ bừng sáng
  const tower = new THREE.Group(); tower.position.set(30, 0, -46); scene.add(tower);
  const twTex = canvasTex(256, 1024, (g, w, h) => { g.fillStyle = '#10141c'; g.fillRect(0, 0, w, h); for (let r = 0; r < 40; r++) for (let c = 0; c < 10; c++) { const on = R() < 0.12; g.fillStyle = on ? '#6f88a8' : '#1b2230'; g.fillRect(6 + c * 25, 6 + r * 25.4, 19, 17); } });
  box(14, 42, 14, std('#ffffff', { map: twTex, roughness: 0.6, emissive: '#ffffff', emissiveMap: twTex, emissiveIntensity: 0.55 }), 0, 21, 0, tower);
  const floorWins = []; for (let c = 0; c < 10; c++) for (const [fx, fz, ry] of [[-7.06, -6.3 + c * 1.4, -Math.PI / 2], [-6.3 + c * 1.4, 7.06, 0]]) { const w = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 0.75), basic('#ffd9a0', { transparent: true, opacity: 0 })); w.position.set(fx, 27.2, fz); w.rotation.y = ry; tower.add(w); floorWins.push(w); }
  const floorGlow = glowSprite('#ffd9a0', 0, 5); floorGlow.position.set(-7.4, 27.2, 7.4); tower.add(floorGlow);
  // cột đèn khí: cạnh cửa sổ phòng tính toán; cột cuối (kết) ở đầu lối đi
  const lampA = gasLamp(scene, 4.6, 1.75, { lit: v === 'a' ? 1 : 0 }), lampB = gasLamp(scene, -9.5, 1.75, { lit: v === 'c' ? 1 : 0 });
  const lighter = figure({ hat: true, scale: 1.0 }); scene.add(lighter.root);
  const pole = cyl(0.015, 0.015, 3.0, lam('#2a2016'), 0, 0.1, 0); lighter.armR.add(pole); pole.rotation.x = -0.25;   /* sào 3 m; góc tổng (tay + sào) dương → đầu sào nghiêng về phía trước (+x thế giới) */
  const wick = glowSprite('#ffb86a', 0.95, 0.42); wick.position.set(0, 1.52, 0); pole.add(wick);
  const wickLight = new THREE.PointLight('#ffae62', 2.6, 3.4, 1.6); wickLight.position.set(0, 1.45, 0.1); pole.add(wickLight);
  const hemi = new THREE.HemisphereLight(night ? '#56609a' : '#7a6a8a', '#1a1418', night ? 1.0 : 0.95); scene.add(hemi);
  const sun = new THREE.DirectionalLight(night ? '#7f8fd0' : '#ffb07a', night ? 0.4 : 0.9); sun.position.set(-30, 10, -40); scene.add(sun);
  const fill = new THREE.PointLight('#ffb070', 2.5, 20, 1.2); fill.position.set(2, 4, 8); scene.add(fill);
  const spillTex = canvasTex(128, 128, (g, w, h) => { const gr = g.createRadialGradient(64, 40, 4, 64, 56, 64); gr.addColorStop(0, '#ffffff'); gr.addColorStop(1, '#000000'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  if (v === 'a') WIN.forEach(({ x, lit }) => { if (!lit) return; const m = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 3.6), basic('#ffb468', { map: spillTex, transparent: true, opacity: 0.32, depthWrite: false, blending: THREE.AdditiveBlending })); m.rotation.x = -Math.PI / 2; m.position.set(x, 0.07, 2.0); scene.add(m); });   /* vệt sáng cửa sổ hắt xuống lối đi */
  const dst = dust(scene, [4.6, 3.0, 1.75], [2.4, 2.0, 2.2], 160, 13);
  const K = {
    a: [{ t: 0, p: [-2.6, 1.35, 12.8], l: [1, 2.5, -2], mm: 30 },   /* Q27 nháp lượt 2: mặt đường tối chiếm nửa khung → máy gần, thấp hơn */ { t: dur, p: [1.4, 2.35, 3.2], l: [1.2, 1.7, -4.0], mm: 36 }],
    b: [{ t: 0, p: [-6.5, 1.6, 9.5], l: [-2, 2.2, 1], mm: 30 }, { t: Math.max(1, (opt.lit || 6) - 1.5), p: [0.2, 1.75, 7.6], l: [3.6, 2.4, 0.4], mm: 34 }, { t: dur, p: [1.9, 2.0, 5.2], l: [3.2, 1.9, -1.2], mm: 44 }],
    c: [{ t: 0, p: [1.5, 2.0, 7.5], l: [3, 2.2, -1], mm: 36 }, { t: (opt.tower || 5) - 0.6, p: [0.5, 1.9, 10.5], l: [12, 6.5, -20], mm: 30 }, { t: dur, p: [0, 1.8, 11.5], l: [20, 11.5, -36], mm: 34 }],
    d: [{ t: 0, p: [-5.2, 1.7, 9.2], l: [-9.6, 2.2, 1.8], mm: 32 }, { t: (opt.lit || 7) + 0.6, p: [-6.6, 2.0, 7.6], l: [-9.6, 2.8, 1.7], mm: 36 }, { t: dur, p: [-6, 9, 24], l: [6, 5, -14], mm: 28 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    let lit = 1, dark = 0, hand = v === 'a' ? 1 : 0, tw = 0;
    if (v === 'b') {   // opt.lit: giây ngọn đèn bén; opt.hand: giây đèn bàn sau kính bừng
      const tl = opt.lit !== undefined ? opt.lit : dur * 0.45, ta = tl - 1.0, u = Math.min(1, t / ta);
      lighter.root.position.set(lerp(-7.5, 4.0, ease(u)), 0.06, 2.3); lighter.root.rotation.y = Math.PI / 2; const rz = u < 1 ? 0 : ease((t - ta) / 1.2); lighter.set({ walk: u < 1 ? t * 5 : 0, armR: lerp(0.2, opt.armUp !== undefined ? opt.armUp : 0.15, rz) }); pole.rotation.x = lerp(-0.25, opt.tilt !== undefined ? opt.tilt : 0.2, rz);   /* giơ sào: nghiêng đầu sào (ngọn lửa mồi) về lồng đèn, không lật sào (lỗi nháp lượt 1) */
      lampA.set(ease((t - tl) / 1.0), f); hand = ease((t - (opt.hand !== undefined ? opt.hand : tl + 1.2)) / 1.2);
    } else if (v === 'd') {
      const tl = opt.lit !== undefined ? opt.lit : dur * 0.4, ta = tl - 1.0, u = Math.min(1, t / ta);
      lighter.root.position.set(lerp(-17, -10.05, ease(u)), 0.06, 2.3); lighter.root.rotation.y = Math.PI / 2; const rz = u < 1 ? 0 : ease((t - ta) / 1.2); lighter.set({ walk: u < 1 ? t * 5 : 0, armR: lerp(0.2, opt.armUp !== undefined ? opt.armUp : 0.15, rz) }); pole.rotation.x = lerp(-0.25, opt.tilt !== undefined ? opt.tilt : 0.2, rz);   /* giơ sào: nghiêng đầu sào (ngọn lửa mồi) về lồng đèn, không lật sào (lỗi nháp lượt 1) */
      lampB.set(ease((t - tl) / 1.0), f); lampA.set(1, f); hand = 1; tw = 1;
    } else if (v === 'c') {   // opt.dark: giây cửa sổ phòng tính toán tắt; opt.tower: giây một tầng tháp bừng sáng
      lighter.root.position.set(lerp(6, 14, ease(t / dur)), 0.06, 3.2); lighter.root.rotation.y = Math.PI / 2; lighter.set({ walk: t * 5 });
      lampA.set(1, f); lampB.set(1, f); dark = ease((t - (opt.dark !== undefined ? opt.dark : 2)) / 1.5); hand = 1 - dark; tw = ease((t - (opt.tower !== undefined ? opt.tower : 5)) / 1.2);
    } else { lighter.root.position.set(6.2, 0.06, 2.8); lighter.root.rotation.y = -0.4; lighter.set({ armR: -0.3 }); lampA.set(1, f); }
    lit = 1 - dark;
    WIN.forEach((w, i) => { if (w.lit) { winM[i].color.set(new THREE.Color('#151720').lerp(new THREE.Color(glassLit), lit)); winM[i].opacity = lerp(0.92, 0.08, lit); } });
    roomLamps.forEach((g, i) => { g.material.opacity = 0.8 * lit * (1 + 0.03 * Math.sin(f * 0.3 + i)); });
    roomLight.intensity = 22 * lit; roomLight2.intensity = 12 * lit;
    hGlow.material.opacity = hand; hLight.intensity = 5 * hand;
    desks.forEach((w, i) => w.set({ armR: -1.05 + 0.1 * Math.sin(t * 6 + i * 1.3), armL: -0.95, headTilt: 0.35 }));
    floorWins.forEach((w, i) => { w.material.opacity = 0.95 * ease(tw * 1.4 - (i % 10) * 0.04); }); floorGlow.material.opacity = 0.8 * tw;
  };
  return { scene, cam: rig.cam, update, grade: night ? 'cold' : 'warm' };
}

// ===== pool: phòng tính toán 1940s =====
async function pool({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#2a2219', 0.03);
  scene.add(new THREE.HemisphereLight('#a89070', '#1a140f', 0.95));
  const floorTex = canvasTex(512, 512, (g, w, h) => { g.fillStyle = '#5b4a3a'; g.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { g.fillStyle = (i + j) % 2 ? '#4f3f31' : '#625040'; g.fillRect(i * 64, j * 64, 64, 64); } });
  floorTex.wrapS = floorTex.wrapT = THREE.RepeatWrapping; floorTex.repeat.set(8, 8);
  const RW = v === 'c' ? 34 : 20;
  box(RW, 0.1, 40, std('#ffffff', { map: floorTex, roughness: 0.85 }), 0, 0, -6); box(RW, 4.4, 0.3, std('#c8b48e'), 0, 2.2, -14);
  box(0.3, 4.4, 40, std('#bfa985'), -RW / 2, 2.2, -6); box(0.3, 4.4, 40, std('#bfa985'), RW / 2, 2.2, -6); if (v !== 'c' && v !== 'd') box(RW, 0.2, 40, std('#d8c8a6'), 0, 4.4, -6);
  // cửa sổ cao bên trái (ánh trời chạng vạng), rèm cuốn
  for (let i = 0; i < 6; i++) { const z = 2 - i * 3; box(0.05, 2.0, 1.4, basic('#9fb6d6'), -RW / 2 + 0.17, 2.5, z); box(0.06, 0.4, 1.5, std('#d9cba8'), -RW / 2 + 0.2, 3.4, z); }
  const sky = new THREE.DirectionalLight('#9fb4dc', 0.7); sky.position.set(-12, 6, 2); sky.castShadow = true; sky.shadow.mapSize.set(2048, 2048); Object.assign(sky.shadow.camera, { left: -18, right: 18, top: 12, bottom: -12 }); scene.add(sky);
  // ốp gỗ chân tường, bảng biểu treo tường, lò sưởi dưới cửa sổ (Q27 lần 4: tường trống, phẳng)
  const wain = std('#5a3c24', { roughness: 0.6 }); box(0.06, 1.1, 40, wain, -RW / 2 + 0.17, 0.55, -6); box(0.06, 1.1, 40, wain, RW / 2 - 0.17, 0.55, -6); box(RW, 1.1, 0.06, wain, 0, 0.55, -13.83);
  box(0.08, 0.06, 40, std('#3a2614'), -RW / 2 + 0.2, 1.12, -6); box(0.08, 0.06, 40, std('#3a2614'), RW / 2 - 0.2, 1.12, -6);
  const chartTex = (k) => canvasTex(256, 192, (g, w, h) => { g.fillStyle = '#efe6cf'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(70,120,100,0.45)'; for (let i = 0; i < w; i += 16) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); } for (let j = 0; j < h; j += 16) { g.beginPath(); g.moveTo(0, j); g.lineTo(w, j); g.stroke(); }
    g.strokeStyle = '#2a2a3a'; g.lineWidth = 3; g.beginPath(); for (let x = 10; x < w - 10; x += 4) { const y = h * 0.8 - (h * 0.6) * (k % 2 ? Math.sin(x / w * 3.1) : 1 - Math.exp(-x / (60 + k * 20))); x > 10 ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); g.fillStyle = '#2a2a3a'; g.font = 'bold 14px DejaVu Serif'; g.fillText(['LIFT', 'DRAG', 'PRESSURE', 'MOMENT'][k % 4], 12, 20); });
  for (let i = 0; i < 5; i++) { const z = 0.5 - i * 3.0; box(0.03, 0.9, 1.2, std('#ffffff', { map: chartTex(i), roughness: 0.9 }), RW / 2 - 0.18, 2.2, z); box(0.05, 0.98, 1.28, std('#3a2614'), RW / 2 - 0.16, 2.2, z); }
  for (let i = 0; i < 6; i++) { const z = 2 - i * 3; box(0.25, 0.6, 1.2, std('#8a8478', { metalness: 0.4, roughness: 0.5 }), -RW / 2 + 0.35, 0.6, z); }
  const patchTex = canvasTex(128, 128, (g, w, h) => { const gr = g.createRadialGradient(64, 64, 6, 64, 64, 62); gr.addColorStop(0, '#ffffff'); gr.addColorStop(1, '#000000'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const shaftM = basic('#fff0cc', { transparent: true, opacity: 0.07, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
  for (let i = 0; i < 6; i++) { const z = 2 - i * 3, sh = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 5.5), shaftM); sh.position.set(-RW / 2 + 2.4, 1.6, z); sh.rotation.set(0, Math.PI / 2, -0.85); scene.add(sh);
    const pt = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 2.6), basic('#ffe6b0', { map: patchTex, transparent: true, opacity: 0.16, depthWrite: false, blending: THREE.AdditiveBlending })); pt.rotation.x = -Math.PI / 2; pt.position.set(-RW / 2 + 3.6, 0.06, z); scene.add(pt); }
  // bảng đen cuối phòng, đồng hồ treo tường
  box(5.2, 1.9, 0.06, std('#ffffff', { map: chalkTex(), roughness: 0.95 }), 0, 2.3, -13.8); box(5.4, 0.08, 0.15, std('#6b4a2a'), 0, 1.33, -13.75);
  const clock = new THREE.Group(); clock.position.set(4.6, 3.3, -13.82); scene.add(clock);
  const face = new THREE.Mesh(new THREE.CircleGeometry(0.32, 32), basic('#efe6cf')); clock.add(face); const rimC = new THREE.Mesh(new THREE.TorusGeometry(0.33, 0.03, 8, 32), std('#3a2a1a')); clock.add(rimC);
  const hourH = box(0.02, 0.16, 0.01, basic('#1a1a1a'), 0, 0.07, 0.01, clock), minH = box(0.014, 0.25, 0.01, basic('#1a1a1a'), 0, 0.11, 0.02, clock);
  // đèn treo trần (quầng) + đèn điểm
  const pend = []; for (let i = 0; i < 4; i++) for (let j = 0; j < 2; j++) { const x = -4 + j * 8, z = 1 - i * 4; cyl(0.004, 0.004, 0.8, lam('#111'), x, 4.0, z); cyl(0.06, 0.3, 0.2, std('#e8e0c8', { side: THREE.DoubleSide }), x, 3.55, z);
    const s = glowSprite('#ffe2b0', 0.7, 0.9); s.position.set(x, 3.45, z); scene.add(s); pend.push(s); }
  const ceil1 = new THREE.PointLight('#ffd8a0', 26, 22, 1.2); ceil1.position.set(-2, 3.4, -2); scene.add(ceil1);
  const ceil2 = new THREE.PointLight('#ffd8a0', 20, 20, 1.2); ceil2.position.set(3, 3.4, -8); scene.add(ceil2);
  // hàng bàn
  const desks = [];
  const rows = v === 'c' ? 7 : 4, cols = v === 'c' ? 9 : 5;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const x = (c - (cols - 1) / 2) * 2.3, z = 0.5 - r * 2.2; if (v === 'd' && Math.abs(x) < 0.6) continue;
    const k = r * cols + c; desks.push({ k, d: computeDesk(scene, x, z, { seed: 100 + k }), x, z });
  }
  desks.slice(0, 6).forEach(({ x, z }) => { const dl = new THREE.PointLight('#ffc27e', 2.2, 2.6, 1.6); dl.position.set(x + 0.5, 1.15, z - 0.15); scene.add(dl); });   /* quầng đèn bàn hàng đầu */
  // bàn chính (cận): đặt ở hàng đầu, giữa — thêm máy đọc phim áp kế, chồng giấy
  const heroD = computeDesk(scene, 0.9, 4.2, { hero: true, orbit: !!opt.orbit, seed: 7 });
  const reader = new THREE.Group(); reader.position.set(1.85, 0.79, 4.0); scene.add(reader);
  box(0.36, 0.42, 0.3, std('#3a3d42', { metalness: 0.4 }), 0, 0.21, 0, reader);
  const film = canvasTex(256, 200, (g, w, h) => { g.fillStyle = '#d9e4d0'; g.fillRect(0, 0, w, h); const R = rng(5); for (let i = 0; i < 22; i++) { const hh = 40 + R() * 120; g.fillStyle = '#26302a'; g.fillRect(10 + i * 11, h - 10 - hh, 5, hh); } g.strokeStyle = '#26302a'; g.strokeRect(4, 4, w - 8, h - 8); });
  const scr = box(0.28, 0.22, 0.01, basic('#ffffff', { map: film }), 0, 0.27, 0.155, reader); const readerGlow = glowSprite('#e9f3d8', 0.35, 0.5); readerGlow.position.set(0, 0.28, 0.2); reader.add(readerGlow);
  const sheets = []; for (let i = 0; i < 24; i++) { const s = box(0.4, 0.006, 0.3, std('#efe7d2'), 0.25, 0.79 + i * 0.007, 4.45, null); s.position.set(0.15 + (i % 3) * 0.004, 0.79 + i * 0.007, 4.5); s.rotation.y = (i % 5 - 2) * 0.02; s.visible = false; sheets.push(s); }
  // vách ngăn hai phòng (d): tường giữa có khung cửa, hai phòng giống nhau
  if (v === 'd') { box(0.25, 4.4, 30, std('#a8977a'), 0, 2.2, -6); }
  // khung cửa hẹp từ hành lang tối (e)
  if (v === 'e') { const cm = std('#2a2018'); box(4.2, 4.4, 0.3, std('#3a2f25'), -2.9, 2.2, 8); box(4.2, 4.4, 0.3, std('#3a2f25'), 2.9, 2.2, 8); box(1.6, 1.9, 0.3, std('#3a2f25'), 0, 3.45, 8);
    box(0.1, 2.5, 0.35, cm, -0.8, 1.25, 8); box(0.1, 2.5, 0.35, cm, 0.8, 1.25, 8); box(1.7, 0.1, 0.35, cm, 0, 2.5, 8);
    const door = box(0.08, 2.4, 0.95, std('#4a3524'), -0.82, 1.2, 8.55); door.rotation.y = 0.6; box(6, 0.1, 6, std('#2a231c'), 0, 0.01, 11); const wash = new THREE.PointLight('#c89a68', 10, 8, 1.3); wash.position.set(-1.6, 2.6, 11.5); scene.add(wash); const wash2 = new THREE.PointLight('#8a7a9a', 6, 7, 1.3); wash2.position.set(1.8, 2.2, 12.5); scene.add(wash2); }
  const dst = dust(scene, [0.9, 1.6, 3.6], [3, 1.6, 2], 200, 31);
  const K = {
    a: [{ t: 0, p: [-6.5, 1.75, 6.5], l: [-2.2, 1.0, -0.2], mm: 30 }, { t: dur, p: [4.8, 1.85, 5.8], l: [1.6, 0.95, -1.2], mm: 32 }],
    b: [{ t: 0, p: [-0.15, 1.42, 3.35], l: [0.65, 0.8, 4.3], mm: 36 }, { t: dur, p: [0.15, 1.3, 3.55], l: [0.6, 0.79, 4.3], mm: 46 }],
    c: [{ t: 0, p: [0, 2.2, 7.5], l: [0, 0.9, -1], mm: 30 }, { t: dur, p: [0, 8.5, 8.5], l: [0, 0, -5], mm: 28 }],
    d: [{ t: 0, p: [-3.5, 6.5, 7.5], l: [0, 0.4, -3], mm: 28 }, { t: dur, p: [3.5, 6.2, 6.8], l: [0, 0.4, -5], mm: 30 }],
    e: [{ t: 0, p: [0.1, 1.6, 13.5], l: [0, 1.4, 4], mm: 30 }, { t: dur, p: [0.05, 1.6, 9.6], l: [0.3, 1.2, 2], mm: 32 }],
  }[v];
  const rig = camRig(W, H, K);
  const N = opt.n;
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const growN = opt.grow ? Math.floor(lerp(5, desks.length, ease((t - (opt.grow0 || 0)) / Math.max(1, dur - (opt.grow0 || 0) - 1)))) : desks.length;
    const emptyN = opt.empty ? Math.floor((desks.length - 3) * ease((t - (opt.empty0 || 0)) / Math.max(1, dur - (opt.empty0 || 0) - 1))) : 0;
    desks.forEach(({ d }, i) => { const occ = (N === undefined || i < N) && i < growN; d.group.visible = (N === undefined || i < N) && (v !== 'c' || i < growN || !opt.grow);
      const lampU = opt.empty ? (i < desks.length - emptyN ? 1 : 0) : (occ ? 1 : 0); if (d.person) d.person.root.visible = occ && lampU > 0; d.set(t, f, { lamp: lampU }); });
    heroD.set(t, f, { lamp: 1, plot: ease((t - (opt.plot !== undefined ? opt.plot : 0.5)) / (opt.plotDur || dur * 0.7)) });
    if (opt.stack) { const n = Math.floor(sheets.length * ease((t - (opt.stack0 || 0)) / Math.max(1, dur - (opt.stack0 || 0)))); sheets.forEach((s, i) => { s.visible = i < n; }); }
    pend.forEach((s, i) => { s.material.opacity = 0.7 * (1 + 0.03 * Math.sin(f * 0.21 + i)); });
    const sec = t + 37 * 60; minH.rotation.z = -sec / 3600 * Math.PI * 2 * 12; hourH.rotation.z = -sec / 3600 * Math.PI * 2;
    readerGlow.material.opacity = 0.35 * (1 + 0.05 * Math.sin(f * 0.5));
  };
  return { scene, cam: rig.cam, update, grade: 'sepia', exposure: 1.25 };
}

// ===== relay: phòng máy rơ-le 1947, băng đục lỗ =====
async function relay({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#221d18', 0.04);
  scene.add(new THREE.HemisphereLight('#9a8a74', '#14100c', 0.85));
  const tile = canvasTex(256, 256, (g, w, h) => { const R = rng(12); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const k = 0.85 + R() * 0.2; g.fillStyle = `rgb(${Math.round(70 * k)},${Math.round(64 * k)},${Math.round(56 * k)})`; g.fillRect(i * 64, j * 64, 64, 64); } g.strokeStyle = 'rgba(20,16,12,0.6)'; g.lineWidth = 2; for (let i = 0; i <= 4; i++) { g.beginPath(); g.moveTo(i * 64, 0); g.lineTo(i * 64, h); g.stroke(); g.beginPath(); g.moveTo(0, i * 64); g.lineTo(w, i * 64); g.stroke(); } });
  tile.wrapS = tile.wrapT = THREE.RepeatWrapping; tile.repeat.set(8, 15);   /* sàn ô vinyl: bề mặt có chi tiết, bắt sáng (Q27 lần 4) */
  box(16, 0.1, 30, std('#ffffff', { map: tile, roughness: 0.45 }), 0, 0, -5); box(16, 3.8, 0.3, std('#b8a98c'), 0, 1.9, -16); box(16, 0.2, 30, std('#cfc3a8'), 0, 3.8, -5);
  const rackTex = canvasTex(256, 512, (g, w, h) => { g.fillStyle = '#7a7c78'; g.fillRect(0, 0, w, h); const R = rng(3);
    for (let r = 0; r < 26; r++) for (let c = 0; c < 8; c++) { g.fillStyle = R() < 0.5 ? '#2c2e30' : '#3b3d40'; g.fillRect(10 + c * 30, 12 + r * 19, 24, 14); g.fillStyle = '#a8742c'; g.fillRect(14 + c * 30, 15 + r * 19, 4, 8); }
    g.fillStyle = '#5c5e5a'; g.fillRect(0, 0, w, 8); g.fillRect(0, h - 8, w, 8); });
  const lampsPos = [], lampsCol = [], racks = [];
  for (const side of [-1, 1]) for (let i = 0; i < 9; i++) {
    const x = side * 1.45, z = 2 - i * 1.25; const rk = box(0.5, 2.6, 1.1, std('#ffffff', { map: rackTex, roughness: 0.6 }), x, 1.3, z); rk.rotation.y = 0; racks.push(rk);
    box(0.55, 0.12, 1.15, std('#55574f'), x, 2.66, z);
    for (let k = 0; k < 12; k++) { lampsPos.push(x - side * 0.27, 0.6 + (k % 6) * 0.32, z - 0.35 + Math.floor(k / 6) * 0.7); lampsCol.push(0.2, 0.15, 0.05); }
  }
  const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(lampsPos, 3)); const colA = new THREE.Float32BufferAttribute(lampsCol, 3); lg.setAttribute('color', colA);
  scene.add(new THREE.Points(lg, new THREE.PointsMaterial({ size: 0.08, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })));
  // bàn đọc băng ở cuối hành lang: đầu đọc, cuộn băng, băng chạy (kết cấu lỗ đục dịch theo thời gian)
  const desk = new THREE.Group(); desk.position.set(0, 0, -9.6); scene.add(desk); const steel = std('#7d8078', { metalness: 0.35, roughness: 0.5 });
  box(2.4, 0.9, 0.9, steel, 0, 0.45, 0, desk); box(2.5, 0.05, 1.0, std('#5e605a'), 0, 0.92, 0, desk);
  const panelTex = canvasTex(512, 240, (g, w, h) => { g.fillStyle = '#7c7f78'; g.fillRect(0, 0, w, h); g.fillStyle = '#5c5f58'; for (let x = 12; x < w; x += 40) for (const y of [10, h - 10]) { g.beginPath(); g.arc(x, y, 3, 0, 7); g.fill(); }
    g.strokeStyle = '#4a4c47'; g.lineWidth = 3; g.strokeRect(20, 24, w - 40, h - 48); g.fillStyle = '#2c2e2a'; g.font = 'bold 18px DejaVu Sans'; g.fillText('TAPE  READER', 34, 52); g.fillText('ROUTINE', w - 130, 52);
    for (let i = 0; i < 6; i++) { g.fillStyle = i % 2 ? '#d8a040' : '#3a6a4a'; g.beginPath(); g.arc(60 + i * 26, h - 40, 7, 0, 7); g.fill(); } });
  box(2.2, 1.0, 0.08, std('#ffffff', { map: panelTex, metalness: 0.3, roughness: 0.55 }), 0, 1.45, -0.42, desk);   // bảng đứng giữ cuộn băng
  const head = box(0.34, 0.16, 0.26, std('#2e3033', { metalness: 0.5 }), 0.3, 1.0, 0.05, desk); box(0.36, 0.03, 0.06, std('#b08a3a', { metalness: 0.6 }), 0.3, 1.09, 0.05, desk);
  const tl = new THREE.PointLight('#ffe0a8', 2.2, 1.6, 1.6); tl.position.set(0.3, 1.25, 0.35); desk.add(tl);
  const tapeTex = canvasTex(64, 1024, (g, w, h) => { g.fillStyle = '#e8dcb8'; g.fillRect(0, 0, w, h); const R = rng(9); g.fillStyle = '#2a2520';
    for (let y = 6; y < h; y += 12) { for (let c = 0; c < 5; c++) if (R() < 0.45) { g.beginPath(); g.arc(8 + c * 10 + (c > 2 ? 6 : 0), y, 3.2, 0, 7); g.fill(); } g.beginPath(); g.arc(37, y, 1.5, 0, 7); g.fill(); } });
  tapeTex.wrapS = tapeTex.wrapT = THREE.RepeatWrapping; tapeTex.repeat.set(1, 3);
  const tapeM = std('#ffffff', { map: tapeTex, roughness: 0.9, side: THREE.DoubleSide });
  const strip = (x0, y0, x1, y1) => { const L = Math.hypot(x1 - x0, y1 - y0), m = new THREE.Mesh(new THREE.PlaneGeometry(0.05, L), tapeM); m.position.set((x0 + x1) / 2, (y0 + y1) / 2, -0.3); m.rotation.z = Math.atan2(x0 - x1, y1 - y0); desk.add(m); return m; };
  strip(-0.45, 1.35, 0.17, 1.07); strip(0.43, 1.07, 1.05, 1.35); const tape1 = strip(-0.12, 1.07, 0.72, 1.07); tape1.rotation.z = Math.PI / 2; tape1.position.y = 1.075; tape1.position.z = 0.05;
  const reels = []; for (const [x, y, z] of [[-0.45, 1.55, -0.34], [1.05, 1.55, -0.34]]) { const reel = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.03, 40), std('#9a9c96', { metalness: 0.6, roughness: 0.35 })); const pack = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.035, 32), std('#e3d6b0')); reel.add(pack); reel.rotation.x = Math.PI / 2; reel.position.set(x, y, z); desk.add(reel); reels.push(reel); for (let s = 0; s < 3; s++) { const sp = box(0.4, 0.02, 0.03, std('#5a5c58', { metalness: 0.6 }), 0, 0.03, 0, reel); sp.rotation.y = s * Math.PI / 3; } }
  const op = figure({ scale: 0.98, color: '#1c1714' }); const bun = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 10), lam('#1c1714')); bun.position.set(0, 1.6, -0.1); op.root.add(bun);
  op.root.position.set(-1.05, 0, 0.85); op.root.rotation.y = Math.PI + 0.55; desk.add(op.root);
  const deskLamp = new THREE.PointLight('#ffd49a', 11, 4.5, 1.5); const key = new THREE.SpotLight('#ffd9a8', 30, 9, 0.55, 0.6, 1.3); key.position.set(-2.2, 3.2, 1.8); key.target.position.set(0.3, 1.2, -0.3); desk.add(key, key.target); deskLamp.position.set(0.2, 1.9, 0.6); desk.add(deskLamp);
  const pend = []; for (let i = 0; i < 4; i++) { const s = glowSprite('#ffe6b8', 0.65, 0.8); s.position.set(0, 3.4, 1.5 - i * 3.2); scene.add(s); pend.push(s); const pl = new THREE.PointLight('#ffdcae', 6, 7, 1.4); pl.position.set(0, 3.3, 1.5 - i * 3.2); scene.add(pl); }
  box(2.6, 1.3, 0.05, basic('#e6d4a8'), 0, 2.1, -15.82); box(2.8, 0.1, 0.1, std('#3a3428'), 0, 2.8, -15.78); box(0.08, 1.3, 0.1, std('#3a3428'), 0, 2.1, -15.78);   /* ô kính mờ có đèn sau ở tường cuối: nền không đen đặc (Q27 nháp lượt 2) */
  const backW = new THREE.PointLight('#ffd6a0', 9, 9, 1.3); backW.position.set(0, 2.6, -14.2); scene.add(backW);
  const dst = dust(scene, [0, 1.8, -3], [2.4, 2.4, 12], 260, 47);
  const K = {
    a: [{ t: 0, p: [0.2, 1.65, 5.2], l: [0, 1.4, -4], mm: 28 }, { t: dur, p: [-0.15, 1.6, -4.6], l: [0.25, 1.1, -9.6], mm: 34 }],
    b: [{ t: 0, p: [0.75, 1.55, -7.0], l: [0.3, 1.2, -9.95], mm: 28 }, { t: dur, p: [0.55, 1.45, -7.8], l: [0.3, 1.2, -9.95], mm: 33 }],
  }[v];
  const rig = camRig(W, H, K);
  const R = rng(71), ph = lampsPos.map(() => R() * 50), rate = lampsPos.map(() => 0.6 + R() * 2.4);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    for (let i = 0; i < colA.count; i++) { const on = Math.sin(t * rate[i] * 3 + ph[i]) > 0.35 ? 1 : 0.12; colA.setXYZ(i, 1.0 * on, 0.62 * on, 0.25 * on); } colA.needsUpdate = true;
    tapeTex.offset.y = -t * 0.35; reels.forEach((r, i) => { r.rotation.y = t * (i ? 1.6 : -1.6); });
    op.set({ armR: -0.9 + 0.08 * Math.sin(t * 1.3), armL: -1.2, headTilt: 0.3 });
    pend.forEach((s, i) => { s.material.opacity = 0.65 * (1 + 0.03 * Math.sin(f * 0.19 + i)); });
  };
  return { scene, cam: rig.cam, update, grade: 'sepia' };
}

// ===== tower: văn phòng tầng cao hôm nay, đêm =====
async function tower({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#0a0f18', 0.03);
  scene.add(new THREE.HemisphereLight('#4a5e88', '#0a0d14', 0.95)); const ceilL = new THREE.PointLight('#a8c0e8', 13, 18, 1.2); ceilL.position.set(-2, 3.0, 1); scene.add(ceilL);
  const carpet = canvasTex(256, 256, (g, w, h) => { const R = rng(31); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const k = 0.85 + R() * 0.25; g.fillStyle = `rgb(${Math.round(42 * k)},${Math.round(48 * k)},${Math.round(60 * k)})`; g.fillRect(i * 64, j * 64, 64, 64); for (let n = 0; n < 40; n++) { g.fillStyle = `rgba(${R() < 0.5 ? '90,100,120' : '20,24,32'},0.35)`; g.fillRect(i * 64 + R() * 64, j * 64 + R() * 64, 2, 2); } } });
  carpet.wrapS = carpet.wrapT = THREE.RepeatWrapping; carpet.repeat.set(15, 12);   /* thảm ô văn phòng (Q27 lần 4: sàn phẳng) */
  box(30, 0.1, 24, std(v === 'c' ? '#d8e0f0' : '#a8b0c0', { map: carpet, roughness: 0.85 }), 0, 0, -4); box(30, 0.2, 24, std('#20242c'), 0, 3.2, -4);
  for (let i = 0; i < 6; i++) { const s = box(2.2, 0.04, 0.3, basic('#cfe0ff', { transparent: true, opacity: 0.45 }), -7 + i * 3, 3.08, -2); } const amb2 = new THREE.PointLight('#9ab4e0', 8, 14, 1.3); amb2.position.set(4, 3.0, -5); scene.add(amb2);
  // phố đêm ngoài kính (mặt phẳng nền: cửa sổ toà khác, quầng mờ)
  const city = canvasTex(1024, 512, (g, w, h) => { const R = rng(23); const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#060a14'); gr.addColorStop(0.7, '#141c30'); gr.addColorStop(1, '#2a2a3a'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let b = 0; b < 26; b++) { const x = R() * w, bw = 30 + R() * 70, bh = 120 + R() * 360; g.fillStyle = '#0c111c'; g.fillRect(x, h - bh, bw, bh);
      for (let yy = h - bh + 8; yy < h - 6; yy += 10) for (let xx = x + 4; xx < x + bw - 4; xx += 8) if (R() < 0.22) { g.fillStyle = R() < 0.7 ? '#e9c88a' : '#9cc0ff'; g.fillRect(xx, yy, 4, 5); } } });
  box(40, 16, 0.1, basic('#ffffff', { map: city }), 0, 4, -20);
  // tường kính: thanh đứng (mặt dựng), phía +z là ngoài toà (biến thể a đi xuyên vào)
  const mull = std('#2a2f38', { metalness: 0.5, roughness: 0.4 });
  for (let i = 0; i < 11; i++) box(0.08, 3.2, 0.12, mull, -10 + i * 2, 1.6, 6); box(22, 0.14, 0.14, mull, 0, 3.14, 6); box(22, 0.14, 0.14, mull, 0, 0.1, 6); box(22, 0.1, 0.12, mull, 0, 1.1, 6);
  box(22, 0.6, 0.3, std('#1a1d24'), 0, 3.5, 6); box(22, 3.0, 0.3, std('#161920'), 0, -1.5, 6);
  // bàn làm việc: hàng bàn trắng, màn hình (phần lớn tắt)
  const deskM = std('#d8d6d0', { roughness: 0.5 }), legM = std('#3a3d44', { metalness: 0.5 });
  const mkDesk = (x, z, on, lampOn) => { const g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g); box(1.6, 0.04, 0.8, deskM, 0, 0.74, 0, g); box(0.04, 0.72, 0.7, legM, -0.75, 0.36, 0, g); box(0.04, 0.72, 0.7, legM, 0.75, 0.36, 0, g);
    const mon = box(0.62, 0.38, 0.03, basic(on ? '#5f7fae' : '#0d1118'), 0, 1.06, -0.22, g); box(0.04, 0.2, 0.04, legM, 0, 0.84, -0.24, g);
    box(0.44, 0.02, 0.14, std('#2a2d33'), 0, 0.77, 0.12, g);   // bàn phím
    cyl(0.006, 0.006, 0.4, std('#3a3226', { metalness: 0.5 }), 0.62, 0.95, -0.2, g); const sh = cyl(0.04, 0.12, 0.12, std('#8a6a3a', { metalness: 0.4, side: THREE.DoubleSide }), 0.56, 1.14, -0.14, g); sh.rotation.z = 0.4;
    const lg = glowSprite('#ffc27a', lampOn ? 0.9 : 0, 0.4); lg.position.set(0.53, 1.08, -0.12); g.add(lg);
    box(0.5, 0.05, 0.48, std('#2c3038'), 0, 0.5, 0.62, g); box(0.5, 0.5, 0.05, std('#2c3038'), 0, 0.8, 0.86, g);
    const rr = Math.abs(Math.sin(x * 3.1 + z * 1.7)); box(0.3, 0.012, 0.22, std('#e8e6df'), -0.5, 0.766, 0.1 + rr * 0.1, g).rotation.y = rr - 0.5; if (rr > 0.4) cyl(0.035, 0.03, 0.09, std(rr > 0.7 ? '#b85a3a' : '#3a6a8a', { roughness: 0.5 }), -0.62, 0.81, -0.15, g);   /* giấy, cốc trên bàn */
    return { g, mon, lg }; };
  const empties = [];
  for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) { const x = -6 + c * 3, z = -1.5 - r * 2.4; if (r === 0 && c === 2) continue; const late = (r === 1 && c === 0) || (r === 2 && c === 3) || (r === 1 && c === 4);
    const dk = mkDesk(x, z, late || (r * 5 + c) % 7 === 3, late); empties.push(dk);
    if (late) { const w = figure({ seated: true, scale: 1.0, color: '#0e1014' }); w.root.position.set(0, 0, 0.72); w.root.rotation.y = Math.PI; dk.g.add(w.root); const ll = new THREE.PointLight('#ffc48a', 1.6, 2.4, 1.6); ll.position.set(0.45, 1.05, 0); dk.g.add(ll); } }   /* người làm muộn: sàn không chết (Q27 nháp) */
  // bàn đang làm: hai màn hình mã, đèn bàn ấm, người (bóng) có ánh viền từ màn hình
  const main = new THREE.Group(); main.position.set(0, 0, -1.5); scene.add(main);
  box(1.8, 0.04, 0.85, deskM, 0, 0.74, 0, main); box(0.04, 0.72, 0.75, legM, -0.85, 0.36, 0, main); box(0.04, 0.72, 0.75, legM, 0.85, 0.36, 0, main);
  const codeC = document.createElement('canvas'); codeC.width = 1024; codeC.height = 640; const cg = codeC.getContext('2d'); const codeT = new THREE.CanvasTexture(codeC); codeT.colorSpace = THREE.SRGBColorSpace; codeT.anisotropy = 4;
  const R = rng(51); const lines = []; const kw = ['def', 'return', 'if', 'for', 'while', 'class', 'import', 'else', 'try', 'with'];
  for (let i = 0; i < 40; i++) { const ind = Math.floor(R() * 3) * 2; const toks = []; const n = 2 + Math.floor(R() * 6); for (let k = 0; k < n; k++) toks.push(R() < 0.25 ? kw[Math.floor(R() * kw.length)] : 'abcdefghijklmnopqrstuvwxyz'.slice(0, 2 + Math.floor(R() * 7)).split('').sort(() => R() - 0.5).join('')); lines.push({ ind, toks }); }
  let lastCode = -1;
  const drawCode = (u, chk, hl) => { const key = Math.round(u * 400) * 1000 + Math.round(chk * 20); if (key === lastCode) return; lastCode = key;
    cg.fillStyle = '#0e1420'; cg.fillRect(0, 0, 1024, 640); cg.fillStyle = '#18202e'; cg.fillRect(0, 0, 60, 640); cg.font = '22px DejaVu Sans Mono';
    const shown = u * lines.length; const top = Math.max(0, Math.floor(shown) - 22);
    for (let i = top; i < Math.min(lines.length, Math.ceil(shown)); i++) { const y = 34 + (i - top) * 27;
      if (chk > 0 && i === hl) { cg.fillStyle = `rgba(255,200,110,${0.28 * chk})`; cg.fillRect(60, y - 21, 964, 27); cg.fillStyle = `rgba(255,200,110,${chk})`; cg.fillRect(60, y - 21, 6, 27); }
      cg.fillStyle = '#4c5a72'; cg.fillText(String(i + 1).padStart(3, ' '), 6, y); let x = 80 + lines[i].ind * 13;
      const frac = Math.min(1, shown - i); const all = lines[i].toks; const vis = Math.max(1, Math.round(all.length * frac));
      for (let k = 0; k < vis; k++) { const s = all[k]; cg.fillStyle = kw.includes(s) ? '#d6a35c' : (k % 3 === 0 ? '#8fb8e8' : '#c9d4e4'); cg.fillText(s, x, y); x += cg.measureText(s + ' ').width; } }
    codeT.needsUpdate = true; };
  drawCode(0.2, 0, -1);
  const scrM = basic('#ffffff', { map: codeT });
  const doc = canvasTex(512, 320, (g, w, h) => { g.fillStyle = '#1a2232'; g.fillRect(0, 0, w, h); g.strokeStyle = '#6f8fbf'; g.lineWidth = 3; for (let i = 0; i < 5; i++) { g.strokeRect(30 + i * 92, 60 + (i % 2) * 90, 70, 50); if (i) { g.beginPath(); g.moveTo(30 + i * 92 - 22, 85 + ((i - 1) % 2) * 90); g.lineTo(30 + i * 92, 85 + (i % 2) * 90); g.stroke(); } } g.fillStyle = '#4c5a72'; for (let i = 0; i < 6; i++) g.fillRect(30, 230 + i * 12, 200 + (i * 37) % 180, 5); });
  const m1 = box(0.74, 0.46, 0.03, scrM, 0.4, 1.12, -0.22, main); m1.rotation.y = -0.22; const m2 = box(0.74, 0.46, 0.03, basic('#ffffff', { map: doc }), -0.38, 1.12, -0.25, main); m2.rotation.y = 0.12;
  box(0.05, 0.24, 0.05, legM, -0.36, 0.86, -0.28, main); box(0.05, 0.24, 0.05, legM, 0.42, 0.86, -0.25, main); box(0.46, 0.02, 0.15, std('#2a2d33'), -0.1, 0.77, 0.14, main);
  cyl(0.006, 0.006, 0.42, std('#3a3226', { metalness: 0.5 }), 0.82, 0.96, -0.15, main); const sh = cyl(0.045, 0.13, 0.13, std('#8a6a3a', { metalness: 0.4, side: THREE.DoubleSide }), 0.76, 1.16, -0.08, main); sh.rotation.z = 0.4;
  const lampG = glowSprite('#ffc27a', 1.0, 0.5); lampG.position.set(0.73, 1.1, -0.06); main.add(lampG); const lampL = new THREE.PointLight('#ffbf7a', 3.5, 3, 1.6); lampL.position.set(0.7, 1.05, 0.0); main.add(lampL);
  const scrL = new THREE.PointLight('#8fb2ff', 3.2, 3.5, 1.6); scrL.position.set(-0.2, 1.1, 0.25); main.add(scrL);
  const dev = figure({ seated: true, scale: 1.0, color: '#0c0d10' }); dev.root.position.set(-0.05, 0.0, 0.72); dev.root.rotation.y = Math.PI; main.add(dev.root);
  const rimL = new THREE.PointLight('#6f8fcc', 1.6, 2.2, 1.8); rimL.position.set(0.3, 1.5, 1.4); main.add(rimL);
  // bàn đầu hàng trống (c): màn hình tắt, đèn tắt, ghế đẩy vào
  if (v === 'c') { scene.add(new THREE.HemisphereLight('#6a7ea8', '#14171f', 0.8)); for (const [x, z] of [[-6, -2], [0, -4.5], [6, -2], [-3, -7]]) { const ov = new THREE.PointLight('#c8d8ff', 9, 10, 1.2); ov.position.set(x, 2.9, z); scene.add(ov); } }   /* toàn sàn quá tối (Q27 nháp lượt 2) */
  const first = mkDesk(-3.2, 2.2, false, false); const firstL = new THREE.SpotLight('#9fb6e0', 14, 6, 0.5, 0.7, 1.4); firstL.position.set(-3.2, 3.0, 2.6); firstL.target.position.set(-3.2, 0.7, 2.2); scene.add(firstL, firstL.target);
  const dst = dust(scene, [0, 1.6, -1], [6, 2.4, 4], 220, 61, '#b8ccff');
  const K = {
    a: [{ t: 0, p: [0.3, 1.5, 12.5], l: [0, 1.2, -1.5], mm: 30 }, { t: dur, p: [0.2, 1.45, 2.6], l: [-0.2, 1.1, -1.6], mm: 34 }],
    b: [{ t: 0, p: [-1.0, 1.52, -0.15], l: [0.4, 1.12, -1.72], mm: 36 }, { t: dur, p: [-0.75, 1.42, -0.7], l: [0.4, 1.12, -1.72], mm: 44 }],
    c: [{ t: 0, p: [-7.5, 2.4, 6.0], l: [-2.5, 0.9, 0.5], mm: 28 }, { t: dur, p: [-4.5, 1.9, 5.2], l: [-2.9, 0.9, 1.8], mm: 32 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const chkT = opt.check !== undefined ? opt.check : 1e9; const chk = ease((t - chkT) / 0.6);
    const rate = 0.75 / Math.max(dur * 1.2, 8), u0 = (x) => 0.25 + x * rate, uc = Math.min(1, u0(Math.min(t, chkT)));
    const typeU = t < chkT + 2.5 ? uc : Math.min(1, uc + (t - chkT - 2.5) * rate * 0.5);   /* sau khi kiểm 2,5 s: mã tiếp tục hiện chậm (không đứng hình), dòng đã kiểm giữ đánh dấu */
    drawCode(typeU, chk, Math.ceil(uc * lines.length) - 6);
    dev.set({ armR: t < chkT ? -1.0 + 0.07 * Math.sin(t * 9) : -1.0, armL: -1.0 + (t < chkT ? 0.07 * Math.sin(t * 8.2) : 0), headTilt: -0.1 + 0.1 * chk });
    scrL.intensity = 3.2 * (1 + 0.04 * Math.sin(t * 13)); lampG.material.opacity = 1.0 * (1 + 0.02 * Math.sin(f * 0.3));
  };
  return { scene, cam: rig.cam, update, grade: 'cold', exposure: 1.3 };
}

// ===== ladder: thang của người thắp đèn tựa cột đèn, góc phố đêm =====
async function ladder({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#121624', 0.06);
  scene.add(new THREE.HemisphereLight('#3a4466', '#08080c', 0.45));
  const cob = canvasTex(512, 512, (g, w, h) => { const R = rng(4); g.fillStyle = '#26252a'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 22) for (let x = (y / 22 % 2) * 14; x < w; x += 28) { const k = 0.7 + R() * 0.4; g.fillStyle = `rgb(${Math.round(70 * k)},${Math.round(68 * k)},${Math.round(72 * k)})`; g.beginPath(); g.ellipse(x + 12, y + 10, 12, 9, 0, 0, 7); g.fill(); } });
  cob.wrapS = cob.wrapT = THREE.RepeatWrapping; cob.repeat.set(10, 10); box(40, 0.1, 40, std('#ffffff', { map: cob, roughness: 0.9 }), 0, -0.05, 0);
  box(20, 8, 0.4, std('#3a3440'), 0, 4, -4); for (let i = 0; i < 6; i++) box(1.0, 1.4, 0.05, basic(i === 2 || i === 4 ? '#c89058' : '#121018'), -6 + i * 2.4, 3.0, -3.78); const win = new THREE.PointLight('#ffb070', 4, 7, 1.4); win.position.set(-1.2, 3.0, -2.6); scene.add(win);
  const lamp = gasLamp(scene, 0, 0, { lit: 1 });
  // thang gỗ: hai thanh dọc, 9 bậc, tựa vào thanh móc thang dưới lồng đèn (cao ≈ 2,65 m)
  const wood = std('#6a4a2c', { roughness: 0.75 }); const L = new THREE.Group(); scene.add(L); L.position.set(0.0, 0, 0.85); L.rotation.x = -0.3;
  box(0.05, 2.9, 0.05, wood, -0.22, 1.45, 0, L); box(0.05, 2.9, 0.05, wood, 0.22, 1.45, 0, L);
  const rungs = []; for (let i = 0; i < 9; i++) { const r = box(0.44, 0.035, 0.035, wood.clone(), 0, 0.25 + i * 0.3, 0, L); rungs.push(r); }
  const glow = new THREE.PointLight('#ffb468', 9, 5.5, 1.6); glow.position.set(0, 2.7, 0.3); scene.add(glow);
  const dst = dust(scene, [0, 2.4, 0.4], [1.6, 1.6, 1.6], 160, 19);
  const K = { a: [{ t: 0, p: [0.8, 3.1, 2.2], l: [0, 2.95, 0.1], mm: 40 }, { t: dur * 0.7, p: [0.9, 1.1, 2.3], l: [0, 0.6, 0.8], mm: 36 }, { t: dur, p: [0.95, 0.8, 2.4], l: [0, 0.3, 0.85], mm: 34 }],
              b: [{ t: 0, p: [2.4, 0.55, 3.4], l: [0, 1.7, 0.3], mm: 28 }, { t: dur, p: [1.8, 0.45, 2.8], l: [0, 1.3, 0.5], mm: 32 }] }[v];   /* b: góc thấp từ mặt đường, cả cột đèn và thang (đoạn 13) */
  const rig = camRig(W, H, K);
  const update = (t, f) => { rig.at(t); dst.update(t); lamp.set(1, f); glow.intensity = 6 * (1 + 0.04 * Math.sin(f * 0.27));
    rungs.forEach((r, i) => { r.material.color.set(new THREE.Color('#120d08').lerp(new THREE.Color('#8a6038'), Math.min(1, i / 4))); }); };
  return { scene, cam: rig.cam, update, grade: 'cold' };
}

// ===== jpl: phòng tính toán ở California, 1958, ban ngày (đoạn 06: đổi nơi chốn rõ ràng — Q31 vòng 2 T06) =====
//   nắng chiều qua cửa sổ cao (đồi khô, hàng cọ), bảng quỹ đạo lớn trên tường: Trái Đất, đường phóng, quỹ đạo elip vẽ dần (opt.orbit0, opt.orbitDur);
//   một người đứng vẽ trên bảng, hai hàng bàn tính ban ngày (đèn bàn bật). a: từ sau hàng bàn đẩy dần tới bảng.
function orbitBoard() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 600; const g = c.getContext('2d'); const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const E = [430, 330], a = 330, b = 200, cx = E[0] + 120;   // tâm elip lệch khỏi Trái Đất (tiêu điểm)
  const pt = (k) => { const th = Math.PI + k * Math.PI * 2; return [cx + a * Math.cos(th), E[1] + b * Math.sin(th)]; };
  let last = -1;
  const draw = (u, w) => { u = Math.max(0, Math.min(1, u)); if (Math.abs(u - last) < 0.003 && w === undefined) return; last = u;
    g.fillStyle = '#ece4cc'; g.fillRect(0, 0, 1024, 600);
    for (let i = 0; i <= 1024; i += 20) { g.strokeStyle = i % 100 ? 'rgba(80,120,110,0.28)' : 'rgba(60,100,90,0.55)'; g.lineWidth = i % 100 ? 1 : 1.8; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 600); g.stroke(); }
    for (let j = 0; j <= 600; j += 20) { g.strokeStyle = j % 100 ? 'rgba(80,120,110,0.28)' : 'rgba(60,100,90,0.55)'; g.lineWidth = j % 100 ? 1 : 1.8; g.beginPath(); g.moveTo(0, j); g.lineTo(1024, j); g.stroke(); }
    g.fillStyle = '#2a3346'; g.font = 'bold 30px DejaVu Serif'; g.fillText('TRAJECTORY  ·  1958', 40, 52); g.font = 'italic 20px DejaVu Serif'; g.fillText('satellite orbit, plotted by hand', 42, 82);
    g.fillStyle = '#4f6a8e'; g.beginPath(); g.arc(E[0], E[1], 62, 0, 7); g.fill(); g.strokeStyle = '#2a3346'; g.lineWidth = 2; g.stroke();
    g.strokeStyle = 'rgba(42,51,70,0.35)'; g.setLineDash([6, 8]); g.beginPath(); g.ellipse(cx, E[1], a, b, 0, 0, 7); g.stroke(); g.setLineDash([]);   // đường dẫn mờ (tính trước)
    g.strokeStyle = '#8a2e22'; g.lineWidth = 4.5; g.beginPath(); g.moveTo(E[0] - 60, E[1] - 18); g.quadraticCurveTo(E[0] - 95, E[1] - 30, pt(0)[0], pt(0)[1]); g.stroke();   // đường phóng
    const n = Math.floor(400 * u); g.beginPath(); for (let k = 0; k <= n; k++) { const [x, y] = pt(k / 400); k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
    g.fillStyle = '#2a3346'; for (let k = 0; k <= n; k += 25) { const [x, y] = pt(k / 400); g.beginPath(); g.arc(x, y, 5, 0, 7); g.fill();  }
    if (n > 0) { const [x, y] = pt(n / 400); g.fillStyle = '#8a2e22'; g.beginPath(); g.arc(x, y, 9, 0, 7); g.fill(); }
    tex.needsUpdate = true; return pt(n / 400); };
  draw(0, 0); return { tex, draw };
}
async function jpl({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#d8c8a8', 0.012);
  scene.add(new THREE.HemisphereLight('#fff1d6', '#6a5a44', 1.6));
  const lino = canvasTex(512, 512, (g, w, h) => { g.fillStyle = '#9a9a84'; g.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { g.fillStyle = (i + j) % 2 ? '#8f907a' : '#a6a58e'; g.fillRect(i * 64, j * 64, 64, 64); } });
  lino.wrapS = lino.wrapT = THREE.RepeatWrapping; lino.repeat.set(6, 6);
  box(16, 0.1, 22, std('#ffffff', { map: lino, roughness: 0.7 }), 0, 0, -3); box(16, 4, 0.3, std('#e6dcc4'), 0, 2, -9); box(0.3, 4, 22, std('#e0d4b8'), 8, 2, -3); box(16, 0.2, 22, std('#efe6d0'), 0, 4, -3);
  // tường trái: cửa sổ cao nhìn ra đồi khô và hàng cọ dưới nắng chiều
  const view = canvasTex(512, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#9ec4e6'); gr.addColorStop(0.6, '#e8dcc0'); gr.addColorStop(1, '#d9c497'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = '#b08a5e'; g.beginPath(); g.moveTo(0, 170); for (let x = 0; x <= w; x += 16) g.lineTo(x, 150 - 40 * Math.sin(x / 70) - 20 * Math.sin(x / 23)); g.lineTo(w, h); g.lineTo(0, h); g.fill();
    g.fillStyle = '#8f7a52'; g.fillRect(0, 210, w, h - 210);
    g.strokeStyle = '#3d3a2a'; g.fillStyle = '#3d3a2a'; for (const [px, ph] of [[90, 150], [210, 175], [370, 160], [450, 140]]) { g.lineWidth = 5; g.beginPath(); g.moveTo(px, 230); g.quadraticCurveTo(px + 8, 230 - ph / 2, px + 4, 230 - ph); g.stroke();
      for (let k = 0; k < 7; k++) { const an = k / 7 * Math.PI * 2; g.beginPath(); g.ellipse(px + 4 + 20 * Math.cos(an), 230 - ph + 8 * Math.sin(an), 24, 5, an, 0, 7); g.fill(); } } });
  for (let i = 0; i < 4; i++) { const z = 3 - i * 3.2; box(0.06, 2.4, 2.0, basic('#ffffff', { map: view }), -7.83, 2.2, z); box(0.12, 2.6, 0.12, std('#5a5444'), -7.8, 2.2, z - 1.05); box(0.12, 0.12, 2.2, std('#5a5444'), -7.8, 2.2, z); box(0.12, 0.12, 2.2, std('#5a5444'), -7.8, 1.0, z); }
  box(0.3, 4, 22, std('#e0d4b8'), -8, 2, -3);
  const sun = new THREE.DirectionalLight('#ffe0a8', 3.2); sun.position.set(-14, 9, 4); sun.target.position.set(0, 0, -3); scene.add(sun, sun.target); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 10, bottom: -10 });
  // vệt nắng trên sàn (cửa sổ chiếu xiên), hạt bụi trong vệt nắng
  for (let i = 0; i < 4; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(3.0, 1.8), basic('#fff0c8', { transparent: true, opacity: 0.22, depthWrite: false, blending: THREE.AdditiveBlending })); m.rotation.x = -Math.PI / 2; m.position.set(-4.6, 0.06, 3 - i * 3.2); scene.add(m); }
  // bảng quỹ đạo trên tường cuối
  const ob = orbitBoard(); box(5.0, 2.9, 0.05, std('#ffffff', { map: ob.tex, roughness: 0.85 }), 0.6, 2.15, -8.8); box(5.2, 0.1, 0.12, std('#6b4a2a'), 0.6, 0.66, -8.75); box(5.2, 0.1, 0.12, std('#6b4a2a'), 0.6, 3.64, -8.75);
  const bl = new THREE.SpotLight('#fff4dc', 40, 12, 0.5, 0.5, 1.2); bl.position.set(0.6, 3.8, -4.5); bl.target.position.set(0.6, 2.1, -8.8); scene.add(bl, bl.target);
  for (const [x, z] of [[-2, -1], [3, -5]]) { const cl = new THREE.PointLight('#fff2dc', 6, 12, 1.2); cl.position.set(x, 3.2, z); scene.add(cl); }
  // người đứng vẽ trên bảng (áo sáng màu, không mặt)
  const pl = figure({ scale: 1.0, color: '#2e2622' }); const bun = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 10), lam('#2e2622')); bun.position.set(0, 1.62, -0.1); pl.root.add(bun);
  pl.root.position.set(-1.2, 0, -8.3); pl.root.rotation.y = Math.PI - 0.25; scene.add(pl.root);
  // hai hàng bàn tính, ban ngày (đèn bàn vẫn bật), người làm việc
  const desks = []; for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) desks.push(computeDesk(scene, -2.6 + c * 2.5, -4.6 + r * 2.4, { lampOn: true, seed: 300 + r * 3 + c, pc: ['#2e2622', '#28292e', '#33281f'][(r + c) % 3] }));
  const dst = dust(scene, [-3.5, 1.6, -1], [4, 2.4, 8], 260, 59, '#fff0d0');
  const K = { a: [{ t: 0, p: [3.2, 1.75, 4.6], l: [-0.4, 1.6, -6], mm: 28 }, { t: dur, p: [1.6, 1.85, -2.6], l: [0.2, 2.0, -8.8], mm: 34 }] }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const u = ease((t - (opt.orbit0 !== undefined ? opt.orbit0 : 0.5)) / (opt.orbitDur || dur * 0.7)); ob.draw(u);
    pl.set({ armR: -1.75 - 0.3 * Math.sin(u * Math.PI * 2), armL: -0.15, headTilt: -0.1 });
    desks.forEach((d) => d.set(t, f, { lamp: 1 }));
  };
  return { scene, cam: rig.cam, update, grade: 'sepia', exposure: 1.0 };
}

export const HEROES = { airfield, pool, relay, tower, ladder, jpl };

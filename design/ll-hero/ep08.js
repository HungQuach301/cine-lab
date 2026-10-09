// Last Lamplighters · Tập 8 "From Headphones to Machine Drafts" — CẢNH ĐINH 3D (dựng riêng, không lặp bố cục cảnh đinh tập 6–7).
// Nội thất chi tiết, sáng, ánh sáng có nguồn, vật liệu có vân (BAI-HOC #97). Người: bóng vô danh, không mặt, không cận mặt.
//   library   góc phố có thư viện đá lúc chạng vạng; trong: phòng đọc bàn dài, đèn đọc sách chao xanh, kệ sách.
//             a: đẩy máy vào dải cửa sổ (móc câu) · b: người thắp đèn thắp cột cạnh cửa sổ, đèn đọc sách trong phòng bừng (opt.lit, opt.hand)
//             c: trong phòng đọc, người dịch tình nguyện (bóng) bên thư, từ điển (opt.write) · d: phố, người thắp đèn đi qua thư viện (cầu 05)
//             e: cầu 09 — cửa sổ thư viện tắt (opt.dark), máy lia sang căn hộ bên kia đường, màn hình sáng (opt.screen) · f: kết — cột cuối (opt.lit), máy cẩu lên
//   booths    phòng xử Nuremberg 1945, trung tính: dãy buồng kính phiên dịch, tai nghe trên mọi băng ghế, cáp trên sàn, đèn quay phim sáng.
//             a: toàn phòng, máy trượt dọc dãy buồng · b: trong buồng qua vai người phiên dịch (lưng), micro, đèn cảnh báo (opt.warn) · c: băng ghế, tai nghe, núm chọn kênh (opt.dial)
//   ibm       phòng máy New York 1954, ban ngày: tủ máy xám, đầu đọc thẻ đục lỗ (thẻ chạy, opt.feed), máy in dòng nhả câu tiếng Anh (opt.print). a: toàn phòng · b: cận máy in
//   postedit  phòng dịch thập niên 1960, nắng qua rèm: bàn gỗ, máy chữ, tạp chí tiếng Nga, bản in máy có vết bút đỏ (opt.mark), bảng thuật ngữ in liên tục.
//             a: toàn phòng · b: cận bản in, bút đỏ sửa dần · c: bảng thuật ngữ + máy chữ gõ (opt.type)
//   studio    bàn người dịch hôm nay, ban ngày: hai màn hình (câu nguồn | bản nháp máy đang sửa, opt.edit), cây xanh, kệ từ điển, nắng cửa sổ.
//             a: từ cửa đẩy vào · b: qua vai, màn hình post-editing · c: góc bên cạnh cửa sổ
//   vrs       buồng phiên dịch từ xa / video relay, ban ngày: tấm tiêu âm, tai nghe micro, màn hình gọi video người ra dấu (cách điệu, không mặt).
//             a: toàn buồng · b: qua vai, màn hình ra dấu · c: góc cửa sổ
import { THREE, useScene, gasLamp, figure, dust, camRig, box, cyl, lam, std, glowSprite, rng, ease, lerp, canvasTex } from './kit.js';

const fogOf = (scene, color, d) => { useScene(scene); scene.fog = new THREE.FogExp2(color, d); scene.background = new THREE.Color(color); };
const basic = (color, o = {}) => new THREE.MeshBasicMaterial({ color, ...o });
const rep = (t, x, y) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(x, y); return t; };

// ===== kết cấu dùng chung =====
const woodTex = (seed, base = [104, 68, 40], planks = 6) => canvasTex(512, 512, (g, w, h) => { const R = rng(seed);
  for (let p = 0; p < planks; p++) { const k = 0.85 + R() * 0.3, y0 = p * h / planks; g.fillStyle = `rgb(${Math.round(base[0] * k)},${Math.round(base[1] * k)},${Math.round(base[2] * k)})`; g.fillRect(0, y0, w, h / planks);
    for (let n = 0; n < 26; n++) { const y = y0 + R() * h / planks, a = 0.08 + R() * 0.12; g.strokeStyle = `rgba(${R() < 0.5 ? '40,22,10' : '190,140,90'},${a})`; g.lineWidth = 1 + R() * 2; g.beginPath(); g.moveTo(0, y);
      for (let x = 0; x <= w; x += 32) g.lineTo(x, y + 3 * Math.sin(x * 0.02 + n)); g.stroke(); }
    g.fillStyle = 'rgba(20,10,4,0.55)'; g.fillRect(0, y0, w, 2); } });
const tileTex = (a, b, n = 8) => canvasTex(256, 256, (g, w, h) => { const R = rng(5); const s = w / n; for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { const k = 0.93 + R() * 0.1, c = (i + j) % 2 ? a : b;
  g.fillStyle = `rgb(${Math.round(c[0] * k)},${Math.round(c[1] * k)},${Math.round(c[2] * k)})`; g.fillRect(i * s, j * s, s, s); } g.strokeStyle = 'rgba(0,0,0,0.25)'; for (let i = 0; i <= n; i++) { g.beginPath(); g.moveTo(i * s, 0); g.lineTo(i * s, h); g.moveTo(0, i * s); g.lineTo(w, i * s); g.stroke(); } });
const plasterTex = (c, seed = 3) => canvasTex(256, 256, (g, w, h) => { const R = rng(seed); g.fillStyle = c; g.fillRect(0, 0, w, h); for (let n = 0; n < 900; n++) { g.fillStyle = `rgba(${R() < 0.5 ? '255,255,255' : '0,0,0'},${0.03 + R() * 0.04})`; g.fillRect(R() * w, R() * h, 2 + R() * 6, 2 + R() * 6); } });
const spinesTex = (seed) => canvasTex(512, 256, (g, w, h) => { const R = rng(seed); g.fillStyle = '#2a1a10'; g.fillRect(0, 0, w, h); const pal = ['#7a2a22', '#2e4a3a', '#34405e', '#8a6a36', '#5a3a28', '#c8b48a', '#3a2a40', '#6a6a5a'];
  for (let row = 0; row < 4; row++) { let x = 2; const y0 = row * 64 + 4; while (x < w - 4) { const bw = 7 + R() * 12, bh = 46 + R() * 12; g.fillStyle = pal[Math.floor(R() * pal.length)]; g.fillRect(x, y0 + 58 - bh, bw, bh);
    g.fillStyle = 'rgba(230,200,140,0.6)'; g.fillRect(x + 1, y0 + 62 - bh + 8, bw - 2, 2); g.fillRect(x + 1, y0 + 62 - bh + 30, bw - 2, 1.5); x += bw + 1; } g.fillStyle = '#4a3020'; g.fillRect(0, y0 + 58, w, 6); } });
const letterTex = (seed, hand = true) => canvasTex(256, 320, (g, w, h) => { const R = rng(seed); g.fillStyle = hand ? '#efe6cf' : '#f4f1e8'; g.fillRect(0, 0, w, h); g.strokeStyle = hand ? 'rgba(40,40,80,0.75)' : 'rgba(30,30,30,0.8)'; g.lineWidth = hand ? 1.6 : 2.2;
  for (let y = 30; y < h - 20; y += hand ? 16 : 13) { let x = 18; const end = w - 18 - R() * 40; g.beginPath(); while (x < end) { const s = 8 + R() * 28; if (hand) { g.moveTo(x, y); for (let k = 0; k < s; k += 3) g.lineTo(x + k, y + 2.5 * Math.sin(k * 0.9 + x)); } else { g.moveTo(x, y); g.lineTo(x + s, y); } x += s + 5; } g.stroke(); } });

// figure ngồi có ánh viền (để bóng không chìm vào nền tối: BAI-HOC #77)
const seated = (color = '#1a1512', scale = 0.95, rim = '#ffe2b0') => { const f = figure({ seated: true, scale, color }); if (rim) { const r = new THREE.PointLight(rim, 0.9, 1.6, 2); r.position.set(0.3, 1.5 * scale, -0.6); f.root.add(r); } return f; };
// tai nghe (vòng cung + hai chụp) gắn lên đầu figure hoặc đặt trên bàn
function headphones(parent, x = 0, y = 0, z = 0, s = 1, color = '#2a2a2e') { const g = new THREE.Group(); g.position.set(x, y, z); g.scale.setScalar(s); parent.add(g);
  const band = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.012, 8, 24, Math.PI), std(color, { metalness: 0.5, roughness: 0.4 })); g.add(band);
  for (const sx of [-1, 1]) { const cup = cyl(0.05, 0.05, 0.035, std('#1c1c20', { roughness: 0.6 }), sx * 0.13, -0.02, 0, g); cup.rotation.z = Math.PI / 2; } return g; }

// ===== library: góc phố thư viện, chạng vạng; phòng đọc bên trong =====
async function library({ W, H, dur, v, opt = {} }) {
  const inside = v === 'c';
  const scene = new THREE.Scene(); fogOf(scene, inside ? '#2a2018' : '#2c2638', inside ? 0.02 : 0.014);
  const sky = new THREE.Mesh(new THREE.SphereGeometry(200, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, map: canvasTex(8, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#141c38'); gr.addColorStop(0.36, '#3a3a66'); gr.addColorStop(0.46, '#a8665a'); gr.addColorStop(0.5, '#e8a464'); gr.addColorStop(0.53, '#3a2a2e'); gr.addColorStop(1, '#141218'); g.fillStyle = gr; g.fillRect(0, 0, w, h); }) }));
  if (!inside) scene.add(sky);
  // phố lát đá, vỉa hè, đường ray ngựa kéo cũ (vạch tối)
  const cob = rep(canvasTex(512, 512, (g, w, h) => { const R = rng(8); g.fillStyle = '#2e2b2e'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 20) for (let x = (y / 20 % 2) * 13; x < w; x += 26) { const k = 0.7 + R() * 0.45; g.fillStyle = `rgb(${Math.round(92 * k)},${Math.round(86 * k)},${Math.round(84 * k)})`; g.beginPath(); g.ellipse(x + 11, y + 9, 11, 8, 0, 0, 7); g.fill(); } }), 14, 6);
  box(80, 0.1, 30, std('#ffffff', { map: cob, roughness: 0.85 }), 0, -0.05, 9);
  const slab = rep(tileTex([120, 114, 104], [108, 102, 94], 4), 30, 2); box(80, 0.16, 3.2, std('#ffffff', { map: slab, roughness: 0.9 }), 0, 0.08, 1.6); box(80, 0.16, 3.2, std('#ffffff', { map: slab, roughness: 0.9 }), 0, 0.08, 16.4);
  // thư viện: mặt tiền đá, bậc, cột, dải cửa sổ cao vòm (phòng đọc thấy qua kính)
  const stone = std('#ffffff', { map: rep(canvasTex(256, 256, (g, w, h) => { const R = rng(12); g.fillStyle = '#b4a68c'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 32; x < w; x += 64) { const k = 0.9 + R() * 0.15; g.fillStyle = `rgb(${Math.round(176 * k)},${Math.round(162 * k)},${Math.round(136 * k)})`; g.fillRect(x + 1, y + 1, 62, 30); } }), 6, 3), roughness: 0.9 });
  const trim = std('#d8ccb0', { roughness: 0.8 });
  const lib = new THREE.Group(); scene.add(lib);
  box(24, 1.0, 0.5, stone, 0, 0.5, -0.25, lib); box(24, 1.5, 0.5, stone, 0, 5.75, -0.25, lib); box(24.6, 0.4, 0.8, trim, 0, 6.6, -0.2, lib); box(24.2, 0.2, 0.7, trim, 0, 5.0, -0.1, lib);
  const WIN = [-9, -5.4, -1.8, 1.8, 5.4, 9]; const winM = [];
  for (let i = 0; i <= 6; i++) { const x = i === 0 ? -11.2 : i === 6 ? 11.2 : (WIN[i - 1] + WIN[i]) / 2; box(i === 0 || i === 6 ? 1.6 : 1.4, 4.0, 0.5, stone, x, 3.0, -0.25, lib); cyl(0.22, 0.25, 4.0, trim, x, 3.0, 0.15, lib); }
  WIN.forEach((x, i) => { const m = basic('#f2c27a', { transparent: true, opacity: 0.1, depthWrite: false }); winM.push(m); box(2.2, 4.0, 0.04, m, x, 3.0, -0.02, lib);
    for (let k = 1; k < 4; k++) box(2.2, 0.05, 0.06, std('#2a2218'), x, 1.0 + k, 0.0, lib); box(0.05, 4.0, 0.06, std('#2a2218'), x, 3.0, 0.0, lib); box(2.4, 0.14, 0.3, trim, x, 1.0, 0.12, lib); });
  for (let s = 0; s < 3; s++) box(5, 0.16, 0.5, stone, 0, 0.08 + s * 0.16, 0.75 - s * 0.35, lib);   // bậc thềm
  const sign = canvasTex(1024, 96, (g, w, h) => { g.fillStyle = '#c8bc9e'; g.fillRect(0, 0, w, h); g.fillStyle = '#4a3e2a'; g.font = 'bold 64px DejaVu Serif'; g.textAlign = 'center'; g.fillText('P U B L I C   L I B R A R Y', w / 2, 70); });
  box(9, 0.8, 0.05, std('#ffffff', { map: sign, roughness: 0.9 }), 0, 5.75, 0.02, lib);
  // phòng đọc: sàn gỗ, kệ sách hai bên và tường sau, bàn dài, đèn chao xanh, đèn trần
  const room = new THREE.Group(); scene.add(room);
  const floorW = rep(woodTex(21, [120, 80, 46], 8), 6, 3);
  box(24, 0.05, 10, std('#ffffff', { map: floorW, roughness: 0.7 }), 0, 0.02, -5.3, room); box(24, 7, 0.2, std('#ffffff', { map: rep(plasterTex('#cdb894'), 4, 2) }), 0, 3.5, -10.3, room); box(24, 0.2, 10, std('#bfa880'), 0, 6.5, -5.3, room);
  const spines = spinesTex(41); for (const [x, z, ry, len] of [[0, -10.1, 0, 22], [-11.8, -5.3, Math.PI / 2, 9.6], [11.8, -5.3, -Math.PI / 2, 9.6]]) { const sh = box(len, 4.4, 0.4, std('#ffffff', { map: rep(spines, len / 3, 1), roughness: 0.85 }), x, 2.3, z, room); sh.rotation.y = ry; }
  box(22, 0.15, 0.5, std('#4a3020'), 0, 4.6, -9.9, room);
  const tableWood = std('#ffffff', { map: rep(woodTex(23, [110, 70, 38], 3), 2, 1), roughness: 0.55 });
  const readers = [], lamps = []; const R = rng(29);
  for (const tz of [-3.2, -6.6]) { box(14, 0.08, 1.4, tableWood, 0, 0.78, tz, room); for (const lx of [-6.6, 6.6]) box(0.12, 0.76, 1.2, std('#3a2414'), lx, 0.38, tz, room);
    for (let k = 0; k < 6; k++) { const x = -5.5 + k * 2.2; const lg = new THREE.Group(); lg.position.set(x, 0.82, tz); room.add(lg);
      cyl(0.06, 0.08, 0.03, std('#8a6a3a', { metalness: 0.6, roughness: 0.3 }), 0, 0.015, 0, lg); cyl(0.01, 0.01, 0.34, std('#8a6a3a', { metalness: 0.6 }), 0, 0.18, 0, lg);
      const shade = cyl(0.14, 0.14, 0.12, std('#2f6a48', { roughness: 0.35, side: THREE.DoubleSide }), 0, 0.38, 0, lg, 20); shade.rotation.x = Math.PI / 2; shade.scale.set(1, 1, 0.45);
      const gl = glowSprite('#ffd79a', 0.9, 0.55); gl.position.set(0, 0.3, 0.05); lg.add(gl); const pl = new THREE.PointLight('#ffcf8a', 0, 3.2, 1.6); pl.position.set(0, 0.28, 0.1); lg.add(pl); lamps.push({ gl, pl, x, tz });
      for (const side of [-1, 1]) { if (R() < 0.35) continue; const p = seated(['#2a221c', '#1f2228', '#30261e'][Math.floor(R() * 3)], 0.95, null); p.root.position.set(x + (R() - 0.5) * 0.6, 0, tz + side * 1.0); p.root.rotation.y = side > 0 ? Math.PI : 0; room.add(p.root); readers.push({ p, ph: R() * 6 }); }
      for (let n = 0; n < 3; n++) { const lt = box(0.24, 0.006, 0.3, std('#ffffff', { map: letterTex(100 + k * 7 + n, n !== 1), roughness: 0.9 }), x + (R() - 0.5) * 1.2, 0.825, tz + (R() - 0.5) * 0.7, room); lt.rotation.y = (R() - 0.5) * 0.8; }
      if (k % 2 === 0) { const bk = box(0.3, 0.09, 0.22, std(['#7a2a22', '#2e4a3a', '#34405e'][k % 3]), x + 0.5, 0.865, tz - 0.25, room); bk.rotation.y = 0.3; box(0.28, 0.02, 0.2, std('#efe4c8'), x + 0.5, 0.915, tz - 0.25, room).rotation.y = 0.3; } } }
  for (const x of [-6, 0, 6]) { const ch = cyl(0.5, 0.35, 0.3, std('#c8a050', { metalness: 0.6, roughness: 0.3 }), x, 5.6, -5, room); const cl = new THREE.PointLight('#ffd8a0', 0, 12, 1.2); cl.position.set(x, 5.2, -5); room.add(cl); lamps.push({ ceil: cl, glow: glowSprite('#ffe0b0', 0.8, 1.4), x }); lamps[lamps.length - 1].glow.position.set(x, 5.35, -5); room.add(lamps[lamps.length - 1].glow); }
  // đèn đọc sách sát cửa sổ (nhận lửa qua ô kính, biến thể b)
  const near = lamps.find((l) => l.gl && Math.abs(l.x - 1.1) < 0.2 && l.tz === -3.2);
  // dãy nhà hai bên phố (mặt tiền gạch, cửa sổ ấm), để phố không trống
  const RB = rng(55); for (const [x0, z0, ry] of [[-26, -0.4, 0], [26, -0.4, 0], [-22, 19.4, Math.PI], [24, 19.4, Math.PI]]) { const n = 3; for (let k = 0; k < n; k++) { const bw = 6 + RB() * 2, bh = 7 + RB() * 5, x = x0 + (k - 1) * 8 * (x0 < 0 ? 1 : 1);
    const b = box(bw, bh, 6, std('#ffffff', { map: rep(plasterTex(['#7a5a4a', '#6a5a62', '#8a6a52'][k % 3], 20 + k), 2, 2), roughness: 0.95 }), x, bh / 2, z0 - 3 * Math.cos(ry)); 
    for (let r = 0; r < Math.floor(bh / 2.6); r++) for (let c = 0; c < 2; c++) { const lit = RB() < 0.45; box(1.0, 1.4, 0.05, basic(lit ? '#e0a860' : '#181a22'), x - bw / 4 + c * bw / 2, 2.0 + r * 2.6, z0 - 6 * Math.cos(ry) * 0 + (ry ? -0.05 : 0.05) + (ry ? 0 : 0)); } } }
  // căn hộ bên kia đường (+z), một ô cửa có màn hình sáng (biến thể e)
  const apt = new THREE.Group(); apt.position.set(4, 0, 19); scene.add(apt);
  const aw = std('#ffffff', { map: rep(plasterTex('#6a5a58', 9), 2, 3), roughness: 0.95 }); box(8.35, 12, 0.4, aw, -4.825, 6, 0, apt); box(8.35, 12, 0.4, aw, 4.825, 6, 0, apt); box(1.3, 4.85, 0.4, aw, 0, 2.425, 0, apt); box(1.3, 5.45, 0.4, aw, 0, 9.275, 0, apt);   /* ô trống cho cửa sổ màn hình: thấy phòng bên trong */
  const aptWins = []; for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) { if (r === 1 && c === 2) continue; const lit = (r * 5 + c) % 4 === 1; const m = basic(lit ? '#d89c58' : '#141620', { transparent: true, opacity: 0.95 }); const w = box(1.3, 1.7, 0.05, m, -6 + c * 3, 2.5 + r * 3.2, -0.22, apt); aptWins.push(w); box(1.5, 0.12, 0.2, std('#8a7a6a'), -6 + c * 3, 1.6 + r * 3.2, -0.3, apt); }
  const scrWin = basic('#141620', { transparent: true, opacity: 0.35, depthWrite: false }); box(1.3, 1.7, 0.02, scrWin, 0, 5.7, -0.25, apt); box(1.5, 0.12, 0.2, std('#8a7a6a'), 0, 4.8, -0.3, apt); box(0.06, 1.7, 0.06, std('#2a2420'), 0, 5.7, -0.27, apt);
  const scrGlow = glowSprite('#9cc4ff', 0, 1.6); scrGlow.position.set(0, 5.6, -0.4); apt.add(scrGlow); const scrL = new THREE.PointLight('#9cc4ff', 0, 5, 1.5); scrL.position.set(0.1, 5.4, 0.6); apt.add(scrL); const aptLamp = gasLamp(scene, 4.5, 15.8, { lit: 1 });
  const scrBox = box(0.5, 0.32, 0.02, basic('#0a0c12'), 0.25, 5.15, 0.9, apt); scrBox.rotation.y = Math.PI + 0.5;
  // phòng sau ô cửa màn hình: tường sau, bàn, người (bóng) nghiêng nhìn màn hình
  box(1.3, 1.7, 0.05, basic('#141620', { transparent: true, opacity: 0.0 }), 0, 5.7, -0.23, apt);
  box(3, 3, 0.1, std('#4a4a58'), 0, 5.6, 2.2, apt); box(3, 0.1, 3, std('#3a3434'), 0, 4.2, 0.9, apt); box(1.2, 0.05, 0.6, std('#6a4a30'), 0.1, 4.95, 0.9, apt);
  const aptP = seated('#0e0e14', 0.9, null); aptP.root.position.set(-0.35, 4.2, 1.0); aptP.root.rotation.y = -Math.PI / 2 - 0.4; apt.add(aptP.root); aptP.set({ armR: -1.2, armL: -1.1, headTilt: 0.2 });
  // cột đèn khí: cạnh cửa sổ (b), giữa phố (d), cuối dãy (f); người thắp đèn
  const lampA = gasLamp(scene, 2.6, 2.4, { lit: 0 }), lampB = gasLamp(scene, -9, 2.4, { lit: 0 }), lampC = gasLamp(scene, 13.5, 2.4, { lit: 0 }), lampD = gasLamp(scene, -20, 2.4, { lit: 0 });
  const lighter = figure({ hat: true, scale: 1.0 }); scene.add(lighter.root);
  const pole = cyl(0.015, 0.015, 3.0, lam('#2a2016'), 0, 0.1, 0); lighter.armR.add(pole); pole.rotation.x = -0.25;
  const wick = glowSprite('#ffb86a', 0.95, 0.42); wick.position.set(0, 1.52, 0); pole.add(wick); const wickL = new THREE.PointLight('#ffae62', 2.6, 3.4, 1.6); wickL.position.set(0, 1.45, 0.1); pole.add(wickL);
  scene.add(new THREE.HemisphereLight(inside ? '#ffe0b8' : '#7a6e96', inside ? '#3a2a1c' : '#1c1618', inside ? 0.9 : 0.95));
  const sun = new THREE.DirectionalLight('#ffb07a', inside ? 0.0 : 0.8); sun.position.set(30, 8, 20); scene.add(sun);
  const fill = new THREE.PointLight('#ffb070', inside ? 0 : 2.4, 22, 1.2); fill.position.set(0, 4, 9); scene.add(fill);
  const winSun = new THREE.SpotLight('#ffcf98', inside ? 30 : 0, 16, 0.6, 0.6, 1.2); winSun.position.set(3, 4.5, 3); winSun.target.position.set(0, 0.8, -4.5); scene.add(winSun, winSun.target);
  const dst = dust(scene, inside ? [0, 1.8, -4] : [2.6, 3.0, 2.4], inside ? [8, 2.4, 5] : [2.4, 2.0, 2.2], 200, 13);
  const K = {
    a: [{ t: 0, p: [-3.5, 1.5, 15], l: [0, 3.0, -1], mm: 28 }, { t: dur, p: [0.6, 2.4, 6.2], l: [0.8, 2.6, -3], mm: 34 }],
    b: [{ t: 0, p: [-6.5, 1.6, 11], l: [-2, 2.4, 1], mm: 30 }, { t: Math.max(1, (opt.lit || 7) - 1.5), p: [-0.6, 1.8, 8.6], l: [2.4, 2.6, 0.5], mm: 34 }, { t: dur, p: [0.9, 2.2, 6.4], l: [1.2, 1.8, -3], mm: 42 }],
    c: [{ t: 0, p: [-4.5, 1.7, -0.6], l: [0, 0.95, -4.6], mm: 30 }, { t: dur, p: [-1.8, 1.45, -1.5], l: [0.6, 0.85, -3.4], mm: 38 }],
    d: [{ t: 0, p: [-14, 1.7, 10], l: [-10, 2.2, 2], mm: 30 }, { t: dur, p: [-3, 1.9, 10.5], l: [1, 2.4, 1], mm: 30 }],
    e: [{ t: 0, p: [0.5, 2.0, 9.5], l: [0.5, 3.0, -1], mm: 32 }, { t: Math.max(0.5, (opt.screen || 6) - 1.0), p: [2.0, 2.4, 10.5], l: [3.8, 4.8, 19], mm: 30 }, { t: dur, p: [3.4, 4.2, 15.0], l: [4.0, 5.25, 19.5], mm: 40 }],
    f: [{ t: 0, p: [8.5, 1.6, 10.5], l: [13, 2.4, 2.4], mm: 32 }, { t: (opt.lit || 7) + 0.6, p: [9.5, 2.0, 9.0], l: [13.4, 3.0, 2.4], mm: 36 }, { t: dur, p: [-2, 8.5, 13.5], l: [8, 2.6, 0], mm: 26 }],
  }[v];
  const rig = camRig(W, H, K);
  const raise = (t, tl, x0, x1, lampX) => { const ta = tl - 1.0, u = Math.min(1, t / ta); lighter.root.position.set(lerp(x0, x1, ease(u)), 0.16, 2.9); lighter.root.rotation.y = Math.PI / 2;
    const rz = u < 1 ? 0 : ease((t - ta) / 1.2); lighter.set({ walk: u < 1 ? t * 5 : 0, armR: lerp(0.2, 0.15, rz) }); pole.rotation.x = lerp(-0.25, 0.2, rz); };
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    let read = 1, hand = 1, screen = 0;
    if (v === 'a') { lampA.set(1, f); lampB.set(1, f); lighter.root.position.set(-30, 0, 0); }
    else if (v === 'b') { const tl = opt.lit !== undefined ? opt.lit : dur * 0.45; raise(t, tl, -7.5, 1.95); lampA.set(ease((t - tl) / 1.0), f); lampB.set(0, f); hand = ease((t - (opt.hand !== undefined ? opt.hand : tl + 1.2)) / 1.2); read = 0.55 + 0.45 * hand; }
    else if (v === 'c') { lampA.set(1, f); lighter.root.position.set(-30, 0, 0); }
    else if (v === 'd') { lighter.root.position.set(lerp(-14, 0, t / dur), 0.16, 3.2); lighter.root.rotation.y = Math.PI / 2; lighter.set({ walk: t * 5 }); lampA.set(1, f); lampB.set(1, f); lampD.set(1, f); }
    else if (v === 'e') { lampA.set(1, f); lampB.set(1, f); lampC.set(1, f); const dk = ease((t - (opt.dark !== undefined ? opt.dark : 1.5)) / 1.6); read = 1 - dk; hand = 1 - dk; screen = ease((t - (opt.screen !== undefined ? opt.screen : 5)) / 1.0);
      lighter.root.position.set(lerp(4, 9, t / dur), 0.16, 3.2); lighter.root.rotation.y = Math.PI / 2; lighter.set({ walk: t * 5 }); }
    else { const tl = opt.lit !== undefined ? opt.lit : dur * 0.4; raise(t, tl, 6, 12.85); lampA.set(1, f); lampB.set(1, f); lampC.set(ease((t - tl) / 1.0), f); screen = 1; }
    winM.forEach((m) => { m.color.set(new THREE.Color('#141620').lerp(new THREE.Color('#f2c27a'), read)); m.opacity = lerp(0.9, inside ? 0.05 : 0.12, read); });
    lamps.forEach((l, i) => { const on = l === near ? hand : read; if (l.gl) { l.gl.material.opacity = 0.9 * on * (1 + 0.03 * Math.sin(f * 0.3 + i)); l.pl.intensity = (l === near ? 4.5 : 2.2) * on; } else { l.ceil.intensity = (inside ? 16 : 10) * read; l.glow.material.opacity = 0.8 * read; } });
    readers.forEach(({ p, ph }) => p.set({ armR: -1.1 + 0.08 * Math.sin(t * 2.4 + ph), armL: -0.9, headTilt: 0.4 + 0.04 * Math.sin(t * 0.5 + ph) }));
    scrWin.opacity = 0.75 - 0.5 * screen; scrWin.color.set(new THREE.Color('#141620').lerp(new THREE.Color('#9cb8e8'), screen * 0.4)); scrGlow.material.opacity = 0.8 * screen; scrL.intensity = 6 * screen; scrBox.material.color.set(new THREE.Color('#0a0c12').lerp(new THREE.Color('#e8f0ff'), screen));
  };
  return { scene, cam: rig.cam, update, grade: 'warm', exposure: inside ? 1.15 : 1.05 };
}

// ===== booths: phòng xử 1945, dãy buồng kính phiên dịch (trung tính, không người bị xử) =====
async function booths({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#2a2016', 0.006);
  scene.add(new THREE.HemisphereLight('#fff4e0', '#5a4028', 1.5));
  const panel = rep(canvasTex(512, 512, (g, w, h) => { const R = rng(61); g.fillStyle = '#5a3a20'; g.fillRect(0, 0, w, h);
    for (let x = 0; x < w; x += 128) { const k = 0.85 + R() * 0.25; g.fillStyle = `rgb(${Math.round(110 * k)},${Math.round(72 * k)},${Math.round(40 * k)})`; g.fillRect(x + 8, 8, 112, h - 16);
      for (let n = 0; n < 18; n++) { g.strokeStyle = `rgba(40,20,8,${0.1 + R() * 0.15})`; g.lineWidth = 1 + R() * 2; const xx = x + 12 + R() * 104; g.beginPath(); g.moveTo(xx, 10); g.bezierCurveTo(xx + 6, h * 0.3, xx - 6, h * 0.6, xx + 3, h - 10); g.stroke(); }
      g.strokeStyle = 'rgba(230,180,110,0.25)'; g.lineWidth = 2; g.strokeRect(x + 14, 14, 100, h - 28); } }), 6, 1);
  const wood = std('#ffffff', { map: panel, roughness: 0.55 }), dark = std('#3a2412', { roughness: 0.5 });
  const parquet = rep(woodTex(63, [130, 88, 52], 10), 10, 6);
  box(30, 0.1, 24, std('#ffffff', { map: parquet, roughness: 0.6 }), 0, 0, -2); box(30, 0.3, 24, std('#e8dcc4'), 0, 7.2, -2);
  box(30, 7.2, 0.3, wood, 0, 3.6, -14); box(0.3, 7.2, 24, wood, -15, 3.6, -2); box(0.3, 7.2, 24, wood, 15, 3.6, -2);
  // cửa sổ cao có rèm xanh (tường trái), trần có đèn
  for (let i = 0; i < 4; i++) { const z = 6 - i * 5; box(0.05, 3.6, 2.2, basic('#e8eef0', { transparent: true, opacity: 0.85 }), -14.8, 4.2, z); for (const dz of [-1.35, 1.35]) box(0.15, 4.2, 0.6, std('#3a5a4a', { roughness: 0.9 }), -14.7, 4.1, z + dz); }
  const winL = new THREE.DirectionalLight('#fff4e0', 1.6); winL.position.set(-20, 8, 2); winL.target.position.set(0, 0, -2); scene.add(winL, winL.target); winL.castShadow = true; winL.shadow.mapSize.set(1024, 1024); Object.assign(winL.shadow.camera, { left: -15, right: 15, top: 10, bottom: -10 });
  for (const [x, z] of [[-7, 0], [0, -4], [7, 0], [0, 5], [9, -6]]) { const cl = new THREE.PointLight('#ffe8c8', 16, 18, 1.15); cl.position.set(x, 6.6, z); scene.add(cl); box(1.2, 0.1, 1.2, basic('#fff2d8'), x, 7.0, z); }
  // đèn quay phim công suất lớn trên chân (sáng, tương phản)
  for (const [x, z, tx, tz] of [[-12, 8, -2, -6], [11, 9, 4, -7]]) { const st = new THREE.Group(); st.position.set(x, 0, z); scene.add(st); cyl(0.04, 0.04, 3.4, std('#2a2a2a', { metalness: 0.6 }), 0, 1.7, 0, st);
    const head = cyl(0.35, 0.45, 0.6, std('#3a3a3c', { metalness: 0.5 }), 0, 3.6, 0, st); head.lookAt(tx - x, 0, tz - z); const lens = glowSprite('#fff6e0', 0.9, 1.2); lens.position.set(0, 3.6, 0.3); st.add(lens);
    const sp = new THREE.SpotLight('#fff4e4', 60, 30, 0.45, 0.5, 1.0); sp.position.set(x, 3.6, z); sp.target.position.set(tx, 0.8, tz); scene.add(sp, sp.target); }
  // dãy buồng kính phiên dịch (tường phải, bục cao), mỗi buồng: khung gỗ, kính, người phiên dịch (lưng), tai nghe, micro, đèn cảnh báo
  const B = []; const glass = new THREE.MeshPhysicalMaterial({ color: '#dfe8e8', transparent: true, opacity: 0.08, roughness: 0.05, metalness: 0, depthWrite: false });
  box(3.2, 0.8, 16, wood, 12.6, 0.4, -4);   // bục
  for (let i = 0; i < 4; i++) { const z = 2 - i * 3.6, g = new THREE.Group(); g.position.set(12.4, 0.8, z); scene.add(g);
    box(0.1, 0.95, 3.3, wood, -1.0, 0.48, 0, g); for (const dz of [-1.6, 1.6]) box(0.12, 2.4, 0.12, dark, -1.0, 1.95, dz, g); box(2.6, 0.12, 3.3, dark, 0.2, 3.1, 0, g); box(2.4, 2.4, 0.08, wood, 0.2, 1.9, -1.62, g); box(2.4, 2.4, 0.08, wood, 0.2, 1.9, 1.62, g); box(0.08, 2.4, 3.3, std('#7a5a3a'), 1.4, 1.9, 0, g);
    const gl = box(0.03, 1.4, 3.1, glass, -1.0, 1.6, 0, g); box(2.4, 0.06, 3.0, std('#5a3a20'), 0.1, 0.95, 0, g);
    const sign = canvasTex(256, 64, (gg, w, h) => { gg.fillStyle = '#2a1a0c'; gg.fillRect(0, 0, w, h); gg.fillStyle = '#e8d8b0'; gg.font = 'bold 34px DejaVu Sans'; gg.textAlign = 'center'; gg.fillText(['ENGLISH', 'FRANÇAIS', 'РУССКИЙ', 'DEUTSCH'][i], w / 2, 45); });
    box(0.04, 0.3, 1.4, basic('#ffffff', { map: sign }), -1.06, 2.82, 0, g);
    const p = seated('#2a2420', 1.0, '#fff0d0'); p.root.position.set(0.6, 0.15, 0); p.root.rotation.y = -Math.PI / 2; g.add(p.root); headphones(p.root, 0, 1.17, 0, 1.0);
    const mic = new THREE.Group(); mic.position.set(-0.35, 1.0, 0); g.add(mic); cyl(0.05, 0.06, 0.03, std('#2a2a2a', { metalness: 0.6 }), 0, 0, 0, mic); cyl(0.008, 0.008, 0.25, std('#5a5a5a', { metalness: 0.7 }), 0, 0.13, 0, mic); const mh = cyl(0.035, 0.035, 0.09, std('#3a3a3a', { metalness: 0.7, roughness: 0.3 }), 0, 0.28, 0, mic); mh.rotation.z = Math.PI / 2;
    const warn = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), basic('#5a3a10')); warn.position.set(-0.6, 1.07, 0.9); g.add(warn); const wg = glowSprite('#ffb030', 0, 0.5); wg.position.copy(warn.position); g.add(wg);
    for (let n = 0; n < 3; n++) box(0.2, 0.004, 0.28, std('#ffffff', { map: letterTex(300 + i * 5 + n, false) }), -0.2 + n * 0.12, 0.985, -0.6 + n * 0.5, g).rotation.y = 0.2 * n;
    const bl = new THREE.PointLight('#ffe4b8', 7, 5, 1.3); bl.position.set(0.3, 2.7, 0); g.add(bl); const bg = glowSprite('#fff0d0', 0.7, 0.8); bg.position.set(0.3, 2.95, 0); g.add(bg);
    B.push({ g, p, warn, wg, ph: i * 1.7 }); }
  // băng ghế với tai nghe, núm chọn kênh, cáp trên sàn; bàn thẩm phán trống ở cuối, bục có micro
  const benchWood = std('#ffffff', { map: rep(woodTex(67, [120, 80, 44], 4), 2, 1), roughness: 0.5 });
  const dials = []; const listeners = [];
  for (let r = 0; r < 4; r++) for (const side of [-1, 1]) { const z = 4 - r * 2.6, x = side * 4.2 - 2; box(6.2, 0.08, 0.7, benchWood, x, 0.78, z); box(6.2, 0.75, 0.08, dark, x, 0.38, z + 0.32); box(6.2, 0.06, 0.5, benchWood, x, 0.46, z + 0.8); box(6.2, 0.6, 0.06, dark, x, 0.8, z + 1.05);
    for (let k = 0; k < 4; k++) { const hx = x - 2.3 + k * 1.5; if ((r + k) % 3 === 1 && r > 0) { const p = seated(['#2e2a28', '#3a3430', '#26282c'][k % 3], 1.0, null); p.root.position.set(hx, 0, z + 0.85); p.root.rotation.y = Math.PI; scene.add(p.root); headphones(p.root, 0, 1.17, 0, 1.0); listeners.push({ p, ph: r + k }); continue; }
      const hp = headphones(scene, hx, 0.86, z - 0.05, 1.0); hp.rotation.x = -Math.PI / 2;
      const db = box(0.16, 0.06, 0.1, std('#2a2a2a', { metalness: 0.4 }), hx + 0.35, 0.85, z - 0.2); const knob = cyl(0.03, 0.03, 0.03, std('#c8b070', { metalness: 0.7, roughness: 0.3 }), hx + 0.35, 0.9, z - 0.2); dials.push(knob);
      const cab = cyl(0.008, 0.008, 1.2, std('#1a1a1a'), hx + 0.1, 0.42, z - 0.1); cab.rotation.z = 0.2; } }
  for (let i = 0; i < 9; i++) { const c = cyl(0.015, 0.015, 7 + i * 0.6, std('#141414', { roughness: 0.6 }), -1 + i * 1.3, 0.02, -2 + (i % 3) * 1.1); c.rotation.z = Math.PI / 2; c.rotation.y = 0.15 * Math.sin(i * 1.7); }
  box(12, 1.4, 1.6, wood, -2, 1.2, -11.6); box(12.4, 0.12, 1.9, dark, -2, 1.95, -11.6); for (let k = 0; k < 5; k++) { const mx = -6.4 + k * 2.2; cyl(0.006, 0.006, 0.4, std('#5a5a5a', { metalness: 0.7 }), mx, 2.2, -11.2); headphones(scene, mx + 0.5, 2.03, -11.3, 0.9).rotation.x = -Math.PI / 2; }
  const lect = box(0.9, 1.2, 0.6, wood, -2, 0.6, -5.5); cyl(0.008, 0.008, 0.5, std('#5a5a5a', { metalness: 0.7 }), -2, 1.45, -5.4);
  const dst = dust(scene, [2, 3, -2], [16, 5, 14], 320, 71, '#fff0d0');
  const K = {
    a: [{ t: 0, p: [-4, 2.4, 8.5], l: [11, 2.0, -3], mm: 28 }, { t: dur, p: [3, 2.2, 7.0], l: [12, 2.0, -6], mm: 32 }],
    b: [{ t: 0, p: [14.0, 2.45, 2.75], l: [10.0, 1.75, 1.3], mm: 28 }, { t: dur, p: [13.85, 2.4, 2.55], l: [9.0, 1.6, 0.6], mm: 32 }],
    c: [{ t: 0, p: [-6.4, 1.35, 5.3], l: [-4.0, 0.85, 3.6], mm: 36 }, { t: dur, p: [-3.2, 1.25, 5.2], l: [-1.5, 0.85, 3.7], mm: 40 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const wt = opt.warn !== undefined ? opt.warn : 1e9;
    B.forEach(({ p, warn, wg, ph }, i) => { p.set({ armR: -0.6 + 0.12 * Math.sin(t * 2.3 + ph), armL: -0.9 + 0.05 * Math.sin(t * 1.7 + ph), headTilt: 0.15 + 0.05 * Math.sin(t * 0.9 + ph) });
      const on = i === 1 && t > wt && t < wt + 3.2 ? (Math.sin((t - wt) * 9) > -0.2 ? 1 : 0.2) : 0; warn.material.color.set(on ? '#ffc040' : '#5a3a10'); wg.material.opacity = 0.9 * on; });
    listeners.forEach(({ p, ph }) => p.set({ armR: -0.4, armL: -0.4, headTilt: 0.1 + 0.04 * Math.sin(t * 0.6 + ph) }));
    const dt = opt.dial !== undefined ? opt.dial : 1e9; dials.forEach((k, i) => { k.rotation.y = i === 0 ? ease((t - dt) / 0.8) * 2.2 : 0.4 * i; });
  };
  return { scene, cam: rig.cam, update, grade: 'sepia', exposure: 1.1 };
}

// ===== ibm: phòng máy New York 1954, ban ngày =====
async function ibm({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#d8d2c4', 0.01);
  scene.add(new THREE.HemisphereLight('#fffaf0', '#7a7060', 1.2));
  box(26, 0.1, 22, std('#ffffff', { map: rep(tileTex([214, 208, 192], [120, 128, 120], 8), 3, 2.6), roughness: 0.35 }), 0, 0, -3);
  box(26, 4.2, 0.3, std('#ffffff', { map: rep(plasterTex('#e8e2d2', 4), 6, 1) }), 0, 2.1, -14); box(0.3, 4.2, 22, std('#e2dccb'), 13, 2.1, -3); box(26, 0.3, 22, std('#f2eee4'), 0, 4.2, -3);
  for (let i = 0; i < 5; i++) { box(2.4, 0.06, 0.6, basic('#fffdf4'), -8 + i * 4, 4.02, -4); box(2.4, 0.06, 0.6, basic('#fffdf4'), -8 + i * 4, 4.02, 2); }
  for (const [x, z] of [[-6, -4], [2, -4], [8, 2], [-4, 3]]) { const cl = new THREE.PointLight('#fff8ec', 9, 16, 1.2); cl.position.set(x, 3.8, z); scene.add(cl); }
  // cửa sổ có rèm lá (tường trái), nắng xiên vào sàn
  for (let i = 0; i < 4; i++) { const z = 4 - i * 4.5; box(0.05, 2.4, 2.6, basic('#f8f4e8'), -12.9, 2.3, z); for (let s = 0; s < 12; s++) box(0.08, 0.04, 2.6, std('#d8d0bc'), -12.8, 1.2 + s * 0.2, z); }
  box(0.3, 4.2, 22, std('#e2dccb'), -13, 2.1, -3);
  const sun = new THREE.DirectionalLight('#fff0d0', 2.6); sun.position.set(-18, 9, 3); sun.target.position.set(0, 0, -3); scene.add(sun, sun.target); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 10, bottom: -10 });
  // tủ máy xám có đèn bảng, băng từ quay
  const grey = std('#8a8e92', { metalness: 0.3, roughness: 0.45 }), panelM = std('#4a4e54', { metalness: 0.4 });
  const blinks = [], reels = [];
  for (let i = 0; i < 6; i++) { const x = -9 + i * 3.4, z = -12.5; const u = new THREE.Group(); u.position.set(x, 0, z); scene.add(u); box(2.6, 2.2, 1.2, grey, 0, 1.1, 0, u); box(2.6, 0.12, 1.25, panelM, 0, 2.26, 0, u);
    if (i % 2) { for (const rx of [-0.55, 0.55]) { const r = cyl(0.42, 0.42, 0.05, std('#2a2a2e', { metalness: 0.6 }), rx, 1.45, 0.62, u, 24); r.rotation.x = Math.PI / 2; reels.push(r); cyl(0.12, 0.12, 0.06, std('#c8c8c8', { metalness: 0.8 }), rx, 1.45, 0.64, u).rotation.x = Math.PI / 2; } box(2.0, 0.6, 0.02, basic('#d8e0e4', { transparent: true, opacity: 0.4 }), 0, 1.45, 0.62, u); }
    else for (let r = 0; r < 4; r++) for (let c = 0; c < 10; c++) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 6), basic('#5a4020')); b.position.set(-0.9 + c * 0.2, 1.2 + r * 0.22, 0.61); u.add(b); blinks.push({ b, ph: (i * 40 + r * 10 + c) * 0.73 }); } }
  // bàn điều khiển có bảng đèn
  const con = new THREE.Group(); con.position.set(-3, 0, -6); scene.add(con); box(3.2, 0.9, 1.0, grey, 0, 0.45, 0, con); const top = box(3.2, 0.08, 1.0, panelM, 0, 1.0, -0.1, con); top.rotation.x = -0.3;
  for (let c = 0; c < 16; c++) for (let r = 0; r < 3; r++) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 6), basic('#5a4020')); b.position.set(-1.4 + c * 0.18, 1.02 + r * 0.07, 0.15 - r * 0.22); con.add(b); blinks.push({ b, ph: c * 1.3 + r * 2.1 }); }
  // đầu đọc thẻ đục lỗ: chồng thẻ, thẻ trượt qua
  const cardT = canvasTex(256, 112, (g, w, h) => { const R = rng(77); g.fillStyle = '#efe0b4'; g.fillRect(0, 0, w, h); g.fillStyle = '#c8b480'; g.fillRect(0, 0, 14, h); g.fillStyle = '#3a3020'; g.font = '9px DejaVu Sans Mono'; for (let c = 0; c < 40; c++) g.fillText(String(c % 10), 18 + c * 5.8, 10);
    for (let c = 0; c < 40; c++) for (let r = 0; r < 12; r++) if (R() < 0.12) g.fillRect(18 + c * 5.8, 16 + r * 7.8, 3, 5); });
  const cardM = std('#ffffff', { map: cardT, roughness: 0.8 });
  const rd = new THREE.Group(); rd.position.set(4.5, 0, -6.5); scene.add(rd); box(1.8, 1.0, 1.0, grey, 0, 0.5, 0, rd); box(1.8, 0.06, 1.0, panelM, 0, 1.03, 0, rd);
  const hopper = box(0.5, 0.35, 0.25, std('#c8b480'), -0.45, 1.24, 0, rd); for (let k = 0; k < 16; k++) box(0.48, 0.004, 0.22, cardM, -0.45, 1.07 + k * 0.022, 0, rd);
  const flying = []; for (let k = 0; k < 6; k++) { const c = box(0.48, 0.004, 0.22, cardM, 0, 1.1, 0, rd); flying.push(c); }
  const stack = box(0.5, 0.2, 0.24, cardM, 0.5, 1.15, 0, rd);
  // máy in dòng: giấy liên tục, câu tiếng Anh in dần
  const LINES = ['THE QUALITY OF COAL IS DETERMINED BY CALORY CONTENT.', 'TNT IS PRODUCED FROM COAL.', 'GASOLINE IS PREPARED BY CHEMICAL METHODS FROM CRUDE OIL.', 'THE PRICE OF CRUDE OIL IS DETERMINED BY THE MARKET.', 'AMMONITE IS OBTAINED FROM SALTPETER.', 'THEY OBTAIN DYNAMITE FROM NITROGLYCERINE.'];
  const pc = document.createElement('canvas'); pc.width = 768; pc.height = 1024; const pg = pc.getContext('2d'); const pT = new THREE.CanvasTexture(pc); pT.colorSpace = THREE.SRGBColorSpace; pT.anisotropy = 4; let lastP = -1;
  const drawP = (u) => { const k = Math.round(u * 600); if (k === lastP) return; lastP = k; pg.fillStyle = '#f4f0e2'; pg.fillRect(0, 0, 768, 1024);
    for (let y = 0; y < 1024; y += 64) { pg.fillStyle = 'rgba(150,200,170,0.25)'; pg.fillRect(40, y, 688, 32); } pg.fillStyle = '#d8d0b8'; for (let y = 10; y < 1024; y += 28) { pg.beginPath(); pg.arc(18, y, 6, 0, 7); pg.arc(750, y, 6, 0, 7); pg.fill(); }
    pg.fillStyle = '#20201c'; pg.font = 'bold 26px DejaVu Sans Mono'; const total = LINES.join('').length; let left = Math.floor(u * total); let y = 120;
    for (const L of LINES) { if (left <= 0) break; const s = L.slice(0, left); pg.fillText(s, 50, y); left -= L.length; y += 72; } pT.needsUpdate = true; };
  drawP(0);
  const pr = new THREE.Group(); pr.position.set(1.0, 0, -3.2); scene.add(pr); box(1.8, 1.0, 1.1, grey, 0, 0.5, 0, pr); box(1.9, 0.1, 1.15, panelM, 0, 1.05, 0, pr); box(1.6, 0.3, 0.2, panelM, 0, 1.25, -0.2, pr);
  const sheet = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 1.73), std('#ffffff', { map: pT, roughness: 0.9, side: THREE.DoubleSide })); sheet.position.set(0, 1.95, -0.22); sheet.rotation.x = -0.12; pr.add(sheet);
  const fold = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 0.9), std('#f0ecdc', { side: THREE.DoubleSide })); fold.position.set(0, 0.55, 0.62); fold.rotation.x = -1.1; pr.add(fold);
  // người xem (bóng, đứng, áo vest) và người vận hành
  const people = []; for (const [x, z, ry, c] of [[-0.6, -1.6, Math.PI + 0.3, '#2a2a30'], [2.4, -1.4, Math.PI - 0.2, '#30302e'], [3.0, -5.0, Math.PI / 2 + 0.6, '#262a30'], [-4.5, -4.7, Math.PI, '#2c2822']]) { const p = figure({ scale: 1.0, color: c }); p.root.position.set(x, 0, z); p.root.rotation.y = ry; scene.add(p.root); people.push(p); const r = new THREE.PointLight('#fff4e0', 0.8, 1.8, 2); r.position.set(0, 1.7, -0.5); p.root.add(r); }
  const dst = dust(scene, [-2, 1.8, -3], [10, 3, 8], 240, 81, '#fff6e0');
  const K = {
    a: [{ t: 0, p: [-10, 2.2, 6.5], l: [2, 1.2, -6], mm: 26 }, { t: dur, p: [-2.5, 1.8, 3.6], l: [4.3, 1.1, -6.4], mm: 32 }],
    b: [{ t: 0, p: [1.9, 1.8, -0.7], l: [0.9, 1.85, -3.4], mm: 34 }, { t: dur, p: [1.4, 1.95, -1.5], l: [0.85, 2.0, -3.4], mm: 42 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    blinks.forEach(({ b, ph }) => b.material.color.set(Math.sin(t * 3 + ph) > 0.3 ? '#ffd070' : '#5a4020'));
    reels.forEach((r, i) => { r.rotation.y = t * (i % 2 ? 2.2 : -1.6); });
    const ft = opt.feed !== undefined ? opt.feed : 0.5; flying.forEach((c, k) => { const u = ((t - ft) * 1.4 + k / 6) % 1; const on = t > ft; c.visible = on; c.position.set(lerp(-0.45, 0.5, u), 1.12 + 0.1 * Math.sin(u * Math.PI), 0); });
    const pt = opt.print !== undefined ? opt.print : 0.5; drawP(Math.min(1, Math.max(0, (t - pt) / Math.max(4, dur * 0.8))));
    people.forEach((p, i) => p.set({ armR: -0.15 + (i === 1 ? -0.5 * ease((t - 2) / 1) : 0), armL: -0.1, headTilt: 0.15 + 0.04 * Math.sin(t * 0.7 + i) }));
  };
  return { scene, cam: rig.cam, update, grade: 'sepia', exposure: 1.0 };
}

// ===== postedit: phòng dịch 1960s, ban ngày =====
async function postedit({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#3a3026', 0.015);
  scene.add(new THREE.HemisphereLight('#fff0d8', '#4a3a28', 0.95));
  box(18, 0.1, 16, std('#ffffff', { map: rep(tileTex([150, 132, 104], [134, 116, 90], 8), 3, 2.5), roughness: 0.6 }), 0, 0, -3);
  box(18, 3.6, 0.3, std('#ffffff', { map: rep(plasterTex('#d8c8a4', 6), 4, 1) }), 0, 1.8, -11); box(0.3, 3.6, 16, std('#d4c4a0'), 9, 1.8, -3); box(18, 0.2, 16, std('#f2e8d2'), 0, 3.6, -3); scene.add(new THREE.PointLight('#fff4e0', 5, 14, 1.2).translateY(3.2).translateZ(-6));
  box(18, 1.0, 0.32, std('#ffffff', { map: rep(woodTex(91, [100, 66, 38], 3), 6, 1) }), 0, 0.5, -10.95);   // ốp chân tường gỗ
  // cửa sổ rèm lá (tường trái) — nắng xiên thành sọc
  box(0.3, 3.6, 16, std('#d4c4a0'), -9, 1.8, -3);
  for (let i = 0; i < 3; i++) { const z = 2 - i * 4.5; box(0.05, 2.0, 2.4, basic('#fff6e0'), -8.84, 2.0, z); for (let s = 0; s < 14; s++) box(0.06, 0.03, 2.4, std('#e0d4b4'), -8.78, 1.05 + s * 0.14, z); }
  const sun = new THREE.DirectionalLight('#ffe0a8', 3.0); sun.position.set(-14, 6, 1); sun.target.position.set(0, 0.7, -3); scene.add(sun, sun.target); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -12, right: 12, top: 8, bottom: -8 });
  const stripes = canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); g.fillStyle = '#fff'; for (let y = 0; y < h; y += 18) g.fillRect(0, y, w, 10); });
  for (let i = 0; i < 3; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 2.6), basic('#fff0c8', { map: stripes, transparent: true, opacity: 0.2, depthWrite: false, blending: THREE.AdditiveBlending })); m.rotation.x = -Math.PI / 2; m.position.set(-5.6, 0.06, 2 - i * 4.5); scene.add(m); }
  for (const [x, z] of [[-2, -1], [3, -6]]) { const cl = new THREE.PointLight('#fff2dc', 6, 12, 1.2); cl.position.set(x, 3.3, z); scene.add(cl); box(1.0, 0.06, 0.4, basic('#fff6e4'), x, 3.48, z); }
  // đồng hồ treo tường, tủ hồ sơ, giá áo, kệ tạp chí tiếng Nga
  const clock = canvasTex(128, 128, (g) => { g.fillStyle = '#f4ecd8'; g.beginPath(); g.arc(64, 64, 60, 0, 7); g.fill(); g.strokeStyle = '#2a2018'; g.lineWidth = 4; g.stroke(); for (let k = 0; k < 12; k++) { const a = k / 12 * 6.283; g.fillStyle = '#2a2018'; g.fillRect(64 + 48 * Math.sin(a) - 2, 64 - 48 * Math.cos(a) - 2, 4, 4); } g.lineWidth = 4; g.beginPath(); g.moveTo(64, 64); g.lineTo(64, 30); g.moveTo(64, 64); g.lineTo(92, 70); g.stroke(); });
  const ck = new THREE.Mesh(new THREE.CircleGeometry(0.35, 32), std('#ffffff', { map: clock })); ck.position.set(2, 2.8, -10.83); scene.add(ck);
  for (let i = 0; i < 3; i++) { const fc = box(0.8, 1.4, 0.7, std('#6a6e66', { metalness: 0.4, roughness: 0.5 }), 5 + i * 0.85, 0.7, -10.4); for (let d = 0; d < 3; d++) box(0.6, 0.04, 0.02, std('#c8c8c0', { metalness: 0.7 }), 5 + i * 0.85, 0.35 + d * 0.42, -10.04); }
  const journ = (seed) => canvasTex(160, 220, (g, w, h) => { const R = rng(seed); const c = ['#a83a2a', '#2a5a7a', '#c89838', '#3a6a4a'][seed % 4]; g.fillStyle = '#efe6d0'; g.fillRect(0, 0, w, h); g.fillStyle = c; g.fillRect(0, 0, w, 60); g.fillStyle = '#fff'; g.font = 'bold 18px DejaVu Sans'; g.fillText(['ЖУРНАЛ', 'ВЕСТНИК', 'ДОКЛАДЫ', 'ХИМИЯ'][seed % 4], 10, 38); g.fillStyle = '#2a2a2a'; g.font = '11px DejaVu Sans'; for (let y = 80; y < h - 10; y += 14) g.fillRect(10, y, 40 + R() * 100, 3); });
  const shelf = new THREE.Group(); shelf.position.set(-3.5, 0, -10.5); scene.add(shelf); box(3.0, 2.2, 0.4, std('#5a3a22'), 0, 1.1, 0, shelf); for (let r = 0; r < 4; r++) for (let k = 0; k < 7; k++) { const j = box(0.32, 0.42, 0.03, std('#ffffff', { map: journ(k + r * 7) }), -1.15 + k * 0.38, 0.32 + r * 0.52, 0.21, shelf); j.rotation.z = (k % 3 - 1) * 0.04; }
  // bàn người dịch: bản in máy (bút đỏ sửa dần), máy chữ, bảng thuật ngữ, từ điển, gạt tàn, đèn bàn
  const deskW = std('#ffffff', { map: rep(woodTex(93, [118, 76, 42], 3), 1.5, 1), roughness: 0.5 });
  const MT = ['THE INVESTIGATION OF STATE OF SYSTEM OF KROVOTVORENI4 AND', 'DETERMINATION OF INTERMEDIATE PRODUCTS THE EXCHANGE OF', 'NUCLEINIC ACIDS WAS CONDUCTED ON MAMMALS. BESIDES THIS,', 'THERE WAS CONDUCTED THE CHECK FOR THE STATE OR PIGMENTAQII', 'THE HAIR AT BLACK MICE. THE PHYSIOLOGICAL SHIFTS WERE STUDIED', 'ALSO ON THE SEEDS OF HIGHER PLANTS, MICROORGANISMS, THE CELLS', 'OF THE DIFFERENT TISSUES IN CULTURE AND T D.'];
  const FIX = [[0, 37, 57, 'blood formation'], [1, 46, 54, 'metabolism'], [2, 0, 15, 'nucleic acids'], [3, 41, 56, 'pigmentation of'], [4, 0, 8, 'in the'], [6, 39, 44, 'etc.']];
  const mc = document.createElement('canvas'); mc.width = 1024; mc.height = 768; const mg = mc.getContext('2d'); const mT = new THREE.CanvasTexture(mc); mT.colorSpace = THREE.SRGBColorSpace; mT.anisotropy = 8; let lastM = -1;
  const drawM = (u) => { const k = Math.round(u * 300); if (k === lastM) return; lastM = k; mg.fillStyle = '#f2eedf'; mg.fillRect(0, 0, 1024, 768);
    mg.fillStyle = '#d8d0b4'; for (let y = 12; y < 768; y += 30) { mg.beginPath(); mg.arc(16, y, 6, 0, 7); mg.arc(1008, y, 6, 0, 7); mg.fill(); }
    mg.font = '22px DejaVu Sans Mono'; mg.fillStyle = '#26241e'; const cw = mg.measureText('M').width; MT.forEach((L, i) => mg.fillText(L, 44, 90 + i * 90));
    const n = u * FIX.length; FIX.forEach(([ln, a, b, rep], j) => { const q = Math.max(0, Math.min(1, n - j)); if (q <= 0) return; const y = 90 + ln * 90, x0 = 44 + a * cw, x1 = 44 + b * cw;
      mg.strokeStyle = '#c0281c'; mg.lineWidth = 3.5; mg.beginPath(); mg.moveTo(x0, y - 7); mg.lineTo(x0 + (x1 - x0) * Math.min(1, q * 2), y - 9); mg.stroke();
      if (q > 0.5) { mg.fillStyle = '#c0281c'; mg.font = 'italic 30px DejaVu Serif'; const s = rep.slice(0, Math.ceil(rep.length * (q - 0.5) * 2)); mg.fillText(s, x0, y - 30); mg.font = '22px DejaVu Sans Mono'; } });
    mT.needsUpdate = true; };
  drawM(0);
  const GL = [['кровотворение', 'blood formation'], ['обмен веществ', 'metabolism'], ['нуклеиновые кислоты', 'nucleic acids'], ['пигментация', 'pigmentation'], ['ткань', 'tissue'], ['клетка', 'cell'], ['семена', 'seeds'], ['микроорганизм', 'microorganism'], ['млекопитающие', 'mammals'], ['промежуточный продукт', 'intermediate product']];
  const glT = canvasTex(512, 768, (g, w, h) => { g.fillStyle = '#f4f0e0'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(150,200,170,0.25)'; for (let y = 0; y < h; y += 60) g.fillRect(30, y, w - 60, 30); g.fillStyle = '#d8d0b4'; for (let y = 12; y < h; y += 30) { g.beginPath(); g.arc(14, y, 5, 0, 7); g.arc(w - 14, y, 5, 0, 7); g.fill(); }
    g.fillStyle = '#26241e'; g.font = 'bold 18px DejaVu Sans Mono'; g.fillText('TEXT-RELATED GLOSSARY', 40, 40); g.font = '17px DejaVu Sans Mono'; GL.forEach(([a, b], i) => { g.fillText(a.toUpperCase(), 40, 90 + i * 60); g.fillText(b.toUpperCase(), 40, 112 + i * 60); }); });
  const tc = document.createElement('canvas'); tc.width = 512; tc.height = 640; const tg = tc.getContext('2d'); const tT = new THREE.CanvasTexture(tc); tT.colorSpace = THREE.SRGBColorSpace; let lastT = -1;
  const TYPED = 'The investigation of the blood-forming system and the determination of intermediate products of nucleic acid metabolism were carried out on mammals.';
  const drawT = (u) => { const k = Math.round(u * TYPED.length); if (k === lastT) return; lastT = k; tg.fillStyle = '#f8f6ee'; tg.fillRect(0, 0, 512, 640); tg.fillStyle = '#22201c'; tg.font = '22px DejaVu Serif';
    const words = TYPED.slice(0, k).split(' '); const L = []; let line = ''; for (const w of words) { if (tg.measureText(line + w).width > 440) { L.push(line); line = ''; } line += w + ' '; } L.push(line); L.forEach((s, i) => tg.fillText(s, 36, 600 - (L.length - 1 - i) * 36)); tT.needsUpdate = true; };   /* giấy cuộn lên: dòng đang gõ nằm sát trục cuốn */
  drawT(0);
  const D = new THREE.Group(); D.position.set(0, 0, -3); scene.add(D);
  box(2.6, 0.06, 1.2, deskW, 0, 0.76, 0, D); box(0.08, 0.73, 1.1, std('#3a2414'), -1.2, 0.37, 0, D); box(0.6, 0.6, 1.1, std('#4a2e18'), 0.95, 0.4, 0, D);
  const mt = box(0.9, 0.004, 0.68, std('#ffffff', { map: mT, roughness: 0.9 }), -0.35, 0.795, 0.12, D); mt.rotation.y = 0.06;
  const cont = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.5), std('#efebdc', { side: THREE.DoubleSide })); cont.position.set(-0.35, 0.55, 0.68); cont.rotation.x = -1.2; D.add(cont);
  const gls = box(0.42, 0.004, 0.62, std('#ffffff', { map: glT, roughness: 0.9 }), 0.55, 0.795, 0.2, D); gls.rotation.y = -0.1;
  const pencil = cyl(0.006, 0.006, 0.17, std('#b82a1c'), -0.1, 0.81, 0.3, D); pencil.rotation.z = Math.PI / 2; pencil.rotation.y = 0.5;
  // máy chữ: thân, bàn phím, trục cuốn giấy, tờ giấy đang gõ
  const tw = new THREE.Group(); tw.position.set(0.5, 0.79, -0.32); D.add(tw); const twM = std('#2e3a36', { metalness: 0.3, roughness: 0.4 });
  box(0.56, 0.12, 0.42, twM, 0, 0.06, 0, tw); box(0.5, 0.06, 0.18, twM, 0, 0.12, -0.14, tw); const plat = cyl(0.035, 0.035, 0.6, std('#1a1a1a'), 0, 0.17, -0.18, tw); plat.rotation.z = Math.PI / 2;
  for (let r = 0; r < 4; r++) for (let c = 0; c < 11; c++) { cyl(0.0085, 0.0085, 0.006, std('#ece4cc', { roughness: 0.4 }), -0.21 + c * 0.04 + r * 0.01, 0.128 + r * 0.013, 0.17 - r * 0.036, tw, 12); cyl(0.0095, 0.0095, 0.004, std('#b8a878', { metalness: 0.7, roughness: 0.3 }), -0.21 + c * 0.04 + r * 0.01, 0.124 + r * 0.013, 0.17 - r * 0.036, tw, 12); }
  for (let k = 0; k < 22; k++) { const a = -1.2 + k * 0.11, bar = box(0.004, 0.003, 0.09, std('#9a9488', { metalness: 0.8, roughness: 0.3 }), 0.09 * Math.sin(a), 0.135, -0.06 + 0.03 * Math.cos(a), tw); bar.rotation.y = a; }   /* rổ cần chữ */
  for (const sx of [-0.2, 0.2]) { cyl(0.04, 0.04, 0.015, std('#1a1a1a'), sx, 0.155, -0.06, tw, 20); cyl(0.03, 0.03, 0.017, std('#7a1a14'), sx, 0.156, -0.06, tw, 20); }   /* hai cuộn ruy băng */
  const lever = cyl(0.006, 0.006, 0.14, std('#c8c0b0', { metalness: 0.8 }), -0.33, 0.2, -0.16, tw); lever.rotation.z = 1.2;
  const tp = new THREE.Mesh(new THREE.PlaneGeometry(0.34, 0.42), std('#ffffff', { map: tT, side: THREE.DoubleSide, roughness: 0.9 })); tp.position.set(0, 0.36, -0.22); tp.rotation.x = -0.25; tw.add(tp);
  const dict = box(0.3, 0.1, 0.22, std('#7a2a22'), -1.0, 0.84, -0.3, D); box(0.28, 0.02, 0.2, std('#efe4c8'), -1.0, 0.9, -0.3, D);
  const dl = new THREE.Group(); dl.position.set(-1.05, 0.79, -0.42); D.add(dl); cyl(0.07, 0.08, 0.02, std('#2a2a26', { metalness: 0.6 }), 0, 0, 0, dl); const arm = cyl(0.008, 0.008, 0.45, std('#2a2a26', { metalness: 0.6 }), 0.05, 0.22, 0, dl); arm.rotation.z = -0.2;
  const shd = cyl(0.05, 0.12, 0.12, std('#c89838', { metalness: 0.5, side: THREE.DoubleSide }), 0.14, 0.44, 0.08, dl); shd.rotation.x = 0.6; const dlL = new THREE.PointLight('#ffd49a', 3, 2.6, 1.6); dlL.position.set(0.14, 0.38, 0.2); dl.add(dlL);
  const tr = seated('#2c2620', 1.0, '#fff0d0'); tr.root.position.set(-0.2, 0, 0.75); tr.root.rotation.y = Math.PI; D.add(tr.root);
  // các bàn khác (người làm, giấy, máy chữ)
  const others = []; for (const [x, z] of [[-4.2, -2.5], [4.2, -2.5], [-4.2, -6.5], [0, -7.0], [4.2, -6.5]]) { const g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g); box(2.2, 0.06, 1.1, deskW, 0, 0.76, 0, g); box(0.5, 0.6, 1.0, std('#4a2e18'), 0.8, 0.4, 0, g); box(0.5, 0.15, 0.4, twM, 0.2, 0.86, -0.25, g);
    for (let n = 0; n < 3; n++) box(0.3, 0.005, 0.4, std('#ffffff', { map: letterTex(400 + n + x * 3 | 0, false) }), -0.5 + n * 0.25, 0.795, 0.1, g).rotation.y = 0.15 * n;
    const p = seated(['#2e2a26', '#262a2e', '#30281e'][others.length % 3], 0.98, null); p.root.position.set(0, 0, 0.75); p.root.rotation.y = Math.PI; g.add(p.root); others.push(p); }
  const dst = dust(scene, [-4, 1.6, -2], [5, 2.4, 9], 260, 95, '#fff0d0');
  const K = {
    a: [{ t: 0, p: [3.8, 2.3, 4.2], l: [-1, 0.9, -4.5], mm: 28 }, { t: dur, p: [1.6, 1.9, 1.6], l: [-0.6, 0.85, -3.6], mm: 32 }],
    b: [{ t: 0, p: [-0.35, 1.55, -2.35], l: [-0.35, 0.8, -2.88], mm: 36 }, { t: dur, p: [-0.3, 1.38, -2.5], l: [-0.32, 0.79, -2.88], mm: 42 }],
    c: [{ t: 0, p: [1.15, 1.32, -2.35], l: [0.5, 1.05, -3.5], mm: 34 }, { t: dur, p: [0.9, 1.27, -2.55], l: [0.5, 1.08, -3.52], mm: 42 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const mk = opt.mark !== undefined ? opt.mark : 1.0; drawM(Math.max(0, Math.min(1, (t - mk) / Math.max(4, dur * 0.75))));
    const ty = opt.type !== undefined ? opt.type : 0.5; const tu = Math.max(0, Math.min(1, (t - ty) / Math.max(5, dur * 0.85))); drawT(tu); tw.position.x = 0.5 + 0.08 * (0.5 - (tu * 9 % 1));
    const typing = v === 'c' && tu > 0 && tu < 1; tr.set({ armR: typing ? -1.2 + 0.1 * Math.sin(t * 14) : -1.0 + 0.06 * Math.sin(t * 1.6), armL: typing ? -1.2 + 0.1 * Math.sin(t * 13 + 1) : -0.9, headTilt: 0.45 });
    others.forEach((p, i) => p.set({ armR: -1.1 + 0.1 * Math.sin(t * (6 + i) + i), armL: -1.0 + 0.08 * Math.sin(t * (5 + i)), headTilt: 0.35 }));
  };
  return { scene, cam: rig.cam, update, grade: 'sepia', exposure: 1.05 };
}

// ===== studio: bàn người dịch hôm nay, ban ngày =====
async function studio({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#c8d2dc', 0.012);
  scene.add(new THREE.HemisphereLight('#f4f8ff', '#8a8070', 1.15));
  box(14, 0.1, 12, std('#ffffff', { map: rep(woodTex(111, [168, 128, 88], 10), 4, 3), roughness: 0.55 }), 0, 0, -2);
  const rug = canvasTex(256, 256, (g, w, h) => { const R = rng(113); g.fillStyle = '#3e5a6a'; g.fillRect(0, 0, w, h); g.strokeStyle = '#d8c8a0'; g.lineWidth = 6; g.strokeRect(14, 14, w - 28, h - 28); for (let n = 0; n < 1500; n++) { g.fillStyle = `rgba(${R() < 0.5 ? '255,255,255' : '0,0,0'},0.06)`; g.fillRect(R() * w, R() * h, 2, 2); } });
  box(3.6, 0.02, 2.6, std('#ffffff', { map: rug, roughness: 0.95 }), 0, 0.06, -1.6);
  box(14, 3.2, 0.3, std('#ffffff', { map: rep(plasterTex('#e8e4dc', 7), 4, 1) }), 0, 1.6, -6); box(0.3, 3.2, 12, std('#e4e0d6'), 6, 1.6, -2); box(14, 0.2, 12, std('#f4f2ec'), 0, 3.2, -2);
  // cửa sổ lớn (tường trái), phố ban ngày ngoài kính
  const city = canvasTex(1024, 512, (g, w, h) => { const R = rng(117); const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#8ab4e0'); gr.addColorStop(0.7, '#d4e4f2'); gr.addColorStop(1, '#e8eef2'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let b = 0; b < 18; b++) { const x = R() * w, bw = 60 + R() * 110, bh = 140 + R() * 300, c = ['#c8b8a0', '#a8a8b0', '#d8ccb8', '#9aa4b0'][b % 4]; g.fillStyle = c; g.fillRect(x, h - bh, bw, bh); g.fillStyle = 'rgba(60,80,100,0.45)'; for (let yy = h - bh + 10; yy < h - 8; yy += 18) for (let xx = x + 6; xx < x + bw - 8; xx += 14) g.fillRect(xx, yy, 8, 10); }
    g.fillStyle = '#4a7a4a'; for (let k = 0; k < 14; k++) { g.beginPath(); g.arc(R() * w, h - 10, 20 + R() * 30, 0, 7); g.fill(); } });
  box(0.05, 2.4, 5.2, basic('#ffffff', { map: city }), -6.6, 1.7, -2.4); box(0.3, 3.2, 12, std('#e4e0d6'), -6.2, 1.6, -2).visible = false;
  for (const z of [-4.9, -2.4, 0.1]) box(0.12, 2.5, 0.1, std('#f0f0ec'), -6.15, 1.7, z); box(0.15, 0.12, 5.2, std('#f0f0ec'), -6.15, 0.45, -2.4); box(0.15, 0.12, 5.2, std('#f0f0ec'), -6.15, 2.95, -2.4);
  box(0.3, 0.45, 12, std('#e4e0d6'), -6.2, 0.22, -2); box(0.3, 0.25, 12, std('#e4e0d6'), -6.2, 3.07, -2); box(0.3, 3.2, 3.3, std('#e4e0d6'), -6.2, 1.6, 2.6); box(0.3, 3.2, 1.0, std('#e4e0d6'), -6.2, 1.6, -5.5);
  const sun = new THREE.DirectionalLight('#fff4e0', 3.2); sun.position.set(-12, 7, -1); sun.target.position.set(0, 0.6, -2.5); scene.add(sun, sun.target); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 6, bottom: -6 });
  const skyL = new THREE.PointLight('#dceaff', 5, 10, 1.2); skyL.position.set(-4.5, 2.2, -2.4); scene.add(skyL);
  // kệ sách từ điển (tường sau), cây xanh, tranh, ghế đọc
  const sh = box(3.4, 2.4, 0.4, std('#ffffff', { map: rep(spinesTex(119), 1.2, 1), roughness: 0.85 }), 2.6, 1.2, -5.7); box(3.5, 0.08, 0.45, std('#f0ece4'), 2.6, 2.44, -5.7);
  const plant = (x, z, s) => { cyl(0.18 * s, 0.14 * s, 0.32 * s, std('#c87a4a', { roughness: 0.7 }), x, 0.16 * s, z); for (let k = 0; k < 9; k++) { const l = new THREE.Mesh(new THREE.SphereGeometry(0.16 * s, 10, 8), std(k % 2 ? '#3f7a44' : '#4e8c50', { roughness: 0.7 })); l.scale.set(1, 0.4, 0.6); l.position.set(x + 0.18 * s * Math.cos(k * 0.7), (0.4 + 0.09 * k) * s, z + 0.18 * s * Math.sin(k * 1.3)); l.rotation.z = 0.5 * Math.sin(k); scene.add(l); } };
  plant(-5.4, -5.0, 2.2); plant(-1.5, -5.4, 1.4);
  const art = canvasTex(256, 192, (g, w, h) => { g.fillStyle = '#f2ece0'; g.fillRect(0, 0, w, h); g.fillStyle = '#d88a4a'; g.beginPath(); g.arc(90, 90, 46, 0, 7); g.fill(); g.fillStyle = '#3e5a6a'; g.fillRect(130, 40, 90, 110); g.strokeStyle = '#2a2a2a'; g.lineWidth = 6; g.strokeRect(3, 3, w - 6, h - 6); });
  box(1.4, 1.05, 0.04, std('#ffffff', { map: art }), -1.2, 2.0, -5.83);
  // bàn làm việc: hai màn hình (nguồn | bản nháp máy đang sửa), bàn phím, chuột, cốc, sổ, tai nghe, đèn bàn
  const SRC = ['Die Untersuchung wurde an 412 Patienten', 'durchgeführt. Die Ergebnisse zeigen eine', 'deutliche Verbesserung nach sechs Wochen.', 'Nebenwirkungen traten selten auf und', 'waren überwiegend leicht.', 'Weitere Studien sind erforderlich, um', 'die Langzeitwirkung zu bewerten.', 'Die Dosierung richtet sich nach dem', 'Körpergewicht des Patienten.'];
  const MTX = ['The investigation was carried out on 412 patients.', 'The results show a clear improvement after six weeks.', 'Side effects occurred rarely and were mostly light.', 'Further studies are required to evaluate the long-term effect.', 'The dosage depends on the body weight of the patient.'];
  const FIXD = ['The study was carried out in 412 patients.', 'The results show a clear improvement after six weeks.', 'Side effects were rare and mostly mild.', 'Further studies are needed to assess long-term effects.', "Dosage is based on the patient's body weight."];
  const sc = document.createElement('canvas'); sc.width = 1280; sc.height = 800; const sg = sc.getContext('2d'); const sT = new THREE.CanvasTexture(sc); sT.colorSpace = THREE.SRGBColorSpace; sT.anisotropy = 8; let lastS = -1;
  const drawS = (u, scroll) => { const key = Math.round(u * 200) * 100 + Math.round(scroll * 10); if (key === lastS) return; lastS = key;
    sg.fillStyle = '#f6f7f9'; sg.fillRect(0, 0, 1280, 800); sg.fillStyle = '#2e3a4a'; sg.fillRect(0, 0, 1280, 56); sg.fillStyle = '#e8eef6'; sg.font = 'bold 24px DejaVu Sans'; sg.fillText('Translation editor   ·   DE → EN   ·   segment review', 24, 37);
    sg.fillStyle = '#e4e8ee'; sg.fillRect(0, 56, 640, 744); sg.fillStyle = '#5a6a7e'; sg.font = 'bold 20px DejaVu Sans'; sg.fillText('SOURCE', 30, 92); sg.fillText('MACHINE DRAFT → REVIEWED', 670, 92);
    const n = u * MTX.length; for (let i = 0; i < MTX.length; i++) { const y = 140 + i * 128 - scroll * 20; const cur = i === Math.min(MTX.length - 1, Math.floor(n));
      if (cur) { sg.fillStyle = 'rgba(255,196,90,0.28)'; sg.fillRect(650, y - 34, 620, 112); sg.fillStyle = '#f0a030'; sg.fillRect(650, y - 34, 6, 112); }
      sg.fillStyle = '#2a3442'; sg.font = '22px DejaVu Sans'; const sp = [[0, 1], [1, 2], [3, 4], [5, 6], [7, 8]][i]; sg.fillText(SRC[sp[0]], 30, y); sg.fillText(SRC[sp[1]], 30, y + 32);
      const q = Math.max(0, Math.min(1, n - i)); const done = q >= 1; const txt = done ? FIXD[i] : MTX[i];
      sg.fillStyle = done ? '#1e5a36' : '#3a4a5e'; sg.font = (done ? '' : 'italic ') + '22px DejaVu Sans'; const words = txt.split(' '); let line = '', yy = y; for (const w of words) { if (sg.measureText(line + w).width > 580) { sg.fillText(line, 670, yy); yy += 32; line = ''; } line += w + ' '; } sg.fillText(line, 670, yy);
      sg.fillStyle = done ? '#2e8a4e' : '#8a96a8'; sg.font = 'bold 18px DejaVu Sans'; sg.fillText(done ? '✓ reviewed' : (cur ? 'editing…' : 'MT draft'), 1130, y + 64);
      if (cur && !done) { const blink = (Math.floor(u * 400) % 2) === 0; if (blink) { sg.fillStyle = '#2a3442'; sg.fillRect(670 + Math.min(560, q * 560), y - 20, 3, 28); } } }
    sT.needsUpdate = true; };
  drawS(0, 0);
  const srcOnly = canvasTex(1280, 800, (g, w, h) => { g.fillStyle = '#fbfaf6'; g.fillRect(0, 0, w, h); g.fillStyle = '#2e3a4a'; g.fillRect(0, 0, w, 56); g.fillStyle = '#e8eef6'; g.font = 'bold 24px DejaVu Sans'; g.fillText('Reference · glossary · style guide', 24, 37);
    g.fillStyle = '#2a3442'; g.font = '24px DejaVu Serif'; SRC.forEach((s, i) => g.fillText(s, 40, 120 + i * 44)); g.fillStyle = '#5a6a7e'; g.font = 'bold 22px DejaVu Sans'; g.fillText('Glossary', 40, 560); g.font = '22px DejaVu Sans'; [['Nebenwirkungen', 'side effects'], ['Dosierung', 'dosage'], ['Langzeitwirkung', 'long-term effect']].forEach(([a, b], i) => g.fillText(a + '  →  ' + b, 40, 600 + i * 36)); });
  const deskW = std('#ffffff', { map: rep(woodTex(121, [196, 160, 118], 3), 1.5, 1), roughness: 0.45 }), legM = std('#2a2c30', { metalness: 0.6, roughness: 0.4 });
  const D = new THREE.Group(); D.position.set(0, 0, -2.6); scene.add(D);
  box(2.0, 0.05, 0.9, deskW, 0, 0.74, 0, D); for (const x of [-0.95, 0.95]) box(0.05, 0.72, 0.8, legM, x, 0.36, 0, D);
  const scrM = basic('#ffffff', { map: sT }); const m1 = box(0.82, 0.52, 0.025, scrM, 0.42, 1.14, -0.24, D); m1.rotation.y = -0.18; const m2 = box(0.82, 0.52, 0.025, basic('#ffffff', { map: srcOnly }), -0.45, 1.14, -0.26, D); m2.rotation.y = 0.14;
  for (const [x, ry] of [[0.42, -0.18], [-0.45, 0.14]]) { const bz = box(0.86, 0.56, 0.02, std('#1a1c20'), x, 1.14, -0.255 - (x > 0 ? 0 : 0.02), D); bz.rotation.y = ry; box(0.05, 0.3, 0.05, legM, x, 0.9, -0.27, D); box(0.24, 0.02, 0.18, legM, x, 0.77, -0.27, D); }
  box(0.46, 0.02, 0.15, std('#e8e8e4'), 0, 0.775, 0.14, D); box(0.06, 0.03, 0.1, std('#e8e8e4'), 0.38, 0.78, 0.15, D);
  cyl(0.045, 0.04, 0.1, std('#d85a3a', { roughness: 0.4 }), -0.75, 0.81, 0.2, D); box(0.22, 0.02, 0.3, std('#2a4a6a'), -0.5, 0.78, 0.18, D).rotation.y = 0.3; headphones(D, 0.8, 0.8, 0.15, 0.9, '#3a3a40').rotation.x = -Math.PI / 2;
  const books = [['#7a2a22', 0.06], ['#2e4a3a', 0.05], ['#34405e', 0.07]]; books.forEach(([c, th], i) => box(0.24, th, 0.32, std(c), -0.82, 0.79 + i * 0.065, -0.18, D));
  const dlamp = new THREE.Group(); dlamp.position.set(0.85, 0.77, -0.25); D.add(dlamp); cyl(0.07, 0.08, 0.02, legM, 0, 0, 0, dlamp); const a1 = cyl(0.008, 0.008, 0.4, legM, 0.02, 0.2, 0, dlamp); a1.rotation.z = 0.15; const sh2 = cyl(0.04, 0.09, 0.1, std('#e8e4dc', { side: THREE.DoubleSide }), -0.08, 0.42, 0.04, dlamp); sh2.rotation.z = 0.7;
  const lg = glowSprite('#ffe2b0', 0.7, 0.35); lg.position.set(-0.1, 0.37, 0.05); dlamp.add(lg); const lgL = new THREE.PointLight('#ffe0b0', 2, 2.2, 1.6); lgL.position.set(-0.1, 0.33, 0.1); dlamp.add(lgL);
  const scrL = new THREE.PointLight('#e8f0ff', 2.6, 2.8, 1.6); scrL.position.set(0, 1.1, 0.3); D.add(scrL);
  const chair = new THREE.Group(); chair.position.set(0, 0, 0.75); D.add(chair); box(0.55, 0.06, 0.5, std('#3a3e44'), 0, 0.48, 0, chair); box(0.55, 0.6, 0.06, std('#3a3e44'), 0, 0.85, 0.24, chair); cyl(0.03, 0.03, 0.45, legM, 0, 0.24, 0, chair);
  const tr = seated('#32363e', 1.0, '#eaf2ff'); tr.root.position.set(0, 0, 0.72); tr.root.rotation.y = Math.PI; D.add(tr.root);
  const dst = dust(scene, [-3, 1.6, -2.4], [4, 2, 4], 200, 123, '#fff8e8');
  const K = {
    a: [{ t: 0, p: [2.8, 1.7, 4.5], l: [-0.3, 1.0, -2.8], mm: 28 }, { t: dur, p: [1.2, 1.55, 0.9], l: [0.0, 1.0, -2.8], mm: 32 }],
    b: [{ t: 0, p: [-0.5, 1.5, -1.45], l: [0.42, 1.12, -2.86], mm: 34 }, { t: dur, p: [-0.15, 1.42, -1.75], l: [0.42, 1.12, -2.86], mm: 42 }],
    c: [{ t: 0, p: [-4.6, 1.3, 1.8], l: [0.2, 1.0, -2.8], mm: 30 }, { t: dur, p: [-3.6, 1.35, 0.5], l: [0.3, 1.05, -2.8], mm: 34 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const et = opt.edit !== undefined ? opt.edit : 0.5; const eu = Math.max(0, Math.min(1, (t - et) / Math.max(6, dur * 0.9))); drawS(eu, 0);
    tr.set({ armR: -1.05 + 0.06 * Math.sin(t * 9), armL: -1.0 + 0.05 * Math.sin(t * 8.3 + 1), headTilt: 0.05 + 0.03 * Math.sin(t * 0.6) });
  };
  return { scene, cam: rig.cam, update, grade: 'cold', exposure: 1.15 };
}

// ===== vrs: buồng phiên dịch từ xa / video relay, ban ngày =====
async function vrs({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#c4ccd6', 0.014);
  scene.add(new THREE.HemisphereLight('#eef4ff', '#6a6458', 1.1));
  box(10, 0.1, 10, std('#ffffff', { map: rep(canvasTex(256, 256, (g, w, h) => { const R = rng(131); g.fillStyle = '#5a6470'; g.fillRect(0, 0, w, h); for (let n = 0; n < 3000; n++) { g.fillStyle = `rgba(${R() < 0.5 ? '255,255,255' : '0,0,0'},0.07)`; g.fillRect(R() * w, R() * h, 2, 2); } }), 6, 6), roughness: 0.95 }), 0, 0, -1);
  // tường tiêu âm (ô xốp kim tự tháp có màu), tường sau xám ấm
  const foam = canvasTex(256, 256, (g, w, h) => { for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const x = i * 64, y = j * 64; const c = (i + j) % 2 ? '#3a5a6e' : '#4a6a7e'; g.fillStyle = c; g.fillRect(x, y, 64, 64); g.fillStyle = 'rgba(255,255,255,0.12)'; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 32, y + 32); g.lineTo(x + 64, y); g.fill(); g.fillStyle = 'rgba(0,0,0,0.18)'; g.beginPath(); g.moveTo(x, y + 64); g.lineTo(x + 32, y + 32); g.lineTo(x + 64, y + 64); g.fill(); } });
  box(10, 3.0, 0.3, std('#ffffff', { map: rep(plasterTex('#d4ccc0', 11), 3, 1) }), 0, 1.5, -4.5);
  for (const [x, z, ry, w] of [[0, -4.33, 0, 4.6], [4.8, -1, -Math.PI / 2, 5]]) { const p = box(w, 1.8, 0.06, std('#ffffff', { map: rep(foam, w / 1.2, 1.5), roughness: 0.95 }), x, 1.7, z); p.rotation.y = ry; }
  box(0.3, 3.0, 10, std('#d4ccc0'), 5, 1.5, -1); box(10, 0.2, 10, std('#ecebe8'), 0, 3.0, -1);
  // cửa sổ (tường trái), ban ngày
  const out = canvasTex(512, 384, (g, w, h) => { const R = rng(137); const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#9cc4ea'); gr.addColorStop(1, '#e4eef6'); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = '#5a8a5a'; for (let k = 0; k < 10; k++) { g.beginPath(); g.arc(R() * w, h - 40 + R() * 30, 30 + R() * 40, 0, 7); g.fill(); } g.fillStyle = '#c8b8a0'; g.fillRect(300, 120, 120, 264); g.fillStyle = 'rgba(60,80,100,0.4)'; for (let y = 140; y < 370; y += 22) for (let x = 312; x < 410; x += 18) g.fillRect(x, y, 10, 12); });
  box(0.3, 3.0, 10, std('#d4ccc0'), -5, 1.5, -1).visible = false; box(0.05, 1.6, 2.4, basic('#ffffff', { map: out }), -5.1, 1.7, -1.5);
  box(0.3, 0.9, 10, std('#d4ccc0'), -5, 0.45, -1); box(0.3, 0.5, 10, std('#d4ccc0'), -5, 2.75, -1); box(0.3, 1.6, 3.3, std('#d4ccc0'), -5, 1.7, -4.4); box(0.3, 1.6, 4.3, std('#d4ccc0'), -5, 1.7, 2.85);
  const sun = new THREE.DirectionalLight('#fff4e0', 2.4); sun.position.set(-10, 6, -1); sun.target.position.set(0, 0.8, -2); scene.add(sun, sun.target); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -6, right: 6, top: 5, bottom: -5 });
  const ceil = new THREE.PointLight('#f4f8ff', 6, 9, 1.2); ceil.position.set(0, 2.8, -1); scene.add(ceil);
  // đèn vòng (ring light), đèn "IN SESSION"
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.025, 10, 40), basic('#fffaf0')); ring.position.set(-1.1, 1.45, -3.2); ring.rotation.y = 0.5; scene.add(ring); cyl(0.01, 0.01, 1.45, std('#2a2a2e', { metalness: 0.6 }), -1.1, 0.72, -3.2); const rl = new THREE.PointLight('#fffaf0', 2.5, 3.5, 1.5); rl.position.set(-1.0, 1.45, -3.0); scene.add(rl);
  const sess = canvasTex(256, 64, (g, w, h) => { g.fillStyle = '#5a1a14'; g.fillRect(0, 0, w, h); g.fillStyle = '#ffd8c8'; g.font = 'bold 30px DejaVu Sans'; g.textAlign = 'center'; g.fillText('IN SESSION', w / 2, 43); });
  const sessM = basic('#ffffff', { map: sess }); box(0.7, 0.18, 0.04, sessM, 1.6, 2.5, -4.32); const sessG = glowSprite('#ff7a5a', 0.6, 0.9); sessG.position.set(1.6, 2.5, -4.2); scene.add(sessG);
  // màn hình gọi video: người ra dấu cách điệu (không mặt), khung tự xem nhỏ
  const vc = document.createElement('canvas'); vc.width = 1280; vc.height = 760; const vg = vc.getContext('2d'); const vT = new THREE.CanvasTexture(vc); vT.colorSpace = THREE.SRGBColorSpace; vT.anisotropy = 8;
  const drawV = (t) => { vg.fillStyle = '#1c2430'; vg.fillRect(0, 0, 1280, 760); const gr = vg.createLinearGradient(0, 60, 0, 700); gr.addColorStop(0, '#6a7e94'); gr.addColorStop(1, '#3a4656'); vg.fillStyle = gr; vg.fillRect(40, 60, 1200, 640);
    vg.fillStyle = '#c8a888'; vg.fillRect(860, 120, 260, 200); vg.fillStyle = '#4a6a4a'; vg.beginPath(); vg.arc(1000, 230, 50, 0, 7); vg.fill();   // tranh sau người ra dấu
    const cx = 640, cy = 420; vg.fillStyle = '#26303e'; vg.beginPath(); vg.ellipse(cx, cy + 210, 230, 200, 0, Math.PI, 0); vg.fill(); vg.fillRect(cx - 230, cy + 210, 460, 90);
    vg.fillStyle = '#b08a70'; vg.beginPath(); vg.ellipse(cx, cy - 40, 78, 96, 0, 0, 7); vg.fill(); vg.fillStyle = '#2a1e18'; vg.beginPath(); vg.ellipse(cx, cy - 90, 86, 60, 0, Math.PI, 0); vg.fill();
    const hand = (side, ph) => { const hx = cx + side * (120 + 70 * Math.sin(t * 2.6 + ph)), hy = cy + 60 + 70 * Math.sin(t * 3.3 + ph * 1.7); vg.strokeStyle = '#26303e'; vg.lineWidth = 46; vg.lineCap = 'round'; vg.beginPath(); vg.moveTo(cx + side * 190, cy + 150); vg.lineTo(hx, hy); vg.stroke();
      vg.fillStyle = '#b08a70'; vg.beginPath(); vg.ellipse(hx, hy, 34, 42, 0.6 * Math.sin(t * 4 + ph), 0, 7); vg.fill(); for (let k = 0; k < 4; k++) { vg.fillRect(hx - 24 + k * 14, hy - 62 - 8 * Math.sin(t * 6 + k + ph), 9, 30); } };
    hand(-1, 0); hand(1, 1.3);
    vg.fillStyle = '#0e1218'; vg.fillRect(40, 660, 1200, 40); vg.fillStyle = '#e8eef6'; vg.font = 'bold 22px DejaVu Sans'; vg.fillText('VIDEO RELAY  ·  connected', 60, 688); vg.fillStyle = '#e04a3a'; vg.beginPath(); vg.arc(1210, 680, 8, 0, 7); vg.fill();
    vg.fillStyle = '#2a3442'; vg.fillRect(980, 470, 230, 160); vg.fillStyle = '#4a5a6e'; vg.fillRect(990, 480, 210, 140); vg.fillStyle = '#1e242c'; vg.beginPath(); vg.ellipse(1095, 600, 60, 40, 0, Math.PI, 0); vg.fill(); vg.beginPath(); vg.arc(1095, 540, 28, 0, 7); vg.fill();
    vT.needsUpdate = true; };
  drawV(0);
  const D = new THREE.Group(); D.position.set(0, 0, -2.8); scene.add(D);
  const deskW = std('#ffffff', { map: rep(woodTex(141, [176, 140, 100], 3), 1.5, 1), roughness: 0.45 }), legM = std('#2a2c30', { metalness: 0.6, roughness: 0.4 });
  box(1.9, 0.05, 0.85, deskW, 0, 0.74, 0, D); for (const x of [-0.9, 0.9]) box(0.05, 0.72, 0.75, legM, x, 0.36, 0, D);
  const mon = box(1.1, 0.65, 0.03, basic('#ffffff', { map: vT }), 0.05, 1.2, -0.26, D); box(1.14, 0.69, 0.02, std('#15171a'), 0.05, 1.2, -0.28, D); box(0.06, 0.3, 0.05, legM, 0.05, 0.9, -0.28, D);
  const cam = box(0.1, 0.04, 0.05, std('#1a1a1e'), 0.05, 1.56, -0.25, D);
  box(0.42, 0.02, 0.14, std('#2a2c30'), 0, 0.775, 0.12, D); cyl(0.04, 0.035, 0.1, std('#ffffff', { roughness: 0.3 }), -0.7, 0.81, 0.15, D);
  const nb = box(0.24, 0.015, 0.32, std('#f0e8d0'), 0.6, 0.775, 0.15, D); nb.rotation.y = -0.3;
  const scrL = new THREE.PointLight('#dce8ff', 3, 2.8, 1.6); scrL.position.set(0.05, 1.2, 0.3); D.add(scrL);
  const it = seated('#2e3440', 1.0, '#eaf2ff'); it.root.position.set(0, 0, 0.72); it.root.rotation.y = Math.PI; D.add(it.root); headphones(it.root, 0, 1.17, 0, 1.0, '#202024');
  const boom = cyl(0.006, 0.006, 0.22, std('#202024'), 0.12, 1.06, -0.1, it.root); boom.rotation.x = 1.2; boom.rotation.z = -0.3;
  const dst = dust(scene, [-2.5, 1.6, -1.5], [3, 2, 3], 160, 143, '#fff8e8');
  const K = {
    a: [{ t: 0, p: [3.2, 1.8, 3.6], l: [-0.2, 1.1, -3.0], mm: 28 }, { t: dur, p: [1.6, 1.6, 1.2], l: [0.0, 1.15, -3.1], mm: 32 }],
    b: [{ t: 0, p: [0.75, 1.55, -1.3], l: [0.05, 1.2, -3.06], mm: 34 }, { t: dur, p: [0.45, 1.5, -1.6], l: [0.05, 1.2, -3.06], mm: 40 }],
    c: [{ t: 0, p: [-4.0, 1.4, 1.5], l: [0.0, 1.1, -3.0], mm: 30 }, { t: dur, p: [-3.2, 1.45, 0.6], l: [0.1, 1.15, -3.0], mm: 34 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t); drawV(t);
    it.set({ armR: -0.9 + 0.2 * Math.sin(t * 2.6), armL: -0.8 + 0.2 * Math.sin(t * 3.1 + 1), headTilt: 0.02 + 0.03 * Math.sin(t * 0.8) });
    sessG.material.opacity = 0.6 * (1 + 0.05 * Math.sin(f * 0.2));
  };
  return { scene, cam: rig.cam, update, grade: 'cold', exposure: 1.1 };
}

export const HEROES = { library, booths, ibm, postedit, studio, vrs };

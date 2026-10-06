// Last Lamplighters · Tập 6 "The Hand That Drew It" — CẢNH ĐINH 3D (dựng riêng, không lặp bố cục cảnh đinh tập trước).
//   printshop  ngoài phố: xưởng in tầng hầm + cửa sổ tầng trên (bàn vẽ, màn hình). Biến thể a: đẩy máy vào cửa sổ (móc câu) · b: hạ máy xuống bậc hầm (vào truyện) · c: cầu nối 06 (người thắp đèn đi qua, cửa sổ đổi từ đèn bàn sang màn hình) · d: kết (cẩu máy lên mái)
//   cellar     trong hầm: khay chữ chì dưới đèn treo, tay cầm sắp chữ đầy dần chữ — a: trượt ngang · b: cận khay chữ (sepia)
//   linotype   phòng sắp chữ: hàng máy Linotype, nồi chì đỏ, người vận hành (bóng), đèn treo chao xanh — a: lia dọc hàng · b: góc cao
//   drafts     xưởng thiết kế hôm nay: bức tường màn hình, bản nháp hiện dần hàng chục ô, người thiết kế (bóng) — a: đẩy chậm · b: ngược sáng từ sau lưng
import { THREE, useScene, gasLamp, figure, dust, camRig, box, cyl, lam, std, glowSprite, rng, ease, lerp, canvasTex } from './kit.js';

const fogOf = (scene, color, d) => { useScene(scene); scene.fog = new THREE.FogExp2(color, d); scene.background = new THREE.Color(color); };

// mặt tiền gạch có mạch vữa (kết cấu canvas)
const brickTex = (seed, base = '#5a3326') => canvasTex(512, 512, (g, w, h) => {
  const R = rng(seed); g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let y = 0, r = 0; y < h; y += 16, r++) for (let x = -(r % 2) * 16; x < w; x += 32) {
    const k = 0.82 + R() * 0.3; g.fillStyle = `rgb(${Math.round(110 * k)},${Math.round(58 * k)},${Math.round(42 * k)})`; g.fillRect(x + 1, y + 1, 30, 14); }
  g.fillStyle = 'rgba(0,0,0,0.25)'; for (let i = 0; i < 40; i++) g.fillRect(R() * w, R() * h, 2 + R() * 60, 1 + R() * 3);
});

// ===== printshop: phố, xưởng in, cửa sổ tầng trên =====
async function printshop({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, v === 'd' ? '#1f2438' : '#2c2739', 0.022);
  const R = rng(61), bt = brickTex(3); bt.wrapS = bt.wrapT = THREE.RepeatWrapping; bt.repeat.set(3, 3);
  const sky = new THREE.Mesh(new THREE.SphereGeometry(180, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, map: canvasTex(8, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#121931'); gr.addColorStop(0.42, '#352f52'); gr.addColorStop(0.5, '#7a5266'); gr.addColorStop(0.53, '#2a2232'); gr.addColorStop(1, '#1a1620'); g.fillStyle = gr; g.fillRect(0, 0, w, h); }) }));
  scene.add(sky);
  // mặt đường + vỉa hè có hố bậc hầm (areaway) trước xưởng in: x 2.1–4.7, z 0.2–2.4
  const road = std('#2c2b30', { roughness: 0.95 }), walk = std('#56514d', { roughness: 0.9 });
  box(80, 0.1, 40, road, 0, -0.05, 23.5); box(80, 0.1, 4, road, 0, -0.05, -2);                 // lòng đường (trước/sau)
  box(40, 0.2, 3.6, walk, -17.9, 0.05, 1.8); box(40, 0.2, 3.6, walk, 24.7, 0.05, 1.8);          // vỉa hè hai bên hố
  box(2.6, 0.2, 1.2, walk, 3.4, 0.05, 3.0);                                                      // vỉa hè trước hố
  const pitM = std('#2b2420', { roughness: 0.95 });
  box(2.6, 2.6, 0.12, pitM, 3.4, -1.2, 2.42); box(0.12, 2.6, 2.3, pitM, 2.1, -1.2, 1.3); box(0.12, 2.6, 2.3, pitM, 4.7, -1.2, 1.3); box(2.6, 0.1, 2.3, pitM, 3.4, -2.5, 1.3);
  for (let i = 0; i < 9; i++) box(1.2, 0.2, 0.26, std('#4d4844'), 3.9, -0.1 - i * 0.26, 2.25 - i * 0.24);   // bậc xuống
  for (let i = 0; i <= 8; i++) cyl(0.015, 0.015, 0.9, std('#1d1d22', { metalness: 0.6 }), 2.2 + i * 0.3, 0.6, 2.45);   // lan can sắt
  box(2.5, 0.03, 0.03, std('#1d1d22', { metalness: 0.6 }), 3.4, 1.05, 2.45);
  // mặt tiền 3 tầng
  const front = new THREE.Group(); scene.add(front); const fm = std('#ffffff', { map: bt, roughness: 0.9 });
  box(12, 6.55, 0.6, fm, 0, 3.275, -0.3, front); box(12, 2.35, 0.6, fm, 0, 9.825, -0.3, front); box(4.7, 2.1, 0.6, fm, -3.65, 7.6, -0.3, front); box(4.7, 2.1, 0.6, fm, 3.65, 7.6, -0.3, front);
  box(12.4, 0.35, 0.9, std('#2f2622'), 0, 11.1, -0.2, front);
  const winFrame = (x, y, w, h) => { box(w + 0.24, 0.14, 0.2, std('#d9cfbd'), x, y - h / 2 - 0.1, 0.05, front); box(w + 0.3, 0.18, 0.18, std('#d9cfbd'), x, y + h / 2 + 0.12, 0.05, front);
    box(0.06, h, 0.1, std('#2a1d16'), x, y, 0.05, front); box(w, 0.06, 0.1, std('#2a1d16'), x, y + h * 0.15, 0.05, front); };
  const glass = (x, y, w, h, col, op) => { const m = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op }); box(w, h, 0.02, m, x, y, 0.03, front); winFrame(x, y, w, h); return m; };
  for (const [x, y] of [[-4, 4.4], [4, 4.4], [-4, 7.6], [4, 7.6]]) { const on = R() < 0.5; glass(x, y, 1.6, 2.0, on ? '#c48b4c' : '#0e0d12', on ? 0.85 : 0.95); }
  // phòng thiết kế sau cửa sổ giữa tầng 2: tường sau sáng, bàn vẽ nghiêng, đèn kẹp, màn hình
  const designGlass = glass(0, 7.6, 2.6, 2.1, '#8a7a66', 0.12);
  const room = new THREE.Group(); room.position.set(0, 7.6, -0.6); front.add(room);
  // phòng thụt vào trong tường: tường sau + hai vách + trần + sàn (chỉ thấy qua ô cửa)
  const roomM = std('#b9a07a', { roughness: 0.9 }); box(2.8, 2.4, 0.1, roomM, 0, 0, -2.4, room); box(0.1, 2.4, 2.4, roomM, -1.4, 0, -1.2, room); box(0.1, 2.4, 2.4, roomM, 1.4, 0, -1.2, room);
  box(2.8, 0.1, 2.4, std('#3a2c22'), 0, -1.2, -1.2, room); box(2.8, 0.1, 2.4, std('#8f7a5e'), 0, 1.2, -1.2, room);
  const board = box(1.3, 0.05, 0.85, std('#e7dfc8'), -0.35, -0.45, -1.1, room); board.rotation.x = 0.75;
  const sheet = box(0.9, 0.06, 0.6, std('#f4eedd'), -0.35, -0.42, -1.08, room); sheet.rotation.x = 0.75;
  const designer = figure({ seated: true, scale: 0.78 }); designer.root.position.set(-0.3, -1.15, -0.25); designer.root.rotation.y = Math.PI; room.add(designer.root);
  const screen = box(0.62, 0.4, 0.03, new THREE.MeshBasicMaterial({ color: '#2a3448' }), 0.85, -0.55, -1.6, room); screen.rotation.y = -0.4;
  const roomLamp = new THREE.PointLight('#ffc68a', 14, 5, 1.4); roomLamp.position.set(-0.7, 0.5, -0.8); room.add(roomLamp);
  const scrLight = new THREE.PointLight('#8fb8ff', 0, 3, 1.6); scrLight.position.set(0.8, -0.3, -1.2); room.add(scrLight);
  // biển hiệu (tự thiết kế)
  box(6.2, 0.9, 0.12, new THREE.MeshBasicMaterial({ map: canvasTex(1024, 150, (g, w, h) => { g.fillStyle = '#1b2a22'; g.fillRect(0, 0, w, h);
    g.strokeStyle = '#b89b5e'; g.lineWidth = 6; g.strokeRect(10, 10, w - 20, h - 20); g.fillStyle = '#d9c38a'; g.font = 'bold 66px DejaVu Serif, serif'; g.textAlign = 'center'; g.fillText('PRINTING · COMPOSING', w / 2, 98); }) }), 1.8, 3.05, 0.12, front);   // lệch phải: ngọn đèn phố không che chữ ở mọi góc máy (xem trước 06/10)
  // cửa hàng tầng trệt (cửa kính tối), cửa hầm sáng ấm cuối bậc
  glass(-3.6, 1.3, 3.0, 1.8, '#3a2a1e', 0.9); box(1.1, 2.3, 0.08, std('#2a1d16'), -0.9, 1.15, 0.05, front);
  box(1.0, 1.9, 0.05, new THREE.MeshBasicMaterial({ color: '#d58e47' }), 3.4, -1.5, 0.22);          // cửa hầm sáng
  const cellarLight = new THREE.PointLight('#ffa65a', 9, 6, 1.4); cellarLight.position.set(3.4, -1.3, 1.0); scene.add(cellarLight);
  const spill = new THREE.SpotLight('#ffa65a', 40, 9, 0.7, 0.6, 1.3); spill.position.set(3.4, -1.6, 1.6); spill.target.position.set(3.4, 4, 0.2); scene.add(spill, spill.target);   // ánh hầm hắt lên lan can, mặt tiền
  // dãy nhà hai bên
  for (const sx of [-1, 1]) for (let k = 0; k < 3; k++) {
    const hh = 9 + R() * 6, xx = sx * (9.5 + k * 7.5), zz = -0.4 - k * 0.2; box(7, hh, 6, std(k % 2 ? '#3d3542' : '#47393a'), xx, hh / 2, zz - 3);
    for (let i = 0; i < 8; i++) { const on = R() < 0.35; box(0.9, 1.2, 0.05, new THREE.MeshBasicMaterial({ color: on ? '#b88446' : '#18161c' }), xx - 2.5 + (i % 4) * 1.6, 2.5 + Math.floor(i / 4) * 3.2, zz + 0.02); }
  }
  const lamp = gasLamp(scene, -2.2, 3.0, { lit: v === 'a' || v === 'd' ? 1 : 0 });
  const lighter = figure({ hat: true, scale: 1.0 }); scene.add(lighter.root);
  const pole = cyl(0.015, 0.015, 2.6, lam('#2a2016'), 0, -0.2, 0); lighter.armR.add(pole); pole.rotation.x = -0.25;
  scene.add(new THREE.HemisphereLight('#5a6690', '#1a1418', 0.9));
  const moon = new THREE.DirectionalLight('#8f9fd8', 0.6); moon.position.set(-20, 30, 25); scene.add(moon);
  const fill = new THREE.PointLight('#ffb070', 3, 18, 1.2); fill.position.set(-2.2, 3.5, 6); scene.add(fill);
  const dst = dust(scene, [-2.2, 2.9, 3.0], [2.2, 2.0, 2.2], 180, 11);
  const K = {
    a: [{ t: 0, p: [0.6, 3.4, 18], l: [0, 6.4, 0], mm: 30 }, { t: dur, p: [0.15, 7.3, 5.4], l: [-0.2, 7.3, -1.8], mm: 45 }],
    b: [{ t: 0, p: [-3.5, 1.65, 12.5], l: [-1.2, 2.6, 0], mm: 30 }, { t: dur, p: [0.5, 1.7, 11.0], l: [-0.2, 2.8, 0], mm: 32 }],
    c: [{ t: 0, p: [9, 1.8, 12], l: [0, 2.8, 0], mm: 32 }, { t: dur, p: [-2.5, 4.8, 9.5], l: [0, 7.3, -0.6], mm: 40 }],
    d: opt.lit !== undefined   // có opt.lit: giữ máy gần ngọn đèn tới lúc bén, rồi lùi và cẩu lên mái
      ? [{ t: 0, p: [-0.6, 1.7, 9.5], l: [-3.6, 2.4, 3.0], mm: 35 }, { t: opt.lit + 0.6, p: [0.2, 1.9, 9.0], l: [-2.4, 2.9, 3.0], mm: 38 }, { t: Math.min(dur - 2, opt.lit + 3), p: [0.8, 6, 15], l: [0, 6, 0], mm: 30 }, { t: dur, p: [1, 22, 28], l: [0, 6, -6], mm: 26 }]
      : [{ t: 0, p: [0.5, 1.8, 11], l: [-2.2, 3.1, 3.0], mm: 35 }, { t: dur * 0.5, p: [0.8, 6, 15], l: [0, 6, 0], mm: 30 }, { t: dur, p: [1, 22, 28], l: [0, 6, -6], mm: 26 }],
  }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    if (v === 'b' || v === 'c' || opt.lit !== undefined) {   // opt.lit: giây ngọn đèn bén (khớp tiếng xì đèn trong đặc tả); mặc định 0,45·dur + 1
      const tl = opt.lit !== undefined ? opt.lit : dur * 0.45 + 1.0, ta = tl - 1.0, u = Math.min(1, t / ta), x = lerp(-9, -2.7, ease(u)); lighter.root.position.set(x, 0.15, 2.6); lighter.root.rotation.y = Math.PI / 2;
      lighter.set({ walk: u < 1 ? t * 5 : 0, armR: u < 1 ? 0.2 : -2.4 * ease((t - ta) / 1.2) });
      lamp.set(ease((t - tl) / 1.0), f);
    } else { lighter.root.position.set(-2.9, 0.15, 2.7); lighter.root.rotation.y = 0.6; lighter.set({ armR: -0.3 }); lamp.set(1, f); }
    const u2 = v === 'c' ? ease((t - (opt.screen !== undefined ? opt.screen : dur * 0.55)) / 2.5) : v === 'a' ? 0.45 : 0;   // opt.screen: giây màn hình bừng lạnh
    screen.material.color.set(new THREE.Color('#2a3448').lerp(new THREE.Color('#a8cbff'), Math.max(u2, 0.2)));
    scrLight.intensity = 5 * u2; roomLamp.intensity = 7 * (1 - 0.5 * u2) * (1 + 0.02 * Math.sin(f * 0.4));
    designer.set({ armR: -0.9 + 0.08 * Math.sin(t * 2.2), armL: -0.7, headTilt: 0.25 });
    cellarLight.intensity = 9 * (1 + 0.05 * Math.sin(f * 0.37));
  };
  return { scene, cam: rig.cam, update, grade: 'warm' };
}

// ===== cellar: khay chữ chì =====
async function cellar({ W, H, dur, v, opt = {} }) {
  const scene = new THREE.Scene(); fogOf(scene, '#1a130e', 0.045);
  scene.add(new THREE.HemisphereLight('#8a6a50', '#140e0a', 0.75));
  const grain = canvasTex(256, 256, (g, w, h) => { const R = rng(5); g.fillStyle = '#7a4e2e'; g.fillRect(0, 0, w, h); for (let i = 0; i < 120; i++) { g.strokeStyle = `rgba(${40 + R() * 40},${20 + R() * 20},10,0.35)`; g.lineWidth = 1 + R() * 2; g.beginPath(); const y = R() * h; g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + R() * 8 - 4, w * 0.7, y + R() * 8 - 4, w, y + R() * 6 - 3); g.stroke(); } });
  const wood = std('#ffffff', { map: grain, roughness: 0.7 }), wood2 = std('#4a2d19'), lead = std('#7f858d', { metalness: 0.7, roughness: 0.4 });
  box(10, 5, 0.3, std('#6a5442'), 0, 2.5, -2.0); box(10, 0.1, 6, std('#3a3029'), 0, 0, 0); box(0.3, 5, 6, std('#5c4838'), -3.2, 2.5, 0);
  for (let i = 0; i < 4; i++) for (let j = 0; j < 6; j++) box(0.5, 0.08, 0.7, std('#5a3a22'), -2.2 + j * 0.62, 0.6 + i * 0.32, -1.6);   // kệ khay chữ phía sau
  const wallWash = new THREE.PointLight('#ffb070', 5, 6, 1.3); wallWash.position.set(-1.5, 2.6, -0.8); scene.add(wallWash);
  // một khay chữ lớn đặt nghiêng về phía máy quay trên giá
  const rack = new THREE.Group(); scene.add(rack); box(2.6, 0.95, 1.0, wood2, 0, 0.475, -0.4, rack);
  const cs = new THREE.Group(); cs.position.set(0, 1.08, -0.25); cs.rotation.x = 0.42; rack.add(cs);
  box(2.4, 0.08, 1.0, wood, 0, 0, 0, cs);
  const nx = 16, nz = 8; for (let i = 0; i <= nx; i++) box(0.022, 0.08, 1.0, wood2, -1.2 + i * (2.4 / nx), 0.07, 0, cs);
  for (let j = 0; j <= nz; j++) box(2.4, 0.08, 0.022, wood2, 0, 0.07, -0.5 + j * (1.0 / nz), cs);
  const R = rng(91); for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) { const n = 2 + Math.floor(R() * 5);
    for (let k = 0; k < n; k++) { const s = box(0.03, 0.035, 0.03, lead, -1.2 + (i + 0.25 + R() * 0.5) * (2.4 / nx), 0.06, -0.5 + (j + 0.25 + R() * 0.5) * (1.0 / nz), cs); s.castShadow = false; } }
  // tay cầm sắp chữ (composing stick) ở tiền cảnh, đầy dần chữ
  const stick = new THREE.Group(); stick.position.set(0.45, 1.28, 0.55); stick.rotation.set(0.25, -0.25, 0); scene.add(stick);
  const steel = std('#8f949a', { metalness: 0.7, roughness: 0.35 });
  box(0.7, 0.025, 0.13, steel, 0, 0, 0, stick); box(0.7, 0.07, 0.015, steel, 0, 0.035, -0.06, stick); box(0.02, 0.09, 0.13, steel, -0.34, 0.045, 0, stick);
  const sorts = []; for (let i = 0; i < 26; i++) { const s = box(0.024, 0.06, 0.11, lead, -0.32 + i * 0.026, 0.045, 0, stick); s.visible = false; sorts.push(s); }
  const hand = new THREE.Group(); scene.add(hand); const skin = lam('#3a2a20');
  box(0.11, 0.045, 0.16, skin, 0, 0, 0, hand); for (let i = 0; i < 4; i++) box(0.022, 0.026, 0.09, skin, -0.04 + i * 0.027, 0, 0.11, hand); box(0.025, 0.025, 0.08, skin, -0.07, 0, 0.03, hand).rotation.y = 0.7;
  cyl(0.06, 0.36, 0.24, std('#2f4a36', { side: THREE.DoubleSide }), 0, 2.45, 0.05); cyl(0.004, 0.004, 1.0, lam('#111'), 0, 3.05, 0.05);
  const bulb = new THREE.PointLight('#ffb468', 13, 6, 1.4); bulb.position.set(0, 2.3, 0.05); bulb.castShadow = true; bulb.shadow.mapSize.set(1024, 1024); bulb.shadow.radius = 4; scene.add(bulb);
  const g = glowSprite('#ffc27a', 1.0, 0.7); g.position.set(0, 2.3, 0.05); scene.add(g);
  const back = new THREE.PointLight('#d07a3a', 2.5, 8, 1.2); back.position.set(-3, 2.5, -1.5); scene.add(back);
  const dst = dust(scene, [0, 1.9, 0.1], [0.9, 0.7, 0.7], 120, 23);
  const K = { a: [{ t: 0, p: [-1.9, 1.75, 2.5], l: [0.1, 1.2, -0.6], mm: 32 }, { t: dur, p: [1.5, 1.7, 2.4], l: [-0.1, 1.25, -0.6], mm: 34 }],
              b: [{ t: 0, p: [1.3, 1.5, 1.7], l: [0.35, 1.3, 0.45], mm: 45 }, { t: dur, p: [1.05, 1.45, 1.45], l: [0.4, 1.3, 0.5], mm: 52 }] }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    const n = Math.min(sorts.length, Math.floor(t / Math.max(0.5, dur / 28))); sorts.forEach((s, i) => { s.visible = i < n; });
    const dn = opt.done !== undefined ? ease((t - opt.done) / 0.9) : 0; if (dn > 0) sorts.forEach((s) => { s.visible = true; });   // opt.done: dòng chữ đầy, bàn tay rời đi (sự kiện hình)
    const ph = (t % 1.2) / 1.2, a = ph < 0.5 ? ease(ph * 2) : ease((1 - ph) * 2);
    hand.position.set(lerp(lerp(-0.3 + 0.25 * Math.sin(t * 0.9), 0.3, a), -0.6, dn), lerp(lerp(1.3, 1.36, a), 1.05, dn), lerp(lerp(-0.1, 0.52, a), -0.5, dn)); hand.rotation.set(-0.4, 0.2, 0); hand.visible = dn < 0.9;   // rút xuống sau khay, xa máy quay
    bulb.intensity = 22 * (1 + 0.03 * Math.sin(f * 0.31));
  };
  return { scene, cam: rig.cam, update, grade: 'sepia', exposure: 1.1 };
}

// ===== linotype: phòng sắp chữ =====
async function linotype({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, '#2a2219', 0.028);
  scene.add(new THREE.HemisphereLight('#a08a6a', '#1a140f', 0.95));
  const iron = std('#5d6168', { metalness: 0.55, roughness: 0.45 }), iron2 = std('#43464c', { metalness: 0.55, roughness: 0.5 }), keyM = std('#e6dcc2');
  box(44, 0.1, 16, std('#3a322a'), 0, 0, 0); box(44, 7, 0.3, std('#5a4c3e'), 0, 3.5, -5);
  for (let i = 0; i < 6; i++) { box(1.6, 2.4, 0.05, new THREE.MeshBasicMaterial({ color: '#9fb2c8' }), -15 + i * 6, 3.6, -4.8); }   // cửa sổ cao (ánh trời)
  const sun = new THREE.DirectionalLight('#cfd8e8', 0.9); sun.position.set(-6, 9, -10); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -20, right: 20, top: 10, bottom: -10 }); scene.add(sun);
  const machines = [], ops = [], pots = [];
  for (let i = 0; i < 7; i++) {
    const m = new THREE.Group(); m.position.set(-12 + i * 4, 0, -1.2); scene.add(m); machines.push(m);
    box(1.4, 1.1, 1.0, iron, 0, 0.55, 0, m);
    const mag = box(1.25, 1.35, 0.3, iron2, 0, 1.95, -0.25, m); mag.rotation.x = 0.35;
    for (let k = 0; k < 10; k++) box(0.06, 1.2, 0.02, std('#7a7f86', { metalness: 0.6 }), -0.54 + k * 0.12, 1.95, -0.08, m).rotation.x = 0.35;   // rãnh khuôn chữ
    box(0.25, 1.7, 0.25, iron2, 0.78, 1.35, -0.3, m); box(0.9, 0.12, 0.12, iron2, 0.35, 2.75, -0.3, m);
    const kb = box(1.0, 0.06, 0.42, iron2, 0, 1.15, 0.56, m); kb.rotation.x = -0.4;
    for (let r = 0; r < 3; r++) for (let k = 0; k < 9; k++) box(0.07, 0.03, 0.07, keyM, -0.4 + k * 0.1, 1.2 + r * 0.04, 0.48 + r * 0.09, m);
    cyl(0.18, 0.2, 0.3, iron2, -0.85, 1.0, 0.0, m);
    const pg = glowSprite('#ff6a2a', 0.9, 0.6); pg.position.set(-0.85, 1.2, 0.05); m.add(pg); pots.push(pg);
    const pl = new THREE.PointLight('#ff7a3a', 3, 2.5, 2); pl.position.set(-0.85, 1.25, 0.1); m.add(pl);
    const op = figure({ seated: true, scale: 0.95, color: '#241b16' }); op.root.position.set(0.05, 0.05, 1.35); op.root.rotation.y = Math.PI; m.add(op.root); ops.push(op);
    box(0.5, 0.45, 0.45, std('#3a2a1e'), 0.05, 0.22, 1.4, m);
    cyl(0.06, 0.34, 0.24, std('#3c6047', { side: THREE.DoubleSide }), 0.1, 3.1, 0.4, m); cyl(0.004, 0.004, 1.5, lam('#111'), 0.1, 4.0, 0.4, m);
    const lb = new THREE.PointLight('#ffcf8a', 10, 6, 1.5); lb.position.set(0.1, 2.95, 0.45); m.add(lb);
    const gs = glowSprite('#ffd79a', 0.9, 0.7); gs.position.set(0.1, 2.95, 0.45); m.add(gs);
  }
  const dst = dust(scene, [-6, 2.6, 0.4], [10, 1.2, 1.2], 180, 31);
  const K = { a: [{ t: 0, p: [-14.5, 2.2, 3.6], l: [-9.5, 1.5, -0.9], mm: 32 }, { t: dur, p: [-3.5, 2.1, 3.6], l: [1.5, 1.5, -1.0], mm: 34 }],
              b: [{ t: 0, p: [4, 5.6, 6.5], l: [-2, 1.0, -1], mm: 28 }, { t: dur, p: [-3, 5.0, 6], l: [-7, 1.0, -1], mm: 30 }] }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    ops.forEach((o, i) => o.set({ armL: -1.1 + 0.12 * Math.sin(t * 9 + i), armR: -1.1 + 0.12 * Math.sin(t * 8.3 + i * 1.7), headTilt: 0.15 }));
    pots.forEach((p, i) => { p.material.opacity = 0.75 + 0.2 * Math.sin(f * 0.23 + i); });
  };
  return { scene, cam: rig.cam, update, grade: 'sepia' };
}

// ===== drafts: xưởng thiết kế hôm nay, bức tường bản nháp =====
async function drafts({ W, H, dur, v }) {
  const scene = new THREE.Scene(); fogOf(scene, '#0b1018', 0.05);
  scene.add(new THREE.HemisphereLight('#3a4a6a', '#05070a', 0.35));
  box(30, 0.1, 14, std('#1a1d22'), 0, 0, 0); box(30, 8, 0.3, std('#161a22'), 0, 4, -3);
  // tường màn hình 12 × 6 ô — mỗi ô một "bản nháp" áp phích tự sinh (hình học trừu tượng, không mô phỏng tác phẩm có thật)
  const R = rng(77), tiles = [], pal = ['#c99a5a', '#4f7096', '#a95a4c', '#ddd5bd', '#5a8a7c', '#8c7aa0', '#2f3b52'];
  for (let r = 0; r < 6; r++) for (let c = 0; c < 12; c++) {
    const tex = canvasTex(96, 128, (g, w, h) => { g.fillStyle = pal[Math.floor(R() * pal.length)]; g.fillRect(0, 0, w, h);
      for (let k = 0; k < 3; k++) { g.fillStyle = pal[Math.floor(R() * pal.length)]; const s = 20 + R() * 50; if (R() < 0.5) { g.beginPath(); g.arc(R() * w, R() * h, s / 2, 0, 7); g.fill(); } else g.fillRect(R() * w, R() * h, s, s * 0.6); }
      g.fillStyle = 'rgba(20,20,24,0.8)'; g.fillRect(10, h - 26, w - 20, 6); g.fillRect(10, h - 16, (w - 20) * 0.6, 4); });
    const m = new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: 0 });
    const o = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.82), m); o.position.set(-4.1 + c * 0.75, 1.0 + r * 0.95, -2.8); scene.add(o); tiles.push({ o, m, k: R() });
  }
  const wallLight = new THREE.PointLight('#7fa6ff', 4, 12, 1.4); wallLight.position.set(0, 3.5, -1.2); scene.add(wallLight);
  // bàn, màn hình, người thiết kế (bóng), một tờ in và bút chì trên bàn
  box(2.6, 0.06, 1.0, std('#26292e'), 0, 0.78, 0.6); box(0.06, 0.76, 0.9, std('#1d1f23'), -1.2, 0.38, 0.6); box(0.06, 0.76, 0.9, std('#1d1f23'), 1.2, 0.38, 0.6);
  const mon = box(1.1, 0.65, 0.04, new THREE.MeshBasicMaterial({ color: '#5f7fae' }), 0.4, 1.25, 0.35); mon.rotation.y = -0.15;
  box(0.42, 0.003, 0.3, std('#efe8d6'), -0.5, 0.815, 0.75).rotation.y = 0.2;
  const designer = figure({ seated: true, scale: 1.0, color: '#0c0d10' }); designer.root.position.set(0.2, 0.0, 1.45); designer.root.rotation.y = Math.PI; scene.add(designer.root);
  const desk = new THREE.PointLight('#ffcf9a', 4, 3, 2); desk.position.set(-0.72, 1.32, 0.66); scene.add(desk);
  const g2 = glowSprite('#9cc0ff', 0.7, 1.8); g2.position.set(0.4, 1.25, 0.4); scene.add(g2);
  // đèn bàn kẹp (vật nối liền mạch: ngọn đèn có mặt ở mọi chuyển hồi, Q30) — chao đồng, quầng ấm trên tờ in
  const arm = cyl(0.012, 0.012, 0.7, std('#3a3226', { metalness: 0.5 }), -0.95, 1.15, 0.55); arm.rotation.z = 0.5;
  const shade = cyl(0.05, 0.16, 0.16, std('#7a5a2e', { metalness: 0.4, roughness: 0.5, side: THREE.DoubleSide }), -0.78, 1.45, 0.62); shade.rotation.z = -0.5;
  const dl = glowSprite('#ffc27a', 0.9, 0.45); dl.position.set(-0.74, 1.38, 0.64); scene.add(dl);
  const dst = dust(scene, [0, 2, -1], [8, 3, 3], 300, 41, '#b8ccff');
  const K = { a: [{ t: 0, p: [0.4, 1.6, 4.6], l: [0, 2.6, -2.8], mm: 28 }, { t: dur, p: [0.2, 1.9, 2.6], l: [0, 2.9, -2.8], mm: 34 }],
              b: [{ t: 0, p: [1.5, 1.35, 3.6], l: [-0.3, 1.7, -2.8], mm: 30 }, { t: dur, p: [0.9, 1.4, 3.1], l: [-0.8, 1.9, -2.8], mm: 32 }] }[v];
  const rig = camRig(W, H, K);
  const update = (t, f) => {
    rig.at(t); dst.update(t);
    // ô bản nháp hiện dần: tới 60 % thời lượng thì đầy tường (hàng chục bản nháp)
    const full = dur * 0.6; tiles.forEach((x, i) => { const a = ease((t - (i / tiles.length) * full) / 0.4); x.m.opacity = a * (0.85 + 0.15 * Math.sin(t * 3 + x.k * 9)); });
    designer.set({ armR: -1.0 + 0.06 * Math.sin(t * 3.1), armL: -1.0, headTilt: -0.15 });
    wallLight.intensity = 1.5 + 3.5 * ease(t / full);
  };
  return { scene, cam: rig.cam, update, grade: 'cold' };
}

export const HEROES = { printshop, cellar, linotype, drafts };

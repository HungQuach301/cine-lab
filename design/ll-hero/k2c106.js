// KÊNH 2 · thí điểm T1 K2C-T1-06 "Apartments" — 7 BỘ CẢNH 3D (G1b, 13/10/2026). Nhận diện channel-k2/NHAN-DIEN.md:
//   sa bàn/khối có vân vật liệu, MỘT màu nhấn cam #F08A4B cho thứ đang được giải thích, xanh lục lam #3CC2B0 cho dòng "được phép/bình thường",
//   hổ phách #F2C14E cho cảnh báo; nền mực #0F1722. Không logo, không chữ nướng vào 3D (chữ ở lớp 2D bám `anchors`), không mặt người.
//   Máy quay: opt.cam = [{u: 0..1, p:[x,y,z], l:[x,y,z], mm}] hoặc preset scripts/k2/cams.yaml (k2c106/<cảnh>).
//   corner  toà góc phố 4 tầng (cửa hàng tầng trệt + 3 tầng căn hộ, MỘT cầu thang) ở ngã tư phố cũ; opt.tod dusk|day|blue; opt.section [t0,t1] cắt lớp
//           (mặt tiền góc mờ dần → thấy sàn, căn hộ, lõi thang cam); opt.shop (độ sáng cửa hàng 0..1); opt.lock = 'map'|'stair'|'bank' (vòng sáng khoá ở kết).
//   street  dãy phố: duplex · triplex · fourplex · walk-up 5–19 căn (4–5 tầng); opt.hl = chỉ số toà nhấn cam (giây mọc trong opt.hlAt); opt.tod.
//   tiers   sa bàn "tầng khu" kiểu Euclid 1922 (minh hoạ): U-1 nhà một hộ · U-2 nhà hai hộ · U-3 căn hộ · U-4 cửa hàng; opt.fill [t,...] (giây tô từng tầng),
//           opt.probe {at, zones} (toà góc phố thử từng khu: đỏ/xanh), opt.sun (bóng toà căn hộ lên nhà nhỏ).
//   lot     lô góc phố nhìn trên: dấu chân toà + ô đỗ (opt.stalls n, opt.grow [t0,t1]); toà co theo số ô (minh hoạ, không số).
//   stairs  mặt cắt toà 4–6 tầng: opt.mode one|two|compare; opt.floors (số tầng mọc, opt.stackAt); tầng 4 với 1 thang → khung đỏ "NP" (opt.np);
//           phần sàn bị thang 2 + hành lang chiếm tô cam (~7 %, Pew); opt.press (thang kín, mũi tên áp suất); opt.fire (3 điều kiện mô hình Minnesota).
//   bank    hàng khối nhà 1–2–3–4 căn | vạch 4 | khối 5 căn; hai quầy (single-family / multifamily); opt.fifth [t0,t1] khối 5 trượt sang quầy kia;
//           opt.shop (biến thể có cửa hàng tầng trệt), opt.reject (cả hai quầy từ chối: đèn hổ phách).
//   ends    sa bàn "hai đầu": nhà một hộ (trái), toà ≥ 50 căn (phải), toà nhỏ ở giữa; opt.year 1972→2025 (nội suy theo opt.yearAt [t0,t1]).
import { THREE, useScene, figure, dust, camRig, box, cyl, std, glowSprite, rng, ease, lerp, canvasTex } from './kit.js';

const C = { ink: '#0F1722', text: '#EEF1F4', steel: '#9AA7B5', orange: '#F08A4B', teal: '#3CC2B0', amber: '#F2C14E', red: '#E0564B' };
const GRADE_K2 = { gCanvas: 0.0, gVig: 0.24, gLift: 0.025, gSat: 0.92, gShadowTint: [0.22, 0.34, 0.62], gHiTint: [1.02, 1.0, 0.97] };
const GRADE_K2_WARM = { gCanvas: 0.0, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.26, 0.33, 0.6], gHiTint: [1.05, 0.99, 0.92] };
const GRADE_K2_DAY = { gCanvas: 0.0, gVig: 0.18, gLift: 0.015, gSat: 0.97, gShadowTint: [0.2, 0.3, 0.5], gHiTint: [1.02, 1.0, 0.98] };
const basic = (color, o = {}) => new THREE.MeshBasicMaterial({ color, ...o });
const V3 = (a) => new THREE.Vector3(...a);
const clamp01 = (u) => Math.max(0, Math.min(1, u));
const win01 = (t, w) => (w ? clamp01((t - w[0]) / Math.max(0.05, w[1] - w[0])) : 0);
// camera_id = tên preset trong CAM[cảnh] (opt.preset) hoặc opt.cam [{u,p,l,mm}] (u = phần thời lượng shot)
function rigOf(W, H, dur, opt, def, P = {}) { const K = (opt.cam || P[opt.preset] || def).map((k) => ({ t: k.u * dur, p: k.p, l: k.l, mm: k.mm || 32 })); return camRig(W, H, K.length > 1 ? K : [K[0], { ...K[0], t: dur }]); }
function skyDome(scene, stops, r = 320) {
  scene.add(new THREE.Mesh(new THREE.SphereGeometry(r, 32, 16), new THREE.MeshBasicMaterial({ side: THREE.BackSide, fog: false, map: canvasTex(8, 256, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([u, c]) => gr.addColorStop(u, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); }) })));
}
const fogOf = (scene, color, d) => { useScene(scene); scene.fog = new THREE.FogExp2(color, d); scene.background = new THREE.Color(color); };

// ---------- vân vật liệu (canvas, lặp; màu qua getHexString — BAI-HOC-K2 K5) ----------
const rep = (t, a, b) => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(a, b); t.anisotropy = 4; return t; };
const hex = (c) => '#' + c.getHexString();
function brickTex(seed = 3, base = '#7a3e2c', mortar = '#3a302a') { const R = rng(seed); return canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = mortar; g.fillRect(0, 0, w, h); const bw = 64, bh = 22;
  for (let y = 0, r = 0; y < h; y += bh, r++) for (let x = -(r % 2) * bw / 2; x < w; x += bw) { g.fillStyle = hex(new THREE.Color(base).multiplyScalar(0.72 + R() * 0.5)); g.fillRect(x + 2, y + 2, bw - 4, bh - 4); }
  for (let i = 0; i < 40; i++) { const x = R() * w, gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(15,12,12,0)'); gr.addColorStop(0.6, 'rgba(15,12,12,0.18)'); gr.addColorStop(1, 'rgba(15,12,12,0)'); g.fillStyle = gr; g.fillRect(x, 0, 4 + R() * 16, h); } }); }
function concTex(seed = 7, base = '#6d6c68', joint = 128) { const R = rng(seed); return canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h); for (let i = 0; i < 5000; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '20,20,18' : '210,206,198'},${0.03 + R() * 0.07})`; g.fillRect(R() * w, R() * h, 1 + R() * 3, 1 + R() * 3); }
  g.strokeStyle = 'rgba(20,20,20,0.35)'; g.lineWidth = 2; for (let i = 0; i <= w; i += joint) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }); }
function asphaltTex(seed = 11) { const R = rng(seed); return canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = '#2b2d30'; g.fillRect(0, 0, w, h); for (let i = 0; i < 9000; i++) { const v = 30 + R() * 50 | 0; g.fillStyle = `rgba(${v},${v},${v + 4},0.35)`; g.fillRect(R() * w, R() * h, 1 + R() * 2, 1 + R() * 2); }
  for (let i = 0; i < 6; i++) { g.strokeStyle = 'rgba(15,15,15,0.5)'; g.lineWidth = 1 + R() * 2; g.beginPath(); let x = R() * w, y = R() * h; g.moveTo(x, y); for (let k = 0; k < 8; k++) { x += (R() - 0.5) * 60; y += (R() - 0.5) * 60; g.lineTo(x, y); } g.stroke(); } }); }
function clapTex(seed = 13, base = '#c9c3b6') { const R = rng(seed); return canvasTex(256, 256, (g, w, h) => {
  for (let y = 0; y < h; y += 16) { g.fillStyle = hex(new THREE.Color(base).multiplyScalar(0.86 + R() * 0.12)); g.fillRect(0, y, w, 16); g.fillStyle = 'rgba(0,0,0,0.28)'; g.fillRect(0, y + 14, w, 2); } }); }
function stuccoTex(seed = 17, base = '#b9ad98') { const R = rng(seed); return canvasTex(256, 256, (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h); for (let i = 0; i < 3000; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '60,55,48' : '235,230,220'},${0.04 + R() * 0.06})`; g.fillRect(R() * w, R() * h, 1 + R() * 3, 1 + R() * 3); } }); }
function gridTex(bg = '#121b28', rep0 = 6) { return rep(canvasTex(1024, 1024, (g, w, h) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); for (let i = 0; i <= w; i += 32) { g.strokeStyle = i % 128 ? 'rgba(154,167,181,0.07)' : 'rgba(154,167,181,0.2)'; g.lineWidth = i % 128 ? 1 : 2; g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke(); } }), rep0, rep0); }
// cửa sổ có rèm và ánh đèn ngẫu nhiên (đêm/chạng vạng) hoặc kính phản chiếu trời (ngày)
function winTex(seed, lit, day) { const R = rng(seed); return canvasTex(64, 96, (g, w, h) => {
  if (day) { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#9fb6cc'); gr.addColorStop(1, '#3d4c5c'); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(255,255,255,0.18)'; g.fillRect(4, 6, 14, h - 12); }
  else if (lit) { const gr = g.createRadialGradient(w / 2, h * 0.55, 4, w / 2, h * 0.55, h * 0.7); gr.addColorStop(0, '#ffd59a'); gr.addColorStop(1, R() < 0.5 ? '#c98a4e' : '#a5764a'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = 'rgba(90,50,30,0.55)'; g.fillRect(0, 0, w * (0.18 + R() * 0.2), h); g.fillRect(w * (0.78 - R() * 0.15), 0, w, h); }
  else { g.fillStyle = '#1a2230'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(120,140,170,0.15)'; g.fillRect(4, 4, w - 8, h * 0.4); }
  g.fillStyle = '#e8e2d6'; g.fillRect(w / 2 - 1.5, 0, 3, h); g.fillRect(0, h / 2 - 1.5, w, 3); g.lineWidth = 5; g.strokeStyle = '#ece6da'; g.strokeRect(2, 2, w - 4, h - 4); }); }

// THƯ VIỆN GÓC MÁY (camera_id = tên preset; mỗi preset là chuyển động liên tục). Tên khớp camera_id trong channel-k2/k2c-t1-06/shots.yaml
const CAM = {
  corner: {
    wide_dusk: [{ u: 0, p: [-18, 1.9, -20], l: [9, 6.6, 9], mm: 28 }, { u: 1, p: [-14.5, 2.2, -16.5], l: [9, 6.9, 9], mm: 28 }],
    push_facade: [{ u: 0, p: [-9, 2.6, -7], l: [9, 7.6, 8.5], mm: 30 }, { u: 1, p: [-3.2, 3.2, -2.2], l: [9, 8.0, 8.5], mm: 30 }],
    section: [{ u: 0, p: [-15, 13, -17], l: [10, 5.8, 10], mm: 30 }, { u: 1, p: [-12, 12, -14.5], l: [10, 6.2, 10], mm: 30 }],
    stair_section: [{ u: 0, p: [-6, 11, -12], l: [14, 7, 13], mm: 32 }, { u: 1, p: [-4, 12.5, -9], l: [14, 7.5, 13], mm: 32 }],
    shop_section: [{ u: 0, p: [-10, 3.2, -11], l: [8, 3.0, 8], mm: 30 }, { u: 1, p: [-7, 3.6, -9], l: [8, 3.4, 8], mm: 30 }],
    day_town_center: [{ u: 0, p: [-24, 7, -6], l: [9, 6, 9], mm: 32 }, { u: 1, p: [-22, 7.5, -12], l: [9, 6.2, 9], mm: 32 }],
    blue_hour_end: [{ u: 0, p: [-4, 2.2, -28], l: [10, 7, 9], mm: 35 }, { u: 1, p: [-8, 2.4, -26], l: [10, 7, 9], mm: 35 }],
    section_end: [{ u: 0, p: [-18, 9, -12], l: [10, 6, 10], mm: 30 }, { u: 1, p: [-15, 10, -16], l: [10, 6.4, 10], mm: 30 }],
    crane_up: [{ u: 0, p: [-8, 1.8, -9], l: [9, 7, 9], mm: 28 }, { u: 1, p: [-16, 30, -20], l: [9, 3, 9], mm: 28 }],
  },
  street: {
    dolly_day: [{ u: 0, p: [-36, 6.5, -17], l: [-28, 6, 15], mm: 28 }, { u: 1, p: [24, 7, -17], l: [32, 7, 15], mm: 28 }],
    tall_walkups: [{ u: 0, p: [10, 1.6, 0], l: [24, 10, 15], mm: 24 }, { u: 1, p: [16, 1.8, -1], l: [28, 11, 15], mm: 24 }],
    dusk_new: [{ u: 0, p: [-30, 6, -14], l: [0, 5, 15], mm: 30 }, { u: 1, p: [-22, 6.5, -16], l: [4, 5, 15], mm: 30 }],
    high_block: [{ u: 0, p: [-10, 30, -30], l: [2, 3, 14], mm: 30 }, { u: 1, p: [0, 28, -30], l: [6, 3, 14], mm: 30 }],
    low_curb: [{ u: 0, p: [-24, 1.2, 4], l: [-4, 4, 14], mm: 26 }, { u: 1, p: [-20, 1.3, 4.5], l: [0, 4.5, 14], mm: 26 }],
    tele_fronts: [{ u: 0, p: [-60, 5, -30], l: [-15, 5, 15], mm: 70 }, { u: 1, p: [-50, 5, -34], l: [-5, 5, 15], mm: 70 }],
  },
  tiers: {
    top: [{ u: 0, p: [0, 64, 5], l: [0, 0, 0], mm: 30 }, { u: 1, p: [2, 60, 4], l: [1, 0, 0], mm: 30 }],
    oblique_tiers: [{ u: 0, p: [-34, 30, 40], l: [0, 1, -3], mm: 30 }, { u: 1, p: [-22, 27, 45], l: [2, 1, -3], mm: 30 }],
    shadow_low: [{ u: 0, p: [-6, 5, 10], l: [6, 3, -10], mm: 28 }, { u: 1, p: [-3, 5.5, 8], l: [6, 3, -10], mm: 28 }],
    orbit_r: [{ u: 0, p: [36, 28, 36], l: [0, 1, -3], mm: 30 }, { u: 1, p: [24, 26, 44], l: [0, 1, -3], mm: 30 }],
    close_u3: [{ u: 0, p: [2, 14, 12], l: [8, 2, -6], mm: 32 }, { u: 1, p: [5, 13, 13], l: [9, 2, -6], mm: 32 }],
    front_low: [{ u: 0, p: [0, 9, 40], l: [0, 2, -2], mm: 32 }, { u: 1, p: [3, 10, 39], l: [0, 2, -2], mm: 32 }],
  },
  lot: {
    plan: [{ u: 0, p: [11.5, 46, 42], l: [11.5, 0, 17.5], mm: 30 }, { u: 1, p: [13.5, 42, 41], l: [11.5, 0, 17.5], mm: 30 }],
    pencil: [{ u: 0, p: [-14, 16, -6], l: [11, 5, 16], mm: 32 }, { u: 1, p: [-10, 15, -10], l: [11, 5, 16], mm: 32 }],
    top: [{ u: 0, p: [10.5, 56, 19.5], l: [11.5, 0, 19], mm: 30 }, { u: 1, p: [12.5, 52, 19.5], l: [11.5, 0, 19], mm: 30 }],
    street_level: [{ u: 0, p: [-6, 1.7, 2], l: [11, 4, 18], mm: 28 }, { u: 1, p: [-4, 1.8, 0], l: [11, 4, 18], mm: 28 }],
    orbit: [{ u: 0, p: [36, 22, 8], l: [11.5, 1, 18], mm: 30 }, { u: 1, p: [34, 22, 30], l: [11.5, 1, 18], mm: 30 }],
    rear: [{ u: 0, p: [14, 18, 56], l: [11.5, 2, 18], mm: 32 }, { u: 1, p: [9, 17, 56], l: [11.5, 2, 18], mm: 32 }],
  },
  stairs: {
    elev_stack: [{ u: 0, p: [13, 7, 18], l: [0, 5.5, 0], mm: 30 }, { u: 1, p: [10.5, 9, 19.5], l: [0, 6.5, 0], mm: 30 }],
    model_code: [{ u: 0, p: [24, 16, 30], l: [0, 5, 0], mm: 30 }, { u: 1, p: [20, 15, 32], l: [0, 5, 0], mm: 30 }],
    plan_compare: [{ u: 0, p: [0, 46, 20], l: [0, 3, 0], mm: 30 }, { u: 1, p: [2, 42, 22], l: [0, 3, 0], mm: 30 }],
    floor_plate: [{ u: 0, p: [6, 22, 14], l: [0, 6, 0], mm: 30 }, { u: 1, p: [-4, 21, 15], l: [0, 6, 0], mm: 30 }],
    pressurized: [{ u: 0, p: [10, 9, 14], l: [0, 5, 0], mm: 30 }, { u: 1, p: [7, 10, 16], l: [0, 5.5, 0], mm: 30 }],
    fire_logic: [{ u: 0, p: [-14, 12, 22], l: [0, 6.5, -2], mm: 30 }, { u: 1, p: [-10, 12.5, 24], l: [0, 6.5, -2], mm: 30 }],
  },
  bank: {
    side: [{ u: 0, p: [-24, 5, 12], l: [0, 2.5, 0], mm: 32 }, { u: 1, p: [-21, 5.5, 15], l: [0, 2.5, 0], mm: 32 }],
    line_four: [{ u: 0, p: [3, 3.5, 12], l: [0, 3, 0], mm: 32 }, { u: 1, p: [5, 3.8, 11], l: [0.5, 3, 0], mm: 32 }],
    counter: [{ u: 0, p: [-14, 6, 8], l: [-8, 2.5, -9], mm: 32 }, { u: 1, p: [-11, 5.5, 7], l: [-8, 2.5, -9], mm: 32 }],
    fifth_block: [{ u: 0, p: [-11, 5.5, 16.5], l: [-0.5, 2.6, -3.5], mm: 28 }, { u: 1, p: [-8, 5.8, 17], l: [0.5, 2.6, -3.5], mm: 28 }],
    mixed_reject: [{ u: 0, p: [0, 9, 22], l: [1, 2.5, -4], mm: 30 }, { u: 1, p: [-3, 9.5, 21], l: [1, 2.5, -4], mm: 30 }],
    line_still: [{ u: 0, p: [10, 4, 14], l: [1, 2.8, 0], mm: 32 }, { u: 1, p: [8, 4.2, 15], l: [1, 2.8, 0], mm: 32 }],
  },
  ends: {
    wide_1972: [{ u: 0, p: [-8, 40, 52], l: [0, 2, 0], mm: 30 }, { u: 1, p: [-2, 38, 54], l: [0, 2, 0], mm: 30 }],
    wide_2025: [{ u: 0, p: [10, 36, 50], l: [2, 3, 0], mm: 30 }, { u: 1, p: [4, 38, 52], l: [2, 3, 0], mm: 30 }],
    low_middle: [{ u: 0, p: [-2, 4, 22], l: [0, 3, -10], mm: 26 }, { u: 1, p: [2, 4.5, 21], l: [0, 3, -10], mm: 26 }],
    top: [{ u: 0, p: [-4, 70, 8], l: [0, 0, 0], mm: 30 }, { u: 1, p: [4, 66, 8], l: [0, 0, 0], mm: 30 }],
    orbit_l: [{ u: 0, p: [-58, 30, 30], l: [0, 2, 0], mm: 30 }, { u: 1, p: [-46, 30, 44], l: [0, 2, 0], mm: 30 }],
    close_big: [{ u: 0, p: [14, 12, 22], l: [30, 8, -2], mm: 30 }, { u: 1, p: [18, 13, 22], l: [31, 8, -2], mm: 30 }],
  },
};
const M = {};
function mats() { if (M.brick) return M;
  M.brick = std('#ffffff', { map: rep(brickTex(3), 1, 1), roughness: 0.95 }); M.brick2 = std('#ffffff', { map: rep(brickTex(8, '#5d4a3e'), 1, 1), roughness: 0.95 }); M.brick3 = std('#ffffff', { map: rep(brickTex(21, '#8a6a4a'), 1, 1), roughness: 0.95 });
  M.conc = std('#ffffff', { map: rep(concTex(7), 1, 1), roughness: 0.95 }); M.walk = std('#ffffff', { map: rep(concTex(19, '#8a8780', 64), 1, 1), roughness: 0.92 });
  M.asph = std('#ffffff', { map: rep(asphaltTex(11), 1, 1), roughness: 0.9 }); M.clap = std('#ffffff', { map: rep(clapTex(13), 1, 1), roughness: 0.9 }); M.clap2 = std('#ffffff', { map: rep(clapTex(23, '#9fb0a8'), 1, 1), roughness: 0.9 });
  M.stucco = std('#ffffff', { map: rep(stuccoTex(17), 1, 1), roughness: 0.95 }); M.trim = std('#e4ddcf', { roughness: 0.7 }); M.dark = std('#23272e', { roughness: 0.85 }); M.iron = std('#2b2f36', { roughness: 0.6, metalness: 0.4 });
  M.roof = std('#3a3c40', { roughness: 0.95 }); M.glass = std('#1d2a38', { roughness: 0.15, metalness: 0.6 }); return M; }
// khối có vân lặp theo kích thước (UV theo mét)
function tbox(w, h, d, mat, x, y, z, parent, k = 0.2) { const g = new THREE.BoxGeometry(w, h, d), uv = g.attributes.uv, n = g.attributes.normal;
  for (let i = 0; i < uv.count; i++) { const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)); const su = ax > 0.5 ? d : w, sv = ay > 0.5 ? d : h; uv.setXY(i, uv.getX(i) * su * k, uv.getY(i) * sv * k); }
  const m = new THREE.Mesh(g, mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; (parent || window.__scene).add(m); return m; }
const TOD = {
  dusk: { fog: '#1b2233', fd: 0.010, sky: [[0, '#0b1222'], [0.36, '#1c2a46'], [0.46, '#4a4560'], [0.495, '#c8784a'], [0.505, '#e39654'], [0.53, '#202434'], [1, '#0e121b']], hemi: ['#8293c4', '#2a2418', 2.2], sun: ['#ffb383', 2.2, [-60, 22, -90]], lit: 0.75, grade: GRADE_K2_WARM, exp: 1.35, day: false },
  blue: { fog: '#1d2a3e', fd: 0.009, sky: [[0, '#0a1430'], [0.38, '#1e3460'], [0.47, '#4f6a96'], [0.5, '#8aa3c4'], [0.52, '#2a3446'], [1, '#121820']], hemi: ['#9ab4e0', '#3a4256', 2.2], sun: ['#a9c2ee', 1.0, [50, 40, -70]], lit: 0.6, grade: GRADE_K2, exp: 1.3, day: false },
  day: { fog: '#a9bccf', fd: 0.0055, sky: [[0, '#4d77a8'], [0.4, '#8fb0d4'], [0.5, '#d9e2ea'], [0.52, '#b7c3cc'], [1, '#6e7a84']], hemi: ['#d4e4ff', '#6a5e4c', 2.0], sun: ['#fff1dc', 3.4, [-50, 70, 40]], lit: 0.0, grade: GRADE_K2_DAY, exp: 1.0, day: true },
};
function lightTod(scene, T, ext = 60, target = [0, 0, 0]) { scene.add(new THREE.HemisphereLight(...T.hemi)); const sun = new THREE.DirectionalLight(T.sun[0], T.sun[1]); sun.position.set(...T.sun[2]); sun.target.position.set(...target); scene.add(sun.target);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -ext, right: ext, top: ext, bottom: -ext, far: 400 }); sun.shadow.bias = -0.0004; scene.add(sun); return sun; }

// ---------- chi tiết phố ----------
function tree(x, z, s = 1, R = Math.random, bare = false) { const g = new THREE.Group(); g.position.set(x, 0, z); window.__scene.add(g);
  cyl(0.12 * s, 0.18 * s, 2.6 * s, std('#3b2e24', { roughness: 0.95 }), 0, 1.3 * s, 0, g, 7);
  if (!bare) for (let i = 0; i < 4; i++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry((0.9 + R() * 0.5) * s, 1), std(['#3d5a3a', '#4a6a40', '#35503a'][i % 3], { roughness: 0.95, flatShading: true })); m.position.set((R() - 0.5) * 1.2 * s, (2.9 + R() * 0.9) * s, (R() - 0.5) * 1.2 * s); m.castShadow = true; g.add(m); }
  return g; }
function lamp(x, z, on) { const g = new THREE.Group(); g.position.set(x, 0, z); window.__scene.add(g); cyl(0.06, 0.09, 4.2, M.iron, 0, 2.1, 0, g, 8); box(0.7, 0.06, 0.06, M.iron, 0.3, 4.15, 0, g); box(0.3, 0.16, 0.22, M.dark, 0.62, 4.05, 0, g);
  if (on) { const pl = new THREE.PointLight('#ffcf8a', 14, 13, 1.7); pl.position.set(0.62, 3.9, 0); g.add(pl); const sp = glowSprite('#ffd29a', 0.9, 1.6); sp.position.set(0.62, 3.95, 0); g.add(sp); } return g; }
function car(x, z, ry, color, R) { const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; window.__scene.add(g);
  const body = std(color, { roughness: 0.35, metalness: 0.5 }); box(1.8, 0.6, 4.2, body, 0, 0.55, 0, g); box(1.6, 0.5, 2.1, body, 0, 1.05, -0.2, g); box(1.62, 0.42, 2.0, M.glass, 0, 1.06, -0.2, g);
  for (const [a, b] of [[-0.85, 1.3], [0.85, 1.3], [-0.85, -1.3], [0.85, -1.3]]) { const w = cyl(0.33, 0.33, 0.22, M.dark, a, 0.33, b, g, 12); w.rotation.z = Math.PI / 2; } return g; }
function people(n, area, R, color = '#1a1714') { const L = []; for (let i = 0; i < n; i++) { const f = figure({ color, scale: 0.95 + R() * 0.12 }); f.root.position.set(area[0] + R() * (area[1] - area[0]), 0, area[2] + R() * (area[3] - area[2])); f.root.rotation.y = R() * 6.28; window.__scene.add(f.root); L.push({ f, ph: R() * 6, sp: (R() - 0.5) * 0.8 }); } return L; }
// ô lưới cửa sổ trên một mặt nhà: mặt ở z = zf hướng +z (hoặc trục x khi axis = 'x')
function windows(x0, x1, y0, nF, fH, z, { axis = 'z', dir = 1, per = 2.2, w = 1.1, h = 1.6, seed = 1, T, litP = 0.6 }) { const R = rng(seed); const n = Math.max(1, Math.floor((x1 - x0) / per)); const step = (x1 - x0) / n; const out = [];
  for (let f = 0; f < nF; f++) for (let i = 0; i < n; i++) { const lit = !T.day && R() < litP * (0.6 + T.lit * 0.5); const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: winTex(seed * 100 + f * 17 + i, lit, T.day), emissive: lit ? '#ffb469' : '#000000', emissiveIntensity: lit ? 0.85 : 0, roughness: T.day ? 0.2 : 0.6, metalness: T.day ? 0.3 : 0 }));
    const c = x0 + step * (i + 0.5), y = y0 + f * fH + fH * 0.55; if (axis === 'z') { m.position.set(c, y, z + 0.02 * dir); m.rotation.y = dir > 0 ? 0 : Math.PI; } else { m.position.set(z + 0.02 * dir, y, c); m.rotation.y = dir > 0 ? Math.PI / 2 : -Math.PI / 2; }
    window.__scene.add(m); box(axis === 'z' ? w + 0.25 : 0.12, 0.12, axis === 'z' ? 0.12 : w + 0.25, M.trim, axis === 'z' ? c : z + 0.06 * dir, y - h / 2 - 0.08, axis === 'z' ? z + 0.06 * dir : c, window.__scene); out.push(m); } return out; }

// toà walk-up: thân gạch, phào mái, cửa sổ hai mặt, (tuỳ chọn) cửa hàng tầng trệt. Trả {group, top, shop, floors:[y]}
function walkup({ x, z, w, d, floors, fH = 3.1, mat, T, seed = 1, shop = false, cornice = true, faces = ['z', 'x'], parent }) {
  const mt = mats(); const g = new THREE.Group(); g.position.set(x, 0, z); (parent || window.__scene).add(g); const H = floors * fH + (shop ? 0.6 : 0); const sc = window.__scene; window.__scene = g;
  tbox(w, H, d, mat, 0, H / 2, 0, g, 0.25);
  if (cornice) { box(w + 0.5, 0.45, d + 0.5, mt.trim, 0, H + 0.1, 0, g); box(w + 0.3, 0.25, d + 0.3, mt.dark, 0, H + 0.42, 0, g); box(w + 0.2, 0.2, d + 0.2, mt.trim, 0, fH * (shop ? 1 : 0) + 0.2, 0, g); }
  const y0 = shop ? fH + 0.6 : 0.3, nUp = shop ? floors - 1 : floors;
  if (faces.includes('z')) windows(-w / 2 + 0.4, w / 2 - 0.4, y0, nUp, fH, d / 2, { seed, T });
  if (faces.includes('x')) windows(-d / 2 + 0.4, d / 2 - 0.4, y0, nUp, fH, w / 2, { axis: 'x', seed: seed + 7, T });
  let shopM = null;
  if (shop) { const sh = new THREE.MeshStandardMaterial({ color: '#2a2016', emissive: '#ffb066', emissiveIntensity: T.day ? 0.05 : 0.9, roughness: 0.3, metalness: 0.2 });
    const fz = new THREE.Mesh(new THREE.PlaneGeometry(w - 1.2, fH - 0.8), sh); fz.position.set(0, (fH - 0.2) / 2 + 0.2, d / 2 + 0.03); g.add(fz);
    const fx = new THREE.Mesh(new THREE.PlaneGeometry(d - 1.2, fH - 0.8), sh); fx.position.set(w / 2 + 0.03, (fH - 0.2) / 2 + 0.2, 0); fx.rotation.y = Math.PI / 2; g.add(fx);
    const aw = std(C.teal, { roughness: 0.8, side: THREE.DoubleSide }); const a1 = box(w - 0.8, 0.08, 1.4, aw, 0, fH + 0.05, d / 2 + 0.65, g); a1.rotation.x = 0.32; const a2 = box(1.4, 0.08, d - 0.8, aw, w / 2 + 0.65, fH + 0.05, 0, g); a2.rotation.z = -0.32;
    box(w - 1.0, 0.5, 0.12, mt.dark, 0, fH - 0.2, d / 2 + 0.08, g); box(0.12, 0.5, d - 1.0, mt.dark, w / 2 + 0.08, fH - 0.2, 0, g);   // dải biển hiệu trống (không chữ, không logo)
    shopM = sh; }
  window.__scene = sc; return { group: g, top: V3([x, H + 0.6, z]), shop: shopM, H, floorY: (k) => y0 + (k - (shop ? 1 : 0)) * fH + fH * 0.5 };
}
function house(x, z, { w = 6, d = 7, h = 3.0, mat, roofC = '#3a3c40', ry = 0, T, seed = 1, parent }) { const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; (parent || window.__scene).add(g);
  tbox(w, h, d, mat, 0, h / 2, 0, g, 0.3); const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, w * 0.62, 2.0, 4, 1), std(roofC, { roughness: 0.9, flatShading: true })); roof.position.set(0, h + 1.0, 0); roof.rotation.y = Math.PI / 4; roof.scale.set(1, 1, d / w); roof.castShadow = true; g.add(roof);
  const sc = window.__scene; window.__scene = g; windows(-w / 2 + 0.6, w / 2 - 0.6, 0.2, 1, h - 0.4, d / 2, { seed, T, per: 2.4, w: 1.0, h: 1.3 }); window.__scene = sc; return g; }

// =================================== corner ===================================
async function corner({ W, H, dur, opt }) {
  const mt = mats(); const T = TOD[opt.tod || 'dusk']; const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, T.fog, T.fd); skyDome(scene, T.sky); const R = rng(5);
  // mặt đường, vỉa hè, vạch qua đường
  tbox(160, 0.1, 160, mt.asph, 0, -0.05, 0, scene, 0.08);
  for (const [x, z, w, d] of [[-24, -24, 40, 40], [24, -24, 40, 40], [-24, 24, 40, 40], [24, 24, 40, 40]]) { tbox(w, 0.25, d, mt.walk, x + Math.sign(x) * 0, 0.12, z, scene, 0.35); }
  for (let i = -3; i <= 3; i++) { box(0.5, 0.02, 3, basic('#d9d4c4'), i * 1.0, 0.02, 6.2); box(3, 0.02, 0.5, basic('#d9d4c4'), 6.2, 0.02, i * 1.0); }
  box(160, 0.02, 0.18, basic('#c9a24a'), 0, 0.02, -0.3); box(0.18, 0.02, 160, basic('#c9a24a'), -0.3, 0.02, 0);
  // TOÀ GÓC: góc đường ở (4,4) → khối x 4..16, z 4..14 (mặt tiền +x? ) — đặt tâm (10, 9.5), mặt nhìn về giao lộ là −x và −z
  const B = new THREE.Group(); B.position.set(10.5, 0.25, 10); scene.add(B);
  const bw = 12, bd = 11, fH = 3.2, floors = 4, BH = floors * fH + 0.6;
  const shell = new THREE.Group(); B.add(shell); window.__scene = shell;
  const facade = tbox(bw, BH, bd, mt.brick, 0, BH / 2, 0, shell, 0.25);
  box(bw + 0.6, 0.5, bd + 0.6, mt.trim, 0, BH + 0.12, 0, shell); box(bw + 0.4, 0.3, bd + 0.4, mt.dark, 0, BH + 0.5, 0, shell); box(bw + 0.25, 0.25, bd + 0.25, mt.trim, 0, fH + 0.3, 0, shell);
  for (let f = 1; f < floors; f++) box(bw + 0.1, 0.12, bd + 0.1, mt.trim, 0, fH + 0.6 + f * fH - 0.05, 0, shell);
  // cửa sổ hai mặt hướng giao lộ (−z và −x)
  windows(-bw / 2 + 0.5, bw / 2 - 0.5, fH + 0.6, floors - 1, fH, -bd / 2, { dir: -1, seed: 31, T, per: 2.0 });
  windows(-bd / 2 + 0.5, bd / 2 - 0.5, fH + 0.6, floors - 1, fH, -bw / 2, { axis: 'x', dir: -1, seed: 37, T, per: 2.0 });
  // cửa hàng tầng trệt (hai mặt kính) + mái hiên + dải biển trống
  const shopMat = new THREE.MeshStandardMaterial({ color: '#2a2016', emissive: '#ffb066', emissiveIntensity: T.day ? 0.06 : 0.95, roughness: 0.25, metalness: 0.3 });
  const gz = new THREE.Mesh(new THREE.PlaneGeometry(bw - 2.4, fH - 0.9), shopMat); gz.position.set(0.4, (fH - 0.9) / 2 + 0.45, -bd / 2 - 0.03); gz.rotation.y = Math.PI; shell.add(gz);
  const gx = new THREE.Mesh(new THREE.PlaneGeometry(bd - 2.4, fH - 0.9), shopMat); gx.position.set(-bw / 2 - 0.03, (fH - 0.9) / 2 + 0.45, 0.4); gx.rotation.y = -Math.PI / 2; shell.add(gx);
  for (let k = -2; k <= 2; k++) { box(0.12, fH - 0.9, 0.12, mt.trim, 0.4 + k * 2.0, (fH - 0.9) / 2 + 0.45, -bd / 2 - 0.08, shell); box(0.12, fH - 0.9, 0.12, mt.trim, -bw / 2 - 0.08, (fH - 0.9) / 2 + 0.45, 0.4 + k * 1.8, shell); }
  const doorC = box(1.3, 2.3, 0.15, std('#3a2a1c'), -bw / 2 + 0.9, 1.2, -bd / 2 - 0.05, shell);   // cửa vát góc
  const awn = std(C.teal, { roughness: 0.85, side: THREE.DoubleSide }); const aw1 = box(bw - 1.6, 0.08, 1.5, awn, 0.4, fH + 0.05, -bd / 2 - 0.7, shell); aw1.rotation.x = -0.32; const aw2 = box(1.5, 0.08, bd - 1.6, awn, -bw / 2 - 0.7, fH + 0.05, 0.4, shell); aw2.rotation.z = 0.32;
  box(bw - 2.0, 0.55, 0.12, mt.dark, 0.4, fH - 0.15, -bd / 2 - 0.08, shell); box(0.12, 0.55, bd - 2.0, mt.dark, -bw / 2 - 0.08, fH - 0.15, 0.4, shell);
  // lối vào căn hộ (cửa riêng mặt −z, cạnh cửa hàng) + cầu thang thoát hiểm sắt mặt +x (phía sau)
  box(1.1, 2.4, 0.15, std('#2c241c'), bw / 2 - 1.0, 1.25, -bd / 2 - 0.05, shell); box(1.5, 0.2, 0.6, mt.trim, bw / 2 - 1.0, 2.6, -bd / 2 - 0.3, shell);
  window.__scene = scene;
  // NỘI THẤT (cắt lớp): sàn từng tầng, vách căn hộ, lõi thang cam (MỘT cầu thang)
  const inside = new THREE.Group(); B.add(inside); inside.visible = false;
  const floorM = std('#6b5a48', { roughness: 0.8 }), wallM = std('#8c7f6c', { roughness: 0.9, transparent: true, opacity: 0.55, depthWrite: false }), stairM = std(C.orange, { roughness: 0.45, emissive: '#c4561c', emissiveIntensity: 0.9 });
  for (let f = 0; f <= floors; f++) box(bw - 0.4, 0.22, bd - 0.4, floorM, 0, f === 0 ? 0.1 : fH + 0.6 + (f - 1) * fH, 0, inside);
  for (let f = 1; f < floors; f++) { const y = fH + 0.6 + (f - 1) * fH + fH / 2; box(0.15, fH - 0.3, bd - 0.6, wallM, 0.5, y, 0, inside); box(bw - 0.6, fH - 0.3, 0.15, wallM, 0, y, 1.2, inside);
    for (const [xx, zz] of [[-3, -2.5], [3.2, -2.6], [-3.2, 3.6], [3.4, 3.5]]) { box(1.6, 0.5, 0.8, std(['#7a5a3c', '#5a6a7a', '#8a7a5c'][f % 3]), xx, y - fH / 2 + 0.45, zz, inside); }
    const lt = new THREE.PointLight('#ffd09a', T.day ? 1.5 : 4, 8, 1.8); lt.position.set(-2, y + 0.8, -1); inside.add(lt); }
  const stair = new THREE.Group(); stair.position.set(bw / 2 - 1.6, 0, -bd / 2 + 2.0); inside.add(stair);   // MỘT cầu thang, ngay sau cửa riêng của căn hộ (mặt −z)
  for (let f = 0; f < floors; f++) for (let s = 0; s < 9; s++) { const y = (f === 0 ? 0.2 : fH + 0.6 + (f - 1) * fH) + s * (f === 0 ? (fH + 0.6) : fH) / 9; box(1.5, 0.22, 0.34, stairM, (s % 2 ? 0.55 : -0.55) * 0, y, -1.3 + (f % 2 ? 9 - s : s) * 0.3, stair); }
  box(2.6, BH, 0.1, std(C.orange, { transparent: true, opacity: 0.18, depthWrite: false }), 0, BH / 2, 1.6, stair);
  // hàng xóm: nhà hai tầng ốp gỗ (+z), dãy walk-up gạch (+x), phố đối diện
  walkup({ x: 23, z: 10, w: 9, d: 10, floors: 3, mat: mt.brick2, T, seed: 41, faces: ['z'] });
  house(10, 24, { w: 9, d: 8, h: 6.2, mat: mt.clap, T, seed: 43, ry: Math.PI });
  walkup({ x: -12, z: 11, w: 10, d: 11, floors: 3, mat: mt.brick3, T, seed: 47, shop: true });
  walkup({ x: 11, z: -12, w: 11, d: 10, floors: 2, mat: mt.stucco, T, seed: 53, shop: true, faces: ['x'] });
  house(-34, -12, { w: 9, d: 9, h: 6.0, mat: mt.clap2, T, seed: 59 });
  for (let i = 0; i < 6; i++) { const s = [-1, 1][i % 2]; tree(s * (3.6 + R() * 1.5) + (i < 3 ? 16 : -16) * 0.6, (i < 3 ? 1 : -1) * (14 + i * 4), 0.9, R, !T.day && false); }
  for (const [x, z] of [[3.4, 18], [3.4, -18], [18, 3.4], [-18, 3.4], [3.4, 14.5]]) lamp(x, z, !T.day);
  car(-2.5, 20, 0, '#6b2e2a', R); car(2.4, -26, Math.PI, '#2d4a5e', R); car(26, -2.4, Math.PI / 2, '#8a8478', R); car(-30, 2.6, -Math.PI / 2, '#3a3d44', R);
  const ppl = people(7, [-8, 24, 3.2, 4.6], R); people(4, [3.2, 4.6, -20, 18], R);
  const sun = lightTod(scene, T, 50, [8, 0, 8]);
  const shopGlow = new THREE.PointLight('#ffb36a', T.day ? 0 : 45, 16, 1.6); shopGlow.position.set(3.2, 2.0, 3.0); scene.add(shopGlow);
  const dst = dust(scene, [6, 4, 6], [30, 8, 30], 260, 7, T.day ? '#ffffff' : '#ffd9a8');
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [-26, 5.5, -30], l: [9, 7, 9], mm: 30 }, { u: 1, p: [-21, 6.5, -24], l: [9, 7.2, 9], mm: 32 }], CAM.corner);
  const anchors = { building: V3([10.5, BH + 1.2, 10]), shop: V3([4.0, 1.8, 4.2]), apt2: V3([4.3, fH + 0.6 + fH * 0.5, 7]), apt3: V3([4.3, fH + 0.6 + fH * 1.5, 7]), apt4: V3([4.3, fH + 0.6 + fH * 2.5, 7]),
    stair: V3([10.5 + bw / 2 - 1.6, BH * 0.55, 10 - bd / 2 + 2.0]), roof: V3([10.5, BH + 0.8, 10]), street: V3([0, 0.3, 0]), corner: V3([4.4, 0.4, 4.4]) };
  const sec = opt.section; const shopK = opt.shop ?? 1;
  const update = (t, f) => { rig.at(t); dst.update(t); ppl.forEach((p) => { p.f.root.position.x += p.sp * 0.02; p.f.set({ walk: t * 4 + p.ph }); });
    const u = sec ? win01(t, sec) : 0; inside.visible = u > 0.02;
    // cắt lớp: hai mặt hướng giao lộ mờ dần (mặt tiền + cửa sổ + cửa hàng)
    if (u > 0) shell.traverse((o) => { if (o.isMesh) { if (!o.userData.fade) { o.material = o.material.clone(); o.material.transparent = true; o.userData.fade = 1; } o.material.opacity = 1 - 0.88 * u; o.material.depthWrite = u < 0.5; } });
    shopMat.emissiveIntensity = (T.day ? 0.06 : 0.95) * shopK * (1 + 0.03 * Math.sin(f * 0.21)); };
  return { scene, cam: rig.cam, update, grade: T.grade, exposure: T.exp, anchors };
}

// =================================== street ===================================
async function street({ W, H, dur, opt }) {
  const mt = mats(); const T = TOD[opt.tod || 'day']; const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, T.fog, T.fd * 0.9); skyDome(scene, T.sky); const R = rng(9);
  tbox(220, 0.1, 120, mt.asph, 0, -0.05, 0, scene, 0.08); tbox(220, 0.25, 6, mt.walk, 0, 0.12, 6, scene, 0.35); tbox(220, 0.25, 60, std('#3e4a36', { roughness: 1 }), 0, 0.05, 40, scene, 0.1);
  // bốn kiểu toà nhỏ, trái → phải; mỗi toà một lô 12 m
  const lots = [
    { k: 'duplex', mk: () => house(-30, 15, { w: 8, d: 10, h: 6.2, mat: mt.clap, T, seed: 61 }), top: 9.6, x: -30 },
    { k: 'triplex', mk: () => walkup({ x: -15, z: 15, w: 8, d: 11, floors: 3, mat: mt.brick2, T, seed: 63, faces: ['z'] }), top: 10.8, x: -15 },
    { k: 'fourplex', mk: () => walkup({ x: 0, z: 15, w: 11, d: 11, floors: 2, mat: mt.stucco, T, seed: 67, faces: ['z'] }), top: 7.6, x: 0 },
    { k: 'walkup', mk: () => walkup({ x: 17, z: 15, w: 14, d: 14, floors: 5, mat: mt.brick, T, seed: 71, faces: ['z', 'x'] }), top: 17.2, x: 17 },
    { k: 'walkup2', mk: () => walkup({ x: 35, z: 15, w: 13, d: 13, floors: 4, mat: mt.brick3, T, seed: 73, shop: true, faces: ['z', 'x'] }), top: 14.4, x: 35 },
  ];
  const built = lots.map((l) => ({ ...l, o: l.mk() }));
  // bậc cửa, cây, đèn, xe
  for (let i = -5; i < 6; i++) tree(i * 8.5 + 3, 8.3, 0.85, R); for (let i = -3; i < 4; i++) lamp(i * 14, 8.6, !T.day);
  car(-22, 2.8, Math.PI / 2, '#7a3a30', R); car(8, 2.8, Math.PI / 2, '#3a5a6e', R); car(26, -2.8, -Math.PI / 2, '#8a8478', R);
  const ppl = people(8, [-40, 45, 5, 7.5], R);
  lightTod(scene, T, 60, [0, 0, 15]);
  const hlI = opt.hl ?? -1; const ring = new THREE.Mesh(new THREE.RingGeometry(6.5, 7.2, 48), basic(C.orange, { transparent: true, opacity: 0, side: THREE.DoubleSide })); ring.rotation.x = -Math.PI / 2; ring.position.set(hlI >= 0 ? lots[hlI].x : 0, 0.3, 15); scene.add(ring);
  const dst = dust(scene, [0, 5, 10], [90, 10, 20], 220, 9, T.day ? '#ffffff' : '#ffd9a8');
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [-46, 6, -10], l: [-14, 6, 14], mm: 32 }, { u: 1, p: [30, 6.5, -12], l: [16, 7, 14], mm: 32 }], CAM.street);
  const anchors = {}; built.forEach((b) => { anchors[b.k] = V3([b.x, b.top + 1.0, 15]); anchors[b.k + '_base'] = V3([b.x, 0.5, 9.4]); });
  const update = (t) => { rig.at(t); dst.update(t); ppl.forEach((p) => { p.f.root.position.x += p.sp * 0.025; p.f.set({ walk: t * 4 + p.ph }); }); ring.material.opacity = hlI >= 0 ? 0.85 * win01(t, opt.hlAt || [0, 0.6]) : 0; };
  return { scene, cam: rig.cam, update, grade: T.grade, exposure: T.exp, anchors };
}

// =================================== tiers (minh hoạ) ===================================
async function tiers({ W, H, dur, opt }) {
  const mt = mats(); const T = { ...TOD.day, day: true }; const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.006); const R = rng(14);
  tbox(220, 0.2, 220, std('#ffffff', { map: gridTex('#121b28', 8), roughness: 0.85 }), 0, -0.1, 0, scene, 0.02);
  box(64, 0.6, 46, std('#2a3340', { roughness: 0.7 }), 0, 0.3, 0);   // bệ sa bàn
  const Z = [{ x: -24, c: '#3CC2B0' }, { x: -8, c: '#7fb8a8' }, { x: 8, c: '#c9a24a' }, { x: 24, c: C.orange }];   // U-1..U-4
  const tiles = Z.map((z, i) => { const m = std(z.c, { roughness: 0.9, transparent: true, opacity: 0.0 }); const p = box(15.4, 0.08, 42, m, z.x, 0.66, 0); return p; });
  const tileBase = std('#cfc9bb', { roughness: 0.95 }); Z.forEach((z) => box(15.4, 0.05, 42, tileBase, z.x, 0.62, 0));
  for (let x = -16; x <= 16; x += 16) box(0.6, 0.1, 42, std('#3b4048'), x, 0.7, 0);   // đường ranh tầng khu
  box(64, 0.1, 1.2, std('#3b4048'), 0, 0.7, -8); box(64, 0.1, 1.2, std('#3b4048'), 0, 0.7, 8);
  const s = 0.45, TT = TOD.day; const grpOf = () => { const g = new THREE.Group(); scene.add(g); return g; };
  // U-1: nhà một hộ · U-2: nhà hai hộ · U-3: căn hộ · U-4: cửa hàng (+ mọi loại dưới, khu tích luỹ)
  const g1 = grpOf(); for (let i = 0; i < 9; i++) house(-29 + (i % 3) * 5, -15 + Math.floor(i / 3) * 13, { w: 3.2, d: 3.6, h: 1.8, mat: mt.clap, T: TT, seed: 80 + i, parent: g1 });
  const g2 = grpOf(); for (let i = 0; i < 6; i++) house(-12.5 + (i % 2) * 8, -15 + Math.floor(i / 2) * 13, { w: 4.2, d: 4.6, h: 3.2, mat: mt.clap2, T: TT, seed: 90 + i, parent: g2 });
  const g3 = grpOf(); const apts = []; for (let i = 0; i < 4; i++) apts.push(walkup({ x: 4.5 + (i % 2) * 7.5, z: -12 + Math.floor(i / 2) * 18, w: 5.5, d: 6, floors: 5, fH: 1.6, mat: mt.brick, T: TT, seed: 100 + i, parent: g3, cornice: true }));
  const g4 = grpOf(); for (let i = 0; i < 4; i++) walkup({ x: 20 + (i % 2) * 8, z: -12 + Math.floor(i / 2) * 18, w: 6, d: 6, floors: 2, fH: 1.8, mat: mt.stucco, T: TT, seed: 110 + i, parent: g4, shop: true });
  [g1, g2, g3, g4].forEach((g) => g.position.y = 0.66);
  // toà góc phố thử từng khu
  const probe = walkup({ x: 0, z: 0, w: 4, d: 4, floors: 4, fH: 1.4, mat: mt.brick3, T: TT, seed: 120, shop: true }); probe.group.visible = false;
  const pr = new THREE.Mesh(new THREE.RingGeometry(3.4, 3.9, 40), basic(C.red, { transparent: true, opacity: 0.9, side: THREE.DoubleSide })); pr.rotation.x = -Math.PI / 2; scene.add(pr); pr.visible = false;
  scene.add(new THREE.HemisphereLight('#a8b8d8', '#1a2230', 1.7));
  const sunD = new THREE.DirectionalLight('#fff1dc', 2.6); const sunAng = opt.sun ? 0.45 : 1.0; sunD.position.set(-30, 40 * sunAng, -10); sunD.castShadow = true; sunD.shadow.mapSize.set(2048, 2048); Object.assign(sunD.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40 }); scene.add(sunD);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.8); rim.position.set(30, 12, 40); scene.add(rim);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [0, 58, 34], l: [0, 0, 2], mm: 30 }, { u: 1, p: [-6, 50, 38], l: [0, 0, 0], mm: 30 }], CAM.tiers);
  const anchors = { u1: V3([-24, 4, -21]), u2: V3([-8, 6, -21]), u3: V3([8, 10, -21]), u4: V3([24, 5, -21]), probe: () => probe.group.position.clone().add(V3([0, 7.5, 0])), apt: V3([4.5, 9.5, -12]), small: V3([-12.5, 4.5, -2]) };
  const fills = opt.fill || [-1, -1, -1, -1]; const P = opt.probe;
  const update = (t) => { rig.at(t); tiles.forEach((m, i) => { m.material.opacity = 0.55 * (fills[i] < 0 ? 1 : win01(t, [fills[i], fills[i] + 0.8])); });
    if (P) { const n = P.zones.length, u = clamp01((t - P.at) / (P.step || 1.2)); const k = Math.min(n - 1, Math.floor(u * n * 0.999)); const zi = P.zones[k]; probe.group.visible = t >= P.at; pr.visible = t >= P.at;
      probe.group.position.set(Z[zi].x, 0.66, 0); pr.position.set(Z[zi].x, 0.75, 0); pr.material.color.set(zi === 3 ? C.teal : C.red); } };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.05, anchors };
}

// =================================== lot ===================================
async function lot({ W, H, dur, opt }) {
  const mt = mats(); const T = TOD.day; const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.006); const R = rng(21);
  tbox(200, 0.2, 200, std('#ffffff', { map: gridTex('#121b28', 8), roughness: 0.85 }), 0, -0.1, 0, scene, 0.02);
  tbox(70, 0.1, 70, mt.asph, 0, 0.05, 0, scene, 0.1); tbox(30, 0.2, 30, mt.walk, 10, 0.12, 10, scene, 0.3);
  const LW = 15, LD = 30; const lotM = std('#56634e', { roughness: 1 }); box(LW, 0.06, LD, lotM, 4 + LW / 2, 0.24, 4 + LD / 2);   // lô góc 15 × 30 m (minh hoạ)
  const edge = std(C.text, { emissive: '#ffffff', emissiveIntensity: 0.3 }); for (const [x, z, w, d] of [[4 + LW / 2, 4, LW, 0.12], [4 + LW / 2, 4 + LD, LW, 0.12], [4, 4 + LD / 2, 0.12, LD], [4 + LW, 4 + LD / 2, 0.12, LD]]) box(w, 0.1, d, edge, x, 0.32, z);
  // toà: chiều sâu co theo số ô đỗ
  const bld = walkup({ x: 4 + LW / 2, z: 4 + 8, w: LW - 2, d: 14, floors: 4, fH: 3.0, mat: mt.brick, T, seed: 130, shop: true }); bld.group.position.y = 0.25; box(LW - 2.3, 0.12, 13.7, std('#8a9098', { roughness: 0.95 }), 0, bld.H + 0.56, 0, bld.group);   // mái sỏi sáng (nhìn từ trên đọc được dấu chân toà)
  const n = opt.stalls ?? 8, gw = opt.grow || [0.5, dur - 0.5]; const stalls = [];
  for (let i = 0; i < n; i++) { const g = new THREE.Group(); const sx = 4 + 1.6 + (i % 5) * 2.7, sz = 4 + LD - 3 - Math.floor(i / 5) * 5.6; g.position.set(sx, 0.3, sz); scene.add(g);
    box(2.5, 0.04, 5.2, std('#3d4248', { roughness: 0.9 }), 0, 0, 0, g); box(0.1, 0.06, 5.2, basic('#e8e2d0'), -1.25, 0.02, 0, g); box(0.1, 0.06, 5.2, basic('#e8e2d0'), 1.25, 0.02, 0, g);
    const c = car(0, 0, 0, ['#7a3a30', '#3a5a6e', '#8a8478', '#2d3a2a', '#5a4a6a'][i % 5], R); g.add(c); c.position.set(0, 0, 0); c.scale.setScalar(0.92); stalls.push(g); }
  lightTod(scene, T, 40, [10, 0, 18]);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [11.5, 54, 19.5], l: [11.5, 0, 19.0], mm: 30 }, { u: 1, p: [11.5, 48, 21], l: [11.5, 0, 19.0], mm: 30 }], CAM.lot);
  const anchors = { lot: V3([4 + LW / 2, 0.5, 4 + LD + 1.5]), building: V3([4 + LW / 2, 13.5, 12]), parking: V3([4 + LW / 2, 1, 4 + LD - 5]), corner: V3([4, 0.4, 4]) };
  const update = (t) => { rig.at(t); const k = win01(t, gw); stalls.forEach((s, i) => { const u = clamp01(k * n - i); s.visible = u > 0.01; s.position.y = 0.3 + (1 - ease(u)) * 4; });
    const used = Math.ceil(k * n / 5) * 5.6; const d = Math.max(5, 14 - Math.max(0, used - 8)); bld.group.scale.z = d / 14; bld.group.position.z = 4 + d / 2 + 1; };
  return { scene, cam: rig.cam, update, grade: GRADE_K2_DAY, exposure: 1.0, anchors };
}

// =================================== stairs (mặt cắt) ===================================
async function stairs({ W, H, dur, opt }) {
  const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.008); const R = rng(27);
  box(200, 0.2, 200, std('#ffffff', { map: gridTex('#121b28', 8), roughness: 0.85 }), 0, -0.1, 0);
  const mode = opt.mode || 'compare'; const fH = 3.0; const NF = opt.floors || 4;
  const slab = std('#c9c3b6', { roughness: 0.8 }), wall = std('#8f969e', { roughness: 0.9, transparent: true, opacity: 0.32, depthWrite: false }), core1 = std(C.teal, { roughness: 0.5, emissive: '#0d3a34', emissiveIntensity: 0.6 }), core2 = std(C.orange, { roughness: 0.5, emissive: '#5a2a10', emissiveIntensity: 0.6 });
  const unitM = [std('#6a7a8c', { roughness: 0.8 }), std('#7a6a5a', { roughness: 0.8 }), std('#5a6a5a', { roughness: 0.8 }), std('#6a5a6a', { roughness: 0.8 })];
  // một toà = các tầng (sàn + 4 căn + lõi thang). ox: vị trí; two: có thang thứ hai + hành lang
  const build = (ox, two) => { const G = new THREE.Group(); G.position.set(ox, 0, 0); scene.add(G); const floors = []; const w = 14, d = 11;
    for (let f = 0; f < 6; f++) { const g = new THREE.Group(); g.position.y = f * fH; G.add(g); box(w, 0.25, d, slab, 0, 0.12, 0, g);
      // 4 căn (khối thấp có màu) chừa chỗ lõi thang
      const uw = two ? 5.4 : 6.0; [[-w / 2 + uw / 2 + 0.3, -d / 4 - 0.3], [w / 2 - uw / 2 - 0.3, -d / 4 - 0.3], [-w / 2 + uw / 2 + 0.3, d / 4 + 0.3], [w / 2 - uw / 2 - 0.3, d / 4 + 0.3]].forEach(([x, z], i) => box(uw, 0.9, d / 2 - 1.4, unitM[(i + f) % 4], x, 0.7, z, g));
      // lõi thang 1 (giữa) + bậc
      const c1 = new THREE.Group(); c1.position.set(0, 0, 0); g.add(c1); box(2.2, fH - 0.3, 2.6, core1, 0, fH / 2, 0, c1).material = core1;
      let c2 = null, corr = null; if (two) { c2 = new THREE.Group(); c2.position.set(w / 2 - 1.3, 0, 0); g.add(c2); box(2.2, fH - 0.3, 2.6, core2, 0, fH / 2, 0, c2); corr = box(w - 3.0, 0.3, 1.4, core2, 0.6, 0.32, 0, g); }
      box(w, fH - 0.3, 0.12, wall, 0, fH / 2, d / 2, g); box(0.12, fH - 0.3, d, wall, -w / 2, fH / 2, 0, g);
      floors.push(g); }
    return { G, floors, top: (n) => V3([ox, n * fH + 1.5, 0]) }; };
  const A = build(mode === 'compare' ? -10 : 0, mode === 'two'), Bb = mode === 'compare' ? build(10, true) : null;
  const npM = new THREE.MeshBasicMaterial({ color: C.red, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }); const np = new THREE.Mesh(new THREE.BoxGeometry(14.6, fH, 11.6), npM); np.position.set(A.G.position.x, 3 * fH + fH / 2, 0); scene.add(np);
  const npEdge = new THREE.LineSegments(new THREE.EdgesGeometry(np.geometry), new THREE.LineBasicMaterial({ color: C.red, transparent: true, opacity: 0 })); np.add(npEdge);
  // áp suất (mũi tên vào lõi thang kín) và 3 điều kiện cháy (đèn)
  const arrows = []; for (let i = 0; i < 6; i++) { const a = new THREE.Mesh(new THREE.ConeGeometry(0.35, 1.0, 10), basic(C.teal, { transparent: true, opacity: 0 })); a.rotation.z = i % 2 ? Math.PI / 2 : -Math.PI / 2; a.position.set(A.G.position.x + (i % 2 ? 2.3 : -2.3), 1.2 + Math.floor(i / 2) * fH, 0); scene.add(a); arrows.push(a); }
  const fireL = [0, 1, 2].map((i) => { const s = glowSprite([C.amber, C.orange, C.red][i], 0.0, 1.8); s.position.set(A.G.position.x - 4 + i * 4, 2 * fH + 2.2, -5.8); scene.add(s); return s; });
  scene.add(new THREE.HemisphereLight('#a8b8d8', '#1a2230', 1.8)); const key = new THREE.DirectionalLight('#ffffff', 2.4); key.position.set(-20, 40, 30); key.castShadow = true; key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30 }); scene.add(key);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.9); rim.position.set(30, 10, -30); scene.add(rim);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [26, 22, 34], l: [0, 6, 0], mm: 30 }, { u: 1, p: [20, 20, 36], l: [0, 6, 0], mm: 30 }], CAM.stairs);
  const anchors = { one: () => A.top(Math.min(NF, 3)), two: () => (Bb ? Bb.top(4) : A.top(4)), core1: V3([A.G.position.x, 2 * fH + 1.5, 0]), core2: V3([(Bb ? Bb.G.position.x : A.G.position.x) + 5.7, 2 * fH + 1.5, 0]),
    np: V3([A.G.position.x, 4 * fH + 0.6, 0]), floor4: V3([A.G.position.x + 7.5, 3 * fH + 1.5, 0]), fire1: () => fireL[0].position, fire2: () => fireL[1].position, fire3: () => fireL[2].position };
  const stackAt = opt.stackAt || [-1, -1]; const NPw = opt.np, PRw = opt.press, FIw = opt.fire;
  const update = (t) => { rig.at(t);
    [A, Bb].filter(Boolean).forEach((b) => b.floors.forEach((g, f) => { const shown = f < NF; const u = stackAt[0] < 0 ? 1 : clamp01((t - stackAt[0] - f * (stackAt[1] || 0.5)) / 0.45); g.visible = shown && u > 0.01; g.position.y = f * fH + (1 - ease(u)) * 3; }));
    const kn = NPw ? win01(t, NPw) : 0; npM.opacity = 0.22 * kn; npEdge.material.opacity = 0.95 * kn;
    const kp = PRw ? win01(t, PRw) : 0; arrows.forEach((a, i) => { a.material.opacity = kp * (0.55 + 0.45 * Math.sin(t * 5 + i)); });
    fireL.forEach((s, i) => { const k = FIw ? win01(t, [FIw[0] + i * (FIw[1] || 0.8), FIw[0] + i * (FIw[1] || 0.8) + 0.4]) : 0; s.material.opacity = 0.95 * k; }); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.05, anchors };
}

// =================================== bank ===================================
async function bank({ W, H, dur, opt }) {
  const mt = mats(); const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.008); const R = rng(33);
  box(200, 0.2, 200, std('#ffffff', { map: gridTex('#121b28', 8), roughness: 0.85 }), 0, -0.1, 0);
  // bàn quầy (hai cửa): single-family (trái) / multifamily (phải)
  const deskM = std('#3a2e24', { roughness: 0.6 }); tbox(12, 1.1, 2.2, deskM, -8, 0.55, -9, scene, 0.3); tbox(12, 1.1, 2.2, deskM, 10, 0.55, -9, scene, 0.3);
  const lampSF = glowSprite(C.teal, 0.9, 2.2), lampMF = glowSprite(C.steel, 0.6, 2.2); lampSF.position.set(-8, 2.6, -9); lampMF.position.set(10, 2.6, -9); scene.add(lampSF, lampMF);
  const plaqueSF = box(6, 1.4, 0.15, std(C.teal, { emissive: '#0d3a34', emissiveIntensity: 0.6 }), -8, 1.85, -9.95), plaqueMF = box(6, 1.4, 0.15, std('#5a6676', { emissive: '#1a2230', emissiveIntensity: 0.5 }), 10, 1.85, -9.95);
  // vạch "4": tấm kính đứng giữa
  const line = box(0.25, 4.2, 14, std(C.orange, { emissive: '#7a3a14', emissiveIntensity: 0.9, transparent: true, opacity: 0.85 }), 1.2, 2.1, 0);
  // khối nhà 1..4 (trái vạch) và 5 (phải); mỗi căn = một khối nhỏ xếp tầng
  const unit = new THREE.BoxGeometry(1.8, 1.2, 1.8); const mats5 = [mt.brick, mt.brick2, mt.brick3, mt.stucco, mt.clap];
  const stacks = [1, 2, 3, 4, 5].map((n, i) => { const g = new THREE.Group(); g.position.set(-11 + i * 3.2 + (n === 5 ? 3.4 : 0), 0, 0); scene.add(g);
    for (let k = 0; k < n; k++) { const m = new THREE.Mesh(unit, mats5[i % 5]); m.position.set(0, 0.6 + k * 1.25, 0); m.castShadow = m.receiveShadow = true; g.add(m);
      const w = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.6), new THREE.MeshStandardMaterial({ color: '#2a2a2a', emissive: '#ffcf8a', emissiveIntensity: 0.6 })); w.position.set(0, 0.6 + k * 1.25, 0.91); g.add(w); }
    box(2.1, 0.12, 2.1, mt.trim, 0, n * 1.25 + 0.06, 0, g); return g; });
  const shopL = stacks.map((g) => { const m = box(1.9, 0.9, 1.9, new THREE.MeshStandardMaterial({ color: '#2a2016', emissive: '#ffb066', emissiveIntensity: 0.9 }), 0, 0.45, 0, g); m.visible = false; return m; });
  scene.add(new THREE.HemisphereLight('#a8b8d8', '#1a2230', 1.6)); const key = new THREE.SpotLight('#ffffff', 2200, 120, 0.7, 0.6, 1.4); key.position.set(-12, 30, 22); key.target.position.set(0, 0, -2); key.castShadow = true; key.shadow.mapSize.set(2048, 2048); scene.add(key, key.target);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.9); rim.position.set(30, 12, -30); scene.add(rim); const warm = new THREE.PointLight(C.orange, 30, 18, 1.5); warm.position.set(1.2, 3, 3); scene.add(warm);
  const dst = dust(scene, [0, 4, 0], [30, 8, 20], 200, 33, '#b9c6d6');
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [0, 7, 24], l: [0, 2.5, -2], mm: 30 }, { u: 1, p: [-4, 7.5, 23], l: [0, 2.5, -2], mm: 30 }], CAM.bank);
  const anchors = { s1: V3([-11, 2.2, 0]), s4: V3([-1.4, 6.0, 0]), s5: () => stacks[4].position.clone().add(V3([0, 7.2, 0])), line: V3([1.2, 4.6, 0]), sf: V3([-8, 4.6, -10]), mf: V3([10, 4.6, -10]) };
  const fw = opt.fifth, shopOn = opt.shop, rej = opt.reject;
  const update = (t) => { rig.at(t); dst.update(t); const u = fw ? ease(win01(t, fw)) : 0; stacks[4].position.x = lerp(5.4, 9.8, u); stacks[4].position.z = lerp(0, -5.5, u);
    shopL.forEach((m, i) => { m.visible = !!shopOn && (i === 2 || i === 4); }); const kr = rej ? win01(t, rej) : 0; lampSF.material.color.set(kr > 0.5 ? C.amber : C.teal); lampMF.material.color.set(kr > 0.5 ? C.amber : C.steel); lampSF.material.opacity = lampMF.material.opacity = 0.6 + 0.35 * Math.max(kr, 0.5); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.08, anchors };
}

// =================================== ends ===================================
async function ends({ W, H, dur, opt }) {
  const mt = mats(); const T = TOD.day; const scene = new THREE.Scene(); window.__scene = scene; fogOf(scene, C.ink, 0.006); const R = rng(41);
  box(220, 0.2, 220, std('#ffffff', { map: gridTex('#121b28', 8), roughness: 0.85 }), 0, -0.1, 0);
  box(84, 0.6, 40, std('#2a3340', { roughness: 0.7 }), 0, 0.3, 0); tbox(82, 0.06, 38, std('#cfc9bb', { roughness: 0.95 }), 0, 0.63, 0, scene, 0.1);
  // trái: nhà một hộ (số lượng tăng theo năm); phải: toà ≥ 50 căn (cao dần); giữa: toà nhỏ (thưa dần)
  const houses = []; for (let i = 0; i < 40; i++) { const g = house(-38 + (i % 8) * 3.6, -16 + Math.floor(i / 8) * 7.5, { w: 2.4, d: 2.8, h: 1.4, mat: i % 2 ? mt.clap : mt.clap2, T, seed: 140 + i }); g.position.y = 0.63; houses.push(g); }
  const small = []; for (let i = 0; i < 12; i++) { const o = walkup({ x: -6 + (i % 4) * 4.2, z: -14 + Math.floor(i / 4) * 12, w: 3.2, d: 3.4, floors: 3 + (i % 2), fH: 1.2, mat: [mt.brick, mt.brick2, mt.brick3][i % 3], T, seed: 160 + i }); o.group.position.y = 0.63; small.push(o.group); }
  const big = []; for (let i = 0; i < 4; i++) { const o = walkup({ x: 26 + (i % 2) * 9, z: -10 + Math.floor(i / 2) * 18, w: 7.5, d: 9, floors: 12, fH: 1.2, mat: mt.conc, T, seed: 180 + i }); o.group.position.y = 0.63; big.push(o.group); }
  scene.add(new THREE.HemisphereLight('#a8b8d8', '#1a2230', 1.7)); const sunD = new THREE.DirectionalLight('#fff1dc', 2.6); sunD.position.set(-30, 40, 20); sunD.castShadow = true; sunD.shadow.mapSize.set(2048, 2048); Object.assign(sunD.shadow.camera, { left: -50, right: 50, top: 40, bottom: -40 }); scene.add(sunD);
  const rim = new THREE.DirectionalLight('#5fa9c9', 0.8); rim.position.set(30, 12, -40); scene.add(rim);
  const rig = rigOf(W, H, dur, opt, [{ u: 0, p: [0, 42, 52], l: [0, 2, 0], mm: 30 }, { u: 1, p: [6, 40, 54], l: [0, 2, 0], mm: 30 }], CAM.ends);
  const anchors = { houses: V3([-25, 5, -18]), small: V3([0, 7, -18]), big: V3([30, 17, -18]) };
  const y0 = opt.year ?? 1972, y1 = opt.year1 ?? y0, yw = opt.yearAt || [0, dur];
  const update = (t) => { rig.at(t); const y = lerp(y0, y1, ease(win01(t, yw))); const k = clamp01((y - 1972) / (2025 - 1972));
    houses.forEach((h, i) => { h.visible = i < 24 + k * 16; }); small.forEach((s, i) => { s.visible = i < Math.round(12 - k * 8); }); big.forEach((b, i) => { b.scale.y = 0.45 + 0.55 * k; b.visible = i < 2 + Math.round(k * 2); }); };
  return { scene, cam: rig.cam, update, grade: GRADE_K2, exposure: 1.05, anchors };
}

export const HEROES = { corner, street, tiers, lot, stairs, bank, ends };

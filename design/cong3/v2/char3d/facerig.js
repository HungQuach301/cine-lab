// Cine Lab · Cổng 5 v2 · W3 — MẶT IDA A-i (quyết định chủ dự án: đảo C′ của Cổng 3).
// Mặt ĐIÊU KHẮC trong lưới (không vẽ nét lên đầu): gờ mày, mí dày, môi có khối, khe môi thật (rãnh), nhân trung, rãnh mũi–má là ranh giới khối,
// cằm, khối dưới cằm liền cổ. RIG BIỂU CẢM bằng morph CPU (tương đương blendshape; tính trên CPU để mọi pass — kể cả G-buffer lớp vẽ có
// vertex shader riêng — thấy đúng hình): kênh mày, mí chớp/nheo, khoé miệng, hàm mở, mím, chu, kéo rộng, môi dưới vào (F-V), cằm, má.
// Bộ khẩu hình Cổng 6: A, E, O, MBP, FV, L. Biểu cảm neutral / sad_smile / strained / choked dựng lại trên rig.
// Mắt: nhãn cầu riêng, vật liệu có phản xạ (giác mạc bắt sáng thật từ đèn cảnh), mi trên là KHỐI mi dày tối đi theo mí khi chớp,
// đường nước ở mí dưới. Da: sắc độ bằng màu đỉnh (ấm mũi/má/tai, mát dưới mắt), tán xạ dưới da giả lập (ánh sáng "bọc" ấm ở ranh sáng tối).
// Đơn vị: H (chiều dài đầu). Hệ đầu: y = 0 cằm, 1 đỉnh sọ, +z mặt, x trái nhân vật.
import * as THREE from '../../shared/node_modules/three/build/three.module.js';
import { ell, sph, cap, smin, smax, gauss, sstep, sculpt, fbm } from './sdf.js';

export const AI_E = [0.148, 0.575, 0.292];   // tâm nhãn cầu
export const AI_ER = 0.064;                   // bán kính nhãn cầu (cách điệu: lớn hơn A1 0,058)
const MY = 0.266, MW = 0.07, MZ = 0.385;   // MZ: độ sâu tâm khe môi (A-i: miệng + cằm đưa ra trước 0,025 H — bản đầu lõm như người móm)                 // khe môi: độ cao, nửa bề rộng miệng

// ---------------- hình khối đầu (SDF) ----------------
// Rãnh/gờ mềm theo đường gấp khúc chiếu trước (ax, y) — dùng cho nếp tuổi dạng KHỐI (rộng ≥ 0,01 H, không nét mảnh).
const g2 = (ax, y, pts, w) => { let d = 1e9; for (let i = 0; i < pts.length - 1; i++) { const [a0, a1] = pts[i], [b0, b1] = pts[i + 1], bx = b0 - a0, by = b1 - a1;
  const h = Math.max(0, Math.min(1, ((ax - a0) * bx + (y - a1) * by) / (bx * bx + by * by))); d = Math.min(d, Math.hypot(ax - a0 - bx * h, y - a1 - by * h)); } return gauss(d, w); };
export const lipY = (x, y) => y + 0.7 * x * x;   // hệ môi uốn: khoé miệng cụp nhẹ (tuổi)
export function aiHeadSDF(x, y, z) {
  const ax = Math.sqrt(x * x + 1e-4), E = AI_E, ER = AI_ER, fr = (z0) => sstep(z0, z0 + 0.1, z), yb = lipY(x, y);   // |x| TRƠN (ε = 0,01 H): hết nếp gãy pháp tuyến dọc đường giữa mặt
  let d = ell(x, y, z, [0, 0.59, -0.03], [0.385, 0.41, 0.44]);                                  // sọ (đỉnh ≈ 1,0 H)
  d = smin(d, ell(x, y, z, [0, 0.41, 0.105], [0.30, 0.30, 0.31]), 0.12);                          // khối giữa mặt
  d = smin(d, ell(ax, y, z, [0.15, 0.34, 0.21], [0.10, 0.13, 0.11]), 0.13);                      // má đầy mềm (cao — mặt nữ tròn)
  d = smin(d, ell(x, y, z, [0, 0.155, 0.245], [0.085, 0.09, 0.09]), 0.12);                         // cằm tròn nhỏ
  d = smin(d, sph(x, y, z, [0, 0.145, 0.28], 0.048), 0.05);                                       // đệm cằm
  d = smin(d, ell(x, y, z, [0, 0.085, 0.11], [0.13, 0.07, 0.13]), 0.12);                          // khối dưới cằm (da chùng, nối cổ)
  d = smin(d, ell(ax, y, z, [0.15, 0.2, 0.18], [0.045, 0.045, 0.045]), 0.08);
  d = smin(d, ell(x, y, z, [0, -0.06, 0.035], [0.178, 0.27, 0.212]), 0.05);                                        // CỔ LIỀN HÀM: phần cổ trên là cùng một lưới với đầu (lượn mềm từ hàm/dưới cằm xuống), bọc ngoài ống cổ của thân                      // má chùng nhẹ trên đường hàm (tuổi)
  d = smin(d, ell(ax, y, z, [0.215, 0.49, 0.25], [0.085, 0.05, 0.08]), 0.09);                     // gò má cao
  d = smin(d, ell(ax, y, z, [0.13, 0.355, 0.30], [0.06, 0.08, 0.045]), 0.09);                     // đệm má (ngoài rãnh mũi–má)
  d += (0.0035 * g2(ax, y, [[0.058, 0.43], [0.085, 0.36], [0.104, 0.3], [0.112, 0.27]], 0.021)       // RÃNH MŨI–MÁ: lõm phía trong…
    - 0.003 * g2(ax, y, [[0.085, 0.42], [0.112, 0.35], [0.13, 0.29]], 0.024)) * fr(0.22);           // …gờ má phủ phía ngoài (nếp gấp là khối; dừng trên khoé miệng — không kéo xuống cằm kiểu 'hàm rối')
  d += (0.0022 * g2(ax, y, [[0.075, 0.495], [0.13, 0.476], [0.19, 0.49]], 0.014)                   // rãnh dưới bọng mắt
    - 0.0025 * g2(ax, y, [[0.09, 0.515], [0.145, 0.505], [0.195, 0.515]], 0.014)) * fr(0.25);        // bọng dưới mắt
  d += 0.0025 * (gauss(y - 0.745 - 0.12 * ax * ax, 0.012) + gauss(y - 0.785 - 0.12 * ax * ax, 0.012)) * sstep(0.28, 0.08, ax) * fr(0.25);   // nếp trán mềm
  d = smin(d, cap(ax, y, z, [0.02, 0.668, 0.385], [0.22, 0.656, 0.305], 0.04, 0.028), 0.05);      // gờ mày
  d = smax(d, -ell(ax, y, z, [E[0], E[1] + 0.008, 0.365], [0.10, 0.074, 0.075]), 0.04);            // hốc mắt
  const lid = sph(ax, y, z, E, ER + 0.012);
  d = smin(d, smax(lid, -(y - (E[1] + 0.025 - 0.035 * (ax - E[0]))), 0.012), 0.02);                // mí trên DÀY (khối), đuôi cụp
  d = smin(d, smax(lid, y - (E[1] - 0.037), 0.01), 0.012);                                         // mí dưới
  d = smin(d, cap(ax, y, z, [0.09, 0.628, 0.34], [0.215, 0.605, 0.30], 0.02), 0.03);                // da chùng trên mí (mí sụp tuổi: khối)
  d = smin(d, cap(x, y, z, [0, 0.625, 0.37], [0, 0.47, 0.462], 0.028, 0.034), 0.04);                // sống mũi dài
  d = smin(d, sph(x, y, z, [0, 0.535, 0.435], 0.03), 0.03);                                         // gồ mũi
  d = smin(d, sph(x, y, z, [0, 0.438, 0.482], 0.036), 0.035);                                       // đầu mũi
  d = smin(d, sph(x, y, z, [0, 0.415, 0.47], 0.03), 0.03);                                          // khoằm
  d = smin(d, sph(ax, y, z, [0.045, 0.418, 0.43], 0.031), 0.03);                                    // cánh mũi
  d = smax(d, -ell(ax, y, z, [0.026, 0.403, 0.45], [0.013, 0.008, 0.016]), 0.016);                 // lỗ mũi
  // môi trên (mỏng — tuổi) + môi dưới có khối: hợp với nhau bằng nối NHỎ → đường môi là NẾP HÌNH HỌC (rãnh chữ V giữa hai khối), không khoét khe
  const lips = smin(ell(x, yb, z, [0, MY + 0.018, MZ - 0.008], [0.074, 0.017, 0.029]), ell(x, yb, z, [0, MY - 0.02, MZ - 0.019], [0.064, 0.021, 0.031]), 0.004);
  d = smin(d, lips, 0.05);
  d += 0.004 * gauss(ax, 0.013) * gauss(y - 0.33, 0.026) * fr(0.35);                               // nhân trung (rãnh khối)
  d = smax(d, -ell(x, yb, z, [0, MY, MZ + 0.03], [MW, 0.0012, 0.03]), 0.003);                       // khe môi nông ở mặt trước (sắc nét đường môi)
  d += 0.006 * gauss(y - 0.195, 0.02) * gauss(ax, 0.07) * fr(0.2);                                 // hõm môi–cằm
  return d;
}

// ---------------- kênh rig (dịch chuyển tại điểm trung tính, đơn vị H) ----------------
export const CHANNELS = ['browUp', 'browDown', 'browInnerUp', 'browKnit', 'blink', 'lidDrop', 'squint', 'cheekRaise', 'smile', 'frown',
  'jawOpen', 'press', 'pucker', 'wide', 'lowerLipIn', 'chinRaise'];
function channelDisp(ch, x, y, z) {
  const E = AI_E, ER = AI_ER, ax = Math.abs(x), sx = x < 0 ? -1 : 1, fm = sstep(0.05, 0.25, z); if (fm <= 0 && ch !== 'jawOpen') return null;
  const gp = (cx, cy, r) => gauss(Math.hypot(ax - cx, y - cy), r);
  let dx = 0, dy = 0, dz = 0, k;
  const lidRot = (thUp, thLo) => {   // xoay vỏ mí quanh tâm nhãn cầu (giữ khoảng cách tới mắt)
    const Y = y - E[1], Z = z - E[2], rr = Math.hypot(ax - E[0], Y, Z), shell = gauss(rr - ER - 0.012, 0.022) * gauss(ax - E[0], 0.085);
    const th = thUp * sstep(-0.012, 0.012, Y) * shell + thLo * sstep(0.005, -0.02, Y) * shell;
    if (th) { const c = Math.cos(th), s = Math.sin(th); dy += (Y * c - Z * s) - Y; dz += (Y * s + Z * c) - Z; } };
  switch (ch) {
    case 'browUp': k = gauss(y - 0.66, 0.05) * gauss(ax - 0.13, 0.13); dy += 0.03 * k; k = gauss(ax, 0.2) * gauss(y - 0.76, 0.07); dy += 0.012 * k; break;
    case 'browDown': k = gauss(y - 0.66, 0.05) * gauss(ax - 0.13, 0.13); dy -= 0.02 * k; dz += 0.006 * k; break;
    case 'browInnerUp': k = gp(0.05, 0.66, 0.055); dy += 0.045 * k; k = gauss(ax, 0.1) * gauss(y - 0.75, 0.06); dy += 0.015 * k; break;
    case 'browKnit': k = gp(0.05, 0.655, 0.05); dx -= sx * 0.014 * k * sstep(0, 0.04, ax); dy -= 0.006 * k; dz += 0.006 * k; break;
    case 'blink': lidRot(0.78, -0.08); break;
    case 'lidDrop': lidRot(0.30, 0); break;
    case 'squint': lidRot(0.12, -0.32); k = gp(0.2, 0.47, 0.06); dy += 0.006 * k; break;
    case 'cheekRaise': k = gp(0.15, 0.37, 0.07); dy += 0.018 * k; dz += 0.012 * k; lidRot(0, -0.15); break;
    case 'smile': k = gp(MW, MY, 0.05); dy += 0.05 * k; dx += sx * 0.024 * k; dz -= 0.018 * k; k = gauss(ax, 0.06) * gauss(y - MY - 0.015, 0.02) * fm; dy += 0.004 * k; k = gp(0.14, 0.34, 0.06); dy += 0.02 * k; dz += 0.016 * k; k = gauss(ax, 0.05) * gauss(y - MY + 0.022, 0.02) * fm; dz -= 0.007 * k; dy += 0.003 * k; break;   // môi dưới kéo phẳng (không bĩu)
    case 'frown': k = gp(MW, MY, 0.045); dy -= 0.036 * k; dz -= 0.004 * k; k = gp(MW + 0.015, MY - 0.05, 0.035); dy -= 0.01 * k; break;
    case 'jawOpen': {   // xoay hàm dưới quanh bản lề gần tai; chỉ phần dưới khe môi
      const yb = lipY(x, y), spread = 0.004 + 0.11 * sstep(0.045, 0.22, ax);   // giữa: tách gọn ở khe môi; khoé–má: chuyển mềm (má giãn, không 'hàm rối gỗ')
      const w = sstep(MY + 0.002, MY - spread, yb) * sstep(-0.12, 0.05, z) * sstep(0.36, 0.26, ax) * sstep(-0.04, 0.08, y);   // cổ không theo hàm
      if (w) { const a = 0.24 * w, hy = 0.42, hz = -0.03, Y = y - hy, Z = z - hz, c = Math.cos(a), s = Math.sin(a);
        dy += (Y * c - Z * s) - Y; dz += (Y * s + Z * c) - Z; }   // quay quanh trục x (+a: cằm xuống–ra sau), như rotation.x = +a
      k = gauss(ax, 0.07) * gauss(y - MY - 0.02, 0.015) * fm; dy += 0.008 * k;   // môi trên nhích lên
      k = sstep(0.007, 0.003, Math.abs(yb - MY)) * sstep(0.3, 0.34, z) * sstep(MW + 0.004, MW - 0.012, ax) * fm; dz -= 0.055 * k;   // vách trong khe môi lùi sâu → hốc miệng có chiều sâu (răng lộ phía trước)
      break; }
    case 'press': k = gauss(ax, 0.06) * gauss(y - MY - 0.02, 0.016) * fm; dy -= 0.006 * k; dz -= 0.004 * k; k = gauss(ax, 0.06) * gauss(y - MY + 0.022, 0.018) * fm; dy += 0.007 * k; dz -= 0.003 * k; break;
    case 'pucker': k = gauss(ax, 0.08) * gauss(y - MY, 0.04) * fm; dz += 0.02 * k; dx -= sx * 0.014 * k * sstep(0, 0.06, ax); k = gp(MW, MY, 0.04) * fm; dx -= sx * 0.028 * k; dz += 0.008 * k; break;   // khoé miệng co vào → miệng tròn
    case 'wide': k = gp(MW, MY, 0.05); dx += sx * 0.018 * k; dz -= 0.006 * k; dy += 0.004 * k; break;
    case 'lowerLipIn': k = gauss(ax, 0.06) * gauss(y - MY + 0.024, 0.018) * fm; dy += 0.012 * k; dz -= 0.014 * k; break;
    case 'chinRaise': k = gp(0, 0.15, 0.06); dy += 0.012 * k; dz += 0.008 * k; k = gauss(ax, 0.05) * gauss(y - MY + 0.03, 0.02); dz += 0.006 * k; break;
  }
  return (dx || dy || dz) ? [dx * (ch === 'jawOpen' ? 1 : fm), dy * (ch === 'jawOpen' ? 1 : fm), dz * (ch === 'jawOpen' ? 1 : fm)] : null;
}
export function faceDisp(w, x, y, z) { let dx = 0, dy = 0, dz = 0; for (const [ch, v] of Object.entries(w || {})) { if (!v) continue; const d = channelDisp(ch, x, y, z); if (d) { dx += v * d[0]; dy += v * d[1]; dz += v * d[2]; } } return [dx, dy, dz]; }

// Biểu cảm (dựng lại trên rig) và khẩu hình.
export const FACE_PRESETS = {
  neutral: {},
  sad_smile: { smile: 1.0, cheekRaise: 0.8, browInnerUp: 0.6, browKnit: 0.15, squint: 0.45 },   // cười (khoé lên, má nâng, mí dưới nâng) + đầu trong mày nâng nhẹ = cười buồn
  strained: { press: 0.8, browKnit: 0.8, browDown: 0.3, chinRaise: 0.4 },
  choked: { frown: 1.0, browInnerUp: 1.0, browKnit: 0.65, chinRaise: 1.0, press: 0.6, lidDrop: 0.25, squint: 0.2 },
};
export const VISEMES = {
  rest: {}, A: { jawOpen: 0.75, wide: 0.1 }, E: { jawOpen: 0.3, wide: 0.7 }, O: { jawOpen: 0.5, pucker: 0.9 },
  MBP: { press: 1.0 }, FV: { lowerLipIn: 1.0, jawOpen: 0.1 }, L: { jawOpen: 0.4, wide: 0.25 },
};
export const mixW = (...ws) => { const o = {}; for (const w of ws) for (const [k, v] of Object.entries(w || {})) o[k] = (o[k] || 0) + v; return o; };

// ---------------- dựng đầu + mắt + mày + rig ----------------
// p = { H, R, hq, headG, add(parent, geo, role, color, part), parts, matFn, C, opts, strandGeo, aoCol, gaze }
export function buildIdaFace(p) {
  const { H, R, headG, add, parts, matFn, C, opts, strandGeo, aoCol } = p, E = AI_E, ER = AI_ER, hq = p.hq ?? 1;
  // Sắc độ da bằng màu đỉnh (không nét): ấm mũi/má, mát dưới mắt, môi hồng, lòng miệng tối, che khuất dưới hàm và dưới vành mũ.
  const tint = (x, y, z, n) => {
    const ax = Math.abs(x), gp = (cx, cy, r) => gauss(Math.hypot(ax - cx, y - cy), r), fz = sstep(0.1, 0.3, z);
    let r = 1, g = 1, b = 1;
    const warm = (0.10 * gp(0.17, 0.37, 0.08) + 0.12 * gp(0, 0.44, 0.05)) * fz; r += warm * 0.2; g -= warm * 0.9; b -= warm * 1.0;       // má, mũi ấm hồng
    const cool = 0.07 * gp(0.14, 0.50, 0.035) * fz; r -= cool * 0.7; g -= cool * 0.5; b -= cool * 0.2;                                // dưới mắt mát
    const yb = lipY(x, y), lip = sstep(0.018, 0.0, Math.hypot(ax / 1.15, (yb - MY) / 0.75) - 0.05) * fz; r -= 0.03 * lip; g -= 0.30 * lip; b -= 0.25 * lip;   // môi hồng xỉn (vùng, không nét)
    const inner = sstep(0.009, 0.004, Math.abs(yb - MY)) * sstep(MZ + 0.03, MZ + 0.012, z) * sstep(MW + 0.008, MW - 0.004, ax);                        // vách trong môi tối dần
    const nost = sstep(0.018, 0.003, ell(ax, y, z, [0.026, 0.403, 0.45], [0.013, 0.008, 0.016]));   // lòng lỗ mũi tối (không đốm sáng 'khuyên mũi')
    const mot = fbm(x * 9, y * 9, z * 9, 3, 41) * fz, spot = Math.max(0, fbm(x * 26, y * 26, z * 26, 2, 53) - 0.28) * sstep(0.55, 0.8, y) * fz;   // da không phẳng: loang hồng nhẹ + vài đốm tuổi mờ ở trán/thái dương
    r += 0.03 * mot; g -= 0.02 * mot; b -= 0.03 * mot; r -= 0.25 * spot; g -= 0.35 * spot; b -= 0.45 * spot;
    const occ = Math.max(0.45 * sstep(-0.15, -0.75, n[1]) * sstep(0.34, 0.12, y), 0.3 * sstep(0.70, 0.80, y), 0.35 * sstep(0.12, 0.0, y) * sstep(-0.3, -0.05, y) * sstep(0.25, 0.1, z) + 0.1 * sstep(0.0, -0.3, y));   // cổ: tối dưới bóng hàm
    const k = (1 - occ) * (1 - 0.85 * inner) * (1 - 0.88 * nost);
    return [r * k, g * k * (1 - 0.4 * inner), b * k * (1 - 0.35 * inner)];   // vách trong môi: đỏ sẫm ướt
  };
  const geo = sculpt(aiHeadSDF, { c: [0, 0.48, 0.02], r: [0.45, 0.8, 0.6], nu: R(210 * hq), nv: R(165 * hq), scale: H, uv: [6, 3], gradE: 0.002, warp: [0.4, 0.62], eps: 2e-5,
    color: aoCol(aiHeadSDF, 0.2, tint) });
  const head = add(headG, geo, 'skin', C.skin, 'head');
  // Lòng miệng: vách trong khe môi (màu đỉnh đỏ sẫm) giãn ra khi hàm mở; răng trên cố định nằm trong khối môi trên (lộ mép khi môi trên nâng),
  // răng dưới theo hàm (quay quanh bản lề cùng góc kênh jawOpen). Không khoét lỗ lưới (mép lỗ răng cưa ở độ phân giải này).
  const JH = [0, 0.42, -0.03], jaw = new THREE.Group(); jaw.position.set(0, JH[1] * H, JH[2] * H); headG.add(jaw);
  { const arc = (yc, rr, zc, a) => { const pts = []; for (let i = 0; i <= 8; i++) { const t = -a + 2 * a * i / 8; pts.push([Math.sin(t) * rr * H, yc * H, (zc + Math.cos(t) * rr) * H]); } return pts; };
    const teethM = matFn('skin', '#cfc4b2', 'teeth', {});
    const ut = new THREE.Mesh(strandGeo(arc(MY + 0.02, 0.05, MZ - 0.088, 0.75), () => [0.003 * H, 0.0075 * H], 6, 16), teethM); ut.userData.part = 'teeth'; headG.add(ut); parts.push(ut);
    const lt = new THREE.Mesh(strandGeo(arc(MY - 0.02, 0.046, MZ - 0.09, 0.7), () => [0.003 * H, 0.0065 * H], 6, 16), teethM); lt.userData.part = 'teeth'; lt.position.set(0, -JH[1] * H, -JH[2] * H); jaw.add(lt); parts.push(lt); }
  // Da: Lambert + "bọc" ánh sáng theo kênh màu (đỏ lan sâu hơn qua ranh sáng tối — tán xạ dưới da giả lập) + giữ sắc ấm khi ánh lạnh.
  // Da (A-i): vật liệu PBR riêng (bóng da mềm: nhám 0,5 — ánh bóng nhẹ ở mũi, trán, gò má, môi; Lambert cũ đọc thành sáp/đất sét)
  //  + khuếch tán "bọc" lệch đỏ (tán xạ dưới da giả lập: ranh sáng–tối ấm, mềm) + giữ sắc ấm khi ánh lạnh (skinWarm như bản cũ).
  const mat = new THREE.MeshStandardMaterial({ color: new THREE.Color(C.skin), roughness: opts.skinRough ?? 0.42, metalness: 0, vertexColors: true, map: head.material.map || null, envMapIntensity: 0 });
  const warm = opts.skinWarm ?? 0.7, spec = opts.skinSpec ?? 1.0;
  const phys = THREE.ShaderChunk.lights_physical_pars_fragment
    .replace('reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );',
      `{ float nlW = dot( geometryNormal, directLight.direction ); vec3 wr = vec3( 0.34, 0.16, 0.11 );
        reflectedLight.directDiffuse += clamp( ( vec3( nlW ) + wr ) / ( 1.0 + wr ), 0.0, 1.0 ) * directLight.color * BRDF_Lambert( material.diffuseColor ); }`)
    .replace('reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );',
      'reflectedLight.directSpecular += ' + spec.toFixed(3) + ' * irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );');
  if (phys === THREE.ShaderChunk.lights_physical_pars_fragment) console.warn('facerig: không vá được lights_physical_pars_fragment');
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('#include <lights_physical_pars_fragment>', phys)
      .replace('vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;',
        `vec3 alb = max(diffuseColor.rgb, vec3(1e-3)); vec3 eSk = totalDiffuse / alb;
         float lSk = dot(eSk, vec3(0.2126, 0.7152, 0.0722)), cSk = smoothstep(0.0, 0.25, (eSk.b - eSk.r) / max(lSk, 1e-5));
         eSk = mix(eSk, lSk * vec3(1.06, 1.0, 0.92), ${warm.toFixed(3)} * cSk);
         vec3 outgoingLight = eSk * alb + totalSpecular + totalEmissiveRadiance;`); };
  mat.customProgramCacheKey = () => '|aiSkin' + warm + '|' + spec;
  head.material = mat;

  // ---- morph CPU ----
  const pa = geo.attributes.position, nA = geo.attributes.normal, n = pa.count;
  const P0 = Float32Array.from(pa.array), N0 = Float32Array.from(nA.array);
  const gN = geo.clone(); gN.computeVertexNormals(); const Nm0 = Float32Array.from(gN.attributes.normal.array); gN.dispose();
  const deltas = {};
  for (const chn of CHANNELS) { const idx = [], dv = [];
    for (let i = 0; i < n; i++) { const d = channelDisp(chn, P0[i * 3] / H, P0[i * 3 + 1] / H, P0[i * 3 + 2] / H); if (d && (Math.abs(d[0]) + Math.abs(d[1]) + Math.abs(d[2]) > 1e-6)) { idx.push(i); dv.push(d[0] * H, d[1] * H, d[2] * H); } }
    deltas[chn] = { idx: Uint32Array.from(idx), dv: Float32Array.from(dv) }; }

  // ---- mắt ----
  const eyeTex = (() => {
    const cv = document.createElement('canvas'); cv.width = 512; cv.height = 256; const g = cv.getContext('2d');
    g.fillStyle = '#bdb3a8'; g.fillRect(0, 0, 512, 256);                                   // lòng trắng ngà vừa (không phát sáng, không đỏ)
    const cx = 128, cy = 128, ri = 46;
    const gr = g.createRadialGradient(cx, cy, ri * 0.2, cx, cy, ri); gr.addColorStop(0, '#4a4a48'); gr.addColorStop(0.5, '#403f3d'); gr.addColorStop(0.8, C.eyes || '#5a4636'); gr.addColorStop(0.9, '#23211f'); gr.addColorStop(1, '#141416');   // tròng nâu XÁM lệch lạnh: grade cảnh nâng vùng tối về ấm (bóng đổ ấm) → tròng nâu ấm cũ thành đỏ ('mắt đỏ, ma', lần 6); vòng #5a4636 của sheet ở rìa   // tròng nâu xám (dưới điện trắng + grade ấm không ngả đỏ cam)
    g.fillStyle = gr; g.beginPath(); g.arc(cx, cy, ri, 0, Math.PI * 2); g.fill();
    for (let k = 0; k < 96; k++) { const a = k / 96 * Math.PI * 2, r0 = ri * 0.45, r1 = ri * (0.72 + 0.18 * Math.sin(k * 7.3));
      g.strokeStyle = k % 2 ? 'rgba(150,118,84,0.22)' : 'rgba(40,28,22,0.2)'; g.lineWidth = 2.2; g.beginPath(); g.moveTo(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0); g.lineTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1); g.stroke(); }
    const pg = g.createRadialGradient(cx, cy, ri * 0.33, cx, cy, ri * 0.45); pg.addColorStop(0, 'rgba(8,10,14,1)'); pg.addColorStop(1, 'rgba(8,10,14,0)');   // con ngươi mép mềm
    g.fillStyle = pg; g.beginPath(); g.arc(cx, cy, ri * 0.45, 0, Math.PI * 2); g.fill();
    const lg = g.createRadialGradient(cx, cy, ri * 0.98, cx, cy, ri * 1.35); lg.addColorStop(0, 'rgba(60,44,36,0.55)'); lg.addColorStop(1, 'rgba(60,44,36,0)');   // viền tròng tan vào lòng trắng (không 'mắt kính')
    g.fillStyle = lg; g.beginPath(); g.arc(cx, cy, ri * 1.35, 0, Math.PI * 2); g.fill();
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const eyeMat = new THREE.MeshPhysicalMaterial({ map: eyeTex, roughness: 0.45, metalness: 0.0, clearcoat: 1.0, clearcoatRoughness: 0.06, vertexColors: true, envMapIntensity: 0 });   // lớp ướt (clearcoat) bắt điểm sáng nhỏ gọn; nền nhám (không 'bi thuỷ tinh')   // giác mạc bắt sáng THẬT (phản xạ đèn cảnh)
  { const en = opts.eyeNeutral ?? 0.65;   // mắt giữ màu dưới ánh hổ phách/điện: sắc ánh sáng tới mắt kéo về trung tính (như tóc bạc) — hết "mắt đỏ, ma" (lần 6, s39)
    eyeMat.onBeforeCompile = (sh) => { sh.fragmentShader = sh.fragmentShader.replace('vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;',
      `vec3 albE = max(diffuseColor.rgb, vec3(1e-3)); vec3 eE = totalDiffuse / albE; float lE = dot(eE, vec3(0.2126, 0.7152, 0.0722));
       vec3 outgoingLight = mix(eE, vec3(lE), ${en.toFixed(3)}) * albE + totalSpecular + totalEmissiveRadiance;`); };
    eyeMat.customProgramCacheKey = () => '|aiEye' + en; }
  const eyes = [];
  for (const sx of [1, -1]) {
    const eg = new THREE.SphereGeometry(ER * H, R(28), R(20));
    { const q = eg.attributes.position, col = new Float32Array(q.count * 3); for (let i = 0; i < q.count; i++) { const yy = q.getY(i) / (ER * H), a = 1 - 0.5 * sstep(0.15, 0.8, yy); col.set([a, a * 0.97, a * 0.97], i * 3); } eg.setAttribute('color', new THREE.BufferAttribute(col, 3)); }   // bóng mí trên trên nhãn cầu
    const e = new THREE.Mesh(eg, eyeMat); e.userData.part = 'eyes'; e.castShadow = true; e.receiveShadow = true; headG.add(e); parts.push(e);
    e.position.set(sx * E[0] * H, E[1] * H, E[2] * H); e.rotation.set(0.1 + (opts.gaze?.[1] ?? 0), sx * 0.025 + (opts.gaze?.[0] ?? 0), 0); eyes.push(e);
  }
  // Khối mi trên (dày, tối) và đường nước mí dưới — gắn trục quay tại tâm nhãn cầu, quay theo mí khi chớp/nheo.
  const lidPivots = [];
  const lashMat = matFn('hair', '#3a302c', 'lash', { vertexColors: false });
  const waterMat = new THREE.MeshStandardMaterial({ color: '#c98f86', roughness: 0.2, metalness: 0, emissive: new THREE.Color('#3a1c18'), emissiveIntensity: 0.2 });
  for (const sx of [1, -1]) {
    const up = new THREE.Group(), lo = new THREE.Group(); for (const g of [up, lo]) { g.position.set(sx * E[0] * H, E[1] * H, E[2] * H); headG.add(g); }
    const rim = (yOff, slope, rr, n_, a0, a1) => { const pts = []; for (let i = 0; i <= n_; i++) { const u = a0 + (a1 - a0) * i / n_, lx = u * 0.078, ly = yOff - slope * lx;
      const lz = Math.sqrt(Math.max(1e-6, rr * rr - lx * lx - ly * ly)); pts.push([sx * lx * H, ly * H, lz * H]); } return pts; };
    const lashPts = rim(0.025, 0.035, ER + 0.012, 10, -0.85, 0.92);
    const lash = new THREE.Mesh(strandGeo(lashPts, (s) => { const t = Math.sin(Math.PI * Math.min(1, 0.08 + s)); return [0.005 * H * t + 0.0015 * H, 0.0028 * H]; }, 6, 16), lashMat);
    lash.userData.part = 'lash'; lash.castShadow = false; up.add(lash); parts.push(lash);
    const wl = new THREE.Mesh(strandGeo(rim(-0.036, 0.0, ER + 0.004, 8, -0.8, 0.85), (s) => [0.0028 * H * Math.sin(Math.PI * Math.min(1, 0.1 + s)) + 0.0005 * H, 0.0016 * H], 5, 12), waterMat);
    wl.userData.part = 'waterline'; wl.castShadow = false; lo.add(wl); parts.push(wl);
    lidPivots.push({ up, lo });
  }
  // Lông mày: khối sợi dày mềm (bạc xám) bám gờ mày, đi theo rig.
  const browMat = matFn('hair', '#8e8680', 'brow', {});
  const onFace = (x, y) => { let z = 0.9; for (let it = 0; it < 80; it++) { const v = aiHeadSDF(x, y, z); if (Math.abs(v) < 1e-5) break; z -= v * 0.7; } return z; };
  const browBase = [[0.04, 0.662], [0.10, 0.683], [0.165, 0.682], [0.215, 0.66], [0.245, 0.632]].map(([x, y]) => [x, y, onFace(x, y) + 0.004]);
  // mỗi mày = 7 lọn sợi ngắn chồng lệch (đọc là lông, không phải vệt vẽ): [t0, t1, lệch y, dày]
  const BROW_TUFTS = [[0, 0.3, -0.005, 0.006], [0.02, 0.36, 0.004, 0.0055], [0.12, 0.5, -0.001, 0.006], [0.22, 0.6, 0.006, 0.005], [0.3, 0.72, -0.004, 0.0055], [0.42, 0.82, 0.003, 0.005], [0.55, 0.95, -0.002, 0.0045], [0.66, 1.0, 0.004, 0.004], [0.78, 1.0, -0.003, 0.0035]];
  const along = (pts, t) => { const u = t * (pts.length - 1), i = Math.min(pts.length - 2, Math.floor(u)), f = u - i; return pts[i].map((v, k) => v + (pts[i + 1][k] - v) * f); };
  const brows = []; for (const sx of [1, -1]) for (const tf of BROW_TUFTS) { const m = new THREE.Mesh(new THREE.BufferGeometry(), browMat); m.userData.part = 'brow'; m.castShadow = false; headG.add(m); parts.push(m); brows.push({ m, sx, tf }); }

  let cur = {};
  function setFace(w = {}) {
    cur = { ...w };
    const arr = pa.array; arr.set(P0);
    for (const [chn, v] of Object.entries(w)) { if (!v || !deltas[chn]) continue; const { idx, dv } = deltas[chn]; for (let j = 0; j < idx.length; j++) { const i = idx[j] * 3; arr[i] += v * dv[j * 3]; arr[i + 1] += v * dv[j * 3 + 1]; arr[i + 2] += v * dv[j * 3 + 2]; } }
    pa.needsUpdate = true; geo.computeVertexNormals();
    const na = nA.array; for (let i = 0; i < n; i++) { const x = N0[i * 3] + na[i * 3] - Nm0[i * 3], y = N0[i * 3 + 1] + na[i * 3 + 1] - Nm0[i * 3 + 1], z = N0[i * 3 + 2] + na[i * 3 + 2] - Nm0[i * 3 + 2], l = Math.hypot(x, y, z) || 1; na[i * 3] = x / l; na[i * 3 + 1] = y / l; na[i * 3 + 2] = z / l; }
    nA.needsUpdate = true; geo.computeBoundingSphere();
    const thUp = 0.78 * (w.blink || 0) + 0.30 * (w.lidDrop || 0) + 0.12 * (w.squint || 0), thLo = -0.08 * (w.blink || 0) - 0.32 * (w.squint || 0) - 0.15 * (w.cheekRaise || 0);
    for (const { up, lo } of lidPivots) { up.rotation.x = thUp; lo.rotation.x = thLo; }
    const bp = browBase.map(([x, y, z]) => { const d = faceDisp(w, x, y, z); return [x + d[0], y + d[1], z + d[2]]; });   // nửa trái; nửa phải đối xứng (rig đối xứng)
    for (const { m, sx, tf } of brows) {
      const pts = [0, 0.33, 0.67, 1].map((u) => { const t = tf[0] + (tf[1] - tf[0]) * u, q = along(bp, t); return [sx * q[0] * H, (q[1] + tf[2] * (1 - 0.6 * u) + 0.004 * u * (t < 0.25 ? 1 : 0)) * H, (q[2] + 0.002) * H]; });
      const g = strandGeo(pts, (s) => { const t = Math.sin(Math.PI * Math.min(1, 0.1 + s * 0.9)); return [(tf[3] * t + 0.0015) * H, 0.0035 * H]; }, 6, 10);
      m.geometry.dispose(); m.geometry = g; }
    jaw.rotation.x = 0.24 * Math.min(1, w.jawOpen || 0);
  }
  setFace(FACE_PRESETS[opts.expr] || {});
  return { head, eyes, setFace, getFace: () => cur, headSDF: aiHeadSDF, E, ER, skinMat: mat };
}

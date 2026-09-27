// Cine Lab · Cổng 3 v2 · Cách (2) — thiết kế tranh của Ida và Cas (khối phác, vùng màu, nét vẽ, tranh dải).
// Đơn vị: H (chiều cao đầu của từng nhân vật, lấy từ model sheet). Hệ cục bộ theo khớp của shared/cast.js:
//   đầu: gốc tại khớp 'head' (đỉnh cổ), y lên, mặt nhìn +z, +x = bên TRÁI nhân vật.   thân: gốc tại khớp 'spine' (tâm hông).
// Chi tiết thứ cấp (đã được chủ dự án cho phép thêm để sửa lỗi đọc giới tính/tuổi — xem README):
//   Ida: búi tóc to thấp dưới vành mũ, tóc xám chải ngược lộ ở thái dương, khăn choàng len đan thắt nút trước ngực,
//        váy dài lộ dưới gấu áo, hoa tai nhỏ, mặt có nếp nhăn (trán, đuôi mắt, rãnh mũi–má, khoé miệng), mí sụp.
//   Cas: tóc ngắn lộ ở gáy và thái dương, tai vểnh to, má tròn, tàn nhang, mũ len có gờ gấp và quả bông len xù đặt cao,
//        áo len quá khổ (miếng vá mạng ngực, bo cổ/bo gấu/bo tay), quần hụt lộ cổ chân.
import { vn2, vn3, fbm3, clamp, mix, smooth, hex, lerp3, strokePath, blob, softBlob } from './paint2d.js';

const rgba = (c, a = 1) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
const WHITE = [255, 255, 255], BLACK = [0, 0, 0];
const put = (out, c) => { out[0] = c[0]; out[1] = c[1]; out[2] = c[2]; };
// biến thiên "nét cọ" neo theo vị trí 3D: nhiễu kéo dài (vệt) + lệch nóng/lạnh
function brush(out, P, k = 1, amp = 0.10, hue = 6, st = [9, 26, 9]) {
  const n = vn3(P[0] * st[0], P[1] * st[1], P[2] * st[2]) - 0.5, m = vn3(P[0] * 4.1 + 7, P[1] * 4.1, P[2] * 4.1) - 0.5;
  const f = 1 + n * amp * 2 * k;
  out[0] = out[0] * f + m * hue * k; out[1] = out[1] * f; out[2] = out[2] * f - m * hue * k;
}

// =====================================================================================================
// IDA
// =====================================================================================================
const I = { SKIN: 1, HAIR: 2, HAT: 3, BUN: 4, EAR: 5, BRIM: 6, COAT: 11, COLLAR: 12, SHAWL: 13 };
const ida = {
  skin: [204, 166, 142], hair: [166, 160, 152], hat: hex('#2f2826'), coat: hex('#3f5552'), shawl: [132, 80, 66], dress: [92, 70, 82],
  stocking: [48, 44, 46], boots: hex('#2a2320'), lining: hex('#6b4a3a'),
};

function idaHeadPrims() {
  const P = [];
  const sk = (c, r, rot) => P.push({ c, r, rot, id: I.SKIN, g: 0 });
  sk([0, 0.57, -0.05], [0.375, 0.44, 0.45]);                // sọ
  sk([0, 0.44, 0.08], [0.27, 0.30, 0.33]);                  // mặt (hẹp, thon)
  sk([0, 0.26, 0.10], [0.22, 0.20, 0.30]);                  // hàm dưới thon về cằm nhỏ
  for (const x of [1, -1]) {
    sk([0.18 * x, 0.47, 0.23], [0.07, 0.045, 0.06]);        // gò má (nhẹ)
    sk([0.042 * x, 0.40, 0.445], [0.03, 0.028, 0.034]);     // cánh mũi
    P.push({ c: [0.385 * x, 0.50, -0.03], r: [0.042, 0.13, 0.08], rot: [0, -0.25 * x, 0], id: I.EAR, g: 0 });
  }
  sk([0, 0.63, 0.31], [0.25, 0.05, 0.08]);                  // cung mày (mềm)
  sk([0, 0.50, 0.43], [0.036, 0.12, 0.045], [-0.45, 0, 0]); // sống mũi dài, mảnh (bắt đầu từ hõm gốc mũi)
  sk([0, 0.395, 0.49], [0.04, 0.045, 0.05]);                // đầu mũi hơi trễ xuống (khoằm nhẹ)
  sk([0, 0.285, 0.385], [0.085, 0.03, 0.045]);              // môi trên
  sk([0, 0.228, 0.37], [0.07, 0.028, 0.045]);               // môi dưới
  // tóc xám chải ngược, lộ ở thái dương và gáy
  P.push({ c: [0, 0.60, -0.07], r: [0.395, 0.44, 0.45], clip: [[0, -0.55, 1, 0.02]], id: I.HAIR, g: 1 });
  P.push({ c: [0, 0.47, -0.30], r: [0.33, 0.24, 0.26], id: I.HAIR, g: 1 });              // tóc gom về búi
  for (const x of [1, -1]) P.push({ c: [0.33 * x, 0.61, 0.08], r: [0.10, 0.13, 0.19], rot: [0.3, 0, 0], id: I.HAIR, g: 1 }); // lượn tóc che thái dương, nửa trên tai (khung mặt nữ)
  P.push({ c: [0, 0.50, -0.52], r: [0.26, 0.215, 0.20], id: I.BUN, g: 3 });              // BÚI TO, thấp dưới vành
  // mũ phớt
  P.push({ c: [0, 0.86, 0.02], r: [0.68, 0.024, 0.74], rot: [0.10, 0, 0], id: I.BRIM, g: 2 });
  P.push({ c: [0, 0.78, 0.0], r: [0.445, 0.64, 0.495], rot: [0.08, 0, 0], clip: [[0, 1, 0, 1.30], [0, -1, 0, -0.84]], id: I.HAT, g: 2 });
  return P;
}

// Tóc: sợi chải từ chân tóc về búi (đường đồng quy tại búi) — búi là các vòng xoắn lọn to.
const BUN = [0, 0.50, -0.52];
function idaHair(id, P) {
  const dx = P[0] - BUN[0], dy = P[1] - BUN[1], dz = P[2] - BUN[2];
  let lock, fine;
  if (id === I.BUN) { const a = Math.atan2(dy, dx), r = Math.hypot(dx, dy); lock = 0.5 + 0.5 * Math.sin(r * 58 + a * 1.2 + vn2(a * 2, r * 8) * 2.5); fine = 0.5 + 0.5 * Math.sin(r * 320 + vn2(a * 9, r * 30) * 5); }
  else { const phi = Math.atan2(dx, dy), d = Math.hypot(dx, dy, dz); lock = vn2(phi * 7 + d * 3, d * 2.5) * 0.7 + vn2(phi * 20, d * 5) * 0.3; fine = 0.5 + 0.5 * Math.sin(phi * 110 + vn2(phi * 12, d * 6) * 9); }
  const t = clamp(0.2 + 0.65 * lock + 0.16 * (fine - 0.5));
  return t < 0.5 ? lerp3([104, 100, 98], [158, 153, 147], t * 2) : lerp3([158, 153, 147], [212, 208, 200], (t - 0.5) * 2);
}
function idaHeadColor(id, P, out) {
  const y = P[1], x = P[0], z = P[2], ax = Math.abs(x);
  if (id === I.SKIN || id === I.EAR) {
    let c = ida.skin.slice();
    c = lerp3(c, [212, 182, 150], smooth(0.56, 0.74, y) * 0.8);                                  // trán: vàng nhạt
    const red = Math.exp(-((y - 0.44) ** 2) / 0.010) * smooth(0.08, 0.26, ax) + Math.exp(-((x / 0.05) ** 2)) * smooth(0.40, 0.47, z) * Math.exp(-(((y - 0.46) / 0.09) ** 2)) * 0.8 + (id === I.EAR ? 0.7 : 0);
    c = lerp3(c, [212, 138, 124], clamp(red) * 0.55);                                            // má–mũi–tai: đỏ
    c = lerp3(c, [182, 160, 152], smooth(0.34, 0.12, y) * 0.75);                                 // hàm: lạnh, xám
    c = lerp3(c, [176, 138, 146], Math.exp(-((y - 0.50) ** 2) / 0.0012) * smooth(0.08, 0.13, ax) * (1 - smooth(0.22, 0.28, ax)) * 0.5); // quầng dưới mắt
    const spot = vn3(P[0] * 46 + 3, P[1] * 46, P[2] * 46);                                       // đồi mồi nhỏ, nhạt
    if (spot > 0.80 && (y > 0.55 || ax > 0.22)) c = lerp3(c, [182, 140, 116], clamp((spot - 0.80) * 8) * 0.35);
    put(out, c); brush(out, P, 1, 0.07, 7, [10, 30, 10]);
  } else if (id === I.HAIR || id === I.BUN) {
    put(out, idaHair(id, P)); brush(out, P, 0.4, 0.04, 3);
  } else {
    let c = ida.hat.slice();
    const band = id === I.HAT && y > 0.855 && y < 0.95;
    if (band) c = [30, 24, 23];
    if (id === I.HAT) c = lerp3(c, [16, 13, 13], Math.exp(-((x / 0.06) ** 2)) * smooth(1.12, 1.29, y) * 0.55);   // nếp gấp đỉnh mũ (mềm)
    put(out, c); brush(out, P, 1, 0.10, 3, [8, 8, 8]);
    if (id === I.BRIM) { const r = Math.hypot(x / 0.68, z / 0.74); out[0] += smooth(0.9, 1.0, r) * 10; out[1] += smooth(0.9, 1.0, r) * 8; out[2] += smooth(0.9, 1.0, r) * 7; } // mép vành sờn
  }
}

// Nét vẽ mặt Ida (đơn vị H, hệ (s, t) tiếp tuyến tại điểm neo: s theo +x nhân vật, t lên).
function idaFeatures(api, A) {
  const skinIds = new Set([I.SKIN, I.EAR]);
  for (const x of [1, -1]) {
    const E = A['eye' + x], o = x; // o = hướng đuôi mắt (ra ngoài) theo s
    api.feature(E, [1, 0, 0], (g, mode) => {
      if (mode === 'color') {
        softBlob(g, 0.005 * o, 0.012, 0.10, [132, 84, 84], 0.42, 0.8);                       // hốc mắt sâu
        strokePath(g, [[-0.075 * o, 0.030], [-0.01 * o, 0.052], [0.06 * o, 0.040], [0.105 * o, 0.006]], 0.014, 0.010, rgba([128, 84, 76], 0.9)); // mí trên sụp
        // khe mắt hình hạnh, đuôi cụp
        g.save(); g.beginPath(); g.moveTo(-0.062 * o, 0.004); g.quadraticCurveTo(0.0, 0.030, 0.066 * o, -0.004); g.quadraticCurveTo(0.0, -0.016, -0.062 * o, 0.004); g.closePath();
        g.fillStyle = rgba([176, 156, 148]); g.fill(); g.clip();
        blob(g, 0.004 * o, 0.004, 0.024, 0.024, 0, rgba([74, 58, 50])); blob(g, 0.004 * o, 0.004, 0.011, 0.011, 0, rgba([22, 16, 16]));
        g.restore();
        strokePath(g, [[-0.064 * o, 0.006], [0.0, 0.028], [0.068 * o, -0.004]], 0.016, 0.010, rgba([26, 16, 16], 1.0));   // bờ mi trên
        for (const k of [0.3, 0.55, 0.8]) strokePath(g, [[(-0.064 + 0.132 * k) * o, 0.028 * Math.sin(Math.PI * k) - 0.01 * k + 0.004], [(-0.056 + 0.15 * k) * o, 0.036 * Math.sin(Math.PI * k) - 0.004 * k + 0.012]], 0.004, 0.002, rgba([40, 26, 26], 0.8)); // vài sợi mi
        strokePath(g, [[-0.05 * o, -0.012], [0.01 * o, -0.020], [0.065 * o, -0.010]], 0.004, 0.003, rgba([120, 78, 74], 0.7)); // bờ mi dưới
        strokePath(g, [[-0.055 * o, -0.042], [0.01 * o, -0.056], [0.075 * o, -0.040]], 0.006, 0.004, rgba([150, 104, 98], 0.75)); // bọng mắt
        for (const [a, b] of [[0.13, 0.035], [0.14, -0.002], [0.125, -0.042]]) strokePath(g, [[0.085 * o, 0.0], [a * o, b]], 0.005, 0.002, rgba([150, 102, 92], 0.8)); // vết chân chim
      } else {
        softBlob(g, 0.005 * o, 0.012, 0.09, BLACK, 0.8, 0.8);
        strokePath(g, [[-0.075 * o, 0.030], [-0.01 * o, 0.052], [0.06 * o, 0.040], [0.105 * o, 0.006]], 0.02, 0.014, rgba(WHITE, 0.9));
        strokePath(g, [[-0.055 * o, -0.042], [0.01 * o, -0.056], [0.075 * o, -0.040]], 0.02, 0.012, rgba(WHITE, 0.6));
        for (const [a, b] of [[0.13, 0.035], [0.14, -0.002], [0.125, -0.042]]) strokePath(g, [[0.085 * o, 0.0], [a * o, b]], 0.006, 0.003, rgba(BLACK, 0.8));
      }
    }, [-0.13, -0.12, 0.13, 0.12], { ids: skinIds, reliefAmp: 0.012, tol: 0.06 });
    // lông mày thưa, đuôi cụp (hiền, buồn)
    api.feature(A['brow' + x], [1, 0, 0], (g, mode) => {
      if (mode !== 'color') return;
      for (let k = 0; k < 11; k++) { const t = k / 10; strokePath(g, [[(-0.07 + 0.15 * t) * o, 0.004 + 0.02 * Math.sin(Math.PI * t) - 0.02 * t], [(-0.05 + 0.15 * t) * o, 0.012 + 0.02 * Math.sin(Math.PI * t) - 0.03 * t]], 0.009, 0.004, rgba([96, 86, 82], 0.85)); }
    }, [-0.12, -0.06, 0.12, 0.06], { ids: skinIds });
    // rãnh mũi–má sâu
    api.feature(A['naso' + x], [1, 0, 0], (g, mode) => {
      const pts = [[-0.035 * o, 0.075], [-0.005 * o, 0.02], [0.012 * o, -0.04], [0.018 * o, -0.10]];
      if (mode === 'color') { strokePath(g, pts, 0.010, 0.005, rgba([160, 108, 98], 0.5)); }
      else { strokePath(g, pts, 0.014, 0.008, rgba(BLACK, 0.9)); strokePath(g, pts.map(([a, b]) => [a + 0.022 * o, b]), 0.03, 0.016, rgba(WHITE, 0.5)); }
    }, [-0.08, -0.14, 0.08, 0.12], { ids: skinIds, reliefAmp: 0.014, tol: 0.08 });
    // rãnh khoé miệng → cằm
    api.feature(A['mar' + x], [1, 0, 0], (g, mode) => {
      const pts = [[0.0, 0.02], [0.006 * o, -0.03], [0.004 * o, -0.07]];
      strokePath(g, pts, 0.007, 0.003, mode === 'color' ? rgba([166, 120, 110], 0.4) : rgba(BLACK, 0.5));
    }, [-0.05, -0.1, 0.05, 0.05], { ids: skinIds, reliefAmp: 0.01 });
    // tai: vành trong + hoa tai nhỏ
    api.feature(A['ear' + x], null, (g, mode) => {
      const pts = [[0.03, 0.09], [-0.01, 0.10], [-0.04, 0.05], [-0.03, -0.03], [0.0, -0.06]].map(([a, b]) => [-a * x, b]); // (ra sau, lên) → s
      if (mode === 'color') {
        strokePath(g, pts, 0.012, 0.008, rgba([150, 92, 86], 0.8));
        blob(g, 0.005, -0.11, 0.014, 0.014, 0, rgba([214, 206, 192])); blob(g, 0.009, -0.106, 0.005, 0.005, 0, rgba([250, 246, 236])); // hoa tai ngọc trai nhỏ
      } else strokePath(g, pts, 0.014, 0.01, rgba(BLACK, 0.8));
    }, [-0.08, -0.14, 0.08, 0.14], { ids: skinIds, reliefAmp: 0.01, minFace: 0.2, tol: 0.08 });
    // vài sợi tóc lộ ở thái dương
    api.feature(A['temple' + x], null, (g, mode) => {
      if (mode !== 'color') return;
      const f = -x; // (ra trước, lên) → s
      for (let k = 0; k < 7; k++) strokePath(g, [[(0.06 - k * 0.012) * f, -0.05 + k * 0.004], [(-0.02 - k * 0.01) * f, 0.02 + k * 0.01], [(-0.08 - k * 0.01) * f, 0.05 + k * 0.012]], 0.007, 0.003, rgba(k % 2 ? [214, 208, 200] : [150, 144, 138], 0.8));
    }, [-0.16, -0.08, 0.1, 0.16], { ids: new Set([I.HAIR, I.SKIN]), tol: 0.1 });
  }
  // nơ vải nhỏ trên băng mũ (chi tiết thứ cấp: mũ của phụ nữ)
  api.feature(A.bow, null, (g, mode) => {
    const c = mode === 'color' ? [92, 58, 62] : WHITE;
    for (const sx of [1, -1]) { g.beginPath(); g.moveTo(0, 0); g.quadraticCurveTo(0.06 * sx, 0.06, 0.10 * sx, 0.02); g.quadraticCurveTo(0.11 * sx, -0.03, 0.0, 0.0); g.fillStyle = rgba(c, 0.95); g.fill(); }
    blob(g, 0, 0, 0.022, 0.03, 0, rgba(mode === 'color' ? [70, 42, 46] : WHITE, 1));
    if (mode === 'color') for (const sx of [1, -1]) strokePath(g, [[0.004 * sx, -0.01], [0.03 * sx, -0.06], [0.05 * sx, -0.09]], 0.018, 0.012, rgba([86, 54, 58], 0.9), false);
  }, [-0.14, -0.12, 0.14, 0.1], { ids: new Set([I.HAT]), reliefAmp: 0.012, tol: 0.12, minFace: 0.15 });
  // lỗ mũi
  api.feature(A.nostril, [1, 0, 0], (g, mode) => {
    if (mode !== 'color') return;
    for (const x of [1, -1]) blob(g, 0.036 * x, 0.0, 0.016, 0.008, 0.3 * x, rgba([96, 52, 48], 0.9));
  }, [-0.07, -0.03, 0.07, 0.03], { ids: skinIds, minFace: 0.05 });
  // miệng: môi mỏng hồng phai, khoé hơi trễ; nếp dọc môi trên
  api.feature(A.mouth, [1, 0, 0], (g, mode) => {
    if (mode === 'color') {
      g.beginPath(); g.moveTo(-0.078, -0.004); g.quadraticCurveTo(-0.03, 0.030, 0.0, 0.020); g.quadraticCurveTo(0.03, 0.030, 0.078, -0.006); g.quadraticCurveTo(0, 0.004, -0.078, -0.004); g.fillStyle = rgba([168, 96, 98], 0.9); g.fill();
      g.beginPath(); g.moveTo(-0.06, -0.006); g.quadraticCurveTo(0.0, -0.045, 0.06, -0.008); g.quadraticCurveTo(0, -0.006, -0.06, -0.006); g.fillStyle = rgba([180, 108, 108], 0.85); g.fill();
      strokePath(g, [[-0.08, -0.006], [-0.03, 0.001], [0.03, 0.0], [0.08, -0.012]], 0.008, 0.006, rgba([96, 50, 50], 0.95));
      for (const x of [-0.04, -0.015, 0.02, 0.045]) strokePath(g, [[x, 0.024], [x * 1.05, 0.05]], 0.003, 0.002, rgba([160, 112, 104], 0.6));
      strokePath(g, [[-0.03, -0.075], [0.0, -0.068], [0.03, -0.075]], 0.006, 0.004, rgba([168, 122, 112], 0.6)); // nếp cằm
    } else { strokePath(g, [[-0.08, -0.006], [-0.03, 0.001], [0.03, 0.0], [0.08, -0.012]], 0.012, 0.01, rgba(BLACK, 0.9)); }
  }, [-0.12, -0.1, 0.12, 0.08], { ids: skinIds, reliefAmp: 0.008, tol: 0.07 });
  // trán: ba nếp ngang
  api.feature(A.forehead, [1, 0, 0], (g, mode) => {
    for (let k = 0; k < 3; k++) { const t = k * 0.034, w = 0.17 - k * 0.02;
      strokePath(g, [[-w, t - 0.01], [-w * 0.4, t + 0.006], [w * 0.2, t - 0.002], [w, t + 0.004]], 0.006, 0.004, mode === 'color' ? rgba([176, 132, 116], 0.6) : rgba(BLACK, 0.7)); }
  }, [-0.2, -0.04, 0.2, 0.1], { ids: skinIds, reliefAmp: 0.006, tol: 0.09 });
}

function idaHeadDesign() {
  return {
    groups: [{ k: 22 }, { k: 16 }, { k: 0 }, { k: 0 }], prims: idaHeadPrims(), color: idaHeadColor,
    anchors: {
      eye1: [[0.15, 0.53, 0.40], [0.25, 0.05, 1]], 'eye-1': [[-0.15, 0.53, 0.40], [-0.25, 0.05, 1]],
      brow1: [[0.16, 0.625, 0.39], [0.2, 0.3, 1]], 'brow-1': [[-0.16, 0.625, 0.39], [-0.2, 0.3, 1]],
      naso1: [[0.10, 0.36, 0.40], [0.35, 0, 1]], 'naso-1': [[-0.10, 0.36, 0.40], [-0.35, 0, 1]],
      mar1: [[0.08, 0.235, 0.39], [0.3, -0.2, 1]], 'mar-1': [[-0.08, 0.235, 0.39], [-0.3, -0.2, 1]],
      ear1: [[0.43, 0.50, -0.03], [1, 0, 0.25]], 'ear-1': [[-0.43, 0.50, -0.03], [-1, 0, 0.25]],
      temple1: [[0.33, 0.62, 0.16], [0.8, 0.1, 0.6]], 'temple-1': [[-0.33, 0.62, 0.16], [-0.8, 0.1, 0.6]],
      nostril: [[0, 0.372, 0.475], [0, -0.6, 1]], mouth: [[0, 0.255, 0.42], [0, 0, 1]], forehead: [[0, 0.73, 0.35], [0, 0.35, 1]],
      bow: [[0.40, 0.90, 0.22], [0.85, 0, 0.5]],
    },
    features: idaFeatures,
    cavity: { r: 0.045, gain: 10, amt: 0.45, tint: (id) => (id === I.HAT || id === I.BRIM ? [20, 16, 16] : id === I.HAIR || id === I.BUN ? [70, 64, 62] : [118, 64, 64]) },
    reliefFn: (id, P) => (id === I.HAIR || id === I.BUN ? (idaHair(id, P)[0] / 212 - 0.6) * (id === I.BUN ? 0.02 : 0.008) : id === I.HAT ? -0.02 * Math.exp(-((P[0] / 0.06) ** 2)) * smooth(1.12, 1.29, P[1]) : 0),
    soft: 0.008, edge: 0.4, frame: { c: [0, 0.62, -0.05], size: 2.3 },
  };
}

function idaTorsoDesign() {
  const P = [];
  const co = (c, r, rot) => P.push({ c, r, rot, id: I.COAT, g: 0 });
  co([0, 1.45, 0.0], [0.60, 0.55, 0.38]); co([0, 0.9, 0], [0.53, 0.55, 0.34]); co([0, 0.42, 0], [0.64, 0.46, 0.43]); co([0, 1.6, -0.1], [0.5, 0.4, 0.33]);
  for (const x of [1, -1]) { co([0.2 * x, 1.33, 0.19], [0.19, 0.16, 0.16]); co([0.52 * x, 1.77, -0.02], [0.2, 0.15, 0.2]); }
  P.push({ c: [0, 2.10, 0.02], r: [0.25, 0.36, 0.23], clip: [[0, 1, 0, 2.40], [0, -1, 0, -1.86]], id: I.COLLAR, g: 1 });   // cổ đứng 0,35 H (model sheet)
  const sh = (c, r, rot, clip) => P.push({ c, r, rot, clip, id: I.SHAWL, g: 2 });
  sh([0, 1.66, -0.04], [0.76, 0.40, 0.50], null, [[0, -1, 0.35, -1.40]]);   // vòng qua vai: thấp dần ra sau
  sh([0, 1.30, -0.30], [0.42, 0.38, 0.14]);                                  // góc khăn buông sau lưng
  sh([0, 2.16, 0.03], [0.30, 0.17, 0.28]);                                   // vòng khăn quấn quanh cổ
  for (const x of [1, -1]) sh([0.15 * x, 1.42, 0.38], [0.10, 0.24, 0.08], [0, 0, 0.55 * x]); // hai mép khăn chéo xuống nút
  sh([0, 1.24, 0.43], [0.10, 0.085, 0.08]); sh([0.05, 1.05, 0.41], [0.07, 0.18, 0.05], [0, 0, 0.12]); sh([-0.07, 1.03, 0.40], [0.065, 0.19, 0.05], [0, 0, -0.1]);
  return {
    groups: [{ k: 12 }, { k: 0 }, { k: 16 }], prims: P,
    color(id, Q, out) {
      const [x, y, z] = Q;
      if (id === I.SHAWL) { // len đan: gân chéo theo vạt + sọc nhạt ở mép
        const rib = 0.5 + 0.5 * Math.sin((x * 0.5 + y) * 90 + vn3(x * 6, y * 6, z * 6) * 3), blot = vn3(x * 5, y * 5, z * 5);
        let c = lerp3([104, 68, 62], [140, 98, 86], 0.35 + 0.3 * blot + 0.2 * rib);
        put(out, c); brush(out, Q, 0.8, 0.06, 5);
        if (y < 1.0 && Math.abs(z - 0.4) < 0.1) { out[0] *= 0.9; out[1] *= 0.9; out[2] *= 0.9; }
        return;
      }
      let c = ida.coat.slice();
      const fold = vn3(x * 12, y * 2.2, z * 12);                         // nếp vải dọc
      c = lerp3(c, [44, 62, 60], smooth(0.55, 0.8, fold) * 0.6); c = lerp3(c, [84, 108, 102], smooth(0.4, 0.15, fold) * 0.35);
      if (id === I.COLLAR) c = lerp3(c, [40, 56, 54], 0.4);
      if (id === I.COAT && y > 0.5 && y < 0.6) c = [44, 36, 33];         // thắt lưng da
      put(out, c); brush(out, Q, 1, 0.08, 4, [10, 20, 10]);
    },
    anchors: { buckle: [[0, 0.55, 0.40], [0, 0, 1]], btn1: [[0.06, 0.80, 0.34], [0.1, 0, 1]], fringe: [[0, 0.88, 0.42], [0, 0, 1]], btn2: [[0.06, 0.30, 0.43], [0.1, 0, 1]], lap1: [[0.25, 1.8, 0.2], [0.4, 0.6, 1]] },
    features(api, A) {
      api.feature(A.buckle, [1, 0, 0], (g, mode) => { if (mode !== 'color') return; g.strokeStyle = rgba([120, 104, 80]); g.lineWidth = 0.014; g.strokeRect(-0.045, -0.04, 0.09, 0.08); }, [-0.07, -0.07, 0.07, 0.07], { tol: 0.1 });
      api.feature(A.fringe, [1, 0, 0], (g, mode) => { if (mode !== 'color') return; for (let k = 0; k < 12; k++) { const x = -0.1 + k * 0.018; strokePath(g, [[x, 0.04], [x + 0.004 * Math.sin(k * 3), -0.03]], 0.008, 0.004, rgba(k % 2 ? [118, 80, 70] : [90, 58, 52], 0.9)); } }, [-0.14, -0.06, 0.14, 0.06], { tol: 0.12 }); // tua khăn
      for (const b of [A.btn1, A.btn2]) api.feature(b, [1, 0, 0], (g, mode) => { blob(g, 0, 0, 0.028, 0.028, 0, mode === 'color' ? rgba([34, 30, 28]) : rgba(WHITE, 0.9)); if (mode === 'color') blob(g, -0.006, 0.006, 0.01, 0.01, 0, rgba([80, 74, 66], 0.8)); }, [-0.05, -0.05, 0.05, 0.05], { tol: 0.1, reliefAmp: 0.01, ids: new Set([I.COAT]) });
    },
    cavity: { r: 0.06, gain: 7, amt: 0.4, tint: (id) => (id === I.SHAWL ? [60, 30, 28] : [22, 30, 32]) },
    reliefFn: (id, Q) => (id === I.SHAWL ? Math.sin((Q[0] * 0.5 + Q[1]) * 90 + vn3(Q[0] * 6, Q[1] * 6, Q[2] * 6) * 3) * 0.003 + (vn3(Q[0] * 5, Q[1] * 5, Q[2] * 5) - 0.5) * 0.04 : (vn3(Q[0] * 12, Q[1] * 2.2, Q[2] * 12) - 0.5) * 0.03),
    soft: 0.02, edge: 0.5, frame: { c: [0, 1.3, 0], size: 2.5 },
  };
}

// =====================================================================================================
// CAS
// =====================================================================================================
const C = { SKIN: 1, HAIR: 2, CAP: 3, CUFF: 4, BOB: 5, EAR: 6, SW: 11, RIB: 12 };
const cas = { skin: hex('#e2bfa2'), hair: [92, 64, 50], cap: hex('#d6c9ae'), bob: hex('#a8483a'), sweater: hex('#8a4a3c'), trousers: hex('#3a3d48'), boots: hex('#2c2522') };

function casHeadDesign() {
  const P = [];
  const sk = (c, r, rot) => P.push({ c, r, rot, id: C.SKIN, g: 0 });
  sk([0, 0.57, -0.03], [0.45, 0.45, 0.49]); sk([0, 0.38, 0.10], [0.34, 0.34, 0.36]); sk([0, 0.14, 0.20], [0.15, 0.10, 0.13]);
  sk([0, 0.42, 0.47], [0.062, 0.056, 0.062]); sk([0, 0.60, 0.34], [0.25, 0.05, 0.07]); sk([0, 0.255, 0.43], [0.07, 0.03, 0.04]);
  for (const x of [1, -1]) {
    sk([0.20 * x, 0.34, 0.22], [0.165, 0.145, 0.165]);                                                       // má tròn trẻ con
    P.push({ c: [0.475 * x, 0.46, -0.06], r: [0.05, 0.155, 0.115], rot: [0, -0.62 * x, 0], id: C.EAR, g: 0 }); // TAI VỂNH TO
    P.push({ c: [0.41 * x, 0.56, 0.13], r: [0.07, 0.10, 0.08], id: C.HAIR, g: 1 });                         // tóc mai
  }
  P.push({ c: [0, 0.55, -0.08], r: [0.47, 0.40, 0.475], clip: [[0, -0.3, 1, -0.02]], id: C.HAIR, g: 1 });   // tóc ngắn: gáy
  P.push({ c: [0, 0.64, -0.02], r: [0.49, 0.46, 0.53], clip: [[0, -1, 0, -0.62]], id: C.CAP, g: 2 });       // chỏm mũ len
  P.push({ c: [0, 0.68, -0.02], r: [0.515, 0.10, 0.555], id: C.CUFF, g: 2 });                               // gờ gấp
  P.push({ c: [0, 1.20, -0.04], r: [0.205, 0.195, 0.205], id: C.BOB, g: 3 });                              // quả bông cao, tách khỏi chỏm
  return {
    groups: [{ k: 20 }, { k: 18 }, { k: 10 }, { k: 0 }], prims: P,
    color(id, Q, out) {
      const [x, y, z] = Q, ax = Math.abs(x);
      if (id === C.SKIN || id === C.EAR) {
        let c = cas.skin.slice();
        c = lerp3(c, [230, 200, 170], smooth(0.52, 0.66, y) * 0.6);
        const red = Math.exp(-((y - 0.34) ** 2) / 0.012) * smooth(0.08, 0.24, ax) + (id === C.EAR ? 1 : 0) + (ax < 0.07 && z > 0.44 ? 0.7 : 0);
        c = lerp3(c, [228, 150, 132], clamp(red) * 0.55);                               // má, mũi, tai ửng đỏ vì lạnh
        c = lerp3(c, [206, 178, 164], smooth(0.24, 0.10, y) * 0.5);
        const fr = vn3(x * 60, y * 60, z * 60);                                         // tàn nhang
        if (fr > 0.72 && y > 0.3 && y < 0.52 && z > 0.25) c = lerp3(c, [176, 112, 84], clamp((fr - 0.72) * 5) * 0.8);
        put(out, c); brush(out, Q, 1, 0.06, 6, [10, 28, 10]);
      } else if (id === C.HAIR) {
        const t = vn3(x * 50, y * 14, z * 50);
        put(out, lerp3([66, 44, 34], [128, 92, 70], smooth(0.3, 0.8, t))); brush(out, Q, 0.5, 0.05, 3);
      } else if (id === C.CAP || id === C.CUFF) {
        // len đan: gân dọc (cột mũi) + hàng ngang; gờ gấp là gân to
        const a = Math.atan2(x, z);
        const col = 0.5 + 0.5 * Math.sin(a * (id === C.CUFF ? 44 : 30)), row = 0.5 + 0.5 * Math.sin(y * 180);
        let c = lerp3([176, 162, 134], [228, 218, 196], col * 0.7 + row * 0.15);
        if (id === C.CAP && y > 0.9) c = lerp3(c, [160, 146, 120], smooth(0.9, 1.08, y) * 0.3);
        put(out, c); brush(out, Q, 0.6, 0.05, 4);
      } else { // quả bông: sợi len rối
        const t = vn3(x * 70, y * 70, z * 70), u = vn3(x * 18 + 3, y * 18, z * 18);
        put(out, lerp3([120, 40, 32], [200, 96, 78], smooth(0.2, 0.9, t * 0.7 + u * 0.3)));
      }
    },
    anchors: {
      eye1: [[0.16, 0.50, 0.40], [0.3, 0.05, 1]], 'eye-1': [[-0.16, 0.50, 0.40], [-0.3, 0.05, 1]],
      brow1: [[0.16, 0.60, 0.40], [0.25, 0.3, 1]], 'brow-1': [[-0.16, 0.60, 0.40], [-0.25, 0.3, 1]],
      ear1: [[0.50, 0.46, -0.06], [1, 0, 0.6]], 'ear-1': [[-0.50, 0.46, -0.06], [-1, 0, 0.6]],
      mouth: [[0, 0.26, 0.45], [0, 0, 1]], nostril: [[0, 0.385, 0.49], [0, -0.6, 1]],
      nape: [[0, 0.30, -0.42], [0, -0.3, -1]], neckL: [[0.3, 0.33, -0.33], [0.7, -0.2, -0.7]], neckR: [[-0.3, 0.33, -0.33], [-0.7, -0.2, -0.7]],
    },
    features(api, A) {
      const skinIds = new Set([C.SKIN, C.EAR]);
      for (const o of [1, -1]) {
        api.feature(A['eye' + o], [1, 0, 0], (g, mode) => {
          if (mode === 'color') {
            softBlob(g, 0, 0.0, 0.085, [190, 140, 130], 0.25, 0.8);
            g.save(); g.beginPath(); g.moveTo(-0.058 * o, 0.0); g.quadraticCurveTo(0.0, 0.052, 0.062 * o, 0.004); g.quadraticCurveTo(0.0, -0.034, -0.058 * o, 0.0); g.closePath();
            g.fillStyle = rgba([226, 214, 204]); g.fill(); g.clip();
            blob(g, 0.004 * o, 0.006, 0.034, 0.034, 0, rgba([92, 72, 52])); blob(g, 0.004 * o, 0.006, 0.016, 0.016, 0, rgba([20, 14, 14]));
            blob(g, -0.008 * o, 0.018, 0.007, 0.007, 0, rgba([250, 250, 246], 0.9));
            g.restore();
            strokePath(g, [[-0.06 * o, 0.002], [0.0, 0.048], [0.066 * o, 0.006]], 0.011, 0.008, rgba([40, 26, 24], 0.95));
            strokePath(g, [[-0.05 * o, 0.064], [0.0, 0.080], [0.055 * o, 0.064]], 0.005, 0.004, rgba([196, 146, 132], 0.6));
          } else { softBlob(g, 0, 0.0, 0.07, BLACK, 0.5, 0.8); strokePath(g, [[-0.05 * o, 0.064], [0.0, 0.080], [0.055 * o, 0.064]], 0.012, 0.01, rgba(WHITE, 0.6)); }
        }, [-0.1, -0.08, 0.1, 0.1], { ids: skinIds, reliefAmp: 0.01, tol: 0.06 });
        api.feature(A['brow' + o], [1, 0, 0], (g, mode) => { if (mode !== 'color') return;
          strokePath(g, [[-0.07 * o, -0.004], [0.0, 0.016], [0.075 * o, 0.002]], 0.022, 0.012, rgba([96, 66, 50], 0.9)); }, [-0.1, -0.05, 0.1, 0.05], { ids: skinIds });
        api.feature(A['ear' + o], null, (g, mode) => {
          const pts = [[0.05, 0.1], [-0.01, 0.12], [-0.06, 0.06], [-0.05, -0.04], [0.0, -0.08]].map(([a, b]) => [-a * o, b]);
          strokePath(g, pts, 0.016, 0.01, mode === 'color' ? rgba([176, 104, 92], 0.85) : rgba(BLACK, 0.8));
        }, [-0.1, -0.14, 0.1, 0.16], { ids: skinIds, reliefAmp: 0.012, minFace: 0.15, tol: 0.1 });
      }
      api.feature(A.nostril, [1, 0, 0], (g, mode) => { if (mode !== 'color') return; for (const x of [1, -1]) blob(g, 0.028 * x, 0, 0.012, 0.007, 0.3 * x, rgba([150, 84, 74], 0.9)); }, [-0.05, -0.03, 0.05, 0.03], { ids: skinIds, minFace: 0.05 });
      api.feature(A.mouth, [1, 0, 0], (g, mode) => {
        if (mode === 'color') {
          g.beginPath(); g.moveTo(-0.05, 0.0); g.quadraticCurveTo(0.0, -0.04, 0.05, 0.0); g.quadraticCurveTo(0, -0.004, -0.05, 0); g.fillStyle = rgba([206, 128, 116], 0.7); g.fill();
          strokePath(g, [[-0.055, 0.004], [0.0, -0.002], [0.055, 0.004]], 0.008, 0.006, rgba([120, 60, 56], 0.95));
        } else strokePath(g, [[-0.055, 0.004], [0.0, -0.002], [0.055, 0.004]], 0.012, 0.01, rgba(BLACK, 0.8));
      }, [-0.08, -0.06, 0.08, 0.04], { ids: skinIds, reliefAmp: 0.008 });
      // gáy: chân tóc ngắn lởm chởm (đọc là tóc cắt ngắn của bé trai)
      for (const an of [A.nape, A.neckL, A.neckR]) api.feature(an, null, (g, mode) => {
        if (mode !== 'color') return;
        for (let k = 0; k < 26; k++) { const s = -0.2 + 0.4 * (k / 25), l = 0.03 + 0.03 * ((k * 7) % 5) / 5; strokePath(g, [[s, 0.06], [s + 0.01 * Math.sin(k), 0.06 - l]], 0.012, 0.004, rgba(k % 3 ? [70, 48, 38] : [120, 86, 64], 0.9)); }
      }, [-0.24, -0.04, 0.24, 0.1], { ids: new Set([C.HAIR, C.SKIN]), tol: 0.12 });
    },
    cavity: { r: 0.045, gain: 9, amt: 0.35, tint: (id) => (id === C.CAP || id === C.CUFF ? [110, 96, 80] : id === C.BOB ? [70, 20, 18] : id === C.HAIR ? [40, 28, 22] : [150, 80, 72]) },
    reliefFn: (id, Q) => {
      if (id === C.CAP || id === C.CUFF) { const a = Math.atan2(Q[0], Q[2]); return Math.sin(a * (id === C.CUFF ? 44 : 30)) * 0.006 + Math.sin(Q[1] * 180) * 0.002; }
      if (id === C.BOB) return (vn3(Q[0] * 70, Q[1] * 70, Q[2] * 70) - 0.5) * 0.03;
      if (id === C.HAIR) return (vn3(Q[0] * 50, Q[1] * 14, Q[2] * 50) - 0.5) * 0.01;
      return 0;
    },
    soft: 0.008, edge: 0.6, frame: { c: [0, 0.66, -0.03], size: 1.9 },
    fuzz: C.BOB,
  };
}

function casTorsoDesign() {
  const P = [];
  const sw = (c, r, clip) => P.push({ c, r, clip, id: C.SW, g: 0 });
  sw([0, 1.0, 0], [0.62, 0.52, 0.37]); sw([0, 0.40, 0.02], [0.63, 0.55, 0.39], [[0, -1, 0, 0.10]]);
  for (const x of [1, -1]) sw([0.50 * x, 1.2, -0.02], [0.2, 0.16, 0.19]);
  P.push({ c: [0, 1.47, 0.0], r: [0.23, 0.09, 0.2], id: C.RIB, g: 1 });
  const knit = (Q) => { const row = Math.sin(Q[1] * 95), col = Math.abs(Math.sin(Math.atan2(Q[0], Q[2]) * 26 + (row > 0 ? 0.6 : -0.6))); return 0.5 * col + 0.25 * (row * 0.5 + 0.5); };
  return {
    groups: [{ k: 10 }, { k: 0 }], prims: P,
    color(id, Q, out) {
      const [x, y, z] = Q;
      let c;
      if (id === C.RIB || y < 0.06) { const rib = 0.5 + 0.5 * Math.sin(Math.atan2(x, z) * 60); c = lerp3([112, 56, 44], [150, 82, 66], rib); }
      else c = lerp3([118, 60, 48], [158, 88, 70], knit(Q));
      c = lerp3(c, [100, 52, 44], smooth(0.55, 0.85, vn3(x * 5, y * 3, z * 5)) * 0.5);        // áo rộng: võng nếp
      put(out, c); brush(out, Q, 0.8, 0.06, 5);
    },
    anchors: { patch: [[0.22, 0.95, 0.33], [0.3, 0, 1]] },
    features(api, A) { // miếng vá mạng (len khác màu) — dấu vết nhà nghèo, đọc được ở trung cảnh
      api.feature(A.patch, [1, 0, 0], (g, mode) => {
        if (mode === 'color') { g.fillStyle = rgba([112, 104, 90], 0.95); g.beginPath(); g.moveTo(-0.08, -0.07); g.lineTo(0.09, -0.08); g.lineTo(0.08, 0.08); g.lineTo(-0.07, 0.07); g.closePath(); g.fill();
          g.strokeStyle = rgba([70, 60, 50], 0.9); g.lineWidth = 0.006; for (let k = -3; k <= 3; k++) { g.beginPath(); g.moveTo(k * 0.022, -0.07); g.lineTo(k * 0.022, 0.07); g.stroke(); } }
        else { g.fillStyle = rgba(WHITE, 0.5); g.fillRect(-0.08, -0.08, 0.17, 0.16); }
      }, [-0.1, -0.1, 0.1, 0.1], { tol: 0.1, reliefAmp: 0.008 });
    },
    cavity: { r: 0.06, gain: 7, amt: 0.4, tint: () => [60, 26, 22] },
    reliefFn: (id, Q) => (id === C.RIB || Q[1] < 0.06 ? Math.sin(Math.atan2(Q[0], Q[2]) * 60) * 0.006 : (knit(Q) - 0.4) * 0.012),
    soft: 0.02, edge: 0.6, frame: { c: [0, 0.68, 0], size: 1.9 },
  };
}

// =====================================================================================================
// Tranh dải (W×H px; v = 0 ở gốc chi)
// =====================================================================================================
const skinRib = (base, old) => (u, v, out, s) => {
  const c = base.slice(); const n = vn2(u * 6, v * 30) - 0.5;
  out[0] = c[0] * (1 + n * 0.08); out[1] = c[1] * (1 + n * 0.08); out[2] = c[2] * (1 + n * 0.08);
  if (old) { const sp = vn2(u * 14 + 5, v * 40); if (sp > 0.75) { out[0] -= 30 * (sp - 0.75) * 4; out[1] -= 40 * (sp - 0.75) * 4; out[2] -= 42 * (sp - 0.75) * 4; } }
};
function clothRib(base, dark, lite, foldAt = [], cuff = null) {
  return (u, v, out, s) => {
    let c = base.slice();
    const f = vn2(u * 3 + v * 2, v * 9);
    c = lerp3(c, dark, smooth(0.55, 0.85, f) * 0.6); c = lerp3(c, lite, smooth(0.35, 0.1, f) * 0.3);
    for (const [v0, w] of foldAt) { const d = Math.abs(v - v0 - 0.02 * Math.sin(u * 6)); c = lerp3(c, dark, (1 - smooth(0, w, d)) * 0.5 * (0.5 + 0.5 * Math.cos(u * 9))); }
    if (cuff && v > cuff[0]) c = lerp3(c, cuff[1], 0.7);
    const n = vn2(u * 20, v * 120) - 0.5; out[0] = c[0] * (1 + n * 0.1); out[1] = c[1] * (1 + n * 0.1); out[2] = c[2] * (1 + n * 0.1);
  };
}

export function ribbonDesigns(isIda, hi, sheet) {
  const R = (w, h) => ({ W: hi ? w * 2 : w, H: hi ? h * 2 : h });
  if (isIda) return {
    sleeve: { ...R(64, 512), aspect: 13, color: clothRib(ida.coat, [42, 58, 56], [88, 112, 106], [[0.5, 0.05], [0.44, 0.03], [0.57, 0.03]], [0.9, [52, 70, 68]]),
      relief: (u, v) => (vn2(u * 3 + v * 2, v * 9) - 0.5) * 0.12 + (v > 0.9 && v < 0.915 ? 0.08 : 0), edge: 0.3,
      draw(g, W, H) { g.strokeStyle = rgba([110, 80, 64], 0.8); g.lineWidth = Math.max(1, W / 40); g.beginPath(); g.moveTo(0, H * 0.985); g.lineTo(W, H * 0.985); g.stroke(); } }, // lót áo lộ ở mép tay áo
    leg: { ...R(32, 256), aspect: 18, color: clothRib(ida.stocking, [30, 28, 30], [70, 64, 66]), edge: 0.2 },
    boot: { ...R(64, 128), aspect: 4, color: clothRib(ida.boots, [20, 16, 15], [70, 58, 50]), endRound: [0.2, 0.25], edge: 0.2 },
    shaft: { ...R(32, 64), aspect: 3, color: clothRib(ida.boots, [20, 16, 15], [70, 58, 50]), edge: 0.2 },
    neck: { ...R(64, 128), aspect: 3, color: (u, v, out) => { skinRib(ida.skin, false)(u, v, out); const w = smooth(0.55, 0.9, vn2(u * 3, v * 9)); out[0] -= w * 12; out[1] -= w * 18; out[2] -= w * 14; },
      relief: (u, v) => -smooth(0.55, 0.9, vn2(u * 3, v * 9)) * 0.03 },
    skirt: { ...R(128, 512), aspect: 6, edge: 0.6, // v: 0 → 0.8 áo khoác; 0.8 → 1 váy
      color(u, v, out) { const hem = 0.8;
        if (v < hem) { clothRib(ida.coat, [40, 56, 54], [86, 110, 104])(u, v * 1.2, out); const fold = Math.sin(u * 22 + vn2(u * 4, v * 3) * 4); const k = 0.5 + 0.5 * fold; out[0] *= 0.86 + 0.18 * k; out[1] *= 0.86 + 0.18 * k; out[2] *= 0.86 + 0.18 * k;
          if (Math.abs(u - 0.5) < 0.012 && v > 0.12) { out[0] *= 0.6; out[1] *= 0.6; out[2] *= 0.6; } // mép vạt trước
          if (v > hem - 0.02) { out[0] *= 0.8; out[1] *= 0.8; out[2] *= 0.8; } }
        else { const fold = 0.5 + 0.5 * Math.sin(u * 30 + vn2(u * 5, v * 5) * 3); put(out, lerp3([70, 52, 62], [112, 88, 100], fold)); if (v > 0.97) put(out, lerp3(out, [60, 44, 52], 0.6)); }
      },
      relief: (u, v) => (v < 0.8 ? Math.sin(u * 22 + vn2(u * 4, v * 3) * 4) * 0.03 : Math.sin(u * 30 + vn2(u * 5, v * 5) * 3) * 0.03) },
    palm: { ...R(64, 64), aspect: 2.6, width: (v) => 0.76 + 0.24 * smooth(0.0, 0.55, v), color: skinRib([214, 170, 146], true), edge: 0.2, endRound: [0, 0.2],
      draw(g, W, H) { g.strokeStyle = rgba([150, 100, 90], 0.7); g.lineWidth = W / 60; for (const [a, b, c, d] of [[0.2, 0.55, 0.8, 0.35], [0.25, 0.7, 0.7, 0.6], [0.6, 0.3, 0.45, 0.9]]) { g.beginPath(); g.moveTo(a * W, b * H); g.quadraticCurveTo(0.5 * W, 0.5 * H, c * W, d * H); g.stroke(); } } },
    back: { ...R(64, 64), aspect: 2.6, width: (v) => 0.76 + 0.24 * smooth(0.0, 0.55, v), color: skinRib([208, 168, 146], true), edge: 0.2, endRound: [0, 0.12],
      draw(g, W, H) { g.strokeStyle = rgba([150, 116, 124], 0.55); g.lineWidth = W / 50; for (const x of [0.3, 0.45, 0.6, 0.72]) { g.beginPath(); g.moveTo(0.5 * W, 0.05 * H); g.quadraticCurveTo(x * W, 0.5 * H, (x + (x - 0.5) * 0.4) * W, 0.92 * H); g.stroke(); } },
      relief: (u, v) => { let r = 0; for (const x of [0.3, 0.45, 0.6, 0.72]) r += Math.exp(-(((u - (0.5 + (x - 0.5) * v * 1.3)) / 0.03) ** 2)) * smooth(0.2, 0.9, v) * 0.04; return r + smooth(0.85, 1.0, v) * 0.05; } },
    finger: { ...R(32, 128), aspect: 8, edge: 0.2, endRound: [0, 0.2], width: (v) => 1 - 0.16 * v, color: skinRib([212, 166, 142], true),
      draw(g, W, H) { g.strokeStyle = rgba([150, 96, 86], 0.8); g.lineWidth = Math.max(1, H / 90); for (const v of [0.10, 0.52, 0.78]) { g.beginPath(); g.moveTo(W * 0.15, H * v); g.quadraticCurveTo(W * 0.5, H * (v + 0.02), W * 0.85, H * v); g.stroke(); } },
      relief: (u, v) => [0.10, 0.52, 0.78].reduce((a, v0) => a + Math.exp(-(((v - v0) / 0.04) ** 2)) * 0.06, 0) },
    fingerBack: { ...R(32, 128), aspect: 8, edge: 0.2, endRound: [0, 0.2], width: (v) => 1 - 0.16 * v, color: skinRib([206, 164, 142], true),
      draw(g, W, H) { g.fillStyle = rgba([226, 196, 182], 0.8); g.beginPath(); g.ellipse(W * 0.5, H * 0.9, W * 0.28, H * 0.06, 0, 0, Math.PI * 2); g.fill();
        g.strokeStyle = rgba([150, 106, 100], 0.7); g.lineWidth = Math.max(1, H / 100); for (const v of [0.08, 0.5, 0.76]) for (let k = 0; k < 2; k++) { g.beginPath(); g.moveTo(W * 0.3, H * (v + k * 0.02)); g.lineTo(W * 0.7, H * (v + k * 0.02)); g.stroke(); } },
      relief: (u, v) => [0.08, 0.5, 0.76].reduce((a, v0) => a + Math.exp(-(((v - v0) / 0.05) ** 2)) * 0.08, 0) },
  };
  const th = sheet.parts.thigh.length, sh = sheet.parts.shin.length, hm = sheet.costume.trousers.hem_above_ankle_H;
  const lens = [th * 0.5 + 0.08, th * 0.5, sh * 0.45, sh * 0.55 - hm, 0.005, hm], tot = lens.reduce((a, b) => a + b);
  const vHem = (tot - hm - 0.005) / tot;
  return {
    sleeve: { ...R(64, 512), aspect: 12, edge: 0.5, // len đan, bo tay ~14 % cuối (từ gần cổ tay)
      color(u, v, out) { const cuff = v > 0.86; const row = Math.sin(v * (cuff ? 30 : 260)), col = Math.abs(Math.sin(u * (cuff ? 40 : 24) + (row > 0 ? 0.6 : -0.6)));
        let c = cuff ? lerp3([108, 54, 42], [150, 82, 66], 0.5 + 0.5 * Math.sin(u * 40)) : lerp3([116, 60, 48], [158, 88, 70], 0.5 * col + 0.25 * (row * 0.5 + 0.5));
        c = lerp3(c, [96, 48, 40], smooth(0.5, 0.85, vn2(u * 3 + v * 3, v * 10)) * 0.5); put(out, c); },
      relief: (u, v) => (v > 0.86 ? Math.sin(u * 40) * 0.05 : Math.sin(v * 260) * 0.02) + (vn2(u * 3 + v * 3, v * 10) - 0.5) * 0.15 },
    leg: { ...R(32, 256), aspect: 18, edge: 0.3, // quần tới vHem (khớp hàng dải trong cast2d.js); cổ chân trần
      color(u, v, out) { if (v < vHem) { clothRib(cas.trousers, [36, 38, 46], [82, 86, 98])(u, v, out); if (v > vHem - 0.03) { out[0] *= 0.8; out[1] *= 0.8; out[2] *= 0.8; } } else skinRib([222, 184, 158])(u, v, out); } },
    boot: { ...R(64, 128), aspect: 4, color: clothRib(cas.boots, [22, 18, 16], [76, 64, 56]), endRound: [0.2, 0.3], edge: 0.2 },
    shaft: { ...R(32, 64), aspect: 3, color: clothRib(cas.boots, [22, 18, 16], [76, 64, 56]), edge: 0.2 },
    neck: { ...R(64, 128), aspect: 3, color: skinRib(cas.skin) },
    palm: { ...R(64, 64), aspect: 2.6, width: (v) => 0.76 + 0.24 * smooth(0.0, 0.55, v), color: skinRib([226, 184, 160]), edge: 0.2, endRound: [0, 0.2],
      draw(g, W, H) { g.strokeStyle = rgba([180, 120, 108], 0.6); g.lineWidth = W / 60; for (const [a, b, c, d] of [[0.2, 0.55, 0.8, 0.35], [0.25, 0.7, 0.7, 0.6]]) { g.beginPath(); g.moveTo(a * W, b * H); g.quadraticCurveTo(0.5 * W, 0.5 * H, c * W, d * H); g.stroke(); } } },
    back: { ...R(64, 64), aspect: 2.6, width: (v) => 0.76 + 0.24 * smooth(0.0, 0.55, v), color: skinRib([222, 182, 158]), edge: 0.2, endRound: [0, 0.2], relief: (u, v) => smooth(0.85, 1.0, v) * 0.04 },
    finger: { ...R(32, 128), aspect: 8, edge: 0.2, endRound: [0, 0.22], width: (v) => 1 - 0.14 * v, color: skinRib([226, 180, 156]),
      draw(g, W, H) { g.strokeStyle = rgba([186, 126, 112], 0.7); g.lineWidth = Math.max(1, H / 110); for (const v of [0.10, 0.52, 0.78]) { g.beginPath(); g.moveTo(W * 0.2, H * v); g.lineTo(W * 0.8, H * v); g.stroke(); } } },
    fingerBack: { ...R(32, 128), aspect: 8, edge: 0.2, endRound: [0, 0.22], width: (v) => 1 - 0.14 * v, color: skinRib([222, 180, 158]),
      draw(g, W, H) { g.fillStyle = rgba([236, 206, 192], 0.85); g.beginPath(); g.ellipse(W * 0.5, H * 0.9, W * 0.26, H * 0.06, 0, 0, Math.PI * 2); g.fill(); } },
  };
}

// Chuẩn hoá điểm neo: {tên: [p, n]} → snap lên khối (làm một lần cho mỗi thiết kế).
export function prepare(design, snapFn) {
  const A = {};
  for (const [k, [p, n]] of Object.entries(design.anchors || {})) A[k] = snapFn(design.prims, design.groups, p, n);
  const f = design.features;
  design.features = f ? (api) => f(api, A) : null;
  return design;
}

export const DESIGNS = { ida: { head: idaHeadDesign, torso: idaTorsoDesign }, cas: { head: casHeadDesign, torso: casTorsoDesign } };
export const COLORS = { ida, cas };

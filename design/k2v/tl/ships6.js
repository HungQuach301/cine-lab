// K2V tl · V6 (lệnh P6 chủ dự án 18/10) · PIN NỔI 1782 DỰNG CHI TIẾT theo bản khắc PD/CC0 có trong TIEN-KY T3:
//  Rijks RP-P-OB-19.249 "The Destruction of the Floating Batteries before Gibraltar" (Serres/Jukes 1783, CC0) — thân tàu tối mạn cao, MỘT HÀNG LỖ PHÁO ở mạn đánh,
//  MÁI DỐC LỚN che sàn (phủ da/lớp chống đạn nung theo thiết kế d'Arçon — màu nâu đỏ, sườn mái), đuôi có lan can/khung mắt cáo; Drinkwater 1786 "View of the grand attack".
//  Cột buồm: 13/9 pin nổi tự đi vào vị trí (Drinkwater: "got under way … bore down") → còn cột thấp + trục + buồm cuộn (bản khắc 14/9 vẽ cột đã gãy/cụt).
//  KÍCH THƯỚC thân: chưa có nguồn số → minh hoạ (dài 54 m, rộng 15 m), nhãn "hulls drawn from engravings · illustrative". Không người trên boong (§10.6).
//  Một BufferGeometry màu đỉnh mỗi pin (gộp), hướng: mũi +X, mạn đánh = +Z cục bộ (makeFleet quay theo heading; cảnh chọn side).
import { THREE } from './core.js';

export function batteryV6(R, { side = 1, burning = false } = {}) {
  const P = [], C = [], push = (a, b, c, col) => { P.push(...a, ...b, ...c); C.push(...col, ...col, ...col); }, quad = (a, b, c, d, col) => { push(a, b, c, col); push(a, c, d, col); };
  const L = 54, B = 15, sh = (k, col) => col.map((v) => v * k), wood = [0.075, 0.055, 0.04], wale = [0.03, 0.025, 0.02], ochre = [0.30, 0.22, 0.11], hide = [0.14, 0.08, 0.055], lightw = [0.48, 0.40, 0.29], iron = [0.05, 0.05, 0.055], canvas = [0.78, 0.74, 0.64];
  // --- thân: trạm dọc x, nửa bề rộng theo x và cao y (thắt đáy, phình hông, thu vào ở mạn trên — tumblehome); mạn cao dần về đuôi/mũi (sheer)
  const NX = 24, Ys = [-4.8, -3.6, -2.0, 0.0, 1.6, 3.2, 4.6, 5.6];
  const half = (x, y) => { const u = x / (L / 2), bow = u > 0 ? Math.pow(Math.max(0, 1 - u * u * u * u), 0.5) * Math.max(0, 1 - Math.pow(u, 6)) : Math.pow(Math.max(0, 1 - Math.pow(-u, 8)), 0.35);
    const yk = y < -1 ? 0.55 + 0.45 * Math.sin(Math.PI / 2 * (y + 4.8) / 3.8) : y < 2.5 ? 1.0 : 1.0 - 0.08 * (y - 2.5) / 3.1; return Math.max(0.05, B / 2 * bow * yk * (y < -4.2 ? 0.35 : 1)); };
  const sheer = (x) => 2.6 * Math.pow(Math.abs(x) / (L / 2), 2.2) + (x > L * 0.38 ? (x - L * 0.38) * 0.35 : 0);   // cong mạn + mũi vểnh
  const st = [...Array(NX + 1).keys()].map((i) => -L / 2 + L * i / NX);
  const colAt = (y) => (y > 1.0 && y < 1.6 ? wale : y > 3.9 && y < 4.4 ? ochre : y < 0.15 ? sh(0.6, wood) : wood);
  for (let i = 0; i < NX; i++) for (let j = 0; j < Ys.length - 1; j++) for (const sd of [1, -1]) {
    const x0 = st[i], x1 = st[i + 1], y0 = Ys[j], y1 = Ys[j + 1], ya = (x) => (j >= Ys.length - 3 ? sheer(x) * (j === Ys.length - 2 ? 1 : 0.5) : 0), yb = (x) => (j >= Ys.length - 2 ? sheer(x) * 0.5 : 0);
    const a = [x0, y0 + yb(x0), sd * half(x0, y0)], b = [x1, y0 + yb(x1), sd * half(x1, y0)], c = [x1, y1 + ya(x1), sd * half(x1, y1)], d = [x0, y1 + ya(x0), sd * half(x0, y1)], col = sh(0.85 + 0.25 * R(), colAt((y0 + y1) / 2));
    if (sd > 0) quad(a, b, c, d, col); else quad(b, a, d, c, col); }
  // đuôi phẳng (transom) + khung mắt cáo lan can đuôi (bản khắc: đuôi trang trí sáng)
  const xs = -L / 2 + 0.5, tw = half(xs, 4.0); quad([xs, 0, -tw], [xs, 0, tw], [xs, 7.4, tw * 0.85], [xs, 7.4, -tw * 0.85], sh(0.9, wood));
  for (let k = 0; k < 6; k++) { const z = -tw * 0.8 + k * tw * 1.6 / 5; quad([xs - 0.12, 4.6, z - 0.08], [xs - 0.12, 4.6, z + 0.08], [xs - 0.12, 7.2, z + 0.08], [xs - 0.12, 7.2, z - 0.08], lightw); }
  for (const y of [4.6, 5.9, 7.2]) quad([xs - 0.12, y - 0.07, -tw * 0.82], [xs - 0.12, y - 0.07, tw * 0.82], [xs - 0.12, y + 0.07, tw * 0.82], [xs - 0.12, y + 0.07, -tw * 0.82], lightw);
  // sàn (dưới mái) — chỉ thấy ở mép
  quad([-L / 2 + 1, 5.0, -half(0, 5) + 0.3], [L / 2 - 2, 5.0, -half(0, 5) + 0.3], [L / 2 - 2, 5.0, half(0, 5) - 0.3], [-L / 2 + 1, 5.0, half(0, 5) - 0.3], sh(0.7, lightw));
  // --- MÁI DỐC che sàn: từ mép mạn đánh (y 5,6) lên NÓC lệch về mạn kia (y 12,5, z = −0,25 B·side) rồi xuống mép mạn kia (y 7); sườn mái mỗi 1,6 m (màu đậm hơn)
  const rx0 = -L / 2 + 4, rx1 = L / 2 - 6, zr = -0.22 * B * side, zA = side * (half(0, 5.6) - 0.2), zB = -side * (half(0, 5.6) - 0.2);
  for (let x = rx0; x < rx1; x += 1.6) { const x1 = Math.min(rx1, x + 1.6), k = 0.7 + 0.5 * R(), rib = sh(0.55, hide);   // da ướt: tối, loang không đều
    const A0 = [x, 5.6, zA], A1 = [x1, 5.6, zA], T0 = [x, 12.5, zr], T1 = [x1, 12.5, zr], B0 = [x, 7.0, zB], B1 = [x1, 7.0, zB];
    if (side > 0) { quad(A0, T0, T1, A1, sh(k, hide)); quad(T0, B0, B1, T1, sh(k * 0.9, hide)); } else { quad(A1, T1, T0, A0, sh(k, hide)); quad(T1, B1, B0, T0, sh(k * 0.9, hide)); }
    const xr = x1 - 0.12, d = side > 0 ? 0.06 : -0.06; quad([xr, 5.6, zA + d], [xr, 12.5, zr + d], [xr + 0.24, 12.5, zr + d], [xr + 0.24, 5.6, zA + d], rib); }
  for (const xe of [rx0, rx1]) push([xe, 5.6, zA], [xe, 12.5, zr], [xe, 7.0, zB], sh(0.75, hide));   // đầu hồi tam giác
  // --- MỘT HÀNG LỖ PHÁO + nòng ở mạn đánh (y ≈ 2,6) — 13 khẩu/pin (≈ 138–142 khẩu / 10 pin, S068)
  for (let k = 0; k < 13; k++) { const x = -L * 0.36 + k * L * 0.058, z = side * (half(x, 2.6) + 0.02), w = 0.75, h = 0.7;
    quad([x - w / 2, 2.25, z], [x + w / 2, 2.25, z], [x + w / 2, 2.25 + h, z], [x - w / 2, 2.25 + h, z].map((v, i) => v), [0.02, 0.015, 0.012]);
    if (side < 0) { /* mặt quay ngược: vẽ hai phía */ quad([x + w / 2, 2.25, z], [x - w / 2, 2.25, z], [x - w / 2, 2.25 + h, z], [x + w / 2, 2.25 + h, z], [0.02, 0.015, 0.012]); }
    const r = 0.2, l = 1.4, zz = z + side * l; for (let q = 0; q < 6; q++) { const a0 = q / 6 * 6.283, a1 = (q + 1) / 6 * 6.283; const p = (a, zv) => [x + Math.cos(a) * r, 2.6 + Math.sin(a) * r, zv]; quad(p(a0, z), p(a1, z), p(a1, zz), p(a0, zz), iron); } }
  // --- cột buồm: mũi + chính (thấp, có trục + buồm cuộn), cột cờ đuôi; dây chằng (tam giác mảnh) mỗi bên
  const mast = (x, h, yardW) => { const r = 0.32; for (let q = 0; q < 6; q++) { const a0 = q / 6 * 6.283, a1 = (q + 1) / 6 * 6.283; quad([x + Math.cos(a0) * r, 5, Math.sin(a0) * r], [x + Math.cos(a1) * r, 5, Math.sin(a1) * r], [x + Math.cos(a1) * r * 0.6, 5 + h, Math.sin(a1) * r * 0.6], [x + Math.cos(a0) * r * 0.6, 5 + h, Math.sin(a0) * r * 0.6], sh(1.2, wood)); }
    for (const [yy, ww] of [[5 + h * 0.62, yardW], [5 + h * 0.95, yardW * 0.7]]) { quad([x - 0.2, yy, -ww / 2], [x + 0.2, yy, -ww / 2], [x + 0.2, yy, ww / 2], [x - 0.2, yy, ww / 2], sh(1.1, wood));
      for (let q = 0; q < 2; q++) { const yb = yy - 0.25 - q * 0.6; quad([x + 0.35, yb - 0.6, -ww * 0.45], [x + 0.35, yb - 0.6, ww * 0.45], [x + 0.35, yb, ww * 0.45], [x + 0.35, yb, -ww * 0.45], sh(0.9 + 0.1 * q, canvas)); quad([x + 0.35, yb, -ww * 0.45], [x + 0.35, yb, ww * 0.45], [x + 0.35, yb - 0.6, ww * 0.45], [x + 0.35, yb - 0.6, -ww * 0.45], sh(0.8, canvas)); } }
    for (const sd of [1, -1]) { const zb = sd * (half(x, 5) - 0.2); push([x - 1.6, 5.4, zb], [x + 1.6, 5.4, zb], [x, 5 + h * 0.6, sd * 0.3], [0.04, 0.035, 0.03]); push([x + 1.6, 5.4, zb], [x - 1.6, 5.4, zb], [x, 5 + h * 0.6, sd * 0.3], [0.04, 0.035, 0.03]); } };
  if (!burning || R() < 0.5) { mast(L * 0.22, 17, 12); mast(-L * 0.06, 21, 15); } else mast(-L * 0.06, 9, 0.1);   // pin cháy: cột chính cụt
  // mũi: xà mũi (bowsprit)
  { const x0 = L / 2 - 2, r = 0.25; for (let q = 0; q < 5; q++) { const a0 = q / 5 * 6.283, a1 = (q + 1) / 5 * 6.283; quad([x0, 5.2 + Math.cos(a0) * r, Math.sin(a0) * r], [x0, 5.2 + Math.cos(a1) * r, Math.sin(a1) * r], [x0 + 11, 8.5 + Math.cos(a1) * r * 0.5, Math.sin(a1) * r * 0.5], [x0 + 11, 8.5 + Math.cos(a0) * r * 0.5, Math.sin(a0) * r * 0.5], sh(1.1, wood)); } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true;
  const grp = new THREE.Group(); grp.add(o); grp.userData.tris = P.length / 9; return grp;
}

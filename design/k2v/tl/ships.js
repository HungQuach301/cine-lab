// K2V tl · TÀU THEO THỜI KỲ (V5b-1b, lớp nội dung trung cảnh — cổng 16/10: "khung trống, biển chiếm phần lớn").
// Ba thế hệ, mỗi chiếc có cửa sổ năm riêng (xuất hiện/biến mất so le, không đổi đột ngột cả bến):
//   buồm 1704–1860 (vịnh phía tây phố trong tường; mở đầu kể "British and Dutch forces capture Gibraltar" — số lượng MINH HOẠ, không theo sổ hạm đội)
//   · thuyền nhỏ + tàu hơi nước 1860–1965 (ảnh LoC 2025710366 c.1900 cho thấy nhiều thuyền neo vịnh phía tây eo đất)
//   · tàu hàng/tàu dầu tiếp nhiên liệu/tàu khách 1965–2026 (neo vịnh Gibraltar — đặc trưng hiện nay). Hình khối cách điệu, không mô phỏng tàu cụ thể.
import { THREE, rng } from './core.js';

const L = (c) => new THREE.MeshLambertMaterial({ color: c });
function hullGeo(len, beam, depth, bowK = 0.22) {   // thân: mặt bằng nhọn mũi, đùn đứng
  const s = new THREE.Shape(), hl = len / 2, hb = beam / 2;
  s.moveTo(-hl, -hb * 0.85); s.lineTo(hl * (1 - bowK * 2), -hb); s.quadraticCurveTo(hl, -hb * 0.6, hl, 0); s.quadraticCurveTo(hl, hb * 0.6, hl * (1 - bowK * 2), hb); s.lineTo(-hl, hb * 0.85); s.lineTo(-hl, -hb * 0.85);
  return new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: false }).rotateX(-Math.PI / 2);   // y lên, x = dọc tàu
}
export function makeShips(U) {
  const group = new THREE.Group(), R = rng(73), ships = [];
  const add = (kind, e, n, rot, y0, y1) => {
    const g = new THREE.Group(); g.position.set(e, 0, -n); g.rotation.y = rot; const m = (geo, mat, x, y, z) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; g.add(o); };
    if (kind === 'sail') { const len = 34 + 14 * R(); m(hullGeo(len, len * 0.27, 6), L(0x4a3426), 0, -2.2, 0); m(new THREE.BoxGeometry(len * 0.92, 0.9, len * 0.255), L(0xb8a070), -len * 0.02, 3.0, 0);
      for (const [x, hh] of [[-len * 0.28, 22], [0.02 * len, 27], [len * 0.28, 20]]) { m(new THREE.CylinderGeometry(0.35, 0.45, hh, 5), L(0x3a2a1e), x, hh / 2 + 2, 0);
        for (let k = 0; k < 3; k++) m(new THREE.BoxGeometry(0.4, hh * 0.24, len * 0.26 * (1 - k * 0.18)), L(k === 0 ? 0xefe8d6 : 0xe6dcc4), x + 0.6, 7 + k * hh * 0.27, 0); } }
    else if (kind === 'boat') { const len = 7 + 5 * R(); m(hullGeo(len, len * 0.3, 1.6, 0.3), L([0x2f5d7a, 0x7a2f2a, 0xe8e2d0, 0x3c5a3a][Math.floor(R() * 4)]), 0, -0.6, 0); if (R() < 0.6) { m(new THREE.CylinderGeometry(0.1, 0.12, len * 0.9, 4), L(0x4a3a2a), 0, len * 0.45, 0); m(new THREE.BoxGeometry(0.1, len * 0.6, len * 0.4), L(0xf0ead8), 0.3, len * 0.42, 0); } }
    else if (kind === 'steam') { const len = 60 + 30 * R(); m(hullGeo(len, len * 0.14, 7, 0.15), L(0x1e2226), 0, -3, 0); m(new THREE.BoxGeometry(len * 0.3, 4, len * 0.1), L(0xeee8dc), -len * 0.05, 5.5, 0);
      m(new THREE.CylinderGeometry(1.6, 1.8, 9, 8), L(R() < 0.5 ? 0xb03a2e : 0x2a2a2a), -len * 0.05, 11, 0); for (const x of [-len * 0.32, len * 0.3]) m(new THREE.CylinderGeometry(0.3, 0.35, 18, 4), L(0x3a3a3a), x, 13, 0); }
    else if (kind === 'cargo') { const len = 150 + 80 * R(), b = len * 0.15; m(hullGeo(len, b, 12, 0.12), L([0x2c3e66, 0x7a2a28, 0x2d4a3a, 0x222428][Math.floor(R() * 4)]), 0, -6, 0); m(new THREE.BoxGeometry(len * 0.9, 1, b * 0.96), L(0x8a3a2a), 0, 6.2, 0);
      m(new THREE.BoxGeometry(len * 0.1, 14, b * 0.9), L(0xf2f0ea), -len * 0.4, 13, 0);
      if (R() < 0.6) for (let k = 0; k < 7; k++) m(new THREE.BoxGeometry(len * 0.09, 6 + 4 * R(), b * 0.86), L([0xb4472e, 0x2f6a8a, 0x8a8a3a, 0x6a2a4a, 0xd0c8b0][Math.floor(R() * 5)]), -len * 0.25 + k * len * 0.1, 9 + 2 * R(), 0);
      else for (let k = 0; k < 3; k++) m(new THREE.CylinderGeometry(1.0, 1.0, len * 0.18, 6).rotateZ(Math.PI / 2), L(0xd8d4c8), -len * 0.18 + k * len * 0.2, 8, 0); }   // tàu dầu: ống trên boong
    else if (kind === 'cruise') { const len = 230; m(hullGeo(len, 30, 14, 0.1), L(0xf4f4f2), 0, -7, 0); for (let k = 0; k < 5; k++) m(new THREE.BoxGeometry(len * (0.8 - k * 0.08), 3, 28 - k * 1.5), L(k % 2 ? 0x2f4a6a : 0xf6f6f4), -len * 0.04, 8.5 + k * 3, 0);
      m(new THREE.BoxGeometry(14, 8, 10), L(0x2a3a5a), -len * 0.3, 27, 0); }
    g.visible = false; group.add(g); ships.push({ g, y0, y1 });
  };
  // buồm 1704–1860: vịnh phía tây phố trong tường (E < −1150 m, N −600…−1900 m: nước ở mọi năm)
  for (let k = 0; k < 11; k++) add('sail', -1250 - R() * 900, -650 - R() * 1250, R() * 6.28, 1700 + R() * 8, 1795 + R() * 65);
  // thuyền nhỏ 1860–1965: vịnh tây eo đất (ảnh LoC c.1900) + bến phố
  for (let k = 0; k < 40; k++) { const w = R() < 0.6; add('boat', w ? -1150 - R() * 900 : -1300 - R() * 600, w ? 250 + R() * 500 : -500 - R() * 1200, R() * 6.28, 1860 + R() * 30, 1945 + R() * 25); }
  for (let k = 0; k < 9; k++) add('steam', -1300 - R() * 1100, -400 - R() * 1500, R() * 6.28, 1862 + R() * 40, 1940 + R() * 30);
  // hiện đại 1965–2026: tàu hàng/tàu dầu neo vịnh, tàu khách ở cảng
  for (let k = 0; k < 13; k++) add('cargo', -1500 - R() * 2600, -1600 + R() * 3400, R() * 6.28, 1965 + R() * 40, 2100);
  add('cruise', -1180, -1250, -0.25, 2008, 2100);
  function update(year) { for (const s of ships) s.g.visible = year >= s.y0 && year < s.y1; }
  return { group, update, n: ships.length };
}

// ======================================================================================================================================
// V5b-2b (T3 P0, M3 rút gọn) · HẠM ĐỘI THEO ĐỘI HÌNH + ĐƯỜNG ĐI THEO GIỜ. Mỗi tàu nội suy vị trí theo "giá trị thời gian" tv (giờ trong ngày ở cảnh mốc đinh,
//  hoặc năm thập phân), hướng mũi theo chuyển động (đứng yên: hướng khai). Kiểu: 'battery' (pin nổi 1782 — hình dáng MINH HOẠ theo bản khắc Rijks RP-P-OB-19.249
//  / Drinkwater view: thân thấp, mái nghiêng che sàn pháo, một hàng lỗ pháo, 2 cột ngắn; kích thước thân tàu CHƯA có nguồn → nhãn "illustrative"),
//  'line' (tàu chiến tuyến), 'sail', 'boat' (như makeShips). Không người trên boong (luật hình chiến tranh §6.2).
export function lineFormation({ n, center, axis = 0, spacing = 140, ...rest }) {   // n tàu xếp hàng dọc trục axis (độ, 0 = Bắc, chiều kim đồng hồ) quanh center [E, N]
  const a = axis * Math.PI / 180, u = [Math.sin(a), Math.cos(a)];
  return [...Array(n).keys()].map((i) => { const o = (i - (n - 1) / 2) * spacing; return Object.assign({ at: [center[0] + u[0] * o, center[1] + u[1] * o] }, rest); });
}
function batteryGroup(R) {
  const g = new THREE.Group(), m = (geo, mat, x, y, z, ry = 0) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); o.rotation.y = ry; o.castShadow = o.receiveShadow = true; g.add(o); return o; };
  const len = 50 + 6 * R(), beam = 15;
  m(hullGeo(len, beam, 5.5, 0.16), L(0x3a2c20), 0, -2.6, 0);
  m(new THREE.BoxGeometry(len * 0.86, 2.2, beam * 0.9), L(0x4a3828), -len * 0.03, 3.4, 0);   // sàn pháo
  const roof = new THREE.BoxGeometry(len * 0.8, 0.7, beam * 0.62); const r1 = m(roof, L(0x5a4632), -len * 0.03, 6.2, beam * 0.2); r1.rotation.x = 0.42;   // mái nghiêng che sàn (phía hướng thành)
  for (let k = 0; k < 11; k++) for (const sd of [-1, 1]) m(new THREE.BoxGeometry(1.3, 1.2, 0.3), L(0x120e0a), -len * 0.38 + k * len * 0.068, 3.6, sd * beam * 0.455);   // hàng lỗ pháo hai mạn
  for (const sd of [-1, 1]) { m(new THREE.BoxGeometry(len * 0.88, 0.45, 0.35), L(0xb89a6a), -len * 0.03, 4.75, sd * beam * 0.46); m(new THREE.BoxGeometry(len * 0.9, 0.35, 0.3), L(0x8a6a44), 0, 1.6, sd * beam * 0.5); }   // mép boong gỗ sáng + gờ mạn (đọc được khối thân ở xa)
  m(new THREE.BoxGeometry(len * 0.97, 0.5, beam * 0.98), L(0x1c1a17), 0, 0.15, 0);   // đường mớn nước tối
  for (const [x, hh] of [[-len * 0.2, 16], [len * 0.18, 14]]) { m(new THREE.CylinderGeometry(0.35, 0.45, hh, 5), L(0x2e241b), x, hh / 2 + 4, 0); m(new THREE.CylinderGeometry(0.5, 0.5, beam * 0.6, 5).rotateX(Math.PI / 2), L(0xd8ccb0), x + 0.4, hh * 0.72 + 4, 0); }   // cột ngắn + buồm cuộn
  // V5b-2d: đọc được ở xa — cột chính cao + trục ngang + buồm thu nửa (bản khắc RP-P-OB-19.249 vẽ pin nổi có cột buồm), dải mạn sơn vàng đất, nòng pháo ló ở lỗ pháo,
  //  mái che phủ da sống ướt (màu nâu đỏ — chống đạn nung theo thiết kế d'Arçon), cột cờ đuôi (cờ trắng hải quân Bourbon trước 1785 — minh hoạ)
  m(new THREE.CylinderGeometry(0.4, 0.55, 26, 6), L(0x2e241b), 0, 17, 0); for (const [y, w] of [[14, 0.62], [22, 0.48]]) { m(new THREE.CylinderGeometry(0.22, 0.22, beam * w * 1.6, 5).rotateX(Math.PI / 2), L(0x2e241b), 0.3, y, 0); m(new THREE.BoxGeometry(0.3, 4.2, beam * w * 1.5), L(0xe6dcc4), 0.7, y - 2.2, 0); }
  for (const sd of [-1, 1]) m(new THREE.BoxGeometry(len * 0.86, 0.9, 0.2), L(0xa8823e), -len * 0.03, 2.5, sd * beam * 0.49);
  for (let k = 0; k < 11; k++) m(new THREE.CylinderGeometry(0.22, 0.26, 1.4, 6).rotateX(Math.PI / 2), L(0x0c0c0d), -len * 0.38 + k * len * 0.068, 3.6, beam * 0.5 + 0.4);
  r1.material = L(0x6e3b28);
  m(new THREE.CylinderGeometry(0.12, 0.15, 8, 4), L(0x2e241b), -len * 0.47, 9, 0); m(new THREE.BoxGeometry(0.06, 2.0, 3.2), L(0xf2efe6), -len * 0.47, 11.8, -1.6);
  return g;
}
export function makeFleet(U, specs) {
  const group = new THREE.Group(), R = rng(1782), list = [];
  for (const sp of specs) {   // sp: {kind, at:[E,N] | path:[[tv, E, N], …], heading (độ), t:[hiện, ẩn] (tv)}
    let g; if (sp.kind === 'battery') g = batteryGroup(R);
    else { const tmp = new THREE.Group(); g = tmp; const len = sp.kind === 'line' ? 52 + 8 * R() : 36; const mm = (geo, mat, x, y, z) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; g.add(o); };
      mm(hullGeo(len, len * 0.27, 7, 0.2), L(0x3c2a1c), 0, -2.6, 0); mm(new THREE.BoxGeometry(len * 0.92, 1.0, len * 0.255), L(0xb09868), 0, 3.6, 0);
      for (const [x, hh] of [[-len * 0.3, 28], [0, 34], [len * 0.28, 25]]) { mm(new THREE.CylinderGeometry(0.4, 0.5, hh, 5), L(0x3a2a1e), x, hh / 2 + 2, 0); for (let k = 0; k < 3; k++) mm(new THREE.BoxGeometry(0.4, hh * 0.22, len * 0.27 * (1 - k * 0.18)), L(0xece4d0), x + 0.6, 8 + k * hh * 0.26, 0); } }
    g.visible = false; group.add(g); list.push({ sp, g });
  }
  const posAt = (sp, tv) => { if (!sp.path) return [sp.at[0], sp.at[1], null]; const P = sp.path; if (tv <= P[0][0]) return [P[0][1], P[0][2], null]; if (tv >= P[P.length - 1][0]) return [P[P.length - 1][1], P[P.length - 1][2], null];
    let i = 1; while (P[i][0] < tv) i++; const [t0, e0, n0] = P[i - 1], [t1, e1, n1] = P[i], u = (tv - t0) / (t1 - t0), s = u * u * (3 - 2 * u); return [e0 + (e1 - e0) * s, n0 + (n1 - n0) * s, Math.atan2(n1 - n0, e1 - e0)]; };
  return { group, list, n: list.length,
    update(tv) { for (const { sp, g } of list) { const vis = !sp.t || (tv >= sp.t[0] && tv <= sp.t[1]); g.visible = vis; if (!vis) continue; const [e, n, hd] = posAt(sp, tv);
      g.position.set(e, 0, -n); g.rotation.y = hd != null ? hd : (90 - (sp.heading || 0)) * Math.PI / 180; } },
    positions(tv) { return list.map(({ sp }) => posAt(sp, tv)); } };
}

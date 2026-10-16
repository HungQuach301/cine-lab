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

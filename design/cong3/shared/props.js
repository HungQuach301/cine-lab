// Đạo cụ dùng chung Cổng 3: cột đèn khí (luật thế giới mục 2: lồng kính trên cột ~3,4 m). Đợt vá A2+ (V4): thiết kế lại thành đạo cụ chi tiết.
// Kích thước (m) — trang đạo cụ: bible/props/gas-lamp.md
//   Cột: cao tới đáy lồng 2,95; bệ gang bát giác Ø0,36 cao 0,62 có gờ; thân thuôn Ø0,11→0,075; 2 vòng cổ.
//   Thanh móc thang (tựa thang): ngang 0,62 dưới lồng 0,30, hai đầu tròn.
//   Ống khí + van (đồng): ống Ø0,03 dọc thân lên đáy lồng; van xoay có tay gạt dài 0,10 (Ida mở/đóng bằng sào).
//   Lồng: đáy phễu vuông 0,20 → 0,12; khung sắt 4 trụ; 4 tấm kính hình thang (rộng 0,24 dưới, 0,34 trên, cao 0,42);
//         vành trên và dưới; nắp chóp vuông rộng 0,52 cao 0,20 có vành nhô; ống thông hơi Ø0,08 có mũ; quả chóp.
//   Bầu đốt: đế đồng Ø0,05 + mạng đèn (lửa) ở tâm lồng. Toàn bộ cao 3,40.
import * as THREE from './node_modules/three/build/three.module.js';

// buildGasLamp({height, mat}) → Group; userData.flame = điểm lửa (Object3D), userData.glassY = tâm lồng kính.
// mat(role, color): role ∈ 'iron' | 'brass' | 'glass' | 'flame'.
export function buildGasLamp({ height = 3.4, mat } = {}) {
  mat = mat || ((role, c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.7, metalness: role === 'iron' ? 0.4 : 0 }));
  const g = new THREE.Group(); g.name = 'gas_lamp';
  const iron = mat('iron', '#23252b'), iron2 = mat('iron', '#30333b'), brass = mat('brass', '#8a6a3a');
  const add = (geo, m, x, y, z, ry = 0) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.rotation.y = ry; g.add(o); return o; };
  const cyl = (r0, r1, h, m, y, seg = 16, ry = 0) => add(new THREE.CylinderGeometry(r0, r1, h, seg), m, 0, y, 0, ry);
  const cageY = height - 0.45;                                   // đáy lồng kính
  // bệ gang bát giác có gờ
  cyl(0.18, 0.2, 0.08, iron, 0.04, 8, Math.PI / 8); cyl(0.15, 0.18, 0.4, iron2, 0.28, 8, Math.PI / 8); cyl(0.17, 0.15, 0.05, iron, 0.505, 8, Math.PI / 8);
  cyl(0.1, 0.13, 0.12, iron, 0.59, 16);
  for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4 + Math.PI / 8; add(new THREE.BoxGeometry(0.012, 0.34, 0.012), iron, Math.cos(a) * 0.162, 0.28, Math.sin(a) * 0.162); }   // gờ đứng
  // thân thuôn + vòng cổ
  const shaftH = cageY - 0.65; cyl(0.0375, 0.055, shaftH, iron, 0.65 + shaftH / 2, 16);
  for (const yy of [1.3, cageY - 0.42]) { cyl(0.07, 0.07, 0.05, iron2, yy, 16); cyl(0.06, 0.07, 0.03, iron, yy + 0.04, 16); }
  // thanh móc thang: ngang, hai đầu tròn
  const armY = cageY - 0.3; add(new THREE.BoxGeometry(0.62, 0.035, 0.035), iron, 0, armY, 0);
  for (const s of [-1, 1]) add(new THREE.SphereGeometry(0.03, 10, 8), iron, s * 0.31, armY, 0);
  // ống khí + van đồng (tay gạt)
  add(new THREE.CylinderGeometry(0.014, 0.014, 0.3, 8), brass, 0.06, cageY - 0.16, 0);
  const valve = add(new THREE.CylinderGeometry(0.028, 0.028, 0.05, 12), brass, 0.06, cageY - 0.2, 0); valve.rotation.z = Math.PI / 2;
  const lever = add(new THREE.BoxGeometry(0.1, 0.012, 0.012), brass, 0.11, cageY - 0.2, 0); lever.rotation.z = -0.5;
  add(new THREE.SphereGeometry(0.014, 8, 6), brass, 0.155, cageY - 0.225, 0);
  // lồng: đáy phễu vuông, vành dưới, 4 trụ góc, 4 kính hình thang, vành trên
  const bot = add(new THREE.CylinderGeometry(0.14, 0.085, 0.1, 4, 1), iron, 0, cageY + 0.05, 0, Math.PI / 4);
  const H = 0.42, wB = 0.24, wT = 0.34, y0 = cageY + 0.1, thin = [];
  const frameRing = (w, y) => { for (const [dx, dz, sx, sz] of [[0, w / 2, w + 0.03, 0.025], [0, -w / 2, w + 0.03, 0.025], [w / 2, 0, 0.025, w + 0.03], [-w / 2, 0, 0.025, w + 0.03]]) thin.push(add(new THREE.BoxGeometry(sx, 0.025, sz), iron, dx, y, dz)); };
  frameRing(wB, y0); frameRing(wT, y0 + H);
  const tilt = Math.atan2((wT - wB) / 2, H);
  for (const [sx, sz] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) {   // trụ góc nối đúng góc dưới (wB) với góc trên (wT)
    const a = new THREE.Vector3(sx * wB / 2, y0, sz * wB / 2), b = new THREE.Vector3(sx * wT / 2, y0 + H, sz * wT / 2), d = b.clone().sub(a);
    const p = add(new THREE.BoxGeometry(0.018, d.length() + 0.02, 0.018), iron, (a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2);
    p.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); thin.push(p);
  }
  const glassM = mat('glass', '#ffcf86'), panes = [];
  for (let k = 0; k < 4; k++) {   // kính hình thang, nghiêng theo khung
    const shape = new THREE.Shape([new THREE.Vector2(-wB / 2, 0), new THREE.Vector2(wB / 2, 0), new THREE.Vector2(wT / 2, H), new THREE.Vector2(-wT / 2, H)]);
    const geo = new THREE.ShapeGeometry(shape); geo.rotateX(tilt);
    const pane = new THREE.Mesh(geo, glassM); const a = k * Math.PI / 2; pane.rotation.y = a;
    pane.position.set(Math.sin(a) * wB / 2, y0, Math.cos(a) * wB / 2); g.add(pane); panes.push(pane);
  }
  // nắp chóp có vành nhô, ống thông hơi có mũ, quả chóp
  add(new THREE.BoxGeometry(wT + 0.1, 0.03, wT + 0.1), iron, 0, y0 + H + 0.03, 0);
  add(new THREE.ConeGeometry(0.37, 0.2, 4, 1), iron, 0, y0 + H + 0.145, 0, Math.PI / 4);
  cyl(0.04, 0.04, 0.08, iron2, y0 + H + 0.28, 12); add(new THREE.ConeGeometry(0.075, 0.05, 12), iron, 0, y0 + H + 0.345, 0);
  add(new THREE.SphereGeometry(0.022, 10, 8), iron, 0, y0 + H + 0.39, 0);
  // bầu đốt + mạng đèn (lửa)
  cyl(0.025, 0.03, 0.06, brass, y0 + 0.05, 12);
  const flame = new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 8), mat('flame', '#fff0c8')); flame.scale.set(0.8, 1.7, 0.8); flame.position.y = y0 + 0.16; g.add(flame);
  // Thanh mảnh của lồng (trụ góc, vành) KHÔNG đổ bóng: mạng đèn thật rộng vài cm + kính mờ làm bóng chúng tan gần hết; để đổ bóng thì
  // tạo các dải nêm tối lớn trên tường (đo ở clip đi bộ A2+). Nắp và đế vẫn đổ bóng (chắn sáng lên/xuống thật, như nắp đèn lồng 5A).
  // A2+ (đo ở clip đi bộ): với 3 mẫu jitter, nắp/đế/khung đổ bóng thành các khối nêm có bậc trên tường. Xấp xỉ: MỌI phần của lồng
  // (cao hơn đáy lồng) không đổ bóng; chỉ cột và bệ đổ bóng. Mất vùng tối mềm phía trên nắp — ghi trong bible/props/gas-lamp.md.
  g.traverse((o) => { if (o.isMesh) { o.castShadow = o !== flame && !panes.includes(o) && !thin.includes(o) && o.position.y < cageY - 0.02; o.receiveShadow = true; } });
  g.userData = { flame, glassY: y0 + H / 2, height, parts: { panes, valve, lever, armY } };
  return g;
}

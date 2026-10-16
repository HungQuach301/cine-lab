// K2V tl · V5b-2a · phần tử 3D cho ngữ pháp máy (campath.js): dải màu hai bên RANH GIỚI thật (boundary trace) và vật thể chuyển động A-lite (follow-object).
//  boundaryRibbons: hai dải trên mặt đất dọc polyline ranh giới (lines.json "border", OSM admin_level=2), mỗi bên một màu theo SỐ (setValues(a, b), 0..1)
//   — thang tuần tự CHUNG cho hai bên (nhạt → đậm), để so được bằng mắt; không phải nội dung hình học (mặt nạ = nền).
//  makeMover: xe kiểu thập niên 1940 (hình khối, không mô phỏng mẫu cụ thể — như hàng xe A-lite ở heroes.js) chạy dọc polyline theo quãng đường s(t).
import { THREE, maskify } from './core.js';
import { lineAt } from './campath.js';

const RAMP = ['#efe6cf', '#e9b872', '#d97a3c', '#b8402a'];   // nhạt → đậm (thang tuần tự chung)
function rampColor(v) { v = Math.max(0, Math.min(1, v)) * (RAMP.length - 1); const i = Math.min(RAMP.length - 2, Math.floor(v)); return new THREE.Color(RAMP[i]).lerp(new THREE.Color(RAMP[i + 1]), v - i); }
export function boundaryRibbons(line, hAt, U, { width = 70, gap = 3, lift = 1.2 } = {}) {
  const group = new THREE.Group(), mats = [];
  for (const side of [1, -1]) {
    const P = [], I = [];
    for (let i = 0; i < line.length; i++) { const a = line[Math.max(0, i - 1)], b = line[Math.min(line.length - 1, i + 1)], d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1, nn = [-d[1] / l, d[0] / l];
      for (const o of [gap, gap + width]) { const e = line[i][0] + nn[0] * o * side, n = line[i][1] + nn[1] * o * side; P.push(e, Math.max(hAt(e, n), 0.5) + lift, -n); } }
    for (let i = 0; i < line.length - 1; i++) { const k = i * 2; I.push(k, k + 2, k + 1, k + 1, k + 2, k + 3); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setIndex(I);
    const m = new THREE.MeshBasicMaterial({ color: RAMP[0], transparent: true, opacity: 0.0, depthWrite: false, side: THREE.DoubleSide, fog: false, polygonOffset: true, polygonOffsetFactor: -6, polygonOffsetUnits: -6 });
    maskify(m, U, 0); mats.push(m); const mesh = new THREE.Mesh(g, m); mesh.renderOrder = 2; group.add(mesh);
  }
  group.visible = false;
  // side +1 = bên trái theo hướng polyline (E tăng → phía BẮC = Tây Ban Nha), −1 = phía NAM (Gibraltar)
  return { group, setValues(a, b, op = 0.55) { mats[0].color.copy(rampColor(a)); mats[1].color.copy(rampColor(b)); mats[0].opacity = mats[1].opacity = op; group.visible = op > 0.01; } };
}
export function makeMover(line, hAt, { kind = 'car', color = 0x2b3a2f } = {}) {
  const M = (c) => new THREE.MeshLambertMaterial({ color: c }), grp = new THREE.Group(), add = (geo, mat, x, y, z) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; grp.add(o); };
  const L = kind === 'bus' ? 9.0 : 4.3, W = kind === 'bus' ? 2.4 : 1.7, c = M(color), gl = M(0x31414f), blk = M(0x15171a);
  if (kind === 'bus') { add(new THREE.BoxGeometry(L, 2.3, W), M(0xb8392e), 0, 1.45, 0); add(new THREE.BoxGeometry(L * 0.9, 0.5, W + 0.03), gl, 0, 1.95, 0); }
  else { add(new THREE.BoxGeometry(L, 0.75, W), c, 0, 0.75, 0); add(new THREE.BoxGeometry(L * 0.48, 0.65, W * 0.9), c, -0.25, 1.45, 0); add(new THREE.BoxGeometry(L * 0.46, 0.45, W * 0.92), gl, -0.25, 1.45, 0); add(new THREE.BoxGeometry(L * 0.22, 0.5, W * 1.08), c, L * 0.34, 0.7, 0); }
  for (const x of [-L * 0.32, L * 0.32]) for (const z of [-W / 2, W / 2]) add(new THREE.BoxGeometry(0.7, 0.7, 0.25), blk, x, 0.35, z);
  grp.visible = false;
  // đặt xe tại quãng s (m) dọc polyline, chạy theo chiều dir (+1 / −1), lệch làn lane m; trả {p:[E, y, N], dir:[dE, dN]} cho preset follow
  const at = (s, dir = 1, lane = 0) => { const [e, n] = lineAt(line, s), [e2, n2] = lineAt(line, s + dir * 2), d = [e2 - e, n2 - n], l = Math.hypot(...d) || 1, nn = [-d[1] / l, d[0] / l];
    const E = e + nn[0] * lane, N = n + nn[1] * lane; return { p: [E, Math.max(hAt(E, N), 3.0) + 0.45, N], dir: [d[0] / l, d[1] / l] }; };
  return { group: grp, at, place(o) { grp.position.set(o.p[0], o.p[1], -o.p[2]); grp.rotation.y = Math.atan2(o.dir[1], o.dir[0]); grp.visible = true; } };
}

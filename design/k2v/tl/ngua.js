// V7C (việc 2d) · NGỰA KỴ BINH ở trại vây hãm 1779: hàng cọc buộc ngựa cạnh dãy trại.
//  Số: S048 (Drinkwater 1786 — đầu 10/1779 quân TBN gồm 16 tiểu đoàn bộ binh và "12 squadrons of horse"): 12 đội × ≈ 120 ngựa ≈ 1 440 (cỡ đội ≈ 120: bậc 5);
//  vị trí hàng ngựa: bậc 5 (cạnh dãy trại có nguồn Faden 1783); hình ngựa: khối giản lược (bậc 4–5). Hiện theo cửa sổ năm của dãy trại (win(Y, w)).
//  horseLines([{ at: [E, N], heading (độ), n, w: {on, full, off0, off1} }], ctx)
import { rng } from './core.js';
import { win } from './tl7.js';

export function horseLines(specs, ctx) {
  const { THREE, terr } = ctx, R = rng(1779), group = new THREE.Group(); group.name = 'horses';
  const box = (w, h, d, x, y, z, rz = 0) => new THREE.BoxGeometry(w, h, d).rotateZ(rz).translate(x, y, z);
  const merge = (gs) => { const P = [], Nn = []; for (const g0 of gs) { const g = g0.toNonIndexed(); P.push(...g.attributes.position.array); Nn.push(...g.attributes.normal.array); }   // gộp khối (không dùng BufferGeometryUtils: nó import 'three' trần)
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(Nn, 3)); return g; };
  const geo = merge([box(1.7, 0.72, 0.55, 0, 1.25, 0), box(0.85, 0.32, 0.3, 1.05, 1.62, 0, 0.9), box(0.5, 0.26, 0.24, 1.42, 1.9, 0, -0.3),
    box(0.14, 0.95, 0.14, 0.65, 0.48, 0.18), box(0.14, 0.95, 0.14, 0.65, 0.48, -0.18), box(0.14, 0.95, 0.14, -0.65, 0.48, 0.18), box(0.14, 0.95, 0.14, -0.65, 0.48, -0.18), box(0.1, 0.55, 0.12, -0.92, 1.1, 0, -0.5)]);
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff }); ctx.maskify(mat, ctx.U, 1);
  const COL = [[0.36, 0.22, 0.13], [0.24, 0.15, 0.1], [0.45, 0.3, 0.18], [0.12, 0.1, 0.09], [0.55, 0.5, 0.44]];
  const lines = [];
  function horses() {
    for (const sp of specs) { const n = sp.n || 120, hd = (sp.heading || 0) * Math.PI / 180, dx = Math.cos(hd), dn = Math.sin(hd), im = new THREE.InstancedMesh(geo, mat, n), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), Y = new THREE.Vector3(0, 1, 0), c = new THREE.Color(), P = [];
      for (let i = 0; i < n; i++) { const row = i % 2, k = Math.floor(i / 2), s = (k - n / 4) * 1.35 + (R() - 0.5) * 0.3, o = row ? 2.2 : -2.2, e = sp.at[0] + dx * s - dn * o, nn = sp.at[1] + dn * s + dx * o;
        P.push({ e, n: nn, a: -hd + (row ? Math.PI / 2 : -Math.PI / 2) + (R() - 0.5) * 0.35, k: R() }); c.setRGB(...COL[Math.floor(R() * COL.length)]); im.setColorAt(i, c); }
      im.castShadow = im.receiveShadow = true; group.add(im); lines.push({ sp, im, P, m4, q, Y }); } }
  horses();
  return { group, n: specs.reduce((a, s) => a + (s.n || 120), 0), update(Yr) { for (const L of lines) { const k = win(Yr, L.sp.w); L.im.visible = k > 0.01;
    L.P.forEach((p, i) => { const on = p.k < k; L.m4.compose(new THREE.Vector3(p.e, Math.max(terr.hAt(p.e, p.n), 0.3), -p.n), L.q.setFromAxisAngle(L.Y, p.a), new THREE.Vector3(on ? 1 : 0, on ? 1 : 0, on ? 1 : 0)); L.im.setMatrixAt(i, L.m4); });
    L.im.instanceMatrix.needsUpdate = true; } } };
}

// Test hình học toà (design/k2v/tl/geom.js): hướng mặt kiểm bằng tích có hướng, không bằng mắt (bài học R&D §6.3 lỗi 0).
import assert from 'node:assert/strict';
import { walls, roof, ccw, signedArea, simplify, isConvex } from '../../../design/k2v/tl/geom.js';
const fan = (r) => r.slice(1, -1).map((_, i) => [0, i + 1, i + 2]);
let n = 0;
const check = (ring, h, label) => {
  const V = []; walls(ring, h, (x, y, z, nx, ny, nz) => V.push([x, y, z, nx, ny, nz]));
  const r = ccw(ring), cx = r.reduce((s, p) => s + p[0], 0) / r.length, cn = r.reduce((s, p) => s + p[1], 0) / r.length;
  for (let i = 0; i < V.length; i += 3) {
    const [a, b, c] = [V[i], V[i + 1], V[i + 2]], u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
    const g = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
    assert.ok(g[0] * a[3] + g[1] * a[4] + g[2] * a[5] > 0, `${label}: tam giác ${i / 3} quấn ngược pháp tuyến`);
    const mx = (a[0] + b[0] + c[0]) / 3, mz = (a[2] + b[2] + c[2]) / 3;   // pháp tuyến hướng RA khỏi tâm (vòng lồi)
    assert.ok((mx - cx) * a[3] + (mz + cn) * a[5] > 0, `${label}: pháp tuyến tường hướng vào trong`); n++;
  }
  const R = []; roof(ring, h, 0, fan, (x, y, z, nx, ny, nz) => R.push([x, y, z, nx, ny, nz]));
  for (let i = 0; i < R.length; i += 3) { const [a, b, c] = [R[i], R[i + 1], R[i + 2]];
    const cr = (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2]); assert.ok(cr > 0, `${label}: mái phẳng quấn xuống`); n++; }
  const P = []; roof(ring, h, 2.5, fan, (x, y, z, nx, ny, nz) => P.push([x, y, z, nx, ny, nz]));
  for (let i = 0; i < P.length; i += 3) { const [a, b, c] = [P[i], P[i + 1], P[i + 2]], u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
    const g = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]; assert.ok(g[1] > 0 && g[0] * a[3] + g[1] * a[4] + g[2] * a[5] > 0, `${label}: mái hông quấn sai`); n++; }
};
const sq = [[0, 0], [10, 0], [10, 8], [0, 8]];
check(sq, 9, 'vuông CCW'); check(sq.slice().reverse(), 9, 'vuông CW'); check([[0, 0], [12, 2], [9, 11], [-2, 7]], 6, 'tứ giác lệch');
assert.equal(Math.round(signedArea(ccw(sq.slice().reverse()))), 80);
assert.equal(isConvex(sq), true); assert.equal(isConvex([[0, 0], [10, 0], [5, 2], [10, 8], [0, 8]]), false);
assert.equal(simplify([[0, 0], [5, 0.05], [10, 0], [10, 8], [0, 8]], 0.5).length, 4);
console.log(`test_geom OK (${n} tam giác kiểm hướng)`);

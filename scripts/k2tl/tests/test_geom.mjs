// Test hình học toà (design/k2v/tl/geom.js): hướng mặt kiểm bằng tích có hướng, không bằng mắt (bài học R&D §6.3 lỗi 0).
import assert from 'node:assert/strict';
import { walls, roof, ccw, signedArea, simplify, isConvex, pitched, rectOf, boxAt, parcels, clipHalf } from '../../../design/k2v/tl/geom.js';
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
// V5b-1b: mái hai mái / mái hông có nóc / hộp: pháp tuyến khai báo = pháp tuyến hình học (tích có hướng), mái hướng lên, mặt hộp hướng ra khỏi tâm
const geoN = (V, label, up, ctr) => { for (let i = 0; i < V.length; i += 3) { const [a, b, c] = [V[i], V[i + 1], V[i + 2]], u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
  const g = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]; assert.ok(g[0] * a[3] + g[1] * a[4] + g[2] * a[5] > 0, `${label}: tam giác ${i / 3} quấn ngược pháp tuyến khai báo`);
  if (up && a[6] < 0) assert.ok(a[4] > -1e-6, `${label}: mặt mái hướng xuống`);
  if (ctr) { const m = [(a[0] + b[0] + c[0]) / 3 - ctr[0], (a[1] + b[1] + c[1]) / 3 - ctr[1], (a[2] + b[2] + c[2]) / 3 - ctr[2]]; assert.ok(m[0] * a[3] + m[1] * a[4] + m[2] * a[5] > 0, `${label}: mặt hộp hướng vào tâm`); } n++; } };
for (const [ring, lab] of [[sq, 'chữ nhật'], [sq.slice().reverse(), 'chữ nhật CW'], [[[0, 0], [10, 3], [7, 13], [-3, 10]], 'chữ nhật xoay']]) for (const k of ['gable', 'hipr']) {
  const V = []; assert.equal(pitched(ring, 9, 2.5, k, (x, y, z, nx, ny, nz, u) => V.push([x, y, z, nx, ny, nz, u])), k); geoN(V, `${lab} ${k}`, true); }
assert.equal(rectOf([[0, 0], [10, 0], [12, 8], [0, 8]]), null);   // không vuông góc → không dựng mái dốc chữ nhật
{ const V = []; boxAt(5, 2, 7, 3, 2, 4, 0.6, (x, y, z, nx, ny, nz, u) => V.push([x, y, z, nx, ny, nz, u])); geoN(V, 'hộp', false, [5, 4, -7]); assert.equal(V.length, 30); }
{ const big = [[0, 0], [40, 0], [40, 25], [0, 25]], P = parcels(big, (() => { let k = 0; return () => ((k = (k * 9301 + 49297) % 233280) / 233280); })());
  const A = P.reduce((s, r) => s + Math.abs(signedArea(r)), 0); assert.ok(P.length >= 4, 'chia lô quá ít'); assert.ok(Math.abs(A - 1000) < 1, `tổng diện tích lô ${A} ≠ 1000`); }
assert.equal(clipHalf(sq, 1, 0, 5).length, 4);
console.log(`test_geom OK (${n} tam giác kiểm hướng)`);

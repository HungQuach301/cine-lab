// Test máy quay (design/k2v/tl/campath.js): spline đi qua mốc, bay dọc tuyến lệch ≤ 15 m, đo đứng yên, tỉ lệ reveal.
import assert from 'node:assert/strict';
import { alongLine, makeCamPath, camLog, distToLine, lineLen } from '../../../design/k2v/tl/campath.js';
const L = [[0, 0], [10, 300], [-20, 600], [5, 900]];
assert.ok(Math.abs(lineLen(L) - (Math.hypot(10, 300) + Math.hypot(30, 300) + Math.hypot(25, 300))) < 1e-6);
assert.ok(distToLine(L, 10, 300) < 1e-9 && Math.abs(distToLine(L, -50, -10) - Math.hypot(50, 10)) < 1e-6);
const K = [{ t: 0, p: [-500, 400, -300], l: [0, 0, 0] }, ...alongLine(L, { s0: 50, s1: 850, t0: 2, t1: 6, h: 60 }), { t: 8, p: [400, 300, 1200], l: [0, 0, 600] }];
const P = makeCamPath(K);
for (const k of K) { const c = P.at(k.t); assert.ok(Math.hypot(c.p[0] - k.p[0], c.p[1] - k.p[1], c.p[2] - k.p[2]) < 1e-6, 'spline phải qua mốc'); }
const log = camLog(P, 8 * 24, 24, (t) => 1900 + t, { line: L, focus: { a: [0, 0, 0] } });
const dev = log.frames.filter((r) => r.dev_m !== undefined);
assert.ok(dev.length >= 3 * 24, 'bay dọc tuyến ≥ 3 s'); assert.ok(Math.max(...dev.map((r) => r.dev_m)) <= 15, 'lệch tim tuyến ≤ 15 m');
assert.ok(log.max_still_s < 6, 'máy không đứng yên > 6 s');
const still = camLog(makeCamPath([{ t: 0, p: [0, 10, 0], l: [0, 0, 100] }, { t: 8, p: [0, 10, 0], l: [0, 0, 100] }]), 192, 24, () => 0);
assert.ok(still.max_still_s > 6, 'phải phát hiện máy đứng yên');
console.log(`test_campath OK (lệch tuyến tối đa ${Math.max(...dev.map((r) => r.dev_m)).toFixed(2)} m, ${dev.length} khung trên tuyến)`);

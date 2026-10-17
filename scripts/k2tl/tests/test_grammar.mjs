// V5b-2a · test NGỮ PHÁP MÁY (design/k2v/tl/campath.js, Node thuần, địa hình phẳng): liên hoàn + 6 preset — vai bắt buộc, giới hạn KK1/HH2
// (năm ≤ 10 năm/s, tốc độ góc ≤ 90 °/s, độ cao bay tuyến theo loại tuyến, orbit 4–6 s, năm dừng 1,5–2 s), SPP theo pha, hình học riêng từng preset.
import assert from 'node:assert/strict';
import { lienHoan, pushIn, boundaryTrace, follow, lateral, topDownRise, vertigo, grammar, grammarLog, sppOf, ALT_MAX, LIMITS, distToLine } from '../../../design/k2v/tl/campath.js';
const fps = 24, track = (K) => (t) => { if (t <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (t <= K[i][0]) { const [t0, a] = K[i - 1], [t1, b] = K[i]; return a + (b - a) * (t - t0) / (t1 - t0); } return K[K.length - 1][1]; };
const road = [[-200, -900], [-150, -500], [-60, -200], [0, 0], [30, 400]];
// vai sai / bay quá cao → lỗi
assert.throws(() => pushIn({ vai: 'trang-tri', from: [0, 100, 0], to: [0, 50, 100], look: [0, 0, 300], t0: 0, t1: 3, fov: 30 }), /vai/);
assert.throws(() => lienHoan({ vai: 'buoc-ngoat', route: { line: road, type: 'pho', nguon: 'x' }, fly: { s0: 0, s1: 200, t: [0, 3], h: 150 }, ramp: { t1: 4 }, orbit: { c: [0, 0, 0], r: 100, h: 40, a0: -90, a1: -200, t1: 9, fov: 32 }, crane: { t1: 10, h: 200 }, reveal: { t1: 13, p: [-2000, 1500, 0], l: [0, 0, 300], fov: 33 } }), /> 120/);
assert.deepEqual([sppOf('fly'), sppOf('ramp'), sppOf('orbit'), sppOf('pin'), sppOf('crane'), sppOf('reveal')], [1, 1, 4, 4, 2, 2]);
// 1) liên hoàn
const lh = lienHoan({ vai: 'buoc-ngoat', route: { line: road, type: 'eo_dat', nguon: 'test' }, fly: { s0: 80, s1: 320, t: [1, 4], h: [100, 95], target: [100, 0, 1500], fov: 26 },
  ramp: { t1: 4.8 }, orbit: { c: [0, 2, 0], r: 100, h: 40, look: 12, a0: -92, a1: -248, t1: 9.8, fov: 32, heroId: 'x' }, crane: { t1: 11, h: 240, l: [-60, 30, -500] },
  reveal: { keys: [{ t: 13, p: [-700, 620, 420], l: [-80, 0, -60], fov: 31 }, { t: 15, p: [-2600, 2080, 60], l: [-150, 0, 350], fov: 33 }] }, pin: [5.6, 7.4] });
const yr = track([[0, 1880], [1, 1890], [4, 1919], [4.8, 1927], [5.6, 1935], [7.4, 1935], [9.8, 1958], [11, 1970], [15, 2010], [16, 2010]]);
const G = grammar([lh], [{ t: 0, p: [-400, 300, -1400], l: [-100, 50, -800], fov: 34 }, { t: 16, p: [-2700, 2150, 50], l: [-150, 0, 355], fov: 33 }]);
const L = grammarLog(G, 16 * fps, fps, yr, {}), S = L.shots[0];
assert.equal(S.preset, 'lien-hoan'); assert.equal(S.vai, 'buoc-ngoat');
assert.ok(S.fly_s >= 3 && S.fly_dev_max <= 15, `bay tuyến ${S.fly_s} s lệch ${S.fly_dev_max} m`); assert.ok(S.fly_agl_max <= ALT_MAX.eo_dat && S.fly_agl_max <= 120, `cao ${S.fly_agl_max}`);
assert.ok(S.orbit_s >= 4 && S.orbit_s <= 6); assert.ok(S.pin_s >= 1.5 && S.pin_s <= 2.0, `năm dừng ${S.pin_s}`);
assert.ok(S.year_rate_max <= LIMITS.year_rate + 1e-9, `năm ${S.year_rate_max}/s`); assert.ok(S.ang_rate_max <= LIMITS.ang_rate, `góc ${S.ang_rate_max} °/s`);
assert.deepEqual(Object.values(S.ok).every(Boolean), true);
const at = (t) => L.frames[Math.round(t * fps)];
assert.equal(at(2).spp, 1); assert.equal(at(6.5).phase, 'pin'); assert.equal(at(6.5).spp, 4); assert.equal(at(9).spp, 4); assert.equal(at(10.5).spp, 2); assert.equal(at(0.5).spp, null);
const orb = L.frames.filter((r) => (r.phase === 'orbit' && r.t > 4.8 + 0.25) || r.phase === 'pin');   // 0,25 s đầu orbit: chuyển tiếp từ ramp (spline nối) assert.ok(Math.max(...orb.map((r) => Math.abs(r.d_x ?? 0))) === 0);
for (const r of orb) assert.ok(Math.abs(Math.hypot(r.pos[0], r.pos[2]) - 100) < 3, `orbit bán kính ${Math.hypot(r.pos[0], r.pos[2])} khung ${r.f} ${r.t}`);
assert.ok(at(15).pos[1] / at(10).pos[1] > 5, 'reveal: lên cao/lùi xa');
// 2) push-in giữ hơi: tiến chậm dần, pha "hero" cuối không đứng yên nhưng chậm
const pi = pushIn({ vai: 'co-che', from: [-500, 250, -400], to: [-150, 100, -120], look: [0, 30, 0], t0: 0, t1: 4.5, hold: 1.3, fov: 34, fov1: 30 });
const Lp = grammarLog(grammar([pi]), 108, fps, () => 1900, {}); const vEnd = Lp.frames.slice(-20).map((r) => r.v), vStart = Lp.frames.slice(2, 20).map((r) => r.v);
assert.ok(Math.max(...vEnd) < 0.2 * Math.max(...vStart) && Math.min(...vEnd) > 0, 'giữ hơi: chậm hẳn nhưng không đứng yên'); assert.deepEqual(Lp.shots[0].spp.sort(), [2, 4]);
// 3) boundary trace: trên ranh giới (≤ 15 m), dưới trần độ cao
const border = [[-300, 380], [-100, 360], [100, 390], [300, 370], [450, 400]];
const bt = boundaryTrace({ vai: 'he-qua', line: border, nguon: 'test', s0: 40, s1: 700, t0: 0, t1: 4.5, h: 95, look: 320, dip: 95 });
const Lb = grammarLog(grammar([bt]), 108, fps, track([[0, 1960], [4.5, 2004]]), {}); assert.ok(Lb.shots[0].fly_dev_max <= 15 && Lb.shots[0].ok.alt && Lb.shots[0].ok.year_rate);
// 4) follow: khoảng cách máy–vật không đổi
const obj = (t) => ({ p: [0, 4, 300 - 11 * t], dir: [0, -1] }), fo = follow({ vai: 'co-che', objAt: obj, t0: 0, t1: 4.5, back: 26, up: 11, side: 6 });
const Lf = grammarLog(grammar([fo]), 108, fps, () => 1941, {}); for (const r of Lf.frames.slice(1, -1)) { const o = obj(r.t).p; assert.ok(Math.abs(Math.hypot(r.pos[0] - o[0], r.pos[1] - o[1], r.pos[2] - o[2]) - Math.hypot(26, 11, 6)) < 0.5, 'follow: giữ khoảng cách'); }
// 5) lateral: máy trượt ngang (vuông góc trục nhìn), tốc độ góc nhỏ
const la = lateral({ vai: 'he-qua', c: [170, 10, 1150], yaw: 72, dist: 720, len: 420, h: 110, t0: 0, t1: 4.5 }), Ll = grammarLog(grammar([la]), 108, fps, () => 2000, {});
assert.ok(Ll.shots[0].ang_rate_max < 10); { const a = Ll.frames[1].pos, b = Ll.frames[100].pos, f = [Math.cos(72 * Math.PI / 180), Math.sin(72 * Math.PI / 180)], m = [b[0] - a[0], b[2] - a[2]];
  assert.ok(Math.abs(m[0] * f[0] + m[1] * f[1]) / Math.hypot(...m) < 0.02, 'lateral: chuyển động vuông góc trục nhìn'); }
// 6) top-down: nhìn gần thẳng đứng, bay lên
const td = topDownRise({ vai: 'buoc-ngoat', c: [0, 0, 0], h0: 260, h1: 1300, t0: 0, t1: 4.5 }), Lt = grammarLog(grammar([td]), 108, fps, () => 1940, {});
for (const r of [Lt.frames[5], Lt.frames[100]]) { const d = r.look.map((v, i) => v - r.pos[i]); assert.ok(Math.atan2(-d[1], Math.hypot(d[0], d[2])) * 180 / Math.PI > 89, 'top-down: nhìn thẳng xuống'); }
assert.ok(Lt.frames[107].agl / Lt.frames[0].agl > 4.5);
// 7) vertigo: bề rộng chủ thể giữ nguyên (≤ 1 %) trong khi fov đổi mạnh
const vg = vertigo({ vai: 'buoc-ngoat', c: [0, 14, 0], yaw: 35, pitch: 14, d0: 230, d1: 560, w: 85, t0: 0, t1: 4.5 }), Lv = grammarLog(grammar([vg]), 108, fps, () => 1990, {});
assert.ok(Lv.shots[0].vertigo_w_dev_pct < 1, `vertigo lệch ${Lv.shots[0].vertigo_w_dev_pct} %`); assert.ok(Lv.shots[0].fov[0] / Lv.shots[0].fov[1] > 2);
// cắt giữa các cú (cuộn minh hoạ): spline riêng, không lấn sang cú sau
const Gc = grammar([pi, Object.assign({}, la, { t: [4.5 + 1 / fps, 9], keys: la.keys.map((k) => Object.assign({}, k, { t: k.t + 4.5 + 1 / fps })) })], [], { cuts: true });
assert.ok(Math.abs(Gc.path.at(4.4).p[0] - grammar([pi]).path.at(4.4).p[0]) < 1e-6, 'cắt: cú trước giữ nguyên spline');
console.log(`test_grammar OK (liên hoàn: bay ${S.fly_s} s lệch ${S.fly_dev_max} m cao ${S.fly_agl_max} m · orbit ${S.orbit_s} s · năm dừng ${S.pin_s} s · ${S.year_rate_max} năm/s · ${S.ang_rate_max} °/s; 6 preset ĐẠT)`);

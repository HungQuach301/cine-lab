// V5b-2b · test thuần Node cho phần T3: M6 sun.js (lịch Gregory/Julius, giờ địa phương, vị trí mặt trời), M3 đội hình hàng, bộ ghi lớp chữ record.js.
import assert from 'node:assert/strict';
import { jdOf, jdJulian, calOf, sunPos, jdLocal, clockLabel } from '../../../design/k2v/tl/sun.js';
import { makeRecorder } from '../../../design/k2v/tl/record.js';
// JD chuẩn: 2000-01-01 12:00 UTC = 2451545.0; lịch Julius đổi Gregory 4/10/1582 (J) → 15/10/1582 (G) liền ngày
assert.equal(jdOf(2000, 1, 1, 12), 2451545.0);
assert.equal(jdJulian(1582, 10, 4, 12) + 1, jdOf(1582, 10, 15, 12));
assert.deepEqual(calOf(jdOf(1782, 9, 13, 12), true), { y: 1782, mo: 9, d: 13 });
assert.deepEqual(calOf(jdOf(1782, 9, 13, 12), false), { y: 1782, mo: 9, d: 2 });   // chênh 11 ngày ở thế kỷ 18
// hai lịch 1704 (TIEN-KY-VAY-HAM §5 M6): N.S. 4 Aug 1704 = O.S. 24 Jul
assert.equal(clockLabel(jdLocal(1704, 8, 4, 12), { dual: true }).sub, 'O.S. 24 Jul · N.S. 4 Aug 1704');
assert.equal(clockLabel(jdLocal(1782, 9, 13, 9.75)).s, '13 Sep 1782 · 09:45');
// mặt trời: trưa thật ở Greenwich hạ chí 2026 → cao ≈ 90 − 51,48 + 23,44 = 61,96°, phương vị ≈ 180°
const g = sunPos(jdOf(2026, 6, 21, 12) + 1.8 / 1440, 51.48, 0); assert.ok(Math.abs(g.el - 61.96) < 0.1 && Math.abs(g.az - 180) < 1, JSON.stringify(g));
// Gibraltar 13/9/1782 09:45 giờ địa phương: buổi sáng, hướng đông-nam, cao 40–50°
const p = sunPos(jdLocal(1782, 9, 13, 9.75)); assert.ok(p.az > 110 && p.az < 140 && p.el > 40 && p.el < 50, JSON.stringify(p));
// record.js: cùng API text.js; độ đục theo cửa sổ; neo chuẩn hoá 0..1; thẻ không neo → dải dưới (anchor null)
const R = makeRecorder(1920, 1080); R.begin(); R.chrome(1, { s: '13 Sep 1782 · 09:45' }, 1, null, null, null); R.card(1, [0, 3], 'T', 'S', [960, 540]); R.card(1, [0, 3], 'T2', 'S2', null);
R.tag(1, [0, 3], 'tag', null); R.where(1, [0, 3], 'Bay of Gibraltar'); R.ghostSrc(5, [0, 3], 'x');
const D = R.data(); assert.equal(D.chrome.clock.s, '13 Sep 1782 · 09:45'); assert.deepEqual(D.cards[0].anchor, [0.5, 0.5]); assert.equal(D.cards[1].anchor, null);
assert.equal(D.tags.length, 0); assert.equal(D.where.s, 'Bay of Gibraltar'); assert.equal(D.ghost_src, undefined);
console.log(`test_t3 OK (sun 1782-09-13 09:45: cao ${p.el.toFixed(1)}°, phương vị ${p.az.toFixed(1)}° · lịch O.S./N.S. · record.js)`);

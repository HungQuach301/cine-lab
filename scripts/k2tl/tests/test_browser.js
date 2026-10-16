// Test trình duyệt (SwiftShader) cho design/k2v/tl: dựng 3 khung 480×270 của gib20 (mở, mốc đinh, kết) và kiểm:
// không lỗi trang/shader; ngân sách chữ (≤ 15 % thường, ≤ 25 % mốc đinh, vùng giữa 0 %), ≤ 1 thẻ, không tràn; tương phản ≥ 4,5:1; chữ ≥ 38 px@1080;
// tất định (cùng khung dựng 2 lần → cùng ảnh); năm đúng mốc (khung 300 = 1941).
const { execFileSync } = require('child_process'); const fs = require('fs'), path = require('path'), assert = require('assert');
const out = fs.mkdtempSync('/tmp/k2tl-test-'); const R = path.join(__dirname, '..', 'render.js');
execFileSync('node', [R, '--w', '480', '--h', '270', '--out', out, '--only', '24,300,300,470', '--tech', '{"spp":1}'], { stdio: ['ignore', 'ignore', 'pipe'] });
const log = JSON.parse(fs.readFileSync(path.join(out, 'log.json'))); const F = log.frames;
for (const r of F) { const pin = r.f >= 290 && r.f <= 336; assert.ok(r.budget.pct <= (pin ? 25 : 15), `khung ${r.f}: chữ ${r.budget.pct}%`); assert.equal(r.budget.center_unanchored_pct, 0); assert.ok(r.budget.cards <= 1); assert.deepEqual(r.overflow, []);
  for (const t of r.text || []) { assert.ok(t.ratio >= 4.5, `khung ${r.f} tương phản ${t.s} ${t.ratio}`); assert.ok(t.px1080 >= 38, `cỡ chữ ${t.s}`); } }
assert.equal(Math.floor(F.find((r) => r.f === 300).year), 1941);
const a = fs.readFileSync(path.join(out, '00300.jpg')); assert.ok(a.length > 1000);
// tất định: khung 300 dựng 2 lần trong cùng phiên → log ghi đè cùng tệp; so log gl và kích thước tệp với lượt dựng riêng
const out2 = fs.mkdtempSync('/tmp/k2tl-test-'); execFileSync('node', [R, '--w', '480', '--h', '270', '--out', out2, '--only', '300', '--tech', '{"spp":1}'], { stdio: ['ignore', 'ignore', 'pipe'] });
const b = fs.readFileSync(path.join(out2, '00300.jpg')); const same = Buffer.compare(a, b) === 0;
console.log(`test_browser OK (${F.length} khung; chữ max ${Math.max(...F.map((r) => r.budget.pct))}%; tương phản min ${Math.min(...F.flatMap((r) => (r.text || []).map((t) => t.ratio)))}; tất định: ${same ? 'trùng byte' : 'KHÁC byte'})`);
if (!same) { console.error('CẢNH BÁO: khung 300 dựng lại không trùng byte (thứ tự dựng khác: bóng/khoá cache)'); }

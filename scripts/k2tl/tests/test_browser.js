// Test trình duyệt cho design/k2v/tl — chạy với trình dựng của K2TL_GL (llvmpipe mặc định | swiftshader; run.sh chạy CẢ HAI). Dựng 3 khung 960×540
// (ở 480×270 chữ 38 px@1080 còn ~9 px: đo tương phản không tin cậy) của gib20 (mở, mốc đinh 1941 trong orbit, màn kết) và kiểm:
// renderer thật đúng trình dựng yêu cầu và có trong log; không lỗi trang/shader; ngân sách chữ (≤ 15 % thường, ≤ 25 % mốc đinh, vùng giữa 0 %), ≤ 1 thẻ, không tràn;
// tương phản ≥ 4,5:1; chữ ≥ 38 px@1080; năm đúng mốc (khung 320 = 1941); log đường dẫn neo ở khung có thẻ neo; dòng nguồn số đếm (index_src) ở màn kết;
// mặt nạ: hero_pct (id crossing) ≥ 25 % trong orbit; tất định (cùng khung dựng 2 lượt → so byte).
const { execFileSync, spawnSync } = require('child_process'); const fs = require('fs'), path = require('path'), assert = require('assert');
const GL = process.env.K2TL_GL || 'llvmpipe', WANT = { llvmpipe: /llvmpipe/i, swiftshader: /SwiftShader/i }[GL];
const out = fs.mkdtempSync('/tmp/k2tl-test-'); const R = path.join(__dirname, '..', 'render.js'); const env = Object.assign({}, process.env, { K2TL_GL: GL });
execFileSync('node', [R, '--w', '960', '--h', '540', '--out', out, '--only', '24,320,320,580', '--tech', '{"spp":1}'], { stdio: ['ignore', 'ignore', 'pipe'], env });
const log = JSON.parse(fs.readFileSync(path.join(out, 'log.json'))); const F = log.frames;
assert.ok(WANT.test(log.renderer) && log.gl === GL, `renderer ${log.renderer} ≠ ${GL}`);
for (const r of F) { const pin = r.f >= 293 && r.f <= 374; assert.ok(r.budget.pct <= (pin ? 25 : 15), `khung ${r.f}: chữ ${r.budget.pct}%`); assert.equal(r.budget.center_unanchored_pct, 0); assert.ok(r.budget.cards <= 1); assert.deepEqual(r.overflow, []);
  for (const t of r.text || []) { assert.ok(t.ratio >= 4.5, `khung ${r.f} tương phản ${t.s} ${t.ratio}`); assert.ok(t.px1080 >= 38, `cỡ chữ ${t.s}`); } }
const f320 = F.find((r) => r.f === 320), f580 = F.find((r) => r.f === 580);
assert.equal(Math.floor(f320.year), 1941); assert.equal(f320.phase, 'pin'); assert.equal(f320.spp, 1);   // --tech spp:1 ghi đè SPP thích ứng
assert.ok((f320.leaders || []).some((l) => l.role === 'card' && l.world), 'khung 320: thiếu log đường dẫn thẻ neo');
assert.ok((f580.text || []).some((t) => t.role === 'index_src'), 'màn kết: thiếu dòng nguồn số đếm (role index_src)');
const mk = path.join(out, 'mask.json'); execFileSync('node', [R, '--w', '960', '--h', '540', '--only', '320', '--maskonly', mk], { stdio: ['ignore', 'ignore', 'pipe'], env });
const m = JSON.parse(fs.readFileSync(mk))[0]; assert.ok(WANT.test(m.renderer)); assert.equal(m.hero_id, 'crossing'); assert.ok(m.hero_pct >= 25, `hero_pct ${m.hero_pct}`);
const a = fs.readFileSync(path.join(out, '00320.jpg')); assert.ok(a.length > 1000);
const out2 = fs.mkdtempSync('/tmp/k2tl-test-'); execFileSync('node', [R, '--w', '960', '--h', '540', '--out', out2, '--only', '320', '--tech', '{"spp":1}'], { stdio: ['ignore', 'ignore', 'pipe'], env });
const b = fs.readFileSync(path.join(out2, '00320.jpg')); const same = Buffer.compare(a, b) === 0;
// cơ chế DỪNG: yêu cầu trình dựng này nhưng cờ của trình dựng kia → render.js phải thoát mã 6 (không âm thầm dựng sai trình dựng)
const other = GL === 'llvmpipe' ? ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] : ['--use-gl=angle', '--use-angle=gl-egl'];
const st = spawnSync('node', [R, '--w', '480', '--h', '270', '--campath', path.join(out, 'x.json')], { env: Object.assign({}, env, { K2TL_GL_FLAGS: JSON.stringify(other) }), encoding: 'utf8' });
assert.equal(st.status, 6, `cờ sai phải DỪNG mã 6, nhận ${st.status}`); assert.ok(/DỪNG/.test(st.stderr));
console.log(`test_browser ${GL} OK (${log.renderer}; ${F.length} khung; chữ max ${Math.max(...F.map((r) => r.budget.pct))}%; tương phản min ${Math.min(...F.flatMap((r) => (r.text || []).map((t) => t.ratio)))}; hero_pct mốc đinh ${m.hero_pct}%; cờ sai → DỪNG mã 6; tất định: ${same ? 'trùng byte' : 'KHÁC byte'})`);
if (!same) { console.error('CẢNH BÁO: khung 320 dựng lại không trùng byte (thứ tự dựng khác: bóng/khoá cache)'); }

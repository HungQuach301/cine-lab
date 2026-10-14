// KÊNH 2 · driver cảnh 3D (bản sao scripts/ll/hero.js + ghi điểm neo màn hình vào <out>/anchors.json). Ghi chuỗi JPG (q 2) để mẫu `plate` của scripts/ll/lib phát làm nền.
//   node scripts/ll/hero.js --hero ep06/printshop --variant a --dur 12.5 --out /var/tmp/cine-out/hero/ep06-printshop-a [--w 1920 --h 1080] [--only 0,120] [--opt '{}'] [--resume]
// Tất định: cùng tham số → cùng khung. Ghi <out>/%05d.jpg + <out>/meta.json (khung, s/khung).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../../design');   // trang: design/ll-hero/k2page.js, hoặc design/k2v/page.js khi cảnh thuộc module hình k2v (map, chart3d, photo)
const CACHE = process.env.K2V_CACHE || '/var/tmp/cine-out/k2v-cache';   // tài sản ngoài git (Blue Marble, ảnh LoC, trang PDF): /cache/<tệp>
const PAGE = fs.existsSync(path.join(ROOT, 'k2v', String(arg('hero', '')).split('/')[0] + '.js')) ? 'k2v' : 'll-hero';
const W = +arg('w', 1920), H = +arg('h', 1080), OUT = path.resolve(arg('out')), DUR = +arg('dur', 6), N = Math.ceil(DUR * 24);
const ONLY = (arg('only', '') || '').split(',').filter(Boolean).map(Number);
// FOOTAGE nguồn ngoài (K2C-T1-06, 13/10/2026): --hero footage/clip, opt {file: '<đường dẫn tệp clip ngoài git>', sha256, ss (giây trong clip), crop?, eq?}  · decimate: true = bỏ khung nhồi 24p→29,97 (chu kỳ 5) trước fps=24 (Q2, PX-36624235)
// → trích khung 24 fps đúng độ dài cảnh bằng ffmpeg (không qua hậu kỳ 3D: giữ màu gốc, không ACES/grain). Kiểm SHA-256 tệp trước khi dùng (QUAN-TRI-RUI-RO §6, luật K Q32a).
if (String(arg('hero', '')).startsWith('footage/')) {
  const o = JSON.parse(arg('opt', '{}')); fs.mkdirSync(OUT, { recursive: true });
  const buf = fs.readFileSync(o.file), sha = require('crypto').createHash('sha256').update(buf).digest('hex');
  if (o.sha256 && sha !== o.sha256) { console.error(`LỖI SHA footage ${o.file}: ${sha} ≠ sổ ${o.sha256}`); process.exit(4); }
  const vf = [o.decimate ? 'decimate=cycle=5' : null, o.crop ? `crop=${o.crop}` : null, `scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos`, `crop=${W}:${H}`, 'fps=24', o.eq ? `eq=${o.eq}` : null].filter(Boolean).join(',');
  const t0 = Date.now(); const r = require('child_process').spawnSync('ffmpeg', ['-nostdin', '-v', 'error', '-y', '-ss', String(o.ss || 0), '-i', o.file, '-t', String(N / 24 + 0.1), '-vf', vf, '-frames:v', String(N), '-q:v', '2', '-start_number', '0', path.join(OUT, '%05d.jpg')]);
  if (r.status) { console.error(String(r.stderr)); process.exit(5); }
  const got = fs.readdirSync(OUT).filter((f) => /^\d{5}\.jpg$/.test(f)).length;
  if (got < N) { console.error(`LỖI footage: clip ngắn hơn cảnh (${got}/${N} khung) — giảm độ dài shot hoặc ss`); process.exit(6); }
  fs.writeFileSync(path.join(OUT, 'anchors.json'), '{}');
  fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify({ hero: arg('hero'), frames: N, dur: DUR, w: W, h: H, spp: 1, footage: { file: path.basename(o.file), sha256: sha, ss: o.ss || 0 }, s_per_frame: +((Date.now() - t0) / 1000 / N).toFixed(3) }));
  console.error(`[hero footage] ${N} khung từ ${path.basename(o.file)} @${o.ss || 0}s`); process.exit(0);
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|VALIDATE_STATUS false/.test(t)) { console.error('[page] LỖI SHADER — dừng (V2 14/10: lỗi biên dịch từng cho ra khung thiếu địa hình mà không báo)', t.slice(0, 600)); process.exit(7); }
    if (!/GPU stall|GL Driver|WebGLRenderer|swiftshader/i.test(t)) console.error('[page]', t); });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname), p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : u.startsWith('/assets/') ? path.join(ROOT, '..', u) : path.join(ROOT, u);   // /assets/: tư liệu tài sản công đã commit (RIGHTS.md)
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pf = path.join(ROOT, `${PAGE}/page-${process.pid}.html`);
  fs.writeFileSync(pf, `<!doctype html><html><body style="margin:0"><script type="module" src="/${PAGE}/${PAGE === 'k2v' ? 'page' : 'k2page'}.js"></script></body></html>`);
  await page.goto(`http://cine.local/${PAGE}/${path.basename(pf)}`); await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 }); fs.unlinkSync(pf);
  const SU = await page.evaluate(async (c) => await window.setup(c), { W, H, hero: arg('hero'), variant: arg('variant', 'a'), dur: DUR, spp: +arg('spp', 1), opt: JSON.parse(arg('opt', '{}')) });
  let frames = ONLY.length ? ONLY : [...Array(N).keys()]; const t0 = Date.now();
  const AF = path.join(OUT, 'anchors.json'); let ANC = {}; try { ANC = JSON.parse(fs.readFileSync(AF, 'utf8')); } catch (e) { ANC = {}; }
  if (process.argv.includes('--resume')) {   /* dựng tiếp sau khi job nền bị ngắt (giới hạn 2 giờ): bỏ khung đã có, dựng lại khung cuối có thể ghi dở */
    const have = frames.filter((f) => { try { return fs.statSync(path.join(OUT, String(f).padStart(5, '0') + '.jpg')).size > 0; } catch { return false; } });
    const keep = new Set(have.slice(0, -1)); frames = frames.filter((f) => !keep.has(f)); console.error(`[hero ${arg('hero')}/${arg('variant', 'a')}] dựng tiếp: giữ ${keep.size} khung, còn ${frames.length}`); }
  for (const f of frames) {
    await page.evaluate(async (f) => await window.renderFrame(f), f);
    const b64 = await page.evaluate((f) => window.finalize(f), f);
    const an = await page.evaluate(() => window.anchorsAt()); if (an) ANC[f] = an;
    if (f % 48 === 0) fs.writeFileSync(AF, JSON.stringify(ANC));
    const raw = Buffer.from(b64, 'base64');
    const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-q:v', '2', path.join(OUT, String(f).padStart(5, '0') + '.jpg')]);
    enc.stdin.end(raw); await new Promise((r) => enc.on('close', r));
    if (f % 48 === 0) console.error(`[hero ${arg('hero')}/${arg('variant', 'a')}] ${f}/${N} ${((Date.now() - t0) / 1000 / (frames.indexOf(f) + 1)).toFixed(2)} s/khung`);
  }
  fs.writeFileSync(AF, JSON.stringify(ANC));
  fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify({ hero: arg('hero'), variant: arg('variant', 'a'), frames: N, dur: DUR, w: W, h: H, spp: +arg('spp', 1), max_tex: SU && SU.maxTex, s_per_frame: +((Date.now() - t0) / 1000 / Math.max(1, frames.length)).toFixed(2) }));
  await browser.close();
})();

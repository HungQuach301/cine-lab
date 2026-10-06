// Last Lamplighters · driver CẢNH ĐINH 3D (CHUAN-KENH §11.3). Ghi chuỗi JPG (q 2) để mẫu `plate` của scripts/ll/lib phát làm nền.
//   node scripts/ll/hero.js --hero ep06/printshop --variant a --dur 12.5 --out /var/tmp/cine-out/hero/ep06-printshop-a [--w 1920 --h 1080] [--only 0,120] [--opt '{}']
// Tất định: cùng tham số → cùng khung. Ghi <out>/%05d.jpg + <out>/meta.json (khung, s/khung).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../../design');
const W = +arg('w', 1920), H = +arg('h', 1080), OUT = path.resolve(arg('out')), DUR = +arg('dur', 6), N = Math.ceil(DUR * 24);
const ONLY = (arg('only', '') || '').split(',').filter(Boolean).map(Number);
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver|WebGLRenderer|swiftshader/i.test(t)) console.error('[page]', t); });
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pf = path.join(ROOT, `ll-hero/page-${process.pid}.html`);
  fs.writeFileSync(pf, '<!doctype html><html><body style="margin:0"><script type="module" src="/ll-hero/page.js"></script></body></html>');
  await page.goto(`http://cine.local/ll-hero/${path.basename(pf)}`); await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 }); fs.unlinkSync(pf);
  await page.evaluate(async (c) => await window.setup(c), { W, H, hero: arg('hero'), variant: arg('variant', 'a'), dur: DUR, spp: +arg('spp', 1), opt: JSON.parse(arg('opt', '{}')) });
  const frames = ONLY.length ? ONLY : [...Array(N).keys()]; const t0 = Date.now();
  for (const f of frames) {
    await page.evaluate(async (f) => await window.renderFrame(f), f);
    const b64 = await page.evaluate((f) => window.finalize(f), f);
    const raw = Buffer.from(b64, 'base64');
    const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-q:v', '2', path.join(OUT, String(f).padStart(5, '0') + '.jpg')]);
    enc.stdin.end(raw); await new Promise((r) => enc.on('close', r));
    if (f % 48 === 0) console.error(`[hero ${arg('hero')}/${arg('variant', 'a')}] ${f}/${N} ${((Date.now() - t0) / 1000 / (frames.indexOf(f) + 1)).toFixed(2)} s/khung`);
  }
  fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify({ hero: arg('hero'), variant: arg('variant', 'a'), frames: N, dur: DUR, w: W, h: H, s_per_frame: +((Date.now() - t0) / 1000 / frames.length).toFixed(2) }));
  await browser.close();
})();

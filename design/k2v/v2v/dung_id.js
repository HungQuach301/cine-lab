// NC-V2V · driver MẶT NẠ ID mỗi khung (lượt riêng, không dựng hình màu). Chromium headless + llvmpipe như máy V7B.
//   node dung_id.js --wt /var/tmp/v7b-wt --page <thư mục có page-id.js> --opt '<opt shot>' --dur 10 --w 1280 --h 720 --out <thư mục> [--from 0 --to 240] [--census]
// Ra: <out>/id/%05d.png (bảng màu V2V_PAL) + <out>/id.json (% điểm ảnh từng loại mỗi khung).
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const WT = path.resolve(arg('wt', '/var/tmp/v7b-wt')), ROOT = path.join(WT, 'design'), PG = path.resolve(arg('page')), CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require(path.join(WT, 'scripts/k2tl/gl.js')), { gl: GL, flags: GLFLAGS } = GLM.pick();
const W = +arg('w', 1280), H = +arg('h', 720), OUT = path.resolve(arg('out')), DUR = +arg('dur', 10), SCALE = +arg('scale', 1);
(async () => {
  fs.mkdirSync(path.join(OUT, 'id'), { recursive: true });
  const browser = await chromium.launch({ args: [...GLFLAGS, '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=12000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|VALIDATE_STATUS false/.test(t)) { console.error('[page] LỖI SHADER', t.slice(0, 600)); process.exit(7); } if (!/GPU stall|GL Driver|WebGLRenderer|llvmpipe|Mesa|swiftshader|Automatic fallback/i.test(t)) console.error('[page]', t.slice(0, 300)); });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname);
    if (u === '/v2v.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0"><script type="module" src="/k2v/v2v/page-id.js"></script></body>' });
    const p = u === '/k2v/v2v/page-id.js' ? path.join(PG, 'page-id.js') : u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : u.startsWith('/assets/') ? path.join(WT, u) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/v2v.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 120000 });
  const SU = await page.evaluate(async (c) => await window.setup(c), { W, H, hero: 'tl/t3tl', variant: 'a', dur: DUR, spp: 1, opt: JSON.parse(arg('opt', '{}')) });
  const renderer = await GLM.assertRenderer(GL, (SU && SU.renderer) || await GLM.rendererOf(page), browser, 'v2v id');
  if (process.argv.includes('--census')) { console.log(JSON.stringify(await page.evaluate(() => window.v2vCensus()), null, 1)); }
  const N = Math.min(Math.round(DUR * 24), SU && SU.N ? SU.N : 1e9), from = +arg('from', 0), to = Math.min(+arg('to', N), N), rows = [];
  const only = (arg('only', '') || '').split(',').filter(Boolean).map(Number), frames = only.length ? only : [...Array(to - from).keys()].map((i) => i + from);
  const t0 = Date.now();
  for (const f of frames) {
    const r = await page.evaluate(([f, s]) => window.v2vIdMask(f, s), [f, SCALE]);
    fs.writeFileSync(path.join(OUT, 'id', String(f).padStart(5, '0') + '.png'), Buffer.from(r.png_b64, 'base64')); delete r.png_b64; rows.push(r);
    if (f % 48 === 0) console.error(`[id] ${f} ${((Date.now() - t0) / 1000 / rows.length).toFixed(2)} s/khung ${JSON.stringify(r.pct)}`);
  }
  fs.writeFileSync(path.join(OUT, 'id.json'), JSON.stringify({ renderer, gl: GL, W, H, scale: SCALE, frames: rows }));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

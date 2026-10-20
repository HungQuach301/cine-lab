// NC-V2V3 · driver MỘT LẦN DỰNG mỗi khung: (1) MÀU — đúng vòng của scripts/k2/hero.js V7B (window.renderFrame → window.finalize → ffmpeg vflip JPEG q2),
// (2) ĐỘ SÂU từ chính renderer (depth.js), (3) MẶT NẠ ID 10 loại (idmask.js NC-V2V). Chromium headless + llvmpipe như máy V7B (KHOP1: kiểm trình dựng).
//   node dung3.js --wt /var/tmp/v7b-wt --page <thư mục có page-v2v3.js> --opt '<opt shot>' --dur 10 --w 1280 --h 720 --out <thư mục> [--from 0 --to 240] [--idscale 1]
// Ra: <out>/rgb/%05d.jpg · <out>/pho/%05d.png (trắng = mesh phố makeCity, cho mái nhà) · <out>/depth/%05d.png (log 16 bit R:G, B = trời) · <out>/id/%05d.png (bảng V2V_PAL) · <out>/meta3.json
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const WT = path.resolve(arg('wt', '/var/tmp/v7b-wt')), ROOT = path.join(WT, 'design'), PG = path.resolve(arg('page')), CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require(path.join(WT, 'scripts/k2tl/gl.js')), { gl: GL, flags: GLFLAGS } = GLM.pick();
const W = +arg('w', 1280), H = +arg('h', 720), OUT = path.resolve(arg('out')), DUR = +arg('dur', 10), IDS = +arg('idscale', 1);
(async () => {
  for (const d of ['rgb', 'depth', 'id', 'pho']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
  const browser = await chromium.launch({ args: [...GLFLAGS, '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=12000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|VALIDATE_STATUS false/.test(t)) { console.error('[page] LỖI SHADER', t.slice(0, 600)); process.exit(7); } if (!/GPU stall|GL Driver|WebGLRenderer|llvmpipe|Mesa|swiftshader|Automatic fallback/i.test(t)) console.error('[page]', t.slice(0, 300)); });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname);
    if (u === '/v2v3.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0"><script type="module" src="/k2v/v2v3/page-v2v3.js"></script></body>' });
    const p = u === '/k2v/v2v3/page-v2v3.js' ? path.join(PG, 'page-v2v3.js') : u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : u.startsWith('/assets/') ? path.join(WT, u) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/v2v3.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 120000 });
  const SU = await page.evaluate(async (c) => await window.setup(c), { W, H, hero: 'tl/t3tl', variant: 'a', dur: DUR, spp: 1, opt: JSON.parse(arg('opt', '{}')) });
  const renderer = await GLM.assertRenderer(GL, (SU && SU.renderer) || await GLM.rendererOf(page), browser, 'v2v3');
  const N = Math.min(Math.round(DUR * 24), SU && SU.N ? SU.N : 1e9), from = +arg('from', 0), to = Math.min(+arg('to', N), N), rows = [];
  const SKIP = (arg('skip', '') || '').split(','), t0 = Date.now(), nm = (f, e) => String(f).padStart(5, '0') + e;
  for (let f = from; f < to; f++) {
    const ta = Date.now();
    await page.evaluate(async (f) => await window.renderFrame(f), f);
    const b64 = await page.evaluate((f) => window.finalize(f), f);
    const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-q:v', '2', path.join(OUT, 'rgb', nm(f, '.jpg'))]);
    enc.stdin.end(Buffer.from(b64, 'base64')); const encP = new Promise((r) => enc.on('close', r));
    const tb = Date.now(); const d = SKIP.includes('depth') ? { png_b64: '' } : await page.evaluate(() => window.v2v3Depth(1)); fs.writeFileSync(path.join(OUT, 'depth', nm(f, '.png')), Buffer.from(d.png_b64, 'base64')); delete d.png_b64;
    const c = SKIP.includes('city') ? { png_b64: '' } : await page.evaluate(() => window.v2v3City(1)); fs.writeFileSync(path.join(OUT, 'pho', nm(f, '.png')), Buffer.from(c.png_b64, 'base64'));
    const tc = Date.now(); const r = SKIP.includes('id') ? { png_b64: '' } : await page.evaluate(([f, s]) => window.v2vIdMask(f, s), [f, IDS]); fs.writeFileSync(path.join(OUT, 'id', nm(f, '.png')), Buffer.from(r.png_b64, 'base64')); delete r.png_b64;
    await encP; rows.push({ f, depth: d, pho_pct: c.pct, id_pct: r.pct, year: r.year, s_mau: (tb - ta) / 1000, s_sau: (tc - tb) / 1000, s_id: (Date.now() - tc) / 1000 });
    if (f % 24 === 0) { console.error(`[v2v3] ${f}/${to} ${((Date.now() - t0) / 1000 / rows.length).toFixed(2)} s/khung · sâu ${d.zmin}–${d.zmax} m trời ${d.sky_pct}% · id ${JSON.stringify(r.pct)}`);
      fs.writeFileSync(path.join(OUT, 'meta3.json.part'), JSON.stringify({ frames: rows })); }
  }
  fs.writeFileSync(path.join(OUT, 'meta3.json'), JSON.stringify({ renderer, gl: GL, W, H, dur: DUR, idscale: IDS, opt: JSON.parse(arg('opt', '{}')), s_per_frame: +((Date.now() - t0) / 1000 / rows.length).toFixed(2), frames: rows }));
  try { fs.unlinkSync(path.join(OUT, 'meta3.json.part')); } catch (e) { /* */ }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

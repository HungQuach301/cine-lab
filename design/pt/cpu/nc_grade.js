// NC-CPU · CHỈNH MÀU ảnh Cycles/Eevee (HDR tuyến tính) bằng CHÍNH đường ống k2v (window.gradeHDR: tone ACES + LUT A + chỉnh màu V6 + hạt) → cách B/C
//  cùng tông với cách A (ghép liền ở cú lặn). Đầu vào: <thư mục>/*.f32 (RGBA float32, hàng từ dưới lên; nc_exr.py ghi) → <ra>/<tên>.png
//  NC_DESIGN=… NC_SCRIPTS=… node design/pt/cpu/nc_grade.js --scene ../nc/ncA --opt '<json>' --in <thư mục f32> --out <thư mục> --w 1920 --h 1080 [--f0 <khung đầu (hạt)>]
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = process.env.NC_DESIGN, SCR = process.env.NC_SCRIPTS, CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require(path.join(SCR, 'gl.js')), { gl: GL, flags: GLFLAGS } = GLM.pick();
(async () => {
    const browser = await chromium.launch({ args: [...GLFLAGS, '--ignore-gpu-blocklist', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=14000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|ERROR: 0:/.test(t)) { console.error('[page] LỖI SHADER', t.slice(0, 3000)); process.exit(7); } });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname), p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (u === '/tl.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"><script type="module" src="/k2v/tl/page.js"></script></body>' });
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p }); route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/tl.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const cfg = { W: +arg('w', 1920), H: +arg('h', 1080), scene: arg('scene'), pack: '/cache/scene/gib/pack/', lut: '/cache/lut/k2-a-thep-lanh.cube', lutMode: 1, look: {}, photo: '/cache/loc/ng_crop.jpg', tech: JSON.parse(arg('tech', '{"spp":1}')), lutK: 1, opt: JSON.parse(arg('opt', '{}')) };
  const info = await page.evaluate(async (c) => await window.setup(c), cfg); await GLM.assertRenderer(GL, info.renderer, browser);
  const IN = path.resolve(arg('in')), OUT = path.resolve(arg('out')); fs.mkdirSync(OUT, { recursive: true });
  const files = fs.readdirSync(IN).filter((x) => x.endsWith('.f32')).sort(), t0 = Date.now();
  for (const fn of files) { const b64 = fs.readFileSync(path.join(IN, fn)).toString('base64'), f = parseInt(fn) || +arg('f0', 0);
    const png = await page.evaluate(async ([f, b]) => await window.gradeHDR(f, b, false), [f, b64]); fs.writeFileSync(path.join(OUT, fn.replace('.f32', '.png')), Buffer.from(png, 'base64')); }
  console.log(JSON.stringify({ anh: files.length, s: (Date.now() - t0) / 1000 }));
  await browser.close();
})();

// V7C (việc 2) · driver ĐO BỐ CỤC bằng mặt nạ ID (idmask_v7c.js nối vào cuối bản sao page.js lúc phục vụ trang — page.js trên đĩa không đổi).
//   node design/k2v/v7c/do_bocuc.js --opt '<opt shot>' --out <tệp.json> [--every 12 | --only 0,48] [--td '<json tiêu điểm>'] [--png <thư mục mặt nạ>] [--jpg <thư mục khung màu>] [--w 960 --h 540] [--scale 0.5] [--census]
//   (--root <cây repo> để đo cùng thước trên mã V7B: worktree tại 317dcf51)
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const RT = path.resolve(arg('root', path.join(__dirname, '../../..'))), ROOT = path.join(RT, 'design'), CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require(path.join(RT, 'scripts/k2tl/gl.js')), { gl: GL, flags: GLFLAGS } = GLM.pick();
const W = +arg('w', 960), H = +arg('h', 540), SCALE = +arg('scale', 0.5), ID = fs.readFileSync(path.join(__dirname, 'idmask_v7c.js'), 'utf8');
(async () => {
  const browser = await chromium.launch({ args: [...GLFLAGS, '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=12000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|VALIDATE_STATUS false|ERROR: 0:/.test(t)) { console.error('[page] LỖI SHADER', t.slice(0, 1500)); process.exit(7); } });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname);
    if (u === '/tl.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"><script type="module" src="/k2v/tl/page-v7c.js"></script></body>' });
    if (u === '/k2v/tl/page-v7c.js') { const s = fs.readFileSync(path.join(ROOT, 'k2v/tl/page.js'), 'utf8').replace('window.ready = true;', '') + '\n// ===== V7C idmask_v7c.js =====\n' + ID + '\nwindow.ready = true;\n';
      return route.fulfill({ status: 200, contentType: 'text/javascript', body: s }); }
    const p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/tl.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 90000 });
  const cfg = { W, H, opt: JSON.parse(arg('opt', '{}')), scene: arg('scene', 't3tl'), pack: '/cache/scene/gib/pack/', lut: '/cache/lut/k2-a-thep-lanh.cube', lutMode: 1, look: {}, photo: '/cache/loc/ng_crop.jpg', tech: { spp: 1 }, lutK: 1 };
  const info = await page.evaluate(async (c) => await window.setup(c), cfg); await GLM.assertRenderer(GL, info.renderer, browser);
  if (process.argv.includes('--census')) console.error(JSON.stringify(await page.evaluate(() => window.v7cCensus()), null, 1));
  const N = info.N, every = +arg('every', 12), only = (arg('only', '') || '').split(',').filter(Boolean).map(Number), frames = only.length ? only : [...Array(Math.ceil(N / every)).keys()].map((i) => i * every);
  const TD = JSON.parse(arg('td', '[]')), PNG = arg('png'), rows = [], t0 = Date.now();
  if (PNG) fs.mkdirSync(PNG, { recursive: true });
  const JPG = arg('jpg'); if (JPG) fs.mkdirSync(JPG, { recursive: true });
  for (const f of frames) { if (JPG && !arg('cams')) { const im = await page.evaluate(async (f) => (await window.renderFrame(f, false, { noText: true })).img, f); fs.writeFileSync(path.join(JPG, String(f).padStart(5, '0') + '.jpg'), Buffer.from(im, 'base64')); }   // khung màu xem kèm (soi bố cục)
    const CAMS = JSON.parse(arg('cams', '[null]'));   // --cams '[{id, p, l, fov}, …]': đo mọi ứng viên ở cùng khung (soạn máy)
    for (const cv of CAMS) { const r = await page.evaluate(([f, s, td, png, cv]) => window.v7cMeasure(f, s, td, png, cv), [f, SCALE, TD, !!PNG, cv]);
      if (cv) { r.ung_vien = cv.id; if (JPG) { const im = await page.evaluate(async ([f, cv]) => (await window.renderFrame(f, false, { noText: true, cam: cv })).img, [f, cv]); fs.writeFileSync(path.join(JPG, cv.id + '-' + String(f).padStart(5, '0') + '.jpg'), Buffer.from(im, 'base64')); } }
      if (r.png_b64) fs.writeFileSync(path.join(PNG, (cv ? cv.id + '-' : '') + String(f).padStart(5, '0') + '.png'), Buffer.from(r.png_b64, 'base64')); delete r.png_b64; rows.push(r); } }
  fs.mkdirSync(path.dirname(path.resolve(arg('out'))), { recursive: true });
  fs.writeFileSync(arg('out'), JSON.stringify({ renderer: info.renderer, gl: GL, W, H, scale: SCALE, N, s_per_frame: +((Date.now() - t0) / 1000 / frames.length).toFixed(2), frames: rows }));
  const avg = (k) => +(rows.reduce((a, r) => a + r[k], 0) / rows.length).toFixed(1);
  console.log(JSON.stringify({ n: rows.length, noi_dung: avg('noi_dung'), trong: avg('trong'), agl: avg('agl'), xuong: avg('xuong') }));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

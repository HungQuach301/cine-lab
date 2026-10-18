// V6 bước 7 (phương án A) · trình điều khiển XUẤT CẢNH k2v → Blender/Cycles và CHỈNH MÀU ảnh ghép bằng CHÍNH đường ống k2v (tone ACES + LUT A + V6 grade + hạt).
//  node scripts/k2tl/export6.js export --scene vinh6 --f 192 --out <thư mục>   → manifest.json + b<i>.bin (hình học, ma trận bản sao) + albedo.f32, nosmoke.f32, smoke.f32 (RGBA float, hàng từ dưới lên) + clean.jpg
//  node scripts/k2tl/export6.js grade  --scene vinh6 --f 192 --hdr <ghep.f32> --out <ra.png> [--text]  → ảnh cuối (cùng tone/grade/hạt của khung; --text: thêm lớp chữ của cảnh)
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const MODE = process.argv[2], ROOT = path.resolve(__dirname, '../../design'), CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require('./gl.js'), { gl: GL, flags: GLFLAGS } = GLM.pick();
const W = +arg('w', 1920), H = +arg('h', 1080), F = +arg('f', 0), OUT = path.resolve(arg('out'));
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
  const cfg = { W, H, scene: arg('scene'), pack: '/cache/scene/gib/pack/', lut: '/cache/lut/k2-a-thep-lanh.cube', lutMode: 1, look: {}, photo: '/cache/loc/ng_crop.jpg', tech: JSON.parse(arg('tech', '{}')), lutK: 1, opt: JSON.parse(arg('opt', '{}')) };
  const info = await page.evaluate(async (c) => await window.setup(c), cfg); await GLM.assertRenderer(GL, info.renderer, browser);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const t0 = Date.now();
  if (MODE === 'export') {
    fs.mkdirSync(OUT, { recursive: true });
    const r = await page.evaluate(async (f) => { const r = await window.renderFrame(f, false, { noText: true }); return { img: r.img }; }, F);   // áp trạng thái khung + khung sạch k2v
    fs.writeFileSync(path.join(OUT, 'clean.jpg'), Buffer.from(r.img, 'base64'));
    const man = await page.evaluate(async (o) => await window.exportFrame(o), { far: +arg('far', 6000) });
    const bufs = []; for (let i = 0; i < man.nbuf; i++) { const b = await page.evaluate((i) => window.exportBuf(i), i); fs.writeFileSync(path.join(OUT, `b${i}.bin`), Buffer.from(b.b64, 'base64')); bufs.push({ type: b.type, n: b.n }); }
    man.bufs = bufs; man.scene = cfg.scene; man.f = F; man.renderer = info.renderer;
    for (const pass of ['albedo', 'nosmoke', 'smoke']) { const b = await page.evaluate(async ([f, p]) => await window.passFrame(f, p), [F, pass]); fs.writeFileSync(path.join(OUT, pass + '.f32'), Buffer.from(b, 'base64')); }
    man.passes = { W, H, fmt: 'RGBA float32, hàng từ dưới lên', albedo: 'diffuseColor tuyến tính (uMask 3)', nosmoke: 'HDR tuyến tính trước tone (không khói, có SSAO)', smoke: 'HDR khói nhân alpha trên nền trong suốt, có che độ sâu' };
    man.export_s = (Date.now() - t0) / 1000; fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(man));
    console.log(JSON.stringify({ vat: man.objs.length, tam_giac: man.objs.reduce((a, o) => a + o.nt * (o.inst || 1), 0), MB: +(man.bytes / 1e6).toFixed(1), s: man.export_s }));
  } else if (MODE === 'grade') {
    await page.evaluate(async (f) => { await window.renderFrame(f, false, { noText: true }); }, F);
    const hdr = fs.readFileSync(path.resolve(arg('hdr'))).toString('base64');
    const img = await page.evaluate(async ([f, b, txt]) => await window.gradeHDR(f, b, txt), [F, hdr, !!process.argv.includes('--text')]);
    fs.writeFileSync(OUT, Buffer.from(img, 'base64')); console.log(JSON.stringify({ ra: OUT, s: (Date.now() - t0) / 1000 }));
  }
  await browser.close();
})();

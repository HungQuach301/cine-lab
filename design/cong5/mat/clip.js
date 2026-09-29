// W3 (Cổng 5 v2, mặt Ida A-i) — driver CLIP: dựng trang một lần, render N khung liên tiếp (mỗi khung tích luỹ lại từ đầu), ghép mp4 24 fps.
// node design/cong5/mat/clip.js --page cong5/mat/page_layout_fl.js --out <thư mục> --frames 72 [--samples 2] [--w 1920 --h 1080] --args '<json>'
// Trang phải hiểu tên khung là số thứ tự "0".."N-1" (page_layout_fl.js: f = f0 + i, track[i] = trọng số rig mặt của khung i).
// Ghi: <out>/clip.mp4 (H.264, yuv420p, CRF 16), <out>/f####.png (mọi khung), <out>/clip.timing.json.
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../..');
const page_ = arg('page'), out = path.resolve(arg('out', '.'));
const samples = +arg('samples', 2), N = +arg('frames', 72), W = +arg('w', 1920), H = +arg('h', 1080);
const extra = JSON.parse(arg('args', '{}'));
fs.mkdirSync(out, { recursive: true });

(async () => {
  const t0 = Date.now();
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver/.test(t)) console.error('[page]', t); });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pageFile = path.join(ROOT, `page-${process.pid}.html`);
  fs.writeFileSync(pageFile, `<!doctype html><html><body style="margin:0"><script type="module" src="/${page_}"></script></body></html>`);
  try {
    await page.goto(`http://cine.local/${path.basename(pageFile)}`);
    await page.waitForFunction(() => typeof window.setup === 'function' && typeof window.renderFrame === 'function', null, { timeout: 60000 });
    const tS = Date.now();
    await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, ...extra });
    const setup_s = (Date.now() - tS) / 1000, per = [];
    for (let i = 0; i < N; i++) {
      const tA = Date.now();
      await page.evaluate(async ([f, s]) => await window.renderFrame(f, s), [String(i), samples]);
      const b64 = await page.evaluate((f) => window.finalize(f), i);
      spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', path.join(out, `f${String(i).padStart(4, '0')}.png`)], { input: Buffer.from(b64, 'base64') });
      per.push((Date.now() - tA) / 1000);
      if (i % 12 === 0) console.log(`khung ${i}/${N} ${per[per.length - 1].toFixed(1)} s`);
    }
    const r = spawnSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '24', '-i', path.join(out, 'f%04d.png'), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path.join(out, 'clip.mp4')]);
    if (r.status !== 0) console.error(String(r.stderr));
    const timing = { page: page_, W, H, samples, frames: N, setup_s, frame_s_mean: per.reduce((a, b) => a + b, 0) / N, frame_s_max: Math.max(...per), total_wall_s: (Date.now() - t0) / 1000, args: extra };
    fs.writeFileSync(path.join(out, 'clip.timing.json'), JSON.stringify(timing, null, 1));
    console.log(JSON.stringify({ frame_s_mean: timing.frame_s_mean, total_wall_s: timing.total_wall_s }));
  } finally { await browser.close(); if (fs.existsSync(pageFile)) fs.unlinkSync(pageFile); }
})().catch((e) => { console.error(e); process.exit(1); });

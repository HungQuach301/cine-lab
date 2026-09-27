// Driver render khung tĩnh cho Cổng 3 (Chromium headless + SwiftShader).
// node shared/render_still.js --page <đường dẫn module JS, tính từ design/cong3> --frame <tên khung> --out <thư mục>
//      [--samples 32] [--frames 1] [--w 1920 --h 1080] [--args '<json>']
// Module trang phải gán: window.setup(cfg) (async được) và window.renderFrame(name, samples) → {accum_ms} sau khi tích luỹ;
// rồi driver gọi window.finalize(f) cho f = 0..frames-1 (chỉ pass cuối, grain đổi theo f).
// Ghi: <out>/<frame>.png (khung 0), <out>/<frame>.rgb (nếu --frames > 1, RGB24 thô để ghép video), <out>/<frame>.timing.json.
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '..');
const page_ = arg('page'), frame = arg('frame'), out = path.resolve(arg('out', '.'));
const samples = +arg('samples', 32), frames = +arg('frames', 1), W = +arg('w', 1920), H = +arg('h', 1080);
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
  await page.goto(`http://cine.local/${path.basename(pageFile)}`);
  await page.waitForFunction(() => typeof window.setup === 'function' && typeof window.renderFrame === 'function', null, { timeout: 60000 });
  const tSetup0 = Date.now();
  await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, ...extra });
  const tSetup = Date.now() - tSetup0;
  const tA = Date.now();
  const r = await page.evaluate(async ([f, s]) => await window.renderFrame(f, s), [frame, samples]);
  const first = await page.evaluate((f) => window.finalize(f), 0); // đồng bộ GPU: readPixels chặn tới khi render xong
  const accumWall = Date.now() - tA;
  const bufs = [Buffer.from(first, 'base64')];
  const tF = Date.now();
  for (let f = 1; f < frames; f++) bufs.push(Buffer.from(await page.evaluate((f) => window.finalize(f), f), 'base64'));
  const finWall = frames > 1 ? (Date.now() - tF) / (frames - 1) : null;
  await browser.close(); fs.unlinkSync(pageFile);
  const png = path.join(out, frame + '.png');
  spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', png], { input: bufs[0] });
  if (frames > 1) fs.writeFileSync(path.join(out, frame + '.rgb'), Buffer.concat(bufs));
  const timing = { page: page_, frame, W, H, samples, frames, setup_s: tSetup / 1000, render_frame_s: accumWall / 1000,
    page_reported_accum_ms: r && r.accum_ms, page_prof_ms: r && r.prof_ms, finalize_per_extra_frame_s: finWall && finWall / 1000, total_wall_s: (Date.now() - t0) / 1000,
    note: 'render_frame_s = tích luỹ mọi mẫu + pass cuối + readPixels của khung 0 (thời gian render thật một khung cuối cùng)' };
  fs.writeFileSync(path.join(out, frame + '.timing.json'), JSON.stringify(timing, null, 1));
  console.log(JSON.stringify(timing));
})().catch((e) => { console.error(e); process.exit(1); });

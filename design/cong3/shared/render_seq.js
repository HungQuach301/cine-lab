// Driver render chuỗi khung (shot chuyển động) cho Cổng 3 v2.
// node shared/render_seq.js --page v2/page.js --shot walk --from 0 --to 96 --out <dir> [--samples 8] [--w 1920 --h 1080] [--args '<json>']
//   [--pngs 0,48,95] (ghi PNG các khung này) [--mp4 <file>] (mã hoá như M1: 30 Mbps tune grain, BT.709 tv)
// Mỗi khung: renderFrame('<shot>@<f>', samples) (trang đặt pose theo f, tích luỹ mẫu, lớp vẽ) rồi finalize(f) (grain theo f).
// Thời gian đo từng khung = tích luỹ + lớp vẽ + pass cuối + readPixels (đồng bộ GPU). Setup đo riêng.
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn, spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '..');
const page_ = arg('page'), shot = arg('shot'), out = path.resolve(arg('out', '.'));
const from = +arg('from', 0), to = +arg('to', 96), samples = +arg('samples', 8), W = +arg('w', 1920), H = +arg('h', 1080);
const rawOut = arg('raw', null); // --raw <file>: ghi RGB24 thô (hàng từ dưới lên) để đo nhấp nháy
const extra = JSON.parse(arg('args', '{}')), pngs = new Set((arg('pngs', '') || '').split(',').filter(Boolean).map(Number)), mp4 = arg('mp4', null);
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
  const tS = Date.now(); await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, shot, ...extra }); const setup_s = (Date.now() - tS) / 1000;
  const ff = mp4 ? spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', '24', '-i', '-',
    '-vf', 'vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-tune', 'grain',
    '-profile:v', 'high', '-b:v', '30M', '-maxrate', '40M', '-bufsize', '60M', '-g', '48', '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24', mp4], { stdio: ['pipe', 'inherit', 'inherit'] }) : null;
  const times = []; const rawFd = rawOut ? fs.openSync(rawOut, 'w') : null;
  for (let f = from; f < to; f++) {
    const a = Date.now();
    await page.evaluate(async ([n, s]) => await window.renderFrame(n, s), [`${shot}@${f}`, samples]);
    const b64 = await page.evaluate((f) => window.finalize(f), f);
    times.push((Date.now() - a) / 1000);
    const buf = Buffer.from(b64, 'base64');
    if (ff && !ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (rawFd !== null) fs.writeSync(rawFd, buf);
    if (pngs.has(f)) spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', path.join(out, `${shot}_${String(f).padStart(3, '0')}.png`)], { input: buf });
  }
  if (ff) { ff.stdin.end(); await new Promise((r) => ff.on('close', r)); }
  if (rawFd !== null) fs.closeSync(rawFd);
  await browser.close(); fs.unlinkSync(pageFile);
  const sorted = [...times].sort((x, y) => x - y);
  const res = { page: page_, shot, from, to, frames: times.length, W, H, samples, args: extra, setup_s, per_frame_s: { mean: times.reduce((s, x) => s + x, 0) / times.length, median: sorted[sorted.length >> 1], max: sorted[sorted.length - 1] }, total_wall_s: (Date.now() - t0) / 1000, mp4 };
  fs.writeFileSync(path.join(out, `${shot}.seq-timing.json`), JSON.stringify({ ...res, times }, null, 1));
  console.log(JSON.stringify(res));
})().catch((e) => { console.error(e); process.exit(1); });

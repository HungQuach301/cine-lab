// Cine Lab · M3 THỬ PHONG CÁCH (nhánh thu-phong-cach, không merge) — driver render theo shot, dựa trên page.js của layout (cùng đường ống).
// Học từ design/cong7/thu-mat/frames.js (gói THỬ MẶT V1, reports/m2/cong7/thu-mat/ma-v1.patch).
// node design/m3/thu-phong-cach/frames.js --shot s22 --out <thư mục> [--dbg '{"style":"b3"}'] [--all] [--frames 1440,1452] [--w 960 --h 540] [--tag x]
//   --all    : render trọn shot → <out>/<shot><tag>.mp4 (x264 crf 14 như render_film.js)
//   --page-file <đường dẫn> : phục vụ tệp này thay cho /cong5/layout/page.js (render bằng page.js gốc ebdacde để đối chứng 0 px)
//   --frames : khung phim toàn cục cần lưu PNG → <out>/<shot><tag>_f<khung>.png (không có --all thì chỉ render các khung này)
// Ghi <out>/<shot><tag>.timing.json: giây mỗi khung (render + finalize).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn, spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes('--' + k);
const ROOT = path.resolve(__dirname, '../..');
const W = +arg('w', 960), H = +arg('h', 540), out = path.resolve(arg('out', 'out')), SHOT = arg('shot'), TAG = arg('tag', '');
const dbg = JSON.parse(arg('dbg', '{}')), PAGE_FILE = arg('page-file', null);

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver|THREE.WebGLRenderer/.test(t)) console.error('[page]', t); });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname);
    const p = (PAGE_FILE && u === '/cong5/layout/page.js') ? PAGE_FILE : path.join(ROOT, u);   // --page-file: page.js gốc (đối chứng 0 px)
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.route('http://cine.local/tpc.html', (route) => route.fulfill({ status: 200, contentType: 'text/html',
    body: '<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>' }));
  await page.goto('http://cine.local/tpc.html');
  await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 });
  return page;
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  const page = await newPage(browser);
  const a = Date.now();
  const r = await page.evaluate(async (cfg) => await window.setup(cfg), { W, H, shot: SHOT, nopaint: has('nopaint'), dbg });
  const setup_s = (Date.now() - a) / 1000;
  const f0 = Math.round(r.t0 * 24), f1 = Math.round(r.t1 * 24);
  const pick = arg('frames') ? arg('frames').split(',').map(Number) : [];
  const all = has('all'), todo = all ? Array.from({ length: f1 - f0 }, (_, i) => f0 + i) : pick;
  let ff = null;
  if (all) ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', '24', '-i', '-',
    '-vf', 'vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-tune', 'grain',
    '-g', '48', '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24', path.join(out, `${SHOT}${TAG}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
  const times = [];
  for (const f of todo) {
    const b = Date.now();
    await page.evaluate(async (f) => await window.renderFrame(f), f);
    const b64 = await page.evaluate((f) => window.finalize(f), f);
    times.push((Date.now() - b) / 1000);
    const buf = Buffer.from(b64, 'base64');
    if (ff && !ff.stdin.write(buf)) await new Promise((res) => ff.stdin.once('drain', res));
    if (pick.includes(f)) spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', path.join(out, `${SHOT}${TAG}_f${f}.png`)], { input: buf });
  }
  if (ff) { ff.stdin.end(); await new Promise((res) => ff.on('close', res)); }
  await browser.close();
  const mean = times.reduce((x, y) => x + y, 0) / Math.max(1, times.length);
  const rec = { shot: SHOT, dbg, W, H, frames: todo.length, setup_s, per_frame_s: { mean: +mean.toFixed(3), max: +Math.max(...times).toFixed(3) }, times };
  fs.writeFileSync(path.join(out, `${SHOT}${TAG}.timing.json`), JSON.stringify(rec, null, 1));
  console.log(JSON.stringify({ shot: SHOT, frames: todo.length, per_frame_s: rec.per_frame_s, setup_s }));
})().catch((e) => { console.error(e); process.exit(1); });

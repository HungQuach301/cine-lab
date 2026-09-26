// Driver render theo khung cho phong cách (a) 2D Canvas và (b) three.js trong Chromium headless.
// node render_chromium.js --style 2d|3d --start 0 --end 240 --samples 1 --out out.mp4 [--json timing.json]
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const style = arg('style', '2d'), start = +arg('start', 0), end = +arg('end', 240), samples = +arg('samples', 1);
const out = arg('out', `out-${style}.mp4`), jsonOut = arg('json', null);
const ROOT = __dirname;
const scene = JSON.parse(fs.readFileSync(path.join(ROOT, 'scene.json')));
const sheet = JSON.parse(fs.readFileSync(path.join(ROOT, '../consistency/model-sheet.json')));

(async () => {
  const tStart = Date.now();
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('console', (m) => console.error('[page]', m.text()));
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  // Phục vụ file cục bộ qua origin giả để import ES module không vướng CORS của file://.
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : 'text/html';
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const html = style === '3d'
    ? '<canvas id="c"></canvas><script type="module" src="scene3d.js"></script>'
    : '<canvas id="c"></canvas><script src="scene2d.js"></script>';
  fs.writeFileSync(path.join(ROOT, `page-${style}.html`), `<!doctype html><html><body style="margin:0">${html}</body></html>`);
  await page.goto(`http://cine.local/page-${style}.html`);
  await page.waitForFunction(() => typeof window.setup === 'function' && typeof window.renderFrame === 'function');
  await page.evaluate(([s, m]) => window.setup(s, m), [scene, sheet]);

  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(scene.fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', String(scene.fps), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const tReady = Date.now();
  let draw = 0, enc = 0, xfer = 0;
  for (let f = start; f < end; f++) {
    const a = Date.now();
    const r = await page.evaluate(([f, s]) => window.renderFrame(f, s), [f, samples]);
    const buf = Buffer.from(r.url.slice(r.url.indexOf(',') + 1), 'base64');
    draw += r.draw_ms; enc += r.encode_ms; xfer += Date.now() - a - r.draw_ms - r.encode_ms;
    if (!ff.stdin.write(buf)) await new Promise((res) => ff.stdin.once('drain', res));
  }
  ff.stdin.end();
  await new Promise((res) => ff.on('close', res));
  await browser.close();
  const tEnd = Date.now();
  const frames = end - start, filmS = frames / scene.fps, wall = (tEnd - tStart) / 1000;
  const res = { style, samples, frames, film_s: filmS, wall_s: wall, startup_s: (tReady - tStart) / 1000,
    draw_s: draw / 1000, png_encode_s: enc / 1000, transfer_s: xfer / 1000,
    render_s_per_film_s: wall / filmS, out };
  console.log(JSON.stringify(res));
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(res, null, 1));
})();

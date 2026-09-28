// Driver render ANIMATIC Cổng 4. Mỗi shot một trang Chromium mới (không nhiễm chéo trạng thái giữa các bộ cảnh).
// node design/cong5/layout/render_film.js --out <thư mục> [--w 960 --h 540] [--only s01,s02] [--list] [--events] [--probe] [--meta-only] [--nopaint]
// Ghi: <out>/video.mp4 (hình, chưa tiếng; x264 crf 16 — bản trung gian), <out>/shots/<id>.timing.json, <out>/motion/<id>.json,
//      <out>/thumbs/<id>_{a,b,c}.png (đầu, giữa, cuối shot) ; --list: in bảng shot (JSON) rồi thoát.
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn, spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes('--' + k);
const ROOT = path.resolve(__dirname, '../..');               // design/ → URL /cong3/..., /cong4/...
const W = +arg('w', 960), H = +arg('h', 540), out = path.resolve(arg('out', 'out'));
const only = (arg('only', '') || '').split(',').filter(Boolean);

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver|THREE.WebGLRenderer/.test(t)) console.error('[page]', t); });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pageFile = path.join(ROOT, `cong5/layout/page-${process.pid}.html`);
  fs.writeFileSync(pageFile, `<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>`);
  await page.goto(`http://cine.local/cong5/layout/${path.basename(pageFile)}`);
  await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 });
  fs.unlinkSync(pageFile);
  return page;
}

(async () => {
  const T0 = Date.now();
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  let page = await newPage(browser);
  const list = await page.evaluate(() => window.listShots());
  if (has('list')) { console.log(JSON.stringify(list, null, 1)); await browser.close(); return; }
  if (has('events')) { console.log(JSON.stringify(await page.evaluate(() => window.listEvents()), null, 1)); await browser.close(); return; }
  await page.close();
  for (const d of ['shots', 'motion', 'thumbs']) fs.mkdirSync(path.join(out, d), { recursive: true });
  const todo = only.length ? list.filter((s) => only.includes(s.id)) : list;
  const mp4 = path.join(out, only.length ? `video_${only.join('-')}.mp4` : 'video.mp4');
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', '24', '-i', '-',
    '-vf', 'vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-tune', 'grain',
    '-g', '48', '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const summary = [];
  for (const s of todo) {
    const a = Date.now(); page = await newPage(browser);
    await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, shot: s.id, nopaint: has('nopaint'), dbg: JSON.parse(arg('dbg', '{}')) });
    const setup_s = (Date.now() - a) / 1000;
    const f0 = Math.round(s.t0 * 24), f1 = Math.round(s.t1 * 24), times = [], meta = [];
    const probe = has('probe'), fl = probe ? [f0, (f0 + f1) >> 1, f1 - 1] : null, metaOnly = has('meta-only');
    if (metaOnly) { for (let f = f0; f < f1; f++) { await page.evaluate((f) => window.stepFrame(f), f); meta.push(await page.evaluate(() => window.frameMeta())); }
      await page.close(); fs.writeFileSync(path.join(out, 'motion', `${s.id}.json`), JSON.stringify({ first_frame: f0, frames: meta })); console.error(`${s.id}: xuất lại chuyển động ${meta.length} khung`); continue; }
    for (let f = f0; f < f1; f++) {
      if (probe && !fl.includes(f)) continue;
      const b = Date.now();
      await page.evaluate(async (f) => await window.renderFrame(f), f);
      const b64 = await page.evaluate((f) => window.finalize(f), f);
      times.push((Date.now() - b) / 1000);
      meta.push(await page.evaluate(() => window.frameMeta()));
      const buf = Buffer.from(b64, 'base64');
      if (!probe && !ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      const k = f - f0, n = f1 - f0;
      if (k === 0 || k === (n >> 1) || k === n - 1) spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', path.join(out, 'thumbs', `${s.id}_${k === 0 ? 'a' : k === n - 1 ? 'c' : 'b'}.jpg`)], { input: buf });
    }
    await page.close();
    const mean = times.reduce((x, y) => x + y, 0) / times.length;
    const rec = { id: s.id, t0: s.t0, t1: s.t1, frames: times.length, setup_s, per_frame_s: { mean: +mean.toFixed(3), max: +Math.max(...times).toFixed(3) }, wall_s: (Date.now() - a) / 1000 };
    fs.writeFileSync(path.join(out, 'shots', `${s.id}.timing.json`), JSON.stringify({ ...rec, times }, null, 1));
    fs.writeFileSync(path.join(out, 'motion', `${s.id}.json`), JSON.stringify({ first_frame: f0, frames: meta }));
    summary.push(rec); console.error(`${s.id}: ${rec.frames} khung, dựng ${setup_s.toFixed(1)} s, ${mean.toFixed(2)} s/khung, tổng ${rec.wall_s.toFixed(0)} s`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
  await browser.close();
  const res = { W, H, shots: summary.length, frames: summary.reduce((x, s) => x + s.frames, 0), total_wall_s: (Date.now() - T0) / 1000, mp4 };
  fs.writeFileSync(path.join(out, only.length ? `timing_${only.join('-')}.json` : 'timing.json'), JSON.stringify({ ...res, summary }, null, 1));
  console.log(JSON.stringify(res));
})().catch((e) => { console.error(e); process.exit(1); });

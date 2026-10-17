// R&D City Timelapse — dựng khung cảnh thử bằng Chromium headless + SwiftShader (như bộ k2v; mã riêng, không sửa design/).
// node render.js --out <mp4|mkv> [--w 960 --h 540 --from 0 --to 720 --shadows 1 --copies 1 --stills 0,240 --jpgdir d --measure 24]
// Ra: video + <out>.log.json (s/khung, ms GL, RSS trình duyệt, tương phản chữ đo trên điểm ảnh).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn, execSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const HERE = __dirname, DATA = process.env.TL_DATA || path.join(process.env.HOME, '.cache/cine-timelapse');
const W = +arg('w', 960), H = +arg('h', 540), F0 = +arg('from', 0), F1 = +arg('to', 720), MEAS = +arg('measure', 24);
const OPT = { W, H, frames: 720, shadows: arg('shadows', '1') === '1', copies: +arg('copies', 1), shadowRes: +arg('shadowres', 4096), fx: arg('fx', '1') === '1' };

const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(q.url.split('?')[0]);
  const MAP = { '/scene.json': 'ams/scene.json', '/damrak.json': 'ams/damrak.json', '/pose.json': 'photo/pose.json', '/photo.jpg': 'photo/r200144330.jpg' };
  let f = u.startsWith('/three/') ? path.join(HERE, 'node_modules/three', u.slice(7)) : MAP[u] ? path.join(DATA, MAP[u]) : path.join(HERE, u);
  if (u === '/') { r.setHeader('content-type', 'text/html'); return r.end('<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"></body>'); }
  if (!fs.existsSync(f)) { r.statusCode = 404; return r.end(); }
  r.setHeader('content-type', f.endsWith('.js') ? 'text/javascript' : f.endsWith('.jpg') ? 'image/jpeg' : 'application/json'); fs.createReadStream(f).pipe(r);
});
const rss = (pid) => { try { // tổng RSS (MB) của cây tiến trình trình duyệt
  const out = execSync(`ps -e -o pid=,ppid=,rss=`).toString().trim().split('\n').map((l) => l.trim().split(/\s+/).map(Number));
  const kids = new Set([pid]); let grow = true; while (grow) { grow = false; for (const [p, pp] of out) if (kids.has(pp) && !kids.has(p)) { kids.add(p); grow = true; } }
  return Math.round(out.filter(([p]) => kids.has(p)).reduce((a, [, , r]) => a + r, 0) / 1024); } catch { return null; } };

(async () => {
  await new Promise((res) => srv.listen(0, res)); const PORT = srv.address().port;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=12000'] });
  const bpid = browser.process ? browser.process().pid : null;
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; }); page.on('console', (m) => console.error('[page]', m.text()));
  await page.goto(`http://127.0.0.1:${PORT}/`);
  const tl0 = Date.now();
  await page.evaluate(async (opt) => { const j = async (u) => (await fetch(u)).json(); const d = await j('/scene.json');
    const img = new Image(); img.src = '/photo.jpg'; await img.decode();
    window.TL = Object.assign(opt, { data: d, damrak: (await j('/damrak.json')).pts, pose: await j('/pose.json'), photoImg: img }); await import('/scene.js'); }, OPT);
  await page.waitForFunction(() => window.TL && window.TL.ready, null, { timeout: 0 });
  const info = await page.evaluate(() => window.TL.info()); info.load_s = (Date.now() - tl0) / 1000; info.rss_after_load_mb = bpid ? rss(bpid) : null;
  console.error('[info]', JSON.stringify(info));
  if (arg('budget')) { fs.writeFileSync(arg('budget'), JSON.stringify(await page.evaluate(() => window.TL.budgetAll()))); await browser.close(); srv.close(); return; }
  if (arg('campath')) { fs.writeFileSync(arg('campath'), JSON.stringify(await page.evaluate(() => window.TL.camPath()))); await browser.close(); srv.close(); return; }
  if (arg('debugpose')) { const d = path.join(HERE, 'out'); for (const [yr, al, so] of [[1700, 0.5, 0], [2026, 0.5, 0], [2026, 0, 0], [2026, 0.5, 1]]) {
      const r = await page.evaluate(([yr, al, so]) => window.TL.debugPose(yr, al, so), [yr, al, so]); fs.writeFileSync(path.join(d, `pose_${yr}_${al}_${so}.jpg`), Buffer.from(r.img, 'base64')); console.log(yr, al, r.anchor); }
    await browser.close(); srv.close(); return; }
  const STILLS = (arg('stills', '') || '').split(',').filter(Boolean).map(Number);
  if (STILLS.length) { const d = arg('jpgdir', path.join(HERE, 'out')); fs.mkdirSync(d, { recursive: true });
    const res = [];
    for (const f of STILLS) { const t = Date.now(); const r = await page.evaluate(([f]) => window.TL.drawFrame(f, true), [f]);
      fs.writeFileSync(path.join(d, `f${String(f).padStart(4, '0')}.jpg`), Buffer.from(r.img, 'base64')); delete r.img; r.s = (Date.now() - t) / 1000; res.push(r); }
    console.log(JSON.stringify({ info, stills: res, rss_mb: bpid ? rss(bpid) : null })); await browser.close(); srv.close(); return; }
  const OUT = path.resolve(arg('out'));
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', '24', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-g', '48', '-r', '24', '-movflags', '+faststart', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now(), gl = [], texts = [], mem = [], msf = [], bud = [];
  for (let f = F0; f < F1; f++) {
    const tf = Date.now();
    const r = await page.evaluate(([f, m]) => window.TL.drawFrame(f, m), [f, f % MEAS === 0]);
    gl.push(r.gl_ms); if (r.text) texts.push({ f, year: r.year, items: r.text });
    if (!ff.stdin.write(Buffer.from(r.img, 'base64'))) await new Promise((res) => ff.stdin.once('drain', res));
    msf.push(Date.now() - tf); bud.push(r.budget);
    if ((f - F0) % 48 === 0) { const m = bpid ? rss(bpid) : null; mem.push(m); console.error(`[render] ${f}/${F1} ${((Date.now() - t0) / 1000 / (f - F0 + 1)).toFixed(2)} s/khung rss ${m} MB`); }
  }
  ff.stdin.end(); await new Promise((res) => ff.on('close', res));
  await browser.close(); srv.close();
  const spf = (Date.now() - t0) / 1000 / (F1 - F0);
  const log = { info, opt: { W, H, shadows: OPT.shadows, copies: OPT.copies, shadowRes: OPT.shadowRes }, frames: F1 - F0, s_per_frame: +spf.toFixed(3),
    gl_ms_median: gl.slice().sort((a, b) => a - b)[gl.length >> 1], rss_mb_max: Math.max(...mem.filter(Boolean)), rss_mb: mem, ms_per_frame: msf, budget: bud, text: texts };
  fs.writeFileSync(OUT + '.log.json', JSON.stringify(log));
  console.log(JSON.stringify({ frames: log.frames, s_per_frame: log.s_per_frame, gl_ms_median: log.gl_ms_median, rss_mb_max: log.rss_mb_max }));
})().catch((e) => { console.error(e); process.exit(1); });

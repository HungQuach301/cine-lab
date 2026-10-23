// TIEN-KY-T4 · driver dựng London (design/k2v/ldn/page.js) — Chromium headless llvmpipe, như scripts/k2tl/render.js (gl.js chọn + kiểm trình dựng).
//  node scripts/k2ldn/render_ldn.js --shot <shot.json> --out <thư mục> [--w 1280 --h 720] [--from 0 --to N] [--only 0,24] [--spp 4]
// shot.json: {fps, dur, keys:[{t, p:[E,N,h], l:[E,N,h], fov, year?, hour?, hod?}], spp, smokeSky}. Nội suy Catmull-Rom (vị trí, đích) + tuyến tính (fov, năm, giờ).
// Ra: <out>/%05d.jpg + <out>/log.json (s/khung, mặt trời, ma trận máy mỗi khung — dùng để chiếu bản đồ/tranh khắc khớp cùng góc).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn } = require('child_process'); const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../../design'), DATA = process.env.LDN_DATA || '/var/tmp/ldn';
const GLM = require('../k2tl/gl.js'), { gl: GL, flags } = GLM.pick();
const S = JSON.parse(fs.readFileSync(arg('shot'))); const W = +arg('w', S.W || 1280), H = +arg('h', S.H || 720), OUT = path.resolve(arg('out'));
const fps = S.fps || 24, N = Math.round((S.dur || 10) * fps);
function cr(p0, p1, p2, p3, t) { const t2 = t * t, t3 = t2 * t; return p1.map((_, i) => 0.5 * (2 * p1[i] + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2 + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3)); }
const ease = (t) => t * t * (3 - 2 * t);
function at(t) {
  const K = S.keys; if (t <= K[0].t) return K[0]; if (t >= K[K.length - 1].t) return K[K.length - 1];
  let i = 0; while (K[i + 1].t < t) i++; const a = K[i], b = K[i + 1]; let u = (t - a.t) / (b.t - a.t); const ue = S.easeKeys === false ? u : ease(u);
  const k0 = K[Math.max(0, i - 1)], k3 = K[Math.min(K.length - 1, i + 2)]; const um = S.smooth ? u : ue;
  const lin = (x, y) => (x == null ? y : y == null ? x : x + (y - x) * u);
  return { p: cr(k0.p, a.p, b.p, k3.p, um), l: cr(k0.l, a.l, b.l, k3.l, um), fov: lin(a.fov, b.fov), year: lin(a.year, b.year), hour: (a.hour == null || b.hour == null) ? (a.hour ?? -1) : lin(a.hour, b.hour), hod: lin(a.hod, b.hod),
    fire: a.fire, smoke: a.smoke, smokeSky: lin(a.smokeSky ?? S.smokeSky, b.smokeSky ?? S.smokeSky) };
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: [...flags, '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=12000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/ERROR: 0:|Shader Error/.test(t)) { console.error('[shader]', t.slice(0, 3000)); process.exit(7); } if (!/GPU stall|GL Driver|Automatic fallback|llvmpipe|Mesa/i.test(t)) console.error('[page]', t.slice(0, 300)); });
  const http = require('http');
  const srv = http.createServer((q, res) => { const u = decodeURIComponent(new URL(q.url, 'http://x').pathname);
    if (u === '/ldn.html') { res.writeHead(200, { 'content-type': 'text/html' }); return res.end('<!doctype html><meta charset=utf-8><body style="margin:0"><script type="module" src="/k2v/ldn/page.js"></script></body>'); }
    const p = u.startsWith('/data/') ? path.join(DATA, u.slice(6)) : path.join(ROOT, u); if (!fs.existsSync(p)) { res.writeHead(404); return res.end('nf'); }
    res.writeHead(200, { 'content-type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream' }); fs.createReadStream(p).pipe(res); });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r)); const PORT = srv.address().port;
  await page.goto(`http://127.0.0.1:${PORT}/ldn.html`); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const info = await page.evaluate(async (c) => await window.setup(c), { W, H, data: '/data/canh/', exposure: S.exposure || 1.0 });
  await GLM.assertRenderer(GL, info.renderer, browser); console.error('[info]', JSON.stringify(info));
  const only = (arg('only', '') || '').split(',').filter(Boolean).map(Number);
  const frames = only.length ? only : [...Array(+arg('to', N) - +arg('from', 0)).keys()].map((i) => i + +arg('from', 0));
  const ff = spawn('ffmpeg', ['-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-r', String(fps), '-i', '-', '-vf', 'vflip', '-q:v', '2', '-start_number', '0', path.join(OUT, 'tmp_%05d.jpg')]);
  const log = { renderer: info.renderer, W, H, shot: S, frames: [] }, t0 = Date.now();
  for (const f of frames) {
    const k = at(f / fps); const fr = { cam: { p: k.p, l: k.l, fov: k.fov }, year: k.year ?? 1666.6, hour: k.hour ?? -1, hod: k.hod, t: f / fps, n: f, spp: +arg('spp', S.spp || 4), fire: k.fire, smoke: k.smoke, smokeSky: k.smokeSky };
    const r = await page.evaluate(async (x) => await window.renderFrame(x), fr);
    const buf = Buffer.from(r.img, 'base64'); if (!ff.stdin.write(buf)) await new Promise((res) => ff.stdin.once('drain', res));
    delete r.img; log.frames.push(Object.assign({ f, year: fr.year, hour: fr.hour, cam: fr.cam }, r));
    if (frames.indexOf(f) % 12 === 0) console.error(`[ldn] ${f} ${((Date.now() - t0) / 1000 / (frames.indexOf(f) + 1)).toFixed(2)} s/khung · mặt trời ${r.sun_el.toFixed(1)}° · lửa ${r.fire.toFixed(0)}`);
  }
  ff.stdin.end(); await new Promise((res) => ff.on('close', res));
  frames.forEach((f, i) => { const a = path.join(OUT, 'tmp_' + String(i).padStart(5, '0') + '.jpg'); if (fs.existsSync(a)) fs.renameSync(a, path.join(OUT, String(f).padStart(5, '0') + '.jpg')); });
  log.s_per_frame = (Date.now() - t0) / 1000 / frames.length; fs.writeFileSync(path.join(OUT, 'log.json'), JSON.stringify(log));
  console.log(JSON.stringify({ frames: frames.length, s_per_frame: +log.s_per_frame.toFixed(2), renderer: info.renderer }));
  await browser.close(); srv.close();
})().catch((e) => { console.error(e); process.exit(1); });

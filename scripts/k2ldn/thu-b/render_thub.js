// THU-B-T4 · BẢN SAO scripts/k2ldn/render_look.js (sha256 9a5a3b88520c5298c4b18c0bcd99944c40cee7c822527d48473de55981f32875, không sửa tệp gốc) + --fac <json> nạp atlas vân nướng D2 (window.setFac của look3.js).
// LOOK-T4 · driver dựng look London (design/k2v/ldn/look.js) — Chromium headless llvmpipe; kế thừa render_ldn.js (tiền kỳ; không sửa tệp đó).
//  node scripts/k2ldn/render_look.js --shot <shot.json> --out <thư mục> [--w 1920 --h 1080] [--from 0 --to N] [--only 0,24] [--spp 16] [--png 1] [--page look2 --lk look2/] [--mask 1|2]
// (LOOK-T4-V2: --page chọn trang dựng design/k2v/ldn/<page>.js, mặc định look; --lk thư mục hình học trong $LDN_DATA; --mask 2 = mặt nạ mã công trình.)
// shot.json: {fps, dur, look:{…}, bake:{url, box}, keys:[{t, p:[E,N,h], l:[E,N,h], fov, year?, hour?, h40?, date?, tz?, leaf?, wind?, smokeSky?, look?}]}.
// Ra: <out>/%05d.jpg|png + log.json (s/khung, mặt trời, ma trận máy mỗi khung).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn } = require('child_process'); const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../../../design'), DATA = process.env.LDN_DATA || '/var/tmp/ldn';
const GLM = require('../../k2tl/gl.js'), { gl: GL, flags } = GLM.pick();
const S = JSON.parse(fs.readFileSync(arg('shot'))); const W = +arg('w', S.W || 1920), H = +arg('h', S.H || 1080), OUT = path.resolve(arg('out'));
const fps = S.fps || 24, N = Math.round((S.dur || 0.0417) * fps) || 1;
function cr(p0, p1, p2, p3, t) { const t2 = t * t, t3 = t2 * t; return p1.map((_, i) => 0.5 * (2 * p1[i] + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2 + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3)); }
const ease = (t) => t * t * (3 - 2 * t);
function at(t) {
  const K = S.keys; if (K.length === 1 || t <= K[0].t) return K[0]; if (t >= K[K.length - 1].t) return K[K.length - 1];
  let i = 0; while (K[i + 1].t < t) i++; const a = K[i], b = K[i + 1]; const u = (t - a.t) / (b.t - a.t); const um = S.easeKeys === false ? u : ease(u);
  const k0 = K[Math.max(0, i - 1)], k3 = K[Math.min(K.length - 1, i + 2)];
  const lin = (x, y) => (x == null ? y : y == null ? x : x + (y - x) * u);
  const o = Object.assign({}, a, { p: cr(k0.p, a.p, b.p, k3.p, um), l: cr(k0.l, a.l, b.l, k3.l, um), fov: lin(a.fov, b.fov), year: lin(a.year, b.year) });
  for (const k of ['hour', 'h40', 'smokeSky', 'leaf']) if (a[k] != null && b[k] != null) o[k] = lin(a[k], b[k]);
  if (a.date && b.date) o.date = a.date.map((v, j) => lin(v, b.date[j]));
  return o;
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: [...flags, '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=14000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/ERROR: 0:|Shader Error|THREE.WebGLProgram/.test(t)) { console.error('[shader]', t.slice(0, 4000)); process.exit(7); } if (!/GPU stall|GL Driver|Automatic fallback|llvmpipe|Mesa/i.test(t)) console.error('[page]', t.slice(0, 300)); });
  const http = require('http');
  const srv = http.createServer((q, res) => { const u = decodeURIComponent(new URL(q.url, 'http://x').pathname);
    if (u === '/look.html') { res.writeHead(200, { 'content-type': 'text/html' }); return res.end(`<!doctype html><meta charset=utf-8><body style="margin:0"><script type="module" src="/k2v/ldn/${arg('page', 'look')}.js"></script></body>`); }
    const p = u.startsWith('/data/') ? path.join(DATA, u.slice(6)) : path.join(ROOT, u); if (!fs.existsSync(p)) { res.writeHead(404); return res.end('nf'); }
    res.writeHead(200, { 'content-type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream' }); fs.createReadStream(p).pipe(res); });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r)); const PORT = srv.address().port;
  await page.goto(`http://127.0.0.1:${PORT}/look.html`); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const t_setup = Date.now();
  const info = await page.evaluate(async (c) => await window.setup(c), { W, H, data: '/data/', exposure: S.exposure, shadow: S.shadow, lk: arg('lk', 'look2/') });
  await GLM.assertRenderer(GL, info.renderer, browser); info.setup_s = (Date.now() - t_setup) / 1000; console.error('[info]', JSON.stringify(info));
  if (S.bake) info.bake = await page.evaluate(async (b) => await window.setBake(b.url, b.box), S.bake);
  if (arg('fac')) { const F = JSON.parse(fs.readFileSync(arg('fac'))); info.fac = await page.evaluate(async (F) => await window.setFac(F.fac_url, F.roof_url, F), F); }   /* THU-B: atlas vân nướng D2 */
  const only = (arg('only', '') || '').split(',').filter(Boolean).map(Number);
  const frames = only.length ? only : [...Array(+arg('to', N) - +arg('from', 0)).keys()].map((i) => i + +arg('from', 0));
  const EXT = arg('mask') || arg('png') ? '.png' : '.jpg';
  const ff = spawn('ffmpeg', ['-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-r', String(fps), '-i', '-', '-vf', 'vflip', ...(EXT === '.jpg' ? ['-q:v', '2'] : []), '-start_number', '0', path.join(OUT, 'tmp_%05d' + EXT)]);
  const log = { renderer: info.renderer, setup_s: info.setup_s, bake: info.bake, W, H, shot: S, frames: [] }, t0 = Date.now();
  for (const f of frames) {
    const k = at(f / fps); const look = Object.assign({}, S.look || {}, k.look || {});
    const fr = Object.assign({}, k, { cam: { p: k.p, l: k.l, fov: k.fov }, year: k.year ?? 1666.6, t: (S.t0 || 0) + f / fps, n: f, spp: +arg('spp', S.spp || 4), look, mask: arg('mask') ? +arg('mask') : false });
    delete fr.p; delete fr.l;
    const r = await page.evaluate(async (x) => await window.renderFrame(x), fr);
    const buf = Buffer.from(r.img, 'base64'); if (!ff.stdin.write(buf)) await new Promise((res) => ff.stdin.once('drain', res));
    delete r.img; log.frames.push(Object.assign({ f, year: fr.year, hour: fr.hour, h40: fr.h40, cam: fr.cam }, r));
    if (frames.indexOf(f) % 12 === 0) console.error(`[look] ${f} ${((Date.now() - t0) / 1000 / (frames.indexOf(f) + 1)).toFixed(2)} s/khung · mặt trời ${r.sun_el.toFixed(1)}° · lửa ${r.fire.toFixed(0)}`);
  }
  ff.stdin.end(); await new Promise((res) => ff.on('close', res));
  frames.forEach((f, i) => { const a = path.join(OUT, 'tmp_' + String(i).padStart(5, '0') + EXT); if (fs.existsSync(a)) fs.renameSync(a, path.join(OUT, String(f).padStart(5, '0') + EXT)); });
  log.s_per_frame = (Date.now() - t0) / 1000 / frames.length; fs.writeFileSync(path.join(OUT, 'log.json'), JSON.stringify(log));
  console.log(JSON.stringify({ frames: frames.length, s_per_frame: +log.s_per_frame.toFixed(2), setup_s: info.setup_s, renderer: info.renderer }));
  await browser.close(); srv.close();
})().catch((e) => { console.error(e); process.exit(1); });

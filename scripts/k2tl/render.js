// V5b-1 · driver dựng xương sống thời gian (design/k2v/tl/page.js) — Chromium headless, chỉ CPU (mã riêng, không sửa scripts/k2).
//  node scripts/k2tl/render.js --scene gib20 --pack gib --out <thư mục> [--w 1920 --h 1080] [--from 0 --to 480 | --only 0,120] [--tech '{"lod":true,...}']
//       [--measure 24] [--campath <tệp.json>] [--budget <tệp.json>] [--maskonly <tệp.json>]
// Ra: <out>/%05d.jpg + <out>/log.json (s/khung từng khung, ms GL, spp, LOD, ngân sách chữ, tương phản, RSS). Tất định: không Math.random trong cảnh.
// V5b-2a (GG1): trình dựng chọn bằng biến môi trường K2TL_GL = llvmpipe (MẶC ĐỊNH; Mesa llvmpipe qua ANGLE/EGL, ≈ 5× SwiftShader — GPU-RD §7)
//  | swiftshader (giữ được, khung vàng cũ). Mỗi lượt đọc UNMASKED_RENDERER thật và DỪNG (mã 6) nếu không đúng trình dựng yêu cầu
//  (cờ sai Chromium âm thầm rơi về SwiftShader — GPU-RD §3.2). Chuỗi renderer ghi vào MỌI log (log.json, campath, ngân sách chữ, mặt nạ).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../../design'), CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GL = process.env.K2TL_GL || 'llvmpipe';
const GLS = { llvmpipe: { flags: ['--use-gl=angle', '--use-angle=gl-egl'], want: /llvmpipe/i }, swiftshader: { flags: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'], want: /SwiftShader/i } };
if (!GLS[GL]) { console.error(`K2TL_GL không hợp lệ: ${GL} (llvmpipe | swiftshader)`); process.exit(2); }
const W = +arg('w', 1920), H = +arg('h', 1080), OUT = arg('out') ? path.resolve(arg('out')) : null;
const rssAll = () => { try { return Math.round(execSync("ps -C chrome-headless-shell -o rss=").toString().trim().split('\n').map(Number).reduce((a, b) => a + b, 0) / 1024); } catch { return null; } };
const rss = (pid) => { try { const o = execSync('ps -e -o pid=,ppid=,rss=').toString().trim().split('\n').map((l) => l.trim().split(/\s+/).map(Number));
  const k = new Set([pid]); let g = true; while (g) { g = false; for (const [p, pp] of o) if (k.has(pp) && !k.has(p)) { k.add(p); g = true; } } return Math.round(o.filter(([p]) => k.has(p)).reduce((a, [, , r]) => a + r, 0) / 1024); } catch { return null; } };
(async () => {
  if (OUT) fs.mkdirSync(OUT, { recursive: true });
  const flags = process.env.K2TL_GL_FLAGS ? JSON.parse(process.env.K2TL_GL_FLAGS) : GLS[GL].flags;   // chỉ để test cơ chế DỪNG (cờ sai → rơi trình dựng khác)
  const browser = await chromium.launch({ args: [...flags, '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=12000'] });
  const bpid = browser.process ? browser.process().pid : null;
  const page = await browser.newPage({ viewport: { width: 800, height: 600 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|VALIDATE_STATUS false|ERROR: 0:/.test(t)) { console.error('[page] LỖI SHADER — dừng', t.slice(0, 4000)); process.exit(7); }
    if (!/GPU stall|GL Driver|swiftshader|Automatic fallback|llvmpipe|Mesa/i.test(t)) console.error('[page]', t.slice(0, 400)); });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname);
    const p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : p.endsWith('.html') ? 'text/html' : 'application/octet-stream';
    if (u === '/tl.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"><script type="module" src="/k2v/tl/page.js"></script></body>' });
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/tl.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const pack = arg('pack', 'gib');
  const cfg = { W, H, scene: arg('scene', 'gib20'), pack: `/cache/scene/${pack}/pack/`, lut: '/cache/lut/' + arg('lut', 'k2-a-thep-lanh') + '.cube', lutMode: +arg('lutmode', 1), vib: +arg('vib', 0.35), look: JSON.parse(arg('look', '{}')), photo: '/cache/loc/ng_crop.jpg', tech: JSON.parse(arg('tech', '{}')), lutK: +arg('lutk', 1) };
  const tl0 = Date.now(); const info = await page.evaluate(async (c) => await window.setup(c), cfg); info.load_wall_s = (Date.now() - tl0) / 1000; info.rss_after_load_mb = rssAll();
  console.error('[info]', JSON.stringify(info));
  info.gl = GL; const RD = { renderer: info.renderer, gl: GL };
  if (!GLS[GL].want.test(info.renderer || '')) { console.error(`[gl] DỪNG: yêu cầu ${GL} nhưng trình dựng thật là "${info.renderer}"`); await browser.close(); process.exit(6); }
  console.error(`[gl] ${GL} · ${info.renderer}`);
  const tagRows = (rows) => rows.map((r) => Object.assign(r, RD));   // mảng (mỗi khung) → mỗi phần tử mang renderer (bộ kiểm đọc mảng)
  if (arg('campath')) { fs.writeFileSync(arg('campath'), JSON.stringify(Object.assign(await page.evaluate(() => window.camLog()), RD))); await browser.close(); return; }
  if (arg('budget')) { fs.writeFileSync(arg('budget'), JSON.stringify(tagRows(await page.evaluate(() => window.budgetAll())))); await browser.close(); return; }
  const only = (arg('only', '') || '').split(',').filter(Boolean).map(Number);
  const frames = only.length ? only : [...Array(+arg('to', info.N) - +arg('from', 0)).keys()].map((i) => i + +arg('from', 0));
  const OV = JSON.parse(arg('override', '[]'));   // [{year, cam:{p,l,fov}, spp, noText}] theo thứ tự --only
  const MEAS = +arg('measure', 24), log = { renderer: info.renderer, gl: GL, info, cfg, frames: [] }, t0 = Date.now(), mem = [];
  for (const f of frames) {
    if (arg('maskonly')) { const r = Object.assign({ f }, await page.evaluate(async ([f, ov]) => window.contentMask(f, ov), [f, OV[frames.indexOf(f)] || OV[0] || null])); log.frames.push(r); continue; }   // V5b-1b: đo mặt nạ nội dung ở LƯỢT RIÊNG (xen với dựng hình làm hỏng trạng thái bóng/terrain — lỗi phát hiện 16/10)
    const tf = Date.now(); const r = await page.evaluate(async ([f, m, ov]) => await window.renderFrame(f, m, ov), [f, f % MEAS === 0 || only.length > 0, OV[frames.indexOf(f)] || OV[0] || null]);
    if (OUT) fs.writeFileSync(path.join(OUT, String(f).padStart(5, '0') + '.jpg'), Buffer.from(r.img, 'base64')); delete r.img; r.wall_ms = Date.now() - tf;
    log.frames.push(r);
    if ((frames.indexOf(f)) % 24 === 0) { const m = rssAll(); mem.push(m); console.error(`[tl ${GL}] ${f} ${((Date.now() - t0) / 1000 / (frames.indexOf(f) + 1)).toFixed(2)} s/khung · gl ${r.gl_ms} ms · spp ${r.spp} · chữ ${r.budget.pct}% · rss ${m} MB`); }
    if (OUT && frames.indexOf(f) % 48 === 0) fs.writeFileSync(path.join(OUT, 'log.json'), JSON.stringify(log));
  }
  if (arg('maskonly')) { fs.writeFileSync(arg('maskonly'), JSON.stringify(tagRows(log.frames))); console.log(JSON.stringify(log.frames.map((r) => [r.f, r.content_pct, r.content_center_pct, r.fabric_pct, r.hero_pct]))); await browser.close(); return; }
  log.s_per_frame = +((Date.now() - t0) / 1000 / frames.length).toFixed(3); log.rss_mb_max = Math.max(...mem.filter(Boolean), 0); log.wall_s = (Date.now() - t0) / 1000;
  if (OUT) fs.writeFileSync(path.join(OUT, 'log.json'), JSON.stringify(log));
  console.log(JSON.stringify({ renderer: info.renderer, gl: GL, frames: frames.length, s_per_frame: log.s_per_frame, rss_mb_max: log.rss_mb_max, load_s: info.load_wall_s }));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

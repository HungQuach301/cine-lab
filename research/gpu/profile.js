// GPU-RD · hồ sơ đường dựng một khung của mô-đun xương sống thời gian (design/k2v/tl, nhánh v5b1b) — tách thời gian theo bước.
// Không sửa mã dựng: gắn đo bằng addInitScript (bọc drawImage/toDataURL/draw*) + đọc CPU từng tiến trình Chromium (/proc) + Chrome tracing.
//  node research/gpu/profile.js --root <checkout v5b1b> --only 470,175,300 --rep 2 --tech '{"spp":2}' --out <ra.json> [--trace <trace.json>] [--nofinish] [--save <thư mục khung JPG lượt cuối>]
//  Biến môi trường CINE_GL: swiftshader (mặc định, như render.js) | vulkan | egl | gl  → cờ Chromium tương ứng (dùng cho máy GPU).
// Mỗi khung ghi: tổng tường; JS+gửi lệnh GL (accumulate); gl.finish (chờ phần dựng còn lại); drawImage WebGL→2D (đọc lại/đồng bộ canvas);
// lớp chữ; toDataURL JPEG; chuyển base64 về Node + ghi; CPU-giây theo loại tiến trình (gpu-process = SwiftShader + giải mã lệnh; renderer = JS/V8/Skia 2D).
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path'), os = require('os');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes('--' + k);
const REPO = path.resolve(arg('root', path.resolve(__dirname, '../..')));
const ROOT = path.join(REPO, 'design'), CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const W = +arg('w', 1920), H = +arg('h', 1080);
const GL = process.env.CINE_GL || 'swiftshader';
const GLARGS = { swiftshader: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  vulkan: ['--use-angle=vulkan', '--enable-features=Vulkan', '--disable-vulkan-surface', '--enable-gpu-rasterization'],
  egl: ['--use-gl=angle', '--use-angle=gl-egl'], gl: ['--use-gl=angle', '--use-angle=gl'] }[GL];
const HZ = 100;   // CLK_TCK
function procs() {   // pid → {type, cpu_s}
  const out = {};
  for (const d of fs.readdirSync('/proc')) {
    if (!/^\d+$/.test(d)) continue;
    let cmd; try { cmd = fs.readFileSync(`/proc/${d}/cmdline`, 'utf8'); } catch { continue; }
    if (!/chrom/.test(cmd)) continue;
    const m = cmd.match(/--type=([a-z-]+)/), type = m ? (/--utility-sub-type=network/.test(cmd) ? 'network' : m[1]) : 'browser';
    try { const s = fs.readFileSync(`/proc/${d}/stat`, 'utf8').split(') ')[1].split(' '); out[d] = { type, cpu_s: (+s[11] + +s[12]) / HZ }; } catch {}
  }
  return out;
}
function cpuDelta(a, b) { const r = {}; for (const [p, v] of Object.entries(b)) { const d = v.cpu_s - (a[p] ? a[p].cpu_s : 0); r[v.type] = +((r[v.type] || 0) + d).toFixed(2); } return r; }
const INIT = (nofinish) => {
  const P = (window.__prof = { draws: 0, draw_ms: 0, finish_ms: 0, readback_ms: 0, encode_ms: 0, drawimg_n: 0, flush2d_ms: 0, getimg_ms: 0, encode_cpu_ms: 0 });
  const now = () => performance.now();
  for (const C of [WebGL2RenderingContext, WebGLRenderingContext]) for (const k of ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced', 'drawRangeElements']) {
    const o = C.prototype[k]; if (!o) continue;
    C.prototype[k] = function (...a) { const t = now(); const r = o.apply(this, a); P.draws++; P.draw_ms += now() - t; return r; };
  }
  const di = CanvasRenderingContext2D.prototype.drawImage;
  CanvasRenderingContext2D.prototype.drawImage = function (src, ...a) {
    if (src instanceof HTMLCanvasElement && !src.__is2d) {
      const gl = src.getContext('webgl2') || src.getContext('webgl');
      if (gl) { const t0 = now(); if (!nofinish) gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); const t1 = now();   /* gl.finish() trong Chrome không chặn (đo 16/10: 0 ms) → đọc 1 điểm ảnh để buộc chờ dựng xong */ const r = di.call(this, src, ...a); const t2 = now(); P.finish_ms += t1 - t0; P.readback_ms += t2 - t1; P.drawimg_n++; return r; }
    }
    return di.call(this, src, ...a);
  };
  const gc = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (t, ...a) { if (t === '2d') this.__is2d = true; return gc.call(this, t, ...a); };
  const td = HTMLCanvasElement.prototype.toDataURL;
  HTMLCanvasElement.prototype.toDataURL = function (...a) {
    if (this.__is2d && !nofinish) {   // tách: (1) xả lớp 2D (ghép ảnh WebGL + chữ) · (2) đọc lại đủ khung về CPU · (3) toDataURL thật · (4) mã hoá JPEG thuần CPU (canvas phần mềm, đo riêng, không tính vào tường)
      const g = this.getContext('2d'); let t = now(); g.getImageData(0, 0, 1, 1); P.flush2d_ms += now() - t;
      t = now(); const id = g.getImageData(0, 0, this.width, this.height); P.getimg_ms += now() - t;
      t = now(); const r = td.apply(this, a); P.encode_ms += now() - t;
      const sc = document.createElement('canvas'); sc.width = this.width; sc.height = this.height; const sg = sc.getContext('2d', { willReadFrequently: true }); sg.putImageData(id, 0, 0);
      t = now(); td.apply(sc, a); P.encode_cpu_ms += now() - t; return r;
    }
    const t = now(); const r = td.apply(this, a); P.encode_ms += now() - t; return r; };
};
(async () => {
  const browser = await chromium.launch({ args: [...GLARGS, '--ignore-gpu-blocklist', '--font-render-hinting=none', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=12000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 }, deviceScaleFactor: 1 });
  await page.addInitScript(INIT, has('nofinish'));
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver|swiftshader|Automatic fallback/i.test(t)) console.error('[page]', t.slice(0, 300)); });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname);
    const p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (u === '/tl.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"><script type="module" src="/k2v/tl/page.js"></script></body>' });
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/tl.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const renderer = await page.evaluate(() => { const c = document.createElement('canvas').getContext('webgl2'); const e = c.getExtension('WEBGL_debug_renderer_info'); return e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER); });
  console.error('[gl]', GL, renderer);
  const cfg = { W, H, scene: arg('scene', 'gib20'), pack: `/cache/scene/${arg('pack', 'gib')}/pack/`, lut: '/cache/lut/k2-a-thep-lanh.cube', lutMode: 1, vib: 0.35, look: {}, photo: '/cache/loc/ng_crop.jpg', tech: JSON.parse(arg('tech', '{"spp":2}')), lutK: 1 };
  const tl0 = Date.now(); const info = await page.evaluate(async (c) => await window.setup(c), cfg); info.load_wall_s = (Date.now() - tl0) / 1000;
  const frames = arg('only', '470,175,300').split(',').map(Number), REP = +arg('rep', 2), rows = [];
  const tracePath = arg('trace');
  for (let rep = 0; rep < REP; rep++) for (const f of frames) {
    const doTrace = tracePath && rep === REP - 1 && f === frames[0];
    if (doTrace) await browser.startTracing(page, { path: tracePath, categories: ['toplevel', 'gpu', 'v8', 'blink', 'cc', 'viz', 'disabled-by-default-gpu.service', 'disabled-by-default-devtools.timeline'] });
    await page.evaluate(() => { for (const k in window.__prof) window.__prof[k] = 0; });
    const c0 = procs(), tf = Date.now();
    const r = await page.evaluate(async ([f]) => { const t = performance.now(); const r = await window.renderFrame(f, false, null); r.page_ms = performance.now() - t; r.prof = Object.assign({}, window.__prof); r.b64_len = r.img.length; return r; }, [f]);
    const t_eval = Date.now() - tf;
    const tw = Date.now(); const buf = Buffer.from(r.img, 'base64'); fs.writeFileSync(arg('save') && rep === REP - 1 ? (fs.mkdirSync(arg('save'), { recursive: true }), path.join(arg('save'), String(f).padStart(5, '0') + '.jpg')) : path.join(os.tmpdir(), 'gpu-rd-frame.jpg'), buf); const write_ms = Date.now() - tw;
    const wall = Date.now() - tf - Math.round(r.prof.encode_cpu_ms + r.prof.getimg_ms),   /* trừ hai phép đo phụ (đọc lại đủ khung + mã hoá CPU riêng) */ cpu = cpuDelta(c0, procs());
    if (doTrace) await browser.stopTracing();
    const p = r.prof;
    const row = { f, rep, spp: r.spp, wall_ms: wall, page_ms: Math.round(r.page_ms), ipc_b64_ms: t_eval - Math.round(r.page_ms), write_ms,
      acc_js_submit_ms: r.ms.acc, out_ms: r.ms.out, finish_ms: Math.round(p.finish_ms), readback_ms: Math.round(p.readback_ms), overlay_ms: r.ms.overlay,
      flush2d_ms: Math.round(p.flush2d_ms), getimg_ms: Math.round(p.getimg_ms), encode_ms: Math.round(p.encode_ms), encode_cpu_only_ms: Math.round(p.encode_cpu_ms), draws: p.draws, draw_call_ms: Math.round(p.draw_ms), jpg_kb: Math.round(buf.length / 1024), cpu_s: cpu, traced: !!doTrace };
    rows.push(row); console.error(JSON.stringify(row));
  }
  const last = rows.filter((r) => r.rep === REP - 1 && !r.traced), mean = (k) => Math.round(last.reduce((a, r) => a + r[k], 0) / Math.max(1, last.length));
  const cpuMean = {}; for (const r of last) for (const [k, v] of Object.entries(r.cpu_s)) cpuMean[k] = +(((cpuMean[k] || 0) + v / last.length)).toFixed(2);
  const out = { when: new Date().toISOString(), gl: GL, renderer, nproc: os.cpus().length, cpu_model: os.cpus()[0].model, W, H, tech: cfg.tech, nofinish: has('nofinish'), info: { load_wall_s: info.load_wall_s, buildings: info.buildings, terrain_tris: info.terrain_tris, city_tris: info.city_tris },
    rows, mean_last_rep: Object.fromEntries(['wall_ms', 'page_ms', 'acc_js_submit_ms', 'out_ms', 'finish_ms', 'readback_ms', 'overlay_ms', 'flush2d_ms', 'getimg_ms', 'encode_ms', 'encode_cpu_only_ms', 'ipc_b64_ms', 'write_ms', 'draws', 'draw_call_ms'].map((k) => [k, mean(k)])), cpu_s_mean_last_rep: cpuMean };
  if (arg('out')) fs.writeFileSync(arg('out'), JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out.mean_last_rep), JSON.stringify(cpuMean));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

// Cine Lab · Cổng 7 THỬ MẶT (nhánh thu-mat, không merge) — driver render theo shot, dựa trên page.js của layout (cùng đường ống, cùng lớp vẽ).
// node design/cong7/thu-mat/frames.js --shot s22 --out <thư mục> [--dbg '{"thuMat":"v1"}'] [--all] [--frames 1440,1452] [--dai] [--mask] [--w 960 --h 540]
//   --all    : render trọn shot → <out>/<shot>.mp4 (x264 crf 14 như render_film.js, chưa phụ đề)
//   --dai    : các khung của dải kiểm mù (bước 0,5 s từ đầu shot) → <out>/<shot>_f<khung>.png
//   --frames : danh sách khung phim toàn cục (thay cho --dai)
//   --mask   : kèm mặt nạ DA MẶT nhìn thấy (bộ phận 'head' của Ida; mọi vật khác tô đen nhưng vẫn che) → <out>/<shot>_f<khung>_mask.png
// Ghi <out>/<shot>.timing.json: giây mỗi khung (render + finalize, không tính mặt nạ).
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn, spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes('--' + k);
const ROOT = path.resolve(__dirname, '../..');
const W = +arg('w', 960), H = +arg('h', 540), out = path.resolve(arg('out', 'out')), SHOT = arg('shot');
const dbg = JSON.parse(arg('dbg', '{}'));

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
  await page.route('http://cine.local/thu-mat.html', (route) => route.fulfill({ status: 200, contentType: 'text/html',
    body: '<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>' }));
  await page.goto('http://cine.local/thu-mat.html');
  await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 });
  return page;
}

// Mặt nạ da mặt: render lại cảnh (đã đặt trạng thái khung) bằng vật liệu phẳng: 'head' của Ida trắng, vật khác đen (vẫn ghi độ sâu).
const MASK_FN = () => {
  const { THREE, cur, renderer } = window.__cine, scene = cur.scene, ida = cur.named && cur.named.ida; if (!ida) return null;
  const inIda = (o) => { for (let q = o; q; q = q.parent) if (q === ida.root) return true; return false; };
  const white = new THREE.MeshBasicMaterial({ color: 0xffffff }), black = new THREE.MeshBasicMaterial({ color: 0x000000 });
  const saved = [], vis = [];
  scene.traverse((o) => {
    if (!(o.isMesh || o.isLine || o.isPoints || o.isSprite)) return;
    if (!o.isMesh || (o.material && (Array.isArray(o.material) ? o.material.some((m) => m.transparent) : o.material.transparent))) { vis.push([o, o.visible]); o.visible = false; return; }
    saved.push([o, o.material]); o.material = o.userData.part === 'head' && inIda(o) ? white : black; });
  const bg = scene.background, fog = scene.fog; scene.background = new THREE.Color(0); scene.fog = null;
  const w = renderer.domElement.width, h = renderer.domElement.height;
  const rt = new THREE.WebGLRenderTarget(w, h); const oldRT = renderer.getRenderTarget(), tm = renderer.toneMapping;
  renderer.toneMapping = THREE.NoToneMapping; renderer.setRenderTarget(rt); renderer.clear(); renderer.render(scene, cur.cam);
  const px = new Uint8Array(w * h * 4); renderer.readRenderTargetPixels(rt, 0, 0, w, h, px);
  renderer.setRenderTarget(oldRT); renderer.toneMapping = tm; rt.dispose();
  for (const [o, m] of saved) o.material = m; for (const [o, v] of vis) o.visible = v; scene.background = bg; scene.fog = fog;
  let s = ''; const CH = 0x8000; const m1 = new Uint8Array(w * h); for (let i = 0; i < w * h; i++) m1[i] = px[i * 4] > 127 ? 255 : 0;
  for (let i = 0; i < m1.length; i += CH) s += String.fromCharCode.apply(null, m1.subarray(i, i + CH));
  return { w, h, b64: btoa(s) };
};

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  const page = await newPage(browser);
  const a = Date.now();
  const r = await page.evaluate(async (cfg) => await window.setup(cfg), { W, H, shot: SHOT, nopaint: false, dbg });
  const setup_s = (Date.now() - a) / 1000;
  const f0 = Math.round(r.t0 * 24), f1 = Math.round(r.t1 * 24);
  const dai = []; for (let t = 0; t < (r.t1 - r.t0) - 1e-6; t += 0.5) dai.push(f0 + Math.round(t * 24));
  const pick = arg('frames') ? arg('frames').split(',').map(Number) : dai;
  const all = has('all'), todo = all ? Array.from({ length: f1 - f0 }, (_, i) => f0 + i) : pick;
  let ff = null;
  if (all) ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', '24', '-i', '-',
    '-vf', 'vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-tune', 'grain',
    '-g', '48', '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '24', path.join(out, `${SHOT}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
  const times = [];
  for (const f of todo) {
    const b = Date.now();
    await page.evaluate(async (f) => await window.renderFrame(f), f);
    const b64 = await page.evaluate((f) => window.finalize(f), f);
    times.push((Date.now() - b) / 1000);
    const buf = Buffer.from(b64, 'base64');
    if (ff && !ff.stdin.write(buf)) await new Promise((res) => ff.stdin.once('drain', res));
    if (pick.includes(f)) {
      spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', path.join(out, `${SHOT}_f${f}.png`)], { input: buf });
      if (has('mask')) { const m = await page.evaluate(MASK_FN);
        if (m) spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', `${m.w}x${m.h}`, '-i', '-', '-vf', 'vflip', '-frames:v', '1', path.join(out, `${SHOT}_f${f}_mask.png`)], { input: Buffer.from(m.b64, 'base64') }); }
    }
  }
  if (ff) { ff.stdin.end(); await new Promise((res) => ff.on('close', res)); }
  await browser.close();
  const mean = times.reduce((x, y) => x + y, 0) / times.length;
  const rec = { shot: SHOT, dbg, W, H, frames: todo.length, dai, setup_s, per_frame_s: { mean: +mean.toFixed(3), max: +Math.max(...times).toFixed(3) }, times };
  fs.writeFileSync(path.join(out, `${SHOT}.timing.json`), JSON.stringify(rec, null, 1));
  console.log(JSON.stringify({ shot: SHOT, frames: todo.length, per_frame_s: rec.per_frame_s, setup_s }));
})().catch((e) => { console.error(e); process.exit(1); });

// Phiên K (checks v1.5) — công cụ tham chiếu: mặt nạ BÓNG NHÂN VẬT cho P0 (RUN.md 3.1.1), từ CHÍNH trang render layout.
// Không sửa design/: page.js được phục vụ nguyên văn, chỉ nối thêm một dòng để lộ biến module (cur, renderer, THREE) cho công cụ.
// Mặt nạ = phần NHÌN THẤY của mọi lưới thuộc cây nhân vật (cur.named: thân, quần áo, tóc, mũ), trắng; mọi vật khác tô đen nhưng vẫn
// ghi độ sâu (che đúng như ảnh render, giữ mặt hiển thị FrontSide/BackSide/DoubleSide); vật trong suốt không thuộc nhân vật không che
// (cùng quy tắc exportC3 của page.js). Vật cầm tay KHÔNG tính (bỏ lưới có userData.prop hoặc tên chứa 'prop').
// node reports/checks-v1.5/dryrun/k_sil.js --design <thư mục design/> --out <X.parts> --frames 1980,2775 [--scale 1]
//   → <out>/sil/<khung 5 số>.png + <out>/sil.json {khung: đường dẫn}
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(arg('design')), OUT = path.resolve(arg('out')), scale = +arg('scale', 1);
const W = 960, H = 540;
const EXPOSE = '\nwindow.__k = () => ({ cur, renderer, THREE });\n';

async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const rel = decodeURIComponent(new URL(route.request().url()).pathname);
    if (rel === '/k-sil.html') return route.fulfill({ status: 200, contentType: 'text/html',
      body: '<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>' });
    const p = path.join(ROOT, rel);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'application/octet-stream';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    let body = fs.readFileSync(p);
    if (rel === '/cong5/layout/page.js') body = Buffer.concat([body, Buffer.from(EXPOSE)]);
    route.fulfill({ status: 200, contentType: type, body });
  });
  await page.goto('http://cine.local/k-sil.html');
  await page.waitForFunction(() => typeof window.setup === 'function' && typeof window.__k === 'function', null, { timeout: 60000 });
  return page;
}

async function silhouette(page, f, sc) {
  return page.evaluate(async ([f, sc, W, H]) => {
    window.stepFrame(f);
    const { cur, renderer, THREE } = window.__k();
    const named = Object.entries(cur.named || {}).filter(([, ch]) => ch && ch.root && ch.root.visible && ch.root.parent);
    const body = new Set(), who = {};
    for (const [n, ch] of named) ch.root.traverse((o) => {
      if (!o.isMesh) return;
      if (o.userData && (o.userData.prop || /prop/i.test(o.name || ''))) return;
      body.add(o); who[n] = (who[n] || 0) + 1;
    });
    cur.scene.updateMatrixWorld(true); cur.cam.updateMatrixWorld(true);
    const blacks = [THREE.FrontSide, THREE.BackSide, THREE.DoubleSide].map((sd) => new THREE.MeshBasicMaterial({ color: 0x000000, side: sd }));
    const white = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
    const save = [];
    cur.scene.traverse((o) => {
      if (o.isSprite || o.isPoints || o.isLine) { save.push([o, 'v', o.visible]); o.visible = false; return; }
      if (!o.isMesh) return; save.push([o, 'm', o.material]);
      const m0 = Array.isArray(o.material) ? o.material[0] : o.material;
      if (body.has(o)) { o.material = white; return; }
      if (m0 && (m0.transparent || m0.depthWrite === false || (m0.opacity ?? 1) < 1)) { save.push([o, 'v', o.visible]); o.visible = false; return; }
      o.material = blacks[m0 && m0.side != null ? m0.side : 0];
    });
    const bg = cur.scene.background, fog = cur.scene.fog; cur.scene.background = new THREE.Color(0); cur.scene.fog = null;
    const sm = renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate = false;
    const w = W * sc, h = H * sc, rt = new THREE.WebGLRenderTarget(w, h, { depthBuffer: true }), px = new Uint8Array(w * h * 4);
    renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(cur.scene, cur.cam);
    renderer.readRenderTargetPixels(rt, 0, 0, w, h, px); renderer.setRenderTarget(null); rt.dispose();
    renderer.shadowMap.autoUpdate = sm; cur.scene.background = bg; cur.scene.fog = fog;
    for (let i = save.length - 1; i >= 0; i--) { const [o, k, v] = save[i]; if (k === 'v') o.visible = v; else o.material = v; }
    const cv = new OffscreenCanvas(w, h), g = cv.getContext('2d'), img = g.createImageData(w, h), d32 = new Uint32Array(img.data.buffer);
    let n = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const on = px[((h - 1 - y) * w + x) * 4] >= 128; d32[y * w + x] = on ? 0xffffffff : 0x00000000; n += on; }
    g.putImageData(img, 0, 0); const ab = await (await cv.convertToBlob({ type: 'image/png' })).arrayBuffer();
    let bin = ''; const u8 = new Uint8Array(ab); for (let j = 0; j < u8.length; j += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(j, j + 0x8000));
    return { png: btoa(bin), px: n, who };
  }, [f, sc, W, H]);
}

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  let page = await newPage(browser); const list = await page.evaluate(() => window.listShots()); await page.close();
  const want = arg('frames').split(',').map(Number);
  fs.mkdirSync(path.join(OUT, 'sil'), { recursive: true });
  const map = fs.existsSync(path.join(OUT, 'sil.json')) ? JSON.parse(fs.readFileSync(path.join(OUT, 'sil.json'))) : {}, stat = [];
  for (const s of list) {
    const f0 = Math.round(s.t0 * 24), f1 = Math.round(s.t1 * 24), fl = want.filter((f) => f >= f0 && f < f1); if (!fl.length) continue;
    if (s.src && s.src !== 'new') { for (const f of fl) stat.push({ f, shot: s.id, skip: 'khung tái dùng v1' }); continue; }
    page = await newPage(browser); await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, shot: s.id });
    for (const f of fl) {
      const r = await silhouette(page, f, scale), rel = `sil/${String(f).padStart(5, '0')}.png`;
      fs.writeFileSync(path.join(OUT, rel), Buffer.from(r.png, 'base64')); map[String(f)] = rel;
      stat.push({ f, shot: s.id, px: r.px, who: r.who }); console.error(`${s.id} khung ${f}: ${r.px} px, ${JSON.stringify(r.who)}`);
    }
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'sil.json'), JSON.stringify(map, null, 1));
  console.log(JSON.stringify(stat));
})().catch((e) => { console.error(e); process.exit(1); });

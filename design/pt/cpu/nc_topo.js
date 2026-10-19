// NC-CPU · ALBEDO NỀN NHÌN THẲNG XUỐNG từ chính cảnh k2v (ncA: vân CC0 theo lớp phủ + vật liệu thủ tục + đường/vườn dán) → ảnh sRGB cho Blender
//  (cách B/C dùng CÙNG màu nền với cách A; nướng ánh sáng cũng dùng albedo này cho phần nảy).
//  NC_DESIGN=<thư mục design phục vụ trang> NC_SCRIPTS=<scripts/k2tl> node design/pt/cpu/nc_topo.js --scene ../nc/ncA --opt '<json>' --f <khung>
//      --box E0,N0,E1,N1 --res <m/px> --out <thư mục>   → <out>/topo_<i>_<j>.png (ô 2048 px, hàng 0 = bắc) + <out>/topo.json
//  Máy trực giao đặt ở 900 m trên tâm ô (vật liệu "gần" của terrain.js bật ≤ 2,6 km), chỉ hiện địa hình + lớp dán (polygonOffset: đường, vườn, đường băng).
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = process.env.NC_DESIGN, SCR = process.env.NC_SCRIPTS, CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require(path.join(SCR, 'gl.js')), { gl: GL, flags: GLFLAGS } = GLM.pick();
(async () => {
  const OUT = path.resolve(arg('out')); fs.mkdirSync(OUT, { recursive: true });
  const box = arg('box').split(',').map(Number), res = +arg('res', 1), TILE = +arg('tile', 2048), F = +arg('f', 0);
  const browser = await chromium.launch({ args: [...GLFLAGS, '--ignore-gpu-blocklist', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=14000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|ERROR: 0:/.test(t)) { console.error('[page] LỖI SHADER', t.slice(0, 3000)); process.exit(7); } });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname), p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (u === '/tl.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"><script type="module" src="/k2v/tl/page.js"></script></body>' });
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p }); route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  await page.goto('http://cine.local/tl.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const cfg = { W: 640, H: 360, scene: arg('scene'), pack: '/cache/scene/gib/pack/', lut: '/cache/lut/k2-a-thep-lanh.cube', lutMode: 1, look: {}, photo: '/cache/loc/ng_crop.jpg', tech: JSON.parse(arg('tech', '{"spp":1}')), lutK: 1, opt: JSON.parse(arg('opt', '{}')) };
  const info = await page.evaluate(async (c) => await window.setup(c), cfg); await GLM.assertRenderer(GL, info.renderer, browser);
  await page.evaluate(async (f) => { await window.renderFrame(f, false, { noText: true }); }, F);   // áp trạng thái khung (năm, lớp hiện/ẩn)
  const t0 = Date.now(), nx = Math.ceil((box[2] - box[0]) / res / TILE), ny = Math.ceil((box[3] - box[1]) / res / TILE), tiles = [];
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const e0 = box[0] + i * TILE * res, n1 = box[3] - j * TILE * res, w = Math.min(TILE, Math.round((box[2] - e0) / res)), h = Math.min(TILE, Math.round((n1 - box[1]) / res));
    const b64 = await page.evaluate(async ([e0, n1, w, h, res]) => {
      const { ctx } = globalThis.NC, T = ctx.THREE, R = ctx.R, sc = ctx.scene, U = ctx.U;
      const keep = []; sc.traverse((o) => { if (!(o.isMesh || o.isSprite || o.isPoints || o.isLine)) return; let inT = false; for (let p = o; p; p = p.parent) if (p === ctx.terr.group) inT = true;
        const m = [].concat(o.material || [])[0], dec = m && m.polygonOffset && !o.isInstancedMesh; if (!(inT || dec) && o.visible) { keep.push(o); o.visible = false; } });
      const ce = e0 + w * res / 2, cn = n1 - h * res / 2, cam = new T.OrthographicCamera(-w * res / 2, w * res / 2, h * res / 2, -h * res / 2, 10, 5000);
      cam.position.set(ce, 900, -cn); cam.up.set(0, 0, -1); cam.lookAt(ce, 0, -cn); cam.updateMatrixWorld(); cam.updateProjectionMatrix(); ctx.terr.update(cam);
      const fog = sc.fog, sm = R.shadowMap.enabled; sc.fog = null; R.shadowMap.enabled = false; U.uMask.value = 3;
      const rt = new T.WebGLRenderTarget(w, h, { type: T.FloatType }); R.setRenderTarget(rt); R.setClearColor(0x000000, 0); R.clear(); R.render(sc, cam);
      const px = new Float32Array(w * h * 4); R.readRenderTargetPixels(rt, 0, 0, w, h, px); R.setRenderTarget(null); rt.dispose();
      U.uMask.value = 0; sc.fog = fog; R.shadowMap.enabled = sm; for (const o of keep) o.visible = true;
      const cv = new OffscreenCanvas(w, h), g = cv.getContext('2d'), id = g.createImageData(w, h), s = (v) => Math.round(255 * Math.pow(Math.min(1, Math.max(0, v)), 1 / 2.2));
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const a = ((h - 1 - y) * w + x) * 4, b = (y * w + x) * 4; id.data[b] = s(px[a]); id.data[b + 1] = s(px[a + 1]); id.data[b + 2] = s(px[a + 2]); id.data[b + 3] = px[a + 3] > 0 ? 255 : 0; }
      g.putImageData(id, 0, 0); const bl = await cv.convertToBlob({ type: 'image/png' }), ab = new Uint8Array(await bl.arrayBuffer()); let str = ''; for (let k = 0; k < ab.length; k += 0x8000) str += String.fromCharCode.apply(null, ab.subarray(k, k + 0x8000)); return btoa(str);
    }, [e0, n1, w, h, res]);
    const fn = `topo_${i}_${j}.png`; fs.writeFileSync(path.join(OUT, fn), Buffer.from(b64, 'base64')); tiles.push({ i, j, file: fn, e0, n1, w, h });
  }
  fs.writeFileSync(path.join(OUT, 'topo.json'), JSON.stringify({ box, res, TILE, nx, ny, tiles, scene: cfg.scene, f: F, renderer: info.renderer, s: (Date.now() - t0) / 1000, ghi_chu: 'albedo tuyến tính → sRGB (mũ 1/2,2); hàng 0 = bắc; alpha 0 = không có nền' }));
  console.log(JSON.stringify({ tiles: tiles.length, s: (Date.now() - t0) / 1000 }));
  await browser.close();
})();

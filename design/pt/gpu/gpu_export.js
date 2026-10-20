// NC-GPU · XUẤT CẢNH k2v → Blender cho Cycles GPU — dựa trên design/pt/cpu/nc_export.js (NC-CPU), thêm (a) MÀU VẬT LIỆU mỗi vật (m.color/emissive/opacity: lều, mái bằng, vật không có màu đỉnh),
//  (b) KHÓI/LỬA của k2v (smokeV6: mọi cụm khói/lửa đang hiện ở khung, vị trí thế giới + cỡ + alpha + loại) → fx.json, (c) --probe: liệt kê vật trong suốt/sprite/điểm mà bản xuất bỏ qua.
//  export6.js của V7B KHÔNG bị sửa: trang nhận bản vá khi phục vụ (thay một dòng `rec.side = …` bằng `rec.side = …; rec.mc = …`).
//  (1) trang phục vụ từ NC_DESIGN (cây design của nhánh V7B + design/k2v/tl/nc), (2) gọi NC.post.exportPrep() trước khi gom (ẩn trên CPU các bụi mà shader ẩn theo năm),
//  (3) --nopass: bỏ 3 lượt albedo/nosmoke/smoke (chỉ cần hình học + máy + nắng cho cảnh Blender đứng riêng).
//  NC_DESIGN=… NC_SCRIPTS=… node design/pt/cpu/nc_export.js --scene ../nc/ncA --opt '<json>' --f <khung> --far 6000 --out <thư mục> [--nopass] [--cam '{"p":[E,cao,N],"l":[E,cao,N],"fov":40}']
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const MODE = 'export', ROOT = process.env.NC_DESIGN, CACHE = process.env.K2TL_CACHE || '/var/tmp/cine-out/k2tl-cache';
const GLM = require(path.join(process.env.NC_SCRIPTS, 'gl.js')), { gl: GL, flags: GLFLAGS } = GLM.pick();
const W = +arg('w', 1920), H = +arg('h', 1080), F = +arg('f', 0), OUT = path.resolve(arg('out'));
(async () => {
  const browser = await chromium.launch({ args: [...GLFLAGS, '--ignore-gpu-blocklist', '--force-color-profile=srgb', '--js-flags=--max-old-space-size=14000'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (/Shader Error|ERROR: 0:/.test(t)) { console.error('[page] LỖI SHADER', t.slice(0, 3000)); process.exit(7); } });
  await page.route('http://cine.local/**', (route) => {
    const u = decodeURIComponent(new URL(route.request().url()).pathname), p = u.startsWith('/cache/') ? path.join(CACHE, u.slice(7)) : path.join(ROOT, u);
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'application/octet-stream';
    if (u === '/tl.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><meta charset=utf-8><body style="margin:0;background:#000"><script type="module" src="/k2v/tl/page.js"></script></body>' });
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    let body = fs.readFileSync(p);
    if (u.endsWith('/k2v/tl/export6.js')) { const s0 = body.toString(), A = 'rec.side = m.side === THREE.DoubleSide ? 2 : 0;';
      if (!s0.includes(A)) { console.error('LỖI: export6.js đổi — không vá được'); process.exit(8); }
      body = Buffer.from(s0.replace(A, A + " rec.mc = m.color ? m.color.toArray() : null; rec.me = m.emissive ? m.emissive.toArray().concat([m.emissiveIntensity ?? 1]) : null; rec.mo = m.opacity ?? 1; rec.mt = m.type; rec.mk = (m.customProgramCacheKey ? m.customProgramCacheKey() : '').slice(0, 24); rec.on = (o.name || '') + '|' + (o.parent && o.parent.name || ''); if (m.map && m.map.image && m.map.image.toDataURL && g.attributes.uv) { rec.map = m.map.image.toDataURL('image/png'); BUF.push(new Float32Array(g.attributes.uv.array)); rec.buf.UV = BUF.length - 1; }")); }
    route.fulfill({ status: 200, contentType: type, body });
  });
  await page.goto('http://cine.local/tl.html'); await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const cfg = { W, H, scene: arg('scene'), pack: '/cache/scene/gib/pack/', lut: '/cache/lut/k2-a-thep-lanh.cube', lutMode: 1, look: {}, photo: '/cache/loc/ng_crop.jpg', tech: JSON.parse(arg('tech', '{}')), lutK: 1, opt: JSON.parse(arg('opt', '{}')) };
  const info = await page.evaluate(async (c) => await window.setup(c), cfg); await GLM.assertRenderer(GL, info.renderer, browser);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const t0 = Date.now();
  if (arg('lightfx')) {   // CHỈ trạng thái mỗi khung (không hình học): khói/lửa smokeV6 + nắng/ánh trời k2v → <out>/<khung>.json (cú lặn: đổi ánh sáng TỪNG khung, nội suy không cần)
    const [a, b] = arg('lightfx').split(':').map(Number); fs.mkdirSync(OUT, { recursive: true });
    for (let f = a; f < b; f++) {
      await page.evaluate(async (f) => { await window.renderFrame(f, false, { noText: true }); }, f);
      const st = await page.evaluate(() => { const { ctx } = globalThis.NC, puffs = [];
        ctx.scene.traverse((o) => { const g = o.geometry; if (g && g.attributes && g.attributes.iP && g.attributes.iA) { const n = g.instanceCount || 0, P = g.attributes.iP.array, A = g.attributes.iA.array;
          for (let i = 0; i < n; i++) puffs.push([P[i * 4], P[i * 4 + 1], -P[i * 4 + 2], P[i * 4 + 3], A[i * 4], A[i * 4 + 1], A[i * 4 + 2], A[i * 4 + 3]]); } });
        return { puffs, sun: { dir: ctx.sunDir.toArray(), color: ctx.sun.color.toArray(), intensity: ctx.sun.intensity }, hemi: { sky: ctx.hemi.color.toArray(), ground: ctx.hemi.groundColor.toArray(), intensity: ctx.hemi.intensity },
          year: ctx.U.uYear ? ctx.U.uYear.value : null, night: ctx.U.uNight ? ctx.U.uNight.value : null }; });
      fs.writeFileSync(path.join(OUT, String(f).padStart(5, '0') + '.json'), JSON.stringify(st)); }
    console.log(JSON.stringify({ lightfx: [a, b], s: (Date.now() - t0) / 1000 })); await browser.close(); return; }
  if (MODE === 'export') {
    fs.mkdirSync(OUT, { recursive: true });
    const r = await page.evaluate(async (f) => { const r = await window.renderFrame(f, false, { noText: true }); return { img: r.img }; }, F);   // áp trạng thái khung + khung sạch k2v
    fs.writeFileSync(path.join(OUT, 'clean.jpg'), Buffer.from(r.img, 'base64'));
    if (arg('cam')) await page.evaluate((c) => { const { ctx } = globalThis.NC, cam = ctx.cam; cam.position.set(c.p[0], c.p[1], -c.p[2]); cam.lookAt(c.l[0], c.l[1], -c.l[2]); cam.fov = c.fov || cam.fov; cam.updateProjectionMatrix(); cam.updateMatrixWorld(); }, JSON.parse(arg('cam')));
    const hid = await page.evaluate(() => (globalThis.NC && globalThis.NC.post.exportPrep ? globalThis.NC.post.exportPrep() : 0));
    const man = await page.evaluate(async (o) => await window.exportFrame(o), { far: +arg('far', 6000) }); man.bui_an = hid;
    // KHÓI/LỬA k2v ở khung này: mọi lưới instanced có thuộc tính iP/iA (smokeV6) → [E, cao, N, cỡ, alpha, tuổi, loại 0 khói/1 lửa/2 khói đen, hạt]
    const fx = await page.evaluate(() => { const { ctx } = globalThis.NC, out = [], other = [];
      ctx.scene.traverse((o) => { const g = o.geometry, vis = (() => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; })();
        if (g && g.attributes && g.attributes.iP && g.attributes.iA) { const n = g.instanceCount || 0, P = g.attributes.iP.array, A = g.attributes.iA.array;
          for (let i = 0; i < n; i++) out.push([P[i * 4], P[i * 4 + 1], -P[i * 4 + 2], P[i * 4 + 3], A[i * 4], A[i * 4 + 1], A[i * 4 + 2], A[i * 4 + 3]]); return; }
        if (!vis) return; const m = [].concat(o.material || [])[0];
        if (o.isSprite || o.isPoints || (m && (m.isRawShaderMaterial || (m.transparent && !m.depthWrite)))) { const wp = new ctx.THREE.Vector3(); o.getWorldPosition(wp);
          other.push({ name: o.name, type: o.type, mat: m ? m.type : null, key: m && m.customProgramCacheKey ? m.customProgramCacheKey().slice(0, 30) : '', n: o.count || (g && g.instanceCount) || (g && g.attributes.position ? g.attributes.position.count : 0), at: [wp.x, wp.y, -wp.z], col: m && m.color ? m.color.toArray() : null }); } });
      return { puffs: out, other }; });
    fs.writeFileSync(path.join(OUT, 'fx.json'), JSON.stringify(fx)); man.fx = { puffs: fx.puffs.length, other: fx.other.length };
    const bufs = []; for (let i = 0; i < man.nbuf; i++) { const b = await page.evaluate((i) => window.exportBuf(i), i); fs.writeFileSync(path.join(OUT, `b${i}.bin`), Buffer.from(b.b64, 'base64')); bufs.push({ type: b.type, n: b.n }); }
    man.bufs = bufs; man.scene = cfg.scene; man.f = F; man.renderer = info.renderer;
    if (!process.argv.includes('--nopass')) for (const pass of ['albedo', 'nosmoke', 'smoke']) { const b = await page.evaluate(async ([f, p]) => await window.passFrame(f, p), [F, pass]); fs.writeFileSync(path.join(OUT, pass + '.f32'), Buffer.from(b, 'base64')); }
    man.passes = { W, H, fmt: 'RGBA float32, hàng từ dưới lên', albedo: 'diffuseColor tuyến tính (uMask 3)', nosmoke: 'HDR tuyến tính trước tone (không khói, có SSAO)', smoke: 'HDR khói nhân alpha trên nền trong suốt, có che độ sâu' };
    man.export_s = (Date.now() - t0) / 1000; fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(man));
    console.log(JSON.stringify({ vat: man.objs.length, tam_giac: man.objs.reduce((a, o) => a + o.nt * (o.inst || 1), 0), MB: +(man.bytes / 1e6).toFixed(1), s: man.export_s }));
  }
  await browser.close();
})();

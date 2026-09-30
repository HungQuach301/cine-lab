// Phiên P — DÒ CỘT ĐÈN ĐIỆN TRONG KHUNG (chủ dự án 30/09/2026: cột điện luôn ở mé đường đối diện dãy đèn khí; cảnh 1:03–1:05 không cho cột điện vào khung).
// Với mỗi shot × 3 khung (đầu, giữa, cuối — như --probe), tìm mọi cột điện (street.js electricLamp: thân trụ r 0,085/0,11, cao ≥ 4 m) và mọi cột đèn khí
// (props.js buildGasLamp: userData.flame), chiếu 9 điểm dọc thân vào máy; điểm "thấy" = trong khung và tia máy → điểm không vướng vật đục khác.
// In JSON mỗi dòng: {shot, f, posts:[{world:[x,z], seen:n/9, uv:[u,v]}], gas:[...]}. Chỉ đọc cảnh, không ghi gì vào repo.
// Dùng: node scripts/p/do_cot_dien.js [--only s26,s27] > ra.jsonl
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../../design');
async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    let body = fs.readFileSync(p);
    // móc gỡ lỗi CHỈ trong bản phục vụ cho trình duyệt (không sửa page.js trên đĩa — page.js là tệp cảnh trong kiểm toán C3)
    if (p.endsWith('/cong5/layout/page.js')) body = Buffer.concat([body, Buffer.from('\nwindow.__cur = () => ({ scene: cur.scene, cam: cur.cam }); window.__THREE = THREE;\n')]);
    route.fulfill({ status: 200, contentType: type, body });
  });
  const pageFile = path.join(ROOT, `cong5/layout/page-cot-${process.pid}.html`);
  fs.writeFileSync(pageFile, `<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>`);
  await page.goto(`http://cine.local/cong5/layout/${path.basename(pageFile)}`);
  await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 }); fs.unlinkSync(pageFile);
  return page;
}
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  let page = await newPage(browser); const list = await page.evaluate(() => window.listShots()); await page.close();
  const only = arg('only') ? arg('only').split(',') : null;
  for (const s of list) {
    if (only && !only.includes(s.id)) continue; if (s.src !== 'new') { console.log(JSON.stringify({ shot: s.id, skip: s.src })); continue; }
    const f0 = Math.round(s.t0 * 24), f1 = Math.round(s.t1 * 24);
    page = await newPage(browser); await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W: 960, H: 540, shot: s.id });
    for (const f of [f0, (f0 + f1) >> 1, f1 - 1]) {
      const r = await page.evaluate((f) => {
        window.stepFrame(f); const { scene, cam } = window.__cur();
        const THREE = window.__THREE; scene.updateMatrixWorld(true); cam.updateMatrixWorld(true);
        const posts = [], gas = [], ray = new THREE.Raycaster(), cp = cam.getWorldPosition(new THREE.Vector3());
        const vis = (o) => { let v = o.visible; for (let p = o.parent; p; p = p.parent) v = v && p.visible; return v; };
        const occl = []; scene.traverse((o) => { if (o.isMesh && vis(o)) { const m = Array.isArray(o.material) ? o.material[0] : o.material; if (!(m && (m.transparent || m.depthWrite === false))) occl.push(o); } });
        const test = (obj, y0, y1) => { let n = 0, uv = null; const b = new THREE.Vector3();
          for (let i = 0; i < 9; i++) { const w = obj.localToWorld(new THREE.Vector3(0, y0 + (y1 - y0) * i / 8, 0)); const q = w.clone().project(cam);
            if (q.z < -1 || q.z > 1 || Math.abs(q.x) > 1 || Math.abs(q.y) > 1) continue;
            const d = w.clone().sub(cp), L = d.length(); ray.set(cp, d.normalize()); ray.far = L - 0.25; const hit = ray.intersectObjects(occl, false).find((h) => { let p = h.object; while (p) { if (p === obj) return false; p = p.parent; } return true; });
            if (!hit) { n++; uv = [+((q.x + 1) / 2).toFixed(3), +((1 - q.y) / 2).toFixed(3)]; } }
          return { n, uv }; };
        scene.traverse((o) => {
          if (o.isMesh && o.geometry && o.geometry.type === 'CylinderGeometry') { const p = o.geometry.parameters;
            if (Math.abs(p.radiusTop - 0.085) < 1e-3 && Math.abs(p.radiusBottom - 0.11) < 1e-3 && p.height >= 4 && vis(o)) { const g = o.parent, w = g.getWorldPosition(new THREE.Vector3());
              const t = test(g, 0.3, 6.0); posts.push({ world: [+w.x.toFixed(2), +w.z.toFixed(2)], seen: t.n, uv: t.uv }); } }
          if (o.userData && o.userData.flame && vis(o)) { const w = o.getWorldPosition(new THREE.Vector3()); const t = test(o, 0.3, 3.3); gas.push({ world: [+w.x.toFixed(2), +w.z.toFixed(2)], seen: t.n, uv: t.uv }); } });
        return { posts: posts.filter((p) => p.seen > 0), gas: gas.filter((p) => p.seen > 0) };
      }, f);
      console.log(JSON.stringify({ shot: s.id, f, ...r }));
    }
    await page.close();
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

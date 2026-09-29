// checks v1.5 (RUN.md 3.6.3): xuất BÓNG MỌI NHÂN VẬT (`silhouettes`) cho mọi khung P0 lấy mẫu có nhân vật, từ CHÍNH trang render (page.js, window.exportSil).
// node design/cong5/layout/export_sil.js --parts-dir <X.parts> --text <X.text> [--scale 1]
//   → <X.parts>/sil/<khung 5 số>.png + khoá "silhouettes" trong <X.parts>/parts.json (chạy SAU export_c3.js, vì export_c3 ghi lại parts.json)
// node design/cong5/layout/export_sil.js --audit-dir <X.audit/rerender> --frames 1980[,…] [--scale 1]  → <khung 5 số>/silhouette.png (mục 3.7)
// Khung P0 lấy mẫu (RUN.md 3.6.3): 0, b, 2b, … và khung cuối; b = 12 nếu ⌊n/12⌋ ≤ 240, còn không b = ⌈n/240⌉; cộng khung giữa mỗi phần tử chữ.
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../..');
const W = 960, H = 540, scale = +arg('scale', 1), auditDir = arg('audit-dir', null), pdir = path.resolve(auditDir || arg('parts-dir'));
async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pageFile = path.join(ROOT, `cong5/layout/page-sil-${process.pid}.html`);
  fs.writeFileSync(pageFile, `<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>`);
  await page.goto(`http://cine.local/cong5/layout/${path.basename(pageFile)}`);
  await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 }); fs.unlinkSync(pageFile);
  return page;
}
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  let page = await newPage(browser); const list = await page.evaluate(() => window.listShots()); await page.close();
  const n = Math.round(Math.max(...list.map((s) => s.t1)) * 24);
  let want;
  if (arg('frames')) want = arg('frames').split(',').map(Number);
  else {
    const b = Math.floor(n / 12) <= 240 ? 12 : Math.ceil(n / 240), set = new Set();
    for (let f = 0; f < n; f += b) set.add(f); set.add(n - 1);
    const tj = path.join(path.resolve(arg('text')), 'elements.json');
    if (fs.existsSync(tj)) for (const e of JSON.parse(fs.readFileSync(tj)).elements) set.add(Math.floor((e.first_frame + e.last_frame) / 2));
    want = [...set].sort((a, c) => a - c);
  }
  fs.mkdirSync(pdir, { recursive: true });
  const map = {}, stat = [];
  for (const s of list) {
    const f0 = Math.round(s.t0 * 24), f1 = Math.round(s.t1 * 24), fl = want.filter((f) => f >= f0 && f < f1); if (!fl.length) continue;
    page = await newPage(browser); await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, shot: s.id });
    for (const f of fl) {
      const r = await page.evaluate(async ([f, sc]) => await window.exportSil(f, sc), [f, scale]);
      stat.push({ f, shot: s.id, px: r.px, who: r.who });
      if (!r.px && !auditDir) continue;   // khung không có nhân vật nhìn thấy: không cần bóng
      const rel = auditDir ? path.join(String(f).padStart(5, '0'), 'silhouette.png') : `sil/${String(f).padStart(5, '0')}.png`;
      fs.mkdirSync(path.dirname(path.join(pdir, rel)), { recursive: true });
      fs.writeFileSync(path.join(pdir, rel), Buffer.from(r.png, 'base64')); if (!auditDir) map[String(f)] = rel;
      console.error(`${s.id} khung ${f}: ${r.px} px ${JSON.stringify(r.who)}`);
    }
    await page.close();
  }
  await browser.close();
  if (!auditDir) {
    const pj = path.join(pdir, 'parts.json'), P = JSON.parse(fs.readFileSync(pj));
    P.silhouettes = map; fs.writeFileSync(pj, JSON.stringify(P, null, 1));
  }
  fs.writeFileSync(path.join(pdir, auditDir ? 'sil_rerender_stat.json' : 'sil_stat.json'), JSON.stringify({ frames_sampled: want.length, with_char: Object.keys(map).length, stat }, null, 1));
  console.log(JSON.stringify({ sampled: want.length, written: auditDir ? want.length : Object.keys(map).length }));
})().catch((e) => { console.error(e); process.exit(1); });

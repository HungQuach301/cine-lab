// Xuất mặt nạ C3 + views (RUN.md 3.6, 3.6.2, v1.4) cho ANIMATIC, từ CHÍNH trang render (page.js + film.js), nhân vật Ida.
// node design/cong5/layout/export_c3.js --parts-dir <X.parts> [--scale 4] [--frames 0,12,...]  → <X.parts>/parts.json + <khung 5 số>/<bộ phận>.png
// node design/cong5/layout/export_c3.js --audit-dir <X.audit/rerender> --frames 1236[,…] [--scale 4]  → render lại khung được chọn (mục 3.7 bước 4)
// Mọi khung chia hết cho 12 của phim đều có mục; khung Ida không hiện (shot không có Ida hoặc Ida ẩn): mặt nạ rỗng (đầu rỗng).
// Shot 'v1:' (tái dùng khung v1): không còn nhân vật Ida trong khung (s01 thành phố, s43 thành phố, s48 phòng Cas) → mặt nạ rỗng.
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = path.resolve(__dirname, '../..');
const W = 960, H = 540, scale = +arg('scale', 4), auditDir = arg('audit-dir', null), pdir = path.resolve(auditDir || arg('parts-dir'));
const KEYS = ['head', 'torso', 'upper_arm', 'forearm', 'thigh', 'shin'];
// Khung Ida không có trong khung: mọi bộ phận khai che hoàn toàn (hidden = 1) → máy tính là không đo được; góc không có nghĩa (ghi 0).
const EMPTY_VIEW = { view_deg: 0, elev_deg: 0, parts: Object.fromEntries(KEYS.map((k) => [k, { foreshorten: 1, hidden: 1, depth: 1 }])) };

function emptyPng(w, h) {   // PNG RGBA toàn trong suốt, cùng kích thước mặt nạ thật
  const crc = (b) => { let c, t = []; for (let n = 0; n < 256; n++) { c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    let x = 0xffffffff; for (const v of b) x = t[(x ^ v) & 0xff] ^ (x >>> 8); return (x ^ 0xffffffff) >>> 0; };
  const chunk = (ty, d) => { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(ty), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 6;
  const raw = Buffer.alloc((w * 4 + 1) * h); return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]);
}
async function newPage(browser) {
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pageFile = path.join(ROOT, `cong5/layout/page-c3-${process.pid}.html`);
  fs.writeFileSync(pageFile, `<!doctype html><html><body style="margin:0"><script type="module" src="/cong5/layout/page.js"></script></body></html>`);
  await page.goto(`http://cine.local/cong5/layout/${path.basename(pageFile)}`);
  await page.waitForFunction(() => typeof window.setup === 'function', null, { timeout: 60000 }); fs.unlinkSync(pageFile);
  return page;
}
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  let page = await newPage(browser); const list = await page.evaluate(() => window.listShots()); await page.close();
  const F = Math.round(list[list.length - 1].t1 * 24);
  const want = arg('frames') ? arg('frames').split(',').map(Number) : Array.from({ length: Math.ceil(F / 12) }, (_, i) => i * 12);
  fs.mkdirSync(pdir, { recursive: true });
  const empty = emptyPng(W * scale, H * scale), frames = {}, views = {}, stat = [];
  for (const s of list) {
    const f0 = Math.round(s.t0 * 24), f1 = Math.round(s.t1 * 24), fl = want.filter((f) => f >= f0 && f < f1); if (!fl.length) continue;
    let has = false;
    if (s.src === 'new') { page = await newPage(browser); await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, shot: s.id }); has = await page.evaluate(() => window.hasChar('ida')); }
    for (const f of fl) {
      const fd = String(f).padStart(5, '0'); fs.mkdirSync(path.join(pdir, fd), { recursive: true }); frames[String(f)] = {};
      if (has) {
        const r = await page.evaluate(async ([f, sc]) => await window.exportC3(f, sc, 'ida', 'L'), [f, scale]);
        for (const k of KEYS) { fs.writeFileSync(path.join(pdir, fd, k + '.png'), Buffer.from(r.parts[k], 'base64')); frames[String(f)][k] = `${fd}/${k}.png`; }
        // bộ phận nằm sau mặt phẳng máy quay (depth ≤ 0, chỉ xảy ra ở insert rất gần như s09w, s46) thì không có mặt nạ: bỏ khỏi views (RUN.md 3.6.2 chỉ bắt buộc head + bộ phận có mặt nạ)
        for (const k of Object.keys(r.views.parts)) if (k !== 'head' && r.views.parts[k].depth <= 0 && r.count[k] === 0) { delete r.views.parts[k]; delete frames[String(f)][k]; fs.unlinkSync(path.join(pdir, fd, k + '.png')); }
        views[String(f)] = r.views; if (auditDir) fs.writeFileSync(path.join(pdir, fd, 'views.json'), JSON.stringify(r.views, null, 1));
        stat.push({ f, shot: s.id, count: r.count, view: r.views.view_deg }); console.error(`${s.id} khung ${f}: đầu ${r.count.head} px, góc ${r.views.view_deg}°`);
      } else { for (const k of KEYS) { fs.writeFileSync(path.join(pdir, fd, k + '.png'), empty); frames[String(f)][k] = `${fd}/${k}.png`; }
        views[String(f)] = EMPTY_VIEW; if (auditDir) fs.writeFileSync(path.join(pdir, fd, 'views.json'), JSON.stringify(EMPTY_VIEW, null, 1));
        stat.push({ f, shot: s.id, empty: true }); }
    }
    if (s.src === 'new') await page.close();
  }
  await browser.close();
  if (!auditDir) fs.writeFileSync(path.join(pdir, 'parts.json'), JSON.stringify({ model_sheet: 'design/cong3/model-sheet/ida.json', scale, side: 'L', frames, views }, null, 1));
  fs.writeFileSync(path.join(pdir, auditDir ? 'rerender_stat.json' : '../c3_export_stat.json'), JSON.stringify(stat, null, 1));
  console.log(JSON.stringify({ frames: Object.keys(frames).length, with_ida: stat.filter((x) => !x.empty).length }));
})().catch((e) => { console.error(e); process.exit(1); });

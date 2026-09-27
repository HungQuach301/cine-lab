// Xuất file đi kèm cho checks/run.py từ CHÍNH trang render (cùng cảnh, cùng máy quay, cùng tư thế) — Cổng 3 v3, bước 9.
// node shared/export_sidecars.js --page v2/page.js --shot walk --video <X.mp4> [--parts 0,12,24,36] [--scale 4] [--who 0] [--side L]
//   [--motion 0:48] [--sheet design/cong3/model-sheet/ida.json] [--args '<json>'] [--only-parts] [--audit-dir <X.audit/rerender>]
// Ghi cạnh video: X.parts/parts.json + X.parts/<khung 5 số>/<bộ phận>.png ; X.motion.json ; X.text/elements.json (rỗng) ; X.script.txt (rỗng)
// Với --audit-dir: chỉ render lại mặt nạ các khung trong --parts vào <audit-dir>/<khung>/<bộ phận>.png (RUN.md 3.7, bước 4).
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const has = (k) => process.argv.includes('--' + k);
const ROOT = path.resolve(__dirname, '..'), REPO = path.resolve(ROOT, '../..');
const page_ = arg('page'), shot = arg('shot'), video = path.resolve(arg('video'));
const W = +arg('w', 1920), H = +arg('h', 1080), scale = +arg('scale', 4), who = +arg('who', 0), side = arg('side', 'L');
const partsF = (arg('parts', '') || '').split(',').filter((s) => s !== '').map(Number), motion = arg('motion', null);
const extra = JSON.parse(arg('args', '{}')), auditDir = arg('audit-dir', null);
const base = video.replace(/\.mp4$/, '');

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver/.test(t)) console.error('[page]', t); });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.route('http://cine.local/**', (route) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(p) });
  });
  const pageFile = path.join(ROOT, `page-x${process.pid}.html`);
  fs.writeFileSync(pageFile, `<!doctype html><html><body style="margin:0"><script type="module" src="/${page_}"></script></body></html>`);
  await page.goto(`http://cine.local/${path.basename(pageFile)}`);
  await page.waitForFunction(() => typeof window.setup === 'function' && typeof window.exportParts === 'function', null, { timeout: 60000 });
  await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W, H, shot, ...extra });
  const shotName = shot.split('@')[0];
  const log = {};
  if (partsF.length) {
    const pdir = auditDir ? path.resolve(auditDir) : base + '.parts'; fs.mkdirSync(pdir, { recursive: true });
    const frames = {}; let sheetId = null;
    for (const f of partsF) {
      const r = await page.evaluate(async ([n, s, o]) => await window.exportParts(n, s, o), [`${shotName}@${f}`, scale, { who, side }]);
      sheetId = r.sheet; const fd = String(f).padStart(5, '0'); fs.mkdirSync(path.join(pdir, fd), { recursive: true }); frames[String(f)] = {};
      for (const [k, b64] of Object.entries(r.parts)) { fs.writeFileSync(path.join(pdir, fd, k + '.png'), Buffer.from(b64, 'base64')); frames[String(f)][k] = `${fd}/${k}.png`; }
      log[f] = { size: [r.w, r.h], pixels: r.count, meshes: r.picked };
      console.error(`khung ${f}: ${r.w}×${r.h}`, JSON.stringify(r.count));
    }
    if (!auditDir) {
      const sheet = arg('sheet', sheetId && sheetId.startsWith('CHR-ida') ? 'design/cong3/model-sheet/ida.json' : 'design/cong3/model-sheet/cas.json');
      fs.writeFileSync(path.join(pdir, 'parts.json'), JSON.stringify({ model_sheet: sheet, scale, side, frames }, null, 1));
    }
  }
  if (motion && !auditDir) {
    const [a, b] = motion.split(':').map(Number);
    const m = await page.evaluate(async ([s, a, b, o]) => await window.exportMotion(s, a, b, o), [shotName, a, b, { who }]);
    fs.writeFileSync(base + '.motion.json', JSON.stringify(m));
  }
  if (!auditDir && !has('only-parts')) {
    fs.mkdirSync(base + '.text', { recursive: true });
    fs.writeFileSync(path.join(base + '.text', 'elements.json'), JSON.stringify({ elements: [] }));   // khung không có chữ (không tiêu đề, phụ đề, biển hiệu)
    fs.writeFileSync(base + '.script.txt', '');                                                       // đoạn không lời
  }
  await browser.close(); fs.unlinkSync(pageFile);
  console.log(JSON.stringify(log));
})().catch((e) => { console.error(e); process.exit(1); });

// KÊNH 2 · dựng THƯ VIỆN STICKER (phiên V2): design/k2v/sticker-lab.js (vật 3D, toon) + scripts/k2/lib/sticker.js (nhân vật A-lite, phong cách viền/bóng)
// → design/k2v/stickers/<tên>.png + stickers.json (SHA-256, nguồn mô hình) + tờ liên hợp channel-k2/k2v2-mau/stickers-sheet.jpg.
//   node scripts/k2/stickers_build.js [tên…]
// Mô hình của tập (design/ll-hero/k2g01.js, k2c106.js) nạp qua /ll-hero/<tệp>.js?rx=<hàm,…>: phục vụ nguyên văn + dòng `export {…}` — không sửa tệp tập.
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path'), crypto = require('crypto'), { spawnSync } = require('child_process');
const ROOT = path.resolve(__dirname, '../../design'), OUT = path.join(ROOT, 'k2v/stickers'), LIB = path.join(__dirname, 'lib/sticker.js');
const OBJ = ['furnace', 'factory', 'house', 'town', 'mine', 'ship', 'boat', 'coin', 'coins', 'document', 'bank', 'flag', 'wagon', 'sack', 'barrel', 'mountain'];
const SRC = { furnace: 'design/ll-hero/k2g01.js blastFurnace (K2G-01)', factory: 'design/ll-hero/k2g01.js shed (K2G-01) + ống khói mới', house: 'design/ll-hero/k2c106.js house (K2C-T1-06)', town: 'design/ll-hero/k2c106.js house ×3 (K2C-T1-06)' };
const ROLES = ['worker', 'merchant', 'banker', 'soldier', 'official', 'engineer', 'farmer', 'sailor'];
(async () => {
  fs.mkdirSync(OUT, { recursive: true }); const only = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; });
  page.on('console', (m) => { const t = m.text(); if (!/GPU stall|GL Driver|WebGLRenderer|swiftshader|willReadFrequently/i.test(t)) console.error('[page]', t); });
  await page.route('http://cine.local/**', (route) => {
    const U = new URL(route.request().url()), u = decodeURIComponent(U.pathname), p = path.join(ROOT, u);
    if (u === '/lab.html') return route.fulfill({ status: 200, contentType: 'text/html', body: `<!doctype html><html><body><script src="/stk.js"></script><script type="module" src="/k2v/sticker-lab.js"></script></body></html>` });
    if (u === '/stk.js') return route.fulfill({ status: 200, contentType: 'text/javascript', body: fs.readFileSync(LIB) });
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    let body = fs.readFileSync(p); const rx = U.searchParams.get('rx'); if (rx) body = Buffer.concat([body, Buffer.from(`\nexport { ${rx} };\n`)]);
    route.fulfill({ status: 200, contentType: p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream', body });
  });
  await page.goto('http://cine.local/lab.html'); await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  const man = fs.existsSync(path.join(OUT, 'stickers.json')) ? JSON.parse(fs.readFileSync(path.join(OUT, 'stickers.json'))) : {};
  const save = (name, url, meta) => { const buf = Buffer.from(url.split(',')[1], 'base64'), f = path.join(OUT, name + '.png'); fs.writeFileSync(f, buf);
    spawnSync('/opt/cine/bin/python', ['-c', `from PIL import Image;im=Image.open('${f}');im.save('${f}',optimize=True)`]);
    man[name] = { ...meta, sha256: crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') }; console.error('[stk]', name, fs.statSync(f).size, 'B'); };
  for (const n of OBJ) if (!only.length || only.includes(n)) save(n, await page.evaluate(async (n) => await window.renderIcon(n, 640), n), { kind: 'object', src: SRC[n] || 'design/k2v/sticker-lab.js (vật mới, tự dựng)' });
  for (const r of ROLES) if (!only.length || only.includes(r)) save('role-' + r, await page.evaluate((r) => window.renderChar({ role: r }, 420), r), { kind: 'character', src: 'scripts/k2/lib/sticker.js STK.char (vector, tự vẽ)' });
  man._note = 'Thư viện sticker K2V2 — tác phẩm tự dựng của dự án (mô hình three.js + vẽ vector), không dùng hình của bên thứ ba. Tạo lại: node scripts/k2/stickers_build.js';
  fs.writeFileSync(path.join(OUT, 'stickers.json'), JSON.stringify(man, null, 1));
  await browser.close();
})();

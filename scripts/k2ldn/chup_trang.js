// Chụp trang bằng chứng giấy phép: node chup_trang.js <thư mục licenses>  (đọc <id>.json → trang → <id>-trang.jpg + <id>-trang.html)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const dir = process.argv[2]; const only = process.argv.slice(3);
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 1600 }, userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 CineLab-research (+https://github.com/HungQuach301/cine-lab)' });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json'))) {
    const j = JSON.parse(fs.readFileSync(path.join(dir, f))); if (only.length && !only.includes(j.id)) continue;
    const p = await ctx.newPage();
    try {
      const r = await p.goto(j.trang, { waitUntil: 'networkidle', timeout: 90000 }).catch(e => null);
      await p.waitForTimeout(4000);
      const t = await p.title();
      await p.screenshot({ path: path.join(dir, j.id + '-trang.jpg'), type: 'jpeg', quality: 55, fullPage: false });
      fs.writeFileSync(path.join(dir, j.id + '-trang.html'), (await p.content()).slice(0, 400000));
      console.log(j.id, r ? r.status() : 'ERR', t);
    } catch (e) { console.log(j.id, 'LỖI', e.message); }
    await p.close();
  }
  await b.close();
})();

// Tải tệp qua Chromium thật (trang có Cloudflare chặn curl). node tai_trinh_duyet.js <url> <ra> [trang-mở-trước]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [url, out, pre] = process.argv.slice(2);
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 CineLab-research (+https://github.com/HungQuach301/cine-lab)' });
  const p = await ctx.newPage();
  if (pre) { await p.goto(pre, { waitUntil: 'networkidle', timeout: 90000 }).catch(e => console.error('pre', e.message)); await p.waitForTimeout(8000); }
  const r = await ctx.request.get(url, { timeout: 600000 });
  console.log(r.status(), r.headers()['content-type']);
  fs.writeFileSync(out, await r.body());
  await b.close();
})();

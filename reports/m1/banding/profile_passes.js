// Đo chi phí từng pass của scene3d_dither.js (đồng bộ bằng readPixels 1 px vì gl.finish không chặn trên SwiftShader).
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path'); const ROOT = __dirname;
(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage();
  await p.route('http://cine.local/**', (r) => { const f = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname));
    r.fulfill({ status: 200, contentType: f.endsWith('.js') ? 'text/javascript' : 'text/html', body: fs.readFileSync(f) }); });
  fs.writeFileSync(path.join(ROOT, 'page-prof.html'), '<!doctype html><canvas id="c"></canvas><script type="module" src="scene3d_dither.js"></script>');
  await p.goto('http://cine.local/page-prof.html');
  await p.waitForFunction(() => typeof window.setup === 'function');
  await p.evaluate(([s, m]) => window.setup(s, m), [JSON.parse(fs.readFileSync(path.join(ROOT, 'scene.json'))), JSON.parse(fs.readFileSync(path.join(ROOT, '../../m0/consistency/model-sheet.json')))]);
  const r = await p.evaluate(() => window._profile(6));
  console.log(JSON.stringify(r)); await b.close();
})();

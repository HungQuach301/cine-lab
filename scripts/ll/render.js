// Last Lamplighters · nhà máy — render một đoạn (16:9) hoặc một Short (9:16) từ timeline của ll.py, trong Chromium (canvas2D).
// node scripts/ll/render.js --tl <timeline.json> --seg <id> | --short <id>  --out <tệp.mkv> [--from f --to f] [--only f1,f2 --jpgdir d]
// Ra: <out> (H.264 crf 10 yuv444p, trung gian gần không mất) + <out>.log.json:
//   act: chuỗi '0'/'1' mỗi khung (có nội dung đang hiện/chuyển), cam: khoảng cách máy tới lớp gần nhất (cảnh 2.5D),
//   text: ở khung mẫu (mỗi 12 khung) — chữ, cỡ chữ hoa hiệu dụng (px), tương phản đo trên điểm ảnh thật (WCAG), raised: số lần mẫu phải nâng cỡ chữ.
const { chromium } = require('/opt/pw/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const TL = JSON.parse(fs.readFileSync(arg('tl'), 'utf8')), SEG = arg('seg'), SH = arg('short');
const spec = SH ? TL.shorts.find((s) => s.id === SH) : TL.segments.find((s) => s.id === SEG);
if (!spec) { console.error('không thấy đoạn/short', SEG || SH); process.exit(2); }
const fmt = SH ? '9x16' : '16x9', [W, H] = SH ? [1080, 1920] : [1920, 1080];
const OUT = path.resolve(arg('out')), LIB = path.join(__dirname, 'lib');
const SAMPLE = +arg('sample', 12);
(async () => {
  const browser = await chromium.launch({ args: ['--disable-gpu', '--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('[pageerror]', e.message); process.exitCode = 3; }); page.on('console', (m) => console.error('[page]', m.text()));
  const libs = ['core', 'charts', 'map', 'scenes', 'props', 'v2', 'shot'].map((n) => fs.readFileSync(path.join(LIB, n + '.js'), 'utf8')).join('\n;\n');
  // ảnh tư liệu (mẫu archive): nạp sẵn thành data URI, chờ giải mã xong mới vẽ
  const imgs = [...new Set((JSON.stringify(spec).match(/"img":"([^"]+)"/g) || []).map((m) => m.slice(7, -1)))];
  const REPO = path.join(__dirname, '..', '..');
  const imgjs = imgs.map((f) => `IMGS[${JSON.stringify(f)}]=Object.assign(new Image(),{src:'data:image/jpeg;base64,${fs.readFileSync(path.join(REPO, f)).toString('base64')}'});`).join('');
  const html = `<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#000"><canvas id="c"></canvas>
<script>window.LL={fmt:'${fmt}'};window.SPEC=${JSON.stringify(spec)};window.IMGS={};${imgjs}</script><script>${libs}</script></body></html>`;
  await page.setContent(html); await page.evaluate(() => document.fonts.ready); await page.evaluate(() => Promise.all(Object.values(window.IMGS).map((i) => i.decode())));
  const N = spec.frames, F0 = +arg('from', 0), F1 = Math.min(N, +arg('to', N));
  const ONLY = (arg('only', '') || '').split(',').filter(Boolean).map(Number);
  if (ONLY.length) { const d = arg('jpgdir', path.dirname(OUT)); fs.mkdirSync(d, { recursive: true });
    for (const f of ONLY) { await page.evaluate((f) => window.drawFrame(f), f); fs.writeFileSync(path.join(d, `${SEG || SH}_f${String(f).padStart(5, '0')}.jpg`), await page.screenshot({ type: 'jpeg', quality: 88 })); }
    await browser.close(); return; }
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', '24', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '10', '-pix_fmt', 'yuv444p', '-g', '48', '-r', '24', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
  const act = [], fill = [], cam = [], texts = [], hit = []; const t0 = Date.now();
  for (let f = F0; f < F1; f++) {
    const r = await page.evaluate(([f, smp]) => {
      LL.tlog = smp ? [] : null; window.drawFrame(f);
      const c = document.getElementById('c'), out = { hit: LL.hit ? 1 : 0, act: LL.act ? 1 : 0, fill: LL.fill ? 1 : 0, cam: isFinite(LL.camNear) ? +LL.camNear.toFixed(3) : null, img: c.toDataURL('image/jpeg', 0.96).slice(23) };
      if (smp) { const g = c.getContext('2d'), lum = (r, g2, b) => [r, g2, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }).reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
        const parse = (s) => { if (s[0] === '#') return [1, 3, 5].map((i) => parseInt(s.slice(i, i + 2), 16)); const m = s.match(/[\d.]+/g).map(Number); return m.slice(0, 3); };
        out.text = LL.tlog.filter((e) => e.alpha >= 0.95).map((e) => { const [x0, y0, x1, y1] = e.box, X0 = Math.max(0, x0 - 5), Y0 = Math.max(0, y0 - 5), X1 = Math.min(c.width - 1, x1 + 5), Y1 = Math.min(c.height - 1, y1 + 5);
          if (X1 - X0 < 2 || Y1 - Y0 < 2) return null; const d = g.getImageData(X0, Y0, X1 - X0 + 1, Y1 - Y0 + 1).data, w = X1 - X0 + 1, hh = Y1 - Y0 + 1, L = [];
          for (let x = 0; x < w; x += 2) for (const y of [0, hh - 1]) { const i = (y * w + x) * 4; L.push(lum(d[i], d[i + 1], d[i + 2])); }
          for (let y = 0; y < hh; y += 2) for (const x of [0, w - 1]) { const i = (y * w + x) * 4; L.push(lum(d[i], d[i + 1], d[i + 2])); }
          L.sort((a, b) => a - b); const bg = L[Math.floor(L.length / 2)], [cr, cg, cb] = parse(e.color), nom = lum(cr, cg, cb), I = [];
          for (let y = 5; y < hh - 5; y++) for (let x = 5; x < w - 5; x++) { const i = (y * w + x) * 4; I.push(lum(d[i], d[i + 1], d[i + 2])); }
          I.sort((a, b) => a - b); const ft = !I.length ? nom : nom < bg ? I[Math.floor(I.length * 0.05)] : I[Math.floor(I.length * 0.95)];   // màu chữ đo trên điểm ảnh (đã qua ánh rọi)
          return { s: e.s, cap: e.cap, ratio: +((Math.max(bg, ft) + 0.05) / (Math.min(bg, ft) + 0.05)).toFixed(2), box: e.box, out: x0 < 0 || y0 < 0 || x1 > c.width || y1 > c.height ? 1 : 0 }; }).filter(Boolean); }
      return out; }, [f, f % SAMPLE === 0]);
    act.push(r.act); hit.push(r.hit); fill.push(r.fill); cam.push(r.cam); if (r.text) texts.push({ f, items: r.text });
    if (!ff.stdin.write(Buffer.from(r.img, 'base64'))) await new Promise((res) => ff.stdin.once('drain', res));
    if ((f - F0) % 120 === 0) console.error(`[render ${SEG || SH}] ${f}/${F1} ${((Date.now() - t0) / 1000 / (f - F0 + 1)).toFixed(2)} s/khung`);
  }
  ff.stdin.end(); await new Promise((res) => ff.on('close', res));
  const raised = await page.evaluate(() => LL.stat); await browser.close();
  fs.writeFileSync(OUT + '.log.json', JSON.stringify({ id: SEG || SH, fmt, from: F0, to: F1, s_per_frame: +((Date.now() - t0) / 1000 / (F1 - F0)).toFixed(3), act: act.join(''), hit: hit.join(''), fill: fill.join(''), cam, raised, text: texts }));
  console.log(JSON.stringify({ id: SEG || SH, frames: F1 - F0, s_per_frame: +((Date.now() - t0) / 1000 / (F1 - F0)).toFixed(3) }));
})().catch((e) => { console.error(e); process.exit(1); });

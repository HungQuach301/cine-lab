// Đo hình học nhân vật 3D (không render): bề rộng đầu theo độ cao, bề rộng cổ, hệ H. node probe_char.js <who> [expr]
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
(async () => {
  const who = process.argv[2] || 'ida';
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const page = await b.newPage();
  page.on('pageerror', (e) => console.error('[pageerror]', e.message)); page.on('console', (m) => { if (!/GPU/.test(m.text())) console.error('[page]', m.text()); });
  await page.route('http://cine.local/**', (r) => { const p = path.join(ROOT, decodeURIComponent(new URL(r.request().url()).pathname)); if (!fs.existsSync(p)) return r.fulfill({ status: 404 }); r.fulfill({ status: 200, contentType: p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : 'text/html', body: fs.readFileSync(p) }); });
  fs.writeFileSync(path.join(ROOT, 'cong4/tools/probe.html'), '<!doctype html><body></body>'); await page.goto('http://cine.local/cong4/tools/probe.html');
  const r = await page.evaluate(async (who) => {
    const THREE = await import('/cong3/shared/node_modules/three/build/three.module.js'); const mod = await import('/cong3/v2/char3d/cast3d.js');
    const sheet = await fetch(`/cong3/model-sheet/${who}.json`).then((x) => x.json());
    const ch = mod.buildCharacter(sheet, { detail: 36 }); ch.setPose(sheet.poses.turnaround); ch.root.updateMatrixWorld(true);
    const H = sheet.H_m, out = { H, parts: {} };
    const head = ch.parts.find((m) => m.userData.part === 'head'), neck = ch.parts.find((m) => m.userData.part === 'neck');
    const hj = new THREE.Vector3(); ch.joints.head.getWorldPosition(hj);
    const stat = (m) => { const p = m.geometry.attributes.position, v = new THREE.Vector3(); const pts = []; for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); m.localToWorld(v); pts.push([v.x, v.y, v.z]); } return pts; };
    const hp = stat(head), np = stat(neck); const y0 = Math.min(...hp.map((p) => p[1])), y1 = Math.max(...hp.map((p) => p[1]));
    out.head_len_H = (y1 - y0) / H; out.width_by_y = [];
    for (let k = 0; k <= 10; k++) { const y = y0 + (y1 - y0) * k / 10; const band = hp.filter((p) => Math.abs(p[1] - y) < (y1 - y0) * 0.03); if (!band.length) continue;
      out.width_by_y.push([+(k / 10).toFixed(1), +((Math.max(...band.map((p) => p[0])) - Math.min(...band.map((p) => p[0]))) / H).toFixed(3)]); }
    const ny0 = Math.min(...np.map((p) => p[1])), ny1 = Math.max(...np.map((p) => p[1])); const mid = np.filter((p) => Math.abs(p[1] - (ny0 + ny1) / 2) < 0.01);
    out.neck_width_mid_H = +((Math.max(...mid.map((p) => p[0])) - Math.min(...mid.map((p) => p[0]))) / H).toFixed(3);
    out.sheet = { head_w: sheet.parts.head.width_front, neck_w: sheet.parts.neck.width_front };
    return out;
  }, who);
  console.log(JSON.stringify(r)); await b.close(); fs.unlinkSync(path.join(ROOT, 'cong4/tools/probe.html'));
})().catch((e) => { console.error(e); process.exit(1); });

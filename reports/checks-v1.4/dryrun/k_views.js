// Phiên K — công cụ CHẠY THỬ checks v1.4 trên số đo thật của P (Cổng 3 A2+). Không sửa design/.
// Nạp CHÍNH trang render của P (design/cong3/v2/page.js, cùng cảnh, máy quay, tư thế), tính cho mỗi khung mẫu C3 mục
// 'views' theo lược đồ RUN.md 3.6 (v1.4): view_deg, elev_deg; mỗi bộ phận foreshorten, hidden, depth.
// Đây cũng là bản tham chiếu cách tính cho bộ xuất của xưởng.
//   KNODE=<thư mục có node_modules/three 0.180.0> PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
//   node k_views.js --shot walk --frames 0,12,24,36 [--who 0] [--side L] > walk.views.json
// (design/cong3/shared/node_modules không nằm trong repo: cài three@0.180.0 theo package-lock rồi trỏ KNODE tới đó.)
const { chromium } = require('/opt/pw/node_modules/playwright');
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const REPO = path.resolve(__dirname, '../../..'), ROOT = path.join(REPO, 'design/cong3');
const shot = arg('shot'), frames = arg('frames', '0').split(',').map(Number), who = +arg('who', 0), side = arg('side', 'L');
const EXPOSE = '\nwindow.__k = { built, build, THREE, rend: () => renderer, WH: () => [W, H] };\n';

async function computeViews([shot, f, who, side]) {
  const K = window.__k, THREE = K.THREE, D2R = Math.PI / 180, R2D = 180 / Math.PI;
  const cur = K.built[shot] || (K.built[shot] = await K.build(shot));
  if (cur.setFrame) cur.setFrame(f);
  const ch = cur.chars[who], J = ch.joints, H = ch.H, S = side;
  cur.scene.updateMatrixWorld(true); cur.cam.updateMatrixWorld(true);
  const W = (o, l = [0, 0, 0]) => o.localToWorld(new THREE.Vector3(...l));
  const bones = () => ({
    head: [W(J.head), W(J.head, [0, H, 0])], torso: [W(J.spine), W(J.neck)],
    upper_arm: [W(J['shoulder_' + S]), W(J['elbow_' + S])], forearm: [W(J['elbow_' + S]), W(J['wrist_' + S])],
    thigh: [W(J['hip_' + S]), W(J['knee_' + S])], shin: [W(J['knee_' + S]), W(J['ankle_' + S])] });
  const toRoot = (v) => ch.root.worldToLocal(v.clone());
  const now = bones();
  // góc nhìn: hướng từ tâm thân tới máy quay, trong hệ gốc nhân vật (x = trái nhân vật, y = lên, z = hướng mặt)
  const camW = cur.cam.getWorldPosition(new THREE.Vector3());
  const tc = now.torso[0].clone().add(now.torso[1]).multiplyScalar(0.5);
  const c = toRoot(camW).sub(toRoot(tc));
  const view = -Math.atan2(c.x, c.z) * R2D, elev = Math.atan2(c.y, Math.hypot(c.x, c.z)) * R2D;
  // tư thế turnaround (chỉ góc khớp; gốc, đạo cụ giữ nguyên) → hướng xương tham chiếu, rồi trả lại tư thế
  const saved = Object.fromEntries(Object.entries(J).map(([k, j]) => [k, j.rotation.clone()]));
  for (const j of Object.values(J)) j.rotation.set(0, 0, 0);
  for (const [n, [x, y, z]] of Object.entries(ch.sheet.poses.turnaround.joints || {})) if (J[n]) J[n].rotation.set(x * D2R, y * D2R, z * D2R, 'XYZ');
  ch.root.updateMatrixWorld(true); const ref = bones();
  for (const [k, r] of Object.entries(saved)) J[k].rotation.copy(r);
  ch.root.updateMatrixWorld(true);
  // độ sâu theo trục máy quay: giữa xương / tâm đầu (đầu: tâm = gốc đầu + 0,5 H)
  const fwd = cur.cam.getWorldDirection(new THREE.Vector3()), zc = (p) => p.clone().sub(camW).dot(fwd);
  const ortho = !!cur.cam.isOrthographicCamera, zHead = zc(W(J.head, [0, 0.5 * H, 0]));
  // che: điểm ảnh bộ phận nhìn thấy trong cảnh (mọi vật khác tô đen, vẫn ghi độ sâu — như exportParts) so với khi chỉ vẽ
  // thân nhân vật (mọi lưới gắn nhãn bộ phận/trang phục: tự che theo thiết kế vẫn giữ; bỏ cảnh, đạo cụ, nhân vật khác)
  const PART_MAP = { head: ['head'], torso: ['torso'], upper_arm: ['upper_arm'], forearm: ['forearm'], thigh: ['thigh', 'thigh_skin'], shin: ['shin', 'shin_trouser'] };
  const keys = Object.keys(PART_MAP), partOf = {}; for (const [k, v] of Object.entries(PART_MAP)) for (const t of v) partOf[t] = k;
  const renderer = K.rend(), [w, h] = K.WH(), v = new THREE.Vector3(), box = new THREE.Box3();
  const black = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
  const idMat = keys.map((k, i) => new THREE.MeshBasicMaterial({ color: new THREE.Color((i + 1) * 30 / 255, 0, 0), side: THREE.DoubleSide }));
  const saveM = [], owner = new Map(), vis0 = new Map(), body = new Set(ch.parts);
  cur.scene.traverse((o) => {
    if (o.isSprite || o.isPoints || o.isLine) { saveM.push([o, 'v', o.visible]); o.visible = false; return; }
    if (!o.isMesh) return; saveM.push([o, 'm', o.material]); saveM.push([o, 'v', o.visible]); vis0.set(o, o.visible);
    let mine = false; for (let p = o; p; p = p.parent) if (p === ch.root) { mine = true; break; }
    const k = mine ? partOf[o.userData.part] : undefined; let ok = !!k;
    if (ok && k !== 'head' && k !== 'torso') { o.geometry.computeBoundingBox(); box.copy(o.geometry.boundingBox).applyMatrix4(o.matrixWorld); box.getCenter(v); ch.root.worldToLocal(v); ok = (v.x > 0) === (S === 'L'); }
    owner.set(o, ok ? k : null);
  });
  const bg = cur.scene.background, fog = cur.scene.fog; cur.scene.background = new THREE.Color(0); cur.scene.fog = null;
  const sm = renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate = false;
  cur.cam.clearViewOffset && cur.cam.clearViewOffset();
  const rt = new THREE.WebGLRenderTarget(w, h, { depthBuffer: true }), px = new Uint8Array(w * h * 4);
  const count = (bodyOnly) => {
    for (const [o, k] of owner) { o.material = k ? idMat[keys.indexOf(k)] : black; o.visible = vis0.get(o) && (!bodyOnly || body.has(o)); }
    renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(cur.scene, cur.cam);
    renderer.readRenderTargetPixels(rt, 0, 0, w, h, px); renderer.setRenderTarget(null);
    const n = Object.fromEntries(keys.map((k) => [k, 0]));
    for (let j = 0; j < px.length; j += 4) { const id = Math.round(px[j] / 30); if (id >= 1 && id <= keys.length) n[keys[id - 1]]++; }
    return n;
  };
  const vis = count(false), alone = count(true);
  rt.dispose(); renderer.shadowMap.autoUpdate = sm; cur.scene.background = bg; cur.scene.fog = fog;
  for (let i = saveM.length - 1; i >= 0; i--) { const [o, k, val] = saveM[i]; if (k === 'v') o.visible = val; else o.material = val; }
  const parts = {};
  for (const k of keys) {
    const [a, b] = now[k], mid = a.clone().add(b).multiplyScalar(0.5);
    // co ngắn do tư thế: độ dài chiếu lên mặt phẳng ảnh của xương bây giờ / của cùng xương ở tư thế turnaround (cùng gốc, cùng máy)
    const P = (d) => d.clone().sub(fwd.clone().multiplyScalar(d.dot(fwd))).length();
    const fs_ = P(now[k][1].clone().sub(now[k][0])) / Math.max(P(ref[k][1].clone().sub(ref[k][0])), 1e-9);
    parts[k] = { foreshorten: +fs_.toFixed(4), hidden: alone[k] ? +Math.max(0, 1 - vis[k] / alone[k]).toFixed(4) : 1,
                 depth: ortho ? 1 : +(zc(k === 'head' ? W(J.head, [0, 0.5 * H, 0]) : mid) / zHead).toFixed(4),
                 _px_nhin_thay_1x: vis[k], _px_chi_than_1x: alone[k] };
  }
  return { view_deg: +view.toFixed(2), elev_deg: +elev.toFixed(2), parts };
}

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--js-flags=--max-old-space-size=8192'] });
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message)); page.on('console', (m) => { if (process.env.KDEBUG) console.error('[page]', m.text()); }); page.on('requestfailed', (r) => console.error('[reqfail]', r.url()));
  await page.route('http://cine.local/**', (route) => {
    const rel = decodeURIComponent(new URL(route.request().url()).pathname);
    // three.js theo package-lock của P (0.180.0); node_modules không nằm trong repo → KNODE trỏ tới bản cài
    const p = rel.startsWith('/shared/node_modules/') && process.env.KNODE ? path.join(process.env.KNODE, rel.slice('/shared/'.length)) : path.join(ROOT, rel);
    if (rel === '/__k.html') return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><html><body><script type="module" src="/v2/page.js"></script></body></html>' });
    const type = p.endsWith('.js') ? 'text/javascript' : p.endsWith('.json') ? 'application/json' : p.endsWith('.png') ? 'image/png' : 'text/html';
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'not found ' + p });
    let body = fs.readFileSync(p); if (rel === '/v2/page.js') body = Buffer.concat([body, Buffer.from(EXPOSE)]);
    route.fulfill({ status: 200, contentType: type, body });
  });
  await page.goto('http://cine.local/__k.html');
  await page.waitForFunction(() => typeof window.setup === 'function' && window.__k, null, { timeout: 60000 });
  await page.evaluate(async (cfg) => { await window.setup(cfg); }, { W: 1920, H: 1080, shot, char: '3d' });
  const out = {};
  for (const f of frames) { out[String(f)] = await page.evaluate(computeViews, [shot, f, who, side]); console.error(shot, f, JSON.stringify(out[String(f)]).slice(0, 300)); }
  await browser.close();
  process.stdout.write(JSON.stringify(out, null, 1) + '\n');
})().catch((e) => { console.error(e); process.exit(1); });

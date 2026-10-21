// V7C (việc 2) · MẶT NẠ ID + ĐO BỐ CỤC — tái dùng design/k2v/v2v/idmask.js (NC-V2V, nhánh nc-v2v @2c1d1e12) nguyên cách gắn loại theo ngăn xếp gọi Object3D.add,
//  thêm: (1) 'pho' = nền phố của năm (lượt mặt nạ: xanh lục = đô thị — terrain.js uMask 1), (2) đất tự nhiên tách 'bang' (bằng, cỏ/cát trống: lam 0,5) · 'suon' (bằng > 30 m: lam 0,70)
//  · 'da' (dốc/vách: lam 0,9), (3) 'trai' (camps) và 'congsu' (fortify/frontLines/fence) tách khỏi 'nha', (4) TIÊU ĐIỂM: chiếu các điểm thế giới [E, cao, N] của vật hero/biến cố
//  qua đúng máy của khung → hộp bao (bề ngang % khung), tâm, nằm trong 1/3 giữa hay sát giao điểm 1/3. Đoạn mã NỐI VÀO CUỐI page.js (driver do_bocuc.js), không sửa page.js.
Error.stackTraceLimit = 60;
{
  const add0 = THREE.Object3D.prototype.add;
  THREE.Object3D.prototype.add = function (...objs) {
    const st = new Error().stack || '', fn = [];
    for (const m of st.matchAll(/at (?:async )?(?:new )?([\w$.]+) \(/g)) { const n = m[1].split('.').pop(); if (n !== 'add' && !fn.includes(n)) fn.push(n); }
    for (const o of objs) if (o && o.userData && !o.userData.v2vFn) o.userData.v2vFn = fn;
    return add0.apply(this, objs);
  };
}
const V7C_RULES = [
  ['co', ['shipFlags', 'flags']],
  ['pin', ['batteryV6', 'batteryGroup']],
  ['tau', ['makeFleet', 'makeShips']],
  ['nguoi', ['person', 'life', 'units', 'unitsV6', 'people', 'makePeople', 'crowd', 'walkers', 'campLife', 'horses', 'carts']],
  ['khac', ['car', 'carOn', 'streetTrees', 'streetLamps', 'parkedCars']],
  ['trai', ['camps']],
  ['congsu', ['fortify', 'frontLines', 'fence', 'wallRing']],
  ['nha', ['makeCity', 'makeHeroes', 'ruins', 'footprints', 'phaseMaps', 'landmarks', 'facades']],
  ['datvat', ['makeTrees', 'makeRoads', 'trees', 'roads', 'gardens', 'makeBushes']],
];
const V7C_PAL = { troi: [40, 80, 200], nuoc: [0, 170, 190], bang: [200, 170, 90], suon: [150, 120, 70], da: [110, 100, 95], pho: [255, 200, 220], nha: [235, 235, 235], trai: [245, 225, 160], congsu: [170, 150, 120],
  tau: [255, 0, 0], co: [255, 255, 0], pin: [255, 0, 255], lua: [255, 128, 0], nguoi: [0, 255, 0], khac: [128, 128, 128] };
const V7C_NOIDUNG = ['pho', 'nha', 'trai', 'congsu', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac'], V7C_TRONG = ['nuoc', 'bang', 'suon'];
const v7cMatFlag = (o) => { const ms = Array.isArray(o.material) ? o.material : [o.material]; return ms.some((m) => m && m.customProgramCacheKey && /flag/.test(String(m.customProgramCacheKey()))); };
function v7cCls(o) {
  if (o.isMesh && v7cMatFlag(o)) return 'co';
  for (let p = o; p; p = p.parent) { const fn = p.userData && p.userData.v2vFn; if (!fn) continue; for (const [c, names] of V7C_RULES) if (names.some((n) => fn.includes(n))) return c; }
  const f0 = o.userData && o.userData.v2vFn; if (f0 && f0[0] === 'setup') return 'datvat';
  return 'khac';
}
let v7cRT = null;
window.v7cCensus = () => { const by = {}; scene.traverse((o) => { if (!(o.isMesh || o.isSprite || o.isPoints || o.isInstancedMesh)) return; const c = v7cCls(o), k = c + ' ← ' + ((o.userData.v2vFn || (o.parent && o.parent.userData.v2vFn) || []).slice(0, 4).join('/')); by[k] = (by[k] || 0) + 1; }); return by; };
// td = [{ten, t: [t0, t1], pts: [[E, cao, N], …]}] — tiêu điểm khai theo khoảng giây của shot
window.v7cMeasure = (f, scale, td, png, camOv) => {   // camOv = {p: [E, cao, N], l: [E, cao, N], fov} — thử điểm máy ứng viên trên cùng trạng thái khung (soạn máy)
  const t = f / SC.fps, st = SC.state(t), U = ctx.U; if (camOv) st.cam = camOv; U.uYear.value = st.year; U.uDim.value = 0; U.uT.value = t;
  applyCam(cam, st.cam); ctx.terr.update(cam); ctx.city.update(cam); if (ctx.trees) ctx.trees.update(cam); ctx.ships.update(st.year); SC.apply && SC.apply(st, t);
  const w = Math.round(C.W * (scale || 0.5)), h = Math.round(C.H * (scale || 0.5)); if (!v7cRT || v7cRT.width !== w) v7cRT = new THREE.WebGLRenderTarget(w, h);
  const all = []; scene.traverse((o) => { if ((o.isMesh || o.isSprite || o.isPoints || o.isInstancedMesh) && o.visible) all.push(o); });
  const terrSet = new Set(); ctx.terr.group.traverse((o) => terrSet.add(o));
  const hideSet = new Set(); for (const g of ctx.maskHide || []) g.traverse((o) => hideSet.add(o));
  const isL = (o) => (o.userData.v2vFn || []).includes('lamps');
  const lmpSet = new Set(); for (const o of all) { let q = o; while (q) { if (q.userData && isL(q)) { lmpSet.add(o); break; } q = q.parent; } }
  const cls = new Map(); for (const o of all) if (!terrSet.has(o) && !hideSet.has(o)) cls.set(o, v7cCls(o));
  const sm = R.shadowMap.enabled, cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(), wv = ctx.ws.water.visible, sv = ctx.ws.sky.visible;
  const pass = (keep, mask) => { const hid = all.filter((o) => !keep(o)); for (const o of hid) o.visible = false;
    U.uMask.value = mask ? 1 : 0; ctx.ws.water.visible = ctx.ws.sky.visible = false; R.shadowMap.enabled = false; R.setClearColor(0x000000, 1);
    R.setRenderTarget(v7cRT); R.clear(); R.render(scene, cam); const px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(v7cRT, 0, 0, w, h, px); R.setRenderTarget(null);
    for (const o of hid) o.visible = true; return px; };
  const isRed = (px, i) => px[i] > 128 && px[i + 1] < 90;
  const pAll = pass((o) => !hideSet.has(o), true);
  const order = ['co', 'pin', 'tau', 'nguoi', 'khac', 'trai', 'congsu', 'nha', 'datvat'], per = {}, present = new Set(cls.values());
  for (const c of order) { if (!present.has(c)) continue; per[c] = pass((o) => terrSet.has(o) || cls.get(o) === c, true); }
  let pFire = null, pTer = null; if (lmpSet.size) { pTer = pass((o) => terrSet.has(o), false); pFire = pass((o) => terrSet.has(o) || lmpSet.has(o), false); }
  U.uMask.value = 0; ctx.ws.water.visible = wv; ctx.ws.sky.visible = sv; R.shadowMap.enabled = sm; R.setClearColor(cc, ca);
  cam.updateMatrixWorld(); const ivp = new THREE.Matrix4().multiplyMatrices(cam.matrixWorld, cam.projectionMatrixInverse), rv = new THREE.Vector3();
  const below = new Uint8Array(w * h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x += 8) { rv.set((x + 0.5) / w * 2 - 1, (y + 0.5) / h * 2 - 1, 0.5).applyMatrix4(ivp).sub(cam.position); const b = rv.y < 0 ? 1 : 0; for (let k = x; k < Math.min(w, x + 8); k++) below[y * w + k] = b; }
  const names = Object.keys(V7C_PAL), ix = Object.fromEntries(names.map((n, i) => [n, i])), id = new Uint8Array(w * h), cnt = new Array(names.length).fill(0);
  for (let k = 0; k < w * h; k++) { const i = k * 4; let c;
    if (isRed(pAll, i)) { c = 'khac'; for (const q of order) if (per[q] && isRed(per[q], i)) { c = q; break; } if (c === 'datvat') c = 'bang'; }
    else if (pAll[i] < 90 && pAll[i + 1] > 128) c = 'pho';
    else if (pAll[i] < 20 && pAll[i + 1] < 20 && pAll[i + 2] < 20) c = below[k] ? 'nuoc' : 'troi';
    else { const b = pAll[i + 2]; c = b > 40 && b <= 90 ? (pAll[i] < 20 && pAll[i + 1] < 20 ? 'nuoc' : 'bang') : b > 90 && b < 160 ? 'bang' : b >= 160 && b < 200 ? 'suon' : b >= 200 ? 'da' : 'bang'; }
    if (pFire && Math.abs(pFire[i] - pTer[i]) + Math.abs(pFire[i + 1] - pTer[i + 1]) + Math.abs(pFire[i + 2] - pTer[i + 2]) > 60) c = 'lua';
    id[k] = ix[c]; cnt[ix[c]]++; }
  const pct = {}; names.forEach((n, i) => { pct[n] = +(cnt[i] / (w * h) * 100).toFixed(2); });
  const noi_dung = +V7C_NOIDUNG.reduce((a, n) => a + pct[n], 0).toFixed(2), trong = +V7C_TRONG.reduce((a, n) => a + pct[n], 0).toFixed(2);
  // tiêu điểm
  const tds = []; for (const d of td || []) { if (d.t && (t < d.t[0] || t > d.t[1])) continue; let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, nIn = 0;
    for (const p of d.pts) { const hy = p[1] == null ? Math.max(0, ctx.terr.hAt(p[0], p[2])) + (p[3] || 0) : p[1], v = new THREE.Vector3(p[0], hy, -p[2]).project(cam); if (!(v.z > -1 && v.z < 1)) continue; const X = (v.x + 1) / 2, Y = (1 - v.y) / 2; nIn++; x0 = Math.min(x0, X); x1 = Math.max(x1, X); y0 = Math.min(y0, Y); y1 = Math.max(y1, Y); }
    if (!nIn) { tds.push({ ten: d.ten, thay: false }); continue; }
    const cx = (Math.max(0, x0) + Math.min(1, x1)) / 2, cy = (Math.max(0, y0) + Math.min(1, y1)) / 2, wi = Math.min(1, x1) - Math.max(0, x0), hi = Math.min(1, y1) - Math.max(0, y0);
    const giua = cx >= 1 / 3 && cx <= 2 / 3 && cy >= 1 / 3 && cy <= 2 / 3, gd = [[1 / 3, 1 / 3], [2 / 3, 1 / 3], [1 / 3, 2 / 3], [2 / 3, 2 / 3]].some(([a, b]) => Math.abs(cx - a) <= 1 / 12 && Math.abs(cy - b) <= 1 / 9);
    const trong_khung = x1 > 0 && x0 < 1 && y1 > 0 && y0 < 1;
    tds.push({ ten: d.ten, thay: trong_khung, rong_pct: +(wi * 100).toFixed(1), cao_pct: +(hi * 100).toFixed(1), tam: [+cx.toFixed(3), +cy.toFixed(3)], giua, giao_1_3: gd, dat: trong_khung && wi >= 0.08 && (giua || gd) }); }
  // máy
  const c = st.cam, pos = cam.position, dir = new THREE.Vector3(); cam.getWorldDirection(dir);
  const agl = +(pos.y - Math.max(0, ctx.terr.hAt(pos.x, -pos.z))).toFixed(1), xuong = +(Math.asin(-dir.y) * 180 / Math.PI).toFixed(1);
  let png_b64 = null; if (png) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'), im = g.createImageData(w, h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const col = V7C_PAL[names[id[(h - 1 - y) * w + x]]], o = (y * w + x) * 4; im.data[o] = col[0]; im.data[o + 1] = col[1]; im.data[o + 2] = col[2]; im.data[o + 3] = 255; }
    g.putImageData(im, 0, 0); png_b64 = cv.toDataURL('image/png').slice(22); }
  return { f, t: +t.toFixed(3), year: +st.year.toFixed(4), w, h, pct, noi_dung, trong, td: tds, agl, xuong, fov: +cam.fov.toFixed(2), cam: [pos.x, pos.y, -pos.z].map((x) => +x.toFixed(1)), png_b64 };
};

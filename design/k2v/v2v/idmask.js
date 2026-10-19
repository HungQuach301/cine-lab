// NC-V2V · MẶT NẠ ID theo loại vật — đoạn mã NỐI VÀO CUỐI bản sao trang dựng V7B (design/k2v/tl/page.js @317dcf5) do mk_page.py tạo,
// nên dùng được biến của mô-đun (scene, cam, ctx, R, SC, C). KHÔNG sửa mã k2v cũ.
// Cách gắn loại: mỗi lần Object3D.add, ghi TÊN HÀM trong ngăn xếp gọi (batteryV6, makeFleet, shipFlags, flags, lamps, makeCity, …) vào userData.v2vFn.
// Loại của một mesh = luật ưu tiên đầu tiên khớp trên chính nó rồi tới tổ tiên. Vật liệu cờ (khoá chương trình chứa 'flag') luôn là cờ.
// Mỗi khung: (1) lượt TẤT CẢ (uMask = 1, nước/trời ẩn): đỏ = vật nội dung, đen = nước (dưới chân trời) / trời (trên), còn lại = đất;
// (2) mỗi loại một lượt (chỉ địa hình + loại đó) → điểm đỏ ở cả (1) và (2) thuộc loại đó, chồng lấn theo ưu tiên cờ > pin nổi > tàu > người > nhà > vật đất;
// (3) lửa = điểm khác nhau giữa lượt (địa hình + nhóm đèn/lửa, không mặt nạ) và lượt địa hình trơn.
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
const V2V_RULES = [
  ['co', ['shipFlags', 'flags']],
  ['pin', ['batteryV6', 'batteryGroup']],
  ['tau', ['makeFleet', 'makeShips']],
  ['nguoi', ['person', 'life', 'units', 'unitsV6', 'people', 'makePeople', 'crowd', 'walkers']],
  ['khac', ['car', 'carOn']],
  ['nha', ['makeCity', 'makeHeroes', 'fortify', 'camps', 'ruins', 'footprints', 'frontLines', 'fence', 'phaseMaps', 'landmarks']],
  ['datvat', ['makeTrees', 'makeRoads', 'trees', 'roads', 'gardens']],
];
export const V2V_PAL = { troi: [40, 80, 200], nuoc: [0, 170, 190], dat: [140, 105, 60], nha: [235, 235, 235], tau: [255, 0, 0], co: [255, 255, 0], pin: [255, 0, 255], lua: [255, 128, 0], nguoi: [0, 255, 0], khac: [128, 128, 128] };
const v2vMatFlag = (o) => { const ms = Array.isArray(o.material) ? o.material : [o.material]; return ms.some((m) => m && m.customProgramCacheKey && /flag/.test(String(m.customProgramCacheKey()))); };
function v2vCls(o) {
  if (o.isMesh && v2vMatFlag(o)) return 'co';
  for (let p = o; p; p = p.parent) { const fn = p.userData && p.userData.v2vFn; if (!fn) continue; for (const [c, names] of V2V_RULES) if (names.some((n) => fn.includes(n))) return c; }
  return 'khac';
}
let v2vRT = null;
window.v2vCensus = () => { const by = {}; scene.traverse((o) => { if (!(o.isMesh || o.isSprite || o.isPoints || o.isInstancedMesh)) return; const c = v2vCls(o), k = c + ' ← ' + ((o.userData.v2vFn || (o.parent && o.parent.userData.v2vFn) || []).slice(0, 4).join('/')); by[k] = (by[k] || 0) + 1; }); return by; };
window.v2vIdMask = (f, scale) => {
  const t = f / SC.fps, st = SC.state(t), U = ctx.U; U.uYear.value = st.year; U.uDim.value = 0; U.uT.value = t;
  applyCam(cam, st.cam); ctx.terr.update(cam); ctx.city.update(cam); if (ctx.trees) ctx.trees.update(cam); ctx.ships.update(st.year); SC.apply && SC.apply(st, t);
  const w = Math.round(C.W * (scale || 1)), h = Math.round(C.H * (scale || 1)); if (!v2vRT || v2vRT.width !== w) v2vRT = new THREE.WebGLRenderTarget(w, h);
  const all = []; scene.traverse((o) => { if ((o.isMesh || o.isSprite || o.isPoints || o.isInstancedMesh) && o.visible) all.push(o); });
  const terrSet = new Set(); ctx.terr.group.traverse((o) => terrSet.add(o));
  const hideSet = new Set(); for (const g of ctx.maskHide || []) g.traverse((o) => hideSet.add(o));
  const lmpSet = new Set(); for (const o of all) if (hideSet.has(o) && (o.userData.v2vFn || (o.parent && o.parent.userData.v2vFn) || []).includes('lamps')) lmpSet.add(o);
  for (const p of all) if (!lmpSet.has(p)) { let q = p.parent; while (q) { if (q.userData && q.userData.v2vFn && q.userData.v2vFn.includes('lamps')) { lmpSet.add(p); break; } q = q.parent; } }
  const cls = new Map(); for (const o of all) if (!terrSet.has(o) && !hideSet.has(o)) cls.set(o, v2vCls(o));
  const sm = R.shadowMap.enabled, cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(), wv = ctx.ws.water.visible, sv = ctx.ws.sky.visible;
  const pass = (keep, mask) => { const hid = all.filter((o) => !keep(o)); for (const o of hid) o.visible = false;
    U.uMask.value = mask ? 1 : 0; ctx.ws.water.visible = ctx.ws.sky.visible = false; R.shadowMap.enabled = false; R.setClearColor(0x000000, 1);
    R.setRenderTarget(v2vRT); R.clear(); R.render(scene, cam); const px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(v2vRT, 0, 0, w, h, px); R.setRenderTarget(null);
    for (const o of hid) o.visible = true; return px; };
  const isRed = (px, i) => px[i] > 128 && px[i + 1] < 90;
  const pAll = pass((o) => !hideSet.has(o), true);
  const order = ['co', 'pin', 'tau', 'nguoi', 'khac', 'nha', 'datvat'], per = {};
  for (const c of order) { if (![...cls.values()].includes(c)) continue; per[c] = pass((o) => terrSet.has(o) || cls.get(o) === c, true); }
  let pFire = null, pTer = null; if (lmpSet.size) { pTer = pass((o) => terrSet.has(o), false); pFire = pass((o) => terrSet.has(o) || lmpSet.has(o), false); }
  U.uMask.value = 0; ctx.ws.water.visible = wv; ctx.ws.sky.visible = sv; R.shadowMap.enabled = sm; R.setClearColor(cc, ca);
  cam.updateMatrixWorld(); const ivp = new THREE.Matrix4().multiplyMatrices(cam.matrixWorld, cam.projectionMatrixInverse), rv = new THREE.Vector3();
  const below = new Uint8Array(h); for (let y = 0; y < h; y++) { rv.set(0, (y + 0.5) / h * 2 - 1, 0.5).applyMatrix4(ivp).sub(cam.position); below[y] = rv.y < 0 ? 1 : 0; }   // gần đúng: chân trời theo cột giữa (máy không nghiêng ngang)
  const id = new Uint8Array(w * h), names = ['troi', 'nuoc', 'dat', 'nha', 'tau', 'co', 'pin', 'lua', 'nguoi', 'khac'], ix = Object.fromEntries(names.map((n, i) => [n, i])), cnt = new Array(names.length).fill(0);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const k = y * w + x, i = k * 4; let c;
    if (isRed(pAll, i)) { c = 'khac'; for (const q of order) if (per[q] && isRed(per[q], i)) { c = q; break; } if (c === 'datvat') c = 'dat'; }
    else if (pAll[i] < 20 && pAll[i + 1] < 20 && pAll[i + 2] < 20) c = below[y] ? 'nuoc' : 'troi'; else if (pAll[i + 2] > 40 && pAll[i + 2] <= 90 && pAll[i] < 90) c = 'nuoc'; else c = 'dat';   // lam 40–90 = đáy biển dưới mặt nước (cùng mã như contentMask)
    if (pFire && Math.abs(pFire[i] - pTer[i]) + Math.abs(pFire[i + 1] - pTer[i + 1]) + Math.abs(pFire[i + 2] - pTer[i + 2]) > 60) c = 'lua';
    id[k] = ix[c]; cnt[ix[c]]++; }
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'), im = g.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const c = V2V_PAL[names[id[(h - 1 - y) * w + x]]], o = (y * w + x) * 4; im.data[o] = c[0]; im.data[o + 1] = c[1]; im.data[o + 2] = c[2]; im.data[o + 3] = 255; }   // lật dọc về chiều ảnh
  g.putImageData(im, 0, 0);
  const pct = {}; names.forEach((n, i) => { pct[n] = +(cnt[i] / (w * h) * 100).toFixed(3); });
  return { f, year: +st.year.toFixed(4), w, h, pct, png_b64: cv.toDataURL('image/png').slice(22) };
};

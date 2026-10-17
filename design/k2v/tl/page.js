// K2V tl · TRANG DỰNG xương sống thời gian (driver: scripts/k2tl/render.js). Chromium headless + SwiftShader (chỉ CPU).
// Đường ống: post.js dùng chung (tích luỹ SPP có jitter → tone ACES → grade [lọc cạnh SPP1 + LUT A + vignette] → grain cố định),
// rồi lớp 2D (text.js: năm, chỉ số, thẻ, ảnh chú thích) vẽ SAU (chữ không qua LUT/grain), đo ngân sách chữ + tương phản trên điểm ảnh thật.
// Kỹ thuật đo được bật/tắt qua cfg.tech: lod, ao (AO nướng theo năm), shadowCache (bóng 1 lần/khung + giữ khi cảnh không đổi), spp ('adaptive' | số), shadowRes.
import { THREE, track, loadJSON, loadImg, maskify } from './core.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { makeTerrain } from './terrain.js';
import { makeWaterSky } from './water.js';
import { makeCity } from './city.js';
import { makeTrees, makeRoads } from './nature.js';
import { makeHeroes } from './heroes.js';
import { makeShips } from './ships.js';
import { applyCam } from './campath.js';
import { makeText } from './text.js';
import { loadCube, GRADE_GLSL } from './lut.js';
import { makeRecorder } from './record.js';
import { sunDirENU } from './sun.js';

let C, R, pipe, scene, cam, SC, ctx, outScene, quadCam, txt, rec, HERO = false, last = null, stats = {};
// V5b-2b (V5B2A §8.2): trang dựng được gọi từ scripts/k2/hero.js ('tl/<cảnh>', opt = {pack, lut, lutMode, vib, look, photo, tech, layers, …}) —
//  chế độ HERO: khung KHÔNG chữ (window.finalize → RGB), lớp chữ ghi lại bằng record.js vào anchorsAt()._tl để scripts/k2/lib/k2.js vẽ; frameMeta() mỗi khung (AGL, SPP, pha).
function heroCfg(c) { const o = c.opt || {}; return { W: c.W, H: c.H, hero: c.hero, scene: c.hero.split('/')[1], opt: o, pack: `/cache/scene/${o.pack || 'gib'}/pack/`, lut: '/cache/lut/' + (o.lut || 'k2-a-thep-lanh') + '.cube',
  lutMode: o.lutMode ?? 1, vib: o.vib ?? 0.35, look: o.look || {}, photo: o.photo === undefined ? '/cache/loc/ng_crop.jpg' : o.photo, tech: o.tech || {}, lutK: o.lutK ?? 1 }; }
window.setup = async (cfg) => {
  if (cfg.hero) { HERO = true; cfg = heroCfg(cfg); }
  C = cfg; const T = Object.assign({ lod: true, ao: true, shadowCache: true, spp: 'adaptive', shadowRes: 4096, city: true, trees: true, baked: false, lambert: true } /* baked: nhiễu nướng sẵn (chống lặp ô) — đo lại 16/10 không nhanh hơn nhiễu thủ tục → tắt mặc định */, cfg.tech || {}); C.tech = T;
  const t0 = performance.now(), base = cfg.pack;
  const M = await loadJSON(base + 'meta.json');
  R = createRenderer(cfg.W, cfg.H); R.shadowMap.type = THREE.PCFSoftShadowMap; R.shadowMap.autoUpdate = !T.shadowCache;
  const lut = await loadCube(cfg.lut);   /* V5b-1b: LUT chọn bằng số đo (reports/V5B1B-BAO-CAO.md §2) */
  const LU = { tLut: { value: lut.tex }, uLutK: { value: cfg.lutK ?? 1.0 }, uLutN: { value: lut.N }, uVig: { value: 0.16 }, uAA: { value: 0 }, uLutMode: { value: cfg.lutMode ?? 1 }, uVib: { value: cfg.vib ?? 0.35 } };
  pipe = createPipeline(R, cfg.W, cfg.H, { exposure: cfg.exposure ?? 1.0, gradeGLSL: GRADE_GLSL, uniforms: LU });
  quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1); outScene = new THREE.Scene(); outScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), pipe.outMat));
  scene = new THREE.Scene();
  const sunEl = 31 * Math.PI / 180, sunAz = 238 * Math.PI / 180;   // nắng chiều hướng tây-nam (nổi mặt tây Rock, vách bắc vào bóng)
  const sunDir = new THREE.Vector3(Math.sin(sunAz) * Math.cos(sunEl), Math.sin(sunEl), -Math.cos(sunAz) * Math.cos(sunEl)).normalize();
  const U = { uMask: { value: 0 }, uYear: { value: 1700 }, uDim: { value: 0 }, uSample: { value: 0 }, uT: { value: 0 }, uAOon: { value: T.ao ? 1 : 0 }, uBaked: { value: T.baked ? 1 : 0 }, lambert: T.lambert, terrainLod: T.terrainLod, treeDetail: T.treeDetail, groundNear: T.groundNear ?? 1, sunDir };
  // V5b-1b: sương CHỈ ở xa, ngả xanh (cùng màu chân trời trời mới), mật độ thấp hơn → cận/trung cảnh trong; nắng thấp có hướng mạnh hơn,
  // ánh trời xanh làm bóng ngả lạnh (tương phản ấm–lạnh), bóng sắc hơn (bán kính PCF 3 → 1,5).
  const L = Object.assign({ fogC: [0.60, 0.74, 0.90], fogD: 0.0000175, hemiSky: '#9cbcf0', hemiGnd: '#7a6648', hemiI: 0.62, sunC: '#ffe3b8', sunI: 3.3, shR: 1.5 }, cfg.look || {}); C.look = L;
  const fogC = new THREE.Color(...L.fogC); scene.fog = new THREE.FogExp2(fogC, L.fogD);
  scene.add(new THREE.HemisphereLight(L.hemiSky, L.hemiGnd, L.hemiI));
  const sun = new THREE.DirectionalLight(L.sunC, L.sunI); sun.castShadow = T.shadows !== false; sun.shadow.mapSize.set(T.shadowRes, T.shadowRes); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.6; sun.shadow.radius = L.shR;
  scene.add(sun, sun.target);
  const terr = await makeTerrain(base, M, U); scene.add(terr.group);
  const ws = makeWaterSky(U, scene.fog);   /* ctx.ws: mặt nạ nội dung ẩn nước/trời */ scene.add(ws.water, ws.sky);
  let B = T.city ? await loadJSON(base + 'buildings.json') : [];
  if (T.copies > 1) { const B0 = B; B = []; for (let k = 0; k < T.copies; k++) for (const b of B0) B.push(k ? [b[0], b[1], b[2], b[3], b[4], b[5], b[6].map(([e, n]) => [e + ((k % 4) - 1.5) * 3000, n + 4500 + Math.floor(k / 4) * 3500])] : b); }   /* thử tải: nhân bản toà (đo trần toà/cảnh) */
  // V5b-2b (M9): opt.cut = [lớp footprint] → bỏ toà của gói nằm trong các vòng đó (vd. công sự King's Bastion dựng riêng: không để nhà tái dựng mọc trên mặt sàn pháo)
  if (cfg.opt && cfg.opt.cut) { const inside = (p, r) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > p[1]) !== (r[j][1] > p[1]) && p[0] < (r[j][0] - r[i][0]) * (p[1] - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; };
    const rings = []; for (const f of cfg.opt.cut) rings.push(...(await loadJSON(`${base}layers/${f}.json`)).records.map((r) => r[6]));
    const n0 = B.length; B = B.filter((b) => { const cx = b[6].reduce((a, q) => a + q[0], 0) / b[6].length, cn = b[6].reduce((a, q) => a + q[1], 0) / b[6].length; return !rings.some((r) => inside([cx, cn], r)); }); stats.cut = n0 - B.length; }
  const city = makeCity(B, U, { lod: T.lod }); scene.add(city.group);
  const roads = makeRoads(await loadJSON(base + 'roads.json'), terr.hAt, U); scene.add(roads.mesh);
  const trees = T.trees ? makeTrees(new Float32Array(await (await fetch(base + 'trees.f32')).arrayBuffer()), terr.hAt, U, { lod: T.lod }) : null; if (trees) scene.add(trees.group);
  const LINES = await loadJSON(base + 'lines.json'); const heroes = makeHeroes(await loadJSON(base + 'heroes.json'), terr.hAt, U, terr, LINES); scene.add(heroes.group);
  const ships = makeShips(U); if (T.ships !== false) scene.add(ships.group);
  cam = new THREE.PerspectiveCamera(38, cfg.W / cfg.H, 5, 80000);
  txt = makeText(cfg.W, cfg.H); rec = makeRecorder(cfg.W, cfg.H);
  const photo = cfg.photo ? await loadImg(cfg.photo) : null;
  const mod = await import(`./scenes/${cfg.scene}.js`);
  ctx = { THREE, U, M, terr, city, roads, trees, heroes, ships, sun, sunDir, cam, photo, lines: LINES, W: cfg.W, H: cfg.H, track, scene, maskify, base, opt: cfg.opt || {}, makeCity, loadJSON, R };   /* V5b-2b: opt của shot + makeCity (lớp footprint M9) */   /* V5b-2a: cảnh thêm phần tử 3D riêng (overlay3d.js) */
  SC = await mod.build(ctx);
  // mặt nạ nội dung: hero + đường = nội dung (city/terrain tự có mã mặt nạ); cây = nền
  const mk = (obj, v, hid = 0) => obj && obj.traverse((o) => { if (o.isMesh) for (const m of [].concat(o.material)) if (!m.isShaderMaterial) maskify(m, U, v, hid); });
  for (const [k, objs] of Object.entries(heroes.heroParts || {})) for (const o of objs) mk(o, 1, heroes.heroIds[k]);   // V5b-2a: hero có id (trước mk chung — maskify bỏ qua vật liệu đã gắn)
  mk(heroes.group, 1); mk(roads.mesh, 1); mk(ships.group, 1); if (trees) mk(trees.group, 0); mk(terr.group.children.find((o) => o.material && o.material.map), 0);
  ctx.ws = ws;
  stats = { cut: stats.cut || 0, ships: ships.n, styles: city.styles, corner_towers: heroes.cornerTowers, load_s: +((performance.now() - t0) / 1000).toFixed(2), terrain_tris: terr.tris, city_tris: city.tris, city_tiles: city.nTiles, buildings: B.length, roads_tris: roads.tris, trees: trees ? trees.n : 0,
    renderer: (() => { const gl = R.getContext(), e = gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER); })(), tech: T, N: SC.N, scene_meta: SC.meta || null };
  return stats;
};
let shadowKey = null, shadowUpdates = 0;
function fitShadow(st) {   // hộp bóng bám điểm nhìn; cỡ theo khoảng cách máy
  const look = new THREE.Vector3(st.cam.l[0], 0, -st.cam.l[2]);
  const d = Math.hypot(st.cam.p[0] - st.cam.l[0], st.cam.p[1] - st.cam.l[1], st.cam.p[2] - st.cam.l[2]);
  const ext = Math.min(3200, Math.max(260, d * 1.15)), s = ctx.sun, sc = s.shadow.camera;
  const key = [Math.round(look.x / (ext * 0.08)), Math.round(look.z / (ext * 0.08)), Math.round(Math.log(ext) * 12), Math.round(st.year * 4) / 4];
  const changed = !shadowKey || key.some((v, i) => v !== shadowKey[i]);
  if (changed) { s.target.position.copy(look); s.position.copy(look).addScaledVector(ctx.sunDir, 7000);
    Object.assign(sc, { left: -ext, right: ext, top: ext, bottom: -ext, near: 100, far: 14000 }); sc.updateProjectionMatrix(); s.target.updateMatrixWorld(); s.updateMatrixWorld();
    shadowKey = key; }
  return changed;
}
// dựng một khung: trả JPEG base64 + nhật ký (ms, spp, ngân sách chữ, tương phản, LOD)
// V5b-2b (M6): cảnh khai st.sun = {el, az} (thiên văn, sun.js) → đổi hướng nắng mỗi khung (khoá bóng gồm hướng nắng)
function applySun(st) { if (!st.sun) return; const d = sunDirENU(st.sun); if (Math.abs(d[0] - ctx.sunDir.x) + Math.abs(d[1] - ctx.sunDir.y) + Math.abs(d[2] - ctx.sunDir.z) > 1e-6) { ctx.sunDir.set(...d).normalize(); shadowKey = null; } }
window.renderFrame = async (f, measure, ov) => {
  const t = f / SC.fps, st = Object.assign(SC.state(t), ov || {}); const U = ctx.U;   // ov: ghi đè trạng thái (khung kiểm: năm/máy cố định)
  applySun(st); last = { f, t, st };
  U.uYear.value = st.year; U.uDim.value = st.dim || 0; U.uT.value = t;
  applyCam(cam, st.cam); ctx.terr.update(cam); ctx.city.update(cam); if (ctx.trees) ctx.trees.update(cam); ctx.ships.update(st.year); SC.apply && SC.apply(st, t);
  const spp = C.tech.spp === 'adaptive' ? st.spp : +C.tech.spp;
  pipe.outMat.uniforms.uAA.value = spp === 1 ? 1 : 0;
  const t0 = performance.now();
  let shadowDone = false;
  if (C.tech.shadowCache) { if (fitShadow(st)) { R.shadowMap.needsUpdate = true; shadowUpdates++; } }
  else fitShadow(st);
  const ms = pipe.accumulate(scene, cam, spp, (i) => { U.uSample.value = i + f * 0.137; if (C.tech.shadowCache && i > 0) R.shadowMap.needsUpdate = false; });
  R.setRenderTarget(null); pipe.outMat.uniforms.frame.value = f; R.render(outScene, quadCam);
  const t1 = performance.now();
  if (HERO) return { f, spp, gl_ms: +ms.toFixed(1), phase: st.phase || null };   // chế độ hero: chữ do k2.js vẽ (anchorsAt()._tl)
  const t2 = performance.now(); txt.begin(R.domElement);
  if (!(ov && ov.noText)) SC.overlay(t, st, txt, projOf());
  const r = { f, year: +st.year.toFixed(2), spp, phase: st.phase || null, preset: st.preset || null, gl_ms: +ms.toFixed(1), post_ms: +(t1 - t0 - ms).toFixed(1), lod: ctx.city.stat(), tlod: ctx.terr.stat(), shadow_upd: shadowUpdates, budget: txt.budget(), overflow: txt.log.overflow.slice() };
  // V5b-2a (K §7.1): log chữ MỌI khung có thẻ/ảnh/nhãn neo (không chỉ khung đo) + đường dẫn neo (đầu đường dẫn ↔ điểm 3D, TL-Q4b)
  if (measure || txt.log.cards > 0 || txt.log.leaders.length) r.text = txt.contrast();
  if (txt.log.leaders.length) r.leaders = txt.log.leaders.slice();
  const t3 = performance.now(); r.img = txt.cv.toDataURL('image/jpeg', 0.95).slice(23); r.ms = { acc: +ms.toFixed(0), out: +(t2 - t0 - ms).toFixed(0), overlay: +(t3 - t2).toFixed(0), encode: +(performance.now() - t3).toFixed(0) };
  return r;
};
// chiếu điểm 3D → điểm ảnh; mảng trả về mang .w = điểm 3D ENU [E, cao, N] (text.js ghi vào log đường dẫn để đo lệch độc lập từ campath)
const projOf = () => (v) => { const p = v.clone().project(cam); if (!(p.z < 1 && p.z > -1)) return null; const a = [(p.x + 1) / 2 * C.W, (1 - p.y) / 2 * C.H]; a.w = [v.x, v.y, -v.z]; return a; };
// tỉ lệ diện tích NỘI DUNG có nghĩa trong khung (cả khung + vùng giữa 15–85 %) — đo trên mặt nạ dựng cùng máy/năm, không tự khai
let maskRT = null;
window.contentMask = (f, ov, png) => {
  const t = f / SC.fps, st = Object.assign(SC.state(t), ov || {}), U = ctx.U; U.uYear.value = st.year; U.uDim.value = 0; U.uT.value = t;
  applyCam(cam, st.cam); ctx.terr.update(cam); ctx.city.update(cam); if (ctx.trees) ctx.trees.update(cam); ctx.ships.update(st.year); SC.apply && SC.apply(st, t);
  const w = Math.round(C.W / 2), h = Math.round(C.H / 2); if (!maskRT) maskRT = new THREE.WebGLRenderTarget(w, h);
  const MH = (ctx.maskHide || []).filter((o) => o.visible); for (const o of MH) o.visible = false;   // V5b-2b: khói/sprite không vào mặt nạ (nền)
  U.uMask.value = 1; ctx.ws.water.visible = ctx.ws.sky.visible = false; const sm = R.shadowMap.enabled; R.shadowMap.enabled = false; const cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(); R.setClearColor(0x000000, 1);
  R.setRenderTarget(maskRT); R.clear(); R.render(scene, cam); const px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(maskRT, 0, 0, w, h, px); R.setRenderTarget(null);
  U.uMask.value = 0; ctx.ws.water.visible = ctx.ws.sky.visible = true; for (const o of MH) o.visible = true; R.shadowMap.enabled = sm; R.setClearColor(cc, ca);
  const ids = Object.assign({}, ctx.heroes.heroIds || {}, SC.heroIds || {}), hn = {};   // V5b-2b: cảnh thêm hero (lớp footprint có hid) for (const k in ids) hn[k] = 0;
  let n = 0, nc = 0, tc = 0, nf = 0, nh = 0, ng = 0; for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = (y * w + x) * 4, on = px[i] > 128 && px[i + 1] < 90, fb = px[i] < 90 && px[i + 1] > 128; n += on; nf += on || fb; ng += on && px[i + 1] > 30 && px[i + 2] === 0; if (x >= w * 0.15 && x < w * 0.85 && y >= h * 0.15 && y < h * 0.85) { tc++; nc += on; }
    if (on && px[i + 2] > 0) { nh++; for (const k in ids) if (Math.abs(px[i + 2] - ids[k]) < 0.5) hn[k]++; } }
  // content = HÌNH HỌC nội dung (toà, hero, tường, đường, tàu, xe/người); fabric = content + nền phố (mặt đất đô thị của năm đó: sân, phố, quảng trường)
  // V5b-2a: hero_pct = % khung của hero ĐANG KỂ (st.hero = id tên trong heroIds; không khai → mọi hero), hero_pct_by_id theo từng hero
  const P = (k) => +(k / (w * h) * 100).toFixed(2), by = {}; for (const k in hn) by[k] = P(hn[k]);
  let png_b64 = null; if (png) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'), im = g.createImageData(w, h);   // V5b-2a: ảnh mặt nạ (lật dọc về chiều ảnh) cho đo sáng công trình (TL-Q1c)
    for (let y = 0; y < h; y++) im.data.set(px.subarray((h - 1 - y) * w * 4, (h - y) * w * 4), y * w * 4); g.putImageData(im, 0, 0); png_b64 = cv.toDataURL('image/png').slice(22); }
  return { content_pct: +(n / (w * h) * 100).toFixed(1), content_center_pct: +(nc / tc * 100).toFixed(1), fabric_pct: +(nf / (w * h) * 100).toFixed(1), ghost_pct: +(ng / (w * h) * 100).toFixed(2), noi: st.noi || null, nam_khung: SC.namKhung ? SC.namKhung(st) : null,
    hero_id: st.hero || 'all', hero_pct: st.hero ? by[st.hero] : P(nh), hero_pct_by_id: by, phase: st.phase || null, preset: st.preset || null, year: +st.year.toFixed(2), png_b64 };
};
window.camLog = () => SC.camLog();
// V5b-2b (hero.js): RGB không chữ; điểm neo đặt tên (SC.anchors: {tên: [E, cao, N] | () => …}) chuẩn hoá 0..1 + lớp chữ ghi lại (_tl); siêu dữ liệu khung
window.finalize = (f) => pipe.finalize(f);
window.anchorsAt = () => { if (!last) return null; const { t, st } = last, P = projOf(), out = {};
  for (const [k, a] of Object.entries(SC.anchors || {})) { const w = typeof a === 'function' ? a(t, st) : a; const q = w ? P(new THREE.Vector3(w[0], w[1], -w[2])) : null;
    out[k] = q && q[0] >= -0.05 * C.W && q[0] <= 1.05 * C.W && q[1] >= -0.05 * C.H && q[1] <= 1.05 * C.H ? [+(q[0] / C.W).toFixed(4), +(q[1] / C.H).toFixed(4), 1] : [0, 0, 0]; }
  rec.begin(); SC.overlay(t, st, rec, P); out._tl = rec.data(); return out; };
window.frameMeta = () => { if (!last) return null; const { f, t, st } = last, c = st.cam, g = Math.max(0, ctx.terr.hAt(c.p[0], c.p[2])), agl = c.p[1] - g;
  return { f, t: +t.toFixed(3), agl_m: +agl.toFixed(1), agl_km: +(agl / 1000).toFixed(4), spp: C.tech.spp === 'adaptive' ? st.spp : +C.tech.spp, phase: st.phase || null, preset: st.preset || null, vai: st.vai || null,
    year: +st.year.toFixed(3), clock: st.clock ? st.clock.s : null, noi: st.noi || null, hero: st.hero || null, sun: st.sun ? { el: +st.sun.el.toFixed(2), az: +st.sun.az.toFixed(2) } : null }; };
window.budgetAll = () => { const out = []; for (let f = 0; f < SC.N; f++) { const t = f / SC.fps, st = SC.state(t); applyCam(cam, st.cam); txt.begin(null); SC.overlay(t, st, txt, projOf());
  out.push(Object.assign({ f }, txt.budget(), { overflow: txt.log.overflow.length, msg: txt.log.overflow.slice(0, 2), roles: txt.roles() }, txt.log.leaders.length ? { leaders: txt.log.leaders.slice() } : {})); } return out; };
window.grammarLog = () => (SC.grammarLog ? SC.grammarLog() : null);
window.ready = true;

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
import { fitShadowView, makeSSAO } from './light6.js';   // V6: bóng khít khung nhìn + SSAO + chỉnh màu

let C, R, pipe, scene, cam, SC, ctx, outScene, quadCam, txt, rec, HERO = false, last = null, stats = {}, V6 = null, SSAO = null, aoHide = [], v6Key = null, v6Shadow = null, REFL = null;
// V5b-2b (V5B2A §8.2): trang dựng được gọi từ scripts/k2/hero.js ('tl/<cảnh>', opt = {pack, lut, lutMode, vib, look, photo, tech, layers, …}) —
//  chế độ HERO: khung KHÔNG chữ (window.finalize → RGB), lớp chữ ghi lại bằng record.js vào anchorsAt()._tl để scripts/k2/lib/k2.js vẽ; frameMeta() mỗi khung (AGL, SPP, pha).
function heroCfg(c) { const o = c.opt || {}; return { W: c.W, H: c.H, hero: c.hero, scene: c.hero.split('/')[1], opt: o, pack: `/cache/scene/${o.pack || 'gib'}/pack/`, lut: '/cache/lut/' + (o.lut || 'k2-a-thep-lanh') + '.cube',
  lutMode: o.lutMode ?? 1, vib: o.vib, look: o.look || {}, photo: o.photo === undefined ? '/cache/loc/ng_crop.jpg' : o.photo, tech: o.tech || {}, lutK: o.lutK ?? 1 }; }
window.setup = async (cfg) => {
  if (cfg.hero) { HERO = true; cfg = heroCfg(cfg); }
  C = cfg; const T = Object.assign({ lod: true, ao: true, shadowCache: true, spp: 'adaptive', shadowRes: 4096, city: true, trees: true, baked: false, lambert: true } /* baked: nhiễu nướng sẵn (chống lặp ô) — đo lại 16/10 không nhanh hơn nhiễu thủ tục → tắt mặc định */, cfg.tech || {}); C.tech = T;
  const t0 = performance.now(), base = cfg.pack;
  const M = await loadJSON(base + 'meta.json');
  R = createRenderer(cfg.W, cfg.H); R.shadowMap.type = THREE.PCFSoftShadowMap; R.shadowMap.autoUpdate = !T.shadowCache;
  const lut = await loadCube(cfg.lut);   /* V5b-1b: LUT chọn bằng số đo (reports/V5B1B-BAO-CAO.md §2) */
  const LU = { tLut: { value: lut.tex }, uLutK: { value: cfg.lutK ?? 1.0 }, uLutN: { value: lut.N }, uVig: { value: 0.16 }, uAA: { value: 0 }, uLutMode: { value: cfg.lutMode ?? 1 }, uVib: { value: cfg.vib ?? 0.35 }, uV6: { value: 0 }, uV6c: { value: new THREE.Vector3(1, 0.35, 1) } };
  pipe = createPipeline(R, cfg.W, cfg.H, { exposure: cfg.exposure ?? 1.0, gradeGLSL: GRADE_GLSL, uniforms: LU });
  quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1); outScene = new THREE.Scene(); outScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), pipe.outMat));
  scene = new THREE.Scene();
  const mod = await import(`./scenes/${cfg.scene}.js`);
  // V6 (V2D-1): cảnh khai V6 = {…} (hoặc tech.v6) → bóng khít khung 8192², SSAO hai tầng, chỉnh màu V6, tỉ lệ nắng/trời; tech.v6 === false tắt (đo trước/sau)
  V6 = T.v6 === false ? null : (T.v6 || mod.V6 ? Object.assign({ shadowRes: 8192, sunK: 1.0, hemiK: 1.0, grade: [1.0, 0.35, 1.0], ao: {} }, mod.V6 || {}, typeof T.v6 === 'object' ? T.v6 : {}) : null);
  if (V6) { T.shadowRes = V6.shadowRes; LU.uV6.value = 1; LU.uV6c.value.set(...V6.grade); }   // V5b-2c: nạp cảnh TRƯỚC địa hình/ánh sáng — cảnh khai TERRAIN (vách bắc Rock), LOOK mà không đổi cảnh cũ
  if (mod.GRADE) { if (mod.GRADE.vib != null && cfg.vib == null) LU.uVib.value = mod.GRADE.vib; if (mod.GRADE.exposure != null && pipe.setExposure) pipe.setExposure(mod.GRADE.exposure); }   // V5b-2c (I5): vibrance riêng cảnh (opt.vib của shot vẫn thắng)
  const sunEl = 31 * Math.PI / 180, sunAz = 238 * Math.PI / 180;   // nắng chiều hướng tây-nam (nổi mặt tây Rock, vách bắc vào bóng)
  const sunDir = new THREE.Vector3(Math.sin(sunAz) * Math.cos(sunEl), Math.sin(sunEl), -Math.cos(sunAz) * Math.cos(sunEl)).normalize();
  const U = { uMask: { value: 0 }, uYear: { value: 1700 }, uDim: { value: 0 }, uSample: { value: 0 }, uT: { value: 0 }, uAOon: { value: T.ao ? 1 : 0 }, uBaked: { value: T.baked ? 1 : 0 }, lambert: T.lambert, terrainLod: T.terrainLod, treeDetail: T.treeDetail, groundNear: T.groundNear ?? 1, sunDir };
  // V5b-1b: sương CHỈ ở xa, ngả xanh (cùng màu chân trời trời mới), mật độ thấp hơn → cận/trung cảnh trong; nắng thấp có hướng mạnh hơn,
  // ánh trời xanh làm bóng ngả lạnh (tương phản ấm–lạnh), bóng sắc hơn (bán kính PCF 3 → 1,5).
  const L = Object.assign({ fogC: [0.60, 0.74, 0.90], fogD: 0.0000175, hemiSky: '#9cbcf0', hemiGnd: '#7a6648', hemiI: 0.62, sunC: '#ffe3b8', sunI: 3.3, shR: 1.5 }, cfg.look || {}, mod.LOOK || {}); C.look = L;   /* V5b-2c: cảnh khai LOOK (ánh sáng riêng) */
  if (V6) { L.sunI *= V6.sunK; L.hemiI *= V6.hemiK; }   // V6: nắng mạnh hơn / trời dịu hơn → bóng đổ đọc được (AO thay phần tối của ánh trời)
  const fogC = new THREE.Color(...L.fogC); scene.fog = new THREE.FogExp2(fogC, L.fogD);
  const hemi = new THREE.HemisphereLight(L.hemiSky, L.hemiGnd, L.hemiI); scene.add(hemi);
  const sun = new THREE.DirectionalLight(L.sunC, L.sunI); sun.castShadow = T.shadows !== false; sun.shadow.mapSize.set(T.shadowRes, T.shadowRes); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.6; sun.shadow.radius = L.shR;
  scene.add(sun, sun.target);
  const terr = await makeTerrain(base, M, U, Object.assign({}, mod.TERRAIN || {}, (cfg.opt && cfg.opt.terrain) || {})); scene.add(terr.group);
  const ws = makeWaterSky(U, scene.fog, L.skyHor, V6 ? { wave: V6.wave ?? 1.6 } : null);   /* ctx.ws: mặt nạ nội dung ẩn nước/trời */ scene.add(ws.water, ws.sky);
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
  ctx = { hemi, THREE, U, M, terr, city, roads, trees, heroes, ships, sun, sunDir, cam, photo, lines: LINES, W: cfg.W, H: cfg.H, track, scene, maskify, base, opt: cfg.opt || {}, makeCity, loadJSON, R };   /* V5b-2b: opt của shot + makeCity (lớp footprint M9) */   /* V5b-2a: cảnh thêm phần tử 3D riêng (overlay3d.js) */
  if (V6) { ctx.v6people = V6.people !== false; ctx.v6smoke = V6.smoke !== false; }   // V6: người/quân có khớp (people.js), khói giả thể tích (smoke6.js)
  SC = await mod.build(ctx);
  // mặt nạ nội dung: hero + đường = nội dung (city/terrain tự có mã mặt nạ); cây = nền
  const mk = (obj, v, hid = 0) => obj && obj.traverse((o) => { if (o.isMesh) for (const m of [].concat(o.material)) if (!m.isShaderMaterial) maskify(m, U, v, hid); });
  for (const [k, objs] of Object.entries(heroes.heroParts || {})) for (const o of objs) mk(o, 1, heroes.heroIds[k]);   // V5b-2a: hero có id (trước mk chung — maskify bỏ qua vật liệu đã gắn)
  mk(heroes.group, 1); mk(roads.mesh, 1); mk(ships.group, 1); if (trees) mk(trees.group, 0); mk(terr.group.children.find((o) => o.material && o.material.map), 0);
  ctx.ws = ws;
  // V6: PHẢN CHIẾU MẶT NƯỚC — máy gương (đối xứng qua y = 0, máy đúng chiều), nửa độ phân giải, cắt mọi thứ dưới mặt nước; nền trong suốt (trời dùng skyCol)
  if (V6 && V6.refl !== false) { const rt = new THREE.WebGLRenderTarget(Math.round(cfg.W / 2), Math.round(cfg.H / 2), { type: THREE.HalfFloatType, colorSpace: THREE.LinearSRGBColorSpace });
    REFL = { rt, cam: new THREE.PerspectiveCamera(38, cfg.W / cfg.H, 5, 80000), clip: [new THREE.Plane(new THREE.Vector3(0, 1, 0), -0.3)], ms: 0 }; ws.water.material.uniforms.tRefl.value = rt.texture; ws.water.material.uniforms.uRefl.value = 1; }
  // V6: SSAO + danh sách vật KHÔNG vào lượt pháp tuyến (nước, trời, khói/sprite, vật liệu không có nhánh uMask)
  if (V6) { SSAO = makeSSAO(R, cfg.W, cfg.H, V6.ao); const hid = new Set([ws.water, ws.sky]);
    scene.traverse((o) => { if (!(o.isMesh || o.isSprite || o.isPoints || o.isLine)) return; const ms = [].concat(o.material || []); if (o.isSprite || !ms.some((m) => m && (m.userData.masked || m.userData.v6n))) hid.add(o); });
    aoHide = [...hid]; }
  stats = { cut: stats.cut || 0, ships: ships.n, styles: city.styles, corner_towers: heroes.cornerTowers, load_s: +((performance.now() - t0) / 1000).toFixed(2), terrain_tris: terr.tris, city_tris: city.tris, city_tiles: city.nTiles, buildings: B.length, roads_tris: roads.tris, trees: trees ? trees.n : 0,
    renderer: (() => { const gl = R.getContext(), e = gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER); })(), tech: T, N: SC.N, scene_meta: SC.meta || null, cliff: terr.cliffStat || null };
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
function applySun(st) { if (!st.sun) return; const d = sunDirENU(st.sun); if (Math.abs(d[0] - ctx.sunDir.x) + Math.abs(d[1] - ctx.sunDir.y) + Math.abs(d[2] - ctx.sunDir.z) > 1e-6) { ctx.sunDir.set(...d).normalize(); shadowKey = null; }
  // V5b-2c (F1 chu kỳ ngày): nắng thấp → yếu + ngả cam, ánh trời giảm (chỉ khi cảnh khai st.dayCycle; cảnh cũ giữ ánh sáng cố định)
  if (st.dayCycle) { const el = st.sun.el, k = Math.max(0, Math.min(1, (el + 2) / 14)), w = Math.max(0, Math.min(1, (18 - el) / 18));
    ctx.sun.intensity = C.look.sunI * (0.15 + 0.85 * k); ctx.sun.color.set(C.look.sunC).lerp(new THREE.Color('#ff9a52'), 0.75 * w * w); ctx.hemi.intensity = C.look.hemiI * (0.35 + 0.65 * k); } }
window.renderFrame = async (f, measure, ov) => {
  const t = f / SC.fps, st = Object.assign(SC.state(t), ov || {}); const U = ctx.U;   // ov: ghi đè trạng thái (khung kiểm: năm/máy cố định)
  applySun(st); last = { f, t, st };
  U.uYear.value = st.year; U.uDim.value = st.dim || 0; U.uT.value = t;
  applyCam(cam, st.cam); ctx.terr.update(cam); ctx.city.update(cam); if (ctx.trees) ctx.trees.update(cam); ctx.ships.update(st.year); SC.apply && SC.apply(st, t);
  const spp = C.tech.spp === 'adaptive' ? st.spp : +C.tech.spp;
  pipe.outMat.uniforms.uAA.value = spp === 1 ? 1 : 0;
  const t0 = performance.now();
  let shadowDone = false;
  if (V6) { applyCam(cam, st.cam); const fs = fitShadowView(ctx.sun, ctx.sunDir, cam, { res: C.tech.shadowRes, dmax: V6.shadowDmax || 3000 }); v6Shadow = fs; const key = fs.key + '|' + ctx.sunDir.toArray().map((x) => x.toFixed(5)).join(',') + '|' + (Math.round(st.year * 4) / 4);
    if (!C.tech.shadowCache || key !== v6Key) { R.shadowMap.needsUpdate = true; shadowUpdates++; } v6Key = key; }
  else if (C.tech.shadowCache) { if (fitShadow(st)) { R.shadowMap.needsUpdate = true; shadowUpdates++; } }
  else fitShadow(st);
  if (REFL) { const t0r = performance.now(), mc = REFL.cam; cam.updateMatrixWorld(); mc.fov = cam.fov; mc.aspect = cam.aspect; mc.near = cam.near; mc.far = cam.far; mc.updateProjectionMatrix();
    const dir = new THREE.Vector3(); cam.getWorldDirection(dir); mc.position.set(cam.position.x, -cam.position.y, cam.position.z); mc.up.set(0, 1, 0); mc.lookAt(mc.position.x + dir.x, mc.position.y - dir.y, mc.position.z + dir.z); mc.updateMatrixWorld();
    const wv = ctx.ws.water.visible, sv = ctx.ws.sky.visible; ctx.ws.water.visible = ctx.ws.sky.visible = false; const cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(), sm = R.shadowMap.autoUpdate, nu = R.shadowMap.needsUpdate;
    R.shadowMap.autoUpdate = false; R.shadowMap.needsUpdate = false; R.clippingPlanes = REFL.clip; R.setRenderTarget(REFL.rt); R.setClearColor(0x000000, 0); R.clear(); R.render(scene, mc); R.setRenderTarget(null); R.clippingPlanes = [];
    R.setClearColor(cc, ca); R.shadowMap.autoUpdate = sm; R.shadowMap.needsUpdate = nu; ctx.ws.water.visible = wv; ctx.ws.sky.visible = sv;
    ctx.ws.water.material.uniforms.uReflVP.value.multiplyMatrices(mc.projectionMatrix, mc.matrixWorldInverse); REFL.ms = performance.now() - t0r; }
  const ms = pipe.accumulate(scene, cam, spp, (i) => { U.uSample.value = i + f * 0.137; if ((C.tech.shadowCache || V6) && i > 0) R.shadowMap.needsUpdate = false; });
  const aoMs = SSAO ? SSAO.apply(scene, cam, pipe.accRT, U.uMask, aoHide) : 0;   // V6: AO nhân vào bộ tích luỹ HDR
  R.setRenderTarget(null); pipe.outMat.uniforms.frame.value = f; R.render(outScene, quadCam);
  const t1 = performance.now();
  if (HERO) return { f, spp, gl_ms: +ms.toFixed(1), ao_ms: +aoMs.toFixed(1), phase: st.phase || null };   // chế độ hero: chữ do k2.js vẽ (anchorsAt()._tl)
  const t2 = performance.now(); txt.begin(R.domElement);
  if (!(ov && ov.noText)) SC.overlay(t, st, txt, projOf());
  const r = { f, year: +st.year.toFixed(2), spp, phase: st.phase || null, preset: st.preset || null, gl_ms: +ms.toFixed(1), ao_ms: +aoMs.toFixed(1), shadow: v6Shadow, post_ms: +(t1 - t0 - ms - aoMs).toFixed(1), lod: ctx.city.stat(), tlod: ctx.terr.stat(), shadow_upd: shadowUpdates, budget: txt.budget(), overflow: txt.log.overflow.slice() };
  // V5b-2a (K §7.1): log chữ MỌI khung có thẻ/ảnh/nhãn neo (không chỉ khung đo) + đường dẫn neo (đầu đường dẫn ↔ điểm 3D, TL-Q4b)
  if (measure || txt.log.cards > 0 || txt.log.leaders.length || txt.log.ai) r.text = txt.contrast();
  if (SC.aiTexture) r.ai_texture = !!SC.aiTexture(st, t);
  if (SC.troops) r.quan = SC.troops(); if (SC.song) r.song = SC.song();   // V6: số người/quân đang hiện (đo người/khung, BC3)   // V6: khung có vân AI (HC7) — log cho K-LAI-1/2
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
  const ids = Object.assign({}, ctx.heroes.heroIds || {}, SC.heroIds || {}), hn = {};   /* V5b-2b: cảnh thêm hero (lớp footprint có hid) */ for (const k in ids) hn[k] = 0;
  // V5b-2c (luật bố cục I3): 'trống' = nước (điểm đen DƯỚI chân trời: nước/trời bị ẩn ở lượt mặt nạ) + đất tự nhiên bằng (lam 0,5 ở terrain.js); trời = đen TRÊN chân trời
  cam.updateMatrixWorld(); const ivp = new THREE.Matrix4().multiplyMatrices(cam.matrixWorld, cam.projectionMatrixInverse), rv = new THREE.Vector3(); let nWater = 0, nFlat = 0, nSky = 0, nRock = 0, nSlope = 0;
  const below = new Uint8Array(w * h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x += 8) { rv.set((x + 0.5) / w * 2 - 1, (y + 0.5) / h * 2 - 1, 0.5).applyMatrix4(ivp).sub(cam.position); const b = rv.y < 0 ? 1 : 0; for (let k = x; k < Math.min(w, x + 8); k++) below[y * w + k] = b; }
  let n = 0, nc = 0, tc = 0, nf = 0, nh = 0, ng = 0; for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = (y * w + x) * 4, on = px[i] > 128 && px[i + 1] < 90, fb = px[i] < 90 && px[i + 1] > 128; n += on; nf += on || fb; ng += on && px[i + 1] > 30 && px[i + 2] === 0; if (x >= w * 0.15 && x < w * 0.85 && y >= h * 0.15 && y < h * 0.85) { tc++; nc += on; }
    if (!on && !fb) { const blk = px[i] < 20 && px[i + 1] < 20 && px[i + 2] < 20; if (blk) { if (below[y * w + x]) nWater++; else nSky++; } else if (px[i + 2] > 90 && px[i + 2] < 160) nFlat++; else if (px[i + 2] >= 160 && px[i + 2] < 200) nSlope++; else if (px[i + 2] > 40 && px[i + 2] <= 90) nWater++; else if (px[i + 2] >= 200) nRock++; }   /* V6 (V2D-5): sườn đồi bằng > 30 m (lam 0,70) tách khỏi cỏ trống */   /* V5b-2d: đất dốc tự nhiên riêng */
    if (on && px[i + 2] > 0) { nh++; for (const k in ids) if (Math.abs(px[i + 2] - ids[k]) < 0.5) hn[k]++; } }
  // content = HÌNH HỌC nội dung (toà, hero, tường, đường, tàu, xe/người); fabric = content + nền phố (mặt đất đô thị của năm đó: sân, phố, quảng trường)
  // V5b-2a: hero_pct = % khung của hero ĐANG KỂ (st.hero = id tên trong heroIds; không khai → mọi hero), hero_pct_by_id theo từng hero
  const P = (k) => +(k / (w * h) * 100).toFixed(2), by = {}; for (const k in hn) by[k] = P(hn[k]);
  let png_b64 = null; if (png) { const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'), im = g.createImageData(w, h);   // V5b-2a: ảnh mặt nạ (lật dọc về chiều ảnh) cho đo sáng công trình (TL-Q1c)
    for (let y = 0; y < h; y++) im.data.set(px.subarray((h - 1 - y) * w * 4, (h - y) * w * 4), y * w * 4); g.putImageData(im, 0, 0); png_b64 = cv.toDataURL('image/png').slice(22); }
  return { empty_pct: +((nWater + nFlat) / (w * h) * 100).toFixed(1), water_pct: +(nWater / (w * h) * 100).toFixed(1), flat_nat_pct: +(nFlat / (w * h) * 100).toFixed(1), sky_pct: +(nSky / (w * h) * 100).toFixed(1), dat_doc_pct: +(nRock / (w * h) * 100).toFixed(1), suon_pct: +(nSlope / (w * h) * 100).toFixed(1), co_trong_pct: +(nFlat / (w * h) * 100).toFixed(1), nuoc_pct: +(nWater / (w * h) * 100).toFixed(1), troi_pct: +(nSky / (w * h) * 100).toFixed(1),   /* V6 (K-1.15 §8b): tên trường cho BC2 */ bo_pct: +(100 - (nWater + nSky) / (w * h) * 100).toFixed(1),   /* V5b-2d: bờ = mọi thứ trừ nước + trời */ content_pct: +(n / (w * h) * 100).toFixed(1), content_center_pct: +(nc / tc * 100).toFixed(1), fabric_pct: +(nf / (w * h) * 100).toFixed(1), ghost_pct: +(ng / (w * h) * 100).toFixed(2), noi: st.noi || null, nam_khung: SC.namKhung ? SC.namKhung(st) : null,
    hero_id: st.hero || 'all', hero_pct: st.hero ? by[st.hero] : P(nh), hero_pct_by_id: by, phase: st.phase || null, preset: st.preset || null, year: +st.year.toFixed(2), png_b64 };
};
window.camLog = () => SC.camLog();
// V6 bước 7 (bản TỐT NHẤT, scripts/k2tl/export6.js): xuất cảnh + các lượt + chỉnh màu ảnh HDR ghép bằng chính đường ống này
let EXP = null;
window.exportFrame = async (o) => { const { makeExporter } = await import('./export6.js'); EXP = makeExporter({ scene, cam, ctx, R, pipe, C, SC }); return EXP.frame(o || {}); };
window.exportBuf = (i) => EXP.buf(i);
const f32b64 = (a) => { const u8 = new Uint8Array(a.buffer); let s = ''; for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000)); return btoa(s); };
window.passFrame = async (f, pass) => {   // trạng thái khung f đã áp (renderFrame); trả RGBA float32 base64 (hàng từ dưới lên)
  const W = C.W, H = C.H, px = new Float32Array(W * H * 4), hideL = (ctx.maskHide || []).filter((o) => o.visible), U = ctx.U;
  if (pass === 'albedo' || pass === 'nosmoke') { for (const o of hideL) o.visible = false; const wv = ctx.ws.water.visible, sv = ctx.ws.sky.visible;
    if (pass === 'albedo') { ctx.ws.water.visible = ctx.ws.sky.visible = false; U.uMask.value = 3; const fog = scene.fog; scene.fog = null; const sm = R.shadowMap.enabled; R.shadowMap.enabled = false;
      pipe.accumulate(scene, cam, 4, () => {}); U.uMask.value = 0; scene.fog = fog; R.shadowMap.enabled = sm; }
    else { R.shadowMap.needsUpdate = true; pipe.accumulate(scene, cam, 4, (i) => { U.uSample.value = i + f * 0.137; if (i > 0) R.shadowMap.needsUpdate = false; }); if (SSAO) SSAO.apply(scene, cam, pipe.accRT, U.uMask, aoHide); }
    ctx.ws.water.visible = wv; ctx.ws.sky.visible = sv; for (const o of hideL) o.visible = true; R.readRenderTargetPixels(pipe.accRT, 0, 0, W, H, px); R.setRenderTarget(null); return f32b64(px); }
  if (pass === 'smoke') {   // độ sâu cảnh (không ghi màu) rồi CHỈ khói, nền trong suốt
    const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.FloatType, depthBuffer: true }), keep = new Set(); for (const g of hideL) g.traverse((o) => keep.add(o));
    const ac = R.autoClear, cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(); R.setRenderTarget(rt); R.setClearColor(0x000000, 0); R.clear();
    for (const o of hideL) o.visible = false; const dm = new THREE.MeshBasicMaterial({ colorWrite: false }); scene.overrideMaterial = dm; const sv = ctx.ws.sky.visible; ctx.ws.sky.visible = false; R.render(scene, cam); scene.overrideMaterial = null; ctx.ws.sky.visible = sv;
    const vis = []; scene.traverse((o) => { if ((o.isMesh || o.isSprite || o.isPoints) && !keep.has(o) && o.visible) { vis.push(o); o.visible = false; } }); for (const o of hideL) o.visible = true;
    R.autoClear = false; R.render(scene, cam); R.autoClear = ac; for (const o of vis) o.visible = true; R.setClearColor(cc, ca);
    R.readRenderTargetPixels(rt, 0, 0, W, H, px); R.setRenderTarget(null); rt.dispose(); return f32b64(px); }
  throw new Error('lượt ' + pass);
};
window.gradeHDR = async (f, b64, withText) => {   // HDR tuyến tính ghép (RGBA float32, hàng từ dưới lên) → tone ACES + grade + hạt như khung thường (+ lớp chữ)
  const W = C.W, H = C.H, bin = atob(b64), u8 = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
  const tex = new THREE.DataTexture(new Float32Array(u8.buffer), W, H, THREE.RGBAFormat, THREE.FloatType); tex.needsUpdate = true;
  const m = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, uniforms: { t: { value: tex } }, vertexShader: 'in vec3 position; out vec2 v; void main(){ v = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: 'precision highp float; uniform sampler2D t; in vec2 v; out vec4 o; void main(){ o = texture(t, v); }', depthTest: false, depthWrite: false });
  const sc = new THREE.Scene(); sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m)); R.setRenderTarget(pipe.accRT); R.render(sc, quadCam);
  pipe.outMat.uniforms.uAA.value = 0; R.setRenderTarget(null); pipe.outMat.uniforms.frame.value = f; R.render(outScene, quadCam);
  txt.begin(R.domElement); if (withText && last) SC.overlay(last.t, last.st, txt, projOf()); return txt.cv.toDataURL('image/png').slice(22); };
// V5b-2b (hero.js): RGB không chữ; điểm neo đặt tên (SC.anchors: {tên: [E, cao, N] | () => …}) chuẩn hoá 0..1 + lớp chữ ghi lại (_tl); siêu dữ liệu khung
window.finalize = (f) => pipe.finalize(f);
window.anchorsAt = () => { if (!last) return null; const { t, st } = last, P = projOf(), out = {};
  for (const [k, a] of Object.entries(SC.anchors || {})) { const w = typeof a === 'function' ? a(t, st) : a; const q = w ? P(new THREE.Vector3(w[0], w[1], -w[2])) : null;
    out[k] = q && q[0] >= -0.05 * C.W && q[0] <= 1.05 * C.W && q[1] >= -0.05 * C.H && q[1] <= 1.05 * C.H ? [+(q[0] / C.W).toFixed(4), +(q[1] / C.H).toFixed(4), 1] : [0, 0, 0]; }
  rec.begin(); SC.overlay(t, st, rec, P); out._tl = rec.data(); return out; };
// V5b-2c (M14/B4): DẤU CHÂN KHUNG MÁY trên mặt đất — 4 tia góc khung cắt mặt phẳng cao độ tâm nhìn (tia trên chân trời: cắt ở 25 km), đổi ENU → lon/lat (gần đúng phẳng quanh gốc gói)
function footprint() { cam.updateMatrixWorld(); const ivp = new THREE.Matrix4().multiplyMatrices(cam.matrixWorld, cam.projectionMatrixInverse), o = cam.position, out = [];
  const gl = last && last.st.cam ? Math.max(0, ctx.terr.hAt(last.st.cam.l[0], last.st.cam.l[2])) : 0, [lon0, lat0] = ctx.M.origin_ll || [-5.3487, 36.1513];
  for (const [x, y] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) { const d = new THREE.Vector3(x, y, 0.5).applyMatrix4(ivp).sub(o).normalize(); let k = d.y < -1e-4 ? (gl - o.y) / d.y : 25000; k = Math.min(k, 25000);
    const E = o.x + d.x * k, N = -(o.z + d.z * k); out.push([+(lon0 + E / (111320 * Math.cos(lat0 * Math.PI / 180))).toFixed(5), +(lat0 + N / 110574).toFixed(5)]); }
  return out; }
window.frameMeta = () => { if (!last) return null; const { f, t, st } = last, c = st.cam, g = Math.max(0, ctx.terr.hAt(c.p[0], c.p[2])), agl = c.p[1] - g;
  return { f, t: +t.toFixed(3), agl_m: +agl.toFixed(1), agl_km: +(agl / 1000).toFixed(4), spp: C.tech.spp === 'adaptive' ? st.spp : +C.tech.spp, phase: st.phase || null, preset: st.preset || null, vai: st.vai || null,
    year: +st.year.toFixed(3), clock: st.clock ? st.clock.s : null, noi: st.noi || null, hero: st.hero || null, sun: st.sun ? { el: +st.sun.el.toFixed(2), az: +st.sun.az.toFixed(2) } : null, quan: SC.troops ? SC.troops() : null, song: SC.song ? SC.song() : null, foot: footprint(), ai_texture: SC.aiTexture ? !!SC.aiTexture(st, t) : false }; };   /* V6: khung có vân AI (K-LAI-1) */   /* V5b-2c: lớp sống — số vật chuyển động theo loại */   /* V5b-2b (AC1): khối quân hiện / ẩn vì khói */
window.budgetAll = () => { const out = []; for (let f = 0; f < SC.N; f++) { const t = f / SC.fps, st = SC.state(t); applyCam(cam, st.cam); txt.begin(null); SC.overlay(t, st, txt, projOf());
  out.push(Object.assign({ f }, txt.budget(), { overflow: txt.log.overflow.length, msg: txt.log.overflow.slice(0, 2), roles: txt.roles() }, txt.log.leaders.length ? { leaders: txt.log.leaders.slice() } : {})); } return out; };
window.grammarLog = () => (SC.grammarLog ? SC.grammarLog() : null);
window.ready = true;

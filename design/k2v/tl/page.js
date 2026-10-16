// K2V tl · TRANG DỰNG xương sống thời gian (driver: scripts/k2tl/render.js). Chromium headless + SwiftShader (chỉ CPU).
// Đường ống: post.js dùng chung (tích luỹ SPP có jitter → tone ACES → grade [lọc cạnh SPP1 + LUT A + vignette] → grain cố định),
// rồi lớp 2D (text.js: năm, chỉ số, thẻ, ảnh chú thích) vẽ SAU (chữ không qua LUT/grain), đo ngân sách chữ + tương phản trên điểm ảnh thật.
// Kỹ thuật đo được bật/tắt qua cfg.tech: lod, ao (AO nướng theo năm), shadowCache (bóng 1 lần/khung + giữ khi cảnh không đổi), spp ('adaptive' | số), shadowRes.
import { THREE, track, loadJSON, loadImg } from './core.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { makeTerrain } from './terrain.js';
import { makeWaterSky } from './water.js';
import { makeCity } from './city.js';
import { makeTrees, makeRoads } from './nature.js';
import { makeHeroes } from './heroes.js';
import { applyCam } from './campath.js';
import { makeText } from './text.js';
import { loadCube, GRADE_GLSL } from './lut.js';

let C, R, pipe, scene, cam, SC, ctx, outScene, quadCam, txt, stats = {};
window.setup = async (cfg) => {
  C = cfg; const T = Object.assign({ lod: true, ao: true, shadowCache: true, spp: 'adaptive', shadowRes: 4096, city: true, trees: true, baked: false, lambert: true } /* baked: nhiễu nướng sẵn (chống lặp ô) — đo lại 16/10 không nhanh hơn nhiễu thủ tục → tắt mặc định */, cfg.tech || {}); C.tech = T;
  const t0 = performance.now(), base = cfg.pack;
  const M = await loadJSON(base + 'meta.json');
  R = createRenderer(cfg.W, cfg.H); R.shadowMap.type = THREE.PCFSoftShadowMap; R.shadowMap.autoUpdate = !T.shadowCache;
  const lut = await loadCube(cfg.lut);
  const LU = { tLut: { value: lut.tex }, uLutK: { value: cfg.lutK ?? 1.0 }, uLutN: { value: lut.N }, uVig: { value: 0.16 }, uAA: { value: 0 } };
  pipe = createPipeline(R, cfg.W, cfg.H, { exposure: cfg.exposure ?? 1.0, gradeGLSL: GRADE_GLSL, uniforms: LU });
  quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1); outScene = new THREE.Scene(); outScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), pipe.outMat));
  scene = new THREE.Scene();
  const sunEl = 31 * Math.PI / 180, sunAz = 238 * Math.PI / 180;   // nắng chiều hướng tây-nam (nổi mặt tây Rock, vách bắc vào bóng)
  const sunDir = new THREE.Vector3(Math.sin(sunAz) * Math.cos(sunEl), Math.sin(sunEl), -Math.cos(sunAz) * Math.cos(sunEl)).normalize();
  const U = { uYear: { value: 1700 }, uDim: { value: 0 }, uSample: { value: 0 }, uT: { value: 0 }, uAOon: { value: T.ao ? 1 : 0 }, uBaked: { value: T.baked ? 1 : 0 }, lambert: T.lambert, terrainLod: T.terrainLod, treeDetail: T.treeDetail, sunDir };
  const fogC = new THREE.Color(0.78, 0.84, 0.90); scene.fog = new THREE.FogExp2(fogC, 0.000026);
  scene.add(new THREE.HemisphereLight('#bcd2ee', '#6d5f4c', 0.85));
  const sun = new THREE.DirectionalLight('#ffeed6', 2.6); sun.castShadow = T.shadows !== false; sun.shadow.mapSize.set(T.shadowRes, T.shadowRes); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.6; sun.shadow.radius = 3;
  scene.add(sun, sun.target);
  const terr = await makeTerrain(base, M, U); scene.add(terr.group);
  const ws = makeWaterSky(U, scene.fog); scene.add(ws.water, ws.sky);
  let B = T.city ? await loadJSON(base + 'buildings.json') : [];
  if (T.copies > 1) { const B0 = B; B = []; for (let k = 0; k < T.copies; k++) for (const b of B0) B.push(k ? [b[0], b[1], b[2], b[3], b[4], b[5], b[6].map(([e, n]) => [e + ((k % 4) - 1.5) * 3000, n + 4500 + Math.floor(k / 4) * 3500])] : b); }   /* thử tải: nhân bản toà (đo trần toà/cảnh) */
  const city = makeCity(B, U, { lod: T.lod }); scene.add(city.group);
  const roads = makeRoads(await loadJSON(base + 'roads.json'), terr.hAt, U); scene.add(roads.mesh);
  const trees = T.trees ? makeTrees(new Float32Array(await (await fetch(base + 'trees.f32')).arrayBuffer()), terr.hAt, U, { lod: T.lod }) : null; if (trees) scene.add(trees.group);
  const heroes = makeHeroes(await loadJSON(base + 'heroes.json'), terr.hAt, U, terr); scene.add(heroes.group);
  cam = new THREE.PerspectiveCamera(38, cfg.W / cfg.H, 5, 80000);
  txt = makeText(cfg.W, cfg.H);
  const photo = cfg.photo ? await loadImg(cfg.photo) : null;
  const mod = await import(`./scenes/${cfg.scene}.js`);
  ctx = { THREE, U, M, terr, city, roads, trees, heroes, sun, sunDir, cam, photo, lines: await loadJSON(base + 'lines.json'), W: cfg.W, H: cfg.H, track };
  SC = await mod.build(ctx);
  stats = { load_s: +((performance.now() - t0) / 1000).toFixed(2), terrain_tris: terr.tris, city_tris: city.tris, city_tiles: city.nTiles, buildings: B.length, roads_tris: roads.tris, trees: trees ? trees.n : 0,
    renderer: (() => { const gl = R.getContext(), e = gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER); })(), tech: T, N: SC.N };
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
window.renderFrame = async (f, measure, ov) => {
  const t = f / SC.fps, st = Object.assign(SC.state(t), ov || {}); const U = ctx.U;   // ov: ghi đè trạng thái (khung kiểm: năm/máy cố định)
  U.uYear.value = st.year; U.uDim.value = st.dim || 0; U.uT.value = t;
  applyCam(cam, st.cam); ctx.terr.update(cam); ctx.city.update(cam); if (ctx.trees) ctx.trees.update(cam); SC.apply && SC.apply(st, t);
  const spp = C.tech.spp === 'adaptive' ? st.spp : +C.tech.spp;
  pipe.outMat.uniforms.uAA.value = spp === 1 ? 1 : 0;
  const t0 = performance.now();
  let shadowDone = false;
  if (C.tech.shadowCache) { if (fitShadow(st)) { R.shadowMap.needsUpdate = true; shadowUpdates++; } }
  else fitShadow(st);
  const ms = pipe.accumulate(scene, cam, spp, (i) => { U.uSample.value = i + f * 0.137; if (C.tech.shadowCache && i > 0) R.shadowMap.needsUpdate = false; });
  R.setRenderTarget(null); pipe.outMat.uniforms.frame.value = f; R.render(outScene, quadCam);
  const t1 = performance.now();
  const t2 = performance.now(); txt.begin(R.domElement); const proj = (v) => { const p = v.clone().project(cam); return p.z < 1 && p.z > -1 ? [(p.x + 1) / 2 * C.W, (1 - p.y) / 2 * C.H] : null; };
  if (!(ov && ov.noText)) SC.overlay(t, st, txt, proj);
  const r = { f, year: +st.year.toFixed(2), spp, gl_ms: +ms.toFixed(1), post_ms: +(t1 - t0 - ms).toFixed(1), lod: ctx.city.stat(), tlod: ctx.terr.stat(), shadow_upd: shadowUpdates, budget: txt.budget(), overflow: txt.log.overflow.slice() };
  if (measure) r.text = txt.contrast();
  const t3 = performance.now(); r.img = txt.cv.toDataURL('image/jpeg', 0.95).slice(23); r.ms = { acc: +ms.toFixed(0), out: +(t2 - t0 - ms).toFixed(0), overlay: +(t3 - t2).toFixed(0), encode: +(performance.now() - t3).toFixed(0) };
  return r;
};
window.camLog = () => SC.camLog();
window.budgetAll = () => { const out = []; for (let f = 0; f < SC.N; f++) { const t = f / SC.fps, st = SC.state(t); applyCam(cam, st.cam); txt.begin(null); const proj = (v) => { const p = v.clone().project(cam); return p.z < 1 && p.z > -1 ? [(p.x + 1) / 2 * C.W, (1 - p.y) / 2 * C.H] : null; }; SC.overlay(t, st, txt, proj); out.push(Object.assign({ f }, txt.budget(), { overflow: txt.log.overflow.length, msg: txt.log.overflow.slice(0, 2) })); } return out; };
window.ready = true;

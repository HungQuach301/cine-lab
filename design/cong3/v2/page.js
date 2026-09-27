// Cổng 3 v2 — trang render chung (driver: shared/render_still.js hoặc shared/render_seq.js).
// --args: {"char": "base" | "3d" | "2d"}  (module dựng nhân vật: shared/cast.js | v2/char3d/cast3d.js | v2/char2d/cast2d.js)
//         {"nopaint": 1} bỏ lớp vẽ (để đo nhấp nháy của lớp vẽ); {"shot": "..."} dựng sẵn một shot trong setup.
// Khung: a_close_ida | b_cas_bird | c_s5_wide | walk@<số khung>
// Module nhân vật PHẢI xuất: buildCharacter(sheet, opts) (cùng API shared/cast.js) và có thể xuất update(ch, camera) (gọi trước mỗi mẫu).
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '../shared/post.js';
import { createPaint } from '../dir-C/paint.js';
import { createDOF } from '../shared/dof.js';
import { buildS5 } from './s5.js';
import { buildS6 } from './s6.js';
import { buildS1 } from './s1.js';
import { buildCloseIda, buildCasBird, buildWalk, buildPropGasLamp, buildTurn } from './shots.js';

const CHAR = { base: '../shared/cast.js', '3d': './char3d/cast3d.js', '2d': './char2d/cast2d.js' };
// Grade hướng C (chép từ dir-C/scene.js để dùng chung, không đổi).
const GRADE = `
uniform float gCanvas, gVig, gLift, gSat; uniform vec3 gShadowTint, gHiTint;
float ch21(vec2 p){ p = fract(p*vec2(233.34, 851.73)); p += dot(p, p+23.45); return fract(p.x*p.y); }
float cvn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
  return mix(mix(ch21(i), ch21(i+vec2(1,0)), f.x), mix(ch21(i+vec2(0,1)), ch21(i+vec2(1,1)), f.x), f.y); }
vec3 grade(vec3 c, vec2 uv){
  float L = dot(c, vec3(0.2126,0.7152,0.0722));
  c = mix(vec3(L), c, gSat);
  float sh = 1.0 - smoothstep(0.0, 0.45, L), hi = smoothstep(0.55, 1.0, L);
  c += gShadowTint * sh * gLift;
  c = mix(c, c * gHiTint, hi * 0.5);
  vec2 p = uv * res;
  float weave = sin(p.x * 2.09) * sin(p.y * 2.09 + 1.3 * sin(p.x * 0.05));
  float tooth = cvn(p / 7.0) - 0.5;
  float midw = 4.0 * L * (1.0 - L);
  c *= 1.0 + gCanvas * (0.55 * weave + 0.9 * tooth) * (0.35 + 0.65 * midw);
  vec2 q = (uv - 0.5) * vec2(1.0, 0.82);
  c *= mix(1.0, 1.0 - gVig, smoothstep(0.28, 0.75, length(q)));
  return c;
}`;
const GRADES = {
  turn: { gCanvas: 0, gVig: 0, gLift: 0, gSat: 1, gShadowTint: [1, 1, 1], gHiTint: [1, 1, 1] },
  prop_gaslamp: { gCanvas: 0.006, gVig: 0.12, gLift: 0.0, gSat: 1.0, gShadowTint: [1, 1, 1], gHiTint: [1, 1, 1] },
  face_ida: { gCanvas: 0.012, gVig: 0.28, gLift: 0.02, gSat: 1.0, gShadowTint: [0.40, 0.32, 0.90], gHiTint: [1.0, 0.975, 0.93] },
  a_close_ida: { gCanvas: 0.012, gVig: 0.28, gLift: 0.02, gSat: 1.0, gShadowTint: [0.40, 0.32, 0.90], gHiTint: [1.0, 0.975, 0.93] },
  b_cas_bird: { gCanvas: 0.012, gVig: 0.30, gLift: 0.02, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [1.0, 0.98, 0.94] },
  s1_opening: { gCanvas: 0.012, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.975, 0.93] },
  walk_cas: { gCanvas: 0.012, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.975, 0.93] },
  d_s6_alley: { gCanvas: 0.012, gVig: 0.30, gLift: 0.02, gSat: 1.0, gShadowTint: [0.32, 0.30, 0.90], gHiTint: [1.0, 0.975, 0.93] },
  e_ending: { gCanvas: 0.012, gVig: 0.24, gLift: 0.02, gSat: 0.95, gShadowTint: [0.30, 0.32, 0.90], gHiTint: [0.98, 0.995, 1.03] },
  c_s5_medium: { gCanvas: 0.012, gVig: 0.26, gLift: 0.018, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [0.985, 0.995, 1.02] },
  c_s5_wide: { gCanvas: 0.012, gVig: 0.30, gLift: 0.018, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [0.985, 0.995, 1.02] },
  walk: { gCanvas: 0.012, gVig: 0.26, gLift: 0.02, gSat: 1.0, gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.975, 0.93] },
};
// Phơi sáng theo shot (máy quay), cùng một thế giới đèn: cận mặt sát ngọn lửa phải đóng khẩu; cảnh đêm xa đèn phải mở khẩu.
const EXPOSE = { turn: 1.0, prop_gaslamp: 0.9, s1_opening: 1.0, face_ida: 0.12, a_close_ida: 0.30, b_cas_bird: 2.6, c_s5_wide: 1.0, c_s5_medium: 1.0, d_s6_alley: 4.0, e_ending: 1.0, walk: 1.05, walk_cas: 1.05 };
const S6_PAINT = { rNear: 3.0, rFar: 6.0, dNear: 1.5, dFar: 14, impScale: 0.4, stroke: 0.04, halation: 0.12, bloomWide: 0.06, wob: 1.2 };   // V1/V3: wob nhỏ → cột, mép thẳng
const END_PAINT = { rNear: 3.0, rFar: 6.0, dNear: 4, dFar: 40, impScale: 0.5, stroke: 0.04, halation: 0.10, bloomWide: 0.05, wob: 1.2 };
const S5_PAINT_MED = { rNear: 3.0, rFar: 6.0, dNear: 1.2, dFar: 8, impScale: 0.4, stroke: 0.04, preAmp: 0.14, wob: 3.0 };   // trung cảnh: máy gần → nét nhỏ hơn
const S5_PAINT = { rNear: 7.0, rFar: 9.0, dNear: 6, dFar: 12, impScale: 0.5, stroke: 0.045, preAmp: 0.16, wob: 3.5, preLen: 46, preWid: 6 };

let W, H, cfg, renderer, pipe, sheets, mod; const built = {};
async function buildRaw(shot) {
  const mkChar = (sheet, opts) => mod.buildCharacter(sheet, opts), upd = mod.update || null;
  if (shot === 'a_close_ida') return buildCloseIda(sheets[0], mkChar, upd, 0, cfg.dbg || {});
  if (shot === 'turn') return buildTurn(sheets[(cfg.dbg && cfg.dbg.who === 'cas') ? 1 : 0], mkChar, upd, cfg.dbg || {});
  if (shot === 'prop_gaslamp') return buildPropGasLamp(cfg.dbg || {});
  if (shot === 'face_ida') return buildCloseIda(sheets[0], mkChar, upd, 0, { ...(cfg.dbg || {}), face: true });
  if (shot === 'b_cas_bird') return buildCasBird(sheets[1], mkChar, upd, 0, cfg.dbg || {});
  if (shot === 'walk') return buildWalk(sheets[0], mkChar, upd);
  if (shot === 'walk_cas') return buildWalk(sheets[1], mkChar, upd, 'cas');
  if (shot === 's1_opening') { const r = await buildS1(sheets[0], H, cfg.dbg || {}, mkChar); return { ...r, chars: [r.chIda], paintP: { rNear: 3.0, rFar: 6.5, dNear: 30, dFar: 400, impScale: 0.4, stroke: 0.035, halation: 0.16, bloomWide: 0.07 } }; }
  if (shot === 'd_s6_alley' || shot === 'e_ending') { const r = await buildS6(sheets[0], sheets[1], cfg.dbg || {}, mkChar, upd, shot === 'd_s6_alley' ? 'alley' : 'ending'); return { ...r, paintP: shot === 'd_s6_alley' ? S6_PAINT : END_PAINT }; }
  if (shot === 'c_s5_medium') { const r = await buildS5(sheets[0], sheets[1], { ...(cfg.dbg || {}), medium: (cfg.dbg && cfg.dbg.medium) || 1 }, mkChar, upd); return { ...r, chars: [r.chIda, r.chCas], paintP: S5_PAINT_MED }; }
  if (shot === 'c_s5_wide') { const r = await buildS5(sheets[0], sheets[1], cfg.dbg || {}, mkChar, upd); return { ...r, chars: [r.chIda, r.chCas], paintP: S5_PAINT }; }
  throw new Error('shot không có: ' + shot);
}
async function build(shot) { return buildRaw(shot); }
window.setup = async (c) => {
  cfg = c; W = c.W; H = c.H;
  mod = await import(CHAR[c.char || 'base']);
  sheets = await Promise.all(['model-sheet/ida.json', 'model-sheet/cas.json'].map((p) => fetch('/' + p).then((r) => r.json())));
  renderer = createRenderer(W, H);
  // 7A (v3): bóng PCF (thay PCFSoft) — đo cận mặt: tra bóng mỗi điểm ảnh là chi phí chính; độ mềm đến từ jitter nguồn qua các mẫu.
  renderer.shadowMap.type = THREE[(c.dbg && c.dbg.shadowType) || 'PCFShadowMap'];
  if (c.dbg && c.dbg.noShadow) renderer.shadowMap.enabled = false;
  const uniforms = { gCanvas: { value: 0 }, gVig: { value: 0 }, gLift: { value: 0 }, gSat: { value: 1 }, gShadowTint: { value: new THREE.Vector3() }, gHiTint: { value: new THREE.Vector3(1, 1, 1) } };
  pipe = createPipeline(renderer, W, H, { exposure: 1.0, gradeGLSL: GRADE, uniforms });
  if (c.shot) { const b = built[c.shot] = await build(c.shot); b.paint = createPaint(renderer, W, H, pipe, b.paintP); renderer.compile(b.scene, b.cam);
    pipe.accumulate(b.scene, b.cam, 1, b.onSample); if (!cfg.nopaint) b.paint.apply(b.scene, b.cam);
    if (b.dof && !cfg.nopaint) { b.dofFx = createDOF(renderer, W, H, pipe); b.dofFx.apply(b.paint.outRT.texture, b.paint.gRT.texture, b.dof); } pipe.finalize(0); } // khởi động (biên dịch shader, cấp RT) — chi phí một lần mỗi shot
};
window.renderFrame = async (name, samples) => {
  const [shot, fs] = name.split('@'); const f = fs ? +fs : 0;
  const cur = built[shot] || (built[shot] = await build(shot));
  if (!cur.paint) cur.paint = createPaint(renderer, W, H, pipe, cur.paintP);
  const g = GRADES[shot], u = pipe.outMat.uniforms;
  u.gCanvas.value = g.gCanvas; u.gVig.value = g.gVig; u.gLift.value = g.gLift; u.gSat.value = g.gSat; u.gShadowTint.value.set(...g.gShadowTint); u.gHiTint.value.set(...g.gHiTint);
  u.uExp.value = (cfg.expose && cfg.expose[shot]) || EXPOSE[shot];
  if (cur.setFrame) cur.setFrame(f);
  // cfg.mask: mặt nạ nhân vật để ĐO (tỷ lệ chiều cao người trong khung, vùng mặt): nhân vật trắng, còn lại đen, không lớp vẽ.
  if (cfg.mask) {
    const white = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }), black = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
    cur.scene.traverse((o) => { if (o.isSprite) o.visible = false; if (!o.isMesh) return; let imp = false; for (let p = o; p; p = p.parent) if (p.userData.imp && p.isObject3D && p.type !== 'Scene' && !p.userData.lightAnchor) imp = imp || (cur.chars || []).some((c) => c.root === p); o.material = imp ? white : black; });
    cur.scene.background = new THREE.Color(0); cur.scene.fog = null; u.uExp.value = 1.0;
    const ms = pipe.accumulate(cur.scene, cur.cam, 1, null); cur.paint.bypass(); return { accum_ms: ms };
  }
  // cfg.prof: đồng bộ GPU sau từng chặng để đo chi phí thật (tích luỹ / lớp vẽ / DOF), ghi vào timing.json.
  const _px = new Float32Array(4), sync = (rt) => { renderer.readRenderTargetPixels(rt, 0, 0, 1, 1, _px); return performance.now(); };
  const t0 = performance.now();
  // 7A: bản đồ bóng chỉ vẽ lại khi đèn đổi vị trí jitter (mỗi `se` mẫu một vị trí); giữa hai lần dùng lại bản đồ cũ.
  const se = (cfg.dbg && cfg.dbg.shadowEvery) || 1;
  const onS = (i, n, j) => { const k = Math.floor(i / se), nk = Math.ceil(n / se); renderer.shadowMap.autoUpdate = false; renderer.shadowMap.needsUpdate = i % se === 0; if (cur.onSample) cur.onSample(k, nk, j); };
  const ms = pipe.accumulate(cur.scene, cur.cam, samples, se > 1 ? onS : cur.onSample);
  renderer.shadowMap.autoUpdate = true;
  const t1 = cfg.prof ? sync(pipe.accRT) : 0;
  if (!cfg.nopaint) cur.paint.apply(cur.scene, cur.cam); else cur.paint.bypass();
  const t2 = cfg.prof ? sync(cur.paint.outRT) : 0;
  if (cur.dof && !cfg.nopaint) { if (!cur.dofFx) cur.dofFx = createDOF(renderer, W, H, pipe); cur.dofFx.apply(cur.paint.outRT.texture, cur.paint.gRT.texture, cur.dof); }   // v3: DOF hậu kỳ (L1, L2)
  if (cfg.prof) return { accum_ms: ms, prof_ms: { accum: t1 - t0, paint: t2 - t1, dof: cur.dofFx ? sync(cur.dofFx.outRT) - t2 : 0 } };
  return cur.dump ? { accum_ms: ms, prof_ms: cur.dump } : { accum_ms: ms };
};
window.finalize = (f) => pipe.finalize(f);

// ================= Xuất file đi kèm cho checks/run.py (v3, bước 9) =================
// Mặt nạ bộ phận C3 (RUN.md 3.6): render THẬT ở scale× độ phân giải khung, cùng máy quay, cùng tư thế của khung f (tâm màn trập),
// vật liệu ID phẳng; mọi vật khác (kể cả phần còn lại của nhân vật) tô đen nhưng vẫn ghi độ sâu → mặt nạ là phần NHÌN THẤY của bộ phận.
// Bộ phận chi: lấy một bên (mặc định 'L'), xác định bằng tâm hình học trong hệ toạ độ gốc nhân vật (x > 0 = trái).
const PART_MAP = { head: ['head'], torso: ['torso'], upper_arm: ['upper_arm'], forearm: ['forearm'], thigh: ['thigh', 'thigh_skin'], shin: ['shin', 'shin_trouser'] };
window.exportParts = async (name, scale, opts = {}) => {
  const [shot, fs] = name.split('@'); const f = fs ? +fs : 0; const cur = built[shot] || (built[shot] = await build(shot));
  if (cur.setFrame) cur.setFrame(f);
  const ch = cur.chars[opts.who ?? 0], side = opts.side || 'L', keys = Object.keys(PART_MAP);
  const partOf = {}; for (const [k, v] of Object.entries(PART_MAP)) for (const t of v) partOf[t] = k;
  const black = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
  const idMat = keys.map((k, i) => new THREE.MeshBasicMaterial({ color: new THREE.Color((i + 1) * 30 / 255, 0, 0), side: THREE.DoubleSide }));
  cur.scene.updateMatrixWorld(true);
  const saved = [], v = new THREE.Vector3(), box = new THREE.Box3(), picked = {};
  cur.scene.traverse((o) => {
    if (o.isSprite || o.isPoints || o.isLine) { saved.push([o, 'v', o.visible]); o.visible = false; return; }
    if (!o.isMesh) return;
    saved.push([o, 'm', o.material]);
    let mine = false; for (let p = o; p; p = p.parent) if (p === ch.root) { mine = true; break; }
    const k = mine ? partOf[o.userData.part] : undefined; let ok = !!k;
    if (ok && k !== 'head' && k !== 'torso') { o.geometry.computeBoundingBox(); box.copy(o.geometry.boundingBox).applyMatrix4(o.matrixWorld); box.getCenter(v); ch.root.worldToLocal(v); ok = (v.x > 0) === (side === 'L'); }
    o.material = ok ? idMat[keys.indexOf(k)] : black; if (ok) picked[k] = (picked[k] || 0) + 1;
  });
  const bg = cur.scene.background, fog = cur.scene.fog; cur.scene.background = new THREE.Color(0); cur.scene.fog = null;
  const w = W * scale, h = H * scale, rt = new THREE.WebGLRenderTarget(w, h, { depthBuffer: true });
  const sm = renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate = false;
  cur.cam.clearViewOffset && cur.cam.clearViewOffset();
  renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(cur.scene, cur.cam);
  const px = new Uint8Array(w * h * 4); renderer.readRenderTargetPixels(rt, 0, 0, w, h, px); renderer.setRenderTarget(null); rt.dispose();
  renderer.shadowMap.autoUpdate = sm; cur.scene.background = bg; cur.scene.fog = fog;
  for (const [o, k, val] of saved) { if (k === 'v') o.visible = val; else o.material = val; }
  const id = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) { const src = (h - 1 - y) * w * 4, dst = y * w; for (let x = 0; x < w; x++) id[dst + x] = Math.round(px[src + x * 4] / 30); }   // lật dọc (GL gốc dưới)
  const out = {}, count = {};
  const cv = new OffscreenCanvas(w, h), g = cv.getContext('2d'), img = g.createImageData(w, h), d32 = new Uint32Array(img.data.buffer);
  for (let i = 0; i < keys.length; i++) {
    let n = 0; for (let j = 0; j < id.length; j++) { const on = id[j] === i + 1; d32[j] = on ? 0xffffffff : 0x00000000; n += on; }   // ngoài bộ phận: đen, alpha 0 (máy đọc 'xám hoặc alpha' ≥ 128; lần nộp đầu để alpha 255 toàn ảnh → sai)
    g.putImageData(img, 0, 0); const ab = await (await cv.convertToBlob({ type: 'image/png' })).arrayBuffer();
    let bin = ''; const u8 = new Uint8Array(ab); for (let j = 0; j < u8.length; j += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(j, j + 0x8000));
    out[keys[i]] = btoa(bin); count[keys[i]] = n;
  }
  return { w, h, parts: out, count, picked, sheet: ch.sheet.id };
};

// Chuyển động bake (RUN.md 3.2, 3.4): góc khớp sau khi đặt tư thế (rad, Euler XYZ) mỗi khung; gốc nhân vật; track màn hình của các khớp
// có chi tiết (đầu, cổ tay, cổ chân) chiếu qua máy quay render, toạ độ điểm ảnh file video (gốc trên–trái).
window.exportMotion = async (shot, from, to, opts = {}) => {
  const cur = built[shot] || (built[shot] = await build(shot)); const ch = cur.chars[opts.who ?? 0];
  const nm = ch.sheet.id.startsWith('CHR-ida') ? 'ida' : 'cas';
  // Track đặt trên vùng có chi tiết (RUN.md 3.4): tâm đầu/mũ và tâm lòng bàn tay (da sáng trên áo tối). Lần 1 dùng cổ tay/cổ chân
  // (cổ tay áo tối, ủng tối sát nền = mảng phẳng, luồng quang học yếu) → H1b trượt; track toàn null (ra ngoài khung) bị bỏ.
  const J = Object.keys(ch.joints), ch_ = {}, root = [], tracks = { head: [], hand_L: [], hand_R: [] };
  for (const j of J) ch_[j] = [];
  const v = new THREE.Vector3(), rc = new THREE.Raycaster();
  const vis = []; cur.scene.traverse((o) => { if (o.isMesh && o.visible && o.material && !o.material.transparent && o.material.colorWrite !== false) vis.push(o); });
  for (let f = from; f < to; f++) {
    if (cur.setFrame) cur.setFrame(f);
    for (const o of vis) o.geometry.computeBoundingSphere();   // lưới da CPU đổi hình theo tư thế
    ch.root.updateMatrixWorld(true); cur.cam.updateMatrixWorld(true);
    for (const j of J) { const r = ch.joints[j].rotation; ch_[j].push([+r.x.toFixed(6), +r.y.toFixed(6), +r.z.toFixed(6)]); }
    root.push(ch.root.position.toArray().map((x) => +x.toFixed(5)));
    for (const t of Object.keys(tracks)) {
      if (t === 'head') { ch.joints.head.getWorldPosition(v); v.y += 0.45 * ch.H; }
      else { const h = ch.hands[t.slice(-1)].hand; v.set(0, -ch.sheet.parts.hand.palm_length * ch.H * 0.5, 0); h.localToWorld(v); }
      const p = v.clone().project(cur.cam), xs = (p.x + 1) / 2 * W, ys = (1 - p.y) / 2 * H;
      // Che khuất (RUN.md 3.4: null khi bị che): tia từ máy quay tới điểm; gặp mặt lưới khác gần hơn điểm quá 3 cm thì coi là bị che.
      const cp = cur.cam.getWorldPosition(new THREE.Vector3()), dir = v.clone().sub(cp), dist = dir.length();
      rc.set(cp, dir.normalize()); rc.far = dist;
      const own = t === 'head' ? ch.joints.head : ch.hands[t.slice(-1)].hand;   // bỏ lưới của chính bộ phận (điểm nằm trong khối của nó)
      const hit = rc.intersectObjects(vis, false).some((h) => { for (let q = h.object; q; q = q.parent) if (q === own) return false; return h.distance < dist - 0.03; });
      tracks[t].push(p.z < 1 && xs >= 0 && xs < W && ys >= 0 && ys < H && !hit ? [+xs.toFixed(2), +ys.toFixed(2)] : null);
    }
  }
  const channels = J.map((j) => ({ id: `${nm}/${j}.rot`, class: 'character_part', first_frame: from, values: ch_[j] }));
  channels.push({ id: `${nm}/root.loc`, class: 'character_root', first_frame: from, values: root });
  return { fps: 24, channels, screen_tracks: Object.entries(tracks).filter(([, vals]) => vals.some((x) => x)).map(([t, vals]) => ({ id: `${nm}/${t}`, first_frame: from, values: vals })) };
};

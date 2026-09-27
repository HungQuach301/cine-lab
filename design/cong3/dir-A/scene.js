// Cine Lab · Cổng 3 vòng 1 · HƯỚNG A — "Tin & Felt" (diorama thủ công thu nhỏ quay bằng ống kính thật).
// Khung: s1_opening (toàn cảnh cao, chạng vạng), s5_shadows (hốc cửa bốc hàng, hai bóng người).
// Khung phụ đo đạc: s5_measure (in tỷ lệ key : tràn tại vách trong ra console, không dùng làm hình).
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { buildCharacter, buildLantern } from '../shared/cast.js';
import { createPipeline, createRenderer } from '../shared/post.js';
import { procMat, feltCharacterMaterial, addSolder, mergeInto, metricUV, halton, mulberry, haloSprite, dofCamera, importAddon, LIBCFG, bakeStatic, haloPoints } from './lib.js';

let DBG = {}; let W, H, renderer, pipe, sheets, RoundedBoxGeometry, RectAreaLightUniformsLib;
const shots = {};

// Chỉnh màu hiển thị (sRGB): vignette ống kính tự nhiên + tách tông nhẹ (bóng hơi lạnh, sáng giữ ấm) + chân đen phim.
const GRADE = /* glsl */`
uniform float uVig; uniform float uCoolShadow;
vec3 grade(vec3 c, vec2 uv){
  vec2 d = (uv - 0.5) * vec2(1.7778, 1.0);
  float r2 = dot(d, d);
  c *= 1.0 - uVig * r2 * (0.85 + 0.15*r2);
  float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
  float sh = 1.0 - smoothstep(0.02, 0.32, l);
  c = mix(c, c * vec3(0.93, 0.99, 1.10), sh * uCoolShadow);
  c = c * 0.975 + vec3(0.010, 0.010, 0.014);
  return c;
}`;

// Tone map: ACES (như mặc định của post.js) nhưng giữ sắc độ ở vùng sáng — nguồn hổ phách không cháy thành trắng
// (hào quang và vũng sáng quanh đèn giữ màu ấm như phim thật bị quá sáng nhẹ). Trộn 55% bản giữ sắc độ.
const TONE = /* glsl */`
vec3 RRTAndODTFit(vec3 v){ vec3 a = v*(v+0.0245786)-0.000090537; vec3 b = v*(0.983729*v+0.4329510)+0.238081; return a/b; }
vec3 acesFit(vec3 c){
  const mat3 I = mat3(vec3(0.59719,0.07600,0.02840), vec3(0.35458,0.90834,0.13383), vec3(0.04823,0.01566,0.83777));
  const mat3 O = mat3(vec3(1.60475,-0.10208,-0.00327), vec3(-0.53108,1.10813,-0.07276), vec3(-0.07367,-0.00605,1.07602));
  return clamp(O*RRTAndODTFit(I*c), 0.0, 1.0); }
vec3 tonemap(vec3 c){
  c *= EXPOSURE/0.6;
  vec3 a = acesFit(c);
  float L = max(dot(c, vec3(0.2126,0.7152,0.0722)), 1e-6);
  float Lt = acesFit(vec3(L)).g;
  vec3 h = c * (Lt / L);
  float mx = max(h.r, max(h.g, h.b));
  if (mx > 1.0) { h /= mx; h = mix(h, vec3(1.0), clamp((mx - 1.0) * 0.25, 0.0, 0.45)); }
  return clamp(mix(a, h, 0.7), 0.0, 1.0);
}`;

window.setup = async (cfg) => {
  W = cfg.W; H = cfg.H; DBG = cfg.dbg || {}; LIBCFG.plain = !!DBG.plain;
  ({ RoundedBoxGeometry } = await importAddon('geometries/RoundedBoxGeometry.js'));
  ({ RectAreaLightUniformsLib } = await importAddon('lights/RectAreaLightUniformsLib.js'));
  RectAreaLightUniformsLib.init();
  const [ida, cas] = await Promise.all(['model-sheet/ida.json', 'model-sheet/cas.json'].map((p) => fetch('/' + p).then((r) => r.json())));
  sheets = { ida, cas };
  renderer = createRenderer(W, H);
  const only = cfg.only; // tuỳ chọn: chỉ dựng một cảnh khi thử nhanh
  if (!only || only === 's5') shots.s5 = buildS5();
  if (!only || only === 's1') shots.s1 = buildS1();
  const warm = new THREE.WebGLRenderTarget(64, 36, { type: THREE.FloatType });
  // Biên dịch shader + đổ bóng một lần trước (thời gian dựng cảnh không tính vào thời gian render khung).
  for (const s of Object.values(shots)) { renderer.compile(s.scene, s.cam); renderer.setRenderTarget(warm); renderer.info.autoReset = true; renderer.render(s.scene, s.cam); console.log('INFO', JSON.stringify(renderer.info.render), renderer.info.programs.length); }
  renderer.setRenderTarget(null);
};

window.renderFrame = async (name, samples) => {
  if (name === 's5_measure') return measureS5(samples);
  const key = name.startsWith('s1') ? 's1' : 's5';
  const s = shots[key];
  pipe = createPipeline(renderer, W, H, { exposure: s.exposure, toneGLSL: TONE, gradeGLSL: GRADE, uniformDecl: '', uniforms: { uVig: { value: 0.32 }, uCoolShadow: { value: 0.5 } } });
  pipe.outMat.uniforms.uVig.value = s.vig; pipe.outMat.uniforms.uCoolShadow.value = s.cool;
  const ms = pipe.accumulate(s.scene, s.cam, samples, s.onSample);
  s.dof.reset();
  return { accum_ms: ms };
};
window.finalize = (f) => pipe.finalize(f);

// ======================================================================================================
// Tiện ích dựng
const RB = (w, h, d, r = 0.05, seg = 2) => new RoundedBoxGeometry(w, h, d, seg, Math.min(r, Math.min(w, h, d) / 2 - 1e-4));
const mat4 = (x = 0, y = 0, z = 0, ry = 0, rx = 0, rz = 0, s = 1) => new THREE.Matrix4().compose(new THREE.Vector3(x, y, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(rx, ry, rz, 'YXZ')), new THREE.Vector3(s, s, s));
function characters(env, glassGlow = 0.5) {
  const mf = feltCharacterMaterial({ envMap: env, env: 0.5, glassGlow });
  const ida = buildCharacter(sheets.ida, { material: mf, detail: 32 });
  const cas = buildCharacter(sheets.cas, { material: mf, detail: 32 });
  // Chi tiết trang trí gắn khớp đầu (không đổi đường bao): lớp tóc sau gáy bằng len thô — nhìn từ sau không lộ "đầu trọc".
  for (const [ch, col, t0, t1, k] of [[ida, sheets.ida.local_colors.hair, 0.0, 0.80, 1.035], [cas, '#5a4034', 0.30, 0.80, 1.03]]) {
    const hd = ch.sheet.parts.head, Hm = ch.H;
    const g = new THREE.SphereGeometry(0.5, 40, 20, Math.PI * 1.08, Math.PI * 0.84, Math.PI * t0, Math.PI * (t1 - t0));
    const m = new THREE.Mesh(g, mf('hair', col, 'hair_back'));
    m.scale.set(hd.width_front * Hm * k, hd.length * Hm * k, hd.width_side * Hm * k); m.position.y = hd.length * Hm / 2; m.castShadow = true;
    ch.joints.head.add(m);
  }
  return { ida, cas, mf };
}

// ======================================================================================================
// S5 — HỐC CỬA BỐC HÀNG. Toạ độ: mặt tường nhà kho z = 0, hốc lùi vào −z tới vách trong z = −4.
// Miệng vòm rộng 3,2 m, chân vòm 2,4 m, đỉnh 4,0 m. Đèn lồng z = −1 (cách vách 3 m), Ida/Cas z = −3 (cách vách 1 m).
function buildS5() {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  const BW = 3.2, R = 1.6, SPR = 2.4, DEP = 4.0, FT = 0.55; // bề dày tường mặt tiền
  const floorY = 0.075;

  // --- env nhỏ cho vật kim loại/dạ: phòng tối ấm + ô sáng lạnh phía sau máy quay (phố trắng) ---
  const pm = new THREE.PMREMGenerator(renderer);
  const es = new THREE.Scene();
  es.add(new THREE.Mesh(new THREE.BoxGeometry(20, 20, 20), new THREE.MeshBasicMaterial({ color: new THREE.Color(0.018, 0.013, 0.009), side: THREE.BackSide })));
  const bright = new THREE.Mesh(new THREE.PlaneGeometry(12, 7), new THREE.MeshBasicMaterial({ color: new THREE.Color(0.55, 0.62, 0.72) }));
  bright.position.set(0, 1, 9.5); bright.rotation.y = Math.PI; es.add(bright);
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(2, 1), new THREE.MeshBasicMaterial({ color: new THREE.Color(0.9, 0.5, 0.2) }));
  glow.position.set(0, -2, 0); glow.rotation.x = -Math.PI / 2; es.add(glow);
  const env = pm.fromScene(es, 0.02, 0.1, 50).texture;

  // --- vật liệu ---
  const limeIn = procMat('lime', { color: '#ece6d9', rough: 0.93, env: 0, side: THREE.DoubleSide, ground: floorY });
  const facadeM = procMat('brickwash', { color: '#e8e3d8', rough: 0.9, env: 0, ground: floorY, worn: 0.26 });
  const dressed = procMat('stone', { color: '#ffffff', vc: true, rough: 0.85, env: 0, sc: 6 });
  const settM = procMat('stone', { color: '#ffffff', rough: 0.78, env: 0, sc: 14 });
  const beddingM = procMat('stone', { color: '#1b1a18', rough: 1, env: 0, sc: 20 });
  const ironM = procMat('iron', { color: '#24262a', rough: 0.5, metal: 0.3, envMap: env, env: 0.6 });

  // --- mặt tiền có lỗ vòm, vát mép bo (bìa/thạch cao) ---
  const sh = new THREE.Shape(); sh.moveTo(-9, -0.4); sh.lineTo(9, -0.4); sh.lineTo(9, 9); sh.lineTo(-9, 9); sh.lineTo(-9, -0.4);
  const hole = new THREE.Path(); hole.moveTo(-R, -0.2); hole.lineTo(R, -0.2); hole.lineTo(R, SPR); hole.absarc(0, SPR, R, 0, Math.PI, false); hole.lineTo(-R, -0.2);
  sh.holes.push(hole);
  const facG = new THREE.ExtrudeGeometry(sh, { depth: FT - 0.06, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 3, curveSegments: 48 });
  facG.translate(0, 0, -FT + 0.03);
  const fac = new THREE.Mesh(facG, facadeM); fac.castShadow = fac.receiveShadow = true; scene.add(fac);

  // --- vỏ trong của hốc: 2 vách bên, vòm bán trụ, vách trong ---
  const shell = [];
  const quadStrip = (pts, nrm) => { // pts: mảng [a,b,c,d] → 2 tam giác; tự đảo chiều quấn cho khớp pháp tuyến
    const g = new THREE.BufferGeometry(); let [a, b, c, d] = pts;
    { const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b), C = new THREE.Vector3(...c);
      const gn = B.clone().sub(A).cross(C.clone().sub(A)); if (gn.dot(new THREE.Vector3(...nrm)) < 0) { [b, d] = [d, b]; } }
    g.setAttribute('position', new THREE.Float32BufferAttribute([...a, ...b, ...c, ...a, ...c, ...d].map(Number), 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(new Array(6).fill(nrm).flat(), 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(new Array(12).fill(0), 2)); return g; };
  const z0 = -FT + 0.02, z1 = -DEP;
  for (const s of [-1, 1]) shell.push(quadStrip([[s * R, -0.1, z0], [s * R, -0.1, z1], [s * R, SPR, z1], [s * R, SPR, z0]], [-s, 0, 0]));
  const K = 40;
  for (let k = 0; k < K; k++) {
    const a0 = Math.PI * k / K, a1 = Math.PI * (k + 1) / K;
    const p = (a, z) => [R * Math.cos(a), SPR + R * Math.sin(a), z];
    const am0 = (a0 + a1) / 2; const g = quadStrip([p(a0, z0), p(a1, z0), p(a1, z1), p(a0, z1)], [-Math.cos(am0), -Math.sin(am0), 0]);
    // pháp tuyến mượt theo góc của từng đỉnh (hướng vào trong)
    const nn = g.attributes.normal, pp = g.attributes.position;
    for (let i = 0; i < 6; i++) { const a = Math.atan2(pp.getY(i) - SPR, pp.getX(i)); nn.setXYZ(i, -Math.cos(a), -Math.sin(a), 0); }
    shell.push(g);
  }
  const shellM = new THREE.Mesh(mergeInto(shell.map((g) => ({ g }))), limeIn); shellM.castShadow = shellM.receiveShadow = true; scene.add(shellM);
  const back = new THREE.Shape(); back.moveTo(-R - 0.05, -0.1); back.lineTo(R + 0.05, -0.1); back.lineTo(R + 0.05, SPR); back.absarc(0, SPR, R + 0.05, 0, Math.PI, false); back.lineTo(-R - 0.05, -0.1);
  const backG = new THREE.ShapeGeometry(back, 64); backG.translate(0, 0, z1);
  const backM = new THREE.Mesh(backG, limeIn); backM.receiveShadow = true; backM.castShadow = true; scene.add(backM);
  // Khối nhà kho phía trên/hai bên (chỉ để chặn ánh điện, không thấy trong hình)
  const mass = new THREE.Mesh(new THREE.BoxGeometry(18, 6, 12), new THREE.MeshStandardMaterial({ color: 0x777777 }));
  mass.position.set(0, 4.1 + 3 + 0.05, -FT - 6.05); mass.castShadow = true; mass.visible = true; scene.add(mass);
  for (const s of [-1, 1]) { const side = new THREE.Mesh(new THREE.BoxGeometry(7, 4.2, 12), mass.material); side.position.set(s * (R + 3.55), 2.1, -FT - 6.05); side.castShadow = true; scene.add(side); }

  // --- vòm đá gọt (voussoir) viền miệng vòm + đá góc hai bên, nhô 6 cm, bo cạnh ---
  const vous = [];
  const NV = 13;
  for (let i = 0; i < NV; i++) {
    const a = Math.PI * (i + 0.5) / NV, big = i === (NV - 1) / 2 ? 1.25 : 1.0;
    const rr = R + 0.26 * big;
    vous.push({ g: RB(0.40 * (i === (NV - 1) / 2 ? 1.15 : 1), 0.52 * big, 0.16, 0.035), m: mat4(rr * Math.cos(a), SPR + rr * Math.sin(a), 0.05, 0, 0, a - Math.PI / 2) });
  }
  const qr = mulberry(77);
  for (const s of [-1, 1]) for (let j = 0; j < 6; j++) {
    const wide = (j % 2 ? 0.60 : 0.40) + (qr() - 0.5) * 0.08, hh = 0.4;
    vous.push({ g: RB(wide, hh - 0.03, 0.12 + qr() * 0.04, 0.03 + qr() * 0.02), m: mat4(s * (R + wide / 2 - 0.02), 0.2 + hh * j + hh / 2 - 0.1 + 0.08, 0.045, (qr() - 0.5) * 0.03, 0, (qr() - 0.5) * 0.02),
      color: '#' + new THREE.Color().setHSL(0.1 + qr() * 0.03, 0.12 + qr() * 0.1, 0.72 + qr() * 0.1).getHexString() });
  }
  // plinth đá dưới chân mặt tiền
  for (const s of [-1, 1]) vous.push({ g: RB(7, 0.42, 0.16, 0.04), m: mat4(s * (R + 3.5), 0.18, 0.05) });
  vous.forEach((v) => { if (!v.color) v.color = '#e6dccb'; });
  const vm = new THREE.Mesh(mergeInto(vous, { color: true }), dressed); vm.castShadow = vm.receiveShadow = true; scene.add(vm);

  // --- ống máng thoát nước bên trái, vòng sắt buộc ngựa bên phải (chi tiết mép khung, ngoài phố) ---
  const pipeG = new THREE.CylinderGeometry(0.055, 0.055, 9, 12);
  const pipes = [{ g: pipeG, m: mat4(-2.85, 4.5, 0.12) }];
  for (let j = 0; j < 5; j++) pipes.push({ g: new THREE.CylinderGeometry(0.075, 0.075, 0.06, 12), m: mat4(-2.85, 0.6 + j * 1.8, 0.12) });
  pipes.push({ g: new THREE.TorusGeometry(0.09, 0.016, 8, 20), m: mat4(2.35, 1.05, 0.08, 0, 0, 0) });
  pipes.push({ g: new THREE.CylinderGeometry(0.03, 0.03, 0.08, 10), m: mat4(2.35, 1.14, 0.05, 0, Math.PI / 2, 0) });
  const pm2 = new THREE.Mesh(mergeInto(pipes), ironM); pm2.castShadow = pm2.receiveShadow = true; scene.add(pm2);

  // --- đá lát từng viên (instanced), mạch vữa tối bên dưới ---
  const bed = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), beddingM); bed.rotation.x = -Math.PI / 2; bed.position.set(0, 0.0, 0); bed.receiveShadow = true; scene.add(bed);
  const rnd = mulberry(1234);
  const stoneG = RB(1, 1, 1, 0.14, 1);
  const cells = [];
  const SL = 0.135;
  for (let z = 6.0; z > -DEP - 0.2; z -= SL + (rnd() - 0.5) * 0.01) {
    const inside = z < -0.1;
    for (let x = -6 - rnd() * 0.2; x < 6;) {
      const w = 0.15 + rnd() * 0.11;
      if (!(inside && Math.abs(x + w / 2) > R + 0.1)) cells.push([x + w / 2 + (rnd() - 0.5) * 0.008, z + (rnd() - 0.5) * 0.008, w]);
      x += w;
    }
  }
  const inst = new THREE.InstancedMesh(stoneG, settM, cells.length);
  const col = new THREE.Color(), q = new THREE.Quaternion(), e = new THREE.Euler();
  cells.forEach(([x, z, cw], i) => {
    const w = cw - 0.012 - rnd() * 0.01, l = SL - 0.012 - rnd() * 0.01, h = 0.07 + rnd() * 0.01;
    e.set((rnd() - 0.5) * 0.04, (rnd() - 0.5) * 0.06, (rnd() - 0.5) * 0.04); q.setFromEuler(e);
    const m = new THREE.Matrix4().compose(new THREE.Vector3(x, floorY - h / 2 + (rnd() - 0.5) * 0.007, z), q, new THREE.Vector3(w, h, l));
    inst.setMatrixAt(i, m);
    const t = rnd(); col.setRGB(0.30 + 0.10 * t, 0.29 + 0.08 * t + 0.02 * rnd(), 0.28 + 0.06 * t + 0.05 * rnd()).multiplyScalar(0.75 + 0.45 * rnd());
    inst.setColorAt(i, col);
  });
  inst.castShadow = false; inst.receiveShadow = true; scene.add(inst);

  // --- nhân vật: quay lưng về máy quay (nhìn −z), cách vách 1 m ---
  const { ida, cas, mf } = characters(env, 1.6);
  ida.setPose(sheets.ida.poses.look_shadows); cas.setPose(sheets.cas.poses.half_raised);
  ida.root.rotation.y = Math.PI; cas.root.rotation.y = Math.PI;
  ida.root.position.set(-0.43, floorY + ida.root.position.y, -3.0); cas.root.position.set(0.44, floorY + cas.root.position.y, -3.0);
  cas.root.rotation.y = Math.PI + 0.08; ida.root.rotation.y = Math.PI - 0.05;
  scene.add(ida.root, cas.root);
  bakeStatic(ida.root, scene); bakeStatic(cas.root, scene);

  // --- đèn lồng trên nền đá, cách vách 3 m ---
  const LH = sheets.ida.props.lantern.height_H * sheets.ida.H_m;
  const lan = buildLantern(LH, mf); addSolder(lan, mf('tin', '#8e8a80', 'lantern'), LH);
  { // khung thiếc gấp mép quanh kính (4 cạnh đứng + đai trên/dưới) và bản lề cửa — chi tiết trang trí, không đổ bóng
    const tinM = mf('tin', '#8e8a80', 'lantern'), w = LH * 0.58 * 0.96, t = LH * 0.035;
    for (const [x, z] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) { const b = new THREE.Mesh(new THREE.BoxGeometry(t, LH * 0.6, t), tinM); b.position.set(x * w / 2, LH * 0.40, z * w / 2); lan.add(b); }
    for (const y of [0.105, 0.695]) { const band = new THREE.Mesh(new THREE.BoxGeometry(w + t, LH * 0.03, w + t), tinM); band.position.y = LH * y; lan.add(band); }
    const hinge = new THREE.Mesh(new THREE.CylinderGeometry(t * 0.45, t * 0.45, LH * 0.5, 8), tinM); hinge.position.set(w / 2 + t * 0.4, LH * 0.40, w / 2 + t * 0.4); lan.add(hinge);
  }
  lan.position.set(0.02, floorY, -1.0); lan.rotation.y = 0.35; scene.add(lan);
  lan.traverse((o) => { if (o.isMesh) { const gp = o.geometry.parameters || {}; o.castShadow = !!(gp.radialSegments === 4 && gp.radiusTop != null); /* chỉ đế đèn đổ bóng; nắp đục lỗ thông hơi, coi như không chặn */ /* chỉ đế đèn đổ bóng (nắp có lỗ thông hơi) */ o.receiveShadow = true; } });
  lan.updateMatrixWorld(true);
  const anchor = new THREE.Vector3(); lan.userData.lightAnchor.getWorldPosition(anchor);
  const halo = haloSprite(new THREE.Color(1.0, 0.60, 0.28), 1.3, 0.7); halo.position.copy(anchor); scene.add(halo);

  // --- ánh sáng ---
  // Đèn lồng: nguồn điểm ấm ~2000 K (hổ phách), có bóng; jitter vị trí trong khoảng kính (~12 cm) theo mẫu → bóng mềm.
  const LCOL = new THREE.Color(1.0, 0.54, 0.22);
  const key = new THREE.PointLight(LCOL, 11.0, 0, 2);
  key.position.copy(anchor); key.castShadow = true; key.shadow.mapSize.set(1024, 1024); key.shadow.camera.near = 0.04; key.shadow.camera.far = 12; key.shadow.bias = -0.004; key.shadow.normalBias = 0.01;
  scene.add(key);
  if (DBG.noKeyShadow) key.castShadow = false;
  // Ánh điện ngoài phố: nguồn rộng, cao, nhiều cột → mô phỏng bằng đèn hướng jitter trong nón rộng theo mẫu (trắng lạnh ~6000 K):
  // phẳng, gần như không bóng đổ; khối nhà kho che nên không lọt sâu vào hốc.
  const ECOL = new THREE.Color(0.70, 0.85, 1.0);
  const street = new THREE.DirectionalLight(ECOL, 9.0);
  street.castShadow = true; street.shadow.mapSize.set(2048, 2048);
  Object.assign(street.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 80 }); street.shadow.bias = -0.0006; street.shadow.normalBias = 0.03;
  street.target.position.set(0, 0, 1.5); scene.add(street, street.target);
  // Ánh dội lạnh từ mặt phố trắng lọt qua miệng vòm (nguồn diện rộng, không bóng) — "tràn" rất yếu trong hốc.
  const fill = new THREE.RectAreaLight(ECOL, 0.30, BW - 0.2, 1.4);
  fill.position.set(0, 0.8, -0.3); fill.lookAt(0, 0.9, -4); scene.add(fill);
  const amb = new THREE.HemisphereLight(new THREE.Color(0.7, 0.8, 1.0), new THREE.Color(0.25, 0.22, 0.2), 0.02); scene.add(amb);

  // --- máy quay: ngang tầm người lớn 1,32 m, ngoài miệng vòm; nét ở nhân vật/vách, nhoè nhẹ đèn lồng tiền cảnh ---
  const cam = new THREE.PerspectiveCamera(37, W / H, 0.05, 200);
  const cpos = new THREE.Vector3(0.12, 1.32, 3.3), ctgt = new THREE.Vector3(0.0, 1.42, -4);
  const focusD = cpos.distanceTo(new THREE.Vector3(0, 1.3, -3.25));
  const dof = dofCamera(cam, cpos, ctgt, focusD, 0.030); dof.reset();

  const base = anchor.clone();
  const onSample = (i, n) => {
    dof.jitter(i, n);
    key.position.set(base.x + (halton(i, 2) - 0.5) * 0.12, base.y + (halton(i, 3) - 0.5) * 0.08, base.z + (halton(i, 5) - 0.5) * 0.12);
    // nón ánh điện: ±38° dọc phố (x), 0–10° nghiêng vào tường
    const ax = (halton(i, 7) - 0.5) * 2 * 0.70, az = 0.06 + halton(i, 11) * 0.38;
    const d = new THREE.Vector3(Math.sin(ax), -Math.cos(ax) * Math.cos(az), -Math.sin(az)).normalize();
    street.position.copy(street.target.position).addScaledVector(d, -40);
  };
  if (DBG.noFill) fill.visible = false; if (DBG.noSetts) inst.visible = false; if (DBG.noStreetShadow) street.castShadow = false; if (DBG.noChars) { ida.root.visible = false; cas.root.visible = false; }
  if (DBG.keyOnly) { street.visible = false; fill.visible = false; amb.visible = false; }
  return { scene, cam, dof, onSample, exposure: 1.0, vig: 0.30, cool: 0.55, lights: { key, street, fill, amb }, halo, wallZ: z1 };
}

// Đo tỷ lệ key : tràn tại vách trong (không gian tuyến tính, trước tone map). Hai lần tích luỹ: chỉ đèn lồng / chỉ tràn.
function measureS5(samples) {
  const s = shots.s5; const L = s.lights;
  pipe = createPipeline(renderer, W, H, { exposure: s.exposure, toneGLSL: TONE, gradeGLSL: GRADE, uniforms: { uVig: { value: 0.3 }, uCoolShadow: { value: 0.5 } } });
  const pts = [[-1.25, 0.9], [1.25, 0.9], [-1.3, 2.0], [1.3, 2.0], [0, 3.4], [-0.6, 3.1], [0.7, 3.1]].map(([x, y]) => new THREE.Vector3(x, y, s.wallZ + 0.01));
  const read = () => {
    const out = []; const buf = new Float32Array(4 * 9);
    for (const p of pts) { const v = p.clone().project(s.cam); const px = Math.round((v.x * 0.5 + 0.5) * W), py = Math.round((v.y * 0.5 + 0.5) * H);
      renderer.readRenderTargetPixels(pipe.accRT, px - 1, py - 1, 3, 3, buf); let lum = 0; for (let k = 0; k < 9; k++) lum += 0.2126 * buf[k * 4] + 0.7152 * buf[k * 4 + 1] + 0.0722 * buf[k * 4 + 2]; out.push(lum / 9); }
    return out; };
  const vis = (k, f) => { L.key.visible = k; s.halo.visible = k; L.street.visible = f; L.fill.visible = f; L.amb.visible = f; };
  vis(true, false); pipe.accumulate(s.scene, s.cam, samples, s.onSample); const kv = read();
  vis(false, true); pipe.accumulate(s.scene, s.cam, samples, s.onSample); const fv = read();
  vis(true, true); pipe.accumulate(s.scene, s.cam, samples, s.onSample); s.dof.reset();
  const ratios = kv.map((k, i) => +(k / Math.max(1e-6, fv[i])).toFixed(2));
  console.log('S5_MEASURE ' + JSON.stringify({ points: pts.map((p) => [p.x, p.y]), key: kv.map((v) => +v.toFixed(5)), fill: fv.map((v) => +v.toFixed(5)), ratio: ratios }));
  return { accum_ms: 0, ratios };
}

// Kiểm điểm nào thấy được từ máy quay: render độ sâu tuyến tính (1/4 độ phân giải), so với độ sâu điểm.
function visibleFrom(scene, cam, pts, tol) {
  const w = Math.round(W / 2), h = Math.round(H / 2);
  const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.FloatType });
  const dm = new THREE.ShaderMaterial({ vertexShader: 'varying float vD; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vD = -mv.z; gl_Position = projectionMatrix * mv; }',
    fragmentShader: 'varying float vD; void main(){ gl_FragColor = vec4(vD, 0.0, 0.0, 1.0); }', side: THREE.DoubleSide });
  const bg = scene.background, fog = scene.fog; scene.overrideMaterial = dm; scene.background = null; scene.fog = null;
  renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, cam);
  const buf = new Float32Array(w * h * 4); renderer.readRenderTargetPixels(rt, 0, 0, w, h, buf);
  scene.overrideMaterial = null; scene.background = bg; scene.fog = fog; renderer.setRenderTarget(null); rt.dispose();
  const m = new THREE.Matrix4().copy(cam.matrixWorldInverse);
  return pts.map((p) => { const v = p.clone().project(cam); if (Math.abs(v.x) > 1 || Math.abs(v.y) > 1 || v.z > 1) return false;
    const px = Math.min(w - 1, Math.floor((v.x * 0.5 + 0.5) * w)), py = Math.min(h - 1, Math.floor((v.y * 0.5 + 0.5) * h));
    const d = -p.clone().applyMatrix4(m).z; let best = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { const x = Math.max(0, Math.min(w - 1, px + dx)), y = Math.max(0, Math.min(h - 1, py + dy)); const z = buf[(y * w + x) * 4]; if (z <= 0 || z > d - tol) best++; }
    if (DBG.vis && d < 160) console.log('VIS', d.toFixed(1), buf[(py * w + px) * 4].toFixed(1), px, py);
    return best >= 2; });
}

// ======================================================================================================
// S1 — TOÀN CẢNH CAO. Phố Ostler cong, dốc nhẹ xuống xa máy quay; quảng trường + đồng hồ gần máy quay (dưới khung).
function buildS1() {
  const scene = new THREE.Scene();
  const R = mulberry(20260927);
  const SUN = new THREE.Vector3(-0.42, 0.0, -1).normalize(); const ENVK = 5.0;
  // --- trời chạng vạng: hồng (chân trời phía mặt trời lặn) → tím → xanh thẫm ở thiên đỉnh, dải mây mỏng ---
  const skyMat = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { sun: { value: SUN }, k: { value: 0.72 } },
    vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 p = projectionMatrix * modelViewMatrix * vec4(position,1.0); gl_Position = p.xyww; }`,
    fragmentShader: `varying vec3 vD; uniform vec3 sun; uniform float k;
      float h13(vec3 p){ p = fract(p*vec3(0.1031,0.1030,0.0973)); p += dot(p, p.yzx+33.33); return fract((p.x+p.y)*p.z); }
      float vn(vec3 p){ vec3 i=floor(p); vec3 f=fract(p); f=f*f*(3.0-2.0*f);
        return mix(mix(mix(h13(i),h13(i+vec3(1,0,0)),f.x),mix(h13(i+vec3(0,1,0)),h13(i+vec3(1,1,0)),f.x),f.y),
                   mix(mix(h13(i+vec3(0,0,1)),h13(i+vec3(1,0,1)),f.x),mix(h13(i+vec3(0,1,1)),h13(i+vec3(1,1,1)),f.x),f.y), f.z); }
      float fbm(vec3 p){ return 0.5*vn(p)+0.25*vn(p*2.03+11.3)+0.125*vn(p*4.07+27.1)+0.0625*vn(p*8.11+5.7); }
      void main(){
        vec3 d = normalize(vD); float e = d.y;
        float az = max(dot(normalize(vec3(d.x, 0.0, d.z) + 1e-5), sun), 0.0);
        vec3 zen = vec3(0.016, 0.022, 0.066), mid = vec3(0.070, 0.050, 0.130);
        vec3 horC = vec3(0.17, 0.12, 0.20), horW = vec3(0.62, 0.25, 0.20);
        vec3 hor = mix(horC, horW, pow(az, 2.5));
        vec3 c = mix(hor, mid, smoothstep(0.0, 0.20, e));
        c = mix(c, zen, smoothstep(0.14, 0.75, e));
        c += vec3(0.55, 0.20, 0.06) * pow(az, 6.0) * exp(-max(e, 0.0) * 28.0);
        // mây tầng mỏng, đáy mây bắt hồng
        vec2 cp = d.xz / max(e, 0.03) * 1.2;
        float cl = smoothstep(0.56, 0.80, fbm(vec3(cp.x*0.6, cp.y*1.4, 0.3))) * smoothstep(0.02, 0.07, e) * (1.0 - smoothstep(0.25, 0.45, e));
        vec3 cc = mix(vec3(0.10, 0.07, 0.13), vec3(0.75, 0.33, 0.28), pow(az, 1.5));
        c = mix(c, cc, cl * 0.55);
        if (e < 0.0) c = mix(hor * 0.55, vec3(0.018, 0.016, 0.024), smoothstep(0.0, -0.06, e));
        gl_FragColor = vec4(c * k, 1.0);
      }` });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(4000, 48, 24), skyMat); sky.frustumCulled = false; sky.renderOrder = -1; scene.add(sky);
  const pm = new THREE.PMREMGenerator(renderer);
  const envScene = new THREE.Scene(); envScene.add(new THREE.Mesh(sky.geometry, skyMat));
  const env = pm.fromScene(envScene, 0.04, 1, 5000).texture;
  scene.environment = env;
  scene.fog = new THREE.Fog(new THREE.Color(0.125, 0.092, 0.150), 60, 1250);

  // --- mặt đất dốc: phố xuống dần xa máy quay ---
  const gy = (z) => (z > 6 ? 0 : (z - 6) * 0.035);
  const pts = [[0, 8], [3.5, -28], [5.5, -66], [-1.5, -104], [-13, -142], [-22, -176], [-25, -196]].map(([x, z]) => new THREE.Vector3(x, 0, z));
  const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
  const L = curve.getLength();
  const at = (s) => { const u = THREE.MathUtils.clamp(s / L, 0, 1); const p = curve.getPointAt(u); p.y = gy(p.z); const t = curve.getTangentAt(u); const side = new THREE.Vector3(-t.z, 0, t.x).normalize(); return { p, t, side }; };

  // Máy quay (đặt sớm để loại nhà ngoài khung khi dựng)
  const cam = new THREE.PerspectiveCamera(50, W / H, 1, 6000);
  const cpos = new THREE.Vector3(-8, 37, 62);
  const PITCH = 19 * Math.PI / 180;
  const aim = at(70).p.clone(); const hd = new THREE.Vector3(aim.x - cpos.x, 0, aim.z - cpos.z).normalize();
  const tgt = cpos.clone().add(new THREE.Vector3(hd.x * Math.cos(PITCH), -Math.sin(PITCH), hd.z * Math.cos(PITCH)).multiplyScalar(100));
  cam.position.copy(cpos); cam.lookAt(tgt); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
  const inView = (x, y, z, m = 0.15) => { const v = new THREE.Vector3(x, y, z).project(cam); return v.z < 1 && Math.abs(v.x) < 1 + m && v.y > -1 - m * 2 && v.y < 1 + m; };
  const BGL = []; // đèn khí xa trên các phố khác (chỉ chấm hổ phách + hào quang)

  // Vật liệu
  const facadeM = procMat('facade', { color: '#ffffff', vc: true, aux: true, rough: 0.9, env: 0.9, litFrac: 0.06, winEmit: 1.4 });
  const roofM = procMat('roof', { color: '#ffffff', vc: true, rough: 0.58, env: 1.0 });
  const trimM = procMat('stone', { color: '#ffffff', vc: true, rough: 0.85, env: 0.9, sc: 3 });
  const brickM = procMat('brickwash', { color: '#8d6a5c', rough: 0.9, env: 0.8, worn: 0.75, ground: -100 });
  const streetM = procMat('setts', { color: '#6d6a68', rough: 0.72, env: 1.0, w: 0.2, l: 0.13 });
  const walkM = procMat('flags', { color: '#77716a', rough: 0.85, env: 0.9 });
  const squareM = procMat('setts', { color: '#6f6b67', rough: 0.72, env: 1.0, world: true, w: 0.21, l: 0.14 });
  const groundM = procMat('stone', { color: '#2d2a28', rough: 0.95, env: 0.6, sc: 0.8 });
  const ironM = procMat('iron', { color: '#1c1d20', rough: 0.45, metal: 0.4, env: 1.0 });
  const steelM = procMat('iron', { color: '#3b4046', rough: 0.4, metal: 0.55, env: 1.0 });
  const glassDark = procMat('plain', { color: '#1a1c20', rough: 0.08, env: 1.2 });
  const glassLit = procMat('plain', { color: '#ffcf8a', rough: 0.2, emissive: '#ffa24a', emissiveIntensity: 16 });
  const frosted = procMat('plain', { color: '#c9ccd0', rough: 0.35, env: 1.0, physical: true });
  const blackM = procMat('plain', { color: '#0b0b0c', rough: 0.6, env: 0.5 });

  // --- nền, phố, vỉa hè ---
  const gnd = new THREE.PlaneGeometry(3000, 3000, 1, 60); gnd.rotateX(-Math.PI / 2);
  { const p = gnd.attributes.position; for (let i = 0; i < p.count; i++) p.setY(i, gy(p.getZ(i)) - 0.12); gnd.computeVertexNormals(); }
  const ground = new THREE.Mesh(gnd, groundM); ground.receiveShadow = true; scene.add(ground);
  const strip = (s0, s1, l0, l1, y, uvW) => { // dải dọc phố từ lề l0 đến l1 (m), uv mét (u ngang, v dọc)
    const P = [], N = [], U = [], I = []; const ds = 1.0; let k = 0;
    for (let s = s0; s <= s1 + 1e-6; s += ds, k++) { const a = at(s); for (const l of [l0, l1]) { const v = a.p.clone().addScaledVector(a.side, l); P.push(v.x, v.y + y, v.z); N.push(0, 1, 0); U.push(l * (uvW ?? 1), s); } }
    for (let i = 0; i < k - 1; i++) { const a = i * 2; I.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); g.setIndex(I); g.computeVertexNormals(); return g; };
  const SL = L - 6;
  const road = new THREE.Mesh(strip(-2, SL, -3.0, 3.0, 0.0), streetM); road.receiveShadow = true; scene.add(road);
  for (const s of [-1, 1]) {
    const w = new THREE.Mesh(strip(4, SL, s * 3.0, s * 4.5, 0.13), walkM); w.receiveShadow = true; w.material.side = THREE.DoubleSide; scene.add(w);
    const curb = new THREE.Mesh(strip(4, SL, s * 2.98, s * 3.1, 0.14), trimM); scene.add(curb);
  }
  // quảng trường
  const sq = new THREE.Mesh(new THREE.PlaneGeometry(40, 36), squareM); sq.rotation.x = -Math.PI / 2; sq.position.set(0, 0.01, 24); sq.receiveShadow = true; scene.add(sq);

  // --- nhà: thân hộp bo cạnh, mặt tiền thủ tục (cửa sổ kính), mái đá phiến/ngói xếp lớp, gờ, ống khói ---
  const FAC = [], ROOF = [], TRIM = [], BRICK = [], TREE = [], TRUNK = [];
  const tree = (x, z, sc) => { const y = gy(z); TRUNK.push({ g: new THREE.CylinderGeometry(0.18 * sc, 0.28 * sc, 3.2 * sc, 6), m: mat4(x, y + 1.6 * sc, z) });
    const nb = 2 + Math.floor(R() * 3); for (let k = 0; k < nb; k++) { const r = (1.6 + R() * 1.4) * sc; TREE.push({ g: new THREE.IcosahedronGeometry(r, 1), m: mat4(x + (R() - 0.5) * 2.4 * sc, y + (3.6 + R() * 2.2) * sc, z + (R() - 0.5) * 2.4 * sc, R() * 6), color: ['#5d6e52', '#68724f', '#566a50', '#737a58'][Math.floor(R() * 4)] }); } };
  const paints = ['#b8a27f', '#a88579', '#8b9486', '#cbc2ab', '#7f8a94', '#9a7462', '#b5a992', '#8f8272', '#a39a8a', '#c6b69a'];
  const roofs = ['#5d636e', '#4f5560', '#6a6f78', '#8e604c', '#7b5646', '#575d68'];
  function house(M, w, d, st, seed, opt = {}) {
    const h = st * 3.1 + 0.35; const drop = 3;
    const lo = !!opt.lo;
    const body = metricUV(lo ? new THREE.BoxGeometry(w, h + drop, d) : RB(w, h + drop, d, 0.12, 1), w, d); body.translate(0, (h + drop) / 2 - drop, 0);
    const paint = opt.paint ?? paints[Math.floor(seed * 97) % paints.length];
    FAC.push({ g: body, m: M, color: paint, aux: [seed * 100, w, st, 1] });
    const cross = opt.cross ?? false; // hồi mái quay ra phố
    const pitch = 0.62 + 0.14 * ((seed * 13) % 1);
    const [rw, rd] = cross ? [d, w] : [w, d];
    const rise = rd / 2 * Math.tan(pitch), sl = rd / 2 / Math.cos(pitch) + 0.35;
    const rot = cross ? Math.PI / 2 : 0;
    const RM = M.clone().multiply(mat4(0, h, 0, rot));
    const rc = opt.roof ?? roofs[Math.floor(seed * 53) % roofs.length];
    for (const s of [1, -1]) {
      const g = lo ? new THREE.BoxGeometry(rw + 0.34, 0.15, sl) : RB(rw + 0.34, 0.15, sl, 0.05, 1);
      const p = g.attributes.position, uv = g.attributes.uv;
      for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) + rw / 2, s > 0 ? p.getZ(i) + sl / 2 : sl / 2 - p.getZ(i));
      const cz = s * (rd / 4 + 0.35 / 2 * Math.cos(pitch)), cy = rise / 2 - 0.35 / 2 * Math.sin(pitch) + 0.08;
      ROOF.push({ g, m: RM.clone().multiply(mat4(0, cy, cz, 0, s * pitch)), color: rc });
    }
    // tam giác hồi
    const tri = new THREE.Shape(); tri.moveTo(-rd / 2, 0); tri.lineTo(rd / 2, 0); tri.lineTo(0, rise); tri.lineTo(-rd / 2, 0);
    const tg = new THREE.ExtrudeGeometry(tri, { depth: rw - 0.2, bevelEnabled: false }); tg.rotateY(Math.PI / 2); tg.translate(-(rw - 0.2) / 2, 0, 0);
    { const p = tg.attributes.position, uv = tg.attributes.uv; for (let i = 0; i < p.count; i++) uv.setXY(i, p.getZ(i) + rd / 2, p.getY(i) + h); }
    FAC.push({ g: tg, m: RM, color: paint, aux: [seed * 100, w, 0, 0] });
    // gờ mái (cornice) trước và sau
    if (!cross && !lo) for (const s of [1, -1]) TRIM.push({ g: RB(w + 0.12, 0.26, 0.22, 0.05, 1), m: M.clone().multiply(mat4(0, h - 0.13, s * (d / 2 + 0.05))), color: '#d2cab8' });
    // ống khói
    const nc = 1 + ((seed * 7) % 1 > 0.5 ? 1 : 0);
    for (let c = 0; c < nc; c++) {
      const cx = (c === 0 ? -1 : 1) * (rw / 2 - 0.5);
      const ch = rise + 1.1;
      BRICK.push({ g: lo ? new THREE.BoxGeometry(0.6, ch, 0.5) : RB(0.6, ch, 0.5, 0.05, 1), m: RM.clone().multiply(mat4(cx, ch / 2 + 0.3, 0)) });
      const npots = 1 + Math.floor(((seed * 31 + c) % 1) * 3);
      if (!lo) for (let k = 0; k < npots; k++) TRIM.push({ g: new THREE.CylinderGeometry(0.08, 0.1, 0.36, 8), m: RM.clone().multiply(mat4(cx + (k - (npots - 1) / 2) * 0.19, ch + 0.48, 0)), color: '#8a5a44' });
    }
  }
  // dọc phố hai bên
  const walkFront = 4.5;
  for (const side of [-1, 1]) {
    let s = side > 0 ? 4 : 5;
    while (s < SL - 12) {
      const w = 5 + R() * 3.2; const d = 9 + R() * 3; const st = 2 + Math.floor(R() * 2.4);
      const a = at(s + w / 2);
      const c = a.p.clone().addScaledVector(a.side, side * (walkFront + d / 2));
      const dir = a.side.clone().multiplyScalar(-side);
      const M = mat4(c.x, gy(c.z) + 0.1, c.z, Math.atan2(dir.x, dir.z));
      house(M, w + 0.25, d, st, R(), { cross: R() < 0.22 });
      s += w + (R() < 0.12 ? 1.4 : 0);
    }
  }
  // ba mặt quảng trường
  for (const [x0, z0, dx, dz, n] of [[-21, 40, 0, -1, 5], [21, 40, 0, -1, 5]]) {
    let t = 0; while (t < 32) { const w = 5.5 + R() * 2.5, d = 10; const st = 3 + Math.floor(R() * 1.6);
      const c = new THREE.Vector3(x0 + dx * (t + w / 2) + Math.sign(x0) * d / 2, 0, z0 + dz * (t + w / 2));
      house(mat4(c.x, gy(c.z), c.z, x0 < 0 ? Math.PI / 2 : -Math.PI / 2), w + 0.2, d, st, R()); t += w; void n; }
  }
  // dãy nhà phía bắc quảng trường (dưới máy quay, tiền cảnh nhoè)
  { let t = 0; while (t < 44) { const w = 5.5 + R() * 3; house(mat4(-22 + t + w / 2, 0, 49, Math.PI), w + 0.2, 10, 3 + Math.floor(R() * 1.5), R()); t += w; } }
  // thành phố nền (lưới, lệch ngẫu nhiên), bỏ vùng quanh phố và quảng trường
  const cl = []; for (let s = -2; s < L; s += 2) cl.push(at(s).p);
  const nearStreet = (x, z, r) => cl.some((p) => (p.x - x) ** 2 + (p.z - z) ** 2 < r * r);
  // Khối phố 40×34 m, phố 9 m giữa các khối; nhà liền kề quanh chu vi khối (sân trong ở giữa).
  const BX = 52, BZ = 45, TH = 0.33; // lưới khối xoay ~19° so với trục nhìn → bớt cảm giác lưới máy tính
  const G = (x, z) => { const dx = x + 10, dz = z + 150; return [-10 + dx * Math.cos(TH) + dz * Math.sin(TH), -150 - dx * Math.sin(TH) + dz * Math.cos(TH)]; };
  const pushLamp = (x, z) => { const [gx, gz] = G(x, z); if (nearStreet(gx, gz, 9) || (Math.abs(gx) < 30 && gz > 0 && gz < 55)) return; BGL.push(new THREE.Vector3(gx, gy(gz) + 3.4, gz)); };
  for (let j = -2; j < 26; j++) for (let i = -3; i < 20; i++) {
    const bx = -430 + i * BX, bz = 64 - j * BZ;
    const [cx, cz] = G(bx + 20, bz - 17);
    if (!inView(cx, gy(cz) + 6, cz, 0.35)) continue;
    const dist = Math.hypot(cx - cpos.x, cz - cpos.z); const lo = dist > 140;
    // đèn khí dọc mép phố phía +z và phía +x của khối
    for (let t = 6; t < 40; t += 21) if (R() < 0.45) pushLamp(bx + t, bz + 5.5);
    for (let t = 5; t < 40; t += 15) if (R() < 0.6) pushLamp(bx + 40 + ((t / 15) % 2 < 1 ? 3 : 9), bz - t);
    if (!lo || dist < 420) { const nt = Math.floor(R() * 3.2); for (let k = 0; k < nt; k++) { const [tx, tz] = G(bx + 11 + R() * 18, bz - 10 - R() * 14); if (!nearStreet(tx, tz, 14)) tree(tx, tz, 0.9 + R() * 0.5); } }
    const tall = R() < 0.12 ? 1.6 : 0; // vài khối nhà cao hơn (kho, xưởng)
    const edges = [[bx, bz, 1, 0, 40], [bx + 40, bz - 34, -1, 0, 40], [bx + 40, bz, 0, -1, 34], [bx, bz - 34, 0, 1, 34]];
    for (const [ex, ez, dx, dz, len] of edges) {
      let t = 0;
      while (t < len - 4) {
        const w = Math.min(len - t, 5.5 + R() * 4.5), d = 8.5 + R() * 2.5, st = 2 + Math.floor(R() * 2.6 + tall);
        // mặt tiền hướng ra phố (ra ngoài khối): pháp tuyến ngoài = (−dz, dx)
        const nx = -dz, nz = dx;
        const [hx, hz] = G(ex + dx * (t + w / 2) - nx * d / 2, ez + dz * (t + w / 2) - nz * d / 2);
        const skip = nearStreet(hx, hz, 12) || (Math.abs(hx) < 30 && hz > -2 && hz < 55) || R() < 0.04;
        if (!skip) house(mat4(hx, gy(hz), hz, Math.atan2(nx, nz) + TH + (R() - 0.5) * 0.04), w + 0.1, d, st, R(), { cross: R() < 0.18, lo });
        t += w;
      }
    }
  }
  // nhà kho cuối phố: tường gạch trắng vôi + hốc bốc hàng tối
  {
    const a = at(SL + 4); const dir = a.t.clone().multiplyScalar(-1);
    const c = a.p.clone().addScaledVector(a.t, 12);
    const M = mat4(c.x, gy(c.z), c.z, Math.atan2(dir.x, dir.z));
    const wg = metricUV(RB(34, 16, 24, 0.2, 2), 34, 24); wg.translate(0, 5, 0);
    FAC.push({ g: wg, m: M, color: '#ddd8cc', aux: [0.37 * 100, 34, 0, 0] });
    TRIM.push({ g: RB(3.4, 4.2, 0.6, 0.1, 1), m: M.clone().multiply(mat4(4, 2.0, 12.0)), color: '#161413' });
    const rg = RB(35, 0.3, 14, 0.08, 1); { const p = rg.attributes.position, uv = rg.attributes.uv; for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i), p.getZ(i) + 7); }
    ROOF.push({ g: rg, m: M.clone().multiply(mat4(0, 13.6, 6, 0, 0.38)), color: '#4a4c52' });
    const rg2 = rg.clone(); ROOF.push({ g: rg2, m: M.clone().multiply(mat4(0, 13.6, -6, Math.PI, 0.38)), color: '#4a4c52' });
  }
  const addMerged = (list, m, opt) => { const g = mergeInto(list, opt); const mesh = new THREE.Mesh(g, m); mesh.castShadow = mesh.receiveShadow = true; scene.add(mesh); return mesh; };
  addMerged(FAC, facadeM, { color: true, aux: true });
  addMerged(ROOF, roofM, { color: true });
  addMerged(TRIM, trimM, { color: true });
  addMerged(BRICK, brickM, {});
  addMerged(TREE, procMat('felt', { color: '#ffffff', vc: true, rough: 0.95, sheen: 1.0, sheenColor: '#8a9a88', sheenRough: 0.5, env: 1.0, mot: 1.5 }), { color: true });
  addMerged(TRUNK, procMat('wood', { color: '#3a2e26', rough: 0.9, env: 0.8 }), {});

  // đồi xa + ống khói nhà máy + bồn khí (bóng dáng chân trời)
  {
    const rg = []; const N = 120; const P = [];
    for (let i = 0; i <= N; i++) { const x = -2600 + 5200 * i / N; const hgt = 10 + 16 * Math.sin(i * 0.21) * 0.5 + 12 * Math.sin(i * 0.57 + 1) * 0.5 + 5 * R(); P.push([x, hgt]); }
    const pos = []; for (let i = 0; i < N; i++) { const [x0, h0] = P[i], [x1, h1] = P[i + 1]; const z = -1700; pos.push(x0, -60, z, x1, -60, z, x1, h1, z, x0, -60, z, x1, h1, z, x0, h0, z); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
    g.setAttribute('uv', new THREE.Float32BufferAttribute(new Array(pos.length / 3 * 2).fill(0), 2)); void rg;
    scene.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: new THREE.Color(0.10, 0.074, 0.122), fog: false, side: THREE.DoubleSide })));
    const stk = [];
    for (const [x, z, hh] of [[-150, -760, 38], [-128, -780, 30], [210, -640, 34]]) stk.push({ g: new THREE.CylinderGeometry(1.1, 1.9, hh, 10), m: mat4(x, gy(z) + hh / 2, z), color: '#5a4038' });
    for (let i = 0; i < 10; i++) { const a = i / 10 * Math.PI * 2; stk.push({ g: new THREE.CylinderGeometry(0.4, 0.4, 26, 6), m: mat4(95 + 16 * Math.cos(a), gy(-520) + 13, -520 + 16 * Math.sin(a)), color: '#3a3a40' }); }
    stk.push({ g: new THREE.CylinderGeometry(15, 15, 18, 36), m: mat4(95, gy(-520) + 9, -520), color: '#4c4d52' });
    stk.push({ g: new THREE.TorusGeometry(16, 0.35, 4, 36), m: mat4(95, gy(-520) + 26, -520, 0, Math.PI / 2), color: '#3a3a40' });
    addMerged(stk, trimM, { color: true });
  }

  // --- đèn khí (11), cột điện kiểu mới (6), dây điện ---
  const lampS = Array.from({ length: 11 }, (_, i) => 12 + i * 16.8);
  const LIT = 4;
  const IRON = [], GLASSD = [], GLASSL = [], STEEL = [], FROST = [], BLACK = [];
  const postProfile = [[0.001, 0], [0.19, 0], [0.19, 0.22], [0.13, 0.32], [0.1, 0.5], [0.075, 0.9], [0.058, 2.7], [0.075, 2.78], [0.06, 2.86], [0.05, 3.0], [0.001, 3.02]].map(([r, y]) => new THREE.Vector2(r, y));
  const postG = new THREE.LatheGeometry(postProfile, 10);
  const lampLights = []; const lampHeads = [];
  lampS.forEach((s, i) => {
    const side = i % 2 ? 1 : -1; const a = at(s);
    const p = a.p.clone().addScaledVector(a.side, side * 3.3); p.y = gy(p.z) + 0.13;
    const ry = Math.atan2(a.side.x * side, a.side.z * side);
    IRON.push({ g: postG, m: mat4(p.x, p.y, p.z, ry) });
    IRON.push({ g: new THREE.BoxGeometry(0.72, 0.045, 0.045), m: mat4(p.x, p.y + 2.72, p.z, ry) }); // tay tựa thang
    IRON.push({ g: new THREE.CylinderGeometry(0.13, 0.07, 0.1, 4), m: mat4(p.x, p.y + 3.07, p.z, ry + Math.PI / 4) });
    IRON.push({ g: new THREE.ConeGeometry(0.28, 0.24, 4), m: mat4(p.x, p.y + 3.66, p.z, ry + Math.PI / 4) });
    IRON.push({ g: new THREE.SphereGeometry(0.05, 8, 6), m: mat4(p.x, p.y + 3.83, p.z) });
    const gg = new THREE.CylinderGeometry(0.2, 0.13, 0.46, 4, 1);
    (i < LIT ? GLASSL : GLASSD).push({ g: gg, m: mat4(p.x, p.y + 3.33, p.z, ry + Math.PI / 4) });
    lampHeads.push(new THREE.Vector3(p.x, p.y + 3.3, p.z));
  });
  const elecS = [0, 1, 2, 3, 4, 5].map((k) => 20.4 + 33.6 * k);
  const elecTops = [];
  elecS.forEach((s, k) => {
    const side = k % 2 ? -1 : 1; const a = at(Math.min(s, SL - 2));
    const p = a.p.clone().addScaledVector(a.side, side * 3.45); p.y = gy(p.z) + 0.13;
    const inward = a.side.clone().multiplyScalar(-side);
    const ry = Math.atan2(inward.x, inward.z);
    STEEL.push({ g: new THREE.CylinderGeometry(0.065, 0.11, 7.0, 10), m: mat4(p.x, p.y + 3.5, p.z) });
    STEEL.push({ g: new THREE.CylinderGeometry(0.2, 0.24, 0.5, 10), m: mat4(p.x, p.y + 0.25, p.z) });
    const arm = mat4(p.x, p.y + 7.0, p.z, ry);
    STEEL.push({ g: RB(0.06, 0.06, 1.3, 0.02, 1), m: arm.clone().multiply(mat4(0, 0, 0.6)) });
    STEEL.push({ g: RB(0.95, 0.16, 0.6, 0.04, 1), m: arm.clone().multiply(mat4(0, -0.12, 1.25)) });
    FROST.push({ g: new THREE.BoxGeometry(0.85, 0.03, 0.5), m: arm.clone().multiply(mat4(0, -0.215, 1.25)) });
    elecTops.push(new THREE.Vector3(p.x, p.y + 6.8, p.z));
  });
  // dây điện võng giữa các cột (2 sợi)
  const WIRES = [];
  for (let k = 0; k < elecTops.length - 1; k++) for (const dy of [0, -0.35]) {
    const a = elecTops[k].clone(), b = elecTops[k + 1].clone(); a.y += dy; b.y += dy;
    const cps = []; for (let j = 0; j <= 16; j++) { const t = j / 16; const v = a.clone().lerp(b, t); v.y -= 1.1 * 4 * t * (1 - t); cps.push(v); }
    WIRES.push({ g: new THREE.TubeGeometry(new THREE.CatmullRomCurve3(cps), 32, 0.028, 4) });
  }
  // cột đồng hồ điện ở quảng trường (chưa sáng): mặt kính mờ 1,2 m, 12 vạch, 2 kim, không chữ số
  {
    const cx = -3, cz = 13, y0 = 0;
    const prof = [[0.001, 0], [0.42, 0], [0.42, 0.35], [0.3, 0.5], [0.22, 0.9], [0.13, 1.4], [0.11, 5.4], [0.16, 5.55], [0.001, 5.6]].map(([r, y]) => new THREE.Vector2(r, y));
    IRON.push({ g: new THREE.LatheGeometry(prof, 16), m: mat4(cx, y0, cz) });
    const face = mat4(cx, y0 + 6.25, cz, 0.35);
    IRON.push({ g: new THREE.CylinderGeometry(0.68, 0.68, 0.22, 40), m: face.clone().multiply(mat4(0, 0, 0, 0, Math.PI / 2)) });
    for (const s of [1, -1]) {
      FROST.push({ g: new THREE.CylinderGeometry(0.6, 0.6, 0.02, 40), m: face.clone().multiply(mat4(0, 0, s * 0.115, 0, Math.PI / 2)) });
      for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2; BLACK.push({ g: new THREE.BoxGeometry(0.035, 0.13, 0.01), m: face.clone().multiply(mat4(0.5 * Math.sin(a), 0.5 * Math.cos(a), s * 0.128, 0, 0, -a)) }); }
      const hh = -0.35, mm = -0.52;
      BLACK.push({ g: new THREE.BoxGeometry(0.045, 0.32, 0.01), m: face.clone().multiply(mat4(0.16 * Math.sin(hh), 0.16 * Math.cos(hh), s * 0.132, 0, 0, -hh)) });
      BLACK.push({ g: new THREE.BoxGeometry(0.03, 0.52, 0.01), m: face.clone().multiply(mat4(0.26 * Math.sin(mm), 0.26 * Math.cos(mm), s * 0.134, 0, 0, -mm)) });
    }
    IRON.push({ g: new THREE.SphereGeometry(0.12, 12, 8), m: mat4(cx, y0 + 7.0, cz) });
    // cột điện 4 góc quảng trường
    for (const [x, z] of [[-14, 8], [14, 8], [-14, 36], [14, 36]]) {
      STEEL.push({ g: new THREE.CylinderGeometry(0.065, 0.11, 7.0, 10), m: mat4(x, 3.5, z) });
      STEEL.push({ g: RB(0.95, 0.16, 0.6, 0.04, 1), m: mat4(x, 7.0, z) });
      FROST.push({ g: new THREE.BoxGeometry(0.85, 0.03, 0.5), m: mat4(x, 6.905, z) });
    }
    // cọc chắn đá quanh quảng trường
    for (let k = 0; k < 16; k++) TRIM.length; // (không dùng)
  }
  addMerged(IRON, ironM); addMerged(STEEL, steelM); addMerged(FROST, frosted); addMerged(BLACK, blackM);
  addMerged(GLASSD, glassDark); const gl = addMerged(GLASSL, glassLit); gl.castShadow = false;
  const wm = addMerged(WIRES, blackM); wm.castShadow = false;

  // --- ánh sáng ---
  const LCOL = new THREE.Color(1.0, 0.47, 0.15); const LAMPI = 190;
  // hào quang: đèn phố Ostler đã thắp + đèn khí xa trên các phố khác
  const HL = [], HC = [];
  for (let i = 0; i < LIT; i++) { HL.push({ p: lampHeads[i], c: new THREE.Color(1.0, 0.48, 0.18).multiplyScalar(0.9) }); HC.push({ p: lampHeads[i], c: new THREE.Color(1.0, 0.78, 0.5).multiplyScalar(1.5) }); }
  for (const p of BGL) { HL.push({ p, c: new THREE.Color(1.0, 0.46, 0.16).multiplyScalar(0.45) }); HC.push({ p, c: new THREE.Color(1.0, 0.75, 0.45).multiplyScalar(0.9) }); }
  // Chỉ giữ đèn nền nhìn thấy được từ máy quay (kiểm độ sâu trên GPU một lần), tránh hào quang xuyên mái.
  { const vis = visibleFrom(scene, cam, BGL.map((p) => p.clone().add(new THREE.Vector3(0, 0.4, 0))), 2.5);
    const keep = BGL.filter((_, i) => vis[i]); console.log('BGL visible', keep.length, '/', BGL.length);
    HL.length = LIT; HC.length = LIT;
    for (const p of keep) { HL.push({ p, c: new THREE.Color(1.0, 0.46, 0.16).multiplyScalar(0.9) }); HC.push({ p, c: new THREE.Color(1.0, 0.75, 0.45).multiplyScalar(1.4) }); }
    // quầng khí sáng (sương bắt ánh đèn) phía trên các ngọn bị mái che: thấy lờ mờ trên nóc nhà
    const haze = BGL.filter((p, i) => !vis[i] && (i % 2 === 0) && p.distanceTo(cpos) < 520).map((p) => ({ p: p.clone().add(new THREE.Vector3(0, 9.5, 0)), c: new THREE.Color(1.0, 0.45, 0.17).multiplyScalar(0.16) }));
    scene.add(haloPoints(haze, 15.0)); }
  // đặt hào quang lệch ~1,2 m về phía máy quay để không bị chính mũ đèn che (hào quang là hiện tượng của ống kính/không khí)
  for (const L of [HL, HC]) for (const it of L) it.p = it.p.clone().add(cpos.clone().sub(it.p).normalize().multiplyScalar(1.2));
  const hp1 = haloPoints(HL, 9.0), hp2 = haloPoints(HC, 2.2); scene.add(hp1, hp2);
  if (DBG.bigHalo) { hp1.material.size = 60; hp1.material.depthTest = false; console.log('BGL', BGL.length, JSON.stringify(BGL.slice(0,3))); }
  const lampLightsArr = [];
  for (let i = 0; i < LIT; i++) {
    const hp = lampHeads[i];
    if (i === LIT - 1) {
      const sp = new THREE.SpotLight(LCOL, LAMPI, 0, 1.35, 0.55, 2); sp.position.copy(hp); sp.target.position.set(hp.x, hp.y - 10, hp.z);
      sp.castShadow = true; sp.shadow.mapSize.set(1024, 1024); sp.shadow.camera.near = 0.3; sp.shadow.camera.far = 30; sp.shadow.bias = -0.0008; sp.shadow.normalBias = 0.02;
      scene.add(sp, sp.target); lampLightsArr.push(sp);
    } else { const pl = new THREE.PointLight(LCOL, LAMPI, 0, 2); pl.position.copy(hp); scene.add(pl); lampLightsArr.push(pl); }
  }
  // Ánh hồng cuối trời: nguồn rộng, thấp phía tây — đèn hướng rất yếu, jitter lớn (bóng rất mềm), chỉ chạm mái và tầng trên.
  const glowL = new THREE.DirectionalLight(new THREE.Color(1.0, 0.55, 0.52), 2.4);
  glowL.castShadow = true; glowL.shadow.mapSize.set(2048, 2048);
  Object.assign(glowL.shadow.camera, { left: -170, right: 170, top: 170, bottom: -170, near: 10, far: 900 }); glowL.shadow.bias = -0.0015; glowL.shadow.normalBias = 0.3;
  glowL.target.position.set(0, 0, -70); scene.add(glowL, glowL.target);

  // --- Ida rất nhỏ, vác thang, vừa rời ngọn đèn số 4 ---
  const { ida } = characters(env, 1.2);
  ida.setPose(sheets.ida.poses.walk_ladder);
  const sI = lampS[LIT - 1] + 2.2; const aI = at(sI); const side = (LIT - 1) % 2 ? 1 : -1;
  const pI = aI.p.clone().addScaledVector(aI.side, side * 3.75); pI.y = gy(pI.z) + 0.13;
  ida.root.position.set(pI.x, pI.y, pI.z); ida.root.rotation.y = Math.atan2(aI.t.x, aI.t.z);
  ida.root.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  scene.add(ida.root);
  bakeStatic(ida.root, scene);
  const belt = new THREE.Vector3(); ida.props.lantern.getWorldPosition(belt);
  const bh = haloSprite(new THREE.Color(1.0, 0.6, 0.25), 0.7, 0.5); bh.position.copy(belt).add(new THREE.Vector3(0, 0.1, 0)); scene.add(bh);

  // --- máy quay ~38 m trên quảng trường, chúc ~22°, nhìn dọc phố cong; tilt-shift: khẩu độ lớn so với "mô hình" ---
  const idaC = new THREE.Vector3(pI.x, pI.y + 1, pI.z);
  const dof = dofCamera(cam, cpos, tgt, cpos.distanceTo(idaC), 0.8); dof.reset();
  // lấy nét đúng khoảng cách tới Ida dọc trục nhìn
  { const fwd = tgt.clone().sub(cpos).normalize(); const fd = idaC.clone().sub(cpos).dot(fwd); const d2 = dofCamera(cam, cpos, tgt, fd, 0.8); Object.assign(dof, d2); dof.reset(); }

  const sunBase = SUN.clone();
  const onSample = (i, n) => {
    dof.jitter(i, n);
    const az = (halton(i, 2) - 0.5) * 0.9, el = 0.06 + halton(i, 3) * 0.16;
    const d = sunBase.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), az); d.y = Math.sin(el); d.normalize();
    glowL.position.copy(glowL.target.position).addScaledVector(d, 400);
    const sp = lampLightsArr[LIT - 1]; const hp = lampHeads[LIT - 1];
    sp.position.set(hp.x + (halton(i, 5) - 0.5) * 0.12, hp.y + (halton(i, 7) - 0.5) * 0.1, hp.z + (halton(i, 11) - 0.5) * 0.12);
  };
  // Ánh trời (IBL) mạnh hơn: đồng bộ phơi sáng với trời trong hình
  const seen = new Set(); scene.traverse((o) => { if (o.material && !seen.has(o.material) && o.material.envMapIntensity != null && o !== sky) { seen.add(o.material); o.material.envMapIntensity *= ENVK; } });
  return { scene, cam, dof, onSample, exposure: 2.2, vig: 0.38, cool: 0.35 };
}

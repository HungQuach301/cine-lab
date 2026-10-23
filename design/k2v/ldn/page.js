// K2V ldn · TRANG DỰNG LONDON (T4 K2C-T4-02) — cách A sơ bộ cho tiền kỳ: three.js 0.180 + post.js dùng chung, Chromium headless (llvmpipe).
// Hình học từ scripts/k2ldn/hinh_hoc.py (ldn.bin, dùng chung với Cycles). Thời gian: uYear (năm thập phân) + uHour (giờ kể từ 2/9/1666 00:00 lịch Julius; < 0 = tắt chế độ cháy).
// Mỗi đỉnh tl = [năm sinh, năm mất, y đáy, giờ bén lửa]. Lửa/khói: hạt billboard tất định theo thời gian (không trạng thái) + bản đồ ánh lửa 20 m (CPU) chiếu lên mặt tường/mặt nước.
// KHÔNG sửa design/k2v/tl/* (T3). Driver: scripts/k2ldn/render_ldn.js.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { sunPos, jdOf, jdJulian } from '/k2v/tl/sun.js';

const LON = { lat: 51.512, lon: -0.098 };
let R, pipe, scene, cam, META, BLD, TER, WATER, SKY, FIRE, SMOKE, FMAP, FTEX, LG = {}, SH = {}, CFG, ACC = {};
const U = { uYear: { value: 1666.5 }, uHour: { value: -1 }, uT: { value: 0 }, uNight: { value: 0 }, uFire: { value: null }, uFireBox: { value: new THREE.Vector4() },
  uSunDir: { value: new THREE.Vector3(0, 1, 0) }, uSunCol: { value: new THREE.Color(1, 1, 1) }, uSky: { value: new THREE.Color(0.6, 0.7, 0.85) }, uHaze: { value: new THREE.Color(0.7, 0.74, 0.8) },
  uHazeK: { value: 1 / 7000 }, uCam: { value: new THREE.Vector3() }, uFireK: { value: 1 }, uWin: { value: 0 }, uMask: { value: 0 } };

// ---------------------------------------------------------------- thời gian
const yearOfHour = (h) => 1666 + (244 + h / 24) / 365;          // 2/9 (J.) = ngày 245 (0-based 244)
const burnI = `float burnI(float ign, float h){ if (ign < 0.0 || h < ign) return 0.0; float a = h - ign;
  return smoothstep(0.0, 0.7, a) * (1.0 - smoothstep(4.0, 9.0, a)) + 0.025 * (1.0 - smoothstep(9.0, 48.0, a)) * step(9.0, a); }`;
const GLSL_N = `vec3 s2l(vec3 c){ return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }
  float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f); return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
  float fbm(vec2 p){ float s = 0.0, a = 0.5; for (int i = 0; i < 5; i++){ s += a * vn(p); p = p * 2.03 + 7.1; a *= 0.5; } return s; }`;

// ---------------------------------------------------------------- vật liệu nhà (Lambert + chèn: mọc/mất theo năm, cháy theo giờ, ánh lửa)
function patch(mat, depth) {
  mat.onBeforeCompile = (s) => {
    Object.assign(s.uniforms, U);
    s.vertexShader = s.vertexShader.replace('#include <common>', `#include <common>
      attribute vec4 tl; attribute float kk; uniform float uYear, uHour; varying float vAlive; varying float vBurn; varying vec3 vW; varying float vK; varying float vRel;
      ${burnI}`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>
      float alive = 1.0, grow = 1.0;
      bool fireMode = uHour >= 0.0; float ign = tl.w;
      if (fireMode && ign >= 0.0) {
        float a = uHour - ign;
        if (kk < 1.5 || kk > 7.5 || (kk > 4.5 && kk < 5.5)) { alive = a < 7.0 ? 1.0 : 0.0; grow = a < 2.5 ? 1.0 : mix(1.0, 0.35, smoothstep(2.5, 7.0, a)); }   // nhà/tháp/công trình cháy: sập dần
        else if (kk > 1.5 && kk < 2.5) { alive = a > 5.0 ? 1.0 : 0.0; }                                                                          // phế tích
        else alive = 0.0;                                                                                                                        // nhà xây lại: chưa có
        if (kk > 4.5 && kk < 5.5 && tl.y > 1667.0) alive = a > 6.0 ? 1.0 : 0.0;                                                                 // phế tích công trình có tên
      } else {
        alive = (uYear >= tl.x && uYear < tl.y) ? 1.0 : 0.0;
        float gw = kk > 3.5 && kk < 4.5 ? 2.5 : (kk > 4.5 && kk < 5.5 ? 1.5 : 0.6);
        grow = clamp((uYear - tl.x) / gw, 0.0, 1.0); grow = grow * grow * (3.0 - 2.0 * grow);
        if (fireMode) { alive = (tl.x < 1666.68 && tl.y > 1666.67) ? 1.0 : 0.0; grow = 1.0; }
      }
      transformed.y = tl.z + (transformed.y - tl.z) * max(grow, 0.001);
      vAlive = alive; vBurn = fireMode ? burnI(ign, uHour) : 0.0; vK = kk; vRel = transformed.y - tl.z;
      vW = (modelMatrix * vec4(transformed, 1.0)).xyz;`);
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>
      varying float vAlive; varying float vBurn; varying vec3 vW; varying float vK; varying float vRel;
      uniform sampler2D uFire; uniform vec4 uFireBox; uniform float uT, uNight, uFireK, uWin, uMask; uniform vec3 uHaze, uCam; uniform float uHazeK;
      ${GLSL_N}`);
    if (depth) s.fragmentShader = s.fragmentShader.replace('void main() {', 'void main() { if (vAlive < 0.5) discard;');
    else s.fragmentShader = s.fragmentShader.replace('void main() {', 'void main() { if (vAlive < 0.5) discard;')
      .replace('#include <dithering_fragment>', `#include <dithering_fragment>
        vec2 fu = (vW.xz - uFireBox.xy) / uFireBox.zw; vec3 fg = texture2D(uFire, fu).rgb;               // ánh lửa: 3 bán kính (gần/vừa/xa)
        float hfall = exp(-max(vW.y - 5.0, 0.0) / 60.0);
        vec3 fireCol = vec3(1.0, 0.42, 0.12);
        vec3 alb = vColor.rgb;
        gl_FragColor.rgb += alb * fireCol * uFireK * (fg.r * 2.2 * hfall + fg.g * 0.45 + fg.b * 0.05);
        if (vBurn > 0.01) {                                                                               // tường đang cháy: than + cửa sổ rực
          float fl = fbm(vec2(vW.x * 0.35 + uT * 1.7, vW.y * 0.6 - uT * 3.1)) ;
          gl_FragColor.rgb = mix(gl_FragColor.rgb, gl_FragColor.rgb * 0.25, clamp(vBurn * 1.4, 0.0, 0.8));
          gl_FragColor.rgb += fireCol * vBurn * (0.6 + 1.6 * smoothstep(0.45, 0.8, fl)) * 2.2;
        }
        if (uWin > 0.0 && vK > 3.5 && vK < 4.5 && vRel > 3.0) {                                           // 2026: cửa sổ sáng ban đêm
          vec2 g = vec2(vW.x + vW.z, vW.y) / vec2(3.2, 3.6); vec2 f = fract(g);
          float on = step(0.45, h21(floor(g) + floor(vW.xz / 40.0))) * step(0.18, f.x) * step(f.x, 0.82) * step(0.25, f.y) * step(f.y, 0.75);
          gl_FragColor.rgb += vec3(1.0, 0.78, 0.5) * on * uWin * 0.9;
        }
        float dist = length(vW - uCam); gl_FragColor.rgb = mix(gl_FragColor.rgb, uHaze, 1.0 - exp(-dist * uHazeK));
        if (uMask > 0.5) gl_FragColor = vec4(s2l(vec3(235.0, 235.0, 235.0) / 255.0), 1.0);   // 'nha' (bảng màu n2p_lib)`);
  };
  mat.customProgramCacheKey = () => (depth ? 'ldn-d' : 'ldn-c');
}

// ---------------------------------------------------------------- dựng cảnh
async function build(cfg) {
  const base = cfg.data;
  META = await (await fetch(base + 'ldn.json')).json();
  const buf = await (await fetch(base + 'ldn.bin')).arrayBuffer();
  const A = (nm, T) => { const l = META.bo_cuc[nm]; return new T(buf, l.off, l.len / T.BYTES_PER_ELEMENT); };
  const pos = A('pos', Float32Array), col = A('col', Uint8Array), tl = A('tl', Float32Array), kk = A('k', Uint8Array);
  const g = new THREE.BufferGeometry();
  const LUT8 = new Float32Array(256).map((_, i) => Math.pow(i / 255, 2.2)); const colL = new Float32Array(col.length); for (let i = 0; i < col.length; i++) colL[i] = LUT8[col[i]];   // màu đỉnh sRGB → tuyến tính
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(colL, 3));
  g.setAttribute('tl', new THREE.BufferAttribute(tl, 4)); g.setAttribute('kk', new THREE.BufferAttribute(new Float32Array(kk), 1));
  g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ vertexColors: true }); patch(m, false);
  BLD = new THREE.Mesh(g, m); BLD.castShadow = BLD.receiveShadow = true; BLD.frustumCulled = false;
  const dm = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }); patch(dm, true); BLD.customDepthMaterial = dm;
  scene.add(BLD);
  // địa hình: hai cao độ (1666 / 2026), Embankment 1864–1870
  const T = META.dia_hinh, nx = T.nx, nz = T.nz; const h26 = A('h26', Float32Array), h66 = A('h66', Float32Array), xanh = A('xanh', Uint8Array);
  const tg = new THREE.PlaneGeometry(1, 1, nx - 1, nz - 1); const tp = tg.attributes.position.array, H2 = new Float32Array(nx * nz), H6 = new Float32Array(nx * nz), GR = new Float32Array(nx * nz);
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const v = j * nx + i; tp[v * 3] = T.x0 + i * T.step; tp[v * 3 + 1] = 0; tp[v * 3 + 2] = T.z0 + j * T.step; H2[v] = h26[v]; H6[v] = h66[v]; GR[v] = xanh[v]; }
  tg.setAttribute('h2', new THREE.BufferAttribute(H2, 1)); tg.setAttribute('h6', new THREE.BufferAttribute(H6, 1)); tg.setAttribute('gr', new THREE.BufferAttribute(GR, 1));
  const tm = new THREE.MeshLambertMaterial({ color: 0xffffff });
  tm.onBeforeCompile = (s) => { Object.assign(s.uniforms, U);
    s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nattribute float h2, h6, gr; uniform float uYear; varying vec3 vW; varying float vGr; varying float vWet;')
      .replace('#include <begin_vertex>', `#include <begin_vertex>
        float k = smoothstep(1864.0, 1870.5, uYear); transformed.y = mix(h6, h2, k); vGr = gr * step(1850.0, uYear); vWet = smoothstep(1.0, -1.0, transformed.y);
        vW = (modelMatrix * vec4(transformed, 1.0)).xyz;`)
      .replace('#include <beginnormal_vertex>', '#include <beginnormal_vertex>');
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>
      varying vec3 vW; varying float vGr; varying float vWet; uniform sampler2D uFire; uniform vec4 uFireBox; uniform float uFireK, uYear, uMask; uniform vec3 uHaze, uCam; uniform float uHazeK; ${GLSL_N}`)
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', `float n = fbm(vW.xz * 0.06);
        vec3 c66 = mix(vec3(0.43, 0.38, 0.30), vec3(0.50, 0.45, 0.36), n);       // đất nện / sỏi
        vec3 c26 = mix(vec3(0.50, 0.49, 0.47), vec3(0.56, 0.55, 0.52), n);       // lát đá / nhựa
        vec3 cg = mix(vec3(0.27, 0.36, 0.20), vec3(0.33, 0.42, 0.24), n);
        vec3 cc = mix(c66, c26, smoothstep(1850.0, 1950.0, uYear)); cc = mix(cc, cg, vGr); cc = mix(cc, vec3(0.30, 0.27, 0.23), vWet);
        vec4 diffuseColor = vec4(cc, 1.0);`)
      .replace('#include <dithering_fragment>', `#include <dithering_fragment>
        vec2 fu = (vW.xz - uFireBox.xy) / uFireBox.zw; vec3 fg = texture2D(uFire, fu).rgb;
        gl_FragColor.rgb += vec3(1.0, 0.42, 0.12) * uFireK * (fg.r * 1.4 + fg.g * 0.5 + fg.b * 0.08) * 0.5;
        float dist = length(vW - uCam); gl_FragColor.rgb = mix(gl_FragColor.rgb, uHaze, 1.0 - exp(-dist * uHazeK));
        if (uMask > 0.5) gl_FragColor = vec4(s2l(vec3(200.0, 170.0, 90.0) / 255.0), 1.0);   // 'bang'`); };
  TER = new THREE.Mesh(tg, tm); TER.receiveShadow = true; TER.frustumCulled = false; scene.add(TER);
  // mặt nước (Thames): phản chiếu trời + ánh lửa, gợn thủ tục
  const wm = new THREE.ShaderMaterial({ uniforms: U, vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `varying vec3 vW; uniform vec3 uSky, uHaze, uCam, uSunDir, uSunCol; uniform float uHazeK, uT, uFireK, uNight, uMask; uniform sampler2D uFire; uniform vec4 uFireBox; ${GLSL_N}
      void main(){ vec3 V = normalize(uCam - vW); vec2 q = vW.xz * 0.08 + vec2(uT * 0.05, uT * 0.02);
        vec3 N = normalize(vec3((fbm(q) - 0.5) * 0.18, 1.0, (fbm(q + 9.3) - 0.5) * 0.18)); float fr = 0.03 + 0.97 * pow(1.0 - max(dot(N, V), 0.0), 5.0);
        vec3 deep = mix(vec3(0.08, 0.10, 0.10), vec3(0.015, 0.02, 0.03), uNight);
        vec3 c = mix(deep, uSky * 0.95, fr);
        vec3 Rf = reflect(-V, N); c += uSunCol * pow(max(dot(Rf, uSunDir), 0.0), 300.0) * 3.0 * (1.0 - uNight);
        vec2 fu = (vW.xz + vec2(0.0, -120.0) - uFireBox.xy) / uFireBox.zw; vec3 fg = texture2D(uFire, fu + (N.xz) * 0.02).rgb;
        c += vec3(1.0, 0.45, 0.15) * uFireK * (fg.g * 0.10 + fg.b * 0.03) * (0.15 + fr);
        float d = length(vW - uCam); c = mix(c, uHaze, 1.0 - exp(-d * uHazeK)); gl_FragColor = vec4(c, 1.0); if (uMask > 0.5) gl_FragColor = vec4(vec3(0.0, 170.0, 190.0) / 255.0, 1.0); }` });   // 'nuoc' (ShaderMaterial: không mã hoá sRGB)
  // mặt nước chỉ trong hộp địa hình (ngoài hộp là đất xa — tránh dải "biển" giả ở chân trời: London không có biển)
  const TW = (T.nx - 1) * T.step, TD = (T.nz - 1) * T.step;
  WATER = new THREE.Mesh(new THREE.PlaneGeometry(TW, TD).rotateX(-Math.PI / 2), wm); WATER.position.set(T.x0 + TW / 2, 0.6, T.z0 + TD / 2); scene.add(WATER);
  const fm = new THREE.MeshLambertMaterial({ color: new THREE.Color(0.30, 0.28, 0.24) });
  fm.onBeforeCompile = (s) => { Object.assign(s.uniforms, U); s.fragmentShader = s.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uMask; uniform vec3 uHaze, uCam; uniform float uHazeK; varying vec3 vWf;').replace('#include <dithering_fragment>', '#include <dithering_fragment>\n float dist = length(vWf - uCam); gl_FragColor.rgb = mix(gl_FragColor.rgb, uHaze, 1.0 - exp(-dist * uHazeK)); if (uMask > 0.5) gl_FragColor = vec4(s2lf(vec3(200.0, 170.0, 90.0) / 255.0), 1.0);').replace('void main() {', 'vec3 s2lf(vec3 c){ return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }\nvoid main() {');
    s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWf;').replace('#include <begin_vertex>', '#include <begin_vertex>\n vWf = (modelMatrix * vec4(transformed, 1.0)).xyz;'); };
  const sh = new THREE.Shape([new THREE.Vector2(-30000, -30000), new THREE.Vector2(30000, -30000), new THREE.Vector2(30000, 30000), new THREE.Vector2(-30000, 30000)]);
  const m5 = 5;   // lỗ = hộp địa hình (thu 5 m để khít mép)
  sh.holes.push(new THREE.Path([new THREE.Vector2(T.x0 + m5, -(T.z0 + m5)), new THREE.Vector2(T.x0 + m5, -(T.z0 + TD - m5)), new THREE.Vector2(T.x0 + TW - m5, -(T.z0 + TD - m5)), new THREE.Vector2(T.x0 + TW - m5, -(T.z0 + m5))]));
  const FAR = new THREE.Mesh(new THREE.ShapeGeometry(sh).rotateX(-Math.PI / 2), fm); FAR.position.set(0, 6.0, 0);   // đất xa ngoài hộp (bậc 5: chỉ để chân trời là đất)
  FAR.renderOrder = -0.5; scene.add(FAR);
  // trời
  const sm = new THREE.ShaderMaterial({ uniforms: U, side: THREE.BackSide, depthWrite: false, vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 p = projectionMatrix * viewMatrix * vec4(position + cameraPosition, 1.0); gl_Position = p.xyww; }`,
    fragmentShader: `varying vec3 vD; uniform vec3 uSky, uHaze, uSunDir, uSunCol; uniform float uNight, uFireK, uT, uMask; ${GLSL_N}
      void main(){ vec3 d = normalize(vD); float h = max(d.y, 0.0);
        vec3 c = mix(uHaze, uSky, pow(h, 0.55));
        float sd = max(dot(d, uSunDir), 0.0); c += uSunCol * (pow(sd, 900.0) * 30.0 + pow(sd, 12.0) * 0.25) * step(-0.02, uSunDir.y);
        float cl = smoothstep(0.55, 0.85, fbm(d.xz / max(d.y, 0.08) * 1.4 + uT * 0.002)) * smoothstep(0.02, 0.2, d.y);
        c = mix(c, mix(vec3(0.92), vec3(0.08, 0.09, 0.12), uNight) , cl * 0.55);
        c += vec3(1.0, 0.35, 0.08) * uFireK * 0.30 * exp(-h * 9.0) * smoothstep(-0.2, 0.1, d.z * -1.0 + 0.2);   // trời "màu lửa" (Evelyn b41) phía thành
        gl_FragColor = vec4(c, 1.0); if (uMask > 0.5) gl_FragColor = vec4(vec3(40.0, 80.0, 200.0) / 255.0, 1.0); }` });   // 'troi'
  SKY = new THREE.Mesh(new THREE.SphereGeometry(5000, 32, 16), sm); SKY.frustumCulled = false; SKY.renderOrder = -1; scene.add(SKY);
  // đèn
  LG.hemi = new THREE.HemisphereLight(0xbfd2ee, 0x5a4a3a, 0.8); scene.add(LG.hemi);
  LG.sun = new THREE.DirectionalLight(0xffffff, 2.2); LG.sun.castShadow = true; LG.sun.shadow.mapSize.set(4096, 4096); LG.sun.shadow.bias = -0.0004; LG.sun.shadow.normalBias = 0.6;
  scene.add(LG.sun); scene.add(LG.sun.target);
  // bản đồ ánh lửa 20 m (từ lưới thời gian cháy — CPU mỗi khung)
  const LC = META.luoi_chay; FMAP = { nx: LC.nx, nz: LC.nz, t: new Float32Array(await (await fetch(base + 'luoi_chay.f32')).arrayBuffer()) };
  FTEX = new THREE.DataTexture(new Float32Array(LC.nx * LC.nz * 4), LC.nx, LC.nz, THREE.RGBAFormat, THREE.FloatType); FTEX.magFilter = FTEX.minFilter = THREE.LinearFilter; FTEX.needsUpdate = true;
  U.uFire.value = FTEX; U.uFireBox.value.set(LC.E0 - 532000 - 10, -(LC.N0 - 180800) - 10, LC.nx * LC.buoc, LC.nz * LC.buoc);
  const TL = new THREE.TextureLoader(); const ld = (u) => new Promise((r) => TL.load(u, (t) => { t.colorSpace = THREE.NoColorSpace; t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter; t.generateMipmaps = false; r(t); }, undefined, () => r(null)));
  U.uAtF = { value: await ld(base + 'fb/lua.png') }; U.uAtS = { value: await ld(base + 'fb/khoi.png') }; U.uAtlas = { value: (U.uAtF.value && CFG.fx !== 'thu_tuc') ? 1 : 0 };
  buildParticles(LC);
}
function blur1(src, nx, nz, r) { const o = new Float32Array(nx * nz), t = new Float32Array(nx * nz);
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { let s = 0, w = 0; for (let k = -r; k <= r; k++) { const ii = i + k; if (ii < 0 || ii >= nx) continue; s += src[j * nx + ii]; w++; } t[j * nx + i] = s / w; }
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { let s = 0, w = 0; for (let k = -r; k <= r; k++) { const jj = j + k; if (jj < 0 || jj >= nz) continue; s += t[jj * nx + i]; w++; } o[j * nx + i] = s / w; }
  return o; }
function burnIJS(ign, h) { if (ign < 0 || h < ign) return 0; const a = h - ign, ss = (e0, e1, x) => { const t = Math.min(1, Math.max(0, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t); };
  return ss(0, 0.7, a) * (1 - ss(4, 9, a)) + (a >= 9 ? 0.025 * (1 - ss(9, 48, a)) : 0); }
function updateFire(h) {
  const { nx, nz, t } = FMAP, I = new Float32Array(nx * nz);
  if (h >= 0) for (let v = 0; v < nx * nz; v++) I[v] = burnIJS(t[v], h);
  const a = blur1(I, nx, nz, 1), b = blur1(I, nx, nz, 4), c = blur1(I, nx, nz, 12), d = FTEX.image.data;
  for (let v = 0; v < nx * nz; v++) { d[v * 4] = a[v]; d[v * 4 + 1] = b[v] * 3; d[v * 4 + 2] = c[v] * 8; d[v * 4 + 3] = 1; }
  FTEX.needsUpdate = true; let s = 0; for (let v = 0; v < nx * nz; v++) s += I[v]; return s;
}
// ---------------------------------------------------------------- hạt lửa + khói (billboard instanced, tất định theo giờ)
function buildParticles(LC) {
  const { nx, nz, t } = FMAP; const cells = [];
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const ig = t[j * nx + i]; if (ig < 0) continue; const x = LC.E0 - 532000 + i * LC.buoc, z = -(LC.N0 - 180800) + j * LC.buoc; cells.push([x, z, ig]); }
  const mk = (perCell, kind) => { const n = cells.length * perCell, off = new Float32Array(n * 4), sd = new Float32Array(n * 2); let q = 0;
    for (const [x, z, ig] of cells) for (let k = 0; k < perCell; k++) { const r1 = frac(Math.sin((x * 12.9 + z * 78.2 + k * 37.1)) * 43758.5), r2 = frac(Math.sin((x * 3.7 + z * 11.3 + k * 91.7)) * 24634.6);
      off[q * 4] = x + (r1 - 0.5) * 18; off[q * 4 + 1] = groundAt(x, z); off[q * 4 + 2] = z + (r2 - 0.5) * 18; off[q * 4 + 3] = ig + r1 * 0.6; sd[q * 2] = r1; sd[q * 2 + 1] = r2; q++; }
    const g = new THREE.InstancedBufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([-0.5, 0, 0, 0.5, 0, 0, 0.5, 1, 0, -0.5, 1, 0]), 3)); g.setIndex([0, 1, 2, 0, 2, 3]);
    g.setAttribute('off', new THREE.InstancedBufferAttribute(off, 4)); g.setAttribute('sd', new THREE.InstancedBufferAttribute(sd, 2)); g.instanceCount = n; return g; };
  const VS = (kind) => `attribute vec4 off; attribute vec2 sd; uniform float uHour, uT, uAtlas; uniform vec3 uCam; varying vec2 vUv; varying float vA; varying float vH; varying float vSeed; ${burnI}
    void main(){ vUv = position.xy + vec2(0.5, 0.0); float I = burnI(off.w, uHour); vSeed = sd.x;
      ${kind === 'flame' ? `float life = 2.5 + sd.y * 2.0; float age = mod(uT + sd.x * 17.0, life) / life; float size = (4.0 + sd.y * 7.0) * smoothstep(0.15, 0.6, I) * (1.0 - 0.5 * age);
        vec3 c = off.xyz + vec3(-age * 6.0, 6.0 + age * 14.0 * (0.5 + sd.y), 0.0); vA = smoothstep(0.15, 0.6, I) * (1.0 - age) * 0.55;`
        : `float life = 40.0 + sd.y * 50.0; float age = mod(uT * 0.9 + sd.x * 97.0, life) / life; float I2 = max(I, 0.0);
        float size = (25.0 + age * 160.0 * (0.6 + sd.y)) * smoothstep(0.0, 0.08, I2);
        vec3 c = off.xyz + vec3(-age * 520.0 * (0.7 + sd.x * 0.6), 18.0 + age * (240.0 + sd.y * 260.0), (sd.y - 0.5) * age * 120.0);   // gió đông → khói sang tây (b39)
        vA = smoothstep(0.0, 0.08, I2) * (1.0 - age) * smoothstep(0.0, 0.05, age) * (0.35 + 0.65 * min(I2 * 3.0, 1.0));`}
      vH = clamp(age, 0.0, 1.0);
      vec3 toC = normalize(uCam - c); vec3 rt = normalize(cross(vec3(0.0, 1.0, 0.0), toC)); vec3 up = ${kind === 'flame' ? 'vec3(0.0, 1.0, 0.0)' : 'normalize(cross(toC, rt))'};
      float ar = uAtlas > 0.5 ? 2.0 : ${kind === 'flame' ? '1.6' : '1.0'}; float sz = uAtlas > 0.5 ? size * ${kind === 'flame' ? '0.75' : '0.8'} : size;
      float dcam = length(uCam - c); ${kind === 'flame' ? '' : 'vA *= smoothstep(60.0, 220.0, dcam);'}
      vec3 w = c + rt * position.x * sz + up * (position.y - ${kind === 'flame' ? '0.1' : '0.5'}) * sz * ar;
      if (size < 0.01) w = vec3(0.0, -1000.0, 0.0);
      gl_Position = projectionMatrix * viewMatrix * vec4(w, 1.0); }`;
  const ATL = `uniform sampler2D uAtF, uAtS; uniform float uAtlas; vec2 atl(vec2 uv, float age, float seed){ float idx = mod(floor(age * 63.0) + floor(seed * 64.0), 64.0); float c = mod(idx, 8.0), r = floor(idx / 8.0);
      return vec2((c + clamp(uv.x, 0.0, 1.0)) / 8.0, 1.0 - (r + 1.0 - clamp(uv.y, 0.0, 1.0)) / 8.0); }`;
  const FS_FLAME = `varying vec2 vUv; varying float vA; varying float vH; varying float vSeed; uniform float uT, uNight; ${GLSL_N} ${ATL}
    void main(){ if (uAtlas > 0.5) { vec3 t = texture2D(uAtF, atl(vUv, fract(uT * 0.35 + vSeed), vSeed)).rgb; vec3 o = t * t * vec3(1.0, 0.62, 0.32); gl_FragColor = vec4(o * vA * (0.55 + 1.0 * uNight) * 1.6, 0.0); return; }
      vec2 p = vUv - vec2(0.5, 0.0); float n = fbm(vec2(p.x * 3.0 + vSeed * 9.0, vUv.y * 2.2 - uT * 2.6));
      float sh = smoothstep(0.5, 0.0, abs(p.x) * (1.0 + vUv.y * 1.8) + (vUv.y - 0.25) * 0.45 - n * 0.35) * smoothstep(1.0, 0.25, vUv.y);
      vec3 c = mix(vec3(1.0, 0.85, 0.45), vec3(1.0, 0.32, 0.05), smoothstep(0.1, 0.8, vUv.y + n * 0.3));
      gl_FragColor = vec4(c * sh * vA * 1.4 * (0.35 + 0.65 * uNight), 0.0); }`;
  const FS_SMOKE = `varying vec2 vUv; varying float vA; varying float vH; varying float vSeed; uniform float uT, uNight, uFireK; uniform vec3 uSunCol, uSky; ${GLSL_N} ${ATL}
    void main(){ if (uAtlas > 0.5) { vec3 t = texture2D(uAtS, atl(vUv, vH, vSeed)).rgb; float d = t.r * vA * 0.55 * smoothstep(0.0, 0.08, vUv.y) * smoothstep(1.0, 0.6, vUv.y) * smoothstep(0.0, 0.18, min(vUv.x, 1.0 - vUv.x));
        vec3 day = mix(vec3(0.10, 0.09, 0.085), vec3(0.58, 0.55, 0.52) * (0.55 + 0.45 * uSunCol), t.g);
        vec3 night = vec3(0.018, 0.016, 0.016) + vec3(0.95, 0.36, 0.09) * t.b * (1.0 - vH) * (1.0 - vH) * 0.6;
        gl_FragColor = vec4(mix(day, night, uNight) * d, d); return; } vec2 p = vUv - 0.5; float r = length(p); float n = fbm(p * 3.2 + vec2(vSeed * 13.0, uT * 0.03 + vSeed));
      float d = smoothstep(0.5, 0.05, r + (n - 0.5) * 0.45) * vA * 0.45;
      vec3 day = mix(vec3(0.16, 0.14, 0.13), vec3(0.50, 0.47, 0.44) * (0.6 + 0.4 * uSunCol), smoothstep(0.35, 0.95, n + vUv.y * 0.35));
      vec3 night = mix(vec3(0.75, 0.28, 0.07) * (1.0 - vH) * (1.0 - vH), vec3(0.025, 0.022, 0.022), clamp(smoothstep(0.0, 0.45, vH) + vUv.y * 0.25, 0.0, 1.0));
      vec3 c = mix(day, night, uNight);
      gl_FragColor = vec4(c * d, d); }`;
  FIRE = new THREE.Mesh(mk(2, 'flame'), new THREE.ShaderMaterial({ uniforms: U, vertexShader: VS('flame'), fragmentShader: FS_FLAME, transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor }));
  SMOKE = new THREE.Mesh(mk(3, 'smoke'), new THREE.ShaderMaterial({ uniforms: U, vertexShader: VS('smoke'), fragmentShader: FS_SMOKE, transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor }));
  FIRE.frustumCulled = SMOKE.frustumCulled = false; SMOKE.renderOrder = 2; FIRE.renderOrder = 3; scene.add(SMOKE); scene.add(FIRE);
}
const frac = (x) => x - Math.floor(x);
function groundAt(x, z) { const T = META.dia_hinh; const i = Math.round((x - T.x0) / T.step), j = Math.round((z - T.z0) / T.step); if (i < 0 || j < 0 || i >= T.nx || j >= T.nz) return 5;
  const l = META.bo_cuc.h66; return new Float32Array(BUFREF, l.off + 4 * (j * T.nx + i), 1)[0]; }
let BUFREF = null;

// ---------------------------------------------------------------- ánh sáng theo thời điểm
function setTime(year, hour, opt = {}) {
  U.uYear.value = year; U.uHour.value = hour; let jd;
  if (hour >= 0) jd = jdJulian(1666, 9, 2, hour - LON.lon / 15);   // giờ địa phương 1666 (LMT)
  else { const y = Math.floor(year), d = (year - y) * 365; jd = jdOf(y, 1, 1, 0) + d + (opt.hod != null ? opt.hod / 24 - LON.lon / 15 / 24 - (d % 1) : 0); }
  const sp = sunPos(jd, LON.lat, LON.lon); const el = sp.el * Math.PI / 180, az = sp.az * Math.PI / 180;
  const sd = new THREE.Vector3(Math.sin(az) * Math.cos(el), Math.sin(el), -Math.cos(az) * Math.cos(el)); U.uSunDir.value.copy(sd);
  const day = THREE.MathUtils.smoothstep(sp.el, -8, 6), night = 1 - day; U.uNight.value = night;
  const warm = THREE.MathUtils.smoothstep(sp.el, 0, 25);
  U.uSunCol.value.setRGB(1.0, 0.72 + 0.26 * warm, 0.45 + 0.5 * warm);
  U.uSky.value.setRGB(0.30 * day + 0.006, 0.46 * day + 0.009, 0.80 * day + 0.022); U.uHaze.value.setRGB(0.62 * day + 0.012, 0.66 * day + 0.014, 0.72 * day + 0.024);
  if (opt.smokeSky && hour >= 0) { const k = opt.smokeSky; U.uSky.value.lerp(new THREE.Color(0.55, 0.45, 0.36), k * day); U.uHaze.value.lerp(new THREE.Color(0.62, 0.52, 0.42), k * day); }
  LG.sun.intensity = 3.0 * day + 0.30 * night;   // trăng sáng (Pepys b38: 'moon: shine') LG.sun.color.copy(U.uSunCol.value); if (night > 0.5) LG.sun.color.setRGB(0.55, 0.65, 0.9);   // trăng (b38: đêm 2/9 sáng trăng)
  const dir = night > 0.5 ? new THREE.Vector3(-0.3, 0.6, 0.5).normalize() : sd; LG.sun.position.copy(dir).multiplyScalar(3000); LG.hemi.intensity = 0.55 * day + 0.12 * night;
  LG.hemi.color.setRGB(0.75 * day + 0.2 * night, 0.82 * day + 0.25 * night, 0.93 * day + 0.4 * night);
  U.uWin.value = hour < 0 && year > 1950 ? night : 0;
  const f = updateFire(hour); U.uFireK.value = hour >= 0 ? (0.5 + 1.2 * night) : 0;
  return { el: sp.el, az: sp.az, fireSum: f };
}
function setCam(c) {
  const P = (e) => new THREE.Vector3(e[0] - 532000, e[2], -(e[1] - 180800));
  cam.fov = c.fov; cam.aspect = CFG.W / CFG.H; cam.near = 2; cam.far = 12000; cam.updateProjectionMatrix();
  cam.position.copy(P(c.p)); cam.lookAt(P(c.l)); cam.updateMatrixWorld(); U.uCam.value.copy(cam.position);
  const tgt = P(c.l); LG.sun.target.position.copy(tgt); LG.sun.position.add(tgt);
  const span = Math.min(2600, Math.max(700, cam.position.distanceTo(tgt) * 1.6)); const sc = LG.sun.shadow.camera; sc.left = sc.bottom = -span; sc.right = sc.top = span; sc.near = 10; sc.far = 7000; sc.updateProjectionMatrix();
}
window.setup = async (cfg) => {
  CFG = cfg; R = createRenderer(cfg.W, cfg.H); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  document.body.appendChild(R.domElement); scene = new THREE.Scene(); cam = new THREE.PerspectiveCamera(40, cfg.W / cfg.H, 2, 12000);
  BUFREF = await (await fetch(cfg.data + 'ldn.bin')).arrayBuffer();
  await build(cfg);
  pipe = createPipeline(R, cfg.W, cfg.H, { exposure: cfg.exposure || 0.85, gradeGLSL: `vec3 grade(vec3 c, vec2 uv){ vec2 d = (uv - 0.5) * vec2(1.0, 0.82); return c * mix(1.0, 0.86, smoothstep(0.3, 0.8, length(d))); }` });
  const e = R.getContext().getExtension('WEBGL_debug_renderer_info');
  return { renderer: e ? R.getContext().getParameter(e.UNMASKED_RENDERER_WEBGL) : 'unknown', tris: META.tam_giac };
};
// f: {cam:{p,l,fov}, year, hour, t (giây phim), spp, smokeSky, hod, layers:{fire,smoke}}
window.renderFrame = async (f) => {
  const t0 = performance.now(); setCam(f.cam); const L = setTime(f.year, f.hour ?? -1, f); U.uT.value = f.t || 0;
  FIRE.visible = (f.hour ?? -1) >= 0 && f.fire !== false; SMOKE.visible = (f.hour ?? -1) >= 0 && f.smoke !== false;
  if (f.mask) {   // mặt nạ ID theo bảng màu scripts/k2ldn/ai/n2p_lib.py: 'nha' = lớp (a) nhà/công trình/cầu/tường; 'bang' = đất; 'nuoc' = nước; 'troi' = trời (vật chuyển động: không có trong mặt nạ)
    U.uMask.value = 1; FIRE.visible = SMOKE.visible = false; R.setRenderTarget(null); R.render(scene, cam); U.uMask.value = 0;
    const gl = R.getContext(), W = CFG.W, H = CFG.H, px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const rgb = new Uint8Array(W * H * 3); for (let i = 0, j = 0; i < px.length; i += 4, j += 3) { rgb[j] = px[i]; rgb[j + 1] = px[i + 1]; rgb[j + 2] = px[i + 2]; }
    let bin = ''; for (let i = 0; i < rgb.length; i += 0x8000) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + 0x8000));
    return { img: btoa(bin), ms: performance.now() - t0, sun_el: L.el, fire: L.fireSum, view: cam.matrixWorldInverse.elements.slice(), proj: cam.projectionMatrix.elements.slice(), mask: true };
  }
  const spp = f.spp || 4;
  pipe.accumulate(scene, cam, spp);
  const img = pipe.finalize(f.n || 0);
  const view = cam.matrixWorldInverse.elements.slice(), projE = cam.projectionMatrix.elements.slice();
  return { img, ms: performance.now() - t0, sun_el: L.el, fire: L.fireSum, view, proj: projE };
};
window.ready = true;

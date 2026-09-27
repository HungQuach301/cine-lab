// Cine Lab · Cổng 3 vòng 1 · HƯỚNG B — "Ink & Lamplight" (đồ hoạ mực, sáng tối phân tầng).
// Trang cho shared/render_still.js: khung 's1_opening' và 's5_shadows'.
// Kỹ thuật: vật liệu tô phẳng lượng tử hoá theo log-độ rọi (tầng sáng ngả ấm, tầng tối ngả lạnh) gắn vào vòng lặp đèn của
// three.js (MeshLambertMaterial + onBeforeCompile) nên bóng đổ, suy giảm khoảng cách đều bị lượng tử hoá thành mảng;
// viền mực: G-buffer riêng (pháp tuyến + độ sâu + mã vật liệu) → Sobel/Laplace nhiều hướng, độ dày theo khoảng cách,
// run tay bằng nhiễu tần thấp, tích luỹ theo jitter dưới điểm ảnh; giấy + chấm lưới vùng tối trong gradeGLSL.
// Grain/dither của shared/post.js giữ nguyên.
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { buildCharacter, buildLantern, buildLadder } from '../shared/cast.js';
import { createPipeline, createRenderer } from '../shared/post.js';

// ---------------------------------------------------------------- bảng màu (sRGB hex) ----------------------------------------------
export const PAL = {
  ink: '#161a2b',        // mực chàm đen: viền, vạch mặt đồng hồ
  night0: '#1b2242',     // chàm đêm sâu (thiên đỉnh, bóng sâu)
  night1: '#2e3868',     // chàm
  violet: '#6c5e9e',     // tím chạng vạng
  mauve: '#b27f9e',      // tím hồng tầng giữa trời
  rose: '#eaa697',       // hồng chân trời
  bone: '#efe6d2',       // trắng xương: vôi
  boneCold: '#e4e9ee',   // trắng lạnh: ánh điện
  amberCore: '#ffe3a4',  // lõi lửa
  amber: '#f4a64a',      // hổ phách
  amberDeep: '#b8622a',  // hổ phách sẫm
  brick: '#a2412f',      // nhấn 1: đỏ gạch (áo len Cas)
  moss: '#58663c',       // nhấn 2: xanh rêu (áo khoác Ida)
};
const C = (hex) => new THREE.Color(hex); // sRGB hex → tuyến tính (ColorManagement bật mặc định)
const V3 = (c) => new THREE.Vector3(c.r, c.g, c.b);
function rng(seed) { let s = seed >>> 0; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }

// ---------------------------------------------------------------- uniform chung cho mọi vật liệu tô phẳng -------------------------
const G = {
  uStep: { value: 1.0 }, uOff: { value: 0.0 }, uQlo: { value: -4 }, uQhi: { value: 1 },
  uCool: { value: new THREE.Vector3(0.80, 0.88, 1.16) }, uWarm: { value: new THREE.Vector3(1.10, 1.0, 0.84) },
  uInk: { value: V3(C(PAL.ink)) },
  uElec: { value: new THREE.Vector4(0, 0, 0, 0) },       // rgb·I, w=bật
  uBay: { value: new THREE.Vector4(1.6, 4.0, 0.92, 0) },   // nửa rộng hốc, z miệng, hệ số tắt, w=có hốc
  uBounce: { value: new THREE.Vector4(0, 0, 0, 0) },
  uLanternPos: { value: new THREE.Vector3() }, uLantAng: { value: new THREE.Vector4(0, 0.7, 0, 0.3) },
  uFog: { value: new THREE.Vector4(0, 0, 1, 0) },          // mật độ, bắt đầu, nhân màu
  uSkyA: { value: V3(C(PAL.rose)) }, uSkyB: { value: V3(C(PAL.mauve)) }, uSkyC: { value: V3(C(PAL.violet)) }, uSkyD: { value: V3(C(PAL.night1)) },
  uSunDir: { value: new THREE.Vector3(0.3, 0.02, -1).normalize() },
};

const NOISE_GLSL = /* glsl */`
float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.0-2.0*f);
  return mix(mix(h21(i),h21(i+vec2(1.0,0.0)),f.x), mix(h21(i+vec2(0.0,1.0)),h21(i+vec2(1.0,1.0)),f.x), f.y); }
float fbm(vec2 p){ float s=0.0, a=0.5; for(int i=0;i<3;i++){ s+=a*vn(p); p=p*2.03+17.1; a*=0.5; } return s*1.14; }
`;
const SKY_GLSL = /* glsl */`
vec3 skyCol(vec3 d){
  float e = d.y;
  vec2 hz = normalize(d.xz + vec2(1e-5)); float az = dot(hz, normalize(uSunDir.xz)); float gl = pow(max(az,0.0), 3.0);
  float e1 = 0.035 + 0.05*gl;
  vec3 c = mix(uSkyA, uSkyB, smoothstep(-0.03, e1 + 0.04, e));
  c = mix(c, uSkyC, smoothstep(e1, 0.26, e));
  c = mix(c, uSkyD, smoothstep(0.20, 0.62, e));
  c *= 1.0 + 0.55*gl*(1.0 - smoothstep(-0.02, 0.22, e));
  return c;
}`;

// Đường kẻ khử răng cưa theo toạ độ thế giới (mạch gạch, mạch đá): tắt dần khi mạch nhỏ hơn ~3 px.
const FRAG_LIB = /* glsl */`
varying vec3 vWP; varying vec4 vFogC;
#ifdef USE_ACOL
varying vec3 vCol;
#endif
uniform vec3 uAlb;
uniform float uStep, uOff, uQlo, uQhi;
uniform vec3 uCool, uWarm, uInk, uLanternPos;
uniform vec4 uElec, uBay, uBounce, uFog, uLantAng; uniform vec3 uHs, uHg, uDc, uDd, uLampC; uniform vec4 uLampP[4];
uniform vec3 uSkyA, uSkyB, uSkyC, uSkyD, uSunDir;
${NOISE_GLSL}
${SKY_GLSL}
float gl1(float x, float sp, float hw){ float fw = fwidth(x); float d = abs(fract(x/sp + 0.5) - 0.5)*sp;
  return (1.0 - smoothstep(hw, hw + fw*1.2, d)) * (1.0 - smoothstep(0.12, 0.35, fw/sp)); }
float archD(vec2 p){ // khoảng cách có dấu tới đường bao vòm nhọn (âm = trong lỗ)
  vec2 q = vec2(abs(p.x), p.y);
  if (q.y < 2.2) return q.x - 1.6;
  return length(q - vec2(-0.2125, 2.2)) - 1.8125; }
`;

const FRAG_OUT = /* glsl */`
vec3 nW = inverseTransformDirection(normal, viewMatrix);
vec3 E = (reflectedLight.directDiffuse + reflectedLight.indirectDiffuse) * PI;
if (uLantAng.x > 0.5) { // phân bố sáng của đèn lồng: nắp thiếc chắn tia hướng lên, đế chắn tia thẳng xuống
  vec3 ld = normalize(vWP - uLanternPos);
  E *= mix(uLantAng.w, 1.0, 1.0 - smoothstep(uLantAng.y - 0.06, uLantAng.y + 0.06, ld.y)) * mix(0.25, 1.0, smoothstep(-0.93, -0.80, ld.y)); }
{ // trời + dư quang + đèn khí phố (giải tích, rẻ hơn vòng đèn của three.js trên SwiftShader)
  E += mix(uHg, uHs, 0.5*nW.y + 0.5) + uDc*max(dot(nW, uDd), 0.0);
  for (int i = 0; i < 4; i++) { vec3 lv = uLampP[i].xyz - vWP; float d2 = max(dot(lv, lv), 0.01);
    E += uLampC * (uLampP[i].w * max(dot(nW, lv*inversesqrt(d2)), 0.0) / d2 * (1.0 - smoothstep(900.0, 1700.0, d2))); } }
if (uElec.w > 0.5) { // ánh điện tràn: phẳng, gần như không hướng; bị che trong hốc cửa
  float sh = 1.0;
  if (uBay.w > 0.5 && vWP.z < uBay.y - 0.02 && abs(vWP.x) < uBay.x + 0.05) sh = exp(-(uBay.y - vWP.z)*uBay.z) * (0.55 + 0.45*max(nW.z, 0.0));
  E += uElec.rgb * (0.76 + 0.24*nW.y) * sh; }
if (uBounce.w > 0.5) { float d = distance(vWP, uLanternPos); float inb = 1.0 - smoothstep(uBay.y - 0.2, uBay.y + 0.6, vWP.z);
  E += uBounce.rgb * inb / (1.0 + d*d*0.5); }
vec3 alb = uAlb;
#ifdef USE_ACOL
alb *= vCol;
#endif
float inkP = 0.0;
#if PAT == 1
{ // gạch quét vôi (mặt tiền nhà kho) + vành đá vòm + đá góc
  vec2 uv = abs(nW.x) > abs(nW.z) ? vec2(vWP.z, vWP.y) : vec2(vWP.x, vWP.y);
  float h = 0.077; float row = floor(uv.y/h);
  float lines = max(gl1(uv.y, h, 0.004), gl1(uv.x + mod(row, 2.0)*0.115, 0.23, 0.004)*0.85);
  float wash = smoothstep(0.40, 0.80, vn(uv*vec2(0.9, 1.4) + 3.0)*0.65 + vn(uv*3.7)*0.35);
  inkP = lines * (0.10 + 0.42*wash);
  alb *= 0.975 + 0.04*vn(uv*3.1) - 0.05*wash;
  if (uBay.w > 0.5 && nW.z > 0.5) {
    float ad = archD(vWP.xy);
    if (ad > -0.01 && ad < 0.46 && vWP.y > 2.2) {
      float ang = atan(vWP.y - 2.2, vWP.x); float seg = 3.14159/19.0;
      float jl = gl1(ang, seg, 0.004);
      inkP = max(jl * 0.75, gl1(ad - 0.46, 10.0, 0.006)*0.8); alb = vec3(0.80, 0.77, 0.70) * (0.95 + 0.08*h21(vec2(floor(ang/seg), 3.0)));
    } else if (ad > -0.01 && ad < 0.46 && vWP.y < 2.2 && vWP.y > 0.55) {
      float r = floor((vWP.y - 0.55)/0.33); float wq = mod(r, 2.0) < 0.5 ? 0.46 : 0.30;
      if (ad < wq) { inkP = max(gl1(vWP.y - 0.55, 0.33, 0.005)*0.75, gl1(ad - wq, 10.0, 0.006)*0.8); alb = vec3(0.80, 0.77, 0.70) * (0.95 + 0.08*h21(vec2(r, sign(vWP.x))));} } } }
#elif PAT == 2
{ // vữa vôi trát (vách trong): loang nhẹ + vết nứt mảnh
  vec2 uv = abs(nW.x) > 0.5 ? vWP.zy : (abs(nW.y) > 0.5 ? vWP.xz : vWP.xy);
  alb *= 0.93 + 0.10*vn(uv*1.7 + 9.0);
  float cr = abs(vn(uv*2.2 + 4.0) - 0.5); float fwc = fwidth(cr);
  inkP = (1.0 - smoothstep(0.004, 0.004 + fwc*1.5, cr)) * smoothstep(0.62, 0.78, vn(uv*0.8 + 1.0)) * 0.45; }
#elif PAT == 3
{ // đá lát hốc cửa
  vec2 uv = vWP.xz; float row = floor(uv.y/0.62); float off = h21(vec2(row, 1.3))*0.8;
  float lines = max(gl1(uv.y, 0.62, 0.008), gl1(uv.x + off, 0.78, 0.008));
  inkP = lines*0.55; alb *= 0.90 + 0.16*h21(vec2(floor((uv.x+off)/0.78), row)) + 0.06*vn(uv*4.0); }
#elif PAT == 4
{ // đá hộc lát phố (sett)
  vec2 uv = vWP.xz; float row = floor(uv.y/0.17); float off = mod(row, 2.0)*0.13;
  float lines = max(gl1(uv.y, 0.17, 0.012), gl1(uv.x + off, 0.26, 0.012));
  inkP = lines*0.42; alb *= 0.90 + 0.14*h21(vec2(floor((uv.x+off)/0.26), row)); }
#elif PAT == 5
{ // ngói/đá phiến mái: hàng ngang
  inkP = gl1(vWP.y, 0.24, 0.012)*0.35; alb *= 0.94 + 0.1*vn(vWP.xz*0.7); }
#endif
float L = dot(E, vec3(0.2126, 0.7152, 0.0722));
vec3 hue = E / max(L, 1e-6);
float qx = log2(max(L, 1e-6)) / uStep + uOff;
float fi = floor(qx); float ff = qx - fi;
float qw = clamp(fwidth(qx)*0.7, 0.03, 0.5);
float q = fi + smoothstep(1.0 - qw, 1.0, ff);
float Lq = min(exp2((q + 0.5 - uOff) * uStep), uLantAng.z > 0.0 ? uLantAng.z : 1e9);
float tt = clamp((q - uQlo) / (uQhi - uQlo), 0.0, 1.0);
vec3 col = alb * mix(uCool, uWarm, tt) * hue * Lq;
col = mix(col, col*0.30 + uInk*0.02, clamp(inkP, 0.0, 1.0));
col = mix(col, vFogC.rgb, vFogC.a);
vec3 outgoingLight = col + totalEmissiveRadiance;
`;

let MAT_ID = 1;
function toon(hex, o = {}) {
  const m = new THREE.MeshLambertMaterial({ color: 0xffffff, side: o.side ?? THREE.FrontSide });
  const pat = o.pat ?? 0;
  m.userData = { toon: true, id: o.id ?? MAT_ID++ };
  m.defines = { PAT: pat };
  if (o.vcol) m.defines.USE_ACOL = '';
  for (const k of ['NOFOG', 'NOPAT']) if (DBG[k]) m.defines[k] = '';
  if (DBG.NOPAT) m.defines.PAT = 0;
  const alb = C(hex);
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uAlb = { value: alb };
    for (const k of Object.keys(G)) sh.uniforms[k] = G[k];
    for (const k of Object.keys(FAR)) sh.uniforms[k] = FAR[k];
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWP; varying vec4 vFogC; uniform vec4 uFog; uniform vec3 uSkyA, uSkyB, uSkyC, uSkyD, uSunDir;\n' + SKY_GLSL + '\n#ifdef USE_ACOL\nattribute vec3 aCol; varying vec3 vCol;\n#endif')
      .replace('#include <project_vertex>', '#include <project_vertex>\nvWP = (modelMatrix*vec4(transformed,1.0)).xyz;\n{ vec3 vd = vWP - cameraPosition; float dd = length(vd); float fa = uFog.x > 0.0 ? 1.0 - exp(-max(dd - uFog.y, 0.0)*uFog.x) : 0.0; vFogC = vec4(mix(mix(skyCol(vd/dd), uSkyC, 0.86)*uFog.z, skyCol(vd/dd), smoothstep(700.0, 2600.0, dd)), fa); }\n#ifdef USE_ACOL\nvCol = aCol;\n#endif');
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\n' + FRAG_LIB)
      .replace('vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;', FRAG_OUT);
  };
  m.customProgramCacheKey = () => 'inkB|' + pat + (o.vcol ? 'v' : '') + JSON.stringify(m.defines);
  return m;
}
// Vật liệu tô phẳng rút gọn cho phố xa (cảnh 1): trời + dư quang tính giải tích, sương tính theo đỉnh — rẻ hơn nhiều
// cho hàng vạn tam giác nhỏ (SwiftShader tô theo khối 2×2 nên tam giác bé rất đắt với shader dài).
const FAR = { uHs: { value: new THREE.Vector3() }, uHg: { value: new THREE.Vector3() }, uDc: { value: new THREE.Vector3() }, uDd: { value: new THREE.Vector3(0, 1, 0) },
  uLampP: { value: [new THREE.Vector4(), new THREE.Vector4(), new THREE.Vector4(), new THREE.Vector4()] }, uLampC: { value: new THREE.Vector3() } };
function farToon(o = {}) {
  const u = { uAlb: { value: C(o.hex ?? '#ffffff') } }; for (const k of Object.keys(G)) u[k] = G[k]; for (const k of Object.keys(FAR)) u[k] = FAR[k];
  const m = new THREE.ShaderMaterial({ uniforms: u,
    vertexShader: `attribute vec3 aCol; varying vec3 vCol; varying vec3 vN; varying vec4 vFog;
      uniform vec4 uFog; uniform vec3 uSkyA, uSkyB, uSkyC, uSkyD, uSunDir;
      ${SKY_GLSL}
      void main(){ vec4 wp = modelMatrix*vec4(position, 1.0); vN = normalize(mat3(modelMatrix)*normal); vCol = aCol;
        vec3 vd = wp.xyz - cameraPosition; float dd = length(vd); float fa = 1.0 - exp(-max(dd - uFog.y, 0.0)*uFog.x);
        vFog = vec4(mix(mix(skyCol(vd/dd), uSkyC, 0.86)*uFog.z, skyCol(vd/dd), smoothstep(700.0, 2600.0, dd)), fa);
#ifdef NOVS
vFog = vec4(0.0);
#endif
 gl_Position = projectionMatrix*viewMatrix*wp; }`,
    fragmentShader: `varying vec3 vCol; varying vec3 vN; varying vec4 vFog; uniform vec3 uAlb, uHs, uHg, uDc, uDd, uCool, uWarm; uniform float uStep, uOff, uQlo, uQhi;
      void main(){ vec3 n = normalize(vN); vec3 E = mix(uHg, uHs, 0.5*n.y + 0.5) + uDc*max(dot(n, uDd), 0.0);
        float L = dot(E, vec3(0.2126, 0.7152, 0.0722)); vec3 hue = E/max(L, 1e-6);
        float qx = log2(max(L, 1e-6))/uStep + uOff; float q = floor(qx); float Lq = exp2((q + 0.5 - uOff)*uStep);
        float tt = clamp((q - uQlo)/(uQhi - uQlo), 0.0, 1.0);
        vec3 col = uAlb*vCol*mix(uCool, uWarm, tt)*hue*Lq; gl_FragColor = vec4(mix(col, vFog.rgb, vFog.a), 1.0); }` });
  if (DBG.NOVS) m.defines = { NOVS: '' };
  if (DBG.NOFS) m.fragmentShader = 'varying vec3 vCol; void main(){ gl_FragColor = vec4(vCol, 1.0); }';
  m.userData = { toon: true, id: MAT_ID++ };
  return m;
}
// Vật phát sáng (lửa, kính đèn, cửa sổ sáng): không lượng tử hoá, giá trị > 1 cho vai tone.
function glow(hex, k, o = {}) {
  const c = C(hex).multiplyScalar(k);
  const m = new THREE.MeshBasicMaterial({ color: c, side: o.side ?? THREE.FrontSide });
  if (o.vcol) {
    m.onBeforeCompile = (sh) => {
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute vec3 aCol; varying vec3 vCol2;').replace('#include <project_vertex>', '#include <project_vertex>\nvCol2 = aCol;');
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vCol2;').replace('vec4 diffuseColor = vec4( diffuse, opacity );', 'vec4 diffuseColor = vec4( diffuse*vCol2, opacity );');
    };
    m.customProgramCacheKey = () => 'glowv';
  }
  m.userData = { glow: true, id: o.id ?? MAT_ID++ };
  return m;
}
// Quầng sáng quanh đèn: dải chuyển mượt (đi qua dither/grain của đường ống chung).
function haloMaterial(pull = 0) {
  return new THREE.ShaderMaterial({ uniforms: { uPull: { value: pull } },
    vertexShader: 'uniform float uPull; attribute vec3 aCol; varying vec3 vC; varying vec2 vU; void main(){ vC = aCol; vU = uv*2.0-1.0; vec4 mv = modelViewMatrix*vec4(position,1.0); mv.xyz -= normalize(mv.xyz)*uPull; gl_Position = projectionMatrix*mv; }',
    fragmentShader: 'varying vec3 vC; varying vec2 vU; void main(){ float r2 = dot(vU,vU); float a = exp(-r2*4.5)*0.45 + exp(-r2*28.0)*0.9; a *= 1.0 - smoothstep(0.75, 1.0, sqrt(r2)); gl_FragColor = vec4(vC*a, 1.0); }',
    blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, side: THREE.DoubleSide,
  });
}

// ---------------------------------------------------------------- gộp hình học ------------------------------------------------------
function bake(geo, mat4, hex, k = 1) {
  let g = geo.index ? geo.toNonIndexed() : geo.clone();
  if (mat4) g.applyMatrix4(mat4);
  const n = g.attributes.position.count, c = C(hex ?? '#ffffff').multiplyScalar(k), a = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { a[i * 3] = c.r; a[i * 3 + 1] = c.g; a[i * 3 + 2] = c.b; }
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', g.attributes.position); out.setAttribute('normal', g.attributes.normal);
  if (g.attributes.uv) out.setAttribute('uv', g.attributes.uv);
  out.setAttribute('aCol', new THREE.BufferAttribute(a, 3));
  return out;
}
function merge(list) {
  let n = 0; for (const g of list) n += g.attributes.position.count;
  const P = new Float32Array(n * 3), N = new Float32Array(n * 3), A = new Float32Array(n * 3), U = new Float32Array(n * 2);
  let o = 0;
  for (const g of list) {
    const c = g.attributes.position.count;
    P.set(g.attributes.position.array, o * 3); N.set(g.attributes.normal.array, o * 3); A.set(g.attributes.aCol.array, o * 3);
    if (g.attributes.uv) U.set(g.attributes.uv.array, o * 2);
    o += c;
  }
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(P, 3)); out.setAttribute('normal', new THREE.BufferAttribute(N, 3));
  out.setAttribute('aCol', new THREE.BufferAttribute(A, 3)); out.setAttribute('uv', new THREE.BufferAttribute(U, 2));
  return out;
}
class Batch {
  constructor() { this.lists = new Map(); }
  add(key, geo, m4, hex, k) { if (!this.lists.has(key)) this.lists.set(key, []); this.lists.get(key).push(bake(geo, m4, hex, k)); }
  build(scene, mats) {
    for (const [k, l] of this.lists) { const mesh = new THREE.Mesh(merge(l), mats[k]); mesh.receiveShadow = true; mesh.name = k; scene.add(mesh); }
  }
}
const M4 = () => new THREE.Matrix4();
const TRS = (x, y, z, ry = 0, sx = 1, sy = 1, sz = 1) => M4().compose(new THREE.Vector3(x, y, z), new THREE.Quaternion().setFromEuler(new THREE.Euler(0, ry, 0)), new THREE.Vector3(sx, sy, sz));

// Lăng trụ tam giác (mái): tiết diện 3 điểm trong mặt (a,b) đùn theo trục thứ ba.
function prism(p0, p1, p2, len, axis = 'x') {
  // p* = [u, y] ; đùn theo axis từ -len/2..len/2. axis 'x': u = z ; axis 'z': u = x
  const pts = [p0, p1, p2];
  const V = (u, y, t) => axis === 'x' ? [t, y, u] : [u, y, t];
  const pos = [];
  const tri = (a, b, c) => pos.push(...a, ...b, ...c);
  const h = len / 2;
  const A0 = V(...pts[0], -h), B0 = V(...pts[1], -h), C0 = V(...pts[2], -h), A1 = V(...pts[0], h), B1 = V(...pts[1], h), C1 = V(...pts[2], h);
  // hai mặt dốc (A-B, B-C) và mặt đáy (C-A) + hai đầu hồi
  const quad = (a, b, c, d) => { tri(a, b, c); tri(a, c, d); };
  quad(A0, A1, B1, B0); quad(B0, B1, C1, C0); quad(C0, C1, A1, A0);
  tri(A0, B0, C0); tri(A1, C1, B1);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.computeVertexNormals();
  // kiểm hướng: pháp tuyến phải hướng ra ngoài; đảo nếu tâm nằm phía dương
  const cen = new THREE.Vector3(); const p = g.attributes.position, nn = g.attributes.normal;
  for (let i = 0; i < p.count; i++) cen.add(new THREE.Vector3(p.getX(i), p.getY(i), p.getZ(i))); cen.divideScalar(p.count);
  const f0 = new THREE.Vector3(p.getX(0), p.getY(0), p.getZ(0)).sub(cen); const n0 = new THREE.Vector3(nn.getX(0), nn.getY(0), nn.getZ(0));
  if (f0.dot(n0) < 0) { for (let i = 0; i < p.count; i += 3) { const x = [p.getX(i + 1), p.getY(i + 1), p.getZ(i + 1)]; p.setXYZ(i + 1, p.getX(i + 2), p.getY(i + 2), p.getZ(i + 2)); p.setXYZ(i + 2, ...x); } g.computeVertexNormals(); }
  return g;
}
// Làm mượt pháp tuyến theo vị trí đỉnh, giữ cạnh gãy khi góc lớn (vòm cong mượt, góc tường–nền vẫn sắc).
function smoothNormals(g, cosT) {
  const p = g.attributes.position, n = g.attributes.normal, key = (i) => `${p.getX(i).toFixed(3)},${p.getY(i).toFixed(3)},${p.getZ(i).toFixed(3)}`;
  const face = []; for (let i = 0; i < p.count; i++) face.push(new THREE.Vector3(n.getX(i), n.getY(i), n.getZ(i)));
  const groups = new Map(); for (let i = 0; i < p.count; i++) { const k = key(i); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(i); }
  const out = new Float32Array(p.count * 3);
  for (const idx of groups.values()) for (const i of idx) { const a = new THREE.Vector3(); for (const j of idx) if (face[j].dot(face[i]) > cosT) a.add(face[j]); a.normalize(); out.set([a.x, a.y, a.z], i * 3); }
  g.setAttribute('normal', new THREE.BufferAttribute(out, 3));
}
// Tách mặt đất phẳng từng tam giác (flat normal) cho khối góc cạnh.
const flat = (g) => { const n = g.index ? g.toNonIndexed() : g; n.computeVertexNormals(); return n; };

// ---------------------------------------------------------------- nhân vật: vật liệu tô phẳng ------------------------------------
const CHAR_REMAP = {
  '#3f5552': PAL.moss, '#6b4a3a': '#7a4a30', '#2f2826': '#2a2432', '#b9b3aa': '#8d8890', '#2a2320': '#2a2226', '#2e2a2b': '#2f2c36',
  '#8a4a3c': PAL.brick, '#d6c9ae': '#e2d6bc', '#a8483a': '#b8452f', '#3a3d48': '#343a58', '#2c2522': '#2b2427',
};
function charMatFn() {
  const cache = new Map();
  return (role, color) => {
    const k = role + '|' + color;
    if (cache.has(k)) return cache.get(k);
    let m;
    if (role === 'flame') m = glow('#fff1cc', 22);
    else if (role === 'glass') { m = glow('#ffb04a', 0.55); m.transparent = true; m.blending = THREE.AdditiveBlending; m.depthWrite = false; }
    else m = toon(CHAR_REMAP[color.toLowerCase()] ?? color);
    cache.set(k, m); return m;
  };
}

// ---------------------------------------------------------------- G-buffer + viền mực -------------------------------------------
const GB_VS = 'varying vec3 vN; varying float vD; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.0); vD = -mv.z; vN = normalize(normalMatrix*normal); gl_Position = projectionMatrix*mv; }';
const GB_FS = `uniform float uId; varying vec3 vN; varying float vD;
vec2 oct(vec3 n){ n /= (abs(n.x)+abs(n.y)+abs(n.z)); vec2 s = vec2(n.x >= 0.0 ? 1.0 : -1.0, n.y >= 0.0 ? 1.0 : -1.0); return n.z >= 0.0 ? n.xy : (1.0 - abs(n.yx))*s; }
void main(){ vec3 n = normalize(vN); if (!gl_FrontFacing) n = -n; gl_FragColor = vec4(oct(n), vD, uId); }`;
const gbCache = new Map();
function gbMat(id, side) {
  const k = id + '|' + side; if (gbCache.has(k)) return gbCache.get(k);
  const m = new THREE.ShaderMaterial({ uniforms: { uId: { value: id } }, vertexShader: GB_VS, fragmentShader: GB_FS, side });
  gbCache.set(k, m); return m;
}
const EDGE_FS = /* glsl */`precision highp float; uniform sampler2D tG; uniform vec2 uRes; uniform float uK, uRmin, uRmax, uNt, uDt, uFogD, uWob, uWt, uSeed; in vec2 vUv; out vec4 o;
${NOISE_GLSL}
vec4 Gb(vec2 p){ return texture(tG, p/uRes); }
vec3 dec(vec2 e){ vec3 n = vec3(e, 1.0 - abs(e.x) - abs(e.y)); float t = max(-n.z, 0.0); n.x += n.x >= 0.0 ? -t : t; n.y += n.y >= 0.0 ? -t : t; return normalize(n); }
void main(){
  vec2 px = gl_FragCoord.xy;
  vec2 wob = (vec2(vn(px*0.012 + uSeed), vn(px*0.012 + 31.7 + uSeed)) - 0.5) * 2.0 * uWob;
  vec2 p = px + wob;
  vec4 g0 = Gb(p); bool sky0 = g0.a < 0.0; float d0 = sky0 ? 1e5 : g0.b;
  float r = clamp(uK / d0, uRmin, uRmax) * (0.72 + 0.56*vn(px*0.03 + 7.0 + uSeed));
  vec3 n0 = dec(g0.rg);
  float e = 0.0;
  for (int k = 0; k < 4; k++){
    vec2 dir = k == 0 ? vec2(1.0, 0.0) : k == 1 ? vec2(0.0, 1.0) : k == 2 ? vec2(0.7071, 0.7071) : vec2(0.7071, -0.7071);
    vec4 a = Gb(p + dir*r), b = Gb(p - dir*r);
    if (abs(a.a - g0.a) > 0.5 || abs(b.a - g0.a) > 0.5) e = max(e, 1.0);
    if (!sky0 && a.a >= 0.0 && b.a >= 0.0) {
      float w0 = 1.0/d0, wa = 1.0/max(a.b, 1e-3), wb = 1.0/max(b.b, 1e-3);
      float lap = abs(wa + wb - 2.0*w0) / w0;
      e = max(e, smoothstep(uDt, uDt*2.5, lap));
      e = max(e, smoothstep(uNt, uNt + 0.2, 1.0 - dot(n0, dec(a.rg))));
      e = max(e, smoothstep(uNt, uNt + 0.2, 1.0 - dot(n0, dec(b.rg))));
    }
  }
  float fogf = exp(-max(min(d0, 3000.0) - 25.0, 0.0) * uFogD);
  e *= mix(0.0, 1.0, fogf);
  e *= 0.70 + 0.30*smoothstep(0.22, 0.62, vn(px*0.045 + uSeed*3.0));
  o = vec4(e*uWt, 0.0, 0.0, uWt);
}`;

// ---------------------------------------------------------------- hậu kỳ: tone + giấy + chấm lưới + mực -----------------------------
const TONE = `vec3 tonemap(vec3 c){ c *= EXPOSURE; float m = max(max(c.r, c.g), c.b);
  if (m > 0.78) { float mm = 0.78 + 0.22*(1.0 - exp(-(m - 0.78)/0.22)); vec3 k = c*(mm/m); c = mix(k, vec3(mm), smoothstep(3.0, 12.0, m)*0.6); }
  return clamp(c, 0.0, 1.0); }`;
const GRADE_DECL = 'uniform sampler2D tInk; uniform sampler2D tPaper; uniform vec3 uInkS; uniform float uPaperK, uHalfK, uInkK, uVig;';
const GRADE = /* glsl */`
vec3 grade(vec3 c, vec2 uv){
  vec2 px = uv*res;
  float lum = dot(c, vec3(0.2126, 0.7152, 0.0722));
  // chấm lưới (halftone) 45°, chu kỳ 5,5 px, chỉ ở vùng tối
  vec2 hp = mat2(0.7071, -0.7071, 0.7071, 0.7071) * px / 5.5; vec2 cell = fract(hp) - 0.5;
  float cov = smoothstep(0.26, 0.04, lum) * 0.55; float rad = sqrt(cov/3.1416);
  float dm = 1.0 - smoothstep(rad - 0.07, rad + 0.07, length(cell));
  c *= 1.0 - dm*uHalfK*step(0.001, cov);
  // mực: pha một chút màu nền (mực in trên màu)
  float ink = clamp(texture(tInk, uv).r * uInkK, 0.0, 1.0);
  c = mix(c, mix(uInkS, c*0.32, 0.30), ink);
  // giấy (nướng sẵn một lần): răng giấy + loang thô + thớ sợi, tĩnh theo khung
  c *= 1.0 + uPaperK*(texture(tPaper, uv).r - 0.5)*2.0;
  vec2 q = uv - 0.5; c *= 1.0 - uVig*dot(q, q);
  return c;
}`;
const PAPER_FS = /* glsl */`precision highp float; uniform vec2 uRes; in vec2 vUv; out vec4 o;
${NOISE_GLSL}
void main(){ vec2 px = vUv*uRes*(1920.0/uRes.x);
  float fine = vn(px*0.85) - 0.5; float coarse = fbm(px*0.0045 + 3.0) - 0.57;
  vec2 fp = mat2(0.94, 0.34, -0.34, 0.94) * px; float fib = vn(vec2(fp.x*0.035, fp.y*0.55)) - 0.5;
  float v = 0.55*fine + 0.9*coarse + 0.45*fib; o = vec4(clamp(0.5 + 0.5*v, 0.0, 1.0), 0.0, 0.0, 1.0); }`;

// ---------------------------------------------------------------- trạng thái trang -------------------------------------------------
let DBG = {}; let paperRT; let W, H, renderer, pipe, gRT, inkRT, edgeScene, edgeMat, quadCam, sheets = {};
const scenes = {};

window.setup = async (cfg) => {
  W = cfg.W; H = cfg.H; DBG = cfg;
  const [ida, cas] = await Promise.all(['model-sheet/ida.json', 'model-sheet/cas.json'].map((p) => fetch('/' + p).then((r) => r.json())));
  sheets = { ida, cas };
  renderer = createRenderer(W, H);
  renderer.shadowMap.type = THREE.BasicShadowMap; // bóng cứng mỗi mẫu; độ mềm đến từ jitter đèn (3 vị trí → rìa hai bậc)
  const rt = { type: THREE.FloatType, format: THREE.RGBAFormat, colorSpace: THREE.LinearSRGBColorSpace };
  gRT = new THREE.WebGLRenderTarget(W, H, { ...rt, depthBuffer: true, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
  inkRT = new THREE.WebGLRenderTarget(W, H, { ...rt, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter });
  edgeMat = new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms: { tG: { value: gRT.texture }, uRes: { value: new THREE.Vector2(W, H) }, uK: { value: 8 }, uRmin: { value: 0.6 }, uRmax: { value: 2.4 },
      uNt: { value: 0.3 }, uDt: { value: 0.04 }, uFogD: { value: 0 }, uWob: { value: 1.0 }, uWt: { value: 1 }, uSeed: { value: 3.7 } },
    vertexShader: 'in vec3 position; out vec2 vUv; void main(){ vUv = position.xy*0.5+0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: EDGE_FS,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendEquation: THREE.AddEquation, depthTest: false, depthWrite: false,
  });
  edgeScene = new THREE.Scene(); edgeScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), edgeMat));
  quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  paperRT = new THREE.WebGLRenderTarget(W, H, { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, depthBuffer: false });
  { const pm = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, uniforms: { uRes: { value: new THREE.Vector2(W, H) } },
      vertexShader: 'in vec3 position; out vec2 vUv; void main(){ vUv = position.xy*0.5+0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }', fragmentShader: PAPER_FS, depthTest: false, depthWrite: false });
    const ps = new THREE.Scene(); ps.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), pm));
    renderer.setRenderTarget(paperRT); renderer.render(ps, new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1)); renderer.setRenderTarget(null); }
  pipe = createPipeline(renderer, W, H, {
    exposure: 1.0, toneGLSL: TONE, gradeGLSL: GRADE, uniformDecl: GRADE_DECL,
    uniforms: { tInk: { value: inkRT.texture }, tPaper: { value: paperRT.texture }, uInkS: { value: new THREE.Vector3(0.09, 0.10, 0.17) }, uPaperK: { value: 0.07 }, uHalfK: { value: 0.22 }, uInkK: { value: 1.0 }, uVig: { value: 0.35 } },
  });
  const which = cfg.only ? [cfg.only] : ['s1_opening', 's5_shadows'];
  for (const n of which) scenes[n] = n === 's1_opening' ? buildS1() : buildS5();
  // khởi động: biên dịch shader, nạp hình học (chi phí một lần mỗi shot, không tính vào thời gian khung)
  for (const n of which) { const s = scenes[n]; s.apply(); renderer.compile(s.scene, s.cam); renderInk(s, 1); pipe.accumulate(s.scene, s.cam, 1, s.hook = sampleHook(s)); renderer.autoClearDepth = true; }
};

function renderInk(s, n) {
  const cam = s.cam, gl = renderer.state.buffers.color;
  const meshes = [], hidden = [];
  s.scene.traverse((o) => {
    if (!o.visible) return;
    if (o.isMesh) {
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      if (mats.every((m) => m.userData && m.userData.toon)) meshes.push([o, o.material]);
      else hidden.push(o);
    } else if (o.isLine || o.isPoints || o.isSprite) hidden.push(o);
  });
  for (const [o, m] of meshes) o.material = Array.isArray(m) ? m.map((x) => gbMat(x.userData.id, x.side)) : gbMat(m.userData.id, m.side);
  for (const o of hidden) o.visible = false;
  const bg = s.scene.background; s.scene.background = null;
  renderer.setRenderTarget(inkRT); renderer.setClearColor(0x000000, 0); renderer.clear(true, false, false);
  const U = edgeMat.uniforms; Object.assign(U.uK, { value: s.ink.K }); U.uRmin.value = s.ink.rmin; U.uRmax.value = s.ink.rmax; U.uNt.value = s.ink.nt; U.uDt.value = s.ink.dt; U.uFogD.value = s.ink.fogD; U.uWob.value = s.ink.wob;
  U.uWt.value = 1 / n;
  const ac = renderer.autoClear;
  for (let i = 0; i < n; i++) {
    const jx = n === 1 ? 0 : ((0.5 + 0.7548776662 * (i + 3)) % 1) - 0.5, jy = n === 1 ? 0 : ((0.5 + 0.5698402910 * (i + 3)) % 1) - 0.5;
    cam.setViewOffset(W, H, jx, jy, W, H);
    renderer.setRenderTarget(gRT); renderer.autoClear = false;
    gl.setClear(0, 0, 1e5, -1); renderer.clear(true, true, false);
    renderer.render(s.scene, cam);
    renderer.setRenderTarget(inkRT); renderer.render(edgeScene, quadCam);
    renderer.autoClear = ac;
  }
  cam.clearViewOffset();
  renderer.setClearColor(0x000000, 0);
  for (const [o, m] of meshes) o.material = m;
  for (const o of hidden) o.visible = true;
  s.scene.background = bg;
}

// Tiền pass độ sâu mỗi mẫu: mỗi điểm ảnh chỉ tô một lần (SwiftShader tính trên CPU nên chồng lớp rất đắt).
const depthMat = new THREE.MeshBasicMaterial({ colorWrite: false, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 2 });
function sampleHook(s) {
  const skip = []; s.scene.traverse((o) => { if (o.isLine || (o.isMesh && (o.material.transparent || o.material.isShaderMaterial))) skip.push(o); });
  return (i, n, jit) => {
    if (s.onSample) s.onSample(i, n, jit);
    if (!DBG.pre) return;
    const [jx, jy] = n === 1 ? [0, 0] : jit;
    s.cam.setViewOffset(W, H, jx, jy, W, H);
    for (const o of skip) o.visible = false;
    s.scene.overrideMaterial = depthMat; renderer.autoClearDepth = true;
    renderer.setRenderTarget(pipe.sceneRT); renderer.render(s.scene, s.cam);
    s.scene.overrideMaterial = null; for (const o of skip) o.visible = true;
    renderer.autoClearDepth = false;
  };
}
window.renderFrame = async (name, samples) => {
  const s = scenes[name]; if (!s) throw new Error('khung lạ ' + name);
  s.apply();
  const t0 = performance.now();
  if (!DBG.noInk) renderInk(s, DBG.inkN ?? Math.max(2, Math.min(8, Math.round(samples / 4))));
  const ms = pipe.accumulate(s.scene, s.cam, samples, s.hook || (s.hook = sampleHook(s)));
  renderer.autoClearDepth = true;
  return { accum_ms: performance.now() - t0, pipe_ms: ms };
};
window.finalize = (f) => pipe.finalize(f);

// Máy quay có dịch ống kính dọc (lens shift): giữ trục chúc xuống mà vẫn lấy đủ trời. Giữ được qua setViewOffset của jitter.
function shiftCam(fov, aspect, near, far, shiftY) {
  const cam = new THREE.PerspectiveCamera(fov, aspect, near, far);
  cam.userData.shiftY = shiftY;
  cam.updateProjectionMatrix = function () {
    THREE.PerspectiveCamera.prototype.updateProjectionMatrix.call(this);
    this.projectionMatrix.elements[9] += this.userData.shiftY || 0;
    this.projectionMatrixInverse.copy(this.projectionMatrix).invert();
  };
  cam.updateProjectionMatrix();
  return cam;
}

// ================================================================= CẢNH 5 — HAI CÁI BÓNG ==========================================
function buildS5() {
  const scene = new THREE.Scene();
  const BAY_W = 3.2, BAY_D = 4.0, SPRING = 2.2;
  // Mặt tiền nhà kho có hốc vòm nhọn, đùn sâu 4 m (z 0 → 4): mặt trước z=4, vách hốc là mặt bên của lỗ.
  const FW = 22, FH = 11;
  const shape = new THREE.Shape(); shape.moveTo(-FW / 2, -0.5); shape.lineTo(FW / 2, -0.5); shape.lineTo(FW / 2, FH); shape.lineTo(-FW / 2, FH); shape.closePath();
  const arch = (bottom) => {
    const p = new THREE.Path(); p.moveTo(-BAY_W / 2, bottom); p.lineTo(-BAY_W / 2, SPRING);
    const R = 1.8125, xc = 0.2125; const a1 = Math.atan2(4.0 - SPRING, 0 - xc);
    for (let i = 1; i <= 20; i++) { const a = Math.PI + (a1 - Math.PI) * i / 20; p.lineTo(xc + R * Math.cos(a), SPRING + R * Math.sin(a)); }
    const a2 = Math.atan2(4.0 - SPRING, 0 + xc);
    for (let i = 1; i <= 20; i++) { const a = a2 + (0 - a2) * i / 20; p.lineTo(-xc + R * Math.cos(a), SPRING + R * Math.sin(a)); }
    p.lineTo(BAY_W / 2, bottom); p.closePath(); return p;
  };
  shape.holes.push(arch(-0.3));
  const facadeG = new THREE.ExtrudeGeometry(shape, { depth: BAY_D, bevelEnabled: false, curveSegments: 1 });
  const mFacade = toon('#e9e6de', { pat: 1 }), mBay = toon('#f0e8d6', { pat: 2, side: THREE.DoubleSide });
  smoothNormals(facadeG, 0.6);
  const facade = new THREE.Mesh(facadeG, [mFacade, mBay]); facade.receiveShadow = true; scene.add(facade);
  // Vách trong (trát vôi) — mặt nhận bóng.
  const backShape = new THREE.Shape(arch(0).getPoints());
  const back = new THREE.Mesh(new THREE.ShapeGeometry(backShape), mBay); back.position.z = 0.001; back.receiveShadow = true; scene.add(back);
  // Nền: đá lát trong hốc, đá hộc ngoài phố.
  const floorIn = new THREE.Mesh(new THREE.PlaneGeometry(BAY_W, BAY_D + 0.02).rotateX(-Math.PI / 2), toon('#958c7d', { pat: 3 }));
  floorIn.position.set(0, 0, BAY_D / 2); floorIn.receiveShadow = true; scene.add(floorIn);
  const street = new THREE.Mesh(new THREE.PlaneGeometry(40, 30).rotateX(-Math.PI / 2), toon('#9d99a6', { pat: 4 }));
  street.position.set(0, -0.005, BAY_D + 15); street.receiveShadow = true; scene.add(street);
  // Bậc ngưỡng đá ở miệng hốc (thấp), chân tường đá, gờ tầng, đá khoá vòm, hai đá chắn bánh xe.
  const mStone = toon('#c9c1b2'), mStoneD = toon('#a59d90');
  const addBox = (w, h, d, x, y, z, m, ry = 0) => { const b = new THREE.Mesh(flat(new THREE.BoxGeometry(w, h, d)), m); b.position.set(x, y, z); b.rotation.y = ry; b.receiveShadow = true; scene.add(b); return b; };
  addBox(BAY_W + 0.1, 0.06, 0.34, 0, 0.03, BAY_D - 0.17, mStone);
  for (const s of [-1, 1]) {
    addBox(FW / 2 - BAY_W / 2 - 0.05, 0.36, 0.07, s * (BAY_W / 2 + (FW / 2 - BAY_W / 2) / 2 + 0.03), 0.18, BAY_D + 0.035, mStoneD);
  }
  addBox(FW, 0.16, 0.18, 0, 5.2, BAY_D + 0.09, mStone);
  const key = new THREE.Mesh(flat(new THREE.CylinderGeometry(0.30, 0.2, 0.7, 4, 1)), mStone); key.rotation.y = Math.PI / 4; key.scale.set(1, 1, 0.35); key.position.set(0, 4.2, BAY_D + 0.05); scene.add(key);
  // Móc sắt, vòng buộc ngựa trên vách hốc (không đổ bóng: chỉ người đổ bóng — hai cái bóng duy nhất).
  const mIron = toon('#2a2d3a');
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.015, 6, 20), mIron); ring.position.set(-BAY_W / 2 + 0.03, 1.05, 2.6); ring.rotation.y = Math.PI / 2; scene.add(ring);
  const hook = addBox(0.04, 0.04, 0.16, BAY_W / 2 - 0.08, 2.05, 1.7, mIron);
  // Thang của Ida dựng ngoài vòm, dựa mặt tiền bên phải (ánh điện phẳng: không bóng đổ dài).
  const ladder = buildLadder(1.806, 0.335, 6, (r, c) => toon('#8a6a45'), '#8a6a45');
  ladder.traverse((o) => { o.castShadow = false; }); ladder.position.set(2.55, 0, BAY_D + 0.42); ladder.rotation.x = -0.2; scene.add(ladder);
  // Cột điện ngoài phố ở mép trái khung: chỉ thân cột (tấm kính ở ngoài khung).
  const post = new THREE.Mesh(flat(new THREE.CylinderGeometry(0.07, 0.11, 7, 6)), mIron); post.position.set(-3.35, 3.5, BAY_D + 1.3); scene.add(post);
  const postBase = new THREE.Mesh(flat(new THREE.CylinderGeometry(0.16, 0.2, 0.7, 6)), mIron); postBase.position.set(-3.35, 0.35, BAY_D + 1.3); scene.add(postBase);

  // Nhân vật: quay lưng về máy, cách vách ~1 m; Ida trái, Cas phải (theo hướng nhìn của máy).
  const mf = charMatFn();
  const ida = buildCharacter(sheets.ida, { material: mf, detail: 28 }); ida.setPose(sheets.ida.poses.look_shadows);
  const cas = buildCharacter(sheets.cas, { material: mf, detail: 28 }); cas.setPose(sheets.cas.poses.half_raised);
  ida.root.position.set(-0.55, 0, 1.0); ida.root.rotation.y = Math.PI - 0.08;
  cas.root.position.set(0.50, 0, 1.0); cas.root.rotation.y = Math.PI + 0.10;
  // Chi tiết trang trí gắn khớp đầu (không đổi đường bao): lớp tóc phủ nửa sau sọ — nhìn từ lưng đọc rõ là gáy, không phải mặt.
  for (const [ch, col] of [[ida, '#b9b3aa'], [cas, '#5a4034']]) {
    const hd = ch.sheet.parts.head, Hm = ch.H;
    const g = new THREE.SphereGeometry(0.5, 40, 20, Math.PI * 1.02, Math.PI * 0.96, 0.12 * Math.PI, 0.60 * Math.PI);
    const sh = new THREE.Mesh(g, mf('hair', col)); sh.scale.set(hd.width_front * Hm * 1.025, hd.length * Hm * 1.02, hd.width_side * Hm * 1.025); sh.position.y = hd.length * Hm / 2;
    sh.material.side = THREE.DoubleSide; ch.joints.head.add(sh);
  }
  for (const ch of [ida, cas]) { scene.add(ch.root); ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); }
  // Đèn lồng trên nền đá, cách vách 3 m, ngay trong miệng vòm.
  const lantern = buildLantern(sheets.ida.props.lantern.height_H * sheets.ida.H_m, mf);
  lantern.position.set(0.05, 0, 3.0); lantern.rotation.y = 0.5; scene.add(lantern);
  lantern.traverse((o) => { if (o.isMesh) { o.castShadow = false; o.receiveShadow = false; } });
  lantern.updateMatrixWorld(true);
  const anchor = new THREE.Vector3(); lantern.userData.lightAnchor.getWorldPosition(anchor);
  // Quầng đèn lồng.
  const haloB = new Batch(); const hs = 0.9;
  haloB.add('halo', new THREE.PlaneGeometry(hs * 2, hs * 2), TRS(anchor.x, anchor.y + 0.05, anchor.z + 0.05), '#ffd29a', 1.1);
  const halo = new THREE.Mesh(merge(haloB.lists.get('halo')), haloMaterial()); scene.add(halo);

  // Đèn: một nguồn điểm hổ phách có bóng, jitter trong kính đèn (3 vị trí → rìa mềm hai bậc).
  const LCOL = C('#ffb366');
  const light = new THREE.PointLight(LCOL, 16, 0, 2);
  light.castShadow = !DBG.noShadow; light.shadow.mapSize.set(1024, 1024); light.shadow.camera.near = 0.05; light.shadow.camera.far = 14; light.shadow.bias = -0.002; light.shadow.normalBias = 0.015; light.shadow.autoUpdate = false; light.shadow.needsUpdate = true;
  light.position.copy(anchor); scene.add(light);
  const J = [[-0.06, -0.025, 0], [0.06, -0.025, 0], [0, 0.05, 0]];
  const FLICK = 0.985; // rung sáng ±4%: khung tĩnh lấy một pha (−1,5%)
  const cam = new THREE.PerspectiveCamera(38, W / H, 0.05, 300);
  cam.position.set(0.25, 1.35, 9.2); cam.lookAt(0.05, 1.35 + 9.2 * Math.tan(3.5 * Math.PI / 180), 0);
  if (DBG.cam) { cam.position.set(...DBG.cam.slice(0, 3)); cam.fov = DBG.cam[6]; cam.updateProjectionMatrix(); cam.lookAt(...DBG.cam.slice(3, 6)); }
  const apply = () => {
    G.uStep.value = 0.95; G.uOff.value = 0.35; G.uQlo.value = -4.5; G.uQhi.value = 0.5;
    G.uCool.value.set(0.78, 0.86, 1.18); G.uWarm.value.set(1.08, 1.0, 0.88);
    const el = C('#d9e3ef').multiplyScalar(1.6); G.uElec.value.set(el.r, el.g, el.b, 1);
    G.uBay.value.set(BAY_W / 2, BAY_D, 0.95, 1);
    const b = LCOL.clone().multiplyScalar(0.10); G.uBounce.value.set(b.r, b.g, b.b, 1); G.uLanternPos.value.copy(anchor);
    G.uFog.value.set(0, 0, 1, 0); G.uLantAng.value.set(1, 0.76, 1.7, 0.30);
    for (const k of ['uHs', 'uHg', 'uDc']) FAR[k].value.set(0, 0, 0); FAR.uLampC.value.set(0, 0, 0);
    Object.assign(pipe.outMat.uniforms.uHalfK, { value: 0.20 }); pipe.outMat.uniforms.uPaperK.value = 0.07; pipe.outMat.uniforms.uVig.value = 0.45;
  };
  const onSample = (i, n) => { const k = Math.min(2, Math.floor(i * 3 / n)); const j = J[k]; if (k !== light.userData.k) { light.userData.k = k; light.shadow.needsUpdate = true; } light.position.set(anchor.x + j[0], anchor.y + j[1], anchor.z + j[2]); light.intensity = 16 * FLICK; };
  return { scene, cam, apply, onSample, ink: { K: 11, rmin: 0.7, rmax: 2.6, nt: 0.28, dt: 0.035, fogD: 0, wob: 0.9 } };
}

// ================================================================= CẢNH 1 — VÒNG ĐÈN (toàn cảnh cao) ===============================
function buildS1() {
  const scene = new THREE.Scene();
  const r = rng(1907);
  // --- đường tim phố Ostler: bắt đầu ở quảng trường, cong dần sang phải, dốc xuống ---
  const S0 = [0, 0, -10]; // đầu phố
  const gH = (x, z) => 0.058 * Math.max(Math.min(z + 10, 0), -660) + (z < -900 ? 0.03 * (-900 - z) : 0);
  const tab = []; { let x = S0[0], z = S0[2]; for (let s = 0; s <= 260; s += 0.5) { const phi = -0.16 + 0.0044 * s; tab.push({ x, z, phi }); x += Math.sin(phi) * 0.5; z -= Math.cos(phi) * 0.5; } }
  const SF = (s) => { const t = tab[Math.max(0, Math.min(tab.length - 1, Math.round(s * 2)))]; const d = new THREE.Vector3(Math.sin(t.phi), 0, -Math.cos(t.phi)); const n = new THREE.Vector3(Math.cos(t.phi), 0, Math.sin(t.phi)); return { p: new THREE.Vector3(t.x, gH(t.x, t.z), t.z), d, n }; };
  const distToStreet = (x, z) => { let best = 1e9; for (let i = 0; i < tab.length; i += 4) { const dx = x - tab[i].x, dz = z - tab[i].z; const dd = dx * dx + dz * dz; if (dd < best) best = dd; } return Math.sqrt(best); };
  const END_S = 200;

  const B = new Batch();
  const FAC = ['#b3aca4', '#a39fb0', '#9a95aa', '#bab2a6', '#8f8aa0', '#aaa3a8', '#c4bcb0', '#9790a4'];
  const ROOF = ['#3a3d58', '#34384e', '#413b54', '#2f3448', '#453f5c'];
  const upV = new THREE.Vector3(0, 1, 0);
  const basisM = (P, X, Z, lean, leanZ) => { const m = M4().makeBasis(X, upV, Z); m.setPosition(P); const sh = M4().set(1, lean, 0, 0, 0, 1, 0, 0, 0, leanZ, 1, 0, 0, 0, 0, 1); return m.multiply(sh); };

  // Nhà: mặt tiền ở z=0 (local) nhìn +z, thân lùi về −z; nền y=0 tại mặt phố.
  function house(m, o) {
    const { w, d, h, pitch, type, fac, roof, lod, litP } = o;
    const add = (key, g, mm, hex, k) => B.add((lod >= 2 && (key === 'wall' || key === 'roof' || key === 'chim') ? 'F' : '') + key, g, M4().multiplyMatrices(m, mm || M4()), hex, k);
    const sink = lod >= 2 ? 2 : 5;
    add('wall', flat(new THREE.BoxGeometry(w, h + sink, d)), TRS(0, (h - sink) / 2, -d / 2), fac);
    const ov = 0.35, rise = Math.min(9, (type === 'A' ? d / 2 : w / 2) * Math.tan(pitch));
    if (type === 'A') { // mái hai dốc, nóc song song phố
      add('roof', prism([ov, h - 0.12], [-d / 2, h + rise], [-d - ov, h - 0.12], w + 0.5, 'x'), null, roof);
      add('wall', prism([0, h - 0.13], [-d / 2, h + rise - 0.25], [-d, h - 0.13], w - 0.02, 'x'), null, fac);
      if (lod < 1 && w > 6.2 && r() < 0.7) { // cửa sổ mái nhọn
        const dz = -(1.4 / Math.tan(pitch)) + 0.1, dx = (r() - 0.5) * (w - 3);
        add('wall', flat(new THREE.BoxGeometry(1.2, 1.6, 2.2)), TRS(dx, h + 0.9, dz - 1.1 + 0.4), fac);
        add('roof', prism([-0.8, h + 1.62], [0, h + 2.7], [0.8, h + 1.62], 2.6, 'z'), TRS(dx, 0, dz - 0.9), roof);
        add('glass', new THREE.PlaneGeometry(0.6, 0.9), TRS(dx, h + 0.95, dz + 0.42), '#ffffff');
      }
    } else { // đầu hồi nhọn quay ra phố
      add('roof', prism([-w / 2 - ov, h - 0.12], [0, h + rise], [w / 2 + ov, h - 0.12], d + 2 * ov, 'z'), TRS(0, 0, -d / 2), roof);
      add('wall', prism([-w / 2 + 0.01, h - 0.13], [0, h + rise - 0.3], [w / 2 - 0.01, h - 0.13], d - 0.02, 'z'), TRS(0, 0, -d / 2), fac);
      if (lod < 2) add(r() < 0.15 && lod < 1 ? 'lit' : 'glass', new THREE.PlaneGeometry(0.7, 1.1), TRS(0, h + rise * 0.35, 0.02), r() < 0.15 ? '#f6b25c' : '#ffffff', r() < 0.15 ? 0.9 : 1);
    }
    // ống khói mảnh, nắp loe, 1–2 ống sành
    const nCh = lod >= 2 ? (r() < 0.5 ? 1 : 0) : 1 + (r() < 0.45 ? 1 : 0);
    for (let i = 0; i < nCh; i++) {
      const cx = (i === 0 ? -1 : 1) * (w / 2 - 0.8) * (0.5 + 0.5 * r()), cz = type === 'A' ? -d / 2 + (r() - 0.5) * 1.5 : -d * (0.3 + 0.5 * r());
      const top = h + rise * (type === 'A' ? 0.85 : 0.6) + 1.6 + r() * 1.8, cw = 0.45 + r() * 0.25;
      add('chim', flat(new THREE.BoxGeometry(cw, top - h, cw * 1.4)), TRS(cx, (top + h) / 2, cz), fac);
      if (lod < 2) {
        add('chim', flat(new THREE.BoxGeometry(cw + 0.2, 0.14, cw * 1.4 + 0.2)), TRS(cx, top, cz), '#5b5566');
        if (lod < 1) for (let k = 0; k < 1 + (r() < 0.5 ? 1 : 0); k++) add('chim', new THREE.CylinderGeometry(0.08, 0.1, 0.55, 6), TRS(cx + (k - 0.5) * 0.22 * 0, top + 0.33, cz + (k - 0.5) * 0.3), '#8a5a48');
      }
    }
    // cửa sổ: cao, hẹp; một vài ô sáng ấm
    if (lod < 2) {
      const floors = Math.max(1, Math.floor((h - 0.6) / 3.1)), nWin = Math.max(1, Math.floor((w - 0.8) / 1.9));
      for (let f = 0; f < floors; f++) for (let i = 0; i < nWin; i++) {
        const x = -w / 2 + w * (i + 0.5) / nWin, y = 1.0 + f * 3.1 + (f === 0 ? 0 : 0.2), wh = f === 0 ? 1.7 : 1.45;
        if (f === 0 && i === (nWin > 1 ? 1 : 0) && lod < 1) { add('door', flat(new THREE.BoxGeometry(1.0, 2.3, 0.1)), TRS(x, 1.15, 0.0), '#3a2f35'); continue; }
        const lit = r() < litP;
        if (lod < 1) add('frame', flat(new THREE.BoxGeometry(0.98, wh + 0.14, 0.08)), TRS(x, y + wh / 2, 0.0), '#d8cfbf');
        add(lit ? 'lit' : 'glass', new THREE.PlaneGeometry(0.78, wh), TRS(x, y + wh / 2, 0.05), lit ? (r() < 0.5 ? '#f6b25c' : '#f0a04a') : '#ffffff', lit ? 0.55 + r() * 0.5 : 1);
        if (lod < 1 && f > 0) add('glass', new THREE.PlaneGeometry(0.78, wh), TRS(-x, y + wh / 2, -d - 0.05, Math.PI), '#ffffff');
      }
      if (lod < 1) add('trim', flat(new THREE.BoxGeometry(w + 0.1, 0.22, 0.2)), TRS(0, h - 0.22, 0.05), '#6d6275');
    }
  }
  // Nhà xa tối giản (~14–24 tam giác): thân không đáy/nóc, mái 2 dốc, hồi tam giác, ống khói thưa.
  function farHouse(m, o) {
    const { w, d, h, pitch, type, fac, roof } = o; const pos = [], rpos = [];
    const q = (arr, a, b, c, e) => arr.push(...a, ...b, ...c, ...a, ...c, ...e);
    const x0 = -w / 2, x1 = w / 2, z0 = 0, z1 = -d, y0 = -2, y1 = h;
    q(pos, [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0]); q(pos, [x1, y0, z1], [x0, y0, z1], [x0, y1, z1], [x1, y1, z1]);
    q(pos, [x1, y0, z0], [x1, y0, z1], [x1, y1, z1], [x1, y1, z0]); q(pos, [x0, y0, z1], [x0, y0, z0], [x0, y1, z0], [x0, y1, z1]);
    if (type === 'A') { const rise = Math.min(8, d / 2 * Math.tan(pitch)), zm = -d / 2;
      q(rpos, [x0 - 0.3, h, z0 + 0.3], [x1 + 0.3, h, z0 + 0.3], [x1 + 0.3, h + rise, zm], [x0 - 0.3, h + rise, zm]);
      q(rpos, [x1 + 0.3, h, z1 - 0.3], [x0 - 0.3, h, z1 - 0.3], [x0 - 0.3, h + rise, zm], [x1 + 0.3, h + rise, zm]);
      pos.push(x1, h, z0, x1, h, z1, x1, h + rise, zm, x0, h, z1, x0, h, z0, x0, h + rise, zm);
    } else { const rise = Math.min(8, w / 2 * Math.tan(pitch));
      q(rpos, [x1 + 0.3, h, z0 + 0.3], [x1 + 0.3, h, z1 - 0.3], [0, h + rise, z1 - 0.3], [0, h + rise, z0 + 0.3]);
      q(rpos, [x0 - 0.3, h, z1 - 0.3], [x0 - 0.3, h, z0 + 0.3], [0, h + rise, z0 + 0.3], [0, h + rise, z1 - 0.3]);
      pos.push(x0, h, z0, x1, h, z0, 0, h + rise, z0, x1, h, z1, x0, h, z1, 0, h + rise, z1);
    }
    if (r() < 0.35) { const cx = (r() - 0.5) * (w - 2), cz = -d * (0.3 + 0.4 * r()), c = 0.4, t = h + 4 + r() * 3;
      q(pos, [cx - c, h, cz + c], [cx + c, h, cz + c], [cx + c, t, cz + c], [cx - c, t, cz + c]); q(pos, [cx + c, h, cz + c], [cx + c, h, cz - c], [cx + c, t, cz - c], [cx + c, t, cz + c]);
      q(pos, [cx - c, h, cz - c], [cx - c, h, cz + c], [cx - c, t, cz + c], [cx - c, t, cz - c]); q(pos, [cx - c, t, cz + c], [cx + c, t, cz + c], [cx + c, t, cz - c], [cx - c, t, cz - c]); }
    const mk = (arr) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(arr, 3)); g.computeVertexNormals(); return g; };
    B.add('Fwall', mk(pos), m, fac); B.add('Froof', mk(rpos), m, roof);
  }
  const placeHouse = (P, X, Z, o) => (o.lod >= 2 ? farHouse : house)(basisM(P, X, Z, (r() - 0.5) * 0.05, (r() - 0.35) * 0.035), o);

  // --- hai dãy nhà phố Ostler ---
  const HALF = 6.0;
  for (const side of [-1, 1]) {
    let s = -1 + r() * 2;
    while (s < END_S - 6) {
      const w = 5.5 + r() * 3.6;
      if (r() < 0.07) { s += 1.6; continue; } // ngõ hẹp
      const f = SF(s + w / 2), set = r() * 0.35;
      const P = f.p.clone().addScaledVector(f.n, side * (HALF + set));
      const X = f.d.clone().multiplyScalar(-side), Z = f.n.clone().multiplyScalar(-side);
      placeHouse(P, X, Z, { w, d: 9 + r() * 3, h: 6.6 + Math.floor(r() * 2.4) * 3.1 + r() * 0.6, pitch: (48 + r() * 12) * Math.PI / 180, type: r() < 0.42 ? 'B' : 'A', fac: FAC[Math.floor(r() * FAC.length)], roof: ROOF[Math.floor(r() * ROOF.length)], lod: 0, litP: 0.08 });
      s += w + 0.05;
    }
  }
  // --- nhà kho cuối phố: tường gạch trắng vôi chắn ngang ---
  { const f = SF(END_S); const P = f.p.clone().addScaledVector(f.d, 1.5); const X = f.n.clone().multiplyScalar(1), Z = f.d.clone().multiplyScalar(-1);
    const m = M4().makeBasis(X, upV, Z); m.setPosition(P);
    B.add('ware', flat(new THREE.BoxGeometry(34, 16, 22)), M4().multiplyMatrices(m, TRS(0, 3, -11)), '#e6dccb');
    B.add('roof', prism([1, 11], [-11, 17], [-23, 11], 34.4, 'x'), m, '#3b3d52');
    B.add('door', flat(new THREE.BoxGeometry(3.2, 4, 0.2)), M4().multiplyMatrices(m, TRS(6, 2, 0.02)), '#262a3c');
  }
  // --- quảng trường đầu phố: nhà vây quanh ---
  for (let i = 0; i < 16; i++) {
    const a = -0.3 + i * 0.36; const R0 = 20 + r() * 2;
    const P = new THREE.Vector3(Math.sin(a) * R0, 0, 4 + Math.cos(a) * R0);
    if (P.z < -8 && Math.abs(P.x) < 12) continue; // chừa miệng phố
    const Z = new THREE.Vector3(-P.x, 0, 4 - P.z).normalize(), X = new THREE.Vector3().crossVectors(upV, Z).normalize();
    placeHouse(P, X, Z, { w: 7 + r() * 3, d: 10, h: 10 + r() * 4, pitch: 55 * Math.PI / 180, type: r() < 0.5 ? 'B' : 'A', fac: FAC[Math.floor(r() * FAC.length)], roof: ROOF[Math.floor(r() * ROOF.length)], lod: 0, litP: 0.08 });
  }
  // --- phần còn lại của thành phố: các dãy phố khác, thưa dần theo khoảng cách ---
  const CAMP = (() => { const f = SF(0); return f.p.clone().addScaledVector(f.d, -50).addScaledVector(f.n, 2).add(new THREE.Vector3(0, 37, 0)); })();
  const farLamps = [];
  { const psi = -0.32, A = new THREE.Vector3(Math.cos(psi), 0, Math.sin(psi)), Bv = new THREE.Vector3(-Math.sin(psi), 0, Math.cos(psi)).multiplyScalar(-1);
    const fwd = SF(72).p.clone().sub(CAMP).setY(0).normalize();
    for (let j = -2; j < 34; j++) {
      const v0 = j * 30;
      for (const [dv, face] of [[-5, 1], [5, -1]]) {
        let u = -1400 + r() * 20;
        while (u < 1400) {
          const P = new THREE.Vector3().addScaledVector(A, u).addScaledVector(Bv, v0 + dv);
          const rel = P.clone().sub(CAMP); rel.y = 0; const dist = rel.length();
          const ang = Math.acos(Math.max(-1, Math.min(1, rel.clone().normalize().dot(fwd))));
          const lod = dist < 190 ? 1 : dist < 420 ? 2 : 3;
          const w = (lod === 3 ? 15 : lod === 2 ? 9 : 6) + r() * 4;
          if (r() < 0.06) { u += 10; continue; } // phố cắt ngang
          if (!DBG.noFar && dist < 700 && ang < 0.95 && distToStreet(P.x, P.z) > 19 && P.clone().sub(new THREE.Vector3(0, 0, 4)).length() > 27) {
            P.y = gH(P.x, P.z);
            const Z = Bv.clone().multiplyScalar(-face), X = new THREE.Vector3().crossVectors(upV, Z).normalize();
            placeHouse(P, X, Z, { w, d: 8 + r() * 3, h: 6.5 + Math.floor(r() * 3) * 3 + r(), pitch: (46 + r() * 14) * Math.PI / 180, type: r() < 0.4 ? 'B' : 'A', fac: FAC[Math.floor(r() * FAC.length)], roof: ROOF[Math.floor(r() * ROOF.length)], lod: Math.max(lod, 1), litP: lod >= 3 ? 0 : 0.05 });
            if (dv < 0 && r() < 0.085 && dist < 700 && dist > 230) { const L = P.clone().addScaledVector(Bv, 5); L.y = gH(L.x, L.z) + 3.4; farLamps.push([L, dist]); }
          }
          u += w + 0.1;
        }
      }
    }
    // tháp chuông nhọn và ống khói nhà máy xa: điểm nhấn đường chân trời
    const spire = (x, z, h, wdt) => { const y = gH(x, z); B.add('wall', flat(new THREE.BoxGeometry(wdt, h, wdt)), TRS(x, y + h / 2 - 3, z, 0.4), '#9a8fa0'); B.add('roof', flat(new THREE.ConeGeometry(wdt * 0.78, h * 0.9, 4)), TRS(x, y + h + h * 0.45 - 3, z, 0.4 + Math.PI / 4), '#3a3f5a'); };
    spire(-150, -520, 34, 7); spire(190, -610, 30, 6);
    // Dải chân trời: thành phố xa vẽ thành các lớp bìa cắt (mái nhọn, ống khói, tháp) — kiểu minh hoạ sách, rất rẻ.
    const skyline = (R, hMin, hMax, hex, seed) => {
      const rr = rng(seed), pos = []; const a0 = Math.atan2(fwd.x, -fwd.z);
      let a = a0 - 0.78;
      while (a < a0 + 0.78) {
        const wd = (10 + rr() * 22) / R, h = hMin + rr() * (hMax - hMin), a1 = a + wd;
        const P = (aa, y) => [CAMP.x + Math.sin(aa) * R, y, CAMP.z - Math.cos(aa) * R];
        const yb = gH(CAMP.x + Math.sin(a) * R, CAMP.z - Math.cos(a) * R) - 25;
        const yt = gH(CAMP.x + Math.sin(a) * R, CAMP.z - Math.cos(a) * R) + h;
        pos.push(...P(a, yb), ...P(a1, yb), ...P(a1, yt), ...P(a, yb), ...P(a1, yt), ...P(a, yt));
        const k = rr();
        if (k < 0.55) pos.push(...P(a, yt), ...P(a1, yt), ...P((a + a1) / 2, yt + (a1 - a) * R * 0.5 * (0.9 + rr() * 0.8)));
        else if (k < 0.85) { const c = a + (a1 - a) * (0.2 + 0.6 * rr()), cw = 1.2 / R; pos.push(...P(c, yt), ...P(c + cw, yt), ...P(c + cw, yt + 4 + rr() * 4), ...P(c, yt), ...P(c + cw, yt + 4 + rr() * 4), ...P(c, yt + 4 + rr() * 4)); }
        else if (k < 0.9) { const c = (a + a1) / 2, cw = 4 / R; pos.push(...P(c - cw, yt), ...P(c + cw, yt), ...P(c, yt + 25 + rr() * 20)); }
        a = a1 + (rr() < 0.15 ? 6 / R : 0);
      }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
      const n = g.attributes.normal; for (let i = 0; i < n.count; i++) { const px = g.attributes.position.getX(i) - CAMP.x, pz = g.attributes.position.getZ(i) - CAMP.z; const l = Math.hypot(px, pz); n.setXYZ(i, -px / l, 0, -pz / l); }
      B.add('Fwall', g, null, hex);
    };
    skyline(780, 12, 26, '#8d8396', 11); skyline(1050, 14, 30, '#8a8096', 12); skyline(1500, 18, 40, '#8a8096', 13); skyline(2300, 25, 55, '#8a8096', 14);
  }
  // --- mặt đất, mặt phố, vỉa hè ---
  { const g = new THREE.PlaneGeometry(9000, 7000, 90, 70).rotateX(-Math.PI / 2); g.translate(0, 0, -3300);
    const p = g.attributes.position; for (let i = 0; i < p.count; i++) p.setY(i, gH(p.getX(i), p.getZ(i)) - 0.2); g.computeVertexNormals();
    B.add('ground', g, null, '#3c3a4c'); }
  const ribbon = (a, b, dy, key, hex) => {
    const pos = [];
    for (let s = -2; s < END_S; s += 1) {
      const f0 = SF(s), f1 = SF(s + 1);
      const P = (f, o) => f.p.clone().addScaledVector(f.n, o).add(new THREE.Vector3(0, dy, 0));
      const a0 = P(f0, a), b0 = P(f0, b), a1 = P(f1, a), b1 = P(f1, b);
      pos.push(...a0.toArray(), ...b0.toArray(), ...b1.toArray(), ...a0.toArray(), ...b1.toArray(), ...a1.toArray());
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
    const n = g.attributes.normal; for (let i = 0; i < n.count; i++) if (n.getY(i) < 0) n.setXYZ(i, -n.getX(i), -n.getY(i), -n.getZ(i));
    B.add(key, g, null, hex);
  };
  ribbon(-3.6, 3.6, 0.02, 'road', '#6a6679');
  ribbon(-HALF - 0.4, -3.6, 0.17, 'pave', '#7c7684'); ribbon(3.6, HALF + 0.4, 0.17, 'pave', '#7c7684');
  { const g = new THREE.CircleGeometry(22, 48).rotateX(-Math.PI / 2); B.add('road', g, TRS(0, 0.03, 4), '#6f6a7c'); }

  // --- 11 cột đèn khí; ngọn 1–4 đã thắp (Ida vừa thắp ngọn 4) ---
  const LIT = 4, lamps = [];
  const lampHead = (m, lit) => {
    const add = (key, g, mm, hex, k) => B.add(key, g, M4().multiplyMatrices(m, mm), hex, k);
    add('iron', flat(new THREE.CylinderGeometry(0.2, 0.26, 0.5, 8)), TRS(0, 0.25, 0), '#2a2d3b');
    add('iron', new THREE.CylinderGeometry(0.05, 0.09, 3.0, 8), TRS(0, 1.75, 0), '#2a2d3b');
    add('iron', flat(new THREE.BoxGeometry(0.75, 0.05, 0.05)), TRS(0, 2.75, 0), '#2a2d3b');
    add(lit ? 'lampLit' : 'lampOff', flat(new THREE.CylinderGeometry(0.24, 0.14, 0.5, 4)), TRS(0, 3.35, 0, Math.PI / 4), lit ? '#ffc167' : '#ffffff', lit ? 1 : 1);
    add('iron', flat(new THREE.ConeGeometry(0.3, 0.32, 4)), TRS(0, 3.76, 0, Math.PI / 4), '#2a2d3b');
    add('iron', new THREE.CylinderGeometry(0.015, 0.03, 0.3, 5), TRS(0, 4.05, 0), '#2a2d3b');
  };
  for (let i = 0; i < 11; i++) {
    const s = 12 + 17 * i, side = i % 2 ? 1 : -1, f = SF(s);
    const P = f.p.clone().addScaledVector(f.n, side * 4.3); P.y += 0.17;
    const m = M4().makeBasis(f.n, upV, f.d.clone().multiplyScalar(-1)); m.setPosition(P);
    lampHead(m, i < LIT); lamps.push({ P, lit: i < LIT, f, side });
  }
  // --- cột điện kiểu mới: cao 7 m, tấm kính mờ chữ nhật, CHƯA bật; dây điện mới ---
  const epTops = [];
  for (let k = 0; k < 6; k++) {
    const s = 20.5 + 34 * k, side = k % 2 ? -1 : 1, f = SF(s);
    const P = f.p.clone().addScaledVector(f.n, side * 4.4); P.y += 0.17;
    const inward = f.n.clone().multiplyScalar(-side);
    const add = (key, g, mm, hex) => B.add(key, g, M4().multiplyMatrices(TRS(P.x, P.y, P.z), mm), hex);
    add('iron', flat(new THREE.CylinderGeometry(0.07, 0.13, 7.0, 6)), TRS(0, 3.5, 0), '#262937');
    const arm = inward.clone().multiplyScalar(0.9);
    const armM = M4().lookAt(new THREE.Vector3(), inward, upV); armM.setPosition(arm.x * 0.5, 6.9, arm.z * 0.5);
    add('iron', flat(new THREE.BoxGeometry(0.06, 0.06, 1.0)), armM, '#262937');
    const panM = M4().lookAt(new THREE.Vector3(), f.d, upV); panM.setPosition(arm.x, 6.55, arm.z);
    add('panel', flat(new THREE.BoxGeometry(0.95, 0.62, 0.12)), panM, '#ffffff');
    epTops.push(new THREE.Vector3(P.x, P.y + 7.05, P.z));
  }
  const wires = [];
  for (let k = 0; k + 1 < epTops.length; k++) { const a = epTops[k], b = epTops[k + 1]; const pts = []; for (let i = 0; i <= 16; i++) { const t = i / 16; const p = a.clone().lerp(b, t); p.y -= 0.9 * 4 * t * (1 - t); pts.push(p); } wires.push(pts); }
  for (let k = 0; k < epTops.length; k++) { const a = epTops[k]; const f = SF(20.5 + 34 * k); const b = a.clone().addScaledVector(f.n, (k % 2 ? 1 : -1) * 9.5); b.y += 1.5; const pts = []; for (let i = 0; i <= 10; i++) { const t = i / 10; const p = a.clone().lerp(b, t); p.y -= 0.35 * 4 * t * (1 - t); pts.push(p); } wires.push(pts); }
  const wireMat = new THREE.LineBasicMaterial({ color: C(PAL.ink) });
  for (const pts of wires) scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), wireMat));

  // --- cột đồng hồ điện ở quảng trường: mặt tròn 1,2 m, 12 vạch, không số, CHƯA sáng ---
  { const f0 = SF(0); const P = f0.p.clone().addScaledVector(f0.n, -7.2).addScaledVector(f0.d, -2.5);
    const face = CAMP.clone().sub(P).setY(0).normalize().applyAxisAngle(upV, 0.35); const X = new THREE.Vector3().crossVectors(upV, face).normalize();
    const m = M4().makeBasis(X, upV, face); m.setPosition(P);
    const add = (key, g, mm, hex) => B.add(key, g, M4().multiplyMatrices(m, mm), hex);
    add('iron', flat(new THREE.CylinderGeometry(0.42, 0.55, 0.9, 8)), TRS(0, 0.45, 0), '#262937');
    add('iron', flat(new THREE.CylinderGeometry(0.11, 0.16, 5.2, 8)), TRS(0, 3.4, 0), '#262937');
    add('iron', flat(new THREE.CylinderGeometry(0.72, 0.72, 0.3, 32).rotateX(Math.PI / 2)), TRS(0, 6.4, 0), '#262937');
    add('dial', new THREE.CircleGeometry(0.6, 40), TRS(0, 6.4, 0.16), '#ffffff');
    add('dial', new THREE.CircleGeometry(0.6, 40).rotateY(Math.PI), TRS(0, 6.4, -0.16), '#ffffff');
    for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; const bm = M4().makeRotationZ(-a); bm.setPosition(Math.sin(a) * 0.49, 6.4 + Math.cos(a) * 0.49, 0.17); add('iron', new THREE.PlaneGeometry(0.04, i % 3 ? 0.13 : 0.18), bm, '#262937'); }
    const hand = (a, len, wd) => { const hm = M4().makeRotationZ(-a); const off = new THREE.Vector3(0, len / 2 - 0.05, 0).applyMatrix4(M4().makeRotationZ(-a)); hm.setPosition(off.x, 6.4 + off.y, 0.18); add('iron', new THREE.PlaneGeometry(wd, len), hm, '#262937'); };
    hand(-2 * Math.PI / 60, 0.55, 0.035); hand(6 * Math.PI / 6 - 0.03, 0.34, 0.05);
    add('iron', flat(new THREE.ConeGeometry(0.16, 0.5, 8)), TRS(0, 7.0, 0), '#262937'); }

  // --- vật liệu ---
  const mats = {
    wall: toon('#ffffff', { vcol: true }), roof: toon('#ffffff', { vcol: true, pat: 5 }), chim: toon('#ffffff', { vcol: true }),
    glass: toon('#262b44', { vcol: true }), frame: toon('#ffffff', { vcol: true }), door: toon('#ffffff', { vcol: true }), trim: toon('#ffffff', { vcol: true }),
    Fwall: farToon(), Froof: farToon(), Fchim: farToon(),
    lit: glow('#ffffff', 1.0, { vcol: true }), ware: toon('#ffffff', { vcol: true, pat: 1 }),
    ground: toon('#ffffff', { vcol: true }), road: toon('#ffffff', { vcol: true, pat: 4 }), pave: toon('#ffffff', { vcol: true, pat: 3 }),
    iron: toon('#ffffff', { vcol: true }), lampLit: glow('#ffffff', 3.2, { vcol: true }), lampOff: toon('#565c7a', { vcol: true }),
    panel: toon('#c9cbd6', { vcol: true }), dial: toon('#d4d2d8', { vcol: true }),
  };
  if (DBG.cheap) for (const k of Object.keys(mats)) mats[k] = new THREE.MeshBasicMaterial({ color: 0x808080 });
  B.build(scene, mats);
  if (DBG.stats) { let t = 0; scene.traverse((o) => { if (o.isMesh) t += o.geometry.attributes.position.count / 3; }); console.log('tris', t); }

  // --- quầng sáng (đèn phố Ostler + đèn khí rải rác khắp thành phố + cửa sổ) ---
  const halos = new Batch(), halosFar = new Batch();
  const CAM = CAMP;
  const bill = (P, size, hex, k) => { const m = M4().lookAt(CAM, P, upV); m.setPosition(P); halos.add('h', new THREE.PlaneGeometry(size, size), m, hex, k); };
  const lampLights = [];
  for (const L of lamps) if (L.lit) {
    const P = L.P.clone(); P.y += 3.35; bill(P, 8, '#ff9a3a', 1.0);
    lampLights.push(new THREE.Vector4(P.x, P.y, P.z, 44));
  }
    for (const [P, dist] of farLamps) { { const m = M4().lookAt(CAM, P, upV); m.setPosition(P.x, P.y + 1, P.z); halosFar.add('h', new THREE.PlaneGeometry(4 + dist * 0.01, 4 + dist * 0.01), m, '#ff9a3a', 0.6); } B.add('x', new THREE.SphereGeometry(0.4, 6, 4), TRS(P.x, P.y, P.z), '#ffc167'); }
  const farLampMesh = new THREE.Mesh(merge(B.lists.get('x') || [bake(new THREE.SphereGeometry(0.01), null, '#000')]), glow('#ffffff', 3.0, { vcol: true })); scene.add(farLampMesh);
  if (halos.lists.get('h')) scene.add(new THREE.Mesh(merge(halos.lists.get('h')), haloMaterial(3)));
  // Đèn khí xa: tâm hổ phách rải khắp các phố khác (quầng không bị mái che: đọc như ánh sáng loang trong sương chiều).
  if (halosFar.lists.get('h')) { const hm = haloMaterial(0); hm.depthTest = false; const mesh = new THREE.Mesh(merge(halosFar.lists.get('h')), hm); mesh.renderOrder = 5; scene.add(mesh); }

  // --- Ida rất nhỏ, vác thang, cạnh ngọn đèn số 4 vừa thắp ---
  const mf = charMatFn();
  const ida = buildCharacter(sheets.ida, { material: mf, detail: 12 }); ida.setPose(sheets.ida.poses.walk_ladder);
  { const L = lamps[LIT - 1]; const P = L.P.clone().addScaledVector(L.f.d, 1.3).addScaledVector(L.f.n, -L.side * 0.9); ida.root.position.copy(P);
    ida.root.rotation.y = Math.atan2(L.f.d.x, L.f.d.z); scene.add(ida.root); }

  // --- trời: dải chuyển hồng → tím → chàm, vài dải mây mỏng phẳng ---
  const skyMat = new THREE.ShaderMaterial({
    uniforms: { uSkyA: G.uSkyA, uSkyB: G.uSkyB, uSkyC: G.uSkyC, uSkyD: G.uSkyD, uSunDir: G.uSunDir, uCl: { value: V3(C('#7e6597')) }, uCl2: { value: V3(C('#f0a898')) } },
    vertexShader: 'varying vec3 vD; void main(){ vD = (modelMatrix*vec4(position,1.0)).xyz - cameraPosition; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
    fragmentShader: `uniform vec3 uSkyA, uSkyB, uSkyC, uSkyD, uSunDir, uCl, uCl2; varying vec3 vD;
      ${NOISE_GLSL}
      ${SKY_GLSL}
      void main(){ vec3 d = normalize(vD); vec3 c = skyCol(d);
        float az = atan(d.x, -d.z), el = asin(clamp(d.y, -1.0, 1.0));
        float n = fbm(vec2(az*1.6, el*55.0) + vec2(3.0, 0.0)) * 0.8 + 0.2*vn(vec2(az*9.0, el*140.0));
        float band = smoothstep(0.02, 0.05, el) * (1.0 - smoothstep(0.10, 0.17, el));
        float fw = fwidth(n)*1.2;
        float m1 = smoothstep(0.63 - fw, 0.63 + fw, n) * band;
        float m2 = smoothstep(0.70 - fw, 0.70 + fw, n) * band;
        vec2 hz = normalize(d.xz); float gl = pow(max(dot(hz, normalize(uSunDir.xz)), 0.0), 2.0);
        vec3 cl = mix(uCl, uCl2, 0.35 + 0.65*gl);
        c = mix(c, cl, m1*0.85); c = mix(c, cl*mix(0.82, 1.18, gl), m2*0.9);
        gl_FragColor = vec4(c, 1.0); }`,
    side: THREE.BackSide, depthWrite: false,
  });
  const sky = new THREE.Mesh(new THREE.SphereGeometry(6000, 48, 24), skyMat);
  // Trời tĩnh: vẽ một lần mỗi khung vào ảnh nền (không lặp lại cho từng mẫu tích luỹ) — dải chuyển vẫn đi qua dither/grain.
  const skyScene = new THREE.Scene(); skyScene.add(sky); let skyRT = null;
  const renderSky = () => { if (skyRT || DBG.noSky) return; skyRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.FloatType, format: THREE.RGBAFormat, depthBuffer: true });
    renderer.setRenderTarget(skyRT); renderer.render(skyScene, cam); renderer.setRenderTarget(null); scene.background = skyRT.texture; };

  // --- ánh sáng: trời chạng vạng (bán cầu), dư quang hồng từ phía tây thấp ---
  const hemi = new THREE.HemisphereLight(C('#8a86c8'), C('#1c1a2c'), 0.42);
  const after = new THREE.DirectionalLight(C('#f0a090'), 0.22); after.position.copy(G.uSunDir.value).multiplyScalar(-100).negate();

  // --- máy quay: cao ~38 m, trục chúc xuống ~23°, dịch ống kính dọc để lấy dải trời ---
  const cam = shiftCam(48.8, W / H, 1, 9000, 0.325);
  cam.position.copy(CAMP);
  { const tgt = SF(72).p; const dir = tgt.clone().sub(CAMP); const yaw = Math.atan2(dir.x, -dir.z); const pitch = -21 * Math.PI / 180;
    cam.rotation.set(0, 0, 0); cam.rotation.order = 'YXZ'; cam.rotation.y = -yaw; cam.rotation.x = pitch; cam.updateMatrixWorld(); }
  if (DBG.dbgIda) { const P = ida.root.position; cam.userData.shiftY = 0; cam.fov = 30; cam.updateProjectionMatrix(); cam.position.set(P.x - 8, P.y + 12, P.z + 14); cam.lookAt(P.x, P.y + 1.5, P.z); }

  const apply = () => {
    G.uStep.value = 1.05; G.uOff.value = 0.1; G.uQlo.value = -3.5; G.uQhi.value = 1.2;
    G.uCool.value.set(0.84, 0.88, 1.18); G.uWarm.value.set(1.04, 1.0, 0.94);
    G.uElec.value.set(0, 0, 0, 0); G.uBay.value.set(1.6, 4, 0.9, 0); G.uBounce.value.set(0, 0, 0, 0);
    G.uFog.value.set(0.0012, 80, 0.95, 0); G.uLantAng.value.set(0, 0.7, 0, 0.3);
    renderSky();
    const hs = hemi.color.clone().multiplyScalar(hemi.intensity), hg = hemi.groundColor.clone().multiplyScalar(hemi.intensity), dc = after.color.clone().multiplyScalar(after.intensity);
    FAR.uHs.value.set(hs.r, hs.g, hs.b); FAR.uHg.value.set(hg.r, hg.g, hg.b); FAR.uDc.value.set(dc.r, dc.g, dc.b); FAR.uDd.value.copy(after.position).normalize();
    const lc = C('#ffa04a'); FAR.uLampC.value.set(lc.r, lc.g, lc.b); lampLights.forEach((v, i) => FAR.uLampP.value[i].copy(v));
    pipe.outMat.uniforms.uHalfK.value = 0.2; pipe.outMat.uniforms.uPaperK.value = 0.07; pipe.outMat.uniforms.uVig.value = 0.4;
  };
  return { scene, cam, apply, onSample: null, ink: { K: 70, rmin: 0.5, rmax: 1.9, nt: 0.3, dt: 0.05, fogD: 0.007, wob: 0.8 } };
}

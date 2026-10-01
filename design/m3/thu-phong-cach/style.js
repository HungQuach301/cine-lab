// Cine Lab · M3 THỬ PHONG CÁCH (nhánh thu-phong-cach, KHÔNG merge) — biến thể hình bật bằng cờ dbg.style.
// page.js chỉ nạp mô-đun này khi dbg.style có giá trị; không có cờ → không nạp, không đổi điểm ảnh (kiểm 0 px ở s03, s05, s22).
//   'b3' : 2.5D cắt giấy / bóng — tách lớp theo độ sâu, mảng sáng bậc thang (posterize log), bóng đổ giấy, viền cắt, nhân vật thành bóng,
//          kết cấu giấy THỦ TỤC cố định theo không gian (không đổi theo khung → không nhấp nháy). Bỏ lớp vẽ Kuwahara (thay bằng mảng phẳng).
//   'b1' : toon + viền nét — vật liệu tô 2–3 bậc (MeshToonMaterial, giữ màu/kết cấu gốc), viền theo độ sâu + pháp tuyến, bỏ chi tiết vi mô.
// Mọi tham số có thể ghi đè bằng dbg (vd. dbg.cam = { mm, pos, look }, dbg.exp = hệ số phơi sáng).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { fovOf } from '/cong5/layout/util.js';
import { LAMP_SHOT } from './lamp_shot.js';
import { installB3v2 } from './style_v2.js';

export const EXTRA = [LAMP_SHOT];
export const extraShot = (id) => EXTRA.find((s) => s.id === id) || null;

// B3: đổi cỡ cảnh/máy để tránh cận mặt (lý do ghi trong reports/m3/THU-PHONG-CACH.md).
//  s03 MS thấp-trước → WS 3/4 cạnh, thấp (Ida trên thang thành bóng nhỏ, ngọn L4 nở thành mảng ấm).
//  s05 MCU 3/4 trước (mặt) → MS nghiêng hẳn (profile) từ phía −x: bóng nghiêng Ida + hai lòng tay trước lồng kính sáng.
//  s22 MCU 3/4 (mặt) → MWS thấp từ lòng phố phía −x: bóng Ida đen trên mặt tiền trắng ánh điện; L10 bắt lửa cuối shot.
export const B3_CAM = {
  s03: { mm: 40, pos: [110.6, 1.15, 0.4], look: [106.0, 2.45, -4.4] },
  s05: { mm: 35, pos: [101.4, 2.4, -3.6], look: [106.2, 2.6, -4.45] },
  s22: { mm: 35, pos: [16.2, 1.0, -0.2], look: [22.0, 2.5, -4.6] },
};
// B1: giữ máy gốc (cờ chỉ đổi shader + hậu kỳ).

const VS = `in vec3 position; out vec2 vUv; void main(){ vUv = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }`;
const HDR = `precision highp float; in vec2 vUv; out vec4 o;
float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
  return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
float lum(vec3 c){ return dot(c, vec3(0.2126,0.7152,0.0722)); }
`;

// G-buffer: r = độ sâu nhìn (m), g = nhân vật (1), b = tấm số liệu (1), a = 1. Vật liệu phẳng, có khối skinning để an toàn.
function gMaterial(id) {
  return new THREE.ShaderMaterial({
    vertexShader: `#include <common>
      #include <morphtarget_pars_vertex>
      #include <skinning_pars_vertex>
      varying float vZ;
      void main(){
        #include <skinbase_vertex>
        #include <begin_vertex>
        #include <morphtarget_vertex>
        #include <skinning_vertex>
        #include <project_vertex>
        vZ = -mvPosition.z; }`,
    fragmentShader: `varying float vZ; void main(){ gl_FragColor = vec4(vZ, ${id === 1 ? '1.0' : '0.0'}, ${id === 2 ? '1.0' : '0.0'}, 1.0); }`,
    side: THREE.DoubleSide });
}
// G-buffer pháp tuyến (B1): rgb = pháp tuyến không gian nhìn, a = độ sâu.
function nMaterial() {
  return new THREE.ShaderMaterial({
    vertexShader: `#include <common>
      #include <morphtarget_pars_vertex>
      #include <skinning_pars_vertex>
      varying float vZ; varying vec3 vN;
      void main(){
        #include <beginnormal_vertex>
        #include <morphnormal_vertex>
        #include <skinbase_vertex>
        #include <skinnormal_vertex>
        #include <defaultnormal_vertex>
        #include <begin_vertex>
        #include <morphtarget_vertex>
        #include <skinning_vertex>
        #include <project_vertex>
        vN = normalize(transformedNormal); vZ = -mvPosition.z; }`,
    fragmentShader: `varying float vZ; varying vec3 vN; void main(){ vec3 n = normalize(vN); if (!gl_FrontFacing) n = -n; gl_FragColor = vec4(n, vZ); }`,
    side: THREE.DoubleSide });
}

export function install(o) {
  if (o.style === 'b3') return installB3(o);
  if (o.style === 'b3v2') return installB3v2(o, { common, gMaterial, B3_CAM, HDR });   // B3 v2 (sửa sau kiểm mù Mốc 1) — tệp riêng, B3 v1/B1 không đổi
  if (o.style === 'b1') return installB1(o);
  throw new Error('dbg.style không hợp lệ: ' + o.style);
}

function common(o) {
  const { THREE: _T, renderer, W, H } = o;
  const fOpt = { type: THREE.FloatType, format: THREE.RGBAFormat, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, colorSpace: THREE.LinearSRGBColorSpace };
  const rt = (w, h, x = {}) => new THREE.WebGLRenderTarget(Math.max(1, Math.round(w)), Math.max(1, Math.round(h)), { ...fOpt, ...x });
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)); const qs = new THREE.Scene(); qs.add(quad);
  const mk = (fs, uniforms) => new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, vertexShader: VS, fragmentShader: HDR + fs, uniforms, depthTest: false, depthWrite: false });
  const run = (m, target) => { quad.material = m; renderer.setRenderTarget(target); renderer.render(qs, cam); };
  // máy quay thay thế (B3) — đặt lại mỗi khung sau update của shot
  const camOv = (o.dbg && o.dbg.cam) || (o.camTable && o.camTable[o.shot.id]) || null;
  const applyCam = () => { if (!camOv) return; const c = o.cur.cam; c.fov = fovOf(camOv.mm); c.updateProjectionMatrix(); c.position.set(...camOv.pos); c.lookAt(...camOv.look); };
  // vẽ G-buffer: thay vật liệu theo nhóm (nhân vật / tấm số liệu / còn lại), ẩn sprite
  function gbuffer(target, mats, scene, camera, clear = [0, 0, 0, 0]) {
    const charSet = new Set(); for (const ch of Object.values(o.cur.named || {})) if (ch && ch.root) ch.root.traverse((x) => { if (x.isMesh) charSet.add(x); });
    const saved = [];
    scene.traverse((x) => {
      if (x.isSprite || x.isPoints || x.isLine || x.userData.noG) { saved.push([x, 'v', x.visible]); x.visible = false; return; }
      if (!x.isMesh) return;
      let id = charSet.has(x) ? 1 : 0; for (let p = x; p && !id; p = p.parent) if (p.userData.tpcData) id = 2;
      saved.push([x, 'm', x.material]); x.material = mats[id];
    });
    const bg = scene.background, fog = scene.fog; scene.background = null; scene.fog = null;
    renderer.setRenderTarget(target); renderer.setClearColor(new THREE.Color(clear[0], clear[1], clear[2]), clear[3]); renderer.clear(); renderer.render(scene, camera);
    scene.background = bg; scene.fog = fog;
    for (const [x, k, v] of saved) { if (k === 'v') x.visible = v; else x.material = v; }
  }
  return { fOpt, rt, mk, run, applyCam, gbuffer };
}

// ======================================================= B3 =======================================================
function installB3(o) {
  const { renderer, pipe, cur, W, H } = o, dbg = o.dbg || {};
  const C = common({ ...o, camTable: B3_CAM });
  const S = W / 960, GS = W >= 1920 ? 1 : 2;   // G-buffer siêu lấy mẫu 2× ở 960/1280 (viền bóng mịn), 1× ở 1920
  const gRT = new THREE.WebGLRenderTarget(W * GS, H * GS, { ...C.fOpt, depthBuffer: true });
  const gM = [gMaterial(0), gMaterial(1), gMaterial(2)];
  const hA = C.rt(W / 2, H / 2), hB = C.rt(W / 2, H / 2), outRT = C.rt(W, H);
  const P = Object.assign({ step: 0.85, soft: 0.07, e0: -0.2, detK: 0.32, sat: 0.82, shK: 0.55, shLen: 9.0, edgeK: 0.35, papK: 0.10, inkK: 1.0, eLo: -2.2, eHi: 0.6, rimK: 0.85 }, dbg.b3 || {});
  const down = C.mk(`uniform sampler2D tSrc; uniform vec2 px; void main(){ vec3 s = vec3(0.0);
      for (int j=-1;j<=1;j++) for (int i=-1;i<=1;i++) s += texture(tSrc, vUv + vec2(i,j)*px).rgb; o = vec4(s/9.0, 1.0); }`,
    { tSrc: { value: null }, px: { value: new THREE.Vector2(1 / W, 1 / H) } });
  const blur = C.mk(`uniform sampler2D tSrc; uniform vec2 dir; uniform float sig;
      void main(){ vec4 s = vec4(0.0); float ws = 0.0;
        for (int k=-6; k<=6; k++){ float x = float(k); float w = exp(-0.5*x*x/(sig*sig)); s += texture(tSrc, vUv + dir*x) * w; ws += w; }
        o = s/ws; }`, { tSrc: { value: null }, dir: { value: new THREE.Vector2() }, sig: { value: P.blur ?? 1.0 } });
  const sty = C.mk(`uniform sampler2D tSrc, tBlur, tG; uniform vec2 px, camOff; uniform float S, fpx, uExp;
    uniform float step_, soft, e0, detK, sat, shK, shLen, edgeK, papK, inkK, eLo, eHi, rimK;
    float zAt(vec2 uv){ float z = texture(tG, uv).r; return z > 0.0 ? z : 1.0e4; }
    float stair(float e){ float x = e / step_; float b = floor(x); return step_ * (b + smoothstep(0.5 - soft, 0.5 + soft, fract(x))); }
    float paper(vec2 p){
      float n = 0.42*vn(p/1.7) + 0.26*vn(p/5.0 + 3.1) + 0.18*vn(p/19.0 + 8.3) + 0.14*vn(p/61.0 + 1.7);
      float fib = vn(vec2(p.x*0.55 + p.y*0.21, p.y*0.06 - p.x*0.018) + 4.4);         // fibre kéo dài
      return n + 0.22*(smoothstep(0.62, 0.9, fib) - 0.1); }
    void main(){
      vec2 fp = gl_FragCoord.xy / S;
      vec2 wv = (vec2(vn(fp/7.0), vn(fp/7.0 + 7.7)) - 0.5) * 1.6 + (vec2(vn(fp/31.0 + 3.0), vn(fp/31.0 + 9.0)) - 0.5) * 2.4;   // viền cắt tay (px)
      vec2 uvw = vUv + wv * S * px;
      vec4 g = texture(tG, uvw); float z = g.r > 0.0 ? g.r : 1.0e4; float ch = g.g, dat = g.b;
      vec3 src = texture(tSrc, vUv).rgb, bl = texture(tBlur, vUv).rgb;
      float Ls = lum(src), Lb = max(lum(bl), 1e-7);
      float e = log2(max(Lb * uExp, 1e-6)), q = stair(e - e0) + e0, gain = exp2(q - e);
      vec3 chroma = mix(vec3(1.0), bl / Lb, sat);
      float hiB = smoothstep(eLo, eHi, q);
      vec3 tint = mix(vec3(0.80, 0.86, 1.18), vec3(1.12, 0.98, 0.80), hiB);           // bóng: mực lam; sáng: hổ phách
      vec3 flatC = chroma * exp2(q) / uExp * tint;
      float det = clamp(Ls / Lb, 0.55, 1.6);
      vec3 c = flatC * mix(1.0, det, detK);
      if (dat > 0.5) c = src * gain * tint;                                          // tấm số liệu: giữ nét chữ, chỉ bậc thang ánh sáng
      // nhân vật thành bóng cắt giấy: mực tối; mép được ánh đèn chạm giữ một viền sáng ấm
      if (ch > 0.01) {
        float m = 1.0; for (int i = 0; i < 6; i++) { float a = float(i) * 1.0472; m = min(m, texture(tG, uvw + vec2(cos(a), sin(a)) * 1.7 * S * px).g); }
        float rim = 1.0 - smoothstep(0.2, 0.9, m);
        float lit = smoothstep(-1.2, 0.6, log2(max(Ls * uExp, 1e-6)));
        vec3 ink = vec3(0.0105, 0.0085, 0.0135) * inkK, warm = vec3(0.060, 0.030, 0.014);
        vec3 sil = mix(ink, warm, 0.35 * lit) / uExp;
        sil = mix(sil, vec3(1.0, 0.62, 0.30) * lum(flatC) * 1.15, rimK * rim * lit);
        c = mix(c, sil, clamp(ch, 0.0, 1.0));
      }
      // bóng đổ giấy: lớp gần hơn ở phía trên-trái → đổ bóng mềm xuống-phải lên lớp sau
      float sh = 0.0, wsum = 0.0; vec2 sd = normalize(vec2(1.0, -1.0));
      for (int i = 1; i <= 5; i++) { float l = float(i) / 5.0; float zq = zAt(uvw - sd * l * shLen * S * px); float w = 1.2 - l; sh += w * step(zq, z * 0.8); wsum += w; }
      c *= 1.0 - shK * clamp(sh / wsum * 1.6, 0.0, 1.0) * (1.0 - 0.6 * ch);
      // viền cắt: mép lớp hướng về ánh (phía trên-trái là lớp xa hơn) → chỉ giấy sáng mảnh
      float zn = zAt(uvw - sd * 1.6 * S * px); float edge = step(z * 1.3, zn) * (1.0 - ch);
      c += edge * edgeK * flatC;
      // kết cấu giấy thủ tục: cố định theo không gian thế giới (bù trượt máy theo độ sâu), mỗi lớp một tờ khác
      float k = floor(clamp(log2(z / 1.25) * 1.1, 0.0, 9.0));
      vec2 tp = fp + camOff * fpx / min(z, 400.0) / S + vec2(k * 37.0, k * 91.0);
      c *= 1.0 + papK * (paper(tp) - 0.5) * 2.0;
      o = vec4(max(c, 0.0), 1.0); }`,
    { tSrc: { value: null }, tBlur: { value: hA.texture }, tG: { value: gRT.texture }, px: { value: new THREE.Vector2(1 / W, 1 / H) }, camOff: { value: new THREE.Vector2() },
      S: { value: S }, fpx: { value: 0 }, uExp: { value: 1 },
      step_: { value: P.step }, soft: { value: P.soft }, e0: { value: P.e0 }, detK: { value: P.detK }, sat: { value: P.sat }, shK: { value: P.shK }, shLen: { value: P.shLen },
      edgeK: { value: P.edgeK }, papK: { value: P.papK }, inkK: { value: P.inkK }, eLo: { value: P.eLo }, eHi: { value: P.eHi }, rimK: { value: P.rimK } });
  // grade: bỏ lớp "vải canvas" của hướng C (kết cấu giấy thay thế), giữ vignette
  const u = pipe.outMat.uniforms; u.gCanvas.value = 0;
  let cam0 = null; const right = new THREE.Vector3(), up = new THREE.Vector3(), d = new THREE.Vector3();
  return {
    noPaint: true,
    frame(t, T, f) { C.applyCam(); if (dbg.exp) u.uExp.value *= dbg.exp; if (o.shot.b3exp) u.uExp.value = o.shot.b3exp(t, T); },
    post() {
      const cam = cur.cam; cam.updateMatrixWorld(true);
      if (!cam0) cam0 = cam.position.clone();
      right.setFromMatrixColumn(cam.matrixWorld, 0); up.setFromMatrixColumn(cam.matrixWorld, 1); d.copy(cam.position).sub(cam0);
      sty.uniforms.camOff.value.set(d.dot(right), d.dot(up)); sty.uniforms.fpx.value = (H / 2) / Math.tan(cam.fov * Math.PI / 360);
      C.gbuffer(gRT, gM, cur.scene, cam);
      down.uniforms.tSrc.value = pipe.accRT.texture; C.run(down, hA);
      blur.uniforms.tSrc.value = hA.texture; blur.uniforms.dir.value.set(2 / W, 0); C.run(blur, hB);
      blur.uniforms.tSrc.value = hB.texture; blur.uniforms.dir.value.set(0, 2 / H); C.run(blur, hA);
      sty.uniforms.tSrc.value = pipe.accRT.texture; sty.uniforms.uExp.value = u.uExp.value;
      C.run(sty, outRT); renderer.setRenderTarget(null);
      u.tAcc.value = outRT.texture;
    },
  };
}

// ======================================================= B1 =======================================================
// Toon: thay vật liệu Lambert/Standard/Phong bằng MeshToonMaterial (cùng màu, map, emissive), gradientMap 3 bậc (B1_STEPS).
// Viền: G-buffer pháp tuyến + độ sâu → Sobel trên độ sâu (tương đối) và pháp tuyến → nét mực. Bỏ lớp vẽ Kuwahara (mảng phẳng của toon thay thế).
function installB1(o) {
  const { renderer, pipe, cur, W, H } = o, dbg = o.dbg || {};
  const C = common({ ...o, camTable: null });
  const P = Object.assign({ steps: [0.16, 0.55, 1.0], lineK: 0.85, lineW: 1.0, zTh: 0.06, nTh: 0.45, charSteps: [0.30, 0.68, 1.0], flatSkin: 0.65 }, dbg.b1 || {});
  const grad = (st) => { const n = st.length, data = new Uint8Array(n * 4); st.forEach((v, i) => { const b = Math.round(255 * v); data.set([b, b, b, 255], i * 4); });
    const t = new THREE.DataTexture(data, n, 1, THREE.RGBAFormat); t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t; };
  const gEnv = grad(P.steps), gChar = grad(P.charSteps);
  const charSet = new Set(); for (const ch of Object.values(cur.named || {})) if (ch && ch.root) ch.root.traverse((x) => { if (x.isMesh) charSet.add(x); });
  const cache = new Map();
  cur.scene.traverse((x) => {
    if (!x.isMesh || !x.material) return;
    const swap = (m) => {
      if (!m || !(m.isMeshLambertMaterial || m.isMeshStandardMaterial || m.isMeshPhongMaterial || m.isMeshPhysicalMaterial)) return m;
      const key = m.uuid + (charSet.has(x) ? 'c' : 'e'); if (cache.has(key)) return cache.get(key);
      const t = new THREE.MeshToonMaterial({ color: m.color, map: m.map || null, emissive: m.emissive || new THREE.Color(0), emissiveMap: m.emissiveMap || null, emissiveIntensity: m.emissiveIntensity ?? 1,
        transparent: m.transparent, opacity: m.opacity, side: m.side, alphaTest: m.alphaTest, vertexColors: m.vertexColors, fog: m.fog, depthWrite: m.depthWrite,
        gradientMap: charSet.has(x) ? gChar : gEnv });
      if (charSet.has(x) && t.map && P.flatSkin > 0) t.map = t.map;   // kết cấu giữ; chi tiết vi mô bị nén bởi bậc tô + lọc mảng ở hậu kỳ
      t.name = (m.name || '') + '_toon'; cache.set(key, t); return t;
    };
    x.material = Array.isArray(x.material) ? x.material.map(swap) : swap(x.material);
  });
  const GS = W >= 1920 ? 1 : 2;
  const nRT = new THREE.WebGLRenderTarget(W * GS, H * GS, { ...C.fOpt, depthBuffer: true });
  const nM = nMaterial(); const nMs = [nM, nM, nM];
  const outRT = C.rt(W, H), hA = C.rt(W / 2, H / 2), hB = C.rt(W / 2, H / 2);
  const down = C.mk(`uniform sampler2D tSrc; uniform vec2 px; void main(){ vec3 s = vec3(0.0);
      for (int j=-1;j<=1;j++) for (int i=-1;i<=1;i++) s += texture(tSrc, vUv + vec2(i,j)*px).rgb; o = vec4(s/9.0, 1.0); }`, { tSrc: { value: null }, px: { value: new THREE.Vector2(1 / W, 1 / H) } });
  const blur = C.mk(`uniform sampler2D tSrc; uniform vec2 dir; uniform float sig;
      void main(){ vec4 s = vec4(0.0); float ws = 0.0;
        for (int k=-6; k<=6; k++){ float x = float(k); float w = exp(-0.5*x*x/(sig*sig)); s += texture(tSrc, vUv + dir*x) * w; ws += w; }
        o = s/ws; }`, { tSrc: { value: null }, dir: { value: new THREE.Vector2() }, sig: { value: 1.6 } });
  const ink = C.mk(`uniform sampler2D tSrc, tN, tBlur; uniform vec2 px; uniform float S, lineK, lineW, zTh, nTh, flatSkin;
    vec4 N(vec2 d){ vec4 v = texture(tN, vUv + d * lineW * S * px); if (v.a <= 0.0) v = vec4(0.0, 0.0, 1.0, 1.0e4); return v; }
    void main(){
      vec4 c0 = N(vec2(0)), a = N(vec2(-1, 0)), b = N(vec2(1, 0)), cU = N(vec2(0, 1)), dD = N(vec2(0, -1)), e1 = N(vec2(-1,-1)), e2 = N(vec2(1,1)), e3 = N(vec2(-1,1)), e4 = N(vec2(1,-1));
      float z = c0.a;
      float dz = (abs(a.a + b.a - 2.0*z) + abs(cU.a + dD.a - 2.0*z) + 0.5*abs(e1.a + e2.a - 2.0*z) + 0.5*abs(e3.a + e4.a - 2.0*z)) / max(z, 0.05);
      float dn = (1.0 - dot(c0.xyz, a.xyz)) + (1.0 - dot(c0.xyz, b.xyz)) + (1.0 - dot(c0.xyz, cU.xyz)) + (1.0 - dot(c0.xyz, dD.xyz));
      float fade = 1.0 - smoothstep(25.0, 90.0, z);                     // nét mảnh dần ở xa (tránh rối)
      float line = max(smoothstep(zTh, zTh * 2.5, dz), smoothstep(nTh, nTh * 1.8, dn) * fade);
      vec3 s = texture(tSrc, vUv).rgb, bl = texture(tBlur, vUv).rgb;
      float Ls = lum(s), Lb = max(lum(bl), 1e-7);
      vec3 c = mix(s, bl * clamp(Ls / Lb, 0.8, 1.25), flatSkin * 0.5);    // mảng màu có kiểm soát: nén chi tiết vi mô, giữ bậc tô
      vec3 inkC = c * 0.08 + vec3(0.002, 0.0015, 0.003);
      o = vec4(mix(c, inkC, lineK * line), 1.0); }`,
    { tSrc: { value: null }, tN: { value: nRT.texture }, tBlur: { value: hA.texture }, px: { value: new THREE.Vector2(1 / W, 1 / H) }, S: { value: W / 960 },
      lineK: { value: P.lineK }, lineW: { value: P.lineW }, zTh: { value: P.zTh }, nTh: { value: P.nTh }, flatSkin: { value: P.flatSkin } });
  const u = pipe.outMat.uniforms; u.gCanvas.value = 0;
  return {
    noPaint: true,
    frame() { C.applyCam(); if (dbg.exp) u.uExp.value *= dbg.exp; },
    post() {
      cur.cam.updateMatrixWorld(true);
      C.gbuffer(nRT, nMs, cur.scene, cur.cam, [0, 0, 0, 0]);
      down.uniforms.tSrc.value = pipe.accRT.texture; C.run(down, hA);
      blur.uniforms.tSrc.value = hA.texture; blur.uniforms.dir.value.set(2 / W, 0); C.run(blur, hB);
      blur.uniforms.tSrc.value = hB.texture; blur.uniforms.dir.value.set(0, 2 / H); C.run(blur, hA);
      ink.uniforms.tSrc.value = pipe.accRT.texture; C.run(ink, outRT); renderer.setRenderTarget(null);
      u.tAcc.value = outRT.texture;
    },
  };
}

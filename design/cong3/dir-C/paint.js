// Cine Lab · Cổng 3 · Hướng C "Painted Glow" — lớp hậu kỳ "vẽ" chạy SAU accumulate, TRƯỚC pass cuối của shared/post.js.
// Toàn bộ trong Float32 tuyến tính; kết quả ghi vào outRT rồi trỏ outMat.uniforms.tAcc sang outRT, nên tone map,
// grade, grain và dither vẫn là của đường ống chung (không đổi GRAIN).
// Các bước (một lần cho mỗi khung, không phải mỗi mẫu):
//  1) G-buffer: độ sâu nhìn (m) + mặt nạ "quan trọng" (mặt/tay/nguồn sáng) → quyết định bán kính nét cọ.
//  2) Tensor cấu trúc (Sobel trên độ sáng nén) + làm mịn Gauss → hướng và độ dị hướng cục bộ.
//  3) Lọc Kuwahara dị hướng, trọng số đa thức 8 cung (Kyprianidis 2010), lấy mẫu thưa theo xoắn ốc vàng trong elip.
//     Bán kính tăng theo độ sâu, giảm ở vùng quan trọng → chi tiết tập trung ở mặt/tay/nguồn sáng.
//  4) Vân nét cọ: nhiễu kéo dài theo hướng tiếp tuyến (ngắn, yếu; không xoáy).
//  5) Bloom nhiều tầng + halation ấm quanh vùng rất sáng (lửa, kính đèn).
import * as THREE from '../shared/node_modules/three/build/three.module.js';

const VS = `in vec3 position; out vec2 vUv; void main(){ vUv = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }`;
const HDR = `precision highp float; in vec2 vUv; out vec4 o;`;

export function createPaint(renderer, W, H, pipe, P = {}) {
  const S = W / 1920; // thang điểm ảnh theo độ phân giải
  const prm = Object.assign({ rNear: 3.0, rFar: 7.0, dNear: 3, dFar: 60, impScale: 0.35, hard: 8.0, q: 8.0,
    stroke: 0.035, strokeLen: 30, strokeWid: 5, bloom: 0.06, bloomWide: 0.05, halation: 0.10, thr: 1.2, ns: 28, detail: 0.35, preAmp: 0.12, preHue: 0.06, preLen: 36, preWid: 7, wob: 3.0 }, P);
  const fOpt = { type: THREE.FloatType, format: THREE.RGBAFormat, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, colorSpace: THREE.LinearSRGBColorSpace };
  const rt = (w, h) => new THREE.WebGLRenderTarget(Math.max(1, Math.round(w)), Math.max(1, Math.round(h)), fOpt);
  const gRT = new THREE.WebGLRenderTarget(W, H, { ...fOpt, depthBuffer: true, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
  const tA = rt(W / 2, H / 2), tB = rt(W / 2, H / 2), paintRT = rt(W / 2, H / 2), outRT = rt(W, H); // Kuwahara xuất ở nửa độ phân giải (nét cọ ≥ 2 px), ghép lại ở full
  const NL = 6; const down = [], up = [];
  for (let i = 0; i < NL; i++) { down.push(rt(W / 2 ** (i + 1), H / 2 ** (i + 1))); up.push(rt(W / 2 ** (i + 1), H / 2 ** (i + 1))); }

  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)); const qs = new THREE.Scene(); qs.add(quad);
  const mk = (fs, uniforms) => new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, vertexShader: VS, fragmentShader: HDR + fs, uniforms, depthTest: false, depthWrite: false });
  const prof = {}; let profOn = false; const _px = new Float32Array(4);
  const sync = (t) => { renderer.readRenderTargetPixels(t, 0, 0, 1, 1, _px); };
  const run = (m, target, tag) => { const t0 = profOn ? performance.now() : 0; quad.material = m; renderer.setRenderTarget(target); renderer.render(qs, cam);
    if (profOn) { sync(target); prof[tag || 'misc'] = (prof[tag || 'misc'] || 0) + performance.now() - t0; } };

  // --- 1) G-buffer ---
  const gVS = `varying float vZ; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vZ = -mv.z; gl_Position = projectionMatrix * mv; }`;
  const gMat = (imp) => new THREE.ShaderMaterial({ vertexShader: gVS, fragmentShader: `varying float vZ; void main(){ gl_FragColor = vec4(vZ, ${imp.toFixed(2)}, 0.0, 1.0); }`, side: THREE.DoubleSide });
  const gM = [gMat(0), gMat(1)];

  // --- 2) tensor ---
  const tensor = mk(`uniform sampler2D tSrc; uniform vec2 px;
    float L(vec2 d){ vec3 c = texture(tSrc, vUv + d*px*1.5).rgb; float l = dot(c, vec3(0.2126,0.7152,0.0722)); return l/(1.0+l); }
    void main(){
      float a=L(vec2(-1,-1)), b=L(vec2(0,-1)), c=L(vec2(1,-1)), d=L(vec2(-1,0)), f=L(vec2(1,0)), g=L(vec2(-1,1)), h=L(vec2(0,1)), i=L(vec2(1,1));
      float gx = (c + 2.0*f + i - a - 2.0*d - g) * 0.25, gy = (g + 2.0*h + i - a - 2.0*b - c) * 0.25;
      o = vec4(gx*gx, gx*gy, gy*gy, 1.0); }`, { tSrc: { value: null }, px: { value: new THREE.Vector2(1 / W, 1 / H) } });
  const blur = mk(`uniform sampler2D tSrc; uniform vec2 dir; uniform float sig;
    void main(){ vec4 s = vec4(0.0); float ws = 0.0;
      for (int k=-4; k<=4; k++){ float x = float(k); float w = exp(-0.5*x*x/(sig*sig)); s += texture(tSrc, vUv + dir*x) * w; ws += w; }
      o = s/ws; }`, { tSrc: { value: null }, dir: { value: new THREE.Vector2() }, sig: { value: 2.5 } });

  // --- 2b) "lớp lót" trước khi lọc: nhiễu kéo dài theo hướng cấu trúc (hoặc theo trường hướng tần số thấp ở vùng phẳng),
  //     điều chế độ sáng và nhiệt độ màu vài %. Kuwahara biến nhiễu này thành các vệt/mảng cọ có biên — "nét cọ".
  const pre = mk(`uniform sampler2D tSrc, tTen, tG; uniform float amp, hueAmp, sLen, sWid, S;
    float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
    float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
      return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
    // Nét cọ thẳng: trộn 3 hướng cố định (trọng số theo trường chậm) + hướng cấu trúc nơi có cạnh. Không xoay toạ độ theo điểm → không xoáy.
    float sdir(vec2 fp, vec2 d, float L, float Wd, float seed){ vec2 q = vec2(dot(fp, d) / L, dot(fp, vec2(-d.y, d.x)) / Wd); return vn(q + seed) * 0.65 + vn(q * 2.07 + seed + 11.3) * 0.35; }
    float strokes(vec2 fp, vec2 dir, float A, float L, float Wd){
      vec3 w = vec3(vn(fp / 160.0), vn(fp / 160.0 + 17.0), vn(fp / 160.0 + 41.0)); w = w*w*w; w /= (w.x + w.y + w.z);
      float nf = w.x * sdir(fp, vec2(0.866, 0.5), L, Wd, 0.0) + w.y * sdir(fp, vec2(0.259, 0.966), L, Wd, 5.0) + w.z * sdir(fp, vec2(0.966, -0.259), L, Wd, 9.0);
      float ns = sdir(fp, dir, L, Wd, 13.0);
      return mix(nf, ns, smoothstep(0.1, 0.5, A));
    }
    uniform float wob; uniform vec2 px;
    void main(){
      vec2 fp0 = gl_FragCoord.xy / S;
      float imp0 = texture(tG, vUv).y;
      // nét "tay vẽ": lệch toạ độ lấy mẫu vài px theo nhiễu chậm → cạnh thẳng hình học thành cạnh vẽ tay
      vec2 wv = vec2(vn(fp0 / 90.0) - 0.5, vn(fp0 / 90.0 + 19.7) - 0.5) + 0.35 * vec2(vn(fp0 / 26.0 + 3.1) - 0.5, vn(fp0 / 26.0 + 8.3) - 0.5);
      vec2 uvw = vUv + wv * 2.0 * wob * S * (1.0 - 0.6 * imp0) * px;
      vec3 c = texture(tSrc, uvw).rgb;
      vec3 t = texture(tTen, vUv).xyz;
      float dd = sqrt(max((t.x-t.z)*(t.x-t.z) + 4.0*t.y*t.y, 0.0));
      float l1 = 0.5*(t.x+t.z+dd), l2 = 0.5*(t.x+t.z-dd);
      vec2 v = vec2(l1 - t.x, -t.y); vec2 dir = dot(v,v) > 1e-14 ? normalize(v) : vec2(1.0, 0.0);
      float A = (l1+l2 > 1e-10) ? (l1-l2)/(l1+l2) : 0.0;
      vec2 fp = gl_FragCoord.xy / S;
      float n = strokes(fp, dir, A, sLen, sWid);
      vec2 q = fp / vec2(sLen, sWid);
      float n2 = vn(q * 0.5 + 37.0);
      float imp = texture(tG, vUv).y;
      float k = 1.0 - 0.5 * imp;
      c *= 1.0 + amp * k * (n - 0.5) * 2.0;
      c *= 1.0 + hueAmp * k * (n2 - 0.5) * 2.0 * vec3(1.0, -0.2, -1.0);   // ấm/lạnh xen nhau: "màu vỡ"
      o = vec4(max(c, 0.0), 1.0); }`, { tSrc: { value: null }, tTen: { value: null }, tG: { value: gRT.texture }, amp: { value: prm.preAmp }, hueAmp: { value: prm.preHue },
    sLen: { value: prm.preLen }, sWid: { value: prm.preWid }, S: { value: S }, wob: { value: prm.wob }, px: { value: new THREE.Vector2(1 / W, 1 / H) } });
  const preRT = rt(W, H);

  // --- 3) Kuwahara dị hướng (trọng số đa thức), mẫu thưa ---
  const NS = prm.ns;
  const kuwa = mk(`uniform sampler2D tSrc, tTen, tG; uniform vec2 px; uniform float rNear, rFar, dNear, dFar, impScale, hard, qq, S;
    const int NS = ${NS};
    vec3 enc(vec3 c){ return c/(1.0+c); }
    vec3 dec(vec3 e){ e = min(e, vec3(0.9995)); return e/(1.0-e); }
    void main(){
      vec3 t = texture(tTen, vUv).xyz;
      float dd = sqrt(max((t.x-t.z)*(t.x-t.z) + 4.0*t.y*t.y, 0.0));
      float l1 = 0.5*(t.x+t.z+dd), l2 = 0.5*(t.x+t.z-dd);
      vec2 v = vec2(l1 - t.x, -t.y);
      vec2 dir = dot(v,v) > 1e-14 ? normalize(v) : vec2(0.0,1.0);
      float A = (l1+l2 > 1e-10) ? (l1-l2)/(l1+l2) : 0.0;
      vec4 g = texture(tG, vUv);
      float depth = g.x > 0.0 ? g.x : dFar;
      float r = S * mix(rNear, rFar, smoothstep(dNear, dFar, depth)) * mix(1.0, impScale, g.y);
      float a = r * clamp(1.0 + A, 0.1, 2.0), b = r * clamp(1.0/(1.0 + A), 0.1, 2.0);
      vec2 ax = dir * a * px, ay = vec2(-dir.y, dir.x) * b * px;
      const float zeta = 0.33; const float eta = (zeta + 0.9238795) / 0.1464466;
      vec3 m[8]; vec3 s[8]; float w[8]; float ws[8];
      for (int k=0;k<8;k++){ m[k]=vec3(0.0); s[k]=vec3(0.0); ws[k]=0.0; }
      vec3 c0 = enc(texture(tSrc, vUv).rgb);
      for (int i=0;i<NS;i++){
        float fi = float(i) + 0.5; float rr = sqrt(fi/float(NS)); float th = fi * 2.3999632;
        vec2 p = rr * vec2(cos(th), sin(th));
        vec3 c = enc(texture(tSrc, vUv + ax*p.x + ay*p.y).rgb); vec3 cc = c*c;
        vec2 q = p; float xx = zeta - eta*q.x*q.x, yy = zeta - eta*q.y*q.y, z, sum = 0.0;
        z = max(0.0, q.y + xx); w[0] = z*z; sum += w[0];
        z = max(0.0, -q.x + yy); w[2] = z*z; sum += w[2];
        z = max(0.0, -q.y + xx); w[4] = z*z; sum += w[4];
        z = max(0.0, q.x + yy); w[6] = z*z; sum += w[6];
        q = 0.70710678 * vec2(p.x - p.y, p.x + p.y);
        xx = zeta - eta*q.x*q.x; yy = zeta - eta*q.y*q.y;
        z = max(0.0, q.y + xx); w[1] = z*z; sum += w[1];
        z = max(0.0, -q.x + yy); w[3] = z*z; sum += w[3];
        z = max(0.0, -q.y + xx); w[5] = z*z; sum += w[5];
        z = max(0.0, q.x + yy); w[7] = z*z; sum += w[7];
        float gw = exp(-2.0*rr*rr) / max(sum, 1e-6);
        for (int k=0;k<8;k++){ float wk = w[k]*gw; m[k] += c*wk; s[k] += cc*wk; ws[k] += wk; }
      }
      vec3 outc = vec3(0.0); float wt = 0.0;
      for (int k=0;k<8;k++){
        if (ws[k] <= 1e-6) continue;
        vec3 mk = m[k]/ws[k]; vec3 sk = abs(s[k]/ws[k] - mk*mk);
        float sg = sk.r + sk.g + sk.b;
        float wk = 1.0 / (1.0 + pow(hard*1000.0*sg, 0.5*qq));
        outc += mk*wk; wt += wk;
      }
      vec3 e = wt > 0.0 ? outc/wt : c0;
      o = vec4(dec(e), 1.0);
    }`, { tSrc: { value: null }, tTen: { value: null }, tG: { value: gRT.texture }, px: { value: new THREE.Vector2(1 / W, 1 / H) },
    rNear: { value: prm.rNear }, rFar: { value: prm.rFar }, dNear: { value: prm.dNear }, dFar: { value: prm.dFar }, impScale: { value: prm.impScale },
    hard: { value: prm.hard }, qq: { value: prm.q }, S: { value: S } });

  // --- 5) bloom: 13 mẫu xuống (Jimenez), lều 9 mẫu lên ---
  const downM = mk(`uniform sampler2D tSrc; uniform vec2 px; uniform float thr; uniform float first;
    vec3 T(vec2 d){ return texture(tSrc, vUv + d*px).rgb; }
    void main(){
      vec3 a=T(vec2(-2,-2)), b=T(vec2(0,-2)), c=T(vec2(2,-2)), d=T(vec2(-1,-1)), e=T(vec2(1,-1)), f=T(vec2(-2,0)), g=T(vec2(0,0)),
           h=T(vec2(2,0)), i=T(vec2(-1,1)), j=T(vec2(1,1)), k=T(vec2(-2,2)), l=T(vec2(0,2)), m=T(vec2(2,2));
      vec3 s = (d+e+i+j)*0.125 + (a+b+f+g)*0.03125 + (b+c+g+h)*0.03125 + (f+g+k+l)*0.03125 + (g+h+l+m)*0.03125;
      if (first > 0.5) { float L = dot(s, vec3(0.2126,0.7152,0.0722)); s *= 1.0 / (1.0 + 0.02*L); } // chống đốm lửa
      o = vec4(s, 1.0); }`, { tSrc: { value: null }, px: { value: new THREE.Vector2() }, thr: { value: prm.thr }, first: { value: 0 } });
  const upM = mk(`uniform sampler2D tSrc, tAdd; uniform vec2 px;
    vec3 T(vec2 d){ return texture(tSrc, vUv + d*px).rgb; }
    void main(){
      vec3 s = T(vec2(0,0))*4.0 + (T(vec2(-1,0))+T(vec2(1,0))+T(vec2(0,-1))+T(vec2(0,1)))*2.0 + T(vec2(-1,-1))+T(vec2(1,-1))+T(vec2(-1,1))+T(vec2(1,1));
      o = vec4(s/16.0 + texture(tAdd, vUv).rgb, 1.0); }`, { tSrc: { value: null }, tAdd: { value: null }, px: { value: new THREE.Vector2() } });

  // --- 4 + 5) ghép: nét cọ + bloom + halation ---
  const comp = mk(`uniform sampler2D tSrc, tOrig, tTen, tG, tB0, tB3; uniform vec2 res; uniform float detail, stroke, sLen, sWid, bloom, bloomWide, halation, thr, S;
    float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
    float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f);
      return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
    // Nét cọ thẳng: trộn 3 hướng cố định (trọng số theo trường chậm) + hướng cấu trúc nơi có cạnh. Không xoay toạ độ theo điểm → không xoáy.
    float sdir(vec2 fp, vec2 d, float L, float Wd, float seed){ vec2 q = vec2(dot(fp, d) / L, dot(fp, vec2(-d.y, d.x)) / Wd); return vn(q + seed) * 0.65 + vn(q * 2.07 + seed + 11.3) * 0.35; }
    float strokes(vec2 fp, vec2 dir, float A, float L, float Wd){
      vec3 w = vec3(vn(fp / 160.0), vn(fp / 160.0 + 17.0), vn(fp / 160.0 + 41.0)); w = w*w*w; w /= (w.x + w.y + w.z);
      float nf = w.x * sdir(fp, vec2(0.866, 0.5), L, Wd, 0.0) + w.y * sdir(fp, vec2(0.259, 0.966), L, Wd, 5.0) + w.z * sdir(fp, vec2(0.966, -0.259), L, Wd, 9.0);
      float ns = sdir(fp, dir, L, Wd, 13.0);
      return mix(nf, ns, smoothstep(0.1, 0.5, A));
    }
    void main(){
      vec3 c = texture(tSrc, vUv).rgb;
      float imp0 = texture(tG, vUv).y;
      c = mix(c, texture(tOrig, vUv).rgb, detail * imp0);   // vùng quan trọng giữ lại một phần chi tiết gốc
      vec3 t = texture(tTen, vUv).xyz;
      float dd = sqrt(max((t.x-t.z)*(t.x-t.z) + 4.0*t.y*t.y, 0.0));
      float l1 = 0.5*(t.x+t.z+dd), l2 = 0.5*(t.x+t.z-dd);
      vec2 v = vec2(l1 - t.x, -t.y); vec2 dir = dot(v,v) > 1e-14 ? normalize(v) : vec2(0.70710678);
      float A = (l1+l2 > 1e-10) ? (l1-l2)/(l1+l2) : 0.0;
      // nét cọ: nhiễu kéo dài theo tiếp tuyến; nơi phẳng (A≈0) dùng hướng chéo cố định → mảng phết đều, không xoáy
      vec2 fp = gl_FragCoord.xy / S;
      float n = smoothstep(0.3, 0.7, strokes(fp, dir, A, sLen, sWid));
      vec2 q = fp / vec2(sLen, sWid);
      float imp = texture(tG, vUv).y;
      float L = dot(c, vec3(0.2126,0.7152,0.0722));
      float amt = stroke * (1.0 - 0.6*imp) * smoothstep(0.002, 0.03, L);
      c *= 1.0 + amt * (n - 0.5) * 2.0;
      c *= 1.0 + 0.4 * amt * (vn(q * 0.37 + 5.0) - 0.5) * 2.0 * vec3(1.0, -0.15, -0.9);
      vec3 b0 = texture(tB0, vUv).rgb, b3 = texture(tB3, vUv).rgb;
      vec3 hi = max(b3 - vec3(thr), vec3(0.0));
      c = c * (1.0 - bloom - bloomWide) + b0 * bloom + b3 * bloomWide + hi * halation * vec3(1.0, 0.42, 0.18);
      o = vec4(c, 1.0); }`, { tSrc: { value: paintRT.texture }, tOrig: { value: null }, detail: { value: prm.detail }, tTen: { value: tA.texture }, tG: { value: gRT.texture }, tB0: { value: up[0].texture }, tB3: { value: up[2].texture },
    res: { value: new THREE.Vector2(W, H) }, stroke: { value: prm.stroke }, sLen: { value: prm.strokeLen }, sWid: { value: prm.strokeWid },
    bloom: { value: prm.bloom }, bloomWide: { value: prm.bloomWide }, halation: { value: prm.halation }, thr: { value: prm.thr }, S: { value: S } });

  function gbuffer(scene, camera) {
    const saved = [];
    scene.traverse((o) => {
      if (o.isSprite || o.userData.noG) { saved.push([o, 'v', o.visible]); o.visible = false; return; }
      if (!o.isMesh) return;
      let imp = 0; for (let p = o; p; p = p.parent) if (p.userData.imp) { imp = 1; break; }
      saved.push([o, 'm', o.material]); o.material = gM[imp];
    });
    const bg = scene.background, fog = scene.fog; scene.background = null; scene.fog = null;
    renderer.setRenderTarget(gRT); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, camera);
    scene.background = bg; scene.fog = fog;
    for (const [o, k, v] of saved) { if (k === 'v') o.visible = v; else o.material = v; }
  }

  function apply(scene, camera) {
    const src = pipe.accRT.texture;
    let tg = profOn ? performance.now() : 0; gbuffer(scene, camera); if (profOn) { sync(gRT); prof.gbuf = performance.now() - tg; }
    tensor.uniforms.tSrc.value = src; run(tensor, tA, 'tensor');
    blur.uniforms.sig.value = 1.1 * S;
    blur.uniforms.tSrc.value = tA.texture; blur.uniforms.dir.value.set(2 / W, 0); run(blur, tB);
    blur.uniforms.tSrc.value = tB.texture; blur.uniforms.dir.value.set(0, 2 / H); run(blur, tA);
    // tA = tensor đã làm mịn (nửa độ phân giải)
    pre.uniforms.tSrc.value = src; pre.uniforms.tTen.value = tA.texture; run(pre, preRT, 'pre');
    kuwa.uniforms.tSrc.value = preRT.texture; kuwa.uniforms.tTen.value = tA.texture; run(kuwa, paintRT, 'kuwa');
    // bloom
    let prev = paintRT;
    for (let i = 0; i < NL; i++) { downM.uniforms.tSrc.value = prev.texture; downM.uniforms.px.value.set(1 / prev.width, 1 / prev.height); downM.uniforms.first.value = i === 0 ? 1 : 0; run(downM, down[i], 'bloom'); prev = down[i]; }
    let acc = down[NL - 1];
    for (let i = NL - 2; i >= 0; i--) { upM.uniforms.tSrc.value = acc.texture; upM.uniforms.tAdd.value = down[i].texture; upM.uniforms.px.value.set(1 / acc.width, 1 / acc.height); run(upM, up[i], 'bloom'); acc = up[i]; }
    // chuẩn hoá: up[0] là tổng NL tầng → chia NL trong comp qua hệ số
    comp.uniforms.bloom.value = prm.bloom / NL; comp.uniforms.bloomWide.value = prm.bloomWide / (NL - 2);
    comp.uniforms.tOrig.value = src;
    run(comp, outRT, 'comp');
    pipe.outMat.uniforms.tAcc.value = outRT.texture;
  }
  function bypass() { pipe.outMat.uniforms.tAcc.value = pipe.accRT.texture; }
  return { apply, bypass, gRT, outRT, prm, prof, setProf: (v) => { profOn = v; } };
}

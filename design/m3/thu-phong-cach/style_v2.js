// Cine Lab · M3 THỬ PHONG CÁCH — B3 v2 (cờ dbg.style = 'b3v2'), sửa sau kiểm mù Mốc 1 (P giao 01/10/2026).
// Tệp riêng: B3 v1 ('b3') và B1 ('b1') giữ nguyên mã, nên không đổi điểm ảnh.
// (a) Ánh sáng bám nguồn: chỉ BẬC THANG HOÁ ÁNH SÁNG (độ sáng nhoè rộng ≈ chiếu sáng, đã trung bình hoá vân tường) rồi nhân lên ảnh gốc
//     làm phẳng nhẹ → hết vệt "ố/loang" do bậc thang hoá vân vật liệu; bậc nhỏ hơn (0,55 stop), mép mềm, dither tĩnh theo điểm ảnh → hết phân dải.
// (b) Bóng nhân vật có khối: viền sáng lấy màu/độ sáng của ánh quanh mép (đèn có trong khung), cộng sắc độ thân mờ (nếp áo, khối vai).
// (c) s22: giảm ánh trắng tràn phẳng (bán cầu) còn 22 %, để cột điện mé đường đối diện (x = 29, POST_Z) là nguồn chính, có hướng, giảm
//     theo khoảng cách, đổ bóng (luật thế giới v0.6). Không thêm đèn khí.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';

export function installB3v2(o, { common, gMaterial, B3_CAM, HDR }) {
  const { renderer, pipe, cur, W, H } = o, dbg = o.dbg || {};
  const C = common({ ...o, camTable: B3_CAM });
  const S = W / 960, GS = W >= 1920 ? 1 : 2;
  const gRT = new THREE.WebGLRenderTarget(W * GS, H * GS, { ...C.fOpt, depthBuffer: true });
  const gM = [gMaterial(0), gMaterial(1), gMaterial(2)];
  const hA = C.rt(W / 2, H / 2), hB = C.rt(W / 2, H / 2), qA = C.rt(W / 8, H / 8), qB = C.rt(W / 8, H / 8), outRT = C.rt(W, H);
  const P = Object.assign({ step: 0.55, soft: 0.24, dith: 0.28, flatK: 0.55, sat: 0.85, shK: 0.45, shLen: 9.0, edgeK: 0.25, papK: 0.07, eLo: -2.2, eHi: 0.6, rimK: 1.0, formK: 0.03 }, dbg.b3 || {});
  const down = C.mk(`uniform sampler2D tSrc; uniform vec2 px; void main(){ vec3 s = vec3(0.0);
      for (int j=-1;j<=1;j++) for (int i=-1;i<=1;i++) s += texture(tSrc, vUv + vec2(i,j)*px).rgb; o = vec4(s/9.0, 1.0); }`,
    { tSrc: { value: null }, px: { value: new THREE.Vector2() } });
  const blur = C.mk(`uniform sampler2D tSrc; uniform vec2 dir; uniform float sig;
      void main(){ vec4 s = vec4(0.0); float ws = 0.0;
        for (int k=-6; k<=6; k++){ float x = float(k); float w = exp(-0.5*x*x/(sig*sig)); s += texture(tSrc, vUv + dir*x) * w; ws += w; }
        o = s/ws; }`, { tSrc: { value: null }, dir: { value: new THREE.Vector2() }, sig: { value: 1.0 } });
  const sty = C.mk(`uniform sampler2D tSrc, tBlur, tBig, tG; uniform vec2 px, camOff; uniform float S, fpx, uExp;
    uniform float step_, soft, dith, flatK, sat, shK, shLen, edgeK, papK, eLo, eHi, rimK, formK;
    float zAt(vec2 uv){ float z = texture(tG, uv).r; return z > 0.0 ? z : 1.0e4; }
    float stair(float e){ float x = e / step_; float b = floor(x); return step_ * (b + smoothstep(0.5 - soft, 0.5 + soft, fract(x))); }
    float paper(vec2 p){
      float n = 0.42*vn(p/1.7) + 0.26*vn(p/5.0 + 3.1) + 0.18*vn(p/19.0 + 8.3) + 0.14*vn(p/61.0 + 1.7);
      float fib = vn(vec2(p.x*0.55 + p.y*0.21, p.y*0.06 - p.x*0.018) + 4.4);
      return n + 0.22*(smoothstep(0.62, 0.9, fib) - 0.1); }
    void main(){
      vec2 fp = gl_FragCoord.xy / S;
      vec2 wv = (vec2(vn(fp/7.0), vn(fp/7.0 + 7.7)) - 0.5) * 1.6 + (vec2(vn(fp/31.0 + 3.0), vn(fp/31.0 + 9.0)) - 0.5) * 2.4;
      vec2 uvw = vUv + wv * S * px;
      vec4 g = texture(tG, uvw); float z = g.r > 0.0 ? g.r : 1.0e4; float ch = g.g, dat = g.b;
      vec3 src = texture(tSrc, vUv).rgb, bl = texture(tBlur, vUv).rgb, big = texture(tBig, vUv).rgb;
      float Ls = lum(src), Lg = max(lum(big), 1e-7);
      // (a) bậc thang hoá ÁNH SÁNG (nhoè rộng ≈ chiếu sáng), dither tĩnh tam giác chống phân dải
      float tri = h21(gl_FragCoord.xy * 0.731) + h21(gl_FragCoord.xy * 1.37 + 17.0) - 1.0;
      float e = log2(max(Lg * uExp, 1e-6)), q = stair(e + tri * dith * step_), gain = exp2(q - e);
      float hiB = smoothstep(eLo, eHi, q);
      vec3 tint = mix(vec3(0.84, 0.88, 1.14), vec3(1.10, 0.98, 0.84), hiB);
      vec3 base = mix(src, bl * clamp(Ls / max(lum(bl), 1e-7), 0.8, 1.25), flatK);      // làm phẳng nhẹ, giữ vân
      float L0 = max(lum(base), 1e-7); base = mix(vec3(L0), base, sat);
      vec3 c = base * gain * tint;
      if (dat > 0.5) c = src * gain * tint;
      // (b) bóng có khối: sắc độ thân mờ + viền sáng theo ánh quanh mép
      if (ch > 0.01) {
        float m = 1.0, mo = 1.0;
        for (int i = 0; i < 8; i++) { float a = float(i) * 0.7854; vec2 d = vec2(cos(a), sin(a));
          m = min(m, texture(tG, uvw + d * 2.2 * S * px).g); mo = min(mo, texture(tG, uvw + d * 4.5 * S * px).g); }
        float rim = 1.0 - smoothstep(0.15, 0.85, m), rim2 = (1.0 - smoothstep(0.15, 0.85, mo)) * 0.45;
        float env = smoothstep(-3.0, 0.3, log2(Lg * uExp));                               // ánh quanh mép (đèn trong khung)
        vec3 envC = big / Lg;
        vec3 ink = vec3(0.0105, 0.0085, 0.0135) / uExp;
        vec3 form = ink * (1.0 + formK * 30.0 * sqrt(clamp(lum(bl) * uExp, 0.0, 1.0)) * vec3(1.0, 0.9, 0.8));                         // khối thân mờ (độ sáng nhoè, không màu da → không lộ nét mặt)
        vec3 rimC = envC * max(Lg, 0.05 / uExp) * 1.25 * tint;
        vec3 sil = mix(form, rimC, clamp(rimK * (rim + rim2 * (1.0 - rim)) * (0.25 + 0.75 * env), 0.0, 1.0));
        c = mix(c, sil, clamp(ch, 0.0, 1.0));
      }
      float sh = 0.0, wsum = 0.0; vec2 sd = normalize(vec2(1.0, -1.0));
      for (int i = 1; i <= 5; i++) { float l = float(i) / 5.0; float zq = zAt(uvw - sd * l * shLen * S * px); float w = 1.2 - l; sh += w * step(zq, z * 0.8); wsum += w; }
      c *= 1.0 - shK * clamp(sh / wsum * 1.6, 0.0, 1.0) * (1.0 - 0.6 * ch);
      float zn = zAt(uvw - sd * 1.6 * S * px); float edge = step(z * 1.3, zn) * (1.0 - ch);
      c += edge * edgeK * c;
      float k = floor(clamp(log2(z / 1.25) * 1.1, 0.0, 9.0));
      vec2 tp = fp + camOff * fpx / min(z, 400.0) / S + vec2(k * 37.0, k * 91.0);
      c *= 1.0 + papK * (paper(tp) - 0.5) * 2.0 * (1.0 - dat);
      o = vec4(max(c, 0.0), 1.0); }`,
    { tSrc: { value: null }, tBlur: { value: hA.texture }, tBig: { value: qA.texture }, tG: { value: gRT.texture }, px: { value: new THREE.Vector2(1 / W, 1 / H) }, camOff: { value: new THREE.Vector2() },
      S: { value: S }, fpx: { value: 0 }, uExp: { value: 1 }, ...Object.fromEntries(['step', 'soft', 'dith', 'flatK', 'sat', 'shK', 'shLen', 'edgeK', 'papK', 'eLo', 'eHi', 'rimK', 'formK'].map((k) => [k === 'step' ? 'step_' : k, { value: P[k] }])) });
  const u = pipe.outMat.uniforms; u.gCanvas.value = 0;
  // (c) s22: nguồn ánh điện có hướng — cột x = 29 mé đối diện đổ bóng; ánh tràn bán cầu giảm
  const sc = cur.scene; let hemiW = null, post = null;
  if (o.shot.id === 's22') {
    sc.traverse((x) => { if (x.isHemisphereLight && x.color.getHexString() === 'dfe6ff') hemiW = x;
      if (x.isPointLight && x.color.getHexString() === 'e3eaff' && Math.abs(x.position.x - 29) < 3) post = x; });
    if (post) { post.castShadow = true; post.shadow.mapSize.set(1024, 1024); post.shadow.bias = -0.0006; post.shadow.normalBias = 0.02; post.shadow.camera.near = 0.2; }
  }
  let cam0 = null; const right = new THREE.Vector3(), up = new THREE.Vector3(), d = new THREE.Vector3();
  return {
    noPaint: true,
    frame(t, T, f) { C.applyCam(); if (dbg.exp) u.uExp.value *= dbg.exp;
      if (hemiW) { hemiW.intensity *= (dbg.hemiK ?? 0.22); u.uExp.value *= (dbg.s22exp ?? 1.7); } },
    post() {
      const cam = cur.cam; cam.updateMatrixWorld(true);
      if (!cam0) cam0 = cam.position.clone();
      right.setFromMatrixColumn(cam.matrixWorld, 0); up.setFromMatrixColumn(cam.matrixWorld, 1); d.copy(cam.position).sub(cam0);
      sty.uniforms.camOff.value.set(d.dot(right), d.dot(up)); sty.uniforms.fpx.value = (H / 2) / Math.tan(cam.fov * Math.PI / 360);
      C.gbuffer(gRT, gM, cur.scene, cam);
      down.uniforms.tSrc.value = pipe.accRT.texture; down.uniforms.px.value.set(1 / W, 1 / H); C.run(down, hA);
      blur.uniforms.sig.value = 1.0;
      blur.uniforms.tSrc.value = hA.texture; blur.uniforms.dir.value.set(2 / W, 0); C.run(blur, hB);
      blur.uniforms.tSrc.value = hB.texture; blur.uniforms.dir.value.set(0, 2 / H); C.run(blur, hA);
      // nhoè rộng (≈ chiếu sáng): 1/8 độ phân giải, σ 3 → ≈ 24 px ảnh đầy
      down.uniforms.tSrc.value = hA.texture; down.uniforms.px.value.set(2 / W, 2 / H); C.run(down, qA);
      blur.uniforms.sig.value = 3.0;
      blur.uniforms.tSrc.value = qA.texture; blur.uniforms.dir.value.set(8 / W, 0); C.run(blur, qB);
      blur.uniforms.tSrc.value = qB.texture; blur.uniforms.dir.value.set(0, 8 / H); C.run(blur, qA);
      sty.uniforms.tSrc.value = pipe.accRT.texture; sty.uniforms.uExp.value = u.uExp.value;
      C.run(sty, outRT); renderer.setRenderTarget(null);
      u.tAcc.value = outRT.texture;
    },
  };
}

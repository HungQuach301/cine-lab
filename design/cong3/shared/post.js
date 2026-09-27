// Cine Lab · Cổng 3 — đường ống xuất hình dùng chung (rút từ reports/m1/banding/scene3d_dither.js, đã qua G3/N2 ở M1).
// 1) Mỗi mẫu render vào target Float32 tuyến tính (không tone map), jitter dưới điểm ảnh (R2) → khử răng cưa;
//    hàm onSample(i, n) cho phép scene đổi theo mẫu (jitter nguồn sáng → bóng mềm; jitter khẩu độ → DOF).
// 2) Cộng dồn Float32. 3) Pass cuối: tone map (mặc định ACES Filmic của three.js) → sRGB → grade(c, uv) do hướng mỹ thuật
//    cung cấp (GLSL, không gian hiển thị) → lớp 2D phủ (tuỳ chọn, canvas → texture) → grain đơn sắc cố định + dither TPDF.
// Grain CỐ ĐỊNH cho cả phim (luật G3b: σ ổn định giữa shot): σ 1,5 mã, hạt 1,6 px, toe 1 mã, dither ±1 LSB.
// Hướng mỹ thuật KHÔNG đổi GRAIN; muốn thêm chất liệu (giấy, nét cọ) thì dùng grade()/lớp 2D, là hình tĩnh theo khung.
import * as THREE from './node_modules/three/build/three.module.js';

export const GRAIN = Object.freeze({ sigma_code: 1.5, size_px: 1.6, dither_lsb: 1.0, grain_toe_code: 1.0, dither_toe_code: 1.0 });

const VS = `in vec3 position; out vec2 vUv; void main(){ vUv = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }`;

export function createPipeline(renderer, W, H, opts = {}) {
  const tone = opts.toneGLSL ?? `vec3 RRTAndODTFit(vec3 v){ vec3 a = v*(v+0.0245786)-0.000090537; vec3 b = v*(0.983729*v+0.4329510)+0.238081; return a/b; }
      vec3 tonemap(vec3 c){
        const mat3 I = mat3(vec3(0.59719,0.07600,0.02840), vec3(0.35458,0.90834,0.13383), vec3(0.04823,0.01566,0.83777));
        const mat3 O = mat3(vec3(1.60475,-0.10208,-0.00327), vec3(-0.53108,1.10813,-0.07276), vec3(-0.07367,-0.00605,1.07602));
        c *= EXPOSURE/0.6; c = I*c; c = RRTAndODTFit(c); c = O*c; return clamp(c,0.0,1.0); }`;
  const grade = opts.gradeGLSL ?? `vec3 grade(vec3 c, vec2 uv){ return c; }`;
  const exposure = opts.exposure ?? 1.0;
  const rtOpt = { type: THREE.FloatType, format: THREE.RGBAFormat, depthBuffer: true, colorSpace: THREE.LinearSRGBColorSpace };
  const sceneRT = new THREE.WebGLRenderTarget(W, H, rtOpt);
  const accRT = new THREE.WebGLRenderTarget(W, H, { ...rtOpt, depthBuffer: false });
  const quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const fsQuad = (m) => { const s = new THREE.Scene(); s.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m)); return s; };
  const accMat = new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3, uniforms: { tSrc: { value: sceneRT.texture }, weight: { value: 1 } }, vertexShader: VS,
    fragmentShader: `precision highp float; uniform sampler2D tSrc; uniform float weight; in vec2 vUv; out vec4 o;
      void main(){ o = vec4(texture(tSrc, vUv).rgb * weight, weight); }`,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendEquation: THREE.AddEquation, depthTest: false, depthWrite: false });
  const overlayTex = opts.overlayCanvas ? new THREE.CanvasTexture(opts.overlayCanvas) : null;
  if (overlayTex) { overlayTex.colorSpace = THREE.NoColorSpace; overlayTex.flipY = true; }
  const outMat = new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms: { tAcc: { value: accRT.texture }, tOver: { value: overlayTex }, frame: { value: 0 }, uExp: { value: exposure }, sigma: { value: GRAIN.sigma_code / 255 }, dith: { value: GRAIN.dither_lsb / 255 }, res: { value: new THREE.Vector2(W, H) }, ...(opts.uniforms || {}) },
    vertexShader: VS,
    fragmentShader: `precision highp float; uniform sampler2D tAcc; uniform sampler2D tOver; uniform float frame, sigma, dith, uExp; uniform vec2 res; in vec2 vUv; out vec4 o;
      ${opts.uniformDecl || ''}
      #define EXPOSURE uExp
      const float GSIZE = ${GRAIN.size_px.toFixed(2)}, GTOE = ${GRAIN.grain_toe_code.toFixed(2)}, DTOE = ${GRAIN.dither_toe_code.toFixed(2)};
      const bool HAS_OVER = ${overlayTex ? 'true' : 'false'};
      ${tone}
      ${grade}
      vec3 srgb(vec3 c){ return mix(c*12.92, 1.055*pow(c, vec3(1.0/2.4))-0.055, step(vec3(0.0031308), c)); }
      uint pcg(uint v){ uint s = v*747796405u+2891336453u; uint w = ((s >> ((s>>28u)+4u)) ^ s)*277803737u; return (w>>22u)^w; }
      float gnode(uvec2 c, uint f){ vec4 r = vec4(uvec4(pcg(c.x + 4099u*c.y + 16777619u*f)) >> uvec4(0u,8u,16u,24u) & 255u) / 255.0; return (r.x+r.y+r.z+r.w-2.0) * 1.7320508; }
      float grain(vec2 p, uint f){ vec2 i = floor(p), t = fract(p); t = t*t*(3.0-2.0*t); uvec2 c = uvec2(i);
        float v = mix(mix(gnode(c,f), gnode(c+uvec2(1u,0u),f), t.x), mix(gnode(c+uvec2(0u,1u),f), gnode(c+uvec2(1u,1u),f), t.x), t.y); return v * 1.347; }
      vec4 bytes(uint h){ return vec4(uvec4(h, h>>8u, h>>16u, h>>24u) & 255u) / 256.0 + 0.5/256.0; }
      void main(){
        vec3 c = srgb(tonemap(max(texture(tAcc, vUv).rgb, 0.0)));
        c = grade(c, vUv);
        if (HAS_OVER) { vec4 ov = texture(tOver, vUv); c = mix(c, ov.rgb, ov.a); }
        c = clamp(c, 0.0, 1.0);
        uvec2 q = uvec2(gl_FragCoord.xy);
        uint h1 = pcg(q.x + 1920u*q.y + 2073600u*uint(frame)); uint h2 = pcg(h1 ^ 0x9E3779B9u);
        vec4 b = bytes(h2);
        float g = grain(gl_FragCoord.xy / GSIZE, uint(frame));
        float d = b.x - b.y;
        float l8 = dot(c, vec3(0.2126, 0.7152, 0.0722)) * 255.0;
        c += g*sigma*clamp(l8 / GTOE, 0.0, 1.0) + d*dith*clamp(l8 / DTOE, 0.0, 1.0);
        o = vec4(clamp(c, 0.0, 1.0), 1.0);
      }`,
    depthTest: false, depthWrite: false });
  const accScene = fsQuad(accMat), outScene = fsQuad(outMat);
  const R2 = (i) => [((0.5 + 0.7548776662 * (i + 1)) % 1) - 0.5, ((0.5 + 0.5698402910 * (i + 1)) % 1) - 0.5];

  // Render tích luỹ n mẫu. onSample(i, n, jitter) để scene đổi theo mẫu (jitter đèn/khẩu độ). Trả thời gian (ms).
  function accumulate(scene, camera, n, onSample) {
    const t0 = performance.now();
    renderer.setRenderTarget(accRT); renderer.setClearColor(0x000000, 0); renderer.clear(true, false, false);
    for (let i = 0; i < n; i++) {
      const [jx, jy] = n === 1 ? [0, 0] : R2(i);
      if (onSample) onSample(i, n, [jx, jy]);
      if (camera.isPerspectiveCamera || camera.isOrthographicCamera) camera.setViewOffset(W, H, jx, jy, W, H);
      renderer.setRenderTarget(sceneRT); renderer.render(scene, camera);
      accMat.uniforms.weight.value = 1 / n;
      renderer.setRenderTarget(accRT); renderer.autoClear = false; renderer.render(accScene, quadCam); renderer.autoClear = true;
    }
    camera.clearViewOffset();
    return performance.now() - t0;
  }
  // Pass cuối cho khung số f (grain đổi theo f). Trả RGB24 base64 (hàng từ dưới lên) để driver ghi file.
  function finalize(f) {
    if (overlayTex) overlayTex.needsUpdate = true;
    outMat.uniforms.frame.value = f;
    renderer.setRenderTarget(null); renderer.render(outScene, quadCam);
    const gl = renderer.getContext();
    const px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const rgb = new Uint8Array(W * H * 3); for (let i = 0, j = 0; i < px.length; i += 4, j += 3) { rgb[j] = px[i]; rgb[j + 1] = px[i + 1]; rgb[j + 2] = px[i + 2]; }
    let bin = ''; const CH = 0x8000; for (let i = 0; i < rgb.length; i += CH) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + CH));
    return btoa(bin);
  }
  return { accumulate, finalize, sceneRT, accRT, outMat };
}

// Tạo renderer chuẩn cho mọi hướng (Chromium headless + SwiftShader).
export function createRenderer(W, H) {
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  const renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: false, preserveDrawingBuffer: true });
  renderer.setSize(W, H, false); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.NoToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
  return renderer;
}

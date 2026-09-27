// Cảnh mẫu M0 — phong cách (b) 2.5D three.js — BẢN SỬA BANDING M1 (bước 3).
// Dàn cảnh, nhân vật, máy quay giữ nguyên từ reports/m0/bench/scene3d.js; chỉ thay đường ống xuất ảnh:
//  1. Mỗi mẫu motion blur render vào render target Float32 tuyến tính (HalfFloat chậm hơn ~25% trên SwiftShader), không tone map; khử răng cưa bằng jitter
//     dưới điểm ảnh theo dãy R2 cho từng mẫu (accumulation AA) thay cho MSAA (MSAA trên HalfFloat làm chậm ~2,3× trên SwiftShader).
//  2. Cộng dồn các mẫu trong target Float32 (blend One/One, trọng số 1/N) — thay cho cộng dồn 8 bit qua canvas 2D ở M0.
//  3. Pass cuối: ACES Filmic (công thức của three.js) → sRGB → grain đơn sắc cố định + dither TPDF ±1 LSB → 8 bit.
//     Grain "cố định": σ 1,5 mã, hạt 1,6 px, toe 1 mã, dither ±1 LSB là hằng số (GRAIN bên dưới, sẽ vào bible);
//     mẫu nhiễu băm theo (x, y, số khung) nên render tất định.
import * as THREE from './node_modules/three/build/three.module.js';

let S, M, renderer, scene, camera, acc, actx, rig, lampLight, W, H;
const U = 0.32; // mét trên 1 H (nhân vật cao 5,6 H ≈ 1,8 m)

function lcg(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0, ...o });

function limb(len, w, color) {
  // Bộ phận treo từ khớp gốc hướng xuống -y.
  const g = new THREE.CapsuleGeometry(w / 2, Math.max(0.001, len - w), 6, 12);
  g.translate(0, -len / 2 + 0, 0);
  const m = new THREE.Mesh(g, mat(color)); m.castShadow = true; return m;
}

function buildCharacter() {
  const root = new THREE.Group(), hip = new THREE.Group(); root.add(hip);
  const T = M.torso, tl = T.length * U;
  const torsoGeo = new THREE.CylinderGeometry(T.top_width * U / 2, T.bottom_width * U / 2, tl, 20, 1);
  const torso = new THREE.Mesh(torsoGeo, mat(T.color)); torso.position.y = tl / 2; torso.scale.z = 0.6; torso.castShadow = true; hip.add(torso);
  const neck = limb(M.neck.length * U + 0.05, M.neck.width * U, M.neck.color); neck.position.y = tl + M.neck.length * U; hip.add(neck);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.5, 24, 16), mat(M.head.color));
  head.scale.set(M.head.width * U, M.head.length * U, M.head.width * U * 0.95);
  const hcY = tl + M.neck.length * U + M.head.length * U / 2; head.position.y = hcY; head.castShadow = true; hip.add(head);
  const brim = new THREE.Mesh(new THREE.CylinderGeometry(M.hat.width * U / 2, M.hat.width * U / 2, 0.03, 24), mat(M.hat.color));
  brim.position.y = hcY + M.head.length * U * 0.3; hip.add(brim);
  const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.4 * U, 0.42 * U, M.hat.length * U, 20), mat(M.hat.color));
  crown.position.y = brim.position.y + M.hat.length * U / 2; crown.castShadow = true; hip.add(crown);
  const chain = (parent, y, z, p1, p2, end, dark) => {
    const j1 = new THREE.Group(); j1.position.set(0, y, z); parent.add(j1);
    const a = limb(p1.length * U, p1.width * U, dark ? '#3b2219' : p1.color); j1.add(a);
    const j2 = new THREE.Group(); j2.position.y = -p1.length * U; j1.add(j2);
    const b = limb(p2.length * U, p2.width * U, dark ? '#3b2219' : p2.color); j2.add(b);
    const e = new THREE.Group(); e.position.y = -p2.length * U; j2.add(e);
    if (end) e.add(end);
    return [j1, j2, e];
  };
  const foot = () => { const f = new THREE.Mesh(new THREE.BoxGeometry(M.foot.length * U, M.foot.width * U, 0.1), mat(M.foot.color)); f.position.set(M.foot.length * U * 0.3, -0.02, 0); f.castShadow = true; return f; };
  const hand = () => { const h = new THREE.Mesh(new THREE.SphereGeometry(M.hand.width * U / 2, 12, 8), mat(M.hand.color)); return h; };
  const legF = chain(hip, 0, 0.1, M.thigh, M.shin, foot());
  const legB = chain(hip, 0, -0.1, M.thigh, M.shin, foot(), true);
  const sy = tl - M.joints.shoulder_from_torso_top * U;
  const armF = chain(hip, sy, 0.2, M.upper_arm, M.forearm, hand());
  const armB = chain(hip, sy, -0.2, M.upper_arm, M.forearm, hand(), true);
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, M.pole.length * U, 8), mat(M.pole.color));
  pole.position.y = M.pole.length * U * 0.25; pole.rotation.z = -0.35; armF[2].add(pole);
  return { root, hip, legF, legB, armF, armB };
}

function build() {
  const r = lcg(7);
  scene = new THREE.Scene();
  scene.background = new THREE.Color('#3a2540');
  scene.fog = new THREE.Fog('#5a3550', 12, 70);
  // Trời: tấm phông gradient xa.
  const skyC = document.createElement('canvas'); skyC.width = 4; skyC.height = 256; const sg = skyC.getContext('2d');
  const gr = sg.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#1b1830'); gr.addColorStop(0.6, '#5a3550'); gr.addColorStop(0.85, '#c0664a'); gr.addColorStop(1, '#2a1a22');
  sg.fillStyle = gr; sg.fillRect(0, 0, 4, 256);
  const skyTex = new THREE.CanvasTexture(skyC); skyTex.colorSpace = THREE.SRGBColorSpace;
  const sky = new THREE.Mesh(new THREE.PlaneGeometry(400, 90), new THREE.MeshBasicMaterial({ map: skyTex, fog: false }));
  sky.position.set(0, 20, -120); scene.add(sky);
  // Lớp xa: silhouette phẳng.
  const farMat = new THREE.MeshBasicMaterial({ color: S.layers[0].color });
  for (let x = -60; x < 120; x += 2 + r() * 3) { const h = 6 + r() * 10, w = 2 + r() * 4; const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), farMat); m.position.set(x, h / 2, -45); scene.add(m); }
  // Lớp giữa: nhà khối có cửa sổ phát sáng.
  const wallMat = mat(S.layers[1].color), winOn = new THREE.MeshBasicMaterial({ color: '#e89a4a' }), winOff = mat('#1a1520');
  for (let x = -12; x < 40; x += 3.2 + r() * 1.5) {
    const w = 2.6 + r() * 1.2, h = 3.5 + r() * 2.5, d = 3;
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wallMat); b.position.set(x, h / 2, -4.5); b.receiveShadow = true; scene.add(b);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(w * 0.75, 1.2, 4), wallMat); roof.rotation.y = Math.PI / 4; roof.position.set(x, h + 0.6, -4.5); scene.add(roof);
    for (let wy = 0.9; wy < h - 0.6; wy += 0.9) for (let wx = -w / 2 + 0.5; wx < w / 2 - 0.3; wx += 0.8) {
      const on = r() < 0.45; const q = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.45), on ? winOn : winOff);
      q.position.set(x + wx, wy, -4.5 + d / 2 + 0.01); scene.add(q);
    }
  }
  // Mặt đường.
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 30), mat('#2b2128', { roughness: 0.6 }));
  ground.rotation.x = -Math.PI / 2; ground.position.z = 0; ground.receiveShadow = true; scene.add(ground);
  // Cột đèn khí + nguồn sáng ấm duy nhất (point light có bóng đổ).
  const lx = S.light.world_x / 100 - 9.6 + 3;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 3.4, 10), mat('#15111a')); post.position.set(lx, 1.7, -1.2); scene.add(post);
  const bulb = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.4, 0.28), new THREE.MeshBasicMaterial({ color: '#ffd08a' })); bulb.position.set(lx, 3.55, -1.2); scene.add(bulb);
  lampLight = new THREE.PointLight(S.light.color, 40, 18, 1.6); lampLight.position.set(lx, 3.5, -1.0);
  lampLight.castShadow = true; lampLight.shadow.mapSize.set(1024, 1024); lampLight.shadow.bias = -0.002; scene.add(lampLight);
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color: '#ffb45a', blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
  glow.scale.set(4, 4, 1); glow.position.copy(bulb.position); scene.add(glow);
  scene.add(new THREE.HemisphereLight('#6a5a9a', '#1a1018', 0.35));
  // Lớp gần: cột và hàng rào tiền cảnh.
  const nearMat = mat(S.layers[2].color);
  for (let x = -8; x < 60; x += 5 + r() * 4) {
    if (r() < 0.5) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.3, 8, 0.3), nearMat); p.position.set(x, 4, 3.2); scene.add(p); }
    else for (let i = 0; i < 5; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.0, 0.08), nearMat); p.position.set(x + i * 0.3, 0.5, 3.0); scene.add(p); }
  }
  rig = buildCharacter(); scene.add(rig.root);
  camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 300);
}

function glowTex() {
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
}

function pose(t) {
  const C = S.character, ph = t * C.step_hz * Math.PI * 2, s = Math.sin(ph);
  const x0 = -10.5, x1 = 17.5; // đi qua khung từ trái sang phải
  const x = x0 + (x1 - x0) * (t / S.duration_s);
  const legLen = (M.thigh.length + M.shin.length + M.foot.width) * U;
  rig.root.position.set(x, legLen * 0.97 - Math.abs(Math.cos(ph)) * 0.02, 0);
  rig.legF[0].rotation.z = 0.42 * s; rig.legF[1].rotation.z = -Math.max(0, 0.7 * Math.sin(ph + 1.2));
  rig.legB[0].rotation.z = -0.42 * s; rig.legB[1].rotation.z = -Math.max(0, -0.7 * Math.sin(ph + 1.2));
  rig.armF[0].rotation.z = 0.12 - 0.05 * s; rig.armF[1].rotation.z = 0.9;
  rig.armB[0].rotation.z = 0.35 * s; rig.armB[1].rotation.z = 0.35;
  const cx = 3 + t * 0.6; camera.position.set(cx, 1.6, 14); camera.lookAt(cx, 1.5, 0);
}


const GRAIN = { sigma_code: 1.5, size_px: 1.6, dither_lsb: 1.0, grain_toe_code: 1.0, dither_toe_code: 1.0 }; // đơn vị: mã 8 bit của ảnh RGB đầu ra
let sceneRT, accRT, accScene, accMat, outScene, outMat, quadCam;

function fsQuad(material) { const s = new THREE.Scene(); s.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), material)); return s; }
const VS = `in vec3 position; out vec2 vUv; void main(){ vUv = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }`;

window.setup = function (sceneCfg, sheet) {
  S = sceneCfg; M = sheet; W = S.width; H = S.height;
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: false, preserveDrawingBuffer: true });
  renderer.setSize(W, H, false); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace; // chỉ áp khi vẽ ra màn; ta tự làm ở pass cuối
  window._gl = cv;
  const rtOpt = { type: (window.RT_TYPE === 'half' ? THREE.HalfFloatType : THREE.FloatType), format: THREE.RGBAFormat, depthBuffer: true, colorSpace: THREE.LinearSRGBColorSpace };
  sceneRT = new THREE.WebGLRenderTarget(W, H, rtOpt);
  accRT = new THREE.WebGLRenderTarget(W, H, { ...rtOpt, depthBuffer: false });
  quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  accMat = new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3, uniforms: { tSrc: { value: sceneRT.texture }, weight: { value: 1 } },
    vertexShader: VS,
    fragmentShader: `precision highp float; uniform sampler2D tSrc; uniform float weight; in vec2 vUv; out vec4 o;
      void main(){ o = vec4(texture(tSrc, vUv).rgb * weight, weight); }`,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendEquation: THREE.AddEquation,
    depthTest: false, depthWrite: false });
  outMat = new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms: { tAcc: { value: accRT.texture }, frame: { value: 0 }, sigma: { value: GRAIN.sigma_code / 255 }, dith: { value: GRAIN.dither_lsb / 255 } },
    vertexShader: VS,
    fragmentShader: `precision highp float; uniform sampler2D tAcc; uniform float frame, sigma, dith; in vec2 vUv; const float GSIZE = ${GRAIN.size_px.toFixed(2)}, GTOE = ${GRAIN.grain_toe_code.toFixed(2)}, DTOE = ${GRAIN.dither_toe_code.toFixed(2)}; out vec4 o;
      vec3 RRTAndODTFit(vec3 v){ vec3 a = v*(v+0.0245786)-0.000090537; vec3 b = v*(0.983729*v+0.4329510)+0.238081; return a/b; }
      vec3 aces(vec3 c){
        const mat3 I = mat3(vec3(0.59719,0.07600,0.02840), vec3(0.35458,0.90834,0.13383), vec3(0.04823,0.01566,0.83777));
        const mat3 O = mat3(vec3(1.60475,-0.10208,-0.00327), vec3(-0.53108,1.10813,-0.07276), vec3(-0.07367,-0.00605,1.07602));
        c *= 1.0/0.6; c = I*c; c = RRTAndODTFit(c); c = O*c; return clamp(c,0.0,1.0); }
      vec3 srgb(vec3 c){ return mix(c*12.92, 1.055*pow(c, vec3(1.0/2.4))-0.055, step(vec3(0.0031308), c)); }
      // Hash nguyên (PCG) — tất định, không phụ thuộc độ chính xác sin() của từng GPU.
      uint pcg(uint v){ uint s = v*747796405u+2891336453u; uint w = ((s >> ((s>>28u)+4u)) ^ s)*277803737u; return (w>>22u)^w; }
      float gnode(uvec2 c, uint f){ vec4 r = vec4(uvec4(pcg(c.x + 4099u*c.y + 16777619u*f)) >> uvec4(0u,8u,16u,24u) & 255u) / 255.0;
        return (r.x+r.y+r.z+r.w-2.0) * 1.7320508; }
      float grain(vec2 p, uint f){ vec2 i = floor(p), t = fract(p); t = t*t*(3.0-2.0*t); uvec2 c = uvec2(i);
        float v = mix(mix(gnode(c,f), gnode(c+uvec2(1u,0u),f), t.x), mix(gnode(c+uvec2(0u,1u),f), gnode(c+uvec2(1u,1u),f), t.x), t.y);
        return v * 1.347; } // bù phương sai giảm do nội suy smoothstep 2D (mô phỏng Monte Carlo: σ ≈ 0,742)
      vec4 bytes(uint h){ return vec4(uvec4(h, h>>8u, h>>16u, h>>24u) & 255u) / 256.0 + 0.5/256.0; }
      void main(){
        uvec2 q = uvec2(gl_FragCoord.xy);
        uint h1 = pcg(q.x + 1920u*q.y + 2073600u*uint(frame)); uint h2 = pcg(h1 ^ 0x9E3779B9u);
        vec4 a = bytes(h1), b = bytes(h2);
        vec3 c = srgb(aces(texture(tAcc, vUv).rgb));
        // Grain đơn sắc có kích thước hạt GSIZE px (value noise nội suy song tuyến từ lưới băm), cùng giá trị cho R,G,B để sống qua 4:2:0.
        // Hạt lớn hơn 1 px giống hạt phim và dồn năng lượng về tần số thấp hơn, nên bộ mã hoá không xoá mất ở vùng tối.
        float g = grain(gl_FragCoord.xy / GSIZE, uint(frame));
        // Dither TPDF ±1 LSB trước lượng tử 8 bit.
        float d = b.x - b.y;
        // Toe tách đôi (đơn vị mã 8 bit của luma RGB):
        //  - grain σ giảm tuyến tính dưới GTOE: grain lớn không bị cắt hàng loạt ở 0 rồi bị bộ mã hoá đẩy dưới mức đen limited (N2);
        //  - dither TPDF ±1 LSB giữ đủ từ DTOE trở lên: vùng gần đen vẫn được dither nên không thành bậc thang (G3).
        float l8 = dot(c, vec3(0.2126, 0.7152, 0.0722)) * 255.0;
        c += g*sigma*clamp(l8 / GTOE, 0.0, 1.0) + d*dith*clamp(l8 / DTOE, 0.0, 1.0);
        o = vec4(clamp(c,0.0,1.0), 1.0);
      }`,
    depthTest: false, depthWrite: false });
  accScene = fsQuad(accMat); outScene = fsQuad(outMat);
  build();
};

window.renderFrame = function (f, samples, fmt) {
  const t0 = performance.now(), sh = S.motion_blur.shutter;
  renderer.setRenderTarget(accRT); renderer.setClearColor(0x000000, 0); renderer.clear(true, false, false);
  // Bóng đổ cập nhật 1 lần/khung: mẫu đầu tiên được render là mẫu gần giữa màn trập (thứ tự bắt đầu từ samples/2).
  // Nhân vật dịch ~6 cm trong 1/48 s nên bóng không cần motion blur; bớt 6 lượt render cube bóng cho mỗi mẫu còn lại.
  renderer.shadowMap.autoUpdate = false; renderer.shadowMap.needsUpdate = true;
  for (let k = 0; k < samples; k++) {
    const s = (k + (samples >> 1)) % samples;
    const off = samples === 1 ? 0 : sh * ((s + 0.5) / samples - 0.5);
    pose((f + off) / S.fps);
    // Jitter dưới điểm ảnh (dãy R2, lệch tâm ±0,5 px); samples = 1 thì không jitter.
    const jx = samples === 1 ? 0 : ((0.5 + 0.7548776662 * (s + 1)) % 1) - 0.5, jy = samples === 1 ? 0 : ((0.5 + 0.5698402910 * (s + 1)) % 1) - 0.5;
    camera.setViewOffset(W, H, jx, jy, W, H);
    renderer.setRenderTarget(sceneRT); renderer.render(scene, camera);
    accMat.uniforms.weight.value = 1 / samples;
    renderer.setRenderTarget(accRT); renderer.autoClear = false; renderer.render(accScene, quadCam); renderer.autoClear = true;
  }
  camera.clearViewOffset(); outMat.uniforms.frame.value = f;
  renderer.setRenderTarget(null); renderer.render(outScene, quadCam);
  const gl = renderer.getContext(); gl.finish(); // đo thật thời gian dựng hình (GPU chạy bất đồng bộ)
  const t1 = performance.now();
  if (fmt === 'raw') {
    // Đọc điểm ảnh thô, bỏ alpha còn RGB24 (hàng từ dưới lên; driver lật bằng vflip trong ffmpeg), mã hoá base64 để chuyển qua CDP.
    const px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const rgb = new Uint8Array(W * H * 3); for (let i = 0, j = 0; i < px.length; i += 4, j += 3) { rgb[j] = px[i]; rgb[j + 1] = px[i + 1]; rgb[j + 2] = px[i + 2]; }
    let bin = ''; const CH = 0x8000; for (let i = 0; i < rgb.length; i += CH) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + CH));
    return { url: 'raw,' + btoa(bin), draw_ms: t1 - t0, encode_ms: performance.now() - t1 };
  }
  const url = window._gl.toDataURL(fmt || 'image/png');
  return { url, draw_ms: t1 - t0, encode_ms: performance.now() - t1 };
};
window.ready = true;

// Đo chi phí từng pass (chỉ dùng cho profile_passes.js).
window._profile = function (n) {
  const gl = renderer.getContext(), px = new Uint8Array(4);
  const sync = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  const t = (fn) => { sync(); const a = performance.now(); for (let i = 0; i < n; i++) { fn(i); sync(); } return (performance.now() - a) / n; };
  pose(1);
  const res = {};
  res.scene_to_halffloat_ms = t(() => { renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); });
  res.scene_to_default_fb_ms = t(() => { renderer.setRenderTarget(null); renderer.render(scene, camera); });
  lampLight.castShadow = false;
  res.scene_halffloat_no_shadow_ms = t(() => { renderer.setRenderTarget(sceneRT); renderer.render(scene, camera); });
  lampLight.castShadow = true;
  res.accumulate_pass_ms = t(() => { renderer.setRenderTarget(accRT); renderer.autoClear = false; renderer.render(accScene, quadCam); renderer.autoClear = true; });
  res.final_pass_ms = t(() => { renderer.setRenderTarget(null); renderer.render(outScene, quadCam); });
  const big = new Uint8Array(W * H * 4);
  res.readpixels_full_ms = t(() => gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, big));
  return res;
};

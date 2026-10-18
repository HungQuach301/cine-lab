// K2V tl · V6 (lệnh V2D-1 chủ dự án 18/10 12:05) · ÁNH SÁNG cho bản SẢN XUẤT llvmpipe — chỉ bật khi cảnh khai `export const V6 = {...}` hoặc cfg.tech.v6.
//  1) BÓNG ĐỔ KHÍT KHUNG NHÌN: hộp bóng của mặt trời ôm ĐÚNG vùng mặt đất máy nhìn thấy (tia 9×7 qua khung, cắt mặt phẳng cao độ 0 / 460 m, cụt ở dmax),
//     trong hệ toạ độ của nguồn sáng, khớp lưới texel (chống nháy) — thay hộp vuông quanh điểm nhìn (V5b: tới 3,2 km / 4096 px ≈ 1,6 m/texel → người không có bóng).
//     Bản đồ bóng 8192² (đo: tl.shadowRes). Bóng mềm PCF giữ của page.js.
//  2) SSAO HAI TẦNG (che khuất môi trường trong không gian màn hình, GTAO rút gọn theo bán cầu pháp tuyến): tầng TIẾP XÚC (bán kính ≈ 0,5 % khoảng cách, 0,35–5 m:
//     chân tường, mép mái, người/quân trên đất) + tầng RỘNG (≈ 3 % khoảng cách, 3–45 m: hẻm, sân trong, chân Rock). Lượt pháp tuyến + độ sâu dùng CHÍNH vật liệu cảnh
//     (uMask = 2 — cùng cơ chế mặt nạ nội dung, nên địa hình hạ theo năm, quân mọc theo ngày… đều đúng), không vật liệu thay thế. Khử nhiễu 4×4 theo độ sâu.
//     Nhân vào bộ tích luỹ HDR (trước tone map) — nước, trời, khói không nhận AO.
//  Không sửa design/cong3/shared/post.js (dùng chung với LL/K2 — khung vàng steel/ll08 giữ nguyên).
import { THREE } from './core.js';

// ---------- 1) bóng đổ khít khung nhìn ----------
export function fitShadowView(sun, sunDir, cam, { dmax = 3000, zTop = 460, res = 8192, pad = 30 } = {}) {
  cam.updateMatrixWorld(); const ivp = new THREE.Matrix4().multiplyMatrices(cam.matrixWorld, cam.projectionMatrixInverse), o = cam.position, pts = [o.clone()];
  for (let j = 0; j <= 6; j++) for (let i = 0; i <= 8; i++) {
    const d = new THREE.Vector3(i / 8 * 2 - 1, j / 6 * 2 - 1, 0.5).applyMatrix4(ivp).sub(o).normalize();
    let t = dmax; if (d.y < -1e-4) t = Math.min(t, (0 - o.y) / d.y); else if (d.y > 1e-4) t = Math.min(t, Math.max(0, (zTop - o.y) / d.y));
    pts.push(o.clone().addScaledVector(d, Math.max(t, 1)));
    pts.push(o.clone().addScaledVector(d, Math.min(t, 60)));
  }
  // khung nhìn ↔ hệ nguồn sáng: tâm = tâm khối điểm; nguồn ở xa theo hướng mặt trời
  const c = pts.reduce((a, p) => a.add(p), new THREE.Vector3()).multiplyScalar(1 / pts.length);
  const sc = sun.shadow.camera; sun.target.position.copy(c); sun.position.copy(c).addScaledVector(sunDir, 9000); sun.target.updateMatrixWorld(); sun.updateMatrixWorld();
  sc.position.copy(sun.position); sc.lookAt(c); sc.updateMatrixWorld(); const inv = sc.matrixWorldInverse;
  let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, z0 = 1e9, z1 = -1e9;
  for (const p of pts) { const q = p.clone().applyMatrix4(inv); x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y); z0 = Math.min(z0, q.z); z1 = Math.max(z1, q.z); }
  x0 -= pad; x1 += pad; y0 -= pad; y1 += pad;
  // khớp lưới texel: cạnh hộp lượng tử hoá theo bậc 4 % rồi mép theo texel → bóng không "bơi" khi máy trôi chậm
  const ext = Math.max(x1 - x0, y1 - y0), q = Math.pow(1.04, Math.ceil(Math.log(ext) / Math.log(1.04))), tx = q / res;
  const cx = Math.round((x0 + x1) / 2 / tx) * tx, cy = Math.round((y0 + y1) / 2 / tx) * tx;
  Object.assign(sc, { left: cx - q / 2, right: cx + q / 2, bottom: cy - q / 2, top: cy + q / 2, near: Math.max(1, -z1 - 2500), far: -z0 + 200 });
  sc.updateProjectionMatrix();
  return { texel_m: +tx.toFixed(3), ext_m: Math.round(q), key: [Math.round(cx / tx), Math.round(cy / tx), Math.round(q), Math.round(c.x), Math.round(c.z)].join(',') };
}

// ---------- 2) SSAO hai tầng ----------
const VS = `in vec3 position; out vec2 vUv; void main(){ vUv = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }`;
function kernel(n, seed) {   // bán cầu (z+) dồn về tâm, tất định
  let s = seed; const R = () => { s = (s * 16807) % 2147483647; return s / 2147483647; }, out = [];
  for (let i = 0; i < n; i++) { const u = R(), v = R(), th = 2 * Math.PI * u, z = Math.sqrt(1 - v), r = Math.sqrt(v); let k = (i + 0.5) / n; k = 0.15 + 0.85 * k * k;
    out.push(new THREE.Vector3(Math.cos(th) * r * k, Math.sin(th) * r * k, z * k)); }
  return out;
}
export function makeSSAO(R, W, H, opt = {}) {
  const O = Object.assign({ n1: 12, n2: 10, k1: 0.005, r1: [0.35, 5.0], k2: 0.03, r2: [3.0, 45.0], s1: 0.85, s2: 0.6, strength: 1.0, maxD: 9000 }, opt);
  const dt = new THREE.DepthTexture(W, H); dt.type = THREE.FloatType;
  const nRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType, depthTexture: dt, depthBuffer: true });
  const aRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType }), bRT = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType });
  const K1 = kernel(O.n1, 7), K2 = kernel(O.n2, 1301);
  const U = { tN: { value: nRT.texture }, tD: { value: dt }, uP: { value: new THREE.Matrix4() }, uPI: { value: new THREE.Matrix4() }, res: { value: new THREE.Vector2(W, H) },
    K1: { value: K1 }, K2: { value: K2 }, uK: { value: new THREE.Vector4(O.k1, O.k2, O.s1, O.s2) }, uR: { value: new THREE.Vector4(O.r1[0], O.r1[1], O.r2[0], O.r2[1]) }, uMaxD: { value: O.maxD } };
  const aoMat = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, uniforms: U, vertexShader: VS, depthTest: false, depthWrite: false,
    fragmentShader: `precision highp float; uniform sampler2D tN; uniform highp sampler2D tD; uniform mat4 uP, uPI; uniform vec2 res; uniform vec3 K1[${O.n1}]; uniform vec3 K2[${O.n2}]; uniform vec4 uK, uR; uniform float uMaxD; in vec2 vUv; out vec4 o;
      vec3 vpos(vec2 uv, float d){ vec4 p = uPI * vec4(uv * 2.0 - 1.0, d * 2.0 - 1.0, 1.0); return p.xyz / p.w; }
      float ign(vec2 p){ return fract(52.9829189 * fract(dot(p, vec2(0.06711056, 0.00583715)))); }
      float occ(vec3 P, mat3 TBN, float r, int which){ float s = 0.0; int n = which == 0 ? ${O.n1} : ${O.n2};
        for (int i = 0; i < ${Math.max(O.n1, O.n2)}; i++){ if (i >= n) break; vec3 k = which == 0 ? K1[i] : K2[i]; vec3 S = P + TBN * k * r; vec4 c = uP * vec4(S, 1.0); vec2 uv = c.xy / c.w * 0.5 + 0.5;
          if (uv.x < 0.0 || uv.y < 0.0 || uv.x > 1.0 || uv.y > 1.0) continue; float d = texture(tD, uv).r; if (d >= 0.99999) continue; float sz = vpos(uv, d).z;
          float rc = smoothstep(0.0, 1.0, r / max(abs(P.z - sz), 1e-3)); s += (sz >= S.z + r * 0.04 ? 1.0 : 0.0) * rc; }
        return s / float(n); }
      void main(){ float d = texture(tD, vUv).r; if (d >= 0.99999) { o = vec4(1.0); return; } vec3 P = vpos(vUv, d); float z = -P.z; if (z > uMaxD) { o = vec4(1.0); return; }
        vec3 N = normalize(texture(tN, vUv).rgb * 2.0 - 1.0); float a = ign(gl_FragCoord.xy) * 6.2831853; vec3 rv = vec3(cos(a), sin(a), 0.0);
        vec3 T = normalize(rv - N * dot(rv, N)), B = cross(N, T); mat3 TBN = mat3(T, B, N);
        float r1 = clamp(uK.x * z, uR.x, uR.y), r2 = clamp(uK.y * z, uR.z, uR.w);
        float a1 = 1.0 - uK.z * occ(P, TBN, r1, 0), a2 = 1.0 - uK.w * occ(P, TBN, r2, 1);
        float fade = 1.0 - smoothstep(uMaxD * 0.6, uMaxD, z);   // AO mờ dần ở xa (chân trời, Rock xa)
        o = vec4(vec3(mix(1.0, a1 * a2, fade)), 1.0); }` });
  const blurMat = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, uniforms: { tA: { value: aRT.texture }, tD: { value: dt }, res: U.res, uPI: U.uPI, uS: { value: O.strength } }, vertexShader: VS, depthTest: false, depthWrite: false,
    // khử nhiễu 4×4 (khớp chu kỳ xoay ign) có trọng theo độ sâu; ra = AO cuối (nhân), alpha 1
    fragmentShader: `precision highp float; uniform sampler2D tA; uniform highp sampler2D tD; uniform vec2 res; uniform mat4 uPI; uniform float uS; in vec2 vUv; out vec4 o;
      float lz(vec2 uv){ float d = texture(tD, uv).r; vec4 p = uPI * vec4(uv * 2.0 - 1.0, d * 2.0 - 1.0, 1.0); return -p.z / p.w; }
      void main(){ float z0 = lz(vUv), s = 0.0, w = 0.0; for (int j = -2; j < 2; j++) for (int i = -2; i < 2; i++){ vec2 uv = vUv + (vec2(i, j) + 0.5) / res; float wz = exp(-abs(lz(uv) - z0) / max(0.02 * z0, 0.05)); s += texture(tA, uv).r * wz; w += wz; }
        float a = mix(1.0, s / max(w, 1e-4), uS); o = vec4(vec3(a), 1.0); }`,
    // nhân vào bộ tích luỹ: dst.rgb *= a (alpha giữ)
    blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.ZeroFactor, blendDst: THREE.SrcColorFactor, blendSrcAlpha: THREE.ZeroFactor, blendDstAlpha: THREE.OneFactor, transparent: true });
  const quad = (m) => { const s = new THREE.Scene(); const q = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m); q.frustumCulled = false; s.add(q); return s; };
  const aoScene = quad(aoMat), blurScene = quad(blurMat), qc = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  let lastMs = 0, dbg = null;
  return {
    // hide: vật KHÔNG vào lượt AO (nước, trời, khói/sprite); Umask: uniform mặt nạ dùng chung (uMask = 2 → pháp tuyến)
    apply(scene, cam, accRT, Umask, hide = []) {
      const t0 = performance.now(), vis = hide.filter((x) => x && x.visible); for (const x of vis) x.visible = false;
      const sm = R.shadowMap.enabled; R.shadowMap.enabled = false; const cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(); const fog = scene.fog; scene.fog = null;
      Umask.value = 2; R.setRenderTarget(nRT); R.setClearColor(0x8080ff, 1); R.clear(); R.render(scene, cam); Umask.value = 0;
      scene.fog = fog; R.shadowMap.enabled = sm; R.setClearColor(cc, ca); for (const x of vis) x.visible = true;
      U.uP.value.copy(cam.projectionMatrix); U.uPI.value.copy(cam.projectionMatrixInverse);
      R.setRenderTarget(aRT); R.render(aoScene, qc);
      R.setRenderTarget(accRT); const ac = R.autoClear; R.autoClear = false; R.render(blurScene, qc); R.autoClear = ac;
      if (dbg) { R.setRenderTarget(dbg); R.render(blurScene, qc); }
      R.setRenderTarget(null); lastMs = performance.now() - t0; return lastMs;
    },
    ms: () => lastMs, opt: O, aRT, nRT,
    // đọc ảnh AO (0..255, 1/4 cỡ) để đo/kiểm — chỉ dùng khi chẩn đoán
    readAO() { const w = W, h = H, px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(aRT, 0, 0, w, h, px); let s = 0; for (let i = 0; i < px.length; i += 4) s += px[i]; return { mean: +(s / (w * h) / 255).toFixed(4) }; },
  };
}

// ---------- 3) chỉnh màu V6 (thêm vào GRADE của lut.js, bật bằng uV6) ----------
//  đường cong S nhẹ quanh trung tính (tương phản phim), tách tông bóng lạnh/ánh sáng ấm (nhẹ), "clarity" (tương phản cục bộ trên độ sáng, bán kính 3 px) —
//  không đổi bão hoà trung bình (đo lại sau: trung vị ≥ 0,40).
export const GRADE_V6 = `
vec3 v6grade(vec3 c, vec2 uv){
  float Y = dot(c, vec3(0.2126, 0.7152, 0.0722));
  // clarity: độ sáng trừ trung bình 3 px (đọc lại bộ tích luỹ đã tone map) → tăng tương phản tầm trung, không đụng cạnh cứng (giới hạn)
  vec2 px = 3.0 / res; float b = 0.0; for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) { vec3 s = pow(tonemap(max(texture(tAcc, uv + vec2(i, j) * px).rgb, 0.0)), vec3(1.0 / 2.2)); b += dot(s, vec3(0.2126, 0.7152, 0.0722)); }
  b /= 9.0; float dl = clamp(Y - b, -0.06, 0.06) * uV6c.x; c += dl;
  // S nhẹ: y = x + k·x(1−x)(x−0,45)
  c = c + uV6c.y * c * (1.0 - c) * (c - 0.45) * 2.0;
  // tách tông: bóng ngả lam-lục nhẹ, sáng ngả ấm
  float Y2 = dot(c, vec3(0.2126, 0.7152, 0.0722)), ws = 1.0 - smoothstep(0.05, 0.40, Y2), wh = smoothstep(0.55, 0.95, Y2);
  c += uV6c.z * (ws * vec3(-0.010, 0.002, 0.016) + wh * vec3(0.016, 0.006, -0.012));
  return max(c, 0.0); }`;

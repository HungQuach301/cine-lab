// Cine Lab · Cổng 3 v3 — độ sâu trường ảnh (DOF) hậu kỳ, dùng chung. Sửa L1 (đốm sáng nhoè vỡ thành ô vuông) và
// L2 (ngón tay gần máy nhân lớp): vòng 2 làm DOF bằng rung khẩu độ 8 mẫu → vật nhoè = 8 bản sao rời (L2), và cửa sổ
// chữ nhật nhoè thành chồng chữ nhật, rồi Kuwahara của lớp vẽ san phẳng thành bậc (L1).
// Cách mới: máy quay KHÔNG rung khẩu độ (mẫu tích luỹ chỉ còn khử răng cưa + bóng mềm). Sau lớp vẽ, trước pass cuối
// (tone map, grade, grain — grain KHÔNG bị nhoè):
//  1) CoC (bán kính vòng nhoè, px) theo thấu kính mỏng từ độ sâu nhìn thật (G-buffer của lớp vẽ), cùng công thức hình học
//     với rung khẩu độ cũ: c = A·|d − F|/d · Hpx / (2F·tan(fov/2)). Nửa độ phân giải: màu (lọc 4 điểm) + CoC có dấu.
//  2) Ô 8×8 (1/16 khung): CoC lớn nhất, nới 3×3 khi đọc → bán kính gom của mỗi điểm (để tiền cảnh nhoè tràn ra nền nét).
//  3) Gom (scatter-as-gather) 64 mẫu trong ĐĨA TRÒN (xoắn ốc vàng, xoay theo điểm bằng nhiễu IGN): mẫu j phủ điểm này nếu
//     c_j ≥ khoảng cách; mẫu ở SAU điểm đang xét bị giới hạn bởi CoC của điểm (nền không tràn lên tiền cảnh nét);
//     trọng số 1/c_j² (năng lượng một điểm trải đều trên đĩa) → đốm sáng tròn, sáng đều, biên rõ như ống kính thật.
//  4) Lọc lều 3×3 nửa độ phân giải (xoá nhiễu xoay mẫu; không để lộ lưới mẫu), rồi ghép với ảnh nét ở toàn độ phân giải
//     theo CoC và tỷ lệ tiền cảnh tràn sang.
import * as THREE from './node_modules/three/build/three.module.js';

const VS = `in vec3 position; out vec2 vUv; void main(){ vUv = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }`;
const HDR = `precision highp float; in vec2 vUv; out vec4 o;`;
const NT = 64;

export function createDOF(renderer, W, H, pipe) {
  const fOpt = { type: THREE.FloatType, format: THREE.RGBAFormat, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, colorSpace: THREE.LinearSRGBColorSpace };
  const nOpt = { ...fOpt, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter };
  const hw = Math.ceil(W / 2), hh = Math.ceil(H / 2), tw = Math.ceil(W / 16), th = Math.ceil(H / 16);
  const halfRT = new THREE.WebGLRenderTarget(hw, hh, nOpt), gathRT = new THREE.WebGLRenderTarget(hw, hh, fOpt), tentRT = new THREE.WebGLRenderTarget(hw, hh, fOpt);
  const tileRT = new THREE.WebGLRenderTarget(tw, th, nOpt), outRT = new THREE.WebGLRenderTarget(W, H, fOpt);
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2)); const qs = new THREE.Scene(); qs.add(quad);
  const mk = (fs, uniforms) => new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, vertexShader: VS, fragmentShader: HDR + fs, uniforms, depthTest: false, depthWrite: false });
  const run = (m, t) => { quad.material = m; renderer.setRenderTarget(t); renderer.render(qs, cam); };
  const U = () => ({ A: { value: 0 }, F: { value: 1 }, K: { value: 1 } });   // A khẩu độ (m), F khoảng lấy nét (m), K = Hpx/(2F·tan(fov/2))
  const COC = `uniform float A, F, K; float coc(float d){ d = d > 0.0 ? d : 1e4; return A * (d - F) / d * K; }`;   // có dấu: âm = trước điểm nét (px toàn khung)

  const pre = mk(`uniform sampler2D tSrc, tG; uniform vec2 px; ${COC}
    void main(){
      vec3 c = 0.25 * (texture(tSrc, vUv + vec2(-0.5, -0.5) * px).rgb + texture(tSrc, vUv + vec2(0.5, -0.5) * px).rgb
                     + texture(tSrc, vUv + vec2(-0.5, 0.5) * px).rgb + texture(tSrc, vUv + vec2(0.5, 0.5) * px).rgb);
      float d = texture(tG, vUv).x;
      o = vec4(c, coc(d)); }`, { tSrc: { value: null }, tG: { value: null }, px: { value: new THREE.Vector2(1 / W, 1 / H) }, ...U() });

  const tile = mk(`uniform sampler2D tHalf; uniform vec2 hpx;
    void main(){ float m = 0.0;
      for (int y = 0; y < 8; y++) for (int x = 0; x < 8; x++) m = max(m, abs(texture(tHalf, vUv + (vec2(x, y) - 3.5) * hpx).a));
      o = vec4(m, 0.0, 0.0, 1.0); }`, { tHalf: { value: halfRT.texture }, hpx: { value: new THREE.Vector2(1 / hw, 1 / hh) } });

  const gath = mk(`uniform sampler2D tHalf, tTile; uniform vec2 hpx, tpx; uniform float maxR;
    const int NT = ${NT};
    void main(){
      float R = 0.0;
      for (int y = -1; y <= 1; y++) for (int x = -1; x <= 1; x++) R = max(R, texture(tTile, vUv + vec2(x, y) * tpx).r);
      R = min(R, maxR);
      vec4 c0 = texture(tHalf, vUv); float cc = abs(c0.a);
      float w0 = 1.0 / max(cc * cc, 1.0); vec3 s = c0.rgb * w0; float ws = w0, fg = 0.0, fgw = 0.0;
      if (R > 1.0) {
        float rot = 6.2831853 * fract(52.9829189 * fract(dot(gl_FragCoord.xy, vec2(0.06711056, 0.00583715))));   // IGN: xoay đĩa mẫu theo điểm
        for (int i = 0; i < NT; i++) {
          float fi = float(i) + 0.5, rr = sqrt(fi / float(NT)) * R, a = fi * 2.3999632 + rot;
          vec2 off = rr * vec2(cos(a), sin(a));                       // px toàn khung
          vec4 t = texture(tHalf, vUv + off * 0.5 * hpx);
          float ct = abs(t.a);
          if (t.a > c0.a) ct = min(ct, cc);                            // mẫu ở sau: không tràn lên điểm gần hơn
          float cov = clamp(ct - rr + 1.0, 0.0, 1.0);
          float w = cov / max(ct * ct, 1.0);
          s += t.rgb * w; ws += w;
          if (t.a < c0.a - 1.0) { fg += cov; } fgw += 1.0;
        }
      }
      o = vec4(s / ws, fgw > 0.0 ? fg / fgw : 0.0); }`, { tHalf: { value: halfRT.texture }, tTile: { value: tileRT.texture }, hpx: { value: new THREE.Vector2(1 / hw, 1 / hh) },
    tpx: { value: new THREE.Vector2(1 / tw, 1 / th) }, maxR: { value: 48 } });

  const tent = mk(`uniform sampler2D tSrc; uniform vec2 hpx;
    void main(){ vec4 s = texture(tSrc, vUv) * 4.0;
      s += (texture(tSrc, vUv + vec2(hpx.x, 0.0)) + texture(tSrc, vUv - vec2(hpx.x, 0.0)) + texture(tSrc, vUv + vec2(0.0, hpx.y)) + texture(tSrc, vUv - vec2(0.0, hpx.y))) * 2.0;
      s += texture(tSrc, vUv + hpx) + texture(tSrc, vUv - hpx) + texture(tSrc, vUv + vec2(hpx.x, -hpx.y)) + texture(tSrc, vUv + vec2(-hpx.x, hpx.y));
      o = s / 16.0; }`, { tSrc: { value: gathRT.texture }, hpx: { value: new THREE.Vector2(1 / hw, 1 / hh) } });

  const comp = mk(`uniform sampler2D tSrc, tBlur, tG; ${COC}
    void main(){
      vec3 sharp = texture(tSrc, vUv).rgb; vec4 b = texture(tBlur, vUv);
      float c = abs(coc(texture(tG, vUv).x));
      float k = max(smoothstep(0.6, 2.2, c), clamp(b.a * 3.0, 0.0, 1.0));
      o = vec4(mix(sharp, b.rgb, k), 1.0); }`, { tSrc: { value: null }, tBlur: { value: tentRT.texture }, tG: { value: null }, ...U() });

  // p = { aperture (m, bán kính), focusD (m), cam } — cùng tham số hình học với rung khẩu độ cũ.
  function apply(srcTex, gTex, p) {
    const K = H / (2 * p.focusD * Math.tan(THREE.MathUtils.degToRad(p.cam.fov) / 2));
    for (const m of [pre, comp]) { m.uniforms.A.value = p.aperture; m.uniforms.F.value = p.focusD; m.uniforms.K.value = K; }
    pre.uniforms.tSrc.value = srcTex; pre.uniforms.tG.value = gTex; run(pre, halfRT);
    run(tile, tileRT); run(gath, gathRT); run(tent, tentRT);
    comp.uniforms.tSrc.value = srcTex; comp.uniforms.tG.value = gTex; run(comp, outRT);
    pipe.outMat.uniforms.tAcc.value = outRT.texture;
  }
  return { apply, outRT };
}

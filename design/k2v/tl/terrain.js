// K2V tl · NỀN SỐNG (lớp 3 chuẩn hình): địa hình DTM 20 m (trong) + 60 m (ngoài), phủ mặt đất Sentinel-2 theo NĂM
// (nền tự nhiên ↔ nền đô thị theo năm đô thị hoá), đá vôi trên vách dốc, chi tiết gần, AO tiếp đất nướng sẵn theo năm,
// đất khai hoang chỉ nổi lên từ năm có bằng chứng (years.png kênh B/A). Mặt nước: water.js. Chữ/thẻ: text.js.
import { THREE, GLSL_YEAR, GLSL_NOISE, loadF32, tex, noiseTex } from './core.js';

export const GLSL_LAND = `${GLSL_YEAR}
// năm có đất: 0 = luôn; 1941 = khai hoang đường băng (đủ 1943, HMGoG 199/2018); mốc khác: nổi trong 1,5 năm trước mốc; 9999 = biển
float landK(float ly, float y){ if (ly < 1.0) return 1.0; if (ly > 9000.0) return 0.0;
  if (abs(ly - 1941.0) < 0.5) return clamp((y - 1941.0) / 2.0, 0.0, 1.0); return clamp((y - (ly - 1.5)) / 1.5, 0.0, 1.0); }`;

// V5b-2c (lệnh V0 18/10, mục 5): VÁCH BẮC ROCK. Copernicus GLO-30 (30 m) làm mượt vách: đỉnh gói 359 m (thật ≈ 412–426 m), dốc lớn nhất ≈ 54°, nên Rock
//  nhìn từ bắc thành "đồi tròn phủ cỏ". opt.cliff (cảnh tự khai TERRAIN.cliff): (1) làm sắc vách bắc bằng unsharp DEM trong hộp vách (dốc > 25°, mặt quay bắc;
//  σ ≈ 40 m, k, nâng ≤ capUp m, chân không xuống dưới 1 m) — XẤP XỈ hình thái (không phải số đo mới), ghi báo cáo; (2) vật liệu VÁCH ĐÁ VÔI từ dốc > ~30°
//  (trước: > ~63°) với vân lớp đá + khe nứt dọc theo mặt đứng. Cảnh không khai → địa hình/vật liệu như cũ (golden giữ nguyên).
function sharpenCliff(H, R, Cn, e0, n1, st, o) {
  const [E0, N0, E1, N1] = o.box || [-100, -1100, 950, -420], k = o.k ?? 1.3, cap = o.capUp ?? 55, it = o.iters ?? 2;
  const r0 = Math.max(1, Math.floor((n1 - N1) / st)), r1 = Math.min(R - 2, Math.ceil((n1 - N0) / st)), c0 = Math.max(1, Math.floor((E0 - e0) / st)), c1 = Math.min(Cn - 2, Math.ceil((E1 - e0) / st));
  let B = Float32Array.from(H); const tmp = new Float32Array(H.length);
  for (let i = 0; i < it; i++) { for (let r = r0 - 3; r <= r1 + 3; r++) for (let c = c0 - 3; c <= c1 + 3; c++) { let a = 0; for (let d = -2; d <= 2; d++) a += B[r * Cn + c + d] * [1, 4, 6, 4, 1][d + 2]; tmp[r * Cn + c] = a / 16; }
    for (let r = r0 - 1; r <= r1 + 1; r++) for (let c = c0 - 1; c <= c1 + 1; c++) { let a = 0; for (let d = -2; d <= 2; d++) a += tmp[(r + d) * Cn + c] * [1, 4, 6, 4, 1][d + 2]; B[r * Cn + c] = a / 16; } }
  let n = 0, up = 0, dn = 0;
  for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) { const i = r * Cn + c, dzN = (H[i - Cn] - H[i + Cn]) / (2 * st), dzE = (H[i + 1] - H[i - 1]) / (2 * st), sl = Math.atan(Math.hypot(dzN, dzE)) * 57.3;
    if (sl < 25 || dzN > -0.25) continue;   // chỉ mặt dốc quay bắc (cao lên khi đi về nam)
    const w = Math.min(1, (sl - 25) / 10), d = (H[i] - B[i]) * k * w, v = Math.max(Math.min(H[i], 1.0), Math.min(H[i] + cap, H[i] + d));
    tmp[i] = v; n++; up = Math.max(up, v - H[i]); dn = Math.min(dn, v - H[i]); }
  for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) { const i = r * Cn + c, dzN = (H[i - Cn] - H[i + Cn]) / (2 * st), dzE = (H[i + 1] - H[i - 1]) / (2 * st), sl = Math.atan(Math.hypot(dzN, dzE)) * 57.3;
    if (!(sl < 25 || dzN > -0.25)) H[i] = tmp[i]; }
  return { o_sua: n, nang_max_m: +up.toFixed(1), ha_max_m: +dn.toFixed(1) };
}
export async function makeTerrain(base, M, U, TO = {}) {
  const [e0, n0, e1, n1] = M.ext, [R, Cn] = M.terrain_shape, st = M.step_terrain;
  const Hh = await loadF32(base + 'terrain.f32');
  const cliffStat = TO.cliff ? sharpenCliff(Hh, R, Cn, e0, n1, st, TO.cliff === true ? {} : TO.cliff) : null;
  // V5b-2d (C2-9): ĐỐI CHIẾU ẢNH PD (LoC 2025710362 "Gibraltar. Rock from neutral ground", c. 1900–10, "No known restrictions on publication"): vách bắc là vách gần
  //  đứng, đỉnh bắc cao hơn hẳn DEM (Copernicus 359 m; thật: Rock Gun ≈ 412 m, O'Hara's ≈ 426 m) → nâng phần cao của Rock theo luỹ thừa (chân giữ nguyên) để đỉnh = peak m.
  if (cliffStat && TO.cliff.peak) { const [E0, N0, E1, N1] = TO.cliff.peakBox || [-450, -5200, 1600, -350], base = TO.cliff.peakBase ?? 120;
    let mx = 0; for (let r = 0; r < R; r++) for (let c = 0; c < Cn; c++) { const e = e0 + c * st, n = n1 - r * st; if (e > E0 && e < E1 && n > N0 && n < N1) mx = Math.max(mx, Hh[r * Cn + c]); }
    let k = 0; if (mx > base + 1) for (let r = 0; r < R; r++) for (let c = 0; c < Cn; c++) { const e = e0 + c * st, n = n1 - r * st, i = r * Cn + c; if (!(e > E0 && e < E1 && n > N0 && n < N1) || Hh[i] <= base) continue;
      Hh[i] += Math.pow((Hh[i] - base) / (mx - base), 1.6) * (TO.cliff.peak - mx); k++; }
    Object.assign(cliffStat, { dinh_dem_m: +mx.toFixed(1), dinh_moi_m: TO.cliff.peak, o_nang: k, nguon_anh: 'LoC 2025710362 (PD — No known restrictions)' }); }
  const hAt = (e, n) => { const fc = Math.max(0, Math.min(Cn - 1.001, (e - e0) / st)), fr = Math.max(0, Math.min(R - 1.001, (n1 - n) / st));
    const c = Math.floor(fc), r = Math.floor(fr), a = fc - c, b = fr - r, g = (rr, cc) => Hh[rr * Cn + cc];
    return (g(r, c) * (1 - a) + g(r, c + 1) * a) * (1 - b) + (g(r + 1, c) * (1 - a) + g(r + 1, c + 1) * a) * b; };
  const [tNat, tUrb, tYears, tAO, tCls] = await Promise.all([tex(base + 'ground_nat.jpg'), tex(base + 'ground_urb.jpg'),
    tex(base + 'years.png', { srgb: false, nearest: true }), tex(base + 'ao.png', { srgb: false }), tex(base + 'cls.png', { srgb: false, nearest: true })]);
  const [Gh, Gw] = M.ground_shape;
  const uni = { uYear: U.uYear, uDim: U.uDim, tNat: { value: tNat }, tUrb: { value: tUrb }, tYears: { value: tYears }, tAO: { value: tAO }, tCls: { value: tCls }, uNearK: { value: U.groundNear ?? 1 },
    uExt: { value: new THREE.Vector4(e0 - 5, n0 - 5, Gw * 10, Gh * 10) }, tNoise: { value: noiseTex() }, uBaked: U.uBaked, uAOBox: { value: new THREE.Vector4(...M.ao_box) }, uAOon: U.uAOon, uDetail: { value: 1 },
    tGhostU: { value: new THREE.DataTexture(new Uint8Array([255, 255, 255, 255]), 1, 1) }, uGhostBox: { value: new THREE.Vector4(0, 0, 1, 1) }, uGhostOn: { value: 0 }, uCliff: { value: TO.cliff ? 1 : 0 } };   // V5b-2b: nền đô thị theo vùng ghost (layers.town1782)
  uni.tGhostU.value.needsUpdate = true;
  const mat = U.lambert ? new THREE.MeshLambertMaterial({ color: 0xffffff }) : new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.96, metalness: 0 });
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, uni, { uMask: U.uMask });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', `#include <common>
      uniform sampler2D tYears; uniform vec4 uExt; uniform float uYear; varying vec3 vWP; varying vec3 vWN; ${GLSL_LAND}`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>
      { vec2 uv = vec2((position.x - uExt.x) / uExt.z, (-position.z - uExt.y) / uExt.w); vec4 yv = textureLod(tYears, uv, 0.0);
        float k = landK(decYear(yv.ba), uYear); transformed.y = mix(min(transformed.y, -10.0), transformed.y, k); }
      vWP = (modelMatrix * vec4(transformed, 1.0)).xyz; vWN = normalize(mat3(modelMatrix) * objectNormal);`);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
      uniform sampler2D tNat, tUrb, tYears, tAO, tNoise, tCls, tGhostU; uniform vec4 uGhostBox; uniform float uGhostOn, uCliff; uniform vec4 uExt, uAOBox; uniform float uYear, uDim, uAOon, uDetail, uBaked, uNearK, uMask; varying vec3 vWP; varying vec3 vWN;
      ${GLSL_YEAR} ${GLSL_NOISE}
      float fbmT(vec2 p){ if (uBaked < 0.5) return fbm(p); vec2 q = mat2(0.80, -0.60, 0.60, 0.80) * p * 0.173 + 0.37; return 0.6 * texture(tNoise, p * 0.25).r + 0.4 * texture(tNoise, q).b; }   // nhiễu nướng sẵn chống lặp ô: 2 mẫu, tỉ lệ không thông ước + xoay miền
      // V5b-1b · VẬT LIỆU THỦ TỤC THEO LỚP (build_scene.build_classes): có biến thiên tầm trung + chi tiết nhỏ; mờ dần chi tiết theo fwidth (chống răng cưa)
      float fw(vec2 p, float f){ return 1.0 - clamp(length(fwidth(p * f)) * 1.2, 0.0, 1.0); }
      float lineAA(float x, float w, float f){ float d = abs(fract(x) - 0.5); return smoothstep(0.5 - w - f, 0.5 - w, d); }
      // nhiễu cho vật liệu nền: thủ tục (fbm/vn) hoặc NƯỚNG SẴN (tech.baked: 1 lần lấy mẫu kết cấu thay 4 tầng vn) — đo ở báo cáo V5B1B §7
      float FBM(vec2 p){ return uBaked > 0.5 ? texture(tNoise, p * 0.25).r : fbm(p); }
      float VN(vec2 p){ return uBaked > 0.5 ? texture(tNoise, p * 0.03125).a : vn(p); }
      // V5b-2a · chi tiết CẬN CẢNH cho bay thấp ≤ 120 m (cú liên hoàn): cụm cỏ 0,7–1,5 m (tối, có tâm sáng), hạt cỏ 0,3 m, bụi thấp 2–4 m lẻ — mờ dần khi
      // nhỏ hơn điểm ảnh (fw) nên không răng cưa/nhấp nháy ở xa; chỉ vật liệu cỏ (cỏ khô, đồng cỏ eo đất) — phong cách hoá, không phải dữ liệu mới
      vec3 tufts(vec3 s, vec2 p, vec3 bushC){
        vec2 q = p * 0.9, ci = floor(q), cf = fract(q) - 0.5; float dt = length(cf - (vec2(h21(ci), h21(ci + 7.3)) - 0.5) * 0.6);
        float k1 = fw(p, 0.9), tuft = (1.0 - smoothstep(0.16, 0.40, dt)) * step(0.35, h21(ci + 2.1)) * k1;
        s *= 1.0 - 0.30 * tuft + 0.10 * (1.0 - smoothstep(0.0, 0.12, dt)) * k1;
        s *= 0.88 + 0.24 * vn(p * 3.1) * fw(p, 3.1);
        vec2 b = p * 0.3, bi = floor(b), bf = fract(b) - 0.5; float bd = length(bf - (vec2(h21(bi + 1.7), h21(bi + 9.1)) - 0.5) * 0.5);
        float bush = (1.0 - smoothstep(0.09, 0.20, bd)) * step(0.70, h21(bi + 4.4)) * fw(p, 0.3);
        return mix(s, bushC * (0.8 + 0.4 * vn(p * 1.3)), bush * 0.8); }
      vec3 matC(float c, vec2 p, float dc, float sl){
        float m1 = FBM(p * 0.045), m2 = VN(p * 0.31), mi = VN(p * 1.7) * fw(p, 1.7), m3 = FBM(p * 0.012 + 4.0);
        if (c < 1.5) {   // 1 cát bãi: gợn cát, vệt ướt sát mép nước, vỏ sò
          vec3 s = mix(vec3(0.90, 0.81, 0.62), vec3(0.84, 0.74, 0.55), m1); s *= 0.95 + 0.06 * sin(p.x * 1.1 + p.y * 0.7 + m2 * 6.0) * fw(p, 0.3) + 0.05 * mi;
          s = mix(s, vec3(0.62, 0.55, 0.43), smoothstep(10.0, 3.0, dc)); return s; }
        if (c < 2.5) {   // 2 cỏ khô: vàng rơm, búi tối, đất lộ
          vec3 s = mix(vec3(0.70, 0.64, 0.38), vec3(0.56, 0.56, 0.30), m1); s = mix(s, vec3(0.66, 0.56, 0.40), smoothstep(0.62, 0.8, m2) * 0.6);
          float sh = smoothstep(0.58, 0.70, FBM(p * 0.05 + 3.0) * 0.6 + VN(p * 0.6) * 0.45); s = mix(s, vec3(0.30, 0.38, 0.18) * (0.85 + 0.3 * mi), sh * 0.7);   // garrigue: cụm bụi lẻ trên cỏ khô
          return tufts(s, p, vec3(0.30, 0.36, 0.17)) * (0.84 + 0.26 * mi); }
        if (c < 3.5) {   // 3 maquis: cụm bụi xanh đậm, khe đá vôi/đất giữa cụm
          float cl = FBM(p * 0.11 + 2.0); vec3 s = mix(vec3(0.17, 0.29, 0.12), vec3(0.32, 0.40, 0.17), m2 * 0.7 + m3 * 0.5);
          s = mix(s, vec3(0.62, 0.58, 0.48), smoothstep(0.42, 0.30, cl) * 0.85); return s * (0.80 + 0.32 * mi); }
        if (c < 4.5) {   // 4 đá vôi: tầng, vết nứt, địa y
          float st = FBM(vec2(p.x * 0.05 + p.y * 0.03, p.y * 0.4) ); vec3 s = mix(vec3(0.76, 0.73, 0.66), vec3(0.62, 0.60, 0.55), st);
          float cr = VN(p * 0.6) * VN(p * 0.23 + 3.0); s *= 1.0 - 0.35 * smoothstep(0.35, 0.6, cr) * fw(p, 0.6);   // hốc tối
          s = mix(s, vec3(0.25, 0.34, 0.16), smoothstep(0.62, 0.78, FBM(p * 0.14 + 5.0)) * 0.8);   // bụi lẻ trong đá
          return s * (0.84 + 0.24 * mi); }
        if (c < 5.5) {   // 5 ruộng/vườn: luống theo hướng băm từng thửa 60 m
          vec2 cell = floor(p / 60.0); float a = h21(cell) * 3.14; vec2 d = vec2(cos(a), sin(a)); float r = dot(p, d) / 1.6;
          vec3 s = mix(vec3(0.46, 0.38, 0.26), vec3(0.36, 0.48, 0.20), step(0.5, h21(cell + 3.0))); return s * (0.82 + 0.22 * lineAA(r, 0.22, 0.05) * fw(p, 0.6)) * (0.9 + 0.15 * m1); }
        if (c < 6.5) { vec3 s = vec3(0.27, 0.28, 0.30) * (0.88 + 0.2 * m1) * (0.93 + 0.12 * mi); return mix(s, vec3(0.20, 0.20, 0.22), smoothstep(0.6, 0.75, m2) * 0.5); }   // 6 nhựa: vá, đá dăm
        if (c < 7.5) {   // 7 nền lát đô thị: tấm 2 m, vết ố, ron
          vec2 g = abs(fract(p / 2.0) - 0.5); float j = (1.0 - smoothstep(0.44, 0.48, max(g.x, g.y))) ; vec3 s = mix(vec3(0.72, 0.69, 0.64), vec3(0.62, 0.60, 0.57), m1); if (uCliff > 0.5) s = mix(vec3(0.78, 0.66, 0.50), vec3(0.68, 0.58, 0.46), m1);   /* V5b-2c: phố 1782 lát đá vôi địa phương (ấm) */
          s *= mix(0.86, 1.0, j * fw(p, 0.5) + (1.0 - fw(p, 0.5))); return s * (0.9 + 0.14 * mi) * (1.0 - 0.15 * smoothstep(0.65, 0.85, m2)); }
        if (c < 8.5) {   // 8 sân thể thao: cỏ xén sọc 5 m
          vec3 s = vec3(0.22, 0.50, 0.22) * (0.9 + 0.12 * step(0.5, fract(p.x / 10.0)) * fw(p, 0.1)); return s * (0.92 + 0.1 * mi); }
        if (c < 9.5) {   // 9 bãi đỗ: nhựa + vạch ô đỗ 2,5 m (theo trục lưới cảnh, phong cách hoá)
          vec3 s = vec3(0.30, 0.31, 0.33) * (0.9 + 0.15 * m1); float ln = 1.0 - lineAA(p.x / 2.5, 0.46, 0.02); float row = step(0.25, fract(p.y / 11.0)) * step(fract(p.y / 11.0), 0.7);
          return mix(s, vec3(0.85, 0.85, 0.82), ln * row * fw(p, 0.4) * 0.8); }
        if (c < 10.5) { vec2 g = abs(fract(p / 6.0) - 0.5); vec3 s = mix(vec3(0.66, 0.65, 0.62), vec3(0.56, 0.56, 0.55), m1) * (1.0 - 0.1 * step(0.47, max(g.x, g.y)) * fw(p, 0.2));   // 10 bê tông cảng
          return s * (1.0 - 0.25 * smoothstep(0.7, 0.85, m2)) * (0.92 + 0.1 * mi); }
        if (c < 11.5) { vec3 s = mix(vec3(0.66, 0.54, 0.40), vec3(0.58, 0.48, 0.36), m1); return s * (0.86 + 0.22 * mi) * (0.95 + 0.08 * sin(p.x * 0.8 + m2 * 5.0)); }   // 11 đất trống
        if (c < 12.5) { vec3 s = mix(vec3(0.28, 0.48, 0.20), vec3(0.36, 0.52, 0.24), m1); return s * (0.86 + 0.2 * mi); }   // 12 cỏ công viên
        // 13 đồng cỏ eo đất (trước đô thị hoá): cỏ xanh-ô liu xen mảng cỏ khô + lối mòn sáng (phong cách hoá theo ảnh LoC c.1900)
        vec3 s = mix(vec3(0.40, 0.48, 0.24), vec3(0.54, 0.55, 0.32), m1); s = mix(s, vec3(0.68, 0.63, 0.40), smoothstep(0.55, 0.72, m3) * 0.7);
        float tr = (1.0 - smoothstep(0.0, 0.005, abs(FBM(p * 0.0032 + 9.0) - 0.5))) * fw(p, 0.25); s = mix(s, vec3(0.76, 0.71, 0.56), tr * 0.5);
        return tufts(s, p, vec3(0.24, 0.30, 0.14)) * (0.84 + 0.24 * mi); }
      // V5b-2c: VÁCH ĐÁ VÔI theo mặt đứng (toạ độ ngang dọc vách × cao độ): lớp đá nghiêng, khe nứt dọc, vệt ố, gờ đá có bụi lẻ
      vec3 cliffC(vec3 w, float sl){ float hz = w.x * 0.83 + w.z * 0.55, y = w.y;
        float bed = FBM(vec2(hz * 0.02, y * 0.11 + hz * 0.012)); vec3 s = mix(vec3(0.80, 0.77, 0.70), vec3(0.64, 0.62, 0.58), smoothstep(0.3, 0.75, bed));
        s = mix(s, vec3(0.86, 0.80, 0.66), smoothstep(0.62, 0.8, FBM(vec2(hz * 0.05, y * 0.03) + 3.0)) * 0.5);   // mảng đá vàng ngà
        float jt = VN(vec2(hz * 0.35, y * 0.025)) * VN(vec2(hz * 0.11 + 4.0, y * 0.01)); s *= 1.0 - 0.45 * smoothstep(0.32, 0.55, jt);   // khe nứt dọc tối
        s *= 1.0 - 0.25 * smoothstep(0.55, 0.8, VN(vec2(hz * 0.08, y * 0.004)));   // vệt nước chảy
        float ledge = smoothstep(0.62, 0.42, sl) * smoothstep(0.55, 0.7, FBM(vec2(hz * 0.04, y * 0.06) + 9.0)); s = mix(s, vec3(0.28, 0.34, 0.17) * (0.8 + 0.4 * VN(w.xz * 0.3)), ledge * 0.75);   // bụi trên gờ
        return s; }`)
      .replace('#include <map_fragment>', `
      vec2 guv = vec2((vWP.x - uExt.x) / uExt.z, (-vWP.z - uExt.y) / uExt.w);
      vec4 yv = texture(tYears, guv); float uy = decYear(yv.rg);
      vec3 cN = texture(tNat, guv).rgb, cU = texture(tUrb, guv).rgb;
      float uk = uy > 9000.0 ? 0.0 : smoothstep(uy - 1.0, uy, uYear);   // nền đô thị không hiện trước năm bằng chứng
      if (uGhostOn > 0.5) { vec2 gq = (vec2(vWP.x, -vWP.z) - uGhostBox.xy) / uGhostBox.zw; uk *= (gq.x < 0.0 || gq.x > 1.0 || gq.y < 0.0 || gq.y > 1.0) ? 0.0 : texture(tGhostU, gq).r; }   /* V5b-2b: mốc có ghost → nền phố CHỈ quanh khối ghost (giãn 25 m), ngoài đó nền tự nhiên như bản đồ (vườn/sườn) */
      // nền tự nhiên (vùng đã vá): thêm biến thiên tầm trung (cát/cỏ khô/bụi) để không phẳng loang
      float nv = fbmT(vWP.xz * 0.006), nv2 = fbmT(vWP.xz * 0.035 + 7.0);
      float flat_ = (1.0 - smoothstep(0.08, 0.2, 1.0 - vWN.y)) * (1.0 - smoothstep(15.0, 40.0, vWP.y));   // chỉ bãi bằng thấp (eo đất), không loang lên sườn Rock
      vec3 cNd = cN * (0.82 + 0.36 * nv * flat_ + 0.18 * (1.0 - flat_)); cNd = mix(cNd, vec3(0.50, 0.50, 0.34), 0.35 * smoothstep(0.45, 0.75, nv2) * flat_); cNd = mix(cNd, vec3(0.80, 0.74, 0.60), 0.25 * smoothstep(0.55, 0.85, 1.0 - nv2) * flat_);
      vec3 g = mix(pow(cNd, vec3(0.9)) * 1.12, cU * 1.08, uk);
      // đá vôi trên vách dốc (Rock): sọc tầng đá + loang (ảnh vệ tinh ở XA)
      float slope = 1.0 - clamp(vWN.y, 0.0, 1.0);
      float strata = 0.82 + 0.22 * fbmT(vec2(vWP.x * 0.015 + vWP.z * 0.011, vWP.y * 0.35)) ;
      vec3 rock = vec3(0.70, 0.67, 0.60) * strata;
      g = mix(g, rock, smoothstep(mix(0.30, 0.16, uCliff), mix(0.55, 0.30, uCliff), slope) * (1.0 - uk));
      if (uCliff > 0.5) g = mix(g, cliffC(vWP, slope), smoothstep(0.16, 0.30, slope) * (1.0 - uk));
      float dd = length(vWP - cameraPosition);
      // V5b-1b: GẦN (≤ 2,6 km, mờ dần tới 3,6 km): vật liệu thủ tục theo lớp, KHÔNG trải ảnh vệ tinh (chỉ tông vùng ≤ 18 % từ mip mờ ~160 m); XA: ảnh vệ tinh như cũ
      float nearK = uNearK * (1.0 - smoothstep(2600.0, 3600.0, dd));
      if (nearK > 0.001) { vec2 p = vec2(vWP.x, -vWP.z); vec2 wv = (vec2(FBM(p * 0.021), FBM(p * 0.021 + 17.0)) - 0.5) * 56.0 + (vec2(VN(p * 0.17), VN(p * 0.17 + 5.0)) - 0.5) * 9.0;   // ranh lớp hữu cơ: cong vênh ±15 m + răng cưa nhỏ
        vec4 cl = texture(tCls, guv + wv / uExt.zw) * 255.0; float c = mix(cl.r, cl.g, step(0.5, uk));
        // V5b-2b (T3 1782): lớp nền đô thị là của 2026 (OSM) — trước 1900 không có nhựa đường, sân thể thao, bãi đỗ, cỏ công viên: đổi về nền lát / đất trống (không bịa vật thể mới)
        if (uYear < 1900.0 && uk > 0.5) { if (c > 5.5 && c < 6.5 || c > 7.5 && c < 8.5) c = 7.0; else if (c > 8.5 && c < 9.5 || c > 11.5 && c < 12.5) c = 11.0; }
        float dc = uYear < 1987.0 ? cl.b : cl.a; float sl = slope;
        if (c > 0.5) { vec3 pc = matC(c, p, dc, sl);
          if (c < 3.5 || c > 12.5) { vec3 tb = mix(textureLod(tNat, guv, 4.0).rgb, textureLod(tUrb, guv, 4.0).rgb, uk); pc = mix(pc, pc * (0.6 + 0.8 * dot(tb, vec3(0.333)) / max(dot(pc, vec3(0.333)), 0.05)), 0.18); }   // tông vùng từ vệ tinh (nhẹ)
          if (sl > 0.45) pc = mix(pc, matC(4.0, p, dc, sl), smoothstep(0.45, 0.62, sl));
          if (uCliff > 0.5) pc = mix(pc, cliffC(vWP, sl), smoothstep(0.16, 0.30, sl) * (1.0 - uk));   // vách rất dốc → đá vôi, không loang
          g = mix(g, pc, nearK); } }
      float det = mix(0.80 + 0.40 * fbmT(vWP.xz * 0.21) , 1.0, max(smoothstep(600.0, 2500.0, dd), nearK));
      g *= mix(1.0, det, uDetail) * (0.94 + 0.12 * fbmT(vWP.xz * 0.012));
      if (vWP.y < -0.5) g = mix(g, vec3(0.30, 0.33, 0.32), 0.8);   // đáy cát dưới nước (đất chưa khai hoang)
      // AO tiếp đất nướng sẵn theo năm (chỉ toà đã mọc gây tối)
      if (uAOon > 0.5) { vec2 auv = vec2((vWP.x - uAOBox.x) / (uAOBox.z - uAOBox.x), (-vWP.z - uAOBox.y) / (uAOBox.w - uAOBox.y));
        if (auv.x > 0.0 && auv.x < 1.0 && auv.y > 0.0 && auv.y < 1.0) { vec3 a = texture(tAO, auv).rgb; float ay = decYear(a.gb);
          g *= 1.0 - 0.5 * a.r * smoothstep(ay - 2.0, ay, uYear); } }
      float L = dot(g, vec3(0.299, 0.587, 0.114)); g = mix(g, vec3(L), 0.55 * uDim) * (1.0 - 0.36 * uDim);
      diffuseColor.rgb = g;`).replace('#include <dithering_fragment>', '#include <dithering_fragment>\n if (uMask > 0.5) gl_FragColor = vec4(0.0, step(0.5, uk), vWP.y < 0.2 ? 0.25 : (1.0 - step(0.5, uk)) * mix(0.9, 0.5, 1.0 - step(0.2, 1.0 - clamp(vWN.y, 0.0, 1.0))), 1.0);   /* V5b-2d: lam 0,9 = đất tự nhiên DỐC (vách/sườn Rock) — trước: đen (lẫn vào nước/trời) */   /* mặt nạ: xanh = nền phố (đô thị theo năm); V5b-2c: lam 0,5 = đất tự nhiên BẰNG (cỏ/cát trống, dốc < ~37°), lam 0,25 = đáy dưới mặt nước (= nước) */');
  };
  // lưới trong 20 m + lưới ngoài 60 m (đỉnh nằm trong vùng trong bị hạ 40 m → không lộ, không z-fight)
  const IN = [-3000, -5500, 2000, 5000];
  const grid = (eA, nA, eB, nB, s, sinkIn) => {
    const nx = Math.round((eB - eA) / s) + 1, nz = Math.round((nB - nA) / s) + 1, P = new Float32Array(nx * nz * 3), I = [];
    for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const e = eA + i * s, n = nB - j * s, k = (j * nx + i) * 3;
      let h = hAt(e, n); if (sinkIn && e > IN[0] + s && e < IN[2] - s && n > IN[1] + s && n < IN[3] - s) h -= 40; P[k] = e; P[k + 1] = h; P[k + 2] = -n; }
    // V5b-2a: lưới ngoài 60 m BỎ các ô nằm trọn trong vùng trong (đã có ô 20/60 m của LOD) — nội suy thô qua vách đứng (mặt bắc Rock cao ≈ 400 m) đâm xuyên lưới mịn dù đã hạ 40 m
    const inIn = (e, n) => sinkIn && e > IN[0] + 2 * s && e < IN[2] - 2 * s && n > IN[1] + 2 * s && n < IN[3] - 2 * s;
    for (let j = 0; j < nz - 1; j++) for (let i = 0; i < nx - 1; i++) { const a = j * nx + i, b = a + 1, c = a + nx, d = c + 1;
      if (inIn(eA + i * s, nB - j * s) && inIn(eA + (i + 1) * s, nB - (j + 1) * s)) continue; I.push(a, c, b, b, c, d); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setIndex(I); g.computeVertexNormals(); return g;
  };
  // LOD địa hình theo ô 1 km (kỹ thuật V5b-1): ô gần 20 m, ô xa 60 m; váy (skirt) 30 m che khe nứt giữa hai mức
  const group = new THREE.Group(), chunks = [], CK = 1000;
  const chunk = (eA, nA, s) => { const g = grid(eA - s, nA - s, eA + CK + s, nA + CK + s, s, false); return g; };
  if (U.terrainLod === false) { const inner = new THREE.Mesh(grid(IN[0], IN[1], IN[2], IN[3], st, false), mat); inner.receiveShadow = inner.castShadow = true; inner.frustumCulled = false; group.add(inner); }
  else for (let eA = IN[0]; eA < IN[2]; eA += CK) for (let nA = IN[1]; nA < IN[3]; nA += CK) {
    const hi = new THREE.Mesh(chunk(eA, nA, st), mat), lo = new THREE.Mesh(chunk(eA, nA, st * 3), mat);
    lo.position.y = -0.6;   // mức thô hơi thấp hơn: chỗ chồng mép luôn thấy mức mịn
    for (const m of [hi, lo]) { m.receiveShadow = m.castShadow = true; m.frustumCulled = true; m.geometry.computeBoundingSphere(); group.add(m); }
    chunks.push({ c: [eA + CK / 2, -(nA + CK / 2)], hi, lo }); }
  const outer = new THREE.Mesh(grid(e0, n0, e1, n1, st * 3, true), mat); outer.receiveShadow = outer.castShadow = true; outer.frustumCulled = false; group.add(outer);
  const terrStat = { hi: 0, lo: 0 };
  function update(cam) { terrStat.hi = terrStat.lo = 0; for (const k of chunks) { const d = Math.hypot(cam.position.x - k.c[0], cam.position.z - k.c[1]) - 0.3 * cam.position.y; const near = d < 2200;
    k.hi.visible = near; k.lo.visible = !near; terrStat[near ? 'hi' : 'lo']++; } }
  // vòng XA 150 m (chân trời): DSM + màu Sentinel-2 đã vá đô thị; phần trùng gói cảnh hạ 60 m (không lộ, không z-fight)
  let farTris = 0;
  if (M.far_box) { const [fe0, fn0, fe1, fn1] = M.far_box, [fr, fc] = M.far_shape, fs = M.far_step, FH = await loadF32(base + 'far.f32'), ftex = await tex(base + 'far.jpg');
    const P = new Float32Array(fr * fc * 3), UV = new Float32Array(fr * fc * 2), I = [];
    for (let j = 0; j < fr; j++) for (let i = 0; i < fc; i++) { const e = fe0 + i * fs, n = fn1 - j * fs, k = j * fc + i; let h = FH[k];
      if (e > e0 + 2 * fs && e < e1 - 2 * fs && n > n0 + 2 * fs && n < n1 - 2 * fs) h -= 60; P.set([e, h, -n], k * 3); UV.set([i / (fc - 1), 1 - j / (fr - 1)], k * 2); }
    // V5b-2a: BỎ ô vòng xa nằm trọn trong gói cảnh (lỗi V5b-1 → V5b-2a: ô 150 m nội suy qua vách bắc Rock đâm xuyên lưới gần → mảng ảnh vệ tinh tối hình tam giác trên vách)
    const inBox = (e, n) => e > e0 + 3 * fs && e < e1 - 3 * fs && n > n0 + 3 * fs && n < n1 - 3 * fs;
    for (let j = 0; j < fr - 1; j++) for (let i = 0; i < fc - 1; i++) { const a = j * fc + i, b = a + 1, c = a + fc, d = c + 1;
      if (inBox(fe0 + i * fs, fn1 - j * fs) && inBox(fe0 + (i + 1) * fs, fn1 - (j + 1) * fs)) continue; I.push(a, c, b, b, c, d); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('uv', new THREE.BufferAttribute(UV, 2)); g.setIndex(I); g.computeVertexNormals();
    const fm = new THREE.MeshStandardMaterial({ map: ftex, roughness: 1 }); fm.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uDim: U.uDim });
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uDim;').replace('#include <map_fragment>', '#include <map_fragment>\n diffuseColor.rgb *= 1.15; { float L = dot(diffuseColor.rgb, vec3(0.299,0.587,0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55*uDim) * (1.0 - 0.36*uDim); }'); };
    const far = new THREE.Mesh(g, fm); far.frustumCulled = false; far.receiveShadow = false; group.add(far); farTris = I.length / 3; }
  return { group, hAt, mat, uni, update, cliffStat, stat: () => terrStat, tris: chunks.reduce((s, k) => s + k.hi.geometry.index.count / 3, 0) + outer.geometry.index.count / 3 + farTris };
}

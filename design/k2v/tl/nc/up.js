// NC-CPU · CÁCH A — LỚP NÂNG CẤP ĐỘ THẬT BỀ MẶT cho cảnh tl (chỉ CPU, llvmpipe). Mã thử mới; không sửa terrain.js/city.js/water.js:
//  vá vật liệu bằng onBeforeCompile NỐI TIẾP (giữ mặt nạ uMask 1/2/3 của page.js), thêm lớp bụi cây instanced, thay shader nước, sương khí quyển.
//  1. NỀN: vân ảnh chụp CC0 (Poly Haven, 18 tấm, RIGHTS: reports/nc-cpu/RIGHTS-NC.md) theo 13 lớp phủ (cls.png), 2 tỉ lệ không thông ước + pháp tuyến;
//     giữ bảng màu thủ tục của k2v (vân ảnh mang CẤU TRÚC + một phần sắc độ), chỉ trong vùng vật liệu gần (≤ 2,6–3,6 km) như terrain.js.
//  2. BỤI CÂY: maquis/garrigue rải theo lớp phủ tự nhiên (cl.r), ẩn ở nền đô thị theo năm (cùng logic terrain.js: tYears + tGhostU), đất chưa nổi, dải trại
//     (bọc ctx.trees.hideWhere: mọi lệnh ẩn cây của t3tl áp cả bụi). Mật độ trước 1900 × 0,45 (đồn trú chặt củi, bản khắc Drinkwater: sườn thưa — bậc 5).
//  3. NƯỚC: sóng 5 hướng + nhiễu, màu sâu bớt bão hoà, dải nông/bọt sát bờ theo khoảng cách bờ của NĂM (đất lấn biển 1941), phản chiếu phẳng của V6 giữ nguyên.
//  4. SƯƠNG KHÍ QUYỂN: thay fog_fragment (toàn cục, chỉ tiến trình dựng này) bằng tắt dần e^(−σd) về màu chân trời sáng, σ theo cảnh.
//  5. NHÀ / CÔNG SỰ: vân vữa (tường), ngói (mái dốc), đá (công sự) nhân vào albedo; AO hẻm phố từ lượt nướng (bake.js) nếu có.
import { THREE, rng } from '../core.js';
import { makeBake } from './bake.js';

export const NC_LOOK = {};
const TEX = '/cache/nc/tex/';
const LAYERS = [   // [tên Poly Haven, độ phân giải tệp, cỡ thật m]
  ['aerial_beach_01', '2k', 30], ['aerial_sand', '2k', 15], ['aerial_grass_rock', '2k', 15], ['dry_ground_rocks', '2k', 4], ['sparse_grass', '2k', 2],
  ['aerial_rocks_02', '2k', 50], ['marble_cliff_02', '1k', 6.8], ['farm_soil', '2k', 2], ['aerial_asphalt_01', '2k', 30], ['stony_dirt_path', '2k', 2.17],
  ['dirt_aerial_02', '2k', 20], ['gravel_concrete', '2k', 2.12], ['dry_ground_01', '2k', 4], ['grass_ground', '2k', 2.51], ['aerial_ground_rock', '2k', 20],
  ['white_plaster_rough_01', '1k', 1.0], ['clay_roof_tiles_02', '1k', 2.5], ['seaworn_sandstone_brick', '1k', 1.69]];
const S = 1024;

async function decode(url, w = S) {   // JPEG → RGBA8 (OffscreenCanvas; ảnh không có alpha nên không mất kênh)
  const b = await (await fetch(url)).blob(), im = await createImageBitmap(b, { colorSpaceConversion: 'none' });
  const cv = new OffscreenCanvas(w, w), g = cv.getContext('2d'); g.drawImage(im, 0, 0, w, w); return g.getImageData(0, 0, w, w).data;
}
async function texArray(kind) {   // kind: diff | nor → DataArrayTexture 1024² × 18 lớp, mipmap; trả {tex, mean[]} (mean tuyến tính của lớp diff)
  const n = LAYERS.length, data = new Uint8Array(S * S * 4 * n), mean = [];
  const px = await Promise.all(LAYERS.map(([id, r]) => decode(`${TEX}${id}_${kind}_${r}.jpg`)));
  px.forEach((p, i) => { data.set(p, i * S * S * 4); if (kind === 'diff') { let a = [0, 0, 0]; for (let k = 0; k < p.length; k += 64) for (let c = 0; c < 3; c++) a[c] += Math.pow(p[k + c] / 255, 2.2); mean.push(a.map((v) => v / (p.length / 64))); } });
  const t = new THREE.DataArrayTexture(data, S, S, n); t.format = THREE.RGBAFormat; t.type = THREE.UnsignedByteType; t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.generateMipmaps = true; t.anisotropy = +(globalThis.NC_ANISO ?? 1);
  t.colorSpace = kind === 'diff' ? THREE.SRGBColorSpace : THREE.NoColorSpace; t.needsUpdate = true; return { tex: t, mean, bytes: data.length };
}
// đọc CHÍNH XÁC byte của một texture đã tải (tYears/tCls có kênh alpha mang dữ liệu → không qua canvas) — cùng cách export6.js
function gpuBytes(R, tex) {
  const img = tex.image, w = img.width, h = img.height, rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.UnsignedByteType, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
  const m = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, uniforms: { t: { value: tex } }, vertexShader: 'in vec3 position; void main(){ gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: 'precision highp float; uniform sampler2D t; out vec4 o; void main(){ o = texelFetch(t, ivec2(gl_FragCoord.xy), 0); }' });
  const sc = new THREE.Scene(); sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m)); R.setRenderTarget(rt); R.render(sc, new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1));
  const px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(rt, 0, 0, w, h, px); R.setRenderTarget(null); rt.dispose(); m.dispose();
  return { px, w, h, flipY: tex.flipY };   // hàng 0 = đáy texture (GL); flipY = true → hàng 0 là hàng CUỐI của ảnh PNG
}
// (E, N) → chỉ số điểm ảnh trong mảng gpuBytes (cùng uv như shader: u = (E − ext.x)/ext.z, v = (N − ext.y)/ext.w)
const pix = (B, ext, e, n) => { const u = (e - ext.x) / ext.z, v = (n - ext.y) / ext.w; if (u < 0 || u >= 1 || v < 0 || v >= 1) return -1;
  const ix = Math.floor(u * B.w), iy0 = Math.floor(v * B.h), iy = B.flipY ? iy0 : B.h - 1 - iy0; return (iy * B.w + ix) * 4; };

// ---------------------------------------------------------------- GLSL chung
const G_DECL = `uniform highp sampler2DArray tNcD, tNcN; uniform vec3 uNcMean[18]; uniform float uNcOn, uNcNK, uNcYear, uNcSkip;
  vec2 ncNP = vec2(0.0); vec2 ncDX = vec2(0.0), ncDY = vec2(0.0); vec3 ncWX = vec3(0.0), ncWY = vec3(0.0);   // đạo hàm toạ độ vân tính ở ĐẦU main (luồng đồng nhất) → textureGrad trong nhánh
  float ncH(vec2 p){ p = fract(p * vec2(233.34, 851.73)); p += dot(p, p + 23.45); return fract(p.x * p.y); }
  float ncVN(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f); return mix(mix(ncH(i), ncH(i + vec2(1, 0)), f.x), mix(ncH(i + vec2(0, 1)), ncH(i + vec2(1, 1)), f.x), f.y); }
  // chống lặp ô (kiểu Quilez "texture repetition" cách 3): 2 mẫu lệch theo chỉ số nhiễu, hoà theo độ chênh màu
  vec3 ncT(int L, vec2 q, vec2 dx, vec2 dy){ float k = ncVN(q * 0.43) * 8.0, ia = floor(k), f = fract(k); vec2 oa = sin(vec2(3.0, 7.0) * ia), ob = sin(vec2(3.0, 7.0) * (ia + 1.0));
    vec3 a = textureGrad(tNcD, vec3(q + oa, float(L)), dx, dy).rgb, b = textureGrad(tNcD, vec3(q + ob, float(L)), dx, dy).rgb;
    return mix(a, b, smoothstep(0.2, 0.8, f - 0.1 * dot(a - b, vec3(1.0)))) / max(uNcMean[L], vec3(0.02)); }
  vec3 ncT1(int L, vec2 q, vec2 dx, vec2 dy){ return textureGrad(tNcD, vec3(q, float(L)), dx, dy).rgb / max(uNcMean[L], vec3(0.02)); }
  vec2 ncN(int L, vec2 q, vec2 dx, vec2 dy){ return textureGrad(tNcN, vec3(q, float(L)), dx, dy).xy * 2.0 - 1.0; }
  const mat2 ncRot = mat2(0.80, -0.60, 0.60, 0.80);`;
const G_GROUND = `
  // lớp phủ c (1–13) → 2 lớp vân [L1 @ s1 m, L2 @ s2 m] + độ nhận sắc kc (0 = chỉ độ sáng/cấu trúc, 1 = màu ảnh)
  vec3 ncG(vec3 pc, float c, vec2 p, float sl, float dd){
    if (uNcOn < 0.5 || mod(uNcSkip, 2.0) > 0.5) return pc;
    int L1 = 2, L2 = 4; float s1 = 15.0, s2 = 2.0, kc = 0.25, kd = 1.0;
    if (c < 1.5) { L1 = 0; s1 = 30.0; L2 = 1; s2 = 15.0; kc = 0.30; }
    else if (c < 2.5) { L1 = 2; s1 = 15.0; L2 = 3; s2 = 4.0; kc = 0.30; }
    else if (c < 3.5) { L1 = 14; s1 = 20.0; L2 = 3; s2 = 4.0; kc = 0.20; }
    else if (c < 4.5) { L1 = 5; s1 = 50.0; L2 = 14; s2 = 20.0; kc = 0.35; }
    else if (c < 5.5) { L1 = 10; s1 = 20.0; L2 = 7; s2 = 2.0; kc = 0.30; }
    else if (c < 6.5 || (c > 8.5 && c < 9.5)) { L1 = 8; s1 = 30.0; L2 = 11; s2 = 2.12; kc = 0.25; }
    else if (c < 7.5) { if (uNcYear < 1900.0) { L1 = 10; s1 = 20.0; L2 = 9; s2 = 2.17; kc = 0.30; } else { L1 = 8; s1 = 30.0; L2 = 11; s2 = 2.12; kc = 0.20; } }
    else if (c < 8.5 || (c > 11.5 && c < 12.5)) { L1 = 13; s1 = 2.51; L2 = 2; s2 = 15.0; kc = 0.15; }
    else if (c < 10.5) { L1 = 11; s1 = 2.12; L2 = 8; s2 = 30.0; kc = 0.20; }
    else if (c < 11.5) { L1 = 10; s1 = 20.0; L2 = 12; s2 = 4.0; kc = 0.30; }
    if (sl > 0.45) { float k = smoothstep(0.45, 0.62, sl); if (k > 0.5) { L1 = 5; s1 = 50.0; L2 = 6; s2 = 6.8; kc = 0.35; } }
    vec2 q1 = p / s1, q2 = ncRot * p / s2 + 0.37; mat2 r2 = ncRot * ncRot;
    vec3 t1 = ncT(L1, q1, ncDX / s1, ncDY / s1), t2 = ncT(L2, q2, ncRot * ncDX / s2, ncRot * ncDY / s2), t3 = ncT1(L1, r2 * p / (s1 * 3.7) + 0.71, r2 * ncDX / (s1 * 3.7), r2 * ncDY / (s1 * 3.7));
    vec3 t = t1 * mix(vec3(1.0), t3, 0.55) * mix(vec3(1.0), t2, 0.55);
    t = clamp(mix(vec3(1.0), t, 0.8), vec3(0.15), vec3(2.6));
    float lt = dot(t, vec3(0.299, 0.587, 0.114));
    ncNP = (ncN(L1, q1, ncDX / s1, ncDY / s1) * 0.8 + ncN(L2, q2, ncRot * ncDX / s2, ncRot * ncDY / s2) * 0.6) * (1.0 - smoothstep(1800.0, 3200.0, dd));
    vec3 outc = pc * mix(vec3(lt), t, kc);
    if (mod(floor(uNcSkip / 8.0), 2.0) > 0.5) { if (any(isnan(ncNP)) || any(isinf(ncNP))) return vec3(0.0, 50.0, 0.0); if (any(isnan(outc)) || any(isinf(outc))) return vec3(50.0, 0.0, 0.0); }
    return outc; }`;
const BAKE_DECL = `uniform sampler2D tNcBake; uniform vec4 uNcBakeBox; uniform float uNcBakeOn, uNcSkyK, uNcBncK, uNcFireK; uniform vec3 uNcSunC, uNcFireC;
  vec4 ncBake(vec2 en){ vec2 b = (en - uNcBakeBox.xy) / (uNcBakeBox.zw - uNcBakeBox.xy); if (uNcBakeOn < 0.5 || b.x < 0.0 || b.y < 0.0 || b.x > 1.0 || b.y > 1.0) return vec4(-1.0); return texture(tNcBake, b); }`;
// ánh sáng nướng: R = bức xạ trời (có che khuất + nảy) / bức xạ trời mặt phẳng trống, G = nảy của nắng (gián tiếp) / nắng thẳng mặt phẳng, B = lửa (gián tiếp + trực tiếp), A = 1
//  → gián tiếp (hemi k2v) × R ; + albedo × màu nắng × G ; + albedo × màu lửa × B × cường độ lửa theo thời gian
const BAKE_APPLY = (wp, nrm, lift) => `{ vec3 ncW = ${wp}; vec3 ncNw = ${nrm}; vec2 ncEN = vec2(ncW.x, -ncW.z) + ncNw.xz * vec2(1.0, -1.0) * ${lift};
    vec4 bk = ncBake(ncEN); if (bk.r >= 0.0) { float up = ${lift === '0.0' ? '0.0' : 'smoothstep(0.0, 14.0, ncW.y - bk.a * 600.0)'};
      float sky = mix(bk.r * uNcSkyK, 1.0, up * 0.7);
      reflectedLight.indirectDiffuse *= sky;
      reflectedLight.indirectDiffuse += diffuseColor.rgb * (uNcSunC * bk.g * uNcBncK * (1.0 - up * 0.5) + uNcFireC * bk.b * uNcFireK); } }`;

// ---------------------------------------------------------------- vá vật liệu (nối tiếp onBeforeCompile; khoá bộ đệm chương trình riêng)
function chain(m, tag, fn) {
  if (m.userData['nc_' + tag]) return; m.userData['nc_' + tag] = true;
  const prev = m.onBeforeCompile, key0 = m.customProgramCacheKey ? m.customProgramCacheKey.bind(m) : null;
  m.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r); if (globalThis.NC_DBG) console.log('nc-chain', tag, m.type, (key0 ? key0() : '').slice(0, 80), sh.fragmentShader.includes('vViewPosition'), (sh.fragmentShader.match(/tNcD, tNcN/g) || []).length); fn(sh); };
  m.customProgramCacheKey = () => (key0 ? key0() : '') + '|nc-' + tag; m.needsUpdate = true;
}

// ---------------------------------------------------------------- bụi cây (maquis / garrigue)
const VHEAD = `#include <common>
      uniform sampler2D tYears, tGhostU; uniform vec4 uExt, uGhostBox; uniform float uGhostOn, uYear; float decY(vec2 hl){ return floor(hl.x * 255.0 + 0.5) * 256.0 + floor(hl.y * 255.0 + 0.5); }`;
const VHIDE = `#include <begin_vertex>
      { vec3 ip = (instanceMatrix * vec4(0.0, 0.0, 0.0, 1.0)).xyz; vec2 en = vec2(ip.x, -ip.z); vec2 guv = (en - uExt.xy) / uExt.zw; vec4 yv = textureLod(tYears, guv, 0.0);
        float uy = decY(yv.rg); float uk = uy > 9000.0 ? 0.0 : step(uy - 0.5, uYear);
        if (uGhostOn > 0.5) { vec2 gq = (en - uGhostBox.xy) / uGhostBox.zw; uk *= (gq.x < 0.0 || gq.x > 1.0 || gq.y < 0.0 || gq.y > 1.0) ? 0.0 : textureLod(tGhostU, gq, 0.0).r; }
        float ly = decY(yv.ba); float land = ly < 1.0 ? 1.0 : (ly > 9000.0 ? 0.0 : step(ly, uYear));
        if (uk > 0.5 || land < 0.5) transformed *= 0.0; }`;
function makeBushes(ctx, U, B, Y, era, P) {
  const { terr } = ctx, ext = terr.uni.uExt.value, R0 = rng(4407);
  const DENS = { 2: 0.011, 3: 0.050, 4: 0.007, 13: 0.0035 };   // bụi / m² theo lớp tự nhiên (cl.r) — 2026; trước 1900 × 0,45
  const k82 = era < 1900 ? 0.45 : 1.0, box = P.bushBox || [-3000, -5500, 2000, 5000], cell = 10, TILE = 400;
  const tiles = new Map(); let n = 0;
  for (let N0 = box[1]; N0 < box[3]; N0 += cell) for (let E0 = box[0]; E0 < box[2]; E0 += cell) {
    const i = pix(B, ext, E0 + 5, N0 + 5); if (i < 0) continue; const c = B.px[i], d = DENS[c]; if (!d) continue;
    const j = pix(Y, ext, E0 + 5, N0 + 5), ly = Y.px[j + 2] * 256 + Y.px[j + 3]; if (ly > 9000) continue;
    let lam = d * cell * cell * k82; while (lam > 0) { if (R0() > Math.min(1, lam)) { lam -= 1; continue; } lam -= 1;
      const e = E0 + R0() * cell, nn = N0 + R0() * cell, h = terr.hAt(e, nn); if (h < 0.8) continue;
      const sl = Math.hypot(terr.hAt(e + 3, nn) - terr.hAt(e - 3, nn), terr.hAt(e, nn + 3) - terr.hAt(e, nn - 3)) / 6; if (sl > 1.1) continue;   // vách > 48°: không bụi
      const big = R0() < (c === 3 ? 0.06 : 0.02), r = big ? 2.8 + 1.6 * R0() : 0.9 + 1.4 * Math.pow(R0(), 1.5), hy = big ? 0.9 + 0.3 * R0() : 0.55 + 0.3 * R0();
      const key = Math.floor(e / TILE) + ',' + Math.floor(nn / TILE); if (!tiles.has(key)) tiles.set(key, []);
      const g = c === 3 ? [0.11 + 0.06 * R0(), 0.17 + 0.07 * R0(), 0.07 + 0.04 * R0()] : [0.20 + 0.08 * R0(), 0.22 + 0.06 * R0(), 0.12 + 0.05 * R0()];   // maquis xanh đậm · garrigue xám ô liu (tuyến tính)
      if (era < 1900) { g[0] *= 1.12; g[1] *= 1.02; }   // thưa, khô hơn
      tiles.get(key).push([e, h - 0.15 * r, nn, r, hy, R0() * 6.283, ...g]); n++; } }
  // hai lưới gốc: gần (khối 20 mặt méo) · xa (8 mặt)
  const mk = (geo, seed) => { const p = geo.attributes.position, R = rng(seed); for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = 0.78 + 0.4 * R(); p.setXYZ(i, x * k, Math.max(y, -0.35) * k, z * k); } geo.computeVertexNormals(); geo.translate(0, 0.35, 0); return geo; };
  const gNear = mk(new THREE.IcosahedronGeometry(1, 0), 11), gFar = mk(new THREE.OctahedronGeometry(1, 0), 12);
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff }); mat.userData.v6n = true;
  const uni = { tYears: terr.uni.tYears, uExt: terr.uni.uExt, tGhostU: terr.uni.tGhostU, uGhostBox: terr.uni.uGhostBox, uGhostOn: terr.uni.uGhostOn, uYear: U.uYear };
  mat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, uni);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', VHEAD).replace('#include <begin_vertex>', VHIDE); };
  mat.customProgramCacheKey = () => 'nc-bush'; ctx.maskify(mat, U, 0);
  const dmat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }); dmat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, uni);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', VHEAD).replace('#include <begin_vertex>', VHIDE); }; dmat.customProgramCacheKey = () => 'nc-bush-d';
  const group = new THREE.Group(), list = [], m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), Yx = new THREE.Vector3(0, 1, 0);
  for (const [key, arr] of tiles) { const mkI = (geo) => { const im = new THREE.InstancedMesh(geo, mat, arr.length); im.customDepthMaterial = dmat; im.castShadow = true; im.receiveShadow = true;
      arr.forEach((b, i) => { m4.compose(new THREE.Vector3(b[0], b[1], -b[2]), q.setFromAxisAngle(Yx, b[5]), new THREE.Vector3(b[3], b[3] * b[4], b[3])); im.setMatrixAt(i, m4); im.setColorAt(i, new THREE.Color(b[6], b[7], b[8])); });
      im.instanceMatrix.needsUpdate = true; im.instanceColor.needsUpdate = true; im.computeBoundingSphere(); return im; };
    const near = mkI(gNear), far = mkI(gFar); group.add(near, far);
    const [te, tn] = key.split(',').map(Number); list.push({ c: [(te + 0.5) * TILE, -((tn + 0.5) * TILE)], near, far, arr }); }
  function update(cam) { let a = 0; for (const t of list) { const d = Math.hypot(cam.position.x - t.c[0], cam.position.z - t.c[1]) - 0.25 * cam.position.y;
      t.near.visible = d < 1500; t.far.visible = d >= 1500 && d < (P.bushFar || 3600); if (t.near.visible || t.far.visible) a += t.arr.length; } return a; }
  function hideWhere(test) { let k = 0; const z = new THREE.Matrix4().makeScale(0, 0, 0);
    for (const t of list) { let ch = false; t.arr.forEach((b, i) => { if (test(b[0], b[2])) { t.near.setMatrixAt(i, z); t.far.setMatrixAt(i, z); k++; ch = true; } });
      if (ch) { t.near.instanceMatrix.needsUpdate = true; t.far.instanceMatrix.needsUpdate = true; } } return k; }
  // xuất sang Blender (design/pt/cpu/nc_export.js): ẩn TRÊN CPU đúng các bụi mà shader ẩn ở năm hiện tại (nền đô thị theo năm, vùng ghost, đất chưa nổi)
  function exportPrep(R) { const yr = U.uYear.value, gOn = terr.uni.uGhostOn.value > 0.5, GB = gOn ? gpuBytes(R, terr.uni.tGhostU.value) : null, gb = terr.uni.uGhostBox.value, z = new THREE.Matrix4().makeScale(0, 0, 0); let k = 0;
    for (const t of list) { t.arr.forEach((b, i) => { const j = pix(Y, ext, b[0], b[2]); if (j < 0) return; const uy = Y.px[j] * 256 + Y.px[j + 1], ly = Y.px[j + 2] * 256 + Y.px[j + 3];
        let uk = uy > 9000 ? 0 : (yr >= uy - 0.5 ? 1 : 0); if (gOn) { const g = pix(GB, gb, b[0], b[2]); uk *= g < 0 ? 0 : (GB.px[g] > 127 ? 1 : 0); }
        const land = ly < 1 ? 1 : (ly > 9000 ? 0 : (ly <= yr ? 1 : 0)); if (uk > 0.5 || !land) { t.near.setMatrixAt(i, z); t.far.setMatrixAt(i, z); k++; } });
      t.near.instanceMatrix.needsUpdate = t.far.instanceMatrix.needsUpdate = true; t.far.visible = false; t.near.visible = true; } return k; }
  group.userData.k6 = 'bui';
  return { group, update, hideWhere, exportPrep, n, tiles: list.length };
}

// ---------------------------------------------------------------- khoảng cách bờ (m) theo năm → texture R8 (0..255 = 0..510 m; đất = 0)
function coastTex(Y, ext, year, hAt = null) {   // ANIMATIC-T3 (LOOK-4): hAt → điểm ảnh 'đất' có cao độ ≤ 0,2 m (đê ngầm, bãi trũng) KHÔNG tính là bờ (hết vệt bọt thẳng giữa nước)
  const w = Y.w, h = Y.h, D = new Float32Array(w * h), INF = 1e9;
  for (let iy = 0; iy < h; iy++) for (let ix = 0; ix < w; ix++) { const q = (iy * w + ix) * 4, ly = Y.px[q + 2] * 256 + Y.px[q + 3]; let land = ly < 1 || (ly < 9000 && ly <= year);
    if (land && hAt && hAt(ext.x + (ix + 0.5) / w * ext.z, ext.y + (iy + 0.5) / h * ext.w) <= 0.2) land = false; D[iy * w + ix] = land ? 0 : INF; }
  const a = 10, b = 14.1; for (let it = 0; it < 2; it++) {
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = y * w + x; let v = D[i]; if (!v) continue; if (x > 0) v = Math.min(v, D[i - 1] + a); if (y > 0) { v = Math.min(v, D[i - w] + a); if (x > 0) v = Math.min(v, D[i - w - 1] + b); if (x < w - 1) v = Math.min(v, D[i - w + 1] + b); } D[i] = v; }
    for (let y = h - 1; y >= 0; y--) for (let x = w - 1; x >= 0; x--) { const i = y * w + x; let v = D[i]; if (!v) continue; if (x < w - 1) v = Math.min(v, D[i + 1] + a); if (y < h - 1) { v = Math.min(v, D[i + w] + a); if (x < w - 1) v = Math.min(v, D[i + w + 1] + b); if (x > 0) v = Math.min(v, D[i + w - 1] + b); } D[i] = v; } }
  const d8 = new Uint8Array(w * h); for (let i = 0; i < w * h; i++) d8[i] = Math.min(255, Math.round(D[i] / 2));
  const t = new THREE.DataTexture(d8, w, h, THREE.RedFormat); t.flipY = false; t.magFilter = t.minFilter = THREE.LinearFilter; t.needsUpdate = true;
  return { t, flip: Y.flipY };   // hàng 0 của mảng = hàng 0 GPU (đáy) → uv như tYears
}

const WATER_FS = (GLSL_NOISE, SKY, GLSL_LAND = null) => `uniform float uT, uFogD, uDim, uBaked, uRefl, uWave, uNcCoastOn, uNcCoastFlip; uniform sampler2D tNoise, tRefl, tCoast; uniform mat4 uReflVP; uniform vec3 uFogC; uniform vec4 uExt; varying vec3 vWP; ${GLSL_NOISE} ${SKY}
  ${GLSL_LAND ? 'uniform sampler2D tYears; uniform float uYear; ' + GLSL_LAND + '\n#define NC_LANDNOW 1' : ''}
  // NC-CPU: sóng tổng 5 hướng (bước sóng 9–70 m, dịch theo thời gian) + nhiễu kết cấu; mờ theo cỡ điểm ảnh (fwidth) để không răng cưa ở xa
  vec2 wv(vec2 p, float t){ vec2 g = vec2(0.0); const int NW = 5;
    vec3 W[NW]; W[0] = vec3(0.95, 0.31, 70.0); W[1] = vec3(0.70, -0.71, 37.0); W[2] = vec3(0.26, 0.97, 23.0); W[3] = vec3(-0.50, 0.87, 14.0); W[4] = vec3(0.98, -0.17, 9.0);
    for (int i = 0; i < NW; i++) { float k = 6.2832 / W[i].z, sp = sqrt(9.81 / k), ph = dot(p, W[i].xy) * k - t * sp * k; float a = 0.035 * W[i].z / 70.0 + 0.012;
      float fade = 1.0 - clamp(length(fwidth(p)) * k * 0.9, 0.0, 1.0); g += W[i].xy * cos(ph) * a * k * 6.0 * fade; } return g; }
  void main(){ vec3 V = normalize(cameraPosition - vWP); float dist = length(cameraPosition - vWP); vec2 p = vWP.xz;
    vec2 en = vec2(vWP.x, -vWP.z), cuv = (en - uExt.xy) / uExt.zw; float dc = (cuv.x > 0.0 && cuv.x < 1.0 && cuv.y > 0.0 && cuv.y < 1.0 && uNcCoastOn > 0.5) ? texture(tCoast, vec2(cuv.x, uNcCoastFlip > 0.5 ? 1.0 - cuv.y : cuv.y)).r * 510.0 : 999.0;
    #ifdef NC_LANDNOW
    /* ANIM-V2 (AT-D1): ô đất lấn CHƯA nổi ở năm của khung (đường băng 1941 đang mọc theo uRecl, đất 1987/2026 trước năm nổi) là NƯỚC — không để bờ tĩnh của mốc tính nó là đất (bọt + màu nông = mảng xanh nhạt phẳng) */
    if (cuv.x > 0.0 && cuv.x < 1.0 && cuv.y > 0.0 && cuv.y < 1.0) { float lyW = decYear(texture(tYears, cuv).ba); if (lyW > 1.0 && lyW < 9000.0 && landKx(lyW, uYear, vWP.x) < 0.5) dc = max(dc, 30.0); }
    #endif
    vec2 g = wv(p, uT) * uWave * 0.55;
    float fn = 1.0 - clamp(length(fwidth(p)) * 0.08, 0.0, 1.0);
    vec2 nz = vec2(texture(tNoise, p * 0.011 + vec2(uT * 0.004, 0.0)).g - texture(tNoise, p * 0.011 + vec2(0.37, uT * 0.003)).a, texture(tNoise, p * 0.031 - uT * 0.006).b - texture(tNoise, p * 0.031 + 3.1).r) * 1.6 * fn;
    float calm = 0.78 + 0.22 * smoothstep(0.35, 0.65, texture(tNoise, p * 0.0009 + 0.2).r);   // vệt gió (mặt lặng / gợn) quy mô 1 km
    vec3 N = normalize(vec3((g.x + nz.x * 0.35) * calm, 1.0, (g.y + nz.y * 0.35) * calm));
    vec3 R = reflect(-V, N); R.y = abs(R.y);
    float F = 0.02 + 0.98 * pow(1.0 - max(dot(N, V), 0.0), 5.0);
    vec3 env = skyCol(R);
    if (uRefl > 0.5) { vec4 cp = uReflVP * vec4(vWP + vec3(N.x, 0.0, N.z) * 10.0 * uWave * min(dist / 120.0, 6.0), 1.0); vec2 ruv = cp.xy / cp.w * 0.5 + 0.5;
      if (ruv.x > 0.0 && ruv.x < 1.0 && ruv.y > 0.0 && ruv.y < 1.0) { vec4 rc = texture2D(tRefl, ruv); env = mix(env, rc.rgb, clamp(rc.a, 0.0, 1.0) * 0.85); } }
    vec3 deep = vec3(0.014, 0.062, 0.098), shal = vec3(0.024, 0.100, 0.112);   // sâu: lam đậm bớt bão hoà · nông: ngả lục (chỉ sát bờ ≤ 60 m)
    vec3 body = mix(shal, deep, smoothstep(2.0, 18.0, dc)) * (1.0 - 0.88 * uNight);
    vec3 c = mix(body, env, F);
    float foam = (1.0 - smoothstep(1.5, 9.0, dc + 4.0 * texture(tNoise, p * 0.05 + uT * 0.01).r)) * (0.55 + 0.45 * sin(dc * 0.9 - uT * 1.3)) * fn;
    c = mix(c, vec3(0.80, 0.82, 0.80) * (1.0 - 0.9 * uNight), clamp(foam, 0.0, 1.0) * 0.5);   // ANIMATIC-T3 (LOOK-4): bọt 0,75 → 0,5, dải nông 38 → 18 m (viền xanh nhạt quanh bờ)
    vec3 S3 = uSun; c += vec3(1.0, 0.92, 0.75) * pow(max(dot(R, S3), 0.0), 900.0) * 4.0 * (1.0 - uNight) * calm;
    float L = dot(c, vec3(0.299, 0.587, 0.114)); c = mix(c, vec3(L), 0.5 * uDim) * (1.0 - 0.34 * uDim);
    float f = 1.0 - exp(-uFogD * dist); gl_FragColor = vec4(mix(c, uFogC, f), 1.0); }`;

// ---------------------------------------------------------------- trước khi cảnh dựng
export async function preBuild(ctx, P) {
  const t0 = performance.now(), { THREE: T, terr, U } = ctx, R = ctx.R;
  const B = gpuBytes(R, terr.uni.tCls.value), Y = gpuBytes(R, terr.uni.tYears.value);
  const o = ctx.opt || {}, yr = (() => { const tk = o.time || []; const ys = tk.map((k) => (Array.isArray(k) ? k[1] : k.y)).filter((x) => typeof x === 'number'); return ys.length ? ys.reduce((a, b) => a + b) / ys.length : 2026; })();
  const era = P.era || yr;
  let BU = null;
  if (P.bushes !== false) { BU = makeBushes(ctx, U, B, Y, era, P); ctx.scene.add(BU.group);
    if (ctx.trees && ctx.trees.hideWhere) { const hw = ctx.trees.hideWhere.bind(ctx.trees); ctx.trees.hideWhere = (fn) => { BU.hideWhere(fn); return hw(fn); }; } }
  return { B, Y, BU, era, pre_s: (performance.now() - t0) / 1000 };
}

// ---------------------------------------------------------------- sau khi cảnh dựng
export async function postBuild(ctx, SC, P, pre) { globalThis.NC_DBG = !!P.dbg;
  const t0 = performance.now(), { terr, U, scene } = ctx, meta = { era: pre.era, bushes: pre.BU ? pre.BU.n : 0 };
  const [D, N] = await Promise.all([texArray('diff'), texArray('nor')]); meta.tex_mb = +((D.bytes + N.bytes) * 1.33 / 1e6).toFixed(1);
  const NU = { tNcD: { value: D.tex }, tNcN: { value: N.tex }, uNcMean: { value: D.mean.map((m) => new THREE.Vector3(...m)) }, uNcOn: { value: P.tex === false ? 0 : 1 }, uNcNK: { value: P.nk ?? 0.55 }, uNcYear: U.uYear, uNcSkip: { value: P.skip || 0 } };
  const BK = await makeBake(ctx, P); meta.bake = BK.meta;
  const BU_ = Object.assign({}, NU, BK.uni);
  // 1. nền
  chain(terr.mat, 'ground', (sh) => { Object.assign(sh.uniforms, BU_);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\n${G_DECL}\n${BAKE_DECL}\n${G_GROUND}`)
      .replace('void main() {', 'void main() { ncDX = dFdx(vec2(vWP.x, -vWP.z)); ncDY = dFdy(vec2(vWP.x, -vWP.z));')
      .replace('g = mix(g, pc, nearK); } }', 'pc = ncG(pc, c, p, sl, dd); g = mix(g, pc, nearK); } }')
      .replace('#include <normal_fragment_maps>', '#include <normal_fragment_maps>\n normal = normalize(normal + (viewMatrix * vec4(ncNP.x, 0.0, -ncNP.y, 0.0)).xyz * uNcNK);')
      .replace('#include <aomap_fragment>', '#include <aomap_fragment>\n' + BAKE_APPLY('vWP', 'vec3(0.0, 1.0, 0.0)', '0.0')); });
  // 2. nhà (city.js của gói + các lớp footprint t3tl) · công sự / tường (fort.js) · vật Lambert/Standard khác có pháp tuyến (bóng hẻm phố từ bake)
  let nCity = 0, nGen = 0;
  scene.traverse((o) => { if (!o.isMesh || o.isInstancedMesh && o.geometry === undefined) return; for (const m of [].concat(o.material || [])) { if (!m || m.isShaderMaterial || m.isRawShaderMaterial || m.isMeshDepthMaterial) continue;
    const key = m.customProgramCacheKey ? m.customProgramCacheKey() : '';
    if (/tl-city-0|tl-city-1/.test(key) && !/-d/.test(key.split('|')[0])) { nCity++; chain(m, 'city', (sh) => { Object.assign(sh.uniforms, BU_);
        sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\n${G_DECL}\n${BAKE_DECL}`)
          .replace('void main() {', 'void main() { ncDX = dFdx(vec2(vU, vLY)); ncDY = dFdy(vec2(vU, vLY)); ncWX = dFdx(vWPc); ncWY = dFdy(vWPc);')
          .replace('diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55 * uDim) * (1.0 - 0.36 * uDim);', `
          if (uNcOn > 0.5 && mod(floor(uNcSkip / 2.0), 2.0) < 0.5) { float ncF = 1.0 - smoothstep(900.0, 2600.0, length(vViewPosition));
            if (vU >= 0.0) { vec3 t = ncT(15, vec2(vU, vLY) / 1.6, ncDX / 1.6, ncDY / 1.6); float lt = dot(t, vec3(0.299, 0.587, 0.114)); diffuseColor.rgb *= mix(1.0, clamp(mix(lt, 1.0, 0.35), 0.6, 1.4), ncF);
              float st = textureGrad(tNcD, vec3(vec2(vU * 0.21, 0.0), 10.0), ncDX * 0.21, ncDY * 0.21).g / uNcMean[10].g; diffuseColor.rgb *= 1.0 - 0.10 * smoothstep(0.9, 1.3, st) * (1.0 - smoothstep(0.0, 9.0, vLY)) ; }   // vệt bẩn mưa chân tường
            else if (vObjN.y > 0.25 && abs(vObjN.y) < 0.98) { vec3 t = ncT(16, vec2(vWPc.x, vWPc.z) / 2.5, ncWX.xz / 2.5, ncWY.xz / 2.5); diffuseColor.rgb *= mix(vec3(1.0), clamp(t, vec3(0.5), vec3(1.6)), 0.55 * ncF); } }
          diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55 * uDim) * (1.0 - 0.36 * uDim);`)
          .replace('#include <aomap_fragment>', '#include <aomap_fragment>\n' + BAKE_APPLY('vWPc', '((vec4(normal, 0.0) * viewMatrix).xyz / max(length(normal), 1e-4))', '3.0')); }); continue; }
    if (!(m.isMeshLambertMaterial || m.isMeshStandardMaterial || m.isMeshPhongMaterial) || m === terr.mat || Object.keys(m.userData).some((k) => k.startsWith('nc_'))) continue; if (m.userData.nc_bush || /nc-bush/.test(key)) continue;
    const fort = /tl-fort/.test(key);
    nGen++; chain(m, fort ? 'fort' : 'gen', (sh) => { Object.assign(sh.uniforms, BU_);
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\n${G_DECL}\n${BAKE_DECL}\n \n#define ncWP() ((inverse(viewMatrix) * vec4(-vViewPosition, 1.0)).xyz)`)
        .replace('void main() {', 'void main() { { vec3 w0 = ncWP(); ncWX = dFdx(w0); ncWY = dFdy(w0); }')
        .replace('#include <normal_fragment_maps>', '#include <normal_fragment_maps>\n' + (fort ? `{ vec3 w = ncWP(); vec3 an = abs((vec4(normal, 0.0) * viewMatrix).xyz); an /= max(an.x + an.y + an.z, 1e-4); float ncF = 1.0 - smoothstep(700.0, 2200.0, length(vViewPosition));
            vec3 t = an.x > an.z ? ncT(17, vec2(w.z, w.y) / 1.69, ncWX.zy / 1.69, ncWY.zy / 1.69) : ncT(17, vec2(w.x, w.y) / 1.69, ncWX.xy / 1.69, ncWY.xy / 1.69); if (an.y > 0.55) t = ncT(9, vec2(w.x, w.z) / 2.17, ncWX.xz / 2.17, ncWY.xz / 2.17);
            float lt = dot(t, vec3(0.299, 0.587, 0.114)); if (uNcOn > 0.5 && mod(floor(uNcSkip / 4.0), 2.0) < 0.5) diffuseColor.rgb *= mix(1.0, clamp(mix(lt, 1.0, 0.25), 0.55, 1.45), ncF); }\n` : ''))
        .replace('#include <aomap_fragment>', '#include <aomap_fragment>\n' + BAKE_APPLY('ncWP()', '((vec4(normal, 0.0) * viewMatrix).xyz / max(length(normal), 1e-4))', '2.0')); }); } });
  meta.patched = { city: nCity, other: nGen };
  // 3. nước
  let water = null; scene.traverse((o) => { if (o.isMesh && o.material && o.material.isShaderMaterial && o.material.uniforms && o.material.uniforms.uReflVP && o.renderOrder === 5) water = o; });
  let CT = null, CT2 = null, CT0 = null, CT41 = null, CT87 = null;   // ANIMATIC-T3 (LOOK-4): CT0 = bờ thời 1790 cho năm < 1900 (bờ 1940 có đê/đất lấn chưa tồn tại → vệt bọt thẳng ngoài khơi + mảng nông xanh nhạt)
  if (water && P.water !== false) { const wm = water.material, mod = await import('../water.js'), core = await import('../core.js');
    const hA = (e, n) => terr.hAt(e, n); CT = coastTex(pre.Y, terr.uni.uExt.value, 1940, hA); CT2 = coastTex(pre.Y, terr.uni.uExt.value, 2026, hA); CT0 = coastTex(pre.Y, terr.uni.uExt.value, 1790, hA); CT41 = coastTex(pre.Y, terr.uni.uExt.value, 1941, hA); CT87 = coastTex(pre.Y, terr.uni.uExt.value, 1987, hA);   /* ANIM-V2 (AT-D1): bờ theo đúng các mốc đất lấn có trong years.png (0 · 1941 · 1987 · 2026) */
    Object.assign(wm.uniforms, { tCoast: { value: CT.t }, uExt: terr.uni.uExt, uNcCoastOn: { value: 1 }, uNcCoastFlip: { value: P.cflip ? 1 : 0 }, tYears: terr.uni.tYears, uYear: U.uYear, uRecl: U.uRecl || { value: 0 } });
    wm.fragmentShader = WATER_FS(core.GLSL_NOISE, mod.SKY, (await import('../terrain.js')).GLSL_LAND); wm.needsUpdate = true; meta.water = 'nc'; }
  // 4. sương khí quyển: tắt dần e^(−σ d) — σ mặc định 1/16 km; màu: chân trời sáng ngả xám-lam
  const haze = P.haze === false ? null : Object.assign({ s: 1 / 16000, c: [0.66, 0.74, 0.84] }, typeof P.haze === 'object' ? P.haze : {});
  if (haze) { scene.fog.density = haze.s; scene.fog.color.setRGB(...haze.c); if (water) water.material.uniforms.uFogD.value = haze.s; meta.haze = haze; }
  meta.post_s = +((performance.now() - t0) / 1000).toFixed(2); meta.pre_s = +pre.pre_s.toFixed(2);
  return { meta, exportPrep: () => (pre.BU ? pre.BU.exportPrep(ctx.R) : 0), update(st, t) { if (pre.BU) meta.bush_vis = pre.BU.update(ctx.cam); if (CT && water) water.material.uniforms.tCoast.value = st.year >= 2024.5 ? CT2.t : st.year >= 1987 ? CT87.t : st.year >= 1941.9 ? CT41.t : st.year >= 1900 ? CT.t : CT0.t; /* ANIM-V2 (AT-D1): trước đây ≥ 1942,5 dùng bờ 2026 → đất 1987/2026 chưa nổi bị tính là bờ */ BK.update(st, t); } };
}

// sương: fog_fragment toàn cục (chỉ tiến trình dựng này nạp up.js) — FogExp2 density = σ (1/m), tắt dần tuyến tính theo quang trình
THREE.ShaderChunk.fog_fragment = `#ifdef USE_FOG
  #ifdef FOG_EXP2
    float fogFactor = 1.0 - exp( - fogDensity * vFogDepth );
  #else
    float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
  #endif
  gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`;

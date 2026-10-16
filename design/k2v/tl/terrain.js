// K2V tl · NỀN SỐNG (lớp 3 chuẩn hình): địa hình DTM 20 m (trong) + 60 m (ngoài), phủ mặt đất Sentinel-2 theo NĂM
// (nền tự nhiên ↔ nền đô thị theo năm đô thị hoá), đá vôi trên vách dốc, chi tiết gần, AO tiếp đất nướng sẵn theo năm,
// đất khai hoang chỉ nổi lên từ năm có bằng chứng (years.png kênh B/A). Mặt nước: water.js. Chữ/thẻ: text.js.
import { THREE, GLSL_YEAR, GLSL_NOISE, loadF32, tex, noiseTex } from './core.js';

export const GLSL_LAND = `${GLSL_YEAR}
// năm có đất: 0 = luôn; 1941 = khai hoang đường băng (đủ 1943, HMGoG 199/2018); mốc khác: nổi trong 1,5 năm trước mốc; 9999 = biển
float landK(float ly, float y){ if (ly < 1.0) return 1.0; if (ly > 9000.0) return 0.0;
  if (abs(ly - 1941.0) < 0.5) return clamp((y - 1941.0) / 2.0, 0.0, 1.0); return clamp((y - (ly - 1.5)) / 1.5, 0.0, 1.0); }`;

export async function makeTerrain(base, M, U) {
  const [e0, n0, e1, n1] = M.ext, [R, Cn] = M.terrain_shape, st = M.step_terrain;
  const Hh = await loadF32(base + 'terrain.f32');
  const hAt = (e, n) => { const fc = Math.max(0, Math.min(Cn - 1.001, (e - e0) / st)), fr = Math.max(0, Math.min(R - 1.001, (n1 - n) / st));
    const c = Math.floor(fc), r = Math.floor(fr), a = fc - c, b = fr - r, g = (rr, cc) => Hh[rr * Cn + cc];
    return (g(r, c) * (1 - a) + g(r, c + 1) * a) * (1 - b) + (g(r + 1, c) * (1 - a) + g(r + 1, c + 1) * a) * b; };
  const [tNat, tUrb, tYears, tAO] = await Promise.all([tex(base + 'ground_nat.jpg'), tex(base + 'ground_urb.jpg'),
    tex(base + 'years.png', { srgb: false, nearest: true }), tex(base + 'ao.png', { srgb: false })]);
  const [Gh, Gw] = M.ground_shape;
  const uni = { uYear: U.uYear, uDim: U.uDim, tNat: { value: tNat }, tUrb: { value: tUrb }, tYears: { value: tYears }, tAO: { value: tAO },
    uExt: { value: new THREE.Vector4(e0 - 5, n0 - 5, Gw * 10, Gh * 10) }, tNoise: { value: noiseTex() }, uBaked: U.uBaked, uAOBox: { value: new THREE.Vector4(...M.ao_box) }, uAOon: U.uAOon, uDetail: { value: 1 } };
  const mat = U.lambert ? new THREE.MeshLambertMaterial({ color: 0xffffff }) : new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.96, metalness: 0 });
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, uni);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', `#include <common>
      uniform sampler2D tYears; uniform vec4 uExt; uniform float uYear; varying vec3 vWP; varying vec3 vWN; ${GLSL_LAND}`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>
      { vec2 uv = vec2((position.x - uExt.x) / uExt.z, (-position.z - uExt.y) / uExt.w); vec4 yv = textureLod(tYears, uv, 0.0);
        float k = landK(decYear(yv.ba), uYear); transformed.y = mix(min(transformed.y, -10.0), transformed.y, k); }
      vWP = (modelMatrix * vec4(transformed, 1.0)).xyz; vWN = normalize(mat3(modelMatrix) * objectNormal);`);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
      uniform sampler2D tNat, tUrb, tYears, tAO, tNoise; uniform vec4 uExt, uAOBox; uniform float uYear, uDim, uAOon, uDetail, uBaked; varying vec3 vWP; varying vec3 vWN;
      ${GLSL_YEAR} ${GLSL_NOISE}
      float fbmT(vec2 p){ if (uBaked < 0.5) return fbm(p); vec2 q = mat2(0.80, -0.60, 0.60, 0.80) * p * 0.173 + 0.37; return 0.6 * texture(tNoise, p * 0.25).r + 0.4 * texture(tNoise, q).b; }   // nhiễu nướng sẵn chống lặp ô: 2 mẫu, tỉ lệ không thông ước + xoay miền`)
      .replace('#include <map_fragment>', `
      vec2 guv = vec2((vWP.x - uExt.x) / uExt.z, (-vWP.z - uExt.y) / uExt.w);
      vec4 yv = texture(tYears, guv); float uy = decYear(yv.rg);
      vec3 cN = texture(tNat, guv).rgb, cU = texture(tUrb, guv).rgb;
      float uk = uy > 9000.0 ? 0.0 : smoothstep(uy - 1.0, uy, uYear);   // nền đô thị không hiện trước năm bằng chứng
      // nền tự nhiên (vùng đã vá): thêm biến thiên tầm trung (cát/cỏ khô/bụi) để không phẳng loang
      float nv = fbmT(vWP.xz * 0.006), nv2 = fbmT(vWP.xz * 0.035 + 7.0);
      float flat_ = (1.0 - smoothstep(0.08, 0.2, 1.0 - vWN.y)) * (1.0 - smoothstep(15.0, 40.0, vWP.y));   // chỉ bãi bằng thấp (eo đất), không loang lên sườn Rock
      vec3 cNd = cN * (0.82 + 0.36 * nv * flat_ + 0.18 * (1.0 - flat_)); cNd = mix(cNd, vec3(0.50, 0.50, 0.34), 0.35 * smoothstep(0.45, 0.75, nv2) * flat_); cNd = mix(cNd, vec3(0.80, 0.74, 0.60), 0.25 * smoothstep(0.55, 0.85, 1.0 - nv2) * flat_);
      vec3 g = mix(pow(cNd, vec3(0.9)) * 1.12, cU * 1.08, uk);
      // đá vôi trên vách dốc (Rock): sọc tầng đá + loang; chi tiết gần (≤ 1,5 km) cho đất/cỏ
      float slope = 1.0 - clamp(vWN.y, 0.0, 1.0);
      float strata = 0.82 + 0.22 * fbmT(vec2(vWP.x * 0.015 + vWP.z * 0.011, vWP.y * 0.35)) ;
      vec3 rock = vec3(0.70, 0.67, 0.60) * strata;
      g = mix(g, rock, smoothstep(0.30, 0.55, slope) * (1.0 - uk));
      float dd = length(vWP - cameraPosition);
      float det = mix(0.80 + 0.40 * fbmT(vWP.xz * 0.21) , 1.0, smoothstep(600.0, 2500.0, dd));
      g *= mix(1.0, det, uDetail) * (0.94 + 0.12 * fbmT(vWP.xz * 0.012));
      if (vWP.y < -0.5) g = mix(g, vec3(0.30, 0.33, 0.32), 0.8);   // đáy cát dưới nước (đất chưa khai hoang)
      // AO tiếp đất nướng sẵn theo năm (chỉ toà đã mọc gây tối)
      if (uAOon > 0.5) { vec2 auv = vec2((vWP.x - uAOBox.x) / (uAOBox.z - uAOBox.x), (-vWP.z - uAOBox.y) / (uAOBox.w - uAOBox.y));
        if (auv.x > 0.0 && auv.x < 1.0 && auv.y > 0.0 && auv.y < 1.0) { vec3 a = texture(tAO, auv).rgb; float ay = decYear(a.gb);
          g *= 1.0 - 0.5 * a.r * smoothstep(ay - 2.0, ay, uYear); } }
      float L = dot(g, vec3(0.299, 0.587, 0.114)); g = mix(g, vec3(L), 0.55 * uDim) * (1.0 - 0.36 * uDim);
      diffuseColor.rgb = g;`);
  };
  // lưới trong 20 m + lưới ngoài 60 m (đỉnh nằm trong vùng trong bị hạ 40 m → không lộ, không z-fight)
  const IN = [-3000, -5500, 2000, 5000];
  const grid = (eA, nA, eB, nB, s, sinkIn) => {
    const nx = Math.round((eB - eA) / s) + 1, nz = Math.round((nB - nA) / s) + 1, P = new Float32Array(nx * nz * 3), I = [];
    for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const e = eA + i * s, n = nB - j * s, k = (j * nx + i) * 3;
      let h = hAt(e, n); if (sinkIn && e > IN[0] + s && e < IN[2] - s && n > IN[1] + s && n < IN[3] - s) h -= 40; P[k] = e; P[k + 1] = h; P[k + 2] = -n; }
    for (let j = 0; j < nz - 1; j++) for (let i = 0; i < nx - 1; i++) { const a = j * nx + i, b = a + 1, c = a + nx, d = c + 1; I.push(a, c, b, b, c, d); }
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
    for (let j = 0; j < fr - 1; j++) for (let i = 0; i < fc - 1; i++) { const a = j * fc + i, b = a + 1, c = a + fc, d = c + 1; I.push(a, c, b, b, c, d); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('uv', new THREE.BufferAttribute(UV, 2)); g.setIndex(I); g.computeVertexNormals();
    const fm = new THREE.MeshStandardMaterial({ map: ftex, roughness: 1 }); fm.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uDim: U.uDim });
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uDim;').replace('#include <map_fragment>', '#include <map_fragment>\n diffuseColor.rgb *= 1.15; { float L = dot(diffuseColor.rgb, vec3(0.299,0.587,0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55*uDim) * (1.0 - 0.36*uDim); }'); };
    const far = new THREE.Mesh(g, fm); far.frustumCulled = false; far.receiveShadow = false; group.add(far); farTris = I.length / 3; }
  return { group, hAt, mat, uni, update, stat: () => terrStat, tris: chunks.reduce((s, k) => s + k.hi.geometry.index.count / 3, 0) + outer.geometry.index.count / 3 + farTris };
}

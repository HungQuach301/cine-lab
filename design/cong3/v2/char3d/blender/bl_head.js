// Cine Lab · Cửa mặt Ida lượt 2 (W4) — đầu Ida 'bl': lưới dựng trong Blender (MPFB2 CC0 + tóc/mày/mắt/búi của W4), render bằng three.js.
// Dùng: await preloadIdaBL()  (một lần, TRƯỚC buildCharacter — GLTFLoader bất đồng bộ, buildCharacter đồng bộ)
//       buildCharacter(sheet, { idaStyle: 'bl', … })  → cast3d gọi buildIdaBL(…) thay cho đầu/tóc/tai/cổ.
// GLTFLoader của three (examples/jsm) import 'three' dạng tên trần; trang của dự án không có import map → nạp mã loader qua Blob,
// thay 'three' bằng URL tuyệt đối của three.module.js (cùng URL với cả dự án → cùng một thực thể module).
// Rig: shape key của glb (TÊN = 16 kênh facerig.js + vis_*) tính trên CPU như facerig.js (mọi pass, kể cả G-buffer lớp vẽ, thấy đúng hình);
// morph GPU bị gỡ. Pháp tuyến: N0 (glb) + (N(lưới biến dạng) − N(lưới gốc)) → không lộ đường nối UV.
import * as THREE from '../../../shared/node_modules/three/build/three.module.js';

export const BL_URL = new URL('./ida_bl_v151.glb', import.meta.url).href;   // Cổng 6 (W4): v1.5.1 đề xuất (mắt, mũ); ida_bl.glb v1.5 khoá SHA giữ nguyên
export const CAS_BL_URL = new URL('./cas_bl.glb', import.meta.url).href;   // Cổng 6 (W4): đầu Cas MPFB
const CACHES = {};

async function loadGLTFLoader() {
  const base = new URL('../../../shared/node_modules/three/', import.meta.url).href, threeURL = base + 'build/three.module.js';
  const fix = (src) => src.replace(/from\s*'three'/g, `from '${threeURL}'`);
  const blobURL = (src) => URL.createObjectURL(new Blob([src], { type: 'text/javascript' }));
  const bgu = blobURL(fix(await (await fetch(base + 'examples/jsm/utils/BufferGeometryUtils.js')).text()));
  const gl = fix(await (await fetch(base + 'examples/jsm/loaders/GLTFLoader.js')).text()).replace("'../utils/BufferGeometryUtils.js'", `'${bgu}'`);
  return (await import(blobURL(gl))).GLTFLoader;
}

async function preloadBL(kind, url) {
  if (CACHES[kind] && CACHES[kind].url === url) return CACHES[kind];
  const GLTFLoader = await loadGLTFLoader();
  const [gltf, meta] = await Promise.all([new GLTFLoader().loadAsync(url), fetch(url.replace(/\.glb$/, '.json')).then((r) => r.json())]);
  CACHES[kind] = { url, gltf, meta };
  return CACHES[kind];
}
export const preloadIdaBL = (url = BL_URL) => preloadBL('ida', url);
export const preloadCasBL = (url = CAS_BL_URL) => preloadBL('cas', url);
export const idaBLReady = () => !!CACHES.ida;
export const casBLReady = () => !!CACHES.cas;

// Da: PBR mờ (nhám 0,66, bóng gương 0,3) + khuếch tán "bọc" lệch đỏ (tán xạ dưới da giả lập) + giữ sắc ấm khi ánh lạnh + kéo 35 % ánh hổ phách về trung tính.
export function skinMaterial(opts) {
  const bump = (() => { const N = 512, cv = document.createElement('canvas'); cv.width = cv.height = N; const g = cv.getContext('2d'), im = g.createImageData(N, N);   // lượt 3: vân da nhỏ (lỗ chân lông + nếp mịn), thủ tục
    let sd = 7654321; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647); const b = new Float32Array(N * N).map(rnd);
    const blur = (a, r) => { const o = new Float32Array(N * N), o2 = new Float32Array(N * N); for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { let t = 0; for (let k = -r; k <= r; k++) t += a[y * N + ((x + k + N) % N)]; o[y * N + x] = t / (2 * r + 1); }
      for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { let t = 0; for (let k = -r; k <= r; k++) t += o[((y + k + N) % N) * N + x]; o2[y * N + x] = t / (2 * r + 1); } return o2; };
    const b1 = blur(b, 1), b4 = blur(b, 4);
    for (let i = 0; i < N * N; i++) { const v = 128 + 170 * (b1[i] - 0.5) + 300 * (b4[i] - 0.5); im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = Math.max(0, Math.min(255, v)); im.data[i * 4 + 3] = 255; }
    g.putImageData(im, 0, 0); const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(6, 4); return t; })();
  const mat = new THREE.MeshStandardMaterial({ color: 0xffffff, vertexColors: true, roughness: 1, metalness: 0, envMapIntensity: 0, bumpMap: bump, bumpScale: opts.skinBump ?? 1.4 });
  const warm = opts.skinWarm ?? 0.7, spec = opts.skinSpec ?? 0.3, neu = opts.skinNeutral ?? 0.35;
  const phys = THREE.ShaderChunk.lights_physical_pars_fragment
    .replace('reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );',
      `{ float nlW = dot( geometryNormal, directLight.direction ); vec3 wr = vec3( 0.30, 0.14, 0.10 );
        reflectedLight.directDiffuse += clamp( ( vec3( nlW ) + wr ) / ( 1.0 + wr ), 0.0, 1.0 ) * directLight.color * BRDF_Lambert( material.diffuseColor ); }`)
    .replace('reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );',
      'reflectedLight.directSpecular += ' + spec.toFixed(3) + ' * irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );');
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('#include <lights_physical_pars_fragment>', phys)
      .replace('#include <roughnessmap_fragment>', '#include <roughnessmap_fragment>\n#if defined( USE_COLOR_ALPHA )\n  roughnessFactor = mix(0.45, 0.85, vColor.a);\n#else\n  roughnessFactor = 0.66;\n#endif')
      .replace('#include <color_fragment>', '#include <color_fragment>\n#if defined( USE_COLOR_ALPHA )\n  diffuseColor.a = opacity;\n#endif')
      .replace('vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;',
        `vec3 alb = max(diffuseColor.rgb, vec3(1e-3)); vec3 eSk = totalDiffuse / alb;
         float lSk = dot(eSk, vec3(0.2126, 0.7152, 0.0722)), cSk = smoothstep(0.0, 0.25, (eSk.b - eSk.r) / max(lSk, 1e-5));
         eSk = mix(eSk, lSk * vec3(1.06, 1.0, 0.92), ${warm.toFixed(3)} * cSk);
         eSk = mix(eSk, lSk * vec3(1.07, 1.0, 0.9), ${neu.toFixed(3)});
         vec3 outgoingLight = eSk * alb + totalSpecular + totalEmissiveRadiance;`); };
  mat.customProgramCacheKey = () => '|blSkin3' + warm + '|' + spec + '|' + neu;
  return mat;
}
// Cổng 6 (W4 gói nhân vật): mắt bớt "búp bê" — điểm sáng mềm, nhỏ (clearcoat 0,45, nhám 0,2; trước 1,0 / 0,05 = đốm trắng gắt);
// bóng mí + góc mắt đổ lên nhãn cầu (che khuất, theo vị trí trên nhãn cầu — không phải đèn). opts.eyeCoat / eyeCoatRough / eyeAO ghi đè.
function eyeMaterial(map, opts, R = 1) {
  const m = new THREE.MeshPhysicalMaterial({ map, roughness: 0.5, metalness: 0, clearcoat: opts.eyeCoat ?? 0.45, clearcoatRoughness: opts.eyeCoatRough ?? 0.2, envMapIntensity: 0 });
  const en = opts.eyeNeutral ?? 0.6, ao = opts.eyeAO ?? 1.0;
  m.onBeforeCompile = (sh) => {
    sh.vertexShader = 'varying vec3 vEyeP;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\nvEyeP = position;');
    sh.fragmentShader = 'varying vec3 vEyeP;\n' + sh.fragmentShader.replace('vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;',
    `vec3 albE = max(diffuseColor.rgb, vec3(1e-3)); vec3 eE = totalDiffuse / albE; float lE = dot(eE, vec3(0.2126, 0.7152, 0.0722));
     float eyU = vEyeP.y / ${R.toFixed(5)}, eyX = abs(vEyeP.x) / ${R.toFixed(5)};
     float aoE = 1.0 - ${ao.toFixed(3)} * (0.55 * smoothstep(0.0, 0.55, eyU) + 0.25 * smoothstep(0.5, 0.95, eyX)); aoE = max(aoE, 0.3);
     vec3 outgoingLight = mix(eE, vec3(lE), ${en.toFixed(3)}) * albE * aoE + totalSpecular * mix(1.0, aoE, 0.8) + totalEmissiveRadiance;`); };
  m.customProgramCacheKey = () => '|blEye6' + en + '|' + ao + '|' + R.toFixed(5);
  return m;
}

// p = { H, headG, parts, C, opts, hairMat }
export const buildIdaBL = (p) => buildBL(p, 'ida');
export const buildCasBL = (p) => buildBL(p, 'cas');
function buildBL(p, kind) {
  const CACHE = CACHES[kind];
  if (!CACHE) throw new Error(kind + "Style 'bl': cần await preload" + (kind === 'ida' ? 'Ida' : 'Cas') + "BL() trước buildCharacter");
  const { H, headG, parts, opts, hairMat } = p, meta = CACHE.meta;
  const root = new THREE.Group(); root.name = kind + '_bl'; root.scale.setScalar(H); headG.add(root);
  const src = {}; CACHE.gltf.scene.traverse((o) => { if (o.isMesh) src[o.name.replace(/^(ida|cas)_/, 'x_')] = o; });
  const reg = (m, part) => { m.userData.part = part; m.castShadow = true; m.receiveShadow = true; parts.push(m); return m; };
  const morphables = [];
  const skinMat = skinMaterial(opts);
  // Chuẩn bị một lưới có rig (CPU): trả { geo (đủ chỉ số, không vào cảnh), apply(w) }
  const rigged = (o) => {
    const g = o.geometry.clone(), names = o.morphTargetDictionary || {}, rel = g.morphTargetsRelative;
    const pa = g.attributes.position, P0 = Float32Array.from(pa.array), N0 = Float32Array.from(g.attributes.normal.array);
    const D = {}; for (const [k, i] of Object.entries(names)) { const a = g.morphAttributes.position[i].array; D[k] = rel ? Float32Array.from(a) : Float32Array.from(a, (v, j) => v - P0[j]); }
    g.morphAttributes = {}; g.morphTargetsRelative = false;
    const gN = g.clone(); gN.computeVertexNormals(); const Nm0 = Float32Array.from(gN.attributes.normal.array); gN.dispose();
    const r = { geo: g, keys: Object.keys(D), apply(w) {
      const arr = pa.array; arr.set(P0);
      for (const [k, v] of Object.entries(w || {})) { const d = D[k]; if (!v || !d) continue; for (let i = 0; i < arr.length; i++) arr[i] += v * d[i]; }
      pa.needsUpdate = true; g.computeVertexNormals();
      const na = g.attributes.normal.array; for (let i = 0; i < na.length; i += 3) { const x = N0[i] + na[i] - Nm0[i], y = N0[i + 1] + na[i + 1] - Nm0[i + 1], z = N0[i + 2] + na[i + 2] - Nm0[i + 2], l = Math.hypot(x, y, z) || 1; na[i] = x / l; na[i + 1] = y / l; na[i + 2] = z / l; }
      g.attributes.normal.needsUpdate = true; g.computeBoundingSphere(); } };
    morphables.push(r); return r;
  };
  // ĐẦU + CỔ: cùng thuộc tính đỉnh, hai chỉ số → hai lưới (part 'head' cho đo C3; 'neck' dưới đường cằm)
  const hr = rigged(src.x_head), hg = hr.geo, ix = hg.index.array, py = hg.attributes.position.array, hi = [], ni = [];
  for (let t = 0; t < ix.length; t += 3) { const a = ix[t], b = ix[t + 1], c = ix[t + 2], yc = (py[a * 3 + 1] + py[b * 3 + 1] + py[c * 3 + 1]) / 3; (yc < -0.02 ? ni : hi).push(a, b, c); }
  const sub = (idx) => { const g = new THREE.BufferGeometry(); for (const [k, v] of Object.entries(hg.attributes)) g.setAttribute(k, v); g.setIndex(idx); g.computeBoundingSphere(); return g; };
  const head = reg(new THREE.Mesh(sub(hi), skinMat), 'head'); root.add(head);
  const neck = reg(new THREE.Mesh(sub(ni), skinMat), 'neck'); root.add(neck);
  const subs = [head.geometry, neck.geometry];
  // mày (rig), tóc, búi
  const br = rigged(src.x_brows); const brows = reg(new THREE.Mesh(br.geo, hairMat), 'brow'); root.add(brows);
  for (const n of ['x_hair_shell', 'x_hair_cards', 'x_hair_fine', 'x_bun']) if (src[n]) { const m = reg(new THREE.Mesh(src[n].geometry.clone(), hairMat), 'hair'); m.position.copy(src[n].position); root.add(m); }
  // mắt: nhãn cầu riêng (tròng + giác mạc bắt sáng thật), hội tụ đã nướng trong lưới; opts.gaze [ngang, dọc] (rad)
  src.x_eye_L.geometry.computeBoundingSphere(); const eyeMat = eyeMaterial(src.x_eye_L.material.map, opts, src.x_eye_L.geometry.boundingSphere.radius), eyes = [];
  for (const n of ['x_eye_L', 'x_eye_R']) { const m = reg(new THREE.Mesh(src[n].geometry.clone(), eyeMat), 'eyes'); m.position.copy(src[n].position); m.rotation.set(opts.gaze?.[1] ?? 0, opts.gaze?.[0] ?? 0, 0); root.add(m); eyes.push(m); }
  // hoa tai treo ở dái tai (nụ + móc + giọt), vàng cũ #c9a466 — như cast3d A-α
  const ringM = new THREE.MeshStandardMaterial({ color: '#c9a466', metalness: 0.85, roughness: 0.28, emissive: new THREE.Color('#5a4424'), emissiveIntensity: 0.25 });
  for (const s of ['L', 'R']) { const e = (meta.earring || {})[s]; if (!e) continue;
    const items = [[new THREE.SphereGeometry(0.016, 14, 10), 0], [new THREE.CylinderGeometry(0.0035, 0.0035, 0.05, 6), -0.03], [new THREE.SphereGeometry(0.024, 14, 10), -0.068]];
    for (const [g, dy] of items) { const m = new THREE.Mesh(g, ringM); m.position.set(e[0], e[1] + dy, e[2]); m.userData.part = 'earring'; m.castShadow = false; m.receiveShadow = false; root.add(m); parts.push(m); } }
  let cur = {};
  const CORR = meta.correctives || {};   // lượt 3: shape key sửa lỗi — trọng số = tích các kênh 'mul' × max các kênh 'max' (vd. corr_mouth = frown × max(press, chinRaise))
  const withCorr = (w) => { const o = { ...w }; for (const [k, c] of Object.entries(CORR)) { let v = 1; for (const a of c.mul || []) v *= Math.min(1, w[a] || 0); if (c.max) v *= Math.min(1, Math.max(0, ...c.max.map((a) => w[a] || 0))); for (const [a, L] of Object.entries(c.lim || {})) v *= Math.min(w[a] || 0, L) / L; if (v > 0) o[k] = v; } return o; };
  function setFace(w = {}) { cur = { ...w }; const wc = withCorr(w); for (const r of morphables) r.apply(wc); for (const g of subs) g.computeBoundingSphere(); }
  setFace((meta.presets || {})[opts.expr] || {});   // biểu cảm dựng sẵn theo tên (như facerig.js)
  let sdf = null;   // lượt 3: khoảng cách có dấu của da 'bl' (lưới 0,025 H, nội suy ba chiều) — cast3d dùng cho mép cổ áo/khăn
  if (meta.sdf) { const { lo, h, n } = meta.sdf, bin = atob(meta.sdf.b64), u8 = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    const G = new Float32Array(u8.buffer), at = (i, j, k) => G[(i * n[1] + j) * n[2] + k];
    sdf = (x, y, z) => { const fx = (x - lo[0]) / h, fy = (y - lo[1]) / h, fz = (z - lo[2]) / h; if (fx < 0 || fy < 0 || fz < 0 || fx >= n[0] - 1 || fy >= n[1] - 1 || fz >= n[2] - 1) return 1;
      const i = Math.floor(fx), j = Math.floor(fy), k = Math.floor(fz), a = fx - i, b = fy - j, c = fz - k; let v = 0;
      for (let di = 0; di < 2; di++) for (let dj = 0; dj < 2; dj++) for (let dk = 0; dk < 2; dk++) v += (di ? a : 1 - a) * (dj ? b : 1 - b) * (dk ? c : 1 - c) * at(i + di, j + dj, k + dk);
      return v; }; }
  return { sdf, head, neck, eyes, setFace, getFace: () => cur, skinMat, meta, keys: hr.keys, root };
}

// Cine Lab · Cửa mặt Ida lượt 2 (W4) — đầu Ida 'bl': lưới dựng trong Blender (MPFB2 CC0 + tóc/mày/mắt/búi của W4), render bằng three.js.
// Dùng: await preloadIdaBL()  (một lần, TRƯỚC buildCharacter — GLTFLoader bất đồng bộ, buildCharacter đồng bộ)
//       buildCharacter(sheet, { idaStyle: 'bl', … })  → cast3d gọi buildIdaBL(…) thay cho đầu/tóc/tai/cổ.
// GLTFLoader của three (examples/jsm) import 'three' dạng tên trần; trang của dự án không có import map → nạp mã loader qua Blob,
// thay 'three' bằng URL tuyệt đối của three.module.js (cùng URL với cả dự án → cùng một thực thể module).
// Rig: shape key của glb (TÊN = 16 kênh facerig.js + vis_*) tính trên CPU như facerig.js (mọi pass, kể cả G-buffer lớp vẽ, thấy đúng hình);
// morph GPU bị gỡ. Pháp tuyến: N0 (glb) + (N(lưới biến dạng) − N(lưới gốc)) → không lộ đường nối UV.
import * as THREE from '../../../shared/node_modules/three/build/three.module.js';

export const BL_URL = new URL('./ida_bl.glb', import.meta.url).href;
let CACHE = null;

async function loadGLTFLoader() {
  const base = new URL('../../../shared/node_modules/three/', import.meta.url).href, threeURL = base + 'build/three.module.js';
  const fix = (src) => src.replace(/from\s*'three'/g, `from '${threeURL}'`);
  const blobURL = (src) => URL.createObjectURL(new Blob([src], { type: 'text/javascript' }));
  const bgu = blobURL(fix(await (await fetch(base + 'examples/jsm/utils/BufferGeometryUtils.js')).text()));
  const gl = fix(await (await fetch(base + 'examples/jsm/loaders/GLTFLoader.js')).text()).replace("'../utils/BufferGeometryUtils.js'", `'${bgu}'`);
  return (await import(blobURL(gl))).GLTFLoader;
}

export async function preloadIdaBL(url = BL_URL) {
  if (CACHE && CACHE.url === url) return CACHE;
  const GLTFLoader = await loadGLTFLoader();
  const [gltf, meta] = await Promise.all([new GLTFLoader().loadAsync(url), fetch(url.replace(/\.glb$/, '.json')).then((r) => r.json())]);
  CACHE = { url, gltf, meta };
  return CACHE;
}
export const idaBLReady = () => !!CACHE;

// Da: PBR mờ (nhám 0,66, bóng gương 0,3) + khuếch tán "bọc" lệch đỏ (tán xạ dưới da giả lập) + giữ sắc ấm khi ánh lạnh + kéo 35 % ánh hổ phách về trung tính.
function skinMaterial(opts) {
  const mat = new THREE.MeshStandardMaterial({ color: 0xffffff, vertexColors: true, roughness: opts.skinRough ?? 0.66, metalness: 0, envMapIntensity: 0 });
  const warm = opts.skinWarm ?? 0.7, spec = opts.skinSpec ?? 0.3, neu = opts.skinNeutral ?? 0.35;
  const phys = THREE.ShaderChunk.lights_physical_pars_fragment
    .replace('reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );',
      `{ float nlW = dot( geometryNormal, directLight.direction ); vec3 wr = vec3( 0.30, 0.14, 0.10 );
        reflectedLight.directDiffuse += clamp( ( vec3( nlW ) + wr ) / ( 1.0 + wr ), 0.0, 1.0 ) * directLight.color * BRDF_Lambert( material.diffuseColor ); }`)
    .replace('reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );',
      'reflectedLight.directSpecular += ' + spec.toFixed(3) + ' * irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );');
  mat.onBeforeCompile = (sh) => {
    sh.fragmentShader = sh.fragmentShader.replace('#include <lights_physical_pars_fragment>', phys)
      .replace('vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;',
        `vec3 alb = max(diffuseColor.rgb, vec3(1e-3)); vec3 eSk = totalDiffuse / alb;
         float lSk = dot(eSk, vec3(0.2126, 0.7152, 0.0722)), cSk = smoothstep(0.0, 0.25, (eSk.b - eSk.r) / max(lSk, 1e-5));
         eSk = mix(eSk, lSk * vec3(1.06, 1.0, 0.92), ${warm.toFixed(3)} * cSk);
         eSk = mix(eSk, lSk * vec3(1.07, 1.0, 0.9), ${neu.toFixed(3)});
         vec3 outgoingLight = eSk * alb + totalSpecular + totalEmissiveRadiance;`); };
  mat.customProgramCacheKey = () => '|blSkin' + warm + '|' + spec + '|' + neu;
  return mat;
}
function eyeMaterial(map, opts) {
  const m = new THREE.MeshPhysicalMaterial({ map, roughness: 0.4, metalness: 0, clearcoat: 1.0, clearcoatRoughness: 0.05, envMapIntensity: 0 });
  const en = opts.eyeNeutral ?? 0.6;
  m.onBeforeCompile = (sh) => { sh.fragmentShader = sh.fragmentShader.replace('vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;',
    `vec3 albE = max(diffuseColor.rgb, vec3(1e-3)); vec3 eE = totalDiffuse / albE; float lE = dot(eE, vec3(0.2126, 0.7152, 0.0722));
     vec3 outgoingLight = mix(eE, vec3(lE), ${en.toFixed(3)}) * albE + totalSpecular + totalEmissiveRadiance;`); };
  m.customProgramCacheKey = () => '|blEye' + en;
  return m;
}

// p = { H, headG, parts, C, opts, hairMat }
export function buildIdaBL(p) {
  if (!CACHE) throw new Error("idaStyle 'bl': cần await preloadIdaBL() trước buildCharacter");
  const { H, headG, parts, opts, hairMat } = p, meta = CACHE.meta;
  const root = new THREE.Group(); root.name = 'ida_bl'; root.scale.setScalar(H); headG.add(root);
  const src = {}; CACHE.gltf.scene.traverse((o) => { if (o.isMesh) src[o.name] = o; });
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
  const hr = rigged(src.ida_head), hg = hr.geo, ix = hg.index.array, py = hg.attributes.position.array, hi = [], ni = [];
  for (let t = 0; t < ix.length; t += 3) { const a = ix[t], b = ix[t + 1], c = ix[t + 2], yc = (py[a * 3 + 1] + py[b * 3 + 1] + py[c * 3 + 1]) / 3; (yc < -0.02 ? ni : hi).push(a, b, c); }
  const sub = (idx) => { const g = new THREE.BufferGeometry(); for (const [k, v] of Object.entries(hg.attributes)) g.setAttribute(k, v); g.setIndex(idx); g.computeBoundingSphere(); return g; };
  const head = reg(new THREE.Mesh(sub(hi), skinMat), 'head'); root.add(head);
  const neck = reg(new THREE.Mesh(sub(ni), skinMat), 'neck'); root.add(neck);
  const subs = [head.geometry, neck.geometry];
  // mày (rig), tóc, búi
  const br = rigged(src.ida_brows); const brows = reg(new THREE.Mesh(br.geo, hairMat), 'brow'); root.add(brows);
  for (const n of ['ida_hair_shell', 'ida_hair_cards', 'ida_hair_fine', 'ida_bun']) if (src[n]) { const m = reg(new THREE.Mesh(src[n].geometry.clone(), hairMat), 'hair'); m.position.copy(src[n].position); root.add(m); }
  // mắt: nhãn cầu riêng (tròng + giác mạc bắt sáng thật), hội tụ đã nướng trong lưới; opts.gaze [ngang, dọc] (rad)
  const eyeMat = eyeMaterial(src.ida_eye_L.material.map, opts), eyes = [];
  for (const n of ['ida_eye_L', 'ida_eye_R']) { const m = reg(new THREE.Mesh(src[n].geometry.clone(), eyeMat), 'eyes'); m.position.copy(src[n].position); m.rotation.set(opts.gaze?.[1] ?? 0, opts.gaze?.[0] ?? 0, 0); root.add(m); eyes.push(m); }
  // hoa tai treo ở dái tai (nụ + móc + giọt), vàng cũ #c9a466 — như cast3d A-α
  const ringM = new THREE.MeshStandardMaterial({ color: '#c9a466', metalness: 0.85, roughness: 0.28, emissive: new THREE.Color('#5a4424'), emissiveIntensity: 0.25 });
  for (const s of ['L', 'R']) { const e = meta.earring[s]; if (!e) continue;
    const items = [[new THREE.SphereGeometry(0.016, 14, 10), 0], [new THREE.CylinderGeometry(0.0035, 0.0035, 0.05, 6), -0.03], [new THREE.SphereGeometry(0.024, 14, 10), -0.068]];
    for (const [g, dy] of items) { const m = new THREE.Mesh(g, ringM); m.position.set(e[0], e[1] + dy, e[2]); m.userData.part = 'earring'; m.castShadow = false; m.receiveShadow = false; root.add(m); parts.push(m); } }
  let cur = {};
  function setFace(w = {}) { cur = { ...w }; for (const r of morphables) r.apply(w); for (const g of subs) g.computeBoundingSphere(); }
  setFace((meta.presets || {})[opts.expr] || {});   // biểu cảm dựng sẵn theo tên (như facerig.js)
  return { head, neck, eyes, setFace, getFace: () => cur, skinMat, meta, keys: hr.keys, root };
}

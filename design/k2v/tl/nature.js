// K2V tl · CÂY INSTANCED + ĐƯỜNG theo năm (lớp 3 chuẩn hình).
// Cây: vị trí từ NDVI Sentinel-2 (thảm cây bụi/rừng thông trên Rock, cây ngoài phố — luôn có) + cây OSM trong phố (mọc theo năm đô thị).
// Đường: dải phủ theo địa hình từ OSM; hiện từ năm đô thị của khu (hoặc mốc ảnh c.1900 cho trục biên giới); trước 1940 mặt đường đất cát.
import { THREE, rng } from './core.js';
const TT = 600;
export function makeTrees(T, hAt, U, { lod = true } = {}) {
  const geo = (() => { const c = new THREE.IcosahedronGeometry(1, U.treeDetail ?? 0); c.scale(0.9, 0.75, 0.9); c.translate(0, 1.15, 0);   // tán 20 mặt (chi tiết 1 = 80 mặt: đo V5b-1)
    const t = new THREE.CylinderGeometry(0.09, 0.12, 0.6, 4, 1, true); t.translate(0, 0.3, 0);
    const P = [], N = [], C = [];
    for (const [g, col] of [[c, [1, 1, 1]], [t, [0.42, 0.33, 0.24]]]) { const gg = g.toNonIndexed(); P.push(...gg.attributes.position.array); N.push(...gg.attributes.normal.array); for (let i = 0; i < gg.attributes.position.count; i++) C.push(...col); }
    const G = new THREE.BufferGeometry(); G.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); G.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); G.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); return G; })();
  const mat = U.lambert ? new THREE.MeshLambertMaterial({ vertexColors: true }) : new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.9 });
  mat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uYear: U.uYear, uDim: U.uDim });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aYear; uniform float uYear;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\n transformed *= clamp((uYear - (aYear - 3.0)) / 3.0, 0.0, 1.0);');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uDim;').replace('#include <dithering_fragment>', '#include <dithering_fragment>\n { float L = dot(gl_FragColor.rgb, vec3(0.299,0.587,0.114)); gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(L), 0.55*uDim) * (1.0 - 0.36*uDim); }'); };
  // bóng của cây chưa mọc: vật liệu độ sâu cùng phép co theo năm (lỗi lượt 1: bóng cây tương lai lấm tấm trên eo đất)
  const dmat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }); dmat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uYear: U.uYear });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aYear; uniform float uYear;').replace('#include <begin_vertex>', '#include <begin_vertex>\n transformed *= clamp((uYear - (aYear - 3.0)) / 3.0, 0.0, 1.0);'); };
  const by = new Map(); for (let i = 0; i < T.length; i += 4) { const k = Math.floor(T[i] / TT) + ',' + Math.floor(T[i + 1] / TT); if (!by.has(k)) by.set(k, []); by.get(k).push(i); }
  const group = new THREE.Group(), tiles = [], R = rng(5), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3();
  const greens = [[0.20, 0.30, 0.13], [0.26, 0.34, 0.16], [0.17, 0.26, 0.14], [0.31, 0.36, 0.20]];
  for (const [k, idx] of by) {
    const im = new THREE.InstancedMesh(geo, mat, idx.length), yr = new Float32Array(idx.length);
    idx.forEach((i, j) => { const e = T[i], n = T[i + 1], h = T[i + 2]; p.set(e, hAt(e, n) - 0.2, -n); const w = h * (0.45 + 0.25 * R()); s.set(w, h * 0.6, w);
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), R() * 6.28); m4.compose(p, q, s); im.setMatrixAt(j, m4); const g = greens[Math.floor(R() * 4)]; im.setColorAt(j, new THREE.Color(g[0], g[1], g[2])); yr[j] = T[i + 3]; });
    im.geometry = geo.clone(); im.geometry.setAttribute('aYear', new THREE.InstancedBufferAttribute(yr, 1));
    im.customDepthMaterial = dmat; im.castShadow = true; im.receiveShadow = true; im.frustumCulled = false; const [tx, tn] = k.split(',').map(Number); im.userData.c = [(tx + 0.5) * TT, -(tn + 0.5) * TT];
    group.add(im); tiles.push(im);
  }
  function update(cam) { for (const im of tiles) { const d = Math.hypot(cam.position.x - im.userData.c[0], cam.position.z - im.userData.c[1]) - cam.position.y * 0.3; im.visible = !lod || d < 2000; } }
  return { group, update, n: T.length / 4 };
}

export function makeRoads(roads, hAt, U) {
  const P = [], A = [], W = [];
  for (const r of roads) {
    const Y = Array.isArray(r.y) ? r.y : r.p.map(() => r.y), pts = [], py = [];   // năm theo từng đỉnh (build_scene.py)
    for (let i = 0; i < r.p.length - 1; i++) { const [a, b] = [r.p[i], r.p[i + 1]], l = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(1, Math.ceil(l / 12));
      for (let k = 0; k < n; k++) { pts.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]); py.push(Math.max(Y[i], Y[i + 1])); } } pts.push(r.p[r.p.length - 1]); py.push(Y[Y.length - 1]);
    const hw = r.w / 2, cls = { trunk: 1, primary: 1, secondary: 1, tertiary: 0.8, pedestrian: 0.3, service: 0.5 }[r.c] ?? 0.6;
    for (let i = 0; i < pts.length - 1; i++) { const [a, b] = [pts[i], pts[i + 1]], dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1, ox = -dn / l * hw, on = dx / l * hw;
      const yy = py[i], v = (e, n, s) => { P.push(e, Math.max(hAt(e, n), 0.2) + 0.25, -n); A.push(yy, cls, s); };
      const q = [[a[0] + ox, a[1] + on, 1], [a[0] - ox, a[1] - on, -1], [b[0] + ox, b[1] + on, 1], [b[0] - ox, b[1] - on, -1]];
      for (const k of [0, 1, 2, 2, 1, 3]) v(...q[k]); }
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('aRd', new THREE.Float32BufferAttribute(A, 3)); g.computeVertexNormals();
  const n = new Float32Array(P.length); for (let i = 1; i < n.length; i += 3) n[i] = 1; g.setAttribute('normal', new THREE.BufferAttribute(n, 3));
  const mat = (U.lambert ? new THREE.MeshLambertMaterial({ color: 0xffffff, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }) : new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.92, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }));
  mat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uYear: U.uYear, uDim: U.uDim });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute vec3 aRd; varying vec3 vRd; varying vec3 vWP2;').replace('#include <begin_vertex>', '#include <begin_vertex>\n vRd = aRd; vWP2 = (modelMatrix * vec4(transformed,1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uYear, uDim; varying vec3 vRd; varying vec3 vWP2;')
      .replace('#include <color_fragment>', `#include <color_fragment>
      float a = smoothstep(vRd.x - 1.0, vRd.x, uYear); if (a < 0.02) discard;
      vec3 dirt = vec3(0.70, 0.63, 0.50), asph = mix(vec3(0.30, 0.31, 0.33), vec3(0.55, 0.53, 0.50), 1.0 - vRd.y);
      vec3 c = mix(dirt, asph, smoothstep(1935.0, 1950.0, uYear));
      float edge = smoothstep(0.80, 0.92, abs(vRd.z)) * step(0.7, vRd.y) * smoothstep(1955.0, 1965.0, uYear);   // vạch mép đường chính
      c = mix(c, vec3(0.82, 0.82, 0.80), edge * 0.6);
      float L = dot(c, vec3(0.299,0.587,0.114)); c = mix(c, vec3(L), 0.55*uDim) * (1.0 - 0.36*uDim);
      diffuseColor.rgb = c; diffuseColor.a = a;`); };
  mat.transparent = true; mat.depthWrite = false;
  const mesh = new THREE.Mesh(g, mat); mesh.receiveShadow = true; mesh.frustumCulled = false; mesh.renderOrder = 1;
  return { mesh, tris: P.length / 9 };
}

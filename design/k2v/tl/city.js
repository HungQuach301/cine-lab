// K2V tl · NHÀ THƯỜNG THỦ TỤC (lớp 2 chuẩn hình) + MỌC THEO NĂM (port lab/timelapse scene.js: hình học gộp + shader mọc).
// Bản ghi toà: [năm, năm_ghost, cao, cốt chân, mái (0 phẳng | 1 dốc), vùng (0 La Línea | 1 Gibraltar), vòng [[E,N]…]].
//  · mọc: toà nổi lên trong aDur năm, kết thúc đúng năm (Catastro: năm xây = năm hoàn thành; mốc tầng chuẩn: 1,5 năm trước mốc);
//  · ghost: từ năm_ghost tới khi toà thật đầy, phần trên đường cắt vẽ mờ (screen-door + tích luỹ SPP), không đổ bóng;
//  · vật liệu theo vùng + thời kỳ (vôi trắng/kem Andalucía; phấn màu kiểu Genoa ở Gibraltar; bê tông/gạch sau 1960);
//  · cửa sổ bằng shader (lưới tầng 3,0 m × khoang theo vùng, chớp xanh/gỗ, tầng trệt cửa hiệu), mờ dần theo khoảng cách (chống răng cưa);
//  · LOD theo ô 500 m: gần (LOD0: mái dốc, đủ đỉnh) · xa (LOD1: vòng đơn giản 2,5 m, mái phẳng) · rất xa: ẩn — nền ảnh vệ tinh làm impostor.
import { THREE, GLSL_NOISE, rng } from './core.js';
import { walls, roof, ridgeFor, simplify } from './geom.js';

const PAL = {
  0: { old: [[0.95, 0.93, 0.88], [0.94, 0.90, 0.80], [0.93, 0.86, 0.70], [0.96, 0.95, 0.92]], mod: [[0.90, 0.88, 0.84], [0.82, 0.74, 0.62], [0.78, 0.77, 0.75], [0.93, 0.91, 0.86]], roofFlat: [0.80, 0.78, 0.74], tile: [0.68, 0.36, 0.25] },
  1: { old: [[0.93, 0.84, 0.64], [0.91, 0.78, 0.60], [0.94, 0.88, 0.72], [0.88, 0.70, 0.58]], mod: [[0.86, 0.84, 0.80], [0.76, 0.75, 0.73], [0.90, 0.86, 0.76], [0.70, 0.72, 0.74]], roofFlat: [0.74, 0.72, 0.69], tile: [0.66, 0.34, 0.24] },
};
const TILE = 500;

export function makeCity(B, U, { lod = true } = {}) {
  const tiles = new Map(); const R = rng(17);
  const tri = (r) => THREE.ShapeUtils.triangulateShape(r.map(([x, y]) => new THREE.Vector2(x, y)), []);
  const add = (key) => { if (!tiles.has(key)) tiles.set(key, { L: [{ a: [] }, { a: [] }], c: null, n: 0 }); return tiles.get(key); };
  for (const b of B) {
    const [y, gy, h, base, rf, reg, ring] = b; if (ring.length < 3) continue;
    let cx = 0, cn = 0; for (const p of ring) { cx += p[0]; cn += p[1]; } cx /= ring.length; cn /= ring.length;
    const T = add(Math.floor(cx / TILE) + ',' + Math.floor(cn / TILE)); T.n++;
    const P = PAL[reg], r1 = R(), mod = y >= 1960 && !(gy && y >= 1987 && reg === 1);
    const wc = (mod ? P.mod : P.old)[Math.floor(r1 * 4)].map((v) => v * (0.94 + 0.08 * R()));
    const rc = rf ? P.tile.map((v) => v * (0.9 + 0.15 * R())) : P.roofFlat.map((v) => v * (0.92 + 0.1 * R()));
    const dur = reg === 1 && !gy ? 1.5 : (reg === 1 ? 1.5 : 4.0);
    const seed = R();
    for (let l = 0; l < 2; l++) {
      const A = T.L[l].a, rr = l === 0 ? ring : simplify(ring, 2.5);
      const emit = (col) => (x, yy, z, nx, ny, nz, u, top) => A.push(x, yy, z, nx, ny, nz, col[0], col[1], col[2], y, gy, base, u, dur, h, reg + seed * 0.5);
      walls(rr, h, emit(wc));
      roof(rr, h, l === 0 && rf ? ridgeFor(rr) : 0, tri, emit(rc));
    }
  }
  const mkMat = (lodLevel, depth) => {
    const m = depth ? new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }) : U.lambert ? new THREE.MeshLambertMaterial({ vertexColors: true }) : new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.88, metalness: 0 });
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, { uYear: U.uYear, uDim: U.uDim, uSample: U.uSample });
      sh.vertexShader = sh.vertexShader.replace('#include <common>', `#include <common>
        attribute float aYear; attribute float aGhost; attribute float aBase; attribute float aU; attribute float aDur; attribute float aH; attribute float aReg;
        uniform float uYear; varying float vU; varying float vLY; varying float vCut; varying float vGhost; varying float vReg; varying float vH; varying float vYear;
        float growK(){ float u = clamp((uYear - (aYear - aDur)) / aDur, 0.0, 1.0); return u < 1.0 ? (1.0 - pow(1.0 - u, 3.0)) * 1.05 - 0.05 * u * u : 1.0; }`)
        .replace('#include <begin_vertex>', `#include <begin_vertex>
        float gk = growK(); bool gh = aGhost > 0.5 && uYear >= aGhost;
        vLY = transformed.y; vU = aU; vReg = aReg; vH = aH; vYear = aYear; vGhost = gh ? 1.0 : 0.0;
        vCut = gh ? aH * gk : 1e5;   // ghost: phần trên đường cắt (chiều cao đã mọc) vẽ mờ
        // ghost = VÙNG có bằng chứng, không phải chiều cao toà hiện nay: khối mờ cao tối đa 12 m (3–4 tầng), toà thật mọc xuyên qua
        if (gh) transformed.y *= max(gk, min(1.0, 12.0 / max(aH, 1.0))); else transformed.y *= gk;
        if (!gh && gk <= 0.0) transformed.y -= 80.0;
        transformed.y += aBase;`);
      const FR = `${GLSL_NOISE}
        uniform float uYear, uDim, uSample; varying float vU; varying float vLY; varying float vCut; varying float vGhost; varying float vReg; varying float vH; varying float vYear;
        bool ghostFrag(){ return vGhost > 0.5 && vLY > vCut + 0.02; }
        bool sdoor(){ float h = h21(floor(gl_FragCoord.xy) + vec2(uSample * 7.31, uSample * 3.17)); return h < 0.62; }`;
      if (depth) {
        sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + FR).replace('void main() {', 'void main() {\n if (ghostFrag()) discard;');
        return;
      }
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + FR)
        .replace('#include <color_fragment>', `#include <color_fragment>
        bool G = ghostFrag(); if (G && sdoor()) discard;
        float dd = length(vViewPosition);
        if (vU >= 0.0 && ${lodLevel === 0 ? 'true' : 'false'}) {   // cửa sổ: lưới tầng 3 m × khoang
          float bay = vReg < 1.0 ? 3.3 : 2.9; vec2 q = vec2(vU / bay, vLY / 3.0); vec2 f = fract(q); vec2 id = floor(q);
          float aa = clamp(fwidth(q.x) * 3.0, 0.0, 1.0);
          float win = step(0.30, f.x) * step(f.x, 0.70) * step(0.28, f.y) * step(f.y, 0.78) * step(1.0, id.y) * step(vLY, vH - 0.8);
          float shop = (1.0 - step(1.0, id.y)) * step(0.15, f.x) * step(f.x, 0.85) * step(f.y, 0.70) * step(0.5, h21(id + 3.0));
          float shut = step(0.5, h21(id * 1.7 + floor(vReg * 97.0)));
          vec3 glass = vec3(0.16, 0.20, 0.25) + 0.10 * h21(id);
          vec3 shc = vReg >= 1.0 && vReg < 1.5 ? vec3(0.24, 0.36, 0.26) : vec3(0.40, 0.31, 0.22);
          vec3 wcol = mix(glass, shc, shut * step(vYear, 1975.0) * 0.85);
          float k = max(win, shop * 0.9) * (1.0 - aa) * (1.0 - smoothstep(700.0, 1600.0, dd));
          diffuseColor.rgb = mix(diffuseColor.rgb, wcol, k);
          diffuseColor.rgb *= 1.0 - 0.06 * step(fract(vLY / 3.0), 0.05) * (1.0 - aa);   // gờ tầng
        }
        diffuseColor.rgb *= 0.70 + 0.30 * smoothstep(0.0, 7.0, vLY);   // AO chân tường
        diffuseColor.rgb *= 0.93 + 0.12 * vn(vec2(vU * 0.4, vLY * 0.6));   // loang vữa
        if (G) diffuseColor.rgb = mix(vec3(0.86, 0.90, 0.95), diffuseColor.rgb, 0.15);
        float L = dot(diffuseColor.rgb, vec3(0.299, 0.587, 0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55 * uDim) * (1.0 - 0.36 * uDim);`);
    };
    return m;
  };
  const mats = [mkMat(0, false), mkMat(1, false)], depth = mkMat(0, true);
  const group = new THREE.Group(); let tris = [0, 0];
  for (const [key, T] of tiles) {
    const [tx, tn] = key.split(',').map(Number); T.c = new THREE.Vector3((tx + 0.5) * TILE, 0, -(tn + 0.5) * TILE); T.m = [];
    for (let l = 0; l < 2; l++) {
      const A = new Float32Array(T.L[l].a), n = A.length / 16, g = new THREE.BufferGeometry(); T.L[l].a = null;
      const at = (o, s) => { const out = new Float32Array(n * s); for (let i = 0; i < n; i++) for (let k = 0; k < s; k++) out[i * s + k] = A[i * 16 + o + k]; return out; };
      g.setAttribute('position', new THREE.BufferAttribute(at(0, 3), 3)); g.setAttribute('normal', new THREE.BufferAttribute(at(3, 3), 3)); g.setAttribute('color', new THREE.BufferAttribute(at(6, 3), 3));
      for (const [nm, o] of [['aYear', 9], ['aGhost', 10], ['aBase', 11], ['aU', 12], ['aDur', 13], ['aH', 14], ['aReg', 15]]) g.setAttribute(nm, new THREE.BufferAttribute(at(o, 1), 1));
      g.boundingSphere = new THREE.Sphere(T.c.clone().setY(30), TILE); const mesh = new THREE.Mesh(g, mats[l]); mesh.customDepthMaterial = depth;
      mesh.castShadow = mesh.receiveShadow = true; mesh.visible = l === 0; group.add(mesh); T.m.push(mesh); tris[l] += n / 3;
    }
  }
  // chọn LOD theo khoảng cách máy (mặt bằng) tới tâm ô
  const near = 1400, far = 5200; let stat = { lod0: 0, lod1: 0, off: 0 };
  function update(cam) { stat = { lod0: 0, lod1: 0, off: 0 };
    for (const T of tiles.values()) { const d = Math.hypot(cam.position.x - T.c.x, cam.position.z - T.c.z) - Math.max(0, cam.position.y * 0.2);
      const l = !lod ? 0 : d < near ? 0 : d < far ? 1 : 2; T.m[0].visible = l === 0; T.m[1].visible = l === 1; stat[['lod0', 'lod1', 'off'][l]]++; } }
  return { group, update, stat: () => stat, tris, nTiles: tiles.size };
}

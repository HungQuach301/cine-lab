// Cine Lab · Cổng 3 · Hướng A "Tin & Felt" — thư viện vật liệu thủ tục + tiện ích hình học.
// Mọi kết cấu sinh bằng mã trong shader (không texture ngoài). Vật liệu dựa trên MeshStandard/MeshPhysical của three.js,
// chèn thêm: nhiễu sợi dạ, len đan, thiếc gò, vữa vôi, gạch quét vôi, đá lát, ngói, mặt tiền có cửa sổ.
import * as THREE from '../shared/node_modules/three/build/three.module.js';

const BASE = new URL('../shared/node_modules/three/', import.meta.url).href;
// Addon của three import 'three' (bare specifier) → nạp qua blob với đường dẫn tuyệt đối (không có import map).
export async function importAddon(rel) { return import(await addonURL(BASE + 'examples/jsm/' + rel)); }
const _blobs = new Map();
async function addonURL(url) {
  if (_blobs.has(url)) return _blobs.get(url);
  const dir = url.slice(0, url.lastIndexOf('/') + 1);
  let src = await (await fetch(url)).text();
  src = src.replace(/from\s+'three'/g, `from '${BASE}build/three.module.js'`);
  const rels = [...src.matchAll(/from\s+'(\.\/[^']+)'/g)].map((m) => m[1]);
  for (const r of rels) src = src.split(`'${r}'`).join(`'${await addonURL(dir + r.slice(2))}'`);
  const u = URL.createObjectURL(new Blob([src], { type: 'text/javascript' })); _blobs.set(url, u); return u;
}

const COMMON = /* glsl */`
varying vec3 vWP; varying vec3 vWN; varying vec2 vUvP; varying vec4 vAux;
float pH = 0.0; float pRough = 0.0; float pMetal = -1.0; vec3 pEmit = vec3(0.0);
float h13(vec3 p){ p = fract(p*vec3(0.1031,0.1030,0.0973)); p += dot(p, p.yzx+33.33); return fract((p.x+p.y)*p.z); }
float h12(vec2 p){ return h13(vec3(p, 17.17)); }
float vn(vec3 p){ vec3 i=floor(p); vec3 f=fract(p); f=f*f*(3.0-2.0*f);
  float a=h13(i), b=h13(i+vec3(1,0,0)), c=h13(i+vec3(0,1,0)), d=h13(i+vec3(1,1,0));
  float e=h13(i+vec3(0,0,1)), g=h13(i+vec3(1,0,1)), k=h13(i+vec3(0,1,1)), l=h13(i+vec3(1,1,1));
  return mix(mix(mix(a,b,f.x),mix(c,d,f.x),f.y), mix(mix(e,g,f.x),mix(k,l,f.x),f.y), f.z); }
float fbm(vec3 p){ return 0.5*vn(p)+0.25*vn(p*2.03+11.3)+0.125*vn(p*4.07+27.1)+0.0625*vn(p*8.11+5.7); }
float fbm2(vec3 p){ return 0.6667*vn(p)+0.3333*vn(p*2.03+11.3); }
// Bump theo đạo hàm màn hình (Mikkelsen), chiều cao tính bằng mét — không phụ thuộc cỡ điểm ảnh.
vec3 pBump(vec3 sp, vec3 n, float h, float fd){
  vec3 sx = dFdx(sp), sy = dFdy(sp); vec3 r1 = cross(sy, n), r2 = cross(n, sx);
  float det = dot(sx, r1) * fd; vec2 dh = vec2(dFdx(h), dFdy(h));
  vec3 g = sign(det) * (dh.x*r1 + dh.y*r2);
  return normalize(abs(det)*n - g);
}
`;

// ---------- mã từng loại bề mặt (chạy sau color_fragment; biến: diffuseColor, vWP, vWN, vUvP, vAux) ----------
const KIND = {
  // Dạ/nỉ: loang màu mảng lớn + lông tơ mịn; đường may nổi theo UV (lathe: u quanh, v dọc profile).
  felt: (o) => `
    vec3 p = vWP;
    float m = fbm(p*${(o.mot ?? 7).toFixed(2)});
    float fib = vn(p*230.0)*0.5 + vn(p*97.0)*0.5;
    diffuseColor.rgb *= (0.82 + 0.34*m) * (0.88 + 0.24*fib);
    pH = fib*0.0010 + m*0.0022;
    ${o.stitchV != null ? `
    { float sv = abs(vUvP.y - ${o.stitchV.toFixed(4)});
      float dash = step(0.42, fract(vUvP.x*${(o.stitchN ?? 60).toFixed(1)}));
      float W = ${(o.stitchW ?? 0.006).toFixed(4)};
      float st = (1.0 - smoothstep(W*0.35, W, sv)) * dash;
      float gr = (1.0 - smoothstep(W, W*2.6, sv)) * (1.0 - st);
      diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb*1.45 + vec3(0.035,0.03,0.02), st*0.85);
      diffuseColor.rgb *= 1.0 - 0.22*gr; pH += st*0.0014 - gr*0.0010; }` : ''}
    ${o.stitchU != null ? `
    { float su = min(abs(vUvP.x - ${o.stitchU.toFixed(4)}), 1.0);
      float dash = step(0.42, fract(vUvP.y*${(o.stitchNU ?? 40).toFixed(1)}));
      float W = ${(o.stitchWU ?? 0.012).toFixed(4)};
      float st = (1.0 - smoothstep(W*0.35, W, su)) * dash;
      diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb*1.45 + vec3(0.035,0.03,0.02), st*0.85); pH += st*0.0014; }` : ''}`,
  // Len đan (áo len, mũ len của Cas): hàng mắt chữ V theo UV.
  knit: (o) => `
    vec2 k = vec2(vUvP.x*${(o.n ?? 70).toFixed(1)}, vUvP.y*${(o.m ?? 70).toFixed(1)});
    float sx = fract(k.x) - 0.5;
    float yy = k.y + abs(sx)*0.9;
    float loop = sin(fract(yy)*3.14159);
    float colm = 1.0 - pow(abs(sx)*2.0, 3.0);
    float hk = loop*colm;
    float fib = vn(vWP*260.0);
    float m = fbm(vWP*6.0);
    diffuseColor.rgb *= (0.66 + 0.40*hk) * (0.9 + 0.2*fib) * (0.9 + 0.2*m);
    pH = hk*${(o.depth ?? 0.0022).toFixed(4)} + fib*0.0006;`,
  // Len thô / quả bông / tóc: sợi dài theo hướng dọc.
  wool: (o) => `
    vec3 p = vWP;
    float s = vn(vec3(p.x*${(o.fx ?? 120).toFixed(1)}, p.y*${(o.fy ?? 30).toFixed(1)}, p.z*${(o.fx ?? 120).toFixed(1)}));
    float f = vn(p*300.0); float m = fbm(p*10.0);
    diffuseColor.rgb *= (0.72 + 0.45*s) * (0.9 + 0.2*f) * (0.9+0.2*m);
    pH = s*0.0018 + f*0.0008;`,
  leather: () => `
    float n = fbm(vWP*55.0); float f = vn(vWP*320.0);
    diffuseColor.rgb *= 0.78 + 0.4*n; pH = f*0.0003 + n*0.0006; pRough = (0.5-n)*0.3;`,
  // Thiếc gò tay: lõm búa, xỉn, loang ô-xy.
  tin: () => `
    float d = vn(vWP*46.0); float pat = fbm(vWP*13.0);
    diffuseColor.rgb *= 0.62 + 0.55*pat; pH = -d*0.0010; pRough = (0.55-pat)*0.35;`,
  // Vữa trát quét vôi (vách trong hốc).
  lime: (o) => `
    vec3 p = vWP;
    float m = fbm(p*vec3(1.4,2.0,1.4));
    float tr = fbm(vec3((p.x+p.z)*4.0, p.y*0.9, (p.x-p.z)*1.0));
    float fine = vn(p*150.0);
    float gy = p.y - ${(o.ground ?? 0).toFixed(3)};
    float damp = 1.0 - smoothstep(0.0, 0.75, gy + (m-0.5)*0.7);
    vec3 c = diffuseColor.rgb * (0.88 + 0.14*m + 0.05*tr);
    c = mix(c, c*vec3(0.74,0.70,0.60), damp*0.75);
    float flake = smoothstep(0.64, 0.70, fbm(p*3.3+3.0));
    c = mix(c, c*vec3(0.90,0.89,0.87), flake*0.6);
    float scuff = smoothstep(0.66, 0.72, fbm(vec3(p.x*9.0+p.z*9.0, p.y*30.0, 1.0))) * (1.0 - smoothstep(0.3, 1.2, gy));
    c *= 1.0 - 0.18*scuff;
    diffuseColor.rgb = c;
    pH = tr*0.0025 + fine*0.0004 - flake*0.0016;`,
  // Gạch quét vôi: mạch vữa lõm, vôi bong lộ gạch.
  brickwash: (o) => `
    vec3 p = vWP; vec3 n = normalize(vWN);
    float a = abs(n.x) > abs(n.z) ? p.z : p.x;
    vec2 b = vec2(a/0.23, (p.y+0.013)/0.077);
    float row = floor(b.y); b.x += mod(row, 2.0)*0.5;
    vec2 id = floor(b); vec2 f = fract(b);
    float edge = min(min(f.x, 1.0-f.x)*0.23, min(f.y, 1.0-f.y)*0.077);
    float groove = smoothstep(0.004, 0.012, edge);
    float rnd = h12(id);
    vec3 brick = mix(vec3(0.34,0.15,0.10), vec3(0.50,0.28,0.18), rnd);
    float wn = fbm(p*vec3(1.8,2.6,1.8)) + 0.12*vn(p*20.0);
    float wash = smoothstep(${(o.worn ?? 0.30).toFixed(2)}, ${(o.worn ?? 0.30).toFixed(2)}+0.08, wn);
    vec3 lime = diffuseColor.rgb * (0.90 + 0.10*rnd);
    vec3 c = mix(brick, lime, wash);
    vec3 mortar = diffuseColor.rgb*0.72;
    c = mix(mortar, c, mix(0.5, 1.0, groove));
    float gy = p.y - ${(o.ground ?? 0).toFixed(3)};
    c = mix(c, c*vec3(0.70,0.66,0.58), (1.0 - smoothstep(0.0, 0.9, gy + (wn-0.5)*0.8))*0.8);
    diffuseColor.rgb = c;
    pH = groove*0.006 + (1.0-wash)*(-0.0015) + vn(p*120.0)*0.0006;`,
  // Đá lát thủ tục (toàn cảnh s1): viên đá chữ nhật xếp so le theo UV mét.
  setts: (o) => `
    vec2 q = ${o.world ? 'vWP.xz' : 'vUvP'};
    vec2 b = vec2(q.x/${(o.w ?? 0.22).toFixed(3)}, q.y/${(o.l ?? 0.14).toFixed(3)});
    float row = floor(b.y); b.x += h12(vec2(row, 3.1))*0.9;
    vec2 id = floor(b); vec2 f = fract(b);
    float edge = min(min(f.x,1.0-f.x)*${(o.w ?? 0.22).toFixed(3)}, min(f.y,1.0-f.y)*${(o.l ?? 0.14).toFixed(3)});
    float dome = smoothstep(0.0, 0.035, edge);
    float r = h12(id + 7.0);
    vec3 st = diffuseColor.rgb * mix(vec3(0.78,0.80,0.86), vec3(1.12,1.04,0.96), r) * (0.85+0.3*vn(vWP*9.0));
    diffuseColor.rgb = mix(st*0.35, st, smoothstep(0.0, 0.012, edge));
    pH = dome*0.02; pRough = (r-0.5)*0.2 - dome*0.1;`,
  flags: () => `
    vec2 q = vUvP; vec2 b = vec2(q.x/0.62, q.y/0.52);
    float row = floor(b.y); b.x += mod(row,2.0)*0.5;
    vec2 id = floor(b); vec2 f = fract(b);
    float edge = min(min(f.x,1.0-f.x)*0.62, min(f.y,1.0-f.y)*0.52);
    float r = h12(id+3.0);
    diffuseColor.rgb *= (0.8+0.35*r) * (0.85+0.3*fbm(vWP*3.0));
    diffuseColor.rgb *= mix(0.45, 1.0, smoothstep(0.0, 0.01, edge));
    pH = smoothstep(0.0, 0.02, edge)*0.006;`,
  // Ngói/đá phiến xếp lớp (UV: u dọc nóc, v xuống dốc, mét).
  roof: () => `
    vec2 q = vUvP;
    float rowF = q.y/0.17; float row = floor(rowF); float fy = fract(rowF);
    float tx = q.x/0.21 + h12(vec2(row, 5.0))*0.5 + mod(row,2.0)*0.5; float id = floor(tx); float fx = fract(tx);
    float r = h12(vec2(id, row));
    float gap = smoothstep(0.0, 0.06, min(fx, 1.0-fx));
    vec3 c = diffuseColor.rgb * (0.72 + 0.5*r) * (0.8 + 0.4*fbm(vWP*0.7));
    float moss = smoothstep(0.62, 0.72, fbm(vWP*1.3+2.0)) * 0.6;
    c = mix(c, vec3(0.13,0.14,0.09), moss*0.5);
    c *= mix(0.55, 1.0, gap) * (0.75 + 0.25*fy);
    diffuseColor.rgb = c;
    pH = fy*0.022 + gap*0.004; pRough = (r-0.5)*0.25;`,
  // Mặt tiền nhà (s1): vữa sơn hoặc gạch, cửa sổ kính bóng (phản chiếu trời qua IBL), một số ô đèn ấm.
  // vUvP = (u dọc tường, v cao trên nền) mét; vAux = (seed, rộng, số tầng, 1 = mặt có cửa sổ).
  facade: () => `
    vec2 q = vUvP; float seed = vAux.x, wid = vAux.y, nst = vAux.z, front = vAux.w;
    vec3 p = vWP;
    float isBrick = step(h12(vec2(seed, 9.0)), 0.3);
    float m = fbm(p*vec3(0.9,1.3,0.9));
    vec3 c = diffuseColor.rgb * (0.86 + 0.22*m);
    // gạch
    { vec2 b = vec2(q.x/0.23, q.y/0.077); float row = floor(b.y); b.x += mod(row,2.0)*0.5; vec2 id = floor(b); vec2 f = fract(b);
      float e = min(min(f.x,1.0-f.x)*0.23, min(f.y,1.0-f.y)*0.077);
      vec3 br = c * mix(0.8, 1.15, h12(id)); br = mix(c*0.7, br, smoothstep(0.004,0.01,e));
      c = mix(c, br, isBrick); pH += isBrick*smoothstep(0.004,0.01,e)*0.004; }
    float SH = 3.1;
    float row = floor(q.y/SH); float fy = q.y - row*SH;
    float ncol = max(1.0, floor(wid/2.2)); float colW = wid/ncol;
    float cx = floor(q.x/colW); float fx = q.x - (cx+0.5)*colW;
    float ww = 0.62 + 0.22*h12(vec2(seed, 1.0)); float wh = 1.35 + 0.25*h12(vec2(seed,2.0));
    float y0 = row < 0.5 ? 0.85 : 0.75;
    float wx = abs(fx) - ww*0.5; float wy = abs(fy - (y0+wh*0.5)) - wh*0.5;
    float inRow = step(row, nst-1.0) * step(0.0, q.y) * front * step(0.25, q.x) * step(q.x, wid-0.25);
    float isDoor = (row < 0.5 && cx == floor(h12(vec2(seed,4.0))*ncol)) ? 1.0 : 0.0;
    if (isDoor > 0.5) { wx = abs(fx) - 0.5; wy = abs(fy - 1.1) - 1.1; }
    float d = max(wx, wy);
    // cửa tối: bệ cửa sổ, ô kính, song cửa
    float frame = step(d, 0.0) * inRow;
    float glass = step(d, -0.065) * inRow;
    float sill = inRow * (1.0 - isDoor) * step(abs(fx), ww*0.5+0.1) * step(abs(fy - (y0 - 0.05)), 0.06);
    float mull = step(abs(fx), 0.025) + step(abs(fy - (y0 + wh*0.62)), 0.022);
    float lit = step(h12(vec2(seed*7.1 + cx, row + 3.3)), ${'LITFRAC'}) * (1.0 - isDoor);
    float strC = step(abs(fy - 0.02), 0.1) * step(0.5, row) * step(row, nst-0.5);  // gờ tầng
    c = mix(c, c*1.18 + 0.02, strC*0.8);
    c = mix(c, c*1.25 + 0.03, sill);
    vec3 fc = isDoor > 0.5 ? vec3(0.09,0.06,0.05) : vec3(0.30,0.28,0.25);
    c = mix(c, fc, frame*(1.0-glass));
    float cur = smoothstep(0.0, 1.0, abs(fx)/(ww*0.5));
    vec3 gl = isDoor > 0.5 ? vec3(0.06,0.04,0.035) : mix(vec3(0.018,0.02,0.026), vec3(0.03), 0.0);
    c = mix(c, gl, glass);
    float mm = glass * (1.0-isDoor) * clamp(mull, 0.0, 1.0);
    c = mix(c, fc, mm);
    pRough = glass*(1.0-isDoor)*(1.0-mm)*(-0.85);
    pEmit = glass*(1.0-mm)*lit * mix(vec3(1.0,0.55,0.22), vec3(0.75,0.38,0.14), cur) * (0.8+0.5*h12(vec2(seed,row))) * ${'WINEMIT'};
    pH += -0.05*frame + 0.03*sill;
    // AO giả: chân tường tối hơn, dưới mái hơi tối
    c *= 0.62 + 0.38*smoothstep(-0.2, 5.0, q.y);
    c *= 1.0 - 0.25*smoothstep(nst*SH - 0.6, nst*SH, q.y);
    diffuseColor.rgb = c;`,
  // Gỗ sơn (thang, cửa).
  wood: () => `
    vec3 p = vWP; float g = vn(vec3(p.x*8.0, p.y*80.0, p.z*8.0));
    diffuseColor.rgb *= 0.8 + 0.35*g; pH = g*0.0006;`,
  // Sắt đúc sơn đen (cột đèn): sơn dày, hơi sần.
  iron: () => `
    float n = fbm(vWP*30.0); diffuseColor.rgb *= 0.8 + 0.4*n; pH = vn(vWP*200.0)*0.0004; pRough = (0.5-n)*0.2;`,
  // Đá (viên lát, đá vòm): lốm đốm hạt, sần.
  stone: (o) => `
    float n = fbm(vWP*${(o.sc ?? 9).toFixed(1)}); float f = vn(vWP*110.0); float g = vn(vWP*37.0);
    diffuseColor.rgb *= (0.74 + 0.42*n) * (0.92 + 0.16*f);
    pH = f*0.0012 + g*0.0018 + n*0.002; pRough = (0.5-n)*0.25;`,
  plain: () => ``,
};

// Tạo vật liệu thủ tục. kind ∈ KIND; o: {color, rough, metal, sheen, sheenColor, sheenRough, env, emissive, emissiveIntensity, vc (vertex colors), side, aux, ...tham số kind}
let _uid = 0; export const LIBCFG = { plain: false };
export function procMat(kind, o = {}) {
  const phys = o.sheen != null || o.physical;
  const M = phys ? THREE.MeshPhysicalMaterial : THREE.MeshStandardMaterial;
  const m = new M({ color: o.color ?? '#ffffff', roughness: o.rough ?? 0.85, metalness: o.metal ?? 0, vertexColors: !!o.vc, side: o.side ?? THREE.FrontSide,
    transparent: !!o.transparent, opacity: o.opacity ?? 1, depthWrite: o.depthWrite ?? true });
  if (phys && o.sheen != null) { m.sheen = o.sheen; m.sheenColor = new THREE.Color(o.sheenColor ?? '#ffffff'); m.sheenRoughness = o.sheenRough ?? 0.6; }
  if (o.emissive) { m.emissive = new THREE.Color(o.emissive); m.emissiveIntensity = o.emissiveIntensity ?? 1; }
  m.envMapIntensity = o.env ?? 1;
  if (o.envMap) m.envMap = o.envMap;
  let code = LIBCFG.plain ? '' : (KIND[kind] || KIND.plain)(o);
  code = code.replace('LITFRAC', (o.litFrac ?? 0.12).toFixed(3)).replace('WINEMIT', (o.winEmit ?? 1).toFixed(3));
  const key = kind + '|' + (_uid++);
  m.customProgramCacheKey = () => key;
  m.onBeforeCompile = (sh) => {
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', `#include <common>\nvarying vec3 vWP; varying vec3 vWN; varying vec2 vUvP; varying vec4 vAux;\n${o.aux ? 'attribute vec4 aAux;' : ''}`)
      .replace('#include <project_vertex>', `#include <project_vertex>
        { vec4 _p = vec4(transformed, 1.0); vec4 _n = vec4(objectNormal, 0.0);
          #ifdef USE_INSTANCING
          _p = instanceMatrix * _p; _n = instanceMatrix * _n;
          #endif
          vWP = (modelMatrix * _p).xyz; vWN = (modelMatrix * _n).xyz; vUvP = uv; vAux = ${o.aux ? 'aAux' : 'vec4(0.0)'}; }`);
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\n' + COMMON)
      .replace('#include <color_fragment>', `#include <color_fragment>\n{ ${code} }`)
      .replace('#include <roughnessmap_fragment>', '#include <roughnessmap_fragment>\nroughnessFactor = clamp(roughnessFactor + pRough, 0.04, 1.0);')
      .replace('#include <metalnessmap_fragment>', '#include <metalnessmap_fragment>\nif (pMetal >= 0.0) metalnessFactor = pMetal;')
      .replace('#include <normal_fragment_maps>', `#include <normal_fragment_maps>\nnormal = pBump(-vViewPosition, normal, pH * ${(o.bump ?? 1).toFixed(3)}, faceDirection);`)
      .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\ntotalEmissiveRadiance += pEmit;');
  };
  return m;
}

// Vật liệu nhân vật "búp bê dạ": theo vai trò trong cast.js.
export function feltCharacterMaterial(opts = {}) {
  const env = opts.env ?? 0.35, envMap = opts.envMap;
  const lighten = (hex, k) => { const c = new THREE.Color(hex); const hsl = {}; c.getHSL(hsl); c.setHSL(hsl.h, hsl.s * 0.55, Math.min(1, hsl.l + k)); return '#' + c.getHexString(); };
  return (role, color, part) => {
    const base = { color, env, envMap };
    switch (role) {
      case 'coat': case 'lining': case 'trousers': case 'hat': {
        const o = { ...base, rough: 0.95, sheen: 1.0, sheenColor: lighten(color, 0.28), sheenRough: 0.55, mot: role === 'hat' ? 11 : 7 };
        if (part && part.startsWith('coat_')) { o.stitchV = 0.955; o.stitchN = 70; o.stitchW = 0.007; }
        if (part === 'torso' && role === 'coat') { o.stitchV = 0.92; o.stitchN = 90; o.stitchW = 0.006; }
        if (part === 'collar') { o.stitchV = 0.8; o.stitchN = 50; o.stitchW = 0.04; }
        if (role === 'hat') { o.sheenRough = 0.45; }
        return procMat('felt', o);
      }
      case 'skin': return procMat('felt', { ...base, rough: 0.9, sheen: 0.8, sheenColor: lighten(color, 0.18), sheenRough: 0.6, mot: 5 });
      case 'eyes': return procMat('wool', { ...base, rough: 0.95, fx: 300, fy: 300, env: 0.1 }); // chỉ thêu, không bóng (không phải mắt nút)
      case 'hair': return procMat('wool', { ...base, rough: 0.9, sheen: 1.0, sheenColor: lighten(color, 0.2), sheenRough: 0.5, fx: 140, fy: 22 });
      case 'sweater': {
        const n = { torso: [64, 40], collar: [90, 10], upper_arm: [22, 38], upper_arm_joint: [22, 10], forearm: [20, 34], forearm_joint: [20, 10], sleeve_cuff: [20, 8] }[part] || [40, 30];
        return procMat('knit', { ...base, rough: 0.95, sheen: 1.0, sheenColor: lighten(color, 0.25), sheenRough: 0.5, n: n[0], m: n[1] });
      }
      case 'cap': return procMat('knit', { ...base, rough: 0.95, sheen: 1.0, sheenColor: lighten(color, 0.15), sheenRough: 0.5, n: 90, m: part === 'cap' ? 30 : 30 });
      case 'bobble': return procMat('wool', { ...base, rough: 1.0, sheen: 1.0, sheenColor: lighten(color, 0.3), sheenRough: 0.35, fx: 260, fy: 260 });
      case 'boots': return procMat('leather', { ...base, rough: 0.55, env: env * 1.5 });
      case 'ladder': return procMat('wood', { ...base, rough: 0.7 });
      case 'tin': return procMat('tin', { ...base, color: '#9a958a', rough: 0.38, metal: 0.85, env: 1.0 });
      case 'glass': return procMat('plain', { ...base, color: '#ffc56b', rough: 0.1, emissive: '#ffb45a', emissiveIntensity: opts.glassGlow ?? 0.5, transparent: true, opacity: 0.55, depthWrite: false });
      case 'flame': return procMat('plain', { ...base, color: '#fff0c8', emissive: '#ffd89a', emissiveIntensity: opts.flameGlow ?? 6 });
      default: return procMat('felt', { ...base, rough: 0.9, sheen: 0.8, sheenColor: lighten(color, 0.2) });
    }
  };
}

// Gắn vết hàn thiếc (hạt tròn nhỏ) vào đèn lồng dựng từ buildLantern: dọc 4 trụ và mép nắp/đế.
export function addSolder(lantern, mat, h) {
  const w = h * 0.58, g = new THREE.SphereGeometry(h * 0.024, 8, 6);
  for (const [x, z] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) {
    for (const y of [0.11, 0.14, 0.68, 0.71]) { const s = new THREE.Mesh(g, mat); s.position.set(x * w / 2, h * y, z * w / 2); s.scale.set(1, 0.6 + 0.3 * Math.abs(Math.sin(x * 3 + y * 17 + z)), 1); lantern.add(s); }
  }
  // gờ viền đế và nắp (dải thiếc gấp mép)
  const rimG = new THREE.TorusGeometry(w * 0.66, h * 0.012, 4, 4); rimG.rotateX(Math.PI / 2); rimG.rotateY(Math.PI / 4);
  const r1 = new THREE.Mesh(rimG, mat); r1.position.y = h * 0.1; lantern.add(r1);
  const r2 = new THREE.Mesh(rimG, mat); r2.position.y = h * 0.71; r2.scale.setScalar(1.12); lantern.add(r2);
  return lantern;
}

// Tổ hợp hình học: gộp danh sách [geometry, matrix, {color, aux}] thành 1 BufferGeometry không chỉ số.
export function mergeInto(list, { color = false, aux = false } = {}) {
  let n = 0; const gs = [];
  for (const it of list) { const g = it.g.index ? it.g.toNonIndexed() : it.g; gs.push([g, it]); n += g.attributes.position.count; }
  const P = new Float32Array(n * 3), N = new Float32Array(n * 3), U = new Float32Array(n * 2), C = color ? new Float32Array(n * 3) : null, A = aux ? new Float32Array(n * 4) : null;
  let o = 0; const v = new THREE.Vector3(), nm = new THREE.Matrix3(), col = new THREE.Color();
  for (const [g, it] of gs) {
    const m = it.m || new THREE.Matrix4(); nm.getNormalMatrix(m);
    const p = g.attributes.position, no = g.attributes.normal, uv = g.attributes.uv;
    if (color) col.set(it.color ?? '#ffffff').convertSRGBToLinear();
    for (let i = 0; i < p.count; i++, o++) {
      v.fromBufferAttribute(p, i).applyMatrix4(m); P.set([v.x, v.y, v.z], o * 3);
      v.fromBufferAttribute(no, i).applyMatrix3(nm).normalize(); N.set([v.x, v.y, v.z], o * 3);
      if (uv) U.set([uv.getX(i), uv.getY(i)], o * 2);
      if (C) C.set([col.r, col.g, col.b], o * 3);
      if (A) A.set(it.aux || [0, 0, 0, 0], o * 4);
    }
  }
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(P, 3)); out.setAttribute('normal', new THREE.BufferAttribute(N, 3)); out.setAttribute('uv', new THREE.BufferAttribute(U, 2));
  if (C) out.setAttribute('color', new THREE.BufferAttribute(C, 3));
  if (A) out.setAttribute('aAux', new THREE.BufferAttribute(A, 4));
  return out;
}

// UV mét theo trục trội của pháp tuyến (cho hộp mặt tiền): u dọc mặt, v = y.
export function metricUV(g, w, d) {
  const p = g.attributes.position, n = g.attributes.normal, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), nx = n.getX(i), nz = n.getZ(i);
    let u; if (Math.abs(nz) >= Math.abs(nx)) u = nz > 0 ? x + w / 2 : w / 2 - x; else u = nx > 0 ? d / 2 - z : z + d / 2;
    uv.setXY(i, u, y);
  }
  return g;
}

// Chuỗi ít sai lệch
export const halton = (i, b) => { let f = 1, r = 0; i += 1; while (i > 0) { f /= b; r += f * (i % b); i = Math.floor(i / b); } return r; };
export function mulberry(seed) { let a = seed >>> 0; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

// Hào quang ống kính quanh nguồn sáng nhỏ (halation) — sprite cộng, mờ theo sương.
let _haloTex = null;
export function haloSprite(color, size, opacity = 1) {
  if (!_haloTex) {
    const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d');
    const g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.12, 'rgba(255,255,255,0.5)'); g.addColorStop(0.35, 'rgba(255,255,255,0.16)'); g.addColorStop(0.7, 'rgba(255,255,255,0.04)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, 128, 128); _haloTex = new THREE.CanvasTexture(c);
  }
  const m = new THREE.SpriteMaterial({ map: _haloTex, color, transparent: true, opacity, blending: THREE.AdditiveBlending, depthWrite: false });
  const s = new THREE.Sprite(m); s.scale.set(size, size, 1); return s;
}

// Nhiều hào quang trong 1 draw call (Points cộng sáng, cỡ theo mét thế giới).
export function haloPoints(list, size) { // list: [{p: Vector3, c: Color}]
  haloSprite(new THREE.Color(1, 1, 1), 1); // bảo đảm texture
  const P = new Float32Array(list.length * 3), C = new Float32Array(list.length * 3);
  list.forEach((it, i) => { P.set([it.p.x, it.p.y, it.p.z], i * 3); C.set([it.c.r, it.c.g, it.c.b], i * 3); });
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('color', new THREE.BufferAttribute(C, 3));
  const m = new THREE.PointsMaterial({ size, map: _haloTex, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true });
  const pts = new THREE.Points(g, m); pts.frustumCulled = false; return pts;
}

// Máy quay có DOF thật: đặt vị trí gốc + điểm nhìn + khoảng lấy nét; jitterAperture(i,n) dời tâm chiếu trên đĩa khẩu độ (Vogel)
// và xoay lại nhìn đúng điểm nét (toe-in, sai số không đáng kể với khẩu nhỏ).
export function dofCamera(cam, pos, target, focusDist, apertureR) {
  const fwd = new THREE.Vector3().subVectors(target, pos).normalize();
  const right = new THREE.Vector3().crossVectors(fwd, new THREE.Vector3(0, 1, 0)).normalize();
  const up = new THREE.Vector3().crossVectors(right, fwd).normalize();
  const focus = pos.clone().addScaledVector(fwd, focusDist);
  return {
    focus, apertureR,
    jitter(i, n) {
      const r = apertureR * Math.sqrt((i + 0.5) / n), th = i * 2.399963 + 0.7;
      cam.position.copy(pos).addScaledVector(right, r * Math.cos(th)).addScaledVector(up, r * Math.sin(th));
      cam.lookAt(focus); cam.updateMatrixWorld();
    },
    reset() { cam.position.copy(pos); cam.lookAt(focus); cam.updateMatrixWorld(); },
  };
}

// Gộp mọi mesh tĩnh của một nhân vật (đã đặt tư thế) theo vật liệu → vài draw call thay vì hàng trăm (SwiftShader tốn theo draw call).
// Chỉ gộp hình học đã biến đổi sang toạ độ thế giới; tỷ lệ bộ phận giữ nguyên tuyệt đối.
export function bakeStatic(root, scene, { castShadow = true, exclude = () => false } = {}) {
  root.updateMatrixWorld(true);
  const groups = new Map(); const hide = [];
  root.traverse((o) => { if (!o.isMesh || !o.visible || exclude(o)) return; let p = o.parent, vis = true; while (p) { if (!p.visible) vis = false; p = p.parent; } if (!vis) return;
    const k = o.material.uuid; if (!groups.has(k)) groups.set(k, { mat: o.material, list: [], cs: false }); const gr = groups.get(k);
    gr.list.push({ g: o.geometry, m: o.matrixWorld.clone() }); gr.cs = gr.cs || o.castShadow; hide.push(o); });
  const out = new THREE.Group();
  for (const { mat, list, cs } of groups.values()) { const m = new THREE.Mesh(mergeInto(list), mat); m.castShadow = castShadow && cs; m.receiveShadow = true; out.add(m); }
  for (const o of hide) o.visible = false;
  scene.add(out); return out;
}

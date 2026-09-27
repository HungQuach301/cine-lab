// Cine Lab · Cổng 3 v2 · cách (1) — công cụ điêu khắc bằng trường khoảng cách (SDF) và da CPU.
// sculpt(): lưới "hình sao" quanh một tâm: mỗi đỉnh của lưới cầu UV được bắn tia từ ngoài vào tới mặt SDF (sphere tracing),
//   pháp tuyến lấy từ gradient SDF (liền mạch, không đường nối), UV giữ nguyên của lưới cầu → dùng được map/normalMap.
// patch(): như sculpt nhưng chỉ một mảng (φ, θ) có biên do hàm quy định (tóc, mảng tóc gáy).
// CpuSkin: da tuyến tính (LBS) tính trên CPU mỗi lần đặt tư thế → mesh thường (không SkinnedMesh) nên mọi pass phụ
//   (G-buffer lớp vẽ, bóng đổ) thấy đúng hình đã uốn.
import * as THREE from '../../shared/node_modules/three/build/three.module.js';

// ---------- nguyên thuỷ SDF (đơn vị tuỳ ý, thường là H) ----------
export const len3 = (x, y, z) => Math.sqrt(x * x + y * y + z * z);
export const sph = (x, y, z, c, r) => len3(x - c[0], y - c[1], z - c[2]) - r;
export function ell(x, y, z, c, r) { // xấp xỉ elipxoit (Quilez)
  const px = (x - c[0]) / r[0], py = (y - c[1]) / r[1], pz = (z - c[2]) / r[2];
  const k0 = len3(px, py, pz), k1 = len3(px / r[0], py / r[1], pz / r[2]);
  return k1 < 1e-9 ? -Math.min(r[0], r[1], r[2]) : k0 * (k0 - 1) / k1;
}
// Nón tròn đầu (xấp xỉ): đoạn a→b, bán kính ra→rb nội suy.
export function cap(x, y, z, a, b, ra, rb = ra) {
  const bx = b[0] - a[0], by = b[1] - a[1], bz = b[2] - a[2], px = x - a[0], py = y - a[1], pz = z - a[2];
  const h = Math.max(0, Math.min(1, (px * bx + py * by + pz * bz) / (bx * bx + by * by + bz * bz)));
  return len3(px - bx * h, py - by * h, pz - bz * h) - (ra + (rb - ra) * h);
}
// Khoảng cách tới đoạn (không trừ bán kính) + tham số h.
export function segD(x, y, z, a, b) {
  const bx = b[0] - a[0], by = b[1] - a[1], bz = b[2] - a[2], px = x - a[0], py = y - a[1], pz = z - a[2];
  const h = Math.max(0, Math.min(1, (px * bx + py * by + pz * bz) / (bx * bx + by * by + bz * bz)));
  return len3(px - bx * h, py - by * h, pz - bz * h);
}
// Hộp bo tròn.
export function rbox(x, y, z, c, hsz, r) {
  const qx = Math.abs(x - c[0]) - hsz[0] + r, qy = Math.abs(y - c[1]) - hsz[1] + r, qz = Math.abs(z - c[2]) - hsz[2] + r;
  return len3(Math.max(qx, 0), Math.max(qy, 0), Math.max(qz, 0)) + Math.min(Math.max(qx, qy, qz), 0) - r;
}
export function smin(a, b, k) { const h = Math.max(k - Math.abs(a - b), 0) / k; return Math.min(a, b) - h * h * k * 0.25; }
export const smax = (a, b, k) => -smin(-a, -b, k);
export const gauss = (d, w) => Math.exp(-(d * d) / (w * w));
export const sstep = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
// Rãnh (nếp nhăn): trả lượng lõm (dương) theo khoảng cách tới đường gấp khúc pts.
export function groove(x, y, z, pts, w, depth) {
  let d = 1e9; for (let i = 0; i < pts.length - 1; i++) d = Math.min(d, segD(x, y, z, pts[i], pts[i + 1]));
  return depth * gauss(d, w);
}

// ---------- nhiễu giá trị 3D (có hạt giống, tất định) ----------
function hash3(i, j, k, s) { let h = (i * 374761393 + j * 668265263 + k * 2147483647 + s * 1274126177) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); h ^= h >>> 16; return (h & 0xffff) / 65535; }
export function vnoise(x, y, z, s = 0) {
  const i = Math.floor(x), j = Math.floor(y), k = Math.floor(z); let fx = x - i, fy = y - j, fz = z - k;
  fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy); fz = fz * fz * (3 - 2 * fz);
  const L = (a, b, t) => a + (b - a) * t;
  return L(L(L(hash3(i, j, k, s), hash3(i + 1, j, k, s), fx), L(hash3(i, j + 1, k, s), hash3(i + 1, j + 1, k, s), fx), fy),
    L(L(hash3(i, j, k + 1, s), hash3(i + 1, j, k + 1, s), fx), L(hash3(i, j + 1, k + 1, s), hash3(i + 1, j + 1, k + 1, s), fx), fy), fz) * 2 - 1;
}
export function fbm(x, y, z, oct = 3, s = 0) { let a = 0.5, f = 1, t = 0; for (let o = 0; o < oct; o++) { t += a * vnoise(x * f, y * f, z * f, s + o); a *= 0.5; f *= 2.03; } return t; }

// ---------- tìm mặt dọc tia (từ ngoài vào) ----------
function trace(sdf, cx, cy, cz, dx, dy, dz, t0, eps) {
  let t = t0, s = 0, tOut = t0;
  for (let it = 0; it < 120; it++) {
    s = sdf(cx + dx * t, cy + dy * t, cz + dz * t);
    if (s >= 0) { tOut = t; if (s < eps) return t; t -= Math.max(s * 0.8, eps * 0.5); if (t < 0) return 0; }
    else { // vượt qua mặt: chia đôi giữa tOut (ngoài) và t (trong)
      let a = t, b = tOut; for (let k = 0; k < 24; k++) { const m = 0.5 * (a + b); if (sdf(cx + dx * m, cy + dy * m, cz + dz * m) < 0) a = m; else b = m; }
      return 0.5 * (a + b);
    }
  }
  return t;
}
function gradN(sdf, x, y, z, e) {
  const nx = sdf(x + e, y, z) - sdf(x - e, y, z), ny = sdf(x, y + e, z) - sdf(x, y - e, z), nz = sdf(x, y, z + e) - sdf(x, y, z - e);
  const l = len3(nx, ny, nz) || 1; return [nx / l, ny / l, nz / l];
}

// Lưới hình sao. dirs: trục cực = y, φ = 0 hướng +z (mặt), đường nối ở −z (sau gáy/lưng).
// o = { c:[cx,cy,cz], r:[rx,ry,rz] (elip bao để khởi đầu tia), nu, nv, scale (nhân toạ độ), uv:[su,sv], color:(x,y,z,n)=>[r,g,b], eps }
export function sculpt(sdf, o) {
  const [cx, cy, cz] = o.c, [rx, ry, rz] = o.r, nu = o.nu, nv = o.nv, sc = o.scale ?? 1, eps = o.eps ?? 1e-4;
  const th0 = o.th0 ?? 0, th1 = o.th1 ?? Math.PI;
  const n = (nu + 1) * (nv + 1), pos = new Float32Array(n * 3), nor = new Float32Array(n * 3), uv = new Float32Array(n * 2);
  const col = o.color ? new Float32Array(n * 3) : null; const e = o.gradE ?? 0.004;
  let k = 0;
  for (let j = 0; j <= nv; j++) {
    const vv = j / nv, vw = o.warp ? vv + o.warp[1] * Math.sin(2 * Math.PI * vv) / (2 * Math.PI) : vv;   // warp: dày lưới ở xích đạo (mặt)
    const th = th0 + (th1 - th0) * vw, st = Math.sin(th), ct = Math.cos(th);
    for (let i = 0; i <= nu; i++, k++) {
      const tt = 2 * i / nu - 1, ph = o.warp ? Math.PI * (o.warp[0] * tt + (1 - o.warp[0]) * tt * tt * tt) : -Math.PI + 2 * Math.PI * i / nu;   // dày lưới ở φ=0 (trước)
      const dx = st * Math.sin(ph), dy = ct, dz = st * Math.cos(ph); // i=0 → −z (đường nối sau)
      const re = 1 / Math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2 + (dz / rz) ** 2);
      const t = trace(sdf, cx, cy, cz, dx, dy, dz, re * 1.35, eps);
      const x = cx + dx * t, y = cy + dy * t, z = cz + dz * t;
      const nn = gradN(sdf, x, y, z, e);
      pos[k * 3] = x * sc; pos[k * 3 + 1] = y * sc; pos[k * 3 + 2] = z * sc;
      nor.set(nn, k * 3);
      uv[k * 2] = i / nu * (o.uv?.[0] ?? 1); uv[k * 2 + 1] = (1 - j / nv) * (o.uv?.[1] ?? 1);
      if (col) col.set(o.color(x, y, z, nn), k * 3);
    }
  }
  return gridGeo(pos, nor, uv, col, nu, nv);
}

// Mảng (patch): u∈[0,1] → φ = phA..phB, v∈[0,1] → θ = th(u)·v (từ cực trên xuống biên). Dùng cho tóc.
export function patch(sdf, o) {
  const [cx, cy, cz] = o.c, nu = o.nu, nv = o.nv, sc = o.scale ?? 1;
  const n = (nu + 1) * (nv + 1), pos = new Float32Array(n * 3), nor = new Float32Array(n * 3), uv = new Float32Array(n * 2);
  const col = o.color ? new Float32Array(n * 3) : null; const e = o.gradE ?? 0.004;
  let k = 0;
  for (let j = 0; j <= nv; j++) for (let i = 0; i <= nu; i++, k++) {
    const u = i / nu, v = j / nv, ph = o.phA + (o.phB - o.phA) * u, th = o.th(u, ph) * v;
    const st = Math.sin(th), dx = st * Math.sin(ph), dy = Math.cos(th), dz = st * Math.cos(ph);
    const t = trace(sdf, cx, cy, cz, dx, dy, dz, o.t0, 1e-4);
    const x = cx + dx * t, y = cy + dy * t, z = cz + dz * t, nn = gradN(sdf, x, y, z, e);
    pos[k * 3] = x * sc; pos[k * 3 + 1] = y * sc; pos[k * 3 + 2] = z * sc; nor.set(nn, k * 3);
    uv[k * 2] = u * (o.uv?.[0] ?? 1); uv[k * 2 + 1] = v * (o.uv?.[1] ?? 1);
    if (col) col.set(o.color(x, y, z, nn, u, v), k * 3);
  }
  return gridGeo(pos, nor, uv, col, nu, nv);
}

export function gridGeo(pos, nor, uv, col, nu, nv) {
  const idx = [];
  for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) {
    const a = j * (nu + 1) + i, b = a + nu + 1;
    idx.push(a, b, a + 1, b, b + 1, a + 1);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  if (nor) g.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  if (col) g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.setIndex(idx);
  if (!nor) g.computeVertexNormals();
  return g;
}

// Ống dọc trục −y theo profile: rings(s) → {r(φ), ...}. Trả geometry có thêm thuộc tính 's' (0..1 dọc chiều dài) để gán trọng số da.
// o = { y0, y1 (y1 < y0), nu, nv, rad:(s, φ) => [rx, rz, dx, dz] (bán kính theo x, z và dịch tâm), color, uv, cap0, cap1 }
export function tube(o) {
  const { y0, y1, nu, nv } = o; const n = (nu + 1) * (nv + 1);
  const pos = new Float32Array(n * 3), uv = new Float32Array(n * 2), S = new Float32Array(n), col = o.color ? new Float32Array(n * 3) : null;
  let k = 0;
  for (let j = 0; j <= nv; j++) {
    const s = j / nv, y = y0 + (y1 - y0) * s;
    for (let i = 0; i <= nu; i++, k++) {
      const ph = 2 * Math.PI * i / nu; // φ=0 → +z
      const [r, dx = 0, dz = 0, dy = 0] = o.rad(s, ph, y);
      const x = Math.sin(ph) * r + dx, z = Math.cos(ph) * r + dz;
      pos[k * 3] = x; pos[k * 3 + 1] = y + dy; pos[k * 3 + 2] = z; S[k] = s;
      uv[k * 2] = i / nu * (o.uv?.[0] ?? 1); uv[k * 2 + 1] = s * (o.uv?.[1] ?? 1);
      if (col) col.set(o.color(s, ph, x, y, z), k * 3);
    }
  }
  const g = gridGeo(pos, null, uv, col, nu, nv);
  g.computeVertexNormals(); fixSeamNormals(g, nu, nv);
  g.setAttribute('s', new THREE.BufferAttribute(S, 1));
  return g;
}
// Cộng pháp tuyến hai cột đường nối (i=0 và i=nu) để không lộ vệt.
export function fixSeamNormals(g, nu, nv) {
  const N = g.attributes.normal;
  for (let j = 0; j <= nv; j++) {
    const a = j * (nu + 1), b = a + nu;
    const x = N.getX(a) + N.getX(b), y = N.getY(a) + N.getY(b), z = N.getZ(a) + N.getZ(b), l = len3(x, y, z) || 1;
    N.setXYZ(a, x / l, y / l, z / l); N.setXYZ(b, x / l, y / l, z / l);
  }
}

// ---------- da CPU ----------
// Mỗi mesh da là con trực tiếp của root (ma trận đơn vị). Toạ độ nghỉ = hệ root lúc mọi khớp quay 0.
export class CpuSkin {
  constructor(root) { this.root = root; this.items = []; this.bones = []; this.bind = []; this._inv = new THREE.Matrix4(); this._m = []; }
  bone(obj) { let i = this.bones.indexOf(obj); if (i < 0) { i = this.bones.length; this.bones.push(obj); this.bind.push(null); } return i; }
  // Gọi khi khung xương đang ở tư thế nghỉ (mọi khớp 0) để ghi ma trận bind.
  captureBind() {
    this.root.updateMatrixWorld(true); const inv = new THREE.Matrix4().copy(this.root.matrixWorld).invert();
    this.bind = this.bones.map((b) => new THREE.Matrix4().multiplyMatrices(inv, b.matrixWorld).invert());
  }
  // geo: toạ độ trong hệ root nghỉ; weights: Array per vertex [[boneIdx, w], ...].
  add(mesh, weights) {
    const g = mesh.geometry, P = g.attributes.position, N = g.attributes.normal;
    const it = { mesh, P0: Float32Array.from(P.array), N0: Float32Array.from(N.array), W: weights };
    mesh.frustumCulled = false; this.items.push(it); return it;
  }
  update() {
    this.root.updateMatrixWorld(true); this._inv.copy(this.root.matrixWorld).invert();
    const M = this.bones.map((b, i) => new THREE.Matrix4().multiplyMatrices(this._inv, b.matrixWorld).multiply(this.bind[i]).elements);
    for (const it of this.items) {
      const P = it.mesh.geometry.attributes.position, N = it.mesh.geometry.attributes.normal, pa = P.array, na = N.array, P0 = it.P0, N0 = it.N0;
      for (let v = 0, n = P.count; v < n; v++) {
        const x = P0[v * 3], y = P0[v * 3 + 1], z = P0[v * 3 + 2], nx = N0[v * 3], ny = N0[v * 3 + 1], nz = N0[v * 3 + 2];
        let ox = 0, oy = 0, oz = 0, qx = 0, qy = 0, qz = 0;
        for (const [bi, w] of it.W[v]) {
          const e = M[bi];
          ox += w * (e[0] * x + e[4] * y + e[8] * z + e[12]); oy += w * (e[1] * x + e[5] * y + e[9] * z + e[13]); oz += w * (e[2] * x + e[6] * y + e[10] * z + e[14]);
          qx += w * (e[0] * nx + e[4] * ny + e[8] * nz); qy += w * (e[1] * nx + e[5] * ny + e[9] * nz); qz += w * (e[2] * nx + e[6] * ny + e[10] * nz);
        }
        pa[v * 3] = ox; pa[v * 3 + 1] = oy; pa[v * 3 + 2] = oz;
        const l = len3(qx, qy, qz) || 1; na[v * 3] = qx / l; na[v * 3 + 1] = qy / l; na[v * 3 + 2] = qz / l;
      }
      P.needsUpdate = true; N.needsUpdate = true;
    }
  }
}

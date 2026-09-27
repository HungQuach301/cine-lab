// Cine Lab · Cổng 3 v2 · Cách (2) — bộ vẽ tranh 2D sinh bằng mã cho nhân vật (không tải tài sản ngoài).
// Hai loại "tranh":
//  (a) Tranh theo góc nhìn (đầu, thân): khối dựng bằng các elip (có mặt phẳng cắt) → "phác khối" bằng một bộ rasterize trực giao
//      trên CPU cho ĐÚNG góc nhìn cần vẽ (bản đồ độ cao = mặt trước của khối, hợp mềm các elip cùng nhóm). Màu = trường màu
//      theo vị trí 3D trên khối (vùng màu kiểu họa sĩ: trán vàng, má–mũi–tai đỏ, hàm lạnh; nét cọ là nhiễu kéo dài neo vào khối
//      nên không "trôi" khi đổi góc) + bóng hốc vẽ tay (từ độ cao) + NÉT VẼ (mắt, mày, nếp nhăn, môi…) vẽ bằng canvas 2D qua
//      phép chiếu affine của khung tiếp tuyến tại điểm neo → nét tự co theo góc quay, và bị khối che đúng (kiểm độ sâu từng điểm ảnh).
//  (b) Tranh dải (tay, chân, ngón, vạt áo…): vẽ trong không gian (u ngang, v dọc) của dải; độ cao = mặt cắt tròn + nổi nếp vải.
// Mỗi tranh cho: map (sRGB, alpha = rìa mềm) + normalMap (suy từ độ cao; kênh alpha = độ nhô để ghi độ sâu từng điểm ảnh).
import * as THREE from '../../shared/node_modules/three/build/three.module.js';

export function rng(seed) { let a = seed >>> 0; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

// ---------- nhiễu giá trị 2D/3D (có hạt giống cố định) ----------
const PERM = new Uint8Array(512);
{ const R = rng(9127); const p = Array.from({ length: 256 }, (_, i) => i); for (let i = 255; i > 0; i--) { const j = Math.floor(R() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; } for (let i = 0; i < 512; i++) PERM[i] = p[i & 255]; }
const h3 = (i, j, k) => PERM[(PERM[(PERM[i & 255] + j) & 255] + k) & 255] / 255;
const h2 = (i, j) => PERM[(PERM[i & 255] + j) & 255] / 255;
const sm = (t) => t * t * (3 - 2 * t);
export function vn3(x, y, z) {
  const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), u = sm(x - xi), v = sm(y - yi), w = sm(z - zi);
  const a = h3(xi, yi, zi), b = h3(xi + 1, yi, zi), c = h3(xi, yi + 1, zi), d = h3(xi + 1, yi + 1, zi);
  const e = h3(xi, yi, zi + 1), f = h3(xi + 1, yi, zi + 1), g = h3(xi, yi + 1, zi + 1), hh = h3(xi + 1, yi + 1, zi + 1);
  const x0 = a + (b - a) * u, x1 = c + (d - c) * u, x2 = e + (f - e) * u, x3 = g + (hh - g) * u;
  const y0 = x0 + (x1 - x0) * v, y1 = x2 + (x3 - x2) * v; return y0 + (y1 - y0) * w;
}
export function vn2(x, y) {
  const xi = Math.floor(x), yi = Math.floor(y), u = sm(x - xi), v = sm(y - yi);
  const a = h2(xi, yi), b = h2(xi + 1, yi), c = h2(xi, yi + 1), d = h2(xi + 1, yi + 1);
  return a + (b - a) * u + (c + (d - c) * u - a - (b - a) * u) * v;
}
export function fbm3(x, y, z, oct = 3) { let s = 0, a = 0.5, f = 1, n = 0; for (let o = 0; o < oct; o++) { s += a * vn3(x * f, y * f, z * f); n += a; a *= 0.5; f *= 2.03; } return s / n; }
export function fbm2(x, y, oct = 3) { let s = 0, a = 0.5, f = 1, n = 0; for (let o = 0; o < oct; o++) { s += a * vn2(x * f + o * 7.1, y * f); n += a; a *= 0.5; f *= 2.07; } return s / n; }

// ---------- vector nhỏ ----------
export const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
export const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
export const norm = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
export const add = (a, b, k = 1) => [a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k];
export const scl = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
export const mix = (a, b, t) => a + (b - a) * t;
export const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
export const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
export const hex = (h) => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
export const lerp3 = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];

// Hệ cơ sở nhìn: F = hướng tới máy quay (trong hệ cục bộ của khớp), U = trục y cục bộ chiếu lên mặt phẳng nhìn, R = U × F.
export function viewBasis(yaw, pitch) {
  const F = [Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch)];
  const U = norm([-F[0] * F[1], 1 - F[1] * F[1], -F[2] * F[1]]);
  return { R: cross(U, F), U, F, yaw, pitch };
}
function basisFromF(F, upHint = [0, 1, 0]) {
  const d = dot(upHint, F); let U = [upHint[0] - d * F[0], upHint[1] - d * F[1], upHint[2] - d * F[2]];
  if (Math.hypot(...U) < 1e-4) U = [0, 0, 1];
  U = norm(U); return { R: cross(U, F), U, F };
}

// Ma trận quay Euler XYZ (cột = trục cục bộ của elip).
function eulerM(r) {
  if (!r) return [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
  const m = new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(r[0] || 0, r[1] || 0, r[2] || 0, 'XYZ')).elements;
  return [[m[0], m[1], m[2]], [m[4], m[5], m[6]], [m[8], m[9], m[10]]]; // 3 cột (trục x, y, z của elip, trong hệ cục bộ)
}

// ---------- bộ rasterize khối elip ----------
// prim: { c:[x,y,z], r:[a,b,c], rot?:[rx,ry,rz], id, g (nhóm), clip?:[[nx,ny,nz,d]...] (giữ n·p <= d) }
// groups: [{k}] — k > 0: hợp mềm (log-sum-exp, độ mềm 1/k đơn vị); k = 0: hợp cứng.
export function sculpt(prims, groups, V, o) {
  const { W, H, cx, cy, s } = o, N = W * H, ng = groups.length;
  const sum = [], braw = [], bid = [];
  for (let g = 0; g < ng; g++) { sum.push(groups[g].k > 0 ? new Float32Array(N) : null); braw.push(new Float32Array(N).fill(-1e9)); bid.push(new Int16Array(N).fill(-1)); }
  for (const p of prims) {
    const Q = eulerM(p.rot), S = p.r;
    // M = S^-1 Q^T : hàng i = cột i của Q / r_i
    const M = [0, 1, 2].map((i) => scl(Q[i], 1 / S[i]));
    const mv = (v) => [dot(M[0], v), dot(M[1], v), dot(M[2], v)];
    const qx = mv(V.R), qy = mv(V.U), q1 = mv(V.F), qc = scl(mv(p.c), -1);
    const a = dot(q1, q1);
    const clips = (p.clip || []).map(([nx, ny, nz, d]) => { const n = [nx, ny, nz]; return [dot(n, V.R), dot(n, V.U), dot(n, V.F), d]; });
    const pr = dot(p.c, V.R), pu = dot(p.c, V.U), rad = Math.max(S[0], S[1], S[2]) * 1.02;
    const i0 = Math.max(0, Math.floor((pr - rad - cx) * s + W / 2)), i1 = Math.min(W - 1, Math.ceil((pr + rad - cx) * s + W / 2));
    const j0 = Math.max(0, Math.floor((pu - rad - cy) * s + H / 2)), j1 = Math.min(H - 1, Math.ceil((pu + rad - cy) * s + H / 2));
    const g = p.g || 0, k = groups[g].k, SG = sum[g], BR = braw[g], BI = bid[g];
    for (let j = j0; j <= j1; j++) {
      const y = cy + (j + 0.5 - H / 2) / s;
      const b0x = y * qy[0] + qc[0], b0y = y * qy[1] + qc[1], b0z = y * qy[2] + qc[2];
      for (let i = i0; i <= i1; i++) {
        const x = cx + (i + 0.5 - W / 2) / s;
        const q0x = x * qx[0] + b0x, q0y = x * qx[1] + b0y, q0z = x * qx[2] + b0z;
        const b = q0x * q1[0] + q0y * q1[1] + q0z * q1[2], c2 = q0x * q0x + q0y * q0y + q0z * q0z - 1;
        const disc = b * b - a * c2; if (disc < 0) continue;
        const sq = Math.sqrt(disc); let zf = (-b + sq) / a, zb = (-b - sq) / a, ok = true;
        for (const [nR, nU, nF, d] of clips) {
          const rhs = d - x * nR - y * nU;
          if (nF > 1e-6) { const zc = rhs / nF; if (zc < zf) zf = zc; } else if (nF < -1e-6) { const zc = rhs / nF; if (zc > zb) zb = zc; } else if (rhs < 0) { ok = false; break; }
        }
        if (!ok || zf < zb) continue;
        const idx = j * W + i;
        if (k > 0) SG[idx] += Math.exp(k * zf);
        if (zf > BR[idx]) { BR[idx] = zf; BI[idx] = p.id; }
      }
    }
  }
  const z = new Float32Array(N).fill(-1e9), id = new Int16Array(N).fill(-1), grp = new Int8Array(N).fill(-1);
  for (let idx = 0; idx < N; idx++) {
    let best = -1e9, bi = -1, bg = -1;
    for (let g = 0; g < ng; g++) { if (bid[g][idx] < 0) continue; const zg = groups[g].k > 0 ? Math.log(sum[g][idx]) / groups[g].k : braw[g][idx]; if (zg > best) { best = zg; bi = bid[g][idx]; bg = g; } }
    z[idx] = best; id[idx] = bi; grp[idx] = bg;
  }
  return { z, id, grp, W, H, V, cx, cy, s };
}

// Chiếu một điểm lên mặt khối theo pháp tuyến gợi ý n (rasterize 3×3 điểm ảnh nhỏ) → {p, n}.
export function snap(prims, groups, p0, n0) {
  const V = basisFromF(norm(n0)), e = 0.004;
  const sc = sculpt(prims, groups, V, { W: 3, H: 3, cx: dot(p0, V.R), cy: dot(p0, V.U), s: 1 / e });
  const zc = sc.z[4];
  if (zc < -1e8) return { p: p0, n: norm(n0) };
  const zx = (sc.z[5] > -1e8 && sc.z[3] > -1e8) ? (sc.z[5] - sc.z[3]) / (2 * e) : 0, zy = (sc.z[7] > -1e8 && sc.z[1] > -1e8) ? (sc.z[7] - sc.z[1]) / (2 * e) : 0;
  const nl = norm([-zx, -zy, 1]);
  const p = add(add(scl(V.R, dot(p0, V.R)), V.U, dot(p0, V.U)), V.F, zc);
  const n = norm(add(add(scl(V.R, nl[0]), V.U, nl[1]), V.F, nl[2]));
  return { p, n };
}

// ---------- tiện ích bộ đệm ----------
function boxBlur(src, W, H, r, out) {
  const tmp = new Float32Array(W * H); out = out || new Float32Array(W * H); const k = 1 / (2 * r + 1);
  for (let j = 0; j < H; j++) { let acc = 0; const row = j * W;
    for (let i = -r; i <= r; i++) acc += src[row + clamp(i, 0, W - 1)];
    for (let i = 0; i < W; i++) { tmp[row + i] = acc * k; acc += src[row + Math.min(W - 1, i + r + 1)] - src[row + Math.max(0, i - r)]; } }
  for (let i = 0; i < W; i++) { let acc = 0;
    for (let j = -r; j <= r; j++) acc += tmp[clamp(j, 0, H - 1) * W + i];
    for (let j = 0; j < H; j++) { out[j * W + i] = acc * k; acc += tmp[Math.min(H - 1, j + r + 1) * W + i] - tmp[Math.max(0, j - r) * W + i]; } }
  return out;
}
export function blur(src, W, H, r, passes = 2) { let a = src; for (let p = 0; p < passes; p++) a = boxBlur(a, W, H, r); return a; }

export function dataTex(data, W, H, srgb) {
  const t = new THREE.DataTexture(data, W, H, THREE.RGBAFormat, THREE.UnsignedByteType);
  t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter;
  t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping; t.anisotropy = 4; t.flipY = false; t.needsUpdate = true;
  return t;
}

// Độ cao → normal map (hệ tiếp tuyến: x theo +u, y theo +v). du, dv = bước điểm ảnh theo đơn vị độ cao.
export function normalFromHeight(h, W, H, du, dv, bump = 1) {
  const out = new Uint8Array(W * H * 4);
  for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
    const il = Math.max(0, i - 1), ir = Math.min(W - 1, i + 1), jd = Math.max(0, j - 1), ju = Math.min(H - 1, j + 1);
    const gx = (h[j * W + ir] - h[j * W + il]) / ((ir - il) * du) * bump, gy = (h[ju * W + i] - h[jd * W + i]) / ((ju - jd) * dv) * bump;
    const l = Math.hypot(gx, gy, 1), o = (j * W + i) * 4;
    out[o] = (-gx / l * 0.5 + 0.5) * 255; out[o + 1] = (-gy / l * 0.5 + 0.5) * 255; out[o + 2] = (1 / l * 0.5 + 0.5) * 255; out[o + 3] = 255;
  }
  return out;
}

const _cv = new Map();
function scratch(W, H, key) { const k = key + W + 'x' + H; if (!_cv.has(k)) { const c = document.createElement('canvas'); c.width = W; c.height = H; _cv.set(k, c); } return _cv.get(k); }

// ---------- tranh theo góc nhìn ----------
// design: { prims, groups, color(id, P, out, ctx), features(api), cavity: {r, gain, amt, tint(id)->[r,g,b]}, soft (px blur độ cao), edge(id,P)->nhiễu rìa }
// view: viewBasis(); frame: {cx, cy, size (đơn vị), W (px)}
export function paintView(design, V, frame) {
  const W = frame.W, H = frame.W, s = W / frame.size;
  const cx = frame.c ? dot(frame.c, V.R) : 0, cy = frame.c ? dot(frame.c, V.U) : 0;
  const sc = sculpt(design.prims, design.groups, V, { W, H, cx, cy, s });
  const N = W * H, { z, id } = sc;
  let zmin = 1e9, zmax = -1e9;
  for (let k = 0; k < N; k++) if (id[k] >= 0) { if (z[k] < zmin) zmin = z[k]; if (z[k] > zmax) zmax = z[k]; }
  if (zmin > zmax) { zmin = 0; zmax = 1; }
  const zfill = zmin - 0.08;
  const zf = new Float32Array(N); for (let k = 0; k < N; k++) zf[k] = id[k] >= 0 ? z[k] : zfill;
  // Bóng hốc vẽ tay: điểm thấp hơn vùng quanh nó (hốc mắt, dưới vành mũ, khe cổ áo) → sẫm và ngả màu bóng.
  const cav = design.cavity || { r: 0.05, gain: 8, amt: 0.3 };
  const cr = Math.max(1, Math.round((cav.r ?? 0.05) * s));
  const zb = blur(zf, W, H, cr, 2);
  const img = new ImageData(W, H), D = img.data, P = [0, 0, 0], col = [0, 0, 0];
  const ctxInfo = { V, s, W, H };
  for (let j = 0; j < H; j++) {
    const y = cy + (j + 0.5 - H / 2) / s;
    for (let i = 0; i < W; i++) {
      const k = j * W + i, o = k * 4; const pid = id[k];
      if (pid < 0) { D[o + 3] = 0; continue; }
      const x = cx + (i + 0.5 - W / 2) / s, zz = z[k];
      P[0] = x * V.R[0] + y * V.U[0] + zz * V.F[0]; P[1] = x * V.R[1] + y * V.U[1] + zz * V.F[1]; P[2] = x * V.R[2] + y * V.U[2] + zz * V.F[2];
      design.color(pid, P, col, ctxInfo);
      { const il = Math.max(0, i - 1), ir = Math.min(W - 1, i + 1), jd = Math.max(0, j - 1), ju = Math.min(H - 1, j + 1);
        const gx = (zf[j * W + ir] - zf[j * W + il]) * s / (ir - il), gy = (zf[ju * W + i] - zf[jd * W + i]) * s / (ju - jd);
        const nz = 1 / Math.sqrt(1 + gx * gx + gy * gy), t = 1 - (design.turn ?? 0.14) * (1 - nz); col[0] *= t; col[1] *= t; col[2] *= t; }
      const cv = clamp((zb[k] - zf[k]) * cav.gain) * (cav.mask ? cav.mask(pid) : 1);
      if (cv > 0) { const t = cav.tint ? cav.tint(pid) : [60, 30, 40]; const a = cav.amt * cv; col[0] = mix(col[0], t[0], a); col[1] = mix(col[1], t[1], a); col[2] = mix(col[2], t[2], a); }
      D[o] = col[0]; D[o + 1] = col[1]; D[o + 2] = col[2]; D[o + 3] = 255;
    }
  }
  const relief = new Float32Array(N);
  // Nét vẽ theo điểm neo 3D (co theo góc, bị che theo độ sâu).
  if (design.features) {
    const cv = scratch(W, H, 'feat'), g = cv.getContext('2d', { willReadFrequently: true });
    const api = {
      V, s,
      // feature(anchor{p,n}, e1hint, drawFn(ctx, mode), ext [s0,t0,s1,t1] (đơn vị), opt{tol, ids:Set, reliefAmp, minFace})
      feature(an, e1h, draw, ext, opt = {}) {
        const n = an.n, facing = dot(n, V.F);
        if (facing < (opt.minFace ?? 0.12)) return;
        let e1 = e1h ? norm(add(e1h, n, -dot(e1h, n))) : norm(cross([0, 1, 0], n)); const e2 = cross(n, e1);
        const px = (dot(an.p, V.R) - cx) * s + W / 2, py = (dot(an.p, V.U) - cy) * s + H / 2, pz = dot(an.p, V.F);
        const A = s * dot(e1, V.R), B = s * dot(e1, V.U), C = s * dot(e2, V.R), Dd = s * dot(e2, V.U);
        // hộp điểm ảnh
        const cs = [[ext[0], ext[1]], [ext[2], ext[1]], [ext[0], ext[3]], [ext[2], ext[3]]].map(([a, b]) => [A * a + C * b + px, B * a + Dd * b + py]);
        const x0 = Math.max(0, Math.floor(Math.min(...cs.map((c) => c[0])) - 3)), x1 = Math.min(W, Math.ceil(Math.max(...cs.map((c) => c[0])) + 3));
        const y0 = Math.max(0, Math.floor(Math.min(...cs.map((c) => c[1])) - 3)), y1 = Math.min(H, Math.ceil(Math.max(...cs.map((c) => c[1])) + 3));
        if (x1 <= x0 || y1 <= y0) return;
        const bw = x1 - x0, bh = y1 - y0;
        const nR = dot(n, V.R), nU = dot(n, V.U), nF = Math.max(0.25, dot(n, V.F)), tol = opt.tol ?? 0.07;
        const fade = smooth(opt.minFace ?? 0.12, (opt.minFace ?? 0.12) + 0.25, facing);
        for (const mode of ['color', 'relief']) {
          if (mode === 'relief' && !opt.reliefAmp) continue;
          g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(x0, y0, bw, bh);
          g.setTransform(A, B, C, Dd, px, py); g.globalAlpha = 1;
          draw(g, mode, { facing, e1, e2 });
          g.setTransform(1, 0, 0, 1, 0, 0);
          const src = g.getImageData(x0, y0, bw, bh).data;
          for (let jj = 0; jj < bh; jj++) for (let ii = 0; ii < bw; ii++) {
            const so = (jj * bw + ii) * 4, a = src[so + 3] / 255 * fade; if (a <= 0.002) continue;
            const k = (y0 + jj) * W + (x0 + ii); if (id[k] < 0) continue;
            if (opt.ids && !opt.ids.has(id[k])) continue;
            const xx = (x0 + ii + 0.5 - px) / s, yy = (y0 + jj + 0.5 - py) / s;
            const zp = pz - (nR * xx + nU * yy) / nF;
            if (z[k] > zp + tol || z[k] < zp - tol * 1.6) continue;
            if (mode === 'color') { const o = k * 4; D[o] = mix(D[o], src[so], a); D[o + 1] = mix(D[o + 1], src[so + 1], a); D[o + 2] = mix(D[o + 2], src[so + 2], a); }
            else relief[k] += (src[so] / 255 * 2 - 1) * a * opt.reliefAmp;
          }
        }
      },
    };
    design.features(api);
  }
  if (design.reliefFn) { // nổi theo vị trí 3D (vân len, sợi tóc…)
    for (let j = 0; j < H; j++) { const y = cy + (j + 0.5 - H / 2) / s; for (let i = 0; i < W; i++) { const k = j * W + i; if (id[k] < 0) continue;
      const x = cx + (i + 0.5 - W / 2) / s, zz = z[k];
      P[0] = x * V.R[0] + y * V.U[0] + zz * V.F[0]; P[1] = x * V.R[1] + y * V.U[1] + zz * V.F[1]; P[2] = x * V.R[2] + y * V.U[2] + zz * V.F[2];
      relief[k] += design.reliefFn(id[k], P); } }
  }
  // Độ cao cho normal: khối (làm mềm nhẹ kiểu tranh) + nổi.
  const soft = Math.max(1, Math.round((design.soft ?? 0.012) * s));
  const hs = blur(zf, W, H, soft, 2);
  for (let k = 0; k < N; k++) hs[k] += relief[k];
  const nm = normalFromHeight(hs, W, H, 1 / s, 1 / s, 1);
  // alpha: phủ + rìa mềm (nhoè 1 px) + rìa cọ (nhiễu theo vị trí)
  const cov = new Float32Array(N); for (let k = 0; k < N; k++) cov[k] = id[k] >= 0 ? 1 : 0;
  const cb = blur(cov, W, H, Math.max(1, Math.round(W / 512)), 1);
  for (let k = 0; k < N; k++) {
    let a = cb[k];
    if (design.edge && a > 0 && a < 1) { const i = k % W, j = (k / W) | 0; a = clamp(a + (vn2(i * 0.35, j * 0.35) - 0.5) * design.edge); }
    D[k * 4 + 3] = a * 255;
    // bên ngoài: màu điểm phủ gần nhất (tránh viền đen khi lọc)
    nm[k * 4 + 3] = clamp((zf[k] - zmin) / (zmax - zmin)) * 255;
  }
  dilateRGB(D, W, H, 4);
  return { map: dataTex(new Uint8Array(D.buffer), W, H, true), nmap: dataTex(nm, W, H, false), zmin, zmax, sc };
}

// Loang màu ra vùng alpha = 0 (để mipmap không kéo viền đen vào).
function dilateRGB(D, W, H, iters) {
  const has = new Uint8Array(W * H); for (let k = 0; k < W * H; k++) has[k] = D[k * 4 + 3] > 8 ? 1 : 0;
  for (let it = 0; it < iters; it++) {
    const nh = has.slice();
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) { const k = j * W + i; if (has[k]) continue;
      let r = 0, g = 0, b = 0, n = 0;
      for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const ii = i + di, jj = j + dj; if (ii < 0 || jj < 0 || ii >= W || jj >= H) continue; const kk = jj * W + ii; if (!has[kk]) continue; r += D[kk * 4]; g += D[kk * 4 + 1]; b += D[kk * 4 + 2]; n++; }
      if (n) { D[k * 4] = r / n; D[k * 4 + 1] = g / n; D[k * 4 + 2] = b / n; nh[k] = 1; } }
    has.set(nh);
  }
  // phần còn lại: trung bình
  let r = 0, g = 0, b = 0, n = 0; for (let k = 0; k < W * H; k++) if (has[k]) { r += D[k * 4]; g += D[k * 4 + 1]; b += D[k * 4 + 2]; n++; }
  if (n) for (let k = 0; k < W * H; k++) if (!has[k]) { D[k * 4] = r / n; D[k * 4 + 1] = g / n; D[k * 4 + 2] = b / n; }
}

// ---------- tranh dải ----------
// o: { W, H, aspect (chiều dài dải / bán kính, theo đơn vị độ cao), width(v)->nửa bề rộng hình (0..1 của dải), color(u,v,out,s), draw(ctx,W,H,mode),
//      relief(u,v,s)->độ cao cộng, edge (biên độ rìa cọ), endRound [đầu, cuối] (độ bo hai đầu, phần v), prof(s)->mặt cắt }
export function paintRibbon(o) {
  const W = o.W, H = o.H, N = W * H;
  const img = new ImageData(W, H), D = img.data, h = new Float32Array(N), col = [0, 0, 0];
  const wOf = o.width || (() => 1), prof = o.prof || ((s) => Math.sqrt(Math.max(0, 1 - s * s)));
  const alpha = new Float32Array(N);
  for (let j = 0; j < H; j++) {
    const v = (j + 0.5) / H, hw = wOf(v);
    for (let i = 0; i < W; i++) {
      const u = (i + 0.5) / W, sx = (u * 2 - 1), k = j * W + i, s = sx / Math.max(1e-3, hw);
      let a = 1 - smooth(0.86, 1.0, Math.abs(s) + (o.edge ? (vn2(v * 2.2 * (o.aspect || 4), sx > 0 ? 3.3 : 9.1) - 0.5) * o.edge * 0.12 : 0));
      if (o.endRound) { const [r0, r1] = o.endRound;
        if (r0 > 0 && v < r0) { const t = (r0 - v) / r0; a *= 1 - smooth(0.85, 1.0, Math.hypot(t, s)); }
        if (r1 > 0 && v > 1 - r1) { const t = (v - 1 + r1) / r1; a *= 1 - smooth(0.85, 1.0, Math.hypot(t, s)); } }
      alpha[k] = a;
      const ss = clamp(s, -1, 1);
      h[k] = prof(ss) * (o.hScale ? o.hScale(v) : 1);
      if (o.endRound) { const [r0, r1] = o.endRound;
        if (r0 > 0 && v < r0) { const t = (r0 - v) / r0; h[k] *= Math.sqrt(Math.max(0, 1 - Math.min(1, t * t))); }
        if (r1 > 0 && v > 1 - r1) { const t = (v - 1 + r1) / r1; h[k] *= Math.sqrt(Math.max(0, 1 - Math.min(1, t * t))); } }
      if (o.relief) h[k] += o.relief(u, v, ss);
      o.color(u, v, col, ss);
      const turn = 1 - (o.turn ?? 0.16) * (1 - Math.sqrt(Math.max(0, 1 - ss * ss)));   // "mép quay đi" tối hơn (kiểu vẽ khối)
      const oo = k * 4; D[oo] = col[0] * turn; D[oo + 1] = col[1] * turn; D[oo + 2] = col[2] * turn; D[oo + 3] = 255;
    }
  }
  if (o.draw) {
    const cv = scratch(W, H, 'rib'), g = cv.getContext('2d', { willReadFrequently: true });
    g.setTransform(1, 0, 0, 1, 0, 0); g.putImageData(img, 0, 0); o.draw(g, W, H, 'color');
    const d2 = g.getImageData(0, 0, W, H).data; D.set(d2);
    if (o.drawRelief) { g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H); o.drawRelief(g, W, H);
      const r = g.getImageData(0, 0, W, H).data; for (let k = 0; k < N; k++) h[k] += (r[k * 4] / 255 * 2 - 1) * (r[k * 4 + 3] / 255) * (o.reliefAmp || 0.1); }
  }
  const hb = blur(h, W, H, 1, 1);
  // bước điểm ảnh theo đơn vị bán kính: ngang 2/W (vì s ∈ [-1,1] trên cả dải), dọc aspect/H
  const nm = normalFromHeight(hb, W, H, 2 / W, (o.aspect || 4) / H, 1);
  for (let k = 0; k < N; k++) { D[k * 4 + 3] = alpha[k] * 255; nm[k * 4 + 3] = clamp(h[k] / (o.hMax || 1)) * 255; }
  dilateRGB(D, W, H, 3);
  return { map: dataTex(new Uint8Array(D.buffer), W, H, true), nmap: dataTex(nm, W, H, false) };
}

// Nét cọ tiện dụng cho canvas: đường cong mềm có độ dày thay đổi (thuôn hai đầu), màu rgba.
export function strokePath(g, pts, w0, w1, color, taper = true) {
  g.strokeStyle = color; g.lineCap = 'round'; g.lineJoin = 'round';
  const n = pts.length; if (n < 2) return;
  const segs = 16 * (n - 1);
  const at = (t) => { // Catmull-Rom qua các điểm
    const f = t * (n - 1), i = Math.min(n - 2, Math.floor(f)), u = f - i;
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(n - 1, i + 2)];
    const cr = (a, b, c, d) => 0.5 * ((2 * b) + (-a + c) * u + (2 * a - 5 * b + 4 * c - d) * u * u + (-a + 3 * b - 3 * c + d) * u * u * u);
    return [cr(p0[0], p1[0], p2[0], p3[0]), cr(p0[1], p1[1], p2[1], p3[1])];
  };
  let prev = at(0);
  for (let k = 1; k <= segs; k++) {
    const t = k / segs, p = at(t);
    const tw = taper ? Math.sin(Math.PI * Math.min(1, Math.max(0, (t - 0.5 / segs)))) : 1;
    g.lineWidth = Math.max(1e-4, mix(w0, w1, t) * (taper ? 0.35 + 0.65 * tw : 1));
    g.beginPath(); g.moveTo(prev[0], prev[1]); g.lineTo(p[0], p[1]); g.stroke(); prev = p;
  }
}
export function blob(g, x, y, rx, ry, rot, color) { g.fillStyle = color; g.beginPath(); g.ellipse(x, y, Math.max(1e-5, rx), Math.max(1e-5, ry), rot, 0, Math.PI * 2); g.fill(); }
export function softBlob(g, x, y, r, rgb, a, sy = 1) {
  g.save(); g.translate(x, y); g.scale(1, sy);
  const gr = g.createRadialGradient(0, 0, 0, 0, 0, r); gr.addColorStop(0, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${a})`); gr.addColorStop(1, `rgba(${rgb[0]},${rgb[1]},${rgb[2]},0)`);
  g.fillStyle = gr; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill(); g.restore();
}

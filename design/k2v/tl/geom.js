// K2V tl · hình học toà nhà THUẦN (không DOM, không three) → kiểm được bằng Node (scripts/k2tl/tests/test_geom.mjs).
// Bài học R&D (lab/timelapse §6.3 lỗi 0): tường từng lộn mặt vào trong vì đổi thứ tự đỉnh theo mắt. Ở đây hướng mặt được
// KIỂM BẰNG TÍCH CÓ HƯỚNG trong test: pháp tuyến hình học (b−a)×(c−a) phải cùng chiều pháp tuyến ngoài của cạnh.
// Toạ độ vòng: [[E, N], …] (m). Đầu ra theo hệ three: x = E, y = cao cục bộ (0 = chân), z = −N.

export const signedArea = (r) => { let s = 0; for (let i = 0; i < r.length; i++) { const [x0, y0] = r[i], [x1, y1] = r[(i + 1) % r.length]; s += x0 * y1 - x1 * y0; } return s / 2; };
export const ccw = (r) => (signedArea(r) < 0 ? r.slice().reverse() : r.slice());   // ngược chiều kim đồng hồ trong mặt phẳng (E, N)
export function isConvex(r) { let sg = 0; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length], c = r[(i + 2) % r.length];
  const z = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]); if (Math.abs(z) < 1e-6) continue; const s = Math.sign(z); if (sg && s !== sg) return false; sg = s; } return true; }
// Douglas–Peucker trên vòng kín (LOD xa)
export function simplify(r, eps) {
  if (r.length <= 4) return r;
  const dp = (p) => { if (p.length < 3) return p; const [a, b] = [p[0], p[p.length - 1]]; let mx = -1, k = 0;
    for (let i = 1; i < p.length - 1; i++) { const d = Math.abs((b[0] - a[0]) * (a[1] - p[i][1]) - (a[0] - p[i][0]) * (b[1] - a[1])) / (Math.hypot(b[0] - a[0], b[1] - a[1]) || 1); if (d > mx) { mx = d; k = i; } }
    return mx > eps ? dp(p.slice(0, k + 1)).slice(0, -1).concat(dp(p.slice(k))) : [a, b]; };
  let k = 0, md = -1; for (let i = 1; i < r.length; i++) { const d = Math.hypot(r[i][0] - r[0][0], r[i][1] - r[0][1]); if (d > md) { md = d; k = i; } }   // tách vòng ở đỉnh xa nhất
  const s = dp(r.slice(0, k + 1)).slice(0, -1).concat(dp(r.slice(k).concat([r[0]])).slice(0, -1)); return s.length >= 3 ? s : r;
}
// Tường: mỗi cạnh 2 tam giác. emit(x, y, z, nx, ny, nz, u, top, EL) — u = khoảng cách dọc CẠNH (m, từ đầu cạnh; V5b-1b: cửa sổ căn giữa
// từng mặt, không vắt qua góc), EL = dài cạnh; top 0/1. y0: chân (≠ 0 cho tường chắn mái / parapet).
export function walls(ring, h, emit, y0 = 0) {
  const r = ccw(ring);
  for (let i = 0; i < r.length; i++) {
    const a = r[i], b = r[(i + 1) % r.length], dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1;
    const nx = dn / l, nz = dx / l;   // pháp tuyến ngoài (E,N) = (dn, −dx) → three (dn, 0, +dx)
    const A0 = [a[0], y0, -a[1]], B0 = [b[0], y0, -b[1]], B1 = [b[0], h, -b[1]], A1 = [a[0], h, -a[1]];
    for (const [p, uu, t] of [[A0, 0, 0], [B0, l, 0], [B1, l, 1], [A0, 0, 0], [B1, l, 1], [A1, 0, 1]]) emit(p[0], p[1], p[2], nx, 0, nz, uu, t, l);
  }
}
// Mái: phẳng (tam giác hoá tiêm vào: tri(ring) → [[i,j,k]…]) hoặc mái chóp/hông cho vòng lồi (đỉnh ở trọng tâm, cao ridge).
export function roof(ring, h, ridge, tri, emit) {
  const r = ccw(ring);
  if (ridge > 0 && isConvex(r) && r.length <= 10) {
    const cx = r.reduce((s, p) => s + p[0], 0) / r.length, cn = r.reduce((s, p) => s + p[1], 0) / r.length;
    for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length];
      const P = [[a[0], h, -a[1]], [b[0], h, -b[1]], [cx, h + ridge, -cn]];
      const ux = P[1][0] - P[0][0], uy = P[1][1] - P[0][1], uz = P[1][2] - P[0][2], vx = P[2][0] - P[0][0], vy = P[2][1] - P[0][1], vz = P[2][2] - P[0][2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
      for (const p of P) emit(p[0], p[1], p[2], nx, ny, nz, -1, 1); }
    return 'hip';
  }
  for (const t of tri(r)) { const P = t.map((k) => [r[k][0], h, -r[k][1]]);
    // giữ thứ tự sao cho pháp tuyến hướng lên (+y)
    const cr = (P[1][0] - P[0][0]) * (P[2][2] - P[0][2]) - (P[1][2] - P[0][2]) * (P[2][0] - P[0][0]);
    const Q = cr > 0 ? [P[0], P[2], P[1]] : P; for (const p of Q) emit(p[0], p[1], p[2], 0, 1, 0, -1, 1); }
  return 'flat';
}
export const ridgeFor = (ring) => Math.max(1.2, Math.min(4.0, 0.22 * Math.sqrt(Math.abs(signedArea(ring)))));

// ---- V5b-1b: mái nhiều kiểu + chi tiết hình học (cổng 16/10: "nhà khối sạch đồng màu")
// tam giác có hướng: đổi thứ tự để pháp tuyến hình học cùng chiều `want` (kiểm bằng tích có hướng trong test)
export function triOut(P0, P1, P2, want, emit, u = -1) {
  const ux = P1[0] - P0[0], uy = P1[1] - P0[1], uz = P1[2] - P0[2], vx = P2[0] - P0[0], vy = P2[1] - P0[1], vz = P2[2] - P0[2];
  let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
  let Q = [P0, P1, P2]; if (nx * want[0] + ny * want[1] + nz * want[2] < 0) { Q = [P0, P2, P1]; nx = -nx; ny = -ny; nz = -nz; }
  for (const p of Q) emit(p[0], p[1], p[2], nx, ny, nz, u, 1, 0);
}
// hình chữ nhật gần đúng (4 đỉnh, góc 90° ± 14°): trả {A,B,C,D (ccw, AB = cạnh dài), L, W, ax, c} — dùng cho mái hai mái / mái hông có nóc
export function rectOf(ring) {
  const r = ccw(ring); if (r.length !== 4) return null;
  for (let i = 0; i < 4; i++) { const a = r[i], b = r[(i + 1) % 4], c = r[(i + 2) % 4], u = [b[0] - a[0], b[1] - a[1]], v = [c[0] - b[0], c[1] - b[1]];
    const cs = (u[0] * v[0] + u[1] * v[1]) / ((Math.hypot(...u) * Math.hypot(...v)) || 1); if (Math.abs(cs) > 0.24) return null; }
  const l01 = Math.hypot(r[1][0] - r[0][0], r[1][1] - r[0][1]), l12 = Math.hypot(r[2][0] - r[1][0], r[2][1] - r[1][1]);
  const k = l01 >= l12 ? 0 : 1, [A, B, C, D] = [0, 1, 2, 3].map((i) => r[(i + k) % 4]);
  const L = Math.hypot(B[0] - A[0], B[1] - A[1]), W = Math.hypot(C[0] - B[0], C[1] - B[1]);
  return { A, B, C, D, L, W, ax: [(B[0] - A[0]) / L, (B[1] - A[1]) / L], c: [(A[0] + C[0]) / 2, (A[1] + C[1]) / 2] };
}
// mái dốc trên hình chữ nhật: kind 'gable' (hai mái + đầu hồi) | 'hipr' (mái hông có nóc). ov = chìa mái (m). Toạ độ three: (E, y, −N).
export function pitched(ring, h, ridge, kind, emit, ov = 0.35) {
  const R = rectOf(ring); if (!R) return null;
  const { ax, L, W, c } = R, ny_ = [-ax[1], ax[0]];   // ny_: pháp tuyến cạnh dài (hướng trong mặt phẳng E,N)
  const P = (s, t, y) => [c[0] + ax[0] * s + ny_[0] * t, y, -(c[1] + ax[1] * s + ny_[1] * t)];
  const hl = L / 2 + ov, hw = W / 2 + ov, rl = kind === 'hipr' ? Math.max(0.5, L / 2 - W / 2) : hl;
  const A = P(-hl, -hw, h), B = P(hl, -hw, h), C = P(hl, hw, h), D = P(-hl, hw, h), R1 = P(-rl, 0, h + ridge), R2 = P(rl, 0, h + ridge);
  const up = (t) => [ny_[0] * t * 0.3, 1, -ny_[1] * t * 0.3];
  triOut(A, B, R2, up(-1), emit); triOut(A, R2, R1, up(-1), emit); triOut(C, D, R1, up(1), emit); triOut(C, R1, R2, up(1), emit);
  const endW = [-ax[0], 0.3, ax[1]], endE = [ax[0], 0.3, -ax[1]];
  if (kind === 'hipr') { triOut(D, A, R1, endW, emit); triOut(B, C, R2, endE, emit); }
  else { const a0 = P(-L / 2, -W / 2, h), d0 = P(-L / 2, W / 2, h), b0 = P(L / 2, -W / 2, h), c0 = P(L / 2, W / 2, h), g1 = P(-L / 2, 0, h + ridge * (hw - ov) / hw), g2 = P(L / 2, 0, h + ridge * (hw - ov) / hw);
    triOut(d0, a0, g1, [-ax[0], 0, ax[1]], (x, y, z, nx, ny, nz) => emit(x, y, z, nx, ny, nz, 0.01, 1, 0)); triOut(b0, c0, g2, [ax[0], 0, -ax[1]], (x, y, z, nx, ny, nz) => emit(x, y, z, nx, ny, nz, 0.01, 1, 0)); }   // đầu hồi: tường (u ≥ 0)
  return kind;
}
// hộp (5 mặt, không đáy) tâm chân (e, y, n), rộng w (dọc hướng rot), sâu d, cao hh; tag u (−2 ban công/lan can, −3 vật trên mái)
export function boxAt(e, y, n, w, d, hh, rot, emit, u = -3) {
  const c = Math.cos(rot), s = Math.sin(rot), V = (x, yy, z) => [e + x * c - z * s, y + yy, -(n + x * s + z * c)];
  const N3 = (x, yy, z) => [x * c - z * s, yy, -(x * s + z * c)];
  const F = [[[1, 0, 0], [[.5, 0, -.5], [.5, 1, -.5], [.5, 1, .5], [.5, 0, .5]]], [[-1, 0, 0], [[-.5, 0, .5], [-.5, 1, .5], [-.5, 1, -.5], [-.5, 0, -.5]]],
    [[0, 1, 0], [[-.5, 1, -.5], [-.5, 1, .5], [.5, 1, .5], [.5, 1, -.5]]], [[0, 0, 1], [[.5, 0, .5], [.5, 1, .5], [-.5, 1, .5], [-.5, 0, .5]]], [[0, 0, -1], [[-.5, 0, -.5], [-.5, 1, -.5], [.5, 1, -.5], [.5, 0, -.5]]]];
  for (const [nn, q] of F) { const P = q.map(([x, yy, z]) => V(x * w, yy * hh, z * d)); const want = N3(...nn); triOut(P[0], P[1], P[2], want, emit, u); triOut(P[0], P[2], P[3], want, emit, u); }
}
// ban công kiểu Gibraltar/Andalucía: mỗi tầng ≥ 1 trên cạnh dài nhất một dải sàn chìa 0,8 m + lan can (shader đục song sắt), tag −2
export function balconies(ring, h, floorH, emit, frac = 0.7) {
  const r = ccw(ring); let k = 0, best = 0;
  for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l > best) { best = l; k = i; } }
  if (best < 5) return 0; const a = r[k], b = r[(k + 1) % r.length], dx = (b[0] - a[0]) / best, dn = (b[1] - a[1]) / best, on = [dn, -dx];   // pháp tuyến ngoài (E,N)
  const rot = Math.atan2(dn, dx), w = best * frac, cx = (a[0] + b[0]) / 2, cn = (a[1] + b[1]) / 2; let n = 0;
  for (let y = floorH; y < h - 1.6; y += floorH) {
    boxAt(cx + on[0] * 0.42, y - 0.12, cn + on[1] * 0.42, w, 0.84, 0.14, rot, emit, -2);
    boxAt(cx + on[0] * 0.82, y + 0.02, cn + on[1] * 0.82, w, 0.06, 1.0, rot, emit, -4); n++; }
  return n;
}

// cắt đa giác bởi nửa mặt phẳng n·p ≤ d (Sutherland–Hodgman; vòng lõm có thể sinh cạnh suy biến diện tích 0 — vô hại khi đùn)
export function clipHalf(r, nx, ny, d) {
  const out = []; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length], da = nx * a[0] + ny * a[1] - d, db = nx * b[0] + ny * b[1] - d;
    if (da <= 0) out.push(a); if ((da < 0 && db > 0) || (da > 0 && db < 0)) { const u = da / (da - db); out.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]); } }
  return out;
}
// chia khối lớn thành LÔ NHÀ (V5b-1b: OSM Gibraltar hay vẽ cả dãy phố là một đa giác → "khối sạch"): cắt theo trục chính (PCA) thành dải
// rộng w0..w1 (m, băm) × sâu dMax; bỏ mảnh < 12 m². Trả danh sách vòng.
export function parcels(ring, R, w0 = 7, w1 = 13, dMax = 16) {
  const n = ring.length; let cx = 0, cy = 0; for (const p of ring) { cx += p[0]; cy += p[1]; } cx /= n; cy /= n;
  let sxx = 0, syy = 0, sxy = 0; for (const [x, y] of ring) { sxx += (x - cx) ** 2; syy += (y - cy) ** 2; sxy += (x - cx) * (y - cy); }
  const th = 0.5 * Math.atan2(2 * sxy, sxx - syy), ux = Math.cos(th), uy = Math.sin(th), vx = -uy, vy = ux;
  let a0 = Infinity, a1 = -Infinity, b0 = Infinity, b1 = -Infinity;
  for (const [x, y] of ring) { const a = (x - cx) * ux + (y - cy) * uy, b = (x - cx) * vx + (y - cy) * vy; a0 = Math.min(a0, a); a1 = Math.max(a1, a); b0 = Math.min(b0, b); b1 = Math.max(b1, b); }
  const nb = Math.max(1, Math.round((b1 - b0) / dMax)), out = [];
  for (let j = 0; j < nb; j++) { const bb0 = b0 + (b1 - b0) * j / nb, bb1 = b0 + (b1 - b0) * (j + 1) / nb;
    for (let a = a0; a < a1 - 1e-6;) { const w = w0 + (w1 - w0) * R(), aa1 = a1 - (a + w) < w0 * 0.6 ? a1 : a + w;
      let r = ring; const o = (nx, ny, d) => { r = clipHalf(r, nx, ny, d); };
      o(ux, uy, aa1 + cx * ux + cy * uy); o(-ux, -uy, -(a + cx * ux + cy * uy)); o(vx, vy, bb1 + cx * vx + cy * vy); o(-vx, -vy, -(bb0 + cx * vx + cy * vy));
      if (r.length >= 3 && Math.abs(signedArea(r)) > 12) out.push(r); a = aa1; } }
  return out.length ? out : [ring];
}

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
// Tường: mỗi cạnh 2 tam giác. emit(x, y, z, nx, ny, nz, u, top) — u = khoảng cách dọc tường (m) cho cửa sổ; top 0/1.
export function walls(ring, h, emit) {
  const r = ccw(ring); let u = 0;
  for (let i = 0; i < r.length; i++) {
    const a = r[i], b = r[(i + 1) % r.length], dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1;
    const nx = dn / l, nz = dx / l;   // pháp tuyến ngoài (E,N) = (dn, −dx) → three (dn, 0, +dx)
    const A0 = [a[0], 0, -a[1]], B0 = [b[0], 0, -b[1]], B1 = [b[0], h, -b[1]], A1 = [a[0], h, -a[1]];
    for (const [p, uu, t] of [[A0, u, 0], [B0, u + l, 0], [B1, u + l, 1], [A0, u, 0], [B1, u + l, 1], [A1, u, 1]]) emit(p[0], p[1], p[2], nx, 0, nz, uu, t);
    u += l;
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

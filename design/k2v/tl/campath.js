// K2V tl · NGỮ PHÁP MÁY QUAY (port lab/timelapse camAt + đo): spline Hermite theo thời gian (tiếp tuyến Catmull-Rom không đều) qua mốc
// {t, p:[E,cao,N], l:[E,cao,N], fov}; bay dọc tuyến thật = mốc dày lấy mẫu trên hình học đường/sông (lệch tim tuyến đo lại mỗi khung);
// đo: khoảng cách tới đích (reveal/zoom-in ≥ 5×), tốc độ, quãng đứng yên (≤ 6 s), mỗi chuyển động gắn nhịp thông tin.
// (thuần JS — không import three: test được bằng Node, scripts/k2tl/tests/test_campath.mjs)

export function lineLen(L) { let s = 0; for (let i = 1; i < L.length; i++) s += Math.hypot(L[i][0] - L[i - 1][0], L[i][1] - L[i - 1][1]); return s; }
export function lineAt(L, s) { for (let i = 1; i < L.length; i++) { const l = Math.hypot(L[i][0] - L[i - 1][0], L[i][1] - L[i - 1][1]); if (s <= l || i === L.length - 1) { const u = Math.min(1, s / (l || 1)); return [L[i - 1][0] + (L[i][0] - L[i - 1][0]) * u, L[i - 1][1] + (L[i][1] - L[i - 1][1]) * u]; } s -= l; } return L[L.length - 1]; }
export function distToLine(L, e, n) { let m = Infinity; for (let i = 1; i < L.length; i++) { const [a, b] = [L[i - 1], L[i]], dx = b[0] - a[0], dn = b[1] - a[1], l2 = dx * dx + dn * dn || 1;
  const u = Math.max(0, Math.min(1, ((e - a[0]) * dx + (n - a[1]) * dn) / l2)); m = Math.min(m, Math.hypot(e - a[0] - u * dx, n - a[1] - u * dn)); } return m; }
// mốc dày dọc tuyến: từ quãng s0→s1 (m) trong [t0, t1], cao h (hoặc [h0,h1]), nhìn trước look m, nghiêng xuống dip m
export function alongLine(L, { s0, s1, t0, t1, h, look = 220, dip = 25, dt = 0.2, hAt = () => 0 }) {
  const K = [], H = Array.isArray(h) ? h : [h, h];
  for (let t = t0; t <= t1 + 1e-6; t += dt) { const u = (t - t0) / (t1 - t0), s = s0 + (s1 - s0) * u, [e, n] = lineAt(L, s), [le, ln] = lineAt(L, s + Math.sign(s1 - s0) * look);
    const hh = H[0] + (H[1] - H[0]) * u; K.push({ t: +t.toFixed(4), p: [e, hAt(e, n) + hh, n], l: [le, hAt(le, ln) + hh - dip, ln], line: true }); }
  return K;
}
export function makeCamPath(keys) {
  const K = keys.slice().sort((a, b) => a.t - b.t);
  const val = (k, f, i) => (f === 'fov' ? (k.fov ?? 38) : k[f][i]);
  function at(t) {
    if (t <= K[0].t) t = K[0].t; if (t >= K[K.length - 1].t) t = K[K.length - 1].t;
    let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], hh = b.t - a.t, u = (t - a.t) / hh, u2 = u * u, u3 = u2 * u;
    const H = (f, j) => { const p0 = val(a, f, j), p1 = val(b, f, j);
      const m0 = i > 0 ? (p1 - val(K[i - 1], f, j)) / (b.t - K[i - 1].t) : (p1 - p0) / hh, m1 = i + 2 < K.length ? (val(K[i + 2], f, j) - p0) / (K[i + 2].t - a.t) : (p1 - p0) / hh;
      return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * hh * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * hh * m1; };
    return { p: [0, 1, 2].map((j) => H('p', j)), l: [0, 1, 2].map((j) => H('l', j)), fov: H('fov', 0), onLine: !!(a.line && b.line) };
  }
  return { at, keys: K };
}
export function applyCam(cam, c) { cam.position.set(c.p[0], c.p[1], -c.p[2]); cam.up.set(0, 1, 0); cam.lookAt(c.l[0], c.l[1], -c.l[2]); if (Math.abs(cam.fov - c.fov) > 1e-4) { cam.fov = c.fov; cam.updateProjectionMatrix(); } cam.updateMatrixWorld(); }
// nhật ký máy quay cả đoạn (không dựng hình): vị trí, điểm nhìn, năm, lệch tuyến, khoảng cách tới đích, tốc độ (m/s), tốc độ góc (°/s)
export function camLog(path, N, fps, yearAt, opt = {}) {
  const out = []; let prev = null;
  for (let f = 0; f < N; f++) { const t = f / fps, c = path.at(t), r = { f, t: +t.toFixed(3), year: +yearAt(t).toFixed(2), pos: c.p.map((v) => +v.toFixed(2)), look: c.l.map((v) => +v.toFixed(2)), fov: +c.fov.toFixed(2) };
    if (opt.line && c.onLine) r.dev_m = +distToLine(opt.line, c.p[0], c.p[2]).toFixed(2);
    for (const [k, p] of Object.entries(opt.focus || {})) r['d_' + k] = +Math.hypot(c.p[0] - p[0], c.p[1] - p[1], c.p[2] - p[2]).toFixed(1);
    if (prev) { r.v = +(Math.hypot(...c.p.map((v, i) => v - prev.p[i])) * fps).toFixed(2);
      const d0 = prev.l.map((v, i) => v - prev.p[i]), d1 = c.l.map((v, i) => v - c.p[i]), n0 = Math.hypot(...d0), n1 = Math.hypot(...d1);
      r.w = +(Math.acos(Math.min(1, d0.reduce((s, v, i) => s + v * d1[i], 0) / (n0 * n1))) * 180 / Math.PI * fps).toFixed(2); }
    out.push(r); prev = c; }
  let run = 0, maxStill = 0; for (const r of out) { if ((r.v ?? 1) < 0.5 && (r.w ?? 1) < 0.3) { run++; maxStill = Math.max(maxStill, run); } else run = 0; }
  return { frames: out, max_still_s: +(maxStill / fps).toFixed(2) };
}

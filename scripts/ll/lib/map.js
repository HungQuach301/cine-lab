// Last Lamplighters · thư viện mẫu — bản đồ thành phố trên tấm giấy (mực nâu), tổng quát hoá từ tập 1 (đoạn 02, 05, 06).
// Sửa việc tồn tập 1 ("phố vắt qua sông phía đông Tower, năm 1820 chưa có cầu"):
//   - mạng phố KHÔNG BAO GIỜ đi qua nước; chỉ cầu có năm xây ≤ năm của bản đồ (p.year) mới được vẽ và nối hai bờ;
//   - dáng sông/đảo theo toạ độ công khai (km từ gốc), giản lược; không dùng tile hay dữ liệu bản đồ có bản quyền.
// p = { city: 'london' | 'newyork' | {đặc tả riêng}, year, title, grow: [t0, t1], cam: [{ t, z, c: [km x, km y] }], labels: [{ s, at: [x,y], t, italic }],
//       pins: [{ s, at: [x,y], t }], lampsLit: [t0, t1] }
'use strict';
const CITY = {
  // gốc Trafalgar Sq; x km về đông, y km về nam. Sông Thames: Wandsworth → Westminster → City → Tower → vòng Isle of Dogs → Blackwall (tập 1, M2.2).
  london: { pxkm: 100, center: [2.2, 1.2], rivers: [{ w: 0.26, pts: [[-4.9, 4.9], [-4.16, 4.73], [-3.4, 3.2], [-3.03, 2.89], [-2.2, 2.75], [-1.5, 2.6], [-0.6, 2.45], [0.07, 2.22], [0.31, 1.5], [0.43, 0.8], [0.53, 0.19], [0.78, -0.08], [1.65, -0.18],
    [2.8, 0.01], [3.66, 0.28], [4.73, 0.44], [5.7, 0.25], [6.5, 0.12], [7.0, 0.45], [7.0, 1.2], [7.2, 2.15], [7.7, 2.6], [8.3, 2.67], [8.95, 2.35], [9.3, 1.6], [9.25, 0.55], [9.6, 0.15], [10.2, 0.6], [10.6, 1.25], [11.6, 1.4]] }],
    // cầu: toạ độ từ vĩ độ/kinh độ công khai (≈ 69,3 km/độ kinh, 111,3 km/độ vĩ ở London)
    bridges: [{ s: 'London Bridge', y: 1209, at: [2.8, 0.01] }, { s: 'Westminster Bridge', y: 1750, at: [0.43, 0.8] }, { s: 'Blackfriars Bridge', y: 1769, at: [1.65, -0.18] }, { s: 'Battersea Bridge', y: 1771, at: [-3.03, 2.89] },
      { s: 'Vauxhall Bridge', y: 1816, at: [0.07, 2.22] }, { s: 'Waterloo Bridge', y: 1817, at: [0.78, -0.08] }, { s: 'Southwark Bridge', y: 1819, at: [2.2, -0.1] }, { s: 'Tower Bridge', y: 1894, at: [3.66, 0.28] }],
    seeds: [[-0.4, 0.2], [2.4, -0.6], [1.0, 1.4], [5.0, -0.5], [-2.0, 1.4]], extent: [[-5, -3], [11.5, 5]] },
  // gốc Battery (40.7003 N, 74.0150 W); x km về đông, y km về nam. Đảo Manhattan giản lược 16 điểm; lưới phố nghiêng ≈ 29°.
  newyork: (() => { const ll = [[40.7003, -74.0150], [40.7230, -74.0130], [40.7480, -74.0090], [40.7720, -73.9940], [40.8000, -73.9720], [40.8300, -73.9520], [40.8600, -73.9340], [40.8780, -73.9260], [40.8730, -73.9110],
      [40.8350, -73.9340], [40.8000, -73.9290], [40.7760, -73.9420], [40.7500, -73.9680], [40.7280, -73.9720], [40.7120, -73.9770], [40.7080, -73.9990]];
    const k = ([la, lo]) => [(lo + 74.015) * 84.4, -(la - 40.7003) * 111.2];
    return { pxkm: 55, center: [4, -9], land: ll.map(k), grid: { ang: -0.506, step: 0.26 },
      bridges: [{ s: 'Brooklyn Bridge', y: 1883, at: k([40.7061, -73.9969]) }, { s: 'Williamsburg Bridge', y: 1903, at: k([40.7134, -73.9724]) }, { s: 'Queensboro Bridge', y: 1909, at: k([40.7570, -73.9540]) }],
      extent: [[-4, -21], [12, 2]] }; })(),
};
function cityOf(p) { return typeof p.city === 'string' ? CITY[p.city] : p.city; }
function inPoly(P, x, y) { let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; }
function segDist(P, x, y) { let b = 1e9; for (let i = 0; i < P.length - 1; i++) { const [ax, ay] = P[i], [bx, by] = P[i + 1], dx = bx - ax, dy = by - ay, u = cl(((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy || 1)); b = Math.min(b, Math.hypot(x - ax - dx * u, y - ay - dy * u)); } return b; }
function smoothLine(k) { const out = []; for (let i = 0; i < k.length - 1; i++) for (let s = 0; s < 8; s++) { const u = s / 8, a = k[Math.max(0, i - 1)], b = k[i], c = k[i + 1], d = k[Math.min(k.length - 1, i + 2)];
  const cr = (p0, p1, p2, p3) => 0.5 * (2 * p1 + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u); out.push([cr(a[0], b[0], c[0], d[0]), cr(a[1], b[1], c[1], d[1])]); } out.push(k[k.length - 1]); return out; }
// nước? (km)
function wet(C, x, y, m = 0.06) { if (C.land && !inPoly(C.land, x, y)) return true; if (C.land && C.land.length && segDist(C.land.concat([C.land[0]]), x, y) < m) return true;
  for (const r of C.rivers || []) if (segDist(r.sm || (r.sm = smoothLine(r.pts)), x, y) < r.w / 2 + m) return true; return false; }
// mạng phố tất định (km); mỗi đoạn mang d = "khoảng cách mọc" để hiện dần
function buildNet(C, seed) {
  if (C._net) return C._net; const R = rng(seed || 1807), segs = [];
  if (C.grid) { const { ang, step } = C.grid, ca = Math.cos(ang), sa = Math.sin(ang), [[ex0, ey0], [ex1, ey1]] = C.extent, D = Math.hypot(ex1 - ex0, ey1 - ey0);
    for (const dir of [0, 1]) for (let o = -D; o <= D; o += dir ? step * 3.2 : step) { let cur = []; const flush = () => { if (cur.length > 1) segs.push(cur); cur = []; };
      for (let s = -D; s <= D; s += 0.08) { const x = (dir ? ca * s - sa * o : ca * o - sa * s) + (ex0 + ex1) / 2, y = (dir ? sa * s + ca * o : sa * o + ca * s) + (ey0 + ey1) / 2;
        if (x < ex0 || x > ex1 || y < ey0 || y > ey1 || wet(C, x, y)) flush(); else cur.push([x, y]); } flush(); } }
  else { const occ = new Map(), cell = 0.2, key = (x, y) => `${Math.floor(x / cell)},${Math.floor(y / cell)}`, [[ex0, ey0], [ex1, ey1]] = C.extent;
    const tips = C.seeds.flatMap(([x, y]) => [0, 1.6, 3.2, 4.8].map((a) => ({ x, y, a: a + R() * 0.4, dep: 0 })));
    while (tips.length && segs.length < 520) { const tp = tips.shift(); let { x, y, a } = tp; const pts = [[x, y]]; let ok = true;
      for (let s = 0, n = 4 + Math.floor(R() * 6); s < n; s++) { a += (R() - 0.5) * 0.24; const st = 0.3 + R() * 0.14, nx = x + Math.cos(a) * st, ny = y + Math.sin(a) * st;
        if (nx < ex0 || nx > ex1 || ny < ey0 || ny > ey1 || wet(C, nx, ny)) { ok = false; break; }
        const o = occ.get(key(nx, ny)); if (o !== undefined && o !== segs.length) { pts.push([nx, ny]); ok = false; break; }
        pts.push([nx, ny]); x = nx; y = ny; occ.set(key(x, y), segs.length); }
      if (pts.length < 2) continue; segs.push(pts); if (!ok || tp.dep > 30) { if (tp.dep < 30 && R() < 0.7) tips.push({ x, y, a: a + (R() < 0.5 ? -1 : 1) * 1.4, dep: tp.dep + 1 }); continue; }
      const nb = R() < 0.45 ? 2 : 1; for (let b = 0; b < nb; b++) tips.push({ x, y, a: a + (b === 0 && nb > 1 ? (R() - 0.5) * 0.3 : (R() < 0.5 ? -1 : 1) * (1.05 + R() * 0.6)), dep: tp.dep + 1 }); } }
  const c0 = C.center; segs.forEach((s) => (s.d = Math.min(...s.map(([x, y]) => Math.hypot(x - c0[0], y - c0[1])))));
  const dmax = Math.max(...segs.map((s) => s.d)) || 1, lamps = [];
  segs.forEach((s) => { for (let i = 1; i < s.length; i += 2) lamps.push([s[i][0], s[i][1], s.d]); });
  return (C._net = { segs, dmax, lamps });
}
TPL.map = (p) => { const C = cityOf(p), net = buildNet(C, p.seed);
  const cams = p.cam || [{ t: p.t0, z: 1, c: C.center }];
  const camAt = (t) => { let i = 0; while (i < cams.length - 2 && t >= cams[i + 1].t) i++; const a = cams[i], b = cams[i + 1] || a, u = b === a ? 0 : sm(pr(t, a.t, b.t));
    return { z: Math.exp(lerp(Math.log(a.z), Math.log(b.z), u)), c: [lerp(a.c[0], b.c[0], u), lerp(a.c[1], b.c[1], u)] }; };
  const bridges = (C.bridges || []).filter((b) => b.y <= (p.year || 9999));
  return { kind: 'card', content(g, t, w, h) {
    const cm = camAt(t), k = C.pxkm * cm.z * (LL.fmt === '9x16' ? 0.75 : 1), S = (x, y) => [w / 2 + (x - cm.c[0]) * k, h / 2 + (y - cm.c[1]) * k];
    const grow = p.grow || [p.t0 + 0.5, p.t0 + 4], gu = eo(rv(t, grow[0], grow[1] - grow[0]));
    g.save(); g.lineCap = 'round'; g.lineJoin = 'round';
    // nước
    g.fillStyle = 'rgba(63,90,122,0.20)'; g.strokeStyle = 'rgba(63,90,122,0.55)';
    if (C.land) { g.fillRect(0, 0, w, h); g.beginPath(); C.land.forEach(([x, y], i) => (i ? g.lineTo(...S(x, y)) : g.moveTo(...S(x, y)))); g.closePath(); g.save(); g.fillStyle = 'rgba(236,223,190,0.85)'; g.fill(); g.restore(); g.lineWidth = 2.5; g.stroke(); }
    for (const r of C.rivers || []) { const sm_ = r.sm || (r.sm = smoothLine(r.pts)); g.lineWidth = r.w * k; g.strokeStyle = 'rgba(63,90,122,0.24)'; g.beginPath(); sm_.forEach(([x, y], i) => (i ? g.lineTo(...S(x, y)) : g.moveTo(...S(x, y)))); g.stroke();
      g.lineWidth = 2; g.strokeStyle = 'rgba(63,90,122,0.6)'; for (const sg of [-1, 1]) { g.beginPath(); sm_.forEach(([x, y], i) => { const q = sm_[Math.min(i + 1, sm_.length - 1)], pq = sm_[Math.max(i - 1, 0)], dx = q[0] - pq[0], dy = q[1] - pq[1], L = Math.hypot(dx, dy) || 1;
        const pt = S(x - dy / L * sg * r.w / 2, y + dx / L * sg * r.w / 2); i ? g.lineTo(...pt) : g.moveTo(...pt); }); g.stroke(); } }
    // phố
    g.strokeStyle = SEPIA; g.lineWidth = Math.max(1.4, 0.03 * k);
    for (const s of net.segs) { const a = cl((gu * net.dmax * 1.05 - s.d) / (0.12 * net.dmax)); if (a <= 0) continue; g.globalAlpha = a; g.beginPath(); s.forEach(([x, y], i) => (i ? g.lineTo(...S(x, y)) : g.moveTo(...S(x, y)))); g.stroke(); }
    g.globalAlpha = 1;
    // cầu có thật ở năm của bản đồ
    for (const b of bridges) { const [x, y] = b.at, r = (C.rivers || [])[0]; let ang = Math.PI / 2;
      if (r) { const sm_ = r.sm; let bi = 0, bd = 1e9; sm_.forEach(([qx, qy], i) => { const d = Math.hypot(qx - x, qy - y); if (d < bd) { bd = d; bi = i; } }); const q = sm_[Math.min(bi + 1, sm_.length - 1)], pq = sm_[Math.max(bi - 1, 0)]; ang = Math.atan2(q[1] - pq[1], q[0] - pq[0]) + Math.PI / 2; }
      const L = ((r ? r.w : 0.3) / 2 + 0.08) * k, [cx, cy] = S(x, y); g.save(); g.globalAlpha = rv(t, grow[0], 0.8); g.strokeStyle = BROWN; g.lineWidth = Math.max(3, 0.06 * k);
      g.beginPath(); g.moveTo(cx - Math.cos(ang) * L, cy - Math.sin(ang) * L); g.lineTo(cx + Math.cos(ang) * L, cy + Math.sin(ang) * L); g.stroke(); g.restore(); }
    // đèn dọc phố
    if (p.lampsLit) { const lu = pr(t, p.lampsLit[0], p.lampsLit[1]); if (lu > 0) LL.act = LL.act || lu < 1;
      for (const [x, y, d] of net.lamps) { const a = cl((lu * net.dmax * 1.05 - d) / (0.1 * net.dmax)); if (a <= 0) continue; const [sx, sy] = S(x, y); if (sx < -20 || sy < -20 || sx > w + 20 || sy > h + 20) continue;
        g.globalAlpha = a; g.fillStyle = 'rgba(214,128,44,0.9)'; g.beginPath(); g.arc(sx, sy, Math.max(1.6, 0.03 * k), 0, 7); g.fill(); } g.globalAlpha = 1; }
    g.restore();
    for (const pn of p.pins || []) { const [sx, sy] = S(...pn.at), a = rv(t, pn.t, 0.6); if (a <= 0) continue; glow(g, sx, sy, 40, RGB_AMB, 0.5 * a); g.save(); g.globalAlpha *= a; g.fillStyle = AMBER; g.beginPath(); g.arc(sx, sy, 9, 0, 7); g.fill(); g.restore();
      if (pn.s) tag(g, pn.s, sx + 18, sy - 26, 30 * K, 'rgba(236,223,190,0.94)', INK, { a }); }
    for (const lb of p.labels || []) { const [sx, sy] = S(...lb.at); tag(g, lb.s, sx, sy, 30 * K, 'rgba(236,223,190,0.92)', INK, { a: rv(t, lb.t === undefined ? grow[0] + 1 : lb.t, 0.6), align: 'center' }); }
    if (p.title) { tag(g, p.title, PAD - 20, 70 * K, 44 * K, 'rgba(236,223,190,0.94)', INK, { a: rv(t, p.t0 + 0.2, 0.7) }); }
    if (p.year) tag(g, String(p.year), w - PAD + 20, 70 * K, 44 * K, 'rgba(236,223,190,0.94)', INK, { a: rv(t, p.t0 + 0.5, 0.7), align: 'right' });
    footer(g, t, p, w, h);
  } }; };

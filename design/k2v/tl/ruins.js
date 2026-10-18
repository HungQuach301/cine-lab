// K2V tl · V6 (V2D-3, lệnh P3 chủ dự án 18/10): PHỐ ĐỔ NÁT 1782 cho khối LẤP ƯỚC TÍNH nằm trong vùng bản đồ ghi "THE RUINS OF GIBRALTAR"
//  (Drinkwater 1786, Plan of the Batteries, IA historyoflatesie00drin leaf 373 — chữ lớn trên phố; vùng: data/ruins-zone-1782.json, nắn affine của SH, sai 0,02 m).
//  Bằng chứng trạng thái: S062 (12/4/1781 pháo kích, dân bỏ chạy về nam) + S063 (14/4/1781 cháy nhà gần Spanish Church) — Drinkwater 1785.
//  Dựng: tường bao không mái, đỉnh vỡ răng cưa (cao 1–6 m, vài mảng 7 m), mảng khuyết; 1–2 vách ngăn; đống gạch đá + mảnh ngói dồn chân tường và giữa lô; dầm cháy gác chéo;
//  vôi trắng loang ám khói ở đỉnh tường, mảng đá lộ. Tất định (rng). Là "estimated" — cảnh hiện dòng "Ruins: estimated".
import { THREE, rng, maskify } from './core.js';

export function pipRing(p, r) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > p[1]) !== (r[j][1] > p[1]) && p[0] < (r[j][0] - r[i][0]) * (p[1] - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; }
const cen = (r) => [r.reduce((s, q) => s + q[0], 0) / r.length, r.reduce((s, q) => s + q[1], 0) / r.length];

export function ruins(recs, ctx, { seed = 1781, hid = 0 } = {}) {
  const P = [], C = [], R = rng(seed), hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3), stat = { lo: 0, tuong_m: 0, dong_gach: 0, dam: 0, m2: 0 };
  const push = (a, b, c, col) => { P.push(a[0], a[1], -a[2], b[0], b[1], -b[2], c[0], c[1], -c[2]); C.push(...col, ...col, ...col); };
  const quad = (a, b, c, d, col) => { push(a, b, c, col); push(a, c, d, col); };
  const lime = [0.80, 0.76, 0.66], stone = [0.55, 0.49, 0.40], soot = [0.20, 0.18, 0.16], rub = [[0.50, 0.45, 0.37], [0.42, 0.38, 0.32], [0.55, 0.28, 0.17], [0.60, 0.55, 0.46]];
  const shade = (c, k) => c.map((v) => v * k);
  // tường dày t từ A→B (ENU), chân y0, đỉnh theo đoạn (răng cưa); mặt ngoài vôi, mặt trong đá lộ; đỉnh vỡ ám khói
  function wall(A, B, y0, t, hmax) {
    const L = Math.hypot(B[0] - A[0], B[1] - A[1]); if (L < 0.8) return; const u = [(B[0] - A[0]) / L, (B[1] - A[1]) / L], nrm = [-u[1] * t / 2, u[0] * t / 2];
    let s = 0; while (s < L) { const ls = Math.min(L - s, 1.2 + R() * 3.2); const gap = R() < 0.16; if (!gap) {
        const h0 = 0.8 + Math.pow(R(), 0.7) * hmax, h1 = Math.max(0.6, h0 + (R() - 0.5) * 2.2), p0 = [A[0] + u[0] * s, A[1] + u[1] * s], p1 = [A[0] + u[0] * (s + ls), A[1] + u[1] * (s + ls)];
        const o0 = [p0[0] + nrm[0], p0[1] + nrm[1]], o1 = [p1[0] + nrm[0], p1[1] + nrm[1]], i0 = [p0[0] - nrm[0], p0[1] - nrm[1]], i1 = [p1[0] - nrm[0], p1[1] - nrm[1]];
        const k = 0.85 + 0.25 * R(), wc = R() < 0.25 ? stone : lime, top = (y) => y;
        // mặt ngoài: chia 2 dải — dưới vôi/đá, trên 0,8 m ám khói
        const ya = y0 + h0, yb = y0 + h1, ma = ya - 0.8, mb = yb - 0.8;
        quad([o0[0], y0 - 0.3, o0[1]], [o1[0], y0 - 0.3, o1[1]], [o1[0], mb, o1[1]], [o0[0], ma, o0[1]], shade(wc, k));
        quad([o0[0], ma, o0[1]], [o1[0], mb, o1[1]], [o1[0], top(yb), o1[1]], [o0[0], top(ya), o0[1]], shade(soot, 1.2 + 0.6 * R()));
        quad([i1[0], y0 - 0.3, i1[1]], [i0[0], y0 - 0.3, i0[1]], [i0[0], ya, i0[1]], [i1[0], yb, i1[1]], shade(stone, 0.8 * k));
        quad([o0[0], ya, o0[1]], [o1[0], yb, o1[1]], [i1[0], yb, i1[1]], [i0[0], ya, i0[1]], shade(stone, 0.95));   // đỉnh vỡ
        quad([o0[0], y0, o0[1]], [o0[0], ya, o0[1]], [i0[0], ya, i0[1]], [i0[0], y0, i0[1]], shade(stone, 0.85));   // mép đứt
        quad([i1[0], y0, i1[1]], [i1[0], yb, i1[1]], [o1[0], yb, o1[1]], [o1[0], y0, o1[1]], shade(stone, 0.85));
        stat.tuong_m += ls; segs.push([p0, p1, h0]); }
      s += ls; }
  }
  // đống gạch: GÒ THẤP (cao ≤ 0,35 × bán kính), 12 cạnh × 2 vòng, đỉnh lệch, sườn lồi lõm + đá rời quanh chân + mảnh ngói phẳng
  const segs = [];   // đoạn tường đã dựng (để dồn gạch sát chân tường)
  function rubble(e, n, r, h, col) { const y = hAt(e, n), k = 12; h = Math.min(h, r * 0.38); const top = [e + (R() - 0.5) * r * 0.5, y + h, n + (R() - 0.5) * r * 0.5];
    const o = [], m = []; for (let i = 0; i < k; i++) { const a = i / k * 6.283 + (R() - 0.5) * 0.3, ro = r * (0.75 + 0.45 * R()), rm = ro * (0.45 + 0.2 * R()); o.push([e + Math.cos(a) * ro, y - 0.05, n + Math.sin(a) * ro]); m.push([e + Math.cos(a) * rm, y + h * (0.55 + 0.3 * R()), n + Math.sin(a) * rm]); }
    for (let i = 0; i < k; i++) { const j = (i + 1) % k, cc = shade(col, 0.78 + 0.34 * R()); push(o[i], o[j], m[j], cc); push(o[i], m[j], m[i], shade(cc, 1.02)); push(m[i], m[j], top, shade(cc, 1.08)); }
    for (let q = 0; q < 4; q++) { const a = R() * 6.283, d = r * (0.9 + 0.6 * R()), sx = 0.25 + 0.35 * R(), ex = e + Math.cos(a) * d, nx = n + Math.sin(a) * d, yy = hAt(ex, nx), c2 = shade(rub[Math.floor(R() * 4)], 0.8 + 0.3 * R());
      const P4 = [[ex - sx, yy, nx - sx * 0.7], [ex + sx, yy, nx - sx * 0.6], [ex + sx * 0.8, yy, nx + sx * 0.7], [ex - sx * 0.7, yy, nx + sx * 0.8]], T = [ex, yy + sx * 0.9, nx]; for (let i = 0; i < 4; i++) push(P4[i], P4[(i + 1) % 4], T, c2); }
    stat.dong_gach++; }
  function tiles(e, n, r) { const y = hAt(e, n) + 0.04; for (let q = 0; q < 5; q++) { const a = R() * 6.283, d = r * R(), ex = e + Math.cos(a) * d, nx = n + Math.sin(a) * d, s1 = 0.3 + 0.4 * R(), b = R() * 3.1;
      const c = shade(rub[2], 0.8 + 0.4 * R()), p0 = [ex + Math.cos(b) * s1, y + 0.05 * R(), nx + Math.sin(b) * s1], p1 = [ex + Math.cos(b + 2.1) * s1, y, nx + Math.sin(b + 2.1) * s1], p2 = [ex + Math.cos(b + 4.2) * s1, y + 0.08, nx + Math.sin(b + 4.2) * s1]; push(p0, p1, p2, c); push(p0, p2, p1, c); } }
  function beam(e, n, L, rot, tilt) { const y = hAt(e, n), c = Math.cos(rot), s = Math.sin(rot), w = 0.22, p0 = [e, y + 0.1, n], p1 = [e + c * L * Math.cos(tilt), y + L * Math.sin(tilt), n + s * L * Math.cos(tilt)], o = [-s * w, c * w];
    quad([p0[0] - o[0], p0[1], p0[2] - o[1]], [p1[0] - o[0], p1[1], p1[2] - o[1]], [p1[0] - o[0], p1[1] + w, p1[2] - o[1]], [p0[0] - o[0], p0[1] + w, p0[2] - o[1]], soot);
    quad([p0[0] + o[0], p0[1] + w, p0[2] + o[1]], [p1[0] + o[0], p1[1] + w, p1[2] + o[1]], [p1[0] + o[0], p1[1], p1[2] + o[1]], [p0[0] + o[0], p0[1], p0[2] + o[1]], shade(soot, 0.8));
    quad([p0[0] - o[0], p0[1] + w, p0[2] - o[1]], [p1[0] - o[0], p1[1] + w, p1[2] - o[1]], [p1[0] + o[0], p1[1] + w, p1[2] + o[1]], [p0[0] + o[0], p0[1] + w, p0[2] + o[1]], shade(soot, 1.3)); stat.dam++; }
  for (const r of recs) {
    const ring = r[6]; if (!ring || ring.length < 3) continue; stat.lo++; const y0 = Math.min(...ring.map(([e, n]) => hAt(e, n))), hmax = 4.5 + 3.0 * R();
    stat.m2 += Math.abs(ring.reduce((a, p, i) => a + p[0] * ring[(i + 1) % ring.length][1] - ring[(i + 1) % ring.length][0] * p[1], 0)) / 2;
    const segStart = segs.length;
    for (let i = 0; i < ring.length; i++) { const A = ring[i], B = ring[(i + 1) % ring.length]; wall(A, B, y0, 0.6, hmax); }
    // vách ngăn: lô lấp là KHỐI lớn → chia lưới phòng/nhà ~7 × 9 m theo hai trục (đọc như dãy nhà đổ), mỗi đoạn có khuyết
    const c = cen(ring), xs = ring.map((p) => p[0]), ys = ring.map((p) => p[1]), we = Math.max(...xs) - Math.min(...xs), wn = Math.max(...ys) - Math.min(...ys);
    const clip = (a, b) => { const out = []; const n = Math.max(2, Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) / 1.0)); let cur = null;
      for (let i = 0; i <= n; i++) { const q = [a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n], ins = pipRing(q, ring); if (ins && !cur) cur = [q, q]; else if (ins) cur[1] = q; else if (cur) { out.push(cur); cur = null; } } if (cur) out.push(cur); return out; };
    for (let x = Math.min(...xs) + 7 + R() * 2; x < Math.max(...xs) - 3; x += 6.5 + R() * 2.5) for (const [a, b] of clip([x, Math.min(...ys) - 1], [x, Math.max(...ys) + 1])) wall(a, b, y0, 0.5, hmax * (0.6 + 0.4 * R()));
    for (let y = Math.min(...ys) + 9 + R() * 2; y < Math.max(...ys) - 3; y += 8 + R() * 3) for (const [a, b] of clip([Math.min(...xs) - 1, y], [Math.max(...xs) + 1, y])) wall(a, b, y0, 0.5, hmax * (0.6 + 0.4 * R()));
    // gạch đổ: phần lớn dồn SÁT CHÂN TƯỜNG trong lô (tường sập xuống), ít gò giữa lô; mảnh ngói rải
    const per = ring.reduce((a, p, i) => a + Math.hypot(ring[(i + 1) % ring.length][0] - p[0], ring[(i + 1) % ring.length][1] - p[1]), 0), nr = Math.round(per / 5 + we * wn / 160);
    const mine = segs.slice(segStart);
    for (let k = 0; k < nr; k++) { let tries = 0; while (tries++ < 10) { let e, n;
        if (mine.length && R() < 0.75) { const sg = mine[Math.floor(R() * mine.length)], u = R(), side = R() < 0.5 ? 1 : -1, d = [sg[1][0] - sg[0][0], sg[1][1] - sg[0][1]], l = Math.hypot(...d) || 1; e = sg[0][0] + d[0] * u - d[1] / l * side * (0.8 + 1.4 * R()); n = sg[0][1] + d[1] * u + d[0] / l * side * (0.8 + 1.4 * R()); }
        else { e = Math.min(...xs) + R() * we; n = Math.min(...ys) + R() * wn; }
        if (!pipRing([e, n], ring)) continue; rubble(e, n, 1.0 + R() * 2.2, 0.4 + R() * 1.0, rub[Math.floor(R() * (R() < 0.3 ? 4 : 2))]); if (R() < 0.4) tiles(e, n, 2.5); break; } }
    for (let k = 0; k < Math.max(1, Math.round(nr / 5)); k++) { const e = c[0] + (R() - 0.5) * we * 0.6, n = c[1] + (R() - 0.5) * wn * 0.6; if (pipRing([e, n], ring)) beam(e, n, 3 + R() * 3, R() * 6.28, 0.2 + R() * 0.5); }
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); maskify(m, ctx.U, 1, hid);
  const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true; const group = new THREE.Group(); group.add(o);
  stat.tuong_m = Math.round(stat.tuong_m); stat.m2 = Math.round(stat.m2);
  return { group, stat };
}

// K2V tl · V5b-2c · M5 THÀNH LUỸ THAM SỐ (lệnh V0 chủ dự án 18/10: "công trình hero King's Bastion là tấm be phẳng").
// Từ footprint (vòng ENU, nguồn OSM/ghost SH) dựng một công sự kiểu bastion thế kỷ 18, mọi kích thước là THAM SỐ (không mô phỏng chi tiết từng công trình):
//   · tường dốc (escarp) ốp đá khối: mặt trên lùi vào batter·h (≈ 1:8), vân đá khối theo hàng 0,55 m × 1,1 m so le, mạch vữa, loang ẩm chân tường, vệt nước mưa;
//   · gờ (cordon) tròn nhô 0,35 m ở đỉnh tường dốc — nét sáng chạy quanh luỹ, đọc được hình khối ở xa;
//   · tường chắn (parapet) dày 3 m: phần dưới liền tới đế lỗ châu mai, phần trên là các khối merlon giữa lỗ châu mai (mở loe vào trong);
//   · sàn pháo (terreplein) lát đá tấm 1,2 m có vết ố;
//   · KHẨU PHÁO ở mỗi lỗ châu mai: bệ gỗ bốn bánh kiểu hải quân + nòng gang chĩa ra ngoài (cỡ minh hoạ, không theo sổ pháo);
//   · chòi gác (garita) tròn mái vòm ở các góc lồi — đặc trưng công sự Gibraltar/Tây Ban Nha; đống đạn tròn xếp tháp sau vài khẩu.
// Khai trong cảnh: fortify(recs, ctx, {hid, h, embr, guns, garita}) — recs như footprints (phần tử 6 = vòng, 3 = cốt chân, 2 = cao).
// Mặt nạ: toàn bộ là NỘI DUNG (maskify v = 1, id hero hid). Không Math.random (rng tất định).
import { THREE, rng, maskify } from './core.js';

const KIND = { wall: 0, cordon: 1, ptop: 2, floor: 3, iron: 4, wood: 5, garita: 6, shot: 7, pinner: 8, plank: 9 };

function orient(ring) { let a = 0; for (let i = 0; i < ring.length; i++) { const p = ring[i], q = ring[(i + 1) % ring.length]; a += p[0] * q[1] - q[0] * p[1]; } return a > 0 ? 1 : -1; }   // +1 = ngược chiều kim đồng hồ (E bên phải, N lên)
function clean(ring) { const r = ring.slice(); if (r.length > 2 && r[0][0] === r[r.length - 1][0] && r[0][1] === r[r.length - 1][1]) r.pop();
  const out = []; for (const p of r) { const q = out[out.length - 1]; if (!q || Math.hypot(p[0] - q[0], p[1] - q[1]) > 0.8) out.push(p); } return out; }
// lùi vòng vào trong d m (miter, giới hạn 2,5 d ở góc nhọn) — vòng đã clean, hướng s
function inset(ring, d, s) {
  const n = ring.length, out = [];
  for (let i = 0; i < n; i++) { const a = ring[(i - 1 + n) % n], p = ring[i], b = ring[(i + 1) % n];
    const e1 = [p[0] - a[0], p[1] - a[1]], e2 = [b[0] - p[0], b[1] - p[1]], l1 = Math.hypot(...e1) || 1, l2 = Math.hypot(...e2) || 1;
    const n1 = [-e1[1] / l1 * s, e1[0] / l1 * s], n2 = [-e2[1] / l2 * s, e2[0] / l2 * s];   // pháp tuyến hướng vào trong
    let m = [n1[0] + n2[0], n1[1] + n2[1]]; const ml = Math.hypot(...m) || 1; m = [m[0] / ml, m[1] / ml]; const cos = Math.max(0.4, m[0] * n1[0] + m[1] * n1[1]);
    out.push([p[0] + m[0] * d / cos, p[1] + m[1] * d / cos]); }
  return out;
}

export function fortify(recs, ctx, o = {}) {
  const P = [], K = [], UV = [], R = rng(o.seed || 53), stat = { luy: 0, lo_chau_mai: 0, phao: 0, garita: 0, dan: 0 };
  const tri = (a, b, c, k, ua, ub, uc) => { P.push(...a, ...b, ...c); K.push(k, k, k); UV.push(...(ua || [0, 0]), ...(ub || [0, 0]), ...(uc || [0, 0])); };
  const quad = (a, b, c, d, k, u0 = 0, u1 = 1) => { tri(a, b, c, k, [u0, a[1]], [u1, b[1]], [u1, c[1]]); tri(a, c, d, k, [u0, a[1]], [u1, c[1]], [u0, d[1]]); };
  const V = (e, y, n) => [e, y, -n];
  const box = (cx, cy, cn, L, H, W, rot, k) => {   // hộp tâm đáy (cx, cy, cn), dài L theo hướng rot (rad, ENU), cao H, rộng W
    const c = Math.cos(rot), s = Math.sin(rot), pt = (x, z) => [cx + c * x - s * z, cn + s * x + c * z], q = [pt(-L / 2, -W / 2), pt(L / 2, -W / 2), pt(L / 2, W / 2), pt(-L / 2, W / 2)];
    for (let i = 0; i < 4; i++) { const a = q[i], b = q[(i + 1) % 4]; quad(V(a[0], cy, a[1]), V(b[0], cy, b[1]), V(b[0], cy + H, b[1]), V(a[0], cy + H, a[1]), k); }
    tri(V(q[0][0], cy + H, q[0][1]), V(q[1][0], cy + H, q[1][1]), V(q[2][0], cy + H, q[2][1]), k); tri(V(q[0][0], cy + H, q[0][1]), V(q[2][0], cy + H, q[2][1]), V(q[3][0], cy + H, q[3][1]), k); };
  const cyl = (cx, cy, cn, r0, r1, len, rot, el, k, seg = 8) => {   // ống tròn từ tâm (cx,cy,cn) dọc hướng rot (ENU rad), ngẩng el
    const d = [Math.cos(rot) * Math.cos(el), Math.sin(el), Math.sin(rot) * Math.cos(el)], up = [0, 1, 0];
    let a = [d[1] * up[2] - d[2] * up[1], d[2] * up[0] - d[0] * up[2], d[0] * up[1] - d[1] * up[0]]; const al = Math.hypot(...a) || 1; a = a.map((v) => v / al);
    const b = [d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0]];
    const ring = (t, r) => Array.from({ length: seg }, (_, i) => { const w = i / seg * 6.2832, x = Math.cos(w) * r, y = Math.sin(w) * r; return [cx + d[0] * t + a[0] * x + b[0] * y, cy + d[1] * t + a[1] * x + b[1] * y, cn + d[2] * t + a[2] * x + b[2] * y]; });
    const A = ring(0, r0), B = ring(len, r1), toV = (p) => [p[0], p[1], -p[2]];
    for (let i = 0; i < seg; i++) { const j = (i + 1) % seg; quad(toV(A[i]), toV(A[j]), toV(B[j]), toV(B[i]), k); tri(toV([cx + d[0] * len, cy + d[1] * len, cn + d[2] * len]), toV(B[i]), toV(B[j]), k); } };
  const dome = (cx, cy, cn, r, k, seg = 10) => { for (let j = 0; j < 3; j++) { const a0 = j / 3 * 1.5708, a1 = (j + 1) / 3 * 1.5708;
    for (let i = 0; i < seg; i++) { const w0 = i / seg * 6.2832, w1 = (i + 1) / seg * 6.2832, p = (w, a) => V(cx + Math.cos(w) * Math.cos(a) * r, cy + Math.sin(a) * r, cn + Math.sin(w) * Math.cos(a) * r);
      quad(p(w0, a0), p(w1, a0), p(w1, a1), p(w0, a1), k); } } };

  for (const rec of recs) {
    const ring = clean(rec[6]); if (ring.length < 3) continue; const s = orient(ring), base = rec[3], h = o.h || rec[2] || 9, n = ring.length;
    const batter = o.batter ?? 0.12, top = inset(ring, h * batter, s), inner = inset(top, o.thick ?? 3.0, s), sole = h + (o.sole ?? 0.95), pt = h + (o.ph ?? 1.9);
    stat.luy++;
    // 1) tường dốc + 2) gờ: theo từng cạnh, toạ độ U = quãng dọc vòng (vân đá liền qua góc)
    let U0 = 0;
    for (let i = 0; i < n; i++) { const a = ring[i], b = ring[(i + 1) % n], ta = top[i], tb = top[(i + 1) % n], L = Math.hypot(b[0] - a[0], b[1] - a[1]);
      // đế tường đi xuống 6 m dưới cốt chân (chân luỹ dưới nước / dốc không lộ khe)
      quad(V(a[0], base - 6, a[1]), V(b[0], base - 6, b[1]), V(tb[0], base + h, tb[1]), V(ta[0], base + h, ta[1]), KIND.wall, U0, U0 + L);
      const on = [-(b[1] - a[1]) / L * -s * 0.35, (b[0] - a[0]) / L * -s * 0.35];   // pháp tuyến ra ngoài × 0,35 m
      const c0 = [ta[0] + on[0], ta[1] + on[1]], c1 = [tb[0] + on[0], tb[1] + on[1]];
      quad(V(ta[0], base + h - 0.45, ta[1]), V(tb[0], base + h - 0.45, tb[1]), V(c1[0], base + h - 0.2, c1[1]), V(c0[0], base + h - 0.2, c0[1]), KIND.cordon, U0, U0 + L);
      quad(V(c0[0], base + h - 0.2, c0[1]), V(c1[0], base + h - 0.2, c1[1]), V(c1[0], base + h + 0.15, c1[1]), V(c0[0], base + h + 0.15, c0[1]), KIND.cordon, U0, U0 + L);
      quad(V(c0[0], base + h + 0.15, c0[1]), V(c1[0], base + h + 0.15, c1[1]), V(tb[0], base + h + 0.3, tb[1]), V(ta[0], base + h + 0.3, ta[1]), KIND.cordon, U0, U0 + L);
      // 3) tường chắn: phần dưới liền (h → đế lỗ châu mai), mặt ngoài + mặt trong
      quad(V(ta[0], base + h + 0.3, ta[1]), V(tb[0], base + h + 0.3, tb[1]), V(tb[0], base + sole, tb[1]), V(ta[0], base + sole, ta[1]), KIND.wall, U0, U0 + L);
      const ia = inner[i], ib = inner[(i + 1) % n];
      quad(V(ib[0], base + h, ib[1]), V(ia[0], base + h, ia[1]), V(ia[0], base + sole, ia[1]), V(ib[0], base + sole, ib[1]), KIND.pinner, U0, U0 + L);
      // merlon giữa lỗ châu mai: lỗ mỗi `embr` m (bỏ 3 m sát góc); lỗ loe: ngoài 0,9 m, trong 2,2 m
      // mặt hậu (gorge) quay vào đất liền cao ngang đỉnh luỹ: không lỗ châu mai/pháo, chỉ tường chắn thấp (đo cao độ 18 m ra ngoài giữa cạnh)
      const mid = [(a[0] + b[0]) / 2 + on[0] / 0.35 * 18, (a[1] + b[1]) / 2 + on[1] / 0.35 * 18], gorge = (ctx.terr && ctx.terr.hAt(mid[0], mid[1]) > base + h * 0.55) || (o.face && (on[0] * o.face[0] + on[1] * o.face[1]) / 0.35 < 0.3);   // o.face: chỉ mặt quay về hướng địch có lỗ châu mai
      const step = o.embr ?? 6.5, emb = [];
      if (L > 8 && !gorge) { const k = Math.max(1, Math.floor((L - 6) / step)), sp = (L - 6) / k; for (let j = 0; j <= k; j++) emb.push(3 + j * sp); }
      const at = (A, B, t) => [A[0] + (B[0] - A[0]) * t / L, A[1] + (B[1] - A[1]) * t / L];
      const cuts = [[0, 0, 0, 0]]; for (const e of emb) cuts.push([e - 0.45, e + 0.45, e - 1.1, e + 1.1]); cuts.push([L, L, L, L]);
      for (let j = 0; j < cuts.length - 1; j++) { const o0 = cuts[j][1], o1 = cuts[j + 1][0], i0 = cuts[j][3], i1 = cuts[j + 1][2]; if (o1 - o0 < 0.3) continue;
        const A0 = at(ta, tb, o0), A1 = at(ta, tb, o1), B0 = at(ia, ib, i0), B1 = at(ia, ib, i1), y0 = base + sole, y1 = base + pt, yi = base + pt - 0.35;   // mặt trên dốc nhẹ vào trong
        quad(V(A0[0], y0, A0[1]), V(A1[0], y0, A1[1]), V(A1[0], y1, A1[1]), V(A0[0], y1, A0[1]), KIND.wall, U0 + o0, U0 + o1);
        quad(V(B1[0], y0, B1[1]), V(B0[0], y0, B0[1]), V(B0[0], yi, B0[1]), V(B1[0], yi, B1[1]), KIND.pinner, U0 + i1, U0 + i0);
        quad(V(A0[0], y1, A0[1]), V(A1[0], y1, A1[1]), V(B1[0], yi, B1[1]), V(B0[0], yi, B0[1]), KIND.ptop);
        quad(V(B0[0], y0, B0[1]), V(A0[0], y0, A0[1]), V(A0[0], y1, A0[1]), V(B0[0], yi, B0[1]), KIND.pinner);   // má lỗ châu mai
        quad(V(A1[0], y0, A1[1]), V(B1[0], y0, B1[1]), V(B1[0], yi, B1[1]), V(A1[0], y1, A1[1]), KIND.pinner); }
      // đế lỗ châu mai (mặt ngang) dọc cả cạnh
      quad(V(ta[0], base + sole, ta[1]), V(tb[0], base + sole, tb[1]), V(ib[0], base + sole, ib[1]), V(ia[0], base + sole, ia[1]), KIND.ptop);
      // 5) khẩu pháo ở mỗi lỗ: bệ + 4 bánh + nòng chĩa ra (hướng pháp tuyến ngoài của cạnh)
      const outRot = Math.atan2(on[1], on[0]);
      for (const e of emb) { stat.lo_chau_mai++; if (o.guns === false || (o.gunEvery && (stat.lo_chau_mai % o.gunEvery))) continue;
        const m = at(ia, ib, e), gx = m[0] - on[0] / 0.35 * 1.6, gn = m[1] - on[1] / 0.35 * 1.6, gy = base + h;
        box(gx - Math.cos(outRot) * 0.6, gy, gn - Math.sin(outRot) * 0.6, 4.2, 0.14, 3.2, outRot, KIND.plank);   // sàn gỗ ván dưới pháo (platform)
        box(gx, gy + 0.32, gn, 1.7, 0.55, 0.9, outRot, KIND.wood);
        for (const [x, z] of [[-0.6, -0.5], [0.6, -0.5], [-0.6, 0.5], [0.6, 0.5]]) { const c = Math.cos(outRot), sn = Math.sin(outRot); box(gx + c * x - sn * z, gy, gn + sn * x + c * z, 0.5, 0.5, 0.18, outRot, KIND.wood); }
        cyl(gx - Math.cos(outRot) * 0.6, gy + 1.05, gn - Math.sin(outRot) * 0.6, 0.24, 0.17, 2.9, outRot, 0.03, KIND.iron); stat.phao++;
        if (R() < 0.35) { const bx = gx - Math.cos(outRot) * 2.6, bn = gn - Math.sin(outRot) * 2.6; for (let lv = 0; lv < 3; lv++) for (let q = 0; q < 3 - lv; q++) box(bx + (q - (2 - lv) / 2) * 0.32, gy + lv * 0.27, bn, 0.27, 0.27, 0.27, outRot, KIND.shot); stat.dan++; } }
      U0 += L;
    }
    // 4) sàn pháo
    const tr = THREE.ShapeUtils.triangulateShape(inner.map(([x, y]) => new THREE.Vector2(x, y)), []);
    for (const [a, b, c] of tr) { const A = inner[a], B = inner[b], C = inner[c]; tri(V(A[0], base + h, A[1]), V(B[0], base + h, B[1]), V(C[0], base + h, C[1]), KIND.floor); }
    // 6) chòi gác ở góc lồi nhọn (< 125°), nhô 0,6 m ra ngoài, trên đỉnh tường chắn
    if (o.garita !== false) for (let i = 0; i < n; i++) { const a = ring[(i - 1 + n) % n], p = ring[i], b = ring[(i + 1) % n];
      const e1 = [p[0] - a[0], p[1] - a[1]], e2 = [b[0] - p[0], b[1] - p[1]], cr = (e1[0] * e2[1] - e1[1] * e2[0]) * s, ang = Math.acos(Math.max(-1, Math.min(1, -(e1[0] * e2[0] + e1[1] * e2[1]) / ((Math.hypot(...e1) * Math.hypot(...e2)) || 1)))) * 57.3;
      if (cr >= 0 || ang > 125 || Math.hypot(...e1) < 10 || Math.hypot(...e2) < 10) continue;   // chỉ góc lồi, nhọn, cạnh đủ dài
      const t = top[i], dir = [t[0] - inner[i][0], t[1] - inner[i][1]], dl = Math.hypot(...dir) || 1, g = [t[0] + dir[0] / dl * 0.4, t[1] + dir[1] / dl * 0.4], y0 = base + h + 0.2;
      cyl(g[0], y0 - 1.1, g[1], 0.35, 1.05, 1.1, 0, 1.5708, KIND.garita); cyl(g[0], y0, g[1], 1.05, 1.05, 2.5, 0, 1.5708, KIND.garita, 12); dome(g[0], y0 + 2.5, g[1], 1.15, KIND.garita); stat.garita++; }
  }
  // hình học → BufferGeometry (pháp tuyến phẳng theo tam giác)
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('aK', new THREE.Float32BufferAttribute(K, 1)); g.setAttribute('aUV', new THREE.Float32BufferAttribute(UV, 2)); g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ color: 0xffffff, side: THREE.DoubleSide }), seedC = (o.seed || 53) * 0.37;
  m.customProgramCacheKey = () => 'tl-fort';
  m.onBeforeCompile = (sh) => {
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aK; attribute vec2 aUV; varying float vK; varying vec2 vUV; varying vec3 vWPf;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvK = aK; vUV = aUV; vWPf = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
      varying float vK; varying vec2 vUV; varying vec3 vWPf;
      float hf(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      float vnf(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f); return mix(mix(hf(i), hf(i + vec2(1, 0)), f.x), mix(hf(i + vec2(0, 1)), hf(i + vec2(1, 1)), f.x), f.y); }
      // đá vôi Gibraltar: khối mật ong ↔ xám tro, mạch vữa sáng-tối, loang ẩm chân tường, vệt nước mưa dọc
      vec3 ashlar(vec2 q, float wet){ float row = floor(q.y / 0.55); vec2 b = vec2((q.x + 0.55 * mod(row, 2.0)) / 1.1, q.y / 0.55); vec2 id = floor(b), f = fract(b);
        float aa = clamp(length(fwidth(b)) * 1.5, 0.0, 1.0), j = (1.0 - aa) * (1.0 - smoothstep(0.035, 0.07, min(min(f.x, 1.0 - f.x) * 0.5, min(f.y, 1.0 - f.y))));
        float r = hf(id + ${seedC.toFixed(3)}); vec3 c = mix(vec3(0.86, 0.64, 0.38), vec3(0.76, 0.66, 0.50), smoothstep(0.35, 0.95, r)); c = mix(c, vec3(0.90, 0.72, 0.44), step(0.86, r) * 0.7);   // V5b-2c (I5): đá vôi mật ong ấm hơn
        c *= 0.90 + 0.16 * vnf(q * 2.3 + id) ;   // mặt đá sần
        c = mix(c, vec3(0.42, 0.37, 0.30), j * 0.75);
        c *= 1.0 - 0.22 * smoothstep(0.55, 0.85, vnf(vec2(q.x * 0.6, q.y * 0.08)));   // vệt nước mưa dọc
        c = mix(c, vec3(0.40, 0.42, 0.30), wet);   // rêu/ẩm chân tường
        return c; }`)
      .replace('#include <color_fragment>', `#include <color_fragment>
      { int k = int(vK + 0.5); vec3 c;
        if (k == 0 || k == 8) { float wet = 0.55 * (1.0 - smoothstep(0.0, 2.2, vWPf.y)) * (k == 0 ? 1.0 : 0.0); c = ashlar(vec2(vUV.x, vWPf.y), wet); if (k == 8) c *= 0.92; }
        else if (k == 1) c = vec3(0.92, 0.84, 0.68) * (0.92 + 0.1 * vnf(vec2(vUV.x * 1.5, 0.0)));   // gờ đá sáng
        else if (k == 2) c = vec3(0.82, 0.68, 0.48) * (0.88 + 0.16 * vnf(vWPf.xz * 1.7));
        else if (k == 3) { vec2 p = vWPf.xz; vec2 g = abs(fract(p / 1.2 + vec2(0.0, 0.5 * step(0.5, fract(p.x / 2.4)))) - 0.5); float aa = clamp(length(fwidth(p)) * 1.5, 0.0, 1.0);
          float jt = (1.0 - aa) * step(0.46, max(g.x, g.y)); c = mix(vec3(0.80, 0.60, 0.36), vec3(0.70, 0.55, 0.38), vnf(floor(p / 1.2) * 3.1)) * (0.86 + 0.2 * vnf(p * 0.35));
          c *= 1.0 - 0.12 * jt; c *= 1.0 - 0.18 * smoothstep(0.6, 0.85, vnf(p * 0.08)); }   // sàn pháo lát tấm + vết ố
        else if (k == 4) c = vec3(0.10, 0.10, 0.11);   // gang
        else if (k == 5) c = vec3(0.42, 0.27, 0.15) * (0.85 + 0.2 * vnf(vWPf.xz * 4.0));   // gỗ bệ pháo
        else if (k == 9) { float pl = step(0.5, fract(dot(vWPf.xz, vec2(0.7071)) * 3.3)); c = mix(vec3(0.55, 0.40, 0.24), vec3(0.48, 0.34, 0.20), pl) * (0.85 + 0.2 * vnf(vWPf.xz * 2.0)); }
        else if (k == 6) c = vec3(0.90, 0.80, 0.62) * (0.92 + 0.12 * vnf(vec2(atan(vWPf.x, vWPf.z) * 4.0, vWPf.y * 3.0)));
        else c = vec3(0.16, 0.15, 0.15);
        diffuseColor.rgb = c; }`);
  };
  maskify(m, ctx.U, 1, o.hid || 0);
  const mesh = new THREE.Mesh(g, m); mesh.castShadow = mesh.receiveShadow = true;
  const group = new THREE.Group(); group.add(mesh);
  return { group, stat, update() {} };
}

// tường thành dọc tuyến (Line Wall…): đệm tuyến thành dải dày `thick` → vòng → fortify (lỗ châu mai, gờ, đá khối như luỹ)
//  thickL/thickR: bề dày về bên trái/phải tuyến (bên đất liền dày hơn = mặt thành đắp/terreplein sau tường — Line Wall có lớp đất đắp phía phố)
export function wallRing(pts, thickL = 3.5, thickR = thickL) {
  const L = [], R_ = [];
  for (let i = 0; i < pts.length; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1, nn = [-d[1] / l, d[0] / l];
    L.push([pts[i][0] + nn[0] * thickL, pts[i][1] + nn[1] * thickL]); R_.push([pts[i][0] - nn[0] * thickR, pts[i][1] - nn[1] * thickR]); }
  return L.concat(R_.reverse());
}

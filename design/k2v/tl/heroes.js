// K2V tl · CÔNG TRÌNH BIỂU TƯỢNG (lớp 1 chuẩn hình) — dựng chi tiết riêng theo số đo có nguồn (design/k2v/tl/heroes/*.json):
//  · Tower of Homage (Moorish Castle): vòng chân OSM way 950058970 (334 m², nguồn ghi 320 m² — lệch 4 %), cao 23 m (Ministry for Heritage, Gibraltar);
//    tường tapia (lớp đầm ~0,85 m, lỗ giằng ván), lỗ châu mai, răng cưa đỉnh; tường thành lâu đài (OSM barrier=city_wall).
//  · Đường băng 09/27 cắt ngang đường vào: tim OSM way 157316482 (1 798 × 45 m); có từ 1941 (HMGoG 177/2023), phần lấn vịnh khai hoang 1941–1943
//    (HMGoG 199/2018); vạch sơn theo ICAO Annex 14 (ngưỡng phím đàn 30 × 1,8 m, số hiệu, tim 30 m / khe 20 m, mép, điểm ngắm) — vẽ trên kết cấu canvas.
//  · Tường thành thành phố (Line Wall, Charles V…): OSM historic=citywalls, cao ~6 m (ước), có từ trước 1704 (ước, ghi trong báo cáo).
import { THREE, GLSL_NOISE, GLSL_YEAR, rng } from './core.js';
import { walls, roof } from './geom.js';
import { GLSL_LAND } from './terrain.js';

const TAPIA = `${GLSL_NOISE}
uniform float uYearH;
vec3 tapia(vec3 wp, vec3 n, float ly){ vec3 c = vec3(0.80, 0.62, 0.42);   // tapia: vữa vôi + cát đỏ, gạch gốm nghiền (ấm, đất)
  float age = 0.35 + 0.65 * smoothstep(1700.0, 2026.0, uYearH);   // V5b-1b: loang theo NĂM (vệt mưa, rêu chân tường đậm dần)
  c *= 0.94 + 0.12 * step(0.5, fract(floor(ly / 0.85) * 0.37 + floor((abs(n.x) > abs(n.z) ? wp.z : wp.x) / 3.2) * 0.21));   // mỗi mẻ đầm một tông (lớp có lớp)
  float course = smoothstep(0.0, 0.05, abs(fract(ly / 0.85) - 0.5) - 0.42);   // vạch giữa các lớp đầm
  c *= 1.0 - 0.22 * course; float u = abs(n.x) > abs(n.z) ? wp.z : wp.x;
  vec2 pl = vec2(fract(u / 1.6), fract(ly / 0.85)); float hole = step(0.47, pl.x) * step(pl.x, 0.53) * step(0.03, pl.y) * step(pl.y, 0.14);
  c *= 1.0 - 0.35 * hole; c *= 0.86 + 0.20 * fbm(vec2(u * 0.35, ly * 0.9)); c *= 0.82 + 0.18 * smoothstep(0.0, 6.0, ly);
  c = mix(c, c * vec3(0.78, 0.76, 0.72), age * smoothstep(0.45, 0.9, fbm(vec2(u * 0.35, ly * 0.03 + 3.0))));   // vệt mưa chảy dọc
  c = mix(c, vec3(0.42, 0.44, 0.30), age * 0.35 * (1.0 - smoothstep(0.0, 2.5, ly)) * smoothstep(0.4, 0.7, fbm(vec2(u * 0.5, ly))));   // rêu/ẩm chân tường
  c = mix(c, vec3(0.86, 0.74, 0.58), step(1995.0, uYearH) * 0.5 * smoothstep(0.66, 0.72, fbm(vec2(u * 0.05 + 11.0, ly * 0.05))));   // mảng trát tu bổ (sau 1995, tông nhạt)
  return c; }`;

function stoneMat(U, hiU, kind) {
  const m = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.93 });
  m.customProgramCacheKey = () => 'tl-stone-' + kind;   // V5b-1b: 'lime' và 'tapia' cùng mã nguồn onBeforeCompile → phải khác khoá, nếu không three dùng chung một shader
  m.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uDim: U.uDim, uHi: hiU, uYearH: U.uYear });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aLY; varying float vLY; varying vec3 vWPh; varying vec3 vWNh;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\n vLY = aLY; vWPh = (modelMatrix * vec4(transformed,1.0)).xyz; vWNh = normalize(mat3(modelMatrix) * objectNormal);');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\nuniform float uDim, uHi; varying float vLY; varying vec3 vWPh; varying vec3 vWNh; ${TAPIA}`)
      .replace('#include <color_fragment>', `#include <color_fragment>
      vec3 c = ${kind === 'lime' ? 'mix(vec3(0.74, 0.71, 0.63), vec3(0.62,0.60,0.55), smoothstep(0.4,0.8,fbm(vWPh.xz*0.07 + vLY*0.2)))' : 'tapia(vWPh, vWNh, vLY)'};
      { vec3 Vd = normalize(cameraPosition - vWPh); float rim = pow(1.0 - abs(dot(normalize(vWNh), Vd)), 2.5);   // viền sáng Fresnel khi nhấn hero
        c = mix(c, vec3(1.0, 0.84, 0.50), 0.18 * uHi) + vec3(1.0, 0.78, 0.35) * rim * 0.9 * uHi; }
      float L = dot(c, vec3(0.299,0.587,0.114)); c = mix(c, vec3(L), 0.55 * uDim * (1.0 - uHi)) * (1.0 - 0.36 * uDim * (1.0 - uHi));
      diffuseColor.rgb = c;`); };
  return m;
}
const geoFrom = (A) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(A.p, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(A.n, 3)); g.setAttribute('aLY', new THREE.Float32BufferAttribute(A.l, 1)); return g; };
const acc = () => ({ p: [], n: [], l: [] });
const push = (A, base) => (x, y, z, nx, ny, nz) => { A.p.push(x, y + base, z); A.n.push(nx, ny, nz); A.l.push(y); };
function box(A, cx, cy, cz, w, h, d, rot) {   // hộp đặc (răng cưa, chắn), xoay quanh trục y
  const c = Math.cos(rot), s = Math.sin(rot), V = (x, y, z) => [cx + x * c - z * s, cy + y, cz + x * s + z * c];
  const F = [[[1, 0, 0], [[.5, -.5, -.5], [.5, .5, -.5], [.5, .5, .5], [.5, -.5, .5]]], [[-1, 0, 0], [[-.5, -.5, .5], [-.5, .5, .5], [-.5, .5, -.5], [-.5, -.5, -.5]]],
    [[0, 1, 0], [[-.5, .5, -.5], [-.5, .5, .5], [.5, .5, .5], [.5, .5, -.5]]], [[0, 0, 1], [[.5, -.5, .5], [.5, .5, .5], [-.5, .5, .5], [-.5, -.5, .5]]], [[0, 0, -1], [[-.5, -.5, -.5], [-.5, .5, -.5], [.5, .5, -.5], [.5, -.5, -.5]]]];
  for (const [n, q] of F) { const nn = [n[0] * c - n[2] * s, n[1], n[0] * s + n[2] * c], P = q.map(([x, y, z]) => V(x * w, y * h + h / 2, z * d));
    for (const k of [0, 1, 2, 0, 2, 3]) { A.p.push(...P[k]); A.n.push(...nn); A.l.push(P[k][1] - cy); } }
}
function pyr(A, cx, cy, cz, w, d, h, rot) {   // mũ chóp răng cưa kiểu Moor (4 tam giác, hướng ra ngoài)
  const c = Math.cos(rot), s = Math.sin(rot), V = (x, z) => [cx + x * c - z * s, cy, cz + x * s + z * c], T = [cx, cy + h, cz];
  const Q = [V(-w / 2, -d / 2), V(w / 2, -d / 2), V(w / 2, d / 2), V(-w / 2, d / 2)];
  for (let i = 0; i < 4; i++) { const a = Q[i], b = Q[(i + 1) % 4], m = [(a[0] + b[0]) / 2 - cx, 0.0, (a[2] + b[2]) / 2 - cz];
    const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [T[0] - a[0], T[1] - a[1], T[2] - a[2]]; let n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
    let P = [a, b, T]; if (n[0] * m[0] + n[2] * m[2] < 0) { P = [a, T, b]; n = n.map((x) => -x); } const l = Math.hypot(...n) || 1;
    for (const q of P) { A.p.push(...q); A.n.push(n[0] / l, n[1] / l, n[2] / l); A.l.push(q[1] - cy + 20); } }
}
function crenel(A, ring, h, base, step = 2.2, mw = 1.1, mh = 1.6, md = 0.9, cap = 0) {   // răng cưa dọc mép đỉnh tường (cap > 0: mũ chóp)
  for (let i = 0; i < ring.length - 1; i++) { const [a, b] = [ring[i], ring[i + 1]], l = Math.hypot(b[0] - a[0], b[1] - a[1]), rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]);
    for (let s = step / 2; s < l; s += step) { const u = s / l, x = a[0] + (b[0] - a[0]) * u, z = -(a[1] + (b[1] - a[1]) * u); box(A, x, base + h, z, mw, mh, md, rot); if (cap) pyr(A, x, base + h + mh, z, mw, md, cap, rot); } }
}
// vòng nở ra ngoài d m (giao tuyến hai cạnh dịch — đủ cho vòng gần lồi)
function offsetRing(r, d) { const n = r.length, sa = r.reduce((s, p, i) => s + p[0] * r[(i + 1) % n][1] - r[(i + 1) % n][0] * p[1], 0) > 0 ? 1 : -1;
  return r.map((p, i) => { const a = r[(i + n - 1) % n], b = r[(i + 1) % n], e1 = [p[0] - a[0], p[1] - a[1]], e2 = [b[0] - p[0], b[1] - p[1]], l1 = Math.hypot(...e1) || 1, l2 = Math.hypot(...e2) || 1;
    const n1 = [e1[1] / l1 * sa, -e1[0] / l1 * sa], n2 = [e2[1] / l2 * sa, -e2[0] / l2 * sa], m = [n1[0] + n2[0], n1[1] + n2[1]], ml = Math.max(0.5, (m[0] * n1[0] + m[1] * n1[1]));
    return [p[0] + m[0] / ml * d, p[1] + m[1] / ml * d]; }); }
// ô cửa vòm trên mặt tường: lõi tối + vòm bậc (xấp xỉ bán nguyệt) + viền đá sáng nhô; s dọc cạnh (m), y cao (m, tính từ chân), w × hh ô
function archOpening(D, F, a, b, base, s, y, w, hh, proud = 0.12) {
  const l = Math.hypot(b[0] - a[0], b[1] - a[1]), u = s / l, dx = (b[0] - a[0]) / l, dn = (b[1] - a[1]) / l, on = [dn, -dx], rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]);
  const at = (o) => [a[0] + (b[0] - a[0]) * u + on[0] * o, a[1] + (b[1] - a[1]) * u + on[1] * o];
  const [e1, n1] = at(proud * 0.5), [e2, n2] = at(proud * 0.35);
  box(F, e2, base + y - 0.25, -n2, w + 0.7, hh + 0.25, proud * 0.7, rot);   // viền + bậu
  box(D, e1, base + y, -n1, w, hh, proud, rot);
  [0.96, 0.86, 0.68, 0.40].forEach((k, i) => { box(F, e2, base + y + hh + i * w * 0.13, -n2, (w + 0.7) * Math.max(k, 0.5) + 0.0, w * 0.13 + 0.05, proud * 0.7, rot); box(D, e1, base + y + hh + i * w * 0.12, -n1, w * k, w * 0.12, proud, rot); });
}
function wallLine(A, pts, hAt, h, thick) {   // tường dạng tuyến: dải hai mặt + đỉnh, chân bám địa hình
  for (let i = 0; i < pts.length - 1; i++) { const [a, b] = [pts[i], pts[i + 1]], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l < 0.5) continue;
    const ha = Math.max(hAt(...a), 0.5) - 1.0, hb = Math.max(hAt(...b), 0.5) - 1.0, rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]);
    const n = Math.max(1, Math.round(l / 6)); for (let k = 0; k < n; k++) { const u = (k + 0.5) / n; box(A, a[0] + (b[0] - a[0]) * u, ha + (hb - ha) * u, -(a[1] + (b[1] - a[1]) * u), l / n + 0.3, h + 1.0, thick, rot); } }
}

export function makeHeroes(H, hAt, U, terr, lines) {
  const group = new THREE.Group(), out = { group, hi: { tower: { value: 0 }, runway: { value: 0 } } };
  // ---- Tower of Homage + tường lâu đài
  const T = acc(), tw = H.tower; const base = tw.base - 1.5, ring = tw.p;
  walls(ring, tw.h + 1.5, push(T, base)); roof(ring, tw.h + 1.5, 0, (r) => THREE.ShapeUtils.triangulateShape(r.map(([x, y]) => new THREE.Vector2(x, y)), []), push(T, base));
  const CW = acc(); for (const w of H.castle_walls) { wallLine(CW, w, hAt, 8.0, 2.2); for (let i = 0; i < w.length - 1; i++) { const a = w[i], b = w[i + 1], ha = Math.max(hAt(...a), 0.5) - 1.0 + 9.0;   // răng cưa dọc tường lâu đài
      crenel(CW, [a, b], 0, ha, 2.4, 1.0, 1.2, 1.0, 0.0); } }
  // V5b-1b · ĐẶC ĐIỂM NHẬN DIỆN (cổng 16/10: "hero khối + khe") — dựng bằng HÌNH HỌC, số đo ƯỚC theo ảnh tài sản công (heroes/tower-of-homage.json):
  //  (1) chân tường choãi (talus) 2,5 m · (2) bậc thềm + cửa vào vòm mặt tây · (3) cửa sổ vòm hai tầng trên mỗi mặt dài · (4) răng cưa đúng nhịp 2,2 m có MŨ CHÓP kiểu Moor
  //  (5) gờ đá dưới tường chắn + sàn đỉnh có lầu cầu thang · (6) tường lâu đài có THÁP GÓC ở chỗ gãy khúc (≥ 28°) — mỗi tháp có răng cưa
  const LS = acc(), DK = acc(), rr = ring.map((p) => p.slice()); { const sa = rr.reduce((s, p, i) => s + p[0] * rr[(i + 1) % rr.length][1] - rr[(i + 1) % rr.length][0] * p[1], 0); if (sa < 0) rr.reverse(); }
  walls(offsetRing(rr, 0.7), 2.5, push(T, base));   // (1) chân choãi
  walls(offsetRing(rr, 0.28), tw.h + 1.5 - 1.6, push(LS, base), tw.h + 1.5 - 2.1);   // (5) gờ đá
  crenel(T, ring.concat([ring[0]]), tw.h + 1.5, base, 2.2, 1.1, 1.6, 0.9, 0.7);   // (4) răng cưa + mũ chóp
  const edges = rr.map((a, i) => [a, rr[(i + 1) % rr.length]]).map(([a, b]) => ({ a, b, l: Math.hypot(b[0] - a[0], b[1] - a[1]) })).filter((e) => e.l > 7).sort((x, y) => y.l - x.l);
  for (const e of edges) for (const [y, k] of [[8.5, 0], [15.5, 1]]) { const nW = Math.max(1, Math.floor(e.l / 9)); for (let j = 0; j < nW; j++) archOpening(DK, LS, e.a, e.b, base, e.l * (j + 0.5 + 0.18 * (k ? -1 : 1)) / nW, y, 1.0, 1.7); }   // (3)
  { const w = edges.reduce((m, e) => (((e.a[0] + e.b[0]) / 2 < (m.a[0] + m.b[0]) / 2) ? e : m), edges[0]); out.towerDoorEdge = w;   // (2) cửa vào mặt tây + bậc thềm
    archOpening(DK, LS, w.a, w.b, base + 1.6, w.l * 0.5, 0.0, 1.8, 2.4, 0.2);
    const l = w.l, dx = (w.b[0] - w.a[0]) / l, dn = (w.b[1] - w.a[1]) / l, on = [dn, -dx], rot = Math.atan2(-(w.b[1] - w.a[1]), w.b[0] - w.a[0]);
    for (let k = 0; k < 6; k++) { const o = 0.9 + (5 - k) * 0.55, e = (w.a[0] + w.b[0]) / 2 + on[0] * o, n = (w.a[1] + w.b[1]) / 2 + on[1] * o; box(LS, e, Math.min(base, hAt(e, n)) - 0.5, -n, 3.4, base - Math.min(base, hAt(e, n)) + 0.5 + (k + 1) * 0.28, 0.6, rot); } }
  { const c0 = rr[0], c1 = rr[1], dx = c1[0] - c0[0], dn = c1[1] - c0[1], l = Math.hypot(dx, dn), ctr = rr.reduce((s, p) => [s[0] + p[0] / rr.length, s[1] + p[1] / rr.length], [0, 0]);   // (5) lầu cầu thang trên sàn đỉnh
    const e = c0[0] + (ctr[0] - c0[0]) * 0.32, n = c0[1] + (ctr[1] - c0[1]) * 0.32, rot = Math.atan2(-dn, dx); box(T, e, base + tw.h + 1.5, -n, 3.6, 3.0, 3.6, rot);
    const sq = [[-1.8, -1.8], [1.8, -1.8], [1.8, 1.8], [-1.8, 1.8], [-1.8, -1.8]].map(([x, z]) => [e + x * Math.cos(rot) - z * Math.sin(rot), n - (x * Math.sin(rot) + z * Math.cos(rot))]); crenel(T, sq, tw.h + 4.5, base, 1.2, 0.6, 0.8, 0.5, 0.4); }
  // (6) tháp góc tường lâu đài
  for (const w of H.castle_walls) for (let i = 1; i < w.length - 1; i++) { const a = w[i - 1], p = w[i], b = w[i + 1], u = [p[0] - a[0], p[1] - a[1]], v = [b[0] - p[0], b[1] - p[1]];
    const ang = Math.acos(Math.max(-1, Math.min(1, (u[0] * v[0] + u[1] * v[1]) / ((Math.hypot(...u) * Math.hypot(...v)) || 1)))) * 180 / Math.PI; if (ang < 28) continue;
    const g = Math.max(hAt(...p), 0.5) - 1.0, rot = Math.atan2(-u[1], u[0]); box(CW, p[0], g, -p[1], 5.6, 12.0, 5.6, rot);
    const sq = [[-2.8, -2.8], [2.8, -2.8], [2.8, 2.8], [-2.8, 2.8], [-2.8, -2.8]].map(([x, z]) => [p[0] + x * Math.cos(rot) - z * Math.sin(rot), p[1] - (x * Math.sin(rot) + z * Math.cos(rot))]);
    crenel(CW, sq, 12.0, g, 1.9, 0.95, 1.3, 0.7, 0.55); out.cornerTowers = (out.cornerTowers || 0) + 1; }
  const towerM = new THREE.Mesh(geoFrom(T), stoneMat(U, out.hi.tower, 'tapia')), castleM = new THREE.Mesh(geoFrom(CW), stoneMat(U, out.hi.tower, 'tapia'));
  const lsM = new THREE.Mesh(geoFrom(LS), stoneMat(U, out.hi.tower, 'lime')), dkM = new THREE.Mesh(geoFrom(DK), new THREE.MeshStandardMaterial({ color: 0x17120e, roughness: 1 }));
  for (const m of [lsM, dkM]) { m.castShadow = m.receiveShadow = true; group.add(m); }
  // khe bắn tên: dải tối mảnh trên tường tháp (hộp lõm tối)
  const SL = acc(); { const r = ring; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l < 6) continue;
      const rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]); for (const lv of [9, 16]) for (let s = l / 4; s < l; s += l / 2.01) { const u = s / l; box(SL, a[0] + (b[0] - a[0]) * u, base + lv, -(a[1] + (b[1] - a[1]) * u), 0.35, 1.8, 0.25, rot); } } }
  const slitM = new THREE.Mesh(geoFrom(SL), new THREE.MeshStandardMaterial({ color: 0x1d1813, roughness: 1 }));
  for (const m of [towerM, castleM, slitM]) { m.castShadow = m.receiveShadow = true; group.add(m); }
  // viền sáng tháp (vỏ lộn mặt sau, nở 1,8 m) cho mốc đinh/nhấn
  const hull = new THREE.Mesh(new THREE.ExtrudeGeometry(new THREE.Shape(ring.map(([x, y]) => new THREE.Vector2(x, y))), { depth: tw.h + 3.5, bevelEnabled: false }).rotateX(-Math.PI / 2),
    new THREE.MeshBasicMaterial({ color: '#ffd166', side: THREE.BackSide, transparent: true, opacity: 0, depthWrite: false, fog: false }));
  { const c = ring.reduce((s, p) => [s[0] + p[0] / ring.length, s[1] + p[1] / ring.length], [0, 0]); hull.geometry.translate(-c[0], 0, c[1]); hull.scale.set(1.12, 1, 1.12); hull.position.set(c[0], base, -c[1]); out.towerTop = new THREE.Vector3(c[0], base + tw.h + 2, -c[1]); out.towerC = c; }
  hull.visible = false; group.add(hull); out.towerHull = hull;
  // ---- tường thành thành phố (đá vôi)
  const LW = acc(); for (const w of H.citywalls) wallLine(LW, w, hAt, 6.0, 3.0);
  const lw = new THREE.Mesh(geoFrom(LW), stoneMat(U, { value: 0 }, 'lime')); lw.castShadow = lw.receiveShadow = true; group.add(lw);
  // ---- đường băng
  // hai đầu đường băng = cực trị của tim OSM + đoạn ngưỡng lùi (displaced_threshold) chiếu lên trục
  const rp = H.runway.p.concat(...H.thresholds), a0 = H.runway.p[0], b0 = H.runway.p[H.runway.p.length - 1], ax = [b0[0] - a0[0], b0[1] - a0[1]], al = Math.hypot(...ax);
  const pr = rp.map((p) => [(p[0] - a0[0]) * ax[0] / al + (p[1] - a0[1]) * ax[1] / al, p]); pr.sort((x, y) => x[0] - y[0]);
  let W0 = pr[0][1], E0 = pr[pr.length - 1][1]; if (W0[0] > E0[0]) [W0, E0] = [E0, W0];
  const L = Math.hypot(E0[0] - W0[0], E0[1] - W0[1]), dir = [(E0[0] - W0[0]) / L, (E0[1] - W0[1]) / L], nrm = [-dir[1], dir[0]], hw = H.runway.w / 2;
  const disp = H.thresholds.map((p) => p.map(([e, n]) => (e - W0[0]) * dir[0] + (n - W0[1]) * dir[1])).map((s) => [Math.min(...s), Math.max(...s)]);
  const dW = Math.max(0, ...disp.filter((d) => d[0] < L / 2).map((d) => d[1])), dE = L - Math.max(0, ...disp.filter((d) => d[0] > L / 2).map((d) => L - d[0]));
  const TW = 8192, TH = 256, cv = document.createElement('canvas'); cv.width = TW; cv.height = TH; const g = cv.getContext('2d');
  const X = (s) => s / L * TW, Yv = (o) => (o + hw) / (2 * hw) * TH;   // s dọc (m từ đầu tây), o ngang (m, −hw..hw)
  g.fillStyle = '#4a4c50'; g.fillRect(0, 0, TW, TH);
  { const R = rng(3); for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '30,30,32' : '120,120,118'},${0.05 + R() * 0.08})`; g.fillRect(R() * TW, R() * TH, 2 + R() * 30, 1 + R() * 3); } }
  g.fillStyle = 'rgba(25,25,27,0.35)'; g.fillRect(X(dW + 250), Yv(-6), X(L - dW - 500) - X(0) + 0, Yv(6) - Yv(-6));   // vết lốp vùng chạm bánh (giữa)
  g.fillStyle = '#ecebe6';
  const rect = (s0, s1, o0, o1) => g.fillRect(X(s0), Yv(o0), X(s1) - X(s0), Yv(o1) - Yv(o0));
  rect(0, L, hw - 1.5, hw - 0.6); rect(0, L, -hw + 0.6, -hw + 1.5);   // vạch mép
  for (let s = dW + 30 + 12 + 9 + 12; s < dE - 30 - 12 - 9 - 12 - 30; s += 50) rect(s, s + 30, -0.45, 0.45);   // tim: 30 m vạch, 20 m khe
  const piano = (s0) => { for (let k = 0; k < 6; k++) { const o = 3.0 + k * 3.6; rect(s0, s0 + 30, o - 0.9, o + 0.9); rect(s0, s0 + 30, -o - 0.9, -o + 0.9); } };
  piano(dW + 6); piano(dE - 36);
  for (const s of [dW + 250, dE - 295]) { rect(s, s + 45, 4.5, 10.5); rect(s, s + 45, -10.5, -4.5); }   // điểm ngắm
  const num = (txt, s, rot) => { g.save(); g.translate(X(s), TH / 2); g.rotate(rot); g.scale(TW / L / (TH / (2 * hw)), 1); g.font = `bold ${Math.round(9 / (2 * hw) * TH * 1.35)}px DejaVu Sans, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, 0, 0); g.restore(); };
  num('09', dW + 52, Math.PI / 2); num('27', dE - 52, -Math.PI / 2);
  for (const [s0, s1] of [[0, dW], [dE, L]]) for (let s = s0 + 10; s < s1 - 10; s += 30) { g.save(); g.translate(X(s), TH / 2); g.fillRect(0, -2, X(18) - X(0), 4); g.restore(); }   // mũi tên ngưỡng lùi (tối giản)
  const rtex = new THREE.CanvasTexture(cv); rtex.colorSpace = THREE.SRGBColorSpace; rtex.anisotropy = 16;
  const RP = [], RU = [], N = Math.ceil(L / 15);
  for (let i = 0; i <= N; i++) { const s = L * i / N; for (const o of [-hw, hw]) { const e = W0[0] + dir[0] * s + nrm[0] * o, n = W0[1] + dir[1] * s + nrm[1] * o; RP.push(e, Math.max(3.0, hAt(e, n)) + 0.45, -n); RU.push(i / N, (o + hw) / (2 * hw)); } }
  const RI = []; for (let i = 0; i < N; i++) { const k = i * 2; RI.push(k, k + 2, k + 1, k + 1, k + 2, k + 3); }
  const rg = new THREE.BufferGeometry(); rg.setAttribute('position', new THREE.Float32BufferAttribute(RP, 3)); rg.setAttribute('uv', new THREE.Float32BufferAttribute(RU, 2)); rg.setIndex(RI); rg.computeVertexNormals();
  const rmat = new THREE.MeshStandardMaterial({ map: rtex, roughness: 0.85, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
  rmat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uYear: U.uYear, uDim: U.uDim, uHi: out.hi.runway, tYears: terr.uni.tYears, uExt: terr.uni.uExt });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWPr;').replace('#include <begin_vertex>', '#include <begin_vertex>\n vWPr = (modelMatrix * vec4(transformed,1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\nuniform float uYear, uDim, uHi; uniform sampler2D tYears; uniform vec4 uExt; varying vec3 vWPr; ${GLSL_LAND}`)
      .replace('#include <map_fragment>', `#include <map_fragment>
      vec2 guv = vec2((vWPr.x - uExt.x) / uExt.z, (-vWPr.z - uExt.y) / uExt.w); float lk = landK(decYear(texture(tYears, guv).ba), uYear);
      if (uYear < 1941.0 || lk < 0.98) discard;
      diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * 1.35 + vec3(0.06, 0.05, 0.02), uHi);   // V5b-1b: mốc đinh làm SÁNG (không ám nâu)
      { float L = dot(diffuseColor.rgb, vec3(0.299,0.587,0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55*uDim*(1.0-uHi)) * (1.0 - 0.36*uDim*(1.0-uHi)); }`); };
  const runway = new THREE.Mesh(rg, rmat); runway.receiveShadow = true; group.add(runway);
  // viền sáng đường băng (mốc đinh): khung chữ nhật phát sáng, chỉ phần trên đất
  const fr = new THREE.Group(); const fmat = new THREE.MeshBasicMaterial({ color: '#ffd166', transparent: true, opacity: 0, depthWrite: false, fog: false });
  const seg = (s0, s1, o0, o1) => { const e0 = W0[0] + dir[0] * s0 + nrm[0] * o0, n0 = W0[1] + dir[1] * s0 + nrm[1] * o0, e1 = W0[0] + dir[0] * s1 + nrm[0] * o1, n1 = W0[1] + dir[1] * s1 + nrm[1] * o1;
    const l = Math.hypot(e1 - e0, n1 - n0), m = new THREE.Mesh(new THREE.BoxGeometry(l + 3, 1.2, 3), fmat); m.position.set((e0 + e1) / 2, 4.6, -(n0 + n1) / 2); m.rotation.y = Math.atan2(-(n1 - n0), e1 - e0); fr.add(m); };
  // khung chỉ trên phần đường băng có đất năm 1941 (đông bờ vịnh cũ, ≈ E −340 m — xem build_scene.OLD_BAY); phần lấn vịnh khai hoang 1941–43
  const sL = Math.max(0, Math.min(L, (-340 - W0[0]) / dir[0])); out.rwLandS = sL;
  seg(sL, L, hw + 3, hw + 3); seg(sL, L, -hw - 3, -hw - 3); seg(sL, sL, -hw - 3, hw + 3); seg(L, L, -hw - 3, hw + 3); fr.visible = false; group.add(fr); out.rwFrame = fr; out.rwFrameMat = fmat;
  // chắn đường ngang (đỏ/trắng) ở hai mép đường băng trên trục Winston Churchill Ave (gốc toạ độ)
  const bar = new THREE.Group(); for (const o of [hw + 9, -hw - 9]) { const e = nrm[0] * o, n = nrm[1] * o, h0 = Math.max(3, hAt(e, n));
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.4, 0.5), new THREE.MeshStandardMaterial({ color: 0x9aa0a6 })); post.position.set(e + 5, h0 + 0.7, -n); bar.add(post);
    for (let k = 0; k < 6; k++) { const arm = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.18, 0.18), new THREE.MeshStandardMaterial({ color: k % 2 ? 0xf2f2f2 : 0xc8322b })); arm.position.set(e + 4.2 - k * 1.6, h0 + 1.3, -n); bar.add(arm); } }
  bar.visible = false; group.add(bar); out.barriers = bar;
  out.runwayMid = new THREE.Vector3(0, 4, 0); out.runway = { W0, E0, L, dir, hw, dW, dE };
  // ---- V5b-1b · MỐC 1941 A-lite: trạm biên giới (OSM node 5029266974) + hàng xe chờ ở chắn đường băng + người đi bộ (phẳng màu, đổ bóng thật).
  // Hình dáng xe kiểu thập niên 1940 (thân hộp + cabin + bánh), KHÔNG mô phỏng mẫu xe cụ thể; chỉ hiện quanh mốc 1941 (1940,5–1946,5) — số lượng là minh hoạ.
  const life = new THREE.Group(), RR = rng(41), M = (c) => new THREE.MeshLambertMaterial({ color: c });
  const mBlk = M(0x15171a), mCols = [0x2b3a2f, 0x1c2230, 0x5a2a24, 0x2a2a2a, 0x6b5a3a].map(M), mGl = M(0x31414f), skin = [0xc99a78, 0xa8785a, 0xe0b896].map(M), coats = [0x30384a, 0x5a4a3a, 0x7a2e2a, 0xd8d0c0, 0x3c4a34, 0x24282e].map(M);
  const put = (geo, mat, e, y, n, rot = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(e, y, -n); m.rotation.y = rot; m.castShadow = true; m.receiveShadow = true; life.add(m); return m; };
  const car = (e, n, rot, kind) => { const g = Math.max(hAt(e, n), 3.0) + 0.45, c = mCols[Math.floor(RR() * mCols.length)], L_ = kind === 'bus' ? 9.0 : kind === 'truck' ? 6.0 : 4.3, W_ = kind === 'bus' ? 2.4 : 1.7;
    const grp = new THREE.Group(); grp.position.set(e, g, -n); grp.rotation.y = rot; life.add(grp); const add = (geo, mat, x, y, z) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; grp.add(m); };
    if (kind === 'bus') { add(new THREE.BoxGeometry(L_, 2.3, W_), M(0xb8392e), 0, 1.45, 0); add(new THREE.BoxGeometry(L_ * 0.96, 0.7, W_ + 0.02), M(0xe8e0c8), 0, 1.95, 0); add(new THREE.BoxGeometry(L_ * 0.9, 0.5, W_ + 0.03), mGl, 0, 1.95, 0); }
    else if (kind === 'truck') { add(new THREE.BoxGeometry(1.8, 1.7, W_), c, L_ / 2 - 0.9, 1.25, 0); add(new THREE.BoxGeometry(0.1, 0.6, W_ * 0.8), mGl, L_ / 2 - 0.02, 1.6, 0); add(new THREE.BoxGeometry(L_ - 2.0, 1.1, W_ + 0.1), M(0x6b5a3a), -1.0, 1.0, 0); }
    else { add(new THREE.BoxGeometry(L_, 0.75, W_), c, 0, 0.75, 0); add(new THREE.BoxGeometry(L_ * 0.48, 0.65, W_ * 0.9), c, -0.25, 1.45, 0); add(new THREE.BoxGeometry(L_ * 0.46, 0.45, W_ * 0.92), mGl, -0.25, 1.45, 0);
      add(new THREE.BoxGeometry(L_ * 0.22, 0.5, W_ * 1.08), c, L_ * 0.34, 0.7, 0); }
    for (const x of [-L_ * 0.32, L_ * 0.32]) for (const z of [-W_ / 2, W_ / 2]) add(new THREE.BoxGeometry(0.7, 0.7, 0.25), mBlk, x, 0.35, z); };
  const person = (e, n) => { const g = Math.max(hAt(e, n), 3.0) + 0.45, h = 1.6 + 0.2 * RR(), rot = RR() * 6.28;
    put(new THREE.BoxGeometry(0.34, h * 0.45, 0.22), mBlk, e, g + h * 0.22, n, rot); put(new THREE.BoxGeometry(0.48, h * 0.38, 0.28), coats[Math.floor(RR() * coats.length)], e, g + h * 0.62, n, rot);
    put(new THREE.BoxGeometry(0.22, 0.24, 0.22), skin[Math.floor(RR() * skin.length)], e, g + h * 0.92, n, rot); };
  // hàng xe hai phía chắn, ĐẶT TRÊN tim Winston Churchill Ave (OSM, gộp hai chiều xe theo N mỗi 20 m như scenes/gib20.js)
  const bins = new Map(); for (const [e, n] of (lines && lines.wca) || [[0, -300], [0, 600]]) { const k = Math.round(n / 20); if (!bins.has(k)) bins.set(k, []); bins.get(k).push(e); }
  const WC = [...bins.entries()].sort((a, b) => a[0] - b[0]).map(([k, es]) => [es.reduce((s, v) => s + v, 0) / es.length, k * 20]);
  const onRoad = (n, lane) => { let i = 1; while (i < WC.length - 1 && WC[i][1] < n) i++; const [a, b] = [WC[i - 1], WC[i]], u = Math.max(0, Math.min(1, (n - a[1]) / ((b[1] - a[1]) || 1))), dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1;
    return [a[0] + dx * u + dn / l * lane, n - dx / l * lane, Math.atan2(dn, dx)]; };
  const carOn = (n, lane, dirN, kind) => { const [e, nn, ang] = onRoad(n, lane); car(e, nn, ang + (dirN > 0 ? 0 : Math.PI), kind); };
  for (let k = 0; k < 6; k++) carOn(hw + 16 + k * 7.5 + RR() * 2, -2.4, -1, k === 3 ? 'truck' : 'car');   // chờ đi về phía nam
  for (let k = 0; k < 5; k++) carOn(-hw - 16 - k * 7.5 - RR() * 2, 2.4, 1, k === 1 ? 'bus' : 'car');    // chờ đi về phía bắc
  for (let k = 0; k < 4; k++) carOn(120 + k * 70 + RR() * 20, 2.4, 1, 'car');   // xe đang chạy về phía biên giới
  for (let k = 0; k < 16; k++) { const [e, n] = onRoad(hw + 12 + RR() * 60, -7.0 - RR() * 2); person(e, n); }   // người đi bộ chờ qua đường băng (lề tây)
  for (let k = 0; k < 8; k++) { const [e, n] = onRoad(-hw - 12 - RR() * 40, 7.0 + RR() * 2); person(e, n); }
  if (H.gate) { const [ge, gn] = H.gate, g0 = Math.max(hAt(ge, gn), 3.0);   // trạm biên giới: nhà gác, chắn, bốt lính, người qua
    put(new THREE.BoxGeometry(6, 3.2, 4), M(0xece6d8), ge - 9, g0 + 1.6, gn); put(new THREE.ConeGeometry(4.6, 1.4, 4, 1).rotateY(Math.PI / 4), M(0xa04a32), ge - 9, g0 + 3.9, gn);
    put(new THREE.BoxGeometry(6, 3.2, 4), M(0xe2dccb), ge + 10, g0 + 1.6, gn + 3); put(new THREE.BoxGeometry(6.6, 0.3, 4.6), M(0x7a7266), ge + 10, g0 + 3.3, gn + 3);
    put(new THREE.BoxGeometry(1.4, 2.6, 1.4), M(0x2c3e2e), ge - 4.5, g0 + 1.3, gn - 3); for (let k = 0; k < 5; k++) put(new THREE.BoxGeometry(1.5, 0.16, 0.16), M(k % 2 ? 0xf2f2f2 : 0xc8322b), ge - 3 + k * 1.5, g0 + 1.2, gn - 1);
    for (let k = 0; k < 3; k++) carOn(gn - 14 - k * 8, 2.4, 1, k === 0 ? 'bus' : 'car');
    for (let k = 0; k < 18; k++) person(ge + 4 + RR() * 5, gn - 30 + RR() * 45); }
  life.visible = false; group.add(life); out.life = life;
  out.update = (year) => { bar.visible = year >= 1941; life.visible = year >= 1940.5 && year <= 1946.5; };
  return out;
}

// BAN-CUOI-T3 (22/10/2026, việc 1b — chủ dự án V2-D8: "được thêm vật đời sống chung trên eo đất, không cần tra nguồn mới") · VẬT ĐỜI SỐNG CHUNG CHUNG.
// Mọi vật ở đây là MINH HOẠ BẬC 5 (ước lượng; số, vị trí, hình dạng không có nguồn riêng) — không công trình có tên, không trái mốc năm (cửa sổ wY do đặc tả khai).
// opt.doiSong = [{ kind, at: [E, N] | pts: [[E, N], …], n, r, wY: {on, full?, off0?, off1?}, seed, ... }]
//   leu   : lều vải (cụm tự nhiên, xoay/lệch ngẫu nhiên — tránh "bàn cờ" LOOK-4)   kho : kho/lán thấp mái dốc        rao : hàng rào cọc + 2 thanh theo pts
//   vuon  : ô vườn luống (màu luống/đất)                                          dong: đống vật liệu (đá, cát, gỗ)  duong: đường mòn đất theo pts (rộng w m)
//   xe    : xe (kieu 'ngua' = xe kéo bằng ngựa/la; 'tai' = xe tải đời 1930s) chạy theo pts, tốc v m/s (thời gian phim)
//   giasuc: gia súc gặm cỏ (bò/dê) quanh at, bán kính r, di chậm
// Tên hàm dựng (camps, fence, gardens, roads, carts, horses, piles) khớp luật lớp của mặt nạ ID (design/k2v/v7c/idmask_v7c.js): lều/kho = 'trai', rào = 'congsu',
// vườn/đường = 'datvat', xe/gia súc = 'nguoi', đống = 'khac'.
import { maskify } from './core.js';
let THREE = null;   // lấy từ ctx.THREE (như ngua.js)

const rng = (s) => { let x = (s >>> 0) || 1; return () => { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return ((x >>> 0) % 1e6) / 1e6; }; };
const win = (Y, w) => { if (!w) return 1; const on = w.on ?? -1e9, full = w.full ?? on, off0 = w.off0 ?? 1e9, off1 = w.off1 ?? off0;
  if (Y < on || Y >= off1) return 0; const a = full > on ? Math.min(1, (Y - on) / (full - on)) : 1, b = off1 > off0 ? Math.min(1, Math.max(0, (off1 - Y) / (off1 - off0))) : (Y >= off0 ? 0 : 1); return Math.min(a, b); };
const cum = (P) => { const c = [0]; for (let i = 1; i < P.length; i++) c.push(c[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1])); return c; };
const along = (P, C, s) => { const L = C[C.length - 1]; s = ((s % L) + L) % L; let i = 1; while (i < P.length - 1 && C[i] < s) i++; const a = P[i - 1], b = P[i], u = (s - C[i - 1]) / ((C[i] - C[i - 1]) || 1);
  return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, Math.atan2(b[0] - a[0], b[1] - a[1])]; };
function lam(col, ctx) { const m = new THREE.MeshLambertMaterial({ color: col }); maskify(m, ctx.U, 1); return m; }
function geoMerge(parts) {   // gộp hình học nhỏ (đã đặt vị trí) thành một
  const pos = [], nor = []; for (const g0 of parts) { const g = g0.index ? g0.toNonIndexed() : g0; pos.push(...g.attributes.position.array); nor.push(...g.attributes.normal.array); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3)); return g; }
function inst(geo, mat, n) { const im = new THREE.InstancedMesh(geo, mat, Math.max(1, n)); im.castShadow = im.receiveShadow = true; im.frustumCulled = false; return im; }
let M4, Q, Yx, V, S;
function put(im, i, e, y, n, rot, s) { M4.compose(V.set(e, y, -n), Q.setFromAxisAngle(Yx, rot), S.set(s, s, s)); im.setMatrixAt(i, M4); }

function cluster(sp, R, minD) {   // điểm rải tự nhiên trong đĩa bán kính r, giữ khoảng cách tối thiểu
  const P = []; let tries = 0; const n = sp.n || 10, r = sp.r || 30;
  while (P.length < n && tries++ < n * 60) { const a = R() * 6.2832, d = r * Math.sqrt(R()), e = sp.at[0] + Math.cos(a) * d * (sp.sx || 1), q = sp.at[1] + Math.sin(a) * d;
    if (P.every((p) => Math.hypot(p[0] - e, p[1] - q) >= minD)) P.push([e, q, R()]); }
  return P; }

// ---- lều + kho (lớp 'trai') ----
function camps(sp, ctx, terr, g) {
  const R = rng(sp.seed || 11), leu = sp.kind === 'leu';
  const geo = leu ? geoMerge([new THREE.ConeGeometry(2.0, 2.6, 7).translate(0, 1.3, 0)]) : geoMerge([new THREE.BoxGeometry(7, 2.6, 4).translate(0, 1.3, 0), new THREE.CylinderGeometry(0.01, 2.6, 7.4, 3, 1).rotateZ(Math.PI / 2).scale(1, 0.55, 1).translate(0, 3.1, 0)]);
  const cols = leu ? [0xe6dcc4, 0xd8cdb0, 0xcfc29f] : [0xc9bfa8, 0xb3a487, 0xa38c6c];   // lán: tường vôi/đá nhạt
  const P = cluster(sp, R, leu ? 6 : 12), ims = cols.map((c) => inst(geo, lam(c, ctx), P.length)); ims.forEach((im) => g.add(im));
  const it = P.map((p, i) => ({ e: p[0], n: p[1], k: p[2], c: i % cols.length, rot: R() * 6.28, s: (leu ? 0.8 : 0.85) + R() * 0.4, y: terr.hAt(p[0], p[1]) }));
  return { n: P.length, update(Y) { const k = win(Y, sp.wY); const cnt = cols.map(() => 0);
    for (const x of it) { const im = ims[x.c], j = cnt[x.c]++; put(im, j, x.e, Math.max(x.y, 0.3) - 0.05, x.n, x.rot, x.k < k ? x.s : 0); }
    ims.forEach((im, c) => { im.count = cnt[c]; im.instanceMatrix.needsUpdate = true; }); } }; }

// ---- hàng rào cọc (lớp 'congsu') ----
function fence(sp, ctx, terr, g) {
  const C = cum(sp.pts), L = C[C.length - 1], st = sp.buoc || 3, N = Math.floor(L / st) + 1;
  const post = inst(new THREE.BoxGeometry(0.18, 1.4, 0.18).translate(0, 0.7, 0), lam(0x6b5236, ctx), N), rail = inst(new THREE.BoxGeometry(0.08, 0.1, st).translate(0, 0, 0), lam(0x7a6040, ctx), N * 2);
  g.add(post, rail); const it = []; for (let i = 0; i < N; i++) { const s = Math.min(L, i * st), [e, n, a] = along(sp.pts, C, s); it.push({ e, n, a, u: s / L, y: Math.max(terr.hAt(e, n), 0.3) }); }
  return { n: N, update(Y) { const k = win(Y, sp.wY);   // mọc dọc tuyến theo k
    it.forEach((x, i) => { const on = x.u <= k; put(post, i, x.e, x.y, x.n, Math.PI - x.a, on ? 1 : 0);
      for (const [j, h] of [[0, 0.55], [1, 1.1]]) put(rail, i * 2 + j, x.e + Math.sin(x.a) * st / 2, x.y + h, x.n + Math.cos(x.a) * st / 2, Math.PI - x.a, on && i < N - 1 ? 1 : 0); });
    post.instanceMatrix.needsUpdate = rail.instanceMatrix.needsUpdate = true; } }; }

// ---- vườn (luống) + đường mòn (lớp 'datvat') ----
function gardens(sp, ctx, terr, g) {
  const R = rng(sp.seed || 21), w = sp.w || 14, h = sp.h || 9, nr = sp.luong || 5, hh = sp.cao ?? 0.7, P = cluster(sp, R, Math.max(w, h) * 1.05);
  const geo = geoMerge([...Array(nr).keys()].map((i) => new THREE.BoxGeometry(w, hh, h / (nr + 2)).translate(0, hh / 2, (i - (nr - 1) / 2) * h / nr)).concat([new THREE.BoxGeometry(w, 0.06, h).translate(0, 0.03, 0)]));   /* luống + nền đất ruộng */
  const cols = sp.mau || [0x4f6b2e, 0x6b7a35, 0x7a5a3a], ims = cols.map((c) => inst(geo, lam(c, ctx), P.length)); ims.forEach((im) => g.add(im));
  const it = P.map((p, i) => ({ e: p[0], n: p[1], k: p[2], c: i % 3, rot: (sp.rot ?? R() * 3.14) + (R() - 0.5) * 0.3, y: terr.hAt(p[0], p[1]) }));
  return { n: P.length, update(Y) { const k = win(Y, sp.wY), cnt = [0, 0, 0];
    for (const x of it) { const j = cnt[x.c]++; put(ims[x.c], j, x.e, Math.max(x.y, 0.3), x.n, x.rot, x.k < k ? 1 : 0); }
    ims.forEach((im, c) => { im.count = cnt[c]; im.instanceMatrix.needsUpdate = true; }); } }; }
function roads(sp, ctx, terr, g) {
  const C = cum(sp.pts), L = C[C.length - 1], st = 4, N = Math.ceil(L / st), w = sp.w || 4;
  const im = inst(new THREE.BoxGeometry(w, 0.12, st * 1.05), lam(sp.mau || 0x9c8460, ctx), N); im.castShadow = false; g.add(im);
  const it = []; for (let i = 0; i < N; i++) { const [e, n, a] = along(sp.pts, C, (i + 0.5) * st); it.push({ e, n, a, u: i / N, y: Math.max(terr.hAt(e, n), 0.3) }); }
  return { n: N, update(Y) { const k = win(Y, sp.wY); it.forEach((x, i) => put(im, i, x.e, x.y + 0.08, x.n, Math.PI - x.a, x.u <= k ? 1 : 0)); im.instanceMatrix.needsUpdate = true; } }; }

// ---- xe + gia súc (lớp 'nguoi': vật động có vai sống) ----
function carts(sp, ctx, terr, g) {
  const R = rng(sp.seed || 31), tai = sp.kieu === 'tai', C = cum(sp.pts), L = C[C.length - 1], n = sp.n || 4, v = sp.v ?? (tai ? 6 : 1.6);
  const body = tai ? geoMerge([new THREE.BoxGeometry(2.2, 1.6, 5.2).translate(0, 1.5, -0.6), new THREE.BoxGeometry(2.0, 1.7, 1.6).translate(0, 1.55, 2.6)])
    : geoMerge([new THREE.BoxGeometry(1.6, 0.7, 3.0).translate(0, 1.05, 0), new THREE.BoxGeometry(0.7, 1.3, 2.0).translate(0, 1.2, 2.6)]);   // thùng xe + con vật kéo (khối)
  const whl = new THREE.CylinderGeometry(tai ? 0.5 : 0.65, tai ? 0.5 : 0.65, 0.2, 10).rotateZ(Math.PI / 2);
  const wg = geoMerge(tai ? [whl.clone().translate(1.1, 0.5, 1.9), whl.clone().translate(-1.1, 0.5, 1.9), whl.clone().translate(1.1, 0.5, -1.8), whl.clone().translate(-1.1, 0.5, -1.8)] : [whl.clone().translate(0.9, 0.65, -0.2), whl.clone().translate(-0.9, 0.65, -0.2)]);
  const cols = tai ? [0x3e4a3a, 0x5a4c3a] : [0x7a5a3a, 0x8c6c48], bi = cols.map((c) => inst(body, lam(c, ctx), n)), wi = inst(wg, lam(0x2a2420, ctx), n); bi.forEach((x) => g.add(x)); g.add(wi);
  const it = [...Array(n)].map((_, i) => ({ s0: (i / n + R() * 0.3 / n) * L, dir: sp.hai_chieu && i % 2 ? -1 : 1, c: i % cols.length, off: (R() - 0.5) * (sp.lech || 2) }));
  return { n, update(Y, t) { const k = win(Y, sp.wY), cnt = cols.map(() => 0);
    it.forEach((x, i) => { const s = x.s0 + x.dir * v * t, [e, q, a] = along(sp.pts, C, x.dir > 0 ? s : L - ((-s % L) + L) % L), ee = e + Math.cos(a) * x.off, qq = q - Math.sin(a) * x.off, y = Math.max(terr.hAt(ee, qq), 0.3), on = i / n < k ? 1 : 0;
      const ro = Math.PI - a + (x.dir < 0 ? Math.PI : 0); put(bi[x.c], cnt[x.c]++, ee, y, qq, ro, on); put(wi, i, ee, y, qq, ro, on);   /* hướng: (E, N) = (sin a, cos a) → quay Y = π − a */ });
    bi.forEach((im, c) => { im.count = cnt[c]; im.instanceMatrix.needsUpdate = true; }); wi.instanceMatrix.needsUpdate = true; } }; }
function horses(sp, ctx, terr, g) {
  const R = rng(sp.seed || 41), P = cluster(sp, R, 2.5), de = sp.loai === 'de';
  const geo = de ? geoMerge([new THREE.BoxGeometry(0.4, 0.45, 0.9).translate(0, 0.65, 0), new THREE.BoxGeometry(0.22, 0.3, 0.3).translate(0, 0.85, 0.55), ...[[-0.13, -0.32], [0.13, -0.32], [-0.13, 0.32], [0.13, 0.32]].map(([x, z]) => new THREE.BoxGeometry(0.08, 0.42, 0.08).translate(x, 0.21, z))])
    : geoMerge([new THREE.BoxGeometry(0.75, 0.75, 1.9).translate(0, 1.05, 0), new THREE.BoxGeometry(0.4, 0.45, 0.6).translate(0, 1.25, 1.15), ...[[-0.25, -0.65], [0.25, -0.65], [-0.25, 0.65], [0.25, 0.65]].map(([x, z]) => new THREE.BoxGeometry(0.15, 0.7, 0.15).translate(x, 0.35, z))]);
  const cols = de ? [0xe9e2d2, 0x5a4a3a, 0xbfae92] : [0x6b4a30, 0x2e2622, 0xd9cfbf], ims = cols.map((c) => inst(geo, lam(c, ctx), P.length)); ims.forEach((im) => g.add(im));
  const it = P.map((p, i) => ({ e: p[0], n: p[1], c: i % cols.length, ph: R() * 6.28, rot: R() * 6.28, k: p[2] }));
  return { n: P.length, update(Y, t) { const k = win(Y, sp.wY), cnt = cols.map(() => 0);
    for (const x of it) { const dx = Math.sin(t * 0.05 + x.ph) * 2.0, dn = Math.cos(t * 0.04 + x.ph * 1.3) * 2.0, e = x.e + dx, q = x.n + dn;
      put(ims[x.c], cnt[x.c]++, e, Math.max(terr.hAt(e, q), 0.3), q, x.rot + Math.sin(t * 0.1 + x.ph) * 0.6, x.k < k ? 1 : 0); }
    ims.forEach((im, c) => { im.count = cnt[c]; im.instanceMatrix.needsUpdate = true; }); } }; }
// ---- đống vật liệu (lớp 'khac') ----
function piles(sp, ctx, terr, g) {
  const R = rng(sp.seed || 51), P = cluster(sp, R, 5), geo = new THREE.ConeGeometry(2.2, 1.6, 6).translate(0, 0.8, 0), cols = [0xb8a888, 0x8e8478, 0x6e5a40];
  const ims = cols.map((c) => inst(geo, lam(c, ctx), P.length)); ims.forEach((im) => g.add(im)); const it = P.map((p, i) => ({ e: p[0], n: p[1], k: p[2], c: i % 3, s: 0.7 + R() * 0.8, rot: R() * 6.28 }));
  return { n: P.length, update(Y) { const k = win(Y, sp.wY), cnt = [0, 0, 0]; for (const x of it) put(ims[x.c], cnt[x.c]++, x.e, Math.max(terr.hAt(x.e, x.n), 0.3), x.n, x.rot, x.k < k ? x.s : 0);
    ims.forEach((im, c) => { im.count = cnt[c]; im.instanceMatrix.needsUpdate = true; }); } }; }

const BUILD = { leu: camps, kho: camps, rao: fence, vuon: gardens, duong: roads, xe: carts, giasuc: horses, dong: piles };
export function doiSong(specs, ctx, terr) {
  THREE = ctx.THREE; M4 = new THREE.Matrix4(); Q = new THREE.Quaternion(); Yx = new THREE.Vector3(0, 1, 0); V = new THREE.Vector3(); S = new THREE.Vector3();
  const group = new THREE.Group(), list = [], dem = {};
  for (const sp of specs || []) { const f = BUILD[sp.kind]; if (!f) throw new Error('doiSong: loại lạ ' + sp.kind); const g = new THREE.Group(); group.add(g); const r = f(sp, ctx, terr, g); list.push(r); dem[sp.kind] = (dem[sp.kind] || 0) + r.n; }
  return { group, n: dem, update(Y, t) { for (const r of list) r.update(Y, t || 0); },
    log: { lop: 'doi_song_chung', n: dem, nguon: 'không nguồn riêng — chủ dự án V2-D8 (22/10/2026 11:09): được thêm vật đời sống chung trên eo đất, không cần tra nguồn mới', bac: 5, uoc_luong: true } };
}

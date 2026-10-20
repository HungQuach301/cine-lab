// K2V tl · V7-PILOT (19/10/2026) · BỘ MÁY TIMELAPSE "XƯƠNG SỐNG" — ngữ pháp hình TL-1…TL-6 (chủ dự án duyệt 19/10; thắng §12.1 khi trái).
//  Một shot = (điểm máy cố định/trôi rất chậm, đường cong thời gian). Trong shot THỜI GIAN chạy liên tục; mọi lớp đọc thời gian và tự mọc/cháy/sập/rút.
//  · timeline(keys)  — đường cong thời gian: mốc [{t (s cảnh), at ('YYYY-MM-DD HH:MM' giờ địa phương | năm thập phân), sun ('real' | giờ cố định), lab ('y'|'m'|'d'|'dt'), hold}]
//                      → JD liên tục (Hermite đơn điệu Fritsch–Carlson: không vượt mốc, đảo chiều mượt khi tua ngược), năm thập phân, tốc độ (ngày/s), giờ mặt trời, nhãn bộ đếm.
//                      Đoạn chạy nhanh khai sun = giờ cố định → không nhấp nháy ngày–đêm; đoạn chậm sun = 'real' → chu kỳ ngày–đêm thật theo thiên văn (sun.js).
//  · win(Y, w)       — trạng thái vật có ngày: w = {on, full, off0, off1} (năm thập phân) → mọc 0..1, rút/huỷ 1..0.
//  · crossings(tl,…) — thời điểm (s cảnh) đường cong đi qua một năm (sự kiện điểm: vây hãm, nổ) để phát khói/lửa theo GIÂY cảnh (không biến mất khi năm chạy nhanh).
//  · camps(specs)    — trại lều xếp hàng dọc tuyến trại đã nắn từ bản đồ có nguồn (Faden 1783 / Drinkwater 1786), lều hiện dần theo k.
//  · lamps(specs)    — nguồn sáng đêm: quầng sáng cộng (sprite) + vệt sáng mặt đất; cường độ theo uNight.
//  · fence(pts)      — hàng rào cọc + lưới mảnh dọc tuyến (1909), mọc dọc tuyến theo k.
// Không Math.random (tất định). Nguồn + bậc từng lớp: cảnh ghi vào meta (log), KHÔNG lên hình (§12.1).
import { THREE, rng, maskify } from './core.js';
import { jdOf, calOf, sunPos, GIB } from './sun.js';

const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const pad = (n) => String(n).padStart(2, '0');
const cl = (u) => Math.max(0, Math.min(1, u));
const sstep = (a, b, x) => { const u = cl((x - a) / (b - a)); return u * u * (3 - 2 * u); };

// ---------- 1. thời gian liên tục ----------
export function jdOfKey(a, tz = null) {   // 'YYYY-MM-DD HH:MM' (giờ địa phương: LMT, hoặc múi tz) | năm thập phân
  if (typeof a === 'number') { const y = Math.floor(a), j0 = jdOf(y, 1, 1, 0), j1 = jdOf(y + 1, 1, 1, 0); return j0 + (a - y) * (j1 - j0); }
  const m = String(a).match(/^(-?\d+)-(\d+)-(\d+)(?:[ T](\d+):(\d+))?$/); if (!m) throw new Error('tl7: mốc thời gian sai ' + a);
  const h = m[4] ? +m[4] + +m[5] / 60 : 12; return jdOf(+m[1], +m[2], +m[3], h - (tz == null ? GIB.lon / 15 : tz));
}
export function yearOfJD(jd) { const c = calOf(jd), j0 = jdOf(c.y, 1, 1, 0), j1 = jdOf(c.y + 1, 1, 1, 0); return c.y + (jd - j0) / (j1 - j0); }
export function timeline(keys, { tz = null } = {}) {
  const K = keys.map((k) => Object.assign({}, k, { jd: jdOfKey(k.at, tz) })), n = K.length;
  if (n < 1) throw new Error('tl7: timeline rỗng');
  if (n === 1) K.push(Object.assign({}, K[0], { t: K[0].t + 1e3 }));
  const N = K.length, d = [], m = [];
  for (let i = 0; i < N - 1; i++) d.push((K[i + 1].jd - K[i].jd) / (K[i + 1].t - K[i].t));
  for (let i = 0; i < N; i++) {   // Fritsch–Carlson: tiếp tuyến đơn điệu; mốc hold → 0 (dừng mượt); đổi chiều → 0
    if (K[i].hold) { m.push(0); continue; }
    if (i === 0) { m.push(d[0]); continue; } if (i === N - 1) { m.push(d[N - 2]); continue; }
    const a = d[i - 1], b = d[i]; m.push(a * b <= 0 ? 0 : 2 / (1 / a + 1 / b));
  }
  for (let i = 0; i < N - 1; i++) { if (d[i] === 0) { m[i] = m[i + 1] = 0; continue; } const a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b; if (s > 9) { const tt = 3 / Math.sqrt(s); m[i] = tt * a * d[i]; m[i + 1] = tt * b * d[i]; } }
  const seg = (t) => { let i = 0; while (i < N - 2 && t > K[i + 1].t) i++; return i; };
  function jdAt(t) { if (t <= K[0].t) return K[0].jd; if (t >= K[N - 1].t) return K[N - 1].jd; const i = seg(t), h = K[i + 1].t - K[i].t, u = (t - K[i].t) / h, u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * K[i].jd + (u3 - 2 * u2 + u) * h * m[i] + (-2 * u3 + 3 * u2) * K[i + 1].jd + (u3 - u2) * h * m[i + 1]; }
  const rate = (t) => (jdAt(t + 1 / 48) - jdAt(t - 1 / 48)) * 24;   // ngày/s (có dấu)
  const lon = GIB.lon;
  function sunJD(t) { const jd = jdAt(t), k = K[seg(t)], sh = k.sun ?? 'real'; if (sh === 'real') return jd;
    const jl = jd + (tz == null ? lon / 15 : tz) / 24, day = Math.floor(jl - 0.5) + 0.5; return day + sh / 24 - (tz == null ? lon / 15 : tz) / 24; }
  function label(t) { const jd = jdAt(t), k = K[seg(t)], lab = k.lab || 'y', jl = jd + (tz == null ? lon / 15 : tz) / 24, c = calOf(jl), mins = Math.round(((jl + 0.5) % 1) * 1440) % 1440;
    if (lab === 'y') return String(Math.floor(yearOfJD(jd)));
    if (lab === 'm') return `${MON[c.mo - 1]} ${c.y}`;
    if (lab === 'd') return `${c.d} ${MON[c.mo - 1]} ${c.y}`;
    return `${c.d} ${MON[c.mo - 1]} ${c.y} · ${pad(Math.floor(mins / 60))}:${pad(mins % 60)}`; }
  return { keys: K, jdAt, year: (t) => yearOfJD(jdAt(t)), rate, sunJD, sun: (t) => sunPos(sunJD(t)), label, seg };
}
// năm/s lớn nhất trong đoạn (log + so §10.3)
export function yearRate(tl, t0, t1, fps = 24) { let mx = 0; for (let t = t0; t < t1; t += 1 / fps) mx = Math.max(mx, Math.abs(tl.year(t + 1 / fps) - tl.year(t)) * fps); return mx; }

// ---------- 2. vật có ngày ----------
export function win(Y, w) { if (!w) return 1; const g = w.full != null && w.full > w.on ? cl((Y - w.on) / (w.full - w.on)) : Y >= w.on ? 1 : 0;
  const o = w.off0 == null ? 1 : w.off1 != null && w.off1 > w.off0 ? 1 - cl((Y - w.off0) / (w.off1 - w.off0)) : Y < w.off0 ? 1 : 0; return g * o; }
// thời điểm (giây cảnh) đường cong đi qua năm Y (cả hai chiều) — quét theo khung
export function crossings(tl, Y, T, fps = 24) { const out = []; let p = tl.year(0); for (let f = 1; f <= Math.round(T * fps); f++) { const t = f / fps, y = tl.year(t); if ((p - Y) * (y - Y) <= 0 && p !== y) out.push(+(t - (y - Y) / (y - p) / fps).toFixed(3)); p = y; } return out; }

// ---------- 3. trại lều ----------
//  spec: {pts: [[E,N],[E,N]…] (trục dãy trại), rows (số hàng lều song song), gap (m giữa lều dọc hàng), rowGap (m giữa hàng), w: {on, full, off0, off1}, w2 + frac (phần lều theo cửa sổ thứ hai), color, seed, side}
//  Lều = lều mái chữ A vải lanh (cao 2,1 m, dài 3 m, rộng 2,4 m) — hình theo bản khắc/tranh vây hãm (Drinkwater 1786 'View of the Spanish batteries', Copley) bậc 4; số lều theo quân số bậc 2.
export function camps(specs, ctx, opt = {}) {   // V7C (việc 2d): opt.hangLoi — lều mọc theo HÀNG LỐI từ đầu dãy (phần đã dựng kín hàng, như dải trại Faden 1783) thay vì rải ngẫu nhiên khắp dãy; dải đất giẫm dài theo phần đã dựng
  const hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3), group = new THREE.Group(), all = [];
  const g = new THREE.BufferGeometry(), L = 3.0, Wd = 2.4, Hh = 2.1;
  const P = [-L / 2, 0, -Wd / 2, L / 2, 0, -Wd / 2, L / 2, Hh, 0, -L / 2, 0, -Wd / 2, L / 2, Hh, 0, -L / 2, Hh, 0,  -L / 2, 0, Wd / 2, -L / 2, Hh, 0, L / 2, Hh, 0, -L / 2, 0, Wd / 2, L / 2, Hh, 0, L / 2, 0, Wd / 2,
    L / 2, 0, -Wd / 2, L / 2, 0, Wd / 2, L / 2, Hh, 0, -L / 2, 0, Wd / 2, -L / 2, 0, -Wd / 2, -L / 2, Hh, 0];
  g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.computeVertexNormals();
  for (const sp of specs || []) { const R = rng(sp.seed || 1779), rows = sp.rows || 3, gap = sp.gap || 4.2, rg = sp.rowGap || 5.5, C = [0];
    for (let i = 1; i < sp.pts.length; i++) C.push(C[i - 1] + Math.hypot(sp.pts[i][0] - sp.pts[i - 1][0], sp.pts[i][1] - sp.pts[i - 1][1]));
    const len = C[C.length - 1];
    for (let s = 0; s < len; s += gap) { let i = 1; while (i < sp.pts.length - 1 && C[i] < s) i++; const a = sp.pts[i - 1], b = sp.pts[i], u = (s - C[i - 1]) / ((C[i] - C[i - 1]) || 1), dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1;
      for (let r = 0; r < rows; r++) { const o = (r - (rows - 1) / 2) * rg + (r >= rows / 2 ? 2.5 : 0), e = a[0] + dx * u - dn / l * o + (R() - 0.5) * 0.6, n = a[1] + dn * u + dx / l * o + (R() - 0.5) * 0.6;
        if (ctx.terr.hAt(e, n) < 0.5) continue; all.push({ sp, e, n, hd: Math.atan2(dn, dx) + Math.PI / 2 + (R() - 0.5) * 0.06, s: s / len, k: 0.9 + 0.2 * R(), j: opt.hangLoi ? Math.min(0.999, s / len + 0.004 * R()) : R() }); } } }
  // nền trại: dải đất giẫm (đất trơ, nhạt) dưới mỗi dãy — đọc được từ xa như dải trại trên bản đồ; hiện theo k của dãy (vật nền phụ, bậc 5)
  const grounds = []; for (const sp of specs || []) { const a = sp.pts[0], b = sp.pts[sp.pts.length - 1], dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1, wd = (sp.rows || 3) * (sp.rowGap || 5.5) + 12, nx = -dn / l * wd / 2, nn = dx / l * wd / 2;
    const P = [], N = 24; for (let i = 0; i <= N; i++) for (const sg of [-1, 1]) { const e = a[0] + dx * i / N - dx / l * 6 + nx * sg, n = a[1] + dn * i / N - dn / l * 6 + nn * sg; P.push(e, hAt(e, n) + 0.3, -n); }
    const I = []; for (let i = 0; i < N; i++) { const k = i * 2; I.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    const gg = new THREE.BufferGeometry(); gg.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); gg.setIndex(I); gg.computeVertexNormals();
    const gm = new THREE.MeshLambertMaterial({ color: '#cdb98f', transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -3 }); maskify(gm, ctx.U, 1);
    const gmesh = new THREE.Mesh(gg, gm); gmesh.receiveShadow = true; gmesh.renderOrder = 2; group.add(gmesh); grounds.push({ sp, gm, gmesh }); }
  const kOf = (sp, year) => (sp.w2 ? sp.frac * win(year, sp.w) + (1 - sp.frac) * win(year, sp.w2) : win(year, sp.w));
  const byC = {}; for (const q of all) { const c = q.sp.color || '#e9e3d3'; (byC[c] = byC[c] || []).push(q); }
  const meshes = [];
  for (const [c, Q] of Object.entries(byC)) { const m = new THREE.MeshLambertMaterial({ color: new THREE.Color(c), side: THREE.DoubleSide }); maskify(m, ctx.U, 1);
    const im = new THREE.InstancedMesh(g, m, Q.length); im.castShadow = im.receiveShadow = true; im.frustumCulled = false; group.add(im); meshes.push({ im, Q }); }
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), sc = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0);
  let shown = 0;
  return { group, n: all.length, stat: () => ({ leu: all.length, hien: shown }),
    update(year) { shown = 0; for (const g of grounds) { if (opt.hangLoi) { const kk = kOf(g.sp, year); g.gm.opacity = 0.8 * Math.min(1, kk * 12); g.gmesh.visible = kk > 0.005; g.gmesh.geometry.setDrawRange(0, 6 * Math.max(1, Math.ceil(24 * Math.min(1, kk + 0.02)))); continue; }
      const k = Math.min(1, kOf(g.sp, year) * 2.2); g.gm.opacity = 0.8 * k; g.gmesh.visible = k > 0.01; }
      for (const { im, Q } of meshes) { Q.forEach((p, i) => { const k = kOf(p.sp, year), on = p.j < k;   // lều mọc ngẫu nhiên tất định theo k (trại dựng dần), rút cùng thứ tự
        v.set(p.e, hAt(p.e, p.n) - 0.05, -p.n); q.setFromAxisAngle(Y, p.hd); const s = on ? p.k : 0; sc.set(s, s, s); m4.compose(v, q, sc); im.setMatrixAt(i, m4); shown += on ? 1 : 0; }); im.instanceMatrix.needsUpdate = true; } } };
}

// ---------- 4. đèn đêm ----------
function glowTex(warm) { const S = 64, cv = document.createElement('canvas'); cv.width = cv.height = S; const g2 = cv.getContext('2d'), gr = g2.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.18, warm ? 'rgba(255,214,150,0.55)' : 'rgba(225,235,255,0.55)'); gr.addColorStop(1, 'rgba(255,200,140,0)'); g2.fillStyle = gr; g2.fillRect(0, 0, S, S);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; }
//  spec: {pts: [[E,N,cao, kiểu]…] kiểu 'pho' (đèn đường, ấm) | 'rw' (đèn mép đường băng, trắng) | 'th' (đèn ngưỡng, xanh) | 'fire' (lửa, cam), w (cửa sổ năm), size}
export function lamps(specs, ctx) {
  const group = new THREE.Group(), hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3), T = { warm: glowTex(true), cool: glowTex(false) }, list = [];
  const COL = { pho: [1.0, 0.82, 0.58], rw: [0.95, 0.97, 1.0], th: [0.55, 1.0, 0.6], fire: [1.0, 0.55, 0.22] };
  for (const sp of specs || []) {
    const pts = sp.pts, n = pts.length, kind = sp.kind || 'pho', col = COL[kind], sz = sp.size || (kind === 'pho' ? 5 : kind === 'fire' ? 40 : 3.2);
    const geo = new THREE.BufferGeometry(), P = new Float32Array(n * 3); pts.forEach(([e, nn, h], i) => { P[i * 3] = e; P[i * 3 + 1] = hAt(e, nn) + (h ?? (kind === 'pho' ? 7.5 : kind === 'fire' ? sz * 0.15 : 0.6)); P[i * 3 + 2] = -nn; });
    geo.setAttribute('position', new THREE.BufferAttribute(P, 3));
    const m = new THREE.PointsMaterial({ map: kind === 'rw' || kind === 'th' ? T.cool : T.warm, color: new THREE.Color(...col), size: sz, sizeAttenuation: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false, opacity: 0 });
    const pt = new THREE.Points(geo, m); pt.renderOrder = 7; pt.frustumCulled = false; group.add(pt);
    // vệt sáng mặt đất (đèn đường): đĩa cộng sáng bán kính 11 m dưới mỗi đèn
    let pool = null;
    if (kind === 'pho' || kind === 'fire') { const r = kind === 'fire' ? Math.min(45, sz * 0.4) : 7.5, pg = new THREE.PlaneGeometry(2 * r, 2 * r).rotateX(-Math.PI / 2), pm = new THREE.MeshBasicMaterial({ map: T.warm, color: new THREE.Color(...col).multiplyScalar(kind === 'fire' ? 0.5 : 0.16), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false, opacity: 0, polygonOffset: true, polygonOffsetFactor: -6, polygonOffsetUnits: -6 });
      pool = new THREE.InstancedMesh(pg, pm, n); const m4 = new THREE.Matrix4(); pts.forEach(([e, nn], i) => { m4.makeTranslation(e, hAt(e, nn) + 0.35, -nn); pool.setMatrixAt(i, m4); }); pool.renderOrder = 6; pool.frustumCulled = false; group.add(pool); }
    list.push({ sp, pt, m, pool });
  }
  return { group, n: list.reduce((a, l) => a + l.sp.pts.length, 0),
    update(night, year, t = 0) { for (const l of list) { const k = (l.sp.kind === 'fire' ? (0.45 + 0.55 * night) * (0.85 + 0.15 * Math.sin(t * 9.1 + l.sp.pts.length)) : night) * win(year, l.sp.w); l.m.opacity = Math.min(1, k * (l.sp.gain ?? 1)); l.pt.visible = k > 0.01;
      if (l.pool) { l.pool.material.opacity = k; l.pool.visible = k > 0.01; } } } };
}

// ---------- 5. hàng rào ----------
export function fence(pts, ctx, { w = null, h = 2.4, step = 3.0, color = '#8b8478' } = {}) {
  const hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3), group = new THREE.Group(), C = [0]; for (let i = 1; i < pts.length; i++) C.push(C[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const len = C[C.length - 1], posts = []; for (let s = 0; s <= len; s += step) { let i = 1; while (i < pts.length - 1 && C[i] < s) i++; const a = pts[i - 1], b = pts[i], u = (s - C[i - 1]) / ((C[i] - C[i - 1]) || 1); posts.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, s / len]); }
  const pm = new THREE.MeshLambertMaterial({ color }); maskify(pm, ctx.U, 1); const pg = new THREE.BoxGeometry(0.12, h, 0.12).translate(0, h / 2, 0);
  const im = new THREE.InstancedMesh(pg, pm, posts.length); im.castShadow = true; im.frustumCulled = false; group.add(im);
  // lưới: dải mảnh bán trong giữa các cọc
  const P = [], S = []; for (let i = 0; i < posts.length - 1; i++) { const [a, b] = [posts[i], posts[i + 1]], ya = hAt(a[0], a[1]), yb = hAt(b[0], b[1]);
    P.push(a[0], ya + 0.1, -a[1], b[0], yb + 0.1, -b[1], b[0], yb + h * 0.92, -b[1], a[0], ya + 0.1, -a[1], b[0], yb + h * 0.92, -b[1], a[0], ya + h * 0.92, -a[1]); S.push(a[2], b[2], b[2], a[2], b[2], a[2]); }
  const mg = new THREE.BufferGeometry(); mg.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); mg.setAttribute('aS', new THREE.Float32BufferAttribute(S, 1)); mg.computeVertexNormals();
  const mm = new THREE.MeshLambertMaterial({ color: '#6f6a62', transparent: true, opacity: 0.38, side: THREE.DoubleSide, depthWrite: false }); maskify(mm, ctx.U, 1);
  const uK = { value: 1 }; mm.onBeforeCompile = (sh) => { sh.uniforms.uK = uK; sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aS; varying float vS;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvS = aS;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uK; varying float vS;').replace('#include <color_fragment>', '#include <color_fragment>\nif (vS > uK) discard;'); };
  mm.customProgramCacheKey = () => 'tl7-fence'; const mesh = new THREE.Mesh(mg, mm); group.add(mesh);
  const m4 = new THREE.Matrix4();
  return { group, len, update(year) { const k = win(year, w); uK.value = k; mesh.visible = k > 0; posts.forEach((p, i) => { m4.makeScale(p[2] <= k ? 1 : 0, p[2] <= k ? 1 : 0, p[2] <= k ? 1 : 0); m4.setPosition(p[0], hAt(p[0], p[1]), -p[1]); im.setMatrixAt(i, m4); }); im.instanceMatrix.needsUpdate = true; } };
}

// ---------- 6. nhật ký trôi máy (TL-1: ≤ 2 % khung/giây) ----------
//  độ trôi = tốc độ góc của hướng nhìn (°/s) ÷ FOV ngang + tốc độ dịch điểm nhìn chiếu lên khung — gần đúng: |Δhướng|/fovH + |Δvị trí| / (2·d·tan(fovH/2))
export function driftPct(path, t0, t1, aspect = 16 / 9) { let mx = 0; const dt = 0.25;
  for (let t = t0; t < t1 - dt; t += dt) { const a = path.at(t), b = path.at(t + dt), fv = a.fov * Math.PI / 180, fh = 2 * Math.atan(Math.tan(fv / 2) * aspect);
    const da = [a.l[0] - a.p[0], a.l[1] - a.p[1], a.l[2] - a.p[2]], db = [b.l[0] - b.p[0], b.l[1] - b.p[1], b.l[2] - b.p[2]], na = Math.hypot(...da), nb = Math.hypot(...db);
    const ang = Math.acos(Math.max(-1, Math.min(1, (da[0] * db[0] + da[1] * db[1] + da[2] * db[2]) / (na * nb)))), mv = Math.hypot(b.p[0] - a.p[0], b.p[1] - a.p[1], b.p[2] - a.p[2]);
    const zoom = Math.abs(b.fov - a.fov) / a.fov;
    mx = Math.max(mx, (ang / fh + mv / (2 * na * Math.tan(fh / 2)) + zoom) / dt * 100); }
  return +mx.toFixed(2); }

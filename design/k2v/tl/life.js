// K2V tl · V5b-2c · LỚP SỐNG `song` (lệnh F1/F3 chủ dự án 17/10: "mọi cảnh 3D có ≥ 3 vật chuyển động: người/xe/tàu/khói/chim/cờ").
// Một lớp gom các vật chuyển động nền theo THỜI GIAN CẢNH (giây, tất định — không Math.random), để cảnh không bao giờ "đứng hình":
//   · birds    — đàn hải âu bay vòng (cánh vỗ), cao 25–90 m; nền (mặt nạ 0);
//   · walkers  — người A-lite đi dọc tuyến phố/tường (thân + mũ, cao 1,75 m, 1,1–1,5 m/s, nhấp nhô bước), màu áo theo nhóm; KHÔNG cận mặt (cảnh tự giữ máy ≥ 10 m);
//   · boats    — thuyền nhỏ chèo/buồm chạy theo tuyến trên vịnh, vệt sóng sau lái (cùng kiểu thân với ships.js);
//   · chimney  — khói bếp mảnh (khói M7 kiểu nhạt) từ mái nhà chọn tất định.
// Luật hình chiến tranh §6.2 giữ ở cảnh: không người trong vùng khói (update nhận zones như layers.units), không người ngã/chết.
// stat() trả số vật chuyển động đang hiện theo loại → log cho K (song_n ≥ 3).
import { THREE, rng, maskify } from './core.js';
import { smoke } from './layers.js';
import { makeKit, makeSet, walkerLook } from './people.js';   // V6: người có khớp + chu kỳ đi

const cum = (pts) => { const c = [0]; for (let i = 1; i < pts.length; i++) c.push(c[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])); return c; };
function along(pts, C, s) { const L = C[C.length - 1]; s = ((s % L) + L) % L; let i = 1; while (i < pts.length - 1 && C[i] < s) i++; const a = pts[i - 1], b = pts[i], u = (s - C[i - 1]) / ((C[i] - C[i - 1]) || 1);
  return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, Math.atan2(b[1] - a[1], b[0] - a[0])]; }

export function life(spec, ctx) {
  const group = new THREE.Group(), parts = [], R = rng(spec.seed || 404), hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), sc = new THREE.Vector3(1, 1, 1), Y = new THREE.Vector3(0, 1, 0), X = new THREE.Vector3(1, 0, 0);
  // --- chim ---
  if (spec.birds) for (const b of [].concat(spec.birds)) {
    const n = b.n || 14, wing = new THREE.BufferGeometry(); wing.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, -0.18, 0, 0, 0.18, 0.95 * (b.size || 1), 0, 0], 3)); wing.computeVertexNormals();
    const mat = new THREE.MeshLambertMaterial({ color: 0xf2f0ea, side: THREE.DoubleSide }); maskify(mat, ctx.U, 0);
    const L_ = new THREE.InstancedMesh(wing, mat, n), Rw = new THREE.InstancedMesh(wing, mat, n); group.add(L_, Rw);
    const B = [...Array(n).keys()].map(() => ({ ph: R() * 6.28, r: (b.r || 120) * (0.6 + 0.6 * R()), h: (b.h || 50) * (0.6 + 0.8 * R()), w: (0.18 + 0.12 * R()) * (R() < 0.5 ? 1 : -1), f: 3.5 + 2 * R() }));
    parts.push({ kind: 'chim', n, update(t) { B.forEach((o, i) => { const a = o.ph + o.w * t, e = b.c[0] + Math.cos(a) * o.r, nn = b.c[1] + Math.sin(a) * o.r, flap = Math.sin(t * o.f + o.ph) * 0.7;
      const hd = a + Math.sign(o.w) * 1.5708; v.set(e, (b.base ?? 0) + o.h + Math.sin(t * 0.7 + o.ph) * 3, -nn); const s = (b.size || 1) * 1.6;
      for (const [M, sd] of [[L_, 1], [Rw, -1]]) { q.setFromAxisAngle(Y, hd).multiply(new THREE.Quaternion().setFromAxisAngle(X, sd * flap)); if (sd < 0) q.multiply(new THREE.Quaternion().setFromAxisAngle(Y, Math.PI)); sc.set(s, s, s); m4.compose(v, q, sc); M.setMatrixAt(i, m4); } });
      L_.instanceMatrix.needsUpdate = Rw.instanceMatrix.needsUpdate = true; return n; } });
  }
  // --- V6: người đi bộ / đám đông = người low-poly có khớp (people.js), bước chân theo tốc độ; cùng tuyến, cùng luật near/khói như bản cũ ---
  if (ctx.v6people && (spec.walkers || spec.crowds)) {
    const kit = ctx.peopleKit || (ctx.peopleKit = makeKit(ctx));
    const mkSets = (list) => { const by = {}; for (const p of list) { const k = p.kind + '|' + p.uni; (by[k] = by[k] || { kind: p.kind, uni: p.uni, L: [] }).L.push(p); }
      return Object.values(by).map((G) => { const S = makeSet(kit, ctx, { kind: G.kind, n: G.L.length, lodPx: 22 }); G.L.forEach((p, i) => { p.i = i; p.S = S; S.look(i, G.uni, p.R, { gait: p.gait, freq: p.freq }); }); group.add(S.group); return S; }); };
    for (const w of [].concat(spec.walkers || [])) {
      const C = cum(w.pts), n = w.n || 30, cols = w.colors || ['#b8402f', '#6b5a48', '#d8d0bc', '#3b4a5c'];
      const P = [...Array(n).keys()].map((k) => { const sp = (1.1 + 0.4 * R()) * (R() < 0.5 ? 1 : -1), [kind, uni] = walkerLook(cols[Math.floor(R() * cols.length)], R, w.women !== false, spec.era ?? 1782); return { s: R() * C[C.length - 1], sp, lat: (R() - 0.5) * (w.width || 5), kind, uni, R: rng((spec.seed || 404) * 7 + k), gait: 1, freq: Math.abs(sp) / 1.45 }; });
      const sets = mkSets(P); let shown = 0;
      parts.push({ kind: 'nguoi', n, update(t, zones) { shown = 0; const cp = ctx.cam ? ctx.cam.position : null; for (const S of sets) S.begin();
        for (const p of P) { const [e0, n0, hd] = along(w.pts, C, p.s + p.sp * t), nn = [-Math.sin(hd), Math.cos(hd)], e = e0 + nn[0] * p.lat, n_ = n0 + nn[1] * p.lat;
          const far = w.near && cp && Math.hypot(e - cp.x, n_ + cp.z, (w.y != null ? w.y : 0) - cp.y) > w.near, hidden = far || (zones && zones.some((z) => Math.hypot(e - z.c[0], n_ - z.c[1]) < z.r + 15));
          if (!hidden) { p.S.put(p.i, e, w.y != null ? w.y : hAt(e, n_), n_, hd + (p.sp < 0 ? Math.PI : 0), true, w.scale || 1); shown++; } }
        for (const S of sets) S.end(); return shown; } });
    }
    for (const cw of [].concat(spec.crowds || [])) {
      const C = cum(cw.pts), L = C[C.length - 1], cols = cw.colors || ['#b03a2e', '#e7e0cf', '#5e4a38'], M = [];
      for (let g = 0; g < (cw.groups || 8); g++) { const s0 = (g + R() * 0.6) / (cw.groups || 8) * L, sz = Math.round((cw.size || [12, 40])[0] + R() * ((cw.size || [12, 40])[1] - (cw.size || [12, 40])[0])), sp = (cw.speed || 0.6) * (R() < 0.5 ? 1 : -1) * (0.6 + 0.6 * R());
        const rad = Math.sqrt(sz) * 0.55; for (let k = 0; k < sz; k++) { const a = R() * 6.283, rr = Math.sqrt(R()) * rad, [kind, uni] = walkerLook(cols[Math.floor(R() * cols.length)], R, cw.women !== false, spec.era ?? 1782), stand = R() < 0.3;
          M.push({ g, s0, sp, dx: Math.cos(a) * rr * 1.6, dy: Math.sin(a) * rr * 0.8, kind, uni, ph: R() * 6.28, R: rng((spec.seed || 404) * 13 + M.length), gait: stand ? 0 : 1, freq: Math.abs(sp) / 1.2 + 0.2 }); } }
      const sets = mkSets(M);
      parts.push({ kind: 'dam_dong', n: M.length, update(t, zones) { let shown = 0; for (const S of sets) S.begin();
        for (const p of M) { const [e0, n0, hd] = along(cw.pts, C, p.s0 + p.sp * t), u = [Math.cos(hd), Math.sin(hd)], e = e0 + u[0] * p.dx - u[1] * p.dy, n_ = n0 + u[1] * p.dx + u[0] * p.dy;
          const hidden = zones && zones.some((z) => Math.hypot(e - z.c[0], n_ - z.c[1]) < z.r + 15); if (hidden) continue;
          p.S.put(p.i, e, hAt(e, n_), n_, hd + (p.sp < 0 ? Math.PI : 0) + Math.sin(p.ph) * (p.gait ? 0.3 : 1.6), true, 1); shown++; }
        for (const S of sets) S.end(); return shown; } });
    }
  }
  // --- người đi bộ ---
  if (spec.walkers && !ctx.v6people) {
    const body = new THREE.BoxGeometry(0.5, 1.35, 0.34).translate(0, 0.68, 0), hat = new THREE.BoxGeometry(0.44, 0.28, 0.44).translate(0, 1.54, 0);
    for (const w of [].concat(spec.walkers)) {
      const C = cum(w.pts), n = w.n || 30, cols = w.colors || ['#b8402f', '#6b5a48', '#d8d0bc', '#3b4a5c'];
      const P = [...Array(n).keys()].map(() => ({ s: R() * C[C.length - 1], sp: (1.1 + 0.4 * R()) * (R() < 0.5 ? 1 : -1), lat: (R() - 0.5) * (w.width || 5), col: Math.floor(R() * cols.length), ph: R() * 6.28 }));
      const byC = cols.map((c, k) => { const S = P.filter((p) => p.col === k); const mb = new THREE.MeshLambertMaterial({ color: new THREE.Color(c) }), mh = new THREE.MeshLambertMaterial({ color: 0x1e1b18 }); maskify(mb, ctx.U, 1); maskify(mh, ctx.U, 1);
        const ib = new THREE.InstancedMesh(body, mb, Math.max(1, S.length)), ih = new THREE.InstancedMesh(hat, mh, Math.max(1, S.length)); ib.castShadow = ih.castShadow = true; group.add(ib, ih); return { S, ib, ih }; });
      let shown = 0;
      // V5b-2d (C2-7): w.near (m) — người ĐƠN chỉ hiện trong tầm near quanh máy; xa hơn → ẩn (đám đông ở tầm xa do spec.crowds đảm nhận, không phóng to người)
      parts.push({ kind: 'nguoi', n, update(t, zones) { shown = 0; const cp = ctx.cam ? ctx.cam.position : null; for (const { S, ib, ih } of byC) { S.forEach((p, i) => { const [e0, n0, hd] = along(w.pts, C, p.s + p.sp * t), nn = [-Math.sin(hd), Math.cos(hd)], e = e0 + nn[0] * p.lat, n_ = n0 + nn[1] * p.lat;
          const far = w.near && cp && Math.hypot(e - cp.x, n_ + cp.z, (w.y != null ? w.y : 0) - cp.y) > w.near;
          const hidden = far || (zones && zones.some((z) => Math.hypot(e - z.c[0], n_ - z.c[1]) < z.r + 15)); const k = w.scale || 1;
          v.set(e, (w.y != null ? w.y : hAt(e, n_)) + Math.abs(Math.sin(t * 7 + p.ph)) * 0.06, -n_); q.setFromAxisAngle(Y, hd + (p.sp < 0 ? Math.PI : 0)); sc.set(hidden ? 0 : k, hidden ? 0 : k, hidden ? 0 : k); m4.compose(v, q, sc); ib.setMatrixAt(i, m4); ih.setMatrixAt(i, m4); shown += hidden ? 0 : 1; });
          ib.instanceMatrix.needsUpdate = ih.instanceMatrix.needsUpdate = true; } return shown; } });
    }
  }
  // --- V5b-2d (C2-7): ĐÁM ĐÔNG — cụm người dày đi chậm theo tuyến (đọc được ở tầm ≥ 150 m mà KHÔNG phóng to người: cụm 12–60 người, cách 0,8 m) ---
  if (spec.crowds && !ctx.v6people) {
    const body = new THREE.BoxGeometry(0.5, 1.35, 0.34).translate(0, 0.68, 0), hat = new THREE.BoxGeometry(0.44, 0.28, 0.44).translate(0, 1.54, 0);
    for (const cw of [].concat(spec.crowds)) {
      const C = cum(cw.pts), L = C[C.length - 1], cols = cw.colors || ['#b03a2e', '#e7e0cf', '#5e4a38'], M = [];
      for (let g = 0; g < (cw.groups || 8); g++) { const s0 = (g + R() * 0.6) / (cw.groups || 8) * L, sz = Math.round((cw.size || [12, 40])[0] + R() * ((cw.size || [12, 40])[1] - (cw.size || [12, 40])[0])), sp = (cw.speed || 0.6) * (R() < 0.5 ? 1 : -1) * (0.6 + 0.6 * R());
        const rad = Math.sqrt(sz) * 0.55; for (let k = 0; k < sz; k++) { const a = R() * 6.283, rr = Math.sqrt(R()) * rad; M.push({ g, s0, sp, dx: Math.cos(a) * rr * 1.6, dy: Math.sin(a) * rr * 0.8, col: Math.floor(R() * cols.length), ph: R() * 6.28 }); } }
      const byC = cols.map((c, k) => { const S = M.filter((p) => p.col === k); const mb = new THREE.MeshLambertMaterial({ color: new THREE.Color(c) }), mh = new THREE.MeshLambertMaterial({ color: 0x1e1b18 }); maskify(mb, ctx.U, 1); maskify(mh, ctx.U, 1);
        const ib = new THREE.InstancedMesh(body, mb, Math.max(1, S.length)), ih = new THREE.InstancedMesh(hat, mh, Math.max(1, S.length)); ib.castShadow = ih.castShadow = true; group.add(ib, ih); return { S, ib, ih }; });
      parts.push({ kind: 'dam_dong', n: M.length, update(t, zones) { let shown = 0; for (const { S, ib, ih } of byC) { S.forEach((p, i) => { const [e0, n0, hd] = along(cw.pts, C, p.s0 + p.sp * t), u = [Math.cos(hd), Math.sin(hd)], e = e0 + u[0] * p.dx - u[1] * p.dy, n_ = n0 + u[1] * p.dx + u[0] * p.dy;
          const hidden = zones && zones.some((z) => Math.hypot(e - z.c[0], n_ - z.c[1]) < z.r + 15); v.set(e, hAt(e, n_) + Math.abs(Math.sin(t * 6 + p.ph)) * 0.04, -n_); q.setFromAxisAngle(Y, hd + (p.sp < 0 ? Math.PI : 0) + Math.sin(p.ph) * 0.6);
          sc.set(hidden ? 0 : 1, hidden ? 0 : 1, hidden ? 0 : 1); m4.compose(v, q, sc); ib.setMatrixAt(i, m4); ih.setMatrixAt(i, m4); shown += hidden ? 0 : 1; }); ib.instanceMatrix.needsUpdate = ih.instanceMatrix.needsUpdate = true; } sc.set(1, 1, 1); return shown; } });
    }
  }
  // --- thuyền nhỏ + vệt sóng ---
  if (spec.boats) for (const bt of [].concat(spec.boats)) {
    const C = cum(bt.pts), g = new THREE.Group(), len = bt.len || 9, mk = (geo, c, x, y, z) => { const mm = new THREE.MeshLambertMaterial({ color: c }); maskify(mm, ctx.U, 1); const o = new THREE.Mesh(geo, mm); o.position.set(x, y, z); o.castShadow = true; g.add(o); return o; };
    const sh = new THREE.Shape(), hl = len / 2, hb = len * 0.16; sh.moveTo(-hl, -hb * 0.8); sh.lineTo(hl * 0.55, -hb); sh.quadraticCurveTo(hl, -hb * 0.4, hl, 0); sh.quadraticCurveTo(hl, hb * 0.4, hl * 0.55, hb); sh.lineTo(-hl, hb * 0.8); sh.lineTo(-hl, -hb * 0.8);
    mk(new THREE.ExtrudeGeometry(sh, { depth: 1.4, bevelEnabled: false }).rotateX(-Math.PI / 2), bt.color || 0x5a3b26, 0, -0.5, 0);
    if (bt.sail) { mk(new THREE.CylinderGeometry(0.08, 0.1, len * 0.9, 4), 0x3a2a1e, 0, len * 0.45, 0); mk(new THREE.BoxGeometry(len * 0.5, len * 0.62, 0.08), 0xeee6d2, -len * 0.05, len * 0.45, 0); }
    else for (let k = -2; k <= 2; k++) mk(new THREE.BoxGeometry(0.08, 0.08, len * 0.5), 0x3a2a1e, k * len * 0.12, 0.9, 0);   // mái chèo
    const wm = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.55, depthWrite: false }); maskify(wm, ctx.U, 0);
    const wake = new THREE.Mesh(new THREE.PlaneGeometry(len * 3.5, len * 0.5).rotateX(-Math.PI / 2).translate(-len * 2.1, 0.12, 0), wm); g.add(wake); group.add(g);
    const sp = bt.speed || 3, s0 = (bt.s0 ?? R()) * C[C.length - 1];
    parts.push({ kind: 'tau', n: 1, update(t) { const [e, n_, hd] = along(bt.pts, C, s0 + sp * t); g.position.set(e, Math.sin(t * 1.3 + s0) * 0.15, -n_); g.rotation.y = hd + (bt.sail ? Math.sin(t * 0.8) * 0.03 : 0); wm.opacity = 0.45 + 0.1 * Math.sin(t * 3 + s0); return 1; } });
  }
  // --- khói bếp ---
  let CH = null;
  if (spec.chimney && spec.chimney.at && spec.chimney.at.length) {
    CH = smoke(spec.chimney.at.map(([e, y, n], i) => ({ at: [e, y, n], t: [-1e6, 1e6], n: 5, size: 7, rise: 26, drift: spec.chimney.drift || [-1.2, 0.3], period: 6 + (i % 5), seed: 900 + i, alpha: 0.42 })), ctx);
    group.add(CH.group); parts.push({ kind: 'khoi', n: spec.chimney.at.length, update(t) { CH.update(t); return spec.chimney.at.length; } });
  }
  let last = {};
  return { group, smokeGroup: CH ? CH.group : null,
    update(t, zones = []) { last = {}; for (const p of parts) last[p.kind] = (last[p.kind] || 0) + p.update(t, zones); return last; },
    stat: () => Object.assign({ loai: Object.keys(last).filter((k) => last[k] > 0).length }, last) };
}

// chọn tất định n nóc nhà (đỉnh tường + 2 m) từ bản ghi footprint (layers footprints → records), tránh vùng box [e0, n0, e1, n1] nếu có
export function chimneysFrom(recs, n, R = rng(77), skip = null) {
  const out = [], cand = recs.filter((r) => r[6] && r[6].length > 2);
  for (let k = 0; k < n * 4 && out.length < n; k++) { const r = cand[Math.floor(R() * cand.length)]; if (!r) break; const p = r[6][Math.floor(R() * r[6].length)];
    const c = [r[6].reduce((a, q) => a + q[0], 0) / r[6].length, r[6].reduce((a, q) => a + q[1], 0) / r[6].length], e = c[0] * 0.6 + p[0] * 0.4, nn = c[1] * 0.6 + p[1] * 0.4;
    if (skip && e > skip[0] && e < skip[2] && nn > skip[1] && nn < skip[3]) continue; out.push([e, (r[3] || 0) + 9, nn]); }
  return out;
}

// dời tuyến đi bộ (vd tim Main Street OSM) sang hành lang TRỐNG gần nhất giữa các khối footprint (plan 1782 lệch RMS ~21 m so OSM → tim OSM có đoạn nằm trong khối)
export function freePath(pts, recs, maxOff = 40, step = 2) {
  const rings = recs.map((r) => r[6]).filter((r) => r && r.length > 2), inside = (p) => rings.some((r) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > p[1]) !== (r[j][1] > p[1]) && p[0] < (r[j][0] - r[i][0]) * (p[1] - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; });
  const dense = []; for (let i = 0; i < pts.length - 1; i++) { const a = pts[i], b = pts[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(1, Math.round(L / 10)); for (let k = 0; k < n; k++) dense.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]); } dense.push(pts[pts.length - 1]);
  let prev = 0; const out = [];
  for (let i = 0; i < dense.length; i++) { const a = dense[Math.max(0, i - 1)], b = dense[Math.min(dense.length - 1, i + 1)], d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1, nn = [-d[1] / l, d[0] / l];
    let best = null; search: for (let o = 0; o <= 2 * maxOff; o += step) for (const sg of [1, -1]) { const off = prev + sg * o; if (Math.abs(off) > maxOff) continue; const q = [dense[i][0] + nn[0] * off, dense[i][1] + nn[1] * off]; if (!inside(q)) { best = off; break search; } }
    if (best == null) continue; prev = best; out.push([dense[i][0] + nn[0] * best, dense[i][1] + nn[1] * best]); }
  return out;
}

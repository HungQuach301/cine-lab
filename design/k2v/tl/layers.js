// K2V tl · V5b-2b · LỚP THEO MỐC cho T3 "vây hãm" (TIEN-KY-VAY-HAM §5): mọi lớp nhận "giá trị thời gian" tv do cảnh chọn (năm thập phân, hoặc giờ trong ngày
// của một cảnh mốc đinh) và tự hiện/ẩn/mọc theo cửa sổ khai báo. Không Math.random (khung tất định). Mặt nạ: footprint = nội dung; bản đồ pha, khói = nền;
// chiến tuyến / mũi tên = nội dung (là hình học có nghĩa của cảnh).
//  · M9  footprints(specs)  — lớp nhà nạp bằng scripts/k2tl/load_footprints.py (OSM / Catastro / ghost GeoJSON), mái theo thời kỳ (city.js styleOf pd), cửa sổ năm;
//  · M12 phaseMaps(specs)   — raster ĐÃ NẮN (hộp ENU) phủ địa hình làm vân mặt đất, crossfade theo mốc (fade năm), lưới bám DTM;
//  · M4  frontLines(specs)  — chiến tuyến/hào MỌC theo thời gian (dải hạ thấp + gờ đất trên DTM), dải màu phe;
//  · M1  arrows(specs)      — mũi tên ruy băng bám địa hình, mọc theo thời gian (màu trung tính cho dân thường);
//  · M7  smoke(specs)       — khói/lửa sprite 2D (billboard + tích luỹ SPP); cảnh phải KHÔNG đặt người trong vùng khói (luật §6.2) — lớp ghi vùng khói để kiểm.
import { THREE, rng, loadJSON, maskify } from './core.js';
import { makeCity } from './city.js';
import { walls, roof } from './geom.js';
import { fortify, wallRing } from './fort.js';   // V5b-2c: M5 thành luỹ tham số

// V5b-2c: màu phe theo B6 (chủ dự án duyệt 17/10, cố định cả series, BD-7 — 3D và bản đồ chiến lược cùng một màu): Anh đỏ gạch, TBN vàng đất, Pháp lam; dân thường kem
export const FACTION = { es: '#c9a227', fr: '#2e5c8a', gb: '#b03a2e', civ: '#efe6cf', neutral: '#a89f8a' };   // nhận diện kênh: cam = Pháp–TBN, lục lam = đồn trú; KHÔNG đỏ máu (§6.2)
const win = (tv, w, fade = 0) => { if (!w) return 1; const [a, b] = w; if (fade <= 0) return tv >= a && tv <= b ? 1 : 0; return Math.max(0, Math.min(1, (tv - a) / fade + 1, (b - tv) / fade + 1)); };

// ---------- công sự (bastion / tường thành): footprint đùn bằng đá vôi, mặt sàn pháo phẳng, tường chắn mái có lỗ châu mai — KHÔNG dựng như nhà ở ----------
//  (M5 thành luỹ tham số là P2; đây là bản rút gọn đủ đúng: cao h tường ốp đá, tường chắn 1,6 m dày 2 m, lỗ châu mai mỗi 7 m)
function fortMesh(recs, ctx, hid) {
  const P = [], N = [], C = [], tri = (r) => THREE.ShapeUtils.triangulateShape(r.map(([x, y]) => new THREE.Vector2(x, y)), []), R = rng(31);
  const emit = (col) => (x, y, z, nx, ny, nz) => { P.push(x, y, z); N.push(nx, ny, nz); const k = 0.92 + 0.08 * Math.sin(x * 0.7 + z * 0.3) * Math.cos(y * 2.1); C.push(col[0] * k, col[1] * k, col[2] * k); };
  for (const r of recs) { const ring = r[6], base = r[3], h = r[2]; const sh = (x, y, z, nx, ny, nz, ...a) => [x, y + base, z, nx, ny, nz, ...a];
    const lime = [0.80, 0.75, 0.64], top = [0.62, 0.58, 0.50];
    walls(ring, h, (...a) => emit(lime)(...sh(...a)), -6); roof(ring, h, 0, tri, (...a) => emit(top)(...sh(...a)));
    // tường chắn mái: dải trong cách mép 2 m, cao 1,6 m, có khe châu mai (bỏ đoạn 1,2 m mỗi 7 m)
    for (let i = 0; i < ring.length; i++) { const a = ring[i], b = ring[(i + 1) % ring.length], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l < 2) continue;
      for (let s0 = 0; s0 < l; s0 += 7) { const s1 = Math.min(l, s0 + 5.8), A = [a[0] + (b[0] - a[0]) * s0 / l, a[1] + (b[1] - a[1]) * s0 / l], B = [a[0] + (b[0] - a[0]) * s1 / l, a[1] + (b[1] - a[1]) * s1 / l];
        walls([A, B, [B[0] + 0.01, B[1] + 0.01]], h + 1.6, (...q) => emit(lime)(...sh(...q)), h); } } }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3));
  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); maskify(m, ctx.U, 1, hid); const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true;
  const grp = new THREE.Group(); grp.add(o); return { group: grp, update() {} };
}

// ---------- M9: lớp nhà ----------
export async function footprints(specs, ctx) {
  const group = new THREE.Group(), list = [];
  for (const sp of specs || []) {
    const L = await loadJSON(`${ctx.base}layers/${sp.file}.json`);
    const recs = L.records.map((r) => { const base = r[3] != null ? r[3] : Math.min(...r[6].map(([e, n]) => ctx.terr.hAt(e, n))); return [r[0], r[1], r[2], Math.max(0.3, base), r[4], r[5], r[6], r[7]]; });
    if (sp.remap) for (let i = 0; i < recs.length; i++) recs[i] = sp.remap(recs[i]);
    if (sp.largest) { const ar = (q) => Math.abs(q.reduce((a, p, i) => a + p[0] * q[(i + 1) % q.length][1] - q[(i + 1) % q.length][0] * p[1], 0)) / 2; recs.sort((a, b) => ar(b[6]) - ar(a[6])); recs.length = 1; }   // V5b-2c: King's Bastion = vòng lớn nhất (vòng nhỏ trong là toà/bậc thang hiện đại)
    const c = sp.fort ? fortify(recs.map((r) => (sp.h ? Object.assign(r.slice(), { 2: sp.h }) : r)), ctx, Object.assign({ hid: sp.hid || 0 }, sp.fortOpt || {})) : makeCity(recs, ctx.U, { lod: true, hid: sp.hid || 0, ghostDesat: sp.ghostDesat ?? 0.22 }); group.add(c.group);
    list.push({ recs, name: L.name, kind: L.kind, src: sp.src || L.src, years: sp.years || L.years, period: L.period, n: L.n, city: c, yearMax: L.kind === 'ghost' ? (sp.years || L.years)[0] : Math.max(...L.records.map((r) => r[0] < 9999 ? r[0] : 0)) });
  }
  return { group, list,
    update(year, cam) { for (const l of list) { l.city.group.visible = win(year, l.years) > 0; if (l.city.group.visible && cam) l.city.update(cam); } },
    // nam_khung (K-1.13 NC-H5a): năm lớn nhất của phần tử ĐANG HIỆN theo lớp; ghost: năm nguồn
    namMax(year) { const o = {}; for (const l of list) if (win(year, l.years) > 0) o[l.name] = l.yearMax; return o; },
    ghostSrc(year) { const g = list.find((l) => l.kind === 'ghost' && win(year, l.years) > 0); return g ? g.src : null; } };
}

// ---------- M12: bản đồ pha theo mốc ----------
function drape(box, hAt, step, lift) {
  const [e0, n0, e1, n1] = box, nx = Math.max(2, Math.ceil((e1 - e0) / step) + 1), ny = Math.max(2, Math.ceil((n1 - n0) / step) + 1), P = [], UV = [], I = [];
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const e = e0 + (e1 - e0) * i / (nx - 1), n = n0 + (n1 - n0) * j / (ny - 1); P.push(e, Math.max(hAt(e, n), 0.2) + lift, -n); UV.push(i / (nx - 1), j / (ny - 1)); }
  for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) { const k = j * nx + i; I.push(k, k + 1, k + nx, k + 1, k + nx + 1, k + nx); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(UV, 2)); g.setIndex(I); g.computeVertexNormals(); return g;
}
export async function phaseMaps(specs, ctx) {
  const group = new THREE.Group(), list = [];
  for (const sp of specs || []) {
    const t = await new THREE.TextureLoader().loadAsync(sp.url); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    const m = new THREE.MeshLambertMaterial({ map: t, transparent: true, opacity: 0, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
    maskify(m, ctx.U, 0); const mesh = new THREE.Mesh(drape(sp.box, ctx.terr.hAt, sp.step || 20, sp.lift ?? 0.6), m); mesh.renderOrder = 1; mesh.receiveShadow = true; group.add(mesh);
    list.push({ sp, m, mesh });
  }
  return { group, list, update(tv) { for (const l of list) { const a = win(tv, l.sp.years, l.sp.fade ?? 2) * (l.sp.opacity ?? 0.85); l.m.opacity = a; l.mesh.visible = a > 0.005; } },
    srcAt(tv) { const l = list.filter((x) => win(tv, x.sp.years, x.sp.fade ?? 2) > 0.5).pop(); return l ? l.sp.src : null; } };
}

// ---------- M4: chiến tuyến / hào mọc theo thời gian ----------
function hull2(P) { const p = P.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]); if (p.length < 3) return p; const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo = [], up = []; for (const q of p) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q); } for (const q of p.reverse()) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q); }
  return lo.slice(0, -1).concat(up.slice(0, -1)); }
function pip(p, r) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > p[1]) !== (r[j][1] > p[1]) && p[0] < (r[j][0] - r[i][0]) * (p[1] - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; }
const cumLen = (pts) => { const c = [0]; for (let i = 1; i < pts.length; i++) c.push(c[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])); return c; };
function ribbonGeo(pts, hAt, w, lift, berm) {   // dải rộng w bám DTM; berm > 0: gờ đất (mặt cắt hình thang cao berm m) dọc tim tuyến
  const P = [], I = [], S = [], C = cumLen(pts), prof = berm > 0 ? [[-1, 0], [-0.35, berm], [0.35, berm], [1, 0]] : [[-1, 0], [1, 0]], np = prof.length;
  for (let i = 0; i < pts.length; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1, nn = [-d[1] / l, d[0] / l];
    for (const [o, hh] of prof) { const e = pts[i][0] + nn[0] * o * w / 2, n = pts[i][1] + nn[1] * o * w / 2; P.push(e, Math.max(hAt(e, n), 0.3) + lift + hh, -n); S.push(C[i]); } }
  for (let i = 0; i < pts.length - 1; i++) for (let k = 0; k < np - 1; k++) { const q = i * np + k; I.push(q, q + np, q + 1, q + 1, q + np, q + np + 1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('aS', new THREE.Float32BufferAttribute(S, 1)); g.setIndex(I); g.computeVertexNormals();
  return { g, len: C[C.length - 1] };
}
function growMat(color, U, opacity = 1) {   // mọc theo quãng dọc tuyến: uGrow (m) — phần chưa tới bị loại
  const m = new THREE.MeshLambertMaterial({ color, transparent: opacity < 1, opacity, polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -3, side: THREE.DoubleSide });
  m.userData.uGrow = { value: 0 };
  m.onBeforeCompile = (sh) => { sh.uniforms.uGrow = m.userData.uGrow; sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aS; varying float vS;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvS = aS;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uGrow; varying float vS;').replace('#include <color_fragment>', '#include <color_fragment>\nif (vS > uGrow) discard;'); };
  m.customProgramCacheKey = () => 'tl-grow'; maskify(m, U, 1); return m;
}
export function frontLines(specs, ctx) {
  const group = new THREE.Group(), list = [];
  for (const sp of specs || []) {
    const col = new THREE.Color(sp.color || FACTION[sp.side] || FACTION.neutral);
    const band = ribbonGeo(sp.pts, ctx.terr.hAt, sp.w || 26, 0.5, 0), berm = ribbonGeo(sp.pts, ctx.terr.hAt, (sp.w || 26) * 0.45, 0.4, sp.berm ?? 2.2);
    const mb = growMat(col.clone().lerp(new THREE.Color('#2a2420'), 0.15), ctx.U, sp.bandA ?? 0.45), mk = growMat(new THREE.Color('#9a8566').lerp(col, 0.22), ctx.U, 1);   // V5b-2b: dải phe nhạt hơn, gờ màu đất/đá pha phe (đọc là công trình, không phải nét vẽ)   // dải phe (bán trong) + gờ đất (màu đất pha phe)
    if (sp.stone) mk.color.set(sp.stone);   // tường đá (Line Wall): gờ cao màu đá vôi, không dải phe
    const a = new THREE.Mesh(band.g, mb), b = new THREE.Mesh(berm.g, mk); b.castShadow = b.receiveShadow = true; a.renderOrder = 2; group.add(b); if (sp.band !== false) group.add(a);
    list.push({ sp, len: band.len, mats: [mb, mk], meshes: [a, b] });
  }
  return { group, list, update(tv) { for (const l of list) { const [t0, t1] = l.sp.grow, u = Math.max(0, Math.min(1, (tv - t0) / Math.max(1e-6, t1 - t0))), fadeOut = l.sp.fade ? win(tv, [t0, l.sp.fade[1]], l.sp.fade[1] - l.sp.fade[0]) : 1;
    for (const m of l.mats) m.userData.uGrow.value = u * l.len + 0.01; l.mats[0].opacity = (l.sp.bandA ?? 0.45) * fadeOut; for (const o of l.meshes) o.visible = u > 0 && fadeOut > 0.01; } } };
}

// ---------- M1: mũi tên ruy băng bám địa hình ----------
export function arrows(specs, ctx) {
  const group = new THREE.Group(), list = [];
  for (const sp of specs || []) {
    const w = sp.w || 40, pts = sp.pts, last = pts[pts.length - 1], prev = pts[pts.length - 2], d = [last[0] - prev[0], last[1] - prev[1]], l = Math.hypot(...d), u = [d[0] / l, d[1] / l];
    const body = pts.slice(0, -1).concat([[last[0] - u[0] * w * 1.6, last[1] - u[1] * w * 1.6]]), rb = ribbonGeo(body, ctx.terr.hAt, w, sp.lift ?? 3, 0);
    const col = new THREE.Color(sp.color || FACTION[sp.side] || FACTION.civ), m = growMat(col, ctx.U, 0.92);
    const hb = [last[0] - u[0] * w * 1.6, last[1] - u[1] * w * 1.6], nn = [-u[1], u[0]], H = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3) + (sp.lift ?? 3);
    const tri = [[hb[0] + nn[0] * w * 1.1, hb[1] + nn[1] * w * 1.1], [hb[0] - nn[0] * w * 1.1, hb[1] - nn[1] * w * 1.1], last];
    const hg = new THREE.BufferGeometry(); hg.setAttribute('position', new THREE.Float32BufferAttribute(tri.flatMap(([e, n]) => [e, H(e, n), -n]), 3)); hg.setAttribute('aS', new THREE.Float32BufferAttribute([rb.len + 1, rb.len + 1, rb.len + w * 1.6], 1)); hg.computeVertexNormals();
    const a = new THREE.Mesh(rb.g, m), h = new THREE.Mesh(hg, m); a.renderOrder = h.renderOrder = 3; group.add(a, h);
    list.push({ sp, len: rb.len + w * 1.6, m, meshes: [a, h] });
  }
  return { group, list, update(tv) { for (const l of list) { const [t0, t1] = l.sp.grow, u = Math.max(0, Math.min(1, (tv - t0) / Math.max(1e-6, t1 - t0))), f = l.sp.out ? win(tv, [t0, l.sp.out], 0.5) : 1;
    l.m.userData.uGrow.value = u * l.len + 0.01; l.m.opacity = 0.92 * f; for (const o of l.meshes) o.visible = u > 0 && f > 0.01; } } };
}

// ---------- M7: khói / lửa sprite 2D ----------
function puffTex(seed, warm) {   // kết cấu cụm khói thủ tục (tất định): nhiều đĩa mềm chồng nhau, viền nhiễu
  const S = 128, cv = document.createElement('canvas'); cv.width = cv.height = S; const g = cv.getContext('2d'), R = rng(seed);
  for (let k = 0; k < 26; k++) { const a = R() * 6.283, r = Math.sqrt(R()) * S * 0.28, x = S / 2 + Math.cos(a) * r, y = S / 2 + Math.sin(a) * r * 0.8, rr = S * (0.10 + 0.14 * R());
    const gr = g.createRadialGradient(x, y, 0, x, y, rr), c = warm ? [255, 150 + 60 * R() | 0, 60] : [210 + 30 * R() | 0, 205 + 30 * R() | 0, 200 + 30 * R() | 0];
    gr.addColorStop(0, `rgba(${c[0]},${c[1]},${c[2]},${warm ? 0.55 : 0.22})`); gr.addColorStop(1, `rgba(${c[0]},${c[1]},${c[2]},0)`); g.fillStyle = gr; g.fillRect(0, 0, S, S); }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t;
}
export function smoke(specs, ctx) {
  const group = new THREE.Group(), list = [], texS = [0, 1, 2].map((i) => puffTex(91 + i, false)), texF = puffTex(7, true);
  for (const sp of specs || []) {   // sp: {at:[E, cao, N], t:[bắt đầu, hết], n (số cụm), size, rise (m/đơn vị tv), drift [dE, dN] (m/đơn vị tv), fire (0..1), dark}
    const R = rng(sp.seed || 5), puffs = [];
    for (let k = 0; k < (sp.n || 14); k++) { const m = new THREE.SpriteMaterial({ map: sp.fire && k < 2 ? texF : texS[k % 3], transparent: true, depthWrite: false, fog: true, color: new THREE.Color(sp.dark ? 0x6a6560 : 0xc2bdb2).multiplyScalar(0.86 + 0.2 * R()), opacity: 0 });   /* khói thuốc súng: xám ngà, mỗi cụm một độ sáng */
      maskify(m, ctx.U, 0); const s = new THREE.Sprite(m); s.renderOrder = 5; group.add(s); puffs.push({ s, m, ph: R(), fire: sp.fire && k < 2, j: [R() - 0.5, R() - 0.5] }); }
    list.push({ sp, puffs });
  }
  return { group, list,
    update(tv) { for (const { sp, puffs } of list) { const on = tv >= sp.t[0] && tv <= sp.t[1]; for (const p of puffs) { if (!on) { p.s.visible = false; continue; }
      const age = ((tv - sp.t[0]) / (sp.period || 0.12) + p.ph) % 1, sz = (sp.size || 40) * (p.fire ? 0.45 : 0.6 + 1.6 * age), d = sp.drift || [6, 2];
      const life = (sp.period || 0.12) * age; p.s.position.set(sp.at[0] + d[0] * life / (sp.period || 0.12) * 6 + p.j[0] * sz * 0.6, sp.at[1] + (p.fire ? sz * 0.2 : (sp.rise || 60) * age + sz * 0.3), -(sp.at[2] + d[1] * life / (sp.period || 0.12) * 6 + p.j[1] * sz * 0.6));
      p.s.scale.set(sz, sz, 1); p.m.opacity = p.fire ? 0.85 * (sp.fire || 0) : Math.min(1, age * 5) * (1 - age) * (sp.alpha ?? 0.85); p.s.visible = true; } } },
    // vùng khói (hình chiếu tròn trên mặt đất, m) — cảnh kiểm KHÔNG có người/xe A-lite trong vùng này (luật hình chiến tranh §6.2)
    zones(tv) { return list.filter(({ sp }) => tv >= sp.t[0] && tv <= sp.t[1]).map(({ sp }) => ({ c: [sp.at[0], sp.at[2]], r: (sp.size || 40) * 2.5 + 30, fire: !!sp.fire })); } };
}

// ---------- V5b-2b (lệnh AE, chủ dự án 17/10): PHỐ 1782 từ ghost của phiên SH (channel-k2/k2c-t3-01/ghost/ghost-1782.geojson, nhánh claude/sh-ghost-gibraltar-t3-1gkftx @ 54185b3) ----------
//  nạp qua scripts/k2tl/load_footprints.py: ghost1782 (22 khối phố + 13 toà, do_tin cao/vừa → nhà tái dựng thời kỳ 0, 2 tầng chuẩn mốc), fort1782 (bastion, Old Mole, 2 pháo đài TBN;
//  King's Bastion lấy footprint OSM — chính xác hơn RMS 21 m), lines1782 (Line Wall + tường nam: gờ đá; Línea de Contravalación: chiến tuyến phe TBN). Feature do_tin = thấp KHÔNG dùng.
//  Lớp tái dựng 1705 của gói cảnh (V5b-1) bị ẩn: một mốc, một nguồn. Nửa đông phố cổ: bản đồ vẽ sườn đồi không viền → để trống (SH không bịa).
export const SRC1782 = 'Reconstructed from J. Drinkwater, Plan of the Batteries, 1782';
export async function town1782(ctx, { hidPack = true, infill = true, kbOpt = {} } = {}) {
  if (hidPack) ctx.city.group.visible = false;
  // V5b-2c (I2): + lớp LẤP ƯỚC TÍNH infill1782 (scripts/k2tl/infill_1782.py, do_tin uoc, tông lệch nhẹ) — dòng phương pháp "Grey-washed blocks: estimated infill" do cảnh hiện
  // bastion của plan (Orange's, Montague, South Bastion, Old Mole…) có ≥ 6 điểm tường OSM trong 75 m → thay vòng bằng bao lồi điểm OSM (vị trí thật), bỏ các điểm đó khỏi tuyến tường
  const H = await loadJSON(`${ctx.base}heroes.json`), osmPts = H.citywalls.flat(), used = [];
  const fortRemap = (r) => { const c = [r[6].reduce((a, q) => a + q[0], 0) / r[6].length, r[6].reduce((a, q) => a + q[1], 0) / r[6].length], near = osmPts.filter((p) => Math.hypot(p[0] - c[0], p[1] - c[1]) < 75);
    if (near.length < 6 || c[1] > 600) return r; const hr = hull2(near); used.push(hr); return Object.assign(r.slice(), { 6: hr }); };
  const FP = await footprints([{ file: 'ghost1782', ghostDesat: 0.08 }, { file: 'fort1782', fort: true, h: 8, remap: fortRemap }].concat(infill ? [{ file: 'infill1782', ghostDesat: 0.08 }] : []), ctx);   // V5b-2c (I5): giảm bão hoà lớp tái dựng 22 % → 8 % (vẫn nhận ra là tái dựng nhờ nhãn nguồn + tông lệch)
  ctx.scene.add(FP.group); ctx.scene.add(FP.group);
  const L = await loadJSON(`${ctx.base}layers/lines1782.json`);
  // V5b-2c (M5): Line Wall + tường nam dựng như tường thành đá (gờ, tường chắn, lỗ châu mai, pháo mỗi 2 lỗ); Línea (đất + đá TBN) giữ gờ chiến tuyến
  // Línea de Contravalación (TBN, xây 1730–35, tường đá + bastion — SH ghi "tường và các bastion"): V5b-2c dựng như tường đá thấp 5,5 m, mặt chính quay NAM (về Gibraltar)
  const FL = frontLines([], ctx), lineaRecs = [];
  for (const l of L.lines.filter((x) => x.loai === 'chien_tuyen')) { for (let i = 0; i < l.pts.length - 1; i++) { const a = l.pts[i], b = l.pts[i + 1], hs = [a, b].map(([e, n]) => ctx.terr.hAt(e, n)), lo = Math.max(0.3, Math.min(...hs)), hi = Math.max(0.3, ...hs);
    lineaRecs.push([0, 0, 5.5 + (hi - lo), lo, 0, 1, wallRing([a, b], 3, 3), 0]); } }
  const LN = fortify(lineaRecs, ctx, { thick: 2.0, batter: 0.12, embr: 9, gunEvery: 2, garita: true, seed: 71, face: [0, -1] }); ctx.scene.add(LN.group);
  // tường leo dốc (tường nam Charles V): cắt đoạn ≤ 24 m, mỗi đoạn cốt chân riêng, đỉnh = 7,5 m trên điểm cao nhất của đoạn
  // V5b-2c: Line Wall + King's Bastion lấy hình học OSM historic=citywalls (heroes.json — đúng vị trí thật, không lệch RMS 21 m của plan), dựng bằng M5;
  //  tường cùng tên của plan (C1782-06…09) chỉ còn dùng khi không có OSM. Bastion = bao lồi điểm tường OSM quanh tâm; tường giản lược cũ của gói (heroes) ẩn.
  const KBc = [-602, -1276], inB = (p) => p[0] > -800 && p[0] < -150 && p[1] > -1950 && p[1] < -640;
  const kbPts = H.citywalls.flat().filter((p) => Math.hypot(p[0] - KBc[0], p[1] - KBc[1]) < 85), kbRing = hull2(kbPts);
  if (ctx.heroes && ctx.heroes.citywallMesh) ctx.heroes.citywallMesh.visible = false;
  const KB = kbRing.length > 3 ? fortify([[0, 0, kbOpt.h || 9, Math.max(0.3, Math.min(...kbRing.map(([e, n]) => ctx.terr.hAt(e, n)))), 0, 1, kbRing, 0]], ctx, Object.assign({ hid: kbOpt.hid || 0, seed: 53 }, kbOpt)) : null; if (KB) ctx.scene.add(KB.group);
  const inKB = (p) => (kbRing.length > 3 && pip(p, kbRing)) || used.some((r) => pip(p, r));
  const wallRecs = [], slopeRecs = []; const osmLines = H.citywalls.filter((w) => w.some(inB)).map((w) => ({ pts: w.filter((p) => !inKB(p)) })).filter((l) => l.pts.length > 1);
  for (const l of osmLines) { const C = cumLen(l.pts), tot = C[C.length - 1], steep = Math.max(...l.pts.map(([e, n]) => ctx.terr.hAt(e, n))) > 18, ns = Math.max(1, Math.ceil(tot / (steep ? 7 : 24)));   // tường leo sườn (Charles V, tường Moor): đoạn 7 m, mỏng, không terreplein
    const at = (sv) => { let i = 1; while (i < l.pts.length - 1 && C[i] < sv) i++; const a = l.pts[i - 1], b = l.pts[i], u = Math.max(0, Math.min(1, (sv - C[i - 1]) / ((C[i] - C[i - 1]) || 1))); return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]; };
    for (let k = 0; k < ns; k++) { const s0 = tot * k / ns, s1 = Math.min(tot, tot * (k + 1) / ns + 0.6), seg = [at(s0)]; for (let i = 0; i < l.pts.length; i++) if (C[i] > s0 && C[i] < s1) seg.push(l.pts[i]); seg.push(at(s1));
      const hs = seg.map(([e, n]) => ctx.terr.hAt(e, n)), lo = Math.max(0.3, Math.min(...hs)), hi = Math.max(0.3, ...hs);
      // bên phố được đắp 26 m (terreplein), bên biển 4 m
      const m0 = seg[0], m1 = seg[seg.length - 1], dd = [m1[0] - m0[0], m1[1] - m0[1]], dl = Math.hypot(...dd) || 1, nl = [-dd[1] / dl, dd[0] / dl], mc = [(m0[0] + m1[0]) / 2, (m0[1] + m1[1]) / 2];
      const left = nl[0] * (-430 - mc[0]) + nl[1] * (-1300 - mc[1]) > 0;   // bên PHỐ (tâm phố cổ 1782 ≈ E −430, N −1300; DEM 2026 có đất lấn biển nên không dùng cao độ)
      // từng đoạn THẲNG (vòng lồi → sàn tam giác hoá đúng; đoạn gãy khúc cho vòng tự cắt → mất sàn, lộ nước), nối đè 3 m ở khớp
      for (let j = 0; j < seg.length - 1; j++) { const a0 = seg[j], b0 = seg[j + 1], dv = [b0[0] - a0[0], b0[1] - a0[1]], ll = Math.hypot(...dv); if (ll < 1) continue; const u = [dv[0] / ll, dv[1] / ll], A = [a0[0] - u[0] * 3, a0[1] - u[1] * 3], B = [b0[0] + u[0] * 3, b0[1] + u[1] * 3];
        (steep ? slopeRecs : wallRecs).push([0, 0, (steep ? 5.5 : 7.5) + (hi - lo), lo, 0, 1, steep ? wallRing([A, B], 1.6, 1.6) : left ? wallRing([A, B], 26, 4) : wallRing([A, B], 4, 26), 0]); } } }
  const WL = fortify(wallRecs, ctx, { thick: 2.4, batter: 0.1, gunEvery: 2, garita: false, seed: 61 }); ctx.scene.add(WL.group);
  const WS = fortify(slopeRecs, ctx, { thick: 0.7, batter: 0.0, embr: 1e9, guns: false, garita: false, seed: 62 }); ctx.scene.add(WS.group);   // tường sườn: mỏng, không lỗ châu mai/pháo
  // nền phố của địa hình CHỈ quanh khối ghost + công sự (giãn 25 m, 2 m/điểm ảnh); đường OSM 2026 ẩn (đường giữa các khối là nền phố)
  const recs = []; for (const f of ['ghost1782', 'fort1782'].concat(infill ? ['infill1782'] : [])) recs.push(...(await loadJSON(`${ctx.base}layers/${f}.json`)).records.map((r) => r[6]));
  const all = recs.flat(), e0 = Math.min(...all.map((q) => q[0])) - 80, e1 = Math.max(...all.map((q) => q[0])) + 80, n0 = Math.min(...all.map((q) => q[1])) - 80, n1 = Math.max(...all.map((q) => q[1])) + 80, res = 2;
  const cv = document.createElement('canvas'); cv.width = Math.ceil((e1 - e0) / res); cv.height = Math.ceil((n1 - n0) / res); const g = cv.getContext('2d');
  g.fillStyle = '#000'; g.fillRect(0, 0, cv.width, cv.height); g.fillStyle = g.strokeStyle = '#fff'; g.lineWidth = 50 / res; g.lineJoin = 'round';
  for (const r of recs) { g.beginPath(); r.forEach(([e, n], i) => (i ? g.lineTo : g.moveTo).call(g, (e - e0) / res, (n1 - n) / res)); g.closePath(); g.fill(); g.stroke(); }
  // cây 2026 trong phố cổ (trong hộp ghost, dưới 70 m cao độ) ẩn ở mốc 1782 — không có nguồn vườn/cây 1782
  if (ctx.trees && ctx.trees.hideWhere) ctx._treesHid = ctx.trees.hideWhere((e, n) => e > e0 + 40 && e < e1 - 20 && n > n0 + 40 && n < n1 - 40 && ctx.terr.hAt(e, n) < 70);
  g.filter = 'blur(4px)'; g.drawImage(cv, 0, 0); const tx = new THREE.CanvasTexture(cv); tx.minFilter = THREE.LinearFilter;
  const u = ctx.terr.uni; u.tGhostU.value = tx; u.uGhostBox.value.set(e0, n0, e1 - e0, n1 - n0); u.uGhostOn.value = 1; if (ctx.roads) ctx.roads.mesh.visible = false;
  return { FP, FL, WL, LN, KB, kbRing, infill, INFILL_SRC: 'Grey-washed blocks: estimated infill', update(year, cam) { FP.update(year, cam); FL.update(year); }, namMax: (y) => FP.namMax(y), src: SRC1782 };
}

// ---------- M2 RÚT GỌN (lệnh AC1, chủ dự án 17/10): KHỐI ĐƠN VỊ QUÂN instanced ----------
//  Mỗi đơn vị = đội hình hàng × cột hình người A-lite (thân + mũ, cao 1,75 m, cách 0,9 m × 1,3 m), KHÔNG cận mặt, KHÔNG người ngã/chết; màu phe cố định (FACTION).
//  Vị trí lấy từ hình học đã nắn có nguồn: spec.pts = tuyến (vd Línea de Contravalación, ghost SH từ Drinkwater 1786) + s (m dọc tuyến) + off (m vuông góc, sau tường chắn);
//  hoặc spec.at = [E, N]. Mọc theo ngày: day = [xuất hiện, rút] (đơn vị "ngày" do cảnh chọn: uDay), mọc 0,5 ngày từ mặt đất; dịch: move = [[day, dE, dN], …].
//  update(day, zones): đơn vị có tâm trong vùng khói/lửa (layers.smoke zones) bị ẨN và đếm (luật hình chiến tranh §6.2: không người trong vùng khói).
export function units(specs, ctx) {
  const fig = { body: new THREE.BoxGeometry(0.5, 1.35, 0.32).translate(0, 0.68, 0), hat: new THREE.BoxGeometry(0.42, 0.3, 0.42).translate(0, 1.55, 0) };
  const slots = [];
  for (const sp of specs || []) {
    let E, N, hd;
    if (sp.pts) { const C = cumLen(sp.pts); let i = 1; while (i < sp.pts.length - 1 && C[i] < sp.s) i++; const a = sp.pts[i - 1], b = sp.pts[i], u = Math.max(0, Math.min(1, (sp.s - C[i - 1]) / ((C[i] - C[i - 1]) || 1)));
      const d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1, nn = [-d[1] / l, d[0] / l]; E = a[0] + d[0] * u + nn[0] * (sp.off || 0); N = a[1] + d[1] * u + nn[1] * (sp.off || 0); hd = Math.atan2(d[1], d[0]); }
    else { E = sp.at[0]; N = sp.at[1]; hd = (90 - (sp.heading || 0)) * Math.PI / 180; }
    const rows = sp.rows || 3, cols = sp.cols || 24, R = rng(sp.seed || 7);
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) slots.push({ sp, E, N, hd, x: (c - (cols - 1) / 2) * 0.9 + (R() - 0.5) * 0.12, z: (r - (rows - 1) / 2) * 1.3 + (R() - 0.5) * 0.1, k: 0.95 + 0.1 * R() });
  }
  const group = new THREE.Group(), mats = {}, meshes = [];
  const byColor = {}; for (const s of slots) { const col = s.sp.color || FACTION[s.sp.side] || FACTION.neutral; (byColor[col] = byColor[col] || []).push(s); }
  for (const [col, S] of Object.entries(byColor)) {
    const mb = new THREE.MeshLambertMaterial({ color: new THREE.Color(col).multiplyScalar(0.82) }), mh = new THREE.MeshLambertMaterial({ color: 0x1d1b19 });
    maskify(mb, ctx.U, 1); maskify(mh, ctx.U, 1);
    const ib = new THREE.InstancedMesh(fig.body, mb, S.length), ih = new THREE.InstancedMesh(fig.hat, mh, S.length); ib.castShadow = ih.castShadow = true; ib.receiveShadow = true;
    group.add(ib, ih); meshes.push({ S, ib, ih }); mats[col] = mb;
  }
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), sc = new THREE.Vector3(), Y = new THREE.Vector3(0, 1, 0);
  let stat = { don_vi: specs ? specs.length : 0, nguoi: slots.length, an_vi_khoi: 0, hien: 0 };
  return { group, meshes, stat: () => stat,
    update(day, zones = []) {
      const hidUnits = new Set(); let shown = 0;
      for (const { S, ib, ih } of meshes) { S.forEach((s, i) => {
        const [d0, d1] = s.sp.day || [-1e9, 1e9]; let g = Math.max(0, Math.min(1, (day - d0) / 0.5)) * (day <= d1 ? 1 : 0);
        let dE = 0, dN = 0; if (s.sp.move) { const M = s.sp.move; let j = 0; while (j < M.length - 1 && M[j + 1][0] <= day) j++; const A = M[j], B = M[Math.min(M.length - 1, j + 1)], u = B[0] > A[0] ? Math.max(0, Math.min(1, (day - A[0]) / (B[0] - A[0]))) : 0; dE = A[1] + (B[1] - A[1]) * u; dN = A[2] + (B[2] - A[2]) * u; }
        const E = s.E + dE, N = s.N + dN; if (zones.some((z) => Math.hypot(E - z.c[0], N - z.c[1]) < z.r + 15)) { g = 0; hidUnits.add(s.sp); }
        const ce = Math.cos(s.hd), sn = Math.sin(s.hd), e = E + ce * s.x - sn * s.z, n = N + sn * s.x + ce * s.z;
        v.set(e, Math.max(ctx.terr.hAt(e, n), 0.4) - 0.05, -n); q.setFromAxisAngle(Y, s.hd); sc.set(g > 0 ? 1 : 0, g * s.k, g > 0 ? 1 : 0); m4.compose(v, q, sc); ib.setMatrixAt(i, m4); ih.setMatrixAt(i, m4); if (g > 0) shown++; });
        ib.instanceMatrix.needsUpdate = ih.instanceMatrix.needsUpdate = true; }
      stat = { don_vi: specs.length, nguoi: slots.length, an_vi_khoi: hidUnits.size, hien: shown }; return stat; } };
}

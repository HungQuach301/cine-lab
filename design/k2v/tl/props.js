// K2V tl · V5b-2d · ĐẠO CỤ CẢNH 1782 (lệnh V5b-2d chủ dự án 18/10, C2-1…C2-9): cờ, vườn có nguồn, điểm nhấn phố, đồ trên sàn pháo.
//  · flags(specs)     — cột + lá cờ vải gợn (shader, theo thời gian cảnh), mẫu vẽ canvas: 'union1707' (Great Union 1707: chữ thập St George đỏ viền trắng trên
//                       chéo St Andrew trắng nền lam — trước 1801, không có chéo St Patrick) · 'burgundy' (Cruz de Borgoña: chéo đỏ răng cưa trên nền trắng — cờ quân TBN 1506–1843);
//  · gardens(feats)   — LUỐNG VƯỜN chỉ nơi bản đồ Drinkwater 1786 vẽ luống/ghi GARDENS (lớp extra1782 của scripts/k2tl/so_hoa_v5b2d.py): mặt luống sọc xanh–đất
//                       bám DTM + cây chỉ trong vòng vườn (opt.trees) + nhà vườn (ô □ trên bản đồ); KHÔNG cây ngoài vòng vườn;
//  · landmarks(L)     — St Mary the Crowned (Spanish Church, N1782-09: thân nhà thờ + tháp chuông) và dinh Thống đốc (Convent, N1782-07: khối có sân trong) dựng
//                       trên footprint ghost SH; chiều cao MINH HOẠ (ghi dòng phương pháp của cảnh);
//  · battery(guns)    — đồ trên sàn pháo King's Bastion: đống đạn, thùng thuốc súng, lán chắn mảnh (splinter-proof), lò nung đạn (Drinkwater 1785: "grates and furnaces for heating
//                       shot") — vị trí theo khẩu pháo của fort.js, số lượng minh hoạ.
// Mặt nạ: cờ, luống, cây, nhà, điểm nhấn, đồ sàn pháo = NỘI DUNG (maskify 1). Không Math.random (rng tất định).
import { THREE, rng, maskify } from './core.js';
import { makeCity } from './city.js';

// V7B (việc 2, nguồn mẫu cờ: reports/v7b/V7B-BAO-CAO.md §2): thêm 'red_ensign1707' (Red Ensign 1707–1800: nền đỏ, góc cờ Great Union 1707 — Order in Council 21/7/1707),
//  'es_naval1701' (cờ hải quân TBN 1701–1785: nền TRẮNG + huy hiệu hoàng gia Bourbon, thay bằng đỏ–vàng ngày 28/5/1785 vì dễ lẫn cờ trắng các nước Bourbon — FOTW es1701/es1785),
//  'fr_white' (hải quân Pháp thời Louis XVI: cờ trắng trơn). Huy hiệu vẽ giản lược (khiên + vương miện) — đọc ở 1–2 km chỉ còn một đốm màu giữa nền trắng.
function unionCanton(g, x, y, W, H) {
  g.fillStyle = '#1f3a7a'; g.fillRect(x, y, W, H); g.save(); g.beginPath(); g.rect(x, y, W, H); g.clip();
  g.strokeStyle = '#f4f1ea'; g.lineWidth = H * 0.2; g.beginPath(); g.moveTo(x, y); g.lineTo(x + W, y + H); g.moveTo(x + W, y); g.lineTo(x, y + H); g.stroke();
  g.fillStyle = '#f4f1ea'; g.fillRect(x + W / 2 - H * 0.17, y, H * 0.34, H); g.fillRect(x, y + H / 2 - H * 0.17, W, H * 0.34);
  g.fillStyle = '#c8202f'; g.fillRect(x + W / 2 - H * 0.1, y, H * 0.2, H); g.fillRect(x, y + H / 2 - H * 0.1, W, H * 0.2); g.restore();
}
export function flagTex(kind) {
  const W = 192, H = 96, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
  if (kind === 'red_ensign1707') { g.fillStyle = '#b8222c'; g.fillRect(0, 0, W, H); unionCanton(g, 0, 0, W / 2, H / 2); }
  else if (kind === 'fr_white') { g.fillStyle = '#f5f3ec'; g.fillRect(0, 0, W, H); }
  else if (kind === 'es_naval1701') { g.fillStyle = '#f5f3ec'; g.fillRect(0, 0, W, H); const cx = W * 0.42, cy = H * 0.54, sw = H * 0.30, sh = H * 0.36;   // khiên Bourbon giản lược: 4 ô Castilla (đỏ)/León (trắng-tím) + ô giữa lam + vương miện vàng
    g.fillStyle = '#b8232b'; g.fillRect(cx - sw, cy - sh, sw, sh); g.fillRect(cx, cy, sw, sh); g.fillStyle = '#e9e2d0'; g.fillRect(cx, cy - sh, sw, sh); g.fillRect(cx - sw, cy, sw, sh);
    g.fillStyle = '#7a3b6a'; g.fillRect(cx + sw * 0.35, cy - sh * 0.7, sw * 0.3, sh * 0.4); g.fillRect(cx - sw * 0.65, cy + sh * 0.3, sw * 0.3, sh * 0.4); g.fillStyle = '#d2a530'; g.fillRect(cx - sw * 0.65, cy - sh * 0.7, sw * 0.3, sh * 0.4); g.fillRect(cx + sw * 0.35, cy + sh * 0.3, sw * 0.3, sh * 0.4);
    g.fillStyle = '#2e4f9a'; g.beginPath(); g.ellipse(cx, cy, sw * 0.32, sh * 0.32, 0, 0, 6.283); g.fill(); g.fillStyle = '#d2a530'; g.fillRect(cx - sw * 0.8, cy - sh * 1.45, sw * 1.6, sh * 0.38); }
  else if (kind === 'union1707') {
    g.fillStyle = '#1f3a7a'; g.fillRect(0, 0, W, H);
    g.strokeStyle = '#f4f1ea'; g.lineWidth = H * 0.2; g.beginPath(); g.moveTo(0, 0); g.lineTo(W, H); g.moveTo(W, 0); g.lineTo(0, H); g.stroke();   // chéo St Andrew
    g.fillStyle = '#f4f1ea'; g.fillRect(W / 2 - H * 0.17, 0, H * 0.34, H); g.fillRect(0, H / 2 - H * 0.17, W, H * 0.34);   // viền trắng
    g.fillStyle = '#c8202f'; g.fillRect(W / 2 - H * 0.1, 0, H * 0.2, H); g.fillRect(0, H / 2 - H * 0.1, W, H * 0.2);   // chữ thập St George
  } else {   // Cruz de Borgoña
    g.fillStyle = '#f3efe4'; g.fillRect(0, 0, W, H); g.strokeStyle = '#b8232b'; g.lineWidth = H * 0.13; g.lineCap = 'round';
    for (const [x0, y0, x1, y1] of [[W * 0.08, H * 0.1, W * 0.92, H * 0.9], [W * 0.92, H * 0.1, W * 0.08, H * 0.9]]) { g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke();
      for (let k = 1; k < 6; k++) { const u = k / 6, x = x0 + (x1 - x0) * u, y = y0 + (y1 - y0) * u; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (k % 2 ? 1 : -1) * H * 0.09, y - H * 0.06); g.stroke(); } }   // mấu cành (ragged staff)
  }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}

// specs: [{at:[E, N], base (cốt chân, mặc định DTM), pole (m), w, kind, phase}]
export function flags(specs, ctx) {
  const group = new THREE.Group(), U = { uT: { value: 0 } }, tex = {}, cloths = [];
  const poleM = new THREE.MeshLambertMaterial({ color: 0x5b4632 }); maskify(poleM, ctx.U, 1);
  for (const sp of specs || []) {
    const sc = Math.min(1.5, sp.scale || 1), pole = (sp.pole || 12) * Math.max(1, sc * 0.85), w = (sp.w || 4.2) * sc, h = w / 2, base = sp.base ?? Math.max(0.3, ctx.terr.hAt(sp.at[0], sp.at[1]));
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.14, pole, 6).translate(0, pole / 2, 0), poleM); p.position.set(sp.at[0], base, -sp.at[1]); p.castShadow = true; group.add(p);
    const k = sp.kind || 'union1707'; tex[k] = tex[k] || flagTex(k);
    const m = new THREE.MeshLambertMaterial({ map: tex[k], side: THREE.DoubleSide });
    m.onBeforeCompile = (sh) => { sh.uniforms.uT = U.uT; sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float uT;')
      .replace('#include <begin_vertex>', `#include <begin_vertex>\n float fx = clamp(position.x / ${w.toFixed(2)}, 0.0, 1.0); transformed.z += sin(position.x * 1.7 - uT * 6.0 + ${(sp.phase || 0).toFixed(2)}) * 0.35 * fx; transformed.y -= 0.25 * fx * fx;`);
      if (ctx.v6) sh.fragmentShader = sh.fragmentShader.replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n totalEmissiveRadiance += diffuseColor.rgb * 0.4;');   // V6: vải XUYÊN SÁNG — cờ ngược nắng vẫn đọc được (vật mang dữ kiện; như lượt Cycles)
    };
    m.customProgramCacheKey = () => 'tl-flag-' + w.toFixed(2) + (ctx.v6 ? '-v6' : '');
    maskify(m, ctx.U, 1);   // V6: SAU onBeforeCompile (trước đây hook cờ ghi đè hook mặt nạ → cờ không vào mặt nạ nội dung / lượt pháp tuyến / lượt albedo)
    const cl = new THREE.Mesh(new THREE.PlaneGeometry(w, h, 12, 2).translate(w / 2, -h / 2, 0), m); cl.position.set(sp.at[0], base + pole - 0.1, -sp.at[1]);
    cl.rotation.y = (90 - (sp.toward ?? 135)) * Math.PI / 180; group.add(cl); cloths.push({ cl, top: base + pole - 0.1, low: base + Math.min(2.5, pole * 0.2) + h });   // toward: hướng gió thổi tới (độ, 0 = Bắc) — cờ bay theo gió
  }
  // V7B: hoist 0..1 = vị trí lá cờ trên cột (0 = hạ sát chân, 1 = đỉnh) — khoảnh khắc đổi chủ: hạ cờ cũ rồi kéo cờ mới
  return { group, n: (specs || []).length, update(t, hoist = 1) { U.uT.value = t; for (const c of cloths) c.cl.position.y = c.low + (c.top - c.low) * Math.max(0, Math.min(1, hoist)); } };
}

function pip(p, r) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > p[1]) !== (r[j][1] > p[1]) && p[0] < (r[j][0] - r[i][0]) * (p[1] - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; }

// luống vườn: lưới bám DTM trong hộp bao vòng, loại ô ngoài vòng; sọc luống xanh lá / xanh vàng / đất theo hướng lô (bản đồ: sọc luống); cây (tuỳ chọn) trong vòng
export function gardens(feats, ctx, { trees = {}, houses = true, seed = 5 } = {}) {
  const group = new THREE.Group(), R = rng(seed), stat = { vuon: 0, cay: 0, nha: 0, m2: 0 };
  const hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3);
  const mat = new THREE.MeshLambertMaterial({ vertexColors: true, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }); maskify(mat, ctx.U, 1);
  const treeRecs = [], houseRecs = [];
  for (const f of feats.filter((x) => x.loai === 'vuon')) {
    const r = f.ring, xs = r.map((p) => p[0]), ys = r.map((p) => p[1]), e0 = Math.min(...xs), e1 = Math.max(...xs), n0 = Math.min(...ys), n1 = Math.max(...ys), st = 1.5, P = [], C = [];
    const ang = R() * Math.PI, ca = Math.cos(ang), sa = Math.sin(ang), plots = 18 + Math.floor(R() * 10);
    for (let e = e0; e < e1; e += st) for (let n = n0; n < n1; n += st) {
      const c = [e + st / 2, n + st / 2]; if (!pip(c, r)) continue;
      const u = (c[0] * ca + c[1] * sa), v = (-c[0] * sa + c[1] * ca), plot = Math.floor(v / plots + 100) * 7 + Math.floor(u / (plots * 1.7) + 100), row = Math.floor(u / 1.5 + 1000) % 2;   // lô (ô lớn) × luống (sọc 1,5 m)
      const pr = rng(plot * 31 + seed)(), base = pr < 0.45 ? [0.24, 0.34, 0.15] : pr < 0.75 ? [0.32, 0.38, 0.17] : pr < 0.9 ? [0.30, 0.31, 0.14] : [0.22, 0.31, 0.16];   // V5b-2d: lục trầm (chấm mù: 'ruộng sọc đồ chơi')
      const walk = (((u % 12) + 12) % 12) < 1.4 || (((v % 16) + 16) % 16) < 1.4;   // lối đi đất nện giữa các lô
      const col = walk ? [0.62, 0.53, 0.40] : row ? base : [0.42, 0.33, 0.23], q = [[e, n], [e + st, n], [e + st, n + st], [e, n + st]];   // luống: sọc cây xanh xen sọc đất
      for (const k of [0, 1, 2, 0, 2, 3]) { const [qe, qn] = q[k]; P.push(qe, hAt(qe, qn) + 0.15, -qn); C.push(...col); }
      stat.m2 += st * st;
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.computeVertexNormals();
    const o = new THREE.Mesh(g, mat); o.receiveShadow = true; group.add(o); stat.vuon++;
    const tr = trees[f.id]; if (tr) { let got = 0; for (let k = 0; k < tr * 20 && got < tr; k++) { const p = [e0 + R() * (e1 - e0), n0 + R() * (n1 - n0)]; if (pip(p, r)) { treeRecs.push(p); got++; } } }   // tr = số cây (minh hoạ) TRONG vòng vườn
  }
  if (treeRecs.length && ctx.v6people) {   // V6 (V2D-1): cây vườn ĐỊA TRUNG HẢI (cam/vả/ô liu — loài minh hoạ): tán nhiều cụm méo, sáng trên/tối dưới, thân + 2–3 cành; thay "cây kẹo mút"
    const geo = treeGeoV6(rng(seed * 7 + 3)), mc = new THREE.MeshLambertMaterial({ vertexColors: true }); maskify(mc, ctx.U, 1);
    const ic = new THREE.InstancedMesh(geo, mc, treeRecs.length), m4 = new THREE.Matrix4(), col = new THREE.Color();
    treeRecs.forEach(([e, n], i) => { const s = 0.75 + 0.5 * R(); m4.compose(new THREE.Vector3(e, hAt(e, n) - 0.1, -n), new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), R() * 6.28), new THREE.Vector3(s * (0.9 + 0.2 * R()), s * (0.85 + 0.3 * R()), s * (0.9 + 0.2 * R())));
      ic.setMatrixAt(i, m4); col.setRGB(0.85 + 0.25 * R(), 0.88 + 0.22 * R(), 0.8 + 0.25 * R()); ic.setColorAt(i, col); });
    ic.castShadow = ic.receiveShadow = true; group.add(ic); stat.cay = treeRecs.length; treeRecs.length = 0;
  }
  if (treeRecs.length) {   // cây vườn: tán tròn lục đậm + thân (cùng kiểu nature.js), cao 4–7 m
    const geo = new THREE.IcosahedronGeometry(1, 1); geo.scale(1.5, 1.1, 1.5); geo.translate(0, 2.2, 0); { const ps = geo.attributes.position; for (let i = 0; i < ps.count; i++) { const x = ps.getX(i), y = ps.getY(i), z = ps.getZ(i), h = Math.sin(x * 12.9 + y * 78.2 + z * 37.7) * 43758.5, k = 0.8 + 0.35 * (h - Math.floor(h)); ps.setXYZ(i, x * k, 2.2 + (y - 2.2) * k, z * k); } geo.computeVertexNormals(); }   // tán xô lệch (không 'kẹo mút')
    const trunk = new THREE.CylinderGeometry(0.12, 0.16, 1.6, 5).translate(0, 0.8, 0);
    const mc = new THREE.MeshLambertMaterial({ color: 0x33522a }), mt = new THREE.MeshLambertMaterial({ color: 0x5a4330 }); maskify(mc, ctx.U, 1); maskify(mt, ctx.U, 1);
    const ic = new THREE.InstancedMesh(geo, mc, treeRecs.length), it = new THREE.InstancedMesh(trunk, mt, treeRecs.length), m4 = new THREE.Matrix4(), col = new THREE.Color();
    treeRecs.forEach(([e, n], i) => { const s = 0.6 + 0.45 * R(); m4.compose(new THREE.Vector3(e, hAt(e, n), -n), new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), R() * 6.28), new THREE.Vector3(s, s * (0.9 + 0.3 * R()), s));
      ic.setMatrixAt(i, m4); it.setMatrixAt(i, m4); col.setRGB(0.8 + 0.35 * R(), 0.85 + 0.3 * R(), 0.75 + 0.3 * R()); ic.setColorAt(i, col); });
    ic.castShadow = it.castShadow = true; group.add(ic, it); stat.cay = treeRecs.length;
  }
  if (houses) for (const f of feats.filter((x) => x.loai === 'nha_vuon')) houseRecs.push([1700, 0, 4.2, null, 1, 1, f.ring, 0]);
  if (houseRecs.length) { const recs = houseRecs.map((r) => [r[0], r[1], r[2], Math.min(...r[6].map(([e, n]) => hAt(e, n))), r[4], r[5], r[6], r[7]]); const c = makeCity(recs, ctx.U, { lod: false }); group.add(c.group); stat.nha = recs.length; group.userData.city = c; }
  return { group, stat, update(cam) { if (group.userData.city && cam) group.userData.city.update(cam); } };
}

// ---------- điểm nhấn phố 1782 ----------
function ringBox(P, N, C, ring, y0, y1, col, R) {   // tường đùn của vòng (pháp tuyến phẳng), mặt trên phẳng
  const tri = THREE.ShapeUtils.triangulateShape(ring.map(([x, y]) => new THREE.Vector2(x, y)), []);
  const push = (a, b, c, cc) => { P.push(...a, ...b, ...c); C.push(...cc, ...cc, ...cc); };
  for (let i = 0; i < ring.length; i++) { const a = ring[i], b = ring[(i + 1) % ring.length], k = 0.9 + 0.12 * R(), cc = col.map((v) => v * k);
    push([a[0], y0, -a[1]], [b[0], y0, -b[1]], [b[0], y1, -b[1]], cc); push([a[0], y0, -a[1]], [b[0], y1, -b[1]], [a[0], y1, -a[1]], cc); }
  for (const [a, b, c] of tri) push([ring[a][0], y1, -ring[a][1]], [ring[b][0], y1, -ring[b][1]], [ring[c][0], y1, -ring[c][1]], col.map((v) => v * 0.86));
}
function pyramid(P, C, cx, cn, half, y0, hh, col) { const q = [[cx - half, cn - half], [cx + half, cn - half], [cx + half, cn + half], [cx - half, cn + half]];
  for (let i = 0; i < 4; i++) { const a = q[i], b = q[(i + 1) % 4]; P.push(a[0], y0, -a[1], b[0], y0, -b[1], cx, y0 + hh, -cn); C.push(...col, ...col, ...col.map((v) => v * 0.8)); } }
const cen = (r) => [r.reduce((s, q) => s + q[0], 0) / r.length, r.reduce((s, q) => s + q[1], 0) / r.length];
function inset(r, d) { const c = cen(r); return r.map(([e, n]) => { const v = [e - c[0], n - c[1]], l = Math.hypot(...v) || 1; return [e - v[0] / l * d, n - v[1] / l * d]; }); }
export function landmarks(L, ctx) {
  const group = new THREE.Group(), R = rng(911), stat = {};
  const P = [], N = [], C = [], hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3);
  const lime = [0.93, 0.89, 0.80], ochre = [0.86, 0.72, 0.50], tile = [0.72, 0.30, 0.16], dark = [0.16, 0.13, 0.12];
  const ch = L['N1782-09'];   // Spanish Church (St Mary the Crowned): thân 13 m + tháp chuông vuông 7 m cạnh, cao 24 m, mái chóp ngói (minh hoạ chiều cao)
  if (ch) { const r = ch.ring, b = Math.min(...r.map(([e, n]) => hAt(e, n))) - 0.5, c = cen(r);
    ringBox(P, N, C, inset(r, 2.5), b, b + 13, lime, R);
    const tw = [c[0] + 8, c[1] + 8], hs = 3.5, tr = [[tw[0] - hs, tw[1] - hs], [tw[0] + hs, tw[1] - hs], [tw[0] + hs, tw[1] + hs], [tw[0] - hs, tw[1] + hs]];
    ringBox(P, N, C, tr, b, b + 24, ochre, R);
    for (const [dx, dn] of [[0, -hs - 0.05], [hs + 0.05, 0], [0, hs + 0.05], [-hs - 0.05, 0]]) {   // ô cửa chuông tối ở 4 mặt
      const o = [tw[0] + dx, tw[1] + dn], along = dx === 0 ? [1, 0] : [0, 1], w = 1.3, y0 = b + 19.5, y1 = b + 22.5, A = [o[0] - along[0] * w, o[1] - along[1] * w], B = [o[0] + along[0] * w, o[1] + along[1] * w];
      P.push(A[0], y0, -A[1], B[0], y0, -B[1], B[0], y1, -B[1], A[0], y0, -A[1], B[0], y1, -B[1], A[0], y1, -A[1]); for (let k = 0; k < 6; k++) C.push(...dark); }
    pyramid(P, C, tw[0], tw[1], hs + 0.4, b + 24, 4.5, tile); stat.nha_tho = { tam: c.map(Math.round), cao_than: 13, cao_thap: 28.5 }; }
  const cv = L['N1782-07'];   // dinh Thống đốc (Convent): khối 3 tầng 11 m quanh sân trong (vòng ghost SH là ô vuông có sân), vữa vàng nhạt
  if (cv) { const r = cv.ring, b = Math.min(...r.map(([e, n]) => hAt(e, n))) - 0.5; ringBox(P, N, C, r, b, b + 11, [0.92, 0.84, 0.66], R);
    const c = cen(r); pyramid(P, C, c[0], c[1], Math.max(4, Math.sqrt(Math.abs(r.reduce((a, p, i) => a + p[0] * r[(i + 1) % r.length][1] - r[(i + 1) % r.length][0] * p[1], 0)) / 2) / 2), b + 11, 2.2, tile); stat.convent = { tam: c.map(Math.round), cao: 11 }; }
  if (P.length) { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.computeVertexNormals();
    const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); maskify(m, ctx.U, 1); const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true; group.add(o); }
  return { group, stat };
}

// ---------- đồ trên sàn pháo (King's Bastion) ----------
//  guns: [{e, n, rot, y}] (fort.js stat.guns) · floor: vòng sàn pháo (ENU) · y: cốt sàn. Trả vị trí PHÁO THỦ đề xuất (sau bệ pháo, tránh đồ) cho layers.units.
export function battery(guns, floor, y, ctx, { seed = 7, sheds = 3, kegs = 4, furnace = true } = {}) {
  const group = new THREE.Group(), R = rng(seed), P = [], C = [], stat = { dan: 0, thung: 0, lan: 0, lo: 0 };
  const box = (cx, cy, cn, L, H, W, rot, col) => { const c = Math.cos(rot), s = Math.sin(rot), pt = (x, z) => [cx + c * x - s * z, cn + s * x + c * z], q = [pt(-L / 2, -W / 2), pt(L / 2, -W / 2), pt(L / 2, W / 2), pt(-L / 2, W / 2)];
    const k = 0.9 + 0.15 * R(), cc = col.map((v) => v * k);
    for (let i = 0; i < 4; i++) { const a = q[i], b = q[(i + 1) % 4]; P.push(a[0], cy, -a[1], b[0], cy, -b[1], b[0], cy + H, -b[1], a[0], cy, -a[1], b[0], cy + H, -b[1], a[0], cy + H, -a[1]); for (let j = 0; j < 6; j++) C.push(...cc); }
    P.push(q[0][0], cy + H, -q[0][1], q[1][0], cy + H, -q[1][1], q[2][0], cy + H, -q[2][1], q[0][0], cy + H, -q[0][1], q[2][0], cy + H, -q[2][1], q[3][0], cy + H, -q[3][1]); for (let j = 0; j < 6; j++) C.push(...cc.map((v) => v * 1.08)); };
  const crews = [];
  for (const g of guns) {
    const back = [-Math.cos(g.rot), -Math.sin(g.rot)], side = [-back[1], back[0]];
    // pháo thủ: 4 người quanh đuôi bệ (2 bên + 2 sau) — vị trí cho units()
    crews.push({ at: [g.e + back[0] * 3.6, g.n + back[1] * 3.6], heading: (90 - g.rot * 180 / Math.PI + 360) % 360, gun: g });
    { const b = [g.e + back[0] * 6.0 + side[0] * 2.6, g.n + back[1] * 6.0 + side[1] * 2.6]; box(b[0] + back[0] * 1.6, y, b[1] + back[1] * 1.6, 1.4, 0.55, 0.8, g.rot, [0.46, 0.33, 0.20]); box(b[0] + back[0] * 1.6, y + 0.55, b[1] + back[1] * 1.6, 1.5, 0.06, 0.9, g.rot, [0.30, 0.24, 0.17]); }   // hòm đạn/dụng cụ sau mỗi khẩu
    if (R() < 0.85) { const b = [g.e + back[0] * 5.5 + side[0] * 2.2, g.n + back[1] * 5.5 + side[1] * 2.2];   // đống đạn tròn xếp tháp
      for (let lv = 0; lv < 4; lv++) for (let i = 0; i < 4 - lv; i++) for (let j = 0; j < 4 - lv; j++) box(b[0] + (i - (3 - lv) / 2) * 0.3, y + lv * 0.26, b[1] + (j - (3 - lv) / 2) * 0.3, 0.27, 0.27, 0.27, g.rot, [0.14, 0.13, 0.13]); stat.dan++; }
  }
  // thùng thuốc súng: cụm sau tuyến pháo, gần mặt hậu (che khuất khỏi hướng địch)
  const fc = cen(floor), far = floor.slice().sort((a, b) => Math.hypot(b[0] - fc[0], b[1] - fc[1]) - Math.hypot(a[0] - fc[0], a[1] - fc[1]));
  const gorge = floor.reduce((m, p) => (p[0] > m[0] ? p : m), floor[0]);   // đỉnh cực đông = phía hậu (về phố)
  for (let k = 0; k < kegs; k++) { const c = [fc[0] + (gorge[0] - fc[0]) * 0.55 + (R() - 0.5) * 14, fc[1] + (gorge[1] - fc[1]) * 0.55 + (R() - 0.5) * 18];
    for (let i = 0; i < 6; i++) { const e = c[0] + (i % 3) * 0.75, n = c[1] + Math.floor(i / 3) * 0.75; box(e, y, n, 0.6, 0.8, 0.6, 0.3, [0.42, 0.29, 0.17]); box(e, y + 0.18, n, 0.64, 0.08, 0.64, 0.3, [0.2, 0.18, 0.16]); box(e, y + 0.58, n, 0.64, 0.08, 0.64, 0.3, [0.2, 0.18, 0.16]); } stat.thung += 6; }
  // lán chắn mảnh (splinter-proof): khung gỗ + mái ván nghiêng phủ đất, dọc phía hậu
  for (let k = 0; k < sheds; k++) { const u = (k + 0.5) / sheds, p = [fc[0] + (gorge[0] - fc[0]) * 0.8, fc[1] - 30 + 60 * u], rot = Math.PI / 2;
    box(p[0], y, p[1], 9, 2.4, 4, rot, [0.48, 0.36, 0.24]); box(p[0] + 0.3, y + 2.4, p[1], 9.6, 0.5, 4.6, rot, [0.56, 0.46, 0.32]); stat.lan++; }
  if (furnace) { const p = [fc[0] + (gorge[0] - fc[0]) * 0.35, fc[1] + 22]; box(p[0], y, p[1], 3.2, 1.8, 2.4, 0, [0.56, 0.36, 0.26]); box(p[0] + 0.9, y + 1.8, p[1], 0.7, 2.6, 0.7, 0, [0.46, 0.30, 0.22]); stat.lo = 1; stat.lo_at = p; }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); maskify(m, ctx.U, 1); const o = new THREE.Mesh(g, m); o.castShadow = o.receiveShadow = true; group.add(o);
  return { group, stat, crews };
}

// V6: lưới cây vườn (≈ 5 m): thân thon + 3 cành, tán = 5–7 cụm cầu méo nhiễu, màu đỉnh sáng/đáy tối (giả AO), xen lá vàng-xanh
export function treeGeoV6(R) {
  const P = [], C = [], push = (g, colf) => { const ps = g.attributes.position, nonIdx = g.index ? g.toNonIndexed() : g, q = nonIdx.attributes.position; for (let i = 0; i < q.count; i++) { const x = q.getX(i), y = q.getY(i), z = q.getZ(i); P.push(x, y, z); C.push(...colf(x, y, z)); } };
  const bark = () => [0.24, 0.18, 0.13];
  const trunk = new THREE.CylinderGeometry(0.11, 0.2, 2.3, 6, 2).translate(0, 1.15, 0); push(trunk, bark);
  for (let k = 0; k < 3; k++) { const a = k * 2.1 + R(), b = new THREE.CylinderGeometry(0.05, 0.09, 1.6, 5).translate(0, 0.8, 0); b.rotateZ(0.7 + 0.2 * R()); b.rotateY(a); b.translate(0, 1.9, 0); push(b, bark); }
  const nb = 5 + Math.floor(R() * 3);
  for (let k = 0; k < nb; k++) { const a = R() * 6.283, rr = k === 0 ? 0 : 0.9 + 0.7 * R(), cy = 3.0 + (k === 0 ? 0.6 : R() * 1.3), sz = k === 0 ? 1.6 : 0.9 + 0.6 * R();
    const g = new THREE.IcosahedronGeometry(sz, 1); const ps = g.attributes.position; for (let i = 0; i < ps.count; i++) { const x = ps.getX(i), y = ps.getY(i), z = ps.getZ(i), h = Math.sin(x * 12.9 + y * 78.2 + z * 37.7 + k * 3.1) * 43758.5, f = 0.78 + 0.4 * (h - Math.floor(h)); ps.setXYZ(i, x * f, y * f * 0.85, z * f); }
    g.translate(Math.cos(a) * rr, cy, Math.sin(a) * rr);
    const tint = R() < 0.25 ? [0.30, 0.36, 0.14] : [0.17, 0.27, 0.10];
    push(g, (x, y, z) => { const t = Math.max(0, Math.min(1, (y - 2.0) / 3.2)), k2 = 0.55 + 0.6 * t; return tint.map((v) => v * k2); }); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.computeVertexNormals(); return g;
}

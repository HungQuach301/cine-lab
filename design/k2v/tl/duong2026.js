// V7C (việc 2e) · PHỐ 2026 CẬN HERO: cây đường phố, cột đèn, xe đỗ dọc đường OSM (La Línea + Gibraltar) — để khung hero hết "khối trơn".
//  Vị trí: theo trục đường OSM 2026 (roads.json của gói, ODbL — bậc 1 cho tuyến phố); khoảng cách/mật độ cây–đèn–xe: bậc 5 (tương đồng phố Andalucía/Gibraltar hiện nay),
//  chỉ là VẬT NỀN PHỤ (BIBLE §12.2). Không đặt vào trong dấu chân toà (kiểm điểm-trong-đa-giác với tệp nhà của shot). Chỉ hiện khi năm ≥ opt.y0 (mặc định 1995).
//  streetLife(ctx, { box: [E0, N0, E1, N1], y0, treeEvery, lampEvery, carEvery, seed })
import { rng } from './core.js';

const TREE_C = ['primary', 'secondary', 'tertiary', 'trunk'], LAMP_C = ['primary', 'secondary', 'tertiary', 'residential', 'living_street', 'unclassified', 'trunk'], CAR_C = ['residential', 'tertiary', 'secondary', 'living_street', 'unclassified'];
const CAR_COL = [[0.92, 0.92, 0.9], [0.62, 0.64, 0.66], [0.12, 0.12, 0.13], [0.78, 0.79, 0.8], [0.2, 0.3, 0.52], [0.6, 0.12, 0.1], [0.85, 0.85, 0.82], [0.35, 0.36, 0.38]];

export async function streetLife(ctx, o = {}) {
  const { THREE, terr, scene } = ctx, R = rng(o.seed || 2026), box = o.box || [-3000, -3000, 2000, 3000];
  const roads = await ctx.loadJSON(`${ctx.base}roads.json`), B = await ctx.loadJSON(ctx.base + ((ctx.opt && ctx.opt.bfile) || 'buildings.json'));
  // lưới băm dấu chân toà (ô 25 m) — để không đặt cây/xe/đèn vào trong nhà
  const G = new Map(), cell = 25, key = (e, n) => Math.floor(e / cell) + ',' + Math.floor(n / cell);
  for (const b of B) { const p = b[6]; if (!p || p.length < 3) continue; let e0 = 1e9, e1 = -1e9, n0 = 1e9, n1 = -1e9; for (const [e, n] of p) { e0 = Math.min(e0, e); e1 = Math.max(e1, e); n0 = Math.min(n0, n); n1 = Math.max(n1, n); }
    if (e1 < box[0] || e0 > box[2] || n1 < box[1] || n0 > box[3]) continue;
    for (let i = Math.floor(e0 / cell); i <= Math.floor(e1 / cell); i++) for (let j = Math.floor(n0 / cell); j <= Math.floor(n1 / cell); j++) { const k = i + ',' + j; if (!G.has(k)) G.set(k, []); G.get(k).push(p); } }
  const pip = (e, n, r) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) if ((r[i][1] > n) !== (r[j][1] > n) && e < (r[j][0] - r[i][0]) * (n - r[i][1]) / (r[j][1] - r[i][1]) + r[i][0]) c = !c; return c; };
  const inside = (e, n, pad = 1.2) => { for (const [de, dn] of [[0, 0], [pad, 0], [-pad, 0], [0, pad], [0, -pad]]) { const L = G.get(key(e + de, n + dn)); if (L && L.some((r) => pip(e + de, n + dn, r))) return true; } return false; };
  const along = (classes, every, side) => { const out = [];
    for (const r of roads) { if (!classes.includes(r.c)) continue; let acc = every * R();
      for (let i = 0; i < r.p.length - 1; i++) { const a = r.p[i], b = r.p[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l < 1) continue;
        while (acc < l) { const u = acc / l, nx = -(b[1] - a[1]) / l, ny = (b[0] - a[0]) / l;
          for (const s of side) { const off = s * ((r.w || 6) / 2 + (o.kerb ?? 1.8)), e = a[0] + (b[0] - a[0]) * u + nx * off, n = a[1] + (b[1] - a[1]) * u + ny * off;
            if (e > box[0] && e < box[2] && n > box[1] && n < box[3] && terr.hAt(e, n) > 0.6 && !inside(e, n)) out.push([e, n, Math.atan2(b[1] - a[1], b[0] - a[0])]); }
          acc += every * (0.8 + 0.4 * R()); }
        acc -= l; } }
    return out; };
  const group = new THREE.Group(); group.name = 'duong2026';
  const put = (geo, mat, P, sc) => { const im = new THREE.InstancedMesh(geo, mat, Math.max(1, P.length)), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), Y = new THREE.Vector3(0, 1, 0);
    P.forEach((p, i) => { const s = sc ? sc(p, i) : [1, 1, 1]; m4.compose(new THREE.Vector3(p[0], terr.hAt(p[0], p[1]), -p[1]), q.setFromAxisAngle(Y, p[2] + (p[3] || 0)), new THREE.Vector3(...s)); im.setMatrixAt(i, m4); });
    im.count = P.length; im.castShadow = true; im.receiveShadow = true; ctx.maskify(mat, ctx.U, 1); return im; };
  function streetTrees() {   // cây đường phố: thân + tán (2 khối) — cây cảnh Địa Trung Hải (tán tròn), cao 5–8 m
    const P = along(TREE_C, o.treeEvery || 11, [1, -1]); if (!P.length) return 0;
    const trunk = new THREE.CylinderGeometry(0.16, 0.22, 2.4, 6).translate(0, 1.2, 0), crown = new THREE.IcosahedronGeometry(2.3, 1).scale(1, 0.85, 1).translate(0, 4.0, 0);
    const mt = new THREE.MeshLambertMaterial({ color: 0x5a4632 }), mc = new THREE.MeshLambertMaterial({ color: 0x4f6b2e });
    const sc = (p, i) => { const k = 0.75 + 0.5 * ((i * 0.6180339) % 1); return [k, k, k]; };
    const a = put(trunk, mt, P, sc), b = put(crown, mc, P, sc);
    const col = new THREE.Color(); P.forEach((p, i) => { col.setRGB(0.26 + 0.08 * ((i * 0.37) % 1), 0.38 + 0.1 * ((i * 0.71) % 1), 0.17 + 0.05 * ((i * 0.13) % 1)); b.setColorAt(i, col); }); if (b.instanceColor) b.instanceColor.needsUpdate = true;
    group.add(a, b); return P.length; }
  function streetLamps() {   // cột đèn đường (ban ngày thấy cột + chao): cùng nhịp đèn đêm của t3tl (30–38 m)
    const P = along(LAMP_C, o.lampEvery || 34, [1]); if (!P.length) return 0;
    const pole = new THREE.CylinderGeometry(0.07, 0.1, 6.5, 5).translate(0, 3.25, 0), head = new THREE.BoxGeometry(0.9, 0.18, 0.35).translate(0.35, 6.5, 0);
    const mp = new THREE.MeshLambertMaterial({ color: 0x3a3d40 }); group.add(put(pole, mp, P), put(head, mp, P)); return P.length; }
  function parkedCars() {   // xe đỗ sát lề (≈ 55 % chỗ có xe), 4,3 × 1,8 × 1,45 m
    const P0 = along(CAR_C, o.carEvery || 6.2, [1, -1]).filter(() => R() < 0.55).map((p) => [p[0], p[1], p[2], 0]); if (!P0.length) return 0;
    const body = new THREE.BoxGeometry(4.3, 0.8, 1.8).translate(0, 0.55, 0), cab = new THREE.BoxGeometry(2.2, 0.62, 1.62).translate(-0.2, 1.2, 0);
    const mb = new THREE.MeshLambertMaterial({ color: 0xffffff }), mg = new THREE.MeshLambertMaterial({ color: 0x2a3138 });
    const a = put(body, mb, P0), b = put(cab, mg, P0), col = new THREE.Color(); P0.forEach((p, i) => { const c = CAR_COL[Math.floor(R() * CAR_COL.length)]; col.setRGB(...c); a.setColorAt(i, col); }); if (a.instanceColor) a.instanceColor.needsUpdate = true;
    group.add(a, b); return P0.length; }
  const n = { cay: streetTrees(), den: streetLamps(), xe: parkedCars() };
  scene.add(group);
  const y0 = o.y0 ?? 1995;
  return { group, n, update(Y) { group.visible = Y >= y0; },
    log: { lop: 'pho2026_vat_nen', n, nguon: 'tuyến phố OSM 2026 (roads.json, ODbL); cây/đèn/xe đỗ: khoảng cách và mật độ ước theo phố Andalucía–Gibraltar hiện nay', bac: 'tuyến: bậc 1 · mật độ/kiểu: bậc 5 (vật nền phụ)' } };
}

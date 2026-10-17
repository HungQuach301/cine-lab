// KÊNH 2 · phòng dựng STICKER VẬT (phiên V2, 14/10/2026): render biểu tượng từ vật thể 3D của kênh (lò cao + xưởng K2G-01, nhà K2C-T1-06 — nạp qua
// /ll-hero/<tệp>.js?rx=<hàm> để KHÔNG sửa tệp tập) và vật mới đơn giản (mỏ, tàu, thuyền kênh, xu, văn bản, nhà máy, ngân hàng, cờ trung tính, xe hàng, bao, thùng).
// Một phong cách: vật liệu toon 3 nấc, góc 3/4 cố định (phương vị 35°, cao 26°), đèn chính trên-trái; viền + bóng do STK.style (scripts/k2/lib/sticker.js).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';

const GRAD = (() => { const d = new Uint8Array([90, 90, 90, 255, 175, 175, 175, 255, 255, 255, 255, 255]); const t = new THREE.DataTexture(d, 3, 1, THREE.RGBAFormat); t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t; })();
const toon = (color, o = {}) => new THREE.MeshToonMaterial({ color, gradientMap: GRAD, ...o });
const B = (w, h, d, m, x = 0, y = 0, z = 0, p) => { const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.position.set(x, y, z); p.add(o); return o; };
const Cy = (r0, r1, h, m, x = 0, y = 0, z = 0, p, s = 24) => { const o = new THREE.Mesh(new THREE.CylinderGeometry(r0, r1, h, s), m); o.position.set(x, y, z); p.add(o); return o; };
// chuyển vật liệu của mô hình có sẵn sang toon (giữ màu + vân), bỏ đèn/sprite phát sáng
function toonify(root) {
  const kill = [];
  root.traverse((o) => { if (o.isLight || o.isSprite || o.isPoints) kill.push(o);
    if (o.isMesh) { const m = o.material; o.material = toon(m.color ? m.color.clone() : '#ffffff', { map: m.map || null, emissive: m.emissive ? m.emissive.clone().multiplyScalar(m.emissiveIntensity ?? 1) : '#000000' }); } });
  for (const o of kill) o.parent.remove(o); return root;
}
export const OWN = async () => {
  const g01 = await import('/ll-hero/k2g01.js?rx=blastFurnace,shed,mats'), c106 = await import('/ll-hero/k2c106.js?rx=house,walkup,mats');
  return { g01, c106 };
};
export const OBJECTS = {
  // ---- từ mô hình của kênh
  async furnace(own) { const g = new THREE.Group(); const M = own.g01.mats(); own.g01.blastFurnace(g, 0, 0, 0.6, M); return toonify(g); },
  async factory(own) { const g = new THREE.Group(); const M = own.g01.mats(); own.g01.shed(g, M, 0, 0, 12, 8, 5, 0, 0.5); const ch = toon('#6e5a4a');
    for (const [x, h] of [[3.5, 11], [5.5, 9]]) { Cy(0.55, 0.75, h, ch, x, h / 2, -2.4, g, 16); Cy(0.68, 0.68, 0.5, toon('#3a3430'), x, h, -2.4, g, 16); } return toonify(g); },
  async house(own) { const g = new THREE.Group(); window.__scene = g; const M = own.c106.mats(); own.c106.house(0, 0, { w: 6, d: 7, h: 3.2, mat: M.clap, roofC: '#6b3f30', T: { lit: 0.2 }, seed: 3, parent: g }); return toonify(g); },
  async town(own) { const g = new THREE.Group(); window.__scene = g; const M = own.c106.mats();
    own.c106.house(-4, 2, { w: 5, d: 6, h: 3, mat: M.clap2, roofC: '#5a4a40', T: { lit: 0.2 }, seed: 5, parent: g }); own.c106.house(3, -1, { w: 6, d: 7, h: 5.5, mat: M.brick2, roofC: '#3a3c40', T: { lit: 0.2 }, seed: 8, parent: g });
    own.c106.house(-1, -6, { w: 5, d: 5, h: 3.4, mat: M.stucco, roofC: '#7a4a36', T: { lit: 0.2 }, seed: 2, parent: g }); return toonify(g); },
  // ---- vật mới, đơn giản
  async mine() { const g = new THREE.Group(), wd = toon('#8a6238'), ir = toon('#4a4f57'), ore = toon('#3a3a3e');
    for (const [x, z] of [[-1.6, -1.6], [1.6, -1.6], [-1.6, 1.6], [1.6, 1.6]]) { const l = B(0.35, 9, 0.35, wd, x * 0.75, 4.5, z * 0.75, g); l.rotation.z = -x * 0.05; l.rotation.x = z * 0.05; }
    for (let y = 2; y < 8.5; y += 2.2) { B(3.3, 0.25, 0.25, wd, 0, y, 1.2, g); B(3.3, 0.25, 0.25, wd, 0, y, -1.2, g); }
    const wh = new THREE.Mesh(new THREE.TorusGeometry(1.3, 0.16, 8, 32), ir); wh.position.set(0, 9.4, 0); g.add(wh); Cy(0.25, 0.25, 0.6, ir, 0, 9.4, 0, g).rotation.x = Math.PI / 2;
    B(5, 3.2, 4, toon('#7d6a58'), -4.6, 1.6, 0.5, g); const rf = B(5.6, 0.3, 4.6, toon('#4a3a33'), -4.6, 3.4, 0.5, g); rf.rotation.z = 0.12;
    const cart = new THREE.Group(); cart.position.set(3.4, 0, 3.2); g.add(cart); B(2.6, 1.2, 1.6, ir, 0, 1.1, 0, cart); for (const x of [-0.8, 0.8]) for (const z of [-0.85, 0.85]) Cy(0.38, 0.38, 0.2, toon('#2b2f36'), x, 0.4, z, cart, 16).rotation.x = Math.PI / 2;
    for (let i = 0; i < 7; i++) { const o = new THREE.Mesh(new THREE.DodecahedronGeometry(0.42, 0), ore); o.position.set(-0.8 + (i % 4) * 0.5, 1.85 + (i > 3 ? 0.3 : 0), -0.3 + (i % 2) * 0.6); cart.add(o); } return g; },
  async ship() { const g = new THREE.Group(), hull = toon('#5a3e2a'), sail = toon('#f1ebdc');
    const sh = new THREE.Shape(); sh.moveTo(-7, 0); sh.quadraticCurveTo(-6.5, -2.2, -3, -2.4); sh.lineTo(5, -2.4); sh.quadraticCurveTo(8, -2, 9, 0.6); sh.lineTo(-7, 0.6); const hg = new THREE.ExtrudeGeometry(sh, { depth: 3.2, bevelEnabled: false }); hg.translate(0, 2.4, -1.6);
    g.add(new THREE.Mesh(hg, hull)); B(16, 0.3, 3.4, toon('#c9a24a'), 1, 2.6, 0, g);
    for (const [x, h] of [[-3, 10], [2.5, 12]]) { Cy(0.16, 0.2, h, toon('#4a3626'), x, 3 + h / 2, 0, g, 10); for (let k = 0; k < 2; k++) { const s = B(0.12, h * 0.34, 4.4 - k * 0.8, sail, x + 0.25, 4.6 + k * h * 0.38 + h * 0.17, 0, g); s.rotation.y = 0.25; } }
    const jib = new THREE.Mesh(new THREE.ConeGeometry(2.4, 7, 3, 1, true), sail); jib.position.set(7, 9, 0); jib.scale.z = 0.05; g.add(jib); return g; },
  async boat() { const g = new THREE.Group(), hull = toon('#6b4a30'), cab = toon('#d9c7a0'), roof = toon('#3f74b8');
    B(14, 1.6, 3.2, hull, 0, 0.8, 0, g); B(14.4, 0.25, 3.5, toon('#4a3626'), 0, 1.65, 0, g); B(7, 1.6, 2.6, cab, -1, 2.6, 0, g); B(7.4, 0.25, 3, roof, -1, 3.5, 0, g);
    for (let i = 0; i < 5; i++) B(0.8, 0.7, 0.08, toon('#2b3a4a'), -4 + i * 1.5, 2.8, 1.31, g);
    for (let i = 0; i < 3; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(0.7, 12, 8), toon('#d8c39a')); s.position.set(4 + i * 0.9, 2.1, (i % 2 - 0.5) * 1.1); s.scale.y = 0.7; g.add(s); } return g; },
  async coin() { const g = new THREE.Group(), au = toon('#d9a640'), rim = toon('#b7832c'); const c = Cy(3, 3, 0.7, au, 0, 0, 0, g, 48); const r = new THREE.Mesh(new THREE.TorusGeometry(2.35, 0.13, 6, 48), rim); r.rotation.x = Math.PI / 2; r.position.y = 0.36; g.add(r); Cy(1.2, 1.2, 0.05, rim, 0, 0.37, 0, g, 32);
    g.rotation.set(0.95, 0, -0.25); return g; },
  async coins() { const g = new THREE.Group(), au = toon('#d9a640'), rim = toon('#b7832c');
    for (let i = 0; i < 6; i++) { Cy(2.4, 2.4, 0.5, au, Math.sin(i * 2.1) * 0.15, 0.25 + i * 0.52, Math.cos(i * 1.7) * 0.15, g, 40); const r = new THREE.Mesh(new THREE.TorusGeometry(2.38, 0.07, 6, 40), rim); r.rotation.x = Math.PI / 2; r.position.y = 0.5 + i * 0.52; g.add(r); }
    const s = Cy(2.4, 2.4, 0.5, au, 3.6, 2.4, 0.4, g, 40); s.rotation.z = Math.PI / 2 - 0.2; return g; },
  async document() { const g = new THREE.Group(), pap = toon('#f3ecdc'), ln = toon('#9a8f7c'); const p = B(6, 0.12, 8, pap, 0, 0.06, 0, g);
    for (let i = 0; i < 7; i++) B(i === 0 ? 3.4 : 4.6 - (i % 3) * 0.6, 0.02, 0.22, ln, -0.4 + (i === 0 ? -0.6 : 0), 0.14, -3 + i * 0.85, g);
    const seal = Cy(0.85, 0.85, 0.22, toon('#b3322a'), 1.6, 0.22, 2.7, g, 20); const rb = B(0.4, 0.04, 2.0, toon('#b3322a'), 1.3, 0.13, 3.6, g); rb.rotation.y = 0.3; void seal;
    g.rotation.x = 0.95; g.position.y = 3; return g; },
  async bank() { const g = new THREE.Group(), st = toon('#e4ddcf'), sh = toon('#bdb5a5');
    B(11, 0.6, 7, sh, 0, 0.3, 0, g); B(10, 0.5, 6.4, st, 0, 0.85, 0.2, g); B(9, 5.8, 5, toon('#d3cbbb'), 0, 4, -0.6, g);
    for (let i = 0; i < 4; i++) Cy(0.42, 0.48, 5.2, st, -3.3 + i * 2.2, 3.7, 2.4, g, 16);
    B(9.8, 0.7, 6.2, st, 0, 6.65, 0, g); const pd = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 5.6, 2.0, 3, 1), st); pd.rotation.z = Math.PI / 2; pd.rotation.y = Math.PI / 2; pd.scale.set(1, 1, 0.75); pd.position.set(0, 7.8, 0.2); pd.rotation.x = Math.PI; g.add(pd);
    B(1.8, 3, 0.1, toon('#4a3626'), 0, 2.6, 1.95, g); const cn = Cy(0.6, 0.6, 0.15, toon('#c9a24a'), 0, 7.7, 3.05, g, 24); cn.rotation.x = Math.PI / 2; return g; },
  async flag() { const g = new THREE.Group(); Cy(0.14, 0.18, 11, toon('#6b5a48'), 0, 5.5, 0, g, 10); Cy(0.3, 0.3, 0.3, toon('#c9a24a'), 0, 11.1, 0, g, 12);
    const geo = new THREE.PlaneGeometry(6, 3.8, 24, 6), P = geo.attributes.position; for (let i = 0; i < P.count; i++) { const x = P.getX(i) + 3; P.setZ(i, Math.sin(x * 1.1) * 0.35 * (x / 6)); } geo.translate(3, 0, 0); geo.computeVertexNormals();
    const f = new THREE.Mesh(geo, toon('#ece6d6', { side: THREE.DoubleSide })); f.position.set(0.15, 8.9, 0); g.add(f); return g; },
  async wagon() { const g = new THREE.Group(), wd = toon('#7a5532'), cv = toon('#efe6d2');
    B(7, 0.9, 3, wd, 0, 1.9, 0, g); for (const x of [-2.4, 2.4]) for (const z of [-1.7, 1.7]) { const w = new THREE.Mesh(new THREE.TorusGeometry(1.15, 0.16, 6, 20), toon('#4a3626')); w.position.set(x, 1.2, z); g.add(w); Cy(0.2, 0.2, 0.2, toon('#4a3626'), x, 1.2, z, g, 8).rotation.x = Math.PI / 2; }
    const cvd = cv.clone(); cvd.side = THREE.DoubleSide; const top = new THREE.Mesh(new THREE.CylinderGeometry(1.8, 1.8, 6.6, 20, 1, true, 0, Math.PI), cvd); top.rotation.z = Math.PI / 2; top.position.set(0, 2.35, 0); g.add(top);
    for (const x of [-3.3, -1.1, 1.1, 3.3]) { const rb = new THREE.Mesh(new THREE.TorusGeometry(1.82, 0.06, 4, 20, Math.PI), wd); rb.rotation.y = Math.PI / 2; rb.position.set(x, 2.35, 0); g.add(rb); }
    const tg = B(0.15, 0.15, 4.5, wd, 4.8, 1.6, 0, g); tg.rotation.y = Math.PI / 2; return g; },
  async sack() { const g = new THREE.Group(), m = toon('#d8c39a'); for (const [x, z, y] of [[-1.3, 0, 0], [1.3, 0.2, 0], [0, -0.2, 1.7]]) { const s = new THREE.Mesh(new THREE.SphereGeometry(1.5, 16, 12), m); s.scale.set(1, 0.75, 0.8); s.position.set(x, 1.1 + y, z); g.add(s); const k = Cy(0.35, 0.5, 0.6, toon('#bba57a'), x, 2.2 + y, z, g, 10); void k; } return g; },
  async mountain() { const g = new THREE.Group(), rk = toon('#7d8a6a', { flatShading: true }), sn = toon('#f2efe8', { flatShading: true });
    for (const [x, z, h, r] of [[0, 0, 7, 4.2], [-4.2, 1.2, 4.6, 3.2], [3.8, 1.6, 3.8, 2.8]]) { const c = new THREE.Mesh(new THREE.ConeGeometry(r, h, 7, 1), rk); c.position.set(x, h / 2, z); c.rotation.y = x; g.add(c);
      const cap = new THREE.Mesh(new THREE.ConeGeometry(r * 0.32, h * 0.32, 7, 1), sn); cap.position.set(x, h * 0.84 + 0.01, z); cap.rotation.y = x; g.add(cap); } return g; },
  async barrel() { const g = new THREE.Group(), wd = toon('#8a5a32'), hp = toon('#3c4148'); const prof = []; for (let i = 0; i <= 12; i++) { const y = i / 12 * 4.4; prof.push(new THREE.Vector2(1.5 + 0.28 * Math.sin(i / 12 * Math.PI), y)); }
    g.add(new THREE.Mesh(new THREE.LatheGeometry(prof, 28), wd)); for (const y of [0.5, 1.4, 3.0, 3.9]) { const h = new THREE.Mesh(new THREE.TorusGeometry(1.5 + 0.28 * Math.sin(y / 4.4 * Math.PI) + 0.02, 0.07, 6, 32), hp); h.rotation.x = Math.PI / 2; h.position.y = y; g.add(h); }
    Cy(1.5, 1.5, 0.05, toon('#a8743e'), 0, 4.4, 0, g, 28); return g; },
  // ---- T2 K2C-T2-01 (đóng tàu, 15/10/2026): tàu hàng kiểu Liberty (thân thẳng, cabin giữa, cột cần cẩu), cẩu cổng trục ụ tàu, phiếu ĐƠN HÀNG (motif xuyên tập)
  async freighter() { const g = new THREE.Group(), hull = toon('#4d5560'), deck = toon('#8a7a62'), house = toon('#e8e2d4'), red = toon('#8c3b2e'), mast = toon('#5b4a3a');
    const sh = new THREE.Shape(); sh.moveTo(-11, 2.6); sh.lineTo(-10.2, 0.4); sh.quadraticCurveTo(-9.6, -0.2, -8, -0.2); sh.lineTo(8.5, -0.2); sh.quadraticCurveTo(10.6, 0.2, 11.6, 2.9); sh.lineTo(-11, 2.6);
    const hg = new THREE.ExtrudeGeometry(sh, { depth: 3.4, bevelEnabled: false }); hg.translate(0, 0, -1.7); g.add(new THREE.Mesh(hg, hull));
    const bt = B(21.4, 0.5, 3.45, red, 0.2, 0.15, 0, g); void bt; B(21, 0.18, 3.3, deck, 0.2, 2.75, 0, g);
    B(4.2, 2.2, 3.0, house, -0.4, 3.95, 0, g); B(3.4, 1.2, 2.6, house, -0.4, 5.6, 0, g); B(4.6, 0.18, 3.3, toon('#5a5148'), -0.4, 5.1, 0, g); Cy(0.55, 0.65, 2.0, toon('#2f3238'), -0.2, 7.0, 0, g, 16);
    for (const x of [-7, -3.6, 3.6, 7.2]) { B(2.6, 0.7, 2.4, toon('#6b6256'), x, 3.15, 0, g); }
    for (const x of [-5.3, 5.4]) { Cy(0.16, 0.2, 7.5, mast, x, 6.5, 0, g, 10); for (const s of [-1, 1]) { const b = Cy(0.08, 0.1, 5.2, mast, x + s * 1.6, 5.4, 0, g, 8); b.rotation.z = -s * 0.75; } }
    return g; },
  async crane() { const g = new THREE.Group(), st = toon('#c9a24a'), dk = toon('#3a3c40'), rl = toon('#6e6a62'), wh = toon('#e8e2d4');   /* cẩu cổng trục kiểu goliath: hai chân là tấm đặc (không khe hẹp — viền sticker lấp khe thành dải trắng) */
    for (const x of [-6.5, 6.5]) { const leg = B(1.1, 14, 2.6, st, x, 7, 0, g); void leg; B(1.6, 0.8, 4.2, rl, x, 0.4, 0, g); }
    B(16.4, 2.0, 2.8, st, 0, 15, 0, g); B(3.2, 2.0, 3.2, wh, 2.2, 17.0, 0, g); B(3.4, 0.3, 3.4, dk, 2.2, 18.1, 0, g);
    B(1.8, 1.0, 2.0, dk, -1.5, 13.5, 0, g); Cy(0.06, 0.06, 6.5, dk, -1.5, 10.0, 0, g, 6); B(2.6, 0.6, 1.4, dk, -1.5, 6.6, 0, g);
    return g; },
  async order() { const g = new THREE.Group(), pap = toon('#f3ecdc'), ln = toon('#9a8f7c'), ink = toon('#2f4f6a');
    B(5.2, 0.14, 7.2, pap, 0, 0.07, 0, g); const tab = B(5.2, 0.14, 1.0, toon('#e2d6bc'), 0, 0.07, -4.1, g); void tab;
    for (let i = 0; i < 4; i++) B(3.8 - (i % 2) * 0.9, 0.02, 0.2, ln, -0.4, 0.15, -2.4 + i * 0.75, g);
    const s = new THREE.Shape(); s.moveTo(-1.8, 0); s.lineTo(1.9, 0); s.lineTo(1.5, -0.6); s.lineTo(-1.5, -0.6); s.lineTo(-1.8, 0); const hullG = new THREE.ShapeGeometry(s); const hull = new THREE.Mesh(hullG, ink); hull.rotation.x = -Math.PI / 2; hull.position.set(-0.2, 0.16, 1.9); g.add(hull);
    B(0.7, 0.02, 0.45, ink, -0.3, 0.16, 1.5, g); const ring = new THREE.Mesh(new THREE.TorusGeometry(1.35, 0.1, 6, 32), toon('#b3322a')); ring.rotation.x = -Math.PI / 2; ring.position.set(1.2, 0.17, 2.4); g.add(ring);
    g.rotation.x = 0.95; g.position.y = 3; return g; },
  // ---- T2 G1b: phương án chở hàng trên bộ (lời 03: "a truck, a train or a pipeline")
  async truck() { const g = new THREE.Group(), cab = toon('#3f74b8'), box = toon('#e8e2d4'), dk = toon('#2b2f36'), gl = toon('#9fc3dd');
    B(9, 4.2, 3.4, box, -1.5, 3.1, 0, g); B(3.2, 3.2, 3.2, cab, 4.7, 2.6, 0, g); B(0.1, 1.2, 2.4, gl, 6.31, 3.2, 0, g); B(14.2, 0.5, 3.0, dk, 0.2, 0.95, 0, g);
    for (const x of [-4.6, -2.6, 4.6]) for (const z of [-1.6, 1.6]) { const w = Cy(0.85, 0.85, 0.5, dk, x, 0.85, z, g, 20); w.rotation.x = Math.PI / 2; } return g; },
  async train() { const g = new THREE.Group(), loco = toon('#8c3b2e'), car = toon('#5b6470'), dk = toon('#2b2f36');
    B(7, 3.4, 3, loco, 0, 2.4, 0, g); B(2.6, 1.4, 2.8, toon('#e8e2d4'), -1.8, 4.8, 0, g); Cy(0.4, 0.5, 1.6, dk, 2.4, 4.6, 0, g, 12);
    for (const x of [-8.2, -15.6]) B(7, 3.0, 3, car, x, 2.2, 0, g);
    B(24, 0.3, 3.6, toon('#6e6a62'), -7.5, 0.4, 0, g); for (let i = 0; i < 9; i++) for (const z of [-1.3, 1.3]) { const w = Cy(0.55, 0.55, 0.3, dk, 2.5 - i * 2.4, 0.75, z, g, 14); w.rotation.x = Math.PI / 2; } return g; },
  async pipeline() { const g = new THREE.Group(), st = toon('#9aa3ab'), dk = toon('#5b6470');
    const p = Cy(1.1, 1.1, 22, st, 0, 2.6, 0, g, 24); p.rotation.z = Math.PI / 2;
    for (const x of [-9, -3, 3, 9]) { B(0.5, 1.6, 2.4, dk, x, 0.8, 0, g); const r = new THREE.Mesh(new THREE.TorusGeometry(1.15, 0.14, 8, 24), dk); r.rotation.y = Math.PI / 2; r.position.set(x, 2.6, 0); g.add(r); } return g; },
};
export const OWN_NEEDS = new Set(['furnace', 'factory', 'house', 'town']);
let R = null, own = null;
window.renderIcon = async (name, px = 640) => {
  if (!R) { R = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); R.setPixelRatio(1); R.outputColorSpace = THREE.SRGBColorSpace; }
  if (OWN_NEEDS.has(name) && !own) own = await OWN();
  R.setSize(px, px); R.setClearColor(0x000000, 0);
  const scene = new THREE.Scene(), obj = await OBJECTS[name](own); scene.add(obj);
  scene.add(new THREE.AmbientLight('#ffffff', 0.9)); const k = new THREE.DirectionalLight('#fff6ea', 2.2); k.position.set(-6, 10, 7); scene.add(k); const f = new THREE.DirectionalLight('#cfe0ff', 0.5); f.position.set(8, 3, -4); scene.add(f);
  const box = new THREE.Box3().setFromObject(obj), c = box.getCenter(new THREE.Vector3()), sz = box.getSize(new THREE.Vector3()), r = sz.length() / 2;
  const az = 35 * Math.PI / 180, el = 26 * Math.PI / 180, cam = new THREE.PerspectiveCamera(22, 1, 0.1, 1000), d = r / Math.sin(11 * Math.PI / 180) * 1.02;
  cam.position.set(c.x + d * Math.cos(el) * Math.sin(az), c.y + d * Math.sin(el), c.z + d * Math.cos(el) * Math.cos(az)); cam.lookAt(c);
  R.render(scene, cam);
  // cắt sát theo alpha rồi áp phong cách chung
  const src = R.domElement, tmp = document.createElement('canvas'); tmp.width = px; tmp.height = px; const tg = tmp.getContext('2d'); tg.drawImage(src, 0, 0);
  const D = tg.getImageData(0, 0, px, px).data; let x0 = px, y0 = px, x1 = 0, y1 = 0; for (let y = 0; y < px; y++) for (let x = 0; x < px; x++) if (D[(y * px + x) * 4 + 3] > 8) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  const cw = x1 - x0 + 1, ch = y1 - y0 + 1, crop = document.createElement('canvas'); crop.width = cw; crop.height = ch; crop.getContext('2d').drawImage(tmp, x0, y0, cw, ch, 0, 0, cw, ch);
  return window.STK.style(crop).toDataURL('image/png');
};
window.renderChar = (spec, px = 480) => window.STK.style(window.STK.char(spec, px)).toDataURL('image/png');
window.READY = true;

// KÊNH 2 · module B — SỐ LIỆU 2.5D/3D (k2v/chart3d), thay thẻ phẳng trên nền mờ (BAI-HOC-K2 K6, K7).
// Biểu đồ đứng trong một phòng studio thật (sàn bóng, tường cong, đèn chính/viền) — nền KHÔNG mờ; mọi chữ (số, năm, ACTUAL/PROJECTION, nguồn)
// do lớp 2D (scripts/k2/lib/k2.js: p.tags, p.src, kindTag) vẽ tại điểm neo → cỡ ≥ 30 px và tương phản đo được (Q5/Q6).
// Tỷ lệ THẬT: chiều cao = v × scale (một đơn vị cảnh = 1/scale đơn vị số), không trục cắt; rãnh khối mỗi `block` đơn vị để đếm được.
//
// Cảnh và API (opt; thời điểm = giây trong cảnh, prep.py đổi "@từ" thành giây):
//   chart3d/stack  — cột xếp chồng so sánh các mốc: groups: [{id:'1950', x, segs:[{id:'us', v:87.8, color}], grow:[t0,t1]}], scale, block, w
//                    neo: '<g>:top', '<g>:<seg>' (giữa mép phải đoạn), '<g>:base'
//   chart3d/bars   — cột đùn: bars: [{id, x, v, color, kind:'actual'|'projection', grow}], scale, w  (projection: kính hổ phách + khung nét đứt)
//                    neo: '<id>:top', '<id>:base'
//   chart3d/line   — đường có chiều sâu: pts: [[x, v, kind]], draw:[t0,t1], scale, xk (đơn vị cảnh / 1 đơn vị x), color; dải băng dày + màn dưới đường
//                    neo: 'pt:<i>' (đỉnh mỗi điểm), 'end'
//   chung: ruler: [0, 500, 1000, …] vạch thước dọc ở tường sau (neo 'tick:<v>'), cam: [{u|t, p, l, mm}], env: 'studio', grade, exposure
import { THREE, C, cl, lerp, eo, ease, win, camRig, canvasTex, studio } from './common.js';

// Môi trường phản chiếu (PMREM từ một phòng hộp đèn tự dựng — không cần addon jsm)
function envMap(renderer) {
  const s = new THREE.Scene(), box = new THREE.Mesh(new THREE.BoxGeometry(40, 20, 40), new THREE.MeshBasicMaterial({ color: '#141b26', side: THREE.BackSide })); s.add(box);
  const panel = (w, h, x, y, z, ry, c, k) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), side: THREE.DoubleSide })); m.position.set(x, y, z); m.rotation.y = ry; s.add(m); };
  panel(14, 6, -12, 6, 10, Math.PI * 0.75, '#fff2e0', 6); panel(10, 14, 16, 4, -8, -Math.PI / 2, '#a9c4ff', 2.5); panel(30, 2, 0, 9.5, 0, 0, '#ffffff', 1.2);
  const top = new THREE.Mesh(new THREE.PlaneGeometry(18, 18), new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffffff').multiplyScalar(3) })); top.rotation.x = Math.PI / 2; top.position.y = 9.9; s.add(top);
  const pm = new THREE.PMREMGenerator(renderer); const rt = pm.fromScene(s, 0.04); pm.dispose(); return rt.texture;
}
const roundRect = (w, d, r) => { const s = new THREE.Shape(), x = -w / 2, y = -d / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + d - r); s.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
  s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s; };
// thân cột cao 1 (đáy y=0), cạnh đứng bo tròn — co giãn theo y không méo; nắp vát cố định độ dày
function prism(w, d, r) { const g = new THREE.ExtrudeGeometry(roundRect(w, d, r), { depth: 1, bevelEnabled: false, curveSegments: 6 }); g.rotateX(-Math.PI / 2); return g; }
function capGeo(w, d, r, t) { const g = new THREE.ExtrudeGeometry(roundRect(w - 2 * t, d - 2 * t, Math.max(0.01, r - t)), { depth: 0.001, bevelEnabled: true, bevelThickness: t, bevelSize: t, bevelSegments: 4, curveSegments: 6 });
  g.rotateX(-Math.PI / 2); return g; }
const MAT = (color, o = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.32, metalness: 0.15, clearcoat: 0.7, clearcoatRoughness: 0.25, envMapIntensity: 1.0, ...o });
const STEEL = (o = {}) => new THREE.MeshPhysicalMaterial({ color: '#cfd8e2', roughness: 0.3, metalness: 0.72, clearcoat: 0.4, clearcoatRoughness: 0.2, envMapIntensity: 1.6, ...o });
const matFor = (c) => (!c || c === 'steel' ? STEEL() : MAT(c));

// một cột: thân (co giãn) + nắp vát + rãnh khối; set(h) đặt chiều cao hiện tại
let AO = null;   // bóng tiếp xúc mềm dưới chân cột (đèn chính chiếu từ trước-trái nên bóng đổ khuất sau cột; thiếu AO thì khối như lơ lửng)
function contact(parent, x, z, w, d) { AO = AO || canvasTex(256, 256, (g, W2, H2) => { const gr = g.createRadialGradient(W2 / 2, H2 / 2, 0, W2 / 2, H2 / 2, W2 / 2); gr.addColorStop(0, 'rgba(0,0,0,0.85)'); gr.addColorStop(0.45, 'rgba(0,0,0,0.5)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, W2, H2); }, { srgb: false });
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w * 1.9, d * 1.9), new THREE.MeshBasicMaterial({ map: AO, transparent: true, depthWrite: false, color: '#000000', opacity: 0.9 })); m.rotation.x = -Math.PI / 2; m.position.set(x, 0.004, z); parent.add(m); return m; }
function column(parent, { x = 0, z = 0, w = 2.2, d = 2.2, r = 0.18, mat, y0 = 0, block = 0, scale = 1, glass = false, ao = true }) {
  const g = new THREE.Group(); g.position.set(x, y0, z); parent.add(g); const sh = ao && y0 === 0 ? contact(parent, x, z, w, d) : null;
  const body = new THREE.Mesh(prism(w, d, r), mat); body.castShadow = body.receiveShadow = true; g.add(body);
  const capT = Math.min(0.06, w * 0.03), cap = new THREE.Mesh(capGeo(w, d, r, capT), mat); cap.castShadow = true; g.add(cap);
  const seams = []; const gm = new THREE.MeshStandardMaterial({ color: '#0a0f16', roughness: 0.9 });
  if (block > 0) for (let i = 1; i < 400; i++) { const s = new THREE.Mesh(prism(w * 1.004, d * 1.004, r), gm); s.scale.y = 0.018; s.userData.y = i * block * scale; s.visible = false; g.add(s); seams.push(s); }
  let edge = null; if (glass) { edge = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(w, 1, d)), new THREE.LineDashedMaterial({ color: C.amber, dashSize: 0.18, gapSize: 0.12 })); edge.computeLineDistances(); g.add(edge); }
  const set = (h) => { h = Math.max(0.0005, h); body.scale.y = Math.max(0.0005, h - capT); cap.position.y = body.scale.y; g.visible = h > 0.002; if (sh) sh.visible = g.visible || g.position.y > 0.001;
    for (const s of seams) { s.visible = s.userData.y < h - capT * 1.5 && s.userData.y > 0.02; s.position.y = s.userData.y - 0.009; }
    if (edge) { edge.scale.y = h; edge.position.y = h / 2; } };
  set(0); return { g, set, body, cap, w, d };
}

// khung bao của biểu đồ (x0, x1, cao nhất) để đặt preset máy quay
function extent(o) { const sc = o.scale || 0.01; let xs = [], top = 0;
  for (const G of o.groups || []) { xs.push(G.x); top = Math.max(top, G.segs.reduce((a, s) => a + s.v, 0) * sc); }
  for (const b of o.bars || []) { xs.push(b.x); top = Math.max(top, b.v * sc); }
  for (const q of o.pts || []) { top = Math.max(top, q[1] * sc); } if (o.pts) xs.push(o.xoff ?? -8, (o.xoff ?? -8) + (o.pts[o.pts.length - 1][0] - o.pts[0][0]) * (o.xk || 0.25));
  const x0 = Math.min(...xs), x1 = Math.max(...xs); return { x0, x1, cx: (x0 + x1) / 2, w: x1 - x0 + 4, top: Math.max(top, 2) }; }
// Thư viện góc máy biểu đồ (camera_id = tên preset; scripts/k2/cams.yaml)
export const CHART_PRESETS = {
  'front-dolly': (e) => { const d = Math.max(e.w, e.top) * 1.5 + 6; return [{ u: 0, p: [e.cx - 2, e.top * 0.45 + 1, d * 1.08], l: [e.cx, e.top * 0.42, 0], mm: 35 }, { u: 1, p: [e.cx + 1, e.top * 0.5 + 1, d], l: [e.cx, e.top * 0.45, 0], mm: 35 }]; },
  'crane-up': (e) => [{ u: 0, p: [e.x0 - 3, 2.4, 9], l: [e.x0 + 2, 1.2, 0], mm: 32 }, { u: 0.3, p: [e.x0 - 1, 2.8, 10], l: [e.cx, 1.4, 0], mm: 32 }, { u: 1, p: [e.cx - 10, e.top * 0.62, e.top * 1.6 + 2], l: [e.cx, e.top * 0.48, 0], mm: 30 }],
  'low-hero': (e) => [{ u: 0, p: [e.cx - e.w * 0.5, 0.8, e.top * 0.7 + 6], l: [e.cx, e.top * 0.55, 0], mm: 24 }, { u: 1, p: [e.cx - e.w * 0.3, 0.9, e.top * 0.65 + 6], l: [e.cx, e.top * 0.58, 0], mm: 24 }],
  'orbit-l': (e) => { const r = Math.max(e.w, e.top) * 1.4 + 6; return [{ u: 0, p: [e.cx - r * 0.75, e.top * 0.6, r * 0.66], l: [e.cx, e.top * 0.42, 0], mm: 32 }, { u: 1, p: [e.cx - r * 0.35, e.top * 0.62, r * 0.94], l: [e.cx, e.top * 0.42, 0], mm: 32 }]; },
  'orbit-r': (e) => { const r = Math.max(e.w, e.top) * 1.4 + 6; return [{ u: 0, p: [e.cx + r * 0.75, e.top * 0.6, r * 0.66], l: [e.cx, e.top * 0.42, 0], mm: 32 }, { u: 1, p: [e.cx + r * 0.35, e.top * 0.62, r * 0.94], l: [e.cx, e.top * 0.42, 0], mm: 32 }]; },
  'top-down': (e) => [{ u: 0, p: [e.cx, e.top + 16, 10], l: [e.cx, e.top * 0.3, 0], mm: 30 }, { u: 1, p: [e.cx + 2, e.top + 14, 9], l: [e.cx, e.top * 0.32, 0], mm: 30 }],
  'side-track': (e) => [{ u: 0, p: [e.x0 - 4, e.top * 0.35 + 1, e.top * 0.9 + 7], l: [e.x0, e.top * 0.3, 0], mm: 40 }, { u: 1, p: [e.x1 + 4, e.top * 0.45 + 1, e.top * 0.9 + 7], l: [e.x1, e.top * 0.4, 0], mm: 40 }],
};
function base(o, ctx) {
  const scene = new THREE.Scene(); const env = envMap(ctx.renderer); scene.environment = env;
  const st = studio(scene, { size: o.room || 160, key: o.key || [-16, 26, 30] });
  const anchors = {};
  // thước dọc ở tường sau: vạch mảnh + điểm neo cho số (lớp 2D vẽ số)
  const sc = o.scale || 0.01, rz = o.rulerZ ?? -6, rx = o.rulerX ?? -9;
  for (const v of o.ruler || []) { const y = v * sc; const ln = new THREE.Mesh(new THREE.BoxGeometry(o.rulerW || 26, 0.04, 0.04), new THREE.MeshBasicMaterial({ color: "#8796a8", transparent: true, opacity: 0.6, fog: false }));
    ln.position.set(rx + (o.rulerW || 26) / 2 - 1, y, rz); scene.add(ln); anchors['tick:' + v] = new THREE.Vector3(rx - 0.4, y, rz); }
  const keys = o.cam || (o.preset && CHART_PRESETS[o.preset] ? CHART_PRESETS[o.preset](extent(o)) : null) || [{ u: 0, p: [0, 6, 22], l: [0, 3, 0], mm: 35 }, { u: 1, p: [3, 7, 21], l: [0, 3, 0], mm: 35 }];
  const { cam, at } = camRig(ctx.W, ctx.H, keys, ctx.dur);
  return { scene, cam, at, anchors, st };
}

export const HEROES = {
  async stack(ctx) {
    const o = ctx.opt; const B = base(o, ctx), sc = o.scale || 0.01, cols = [];
    for (const G of o.groups || []) { let y = 0; const segs = [];
      for (const S of G.segs) { const c = column(B.scene, { x: G.x, z: G.z || 0, w: o.w || 2.4, d: o.d || 2.4, mat: matFor(S.color), y0: 0, block: o.block || 0, scale: sc, ao: !segs.length });
        segs.push({ S, c, y0: y, y1: y + S.v * sc }); y += S.v * sc; }
      cols.push({ G, segs, h: y });
      B.anchors[G.id + ':top'] = () => new THREE.Vector3(G.x, cols.find((q) => q.G === G).cur || 0.001, G.z || 0);
      B.anchors[G.id + ':base'] = new THREE.Vector3(G.x, 0, (G.z || 0) + (o.d || 2.4) / 2);
      B.anchors[G.id + ':baseL'] = new THREE.Vector3(G.x - (o.w || 2.4) / 2, 0.35, (G.z || 0) + (o.d || 2.4) / 2); B.anchors[G.id + ':baseR'] = new THREE.Vector3(G.x + (o.w || 2.4) / 2, 0.35, (G.z || 0) + (o.d || 2.4) / 2);
      for (const s of segs) B.anchors[G.id + ':' + s.S.id] = () => { const cur = cols.find((q) => q.G === G).cur || 0; const top = Math.min(cur, s.y1); return top <= s.y0 ? null : new THREE.Vector3(G.x + (o.w || 2.4) / 2, (s.y0 + top) / 2, G.z || 0); }; }
    return { scene: B.scene, cam: B.cam, grade: o.grade || 'info', exposure: o.exposure || 1.1, anchors: B.anchors,
      update(t) { B.at(t);
        for (const col of cols) { const u = eo(win(col.G.grow, t, 1.5)), cur = u * col.h; col.cur = cur;
          for (const s of col.segs) { const h = cl((cur - s.y0) / Math.max(1e-6, s.y1 - s.y0)) * (s.y1 - s.y0); s.c.g.position.y = s.y0; s.c.set(h); } } } };
  },
  async bars(ctx) {
    const o = ctx.opt; const B = base(o, ctx), sc = o.scale || 0.01, bars = [];
    for (const b of o.bars || []) { const pj = b.kind === 'projection';
      const m = pj ? new THREE.MeshPhysicalMaterial({ color: C.amber, roughness: 0.15, metalness: 0, transmission: 0.0, transparent: true, opacity: 0.38, clearcoat: 1 }) : matFor(b.color);
      const c = column(B.scene, { x: b.x, z: b.z || 0, w: o.w || 2.0, d: o.d || 2.0, mat: m, glass: pj, block: o.block || 0, scale: sc }); bars.push({ b, c, h: b.v * sc });
      B.anchors[b.id + ':top'] = () => new THREE.Vector3(b.x, Math.max(0.001, bars.find((q) => q.b === b).cur || 0) + 0.15, b.z || 0); B.anchors[b.id + ':base'] = new THREE.Vector3(b.x, 0, (b.z || 0) + (o.d || 2) / 2); }
    return { scene: B.scene, cam: B.cam, grade: o.grade || 'info', exposure: o.exposure || 1.1, anchors: B.anchors,
      update(t) { B.at(t); for (const q of bars) { q.cur = eo(win(q.b.grow, t, 1.2)) * q.h; q.c.set(q.cur); } } };
  },
  async line(ctx) {
    const o = ctx.opt; const B = base(o, ctx), sc = o.scale || 0.01, xk = o.xk || 0.25, x0 = o.x0 ?? (o.pts[0][0]), off = o.xoff ?? -8, th = o.th || 0.22, dep = o.depth || 1.4;
    const P = o.pts.map(([x, v]) => new THREE.Vector3(off + (x - x0) * xk, v * sc, 0));
    const pj = o.pts.findIndex((q) => q[2] === 'projection');   // từ điểm này: PROJECTION (hổ phách, kính, viền nét đứt ở lớp 2D)
    // dải băng dày (mặt cắt th × dep) + màn dưới đường; actual và projection là hai dải riêng
    const band = (pts, mat, cmat) => { const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal'), N = 60 * (pts.length - 1), pos = [], idx = [], cp = [], ci = [];
      const sh = [[-th / 2, -dep / 2], [th / 2, -dep / 2], [th / 2, dep / 2], [-th / 2, dep / 2]];
      for (let i = 0; i <= N; i++) { const q = curve.getPoint(i / N), tg = curve.getTangent(i / N), n = new THREE.Vector3(-tg.y, tg.x, 0).normalize();
        for (const [a, b] of sh) pos.push(q.x + n.x * a, q.y + n.y * a, b); cp.push(q.x, 0, 0, q.x, q.y, 0);
        if (i) { for (let k = 0; k < 4; k++) { const a0 = (i - 1) * 4 + k, a1 = (i - 1) * 4 + (k + 1) % 4; idx.push(a0, a0 + 4, a1, a1, a0 + 4, a1 + 4); } const c0 = (i - 1) * 2; ci.push(c0, c0 + 2, c0 + 1, c0 + 1, c0 + 2, c0 + 3); } }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
      const cg = new THREE.BufferGeometry(); cg.setAttribute('position', new THREE.Float32BufferAttribute(cp, 3)); cg.setIndex(ci); cg.computeVertexNormals();
      const m = new THREE.Mesh(g, mat); m.castShadow = true; const c = new THREE.Mesh(cg, cmat); B.scene.add(m, c); return { g, cg, N, n: pts.length - 1 }; };
    const col = o.color || C.orange, parts = [];
    const actual = pj > 0 ? P.slice(0, pj) : pj === 0 ? [] : P, proj = pj >= 0 ? P.slice(Math.max(0, pj - 1)) : [];
    if (actual.length > 1) parts.push(band(actual, MAT(col, { emissive: col, emissiveIntensity: 0.15 }), new THREE.MeshStandardMaterial({ color: col, transparent: true, opacity: 0.16, side: THREE.DoubleSide, depthWrite: false })));
    if (proj.length > 1) parts.push(band(proj, new THREE.MeshPhysicalMaterial({ color: C.amber, roughness: 0.15, transparent: true, opacity: 0.45, clearcoat: 1 }), new THREE.MeshStandardMaterial({ color: C.amber, transparent: true, opacity: 0.08, side: THREE.DoubleSide, depthWrite: false })));
    const dots = P.map((q, i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(th * 1.1, 24, 16), MAT(pj >= 0 && i >= pj ? C.amber : '#fff1e4')); m.position.copy(q); B.scene.add(m); B.anchors['pt:' + i] = q.clone().add(new THREE.Vector3(0, 0.35, 0)); return m; });
    B.anchors.end = P[P.length - 1].clone();
    const total = P.length - 1;
    return { scene: B.scene, cam: B.cam, grade: o.grade || 'info', exposure: o.exposure || 1.1, anchors: B.anchors,
      update(t) { B.at(t); const u = win(o.draw, t) * total; let done = 0;   // u: số đoạn đã vẽ (theo điểm)
        for (const q of parts) { const f = cl((u - done) / q.n), k = Math.floor(q.N * f); q.g.setDrawRange(0, k * 24); q.cg.setDrawRange(0, k * 6); done += q.n; }
        dots.forEach((d, i) => { d.visible = i <= u + 1e-3; }); } };
  },
};

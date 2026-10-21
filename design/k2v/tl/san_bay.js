// ANIMATIC-T3 (21/10/2026) · SÂN BAY trên eo đất cho cảnh tl/t3tl:
//  grassStrip — dải cỏ cắt 1934–36 (lời 3h "from 1934, a grass airstrip was built there"): dải sáng hơn nền dọc trục đường băng hiện nay, hiện dần theo năm.
//    Vị trí/bề rộng: ƯỚC TÍNH (bậc 5 — chưa có bản đồ 1934; coi trục trùng đường băng hiện nay); năm: lời khoá.
//  aircraft — máy bay đậu dọc đường băng đêm 7/11/1942 (lời 4i "at least six hundred and fifty aircraft lined the runway", Gibraltar official record):
//    SỐ: bậc 2 (lời khoá); kiểu/bố trí: khối hình máy bay một động cơ/hai động cơ MINH HOẠ (bậc 5) — chờ mô hình có nguồn (D3 G1b). Không cờ, không số hiệu.
import { THREE, rng } from './core.js';
import { win } from './tl7.js';

function along(pts, e0, e1) {   // đoạn polyline đường băng (E tăng dần) cắt trong [e0, e1]
  const P = pts.slice().sort((a, b) => a[0] - b[0]).filter((p) => p[0] >= e0 && p[0] <= e1); return P.length >= 2 ? P : pts;
}

export function grassStrip(ctx, runway, o) {
  const hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3), P = along(runway, o.e0 ?? -650, o.e1 ?? 520), W = o.width ?? 46, pos = [], idx = [];
  for (let i = 0; i < P.length; i++) { const a = P[Math.max(0, i - 1)], b = P[Math.min(P.length - 1, i + 1)], dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1, nx = -dn / l * W / 2, nn = dx / l * W / 2;
    for (const s of [-1, 1]) { const e = P[i][0] + nx * s, n = P[i][1] + nn * s; pos.push(e, hAt(e, n) + 0.25, -n); } }
  for (let i = 0; i < P.length - 1; i++) { const k = i * 2; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ color: o.color || '#a9b874', transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
  ctx.maskify(m, ctx.U, 1); const mesh = new THREE.Mesh(g, m); mesh.receiveShadow = true; mesh.renderOrder = 2;
  return { group: mesh, update(Y) { const k = win(Y, o.w); m.opacity = 0.75 * k; mesh.visible = k > 0.01; },
    log: { lop: 'dai_co_1934', nguon: 'lời khoá 3h (1934 grass airstrip)', bac: 'năm: lời khoá; vị trí/bề rộng: ước tính trên trục đường băng hiện nay (bậc 5)' } };
}

export function aircraft(ctx, runway, o) {
  const R = rng(o.seed || 1942), hAt = (e, n) => Math.max(ctx.terr.hAt(e, n), 0.3), P = along(runway, o.e0 ?? -900, o.e1 ?? 700), n = o.n || 650;
  // khối máy bay: thân + cánh + đuôi ngang + đuôi đứng (≈ 16 × 20 m — cỡ máy bay ném bom hạng nhẹ / vận tải 1942), một hình học gộp
  const parts = [[0, 1.6, 0, 16, 1.8, 1.9], [0.8, 1.9, 0, 3.2, 0.35, 20], [-6.8, 2.2, 0, 2.0, 0.25, 6.5], [-7.2, 3.2, 0, 1.6, 2.2, 0.25]];
  const geos = parts.map(([x, y, z, a, b, c]) => new THREE.BoxGeometry(a, b, c).translate(x, y, z));
  const pos = [], nor = []; for (const gg of geos) { const q = gg.toNonIndexed(); pos.push(...q.attributes.position.array); nor.push(...q.attributes.normal.array); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  const m = new THREE.MeshLambertMaterial({ color: '#ffffff' }); ctx.maskify(m, ctx.U, 1);
  const im = new THREE.InstancedMesh(g, m, n); im.castShadow = im.receiveShadow = true; im.frustumCulled = false;
  const C = [0]; for (let i = 1; i < P.length; i++) C.push(C[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1])); const L = C[C.length - 1];
  const rows = o.rows || [-62, -40, 40, 62, -86, 86], per = Math.ceil(n / rows.length), Q = [], cc = new THREE.Color(), TONE = ['#5d6248', '#6b6e57', '#7d7f78', '#545a4c', '#8a8a84'];
  for (let r = 0; r < rows.length; r++) for (let k = 0; k < per && Q.length < n; k++) { const s = (k + 0.5) / per * L * 0.98 + (R() - 0.5) * 3; let i = 1; while (i < P.length - 1 && C[i] < s) i++;
    const a = P[i - 1], b = P[i], u = (s - C[i - 1]) / ((C[i] - C[i - 1]) || 1), dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1, off = rows[r] + (R() - 0.5) * 3;
    const e = a[0] + dx * u - dn / l * off, nn = a[1] + dn * u + dx / l * off; if (ctx.terr.hAt(e, nn) < 0.3) continue;
    Q.push({ e, n: nn, hd: Math.atan2(dn, dx) + (rows[r] > 0 ? -1 : 1) * (0.55 + (R() - 0.5) * 0.2), j: R(), c: TONE[Math.floor(R() * TONE.length)] }); }
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), Y = new THREE.Vector3(0, 1, 0), v = new THREE.Vector3(), sc = new THREE.Vector3();
  Q.forEach((p, i) => im.setColorAt(i, cc.set(p.c))); if (im.instanceColor) im.instanceColor.needsUpdate = true;
  return { group: im, n: Q.length, update(Yr) { const k = win(Yr, o.w); Q.forEach((p, i) => { const on = p.j < k, s = on ? 1 : 0; v.set(p.e, hAt(p.e, p.n), -p.n); q.setFromAxisAngle(Y, p.hd); sc.set(s, s, s); m4.compose(v, q, sc); im.setMatrixAt(i, m4); }); im.instanceMatrix.needsUpdate = true; },
    log: { lop: 'may_bay_1942', n: Q.length, nguon: 'lời khoá 4i (≥ 650 máy bay, Gibraltar official record, đêm 7/11/1942)', bac: 'số: bậc 2; kiểu/bố trí: khối minh hoạ bậc 5 (chờ mô hình có nguồn — D3 G1b)' } };
}

export function offsetLine(pts, d) {   // polyline lệch ngang d mét (dương = trái theo chiều đi)
  return pts.map((p, i) => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], dx = b[0] - a[0], dn = b[1] - a[1], l = Math.hypot(dx, dn) || 1; return [p[0] - dn / l * d, p[1] + dx / l * d]; });
}

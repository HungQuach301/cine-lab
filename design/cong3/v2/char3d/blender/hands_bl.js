// Cine Lab · Cổng 6 (W4, gói nhân vật) — BÀN TAY MPFB2 (CC0; RIGHTS W4-MPFB-A3) cho Ida và Cas, render bằng three.js.
// Dùng: await preloadHandsBL()  (một lần, TRƯỚC buildCharacter) rồi buildCharacter(sheet, { handsStyle: 'bl', … })
//       hoặc globalThis.CINE_HANDS_STYLE = 'bl'. Mặc định cast3d giữ tay cũ (HANDS_STYLE = 'v14').
// Lưới: blender/build_hands_bl.py → hands_bl.json (lưới đã chia 1 cấp, trọng số 16 xương: wrist + finger1…5 × 3, xương nghỉ).
// Gắn vào nhóm bàn tay của rig cast3d (ch.hands[s].hand, con của khớp wrist_*) → GIỮ khớp cổ tay, HAND_SCALE như cũ.
// Da CPU (LBS) — mọi pass (kể cả G-buffer lớp vẽ, mặt nạ C3) thấy đúng hình.
// Tư thế ngón: pose.hands[s] = { curl, spread, thumb_cross } như cũ (cùng ánh xạ góc 3 khớp của cast3d).
// NẮM CÓ VA CHẠM: lúc render (root.updateMatrixWorld của cảnh), mỗi ngón gập dần tới khi chạm vật gần tay
// (cột đèn, van, quai đèn lồng, sào, bậc thang — mọi lưới không thuộc thân nhân vật) → ngón ôm quanh vật, không xuyên.
// Khi curl ≥ 0,5 và có vật trong tầm lòng bàn tay → "nắm": ngón gập tới khi chạm (tối đa nắm kín); không có vật → theo curl.
import * as THREE from '../../../shared/node_modules/three/build/three.module.js';

export const HANDS_URL = new URL('./hands_bl.json', import.meta.url).href;
let CACHE = null;
export async function preloadHandsBL(url = HANDS_URL) {
  if (CACHE && CACHE.url === url) return CACHE;
  CACHE = { url, j: await (await fetch(url)).json() };
  return CACHE;
}
export const handsBLReady = () => !!CACHE;
const dec = (b, T) => { const s = atob(b), u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return new T(u.buffer); };
const PARENT = (n) => { const m = /^finger(\d)-(\d)$/.exec(n); return !m ? null : m[2] === '1' ? 'wrist' : `finger${m[1]}-${+m[2] - 1}`; };

// p = { ch, who, H, HS, skinHex, material(role, color, part, extra), parts }
export function buildHandsBL(p) {
  if (!CACHE) throw new Error("handsStyle 'bl': cần await preloadHandsBL() trước buildCharacter");
  const J = CACHE.j[p.who], sides = {};
  const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _v = new THREE.Vector3(), _one = new THREE.Vector3(1, 1, 1);
  for (const s of ['L', 'R']) {
    const D = J[s], sx = s === 'L' ? 1 : -1, n = D.n, B = D.bones, nb = B.length;
    const P0 = dec(D.pos, Float32Array), W = dec(D.w, Float32Array), idx = dec(D.idx, Uint32Array), cf = dec(D.col, Float32Array);
    const base = new THREE.Color(p.skinHex), col = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) { col[i * 3] = base.r * cf[i * 3]; col[i * 3 + 1] = base.g * cf[i * 3 + 1]; col[i * 3 + 2] = base.b * cf[i * 3 + 2]; }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(Float32Array.from(P0), 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    geo.setIndex(new THREE.BufferAttribute(idx, 1)); geo.computeVertexNormals();
    const hand = p.ch.hands[s].hand;
    const mesh = new THREE.Mesh(geo, p.material); mesh.userData.part = 'hand'; mesh.castShadow = true; mesh.receiveShadow = true; mesh.frustumCulled = false;
    hand.add(mesh); p.parts.push(mesh);
    // xương: hướng nghỉ = đơn vị; vị trí = đầu xương − đầu xương cha
    const head = B.map((_, b) => new THREE.Vector3(...D.heads[b])), tail = B.map((_, b) => new THREE.Vector3(...D.tails[b]));
    const par = B.map((nm) => { const q = PARENT(nm); return q ? B.indexOf(q) : -1; });
    const dir = B.map((_, b) => tail[b].clone().sub(head[b]).normalize());
    const palmN = new THREE.Vector3(...D.palmN);
    const flexAx = B.map((_, b) => new THREE.Vector3().crossVectors(dir[b], palmN).normalize());   // gập: hướng ngón quay về phía lòng tay
    // ngón cái: trục gập quay về phía giữa lòng bàn tay (đối ngón), không phải thẳng xuống pháp tuyến lòng tay
    const palmC = new THREE.Vector3(...D.palm);
    for (const nm of ['finger1-1', 'finger1-2', 'finger1-3']) { const b = B.indexOf(nm), tgt = palmC.clone().addScaledVector(palmN, 0.02).sub(head[b]).normalize(); const ax = new THREE.Vector3().crossVectors(dir[b], tgt); if (ax.lengthSq() > 1e-8) flexAx[b].copy(ax.normalize()); }
    const qb = B.map(() => new THREE.Quaternion());           // quay cục bộ hiện tại (hệ cha, nghỉ = đơn vị)
    const Mw = B.map(() => new THREE.Matrix4()), Mk = B.map(() => new THREE.Matrix4());
    const FING = [2, 3, 4, 5].map((f) => [1, 2, 3].map((k) => B.indexOf(`finger${f}-${k}`)));
    const THUMB = [1, 2, 3].map((k) => B.indexOf(`finger1-${k}`));
    sides[s] = { sx, n, P0, W, geo, mesh, hand, head, tail, par, dir, flexAx, palmN, palmC, qb, Mw, Mk, FING, THUMB, nb, rad: D.rad, B, ang: {}, key: '' };
  }
  const charMeshes = new Set(p.parts);

  // ---- tư thế theo curl/spread (cùng ánh xạ 3 khớp của cast3d) ----
  const targetOf = (hp, i) => { const c = hp.curl ?? 0.4; return [(0.05 + c * 0.95) * (1 + 0.08 * i), 0.12 + c * 1.25, 0.06 + c * 0.75]; };
  function setRot(S, b, flex, spread = 0, extraQ = null) {
    S.qb[b].setFromAxisAngle(S.flexAx[b], flex);
    if (spread) { _q.setFromAxisAngle(S.palmN, spread); S.qb[b].premultiply(_q); }
    if (extraQ) S.qb[b].premultiply(extraQ);
  }
  function fk(S) {   // ma trận thế giới (hệ bàn tay) + ma trận da từng xương
    for (let b = 0; b < S.nb; b++) {
      const pb = S.par[b], t = pb < 0 ? S.head[b] : _v.copy(S.head[b]).sub(S.head[pb]);
      _m.compose(t, S.qb[b], _one); if (pb < 0) S.Mw[b].copy(_m); else S.Mw[b].multiplyMatrices(S.Mw[pb], _m);
      S.Mk[b].copy(S.Mw[b]).multiply(_m.makeTranslation(-S.head[b].x, -S.head[b].y, -S.head[b].z));
    }
  }
  function skinApply(S) {
    fk(S); const pa = S.geo.attributes.position.array, P0 = S.P0, W = S.W, nb = S.nb, E = S.Mk.map((m) => m.elements);
    for (let i = 0; i < S.n; i++) {
      const x = P0[i * 3], y = P0[i * 3 + 1], z = P0[i * 3 + 2]; let X = 0, Y = 0, Z = 0;
      for (let b = 0; b < nb; b++) { const w = W[i * nb + b]; if (w < 1e-4) continue; const e = E[b];
        X += w * (e[0] * x + e[4] * y + e[8] * z + e[12]); Y += w * (e[1] * x + e[5] * y + e[9] * z + e[13]); Z += w * (e[2] * x + e[6] * y + e[10] * z + e[14]); }
      pa[i * 3] = X; pa[i * 3 + 1] = Y; pa[i * 3 + 2] = Z;
    }
    S.geo.attributes.position.needsUpdate = true; S.geo.computeVertexNormals();
  }
  let pose = {};
  function openLoop(S, hp) {
    for (let b = 0; b < S.nb; b++) S.qb[b].identity();
    const sp = hp.spread ?? 0.1;
    S.FING.forEach((ch, i) => { const a = targetOf(hp, i); ch.forEach((b, k) => setRot(S, b, a[k], k === 0 ? S.sx * (1.5 - i) * 0.22 * sp : 0)); });
    const c = hp.curl ?? 0.4;
    if (hp.thumb_cross) {   // ngón cái dựng theo +z của bàn tay (bóng chim)
      const b = S.THUMB[0]; _q.setFromUnitVectors(S.dir[b], new THREE.Vector3(0, -0.12, 1).normalize()); S.qb[b].copy(_q);
    } else { setRot(S, S.THUMB[0], 0.1 + c * 0.45); setRot(S, S.THUMB[1], 0.1 + c * 0.6); setRot(S, S.THUMB[2], 0.05 + c * 0.5); }
  }

  // ---- nắm có va chạm ----
  const ray = new THREE.Raycaster(); const cand = []; const _a = new THREE.Vector3(), _b = new THREE.Vector3(), _c = new THREE.Vector3(), _d = new THREE.Vector3(), _sph = new THREE.Sphere();
  function gather(scene, center, R) {
    cand.length = 0;
    scene.traverseVisible((o) => { if (!o.isMesh || charMeshes.has(o) || o.isSprite || !o.geometry) return;
      const g = o.geometry; if (!g.boundingSphere) g.computeBoundingSphere(); const nt = (g.index ? g.index.count : g.attributes.position.count) / 3; if (nt > 20000) return;
      const m = Array.isArray(o.material) ? o.material[0] : o.material; if (m && (m.transparent && m.opacity < 0.5)) return;
      _sph.copy(g.boundingSphere).applyMatrix4(o.matrixWorld); if (_sph.radius > 2.5) return;   // tường, nền, trời: không phải vật nắm
      if (_sph.center.distanceTo(center) < _sph.radius + R) cand.push(o); });
    return cand.length;
  }
  function hits(Mh, b, S) {   // đoạn xương b (hệ bàn tay → thế giới) có chạm vật? (tia dọc trục + tia về phía lòng tay ở giữa và đầu đoạn)
    const r = Math.max(0.004, S.rad[b] || 0.006);
    _a.setFromMatrixPosition(S.Mw[b]).applyMatrix4(Mh);
    _b.copy(S.tail[b]).applyMatrix4(S.Mk[b]).applyMatrix4(Mh);
    const L = _a.distanceTo(_b); if (L < 1e-5) return false;
    const sc = Mh.getMaxScaleOnAxis();
    // tia dọc trục (tới đầu đoạn + bán kính)
    _c.copy(_b).sub(_a).normalize(); ray.set(_a, _c); ray.far = L + r * sc * 0.8; ray.near = 0;
    if (ray.intersectObjects(cand, false).length) return true;
    // tia về phía lòng tay từ 2 điểm trên trục
    _d.copy(S.palmN).transformDirection(S.Mw[b]).transformDirection(Mh);
    for (const t of [0.45, 0.95]) { _c.copy(_a).lerp(_b, t); ray.set(_c, _d); ray.far = r * sc * 1.05; if (ray.intersectObjects(cand, false).length) return true; }
    return false;
  }
  function closeChain(S, Mh, chain, from, to, N = 28) {   // gập dần từ góc "from" tới "to"; đoạn chạm → khoá các khớp tới đoạn đó
    const a = from.slice(), frozen = chain.map(() => false), setA = () => chain.forEach((b, k) => { setRot(S, b, a[k], S.spr?.[b] ?? 0); });
    setA(); fk(S);
    for (let st = 0; st < N; st++) {
      const prev = a.slice(); let moved = false;
      chain.forEach((_, k) => { if (!frozen[k] && a[k] < to[k]) { a[k] = Math.min(to[k], a[k] + (to[k] - from[k]) / N); moved = true; } });
      if (!moved) break;
      setA(); fk(S);
      let hitK = -1; for (let k = 0; k < chain.length; k++) if (hits(Mh, chain[k], S)) { hitK = k; break; }
      if (hitK >= 0) { for (let k = 0; k <= hitK; k++) { a[k] = prev[k]; frozen[k] = true; } setA(); fk(S); }
      if (frozen.every((f) => f)) break;
    }
    return a;
  }
  function solveSide(s, scene) {
    const S = sides[s], hp = (pose.hands || {})[s] || { spread: 0.1, curl: 0.4 };
    S.hand.updateWorldMatrix(true, false); const Mh = S.hand.matrixWorld;
    const pc = _v.copy(S.palmC).applyMatrix4(Mh), reach = 0.07 * Mh.getMaxScaleOnAxis() + 0.05;
    const nC = scene ? gather(scene, pc, reach) : 0;
    const key = [hp.curl, hp.spread, hp.thumb_cross, ...Array.from(Mh.elements, (v) => v.toFixed(4)), ...cand.map((o) => o.id + ':' + o.matrixWorld.elements[12].toFixed(4) + ',' + o.matrixWorld.elements[13].toFixed(4) + ',' + o.matrixWorld.elements[14].toFixed(4))].join('|');
    if (key === S.key) return; S.key = key;
    let near = [9, ''];   // gỡ lỗi: vật gần tâm lòng bàn tay nhất (tia 26 hướng)
    if (nC) for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) for (let c = -1; c <= 1; c++) { if (!a && !b && !c) continue; ray.set(pc, _d.set(a, b, c).normalize()); ray.far = 1; ray.near = 0; const h = ray.intersectObjects(cand, false)[0]; if (h && h.distance < near[0]) near = [+h.distance.toFixed(3), (h.object.name || h.object.geometry.type) + '@' + h.point.toArray().map((v) => +v.toFixed(3)).join(',')]; }
    S.dbg = { near, nC, pc: pc.toArray().map((v) => +v.toFixed(3)), cand: cand.map((o) => (o.name || o.geometry.type) + '@' + new THREE.Vector3().setFromMatrixPosition(o.matrixWorld).toArray().map((v) => +v.toFixed(2)).join(',')).slice(0, 8) };
    openLoop(S, hp);
    S.grip = false;
    if (nC && !hp.thumb_cross) {
      const grasp = (hp.curl ?? 0.4) >= 0.5; S.grip = grasp; S.spr = {};
      const sp = hp.spread ?? 0.1;
      S.FING.forEach((ch, i) => { S.spr[ch[0]] = S.sx * (1.5 - i) * 0.22 * sp * (grasp ? 0.3 : 1);
        const tgt = grasp ? [1.45, 1.75, 1.2] : targetOf(hp, i); closeChain(S, Mh, ch, [0.02, 0.05, 0.02], tgt); });
      closeChain(S, Mh, S.THUMB, [0.1, 0.05, 0.02], grasp ? [0.9, 1.2, 0.9] : [0.1 + (hp.curl ?? 0.4) * 0.45, 0.1 + (hp.curl ?? 0.4) * 0.6, 0.05 + (hp.curl ?? 0.4) * 0.5]);
      S.spr = null;
    }
    skinApply(S); S.dbg.grip = S.grip;
  }
  function sceneOf(o) { while (o.parent) o = o.parent; return o.isScene ? o : null; }
  return {
    setPose(ps) { pose = ps || {}; for (const s of ['L', 'R']) sides[s].key = ''; },
    update(root) { const sc = sceneOf(root); for (const s of ['L', 'R']) solveSide(s, sc); },
    gripPoint(s, target = new THREE.Vector3()) { const S = sides[s]; S.hand.updateWorldMatrix(true, false); return target.copy(S.palmC).addScaledVector(S.palmN, 0.018).applyMatrix4(S.hand.matrixWorld); },
    sides,
  };
}

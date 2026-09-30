// Cine Lab · Cổng 5 LAYOUT — GÓI W1: cảnh 1–3 (s01 → hết cảnh 3). Chỉ W1 sửa file này.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { walkPose, WALK, WALK_CHILD } from '/cong3/shared/anim.js';
import { setWallPostOn, B1_FALLBACK } from './sets.js';
import { buildStreetSet, LAMP_X, LAMP_Z, WALK_Z, POST_X, CLOCK, ladderOf, buildWatch, lamMat, flickAt, GRADE_COLD } from './sets.js';
import { buildCitySet, buildWallSet, buildBaySet, buildAlleySet, buildRoomSet } from './sets2.js';
import { buildLantern } from '/cong3/shared/cast.js';
import { createFaceLight } from './facelight.js';   // W3: dội/viền cận mặt từ nguồn có thật
import { U } from '/cong3/v2/s5.js';
import { ease, easeIO, clamp01, fovOf, lerpPose, over, poseAt, valAt, camAt, makeChar, yawTo } from './util.js';
import { CLOCKS, CLOCK_ON, DIALOGUE, DING, FILM_S, FOOT_Z, GAS_ON, GRADE_ALLEY, GRADE_S5, L11_OFF, ON_Z, ORDER, P, PAINT_CLOSE, PAINT_STREET, PAINT_WALL, POST_ON, REACH_IDA, RELAY_1, S, S5_PAINT, S5_PAINT_MED, S6_PAINT, SHOTS, SQUARE_ON, SRC, T0, T1, VALVE, WALL_POST_ON, camMM, expo, faceCam, flameL11, gasLevel, hands, ladderAt, lanternLight, stdState, switchOn, watchInHand, whiteAt } from './common.js';

// Vị trí Cas ở cuối phố (s24, s24c): mặc định = bản Cổng 4; nếu sets_end.js (W2) trả endInfo.casSpot = [x, z] thì dùng vị trí đó
// (chân tường nhà kho, trong quầng hổ phách L11 — xem shots/layout/LAYOUT-W1.md, "Yêu cầu gửi W2").

// v3 (kiểm toán trạng thái ẩn): util.makeChar().place gọi setPose TRƯỚC khi đặt vị trí/hướng gốc → đèn lồng thắt lưng (xoay theo trọng lực
// bằng hướng thế giới của hông) dùng hướng gốc của LẦN ĐẶT TRƯỚC. Render thẳng một khung (hướng gốc còn = 0) khác render nối tiếp ở mọi shot
// Ida quay ≠ 0 (s02, s07, s08, s23). Sửa cục bộ: đặt vị trí + hướng gốc TRƯỚC rồi mới place → mỗi khung chỉ phụ thuộc chính nó.
// (Đề xuất P sửa gốc trong util.js cho mọi gói.)
function mkChar(...a) { const ch = makeChar(...a), place0 = ch.place;
  ch.place = (pose, x, z, yaw, y0 = 0) => { ch.root.position.set(x, y0 + (pose.root_y_m ?? 0), z); ch.root.rotation.y = yaw; ch.root.updateMatrixWorld(true); place0(pose, x, z, yaw, y0); };
  return ch; }
// ---- Cổng 6 · W1: ĐO TIẾP XÚC (chỉ khi --dbg '{"meas":1}'; không đổi hình). Khoảng cách tâm lòng tay MPFB (ch.gripPoint) → mặt vật gần nhất (m, âm = lún vào vật).
const W1V = new THREE.Vector3();
function sdBox(p, hx, hy, hz) { const qx = Math.abs(p.x) - hx, qy = Math.abs(p.y) - hy, qz = Math.abs(p.z) - hz; const o = Math.hypot(Math.max(qx, 0), Math.max(qy, 0), Math.max(qz, 0)); return o + Math.min(Math.max(qx, qy, qz), 0); }
function sdCylY(p, r, hy) { const dx = Math.hypot(p.x, p.z) - r, dy = Math.abs(p.y) - hy; return Math.min(Math.max(dx, dy), 0) + Math.hypot(Math.max(dx, 0), Math.max(dy, 0)); }
const visibleChain = (o) => { for (let q = o; q; q = q.parent) if (q.visible === false) return false; return true; };
function measContacts(scene, chs) {
  scene.updateMatrixWorld(true); const lads = [], valves = [], lampsG = []; let pole = null, watch = null;
  scene.traverse((o) => { if (o.name === 'ladder' && visibleChain(o)) lads.push(o); if (o.name === 'gas_lamp') lampsG.push(o); if (o.name === 'watch') watch = o; if (o.userData && o.userData.parts && o.userData.parts.valve) valves.push(o.userData.parts.valve); });
  const out = {};
  for (const [nm, ch] of Object.entries(chs)) { if (!ch || !ch.gripPoint) continue; if (ch.props && ch.props.pole && ch.props.pole.parent) pole = ch.props.pole;
    for (const s of ['L', 'R']) { const g = ch.gripPoint(s, new THREE.Vector3()); const r = {};
      let dl = 9, dr = 9; for (const l of lads) { const q = g.clone().applyMatrix4(l.matrixWorld.clone().invert()); const len = 1.8, w = 0.34;
        for (const x of [w / 2, -w / 2]) dl = Math.min(dl, sdBox(new THREE.Vector3(q.x - x, q.y - len / 2, q.z), w * 0.04, len / 2, w * 0.06));
        for (let i = 1; i <= 6; i++) { const y = len * i / 7; dr = Math.min(dr, sdCylY(new THREE.Vector3(q.y - y, q.x, q.z), w * 0.035, w / 2)); } }
      if (lads.length) { r.rail = +dl.toFixed(3); r.rung = +dr.toFixed(3); }
      let dv = 9; for (const v of valves) { const q = g.clone().applyMatrix4(v.matrixWorld.clone().invert()); dv = Math.min(dv, sdCylY(q, 0.028, 0.025)); } if (dv < 2) r.valve = +dv.toFixed(3);
      let dp = 9, db = 9, dg = 9; for (const lp of lampsG) { const c = lp.getWorldPosition(new THREE.Vector3()); if (g.y > 0.65 && g.y < 2.95) dp = Math.min(dp, Math.hypot(g.x - c.x, g.z - c.z) - 0.045);
        const q = g.clone().applyMatrix4(lp.matrixWorld.clone().invert()), aY = lp.userData.parts.armY, cY = lp.userData.height - 0.45; db = Math.min(db, sdBox(new THREE.Vector3(q.x, q.y - aY, q.z), 0.31, 0.0175, 0.0175)); dg = Math.min(dg, sdBox(new THREE.Vector3(q.x, q.y - (cY + 0.31), q.z), 0.145, 0.21, 0.145)); }
      if (dp < 2) r.post = +dp.toFixed(3); if (db < 2) r.bar = +db.toFixed(3); if (dg < 2) r.cage = +dg.toFixed(3);
      if (pole && s === 'R') { const q = g.clone().applyMatrix4(pole.matrixWorld.clone().invert()); r.poleAxis = +Math.hypot(q.x, q.z).toFixed(3); }
      if (watch && s === 'R') r.watch = +g.distanceTo(watch.getWorldPosition(W1V)).toFixed(3);
      if (ch.__wall) { const [px, pz, nx, nz] = ch.__wall; r.wall = +((g.x - px) * nx + (g.z - pz) * nz).toFixed(3); }
      r.p = g.toArray().map((x) => +x.toFixed(3)); out[nm + s] = r; } }
  return out;
}
// Bọc S: nếu dbg.meas thì in số đo tiếp xúc mỗi khung được cập nhật (render hoặc stepFrame). Không có cờ → trả nguyên shot (không đổi hình).
const S1 = (o) => S({ ...o, async build(ctx) { const r = await o.build(ctx); if (!(ctx.dbg && ctx.dbg.meas)) return r; const up = r.update; GRIPLOG.on = true;
  return { ...r, update(t, T, f) { GRIPLOG.rows = []; up.call(r, t, T, f); console.log(JSON.stringify({ meas: o.id, t: +t.toFixed(3), T: +T.toFixed(3), f, ...measContacts(r.scene, r.named || {}), grips: GRIPLOG.rows })); } }; } });
// =====================================================================================================================
// CỔNG 6 · W1 — DIỄN HOẠT cảnh 1–3 (AUTHORSHIP "Cổng 6 — diễn hoạt", MỞ W1 30/09/2026). Cách làm theo W2 (shots_w2.js, không sửa tệp đó):
// settle (đứng tự nhiên), gripAt (IK tay MPFB tới MỘT điểm), mặt 16 kênh + 6 viseme (setFace/VISEMES), mốc thoại đo trên tệp take.
// Mọi rãnh là hàm THUẦN theo t/T (đặt gốc trước setPose — mkChar).
// =====================================================================================================================
const wpos = (o) => o.getWorldPosition(new THREE.Vector3());
// ĐỨNG TỰ NHIÊN (= W2 settle): dồn trọng tâm sang một chân (chậu nghiêng 3°), chân kia chùng gối, thân bù nghiêng ngược, thở, dao động trọng tâm rất chậm.
function settle(pose, t, o = {}) {
  const s = o.side ?? 1, ph = o.ph ?? 0, k = (o.k ?? 1) * (1 + 0.15 * Math.sin(2 * Math.PI * t / 7 + ph)), b = Math.sin(2 * Math.PI * t / (o.br ?? 3.8) + ph);
  const J = pose.joints || {}, free = s > 0 ? 'R' : 'L', load = s > 0 ? 'L' : 'R';
  const add = { pelvis: [0, 0, 3 * s * k], spine: [(o.bx ?? 0.9) * b, 0, -2.4 * s * k], neck: [-0.4 * b, 0, 0.8 * s * k],
    ['hip_' + load]: [0, 0, -3 * s * k], ['hip_' + free]: [-5 * k, 0, -3 * s * k], ['knee_' + free]: [10 * k, 0, 0], ['ankle_' + free]: [-5 * k, 0, 0],
    shoulder_L: [0, 0, 0.8 * b], shoulder_R: [0, 0, -0.8 * b] };
  if (o.legs === false) for (const n of ['pelvis', 'hip_L', 'hip_R', 'knee_L', 'knee_R', 'ankle_L', 'ankle_R']) delete add[n];
  const joints = { ...J }; for (const [n, d] of Object.entries(add)) { const v = J[n] || [0, 0, 0]; joints[n] = [v[0] + d[0], v[1] + d[1], v[2] + d[2]]; }
  return { ...pose, joints };
}
const addJ = (pose, add) => { const joints = { ...(pose.joints || {}) }; for (const [n, d] of Object.entries(add)) { const v = joints[n] || [0, 0, 0]; joints[n] = [v[0] + d[0], v[1] + d[1], v[2] + d[2]]; } return { ...pose, joints }; };
// Thở trên thang (không đụng chân — chân khoá bậc): ngực/vai theo chu kỳ br.
const breathe = (pose, T, br = 3.6, a = 1) => { const b = Math.sin(2 * Math.PI * T / br); return addJ(pose, { spine: [0.8 * a * b, 0, 0], neck: [-0.35 * a * b, 0, 0], shoulder_L: [0, 0, 0.7 * a * b], shoulder_R: [0, 0, -0.7 * a * b] }); };
// NẮM TẠI MỘT ĐIỂM (= W2 gripAt, bản sao trong gói W1 — cast3d.reachGrip trượt dọc trục với vật ngắn; đề xuất Đ1 của W2 cho P). Trả khoảng cách tâm lòng tay → mặt vật (m).
function gripAt(ch, s, g) {
  const J = ch.joints, sh = J['shoulder_' + s], el = J['elbow_' + s], wr = J['wrist_' + s], sx = s === 'L' ? 1 : -1, root = ch.root, HS = ch.handScale ?? 1;
  const A = new THREE.Vector3(...g.axis).normalize(), C0 = new THREE.Vector3(...g.point);
  const wq = (o) => o.getWorldQuaternion(new THREE.Quaternion()), wp = (o) => o.getWorldPosition(new THREE.Vector3());
  root.updateMatrixWorld(true);
  const out = g.out ? new THREE.Vector3(...g.out) : wp(sh).sub(C0); out.addScaledVector(A, -out.dot(A)); if (out.lengthSq() < 1e-8) out.set(sx, 0, 0); out.normalize();
  const T = C0.clone().addScaledVector(out, g.radius - 0.002 * HS);
  const xw = out.clone().negate().multiplyScalar(-sx);
  for (let it = 0; it < 4; it++) {
    root.updateMatrixWorld(true);
    const S = wp(sh), E = wp(el);
    const zc = new THREE.Vector3(0, 0, 1).applyQuaternion(wq(wr)); const zw = g.zFix ? A.clone() : A.clone().multiplyScalar(zc.dot(A) >= 0 ? 1 : -1);   // W1: zFix = chiều trục cố định (quyết định ngón chỉ lên hay xuống khi áp phẳng)
    const yw = new THREE.Vector3().crossVectors(zw, xw).normalize(); zw.crossVectors(xw, yw).normalize();
    const Qd = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(xw, yw, zw));
    wr.quaternion.copy(wq(el).invert().multiply(Qd)); root.updateMatrixWorld(true);
    const G2 = ch.gripPoint(s), Wt = T.clone().sub(G2.clone().sub(wp(wr)));
    const a = E.distanceTo(S), b = wp(wr).distanceTo(E), d = Math.min(a + b - 1e-4, Math.max(Math.abs(a - b) + 1e-4, Wt.distanceTo(S)));
    const cur = Math.acos(Math.max(-1, Math.min(1, S.clone().sub(E).normalize().dot(wp(wr).sub(E).normalize())))), want = Math.acos(Math.max(-1, Math.min(1, (a * a + b * b - d * d) / (2 * a * b))));
    let ax = new THREE.Vector3().crossVectors(S.clone().sub(E), wp(wr).sub(E)); if (ax.lengthSq() < 1e-10) ax.set(1, 0, 0).applyQuaternion(wq(el)); ax.normalize();
    const qE = new THREE.Quaternion().setFromAxisAngle(ax, want - cur); el.quaternion.copy(wq(el.parent).invert().multiply(qE).multiply(wq(el)));
    wr.quaternion.copy(wq(el).invert().multiply(Qd)); root.updateMatrixWorld(true);
    const W2 = wp(wr), qS = new THREE.Quaternion().setFromUnitVectors(W2.clone().sub(S).normalize(), Wt.clone().sub(S).normalize());
    sh.quaternion.copy(wq(sh.parent).invert().multiply(qS).multiply(wq(sh))); root.updateMatrixWorld(true); wr.quaternion.copy(wq(el).invert().multiply(Qd));
  }
  root.updateMatrixWorld(true); ch.cpuSkin?.update(); if (ch.handsBL) { for (const k of ['L', 'R']) ch.handsBL.sides[k].key = ''; root.updateMatrixWorld(true); }
  return ch.gripPoint(s).distanceTo(C0) - g.radius;
}
// IK có trộn (k = 0 giữ FK, 1 = nắm hẳn; slerp vai–khuỷu–cổ tay) → vào/ra nắm mượt.
const GRIPLOG = { on: false, rows: [] };   // chỉ để ghi số đo (dbg.meas): khoảng cách tâm lòng tay → mặt vật TRƯỚC (tư thế FK) và SAU IK, theo nhãn đích
function gripK(ch, s, g, k = 1) {
  if (!g || k <= 0.001 || !ch.gripPoint) return null; const J = ['shoulder_', 'elbow_', 'wrist_'].map((n) => ch.joints[n + s]), q0 = J.map((j) => j.quaternion.clone());
  const pre = GRIPLOG.on ? ch.gripPoint(s, new THREE.Vector3()).distanceTo(new THREE.Vector3(...g.point)) - g.radius : 0;
  const e = gripAt(ch, s, g); if (GRIPLOG.on) GRIPLOG.rows.push({ who: (ch.who || '') + s, tag: g.tag || '?', k: +k.toFixed(2), pre: +pre.toFixed(4), post: +e.toFixed(4) }); if (k >= 0.999) return e;
  J.forEach((j, i) => { const q1 = j.quaternion.clone(); j.quaternion.copy(q0[i]).slerp(q1, k); }); ch.root.updateMatrixWorld(true); ch.cpuSkin?.update();
  if (ch.handsBL) { for (const x of ['L', 'R']) ch.handsBL.sides[x].key = ''; ch.root.updateMatrixWorld(true); } return e;
}
// Đích nắm trên cột đèn khí i (props.buildGasLamp): van đồng (trụ Ø0,056 trục ngang), thanh móc thang (hộp 0,035, trục dọc x cục bộ), thân cột (trụ đứng).
function lampGrips(st, i) {
  const l = st.lamps.find((q) => q && q.i === i); if (!l) return null; const g = l.lamp; g.updateMatrixWorld(true);
  const ud = g.userData, v = ud.parts.valve, P0 = wpos(g), X = new THREE.Vector3(1, 0, 0).transformDirection(g.matrixWorld), Y = new THREE.Vector3(0, 1, 0).transformDirection(g.matrixWorld);
  const vc = wpos(v), va = new THREE.Vector3(0, 1, 0).transformDirection(v.matrixWorld);
  return {
    // "van": nắm ỐNG KHÍ đứng (Ø 0,028) ngay dưới thân van 6 cm — lòng tay áp sát thân van (như W2 s36–s40: nắm ngang thân van thì ngón vướng ống, duỗi thẳng — thấy ở probe s22).
    valve: { point: vc.clone().addScaledVector(Y, -0.06).toArray(), axis: Y.toArray(), radius: 0.014, tag: 'van' }, valveBody: { point: vc.toArray(), axis: va.toArray(), radius: 0.028 },
    bar: (dx) => ({ point: P0.clone().addScaledVector(X, dx).addScaledVector(Y, ud.parts.armY).toArray(), axis: X.toArray(), radius: 0.02, tag: 'thanh móc' }),
    post: (y) => ({ point: P0.clone().addScaledVector(Y, y).toArray(), axis: Y.toArray(), radius: 0.0375 + 0.0175 * clamp01((ud.height - 0.45 - y) / (ud.height - 1.1)), tag: 'thân cột' }),
    X, Y, P0,
  };
}
// Ida trên thang ở cột i (mặt +z): khi NGHỈ tay phải nắm thanh móc thang bên phải cột, tay trái nắm thân cột (dưới vòng cổ); khi MỞ VAN tay phải nắm thân van.
// w = { R: k nắm nghỉ tay phải, V: k nắm van tay phải (chồng sau R), L: k nắm nghỉ tay trái }. Trả số đo (m) để ghi báo cáo.
function topHands(ida, G, w) {
  if (!G) return {}; const o = {}, dx = -0.2 * Math.sign(G.X.x || 1);
  if (w.L) o.L = gripK(ida, 'L', G.post(w.Ly ?? 2.4), w.L);
  if (w.LB) o.LB = gripK(ida, 'L', G.bar(-dx), w.LB);   // LB: tay trái nắm nhánh trái thanh móc (khi thân quay về +x — thân cột ngoài tầm với 3–4 cm); chồng sau L để chuyển mượt
  if (w.R) o.R = gripK(ida, 'R', w.Ry ? G.post(w.Ry) : G.bar(dx * (w.Rdx ?? 1)), w.R);
  if (w.V) o.V = gripK(ida, 'R', G.valve, w.V);
  return o;
}
// Trèo thang tựa (lad) ở cột i: hai tay nắm hai thanh dọc, so le theo nhịp bước; gần đỉnh (u > 0,55) chuyển dần sang nắm nghỉ trên cột (topHands).
// u = tiến độ trèo 0…1 (root_y = 1,55·ease(u)); top = { R/L/V } trọng số cuối khi lên hết.
function climbHands(ida, lad, G, u, top = { R: 1, L: 1 }) {
  const ry = 1.55 * ease(u), s = Math.sin(u * Math.PI * 5), kt = ease(clamp01((u - 0.55) / 0.35)), kr = 1 - kt;
  if (kr > 0.001) { const sL = Math.sign(G ? G.X.x || 1 : 1);
    gripK(ida, 'L', railG(lad, sL, Math.min(1.72, ry + 1.12 + 0.1 * s)), kr); gripK(ida, 'R', railG(lad, -sL, Math.min(1.72, ry + 1.12 - 0.1 * s)), kr); }
  if (kt > 0.001) topHands(ida, G, { R: (top.R ?? 0) * kt, L: (top.L ?? 0) * kt, V: (top.V ?? 0) * kt });
}
// Đích nắm trên thanh dọc thang (hộp 0,027 × 0,041 ≈ trụ bán kính 0,018): xs = +1 / −1 thanh; y = độ cao THẾ GIỚI (thang tựa) hoặc tham số dọc thanh 0…1,8 (at: 'len').
function railG(lad, xs, y, at = 'world') { lad.updateMatrixWorld(true); const up = new THREE.Vector3(0, 1, 0).transformDirection(lad.matrixWorld); const o = lad.localToWorld(new THREE.Vector3(xs * 0.17, 0, 0));
  const p = at === 'len' ? o.addScaledVector(up, y) : o.addScaledVector(up, (y - o.y) / up.y); return { point: p.toArray(), axis: up.toArray(), radius: 0.018, tag: 'thanh thang' }; }
// Tay phải giữ thang trên vai: chiếu tâm lòng tay hiện tại lên trục thanh gần nhất rồi nắm tại điểm đó (tay không trượt dọc thanh, chỉ khép vào thanh).
function shoulderLadderG(ch, s = 'R') { const lad = ch.props && ch.props.ladder; if (!lad || !lad.parent) return null; lad.updateMatrixWorld(true);
  const gp = ch.gripPoint(s, new THREE.Vector3()), q = lad.worldToLocal(gp.clone()), xs = q.x >= 0 ? 1 : -1; return { ...railG(lad, xs, Math.max(0.1, Math.min(1.7, q.y)), 'len'), tag: 'thang trên vai' }; }
// MẶT: trọng số 16 kênh theo khoá thời gian; khẩu hình 6 VISEMES; chớp; hướng nhìn = xoay nhãn cầu (= W2).
const mixW = (...ws) => { const o = {}; for (const w of ws) for (const [k, v] of Object.entries(w || {})) o[k] = (o[k] || 0) + v; return o; };
const wLerp = (a, b, u) => { const o = {}; for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) o[k] = (a[k] || 0) + ((b[k] || 0) - (a[k] || 0)) * u; return o; };
const wAt = (keys, t) => { if (t <= keys[0][0]) return keys[0][1]; for (let i = 0; i < keys.length - 1; i++) { const [ta, a] = keys[i], [tb, b] = keys[i + 1]; if (t <= tb) return wLerp(a, b, easeIO((t - ta) / (tb - ta))); } return keys[keys.length - 1][1]; };
function lipKeys(words, t0, lead = 0.04) {
  const K = []; let prevEnd = -9;
  for (const [a, b, seq] of words) {
    if (a - prevEnd > 0.25) { if (prevEnd > -9) K.push([t0 + prevEnd + 0.1 - lead, 'rest']); K.push([t0 + a - 0.07 - lead, 'rest']); }
    for (const [u, v] of seq) K.push([t0 + a + u * (b - a) - lead, v]);
    prevEnd = b;
  }
  K.push([t0 + prevEnd + 0.1 - lead, 'rest']); return K;
}
function mouthAt(K, T, V, amp = 0.8) {
  if (T <= K[0][0] || T >= K[K.length - 1][0]) return {};
  for (let i = 0; i < K.length - 1; i++) if (T < K[i + 1][0]) { const u = ease((T - K[i][0]) / (K[i + 1][0] - K[i][0])); const w = wLerp(V[K[i][1]] || {}, V[K[i + 1][1]] || {}, u); for (const k in w) w[k] *= amp; return w; }
  return {};
}
// Miệng nói có MÔI – MÁ – CẰM cùng động (= W2 v3 richLip): hàm trần 0,35, phần mở còn lại sang môi (pucker/wide), má (cheekRaise), cằm (chinRaise ở âm khép).
function richLip(ex, mo) {
  const j = mo.jawOpen || 0, sp = Math.min(1, j * 2.5), e = { ...ex };
  for (const k of ['frown', 'chinRaise', 'press']) if (e[k]) e[k] *= 1 - 0.6 * sp;
  const o = { ...mo, jawOpen: Math.min(j, 0.35) };
  o.cheekRaise = (o.cheekRaise || 0) + 0.25 * j; o.pucker = (o.pucker || 0) + 0.2 * j + 0.3 * (mo.pucker || 0); o.wide = (o.wide || 0) + 0.15 * j;
  o.lowerLipIn = (o.lowerLipIn || 0) + 0.12 * Math.max(0, j - 0.2); o.chinRaise = (o.chinRaise || 0) + 0.35 * (mo.press || 0) + 0.15 * (mo.lowerLipIn || 0);
  o.browInnerUp = (o.browInnerUp || 0) + 0.08 * j;
  return mixW(e, o);
}
const blinkAt = (T, list) => { let m = 0; for (const e of list) { const [b, s] = Array.isArray(e) ? e : [e, 1]; const d = (T - b) / s; m = Math.max(m, d < 0 ? 0 : d < 0.07 ? d / 0.07 : d < 0.1 ? 1 : d < 0.22 ? 1 - (d - 0.1) / 0.12 : 0); } return m; };
function faceRig(ch) {
  const eyes = ch.face?.eyes || [], g0 = eyes.map((e) => [e.rotation.x, e.rotation.y]); let last = '';
  return (w, gaze = [0, 0]) => {
    const o = {}; for (const [k, v] of Object.entries(w)) { const c = Math.max(0, Math.min(1, v)); if (c > 0.004) o[k] = +c.toFixed(3); }
    const key = JSON.stringify(o); if (key !== last) { ch.setFace(o); last = key; }
    eyes.forEach((e, i) => e.rotation.set(g0[i][0] + gaze[1], g0[i][1] + gaze[0], 0));
  };
}
// Mốc thoại đo trên tệp take đã duyệt (reports/m1/cong2/tableread-d2/lines/L1.mp3, L2.mp3): bao năng lượng 50 ms (> −38 dB so đỉnh) + onset librosa
// + faster-whisper small.en (mốc từ); mix.py đặt câu ở đầu shot (lệch 0,000 s) → giây phim = DIALOGUE.Lk + giây trong tệp.
// L1 "Evening, old street." (2,16 s): "Evening" 0,15–0,95 · "old" 1,00–1,30 · "street." 1,35–2,05.
// L2 "Not yet... not yet." (2,88 s): "Not" 0,15–0,35 · "yet..." 0,50–0,72 (hơi thở 0,85–0,95) · "not" 1,55–1,80 · "yet." 1,95–2,50 (bật "t" 2,75).
const LIP_L1 = [[0.15, 0.95, [[0, 'E'], [0.26, 'FV'], [0.4, 'E'], [0.62, 'L'], [0.78, 'E'], [0.93, 'L']]], [1.0, 1.3, [[0, 'O'], [0.55, 'O'], [0.85, 'L']]],
  [1.35, 2.05, [[0, 'E'], [0.2, 'L'], [0.32, 'O'], [0.5, 'E'], [0.8, 'E'], [0.95, 'L']]]];
const LIP_L2 = [[0.15, 0.35, [[0, 'L'], [0.35, 'A'], [0.9, 'L']]], [0.5, 0.72, [[0, 'E'], [0.5, 'E'], [0.92, 'L']]],
  [1.55, 1.8, [[0, 'L'], [0.35, 'A'], [0.9, 'L']]], [1.95, 2.5, [[0, 'E'], [0.45, 'E'], [0.9, 'L']]]];
// Cas DỰA TƯỜNG CHIM (s23, s24, s24c — action s24c "Cas đứng dựa tường vôi"): Cổng 5 để cậu cách tường 0,95 m, tay trong tay áo → tay không thể chạm tường
// (W4T2: lòng tay MPFB lệch 7,0 cm "tay không còn chạm tường"). Cổng 6: cậu đứng sát tường hơn (cách mặt tường CAS_LEAN.d m, cùng x với casSpot), mặt vẫn về L11/Ida,
// dồn trọng tâm sang chân phía tường, nghiêng người về tường; lòng tay phải MPFB ÁP lên mặt vôi (IK điểm, ngón hướng lên), tay trái vẫn trong tay áo.
// Thử (probe): tay áp tường ngang vai với tường bên phải cậu → đọc thành "vẫy tay chào" từ máy s24c → bỏ. Chốt: LƯNG tựa tường (mặt ra phố, thân quay về L11
// bodyYaw, cổ quay nốt), hai vai ngả nhẹ ra sau; lòng tay phải áp phẳng lên tường cạnh hông (ngón chúc xuống).
const CAS_LEAN = { d: 0.2, y: 0.56, side: 0.2, back: 4, bodyYaw: -25 };
function casLeanSpot(st) { const [cx, cz] = casSpotOf(st), fz = (st.endInfo && st.endInfo.flankZ) ?? -8.1, z = fz + CAS_LEAN.d;
  const yL = yawTo(cx, z, LAMP_X(11), ON_Z), body = CAS_LEAN.bodyYaw * Math.PI / 180;
  return { x: cx, z, wallZ: fz, spot0: [cx, cz], yaw: body, neckY: (yL - body) * 180 / Math.PI }; }
function casLeanPose(p, T, neck = [0, 0, 0]) {
  const b = settle(over(p.C.turnaround, { joints: { neck }, hands: { R: { spread: 0.3, curl: 0.1 } } }), T, { side: -1, k: 0.6, br: 3.0, ph: 1.3 });
  return addJ(b, { spine: [-CAS_LEAN.back, 0, 0] });
}
function casWallHand(cas, L, k = 1) {   // lòng tay phải áp phẳng lên tường cạnh hông phải, cao CAS_LEAN.y
  const r = wpos(cas.root), q = cas.root.getWorldQuaternion(new THREE.Quaternion()), rt = new THREE.Vector3(-1, 0, 0).applyQuaternion(q);
  const pt = [r.x + CAS_LEAN.side * rt.x, CAS_LEAN.y, L.wallZ]; cas.__wall = [pt[0], pt[2], 0, 1];
  const zx = -Math.sign(rt.x || -1);   // tay phải: trục cổ tay z = ± x thế giới sao cho ngón CHÚC XUỐNG (xw = −out, ngón = −y, z = x × y)
  return gripK(cas, 'R', { point: pt, axis: [zx, 0, 0], zFix: true, radius: 0.0, out: [0, 0, 1], tag: 'tường' }, k);
}
// B2 (chỉ đạo chủ dự án 30/09/2026, luật thế giới v0.6 — cột điện luôn ở mé đường ĐỐI DIỆN dãy đèn khí): cột điện tường chim (sets_end wallPost,
// thế giới (17,0; −5,9), CÙNG mé bắc với L11) KHÔNG xuất hiện trong khung s23. Chỉ ẩn trong shot (không sửa sets_end.js — dùng chung cảnh 4):
// thân cột + bóng đèn + quầng + loá (mọi vật ≤ 1,6 m quanh đầu đèn). PointLight của cột dời sang vỉa hè NAM, ngoài khung — cùng chỗ W2 dùng ở s27:
// (7,2; 6,2; 12,2) hệ tường chim = thế giới (17,4; 6,2; 4,1). Ở s23 (52,5–55,5 s) cột còn TẮT (bật 64,4 s) → không có ánh; mức sáng: Cổng 7.
const B2_LIGHT_W = [17.4, 6.2, 4.1];
function hideWallPost(st) {
  const wp = st.endInfo && st.endInfo.wallPost; if (!wp || !wp.group) return null; const Lp = wp.light;
  const hw = Lp ? Lp.getWorldPosition(new THREE.Vector3()) : null, hidden = [wp.group];
  if (hw) st.scene.traverse((o) => { if (o === Lp || !(o.isSprite || o.isMesh)) return; if (o.getWorldPosition(new THREE.Vector3()).distanceTo(hw) < 1.6) hidden.push(o); });
  for (const o of hidden) o.visible = false;
  if (Lp) { const pw = new THREE.Vector3(...B2_LIGHT_W); Lp.parent.updateMatrixWorld(true); Lp.parent.worldToLocal(pw); Lp.position.copy(pw); Lp.distance = 0; Lp.updateMatrixWorld(true); }
  return { hidden: hidden.length, post: [wp.x, wp.z], light: B2_LIGHT_W };
}
// Đồng hồ bỏ túi trong LÒNG tay phải MPFB (common.watchInHand đặt theo lòng tay sheet cũ ở cổ tay → lệch 7,9–9,2 cm với tay MPFB, đo trước khi sửa).
// Đồng hồ nằm trên tâm lòng tay, nhích 3 cm về phía máy (dày ngón + vỏ); máy insert đặt theo đồng hồ như cũ (cách đồng hồ giữ như bản Cổng 5).
function watchInPalm(scene) {
  const w = buildWatch(); scene.add(w);
  return (ch, cam, minDeg, hourDeg, dir = null, dist = 0.3) => { const p = ch.gripPoint('R', new THREE.Vector3());
    if (dir) { cam.position.copy(p).addScaledVector(dir.clone().normalize(), dist); cam.lookAt(p); }
    w.position.copy(p).addScaledVector(cam.position.clone().sub(p).normalize(), 0.03); w.lookAt(cam.position); w.userData.setHands(minDeg, hourDeg); };
}
// Đèn lồng thắt lưng (hông trái): điểm tay trái chạm cửa đèn (mồi lửa ở s04) — mặt trước đèn, ngang giữa kính.
function lanternDoorG(ch) { const lan = ch.props && ch.props.lantern; if (!lan || !lan.parent) return null; lan.updateMatrixWorld(true);
  const a = wpos(lan.userData.lightAnchor), q = ch.root.getWorldQuaternion(new THREE.Quaternion()), fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q);
  return { point: a.addScaledVector(fw, 0.06).toArray(), axis: [0, 1, 0], radius: 0.01, out: fw.toArray(), tag: 'cửa đèn lồng' }; }
const CAS_SPOT = [-1.2, -2.2];
const S22 = { yaw: 45, glint: 0.35, lip: 0.6, pan: 0 };   // Cổng 6: s22 3/4 — máy lệch 45° khỏi hướng mặt, phía phố (−40° bị thân cột che nửa mặt); ánh mắt dịu (glint 0,5 → 0,35); lẩm bẩm: biên độ khẩu hình 0,6
const S05_MODE = 'fl', S05_EK = 1.6;   // C2: facelight gas + phơi sáng fl.exposure() × 1,6 (mặt cháy 0,5 %, nền luma 69, tóc bạc) — LAYOUT-W1.md mục 13
// B1 (sau Cổng 5): chỗ Cas dời sang đông ~4 m. Nếu sets_end.js đã trả endInfo.wallPost (W2 làm B1) thì tin endInfo.casSpot; nếu chưa thì dùng số dự phòng của P.
const casSpotOf = (st) => { const e = st.endInfo; if (!e) return CAS_SPOT; return e.wallPost && e.casSpot ? e.casSpot : B1_FALLBACK.casSpot; };
// Đèn lồng thắt lưng TẮT từ s02 tới lúc mồi ở L4 (kịch bản 0:12; quyết định chủ dự án sau Cổng 5). Nhịp tay mồi làm ở Cổng 6; layout chỉ đổi trạng thái lửa.
function lanternLit(ch, on) {
  const lan = ch.props && ch.props.lantern; if (!lan) return;
  lan.traverse((o) => { if (!o.isMesh || !o.material || o.material.type !== 'MeshBasicMaterial') return;
    const m = o.material; if (!o.userData.col0) { o.userData.col0 = m.color.clone(); o.userData.op0 = m.opacity; }
    if (!m.transparent) { o.visible = on; return; }   // ngọn lửa: ẩn khi tắt
    if (on) { m.color.copy(o.userData.col0); m.opacity = o.userData.op0; } else { m.color.set('#141216'); m.opacity = 0.25; } });   // kính: tối, gần trong suốt
}

// Mặt nạ đo V3: mặt vôi nhà kho (ShapeGeometry có map, trong nhóm cuối phố, không phải vật liệu mặt tiền FT) → trắng; mọi thứ khác → đen (vẫn che khuất).
function limeMask(st) {
  const g = st.endInfo && st.endInfo.group; if (!g) return;
  const face = new Set(); g.traverse((o) => { if (o.isMesh && o.geometry.type === 'ShapeGeometry' && o.material && o.material.map && o.material.color && o.material.color.getHex() === 0xffffff && o.material.map.image && o.material.map.image.width) face.add(o); });
  const W = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }), B = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
  const fixed = new Set(); st.scene.traverse((o) => { if (o.isSprite || o.isPoints) o.visible = false; if (o.isMesh) fixed.add(o); });
  st.scene.fog = null; st.scene.background = new THREE.Color(0);
  for (const o of fixed) o.material = face.has(o) ? W : B;
  st.scene.userData.limeMask = { face: face.size, B, W };
  st.scene.userData.blackenLater = () => st.scene.traverse((o) => { if (o.isMesh && !fixed.has(o)) o.material = B; if (o.isSprite) o.visible = false; });
}

// v3 (kiểm giờ đồng hồ trên hình): móc CHỈ ĐỌC góc kim của vật thể đồng hồ trong cảnh (đồng hồ bỏ túi 'watch'; đồng hồ quảng trường).
// Không đổi hình. clockAudit(scene) → { watch: [phút°, giờ°] | null, square: [phút°, giờ°] | null } (độ theo chiều kim, 0 = 12 giờ).
function clockAudit(scene) {
  const out = { watch: null, square: null }; const deg = (m) => +(((-m.rotation.z * 180 / Math.PI) % 360 + 360) % 360).toFixed(3);
  scene.traverse((o) => {
    if (o.name === 'watch' && !out.watch) { const hs = o.children.filter((c) => c.isMesh && c.geometry.type === 'PlaneGeometry' && Math.abs(c.position.z - 0.0052) < 1e-6);
      if (hs.length >= 2) out.watch = [deg(hs[hs.length - 2]), deg(hs[hs.length - 1])]; }
    if (o.userData && o.userData.head && o.userData.setHands && !out.square) { const ps = o.userData.head.children.filter((c) => c.isGroup && c.children[0] && c.children[0].isMesh);
      if (ps.length >= 2) out.square = [deg(ps[0].children[0]), deg(ps[1].children[0])]; }
  });
  return out;
}
const exposeClock = (scene) => { if (typeof window !== 'undefined') window.__w1clock = () => clockAudit(scene); };
setWallPostOn(WALL_POST_ON);   // Q-W2-3: cột tường chim (bộ phố) bật đúng mốc 1:04 của common.js
// Máy s23 (V3, 0:52): cố định để W2 dựng cuối phố theo đúng khung này (28 mm: FOV dọc 46,4°, ngang 74,6°).
export const S23_CAM = { pos: [27.0, 1.5, 3.8], look: [4.5, 2.0, -1.5], mm: 28 };   // A2: lùi thêm 2,5 m — cuối phố W2 A2 (dãy bắc từ x = 18,5) lộ hông kho dài hơn: mặt vôi 22,5 % → 18,5 % (máy giai đoạn C: 15,5 % với hình cũ)

// ---------------- CẢNH 1 — Vòng đèn (0:00–0:25, 25 s) ----------------
S1({ id: 's01', scene: 1, t0: 0.0, t1: 4.0, size: 'EWS', angle: 'cao, chúc ~20°', mm: 28, move: 'dolly vào rất chậm',
  why: 'Mở phim đúng lựa chọn 1C: thành phố cuối chạng vạng, đèn khí hiện dần như những tâm hổ phách; đặt thế giới trước khi vào người.',
  sound: 'nhạc tạm (ACE-Step M0) vào nhẹ; room tone gió cao', light: 'trời chạng vạng hồng–tím; đèn khí các phố (chấm hổ phách)',
  action: 'Các chấm hổ phách xuất hiện từng cái một khắp thành phố.',
  async build(ctx) { const c = await buildCitySet(ctx, 'dusk'); return { ...c, exposure: 1.0, update: (t, T) => c.update(t, T) }; } });

S1({ id: 's02', scene: 1, t0: 4.0, t1: 8.5, size: 'WS', angle: 'ngang tầm mắt (1,5 m)', mm: 35, move: 'tĩnh',
  why: 'Đặt địa lý phố: đèn đã thắp ở phải (sau lưng Ida), phố chưa thắp phía trái — hướng đi phải→trái giữ suốt cảnh 1–3.',
  sound: 'room tone phố chạng vạng; bước chân; nhạc tạm', light: 'trời chạng vạng + đèn khí L1–L3',
  action: 'Ida vác thang đi từ phải sang trái về cột L4.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 85, x1: 200, shadowLamps: [3], fog: [30, 260] }); const p = P(ctx);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 });
    // W1: máy chéo lên phố (~23° về bắc so với trục phố): mặt tiền bắc lùi sâu bên trái, đèn L3–L1 đã thắp nối nhau về quảng trường,
    // mái + ống khói lớp sau và trời chạng vạng ở trên. Ida từ xa tiến về máy, trôi PHẢI → TRÁI trên khung (giữ hướng cảnh 1–3).
    const cam = camMM(35); cam.position.set(103.5, 1.45, 3.6); cam.lookAt(116.0, 2.6, -1.6);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(walkPose(t + 0.3, p.I.walk_ladder), 114.5 - WALK.speed_mps * t, WALK_Z, -Math.PI / 2); gripK(ida, 'R', shoulderLadderG(ida), 1); lanternLit(ida, false); } };   // Cổng 6: tay phải MPFB nắm thanh thang trên vai (trước: hở 15,6 cm)
  } });

S1({ id: 's03', scene: 1, t0: 8.5, t1: 10.5, size: 'MS', angle: 'thấp, hất lên', mm: 50, move: 'tĩnh',
  why: 'Góc thấp cho nghi thức: tay mở van, "phụp", hổ phách nở trên mặt bà.',
  sound: 'kẽo kẹt thang; tiếng xì khí; "phụp" (9,2 s)', light: 'đèn khí L4 vừa mồi (nguồn chính), trời chạng vạng',
  action: 'Ida lên nốt bậc thang, tay phải mở van; ngọn L4 bắt lửa.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 80, x1: 140, shadowLamps: [4] }); const p = P(ctx); const lad = ladderAt(st.scene, 4);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const G = lampGrips(st, 4);
    const cam = camMM(50); cam.position.set(103.2, 0.95, -0.2); cam.lookAt(106.0, 3.0, -4.3);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.0,
      update(t, T, f) { st.setState(stdState(T), f);
        const pose = t < 0.55 ? p.climb(0.55 + t / 1.2, p.restLadder) : poseAt([[0.55, p.restLadder], [0.75, p.valveLadder], [1.3, p.valveLadder], [1.9, p.warmLadder]], t);
        const u = clamp01(0.55 + t / 1.2); ida.place(breathe(pose, T, 3.0), LAMP_X(4), t < 0.55 ? FOOT_Z + (ON_Z - FOOT_Z) * ease(u) : ON_Z, 0); lanternLit(ida, false);
        // Cổng 6: trèo — hai tay nắm thanh thang; lên bậc cuối — phải nắm thanh móc, trái nắm thân cột; 0,55–0,75 tay phải sang van (IK), 1,3–1,9 buông lên kính.
        const off = 1 - ease(clamp01((t - 1.3) / 0.5));
        if (t < 0.55) climbHands(ida, lad, G, u); else topHands(ida, G, { R: off, L: off, V: ease(clamp01((t - 0.55) / 0.2)) * off }); } };
  } });

S1({ id: 's04', scene: 1, t0: 10.5, t1: 12.0, size: 'WS', angle: 'cao, từ bên kia phố', mm: 28, move: 'tĩnh',
  why: 'Cho thấy BÓNG của bà (bóng = dấu vết con người, luật thế giới mục 2): bóng dài, mềm trên mặt tiền và đá lát.',
  sound: 'room tone; lửa thở rất khẽ', light: 'đèn khí L4 (có bóng)',
  action: 'Ida trên thang, hai tay đưa lên kính; bóng người + thang đổ dài lên tường nhà.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 80, x1: 200, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const G = lampGrips(st, 4);
    const cam = camMM(28); cam.position.set(99.5, 5.2, 3.2); cam.lookAt(106.5, 1.2, -4.6);
    // Cổng 6 — nhịp mồi đèn lồng (shots_w1.json s04): 0,8 s hai tay lên kính; 0,85–1,1 tay trái hạ xuống cửa đèn lồng hông trái (IK), cúi nhìn; 1,2 đèn bắt lửa;
    // 1,2–1,45 tay trái về lại kính. Tay phải giữ thanh móc thang cho vững khi cúi (sào mồi không thấy — quy ước continuity: sào lần đầu thấy ở s21).
    const look = over(p.warmLadder, { joints: { neck: [26, -8, 0], spine: [8, 0, 0] } });
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.0,
      update(t, T, f) { st.setState(stdState(T), f);
        ida.place(breathe(poseAt([[0, p.valveLadder], [0.8, p.warmLadder], [0.9, look], [1.3, look], [1.5, p.warmLadder]], t), T, 3.0), LAMP_X(4), ON_Z, 0); lanternLit(ida, t >= 1.2);
        const kv = 1 - ease(clamp01(t / 0.6)), kd = ease(clamp01((t - 0.85) / 0.25)) * (1 - ease(clamp01((t - 1.25) / 0.2))), kb = ease(clamp01((t - 0.8) / 0.2)) * (1 - ease(clamp01((t - 1.3) / 0.2)));
        topHands(ida, G, { V: kv, L: kv }); if (kb > 0) topHands(ida, G, { R: kb, Rdx: 0.5 }); if (kd > 0) gripK(ida, 'L', lanternDoorG(ida), kd); } };
  } });

S1({ id: 's05', scene: 1, t0: 12.0, t1: 16.0, size: 'MCU', angle: 'ngang mắt, 3/4 trước-trái', mm: 85, move: 'tĩnh (khung style frame a_close_ida)',
  why: 'Thói quen hơ tay đếm ba là mô-típ sẽ trả lại ở 2:07 (Cas). Cận đủ để đếm được ba nhịp tay và nghe lời chào con phố.',
  sound: 'THOẠI L1 "Evening, old street." (12,0–14,16); lửa thở', light: 'đèn khí L4 ngay trước mặt (ấm), trời lạnh viền',
  action: 'Hai lòng tay áp gần kính: một, hai, ba (12,3 / 12,9 / 13,5); nói L1; hạ tay.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 90, x1: 125, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'neutral', gaze: [0, 0], glint: (ctx.dbg && ctx.dbg.glint) ?? 0.45 });
    const cam = camMM(85); let camSet = false;
    const beats = [12.3, 12.9, 13.5].map((b) => b - 12);
    // Cổng 6 — L1 "Evening, old street." (12,0–14,16): lời chào ấm với con phố — nét cười nhẹ, mày trong hơi nâng; mắt nhìn ngọn lửa giữa hai lòng tay,
    // ngước lên lồng kính ở "old street"; chớp giữa hai vế và khi hạ tay. Miệng nói: môi–má–cằm cùng động (richLip), biên độ 0,75.
    const face = faceRig(ida), V = ida.VISEMES || {}, G = lampGrips(st, 4), L1 = DIALOGUE.L1, lip = lipKeys(LIP_L1, L1);
    const X_WARM = { smile: 0.28, cheekRaise: 0.12, browInnerUp: 0.18, lidDrop: 0.12 };
    const expr = [[L1 - 0.3, { ...X_WARM, smile: 0.15 }], [L1 + 0.9, X_WARM], [L1 + 2.2, { ...X_WARM, smile: 0.4, cheekRaise: 0.2 }], [L1 + 3.0, { ...X_WARM, smile: 0.3 }], [L1 + 4.0, { ...X_WARM, smile: 0.22, lidDrop: 0.18 }]];
    const gaze = [[0, [0, 0.12]], [0.95, [0, 0.12]], [1.25, [0, -0.06]], [2.3, [0, -0.04]], [2.8, [0, 0.14]], [4, [0, 0.14]]];
    const blinks = [L1 + 1.0, L1 + 2.45, [L1 + 3.55, 1.2]];
    // C2 (mặt A-α của W3): 'fl' = facelight 'gas' (dội ấm vôi/đá + viền trời, nguồn có thật) + phơi sáng khoá theo fl.exposure() tại KHUNG ĐẦU SHOT (v3: hàm thuần);
    // 'x04' = phơi sáng 0,42 × 0,4 (W3 đo). Mặc định chọn theo số đo trong LAYOUT-W1.md mục 13.
    const mode = (ctx.dbg && ctx.dbg.s05) || S05_MODE; const fl = mode === 'fl' ? createFaceLight(st.scene, { mode: 'gas' }) : null; let EXP = mode === 'x04' ? 0.42 * 0.4 : 0.42;
    const L4 = st.lamps.find((l) => l && l.i === 4);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: () => EXP,
      update(t, T, f) {
        // v3 (kiểm toán trạng thái ẩn): máy và phơi sáng KHOÁ được tính TƯỜNG MINH từ khung đầu shot (t = 0, f0), không phụ thuộc khung nào render trước.
        if (!camSet) { const T0s = T - t, f0 = Math.round(T0s * 24);
          ida.place(p.warmLadder, LAMP_X(4), ON_Z, 0); const head = new THREE.Vector3(); ida.joints.head.getWorldPosition(head); head.y += 0.12;
          cam.position.copy(head).add(new THREE.Vector3(-1.55, 0.02, 1.35)); cam.lookAt(head.clone().add(new THREE.Vector3(-0.14, -0.1, 0.22))); camSet = true;   // máy tĩnh (tư thế cố định)
          if (fl) { apply(0, T0s, f0); fl.update(ida, cam, { key: L4 && L4.L }); EXP = fl.exposure() * ((ctx.dbg && ctx.dbg.ek) || S05_EK); } }
        apply(t, T, f); if (fl) fl.update(ida, cam, { key: L4 && L4.L }); } };
    function apply(t, T, f) { st.setState(stdState(T), f);
      let k = 0; for (const b of beats) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
      const pose = t < 2.4 ? lerpPose(p.warmLadder, p.warmLadderIn, k) : poseAt([[2.4, p.warmLadder], [3.1, p.restLadder]], t);
      ida.place(breathe(pose, T, 3.8, 0.8), LAMP_X(4), ON_Z, 0);
      const kr = ease(clamp01((t - 2.6) / 0.5)); if (kr > 0) topHands(ida, G, { R: kr, L: kr });   // Cổng 6: hạ tay → phải nắm thanh móc, trái nắm thân cột (trước: tay lơ lửng cách 11–19 cm)
      face(mixW(richLip(wAt(expr, T), mouthAt(lip, T, V, 0.75)), { blink: blinkAt(T, blinks) }), valAt(gaze, t)); }
  } });

S1({ id: 's06', scene: 1, t0: 16.0, t1: 20.0, size: 'CU (insert)', angle: 'chúc nhẹ, góc nhìn của Ida', mm: 100, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 1 — gieo mô-típ đồng hồ chậm 7 phút (4A): đồng hồ bỏ túi chỉ 7:31; gõ kính hai lần là thói quen thân thương. Mặt chỉ có vạch, không chữ số.',
  sound: 'hai tiếng gõ kính; tích tắc rất khẽ', light: 'đèn khí L4 phía trên; trời chạng vạng',
  action: 'Dưới chân thang, Ida mở đồng hồ bỏ túi (7:31 — giờ thật 7:38), gõ kính hai lần bằng móng tay, cất đi.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 95, x1: 118, shadowLamps: [], groundSoft: 24 }); const p = P(ctx); ladderAt(st.scene, 4);   // (c) nền nhoè thay DOF
    // Cổng 6: đồng hồ + máy insert GIỮ như Cổng 5 (khung đã duyệt; đặt đồng hồ vào lòng tay MPFB thì tay trái đang gõ nằm chắn giữa máy và mặt số — probe);
    // thay vào đó LÒNG TAY PHẢI MPFB được IK đưa lên ÁP dưới đáy đồng hồ (trước: tâm lòng tay cách tâm đồng hồ 9,2 cm — đồng hồ lơ lửng trên ngón).
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 30 }); const watch = watchInHand(st.scene); const wObj = st.scene.getObjectByName('watch');
    const cam = camMM(100); const [mD, hD] = hands(CLOCKS.beat1.watch);
    exposeClock(st.scene);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.4,
      update(t, T, f) { st.setState(stdState(T), f);
        let tap = 0; for (const b of [0.8, 1.2]) tap = Math.max(tap, Math.exp(-(((t - b) / 0.07) ** 2)));
        const pose = t < 2.3 ? p.watchHold(tap) : lerpPose(p.watchHold(0), p.stand, ease((t - 2.3) / 0.6));
        ida.place(settle(pose, T, { side: 1, k: 0.8, br: 3.6 }), LAMP_X(4) + 0.6, LAMP_Z + 0.9, 0.35);   // Cổng 6: đứng tự nhiên (dồn chân trái, lệch hông, thở)
        const dir = new THREE.Vector3(-0.15, 0.8, 0.6).normalize(); watch(ida, cam, mD + 6 * t / 60, hD, dir, 0.32);
        if (wObj) { const ax = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 1, 0)).normalize(); gripK(ida, 'R', { point: wObj.position.toArray(), axis: ax.toArray(), radius: 0.014, out: dir.clone().negate().toArray(), tag: 'đồng hồ' }, 1 - ease(clamp01((t - 2.3) / 0.35))); } } };
  } });

S1({ id: 's07', scene: 1, t0: 20.0, t1: 24.0, size: 'WS', angle: 'ngang tầm mắt', mm: 35, move: 'dolly ngang theo Ida (phải→trái)',
  why: 'Nhịp sáng–tối của phố đèn khí; bóng bà quét từ trước ra sau khi đi qua cột — cái sẽ mất ở cảnh 2.',
  sound: 'bước chân, thang kẽo kẹt; nhạc tạm', light: 'đèn khí L4, L5 (vừa thắp — lược thời gian)',
  action: 'Ida vác thang đi qua cột L5; bóng đổ ngang đá lát, xoay theo vị trí cột.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 60, x1: 130, shadowLamps: [5] }); const p = P(ctx);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T), f); const x = 95.2 - WALK.speed_mps * t;
        ida.place(walkPose(t, p.I.walk_ladder), x, WALK_Z, -Math.PI / 2); gripK(ida, 'R', shoulderLadderG(ida), 1);   // Cổng 6: tay phải nắm thanh thang
        camAt(cam, [[0, [96.0, 1.4, 4.3], [93.6, 1.6, -2.6]], [4, [92.4, 1.4, 4.3], [90.0, 1.6, -2.6]]], t); } };   // W1: lệch máy về trái — khoảng trống phía trước Ida
  } });

S1({ id: 's08', scene: 1, t0: 24.0, t1: 26.0, size: 'WS (tele)', angle: 'ngang tầm mắt', mm: 135, move: 'tĩnh',
  why: 'Tele nén phố: Ida nhỏ ở tiền cảnh, quảng trường và cột đồng hồ (chưa sáng) ở xa. Tiếng rơ-le "tách" báo điều sắp đến; bà không để ý.',
  sound: 'rơ-le "tách" xa; room tone', light: 'đèn khí dọc phố; đồng hồ quảng trường còn tắt',
  action: 'Ida đi về phía máy; xa sau lưng là quảng trường.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 55, x1: 200, shadowLamps: [], fog: [40, 330], farLit: 0 }); const p = P(ctx);   // W1: sương xa cho tele — quảng trường + dãy nhà xa đọc được
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 18 }); const cam = camMM(135); cam.position.set(58, 1.6, 0.6); cam.lookAt(176, 3.4, 0.2);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.4,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(walkPose(t, p.I.walk_ladder), 88.5 - WALK.speed_mps * t, WALK_Z + 0.6, -Math.PI / 2 - 0.12); gripK(ida, 'R', shoulderLadderG(ida), 1); } };   // Cổng 6: tay phải nắm thanh thang
  } });

// ---------------- CẢNH 2 — Bật điện ----------------
S1({ id: 's09', scene: 2, size: 'MS', angle: 'thấp, hất lên cột đồng hồ', mm: 50, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 2a — thứ sáng đầu tiên của lưới điện là đồng hồ (luật thế giới mục 1): mặt kính sáng trắng đúng 8:00, chuông đánh. Nền trời đêm có sao: đây là ĐÊM, ánh trắng sắp tới là đèn điện, không phải bình minh.',
  sound: 'rơ-le; mặt kính bật; chuông điện "DING"; rè điện bắt đầu', light: 'mặt đồng hồ kính mờ phát trắng (nguồn điện đầu tiên); trời đêm',
  action: 'Mặt đồng hồ bật sáng trắng; hai kim đứng đúng 8:00; chuông đánh một tiếng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 150, x1: 200, shadowLamps: [] });
    const cam = camMM(50); cam.position.set(169.2, 1.7, -3.4); cam.lookAt(176, 5.7, 0.5);   // W1: mái nhà quảng trường neo đáy khung
    const cl = new THREE.PointLight('#e8eeff', 0, 14, 1.5); cl.position.set(CLOCK.x - 0.6, CLOCK.h, CLOCK.z); st.scene.add(cl);
    const [mD, hD] = hands(CLOCKS.beat2.square);
    exposeClock(st.scene);
    return { scene: st.scene, cam, named: {}, paintP: PAINT_STREET, exposure: 1.7,
      update(t, T, f) { const s0 = stdState(T); st.setState(s0, f); st.clock.userData.setHands(mD + 6 * Math.max(0, T - DING) / 60, hD); cl.intensity = 30 * s0.clock; } };
  } });

S1({ id: 's09w', scene: 2, size: 'CU (insert)', angle: 'POV của Ida, tay giơ', mm: 105, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 2b — cắt khớp ngay sau tiếng chuông: đồng hồ bỏ túi của bà chỉ 7:53. Giờ mới đã tới mà giờ của bà còn 7 phút: "trễ" đọc bằng hình, không chữ.',
  sound: 'dư âm chuông; tích tắc gần', light: 'đèn khí L6 (ấm) trên tay; trời đêm',
  action: 'Ida (dưới cột L6) giơ đồng hồ bỏ túi ngang tầm mắt: 7:53.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 55, x1: 110, shadowLamps: [], groundSoft: 24 }); const p = P(ctx);   // (c) nền nhoè thay DOF
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const watch = watchInPalm(st.scene); const cam = camMM(105);   // Cổng 6: đồng hồ trong lòng tay MPFB
    const [mD, hD] = hands(CLOCKS.beat2.watch);
    exposeClock(st.scene);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.6,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(settle(p.watchRaise, T, { side: -1, k: 0.7, br: 3.6, bx: 0.5 }), LAMP_X(6) + 1.2, WALK_Z, -Math.PI / 2);   // Cổng 6: đứng tự nhiên, thở nhẹ (tay giữ đồng hồ yên)
        const wp = new THREE.Vector3(0, -0.07, 0); ida.joints.wrist_R.localToWorld(wp);
        const eye = new THREE.Vector3(); ida.joints.head.getWorldPosition(eye); eye.y += 0.1;
        watch(ida, cam, mD + 6 * t / 60, hD, eye.sub(wp).normalize().add(new THREE.Vector3(0, 0.55, 0)), 0.36); } };   // máy cách đồng hồ 0,33 m như Cổng 5 (0,42 − 0,09)
  } });

S1({ id: 's10e', scene: 2, size: 'MS (chèn)', angle: 'thấp, hất lên đầu cột điện', mm: 35, move: 'tĩnh',
  why: 'NGUỒN ĐIỆN THẤY ĐƯỢC: bóng đèn điện trên cột quảng trường nhấp hai lần rồi đứng trắng (kịch bản dòng 48), loá lạnh, gắt, trên nền trời đêm có sao. Đồng hồ vừa sáng ở hậu cảnh.',
  sound: 'tách rơ-le gần; bóng đèn rít; rè điện 50 Hz', light: 'bóng đèn điện quảng trường (trắng lạnh, loá) — nguồn thấy trong khung',
  action: 'Bóng đèn tối → sáng → tắt → sáng → đứng trắng; vũng trắng phẳng tràn xuống đá lát.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 150, x1: 200, shadowLamps: [] }); const hp = st.squarePosts[0].hp;
    const cam = camMM(35); cam.position.set(163.0, 1.3, hp.z + 4.4); cam.lookAt(hp.x + 0.8, hp.y - 1.4, hp.z - 0.6);   // W1: máy trong quảng trường (v2 đặt ở x = 161,3 — nay là sau mặt tiền góc)
    return { scene: st.scene, cam, named: {}, paintP: PAINT_STREET, exposure: expo(1.8, 1.1, (T) => switchOn(T, SQUARE_ON)),
      update(t, T, f) { const s0 = stdState(T); st.setState(s0, f); st.clock.userData.setHands(6 * Math.max(0, T - DING) / 60, 240); } };
  } });

S1({ id: 's10', scene: 2, size: 'EWS', angle: 'cao, sau quảng trường', mm: 28, move: 'tĩnh',
  why: 'Toàn cảnh lặp khung mở đầu để đo thay đổi, nay là ĐÊM (trời xanh đen, không hồng): tấm kính quanh quảng trường đứng trắng, từng khối phố bật lan xuống dốc. Khối cuối cạnh nhà kho CHƯA bật (đoạn cáp cuối).',
  sound: 'rè điện lớn dần; các tiếng "tách" nối tiếp', light: 'đèn điện (trắng phẳng) lan khỏi quảng trường; đèn khí còn lại',
  action: 'Sóng trắng lăn xuống dốc theo phố Ostler; một đoạn cuối phố còn hổ phách.',
  async build(ctx) { const c = await buildCitySet(ctx, 'wave', { square: SQUARE_ON, t0: T0.s10, skipLast: 1 }); return { ...c, exposure: 1.0, grade: GRADE_COLD }; } });

S1({ id: 's11', scene: 2, size: 'MS', angle: 'ngang, 3/4 trước-trái', mm: 50, move: 'tĩnh',
  why: 'Phản ứng: bà quay về phía quảng trường (phải khung = hướng sóng tới).',
  sound: 'rè điện từ xa; tách', light: 'đèn khí L7 vừa thắp (ấm), ánh trắng lờ mờ phía xa',
  action: 'Ida trên thang ở cột L7, quay đầu và vai về phía quảng trường.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const cam = camMM(50); cam.position.set(61.6, 2.5, -1.2); cam.lookAt(64.0, 2.9, -4.4);
    const wf = whiteAt(64), G = lampGrips(st, 7);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 0.3 * wf(T) }), f); ida.place(breathe(poseAt([[0, p.restLadder], [0.3, p.restLadder], [1.2, p.turnSquare]], t), T, 3.6), LAMP_X(7), ON_Z, 0);
        topHands(ida, G, { R: 1, L: 1, LB: ease(clamp01((t - 0.35) / 0.8)) }); } };   // Cổng 6: phải nắm thanh móc, trái nắm thân cột rồi (0,35–1,15 s, khi quay vai) chuyển sang nhánh trái thanh móc — thân cột ngoài tầm với 3 cm khi thân quay (trước: tay lơ lửng cách 15–19 cm)
  } });

S1({ id: 's12', scene: 2, size: 'WS (qua vai)', angle: 'cao ngang vai Ida, nhìn lên phố', mm: 35, move: 'tĩnh',
  why: 'Qua vai bà: bóng đèn cột điện x=85 nhấp hai lần rồi đứng (nguồn thấy được); trắng nuốt những ngọn bà vừa thắp (L5, L6) — vũng hổ phách mỏng dần. Trời đêm phía trên.',
  sound: 'tách; rè điện', light: 'cột điện x=85 bật; đèn khí L5, L6 chìm trong trắng',
  action: 'Lưng/vai Ida tiền cảnh trái; phía xa bóng đèn điện bật, phố trắng dần.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 55, x1: 200, shadowLamps: [], fog: [30, 220] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35); cam.position.set(62.3, 3.4, -5.0); cam.lookAt(100, 2.6, -1.0);
    const wf = whiteAt(85), G = lampGrips(st, 7);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.2, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 0.5 * wf(T) }), f); ida.place(breathe(p.turnSquare, T, 3.6), LAMP_X(7), ON_Z, 0); topHands(ida, G, { R: 1, LB: 1 }); } };   // Cổng 6: thở; hai tay nắm hai nhánh thanh móc
  } });

S1({ id: 's13', scene: 2, size: 'MS', angle: 'thấp nhẹ, 3/4 trước-phải', mm: 50, move: 'tĩnh',
  why: 'Sóng tới chính bà (0:40, câu hỏi c1): mặt bà đổi từ ấm sang trắng phẳng; bà nhìn xuống.',
  sound: 'rè điện gần; tách', light: 'trắng tràn tới (nhấp 2 lần), đèn khí L7 còn đó nhưng chìm',
  action: 'Trắng tràn lên người Ida; bà cúi nhìn xuống đá lát.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const cam = camMM(50); cam.position.set(66.8, 2.0, -1.0); cam.lookAt(64.0, 2.9, -4.4);
    const wf = (T) => switchOn(T, REACH_IDA), G = lampGrips(st, 7);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.1, wf),
      update(t, T, f) { st.setState({ ...stdState(T, { whiteFill: (T) => 1.2 * wf(T) }), gasLight: (i) => (i === 7 ? 1 - 0.85 * clamp01((T - REACH_IDA) / 0.5) : 1) }, f);   // W1: ánh L7 chìm trong trắng → bóng nhạt hết trong 0,5 s (luật 3.3)
        ida.place(breathe(poseAt([[0, p.turnSquare], [0.5, p.turnSquare], [1.3, p.lookDown]], t), T, 3.6), LAMP_X(7), ON_Z, 0); topHands(ida, G, { R: 1, L: 1, LB: 1 - ease(clamp01((t - 0.5) / 0.8)) }); } };   // Cổng 6: phải nắm thanh móc; trái từ nhánh thanh móc về thân cột khi cúi (0,5–1,3 s)
  } });

S1({ id: 's14', scene: 2, size: 'MS (chúc)', angle: 'cao, chúc xuống đá lát', mm: 28, move: 'tĩnh',
  why: 'Hình then chốt cảnh 2: bóng dài đã mất; bà giơ tay — không gì động trên đá lát.',
  sound: 'rè điện đều; im', light: 'trắng phẳng (không bóng); vệt tối mờ dưới chân thang',
  action: 'Ida giơ tay trái lên; nền đá không có bóng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 90, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 7);   // W1: L7 chìm trong trắng → không bóng dài (luật 3.1, 3.3)
    // Cổng 6: tay trái giơ NGANG ra bên (dạng 75°, gập vai 40°) thay "ra trước–ngang" (−62, 0, 34): từ máy cao chúc, tay ra trước bị co ngắn, đọc thành tay buông cạnh hông (probe)
    const LH = (ctx.dbg && ctx.dbg.lift) || [-40, 0, 75, -8];
    const liftHigh = over(p.liftHand, { joints: { shoulder_L: LH.slice(0, 3), elbow_L: [LH[3], 0, 0], wrist_L: [0, 0, -10] } });   // W1 cục bộ: tay trái giơ ra trước-ngang, lòng úp
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 24 }); const cam = camMM(28); cam.position.set(65.9, 4.5, -2.3); cam.lookAt(64.0, 1.4, -4.7);   // W1: từ phía đầu dốc, chúc ~50° — v2 cắt đầu Ida, lồng đèn che người
    const G = lampGrips(st, 7);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.1,
      update(t, T, f) { st.setState({ ...stdState(T, { whiteFill: () => 1.2 }), gasLight: (i) => (i === 7 ? 0.15 : 1) }, f); ida.place(breathe(poseAt([[0, p.lookDown], [0.4, p.lookDown], [1.1, liftHigh]], t), T, 3.6), LAMP_X(7), ON_Z, 0);
        topHands(ida, G, { R: 1, L: 1 - ease(clamp01((t - 0.35) / 0.35)) }); } };   // Cổng 6: phải giữ thanh móc; trái rời thân cột rồi giơ lên (0,35–0,7 s)
  } });

// ---------------- CẢNH 3 — Chạy đua ----------------
// Montage nén thời gian: mỗi shot có nhịp "nở hổ phách → trắng phủ" riêng; cột điện bật theo POST_ON.
S1({ id: 's15', scene: 3, size: 'WS', angle: 'ngang tầm mắt', mm: 35, move: 'tĩnh',
  why: 'Chuyển cảnh: bà xuống thang, quay người về phía dốc xuống (trái khung) — đuổi theo phần phố chưa có điện. Trời đêm trên mái.',
  sound: 'bước xuống thang; rè điện', light: 'trắng phẳng (cột x=85); đèn khí L7 chìm',
  action: 'Ida tụt nhanh xuống thang, vác thang, quay về phía dốc xuống.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 0, x1: 100, shadowLamps: [], fog: [12, 55] }); const p = P(ctx); const lad = ladderAt(st.scene, 7);   // sương gần: đoạn dốc dưới chìm tối (trắng tràn previs là toàn cục — Cổng 7 làm ánh theo khối)
    // W1: máy phía nam nhìn chéo XUÔI dốc: Ida trong trắng ở phải khung; trái khung là đoạn phố dưới còn tối (chưa điện, chưa thắp) — nơi bà sắp chạy tới.
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35); cam.position.set(69.5, 1.5, 3.4); cam.lookAt(60.0, 2.1, -4.0); const G = lampGrips(st, 7);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f); lad.visible = t < 1.1;   // W1: thang lên vai ở 1,1 s → hết cảnh hai cái thang
        // Cổng 6: tụt thang — hai tay nắm thanh thang (IK, so le); chạm đất → đứng dồn chân, thở gấp; 1,1 s thang lên vai → tay phải nắm thanh thang trên vai (IK trộn vào 0,15 s).
        if (t < 0.8) { const u = 1 - t / 0.8; ida.place(p.climb(u, p.restLadder), LAMP_X(7), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); climbHands(ida, lad, G, u); }
        else { ida.place(settle(poseAt([[0.8, p.stand], [1.4, over(p.stand, { props: ['ladder_shoulder', 'lantern_belt'], joints: p.I.walk_ladder.joints })]], t), T, { side: 1, k: 0.8 * (1 - ease(clamp01((t - 1.1) / 0.3))), br: 2.4 }), LAMP_X(7) - 0.3, FOOT_Z + 0.5, valAt([[0.8, 0], [1.4, -Math.PI / 2]], t));
          if (t >= 1.1) gripK(ida, 'R', shoulderLadderG(ida), ease(clamp01((t - 1.1) / 0.15))); } } };
  } });

const lampShot = (id, i, cam0, why, extra = {}) => S1({ id, scene: 3, size: 'WS', angle: extra.angle || 'ngang', mm: extra.mm || 35, move: 'tĩnh', why,
  sound: `"phụp" L${i}; tách + rè khi cột điện bật`, light: `đèn khí L${i} vừa thắp (có bóng) → bóng đèn cột điện nhấp hai lần, đứng trắng`,
  action: extra.action || `Ida trên thang ở L${i}: hổ phách nở, bóng dài; vài giây sau cột điện bật, trắng phủ, bóng tan trong 0,5 s.`,
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: Math.max(0, LAMP_X(i) - 30), x1: 200, shadowLamps: [i], fog: extra.fog }); const p = P(ctx); ladderAt(st.scene, i);   // W1: dựng tới quảng trường
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 24 }); const cam = camMM(extra.mm || 35); cam.position.set(...cam0[0]); cam.lookAt(...cam0[1]);
    const wf = whiteAt(LAMP_X(i)), G = lampGrips(st, i);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.15, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 1.1 * wf(T) }), f);
        ida.place(breathe(poseAt([[0, p.valveLadder], [0.5, p.valveLadder], [1.2, p.warmLadder]], t), T, 3.0), LAMP_X(i), ON_Z, 0);
        const k = 1 - ease(clamp01((t - 0.5) / 0.5)); topHands(ida, G, { V: k, L: k }); } };   // Cổng 6: tay phải trên van (IK) tới 0,5 s, trái nắm thân cột; buông lên kính
  } });
lampShot('s19', 8, [[41.0, 1.7, 1.0], [53.0, 3.0, -0.5]], 'Montage: ngọn thứ 8 nở hổ phách, bóng bà đổ dài — rồi bóng đèn cột điện x=57 (trong khung, phải) nhấp hai lần, đứng trắng, xoá bóng.');
S1({ id: 's21', scene: 3, t0: 58.0, t1: 60.0, size: 'MCU (tay)', angle: 'ngang, 3/4', mm: 85, move: 'tĩnh',
  why: 'Vội: trèo quá nhanh, tuột sào mồi rồi chụp lại — lần đầu thấy tay bà không vững.',
  sound: 'thang rung; sào gỗ va; hơi thở gấp', light: 'trắng phẳng; L10 chưa thắp',
  action: 'Ida trèo nhanh lên L10, sào mồi trượt khỏi tay (58,9), chụp lại (59,4).',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 0, x1: 50, shadowLamps: [] }); const p = P(ctx); const lad = ladderAt(st.scene, 10); const G = lampGrips(st, 10);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 32 }); const cam = camMM(85); cam.position.set(20.1, 3.1, -2.3); cam.lookAt(22.0, 3.0, -4.5);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.0 }), f);
        const cu = 0.66 + 0.34 * t / 0.7;   // W1: bắt đầu ở bậc cao hơn (v2 bắt đầu 0,4 → khung đầu trống)
        const pose = t < 0.7 ? lerpPose(p.climb(cu, p.poleLadder), p.poleLadder, 0) : poseAt([[0.7, p.poleLadder], [0.9, p.poleFumble], [1.3, p.poleFumble], [1.5, p.poleLadder]], t);
        ida.place(t < 0.7 ? { ...pose, props: ['pole_hand_R', 'lantern_belt'] } : pose, LAMP_X(10), t < 0.7 ? FOOT_Z + (ON_Z - FOOT_Z) * ease(cu) : ON_Z, 0);
        const pole = ida.props.pole; if (pole && t > 0.85 && t < 1.45) pole.rotation.z = 0.5 * Math.sin((t - 0.85) / 0.6 * Math.PI); else if (pole) pole.rotation.z = 0;
        // Cổng 6: tay trái (tay không cầm sào) nắm thanh thang khi trèo, lên đỉnh thì nắm thân cột; buông khi sào trượt (0,8–0,9 s), nắm lại 1,4–1,6 s.
        if (t < 0.7) { const kt = ease(clamp01((cu - 0.55) / 0.35)); gripK(ida, 'L', railG(lad, Math.sign(G.X.x || 1), Math.min(1.72, 1.55 * ease(cu) + 1.12)), 1 - kt); gripK(ida, 'L', G.post(2.4), kt); }
        else gripK(ida, 'L', G.post(2.4), clamp01(1 - ease(clamp01((t - 0.8) / 0.1)) + ease(clamp01((t - 1.4) / 0.2)))); } };
  } });

S1({ id: 's22', scene: 3, t0: 60.0, t1: 63.0, size: 'MCU', angle: 'ngang mắt, 3/4', mm: 85, move: 'tĩnh',
  why: 'Lời thoại duy nhất của cảnh chạy đua; ngọn L10 bắt lửa ấm lên mặt bà rồi bị trắng dìm ngay.',
  sound: 'THOẠI L2 "Not yet... not yet." (60,0–62,88); "phụp" (62,95, sau câu thoại, tràn qua điểm cắt)', light: 'trắng phẳng; đèn khí L10 bắt lửa ở khung cuối (ấm lên mặt)',
  action: 'Ida lẩm bẩm, mở van; lửa bắt ngay khi câu dứt; hổ phách chìm trong trắng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 5, x1: 40, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 10);
    const dbg = ctx.dbg || {};
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'neutral', gaze: [0, 0], glint: dbg.glint ?? S22.glint }); const cam = camMM(85); let camSet = false;
    const face = faceRig(ida), V = ida.VISEMES || {}, G = lampGrips(st, 10), L2 = DIALOGUE.L2, lip = lipKeys(LIP_L2, L2);
    // Cổng 6 (quyết định cố định, shots_w1.json trường cong6): Ida 3/4 — máy lệch S22.yaw độ khỏi hướng mặt (> 30°), GIỮ MCU 85 mm, cách 1,2 m. Máy tĩnh, tính MỘT lần từ tư thế t = 0.
    const X_STR = { press: 0.7, browKnit: 0.75, browDown: 0.3, chinRaise: 0.35, lidDrop: 0.2 };   // 'strained' (FACE_PRESETS) + mí che bớt tròng
    const expr = [[L2 - 0.5, X_STR], [L2 + 1.0, { ...X_STR, browInnerUp: 0.25 }], [L2 + 1.5, { ...X_STR, browInnerUp: 0.35, press: 0.8 }], [L2 + 2.5, { ...X_STR, browDown: 0.1, browInnerUp: 0.4 }],
      [L2 + 2.92, { ...X_STR, browDown: 0.1, browInnerUp: 0.4 }], [L2 + 3.05, { press: 0.2, browKnit: 0.3, browInnerUp: 0.45, lidDrop: 0.05, smile: 0.12 }]];
    const gaze = [[0, [0.02, 0.02]], [1.5, [0.02, 0.04]], [1.9, [0, -0.2]], [2.4, [0, -0.24]], [3.0, [0, -0.22]]];
    const blinks = [L2 + 0.95, [L2 + 1.42, 1.3], L2 + 2.62];
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 0.8,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.0 }), f);
        // W1: tay phải trên van suốt shot; sào mồi chuyển sang tay trái NGOÀI KHUNG (liên tục s21 → s22, xem continuity canh-3.md).
        // v2 kết bằng hai lòng tay xoè (warmLadder) — mâu thuẫn với tay trái đang cầm sào → bỏ; giữ tay trên van tới khi lửa bắt.
        const hv = { R: { spread: 0.05, curl: 0.88 }, L: p.LH.L };   // Cổng 6: ngón ôm thân van (curl 0,6 của sheet với tay MPFB → hai ngón duỗi thẳng)
        const v0 = over(p.valveLadder, { joints: { neck: [-4, 30, 0] }, hands: hv }), v1 = over(p.valveLadder, { joints: { neck: [-14, 26, 0], elbow_R: [-52, 0, 0] }, hands: hv });
        if (!camSet) { ida.place(v0, LAMP_X(10), ON_Z, 0); faceCam(cam, ida, { yaw: dbg.yaw ?? S22.yaw, dist: dbg.dist ?? 1.2, fov: fovOf(85), y: dbg.cy ?? -0.02 }); cam.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), (dbg.pan ?? S22.pan) * Math.PI / 180); camSet = true; }   // máy tĩnh (S22.pan: lia ngang để thử; lia trái 3,5° đưa tay + ống van vào khung thì đọc thành khối đồng che góc trái → chốt 0)
        ida.place(breathe(poseAt([[0, v0], [1.6, v0], [2.4, v1]], t), T, 2.6, 1.3), LAMP_X(10), ON_Z, 0);   // thở gấp (chạy đua)
        const gV = gripK(ida, 'R', G.valve, 1);   // Cổng 6: tay phải MPFB nắm thân van (IK điểm)
        face(mixW(richLip(wAt(expr, T), mouthAt(lip, T, V, dbg.lip ?? S22.lip)), { blink: blinkAt(T, blinks) }), valAt(gaze, t));
        if (dbg.log && f % 6 === 0) { const h = wpos(ida.joints.head), q = ida.joints.head.getWorldQuaternion(new THREE.Quaternion()), fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q); fw.y = 0; fw.normalize();
          const tc = cam.position.clone().sub(h); tc.y = 0; tc.normalize(); console.log(JSON.stringify({ s22: +t.toFixed(2), faceDeg: +(Math.acos(Math.max(-1, Math.min(1, fw.dot(tc)))) * 180 / Math.PI).toFixed(1), gripV: gV === null ? null : +gV.toFixed(4) })); } } };
  } });

S1({ id: 's23', scene: 3, t0: 63.0, t1: 66.0, size: 'WS', angle: 'ngang, nhìn xuôi dốc về nhà kho', mm: 28, move: 'tĩnh',
  why: 'Góc ngọn cuối cạnh bức tường vôi nhà kho thuộc ĐOẠN CÁP CUỐI (luật thế giới mục 1, v0.4): cột điện góc còn TẮT, góc còn tối; phố sau lưng bà đã trắng. Chỉ đạo chủ dự án 0:40.',
  sound: 'bước chạy; thang; "phụp"', light: 'L11 bắt lửa; cột điện góc (x=11) còn tắt; phố trắng ở xa sau lưng',
  action: 'Ida hối hả tới L11, trèo, thắp. Hổ phách.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 60, shadowLamps: [11] }); const p = P(ctx); const lad = ladderAt(st.scene, 11);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const C23 = (ctx.dbg && ctx.dbg.s23cam) || S23_CAM; const cam = camMM(C23.mm); cam.position.set(...C23.pos); cam.lookAt(...C23.look);   // dbg.s23cam: thử máy khi đo
    const fast = { cycle_s: 0.9, stride_m: 0.6, speed_mps: 1.3 };
    // N1 (rà continuity P): Cas đã đứng ở chân tường chim từ trước (s24 thấy cậu ở đó) → có mặt trong s23, đứng yên, nhỏ ở nền, nhìn về L11/Ida.
    const cas = mkChar(ctx, st.scene, 'cas', { detail: 16 }); const CL = casLeanSpot(st), [cx, cz] = [CL.x, CL.z];   // Cổng 6: Cas dựa tường (như s24, s24c)
    const B2 = hideWallPost(st); if (ctx.dbg && ctx.dbg.log) console.log(JSON.stringify({ s23B2: B2 }));   // B2: cột điện tường chim ra khỏi khung
    const G = lampGrips(st, 11), lad0 = { p: lad.position.clone(), q: lad.quaternion.clone() };
    if (ctx.dbg && ctx.dbg.limeMask) limeMask(st);   // đo V3: tỷ lệ điểm ảnh mặt vôi trắng nhà kho (chỉ khi --dbg '{"limeMask":1}' --nopaint)
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: ctx.dbg && ctx.dbg.limeMask ? 1.0 : expo(2.4, 1.8, (T) => gasLevel(11, T)),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.06 }), f);
        cas.place(casLeanPose(p, T, [0, CL.neckY, 0]), cx, cz, CL.yaw); casWallHand(cas, CL);
        // Cổng 6 — "DỰNG THANG" (0,85–1,1 s): thang rời vai, xoay + trượt từ vị trí trên vai tới chỗ tựa cột (nội suy vị trí/hướng thế giới), tay phải vẫn nắm thanh;
        // từ 1,1 s trèo (hai tay nắm thanh, so le) → 1,9 s tay phải lên van (IK), trái nắm thân cột → 2,05–2,5 s buông lên kính. Trước: đổi thang tức thì ở 1,1 s.
        if (t < 1.1) { ida.place(walkPose(t, p.I.walk_ladder, { gait: fast }), valAt([[0, 14.2], [1.1, LAMP_X(11) + 0.2]], t), valAt([[0, WALK_Z], [1.1, FOOT_Z]], t), yawTo(14.2, WALK_Z, LAMP_X(11), FOOT_Z));
          const sl = ida.props.ladder, u = ease(clamp01((t - 0.85) / 0.25));
          if (u <= 0) { sl.visible = true; lad.visible = false; lad.position.copy(lad0.p); lad.quaternion.copy(lad0.q); gripK(ida, 'R', shoulderLadderG(ida), 1); }
          else { sl.updateMatrixWorld(true); const pw = new THREE.Vector3(), qw = new THREE.Quaternion(); sl.matrixWorld.decompose(pw, qw, new THREE.Vector3());
            sl.visible = false; lad.visible = true; lad.position.copy(pw).lerp(lad0.p, u); lad.quaternion.copy(qw).slerp(lad0.q, u); lad.updateMatrixWorld(true);
            gripK(ida, 'R', railG(lad, -Math.sign(G.X.x || 1), 1.0, 'len'), 1 - 0.6 * u); } }
        else { if (ida.props.ladder) ida.props.ladder.visible = true; lad.visible = true; lad.position.copy(lad0.p); lad.quaternion.copy(lad0.q);
          if (t < 1.9) { const u = (t - 1.1) / 0.8; ida.place(p.climb(u, p.valveLadder), LAMP_X(11), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); climbHands(ida, lad, G, u, { V: 1, L: 1 }); }
          else { ida.place(breathe(poseAt([[1.9, p.valveLadder], [2.5, p.warmLadder]], t), T, 2.6, 1.3), LAMP_X(11), ON_Z, 0); const k = 1 - ease(clamp01((t - 2.05) / 0.45)); topHands(ida, G, { V: k, L: k }); } }
        if (st.scene.userData.blackenLater) st.scene.userData.blackenLater(); } };
  } });

S1({ id: 's24', scene: 3, t0: 66.0, t1: 68.0, size: 'MS', angle: 'hơi cao, 3/4 trước-phải', mm: 35, move: 'tĩnh',
  why: 'Nhịp đếm ba lần thứ hai; góc cuối phố chỉ còn hổ phách. Ở nền, cậu bé đứng ở tường nhìn bà — bà không thấy (gieo cảnh 4).',
  sound: 'lửa thở; im lặng tương đối', light: 'đèn khí L11 (ấm) — góc cuối phố chưa có điện',
  action: 'Ida áp tay vào kính: một, hai, ba. Xa phía sau, Cas nhìn.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 30 }); const cas = mkChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(30); cam.position.set(11.2, 2.1, 1.8); cam.lookAt(10.5, 1.8, -5.8);   // A2 (B1, W2 A2): Ida (L11) trái, Cas ở sân trước hông phải, gần hơn 3 m để Cas đọc được; P5 (10,8; 3,9) sau máy, tia tới Cas qua trước góc nhà x = 15   // giai đoạn C: Ida (L11) trái–giữa, Cas ở chân tường chim phải khung (casSpot W2)
    const CL = casLeanSpot(st), [cx, cz] = [CL.x, CL.z];   // Cổng 6: Cas dựa tường
    const beats = [0.2, 0.8, 1.4];
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.6,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.05 }), f);
        let k = 0; for (const b of beats) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        ida.place(breathe(lerpPose(p.warmLadder, p.warmLadderIn, k), T, 3.2), LAMP_X(11), ON_Z, 0);
        cas.place(casLeanPose(p, T, [0, CL.neckY, 0]), cx, cz, CL.yaw); casWallHand(cas, CL); } };
  } });

S1({ id: 's24c', scene: 3, size: 'MS', angle: 'ngang mắt Cas, 3/4 trước-phải', mm: 50, move: 'tĩnh',
  why: 'Giới thiệu Cas rõ (AI mù v1: "Cas 1:04–1:06 chỉ là một chấm"): cậu bé áo len quá khổ, một mình ở chân tường nhà kho, mặt ấm lên vì ngọn L11 vừa thắp; cậu nhìn bà.',
  sound: 'lửa thở xa; im', light: 'đèn khí L11 (ấm, bên phải khung); góc tối', action: 'Cas đứng dựa tường vôi, nhìn về phía cột đèn (phải khung), tay giấu trong tay áo.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 18 }); const cas = mkChar(ctx, st.scene, 'cas', { detail: 34, expr: 'neutral' });
    const CL = casLeanSpot(st), [cx, cz] = [CL.x, CL.z], dbg = ctx.dbg || {};   // Cổng 6: chỗ dựa tường (cùng x casSpot, cách tường CAS_LEAN.d)
    // A2 (B1): máy 3/4 trước Cas, lệch −35° khỏi hướng nhìn của cậu về L11, cách 2,1 m (tính theo casSpot — hướng tới L11 đổi khi Cas dời).
    const gx = LAMP_X(11) - cx, gz = ON_Z - cz, gl = Math.hypot(gx, gz), ga = -35 * Math.PI / 180, dx = (gx * Math.cos(ga) - gz * Math.sin(ga)) / gl, dz = (gx * Math.sin(ga) + gz * Math.cos(ga)) / gl;
    const cam = camMM(50); cam.position.set(cx + 2.1 * dx, 1.05, cz + 2.1 * dz); cam.lookAt(cx, 0.95, cz);   // giai đoạn C: 3/4 trước Cas (lệch 35° khỏi hướng nhìn về L11) — Cas nhìn sang TRÁI khung (về Ida), tường chim sau lưng
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 4.5,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.05 }), f); ida.place(p.warmLadder, LAMP_X(11), ON_Z, 0);
        cas.place(casLeanPose(p, T, [-4, CL.neckY + valAt([[0, -10], [0.6, -10], [1.3, 6]], t), 0]), cx, cz, CL.yaw);
        const gw = casWallHand(cas, CL); if (dbg.log && f % 6 === 0) console.log(JSON.stringify({ s24c: +t.toFixed(2), wall: gw === null ? null : +gw.toFixed(4) })); } };
  } });


// Cine Lab · Cổng 5 LAYOUT — GÓI W2: cảnh 4–6 (s25 → hết phim). Chỉ W2 sửa file này.
// Layout chốt (giai đoạn A): camera cuối (tiêu cự, vị trí, hướng, chuyển máy), dàn dựng, bối cảnh đủ, trục 180°. Bảng + lý do: shots/layout/LAYOUT-W2.md.
// Mọi shot đọc ctx.dbg (--dbg JSON của render_film.js) để dò tham số khi probe; không truyền --dbg thì dùng giá trị chốt.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { walkPose, WALK, WALK_CHILD } from '/cong3/shared/anim.js';
import { buildStreetSet, LAMP_X, LAMP_Z, WALK_Z, POST_X, CLOCK, ladderOf, buildWatch, lamMat, flickAt, GRADE_COLD } from './sets.js';
import { buildCitySet, buildWallSet, buildBaySet, buildAlleySet, buildRoomSet } from './sets2.js';
import { buildLantern } from '/cong3/shared/cast.js';
import { U } from '/cong3/v2/s5.js';
import { ease, easeIO, clamp01, fovOf, lerpPose, over, poseAt, valAt, camAt, makeChar as makeChar0, yawTo } from './util.js';
import { createFaceLight } from './facelight.js';
// B-i (Cổng 5 v2, quyết định chủ dự án): mọi shot W2 là hàm THUẦN theo t. Rig (shared/cast.js applyPose) tính đạo cụ treo (đèn lồng thắt lưng: hướng = nghịch đảo
// hướng xương chậu THẾ GIỚI) theo ma trận gốc ĐANG CÓ; util.makeChar.place đặt gốc SAU setPose → đèn mang hướng gốc của KHUNG TRƯỚC (render thẳng một khung ≠ render nối tiếp;
// khung đầu mỗi shot dùng hướng 0 của nhân vật mới dựng). Bản bọc: đặt gốc (vị trí + hướng) TRƯỚC, rồi mới gọi place gốc (setPose) — không phụ thuộc khung trước.
const rootFirst = (ch, x, y, z, yaw) => { ch.root.position.set(x, y, z); ch.root.rotation.y = yaw; ch.root.updateMatrixWorld(true); };
const makeChar = (...a) => { const ch = makeChar0(...a); const place0 = ch.place;
  ch.place = (pose, x, z, yaw, y0 = 0) => { rootFirst(ch, x, y0 + (pose.root_y_m ?? 0), z, yaw); place0(pose, x, z, yaw, y0); }; return ch; };   // W3: ánh dội/viền cận mặt Ida từ nguồn có thật (không nguồn ngoài truyện)
import { CLOCKS, CLOCK_ON, DIALOGUE, DING, FILM_S, FOOT_Z, GAS_ON, GRADE_ALLEY, GRADE_S5, L11_OFF, ON_Z, ORDER, P, PAINT_CLOSE, PAINT_STREET, PAINT_WALL, POST_ON, REACH_IDA, RELAY_1, S, S5_PAINT, S5_PAINT_MED, S6_PAINT, SHOTS, SQUARE_ON, SRC, T0, T1, VALVE, WALL_POST_ON, camMM, expo, faceCam, flameL11, gasLevel, hands, ladderAt, lanternLight, stdState, switchOn, watchInHand, whiteAt } from './common.js';

const V3a = (v) => v.toArray().map((x) => +x.toFixed(3));
const wpos = (o) => o.getWorldPosition(new THREE.Vector3());

// =====================================================================================================================
// CỔNG 6 · W2 — DIỄN HOẠT (AUTHORSHIP "Cổng 6 — diễn hoạt", 29/09/2026). Mọi rãnh dưới đây là hàm THUẦN theo thời gian phim T (B-i).
// =====================================================================================================================
// (e) ĐỨNG TỰ NHIÊN: dồn trọng tâm sang một chân (hông bên chịu lực cao hơn — chậu nghiêng 3°), chân kia chùng gối, thân bù nghiêng ngược,
// thở (ngực/vai) và dao động trọng tâm rất chậm. Cộng dồn vào tư thế gốc (không thay tư thế sheet). o = { side: +1 dồn chân TRÁI / −1 PHẢI, k, br (chu kỳ thở s), ph }.
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
// (d) NẮM TẠI MỘT ĐIỂM. cast3d.reachGrip đưa tâm lòng tay tới ĐƯỜNG TRỤC vô hạn (chiếu điểm nắm hiện tại lên trục) → với vật NGẮN (thân van 5 cm, cần van 10 cm,
// vòng quai đèn lồng) tay trượt dọc trục, ra khỏi vật (đo s40: lòng tay cách cần van 0,18 m dù hàm trả −2,3 mm). Bản này (viết trong gói W2, không sửa mã dùng chung)
// giữ nguyên thuật toán IK 2 xương + xoay cổ tay của reachGrip nhưng CỐ ĐỊNH đích: tâm trục = g.point; lòng tay úp vào trục từ phía vai (hoặc g.out).
// Trả khoảng cách tâm lòng tay → mặt vật (m) đo 3D thật.
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
    const zc = new THREE.Vector3(0, 0, 1).applyQuaternion(wq(wr)); const zw = A.clone().multiplyScalar(zc.dot(A) >= 0 ? 1 : -1);
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
// (c) MẶT: trọng số 16 kênh shape key ('bl' v1.5.1) theo khoá thời gian; khẩu hình từ 6 VISEMES; chớp mắt; hướng nhìn = xoay nhãn cầu.
const mixW = (...ws) => { const o = {}; for (const w of ws) for (const [k, v] of Object.entries(w || {})) o[k] = (o[k] || 0) + v; return o; };   // = facerig.mixW (ch.mixW)
const wLerp = (a, b, u) => { const o = {}; for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) o[k] = (a[k] || 0) + ((b[k] || 0) - (a[k] || 0)) * u; return o; };
const wAt = (keys, t) => { if (t <= keys[0][0]) return keys[0][1]; for (let i = 0; i < keys.length - 1; i++) { const [ta, a] = keys[i], [tb, b] = keys[i + 1]; if (t <= tb) return wLerp(a, b, easeIO((t - ta) / (tb - ta))); } return keys[keys.length - 1][1]; };
// Khẩu hình: words = [[bắt đầu, kết thúc (giây trong tệp thoại), [[phần trong từ 0…1, viseme], …]], …]; t0 = mốc đặt câu trong phim.
// Miệng đi TRƯỚC tiếng 0,04 s (đồng bộ môi chuẩn); nghỉ > 0,25 s giữa hai từ → khép về 'rest'.
function lipKeys(words, t0, lead = 0.04) {
  const K = []; let prevEnd = -9;
  for (const [a, b, seq] of words) {
    if (a - prevEnd > 0.25) { if (prevEnd > -9) K.push([t0 + prevEnd + 0.1 - lead, 'rest']); K.push([t0 + a - 0.07 - lead, 'rest']); }
    for (const [u, v] of seq) K.push([t0 + a + u * (b - a) - lead, v]);
    prevEnd = b;
  }
  K.push([t0 + prevEnd + 0.1 - lead, 'rest']); return K;
}
function mouthAt(K, T, V, amp = 0.7) {
  if (T <= K[0][0] || T >= K[K.length - 1][0]) return {};
  for (let i = 0; i < K.length - 1; i++) if (T < K[i + 1][0]) { const u = ease((T - K[i][0]) / (K[i + 1][0] - K[i][0])); const w = wLerp(V[K[i][1]] || {}, V[K[i + 1][1]] || {}, u); for (const k in w) w[k] *= amp; return w; }
  return {};
}
// chớp: đóng 0,07 s, giữ 0,03 s, mở 0,12 s (× dài cho chớp chậm)
const blinkAt = (T, list) => { let m = 0; for (const e of list) { const [b, s] = Array.isArray(e) ? e : [e, 1]; const d = (T - b) / s; m = Math.max(m, d < 0 ? 0 : d < 0.07 ? d / 0.07 : d < 0.1 ? 1 : d < 0.22 ? 1 - (d - 0.1) / 0.12 : 0); } return m; };
// điều khiển mặt một nhân vật: setFace chỉ khi trọng số đổi (da CPU đắt); gaze [ngang, dọc] rad (dọc + = nhìn xuống) cộng vào hướng dựng của nhãn cầu
function faceRig(ch) {
  const eyes = ch.face?.eyes || [], g0 = eyes.map((e) => [e.rotation.x, e.rotation.y]); let last = '';
  return (w, gaze = [0, 0]) => {
    const o = {}; for (const [k, v] of Object.entries(w)) { const c = Math.max(0, Math.min(1, v)); if (c > 0.004) o[k] = +c.toFixed(3); }
    const key = JSON.stringify(o); if (key !== last) { ch.setFace(o); last = key; }
    eyes.forEach((e, i) => e.rotation.set(g0[i][0] + gaze[1], g0[i][1] + gaze[0], 0));
  };
}
// Thoại (mốc đo trên chính tệp take đã duyệt, reports/m1/cong2/tableread-d2/lines; bao năng lượng −38 dB + onset librosa + faster-whisper small.en,
// mix.py đặt câu ở đầu shot, lệch cắt đầu tệp = 0,000 s). L4 (giây trong tệp): "That's the last one, then." 0,09–2,01 · "Goodnight, old street." 3,55–5,06 ·
// "You'll be brighter now." 6,54–7,97 · "Just…" 9,32–9,88 · "keep a little dark for the ones who need it." 10,86–14,07. L3 "Go on, then." 0,04–2,05.
const LIP_L4 = [
  [0.09, 0.45, [[0, 'L'], [0.3, 'A'], [0.75, 'E']]], [0.45, 0.62, [[0, 'L'], [0.5, 'E']]], [0.62, 1.02, [[0, 'L'], [0.35, 'A'], [0.8, 'E']]],
  [1.02, 1.38, [[0, 'O'], [0.5, 'A'], [0.85, 'L']]], [1.38, 1.95, [[0, 'L'], [0.3, 'E'], [0.75, 'L']]],
  [3.56, 3.8, [[0, 'E'], [0.4, 'O'], [0.9, 'L']]], [3.8, 4.2, [[0, 'L'], [0.3, 'A'], [0.8, 'E']]], [4.3, 4.58, [[0, 'O'], [0.6, 'L']]], [4.58, 5.05, [[0, 'E'], [0.35, 'O'], [0.6, 'E'], [0.9, 'L']]],
  [6.54, 6.88, [[0, 'E'], [0.5, 'O']]], [6.88, 7.0, [[0, 'MBP'], [0.6, 'E']]], [7.0, 7.4, [[0, 'MBP'], [0.25, 'O'], [0.5, 'A'], [0.85, 'E']]], [7.4, 7.95, [[0, 'L'], [0.4, 'A'], [0.8, 'O']]],
  [9.32, 9.88, [[0, 'O'], [0.45, 'A'], [0.8, 'E']]],
  [10.86, 11.13, [[0, 'E'], [0.55, 'E'], [0.85, 'MBP']]], [11.13, 11.31, [[0, 'A']]], [11.31, 11.73, [[0, 'L'], [0.3, 'E'], [0.6, 'L'], [0.85, 'E']]],
  [11.73, 12.25, [[0, 'L'], [0.3, 'A'], [0.75, 'O']]], [12.25, 12.54, [[0, 'FV'], [0.45, 'O']]], [12.54, 12.72, [[0, 'L'], [0.5, 'E']]], [12.72, 13.11, [[0, 'O'], [0.45, 'A'], [0.8, 'E']]],
  [13.11, 13.5, [[0, 'O']]], [13.5, 13.75, [[0, 'L'], [0.4, 'E'], [0.85, 'L']]], [13.75, 14.05, [[0, 'E'], [0.7, 'L']]],
];
const LIP_L3 = [[0.05, 0.33, [[0, 'E'], [0.4, 'O']]], [0.33, 0.58, [[0, 'O'], [0.6, 'L']]], [0.58, 1.25, [[0, 'L'], [0.3, 'E'], [0.7, 'L']]]];
// Biểu cảm Ida (trọng số kênh). CƯỜI BUỒN (chủ dự án): có nụ cười + mắt chùng xuống + dừng một nhịp — KHÔNG phải cười vui:
// khoé môi lên nhưng má nâng ít (cheekRaise thấp, squint thấp → mắt không híp "cười tươi", đọc được ở góc nghiêng), đầu trong mày nâng (buồn),
// mí trên sụp (lidDrop) + nhãn cầu nhìn xuống.
const X_SOFT = { browInnerUp: 0.25, smile: 0.12 };
const X_SADSMILE = { smile: 0.8, cheekRaise: 0.3, squint: 0.1, browInnerUp: 0.7, browKnit: 0.2, lidDrop: 0.38, jawOpen: 0.02 };
const X_GRIEF = { frown: 0.7, browInnerUp: 1.0, browKnit: 0.6, chinRaise: 0.5, lidDrop: 0.3, squint: 0.15 };
// Rãnh cảnh 5 (T = giây phim). L4 = 93,0 → "then." hết 95,0 → cười buồn + mắt chùng 95,0–96,4 (dừng một nhịp, 1,4 s);
// "Goodnight, old street." 96,55–98,06 → cười buồn + mắt chùng 98,1–98,8 (dừng 0,7 s); "Just…" 102,32; "keep … ones" 103,86–106,0 (cắt sang Cas).
const IDA5 = (L4) => ({
  expr: [[L4 - 2.0, { browInnerUp: 0.1 }], [L4 - 0.8, { browInnerUp: 0.2, smile: 0.1 }], [L4, X_SOFT], [L4 + 1.9, { browInnerUp: 0.35, smile: 0.2 }],
    [L4 + 2.4, X_SADSMILE], [L4 + 3.3, { ...X_SADSMILE, smile: 0.7 }], [L4 + 3.55, { browInnerUp: 0.45, smile: 0.3, lidDrop: 0.05 }],
    [L4 + 5.05, { browInnerUp: 0.55, smile: 0.4 }], [L4 + 5.45, { ...X_SADSMILE, smile: 0.9, lidDrop: 0.42 }], [L4 + 5.8, { ...X_SADSMILE, smile: 0.8, lidDrop: 0.45 }],
    [L4 + 6.4, { browInnerUp: 0.5, smile: 0.3, lidDrop: 0.2 }], [L4 + 8.4, { ...X_GRIEF, frown: 0.4, chinRaise: 0.25 }], [L4 + 9.3, X_GRIEF],
    [L4 + 10.2, { ...X_GRIEF, chinRaise: 0.9, press: 0.5 }], [L4 + 10.8, X_GRIEF], [L4 + 14.1, X_GRIEF], [L4 + 15.8, { ...X_GRIEF, frown: 0.5, lidDrop: 0.45 }]],
  gaze: [[L4 - 2.0, [0, -0.08]], [L4 - 0.5, [0, -0.05]], [L4, [0, -0.02]], [L4 + 2.3, [0, -0.02]], [L4 + 2.65, [0, 0.24]], [L4 + 3.4, [0, 0.22]],
    [L4 + 3.55, [0, -0.04]], [L4 + 5.1, [0, -0.03]], [L4 + 5.4, [0, 0.26]], [L4 + 5.8, [0, 0.25]], [L4 + 6.3, [0, 0.0]], [L4 + 8.6, [0, 0.3]],
    [L4 + 9.2, [0, 0.28]], [L4 + 10.9, [0, 0.18]], [L4 + 13.0, [0, 0.25]], [L4 + 15.8, [0, 0.35]]],
  blinks: [L4 - 1.25, L4 - 0.25, [L4 + 2.75, 2.2], L4 + 4.2, L4 + 6.4, L4 + 7.8, L4 + 8.95, [L4 + 10.45, 1.8], L4 + 12.35, [L4 + 14.6, 1.6]],
  // gật/cúi đầu cộng thêm (độ, cổ x): cúi theo ánh mắt ở hai nhịp dừng; ngẩng lên cho "Goodnight"; cúi về phía Cas ở vế cuối
  nod: [[L4, 0], [L4 + 0.7, 2], [L4 + 1.2, 0], [L4 + 2.3, 0], [L4 + 2.8, 6], [L4 + 3.4, 5], [L4 + 3.6, -2], [L4 + 4.3, 1], [L4 + 5.1, 0], [L4 + 5.5, 7], [L4 + 5.8, 7]],
  lip: lipKeys(LIP_L4, L4),
});

// ---------------- CẢNH 4 — Bức tường ----------------
// Bộ tường chim (sets2.buildWallSet, Cổng 5): tường = mặt nhà kho z = 0, cùng địa lý bộ phố (sets_end.wallFromWorld): Cas ở sân lõm bắc (0,15; 0,95) = casSpot;
// L11 (−2,2; 4,2) = L11 bộ phố; hốc cửa x = 5,4 (phải Cas); đầu hồi nhà đầu dãy bắc z = 5 (x −0,5 … 6,5); phố chính ở x < −0,5; góc nhà + phố rẽ ở x ≈ −12; cột điện (2,6; 1,9).
// Luật 180° cảnh 4: đường Ida–Cas; máy luôn ở phía +x của đường này (sau-phải hai người) → Ida TRÁI, Cas PHẢI; Ida nhìn sang PHẢI khung về Cas.
// B1: Cas dời sang đông 3,95 m (casSpot bộ phố (14,3; −7,15) → hệ tường (4,1; 0,95)); mọi máy / dấu cảnh 4 bám Cas dời theo DX.
const DX = 3.95, CAS_W = [0.15 + DX, 0.95], CAS_YAW = Math.PI + 0.15;
// V4 (s26): Ida đứng xem ở IDA_W — cách ngọn L11 3,5 m (góc ngẩng tới ngọn lửa ≈ 25°, dưới đường che của vành mũ) và L11 gần như CHÍNH TRƯỚC mặt bà
// (lệch ≈ 4° so với hướng bà nhìn Cas) → ngọn L11 là key trước lên mặt; máy 3/4 ở phía +x đường Ida–Cas (đúng trục 180°).
// Bản v2 đặt bà (−0,6; 5,2), L11 ở sau-bên (1,9 m, góc ngẩng ≈ 40°): vành mũ che hết mặt, tròng mắt vẫn bắt ánh → "mắt phát sáng", mặt tối.
const IDA_W = [-3.8, 7.3];
// Đèn lồng trong tay Ida quỳ (s31–s32): THẤP (≈ 0,75 m, dưới tay Cas), SAU tay cậu, TRƯỚC bụng cậu, cách tường 0,62 m (≤ 0,7 m — luật 3.3).
// Thân và đầu Cas ở SAU đèn (z ≥ 0,7) → không đổ bóng lên tường; chỉ hai bàn tay (z ≈ 0,35–0,45) ở giữa đèn và tường → chỉ có chim.
const LAN_T = [-0.22 + DX, 0.75, 0.6];
const LAN_K = 3.0;   // mức đèn lồng trong tay (s30: tăng liên tục tới mức này khi đèn ra khỏi thân bà và hạ sát tường; s31, s32 giữ nguyên — cùng một nguồn). Đèn cháy liên tục từ s23 (quyết định N6), không có nhịp mở cửa.
// s32: Cas nhích 0,1 m (z 0,95 → 0,85) và vươn tay ra trước (birdReach) → cổ tay z ≈ 0,4: tay GIỮA đèn (0,62) và tường → chim ×≈2,5–3, cao ≈ 1,9–2,3 m.
const CAS_S32 = [0.15 + DX, 0.74];
// Tư thế cục bộ: chim bóng (sheet 5B) nhưng hai cánh tay vươn ra trước nhiều hơn (vai −92° thay −123°, khuỷu −12° thay −50°) — giữ bắt chéo cổ tay, ngón cái đầu chim.
const birdReach = (b) => over(b, { joints: { shoulder_L: [-92, b.joints.shoulder_L[1], b.joints.shoulder_L[2]], shoulder_R: [-92, b.joints.shoulder_R[1], b.joints.shoulder_R[2]], elbow_L: [-12, 0, 0], elbow_R: [-12, 0, 0] } });
const kneelOf = (p, ctx, o = {}) => over({ ...p.crouch, root_y_m: (p.crouch.root_y_H ?? 0) * ctx.sheets.ida.H_m }, o);
// Đặt Ida sao cho điểm neo lửa đèn lồng trong tay rơi đúng (x, z) của `tgt` (dịch gốc trên mặt đất; độ cao do tư thế quyết định).
function lanternTo(ch, tgt) { const lan = ch.props.lantern; if (!lan || !lan.parent) return; lan.updateMatrixWorld(true); const a = wpos(lan.userData.lightAnchor);
  ch.root.position.x += tgt[0] - a.x; ch.root.position.z += tgt[2] - a.z; ch.root.updateMatrixWorld(true); if (ch.blob) ch.blob.position.set(ch.root.position.x, 0.012, ch.root.position.z); }
const wallShot = (id, t0, t1, meta, fn) => S({ id, scene: 4, t0, t1, ...meta,
  async build(ctx) {
    const W = buildWallSet(ctx); const p = P(ctx); const dbg = ctx.dbg || {};
    const cas = makeChar(ctx, W.scene, 'cas', { detail: meta.casDetail ?? 30, expr: meta.casExpr }); const ida = makeChar(ctx, W.scene, 'ida', { detail: meta.idaDetail ?? 24, expr: meta.idaExpr, hatBack: 0, glint: meta.idaGlint });
    // Cổng 5: vỏ đèn lồng (kính, khung, nắp) KHÔNG đổ bóng từ chính nguồn sáng nằm trong nó — makeChar bật castShadow cho mọi lưới của nhân vật,
    // kể cả đạo cụ; ngọn lửa nằm trong hộp kính nên bản v2 tự che gần hết ánh đèn lồng lên tường (chim s32 mờ, xám).
    if (ida.props.lantern) ida.props.lantern.traverse((o) => { if (o.isMesh) o.castShadow = false; });
    const cam = camMM(meta.mm);
    const ctl = fn(p, cam, ctx, dbg);
    const fl = meta.faceLight ? createFaceLight(W.scene, { mode: meta.faceLight }) : null;
    return { scene: W.scene, cam, named: { ida, cas }, paintP: meta.paintP || PAINT_WALL, exposure: dbg.exp ?? ctl.exposure ?? 2.6,
      update(t, T, f) {
        const e = switchOn(T, WALL_POST_ON);
        const r = ctl.update(t, T, { ida, cas, cam, e });
        const lp = new THREE.Vector3(); let lk = 0;
        if (ida.props.lantern && ida.props.lantern.parent) { ida.props.lantern.updateMatrixWorld(true); ida.props.lantern.userData.lightAnchor.getWorldPosition(lp); lk = r?.lantern ?? 0.012; }   // v3 (N6): đèn lồng CHÁY LIÊN TỤC ở thắt lưng (kính sáng); hắt lên tường/nền rất yếu vì treo ở hông khuất sau thân và vạt áo bà
        W.setState({ gas: 1, elec: e, lantern: lk, lanternPos: lp, fillK: dbg.fillK ?? 1 }, f);
        if (fl && !dbg.nofl) { const fe = fl.update(ida, cam); if (dbg.log && f % 12 === 0) console.log(JSON.stringify({ id, faceE: fe, flExp: +fl.exposure().toFixed(3) })); }
        if (dbg.log && (f % 12 === 0)) console.log(JSON.stringify({ id, t: +t.toFixed(2), lan: V3a(lp), ida: V3a(ida.root.position), idaHead: V3a(wpos(ida.joints.head)), handL: V3a(wpos(cas.joints.wrist_L)), handR: V3a(wpos(cas.joints.wrist_R)), palmL: V3a(cas.gripPoint('L')), palmR: V3a(cas.gripPoint('R')), casHead: V3a(wpos(cas.joints.head)) }));
      } };
  } });
const BIRD_CAM = [[2.2 + DX, 1.3, 3.6], [0.3 + DX, 1.1, 0]];
const idaWatch = (p, T = 0) => settle(over(p.stand, { joints: { neck: [4, 0, 0] } }), T, { side: 1 });   // Cổng 6 (e): bà đứng xem — dồn chân trái, lệch hông, thở
// Cổng 6 (d): tay MPFB đặt tâm lòng tay lệch ≈ 6,4 cm về phía cổ tay so với tay cũ (BAO-CAO-W4T2 §4) → chim bóng thấp hơn, gần đầu hơn.
// Bù bằng nâng vai thêm BIRD_UP (độ) — giữ hình chim (cổ tay bắt chéo, ngón cái đầu chim) và nhịp vỗ; đo tâm lòng tay trước/sau ở báo cáo.
const BIRD_UP = 8;
const birdW = (p, t, hz, amp, up = BIRD_UP) => { const b = p.bird(t, hz, amp), el = 1.75 * up; return over(b, { joints: { shoulder_L: [b.joints.shoulder_L[0] - up, b.joints.shoulder_L[1], b.joints.shoulder_L[2]], shoulder_R: [b.joints.shoulder_R[0] - up, b.joints.shoulder_R[1], b.joints.shoulder_R[2]],
  elbow_L: [b.joints.elbow_L[0] + el, 0, 0], elbow_R: [b.joints.elbow_R[0] + el, 0, 0] } }); };   // vai nâng thêm `up`°, khuỷu duỗi thêm 1,75·up° → tay lên cao, tách chim khỏi bóng đầu
wallShot('s25', 68.0, 73.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'dolly vào rất chậm (0,3 m)',
  why: 'Giới thiệu Cas bằng việc cậu làm: chim bóng từ đèn khí L11 (khung style frame b_cas_bird).', sound: 'lửa thở; vải sột soạt; im',
  light: 'đèn khí L11 (key, có bóng) — cột điện cạnh tường còn tắt', action: 'Cas giơ hai tay làm chim; chim vỗ cánh chậm trên tường vôi.' },
  (p, cam, ctx, dbg = {}) => ({ exposure: 3.6, update(t, T, { ida, cas }) { cas.place(birdW(p, t, 1.0, 1, dbg.birdUp), ...CAS_W, CAS_YAW); ida.place(idaWatch(p, T), ...IDA_W, yawTo(...IDA_W, ...CAS_W));   // B1: L11 cách tường chim 7 m → tường tối hơn, phơi sáng 2,6 → 3,6
    camAt(cam, [[0, BIRD_CAM[0], BIRD_CAM[1]], [5, [2.0 + DX, 1.3, 3.3], BIRD_CAM[1]]], t); } }));
wallShot('s26', 73.0, 76.0, { size: 'MS', angle: 'ngang mắt, 3/4 trước-phải Ida (máy phía +x đường Ida–Cas)', mm: 50, move: 'tĩnh', idaExpr: 'neutral', idaDetail: 32, idaGlint: 0.02, faceLight: 'gas',
  why: 'Ida xuống thang, đứng xem, không gọi. Đèn lồng ở thắt lưng vẫn cháy (gieo cho 1:26). V4: mặt bà đọc được — ngọn L11 ở trước-phải bà là key thật; sau lưng bà là đầu phố Ostler đã trắng (chiều sâu).', sound: 'lửa thở',
  light: 'đèn khí L11 (key trước mặt bà, ngẩng ≈ 25°); đèn lồng thắt lưng (rất yếu); nền: mặt tiền phố chính đã trắng', action: 'Ida đứng cách cột L11 vài bước, nhìn Cas (phải khung).' },
  (p, cam, ctx, dbg) => { const ip = dbg.ip || IDA_W; return { exposure: 3.4, update(t, T, { ida, cas }) { cas.place(birdW(p, t + 5, 1.0, 1), ...CAS_W, CAS_YAW);
    ida.place(idaWatch(p, T), ...ip, yawTo(...ip, ...CAS_W)); const h = wpos(ida.joints.head);
    cam.position.set(...(dbg.cp || [-2.1, 1.5, 6.55])); cam.lookAt(h.x + 0.05, h.y - 0.04, h.z); return { lantern: dbg.lk ?? 0.012 }; } }; });
wallShot('s27', 76.0, 80.0, { size: 'WS', angle: 'thấp, sau-phải, hất lên', mm: 21, move: 'tĩnh', paintP: PAINT_STREET,
  why: 'Cột điện PHỐ CHÍNH cạnh góc nhà kho bật: bóng đèn thấy trong khung, nhấp hai lần rồi đứng trắng trên nền trời đêm có sao. Trắng phủ tường; chim nhạt dần trong ~11 khung (luật 3.3) — tay vẫn còn, chỉ mất bóng. V3: thấy cả nhà kho (gờ mái, cửa sổ cao, cửa kéo hàng, hốc cửa bên phải), góc nhà + ngõ cong bên trái, mái xa sau nhà kho.',
  sound: 'rơ-le "tách"; bóng đèn rít; rè điện', light: 'cột điện cạnh tường bật — trắng phẳng; đèn khí L11 còn nhưng chìm',
  action: 'Bóng đèn điện bật; chim bóng xám dần rồi mất; tay Cas vẫn vỗ. Ida đứng xem ở trái khung.' },
  (p, cam, ctx, dbg) => ({ exposure: (t, T) => 3.6 - 2.5 * switchOn(T, WALL_POST_ON), update(t, T, { ida, cas }) { cas.place(birdW(p, t + 8, 1.0, 1), ...CAS_W, CAS_YAW);
    ida.place(idaWatch(p, T), ...IDA_W, yawTo(...IDA_W, ...CAS_W)); cam.position.set(...(dbg.cp || [-1.0, 0.85, 13.0])); cam.lookAt(...(dbg.cl || [1.2, 3.0, 1.0])); } }));   // B1: máy từ vỉa hè nam: Ida (trái), L11 + thang, Cas, cột trong sân (phải)
wallShot('s28', 80.0, 83.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'tĩnh',
  why: 'Cas vỗ mạnh hơn vào bức tường trống — không gì cả (luật 3.3: key : tràn ≈ 1 : 1, không còn bóng).', sound: 'rè điện; vải', light: 'trắng phẳng',
  action: 'Cas vỗ tay nhanh, mạnh; tường trắng trơn.' },
  (p, cam, ctx, dbg = {}) => ({ exposure: 1.0, update(t, T, { ida, cas }) { cas.place(birdW(p, t, 2.1, 1.8, dbg.birdUp), ...CAS_W, CAS_YAW); ida.place(idaWatch(p, T), ...IDA_W, yawTo(...IDA_W, ...CAS_W)); cam.position.set(...BIRD_CAM[0]); cam.lookAt(...BIRD_CAM[1]); } }));
wallShot('s29', 83.0, 86.0, { size: 'MCU', angle: 'ngang mắt Cas, 3/4 trước-phải', mm: 85, move: 'tĩnh', casDetail: 36,
  why: 'Cas hạ tay, quay lại, thấy bà — rồi thấy đèn lồng hổ phách ở thắt lưng bà. Cậu không xin.', sound: 'rè điện; im',
  light: 'trắng phẳng; phản ánh ấm rất nhẹ của đèn lồng', action: 'Cas hạ tay, xoay người về phía Ida (trái khung), nhìn xuống đèn lồng.' },
  (p, cam) => ({ exposure: 1.0, update(t, T, { ida, cas }) {
    const yaw = valAt([[0, CAS_YAW], [0.9, CAS_YAW], [1.9, yawTo(...CAS_W, ...IDA_W)]], t);
    cas.place(settle(poseAt([[0, birdW(p, 0, 1, 1)], [0.8, p.C.turnaround], [2.0, over(p.C.turnaround, { joints: { neck: [16, 0, 0] } })]], t), T, { side: -1, k: ease((t - 0.8) / 1.2) * 0.6, br: 3.0 }), ...CAS_W, yaw);   // Cổng 6 (e): hạ tay xong thì dồn chân, thở
    ida.place(idaWatch(p, T), ...IDA_W, yawTo(...IDA_W, ...CAS_W));
    cam.position.set(1.7 + DX, 1.1, 2.8); cam.lookAt(0.1 + DX, 1.05, 1.0); } }));
// s30 → s32: Ida tới đứng bên trái Cas (cắt nén thời gian), tháo đèn lồng, quỳ một gối; đèn lồng hạ xuống dưới hai cánh tay cậu, cách tường 0,62 m.
const IDA_K = [-0.75 + DX, 0.75], kneelYaw = yawTo(-0.75 + DX, 0.75, LAN_T[0], LAN_T[2]);
// Tư thế cục bộ (không có trong sheet): quỳ một gối (crouch_lantern) + tay phải đưa đèn lồng ra trước, ngang hông cậu bé.
const kneelHold = (p, ctx, o = {}) => kneelOf(p, ctx, { joints: { spine: [8, 0, 0], shoulder_R: [-88, 0, -6], elbow_R: [-6, 0, 0], ...(o.joints || {}) } });
wallShot('s30', 86.0, 88.0, { size: 'MS', angle: 'ngang, sau-phải', mm: 35, move: 'tĩnh', idaDetail: 28,
  why: 'Ida tháo đèn lồng, quỳ cạnh cậu, cầm thấp sau tay cậu, cách tường một sải tay (≤ 0,7 m — luật 3.3).', sound: 'kim loại quai đèn; vải',
  light: 'đèn lồng tới gần tường (ấm) trong nền trắng', action: 'Ida tháo đèn lồng, quỳ một gối bên trái Cas; đèn lồng hạ xuống dưới hai cánh tay cậu.' },
  (p, cam, ctx) => { const kn = kneelHold(p, ctx); const standL = over(p.stand, { props: ['lantern_hand_R'], joints: { shoulder_R: [-20, 0, -10] } });
    return { exposure: 1.0, update(t, T, { ida, cas }) {
    cas.place(settle(over(p.C.turnaround, { joints: { neck: [22, 0, 0] } }), T, { side: -1, k: 0.6, br: 3.0 }), ...CAS_W, yawTo(...CAS_W, ...IDA_K));
    const pose = t < 0.7 ? over(walkPose(t, p.stand), { props: ['lantern_belt'] }) : poseAt([[0.7, over(p.stand, { joints: { neck: [10, 0, 0] } })], [0.95, standL], [1.05, standL], [1.85, kn]], t);
    ida.place(pose, valAt([[0, -1.3 + DX], [0.7, IDA_K[0]]], t), valAt([[0, 1.85], [0.7, IDA_K[1]]], t), valAt([[0, yawTo(-1.3 + DX, 1.85, ...IDA_K)], [0.7, yawTo(-1.3 + DX, 1.85, ...IDA_K)], [1.3, kneelYaw]], t));
    if (t > 1.2) { const lan = ida.props.lantern; if (lan && lan.parent) { const k = ease((t - 1.2) / 0.65); lan.updateMatrixWorld(true); const a = wpos(lan.userData.lightAnchor); lanternTo(ida, [a.x + (LAN_T[0] - a.x) * k, 0, a.z + (LAN_T[2] - a.z) * k]); } }
    cam.position.set(2.6 + DX, 1.4, 4.0); cam.lookAt(-0.1 + DX, 0.8, 0.7); return { lantern: 0.012 + (LAN_K - 0.012) * ease((t - 0.8) / 1.05) }; } }; });   // v3 (N6): đèn cháy liên tục — không có nhịp 'mở cửa'; hắt sáng lớn dần LIÊN TỤC khi đèn ra khỏi thân bà (0,8 s) và hạ sát tường (1,85 s), không bật cóc
wallShot('s31', 88.0, 91.0, { size: 'MCU', angle: 'ngang mắt Ida (quỳ), 3/4 trước-phải, qua vai phải Cas', mm: 85, move: 'tĩnh', idaExpr: 'sad_smile', idaDetail: 36,
  why: 'Lời mời, không dạy: bà đưa ánh sáng, cậu tự làm.', sound: 'THOẠI L3 "Go on, then." (đầu s31, 1:14,0 — DIALOGUE.L3)',
  light: 'đèn lồng ấm dưới mặt bà (≈ 0,6 m); trắng phẳng từ trên', action: 'Ida quỳ, đèn lồng thấp trong tay phải, quay đầu về Cas, nói L3.' },
  (p, cam, ctx, dbg) => { const kn = kneelHold(p, ctx, { joints: { neck: [-8, -24, 0] } }); let H0 = null, face = null; return { exposure: 0.45, update(t, T, { ida, cas }) {   // C2: bảng phơi sáng cận mặt W3 (cháy mặt 21 % → ~1 %)
    cas.place(settle(over(p.C.turnaround, { joints: { neck: [22, 0, 0] } }), T, { side: -1, k: 0.5, br: 3.0 }), ...CAS_W, yawTo(...CAS_W, ...IDA_K));
    if (!H0) { ida.place(kn, ...IDA_K, kneelYaw); lanternTo(ida, LAN_T); H0 = wpos(ida.joints.head); H0.y += 0.1; face = faceRig(ida); }   // máy tĩnh: theo đầu ở tư thế gốc (không bám gật đầu)
    // Cổng 6 (c): L3 "Go on, then." (74,05–75,25) — khẩu hình 6 viseme; trước lời: dịu, mày trong hơi nâng; sau lời: cười buồn nhẹ (lời mời), mắt hạ xuống tay cậu, gật nhẹ ở "then".
    const L3 = DIALOGUE.L3, b = Math.sin(2 * Math.PI * T / 4.0);
    ida.place(addJ(kn, { neck: [valAt([[L3 + 0.5, 0], [L3 + 0.8, 4], [L3 + 1.3, 1], [L3 + 2.2, 3]], T) - 0.4 * b, 0, 0], spine: [0.8 * b, 0, 0] }), ...IDA_K, kneelYaw); lanternTo(ida, LAN_T);
    face(mixW(wAt([[L3 - 0.2, { browInnerUp: 0.3, smile: 0.15 }], [L3 + 1.2, { browInnerUp: 0.35, smile: 0.3 }], [L3 + 1.7, { ...X_SADSMILE, smile: 0.7, lidDrop: 0.3 }], [L3 + 3.0, { ...X_SADSMILE, smile: 0.6, lidDrop: 0.35 }]], T),
      mouthAt(lipKeys(LIP_L3, L3), T, ida.VISEMES || {}, 0.65), { blink: blinkAt(T, [L3 + 1.45, [L3 + 2.6, 1.6]]) }), valAt([[L3, [0, 0.02]], [L3 + 1.3, [0, 0.03]], [L3 + 1.8, [0, 0.16]], [L3 + 3, [0, 0.15]]], T));
    const h = H0; const o = dbg.co || [1.6, 0.05, 1.25]; cam.position.set(h.x + o[0], h.y + o[1], h.z + o[2]); cam.lookAt(h.x, h.y - 0.02, h.z); return { lantern: LAN_K }; } }; });
wallShot('s32', 91.0, 94.0, { size: 'WS', angle: 'ngang, sau-phải', mm: 35, move: 'tĩnh',
  why: 'Chim trở lại, TO hơn, ấm, rìa mềm (tay gần nguồn — luật 3.2, 3.3) và bay.', sound: 'Cas cười khẽ (chờ SFX có giấy phép — để trống); nhạc tạm vào',
  light: 'đèn lồng thấp dưới tay Cas, cách tường 0,62 m (key ấm, có bóng) trong nền trắng', action: 'Cas giơ tay vào quầng hổ phách; chim to hiện cao trên tường và bay.' },
  (p, cam, ctx, dbg) => { const kn = kneelHold(p, ctx, { joints: { neck: [-14, -10, 0] } }); return { exposure: 1.0, update(t, T, { ida, cas }) {
    const bird = p.bird(t, 1.2); const sw = Math.sin(t * 0.9) * 10;
    const cz = valAt([[0, CAS_W[1]], [0.2, CAS_W[1]], [0.9, CAS_S32[1]]], t);
    cas.place(poseAt([[0, settle(over(p.C.turnaround, { joints: { neck: [22, 0, 0] } }), T, { side: -1, k: 0.6, br: 3.0 })], [0.8, over(birdReach(bird), { joints: { spine: [-4, sw, 0] } })]], t), CAS_W[0], cz, valAt([[0, yawTo(...CAS_W, ...IDA_K)], [0.7, CAS_YAW]], t));
    ida.place(kn, ...IDA_K, kneelYaw); lanternTo(ida, LAN_T); cam.position.set(...(dbg.cp || [1.9 + DX, 1.35, 4.1])); cam.lookAt(...(dbg.cl || [-0.25 + DX, 1.45, 0])); return { lantern: dbg.lk ?? LAN_K }; } }; });

// ---------------- CẢNH 5 — Ngọn cuối ----------------
// V2 (1:20–1:29, s33–s34): bản v2 để Cas SÁT vách (0,45 m) → bóng cậu ×1,18 gần bằng người, rìa sắc, đứng ngay sau lưng cậu → AI mù đọc "hai cậu bé".
// Sửa bằng quang học thật (luật 3.2, 3.5): phóng đại = (đèn → vách) ÷ (đèn → người). Đèn lồng đặt cách vách 3,0 m, lệch trái 0,3 m (x = −0,3),
// hai người đứng tách ra hai bên đèn → bóng mỗi người bị đẩy RA NGOÀI, lệch khỏi chính người đó (độ lệch = (x_người − x_đèn) × (phóng đại − 1)):
//   Ida (x −0,7) cách vách 1,6 m (đèn → bà 1,4 m) → ×2,14: bóng cao ≈ 3,5 m, tâm bóng x ≈ −1,16 — lệch TRÁI bà 0,46 m;
//   Cas (x 0,62) cách vách 0,9 m (đèn → cậu 2,1 m) → ×1,43: bóng ≈ 1,9 m (to hơn cậu, rìa mềm hơn), tâm bóng x ≈ 1,02 — lệch PHẢI cậu 0,40 m.
//   Hai bóng: bà ≈ 3,5 m, cậu ≈ 1,9 m ("hers, tall… his, small") — tỷ lệ 1,87; giữa hai bóng là khoảng vách sáng. Viền sáng trên người: dội vách bên (uSide) + đèn lồng sau lưng.
const BAY = { lan: [0.2, 3.0], ida: [-0.62, 1.45], cas: [0.9, 0.8] };
// Rà continuity v2 (N3): đèn lồng dời sang phải (x 0,2), Cas x 0,9 → bóng Ida lệch trái bà 0,77 m (tâm x ≈ −1,39; vành mũ của bóng ra khỏi người), bóng Cas lệch phải 0,25 m.
// Cổng 5 (continuity N3): Ida 1,45 m trước vách (đèn → bà 1,55 m) ×1,94 → đỉnh bóng ≈ 3,2 m, NẰM TRONG vùng vách được đèn rọi (nắp chắn > 49° ≈ 3,55 m) nên vành mũ của bóng đọc được;
// bóng lệch trái bà 0,53 m. Cas 0,8 m trước vách (đèn → cậu 2,2 m) ×1,36 → bóng ≈ 1,8 m, lệch phải cậu 0,29 m. Tỷ lệ bóng bà / bóng cậu 1,77.
// Độ mềm: đèn lồng là nguồn ~12 cm; ở render 1 mẫu, vùng nửa tối giả lập bằng PCF (shadow.radius 4) — ở render nhiều mẫu là jitter nguồn thật của s5.
// s34 lấy cả nền đá: vệt bóng trên nền nối chân mỗi người với bóng của chính họ trên vách (dấu hiệu 'bóng của ai').
function placeBayLantern(r, x, z) {   // dời đèn lồng + nguồn sáng (spot có bóng, omni bù trong shader, quầng sprite) — cùng một nguồn điểm
  const old = r.flameP.clone(); r.lan.position.x = x; r.lan.position.z = z; r.lan.updateMatrixWorld(true);
  r.lan.userData.lightAnchor.getWorldPosition(r.flameP);   // sửa tại chỗ: onSample của s5 giữ tham chiếu tới chính vectơ này
  const d = r.flameP.clone().sub(old); r.scene.traverse((o) => { if (o.isSprite && o.position.distanceTo(old) < 0.6) o.position.add(d); });
  r.spot.position.copy(r.flameP); U.uLP.value.copy(r.flameP); U.uLDir.value.copy(r.spot.target.position).sub(r.flameP).normalize(); r.spot.updateMatrixWorld();
}
S({ id: 's33', scene: 5, size: 'WS', angle: 'ngang 1,35 m, "tranh trong tranh"', mm: 32, move: 'dolly vào 0,9 m + dịch ngang trái 0,4 m (thị sai người/bóng)',
  why: 'Hình trung tâm (7A, khung style frame c_s5_wide): trong hốc cửa khuất điện, đèn lồng dưới đất; Ida dừng gần đèn nên bóng bà vươn CAO (×1,94), lệch trái bà 0,77 m; Cas đi tới gần vách nên bóng cậu NHỎ hơn bóng bà (×1,36), lệch sang phải cậu — người và bóng tách nhau. Ngoài vòm: góc phố TỐI lạnh (P5 chưa bật, C5) — hổ phách trong hốc đối với đêm lạnh ngoài.',
  sound: 'nhạc tạm; bước chân vào hốc; rè điện xa', light: 'đèn lồng trên nền đá (nguồn thấp, có bóng); ngoài vòm: góc tối — chỉ hổ phách L11 từ phải + tràn điện xa 0,05 (P5 chưa bật)',
  action: 'Ida đặt đèn lồng, hai người bước vào; Ida dừng giữa hốc, Cas đi tới gần vách; hai bóng một cao một nhỏ.',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}, { l11On: true, dark: true }); const p = P(ctx); const dbg = ctx.dbg || {}; const cam = r.cam; const c0 = cam.position.clone(); [r.chIda, r.chCas].forEach((c) => tameGlint(c));
    for (const ch of [r.chIda, r.chCas]) { ch.sheetRef = ch.sheet; }
    const B = { ...BAY, ...(dbg.bay || {}) }; placeBayLantern(r, ...B.lan); r.spot.shadow.radius = dbg.pcf ?? 4;
    const keep = () => { if (!r.lan.parent) r.scene.add(r.lan); };
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT, grade: GRADE_S5, exposure: dbg.exp ?? 1.5,
      update(t) {
        // (a) s33 rút 7,0 → 5,0 s: đứng dậy 0–0,6 s, Ida đi 0,6–2,7 s, Cas đi 0,6–4,1 s (3,1 m, 0,88 m/s), tư thế cuối 3,6 / 4,6 s.
        const zI = valAt([[0, 3.5], [0.6, 3.5], [2.7, B.ida[1]]], t), zC = valAt([[0, 3.9], [0.6, 3.9], [4.1, B.cas[1]]], t);
        const pI = t < 0.6 ? lerpPose(p.crouch, p.stand, ease(t / 0.6)) : t < 2.7 ? over(walkPose(t - 0.6, p.stand), { props: [] }) : poseAt([[2.7, over(p.stand, { props: [] })], [3.6, over(p.lookShadows, { props: [] })]], t);
        const pC = t < 0.6 ? p.C.turnaround : t < 4.1 ? walkPose(t - 0.6, p.C.turnaround, { gait: WALK_CHILD, bothArms: true }) : poseAt([[4.1, p.C.turnaround], [4.6, p.C.half_raised]], t);
        rootFirst(r.chIda, B.ida[0], pI.root_y_m ?? 0, zI, Math.PI + 0.30 * clamp01((t - 2.5) / 0.8)); r.chIda.setPose({ ...pI, props: [] }); keep(); r.chIda.root.position.set(B.ida[0], pI.root_y_m ?? 0, zI); r.chIda.root.updateMatrixWorld(true);
        rootFirst(r.chCas, B.cas[0], pC.root_y_m ?? 0, zC, Math.PI - 0.25 * clamp01((t - 3.9) / 0.7)); r.chCas.setPose(pC); keep(); r.chCas.root.position.set(B.cas[0], pC.root_y_m ?? 0, zC); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) { ctx.upd(r.chIda, cam); ctx.upd(r.chCas, cam); }
        // (a) thị sai: dolly vào 0,9 m + dịch ngang 0,4 m sang trái → người (cách máy ~8 m) trượt khỏi bóng của họ trên vách (~9 m).
        cam.position.copy(c0).add(new THREE.Vector3(-0.4 * ease(t / 5), 0, -0.9 * ease(t / 5))); } };   // dịch ngang TRÁI 0,4 m: Ida (gần máy hơn vách) trượt sang phải, xa khỏi bóng của bà
  } });

S({ id: 's34', scene: 5, size: 'MS (nghiêng)', angle: 'ngang ngực, từ phía phải, sau đèn lồng, thấy cả nền đá', mm: 26, move: 'tĩnh',
  why: 'Ida ngửa nhìn bóng mình cao vút; bên phải, Cas đứng trước vách, bóng cậu (to hơn cậu, mềm hơn) lệch sang phải cậu — trái → phải: Ida, bóng Ida, Cas, bóng Cas; người có màu và viền sáng, bóng phẳng và tối (V2).',
  sound: 'lửa thở; nhạc tạm', light: 'đèn lồng dưới đất sau lưng hai người (key thấp, có bóng); viền má và mép mũ; dội ấm vách bên',
  action: 'Ida ngửa nhìn bóng, tay đặt lên ngực; Cas giơ nửa tay nhìn bóng mình.',
  async build(ctx) {
    const dbg = ctx.dbg || {};
    const r = await buildBaySet(ctx, { medium: { pos: dbg.cp || [1.35, 1.15, 4.0], look: dbg.cl || [-0.2, 1.35, 0.4], fov: fovOf(dbg.mm ?? 26) } }, { l11On: true, dark: true }); r.spot.shadow.radius = dbg.pcf ?? 4; [r.chIda, r.chCas].forEach((c) => tameGlint(c)); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    const B = { ...BAY, ...(dbg.bay || {}) }; placeBayLantern(r, ...B.lan);
    r.chIda.root.position.set(B.ida[0], 0, B.ida[1]); r.chCas.root.position.set(B.cas[0], 0, B.cas[1]); for (const ch of [r.chIda, r.chCas]) ch.root.updateMatrixWorld(true);
    return { scene: r.scene, cam: r.cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: dbg.exp ?? 1.5, update() {} };
  } });

// Bộ phố cuối (góc ngọn 11): cột góc (POST_ON[5], đoạn cáp cuối) tắt tới giữa câu L4 → góc chỉ có hổ phách + bóng dài; sau đó trắng tràn.
// Cuối phố (V3): sets_end.buildStreetEnd — nhà kho chữ L: mặt cuối phố x = −5 (phố rẽ trái sau góc nam z = +2), hông nam z = −8,1 = tường chim + hốc cửa (x = 2,2).
// B1: cột điện phố chính trong sân (sets_end) SÁNG suốt cảnh 5 (bật từ 1:04,4); ẩn bản cột cũ W1 dựng ở (13,5; −4,2) nếu còn (st.wallPost) — tránh hai cột.
// (b) L11 sau khi tắt: kính trống TỐI (độ đục 0,85, xám đen) — bản kính mờ 0,5 trên nền tường trắng đọc thành 'còn sáng'.
function endStreet(o = {}) {
  const st = buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: o.shadowLamps || [] });
  if (st.wallPost) { st.wallPost.E.group.visible = false; st.wallPost.gl.visible = false; for (const g of st.wallPost.gz.list) g.visible = false; st.wallPost.L.visible = false; }
  const set0 = st.setState, l11 = st.lamps[10];
  st.setState = (s, f) => { set0(s, f); st.endInfo?.wallPost?.set(1); if (l11 && (s.gas(11) ?? 0) <= 0.01) { l11.glassM.color.set('#16181f'); l11.glassM.opacity = 0.85; } };
  return st;
}
const cornerFill = (T) => 0.06 + 1.04 * switchOn(T, POST_ON[5]);
// Mũ Ida: từ s36 (C4, bà tự đẩy vành) tới hết cảnh 5 giữ hat_back = 0,35 (= faceRest) — liên tục qua s37w … s42.
const HB = 0.35;
// Cas giữ thang — Cổng 6 (G10, tay MPFB): bản Cổng 5 để Cas đứng SAU chân thang (8,0; −4,98), đúng lối bà trèo lên/xuống (bà ở mặt dưới thang, −z) → bà xuống thang ở s40w
// sẽ xuyên qua cậu. Nay cậu đứng CẠNH chân thang phía đông (+x, phía phố) (8,40; −4,62), HAI TAY NẮM THANH DỌC phía đông (tay phải cao 1,00 m, tay trái 0,74 m; tầm với ≤ 0,31 m)
// bằng IK tay MPFB (reachGrip) — thang được giữ, lối trèo trống.
const CAS_LAD = [8.4, -4.62], CAS_LYAW = -0.6;   // mặt về +z lệch về thang (−x) 34°: hai tay trước-phải, cùng nắm thanh đông
// Nắm thanh dọc thang (hộp 0,027 × 0,041 m ≈ trụ bán kính 0,018 m) ở độ cao THẾ GIỚI y; xs = +1 thanh đông (x 8,17), −1 thanh tây. Trả khoảng cách lòng tay → mặt thanh (m).
function railG(lad, xs, y) { lad.updateMatrixWorld(true); const up = new THREE.Vector3(0, 1, 0).transformDirection(lad.matrixWorld); const o = lad.localToWorld(new THREE.Vector3(xs * 0.17, 0, 0));
  return { point: o.addScaledVector(up, (y - o.y) / up.y).toArray(), axis: up.toArray(), radius: 0.018 }; }
// IK nắm có trộn: k = 0 giữ tư thế FK, 1 = nắm hẳn (slerp khớp vai–khuỷu–cổ tay) → vào/ra nắm mượt, không bật cóc.
function gripK(ch, s, g, k = 1, at = false) {
  if (k <= 0 || !ch.reachGrip) return null; const J = ['shoulder_', 'elbow_', 'wrist_'].map((n) => ch.joints[n + s]), q0 = J.map((j) => j.quaternion.clone());
  const e = at ? gripAt(ch, s, g) : ch.reachGrip(s, g); if (k >= 1) return e;
  J.forEach((j, i) => { const q1 = j.quaternion.clone(); j.quaternion.copy(q0[i]).slerp(q1, k); }); ch.root.updateMatrixWorld(true); ch.cpuSkin?.update();
  if (ch.handsBL) { for (const x of ['L', 'R']) ch.handsBL.sides[x].key = ''; ch.root.updateMatrixWorld(true); } return e;
}
// PRE_GRIP: khoảng cách tâm lòng tay → mặt vật ở tư thế FK (trước IK) của lần gọi gần nhất — chỉ để ghi số đo (báo cáo), không ảnh hưởng hình.
const PRE_GRIP = {}; const toLine = (P, g) => { const C = new THREE.Vector3(...g.point), A = new THREE.Vector3(...g.axis).normalize(), d = P.clone().sub(C); d.addScaledVector(A, -d.dot(A)); return +(d.length() - g.radius).toFixed(4); };
const casHold = (cas, lad, k = 1) => { const gL = railG(lad, 1, 0.74), gR = railG(lad, 1, 1.0); PRE_GRIP.cas = [toLine(cas.gripPoint('L'), gL), toLine(cas.gripPoint('R'), gR)]; return [gripK(cas, 'L', gL, k), gripK(cas, 'R', gR, k)]; };
const casLadPose = (p, T, neck = -30) => settle(over(p.C.hold_ladder, { joints: { neck: [neck, 0, 0] } }), T, { side: -1, k: 0.5, br: 3.0 });
const FAST_CHILD = { cycle_s: 0.7, stride_m: 0.5, speed_mps: 1.43 };
S({ id: 's35', scene: 5, size: 'WS', angle: 'ngang, xuôi dốc', mm: 28, move: 'tĩnh',
  why: 'Góc ngọn cuối vẫn TỐI (đoạn cáp cuối chưa bật): ngọn L11 là nguồn duy nhất, bóng dài. Bà đi ra từ phía hốc cửa (cuối phố, nền), tới thang, trèo lên lần cuối; Cas chạy theo giữ thang bằng hai tay. V3: cuối phố là nhà kho + hốc cửa + ngõ cong, không còn tường trống.', sound: 'bước chân; thang; rè điện xa',
  light: 'đèn khí L11 (ấm, có bóng); phố trắng ở xa sau lưng máy', action: 'Ida đi dọc mặt tiền phía bắc tới chân thang, trèo; Cas chạy theo giữ thang.',
  async build(ctx) {
    const st = endStreet({ shadowLamps: [11] }); const p = P(ctx); const lad = ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(28); cam.position.set(16.5, 1.7, 2.6); cam.lookAt(5.5, 2.3, -3.8);
    const I0 = [5.7, -6.2], C0 = [3.6, -4.6];   // bà đi ra từ phía hốc cửa (hông nhà kho, trái khung), cậu chạy theo
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: expo(2.4, 1.15, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f);
        if (t < 2.3) ida.place(over(walkPose(t, p.stand), { props: ['lantern_belt'] }), valAt([[0, I0[0]], [2.3, LAMP_X(11)]], t), valAt([[0, I0[1]], [2.3, FOOT_Z]], t), yawTo(...I0, LAMP_X(11), FOOT_Z));
        else if (t < 3.4) { const u = (t - 2.3) / 1.1; ida.place(p.climb(u, p.restLadder), LAMP_X(11), FOOT_Z + (ON_Z1 - FOOT_Z) * ease(u), 0); } else ida.place(p.restLadder, LAMP_X(11), ON_Z1, 0);
        if (t < 3.0) cas.place(walkPose(t, p.C.turnaround, { gait: FAST_CHILD, bothArms: true }), valAt([[0, C0[0]], [3.0, CAS_LAD[0]]], t), valAt([[0, C0[1]], [3.0, CAS_LAD[1]]], t), yawTo(...C0, ...CAS_LAD));
        else { cas.place(poseAt([[3.0, p.C.turnaround], [3.6, casLadPose(p, T)]], t), ...CAS_LAD, valAt([[3.0, yawTo(...C0, ...CAS_LAD)], [3.5, CAS_LYAW]], t)); casHold(cas, lad, ease((t - 3.05) / 0.55)); } } };   // Cổng 6: cậu tới cạnh chân thang phía đông, hai tay nắm thanh (IK)
  } });

// ---------- PA1 — "Nghiêng dưới ngọn lửa" (Cổng 6, chủ dự án chọn PA1; KHÔNG cận mặt chính diện ở cao trào) ----------
// Máy ở phía +x (phía phố, cùng phía máy s37w/s38/s40w/s41 → giữ trục 180° cảnh 5: Ida TRÁI, Cas PHẢI; bà nhìn sang TRÁI khung, cùng hướng màn hình với s37w).
// Góc máy đo so với hướng MẶT (đầu) của bà: s36 60° (3/4, đẩy vành mũ) · s37 90° MS 50 mm · s37b 90° CU 85 mm đẩy chậm · s39 96° CU (nghiêng hơi mất mặt).
// Ngọn L11 GỐC của layout (không đổi đèn) nằm ngay trước mũi bà → trong khung là đèn chính NGANG–TRƯỚC. Máy TĨNH thật: tính một lần từ tư thế gốc của shot
// (không bám đầu đang gật/cúi) — hàm thuần theo t. Tay TRÁI (phía máy) NẮM THÂN VAN đồng bằng tay MPFB (reachGrip) → van không lộ thành "mẩu tay"; tay phải thả lỏng
// phía xa, thân bà che (không đặt lên cột phía sau: lời chê "mẩu tay sau cột" của PA1 cũ).
const ON_Z1 = ON_Z + 0.1;   // bà đứng nhích sát cột 0,1 m trên thang (tầm với tới van: vai → thân van ≈ 0,5 m, trong tầm tay 0,61 m)
function valveOf(st) { const v = st.lamps[10].lamp.userData.parts.valve; v.updateMatrixWorld(true); const a = v.localToWorld(new THREE.Vector3(0, -0.02, 0)), b = v.localToWorld(new THREE.Vector3(0, 0.02, 0));
  return { point: a.clone().lerp(b, 0.5).toArray(), axis: b.sub(a).normalize().toArray(), radius: 0.028 }; }
// Tư thế gốc trên thang cho PA1: faceRest (mũ 0,35, cổ quay về phố) + thở. nodX: gật/cúi thêm; turn: quay cổ.
const idaTop = (p, T, { hb = HB, turn = 35, nodX = 0, arms = {} } = {}) => { const b = Math.sin(2 * Math.PI * T / 4.2);
  const base = p.faceRest(hb, turn); return addJ(over(base, { joints: arms, hands: { L: { spread: 0.1, curl: 0.8 }, R: { spread: 0.1, curl: 0.45 } } }), { spine: [0.7 * b, 0, 0], neck: [nodX - 0.3 * b, 0, 0], shoulder_L: [0, 0, 0.6 * b], shoulder_R: [0, 0, -0.6 * b] }); };
const pa1Shot = (id, meta) => S({ id, scene: 5, size: meta.size, angle: meta.angle, mm: meta.mm, move: meta.move, why: meta.why, sound: meta.sound, light: meta.light, action: meta.action,
  async build(ctx) {
    const dbg = ctx.dbg || {}; const st = endStreet({ shadowLamps: (dbg.shadow ?? 1) ? [11] : [] }); const p = P(ctx); ladderAt(st.scene, 11);   // C2: L11 đổ bóng (bóng vành mũ thật trên mặt)
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'neutral', gaze: [0, 0], glint: 0.45 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(meta.mm); const fl = createFaceLight(st.scene, { mode: meta.fl || 'gas' }); const EK = dbg.ek ?? meta.ek ?? 1.0;
    const face = faceRig(ida), TR = IDA5(DIALOGUE.L4), V = ida.VISEMES || {}, VG = valveOf(st);
    let C = null;   // máy tĩnh: mắt + hướng tính MỘT lần từ tư thế gốc (không phụ thuộc khung trước — cùng kết quả ở mọi khung)
    const camBase = () => { ida.place(meta.pose(p, meta.T0 ?? 0, 0), LAMP_X(11), ON_Z1, 0); const head = wpos(ida.joints.head); head.y += 0.12;
      const q = ida.joints.head.getWorldQuaternion(new THREE.Quaternion()); const fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q); fw.y = 0; fw.normalize();
      const eye = head.clone().addScaledVector(fw, 0.08); eye.y += dbg.cy ?? meta.cy ?? -0.05; return { eye, dir: fw.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), (dbg.yaw ?? meta.yaw) * Math.PI / 180) }; };
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: dbg.exp ?? (() => fl.exposure() * EK),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); cas.place(casLadPose(p, T), ...CAS_LAD, CAS_LYAW);
        if (!C) C = camBase();
        const dist = typeof meta.dist === 'function' ? meta.dist(t) : meta.dist; cam.fov = fovOf(dbg.mm ?? meta.mm); cam.updateProjectionMatrix();
        cam.position.copy(C.eye).addScaledVector(C.dir, dbg.dist ?? dist); cam.position.y += meta.drop ?? 0; cam.lookAt(C.eye.x, C.eye.y + (meta.lookDy ?? 0), C.eye.z);
        ida.place(meta.pose(p, T, t), LAMP_X(11), ON_Z1, 0);
        const preL = +(ida.gripPoint('L').distanceTo(new THREE.Vector3(...VG.point)) - VG.radius).toFixed(4);
        const gL = meta.valve === false ? null : meta.valveK ? gripK(ida, 'L', VG, meta.valveK(t), true) : gripAt(ida, 'L', VG);
        face(mixW(wAt(TR.expr, T), mouthAt(TR.lip, T, V, meta.lipAmp ?? 0.7), { blink: blinkAt(T, TR.blinks) }), valAt(TR.gaze, T));
        const fe = fl.update(ida, cam, meta.fl === 'elec' ? { keyE: st.whiteHemi.intensity } : {});
        if (dbg.log && f % 12 === 0) console.log(JSON.stringify({ id, T: +T.toFixed(2), preL_m: preL, gripL_m: gL === null ? null : +gL.toFixed(4), faceE: fe, flExp: +fl.exposure().toFixed(3) })); } };
  } });
const NOD = (T) => valAt(IDA5(DIALOGUE.L4).nod, T);
pa1Shot('s36', { size: 'MCU', angle: '3/4 nghiêng 60° (phía phố), ngang mắt', mm: 85, move: 'tĩnh', fl: 'gas', ek: 1.3, yaw: 60, dist: 1.9, T0: 1.8,
  why: 'Quyết định C4 của chủ dự án: bà TỰ đẩy vành mũ ra sau trước câu thoại — mặt thoáng ra cho lời từ biệt. PA1: 3/4 nghiêng, ngọn L11 trước mũi bà trong khung.', sound: 'vải dạ; hơi thở',
  light: 'đèn khí L11 ngay trước mặt (ấm, ngang–trước) — góc chưa có điện', action: 'Tay trái đưa lên vành mũ, đẩy vành lên, mũ ngả ra sau; tay hạ xuống nắm van (1,55–2,0 s — nối s37); nhìn ngọn lửa cuối; hít một hơi trước khi nói.', valveK: (t) => ease((t - 1.55) / 0.45),
  pose: (p, T, t) => { const b = Math.sin(2 * Math.PI * T / 4.2), hat = poseAt([[0, p.hatA], [0.35, p.hatA], [1.05, p.hatB], [1.6, p.faceRest()]], t);
    return addJ(hat, { spine: [0.7 * b + 1.2 * ease((t - 1.55) / 0.35) - 1.2 * ease((t - 1.9) / 0.1), 0, 0], neck: [-0.3 * b - 3 * ease((t - 1.5) / 0.4), 0, 0] }); } });   // 1,55–1,9 s: hít vào (ngực nâng), ngẩng nhẹ trước lời
pa1Shot('s37', { size: 'MCU', angle: 'nghiêng 90° (phía phố), ngang mắt', mm: 50, move: 'tĩnh', fl: 'gas', ek: 2.2, yaw: 90, dist: 1.35, cy: -0.02, T0: 0,
  why: 'PA1: lời từ biệt vế đầu trong hổ phách của ngọn cuối, mặt nghiêng, lửa trong khung. Sau "then." bà cười buồn, mắt chùng xuống, dừng một nhịp.', sound: 'THOẠI L4 "That\'s the last one, then."',
  light: 'đèn khí L11 trong khung, ngang–trước mặt — góc chưa có điện', action: 'Tay trái nắm van; nói "That\'s the last one, then."; cười buồn, mắt nhìn xuống, lặng một nhịp.',
  pose: (p, T) => idaTop(p, T, { nodX: NOD(T) }) });
pa1Shot('s37b', { size: 'CU', angle: 'nghiêng 90° (phía phố), ngang mắt', mm: 85, move: 'đẩy vào rất chậm (1,10 → 0,95 m)', fl: 'gas', ek: 2.0, yaw: 90, dist: (t) => valAt([[0, 1.1], [2.4, 0.95]], t), lookDy: 0.05, T0: 0,
  why: 'PA1: CU "Goodnight" đẩy vào chậm — bà ngẩng nhìn con phố lần cuối, chào, rồi cười buồn, mắt chùng, dừng.', sound: 'THOẠI L4 "Goodnight, old street."',
  light: 'đèn khí L11 viền mũi–môi–cằm — góc chưa có điện', action: 'Ngẩng nhìn phố; "Goodnight, old street."; cười buồn, mắt chùng xuống, lặng.',
  pose: (p, T) => idaTop(p, T, { nodX: NOD(T) }) });

// Toàn cảnh góc ngọn cuối (s37w, s40w): cột điện góc (đoạn cáp cuối) ở trái khung, ngọn L11 + thang ở phải khung, cuối phố (nhà kho, hốc cửa, ngõ cong) ở giữa.
const cornerWide = (id, meta, fn) => S({ id, scene: 5, size: 'WS', angle: 'ngang, từ lòng phố, hơi hất', mm: 28, move: 'tĩnh', ...meta,
  async build(ctx) {
    const st = endStreet({ shadowLamps: [11] }); const p = P(ctx); const lad = ladderAt(st.scene, 11); const dbg = ctx.dbg || {};
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 22 });
    const cam = camMM(28); cam.position.set(17.0, 1.6, 1.2); cam.lookAt(8.8, 3.6, 0.6); const VG = valveOf(st);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: expo(2.4, 1.15, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f);
        const r = fn(p, t, T, ida, { cas, lad, VG }) || {};   // Cổng 6: shot tự đặt Cas nếu cần (s40w: cậu buông thang khi bà xuống tới đất)
        if (!r.cas) { cas.place(casLadPose(p, T), ...CAS_LAD, CAS_LYAW); r.grip = casHold(cas, lad); }
        if (dbg.log && f % 12 === 0) console.log(JSON.stringify({ id, T: +T.toFixed(2), preCas_m: PRE_GRIP.cas, gripCas_m: r.grip?.map((e) => e === null ? null : +e.toFixed(4)), gripIda_m: r.gi === undefined || r.gi === null ? null : +r.gi.toFixed(4) })); } };
  } });
cornerWide('s37w', { why: 'CHỈ ĐẠO CHỦ DỰ ÁN (1:50 v1): ngay quanh "You\'ll be brighter now", bóng đèn cột góc (đoạn cáp cuối) nhấp hai lần rồi đứng trắng; trắng tràn vào góc, bóng dài và bóng tối biến mất. Câu thoại khớp với hình. V3: cuối phố là nhà kho có hốc cửa + ngõ cong, không còn tường trống.',
  sound: 'THOẠI L4 (ngoài hình) "…You\'ll be brighter now."; tách rơ-le gần; bóng đèn rít; rè điện', light: 'cột điện góc bật (nhấp 2 lần, đứng) — trắng phẳng tràn góc; L11 nhạt dần',
  action: 'Ida trên thang, Cas giữ thang; bóng đèn điện bật, bóng dài của hai người trên đá lát tan.' },
  (p, t, T, ida, { VG }) => { ida.place(idaTop(p, T, { nodX: NOD(T) }), LAMP_X(11), ON_Z1, 0); return { gi: gripAt(ida, 'L', VG) }; });   // Cổng 6: tay trái vẫn nắm van (liên tục PA1)
S({ id: 's38', scene: 5, size: 'MS', angle: 'cao, chúc xuống (gần mắt Ida)', mm: 50, move: 'tĩnh',
  why: 'Phản ứng của Cas: cậu giữ thang, ngước nhìn bà trong ánh trắng mới — người nghe câu nói thay khán giả. (c) Sau s39: cắt vào giữa "…ones who need it" (sau "for"), câu đã bắt đầu trên mặt Ida.', sound: 'L4 vế cuối "…ones who need it." (ngoài hình)',
  light: 'trắng phẳng (cột góc vừa bật); ấm rất yếu từ L11 trên cao', action: 'Cas giữ hai thanh thang, ngửa mặt nhìn lên.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); const lad = ladderAt(st.scene, 11); const dbg = ctx.dbg || {};
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 20 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34 });
    // Cổng 6: Cas cạnh chân thang phía đông (CAS_LAD) → máy cao (như Cổng 5), trước mặt cậu 3/4, chúc xuống; nhìn vào đầu cậu.
    const cam = camMM(50); cam.position.set(...(dbg.cp || [8.75, 2.45, -3.55])); cam.lookAt(...(dbg.cl || [8.36, 0.95, -4.6]));
    const cp = dbg.cas || CAS_LAD; const cf = faceRig(cas);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); ida.place(idaTop(p, T, { turn: 25, nodX: 12 }), LAMP_X(11), ON_Z1, 0);
        cas.place(casLadPose(p, T, -36), ...cp, CAS_LYAW); const gr = casHold(cas, lad);
        cf({ blink: blinkAt(T, [106.62]), browInnerUp: 0.35 * ease((T - 106.3) / 0.6) }, [0, -0.12]);   // chớp mắt (1,0 s nhịp sheet ≈ 106,6), đầu trong mày nâng dần khi nghe hết câu; nhìn lên bà
        if (dbg.log && f % 12 === 0) console.log(JSON.stringify({ id: 's38', preCas_m: PRE_GRIP.cas, grip_m: gr.map((e) => e === null ? null : +e.toFixed(4)), handL: V3a(wpos(cas.joints.wrist_L)), handR: V3a(wpos(cas.joints.wrist_R)) })); } };
  } });
// s39 (PA1): câu cuối CU NGHIÊNG 96° (hơi mất mặt) dưới ánh trắng — BẮT ĐẦU trên hình Ida ("Just…" 102,32), cắt sang Cas (s38) ở 106,0 giữa "…ones / who need it".
// Bà cúi nhìn xuống Cas ở chân thang (N11: bà nhìn xuống, cậu ngước lên ở s38). Cổ quay 25° (ít hơn 35°: đầu hướng về chân thang), cúi 12°.
pa1Shot('s39', { size: 'CU', angle: 'nghiêng 96° (phía phố), ngang mắt', mm: 85, move: 'tĩnh', fl: 'elec', ek: 0.8, yaw: 96, dist: 0.95, lookDy: 0.05, T0: 0,
  why: 'PA1: vế cuối, giọng vỡ, trong ánh trắng phẳng: "keep a little dark for the ones who need it" — chủ đề phim trong một câu. Mặt nghiêng, cúi về phía Cas.', sound: 'THOẠI L4 "Just... keep a little dark for the ones who need it."',
  light: 'trắng phẳng (cột góc); L11 nhạt', action: 'Ida nghẹn, cúi nhìn xuống Cas; "Just…" — nuốt — "keep a little dark for the ones…"; tay trái vẫn trên van.',
  pose: (p, T) => idaTop(p, T, { turn: 25, nodX: 12 + 2 * ease((T - 103.0) / 0.5) - 2 * ease((T - 103.6) / 0.4) }) });

// s40 — Cổng 6: QUYẾT ĐỊNH CỐ ĐỊNH (chủ dự án 29/09/2026): mặt Ida CHÌM VÀO BÓNG TỐI đúng lúc L11 tắt (L11_OFF = 109,2 s), không lộ mặt chính diện dưới ánh sáng.
// Dàn dựng (không thêm/bớt đèn): máy ở phía phố (+x, như PA1) ngang lồng đèn → cần van (tay trái bà, MPFB, nắm thật bằng reachGrip) ở tiền cảnh, ngọn lửa trong lồng,
// mặt bà NGHIÊNG (≈ 90°) bên phải lồng, được chính ngọn lửa rọi. Lửa co lại, ngả xanh (108,3–109,2); cùng lúc bà cúi đầu và quay mặt khỏi máy (108,75 → 109,2):
// ở 109,2 lửa tắt, kính lồng thành tối đục, mặt bà nằm dưới vành mũ, quay đi — trên hình chỉ còn vành mũ, búi tóc tối. Máy giữ im 0,8 s.
// G2: mũ giữ hat_back 0,35 như s39 (bản Cổng 5 đầu thẳng nhìn trước → đọc thành "mũ đội thẳng").
S({ id: 's40', scene: 5, size: 'CU (insert)', angle: 'ngang lồng đèn, từ lòng phố (phía phố, +x)', mm: 50, move: 'tĩnh',
  why: 'NGỌN CUỐI (AI mù v1: "thắp hay tắt?"): tay bà gạt van; lửa co lại, ngả xanh, tắt; mặt bà chìm vào bóng tối đúng lúc lửa tắt (quyết định cố định Cổng 6); máy giữ im 0,8 s trên lồng kính tối. Rõ là TẮT.', sound: 'van kim loại; lửa xì nhỏ dần; "phụt" tắt; im',
  light: 'ngọn L11 co lại → xanh → tắt; trắng phẳng không đổi', action: 'Tay trái Ida nắm cần van, gạt; ngọn lửa co lại, chuyển xanh, tắt; bà cúi đầu, quay mặt đi — mặt chìm vào bóng vành mũ; lồng kính tối.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11); const dbg = ctx.dbg || {};
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 32, faceQ: 1.2, expr: 'neutral', gaze: [0, 0], glint: 0.3 }); const cam = camMM(50);
    const l11 = st.lamps[10]; const lever = l11.lamp.userData.parts.lever; const fp = l11.fp; const flame = l11.lamp.userData.flame; const fs0 = flame.scale.clone();
    const lv = new THREE.Vector3(); lever.updateMatrixWorld(true); lever.getWorldPosition(lv);
    const mid = fp.clone().lerp(lv, 0.45); cam.position.copy(mid).add(new THREE.Vector3(...(dbg.co || [1.3, 0.16, -0.32]))); cam.lookAt(mid.clone().add(new THREE.Vector3(...(dbg.lo || [0, -0.04, -0.16]))));
    const blue = new THREE.Color('#6f8cff'); const face = faceRig(ida), TR = IDA5(DIALOGUE.L4);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        const u = clamp01((T - VALVE) / 0.6); lever.rotation.z = -0.5 + 1.2 * ease(u); lever.updateMatrixWorld(true);
        const k = ease((T - (L11_OFF - 0.45)) / 0.45);   // cúi + quay mặt đi: 108,75 → 109,2 (xong ĐÚNG lúc lửa tắt)
        const b = Math.sin(2 * Math.PI * T / 4.2);
        const pose = addJ(over(p.faceRest(HB, 0), { hands: { L: { spread: 0.1, curl: 0.85 }, R: { spread: 0.1, curl: 0.45 } } }), { neck: [-10 + 34 * k - 0.3 * b, -38 * k, 0], spine: [0.7 * b + 3 * k, -6 * k, 0] });
        ida.place(pose, LAMP_X(11), ON_Z1, 0);
        // tay trái nắm cần van (hộp 0,10 × 0,012 m): trục = trục x cục bộ của cần, điểm nắm 3 cm ngoài tâm cần; cần xoay → tay xoay theo (IK mỗi khung)
        const ax = new THREE.Vector3(1, 0, 0).transformDirection(lever.matrixWorld), pt = lever.localToWorld(new THREE.Vector3(0.025, 0, 0));
        const preL = +(ida.gripPoint('L').distanceTo(pt) - 0.009).toFixed(4); const gL = gripAt(ida, 'L', { point: pt.toArray(), axis: ax.toArray(), radius: 0.009 });
        face(mixW(wAt(TR.expr, T), { blink: blinkAt(T, TR.blinks) + blinkAt(T, [[107.55, 1.4]]) }), [0, valAt([[107.4, -0.12], [108.7, -0.1], [109.2, 0.3]], T)]);   // nhìn ngọn lửa, rồi cụp mắt theo đầu
        const [kf, bl] = flameL11(T); flame.scale.copy(fs0).multiplyScalar(Math.max(kf, 0.001)); flame.visible = kf > 0.01;
        l11.flameM.color.set('#fff2d0').multiplyScalar(30 * Math.max(kf, 0.2)).lerp(blue.clone().multiplyScalar(8), bl);
        if (dbg.log && f % 6 === 0) console.log(JSON.stringify({ id: 's40', T: +T.toFixed(2), preL_m: preL, gripL_m: +gL.toFixed(4), k: +k.toFixed(2), gp: V3a(ida.gripPoint('L')), wrL: V3a(wpos(ida.joints.wrist_L)), wrR: V3a(wpos(ida.joints.wrist_R)), pt: V3a(pt), cam: V3a(cam.position) })); } };
  } });
// s40w — Cổng 6 G10: bà XUỐNG THANG trong shot (không còn nhảy cắt): 0–0,35 s tay rời van; 0,35–1,55 s xuống (đảo nhịp trèo s35); 1,55–2,0 s chạm đất, quay về Cas,
// tháo đèn lồng khỏi móc thắt lưng sang tay phải (nối s41). Cas nắm thang tới khi bà xuống đất (1,55 s) rồi buông (1,55–1,9 s), quay về bà.
cornerWide('s40w', { why: '"Nothing else changes": ngọn cuối đã tắt, phố trắng y nguyên — không một đèn nào nhấp. Máy tĩnh, giữ 2 s (cùng khung s37w: so sánh trước/sau). Bà xuống thang lần cuối; Cas giữ thang.',
  sound: 'rè điện đều; im; bậc thang kẽo kẹt', light: 'trắng phẳng; lồng kính L11 tối', action: 'Ida rời tay khỏi van, xuống thang; Cas giữ thang rồi buông khi bà chạm đất; bà tháo đèn lồng sang tay phải.' },
  (p, t, T, ida, { cas, lad }) => {
    const top = over(p.restLadder, { hat_back: HB }), IDA_G = [7.95, -5.0];
    if (t < 0.35) ida.place(top, LAMP_X(11), ON_Z1, 0);
    else if (t < 1.55) { const u = 1 - (t - 0.35) / 1.2; const c = p.climb(u, top); c.hat_back = HB; ida.place(c, LAMP_X(11), FOOT_Z + (ON_Z1 - FOOT_Z) * ease(u), 0); }
    else { const standL = over(p.stand, { props: ['lantern_hand_R'], hat_back: HB, joints: { shoulder_R: [-20, 0, -10] } }); const k = ease((t - 1.55) / 0.45);
      ida.place(settle(poseAt([[1.55, over(p.stand, { hat_back: HB })], [1.8, over(p.stand, { hat_back: HB, joints: { shoulder_R: [-30, 0, -20], elbow_R: [-60, 0, 0] } })], [1.95, standL]], t), t, { side: -1, k }),
        valAt([[1.55, LAMP_X(11)], [2.0, IDA_G[0]]], t), valAt([[1.55, FOOT_Z], [2.0, IDA_G[1]]], t), valAt([[1.55, 0], [2.0, yawTo(...IDA_G, ...CAS_41)]], t)); }
    const kc = 1 - ease((t - 1.55) / 0.35);
    cas.place(poseAt([[1.55, casLadPose(p, T)], [2.0, settle(over(p.C.turnaround, { joints: { neck: [10, 0, 0] } }), T, { side: -1, k: 0.6, br: 3.0 })]], t), ...CAS_LAD, valAt([[1.55, CAS_LYAW], [2.0, yawTo(...CAS_LAD, ...IDA_G)]], t));
    return { cas: true, grip: casHold(cas, lad, kc) }; });

// s41 — Cổng 6 (d, việc 3): Cas đứng GẦN bà hơn (0,57 m; Cổng 5: 1,02 m — cậu phải duỗi hết tay); bà chìa đèn ngắn (khuỷu gập), không duỗi thẳng.
// Trao thật: 0–0,45 s bà nhấc đèn về phía cậu; 0,35–0,75 s cậu đưa hai tay, NẮM hai bên vòng quai (IK tay MPFB, trộn vào); 0,85 s bà buông (đèn đổi sang đạo cụ
// riêng, cùng vị trí/hướng — không nhảy); 0,85–1,35 s cậu kéo đèn về sát ngực (ôm, như s42a); bà hạ tay, đứng nghỉ. Ida TRÁI, Cas PHẢI (trục cảnh 5).
const IDA_41 = [7.95, -5.0], CAS_41 = [8.5, -4.85];
// Hai điểm nắm trên vòng quai đèn lồng (như gripRing): trả { L, R } dạng reachGrip.
function ringG(ch, lan, h, ang = 50) {
  const q = ch.root.getWorldQuaternion(new THREE.Quaternion()), right = new THREE.Vector3(1, 0, 0).applyQuaternion(q), up = new THREE.Vector3(0, 1, 0), r = 0.12 * h, a = ang * Math.PI / 180;
  lan.updateMatrixWorld(true); const C = new THREE.Vector3(0, 1.06 * h, 0).applyMatrix4(lan.matrixWorld), rx = new THREE.Vector3(1, 0, 0).transformDirection(lan.matrixWorld), sgnL = rx.dot(right) >= 0 ? 1 : -1, o = {};
  for (const [s, sg] of [['L', sgnL], ['R', -sgnL]]) o[s] = { point: C.clone().addScaledVector(rx, sg * r * Math.sin(a)).addScaledVector(up, r * Math.cos(a)).toArray(), axis: rx.clone().multiplyScalar(Math.cos(a)).addScaledVector(up, -sg * Math.sin(a)).normalize().toArray(), radius: 0.018 * h };
  return o;
}
S({ id: 's41', scene: 5, size: 'WS', angle: 'ngang', mm: 28, move: 'tĩnh',
  why: 'Dưới chân thang bà trao đèn lồng; cậu nhận bằng hai tay, ôm vào ngực.', sound: 'rè điện đều; quai đèn',
  light: 'trắng phẳng; đèn lồng ấm trong tay', action: 'Ida chìa đèn lồng (tay gập, ngắn); Cas đứng sát, nắm quai bằng hai tay, ôm vào ngực; bà buông tay.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11); const dbg = ctx.dbg || {};
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 22 });
    const own = lanternProp(ctx); st.scene.add(own); own.traverse((o) => { if (o.isMesh) o.castShadow = false; }); const h = ctx.sheets.ida.props.lantern.height_H * ctx.sheets.ida.H_m;
    const L = new THREE.PointLight('#ffa050', 0, 0, 2); st.scene.add(L);
    const cam = camMM(28); cam.position.set(12.8, 1.5, 0.6); cam.lookAt(...(dbg.cl || [8.2, 1.15, -4.9]));
    const yI = yawTo(...IDA_41, ...CAS_41), yC = yawTo(...CAS_41, ...IDA_41), SW = 0.85;
    const offer = over(p.holdOut, { hat_back: HB, joints: { neck: [20, 0, 0], shoulder_R: [-44, 0, -4], elbow_R: [-42, 0, 0] } });
    const idaPose = (t) => settle(poseAt([[0, over(p.stand, { props: ['lantern_hand_R'], hat_back: HB, joints: { shoulder_R: [-20, 0, -10], neck: [14, 0, 0] } })], [0.45, offer], [SW, offer], [1.4, over(p.stand, { props: [], hat_back: HB, joints: { neck: [16, 0, 0] } })]], t), t, { side: -1, k: 0.8 });
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        let lanObj;
        if (t < SW) { ida.place(idaPose(t), ...IDA_41, yI); own.visible = false; lanObj = ida.props.lantern; }
        else {   // đèn đã sang tay Cas: đạo cụ riêng xuất phát ĐÚNG vị trí/hướng của đèn trong tay bà lúc buông (tính lại tư thế bà ở SW — hàm thuần theo t)
          const pS = idaPose(SW); ida.place(pS, ...IDA_41, yI); ida.props.lantern.updateMatrixWorld(true); const m0 = ida.props.lantern.matrixWorld.clone();
          const pp = idaPose(t); ida.place({ ...pp, props: [] }, ...IDA_41, yI);
          const P0 = new THREE.Vector3(), Q0 = new THREE.Quaternion(), S0 = new THREE.Vector3(); m0.decompose(P0, Q0, S0);
          const qC = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), yC), fw = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), yC);
          const P1 = new THREE.Vector3(CAS_41[0], 0.8 - 1.06 * h, CAS_41[1]).addScaledVector(fw, 0.2);   // tâm vòng quai trước ngực cậu, cao 0,8 m
          const k = ease((t - SW) / 0.5); own.visible = true; own.position.copy(P0).lerp(P1, k); own.quaternion.copy(Q0).slerp(qC, k); own.scale.copy(S0); own.updateMatrixWorld(true); lanObj = own;
        }
        cas.place(settle(poseAt([[0, over(p.C.turnaround, { joints: { neck: [16, 0, 0] } })], [0.4, over(p.casTake, { joints: { neck: [18, 0, 0] } })], [1.35, over(casHug(p), { joints: { neck: [14, 0, 0] } })]], t), T, { side: 1, k: 0.5, br: 3.0 }), ...CAS_41, yC);
        const kg = ease((t - 0.35) / 0.4); let gr = null;
        let pre = null; if (lanObj && cas.reachGrip) { const G = ringG(cas, lanObj, h); pre = ['L', 'R'].map((sd) => +(cas.gripPoint(sd).distanceTo(new THREE.Vector3(...G[sd].point)) - G[sd].radius).toFixed(4)); gr = [gripK(cas, 'L', G.L, kg, true), gripK(cas, 'R', G.R, kg, true)]; }
        lanObj?.userData?.lightAnchor ? lanObj.userData.lightAnchor.getWorldPosition(L.position) : 0; L.intensity = 1.2 * flickAt(f + 17);
        if (dbg.log && f % 6 === 0) console.log(JSON.stringify({ id: 's41', t: +t.toFixed(2), pre_m: pre, grip_m: gr?.map((e) => e === null ? null : +e.toFixed(4)) })); } };
  } });

// Bộ s5/s6 dựng nhân vật với glint mặc định (5,0 — hợp phơi sáng 0,12 của Cổng 3); ở phơi sáng animatic ~1,0 mắt thành phát sáng → hạ về mức makeChar.
const tameGlint = (ch, k = 0.12) => ch.root.traverse((o) => { if (o.isMesh && o.material && o.material.emissiveMap) o.material.emissiveIntensity = k * (o.userData.part === 'eyes' ? 3 : 1); });
// Đèn lồng Cas cầm (cùng đạo cụ cast.buildLantern, cỡ theo sheet Ida): treo giữa hai cổ tay.
const lanternProp = (ctx) => buildLantern(ctx.sheets.ida.props.lantern.height_H * ctx.sheets.ida.H_m, (r, c) => r === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff0c8').multiplyScalar(20) }) : r === 'glass' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc56b').multiplyScalar(3), transparent: true, opacity: 0.7, depthWrite: false }) : lamMat({ color: c }));
function hangFromHands(lan, ch, h) { const a = new THREE.Vector3(), b = new THREE.Vector3(); ch.joints.wrist_L.getWorldPosition(a); ch.joints.wrist_R.getWorldPosition(b);
  lan.position.copy(a.add(b).multiplyScalar(0.5)).add(new THREE.Vector3(0, -h - 0.03, 0)); lan.updateMatrixWorld(true); }
// Cổng 6 (W4T lượt 3, chủ dự án 29/09/2026): tay MPFB NẮM QUAI THẬT — ngón gập quanh vòng quai (tay 'bl' mới có; tay cũ giữ cách treo giữa hai cổ tay).
// Vòng quai (buildLantern): xuyến bán kính 0,12 h, ống 0,018 h, tâm ở 1,06 h, nằm trong mặt phẳng XY cục bộ. Hai tay nắm hai điểm chéo trên của vòng (±ang so với đỉnh),
// trục nắm = tiếp tuyến vòng tại đó; IK hai xương (ch.reachGrip). move=true: dời đèn cho vòng nằm giữa hai nắm tay (Cas tự cầm); false: đèn đứng yên (Ida đang cầm, s41).
function gripRing(ch, lan, h, { move = true, ang = 45 } = {}) {
  if (!ch.handsBL || !ch.reachGrip) return false;
  const q = ch.root.getWorldQuaternion(new THREE.Quaternion()), right = new THREE.Vector3(1, 0, 0).applyQuaternion(q), up = new THREE.Vector3(0, 1, 0), r = 0.12 * h, a = ang * Math.PI / 180;
  if (move) { const gL = ch.gripPoint('L'), gR = ch.gripPoint('R'), C = gL.add(gR).multiplyScalar(0.5).addScaledVector(up, -r * Math.cos(a));
    lan.quaternion.copy(q); lan.position.copy(C).addScaledVector(up, -1.06 * h); lan.updateMatrixWorld(true); }
  lan.updateMatrixWorld(true);
  const C = new THREE.Vector3(0, 1.06 * h, 0).applyMatrix4(lan.matrixWorld), rx = new THREE.Vector3(1, 0, 0).transformDirection(lan.matrixWorld), sgnL = rx.dot(right) >= 0 ? 1 : -1;
  const err = {};
  for (const [s, sg] of [['L', sgnL], ['R', -sgnL]]) {
    const pt = C.clone().addScaledVector(rx, sg * r * Math.sin(a)).addScaledVector(up, r * Math.cos(a)), ax = rx.clone().multiplyScalar(Math.cos(a)).addScaledVector(up, -sg * Math.sin(a)).normalize();
    err[s] = ch.reachGrip(s, { point: pt.toArray(), axis: ax.toArray(), radius: 0.018 * h });
  }
  return err;
}
// Cổng 5 (continuity N2): Cas ÔM đèn lồng sát ngực (hai tay, đèn treo giữa hai cổ tay) — cùng một cách cầm ở s41 (cuối), s42a, s42b (v2: casTake chìa xa, nhìn nghiêng đọc thành một tay).
const casHug = (p) => over(p.casTake, { joints: { shoulder_L: [-12, 0, -18], elbow_L: [-112, 0, 0], shoulder_R: [-12, 0, 18], elbow_R: [-112, 0, 0] } });   // v2 (N2): khuỷu gập sát, cổ tay trước ngực — đèn áp bụng, nhìn nghiêng không còn 'chìa ra'
const IDA_42A = [6.8, -2.5];
// Chỉ đạo chủ dự án (2:07 v1): "Cas nên chọn 1 góc tối để huơ tay" → nhìn quanh phố trắng (s42a), đi vào vòm hốc cửa tối (s42b), hơ tay trong bóng tối (s42).
S({ id: 's42a', scene: 5, size: 'MS', angle: 'ngang ngực Cas, 3/4 trước', mm: 45, move: 'tĩnh',
  why: 'CHỈ ĐẠO CHỦ DỰ ÁN (2:07 v1): Cas ôm đèn lồng, nhìn quanh phố giờ trắng khắp nơi — không còn chỗ nào cho ngọn lửa nhỏ. Cậu tìm một góc tối.', sound: 'rè điện; lửa đèn lồng thở; nhạc tạm vào lại',
  light: 'trắng phẳng khắp khung; đèn lồng ấm dưới cằm Cas', action: 'Cas cầm đèn lồng bằng hai tay, quay đầu nhìn trái, nhìn phải, rồi nhìn về phía hốc cửa (trái khung).',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 20 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34, expr: 'neutral' }); const idaF = faceRig(ida), idaEyes = (g) => idaF({ lidDrop: 0.15 }, g); const cf = faceRig(cas);
    const lanObj = lanternProp(ctx); st.scene.add(lanObj); lanObj.traverse((o) => { if (o.isMesh) o.castShadow = false; }); const h = ctx.sheets.ida.props.lantern.height_H * ctx.sheets.ida.H_m;
    const lanL = new THREE.PointLight('#ffa050', 0, 0, 2); st.scene.add(lanL);
    const cam = camMM(45); cam.position.set(10.4, 1.0, -0.6); cam.lookAt(7.6, 0.9, -3.3);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        // Cổng 6 (việc 4): bà NHÌN XUỐNG Cas (kiểm mù W4T2: "ánh mắt đi qua trên đầu đứa trẻ"). Mắt bà ≈ 1,50 m, mặt cậu ≈ 1,08 m, cách 1,13 m → góc cúi tới mặt cậu ≈ 20°:
        // cổ cúi 24° + thân 4° + nhãn cầu cúi 0,12 rad (≈ 7°) → tia nhìn rơi vào mặt/đèn trước ngực cậu (không qua đầu). Hướng người nhắm thẳng vào đầu cậu; bà thở, dồn chân.
        ida.place(settle(over(p.stand, { props: [], hat_back: HB, joints: { neck: [24, 0, 0], spine: [4, 0, 0] } }), T, { side: -1, k: 0.8 }), ...IDA_42A, yawTo(...IDA_42A, 7.6, -3.3)); idaEyes([0, 0.12]);   // C3: Ida TRÁI khung
        const nk = valAt([[0, 0], [0.3, 0], [0.8, 38], [1.2, 38], [1.6, -30], [2.0, -45]], t);
        cas.place(settle(over(casHug(p), { joints: { neck: [4, nk, 0] } }), T, { side: 1, k: 0.5, br: 3.0 }), 7.6, -3.3, yawTo(7.6, -3.3, 10.4, -0.6));
        cf({ blink: blinkAt(T, [114.1, 114.95]) }, [nk * 0.004, 0]);   // chớp mắt khi đổi hướng nhìn; nhãn cầu đi trước đầu một chút
        hangFromHands(lanObj, cas, h); const G0 = ringG(cas, lanObj, h, 45), pre = ['L', 'R'].map((sd) => +(cas.gripPoint(sd).distanceTo(new THREE.Vector3(...G0[sd].point)) - G0[sd].radius).toFixed(4)); const gr = gripRing(cas, lanObj, h); const g3 = ['L', 'R'].map((sd) => +(cas.gripPoint(sd).distanceTo(new THREE.Vector3(...G0[sd].point)) - G0[sd].radius).toFixed(4)); if ((ctx.dbg || {}).log && f % 6 === 0) console.log(JSON.stringify({ id: 's42a', pre_m: pre, grip_line_m: gr && [+gr.L.toFixed(4), +gr.R.toFixed(4)], grip_pt_m: g3 })); lanObj.userData.lightAnchor.getWorldPosition(lanL.position); lanL.intensity = 1.2 * flickAt(f + 17); } };
  } });

S({ id: 's42b', scene: 5, size: 'WS', angle: 'ngang 1,3 m, ngoài vòm', mm: 32, move: 'tĩnh',
  why: 'Cas ôm đèn lồng rời phố trắng, bước qua vòm vào hốc cửa khuất điện (nơi hai cái bóng đứng lúc trước): ánh hổ phách đi theo cậu vào trong bóng tối; quay ra vòm, ngồi xổm, đặt đèn xuống nền (nối s42). Cậu vẫn đội mũ len.', sound: 'bước chân trẻ con; rè điện xa dần',
  light: 'ngoài vòm: điện phẳng; trong hốc: chỉ đèn lồng Cas mang theo', action: 'Cas ôm đèn đi từ phố vào vòm (0–1,3 s), quay ra vòm (1,1–1,5 s), ngồi xổm và đặt đèn xuống nền trước mặt (1,45–2,0 s) — tư thế cuối = tư thế mở s42 (N7).',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}); const p = P(ctx); r.chCas.sheetRef = r.chCas.sheet; [r.chIda, r.chCas].forEach((c) => tameGlint(c)); r.chIda.root.visible = false;
    const cam = r.cam; cam.shiftY = 0.05; cam.position.set(0.9, 1.25, 8.2); cam.lookAt(0.3, 1.1, 2.0); cam.updateProjectionMatrix();
    const h = r.lanternH; const f0 = r.flameP.clone();
    const glows = []; r.scene.traverse((o) => { if (o.isSprite && o.position.distanceTo(f0) < 0.4) glows.push([o, o.position.clone().sub(f0)]); });
    const cur = f0.clone();
    const moveLamp = () => { r.lan.userData.lightAnchor.getWorldPosition(cur); r.spot.position.copy(cur); U.uLP.value.copy(cur); r.spot.updateMatrixWorld(); for (const [o, d] of glows) o.position.copy(cur).add(d); };
    const carry = casHug(p); const hCr = (p.C.warm_hands_copy.root_y_H ?? 0) * ctx.sheets.cas.H_m;
    return { scene: r.scene, cam, onSample: (i, n, j) => { r.onSample(i, n, j); moveLamp(); }, named: { cas: r.chCas }, paintP: S5_PAINT, grade: GRADE_S5, exposure: 1.0,
      update(t) {
        // N7: đi 0–1,3 s → quay ra vòm 1,1–1,5 s → 1,45–2,0 s ngồi xổm, đặt đèn xuống nền trước mặt (đúng chỗ đèn ở s42) — s42 mở ở tư thế ngồi.
        const x = valAt([[0, 1.9], [1.3, CAS_BAY[0]]], t), z = valAt([[0, 5.3], [1.3, CAS_BAY[1]]], t);
        const w = walkPose(t, p.C.turnaround, { gait: WALK_CHILD });
        const crouch = p.C.warm_hands_copy;   // đích = đúng tư thế mở s42 (khớp cắt)
        const u = ease((t - 1.45) / 0.55);
        const pose = t < 1.3 ? over(w, { joints: { shoulder_L: carry.joints.shoulder_L, elbow_L: carry.joints.elbow_L, shoulder_R: carry.joints.shoulder_R, elbow_R: carry.joints.elbow_R }, hands: carry.hands }) : t < 1.45 ? carry : lerpPose(carry, crouch, u);
        r.chCas.setPose(pose); r.chCas.root.position.set(x, hCr * u, z); r.chCas.root.rotation.y = t < 1.1 ? yawTo(1.9, 5.3, ...CAS_BAY) : valAt([[1.1, yawTo(1.9, 5.3, ...CAS_BAY)], [1.5, 0]], t); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) ctx.upd(r.chCas, cam);
        if (r.lan.parent !== r.scene) r.scene.add(r.lan); hangFromHands(r.lan, r.chCas, h);
        if (u > 0) { const tgt = new THREE.Vector3(CAS_BAY[0] - 0.03, 0, CAS_BAY[1] + 0.55); const k = ease((t - 1.6) / 0.4); r.lan.position.lerp(tgt, k); r.lan.updateMatrixWorld(true); }
        // Cổng 6 (d): hai tay MPFB NẮM hai bên vòng quai (IK điểm) khi ôm đi và khi hạ đèn; buông 1,75–2,0 s → tư thế cuối = tư thế mở s42 (tay mở, hơ).
        const kr = 1 - ease((t - 1.75) / 0.25); let gr = null, pre = null; if (r.chCas.reachGrip && kr > 0) { const G = ringG(r.chCas, r.lan, h); pre = ['L', 'R'].map((sd) => +(r.chCas.gripPoint(sd).distanceTo(new THREE.Vector3(...G[sd].point)) - G[sd].radius).toFixed(4)); gr = [gripK(r.chCas, 'L', G.L, kr, true), gripK(r.chCas, 'R', G.R, kr, true)]; }
        if ((ctx.dbg || {}).log && Math.round(t * 24) % 6 === 0) console.log(JSON.stringify({ id: 's42b', t: +t.toFixed(2), pre_m: pre, grip_m: gr?.map((e) => e === null ? null : +e.toFixed(4)) }));
        moveLamp(); } };
  } });

// V1 (2:00, s42): nguyên nhân tìm được (đo trên probe + hình học, xem LAYOUT-W2.md):
//  (1) máy CHÍNH DIỆN cậu, thấp 0,72 m, cách 2,5 m, đèn lồng nằm GIỮA máy và cậu: hai lòng bàn tay (cổ tay xoay 70° về phía kính = về phía máy) chính diện,
//      xoè, gần máy hơn đầu 0,4–0,5 m → tay to bất thường (tay đã ×1,30 theo sheet); quầng sprite của đèn lồng phủ lên cả người;
//  (2) mặt + mũ nằm NGOÀI nón sáng đèn lồng (nắp chắn tia > 49° — luật 5A): mặt tối; mũ len kem #d6c9ae chỉ nhận dội ấm, quả bông đỏ khuất sau đỉnh đầu
//      vì máy thấp hơn đỉnh mũ → mũ đọc thành "tóc vàng" (mũ KHÔNG rơi: mũ gắn khớp đầu);
//  (3) dáng ngồi xổm (hông −96°, gối 124°) nhìn thẳng từ trước → hai gối dồn giữa khung, thân ngắn → "méo".
// Sửa bằng dàn dựng + máy, KHÔNG đổi tỷ lệ sheet: Cas quay mặt RA VÒM (về phía Ida và ánh trắng), đèn lồng trước mặt cậu; máy đặt SAU LƯNG, lệch phải,
// lùi 2,3 m, thấp ngang vai (0,66 m), 40 mm: đầu + mũ len + quả bông in trên nền phố trắng qua vòm; tay thấy từ sau-bên (không chính diện); dáng xổm thấy từ sau 3/4.
// Ida ở mép trái miệng vòm; Cas phải khung (luật 180° cảnh 5).
const CAS_BAY = [-0.35, 2.55];   // máy trong hốc nhìn ra (+z): −x là PHẢI khung → Cas ở −x, Ida ở +x mép miệng vòm
S({ id: 's42', scene: 5, size: 'MS', angle: 'thấp ngang vai, sau lưng Cas lệch phải, trong hốc nhìn ra vòm', mm: 40, move: 'tĩnh',
  why: 'Trả mô-típ: trong góc tối cậu tự chọn, không ai bảo, Cas đặt đèn xuống, hơ hai lòng tay trên kính đếm ba — đúng như bà. Qua vòm: phố trắng; Ida đứng ở miệng vòm nhìn vào, không nói. V1: dáng cậu, mũ len + quả bông in trên nền phố trắng; tay thấy từ sau-bên, đúng cỡ.', sound: 'lửa đèn lồng thở; nhạc tạm',
  light: 'đèn lồng trên nền đá trước mặt Cas (nguồn duy nhất trong hốc, viền ấm quanh người cậu); ngoài vòm: điện phẳng', action: 'Cas ngồi xổm quay ra vòm, áp tay: một, hai, ba. Ida ở mép miệng vòm (trái khung) nhìn vào; cuối shot bà kéo vành mũ lại (hết ca) rồi quay người đi.',
  async build(ctx) {
    const dbg = ctx.dbg || {};
    const r = await buildBaySet(ctx, {}); const p = P(ctx); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    const cam = r.cam; cam.shiftY = 0; [r.chIda, r.chCas].forEach((c) => tameGlint(c)); cam.fov = fovOf(dbg.mm ?? 40); cam.position.set(...(dbg.cp || [0.55, 0.66, 0.45])); cam.lookAt(...(dbg.cl || [-0.15, 0.75, 4.5])); cam.updateProjectionMatrix();
    const wc = p.C.warm_hands_copy, wcIn = over(wc, { joints: { shoulder_L: [-66, 0, 10], shoulder_R: [-66, 0, -10], elbow_L: [-28, 0, 0], elbow_R: [-28, 0, 0] } });
    const hC = (wc.root_y_H ?? 0) * ctx.sheets.cas.H_m;
    placeBayLantern(r, CAS_BAY[0] - 0.03, CAS_BAY[1] + 0.55); const LH = r.lanternH;
    // Quyết định chủ dự án (AUTHORSHIP, world-rules v0.5): bà KÉO MŨ LẠI khi rời đi — cử chỉ khép "hết ca", đặt ở cuối s42 (bà ở miệng vòm, vừa thấy Cas
    // tự đếm ba — khoảnh khắc buông tay; nền phố trắng sau lưng bà làm dáng tay–vành mũ in rõ). 0–1,9 s đứng nhìn (hat_back 0,35); 1,9–2,2 s tay trái lên vành;
    // 2,2–2,8 s kéo vành xuống (0,35 → 0); 2,8–3,0 s hạ tay, bắt đầu quay người đi (yaw +0,5 rad, sang phải bà = rời khỏi vòm).
    const iStand = over(p.stand, { props: [], hat_back: HB, joints: { neck: [12, 0, 0] } });
    const iHand = (hb) => over(p.stand, { props: [], hat_back: hb, joints: { neck: [4, 0, 0], shoulder_L: [-86, 0, 34], elbow_L: [-118, 0, 0], wrist_L: [0, 0, 0] }, hands: { L: { spread: 0.2, curl: 0.35 } } });
    const iPose = (t) => poseAt([[0, iStand], [1.9, iStand], [2.2, iHand(HB)], [2.8, iHand(0)], [3.0, over(p.stand, { props: [], hat_back: 0, joints: { neck: [0, 0, 0] } })]], t);
    const IP = dbg.ida || [1.25, 0, 5.25];
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: dbg.exp ?? 0.8,
      update(t) {
        let k = 0; for (const b of [0.6, 1.2, 1.8]) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        r.chIda.setPose(settle(iPose(t), t, { side: -1, k: 0.8 })); r.chIda.root.position.set(...IP); r.chIda.root.rotation.y = Math.PI - 0.25 + 0.5 * ease((t - 2.75) / 0.25); r.chIda.root.updateMatrixWorld(true);
        r.chCas.setPose({ ...lerpPose(wc, wcIn, k), props: [] }); r.chCas.root.position.set(CAS_BAY[0], hC, CAS_BAY[1]); r.chCas.root.rotation.y = 0; r.chCas.root.updateMatrixWorld(true);
        // Cổng 6 (d): mỗi nhịp đếm, LÒNG TAY áp về hai mặt kính đèn lồng (tay MPFB, IK điểm, trộn 0,8 × nhịp k): tâm lòng tay → mặt kính 4 cm (hơ, không chạm), lòng quay vào kính, ngón duỗi.
        const lanC = new THREE.Vector3(r.lan.position.x, r.lan.position.y + 0.4 * LH, r.lan.position.z), hw = 0.28 * LH + 0.04;
        const pre = ['L', 'R'].map((sd, i) => +(r.chCas.gripPoint(sd).distanceTo(lanC.clone().add(new THREE.Vector3(i ? -hw : hw, 0, 0)))).toFixed(4));
        let gw = null; if (k > 0.02 && r.chCas.reachGrip) gw = [gripK(r.chCas, 'L', { point: lanC.toArray(), axis: [0, 1, 0], radius: hw, out: [1, 0, 0] }, 0.8 * k, true), gripK(r.chCas, 'R', { point: lanC.toArray(), axis: [0, 1, 0], radius: hw, out: [-1, 0, 0] }, 0.8 * k, true)];
        if (dbg.log && Math.round(t * 24) % 6 === 0) console.log(JSON.stringify({ id: 's42', t: +t.toFixed(2), k: +k.toFixed(2), palmToGlassFK_m: pre, afterIK_m: gw?.map((e) => e === null ? null : +e.toFixed(4)) }));
        if (ctx.upd) { ctx.upd(r.chIda, cam); ctx.upd(r.chCas, cam); } } };
  } });

// ---------------- CẢNH 6 — Ô cửa ----------------
S({ id: 's43', scene: 6, t0: 130.0, t1: 134.0, size: 'EWS', angle: 'cao (cùng khung mở đầu)', mm: 28, move: 'dolly vào rất chậm',
  why: 'Lặp khung mở đầu để đo cái đã mất: thành phố trắng đều, không ngủ; giữa khung một ô cửa hổ phách.', sound: 'rè điện toàn thành phố; nhạc tạm',
  light: 'đèn điện khắp nơi; một ô cửa đèn lồng', action: 'Toàn cảnh tĩnh; một ô vàng.',
  async build(ctx) { const c = await buildCitySet(ctx, 'night'); return { ...c, exposure: 1.0, grade: GRADE_COLD }; } });

// Cảnh 6: Ida đã trao đèn lồng (s41) → trong ngõ bà KHÔNG còn đèn lồng (props không có lantern_*). Bà vác thang (s47: chỉ 'ladder_shoulder').
const alleyShot = (id, t0, t1, meta, fn) => S({ id, scene: 6, t0, t1, ...meta,
  async build(ctx) {
    const r = await buildAlleySet(ctx, {}); const p = P(ctx); r.chIda.sheetRef = r.chIda.sheet; tameGlint(r.chIda); const cam = r.cam; const ctl = fn(p, cam, r, ctx.dbg || {});
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda }, paintP: S6_PAINT, grade: GRADE_ALLEY, exposure: meta.exposure ?? 4.0,
      update(t, T, f) { ctl.update(t, T, r.chIda); if (ctx.upd) ctx.upd(r.chIda, cam); } };
  } });
alleyShot('s44', 134.0, 137.0, { size: 'WS', angle: 'thấp, hất lên ô cửa', mm: 21, move: 'đẩy vào chậm',
  why: 'Trong ngõ khuất điện, dưới ánh cửa sổ nhà Cas, bóng bà — ngắn, nhạt — nằm lại trên đá lát (khung style frame d_s6_alley).', sound: 'rè điện xa, nghẹt; im',
  light: 'đèn lồng trên bậu cửa sổ (qua ô kính); điện chỉ lọt miệng ngõ', action: 'Ida đứng dưới cửa sổ, ngửa nhìn ô vàng.' },
  (p, cam, r, dbg) => { const c0 = cam.position.clone(); alleyLadder(r.scene); const face = faceRig(r.chIda); return { update(t, T, ida) {
    // Cổng 6 G5: "tay đặt ngực" — lòng bàn tay trái MPFB ÁP lên ngực (IK điểm; trước: FK sheet để tay lơ lửng trước áo). Thở, dồn chân; mắt ngước lên ô cửa, chớp chậm.
    ida.setPose(settle({ ...p.lookShadows, props: [] }, T, { side: 1, k: 0.6, bx: 1.2 })); ida.root.updateMatrixWorld(true);
    const q = ida.root.getWorldQuaternion(new THREE.Quaternion()), fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q), up = new THREE.Vector3(0, 1, 0).applyQuaternion(ida.joints.spine.getWorldQuaternion(new THREE.Quaternion()));
    const chest = wpos(ida.joints.spine).addScaledVector(up, dbg.cy ?? 0.3).addScaledVector(fw, dbg.cf ?? 0.12).add(new THREE.Vector3(-0.03, 0, 0).applyQuaternion(q));
    const pre = ida.gripPoint('L').distanceTo(chest); const e = gripAt(ida, 'L', { point: chest.toArray(), axis: new THREE.Vector3(1, 0, 0).applyQuaternion(q).toArray(), radius: 0.02, out: fw.toArray() });
    face({ browInnerUp: 0.45, smile: 0.2, lidDrop: 0.1, blink: blinkAt(T, [[125.4, 1.5], 126.6]) }, [0, -0.1]);
    if (dbg.log && Math.round(t * 24) % 12 === 0) console.log(JSON.stringify({ id: 's44', palmToChestFK_m: +pre.toFixed(4), afterIK_m: +e.toFixed(4) }));
    cam.position.copy(c0).add(new THREE.Vector3(0, 0, 0.5 * ease(t / 3))); } }; });
// Cổng 6 G13: thang của bà có trong ngõ TRƯỚC khi bà vác đi (s47): tựa vách cửa sổ (x = −0,85; phải khung s44), phía miệng ngõ cách bà 1,4 m (z 2,4), nghiêng 0,2 rad. Chỉ s44, s45 (s46 insert không thấy; s47 thang trên vai).
function alleyLadder(scene) { const g = new THREE.Group(); g.position.set(-0.85 + 1.8 * Math.sin(0.2) + 0.03, 0, 2.4); g.rotation.y = -Math.PI / 2; const lad = ladderOf(); lad.rotation.x = 0.2; g.add(lad); scene.add(g); return g; }
// s45: máy 3/4 trước-phải bà (tính theo đầu + hướng mặt), thấy cả mặt đồng hồ trong tay và mặt bà ngẩng lên — bản v2 máy sau vai, không thấy đồng hồ.
// Hướng nhìn cuối s45 (N10): [cúi/ngẩng cổ, quay cổ, xoay thân] (độ). Hướng đồng hồ insert s46 (N12, dùng chung s45).
const S45_TURN = [-12, 50, 20], D46 = new THREE.Vector3(-0.6, 0.1, 0.8);
// Cổng 6 B1/G6: đồng hồ hạ xuống ngang ngực (watchHold của sheet đưa tay phải lên cằm → tay che nửa mặt, đồng hồ khuất); bà cúi nhìn xuống lòng tay. Dùng chung s45, s46.
const watchLow = (p) => over(p.watchHold(0), { props: [], joints: { neck: [30, 0, 0], shoulder_R: [-22, 0, -14], elbow_R: [-84, 0, 0] } });
const cupG = (ida, watch) => { const q = ida.root.getWorldQuaternion(new THREE.Quaternion()); return { point: watch.position.toArray(), axis: new THREE.Vector3(1, 0, 0).applyQuaternion(q).toArray(), radius: 0.03, out: [0, -1, 0] }; };   // lòng tay trái ĐỠ dưới đồng hồ
alleyShot('s45', 137.0, 139.0, { size: 'MS', angle: 'ngang ngực, 3/4 trước-phải', mm: 50, move: 'tĩnh', exposure: 6.0,
  why: 'ĐỒNG HỒ NHỊP 3a — hai giờ sau (10:00): bà nhìn đồng hồ trong lòng tay (9:53, vẫn chậm 7 phút), rồi quay đầu và vai nhìn qua vai về miệng ngõ — phía quảng trường có đồng hồ điện (N10: dẫn tới POV s45c).', sound: 'tích tắc; rè điện xa',
  light: 'ánh cửa sổ ấm từ trên; phố trắng ở miệng ngõ sau lưng bà (phải khung)', action: 'Ida cúi nhìn đồng hồ trong lòng bàn tay phải; 1,0–1,8 s quay đầu + vai về miệng ngõ (phải khung, sâu), ngẩng nhẹ.' },
  (p, cam, r, dbg) => { let wf = null, watch = null; const probe = new THREE.Object3D(); alleyLadder(r.scene); const face = faceRig(r.chIda); return { update(t, T, ida) {
    if (!wf) { wf = watchInHand(ida.root.parent); watch = ida.root.parent.children[ida.root.parent.children.length - 1]; }
    // Máy TĨNH: tính từ tư thế gốc (watchHold, t = 0) — không bám đầu đang quay (bản trước máy trôi theo đầu khi bà ngẩng).
    const base = watchLow(p); ida.setPose(base); ida.root.updateMatrixWorld(true);
    const h = wpos(ida.joints.head), q = new THREE.Quaternion(); ida.root.getWorldQuaternion(q); const fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q); fw.y = 0; fw.normalize();
    const dir = fw.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), (dbg.yaw ?? -35) * Math.PI / 180);
    cam.fov = fovOf(50); cam.updateProjectionMatrix(); cam.position.copy(h).addScaledVector(dir, dbg.dist ?? 2.0); cam.position.y = h.y - (dbg.dy ?? 0.3); cam.lookAt(h.x, h.y - (dbg.ly ?? 0.12), h.z);   // máy thấp hơn mắt 0,3 m: thấy mặt dưới vành mũ khi bà cúi xem đồng hồ. N10: lùi 1,75 → 2,0 m, tâm nhìn 0,22 → 0,12 m dưới đầu — trọn mũ + đường mắt khi bà quay nhìn miệng ngõ (bản trước cắt đỉnh mũ)
    // N10 (rà continuity v3): miệng ngõ (phố trắng, quảng trường có đồng hồ) ở SAU LƯNG bà, phải khung. 1,0–1,8 s bà quay đầu + vai về miệng ngõ, ngẩng nhẹ —
    // nhìn qua vai về phía quảng trường (bản trước ngẩng về phía máy = quay lưng lại quảng trường). Hàm thuần theo t.
    const sp = base.joints.spine || [0, 0, 0], TN = dbg.turn || S45_TURN;
    const look = over(base, { joints: { neck: [TN[0], TN[1], 0], spine: [sp[0], sp[1] + TN[2], sp[2]] } });
    ida.setPose(poseAt([[0, base], [1.0, base], [1.8, look]], t)); ida.root.updateMatrixWorld(true);
    // N12: đồng hồ đặt ĐÚNG như insert s46 (cùng hàm watchInHand, cùng hướng D46 và cự ly — vật thể ở cùng vị trí/hướng trong tay qua cắt MS → insert), không quay mặt về máy s45.
    wf(ida, probe, ...hands(CLOCKS.beat3.watchFrom), D46, 0.32);
    // Cổng 6 G6 + B1: tay TRÁI không còn tách khỏi đồng hồ (và không che nửa mặt 0–1,0 s như bản Cổng 5): lòng tay trái MPFB đỡ cạnh đồng hồ (IK điểm, 3,5 cm từ tâm vỏ),
    // hai tay cùng giữ đồng hồ như ở insert s46. Hướng mặt/đầu (B1): 0–1,0 s mắt cúi vào mặt số; 0,85 s mắt đi trước, 1,0–1,8 s đầu + vai quay về miệng ngõ, ngẩng nhẹ, chớp khi quay.
    const pre = watch ? ida.gripPoint('L').distanceTo(watch.position) : null; const eL = watch ? gripAt(ida, 'L', cupG(ida, watch)) : null;
    face({ browInnerUp: valAt([[0.9, 0.2], [1.6, 0.45]], t), lidDrop: valAt([[0.8, 0.3], [1.3, 0.05]], t), blink: blinkAt(T, [T0.s45 + 1.12]) }, [valAt([[0.8, 0], [1.05, 0.22], [1.8, 0.1]], t), valAt([[0, 0.28], [0.9, 0.28], [1.2, 0.0], [1.8, -0.04]], t)]);
    if (dbg.log && Math.round(t * 24) % 12 === 0) console.log(JSON.stringify({ id: 's45', palmLToWatchFK_m: pre && +pre.toFixed(4), afterIK_m: eL === null ? null : +eL.toFixed(4) })); } }; });
S({ id: 's45c', scene: 6, size: 'CU', angle: 'tele, POV của Ida qua miệng ngõ', mm: 200, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 3c — POV của Ida: mặt đồng hồ điện trên nền trời đêm chỉ đúng 10:00 (cùng vị trí, cùng cỡ với nhịp 2a): giờ của thành phố, khớp giờ bà vừa vặn (s46). (d) Sau s46: giờ trên hình chỉ tiến (10:00 → 10:00:0x).', sound: 'rè điện xa; tích tắc',
  light: 'mặt đồng hồ phát trắng; trời đêm', action: 'Mặt đồng hồ quảng trường: 10:00.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 140, x1: 200, shadowLamps: [] }); const cam = camMM(200); cam.position.set(150, 6.2, 0.4); cam.lookAt(CLOCK.x, CLOCK.h, CLOCK.z);
    const [mD, hD] = hands(CLOCKS.beat3.square);
    return { scene: st.scene, cam, named: {}, paintP: PAINT_CLOSE, exposure: 1.2, grade: GRADE_COLD,
      update(t, T, f) { st.setState(stdState(T), f); st.clock.userData.setHands(mD + 6 * t / 60, hD); } };
  } });
alleyShot('s46', 139.0, 142.0, { size: 'CU (insert)', angle: 'chúc nhẹ', mm: 100, move: 'tĩnh', exposure: 6.0,
  why: 'ĐỒNG HỒ NHỊP 3b (9B): vừa ngẩng về phía quảng trường (cuối s45), bà vặn kim từ 9:53 lên đúng 10:00 — nhận giờ mới; KHÔNG gõ kính (ngược với nhịp 1). (d) Đặt TRƯỚC s45c để giờ trên hình chỉ tiến.', sound: 'núm vặn lách cách; tách gập',
  light: 'ánh cửa sổ ấm', action: 'Kim phút và kim giờ cùng tiến từ 9:53 lên 10:00 (vặn núm 0,3–2,2 s), rồi giữ 10:00.' },
  (p, cam, r, dbg) => { let wf = null, watch = null; const D = dbg.dir ? new THREE.Vector3(...dbg.dir) : D46; return { update(t, T, ida) {   // A2: máy gần ngang, lệch về phía tường ngõ → nền là tường vôi, không còn đá lát (v1: [0,2; 0,8; 0,55] nhìn chúc xuống nền đá)
    if (!wf) { wf = watchInHand(ida.root.parent); watch = ida.root.parent.children[ida.root.parent.children.length - 1]; }
    ida.setPose(watchLow(p)); ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(dbg.mm ?? 100); cam.updateProjectionMatrix();
    const [m0, h0] = hands(CLOCKS.beat3.watchFrom), mA = valAt([[0, m0], [0.3, m0], [2.2, 360]], t); wf(ida, cam, mA, h0 + (mA - m0) / 12, D, dbg.dist ?? 0.32);
    if (watch && !dbg.noCup) gripAt(ida, 'L', cupG(ida, watch)); } }; });   // Cổng 6 G6: tay trái đỡ dưới đồng hồ như s45 (nối cắt)   // (d) kim giờ ăn khớp kim phút (1/12, như bánh răng thật): cả hai kim chỉ TIẾN, cùng lúc; 9:53 giữ 0–0,3 s, vặn 0,3–2,2 s, 10:00 giữ tới hết
alleyShot('s47', 142.0, 145.0, { size: 'WS', angle: 'ngang, sau lưng Ida', mm: 28, move: 'tĩnh',
  why: 'Bà vác thang đi ra miệng ngõ; bóng mờ của bà mỏng dần rồi tan trong trắng (luật 3.5). Không còn đèn lồng ở thắt lưng (đã trao cho Cas ở s41).', sound: 'bước chân; thang; rè điện lớn dần ở miệng ngõ',
  light: 'ánh cửa sổ (sau lưng) → điện phẳng ở miệng ngõ', action: 'Ida vác thang đi từ dưới cửa sổ ra miệng ngõ.' },
  (p, cam) => ({ update(t, T, ida) { const wp = { ...walkPose(t, p.I.walk_ladder), props: ['ladder_shoulder'] }; ida.setPose(wp); ida.root.position.set(0.3, wp.root_y_m, 1.0 + WALK.speed_mps * 1.05 * t); ida.root.rotation.y = 0; ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(28); cam.updateProjectionMatrix(); cam.position.set(0.1, 1.45, -2.6); cam.lookAt(0.0, 1.3, 6.0); } }));

// s48 — kết 2B (B1: giữ phòng Cas). Luật 3.3 cảnh 6: Cas GẦN đèn hơn (z = −0,35; đèn ở bậu z = −1,62; vách z = +1,6), hai tay giơ CAO phía trước (≈ 1,7 m):
// chim (×≈2,0) nằm trên cao ≈ 2,3 m, tách hẳn khỏi bóng đầu (×≈2,5, đỉnh ≈ 1,8 m) → đọc là chim, không phải một khối bóng người.
S({ id: 's48', scene: 6, t0: 145.0, t1: 150.0, size: 'WS', angle: 'ngang, sau lưng Cas', mm: 28, move: 'tĩnh; mờ dần về đen (cuối shot, 1,5 s)',
  why: 'Kết 2B: đèn lồng trên bậu, Cas quay lưng, chim to và mềm mở cánh bay ngang tường. Ida đã đi trước.', sound: 'nhạc tạm (kết); lửa thở',
  light: 'đèn lồng trên bậu (nguồn duy nhất, hổ phách trọn khung)', action: 'Cas làm chim trên cao; chim bay ngang tường; FADE OUT.',
  async build(ctx) {
    const R = buildRoomSet(ctx); const p = P(ctx); const cas = makeChar(ctx, R.scene, 'cas', { detail: 26, blob: false }); const dbg = ctx.dbg || {};
    const cam = camMM(28); cam.position.set(...(dbg.cp || [-1.45, 1.35, -1.55])); cam.lookAt(...(dbg.cl || [0.45, 1.65, 1.6]));
    const cz = dbg.cz ?? -0.35, sh = dbg.sh ?? -150;
    return { scene: R.scene, cam, named: { cas }, paintP: PAINT_WALL, exposure: (t) => 2.4 * (1 - ease((t - 3.5) / 1.5)),
      update(t, T, f) { R.L.intensity = 3.5 * flickAt(f); const sw = Math.sin(t * 0.8) * 14;
        const b = p.bird(t, 1.0); cas.place(over(b, { joints: { spine: [-4, sw, 0], neck: [-26, 0, 0], shoulder_L: [sh, b.joints.shoulder_L[1], b.joints.shoulder_L[2]], shoulder_R: [sh, b.joints.shoulder_R[1], b.joints.shoulder_R[2]] } }), 0.6 + 0.15 * Math.sin(t * 0.6), cz, -0.15);
        if (dbg.log && f % 12 === 0) console.log(JSON.stringify({ id: 's48', t: +t.toFixed(2), palmL: V3a(cas.gripPoint('L')), palmR: V3a(cas.gripPoint('R')), wrL: V3a(wpos(cas.joints.wrist_L)), casHead: V3a(wpos(cas.joints.head)) })); } };
  } });

// ---------- MỐC SỰ KIỆN (xuất cho âm tạm, phụ đề, SHOTLIST) — cùng nguồn với hình ----------

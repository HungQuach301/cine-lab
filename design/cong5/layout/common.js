// Cine Lab · Cổng 5 LAYOUT — PHẦN CHUNG (P giữ). Tách từ film.js Cổng 4 (animatic v2). Gói W1: shots_w1.js + order_w1.js; W2: shots_w2.js + order_w2.js.
// (gốc) Cổng 4 — BẢNG SHOT ANIMATIC "Last Round" (kịch bản nháp 2, 2:30). Nguồn duy nhất: SHOTLIST.md sinh từ bảng này (make_shotlist.js).
// Mỗi shot: id, cảnh, t0–t1 (giây phim), cỡ, góc, tiêu cự (mm tương đương 35 mm), chuyển máy, lý do, thoại/âm, nguồn sáng trong truyện, hành động;
// build(ctx) → { scene, cam, update(t, T, f), exposure, grade, paintP, named }.
// Quy ước địa lý (luật 180°): phố Ostler chạy dọc x; quảng trường + đồng hồ ở +x (PHẢI màn hình), nhà kho ở −x (TRÁI). Máy luôn ở phía nam phố
// (z > đường đi của Ida) nên Ida đi PHẢI → TRÁI suốt cảnh 1–3; sóng trắng tới từ PHẢI. Cảnh 4–5 (tường, hốc cửa): máy luôn ở phía sau-phải hai người,
// Ida bên TRÁI, Cas bên PHẢI. Cận thoại trên thang: Ida nhìn lên phố (phải khung), Cas dưới chân thang nhìn lên.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { walkPose, WALK, WALK_CHILD } from '/cong3/shared/anim.js';
import { buildStreetSet, LAMP_X, LAMP_Z, WALK_Z, POST_X, CLOCK, ladderOf, buildWatch, lamMat, flickAt, GRADE_COLD } from './sets.js';
import { buildCitySet, buildWallSet, buildBaySet, buildAlleySet, buildRoomSet } from './sets2.js';
import { buildLantern } from '/cong3/shared/cast.js';
import { U } from '/cong3/v2/s5.js';
import { ease, easeIO, clamp01, fovOf, lerpPose, over, poseAt, valAt, camAt, makeChar, yawTo } from './util.js';

export const PAINT_STREET = { rNear: 3.0, rFar: 6.5, dNear: 3, dFar: 40, impScale: 0.4, stroke: 0.04, halation: 0.14, bloomWide: 0.06, wob: 1.5 };
export const PAINT_CLOSE = { rNear: 2.5, rFar: 6.0, dNear: 1.2, dFar: 25, impScale: 0.35, stroke: 0.035, halation: 0.14, bloomWide: 0.06 };
export const PAINT_WALL = { rNear: 3.0, rFar: 6.0, dNear: 2, dFar: 20, impScale: 0.4, stroke: 0.04, halation: 0.12, bloomWide: 0.06 };
export const S5_PAINT = { rNear: 7.0, rFar: 9.0, dNear: 6, dFar: 12, impScale: 0.5, stroke: 0.045, preAmp: 0.16, wob: 3.5, preLen: 46, preWid: 6 };
export const S5_PAINT_MED = { rNear: 3.0, rFar: 6.0, dNear: 1.2, dFar: 8, impScale: 0.4, stroke: 0.04, preAmp: 0.14, wob: 3.0 };
export const S6_PAINT = { rNear: 3.0, rFar: 6.0, dNear: 1.5, dFar: 14, impScale: 0.4, stroke: 0.04, halation: 0.12, bloomWide: 0.06, wob: 1.2 };
export const GRADE_S5 = { gCanvas: 0.012, gVig: 0.30, gLift: 0.018, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [0.985, 0.995, 1.02] };
export const GRADE_ALLEY = { gCanvas: 0.012, gVig: 0.30, gLift: 0.02, gSat: 1.0, gShadowTint: [0.32, 0.30, 0.90], gHiTint: [1.0, 0.975, 0.93] };

// ---------- lịch ánh sáng chung (giây phim) ----------
// Đèn khí thắp: L1–L3 trước phim; L4 9,2; L5 19,0 và L6 26,5 (ngoài hình); L7 32,0; L8 52,4; L9 55,4; L10 62,95; L11 65,0; L11 nhạt từ 1:16 (điện bật), tắt 2:04,6.
// ================= v2 (Cổng 4 vòng sửa): BẢNG THỨ TỰ + THỜI LƯỢNG — nguồn duy nhất cho mốc shot và mốc sự kiện =================
// Mỗi dòng: [id, thời lượng (s), nguồn]. nguồn 'v1:<id>' = tái dùng khung đã render ở v1 (cắt từ đầu shot v1), 'new' = render mới/lại.
import { ORDER_W1 } from './order_w1.js';
import { ORDER_W2 } from './order_w2.js';
export const ORDER = [...ORDER_W1, ...ORDER_W2];   // P ghép; mỗi gói giữ bảng thứ tự của mình
export const T0 = {}, T1 = {}, SRC = {};
{ let t = 0; for (const [id, d, src] of ORDER) { T0[id] = +t.toFixed(3); t += d; T1[id] = +t.toFixed(3); SRC[id] = src; } }
export const FILM_S = T1[ORDER[ORDER.length - 1][0]];
// ---------- lịch sự kiện (giây phim), tính theo đầu shot ----------
// Đèn khí thắp: L1–L3 trước phim; L4 trong s03; L5, L6 ngoài hình; L7 ngay trước s11; L8 đầu s19; L9 ngoài hình; L10 khung cuối s22 (sau câu thoại); L11 trong s23.
export const GAS_ON = { 1: -99, 2: -99, 3: -99, 4: T0.s03 + 0.7, 5: T0.s07 - 1.0, 6: T0.s09 - 0.5, 7: T0.s11 - 2.0, 8: T0.s19 + 0.05, 9: T0.s21 - 1.0, 10: T1.s22 - 0.05, 11: T0.s23 + 2.0 };
// Cột điện (chỉ số POST_X): 0 x=141 · 1 x=113 · 2 x=85 · 3 x=57 · 4 x=29 · 5 x=11,2 (khối cuối, cạnh nhà kho, bật muộn một nhịp — luật thế giới mục 1)
export const CLOCK_ON = T0.s09 + 0.3, DING = T0.s09 + 1.0, SQUARE_ON = T0.s10e + 0.3;
export const POST_ON = [T0.s10 + 0.9, T0.s10 + 2.2, T0.s12 + 1.2, T0.s19 + 1.5, T0.s21 - 0.5, T0.s37w + 0.4];
// Chỉ đạo chủ dự án (v2): góc ngọn 11 thuộc ĐOẠN CÁP CUỐI — cột góc (POST_ON[5]) chỉ bật giữa câu L4, ngay trước "You'll be brighter now" (L4 + 6,45 s).
// Cảnh 4 (1:16): cột PHỐ CHÍNH cạnh góc nhà kho bật, ánh tràn phủ mặt tường Cas làm chim; góc ngọn 11 lùi sau góc nhà vẫn tối.
export const WALL_POST_ON = T0.s27 + 0.4;
// Ngọn cuối (s40): tay gạt van 0,3–0,9 s; lửa co lại, chuyển xanh 0,9–1,8 s; tắt ở 1,8 s; giữ im 0,8 s trước khi cắt ra toàn cảnh.
export const REACH_IDA = T0.s13 + 0.05, VALVE = T0.s40 + 0.3, L11_OFF = T0.s40 + 1.8, RELAY_1 = T0.s08 + 0.3;
// Thoại (giữ nguyên văn): L1 đầu s05, L2 đầu s22, L3 đầu s31, L4 đầu s37 (kéo qua s38, s39).
export const DIALOGUE = { L1: T0.s05, L2: T0.s22, L3: T0.s31, L4: T0.s37 };
// Đồng hồ — 3 nhịp, giờ TIẾN: (1) s06 đồng hồ bỏ túi 7:31 (thật 7:38, chạy chậm 7 phút; gõ kính thân thương);
// (2) s09 → s09w: đồng hồ quảng trường sáng đúng 8:00 lúc điện bật, cắt khớp sang đồng hồ bỏ túi 7:53 — bà trễ đúng lúc giờ mới tới;
// (3) s45c → s46: trong ngõ, đồng hồ quảng trường 10:00; bà vặn kim bỏ túi từ 9:53 lên 10:00, gập lại, không gõ.
export const CLOCKS = { beat1: { watch: [31, 7] }, beat2: { square: [0, 8], watch: [53, 7] }, beat3: { square: [0, 10], watchFrom: [53, 9], watchTo: [0, 10] } };
export const hands = ([m, h]) => [m * 6, (h % 12) * 30 + m * 0.5];   // → [độ kim phút, độ kim giờ]
export const switchOn = (T, t0) => { const d = T - t0; if (d < 0) return 0; if (d < 0.08) return 1; if (d < 0.16) return 0; if (d < 0.26) return 1; if (d < 0.34) return 0.05; return clamp01((d - 0.34) / 0.1); };
export const gasLevel = (i, T) => { const t0 = GAS_ON[i]; if (T < t0) return 0; const bloom = clamp01((T - t0) / 0.35);   // "phụp": nở trong 0,35 s
  if (i === 11 && T >= POST_ON[5]) { if (T >= L11_OFF) return 0;   // tắt hẳn
    if (T >= VALVE + 0.6) return 0.35 * (1 - 0.8 * clamp01((T - VALVE - 0.6) / (L11_OFF - VALVE - 0.6)));   // lửa co lại sau khi gạt van
    return 0.35 + 0.65 * clamp01(1 - (T - POST_ON[5]) / 1.5); }   // nhạt đi trong trắng
  return bloom; };
// Hình ngọn lửa L11 trong s40: [tỉ lệ cỡ, trộn sang xanh 0…1]
export const flameL11 = (T) => { if (T < VALVE + 0.6) return [1, 0]; if (T >= L11_OFF) return [0, 1]; const u = (T - VALVE - 0.6) / (L11_OFF - VALVE - 0.6); return [1 - 0.8 * u, clamp01((u - 0.25) / 0.5)]; };
// Ánh trắng tràn tại vị trí x (các cột trong 26 m) — mức 0…1 theo nhịp bật.
export const whiteAt = (x) => (T) => { let w = 0; POST_X.forEach((px, k) => { const d = Math.abs(px - x); if (d < 26) w = Math.max(w, switchOn(T, POST_ON[k]) * (d < 12 ? 1 : 1 - (d - 12) / 14)); }); if (x > 150) w = Math.max(w, switchOn(T, SQUARE_ON)); return w; };
export const stdState = (T, o = {}) => ({
  gas: (i) => (o.gas && o.gas[i] !== undefined ? o.gas[i](T) : gasLevel(i, T)),
  post: (k) => (o.post && o.post[k] !== undefined ? o.post[k](T) : switchOn(T, POST_ON[k])),
  square: switchOn(T, SQUARE_ON), clock: T >= CLOCK_ON ? clamp01((T - CLOCK_ON) / 0.25) : 0,
  whiteFill: o.whiteFill ? o.whiteFill(T) : 0,
});
// Phơi sáng: đêm có đèn khí mở khẩu; khi trắng tràn máy đóng khẩu (vũng hổ phách chìm vào trắng — kịch bản 0:34–0:42).
export const expo = (open, closed, wf) => (t, T) => open + (closed - open) * clamp01(wf(T));

// ---------- tư thế ----------
export const P = (ctx) => {
  const I = ctx.sheets.ida.poses, C = ctx.sheets.cas.poses;
  const ladderLegs = { spine: I.warm_hands_ladder.joints.spine, hip_L: [-34, 0, 0], knee_L: [58, 0, 0], ankle_L: [-20, 0, 0], hip_R: [-6, 0, 0], knee_R: [10, 0, 0] };
  const LH = { L: { spread: 0.1, curl: 0.8 }, R: { spread: 0.1, curl: 0.45 } };
  const armsRest = { shoulder_L: [-40, 0, 10], elbow_L: [-50, 0, 0], wrist_L: [0, 0, 10], shoulder_R: [-58, 0, -8], elbow_R: [-62, 0, 0], wrist_R: [0, 0, -10] };
  const onLadder = (arms = {}, hands = LH, extra = {}) => ({ joints: { ...ladderLegs, neck: [-4, 0, 0], ...arms }, hands, props: ['lantern_belt'], root_y_m: 1.55, hat_back: 0, ...extra });
  const wh = I.warm_hands_ladder;
  return {
    I, C, LH,
    stand: over(I.turnaround, { props: ['lantern_belt'] }),
    warmLadder: onLadder(wh.joints, wh.hands),
    warmLadderIn: onLadder({ ...wh.joints, shoulder_L: [-100, 0, 4], shoulder_R: [-100, 0, -4], elbow_L: [-26, 0, 0], elbow_R: [-26, 0, 0] }, wh.hands),
    valveLadder: onLadder({ ...armsRest, shoulder_R: [-112, 0, -8], elbow_R: [-40, 0, 0], wrist_R: [0, 0, -20] }, { R: { spread: 0.2, curl: 0.6 }, L: LH.L }),
    restLadder: onLadder(armsRest),
    lookDown: onLadder({ ...armsRest, neck: [30, 0, 0] }),
    liftHand: onLadder({ ...armsRest, neck: [34, 0, 0], shoulder_L: [-30, 0, 38], elbow_L: [-20, 0, 0], wrist_L: [0, 0, 0] }, { L: { spread: 0.6, curl: 0.1 }, R: LH.R }),
    turnSquare: onLadder({ ...armsRest, spine: [10, 28, 0], neck: [-6, 48, 0] }),
    poleLadder: onLadder({ ...armsRest, shoulder_R: [-120, 0, -12], elbow_R: [-35, 0, 0], wrist_R: [10, 0, 0] }, { R: { spread: 0.0, curl: 0.9 }, L: LH.L }, { props: ['pole_hand_R', 'lantern_belt'] }),
    poleFumble: onLadder({ ...armsRest, shoulder_R: [-95, 0, -25], elbow_R: [-20, 0, 0], wrist_R: [-40, 0, 20], shoulder_L: [-85, 0, 30], elbow_L: [-40, 0, 0] }, { R: { spread: 0.6, curl: 0.2 }, L: { spread: 0.5, curl: 0.2 } }, { props: ['pole_hand_R', 'lantern_belt'] }),
    faceRest: (hb = 0.35, turn = 35) => onLadder({ ...armsRest, neck: [-4, turn, 0] }, LH, { hat_back: hb }),
    hatA: onLadder({ ...armsRest, neck: [-4, 35, 0], shoulder_L: [-80, 0, 35], elbow_L: [-120, 0, 0], wrist_L: [0, 0, 0] }, { L: { spread: 0.2, curl: 0.35 }, R: LH.R }, { hat_back: 0 }),
    hatB: onLadder({ ...armsRest, neck: [-4, 35, 0], shoulder_L: [-88, 0, 38], elbow_L: [-116, 0, 0], wrist_L: [0, 0, 0] }, { L: { spread: 0.2, curl: 0.35 }, R: LH.R }, { hat_back: 0.35 }),
    climb: (u, top) => { const e = ease(u), p = lerpPose(onLadder({ ...armsRest, shoulder_L: [-120, 0, 8], elbow_L: [-30, 0, 0], shoulder_R: [-120, 0, -8], elbow_R: [-30, 0, 0] }, { L: { spread: 0.1, curl: 0.9 }, R: { spread: 0.1, curl: 0.9 } }, { root_y_m: 0 }), top, e);
      const s = Math.sin(u * Math.PI * 5); p.joints.hip_L = [-50 + 30 * s, 0, 0]; p.joints.knee_L = [70 + 30 * s, 0, 0]; p.joints.hip_R = [-50 - 30 * s, 0, 0]; p.joints.knee_R = [70 - 30 * s, 0, 0];
      if (u >= 1) return top; p.root_y_m = 1.55 * e; return p; },
    watchHold: (tap = 0) => over(I.turnaround, { props: ['lantern_belt'], joints: { neck: [22, 0, 0], shoulder_R: [-38, 0, -16], elbow_R: [-96, 0, 0], wrist_R: [0, -60, 0], shoulder_L: [-34, 0, 18], elbow_L: [-100 + 10 * tap, 0, 0], wrist_L: [0, 0, 0] }, hands: { R: { spread: 0.1, curl: 0.35 }, L: { spread: 0.1, curl: 0.75 } } }),
    watchRaise: over(I.turnaround, { props: ['lantern_belt'], joints: { neck: [-6, 0, 0], shoulder_R: [-98, 0, -4], elbow_R: [-8, 0, 0], wrist_R: [0, -70, 0] }, hands: { R: { spread: 0.1, curl: 0.4 } } }),
    crouch: I.crouch_lantern,
    holdOut: over(I.turnaround, { props: ['lantern_hand_R'], joints: { neck: [16, 0, 0], shoulder_R: [-62, 0, -6], elbow_R: [-18, 0, 0] }, hands: { R: { spread: 0, curl: 0.9 } } }),
    lookShadows: I.look_shadows,
    casTake: over(C.turnaround, { joints: { neck: [10, 0, 0], shoulder_L: [-60, 0, -8], elbow_L: [-40, 0, 0], shoulder_R: [-60, 0, 8], elbow_R: [-40, 0, 0] }, hands: { L: { spread: 0, curl: 0.8 }, R: { spread: 0, curl: 0.8 } } }),
    bird: (t, hz = 1.1, amp = 1) => { const b = C.shadow_bird, s = Math.sin(2 * Math.PI * hz * t);
      return over(b, { joints: { wrist_L: [b.joints.wrist_L[0] + 7 * amp * s, b.joints.wrist_L[1], b.joints.wrist_L[2]], wrist_R: [b.joints.wrist_R[0] + 7 * amp * s, b.joints.wrist_R[1], b.joints.wrist_R[2]] },
        hands: { L: { spread: 0.78 + 0.16 * amp * s, curl: 0.0, thumb_cross: true }, R: { spread: 0.78 + 0.16 * amp * s, curl: 0.0, thumb_cross: true } } }); },
  };
};
// Thang tựa cột đèn i (phía bắc cột — giữa cột và mặt tiền; bố trí như a_close_ida): Ida trên thang quay mặt +z (về lồng kính).
export function ladderAt(scene, i) { const lad = ladderOf(); lad.position.set(LAMP_X(i), 0.12, LAMP_Z - 0.85); lad.rotation.x = 0.36; scene.add(lad); return lad; }
export const ON_Z = LAMP_Z - 0.58, FOOT_Z = LAMP_Z - 1.15;
// Máy cận mặt kiểu face_ida (Cổng 4 Việc 1): lệch `yaw` độ khỏi hướng mặt, cách `dist` m, ngang mắt.
export function faceCam(cam, ch, { yaw = -10, dist = 1.05, y = -0.02, drop = -0.06, fov = 20 } = {}) {
  const head = new THREE.Vector3(); ch.joints.head.getWorldPosition(head); head.y += 0.12;
  const q = new THREE.Quaternion(); ch.joints.head.getWorldQuaternion(q); const fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q); fw.y = 0; fw.normalize();
  const eye = head.clone().add(fw.clone().multiplyScalar(0.08)).add(new THREE.Vector3(0, y, 0));
  const dir = fw.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), yaw * Math.PI / 180);
  const base = eye.clone().addScaledVector(dir, dist); base.y += drop; cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(base); cam.lookAt(eye);
}
// Nguồn sáng đèn lồng (bám điểm neo lửa của đèn lồng trong tay/thắt lưng).
export function lanternLight(scene, shadow = false, I = 1.6) {
  const L = new THREE.PointLight('#ffa050', 0, 0, 2); if (shadow) { L.castShadow = true; L.shadow.mapSize.set(512, 512); L.shadow.bias = -0.0006; L.shadow.normalBias = 0.02; L.shadow.camera.near = 0.03; } scene.add(L);
  return (ch, f, k = 1) => { const lan = ch.props.lantern; if (!lan || !lan.parent) { L.intensity = 0; return; } lan.updateMatrixWorld(true); lan.userData.lightAnchor.getWorldPosition(L.position); L.intensity = I * k * flickAt(f + 17); };
}
// Đồng hồ bỏ túi bám lòng bàn tay phải, mặt quay về máy.
// Insert: máy đặt theo hướng `dir` cách lòng bàn tay `dist` m; đồng hồ nằm trước ngón tay (3,5 cm về phía máy), mặt quay về máy.
// Đ2 (W1-v2, 30/09/2026): o.grip = true → đặt theo TÂM LÒNG TAY MPFB (ch.gripPoint('R')), nhích o.lift m (mặc định 0,09) về phía máy.
// Mặc định (không có o) GIỮ cách đặt cũ theo lòng tay sheet ở cổ tay — shot W2 đã duyệt (s45, s46, s45c) không đổi điểm ảnh; bật o.grip cho W2 cần duyệt riêng.
export function watchInHand(scene, o = {}) {
  const w = buildWatch(); scene.add(w);
  return (ch, cam, minDeg, hourDeg, dir = null, dist = 0.3) => { const H = ch.H, p = o.grip && ch.gripPoint ? ch.gripPoint('R', new THREE.Vector3()) : new THREE.Vector3(0, -ch.sheetRef.parts.hand.palm_length * H * 0.55, 0); if (!(o.grip && ch.gripPoint)) ch.joints.wrist_R.localToWorld(p);
    if (dir) { cam.position.copy(p).addScaledVector(dir.clone().normalize(), dist); cam.lookAt(p); }
    w.position.copy(p).addScaledVector(cam.position.clone().sub(p).normalize(), o.grip ? (o.lift ?? 0.09) : 0.09); w.lookAt(cam.position); w.userData.setHands(minDeg, hourDeg); };
}
export const camMM = (mm) => new THREE.PerspectiveCamera(fovOf(mm), 16 / 9, 0.03, 900);


export const SHOTS = [];
export const S = (o) => { if (!(o.id in T0)) return; SHOTS.push({ ...o, t0: T0[o.id], t1: T1[o.id], src: SRC[o.id] }); };

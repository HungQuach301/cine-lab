// Cine Lab · Cổng 4 — BẢNG SHOT ANIMATIC "Last Round" (kịch bản nháp 2, 2:30). Nguồn duy nhất: SHOTLIST.md sinh từ bảng này (make_shotlist.js).
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
import { ease, easeIO, clamp01, fovOf, lerpPose, over, poseAt, valAt, camAt, makeChar, yawTo } from './util.js';

const PAINT_STREET = { rNear: 3.0, rFar: 6.5, dNear: 3, dFar: 40, impScale: 0.4, stroke: 0.04, halation: 0.14, bloomWide: 0.06, wob: 1.5 };
const PAINT_CLOSE = { rNear: 2.5, rFar: 6.0, dNear: 1.2, dFar: 25, impScale: 0.35, stroke: 0.035, halation: 0.14, bloomWide: 0.06 };
const PAINT_WALL = { rNear: 3.0, rFar: 6.0, dNear: 2, dFar: 20, impScale: 0.4, stroke: 0.04, halation: 0.12, bloomWide: 0.06 };
const S5_PAINT = { rNear: 7.0, rFar: 9.0, dNear: 6, dFar: 12, impScale: 0.5, stroke: 0.045, preAmp: 0.16, wob: 3.5, preLen: 46, preWid: 6 };
const S5_PAINT_MED = { rNear: 3.0, rFar: 6.0, dNear: 1.2, dFar: 8, impScale: 0.4, stroke: 0.04, preAmp: 0.14, wob: 3.0 };
const S6_PAINT = { rNear: 3.0, rFar: 6.0, dNear: 1.5, dFar: 14, impScale: 0.4, stroke: 0.04, halation: 0.12, bloomWide: 0.06, wob: 1.2 };
const GRADE_S5 = { gCanvas: 0.012, gVig: 0.30, gLift: 0.018, gSat: 1.0, gShadowTint: [0.30, 0.25, 0.85], gHiTint: [0.985, 0.995, 1.02] };
const GRADE_ALLEY = { gCanvas: 0.012, gVig: 0.30, gLift: 0.02, gSat: 1.0, gShadowTint: [0.32, 0.30, 0.90], gHiTint: [1.0, 0.975, 0.93] };

// ---------- lịch ánh sáng chung (giây phim) ----------
// Đèn khí thắp: L1–L3 trước phim; L4 9,2; L5 19,0 và L6 26,5 (ngoài hình); L7 32,0; L8 52,4; L9 55,4; L10 62,95; L11 65,0; L11 nhạt từ 1:16 (điện bật), tắt 2:04,6.
export const GAS_ON = { 1: -99, 2: -99, 3: -99, 4: 9.2, 5: 19.0, 6: 26.5, 7: 32.0, 8: 52.4, 9: 55.4, 10: 62.95, 11: 65.0 };   // L10: bắt lửa SAU câu thoại (kịch bản), sát điểm cắt
// Cột điện (chỉ số POST_X): 0 x=141 · 1 x=113 · 2 x=85 · 3 x=57 · 4 x=29 · 5 x=11,2 (khối cuối, cạnh nhà kho, bật muộn một nhịp — luật thế giới mục 1)
export const POST_ON = [31.4, 33.2, 38.2, 54.0, 57.5, 76.3];
export const CLOCK_ON = 26.3, SQUARE_ON = 30.2, L11_OFF = 124.6, RELAY_1 = 24.3, DING = 27.0;
// Bật: nhấp 2 lần rồi đứng (luật 2).
export const switchOn = (T, t0) => { const d = T - t0; if (d < 0) return 0; if (d < 0.08) return 1; if (d < 0.16) return 0; if (d < 0.26) return 1; if (d < 0.34) return 0.05; return clamp01((d - 0.34) / 0.1); };
export const gasLevel = (i, T) => { const t0 = GAS_ON[i]; if (T < t0) return 0; const bloom = clamp01((T - t0) / 0.35);   // "phụp": nở trong 0,35 s
  if (i === 11 && T >= POST_ON[5]) { if (T >= L11_OFF) return 0.35 * clamp01(1 - (T - L11_OFF) / 0.3); return 0.35 + 0.65 * clamp01(1 - (T - POST_ON[5]) / 1.5); }   // nhạt đi trong trắng, rồi tắt
  return bloom; };
// Ánh trắng tràn tại vị trí x (các cột trong 26 m) — mức 0…1 theo nhịp bật.
const whiteAt = (x) => (T) => { let w = 0; POST_X.forEach((px, k) => { const d = Math.abs(px - x); if (d < 26) w = Math.max(w, switchOn(T, POST_ON[k]) * (d < 12 ? 1 : 1 - (d - 12) / 14)); }); if (x > 150) w = Math.max(w, switchOn(T, SQUARE_ON)); return w; };
const stdState = (T, o = {}) => ({
  gas: (i) => (o.gas && o.gas[i] !== undefined ? o.gas[i](T) : gasLevel(i, T)),
  post: (k) => (o.post && o.post[k] !== undefined ? o.post[k](T) : switchOn(T, POST_ON[k])),
  square: switchOn(T, SQUARE_ON), clock: T >= CLOCK_ON ? clamp01((T - CLOCK_ON) / 0.25) : 0,
  whiteFill: o.whiteFill ? o.whiteFill(T) : 0,
});
// Phơi sáng: đêm có đèn khí mở khẩu; khi trắng tràn máy đóng khẩu (vũng hổ phách chìm vào trắng — kịch bản 0:34–0:42).
const expo = (open, closed, wf) => (t, T) => open + (closed - open) * clamp01(wf(T));

// ---------- tư thế ----------
const P = (ctx) => {
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
function ladderAt(scene, i) { const lad = ladderOf(); lad.position.set(LAMP_X(i), 0.12, LAMP_Z - 0.85); lad.rotation.x = 0.36; scene.add(lad); return lad; }
const ON_Z = LAMP_Z - 0.58, FOOT_Z = LAMP_Z - 1.15;
// Máy cận mặt kiểu face_ida (Cổng 4 Việc 1): lệch `yaw` độ khỏi hướng mặt, cách `dist` m, ngang mắt.
function faceCam(cam, ch, { yaw = -10, dist = 1.05, y = -0.02, drop = -0.06, fov = 20 } = {}) {
  const head = new THREE.Vector3(); ch.joints.head.getWorldPosition(head); head.y += 0.12;
  const q = new THREE.Quaternion(); ch.joints.head.getWorldQuaternion(q); const fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q); fw.y = 0; fw.normalize();
  const eye = head.clone().add(fw.clone().multiplyScalar(0.08)).add(new THREE.Vector3(0, y, 0));
  const dir = fw.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), yaw * Math.PI / 180);
  const base = eye.clone().addScaledVector(dir, dist); base.y += drop; cam.fov = fov; cam.updateProjectionMatrix(); cam.position.copy(base); cam.lookAt(eye);
}
// Nguồn sáng đèn lồng (bám điểm neo lửa của đèn lồng trong tay/thắt lưng).
function lanternLight(scene, shadow = false, I = 1.6) {
  const L = new THREE.PointLight('#ffa050', 0, 0, 2); if (shadow) { L.castShadow = true; L.shadow.mapSize.set(512, 512); L.shadow.bias = -0.0006; L.shadow.normalBias = 0.02; L.shadow.camera.near = 0.03; } scene.add(L);
  return (ch, f, k = 1) => { const lan = ch.props.lantern; if (!lan || !lan.parent) { L.intensity = 0; return; } lan.updateMatrixWorld(true); lan.userData.lightAnchor.getWorldPosition(L.position); L.intensity = I * k * flickAt(f + 17); };
}
// Đồng hồ bỏ túi bám lòng bàn tay phải, mặt quay về máy.
// Insert: máy đặt theo hướng `dir` cách lòng bàn tay `dist` m; đồng hồ nằm trước ngón tay (3,5 cm về phía máy), mặt quay về máy.
function watchInHand(scene) {
  const w = buildWatch(); scene.add(w);
  return (ch, cam, minDeg, hourDeg, dir = null, dist = 0.3) => { const H = ch.H, p = new THREE.Vector3(0, -ch.sheetRef.parts.hand.palm_length * H * 0.55, 0); ch.joints.wrist_R.localToWorld(p);
    if (dir) { cam.position.copy(p).addScaledVector(dir.clone().normalize(), dist); cam.lookAt(p); }
    w.position.copy(p).addScaledVector(cam.position.clone().sub(p).normalize(), 0.09); w.lookAt(cam.position); w.userData.setHands(minDeg, hourDeg); };
}
const camMM = (mm) => new THREE.PerspectiveCamera(fovOf(mm), 16 / 9, 0.03, 900);

// =====================================================================================================
export const SHOTS = [];
const S = (o) => SHOTS.push(o);

// ---------------- CẢNH 1 — Vòng đèn (0:00–0:26, 26 s) ----------------
S({ id: 's01', scene: 1, t0: 0.0, t1: 4.0, size: 'EWS', angle: 'cao, chúc ~20°', mm: 28, move: 'dolly vào rất chậm',
  why: 'Mở phim đúng lựa chọn 1C: thành phố cuối chạng vạng, đèn khí hiện dần như những tâm hổ phách; đặt thế giới trước khi vào người.',
  sound: 'nhạc tạm (ACE-Step M0) vào nhẹ; room tone gió cao', light: 'trời chạng vạng hồng–tím; đèn khí các phố (chấm hổ phách)',
  action: 'Các chấm hổ phách xuất hiện từng cái một khắp thành phố.',
  async build(ctx) { const c = await buildCitySet(ctx, 'dusk'); return { ...c, exposure: 1.0, update: (t, T) => c.update(t, T) }; } });

S({ id: 's02', scene: 1, t0: 4.0, t1: 8.5, size: 'WS', angle: 'ngang tầm mắt (1,5 m)', mm: 35, move: 'tĩnh',
  why: 'Đặt địa lý phố: đèn đã thắp ở phải (sau lưng Ida), phố chưa thắp phía trái — hướng đi phải→trái giữ suốt cảnh 1–3.',
  sound: 'room tone phố chạng vạng; bước chân; nhạc tạm', light: 'trời chạng vạng + đèn khí L1–L3',
  action: 'Ida vác thang đi từ phải sang trái về cột L4.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 70, x1: 160, shadowLamps: [3] }); const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 });
    const cam = camMM(35); cam.position.set(104.5, 1.5, 4.2); cam.lookAt(110, 1.8, -3.0);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(walkPose(t + 0.3, p.I.walk_ladder), 112.5 - WALK.speed_mps * t, WALK_Z, -Math.PI / 2); } };
  } });

S({ id: 's03', scene: 1, t0: 8.5, t1: 10.5, size: 'MS', angle: 'thấp, hất lên', mm: 50, move: 'tĩnh',
  why: 'Góc thấp cho nghi thức: tay mở van, "phụp", hổ phách nở trên mặt bà.',
  sound: 'kẽo kẹt thang; tiếng xì khí; "phụp" (9,2 s)', light: 'đèn khí L4 vừa mồi (nguồn chính), trời chạng vạng',
  action: 'Ida lên nốt bậc thang, tay phải mở van; ngọn L4 bắt lửa.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 80, x1: 140, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 28 });
    const cam = camMM(50); cam.position.set(103.2, 0.95, -0.2); cam.lookAt(106.0, 3.0, -4.3);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.0,
      update(t, T, f) { st.setState(stdState(T), f);
        const pose = t < 0.55 ? p.climb(0.55 + t / 1.2, p.restLadder) : poseAt([[0.55, p.restLadder], [0.75, p.valveLadder], [1.3, p.valveLadder], [1.9, p.warmLadder]], t);
        const u = clamp01(0.55 + t / 1.2); ida.place(pose, LAMP_X(4), t < 0.55 ? FOOT_Z + (ON_Z - FOOT_Z) * ease(u) : ON_Z, 0); } };
  } });

S({ id: 's04', scene: 1, t0: 10.5, t1: 12.0, size: 'WS', angle: 'cao, từ bên kia phố', mm: 28, move: 'tĩnh',
  why: 'Cho thấy BÓNG của bà (bóng = dấu vết con người, luật thế giới mục 2): bóng dài, mềm trên mặt tiền và đá lát.',
  sound: 'room tone; lửa thở rất khẽ', light: 'đèn khí L4 (có bóng)',
  action: 'Ida trên thang, hai tay đưa lên kính; bóng người + thang đổ dài lên tường nhà.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 80, x1: 140, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 });
    const cam = camMM(28); cam.position.set(99.5, 5.2, 3.2); cam.lookAt(106.5, 1.2, -4.6);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.0,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(poseAt([[0, p.valveLadder], [0.8, p.warmLadder]], t), LAMP_X(4), ON_Z, 0); } };
  } });

S({ id: 's05', scene: 1, t0: 12.0, t1: 16.0, size: 'MCU', angle: 'ngang mắt, 3/4 trước-trái', mm: 85, move: 'tĩnh (khung style frame a_close_ida)',
  why: 'Thói quen hơ tay đếm ba là mô-típ sẽ trả lại ở 2:07 (Cas). Cận đủ để đếm được ba nhịp tay và nghe lời chào con phố.',
  sound: 'THOẠI L1 "Evening, old street." (12,0–14,16); lửa thở', light: 'đèn khí L4 ngay trước mặt (ấm), trời lạnh viền',
  action: 'Hai lòng tay áp gần kính: một, hai, ba (12,3 / 12,9 / 13,5); nói L1; hạ tay.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 90, x1: 125, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'neutral', glint: 0.6 });
    const cam = camMM(85);
    const beats = [12.3, 12.9, 13.5].map((b) => b - 12);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 0.55,
      update(t, T, f) { st.setState(stdState(T), f);
        let k = 0; for (const b of beats) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        const pose = t < 2.4 ? lerpPose(p.warmLadder, p.warmLadderIn, k) : poseAt([[2.4, p.warmLadder], [3.1, p.restLadder]], t);
        ida.place(pose, LAMP_X(4), ON_Z, 0);
        const head = new THREE.Vector3(); ida.joints.head.getWorldPosition(head); head.y += 0.12;
        cam.position.copy(head).add(new THREE.Vector3(-1.55, 0.02, 1.35)); cam.lookAt(head.clone().add(new THREE.Vector3(-0.14, -0.1, 0.22))); } };
  } });

S({ id: 's06', scene: 1, t0: 16.0, t1: 20.0, size: 'CU (insert)', angle: 'chúc nhẹ, góc nhìn của Ida', mm: 100, move: 'tĩnh',
  why: 'Gieo mô-típ đồng hồ chậm 7 phút (4A): gõ kính hai lần là thói quen thân thương; mặt chỉ có vạch, không chữ số.',
  sound: 'hai tiếng gõ kính (16,9 / 17,3); tích tắc rất khẽ', light: 'đèn khí L4 phía trên',
  action: 'Dưới chân thang, Ida mở đồng hồ bỏ túi (7:52 — chậm 7 phút), gõ kính hai lần bằng móng tay, cất đi.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 95, x1: 118, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 30 }); const watch = watchInHand(st.scene);
    const cam = camMM(100);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.4,
      update(t, T, f) { st.setState(stdState(T), f);
        let tap = 0; for (const b of [0.9, 1.3]) tap = Math.max(tap, Math.exp(-(((t - b) / 0.07) ** 2)));
        const pose = t < 3.2 ? p.watchHold(tap) : lerpPose(p.watchHold(0), p.stand, ease((t - 3.2) / 0.7));
        ida.place(pose, LAMP_X(4) + 0.6, LAMP_Z + 0.9, 0.35);
        watch(ida, cam, 312, 236, new THREE.Vector3(-0.15, 0.8, 0.6), 0.32); } };
  } });

S({ id: 's07', scene: 1, t0: 20.0, t1: 24.0, size: 'WS', angle: 'ngang tầm mắt', mm: 35, move: 'dolly ngang theo Ida (phải→trái)',
  why: 'Nhịp sáng–tối của phố đèn khí; bóng bà quét từ trước ra sau khi đi qua cột — cái sẽ mất ở cảnh 2.',
  sound: 'bước chân, thang kẽo kẹt; nhạc tạm', light: 'đèn khí L4, L5 (vừa thắp — lược thời gian)',
  action: 'Ida vác thang đi qua cột L5; bóng đổ ngang đá lát, xoay theo vị trí cột.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 70, x1: 120, shadowLamps: [5] }); const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T), f); const x = 95.2 - WALK.speed_mps * t;
        ida.place(walkPose(t, p.I.walk_ladder), x, WALK_Z, -Math.PI / 2);
        camAt(cam, [[0, [96.0, 1.5, 4.3], [95.0, 1.4, -2.6]], [4, [92.6, 1.5, 4.3], [91.4, 1.4, -2.6]]], t); } };
  } });

S({ id: 's08', scene: 1, t0: 24.0, t1: 26.0, size: 'WS (tele)', angle: 'ngang tầm mắt', mm: 135, move: 'tĩnh',
  why: 'Tele nén phố: Ida nhỏ ở tiền cảnh, quảng trường và cột đồng hồ (chưa sáng) ở xa. Tiếng rơ-le "tách" báo điều sắp đến; bà không để ý.',
  sound: 'rơ-le "tách" xa (24,3); room tone', light: 'đèn khí dọc phố; đồng hồ quảng trường còn tắt',
  action: 'Ida đi về phía máy; xa sau lưng là quảng trường.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 55, x1: 200, shadowLamps: [] }); const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 18 }); const cam = camMM(135); cam.position.set(58, 1.6, 0.6); cam.lookAt(176, 3.4, 0.2);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.4,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(walkPose(t, p.I.walk_ladder), 88.5 - WALK.speed_mps * t, WALK_Z + 0.6, -Math.PI / 2 - 0.12); } };
  } });

// ---------------- CẢNH 2 — Bật điện (0:26–0:44, 18 s) ----------------
S({ id: 's09', scene: 2, t0: 26.0, t1: 30.0, size: 'MS', angle: 'thấp, hất lên cột đồng hồ', mm: 50, move: 'tĩnh',
  why: 'Thứ sáng đầu tiên của lưới điện là đồng hồ (luật thế giới mục 1): giờ mới, đúng giờ, lạnh. Góc thấp cho nó uy thế nhưng không phản diện.',
  sound: 'rơ-le; mặt kính bật; chuông điện "DING" (27,0); rè điện bắt đầu', light: 'mặt đồng hồ kính mờ phát trắng (nguồn mới)',
  action: 'Mặt đồng hồ sáng trắng; hai kim đứng đúng giờ (8:00); chuông đánh một tiếng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 150, x1: 200, shadowLamps: [] });
    const cam = camMM(50); cam.position.set(169.2, 1.7, -3.4); cam.lookAt(176, 6.3, 0.5);
    const cl = new THREE.PointLight('#e8eeff', 0, 14, 1.5); cl.position.set(CLOCK.x - 0.6, CLOCK.h, CLOCK.z); st.scene.add(cl);
    return { scene: st.scene, cam, named: {}, paintP: PAINT_STREET, exposure: 1.7,
      update(t, T, f) { const s0 = stdState(T); st.setState(s0, f); st.clock.userData.setHands(0, 240); cl.intensity = 30 * s0.clock; } };
  } });

S({ id: 's10', scene: 2, t0: 30.0, t1: 34.0, size: 'EWS', angle: 'cao, sau quảng trường', mm: 28, move: 'tĩnh',
  why: 'Toàn cảnh lặp lại khung mở đầu để đo thay đổi: tấm kính quanh quảng trường nhấp hai lần rồi đứng; từng khối phố bật lan xuống dốc.',
  sound: 'rè điện lớn dần; các tiếng "tách" nối tiếp', light: 'đèn điện (trắng phẳng) lan khỏi quảng trường; đèn khí còn lại',
  action: 'Sóng trắng lăn xuống dốc theo phố Ostler.',
  async build(ctx) { const c = await buildCitySet(ctx, 'wave'); return { ...c, exposure: 1.0, grade: GRADE_COLD }; } });

S({ id: 's11', scene: 2, t0: 34.0, t1: 37.0, size: 'MS', angle: 'ngang, 3/4 trước-trái', mm: 50, move: 'tĩnh',
  why: 'Phản ứng: bà quay về phía quảng trường (phải khung = hướng sóng tới).',
  sound: 'rè điện từ xa; tách', light: 'đèn khí L7 vừa thắp (ấm), ánh trắng lờ mờ phía xa',
  action: 'Ida trên thang ở cột L7, quay đầu và vai về phía quảng trường.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 28 }); const cam = camMM(50); cam.position.set(61.6, 2.5, -1.2); cam.lookAt(64.0, 2.9, -4.4);
    const wf = whiteAt(64);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 0.3 * wf(T) }), f); ida.place(poseAt([[0, p.restLadder], [0.4, p.restLadder], [1.5, p.turnSquare]], t), LAMP_X(7), ON_Z, 0); } };
  } });

S({ id: 's12', scene: 2, t0: 37.0, t1: 40.0, size: 'WS (qua vai)', angle: 'cao ngang vai Ida, nhìn lên phố', mm: 35, move: 'tĩnh',
  why: 'Qua vai bà: thấy trắng nuốt những ngọn bà vừa thắp (L5, L6) — vũng hổ phách mỏng dần, dải tối giữa các cột biến mất.',
  sound: 'tách (38,2); rè điện', light: 'cột điện x=85 bật; đèn khí L5, L6 chìm trong trắng',
  action: 'Lưng/vai Ida tiền cảnh trái; phía xa phố trắng dần.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 55, x1: 160, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35); cam.position.set(62.3, 3.4, -5.0); cam.lookAt(100, 1.8, -1.0);
    const wf = whiteAt(85);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.2, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 0.5 * wf(T) }), f); ida.place(p.turnSquare, LAMP_X(7), ON_Z, 0); } };
  } });

S({ id: 's13', scene: 2, t0: 40.0, t1: 42.0, size: 'MS', angle: 'thấp nhẹ, 3/4 trước-phải', mm: 50, move: 'tĩnh',
  why: 'Sóng tới chính bà: mặt bà đổi từ ấm sang trắng phẳng; bà nhìn xuống.',
  sound: 'rè điện gần; tách', light: 'trắng tràn tới (nhấp 2 lần), đèn khí L7 còn đó nhưng chìm',
  action: 'Trắng tràn lên người Ida; bà cúi nhìn xuống đá lát.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 28 }); const cam = camMM(50); cam.position.set(66.8, 2.0, -1.0); cam.lookAt(64.0, 2.9, -4.4);
    const wf = (T) => switchOn(T, 40.05);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.1, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 1.2 * wf(T) }), f); ida.place(poseAt([[0, p.turnSquare], [0.5, p.turnSquare], [1.3, p.lookDown]], t), LAMP_X(7), ON_Z, 0); } };
  } });

S({ id: 's14', scene: 2, t0: 42.0, t1: 44.0, size: 'MS (chúc)', angle: 'cao, chúc xuống đá lát', mm: 28, move: 'tĩnh',
  why: 'Hình then chốt cảnh 2: bóng dài đã mất; bà giơ tay — không gì động trên đá lát.',
  sound: 'rè điện đều; im', light: 'trắng phẳng (không bóng); vệt tối mờ dưới chân thang',
  action: 'Ida giơ tay trái lên; nền đá không có bóng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 90, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cam = camMM(28); cam.position.set(63.0, 4.9, -2.3); cam.lookAt(64.3, 0.2, -4.2);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.2 }), f); ida.place(poseAt([[0, p.lookDown], [0.5, p.lookDown], [1.2, p.liftHand]], t), LAMP_X(7), ON_Z, 0); } };
  } });

// ---------------- CẢNH 3 — Chạy đua (0:44–1:08, 24 s) ----------------
// Montage nén thời gian: mỗi shot có nhịp "nở hổ phách → trắng phủ" riêng; cột điện bật theo POST_ON.
S({ id: 's15', scene: 3, t0: 44.0, t1: 46.0, size: 'WS', angle: 'ngang tầm mắt', mm: 35, move: 'tĩnh',
  why: 'Bà xuống thang, quay nhìn ngược dốc về quảng trường (phải khung) — dẫn vào nhịp đồng hồ.',
  sound: 'bước xuống thang; rè điện', light: 'trắng phẳng (cột x=85); đèn khí L7 chìm',
  action: 'Ida xuống thang, quay người nhìn về phía đồng hồ.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35); cam.position.set(58.2, 1.5, 3.2); cam.lookAt(63.8, 1.6, -4.2);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        if (t < 1.1) { const u = 1 - t / 1.1; ida.place(p.climb(u, p.restLadder), LAMP_X(7), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); }
        else ida.place(poseAt([[1.1, p.stand], [1.8, over(p.stand, { joints: { neck: [-10, 0, 0] } })]], t), LAMP_X(7) + 0.2, FOOT_Z + 0.5, valAt([[1.1, 0], [1.8, Math.PI / 2]], t)); } };
  } });

S({ id: 's16', scene: 3, t0: 46.0, t1: 48.5, size: 'CU', angle: 'tele, góc nhìn của Ida (POV)', mm: 200, move: 'tĩnh',
  why: 'Match cut 8B, vế 1: mặt đồng hồ quảng trường, kim phút vừa qua đỉnh.',
  sound: 'rè điện; tích tắc', light: 'mặt đồng hồ phát trắng',
  action: 'Mặt đồng hồ điện: 8:00:30, kim phút lệch phải đỉnh 3°.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 140, x1: 200, shadowLamps: [] }); const cam = camMM(200); cam.position.set(150, 6.2, 0.4); cam.lookAt(CLOCK.x, CLOCK.h, CLOCK.z);
    return { scene: st.scene, cam, named: {}, paintP: PAINT_CLOSE, exposure: 1.2, grade: GRADE_COLD,
      update(t, T, f) { st.setState(stdState(T), f); st.clock.userData.setHands(3 + 6 * t / 60, 240.25); } };
  } });

S({ id: 's17', scene: 3, t0: 48.5, t1: 51.0, size: 'CU (insert)', angle: 'POV của Ida, tay duỗi', mm: 105, move: 'tĩnh',
  why: 'Match cut 8B, vế 2: cùng vị trí, cùng cỡ — đồng hồ bỏ túi, kim phút còn cách đỉnh 42° (7 phút). "Trễ" đọc bằng hình, không chữ.',
  sound: 'tích tắc gần', light: 'trắng phẳng',
  action: 'Đồng hồ bỏ túi giơ ngang tầm mắt: 7:53:30.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 50, x1: 110, shadowLamps: [] }); const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 28 }); const watch = watchInHand(st.scene); const cam = camMM(105);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f); ida.place(p.watchRaise, 64.3, FOOT_Z + 0.5, Math.PI / 2);
        const wp = new THREE.Vector3(0, -0.07, 0); ida.joints.wrist_R.localToWorld(wp);
        const eye = new THREE.Vector3(); ida.joints.head.getWorldPosition(eye); eye.y += 0.1;
        watch(ida, cam, 321 + 6 * t / 60, 236.8, eye.sub(wp).normalize().add(new THREE.Vector3(0, 0.55, 0)), 0.3); } };
  } });

S({ id: 's18', scene: 3, t0: 51.0, t1: 52.4, size: 'MS', angle: 'ngang', mm: 50, move: 'tĩnh',
  why: 'Lần đầu sau bốn mươi năm bà trễ: một hơi cười khô, rồi vác thang đi nhanh.',
  sound: 'hơi thở cười khẽ (chờ SFX/giọng có giấy phép — để trống); bước nhanh', light: 'trắng phẳng',
  action: 'Ida hạ đồng hồ, quay người về phía dốc xuống (trái khung).',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 40, x1: 95, shadowLamps: [] }); const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 26 }); const cam = camMM(50); cam.position.set(61.2, 1.55, 1.1); cam.lookAt(64.3, 1.5, -4.2);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        const pose = poseAt([[0, p.watchRaise], [0.5, p.stand], [0.9, over(p.stand, { props: ['ladder_shoulder', 'lantern_belt'], joints: p.I.walk_ladder.joints })]], t);
        ida.place(pose, 64.3, FOOT_Z + 0.5, valAt([[0, Math.PI / 2], [0.5, Math.PI / 2], [1.3, -Math.PI / 2]], t)); } };
  } });

const lampShot = (id, t0, t1, i, cam0, why, extra = {}) => S({ id, scene: 3, t0, t1, size: 'WS', angle: extra.angle || 'ngang', mm: extra.mm || 35, move: 'tĩnh', why,
  sound: `"phụp" L${i} (${GAS_ON[i]} s); tách + rè khi cột điện bật`, light: `đèn khí L${i} vừa thắp (có bóng) → trắng phủ`,
  action: extra.action || `Ida trên thang ở L${i}: hổ phách nở, bóng dài; vài giây sau trắng phủ, bóng tan trong 0,5 s.`,
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: LAMP_X(i) - 30, x1: LAMP_X(i) + 30, shadowLamps: [i] }); const p = P(ctx); ladderAt(st.scene, i);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cam = camMM(extra.mm || 35); cam.position.set(...cam0[0]); cam.lookAt(...cam0[1]);
    const wf = whiteAt(LAMP_X(i));
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.15, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 1.1 * wf(T) }), f);
        ida.place(poseAt([[0, p.valveLadder], [0.5, p.valveLadder], [1.2, p.warmLadder]], t), LAMP_X(i), ON_Z, 0); } };
  } });
lampShot('s19', 52.4, 55.4, 8, [[44.6, 1.6, 3.0], [50.0, 2.4, -4.6]], 'Montage: ngọn thứ 8 nở hổ phách, bóng bà đổ dài — rồi cột điện x=57 bật, trắng xoá bóng.');
lampShot('s20', 55.4, 58.0, 9, [[39.6, 0.55, 0.9], [36.0, 2.8, -4.6]], 'Montage: ngọn thứ 9, góc thấp khác để nhịp lặp không nhàm; trắng tới nhanh hơn.', { mm: 28, angle: 'thấp' });

S({ id: 's21', scene: 3, t0: 58.0, t1: 60.0, size: 'MCU (tay)', angle: 'ngang, 3/4', mm: 85, move: 'tĩnh',
  why: 'Vội: trèo quá nhanh, tuột sào mồi rồi chụp lại — lần đầu thấy tay bà không vững.',
  sound: 'thang rung; sào gỗ va; hơi thở gấp', light: 'trắng phẳng; L10 chưa thắp',
  action: 'Ida trèo nhanh lên L10, sào mồi trượt khỏi tay (58,9), chụp lại (59,4).',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 0, x1: 50, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 10);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 32 }); const cam = camMM(85); cam.position.set(20.1, 3.1, -2.3); cam.lookAt(22.0, 3.0, -4.5);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.0 }), f);
        const pose = t < 0.7 ? lerpPose(p.climb(0.4 + t / 1.2, p.poleLadder), p.poleLadder, 0) : poseAt([[0.7, p.poleLadder], [0.9, p.poleFumble], [1.3, p.poleFumble], [1.5, p.poleLadder]], t);
        ida.place(t < 0.7 ? { ...pose, props: ['pole_hand_R', 'lantern_belt'] } : pose, LAMP_X(10), t < 0.7 ? FOOT_Z + (ON_Z - FOOT_Z) * ease(0.4 + t / 1.2) : ON_Z, 0);
        const pole = ida.props.pole; if (pole && t > 0.85 && t < 1.45) pole.rotation.z = 0.5 * Math.sin((t - 0.85) / 0.6 * Math.PI); else if (pole) pole.rotation.z = 0; } };
  } });

S({ id: 's22', scene: 3, t0: 60.0, t1: 63.0, size: 'MCU', angle: 'ngang mắt, 3/4', mm: 85, move: 'tĩnh',
  why: 'Lời thoại duy nhất của cảnh chạy đua; ngọn L10 bắt lửa ấm lên mặt bà rồi bị trắng dìm ngay.',
  sound: 'THOẠI L2 "Not yet... not yet." (60,0–62,88); "phụp" (62,95, sau câu thoại, tràn qua điểm cắt)', light: 'trắng phẳng; đèn khí L10 bắt lửa ở khung cuối (ấm lên mặt)',
  action: 'Ida lẩm bẩm, mở van; lửa bắt ngay khi câu dứt; hổ phách chìm trong trắng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 5, x1: 40, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 10);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'strained', glint: 0.5 }); const cam = camMM(85);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 0.8,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.0 }), f);
        ida.place(poseAt([[0, over(p.valveLadder, { joints: { neck: [-4, 30, 0] } })], [1.6, over(p.valveLadder, { joints: { neck: [-4, 30, 0] } })], [2.4, over(p.warmLadder, { joints: { neck: [-4, 30, 0] } })]], t), LAMP_X(10), ON_Z, 0);
        faceCam(cam, ida, { yaw: -12, dist: 1.2, fov: fovOf(85) }); } };
  } });

S({ id: 's23', scene: 3, t0: 63.0, t1: 66.0, size: 'WS', angle: 'ngang, nhìn xuôi dốc về nhà kho', mm: 28, move: 'tĩnh',
  why: 'Ngọn cuối cùng cạnh bức tường vôi nhà kho; cột điện khối cuối còn TỐI (khe thời gian — luật thế giới mục 1).',
  sound: 'bước chạy; thang; "phụp" (65,0)', light: 'L11 bắt lửa; cột điện x=11 còn tắt; trắng từ phía sau',
  action: 'Ida hối hả tới L11, trèo, thắp. Hổ phách.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 40, shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(28); cam.position.set(19.0, 1.7, 2.6); cam.lookAt(5.5, 2.0, -3.8);
    const fast = { cycle_s: 0.9, stride_m: 0.6, speed_mps: 1.3 };
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(1.6, 1.3, (T) => 1 - gasLevel(11, T)),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.55 }), f);
        if (t < 1.1) ida.place(over(walkPose(t, p.I.walk_ladder, { gait: fast }), { props: ['lantern_belt'] }), valAt([[0, 14.2], [1.1, LAMP_X(11) + 0.2]], t), valAt([[0, WALK_Z], [1.1, FOOT_Z]], t), yawTo(14.2, WALK_Z, LAMP_X(11), FOOT_Z));
        else if (t < 1.9) { const u = (t - 1.1) / 0.8; ida.place(p.climb(u, p.valveLadder), LAMP_X(11), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); }
        else ida.place(poseAt([[1.9, p.valveLadder], [2.5, p.warmLadder]], t), LAMP_X(11), ON_Z, 0); } };
  } });

S({ id: 's24', scene: 3, t0: 66.0, t1: 68.0, size: 'MS', angle: 'hơi cao, 3/4 trước-phải', mm: 35, move: 'tĩnh',
  why: 'Nhịp đếm ba lần thứ hai; ở nền, cậu bé đứng ở tường nhìn bà — bà không thấy (gieo cảnh 4).',
  sound: 'lửa thở; im lặng tương đối', light: 'đèn khí L11 (ấm) — vùng cuối phố chưa có điện',
  action: 'Ida áp tay vào kính: một, hai, ba (66,2 / 66,8 / 67,4). Xa phía sau, Cas nhìn.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 30 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(35); cam.position.set(14.5, 2.4, 3.0); cam.lookAt(6.0, 2.2, -2.3);
    const beats = [0.2, 0.8, 1.4];
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.6,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.3 }), f);
        let k = 0; for (const b of beats) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        ida.place(lerpPose(p.warmLadder, p.warmLadderIn, k), LAMP_X(11), ON_Z, 0);
        cas.place(p.C.turnaround, -2.6, -1.6, yawTo(-2.6, -1.6, 8, -4.5)); } };
  } });

// ---------------- CẢNH 4 — Bức tường (1:08–1:34, 26 s) ----------------
const wallShot = (id, t0, t1, meta, fn) => S({ id, scene: 4, t0, t1, ...meta,
  async build(ctx) {
    const W = buildWallSet(ctx); const p = P(ctx);
    const cas = makeChar(ctx, W.scene, 'cas', { detail: meta.casDetail ?? 30, expr: meta.casExpr }); const ida = makeChar(ctx, W.scene, 'ida', { detail: meta.idaDetail ?? 24, expr: meta.idaExpr, hatBack: 0, glint: meta.idaGlint });
    const cam = camMM(meta.mm);
    const lan = lanternLight(W.scene, false, 0);
    const ctl = fn(p, cam);
    return { scene: W.scene, cam, named: { ida, cas }, paintP: PAINT_WALL, exposure: ctl.exposure ?? 2.6,
      update(t, T, f) {
        const e = switchOn(T, POST_ON[5]);
        const r = ctl.update(t, T, { ida, cas, cam, e });
        const lp = new THREE.Vector3(); let lk = 0;
        if (ida.props.lantern && ida.props.lantern.parent) { ida.props.lantern.updateMatrixWorld(true); ida.props.lantern.userData.lightAnchor.getWorldPosition(lp); lk = r?.lantern ?? 0.06; }
        W.setState({ gas: 1, elec: e, lantern: lk, lanternPos: lp }, f);
      } };
  } });
const BIRD_CAM = [[2.2, 1.3, 3.6], [0.3, 1.1, 0]];
wallShot('s25', 68.0, 73.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'dolly vào rất chậm (0,3 m)',
  why: 'Giới thiệu Cas bằng việc cậu làm: chim bóng từ đèn khí L11 (khung style frame b_cas_bird).', sound: 'lửa thở; vải sột soạt; im',
  light: 'đèn khí L11 (key, có bóng) — cột điện cạnh tường còn tắt', action: 'Cas giơ hai tay làm chim; chim vỗ cánh chậm trên tường vôi.' },
  (p, cam) => ({ update(t, T, { ida, cas }) { cas.place(p.bird(t, 1.0), 0.15, 0.95, Math.PI + 0.15); ida.place(p.stand, -3.4, 5.4, 2.5);
    camAt(cam, [[0, BIRD_CAM[0], BIRD_CAM[1]], [5, [2.0, 1.3, 3.3], BIRD_CAM[1]]], t); } }));
wallShot('s26', 73.0, 76.0, { size: 'MS', angle: 'ngang, 3/4 trước-trái Ida', mm: 50, move: 'tĩnh', idaExpr: 'neutral', idaDetail: 32, idaGlint: 0.02,
  why: 'Ida xuống thang, đứng xem, không gọi. Đèn lồng ở thắt lưng vẫn cháy (gieo cho 1:26).', sound: 'lửa thở',
  light: 'đèn khí L11 sau lưng Ida; đèn lồng thắt lưng', action: 'Ida đứng cạnh cột L11 nhìn Cas.' },
  (p, cam) => ({ exposure: 2.6, update(t, T, { ida, cas }) { cas.place(p.bird(t + 5, 1.0), 0.15, 0.95, Math.PI + 0.15);
    ida.place(over(p.stand, { joints: { neck: [4, 0, 0] } }), -1.8, 4.7, yawTo(-1.8, 4.7, 0.15, 0.95)); cam.position.set(0.3, 1.5, 3.1); cam.lookAt(-1.8, 1.5, 4.7); } }));
wallShot('s27', 76.0, 80.0, { size: 'WS', angle: 'ngang, sau-phải', mm: 28, move: 'tĩnh',
  why: 'Khối cuối bật: tách, nhấp hai lần, đứng. Trắng phủ tường; chim nhạt dần trong 12 khung (luật 3.3) — tay vẫn còn, chỉ mất bóng.',
  sound: 'rơ-le "tách" (76,0); rè điện', light: 'cột điện cạnh tường bật (76,3) — trắng phẳng; đèn khí L11 còn nhưng chìm',
  action: 'Chim bóng xám dần rồi mất; tay Cas vẫn vỗ.' },
  (p, cam) => ({ exposure: (t, T) => 2.6 - 1.3 * switchOn(T, POST_ON[5]), update(t, T, { ida, cas }) { cas.place(p.bird(t + 8, 1.0), 0.15, 0.95, Math.PI + 0.15);
    ida.place(p.stand, -1.8, 4.7, yawTo(-1.8, 4.7, 0.15, 0.95)); cam.position.set(3.4, 1.6, 5.4); cam.lookAt(0, 1.5, 0); } }));
wallShot('s28', 80.0, 83.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'tĩnh',
  why: 'Cas vỗ mạnh hơn vào bức tường trống — không gì cả.', sound: 'rè điện; vải', light: 'trắng phẳng',
  action: 'Cas vỗ tay nhanh, mạnh; tường trắng trơn.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) { cas.place(p.bird(t, 2.1, 1.8), 0.15, 0.95, Math.PI + 0.15); ida.place(p.stand, -3.4, 5.4, 2.5); cam.position.set(...BIRD_CAM[0]); cam.lookAt(...BIRD_CAM[1]); } }));
wallShot('s29', 83.0, 86.0, { size: 'MCU', angle: 'ngang mắt Cas, 3/4 trước-phải', mm: 85, move: 'tĩnh', casDetail: 36,
  why: 'Cas hạ tay, quay lại, thấy bà — rồi thấy đèn lồng hổ phách ở thắt lưng bà. Cậu không xin.', sound: 'rè điện; im',
  light: 'trắng phẳng; phản ánh ấm rất nhẹ của đèn lồng', action: 'Cas hạ tay, xoay người về phía Ida (trái khung), nhìn xuống đèn lồng.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) {
    const yaw = valAt([[0, Math.PI + 0.15], [0.9, Math.PI + 0.15], [1.9, yawTo(0.15, 0.95, -1.8, 4.7)]], t);
    cas.place(poseAt([[0, p.bird(0, 1)], [0.8, p.C.turnaround], [2.0, over(p.C.turnaround, { joints: { neck: [22, 0, 0] } })]], t), 0.15, 0.95, yaw);
    ida.place(p.stand, -1.8, 4.7, yawTo(-1.8, 4.7, 0.15, 0.95));
    cam.position.set(1.7, 1.1, 2.8); cam.lookAt(0.1, 1.05, 1.0); } }));
wallShot('s30', 86.0, 88.0, { size: 'MS', angle: 'ngang, sau-phải', mm: 35, move: 'tĩnh', idaDetail: 28,
  why: 'Ida tháo đèn lồng, quỳ cạnh cậu, cầm thấp sau tay cậu, cách tường một sải tay (≤ 0,7 m — luật 3.3).', sound: 'kim loại quai đèn; vải',
  light: 'đèn lồng tới gần tường (ấm) trong nền trắng', action: 'Ida tháo đèn lồng, quỳ một gối bên trái Cas.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) {
    cas.place(over(p.C.turnaround, { joints: { neck: [18, 0, 0] } }), 0.15, 0.95, yawTo(0.15, 0.95, -0.55, 1.35));
    const pose = poseAt([[0, over(p.stand, { props: ['lantern_hand_R'], joints: { shoulder_R: [-20, 0, -10] } })], [0.4, over(p.stand, { props: ['lantern_hand_R'], joints: { shoulder_R: [-20, 0, -10] } })], [1.4, p.crouch]], t);
    ida.place(pose, -0.55, 1.35, yawTo(-0.55, 1.35, 0.15, 0.3)); cam.position.set(2.6, 1.4, 4.0); cam.lookAt(-0.1, 0.8, 0.7); return { lantern: 0.8 + 2.4 * ease((t - 0.8) / 1.0) }; } }));
wallShot('s31', 88.0, 91.0, { size: 'MCU', angle: 'ngang mắt Ida (quỳ), 3/4 sau-phải', mm: 85, move: 'tĩnh', idaExpr: 'sad_smile', idaDetail: 36,
  why: 'Lời mời, không dạy: bà đưa ánh sáng, cậu tự làm.', sound: 'THOẠI L3 "Go on, then." (88,0–90,3)',
  light: 'đèn lồng ấm dưới mặt bà; trắng phẳng từ trên', action: 'Ida quỳ, quay đầu về Cas, nói L3.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) {
    cas.place(over(p.C.turnaround, { joints: { neck: [18, 0, 0] } }), 0.15, 0.95, yawTo(0.15, 0.95, -0.55, 1.35));
    ida.place(over(p.crouch, { joints: { neck: [-6, -27, 0] } }), -0.55, 1.35, yawTo(-0.55, 1.35, 0.15, 0.3));
    const h = new THREE.Vector3(); ida.joints.head.getWorldPosition(h); h.y += 0.1; cam.position.set(0.75, h.y + 0.05, 1.6); cam.lookAt(h.x, h.y - 0.02, h.z); return { lantern: 3.2 }; } }));
wallShot('s32', 91.0, 94.0, { size: 'WS', angle: 'ngang, sau-phải', mm: 35, move: 'tĩnh',
  why: 'Chim trở lại, TO hơn, ấm, rìa mềm (tay gần nguồn — luật 3.2, 3.3) và bay.', sound: 'Cas cười khẽ (chờ SFX có giấy phép — để trống); nhạc tạm vào',
  light: 'đèn lồng thấp sau tay Cas (key ấm, có bóng) trong nền trắng', action: 'Cas giơ tay vào quầng hổ phách; chim to hiện trên tường và bay.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) {
    const bird = p.bird(t, 1.2); const sw = Math.sin(t * 0.9) * 10;
    cas.place(poseAt([[0, p.C.turnaround], [0.8, over(bird, { joints: { spine: [-4, sw, 0] } })]], t), 0.15, 0.95, Math.PI + 0.15);
    ida.place(p.crouch, -0.55, 1.35, yawTo(-0.55, 1.35, 0.15, 0.3)); cam.position.set(1.8, 1.3, 3.9); cam.lookAt(-0.2, 1.4, 0); return { lantern: 6.0 }; } }));

// ---------------- CẢNH 5 — Ngọn cuối (1:34–2:10, 36 s) ----------------
S({ id: 's33', scene: 5, t0: 94.0, t1: 102.0, size: 'WS', angle: 'ngang 1,35 m, "tranh trong tranh"', mm: 32, move: 'dolly vào chậm (1 m)',
  why: 'Hình trung tâm (7A, khung style frame c_s5_wide): trong hốc cửa khuất điện, đèn lồng dưới đất, hai bóng người vươn cao lên vách; ngoài vòm phố trắng không bóng.',
  sound: 'nhạc tạm; bước chân vào hốc; rè điện xa', light: 'đèn lồng trên nền đá (nguồn thấp); ngoài vòm: điện phẳng',
  action: 'Ida đặt đèn lồng, hai người bước qua, đứng giữa đèn và vách; hai bóng hiện.',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}); const p = P(ctx); const cam = r.cam; const c0 = cam.position.clone();
    for (const ch of [r.chIda, r.chCas]) { ch.sheetRef = ch.sheet; }
    const keep = () => { if (!r.lan.parent) r.scene.add(r.lan); };
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT, grade: GRADE_S5, exposure: 1.0,
      update(t) {
        const zI = valAt([[0, 3.5], [1.2, 3.5], [3.8, 1.0]], t), zC = valAt([[0, 3.9], [1.5, 3.9], [4.1, 1.0]], t);
        const pI = t < 1.2 ? lerpPose(p.crouch, p.stand, ease(t / 1.2)) : t < 3.8 ? over(walkPose(t - 1.2, p.stand), { props: [] }) : poseAt([[3.8, over(p.stand, { props: [] })], [4.8, over(p.lookShadows, { props: [] })]], t);
        const pC = t < 1.5 ? p.C.turnaround : t < 4.1 ? walkPose(t - 1.5, p.C.turnaround, { gait: WALK_CHILD, bothArms: true }) : poseAt([[4.1, p.C.turnaround], [5.5, p.C.half_raised]], t);
        r.chIda.setPose({ ...pI, props: [] }); keep(); r.chIda.root.position.set(-0.42, pI.root_y_m ?? 0, zI); r.chIda.root.rotation.y = Math.PI + 0.30 * clamp01((t - 3.5) / 0.8); r.chIda.root.updateMatrixWorld(true);
        r.chCas.setPose(pC); keep(); r.chCas.root.position.set(0.40, pC.root_y_m ?? 0, zC); r.chCas.root.rotation.y = Math.PI - 0.25 * clamp01((t - 3.8) / 0.8); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) { ctx.upd(r.chIda, cam); ctx.upd(r.chCas, cam); }
        cam.position.copy(c0).add(new THREE.Vector3(0, 0, -1.0 * ease(t / 8))); } };
  } });

S({ id: 's34', scene: 5, t0: 102.0, t1: 104.0, size: 'MS (qua vai)', angle: '3/4 sau-phải, cạnh đèn lồng', mm: 35, move: 'tĩnh',
  why: 'Ida nhìn hai cái bóng một lúc lâu (khung style frame c_s5_medium).', sound: 'lửa thở; nhạc tạm',
  light: 'đèn lồng sau lưng, viền má và mép mũ', action: 'Ida ngửa nhìn bóng, tay đặt lên ngực.',
  async build(ctx) {
    const r = await buildBaySet(ctx, { medium: 1 }); const p = P(ctx); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    return { scene: r.scene, cam: r.cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: 1.0, update() {} };
  } });

// Bộ phố cuối (L11) sau khi mọi cột điện đã bật: L11 nhạt (vệt hổ phách yếu trong trắng).
const endStreet = (o = {}) => buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: o.shadowLamps || [] });
S({ id: 's35', scene: 5, t0: 104.0, t1: 108.0, size: 'WS', angle: 'ngang, xuôi dốc', mm: 28, move: 'tĩnh',
  why: 'Ngọn cuối còn cháy nhạt trong trắng; bà trèo lên lần cuối, Cas theo và giữ thang bằng hai tay.', sound: 'bước chân; thang; rè điện',
  light: 'đèn khí L11 nhạt (vệt vàng yếu); điện phẳng khắp phố', action: 'Ida bước ra khỏi hốc, tới thang, trèo; Cas chạy theo giữ thang.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(28); cam.position.set(16.5, 1.7, 2.6); cam.lookAt(5.5, 1.8, -3.8);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        if (t < 1.6) ida.place(over(walkPose(t, p.stand), { props: [] }), valAt([[0, 3.2], [1.6, LAMP_X(11)]], t), valAt([[0, -1.6], [1.6, FOOT_Z]], t), yawTo(3.2, -1.6, LAMP_X(11), FOOT_Z));
        else if (t < 2.8) { const u = (t - 1.6) / 1.2; ida.place(p.climb(u, p.restLadder), LAMP_X(11), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); } else ida.place(p.restLadder, LAMP_X(11), ON_Z, 0);
        if (t < 2.4) cas.place(walkPose(t, p.C.turnaround, { gait: WALK_CHILD, bothArms: true }), valAt([[0, 2.2], [2.4, 8.0]], t), valAt([[0, -1.2], [2.4, -5.25]], t), yawTo(2.2, -1.2, 8.0, -5.25));
        else cas.place(poseAt([[2.4, p.C.turnaround], [3.0, p.C.hold_ladder]], t), 8.0, -5.25, 0); } };
  } });

const faceShot = (id, t0, t1, meta, fn) => S({ id, scene: 5, t0, t1, ...meta,
  async build(ctx) {
    const st = endStreet({ shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: meta.expr, gaze: [0.05, -0.04], glint: 0.45 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(meta.mm); const ctl = fn(p, cam);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: ctl.exposure ?? 0.9,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f); cas.place(p.C.hold_ladder, 8.0, -5.25, 0); ctl.update(t, T, ida); } };
  } });
faceShot('s36', 108.0, 110.0, { size: 'MCU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'tĩnh', expr: 'neutral',
  why: 'Quyết định C4 của chủ dự án: bà TỰ đẩy vành mũ ra sau trước câu thoại — mặt thoáng ra cho lời từ biệt.', sound: 'vải dạ; hơi thở',
  light: 'đèn khí L11 nhạt + trắng phẳng', action: 'Tay trái đưa lên vành mũ (hat_push_a), đẩy vành lên, mũ ngả ra sau (hat_push_b).' },
  (p, cam) => ({ update(t, T, ida) { ida.place(poseAt([[0, p.hatA], [0.35, p.hatA], [1.05, p.hatB], [1.6, p.faceRest()]], t), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: 1.9, y: -0.05, fov: fovOf(85) }); } }));
faceShot('s37', 110.0, 117.0, { size: 'CU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'đẩy vào rất chậm', expr: 'sad_smile',
  why: 'Lời từ biệt, vế đầu: cười buồn. Máy đẩy vào không nhận ra được, để khán giả lại gần bà.', sound: 'THOẠI L4 (110,0–…) "That\'s the last one, then. Goodnight, old street."',
  light: 'đèn khí L11 nhạt (ấm yếu một bên mặt) + trắng phẳng', action: 'Ida nhìn lên phố (phải khung), tay đặt trên van.' },
  (p, cam) => ({ update(t, T, ida) { ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: valAt([[0, 1.1], [7, 0.95]], t), fov: fovOf(85) }); } }));
S({ id: 's38', scene: 5, t0: 117.0, t1: 119.5, size: 'MS', angle: 'cao, chúc xuống (gần mắt Ida)', mm: 50, move: 'tĩnh',
  why: 'Phản ứng của Cas: cậu giữ thang, ngước nhìn bà — người nghe câu nói thay khán giả.', sound: 'L4 tiếp (ngoài hình)',
  light: 'trắng phẳng; ấm rất yếu từ L11 trên cao', action: 'Cas giữ thang, ngửa mặt nhìn lên.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 20 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34 });
    const cam = camMM(50); cam.position.set(9.1, 2.35, -3.7); cam.lookAt(8.0, 1.0, -5.25);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f); ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); cas.place(over(p.C.hold_ladder, { joints: { neck: [-36, 0, 0] } }), 8.0, -5.25, 0.25); } };
  } });
faceShot('s39', 119.5, 124.1, { size: 'CU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'tĩnh', expr: 'choked',
  why: 'Vế cuối, giọng vỡ: "keep a little dark for the ones who need it" — chủ đề phim trong một câu.', sound: 'THOẠI L4 (…–124,08) "You\'ll be brighter now. Just... keep a little dark for the ones who need it."',
  light: 'đèn khí L11 nhạt + trắng phẳng', action: 'Ida nghẹn, một giọt nước mắt; mắt vẫn nhìn lên phố.' },
  (p, cam) => ({ update(t, T, ida) { ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: 0.95, fov: fovOf(85) }); } }));

S({ id: 's40', scene: 5, t0: 124.1, t1: 125.6, size: 'CU (insert)', angle: 'ngang van', mm: 100, move: 'tĩnh',
  why: 'Hành động không lời: tay vặn van, ngọn đèn khí cuối cùng của thành phố tắt.', sound: 'van kim loại; tiếng xì tắt',
  light: 'ngọn L11 tắt (124,6); trắng phẳng không đổi', action: 'Tay phải Ida gạt van; lửa co lại và tắt.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 30 }); const cam = camMM(100);
    const l11 = st.lamps[10]; const lever = l11.lamp.userData.parts.lever; const fp = l11.fp;
    cam.position.copy(fp).add(new THREE.Vector3(0.5, -0.05, 0.5)); cam.lookAt(fp.clone().add(new THREE.Vector3(0, -0.08, 0)));   // lồng kính + ngọn lửa, van ở mép dưới khung
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f); ida.place(p.valveLadder, LAMP_X(11), ON_Z, 0); lever.rotation.z = valAt([[0, -0.5], [0.3, -0.5], [0.7, 0.7]], t); } };
  } });

S({ id: 's41', scene: 5, t0: 125.6, t1: 127.0, size: 'WS', angle: 'ngang', mm: 28, move: 'tĩnh',
  why: '"Không gì khác thay đổi": phố trắng y nguyên. Dưới chân thang bà trao đèn lồng; cậu nhận bằng hai tay.', sound: 'rè điện đều',
  light: 'trắng phẳng; đèn lồng ấm trong tay', action: 'Ida chìa đèn lồng; Cas đón bằng hai tay.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 22 }); const lan = lanternLight(st.scene, false, 1.2);
    const cam = camMM(28); cam.position.set(12.8, 1.5, 0.6); cam.lookAt(8.2, 1.2, -4.6);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        ida.place(poseAt([[0, over(p.stand, { props: ['lantern_hand_R'] })], [0.6, p.holdOut]], t), 8.9, -4.6, yawTo(8.9, -4.6, 7.9, -4.4));
        cas.place(poseAt([[0, p.C.turnaround], [0.8, p.casTake]], t), 7.9, -4.4, yawTo(7.9, -4.4, 8.9, -4.6)); lan(ida, f); } };
  } });

S({ id: 's42', scene: 5, t0: 127.0, t1: 130.0, size: 'MS', angle: 'thấp (ngang đèn lồng), 3/4 trước-phải Cas', mm: 45, move: 'tĩnh',
  why: 'Trả mô-típ: không ai bảo, Cas hơ hai lòng tay trên kính đếm ba — đúng như bà. Ida (nền) thấy, không nói.', sound: 'lửa đèn lồng thở; nhạc tạm vào lại',
  light: 'đèn lồng ấm trên nền đá (dưới mặt Cas); trắng phẳng', action: 'Cas đặt đèn xuống, ngồi xổm, áp tay: một, hai, ba (127,5 / 128,1 / 128,7).',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34, expr: 'neutral' });
    // đèn lồng của Ida (vừa trao) đặt trên đá lát trước tay Cas — cùng đạo cụ cast.buildLantern, cỡ theo sheet Ida
    const lanObj = buildLantern(ctx.sheets.ida.props.lantern.height_H * ctx.sheets.ida.H_m, (r, c) => r === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff0c8').multiplyScalar(20) }) : r === 'glass' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc56b').multiplyScalar(3), transparent: true, opacity: 0.7, depthWrite: false }) : lamMat({ color: c }));
    lanObj.position.set(7.36, 0.0, -3.0); lanObj.rotation.y = 0.4; st.scene.add(lanObj); lanObj.updateMatrixWorld(true); lanObj.traverse((o) => { if (o.isMesh) o.castShadow = false; });
    const lanL = new THREE.PointLight('#ffa050', 0, 0, 2); lanObj.userData.lightAnchor.getWorldPosition(lanL.position); st.scene.add(lanL);
    const cam = camMM(45); cam.position.set(9.3, 0.85, -0.55); cam.lookAt(7.7, 0.55, -3.0);
    const wc = p.C.warm_hands_copy, wcIn = over(wc, { joints: { shoulder_L: [-66, 0, 10], shoulder_R: [-66, 0, -10], elbow_L: [-28, 0, 0], elbow_R: [-28, 0, 0] } });
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.2,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        let k = 0; for (const b of [0.5, 1.1, 1.7]) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        cas.place({ ...lerpPose(wc, wcIn, k), props: [], root_y_m: (wc.root_y_H ?? 0) * ctx.sheets.cas.H_m }, 6.9, -3.0, Math.PI / 2); lanL.intensity = 1.4 * flickAt(f + 17);
        ida.place(over(p.stand, { props: [], joints: { neck: [26, 0, 0] } }), 8.6, -3.3, yawTo(8.6, -3.3, 7.2, -3.0)); } };
  } });

// ---------------- CẢNH 6 — Ô cửa (2:10–2:30, 20 s) ----------------
S({ id: 's43', scene: 6, t0: 130.0, t1: 134.0, size: 'EWS', angle: 'cao (cùng khung mở đầu)', mm: 28, move: 'dolly vào rất chậm',
  why: 'Lặp khung mở đầu để đo cái đã mất: thành phố trắng đều, không ngủ; giữa khung một ô cửa hổ phách.', sound: 'rè điện toàn thành phố; nhạc tạm',
  light: 'đèn điện khắp nơi; một ô cửa đèn lồng', action: 'Toàn cảnh tĩnh; một ô vàng.',
  async build(ctx) { const c = await buildCitySet(ctx, 'night'); return { ...c, exposure: 1.0, grade: GRADE_COLD }; } });

const alleyShot = (id, t0, t1, meta, fn) => S({ id, scene: 6, t0, t1, ...meta,
  async build(ctx) {
    const r = await buildAlleySet(ctx, {}); const p = P(ctx); r.chIda.sheetRef = r.chIda.sheet; const cam = r.cam; const ctl = fn(p, cam, r);
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda }, paintP: S6_PAINT, grade: GRADE_ALLEY, exposure: meta.exposure ?? 4.0,
      update(t, T, f) { ctl.update(t, T, r.chIda); if (ctx.upd) ctx.upd(r.chIda, cam); } };
  } });
alleyShot('s44', 134.0, 137.0, { size: 'WS', angle: 'thấp, hất lên ô cửa', mm: 21, move: 'đẩy vào chậm',
  why: 'Trong ngõ khuất điện, dưới ánh cửa sổ nhà Cas, bóng bà — ngắn, nhạt — nằm lại trên đá lát (khung style frame d_s6_alley).', sound: 'rè điện xa, nghẹt; im',
  light: 'đèn lồng trên bậu cửa sổ (qua ô kính); điện chỉ lọt miệng ngõ', action: 'Ida đứng dưới cửa sổ, ngửa nhìn ô vàng.' },
  (p, cam) => { const c0 = cam.position.clone(); return { update(t, T, ida) { ida.setPose(p.lookShadows); ida.root.updateMatrixWorld(true); cam.position.copy(c0).add(new THREE.Vector3(0, 0, 0.5 * ease(t / 3))); } }; });
alleyShot('s45', 137.0, 139.0, { size: 'MS', angle: 'ngang', mm: 50, move: 'tĩnh', exposure: 6.5,
  why: 'Bà lấy đồng hồ ra, nhìn từ đồng hồ sang mặt đồng hồ quảng trường trên mái (qua miệng ngõ).', sound: 'tích tắc; rè điện xa',
  light: 'ánh cửa sổ ấm từ trên', action: 'Ida lấy đồng hồ, nhìn nó, rồi ngẩng nhìn về phía miệng ngõ.' },
  (p, cam) => { const w = watchInHand; let wf = null; return { update(t, T, ida) {
    if (!wf) wf = w(ida.root.parent);
    ida.setPose(poseAt([[0, over(p.watchHold(0), { props: [] })], [1.0, over(p.watchHold(0), { props: [] })], [1.6, over(p.watchHold(0), { props: [], joints: { neck: [-14, 0, 0] } })]], t)); ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(50); cam.updateProjectionMatrix(); cam.position.set(0.9, 1.45, 3.2); cam.lookAt(0.45, 1.35, 1.0); wf(ida, cam, 318, 236.5); } }; });
alleyShot('s46', 139.0, 142.0, { size: 'CU (insert)', angle: 'chúc nhẹ', mm: 100, move: 'tĩnh', exposure: 6.0,
  why: '9B: kim phút tiến 42° lên trùng 12 — bà nhận giờ mới. Gập đồng hồ, KHÔNG gõ kính.', sound: 'núm vặn lách cách; tách gập',
  light: 'ánh cửa sổ ấm', action: 'Ngón cái vặn núm; kim phút chạy từ 318° lên 360°; bàn tay khép lại.' },
  (p, cam) => { let wf = null; return { update(t, T, ida) {
    if (!wf) wf = watchInHand(ida.root.parent);
    ida.setPose(over(p.watchHold(0), { props: [] })); ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(100); cam.updateProjectionMatrix();
    wf(ida, cam, valAt([[0, 318], [0.3, 318], [2.2, 360]], t), valAt([[0, 236.5], [2.2, 240]], t), new THREE.Vector3(0.2, 0.8, 0.55), 0.32); } }; });
alleyShot('s47', 142.0, 145.0, { size: 'WS', angle: 'ngang, sau lưng Ida', mm: 28, move: 'tĩnh',
  why: 'Bà vác thang đi ra miệng ngõ; bóng mờ của bà mỏng dần rồi tan trong trắng (luật 3.5).', sound: 'bước chân; thang; rè điện lớn dần ở miệng ngõ',
  light: 'ánh cửa sổ (sau lưng) → điện phẳng ở miệng ngõ', action: 'Ida vác thang đi từ dưới cửa sổ ra miệng ngõ.' },
  (p, cam) => ({ update(t, T, ida) { const wp = walkPose(t, p.I.walk_ladder); ida.setPose(wp); ida.root.position.set(0.3, wp.root_y_m, 1.0 + WALK.speed_mps * 1.05 * t); ida.root.rotation.y = 0; ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(28); cam.updateProjectionMatrix(); cam.position.set(0.1, 1.45, -2.6); cam.lookAt(0.0, 1.3, 6.0); } }));

S({ id: 's48', scene: 6, t0: 145.0, t1: 150.0, size: 'WS', angle: 'ngang, sau lưng Cas', mm: 28, move: 'tĩnh; mờ dần về đen (148,5–150)',
  why: 'Kết 2B: đèn lồng trên bậu, Cas quay lưng, chim to và mềm mở cánh bay ngang tường. Ida đã đi trước.', sound: 'nhạc tạm (kết); lửa thở',
  light: 'đèn lồng trên bậu (nguồn duy nhất, hổ phách trọn khung)', action: 'Cas làm chim; chim bay ngang tường; FADE OUT.',
  async build(ctx) {
    const R = buildRoomSet(ctx); const p = P(ctx); const cas = makeChar(ctx, R.scene, 'cas', { detail: 26, blob: false });
    const cam = camMM(28); cam.position.set(-1.4, 1.3, -1.5); cam.lookAt(0.4, 1.5, 1.6);
    return { scene: R.scene, cam, named: { cas }, paintP: PAINT_WALL, exposure: (t) => 2.4 * (1 - ease((t - 3.5) / 1.5)),
      update(t, T, f) { R.L.intensity = 3.5 * flickAt(f); const sw = Math.sin(t * 0.8) * 14;
        const b = p.bird(t, 1.0); cas.place(over(b, { joints: { spine: [-4, sw, 0], shoulder_L: [-98, b.joints.shoulder_L[1], b.joints.shoulder_L[2]], shoulder_R: [-98, b.joints.shoulder_R[1], b.joints.shoulder_R[2]] } }), 0.6 + 0.15 * Math.sin(t * 0.6), -0.5, -0.15); } };
  } });

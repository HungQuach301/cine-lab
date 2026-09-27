// Cine Lab · Cổng 5 LAYOUT — GÓI W2: cảnh 4–6 (s25 → hết phim). Chỉ W2 sửa file này.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { walkPose, WALK, WALK_CHILD } from '/cong3/shared/anim.js';
import { buildStreetSet, LAMP_X, LAMP_Z, WALK_Z, POST_X, CLOCK, ladderOf, buildWatch, lamMat, flickAt, GRADE_COLD } from './sets.js';
import { buildCitySet, buildWallSet, buildBaySet, buildAlleySet, buildRoomSet } from './sets2.js';
import { buildLantern } from '/cong3/shared/cast.js';
import { U } from '/cong3/v2/s5.js';
import { ease, easeIO, clamp01, fovOf, lerpPose, over, poseAt, valAt, camAt, makeChar, yawTo } from './util.js';
import { CLOCKS, CLOCK_ON, DIALOGUE, DING, FILM_S, FOOT_Z, GAS_ON, GRADE_ALLEY, GRADE_S5, L11_OFF, ON_Z, ORDER, P, PAINT_CLOSE, PAINT_STREET, PAINT_WALL, POST_ON, REACH_IDA, RELAY_1, S, S5_PAINT, S5_PAINT_MED, S6_PAINT, SHOTS, SQUARE_ON, SRC, T0, T1, VALVE, WALL_POST_ON, camMM, expo, faceCam, flameL11, gasLevel, hands, ladderAt, lanternLight, stdState, switchOn, watchInHand, whiteAt } from './common.js';

// ---------------- CẢNH 4 — Bức tường ----------------
const wallShot = (id, t0, t1, meta, fn) => S({ id, scene: 4, t0, t1, ...meta,
  async build(ctx) {
    const W = buildWallSet(ctx); const p = P(ctx);
    const cas = makeChar(ctx, W.scene, 'cas', { detail: meta.casDetail ?? 30, expr: meta.casExpr }); const ida = makeChar(ctx, W.scene, 'ida', { detail: meta.idaDetail ?? 24, expr: meta.idaExpr, hatBack: 0, glint: meta.idaGlint });
    const cam = camMM(meta.mm);
    const lan = lanternLight(W.scene, false, 0);
    const ctl = fn(p, cam);
    return { scene: W.scene, cam, named: { ida, cas }, paintP: PAINT_WALL, exposure: ctl.exposure ?? 2.6,
      update(t, T, f) {
        const e = switchOn(T, WALL_POST_ON);
        const r = ctl.update(t, T, { ida, cas, cam, e });
        const lp = new THREE.Vector3(); let lk = 0;
        if (ida.props.lantern && ida.props.lantern.parent) { ida.props.lantern.updateMatrixWorld(true); ida.props.lantern.userData.lightAnchor.getWorldPosition(lp); lk = r?.lantern ?? 0.012; }   // v2: đèn lồng đóng cửa ở thắt lưng — hắt ngược rất yếu (0,06 ở v1 rọi từ dưới lên, cổ áo che cằm → vùng mắt sáng như "mắt phát sáng", AI mù 1:14)
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
    ida.place(over(p.stand, { joints: { neck: [4, 0, 0] } }), -0.6, 5.2, yawTo(-0.6, 5.2, 0.15, 0.95)); cam.position.set(1.0, 1.5, 2.9); cam.lookAt(-0.6, 1.45, 5.2); } }));
wallShot('s27', 76.0, 80.0, { size: 'WS', angle: 'thấp, sau-phải, hất lên', mm: 21, move: 'tĩnh',
  why: 'Cột điện PHỐ CHÍNH cạnh góc nhà kho bật: bóng đèn thấy trong khung, nhấp hai lần rồi đứng trắng trên nền trời đêm có sao. Trắng phủ tường; chim nhạt dần trong 12 khung (luật 3.3) — tay vẫn còn, chỉ mất bóng. Góc ngọn 11 lùi sau góc nhà, vẫn tối (chỉ đạo chủ dự án).',
  sound: 'rơ-le "tách"; bóng đèn rít; rè điện', light: 'cột điện cạnh tường bật — trắng phẳng; đèn khí L11 còn nhưng chìm',
  action: 'Bóng đèn điện bật; chim bóng xám dần rồi mất; tay Cas vẫn vỗ.' },
  (p, cam) => ({ exposure: (t, T) => 2.6 - 1.3 * switchOn(T, WALL_POST_ON), update(t, T, { ida, cas }) { cas.place(p.bird(t + 8, 1.0), 0.15, 0.95, Math.PI + 0.15);
    ida.place(p.stand, -0.6, 5.2, yawTo(-0.6, 5.2, 0.15, 0.95)); cam.position.set(4.5, 0.9, 7.0); cam.lookAt(0.8, 3.3, 0.5); } }));
wallShot('s28', 80.0, 83.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'tĩnh',
  why: 'Cas vỗ mạnh hơn vào bức tường trống — không gì cả.', sound: 'rè điện; vải', light: 'trắng phẳng',
  action: 'Cas vỗ tay nhanh, mạnh; tường trắng trơn.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) { cas.place(p.bird(t, 2.1, 1.8), 0.15, 0.95, Math.PI + 0.15); ida.place(p.stand, -3.4, 5.4, 2.5); cam.position.set(...BIRD_CAM[0]); cam.lookAt(...BIRD_CAM[1]); } }));
wallShot('s29', 83.0, 86.0, { size: 'MCU', angle: 'ngang mắt Cas, 3/4 trước-phải', mm: 85, move: 'tĩnh', casDetail: 36,
  why: 'Cas hạ tay, quay lại, thấy bà — rồi thấy đèn lồng hổ phách ở thắt lưng bà. Cậu không xin.', sound: 'rè điện; im',
  light: 'trắng phẳng; phản ánh ấm rất nhẹ của đèn lồng', action: 'Cas hạ tay, xoay người về phía Ida (trái khung), nhìn xuống đèn lồng.' },
  (p, cam) => ({ exposure: 1.3, update(t, T, { ida, cas }) {
    const yaw = valAt([[0, Math.PI + 0.15], [0.9, Math.PI + 0.15], [1.9, yawTo(0.15, 0.95, -0.6, 5.2)]], t);
    cas.place(poseAt([[0, p.bird(0, 1)], [0.8, p.C.turnaround], [2.0, over(p.C.turnaround, { joints: { neck: [22, 0, 0] } })]], t), 0.15, 0.95, yaw);
    ida.place(p.stand, -0.6, 5.2, yawTo(-0.6, 5.2, 0.15, 0.95));
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

// ---------------- CẢNH 5 — Ngọn cuối ----------------
// Bóng trong hốc (quang học thật, không bóng giả): đèn lồng trên nền đá cách vách 3,0 m. Bóng phóng đại = 3,0 / (3,0 − khoảng cách người–vách).
// Ida đứng cách vách 1,4 m (gần đèn) → bóng ×1,88 ≈ 2,8 m, CAO; Cas đứng sát vách 0,45 m → bóng ×1,18 ≈ 1,5 m, NHỎ, ngay cạnh cậu.
const BAY_Z = { ida: 1.4, cas: 0.45 };
S({ id: 's33', scene: 5, size: 'WS', angle: 'ngang 1,35 m, "tranh trong tranh"', mm: 32, move: 'dolly vào chậm (0,9 m)',
  why: 'Hình trung tâm (7A, khung style frame c_s5_wide): trong hốc cửa khuất điện, đèn lồng dưới đất; Ida dừng gần đèn nên bóng bà vươn CAO lên vách, Cas đi tới sát vách nên bóng cậu NHỎ, đứng ngay cạnh cậu ("hers, tall…; his, small"). Ngoài vòm phố trắng không bóng.',
  sound: 'nhạc tạm; bước chân vào hốc; rè điện xa', light: 'đèn lồng trên nền đá (nguồn thấp, có bóng); ngoài vòm: điện phẳng',
  action: 'Ida đặt đèn lồng, hai người bước vào; Ida dừng giữa hốc, Cas đi tới sát vách; hai bóng một cao một nhỏ.',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}); const p = P(ctx); const cam = r.cam; const c0 = cam.position.clone(); [r.chIda, r.chCas].forEach((c) => tameGlint(c));
    for (const ch of [r.chIda, r.chCas]) { ch.sheetRef = ch.sheet; }
    const keep = () => { if (!r.lan.parent) r.scene.add(r.lan); };
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT, grade: GRADE_S5, exposure: 1.0,
      update(t) {
        const zI = valAt([[0, 3.5], [1.2, 3.5], [3.0, BAY_Z.ida]], t), zC = valAt([[0, 3.9], [1.3, 3.9], [4.0, BAY_Z.cas]], t);
        const pI = t < 1.2 ? lerpPose(p.crouch, p.stand, ease(t / 1.2)) : t < 3.0 ? over(walkPose(t - 1.2, p.stand), { props: [] }) : poseAt([[3.0, over(p.stand, { props: [] })], [4.2, over(p.lookShadows, { props: [] })]], t);
        const pC = t < 1.3 ? p.C.turnaround : t < 4.0 ? walkPose(t - 1.3, p.C.turnaround, { gait: WALK_CHILD, bothArms: true }) : poseAt([[4.0, p.C.turnaround], [5.2, p.C.half_raised]], t);
        r.chIda.setPose({ ...pI, props: [] }); keep(); r.chIda.root.position.set(-0.42, pI.root_y_m ?? 0, zI); r.chIda.root.rotation.y = Math.PI + 0.30 * clamp01((t - 2.8) / 0.8); r.chIda.root.updateMatrixWorld(true);
        r.chCas.setPose(pC); keep(); r.chCas.root.position.set(0.40, pC.root_y_m ?? 0, zC); r.chCas.root.rotation.y = Math.PI - 0.25 * clamp01((t - 3.8) / 0.8); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) { ctx.upd(r.chIda, cam); ctx.upd(r.chCas, cam); }
        cam.position.copy(c0).add(new THREE.Vector3(0, 0, -0.9 * ease(t / 7))); } };
  } });

S({ id: 's34', scene: 5, size: 'MS (nghiêng)', angle: 'ngang ngực, từ phía phải, cạnh đèn lồng', mm: 35, move: 'tĩnh',
  why: 'Ida ngửa nhìn bóng mình cao vút; bên phải, Cas đứng sát vách cạnh cái bóng nhỏ của chính cậu — người và bóng cùng một khung, đọc được bóng nào của ai (AI mù v1 đọc "ba cái bóng").',
  sound: 'lửa thở; nhạc tạm', light: 'đèn lồng dưới đất sau lưng hai người (key thấp, có bóng); viền má và mép mũ',
  action: 'Ida ngửa nhìn bóng, tay đặt lên ngực; Cas giơ nửa tay nhìn bóng mình.',
  async build(ctx) {
    const r = await buildBaySet(ctx, { medium: { pos: [1.42, 1.1, 3.05], look: [-0.35, 1.45, 0.35], fov: 46 } }); [r.chIda, r.chCas].forEach((c) => tameGlint(c)); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    r.chIda.root.position.z = BAY_Z.ida; r.chCas.root.position.z = BAY_Z.cas; for (const ch of [r.chIda, r.chCas]) ch.root.updateMatrixWorld(true);
    return { scene: r.scene, cam: r.cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: 1.0, update() {} };
  } });

// Bộ phố cuối (góc ngọn 11): cột góc (POST_ON[5], đoạn cáp cuối) tắt tới giữa câu L4 → góc chỉ có hổ phách + bóng dài; sau đó trắng tràn.
const endStreet = (o = {}) => buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: o.shadowLamps || [] });
const cornerFill = (T) => 0.06 + 1.04 * switchOn(T, POST_ON[5]);
S({ id: 's35', scene: 5, size: 'WS', angle: 'ngang, xuôi dốc', mm: 28, move: 'tĩnh',
  why: 'Góc ngọn cuối vẫn TỐI (đoạn cáp cuối chưa bật): ngọn L11 là nguồn duy nhất, bóng dài. Bà trèo lên lần cuối; Cas theo và giữ thang bằng hai tay.', sound: 'bước chân; thang; rè điện xa',
  light: 'đèn khí L11 (ấm, có bóng); phố trắng ở xa sau lưng máy', action: 'Ida bước ra khỏi hốc, tới thang, trèo; Cas chạy theo giữ thang.',
  async build(ctx) {
    const st = endStreet({ shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(28); cam.position.set(16.5, 1.7, 2.6); cam.lookAt(5.5, 2.3, -3.8);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: expo(2.4, 1.15, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f);
        if (t < 1.6) ida.place(over(walkPose(t, p.stand), { props: [] }), valAt([[0, 3.2], [1.6, LAMP_X(11)]], t), valAt([[0, -1.6], [1.6, FOOT_Z]], t), yawTo(3.2, -1.6, LAMP_X(11), FOOT_Z));
        else if (t < 2.8) { const u = (t - 1.6) / 1.2; ida.place(p.climb(u, p.restLadder), LAMP_X(11), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); } else ida.place(p.restLadder, LAMP_X(11), ON_Z, 0);
        if (t < 2.4) cas.place(walkPose(t, p.C.turnaround, { gait: WALK_CHILD, bothArms: true }), valAt([[0, 2.2], [2.4, 8.0]], t), valAt([[0, -1.2], [2.4, -5.25]], t), yawTo(2.2, -1.2, 8.0, -5.25));
        else cas.place(poseAt([[2.4, p.C.turnaround], [3.0, p.C.hold_ladder]], t), 8.0, -5.25, 0); } };
  } });

const faceShot = (id, meta, fn) => S({ id, scene: 5, ...meta,
  async build(ctx) {
    const st = endStreet({ shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: meta.expr, gaze: [0.05, -0.04], glint: 0.45 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(meta.mm); const ctl = fn(p, cam);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: ctl.exposure ?? expo(0.36, 0.9, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); cas.place(p.C.hold_ladder, 8.0, -5.25, 0); ctl.update(t, T, ida); } };
  } });
faceShot('s36', { size: 'MCU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'tĩnh', expr: 'neutral',
  why: 'Quyết định C4 của chủ dự án: bà TỰ đẩy vành mũ ra sau trước câu thoại — mặt thoáng ra cho lời từ biệt. Góc còn tối: mặt ấm một bên.', sound: 'vải dạ; hơi thở',
  light: 'đèn khí L11 ngay trước mặt (ấm) — góc chưa có điện', action: 'Tay trái đưa lên vành mũ (hat_push_a), đẩy vành lên, mũ ngả ra sau (hat_push_b).' },
  (p, cam) => ({ update(t, T, ida) { ida.place(poseAt([[0, p.hatA], [0.35, p.hatA], [1.05, p.hatB], [1.6, p.faceRest()]], t), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: 1.9, y: -0.05, fov: fovOf(85) }); } }));
faceShot('s37', { size: 'CU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'đẩy vào rất chậm', expr: 'sad_smile',
  why: 'Lời từ biệt, vế đầu: cười buồn, còn trong hổ phách của ngọn cuối. Máy đẩy vào không nhận ra được.', sound: 'THOẠI L4 "That\'s the last one, then. Goodnight, old street."',
  light: 'đèn khí L11 (ấm) — góc chưa có điện', action: 'Ida nhìn lên phố (phải khung), tay đặt trên van.' },
  (p, cam) => ({ update(t, T, ida) { ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: valAt([[0, 1.1], [5.8, 0.97]], t), fov: fovOf(85) }); } }));

// Toàn cảnh góc ngọn cuối (s37w, s40w): cột điện góc (đoạn cáp cuối) ở trái khung, ngọn L11 + thang ở phải khung, trời đêm phía trên.
const cornerWide = (id, meta, fn) => S({ id, scene: 5, size: 'WS', angle: 'ngang, từ lòng phố, hơi hất', mm: 28, move: 'tĩnh', ...meta,
  async build(ctx) {
    const st = endStreet({ shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 22 });
    const cam = camMM(28); cam.position.set(17.0, 1.6, 1.2); cam.lookAt(8.8, 3.6, 0.6);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: expo(2.4, 1.15, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); cas.place(over(p.C.hold_ladder, { joints: { neck: [-30, 0, 0] } }), 8.0, -5.25, 0); fn(p, t, T, ida); } };
  } });
cornerWide('s37w', { why: 'CHỈ ĐẠO CHỦ DỰ ÁN (1:50 v1): ngay quanh "You\'ll be brighter now", bóng đèn cột góc (đoạn cáp cuối) nhấp hai lần rồi đứng trắng; trắng tràn vào góc, bóng dài và bóng tối biến mất. Câu thoại khớp với hình.',
  sound: 'THOẠI L4 (ngoài hình) "…You\'ll be brighter now."; tách rơ-le gần; bóng đèn rít; rè điện', light: 'cột điện góc bật (nhấp 2 lần, đứng) — trắng phẳng tràn góc; L11 nhạt dần',
  action: 'Ida trên thang, Cas giữ thang; bóng đèn điện bật, bóng dài của hai người trên đá lát tan.' },
  (p, t, T, ida) => ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0));
S({ id: 's38', scene: 5, size: 'MS', angle: 'cao, chúc xuống (gần mắt Ida)', mm: 50, move: 'tĩnh',
  why: 'Phản ứng của Cas: cậu giữ thang, ngước nhìn bà trong ánh trắng mới — người nghe câu nói thay khán giả.', sound: 'L4 tiếp (ngoài hình)',
  light: 'trắng phẳng (cột góc vừa bật); ấm rất yếu từ L11 trên cao', action: 'Cas giữ thang, ngửa mặt nhìn lên.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 20 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34 });
    const cam = camMM(50); cam.position.set(9.1, 2.35, -3.7); cam.lookAt(8.0, 1.0, -5.25);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); cas.place(over(p.C.hold_ladder, { joints: { neck: [-36, 0, 0] } }), 8.0, -5.25, 0.25); } };
  } });
faceShot('s39', { size: 'CU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'tĩnh', expr: 'choked',
  why: 'Vế cuối, giọng vỡ, nay trong ánh trắng phẳng: "keep a little dark for the ones who need it" — chủ đề phim trong một câu.', sound: 'THOẠI L4 "Just... keep a little dark for the ones who need it."',
  light: 'trắng phẳng (cột góc); L11 nhạt', action: 'Ida nghẹn, một giọt nước mắt; mắt vẫn nhìn lên phố.' },
  (p, cam) => ({ update(t, T, ida) { ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: 0.95, fov: fovOf(85) }); } }));

S({ id: 's40', scene: 5, size: 'CU (insert)', angle: 'ngang lồng đèn, từ lòng phố', mm: 50, move: 'tĩnh',
  why: 'NGỌN CUỐI (AI mù v1: "thắp hay tắt?"): tay bà gạt van; lửa co lại, ngả xanh, tắt; máy giữ im 0,8 s trên lồng kính tối. Rõ là TẮT.', sound: 'van kim loại; lửa xì nhỏ dần; "phụt" tắt; im',
  light: 'ngọn L11 co lại → xanh → tắt; trắng phẳng không đổi', action: 'Tay phải Ida gạt van; ngọn lửa co lại, chuyển xanh, tắt; lồng kính tối.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 32 }); const cam = camMM(50);
    const l11 = st.lamps[10]; const lever = l11.lamp.userData.parts.lever; const fp = l11.fp; const flame = l11.lamp.userData.flame; const fs0 = flame.scale.clone();
    const lv = new THREE.Vector3(); lever.updateMatrixWorld(true); lever.getWorldPosition(lv);
    const mid = fp.clone().lerp(lv, 0.45); cam.position.copy(mid).add(new THREE.Vector3(0.5, 0.1, 1.3)); cam.lookAt(mid);
    const blue = new THREE.Color('#6f8cff');
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        const u = clamp01((T - VALVE) / 0.6); ida.place(over(p.valveLadder, { joints: { wrist_R: [0, 0, -20 + 40 * ease(u)] } }), LAMP_X(11), ON_Z, 0);
        // đặt lòng bàn tay phải lên cần van (dịch gốc nhân vật, ≤ vài chục cm — insert không thấy chân thang)
        const palm = new THREE.Vector3(0, -ida.sheetRef.parts.hand.palm_length * ida.H * 0.5, 0); ida.joints.wrist_R.localToWorld(palm);
        lever.rotation.z = -0.5 + 1.2 * ease(u); lever.updateMatrixWorld(true); const tip = new THREE.Vector3(0.05, 0, 0); lever.localToWorld(tip);
        ida.root.position.add(tip.sub(palm)); ida.root.updateMatrixWorld(true);
        const [k, b] = flameL11(T); flame.scale.copy(fs0).multiplyScalar(Math.max(k, 0.001)); flame.visible = k > 0.01;
        l11.flameM.color.set('#fff2d0').multiplyScalar(30 * Math.max(k, 0.2)).lerp(blue.clone().multiplyScalar(8), b); } };
  } });
cornerWide('s40w', { why: '"Nothing else changes": ngọn cuối đã tắt, phố trắng y nguyên — không một đèn nào nhấp. Máy tĩnh, giữ 2 s.',
  sound: 'rè điện đều; im', light: 'trắng phẳng; lồng kính L11 tối', action: 'Ida trên thang, tay rời van; Cas giữ thang; không gì đổi.' },
  (p, t, T, ida) => ida.place(p.restLadder, LAMP_X(11), ON_Z, 0));

S({ id: 's41', scene: 5, size: 'WS', angle: 'ngang', mm: 28, move: 'tĩnh',
  why: 'Dưới chân thang bà trao đèn lồng; cậu nhận bằng hai tay.', sound: 'rè điện đều; quai đèn',
  light: 'trắng phẳng; đèn lồng ấm trong tay', action: 'Ida chìa đèn lồng; Cas đón bằng hai tay.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 22 }); const lan = lanternLight(st.scene, false, 1.2);
    const cam = camMM(28); cam.position.set(12.8, 1.5, 0.6); cam.lookAt(8.2, 1.2, -4.6);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        ida.place(poseAt([[0, over(p.stand, { props: ['lantern_hand_R'] })], [0.5, p.holdOut]], t), 8.9, -4.6, yawTo(8.9, -4.6, 7.9, -4.4));
        cas.place(poseAt([[0, p.C.turnaround], [0.7, p.casTake]], t), 7.9, -4.4, yawTo(7.9, -4.4, 8.9, -4.6)); lan(ida, f); } };
  } });

// Bộ s5/s6 dựng nhân vật với glint mặc định (5,0 — hợp phơi sáng 0,12 của Cổng 3); ở phơi sáng animatic ~1,0 mắt thành phát sáng → hạ về mức makeChar.
const tameGlint = (ch, k = 0.12) => ch.root.traverse((o) => { if (o.isMesh && o.material && o.material.emissiveMap) o.material.emissiveIntensity = k * (o.userData.part === 'eyes' ? 3 : 1); });
// Đèn lồng Cas cầm (cùng đạo cụ cast.buildLantern, cỡ theo sheet Ida): treo giữa hai cổ tay.
const lanternProp = (ctx) => buildLantern(ctx.sheets.ida.props.lantern.height_H * ctx.sheets.ida.H_m, (r, c) => r === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff0c8').multiplyScalar(20) }) : r === 'glass' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffc56b').multiplyScalar(3), transparent: true, opacity: 0.7, depthWrite: false }) : lamMat({ color: c }));
function hangFromHands(lan, ch, h) { const a = new THREE.Vector3(), b = new THREE.Vector3(); ch.joints.wrist_L.getWorldPosition(a); ch.joints.wrist_R.getWorldPosition(b);
  lan.position.copy(a.add(b).multiplyScalar(0.5)).add(new THREE.Vector3(0, -h - 0.03, 0)); lan.updateMatrixWorld(true); }
// Chỉ đạo chủ dự án (2:07 v1): "Cas nên chọn 1 góc tối để huơ tay" → nhìn quanh phố trắng (s42a), đi vào vòm hốc cửa tối (s42b), hơ tay trong bóng tối (s42).
S({ id: 's42a', scene: 5, size: 'MS', angle: 'ngang ngực Cas, 3/4 trước', mm: 45, move: 'tĩnh',
  why: 'CHỈ ĐẠO CHỦ DỰ ÁN (2:07 v1): Cas ôm đèn lồng, nhìn quanh phố giờ trắng khắp nơi — không còn chỗ nào cho ngọn lửa nhỏ. Cậu tìm một góc tối.', sound: 'rè điện; lửa đèn lồng thở; nhạc tạm vào lại',
  light: 'trắng phẳng khắp khung; đèn lồng ấm dưới cằm Cas', action: 'Cas cầm đèn lồng bằng hai tay, quay đầu nhìn trái, nhìn phải, rồi nhìn về phía hốc cửa (trái khung).',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 20 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34, expr: 'neutral' });
    const lanObj = lanternProp(ctx); st.scene.add(lanObj); lanObj.traverse((o) => { if (o.isMesh) o.castShadow = false; }); const h = ctx.sheets.ida.props.lantern.height_H * ctx.sheets.ida.H_m;
    const lanL = new THREE.PointLight('#ffa050', 0, 0, 2); st.scene.add(lanL);
    const cam = camMM(45); cam.position.set(10.4, 1.0, -0.6); cam.lookAt(7.6, 0.9, -3.3);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f);
        ida.place(over(p.stand, { props: [], joints: { neck: [18, 0, 0] } }), 8.9, -4.6, yawTo(8.9, -4.6, 7.6, -3.3));
        const nk = valAt([[0, 0], [0.3, 0], [0.8, 38], [1.2, 38], [1.6, -30], [2.0, -45]], t);
        cas.place(over(p.casTake, { joints: { neck: [4, nk, 0] } }), 7.6, -3.3, yawTo(7.6, -3.3, 10.4, -0.6));
        hangFromHands(lanObj, cas, h); lanObj.userData.lightAnchor.getWorldPosition(lanL.position); lanL.intensity = 1.2 * flickAt(f + 17); } };
  } });

S({ id: 's42b', scene: 5, size: 'WS', angle: 'ngang 1,3 m, ngoài vòm', mm: 32, move: 'tĩnh',
  why: 'Cas mang đèn lồng rời phố trắng, bước qua vòm vào hốc cửa khuất điện (nơi hai cái bóng đứng lúc trước): ánh hổ phách đi theo cậu vào trong bóng tối.', sound: 'bước chân trẻ con; rè điện xa dần',
  light: 'ngoài vòm: điện phẳng; trong hốc: chỉ đèn lồng Cas mang theo', action: 'Cas đi từ phố vào vòm, dừng giữa hốc.',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}); const p = P(ctx); r.chCas.sheetRef = r.chCas.sheet; [r.chIda, r.chCas].forEach((c) => tameGlint(c)); r.chIda.root.visible = false;
    const cam = r.cam; cam.shiftY = 0.05; cam.position.set(0.9, 1.25, 8.2); cam.lookAt(0.3, 1.1, 2.0); cam.updateProjectionMatrix();
    const h = r.lanternH; const f0 = r.flameP.clone();
    const glows = []; r.scene.traverse((o) => { if (o.isSprite && o.position.distanceTo(f0) < 0.4) glows.push([o, o.position.clone().sub(f0)]); });
    const cur = f0.clone();
    const moveLamp = () => { r.lan.userData.lightAnchor.getWorldPosition(cur); r.spot.position.copy(cur); U.uLP.value.copy(cur); r.spot.updateMatrixWorld(); for (const [o, d] of glows) o.position.copy(cur).add(d); };
    const carry = over(p.casTake, {});
    return { scene: r.scene, cam, onSample: (i, n, j) => { r.onSample(i, n, j); moveLamp(); }, named: { cas: r.chCas }, paintP: S5_PAINT, grade: GRADE_S5, exposure: 1.0,
      update(t) {
        const x = valAt([[0, 1.9], [1.7, 0.35]], t), z = valAt([[0, 5.3], [1.7, 3.35]], t);
        const w = walkPose(t, p.C.turnaround, { gait: WALK_CHILD });
        const pose = t < 1.7 ? over(w, { joints: { shoulder_L: carry.joints.shoulder_L, elbow_L: carry.joints.elbow_L, shoulder_R: carry.joints.shoulder_R, elbow_R: carry.joints.elbow_R }, hands: carry.hands }) : carry;
        r.chCas.setPose(pose); r.chCas.root.position.set(x, pose.root_y_m ?? 0, z); r.chCas.root.rotation.y = t < 1.5 ? yawTo(1.9, 5.3, 0.35, 3.35) : valAt([[1.5, yawTo(1.9, 5.3, 0.35, 3.35)], [2.0, -Math.PI]], t); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) ctx.upd(r.chCas, cam);
        if (r.lan.parent !== r.scene) r.scene.add(r.lan); hangFromHands(r.lan, r.chCas, h); moveLamp(); } };
  } });

S({ id: 's42', scene: 5, size: 'MS', angle: 'thấp, từ trong hốc nhìn ra vòm', mm: 32, move: 'tĩnh',
  why: 'Trả mô-típ: trong góc tối cậu tự chọn, không ai bảo, Cas đặt đèn xuống, hơ hai lòng tay trên kính đếm ba — đúng như bà. Qua vòm: phố trắng; Ida đứng ở miệng vòm nhìn vào, không nói.', sound: 'lửa đèn lồng thở; nhạc tạm',
  light: 'đèn lồng trên nền đá (nguồn duy nhất trong hốc); ngoài vòm: điện phẳng', action: 'Cas ngồi xổm, áp tay: một, hai, ba. Ida ở miệng vòm.',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}); const p = P(ctx); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    const cam = r.cam; cam.shiftY = 0; [r.chIda, r.chCas].forEach((c) => tameGlint(c)); cam.fov = fovOf(32); cam.position.set(-0.75, 0.72, 1.05); cam.lookAt(0.3, 0.75, 4.6); cam.updateProjectionMatrix();
    const wc = p.C.warm_hands_copy, wcIn = over(wc, { joints: { shoulder_L: [-66, 0, 10], shoulder_R: [-66, 0, -10], elbow_L: [-28, 0, 0], elbow_R: [-28, 0, 0] } });
    const hC = (wc.root_y_H ?? 0) * ctx.sheets.cas.H_m;
    r.chIda.setPose(over(p.stand, { props: [], joints: { neck: [12, 0, 0] } })); r.chIda.root.position.set(-1.05, 0, 5.3); r.chIda.root.rotation.y = Math.PI + 0.25; r.chIda.root.updateMatrixWorld(true);
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: 0.55,
      update(t) {
        let k = 0; for (const b of [0.6, 1.2, 1.8]) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        r.chCas.setPose({ ...lerpPose(wc, wcIn, k), props: [] }); r.chCas.root.position.set(0.1, hC, 3.55); r.chCas.root.rotation.y = Math.PI; r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) { ctx.upd(r.chIda, cam); ctx.upd(r.chCas, cam); } } };
  } });

// ---------------- CẢNH 6 — Ô cửa ----------------
S({ id: 's43', scene: 6, t0: 130.0, t1: 134.0, size: 'EWS', angle: 'cao (cùng khung mở đầu)', mm: 28, move: 'dolly vào rất chậm',
  why: 'Lặp khung mở đầu để đo cái đã mất: thành phố trắng đều, không ngủ; giữa khung một ô cửa hổ phách.', sound: 'rè điện toàn thành phố; nhạc tạm',
  light: 'đèn điện khắp nơi; một ô cửa đèn lồng', action: 'Toàn cảnh tĩnh; một ô vàng.',
  async build(ctx) { const c = await buildCitySet(ctx, 'night'); return { ...c, exposure: 1.0, grade: GRADE_COLD }; } });

const alleyShot = (id, t0, t1, meta, fn) => S({ id, scene: 6, t0, t1, ...meta,
  async build(ctx) {
    const r = await buildAlleySet(ctx, {}); const p = P(ctx); r.chIda.sheetRef = r.chIda.sheet; tameGlint(r.chIda); const cam = r.cam; const ctl = fn(p, cam, r);
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda }, paintP: S6_PAINT, grade: GRADE_ALLEY, exposure: meta.exposure ?? 4.0,
      update(t, T, f) { ctl.update(t, T, r.chIda); if (ctx.upd) ctx.upd(r.chIda, cam); } };
  } });
alleyShot('s44', 134.0, 137.0, { size: 'WS', angle: 'thấp, hất lên ô cửa', mm: 21, move: 'đẩy vào chậm',
  why: 'Trong ngõ khuất điện, dưới ánh cửa sổ nhà Cas, bóng bà — ngắn, nhạt — nằm lại trên đá lát (khung style frame d_s6_alley).', sound: 'rè điện xa, nghẹt; im',
  light: 'đèn lồng trên bậu cửa sổ (qua ô kính); điện chỉ lọt miệng ngõ', action: 'Ida đứng dưới cửa sổ, ngửa nhìn ô vàng.' },
  (p, cam) => { const c0 = cam.position.clone(); return { update(t, T, ida) { ida.setPose(p.lookShadows); ida.root.updateMatrixWorld(true); cam.position.copy(c0).add(new THREE.Vector3(0, 0, 0.5 * ease(t / 3))); } }; });
alleyShot('s45', 137.0, 139.0, { size: 'MS', angle: 'ngang', mm: 50, move: 'tĩnh', exposure: 6.5,
  why: 'ĐỒNG HỒ NHỊP 3a — hai giờ sau (10:00): bà lấy đồng hồ ra (9:53, vẫn chậm 7 phút), rồi ngẩng nhìn về phía mặt đồng hồ quảng trường trên mái.', sound: 'tích tắc; rè điện xa',
  light: 'ánh cửa sổ ấm từ trên', action: 'Ida lấy đồng hồ, nhìn nó, rồi ngẩng nhìn về phía miệng ngõ.' },
  (p, cam) => { const w = watchInHand; let wf = null; return { update(t, T, ida) {
    if (!wf) wf = w(ida.root.parent);
    ida.setPose(poseAt([[0, over(p.watchHold(0), { props: [] })], [1.0, over(p.watchHold(0), { props: [] })], [1.6, over(p.watchHold(0), { props: [], joints: { neck: [-14, 0, 0] } })]], t)); ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(50); cam.updateProjectionMatrix(); cam.position.set(0.9, 1.45, 3.2); cam.lookAt(0.45, 1.35, 1.0); wf(ida, cam, ...hands(CLOCKS.beat3.watchFrom)); } }; });
S({ id: 's45c', scene: 6, size: 'CU', angle: 'tele, POV của Ida qua miệng ngõ', mm: 200, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 3b — mặt đồng hồ điện trên nền trời đêm chỉ đúng 10:00 (cùng vị trí, cùng cỡ với nhịp 2a): giờ của thành phố.', sound: 'rè điện xa; tích tắc',
  light: 'mặt đồng hồ phát trắng; trời đêm', action: 'Mặt đồng hồ quảng trường: 10:00.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 140, x1: 200, shadowLamps: [] }); const cam = camMM(200); cam.position.set(150, 6.2, 0.4); cam.lookAt(CLOCK.x, CLOCK.h, CLOCK.z);
    const [mD, hD] = hands(CLOCKS.beat3.square);
    return { scene: st.scene, cam, named: {}, paintP: PAINT_CLOSE, exposure: 1.2, grade: GRADE_COLD,
      update(t, T, f) { st.setState(stdState(T), f); st.clock.userData.setHands(mD + 6 * t / 60, hD); } };
  } });
alleyShot('s46', 139.0, 142.0, { size: 'CU (insert)', angle: 'chúc nhẹ', mm: 100, move: 'tĩnh', exposure: 6.0,
  why: 'ĐỒNG HỒ NHỊP 3c (9B): bà vặn kim từ 9:53 lên đúng 10:00 — nhận giờ mới. Gập đồng hồ, KHÔNG gõ kính (ngược với nhịp 1).', sound: 'núm vặn lách cách; tách gập',
  light: 'ánh cửa sổ ấm', action: 'Ngón cái vặn núm; kim phút chạy từ 9:53 lên 10:00; bàn tay khép lại.' },
  (p, cam) => { let wf = null; return { update(t, T, ida) {
    if (!wf) wf = watchInHand(ida.root.parent);
    ida.setPose(over(p.watchHold(0), { props: [] })); ida.root.updateMatrixWorld(true);
    cam.fov = fovOf(100); cam.updateProjectionMatrix();
    const [m0, h0] = hands(CLOCKS.beat3.watchFrom); wf(ida, cam, valAt([[0, m0], [0.3, m0], [2.2, 360]], t), valAt([[0, h0], [2.2, 300]], t), new THREE.Vector3(0.2, 0.8, 0.55), 0.32); } }; });
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

// ---------- MỐC SỰ KIỆN (xuất cho âm tạm, phụ đề, SHOTLIST) — cùng nguồn với hình ----------

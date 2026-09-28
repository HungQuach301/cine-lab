// Cine Lab · Cổng 5 LAYOUT — GÓI W2: cảnh 4–6 (s25 → hết phim). Chỉ W2 sửa file này.
// Layout chốt (giai đoạn A): camera cuối (tiêu cự, vị trí, hướng, chuyển máy), dàn dựng, bối cảnh đủ, trục 180°. Bảng + lý do: shots/layout/LAYOUT-W2.md.
// Mọi shot đọc ctx.dbg (--dbg JSON của render_film.js) để dò tham số khi probe; không truyền --dbg thì dùng giá trị chốt.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { walkPose, WALK, WALK_CHILD } from '/cong3/shared/anim.js';
import { buildStreetSet, LAMP_X, LAMP_Z, WALK_Z, POST_X, CLOCK, ladderOf, buildWatch, lamMat, flickAt, GRADE_COLD } from './sets.js';
import { buildCitySet, buildWallSet, buildBaySet, buildAlleySet, buildRoomSet } from './sets2.js';
import { buildLantern } from '/cong3/shared/cast.js';
import { U } from '/cong3/v2/s5.js';
import { ease, easeIO, clamp01, fovOf, lerpPose, over, poseAt, valAt, camAt, makeChar, yawTo } from './util.js';
import { CLOCKS, CLOCK_ON, DIALOGUE, DING, FILM_S, FOOT_Z, GAS_ON, GRADE_ALLEY, GRADE_S5, L11_OFF, ON_Z, ORDER, P, PAINT_CLOSE, PAINT_STREET, PAINT_WALL, POST_ON, REACH_IDA, RELAY_1, S, S5_PAINT, S5_PAINT_MED, S6_PAINT, SHOTS, SQUARE_ON, SRC, T0, T1, VALVE, WALL_POST_ON, camMM, expo, faceCam, flameL11, gasLevel, hands, ladderAt, lanternLight, stdState, switchOn, watchInHand, whiteAt } from './common.js';

const V3a = (v) => v.toArray().map((x) => +x.toFixed(3));
const wpos = (o) => o.getWorldPosition(new THREE.Vector3());

// ---------------- CẢNH 4 — Bức tường ----------------
// Bộ tường chim (sets2.buildWallSet, Cổng 5): tường = mặt nhà kho z = 0; góc nhà x = −8,5 (trái); hốc cửa x = 6,2 (phải); L11 (−2,2; 4,2); cột điện phố chính (2,6; 1,9).
// Luật 180° cảnh 4: đường Ida–Cas; máy luôn ở phía +x của đường này (sau-phải hai người) → Ida TRÁI, Cas PHẢI; Ida nhìn sang PHẢI khung về Cas.
const CAS_W = [0.15, 0.95], CAS_YAW = Math.PI + 0.15;
// V4 (s26): Ida đứng xem ở IDA_W — cách ngọn L11 3,5 m (góc ngẩng tới ngọn lửa ≈ 25°, dưới đường che của vành mũ) và L11 gần như CHÍNH TRƯỚC mặt bà
// (lệch ≈ 4° so với hướng bà nhìn Cas) → ngọn L11 là key trước lên mặt; máy 3/4 ở phía +x đường Ida–Cas (đúng trục 180°).
// Bản v2 đặt bà (−0,6; 5,2), L11 ở sau-bên (1,9 m, góc ngẩng ≈ 40°): vành mũ che hết mặt, tròng mắt vẫn bắt ánh → "mắt phát sáng", mặt tối.
const IDA_W = [-3.8, 7.3];
// Đèn lồng trong tay Ida quỳ (s31–s32): THẤP (≈ 0,75 m, dưới tay Cas), SAU tay cậu, TRƯỚC bụng cậu, cách tường 0,62 m (≤ 0,7 m — luật 3.3).
// Thân và đầu Cas ở SAU đèn (z ≥ 0,7) → không đổ bóng lên tường; chỉ hai bàn tay (z ≈ 0,35–0,45) ở giữa đèn và tường → chỉ có chim.
const LAN_T = [-0.22, 0.75, 0.6];
const LAN_K = 3.0;   // mức đèn lồng trong tay (s30 tăng dần tới mức này khi mở cửa đèn; s31, s32 giữ nguyên — cùng một nguồn)
// s32: Cas nhích 0,1 m (z 0,95 → 0,85) và vươn tay ra trước (birdReach) → cổ tay z ≈ 0,4: tay GIỮA đèn (0,62) và tường → chim ×≈2,5–3, cao ≈ 1,9–2,3 m.
const CAS_S32 = [0.15, 0.74];
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
    return { scene: W.scene, cam, named: { ida, cas }, paintP: meta.paintP || PAINT_WALL, exposure: dbg.exp ?? ctl.exposure ?? 2.6,
      update(t, T, f) {
        const e = switchOn(T, WALL_POST_ON);
        const r = ctl.update(t, T, { ida, cas, cam, e });
        const lp = new THREE.Vector3(); let lk = 0;
        if (ida.props.lantern && ida.props.lantern.parent) { ida.props.lantern.updateMatrixWorld(true); ida.props.lantern.userData.lightAnchor.getWorldPosition(lp); lk = r?.lantern ?? 0.012; }   // v2: đèn lồng đóng cửa ở thắt lưng — hắt ngược rất yếu
        W.setState({ gas: 1, elec: e, lantern: lk, lanternPos: lp, fillK: dbg.fillK ?? 1 }, f);
        if (dbg.log && (f % 12 === 0)) console.log(JSON.stringify({ id, t: +t.toFixed(2), lan: V3a(lp), ida: V3a(ida.root.position), idaHead: V3a(wpos(ida.joints.head)), handL: V3a(wpos(cas.joints.wrist_L)), handR: V3a(wpos(cas.joints.wrist_R)), casHead: V3a(wpos(cas.joints.head)) }));
      } };
  } });
const BIRD_CAM = [[2.2, 1.3, 3.6], [0.3, 1.1, 0]];
const idaWatch = (p) => over(p.stand, { joints: { neck: [4, 0, 0] } });
wallShot('s25', 68.0, 73.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'dolly vào rất chậm (0,3 m)',
  why: 'Giới thiệu Cas bằng việc cậu làm: chim bóng từ đèn khí L11 (khung style frame b_cas_bird).', sound: 'lửa thở; vải sột soạt; im',
  light: 'đèn khí L11 (key, có bóng) — cột điện cạnh tường còn tắt', action: 'Cas giơ hai tay làm chim; chim vỗ cánh chậm trên tường vôi.' },
  (p, cam) => ({ update(t, T, { ida, cas }) { cas.place(p.bird(t, 1.0), ...CAS_W, CAS_YAW); ida.place(idaWatch(p), ...IDA_W, yawTo(...IDA_W, ...CAS_W));
    camAt(cam, [[0, BIRD_CAM[0], BIRD_CAM[1]], [5, [2.0, 1.3, 3.3], BIRD_CAM[1]]], t); } }));
wallShot('s26', 73.0, 76.0, { size: 'MS', angle: 'ngang mắt, 3/4 trước-phải Ida (máy phía +x đường Ida–Cas)', mm: 50, move: 'tĩnh', idaExpr: 'neutral', idaDetail: 32, idaGlint: 0.02,
  why: 'Ida xuống thang, đứng xem, không gọi. Đèn lồng ở thắt lưng vẫn cháy (gieo cho 1:26). V4: mặt bà đọc được — ngọn L11 ở trước-phải bà là key thật; sau lưng bà là đầu phố Ostler đã trắng (chiều sâu).', sound: 'lửa thở',
  light: 'đèn khí L11 (key trước mặt bà, ngẩng ≈ 25°); đèn lồng thắt lưng (rất yếu); nền: mặt tiền phố chính đã trắng', action: 'Ida đứng cách cột L11 vài bước, nhìn Cas (phải khung).' },
  (p, cam, ctx, dbg) => { const ip = dbg.ip || IDA_W; return { exposure: 2.8, update(t, T, { ida, cas }) { cas.place(p.bird(t + 5, 1.0), ...CAS_W, CAS_YAW);
    ida.place(idaWatch(p), ...ip, yawTo(...ip, ...CAS_W)); const h = wpos(ida.joints.head);
    cam.position.set(...(dbg.cp || [-2.1, 1.5, 6.55])); cam.lookAt(h.x + 0.05, h.y - 0.04, h.z); return { lantern: dbg.lk ?? 0.012 }; } }; });
wallShot('s27', 76.0, 80.0, { size: 'WS', angle: 'thấp, sau-phải, hất lên', mm: 21, move: 'tĩnh', paintP: PAINT_STREET,
  why: 'Cột điện PHỐ CHÍNH cạnh góc nhà kho bật: bóng đèn thấy trong khung, nhấp hai lần rồi đứng trắng trên nền trời đêm có sao. Trắng phủ tường; chim nhạt dần trong ~11 khung (luật 3.3) — tay vẫn còn, chỉ mất bóng. V3: thấy cả nhà kho (gờ mái, cửa sổ cao, cửa kéo hàng, hốc cửa bên phải), góc nhà + ngõ cong bên trái, mái xa sau nhà kho.',
  sound: 'rơ-le "tách"; bóng đèn rít; rè điện', light: 'cột điện cạnh tường bật — trắng phẳng; đèn khí L11 còn nhưng chìm',
  action: 'Bóng đèn điện bật; chim bóng xám dần rồi mất; tay Cas vẫn vỗ. Ida đứng xem ở trái khung.' },
  (p, cam, ctx, dbg) => ({ exposure: (t, T) => 2.6 - 1.5 * switchOn(T, WALL_POST_ON), update(t, T, { ida, cas }) { cas.place(p.bird(t + 8, 1.0), ...CAS_W, CAS_YAW);
    ida.place(idaWatch(p), ...IDA_W, yawTo(...IDA_W, ...CAS_W)); cam.position.set(...(dbg.cp || [6.4, 0.85, 12.5])); cam.lookAt(...(dbg.cl || [0.6, 3.6, 1.0])); } }));
wallShot('s28', 80.0, 83.0, { size: 'MS', angle: 'ngang ngực, 3/4 sau-phải Cas', mm: 45, move: 'tĩnh',
  why: 'Cas vỗ mạnh hơn vào bức tường trống — không gì cả (luật 3.3: key : tràn ≈ 1 : 1, không còn bóng).', sound: 'rè điện; vải', light: 'trắng phẳng',
  action: 'Cas vỗ tay nhanh, mạnh; tường trắng trơn.' },
  (p, cam) => ({ exposure: 1.0, update(t, T, { ida, cas }) { cas.place(p.bird(t, 2.1, 1.8), ...CAS_W, CAS_YAW); ida.place(idaWatch(p), ...IDA_W, yawTo(...IDA_W, ...CAS_W)); cam.position.set(...BIRD_CAM[0]); cam.lookAt(...BIRD_CAM[1]); } }));
wallShot('s29', 83.0, 86.0, { size: 'MCU', angle: 'ngang mắt Cas, 3/4 trước-phải', mm: 85, move: 'tĩnh', casDetail: 36,
  why: 'Cas hạ tay, quay lại, thấy bà — rồi thấy đèn lồng hổ phách ở thắt lưng bà. Cậu không xin.', sound: 'rè điện; im',
  light: 'trắng phẳng; phản ánh ấm rất nhẹ của đèn lồng', action: 'Cas hạ tay, xoay người về phía Ida (trái khung), nhìn xuống đèn lồng.' },
  (p, cam) => ({ exposure: 1.0, update(t, T, { ida, cas }) {
    const yaw = valAt([[0, CAS_YAW], [0.9, CAS_YAW], [1.9, yawTo(...CAS_W, ...IDA_W)]], t);
    cas.place(poseAt([[0, p.bird(0, 1)], [0.8, p.C.turnaround], [2.0, over(p.C.turnaround, { joints: { neck: [16, 0, 0] } })]], t), ...CAS_W, yaw);
    ida.place(idaWatch(p), ...IDA_W, yawTo(...IDA_W, ...CAS_W));
    cam.position.set(1.7, 1.1, 2.8); cam.lookAt(0.1, 1.05, 1.0); } }));
// s30 → s32: Ida tới đứng bên trái Cas (cắt nén thời gian), tháo đèn lồng, quỳ một gối; đèn lồng hạ xuống dưới hai cánh tay cậu, cách tường 0,62 m.
const IDA_K = [-0.75, 0.75], kneelYaw = yawTo(-0.75, 0.75, LAN_T[0], LAN_T[2]);
// Tư thế cục bộ (không có trong sheet): quỳ một gối (crouch_lantern) + tay phải đưa đèn lồng ra trước, ngang hông cậu bé.
const kneelHold = (p, ctx, o = {}) => kneelOf(p, ctx, { joints: { spine: [8, 0, 0], shoulder_R: [-88, 0, -6], elbow_R: [-6, 0, 0], ...(o.joints || {}) } });
wallShot('s30', 86.0, 88.0, { size: 'MS', angle: 'ngang, sau-phải', mm: 35, move: 'tĩnh', idaDetail: 28,
  why: 'Ida tháo đèn lồng, quỳ cạnh cậu, cầm thấp sau tay cậu, cách tường một sải tay (≤ 0,7 m — luật 3.3).', sound: 'kim loại quai đèn; vải',
  light: 'đèn lồng tới gần tường (ấm) trong nền trắng', action: 'Ida tháo đèn lồng, quỳ một gối bên trái Cas; đèn lồng hạ xuống dưới hai cánh tay cậu.' },
  (p, cam, ctx) => { const kn = kneelHold(p, ctx); const standL = over(p.stand, { props: ['lantern_hand_R'], joints: { shoulder_R: [-20, 0, -10] } });
    return { exposure: 1.0, update(t, T, { ida, cas }) {
    cas.place(over(p.C.turnaround, { joints: { neck: [22, 0, 0] } }), ...CAS_W, yawTo(...CAS_W, ...IDA_K));
    const pose = t < 0.7 ? over(walkPose(t, p.stand), { props: ['lantern_belt'] }) : poseAt([[0.7, over(p.stand, { joints: { neck: [10, 0, 0] } })], [0.95, standL], [1.05, standL], [1.85, kn]], t);
    ida.place(pose, valAt([[0, -1.3], [0.7, IDA_K[0]]], t), valAt([[0, 1.85], [0.7, IDA_K[1]]], t), valAt([[0, yawTo(-1.3, 1.85, ...IDA_K)], [0.7, yawTo(-1.3, 1.85, ...IDA_K)], [1.3, kneelYaw]], t));
    if (t > 1.2) { const lan = ida.props.lantern; if (lan && lan.parent) { const k = ease((t - 1.2) / 0.65); lan.updateMatrixWorld(true); const a = wpos(lan.userData.lightAnchor); lanternTo(ida, [a.x + (LAN_T[0] - a.x) * k, 0, a.z + (LAN_T[2] - a.z) * k]); } }
    cam.position.set(2.6, 1.4, 4.0); cam.lookAt(-0.1, 0.8, 0.7); return { lantern: t < 0.95 ? 0.012 : 0.8 + (LAN_K - 0.8) * ease((t - 1.0) / 0.9) }; } }; });
wallShot('s31', 88.0, 91.0, { size: 'MCU', angle: 'ngang mắt Ida (quỳ), 3/4 trước-phải, qua vai phải Cas', mm: 85, move: 'tĩnh', idaExpr: 'sad_smile', idaDetail: 36,
  why: 'Lời mời, không dạy: bà đưa ánh sáng, cậu tự làm.', sound: 'THOẠI L3 "Go on, then." (88,0–90,3)',
  light: 'đèn lồng ấm dưới mặt bà (≈ 0,6 m); trắng phẳng từ trên', action: 'Ida quỳ, đèn lồng thấp trong tay phải, quay đầu về Cas, nói L3.' },
  (p, cam, ctx, dbg) => { const kn = kneelHold(p, ctx, { joints: { neck: [-8, -24, 0] } }); return { exposure: 1.0, update(t, T, { ida, cas }) {
    cas.place(over(p.C.turnaround, { joints: { neck: [22, 0, 0] } }), ...CAS_W, yawTo(...CAS_W, ...IDA_K));
    ida.place(kn, ...IDA_K, kneelYaw); lanternTo(ida, LAN_T);
    const h = wpos(ida.joints.head); h.y += 0.1; const o = dbg.co || [1.6, 0.05, 1.25]; cam.position.set(h.x + o[0], h.y + o[1], h.z + o[2]); cam.lookAt(h.x, h.y - 0.02, h.z); return { lantern: LAN_K }; } }; });
wallShot('s32', 91.0, 94.0, { size: 'WS', angle: 'ngang, sau-phải', mm: 35, move: 'tĩnh',
  why: 'Chim trở lại, TO hơn, ấm, rìa mềm (tay gần nguồn — luật 3.2, 3.3) và bay.', sound: 'Cas cười khẽ (chờ SFX có giấy phép — để trống); nhạc tạm vào',
  light: 'đèn lồng thấp dưới tay Cas, cách tường 0,62 m (key ấm, có bóng) trong nền trắng', action: 'Cas giơ tay vào quầng hổ phách; chim to hiện cao trên tường và bay.' },
  (p, cam, ctx, dbg) => { const kn = kneelHold(p, ctx, { joints: { neck: [-14, -10, 0] } }); return { exposure: 1.0, update(t, T, { ida, cas }) {
    const bird = p.bird(t, 1.2); const sw = Math.sin(t * 0.9) * 10;
    const cz = valAt([[0, CAS_W[1]], [0.2, CAS_W[1]], [0.9, CAS_S32[1]]], t);
    cas.place(poseAt([[0, over(p.C.turnaround, { joints: { neck: [22, 0, 0] } })], [0.8, over(birdReach(bird), { joints: { spine: [-4, sw, 0] } })]], t), CAS_W[0], cz, valAt([[0, yawTo(...CAS_W, ...IDA_K)], [0.7, CAS_YAW]], t));
    ida.place(kn, ...IDA_K, kneelYaw); lanternTo(ida, LAN_T); cam.position.set(...(dbg.cp || [1.9, 1.35, 4.1])); cam.lookAt(...(dbg.cl || [-0.25, 1.45, 0])); return { lantern: dbg.lk ?? LAN_K }; } }; });

// ---------------- CẢNH 5 — Ngọn cuối ----------------
// V2 (1:20–1:29, s33–s34): bản v2 để Cas SÁT vách (0,45 m) → bóng cậu ×1,18 gần bằng người, rìa sắc, đứng ngay sau lưng cậu → AI mù đọc "hai cậu bé".
// Sửa bằng quang học thật (luật 3.2, 3.5): phóng đại = (đèn → vách) ÷ (đèn → người). Đèn lồng đặt cách vách 3,0 m, lệch trái 0,3 m (x = −0,25).
//   Ida cách vách 1,6 m (đèn → bà 1,4 m) → ×2,14: bóng cao ≈ 3,5 m, lệch TRÁI bà 0,34 m;
//   Cas cách vách 0,9 m (đèn → cậu 2,1 m) → ×1,43: bóng ≈ 1,9 m (to hơn cậu, rìa mềm hơn), lệch PHẢI cậu 0,30 m → người và bóng tách nhau.
//   Hai bóng: bà ≈ 3,5 m, cậu ≈ 1,9 m ("hers, tall… his, small") — tỷ lệ 1,87. Viền sáng trên người: ánh dội vách bên (uSide) + đèn lồng sau lưng.
const BAY = { lan: [-0.25, 3.0], ida: [-0.55, 1.6], cas: [0.45, 0.9] };
function placeBayLantern(r, x, z) {   // dời đèn lồng + nguồn sáng (spot có bóng, omni bù trong shader, quầng sprite) — cùng một nguồn điểm
  const old = r.flameP.clone(); r.lan.position.x = x; r.lan.position.z = z; r.lan.updateMatrixWorld(true);
  r.lan.userData.lightAnchor.getWorldPosition(r.flameP);   // sửa tại chỗ: onSample của s5 giữ tham chiếu tới chính vectơ này
  const d = r.flameP.clone().sub(old); r.scene.traverse((o) => { if (o.isSprite && o.position.distanceTo(old) < 0.6) o.position.add(d); });
  r.spot.position.copy(r.flameP); U.uLP.value.copy(r.flameP); U.uLDir.value.copy(r.spot.target.position).sub(r.flameP).normalize(); r.spot.updateMatrixWorld();
}
S({ id: 's33', scene: 5, size: 'WS', angle: 'ngang 1,35 m, "tranh trong tranh"', mm: 32, move: 'dolly vào chậm (0,9 m)',
  why: 'Hình trung tâm (7A, khung style frame c_s5_wide): trong hốc cửa khuất điện, đèn lồng dưới đất; Ida dừng gần đèn nên bóng bà vươn CAO (×2,14), Cas đi tới gần vách nên bóng cậu NHỎ hơn bóng bà (×1,43), lệch sang phải cậu — người và bóng tách nhau. Ngoài vòm phố trắng không bóng.',
  sound: 'nhạc tạm; bước chân vào hốc; rè điện xa', light: 'đèn lồng trên nền đá (nguồn thấp, có bóng); ngoài vòm: điện phẳng',
  action: 'Ida đặt đèn lồng, hai người bước vào; Ida dừng giữa hốc, Cas đi tới gần vách; hai bóng một cao một nhỏ.',
  async build(ctx) {
    const r = await buildBaySet(ctx, {}); const p = P(ctx); const dbg = ctx.dbg || {}; const cam = r.cam; const c0 = cam.position.clone(); [r.chIda, r.chCas].forEach((c) => tameGlint(c));
    for (const ch of [r.chIda, r.chCas]) { ch.sheetRef = ch.sheet; }
    const B = { ...BAY, ...(dbg.bay || {}) }; placeBayLantern(r, ...B.lan);
    const keep = () => { if (!r.lan.parent) r.scene.add(r.lan); };
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT, grade: GRADE_S5, exposure: 1.0,
      update(t) {
        const zI = valAt([[0, 3.5], [1.2, 3.5], [3.2, B.ida[1]]], t), zC = valAt([[0, 3.9], [1.3, 3.9], [4.7, B.cas[1]]], t);
        const pI = t < 1.2 ? lerpPose(p.crouch, p.stand, ease(t / 1.2)) : t < 3.2 ? over(walkPose(t - 1.2, p.stand), { props: [] }) : poseAt([[3.2, over(p.stand, { props: [] })], [4.4, over(p.lookShadows, { props: [] })]], t);
        const pC = t < 1.3 ? p.C.turnaround : t < 4.7 ? walkPose(t - 1.3, p.C.turnaround, { gait: WALK_CHILD, bothArms: true }) : poseAt([[4.7, p.C.turnaround], [5.8, p.C.half_raised]], t);
        r.chIda.setPose({ ...pI, props: [] }); keep(); r.chIda.root.position.set(B.ida[0], pI.root_y_m ?? 0, zI); r.chIda.root.rotation.y = Math.PI + 0.30 * clamp01((t - 3.0) / 0.8); r.chIda.root.updateMatrixWorld(true);
        r.chCas.setPose(pC); keep(); r.chCas.root.position.set(B.cas[0], pC.root_y_m ?? 0, zC); r.chCas.root.rotation.y = Math.PI - 0.25 * clamp01((t - 4.5) / 0.8); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) { ctx.upd(r.chIda, cam); ctx.upd(r.chCas, cam); }
        cam.position.copy(c0).add(new THREE.Vector3(0, 0, -0.9 * ease(t / 7))); } };
  } });

S({ id: 's34', scene: 5, size: 'MS (nghiêng)', angle: 'ngang ngực, từ phía phải, sau đèn lồng', mm: 30, move: 'tĩnh',
  why: 'Ida ngửa nhìn bóng mình cao vút; bên phải, Cas đứng trước vách, bóng cậu (to hơn cậu, mềm hơn) lệch sang phải cậu — trái → phải: Ida, bóng Ida, Cas, bóng Cas; người có màu và viền sáng, bóng phẳng và tối (V2).',
  sound: 'lửa thở; nhạc tạm', light: 'đèn lồng dưới đất sau lưng hai người (key thấp, có bóng); viền má và mép mũ; dội ấm vách bên',
  action: 'Ida ngửa nhìn bóng, tay đặt lên ngực; Cas giơ nửa tay nhìn bóng mình.',
  async build(ctx) {
    const dbg = ctx.dbg || {};
    const r = await buildBaySet(ctx, { medium: { pos: dbg.cp || [1.3, 1.15, 3.6], look: dbg.cl || [-0.3, 1.5, 0.6], fov: fovOf(30) } }); [r.chIda, r.chCas].forEach((c) => tameGlint(c)); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    const B = { ...BAY, ...(dbg.bay || {}) }; placeBayLantern(r, ...B.lan);
    r.chIda.root.position.set(B.ida[0], 0, B.ida[1]); r.chCas.root.position.set(B.cas[0], 0, B.cas[1]); for (const ch of [r.chIda, r.chCas]) ch.root.updateMatrixWorld(true);
    return { scene: r.scene, cam: r.cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: 1.0, update() {} };
  } });

// Bộ phố cuối (góc ngọn 11): cột góc (POST_ON[5], đoạn cáp cuối) tắt tới giữa câu L4 → góc chỉ có hổ phách + bóng dài; sau đó trắng tràn.
// Cuối phố (V3): sets_end.buildStreetEnd — nhà kho có hốc cửa (tâm z = −4,6), góc nhà z = +2, ngõ cong rẽ trái, mái xa + sương.
const endStreet = (o = {}) => buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: o.shadowLamps || [] });
const cornerFill = (T) => 0.06 + 1.04 * switchOn(T, POST_ON[5]);
// Cas giữ thang: đứng sau chân thang (phía mặt tiền), mặt về +z, hai tay trên hai thanh dọc (x = 8 ± 0,17) ở độ cao ≈ 0,9 m.
const CAS_LAD = [8.0, -4.98];
const FAST_CHILD = { cycle_s: 0.7, stride_m: 0.5, speed_mps: 1.43 };
S({ id: 's35', scene: 5, size: 'WS', angle: 'ngang, xuôi dốc', mm: 28, move: 'tĩnh',
  why: 'Góc ngọn cuối vẫn TỐI (đoạn cáp cuối chưa bật): ngọn L11 là nguồn duy nhất, bóng dài. Bà đi ra từ phía hốc cửa (cuối phố, nền), tới thang, trèo lên lần cuối; Cas chạy theo giữ thang bằng hai tay. V3: cuối phố là nhà kho + hốc cửa + ngõ cong, không còn tường trống.', sound: 'bước chân; thang; rè điện xa',
  light: 'đèn khí L11 (ấm, có bóng); phố trắng ở xa sau lưng máy', action: 'Ida đi dọc mặt tiền phía bắc tới chân thang, trèo; Cas chạy theo giữ thang.',
  async build(ctx) {
    const st = endStreet({ shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(28); cam.position.set(16.5, 1.7, 2.6); cam.lookAt(5.5, 2.3, -3.8);
    const I0 = [5.9, -4.9], C0 = [3.9, -3.6];
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: expo(2.4, 1.15, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f);
        if (t < 2.3) ida.place(over(walkPose(t, p.stand), { props: ['lantern_belt'] }), valAt([[0, I0[0]], [2.3, LAMP_X(11)]], t), valAt([[0, I0[1]], [2.3, FOOT_Z]], t), yawTo(...I0, LAMP_X(11), FOOT_Z));
        else if (t < 3.4) { const u = (t - 2.3) / 1.1; ida.place(p.climb(u, p.restLadder), LAMP_X(11), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); } else ida.place(p.restLadder, LAMP_X(11), ON_Z, 0);
        if (t < 3.0) cas.place(walkPose(t, p.C.turnaround, { gait: FAST_CHILD, bothArms: true }), valAt([[0, C0[0]], [3.0, CAS_LAD[0]]], t), valAt([[0, C0[1]], [3.0, CAS_LAD[1]]], t), yawTo(...C0, ...CAS_LAD));
        else cas.place(poseAt([[3.0, p.C.turnaround], [3.6, p.C.hold_ladder]], t), ...CAS_LAD, 0); } };
  } });

const faceShot = (id, meta, fn) => S({ id, scene: 5, ...meta,
  async build(ctx) {
    const st = endStreet({ shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: meta.expr, gaze: [0.05, -0.04], glint: 0.45 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(meta.mm); const ctl = fn(p, cam);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: ctl.exposure ?? expo(0.36, 0.9, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); cas.place(p.C.hold_ladder, ...CAS_LAD, 0); ctl.update(t, T, ida); } };
  } });
faceShot('s36', { size: 'MCU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'tĩnh', expr: 'neutral',
  why: 'Quyết định C4 của chủ dự án: bà TỰ đẩy vành mũ ra sau trước câu thoại — mặt thoáng ra cho lời từ biệt. Góc còn tối: mặt ấm một bên.', sound: 'vải dạ; hơi thở',
  light: 'đèn khí L11 ngay trước mặt (ấm) — góc chưa có điện', action: 'Tay trái đưa lên vành mũ (hat_push_a), đẩy vành lên, mũ ngả ra sau (hat_push_b).' },
  (p, cam) => ({ update(t, T, ida) { ida.place(poseAt([[0, p.hatA], [0.35, p.hatA], [1.05, p.hatB], [1.6, p.faceRest()]], t), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: 1.9, y: -0.05, fov: fovOf(85) }); } }));
faceShot('s37', { size: 'CU', angle: 'ngang mắt, gần chính diện', mm: 85, move: 'đẩy vào rất chậm', expr: 'sad_smile',
  why: 'Lời từ biệt, vế đầu: cười buồn, còn trong hổ phách của ngọn cuối. Máy đẩy vào không nhận ra được.', sound: 'THOẠI L4 "That\'s the last one, then. Goodnight, old street."',
  light: 'đèn khí L11 (ấm) — góc chưa có điện', action: 'Ida nhìn lên phố (phải khung), tay đặt trên van.' },
  (p, cam) => ({ update(t, T, ida) { ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); faceCam(cam, ida, { dist: valAt([[0, 1.1], [5.8, 0.97]], t), fov: fovOf(85) }); } }));

// Toàn cảnh góc ngọn cuối (s37w, s40w): cột điện góc (đoạn cáp cuối) ở trái khung, ngọn L11 + thang ở phải khung, cuối phố (nhà kho, hốc cửa, ngõ cong) ở giữa.
const cornerWide = (id, meta, fn) => S({ id, scene: 5, size: 'WS', angle: 'ngang, từ lòng phố, hơi hất', mm: 28, move: 'tĩnh', ...meta,
  async build(ctx) {
    const st = endStreet({ shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 24 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 22 });
    const cam = camMM(28); cam.position.set(17.0, 1.6, 1.2); cam.lookAt(8.8, 3.6, 0.6);
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: expo(2.4, 1.15, (T) => switchOn(T, POST_ON[5])),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); cas.place(over(p.C.hold_ladder, { joints: { neck: [-30, 0, 0] } }), ...CAS_LAD, 0); fn(p, t, T, ida); } };
  } });
cornerWide('s37w', { why: 'CHỈ ĐẠO CHỦ DỰ ÁN (1:50 v1): ngay quanh "You\'ll be brighter now", bóng đèn cột góc (đoạn cáp cuối) nhấp hai lần rồi đứng trắng; trắng tràn vào góc, bóng dài và bóng tối biến mất. Câu thoại khớp với hình. V3: cuối phố là nhà kho có hốc cửa + ngõ cong, không còn tường trống.',
  sound: 'THOẠI L4 (ngoài hình) "…You\'ll be brighter now."; tách rơ-le gần; bóng đèn rít; rè điện', light: 'cột điện góc bật (nhấp 2 lần, đứng) — trắng phẳng tràn góc; L11 nhạt dần',
  action: 'Ida trên thang, Cas giữ thang; bóng đèn điện bật, bóng dài của hai người trên đá lát tan.' },
  (p, t, T, ida) => ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0));
S({ id: 's38', scene: 5, size: 'MS', angle: 'cao, chúc xuống (gần mắt Ida)', mm: 50, move: 'tĩnh',
  why: 'Phản ứng của Cas: cậu giữ thang, ngước nhìn bà trong ánh trắng mới — người nghe câu nói thay khán giả.', sound: 'L4 tiếp (ngoài hình)',
  light: 'trắng phẳng (cột góc vừa bật); ấm rất yếu từ L11 trên cao', action: 'Cas giữ hai thanh thang, ngửa mặt nhìn lên.',
  async build(ctx) {
    const st = endStreet(); const p = P(ctx); ladderAt(st.scene, 11); const dbg = ctx.dbg || {};
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 20 }); const cas = makeChar(ctx, st.scene, 'cas', { detail: 34 });
    const cam = camMM(50); cam.position.set(...(dbg.cp || [8.75, 2.45, -3.55])); cam.lookAt(...(dbg.cl || [8.0, 0.95, -5.0]));
    const cp = dbg.cas || CAS_LAD;
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: cornerFill }), f); ida.place(p.faceRest(), LAMP_X(11), ON_Z, 0); cas.place(over(p.C.hold_ladder, { joints: { neck: [-36, 0, 0] } }), ...cp, 0);
        if (dbg.log && f % 12 === 0) console.log(JSON.stringify({ id: 's38', handL: V3a(wpos(cas.joints.wrist_L)), handR: V3a(wpos(cas.joints.wrist_R)) })); } };
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
cornerWide('s40w', { why: '"Nothing else changes": ngọn cuối đã tắt, phố trắng y nguyên — không một đèn nào nhấp. Máy tĩnh, giữ 2 s (cùng khung s37w: so sánh trước/sau).',
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
  why: 'Cas mang đèn lồng rời phố trắng, bước qua vòm vào hốc cửa khuất điện (nơi hai cái bóng đứng lúc trước): ánh hổ phách đi theo cậu vào trong bóng tối. Cậu vẫn đội mũ len (V1: nối với s42).', sound: 'bước chân trẻ con; rè điện xa dần',
  light: 'ngoài vòm: điện phẳng; trong hốc: chỉ đèn lồng Cas mang theo', action: 'Cas đi từ phố vào vòm, dừng giữa hốc, đặt đèn xuống trước mặt.',
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
        const x = valAt([[0, 1.9], [1.7, CAS_BAY[0]]], t), z = valAt([[0, 5.3], [1.7, CAS_BAY[1]]], t);
        const w = walkPose(t, p.C.turnaround, { gait: WALK_CHILD });
        const pose = t < 1.7 ? over(w, { joints: { shoulder_L: carry.joints.shoulder_L, elbow_L: carry.joints.elbow_L, shoulder_R: carry.joints.shoulder_R, elbow_R: carry.joints.elbow_R }, hands: carry.hands }) : carry;
        r.chCas.setPose(pose); r.chCas.root.position.set(x, pose.root_y_m ?? 0, z); r.chCas.root.rotation.y = t < 1.5 ? yawTo(1.9, 5.3, ...CAS_BAY) : valAt([[1.5, yawTo(1.9, 5.3, ...CAS_BAY)], [2.0, -Math.PI]], t); r.chCas.root.updateMatrixWorld(true);
        if (ctx.upd) ctx.upd(r.chCas, cam);
        if (r.lan.parent !== r.scene) r.scene.add(r.lan); hangFromHands(r.lan, r.chCas, h); moveLamp(); } };
  } });

// V1 (2:00, s42): nguyên nhân tìm được (xem LAYOUT-W2.md): (1) máy CHÍNH DIỆN, thấp 0,72 m, đặt SAU đèn lồng nhìn vào Cas → hai lòng bàn tay (xoay 70° về
// phía kính = về phía máy) chính diện, xoè, gần máy hơn đầu → tay to bất thường; (2) quả bông đỏ khuất sau đầu (máy thấp hơn đỉnh mũ), mũ len màu kem
// #d6c9ae được lửa rọi từ dưới + quầng sprite của đèn lồng phủ lên → mũ đọc thành "tóc vàng"; (3) dáng ngồi xổm (hông −96°, gối 124°) nhìn thẳng từ trước
// → hai gối dồn giữa khung, thân ngắn lại → "méo". Mũ KHÔNG rơi (mũ gắn khớp đầu). Sửa bằng máy + dàn dựng, không đổi tỷ lệ sheet:
// máy 3/4 từ trước-trái của cậu, cao ngang đỉnh mũ (0,95 m), lùi 3,0 m, 40 mm; đèn lồng không nằm giữa máy và cậu; đầu + quả bông in trên phố trắng qua vòm.
const CAS_BAY = [0.3, 3.4];
S({ id: 's42', scene: 5, size: 'MS', angle: 'ngang đỉnh mũ, 3/4 trước-trái Cas, trong hốc nhìn ra vòm', mm: 40, move: 'tĩnh',
  why: 'Trả mô-típ: trong góc tối cậu tự chọn, không ai bảo, Cas đặt đèn xuống, hơ hai lòng tay trên kính đếm ba — đúng như bà. Qua vòm: phố trắng; Ida đứng ở miệng vòm nhìn vào, không nói. V1: mũ len + quả bông in rõ trên nền phố trắng; tay thấy nghiêng 3/4, đúng cỡ.', sound: 'lửa đèn lồng thở; nhạc tạm',
  light: 'đèn lồng trên nền đá (nguồn duy nhất trong hốc); ngoài vòm: điện phẳng', action: 'Cas ngồi xổm, áp tay: một, hai, ba. Ida ở miệng vòm (trái khung).',
  async build(ctx) {
    const dbg = ctx.dbg || {};
    const r = await buildBaySet(ctx, {}); const p = P(ctx); for (const ch of [r.chIda, r.chCas]) ch.sheetRef = ch.sheet;
    const cam = r.cam; cam.shiftY = 0; [r.chIda, r.chCas].forEach((c) => tameGlint(c)); cam.fov = fovOf(dbg.mm ?? 40); cam.position.set(...(dbg.cp || [-1.35, 0.95, 0.55])); cam.lookAt(...(dbg.cl || [0.05, 0.62, 4.0])); cam.updateProjectionMatrix();
    const wc = p.C.warm_hands_copy, wcIn = over(wc, { joints: { shoulder_L: [-66, 0, 10], shoulder_R: [-66, 0, -10], elbow_L: [-28, 0, 0], elbow_R: [-28, 0, 0] } });
    const hC = (wc.root_y_H ?? 0) * ctx.sheets.cas.H_m;
    placeBayLantern(r, CAS_BAY[0] - 0.02, CAS_BAY[1] - 0.55);
    r.chIda.setPose(over(p.stand, { props: [], joints: { neck: [12, 0, 0] } })); r.chIda.root.position.set(-0.95, 0, 5.2); r.chIda.root.rotation.y = Math.PI + 0.2; r.chIda.root.updateMatrixWorld(true);
    return { scene: r.scene, cam, onSample: r.onSample, named: { ida: r.chIda, cas: r.chCas }, paintP: S5_PAINT_MED, grade: GRADE_S5, exposure: dbg.exp ?? 0.6,
      update(t) {
        let k = 0; for (const b of [0.6, 1.2, 1.8]) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        r.chCas.setPose({ ...lerpPose(wc, wcIn, k), props: [] }); r.chCas.root.position.set(CAS_BAY[0], hC, CAS_BAY[1]); r.chCas.root.rotation.y = Math.PI; r.chCas.root.updateMatrixWorld(true);
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
  (p, cam) => { const c0 = cam.position.clone(); return { update(t, T, ida) { ida.setPose({ ...p.lookShadows, props: [] }); ida.root.updateMatrixWorld(true); cam.position.copy(c0).add(new THREE.Vector3(0, 0, 0.5 * ease(t / 3))); } }; });
// s45: máy 3/4 trước-phải bà (tính theo đầu + hướng mặt), thấy cả mặt đồng hồ trong tay và mặt bà ngẩng lên — bản v2 máy sau vai, không thấy đồng hồ.
alleyShot('s45', 137.0, 139.0, { size: 'MS', angle: 'ngang ngực, 3/4 trước-phải', mm: 50, move: 'tĩnh', exposure: 6.0,
  why: 'ĐỒNG HỒ NHỊP 3a — hai giờ sau (10:00): bà lấy đồng hồ ra (9:53, vẫn chậm 7 phút), rồi ngẩng nhìn về phía mặt đồng hồ quảng trường trên mái.', sound: 'tích tắc; rè điện xa',
  light: 'ánh cửa sổ ấm từ trên', action: 'Ida nhìn đồng hồ trong tay, rồi ngẩng nhìn về phía miệng ngõ.' },
  (p, cam, r, dbg) => { let wf = null; return { update(t, T, ida) {
    if (!wf) wf = watchInHand(ida.root.parent);
    ida.setPose(poseAt([[0, over(p.watchHold(0), { props: [] })], [1.0, over(p.watchHold(0), { props: [] })], [1.6, over(p.watchHold(0), { props: [], joints: { neck: [-14, 0, 0] } })]], t)); ida.root.updateMatrixWorld(true);
    const h = wpos(ida.joints.head), q = new THREE.Quaternion(); ida.root.getWorldQuaternion(q); const fw = new THREE.Vector3(0, 0, 1).applyQuaternion(q); fw.y = 0; fw.normalize();
    const dir = fw.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), (dbg.yaw ?? -35) * Math.PI / 180);
    cam.fov = fovOf(50); cam.updateProjectionMatrix(); cam.position.copy(h).addScaledVector(dir, dbg.dist ?? 1.75); cam.position.y = h.y - 0.05; cam.lookAt(h.x, h.y - 0.28, h.z);
    wf(ida, cam, ...hands(CLOCKS.beat3.watchFrom)); } }; });
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
        const b = p.bird(t, 1.0); cas.place(over(b, { joints: { spine: [-4, sw, 0], neck: [-26, 0, 0], shoulder_L: [sh, b.joints.shoulder_L[1], b.joints.shoulder_L[2]], shoulder_R: [sh, b.joints.shoulder_R[1], b.joints.shoulder_R[2]] } }), 0.6 + 0.15 * Math.sin(t * 0.6), cz, -0.15); } };
  } });

// ---------- MỐC SỰ KIỆN (xuất cho âm tạm, phụ đề, SHOTLIST) — cùng nguồn với hình ----------

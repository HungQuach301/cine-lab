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
const CAS_SPOT = [-1.2, -2.2];
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
    const st = buildStreetSet({ sky: 'dusk', x0: 85, x1: 200, shadowLamps: [3], fog: [30, 260] }); const p = P(ctx);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 });
    // W1: máy chéo lên phố (~23° về bắc so với trục phố): mặt tiền bắc lùi sâu bên trái, đèn L3–L1 đã thắp nối nhau về quảng trường,
    // mái + ống khói lớp sau và trời chạng vạng ở trên. Ida từ xa tiến về máy, trôi PHẢI → TRÁI trên khung (giữ hướng cảnh 1–3).
    const cam = camMM(35); cam.position.set(103.5, 1.45, 3.6); cam.lookAt(116.0, 2.6, -1.6);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(walkPose(t + 0.3, p.I.walk_ladder), 114.5 - WALK.speed_mps * t, WALK_Z, -Math.PI / 2); lanternLit(ida, false); } };
  } });

S({ id: 's03', scene: 1, t0: 8.5, t1: 10.5, size: 'MS', angle: 'thấp, hất lên', mm: 50, move: 'tĩnh',
  why: 'Góc thấp cho nghi thức: tay mở van, "phụp", hổ phách nở trên mặt bà.',
  sound: 'kẽo kẹt thang; tiếng xì khí; "phụp" (9,2 s)', light: 'đèn khí L4 vừa mồi (nguồn chính), trời chạng vạng',
  action: 'Ida lên nốt bậc thang, tay phải mở van; ngọn L4 bắt lửa.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 80, x1: 140, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 });
    const cam = camMM(50); cam.position.set(103.2, 0.95, -0.2); cam.lookAt(106.0, 3.0, -4.3);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.0,
      update(t, T, f) { st.setState(stdState(T), f);
        const pose = t < 0.55 ? p.climb(0.55 + t / 1.2, p.restLadder) : poseAt([[0.55, p.restLadder], [0.75, p.valveLadder], [1.3, p.valveLadder], [1.9, p.warmLadder]], t);
        const u = clamp01(0.55 + t / 1.2); ida.place(pose, LAMP_X(4), t < 0.55 ? FOOT_Z + (ON_Z - FOOT_Z) * ease(u) : ON_Z, 0); lanternLit(ida, false); } };
  } });

S({ id: 's04', scene: 1, t0: 10.5, t1: 12.0, size: 'WS', angle: 'cao, từ bên kia phố', mm: 28, move: 'tĩnh',
  why: 'Cho thấy BÓNG của bà (bóng = dấu vết con người, luật thế giới mục 2): bóng dài, mềm trên mặt tiền và đá lát.',
  sound: 'room tone; lửa thở rất khẽ', light: 'đèn khí L4 (có bóng)',
  action: 'Ida trên thang, hai tay đưa lên kính; bóng người + thang đổ dài lên tường nhà.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 80, x1: 200, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 });
    const cam = camMM(28); cam.position.set(99.5, 5.2, 3.2); cam.lookAt(106.5, 1.2, -4.6);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.0,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(poseAt([[0, p.valveLadder], [0.8, p.warmLadder]], t), LAMP_X(4), ON_Z, 0); lanternLit(ida, t >= 1.2); } };   // đèn lồng bắt lửa 1,2 s (nhịp tay: Cổng 6)
  } });

S({ id: 's05', scene: 1, t0: 12.0, t1: 16.0, size: 'MCU', angle: 'ngang mắt, 3/4 trước-trái', mm: 85, move: 'tĩnh (khung style frame a_close_ida)',
  why: 'Thói quen hơ tay đếm ba là mô-típ sẽ trả lại ở 2:07 (Cas). Cận đủ để đếm được ba nhịp tay và nghe lời chào con phố.',
  sound: 'THOẠI L1 "Evening, old street." (12,0–14,16); lửa thở', light: 'đèn khí L4 ngay trước mặt (ấm), trời lạnh viền',
  action: 'Hai lòng tay áp gần kính: một, hai, ba (12,3 / 12,9 / 13,5); nói L1; hạ tay.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 90, x1: 125, shadowLamps: [4] }); const p = P(ctx); ladderAt(st.scene, 4);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'neutral', glint: 0.6 });
    const cam = camMM(85); let camSet = false;
    const beats = [12.3, 12.9, 13.5].map((b) => b - 12);
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
      ida.place(pose, LAMP_X(4), ON_Z, 0); }
  } });

S({ id: 's06', scene: 1, t0: 16.0, t1: 20.0, size: 'CU (insert)', angle: 'chúc nhẹ, góc nhìn của Ida', mm: 100, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 1 — gieo mô-típ đồng hồ chậm 7 phút (4A): đồng hồ bỏ túi chỉ 7:31; gõ kính hai lần là thói quen thân thương. Mặt chỉ có vạch, không chữ số.',
  sound: 'hai tiếng gõ kính; tích tắc rất khẽ', light: 'đèn khí L4 phía trên; trời chạng vạng',
  action: 'Dưới chân thang, Ida mở đồng hồ bỏ túi (7:31 — giờ thật 7:38), gõ kính hai lần bằng móng tay, cất đi.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 95, x1: 118, shadowLamps: [], groundSoft: 24 }); const p = P(ctx); ladderAt(st.scene, 4);   // (c) nền nhoè thay DOF
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 30 }); const watch = watchInHand(st.scene);
    const cam = camMM(100); const [mD, hD] = hands(CLOCKS.beat1.watch);
    exposeClock(st.scene);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.4,
      update(t, T, f) { st.setState(stdState(T), f);
        let tap = 0; for (const b of [0.8, 1.2]) tap = Math.max(tap, Math.exp(-(((t - b) / 0.07) ** 2)));
        const pose = t < 2.3 ? p.watchHold(tap) : lerpPose(p.watchHold(0), p.stand, ease((t - 2.3) / 0.6));
        ida.place(pose, LAMP_X(4) + 0.6, LAMP_Z + 0.9, 0.35);
        watch(ida, cam, mD + 6 * t / 60, hD, new THREE.Vector3(-0.15, 0.8, 0.6), 0.32); } };
  } });

S({ id: 's07', scene: 1, t0: 20.0, t1: 24.0, size: 'WS', angle: 'ngang tầm mắt', mm: 35, move: 'dolly ngang theo Ida (phải→trái)',
  why: 'Nhịp sáng–tối của phố đèn khí; bóng bà quét từ trước ra sau khi đi qua cột — cái sẽ mất ở cảnh 2.',
  sound: 'bước chân, thang kẽo kẹt; nhạc tạm', light: 'đèn khí L4, L5 (vừa thắp — lược thời gian)',
  action: 'Ida vác thang đi qua cột L5; bóng đổ ngang đá lát, xoay theo vị trí cột.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 60, x1: 130, shadowLamps: [5] }); const p = P(ctx);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T), f); const x = 95.2 - WALK.speed_mps * t;
        ida.place(walkPose(t, p.I.walk_ladder), x, WALK_Z, -Math.PI / 2);
        camAt(cam, [[0, [96.0, 1.4, 4.3], [93.6, 1.6, -2.6]], [4, [92.4, 1.4, 4.3], [90.0, 1.6, -2.6]]], t); } };   // W1: lệch máy về trái — khoảng trống phía trước Ida
  } });

S({ id: 's08', scene: 1, t0: 24.0, t1: 26.0, size: 'WS (tele)', angle: 'ngang tầm mắt', mm: 135, move: 'tĩnh',
  why: 'Tele nén phố: Ida nhỏ ở tiền cảnh, quảng trường và cột đồng hồ (chưa sáng) ở xa. Tiếng rơ-le "tách" báo điều sắp đến; bà không để ý.',
  sound: 'rơ-le "tách" xa; room tone', light: 'đèn khí dọc phố; đồng hồ quảng trường còn tắt',
  action: 'Ida đi về phía máy; xa sau lưng là quảng trường.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'dusk', x0: 55, x1: 200, shadowLamps: [], fog: [40, 330], farLit: 0 }); const p = P(ctx);   // W1: sương xa cho tele — quảng trường + dãy nhà xa đọc được
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 18 }); const cam = camMM(135); cam.position.set(58, 1.6, 0.6); cam.lookAt(176, 3.4, 0.2);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.4,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(walkPose(t, p.I.walk_ladder), 88.5 - WALK.speed_mps * t, WALK_Z + 0.6, -Math.PI / 2 - 0.12); } };
  } });

// ---------------- CẢNH 2 — Bật điện ----------------
S({ id: 's09', scene: 2, size: 'MS', angle: 'thấp, hất lên cột đồng hồ', mm: 50, move: 'tĩnh',
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

S({ id: 's09w', scene: 2, size: 'CU (insert)', angle: 'POV của Ida, tay giơ', mm: 105, move: 'tĩnh',
  why: 'ĐỒNG HỒ NHỊP 2b — cắt khớp ngay sau tiếng chuông: đồng hồ bỏ túi của bà chỉ 7:53. Giờ mới đã tới mà giờ của bà còn 7 phút: "trễ" đọc bằng hình, không chữ.',
  sound: 'dư âm chuông; tích tắc gần', light: 'đèn khí L6 (ấm) trên tay; trời đêm',
  action: 'Ida (dưới cột L6) giơ đồng hồ bỏ túi ngang tầm mắt: 7:53.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 55, x1: 110, shadowLamps: [], groundSoft: 24 }); const p = P(ctx);   // (c) nền nhoè thay DOF
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const watch = watchInHand(st.scene); const cam = camMM(105);
    const [mD, hD] = hands(CLOCKS.beat2.watch);
    exposeClock(st.scene);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.6,
      update(t, T, f) { st.setState(stdState(T), f); ida.place(p.watchRaise, LAMP_X(6) + 1.2, WALK_Z, -Math.PI / 2);
        const wp = new THREE.Vector3(0, -0.07, 0); ida.joints.wrist_R.localToWorld(wp);
        const eye = new THREE.Vector3(); ida.joints.head.getWorldPosition(eye); eye.y += 0.1;
        watch(ida, cam, mD + 6 * t / 60, hD, eye.sub(wp).normalize().add(new THREE.Vector3(0, 0.55, 0)), 0.42); } };
  } });

S({ id: 's10e', scene: 2, size: 'MS (chèn)', angle: 'thấp, hất lên đầu cột điện', mm: 35, move: 'tĩnh',
  why: 'NGUỒN ĐIỆN THẤY ĐƯỢC: bóng đèn điện trên cột quảng trường nhấp hai lần rồi đứng trắng (kịch bản dòng 48), loá lạnh, gắt, trên nền trời đêm có sao. Đồng hồ vừa sáng ở hậu cảnh.',
  sound: 'tách rơ-le gần; bóng đèn rít; rè điện 50 Hz', light: 'bóng đèn điện quảng trường (trắng lạnh, loá) — nguồn thấy trong khung',
  action: 'Bóng đèn tối → sáng → tắt → sáng → đứng trắng; vũng trắng phẳng tràn xuống đá lát.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 150, x1: 200, shadowLamps: [] }); const hp = st.squarePosts[0].hp;
    const cam = camMM(35); cam.position.set(163.0, 1.3, hp.z + 4.4); cam.lookAt(hp.x + 0.8, hp.y - 1.4, hp.z - 0.6);   // W1: máy trong quảng trường (v2 đặt ở x = 161,3 — nay là sau mặt tiền góc)
    return { scene: st.scene, cam, named: {}, paintP: PAINT_STREET, exposure: expo(1.8, 1.1, (T) => switchOn(T, SQUARE_ON)),
      update(t, T, f) { const s0 = stdState(T); st.setState(s0, f); st.clock.userData.setHands(6 * Math.max(0, T - DING) / 60, 240); } };
  } });

S({ id: 's10', scene: 2, size: 'EWS', angle: 'cao, sau quảng trường', mm: 28, move: 'tĩnh',
  why: 'Toàn cảnh lặp khung mở đầu để đo thay đổi, nay là ĐÊM (trời xanh đen, không hồng): tấm kính quanh quảng trường đứng trắng, từng khối phố bật lan xuống dốc. Khối cuối cạnh nhà kho CHƯA bật (đoạn cáp cuối).',
  sound: 'rè điện lớn dần; các tiếng "tách" nối tiếp', light: 'đèn điện (trắng phẳng) lan khỏi quảng trường; đèn khí còn lại',
  action: 'Sóng trắng lăn xuống dốc theo phố Ostler; một đoạn cuối phố còn hổ phách.',
  async build(ctx) { const c = await buildCitySet(ctx, 'wave', { square: SQUARE_ON, t0: T0.s10, skipLast: 1 }); return { ...c, exposure: 1.0, grade: GRADE_COLD }; } });

S({ id: 's11', scene: 2, size: 'MS', angle: 'ngang, 3/4 trước-trái', mm: 50, move: 'tĩnh',
  why: 'Phản ứng: bà quay về phía quảng trường (phải khung = hướng sóng tới).',
  sound: 'rè điện từ xa; tách', light: 'đèn khí L7 vừa thắp (ấm), ánh trắng lờ mờ phía xa',
  action: 'Ida trên thang ở cột L7, quay đầu và vai về phía quảng trường.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const cam = camMM(50); cam.position.set(61.6, 2.5, -1.2); cam.lookAt(64.0, 2.9, -4.4);
    const wf = whiteAt(64);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 2.2,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 0.3 * wf(T) }), f); ida.place(poseAt([[0, p.restLadder], [0.3, p.restLadder], [1.2, p.turnSquare]], t), LAMP_X(7), ON_Z, 0); } };
  } });

S({ id: 's12', scene: 2, size: 'WS (qua vai)', angle: 'cao ngang vai Ida, nhìn lên phố', mm: 35, move: 'tĩnh',
  why: 'Qua vai bà: bóng đèn cột điện x=85 nhấp hai lần rồi đứng (nguồn thấy được); trắng nuốt những ngọn bà vừa thắp (L5, L6) — vũng hổ phách mỏng dần. Trời đêm phía trên.',
  sound: 'tách; rè điện', light: 'cột điện x=85 bật; đèn khí L5, L6 chìm trong trắng',
  action: 'Lưng/vai Ida tiền cảnh trái; phía xa bóng đèn điện bật, phố trắng dần.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 55, x1: 200, shadowLamps: [], fog: [30, 220] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35); cam.position.set(62.3, 3.4, -5.0); cam.lookAt(100, 2.6, -1.0);
    const wf = whiteAt(85);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.2, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 0.5 * wf(T) }), f); ida.place(p.turnSquare, LAMP_X(7), ON_Z, 0); } };
  } });

S({ id: 's13', scene: 2, size: 'MS', angle: 'thấp nhẹ, 3/4 trước-phải', mm: 50, move: 'tĩnh',
  why: 'Sóng tới chính bà (0:40, câu hỏi c1): mặt bà đổi từ ấm sang trắng phẳng; bà nhìn xuống.',
  sound: 'rè điện gần; tách', light: 'trắng tràn tới (nhấp 2 lần), đèn khí L7 còn đó nhưng chìm',
  action: 'Trắng tràn lên người Ida; bà cúi nhìn xuống đá lát.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 100, shadowLamps: [7] }); const p = P(ctx); ladderAt(st.scene, 7);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 28 }); const cam = camMM(50); cam.position.set(66.8, 2.0, -1.0); cam.lookAt(64.0, 2.9, -4.4);
    const wf = (T) => switchOn(T, REACH_IDA);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.1, wf),
      update(t, T, f) { st.setState({ ...stdState(T, { whiteFill: (T) => 1.2 * wf(T) }), gasLight: (i) => (i === 7 ? 1 - 0.85 * clamp01((T - REACH_IDA) / 0.5) : 1) }, f);   // W1: ánh L7 chìm trong trắng → bóng nhạt hết trong 0,5 s (luật 3.3)
        ida.place(poseAt([[0, p.turnSquare], [0.5, p.turnSquare], [1.3, p.lookDown]], t), LAMP_X(7), ON_Z, 0); } };
  } });

S({ id: 's14', scene: 2, size: 'MS (chúc)', angle: 'cao, chúc xuống đá lát', mm: 28, move: 'tĩnh',
  why: 'Hình then chốt cảnh 2: bóng dài đã mất; bà giơ tay — không gì động trên đá lát.',
  sound: 'rè điện đều; im', light: 'trắng phẳng (không bóng); vệt tối mờ dưới chân thang',
  action: 'Ida giơ tay trái lên; nền đá không có bóng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 45, x1: 90, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 7);   // W1: L7 chìm trong trắng → không bóng dài (luật 3.1, 3.3)
    const liftHigh = over(p.liftHand, { joints: { shoulder_L: [-62, 0, 34], elbow_L: [-12, 0, 0], wrist_L: [0, 0, -10] } });   // W1 cục bộ: tay trái giơ ra trước-ngang, lòng úp
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 24 }); const cam = camMM(28); cam.position.set(65.9, 4.5, -2.3); cam.lookAt(64.0, 1.4, -4.7);   // W1: từ phía đầu dốc, chúc ~50° — v2 cắt đầu Ida, lồng đèn che người
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.1,
      update(t, T, f) { st.setState({ ...stdState(T, { whiteFill: () => 1.2 }), gasLight: (i) => (i === 7 ? 0.15 : 1) }, f); ida.place(poseAt([[0, p.lookDown], [0.4, p.lookDown], [1.1, liftHigh]], t), LAMP_X(7), ON_Z, 0); } };
  } });

// ---------------- CẢNH 3 — Chạy đua ----------------
// Montage nén thời gian: mỗi shot có nhịp "nở hổ phách → trắng phủ" riêng; cột điện bật theo POST_ON.
S({ id: 's15', scene: 3, size: 'WS', angle: 'ngang tầm mắt', mm: 35, move: 'tĩnh',
  why: 'Chuyển cảnh: bà xuống thang, quay người về phía dốc xuống (trái khung) — đuổi theo phần phố chưa có điện. Trời đêm trên mái.',
  sound: 'bước xuống thang; rè điện', light: 'trắng phẳng (cột x=85); đèn khí L7 chìm',
  action: 'Ida tụt nhanh xuống thang, vác thang, quay về phía dốc xuống.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 0, x1: 100, shadowLamps: [], fog: [12, 55] }); const p = P(ctx); const lad = ladderAt(st.scene, 7);   // sương gần: đoạn dốc dưới chìm tối (trắng tràn previs là toàn cục — Cổng 7 làm ánh theo khối)
    // W1: máy phía nam nhìn chéo XUÔI dốc: Ida trong trắng ở phải khung; trái khung là đoạn phố dưới còn tối (chưa điện, chưa thắp) — nơi bà sắp chạy tới.
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const cam = camMM(35); cam.position.set(69.5, 1.5, 3.4); cam.lookAt(60.0, 2.1, -4.0);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: 1.15,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.1 }), f); lad.visible = t < 1.1;   // W1: thang lên vai ở 1,1 s → hết cảnh hai cái thang
        if (t < 0.8) { const u = 1 - t / 0.8; ida.place(p.climb(u, p.restLadder), LAMP_X(7), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); }
        else ida.place(poseAt([[0.8, p.stand], [1.4, over(p.stand, { props: ['ladder_shoulder', 'lantern_belt'], joints: p.I.walk_ladder.joints })]], t), LAMP_X(7) - 0.3, FOOT_Z + 0.5, valAt([[0.8, 0], [1.4, -Math.PI / 2]], t)); } };
  } });

const lampShot = (id, i, cam0, why, extra = {}) => S({ id, scene: 3, size: 'WS', angle: extra.angle || 'ngang', mm: extra.mm || 35, move: 'tĩnh', why,
  sound: `"phụp" L${i}; tách + rè khi cột điện bật`, light: `đèn khí L${i} vừa thắp (có bóng) → bóng đèn cột điện nhấp hai lần, đứng trắng`,
  action: extra.action || `Ida trên thang ở L${i}: hổ phách nở, bóng dài; vài giây sau cột điện bật, trắng phủ, bóng tan trong 0,5 s.`,
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: Math.max(0, LAMP_X(i) - 30), x1: 200, shadowLamps: [i], fog: extra.fog }); const p = P(ctx); ladderAt(st.scene, i);   // W1: dựng tới quảng trường
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 24 }); const cam = camMM(extra.mm || 35); cam.position.set(...cam0[0]); cam.lookAt(...cam0[1]);
    const wf = whiteAt(LAMP_X(i));
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_STREET, exposure: expo(2.2, 1.15, wf),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: (T) => 1.1 * wf(T) }), f);
        ida.place(poseAt([[0, p.valveLadder], [0.5, p.valveLadder], [1.2, p.warmLadder]], t), LAMP_X(i), ON_Z, 0); } };
  } });
lampShot('s19', 8, [[41.0, 1.7, 1.0], [53.0, 3.0, -0.5]], 'Montage: ngọn thứ 8 nở hổ phách, bóng bà đổ dài — rồi bóng đèn cột điện x=57 (trong khung, phải) nhấp hai lần, đứng trắng, xoá bóng.');
S({ id: 's21', scene: 3, t0: 58.0, t1: 60.0, size: 'MCU (tay)', angle: 'ngang, 3/4', mm: 85, move: 'tĩnh',
  why: 'Vội: trèo quá nhanh, tuột sào mồi rồi chụp lại — lần đầu thấy tay bà không vững.',
  sound: 'thang rung; sào gỗ va; hơi thở gấp', light: 'trắng phẳng; L10 chưa thắp',
  action: 'Ida trèo nhanh lên L10, sào mồi trượt khỏi tay (58,9), chụp lại (59,4).',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 0, x1: 50, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 10);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 32 }); const cam = camMM(85); cam.position.set(20.1, 3.1, -2.3); cam.lookAt(22.0, 3.0, -4.5);
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 1.1,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.0 }), f);
        const cu = 0.66 + 0.34 * t / 0.7;   // W1: bắt đầu ở bậc cao hơn (v2 bắt đầu 0,4 → khung đầu trống)
        const pose = t < 0.7 ? lerpPose(p.climb(cu, p.poleLadder), p.poleLadder, 0) : poseAt([[0.7, p.poleLadder], [0.9, p.poleFumble], [1.3, p.poleFumble], [1.5, p.poleLadder]], t);
        ida.place(t < 0.7 ? { ...pose, props: ['pole_hand_R', 'lantern_belt'] } : pose, LAMP_X(10), t < 0.7 ? FOOT_Z + (ON_Z - FOOT_Z) * ease(cu) : ON_Z, 0);
        const pole = ida.props.pole; if (pole && t > 0.85 && t < 1.45) pole.rotation.z = 0.5 * Math.sin((t - 0.85) / 0.6 * Math.PI); else if (pole) pole.rotation.z = 0; } };
  } });

S({ id: 's22', scene: 3, t0: 60.0, t1: 63.0, size: 'MCU', angle: 'ngang mắt, 3/4', mm: 85, move: 'tĩnh',
  why: 'Lời thoại duy nhất của cảnh chạy đua; ngọn L10 bắt lửa ấm lên mặt bà rồi bị trắng dìm ngay.',
  sound: 'THOẠI L2 "Not yet... not yet." (60,0–62,88); "phụp" (62,95, sau câu thoại, tràn qua điểm cắt)', light: 'trắng phẳng; đèn khí L10 bắt lửa ở khung cuối (ấm lên mặt)',
  action: 'Ida lẩm bẩm, mở van; lửa bắt ngay khi câu dứt; hổ phách chìm trong trắng.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 5, x1: 40, shadowLamps: [] }); const p = P(ctx); ladderAt(st.scene, 10);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 36, faceQ: 1.4, expr: 'strained', glint: 0.5 }); const cam = camMM(85); let camSet = false;
    return { scene: st.scene, cam, named: { ida }, paintP: PAINT_CLOSE, exposure: 0.8,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 1.0 }), f);
        // W1: tay phải trên van suốt shot; sào mồi chuyển sang tay trái NGOÀI KHUNG (liên tục s21 → s22, xem continuity canh-3.md).
        // v2 kết bằng hai lòng tay xoè (warmLadder) — mâu thuẫn với tay trái đang cầm sào → bỏ; giữ tay trên van tới khi lửa bắt.
        const v0 = over(p.valveLadder, { joints: { neck: [-4, 30, 0] } }), v1 = over(p.valveLadder, { joints: { neck: [-10, 26, 0], elbow_R: [-52, 0, 0] } });
        if (!camSet) { ida.place(v0, LAMP_X(10), ON_Z, 0); faceCam(cam, ida, { yaw: -12, dist: 1.2, fov: fovOf(85) }); camSet = true; }   // W1: máy tĩnh (v2 trôi theo đầu)
        ida.place(poseAt([[0, v0], [1.6, v0], [2.4, v1]], t), LAMP_X(10), ON_Z, 0); } };
  } });

S({ id: 's23', scene: 3, t0: 63.0, t1: 66.0, size: 'WS', angle: 'ngang, nhìn xuôi dốc về nhà kho', mm: 28, move: 'tĩnh',
  why: 'Góc ngọn cuối cạnh bức tường vôi nhà kho thuộc ĐOẠN CÁP CUỐI (luật thế giới mục 1, v0.4): cột điện góc còn TẮT, góc còn tối; phố sau lưng bà đã trắng. Chỉ đạo chủ dự án 0:40.',
  sound: 'bước chạy; thang; "phụp"', light: 'L11 bắt lửa; cột điện góc (x=11) còn tắt; phố trắng ở xa sau lưng',
  action: 'Ida hối hả tới L11, trèo, thắp. Hổ phách.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 60, shadowLamps: [11] }); const p = P(ctx); const lad = ladderAt(st.scene, 11);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 22 }); const C23 = (ctx.dbg && ctx.dbg.s23cam) || S23_CAM; const cam = camMM(C23.mm); cam.position.set(...C23.pos); cam.lookAt(...C23.look);   // dbg.s23cam: thử máy khi đo
    const fast = { cycle_s: 0.9, stride_m: 0.6, speed_mps: 1.3 };
    // N1 (rà continuity P): Cas đã đứng ở chân tường chim từ trước (s24 thấy cậu ở đó) → có mặt trong s23, đứng yên, nhỏ ở nền, nhìn về L11/Ida.
    const cas = mkChar(ctx, st.scene, 'cas', { detail: 16 }); const [cx, cz] = casSpotOf(st);
    if (ctx.dbg && ctx.dbg.limeMask) limeMask(st);   // đo V3: tỷ lệ điểm ảnh mặt vôi trắng nhà kho (chỉ khi --dbg '{"limeMask":1}' --nopaint)
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: ctx.dbg && ctx.dbg.limeMask ? 1.0 : expo(2.4, 1.8, (T) => gasLevel(11, T)),
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.06 }), f);
        cas.place(p.C.turnaround, cx, cz, yawTo(cx, cz, LAMP_X(11), ON_Z));
        lad.visible = t >= 1.1;   // W1: thang trên vai khi chạy (liên tục s15), dựng vào cột ở 1,1 s (tư thế then chốt Cổng 6: "dựng thang")
        if (t < 1.1) ida.place(walkPose(t, p.I.walk_ladder, { gait: fast }), valAt([[0, 14.2], [1.1, LAMP_X(11) + 0.2]], t), valAt([[0, WALK_Z], [1.1, FOOT_Z]], t), yawTo(14.2, WALK_Z, LAMP_X(11), FOOT_Z));
        else if (t < 1.9) { const u = (t - 1.1) / 0.8; ida.place(p.climb(u, p.valveLadder), LAMP_X(11), FOOT_Z + (ON_Z - FOOT_Z) * ease(u), 0); }
        else ida.place(poseAt([[1.9, p.valveLadder], [2.5, p.warmLadder]], t), LAMP_X(11), ON_Z, 0);
        if (st.scene.userData.blackenLater) st.scene.userData.blackenLater(); } };
  } });

S({ id: 's24', scene: 3, t0: 66.0, t1: 68.0, size: 'MS', angle: 'hơi cao, 3/4 trước-phải', mm: 35, move: 'tĩnh',
  why: 'Nhịp đếm ba lần thứ hai; góc cuối phố chỉ còn hổ phách. Ở nền, cậu bé đứng ở tường nhìn bà — bà không thấy (gieo cảnh 4).',
  sound: 'lửa thở; im lặng tương đối', light: 'đèn khí L11 (ấm) — góc cuối phố chưa có điện',
  action: 'Ida áp tay vào kính: một, hai, ba. Xa phía sau, Cas nhìn.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 30 }); const cas = mkChar(ctx, st.scene, 'cas', { detail: 20 });
    const cam = camMM(30); cam.position.set(11.2, 2.1, 1.8); cam.lookAt(10.5, 1.8, -5.8);   // A2 (B1, W2 A2): Ida (L11) trái, Cas ở sân trước hông phải, gần hơn 3 m để Cas đọc được; P5 (10,8; 3,9) sau máy, tia tới Cas qua trước góc nhà x = 15   // giai đoạn C: Ida (L11) trái–giữa, Cas ở chân tường chim phải khung (casSpot W2)
    const [cx, cz] = casSpotOf(st);
    const beats = [0.2, 0.8, 1.4];
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_STREET, exposure: 1.6,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.05 }), f);
        let k = 0; for (const b of beats) k = Math.max(k, Math.exp(-(((t - b) / 0.16) ** 2)));
        ida.place(lerpPose(p.warmLadder, p.warmLadderIn, k), LAMP_X(11), ON_Z, 0);
        cas.place(p.C.turnaround, cx, cz, yawTo(cx, cz, LAMP_X(11), ON_Z)); } };
  } });

S({ id: 's24c', scene: 3, size: 'MS', angle: 'ngang mắt Cas, 3/4 trước-phải', mm: 50, move: 'tĩnh',
  why: 'Giới thiệu Cas rõ (AI mù v1: "Cas 1:04–1:06 chỉ là một chấm"): cậu bé áo len quá khổ, một mình ở chân tường nhà kho, mặt ấm lên vì ngọn L11 vừa thắp; cậu nhìn bà.',
  sound: 'lửa thở xa; im', light: 'đèn khí L11 (ấm, bên phải khung); góc tối', action: 'Cas đứng dựa tường vôi, nhìn về phía cột đèn (phải khung), tay giấu trong tay áo.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: -12, x1: 30, shadowLamps: [11] }); const p = P(ctx); ladderAt(st.scene, 11);
    const ida = mkChar(ctx, st.scene, 'ida', { detail: 18 }); const cas = mkChar(ctx, st.scene, 'cas', { detail: 34, expr: 'neutral' });
    const [cx, cz] = casSpotOf(st);
    // A2 (B1): máy 3/4 trước Cas, lệch −35° khỏi hướng nhìn của cậu về L11, cách 2,1 m (tính theo casSpot — hướng tới L11 đổi khi Cas dời).
    const gx = LAMP_X(11) - cx, gz = ON_Z - cz, gl = Math.hypot(gx, gz), ga = -35 * Math.PI / 180, dx = (gx * Math.cos(ga) - gz * Math.sin(ga)) / gl, dz = (gx * Math.sin(ga) + gz * Math.cos(ga)) / gl;
    const cam = camMM(50); cam.position.set(cx + 2.1 * dx, 1.05, cz + 2.1 * dz); cam.lookAt(cx, 0.95, cz);   // giai đoạn C: 3/4 trước Cas (lệch 35° khỏi hướng nhìn về L11) — Cas nhìn sang TRÁI khung (về Ida), tường chim sau lưng
    return { scene: st.scene, cam, named: { ida, cas }, paintP: PAINT_CLOSE, exposure: 4.5,
      update(t, T, f) { st.setState(stdState(T, { whiteFill: () => 0.05 }), f); ida.place(p.warmLadder, LAMP_X(11), ON_Z, 0);
        cas.place(over(p.C.turnaround, { joints: { neck: [-4, valAt([[0, -10], [0.6, -10], [1.3, 6]], t), 0] } }), cx, cz, yawTo(cx, cz, LAMP_X(11), ON_Z)); } };
  } });


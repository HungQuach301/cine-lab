// V5b-2c · CẢNH (d) — TOÀN CẢNH PHỐ 1782 ĐÔNG NGƯỜI (lệnh V0 mục e, loại cảnh "toàn cảnh đông người"): máy trên sườn tây Rock (≈ 75 m trên mặt đất) nhìn tây-tây-bắc
//  qua phố 1782 (ghost SH + lấp ước tính), Grand Parade có đội hình đồn trú (vị trí bãi tập: khối "phía nam / phía bắc Grand Parade" của plan Drinkwater; SỐ LƯỢNG,
//  CÁCH XẾP minh hoạ), người đi các phố, Line Wall + King's Bastion (OSM, M5) đang bắn (khói từ 09:45), hàng 10 pin nổi + khói ngoài vịnh, đồi Algeciras hậu cảnh.
//  Giờ 10:40 → 10:44 ngày 13/9/1782 (M6; V5b-2d dời từ 09:52 cho đúng thứ tự thời gian đoạn thử), push-in chậm (vai "cơ chế" (phố vận hành dưới vây hãm)). Không người trong vùng khói (life/units nhận zones); không cận mặt (người ≥ 250 m).
import { pushIn, grammar, grammarLog, ALT_MAX } from '../campath.js';
import { ease } from '../core.js';
import { town1782, units, smoke } from '../layers.js';
import { makeFleet, lineFormation } from '../ships.js';
import { life, chimneysFrom, freePath } from '../life.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };   // V5b-2d (C2-9): vách bắc sắc hơn + đỉnh 412 m theo ảnh PD LoC 2025710362 (terrain.js)
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };   // trời Địa Trung Hải sáng tháng 9: chân trời xanh hơn (S 0,33 → 0,46)   // V5b-2c (I5): bóng đổ bớt xám-lam, ánh dội đất ấm (0,74: không cháy sáng)
export const GRADE = { vib: 0.62 };   // V5b-2c (I5): vibrance 0,35 → 0,62 (vữa/đá nhạt lên màu; màu đã đậm gần như giữ)
export const META = { cau: 'push-in', vai: 'co-che', noi: [[0, 99, 'thanh_pho']], nam: 1782 };
const MAIN = [[-409, -1811], [-410, -1700], [-425, -1620], [-435, -1571], [-441, -1543], [-448, -1521], [-450, -1505], [-447, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880], [-417, -788]];
export async function build(ctx) {
  const { THREE, terr, scene } = ctx, fps = 24, DUR = 6.0, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), H = (h, m) => h + m / 60;
  ctx.ships.group.visible = false;
  // V5b-2d: máy trên mặt vịnh trước King's Bastion, ≈ 150 m trên mặt nước, nhìn đông-đông-bắc xuống phố (King's Bastion + Line Wall tiền cảnh, phố dày, Grand Parade
  //  có đồn trú, sườn Rock hậu cảnh). C2-2 vẫn khai vết máy (không có khối lấp ước tính nào trong 150 m — chỉ nước + Line Wall).
  const CAM0 = [-720, 152, -1550], CAM1 = [-700, 148, -1515];
  const TOWN = await town1782(ctx, { kbOpt: { h: 9 }, near: { track: [[CAM0[0], CAM0[2]], [CAM1[0], CAM1[2]]], r: 150 } }), KBC = [-602, -1276];
  const recs = TOWN.FP.list.flatMap((l) => l.recs);
  // đồn trú trên Grand Parade (giữa khối K1782-10 và K1782-12/13) — 4 khối, quay tây
  const GP = [-505, -1165];
  const TR = units([[-16, -26], [16, -26], [-16, 0], [16, 0], [-16, 26], [16, 26]].map(([de, dn], i) => ({ at: [GP[0] + de, GP[1] + dn], heading: 270, rows: 8, cols: 30, side: 'gb', day: [0, 99], seed: 21 + i })), ctx); scene.add(TR.group);
  const FIN = lineFormation({ n: 10, center: [-1430, -1330], axis: 172, spacing: 140, kind: 'battery' });
  const fleet = makeFleet(ctx.U, FIN.map((s) => Object.assign(s, { heading: 172 }))); scene.add(fleet.group);
  fleet.group.traverse((o) => { if (o.isMesh) ctx.maskify(o.material, ctx.U, 1); });
  const sm = smoke([{ at: [-655, 14, -1274], t: [H(9, 45), 24], n: 16, size: 46, rise: 70, drift: [-3, 1], period: 0.09, seed: 11, alpha: 0.8 },
    { at: [-585, 12, -1500], t: [H(9, 46), 24], n: 10, size: 36, rise: 55, drift: [-3, 1], period: 0.1, seed: 12, alpha: 0.7 },
    { at: [-590, 12, -1050], t: [H(9, 47), 24], n: 10, size: 36, rise: 55, drift: [-3, 1], period: 0.1, seed: 13, alpha: 0.7 },
    ...FIN.map((s, i) => ({ at: [s.at[0] + 18, 10, s.at[1]], t: [H(9, 50) + i * (35 / 60) / 9, 24], n: 18, size: 58, rise: 75, drift: [4, 1], period: 0.1, seed: 40 + i, alpha: 0.85 }))], ctx);
  scene.add(sm.group);
  // V5b-2d (C2-1 mục 3, C2-7): máy ≥ 250 m tới phố → người ĐƠN ẩn (near 150 m), thay bằng ĐÁM ĐÔNG dày (cụm 15–45 người, cỡ thật, không phóng to) dọc Main Street
  //  và phố sau Line Wall (Irish Town); thành phần: đa số áo đỏ đồn trú (≈ 7 000 quân, Drinkwater 1785 p. 292 — claim S065), ít dân (dân đã dạt về nam từ 4/1781 — S062)
  const LINEST = [[-560, -1700], [-552, -1500], [-548, -1350], [-546, -1200], [-545, -1050], [-548, -930]];
  const LF = life({ seed: 1779, walkers: [{ pts: freePath(MAIN, recs), n: 120, width: 3, near: 150, colors: ['#b03a2e', '#a8402e', '#e7e0cf', '#5e4a38', '#3d4a5a'] }],
    crowds: [{ pts: freePath(MAIN, recs), groups: 16, size: [15, 45], speed: 0.5, colors: ['#b03a2e', '#a8402e', '#b03a2e', '#e7e0cf', '#5e4a38'] }, { pts: freePath(LINEST, recs), groups: 9, size: [12, 30], speed: 0.4, colors: ['#b03a2e', '#2f3d5c', '#b03a2e', '#e7e0cf'] }],
    birds: [{ c: [-350, -1250], r: 150, h: 60, base: 40, n: 16 }], boats: [{ pts: [[-700, -900], [-745, -1150], [-735, -1450], [-690, -1700]], len: 13, speed: 4.2, s0: 0.2 }, { pts: [[-690, -1650], [-735, -1350], [-750, -1050], [-710, -800]], len: 11, speed: 3.6, s0: 0.6 }],
    chimney: { at: chimneysFrom(recs.filter((r) => r[1] > 0), 22), drift: [-1.4, 0.4] } }, ctx);
  scene.add(LF.group); ctx.maskHide = [sm.group].concat(LF.smokeGroup ? [LF.smokeGroup] : []);
  // máy: sườn tây Rock phía trên phố (E −190, N −1330, ≈ 75 m trên đất) → đẩy nhẹ về tây; nhìn xuống phố + vịnh
  const sh = pushIn({ vai: 'co-che', from: CAM0, to: CAM1, look: [-400, -30, -1250], t0: 0, t1: DUR, hold: 1.0, fov: 41, fov1: 39 });
  const G = grammar([sh]);
  const clockH = (t) => H(10, 40) + t * (4 / 60) / DUR;   // V5b-2d (C2-5): 10:40–10:44 — sau cảnh eo đất 10:32 (thứ tự thời gian trong đoạn thử)
  function state(t) { const hh = clockH(t), jd = jdLocal(1782, 9, 13, hh), ph = G.phaseAt(t); return { year: 1782.7, day: 0.5, cam: G.path.at(t), spp: 2, phase: ph.kind, preset: 'push-in', vai: 'co-che', hero: null, noi: 'thanh_pho', hours: hh, clock: clockLabel(jd), sun: sunPos(jd) }; }
  let troops = null, song = null;
  function apply(st, t) { TOWN.update(st.year, ctx.cam); fleet.update(st.hours); sm.update(st.hours); const z = sm.zones(st.hours); troops = TR.update(st.day, z); song = LF.update(t ?? 0, z); }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  function overlay(t, st, T, proj) {
    T.chrome(t, { s: st.clock.s }, 0, null, { lines: [{ s: TOWN.INFILL_SRC, a: Math.max(0, Math.min(1, (t + 0.3) / 0.35, (DUR + 0.5 - t) / 0.35)) }, { s: 'Troops, crowds, boats: illustrative · gardens: 1782 plan', a: Math.max(0, Math.min(1, (t + 0.3) / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Gibraltar, 13 Sep 1782');
    T.ghostSrc(t, [-1, DUR + 1], TOWN.src);
    T.card(t, [0.6, DUR], 'Grand Parade, 1782', 'Parade ground on the siege plan · troops illustrative', proj(V([GP[0], 8, GP[1]])));
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt });
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: { grand_parade: [GP[0], 8, GP[1]] }, namKhung: (st) => TOWN.namMax(st.year),
    meta: Object.assign({ quan: TR.stat(), town: TOWN.stat(), doPx: { quan: [[-16, -26], [16, -26], [-16, 0], [16, 0], [-16, 26], [16, 26]].map(([de, dn]) => [GP[0] + de, hAt(GP[0] + de, GP[1] + dn), GP[1] + dn]),
      dam_dong: freePath(MAIN, recs).filter((_, i) => i % 3 === 0).map(([e, n]) => [e, hAt(e, n), n]) } }, META), troops: () => troops, song: () => song, smokeZones: (st) => sm.zones(st.hours) };
}

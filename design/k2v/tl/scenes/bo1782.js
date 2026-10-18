// V5b-2d · CẢNH (g) — BỜ + CHIẾN SỰ 13/9/1782 ~17:15 LMT (lệnh C2-1 mục 4 chủ dự án 18/10; loại cảnh 6 "bờ + chiến sự").
//  Máy thấp (16 m) trên mặt vịnh phía TÂY hàng pin nổi, ống kính dài (fov 16°), nhìn ĐÔNG về Line Wall + King's Bastion + phố 1782 + Rock: bờ chiếm ≥ 1/2 khung.
//  Dữ kiện theo giờ (M6):
//   · "the smoke which had been observed to issue from the upper part of the flagship appeared to prevail … and the admiral's second was perceived to be in the
//     same condition" (Drinkwater 1785, p. 298, buổi chiều); lửa bùng ~17:00 (Montero 1860 / Spilsbury — claim S066) → CHỈ 2 pin nổi có lửa (Pastora = soái hạm,
//     neo ~900 yard trước King's Bastion — S066; chiếc kế bên = "admiral's second"), lửa nhỏ trên boong (≤ 15 % khung đỏ), không người trên tàu;
//   · gió chiều: "the wind having changed to the south-west and blowing a smart breeze, with a heavy swell" (p. 298) → khói trôi ĐÔNG-BẮC; vì gió/sóng này
//     "mortar boats and bomb-ketches … were prevented taking a part in the action" (p. 298) → KHÔNG dựng pháo hạm/thuyền cối trong khung (đúng nguồn);
//   · xuồng: pin nổi "attended by a number of boats" (p. 295) và chiều tối "several boats were seen to row round the disabled ships" (p. 298) → xuồng chèo quanh
//     hai pin nổi đang cháy (vị trí minh hoạ);
//   · đồn trú tiếp tục bắn đạn nung (8 300 phát ngày 13/9, quá nửa là đạn nung — S075) → khói dày dọc Line Wall + King's Bastion.
//  Mặt trời thiên văn 13/9/1782 17:15 LMT (≈ 11° trên chân trời, phương vị ≈ 266°) chiếu thẳng mặt phố hướng tây. Không người trong vùng khói/lửa.
import { lateral, grammar, grammarLog, ALT_MAX } from '../campath.js';
import { smoke, town1782 } from '../layers.js';
import { makeFleet, lineFormation } from '../ships.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';
import { life, chimneysFrom } from '../life.js';

export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };   // V5b-2d (C2-9): vách bắc sắc hơn + đỉnh 412 m theo ảnh PD LoC 2025710362 (terrain.js)
export const LOOK = { hemiI: 0.58, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.34, 0.52, 0.86], fogC: [0.52, 0.58, 0.78], sunC: '#ffcf96', sunI: 3.1 };   // chiều muộn: nắng thấp ngả vàng cam (11° trên chân trời), fill dịu → mặt phố có khối
export const GRADE = { vib: 0.62 };
export const META = { cau: 'lateral-parallax', vai: 'he-qua', moc_dinh: '1782-09-13T17:15 LMT', noi: [[0, 99, 'bien']], nam: 1782 };
export async function build(ctx) {
  const { THREE, terr, scene } = ctx, fps = 24, DUR = 6.0, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), H = (h, m) => h + m / 60;
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx, { kbOpt: { h: 9, soot: 0.55, face: [-1, 0], faceMin: -0.25 } });   // máy ≥ 800 m tới bờ → không phải khung gần (C2-2 không áp)
  const FIN = lineFormation({ n: 10, center: [-1430, -1330], axis: 172, spacing: 140, kind: 'battery' });
  const PAST = 4, SEC = 5;   // Pastora (soái hạm, giữa hàng — trước King's Bastion) + "admiral's second"
  const fleet = makeFleet(ctx.U, FIN.map((s) => Object.assign(s, { heading: 172 }))); scene.add(fleet.group);
  fleet.group.traverse((o) => { if (o.isMesh) ctx.maskify(o.material, ctx.U, 1); });
  // khói: (a) pin nổi bắn (mạn đông) — trôi đông-bắc theo gió SW; (b) hai pin nổi cháy: khói đen dày + lửa nhỏ trên boong; (c) Line Wall + King's Bastion bắn đạn nung
  const SW = [2.6, 2.2];
  const sm = smoke([
    ...FIN.map((s, i) => ({ at: [s.at[0] + 22, 9, s.at[1]], t: [H(9, 50) + i * (35 / 60) / 9, 24], n: 26, size: 64, rise: 80, drift: SW, period: 0.1, seed: 40 + i, alpha: i === PAST || i === SEC ? 0.7 : 0.95, zone: 'path' })),   // V5b-2d: khói pháo dày (đấu pháo toàn tuyến từ 10:25 — S067)
    ...[PAST, SEC].map((i, k) => ({ at: [FIN[i].at[0] + 4, 12, FIN[i].at[1] + (k ? -6 : 6)], t: [H(17, 0), 24], n: 18, size: 40, rise: 120, drift: [1.8, 2.0], period: 0.06, seed: 70 + k, alpha: 1.0, dark: true, zone: 'path' })),
    ...(ctx.opt.noFire ? [] : [PAST, SEC]).flatMap((i, k) => [-9, 2, 11].map((dn, j) =>   // --opt '{"noFire":true}': lượt đo % lửa (khác biệt có/không lửa)
      ({ at: [FIN[i].at[0] - 6, 9.5, FIN[i].at[1] + dn], t: [H(17, 0) + j * 0.01, 24], n: 2, size: 24 - 4 * k, rise: 4, drift: [0.2, 0.2], period: 0.05, seed: 80 + k * 3 + j, alpha: 1, fire: k ? 0.8 : 1.0, zone: 'path' }))),
    ...[-1560, -1480, -1400, -1330, -1274, -1210, -1150, -1080, -1020, -950, -900].map((n, k) => ({ at: [-650 - (n === -1274 ? 30 : 0), 13, n], t: [H(9, 45), 24], n: 12, size: 36, rise: 60, drift: SW, period: 0.1, seed: 120 + k, alpha: 0.8, zone: 'path' }))], ctx);
  scene.add(sm.group);
  // xuồng chèo quanh hai pin nổi cháy (Drinkwater p. 295, 298) — vòng ~70 m, minh hoạ
  const ring = (c, r, a0) => [...Array(9).keys()].map((k) => { const a = a0 + k / 8 * 6.283; return [c[0] + Math.cos(a) * r, c[1] + Math.sin(a) * r * 0.8]; });
  const recs1782 = TOWN.FP.list.flatMap((l) => (l.kind === 'ghost' ? l.recs : []));
  const LF = life({ seed: 1309, birds: [{ c: [-900, -1300], r: 220, h: 60, n: 10 }],
    boats: [{ pts: ring(FIN[PAST].at, 75, 0), len: 10, speed: 2.4, s0: 0.1 }, { pts: ring(FIN[PAST].at, 90, 2), len: 9, speed: 2.0, s0: 0.55 }, { pts: ring(FIN[SEC].at, 80, 1), len: 10, speed: 2.2, s0: 0.3 },
      { pts: ring(FIN[SEC].at, 64, 4), len: 8, speed: 1.8, s0: 0.8 }, { pts: [[FIN[PAST].at[0] - 260, FIN[PAST].at[1] + 120], [FIN[PAST].at[0] - 90, FIN[PAST].at[1] + 30]], len: 11, speed: 1.6, s0: 0.2 }],
    chimney: { at: chimneysFrom(recs1782, 10), drift: [1.4, 1.2] } }, ctx);
  scene.add(LF.group); ctx.maskHide = [sm.group].concat(LF.smokeGroup ? [LF.smokeGroup] : []);
  // máy: tây hàng pin nổi ~900 m, cao 16 m, ống dài 16°, trượt ngang 90 m (parallax pin nổi ↔ phố)
  const sh = lateral({ vai: 'he-qua', c: [-800, 100, -1330], yaw: 6.3, dist: 1560, len: 90, h: 16, t0: 0, t1: DUR, fov: 15, hAt });
  const G = grammar([sh]);
  const clockH = (t) => H(17, 13) + t * (4 / 60) / DUR;
  function state(t) { const hh = clockH(t), jd = jdLocal(1782, 9, 13, hh), ph = G.phaseAt(t); return { year: 1782.70, day: 0.5, cam: G.path.at(t), spp: 2, phase: ph.kind, preset: 'lateral-parallax', vai: 'he-qua', hero: null, noi: 'bien', hours: hh, clock: clockLabel(jd), sun: sunPos(jd) }; }
  let song = null;
  function apply(st, t) { fleet.update(st.hours); sm.update(st.hours); TOWN.update(st.year, ctx.cam); song = LF.update(t ?? 0, sm.zones(st.hours)); }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  function overlay(t, st, T, proj) {
    T.where(t, [-1, DUR + 1], 'Bay of Gibraltar, 13 Sep 1782');
    T.ghostSrc(t, [-1, DUR + 1], TOWN.src);
    T.chrome(t, { s: st.clock.s }, 0, null, { lines: [{ s: 'Battery positions, boats: illustrative · fire from c. 17:00 (Montero; Spilsbury)', a: Math.max(0, Math.min(1, (t + 0.3) / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.card(t, [0.8, DUR], 'Flagship and her second on fire', 'Drinkwater 1785: smoke from the flagship "appeared to prevail"', proj(V([FIN[PAST].at[0], 20, FIN[PAST].at[1]])));
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt });
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: { pastora: [FIN[PAST].at[0], 12, FIN[PAST].at[1]] }, namKhung: (st) => TOWN.namMax(st.year),
    smokeZones: (st) => sm.zones(st.hours), meta: Object.assign({ alt_vinh: ALT_MAX.vinh, ghost_src: TOWN.src, fleet: 10, chay: [PAST, SEC], town: TOWN.stat(), doPx: { tau: FIN.map((s) => [s.at[0], 0, s.at[1], s.kind]) } }, META), song: () => song };
}

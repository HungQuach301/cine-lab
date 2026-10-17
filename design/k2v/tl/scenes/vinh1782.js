// ĐOẠN THỬ V5b-2b-T · CẢNH (a) — CÚ LIÊN HOÀN #2 của T3 "vây hãm" (TIEN-KY-VAY-HAM §4.2 shot 2m, [lien-hoan-2-vinh-1782], vai "bước ngoặt", MỐC ĐINH 13/9/1782):
//  bay thấp ≈ 100 m trên mặt vịnh từ phía Algeciras → speed ramp → ORBIT King's Bastion (footprint OSM 952588383 + 256821558, dựng như công sự đá — KHÔNG như nhà)
//  với BỘ ĐẾM NGÀY/GIỜ DỪNG "13 Sep 1782 · 09:45" (năm dừng 1,8 s trong orbit) → crane up → rise-and-reveal hàng 10 PIN NỔI + khói (M7), mặt trời đúng giờ (M6, thiên văn 36,14° B).
// Dữ kiện trên hình (claims-vay-ham.json S066, S067, S075; bảng shot 2m): 09:30 pin nổi vào vị trí → 09:45 đồn trú khai hoả → 10:25 toàn tuyến Pháp–TBN (ba nguồn).
// MINH HOẠ, ghi trên hình: vị trí neo từng pin nổi (kéo theo hàng ~820 m ngoài Line Wall — plan Drinkwater 1786 chưa nắn) và hình thân pin nổi (theo bản khắc).
// Phố 1782: KHÔNG có ghost 1782 (việc của phiên SH, nhánh sh-ghost chưa có) → dùng lớp tái dựng sẵn của gói cảnh, mốc nguồn gần nhất: "LoC print, 1705",
//  nhãn nguồn ghost (role ghost_src) hiện liền suốt cảnh. Tàu buồm minh hoạ 1704 của gói (ships.js makeShips) TẮT; không người (luật hình chiến tranh §6.2).
import { lienHoan, grammar, grammarLog, ALT_MAX } from '../campath.js';
import { ease, track } from '../core.js';
import { footprints, smoke } from '../layers.js';
import { makeFleet, lineFormation } from '../ships.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export const META = { cau: 'lien-hoan', vai: 'buoc-ngoat', moc_dinh: '1782-09-13T09:45 LMT', noi: [[0, 5.6, 'bien'], [5.6, 12.0, 'thanh_pho'], [12.0, 18.0, 'vung']] };
export async function build(ctx) {
  const { THREE, terr, scene } = ctx, fps = 24, hAt = terr.hAt;
  ctx.ships.group.visible = false;   // tàu minh hoạ 1704–1860 của gói không thuộc cảnh này
  // King's Bastion (xây 1773): footprint OSM; công sự đá cao 9 m (ước — plan 1782 chưa nắn; ghi báo cáo). hid 3 → hero_pct
  const KB = await footprints([{ file: 'kings_bastion', fort: true, h: 9, hid: 3, years: [1773, 2100] }], ctx); scene.add(KB.group);
  const KBC = [-620, 0, -1274];   // tâm (E, cao, N)
  // 10 pin nổi: hàng dọc ~ trục 172° quanh (−1430, −1330), cách 140 m; vào vị trí từ tây-bắc 08:40 → 09:30 (đường đi theo giờ, M3)
  const FIN = lineFormation({ n: 10, center: [-1430, -1330], axis: 172, spacing: 140, kind: 'battery' });
  const H = (h, m) => h + m / 60;
  const fleet = makeFleet(ctx.U, FIN.map((s, i) => Object.assign(s, { path: [[H(8, 40) - i * 0.02, s.at[0] - 900, s.at[1] + 1300], [H(9, 30), s.at[0], s.at[1]]], heading: 172 })));
  scene.add(fleet.group); ctx.maskify && fleet.group.traverse((o) => { if (o.isMesh) ctx.maskify(o.material, ctx.U, 1); });
  // khói M7: King's Bastion + khẩu đội Line Wall từ 09:45; pin nổi lần lượt 09:50 → 10:25 (toàn tuyến) — KHÔNG người trong vùng khói; lửa đỏ nhỏ, chỉ ở miệng pháo
  const sm = smoke([{ at: [-655, 14, -1274], t: [H(9, 45), 24], n: 16, size: 46, rise: 70, drift: [-3, 1], period: 0.09, seed: 11, alpha: 0.8 },
    { at: [-640, 14, -1150], t: [H(9, 46), 24], n: 10, size: 36, rise: 55, drift: [-3, 1], period: 0.1, seed: 12, alpha: 0.7 },
    { at: [-630, 14, -1400], t: [H(9, 47), 24], n: 10, size: 36, rise: 55, drift: [-3, 1], period: 0.1, seed: 13, alpha: 0.7 },
    ...FIN.map((s, i) => ({ at: [s.at[0] + 18, 10, s.at[1]], t: [H(9, 50) + i * (35 / 60) / 9, 24], n: 12, size: 42, rise: 60, drift: [4, 1], period: 0.1, seed: 40 + i, alpha: 0.75, fire: i % 3 === 0 ? 0.6 : 0 }))], ctx);
  scene.add(sm.group); ctx.maskHide = [sm.group];
  // giờ theo thời gian cảnh (giờ địa phương LMT), dừng 09:45 trong orbit
  const PIN = [7.4, 9.2];
  const clockH = track([[0, H(9, 5)], [4.0, H(9, 30)], [5.6, H(9, 40)], [PIN[0], H(9, 45)], [PIN[1], H(9, 45)], [10.6, H(9, 58)], [12.0, H(10, 5)], [17.0, H(10, 25)], [18.0, H(10, 27)]]);
  const ROUTE = [[-1700, -1236], [-1250, -1246], [-900, -1262], [-735, -1274]];   // mặt vịnh, hướng đông về King's Bastion (vịnh: ALT_MAX.vinh)
  const lh = lienHoan({ vai: 'buoc-ngoat', hAt: (e, n) => Math.max(0, hAt(e, n)),
    route: { line: ROUTE, type: 'vinh', nguon: 'mặt vịnh Gibraltar, đường thẳng Algeciras → King\'s Bastion (vinh1782.js)' },
    fly: { s0: 0, s1: 430, t: [0.0, 4.0], h: [100, 96], target: KBC, r: 600, pitch: 0.13, fov: 30 },
    ramp: { t1: 5.6, k: 2.2 },
    orbit: { c: [KBC[0], 6, KBC[2]], r: 118, h: 42, look: 4, a0: 182, a1: 330, t1: 10.6, fov: 34, heroId: 'kings_bastion' },
    crane: { t1: 12.0, h: 240, fov: 34, l: [-640, 30, -1280] },
    // reveal: lên + lùi về phía đông-bắc, tâm nhìn trượt từ bastion sang giữa hàng pin nổi (phố + bastion tiền cảnh, hàng pin nổi chiếm bề ngang khung)
    reveal: { keys: [{ t: 13.7, p: [-1150, 280, -1420], l: [-700, 40, -1290], fov: 36 }, { t: 15.4, p: [-1600, 270, -1520], l: [-800, 10, -1290], fov: 37 }, { t: 17.0, p: [-1950, 260, -1580], l: [-880, -10, -1290], fov: 38 }] },   // lùi ra vịnh qua hàng pin nổi: pin nổi tiền cảnh, phố + Rock hậu cảnh (góc bản khắc nhìn từ vịnh)
    pin: PIN });
  const G = grammar([lh], [{ t: 18.0, p: [-1985, 262, -1586], l: [-886, -12, -1290], fov: 38 }]), path = G.path;
  const D0 = [1782, 9, 13];
  const jdAt = (h) => jdLocal(D0[0], D0[1], D0[2], h);
  const pinK = (t) => ease((t - (PIN[0] - 0.1)) / 0.35) * ease((PIN[1] + 0.3 - t) / 0.4);
  const noiAt = (t) => (META.noi.find(([a, b]) => t >= a && t < b) || META.noi[META.noi.length - 1])[2];
  function state(t) {
    const c = path.at(t), ph = G.phaseAt(t), hh = clockH(t), sp = sunPos(jdAt(hh)), pk = pinK(t);
    return { year: 1782.70, cam: c, spp: G.sppAt(t), dim: pk * 0.35, pin: pk, pinZoom: ease((t - PIN[0]) / 0.3) * ease((PIN[1] - t) / 0.35), phase: ph.kind, preset: ph.shot ? ph.shot.preset : null, vai: ph.shot ? ph.shot.vai : null,
      hero: ['orbit', 'pin', 'crane'].includes(ph.kind) ? 'kings_bastion' : null, hours: hh, clock: clockLabel(jdAt(hh)), sun: sp, noi: noiAt(t) };
  }
  function apply(st) { fleet.update(st.hours); sm.update(st.hours); KB.update(st.year, ctx.cam); }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  const mid = FIN[4].at, GHOST = 'Town: reconstructed from LoC print, 1705 · no 1782 plan digitised yet';
  function overlay(t, st, T, proj) {
    T.chrome(t, { s: st.clock.s }, st.pinZoom, null, null, null);
    T.where(t, [0, 5.75], 'Bay of Gibraltar'); T.where(t, [5.75, 12.15], "King's Bastion, Gibraltar"); T.where(t, [12.15, 18.5], 'Bay of Gibraltar');
    T.ghostSrc(t, [-1, 18.5], GHOST);
    T.card(t, [PIN[0] - 0.2, 10.9], "09:45 · The garrison's guns open fire", 'Times: Drinkwater 1786 and two other accounts', proj(V([KBC[0], 16, KBC[2]])));
    T.card(t, [13.0, 18.5], '10 floating batteries · positions illustrative', 'Line: Drinkwater 1786 plan · hulls drawn from engravings', proj(V([mid[0], 18, mid[1]])));
  }
  const N = Math.round(18.0 * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt: (e, n) => Math.max(0, hAt(e, n)), line: ROUTE, focus: { kings_bastion: KBC } });
  return { N, fps, state, apply, overlay, path, grammarLog: glog, camLog: glog, heroIds: { kings_bastion: 3 },
    anchors: { kings_bastion: [KBC[0], 12, KBC[2]], battery_mid: [mid[0], 12, mid[1]] },
    namKhung: (st) => Object.assign({ ghost_1705: 1705 }, KB.namMax(st.year)), smokeZones: (st) => sm.zones(st.hours),
    meta: Object.assign({ alt_vinh: ALT_MAX.vinh, ghost_src: GHOST, fleet: FIN.length }, META) };
}

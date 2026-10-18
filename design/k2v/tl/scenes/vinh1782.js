// ĐOẠN THỬ V5b-2b-T · CẢNH (a) — CÚ LIÊN HOÀN #2 của T3 "vây hãm" (TIEN-KY-VAY-HAM §4.2 shot 2m, [lien-hoan-2-vinh-1782], vai "bước ngoặt", MỐC ĐINH 13/9/1782):
//  bay thấp ≈ 100 m trên mặt vịnh từ phía Algeciras → speed ramp → ORBIT King's Bastion (footprint OSM 952588383 + 256821558, dựng như công sự đá — KHÔNG như nhà)
//  với BỘ ĐẾM NGÀY/GIỜ DỪNG "13 Sep 1782 · 09:45" (năm dừng 1,8 s trong orbit) → crane up → rise-and-reveal hàng 10 PIN NỔI + khói (M7), mặt trời đúng giờ (M6, thiên văn 36,14° B).
// Dữ kiện trên hình (claims-vay-ham.json S066, S067, S075; bảng shot 2m): 09:30 pin nổi vào vị trí → 09:45 đồn trú khai hoả → 10:25 toàn tuyến Pháp–TBN (ba nguồn).
// MINH HOẠ, ghi trên hình: vị trí neo từng pin nổi (kéo theo hàng ~820 m ngoài Line Wall — plan Drinkwater 1786 chưa nắn) và hình thân pin nổi (theo bản khắc).
// Phố 1782 (lệnh AE 17/10): ghost 1782 của phiên SH (Drinkwater 1786 plan, RMS phố 21 m) qua layers.town1782 — lớp tái dựng 1705 của gói ẩn;
//  nhãn nguồn ghost (role ghost_src, SH-BAO-CAO §5) hiện liền suốt cảnh. Tàu buồm minh hoạ 1704 của gói (ships.js makeShips) TẮT; không người (luật hình chiến tranh §6.2).
import { lienHoan, grammar, grammarLog, ALT_MAX } from '../campath.js';
import { ease, track } from '../core.js';
import { footprints, smoke, town1782, units } from '../layers.js';
import { battery, flags } from '../props.js';
import { makeFleet, lineFormation } from '../ships.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';
import { life, chimneysFrom } from '../life.js';

export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };   // V5b-2d (C2-9): vách bắc sắc hơn + đỉnh 412 m theo ảnh PD LoC 2025710362 (terrain.js)
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };   // trời Địa Trung Hải sáng tháng 9: chân trời xanh hơn (S 0,33 → 0,46)   // V5b-2c (I5): bóng đổ bớt xám-lam, ánh dội đất ấm (0,74: không cháy sáng)
export const GRADE = { vib: 0.62 };   // V5b-2c (I5): vibrance 0,35 → 0,62 (vữa/đá nhạt lên màu; màu đã đậm gần như giữ)
export const META = { cau: 'lien-hoan', vai: 'buoc-ngoat', moc_dinh: '1782-09-13T09:45 LMT', noi: [[0, 5.9, 'bien'], [5.9, 12.0, 'thanh_pho'], [12.0, 18.0, 'vung']] };
export async function build(ctx) {
  const { THREE, terr, scene } = ctx, fps = 24, hAt = terr.hAt;
  ctx.ships.group.visible = false;   // tàu minh hoạ 1704–1860 của gói không thuộc cảnh này
  // King's Bastion (xây 1773): footprint OSM; công sự đá cao 9 m (ước — plan 1782 chưa nắn; ghi báo cáo). hid 3 → hero_pct
  // V5b-2c: King's Bastion = bao lồi tường OSM historic=citywalls quanh bastion (layers.town1782, hid 3), dựng bằng M5 (fort.js) — thay footprint toà Leisure Centre
  // V5b-2d (C2-2): khung gần (orbit AGL 27 m, bay 56 m) → tiền cảnh chỉ khối có nguồn: bỏ lấp ước tính trong 150 m quanh vết máy (tuyến bay + vòng orbit r 84 quanh bastion)
  const NEAR = [[-1250, -380], [-980, -620], [-850, -900], [-735, -1274]].concat([...Array(16).keys()].map((k) => { const a = (182 + (330 - 182) * k / 15) * Math.PI / 180; return [-620 + Math.sin(a) * 84, -1274 + Math.cos(a) * 84]; }));
  const TOWN = await town1782(ctx, { kbOpt: { hid: 3, h: 9, soot: 0.55, face: [-1, 0], faceMin: -0.25 }, near: { track: NEAR, r: 150 } }), KB = { update() {}, namMax: () => ({ kings_bastion: 1773 }) };
  // V5b-2d (C2-1 mục 2): SÀN PHÁO King's Bastion — đồ sàn pháo (đạn, thùng thuốc súng, lán chắn mảnh, lò nung đạn), PHÁO THỦ 4 người/khẩu (A-lite, không cận mặt),
  //  cờ Union 1707 (cột cờ MINH HOẠ — cột cờ đồn trú theo Drinkwater ở Grand Battery), KHÓI ĐẦU NÒNG từ 09:45 (M6: "that instant our firing commenced").
  //  Gió sáng 13/9: "a gentle breeze from the north-west" (Drinkwater 1785, p. 295) → khói trôi về nam dọc mặt luỹ, ra ngoài; vùng khói CHÍNH XÁC (zone 'path'), pháo thủ ngoài vùng + 15 m.
  const KBF = TOWN.KB.floors[0], KBG = TOWN.KB.guns, BAT = battery(KBG, KBF.ring, KBF.y, ctx, { seed: 1773, sheds: 3, kegs: 4 }); scene.add(BAT.group);
  const out = (g) => [Math.cos(g.rot), Math.sin(g.rot)], west = KBG.filter((g) => out(g)[0] < -0.35);
  const MZ = west.filter((g, i) => i % 2 === 0).map((g, i) => { const u = out(g); return { at: [g.muzzle[0] + u[0] * 26, 11, g.muzzle[1] + u[1] * 26], t: [9.7495 - 0.0004 * i, 24], n: 9, size: 8, rise: 14, drift: [u[0] * 1.2 + 0.2, u[1] * 1.2 - 0.6], period: 0.08, seed: 600 + i, alpha: 1.0, zone: 'path' }; });
  // + đội dự bị/khuân đạn giữa sàn (2 khối nhỏ, minh hoạ — Drinkwater: thuỷ thủ hải quân phụ pháo binh ngày 13/9)
  const KC = [KBF.ring.reduce((a, p) => a + p[0], 0) / KBF.ring.length, KBF.ring.reduce((a, p) => a + p[1], 0) / KBF.ring.length];
  const CREW = units(BAT.crews.map((c, i) => ({ at: c.at, heading: c.heading, rows: 2, cols: 2, sx: 2.6, sz: 1.6, near: 300, y: KBF.y, color: i % 4 === 3 ? '#a8392c' : '#2f3d5c', day: [0, 99], seed: 900 + i }))
    .concat([{ at: [KC[0] + 6, KC[1] - 10], heading: 270, rows: 3, cols: 8, y: KBF.y, color: '#a8392c', day: [0, 99], seed: 951 }, { at: [KC[0] + 10, KC[1] + 14], heading: 250, rows: 2, cols: 7, y: KBF.y, color: '#3b4a66', day: [0, 99], seed: 952 }]), ctx); scene.add(CREW.group);   // áo lam pháo binh Hoàng gia + vài lính bộ binh phụ (minh hoạ)
  const FLG = flags([{ at: [KBF.ring.reduce((m, p) => (p[0] > m[0] ? p : m), KBF.ring[0])[0] - 6, -1276], base: KBF.y, pole: 14, w: 4.6, kind: 'union1707', toward: 150 }], ctx); scene.add(FLG.group);
  const KBC = [-620, 0, -1274];   // tâm (E, cao, N)
  // 10 pin nổi: hàng dọc ~ trục 172° quanh (−1430, −1330), cách 140 m; vào vị trí từ tây-bắc 08:40 → 09:30 (đường đi theo giờ, M3)
  const FIN = lineFormation({ n: 10, center: [-1430, -1330], axis: 172, spacing: 140, kind: 'battery' });
  const H = (h, m) => h + m / 60;
  // V5b-2c: tàu neo cạnh Old Mole (đồn trú có tàu trong cảng — số lượng/vị trí MINH HOẠ, ghi dòng phương pháp) — nội dung trung cảnh "cảng/bờ"
  FIN.push(...[[-700, -660, 200], [-770, -780, 185], [-655, -545, 210], [-820, -905, 195]].map(([e, n, hd], i) => ({ kind: i % 2 ? 'sail' : 'line', at: [e, n], heading: hd, moored: true })));
  const fleet = makeFleet(ctx.U, FIN.map((s, i) => s.moored ? s : Object.assign(s, { path: [[H(8, 40) - i * 0.02, s.at[0] - 900, s.at[1] + 1300], [H(9, 30), s.at[0], s.at[1]]], heading: 172 })));
  scene.add(fleet.group); ctx.maskify && fleet.group.traverse((o) => { if (o.isMesh) ctx.maskify(o.material, ctx.U, 1); });
  // khói M7: King's Bastion + khẩu đội Line Wall từ 09:45; pin nổi lần lượt 09:50 → 10:25 (toàn tuyến) — KHÔNG người trong vùng khói; lửa đỏ nhỏ, chỉ ở miệng pháo
  const sm = smoke([...MZ,
    { at: [-668, 14, -1150], t: [H(9, 46), 24], n: 10, size: 24, rise: 55, drift: [-1.2, -2.2], period: 0.1, seed: 12, alpha: 0.7, zone: 'path' },   // V5b-2d: khẩu đội Line Wall, khói trôi theo gió NW (Drinkwater), vùng chính xác
    { at: [-660, 14, -1400], t: [H(9, 47), 24], n: 10, size: 24, rise: 55, drift: [-1.2, -2.2], period: 0.1, seed: 13, alpha: 0.7, zone: 'path' },
    ...FIN.filter((s) => s.kind === 'battery').map((s, i) => ({ at: [s.at[0] + 18, 10, s.at[1]], t: [H(9, 50) + i * (35 / 60) / 9, 24], n: 20, size: 76, rise: 80, drift: [4, 1], period: 0.1, seed: 40 + i, alpha: 0.9, fire: i % 3 === 0 ? 0.6 : 0 }))], ctx);   // V5b-2c: khói dày hơn (chấm mù P4 'khói nhạt')
  // LỚP SỐNG (F3): thuyền pháo/xuồng của đồn trú chạy dọc Line Wall (minh hoạ), hải âu quanh King's Bastion, khói bếp mái phố
  const recs1782 = TOWN.FP.list.flatMap((l) => (l.kind === 'ghost' ? l.recs : []));
  const LF = life({ seed: 913, birds: [{ c: [-700, -1250], r: 140, h: 45, n: 14 }, { c: [-1150, -1500], r: 220, h: 70, n: 10 }],
    boats: [{ pts: [[-720, -880], [-760, -1150], [-745, -1450], [-700, -1700]], len: 13, speed: 4.2, s0: 0.15 }, { pts: [[-690, -1650], [-735, -1350], [-760, -1050], [-720, -800]], len: 11, speed: 3.6, s0: 0.4 },
      { pts: [[-880, -950], [-1000, -1180], [-930, -1420]], len: 9, speed: 2.8, s0: 0.7, sail: true }, { pts: [[-650, -620], [-760, -700], [-860, -640]], len: 8, speed: 2.2, s0: 0.3 }],
    chimney: { at: chimneysFrom(recs1782, 16), drift: [-1.4, 0.4] } }, ctx);
  scene.add(LF.group);
  scene.add(sm.group); ctx.maskHide = [sm.group].concat(LF.smokeGroup ? [LF.smokeGroup] : []);
  // giờ theo thời gian cảnh (giờ địa phương LMT), dừng 09:45 trong orbit
  const PIN = [7.4, 9.2];
  const clockH = track([[0, H(9, 5)], [4.0, H(9, 30)], [5.9, H(9, 40)], [PIN[0], H(9, 45)], [PIN[1], H(9, 45)], [10.6, H(9, 58)], [12.0, H(10, 5)], [17.0, H(10, 25)], [18.0, H(10, 27)]]);
  const ROUTE = [[-1250, -380], [-980, -620], [-850, -900], [-735, -1274]];   // V5b-2d (C2-1 mục 5, loại 'cảng'): bay cao hơn (≈ 110 m) qua mặt vịnh trước Old Mole — tàu neo tiền cảnh, Old Mole + phố + Rock hậu cảnh; rồi hạ về King's Bastion
  const lh = lienHoan({ vai: 'buoc-ngoat', hAt: (e, n) => Math.max(0, hAt(e, n)),
    route: { line: ROUTE, type: 'vinh', nguon: 'mặt vịnh Gibraltar, đường thẳng Algeciras → King\'s Bastion (vinh1782.js)' },
    fly: { s0: 0, s1: 480, t: [0.0, 4.0], h: [122, 100], target: [-600, 0, -880], r: 600, pitch: 0.22, fov: 36 },   // nhìn xuống ≈ 12°: tàu neo + Old Mole + phố   // V5b-2d: đích nhìn dời về phố (Old Mole → Orange's Bastion): khối phố chiếm nhiều hơn, tàu neo vẫn trong khung   // V5b-2c (I3): thấp hơn (62 → 56 m) — mặt nước nén lại, bờ phố + Line Wall + tàu neo chiếm giữa khung
    ramp: { t1: 5.9, k: 2.2 },   // V5b-2d: ramp dài hơn 0,3 s (tuyến bay mới xa bastion hơn) — orbit 5,9 → 10,6 s (4,7 s, trong 4–6 s)
    orbit: { c: [KBC[0], 6, KBC[2]], r: 84, h: 27, look: 4, a0: 182, a1: 330, t1: 10.6, fov: 36, heroId: 'kings_bastion' },   // V5b-2c: orbit sát + thấp hơn — mặt tường, lỗ châu mai, pháo đầy khung
    crane: { t1: 12.0, h: 240, fov: 34, l: [-640, 30, -1280] },
    // reveal: lên + lùi về phía đông-bắc, tâm nhìn trượt từ bastion sang giữa hàng pin nổi (phố + bastion tiền cảnh, hàng pin nổi chiếm bề ngang khung)
    reveal: { keys: [{ t: 13.7, p: [-1050, 190, -1820], l: [-820, 40, -1330], fov: 36 }, { t: 15.4, p: [-1380, 105, -2120], l: [-1060, 42, -1340], fov: 36 }, { t: 17.0, p: [-1540, 34, -2245], l: [-1140, 40, -1340], fov: 36 }] },   // V5b-2c (I3): lùi thấp về tây-nam hàng pin nổi (gần nhất ≈ 320 m), chân trời thấp: hàng tàu chéo khung từ trái-giữa, khói, King's Bastion + phố + Rock bên phải
    pin: PIN });
  const G = grammar([lh], [{ t: 18.0, p: [-1552, 33, -2252], l: [-1146, 40, -1338], fov: 36 }]), path = G.path;
  const D0 = [1782, 9, 13];
  const jdAt = (h) => jdLocal(D0[0], D0[1], D0[2], h);
  const pinK = (t) => ease((t - (PIN[0] - 0.1)) / 0.35) * ease((PIN[1] + 0.3 - t) / 0.4);
  const noiAt = (t) => (META.noi.find(([a, b]) => t >= a && t < b) || META.noi[META.noi.length - 1])[2];
  function state(t) {
    const c = path.at(t), ph = G.phaseAt(t), hh = clockH(t), sp = sunPos(jdAt(hh)), pk = pinK(t);
    return { year: 1782.70, cam: c, spp: G.sppAt(t), dim: pk * 0.35, pin: pk, pinZoom: ease((t - PIN[0]) / 0.3) * ease((PIN[1] - t) / 0.35), phase: ph.kind, preset: ph.shot ? ph.shot.preset : null, vai: ph.shot ? ph.shot.vai : null,
      hero: ['orbit', 'pin', 'crane'].includes(ph.kind) ? 'kings_bastion' : null, hours: hh, clock: clockLabel(jdAt(hh)), sun: sp, noi: noiAt(t) };
  }
  let song = null;
  let crew = null;
  function apply(st, t) { fleet.update(st.hours); sm.update(st.hours); KB.update(st.year, ctx.cam); TOWN.update(st.year, ctx.cam); const z = sm.zones(st.hours); song = LF.update(t ?? 0, z); crew = CREW.update(0.5, z); FLG.update(t ?? 0); }
  const V = (p) => new THREE.Vector3(p[0], p[1], -p[2]);
  const mid = FIN[4].at, GHOST = TOWN.src;
  function overlay(t, st, T, proj) {
    T.where(t, [0, 6.05], 'Bay of Gibraltar'); T.where(t, [6.05, 12.15], "King's Bastion, Gibraltar"); T.where(t, [12.15, 18.5], 'Bay of Gibraltar');
    T.ghostSrc(t, [-1, 18.5], GHOST);
    T.chrome(t, { s: st.clock.s }, st.pinZoom, null, { lines: [{ s: 'Map data: OpenStreetMap (ODbL)', a: Math.max(0, Math.min(1, (t + 0.3) / 0.35, (4.6 - t) / 0.35)) }, { s: 'Ships at anchor, boats: illustrative', a: Math.max(0, Math.min(1, (t + 0.3) / 0.35, (5.4 - t) / 0.35)) },
      { s: 'Gun crews, stores, flag: illustrative', a: Math.max(0, Math.min(1, (t - 5.4) / 0.35, (11.0 - t) / 0.35)) }] }, null);
    T.card(t, [PIN[0] - 0.2, 10.9], "09:45 · The garrison's guns open fire", 'Times: Drinkwater 1786 and two other accounts', proj(V([KBC[0], 16, KBC[2]])));
    T.card(t, [14.4, 18.5], '10 floating batteries · positions illustrative', 'Line: Drinkwater 1786 plan · hulls drawn from engravings', proj(V([mid[0], 18, mid[1]])));
  }
  const N = Math.round(18.0 * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt: (e, n) => Math.max(0, hAt(e, n)), line: ROUTE, focus: { kings_bastion: KBC } });
  return { N, fps, state, apply, overlay, path, grammarLog: glog, camLog: glog, heroIds: { kings_bastion: 3 },
    anchors: { kings_bastion: [KBC[0], 12, KBC[2]], battery_mid: [mid[0], 12, mid[1]] },
    namKhung: (st) => Object.assign({}, TOWN.namMax(st.year), KB.namMax(st.year)), smokeZones: (st) => sm.zones(st.hours),
    meta: Object.assign({ alt_vinh: ALT_MAX.vinh, ghost_src: GHOST, fleet: FIN.filter((s) => s.kind === 'battery').length, kb_san: BAT.stat, kb_phao: KBG.length, khoi_dau_nong: MZ.length, town: TOWN.stat(), doPx: { khoi: [3, 2.5], near: 300, quan: BAT.crews.map((c) => [c.at[0], KBF.y, c.at[1]]), tau: FIN.map((s) => [s.at[0], 0, s.at[1], s.kind]) } }, META), song: () => song, troops: () => crew };
}

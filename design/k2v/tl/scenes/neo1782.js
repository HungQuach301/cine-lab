// V5b-2c · CẢNH NEO 1782 (F1/F3 chủ dự án 17/10): KHUNG CỐ ĐỊNH của phiên PT (Grand Parade, mép Main Street, 4,6 m, 281°, 32 mm — campath.NEO_PT),
//  giữ 8 s; thời gian trôi bằng BỘ ĐẾM NĂM là chữ chính (F2: năm 1782 cố định trong cảnh, chuyển mốc bằng hoà ở dựng) + chu kỳ NGÀY → CHIỀU (07:30 → 17:40 LMT,
//  mặt trời thiên văn 13/9/1782, nắng thấp ngả cam — page.applySun dayCycle). Lớp sống ≥ 3 loại: đội hình đồn trú tập trên Grand Parade (dịch theo giờ), người đi qua
//  quảng trường, khói bếp, hải âu, xuồng ngoài Line Wall. Phố = ghost SH 1782 + lấp ước tính (tông lệch nhẹ); Line Wall theo OSM (M5).
//  Khác PT: dựng three.js/llvmpipe (không Cycles) → dùng được ở dây chuyền tl, cùng tư thế máy để cắt/hoà với khung PT.
import { neo, NEO_PT, grammar, grammarLog } from '../campath.js';
import { town1782, units } from '../layers.js';
import { life, chimneysFrom, freePath } from '../life.js';
import { makeFleet } from '../ships.js';
import { jdLocal, sunPos } from '../sun.js';

export const TERRAIN = { cliff: true };
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };
export const GRADE = { vib: 0.62 };
export const META = { cau: 'neo', vai: 'co-che', noi: [[0, 99, 'thanh_pho']], nam: 1782, neo: NEO_PT };
export async function build(ctx) {
  const { terr, scene } = ctx, fps = 24, DUR = 8.0, hAt = (e, n) => Math.max(0, terr.hAt(e, n)), H0 = 7.5, H1 = 17 + 40 / 60;   // 18:20 (bản đầu) làm nền tối dưới trời còn xanh — dừng 17:40, nắng thấp vẫn đọc được
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx), recs = TOWN.FP.list.flatMap((l) => l.recs), P = NEO_PT;
  // đội hình tập: 2 khối hành tiến chậm qua quảng trường theo giờ (minh hoạ); người đi chéo quảng trường + dọc mép phố
  const GP = [-505, -1165];
  const TR = units([0, 1].map((k) => ({ at: [GP[0] - 10 + k * 22, GP[1] - 6], heading: 270, rows: 4, cols: 12, side: 'gb', day: [0, 99], seed: 31 + k, move: [[0, 0, 0], [4, -26, 4], [8, -6, 16]] })), ctx); scene.add(TR.group);
  const cross = [[GP[0] + 40, GP[1] - 40], [GP[0] - 10, GP[1] + 5], [GP[0] - 60, GP[1] + 30]], edge = freePath([[P.E + 5, P.N - 60], [P.E + 2, P.N + 80]], recs, 20);
  const LF = life({ seed: 1781, walkers: [{ pts: cross, n: 26, width: 30, colors: ['#e7e0cf', '#5e4a38', '#3d4a5a', '#b03a2e'] }, { pts: edge.length > 1 ? edge : cross, n: 14, width: 2, colors: ['#b03a2e', '#e7e0cf', '#6b5a48'] }],
    birds: [{ c: [GP[0] - 120, GP[1] + 20], r: 90, h: 30, n: 10 }], boats: [{ pts: [[-650, -900], [-680, -1150], [-660, -1400]], len: 11, speed: 3.0, s0: 0.3 }, { pts: [[-700, -1350], [-720, -1100], [-690, -880]], len: 9, speed: 2.4, s0: 0.7, sail: true }],
    chimney: { at: chimneysFrom(recs.filter((r) => r[1] > 0), 18), drift: [-1.2, 0.4] } }, ctx);
  scene.add(LF.group); ctx.maskHide = LF.smokeGroup ? [LF.smokeGroup] : [];
  const fleet = makeFleet(ctx.U, [[-900, -1000, 190], [-980, -1200, 175], [-1100, -1080, 200]].map(([e, n, hd], i) => ({ kind: i ? 'sail' : 'line', at: [e, n], heading: hd }))); scene.add(fleet.group);
  fleet.group.traverse((o) => { if (o.isMesh) ctx.maskify(o.material, ctx.U, 1); });
  const sh = neo({ vai: 'co-che', t0: 0, t1: DUR, hAt }), G = grammar([sh]);
  const hoursAt = (t) => H0 + (H1 - H0) * t / DUR;
  function state(t) { const hh = hoursAt(t), sp = sunPos(jdLocal(1782, 9, 13, hh)); return { year: 1782.7, day: t, cam: G.path.at(t), spp: 2, phase: 'neo', preset: 'neo', vai: 'co-che', hero: null, noi: 'thanh_pho', hours: hh, sun: sp, dayCycle: true }; }
  let troops = null, song = null;
  function apply(st, t) { TOWN.update(st.year, ctx.cam); fleet.update(st.hours); troops = TR.update(st.day, []); song = LF.update(t ?? 0, []); }
  function overlay(t, st, T) {
    T.chrome(t, 1782, 0, null, { lines: [{ s: 'Fixed view · one day, compressed', a: Math.max(0, Math.min(1, (t - 0.2) / 0.35, (DUR + 0.5 - t) / 0.35)) }, { s: TOWN.INFILL_SRC + ' · people: illustrative', a: Math.max(0, Math.min(1, (t - 0.2) / 0.35, (DUR + 0.5 - t) / 0.35)) }] }, null);
    T.where(t, [-1, DUR + 1], 'Grand Parade, Gibraltar');
    T.ghostSrc(t, [-1, DUR + 1], TOWN.src);
  }
  const N = Math.round(DUR * fps);
  const glog = () => grammarLog(G, N, fps, () => 1782.7, { hAt });
  return { N, fps, state, apply, overlay, path: G.path, grammarLog: glog, camLog: glog, anchors: { grand_parade: [GP[0], 6, GP[1]] }, namKhung: (st) => TOWN.namMax(st.year),
    meta: Object.assign({ quan: TR.stat() }, META), troops: () => troops, song: () => song };
}

// V5b-2b · CẢNH KIỂM MÁY (không phải phim): bật mọi lớp mới của T3 trên trình dựng thật để test (scripts/k2tl/tests/test_t3.js) và tờ khung trong báo cáo.
//  M4 chiến tuyến mọc theo ngày trên eo đất (tuyến MINH HOẠ ngang eo đất ở N ≈ +700 m — Línea de Contravalación thật chờ Faden 1783 đã nắn) · M1 mũi tên
//  · M12 bản đồ pha (raster thay thế: ảnh LoC đã cắt, chỉ để kiểm cơ chế phủ địa hình + crossfade) · M9 lớp ghost từ footprint OSM (chỉ kiểm bộ nạp — KHÔNG phải ghost 1782)
//  · M6 bộ đếm hai lịch 1704 + mặt trời theo giờ · M7 khói. Tất định.
import { grammar, pushIn } from '../campath.js';
import { footprints, phaseMaps, frontLines, arrows, smoke, units } from '../layers.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export async function build(ctx) {
  const { scene, terr } = ctx, fps = 24, DUR = 4;
  ctx.ships.group.visible = false;
  const opt = ctx.opt || {};
  const FP = opt.ghostLayer ? await footprints([{ file: opt.ghostLayer, years: [1700, 2100] }], ctx) : null; if (FP) scene.add(FP.group);
  const PM = await phaseMaps([{ url: '/cache/loc/ng_crop.jpg', box: [-900, 300, 300, 1100], years: [0, 1.5], fade: 1, opacity: 0.8, src: 'test raster' }, { url: '/cache/loc/ng_crop.jpg', box: [-900, 300, 300, 1100], years: [2.5, 9], fade: 1, opacity: 0.4, src: 'test raster 2' }], ctx); scene.add(PM.group);
  const FL = frontLines([{ pts: [[-1100, 700], [-600, 690], [-100, 705], [400, 700]], side: 'es', grow: [0.2, 2.5], w: 30 }, { pts: [[-800, 120], [-300, 110], [200, 125]], side: 'gb', grow: [1.0, 3.0], w: 22 }], ctx); scene.add(FL.group);
  const AR = arrows([{ pts: [[-300, 1400], [-250, 1050], [-200, 760]], side: 'es', grow: [0.5, 2.5], w: 34 }, { pts: [[300, -300], [200, -700], [100, -1000]], side: 'civ', grow: [1.5, 3.5], w: 26 }], ctx); scene.add(AR.group);
  // M2: 3 khối quân dọc tuyến thử, mọc theo uDay (= tv) 0,5 → 1,0; khối giữa cố ý đặt TRONG vùng khói (−600, 690) → phải bị ẩn; khối thứ 3 dịch 60 m về đông theo ngày
  const TR = units([{ at: [-900, 720], heading: 90, rows: 3, cols: 20, side: 'es', day: [0.5, 9] }, { at: [-600, 700], heading: 90, rows: 3, cols: 20, side: 'es', day: [0.5, 9] },
    { at: [-300, 720], heading: 90, rows: 3, cols: 20, side: 'gb', day: [1.0, 9], move: [[1.0, 0, 0], [3.5, 60, 0]] }], ctx); scene.add(TR.group);
  const SM = smoke([{ at: [-600, 20, 690], t: [1.0, 9], n: 12, size: 40, period: 0.6, seed: 3, fire: 0.5 }], ctx); scene.add(SM.group); ctx.maskHide = [SM.group];
  const sh = pushIn({ vai: 'co-che', from: [-1500, 900, -800], to: [-1300, 700, -500], look: [-300, 0, 600], t0: 0, t1: DUR, hold: 1.0, fov: 46 });
  const G = grammar([sh]), H0 = 9.0;
  let troops = null;
  function state(t) { const hh = H0 + t * 0.75, jd = jdLocal(1704, 8, 4, hh); return { year: 1704.6, cam: G.path.at(t), spp: G.sppAt(t), phase: G.phaseAt(t).kind, hours: hh, clock: clockLabel(jd, { dual: true }), sun: sunPos(jd), noi: 'eo_dat', tv: t }; }
  function apply(st) { troops = TR.update(st.tv, SM.zones(st.tv)); PM.update(st.tv); FL.update(st.tv); AR.update(st.tv); SM.update(st.tv); if (FP) FP.update(st.year, ctx.cam); }
  function overlay(t, st, T) { T.chrome(t, { s: st.clock.s, sub: st.clock.sub }, 0, null, null, null); T.where(t, [-1, 9], 'Isthmus, Gibraltar'); if (FP) T.ghostSrc(t, [-1, 9], 'Test layer: OSM footprints shown as ghost'); }
  return { N: DUR * fps, fps, state, apply, overlay, path: G.path, camLog: () => null, anchors: {}, namKhung: (st) => (FP ? FP.namMax(st.year) : {}), smokeZones: (st) => SM.zones(st.tv), troops: () => troops, meta: { kiem: true } };
}

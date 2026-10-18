// V6 · CẢNH KIỂM (không phải phim): người low-poly (people.js) ở cự li gần/trung/xa trên Grand Parade 1782 + ánh sáng V6 — để rà hình người, chu kỳ đi, LOD.
import { grammar, pushIn } from '../campath.js';
import { town1782 } from '../layers.js';
import { makeKit, makeSet } from '../people.js';
import { jdLocal, sunPos, clockLabel } from '../sun.js';

export const V6 = { sunK: 1.15, hemiK: 0.85 };
export const TERRAIN = { cliff: { k: 1.8, capUp: 80, peak: 412 } };
export const LOOK = { hemiI: 0.74, hemiSky: '#a9c0e2', hemiGnd: '#b0845a', skyHor: [0.30, 0.52, 0.90], fogC: [0.40, 0.60, 0.90] };
export const GRADE = { vib: 0.62 };
export async function build(ctx) {
  const { scene, terr } = ctx, fps = 24, DUR = 2, o = ctx.opt || {}, hAt = (e, n) => Math.max(0.3, terr.hAt(e, n));
  ctx.ships.group.visible = false;
  const TOWN = await town1782(ctx);
  const kit = makeKit(ctx), C0 = [-510, -1165], R = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
  const sets = [], rows = [['order', 'gb_inf', 0], ['march', 'gb_inf', 1], ['civ', 'civ', 1], ['woman', 'woman', 0.6], ['sailor', 'sailor', 1], ['order', 'es_inf', 0], ['civ', 'gb_art', 0]];
  rows.forEach(([kind, uni, gait], r) => { const S = makeSet(kit, ctx, { kind, n: 12 }); for (let i = 0; i < 12; i++) S.look(i, uni, R, { gait: gait > 0 ? gait : 0, acc: r }); scene.add(S.group); sets.push({ S, r, gait }); });
  const cam = o.cam ? { p: [o.cam.p[0], hAt(o.cam.p[0], o.cam.p[2]) + o.cam.p[1], o.cam.p[2]], l: [o.cam.l[0], hAt(o.cam.l[0], o.cam.l[2]) + o.cam.l[1], o.cam.l[2]] } : { p: [C0[0] - 14, hAt(...C0) + 2.2, C0[1] - 4], l: [C0[0] + 6, hAt(...C0) + 1.0, C0[1] + 1] };
  const sh = pushIn({ vai: 'co-che', from: cam.p, to: cam.p, look: cam.l, t0: 0, t1: DUR, hold: 0, fov: o.fov || 40 });
  const G = grammar([sh]), H0 = o.hour || 10.5;
  function state(t) { const jd = jdLocal(1782, 9, 13, H0); return { year: 1782.7, cam: G.path.at(t), spp: 4, phase: 'pin', hours: H0, clock: clockLabel(jd), sun: sunPos(jd), noi: 'thanh_pho' }; }
  function apply(st, t) { TOWN.update(st.year, ctx.cam);
    for (const { S, r, gait } of sets) { S.begin(); for (let i = 0; i < 12; i++) { const e = C0[0] + i * 1.1 - 2 + (r % 2) * 0.5, n = C0[1] - 6 + r * 2.2 + (gait > 0 ? (t * 1.3) % 2 : 0); S.put(i, e, hAt(e, n), n, gait > 0 ? Math.PI / 2 : (i % 3 - 1) * 0.6); } S.end(); } }
  function overlay() {}
  return { N: DUR * fps, fps, state, apply, overlay, path: G.path, camLog: () => null, anchors: {}, namKhung: () => ({}), meta: { kit: kit.tris } };
}

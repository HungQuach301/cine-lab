// NC-CPU · CÁCH A — đọc ÁNH SÁNG NƯỚNG Cycles (design/pt/cpu/nc_bake.py) cho three.js: một ảnh RGBA8 phủ hộp [E0, N0, E1, N1] (hàng 0 = bắc):
//  R = bức xạ TRỜI tại mặt đất (trực tiếp từ vòm trời + mọi lần nảy, có che khuất bởi địa hình/nhà/tường/bụi) ÷ bức xạ trời mặt phẳng trống (0..1)
//  G = phần NẢY của nắng (chỉ gián tiếp) ÷ bức xạ nắng thẳng mặt phẳng, × 4 (0..0,25 → 0..1)
//  B = ánh LỬA (pin nổi cháy 13–14/9/1782, đèn điểm Cycles, trực tiếp + gián tiếp) ÷ đỉnh (0..1)
//  A = cao độ mặt đất ÷ 600 m (để tường biết mình cao bao nhiêu trên nền → AO hẻm phố tắt dần lên cao)
//  meta.json: { box, res_m, sun: {el, az}, fire_peak, s: giờ nướng, spp }
import { THREE, tex, loadJSON } from '../core.js';

export async function makeBake(ctx, P) {
  const dummy = new THREE.DataTexture(new Uint8Array([255, 0, 0, 0]), 1, 1); dummy.needsUpdate = true;
  const uni = { tNcBake: { value: dummy }, uNcBakeBox: { value: new THREE.Vector4(0, 0, 1, 1) }, uNcBakeOn: { value: 0 }, uNcSkyK: { value: 1.0 }, uNcBncK: { value: 0.0 },
    uNcFireK: { value: 0.0 }, uNcSunC: { value: new THREE.Color(1, 1, 1) }, uNcFireC: { value: new THREE.Color(1.0, 0.42, 0.12) } };
  // V7C: P.bakes = [{ dir, wY: [năm đầu, năm cuối], fire? }] — một shot đi qua nhiều mốc/trạng thái phố (vd. 2026 → 1782; trước/sau 12/4/1781) → đổi lightmap theo năm của khung
  //  (năm ngoài mọi cửa sổ → lightmap có cửa sổ gần nhất). P.bake = '<dir>' (một lightmap, như NC-CPU) vẫn dùng được.
  const list = P.bakes ? P.bakes.map((b) => Object.assign({ fire: P.fire || null }, b)) : P.bake ? [{ dir: P.bake, wY: [-1e9, 1e9], fire: P.fire || null }] : [];
  if (!list.length) return { uni, meta: null, update() {} };
  for (const b of list) { b.M = await loadJSON(`/cache/nc/bake/${b.dir}/meta.json`); b.t = await tex(`/cache/nc/bake/${b.dir}/bake.png`, { srgb: false });
    b.t.minFilter = THREE.LinearMipmapLinearFilter; b.t.generateMipmaps = true; }
  const pick = (Y) => list.find((b) => Y >= b.wY[0] && Y <= b.wY[1]) || list.slice().sort((a, b) => Math.min(Math.abs(Y - a.wY[0]), Math.abs(Y - a.wY[1])) - Math.min(Math.abs(Y - b.wY[0]), Math.abs(Y - b.wY[1])))[0];
  const use = (b) => { uni.tNcBake.value = b.t; uni.uNcBakeBox.value.set(...b.M.box); uni.uNcBakeOn.value = 1; return b; };
  let cur = use(list[0]);
  const skyK = P.skyK ?? 1.0, bncK = P.bncK ?? 1.0;
  return { uni, meta: Object.assign({}, list[0].M, { dir: list[0].dir, bakes: list.map((b) => ({ dir: b.dir, wY: b.wY })) }), update(st) {
    if (list.length > 1) { const b = pick(st.year); if (b !== cur) cur = use(b); }
    const M = cur.M, fire = cur.fire;
    uni.uNcSkyK.value = skyK;
    // nảy nắng: tỉ lệ theo cường độ nắng hiện tại (đêm → 0) và lệch hướng nắng so lượt nướng (cos góc)
    const s = ctx.sun, d = ctx.sunDir, b = M.sun_dir ? new THREE.Vector3(...M.sun_dir) : d, cosA = Math.max(0, d.dot(b));
    uni.uNcSunC.value.copy(s.color).multiplyScalar(s.intensity * bncK * (M.g_scale || 0.25) / Math.PI * cosA * (1 - (st.night || 0)));
    if (fire && st.year >= fire.wY[0] && st.year <= fire.wY[1]) { const u = (st.year - fire.wY[0]) / (fire.wY[1] - fire.wY[0]);
      uni.uNcFireK.value = (fire.k ?? 1.0) * Math.min(1, u * 8) * Math.min(1, (1 - u) * 4) * (0.85 + 0.15 * Math.sin((st.year * 1e5) % 6.283)); } else uni.uNcFireK.value = 0; } };
}

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
  if (!P.bake) return { uni, meta: null, update() {} };
  const M = await loadJSON(`/cache/nc/bake/${P.bake}/meta.json`), t = await tex(`/cache/nc/bake/${P.bake}/bake.png`, { srgb: false });
  t.minFilter = THREE.LinearMipmapLinearFilter; t.generateMipmaps = true;
  uni.tNcBake.value = t; uni.uNcBakeBox.value.set(...M.box); uni.uNcBakeOn.value = 1;
  const skyK = P.skyK ?? 1.0, bncK = P.bncK ?? 1.0, fire = P.fire || null;   // fire: { wY: [năm bắt đầu, năm tắt], k }
  return { uni, meta: Object.assign({}, M, { dir: P.bake }), update(st) {
    uni.uNcSkyK.value = skyK;
    // nảy nắng: tỉ lệ theo cường độ nắng hiện tại (đêm → 0) và lệch hướng nắng so lượt nướng (cos góc)
    const s = ctx.sun, d = ctx.sunDir, b = M.sun_dir ? new THREE.Vector3(...M.sun_dir) : d, cosA = Math.max(0, d.dot(b));
    uni.uNcSunC.value.copy(s.color).multiplyScalar(s.intensity * bncK * (M.g_scale || 0.25) / Math.PI * cosA * (1 - (st.night || 0)));
    if (fire && st.year >= fire.wY[0] && st.year <= fire.wY[1]) { const u = (st.year - fire.wY[0]) / (fire.wY[1] - fire.wY[0]);
      uni.uNcFireK.value = (fire.k ?? 1.0) * Math.min(1, u * 8) * Math.min(1, (1 - u) * 4) * (0.85 + 0.15 * Math.sin((st.year * 1e5) % 6.283)); } else uni.uNcFireK.value = 0; } };
}

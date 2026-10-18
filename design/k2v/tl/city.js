// K2V tl · NHÀ THƯỜNG THỦ TỤC (lớp 2 chuẩn hình) + MỌC THEO NĂM (port lab/timelapse scene.js: hình học gộp + shader mọc).
// Bản ghi toà: [năm, năm_ghost, cao, cốt chân, mái (0 phẳng | 1 dốc), vùng (0 La Línea | 1 Gibraltar), vòng [[E,N]…]].
//  · mọc: toà nổi lên trong aDur năm, kết thúc đúng năm (Catastro: năm xây = năm hoàn thành; mốc tầng chuẩn: 1,5 năm trước mốc);
//  · V5b-1b — lớp TÁI DỰNG (năm_ghost; cổng 16/10 TRƯỢT: "ghost hộp mờ"): dựng bằng NHÀ ĐẦY ĐỦ (mái ngói, cửa sổ, chớp, ban công), cao 2–4 tầng
//    theo thời kỳ (không dùng chiều cao toà hiện nay), giảm bão hoà 22 % (≤ 25 %, KHÔNG trong suốt); trung thực giữ bằng nhãn phương pháp
//    "reconstructed from <nguồn, năm>" (text.js) — không phải hình toà cụ thể;
//  · KIỂU (≥ 6 mặt đứng × ≥ 6 mái), chọn theo vùng + thời kỳ + cỡ + băm tất định:
//      mặt đứng 0 Genoa/Gibraltar phấn màu + chớp xanh + ban công sắt · 1 Andalucía vôi trắng + chớp gỗ + song sắt · 2 Anh thế kỷ 19 (cửa kéo cao, gờ đá)
//      · 3 chung cư bê tông 1960+ (dải cửa + ban công liền) · 4 kho/xưởng gạch (cửa lớn thưa) · 5 kính/văn phòng 1990+ (lưới kính) · 6 doanh trại đá vôi
//      mái: phẳng · phẳng có tường chắn · phẳng có bồn nước/lồng cầu thang · hai mái ngói · mái hông có nóc · mái chóp — chìa mái 0,35 m;
//  · cửa sổ shader căn giữa TỪNG mặt (không vắt góc): khung, kính phản trời, chớp lá sách, bậu, lanh tô, gờ tầng, gờ mái, chân tường, góc đá;
//  · LOD theo ô 500 m: gần (LOD0: đủ mái/ban công/vật trên mái, hai mặt) · xa (LOD1: vòng đơn giản 2,5 m, mái phẳng/chóp) · rất xa: ẩn.
import { THREE, GLSL_NOISE, rng } from './core.js';
import { walls, roof, ridgeFor, simplify, pitched, rectOf, boxAt, balconies, signedArea, parcels } from './geom.js';

const PAL = {
  0: [[0.93, 0.80, 0.55], [0.94, 0.70, 0.58], [0.95, 0.88, 0.62], [0.86, 0.62, 0.48], [0.80, 0.84, 0.78], [0.96, 0.93, 0.84], [0.90, 0.76, 0.72]],   // Genoa phấn: vàng đất, hồng cá hồi, vàng nhạt, đất nung, xanh xám, kem, hồng tro
  1: [[0.97, 0.96, 0.92], [0.96, 0.93, 0.84], [0.97, 0.90, 0.70], [0.95, 0.95, 0.95], [0.92, 0.86, 0.74]],   // vôi trắng / kem / vàng Andalucía
  2: [[0.84, 0.76, 0.62], [0.78, 0.72, 0.64], [0.88, 0.82, 0.70]],   // đá vôi / vữa đá
  3: [[0.86, 0.83, 0.77], [0.78, 0.77, 0.75], [0.90, 0.86, 0.76], [0.80, 0.70, 0.60], [0.92, 0.90, 0.86]],
  4: [[0.66, 0.40, 0.31], [0.72, 0.50, 0.38], [0.70, 0.70, 0.68]],
  5: [[0.62, 0.70, 0.78], [0.70, 0.74, 0.76], [0.56, 0.64, 0.70]],
  6: [[0.80, 0.76, 0.66], [0.74, 0.70, 0.62]],
};
const TILE_C = [[0.70, 0.36, 0.24], [0.62, 0.30, 0.20], [0.74, 0.44, 0.30], [0.58, 0.34, 0.26]], FLAT_C = [[0.80, 0.78, 0.74], [0.72, 0.70, 0.67], [0.84, 0.80, 0.72], [0.62, 0.62, 0.62]];
const TILE = 500, NA = 19;
// V5b-2c (lệnh V0 mục d, I5): ngói đất nung thế kỷ 18 bão hoà hơn (S ≈ 0,72–0,78 trước ánh sáng) cho phố 1782 — không cháy sáng (giá trị ≤ 0,8)
const TILE_1782 = [[0.76, 0.33, 0.17], [0.70, 0.28, 0.15], [0.80, 0.40, 0.20], [0.66, 0.31, 0.18],
  [0.62, 0.34, 0.22], [0.78, 0.46, 0.26], [0.58, 0.27, 0.17], [0.74, 0.38, 0.28]];   // V5b-2d (C2-1 mục 5): ngói ĐA SẮC NHẸ — thêm nâu cũ, cam nhạt bạc nắng, đỏ sẫm, hồng đất (ngói thủ công nhiều mẻ nung)

// chọn kiểu mặt đứng + mái (tất định theo băm). Trả { sty, roof: 'flat'|'parapet'|'terrace'|'gable'|'hipr'|'pyr', gh (cao lớp tái dựng) }
// V5b-2b (M9): pd = THỜI KỲ của lớp footprint (bản ghi phần tử 8): 0 = 1704–1782 (mái ngói thấp + sân thượng phẳng, 2–3 tầng, không ban công sắt)
//  · 1 = 1900–1943 (mái ngói + mái bằng có tường chắn, ban công) · 2 / không khai = như cũ (theo năm + vùng).
export function styleOf(y, gy, h, reg, ar, R, pd) {
  const r = R(), r2 = R(), old = gy > 0 || (reg === 0 && y < 1960), smallish = ar < 260 && h <= 13;
  let sty, rf;
  if (pd === 3) { sty = 0; rf = r2 < 0.45 ? 'gable' : r2 < 0.7 ? 'hipr' : 'terrace'; return { sty, rf, gh: Math.min(h, 6.0 + Math.floor(R() * 2) * 3.0), noBalc: true, uoc: true }; }   // V5b-2c: phố 1782 LẤP ƯỚC TÍNH (I2) — như thời kỳ 0, tông vữa lệch nhẹ
  if (pd === 0) { sty = reg === 1 ? (r < 0.75 ? 0 : 6) : 1; rf = r2 < 0.38 ? 'gable' : r2 < 0.6 ? 'hipr' : 'terrace'; return { sty, rf, gh: Math.min(h, 6.0 + Math.floor(R() * 2) * 3.0), noBalc: true }; }
  if (pd === 1) { sty = reg === 1 ? (r < 0.6 ? 0 : 2) : (r < 0.8 ? 1 : 0); rf = r2 < 0.3 ? 'gable' : r2 < 0.5 ? 'hipr' : r2 < 0.8 ? 'parapet' : 'terrace'; return { sty, rf, gh: Math.min(h, 7.5 + Math.floor(R() * 3) * 3.0) }; }
  if (reg === 1 && old) { sty = ar > 700 ? 6 : r < 0.68 ? 0 : 2; }
  else if (reg === 0 && old) { sty = ar > 900 && h <= 7 ? 4 : r < 0.85 ? 1 : 0; }
  else { sty = ar > 1200 && h <= 12 ? 4 : h > 28 && y >= 1990 ? 5 : r < 0.15 && y >= 1995 ? 5 : 3; }
  if (old && smallish) rf = r2 < 0.42 ? 'gable' : r2 < 0.66 ? 'hipr' : r2 < 0.78 ? 'pyr' : r2 < 0.9 ? 'terrace' : 'parapet';
  else if (sty === 4) rf = r2 < 0.6 ? 'gable' : 'flat';
  else if (old && ar < 900) rf = r2 < 0.35 ? 'hipr' : r2 < 0.6 ? 'gable' : r2 < 0.8 ? 'terrace' : 'parapet';
  else if (old) rf = r2 < 0.5 ? 'parapet' : r2 < 0.75 ? 'terrace' : 'hipr';
  else rf = r2 < 0.45 ? 'parapet' : r2 < 0.85 ? 'terrace' : 'flat';
  const gh = Math.min(h, (reg === 1 ? 7.5 : 6.5) + Math.floor(R() * 3) * 3.0);   // lớp tái dựng: 2–4 tầng theo thời kỳ, xen kẽ
  return { sty, rf, gh };
}

export function makeCity(B, U, { lod = true, hid = 0, ghostDesat = 0.22 } = {}) {   // V5b-2b: hid > 0 = id hero của cả lớp (kênh B mặt nạ, hero_pct)
  const tiles = new Map(); const R = rng(17); const stats = { sty: [0, 0, 0, 0, 0, 0, 0], roof: {} , balc: 0 };
  const tri = (r) => THREE.ShapeUtils.triangulateShape(r.map(([x, y]) => new THREE.Vector2(x, y)), []);
  const add = (key) => { if (!tiles.has(key)) tiles.set(key, { L: [{ a: [] }, { a: [] }], c: null, n: 0 }); return tiles.get(key); };
  // V5b-1b: khối Gibraltar > 320 m² chia lô (7–13 m × ≤ 16 m), mỗi lô một nhà (kiểu, màu, mái, cao xen kẽ ±1 tầng ở nhà cũ)
  const B2 = []; let nSplit = 0;
  for (const b of B) { const ar = Math.abs(signedArea(b[6]));
    if (b[5] === 1 && ar > 320 && b[6].length >= 3) { const ps = parcels(b[6], R); nSplit++;
      for (const p of ps) { const old = b[1] > 0, dh = old ? (Math.floor(R() * 3) - 1) * 3.0 : 0; B2.push([b[0], b[1], Math.max(4, b[2] + dh), b[3], b[4], b[5], p, b[7]]); } }
    else B2.push(b); }
  stats.split = nSplit; stats.parcels = B2.length;
  for (const b of B2) {
    const [y, gy, h, base, rf0, reg, ring, pd] = b; if (ring.length < 3) continue;
    let cx = 0, cn = 0; for (const p of ring) { cx += p[0]; cn += p[1]; } cx /= ring.length; cn /= ring.length;
    const T = add(Math.floor(cx / TILE) + ',' + Math.floor(cn / TILE)); T.n++;
    const ar = Math.abs(signedArea(ring)), S = styleOf(y, gy, h, reg, ar, R, pd);
    let rfK = S.rf; if (rf0 && (rfK === 'flat' || rfK === 'parapet') && ar < 250) rfK = 'hipr';   // dữ liệu gói cảnh: nhà thấp cũ → mái dốc
    const P = PAL[S.sty]; let wc = P[Math.floor(R() * P.length)].map((v) => v * (0.93 + 0.1 * R()));
    if (S.uoc) wc = [wc[0] * 0.95 + 0.03, wc[1] * 0.97 + 0.03, wc[2] * 1.0 + 0.04].map((v) => Math.min(1, v));   // lấp ước tính: vữa ngả xám-lam nhẹ (khác tông, không trong suốt)
    const pitchedK = rfK === 'gable' || rfK === 'hipr' || rfK === 'pyr';
    const rc = (pitchedK ? (pd === 0 || pd === 3 ? TILE_1782 : TILE_C)[Math.floor(R() * (pd === 0 || pd === 3 ? TILE_1782.length : 4))] : FLAT_C[Math.floor(R() * 4)]).map((v) => v * (0.9 + 0.15 * R()));
    const dur = reg === 1 ? 1.5 : 4.0, seed = R();
    stats.sty[S.sty]++;
    for (let l = 0; l < 2; l++) {
      const A = T.L[l].a, rr = l === 0 ? ring : simplify(ring, 2.5);
      const emit = (col) => (x, yy, z, nx, ny, nz, u, top, el) => A.push(x, yy, z, nx, ny, nz, col[0], col[1], col[2], y, gy, base, u, dur, h, reg + seed * 0.5, el || 0, S.sty + 0.5, S.gh);
      walls(rr, h, emit(wc));
      if (l === 1) { roof(rr, h, pitchedK && rr.length <= 10 ? Math.min(2.5, ridgeFor(rr)) : 0, tri, emit(rc)); continue; }
      let done = false; const ridge = S.sty === 4 ? Math.min(2.0, 0.12 * Math.sqrt(ar)) : Math.max(1.4, Math.min(3.6, 0.24 * Math.sqrt(ar)));
      if (rfK === 'gable' || rfK === 'hipr') done = !!pitched(rr, h, ridge, rfK, emit(rc));
      if (!done && pitchedK) done = roof(rr, h, ridge, tri, emit(rc)) === 'hip';
      if (!done) { roof(rr, h, 0, tri, emit(rc)); if (rfK !== 'flat') walls(rr, h + 0.9, emit(wc.map((v) => v * 0.96)), h); }   // tường chắn mái 0,9 m
      if (!pitchedK && (rfK === 'terrace' || ar > 400)) {   // bồn nước / lồng cầu thang / máy điều hoà trên mái phẳng
        const Rr = rectOf(rr), rot = Rr ? Math.atan2(Rr.ax[1], Rr.ax[0]) : 0, n = ar > 400 ? 3 : 1 + Math.floor(R() * 2);
        for (let k = 0; k < n; k++) { const u = (R() - 0.5) * 0.5, v = (R() - 0.5) * 0.5, sz = 1.4 + R() * 2.2, L_ = Rr ? Rr.L : Math.sqrt(ar), W_ = Rr ? Rr.W : Math.sqrt(ar);
          const e = cx + (Rr ? Rr.ax[0] * u * L_ - Rr.ax[1] * v * W_ : u * L_), nn = cn + (Rr ? Rr.ax[1] * u * L_ + Rr.ax[0] * v * W_ : v * W_);
          boxAt(e, h, nn, sz, sz * (0.7 + 0.5 * R()), 1.0 + R() * 1.8, rot, emit(k === 0 ? wc.map((v) => v * 0.92) : [0.82, 0.83, 0.84]), -3); } }
      if (!S.noBalc && (S.sty === 0 || S.sty === 1 || S.sty === 3) && h >= 6 && R() < (S.sty === 3 ? 0.8 : 0.6)) stats.balc += balconies(rr, Math.min(h, S.sty === 3 ? h : 1e9), 3.0, emit(S.sty === 1 ? [0.25, 0.24, 0.24] : S.sty === 3 ? wc : [0.18, 0.22, 0.20]), S.sty === 3 ? 0.9 : 0.62);
      stats.roof[rfK] = (stats.roof[rfK] || 0) + 1;
    }
  }
  const mkMat = (lodLevel, depth) => {
    const m = depth ? new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }) : U.lambert ? new THREE.MeshLambertMaterial({ vertexColors: true }) : new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.88, metalness: 0 });
    if (!depth && lodLevel === 0) m.side = THREE.DoubleSide;
    m.customProgramCacheKey = () => 'tl-city-' + lodLevel + (depth ? '-d' : '') + '-h' + hid + '-g' + ghostDesat;   // tường chắn mái / lan can thấy cả mặt trong
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, { uYear: U.uYear, uDim: U.uDim, uSample: U.uSample, uMask: U.uMask, uGhostDesat: { value: ghostDesat } });
      sh.vertexShader = sh.vertexShader.replace('#include <common>', `#include <common>
        attribute float aYear; attribute float aGhost; attribute float aBase; attribute float aU; attribute float aDur; attribute float aH; attribute float aReg; attribute float aEL; attribute float aSty; attribute float aGH;
        uniform float uYear; varying float vU; varying float vLY; varying float vGhost; varying float vReg; varying float vH; varying float vYear; varying float vEL; varying float vSty; varying vec3 vObjN; varying vec3 vWPc;
        float growK(){ float u = clamp((uYear - (aYear - aDur)) / aDur, 0.0, 1.0); return u < 1.0 ? (1.0 - pow(1.0 - u, 3.0)) * 1.05 - 0.05 * u * u : 1.0; }`)
        .replace('#include <begin_vertex>', `#include <begin_vertex>
        float gk = growK(); bool gh = aGhost > 0.5 && uYear >= aGhost;
        // lớp tái dựng: nhà đầy đủ cao aGH (2–4 tầng thời kỳ); toà thật (mốc bằng chứng) mọc xuyên qua; mái/vật trên mái giữ hình, chỉ dời theo đỉnh tường
        float sc = gh ? max(gk, aGH / max(aH, 1.0)) : gk; float yy = transformed.y;
        if (aU < -1.5 && aU > -2.5 || aU < -3.5) { if (yy > aH * sc - 1.2) transformed.y = -200.0; }   // ban công/lan can: chỉ tầng đã có
        else transformed.y = min(yy, aH) * sc + max(yy - aH, 0.0) * min(1.0, sc * 3.0);
        vLY = transformed.y; vU = aU; vReg = aReg; vH = aH * sc; vYear = gh && gk < 0.5 ? 1800.0 : aYear; vGhost = gh && gk < 0.99 ? 1.0 : 0.0; vEL = aEL; vSty = aSty; ${depth ? 'vObjN = vec3(0.0, 1.0, 0.0);' : 'vObjN = objectNormal;'}
        if (!gh && gk <= 0.0) transformed.y -= 80.0;
        transformed.y += aBase; vWPc = (modelMatrix * vec4(transformed, 1.0)).xyz;`);
      const FR = `${GLSL_NOISE}
        uniform float uYear, uDim, uSample, uMask, uGhostDesat; varying float vU; varying float vLY; varying float vGhost; varying float vReg; varying float vH; varying float vYear; varying float vEL; varying float vSty; varying vec3 vObjN;
        varying vec3 vWPc; bool railHole(){ if (vU > -3.5) return false; float hr = fract(vLY); return hr < 0.88 && fract((vWPc.x + vWPc.z) * 7.0) > 0.30; }   // lan can: song sắt 0,14 m, tay vịn trên`;
      if (depth) { sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + FR); return; }
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + FR)
        .replace('#include <color_fragment>', `#include <color_fragment>
        float dd_ = length(vViewPosition); if (railHole() && dd_ < 900.0) discard;
        float dd = dd_; int sty = int(vSty); vec3 base = diffuseColor.rgb;
        float seedB = fract(vReg * 2.0) * 97.0;
        if (vU >= 0.0 && ${lodLevel === 0 ? 'true' : 'false'}) {
          float fh = sty == 2 ? 3.4 : 3.0; float bay = sty == 0 ? 2.7 : sty == 1 ? 3.1 : sty == 2 ? 3.0 : sty == 3 ? 3.5 : sty == 4 ? 5.5 : sty == 5 ? 1.6 : 3.2;
          float nb = max(1.0, floor((vEL - 0.8) / bay)), off = (vEL - nb * bay) * 0.5, qx = (vU - off) / bay;
          vec2 q = vec2(qx, vLY / fh); vec2 f = fract(q); vec2 id = floor(q);
          float aa = clamp(fwidth(q.x) * 2.5, 0.0, 1.0), inb = step(0.0, qx) * step(qx, nb), top = vH - 0.55;
          float fl = id.y, nfl = floor(vH / fh);
          // kích thước ô cửa theo kiểu
          vec4 wb = sty == 0 ? vec4(0.30, 0.70, 0.22, 0.80) : sty == 1 ? vec4(0.32, 0.68, 0.25, 0.78) : sty == 2 ? vec4(0.33, 0.67, 0.16, 0.84) : sty == 3 ? vec4(0.12, 0.88, 0.30, 0.78) : sty == 4 ? vec4(0.25, 0.75, 0.45, 0.82) : sty == 5 ? vec4(0.04, 0.96, 0.08, 0.94) : vec4(0.30, 0.70, 0.22, 0.78);
          float win = step(wb.x, f.x) * step(f.x, wb.y) * step(wb.z, f.y) * step(f.y, wb.w) * step(1.0, fl) * step(vLY, top - 0.3) * inb;
          if (sty == 4) win *= step(0.5, h21(id + seedB));
          float door = (1.0 - step(1.0, fl)) * step(0.30, f.x) * step(f.x, 0.70) * step(f.y, 0.72) * inb * step(0.45, h21(vec2(id.x, seedB)));
          float shopw = (1.0 - step(1.0, fl)) * step(0.12, f.x) * step(f.x, 0.88) * step(0.06, f.y) * step(f.y, 0.70) * inb * step(0.6, h21(vec2(id.x + 7.0, seedB))) * step(1.0, float(sty == 3 || sty == 1 || sty == 0));
          float frame = step(wb.x - 0.05, f.x) * step(f.x, wb.y + 0.05) * step(wb.z - 0.04, f.y) * step(f.y, wb.w + 0.03) * step(1.0, fl) * step(vLY, top - 0.3) * inb * (1.0 - win);
          float sill = step(wb.x - 0.07, f.x) * step(f.x, wb.y + 0.07) * step(wb.z - 0.07, f.y) * step(f.y, wb.z - 0.02) * step(1.0, fl) * inb * step(vLY, top - 0.3);
          float lintel = step(wb.x - 0.04, f.x) * step(f.x, wb.y + 0.04) * step(wb.w + 0.03, f.y) * step(f.y, wb.w + 0.09) * step(1.0, fl) * inb * step(vLY, top - 0.3);
          // kính phản trời: sáng trên, tối dưới + loang theo ô
          vec3 glass = mix(vec3(0.10, 0.13, 0.17), vec3(0.42, 0.55, 0.70), smoothstep(wb.z, wb.w, f.y) * 0.65) * (0.8 + 0.35 * h21(id + 1.3));
          if (sty == 5) glass = mix(vec3(0.20, 0.32, 0.44), vec3(0.55, 0.70, 0.84), f.y * 0.6 + 0.25 * h21(id));
          // chớp lá sách (mở/đóng theo ô): kiểu 0, 1, 6; màu theo vùng (xanh Gibraltar, gỗ/xanh lá Andalucía)
          float hasSh = (sty == 0 || sty == 1 || sty == 6) ? 1.0 : 0.0, shutC = step(0.42, h21(id * 1.7 + seedB));
          vec3 shc = sty == 0 || sty == 6 ? vec3(0.16, 0.34, 0.24) : (h21(vec2(seedB, 3.0)) < 0.5 ? vec3(0.42, 0.28, 0.16) : vec3(0.14, 0.30, 0.22));
          float louv = 0.75 + 0.25 * step(0.5, fract(f.y * 22.0));
          vec3 wcol = mix(glass, shc * louv, hasSh * shutC);
          // chớp mở: hai cánh hai bên khung
          float shOpen = hasSh * (1.0 - shutC) * step(1.0, fl) * inb * step(vLY, top - 0.3) * step(wb.z, f.y) * step(f.y, wb.w) * (step(wb.x - 0.17, f.x) * step(f.x, wb.x - 0.05) + step(wb.y + 0.05, f.x) * step(f.x, wb.y + 0.17));
          float k = (1.0 - aa) * (1.0 - smoothstep(650.0, 1500.0, dd));
          vec3 c = base;
          c *= 1.0 - 0.05 * step(fract(vLY / fh), 0.04) * step(1.0, fl);   // gờ tầng
          c = mix(c, base * 0.62, (1.0 - step(0.85, vLY)) * 0.55 * k);   // chân tường (đế)
          c = mix(c, min(base * 1.12 + 0.06, vec3(1.0)), step(top, vLY) * k);   // gờ mái sáng
          c = mix(c, base * 0.70, step(top - 0.18, vLY) * step(vLY, top) * k);   // bóng dưới gờ mái
          if (sty == 0 || sty == 2 || sty == 6) c = mix(c, min(base * 1.1 + 0.05, vec3(1.0)), (step(vU, 0.55) + step(vEL - 0.55, vU)) * k * 0.8);   // góc đá / trụ góc
          c = mix(c, vec3(0.93, 0.92, 0.88), (sill + lintel * 0.6) * k * (sty == 5 ? 0.0 : 1.0));
          c = mix(c, sty == 1 || sty == 0 ? vec3(0.95, 0.94, 0.90) : base * 0.8, frame * k * 0.9);
          c = mix(c, shc * louv, shOpen * k);
          c = mix(c, wcol, win * k);
          c = mix(c, vec3(0.20, 0.16, 0.12) * (0.8 + 0.4 * h21(id + 5.0)), door * k);
          c = mix(c, mix(vec3(0.12, 0.15, 0.18), vec3(0.50, 0.42, 0.30), step(0.55, f.y)), shopw * k * 0.9);
          float far_ = 1.0 - k; c = mix(c, base * 0.86, far_ * 0.35 * step(1.0, fl));   // xa: tông cửa trung bình (không nhấp nháy)
          diffuseColor.rgb = c;
        }
        if (vU < -1.5 && vU > -2.5) diffuseColor.rgb *= 0.92;   // sàn ban công
        if (vU < -3.5) diffuseColor.rgb = vec3(0.12, 0.13, 0.13);
        if (vU >= 0.0 || vU < -1.5) diffuseColor.rgb *= 0.74 + 0.26 * smoothstep(0.0, 6.0, vLY);   // AO chân tường
        diffuseColor.rgb *= 0.94 + 0.10 * vn(vec2(vU * 0.35 + seedB, vLY * 0.5));   // loang vữa
        if (vU > -1.5 && vU < -0.5) {   // mái: ngói (hàng + rãnh) hoặc mái phẳng (tấm + vết)
          float tile = 0.86 + 0.14 * step(0.5, fract(vLY * 3.2)); diffuseColor.rgb *= abs(vObjN.y) < 0.98 ? tile : 1.0;   // hàng ngói trên mái dốc
          diffuseColor.rgb *= 0.92 + 0.14 * vn(vec2(vLY * 1.7 + seedB, seedB));
          if (abs(vObjN.y) > 0.98) { vec2 rp = vWPc.xz; float aa2 = clamp(fwidth(rp.x) * 2.0, 0.0, 1.0);   // mái phẳng: tấm lát 1,2 m, vết ố, lỗ thoát nước
            vec2 g = abs(fract(rp / 1.2) - 0.5); float joint = (1.0 - aa2) * (step(0.47, g.x) + step(0.47, g.y));
            diffuseColor.rgb *= (1.0 - 0.07 * min(joint, 1.0)) * (0.86 + 0.22 * vn(rp * 0.21 + seedB)) * (1.0 - 0.12 * smoothstep(0.62, 0.9, vn(rp * 0.07 - seedB))); }
        }
        if (vGhost > 0.5) { float L = dot(diffuseColor.rgb, vec3(0.299, 0.587, 0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), uGhostDesat); }   // lớp tái dựng: giảm bão hoà 22 %
        float L = dot(diffuseColor.rgb, vec3(0.299, 0.587, 0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55 * uDim) * (1.0 - 0.36 * uDim);`)
        .replace('#include <dithering_fragment>', `#include <dithering_fragment>\n if (uMask > 0.5) gl_FragColor = vec4(1.0, vGhost > 0.5 ? 0.2 : 0.0, ${(hid / 255).toFixed(6)}, 1.0);   /* V5b-2b: G = 0,2 → toà lớp TÁI DỰNG (ghost_pct, K-1.13); B = id hero của lớp */`);
    };
    return m;
  };
  const mats = [mkMat(0, false), mkMat(1, false)], depth = mkMat(0, true);
  const group = new THREE.Group(); let tris = [0, 0];
  for (const [key, T] of tiles) {
    const [tx, tn] = key.split(',').map(Number); T.c = new THREE.Vector3((tx + 0.5) * TILE, 0, -(tn + 0.5) * TILE); T.m = [];
    for (let l = 0; l < 2; l++) {
      const A = new Float32Array(T.L[l].a), n = A.length / NA, g = new THREE.BufferGeometry(); T.L[l].a = null;
      const at = (o, s) => { const out = new Float32Array(n * s); for (let i = 0; i < n; i++) for (let k = 0; k < s; k++) out[i * s + k] = A[i * NA + o + k]; return out; };
      g.setAttribute('position', new THREE.BufferAttribute(at(0, 3), 3)); g.setAttribute('normal', new THREE.BufferAttribute(at(3, 3), 3)); g.setAttribute('color', new THREE.BufferAttribute(at(6, 3), 3));
      for (const [nm, o] of [['aYear', 9], ['aGhost', 10], ['aBase', 11], ['aU', 12], ['aDur', 13], ['aH', 14], ['aReg', 15], ['aEL', 16], ['aSty', 17], ['aGH', 18]]) g.setAttribute(nm, new THREE.BufferAttribute(at(o, 1), 1));
      g.boundingSphere = new THREE.Sphere(T.c.clone().setY(30), TILE); const mesh = new THREE.Mesh(g, mats[l]); mesh.customDepthMaterial = depth;
      mesh.castShadow = mesh.receiveShadow = true; mesh.visible = l === 0; group.add(mesh); T.m.push(mesh); tris[l] += n / 3;
    }
  }
  // chọn LOD theo khoảng cách máy (mặt bằng) tới tâm ô
  const near = 1400, far = 5200; let stat = { lod0: 0, lod1: 0, off: 0 };
  function update(cam) { stat = { lod0: 0, lod1: 0, off: 0 };
    for (const T of tiles.values()) { const d = Math.hypot(cam.position.x - T.c.x, cam.position.z - T.c.z) - Math.max(0, cam.position.y * 0.2);
      const l = !lod ? 0 : d < near ? 0 : d < far ? 1 : 2; T.m[0].visible = l === 0; T.m[1].visible = l === 1; stat[['lod0', 'lod1', 'off'][l]]++; } }
  return { group, update, stat: () => stat, tris, nTiles: tiles.size, styles: stats };
}

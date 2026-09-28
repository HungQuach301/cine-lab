// Cine Lab · Cổng 5 — ÁNH SÁNG CẬN MẶT IDA (gói W3, A1 mục 3). W3 giữ file này; W2 dùng cho s26, s36, s37, s39 (và cận mặt khác nếu cần).
//
// Vấn đề (kiểm mù lần 3): cận mặt chỉ có MỘT nguồn rất gần (đèn khí L11 cách mặt ~0,5 m, chếch trên) → trán cháy, nửa mặt và cằm chìm,
// cổ áo nằm trong bóng cằm → mặt sáng "tách khỏi thân" như mặt nạ; ở s26 đèn lồng thấp chỉ bắt vào mắt ("mắt phát sáng").
// Cách làm: KHÔNG thêm nguồn ngoài truyện. Chỉ thêm ánh DỘI của các nguồn có thật (vôi tường, đá lát, áo, thang) và ánh viền của
// nguồn có thật phía sau (trời đêm / đèn khí xa / ánh điện tràn). Mọi đèn phụ: không đổ bóng, có tầm (distance) ngắn → chỉ chạm vùng quanh đầu.
// Cường độ tính theo TỶ LỆ với độ rọi của nguồn chính tại mặt (key:fill), nên đúng ở mọi khoảng cách tới đèn và theo mức lửa/điện từng khung.
//
// API
//   const fl = createFaceLight(scene, { mode: 'gas' | 'lantern' | 'elec', ...ghi đè preset });
//   // mỗi khung, SAU khi đặt tư thế nhân vật và máy quay, và SAU khi bộ cảnh đặt cường độ đèn (setState):
//   fl.update(ch, cam, { key?: THREE.Light | THREE.Light[], keyE?: number, level?: number });
//      key   : nguồn chính trong truyện (PointLight của L11, của đèn lồng…). Bỏ trống → tự chọn đèn điểm/spot trong cảnh rọi mạnh nhất vào mặt.
//      keyE  : (tuỳ chọn) độ rọi nguồn chính tại mặt nếu nguồn là ánh tràn phẳng (vd. whiteHemi.intensity ở s39). Cộng với phần của `key`.
//      level : (tuỳ chọn) nhân chung 0…1 (vd. để tắt dần cùng nguồn).
//   fl.exposure(target?)  → phơi sáng đề xuất để vùng da sáng nhất KHÔNG cháy (tính từ độ rọi tổng tại mặt; hiệu chỉnh ở face_ida, xem BAO-CAO-W3).
//   fl.faceE()            → độ rọi đo được tại mặt ở lần update gần nhất { key, fill, under, rim, total } (đơn vị three.js: cd/m²·… = I/d²).
//   fl.lights             → { fill, under, rim } (PointLight) để W2 ẩn/soi khi cần. fl.dispose() gỡ khỏi cảnh.
//
// Preset (tỷ lệ so với độ rọi nguồn chính tại mặt):
//   gas     — L11 ngay trước mặt (s36, s37): dội ấm từ vôi tường + đá lát phía máy (fill 0,30), dội từ áo/khăn/đá lên cằm (under 0,14),
//             viền lạnh của trời đêm sau lưng (rim 0,22). Key:fill ≈ 3:1 (≈ 1,6 stop) — đêm, còn bóng, nhưng nửa tối đọc được.
//   lantern — đèn lồng thấp ở thắt lưng/tay (s26, s31): dội từ trên-trước (đèn khí L11 + vôi tường, fill 0,45), dưới nhẹ (0,06 — đèn lồng đã từ dưới),
//             viền ấm của L11 sau lưng (0,25). Mục đích: mặt có khối từ trên xuống nên mắt không còn là chỗ sáng duy nhất.
//   elec    — trắng phẳng của cột điện (s39): điện là nguồn phẳng không bóng (luật thế giới) → chỉ thêm khối rất nhẹ: fill lạnh trung tính
//             lệch 35° (0,12), under 0,08; KHÔNG viền (L11 đang nhạt đã tự rọi mặt). Nguồn chính = L11 (tự chọn) + keyE = whiteHemi.intensity.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';

export const FACE_LIGHT_PRESETS = {
  gas:     { fill: { color: '#d9ad8a', ratio: 0.20, dist: 1.0, elev: 12, side: 1 }, under: { color: '#b58068', ratio: 0.12, dist: 0.7 }, rim: { color: '#8c96d0', ratio: 0.22, dist: 0.8, elev: 40 } },
  lantern: { fill: { color: '#e0b48c', ratio: 0.45, dist: 1.0, elev: 38, side: 1 }, under: { color: '#b58068', ratio: 0.06, dist: 0.7 }, rim: { color: '#ffb872', ratio: 0.25, dist: 0.8, elev: 35 } },
  elec:    { fill: { color: '#e8ecf4', ratio: 0.12, dist: 1.0, elev: 20, side: -1 }, under: { color: '#bdb6b0', ratio: 0.08, dist: 0.7 }, rim: { color: '#ffb872', ratio: 0.0, dist: 0.8, elev: 30 } },
};
// Hiệu chỉnh phơi sáng (đo ở face_ida, 1920×1080, 3 mẫu, lớp vẽ C): uExp × E_mặt ≈ K cho da sáng nhất ~0,80 sau tone map (không cháy).
export const FACE_EXPOSURE_K = { gas: 4.0, lantern: 4.0, elec: 6.0 };   // elec: trắng tràn chịu sáng hơn (giữ cảm giác trắng phẳng), vẫn không cháy da
const CUT = 1.6;   // tầm đèn phụ = 1,6 × khoảng cách đặt (≤ 1,6 m) → không chạm tường/bộ cảnh sau lưng, chỉ vùng đầu–vai

const Y = new THREE.Vector3(0, 1, 0);
const _v = new THREE.Vector3(), _w = new THREE.Vector3(), _q = new THREE.Quaternion();

// Độ rọi (không tính cosθ) của một đèn tại điểm p — cùng mô hình suy giảm với three.js (decay 2, cửa sổ tầm `distance`).
export function illuminanceAt(L, p) {
  if (!L.visible || !(L.intensity > 0)) return 0;
  if (L.isHemisphereLight || L.isAmbientLight) return L.intensity;
  if (L.isDirectionalLight) return L.intensity;
  L.getWorldPosition(_w); const d = Math.max(0.05, _w.distanceTo(p));
  let e = L.intensity / Math.pow(d, L.decay ?? 2);
  if (L.distance > 0) e *= Math.pow(Math.max(0, 1 - Math.pow(d / L.distance, 4)), 2);
  return e;
}

export function createFaceLight(scene, o = {}) {
  const mode = o.mode || 'gas', base = FACE_LIGHT_PRESETS[mode] || FACE_LIGHT_PRESETS.gas;
  const P = { fill: { ...base.fill, ...(o.fill || {}) }, under: { ...base.under, ...(o.under || {}) }, rim: { ...base.rim, ...(o.rim || {}) } };
  const mk = (c) => { const L = new THREE.PointLight(c.color, 0, c.dist * CUT, 2); L.castShadow = false; L.userData.faceLight = true; scene.add(L); return L; };
  const lights = { fill: mk(P.fill), under: mk(P.under), rim: mk(P.rim) };
  const win = (c) => Math.pow(1 - Math.pow(1 / CUT, 4), 2);   // bù cửa sổ tầm tại đúng khoảng cách đặt đèn
  let last = { key: 0, fill: 0, under: 0, rim: 0, total: 0 };

  // Tâm mặt (giữa mắt và miệng) + hướng mặt, theo hệ đầu của cast3d (y = 0 cằm, 1 đỉnh sọ, +z mặt).
  function faceFrame(ch) {
    const H = ch.H, head = ch.joints.head; head.updateWorldMatrix(true, false);
    const c = new THREE.Vector3(0, 0.42 * H, 0.30 * H); head.localToWorld(c);
    head.getWorldQuaternion(_q); const fw = new THREE.Vector3(0, 0, 1).applyQuaternion(_q);
    return { c, fw, H };
  }
  function autoKey(p) {
    let best = null, be = 0;
    scene.traverse((L) => { if (!(L.isPointLight || L.isSpotLight) || L.userData.faceLight) return; const e = illuminanceAt(L, p); if (e > be) { be = e; best = L; } });
    return best;
  }
  // Đặt đèn phụ theo hướng `dir` (đã chuẩn hoá) cách mặt `dist`, cường độ để độ rọi tại mặt = E.
  const place = (L, c, dir, dist, E) => { L.position.copy(c).addScaledVector(dir, dist); L.intensity = Math.max(0, E) * dist * dist / win(); };

  function update(ch, cam, s = {}) {
    const { c, fw } = faceFrame(ch);
    let keys = s.key ? (Array.isArray(s.key) ? s.key : [s.key]) : null;
    if (!keys) { const k = autoKey(c); keys = k ? [k] : []; }
    let Ek = (s.keyE ?? 0); const kp = new THREE.Vector3(); let wsum = 0;
    for (const L of keys) { const e = illuminanceAt(L, c); Ek += e; if (e > 0 && !L.isHemisphereLight) { L.getWorldPosition(_w); kp.addScaledVector(_w, e); wsum += e; } }
    const lv = s.level ?? 1; Ek *= lv;
    // hướng (mặt phẳng ngang) từ mặt tới máy và tới nguồn chính
    const toCam = cam.getWorldPosition(new THREE.Vector3()).sub(c); toCam.y = 0; toCam.normalize();
    let toKey = wsum > 0 ? kp.multiplyScalar(1 / wsum).sub(c) : fw.clone(); toKey.y = 0; if (toKey.lengthSq() < 1e-8) toKey.copy(fw); toKey.normalize();
    // FILL: phía máy, đối xứng với nguồn chính qua trục mặt–máy (ánh dội từ phía không có nguồn); key trùng trục máy → lệch 35° sang phía kia.
    let f = toCam.clone().multiplyScalar(2 * toCam.dot(toKey)).sub(toKey); f.y = 0;
    if (f.lengthSq() < 1e-6 || f.angleTo(toKey) < 0.6) { const sgn = Math.sign(new THREE.Vector3().crossVectors(toKey, toCam).y || 1) * (P.fill.side ?? 1); f = toCam.clone().applyAxisAngle(Y, sgn * 35 * Math.PI / 180); }
    f.normalize(); const fe = P.fill.elev * Math.PI / 180; f.multiplyScalar(Math.cos(fe)).addScaledVector(Y, Math.sin(fe)).normalize();
    // UNDER: dội từ dưới-trước (đá lát, áo, khăn) — nhấc bóng dưới cằm, nối cằm với cổ áo.
    const u = fw.clone(); u.y = 0; u.normalize().multiplyScalar(0.55).addScaledVector(Y, -0.83).normalize();
    // RIM: sau đầu, phía ngược máy, cao — viền mũ/vai/mép má xa (tách khỏi nền), không rọi mặt trước.
    const r = toCam.clone().negate().applyAxisAngle(Y, 30 * Math.PI / 180 * Math.sign(toKey.x * toCam.z - toKey.z * toCam.x || 1)); const re = P.rim.elev * Math.PI / 180;
    r.multiplyScalar(Math.cos(re)).addScaledVector(Y, Math.sin(re)).normalize();
    const E = { fill: P.fill.ratio * Ek, under: P.under.ratio * Ek, rim: P.rim.ratio * Ek };
    place(lights.fill, c, f, P.fill.dist, E.fill); place(lights.under, c, u, P.under.dist, E.under); place(lights.rim, c, r, P.rim.dist, E.rim);
    last = { key: Ek, ...E, total: Ek + E.fill + E.under };
    return last;
  }
  return {
    lights, preset: P, update, faceE: () => last,
    exposure: (K = FACE_EXPOSURE_K[mode] ?? 4.0) => (last.total > 0 ? K / last.total : 1),
    dispose: () => { for (const L of Object.values(lights)) scene.remove(L); },
  };
}

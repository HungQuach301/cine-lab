// Cine Lab · Cổng 4 — tiện ích hoạt hoạ previs: nội suy tư thế có gia tốc (không tuyến tính — luật H1), khoá máy quay, nhân vật.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { charMat, contactBlob } from './sets.js';

export const ease = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
export const easeIO = (u) => { u = Math.max(0, Math.min(1, u)); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
export const clamp01 = (u) => Math.max(0, Math.min(1, u));
export const fovOf = (mm) => 2 * Math.atan(12 / mm) * 180 / Math.PI;   // tiêu cự tương đương 35 mm (cảm biến cao 24 mm) → FOV dọc
export const V = (a) => new THREE.Vector3(...a);

// Trộn hai tư thế (định dạng model sheet + hat_back, root_y_m). Khớp thiếu = 0.
export function lerpPose(a, b, u) {
  const joints = {}, names = new Set([...Object.keys(a.joints || {}), ...Object.keys(b.joints || {})]);
  for (const n of names) { const p = (a.joints || {})[n] || [0, 0, 0], q = (b.joints || {})[n] || [0, 0, 0]; joints[n] = p.map((v, i) => v + (q[i] - v) * u); }
  const hands = {};
  for (const s of ['L', 'R']) { const p = (a.hands || {})[s] || { spread: 0.1, curl: 0.4 }, q = (b.hands || {})[s] || { spread: 0.1, curl: 0.4 };
    hands[s] = { spread: (p.spread ?? 0.1) + ((q.spread ?? 0.1) - (p.spread ?? 0.1)) * u, curl: (p.curl ?? 0.4) + ((q.curl ?? 0.4) - (p.curl ?? 0.4)) * u, thumb_cross: (u < 0.5 ? p : q).thumb_cross }; }
  return { joints, hands, props: (u < 0.5 ? a : b).props || [], hat_back: (a.hat_back ?? 0) + ((b.hat_back ?? 0) - (a.hat_back ?? 0)) * u, root_y_m: (a.root_y_m ?? 0) + ((b.root_y_m ?? 0) - (a.root_y_m ?? 0)) * u };
}
// Ghép khớp: tư thế nền + ghi đè (joints/hands từng phần).
export function over(base, o = {}) {
  return { ...base, ...o, joints: { ...(base.joints || {}), ...(o.joints || {}) }, hands: { ...(base.hands || {}), ...(o.hands || {}) }, props: o.props ?? base.props };
}
// Khoá tư thế theo thời gian: keys = [[t, pose], ...] → tư thế tại t (nội suy easeIO giữa hai khoá).
export function poseAt(keys, t) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [ta, pa] = keys[i], [tb, pb] = keys[i + 1]; if (t <= tb) return lerpPose(pa, pb, easeIO((t - ta) / (tb - ta))); }
  return keys[keys.length - 1][1];
}
// Khoá số/vectơ theo thời gian (easeIO).
export function valAt(keys, t) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) { const [ta, a] = keys[i], [tb, b] = keys[i + 1];
    if (t <= tb) { const u = easeIO((t - ta) / (tb - ta)); return Array.isArray(a) ? a.map((v, k) => v + (b[k] - v) * u) : a + (b - a) * u; } }
  return keys[keys.length - 1][1];
}
// Máy quay theo khoá: keys = [[t, pos[3], look[3], fovDeg?], ...]
export function camAt(cam, keys, t) {
  const p = valAt(keys.map((k) => [k[0], k[1]]), t), l = valAt(keys.map((k) => [k[0], k[2]]), t);
  const fv = valAt(keys.map((k) => [k[0], k[3] ?? cam.fov]), t);
  cam.position.set(...p); cam.lookAt(...l); if (Math.abs(cam.fov - fv) > 1e-4) { cam.fov = fv; cam.updateProjectionMatrix(); }
}
// Rung máy cầm tay nhẹ (không dùng mặc định; chỉ shot chỉ định).
export const handheld = (t, a = 0.004) => [a * Math.sin(t * 1.7) + a * 0.5 * Math.sin(t * 4.3 + 1), a * 0.8 * Math.sin(t * 2.1 + 2), 0];

// Tạo nhân vật trong cảnh: vật liệu Lambert, đổ/nhận bóng, đánh dấu "quan trọng" cho lớp vẽ, vệt tối tiếp xúc dưới chân.
export function makeChar(ctx, scene, who, opts = {}) {
  const sheet = ctx.sheets[who];
  const ch = ctx.mkChar(sheet, { material: opts.material || charMat, detail: opts.detail ?? 22, expr: opts.expr, hatBack: opts.hatBack, faceQ: opts.faceQ, gaze: opts.gaze, glint: opts.glint ?? 0.12 });   // glint theo phơi sáng previs (face_ida dùng 5,0 ở phơi sáng 0,12)
  ch.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  ch.root.userData.imp = 1; scene.add(ch.root);
  ch.who = who; ch.sheetRef = sheet;
  if (opts.blob !== false) { ch.blob = contactBlob(who === 'cas' ? 0.32 : 0.42, opts.blobA ?? 0.5); scene.add(ch.blob); }
  // đặt tư thế + gốc (x, z, hướng); gốc y = pose.root_y_m (+ y0 nền)
  ch.place = (pose, x, z, yaw, y0 = 0) => {
    ch.setPose(pose); ch.root.position.set(x, y0 + (pose.root_y_m ?? 0), z); ch.root.rotation.y = yaw; ch.root.updateMatrixWorld(true);
    if (ctx.upd) ctx.upd(ch, null);
    if (ch.blob) { ch.blob.position.set(x, y0 + 0.012, z); ch.blob.visible = (pose.root_y_m ?? 0) < 0.3; }
  };
  return ch;
}
// Hướng quay (yaw) để nhân vật (mặt +z cục bộ) nhìn về điểm (x, z).
export const yawTo = (fx, fz, tx, tz) => Math.atan2(tx - fx, tz - fz);

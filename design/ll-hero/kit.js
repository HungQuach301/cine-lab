// Last Lamplighters · CẢNH ĐINH 3D (chủ dự án 06/10/2026, CHUAN-KENH §11.3) — bộ đồ nghề dùng chung.
// three.js trong Chromium headless (SwiftShader), cùng đường ống hậu kỳ với tập 1 (design/cong3/shared/post.js).
// Phong cách: khối giản lược, ánh đèn khí ấm, sương theo độ sâu, bóng người vô danh (không mặt), hạt bụi trong vùng sáng.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { buildGasLamp } from '/cong3/shared/props.js';
import { glowSprite, rng } from '/cong3/dir-C/common.js';
export { THREE, buildGasLamp, glowSprite, rng };

// Kịch bản màu theo hồi (CHUAN-KENH §11.2 Q30): truyện ấm · lịch sử sepia · hôm nay lạnh · kết ấm
export const GRADES = {
  warm:  { gCanvas: 0.012, gVig: 0.28, gLift: 0.02, gSat: 1.0,  gShadowTint: [0.45, 0.35, 0.95], gHiTint: [1.0, 0.97, 0.92] },
  sepia: { gCanvas: 0.016, gVig: 0.32, gLift: 0.03, gSat: 0.55, gShadowTint: [0.55, 0.42, 0.30], gHiTint: [1.04, 0.96, 0.84] },
  cold:  { gCanvas: 0.010, gVig: 0.26, gLift: 0.02, gSat: 0.85, gShadowTint: [0.28, 0.34, 0.95], gHiTint: [0.95, 1.0, 1.06] },
};

export const ease = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
export const easeIO = (u) => { u = Math.max(0, Math.min(1, u)); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
export const lerp = (a, b, u) => a + (b - a) * u;
export const V = (x, y, z) => new THREE.Vector3(x, y, z);
export const lam = (color, o = {}) => new THREE.MeshLambertMaterial({ color, ...o });
export const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.8, metalness: 0, ...o });
export const fovOf = (mm) => 2 * Math.atan(12 / mm) * 180 / Math.PI;

// Cảnh đang dựng: box/cyl không truyền parent thì gắn vào cảnh này (lỗi lượt thử đầu: vật thể không có parent bị bỏ rơi)
let CUR = null; export const useScene = (s) => { CUR = s; return s; };
export function box(w, h, d, m, x = 0, y = 0, z = 0, parent) {
  const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; (parent || CUR)?.add(o); return o;
}
export function cyl(r0, r1, h, m, x = 0, y = 0, z = 0, parent, seg = 16) {
  const o = new THREE.Mesh(new THREE.CylinderGeometry(r0, r1, h, seg), m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; (parent || CUR)?.add(o); return o;
}

// Máy quay: khoá mốc { t, p:[x,y,z], l:[x,y,z], mm } nội suy easeIO giữa các mốc (chuyển động liên tục, có easing)
export function camRig(W, H, keys) {
  const cam = new THREE.PerspectiveCamera(fovOf(keys[0].mm || 35), W / H, 0.05, 400);
  const at = (t) => {
    let i = 0; while (i < keys.length - 2 && t > keys[i + 1].t) i++;
    const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)], u = b.t > a.t ? easeIO((t - a.t) / (b.t - a.t)) : 0;
    const P = a.p.map((v, k) => lerp(v, b.p[k], u)), L = a.l.map((v, k) => lerp(v, b.l[k], u)), mm = lerp(a.mm || 35, b.mm || 35, u);
    cam.position.set(...P); cam.lookAt(...L); cam.fov = fovOf(mm); cam.updateProjectionMatrix();
  };
  at(0); return { cam, at };
}

// Bóng người vô danh (không mặt): thân, đầu, tay chân; mũ chóp (người thắp đèn) hoặc không. Trả { root, set(pose) }.
export function figure({ color = '#16110f', hat = false, seated = false, scale = 1, rim } = {}) {
  const m = lam(color), root = new THREE.Group(), s = scale;
  const torso = cyl(0.17 * s, 0.21 * s, 0.62 * s, m, 0, (seated ? 0.72 : 1.18) * s, 0, root);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.12 * s, 16, 12), m); head.position.set(0, (seated ? 1.16 : 1.62) * s, 0); root.add(head);
  if (hat) { cyl(0.11 * s, 0.11 * s, 0.2 * s, m, 0, 1.82 * s, 0, root); cyl(0.19 * s, 0.19 * s, 0.025 * s, m, 0, 1.72 * s, 0, root); }
  const armL = new THREE.Group(), armR = new THREE.Group(); armL.position.set(-0.2 * s, (seated ? 0.98 : 1.44) * s, 0); armR.position.set(0.2 * s, (seated ? 0.98 : 1.44) * s, 0);
  cyl(0.045 * s, 0.04 * s, 0.6 * s, m, 0, -0.3 * s, 0, armL); cyl(0.045 * s, 0.04 * s, 0.6 * s, m, 0, -0.3 * s, 0, armR); root.add(armL, armR);
  const legL = new THREE.Group(), legR = new THREE.Group(); legL.position.set(-0.09 * s, (seated ? 0.45 : 0.86) * s, 0); legR.position.set(0.09 * s, (seated ? 0.45 : 0.86) * s, 0);
  cyl(0.06 * s, 0.05 * s, 0.84 * s, m, 0, -0.42 * s, 0, legL); cyl(0.06 * s, 0.05 * s, 0.84 * s, m, 0, -0.42 * s, 0, legR); root.add(legL, legR);
  if (seated) { legL.rotation.x = legR.rotation.x = -1.45; }
  root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = false; } });
  const set = ({ armL: aL = 0, armR: aR = 0, walk = 0, headTilt = 0 } = {}) => {
    armL.rotation.x = aL; armR.rotation.x = aR; head.rotation.x = headTilt;
    if (!seated) { legL.rotation.x = Math.sin(walk) * 0.45; legR.rotation.x = -Math.sin(walk) * 0.45; }
  };
  return { root, set, armL, armR, head, torso };
}

// Đèn khí thắp được: buildGasLamp của tập 1 + quầng sáng + đèn điểm; lit(u) 0..1, thở ±4 %.
export function gasLamp(scene, x, z, { h = 3.4, lit = 1 } = {}) {
  const g = buildGasLamp({ height: h }); g.position.set(x, 0, z); scene.add(g);
  const pl = new THREE.PointLight('#ffae5c', 0, 14, 1.6); pl.position.set(x, h - 0.3, z); pl.castShadow = false; scene.add(pl);
  const sp = glowSprite('#ffb468', 1.0, 2.6); sp.position.set(x, h - 0.3, z); scene.add(sp);
  const set = (u, f = 0) => { const k = Math.max(0, Math.min(1, u)) * (1 + 0.04 * (0.6 * Math.sin(f * 0.21) + 0.4 * Math.sin(f * 0.083 + 1.3)));
    pl.intensity = 9 * k; sp.material.opacity = 0.95 * k; sp.scale.setScalar(2.6 * (0.6 + 0.4 * k)); };
  set(lit); return { group: g, light: pl, sprite: sp, set };
}

// Hạt bụi trong vùng sáng (chuyển động liên tục mỗi khung → không đứng hình)
export function dust(scene, center, size, n = 260, seed = 7, color = '#ffd9a8') {
  const R = rng(seed), pos = new Float32Array(n * 3), base = [];
  for (let i = 0; i < n; i++) { base.push([(R() - 0.5) * size[0], (R() - 0.5) * size[1], (R() - 0.5) * size[2], R() * 6.28]); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({ color, size: 0.018, transparent: true, opacity: 0.55, depthWrite: false })); scene.add(pts);
  const update = (t) => { base.forEach((b, i) => { pos[i * 3] = center[0] + b[0] + 0.05 * Math.sin(t * 0.3 + b[3]); pos[i * 3 + 1] = center[1] + ((b[1] + t * 0.02 + size[1] * 0.5) % size[1]) - size[1] * 0.5;
    pos[i * 3 + 2] = center[2] + b[2] + 0.05 * Math.cos(t * 0.25 + b[3]); }); geo.attributes.position.needsUpdate = true; };
  update(0); return { update };
}

// Kết cấu canvas nhỏ (chữ, ô, giấy) cho màn hình/áp phích tự thiết kế
export function canvasTex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}

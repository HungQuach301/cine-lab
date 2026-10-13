// KÊNH 2 · module hình k2v — đồ nghề chung (three.js trong Chromium headless + SwiftShader).
// Nhận diện channel-k2/NHAN-DIEN.md: mực #0F1722, chữ #EEF1F4, thép #9AA7B5, cam #F08A4B (Mỹ/nhấn), lục lam #3CC2B0, hổ phách #F2C14E (dự báo).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { glowSprite, rng } from '/cong3/dir-C/common.js';
export { THREE, glowSprite, rng };

export const C = { ink: '#0F1722', ink2: '#16212f', text: '#EEF1F4', steel: '#9AA7B5', orange: '#F08A4B', teal: '#3CC2B0', amber: '#F2C14E', dim: '#B9C3CE' };
export const cl = (u) => Math.max(0, Math.min(1, u));
export const ease = (u) => { u = cl(u); return u * u * (3 - 2 * u); };
export const easeIO = (u) => { u = cl(u); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
export const eo = (u) => { u = cl(u); return 1 - Math.pow(1 - u, 3); };
export const lerp = (a, b, u) => a + (b - a) * u;
export const fovOf = (mm) => 2 * Math.atan(12 / mm) * 180 / Math.PI;
// cửa sổ thời gian [t0, t1] (giây trong cảnh) → 0..1; số đơn → bật sau t (0,6 s); -1/âm = có sẵn từ đầu
export const win = (w, t, d = 0.6) => { if (w === undefined || w === null) return 1; if (typeof w === 'number') return w < 0 ? 1 : ease((t - w) / d); return ease((t - w[0]) / Math.max(0.01, w[1] - w[0])); };

// Mốc máy quay {u|t, …}: u tính theo dur. Trả hàm (t) → mốc nội suy (easeIO giữa hai mốc). f(a, b, u) nội suy từng trường.
export function keyTrack(keys, dur, f) {
  const K = keys.map((k) => ({ ...k, t: k.t !== undefined ? k.t : (k.u || 0) * dur })).sort((a, b) => a.t - b.t);
  return (t) => { if (K.length === 1 || t <= K[0].t) return f(K[0], K[0], 0); let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], u = b.t > a.t ? easeIO((t - a.t) / (b.t - a.t)) : 1; return f(a, b, u); };
}
// Máy quay kiểu kit.js: {p:[x,y,z], l:[x,y,z], mm}
export function camRig(W, H, keys, dur) {
  const cam = new THREE.PerspectiveCamera(fovOf(keys[0].mm || 35), W / H, 0.05, 2000);
  const tr = keyTrack(keys, dur, (a, b, u) => ({ p: a.p.map((v, k) => lerp(v, b.p[k], u)), l: a.l.map((v, k) => lerp(v, b.l[k], u)), mm: lerp(a.mm || 35, b.mm || 35, u) }));
  const at = (t) => { const k = tr(t); cam.position.set(...k.p); cam.lookAt(...k.l); cam.fov = fovOf(k.mm); cam.updateProjectionMatrix(); };
  at(0); return { cam, at };
}

// Kết cấu canvas (sRGB)
export function canvasTex(w, h, draw, { srgb = true, aniso = 8 } = {}) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace; t.anisotropy = aniso; t.needsUpdate = true; return t;
}
export const loadImg = (src) => new Promise((ok, ko) => { const im = new Image(); im.onload = () => ok(im); im.onerror = () => ko(new Error('không tải được ảnh ' + src)); im.src = src; });
export const loadJSON = async (src) => { const r = await fetch(src); if (!r.ok) throw new Error('không tải được ' + src); return r.json(); };

// Phòng studio tối cho đồ hoạ thông tin: sàn bóng mờ có lưới mảnh, tường cong (cyclorama) chuyển sắc, đèn chính + viền + nền.
// Không mờ: nền là cảnh thật có chiều sâu (yêu cầu "nền cảnh không mờ").
export function studio(scene, { size = 160, floor = '#0a0e15', wall = '#101824', grid = 4, key = [-14, 22, 16], tint = '#9fb6d8', pool = [0, 6, -14] } = {}) {
  scene.background = new THREE.Color('#070a10');
  const ft = canvasTex(2048, 2048, (g, w, h) => { g.fillStyle = floor; g.fillRect(0, 0, w, h);
    const R = rng(11); for (let i = 0; i < 30000; i++) { g.fillStyle = `rgba(255,255,255,${0.008 + 0.014 * R()})`; g.fillRect(R() * w, R() * h, 1.2, 1.2); }
    const n = Math.round(size / grid); g.strokeStyle = 'rgba(154,167,181,0.10)'; g.lineWidth = 1.6; for (let i = 0; i <= n; i++) { const x = i * w / n; g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); g.beginPath(); g.moveTo(0, x); g.lineTo(w, x); g.stroke(); } });
  ft.wrapS = ft.wrapT = THREE.RepeatWrapping; ft.repeat.set(12, 12);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(size * 12, size * 12), new THREE.MeshPhysicalMaterial({ map: ft, roughness: 0.78, metalness: 0.0, specularIntensity: 0.22, envMapIntensity: 0.12 })   /* sàn đen nhưng góc sượt phản xạ gương mạnh (Fresnel) → xám bạc; giảm specular */);
  fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; scene.add(fl);
  // tường cong (cyclorama) bao ba phía, đủ rộng để không lộ mép ở mọi preset máy quay
  const r = 12, d = size * 0.18, geo = new THREE.BufferGeometry(), P = [], I = [], prof = [[-d, 0]];
  for (let i = 1; i <= 16; i++) { const a = (i / 16) * Math.PI / 2; prof.push([-d - Math.sin(a) * r, r - Math.cos(a) * r]); } prof.push([-d - r, size * 1.5]);
  prof.forEach(([z, y], j) => { P.push(-size * 6, y, z, size * 6, y, z);   // 13/10: ±1,5·size lộ đầu mút tường (khối đen góc bo) khi máy nhìn dọc tường (K2C-T1-06 ch_pew, ch_terner)
    if (j) { const b = (j - 1) * 2; I.push(b, b + 1, b + 2, b + 1, b + 3, b + 2); } });
  geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); geo.setIndex(I); geo.computeVertexNormals();
  const wl = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: wall, roughness: 0.95, side: THREE.DoubleSide, envMapIntensity: 0.2 })); wl.receiveShadow = true; scene.add(wl);
  // vũng sáng mềm trên tường sau (chiều sâu, tách chủ thể khỏi nền)
  const pt = canvasTex(512, 512, (g, w, h) => { const gr = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, 'rgba(70,96,140,0.55)'); gr.addColorStop(0.5, 'rgba(40,58,90,0.22)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const pl = new THREE.Mesh(new THREE.PlaneGeometry(70, 40), new THREE.MeshBasicMaterial({ map: pt, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false }));
  pl.position.set(pool[0], pool[1] + 8, -d - r + 0.2); scene.add(pl);
  const hemi = new THREE.HemisphereLight('#b7c8e6', '#1a1610', 0.35); scene.add(hemi);
  const K = new THREE.DirectionalLight('#fff3e2', 1.7); K.position.set(...key); K.castShadow = true; K.shadow.mapSize.set(2048, 2048);
  Object.assign(K.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30, near: 1, far: 140 }); K.shadow.bias = -0.0005; K.shadow.radius = 4; scene.add(K);
  const rim = new THREE.DirectionalLight(tint, 1.6); rim.position.set(20, 14, -24); scene.add(rim);
  return { floor: fl, wall: wl, key: K, rim, hemi, pool: pl };
}

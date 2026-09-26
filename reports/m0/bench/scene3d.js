// Cảnh mẫu M0 — phong cách (b) 2.5D three.js (WebGL, SwiftShader CPU trong Chromium headless).
import * as THREE from './node_modules/three/build/three.module.js';

let S, M, renderer, scene, camera, acc, actx, rig, lampLight, W, H;
const U = 0.32; // mét trên 1 H (nhân vật cao 5,6 H ≈ 1,8 m)

function lcg(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0, ...o });

function limb(len, w, color) {
  // Bộ phận treo từ khớp gốc hướng xuống -y.
  const g = new THREE.CapsuleGeometry(w / 2, Math.max(0.001, len - w), 6, 12);
  g.translate(0, -len / 2 + 0, 0);
  const m = new THREE.Mesh(g, mat(color)); m.castShadow = true; return m;
}

function buildCharacter() {
  const root = new THREE.Group(), hip = new THREE.Group(); root.add(hip);
  const T = M.torso, tl = T.length * U;
  const torsoGeo = new THREE.CylinderGeometry(T.top_width * U / 2, T.bottom_width * U / 2, tl, 20, 1);
  const torso = new THREE.Mesh(torsoGeo, mat(T.color)); torso.position.y = tl / 2; torso.scale.z = 0.6; torso.castShadow = true; hip.add(torso);
  const neck = limb(M.neck.length * U + 0.05, M.neck.width * U, M.neck.color); neck.position.y = tl + M.neck.length * U; hip.add(neck);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.5, 24, 16), mat(M.head.color));
  head.scale.set(M.head.width * U, M.head.length * U, M.head.width * U * 0.95);
  const hcY = tl + M.neck.length * U + M.head.length * U / 2; head.position.y = hcY; head.castShadow = true; hip.add(head);
  const brim = new THREE.Mesh(new THREE.CylinderGeometry(M.hat.width * U / 2, M.hat.width * U / 2, 0.03, 24), mat(M.hat.color));
  brim.position.y = hcY + M.head.length * U * 0.3; hip.add(brim);
  const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.4 * U, 0.42 * U, M.hat.length * U, 20), mat(M.hat.color));
  crown.position.y = brim.position.y + M.hat.length * U / 2; crown.castShadow = true; hip.add(crown);
  const chain = (parent, y, z, p1, p2, end, dark) => {
    const j1 = new THREE.Group(); j1.position.set(0, y, z); parent.add(j1);
    const a = limb(p1.length * U, p1.width * U, dark ? '#3b2219' : p1.color); j1.add(a);
    const j2 = new THREE.Group(); j2.position.y = -p1.length * U; j1.add(j2);
    const b = limb(p2.length * U, p2.width * U, dark ? '#3b2219' : p2.color); j2.add(b);
    const e = new THREE.Group(); e.position.y = -p2.length * U; j2.add(e);
    if (end) e.add(end);
    return [j1, j2, e];
  };
  const foot = () => { const f = new THREE.Mesh(new THREE.BoxGeometry(M.foot.length * U, M.foot.width * U, 0.1), mat(M.foot.color)); f.position.set(M.foot.length * U * 0.3, -0.02, 0); f.castShadow = true; return f; };
  const hand = () => { const h = new THREE.Mesh(new THREE.SphereGeometry(M.hand.width * U / 2, 12, 8), mat(M.hand.color)); return h; };
  const legF = chain(hip, 0, 0.1, M.thigh, M.shin, foot());
  const legB = chain(hip, 0, -0.1, M.thigh, M.shin, foot(), true);
  const sy = tl - M.joints.shoulder_from_torso_top * U;
  const armF = chain(hip, sy, 0.2, M.upper_arm, M.forearm, hand());
  const armB = chain(hip, sy, -0.2, M.upper_arm, M.forearm, hand(), true);
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, M.pole.length * U, 8), mat(M.pole.color));
  pole.position.y = M.pole.length * U * 0.25; pole.rotation.z = -0.35; armF[2].add(pole);
  return { root, hip, legF, legB, armF, armB };
}

function build() {
  const r = lcg(7);
  scene = new THREE.Scene();
  scene.background = new THREE.Color('#3a2540');
  scene.fog = new THREE.Fog('#5a3550', 12, 70);
  // Trời: tấm phông gradient xa.
  const skyC = document.createElement('canvas'); skyC.width = 4; skyC.height = 256; const sg = skyC.getContext('2d');
  const gr = sg.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#1b1830'); gr.addColorStop(0.6, '#5a3550'); gr.addColorStop(0.85, '#c0664a'); gr.addColorStop(1, '#2a1a22');
  sg.fillStyle = gr; sg.fillRect(0, 0, 4, 256);
  const skyTex = new THREE.CanvasTexture(skyC); skyTex.colorSpace = THREE.SRGBColorSpace;
  const sky = new THREE.Mesh(new THREE.PlaneGeometry(400, 90), new THREE.MeshBasicMaterial({ map: skyTex, fog: false }));
  sky.position.set(0, 20, -120); scene.add(sky);
  // Lớp xa: silhouette phẳng.
  const farMat = new THREE.MeshBasicMaterial({ color: S.layers[0].color });
  for (let x = -60; x < 120; x += 2 + r() * 3) { const h = 6 + r() * 10, w = 2 + r() * 4; const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), farMat); m.position.set(x, h / 2, -45); scene.add(m); }
  // Lớp giữa: nhà khối có cửa sổ phát sáng.
  const wallMat = mat(S.layers[1].color), winOn = new THREE.MeshBasicMaterial({ color: '#e89a4a' }), winOff = mat('#1a1520');
  for (let x = -12; x < 40; x += 3.2 + r() * 1.5) {
    const w = 2.6 + r() * 1.2, h = 3.5 + r() * 2.5, d = 3;
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wallMat); b.position.set(x, h / 2, -4.5); b.receiveShadow = true; scene.add(b);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(w * 0.75, 1.2, 4), wallMat); roof.rotation.y = Math.PI / 4; roof.position.set(x, h + 0.6, -4.5); scene.add(roof);
    for (let wy = 0.9; wy < h - 0.6; wy += 0.9) for (let wx = -w / 2 + 0.5; wx < w / 2 - 0.3; wx += 0.8) {
      const on = r() < 0.45; const q = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.45), on ? winOn : winOff);
      q.position.set(x + wx, wy, -4.5 + d / 2 + 0.01); scene.add(q);
    }
  }
  // Mặt đường.
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 30), mat('#2b2128', { roughness: 0.6 }));
  ground.rotation.x = -Math.PI / 2; ground.position.z = 0; ground.receiveShadow = true; scene.add(ground);
  // Cột đèn khí + nguồn sáng ấm duy nhất (point light có bóng đổ).
  const lx = S.light.world_x / 100 - 9.6 + 3;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 3.4, 10), mat('#15111a')); post.position.set(lx, 1.7, -1.2); scene.add(post);
  const bulb = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.4, 0.28), new THREE.MeshBasicMaterial({ color: '#ffd08a' })); bulb.position.set(lx, 3.55, -1.2); scene.add(bulb);
  lampLight = new THREE.PointLight(S.light.color, 40, 18, 1.6); lampLight.position.set(lx, 3.5, -1.0);
  lampLight.castShadow = true; lampLight.shadow.mapSize.set(1024, 1024); lampLight.shadow.bias = -0.002; scene.add(lampLight);
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color: '#ffb45a', blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
  glow.scale.set(4, 4, 1); glow.position.copy(bulb.position); scene.add(glow);
  scene.add(new THREE.HemisphereLight('#6a5a9a', '#1a1018', 0.35));
  // Lớp gần: cột và hàng rào tiền cảnh.
  const nearMat = mat(S.layers[2].color);
  for (let x = -8; x < 60; x += 5 + r() * 4) {
    if (r() < 0.5) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.3, 8, 0.3), nearMat); p.position.set(x, 4, 3.2); scene.add(p); }
    else for (let i = 0; i < 5; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.0, 0.08), nearMat); p.position.set(x + i * 0.3, 0.5, 3.0); scene.add(p); }
  }
  rig = buildCharacter(); scene.add(rig.root);
  camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 300);
}

function glowTex() {
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
}

function pose(t) {
  const C = S.character, ph = t * C.step_hz * Math.PI * 2, s = Math.sin(ph);
  const x0 = -10.5, x1 = 17.5; // đi qua khung từ trái sang phải
  const x = x0 + (x1 - x0) * (t / S.duration_s);
  const legLen = (M.thigh.length + M.shin.length + M.foot.width) * U;
  rig.root.position.set(x, legLen * 0.97 - Math.abs(Math.cos(ph)) * 0.02, 0);
  rig.legF[0].rotation.z = 0.42 * s; rig.legF[1].rotation.z = -Math.max(0, 0.7 * Math.sin(ph + 1.2));
  rig.legB[0].rotation.z = -0.42 * s; rig.legB[1].rotation.z = -Math.max(0, -0.7 * Math.sin(ph + 1.2));
  rig.armF[0].rotation.z = 0.12 - 0.05 * s; rig.armF[1].rotation.z = 0.9;
  rig.armB[0].rotation.z = 0.35 * s; rig.armB[1].rotation.z = 0.35;
  const cx = 3 + t * 0.6; camera.position.set(cx, 1.6, 14); camera.lookAt(cx, 1.5, 0);
}

window.setup = function (sceneCfg, sheet) {
  S = sceneCfg; M = sheet; W = S.width; H = S.height;
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  renderer = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(W, H, false); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
  window._gl = cv;
  acc = document.getElementById('c'); acc.width = W; acc.height = H; actx = acc.getContext('2d');
  build();
};

window.renderFrame = function (f, samples, fmt) {
  const t0 = performance.now(), sh = S.motion_blur.shutter;
  for (let s = 0; s < samples; s++) {
    const off = samples === 1 ? 0 : sh * ((s + 0.5) / samples - 0.5);
    pose((f + off) / S.fps); renderer.render(scene, camera);
    actx.globalAlpha = 1 / (s + 1); actx.drawImage(window._gl, 0, 0);
  }
  actx.globalAlpha = 1;
  const t1 = performance.now();
  const url = acc.toDataURL(fmt || 'image/png');
  return { url, draw_ms: t1 - t0, encode_ms: performance.now() - t1 };
};
window.ready = true;

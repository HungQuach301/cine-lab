// Cine Lab · Cổng 7 THỬ MẶT — BIẾN THỂ V1 (three.js trong đường ống hiện có). Nhánh thu-mat, KHÔNG merge.
// Bật: page.js setup({ dbg: { thuMat: 'v1' } }) → globalThis.CINE_THU_MAT = 'v1' (vật liệu da/mắt V1 trong bl_head.js) + install() dưới đây.
// Không bật → không nạp file này, không đổi gì (0 px).
//
// Mỗi khung (gọi SAU cur.update và sau khi page.js đặt uExp):
//  1. ÁNH DỘI TỪ NGUỒN CÓ THẬT: chụp môi trường cảnh (CubeCamera 128 px tại tâm đầu Ida, ẩn chính Ida) → PMREM → envMap cho da và giác mạc.
//     Không thêm đèn: chỉ là ánh của chính tường vôi, khăn, lồng đèn, trời… trong cảnh. Da nhận 30 % phần khuếch tán (đèn phụ facelight đã
//     có phần dội chính) + phản xạ gương đủ (Fresnel → ánh ướt ở góc sượt); giác mạc phản chiếu đủ → điểm sáng đúng vị trí nguồn thật.
//     Chụp lại MỖI khung (hàm thuần theo khung: không trạng thái ẩn giữa các khung).
//  2. PHƠI SÁNG / CUỘN SÁNG DA theo shot (bảng SHOT): s03 hạ phơi sáng sau khi L4 bắt lửa (thích nghi 0,4 s) + cuộn sáng da mềm.
//  3. VI CHUYỂN ĐỘNG MẶT trên kênh facerig có sẵn (không đổi hình khối): liếc/saccade, mí theo hướng nhìn, mày trôi chậm + nhấn theo lời,
//     má–mắt cùng miệng khi nói, thở (môi hé theo nhịp khi im), chớp bổ sung không đều (một phần chớp nửa). Cộng lên trọng số của shot.
export const SHOT = {
  s03: { expo: { at: 9.2, dur: 0.4, k: 0.5 }, knee: 0.4, cap: 1.0, blinks: [[8.95, 1], [10.15, 0.55]] },
  s05: { blinks: [[12.42, 0.5]] },
  s22: {},
};

function rng(seed) { let s = 0; for (const c of seed) s = (s * 31 + c.charCodeAt(0)) >>> 0; s = s || 1; return () => ((s = (s * 16807) % 2147483647) / 2147483647); }
const sstep = (a, b, x) => { const t = Math.max(0, Math.min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const blinkCurve = (T, b, s = 1) => { const d = T - b; return d < 0 ? 0 : d < 0.07 ? d / 0.07 : d < 0.1 ? 1 : d < 0.24 ? 1 - (d - 0.1) / 0.14 : 0; };
// nhiễu 1D mượt (giá trị ngẫu nhiên tại mắt lưới 1/f s, nội suy cosin), theo hạt giống
function noise1(seed, freq) { const r = rng(seed), v = Array.from({ length: 512 }, () => r() * 2 - 1);
  return (T) => { const x = T * freq, i = Math.floor(x), f = x - i, u = (1 - Math.cos(Math.PI * f)) / 2, a = v[((i % 512) + 512) % 512], b = v[(((i + 1) % 512) + 512) % 512]; return a + (b - a) * u; }; }

export function install({ THREE, renderer, cur, shot, dbg = {} }) {
  const ida = cur.named && cur.named.ida; if (!ida) return null;
  const cfg = { ...(SHOT[shot.id] || {}), ...(dbg.thuShot || {}) }, noEnv = !!dbg.thuNoEnv, noMotion = !!dbg.thuNoMotion;
  const mats = []; ida.root.traverse((o) => { if (o.isMesh && o.material && o.material.userData && o.material.userData.thuMat && !mats.includes(o.material)) mats.push(o.material); });
  const skin = mats.find((m) => m.userData.thuMat === 'skin');
  if (skin && cfg.knee) { skin.userData.U.uKnee.value = cfg.knee; skin.userData.U.uCap.value = cfg.cap ?? 1.8; }
  // ---- 1. môi trường thật tại đầu ----
  const cubeRT = new THREE.WebGLCubeRenderTarget(128, { type: THREE.HalfFloatType }), cubeCam = new THREE.CubeCamera(0.05, 400, cubeRT);
  const pmrem = new THREE.PMREMGenerator(renderer); let envRT = null;
  function captureEnv() {
    const H = ida.H, head = ida.joints.head; head.updateWorldMatrix(true, false);
    const c = head.localToWorld(new THREE.Vector3(0, 0.5 * H, 0.15 * H)); cubeCam.position.copy(c);
    const vis = ida.root.visible; ida.root.visible = false;
    const prevRT = renderer.getRenderTarget(), tm = renderer.toneMapping; renderer.toneMapping = THREE.NoToneMapping;
    cubeCam.update(renderer, cur.scene); ida.root.visible = vis;
    envRT = pmrem.fromCubemap(cubeRT.texture, envRT); renderer.setRenderTarget(prevRT); renderer.toneMapping = tm;
    for (const m of mats) { if (m.envMap !== envRT.texture) { m.envMap = envRT.texture; m.needsUpdate = true; } m.envMapIntensity = 1; }
  }
  // ---- 3. vi chuyển động ----
  const face = ida.face, eyes = (face && face.eyes) || [];
  let base = {}; const orig = ida.setFace; if (face && !noMotion) ida.setFace = (w) => { base = { ...(w || {}) }; };
  if (face && face.getFace) base = { ...face.getFace() };
  const r = rng('thu-mat-' + shot.id), sac = [];
  { let T = shot.t0 + 0.15 + r() * 0.3; while (T < shot.t1) { sac.push([T, (r() * 2 - 1) * 0.035, (r() * 2 - 1) * 0.015]); T += 0.3 + r() * 0.85; } }   // 0,3–1,15 s; ±2°/±0,9°
  const nBrow = noise1('brow' + shot.id, 0.7), nBrow2 = noise1('brow2' + shot.id, 0.45), nSm = noise1('sm' + shot.id, 0.35);
  const blinks = [...(cfg.blinks || [])];
  let eyeLast = null;
  function motion(T) {
    // saccade: bước nhảy nhanh 2 khung giữa các điểm dừng
    let yaw = 0, pit = 0; for (let i = 0; i < sac.length; i++) { const [ts, y, p] = sac[i]; const u = sstep(ts, ts + 2 / 24, T); if (u <= 0) break;
      const py = i ? sac[i - 1][1] : 0, pp = i ? sac[i - 1][2] : 0; yaw = py + (y - py) * u; pit = pp + (p - pp) * u; }
    // mắt: bỏ lệch khung trước nếu không ai đặt lại (shot không có faceRig), rồi cộng lệch mới
    if (eyes.length) { if (eyeLast && eyes.every((e, i) => Math.abs(e.rotation.x - eyeLast[i][0]) < 1e-9 && Math.abs(e.rotation.y - eyeLast[i][1]) < 1e-9)) eyes.forEach((e, i) => { e.rotation.x -= eyeLast[i][2]; e.rotation.y -= eyeLast[i][3]; });
      eyes.forEach((e) => { e.rotation.x += pit; e.rotation.y += yaw; }); eyeLast = eyes.map((e) => [e.rotation.x, e.rotation.y, pit, yaw]); }
    if (!face || noMotion) return;
    const gzP = eyes.length ? eyes[0].rotation.x : 0;   // + = nhìn xuống
    const w = { ...base }, add = (k, v) => { w[k] = (w[k] || 0) + v; };
    const mouthE = Math.min(1, (base.jawOpen || 0) * 2 + 0.5 * ((base.pucker || 0) + (base.wide || 0)));
    add('lidDrop', 0.45 * Math.max(0, gzP - 0.02));                                 // mí trên theo mắt nhìn xuống
    add('browInnerUp', 0.05 * Math.max(0, nBrow(T)) + 0.06 * mouthE); add('browUp', 0.04 * Math.max(0, nBrow2(T)) + 0.05 * mouthE); add('browDown', 0.04 * Math.max(0, -nBrow2(T)));
    add('cheekRaise', 0.12 * mouthE); add('squint', 0.06 * mouthE + 0.03 * Math.max(0, nSm(T))); add('smile', 0.03 * nSm(T));
    if (mouthE < 0.05) add('jawOpen', 0.02 + 0.02 * Math.sin(2 * Math.PI * (T - shot.t0) / 3.4));   // thở: môi hé theo nhịp khi im
    let bk = 0; for (const [b, s] of blinks) bk = Math.max(bk, s * blinkCurve(T, b)); if (bk > 0) w.blink = Math.max(w.blink || 0, bk);
    const o = {}; for (const [k, v] of Object.entries(w)) { const c = Math.max(0, Math.min(1, v)); if (c > 0.004) o[k] = +c.toFixed(3); }
    orig(o);
  }
  return {
    frame(t, T, f, uExp) {
      if (cfg.expo) uExp.value *= 1 - (1 - cfg.expo.k) * sstep(cfg.expo.at, cfg.expo.at + cfg.expo.dur, T);
      motion(T);
      if (!noEnv) captureEnv();
    },
  };
}

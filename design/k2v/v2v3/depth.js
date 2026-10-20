// NC-V2V3 · BẢN ĐỒ ĐỘ SÂU TỪ CHÍNH RENDERER — nối vào cuối bản sao trang dựng V7B (cùng idmask.js của NC-V2V), dùng biến mô-đun (scene, cam, R, C, ctx).
// Gọi SAU window.renderFrame(f) (trạng thái cảnh/máy/năm/nắng đúng khung đó): dựng lại cảnh vào một đích có DepthTexture (float) — mọi shader tự dời đỉnh
// (địa hình, nước, cờ bay, bản sao) ghi độ sâu thật của chúng — rồi đổi z bộ đệm → khoảng cách mắt tuyến tính (m), mã hoá log 16 bit:
//   v = ln(z / ZN) / ln(ZF / ZN) (ZN 1 m, ZF 60 km), 0 = gần, 65535 = xa/trời (độ sâu bộ đệm = 1). PNG RGB: R = 8 bit cao, G = 8 bit thấp, B = 255 nếu trời.
const V2V3_ZN = 1.0, V2V3_ZF = 60000.0;
let v2v3D = null;
window.v2v3Depth = (scale) => {
  const w = Math.round(C.W * (scale || 1)), h = Math.round(C.H * (scale || 1));
  if (!v2v3D || v2v3D.w !== w) {
    const rt = new THREE.WebGLRenderTarget(w, h, { depthBuffer: true }); rt.depthTexture = new THREE.DepthTexture(w, h); rt.depthTexture.type = THREE.FloatType;
    const out = new THREE.WebGLRenderTarget(w, h, { type: THREE.FloatType });
    const mat = new THREE.ShaderMaterial({ uniforms: { tD: { value: rt.depthTexture }, n: { value: 1 }, fr: { value: 1 } },
      vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
      fragmentShader: 'uniform sampler2D tD; uniform float n, fr; varying vec2 vUv; void main(){ float d = texture2D(tD, vUv).x; float zn = d * 2.0 - 1.0; float z = 2.0 * n * fr / (fr + n - zn * (fr - n)); gl_FragColor = vec4(z, d, 0.0, 1.0); }' });
    const sc = new THREE.Scene(); sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mat)); v2v3D = { w, h, rt, out, mat, sc, oc: new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1) };
  }
  const D = v2v3D, cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(), nu = R.shadowMap.needsUpdate;
  R.shadowMap.needsUpdate = false; R.setRenderTarget(D.rt); R.setClearColor(0x000000, 1); R.clear(); R.render(scene, cam);
  D.mat.uniforms.n.value = cam.near; D.mat.uniforms.fr.value = cam.far; R.setRenderTarget(D.out); R.render(D.sc, D.oc);
  const px = new Float32Array(w * h * 4); R.readRenderTargetPixels(D.out, 0, 0, w, h, px); R.setRenderTarget(null); R.setClearColor(cc, ca); R.shadowMap.needsUpdate = nu;
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'), im = g.createImageData(w, h), L = Math.log(V2V3_ZF / V2V3_ZN);
  let zmin = 1e9, zmax = 0, nsky = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = ((h - 1 - y) * w + x) * 4, o = (y * w + x) * 4, sky = px[i + 1] >= 0.999999;
    const z = sky ? V2V3_ZF : Math.min(V2V3_ZF, Math.max(V2V3_ZN, px[i])); const v = Math.round(Math.log(z / V2V3_ZN) / L * 65535);
    if (sky) nsky++; else { zmin = Math.min(zmin, z); zmax = Math.max(zmax, z); }
    im.data[o] = v >> 8; im.data[o + 1] = v & 255; im.data[o + 2] = sky ? 255 : 0; im.data[o + 3] = 255; }
  g.putImageData(im, 0, 0);
  cam.updateMatrixWorld(); return { w, h, near: cam.near, far: cam.far, fov: cam.fov, aspect: cam.aspect, mw: cam.matrixWorld.elements.slice(), zmin: +zmin.toFixed(2), zmax: +zmax.toFixed(1), sky_pct: +(nsky / (w * h) * 100).toFixed(2), png_b64: cv.toDataURL('image/png').slice(22) };
};

// MÁI NHÀ PHỐ (cho chế độ B): lượt riêng chỉ địa hình + mesh do makeCity tạo (KHÔNG gồm công sự/trại/phế tích/mốc/nhà hero), uMask = 1 → đỏ.
// Mái = điểm thuộc lượt này VÀ pháp tuyến thế giới hướng lên (tính từ bản đồ độ sâu ở bước sau, ctrl3.py). Gọi sau renderFrame(f).
let v2v3CRT = null;
const V2V3_KHONG_PHO = ['fortify', 'camps', 'ruins', 'footprints', 'frontLines', 'fence', 'phaseMaps', 'landmarks', 'makeHeroes', 'batteryV6', 'batteryGroup', 'makeFleet', 'makeShips', 'shipFlags', 'flags', 'lamps'];
window.v2v3City = (scale) => {
  const w = Math.round(C.W * (scale || 1)), h = Math.round(C.H * (scale || 1)); if (!v2v3CRT || v2v3CRT.width !== w) v2v3CRT = new THREE.WebGLRenderTarget(w, h);
  const all = []; scene.traverse((o) => { if ((o.isMesh || o.isSprite || o.isPoints || o.isInstancedMesh) && o.visible) all.push(o); });
  const terr = new Set(); ctx.terr.group.traverse((o) => terr.add(o));
  const fnOf = (o) => { const out = []; for (let p = o; p; p = p.parent) if (p.userData && p.userData.v2vFn) out.push(...p.userData.v2vFn); return out; };
  const isCity = (o) => { const fn = fnOf(o); return fn.includes('makeCity') && !V2V3_KHONG_PHO.some((n) => fn.includes(n)) && !v2vMatFlag(o); };
  const U = ctx.U, sm = R.shadowMap.enabled, cc = R.getClearColor(new THREE.Color()), ca = R.getClearAlpha(), wv = ctx.ws.water.visible, sv = ctx.ws.sky.visible;   // đọc TRƯỚC khi ẩn (lỗi lượt đầu: đọc sau → nước/trời bị tắt vĩnh viễn)
  const hid = all.filter((o) => !(terr.has(o) || isCity(o))); for (const o of hid) o.visible = false;
  U.uMask.value = 1; ctx.ws.water.visible = ctx.ws.sky.visible = false; R.shadowMap.enabled = false; R.setClearColor(0x000000, 1);
  R.setRenderTarget(v2v3CRT); R.clear(); R.render(scene, cam); const px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(v2v3CRT, 0, 0, w, h, px); R.setRenderTarget(null);
  for (const o of hid) o.visible = true; U.uMask.value = 0; ctx.ws.water.visible = wv; ctx.ws.sky.visible = sv; R.shadowMap.enabled = sm; R.setClearColor(cc, ca);
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d'), im = g.createImageData(w, h); let n = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = ((h - 1 - y) * w + x) * 4, o = (y * w + x) * 4, red = px[i] > 128 && px[i + 1] < 90; if (red) n++; im.data[o] = im.data[o + 1] = im.data[o + 2] = red ? 255 : 0; im.data[o + 3] = 255; }
  g.putImageData(im, 0, 0); return { pct: +(n / (w * h) * 100).toFixed(3), png_b64: cv.toDataURL('image/png').slice(22) };
};

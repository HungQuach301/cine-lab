// K2V tl · CÔNG TRÌNH BIỂU TƯỢNG (lớp 1 chuẩn hình) — dựng chi tiết riêng theo số đo có nguồn (design/k2v/tl/heroes/*.json):
//  · Tower of Homage (Moorish Castle): vòng chân OSM way 950058970 (334 m², nguồn ghi 320 m² — lệch 4 %), cao 23 m (Ministry for Heritage, Gibraltar);
//    tường tapia (lớp đầm ~0,85 m, lỗ giằng ván), lỗ châu mai, răng cưa đỉnh; tường thành lâu đài (OSM barrier=city_wall).
//  · Đường băng 09/27 cắt ngang đường vào: tim OSM way 157316482 (1 798 × 45 m); có từ 1941 (HMGoG 177/2023), phần lấn vịnh khai hoang 1941–1943
//    (HMGoG 199/2018); vạch sơn theo ICAO Annex 14 (ngưỡng phím đàn 30 × 1,8 m, số hiệu, tim 30 m / khe 20 m, mép, điểm ngắm) — vẽ trên kết cấu canvas.
//  · Tường thành thành phố (Line Wall, Charles V…): OSM historic=citywalls, cao ~6 m (ước), có từ trước 1704 (ước, ghi trong báo cáo).
import { THREE, GLSL_NOISE, GLSL_YEAR, rng } from './core.js';
import { walls, roof } from './geom.js';
import { GLSL_LAND } from './terrain.js';

const TAPIA = `${GLSL_NOISE}
vec3 tapia(vec3 wp, vec3 n, float ly){ vec3 c = vec3(0.80, 0.62, 0.42);   // tapia: vữa vôi + cát đỏ, gạch gốm nghiền (ấm, đất)
  float course = smoothstep(0.0, 0.05, abs(fract(ly / 0.85) - 0.5) - 0.42);   // vạch giữa các lớp đầm
  c *= 1.0 - 0.22 * course; float u = abs(n.x) > abs(n.z) ? wp.z : wp.x;
  vec2 pl = vec2(fract(u / 1.6), fract(ly / 0.85)); float hole = step(0.47, pl.x) * step(pl.x, 0.53) * step(0.03, pl.y) * step(pl.y, 0.14);
  c *= 1.0 - 0.35 * hole; c *= 0.86 + 0.20 * fbm(vec2(u * 0.35, ly * 0.9)); c *= 0.82 + 0.18 * smoothstep(0.0, 6.0, ly);
  c = mix(c, c * vec3(0.85, 0.83, 0.80), smoothstep(0.55, 0.9, fbm(vec2(u * 0.08, ly * 0.04 + 3.0))));   // vệt mưa
  return c; }`;

function stoneMat(U, hiU, kind) {
  const m = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.93 });
  m.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uDim: U.uDim, uHi: hiU });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float aLY; varying float vLY; varying vec3 vWPh; varying vec3 vWNh;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\n vLY = aLY; vWPh = (modelMatrix * vec4(transformed,1.0)).xyz; vWNh = normalize(mat3(modelMatrix) * objectNormal);');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\nuniform float uDim, uHi; varying float vLY; varying vec3 vWPh; varying vec3 vWNh; ${TAPIA}`)
      .replace('#include <color_fragment>', `#include <color_fragment>
      vec3 c = ${kind === 'lime' ? 'mix(vec3(0.74, 0.71, 0.63), vec3(0.62,0.60,0.55), smoothstep(0.4,0.8,fbm(vWPh.xz*0.07 + vLY*0.2)))' : 'tapia(vWPh, vWNh, vLY)'};
      { vec3 Vd = normalize(cameraPosition - vWPh); float rim = pow(1.0 - abs(dot(normalize(vWNh), Vd)), 2.5);   // viền sáng Fresnel khi nhấn hero
        c = mix(c, vec3(1.0, 0.84, 0.50), 0.18 * uHi) + vec3(1.0, 0.78, 0.35) * rim * 0.9 * uHi; }
      float L = dot(c, vec3(0.299,0.587,0.114)); c = mix(c, vec3(L), 0.55 * uDim * (1.0 - uHi)) * (1.0 - 0.36 * uDim * (1.0 - uHi));
      diffuseColor.rgb = c;`); };
  return m;
}
const geoFrom = (A) => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(A.p, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(A.n, 3)); g.setAttribute('aLY', new THREE.Float32BufferAttribute(A.l, 1)); return g; };
const acc = () => ({ p: [], n: [], l: [] });
const push = (A, base) => (x, y, z, nx, ny, nz) => { A.p.push(x, y + base, z); A.n.push(nx, ny, nz); A.l.push(y); };
function box(A, cx, cy, cz, w, h, d, rot) {   // hộp đặc (răng cưa, chắn), xoay quanh trục y
  const c = Math.cos(rot), s = Math.sin(rot), V = (x, y, z) => [cx + x * c - z * s, cy + y, cz + x * s + z * c];
  const F = [[[1, 0, 0], [[.5, -.5, -.5], [.5, .5, -.5], [.5, .5, .5], [.5, -.5, .5]]], [[-1, 0, 0], [[-.5, -.5, .5], [-.5, .5, .5], [-.5, .5, -.5], [-.5, -.5, -.5]]],
    [[0, 1, 0], [[-.5, .5, -.5], [-.5, .5, .5], [.5, .5, .5], [.5, .5, -.5]]], [[0, 0, 1], [[.5, -.5, .5], [.5, .5, .5], [-.5, .5, .5], [-.5, -.5, .5]]], [[0, 0, -1], [[-.5, -.5, -.5], [-.5, .5, -.5], [.5, .5, -.5], [.5, -.5, -.5]]]];
  for (const [n, q] of F) { const nn = [n[0] * c - n[2] * s, n[1], n[0] * s + n[2] * c], P = q.map(([x, y, z]) => V(x * w, y * h + h / 2, z * d));
    for (const k of [0, 1, 2, 0, 2, 3]) { A.p.push(...P[k]); A.n.push(...nn); A.l.push(P[k][1] - cy); } }
}
function crenel(A, ring, h, base, step = 2.2, mw = 1.1, mh = 1.6, md = 0.9) {   // răng cưa dọc mép đỉnh tường
  for (let i = 0; i < ring.length - 1; i++) { const [a, b] = [ring[i], ring[i + 1]], l = Math.hypot(b[0] - a[0], b[1] - a[1]), rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]);
    for (let s = step / 2; s < l; s += step) { const u = s / l; box(A, a[0] + (b[0] - a[0]) * u, base + h, -(a[1] + (b[1] - a[1]) * u), mw, mh, md, rot); } }
}
function wallLine(A, pts, hAt, h, thick) {   // tường dạng tuyến: dải hai mặt + đỉnh, chân bám địa hình
  for (let i = 0; i < pts.length - 1; i++) { const [a, b] = [pts[i], pts[i + 1]], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l < 0.5) continue;
    const ha = Math.max(hAt(...a), 0.5) - 1.0, hb = Math.max(hAt(...b), 0.5) - 1.0, rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]);
    const n = Math.max(1, Math.round(l / 6)); for (let k = 0; k < n; k++) { const u = (k + 0.5) / n; box(A, a[0] + (b[0] - a[0]) * u, ha + (hb - ha) * u, -(a[1] + (b[1] - a[1]) * u), l / n + 0.3, h + 1.0, thick, rot); } }
}

export function makeHeroes(H, hAt, U, terr) {
  const group = new THREE.Group(), out = { group, hi: { tower: { value: 0 }, runway: { value: 0 } } };
  // ---- Tower of Homage + tường lâu đài
  const T = acc(), tw = H.tower; const base = tw.base - 1.5, ring = tw.p;
  walls(ring, tw.h + 1.5, push(T, base)); roof(ring, tw.h + 1.5, 0, (r) => THREE.ShapeUtils.triangulateShape(r.map(([x, y]) => new THREE.Vector2(x, y)), []), push(T, base));
  crenel(T, ring.concat([ring[0]]), tw.h + 1.5, base);
  const CW = acc(); for (const w of H.castle_walls) { wallLine(CW, w, hAt, 8.0, 2.2); }
  const towerM = new THREE.Mesh(geoFrom(T), stoneMat(U, out.hi.tower, 'tapia')), castleM = new THREE.Mesh(geoFrom(CW), stoneMat(U, out.hi.tower, 'tapia'));
  // khe bắn tên: dải tối mảnh trên tường tháp (hộp lõm tối)
  const SL = acc(); { const r = ring; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length], l = Math.hypot(b[0] - a[0], b[1] - a[1]); if (l < 6) continue;
      const rot = Math.atan2(-(b[1] - a[1]), b[0] - a[0]); for (const lv of [9, 16]) for (let s = l / 4; s < l; s += l / 2.01) { const u = s / l; box(SL, a[0] + (b[0] - a[0]) * u, base + lv, -(a[1] + (b[1] - a[1]) * u), 0.35, 1.8, 0.25, rot); } } }
  const slitM = new THREE.Mesh(geoFrom(SL), new THREE.MeshStandardMaterial({ color: 0x1d1813, roughness: 1 }));
  for (const m of [towerM, castleM, slitM]) { m.castShadow = m.receiveShadow = true; group.add(m); }
  // viền sáng tháp (vỏ lộn mặt sau, nở 1,8 m) cho mốc đinh/nhấn
  const hull = new THREE.Mesh(new THREE.ExtrudeGeometry(new THREE.Shape(ring.map(([x, y]) => new THREE.Vector2(x, y))), { depth: tw.h + 3.5, bevelEnabled: false }).rotateX(-Math.PI / 2),
    new THREE.MeshBasicMaterial({ color: '#ffd166', side: THREE.BackSide, transparent: true, opacity: 0, depthWrite: false, fog: false }));
  { const c = ring.reduce((s, p) => [s[0] + p[0] / ring.length, s[1] + p[1] / ring.length], [0, 0]); hull.geometry.translate(-c[0], 0, c[1]); hull.scale.set(1.12, 1, 1.12); hull.position.set(c[0], base, -c[1]); out.towerTop = new THREE.Vector3(c[0], base + tw.h + 2, -c[1]); out.towerC = c; }
  hull.visible = false; group.add(hull); out.towerHull = hull;
  // ---- tường thành thành phố (đá vôi)
  const LW = acc(); for (const w of H.citywalls) wallLine(LW, w, hAt, 6.0, 3.0);
  const lw = new THREE.Mesh(geoFrom(LW), stoneMat(U, { value: 0 }, 'lime')); lw.castShadow = lw.receiveShadow = true; group.add(lw);
  // ---- đường băng
  // hai đầu đường băng = cực trị của tim OSM + đoạn ngưỡng lùi (displaced_threshold) chiếu lên trục
  const rp = H.runway.p.concat(...H.thresholds), a0 = H.runway.p[0], b0 = H.runway.p[H.runway.p.length - 1], ax = [b0[0] - a0[0], b0[1] - a0[1]], al = Math.hypot(...ax);
  const pr = rp.map((p) => [(p[0] - a0[0]) * ax[0] / al + (p[1] - a0[1]) * ax[1] / al, p]); pr.sort((x, y) => x[0] - y[0]);
  let W0 = pr[0][1], E0 = pr[pr.length - 1][1]; if (W0[0] > E0[0]) [W0, E0] = [E0, W0];
  const L = Math.hypot(E0[0] - W0[0], E0[1] - W0[1]), dir = [(E0[0] - W0[0]) / L, (E0[1] - W0[1]) / L], nrm = [-dir[1], dir[0]], hw = H.runway.w / 2;
  const disp = H.thresholds.map((p) => p.map(([e, n]) => (e - W0[0]) * dir[0] + (n - W0[1]) * dir[1])).map((s) => [Math.min(...s), Math.max(...s)]);
  const dW = Math.max(0, ...disp.filter((d) => d[0] < L / 2).map((d) => d[1])), dE = L - Math.max(0, ...disp.filter((d) => d[0] > L / 2).map((d) => L - d[0]));
  const TW = 8192, TH = 256, cv = document.createElement('canvas'); cv.width = TW; cv.height = TH; const g = cv.getContext('2d');
  const X = (s) => s / L * TW, Yv = (o) => (o + hw) / (2 * hw) * TH;   // s dọc (m từ đầu tây), o ngang (m, −hw..hw)
  g.fillStyle = '#4a4c50'; g.fillRect(0, 0, TW, TH);
  { const R = rng(3); for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '30,30,32' : '120,120,118'},${0.05 + R() * 0.08})`; g.fillRect(R() * TW, R() * TH, 2 + R() * 30, 1 + R() * 3); } }
  g.fillStyle = 'rgba(25,25,27,0.35)'; g.fillRect(X(dW + 250), Yv(-6), X(L - dW - 500) - X(0) + 0, Yv(6) - Yv(-6));   // vết lốp vùng chạm bánh (giữa)
  g.fillStyle = '#ecebe6';
  const rect = (s0, s1, o0, o1) => g.fillRect(X(s0), Yv(o0), X(s1) - X(s0), Yv(o1) - Yv(o0));
  rect(0, L, hw - 1.5, hw - 0.6); rect(0, L, -hw + 0.6, -hw + 1.5);   // vạch mép
  for (let s = dW + 30 + 12 + 9 + 12; s < dE - 30 - 12 - 9 - 12 - 30; s += 50) rect(s, s + 30, -0.45, 0.45);   // tim: 30 m vạch, 20 m khe
  const piano = (s0) => { for (let k = 0; k < 6; k++) { const o = 3.0 + k * 3.6; rect(s0, s0 + 30, o - 0.9, o + 0.9); rect(s0, s0 + 30, -o - 0.9, -o + 0.9); } };
  piano(dW + 6); piano(dE - 36);
  for (const s of [dW + 250, dE - 295]) { rect(s, s + 45, 4.5, 10.5); rect(s, s + 45, -10.5, -4.5); }   // điểm ngắm
  const num = (txt, s, rot) => { g.save(); g.translate(X(s), TH / 2); g.rotate(rot); g.scale(TW / L / (TH / (2 * hw)), 1); g.font = `bold ${Math.round(9 / (2 * hw) * TH * 1.35)}px DejaVu Sans, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, 0, 0); g.restore(); };
  num('09', dW + 52, Math.PI / 2); num('27', dE - 52, -Math.PI / 2);
  for (const [s0, s1] of [[0, dW], [dE, L]]) for (let s = s0 + 10; s < s1 - 10; s += 30) { g.save(); g.translate(X(s), TH / 2); g.fillRect(0, -2, X(18) - X(0), 4); g.restore(); }   // mũi tên ngưỡng lùi (tối giản)
  const rtex = new THREE.CanvasTexture(cv); rtex.colorSpace = THREE.SRGBColorSpace; rtex.anisotropy = 16;
  const RP = [], RU = [], N = Math.ceil(L / 15);
  for (let i = 0; i <= N; i++) { const s = L * i / N; for (const o of [-hw, hw]) { const e = W0[0] + dir[0] * s + nrm[0] * o, n = W0[1] + dir[1] * s + nrm[1] * o; RP.push(e, Math.max(3.0, hAt(e, n)) + 0.45, -n); RU.push(i / N, (o + hw) / (2 * hw)); } }
  const RI = []; for (let i = 0; i < N; i++) { const k = i * 2; RI.push(k, k + 2, k + 1, k + 1, k + 2, k + 3); }
  const rg = new THREE.BufferGeometry(); rg.setAttribute('position', new THREE.Float32BufferAttribute(RP, 3)); rg.setAttribute('uv', new THREE.Float32BufferAttribute(RU, 2)); rg.setIndex(RI); rg.computeVertexNormals();
  const rmat = new THREE.MeshStandardMaterial({ map: rtex, roughness: 0.85, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
  rmat.onBeforeCompile = (sh) => { Object.assign(sh.uniforms, { uYear: U.uYear, uDim: U.uDim, uHi: out.hi.runway, tYears: terr.uni.tYears, uExt: terr.uni.uExt });
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWPr;').replace('#include <begin_vertex>', '#include <begin_vertex>\n vWPr = (modelMatrix * vec4(transformed,1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>\nuniform float uYear, uDim, uHi; uniform sampler2D tYears; uniform vec4 uExt; varying vec3 vWPr; ${GLSL_LAND}`)
      .replace('#include <map_fragment>', `#include <map_fragment>
      vec2 guv = vec2((vWPr.x - uExt.x) / uExt.z, (-vWPr.z - uExt.y) / uExt.w); float lk = landK(decYear(texture(tYears, guv).ba), uYear);
      if (uYear < 1941.0 || lk < 0.98) discard;
      diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * vec3(1.25, 1.12, 0.85) + vec3(0.10, 0.07, 0.0), uHi);
      { float L = dot(diffuseColor.rgb, vec3(0.299,0.587,0.114)); diffuseColor.rgb = mix(diffuseColor.rgb, vec3(L), 0.55*uDim*(1.0-uHi)) * (1.0 - 0.36*uDim*(1.0-uHi)); }`); };
  const runway = new THREE.Mesh(rg, rmat); runway.receiveShadow = true; group.add(runway);
  // viền sáng đường băng (mốc đinh): khung chữ nhật phát sáng, chỉ phần trên đất
  const fr = new THREE.Group(); const fmat = new THREE.MeshBasicMaterial({ color: '#ffd166', transparent: true, opacity: 0, depthWrite: false, fog: false });
  const seg = (s0, s1, o0, o1) => { const e0 = W0[0] + dir[0] * s0 + nrm[0] * o0, n0 = W0[1] + dir[1] * s0 + nrm[1] * o0, e1 = W0[0] + dir[0] * s1 + nrm[0] * o1, n1 = W0[1] + dir[1] * s1 + nrm[1] * o1;
    const l = Math.hypot(e1 - e0, n1 - n0), m = new THREE.Mesh(new THREE.BoxGeometry(l + 3, 1.2, 3), fmat); m.position.set((e0 + e1) / 2, 4.6, -(n0 + n1) / 2); m.rotation.y = Math.atan2(-(n1 - n0), e1 - e0); fr.add(m); };
  // khung chỉ trên phần đường băng có đất năm 1941 (đông bờ vịnh cũ, ≈ E −340 m — xem build_scene.OLD_BAY); phần lấn vịnh khai hoang 1941–43
  const sL = Math.max(0, Math.min(L, (-340 - W0[0]) / dir[0])); out.rwLandS = sL;
  seg(sL, L, hw + 3, hw + 3); seg(sL, L, -hw - 3, -hw - 3); seg(sL, sL, -hw - 3, hw + 3); seg(L, L, -hw - 3, hw + 3); fr.visible = false; group.add(fr); out.rwFrame = fr; out.rwFrameMat = fmat;
  // chắn đường ngang (đỏ/trắng) ở hai mép đường băng trên trục Winston Churchill Ave (gốc toạ độ)
  const bar = new THREE.Group(); for (const o of [hw + 9, -hw - 9]) { const e = nrm[0] * o, n = nrm[1] * o, h0 = Math.max(3, hAt(e, n));
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.4, 0.5), new THREE.MeshStandardMaterial({ color: 0x9aa0a6 })); post.position.set(e + 5, h0 + 0.7, -n); bar.add(post);
    for (let k = 0; k < 6; k++) { const arm = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.18, 0.18), new THREE.MeshStandardMaterial({ color: k % 2 ? 0xf2f2f2 : 0xc8322b })); arm.position.set(e + 4.2 - k * 1.6, h0 + 1.3, -n); bar.add(arm); } }
  bar.visible = false; group.add(bar); out.barriers = bar;
  out.runwayMid = new THREE.Vector3(0, 4, 0); out.runway = { W0, E0, L, dir, hw, dW, dE };
  out.update = (year) => { bar.visible = year >= 1941; };
  return out;
}

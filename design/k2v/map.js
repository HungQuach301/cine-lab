// KÊNH 2 · module A — BẢN ĐỒ ĐỊA LÝ THẬT (k2v/map). Địa cầu → bay xuống quốc gia/bang/thành phố; cung nối 2 điểm; cột số liệu nhô trên bản đồ;
// nhãn địa danh do lớp chữ 2D (scripts/k2/lib/k2.js, p.places) vẽ tại điểm neo (≥ 30 px), điểm neo ở mặt sau địa cầu → ẩn.
// Dữ liệu: Natural Earth 1:50m/1:10m qua world-atlas 2.0.2 (tài sản công), Census cartographic boundary 2017 qua us-atlas 3.0.1 (tài sản công).
// Texture tuỳ chọn: NASA Blue Marble: Next Generation (12/2004) — bm-global-8192.jpg + vùng gốc bm-crop-*.jpg (scripts/k2/k2v_assets.py, cache ngoài git).
//
// API (opt của cảnh `map/globe`; mọi thời điểm là giây trong cảnh — prep.py đổi "@từ" thành giây):
//   bm: true|false                    nền Blue Marble (mặc định true) hay nền vector mực
//   patches: [{bbox:[lon0,lat0,lon1,lat1], img:'/cache/bm-crop-…jpg'}]   vùng chi tiết cho cảnh bay xuống (nét ở tầm thành phố)
//   detail: '50m'|'10m'                độ chi tiết biên giới trên vùng (mặc định 10m cho patches, 50m toàn cầu)
//   hl: [{country:'United States of America'|id ISO số, color, at, lift}]   tô + viền nhô (tường sáng) cho quốc gia
//   states: true | [{state:'Pennsylvania', color, at}]                     biên giới bang Mỹ (+ tô bang)
//   places: ['washington', {id:'x', ll:[lon,lat], name}]                   ghim địa danh (điểm neo cùng tên)
//   arcs: [{from, to, draw:[t0,t1], color, h}]                              cung đại vòng nhô lên, vẽ dần, có đầu sáng; neo 'arc0' (đỉnh)
//   cols: [{id, at:'washington'|[lon,lat], v (0..1 chiều cao tương đối), grow:[t0,t1], color, r}]   cột số liệu; neo 'col:<id>' (đỉnh)
//   cam: [{u|t, lon, lat, alt, tilt, head, mm}]   máy quay địa lý: nhìn vào (lon,lat) từ độ cao alt (đơn vị bán kính Trái Đất R=10 → alt 20 = 2R),
//                                                  tilt độ nghiêng khỏi phương thẳng đứng (độ), head hướng nhìn (0 = nhìn về phía Bắc), mm tiêu cự
//   grade, exposure                  như k2page
import { THREE, C, cl, lerp, eo, win, keyTrack, fovOf, canvasTex, loadImg, loadJSON, glowSprite, rng } from './common.js';
export const NEEDS = ['geo'];
const R = 10, D2R = Math.PI / 180;
export const ll2v = (lon, lat, r = R) => new THREE.Vector3(r * Math.cos(lat * D2R) * Math.sin(lon * D2R), r * Math.sin(lat * D2R), r * Math.cos(lat * D2R) * Math.cos(lon * D2R));
const hexA = (hex, a) => { const c = new THREE.Color(hex); return `rgba(${Math.round(c.r * 255)},${Math.round(c.g * 255)},${Math.round(c.b * 255)},${a})`; };   // c.r ở đây là sRGB (Color(hex) giữ sRGB khi ColorManagement tắt) — kiểm K5 bằng khung thật

let GEO = null;
async function geo(detail) {
  GEO = GEO || {};
  if (!GEO[detail]) {
    const src = detail === '10m' ? '/k2v/node_modules/world-atlas/countries-10m.json' : detail === '110m' ? '/k2v/data/countries-110m.json' : '/k2v/data/countries-50m.json';
    const w = await loadJSON(src); GEO[detail] = { countries: topojson.feature(w, w.objects.countries).features, borders: topojson.mesh(w, w.objects.countries, (a, b) => a !== b), land: topojson.feature(w, w.objects.land) };
  }
  if (!GEO.us) { const u = await loadJSON('/k2v/data/states-10m.json'); GEO.us = { states: topojson.feature(u, u.objects.states).features, mesh: topojson.mesh(u, u.objects.states, (a, b) => a !== b) }; }
  return { ...GEO[detail], us: GEO.us };
}
const findCountry = (G, q) => G.countries.find((f) => f.properties.name === q || String(+f.id) === String(+q)) || null;

// Vẽ lớp bản đồ lên canvas equirect: ảnh nền (Blue Marble đã hạ tông) hoặc nền mực + đất; biên giới; tô quốc gia/bang.
function paint(g, w, h, proj, G, o, img, k) {
  const path = d3.geoPath(proj, g);
  if (img) { g.drawImage(img, 0, 0, w, h);   // không dùng ctx.filter: canvas lớn (8192×4096) trong Chromium headless trả về rỗng khi có filter (đo 12/10/2026)
    g.fillStyle = `rgba(15,23,34,${o.veil ?? 0.12})`; g.fillRect(0, 0, w, h); }
  else { g.fillStyle = '#0c1522'; g.fillRect(0, 0, w, h); g.beginPath(); path(G.land); g.fillStyle = '#25313f'; g.fill(); }
  const lw = Math.max(1, k);   // k: hệ số nét theo mật độ điểm ảnh của canvas
  for (const H of o.hl || []) { const f = findCountry(G, H.country); if (!f) continue; g.beginPath(); path(f); g.fillStyle = hexA(H.color || C.orange, H.fill ?? 0.26); g.fill(); }
  if (o.states) { const S = Array.isArray(o.states) ? o.states : [];
    for (const s of S) { const f = G.us.states.find((x) => x.properties.name === s.state); if (!f) continue; g.beginPath(); path(f); g.fillStyle = hexA(s.color || C.teal, s.fill ?? 0.3); g.fill(); }
    g.beginPath(); path(G.us.mesh); g.strokeStyle = 'rgba(238,241,244,0.30)'; g.lineWidth = 1.1 * lw; g.stroke(); }
  g.beginPath(); path(G.borders); g.strokeStyle = 'rgba(238,241,244,0.42)'; g.lineWidth = 1.6 * lw; g.stroke();
  if (!img) { g.beginPath(); path(G.land); g.strokeStyle = 'rgba(154,167,181,0.7)'; g.lineWidth = 1.2 * lw; g.stroke(); }
  for (const H of o.hl || []) { const f = findCountry(G, H.country); if (!f) continue; g.beginPath(); path(f); g.strokeStyle = H.color || C.orange; g.lineWidth = 2.6 * lw; g.stroke(); }
}

// Tường sáng dọc biên quốc gia (quốc gia "nhô" khỏi bề mặt): dải đứng từ R tới R(1+lift), alpha tăng theo chiều cao.
function liftWall(f, color, lift) {
  const P = [], H = [], polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  for (const poly of polys) { const ring = poly[0]; if (ring.length < 8) continue;
    for (let i = 0; i < ring.length - 1; i++) { const a = ring[i], b = ring[i + 1];
      const a0 = ll2v(a[0], a[1], R * 1.0004), a1 = ll2v(a[0], a[1], R * (1 + lift)), b0 = ll2v(b[0], b[1], R * 1.0004), b1 = ll2v(b[0], b[1], R * (1 + lift));
      P.push(...a0.toArray(), ...b0.toArray(), ...a1.toArray(), ...b0.toArray(), ...b1.toArray(), ...a1.toArray()); H.push(0, 0, 1, 0, 1, 1); } }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); geo.setAttribute('hh', new THREE.Float32BufferAttribute(H, 1));
  const m = new THREE.ShaderMaterial({ uniforms: { col: { value: new THREE.Color(color) }, k: { value: 0 } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending,
    vertexShader: 'attribute float hh; varying float vh; void main(){ vh = hh; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform vec3 col; uniform float k; varying float vh; void main(){ gl_FragColor = vec4(col * (0.3 + 1.1 * vh * vh), 1.0) * k * (0.15 + 0.6 * vh); }' });
  return new THREE.Mesh(geo, m);
}

// Thư viện góc máy bản đồ (scripts/k2/cams.yaml liệt kê; camera_id = tên preset). Mỗi preset là chuyển động liên tục, không đứng hình.
export const MAP_PRESETS = {
  orbit: (o, LL) => { const [x, y] = LL(o.focus); return [{ u: 0, lon: x - 14, lat: y - 4, alt: 26, mm: 35 }, { u: 1, lon: x + 4, lat: y, alt: 24, mm: 35 }]; },
  flyto: (o, LL) => { const [x, y] = LL(o.focus); return [{ u: 0, lon: x + 18, lat: y - 8, alt: 28, mm: 35 }, { u: 0.25, lon: x + 10, lat: y - 4, alt: 22, mm: 35 }, { u: 1, lon: x, lat: y - 0.6, alt: o.alt || 2.6, tilt: 32, mm: 35 }]; },
  pullback: (o, LL) => { const [x, y] = LL(o.focus); return [{ u: 0, lon: x, lat: y - 0.5, alt: o.alt || 2.4, tilt: 34, mm: 35 }, { u: 1, lon: x - 6, lat: y - 3, alt: 22, tilt: 0, mm: 35 }]; },
  'tilt-low': (o, LL) => { const [x, y] = LL(o.focus); return [{ u: 0, lon: x - 0.8, lat: y - 1.2, alt: (o.alt || 3) * 1.1, tilt: 50, head: -12, mm: 40 }, { u: 1, lon: x + 0.6, lat: y - 0.9, alt: o.alt || 3, tilt: 54, head: 12, mm: 40 }]; },
  top: (o, LL) => { const [x, y] = LL(o.focus); return [{ u: 0, lon: x - 1.5, lat: y, alt: (o.alt || 5) * 1.08, tilt: 0, mm: 35 }, { u: 1, lon: x + 1.5, lat: y, alt: o.alt || 5, tilt: 0, mm: 35 }]; },
  pan: (o, LL) => { const [x, y] = LL(o.focus); return [{ u: 0, lon: x - 9, lat: y - 1, alt: o.alt || 6, tilt: 30, head: 0, mm: 35 }, { u: 1, lon: x + 9, lat: y - 1, alt: o.alt || 6, tilt: 30, head: 0, mm: 35 }]; },
  pair: (o, LL) => { const [ax, ay] = LL(o.from), [bx, by] = LL(o.to), mx = (ax + bx) / 2, my = (ay + by) / 2 + 4, d = Math.hypot(bx - ax, by - ay);
    return [{ u: 0, lon: ax + 8, lat: ay - 6, alt: 24, mm: 35 }, { u: 0.33, lon: ax, lat: ay - 1.6, alt: 2.8, tilt: 34, mm: 35 }, { u: 0.45, lon: ax + 0.8, lat: ay - 1.2, alt: 3.0, tilt: 34, head: 15, mm: 35 },
      { u: 0.62, lon: mx, lat: my, alt: Math.max(6, d * 0.11), tilt: 18, mm: 35 }, { u: 0.85, lon: bx - 0.6, lat: by - 2.2, alt: 2.8, tilt: 36, mm: 35 }, { u: 1, lon: bx - 0.1, lat: by - 1.8, alt: 2.5, tilt: 38, head: -6, mm: 35 }]; },
};

export const HEROES = {
  async globe({ W, H, dur, opt: o = {}, renderer }) {
    const G = await geo('50m'); const scene = new THREE.Scene(); scene.background = new THREE.Color('#05080e');
    const maxT = renderer.capabilities.maxTextureSize, TW = Math.min(8192, maxT);
    const PL = Object.assign({}, await loadJSON('/k2v/data/places.json')); for (const p of o.places || []) if (typeof p === 'object' && p.ll) PL[p.id] = { name: p.name, ll: p.ll };
    const LL = (a) => (Array.isArray(a) ? a : PL[a].ll);
    // ---- địa cầu nền
    const bm = o.bm === false ? null : await loadImg('/cache/bm-global-8192.jpg');
    const proj = d3.geoEquirectangular().scale(TW / (2 * Math.PI)).translate([TW / 2, TW / 4]);
    const tex = canvasTex(TW, TW / 2, (g, w, h) => paint(g, w, h, proj, G, o, bm, TW / 8192 * 0.9));
    const mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.82, metalness: 0, emissive: '#ffffff', emissiveMap: tex, emissiveIntensity: 0.5 });
    const globe = new THREE.Mesh(new THREE.SphereGeometry(R, 256, 128, -Math.PI / 2, Math.PI * 2), mat); scene.add(globe);
    // ---- vùng chi tiết (bay xuống): canvas theo đúng độ phân giải ảnh vùng, biên 10m, mép mờ dần
    if (o.patches && o.patches.length) { const G10 = await geo(o.detail || '10m');
      for (const pa of o.patches) { const [lon0, lat0, lon1, lat1] = pa.bbox, im = pa.img ? await loadImg(pa.img) : null;
        const pw = Math.min(maxT, im ? im.naturalWidth : 4096), ph = Math.round(pw * (lat1 - lat0) / (lon1 - lon0)), k = pw / ((lon1 - lon0) * D2R);
        const pj = d3.geoEquirectangular().scale(k).translate([-k * lon0 * D2R, k * lat1 * D2R]);
        const t2 = canvasTex(pw, ph, (g, w, h) => { paint(g, w, h, pj, G10, o, im, w / ((lon1 - lon0) / 360 * 8192) * 0.55);
          g.globalCompositeOperation = 'destination-in'; const fx = g.createLinearGradient(0, 0, w, 0); fx.addColorStop(0, 'rgba(0,0,0,0)'); fx.addColorStop(0.06, '#000'); fx.addColorStop(0.94, '#000'); fx.addColorStop(1, 'rgba(0,0,0,0)');
          g.fillStyle = fx; g.fillRect(0, 0, w, h); const fy = g.createLinearGradient(0, 0, 0, h); fy.addColorStop(0, 'rgba(0,0,0,0)'); fy.addColorStop(0.1, '#000'); fy.addColorStop(0.9, '#000'); fy.addColorStop(1, 'rgba(0,0,0,0)');
          g.fillStyle = fy; g.fillRect(0, 0, w, h); g.globalCompositeOperation = 'source-over'; });
        const pm = new THREE.MeshStandardMaterial({ map: t2, roughness: 0.82, metalness: 0, emissive: '#ffffff', emissiveMap: t2, emissiveIntensity: 0.5, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 });
        const pg = new THREE.SphereGeometry(R * 1.0003, 192, 96, lon0 * D2R + Math.PI / 2, (lon1 - lon0) * D2R, (90 - lat1) * D2R, (lat1 - lat0) * D2R);
        const pmh = new THREE.Mesh(pg, pm); pmh.renderOrder = 1; scene.add(pmh); } }
    // ---- khí quyển (rìa sáng) + sao
    const atm = new THREE.Mesh(new THREE.SphereGeometry(R * 1.035, 96, 48), new THREE.ShaderMaterial({ side: THREE.BackSide, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 w = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix * normal); vV = normalize(-w.xyz); gl_Position = projectionMatrix * w; }',
      fragmentShader: 'varying vec3 vN; varying vec3 vV; void main(){ float d = -dot(vN, vV); float k = pow(smoothstep(0.0, 0.26, d), 2.2); gl_FragColor = vec4(vec3(0.36, 0.58, 1.0) * k * 0.9, 1.0); }' }));   // mặt sau vỏ R·1.035: sáng nhất ở rìa địa cầu (d ≈ 0,26), tắt dần ra ngoài
    scene.add(atm);
    const rim = new THREE.Mesh(new THREE.SphereGeometry(R * 1.001, 128, 64), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 w = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix * normal); vV = normalize(-w.xyz); gl_Position = projectionMatrix * w; }',
      fragmentShader: 'varying vec3 vN; varying vec3 vV; void main(){ float k = pow(1.0 - max(dot(vN, vV), 0.0), 2.6); gl_FragColor = vec4(vec3(0.35, 0.6, 1.0) * k * 0.55, 1.0); }' }));
    rim.renderOrder = 2; scene.add(rim);
    { const R2 = rng(5), n = 2600, P = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = R2() * 2 - 1, a = R2() * 6.283, s = Math.sqrt(1 - u * u); P.set([600 * s * Math.cos(a), 600 * u, 600 * s * Math.sin(a)], i * 3); }
      const sg = new THREE.BufferGeometry(); sg.setAttribute('position', new THREE.BufferAttribute(P, 3)); scene.add(new THREE.Points(sg, new THREE.PointsMaterial({ color: '#c9d6ee', size: 1.3, sizeAttenuation: false, transparent: true, opacity: 0.5, depthWrite: false }))); }
    // ---- tường sáng quốc gia
    const walls = []; for (const H2 of o.hl || []) { if (!H2.lift) continue; const f = findCountry(G, H2.country); if (!f) continue; const m = liftWall(f, H2.color || C.orange, H2.lift === true ? 0.0022 : H2.lift); m.renderOrder = 3; scene.add(m); walls.push([m, H2.at]); }
    // ---- ánh sáng: chính theo máy quay (luôn sáng vùng đang nhìn), nền lạnh
    const cam = new THREE.PerspectiveCamera(30, W / H, 0.01, 2000); scene.add(cam);
    const key = new THREE.DirectionalLight('#fff4e6', 2.2); key.position.set(-6, 5, 4); cam.add(key); key.target = globe;
    scene.add(new THREE.HemisphereLight('#9fb6e0', '#10141c', 0.7));
    // ---- ghim địa danh
    const anchors = {}, camPos = () => cam.position;
    const visible = (p) => { const n = p.clone().normalize(); return n.dot(camPos().clone().sub(p)) > 0 ? p : null; };
    const pins = [];
    for (const p of o.places || []) { const id = typeof p === 'string' ? p : p.id; const [lon, lat] = LL(id), at = typeof p === 'object' ? p.at : undefined;
      const pos = ll2v(lon, lat, R * 1.0012), dot = glowSprite('#ffe6c8', 1.4, 0.16); dot.position.copy(pos); scene.add(dot);
      const core = new THREE.Mesh(new THREE.SphereGeometry(0.012, 12, 8), new THREE.MeshBasicMaterial({ color: '#fff6ea' })); core.position.copy(pos); scene.add(core);
      pins.push({ dot, core, at }); anchors[id] = () => visible(pos); }
    // ---- cột số liệu (nhô theo pháp tuyến)
    const cols = [];
    for (const c of o.cols || []) { const [lon, lat] = LL(c.at), n = ll2v(lon, lat, 1), base = ll2v(lon, lat, R * 1.0008), hmax = (c.v ?? 0.5) * (c.hmax || 0.5), r = c.r || 0.035;
      const g = new THREE.Group(); g.position.copy(base); g.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), n); scene.add(g);
      const m = new THREE.MeshStandardMaterial({ color: c.color || C.orange, roughness: 0.35, metalness: 0.25, emissive: c.color || C.orange, emissiveIntensity: 0.35 });
      const body = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 40, 1), m); g.add(body);
      const cap = new THREE.Mesh(new THREE.CircleGeometry(r * 1.0, 40), new THREE.MeshBasicMaterial({ color: '#ffd8b8' })); cap.rotation.x = -Math.PI / 2; g.add(cap);
      const ring = new THREE.Mesh(new THREE.RingGeometry(r * 1.3, r * 2.4, 48), new THREE.MeshBasicMaterial({ color: c.color || C.orange, transparent: true, opacity: 0.45, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
      ring.rotation.x = -Math.PI / 2; ring.position.y = 0.002; g.add(ring);
      cols.push({ c, body, cap, ring, hmax, g }); const top = new THREE.Vector3();
      anchors['col:' + (c.id || cols.length - 1)] = () => { g.updateMatrixWorld(); top.set(0, Math.max(0.001, body.scale.y), 0).applyMatrix4(g.matrixWorld); return visible(ll2v(lon, lat, R)) ? top : null; }; }
    // ---- cung đại vòng
    const arcs = [];
    for (const [i, a] of (o.arcs || []).entries()) { const A = ll2v(...LL(a.from), 1), B = ll2v(...LL(a.to), 1), ang = A.angleTo(B), hk = a.h ?? Math.min(0.2, 0.03 + ang * 0.11), pts = [];
      for (let s = 0; s <= 160; s++) { const u = s / 160, v = new THREE.Vector3().copy(A).multiplyScalar(Math.sin((1 - u) * ang) / Math.sin(ang)).add(B.clone().multiplyScalar(Math.sin(u * ang) / Math.sin(ang)));
        pts.push(v.normalize().multiplyScalar(R * (1.001 + hk * Math.sin(Math.PI * u)))); }
      const curve = new THREE.CatmullRomCurve3(pts), TS = 320, RS = 10;
      const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, TS, a.r || 0.022, RS, false), new THREE.MeshBasicMaterial({ color: a.color || C.amber }));
      const glow = new THREE.Mesh(new THREE.TubeGeometry(curve, TS, (a.r || 0.022) * 2.0, RS, false), new THREE.MeshBasicMaterial({ color: a.color || C.amber, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, depthWrite: false }));
      const head = glowSprite(a.color || C.amber, 2.2, 0.5); scene.add(tube, glow, head);
      arcs.push({ a, curve, tube, glow, head, n: TS * RS * 6 }); anchors['arc' + i] = () => visible(curve.getPoint(0.5).clone().setLength(R)) ? curve.getPoint(0.5) : null; }
    // ---- máy quay địa lý: opt.cam, hoặc opt.preset (thư viện, cần opt.focus = địa danh/[lon,lat]; 'pair' cần opt.from/opt.to)
    const keys = o.cam || (o.preset && MAP_PRESETS[o.preset] ? MAP_PRESETS[o.preset](o, LL) : null) || [{ u: 0, lon: -30, lat: 30, alt: 26, tilt: 0, head: 0, mm: 35 }, { u: 1, lon: -20, lat: 32, alt: 24, tilt: 0, head: 0, mm: 35 }];
    const track = keyTrack(keys, dur, (a, b, u) => ({ lon: lerp(a.lon, b.lon, u), lat: lerp(a.lat, b.lat, u), alt: Math.exp(lerp(Math.log(a.alt), Math.log(b.alt), u)),
      tilt: lerp(a.tilt || 0, b.tilt || 0, u), head: lerp(a.head || 0, b.head || 0, u), mm: lerp(a.mm || 35, b.mm || 35, u) }));
    const Y = new THREE.Vector3(0, 1, 0);
    const place = (t) => { const k = track(t), T = ll2v(k.lon, k.lat, R), n = T.clone().normalize();
      const east = new THREE.Vector3().crossVectors(Y, n).normalize(), north = new THREE.Vector3().crossVectors(n, east).normalize();
      const hd = north.clone().multiplyScalar(Math.cos(k.head * D2R)).add(east.clone().multiplyScalar(Math.sin(k.head * D2R)));   // hướng nhìn trên mặt đất
      const off = n.clone().multiplyScalar(Math.cos(k.tilt * D2R)).sub(hd.clone().multiplyScalar(Math.sin(k.tilt * D2R))).multiplyScalar(k.alt);
      cam.position.copy(T).add(off); cam.up.copy(k.tilt > 0.5 ? n : north); cam.lookAt(T); cam.fov = fovOf(k.mm); cam.near = Math.max(0.005, k.alt * 0.02); cam.far = 2000; cam.updateProjectionMatrix(); };
    place(0);
    return { scene, cam, grade: o.grade || 'info', exposure: o.exposure || 1.3, anchors,
      update(t) { place(t);
        for (const p of pins) { const u = win(p.at, t); p.dot.material.opacity = u; p.core.visible = u > 0.02; p.dot.scale.setScalar(0.16 * (0.8 + 0.2 * Math.sin(t * 3)) * Math.max(o.pinMin ?? 0.6, cam.position.distanceTo(p.core.position) / 6)); p.core.scale.setScalar(Math.max(o.pinMin ?? 0.6, cam.position.distanceTo(p.core.position) / 6)); }   // pinMin: ghim nhỏ hơn khi bay xuống tầm thành phố (K2C-T1-06)
        for (const [m, at] of walls) m.material.uniforms.k.value = win(at, t, 1.0);
        for (const c of cols) { const u = eo(win(c.c.grow, t, 1.2)); c.body.scale.y = Math.max(0.0001, u * c.hmax); c.body.position.y = c.body.scale.y / 2; c.cap.position.y = c.body.scale.y + 0.001; c.ring.material.opacity = 0.45 * Math.min(1, u * 4); c.g.visible = u > 0.001; }
        for (const A of arcs) { const u = win(A.a.draw, t), k = Math.floor(A.n * u / 6) * 6; A.tube.geometry.setDrawRange(0, k); A.glow.geometry.setDrawRange(0, k); A.tube.visible = A.glow.visible = k > 0;
          A.head.visible = u > 0.001 && u < 0.999; if (A.head.visible) A.head.position.copy(A.curve.getPoint(u)); A.head.scale.setScalar(0.25 + 0.04 * cam.position.length() / R); }
      } };
  },
};

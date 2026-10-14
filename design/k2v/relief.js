// KÊNH 2 · module E — BẢN ĐỒ ĐỊA HÌNH NỔI (k2v/relief, phiên V2 14/10/2026). Công thức "bản đồ nổi + sticker" (học cách làm, không dùng hình của ai):
// nền địa hình thật (USGS 3DEP 1" → lưới độ cao + tô bóng nhiều hướng, scripts/k2/relief_build.py), sắc nét ở tầm vùng 300–500 km;
// hai bảng màu TỰ NHIÊN (hiện tại) ↔ SEPIA (quá khứ) chuyển dần; vùng tô NỔI theo mã màu từng phía (khối nhô có tường + bóng đổ + viền sáng);
// máy quay trượt liên tục (spline Hermite qua mốc, không dừng ở mốc); cung đường liền/nét đứt chảy; vòng sáng; chồng xu/cột tỷ lệ thật (neo col:<id>).
// Sticker và nhân vật A-lite là lớp 2D (scripts/k2/lib/sticker.js + k2.js p.stickers) đặt tại điểm neo 'st:<id>' do module này xuất (bám toạ độ bản đồ).
//
// API (opt của cảnh `relief/map`; mọi thời điểm = giây trong cảnh, prep.py đổi "@từ" thành giây):
//   relief: 'erie'                       nền đã dựng ở $K2V_CACHE/relief/<tên>/ (relief_build.py build --name … --bbox …)
//   ve: 7                                phóng đại chiều cao (mặc định 7)
//   palette: 'natural'|'sepia' | sepia: [t0, t1] (tự nhiên → sepia) | natural: [t0, t1] (sepia → tự nhiên)
//   regions: [{id, state|country|ll:[[lon,lat]…], color, at:[t0,t1]|t, out, lift (km, mặc định 4), fill (0..1)}]   ≤ 3 vùng; nổi + tô + viền
//   routes: [{id, pts: [[lon,lat] | {src:'erie'|'hudson'|'mohawk', from:[lon,lat], to:[lon,lat]}], draw:[t0,t1], style:'solid'|'dashed', color, w (px ~1080p), flow}]
//   rings: [{id, at: place|[lon,lat], t, out, color, r (km)}]      vòng sáng lan trên mặt đất
//   places: [id | {id, ll, name}]       điểm neo địa danh (nhãn ở lớp 2D p.places); gazetteer data/places.json + places-relief.json
//   pins: [{id, at: place|[lon,lat], dy}]                           neo 'st:<id>' cho sticker đứng yên
//   walkers: [{id, route, t:[t0,t1], u:[u0,u1]}]                   neo 'st:<id>' chạy theo tuyến (nhân vật/tàu đi trên bản đồ)
//   cols: [{id, at, kind:'coins'|'bar', n|v, unit, t:[t0,t1], color, r, dx, dy}]   chồng xu (n đồng, mỗi đồng = unit) / cột (v km) tỷ lệ thật; neo 'col:<id>' (đỉnh) — Q34(c)
//   cam: [{t|u, lon, lat, dist (km), tilt°, head°, mm}]              máy quay: nhìn (lon,lat) từ khoảng cách dist, nghiêng tilt khỏi phương đứng, hướng head (0 = Bắc)
import { THREE, C, cl, lerp, eo, ease, win, fovOf, loadImg, loadJSON, glowSprite } from './common.js';
export const NEEDS = ['geo'];
// tone map riêng cho bản đồ: giữ bảng màu (ACES làm xỉn/đổi sắc giấy sepia); vai mềm trên 0,82
export const TONE = `vec3 tonemap(vec3 c){ c *= EXPOSURE; vec3 k = 0.82 + 0.18 * (1.0 - exp(-(c - 0.82) / 0.18)); return clamp(mix(c, k, step(vec3(0.82), c)), 0.0, 1.0); }`;

const D2R = Math.PI / 180;
function envMap(renderer) {   // phòng hộp đèn (như chart3d) cho phản xạ kim loại của xu
  const s = new THREE.Scene(); s.add(new THREE.Mesh(new THREE.BoxGeometry(40, 20, 40), new THREE.MeshBasicMaterial({ color: '#1c2430', side: THREE.BackSide })));
  const panel = (w, h, x, y, z, ry, c, k) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), side: THREE.DoubleSide })); m.position.set(x, y, z); m.rotation.y = ry; s.add(m); };
  panel(14, 6, -12, 6, 10, Math.PI * 0.75, '#fff2e0', 6); panel(10, 14, 16, 4, -8, -Math.PI / 2, '#cfe0ff', 2.5); panel(30, 2, 0, 9.5, 0, 0, '#ffffff', 1.5);
  const pm = new THREE.PMREMGenerator(renderer); const rt = pm.fromScene(s, 0.04); pm.dispose(); return rt.texture;
}
// Hermite bậc 3 qua các mốc (tiếp tuyến Catmull-Rom theo thời gian): máy quay không dừng ở mốc giữa; hai đầu giữ vận tốc (trượt liên tục qua mối cắt)
function spline(keys, dur, fields) {
  const K = keys.map((k) => ({ ...k, t: k.t !== undefined ? k.t : (k.u || 0) * dur })).sort((a, b) => a.t - b.t);
  const val = (k, f) => (f === 'dist' ? Math.log(k.dist) : k[f] ?? 0);
  return (t) => { const out = {};
    if (K.length === 1) { for (const f of fields) out[f] = K[0][f] ?? 0; return out; }
    let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], h = b.t - a.t, u = (t - a.t) / h;
    for (const f of fields) { const p0 = val(a, f), p1 = val(b, f);
      const m0 = i > 0 ? (p1 - val(K[i - 1], f)) / (b.t - K[i - 1].t) : (p1 - p0) / h, m1 = i + 2 < K.length ? (val(K[i + 2], f) - p0) / (K[i + 2].t - a.t) : (p1 - p0) / h;
      const u2 = u * u, u3 = u2 * u; let v = (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * h * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * h * m1;
      out[f] = f === 'dist' ? Math.exp(v) : v; }
    return out; };
}

export const HEROES = {
  async map({ W, H, dur, opt: o = {}, renderer }) {
    const name = o.relief || 'erie', base = `/cache/relief/${name}/`, meta = await loadJSON(base + 'meta.json');
    const [lon0, lat0, lon1, lat1] = meta.bbox, latc = (lat0 + lat1) / 2, lonc = (lon0 + lon1) / 2, kx = 111.32 * Math.cos(latc * D2R), kz = 110.57;
    const WK = (lon1 - lon0) * kx, HK = (lat1 - lat0) * kz, VE = o.ve ?? 7;
    const X = (lon) => (lon - lonc) * kx, Z = (lat) => -(lat - latc) * kz;
    const PL = Object.assign({}, await loadJSON('/k2v/data/places.json'), await loadJSON('/k2v/data/places-relief.json').catch(() => ({})));
    for (const p of o.places || []) if (typeof p === 'object' && p.ll) PL[p.id] = { name: p.name, ll: p.ll };
    const LL = (a) => (Array.isArray(a) ? a : (PL[a] || (() => { throw new Error('không có địa danh ' + a); })()).ll);
    const scene = new THREE.Scene();
    // ---- độ cao
    const [MW, MH] = meta.mesh, hb = await (await fetch(base + 'height.f32')).arrayBuffer(), HT = new Float32Array(hb);
    const hAt = (lon, lat) => { const fx = cl((lon - lon0) / (lon1 - lon0)) * (MW - 1), fy = cl((lat1 - lat) / (lat1 - lat0)) * (MH - 1), x0 = Math.floor(fx), y0 = Math.floor(fy), x1 = Math.min(MW - 1, x0 + 1), y1 = Math.min(MH - 1, y0 + 1), ax = fx - x0, ay = fy - y0;
      const g = (x, y) => HT[y * MW + x]; return (lerp(lerp(g(x0, y0), g(x1, y0), ax), lerp(g(x0, y1), g(x1, y1), ax), ay)) / 1000 * VE; };
    const geo = new THREE.PlaneGeometry(WK, HK, MW - 1, MH - 1); geo.rotateX(-Math.PI / 2);
    { const P = geo.attributes.position; for (let i = 0; i < P.count; i++) P.setY(i, HT[i] / 1000 * VE); P.needsUpdate = true; }
    // ---- bảng màu
    const maxT = renderer.capabilities.maxTextureSize;
    const tex = async (f) => { const im = await loadImg(base + f); let src = im;
      if (im.naturalWidth > maxT) { const cv = document.createElement('canvas'); cv.width = maxT; cv.height = Math.round(maxT * im.naturalHeight / im.naturalWidth); cv.getContext('2d').drawImage(im, 0, 0, cv.width, cv.height); src = cv; }
      const t = new THREE.Texture(src); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.needsUpdate = true; return t; };
    const tNat = await tex('natural.jpg'), tSep = await tex('sepia.jpg');
    // ---- vùng: mặt nạ tô (RGB = vùng 0..2) và viền, raster theo toạ độ bản đồ; CPU giữ bản sao để đặt vật lên vùng đã nổi
    const RW = 2700, RH = 1800, regions = (o.regions || []).slice(0, 3);
    const fillA = new Uint8Array(RW * RH * 4), edgeA = new Uint8Array(RW * RH * 4);
    if (regions.length) {
      const us = await loadJSON('/k2v/data/states-10m.json'), wa = await loadJSON('/k2v/data/countries-50m.json');
      const ST = topojson.feature(us, us.objects.states).features, CO = topojson.feature(wa, wa.objects.countries).features;
      const pj = d3.geoTransform({ point(x, y) { this.stream.point((x - lon0) / (lon1 - lon0) * RW, (lat1 - y) / (lat1 - lat0) * RH); } });
      regions.forEach((r, i) => { const cv = document.createElement('canvas'); cv.width = RW; cv.height = RH; const g = cv.getContext('2d'), path = d3.geoPath(pj, g);
        const f = r.state ? ST.find((s) => s.properties.name === r.state) : r.country ? CO.find((c) => c.properties.name === r.country) : { type: 'Feature', geometry: { type: 'Polygon', coordinates: [r.ll] } };
        if (!f) throw new Error('không có vùng ' + (r.state || r.country));
        g.fillStyle = '#fff'; g.beginPath(); path(f); g.fill(); const F = g.getImageData(0, 0, RW, RH).data;
        g.clearRect(0, 0, RW, RH); g.strokeStyle = '#fff'; g.lineWidth = r.edgeW || 5; g.lineJoin = 'round'; g.beginPath(); path(f); g.stroke(); const E = g.getImageData(0, 0, RW, RH).data;
        for (let y = 0; y < RH; y++) { const yy = RH - 1 - y; for (let x = 0; x < RW; x++) { const s = (y * RW + x) * 4, d = (yy * RW + x) * 4; fillA[d + i] = F[s + 3]; edgeA[d + i] = E[s + 3]; } } });
    }
    for (let i = 3; i < fillA.length; i += 4) { fillA[i] = 255; edgeA[i] = 255; }
    const dtex = (A) => { const t = new THREE.DataTexture(A, RW, RH, THREE.RGBAFormat); t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.needsUpdate = true; return t; };
    const tFill = dtex(fillA), tEdge = dtex(edgeA);
    const maskAt = (lon, lat) => { const x = Math.round(cl((lon - lon0) / (lon1 - lon0)) * (RW - 1)), y = RH - 1 - Math.round(cl((lat1 - lat) / (lat1 - lat0)) * (RH - 1)), d = (y * RW + x) * 4; return [fillA[d] / 255, fillA[d + 1] / 255, fillA[d + 2] / 255]; };
    const rcol = regions.map((r) => new THREE.Color(r.color || C.teal)); while (rcol.length < 3) rcol.push(new THREE.Color('#ffffff'));
    const U = { tNat: { value: tNat }, tSep: { value: tSep }, tFill: { value: tFill }, tEdge: { value: tEdge }, sep: { value: 0 }, rk: { value: new THREE.Vector3() }, rlift: { value: new THREE.Vector3() },
      rfill: { value: new THREE.Vector3(...[0, 1, 2].map((i) => regions[i] ? regions[i].fill ?? 0.5 : 0)) }, rc0: { value: rcol[0] }, rc1: { value: rcol[1] }, rc2: { value: rcol[2] }, bg: { value: new THREE.Color() }, shOff: { value: new THREE.Vector2(0.0042, -0.0062) } };
    const LIFT_GLSL = 'uniform sampler2D tFill; uniform vec3 rk, rlift; float liftAt(vec2 uv){ return dot(texture2D(tFill, uv).rgb * rk, rlift); }';
    const terr = new THREE.Mesh(geo, new THREE.ShaderMaterial({ uniforms: U, extensions: { derivatives: true },
      vertexShader: `${LIFT_GLSL} varying vec2 vUv; varying vec3 vW; varying vec3 vM;
        void main(){ vUv = uv; vec3 p = position; vM = textureLod(tFill, uv, 1.6).rgb; p.y += dot(vM * rk, rlift);   /* mip ~1,6: tường nổi mượt, không răng cưa theo lưới */ vec4 w = modelMatrix * vec4(p, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `uniform sampler2D tNat, tSep, tFill, tEdge; uniform float sep; uniform vec3 rk, rfill, rc0, rc1, rc2, bg; uniform vec2 shOff; varying vec2 vUv; varying vec3 vW; varying vec3 vM;
        void main(){
          vec3 c = mix(texture2D(tNat, vUv).rgb, texture2D(tSep, vUv).rgb, sep);
          vec3 m = texture2D(tFill, vUv).rgb * rk, e = texture2D(tEdge, vUv).rgb * rk;
          /* bóng đổ của khối nổi lên nền xung quanh (mặt nạ mờ theo mipmap, lệch về Đông Nam) */
          vec3 sh = rk.x + rk.y + rk.z > 0.0005 ? texture2D(tFill, vUv + shOff, 3.5).rgb * rk : vec3(0.0); float shade = max(max(sh.r * (1.0 - m.r), sh.g * (1.0 - m.g)), sh.b * (1.0 - m.b));
          c *= 1.0 - 0.55 * shade;
          vec3 n = normalize(cross(dFdx(vW), dFdy(vW))); float wall = 1.0 - abs(n.y);
          vec3 RC[3]; RC[0] = rc0; RC[1] = rc1; RC[2] = rc2; float MF[3]; MF[0] = m.r; MF[1] = m.g; MF[2] = m.b; float EF[3]; EF[0] = e.r; EF[1] = e.g; EF[2] = e.b; float FL[3]; FL[0] = rfill.x; FL[1] = rfill.y; FL[2] = rfill.z;
          float VM[3]; VM[0] = vM.r; VM[1] = vM.g; VM[2] = vM.b;
          if (rk.x + rk.y + rk.z > 0.0005) for (int i = 0; i < 3; i++) { float k = MF[i]; if (k < 0.002 && EF[i] < 0.002) continue;
            vec3 tint = c * mix(vec3(1.0), RC[i] / max(0.3, dot(RC[i], vec3(0.333))), FL[i]);   /* trộn nhân: giữ nguyên vân tô bóng địa hình */
            c = mix(c, tint * (1.0 + 0.06 * FL[i]), k);
            float wf = clamp(4.0 * VM[i] * (1.0 - VM[i]) * 1.6, 0.0, 1.0) * smoothstep(0.25, 0.7, wall) * step(0.001, rk[i]);   /* tường của khối nổi */
            c = mix(c, RC[i] * 0.42, wf * 0.85);
            c = mix(c, mix(RC[i], vec3(1.0), 0.62), clamp(EF[i] * 1.4, 0.0, 1.0)); }   /* viền sáng kiểu sticker */
          float ed = min(min(vUv.x, 1.0 - vUv.x), min(vUv.y, 1.0 - vUv.y)); c = mix(bg, c, smoothstep(0.0, 0.06, ed));
          gl_FragColor = vec4(c, 1.0); }` }));
    scene.add(terr);
    // ---- máy quay
    const cam = new THREE.PerspectiveCamera(30, W / H, 0.5, 6000); scene.add(cam);
    const camKeys = (o.cam || [{ u: 0, lon: lonc - 0.5, lat: latc, dist: 600, tilt: 25 }, { u: 1, lon: lonc + 0.5, lat: latc, dist: 560, tilt: 28 }]).map((k) => (k.at ? { ...k, lon: LL(k.at)[0], lat: LL(k.at)[1] } : k));
    const ctrack = spline(camKeys, dur, ['lon', 'lat', 'dist', 'tilt', 'head', 'mm']);
    let camDist = 500; const tgt = new THREE.Vector3();
    const place = (t) => { const k = ctrack(t); camDist = k.dist; const tl = (k.tilt || 0) * D2R, hd = (k.head || 0) * D2R;
      tgt.set(X(k.lon), 0.25 * VE, Z(k.lat)); const dir = new THREE.Vector3(Math.sin(hd), 0, -Math.cos(hd));
      cam.position.copy(tgt).addScaledVector(dir, -Math.sin(tl) * k.dist).add(new THREE.Vector3(0, Math.cos(tl) * k.dist, 0));
      cam.up.set(0, 1, 0); if (tl < 0.02) cam.up.copy(dir); cam.lookAt(tgt); cam.fov = fovOf(k.mm || 35); cam.near = Math.max(0.2, k.dist * 0.02); cam.far = k.dist * 8; cam.updateProjectionMatrix(); };
    // ---- độ cao mặt đất tại điểm (kể cả phần nổi của vùng ở thời điểm hiện tại)
    let RK = [0, 0, 0]; const RL = regions.map((r) => r.lift ?? 12);
    const ground = (lon, lat) => { const m = maskAt(lon, lat); let y = hAt(lon, lat); for (let i = 0; i < regions.length; i++) y += m[i] * RK[i] * RL[i]; return y; };
    // ---- tuyến
    let RTS = {}; try { RTS = await loadJSON(base + 'routes.json'); } catch (e) { RTS = {}; }
    const sub = (line, a, b) => { const near = (p) => { let bi = 0, bd = 1e9; line.forEach((q, i) => { const d = Math.hypot(q[0] - p[0], q[1] - p[1]); if (d < bd) { bd = d; bi = i; } }); return bi; };
      let i = a ? near(a) : 0, j = b ? near(b) : line.length - 1; const s = i <= j ? line.slice(i, j + 1) : line.slice(j, i + 1).reverse(); return s; };
    const routePts = (r) => { const out = []; for (const p of r.pts) { if (Array.isArray(p) || typeof p === 'string') out.push(LL(p)); else out.push(...sub(RTS[p.src] || [], p.from && LL(p.from), p.to && LL(p.to))); } return out; };
    const routes = {}, rmeshes = [];
    for (const r of o.routes || []) {
      const ll = routePts(r), P = [];   // lấy mẫu dày ~1,5 km, làm mượt nhẹ
      for (let i = 0; i < ll.length - 1; i++) { const a = ll[i], b = ll[i + 1], n = Math.max(1, Math.ceil(Math.hypot(X(b[0]) - X(a[0]), Z(b[1]) - Z(a[1])) / 1.5)); for (let k = 0; k < n; k++) P.push([lerp(a[0], b[0], k / n), lerp(a[1], b[1], k / n)]); }
      P.push(ll[ll.length - 1]);
      for (let it = 0; it < (r.smooth ?? 3); it++) for (let i = 1; i < P.length - 1; i++) P[i] = [(P[i - 1][0] + 2 * P[i][0] + P[i + 1][0]) / 4, (P[i - 1][1] + 2 * P[i][1] + P[i + 1][1]) / 4];
      const S = [0]; for (let i = 1; i < P.length; i++) S.push(S[i - 1] + Math.hypot(X(P[i][0]) - X(P[i - 1][0]), Z(P[i][1]) - Z(P[i - 1][1])));
      const L = S[S.length - 1], n = P.length, pos = new Float32Array(n * 2 * 3), perp = new Float32Array(n * 2 * 3), side = new Float32Array(n * 2), sArr = new Float32Array(n * 2), msk = new Float32Array(n * 2 * 3), idx = [];
      for (let i = 0; i < n; i++) { const a = P[Math.max(0, i - 1)], b = P[Math.min(n - 1, i + 1)], tx = X(b[0]) - X(a[0]), tz = Z(b[1]) - Z(a[1]), tl = Math.hypot(tx, tz) || 1, m = maskAt(P[i][0], P[i][1]);
        for (let s = 0; s < 2; s++) { const v = i * 2 + s; pos.set([X(P[i][0]), hAt(P[i][0], P[i][1]) + 0.12, Z(P[i][1])], v * 3); perp.set([-tz / tl, 0, tx / tl], v * 3); side[v] = s ? 1 : -1; sArr[v] = S[i]; msk.set(m, v * 3); }
        if (i < n - 1) { const v = i * 2; idx.push(v, v + 1, v + 2, v + 1, v + 3, v + 2); } }
      const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('perp', new THREE.BufferAttribute(perp, 3)); g.setAttribute('side', new THREE.BufferAttribute(side, 1));
      g.setAttribute('s', new THREE.BufferAttribute(sArr, 1)); g.setAttribute('msk', new THREE.BufferAttribute(msk, 3)); g.setIndex(idx);
      const mk = (glow) => new THREE.ShaderMaterial({ transparent: true, depthWrite: false, depthTest: false, blending: glow ? THREE.AdditiveBlending : THREE.NormalBlending,
        uniforms: { rk: U.rk, rlift: U.rlift, wk: { value: 1 }, draw: { value: 0 }, flow: { value: 0 }, dash: { value: r.style === 'dashed' ? 1 : 0 }, dl: { value: r.dl || 9 }, col: { value: new THREE.Color(r.color || C.amber) }, ink: { value: new THREE.Color(r.ink || '#1a1208') }, a: { value: 1 } },
        vertexShader: `attribute vec3 perp; attribute float side, s; attribute vec3 msk; uniform vec3 rk, rlift; uniform float wk; varying float vS, vSide;
          void main(){ vS = s; vSide = side; vec3 p = position + perp * side * wk; p.y += dot(msk * rk, rlift); gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0); }`,
        fragmentShader: `uniform float draw, flow, dash, dl, a; uniform vec3 col, ink; varying float vS, vSide;
          void main(){ if (vS > draw) discard; float e = abs(vSide);
            ${glow ? 'float al = (1.0 - e * e) * 0.55 * a; gl_FragColor = vec4(col * al, al);' :
              'if (dash > 0.5 && fract((vS - flow) / dl) > 0.58) discard; vec3 c = mix(col, ink, smoothstep(0.62, 0.9, e)); gl_FragColor = vec4(c, a * (1.0 - smoothstep(0.92, 1.0, e)));'} }` });
      const line = new THREE.Mesh(g, mk(false)), glow = new THREE.Mesh(g, mk(true)); line.renderOrder = 6; glow.renderOrder = 5; scene.add(glow, line);
      const head = glowSprite(r.color || C.amber, 2.0, 0.5); head.renderOrder = 7; head.material.depthTest = false; scene.add(head);
      const at = (u) => { const sv = cl(u) * L; let i = 0; while (i < n - 2 && S[i + 1] < sv) i++; const f = (sv - S[i]) / Math.max(1e-6, S[i + 1] - S[i]); return [lerp(P[i][0], P[i + 1][0], f), lerp(P[i][1], P[i + 1][1], f)]; };
      routes[r.id] = { r, L, at }; rmeshes.push({ r, line, glow, head, L, at }); }
    // ---- vòng sáng
    const rings = [];
    for (const R of o.rings || []) { const [lon, lat] = LL(R.at); const m = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
        uniforms: { ph: { value: 0 }, a: { value: 0 }, col: { value: new THREE.Color(R.color || '#ffe6b0') } },
        vertexShader: 'varying vec2 vU; void main(){ vU = uv * 2.0 - 1.0; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
        fragmentShader: `uniform float ph, a; uniform vec3 col; varying vec2 vU; void main(){ float r = length(vU); float v = 0.0;
          for (int k = 0; k < 3; k++) { float p = fract(ph + float(k) / 3.0); float rr = 0.15 + 0.85 * p; v += (1.0 - p) * smoothstep(0.045, 0.0, abs(r - rr)); }
          v += smoothstep(0.16, 0.0, r) * 0.9; v *= a * step(r, 1.0); gl_FragColor = vec4(col * v, v); }` }));
      m.rotation.x = -Math.PI / 2; m.renderOrder = 4; scene.add(m); rings.push({ R, m, lon, lat }); }
    // ---- chồng xu / cột (tỷ lệ thật: mỗi đồng = unit; cột cao v km)
    scene.environment = envMap(renderer);
    scene.add(new THREE.HemisphereLight('#fff6e6', '#3a3226', 0.9)); const sun = new THREE.DirectionalLight('#fff1d8', 2.4); sun.position.set(-300, 500, -200); scene.add(sun);
    const anchors = {}, cols = [];
    const shadowTex = (() => { const cv = document.createElement('canvas'); cv.width = cv.height = 128; const g = cv.getContext('2d'), gr = g.createRadialGradient(64, 64, 4, 64, 64, 62); gr.addColorStop(0, 'rgba(0,0,0,0.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(cv); })();
    for (const c of o.cols || []) { const [lon, lat] = LL(c.at), x = X(lon) + (c.dx || 0), z = Z(lat) + (c.dy || 0), lonA = lon + (c.dx || 0) / kx, latA = lat - (c.dy || 0) / kz;
      const grp = new THREE.Group(); scene.add(grp); const r = c.r || 7, items = [];
      const sh = new THREE.Mesh(new THREE.PlaneGeometry(r * 3.4, r * 3.4), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })); sh.rotation.x = -Math.PI / 2; sh.position.y = 0.15; sh.renderOrder = 3; grp.add(sh);
      if ((c.kind || 'coins') === 'coins') { const th = c.th || r * 0.24, n = c.n ?? Math.round(c.v / (c.unit || 1));
        const gold = new THREE.MeshStandardMaterial({ color: c.color || '#e8b54a', metalness: 0.55, roughness: 0.3, envMapIntensity: 1.6, emissive: '#5a3a08', emissiveIntensity: 0.35 }), rim = new THREE.MeshStandardMaterial({ color: '#c99a3a', metalness: 0.6, roughness: 0.4, emissive: '#3a2604', emissiveIntensity: 0.3 });   /* nháp V2: metalness 1 + phòng phản xạ tối → xu nâu đen; vàng sáng như sticker */
        const cg = new THREE.CylinderGeometry(r, r, th * 0.86, 56), eg = new THREE.TorusGeometry(r * 0.97, th * 0.07, 6, 56); eg.rotateX(Math.PI / 2);
        for (let i = 0; i < n; i++) { const g = new THREE.Group(); g.add(new THREE.Mesh(cg, gold)); const e1 = new THREE.Mesh(eg, rim); e1.position.y = th * 0.43; const e2 = e1.clone(); e2.position.y = -th * 0.43; g.add(e1, e2);
          g.userData = { y: th * (i + 0.5), rz: (Math.sin(i * 12.9898) * 0.5) * 0.06, ox: Math.sin(i * 78.233) * r * 0.05, oz: Math.cos(i * 37.71) * r * 0.05 }; grp.add(g); items.push(g); }
        cols.push({ c, grp, items, x, z, lon: lonA, lat: latA, top: () => th * items.filter((g) => g.visible).length, sh });
      } else { const m = new THREE.MeshStandardMaterial({ color: c.color || C.orange, roughness: 0.4, metalness: 0.1 }), b = new THREE.Mesh(new THREE.BoxGeometry(r * 1.6, 1, r * 1.6), m); grp.add(b); items.push(b);
        cols.push({ c, grp, items, x, z, lon: lonA, lat: latA, top: () => b.scale.y, bar: b, sh }); }
      const cc = cols[cols.length - 1], tp = new THREE.Vector3(), pl = new THREE.Vector3(), pr = new THREE.Vector3(), rgt = new THREE.Vector3();
      anchors['col:' + c.id] = () => tp.set(cc.x, cc.grp.position.y + cc.top() + 0.6, cc.z);
      // mép trái/phải ở chân (theo hướng phải của máy quay) → lớp 2D dựng hộp chiếu của chồng xu để nhãn né (BAI-HOC-K2 K11)
      anchors['colL:' + c.id] = () => { rgt.setFromMatrixColumn(cam.matrixWorld, 0).setY(0).normalize().multiplyScalar(r * 1.1); return cc.grp.visible ? pl.set(cc.x, cc.grp.position.y, cc.z).sub(rgt) : null; };
      anchors['colR:' + c.id] = () => { rgt.setFromMatrixColumn(cam.matrixWorld, 0).setY(0).normalize().multiplyScalar(r * 1.1); return cc.grp.visible ? pr.set(cc.x, cc.grp.position.y, cc.z).add(rgt) : null; }; }
    // ---- neo
    for (const p of o.places || []) { const id = typeof p === 'string' ? p : p.id, [lon, lat] = LL(id), v = new THREE.Vector3(); anchors[id] = () => v.set(X(lon), ground(lon, lat) + 0.2, Z(lat)); }
    for (const p of o.pins || []) { const [lon, lat] = LL(p.at), v = new THREE.Vector3(); anchors['st:' + p.id] = () => v.set(X(lon) + (p.dx || 0), ground(lon, lat) + (p.dy || 0.3), Z(lat) + (p.dz || 0)); }
    const walkers = (o.walkers || []).map((w) => { const v = new THREE.Vector3(); let cur = null; anchors['st:' + w.id] = () => cur; return { w, v, set(t) { const R = routes[w.route]; if (!R) return; const uu = w.u || [0, 1], u = lerp(uu[0], uu[1], cl((t - w.t[0]) / (w.t[1] - w.t[0])));
      const [lon, lat] = R.at(u); cur = v.set(X(lon), ground(lon, lat) + 0.3, Z(lat)); } }; });
    for (const R of rmeshes) anchors['rt:' + R.r.id] = () => R.head.visible ? R.head.position : null;
    // ---- palette
    const sepAt = (t) => o.palette === 'sepia' ? 1 : o.sepia ? ease(cl((t - o.sepia[0]) / (o.sepia[1] - o.sepia[0]))) : o.natural ? 1 - ease(cl((t - o.natural[0]) / (o.natural[1] - o.natural[0]))) : 0;
    const BGN = new THREE.Color('#8fa3ab'), BGS = new THREE.Color('#bba985');   // mù nền cùng tông bảng màu (mép bản đồ không lộ khối tối)
    place(0);
    const self = { scene, cam, grade: o.grade || 'info', exposure: o.exposure || 1.0, anchors,
      update(t) { place(t); const sp = sepAt(t); U.sep.value = sp; U.bg.value.copy(BGN).lerp(BGS, sp); scene.background = U.bg.value;
        RK = regions.map((r) => { const a = Array.isArray(r.at) ? eo(cl((t - r.at[0]) / Math.max(0.01, r.at[1] - r.at[0]))) : win(r.at, t, 1.0); return r.out !== undefined ? a * (1 - ease(cl((t - r.out) / 0.8))) : a; });
        U.rk.value.set(RK[0] || 0, RK[1] || 0, RK[2] || 0); U.rlift.value.set(RL[0] || 0, RL[1] || 0, RL[2] || 0);
        const wk = 2 * camDist * Math.tan(cam.fov * D2R / 2) / 1080;   // km ứng với 1 px của khung 1080p ở tâm khung (độ dày nét, cỡ vòng sáng theo px)
        for (const R of rmeshes) { const u = win(R.r.draw, t), d = u * R.L; for (const m of [R.line, R.glow]) { m.material.uniforms.draw.value = d; m.material.uniforms.flow.value = t * (R.r.flow ?? 6); m.material.uniforms.a.value = R.r.out !== undefined ? 1 - ease(cl((t - R.r.out) / 0.6)) : 1; }
          R.line.material.uniforms.wk.value = wk * (R.r.w || 7) / 2; R.glow.material.uniforms.wk.value = wk * (R.r.w || 7) * 1.6;
          R.head.visible = u > 0.002 && u < 0.998; if (R.head.visible) { const [lon, lat] = R.at(u); R.head.position.set(X(lon), ground(lon, lat) + 0.5, Z(lat)); R.head.scale.setScalar(wk * 46); } }
        for (const g of rings) { const a = win(g.R.t, t, 0.5) * (g.R.out !== undefined ? 1 - ease(cl((t - g.R.out) / 0.6)) : 1); g.m.visible = a > 0.001; g.m.material.uniforms.a.value = a; g.m.material.uniforms.ph.value = (t * 0.55) % 1;
          g.m.position.set(X(g.lon), ground(g.lon, g.lat) + 0.25, Z(g.lat)); g.m.scale.setScalar(g.R.r || wk * (g.R.px || 80)); }
        for (const cc of cols) { const y0 = ground(cc.lon, cc.lat); cc.grp.position.set(cc.x, y0, cc.z); const [t0, t1] = cc.c.t || [0, 0.01];
          if (cc.bar) { const u = eo(cl((t - t0) / (t1 - t0))); cc.bar.scale.y = Math.max(0.001, u * cc.c.v); cc.bar.position.y = cc.bar.scale.y / 2; cc.grp.visible = u > 0.001; }
          else { const n = cc.items.length, step = n > 1 ? (t1 - t0) / n : 0; cc.items.forEach((g, i) => { const ti = t0 + i * step, u = cl((t - ti) / 0.32); g.visible = u > 0; const d = g.userData;   // rơi xuống + nảy nhẹ
            g.position.set(d.ox, d.y + (1 - eo(u)) * 6 + Math.sin(cl(u * 1.4) * Math.PI) * 0.0, d.oz); g.rotation.z = d.rz * (1 - u) * 6 + d.rz; });
            cc.grp.visible = cc.items.some((g) => g.visible); cc.sh.material.opacity = cc.grp.visible ? 1 : 0; } }
        for (const w of walkers) w.set(t);
      } };
    return self;
  },
};

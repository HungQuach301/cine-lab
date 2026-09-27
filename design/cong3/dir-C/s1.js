// Hướng C — khung s1_opening: toàn cảnh cao, cuối chạng vạng. Trời hồng → tím; Ostler Street cong, dốc xuống xa máy;
// 11 cột đèn khí (1–4 đã sáng, Ida vừa thắp số 4), cột điện kiểu mới xen giữa (chưa bật), đồng hồ điện ở quảng trường (chưa sáng).
// Máy ở sau–trên quảng trường ~40 m, chúc ~22°, nhìn dọc phố xuống dốc về phía ráng chiều.
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { buildCharacter } from '../shared/cast.js';
import { rng, glowSprite } from './common.js';

// ---------- tiện ích hình học ----------
function mergeGeos(list) {
  const geos = list.map((g) => (g.index ? g.toNonIndexed() : g));
  let n = 0; for (const g of geos) n += g.attributes.position.count;
  const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3), col = new Float32Array(n * 3);
  let o = 0;
  for (const g of geos) {
    const c = g.attributes.position.count;
    pos.set(g.attributes.position.array, o * 3);
    if (!g.attributes.normal) g.computeVertexNormals();
    nor.set(g.attributes.normal.array, o * 3);
    if (g.attributes.color) col.set(g.attributes.color.array, o * 3); else col.fill(1, o * 3, (o + c) * 3);
    o += c;
  }
  const m = new THREE.BufferGeometry();
  m.setAttribute('position', new THREE.BufferAttribute(pos, 3)); m.setAttribute('normal', new THREE.BufferAttribute(nor, 3)); m.setAttribute('color', new THREE.BufferAttribute(col, 3));
  return m;
}
const paint = (g, c) => { g = g.index ? g.toNonIndexed() : g; const n = g.attributes.position.count, a = new Float32Array(n * 3); for (let i = 0; i < n; i++) { a[3 * i] = c.r; a[3 * i + 1] = c.g; a[3 * i + 2] = c.b; } g.setAttribute('color', new THREE.BufferAttribute(a, 3)); return g; };
const place = (g, x, y, z, ry = 0) => { g.rotateY(ry); g.translate(x, y, z); return g; };

// Mái dốc hai mái (lăng trụ tam giác) dài L (theo x cục bộ), rộng D (theo z), cao h; đáy tại y = 0.
function roofGeo(L, D, h, over = 0.25, hip = 0) {
  const hx = L / 2 + over, hz = D / 2 + over;
  if (hip > 0) { // mái chóp bốn mặt: đỉnh ngắn hơn
    const rx = Math.max(0.2, hx - hip);
    const v = [-hx, 0, hz, hx, 0, hz, rx, h, 0, -hx, 0, hz, rx, h, 0, -rx, h, 0,
      hx, 0, -hz, -hx, 0, -hz, -rx, h, 0, hx, 0, -hz, -rx, h, 0, rx, h, 0,
      -hx, 0, -hz, -hx, 0, hz, -rx, h, 0, hx, 0, hz, hx, 0, -hz, rx, h, 0];
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(v), 3)); g.computeVertexNormals(); return g;
  }
  const v = [
    // hai mái
    -hx, 0, hz, hx, 0, hz, hx, h, 0, -hx, 0, hz, hx, h, 0, -hx, h, 0,
    hx, 0, -hz, -hx, 0, -hz, -hx, h, 0, hx, 0, -hz, -hx, h, 0, hx, h, 0,
    // hai đầu hồi
    -L / 2, 0, -D / 2, -L / 2, 0, D / 2, -L / 2, h, 0, L / 2, 0, D / 2, L / 2, 0, -D / 2, L / 2, h, 0,
  ];
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(v), 3)); g.computeVertexNormals(); return g;
}

// ---------- đường cong phố ----------
const OSTLER = new THREE.CatmullRomCurve3([[0, -16], [-2, -46], [3, -74], [16, -98], [36, -114], [60, -123], [86, -126]].map(([x, z]) => new THREE.Vector3(x, 0, z)), false, 'centripetal');
export const groundY = (x, z) => 0.035 * Math.min(z, 0) + 0.03 * Math.min(0, z + 240) + 0.4 * Math.sin(x * 0.03) * Math.min(1, -z / 60);

// Sương theo chiều sâu nhưng MÀU sương đổi theo độ cao trên khung (gần chân trời hồng-đào, xuống thấp tím-lam):
// cách vẽ không khí của tranh luminist. Ghi đè chunk fog của three (chỉ ảnh hưởng vật liệu có fog; cảnh s5 không có fog).
function paintedFog(Hpx, top, mid, bot) {
  const L = (c) => new THREE.Color(c); const v = (c) => `vec3(${L(c).r.toFixed(4)}, ${L(c).g.toFixed(4)}, ${L(c).b.toFixed(4)})`;
  THREE.ShaderChunk.fog_fragment = THREE.ShaderChunk.fog_fragment.replace('gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );',
    `float fyy = gl_FragCoord.y / ${Hpx.toFixed(1)};
	vec3 fogC = mix(${v(bot)}, ${v(mid)}, smoothstep(0.0, 0.6, fyy)); fogC = mix(fogC, ${v(top)}, smoothstep(0.55, 0.95, fyy));
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogC * fogColor, fogFactor );`);
}

export async function buildS1(ida, Hpx = 1080, dbg = {}) {
  paintedFog(Hpx, '#d99aa0', '#a386ad', '#6a679c');
  const R = rng(1901);
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(new THREE.Color(1, 1, 1), 0.0027);

  // ---------- trời ----------
  const sky = new THREE.Mesh(new THREE.SphereGeometry(3000, 64, 32), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { sunDir: { value: new THREE.Vector3(0.18, 0.0, -1).normalize() } },
    vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `varying vec3 vD; uniform vec3 sunDir;
      float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
      float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f); return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
      vec3 lin(vec3 c){ return pow(c, vec3(2.2)); }
      void main(){
        vec3 d = normalize(vD); float el = asin(clamp(d.y, -1.0, 1.0));
        float sunA = max(dot(normalize(vec3(d.x, 0.0, d.z)), normalize(vec3(sunDir.x, 0.0, sunDir.z))), 0.0);
        float t = clamp(el / 0.11, 0.0, 1.0);
        vec3 zen = lin(vec3(0.16, 0.17, 0.36)), up = lin(vec3(0.33, 0.29, 0.55)), mid = lin(vec3(0.58, 0.43, 0.66)), low = lin(vec3(0.86, 0.56, 0.62)), hor = lin(vec3(0.98, 0.72, 0.60));
        vec3 c = mix(low, mid, smoothstep(0.02, 0.16, t)); c = mix(c, up, smoothstep(0.14, 0.45, t)); c = mix(c, zen, smoothstep(0.45, 1.0, t));
        float glow = pow(sunA, 5.0) * exp(-max(el, 0.0) * 70.0);
        c = mix(c, hor, clamp(glow * 1.1 + (1.0 - smoothstep(0.0, 0.05, t)) * 0.35 * sunA, 0.0, 1.0));
        // dải mây tầng mỏng, đáy ửng hồng
        float band = smoothstep(0.006, 0.014, el) * (1.0 - smoothstep(0.03, 0.05, el));
        vec2 q = vec2(atan(d.x, -d.z) * 7.0, el * 320.0);
        float cl = vn(q * vec2(1.0, 1.0)) * 0.6 + vn(q * vec2(2.3, 2.1) + 7.0) * 0.4; cl = smoothstep(0.52, 0.8, cl) * band;
        c = mix(c, mix(lin(vec3(0.62, 0.42, 0.56)), lin(vec3(1.0, 0.66, 0.55)), 0.4 + 0.6 * sunA), cl * 0.75);
        if (el < 0.0) c = mix(lin(vec3(0.88, 0.65, 0.62)), lin(vec3(0.66, 0.53, 0.68)), smoothstep(0.0, 0.2, -el));
        gl_FragColor = vec4(c * 1.05, 1.0);
      }` }));
  sky.userData.noG = false; scene.add(sky);

  // ---------- ánh sáng chạng vạng ----------
  const hemi = new THREE.HemisphereLight('#8a86c8', '#3b2d3a', 0.85); scene.add(hemi);
  const after = new THREE.DirectionalLight('#ff9e8e', 0.55); after.position.set(-40, 25, -300); scene.add(after); // ráng chiều phía xa, không bóng
  const skyFill = new THREE.DirectionalLight('#6f7bd0', 0.25); skyFill.position.set(60, 120, 120); scene.add(skyFill);

  // ---------- nền đất, phố, vỉa hè ----------
  const groundMat = new THREE.MeshLambertMaterial({ vertexColors: true });
  {
    const g = new THREE.PlaneGeometry(1400, 1400, 140, 140); g.rotateX(-Math.PI / 2); g.translate(0, 0, -500);
    const p = g.attributes.position; const col = new Float32Array(p.count * 3);
    for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i); p.setY(i, groundY(x, z) - 0.05); const k = 0.9 + R() * 0.1; col[3 * i] = 0.20 * k; col[3 * i + 1] = 0.18 * k; col[3 * i + 2] = 0.19 * k; }
    g.setAttribute('color', new THREE.BufferAttribute(col, 3)); g.computeVertexNormals();
    const m = new THREE.Mesh(g, groundMat); m.receiveShadow = true; scene.add(m);
  }
  const ribbon = (curve, off0, off1, lift, color, segs = 220) => {
    const pos = [], cols = []; const c = new THREE.Color(color);
    for (let i = 0; i < segs; i++) {
      for (const [a, b] of [[i, i + 1]]) {
        const P = [a, b].map((k) => { const t = k / segs; const p = curve.getPointAt(t), tg = curve.getTangentAt(t); const n = new THREE.Vector3(-tg.z, 0, tg.x).normalize(); return [p, n]; });
        const v = (pn, off) => { const x = pn[0].x + pn[1].x * off, z = pn[0].z + pn[1].z * off; return [x, groundY(x, z) + lift, z]; };
        const A = v(P[0], off0), B = v(P[0], off1), C = v(P[1], off1), D = v(P[1], off0);
        pos.push(...A, ...C, ...B, ...A, ...D, ...C);
        for (let k = 0; k < 6; k++) { const j = 0.93 + R() * 0.1; cols.push(c.r * j, c.g * j, c.b * j); }
      }
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); g.computeVertexNormals();
    const m = new THREE.Mesh(g, groundMat); m.receiveShadow = true; return m;
  };
  scene.add(ribbon(OSTLER, -3.6, 3.6, 0.03, '#7d7486'));       // lòng đường đá cuội (ẩm, bắt ánh trời → dải sáng dẫn mắt)
  scene.add(ribbon(OSTLER, 3.6, 5.6, 0.12, '#8a8088'));        // vỉa hè
  scene.add(ribbon(OSTLER, -5.6, -3.6, 0.12, '#8a8088'));

  // ---------- nhà ----------
  const walls = [], roofs = [], wins = [], chims = [];
  const wallCols = ['#8a5a48', '#9b6a52', '#7a4f45', '#a88a6e', '#b49a7c', '#8c7a6a', '#6e5a58', '#a07058', '#c2ad90'].map((c) => new THREE.Color(c));
  const roofCols = ['#4a4c5c', '#55505a', '#5e4640', '#434556', '#6a4a40'].map((c) => new THREE.Color(c));
  const winDark = new THREE.Color('#1d1b26'), winLit = new THREE.Color('#ffb060');
  const houseList = [];
  // vùng phía trong khúc cong (bên phải phố, sau đoạn đầu): nhà thấp một tầng — phố men sườn dốc, nhìn thấy chuỗi đèn
  const OS = Array.from({ length: 121 }, (_, i) => { const t = i / 120; return { t, p: OSTLER.getPointAt(t), tg: OSTLER.getTangentAt(t) }; });
  const innerLow = (x, z) => { let best = null, bd = 1e9; for (const o of OS) { const d = (o.p.x - x) ** 2 + (o.p.z - z) ** 2; if (d < bd) { bd = d; best = o; } }
    const sd = (x - best.p.x) * (-best.tg.z) + (z - best.p.z) * best.tg.x; return best.t > 0.14 && sd > 0 && bd < 75 * 75; };
  function house(x, z, ry, L, D, Hh, opts = {}) {
    if (!opts.keepH && innerLow(x, z)) Hh = 4.0 + R() * 1.8;
    const y0 = Math.min(groundY(x, z), groundY(x + Math.cos(ry) * L / 2, z - Math.sin(ry) * L / 2), groundY(x - Math.cos(ry) * L / 2, z + Math.sin(ry) * L / 2)) - 0.6;
    const wc = opts.wall || wallCols[Math.floor(R() * wallCols.length)].clone().multiplyScalar(0.9 + R() * 0.2);
    const top = groundY(x, z) + Hh;
    const H0 = top - y0;
    walls.push(paint(place(new THREE.BoxGeometry(L, H0, D), x, y0 + H0 / 2, z, ry), wc));
    const rh = D * (0.32 + R() * 0.12);
    roofs.push(paint(place(roofGeo(L, D, rh, 0.25, R() < 0.3 ? D * 0.45 : 0), x, top, z, ry), (opts.roof || roofCols[Math.floor(R() * roofCols.length)]).clone().multiplyScalar(0.85 + R() * 0.3)));
    // ống khói ở đầu hồi
    const nch = R() < 0.8 ? (R() < 0.4 ? 2 : 1) : 0;
    for (let k = 0; k < nch; k++) {
      const s = k === 0 ? -1 : 1, cx = s * (L / 2 - 0.4), cz = (R() - 0.5) * D * 0.3, ch = rh + 1.0 + R() * 1.2;
      const g = new THREE.BoxGeometry(0.7, ch, 1.1 + R() * 0.6); g.translate(cx, top + ch / 2 - 0.2, cz); g.rotateY(0);
      const gg = g.clone(); gg.translate(-x, 0, -z); // về gốc để xoay đúng quanh tâm nhà
      const t = new THREE.Matrix4().makeRotationY(ry); const p = new THREE.BufferGeometry().copy(g); p.translate(0, 0, 0);
      const cg = new THREE.BoxGeometry(0.7, ch, 1.1 + R() * 0.6); cg.translate(cx, top + ch / 2 - 0.2, cz); cg.applyMatrix4(t); cg.translate(x, 0, z);
      chims.push(paint(cg, wc.clone().multiplyScalar(0.8)));
      // chóp ống khói (2 ống sành nhỏ)
      for (let j = 0; j < 2; j++) { const pg = new THREE.CylinderGeometry(0.12, 0.14, 0.5, 6); pg.translate(cx, top + ch - 0.2 + 0.25, cz + (j - 0.5) * 0.4); pg.applyMatrix4(t); pg.translate(x, 0, z); chims.push(paint(pg, new THREE.Color('#7a5044'))); }
    }
    // cửa sổ trên mặt trước (+z cục bộ) và sau
    if (opts.windows !== false) {
      const floors = Math.max(1, Math.floor((Hh - 1.0) / 3.1)); const nw = Math.max(1, Math.round(L / 2.4));
      for (const side of [1, -1]) for (let f = 0; f < floors; f++) for (let w = 0; w < nw; w++) {
        const wx = -L / 2 + (w + 0.5) * L / nw, wy = groundY(x, z) + 1.4 + f * 3.1 + 0.9;
        if (wy + 0.9 > top - 0.2) continue;
        const lit = R() < (opts.litP ?? 0.07);
        const c = lit ? winLit.clone().multiplyScalar(0.35 + R() * 0.8) : winDark.clone().multiplyScalar(0.8 + R() * 0.6);
        const g = new THREE.PlaneGeometry(0.95, 1.5); if (side < 0) g.rotateY(Math.PI); g.translate(wx, wy, side * (D / 2 + 0.02));
        g.applyMatrix4(new THREE.Matrix4().makeRotationY(ry)); g.translate(x, 0, z);
        wins.push(paint(g, c));
      }
    }
    houseList.push({ x, z, r: Math.max(L, D) / 2 });
  }
  // dãy nhà dọc một đường cong (cả hai bên)
  function terrace(curve, halfW, t0, t1, opts = {}) {
    for (const side of [-1, 1]) {
      let t = t0; const len = curve.getLength();
      while (t < t1) {
        const L = 5 + R() * 3.5; const dt = L / len;
        const tm = Math.min(t + dt / 2, 0.9999);
        const p = curve.getPointAt(tm), tg = curve.getTangentAt(tm); const nrm = new THREE.Vector3(-tg.z, 0, tg.x).normalize();
        const D = 8 + R() * 3; const off = halfW + D / 2 + R() * 0.3;
        const x = p.x + nrm.x * off * side, z = p.z + nrm.z * off * side;
        const ry = Math.atan2(-tg.z, tg.x) + (side > 0 ? Math.PI : 0);   // mặt trước (+z cục bộ) quay ra phố
        const low = opts.lowSide && side === opts.lowSide && tm > (opts.lowFrom ?? 0);
        const Hh = low ? 4.2 + R() * 1.6 : (opts.hMin ?? 7) + R() * (opts.hVar ?? 5);
        if (!opts.avoid || !opts.avoid(x, z)) house(x, z, ry, L + 0.05, D, Hh, opts);
        t += dt;
      }
    }
  }
  const nearOstler = (x, z, d) => { for (let i = 0; i <= 60; i++) { const p = OSTLER.getPointAt(i / 60); if ((p.x - x) ** 2 + (p.z - z) ** 2 < d * d) return true; } return false; };
  terrace(OSTLER, 5.8, 0.0, 0.985, { hMin: 7.5, hVar: 6, litP: 0.035, lowSide: 1, lowFrom: 0.12 });  // phía trong khúc cong: nhà một tầng (phố men sườn dốc) → thấy chuỗi đèn
  // phố khác của thành phố (song song và cắt ngang), nhà thấp dần theo xa
  const others = [];
  const mkCurve = (pts) => new THREE.CatmullRomCurve3(pts.map(([x, z]) => new THREE.Vector3(x, 0, z)), false, 'centripetal');
  for (const dx of [-46, -92, -140, 50, 98, 150]) others.push(mkCurve([[dx * 0.8, 10], [dx + 5, -60], [dx + 18, -130], [dx + 10, -210], [dx - 5, -300], [dx - 18, -420], [dx - 10, -600]]));
  for (const zc of [-70, -140, -250, -330, -420, -520]) others.push(mkCurve([[-260, zc + 8], [-120, zc - 4], [0, zc + 6], [120, zc - 6], [260, zc + 4]]));
  const avoidAll = (x, z) => nearOstler(x, z, 17) || houseList.some((h) => (h.x - x) ** 2 + (h.z - z) ** 2 < (h.r + 2.5) ** 2) || (x * x + (z - 4) * (z - 4) < 31 * 31);
  for (const c of others) terrace(c, 5.0, 0.0, 1.0, { hMin: 6.5, hVar: 6, litP: 0.03, avoid: avoidAll });

  // nhà kho cuối phố: tường gạch quét vôi trắng, dài, mái thấp
  { const p = OSTLER.getPointAt(1.0), tg = OSTLER.getTangentAt(1.0); house(p.x + tg.x * 12, p.z + tg.z * 12, Math.atan2(-tg.x, -tg.z), 46, 18, 11, { wall: new THREE.Color('#e2dccf'), roof: new THREE.Color('#57535c'), windows: false, keepH: true }); }
  // quảng trường: nhà công cộng lớn hai bên
  // nhà vây quanh quảng trường (mặt quay vào trong), chừa lối ra Ostler Street (hướng −z) và một phố về phía máy (+z)
  for (let a = -Math.PI; a < Math.PI; ) {
    const L = 7 + R() * 5, r = 18 + 6; const da = L / r; const am = a + da / 2;
    const dz = Math.cos(am), dx = Math.sin(am);  // hướng từ tâm
    if (Math.abs(Math.atan2(dx, -dz)) > 0.42 && Math.abs(Math.atan2(dx, dz)) > 0.35) house(dx * r, 4 + dz * r, Math.atan2(-dx, -dz), L, 11, 10 + R() * 5, { litP: 0.06 });
    a += da;
  }
  // mốc xa: tháp chuông, ống khói nhà máy (bóng khối trong sương)
  const landmarks = [];
  { const x = -70, z = -470, y = groundY(x, z);
    landmarks.push(paint(place(new THREE.BoxGeometry(8, 34, 8), x, y + 17, z), new THREE.Color('#8a7a78')));
    landmarks.push(paint(place(new THREE.ConeGeometry(6.2, 16, 4), x, y + 42, z, Math.PI / 4), new THREE.Color('#5a5260'))); }
  for (const [x, z, h] of [[140, -560, 46], [165, -600, 38]]) { const y = groundY(x, z); landmarks.push(paint(place(new THREE.CylinderGeometry(1.6, 2.6, h, 12), x, y + h / 2, z), new THREE.Color('#7a6260'))); }

  const wallMat = new THREE.MeshLambertMaterial({ vertexColors: true });
  const roofMat = new THREE.MeshLambertMaterial({ vertexColors: true });
  const winMat = new THREE.MeshBasicMaterial({ vertexColors: true });
  for (const [list, mat] of [[walls, wallMat], [roofs, roofMat], [chims, wallMat], [landmarks, wallMat]]) {
    const m = new THREE.Mesh(mergeGeos(list), mat); m.castShadow = false; m.receiveShadow = true; scene.add(m);  // chỉ Ida đổ bóng (spot đèn số 3): tránh vẽ cả thành phố vào shadow map mỗi mẫu
  }
  scene.add(new THREE.Mesh(mergeGeos(wins), winMat));

  // ---------- quảng trường: lát đá sáng hơn, cột đồng hồ điện (chưa sáng) ----------
  { const g = new THREE.CircleGeometry(18.5, 48); g.rotateX(-Math.PI / 2); g.translate(0, groundY(0, 0) + 0.06, 4); const m = new THREE.Mesh(g, new THREE.MeshLambertMaterial({ color: '#76696c' })); m.receiveShadow = true; scene.add(m); }
  const iron = new THREE.MeshLambertMaterial({ color: '#2a2a30' });
  const clock = new THREE.Group(); clock.position.set(2.5, groundY(2.5, -6), -6); scene.add(clock); clock.userData.imp = 1;
  { clock.add(new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.26, 6, 12).translate(0, 3, 0), iron));
    clock.add(new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 0.8, 12).translate(0, 0.4, 0), iron));
    const head = new THREE.Group(); head.position.set(0, 6.6, 0); head.rotation.y = -0.35; clock.add(head);
    for (const s of [1, -1]) { // hai mặt (trước/sau)
      const face = new THREE.Mesh(new THREE.CircleGeometry(0.6, 40), new THREE.MeshLambertMaterial({ color: '#d9d6e4', emissive: new THREE.Color('#8e86b0'), emissiveIntensity: 0.25 })); // kính mờ tắt: bắt ánh trời face.position.z = s * 0.14; if (s < 0) face.rotation.y = Math.PI; head.add(face);
      for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2; const bar = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.16), new THREE.MeshBasicMaterial({ color: '#141418' }));
        bar.position.set(Math.sin(a) * 0.48, Math.cos(a) * 0.48, s * 0.145); bar.rotation.z = -a; if (s < 0) bar.rotation.y = Math.PI; head.add(bar); }
      const hand = (len, ang, w) => { const h = new THREE.Mesh(new THREE.PlaneGeometry(w, len).translate(0, len / 2 - 0.04, 0), new THREE.MeshBasicMaterial({ color: '#141418' })); h.position.z = s * 0.15; h.rotation.z = -ang; if (s < 0) h.rotation.y = Math.PI; head.add(h); };
      hand(0.52, 0.0, 0.035); hand(0.34, -0.55, 0.05);
    }
    const rim = new THREE.Mesh(new THREE.CylinderGeometry(0.64, 0.64, 0.28, 40, 1, true).rotateX(Math.PI / 2), iron); head.add(rim);
    const capG = new THREE.Mesh(new THREE.SphereGeometry(0.18, 12, 8), iron); capG.position.y = 0.75; head.add(capG);
  }

  // ---------- đèn khí 11 cột + cột điện ----------
  const lampPos = [], lampMeshes = [];
  const Llen = OSTLER.getLength();
  const lampS = Array.from({ length: 11 }, (_, i) => 10 + i * (Llen - 22) / 10);
  const gasGlassOff = new THREE.MeshBasicMaterial({ color: new THREE.Color('#b8b4d8').multiplyScalar(0.9) }); // kính chưa thắp: bắt ánh trời tím nhạt
  const gasGlassOn = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb458').multiplyScalar(9) });
  const JUST = 2;                 // ngọn vừa thắp (số 3); 1–3 sáng, 4–11 chưa
  const lit = [0, 1, 2];
  const glowAll = [];
  lampS.forEach((s, i) => {
    const t = s / Llen, p = OSTLER.getPointAt(t), tg = OSTLER.getTangentAt(t); const nrm = new THREE.Vector3(-tg.z, 0, tg.x).normalize();
    const side = 1; const x = p.x + nrm.x * 4.1 * side, z = p.z + nrm.z * 4.1 * side, y = groundY(x, z) + 0.12;
    const g = new THREE.Group(); g.position.set(x, y, z); scene.add(g);
    g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.1, 3.0, 8).translate(0, 1.5, 0), iron));
    g.add(new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.05, 0.05).translate(0, 2.75, 0), iron));  // thanh gác thang
    const on = lit.includes(i);
    g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.14, 0.45, 4).rotateY(Math.PI / 4).translate(0, 3.22, 0), on ? gasGlassOn : gasGlassOff));
    g.add(new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.22, 4).rotateY(Math.PI / 4).translate(0, 3.55, 0), iron));
    lampPos.push(new THREE.Vector3(x, y + 3.25, z));
    if (on) {
      const pl = new THREE.PointLight('#ffa24f', 95, 36, 2); pl.position.set(x, y + 3.25, z); scene.add(pl);
      const s1 = glowSprite('#ffc070', 7.0, 3.0); s1.position.set(x, y + 3.25, z); scene.add(s1);
      const s2 = glowSprite('#ff9448', 0.30, 9.0); s2.position.set(x, y + 3.0, z); scene.add(s2);
      glowAll.push(s1, s2);
    }
  });
  // cột điện: giữa các cặp đèn khí (1–2, 3–4, 5–6, 7–8, 9–10) và cạnh nhà kho; phía đối diện đèn khí gần nhất
  const ePosts = [];
  for (const sIdx of [0.5, 2.5, 4.5, 6.5, 8.5, 9.8]) {
    const s = 10 + sIdx * (Llen - 22) / 10, t = Math.min(s / Llen, 0.999), p = OSTLER.getPointAt(t), tg = OSTLER.getTangentAt(t);
    const nrm = new THREE.Vector3(-tg.z, 0, tg.x).normalize(); const side = 1;
    const x = p.x + nrm.x * 4.3 * side, z = p.z + nrm.z * 4.3 * side, y = groundY(x, z) + 0.12;
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = Math.atan2(-tg.z, tg.x); scene.add(g);
    g.add(new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.13, 7, 8).translate(0, 3.5, 0), iron));
    g.add(new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 1.1).translate(0, 6.9, -side * 0.5), iron));
    g.add(new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.12, 0.55).translate(0, 6.78, -side * 0.95), new THREE.MeshLambertMaterial({ color: '#b8b6c4', emissive: new THREE.Color('#8e8aa6'), emissiveIntensity: 0.18 }))); // tấm kính mờ, chưa bật
    ePosts.push(new THREE.Vector3(x, y + 6.9, z));
  }
  // dây điện võng giữa các cột
  { const pts = []; for (let i = 0; i < ePosts.length - 1; i++) { const a = ePosts[i], b = ePosts[i + 1]; for (let k = 0; k < 16; k++) { const u0 = k / 16, u1 = (k + 1) / 16;
      const P = (u) => new THREE.Vector3().lerpVectors(a, b, u).add(new THREE.Vector3(0, -1.2 * 4 * u * (1 - u), 0)); pts.push(P(u0), P(u1)); } }
    const g = new THREE.BufferGeometry().setFromPoints(pts); scene.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: '#1c1b22' }))); }

  // đèn khí ở các phố khác: điểm hổ phách rải rác (người thắp đèn khác), phần lớn chưa sáng
  for (const c of others) { const len = c.getLength(); for (let s = 12; s < len; s += 20) { if (R() > 0.45) continue; const t = s / len, p = c.getPointAt(t), tg = c.getTangentAt(t);
      const nrm = new THREE.Vector3(-tg.z, 0, tg.x).normalize(); const x = p.x + nrm.x * 3.6, z = p.z + nrm.z * 3.6; if (nearOstler(x, z, 10)) continue;
      const y = groundY(x, z) + 3.3; const sp = glowSprite('#ffae55', 3.2, 1.5); sp.position.set(x, y, z); scene.add(sp);
      const sp2 = glowSprite('#ff9040', 0.28, 10); sp2.position.set(x, y - 0.5, z); scene.add(sp2); } }

  // ---------- Ida (rất nhỏ) vừa thắp đèn số 4, đi tiếp với thang trên vai ----------
  const chIda = buildCharacter(ida, { detail: 12, material: (role, color) => role === 'flame' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#fff0c8').multiplyScalar(20) })
    : role === 'glass' ? new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffb85a').multiplyScalar(5) }) : new THREE.MeshLambertMaterial({ color }) });
  chIda.setPose(ida.poses.walk_ladder);
  { const s = lampS[JUST] + 2.2, t = s / Llen, p = OSTLER.getPointAt(t), tg = OSTLER.getTangentAt(t); const nrm = new THREE.Vector3(-tg.z, 0, tg.x).normalize();
    const x = p.x + nrm.x * 1.6, z = p.z + nrm.z * 1.6; chIda.root.position.set(x, groundY(x, z) + 0.03, z); chIda.root.rotation.y = Math.atan2(tg.x, tg.z); }
  chIda.root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  chIda.root.userData.imp = 1; scene.add(chIda.root);
  // đèn số 4 (vừa thắp): SpotLight có bóng chúc xuống → bóng Ida dài, mềm trên đá cuội (jitter theo mẫu)
  const L4 = lampPos[JUST];
  const spot = new THREE.SpotLight('#ffa24f', 95, 36, 1.3, 0.5, 2); spot.position.copy(L4); spot.castShadow = true;
  spot.shadow.mapSize.set(1024, 1024); spot.shadow.camera.near = 0.2; spot.shadow.camera.far = 30; spot.shadow.bias = -0.0005;
  const tgt = new THREE.Object3D(); tgt.position.set(L4.x, L4.y - 5, L4.z); scene.add(tgt); spot.target = tgt; scene.add(spot);
  // đèn số 4 dùng spot thay point light: bỏ point light tương ứng
  scene.children.filter((o) => o.isPointLight && o.position.distanceTo(L4) < 0.01).forEach((o) => scene.remove(o));

  if (dbg.nosprite) scene.traverse((o) => { if (o.isSprite) o.visible = false; });
  if (dbg.noshadow) spot.castShadow = false;
  if (dbg.nolights) scene.traverse((o) => { if (o.isPointLight) o.visible = false; });
  // ---------- máy quay ----------
  const cam = new THREE.PerspectiveCamera(46, 16 / 9, 1, 4000);
  cam.position.set(-14, 39, 34); cam.lookAt(10, 0, -71);   // chúc ≈ 20°, cao ~40 m trên phố

  const onSample = (i, n) => { if (n <= 1) return; const u = ((i * 0.618034) % 1) - 0.5, v = ((i * 0.754878) % 1) - 0.5; spot.position.set(L4.x + u * 0.25, L4.y + v * 0.2, L4.z); spot.updateMatrixWorld(); };
  return { scene, cam, onSample, chIda, lampPos };
}

// Cổng 3 đợt vá A2+ — bộ phố dùng chung (V1, V2, V3). Mọi kết cấu sinh bằng mã (canvas), chất vẽ tay của hướng C.
//  • cobbleTex: đá lát (setts granit) — luật thế giới: mặt phố Ostler và quảng trường là ĐÁ LÁT (kịch bản: "cobbles").
//  • groundPlane: mặt đất nằm ngang với UV đúng trục (lỗi V2: planarUV(X, Z) trên mặt phẳng đã xoay → v hằng số → texture thành sọc "ván gỗ").
//  • facadeTex: vữa vôi quét trên gạch, mảng vữa bong lộ gạch, gờ tầng, vệt nước dưới bậu, bẩn chân tường.
//  • windowUnit: ô cửa lõm tường, khung gỗ, song kính 6 ô, bậu đá nhô; kính phát sáng lạnh (đèn điện trong nhà) hoặc ấm.
//  • electricLamp: cột đèn điện thời kỳ (~1905–1915): chân gang có gờ, thân thép thẳng, tay treo, chụp men côn, bóng đèn trần.
//  • paintedSky: trời đêm vẽ theo bảng màu color script (không mảng xanh bão hoà phẳng).
import * as THREE from '../shared/node_modules/three/build/three.module.js';
import { canvasTex, blotches, rng } from '../dir-C/common.js';

const X = new THREE.Vector3(1, 0, 0), Y = new THREE.Vector3(0, 1, 0);

// ---------- đá lát ----------
// Setts ~0,10 × 0,14 m xếp hàng so le, mạch tối mềm, mặt đá vồng (sáng giữa), màu granit xám ấm/lạnh xen kẽ.
export function cobbleTex(seed = 11, { px = 2048, metres = 3 } = {}) {
  const R = rng(seed);
  return canvasTex(px, px, (g, w, h) => {
    const ppm = w / metres;
    g.fillStyle = 'rgb(46,42,40)'; g.fillRect(0, 0, w, h);
    const cols = [[118, 112, 106], [128, 121, 113], [106, 102, 100], [134, 126, 118], [112, 110, 114], [122, 114, 104]];
    const rowH = 0.105 * ppm;
    for (let r = 0, y = 0; y < h + rowH; r++, y += rowH) {
      let x = -(r % 2) * 0.07 * ppm - R() * 0.03 * ppm;
      while (x < w + 0.2 * ppm) {
        const sw = (0.11 + R() * 0.06) * ppm, sh = rowH * (0.86 + R() * 0.1), c = cols[Math.floor(R() * cols.length)], k = 0.86 + R() * 0.26;
        const cx = x + sw / 2 + (R() - 0.5) * 0.01 * ppm, cy = y + rowH / 2 + (R() - 0.5) * 0.01 * ppm;
        for (const [dx, dy] of [[0, 0], [w, 0], [-w, 0], [0, h], [0, -h]]) {
          const X0 = cx + dx, Y0 = cy + dy; if (X0 < -sw || X0 > w + sw || Y0 < -sh || Y0 > h + sh) continue;
          const gr = g.createRadialGradient(X0 - sw * 0.12, Y0 - sh * 0.18, sw * 0.05, X0, Y0, sw * 0.62);
          gr.addColorStop(0, `rgb(${c.map((v) => Math.min(255, v * k * 1.22) | 0)})`); gr.addColorStop(0.7, `rgb(${c.map((v) => v * k | 0)})`); gr.addColorStop(1, `rgb(${c.map((v) => v * k * 0.62 | 0)})`);
          g.fillStyle = gr; g.beginPath(); g.ellipse(X0, Y0, sw * 0.46, sh * 0.44, (R() - 0.5) * 0.12, 0, Math.PI * 2); g.fill();
        }
        x += sw;
      }
    }
    blotches(g, w, h, R, 70, [[40, 36, 34], [150, 142, 132], [96, 90, 84]], 0.15 * ppm, 0.7 * ppm, 0.04, 0.12);   // mảng ẩm/mòn
  });
}

// Mặt đất ngang (y = 0): PlaneGeometry nằm trong XY cục bộ rồi xoay −90° quanh x → UV phải lấy theo (X, Y) CỤC BỘ.
export function groundPlane(wx, wz, mat, metres, { cx = 0, cz = 0, y = 0 } = {}) {
  const geo = new THREE.PlaneGeometry(wx, wz), p = geo.attributes.position, uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) { uv[i * 2] = (p.getX(i) + cx) / metres; uv[i * 2 + 1] = (p.getY(i) - cz) / metres; }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  const m = new THREE.Mesh(geo, mat); m.rotation.x = -Math.PI / 2; m.position.set(cx, y, cz); m.receiveShadow = true; return m;
}

// ---------- mặt tiền ----------
// Vữa vôi trên gạch (vẽ theo mét): mảng loang, vữa bong lộ gạch đỏ nâu, gờ tầng (string course), vệt chảy, bẩn chân tường.
export function facadeTex(seed, { px = 1024, metres = 6, base = '#e7e2d6', brickShow = 0.16, courseAt = [3.1] } = {}) {
  const R = rng(seed);
  return canvasTex(px, px, (g, w, h) => {
    const ppm = w / metres;
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    blotches(g, w, h, R, 120, [[212, 204, 190], [244, 240, 230], [222, 214, 200], [196, 190, 182], [214, 210, 214]], 0.2 * ppm, 1.2 * ppm, 0.06, 0.2);
    // mảng vữa bong: lộ gạch (hàng 0,075 m), mép vữa xù
    const bh = 0.075 * ppm, bw = 0.23 * ppm;
    for (let k = 0; k < 3; k++) {   // A2+: ít và nhạt (7 mảng đỏ đọc thành 'tường lở')
      const px0 = R() * w, py0 = R() * h, rx = (0.2 + R() * 0.3) * ppm, ry = (0.12 + R() * 0.2) * ppm;
      g.save(); g.beginPath();
      for (let a = 0; a < Math.PI * 2; a += 0.35) { const rr = 0.7 + 0.5 * R(); g.lineTo(px0 + Math.cos(a) * rx * rr, py0 + Math.sin(a) * ry * rr); }
      g.closePath(); g.clip();
      g.globalAlpha = 0.45; g.fillStyle = 'rgb(160,128,112)'; g.fillRect(px0 - rx * 1.4, py0 - ry * 1.4, rx * 2.8, ry * 2.8);
      for (let y = Math.floor((py0 - ry * 1.4) / bh) * bh, r = 0; y < py0 + ry * 1.4; y += bh, r++) for (let x = px0 - rx * 1.4 - (r % 2) * bw / 2; x < px0 + rx * 1.4; x += bw) {
        const c = [158 + R() * 26, 124 + R() * 20, 108 + R() * 16]; g.fillStyle = `rgb(${c.map((v) => v | 0)})`; g.fillRect(x + 1.5, y + 1.5, bw - 3, bh - 3); }
      g.globalAlpha = 1; g.restore();
      g.strokeStyle = `rgba(120,108,96,${brickShow})`; g.lineWidth = 2; g.stroke();
    }
    // gờ tầng: dải vữa sáng có bóng dưới
    for (const cy of courseAt) { const y = h - cy * ppm; g.fillStyle = 'rgba(250,246,238,0.8)'; g.fillRect(0, y - 0.09 * ppm, w, 0.09 * ppm);
      const gr = g.createLinearGradient(0, y, 0, y + 0.12 * ppm); gr.addColorStop(0, 'rgba(90,80,72,0.35)'); gr.addColorStop(1, 'rgba(90,80,72,0)'); g.fillStyle = gr; g.fillRect(0, y, w, 0.12 * ppm); }
    // vệt nước chảy dọc
    for (let i = 0; i < 60; i++) { const x = R() * w, y0 = R() * h, len = (0.4 + R() * 1.6) * ppm, gr = g.createLinearGradient(0, y0, 0, y0 + len);
      gr.addColorStop(0, 'rgba(120,112,100,0)'); gr.addColorStop(0.25, `rgba(120,112,100,${(0.05 + R() * 0.08).toFixed(3)})`); gr.addColorStop(1, 'rgba(120,112,100,0)');
      g.fillStyle = gr; g.fillRect(x, y0, (0.02 + R() * 0.06) * ppm, len); }
    // chân tường: dải ẩm bẩn
    const gr = g.createLinearGradient(0, h, 0, h - 0.8 * ppm); gr.addColorStop(0, 'rgba(78,68,58,0.55)'); gr.addColorStop(0.4, 'rgba(100,90,78,0.22)'); gr.addColorStop(1, 'rgba(110,100,90,0)');
    g.fillStyle = gr; g.fillRect(0, h - 0.8 * ppm, w, 0.8 * ppm);
  });
}
// Gán UV theo mét cho mặt phẳng tường (XY cục bộ), texture phủ `metres` mét, gốc v = chân tường.
export function wallUV(geo, metres, x0 = 0) {
  const p = geo.attributes.position, uv = new Float32Array(p.count * 2); geo.computeBoundingBox(); const y0 = geo.boundingBox.min.y;
  for (let i = 0; i < p.count; i++) { uv[i * 2] = (p.getX(i) + x0) / metres; uv[i * 2 + 1] = (p.getY(i) - y0) / metres; }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); return geo;
}

// ---------- cửa sổ ----------
// Kính: gradient dọc vẽ (phản trời/trần nhà), rèm một bên, không phẳng một màu.
function glassTex(kind, seed) {
  const R = rng(seed);
  return canvasTex(64, 96, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h);
    if (kind === 'gold') { gr.addColorStop(0, '#ffcf8a'); gr.addColorStop(0.55, '#ffb35a'); gr.addColorStop(1, '#e8903e'); }
    else if (kind === 'cold') { gr.addColorStop(0, '#e6eef6'); gr.addColorStop(0.6, '#cdd8e3'); gr.addColorStop(1, '#b5c2cf'); }
    else { gr.addColorStop(0, '#5a5f70'); gr.addColorStop(1, '#2c2e38'); }
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    const side = R() < 0.5 ? 0 : w * 0.62, cw = w * (0.3 + R() * 0.12);   // rèm
    g.fillStyle = kind === 'gold' ? 'rgba(170,90,50,0.35)' : kind === 'cold' ? 'rgba(150,160,175,0.45)' : 'rgba(30,28,34,0.5)'; g.fillRect(side, 0, cw, h);
    for (let x = side; x < side + cw; x += 3) { g.fillStyle = `rgba(255,255,255,${(0.04 + R() * 0.05).toFixed(3)})`; g.fillRect(x, 0, 1, h); }
  }, { repeat: false });
}
// Ô cửa lõm 0,14 m vào tường (mặt tường ở z = 0 cục bộ, nhìn ra +z). kind: 'cold' | 'gold' | 'dark'. matFn(color, opts) → vật liệu cảnh.
export function windowUnit(w, h, kind, matFn, emissive, seed = 1) {
  // Tường là mặt phẳng z = 0 (cục bộ, nhìn ra +z): kính sát tường, viền đá/vữa và khung gỗ NHÔ ra (tạo bóng và chiều sâu).
  const g = new THREE.Group(), frameC = '#e9e4d8', frameD = '#5a4636', stone = '#b9b2a6';
  const box = (sx, sy, sz, m, x, y, z) => { const b = new THREE.Mesh(new THREE.BoxGeometry(sx, sy, sz), m); b.position.set(x, y, z); b.castShadow = true; b.receiveShadow = true; g.add(b); return b; };
  const surround = matFn('#cfc8bb'), frame = matFn(kind === 'gold' ? frameD : frameC), sill = matFn(stone);
  box(0.09, h + 0.12, 0.05, surround, -w / 2 - 0.045, 0, 0.025); box(0.09, h + 0.12, 0.05, surround, w / 2 + 0.045, 0, 0.025);   // viền đứng
  const gl = new THREE.Mesh(new THREE.PlaneGeometry(w, h), emissive(glassTex(kind, seed))); gl.position.z = 0.006; g.add(gl);
  const fz = 0.03, bar = 0.05, mul = 0.022;
  box(w, bar, 0.04, frame, 0, h / 2 - bar / 2, fz); box(w, bar, 0.04, frame, 0, -h / 2 + bar / 2, fz); box(bar, h, 0.04, frame, -w / 2 + bar / 2, 0, fz); box(bar, h, 0.04, frame, w / 2 - bar / 2, 0, fz);
  box(w, 0.055, 0.045, frame, 0, h * 0.05, fz + 0.005);                                                 // ray giữa (cửa kéo lên)
  for (const yy of [h * 0.28, -h * 0.22]) box(w, mul, 0.03, frame, 0, yy, fz);                            // song ngang
  for (const xx of [-w / 6, w / 6]) box(mul, h, 0.03, frame, xx, 0, fz);                                  // song dọc → 6 ô mỗi cánh
  box(w + 0.24, 0.07, 0.16, sill, 0, -h / 2 - 0.06, 0.08);                                               // bậu đá nhô
  box(w + 0.26, 0.13, 0.07, sill, 0, h / 2 + 0.1, 0.035);                                                // lanh tô đá
  return g;
}

// ---------- cột đèn điện ----------
// Thời kỳ ~1905–1915: bệ gang bát giác có gờ, thân thép thuôn THẲNG (đủ dày để lớp vẽ không làm cong), vòng cổ, tay treo có giằng cong,
// chụp men côn (xanh lục thẫm ngoài, trắng trong), bóng đèn trần phát sáng. Trả { group, head (Vector3 tâm bóng) }.
export function electricLamp(height, matFn, bulbMat) {
  const g = new THREE.Group(), iron = matFn('#2d3238'), iron2 = matFn('#3a4048'), enamelOut = matFn('#2f4a3c'), enamelIn = matFn('#e8ecef');
  const cyl = (r0, r1, hh, m, y, seg = 16) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r0, r1, hh, seg), m); c.position.y = y; c.castShadow = true; c.receiveShadow = true; g.add(c); return c; };
  cyl(0.20, 0.24, 0.12, iron, 0.06, 8); cyl(0.16, 0.20, 0.55, iron2, 0.39, 8); cyl(0.19, 0.16, 0.06, iron, 0.69, 8);            // bệ bát giác
  cyl(0.13, 0.15, 0.35, iron, 0.9, 16); cyl(0.15, 0.13, 0.05, iron2, 1.1, 16);
  cyl(0.085, 0.11, height - 1.2, iron, 1.1 + (height - 1.2) / 2, 16);                                                          // thân thẳng
  for (const yy of [2.2, height - 0.35]) cyl(0.12, 0.12, 0.06, iron2, yy, 16);                                                  // vòng cổ
  const armL = 0.85, arm = new THREE.Mesh(new THREE.BoxGeometry(armL, 0.06, 0.06), iron); arm.position.set(armL / 2 - 0.05, height - 0.1, 0); g.add(arm);
  const brace = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.02, 6, 16, Math.PI / 2), iron); brace.position.set(0.3, height - 0.42, 0); brace.rotation.z = 0; g.add(brace);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.2, 20, 1, true), enamelOut); shade.position.set(armL - 0.08, height - 0.28, 0); g.add(shade);
  const shadeIn = new THREE.Mesh(new THREE.ConeGeometry(0.275, 0.195, 20, 1, true), enamelIn); shadeIn.material.side = THREE.BackSide; shadeIn.position.copy(shade.position); g.add(shadeIn);
  cyl(0.03, 0.03, 0.12, iron, 0, 8).position.set(armL - 0.08, height - 0.15, 0);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), bulbMat); bulb.scale.set(1, 1.25, 1); bulb.position.set(armL - 0.08, height - 0.4, 0); g.add(bulb);
  const cap = new THREE.Mesh(new THREE.SphereGeometry(0.05, 10, 6), iron2); cap.position.set(0, height + 0.02, 0); g.add(cap);
  return { group: g, head: bulb.position.clone() };
}

// ---------- trời vẽ ----------
// stops: [[t, màu]] từ đỉnh (t=0) tới chân trời (t=1); thêm vệt mây phết mỏng và quầng sáng thành phố gần chân trời.
export function paintedSky(stops, { seed = 5, haze = '#b8c2d4', hazeA = 0.35 } = {}) {
  const R = rng(seed);
  const tex = canvasTex(1024, 512, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([t, c]) => gr.addColorStop(t, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 70; i++) {   // vệt mây ngang (phết cọ), sáng hơn nền một chút nhờ ánh phố hắt lên
      const y = h * (0.35 + R() * 0.55), x = R() * w, len = w * (0.08 + R() * 0.25), th = h * (0.006 + R() * 0.02);
      const a = 0.04 + R() * 0.08; g.fillStyle = `rgba(200,205,225,${a.toFixed(3)})`;
      g.beginPath(); g.ellipse(x, y, len / 2, th, (R() - 0.5) * 0.04, 0, Math.PI * 2); g.fill();
    }
    const hz = g.createLinearGradient(0, h * 0.62, 0, h); const c = new THREE.Color(haze);
    hz.addColorStop(0, `rgba(${c.r * 255 | 0},${c.g * 255 | 0},${c.b * 255 | 0},0)`); hz.addColorStop(1, `rgba(${c.r * 255 | 0},${c.g * 255 | 0},${c.b * 255 | 0},${hazeA})`);
    g.fillStyle = hz; g.fillRect(0, h * 0.62, w, h * 0.38);
  }, { repeat: false });
  tex.wrapS = THREE.RepeatWrapping;
  const m = new THREE.Mesh(new THREE.SphereGeometry(400, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2 + 0.15), new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide, fog: false, depthWrite: false }));
  return m;
}

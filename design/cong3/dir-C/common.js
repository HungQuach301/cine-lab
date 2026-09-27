// Hướng C — tiện ích dùng chung cho hai khung: kết cấu vẽ bằng canvas (sinh bằng mã), sprite quầng sáng, UV phẳng.
import * as THREE from '../shared/node_modules/three/build/three.module.js';

// Bộ sinh ngẫu nhiên có hạt giống (mulberry32) để mọi lần render ra cùng một hình.
export function rng(seed) { let a = seed >>> 0; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

export function canvasTex(w, h, draw, { srgb = true, repeat = true } = {}) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  const g = cv.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  if (repeat) t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.anisotropy = 4; t.needsUpdate = true;
  return t;
}

// Mảng mờ mềm (vết phết lớn): nhiều đốm gradient tròn/elip, alpha thấp.
export function blotches(g, w, h, R, n, colors, rmin, rmax, amin = 0.03, amax = 0.09, sy = 1) {
  for (let i = 0; i < n; i++) {
    const x = R() * w, y = R() * h, r = rmin + (rmax - rmin) * R();
    const c = colors[Math.floor(R() * colors.length)];
    g.save(); g.translate(x, y); g.scale(1, sy); g.rotate(R() * Math.PI);
    const gr = g.createRadialGradient(0, 0, 0, 0, 0, r);
    const a = amin + (amax - amin) * R();
    gr.addColorStop(0, `rgba(${c[0]},${c[1]},${c[2]},${a})`); gr.addColorStop(1, `rgba(${c[0]},${c[1]},${c[2]},0)`);
    g.fillStyle = gr; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill(); g.restore();
    // lặp mép để kết cấu lặp liền
    for (const [dx, dy] of [[w, 0], [-w, 0], [0, h], [0, -h]]) if (x + dx + r > 0 && x + dx - r < w && y + dy + r > 0 && y + dy - r < h) {
      g.save(); g.translate(x + dx, y + dy); g.scale(1, sy); const gg = g.createRadialGradient(0, 0, 0, 0, 0, r);
      gg.addColorStop(0, `rgba(${c[0]},${c[1]},${c[2]},${a})`); gg.addColorStop(1, `rgba(${c[0]},${c[1]},${c[2]},0)`);
      g.fillStyle = gg; g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill(); g.restore();
    }
  }
}

// Vôi quét trên gạch: nền kem, mảng loang, hàng gạch hiện rất mờ, vệt chảy dọc; tuỳ chọn dải bẩn chân tường.
export function limewashTex(seed, { px = 1024, metres = 4, grime = true, brick = 0.05, base = '#ece6da' } = {}) {
  const R = rng(seed);
  return canvasTex(px, px, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    const ppm = w / metres;
    blotches(g, w, h, R, 90, [[214, 204, 186], [246, 242, 232], [226, 216, 200], [200, 192, 180]], 0.25 * ppm, 1.1 * ppm, 0.05, 0.16);
    // hàng gạch 0,075 m, dài 0,23 m, lệch nửa viên
    const bh = 0.075 * ppm, bw = 0.23 * ppm;
    g.lineWidth = Math.max(1, 0.012 * ppm);
    for (let r = 0, y = 0; y < h; r++, y += bh) {
      const off = (r % 2) * bw / 2;
      for (let x = -off; x < w; x += bw) {
        const a = brick * (0.4 + R() * 0.9) * (0.6 + 0.4 * Math.sin(y / h * 7 + x / w * 3));
        g.strokeStyle = `rgba(120,104,90,${a.toFixed(3)})`; g.strokeRect(x, y, bw, bh);
        if (R() < 0.08) { g.fillStyle = `rgba(170,120,95,${(brick * 1.2).toFixed(3)})`; g.fillRect(x + 1, y + 1, bw - 2, bh - 2); }
      }
    }
    // vệt chảy dọc rất mờ
    for (let i = 0; i < 40; i++) { const x = R() * w, y0 = R() * h, len = (0.3 + R() * 1.2) * ppm; const gr = g.createLinearGradient(0, y0, 0, y0 + len);
      gr.addColorStop(0, 'rgba(150,140,125,0.0)'); gr.addColorStop(0.3, `rgba(150,140,125,${(0.03 + R() * 0.05).toFixed(3)})`); gr.addColorStop(1, 'rgba(150,140,125,0)');
      g.fillStyle = gr; g.fillRect(x, y0, (0.02 + R() * 0.05) * ppm, len); }
    if (grime) { // canvas y=0 ở trên; texture flipY → hàng cuối canvas là v=0 (chân tường)
      const gr = g.createLinearGradient(0, h, 0, h - 0.6 * ppm);
      gr.addColorStop(0, 'rgba(92,78,64,0.45)'); gr.addColorStop(0.35, 'rgba(110,96,80,0.18)'); gr.addColorStop(1, 'rgba(120,110,95,0)');
      g.fillStyle = gr; g.fillRect(0, h - 0.6 * ppm, w, 0.6 * ppm);
    }
  });
}

// Đá lát nền: hàng đá chữ nhật không đều, mạch vữa mềm, giữa viên mòn sáng.
export function flagTex(seed, { px = 1024, metres = 4, cols = [[124, 116, 106], [138, 128, 116], [112, 106, 100], [146, 136, 122]] } = {}) {
  const R = rng(seed);
  return canvasTex(px, px, (g, w, h) => {
    const ppm = w / metres;
    g.fillStyle = 'rgb(70,64,58)'; g.fillRect(0, 0, w, h);
    let y = 0;
    while (y < h) {
      const rh = (0.38 + R() * 0.22) * ppm; let x = -R() * 0.5 * ppm;
      while (x < w) {
        const sw = (0.45 + R() * 0.5) * ppm; const c = cols[Math.floor(R() * cols.length)]; const k = 0.9 + R() * 0.2;
        const gap = 0.018 * ppm;
        const gr = g.createRadialGradient(x + sw / 2, y + rh / 2, 0, x + sw / 2, y + rh / 2, sw * 0.7);
        gr.addColorStop(0, `rgb(${c.map((v) => Math.min(255, v * k * 1.08) | 0)})`); gr.addColorStop(1, `rgb(${c.map((v) => v * k * 0.9 | 0)})`);
        g.fillStyle = gr;
        g.beginPath(); const rr = 0.05 * ppm; g.roundRect ? g.roundRect(x + gap, y + gap, sw - 2 * gap, rh - 2 * gap, rr) : g.rect(x + gap, y + gap, sw - 2 * gap, rh - 2 * gap); g.fill();
        x += sw;
      }
      y += rh;
    }
    blotches(g, w, h, R, 50, [[60, 54, 48], [160, 150, 138]], 0.2 * ppm, 0.8 * ppm, 0.03, 0.08);
  });
}

// Sprite quầng sáng (cộng, HDR): hồ sơ tròn mềm hai lớp (lõi + quầng rộng).
let _glowTex = null;
export function glowTexture() {
  if (_glowTex) return _glowTex;
  _glowTex = canvasTex(256, 256, (g, w) => {
    const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
    for (let i = 0; i <= 16; i++) { const t = i / 16; const a = Math.exp(-t * t * 7.0) * 0.85 + Math.exp(-t * 2.8) * 0.15 * (1 - t); gr.addColorStop(t, `rgba(255,255,255,${a.toFixed(4)})`); }
    g.fillStyle = gr; g.fillRect(0, 0, w, w);
  }, { srgb: false, repeat: false });
  return _glowTex;
}
export function glowSprite(color, intensity, size, opts = {}) {
  const c = new THREE.Color(color).multiplyScalar(intensity);
  const m = new THREE.SpriteMaterial({ map: glowTexture(), color: c, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: opts.depthTest ?? true, transparent: true, fog: false });
  const s = new THREE.Sprite(m); s.scale.set(size, size, 1); s.renderOrder = 10; return s;
}

// Gán UV phẳng theo toạ độ thế giới (mét / tile).
export function planarUV(geo, uAxis, vAxis, tile, off = [0, 0]) {
  const p = geo.attributes.position, uv = new Float32Array(p.count * 2);
  const v3 = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) { v3.fromBufferAttribute(p, i); uv[2 * i] = (v3.dot(uAxis) + off[0]) / tile; uv[2 * i + 1] = (v3.dot(vAxis) + off[1]) / tile; }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  return geo;
}

// Máy quay có dịch ống kính dọc (lens shift): giữ đường đứng thẳng như tranh, không chúc/ngửa máy.
// shiftY tính theo NDC (0,25 = dịch khung lên 1/8 chiều cao). Bền với setViewOffset của pipeline (ghi đè sau mỗi update).
export class ShiftCam extends THREE.PerspectiveCamera {
  constructor(fov, aspect, near, far, shiftY = 0) { super(fov, aspect, near, far); this.shiftY = shiftY; this.updateProjectionMatrix(); }
  updateProjectionMatrix() { super.updateProjectionMatrix(); if (this.shiftY) { this.projectionMatrix.elements[9] += this.shiftY; this.projectionMatrixInverse.copy(this.projectionMatrix).invert(); } }
}

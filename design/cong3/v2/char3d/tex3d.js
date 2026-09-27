// Cine Lab · Cổng 3 v2 · cách (1) — kết cấu nhân vật sinh bằng mã (canvas), hợp chất tranh sơn hướng C.
// map: nền gần trắng (nhân với màu gốc model sheet → giữ quan hệ sáng–tối), mảng loang + nét cọ ngắn lệch sắc nóng/lạnh.
// normalMap: suy từ bản đồ độ cao vẽ kèm (Sobel) — sợi dạ, mắt len đan, sợi tóc, da thuộc. Chỉ bắt sáng, không bóng nhựa.
import * as THREE from '../../shared/node_modules/three/build/three.module.js';

function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const cache = new Map();
function canvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function toTex(cv, srgb) {
  const t = new THREE.CanvasTexture(cv); t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4; t.needsUpdate = true; return t;
}
// Vẽ lặp mép (kết cấu liền khi lặp).
function wrapDraw(w, h, x, y, r, f) { for (const dx of [-w, 0, w]) for (const dy of [-h, 0, h]) if (x + dx + r > 0 && x + dx - r < w && y + dy + r > 0 && y + dy - r < h) f(x + dx, y + dy); }

// Nét cọ: elip dài, mép mềm, alpha thấp.
function strokes(g, w, h, R, n, len, wid, cols, a0, a1, ang, angJ) {
  for (let i = 0; i < n; i++) {
    const x = R() * w, y = R() * h, L = len * (0.6 + 0.8 * R()), W = wid * (0.6 + 0.8 * R()), c = cols[(R() * cols.length) | 0], a = a0 + (a1 - a0) * R();
    const th = ang + (R() - 0.5) * angJ;
    wrapDraw(w, h, x, y, L, (xx, yy) => {
      g.save(); g.translate(xx, yy); g.rotate(th); g.scale(1, W / L);
      const gr = g.createRadialGradient(0, 0, 0, 0, 0, L); gr.addColorStop(0, `rgba(${c},${a})`); gr.addColorStop(0.6, `rgba(${c},${a * 0.6})`); gr.addColorStop(1, `rgba(${c},0)`);
      g.fillStyle = gr; g.beginPath(); g.arc(0, 0, L, 0, Math.PI * 2); g.fill(); g.restore();
    });
  }
}

// ---- map màu ----
export function paintMap(kind, seed = 1) {
  const key = 'map|' + kind + '|' + seed; if (cache.has(key)) return cache.get(key);
  const S = 512, cv = canvas(S, S), g = cv.getContext('2d'), R = rng(seed * 97 + kind.length);
  const base = { skin: '#f4f0ec', cloth: '#f2f2f0', felt: '#f0efee', knit: '#f4f2ef', hair: '#f2f2f2', leather: '#efefef', lining: '#f0eeec' }[kind] || '#f0f0f0';
  g.fillStyle = base; g.fillRect(0, 0, S, S);
  if (kind === 'skin') {
    // mảng ấm (máu dưới da) và lạnh (xanh tím ở hốc) — pha màu kiểu tranh, không phải lỗ chân lông
    strokes(g, S, S, R, 60, 70, 50, ['255,214,196', '250,226,206', '222,222,240', '255,240,220'], 0.10, 0.25, 0, Math.PI);
    strokes(g, S, S, R, 160, 22, 9, ['255,236,222', '236,214,210', '250,246,236'], 0.08, 0.2, 0.3, 1.2);
  } else if (kind === 'hair') {
    strokes(g, S, S, R, 500, 60, 3, ['255,255,255', '200,200,205', '230,226,220', '170,170,176'], 0.15, 0.4, Math.PI / 2, 0.15);
  } else if (kind === 'knit') {
    strokes(g, S, S, R, 80, 60, 40, ['255,250,240', '226,226,232', '240,236,226'], 0.12, 0.25, 0, Math.PI);
    strokes(g, S, S, R, 220, 26, 7, ['255,255,255', '214,212,220'], 0.08, 0.18, Math.PI / 2, 0.5);
  } else {
    // vải, dạ, da thuộc: loang rộng + nét cọ ngắn theo thớ
    strokes(g, S, S, R, 70, 90, 60, ['255,250,240', '220,224,236', '236,232,224', '250,244,232'], 0.10, 0.24, 0, Math.PI);
    strokes(g, S, S, R, 260, 30, 8, ['255,255,252', '214,216,224', '236,230,220'], 0.06, 0.18, Math.PI / 2, kind === 'felt' ? 3 : 0.7);
  }
  const t = toTex(cv, true); cache.set(key, t); return t;
}

// ---- normal map từ độ cao ----
function heightToNormal(hc, strength) {
  const w = hc.width, h = hc.height, src = hc.getContext('2d').getImageData(0, 0, w, h).data;
  const H = new Float32Array(w * h); for (let i = 0; i < w * h; i++) H[i] = src[i * 4] / 255;
  const out = canvas(w, h), og = out.getContext('2d'), img = og.createImageData(w, h), d = img.data;
  const at = (x, y) => H[((y + h) % h) * w + ((x + w) % w)];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = (at(x + 1, y - 1) + 2 * at(x + 1, y) + at(x + 1, y + 1) - at(x - 1, y - 1) - 2 * at(x - 1, y) - at(x - 1, y + 1)) * strength;
    const dy = (at(x - 1, y + 1) + 2 * at(x, y + 1) + at(x + 1, y + 1) - at(x - 1, y - 1) - 2 * at(x, y - 1) - at(x + 1, y - 1)) * strength;
    const l = Math.hypot(dx, dy, 1), i = (y * w + x) * 4;
    d[i] = (-dx / l * 0.5 + 0.5) * 255; d[i + 1] = (dy / l * 0.5 + 0.5) * 255; d[i + 2] = (1 / l * 0.5 + 0.5) * 255; d[i + 3] = 255;
  }
  og.putImageData(img, 0, 0); return toTex(out, false);
}
export function normalMap(kind, seed = 1) {
  const key = 'nrm|' + kind + '|' + seed; if (cache.has(key)) return cache.get(key);
  const S = 256, hc = canvas(S, S), g = hc.getContext('2d'), R = rng(seed * 131 + kind.length * 7);
  g.fillStyle = '#808080'; g.fillRect(0, 0, S, S);
  let str = 2.0;
  if (kind === 'knit') {
    // mắt len đan dọc: cột chữ V (stockinette), 16 cột × 22 hàng mỗi ô lặp
    const cols = 16, rows = 22, cw = S / cols, rh = S / rows;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) for (const side of [-1, 1]) {
      const x = c * cw + cw / 2 + side * cw * 0.22, y = r * rh + rh / 2;
      g.save(); g.translate(x, y); g.rotate(side * 0.55); g.scale(1, 2.1);
      const gr = g.createRadialGradient(0, 0, 0, 0, 0, cw * 0.3); gr.addColorStop(0, '#e8e8e8'); gr.addColorStop(1, 'rgba(60,60,60,0.0)');
      g.fillStyle = gr; g.beginPath(); g.arc(0, 0, cw * 0.3, 0, Math.PI * 2); g.fill(); g.restore();
    }
    for (let c = 0; c <= cols; c++) { g.fillStyle = 'rgba(40,40,40,0.5)'; g.fillRect(c * cw - 1, 0, 2, S); }
    str = 2.6;
  } else if (kind === 'rib') {
    const cols = 24, cw = S / cols; for (let c = 0; c < cols; c++) { const gr = g.createLinearGradient(c * cw, 0, c * cw + cw, 0); gr.addColorStop(0, '#303030'); gr.addColorStop(0.5, '#e0e0e0'); gr.addColorStop(1, '#303030'); g.fillStyle = gr; g.fillRect(c * cw, 0, cw, S); }
    str = 2.2;
  } else if (kind === 'hair') {
    for (let i = 0; i < 700; i++) { const x = R() * S, v = (R() * 180 + 40) | 0; g.strokeStyle = `rgba(${v},${v},${v},0.5)`; g.lineWidth = 1 + R() * 2; g.beginPath(); g.moveTo(x, -10); g.bezierCurveTo(x + (R() - 0.5) * 8, S * 0.3, x + (R() - 0.5) * 8, S * 0.7, x + (R() - 0.5) * 6, S + 10); g.stroke(); }
    str = 2.4;
  } else if (kind === 'felt' || kind === 'cloth') {
    // twill chéo mảnh (dạ áo khoác) + gợn lông
    if (kind === 'cloth') for (let i = -S; i < S * 2; i += 5) { g.strokeStyle = 'rgba(200,200,200,0.35)'; g.lineWidth = 2; g.beginPath(); g.moveTo(i, 0); g.lineTo(i + S * 0.6, S); g.stroke(); }
    for (let i = 0; i < 1400; i++) { const x = R() * S, y = R() * S, v = (R() * 255) | 0; g.fillStyle = `rgba(${v},${v},${v},0.18)`; g.beginPath(); g.arc(x, y, 1 + R() * 3, 0, Math.PI * 2); g.fill(); }
    str = kind === 'felt' ? 1.2 : 1.5;
  } else if (kind === 'leather') {
    for (let i = 0; i < 300; i++) { const x = R() * S, y = R() * S, v = (R() * 120 + 60) | 0; g.strokeStyle = `rgba(${v},${v},${v},0.4)`; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (R() - 0.5) * 30, y + (R() - 0.5) * 8); g.stroke(); }
    str = 1.4;
  } else if (kind === 'skin') {
    for (let i = 0; i < 2500; i++) { const x = R() * S, y = R() * S, v = (R() * 80 + 100) | 0; g.fillStyle = `rgba(${v},${v},${v},0.25)`; g.beginPath(); g.arc(x, y, 0.8 + R() * 1.6, 0, Math.PI * 2); g.fill(); }
    str = 0.8;
  }
  const t = heightToNormal(hc, str); cache.set(key, t); return t;
}

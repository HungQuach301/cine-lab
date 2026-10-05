// Last Lamplighters · thư viện mẫu (Mốc B) — lõi: giấy B3, ánh rọi, bụi, chữ, thẻ, biểu tượng, bóng người, vẽ khung.
// Tách và tổng quát hoá từ mã tập 1 (design/m3/ep01/history/lib.js, today/lib.js, shorts/common.js — bản vá trong reports/m3/m2-2b/ma, m2-3).
// Ngôn ngữ hình B3 giữ nguyên (giấy ngà có vân + mép răng cưa, bóng theo ánh rọi, ánh rọi ấm lướt chậm, giấy lay nhẹ, bụi).
// Mới so với tập 1:
//   - LL.fmt ('16x9' | '9x16'): cùng mẫu chạy cho bản dài và Shorts; tấm giấy và cỡ chữ tối thiểu theo khổ.
//   - Chữ tối thiểu Ở MỌI TRẠNG THÁI: text() đọc ma trận biến đổi hiện hành; nếu cỡ hiệu dụng < MINPX thì nâng cỡ (và đếm vào LL.stat.raised).
//     MINPX: 16:9 → 26 px (chữ hoa DejaVu ≈ 0,73 em ≈ 19 px ≥ 18); 9:16 → 42 px (chữ hoa ≈ 30,7 px ≥ 30).
//   - Nhật ký chữ (LL.tlog) ở khung mẫu: hộp chữ trên màn hình, màu, alpha → render.js đo tương phản thật trên điểm ảnh.
//   - rv(t, a, d): tiến độ "nội dung hiện ra" — đánh dấu LL.act khi 0 < u < 1 (qc dùng để bắt chữ đứng > 3 s khi đang có lời).
//   - LL.cam(near): mẫu cảnh 2.5D báo khoảng cách máy tới lớp gần nhất (qc bắt máy xuyên hình học khi near ≤ 0).
'use strict';
const FPS = 24;
const LL = window.LL = window.LL || {};
LL.fmt = LL.fmt || '16x9';
const W = LL.fmt === '9x16' ? 1080 : 1920, H = LL.fmt === '9x16' ? 1920 : 1080;
const MINPX = LL.fmt === '9x16' ? 42 : 26;
const cv = document.getElementById('c'); cv.width = W; cv.height = H; const X = cv.getContext('2d');
const INK = '#211a17', INK2 = '#382d25', CREAM = '#ecdfbe', AMBER = '#c47026', AMBER_L = '#d99a52', COLD = '#3f5a7a', NAVY = '#141a2e',
  COLDW = '#eef3ff', OCHRE = '#6b3a12', SEPIA = '#5b4330', BROWN = '#4f2a0c', RED_D = '#6e1f14';
const RGB_AMB = '255,178,90', RGB_WHT = '225,236,255';
const SANS = '"DejaVu Sans"', SERIFB = '"DejaVu Serif"';
const font = (px, kind = 'sans', bold = true) => `${bold ? 'bold ' : ''}${Math.round(px)}px ${kind === 'serif' ? SERIFB : SANS}`;
const M = '−';
// tấm giấy chuẩn theo khổ
const CARD = LL.fmt === '9x16' ? { x: 40, y: 230, w: 1000, h: 1300 } : { x: 150, y: 90, w: 1620, h: 900 };
// vùng an toàn chữ (toạ độ khung)
const SAFE = LL.fmt === '9x16' ? { x0: 60, x1: 1020, y0: 260, y1: 1500 } : { x0: 96, x1: 1824, y0: 54, y1: 1026 };

// ---------- thời gian ----------
const cl = (u) => Math.max(0, Math.min(1, u));
const sm = (u) => { u = cl(u); return u * u * u * (u * (u * 6 - 15) + 10); };
const eo = (u) => { u = cl(u); return 1 - Math.pow(1 - u, 3); };
const ei = (u) => { u = cl(u); return u * u * u; };
const pr = (t, a, b) => cl((t - a) / (b - a));
const lerp = (a, b, u) => a + (b - a) * u;
LL.act = false; LL.fill = false;
// rv: nội dung (dữ liệu, chữ gắn lời) hiện ra → đánh dấu LL.act khi đang chuyển, LL.fill khi đã thấy (khung không còn "trống")
const rv = (t, a, d = 0.6) => { const u = cl((t - a) / d); if (u > 0 && u < 1) LL.act = true; if (u > 0) LL.fill = true; return u; };
// rvH: khung sườn (tựa, trục, nguồn, biểu tượng) — không tính là nội dung
const rvH = (t, a, d = 0.6) => cl((t - a) / d);
function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
function mixC(a, b, u) { const p = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); return `rgb(${A.map((x, i) => Math.round(lerp(x, B[i], cl(u)))).join(',')})`; }
const fmtN = (v, d = 0) => (v < 0 ? M : '') + Math.abs(Number(v)).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
const fmtP = (v, d = 1) => (v < 0 ? M : v > 0 ? '+' : '') + Math.abs(v).toFixed(d) + '%';

// ---------- giấy ----------
function paperTex(w, h, seed) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); const R = rng(seed);
  g.fillStyle = CREAM; g.fillRect(0, 0, w, h);
  const id = g.getImageData(0, 0, w, h), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const n = (R() - 0.5) * 9; d[i] += n; d[i + 1] += n; d[i + 2] += n * 0.8; }
  g.putImageData(id, 0, 0);
  const nf = Math.round(1400 * w * h / (1620 * 900));
  for (let i = 0; i < nf; i++) { const x = R() * w, y = R() * h, L = 6 + R() * 26, a = R() * Math.PI;
    g.strokeStyle = `rgba(${R() < 0.5 ? '120,95,60' : '255,250,235'},${0.05 + R() * 0.07})`; g.lineWidth = 0.6 + R() * 0.8;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * L * 0.5 + (R() - 0.5) * 4, y + Math.sin(a) * L * 0.5 + (R() - 0.5) * 4, x + Math.cos(a) * L, y + Math.sin(a) * L); g.stroke(); }
  for (let i = 0; i < 26; i++) { const x = R() * w, y = R() * h, r = 40 + R() * 160, gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, `rgba(150,110,60,${0.025 + R() * 0.03})`); gr.addColorStop(1, 'rgba(150,110,60,0)'); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  for (const [x1, y1] of [[0, h], [w, 0]]) { const e = g.createLinearGradient(0, 0, x1, y1); e.addColorStop(0, 'rgba(90,60,30,0.10)'); e.addColorStop(0.05, 'rgba(90,60,30,0)');
    e.addColorStop(0.95, 'rgba(90,60,30,0)'); e.addColorStop(1, 'rgba(90,60,30,0.11)'); g.fillStyle = e; g.fillRect(0, 0, w, h); }
  return c;
}
function edgePath(w, h, seed) { const R = rng(seed), p = [], st = 18;
  for (let x = 0; x <= w; x += st) p.push([x, (R() - 0.5) * 2.2]);
  for (let y = 0; y <= h; y += st) p.push([w + (R() - 0.5) * 2.2, y]);
  for (let x = w; x >= 0; x -= st) p.push([x, h + (R() - 0.5) * 2.2]);
  for (let y = h; y >= 0; y -= st) p.push([(R() - 0.5) * 2.2, y]); return p; }
const TEX = {};
function paper(w, h, seed) { const k = `${w}x${h}:${seed}`; return TEX[k] || (TEX[k] = { tex: paperTex(w, h, seed), edge: edgePath(w, h, seed + 3) }); }
const BG = (() => { const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d'); const R = rng(77);
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#171b2b'); gr.addColorStop(1, '#0d0f19'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  for (let i = 0; i < W * H / 415; i++) { g.fillStyle = `rgba(${R() < 0.5 ? '0,0,0' : '120,110,140'},${0.04 + R() * 0.05})`; g.fillRect(R() * W, R() * H, 1 + R() * 2, 1 + R() * 2); }
  return c; })();
function hatch(color, bg, lw = 3.2) { const c = document.createElement('canvas'); c.width = c.height = 14; const g = c.getContext('2d');
  g.fillStyle = bg; g.fillRect(0, 0, 14, 14); g.strokeStyle = color; g.lineWidth = lw;
  for (const o of [-14, 0, 14]) { g.beginPath(); g.moveTo(o, 14); g.lineTo(o + 14, 0); g.stroke(); } return X.createPattern(c, 'repeat'); }
const HATCH_COLD = hatch(COLD, 'rgba(63,90,122,0.18)');

// ---------- chữ (cỡ tối thiểu theo trạng thái, nhật ký) ----------
LL.stat = { raised: 0, rmax: 0 };
LL.tlog = null;   // render.js đặt [] ở khung mẫu
const effScale = (g) => { const m = g.getTransform(); return Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)); };
// px: cỡ mong muốn (px trong hệ toạ độ hiện hành). Trả cỡ thực dùng.
function fitPx(g, px) { const s = effScale(g) || 1; if (px * s >= MINPX - 0.01) return px; LL.stat.raised++; LL.stat.rmax = Math.max(LL.stat.rmax, MINPX / s - px); return MINPX / s; }
function text(g, s, x, y, px, color, o = {}) {
  s = String(s); if (!s) return 0; const a = o.a === undefined ? 1 : o.a; if (a <= 0.01) return 0;
  const p = o.raw ? px : fitPx(g, px); const f = font(p, o.kind || 'sans', o.bold !== false);
  g.save(); g.globalAlpha *= cl(a); g.font = f; g.fillStyle = color; g.textAlign = o.align || 'left'; g.textBaseline = o.base || 'alphabetic';
  if (o.italic) g.font = 'italic ' + f;
  g.fillText(s, x, y); const w = g.measureText(s).width;
  if (LL.tlog && g.globalAlpha > 0.5 && !o.deco) { const m = g.getTransform(), al = g.textAlign, bl = g.textBaseline;
    const x0 = al === 'center' ? x - w / 2 : al === 'right' ? x - w : x, cap = p * 0.73, yb = bl === 'middle' ? y + cap / 2 : bl === 'top' ? y + cap : y;
    const P = [[x0, yb - cap], [x0 + w, yb - cap], [x0, yb], [x0 + w, yb]].map(([u, v]) => [m.a * u + m.c * v + m.e, m.b * u + m.d * v + m.f]);
    LL.tlog.push({ s: s.slice(0, 40), color, alpha: +g.globalAlpha.toFixed(2), cap: +(cap * effScale(g)).toFixed(1),
      box: [Math.min(...P.map((q) => q[0])), Math.min(...P.map((q) => q[1])), Math.max(...P.map((q) => q[0])), Math.max(...P.map((q) => q[1]))].map(Math.round) }); }
  g.restore(); return w; }
function measure(g, s, px, kind = 'sans') { g.save(); g.font = font(fitPx(g, px), kind); const w = g.measureText(String(s)).width; g.restore(); return w; }
// chữ hiện bằng "mực thấm" trái → phải
function textWipe(g, s, x, y, px, color, u, o = {}) { if (u <= 0) return; const w = measure(g, s, px, o.kind), al = o.align || 'left';
  const x0 = al === 'center' ? x - w / 2 : al === 'right' ? x - w : x; g.save(); g.beginPath(); g.rect(x0 - 6, y - px * 2, (w + 30) * sm(u), px * 3); g.clip();
  text(g, s, x, y, px, color, Object.assign({}, o, { a: (o.a === undefined ? 1 : o.a) * cl(u * 3) })); g.restore(); }
function wrap(g, s, maxW, px, kind = 'sans') { g.save(); g.font = font(fitPx(g, px), kind); const out = []; let a = '';
  for (const w of String(s).split(' ')) { const n = a ? a + ' ' + w : w; if (g.measureText(n).width > maxW && a) { out.push(a); a = w; } else a = n; } out.push(a); g.restore(); return out; }
// đoạn nhiều dòng; trả y dòng cuối
function para(g, s, x, y, maxW, px, color, o = {}) { const L = wrap(g, s, maxW, px, o.kind), lh = o.lh || px * 1.3;
  L.forEach((l, i) => { const ui = o.u === undefined ? 1 : cl(o.u * L.length - i); if (o.wipe) textWipe(g, l, x, y + i * lh, px, color, ui, o); else text(g, l, x, y + i * lh, px, color, Object.assign({}, o, { a: (o.a === undefined ? 1 : o.a) * ui })); });
  return y + (L.length - 1) * lh; }
// thẻ chữ có nền
function tag(g, s, x, y, px, fill, color, o = {}) { const a = o.a === undefined ? 1 : o.a; if (a <= 0.01) return 0; const p = fitPx(g, px);
  g.save(); g.globalAlpha *= cl(a); g.font = font(p); const w = g.measureText(s).width + p * 0.9, h = p * 1.55, al = o.align || 'left', x0 = al === 'right' ? x - w : al === 'center' ? x - w / 2 : x;
  if (fill) { g.fillStyle = fill; g.fillRect(x0, y - h / 2, w, h); }
  if (o.dash) { g.setLineDash([9, 6]); g.strokeStyle = color; g.lineWidth = 2.4; g.strokeRect(x0 + 3, y - h / 2 + 3, w - 6, h - 6); g.setLineDash([]); }
  else if (o.border) { g.strokeStyle = color; g.lineWidth = 2.4; g.strokeRect(x0, y - h / 2, w, h); }
  text(g, s, x0 + p * 0.45, y + 1, p, color, { base: 'middle', raw: true }); g.restore(); return w; }
// nhãn loại số liệu: ACTUAL nét liền viền mực; PROJECTION nét đứt nền xanh lạnh
function kindTag(g, kind, x, y, px, a = 1, align = 'left', label) {
  if (kind === 'projection') return tag(g, label || 'PROJECTION', x, y, px, 'rgba(243,236,218,0.95)', '#16253a', { a, dash: true, align });
  return tag(g, label || 'ACTUAL', x, y, px, null, INK, { a, border: true, align }); }
// dòng nguồn (cỡ tối thiểu tự nâng)
function srcLine(g, s, x, y, a = 1, px) { text(g, s, x, y, px || MINPX, INK2, { a, bold: true }); }

// ---------- ánh rọi, lay, bụi ----------
LL.light = (t) => LL.fmt === '9x16' ? [540 + 230 * Math.sin(2 * Math.PI * t / 23 + 0.6), 880 + 260 * Math.sin(2 * Math.PI * t / 31)]
  : [960 + 360 * Math.sin(2 * Math.PI * t / 23 + 0.6), 470 + 110 * Math.sin(2 * Math.PI * t / 31)];
const DUST = (() => { const R = rng(4242); return Array.from({ length: 46 }, () => [R(), R(), R(), R(), R()]); })();
// tấm giấy: o = { x, y, w, h, seed, alpha, rot (biên độ lay), content(g, t, w, h), flipU, ph, scale, tilt, dx, dy }
function drawCard(g, t, o) {
  const [lx, ly] = LL.light(t), w = o.w || CARD.w, h = o.h || CARD.h, x = (o.x === undefined ? CARD.x : o.x) + (o.dx || 0), y = (o.y === undefined ? CARD.y : o.y) + (o.dy || 0);
  const ra = o.rot === undefined ? 1 : o.rot, ph = o.ph || 0, P = paper(w, h, o.seed || 11);
  const rot = ra * (0.0021 * Math.sin(2 * Math.PI * t / 7.3 + ph) + 0.0012 * Math.sin(2 * Math.PI * t / 4.1 + 1 + ph)) + (o.tilt || 0);
  const dx = ra * 1.6 * Math.sin(2 * Math.PI * t / 5.1 + 0.3 + ph), dy = ra * 1.1 * Math.sin(2 * Math.PI * t / 6.7 + 2 + ph);
  g.save(); g.globalAlpha *= o.alpha === undefined ? 1 : cl(o.alpha);
  g.translate(x + dx + w / 2, y + dy + h / 2); g.rotate(rot); if (o.scale) g.scale(o.scale, o.scale); g.translate(-w / 2, -h / 2);
  if (o.flipU !== undefined) { g.translate(w / 2, 0); g.scale(Math.max(0.001, o.flipU), 1); g.translate(-w / 2, 0); }
  const e = P.edge, path = () => { g.beginPath(); e.forEach(([px, py], i) => (i ? g.lineTo(px, py) : g.moveTo(px, py))); g.closePath(); };
  g.save(); g.shadowColor = 'rgba(0,0,0,0.62)'; g.shadowBlur = 38; g.shadowOffsetX = (x + w / 2 - lx) * 0.03 + 10; g.shadowOffsetY = (y + h / 2 - ly) * 0.03 + 16;
  path(); g.fillStyle = CREAM; g.fill(); g.restore();
  g.save(); path(); g.clip(); g.drawImage(P.tex, 0, 0);
  if (o.content) o.content(g, t, w, h);
  if (o.flipU !== undefined) { g.fillStyle = `rgba(30,20,10,${0.45 * (1 - o.flipU)})`; g.fillRect(0, 0, w, h); }
  g.restore(); g.restore();
}
function drawLight(g, t, a = 1) {
  const [lx, ly] = LL.light(t), R = Math.max(W, H);
  g.save(); g.globalCompositeOperation = 'multiply'; const v = g.createRadialGradient(lx, ly, R * 0.135, lx, ly, R * 0.65);
  v.addColorStop(0, '#fff'); v.addColorStop(1, `rgb(${Math.round(255 - 100 * a)},${Math.round(255 - 105 * a)},${Math.round(255 - 92 * a)})`); g.fillStyle = v; g.fillRect(0, 0, W, H);
  g.globalCompositeOperation = 'lighter'; const s = g.createRadialGradient(lx, ly, 0, lx, ly, R * 0.36);
  s.addColorStop(0, `rgba(60,38,12,${0.55 * a})`); s.addColorStop(1, 'rgba(60,38,12,0)'); g.fillStyle = s; g.fillRect(0, 0, W, H); g.restore(); }
function drawDust(g, t, a = 1) { if (a <= 0) return; const [lx, ly] = LL.light(t); g.save(); g.globalCompositeOperation = 'lighter';
  for (const [r1, r2, r3, r4, r5] of DUST) { const x = lx - 700 + 1400 * ((r1 + 0.012 * (0.5 + r4) * t) % 1), y = ly - 420 + 840 * ((r2 + 0.006 * (0.4 + r5) * t + 0.02 * Math.sin(t * (0.3 + r3) + r1 * 9)) % 1);
    const d = Math.hypot(x - lx, y - ly) / 700, al = a * (0.10 + 0.16 * r3) * Math.max(0, 1 - d * d), rad = 1.2 + 2.4 * r4;
    if (al <= 0.004) continue; const gr = g.createRadialGradient(x, y, 0, x, y, rad * 2); gr.addColorStop(0, `rgba(255,214,160,${al})`); gr.addColorStop(1, 'rgba(255,214,160,0)'); g.fillStyle = gr; g.fillRect(x - rad * 2, y - rad * 2, rad * 4, rad * 4); }
  g.restore(); }
function glow(g, x, y, r, rgb, a) { if (a <= 0.003) return; g.save(); g.globalCompositeOperation = 'lighter'; const gr = g.createRadialGradient(x, y, 0, x, y, r);
  gr.addColorStop(0, `rgba(${rgb},${a})`); gr.addColorStop(0.35, `rgba(${rgb},${a * 0.38})`); gr.addColorStop(1, `rgba(${rgb},0)`); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); g.restore(); }
// nền bàn tối + ánh rọi + bụi quanh một tấm giấy (dùng cho mọi mẫu dữ liệu)
function desk(g, t, cards, o = {}) { g.drawImage(BG, 0, 0); for (const c of cards) drawCard(g, t, c); drawLight(g, t, o.light === undefined ? 1 : o.light); drawDust(g, t, o.dust === undefined ? 1 : o.dust); }

// ---------- biểu tượng ----------
function gasLampIcon(g, x, y, s, a, lit = 1, col = OCHRE) { if (a <= 0) return; g.save(); g.globalAlpha *= cl(a); g.translate(x, y); g.scale(s, s);
  g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 3.4; g.lineJoin = 'round';
  g.fillRect(-4, 40, 8, 104); g.fillRect(-14, 136, 28, 8);
  g.beginPath(); g.moveTo(-20, 32); g.lineTo(20, 32); g.stroke();
  g.beginPath(); g.moveTo(-15, 30); g.lineTo(-22, -4); g.lineTo(22, -4); g.lineTo(15, 30); g.closePath(); g.stroke();
  g.beginPath(); g.moveTo(-26, -4); g.lineTo(0, -22); g.lineTo(26, -4); g.closePath(); g.fill(); g.fillRect(-3, -30, 6, 9);
  if (lit > 0) { g.fillStyle = `rgba(232,150,60,${0.85 * lit})`; g.beginPath(); g.moveTo(0, 22); g.quadraticCurveTo(-8, 12, 0, 1); g.quadraticCurveTo(8, 12, 0, 22); g.fill(); }
  g.restore(); }
// biểu tượng nghề (đơn giản, nét mực) — tên: lamp, lift, headset, phone, chat, typewriter, desk, person
const ICONS = {
  lamp: (g, s, a, col) => gasLampIcon(g, 0, -70 * s, s * 0.9, a, 1, col),
  headset: (g, s, a, col) => { g.save(); g.scale(s, s); g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 7; g.beginPath(); g.arc(0, 0, 44, Math.PI * 1.05, Math.PI * 1.95); g.stroke();
    g.fillRect(-52, -8, 18, 38); g.fillRect(34, -8, 18, 38); g.lineWidth = 5; g.beginPath(); g.moveTo(-43, 30); g.quadraticCurveTo(-40, 56, -6, 58); g.stroke(); g.beginPath(); g.arc(-4, 58, 6, 0, 7); g.fill(); g.restore(); },
  phone: (g, s, a, col) => { g.save(); g.scale(s, s); g.fillStyle = col; g.strokeStyle = col; g.lineWidth = 5; g.fillRect(-40, 10, 80, 44); g.beginPath(); g.arc(0, 30, 15, 0, 7); g.fillStyle = CREAM; g.fill();
    g.fillStyle = col; g.beginPath(); g.moveTo(-50, -10); g.quadraticCurveTo(0, -40, 50, -10); g.lineTo(42, 4); g.quadraticCurveTo(0, -20, -42, 4); g.closePath(); g.fill(); g.restore(); },
  chat: (g, s, a, col) => { g.save(); g.scale(s, s); g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 6; g.beginPath(); g.roundRect(-50, -40, 100, 66, 12); g.stroke();
    g.beginPath(); g.moveTo(-24, 26); g.lineTo(-34, 46); g.lineTo(-6, 26); g.fill(); for (let i = -1; i <= 1; i++) { g.beginPath(); g.arc(i * 22, -7, 6, 0, 7); g.fill(); } g.restore(); },
  lift: (g, s, a, col) => { g.save(); g.scale(s, s); g.strokeStyle = col; g.lineWidth = 5; g.strokeRect(-36, -50, 72, 100); g.lineWidth = 3;
    for (let i = 0; i < 5; i++) { g.beginPath(); g.moveTo(-30 + i * 12, -44); g.lineTo(-18 + i * 12, 44); g.moveTo(-18 + i * 12, -44); g.lineTo(-30 + i * 12, 44); g.stroke(); } g.restore(); },
  typewriter: (g, s, a, col) => { g.save(); g.scale(s, s); g.fillStyle = col; g.fillRect(-50, 0, 100, 34); g.fillRect(-56, -14, 112, 10); g.fillStyle = CREAM; for (let r = 0; r < 2; r++) for (let i = 0; i < 6; i++) { g.beginPath(); g.arc(-38 + i * 15 + r * 7, 12 + r * 12, 4, 0, 7); g.fill(); }
    g.strokeStyle = col; g.lineWidth = 4; g.strokeRect(-26, -46, 52, 32); g.restore(); },
  person: (g, s, a, col) => person(g, 0, 60 * s, 120 * s, { col }),
};
// biểu tượng là khung sườn: gọi với a = rvH(...)
function icon(g, name, x, y, s, a = 1, col = OCHRE) { if (a <= 0 || !ICONS[name]) return; g.save(); g.globalAlpha *= cl(a); g.translate(x, y); ICONS[name](g, s, a, col); g.restore(); }

// ---------- bóng người (không mặt) ----------
// x,y = chân; hgt = cao px; o: { arm, arm2 (rad), step, hat: cap|top|bowler, coat, flip, pole, col, seated, rim, lift (0..1 ngẩng đầu) }
function person(g, x, y, hgt, o = {}) { const k = hgt / 170, col = o.col || '#1a1410'; g.save(); g.translate(x, y); g.scale(k * (o.flip ? -1 : 1), k); g.fillStyle = col; g.strokeStyle = col; g.lineCap = 'round'; g.lineJoin = 'round';
  if (o.rim) { g.shadowColor = o.rim; g.shadowBlur = 2.75 / k; }
  const step = o.step || 0;
  if (!o.seated) { g.lineWidth = 15; g.beginPath(); g.moveTo(-6, -84); g.lineTo(-10 - 12 * step, 0); g.moveTo(6, -84); g.lineTo(10 + 12 * step, 0); g.stroke(); }
  else { g.lineWidth = 15; g.beginPath(); g.moveTo(-6, -84); g.lineTo(-8, -60); g.moveTo(6, -84); g.lineTo(8, -60); g.stroke(); }
  g.beginPath(); g.moveTo(-20, -84); g.lineTo(-18, -142); g.quadraticCurveTo(0, -150, 18, -142); g.lineTo(20, -84); g.closePath(); g.fill();
  if (o.coat) { g.beginPath(); g.moveTo(-22, -86); g.lineTo(-27, -36); g.lineTo(27, -36); g.lineTo(22, -86); g.fill(); }
  if (o.bun) { g.beginPath(); g.arc(0, -168, 9, 0, 7); g.fill(); }
  const lf = o.lift || 0; if (lf) g.translate(2 * lf, -7 * lf);   // ngẩng đầu (tập 3: giao dịch viên nhìn lên)
  g.beginPath(); g.arc(0, -156, 12, 0, 7); g.fill();
  if (lf) g.translate(-2 * lf, 7 * lf);
  if (o.hat === 'cap') { g.beginPath(); g.ellipse(0, -165, 14, 6, 0, 0, 7); g.fill(); g.fillRect(-2, -166, 20, 4); }
  if (o.hat === 'top') { g.fillRect(-11, -188, 22, 24); g.fillRect(-19, -167, 38, 4); }
  if (o.hat === 'bowler') { g.beginPath(); g.ellipse(0, -166, 13, 11, 0, Math.PI, 0); g.fill(); g.fillRect(-18, -167, 36, 4); }
  if (o.headset) { g.lineWidth = 4; g.beginPath(); g.arc(0, -158, 15, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); }
  const sh = [0, -138], a1 = o.arm === undefined ? 0.2 : o.arm, a2 = o.arm2 === undefined ? -0.15 : o.arm2;
  const AL = 62 * (o.armLen || 1); g.lineWidth = 11; const e1 = [sh[0] + Math.sin(a1) * AL, sh[1] + Math.cos(a1) * AL], e2 = [sh[0] + Math.sin(a2) * AL, sh[1] + Math.cos(a2) * AL];
  g.beginPath(); g.moveTo(...sh); g.lineTo(...e1); g.stroke(); g.beginPath(); g.moveTo(...sh); g.lineTo(...e2); g.stroke();
  if (o.pole) { g.lineWidth = 4; g.beginPath(); g.moveTo(e1[0] - Math.sin(a1) * 30, e1[1] - Math.cos(a1) * 30); g.lineTo(e1[0] + Math.sin(a1) * o.pole, e1[1] + Math.cos(a1) * o.pole); g.stroke(); }
  g.restore(); const sx = o.flip ? -1 : 1;
  return { hand: [x + sx * Math.sin(a1) * 62 * k, y + (-138 + Math.cos(a1) * 62) * k], tip: o.pole ? [x + sx * Math.sin(a1) * (62 + o.pole) * k, y + (-138 + Math.cos(a1) * (62 + o.pole)) * k] : null }; }
function ladder(g, x0, y0, x1, y1, wd, col, lw = 3) { const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = -dy / L * wd / 2, ny = dx / L * wd / 2;
  g.save(); g.strokeStyle = col; g.lineWidth = lw; g.lineCap = 'round'; g.beginPath(); g.moveTo(x0 + nx, y0 + ny); g.lineTo(x1 + nx, y1 + ny); g.moveTo(x0 - nx, y0 - ny); g.lineTo(x1 - nx, y1 - ny);
  const n = Math.max(2, Math.round(L / (wd * 0.9))); for (let i = 1; i < n; i++) { const u = i / n; g.moveTo(x0 + dx * u + nx, y0 + dy * u + ny); g.lineTo(x0 + dx * u - nx, y0 + dy * u - ny); } g.stroke(); g.restore(); }

// ---------- vẽ khung ----------
// LL.SEG = { frames, blur: [[t0,t1]], fadeIn, fadeOut, frame(g, t) } do shot.js dựng từ đặc tả.
LL.camNear = Infinity; LL.cam = (near) => { LL.camNear = Math.min(LL.camNear, near); };
function frameAt(g, t) {
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.setTransform(1, 0, 0, 1, 0, 0);
  LL.SEG.frame(g, t);
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.setTransform(1, 0, 0, 1, 0, 0);
  const S = LL.SEG, fi = S.fadeIn === undefined ? 6 : S.fadeIn, fo = S.fadeOut === undefined ? 6 : S.fadeOut, fr = t * FPS, N = S.frames;
  let k = 0; if (fi > 0 && fr < fi) k = Math.max(k, 1 - sm((fr + 1) / (fi + 1))); if (fo > 0 && fr > N - 1 - fo) k = Math.max(k, sm((fr - (N - 1 - fo)) / (fo + 1)));
  if (k > 0) { g.fillStyle = `rgba(3,4,8,${k})`; g.fillRect(0, 0, W, H); }
}
const ACC = document.createElement('canvas'); ACC.width = W; ACC.height = H; const AX = ACC.getContext('2d');
window.drawFrame = (f) => {
  LL.act = false; LL.fill = false; LL.camNear = Infinity; const t = f / FPS, fast = (LL.SEG.blur || []).some(([a, b]) => t >= a && t <= b), N = fast ? 4 : 1;
  if (N === 1) { frameAt(X, t); return; }
  const keep = LL.tlog; for (let k = 0; k < N; k++) { LL.tlog = k === N - 1 ? keep : null; frameAt(AX, t + ((k + 0.5) / N - 0.5) * 0.5 / FPS); X.globalCompositeOperation = 'source-over'; X.globalAlpha = 1 / (k + 1); X.setTransform(1, 0, 0, 1, 0, 0); X.drawImage(ACC, 0, 0); }
  X.globalAlpha = 1;
};

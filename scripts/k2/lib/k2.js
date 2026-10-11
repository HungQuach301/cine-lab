// KÊNH 2 · thư viện lớp 2D (G2 tập K2G-01). Một mẫu duy nhất `plate` (để dùng nguyên ll.py prep: thu lời, mốc "@từ", nguồn tự sinh, kế hoạch cảnh 3D):
//   nền = cảnh 3D (khung JPG của scripts/k2/hero.js) — rõ (shot cảnh) hoặc mờ + tối (shot thẻ: p.card) — nên mọi thẻ số vẫn "ở" một bối cảnh (luật đa dạng bối cảnh Q26b).
//   Lớp trên: nhãn bám vật thể (p.labels, toạ độ từ anchors.json), dải chú thích (p.cap), tựa (p.title), dòng "Facts as of" (p.asof), thẻ số (p.card: num, bars, line,
//   timeline, split, list, quote, path, layers, end). Nhận diện channel-k2/NHAN-DIEN.md: nền mực #0F1722, chữ #EEF1F4, thép #9AA7B5, nhấn cam #F08A4B, lục lam #3CC2B0, hổ phách #F2C14E (dự báo, nét đứt).
// Chữ: Inter / Inter Display. Cỡ tối thiểu K2 = 30 px ở 16:9 (chữ hoa ≈ 22 px > 18 px của LL Q6; đọc trên điện thoại), 46 px ở 9:16. text() tự nâng cỡ, ghi LL.tlog cho render.js đo tương phản.
'use strict';
const FPS = 24;
const LL = window.LL = window.LL || {}; LL.fmt = LL.fmt || '16x9';
const V = LL.fmt === '9x16', W = V ? 1080 : 1920, H = V ? 1920 : 1080, MINPX = V ? 46 : 30, S = V ? 1.45 : 1;
const cv = document.getElementById('c'); cv.width = W; cv.height = H; const X = cv.getContext('2d');
const K = { ink: '#0F1722', ink2: '#16212f', text: '#EEF1F4', steel: '#9AA7B5', orange: '#F08A4B', teal: '#3CC2B0', amber: '#F2C14E', dim: '#B9C3CE' };
const SAFE = V ? { x0: 70, x1: 1010, y0: 300, y1: 1560 } : { x0: 110, x1: 1810, y0: 70, y1: 1010 };
const cl = (u) => Math.max(0, Math.min(1, u)), sm = (u) => { u = cl(u); return u * u * u * (u * (u * 6 - 15) + 10); }, eo = (u) => { u = cl(u); return 1 - Math.pow(1 - u, 3); };
const pr = (t, a, b) => cl((t - a) / (b - a)), lerp = (a, b, u) => a + (b - a) * u;
LL.act = false; LL.fill = false; LL.stat = { raised: 0, rmax: 0 }; LL.tlog = null; LL.zones = [];
const rv = (t, a, d = 0.5) => { if (a === undefined || a === null) a = -1e9; const u = cl((t - a) / d); if (u > 0 && u < 1) LL.act = true; if (u > 0) LL.fill = true; return u; };
const rvH = (t, a, d = 0.5) => cl((t - (a === undefined || a === null ? -1e9 : a)) / d);
const vis = (t, at, out, d = 0.45) => Math.min(rv(t, at, d), out === undefined || out === null ? 1 : 1 - cl((t - out) / 0.35));
const font = (px, w = 600, disp = false) => `${w} ${Math.round(px)}px "${disp ? 'Inter Display' : 'Inter'}", Inter, sans-serif`;
const effScale = (g) => { const m = g.getTransform(); return Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)); };
function fitPx(g, px) { const s = effScale(g) || 1; if (px * s >= MINPX - 0.01) return px; LL.stat.raised++; LL.stat.rmax = Math.max(LL.stat.rmax, MINPX / s - px); return MINPX / s; }
function tw(g, s, px, w = 600, disp = false) { g.save(); g.font = font(fitPx(g, px), w, disp); const r = g.measureText(String(s)).width; g.restore(); return r; }
// chữ: o = { a, w (độ đậm), disp (Inter Display), align, base, deco, maxW }
function text(g, s, x, y, px, color, o = {}) {
  s = String(s); if (!s) return 0; const a = o.a === undefined ? 1 : o.a; if (a <= 0.01) return 0;
  let p = fitPx(g, px); const w0 = o.w || 600;
  if (o.maxW) { g.save(); g.font = font(p, w0, o.disp); const mw = g.measureText(s).width; g.restore(); if (mw > o.maxW) { const q = Math.max(MINPX, p * o.maxW / mw); if (q < p) { p = q; LL.stat.fit = (LL.stat.fit || 0) + 1; } } }
  g.save(); g.globalAlpha *= cl(a); g.font = font(p, w0, o.disp); g.fillStyle = color; g.textAlign = o.align || 'left'; g.textBaseline = o.base || 'alphabetic';
  g.fillText(s, x, y); const wd = g.measureText(s).width;
  if (LL.tlog && g.globalAlpha > 0.5 && !o.deco) { const m = g.getTransform(), al = g.textAlign, bl = g.textBaseline;
    const x0 = al === 'center' ? x - wd / 2 : al === 'right' ? x - wd : x, cap = p * 0.727, yb = bl === 'middle' ? y + cap / 2 : bl === 'top' ? y + cap : y;
    const P = [[x0, yb - cap], [x0 + wd, yb - cap], [x0, yb], [x0 + wd, yb]].map(([u, v]) => [m.a * u + m.c * v + m.e, m.b * u + m.d * v + m.f]);
    LL.tlog.push({ s: s.slice(0, 40), color, alpha: +g.globalAlpha.toFixed(2), cap: +(cap * effScale(g)).toFixed(1), box: [Math.min(...P.map((q) => q[0])), Math.min(...P.map((q) => q[1])), Math.max(...P.map((q) => q[0])), Math.max(...P.map((q) => q[1]))].map(Math.round) }); }
  g.restore(); return wd; }
function wrap(g, s, maxW, px, w = 600, disp = false) { g.save(); g.font = font(fitPx(g, px), w, disp); const out = []; let a = ''; for (const wd of String(s).split(' ')) { const n = a ? a + ' ' + wd : wd; if (g.measureText(n).width > maxW && a) { out.push(a); a = wd; } else a = n; } out.push(a); g.restore(); return out; }
function para(g, s, x, y, maxW, px, color, o = {}) { const L = wrap(g, s, maxW, px, o.w, o.disp), lh = o.lh || px * 1.28; L.forEach((l, i) => text(g, l, x, y + i * lh, px, color, o)); return y + (L.length - 1) * lh; }
function rrect(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function panel(g, x, y, w, h, o = {}) { const a = o.a === undefined ? 1 : o.a; if (a <= 0.01) return; g.save(); g.globalAlpha *= a; g.shadowColor = 'rgba(0,0,0,0.45)'; g.shadowBlur = 30; g.shadowOffsetY = 10;
  rrect(g, x, y, w, h, o.r || 10); g.fillStyle = o.fill || 'rgba(15,23,34,0.86)'; g.fill(); g.shadowColor = 'transparent';
  g.strokeStyle = o.stroke || 'rgba(154,167,181,0.35)'; g.lineWidth = 1.5; if (o.dash) g.setLineDash([12, 8]); g.stroke(); g.setLineDash([]);
  if (o.accent) { g.fillStyle = o.accent; g.fillRect(x, y + 8, 6, h - 16); } g.restore(); }
// nhãn loại số: ACTUAL viền liền; PROJECTION nét đứt hổ phách
function kindTag(g, kind, x, y, a = 1, align = 'left') { if (a <= 0.01 || !kind) return 0; const pj = kind === 'projection', s = pj ? 'PROJECTION' : 'ACTUAL', px = 26 * S;
  const p = Math.max(px, MINPX * 0.9), wd = tw(g, s, p, 700) + p * 0.9, h = p * 1.5, x0 = align === 'right' ? x - wd : align === 'center' ? x - wd / 2 : x;
  g.save(); g.globalAlpha *= a; g.strokeStyle = pj ? K.amber : K.steel; g.lineWidth = 2.4; if (pj) g.setLineDash([9, 6]); g.strokeRect(x0, y - h / 2, wd, h); g.restore();
  text(g, s, x0 + p * 0.45, y + 1, p, pj ? K.amber : K.dim, { a, w: 700, base: 'middle' }); return wd; }
function srcLine(g, s, x, y, a = 1, align = 'left') { if (!s || !String(s).trim()) return; text(g, s, x, y, MINPX, K.dim, { a, w: 500, align, maxW: (V ? W - 2 * 70 : 1500) }); }

// ---------- cảnh 3D nền ----------
LL.camNear = Infinity;
function plateIdx(p, t) { return Math.max(0, Math.min((p.n || 1) - 1, Math.round((t - p.t0) * FPS * (p.speed || 1)) + (p.off || 0))); }
function drawPlate(g, p, t, blur = 0, dim = 0) { const im = window.PLATES[p.dir + '#' + plateIdx(p, t)];
  if (!im) { g.fillStyle = K.ink; g.fillRect(0, 0, W, H); text(g, 'missing plate', 60, 80, 30, '#f55', { deco: true }); return; }
  // khung 3D có thể 960×540 (nháp) hoặc 1920×1080; 9:16 lấy đúng khổ
  g.save(); if (blur > 0) g.filter = `blur(${Math.round(blur)}px)`; const sc = blur > 0 ? 1.04 : 1; g.drawImage(im, -(sc - 1) * W / 2, -(sc - 1) * H / 2, W * sc, H * sc); g.filter = 'none'; g.restore();
  if (dim > 0) { g.fillStyle = `rgba(10,15,23,${dim})`; g.fillRect(0, 0, W, H); } }
function anc(p, t, name) { const A = window.ANC[p.dir]; if (!A) return null; const f = plateIdx(p, t); const e = (A[f] || A[String(f)] || {})[name]; return e ? { x: e[0] * W, y: e[1] * H, v: e[2] } : null; }

// ---------- lớp phủ trên cảnh ----------
// nhãn bám vật thể: {a: tên điểm neo, s, sub, at, out, dx, dy, c (màu nhấn), side: 'up'|'down'|'left'|'right'}
function labels(g, p, t) { for (const L of p.labels || []) { const u = vis(t, L.at, L.out); if (u <= 0.01) continue; const A = anc(p, t, L.a); if (!A || !A.v) continue;
  const px = (L.px || 34) * S, spx = 30 * S, w1 = tw(g, L.s, px, 700, true), w2 = L.sub ? tw(g, L.sub, spx, 500) : 0, bw = Math.max(w1, w2) + 44, bh = L.sub ? px * 1.25 + spx * 1.35 + 26 : px * 1.25 + 24;
  const dx = (L.dx === undefined ? 0 : L.dx) * S, dy = (L.dy === undefined ? -150 : L.dy) * S; let bx = A.x + dx - bw / 2, by = A.y + dy - bh / 2;
  bx = Math.max(SAFE.x0, Math.min(SAFE.x1 - bw, bx)); by = Math.max(SAFE.y0, Math.min(SAFE.y1 - 200 * S - bh, by)); const c = L.c || K.orange;
  g.save(); g.globalAlpha *= u; g.strokeStyle = c; g.lineWidth = 2.5; const ex = Math.max(bx, Math.min(bx + bw, A.x)), ey = A.y < by ? by : by + bh;
  g.beginPath(); g.moveTo(A.x, A.y); g.lineTo(ex, ey); g.stroke(); g.fillStyle = c; g.beginPath(); g.arc(A.x, A.y, 6, 0, 7); g.fill(); g.strokeStyle = 'rgba(255,255,255,0.7)'; g.lineWidth = 1.5; g.beginPath(); g.arc(A.x, A.y, 11 + 3 * Math.sin(t * 3), 0, 7); g.stroke(); g.restore();
  panel(g, bx, by, bw, bh, { a: u, accent: c, dash: L.kind === 'projection' }); text(g, L.s, bx + 24, by + 14 + px * 0.95, px, K.text, { a: u, w: 700, disp: true }); if (L.sub) text(g, L.sub, bx + 24, by + 14 + px * 1.25 + spx * 1.0, spx, L.subc || K.dim, { a: u, w: 500 }); LL.fill = true; } }
// dải chú thích dưới: {s, at, big (số lớn), kind, src}; hiện mục mới nhất
function caps(g, p, t) { const Cs = p.cap || []; let k = -1; Cs.forEach((c, i) => { if (t >= c.at) k = i; }); if (k < 0 && !p.src) return;
  const c = k >= 0 ? Cs[k] : null, a = c ? rv(t, c.at, 0.45) : 0, srcS = (c && c.src) || p.src, y0 = V ? H * 0.70 : H * 0.735;
  const gr = g.createLinearGradient(0, y0 - (V ? 160 : 80), 0, H); gr.addColorStop(0, 'rgba(8,12,18,0)'); gr.addColorStop(0.35, `rgba(8,12,18,${0.78 * Math.max(a, srcS ? 0.85 : 0)})`); gr.addColorStop(1, `rgba(8,12,18,${0.9 * Math.max(a, srcS ? 0.85 : 0)})`);
  g.fillStyle = gr; g.fillRect(0, y0 - (V ? 160 : 80), W, H - y0 + 160); const x = V ? W / 2 : SAFE.x0, al = V ? 'center' : 'left', mw = V ? W - 140 : 1500;
  if (c) { let y = y0 + (V ? 60 : 50); if (c.big) { text(g, c.big, x, y + (V ? 70 : 60), (V ? 110 : 96), c.kind === 'projection' ? K.amber : K.orange, { a, w: 700, disp: true, align: al }); if (c.kind) kindTag(g, c.kind, V ? W / 2 : x + tw(g, c.big, 96, 700, true) + 30, y + (V ? 130 : 30), a, V ? 'center' : 'left'); y += V ? 170 : 105; }
    const L = wrap(g, c.s || '', mw, (V ? 54 : 44), 600); L.slice(0, 2).forEach((l, i) => text(g, l, x, y + 10 + i * (V ? 66 : 54), (V ? 54 : 44), K.text, { a, w: 600, align: al })); }
  if (srcS) srcLine(g, srcS, x, H - (V ? 260 : 44), 1, al); if (p.credit) text(g, p.credit, W - SAFE.x0, H - 44, MINPX, K.dim, { align: 'right', w: 500 }); }
// tựa lớn: {t, sub, at, out, kicker}
function title(g, p, t) { const T = p.title; if (!T) return; const u = vis(t, T.at === undefined ? 0 : T.at, T.out, 0.7); if (u <= 0.01) return;
  const cx = W / 2, cy = V ? H * 0.42 : H * 0.44; const gr = g.createRadialGradient(cx, cy, 50, cx, cy, W * 0.6); gr.addColorStop(0, `rgba(8,12,18,${0.62 * u})`); gr.addColorStop(1, 'rgba(8,12,18,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  if (T.kicker) text(g, T.kicker, cx, cy - (V ? 150 : 120), (V ? 46 : 38), K.orange, { a: u, w: 700, align: 'center' });
  text(g, T.t, cx, cy, (V ? 120 : 132) * (T.scale || 1), K.text, { a: u, w: 700, disp: true, align: 'center', maxW: W - 200 });
  g.save(); g.globalAlpha *= u; g.fillStyle = K.orange; g.fillRect(cx - 60, cy + 34, 120 * eo((t - (T.at || 0)) / 0.8), 6); g.restore();
  if (T.sub) para(g, T.sub, cx, cy + (V ? 130 : 110), V ? W - 160 : 1400, (V ? 50 : 44), K.dim, { a: u, w: 500, align: 'center' }); }
function asof(g, p, t) { if (!p.asof) return; const u = vis(t, p.asofAt === undefined ? p.t0 : p.asofAt); const s = p.asof === true ? 'Facts as of 11 Oct 2026' : p.asof;
  const px = 30 * S, wd = tw(g, s, px, 600) + 40, x = W - SAFE.x0 - wd, y = V ? 210 : 56; panel(g, x, y, wd, px * 1.7, { a: u, stroke: 'rgba(242,193,78,0.6)' }); text(g, s, x + 20, y + px * 1.18, px, K.amber, { a: u, w: 600 }); }

// ---------- thẻ (nền: cảnh 3D mờ) ----------
const CARD = V ? { x: 60, y: 300, w: 960, h: 1220 } : { x: 150, y: 96, w: 1620, h: 780 };
function cardFrame(g, c, t, u) { const R = CARD; panel(g, R.x, R.y, R.w, R.h, { a: u, fill: 'rgba(13,20,30,0.80)', accent: c.accent || K.orange, r: 14 });
  // lưới kỹ thuật mảnh
  g.save(); g.globalAlpha *= 0.5 * u; g.strokeStyle = 'rgba(154,167,181,0.08)'; g.lineWidth = 1; for (let x = R.x + 40; x < R.x + R.w; x += 40) { g.beginPath(); g.moveTo(x, R.y + 8); g.lineTo(x, R.y + R.h - 8); g.stroke(); } for (let y = R.y + 40; y < R.y + R.h; y += 40) { g.beginPath(); g.moveTo(R.x + 8, y); g.lineTo(R.x + R.w - 8, y); g.stroke(); } g.restore();
  if (c.kicker) text(g, c.kicker, R.x + 50, R.y + 62 * S, 30 * S, c.accent || K.orange, { a: u, w: 700 });
  if (c.title) para(g, c.title, R.x + 50, R.y + (c.kicker ? 118 : 80) * S, R.w - 100, 50 * S, K.text, { a: u, w: 700, disp: true }); }
const TPLC = {};
// số lớn: {value/text, s (nhãn), sub, kind, at, beats: [{s, at}], unit}
TPLC.num = (g, c, t, u) => { const R = CARD, cx = R.x + R.w / 2, a = rv(t, c.at, 0.6), big = c.big || c.text || String(c.value);
  const cy = R.y + R.h * (V ? 0.42 : 0.47); text(g, big, cx, cy, (V ? 170 : 210) * (c.scale || 1), c.kind === 'projection' ? K.amber : K.orange, { a: a * u, w: 700, disp: true, align: 'center', maxW: R.w - 120 });
  if (c.unit) text(g, c.unit, cx, cy + (V ? 90 : 80), (V ? 50 : 48), K.text, { a: a * u, w: 600, align: 'center', maxW: R.w - 120 });
  if (c.kind) kindTag(g, c.kind, cx, cy - (V ? 210 : 240), a * u, 'center');
  let y = cy + (V ? 190 : 165); for (const b of c.beats || []) { const ab = rv(t, b.at, 0.45); y = para(g, b.s, cx, y, R.w - 160, (b.px || 40) * S, b.c || K.dim, { a: ab * u, w: 500, align: 'center' }) + 56 * S; } };
// cột: {items: [{label, value, text, at, c, hatch}], max, ref: {value, label, at}, unit, horizontal (mặc định), note}
TPLC.bars = (g, c, t, u) => { const R = CARD, x0 = R.x + (V ? 60 : 420), x1 = R.x + R.w - (V ? 60 : 220), top = R.y + (c.title ? 230 : 150) * S, n = c.items.length, rowH = Math.min(V ? 220 : 150, (R.h - (top - R.y) - 120) / n), mx = c.max || Math.max(...c.items.map((i) => i.value)) * 1.08;
  c.items.forEach((it, i) => { const y = top + i * rowH, a = rv(t, it.at, 0.8), w = (x1 - x0) * it.value / mx * eo((t - (it.at || -1e9)) / 0.8); const col = it.c || K.orange;
    if (V) text(g, it.label, x0, y + 10, 38, K.text, { a: u * rvH(t, it.at), w: 600 }); else text(g, it.label, x0 - 30, y + rowH * 0.45, 38, K.text, { a: u * rvH(t, it.at), w: 600, align: 'right', maxW: 340 });
    const by = V ? y + 30 : y + rowH * 0.45 - 34, bh = V ? 70 : 68; g.save(); g.globalAlpha *= u; g.fillStyle = 'rgba(154,167,181,0.10)'; g.fillRect(x0, by, x1 - x0, bh);
    g.fillStyle = col; if (it.hatch) { g.globalAlpha *= 0.9; } g.fillRect(x0, by, w, bh); if (it.dash) { g.setLineDash([10, 7]); g.strokeStyle = K.amber; g.lineWidth = 3; g.strokeRect(x0, by, w, bh); } g.restore();
    const tx = it.text || String(it.value); text(g, tx, Math.min(x0 + w + 20, x1 - tw(g, tx, 44, 700, true)), by + bh * 0.72, 44, K.text, { a: a * u, w: 700, disp: true }); });
  if (c.ref) { const xr = x0 + (x1 - x0) * c.ref.value / mx, a = rv(t, c.ref.at, 0.5); g.save(); g.globalAlpha *= a * u; g.setLineDash([12, 8]); g.strokeStyle = K.teal; g.lineWidth = 3; g.beginPath(); g.moveTo(xr, top - 40); g.lineTo(xr, top + n * rowH); g.stroke(); g.restore();
    text(g, c.ref.label, xr, top + n * rowH + 50 * S, 32 * S, K.teal, { a: a * u, w: 600, align: xr > x1 - 300 ? 'right' : 'center' }); }
  if (c.note) para(g, c.note, R.x + 50, R.y + R.h - 110 * S, R.w - 100, 32 * S, K.dim, { a: u * rvH(t, c.noteAt), w: 500 }); };
// đường: {pts: [{x, value, text, at, label, peak}], xmin, xmax, ymax, unit, notes: [{x, s, at}]}
TPLC.line = (g, c, t, u) => { const R = CARD, gx0 = R.x + 140, gx1 = R.x + R.w - 120, gy0 = R.y + R.h - 140, gy1 = R.y + 230, X = (x) => gx0 + (gx1 - gx0) * (x - c.xmin) / (c.xmax - c.xmin), Y = (v) => gy0 - (gy0 - gy1) * v / c.ymax;
  g.save(); g.globalAlpha *= u; g.strokeStyle = 'rgba(154,167,181,0.5)'; g.lineWidth = 2; g.beginPath(); g.moveTo(gx0, gy1 - 20); g.lineTo(gx0, gy0); g.lineTo(gx1 + 20, gy0); g.stroke();
  for (let v = 0; v <= c.ymax; v += c.ystep || 50) { g.strokeStyle = 'rgba(154,167,181,0.12)'; g.beginPath(); g.moveTo(gx0, Y(v)); g.lineTo(gx1, Y(v)); g.stroke(); } g.restore();
  for (let v = 0; v <= c.ymax; v += c.ystep || 50) text(g, String(v), gx0 - 20, Y(v) + 11, 30, K.dim, { a: u, w: 500, align: 'right' });
  if (c.unit) text(g, c.unit, gx0, gy1 - 40, 30, K.dim, { a: u, w: 500 });
  for (const x of c.ticks || []) text(g, String(x), X(x), gy0 + 48, 32, K.dim, { a: u, w: 600, align: 'center' });
  const P = c.pts; g.save(); g.globalAlpha *= u; g.strokeStyle = K.orange; g.lineWidth = 6; g.lineJoin = 'round'; g.beginPath(); let started = false;
  for (let i = 0; i < P.length; i++) { const q = P[i], k = i ? eo((t - q.at) / 0.9) : rvH(t, q.at); if (k <= 0) break; const px0 = i ? X(P[i - 1].x) : X(q.x), py0 = i ? Y(P[i - 1].value) : Y(q.value); const xx = lerp(px0, X(q.x), k), yy = lerp(py0, Y(q.value), k); if (!started) { g.moveTo(xx, yy); started = true; } else g.lineTo(xx, yy); } g.stroke(); g.restore();
  for (const q of P) { const a = rv(t, (q.at || 0) + 0.6, 0.4); if (a <= 0) continue; g.save(); g.globalAlpha *= a * u; g.fillStyle = K.orange; g.beginPath(); g.arc(X(q.x), Y(q.value), 9, 0, 7); g.fill(); g.restore();
    if (q.text) { const up = q.below ? 1 : -1; text(g, q.text, X(q.x), Y(q.value) + up * -1 * (q.below ? -62 : 34), 42, K.text, { a: a * u, w: 700, disp: true, align: q.align || 'center' }); if (q.label) text(g, q.label, X(q.x), Y(q.value) + (q.below ? 100 : -78), 30, K.dim, { a: a * u, w: 500, align: q.align || 'center' }); } }
  for (const nt of c.notes || []) { const a = rv(t, nt.at, 0.5); if (a <= 0) continue; const xx = X(nt.x); g.save(); g.globalAlpha *= a * u; g.setLineDash([8, 6]); g.strokeStyle = K.teal; g.lineWidth = 2; g.beginPath(); g.moveTo(xx, gy1); g.lineTo(xx, gy0); g.stroke(); g.restore();
    text(g, nt.s, xx + 14, gy1 + 36 + (nt.dy || 0), 32, K.teal, { a: a * u, w: 600 }); } };
// mốc thời gian: {items: [{date, s, sub, at, c}]} — dọc (9:16) hoặc ngang thành hàng
TPLC.timeline = (g, c, t, u) => { const R = CARD, n = c.items.length, y = R.y + (c.title ? 330 : 260), x0 = R.x + 90, x1 = R.x + R.w - 90;
  if (!V) { const step = (x1 - x0) / Math.max(1, n - 1); g.save(); g.globalAlpha *= u; g.strokeStyle = 'rgba(154,167,181,0.4)'; g.lineWidth = 3; g.beginPath(); g.moveTo(x0, y); g.lineTo(x1, y); g.stroke(); g.restore();
    let last = -1; c.items.forEach((it, i) => { if (t >= (it.at || 0)) last = i; });
    c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5), x = x0 + i * step, col = it.c || (i === last ? K.orange : K.steel); if (a <= 0) return;
      g.save(); g.globalAlpha *= a * u; g.fillStyle = col; g.beginPath(); g.arc(x, y, i === last ? 14 : 10, 0, 7); g.fill(); g.restore();
      const al = i === 0 ? 'left' : i === n - 1 ? 'right' : 'center', xx = i === 0 ? x - 12 : i === n - 1 ? x + 12 : x, mw = Math.min(step * 1.05, 420);
      text(g, it.date, xx, y - 40, 36, i === last ? K.orange : K.text, { a: a * u, w: 700, disp: true, align: al, maxW: mw });
      if (it.big) text(g, it.big, xx, y + 110, 76, i === last ? K.orange : K.text, { a: a * u, w: 700, disp: true, align: al });
      L = wrap(g, it.s, mw, 32, 500); L.slice(0, 4).forEach((l, j) => text(g, l, xx, y + (it.big ? 175 : 70) + j * 42, 32, i === last ? K.text : K.dim, { a: a * u, w: 500, align: al })); }); }
  else { const step = Math.min(200, (R.h - 300) / n); c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5), yy = R.y + 260 + i * step; if (a <= 0) return; g.save(); g.globalAlpha *= a * u; g.fillStyle = it.c || K.orange; g.beginPath(); g.arc(R.x + 70, yy, 12, 0, 7); g.fill(); g.restore();
    text(g, it.date + (it.big ? '  ' + it.big : ''), R.x + 110, yy + 14, 48, K.text, { a: a * u, w: 700, disp: true }); para(g, it.s, R.x + 110, yy + 72, R.w - 160, 46, K.dim, { a: a * u, w: 500 }); }); } };
let L;
// hai cột: {left: {tag, title, lines: [{s, at}], c}, right: {...}, mid: 'vs'}
TPLC.split = (g, c, t, u) => { const R = CARD, gap = 40, cw = V ? R.w - 80 : (R.w - 100 - gap) / 2, top = R.y + (c.title ? 230 : 70);
  [c.left, c.right].forEach((col, k) => { if (!col) return; const a = rv(t, col.at, 0.5); if (a <= 0) return; const x = V ? R.x + 40 : R.x + 50 + k * (cw + gap), y = V ? top + k * (R.h - (top - R.y)) / 2 : top, h = V ? (R.h - (top - R.y)) / 2 - 30 : R.h - (top - R.y) - 50;
    panel(g, x, y, cw, h, { a: a * u, accent: col.c || (k ? K.teal : K.orange), fill: 'rgba(22,33,47,0.9)', dash: col.dash });
    text(g, col.tag, x + 34, y + 62, 32 * S, col.c || (k ? K.teal : K.orange), { a: a * u, w: 700 }); let yy = col.title ? para(g, col.title, x + 34, y + 130, cw - 70, 44 * S, K.text, { a: a * u, w: 700, disp: true }) + 80 : y + 130;
    for (const ln of col.lines || []) { const b = rv(t, ln.at, 0.45); if (b <= 0) continue; g.save(); g.globalAlpha *= b * u; g.fillStyle = col.c || (k ? K.teal : K.orange); g.fillRect(x + 34, yy - 26 * S, 10, 10); g.restore(); yy = para(g, ln.s, x + 60, yy, cw - 100, 36 * S, ln.c || K.text, { a: b * u, w: 500 }) + 60 * S; } }); };
// danh sách / luồng: {items: [{s, sub, at}], flow (mũi tên giữa các bước), num (đánh số)}
TPLC.list = (g, c, t, u) => { const R = CARD, n = c.items.length, top = R.y + (c.title ? 250 : 120) * S;
  if (c.flow && !V) { const bw = (R.w - 100 - (n - 1) * 50) / n; c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5); if (a <= 0) return; const x = R.x + 50 + i * (bw + 50), y = top + 20, h = R.h - (top - R.y) - 140;
      panel(g, x, y, bw, h, { a: a * u, accent: it.c || K.orange, fill: 'rgba(22,33,47,0.92)' }); text(g, String(i + 1), x + 30, y + 72, 56, it.c || K.orange, { a: a * u, w: 700, disp: true });
      const ye = para(g, it.s, x + 30, y + 150, bw - 54, 38, K.text, { a: a * u, w: 700 }); if (it.sub) para(g, it.sub, x + 30, ye + 56, bw - 54, 31, K.dim, { a: a * u, w: 500 });
      if (i < n - 1) { g.save(); g.globalAlpha *= a * u; g.fillStyle = K.steel; g.beginPath(); g.moveTo(x + bw + 12, y + h / 2 - 16); g.lineTo(x + bw + 38, y + h / 2); g.lineTo(x + bw + 12, y + h / 2 + 16); g.fill(); g.restore(); } }); return; }
  let y = top + 20; c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5); if (a <= 0) { y += 0; return; } g.save(); g.globalAlpha *= a * u; g.strokeStyle = it.c || K.orange; g.lineWidth = 3; g.strokeRect(R.x + 60, y - 30 * S, 30 * S, 30 * S);
    if (it.check !== false) { g.beginPath(); g.moveTo(R.x + 66, y - 14 * S); g.lineTo(R.x + 60 + 13 * S, y - 6); g.lineTo(R.x + 60 + 26 * S, y - 26 * S); g.stroke(); } g.restore();
    y = para(g, it.s, R.x + 60 + 54 * S, y, R.w - 180, 40 * S, K.text, { a: a * u, w: 600 }); if (it.sub) y = para(g, it.sub, R.x + 60 + 54 * S, y + 46 * S, R.w - 180, 32 * S, K.dim, { a: a * u, w: 500 }); y += 76 * S; }); };
// trích: {q, by, at}
TPLC.quote = (g, c, t, u) => { const R = CARD, a = rv(t, c.at, 0.7); text(g, '“', R.x + 70, R.y + 220 * S, 200, K.orange, { a: a * u, w: 700, disp: true, deco: true });
  const y = para(g, c.q, R.x + 140, R.y + 210 * S, R.w - 260, (c.px || 56) * S, K.text, { a: a * u, w: 600, disp: true, lh: (c.px || 56) * 1.32 * S });
  if (c.by) para(g, '— ' + c.by, R.x + 140, y + 90 * S, R.w - 260, 34 * S, K.dim, { a: rvH(t, (c.at || 0) + 0.6) * u, w: 500 }); };
// con đường: {nodes: [{s, at}], tolls: [{i (sau nút i), s, at, c}], q: [{s, at}]}
TPLC.path = (g, c, t, u) => { const R = CARD, n = c.nodes.length, y = R.y + R.h * (V ? 0.38 : 0.5), x0 = R.x + 120, x1 = R.x + R.w - 120, step = (x1 - x0) / (n - 1);
  const yy = (i) => V ? R.y + 260 + i * (R.h - 420) / (n - 1) : y, xx = (i) => V ? R.x + 140 : x0 + i * step;
  for (let i = 0; i < n; i++) { const nd = c.nodes[i], a = rv(t, nd.at, 0.5); if (a <= 0) continue;
    if (i) { const k = eo((t - nd.at) / 0.6); g.save(); g.globalAlpha *= u; g.strokeStyle = K.orange; g.lineWidth = 8; g.beginPath(); g.moveTo(xx(i - 1), yy(i - 1)); g.lineTo(lerp(xx(i - 1), xx(i), k), lerp(yy(i - 1), yy(i), k)); g.stroke(); g.restore(); }
    g.save(); g.globalAlpha *= a * u; g.fillStyle = K.ink2; g.strokeStyle = K.orange; g.lineWidth = 4; g.beginPath(); g.arc(xx(i), yy(i), 26, 0, 7); g.fill(); g.stroke(); g.restore();
    if (V) text(g, nd.s, xx(i) + 60, yy(i) + 16, 46, K.text, { a: a * u, w: 700 }); else text(g, nd.s, xx(i), yy(i) + (i % 2 ? 90 : -56), 38, K.text, { a: a * u, w: 700, align: 'center', maxW: step * 1.2 }); }
  for (const tl of c.tolls || []) { const a = rv(t, tl.at, 0.5); if (a <= 0) continue; const xm = V ? xx(0) : (xx(tl.i) + xx(tl.i + 1)) / 2, ym = V ? (yy(tl.i) + yy(tl.i + 1)) / 2 : y, col = tl.c || K.teal;
    g.save(); g.globalAlpha *= a * u; g.fillStyle = col; if (V) { g.fillRect(xm - 50, ym - 6, 100, 12); g.fillRect(xm - 56, ym - 30, 12, 60); } else { g.fillRect(xm - 6, ym - 50, 12, 100); g.fillRect(xm - 30, ym - 56, 60, 12); } g.restore();
    if (V) text(g, tl.s, xm + 60, ym + 14, 40, col, { a: a * u, w: 700 }); else text(g, tl.s, xm, ym + (tl.below ? 120 : -100), 34, col, { a: a * u, w: 700, align: 'center' }); }
  let qy = V ? R.y + R.h - 120 : R.y + R.h - 110; for (const q of c.q || []) { const a = rv(t, q.at, 0.5); if (a <= 0) continue; text(g, q.s, R.x + R.w / 2, qy, (q.px || 46) * S, q.c || K.orange, { a: a * u, w: 700, disp: true, align: 'center', maxW: R.w - 100 }); qy += 70 * S; } };
// ba tầng: {rows: [{k (nhãn), s, sub, at, c}], hi (giây làm nổi hàng cuối)}
TPLC.layers = (g, c, t, u) => { const R = CARD, n = c.rows.length, top = R.y + (c.title ? 220 : 90), rh = (R.h - (top - R.y) - 60) / n;
  let last = -1; c.rows.forEach((r, i) => { if (t >= (r.at || 0)) last = i; });
  c.rows.forEach((r, i) => { const a = rv(t, r.at, 0.55); if (a <= 0) return; const y = top + i * rh, off = (n - 1 - i) * 40 * (V ? 0 : 1), col = r.c || [K.steel, K.orange, K.teal][i % 3];
    panel(g, R.x + 60 + off, y, R.w - 120 - 2 * off, rh - 24, { a: a * u, accent: col, fill: i === last ? 'rgba(30,44,62,0.95)' : 'rgba(22,33,47,0.85)' });
    text(g, r.k, R.x + 100 + off, y + rh * 0.42, 34 * S, col, { a: a * u, w: 700 }); text(g, r.s, R.x + (V ? 100 : 420) + off, y + (V ? rh * 0.42 + 64 : rh * 0.42), 42 * S, K.text, { a: a * u, w: 700, disp: true, maxW: R.w - (V ? 220 : 560) - 2 * off });
    if (r.sub) text(g, r.sub, R.x + (V ? 100 : 420) + off, y + (V ? rh * 0.42 + 120 : rh * 0.42 + 50), 32 * S, K.dim, { a: a * u, w: 500, maxW: R.w - (V ? 220 : 560) - 2 * off }); }); };
// thẻ kết
TPLC.end = (g, c, t, u) => { const R = CARD, cx = R.x + R.w / 2; (c.lines || []).forEach((l, i) => text(g, l.s, cx, R.y + R.h * 0.36 + i * (l.gap || 90) * S, (l.px || 48) * S, l.c || K.text, { a: rv(t, l.at, 0.6) * u, w: l.w || 600, disp: !!l.disp, align: 'center', maxW: R.w - 120 })); };

// ---------- mẫu plate (duy nhất) ----------
const TPL = {};
TPL.plate = (p) => ({ kind: 'full', full(g, t) {
  const c = p.card, blur = c ? (p.blur === undefined ? 14 : p.blur) : (p.blur || 0), dim = c ? (p.dim === undefined ? 0.45 : p.dim) : (p.dim || 0);
  drawPlate(g, p, t, blur, dim); if (!c) { labels(g, p, t); title(g, p, t); }
  if (c) { const u = vis(t, c.in === undefined ? p.t0 : c.in, c.out, 0.5); cardFrame(g, c, t, u); (TPLC[c.type] || (() => {}))(g, c, t, u); LL.fill = true;
    if (p.src) srcLine(g, p.src, CARD.x + 50, CARD.y + CARD.h - 34, u); }
  else caps(g, p, t);
  asof(g, p, t); } });

// thẻ cuối Short (ll.py tự chèn tpl 'endcard', p.line)
TPL.endcard = (p) => ({ kind: 'full', full(g, t) { g.fillStyle = K.ink; g.fillRect(0, 0, W, H); const a = rvH(t, p.t0, 0.4);
  text(g, 'STEEL', W / 2, H * 0.42, V ? 130 : 120, K.text, { a, w: 700, disp: true, align: 'center' }); g.save(); g.globalAlpha *= a; g.fillStyle = K.orange; g.fillRect(W / 2 - 60, H * 0.42 + 36, 120, 6); g.restore();
  text(g, p.line || 'full film on the channel', W / 2, H * 0.42 + 130, V ? 52 : 44, K.dim, { a, w: 600, align: 'center' }); } });

// ---------- ghép shot trong đoạn ----------
(() => {
  const SP = window.SPEC, shots = SP.shots.map((s) => Object.assign({}, s, { T: TPL[s.tpl](Object.assign({ t0: s.t0, t1: s.t1 }, s.p)) }));
  const off = document.createElement('canvas'); off.width = W; off.height = H; const OX = off.getContext('2d');
  const one = (g, s, t) => { g.save(); s.T.full(g, t); g.restore(); };
  function hook(g, t) { if (!SP.hook) return; const a = rvH(t, 0.15, 0.6); const Lh = wrap(g, SP.hook, W - 140, 58, 700, true), hb = 150 + (Lh.length - 1) * 72 + 40;
    const gr = g.createLinearGradient(0, 0, 0, hb + 70); gr.addColorStop(0, `rgba(8,12,18,${0.85 * a})`); gr.addColorStop(hb / (hb + 70), `rgba(8,12,18,${0.75 * a})`); gr.addColorStop(1, 'rgba(8,12,18,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, hb + 70);
    Lh.forEach((l, i) => text(g, l, W / 2, 140 + i * 72, 58, K.text, { align: 'center', w: 700, disp: true, a })); }
  LL.SEG = { frames: SP.frames, fadeIn: SP.fadeIn, fadeOut: SP.fadeOut, frame(g, t) {
    let i = shots.findIndex((s) => t >= s.t0 && t < s.t1); if (i < 0) i = t < shots[0].t0 ? 0 : shots.length - 1;
    const s = shots[i], tr = s.in || { type: 'cut' }, d = tr.d || 0.7, u = i > 0 && tr.type !== 'cut' ? pr(t, s.t0, s.t0 + d) : 1;
    if (u < 1) { LL.act = true; const q = shots[i - 1], e = sm(u), keep = LL.tlog; LL.tlog = null; one(g, q, t); OX.setTransform(1, 0, 0, 1, 0, 0); OX.globalAlpha = 1; OX.globalCompositeOperation = 'source-over'; one(OX, s, t);
      if (tr.type === 'wipe') { g.save(); g.beginPath(); g.rect(0, 0, W * e, H); g.clip(); g.drawImage(off, 0, 0); g.restore(); g.save(); g.fillStyle = K.orange; g.fillRect(W * e - 3, 0, 6, H); g.restore(); }
      else { g.save(); g.globalAlpha = e; g.drawImage(off, 0, 0); g.restore(); } LL.tlog = keep; }
    else one(g, s, t);
    if (V && s.tpl !== 'endcard') hook(g, t); } };
})();
function frameAt(g, t) { g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.setTransform(1, 0, 0, 1, 0, 0); g.filter = 'none'; LL.SEG.frame(g, t); g.globalAlpha = 1; g.setTransform(1, 0, 0, 1, 0, 0);
  const S2 = LL.SEG, fi = S2.fadeIn === undefined || S2.fadeIn === null ? 6 : S2.fadeIn, fo = S2.fadeOut === undefined || S2.fadeOut === null ? 6 : S2.fadeOut, fr = t * FPS, N = S2.frames; let k = 0;
  if (fi > 0 && fr < fi) k = Math.max(k, 1 - sm((fr + 1) / (fi + 1))); if (fo > 0 && fr > N - 1 - fo) k = Math.max(k, sm((fr - (N - 1 - fo)) / (fo + 1))); if (k > 0) { g.fillStyle = `rgba(3,4,8,${k})`; g.fillRect(0, 0, W, H); } }
window.drawFrame = (f) => { LL.act = false; LL.fill = false; LL.camNear = Infinity; LL.zones = []; LL.hit = 0; frameAt(X, f / FPS); };

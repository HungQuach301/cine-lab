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
// mép dưới của dòng nguồn / nhãn ACTUAL (chủ dự án 13/10/2026: mọi chữ cách mép ≥ 48 px, kiểm bằng scripts/k2/edge_check.py)
const EDGE_B = 62;
const SRCPX = V ? 46 : 38;   // dòng nguồn kênh 2: chỉ tên nguồn ngắn, ≥ 38 px ở 16:9 (Kinh thánh §4, duyệt 14/10 20:45; V2b 34 px; trước đó MINPX 30)
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
    LL.tlog.push({ s: s.slice(0, 40), role: o.role, color, alpha: +g.globalAlpha.toFixed(2), cap: +(cap * effScale(g)).toFixed(1), box: [Math.min(...P.map((q) => q[0])), Math.min(...P.map((q) => q[1])), Math.max(...P.map((q) => q[0])), Math.max(...P.map((q) => q[1]))].map(Math.round) }); }
  g.restore(); return wd; }
function wrap(g, s, maxW, px, w = 600, disp = false) { g.save(); g.font = font(fitPx(g, px), w, disp); const out = []; let a = ''; for (const wd of String(s).split(' ')) { const n = a ? a + ' ' + wd : wd; if (g.measureText(n).width > maxW && a) { out.push(a); a = wd; } else a = n; } out.push(a); g.restore(); return out; }
function para(g, s, x, y, maxW, px, color, o = {}) { const L = wrap(g, s, maxW, px, o.w, o.disp), lh = o.lh || px * 1.28; L.forEach((l, i) => text(g, l, x, y + i * lh, px, color, o)); return y + (L.length - 1) * lh; }
function rrect(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function panel(g, x, y, w, h, o = {}) { const a = o.a === undefined ? 1 : o.a; if (a <= 0.01) return; g.save(); g.globalAlpha *= a; g.shadowColor = 'rgba(0,0,0,0.45)'; g.shadowBlur = 30; g.shadowOffsetY = 10;
  rrect(g, x, y, w, h, o.r || 10); g.fillStyle = o.fill || 'rgba(15,23,34,0.86)'; g.fill(); g.shadowColor = 'transparent';
  g.strokeStyle = o.stroke || 'rgba(154,167,181,0.35)'; g.lineWidth = 1.5; if (o.dash) g.setLineDash([12, 8]); g.stroke(); g.setLineDash([]);
  if (o.accent) { g.fillStyle = o.accent; g.fillRect(x, y + 8, 6, h - 16); } g.restore(); }
// nhãn loại số: ACTUAL viền liền; PROJECTION nét đứt hổ phách
const KINDLBL = (k) => ({ projection: 'PROJECTION', estimate: 'ESTIMATE' })[k] || 'ACTUAL';
function kindTag(g, kind, x, y, a = 1, align = 'left') { if (a <= 0.01 || !kind) return 0; const pj = kind === 'projection' || kind === 'estimate', s = KINDLBL(kind), px = 26 * S;   /* T2: 'estimate' → ESTIMATE (trước đây mọi loại khác projection in ACTUAL — sai nhãn) */
  const p = Math.max(px, MINPX * 0.9), wd = tw(g, s, p, 700) + p * 0.9, h = p * 1.5, x0 = align === 'right' ? x - wd : align === 'center' ? x - wd / 2 : x;
  g.save(); g.globalAlpha *= a; g.fillStyle = 'rgba(12,18,27,0.88)'; g.fillRect(x0, y - h / 2, wd, h);   /* SS4 Q5 (17/10): nền tối đặc — nhãn từng chỉ có viền, đè nền sáng (sa mạc, Short S1 khung 300) tương phản 2,17 */
  g.strokeStyle = pj ? K.amber : K.steel; g.lineWidth = 2.4; if (pj) g.setLineDash([9, 6]); g.strokeRect(x0, y - h / 2, wd, h); g.restore();
  text(g, s, x0 + p * 0.45, y + 1, p, pj ? K.amber : K.dim, { a, w: 700, base: 'middle' }); return wd; }
function srcLine(g, s, x, y, a = 1, align = 'left', mw0) { if (!s || !String(s).trim()) return; const mw = mw0 || (V ? W - 2 * 70 : 1500), SP = SRCPX;
  const SC = '#D6DDE4';   /* V2 14/10: K.dim → sáng hơn (3 người chấm mù: dòng nguồn xám, nhỏ, khó đọc trên điện thoại) */
  if (tw(g, s, SP, 500) <= mw) { text(g, s, x, y, SP, SC, { a, w: 500, align, maxW: mw }); return; }
  const L = wrap(g, s, mw, SP, 500); L.forEach((l, i) => text(g, l, x, y - (L.length - 1 - i) * SP * 1.25, SP, SC, { a, w: 500, align, maxW: mw })); }   // nguồn dài: xuống dòng, không tràn (Q22)

// ---------- cảnh 3D nền ----------
LL.camNear = Infinity;
function plateX(p, t) { return Math.max(0, (t - p.t0) * FPS * (p.speed || 1)) + (p.off || 0); }
function plateIdx(p, t) { return Math.max(0, Math.min((p.n || 1) - 1, Math.floor(plateX(p, t) + 1e-6))); }
function drawPlate(g, p, t, blur = 0, dim = 0) { const x = plateX(p, t), i0 = plateIdx(p, t), i1 = Math.min((p.n || 1) - 1, i0 + 1), fr = (p.speed || 1) < 1 ? x - Math.floor(x + 1e-6) : 0;
  const im = window.PLATES[p.dir + '#' + i0], im1 = window.PLATES[p.dir + '#' + i1];
  if (!im) { g.fillStyle = K.ink; g.fillRect(0, 0, W, H); text(g, 'missing plate', 60, 80, 30, '#f55', { deco: true }); return; }
  // khung 3D có thể 960×540 (nháp) hoặc 1920×1080; 9:16 lấy đúng khổ. Nền chậm: hoà khung i0 → i1 theo phần lẻ (không giữ khung)
  g.save(); if (blur > 0) g.filter = `blur(${Math.round(blur)}px)`; const sc = blur > 0 ? 1.04 : 1, dw = (q) => g.drawImage(q, -(sc - 1) * W / 2, -(sc - 1) * H / 2, W * sc, H * sc);
  dw(im); if (fr > 0.01 && im1 && i1 !== i0) { g.globalAlpha = fr; dw(im1); g.globalAlpha = 1; } g.filter = 'none'; g.restore();
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
// nhãn module k2v (design/k2v: map, chart3d, photo) bám điểm neo, không đường dẫn dài: {a, s, sub, at, out, side: 'right'|'left'|'up'|'down', gap, c (màu nhấn), big (số lớn), kind}
//   địa danh (p.places) và số liệu (p.tags) dùng chung; neo bị che (mặt sau địa cầu, ngoài khung) → không vẽ. Cỡ chữ ≥ MINPX (30 px ở 16:9).
function tags(g, p, t, list) { for (const L of list || []) { const u = vis(t, L.at, L.out); if (u <= 0.01) continue; const A = anc(p, t, L.a); if (!A || !A.v) continue;
  const big = !!L.big, px = (L.px || (big ? 54 : 36)) * S, spx = (L.spx || 32) * S, w1 = tw(g, L.s, px, 700, big), w2 = L.sub ? tw(g, L.sub, spx, 500) : 0, kw = L.kind ? tw(g, KINDLBL(L.kind), MINPX * 0.9, 700) + MINPX * 1.4 : 0;
  const bw = Math.max(w1 + kw, w2) + 46, bh = (L.sub ? px * 1.2 + spx * 1.35 : px * 1.2) + 26, gap = (L.gap === undefined ? 30 : L.gap) * S, side = L.side || 'right', c = L.c || K.orange;
  const yMax = (p.src || p.cap) ? (V ? SAFE.y1 - 150 * S : Math.min(SAFE.y1 - 150 * S, H * 0.735 + 10)) : SAFE.y1;   // không đè dải chú thích/dòng nguồn (13/10: 16:9 chặn ở đỉnh câu chú thích, nhãn 317 từng đè câu ở ch_mpls)
  // side 'auto': khi neo nằm trong hộp một vật (chồng xu, sticker), khoảng cách tính từ MÉP hộp đó, không từ tâm neo
  const own = side === 'auto' ? (LL.occ || []).find((o) => A.x >= o[0] - 2 && A.x <= o[2] + 2 && A.y >= o[1] - 12 && A.y <= o[3] + 2) : null;
  const boxOf = (sd) => { let x = sd === 'right' ? (own ? own[2] + 18 : A.x + gap) : sd === 'left' ? (own ? own[0] - 18 : A.x - gap) - bw : A.x - bw / 2, y = sd === 'up' ? (own ? Math.min(own[1], A.y) - 18 : A.y - gap) - bh : sd === 'down' ? (own ? own[3] + 18 : A.y + gap) : A.y - bh / 2;
    return [Math.max(SAFE.x0, Math.min(SAFE.x1 - bw, x)), Math.max(SAFE.y0, Math.min(yMax - bh, y))]; };
  // V2 (BAI-HOC-K2 K11): side 'auto' = hướng đầu tiên trong up/right/left/down không chạm hộp sticker/nhãn đã vẽ ở khung này (LL.occ); giữ hướng đã chọn để nhãn không nhảy
  let side2 = side; if (side === 'auto') { const occ = LL.occ || [];
    const hit2 = ([x, y]) => occ.reduce((m, o) => m + Math.max(0, Math.min(x + bw, o[2]) - Math.max(x, o[0])) * Math.max(0, Math.min(y + bh, o[3]) - Math.max(y, o[1])), 0);   /* tính cả hộp của chính vật: hướng bị kẹp vào lề an toàn có thể trượt đè lên vật (nháp V2, nhãn 1/10) */
    const cand = (L.prefer || ['up', 'right', 'left', 'down']); if (!L._side || hit2(boxOf(L._side)) > 0) { let best = null; for (const sd of cand) { const h2 = hit2(boxOf(sd)); if (!best || h2 < best[1]) best = [sd, h2]; if (!h2) break; } L._side = best[0]; } side2 = L._side; }
  let [bx, by] = boxOf(side2); (LL.occ = LL.occ || []).push([bx, by, bx + bw, by + bh]);
  if (gap > 6 * S) { const ex = Math.max(bx, Math.min(bx + bw, A.x)), ey = Math.max(by, Math.min(by + bh, A.y)); g.save(); g.globalAlpha *= u; g.strokeStyle = c; g.lineWidth = 2.5; g.beginPath(); g.moveTo(A.x, A.y); g.lineTo(ex, ey); g.stroke();
    if (!L.nodot) { g.fillStyle = c; g.beginPath(); g.arc(A.x, A.y, 5.5, 0, 7); g.fill(); } g.restore(); }
  panel(g, bx, by, bw, bh, { a: u, accent: c, dash: L.kind === 'projection', fill: 'rgba(12,18,27,0.93)' });   /* nền đặc hơn thẻ: nhãn nằm trên cảnh 3D sáng/tối bất kỳ (chấm mù P2: chữ phụ mờ) */
  text(g, L.s, bx + 24, by + 13 + px * 0.92, px, big ? (L.kind === 'projection' ? K.amber : c) : K.text, { a: u, w: 700, disp: big });
  if (L.kind) kindTag(g, L.kind, bx + 24 + w1 + MINPX * 0.7, by + 13 + px * 0.6, u);
  if (L.sub) text(g, L.sub, bx + 24, by + 13 + px * 1.2 + spx * 0.98, spx, L.subc || '#E6EBF0', { a: u, w: 500 }); LL.fill = true; } }
// dải chú thích dưới: {s, at, big (số lớn), kind, src}; hiện mục mới nhất
function caps(g, p, t) { const Cs = p.cap || []; let k = -1; Cs.forEach((c, i) => { if (t >= c.at) k = i; }); if (k < 0 && !p.src) return;
  const c = k >= 0 ? Cs[k] : null, a = c ? rv(t, c.at, 0.45) : 0, src0 = (c && c.src) || p.src, srcS = p.credit ? (src0 && String(src0).trim() ? src0 + ' · ' + p.credit : p.credit) : src0;   // credit (3D illustration / our calculation) nối cuối dòng nguồn: không đè nhãn ACTUAL góc phải
  // 13/10 (nháp K2C-T1-06): số lớn + câu 2 dòng + dòng nguồn 2 dòng đè nhau → đẩy cả khối chữ lên cho dòng cuối cách đỉnh dòng nguồn ≥ 18 px
  const lh0 = V ? 66 : 54, px0 = V ? 54 : 44, smw = V ? W - 2 * 70 : 1500, nL = c ? Math.min(3, wrap(g, c.s || '', V ? W - 140 : 1500, px0, 600).length) : 0;
  const nS = srcS && String(srcS).trim() ? (tw(g, srcS, SRCPX, 500) <= smw ? 1 : wrap(g, srcS, smw, SRCPX, 500).length) : 0;
  const srcTop = H - (V ? 260 : EDGE_B) - (nS ? (nS - 1) * SRCPX * 1.25 + SRCPX : 0);
  const last0 = (V ? H * 0.70 : H * 0.735) + (V ? 60 : 50) + (c && c.big ? (V ? 170 : 105) : 0) + 10 + Math.max(0, nL - 1) * lh0;
  const y0 = (V ? H * 0.70 : H * 0.735) - Math.max(0, last0 - (srcTop - 18));
  const x = V ? W / 2 : SAFE.x0, al = V ? 'center' : 'left', mw = V ? W - 140 : 1500;
  if (!V && (p.photo || p.clip)) {   /* SS1-T4 (chủ dự án 17/10): ảnh in/khung footage — không phủ dải tối cả bề ngang (chấm mù P4/P6/P7: dải đè mép ảnh); chỉ một tấm nền sau đúng dòng chữ */
    /* TT1-U3 (chủ dự án 17/10; chấm mù P6 lần 4: "big empty gap between its two lines"): HAI tấm gọn — sau câu chú thích và sau dòng nguồn — không chừa khoảng trống giữa */
    const lw = c && c.s ? wrap(g, c.s, mw, 44, 600).slice(0, 3).map((l) => tw(g, l, 44, 600)) : [], sw = srcS && String(srcS).trim() ? Math.min(smw, tw(g, srcS, SRCPX, 500)) : 0;
    if (lw.length && a > 0.01) { const bw = Math.max(...lw) + 56, top = y0 + 60 - 44 - 16, bot = y0 + 60 + (lw.length - 1) * lh0 + 18;
      panel(g, x - 28, top, bw, bot - top, { a, fill: 'rgba(8,12,18,0.84)', r: 14 }); (LL.occ = LL.occ || []).push([x - 28, top, x - 28 + bw, bot]); }
    if (sw) { const top = srcTop - SRCPX * 0.1 - 14, bot = H - EDGE_B + SRCPX * 0.32 + 14;
      panel(g, x - 28, top, sw + 56, bot - top, { a: Math.max(a, 0.85), fill: 'rgba(8,12,18,0.84)', r: 12 }); (LL.occ = LL.occ || []).push([x - 28, top, x + 28 + sw, bot]); } }
  else { const gr = g.createLinearGradient(0, y0 - (V ? 160 : 80), 0, H); gr.addColorStop(0, 'rgba(8,12,18,0)'); gr.addColorStop(0.35, `rgba(8,12,18,${0.78 * Math.max(a, srcS ? 0.85 : 0)})`); gr.addColorStop(1, `rgba(8,12,18,${0.9 * Math.max(a, srcS ? 0.85 : 0)})`);
    g.fillStyle = gr; g.fillRect(0, y0 - (V ? 160 : 80), W, H - y0 + 160); }
  if (c) { let y = y0 + (V ? 60 : 50); if (c.big) { text(g, c.big, x, y + (V ? 70 : 60), (V ? 110 : 96), c.kind === 'projection' ? K.amber : K.orange, { a, w: 700, disp: true, align: al }); if (c.kind) kindTag(g, c.kind, V ? W / 2 : x + tw(g, c.big, 96, 700, true) + 30, y + (V ? 130 : 30), a, V ? 'center' : 'left'); y += V ? 170 : 105; }
    const L = wrap(g, c.s || '', mw, (V ? 54 : 44), 600); L.slice(0, 3).forEach((l, i) => text(g, l, x, y + 10 + i * (V ? 66 : 54), (V ? 54 : 44), K.text, { a, w: 600, align: al })); }
  if (srcS) srcLine(g, srcS, x, H - (V ? 260 : EDGE_B), 1, al); }
// tựa lớn: {t, sub, at, out, kicker}
function title(g, p, t) { const T = p.title; if (!T) return; const u = vis(t, T.at === undefined ? 0 : T.at, T.out, 0.7); if (u <= 0.01) return;
  const cx = W / 2, cy = V ? H * 0.42 : H * 0.44; const gr = g.createRadialGradient(cx, cy, 50, cx, cy, W * 0.6); gr.addColorStop(0, `rgba(8,12,18,${0.62 * u})`); gr.addColorStop(1, 'rgba(8,12,18,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  if (T.kicker) text(g, T.kicker, cx, cy - (V ? 150 : 120), (V ? 46 : 38), K.orange, { a: u, w: 700, align: 'center' });
  text(g, T.t, cx, cy, (V ? 120 : 132) * (T.scale || 1), K.text, { a: u, w: 700, disp: true, align: 'center', maxW: W - 200 });
  g.save(); g.globalAlpha *= u; g.fillStyle = K.orange; g.fillRect(cx - 60, cy + 34, 120 * eo((t - (T.at || 0)) / 0.8), 6); g.restore();
  if (T.sub) para(g, T.sub, cx, cy + (V ? 130 : 110), V ? W - 160 : 1400, (V ? 50 : 44), K.dim, { a: u, w: 500, align: 'center' }); }
// V2b: cột chú thích bên phải (chân dung lệch trái, D4): p.side = {at, x0 (phần khung, mặc định 0.62), lines: [{s, px, c, w, disp, at, gap}]}; căn giữa theo chiều dọc
function sideCap(g, p, t) { const Sd = p.side; if (!Sd) return; const x = W * (Sd.x0 ?? 0.62), mw = SAFE.x1 - x; const L = [];
  for (const l of Sd.lines) { const px = (l.px || 40) * S, rows = wrap(g, l.s, mw, px, l.w || 600, !!l.disp); L.push({ l, px, rows, h: rows.length * px * 1.22 + (l.gap ?? 18) }); }
  let y = H / 2 - L.reduce((a, e) => a + e.h, 0) / 2; const u0 = vis(t, Sd.at === undefined ? p.t0 : Sd.at, Sd.out, 0.5);
  if (u0 > 0.01) { const gr = g.createLinearGradient(x - 80, 0, W, 0); gr.addColorStop(0, 'rgba(8,10,14,0)'); gr.addColorStop(0.25, `rgba(8,10,14,${0.55 * u0})`); gr.addColorStop(1, `rgba(8,10,14,${0.7 * u0})`); g.fillStyle = gr; g.fillRect(x - 80, 0, W - x + 80, H); }
  for (const e of L) { const a = vis(t, e.l.at === undefined ? Sd.at : e.l.at, Sd.out, 0.5); e.rows.forEach((r, i) => text(g, r, x, y + e.px * (0.95 + i * 1.22), e.px, e.l.c || K.text, { a, w: e.l.w || 600, disp: !!e.l.disp })); y += e.h; }
  if (u0 > 0.01) { g.save(); g.globalAlpha *= u0; g.fillStyle = Sd.accent || K.amber; g.fillRect(x - 28, H / 2 - L.reduce((a, e) => a + e.h, 0) / 2, 5, L.reduce((a, e) => a + e.h, 0) - 18); g.restore(); } LL.fill = true; }
// V2: chip năm lớn (mốc thời gian của bản đồ quá khứ): p.year = {s, at, out, c}; góc trên trái, chữ display 64 px
function yearChip(g, p, t) { const Y = p.year; if (!Y) return; const u = vis(t, Y.at === undefined ? p.t0 : Y.at, Y.out, 0.5); if (u <= 0.01) return;
  const px = 64 * S, w = tw(g, Y.s, px, 700, true) + 56, h = px * 1.45, x = SAFE.x0, y = V ? 210 : 62, sc = backOut(cl((t - (Y.at || 0)) / 0.45));
  g.save(); g.translate(x + w / 2, y + h / 2); g.scale(sc, sc); g.translate(-(x + w / 2), -(y + h / 2)); panel(g, x, y, w, h, { a: u, fill: 'rgba(12,18,27,0.92)', stroke: Y.c || K.amber, r: 12 });
  text(g, Y.s, x + w / 2, y + h / 2 + px * 0.36, px, Y.c || K.amber, { a: u, w: 700, disp: true, align: 'center', role: 'year' }); g.restore(); (LL.occ = LL.occ || []).push([x, y, x + w, y + h]); }
// chip nơi dựng (SS1-T3, chủ dự án 17/10; chấm mù: "the place is never named"): p.where = 'tên' | {s, at, out}; góc trên phải, dưới nhãn "Facts as of" nếu có
function whereChip(g, p, t) { const Wh = p.where; if (!Wh || V) return; const o = typeof Wh === 'string' ? { s: Wh } : Wh; const u = vis(t, o.at === undefined ? p.t0 : o.at, o.out, 0.5); if (u <= 0.01) return;
  const px = 30 * S, ic = px * 0.9, wd = tw(g, o.s, px, 600) + 40 + ic + 12, h = px * 1.7, x = W - SAFE.x0 - wd, y = (p.asof ? (p.asofY !== undefined ? p.asofY : (p.card ? 28 : 56)) + px * 1.7 + 12 : 56);
  panel(g, x, y, wd, h, { a: u, fill: 'rgba(12,18,27,0.9)', stroke: 'rgba(230,235,240,0.35)' });
  g.save(); g.globalAlpha *= u; const cx = x + 20 + ic / 2, cy = y + h / 2 - ic * 0.12; g.fillStyle = K.orange; g.beginPath(); g.arc(cx, cy - ic * 0.12, ic * 0.34, Math.PI, 0); g.lineTo(cx, cy + ic * 0.46); g.closePath(); g.fill();
  g.fillStyle = 'rgba(12,18,27,1)'; g.beginPath(); g.arc(cx, cy - ic * 0.12, ic * 0.13, 0, 7); g.fill(); g.restore();
  text(g, o.s, x + 20 + ic + 12, y + px * 1.18, px, K.text, { a: u, w: 600, role: 'where' }); (LL.occ = LL.occ || []).push([x, y, x + wd, y + h]); }
function asof(g, p, t) { if (!p.asof) return; const u = vis(t, p.asofAt === undefined ? p.t0 : p.asofAt); const s = p.asof === true ? 'Facts as of 11 Oct 2026' : p.asof;
  const px = 30 * S, wd = tw(g, s, px, 600) + 40, x = W - SAFE.x0 - wd, y = p.asofY !== undefined ? p.asofY : V ? 210 : (p.card ? 28 : 56);   /* asofY: Short có hook 2 dòng đặt nhãn dưới dải hook */ panel(g, x, y, wd, px * 1.7, { a: u, stroke: 'rgba(242,193,78,0.6)' }); text(g, s, x + 20, y + px * 1.18, px, K.amber, { a: u, w: 600 }); }

// ---------- XƯƠNG SỐNG THỜI GIAN (V5b-2b, V5B2A §8.5): lớp chữ của cảnh 'tl/<cảnh>' ----------
// Trang tl (design/k2v/tl/page.js) ghi lớp chữ từng khung vào anchors.json[f]._tl (record.js: cùng API text.js); ở đây vẽ lại bằng chữ + bảng màu kênh:
//  bộ đếm năm / ngày-giờ dưới-trái (phóng 1,45× + viền hổ phách khi MỐC ĐINH), dòng lịch thứ hai (O.S./N.S.), chỉ số "≈" trên-phải + dòng nguồn (role index_src),
//  dòng phương pháp (HH3, role method), thẻ ≤ 1 (neo điểm 3D có đường dẫn, hoặc dải dưới), nhãn neo (tag), nhãn nguồn ghost dưới-phải (role ghost_src, ≥ 38 px),
//  chip nơi (p.where thắng; không khai → chip của cảnh). Bật bằng p.tl = true (prep.py tự đặt cho cảnh tl/…). Cỡ chữ ≥ 30 px, nguồn ≥ 38 px (SRCPX).
function tlData(p, t) { const A = window.ANC[p.dir]; if (!A) return null; const fr = A[plateIdx(p, t)] || A[String(plateIdx(p, t))]; return fr && fr._tl ? fr._tl : null; }
function tlLayer(g, p, t) { if (!p.tl) return; const D = tlData(p, t); if (!D) return; const Ch = D.chrome || {};
  const pin = Ch.pin || 0, zs = 1 + 0.45 * pin, ys = Ch.clock ? Ch.clock.s : (Ch.year != null ? String(Math.floor(Ch.year)) : null); let ybR = SAFE.x0, ybT = H - EDGE_B;
  if (ys) { const px = (Ch.clock ? 56 : 72) * S * zs, w = tw(g, ys, px, 700, true) + 52 * zs, h = px * 1.42, x = SAFE.x0, y = H - EDGE_B - h + 8;
    panel(g, x, y, w, h, { a: 1, fill: 'rgba(12,18,27,0.9)', stroke: pin > 0.01 ? `rgba(242,193,78,${0.4 + 0.6 * pin})` : 'rgba(230,235,240,0.30)', r: 12 });
    text(g, ys, x + 26 * zs, y + h / 2 + px * 0.36, px, pin > 0.5 ? K.amber : K.text, { w: 700, disp: true, role: Ch.clock ? 'clock' : 'year' }); ybR = x + w; ybT = y;
    (LL.occ = LL.occ || []).push([x, y, x + w, y + h]);
    if (Ch.clock && Ch.clock.sub) { const sp = 32 * S, sw = tw(g, Ch.clock.sub, sp, 600) + 40, sy = y - sp * 1.7 - 10; panel(g, x, sy, sw, sp * 1.7, { fill: 'rgba(12,18,27,0.88)' }); text(g, Ch.clock.sub, x + 20, sy + sp * 1.18, sp, K.dim, { w: 600, role: 'calendar' }); ybT = sy; } }
  // trên-phải: chip nơi rồi chỉ số + dòng nguồn
  let yR = 56; const wh = p.where || (D.where ? { s: D.where.s } : null);
  if (wh) { whereChip(g, Object.assign({}, p, { where: wh }), t); yR += 30 * S * 1.7 + 12; }
  if (Ch.idx) { const px = 48 * S, w = tw(g, Ch.idx, px, 700, true) + 48, h = px * 1.45, x = W - SAFE.x0 - w; panel(g, x, yR, w, h, { fill: 'rgba(12,18,27,0.9)' }); text(g, Ch.idx, x + 24, yR + h / 2 + px * 0.36, px, K.text, { w: 700, disp: true, role: 'index' }); yR += h + 10;
    if (Ch.idxSrc) { const sw = tw(g, Ch.idxSrc.s, SRCPX, 500) + 40, x2 = W - SAFE.x0 - sw; panel(g, x2, yR, sw, SRCPX * 1.6, { a: Ch.idxSrc.a, fill: 'rgba(12,18,27,0.88)' }); text(g, Ch.idxSrc.s, x2 + 20, yR + SRCPX * 1.12, SRCPX, '#D6DDE4', { a: Ch.idxSrc.a, w: 500, role: 'index_src' }); yR += SRCPX * 1.6 + 10; } }
  // dòng phương pháp: đầu phim trên-trái; màn kết dưới, bên phải hộp năm
  if (Ch.method) { let yy = Ch.method.bottom ? H - EDGE_B - SRCPX * 1.6 : 56; for (const m of Ch.method.lines) { const w = tw(g, m.s, SRCPX, 600) + 40, x = Ch.method.bottom ? ybR + 20 : SAFE.x0;
    panel(g, x, yy, w, SRCPX * 1.6, { a: m.a, fill: 'rgba(12,18,27,0.88)' }); text(g, m.s, x + 20, yy + SRCPX * 1.12, SRCPX, K.text, { a: m.a, w: 600, role: 'method' }); yy += (Ch.method.bottom ? -1 : 1) * (SRCPX * 1.6 + 10); } }
  // nguồn ghost: dưới-phải
  let gw = 0; if (D.ghost_src) { const s2 = D.ghost_src.s, sw = Math.min(W * 0.64, tw(g, s2, SRCPX, 500)) + 40,   /* nhãn nguồn ghost GIỮ ≥ 38 px (NC-H5b): bề ngang tới 64 % khung, không thu chữ */ x = W - SAFE.x0 - sw, y = H - EDGE_B - SRCPX * 1.6 + 8; gw = sw + 20;
    panel(g, x, y, sw, SRCPX * 1.6, { a: D.ghost_src.a, fill: 'rgba(12,18,27,0.9)', stroke: 'rgba(242,193,78,0.45)' }); text(g, s2, x + 20, y + SRCPX * 1.12, SRCPX, '#E6EBF0', { a: D.ghost_src.a, w: 500, role: 'ghost_src', maxW: W * 0.64 }); (LL.occ = LL.occ || []).push([x, y, x + sw, y + SRCPX * 1.6]); }
  // thẻ: neo (đường dẫn hổ phách) hoặc dải dưới bên phải hộp năm
  for (const c of D.cards || []) { const tp = 44 * S, w1 = tw(g, c.title, tp, 700, true), w2 = c.src ? tw(g, c.src, SRCPX, 500) : 0, bw = Math.min(W - 2 * SAFE.x0, Math.max(w1, w2) + 56), bh = tp * 1.3 + (c.src ? SRCPX * 1.35 : 0) + 30;
    // neo trong khung: thẻ ở dải TRÊN (dưới chip nơi), đường dẫn xuống điểm neo — không đè vật chính quanh điểm neo (tự rà V5b-2b-T: thẻ từng đè mặt bastion)
    const inF = c.anchor && c.anchor[0] >= 0.02 && c.anchor[0] <= 0.98 && c.anchor[1] >= 0.04 && c.anchor[1] <= 0.96;
    let bx, by; if (inF) { const ax = c.anchor[0] * W, ay = c.anchor[1] * H; bx = Math.max(SAFE.x0, Math.min(SAFE.x1 - bw, ax - bw / 2)); by = Math.max(SAFE.y0 + 90, Math.min(yR + 12, ay - 90 - bh));
      g.save(); g.globalAlpha *= c.a; g.strokeStyle = K.amber; g.lineWidth = 3; g.beginPath(); g.moveTo(Math.max(bx, Math.min(bx + bw, ax)), by + bh); g.lineTo(ax, ay); g.stroke(); g.fillStyle = K.amber; g.beginPath(); g.arc(ax, ay, 7, 0, 7); g.fill(); g.restore(); }
    else { bx = ybR + 24; by = H - EDGE_B - bh + 8; if (bx + bw > W - SAFE.x0 - gw) { bx = SAFE.x0; by = ybT - 16 - bh; } }   /* không neo / neo ngoài khung: dải dưới; không đủ chỗ cạnh nhãn ghost → hàng trên hộp năm (không bao giờ ra ngoài mép) */
    panel(g, bx, by, bw, bh, { a: c.a, accent: K.amber, fill: 'rgba(12,18,27,0.92)' }); text(g, c.title, bx + 28, by + 14 + tp, tp, K.text, { a: c.a, w: 700, disp: true, role: 'card', maxW: bw - 48 });
    if (c.src) text(g, c.src, bx + 28, by + 14 + tp * 1.3 + SRCPX * 1.05, SRCPX, '#D6DDE4', { a: c.a, w: 500, role: 'src', maxW: bw - 48 }); (LL.occ = LL.occ || []).push([bx, by, bx + bw, by + bh]); LL.fill = true; }
  // nhãn neo nhỏ (ghost/địa danh): quầng tối, đường dẫn trắng
  for (const L of D.tags || []) { if (!L.anchor) continue; const ax = L.anchor[0] * W, ay = L.anchor[1] * H, px = 34 * S, w = tw(g, L.s, px, 600) + 36, h = px * 1.6, x = Math.max(SAFE.x0, Math.min(SAFE.x1 - w, ax - w / 2)), y = Math.max(SAFE.y0, ay - 70 - h);
    g.save(); g.globalAlpha *= L.a; g.strokeStyle = 'rgba(238,241,244,0.9)'; g.lineWidth = 2.5; g.beginPath(); g.moveTo(ax, ay); g.lineTo(Math.max(x, Math.min(x + w, ax)), y + h); g.stroke(); g.fillStyle = K.text; g.beginPath(); g.arc(ax, ay, 5.5, 0, 7); g.fill(); g.restore();
    panel(g, x, y, w, h, { a: L.a, fill: 'rgba(12,18,27,0.9)' }); text(g, L.s, x + 18, y + h / 2 + px * 0.36, px, K.text, { a: L.a, w: 600, role: 'tag' }); (LL.occ = LL.occ || []).push([x, y, x + w, y + h]); }
  LL.fill = true; }

// ---------- STICKER + BẢNG ĐIỂM (phiên V2, 14/10/2026; scripts/k2/lib/sticker.js) ----------
// p.stickers: [{a: 'st:<id>' | 'col:<id>' | địa danh, img: 'stk:<tên thư viện>' | 'role:<vai>' | {role, hat, hand}, at, out, px (cao, px @1080p),
//   pop (bật nảy khi vào, mặc định true), walk (nhún khi đi theo tuyến), bob (lắc nhẹ khi đứng), flip: 'auto' | true, dx, dy}]
const backOut = (u) => { u = cl(u); const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2); };
function stickers(g, p, t) { if (!p.stickers || !window.STK) return;
  const list = p.stickers.map((S, i) => ({ S, i, A: anc(p, t, S.a) })).filter((e) => e.A && e.A.v).sort((a, b) => a.A.y - b.A.y);   // xa trước, gần sau
  for (const { S, A } of list) { const at = S.at === undefined ? p.t0 : S.at, u0 = cl((t - at) / 0.42); if (u0 <= 0) continue;
    const uo = S.out === undefined ? 0 : cl((t - S.out) / 0.3); if (uo >= 1) continue;
    const px = (S.px || 120) * S_, im = STK.get(S.img, px); if (!im) continue; rv(t, at, 0.42);
    let sc = (S.pop === false ? eo(u0) : backOut(u0)) * (1 - eo(uo)), rot = 0, hop = 0;
    if (S.walk) { const ph = (t - at) * (S.hz || 2.4) * Math.PI; hop = Math.abs(Math.sin(ph)) * px * 0.07; rot = Math.sin(ph) * 0.05; }
    else if (S.bob !== false) { rot = Math.sin((t - at) * 1.7 + (S.ph || 0)) * 0.025; }
    let flip = S.flip === true; if (S.flip === 'auto' || (S.walk && S.flip === undefined)) { const B = anc(p, t + 2 / FPS, S.a), Bp = anc(p, t - 2 / FPS, S.a); if (B && Bp && Math.abs(B.x - Bp.x) > 0.4) flip = B.x < Bp.x; else flip = !!S.lastFlip; S.lastFlip = flip; if (S.face === 'left') flip = !flip; }
    const h = px, w = h * im.width / im.height;
    if (S.ground !== false) { const gx = A.x + (S.dx || 0) * S_, gy = A.y + (S.dy || 0) * S_, rw = w * 0.36 * sc * (1 - 0.25 * hop / (px * 0.07 + 1e-6) * 0.5), gr = g.createRadialGradient(gx, gy, 0, gx, gy, rw);   /* bóng tiếp đất: sticker "đứng" trên bản đồ (chấm mù V2: "dán lên") */
      gr.addColorStop(0, `rgba(20,16,10,${0.34 * sc})`); gr.addColorStop(1, 'rgba(20,16,10,0)'); g.save(); g.translate(gx, gy); g.scale(1, 0.32); g.translate(-gx, -gy); g.fillStyle = gr; g.beginPath(); g.arc(gx, gy, rw, 0, 7); g.fill(); g.restore(); }
    g.save(); g.translate(A.x + (S.dx || 0) * S_, A.y + (S.dy || 0) * S_ - hop); g.rotate(rot); g.scale(sc * (flip ? -1 : 1), sc);
    g.drawImage(im, -w / 2, -h * 0.94, w, h); g.restore(); (LL.occ = LL.occ || []).push([A.x - w / 2 * sc, A.y - h * sc, A.x + w / 2 * sc, A.y]); LL.fill = true; } }
const S_ = S;
// V2: hộp chiếu của chồng xu/cột bản đồ (neo col/colL/colR của relief) vào LL.occ → nhãn side:'auto' không đè vật thể (BAI-HOC-K2 K11)
function colOcc(p, t) { const A = window.ANC[p.dir]; if (!A) return; const fr = A[plateIdx(p, t)] || A[String(plateIdx(p, t))]; if (!fr) return;
  for (const k of Object.keys(fr)) { const pre = k.startsWith('col:') ? 'col' : k.startsWith('obj:') ? 'obj' : null; if (!pre) continue; const id = k.slice(4), T = anc(p, t, k), L = anc(p, t, pre + 'L:' + id), R = anc(p, t, pre + 'R:' + id); if (!T || !L || !R || !L.v || !T.v) continue;   /* V2b: cả vật/nhân vật dựng trong cảnh (obj:) */
    (LL.occ = LL.occ || []).push([Math.min(L.x, R.x) - 6, T.y - 10, Math.max(L.x, R.x) + 6, Math.max(L.y, R.y) + 10]); } }

// p.score: biểu tượng góc + bảng tổng kết hai phía (component dùng lại)
//   corner: {at, out, sides: [{s, c, icon, n}]}               huy hiệu góc trên trái: biểu tượng + tên + điểm (n: số hoặc [{t, v}] tăng theo mốc)
//   board:  {at, out, title, sides: [{s, c, icon}], rows: [{k, icon, v: [trái, phải], win: 0|1, at, sub}], foot}
function iconImg(spec, px) { return window.STK ? STK.get(spec, px) : null; }
function drawIcon(g, spec, cx, cy, px, a = 1) { const im = iconImg(spec, px); if (!im) return; let h = px, w = h * im.width / im.height; if (w > px * 1.15) { w = px * 1.15; h = w * im.height / im.width; }   /* sticker rộng (thuyền, xe) co theo ô, không đè chữ */ g.save(); g.globalAlpha *= a; g.drawImage(im, cx - w / 2, cy - h / 2, w, h); g.restore(); }
function score(g, p, t) { const Sc = p.score; if (!Sc) return;
  const Cn = Sc.corner; if (Cn) { const u = vis(t, Cn.at === undefined ? p.t0 : Cn.at, Cn.out, 0.45); if (u > 0.01) { let x = SAFE.x0, y = V ? 210 : 62;
    if (Cn.title) { const px = 34 * S, bh = 72 * S, tw0 = tw(g, Cn.title, px, 700) + 44; panel(g, x, y, tw0, bh, { a: u, fill: 'rgba(12,18,27,0.92)', r: bh / 2 }); text(g, Cn.title, x + 22, y + bh / 2 + px * 0.36, px, '#E6EBF0', { a: u, w: 700 }); x += tw0 + 14; }   /* chú giải điểm (chấm mù V2: '3 vs 0' không rõ nghĩa) */
    for (const sd of Cn.sides) { const n = Array.isArray(sd.n) ? sd.n.reduce((v, e) => (t >= e.t ? e.v : v), '') : sd.n, px = 34 * S;   /* V4 (G3): chữ bảng điểm ≥ 34 px */
      const nw = n === undefined || n === '' ? 0 : tw(g, String(n), 40 * S, 700, true) + 30, bw = 86 * S + tw(g, sd.s, px, 700) + nw + 36, bh = 72 * S;
      panel(g, x, y, bw, bh, { a: u, fill: 'rgba(12,18,27,0.92)', stroke: sd.c, r: bh / 2 }); drawIcon(g, sd.icon, x + 44 * S, y + bh / 2, 58 * S, u);
      text(g, sd.s, x + 86 * S, y + bh / 2 + px * 0.36, px, K.text, { a: u, w: 700 });
      if (nw) { const bx = x + bw - nw - 8; g.save(); g.globalAlpha *= u; g.fillStyle = sd.c; rrect(g, bx, y + 10, nw, bh - 20, (bh - 20) / 2); g.fill(); g.restore(); text(g, String(n), bx + nw / 2, y + bh / 2 + 14 * S, 40 * S, K.ink, { a: u, w: 700, disp: true, align: 'center' }); }
      x += bw + 18; } } }
  const Bd = Sc.board; if (!Bd) return; const u = vis(t, Bd.at === undefined ? p.t0 : Bd.at, Bd.out, 0.5); if (u <= 0.01) return;
  const CMP = !V && (Bd.w || 1340) < 1000, n = Bd.rows.length, rh = V ? 150 : CMP ? 86 : 108, hh = V ? 190 : CMP ? 140 : 150,   /* CMP (V3, E4): bảng hẹp ~40 % khung — hàng 2 dòng: biểu tượng + nhãn trên, hai giá trị dưới */ bw = V ? 960 : (Bd.w || 1340), top0 = Bd.title ? (V ? 90 : 72) : 0, bh = top0 + hh + n * rh + (Bd.foot ? 70 : 30), bx = !V && Bd.align === 'right' ? W - SAFE.x0 - bw : (W - bw) / 2;   /* align right: lộ bản đồ bên trái (chấm mù V2: bảng che bản đồ) */
  const by = Math.max(SAFE.y0 + (Cn ? 90 : 0), (H - bh) / 2 - (V ? 0 : 10)), sl = eo(u);
  g.save(); g.translate(0, (1 - sl) * 40); panel(g, bx, by, bw, bh, { a: u, fill: 'rgba(12,18,27,0.93)', r: 18 });
  const cx = CMP ? [bx + bw * 0.565, bx + bw * 0.835] : [bx + bw * 0.22, bx + bw * 0.78], mid = bx + bw / 2;   /* V4 (G3): bảng gọn — cột nhãn bên trái, hai cột giá trị bên phải, mỗi hàng MỘT dòng, chữ ≥ 34 px */
  if (Bd.title) text(g, Bd.title, mid, by + 58, 40 * S, '#E6EBF0', { a: u, w: 700, align: 'center' });
  Bd.sides.forEach((sd, i) => { const y = by + top0 + hh / 2; drawIcon(g, sd.icon, cx[i], y - (CMP ? 22 : 18), (CMP ? 74 : 96) * S, u); text(g, sd.s, cx[i], y + (CMP ? 48 : 62), (CMP ? 36 : 40) * S, sd.c, { a: u, w: 700, disp: true, align: 'center' });
    g.save(); g.globalAlpha *= u; g.fillStyle = sd.c; g.fillRect(cx[i] - 70, y + (CMP ? 60 : 76), 140, 5); g.restore(); });
  if (!CMP) text(g, 'vs', mid, by + top0 + hh / 2 + 14, 34 * S, K.steel, { a: u, w: 600, align: 'center' });
  Bd.rows.forEach((r, i) => { const a = vis(t, r.at === undefined ? (Bd.at || p.t0) + 0.4 + i * 0.35 : r.at, undefined, 0.45) * u; if (a <= 0.01) return; const y = by + top0 + hh + i * rh;
    g.save(); g.globalAlpha *= a; g.fillStyle = i % 2 ? 'rgba(255,255,255,0.025)' : 'rgba(255,255,255,0.055)'; g.fillRect(bx + 16, y + 6, bw - 32, rh - 12); g.restore();
    const vy = CMP ? y + rh * 0.5 + 15 : y + rh * 0.62;
    if (CMP) { drawIcon(g, r.icon, bx + 50, y + rh * 0.5, 46, a); text(g, r.k, bx + 86, y + rh * 0.5 + 13, 36, '#D6DDE4', { a, w: 600, maxW: bw * 0.43 - 86 }); }
    else { drawIcon(g, r.icon, mid, y + rh * 0.36, 54 * S, a); text(g, r.k, mid, y + rh * 0.88, 32 * S, '#D6DDE4', { a, w: 600, align: 'center' }); }
    r.v.forEach((v, j) => { const win = r.win === j, c = win ? Bd.sides[j].c : K.text, vp = CMP ? (win ? 42 : 40) : (win ? 46 : 42); text(g, v, cx[j], vy, vp * S, c, { a, w: 700, disp: true, align: 'center' });
      if (r.sub && r.sub[j] && !CMP) text(g, r.sub[j], cx[j], vy + 34 * S, 30 * S, K.dim, { a, w: 500, align: 'center' });
      if (win) { g.save(); g.globalAlpha *= a; g.strokeStyle = Bd.sides[j].c; g.lineWidth = 4; const ww = tw(g, v, vp * S, 700, true), pd = CMP ? 14 : 22; rrect(g, cx[j] - ww / 2 - pd, vy - (CMP ? 44 : 50) * S, ww + 2 * pd, (CMP ? 58 : 66) * S, 29 * S); g.stroke(); g.restore(); } }); LL.fill = true; });
  if (Bd.foot) srcLine(g, Bd.foot, mid, by + bh - 30, u, 'center', bw - 48); g.restore(); }

// ---------- thẻ (nền: cảnh 3D mờ) ----------
const CARD = V ? { x: 60, y: 300, w: 960, h: 1220 } : { x: 150, y: 96, w: 1620, h: 780 };
function cardFrame(g, c, t, u) { const R = CARD; panel(g, R.x, R.y, R.w, R.h, { a: u, fill: 'rgba(13,20,30,0.80)', accent: c.accent || K.orange, r: 14 });
  // lưới kỹ thuật mảnh
  g.save(); g.globalAlpha *= 0.5 * u; g.strokeStyle = 'rgba(154,167,181,0.08)'; g.lineWidth = 1; for (let x = R.x + 40; x < R.x + R.w; x += 40) { g.beginPath(); g.moveTo(x, R.y + 8); g.lineTo(x, R.y + R.h - 8); g.stroke(); } for (let y = R.y + 40; y < R.y + R.h; y += 40) { g.beginPath(); g.moveTo(R.x + 8, y); g.lineTo(R.x + R.w - 8, y); g.stroke(); } g.restore();
  if (c.kicker) text(g, c.kicker, R.x + 50, R.y + 62 * S, 30 * S, c.accent || K.orange, { a: u, w: 700 });
  if (c.title) para(g, c.title, R.x + 50, R.y + (c.kicker ? 118 : 80) * S, R.w - 100, 50 * S, K.text, { a: u, w: 700, disp: true }); }
const TPLC = {};
const p0 = (c) => (c.in === undefined ? -1e9 : c.in);   // lúc thẻ vào (thẻ không trống khi chờ số neo theo lời)
// số lớn: {value/text, s (nhãn), sub, kind, at, beats: [{s, at}], unit}
TPLC.num = (g, c, t, u) => { const R = CARD, cx = R.x + R.w / 2, a = rv(t, c.at, 0.6), big = c.big || c.text || String(c.value);
  const cy = R.y + R.h * (V ? 0.42 : ((c.beats || []).length ? 0.47 : 0.55)); text(g, big, cx, cy, (V ? 170 : 210) * (c.scale || 1), c.kind === 'projection' ? K.amber : K.orange, { a: a * u, w: 700, disp: true, align: 'center', maxW: R.w - 120 });
  if (c.unit) text(g, c.unit, cx, cy + (V ? 90 : 80), (V ? 50 : 48), K.text, { a: rv(t, c.unitAt === undefined ? p0(c) : c.unitAt, 0.5) * u, w: 600, align: 'center', maxW: R.w - 120 });
  if (c.kind) kindTag(g, c.kind, cx, cy - (V ? 210 : 240), a * u, 'center');
  let y = cy + (V ? 190 : 165); for (const b of c.beats || []) { const ab = rv(t, b.at, 0.45); y = para(g, b.s, cx, y, R.w - 160, (b.px || 40) * S, b.c || K.dim, { a: ab * u, w: 500, align: 'center' }) + 56 * S; } };
// cột: {items: [{label, value, text, at, c, hatch}], max, ref: {value, label, at}, unit, horizontal (mặc định), note}
TPLC.bars = (g, c, t, u) => { const R = CARD, x0 = R.x + (V ? 60 : 460), x1 = R.x + R.w - (V ? 60 : 120), n = c.items.length, mx = c.max || Math.max(...c.items.map((i) => i.value)) * 1.08;
  const hdr = R.y + (c.title ? (c.kicker ? 200 : 160) : 100) * S, foot = R.y + R.h - (c.note ? 150 : 90) * S, rowH = Math.min(V ? 230 : 170, (foot - hdr) / n), top = hdr + ((foot - hdr) - rowH * n) / 2;
  c.items.forEach((it, i) => { const y = top + i * rowH, a = rv(t, it.at, 0.8), w = (x1 - x0) * it.value / mx * eo((t - (it.at === undefined ? -1e9 : it.at)) / 0.8); const col = it.c || K.orange;
    const by = V ? y + 40 : y + rowH * 0.5 - 45, bh = 90;
    if (V) text(g, it.label, x0, y + 20, 42, K.text, { a: u, w: 600 }); else text(g, it.label, x0 - 30, by + bh * 0.66, 42, K.text, { a: u, w: 600, align: 'right', maxW: 400 });
    g.save(); g.globalAlpha *= u; g.fillStyle = 'rgba(154,167,181,0.10)'; g.fillRect(x0, by, x1 - x0, bh); g.fillStyle = col; g.fillRect(x0, by, w, bh); g.restore();
    const tx = it.text || String(it.value), tw0 = tw(g, tx, 52, 700, true);
    if (x0 + w + 24 + tw0 <= x1) text(g, tx, x0 + w + 24, by + bh * 0.7, 52, K.text, { a: a * u, w: 700, disp: true });
    else text(g, tx, x0 + w - 24, by + bh * 0.7, 52, K.ink, { a: a * u, w: 700, disp: true, align: 'right' }); });
  if (c.ref) { const xr = x0 + (x1 - x0) * c.ref.value / mx, a = rv(t, c.ref.at, 0.5); g.save(); g.globalAlpha *= a * u; g.setLineDash([12, 8]); g.strokeStyle = K.teal; g.lineWidth = 4; g.beginPath(); g.moveTo(xr, top - 30); g.lineTo(xr, top + n * rowH); g.stroke(); g.restore();
    text(g, c.ref.label, xr, top + n * rowH + 44 * S, 34 * S, K.teal, { a: a * u, w: 600, align: xr > x1 - 300 ? 'right' : 'center' }); }
  if (c.note) para(g, c.note, R.x + 50, R.y + R.h - 96 * S, R.w - 100, 34 * S, K.dim, { a: u * rvH(t, c.noteAt), w: 500 }); };
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
TPLC.timeline = (g, c, t, u) => { const R = CARD, n = c.items.length;
  let last = -1; c.items.forEach((it, i) => { if (t >= (it.at === undefined ? -1e9 : it.at)) last = i; });
  if (!V) { const x0 = R.x + 70, x1 = R.x + R.w - 50, cw = (x1 - x0) / n, y = R.y + (c.title ? 330 : 270), hasBig = c.items.some((it) => it.big);
    g.save(); g.globalAlpha *= u; g.strokeStyle = 'rgba(154,167,181,0.4)'; g.lineWidth = 3; g.beginPath(); g.moveTo(x0, y); g.lineTo(x1 - 40, y); g.stroke(); g.restore();
    c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5), x = x0 + i * cw, hi = i === last, col = it.c || (hi ? K.orange : K.steel); if (a <= 0) return;
      g.save(); g.globalAlpha *= a * u; g.fillStyle = col; g.beginPath(); g.arc(x + 12, y, hi ? 15 : 11, 0, 7); g.fill(); g.restore();
      text(g, it.date, x, y - 38, 40, hi ? K.orange : K.text, { a: a * u, w: 700, disp: true, maxW: cw - 30 });
      let yy = y + 70; if (it.big) { text(g, it.big, x, y + 120, 84, hi ? K.orange : K.text, { a: a * u, w: 700, disp: true }); yy = y + 185; } else if (hasBig) yy = y + 70;
      wrap(g, it.s, cw - 40, 34, 500).slice(0, 5).forEach((l, j) => text(g, l, x, yy + j * 44, 34, hi ? K.text : K.dim, { a: a * u, w: 500 })); }); }
  else { const step = Math.min(210, (R.h - 300) / n); c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5), yy = R.y + 260 + i * step; if (a <= 0) return; g.save(); g.globalAlpha *= a * u; g.fillStyle = it.c || (i === last ? K.orange : K.steel); g.beginPath(); g.arc(R.x + 70, yy, 12, 0, 7); g.fill(); g.restore();
    text(g, it.date + (it.big ? '  ' + it.big : ''), R.x + 110, yy + 14, 48, i === last ? K.orange : K.text, { a: a * u, w: 700, disp: true }); para(g, it.s, R.x + 110, yy + 72, R.w - 160, 46, K.dim, { a: a * u, w: 500 }); }); } };
let L;
// hai cột: {left: {tag, title, lines: [{s, at}], c}, right: {...}, mid: 'vs'}
TPLC.split = (g, c, t, u) => { const R = CARD, gap = 40, cw = V ? R.w - 80 : (R.w - 100 - gap) / 2, top = R.y + (c.title ? 230 : 70);
  [c.left, c.right].forEach((col, k) => { if (!col) return; const a = rv(t, col.at, 0.5); if (a <= 0) return; const x = V ? R.x + 40 : R.x + 50 + k * (cw + gap), y = V ? top + k * (R.h - (top - R.y)) / 2 : top, h = V ? (R.h - (top - R.y)) / 2 - 30 : R.h - (top - R.y) - 50;
    panel(g, x, y, cw, h, { a: a * u, accent: col.c || (k ? K.teal : K.orange), fill: 'rgba(22,33,47,0.9)', dash: col.dash });
    text(g, col.tag, x + 34, y + 62, 32 * S, col.c || (k ? K.teal : K.orange), { a: a * u, w: 700 }); let yy = col.title ? para(g, col.title, x + 34, y + 130, cw - 70, 44 * S, K.text, { a: a * u, w: 700, disp: true }) + 80 : y + 130;
    for (const ln of col.lines || []) { const b = rv(t, ln.at, 0.45); if (b <= 0) continue; g.save(); g.globalAlpha *= b * u; g.fillStyle = col.c || (k ? K.teal : K.orange); g.fillRect(x + 34, yy - 26 * S, 10, 10); g.restore(); yy = para(g, ln.s, x + 60, yy, cw - 100, 36 * S, ln.c || K.text, { a: b * u, w: 500 }) + 60 * S; } }); };
// danh sách / luồng: {items: [{s, sub, at}], flow (mũi tên giữa các bước), num (đánh số)}
TPLC.list = (g, c, t, u) => { const R = CARD, n = c.items.length, top = R.y + (c.top || (c.title ? 250 : 120)) * S;   // c.top: thẻ nhiều mục (K2C-T1-06 07, 13/10)
  if (c.flow && !V) { const bw = (R.w - 100 - (n - 1) * 50) / n; c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5); if (a <= 0) return; const x = R.x + 50 + i * (bw + 50), y = top - 30 * S, h = R.h - (top - R.y) - 100 * S;
      panel(g, x, y, bw, h, { a: a * u, accent: it.c || K.orange, fill: 'rgba(22,33,47,0.92)' }); text(g, String(i + 1), x + 30, y + 72, 56, it.c || K.orange, { a: a * u, w: 700, disp: true });
      const ye = para(g, it.s, x + 30, y + 140, bw - 54, 38, K.text, { a: a * u, w: 700 }); if (it.sub) para(g, it.sub, x + 30, ye + 50, bw - 54, 31, K.dim, { a: a * u, w: 500 });
      if (i < n - 1) { g.save(); g.globalAlpha *= a * u; g.fillStyle = K.steel; g.beginPath(); g.moveTo(x + bw + 12, y + h / 2 - 16); g.lineTo(x + bw + 38, y + h / 2); g.lineTo(x + bw + 12, y + h / 2 + 16); g.fill(); g.restore(); } }); return; }
  const px = (c.px || 40) * S, mw = R.w - 180, gap = (c.gap || 64) * S;
  const hts = c.items.map((it) => wrap(g, it.s, mw, px, 600).length * px * 1.28 + (it.sub ? wrap(g, it.sub, mw, 32 * S, 500).length * 32 * S * 1.28 + 16 : 0));
  const total = hts.reduce((x, h) => x + h, 0) + gap * (c.items.length - 1), foot = R.y + R.h - 90 * S; let y = top + (c.top ? 30 * S : Math.max(30, ((foot - top) - total) / 2)) + px * 0.8;   // c.top: bám trên (dòng nguồn nhiều dòng ở đáy thẻ)
  c.items.forEach((it, i) => { const a = rv(t, it.at, 0.5), col = it.c || K.orange; if (a > 0) { g.save(); g.globalAlpha *= a * u;
      if (it.check === false) { g.fillStyle = col; g.fillRect(R.x + 60, y - px * 0.8, 8, px * 0.9); }
      else { g.strokeStyle = col; g.lineWidth = 3; g.strokeRect(R.x + 60, y - 30 * S, 30 * S, 30 * S); g.beginPath(); g.moveTo(R.x + 66, y - 14 * S); g.lineTo(R.x + 60 + 13 * S, y - 6); g.lineTo(R.x + 60 + 26 * S, y - 26 * S); g.stroke(); } g.restore();
      const ye = para(g, it.s, R.x + 60 + 54 * S, y, mw, px, it.check === false && it.c ? it.c : K.text, { a: a * u, w: 600 }); if (it.sub) para(g, it.sub, R.x + 60 + 54 * S, ye + 46 * S, mw, 32 * S, K.dim, { a: a * u, w: 500 }); }
    y += hts[i] + gap; }); };
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
  let last = -1; c.rows.forEach((r, i) => { if (t >= (r.at || 0)) last = i; }); if (c.hiAt !== undefined) last = t >= c.hiAt ? 0 : -1;   // hiAt: nổi hàng 1 (hàng đang kể)
  c.rows.forEach((r, i) => { const a = rv(t, r.at, 0.55); if (a <= 0) return; const y = top + i * rh, off = (n - 1 - i) * 40 * (V ? 0 : 1), col = r.c || [K.steel, K.orange, K.teal][i % 3];
    panel(g, R.x + 60 + off, y, R.w - 120 - 2 * off, rh - 24, { a: a * u, accent: col, fill: i === last ? 'rgba(30,44,62,0.95)' : 'rgba(22,33,47,0.85)' });
    text(g, r.k, R.x + 100 + off, y + rh * 0.42, 34 * S, col, { a: a * u, w: 700 }); text(g, r.s, R.x + (V ? 100 : 420) + off, y + (V ? rh * 0.42 + 64 : rh * 0.42), 42 * S, K.text, { a: a * u, w: 700, disp: true, maxW: R.w - (V ? 220 : 560) - 2 * off });
    if (r.sub) text(g, r.sub, R.x + (V ? 100 : 420) + off, y + (V ? rh * 0.42 + 120 : rh * 0.42 + 50), 32 * S, K.dim, { a: a * u, w: 500, maxW: R.w - (V ? 220 : 560) - 2 * off }); }); };
// thẻ kết
TPLC.end = (g, c, t, u) => { const R = CARD, cx = R.x + R.w / 2; let y = R.y + R.h * 0.34; (c.lines || []).forEach((l) => { text(g, l.s, cx, y, (l.px || 48) * S, l.c || K.text, { a: rv(t, l.at, 0.6) * u, w: l.w || 600, disp: !!l.disp, align: 'center', maxW: R.w - 120 }); y += (l.gap || ((l.px || 48) * 1.9)) * S; }); };

// ---------- mẫu plate (duy nhất) ----------
const TPL = {};
TPL.plate = (p) => ({ kind: 'full', full(g, t) {
  const c = p.card, blur = c ? (p.blur === undefined ? 14 : p.blur) : (p.blur || 0), dim = c ? (p.dim === undefined ? 0.45 : p.dim) : (p.dim || 0);
  drawPlate(g, p, t, blur, dim); if (!c) { labels(g, p, t); title(g, p, t); }
  if (c) { const u = vis(t, c.in === undefined ? p.t0 : c.in, c.out, 0.5); cardFrame(g, c, t, u); (TPLC[c.type] || (() => {}))(g, c, t, u); LL.fill = true;
    if (p.src) srcLine(g, p.src, CARD.x + 50, CARD.y + CARD.h - 34, u); }
  else { colOcc(p, t); yearChip(g, p, t); if (p.tl) tlLayer(g, p, t); else whereChip(g, p, t); stickers(g, p, t); caps(g, p, t); sideCap(g, p, t); tags(g, p, t, p.places); tags(g, p, t, p.tags); score(g, p, t); }   // V2: sticker dưới dải chú thích; bảng điểm trên cùng   // nhãn k2v vẽ SAU dải chú thích/nguồn: dải tối của caps phủ mờ nhãn ở 1/3 dưới khung (chấm mù P2, 12/10)
  const kd = p.__kind === undefined ? (p.__kind = typeof p.kind === 'string' ? p.kind : /"kind":"projection"/.test(JSON.stringify(p)) ? 'projection' : /"kind":"actual"/.test(JSON.stringify(p)) ? 'actual' : '') : p.__kind;   // G2 (K 1.11 O5): p.kind khai rõ nhãn góc ('' = không nhãn góc, khi các thẻ tự mang nhãn) — thẻ dưới nhãn góc thôi khai kind → 1 ACTUAL/khung
  if (kd) { if (c) kindTag(g, kd, CARD.x + CARD.w - 40, CARD.y + CARD.h - 44, vis(t, c.in === undefined ? p.t0 : c.in, c.out, 0.5), 'right'); else if (V) kindTag(g, kd, W / 2, H * 0.70 - 24, 1, 'center'); else kindTag(g, kd, W - SAFE.x0, H - (EDGE_B + 14), 1, 'right'); }   // 9:16: trên dải chú thích (13/10: ở H−330 đè dòng nguồn 2 dòng)   // Q7: shot có số → nhãn ACTUAL/PROJECTION
  asof(g, p, t); } });

// thẻ cuối Short (ll.py tự chèn tpl 'endcard', p.line)
TPL.endcard = (p) => ({ kind: 'full', full(g, t) { const gr = g.createRadialGradient(W / 2, H * 0.45, 40, W / 2, H * 0.45, H * 0.8); gr.addColorStop(0, '#1b2738'); gr.addColorStop(1, K.ink); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  g.save(); g.strokeStyle = 'rgba(154,167,181,0.10)'; g.lineWidth = 1.5; const o = (t * 18) % 60; for (let x = -60 + o; x < W + 60; x += 60) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); } for (let y = -60 + o; y < H + 60; y += 60) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); } g.restore();
  const a = rvH(t, p.t0, 0.4), z = 1 + 0.03 * cl((t - p.t0) / 1.5); g.save(); g.translate(W / 2, H * 0.45); g.scale(z, z); g.translate(-W / 2, -H * 0.45);
  text(g, (window.SPEC && window.SPEC.brand) || p.brand || 'STEEL', W / 2, H * 0.42, V ? 130 : 120, K.text, { a, w: 700, disp: true, align: 'center', maxW: W - 192 }); g.save(); g.globalAlpha *= a; g.fillStyle = K.orange; g.fillRect(W / 2 - 60, H * 0.42 + 36, 120, 6); g.restore();
  text(g, p.line || 'full film on the channel', W / 2, H * 0.42 + 130, V ? 52 : 44, K.dim, { a, w: 600, align: 'center' }); g.restore(); } });

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
  if (fi > 0 && fr < fi) k = Math.max(k, 1 - sm((fr + 1) / (fi + 1))); if (fo > 0 && fr > N - 1 - fo) k = Math.max(k, sm((fr - (N - 1 - fo)) / (fo + 1))); if (k > 0) { g.fillStyle = `rgba(3,4,8,${k})`; g.fillRect(0, 0, W, H); if (k > 0.2 && LL.tlog) LL.tlog.length = 0; } }   // khung đang tối dần (chuyển đoạn): không tính chữ cho Q5
window.drawFrame = (f) => { LL.occ = []; LL.act = false; LL.fill = false; LL.camNear = Infinity; LL.zones = []; LL.hit = 0; frameAt(X, f / FPS); };

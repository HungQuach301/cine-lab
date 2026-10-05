// Last Lamplighters · thư viện mẫu — đồ hoạ số trên tấm giấy B3: bars, line, compare, quote, bignum, text.
// Luật chuẩn kênh dựng sẵn trong mẫu (CHUAN-KENH §3, §5.1):
//   - trục số luôn từ 0 (không có tham số tắt); cột âm mọc xuống từ vạch 0;
//   - số dự báo: gạch chéo + viền nét đứt + nhãn PROJECTION; số thực tế: tô đặc + nhãn ACTUAL (nhãn hiện cùng lúc với số);
//   - dòng nguồn luôn có (ll.py chặn đặc tả thiếu nguồn), cỡ ≥ tối thiểu;
//   - không dựa riêng vào màu: dự báo khác thực tế bằng gạch chéo/nét đứt + chữ.
// Mỗi mẫu: TPL.name(p) → { kind: 'card', content(g, t, w, h), blur? }. t là giây CỤC BỘ của đoạn; mốc thời gian trong p đã được ll.py giải (số giây).
'use strict';
const TPL = window.TPL = window.TPL || {};
const K = LL.fmt === '9x16' ? 1.62 : 1;   // hệ số cỡ chữ theo khổ (26 → 42)
const PAD = LL.fmt === '9x16' ? 40 : 70;

function header(g, t, p, w) {   // trả độ dôi (px) khi tựa phải xuống dòng (khổ dọc)
  const u = rvH(t, p.t0 + 0.1, 0.8), V = LL.fmt === '9x16', px = (V ? 40 : 50) * K, lh = px * 1.15;
  const L = wrap(g, p.title || '', w - 2 * PAD - (V ? 0 : 260), px, 'serif'), ex = (L.length - 1) * lh;
  L.forEach((l, i) => textWipe(g, l, PAD, 92 * K + i * lh, px, INK, cl(u * L.length - i), { kind: 'serif' }));
  beatLine(g, t, p, PAD, 92 * K + ex + 50 * K, 28 * K);
  g.save(); g.strokeStyle = OCHRE; g.lineWidth = 2.5; g.beginPath(); g.moveTo(PAD, 92 * K + ex + 18 * K); g.lineTo(PAD + (w - 2 * PAD) * sm(u), 92 * K + ex + 18 * K); g.stroke(); g.restore();
  return ex;
}
// dòng phụ đề đổi theo lời: p.subtitle (sườn) rồi p.beats [{ s, at }] (nội dung gắn lời, hoà qua 0,4 s)
function beatLine(g, t, p, x, y, px, align = 'left') {
  const B = (p.beats || []).filter((b) => t >= b.at), cur = B[B.length - 1], prev = B[B.length - 2];
  if (!cur) { if (p.subtitle) text(g, p.subtitle, x, y, px, INK2, { a: rvH(t, p.t0 + 0.5, 0.6), align }); return; }
  const u = rv(t, cur.at, 0.4), old = prev ? prev.s : p.subtitle;
  if (old && u < 1) text(g, old, x, y, px, INK2, { a: 1 - u, align });
  text(g, cur.s, x, y, px, BROWN, { a: u, align });
}
function footH(g, p, w) { return p.src ? (wrap(g, p.src, w - 2 * PAD, MINPX).length - 1) * MINPX * 1.2 : 0; }
function footer(g, t, p, w, h) { if (!p.src) return; const L = wrap(g, p.src, w - 2 * PAD, MINPX); L.forEach((l, i) => srcLine(g, l, PAD, h - 30 - (L.length - 1 - i) * MINPX * 1.2, rvH(t, p.t0 + 0.4, 0.6))); }
function niceMax(v) { const e = Math.pow(10, Math.floor(Math.log10(v))), m = v / e; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * e; }
const fmtV = (v, unit, d) => unit === '%' ? fmtP(v, d === undefined ? 1 : d) : fmtN(v, d || 0);

// ---- cột: p = { title, subtitle, unit, bars: [{ label, value, text, kind, at, icon }], max, note, src } ----
TPL.bars = (p) => ({ kind: 'card', content(g, t, w, h) {
  const ex = header(g, t, p, w); footer(g, t, p, w, h);
  const B = p.bars, vmax = Math.max(...B.map((b) => Math.max(0, b.value))), vmin = Math.min(0, ...B.map((b) => b.value));
  const top = (p.max || niceMax(Math.max(vmax, -vmin) * 1.08));
  const y0 = 92 * K + 140 * K + ex, y1 = h - footH(g, p, w) - (p.note ? 175 : 130) * (LL.fmt === '9x16' ? 2 : 1), span = y1 - y0;
  const neg = vmin < 0, pos = vmax > 0, zy = neg && pos ? y0 + span * (top / (top + top)) : neg ? y0 + 40 : y1;
  const sc = (neg && pos ? span / 2 : span - 40) / top;
  const x0 = PAD + 20, x1 = w - PAD - 20, n = B.length, cw = (x1 - x0) / n, bw = Math.min(cw * 0.56, 240);
  // vạch 0 + lưới mờ
  g.save(); g.strokeStyle = INK; g.lineWidth = 2.5; g.globalAlpha *= rvH(t, p.t0 + 0.2, 0.6); g.beginPath(); g.moveTo(x0, zy); g.lineTo(x1, zy); g.stroke(); g.restore();
  tag(g, '0', x0 - 6, zy, 26 * K, 'rgba(243,232,204,0.95)', INK, { align: 'right', a: rvH(t, p.t0 + 0.2, 0.6) });   // nền giấy sáng: nhãn 0 không chìm vào góc tối của ánh rọi
  const kinds = new Set(B.map((b) => b.kind));
  B.forEach((b, i) => {
    const at = b.at === undefined ? p.t0 + 0.8 + i * 0.7 : b.at, u = rv(t, at, 0.9), e = eo(u), cx = x0 + cw * (i + 0.5);
    const hv = b.value * sc * e, yTop = b.value >= 0 ? zy - hv : zy, hh = Math.abs(hv);
    if (u > 0) { g.save();
      if (b.kind === 'projection') { g.fillStyle = HATCH_COLD; g.fillRect(cx - bw / 2, yTop, bw, hh); g.setLineDash([10, 6]); g.strokeStyle = COLD; g.lineWidth = 3; g.strokeRect(cx - bw / 2, yTop, bw, hh); }
      else { g.fillStyle = b.color || OCHRE; g.fillRect(cx - bw / 2, yTop, bw, hh); }
      g.restore(); }
    const la = rv(t, at - 0.1, 0.5);
    const lab = String(b.label || '').split('\n'); lab.forEach((l, k) => text(g, l, cx, (b.value >= 0 || !neg ? zy + 40 * K : zy - 20 * K - (lab.length - 1) * 32 * K) + k * 32 * K, 26 * K, INK, { align: 'center', a: la }));
    if (u > 0) { const v = b.value * e, s = b.text && u >= 1 ? b.text : fmtV(v, p.unit, b.d);
      const vy = b.value >= 0 ? yTop - 18 * K : zy + hh + 44 * K;
      text(g, s, cx, vy, 40 * K, INK, { align: 'center', kind: 'serif' });
      if (kinds.size > 1 || p.kindEach) kindTag(g, b.kind, cx, b.value >= 0 ? vy - 52 * K : vy + 34 * K, 22 * K, rv(t, at + 0.3, 0.4), 'center'); }
    if (b.icon) icon(g, b.icon, cx, (b.value >= 0 ? zy + 110 * K : y0 - 20) , 0.6 * K, la);
  });
  if (kinds.size === 1 && !p.kindEach) kindTag(g, [...kinds][0], w - PAD, LL.fmt === '9x16' ? 92 * K + ex + 56 * K : 92 * K - 12 * K, 22 * K, rvH(t, p.t0 + 0.6, 0.5), 'right');
  if (p.note) para(g, p.note, PAD, h - 82 - footH(g, p, w), w - 2 * PAD, 26 * K, INK2, { a: rv(t, p.noteAt || p.t0 + 1.5, 0.6) });
} });

// ---- đường: p = { title, subtitle, unit, xr: [x0, x1], ymax, series: [{ name, points: [[x, y]], proj_from, color, labels: [chỉ số điểm] }], at, dur, marks: [{ x, label, at }], src } ----
TPL.line = (p) => ({ kind: 'card', content(g, t, w, h) {
  const ex = header(g, t, p, w); footer(g, t, p, w, h);
  const all = p.series.flatMap((s) => s.points), ymax = p.ymax || niceMax(Math.max(...all.map((q) => q[1])) * 1.08);
  const [xa, xb] = p.xr || [Math.min(...all.map((q) => q[0])), Math.max(...all.map((q) => q[0]))];
  const L = PAD + 120 * K, R = w - PAD - 40 * K, T = 92 * K + 150 * K + ex, B = h - footH(g, p, w) - 130 * (LL.fmt === '9x16' ? 2 : 1);
  const px = (x) => L + (R - L) * (x - xa) / (xb - xa), py = (y) => B - (B - T) * y / ymax;
  const ax = rvH(t, p.t0 + 0.2, 0.7);
  g.save(); g.globalAlpha *= ax; g.strokeStyle = INK; g.lineWidth = 2.5; g.beginPath(); g.moveTo(L, T - 10); g.lineTo(L, B); g.lineTo(R, B); g.stroke();
  g.strokeStyle = 'rgba(33,26,23,0.18)'; g.lineWidth = 1.5; g.restore();
  for (let k = 0; k <= 4; k++) { const v = ymax * k / 4, y = py(v);
    if (k) { g.save(); g.globalAlpha *= ax * 0.5; g.strokeStyle = 'rgba(33,26,23,0.35)'; g.setLineDash([4, 6]); g.beginPath(); g.moveTo(L, y); g.lineTo(R, y); g.stroke(); g.restore(); }
    text(g, p.yfmt === 'k' ? (v >= 1000 ? fmtN(v / 1000) + 'k' : fmtN(v)) : fmtV(v, p.unit, 0), L - 14, y, 24 * K, INK, { align: 'right', base: 'middle', a: ax }); }
  (p.xticks || [xa, xb]).forEach((x) => text(g, String(x), px(x), B + 36 * K, 24 * K, INK, { align: 'center', a: ax }));
  if (p.ylabel) text(g, p.ylabel, L, T - 26 * K, 24 * K, INK2, { a: ax });
  const at = p.at === undefined ? p.t0 + 0.8 : p.at, dur = p.dur || 4, ux = eo(rv(t, at, dur)), xcut = xa + (xb - xa) * ux;
  p.series.forEach((s, si) => {
    const pts = s.points.filter((q) => q[0] <= xcut + 1e-9); if (!pts.length) return;
    // điểm nội suy ở đầu bút
    const nx = s.points.find((q) => q[0] > xcut); let head = pts[pts.length - 1];
    if (nx && ux < 1) { const a = pts[pts.length - 1], k2 = (xcut - a[0]) / (nx[0] - a[0]); head = [xcut, lerp(a[1], nx[1], k2)]; }
    const path = pts.concat(head !== pts[pts.length - 1] ? [head] : []), pf = s.proj_from === undefined ? Infinity : s.proj_from;
    g.save(); g.lineWidth = 6; g.lineJoin = 'round'; g.lineCap = 'round';
    for (let i = 1; i < path.length; i++) { const [x0_, y0_] = path[i - 1], [x1_, y1_] = path[i], proj = x0_ >= pf - 1e-9;
      g.strokeStyle = proj ? COLD : (s.color || OCHRE); g.setLineDash(proj ? [14, 10] : []); g.beginPath(); g.moveTo(px(x0_), py(y0_)); g.lineTo(px(x1_), py(y1_)); g.stroke(); }
    g.restore();
    const [hx, hy] = head; g.save(); g.fillStyle = s.color || OCHRE; g.beginPath(); g.arc(px(hx), py(hy), 8, 0, 7); g.fill(); g.restore();
    (s.labels || []).forEach((ix) => { const q = s.points[ix]; if (!q || q[0] > xcut + 1e-9) return; const la = rv(t, at + dur * (q[0] - xa) / (xb - xa), 0.4);
      g.save(); g.fillStyle = INK; g.globalAlpha *= la; g.beginPath(); g.arc(px(q[0]), py(q[1]), 7, 0, 7); g.fill(); g.restore();
      const s2 = (s.ltext && s.ltext[ix]) || (p.yfmt === 'k' && q[1] >= 1000 ? fmtN(q[1] / 1000, q[1] < 10000 ? 1 : 0) + 'k' : fmtV(q[1], p.unit, 0));
      const right = px(q[0]) > R - 160 * K; text(g, s2, px(q[0]) + (right ? -14 : 14), py(q[1]) - 18 * K, 32 * K, INK, { a: la, kind: 'serif', align: right ? 'right' : 'left' }); });
    if (s.name) { const end = path[path.length - 1]; text(g, s.name, Math.min(px(end[0]) + 16, R - 10), py(end[1]) + 40 * K, 26 * K, s.color || OCHRE, { a: rv(t, at + 0.4, 0.5), align: px(end[0]) > R - 240 ? 'right' : 'left' }); }
    // nhãn loại số liệu theo vùng
    if (pf < Infinity) { const xp = Math.max(xa, pf); kindTag(g, 'actual', px(xp) - 12, T + 10, 22 * K, rv(t, at + 0.3, 0.5), 'right');
      if (xcut >= pf) { g.save(); g.globalAlpha *= 0.6; g.strokeStyle = COLD; g.setLineDash([6, 6]); g.lineWidth = 2; g.beginPath(); g.moveTo(px(pf), T); g.lineTo(px(pf), B); g.stroke(); g.restore();
        kindTag(g, 'projection', px(pf) + 12, T + 10, 22 * K, rv(t, at + dur * (pf - xa) / (xb - xa), 0.4)); } }
    else if (si === 0) kindTag(g, s.kind || 'actual', w - PAD, LL.fmt === '9x16' ? 92 * K + ex + 56 * K : 92 * K - 12 * K, 22 * K, rv(t, p.t0 + 0.6, 0.5), 'right');
  });
  (p.marks || []).forEach((m) => { const a = rv(t, m.at, 0.5); if (a <= 0) return; g.save(); g.globalAlpha *= a; g.strokeStyle = BROWN; g.lineWidth = 2; g.setLineDash([3, 5]); g.beginPath(); g.moveTo(px(m.x), T); g.lineTo(px(m.x), B); g.stroke(); g.restore();
    para(g, m.label, px(m.x) + 10, T + 60 * K + (m.dy || 0), 300 * K, 24 * K, BROWN, { a }); });
} });

// ---- so sánh xưa–nay (cùng thước đo; ll.py chặn khác đơn vị): p = { left, right, unit, mid, diff: [..], at } ----
// left/right = { title, years, icon, value, text, kind, note }
TPL.compare = (p) => ({ kind: 'card', content(g, t, w, h) {
  const ex = header(g, t, p, w); footer(g, t, p, w, h);
  const V = LL.fmt === '9x16', cols = V ? [[PAD, 260 * K, w - 2 * PAD], [PAD, 260 * K + (h - 420 * K) / 2, w - 2 * PAD]] : [[PAD, 230, (w - 3 * PAD) / 2], [w / 2 + PAD / 2, 230, (w - 3 * PAD) / 2]];
  [p.left, p.right].forEach((s, i) => { const [x, y, cw] = cols[i], at = s.at === undefined ? p.t0 + 0.8 + i * 1.6 : s.at, a = rv(t, at, 0.6);
    if (a <= 0) return; const ch = (V ? (h - 520 * K) / 2 : h - 420) - footH(g, p, w);
    g.save(); g.globalAlpha *= a; g.strokeStyle = 'rgba(33,26,23,0.5)'; g.lineWidth = 2; g.strokeRect(x, y + (1 - eo(a)) * 20, cw, ch); g.restore();
    icon(g, s.icon, x + 90 * K, y + 100 * K, 0.9 * K, a);
    text(g, s.title, x + 180 * K, y + 80 * K, 34 * K, INK, { a, kind: 'serif' });
    if (s.years) text(g, s.years, x + 180 * K, y + 122 * K, 26 * K, INK2, { a });
    const va = rv(t, at + 0.5, 1.0); if (va > 0) {
      const num = typeof s.value === 'number' ? fmtV(s.value * eo(va), p.unit, s.d) : '';
      text(g, va >= 1 && s.text ? s.text : num, x + 40 * K, y + ch - (V ? 70 : 110) * K, 76 * K, s.kind === 'projection' ? '#22364f' : BROWN, { kind: 'serif' });
      kindTag(g, s.kind, x + cw - 30 * K, y + ch - (V ? 90 : 130) * K, 22 * K, va, 'right'); }
    if (s.note) para(g, s.note, x + 40 * K, y + ch - (V ? 24 : 50) * K, cw - 80 * K, 24 * K, INK2, { a: rv(t, at + 1.0, 0.6) }); });
  if (p.mid) { const a = rv(t, p.midAt || p.t0 + 3.5, 0.6); tag(g, p.mid, w / 2, V ? h / 2 + 20 : 200, 28 * K, '#f3e8cc', INK, { a, border: true, align: 'center' }); }
  (p.diff || []).forEach((d, i) => text(g, '≠ ' + d, PAD + (V ? 0 : i * (w - 2 * PAD) / Math.max(1, p.diff.length)), h - 82 - footH(g, p, w) - (V ? (p.diff.length - 1 - i) * 52 : 0), 26 * K, BROWN, { a: rv(t, (p.diffAt || p.t0 + 5) + i * 0.5, 0.5) }));
} });

// ---- trích dẫn: p = { text, who, where, at } ----
TPL.quote = (p) => ({ kind: 'card', content(g, t, w, h) {
  footer(g, t, p, w, h); if (p.beats) beatLine(g, t, p, w / 2, 90 * K, 30 * K, 'center'); const at = p.at === undefined ? p.t0 + 0.4 : p.at, dur = p.dur || Math.max(1.5, p.text.length / 40);
  text(g, '“', PAD + 10, 230 * K, 180 * K, AMBER, { kind: 'serif', a: rvH(t, p.t0, 0.5), deco: true });
  const yE = para(g, p.text, PAD + 120 * K, 230 * K, w - 2 * PAD - 160 * K, 46 * K, INK, { kind: 'serif', lh: 64 * K, u: rv(t, at, dur), wipe: true });
  if (p.who) text(g, '— ' + p.who, PAD + 120 * K, yE + 90 * K, 30 * K, INK2, { a: rv(t, at + dur, 0.5) });
  if (p.where) text(g, p.where, PAD + 120 * K, yE + 134 * K, 26 * K, INK2, { a: rv(t, at + dur + 0.2, 0.5) });
} });

// ---- thẻ số lớn: p = { value, text, prefix, suffix, d, caption, kind, at, dur, icon, sub } ----
TPL.bignum = (p) => ({ kind: 'card', content(g, t, w, h) {
  const ex = header(g, t, p, w); if (!p.kind) p.kind = (p.nums && p.nums[0] && p.nums[0].kind) || 'actual';   // loại số lấy từ số khai báo (sửa lỗi Short S2: −5,3 % dự báo) footer(g, t, p, w, h);
  const at = p.at === undefined ? p.t0 + 0.6 : p.at, u = rv(t, at, p.dur || 1.6), v = p.value * eo(u);
  if (p.icon) icon(g, p.icon, w / 2, h * 0.36, 1.1 * K, rvH(t, p.t0 + 0.3, 0.6));
  if (u > 0) text(g, u >= 1 && p.text ? p.text : (p.prefix || '') + (v < 0 ? M : '') + fmtN(Math.abs(v), p.d === undefined ? (Number.isInteger(p.value) ? 0 : 1) : p.d) + (p.suffix || ''), w / 2, h * (p.icon ? 0.62 : 0.55), 150 * K, p.kind === 'projection' ? '#22364f' : BROWN, { align: 'center', kind: 'serif' });
  kindTag(g, p.kind, w / 2, h * (p.icon ? 0.62 : 0.55) + 60 * K, 24 * K, rv(t, at + 0.2, 0.5), 'center');
  if (p.caption) para(g, p.caption, w / 2, h * (p.icon ? 0.62 : 0.55) + 140 * K, w - 4 * PAD, 34 * K, INK, { align: 'center', a: rv(t, p.capAt || at + 0.6, 0.6) });
} });

// ---- thẻ chữ / tựa: p = { lines: [{ s, px, at, serif, color }], lamp, align } ----
TPL.text = (p) => ({ kind: 'card', content(g, t, w, h) {
  footer(g, t, p, w, h); if (p.beats) beatLine(g, t, p, w / 2, 90 * K, 30 * K, 'center');
  const sz = p.lines.map((l) => (l.px || 48) * K), gap = p.lh ? p.lh - 48 * K : 34 * K, tot = sz.reduce((a, b) => a + b + gap, -gap);
  let y = h / 2 - tot / 2 + sz[0] * 0.75 + (p.lamp ? 90 * K : 0);
  if (p.lamp) { const lit = rv(t, p.t0 + 0.3, 0.9); gasLampIcon(g, w / 2, y - 330 * K, 1.0 * K, rvH(t, p.t0, 0.6), lit); if (lit > 0) glow(g, w / 2, y - 320 * K, 90 * K, RGB_AMB, 0.4 * lit); }
  p.lines.forEach((l, i) => { const at = l.at === undefined ? p.t0 + 0.4 + i * 0.6 : l.at; if (i) y += sz[i - 1] * 0.25 + gap + sz[i] * 0.75;
    textWipe(g, l.s, p.align === 'left' ? PAD : w / 2, y, sz[i], l.color || INK, rv(t, at, 0.9), { align: p.align || 'center', kind: l.serif === false ? 'sans' : 'serif' }); });
} });

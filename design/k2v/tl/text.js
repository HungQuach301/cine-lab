// K2V tl · NGÂN SÁCH CHỮ (port lab/timelapse overlay + textBudget + contrast, chủ dự án duyệt 16/10):
//  thường trực 2 lớp (năm dưới-trái, chỉ số trên-phải; 1 dòng, không nhãn; "≈" khi nội suy) · nhãn phương pháp + nguồn chỉ 4–6 s đầu + màn kết ·
//  ≤ 1 thẻ cùng lúc (tiêu đề ≤ 10 từ, dòng phụ = nguồn, 3–5 s) · chữ + nền ≤ 15 % khung (≤ 25 % mốc đinh) · vùng 20–80 % × 20–80 % không chữ trừ thẻ/nhãn neo ·
//  chữ ≥ 38 px@1080 cho nguồn đang hiện · tương phản ≥ 4,5:1 đo trên điểm ảnh thật. Vẽ SAU khi lấy khung WebGL (LUT/grain không chạm chữ).
export function makeText(W, H) {
  const S = H / 1080, cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d', { willReadFrequently: true });
  const FONT = '"DejaVu Sans", "Liberation Sans", Arial, sans-serif', RECTS = [], TXT = [], LOG = { cards: 0, overflow: [], leaders: [] };
  let anch = false;
  const words = (s) => s.replace(/[·—–:“”]/g, ' ').split(/\s+/).filter(Boolean).length;
  function text(s, x, y, px, color, o = {}) {
    if (!s || !s.trim() || (o.alpha ?? 1) <= 0.001) return;   // BAI-HOC-LL #46, #47: không vẽ/ghi chữ rỗng hoặc alpha 0
    g.font = `${o.w || 700} ${Math.round(px * S)}px ${FONT}`; g.textAlign = o.align || 'left'; g.textBaseline = 'alphabetic';
    if (o.halo) { g.lineJoin = 'round'; g.lineWidth = Math.max(2, px * S * 0.18); g.strokeStyle = 'rgba(10,14,20,0.88)'; g.strokeText(s, x, y); }
    g.fillStyle = color; g.fillText(s, x, y);
    const m = g.measureText(s), w = m.width, x0 = o.align === 'right' ? x - w : o.align === 'center' ? x - w / 2 : x;
    const box = [x0, y - m.actualBoundingBoxAscent, x0 + w, y + m.actualBoundingBoxDescent];
    if (o.halo) RECTS.push({ r: [box[0] - 4, box[1] - 4, box[2] + 4, box[3] + 4], anchored: !!o.anchored || anch });
    TXT.push({ s, px, box, alpha: o.alpha ?? 1, role: o.role || '' });
  }
  function plate(x0, y0, x1, y1, a) { RECTS.push({ r: [x0, y0, x1, y1], anchored: anch }); g.fillStyle = `rgba(12,16,22,${0.80 * a})`; g.beginPath(); g.roundRect(x0, y0, x1 - x0, y1 - y0, 14 * S); g.fill(); }
  // V5b-2a (TL-Q4b): mỗi đường dẫn ghi đầu đường dẫn (điểm ảnh, ở độ phân giải khung) + điểm 3D neo (ENU) → đo lệch độc lập bằng campath (anchor_dev.py)
  const leader = (role, s, from, end, a) => LOG.leaders.push({ role, s: s.slice(0, 40), from: from.map((v) => +v.toFixed(1)), end: end.map((v) => +v.toFixed(1)), world: a && a.w ? a.w.map((v) => +v.toFixed(2)) : null, W, H });
  const fade = (t, a, b, k = 0.35) => Math.max(0, Math.min(1, (t - a) / k, (b - t) / k));
  let YBOX = 0;
  // thẻ: dải dưới (bên phải hộp năm) hoặc neo vào điểm 3D (anchorPx = [x, y] màn hình)
  function card(t, win, title, src, anchorPx) {
    const a = fade(t, win[0], win[1]); if (a <= 0) return; LOG.cards++; if (words(title) > 10) LOG.overflow.push('tiêu đề > 10 từ: ' + title);
    g.globalAlpha = a; const xl = anchorPx ? 36 * S : YBOX + 24 * S, avail = W - 36 * S - xl;
    let tp = 48; g.font = `700 ${Math.round(tp * S)}px ${FONT}`; let w1 = g.measureText(title).width;
    if (w1 + 64 * S > avail) { tp = Math.max(40, tp * (avail - 64 * S) / w1); g.font = `700 ${Math.round(tp * S)}px ${FONT}`; w1 = g.measureText(title).width; }
    g.font = `500 ${Math.round(38 * S)}px ${FONT}`; const w2 = g.measureText(src).width;
    if (Math.max(w1, w2) + 64 * S > avail + 1) LOG.overflow.push('thẻ tràn: ' + title);
    const w = Math.min(avail, Math.max(w1, w2) + 60 * S), hgt = 126 * S;
    let cx = Math.min(W - 36 * S - w / 2, Math.max(xl + w / 2, W / 2)), y1 = H - 40 * S;
    if (anchorPx) { const [ax, ay] = anchorPx; cx = Math.min(W - 36 * S - w / 2, Math.max(36 * S + w / 2, ax)); y1 = Math.max(hgt + 40 * S, Math.min(H * 0.62, ay - 70 * S));
      anch = true; g.strokeStyle = '#ffd166'; g.lineWidth = 4 * S; g.beginPath(); g.moveTo(cx, y1); g.lineTo(ax, ay); g.stroke(); g.fillStyle = '#ffd166'; g.beginPath(); g.arc(ax, ay, 9 * S, 0, 7); g.fill();
      leader('card', title, [cx, y1], [ax, ay], anchorPx); }
    const y0 = y1 - hgt; plate(cx - w / 2, y0, cx + w / 2, y1, 1); g.fillStyle = '#ffd166'; g.fillRect(cx - w / 2, y0, 8 * S, hgt);
    text(title, cx, y0 + 58 * S, tp, '#ffffff', { align: 'center', alpha: a, role: 'card' }); text(src, cx, y0 + 106 * S, 38, '#c9d3dd', { align: 'center', w: 500, alpha: a, role: 'src' });
    anch = false; g.globalAlpha = 1;
  }
  // ảnh chú thích neo điểm 3D: ảnh (sepia nhẹ, KHÔNG LUT) + đường dẫn tới điểm neo + chú thích 2 dòng (tiêu đề + nguồn)
  function photo(t, win, img, title, src, anchorPx) {
    const a = fade(t, win[0], win[1]); if (a <= 0 || !img || !anchorPx) return; LOG.cards++;
    const [ax, ay] = anchorPx; g.globalAlpha = a; anch = true;
    g.font = `700 ${Math.round(44 * S)}px ${FONT}`; const wt1 = g.measureText(title).width; g.font = `500 ${Math.round(38 * S)}px ${FONT}`; const wt2 = g.measureText(src).width;
    const ih = 330 * S, iw = ih * img.width / img.height, cw = Math.max(wt1, wt2) + 48 * S, x1 = W - 36 * S, py0 = 210 * S, cy0 = py0 + ih + 10 * S, cy1 = cy0 + 116 * S;
    if (cw > W * 0.66) LOG.overflow.push('chú thích ảnh dài: ' + title);
    g.strokeStyle = '#ffd166'; g.lineWidth = 4 * S; g.beginPath(); g.moveTo(x1 - iw, py0 + ih / 2); g.lineTo(ax, ay); g.stroke(); leader('photo', title, [x1 - iw, py0 + ih / 2], [ax, ay], anchorPx);
    const k = (t * 1.2) % 1; g.beginPath(); g.arc(ax, ay, (10 + 26 * k) * S, 0, 7); g.strokeStyle = `rgba(255,209,102,${a * (1 - k)})`; g.stroke();
    g.fillStyle = '#ffd166'; g.beginPath(); g.arc(ax, ay, 9 * S, 0, 7); g.fill();
    g.filter = 'sepia(0.35) contrast(1.05)'; g.drawImage(img, x1 - iw, py0, iw, ih); g.filter = 'none'; g.strokeStyle = '#ffd166'; g.lineWidth = 3 * S; g.strokeRect(x1 - iw, py0, iw, ih);
    plate(x1 - cw, cy0, x1, cy1, 1);
    text(title, x1 - cw + 24 * S, cy0 + 52 * S, 44, '#ffffff', { alpha: a, role: 'card' }); text(src, x1 - cw + 24 * S, cy0 + 98 * S, 38, '#c9d3dd', { w: 500, alpha: a, role: 'src' });
    anch = false; g.globalAlpha = 1;
  }
  function tag(t, win, s, anchorPx) {   // nhãn neo nhỏ (ghost: "reconstructed from …"), có quầng, không nền
    const a = fade(t, win[0], win[1]); if (a <= 0 || !anchorPx) return; g.globalAlpha = a; anch = true;
    const [ax, ay] = anchorPx; g.strokeStyle = 'rgba(255,255,255,0.9)'; g.lineWidth = 3 * S; g.beginPath(); g.moveTo(ax, ay); g.lineTo(ax, ay - 64 * S); g.stroke(); leader('tag', s, [ax, ay - 64 * S], [ax, ay], anchorPx);
    // nền tối (lượt 1 dùng quầng: trên trời sáng đo được 2,24:1 < 4,5 → trượt)
    g.font = `600 ${Math.round(38 * S)}px ${FONT}`; const tw = g.measureText(s).width; plate(ax - tw / 2 - 18 * S, ay - 64 * S - 58 * S, ax + tw / 2 + 18 * S, ay - 64 * S, 1);
    text(s, ax, ay - 64 * S - 16 * S, 38, '#ffffff', { align: 'center', w: 600, alpha: a, role: 'tag' }); anch = false; g.globalAlpha = 1;
  }
  function chrome(t, year, pinZoom, idx, method, idxSrc) {   // năm + chỉ số + nhãn phương pháp (+ V5b-2a: dòng nguồn khi chỉ số là SỐ ĐẾM, role index_src)
    // V5b-2b (M6): year là số (năm) HOẶC {s, sub} — bộ đếm ngày/giờ "13 Sep 1782 · 09:45" (sub: dòng lịch thứ hai "O.S. 24 Jul · N.S. 4 Aug 1704")
    const clk = typeof year === 'object' && year, y = clk ? 0 : Math.floor(year), zs = 1 + 0.45 * pinZoom, ys = clk ? clk.s : String(y);
    g.font = `700 ${Math.round(96 * zs * S)}px ${FONT}`; const wy = g.measureText(ys).width; YBOX = 36 * S + wy + 48 * zs * S;
    plate(36 * S, H - 40 * S - 114 * zs * S, YBOX, H - 40 * S, 1);
    if (pinZoom > 0.01) { g.strokeStyle = `rgba(255,209,102,${pinZoom})`; g.lineWidth = 5 * S; g.strokeRect(36 * S, H - 40 * S - 114 * zs * S, wy + 48 * zs * S, 114 * zs * S); }
    text(ys, 36 * S + 24 * zs * S, H - 40 * S - 22 * zs * S, 96 * zs, pinZoom > 0.5 ? '#ffd166' : '#ffffff', { role: clk ? 'clock' : 'year' });
    if (clk && clk.sub) { g.font = `600 ${Math.round(38 * S)}px ${FONT}`; const w2 = g.measureText(clk.sub).width, yb = H - 40 * S - 114 * zs * S - 8 * S;
      plate(36 * S, yb - 60 * S, 36 * S + w2 + 40 * S, yb, 1); text(clk.sub, 56 * S, yb - 16 * S, 38, '#e8edf2', { w: 600, role: 'calendar' }); }
    let idxW = 0; if (idx) { g.font = `700 ${Math.round(60 * S)}px ${FONT}`; const wp = g.measureText(idx).width; idxW = wp + 52 * S; plate(W - 36 * S - wp - 52 * S, 36 * S, W - 36 * S, 36 * S + 98 * S, 1);
      text(idx, W - 62 * S, 36 * S + 70 * S, 60, '#ffffff', { align: 'right', role: 'index' });
      if (idxSrc && idxSrc.a > 0.001) { g.globalAlpha = idxSrc.a; g.font = `500 ${Math.round(38 * S)}px ${FONT}`; const ws = g.measureText(idxSrc.s).width;
        plate(W - 36 * S - ws - 40 * S, 36 * S + 98 * S + 8 * S, W - 36 * S, 36 * S + 98 * S + 8 * S + 60 * S, 1);
        text(idxSrc.s, W - 56 * S, 36 * S + 98 * S + 8 * S + 44 * S, 38, '#c9d3dd', { align: 'right', w: 500, alpha: idxSrc.a, role: 'index_src' }); g.globalAlpha = 1; } }
    // nhãn phương pháp: 1 hoặc nhiều dòng (V5b-2a HH3: dòng "≈ = interpolated between counts" — mỗi dòng có alpha riêng, xếp dưới nhau trên-trái)
    const ML = !method ? [] : (method.lines || [{ s: method.s, a: method.a }]).filter((m) => m.a > 0.001);
    let yy = method && method.bottom ? H - 40 * S - 64 * S : 36 * S;
    for (const m of ML) { g.globalAlpha = m.a; g.font = `600 ${Math.round(38 * S)}px ${FONT}`; const w1 = g.measureText(m.s).width;
      // đầu phim: trên-trái (không chạm hộp chỉ số); màn kết: dải dưới, bên phải hộp năm (không có thẻ ở màn kết)
      const x0 = method.bottom ? YBOX + 24 * S : 36 * S, y0 = yy;
      if (!method.bottom && idxW && y0 < 36 * S + 98 * S + 70 * S && x0 + w1 + 48 * S > W - 36 * S - idxW - 24 * S) LOG.overflow.push('nhãn phương pháp chạm hộp chỉ số');
      // V5b-2a: tấm nền gọn hơn (cao 64, lề 20) để thêm dòng HH3 mà vẫn ≤ 15 % khung khi trùng thẻ Tower (đo budgetAll)
      plate(x0, y0, x0 + w1 + 40 * S, y0 + 64 * S, 1); text(m.s, x0 + 20 * S, y0 + 45 * S, 38, '#ffffff', { w: 600, alpha: m.a, role: 'method' }); g.globalAlpha = 1;
      yy += method.bottom ? -72 * S : 72 * S; }
  }
  // V5b-2b (T2 TT6 / K-1.13): chip NƠI (trên-phải, dưới hộp chỉ số nếu có) và nhãn NGUỒN GHOST (dưới-phải, ≥ 38 px, role ghost_src)
  function where(t, win, s) { const a = fade(t, win[0], win[1]); if (a <= 0 || !s) return; g.globalAlpha = a; g.font = `600 ${Math.round(38 * S)}px ${FONT}`; const w = g.measureText(s).width;
    const x1 = W - 36 * S, y0 = 36 * S; plate(x1 - w - 76 * S, y0, x1, y0 + 64 * S, 1); g.fillStyle = '#F08A4B'; g.beginPath(); g.arc(x1 - w - 46 * S, y0 + 28 * S, 10 * S, Math.PI, 0); g.lineTo(x1 - w - 46 * S, y0 + 50 * S); g.closePath(); g.fill();
    text(s, x1 - 20 * S, y0 + 45 * S, 38, '#ffffff', { align: 'right', w: 600, alpha: a, role: 'where' }); g.globalAlpha = 1; }
  function ghostSrc(t, win, s) { const a = fade(t, win[0], win[1]); if (a <= 0 || !s) return; g.globalAlpha = a; g.font = `500 ${Math.round(38 * S)}px ${FONT}`; const w = g.measureText(s).width;
    const x1 = W - 36 * S, y1 = H - 40 * S; plate(x1 - w - 40 * S, y1 - 60 * S, x1, y1, 1); text(s, x1 - 20 * S, y1 - 16 * S, 38, '#c9d3dd', { align: 'right', w: 500, alpha: a, role: 'ghost_src' }); g.globalAlpha = 1; }
  function budget() {
    const q = 4, nx = Math.ceil(W / q), ny = Math.ceil(H / q), m = new Uint8Array(nx * ny);
    for (const { r: [x0, y0, x1, y1], anchored } of RECTS) for (let j = Math.max(0, Math.floor(y0 / q)); j < Math.min(ny, Math.ceil(y1 / q)); j++) for (let i = Math.max(0, Math.floor(x0 / q)); i < Math.min(nx, Math.ceil(x1 / q)); i++) m[j * nx + i] |= anchored ? 2 : 1;
    let all = 0, cen = 0, cenN = 0;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const v = m[j * nx + i]; if (v) all++; if (i >= nx * 0.2 && i < nx * 0.8 && j >= ny * 0.2 && j < ny * 0.8) { cenN++; if (v & 1) cen++; } }
    return { pct: +(100 * all / (nx * ny)).toFixed(2), center_unanchored_pct: +(100 * cen / cenN).toFixed(2), blocks: RECTS.length, cards: LOG.cards, min_px: TXT.length ? Math.min(...TXT.map((e) => e.px)) : null };
  }
  function contrast() {   // WCAG trên điểm ảnh thật: nền = trung vị viền hộp; chữ = phân vị 97 % trong hộp
    const lum = (r, gg, b) => [r, gg, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }).reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
    return TXT.filter((e) => e.alpha >= 0.95).map((e) => {
      const [x0, y0, x1, y1] = e.box.map(Math.round), X0 = Math.max(0, x0 - 4), Y0 = Math.max(0, y0 - 4), X1 = Math.min(W - 1, x1 + 4), Y1 = Math.min(H - 1, y1 + 4);
      const d = g.getImageData(X0, Y0, X1 - X0 + 1, Y1 - Y0 + 1).data, w = X1 - X0 + 1, h = Y1 - Y0 + 1, L = [], I = [];
      for (let x = 0; x < w; x++) for (const yy of [0, h - 1]) { const i = (yy * w + x) * 4; L.push(lum(d[i], d[i + 1], d[i + 2])); }
      for (let yy = 3; yy < h - 3; yy++) for (let x = 3; x < w - 3; x++) { const i = (yy * w + x) * 4; I.push(lum(d[i], d[i + 1], d[i + 2])); }
      L.sort((a, b) => a - b); I.sort((a, b) => a - b); const bg = L[Math.floor(L.length / 2)], ft = I[Math.floor(I.length * 0.97)] ?? bg;
      return { s: e.s.slice(0, 48), role: e.role, px1080: e.px, words: words(e.s), ratio: +((Math.max(bg, ft) + 0.05) / (Math.min(bg, ft) + 0.05)).toFixed(2) };
    });
  }
  const roles = () => [...new Set(TXT.filter((e) => e.alpha > 0.001).map((e) => e.role))];
  function begin(img) { RECTS.length = 0; TXT.length = 0; LOG.cards = 0; LOG.overflow = []; LOG.leaders = []; g.clearRect(0, 0, W, H); if (img) g.drawImage(img, 0, 0, W, H); }
  return { cv, g, begin, chrome, card, photo, tag, where, ghostSrc, budget, contrast, roles, log: LOG, S };
}

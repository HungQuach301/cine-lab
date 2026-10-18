// K2V tl · V5b-2b · BỘ GHI LỚP CHỮ (V5B2A §8.5): cùng API với text.js (chrome / card / photo / tag / where / ghostSrc) nhưng KHÔNG vẽ —
// ghi mô tả lớp chữ của khung (độ đục đã tính theo cửa sổ, điểm neo đã chiếu, chuẩn hoá 0..1 theo khung) để scripts/k2/lib/k2.js vẽ lại
// bằng chữ + bảng màu của kênh (Inter, MOVING PARTS) ở lớp 2D của render.js. Một cảnh tl → hai driver cùng nội dung chữ:
//  scripts/k2tl/render.js (text.js vẽ thẳng, đo ngân sách) và scripts/k2/hero.js → anchors.json[f]._tl → k2.js tlLayer().
export function makeRecorder(W, H) {
  let D = null;
  const fade = (t, a, b, k = 0.35) => Math.max(0, Math.min(1, (t - a) / k, (b - t) / k));
  const nx = (p) => (p ? [+(p[0] / W).toFixed(4), +(p[1] / H).toFixed(4)] : null);
  const w3 = (p) => (p && p.w ? p.w.map((v) => +v.toFixed(2)) : null);
  return {
    begin() { D = { cards: [], tags: [], photos: [] }; },
    chrome(t, year, pinZoom, idx, method, idxSrc) {
      const clk = typeof year === 'object' && year;
      D.chrome = { year: clk ? null : +year.toFixed(2), clock: clk ? { s: clk.s, sub: clk.sub || null } : null, pin: +(pinZoom || 0).toFixed(3), idx: idx || null,
        idxSrc: idxSrc && idxSrc.a > 0.001 ? { s: idxSrc.s, a: +idxSrc.a.toFixed(3) } : null,
        method: method ? { bottom: !!method.bottom, lines: (method.lines || [{ s: method.s, a: method.a }]).filter((m) => m.a > 0.001).map((m) => ({ s: m.s, a: +m.a.toFixed(3) })) } : null };
    },
    card(t, win, title, src, anchorPx) { const a = fade(t, win[0], win[1]); if (a <= 0) return;   // như text.js: không neo (null) → dải dưới
      D.cards.push({ title, src, a: +a.toFixed(3), anchor: nx(anchorPx), world: w3(anchorPx) }); },
    photo(t, win, img, title, src, anchorPx) { const a = fade(t, win[0], win[1]); if (a <= 0 || !anchorPx) return; D.photos.push({ title, src, a: +a.toFixed(3), anchor: nx(anchorPx), world: w3(anchorPx), img: img && img.src ? String(img.src).replace(/^.*\/cache\//, 'cache:') : null }); },
    tag(t, win, s, anchorPx) { const a = fade(t, win[0], win[1]); if (a <= 0 || !anchorPx) return; D.tags.push({ s, a: +a.toFixed(3), anchor: nx(anchorPx), world: w3(anchorPx) }); },
    where(t, win, s) { const a = fade(t, win[0], win[1]); if (a > 0 && s) D.where = { s, a: +a.toFixed(3) }; },
    ghostSrc(t, win, s) { const a = fade(t, win[0], win[1]); if (a > 0 && s) D.ghost_src = { s, a: +a.toFixed(3) }; },
    aiLabel(on, zs = 1) { if (on) D.ai_label = { s: 'Surface detail AI-assisted · layout, landmarks & flags from sources' }; },   // V6 (§11.3, K-LAI-2): k2.js vẽ dưới-trái trên hộp năm/giờ, ≥ 38 px
    data() { return D; },
    // không có ngân sách/tương phản ở đây: đo trên khung thật ở render.js (k2) — giữ hàm rỗng để cảnh gọi được
    budget() { return null; }, contrast() { return []; }, roles() { return []; }, log: { cards: 0, overflow: [], leaders: [] },
  };
}

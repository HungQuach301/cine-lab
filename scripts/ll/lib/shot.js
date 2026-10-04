// Last Lamplighters · thư viện mẫu — dựng một đoạn từ đặc tả (window.SPEC do render.js nạp từ timeline của ll.py).
// SPEC = { frames, shots: [{ tpl, t0, t1, in: { type: 'slide'|'flip'|'fade'|'cut', d }, p }], hook?, blur? }
// Chuyển cảnh có chủ ý (CHUAN-KENH §5.1): hai tấm giấy → trượt hoặc lật giấy; có cảnh toàn khung → hoà qua.
// Shorts (LL.fmt = '9x16'): hook = dòng chữ trên đầu khung (ngoài tấm giấy), luôn trong vùng an toàn.
'use strict';
(() => {
  const S = window.SPEC, shots = S.shots.map((s) => Object.assign({}, s, { T: TPL[s.tpl](Object.assign({ t0: s.t0, t1: s.t1 }, s.p)) }));
  const off = document.createElement('canvas'); off.width = W; off.height = H; const OX = off.getContext('2d');
  const cardOf = (s, t, extra = {}) => Object.assign({ seed: 11 + shots.indexOf(s) * 7, content: (g, tt, w, h) => s.T.content(g, tt, w, h),
    scale: 1 + 0.025 * sm(pr(t, s.t0, s.t1)), ph: shots.indexOf(s) * 1.7 }, extra);
  const one = (g, s, t, extra) => { if (s.T.kind === 'full') { g.save(); s.T.full(g, t); g.restore(); } else desk(g, t, [cardOf(s, t, extra)]); };
  function hook(g, t) { if (!S.hook) return; const a = rv(t, 0.15, 0.6); g.save(); g.fillStyle = 'rgba(20,26,46,0.0)';
    const L = wrap(g, S.hook, W - 160, 52); L.forEach((l, i) => text(g, l, W / 2, 120 + i * 64, 52, CREAM, { align: 'center', kind: 'serif', a })); g.restore(); }
  LL.SEG = { frames: S.frames, blur: S.blur || shots.flatMap((s) => s.T.blur || []), fadeIn: S.fadeIn, fadeOut: S.fadeOut, frame(g, t) {
    let i = shots.findIndex((s) => t >= s.t0 && t < s.t1); if (i < 0) i = t < shots[0].t0 ? 0 : shots.length - 1;
    const s = shots[i], tr = s.in || { type: 'cut' }, d = tr.d || 0.7, u = i > 0 && tr.type !== 'cut' ? pr(t, s.t0, s.t0 + d) : 1;
    if (u < 1) { LL.act = true; const q = shots[i - 1], e = sm(u), keep0 = LL.tlog; LL.tlog = null;
      if (tr.type === 'slide' && s.T.kind === 'card' && q.T.kind === 'card') {
        g.drawImage(BG, 0, 0); const sx = LL.fmt === '9x16' ? W : W * 0.9;
        drawCard(g, t, cardOf(q, t, { dx: -sx * 0.35 * e, alpha: 1 - 0.6 * e })); drawCard(g, t, cardOf(s, t, { dx: sx * (1 - e), tilt: 0.02 * (1 - e) })); drawLight(g, t, 1); drawDust(g, t, 1); }
      else if (tr.type === 'flip' && s.T.kind === 'card' && q.T.kind === 'card') {
        g.drawImage(BG, 0, 0); if (e < 0.5) drawCard(g, t, cardOf(q, t, { flipU: 1 - e * 2 })); else drawCard(g, t, cardOf(s, t, { flipU: e * 2 - 1 })); drawLight(g, t, 1); drawDust(g, t, 1); }
      else { one(g, q, t); OX.setTransform(1, 0, 0, 1, 0, 0); OX.globalAlpha = 1; OX.globalCompositeOperation = 'source-over'; one(OX, s, t); g.save(); g.globalAlpha = e; g.drawImage(off, 0, 0); g.restore(); }
      LL.tlog = keep0;
    } else one(g, s, t);
    if (LL.fmt === '9x16' && s.tpl !== 'endcard') hook(g, t);
  } };
})();

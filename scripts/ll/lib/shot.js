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
  // chú thích đè lên cảnh toàn khung (luật nhịp 05/10/2026: bớt thẻ giấy): p.cap = [{ s, at, num?/n?, kind? }] — hiện mục mới nhất, dải tối dưới đáy
  function caps(g, s, t) { const C = (s.p && s.p.cap) || []; let k = -1; C.forEach((c, i) => { if (t >= c.at) k = i; }); if (k < 0) return;
    const c = C[k], a = rv(t, c.at, 0.5), big = c.text !== undefined && c.text !== null, v = LL.fmt === '9x16';
    const y0 = H * (v ? 0.62 : 0.70); if (a > 0.05 && (LL.zones || []).some((z) => z[3] > y0 - 40 && z[1] < H && z[2] > 0 && z[0] < W)) LL.hit = 1; g.save(); const gr = g.createLinearGradient(0, y0 - 40, 0, H); gr.addColorStop(0, 'rgba(12,10,12,0)'); gr.addColorStop(0.35, `rgba(12,10,12,${0.78 * a})`); gr.addColorStop(1, `rgba(12,10,12,${0.88 * a})`);
    g.fillStyle = gr; g.fillRect(0, y0 - 40, W, H - y0 + 40); g.restore();
    const x = v ? W / 2 : 140, al = v ? 'center' : 'left';
    if (big) { text(g, c.text, x, y0 + (v ? 110 : 95), v ? 120 : 104, CREAM, { a, kind: 'serif', bold: true, align: al }); if (c.kind) tag(g, c.kind === 'projection' ? 'PROJECTION' : 'ACTUAL', v ? W / 2 - 80 : x, y0 + (v ? 150 : 130), v ? 30 : 24, 'rgba(243,236,218,0.95)', c.kind === 'projection' ? '#16253a' : INK, { a, dash: c.kind === 'projection', border: c.kind !== 'projection', align: 'left' }); }
    if (c.s) text(g, c.s, x, y0 + (big ? (v ? 230 : 200) : (v ? 120 : 110)), big ? (v ? 46 : 38) : (v ? 54 : 46), CREAM, { a, kind: big ? 'sans' : 'serif', align: al, bold: !big });
    const srcl = c.src || s.p.src; if (s.p.credit) text(g, s.p.credit, W - (v ? 60 : 80), H - (v ? 160 : 34), v ? 26 : 20, 'rgba(236,223,190,0.9)', { align: 'right', a }); /* ảnh tư liệu: dòng nguồn ảnh bên phải, nguồn số bên trái */ /* dải chú thích che dòng nguồn của mẫu → vẽ lại nguồn trên dải */ if (srcl) text(g, srcl, x, H - (v ? 120 : 34), v ? 30 : 20, 'rgba(236,223,190,0.85)', { a, align: al }); }
  const one = (g, s, t, extra) => { if (s.T.kind === 'full') { g.save(); s.T.full(g, t); g.restore(); caps(g, s, t); } else desk(g, t, [cardOf(s, t, extra)]); };
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

// Last Lamplighters · Thư viện HÌNH v2 — "số trong thế giới cắt giấy" (chủ dự án 05/10/2026, mục C1–C3). Dùng từ tập 6.
// Mọi mẫu ở đây là cảnh TOÀN KHUNG (kind 'full'): không tính vào tỷ lệ thẻ giấy (Q16); nhận chú thích đè `cap` như các cảnh khác.
// Cần: core.js, scenes.js (camOf, lay, fog), props.js (PROP, cut, worker, PAPER).

// "sống": bụi trong ánh đèn + hạt phim đổi theo từng khung, để cảnh không bao giờ đứng hình 2–12 khung khi máy quay chậm/dừng (qc Q1, tập 5)
function alive(g, t, a = 1) { drawDust(g, t, 0.7 * a); const f = Math.round(t * 24), R = rng(1 + (f % 997)); g.save(); g.globalAlpha = 0.035 * a; g.fillStyle = '#fff';
  for (let i = 0; i < 260; i++) g.fillRect(R() * W, R() * H, 2, 2); g.globalAlpha = 0.03 * a; g.fillStyle = '#000'; for (let i = 0; i < 260; i++) g.fillRect(R() * W, R() * H, 2, 2); g.restore(); }
// phông diorama chung: tường tối, sàn giấy, đèn ấm, bụi
function diorama(g, t, c, o = {}) {
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, o.top || '#1c1a26'); gr.addColorStop(1, o.bot || '#120e10'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  const Pw = lay(c, 3); for (let i = 0; i < 6; i++) { const [x0, y0] = Pw(-200 + i * 420, H * 0.08), [x1, y1] = Pw(-40 + i * 420, H * 0.6); g.fillStyle = 'rgba(90,80,90,0.16)'; g.fillRect(x0, y0, x1 - x0, y1 - y0); }
  const Pf = lay(c, 1.2), [fx0, fy0] = Pf(-200, H * (o.floor || 0.8)), [fx1] = Pf(W + 200, H);
  cut(g, (q) => { q.rect(fx0, fy0, fx1 - fx0, H - fy0 + 40); }, '#3a2a20', { blur: 20, edge: true });
  glow(g, W * 0.22, H * 0.1, H * 0.9, RGB_AMB, 0.16 + 0.02 * Math.sin(t * 1.3));
}
const fmtBig = (v, unit, d) => { if (d === undefined) d = Number.isInteger(Number(v)) ? 0 : 1; return unit === '%' ? `${v < 0 ? '−' : v > 0 ? '+' : ''}${Math.abs(v).toFixed(d)}%` : fmtN(v, d); };   // không làm tròn số lẻ (3,5 % không thành 4 %)
function lightTag(g, kind, x, y, px, a, align = 'left') {   // nhãn loại số trên nền tối
  tag(g, kind === 'projection' ? 'PROJECTION' : 'ACTUAL', x, y, px, 'rgba(243,236,218,0.95)', kind === 'projection' ? '#16253a' : INK, { a, dash: kind === 'projection', border: kind !== 'projection', align });
}
function v2Head(g, t, p) { if (p.title) text(g, p.title, 110, 96, 46, CREAM, { kind: 'serif', a: rvH(t, p.t0 + 0.1, 0.6) }); if (p.subtitle) text(g, p.subtitle, 110, 140, 26, 'rgba(236,223,190,0.85)', { a: rvH(t, p.t0 + 0.3, 0.6) });
  if (p.src) text(g, p.src, 110, H - 34, MINPX, 'rgba(236,223,190,0.88)', { a: rvH(t, p.t0 + 0.4, 0.6) }); }

// ---- isotype: hàng hình người, mỗi hình = p.unit người. p = { title, subtitle, unit, groups: [{ label, value/num, at, kind }], cam, src } ----
TPL.isotype = (p) => { const cam = camOf(p); return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); diorama(g, t, c);
  const G = p.groups || [], capOn = !!(p.cap && p.cap.length), span = (capOn ? H * 0.70 - 60 : H * 0.92) - 250, rowH = Math.min(220, span / Math.max(1, G.length)), per = p.per || 20;   // có chú thích: hàng hình dừng trên dải chú thích (lỗi lát cắt v2)
  G.forEach((gp, gi) => { const n = Math.max(1, Math.round(Math.abs(gp.value) / (p.unit || 1))), y = 250 + gi * rowH + rowH * 0.78, a0 = gp.at === undefined ? p.t0 + 0.5 : gp.at, proj = gp.kind === 'projection';
    const ha = rvH(t, a0 - 0.3, 0.4); text(g, gp.label || '', 110, y - rowH * 0.62, 30, CREAM, { a: ha });
    const step = Math.min(64, (W - 620) / per), h = Math.min(rowH * 0.62, step * 1.9);
    for (let k = 0; k < n; k++) { const col = k % per, rowk = Math.floor(k / per), a = rv(t, a0 + 0.04 * k, 0.35); if (a <= 0) continue;
      const x = 130 + col * step + rowk * step * 0.35, yy = y - rowk * h * 0.18, dy = (1 - eo(a)) * 24;
      g.save(); g.globalAlpha *= a;
      if (proj) { g.save(); person(g, x, yy + dy, h, { col: 'rgba(0,0,0,0)', rim: null }); g.restore(); g.strokeStyle = '#c9d6e6'; g.setLineDash([5, 4]); g.lineWidth = 2.2; g.beginPath(); g.arc(x, yy + dy - h * 0.92, h * 0.07, 0, 7); g.rect(x - h * 0.11, yy + dy - h * 0.83, h * 0.22, h * 0.5); g.stroke(); }
      else person(g, x, yy + dy, h, { col: gi % 2 ? PAPER.ochre : PAPER.cream, rim: null });
      g.restore(); LL.zones.push([x - h * 0.15, yy + dy - h, x + h * 0.15, yy + dy]); }
    const va = rv(t, a0 + 0.04 * n, 0.5); text(g, gp.text || fmtBig(gp.value, p.unitLabel), W - 110, y - rowH * 0.2, 72, CREAM, { kind: 'serif', a: va, align: 'right' }); if (gp.kind) lightTag(g, gp.kind, W - 110, y + 12, 22, va, 'right'); });
  if (p.unit) text(g, `each figure = ${fmtN(p.unit)} ${p.unitName || 'people'}`, W - 110, 140, 24, 'rgba(236,223,190,0.85)', { align: 'right', a: rvH(t, p.t0 + 0.5, 0.6) });
  v2Head(g, t, p); fog(g, H * 0.98, 0.12, '60,50,46'); alive(g, t); } }; };

// ---- stack: cột dựng bằng đồ vật (chồng hồ sơ, máy đánh chữ, ATM…). p = { title, obj, per, bars: [{ label, value/num, at, kind }], cam, src } ----
TPL.stack = (p) => { const cam = camOf(p); return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); diorama(g, t, c, { floor: 0.82 });
  const B = p.bars || [], P = lay(c, 1.25), obj = PROP[p.obj || 'files'], hgt = { files: 64, ledger: 36, typewriter: 140, atm: 150, terminal: 120, laptop: 86, phone: 84, car: 80, switchboard: 150 }[p.obj || 'files'] || 80, s = p.s || 0.9;
  B.forEach((b, i) => { const n = Math.max(1, Math.round(Math.abs(b.value) / (p.per || 1))), [x, y] = P(W * (i + 1) / (B.length + 1), H * 0.82), a0 = b.at === undefined ? p.t0 + 0.5 : b.at, proj = b.kind === 'projection';
    for (let k = 0; k < n; k++) { const a = rv(t, a0 + 0.12 * k, 0.4); if (a <= 0) continue; g.save(); g.globalAlpha *= (proj ? 0.55 : 1) * a; obj(g, x + ((k * 37) % 7 - 3), y - k * hgt * s * 0.98 - (1 - eo(a)) * 60, s, { glow: 1, lit: 0.5 }); g.restore(); }
    const top = y - n * hgt * s * 0.98, va = rv(t, a0 + 0.12 * n, 0.5);
    text(g, b.text || fmtBig(b.value, p.unit), x, top - 30, 64, CREAM, { kind: 'serif', align: 'center', a: va }); if (b.kind) lightTag(g, b.kind, x, top - 112, 20, va, 'center');
    text(g, b.label || '', x, y + 44, 28, CREAM, { align: 'center', a: rvH(t, a0 - 0.3, 0.4) }); }); alive(g, t);
  if (p.per) text(g, `each ${p.objName || ({ files: 'file stack', atm: 'ATM', typewriter: 'typewriter' })[p.obj] || 'item'} = ${p.unit === '%' ? p.per + ' points' : fmtN(p.per)} ${p.unitName || ''}`.trim(), W - 110, 140, 24, 'rgba(236,223,190,0.85)', { align: 'right', a: rvH(t, p.t0 + 0.5, 0.6) });
  v2Head(g, t, p); } }; };

// ---- sign: số sơn trên biển hiệu/tường nhà, đèn rọi. p = { value/num/text, caption, at, kind, cam, wall: 'brick'|'plaster', src } ----
TPL.sign = (p) => { const cam = camOf(p); return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z);
  sky(g, t, 0.4); const P = lay(c, 1.4), [x0, y0] = P(W * 0.12, H * 0.1), [x1, y1] = P(W * 0.88, H * 0.92);
  cut(g, (q) => q.rect(x0, y0, x1 - x0, y1 - y0), p.wall === 'plaster' ? '#5c4a3c' : '#5a2f22', { blur: 24 });
  if (p.wall !== 'plaster') { g.strokeStyle = 'rgba(20,10,8,0.35)'; g.lineWidth = 2; for (let yy = y0 + 24; yy < y1; yy += 24) { g.beginPath(); g.moveTo(x0, yy); g.lineTo(x1, yy); g.stroke(); } }
  const bx0 = lerp(x0, x1, 0.12), bx1 = lerp(x0, x1, 0.88), by0 = lerp(y0, y1, 0.16), by1 = lerp(y0, y1, 0.66), a = rv(t, p.at === undefined ? p.t0 + 0.6 : p.at, 1.4);
  cut(g, (q) => q.rect(bx0, by0, bx1 - bx0, by1 - by0), '#2b2a2e', { blur: 12 });
  glow(g, (bx0 + bx1) / 2, by0 - 40, (bx1 - bx0) * 0.6, RGB_AMB, 0.28 * Math.max(0.3, a));
  g.save(); g.beginPath(); g.rect(bx0, by0, (bx1 - bx0) * eo(a), by1 - by0); g.clip();   // "sơn" dần từ trái
  if (a > 0) text(g, p.text || fmtBig(p.value, p.unit, p.d), (bx0 + bx1) / 2, (by0 + by1) / 2 + 40, 180, '#f1e4c2', { kind: 'serif', align: 'center', a: Math.min(1, a * 1.5) }); g.restore();
  if (p.kind) lightTag(g, p.kind, bx0 + 30, by0 + 30, 26, a);
  if (p.caption) text(g, p.caption, (x0 + x1) / 2, lerp(y0, y1, 0.78), 40, CREAM, { align: 'center', a: rv(t, (p.capAt === undefined ? (p.at || p.t0) + 0.8 : p.capAt), 0.6) });
  for (const lx of [W * 0.05, W * 0.95]) { gasLampIcon(g, lx, H * 0.95, 2.2, 1, 1); }
  if (p.src) text(g, p.src, 110, H - 34, MINPX, 'rgba(236,223,190,0.88)', { a: rvH(t, p.t0 + 0.4, 0.6) }); fog(g, H, 0.15, '60,50,46'); alive(g, t); } }; };

// ---- desk: nhân vật vô danh ở bàn làm việc, đổi thời kỳ theo mốc. p = { eras: [{ era, at }], accent, cam, label: true } ----
TPL.desk = (p) => { const cam = camOf(p), E = p.eras || [{ era: 1950, at: p.t0 }]; return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); diorama(g, t, c, { floor: 0.78 });
  let k = 0; E.forEach((e, i) => { if (t >= e.at) k = i; }); const u = k > 0 ? rv(t, E[k].at, 0.8) : 1, P = lay(c, 1.3);
  const draw = (e, a) => { if (a <= 0) return; g.save(); g.globalAlpha *= a; const [x, y] = P(W * 0.5, H * 0.78), pr_ = PROP[(ERA[e.era] || {}).prop || 'typewriter'];
    // cửa sổ và thành phố theo thời kỳ
    const [wx0, wy0] = P(W * 0.62, H * 0.18), [wx1, wy1] = P(W * 0.86, H * 0.52); cut(g, (q) => q.rect(wx0, wy0, wx1 - wx0, wy1 - wy0), e.era >= 1988 ? '#24324a' : '#2c2a3a', { blur: 10 });
    const R = rng(e.era); for (let i = 0; i < 18; i++) { g.fillStyle = `rgba(255,${190 + 40 * R()},120,${0.5 * R()})`; g.fillRect(wx0 + 10 + R() * (wx1 - wx0 - 30), wy0 + 10 + R() * (wy1 - wy0 - 30), 8, 12); }
    worker(g, x - 60, y + 150, 560, { era: e.era, accent: p.accent, arm: 1.2 + 0.12 * Math.sin(t * 3.1), arm2: 1.0 + 0.12 * Math.sin(t * 2.7 + 1) });
    cut(g, (q) => q.rect(x - 260, y - 40, 520, 30), PAPER.brown, { blur: 14 }); cut(g, (q) => q.rect(x - 240, y - 10, 24, 140), PAPER.brown); cut(g, (q) => q.rect(x + 216, y - 10, 24, 140), PAPER.brown);
    pr_(g, x + 40, y - 40, 1.4, { lit: 0.5, glow: 1 }); glow(g, x - 160, y - 160, 260, RGB_AMB, 0.22);
    if (p.label !== false && String(e.label || e.era).trim()) text(g, String(e.label || e.era), W - 140, 120, 72, CREAM, { kind: 'serif', align: 'right', a: 1 });
    g.restore(); };
  if (u < 1) { draw(E[k - 1], 1 - u); } draw(E[k], u); fog(g, H * 0.98, 0.14, '60,50,46'); alive(g, t); } }; };

// ---- archive: ảnh tư liệu phạm vi công cộng (danh sách trắng), Ken Burns + phủ tông B3. p = { img, rid, credit, cam: [{t, x, z}], tone } ----
// Ảnh nạp sẵn vào window.IMGS bởi render.js. qc (rights_check.py) chặn nếu rid không có dòng RIGHTS hợp lệ.
TPL.archive = (p) => { const cam = camOf(p); return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); g.fillStyle = '#0e0c0e'; g.fillRect(0, 0, W, H);
  const im = (window.IMGS || {})[p.img]; LL.act = true;
  if (im) { const sc = Math.max(W / im.width, H / im.height) * (1.08 + c.z * 0.6), w = im.width * sc, h = im.height * sc, F = p.focus || [0.5, 0.45];   // focus: điểm chính của ảnh (tỷ lệ 0..1), đặt ở vùng trên dải chú thích
    const fy = (p.cap && p.cap.length) ? H * 0.38 : H * 0.48, x0 = Math.min(0, Math.max(W - w, W / 2 - F[0] * w + c.x * 0.6)), y0 = Math.min(0, Math.max(H - h, fy - F[1] * h)); g.save(); g.drawImage(im, x0, y0, w, h); g.restore();
    g.save(); g.globalCompositeOperation = 'color'; g.fillStyle = `rgba(150,110,70,${p.tone === undefined ? 0.85 : p.tone})`; g.fillRect(0, 0, W, H); g.restore();
    g.save(); g.globalCompositeOperation = 'multiply'; const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, 'rgba(60,70,110,0.55)'); gr.addColorStop(1, 'rgba(40,28,22,0.65)'); g.fillStyle = gr; g.fillRect(0, 0, W, H); g.restore();
    g.save(); g.globalAlpha = 0.18; g.drawImage(paper(W, H, 5).tex, 0, 0, W, H); g.restore(); }
  else text(g, `missing image ${p.img}`, W / 2, H / 2, 40, '#ff8080', { align: 'center' });
  const v = g.createRadialGradient(W / 2, H * 0.5, H * 0.3, W / 2, H * 0.5, H * 0.95); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.7)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
  alive(g, t, 1.4);
  if (p.credit && !(p.cap && p.cap.length)) { g.fillStyle = 'rgba(10,8,10,0.6)'; g.fillRect(W - 60 - measure(g, p.credit, 22) - 16, H - 58, measure(g, p.credit, 22) + 32, 40); text(g, p.credit, W - 60, H - 30, 22, CREAM, { align: 'right' }); } } }; };

// ---- inspect: giám định xe hỏng ngoài trời. p = { era: 1988|2025, flash: [t…] (chụp ảnh), estimate: t (2025: khung ước tính tự hiện trên điện thoại), amount: "$2,340", walk: [t0, t1], cam } ----
TPL.inspect = (p) => { const cam = camOf(p); return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z);
  sky(g, t, 0.35); const P2 = lay(c, 2.4); for (let i = 0; i < 6; i++) { const [x0, y0] = P2(-100 + i * 380, H * 0.28 - (i % 3) * 40), [x1] = P2(240 + i * 380, H); g.fillStyle = 'rgba(30,30,44,0.9)'; g.fillRect(x0, y0, x1 - x0, H * 0.5); }
  const Pf = lay(c, 1.2), [fx0, fy0] = Pf(-200, H * 0.8), [fx1] = Pf(W + 200, H); cut(g, (q) => q.rect(fx0, fy0, fx1 - fx0, H), '#2b2a30', { blur: 10 });
  const P = lay(c, 1.25), [cx, cy] = P(W * 0.42, H * 0.83); PROP.car(g, cx, cy, 2.6, { dent: true, color: '#56657a' });
  const w0 = (p.walk || [p.t0, p.t0 + 4])[0], w1 = (p.walk || [p.t0, p.t0 + 4])[1], u = sm(pr(t, w0, w1)); if (u > 0 && u < 1) LL.act = true;
  const [wx, wy] = P(lerp(W * 0.86, W * 0.72, u), H * 0.86), fl = Math.max(0, ...(p.flash || []).map((f) => (t >= f && t < f + 0.5) ? 1 - (t - f) / 0.5 : 0));
  if (fl > 0) LL.act = true;
  const r = worker(g, wx, wy, 360, { seated: false, era: p.era, accent: p.accent, step: 0.3 * Math.sin(t * 5) * (u > 0 && u < 1 ? 1 : 0), arm: 2.4, arm2: -0.3, flip: true });
  if (p.era >= 2025) { PROP.phone(g, r.hand[0] - 10, r.hand[1] + 30, 0.8); if (fl) glow(g, r.hand[0] - 10, r.hand[1] - 20, 200, '255,250,235', 0.6 * fl); }
  else PROP.camera(g, r.hand[0] - 10, r.hand[1] + 20, 0.9, { flash: fl });
  if (p.estimate !== undefined) { const a = rv(t, p.estimate, 0.8); if (a > 0) { const bx = W * 0.58, by = H * 0.18; g.save(); g.globalAlpha *= a;
    cut(g, (q) => rr(q, bx, by, 520, 230, 14), '#101a2a', { blur: 18 }); text(g, 'AUTOMATED ESTIMATE', bx + 30, by + 56, 26, '#9fc4ec', { a });
    text(g, p.amount || 'estimate ready', bx + 30, by + 140, 72, CREAM, { kind: 'serif', a }); text(g, 'from photos · draft for review', bx + 30, by + 196, 24, 'rgba(236,223,190,0.85)', { a }); g.restore(); } }
  fog(g, H * 0.98, 0.14, '60,50,60'); alive(g, t); } }; };

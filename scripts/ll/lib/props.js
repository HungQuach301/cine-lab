// Last Lamplighters · Thư viện HÌNH v2 — đạo cụ cắt giấy theo thời kỳ (chủ dự án 05/10/2026, mục C2). Dùng từ tập 6.
// Mỗi đạo cụ: PROP[tên](g, x, y, s, o) vẽ tại chân (x, y), cao ≈ 100·s px; phong cách cắt giấy: mảng màu phẳng, viền sáng mép trên, bóng đổ mềm, lay rất nhẹ.
// Bảng màu giấy: kem, đất son, nâu, xám xanh, mực — cùng hệ B3.
const PAPER = { cream: '#e9dcb8', ochre: '#b9783a', brown: '#6b4426', slate: '#46566e', ink: '#221b17', rust: '#8a4a2a', sage: '#7d8a6a', steel: '#8d9aa6' };
function cut(g, draw, fill, o = {}) {   // một mảnh giấy: bóng đổ + mảng + viền sáng
  g.save(); g.shadowColor = 'rgba(0,0,0,0.55)'; g.shadowBlur = o.blur === undefined ? 14 : o.blur; g.shadowOffsetX = 5; g.shadowOffsetY = 8;
  g.beginPath(); draw(g); g.fillStyle = fill; g.fill(); g.restore();
  if (o.edge !== false) { g.save(); g.beginPath(); draw(g); g.clip(); g.strokeStyle = 'rgba(255,245,220,0.35)'; g.lineWidth = 3; g.beginPath(); draw(g); g.stroke(); g.restore(); }
}
const rr = (g, x, y, w, h, r = 6) => { g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
const PROP = {
  typewriter(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => rr(q, -60, -58, 120, 58, 8), PAPER.ink); cut(g, (q) => rr(q, -48, -96, 96, 40, 6), PAPER.slate, { blur: 8 });
    cut(g, (q) => rr(q, -70, -104, 140, 10, 4), PAPER.steel, { blur: 6 });   // trục giấy
    cut(g, (q) => { q.moveTo(-34, -104); q.lineTo(34, -104); q.lineTo(30, -140); q.lineTo(-30, -140); q.closePath(); }, PAPER.cream, { blur: 6 });   // tờ giấy
    g.fillStyle = PAPER.cream; for (let r = 0; r < 3; r++) for (let k = 0; k < 9 - r; k++) { g.beginPath(); g.arc(-44 + r * 5 + k * 11, -42 + r * 11, 3.4, 0, 7); g.fill(); }
    g.restore(); },
  terminal(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => rr(q, -56, -120, 112, 86, 10), PAPER.cream); cut(g, (q) => rr(q, -44, -110, 88, 62, 4), '#1f3324', { edge: false, blur: 0 });
    g.fillStyle = '#9fe0a8'; for (let i = 0; i < 4; i++) g.fillRect(-36, -100 + i * 12, 40 + 18 * Math.sin(i * 2.3), 4);
    cut(g, (q) => rr(q, -64, -26, 128, 24, 5), PAPER.cream); g.restore(); },
  laptop(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => { q.moveTo(-58, -86); q.lineTo(58, -86); q.lineTo(52, -14); q.lineTo(-52, -14); q.closePath(); }, PAPER.steel); cut(g, (q) => rr(q, -48, -80, 96, 58, 3), '#1a2a40', { edge: false, blur: 0 });
    cut(g, (q) => { q.moveTo(-70, -14); q.lineTo(70, -14); q.lineTo(78, 0); q.lineTo(-78, 0); q.closePath(); }, PAPER.steel); g.restore(); },
  ledger(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => rr(q, -62, -20, 124, 20, 3), PAPER.rust); cut(g, (q) => rr(q, -58, -36, 116, 18, 3), PAPER.cream, { blur: 4 });
    g.strokeStyle = 'rgba(80,50,30,0.5)'; g.lineWidth = 1.5; for (let i = 0; i < 5; i++) { g.beginPath(); g.moveTo(-52, -32 + i * 3); g.lineTo(52, -32 + i * 3); g.stroke(); } g.restore(); },
  files(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);   // một chồng hồ sơ
    for (let i = 0; i < 4; i++) cut(g, (q) => rr(q, -52 + (i % 2) * 4, -18 - i * 16, 104, 16, 3), i % 2 ? PAPER.ochre : PAPER.cream, { blur: 5 }); g.restore(); },
  atm(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => rr(q, -46, -150, 92, 150, 8), PAPER.slate); cut(g, (q) => rr(q, -34, -134, 68, 46, 4), '#0c1a2b', { edge: false, blur: 0 });
    if (o.glow) glow(g, 0, -111, 70, '120,170,230', 0.25 * o.glow);
    cut(g, (q) => rr(q, -30, -74, 60, 26, 3), PAPER.steel, { blur: 4 }); cut(g, (q) => rr(q, -24, -38, 48, 6, 2), PAPER.ink, { blur: 0 }); g.restore(); },
  counter(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => rr(q, -90, -70, 180, 70, 4), PAPER.brown); cut(g, (q) => rr(q, -96, -78, 192, 10, 3), PAPER.ochre, { blur: 6 });
    g.strokeStyle = 'rgba(30,20,12,0.85)'; g.lineWidth = 3; for (let i = 0; i < 7; i++) { g.beginPath(); g.moveTo(-72 + i * 24, -78); g.lineTo(-72 + i * 24, -150); g.stroke(); } g.restore(); },
  switchboard(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s);
    cut(g, (q) => rr(q, -70, -150, 140, 150, 6), PAPER.brown); const R = rng(77);
    for (let i = 0; i < 30; i++) { const lit = R() < (o.lit === undefined ? 0.4 : o.lit); g.fillStyle = lit ? '#ffcf7a' : '#2a1d14'; g.beginPath(); g.arc(-56 + (i % 6) * 22, -134 + Math.floor(i / 6) * 22, 5, 0, 7); g.fill(); }
    g.restore(); },
  car(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s);   // xe con thập niên 2020, có vết móp (claims)
    cut(g, (q) => { q.moveTo(-110, -18); q.lineTo(-104, -44); q.lineTo(-60, -50); q.lineTo(-34, -78); q.lineTo(40, -78); q.lineTo(70, -50); q.lineTo(108, -44); q.lineTo(112, -18); q.closePath(); }, o.color || PAPER.slate);
    cut(g, (q) => { q.moveTo(-28, -72); q.lineTo(-4, -72); q.lineTo(-4, -52); q.lineTo(-48, -52); q.closePath(); q.moveTo(4, -72); q.lineTo(36, -72); q.lineTo(58, -52); q.lineTo(4, -52); q.closePath(); }, '#9fb3c8', { blur: 0 });
    if (o.dent) { g.strokeStyle = PAPER.ink; g.lineWidth = 3; g.beginPath(); g.moveTo(70, -40); g.lineTo(82, -30); g.lineTo(76, -22); g.lineTo(90, -16); g.stroke(); }
    for (const wx of [-66, 66]) cut(g, (q) => q.arc(wx, -14, 18, 0, 7), PAPER.ink, { blur: 4 }); g.restore(); },
  phone(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s); cut(g, (q) => rr(q, -22, -84, 44, 84, 7), PAPER.ink); cut(g, (q) => rr(q, -18, -78, 36, 66, 3), '#1a2a40', { edge: false, blur: 0 }); g.restore(); },
};
// nhân vật vô danh xuyên suốt tập ("người làm nghề"): bóng người + khăn quàng màu nhấn cố định để nhận ra qua các thời kỳ; era chọn đạo cụ và mũ
const ERA = { 1900: { hat: 'bowler', prop: 'ledger' }, 1920: { hat: 'cap', prop: 'typewriter' }, 1950: { prop: 'typewriter' }, 1965: { prop: 'switchboard' }, 1975: { prop: 'counter' }, 1988: { prop: 'terminal' }, 2025: { prop: 'laptop' } };
function worker(g, x, y, h, o = {}) {
  const e = ERA[o.era] || {}; const r = person(g, x, y, h, Object.assign({ seated: o.seated !== false, hat: o.hat === undefined ? e.hat : o.hat, col: '#120e0f', rim: 'rgba(255,200,140,0.75)', armLen: 0.8, arm: 0.6, arm2: -0.55 }, o));
  const k = h / 170, acc = o.accent || '#b6462c';   // khăn quàng: dấu nhận diện cố định của nhân vật
  g.save(); g.fillStyle = acc; g.beginPath(); g.ellipse(x, y - 142 * k, 15 * k, 5 * k, 0, 0, 7); g.fill(); g.fillRect(x + 4 * k, y - 142 * k, 6 * k, 22 * k); g.restore();
  return r;
}

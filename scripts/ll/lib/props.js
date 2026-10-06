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
  camera(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s);   // máy ảnh của giám định viên (1980s: máy phim; 2025: điện thoại — dùng PROP.phone)
    cut(g, (q) => rr(q, -40, -52, 80, 52, 6), PAPER.ink); cut(g, (q) => rr(q, -14, -62, 28, 12, 3), PAPER.ink, { blur: 4 }); cut(g, (q) => q.arc(0, -26, 17, 0, 7), PAPER.steel, { blur: 4 });
    g.fillStyle = '#1a2a40'; g.beginPath(); g.arc(0, -26, 10, 0, 7); g.fill(); if (o.flash) glow(g, 22, -50, 160, '255,250,235', 0.7 * o.flash); g.restore(); },
  claimform(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s);   // hồ sơ bồi thường: bìa kẹp + mẫu đơn có ô
    cut(g, (q) => rr(q, -46, -128, 92, 128, 4), PAPER.ochre); cut(g, (q) => rr(q, -40, -120, 80, 114, 2), PAPER.cream, { blur: 4 });
    g.strokeStyle = 'rgba(60,40,25,0.6)'; g.lineWidth = 2; for (let i = 0; i < 6; i++) { g.strokeRect(-32, -110 + i * 17, 14, 11); g.beginPath(); g.moveTo(-12, -104 + i * 17); g.lineTo(30, -104 + i * 17); g.stroke(); }
    if (o.stamp) { g.save(); g.globalAlpha *= o.stamp; g.strokeStyle = '#8a2a1a'; g.lineWidth = 4; g.strokeRect(-20, -46, 52, 26); g.fillStyle = '#8a2a1a'; g.font = 'bold 15px "DejaVu Sans"'; g.fillText('PAID', -12, -27); g.restore(); }
    cut(g, (q) => rr(q, -14, -134, 28, 12, 3), PAPER.steel, { blur: 3 }); g.restore(); },
  typecase(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);   // tập 6: khay chữ chì nghiêng + tay cầm sắp chữ (composing stick)
    cut(g, (q) => { q.moveTo(-96, 0); q.lineTo(96, 0); q.lineTo(84, -92); q.lineTo(-84, -92); q.closePath(); }, PAPER.brown);
    g.strokeStyle = 'rgba(30,18,10,0.9)'; g.lineWidth = 2; for (let r = 0; r < 4; r++) { const yy = -86 + r * 22, w = 84 + r * 3; g.beginPath(); g.moveTo(-w, yy); g.lineTo(w, yy); g.stroke(); for (let k = 0; k < 9; k++) { const xx = -w + (k * 2 * w) / 9; g.beginPath(); g.moveTo(xx, yy); g.lineTo(xx, yy + 22); g.stroke(); } }
    const R = rng(606); g.fillStyle = PAPER.steel; for (let i = 0; i < 70; i++) { const r = Math.floor(R() * 4), k = Math.floor(R() * 9), w = 84 + r * 3; g.fillRect(-w + (k * 2 * w) / 9 + 3 + R() * 12, -82 + r * 22 + R() * 12, 3, 4); }
    cut(g, (q) => rr(q, 30, -118, 76, 14, 3), PAPER.steel, { blur: 6 }); g.fillStyle = PAPER.ink; for (let k = 0; k < 9; k++) g.fillRect(36 + k * 7, -116, 4, 10);   // tay cầm sắp chữ, một dòng chữ đang xếp
    g.restore(); },
  drawboard(g, x, y, s, o = {}) { g.save(); g.translate(x, y); g.scale(s, s);   // tập 6: bàn vẽ nghiêng + tờ vẽ + đèn kẹp
    cut(g, (q) => { q.moveTo(-8, 0); q.lineTo(8, 0); q.lineTo(4, -40); q.lineTo(-4, -40); q.closePath(); }, PAPER.ink, { blur: 4 });
    cut(g, (q) => { q.moveTo(-100, -36); q.lineTo(100, -36); q.lineTo(80, -136); q.lineTo(-80, -136); q.closePath(); }, PAPER.sage);
    cut(g, (q) => { q.moveTo(-70, -46); q.lineTo(64, -46); q.lineTo(50, -122); q.lineTo(-56, -122); q.closePath(); }, PAPER.cream, { blur: 4 });
    g.strokeStyle = 'rgba(40,30,25,0.75)'; g.lineWidth = 2; g.beginPath(); g.moveTo(-40, -60); g.quadraticCurveTo(-6, -118, 30, -70); g.stroke(); g.strokeRect(-30, -104, 34, 22);   // bản phác
    cut(g, (q) => rr(q, -100, -42, 200, 6, 2), PAPER.steel, { blur: 3 });   // thước trượt
    g.strokeStyle = PAPER.ink; g.lineWidth = 4; g.beginPath(); g.moveTo(92, -40); g.lineTo(104, -150); g.lineTo(56, -176); g.stroke();   // tay đèn kẹp
    cut(g, (q) => { q.moveTo(40, -186); q.lineTo(72, -186); q.lineTo(64, -166); q.lineTo(48, -166); q.closePath(); }, PAPER.ochre, { blur: 4 }); glow(g, 56, -150, 120, '255,214,150', 0.32);
    g.restore(); },
  calculator(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);   // tập 7: máy tính cơ (kiểu Friden/Marchant) + giấy kẻ ô
    cut(g, (q) => rr(q, -100, -14, 76, 14, 2), PAPER.cream, { blur: 3 }); g.strokeStyle = 'rgba(70,90,110,0.5)'; g.lineWidth = 1; for (let i = 0; i < 8; i++) { g.beginPath(); g.moveTo(-98 + i * 10, -14); g.lineTo(-98 + i * 10, 0); g.stroke(); }
    cut(g, (q) => { q.moveTo(-14, 0); q.lineTo(96, 0); q.lineTo(88, -62); q.lineTo(-6, -62); q.closePath(); }, PAPER.slate);
    cut(g, (q) => rr(q, -18, -86, 120, 22, 5), PAPER.steel, { blur: 6 });   // xe chạy số
    g.fillStyle = PAPER.cream; for (let k = 0; k < 10; k++) g.fillRect(-8 + k * 11, -80, 6, 9);
    for (let r = 0; r < 4; r++) for (let k = 0; k < 8; k++) { g.fillStyle = r === 3 ? PAPER.ochre : PAPER.cream; g.beginPath(); g.arc(4 + k * 10.5 - r * 1.5, -52 + r * 11, 3.3, 0, 7); g.fill(); }
    g.restore(); },
  dictionary(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s);   // tập 8: chồng từ điển + tờ bản dịch
    cut(g, (q) => rr(q, -96, -24, 88, 24, 3), PAPER.rust); cut(g, (q) => rr(q, -90, -46, 78, 22, 3), PAPER.slate); cut(g, (q) => rr(q, -94, -64, 84, 18, 3), PAPER.sage);
    g.fillStyle = 'rgba(240,225,190,0.8)'; for (const [yy, w] of [[-14, 50], [-36, 44], [-56, 46]]) g.fillRect(-80, yy, w, 3);   // gáy sách
    cut(g, (q) => { q.moveTo(4, 0); q.lineTo(96, 0); q.lineTo(90, -92); q.lineTo(10, -92); q.closePath(); }, PAPER.cream, { blur: 5 });
    g.strokeStyle = 'rgba(60,45,35,0.55)'; g.lineWidth = 2; for (let i = 0; i < 8; i++) { g.beginPath(); g.moveTo(18, -80 + i * 10); g.lineTo(18 + 60 + 8 * Math.sin(i * 1.7), -80 + i * 10); g.stroke(); }
    g.restore(); },
  phone(g, x, y, s) { g.save(); g.translate(x, y); g.scale(s, s); cut(g, (q) => rr(q, -22, -84, 44, 84, 7), PAPER.ink); cut(g, (q) => rr(q, -18, -78, 36, 66, 3), '#1a2a40', { edge: false, blur: 0 }); g.restore(); },
};
// nhân vật vô danh xuyên suốt tập ("người làm nghề"): bóng người + khăn quàng màu nhấn cố định để nhận ra qua các thời kỳ; era chọn đạo cụ và mũ
const ERA = { 1900: { hat: 'bowler', prop: 'ledger' }, 1920: { hat: 'cap', prop: 'typewriter' }, 1950: { prop: 'typewriter' }, 1963: { prop: 'claimform' }, 1965: { prop: 'switchboard' }, 1975: { prop: 'counter' }, 1988: { prop: 'terminal' }, 1942: { prop: 'typecase' }, 1960: { prop: 'drawboard' }, 1944: { prop: 'calculator' }, 1962: { prop: 'dictionary' }, 2025: { prop: 'laptop' } };
function worker(g, x, y, h, o = {}) {
  const e = ERA[o.era] || {}; const r = person(g, x, y, h, Object.assign({ seated: o.seated !== false, hat: o.hat === undefined ? e.hat : o.hat, col: '#120e0f', rim: 'rgba(255,200,140,0.75)', armLen: 0.8, arm: 0.6, arm2: -0.55 }, o));
  const k = h / 170, acc = o.accent || '#b6462c';   // khăn quàng: dấu nhận diện cố định của nhân vật
  g.save(); g.fillStyle = acc; g.beginPath(); g.ellipse(x, y - 142 * k, 15 * k, 5 * k, 0, 0, 7); g.fill(); g.fillRect(x + 4 * k, y - 142 * k, 6 * k, 22 * k); g.restore();
  return r;
}

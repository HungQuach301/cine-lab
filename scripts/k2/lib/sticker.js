// KÊNH 2 · STICKER (phiên V2, 14/10/2026) — một phong cách cho mọi sticker: viền trắng dày + bóng đổ mềm lệch xuống phải.
// Dùng chung: builder thư viện (scripts/k2/stickers_build.js → design/k2v/stickers/*.png) và lớp 2D (scripts/k2/lib/k2.js, p.stickers).
// Nhân vật A-lite: 8 vai phẳng, KHÔNG mặt chi tiết, không diễn xuất, không khớp miệng; nhận ra bằng 1–2 đạo cụ thay được (mũ + vật cầm tay).
//   STK.char({role, hat, hand, coat, pants}, px) → canvas thô (chưa viền), chân ở đáy giữa; STK.style(canvas) → canvas có viền + bóng.
'use strict';
(function () {
  const STK = window.STK = window.STK || {};
  const SKIN = '#E2B08A', SHOE = '#2a221c', INK = '#1d1914';
  // màu theo nhận diện kênh (channel-k2/NHAN-DIEN.md) + tông đất trung tính cho trang phục
  STK.ROLES = {
    worker:   { coat: '#5f7f9c', pants: '#3b4552', hat: 'cap',      hand: 'pickaxe',   acc: 'apron' },
    merchant: { coat: '#8a5a3c', pants: '#4a3a30', hat: 'bowler',   hand: 'sack',      acc: 'vest' },
    banker:   { coat: '#2f3742', pants: '#262c34', hat: 'tophat',   hand: 'moneybag',  acc: 'tie' },
    soldier:  { coat: '#4b5a3c', pants: '#39432f', hat: 'kepi',     hand: 'rifle',     acc: 'crossbelt' },
    official: { coat: '#3d4a6b', pants: '#2c3446', hat: 'none',     hand: 'scroll',    acc: 'sash' },
    engineer: { coat: '#b9874a', pants: '#4a4238', hat: 'wide',     hand: 'blueprint', acc: 'toolbelt' },
    farmer:   { coat: '#c79a4a', pants: '#5a6b7c', hat: 'straw',    hand: 'pitchfork', acc: 'suspenders' },
    sailor:   { coat: '#e9e4d8', pants: '#2f4a6b', hat: 'sailor',   hand: 'oar',       acc: 'stripes' },
  };
  STK.HATS = ['none', 'cap', 'bowler', 'tophat', 'kepi', 'wide', 'straw', 'sailor', 'hardhat', 'tricorn'];
  STK.HANDS = ['none', 'pickaxe', 'shovel', 'sack', 'moneybag', 'ledger', 'rifle', 'scroll', 'blueprint', 'pitchfork', 'wheat', 'oar', 'rope', 'lantern', 'flag', 'coin', 'torch'];
  const shade = (hex, k) => { const n = parseInt(hex.slice(1), 16); let r = n >> 16, g = (n >> 8) & 255, b = n & 255; const f = (v) => Math.max(0, Math.min(255, Math.round(k < 0 ? v * (1 + k) : v + (255 - v) * k))); return `rgb(${f(r)},${f(g)},${f(b)})`; };
  const rr = (g, x, y, w, h, r) => { g.beginPath(); g.roundRect(x, y, w, h, r); };
  const cap = (g, x0, y0, x1, y1, w) => { g.lineCap = 'round'; g.lineWidth = w; g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke(); };
  // ---- đạo cụ cầm tay (toạ độ đơn vị: thân cao 100, gốc ở giữa đáy, y hướng xuống; tay phải ở (21, 57))
  const HAND = {
    pickaxe(g, back) { if (back) return; g.strokeStyle = '#7a5532'; cap(g, 22, 70, 31, 26, 3.4); g.fillStyle = '#8d96a0'; g.beginPath(); g.moveTo(16, 24); g.quadraticCurveTo(31, 17, 45, 27); g.quadraticCurveTo(31, 22, 17, 28); g.fill(); },
    shovel(g, back) { if (back) return; g.strokeStyle = '#7a5532'; cap(g, 21, 66, 26, 22, 3.2); g.fillStyle = '#8d96a0'; rr(g, 15, 64, 18, 20, 5); g.fill(); },
    sack(g, back) { if (back) return; g.fillStyle = '#d8c39a'; g.beginPath(); g.ellipse(25, 64, 10, 12, 0.15, 0, 7); g.fill(); g.fillStyle = '#bba57a'; g.beginPath(); g.ellipse(28, 66, 6, 10, 0.15, 0, 7); g.fill(); g.strokeStyle = '#8a744c'; cap(g, 19, 53, 29, 52, 2.2); },
    moneybag(g, back) { if (back) return; g.fillStyle = '#c9a24a'; g.beginPath(); g.ellipse(24, 67, 10, 11, 0, 0, 7); g.fill(); g.fillStyle = '#a8842f'; rr(g, 20, 54, 8, 5, 2); g.fill(); g.fillStyle = '#5b4518'; g.font = '700 13px Inter, sans-serif'; g.textAlign = 'center'; g.fillText('$', 24, 72); },
    ledger(g, back) { if (back) return; g.fillStyle = '#7a3b2e'; rr(g, 14, 48, 16, 20, 2); g.fill(); g.fillStyle = '#efe6d2'; g.fillRect(28, 50, 2.5, 16); },
    rifle(g, back) { if (!back) return; g.strokeStyle = '#5a3e26'; cap(g, 15, 58, 4, 4, 3.6); g.strokeStyle = '#3c4148'; cap(g, 7, 18, 1, -6, 2.2); },
    scroll(g, back) { if (back) return; g.fillStyle = '#efe2c0'; rr(g, 15, 46, 9, 26, 3); g.fill(); g.fillStyle = '#d9c79c'; g.beginPath(); g.ellipse(19.5, 46, 4.5, 2.2, 0, 0, 7); g.fill(); g.fillStyle = '#b3322a'; g.beginPath(); g.arc(23, 63, 2.6, 0, 7); g.fill(); },
    blueprint(g, back) { if (back) return; g.save(); g.translate(22, 58); g.rotate(-0.6); g.fillStyle = '#3f74b8'; rr(g, -4, -20, 8, 34, 3); g.fill(); g.fillStyle = '#8fb3e0'; g.beginPath(); g.ellipse(0, -20, 4, 2, 0, 0, 7); g.fill(); g.restore(); },
    pitchfork(g, back) { if (back) return; g.strokeStyle = '#7a5532'; cap(g, 22, 82, 25, 18, 3); g.strokeStyle = '#8d96a0'; g.lineWidth = 2; g.beginPath(); g.moveTo(19, 8); g.lineTo(19, 18); g.lineTo(31, 18); g.lineTo(31, 8); g.moveTo(25, 8); g.lineTo(25, 18); g.stroke(); },
    wheat(g, back) { if (back) return; g.strokeStyle = '#b48a2c'; g.lineWidth = 1.8; for (let k = -2; k <= 2; k++) { g.beginPath(); g.moveTo(22, 64); g.lineTo(22 + k * 3, 38); g.stroke(); g.fillStyle = '#d9b14a'; g.beginPath(); g.ellipse(22 + k * 3, 36, 2.2, 6, k * 0.12, 0, 7); g.fill(); } },
    oar(g, back) { if (back) return; g.strokeStyle = '#8a6238'; cap(g, 26, 14, 18, 92, 3); g.fillStyle = '#8a6238'; g.beginPath(); g.ellipse(17, 92, 4.5, 9, 0.1, 0, 7); g.fill(); },
    rope(g, back) { if (back) return; g.strokeStyle = '#b89a62'; g.lineWidth = 2.6; for (let k = 0; k < 3; k++) { g.beginPath(); g.ellipse(25, 66, 9 - k * 2.3, 6 - k * 1.5, 0, 0, 7); g.stroke(); } },
    torch(g, back) { if (back) return; g.strokeStyle = '#3c4148'; cap(g, 22, 60, 30, 70, 2.2); g.fillStyle = '#5b6470'; rr(g, 18, 56, 7, 9, 2); g.fill(); g.fillStyle = '#ffd36a'; g.beginPath(); g.arc(31.5, 71.5, 2.6, 0, Math.PI * 2); g.fill(); g.fillStyle = '#ffffff'; g.beginPath(); g.arc(31.5, 71.5, 1.2, 0, Math.PI * 2); g.fill(); },   /* T2: mỏ hàn (thợ hàn Liberty, chương 03) */
    lantern(g, back) { if (back) return; g.strokeStyle = '#3c4148'; cap(g, 22, 58, 22, 64, 1.6); g.fillStyle = '#3c4148'; rr(g, 17, 64, 10, 13, 2); g.fill(); g.fillStyle = '#ffc95a'; rr(g, 19, 66, 6, 9, 1.5); g.fill(); },
    flag(g, back) { if (back) return; g.strokeStyle = '#6b5a48'; cap(g, 22, 70, 22, 6, 2.4); g.fillStyle = '#ece6d6'; g.beginPath(); g.moveTo(23, 7); g.quadraticCurveTo(33, 3, 43, 8); g.lineTo(43, 24); g.quadraticCurveTo(33, 19, 23, 23); g.fill(); },
    coin(g, back) { if (back) return; g.fillStyle = '#d9a640'; g.beginPath(); g.arc(25, 54, 8, 0, 7); g.fill(); g.strokeStyle = '#a8792a'; g.lineWidth = 1.6; g.beginPath(); g.arc(25, 54, 5.5, 0, 7); g.stroke(); },
    none() {},
  };
  // ---- mũ (đầu tâm (0, 19), r = 10.5)
  const HAT = {
    none(g, o) { g.fillStyle = o.hair || '#3b2c22'; g.beginPath(); g.arc(0, 18, 10.8, Math.PI * 1.02, Math.PI * 1.98); g.fill(); },
    cap(g) { g.fillStyle = '#4a4f57'; g.beginPath(); g.ellipse(0, 11, 11.5, 5.5, 0, Math.PI, 0); g.fill(); rr(g, -2, 9.5, 16, 3.4, 1.6); g.fill(); },
    bowler(g) { g.fillStyle = '#2d2622'; g.beginPath(); g.ellipse(0, 10.5, 9, 7.5, 0, Math.PI, 0); g.fill(); rr(g, -13, 9.2, 26, 3.4, 1.7); g.fill(); },
    tophat(g) { g.fillStyle = '#1e1f24'; rr(g, -8, -6, 16, 17, 1.5); g.fill(); rr(g, -13, 9.5, 26, 3.2, 1.6); g.fill(); g.fillStyle = '#6b2f2a'; g.fillRect(-8, 6, 16, 2.6); },
    kepi(g) { g.fillStyle = '#3f4d33'; g.beginPath(); g.moveTo(-9, 11); g.lineTo(-7, 0); g.lineTo(8, 1); g.lineTo(9, 11); g.fill(); g.fillStyle = '#23272e'; rr(g, -2, 9.5, 15, 3, 1.5); g.fill(); g.fillStyle = '#c9a24a'; g.fillRect(-9, 8.6, 18, 1.4); },
    wide(g) { g.fillStyle = '#6b5032'; g.beginPath(); g.ellipse(0, 9.5, 8.5, 6.5, 0, Math.PI, 0); g.fill(); g.beginPath(); g.ellipse(0, 10.5, 16, 3.2, 0, 0, 7); g.fill(); },
    straw(g) { g.fillStyle = '#e1c46c'; g.beginPath(); g.ellipse(0, 9.5, 8, 6, 0, Math.PI, 0); g.fill(); g.beginPath(); g.ellipse(0, 10.8, 18, 3.6, 0, 0, 7); g.fill(); g.fillStyle = '#b3322a'; g.fillRect(-8, 7.6, 16, 1.8); },
    sailor(g) { g.fillStyle = '#f4f1ea'; g.beginPath(); g.ellipse(0, 9, 10.5, 5.5, 0, Math.PI, 0); g.fill(); rr(g, -11, 8, 22, 4, 2); g.fill(); g.fillStyle = '#2f4a6b'; g.fillRect(-10.5, 10.2, 21, 1.8); },
    hardhat(g) { g.fillStyle = '#F2C14E'; g.beginPath(); g.ellipse(0, 11, 11, 9, 0, Math.PI, 0); g.fill(); rr(g, -13, 9.6, 26, 3, 1.5); g.fill(); },
    tricorn(g) { g.fillStyle = '#26221e'; g.beginPath(); g.moveTo(-15, 10); g.quadraticCurveTo(0, -6, 15, 10); g.quadraticCurveTo(0, 5, -15, 10); g.fill(); },
  };
  const ACC = {
    apron(g) { g.fillStyle = '#8a6a4a'; rr(g, -11, 46, 22, 20, 3); g.fill(); },
    vest(g) { g.fillStyle = '#5a3a26'; g.beginPath(); g.moveTo(-6, 32); g.lineTo(0, 44); g.lineTo(6, 32); g.lineTo(9, 58); g.lineTo(-9, 58); g.fill(); },
    tie(g) { g.fillStyle = '#e8e2d6'; g.beginPath(); g.moveTo(-5, 31); g.lineTo(0, 42); g.lineTo(5, 31); g.fill(); g.fillStyle = '#6b2f2a'; g.beginPath(); g.moveTo(-1.6, 33); g.lineTo(1.6, 33); g.lineTo(2.4, 46); g.lineTo(0, 49); g.lineTo(-2.4, 46); g.fill(); },
    crossbelt(g) { g.strokeStyle = '#e8e2d6'; cap(g, -12, 33, 11, 60, 3); g.fillStyle = '#c9a24a'; g.beginPath(); g.arc(-1, 46, 2, 0, 7); g.fill(); },
    sash(g) { g.strokeStyle = '#b3322a'; cap(g, 13, 33, -11, 60, 4.5); },
    toolbelt(g) { g.fillStyle = '#4a3624'; g.fillRect(-14, 56, 28, 4.5); g.fillStyle = '#8d96a0'; g.fillRect(-10, 59, 3, 6); g.fillRect(6, 59, 2.4, 7); },
    suspenders(g) { g.strokeStyle = '#4a3624'; cap(g, -7, 32, -6, 62, 2.4); cap(g, 7, 32, 6, 62, 2.4); },
    stripes(g) { g.save(); g.beginPath(); g.moveTo(-15, 30); g.lineTo(15, 30); g.lineTo(17, 64); g.lineTo(-17, 64); g.clip(); g.fillStyle = '#2f4a6b'; for (let y = 36; y < 64; y += 6) g.fillRect(-18, y, 36, 2.6); g.restore(); g.fillStyle = '#2f4a6b'; g.beginPath(); g.moveTo(-9, 30); g.lineTo(0, 39); g.lineTo(9, 30); g.fill(); },
  };
  STK.char = function (spec, px) {
    const R = STK.ROLES[spec.role] || STK.ROLES.worker, o = Object.assign({}, R, spec), s = px / 112, cv = document.createElement('canvas');
    cv.width = Math.ceil(78 * s); cv.height = Math.ceil(112 * s); const g = cv.getContext('2d'); g.translate(cv.width / 2, cv.height - 3 * s); g.scale(s, s); g.translate(0, -100);
    const hand = HAND[o.hand] || HAND.none, hat = HAT[o.hat] || HAT.none;
    hand(g, true);
    // chân + giày
    g.fillStyle = o.pants; rr(g, -10.5, 62, 9.5, 34, 3.5); g.fill(); rr(g, 1, 62, 9.5, 34, 3.5); g.fill();
    g.fillStyle = SHOE; g.beginPath(); g.ellipse(-6.5, 97, 7, 3.6, 0, 0, 7); g.fill(); g.beginPath(); g.ellipse(6.8, 97, 7, 3.6, 0, 0, 7); g.fill();
    // tay trái (sau thân)
    g.strokeStyle = shade(o.coat, -0.12); cap(g, -14, 35, -19, 56, 8); g.fillStyle = SKIN; g.beginPath(); g.arc(-19.5, 58, 4, 0, 7); g.fill();
    // thân
    g.fillStyle = o.coat; g.beginPath(); g.moveTo(-14, 30); g.quadraticCurveTo(0, 26, 14, 30); g.lineTo(16.5, 64); g.quadraticCurveTo(0, 67, -16.5, 64); g.closePath(); g.fill();
    (ACC[o.acc] || (() => {}))(g);
    g.save(); g.beginPath(); g.moveTo(-14, 30); g.quadraticCurveTo(0, 26, 14, 30); g.lineTo(16.5, 64); g.quadraticCurveTo(0, 67, -16.5, 64); g.closePath(); g.clip(); g.fillStyle = 'rgba(0,0,0,0.13)'; g.fillRect(4, 20, 20, 50); g.fillStyle = 'rgba(255,255,255,0.10)'; g.fillRect(-18, 20, 7, 50); g.restore();
    // cổ + đầu (không mặt chi tiết)
    g.fillStyle = shade(SKIN, -0.12); g.fillRect(-3.5, 26, 7, 6); g.fillStyle = SKIN; g.beginPath(); g.arc(0, 18, 10.5, 0, 7); g.fill();
    g.fillStyle = 'rgba(0,0,0,0.10)'; g.beginPath(); g.arc(0, 18, 10.5, -1.2, 1.2); g.arc(-4, 18, 9, 1.0, -1.0, true); g.fill();
    hat(g, o);
    // tay phải + đạo cụ
    g.strokeStyle = o.coat; cap(g, 14, 35, 20, 55, 8); hand(g, false); g.fillStyle = SKIN; g.beginPath(); g.arc(21, 57, 4, 0, 7); g.fill();
    void INK; return cv;
  };
  // ---- phong cách chung: viền trắng (giãn alpha theo vòng tròn) + bóng đổ mềm. Đơn vị theo cỡ sticker (o = 7 % cạnh ngắn, tối thiểu 4 px).
  STK.style = function (src, opt = {}) {
    const m = Math.min(src.width, src.height), o = opt.o ?? Math.max(4, Math.round(m * 0.06)), pad = Math.ceil(o * 3.2), W = src.width + 2 * pad, H = src.height + 2 * pad;
    const sil = document.createElement('canvas'); sil.width = W; sil.height = H; const sg = sil.getContext('2d');
    for (let k = 0; k < 32; k++) { const a = k / 32 * Math.PI * 2; for (const f of [1, 0.6]) sg.drawImage(src, pad + Math.cos(a) * o * f, pad + Math.sin(a) * o * f); }
    sg.globalCompositeOperation = 'source-in'; sg.fillStyle = opt.edge || '#ffffff'; sg.fillRect(0, 0, W, H);
    const out = document.createElement('canvas'); out.width = W; out.height = H; const g = out.getContext('2d');
    const sh = document.createElement('canvas'); sh.width = W; sh.height = H; const hg = sh.getContext('2d'); hg.drawImage(sil, 0, 0); hg.globalCompositeOperation = 'source-in'; hg.fillStyle = 'rgba(10,12,16,1)'; hg.fillRect(0, 0, W, H);
    g.save(); g.globalAlpha = opt.sa ?? 0.38; g.filter = `blur(${Math.max(2, o * 0.9)}px)`; g.drawImage(sh, o * 0.55, o * 0.9); g.restore();
    g.drawImage(sil, 0, 0); g.drawImage(src, pad, pad); return out;
  };
  const CACHE = {};
  // sticker theo đặc tả: 'tên' (ảnh thư viện đã nạp ở window.IMGS['stk:tên']) hoặc {role, hat, hand, coat, pants} / 'role:<vai>'
  STK.get = function (spec, px) {
    const key = JSON.stringify(spec) + '@' + Math.round(px); if (CACHE[key]) return CACHE[key];
    let cv;
    if (typeof spec === 'string' && !spec.startsWith('role:')) { const im = (window.IMGS || {})['stk:' + spec.replace(/^stk:/, '')]; if (!im) return null; cv = im; }
    else { const sp = typeof spec === 'string' ? { role: spec.slice(5) } : spec; cv = STK.style(STK.char(sp, px * 0.84)); }
    return (CACHE[key] = cv);
  };
})();

// Last Lamplighters · Thư viện HÌNH v3 — mẫu cảnh vật chất mới (chủ dự án 06/10/2026, CHUAN-KENH §11.3: mỗi tập ≥ 3 bối cảnh/đạo cụ mới;
// Q29: số neo và danh từ chính có HÌNH VẬT CHẤT, không chỉ chữ). Mọi mẫu: cảnh toàn khung, máy quay (camOf), hạt/bụi alive() → không đứng hình.
// Tông màu theo hồi do mẫu tự chọn qua p.mood: 'sepia' | 'cold' | 'warm'.

const MOOD = { sepia: { bg: '#2a2018', lamp: '255,190,120', tint: 'rgba(150,110,70,0.35)' }, cold: { bg: '#121823', lamp: '150,185,255', tint: 'rgba(70,100,150,0.30)' }, warm: { bg: '#2a1d18', lamp: '255,180,110', tint: 'rgba(170,110,60,0.25)' } };
function moodWash(g, m) { g.save(); g.globalCompositeOperation = 'soft-light'; g.fillStyle = MOOD[m].tint; g.fillRect(0, 0, W, H); g.restore(); }
function vign(g, a = 0.65) { const v = g.createRadialGradient(W / 2, H * 0.5, H * 0.25, W / 2, H * 0.5, H * 0.95); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, `rgba(0,0,0,${a})`); g.fillStyle = v; g.fillRect(0, 0, W, H); }

// ---- jobboard: bảng ghim tin tuyển việc (thiết kế, minh hoạ, 3D…); từ p.drop, một tỷ lệ p.share tờ phai rồi rơi. p = { drop, share: 0.17, labels, mood, cam, cap }
TPL.jobboard = (p) => { const cam = camOf(p), R = rng(p.seed || 17), L = p.labels || ['LOGO', 'POSTER', 'BOOK COVER', 'ILLUSTRATION', '3D MODEL', 'PACKAGING', 'ICON SET', 'BANNER', 'MENU', 'FLYER', 'LABEL', 'T-SHIRT'];
  const cards = []; for (let r = 0; r < 4; r++) for (let c = 0; c < 7; c++) cards.push({ x: 0.13 + c * 0.125 + (R() - 0.5) * 0.02, y: 0.2 + r * 0.17 + (R() - 0.5) * 0.02, a: (R() - 0.5) * 0.12, s: L[(r * 7 + c) % L.length], col: ['#efe6cf', '#e9d9a8', '#d8e2e8', '#efd6c6'][Math.floor(R() * 4)], k: R(), pin: ['#b6462c', '#3d6b8c', '#c9a23a'][Math.floor(R() * 3)] });
  const order = cards.map((c, i) => [c.k, i]).sort((a, b) => a[0] - b[0]).map((x) => x[1]), nDrop = Math.round(cards.length * (p.share === undefined ? 0.17 : p.share));
  return { kind: 'full', full(g, t) { const c = cam(t), m = p.mood || 'cold'; LL.cam(1 - c.z); g.fillStyle = MOOD[m].bg; g.fillRect(0, 0, W, H);
    g.save(); g.translate(W / 2 + c.x * 0.5, H / 2); g.scale(1 + c.z, 1 + c.z); g.translate(-W / 2, -H / 2);
    const bx = W * 0.07, by = H * 0.1, bw = W * 0.86, bh = H * 0.74;   // khung bảng bần
    g.fillStyle = '#5b3d25'; g.fillRect(bx - 18, by - 18, bw + 36, bh + 36); g.fillStyle = '#a77b4f'; g.fillRect(bx, by, bw, bh);
    const RR = rng(5); g.fillStyle = 'rgba(70,45,25,0.35)'; for (let i = 0; i < 900; i++) g.fillRect(bx + RR() * bw, by + RR() * bh, 2, 2);
    const drop = p.drop === undefined ? p.t0 + 2 : p.drop;
    cards.forEach((cd, i) => { const rank = order.indexOf(i), gone = rank < nDrop, u = gone ? cl((t - drop - rank * 0.12) / 0.9) : 0; if (u >= 1) return;
      const x = bx + cd.x * bw, y = by + cd.y * bh + (gone ? ei(u) * H * 0.5 : 0), w = bw * 0.1, h = bh * 0.13;
      g.save(); g.globalAlpha *= (1 - u) * rv(t, p.t0 + 0.1 + i * 0.02, 0.4); g.translate(x, y); g.rotate(cd.a + (gone ? u * 0.8 : 0));
      g.shadowColor = 'rgba(0,0,0,0.45)'; g.shadowBlur = 10; g.shadowOffsetY = 5; g.fillStyle = cd.col; g.fillRect(-w / 2, -h / 2, w, h); g.shadowColor = 'transparent';
      g.fillStyle = 'rgba(40,30,25,0.85)'; g.font = font(17, 'sans'); g.textAlign = 'center'; g.fillText(cd.s, 0, -h * 0.12);
      g.fillStyle = 'rgba(60,50,45,0.4)'; for (let k = 0; k < 3; k++) g.fillRect(-w * 0.35, h * 0.08 + k * 11, w * (0.7 - k * 0.15), 4);
      g.fillStyle = cd.pin; g.beginPath(); g.arc(0, -h / 2 + 8, 6, 0, 7); g.fill(); g.restore(); });
    g.restore(); glow(g, W * 0.5, H * 0.05, W * 0.6, MOOD[m].lamp, 0.12); moodWash(g, m); vign(g); alive(g, t, 1); } }; };

// ---- filmstrip: phòng tối tráng ảnh, đèn đỏ an toàn; dải phim âm bản chạy ngang, từ p.fade các ô phim mờ dần (còn lại p.keep). p = { fade, keep: 0.11, cam, cap }
TPL.filmstrip = (p) => { const cam = camOf(p), R = rng(p.seed || 29), F = []; for (let i = 0; i < 22; i++) F.push({ k: R(), h: R() });
  return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); g.fillStyle = '#160807'; g.fillRect(0, 0, W, H);
    glow(g, W * 0.82, H * 0.1, W * 0.6, '255,60,40', 0.45); glow(g, W * 0.82, H * 0.1, W * 0.1, '255,120,90', 0.7); glow(g, W * 0.3, H * 0.45, W * 0.5, '255,90,70', 0.18);
    // khay tráng (dưới), dây phơi phim (trên)
    g.fillStyle = '#2a1110'; g.fillRect(W * 0.08, H * 0.74, W * 0.84, H * 0.16); g.fillStyle = 'rgba(255,60,40,0.12)'; g.fillRect(W * 0.1, H * 0.76, W * 0.8, H * 0.1);
    g.strokeStyle = 'rgba(200,120,110,0.5)'; g.lineWidth = 2; g.beginPath(); g.moveTo(0, H * 0.2); g.lineTo(W, H * 0.22); g.stroke();
    for (let i = 0; i < 6; i++) { const px = W * (0.08 + i * 0.15) + Math.sin(t * 0.7 + i) * 3, py = H * 0.2 + i * H * 0.004 + 6; g.save(); g.translate(px, py); g.rotate(Math.sin(t * 0.9 + i * 2) * 0.03);
      g.fillStyle = '#e8d8c8'; g.fillRect(-55, 6, 110, 80); g.fillStyle = 'rgba(70,40,35,0.6)'; g.fillRect(-48, 13, 96, 66); g.fillStyle = 'rgba(200,170,150,0.5)'; g.beginPath(); g.arc(-10 + i * 6, 44, 16, 0, 7); g.fill(); g.fillStyle = '#6a6e74'; g.fillRect(-8, -2, 16, 14); g.restore(); }
    const y = H * 0.42, fw = 170, fh = 120, x0 = W * 0.06 - ((t - p.t0) * 22) % (fw + 14) + c.x * 0.4, fade = p.fade === undefined ? p.t0 + 2 : p.fade, keep = p.keep === undefined ? 0.11 : p.keep;
    g.fillStyle = '#0b0605'; g.fillRect(0, y - 30, W, fh + 60);
    for (let i = 0; i < 14; i++) { const x = x0 + i * (fw + 14), f = F[i % F.length], gone = f.k > keep, u = gone ? cl((t - fade - f.k * 2.5) / 1.2) : 0;
      g.save(); g.globalAlpha *= 1 - 0.92 * u; const gr = g.createLinearGradient(x, y, x + fw, y + fh); gr.addColorStop(0, `rgba(${235 - f.h * 50},${185 - f.h * 50},${160},0.95)`); gr.addColorStop(1, 'rgba(150,95,85,0.95)');
      g.fillStyle = gr; g.fillRect(x, y, fw, fh); g.fillStyle = 'rgba(30,15,12,0.55)'; g.beginPath(); g.arc(x + fw * (0.3 + f.h * 0.4), y + fh * 0.45, 26 + f.h * 18, 0, 7); g.fill(); g.fillRect(x + fw * 0.15, y + fh * 0.7, fw * 0.7, 10); g.restore();
      g.fillStyle = 'rgba(230,200,180,0.55)'; for (let k = 0; k < 6; k++) { g.fillRect(x + 10 + k * 27, y - 22, 14, 10); g.fillRect(x + 10 + k * 27, y + fh + 12, 14, 10); } }
    moodWash(g, 'warm'); vign(g, 0.75); alive(g, t, 0.8); } }; };

// ---- pasteup: bàn dàn trang nhìn từ trên; cột chữ in sẵn và tranh trượt vào khuôn trang (paste-up), dao cắt rạch một đường. p = { at, cut, mood: 'sepia', cam, cap }
TPL.pasteup = (p) => { const cam = camOf(p), R = rng(p.seed || 41), parts = [];
  for (let i = 0; i < 4; i++) parts.push({ k: 'col', x: 0.08 + i * 0.215, y: 0.28, w: 0.19, h: 0.55 - (i % 2) * 0.14, d: [R() * 2 - 1, R() * 2 - 1] });
  parts.push({ k: 'pic', x: 0.08, y: 0.06, w: 0.62, h: 0.19, d: [-1, -0.5] }, { k: 'pic', x: 0.73, y: 0.06, w: 0.19, h: 0.19, d: [1, -0.5] }, { k: 'pic', x: 0.505, y: 0.7, w: 0.405, h: 0.13, d: [1, 1] });
  return { kind: 'full', full(g, t) { const c = cam(t), m = p.mood || 'sepia'; LL.cam(1 - c.z); g.fillStyle = '#3b2d22'; g.fillRect(0, 0, W, H);
    g.save(); g.translate(W / 2 + c.x * 0.5, H / 2); g.scale(1 + c.z, 1 + c.z); g.rotate(-0.04); g.translate(-W / 2, -H / 2);
    const bx = W * 0.27, by = H * 0.08, bw = W * 0.46, bh = H * 0.84;   // tấm bìa dàn trang (mechanical) có lưới xanh nhạt
    g.shadowColor = 'rgba(0,0,0,0.5)'; g.shadowBlur = 24; g.shadowOffsetY = 10; g.fillStyle = '#f1ead6'; g.fillRect(bx, by, bw, bh); g.shadowColor = 'transparent';
    g.strokeStyle = 'rgba(90,150,200,0.35)'; g.lineWidth = 1; for (let i = 1; i < 12; i++) { g.beginPath(); g.moveTo(bx + bw * i / 12, by); g.lineTo(bx + bw * i / 12, by + bh); g.stroke(); } for (let j = 1; j < 18; j++) { g.beginPath(); g.moveTo(bx, by + bh * j / 18); g.lineTo(bx + bw, by + bh * j / 18); g.stroke(); }
    const a0 = p.at === undefined ? p.t0 + 0.6 : p.at;
    parts.forEach((q, i) => { const u = eo(cl((t - a0 - i * 0.55) / 1.1)), dx = (1 - u) * q.d[0] * W * 0.35, dy = (1 - u) * q.d[1] * H * 0.35, x = bx + q.x * bw + dx, y = by + q.y * bh + dy, w = q.w * bw, h = q.h * bh;
      g.save(); g.globalAlpha *= cl(u * 3); g.shadowColor = 'rgba(0,0,0,0.35)'; g.shadowBlur = 8 + (1 - u) * 20; g.shadowOffsetY = 3 + (1 - u) * 14;
      if (q.k === 'col') { g.fillStyle = '#fbf7ec'; g.fillRect(x, y, w, h); g.shadowColor = 'transparent'; g.fillStyle = 'rgba(40,35,32,0.75)'; for (let k = 0; k * 13 < h - 14; k++) g.fillRect(x + 6, y + 8 + k * 13, w - 12 - ((k * 37) % 5 === 0 ? w * 0.3 : 0), 5); }
      else { g.fillStyle = '#d9cdb0'; g.fillRect(x, y, w, h); g.shadowColor = 'transparent'; g.fillStyle = 'rgba(70,55,40,0.55)'; g.beginPath(); g.moveTo(x, y + h); g.lineTo(x + w * 0.35, y + h * 0.35); g.lineTo(x + w * 0.6, y + h * 0.7); g.lineTo(x + w * 0.8, y + h * 0.45); g.lineTo(x + w, y + h); g.fill(); }
      g.restore(); });
    if (p.cut !== undefined) { const u = cl((t - p.cut) / 1.2); g.strokeStyle = 'rgba(30,25,22,0.8)'; g.lineWidth = 2; g.setLineDash([10, 6]); g.beginPath(); g.moveTo(bx - 30, by + bh * 0.66); g.lineTo(bx - 30 + (bw + 60) * u, by + bh * 0.66); g.stroke(); g.setLineDash([]);
      g.fillStyle = '#9aa0a6'; g.save(); g.translate(bx - 30 + (bw + 60) * u, by + bh * 0.66); g.rotate(-0.5); g.fillRect(-4, -70, 8, 70); g.fillStyle = '#c9ced3'; g.beginPath(); g.moveTo(-4, 0); g.lineTo(4, 0); g.lineTo(0, 18); g.fill(); g.restore(); }
    g.restore(); glow(g, W * 0.3, H * 0.1, W * 0.5, MOOD[m].lamp, 0.22); moodWash(g, m); vign(g); alive(g, t, 1); } }; };

// ---- diptych: chia đôi khung — trái: khay chữ chì dưới đèn (sepia); phải: lưới bản nháp trên màn hình (lạnh); vạch chia trượt vào ở p.split. p = { split, cam, cap }
TPL.diptych = (p) => { const cam = camOf(p), R = rng(p.seed || 53), pal = ['#c99a5a', '#4f7096', '#a95a4c', '#ddd5bd', '#5a8a7c', '#8c7aa0'];
  const tiles = []; for (let r = 0; r < 5; r++) for (let c = 0; c < 6; c++) tiles.push({ r, c, col: pal[Math.floor(R() * pal.length)], k: R() });
  return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); const s = p.split === undefined ? p.t0 + 0.5 : p.split, u = eo(cl((t - s) / 1.0)), mx = W * (1 - 0.5 * u);
    const PL = (q) => q && q.dir ? (window.PLATES || {})[q.dir + '#' + (q.i || 0)] : null, il = PL(p.left), ir = PL(p.right);
    const cover = (im, x0, w, fx) => { const sw = im.height * (w / H), sx = Math.max(0, Math.min(im.width - sw, fx * im.width - sw / 2)); g.drawImage(im, sx, 0, sw, im.height, x0, 0, w, H); };
    // trái: khay chữ
    g.save(); g.beginPath(); g.rect(0, 0, mx, H); g.clip(); g.fillStyle = '#241a12'; g.fillRect(0, 0, W, H);
    if (il) { cover(il, 0, mx, (p.left.fx === undefined ? 0.5 : p.left.fx)); } else {
    const ox = W * 0.08 + c.x * 0.3, oy = H * 0.2, cw = Math.min(W * 0.84, W * 0.42 + (1 - u) * W * 0.42), ch = H * 0.62;
    g.fillStyle = '#7a4e2e'; g.fillRect(ox, oy, cw, ch); g.strokeStyle = '#3d2414'; g.lineWidth = 4;
    for (let i = 0; i <= 12; i++) { g.beginPath(); g.moveTo(ox + cw * i / 12, oy); g.lineTo(ox + cw * i / 12, oy + ch); g.stroke(); } for (let j = 0; j <= 6; j++) { g.beginPath(); g.moveTo(ox, oy + ch * j / 6); g.lineTo(ox + cw, oy + ch * j / 6); g.stroke(); }
    const RR = rng(3); g.fillStyle = 'rgba(190,195,200,0.85)'; for (let i = 0; i < 260; i++) g.fillRect(ox + RR() * cw, oy + RR() * ch, 5, 6);
    glow(g, W * 0.25, H * 0.05, W * 0.45, '255,190,120', 0.35); moodWash(g, 'sepia'); } g.restore();
    // phải: màn hình bản nháp
    if (u > 0 && ir) { g.save(); g.beginPath(); g.rect(mx, 0, W - mx, H); g.clip(); cover(ir, mx, W - mx, (p.right.fx === undefined ? 0.5 : p.right.fx)); g.restore(); g.fillStyle = 'rgba(236,223,190,0.85)'; g.fillRect(mx - 2, 0, 4, H); }
    else if (u > 0) { g.save(); g.beginPath(); g.rect(mx, 0, W - mx, H); g.clip(); g.fillStyle = '#0d1320'; g.fillRect(0, 0, W, H); const sx = W * 0.54, sy = H * 0.16, tw = W * 0.068, th = H * 0.125;
      tiles.forEach((q) => { const a = cl((t - s - 0.4 - q.k * 1.5) / 0.4); if (a <= 0) return; g.globalAlpha = a; g.fillStyle = q.col; g.fillRect(sx + q.c * (tw + 8), sy + q.r * (th + 8), tw, th); g.fillStyle = 'rgba(20,20,26,0.7)'; g.fillRect(sx + q.c * (tw + 8) + 8, sy + q.r * (th + 8) + th - 18, tw - 16, 5); });
      g.globalAlpha = 1; glow(g, W * 0.75, H * 0.5, W * 0.4, '150,185,255', 0.25); moodWash(g, 'cold'); g.restore();
      g.fillStyle = 'rgba(236,223,190,0.85)'; g.fillRect(mx - 2, 0, 4, H); }
    vign(g, 0.55); alive(g, t, 1); } }; };

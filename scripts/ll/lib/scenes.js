// Last Lamplighters · thư viện mẫu — cảnh truyện 2.5D (canvas, toàn khung): phố đèn, văn phòng, phòng hàng ghế (tổng đài / phòng đánh máy).
// Thay thế rẻ cho cảnh three.js của tập 1 (9–13 s/khung) ở các tập nhà máy: ≈ 0,3 s/khung, cùng bảng màu chạng vạng.
// Chuẩn kênh §5.3: ≥ 3 lớp parallax, máy chuyển động chậm có easing, sương theo độ sâu, quầng đèn rung, hạt trong vùng sáng;
// bóng người không mặt, viền tách 2,75 px khỏi nền (rim).
// Máy: p.cam = [{ t, x, z }] — x lia ngang (px ở lớp gần), z đẩy vào (0 … 0,6). Lớp có độ sâu d (1 = gần nhất);
// LL.cam(d_min − z) báo khoảng cách tới lớp gần nhất: z ≥ 1 nghĩa là máy xuyên lớp gần (qc bắt).
'use strict';
function camOf(p) { const C = p.cam || [{ t: p.t0, x: 0, z: 0 }, { t: p.t1, x: -120, z: 0.04 }];
  return (t) => { let i = 0; while (i < C.length - 2 && t >= C[i + 1].t) i++; const a = C[i], b = C[i + 1] || a, u = b === a ? 0 : sm(pr(t, a.t, b.t)); return { x: lerp(a.x, b.x, u), z: lerp(a.z || 0, b.z || 0, u) }; }; }
// đặt điểm của lớp độ sâu d (1 gần … 4 xa) theo máy: lia giảm theo 1/d, phóng quanh tâm theo z/d
function lay(c, d) { const s = 1 / (1 - c.z / d); return (x, y) => [W / 2 + (x - W / 2 + c.x / d) * s, H * 0.62 + (y - H * 0.62) * s]; }
function sky(g, t, warm = 0.5) { const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#1b2140'); gr.addColorStop(0.55, mixC('#3a3550', '#6b4a52', warm)); gr.addColorStop(0.75, mixC('#4a3d48', '#a0644a', warm)); gr.addColorStop(1, '#1a1622');
  g.fillStyle = gr; g.fillRect(0, 0, W, H); }
function fog(g, y, a, col = '120,110,140') { const gr = g.createLinearGradient(0, y - H * 0.25, 0, y + H * 0.1); gr.addColorStop(0, `rgba(${col},0)`); gr.addColorStop(1, `rgba(${col},${a})`); g.fillStyle = gr; g.fillRect(0, y - H * 0.25, W, H * 0.35); }
// dãy nhà (một lớp): hạt giống cố định; cửa sổ ấm/lạnh; trả nothing
const ROWS = {};
function rowOf(seed, n, hmin, hmax) { const k = seed + ':' + n; if (ROWS[k]) return ROWS[k]; const R = rng(seed), b = []; let x = -400;
  while (x < W + 400) { const w = 120 + R() * 160, h = hmin + R() * (hmax - hmin); b.push({ x, w, h, roof: R(), win: Array.from({ length: 40 }, () => [R(), R()]) }); x += w + R() * 10; } return (ROWS[k] = b); }
function houses(g, t, c, d, seed, base, hmin, hmax, col, winA, warm = 0.8) { const P = lay(c, d);
  for (const b of rowOf(seed, d, hmin, hmax)) { const [x0, y0] = P(b.x, base - b.h), [x1, y1] = P(b.x + b.w, base); if (x1 < -50 || x0 > W + 50) continue;
    g.fillStyle = col; g.fillRect(x0, y0, x1 - x0, y1 - y0); if (b.roof > 0.6) { g.beginPath(); g.moveTo(x0, y0); g.lineTo((x0 + x1) / 2, y0 - (x1 - x0) * 0.25); g.lineTo(x1, y0); g.fill(); }
    if (b.roof < 0.3) g.fillRect(x0 + (x1 - x0) * 0.7, y0 - (y1 - y0) * 0.12, (x1 - x0) * 0.08, (y1 - y0) * 0.12);
    const cols = Math.max(2, Math.round((x1 - x0) / (34 / d * 2))), rows = Math.max(2, Math.round((y1 - y0) / (60 / d * 2)));
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows - 1; j++) { const r = b.win[(i * 7 + j * 3) % 40]; if (r[0] > winA) continue;
      const on = 0.6 + 0.4 * Math.sin(t * 0.3 + r[1] * 20); const wx = x0 + (i + 0.3) * (x1 - x0) / cols, wy = y0 + (j + 0.4) * (y1 - y0) / rows;
      g.fillStyle = r[1] < warm ? `rgba(255,190,110,${0.55 * on})` : `rgba(200,220,255,${0.45 * on})`; g.fillRect(wx, wy, (x1 - x0) / cols * 0.4, (y1 - y0) / rows * 0.45); } } }
// đèn khí trên phố (lớp gần) — lit 0..1, rung quầng
function streetLamp(g, t, P, x, base, s, lit, seed) { const [px, py] = P(x, base), [, pt] = P(x, base - 300 * s), k = (py - pt) / 300;
  g.save(); g.fillStyle = '#0f0c0b'; g.fillRect(px - 5 * k, pt + 40 * k, 10 * k, py - pt - 40 * k); g.beginPath(); g.moveTo(px - 26 * k, pt + 40 * k); g.lineTo(px - 18 * k, pt); g.lineTo(px + 18 * k, pt); g.lineTo(px + 26 * k, pt + 40 * k); g.closePath();
  g.fillStyle = lit > 0 ? `rgba(255,${170 + 40 * lit},${90 + 40 * lit},${0.25 + 0.7 * lit})` : 'rgba(40,36,40,0.9)'; g.fill(); g.strokeStyle = '#0f0c0b'; g.lineWidth = 3 * k; g.stroke();
  g.fillStyle = '#0f0c0b'; g.beginPath(); g.moveTo(px - 32 * k, pt); g.lineTo(px, pt - 22 * k); g.lineTo(px + 32 * k, pt); g.fill(); g.fillRect(px - 30 * k, pt + 34 * k, 60 * k, 5 * k); g.restore();
  if (lit > 0) { const fl = 0.88 + 0.07 * Math.sin(t * 11.3 + seed) + 0.05 * Math.sin(t * 23.7 + seed * 2); glow(g, px, pt + 22 * k, 210 * k, RGB_AMB, 0.5 * lit * fl); glow(g, px, py, 160 * k, RGB_AMB, 0.12 * lit * fl);
    const R = rng(seed * 31 + 7); g.save(); g.globalCompositeOperation = 'lighter'; for (let i = 0; i < 14; i++) { const a = R() * 6.28, r = (R() * 120 + ((t * (8 + R() * 10)) % 120)) * k;
      g.fillStyle = `rgba(255,214,160,${0.25 * lit * (1 - r / (120 * k))})`; g.fillRect(px + Math.cos(a) * r, pt + 22 * k + Math.sin(a) * r * 0.7, 2, 2); } g.restore(); }
  return [px, pt + 22 * k]; }
// ---- phố đèn: p = { lamps: [{ x, lit: t }], lighter: { from: [x], to: [x], walk: [t0,t1], lights: [chỉ số đèn] } | null, warm, cam, mood: 'dusk'|'night', windows } ----
TPL.street = (p) => { const cam = camOf(p), L = p.lamps || [{ x: 300 }, { x: 900 }, { x: 1500 }, { x: 2100 }];
  return { kind: 'full', blur: p.blur, full(g, t) { const c = cam(t); LL.cam(1 - c.z); sky(g, t, p.warm === undefined ? 0.5 : p.warm);
    houses(g, t, c, 4, 11, H * 0.66, 260, 420, '#2a2738', 0.25); fog(g, H * 0.66, 0.35);
    houses(g, t, c, 2.4, 23, H * 0.72, 300, 520, '#1d1a26', p.windows === undefined ? 0.35 : p.windows); fog(g, H * 0.74, 0.3, '90,80,110');
    const P = lay(c, 1), [, gy] = P(0, H * 0.86); g.fillStyle = '#16131a'; g.fillRect(0, gy, W, H - gy);   // vỉa hè
    g.fillStyle = 'rgba(255,190,120,0.04)'; for (let i = 0; i < 12; i++) { const [x0] = P(i * 220 - 300, H * 0.86); g.fillRect(x0, gy, 2, H - gy); }
    const tips = L.map((l, i) => streetLamp(g, t, P, l.x, H * 0.86, 1, l.lit === undefined ? 1 : rv(t, l.lit, 0.5), i + 1));
    const lt = p.lighter; if (lt) { const u = pr(t, lt.walk[0], lt.walk[1]), x = lerp(lt.from, lt.to, sm(u)), [px, py] = P(x, H * 0.86), [, ph] = P(x, H * 0.86 - 210);
      const near = L.findIndex((l, i) => (lt.lights || []).includes(i) && l.lit !== undefined && Math.abs(t - l.lit) < 0.8), reach = near >= 0 ? 1 - Math.abs(t - L[near].lit) / 0.8 : 0;
      person(g, px, py, py - ph, { hat: 'top', coat: true, step: u > 0 && u < 1 ? Math.sin(t * 7) * 0.8 : 0, arm: lerp(0.5, 2.7, sm(reach)), pole: 90, col: '#0c0a0a', rim: 'rgba(255,200,140,0.9)' }); }
    for (const l of L) if (l.lit !== undefined) { if (Math.abs(t - l.lit) < 0.02) LL.act = true; }
    const v = g.createRadialGradient(W / 2, H / 2, H * 0.4, W / 2, H / 2, H * 1.0); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.55)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
  } }; };
// ---- văn phòng (khối cửa sổ hiện đại sau đèn khí): p = { cam, lamp: true, rows, cols, light: t (đèn văn phòng bật dần) } ----
TPL.office = (p) => { const cam = camOf(p); return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z); sky(g, t, 0.25);
  houses(g, t, c, 4, 51, H * 0.7, 500, 820, '#232638', 0.6, 0.1); fog(g, H * 0.68, 0.3, '80,90,120');
  const P = lay(c, 1.8), R = rng(91); for (let b = 0; b < 3; b++) { const bx = 300 + b * 620, bw = 520, bh = 700 - b * 90, [x0, y0] = P(bx, H * 0.86 - bh), [x1, y1] = P(bx + bw, H * 0.86);
    g.fillStyle = '#1a1c28'; g.fillRect(x0, y0, x1 - x0, y1 - y0); const cols = 9, rows = 12, on = p.light === undefined ? 1 : rv(t, p.light + b * 0.4, 2.5);
    for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) { const r = R(), r2 = R(); if (r > 0.75) continue; const a = cl(on * 1.3 - r2 * 0.3) * (0.6 + 0.4 * Math.sin(t * 0.2 + r2 * 30));
      g.fillStyle = r2 < 0.08 ? `rgba(255,196,120,${0.7 * a})` : `rgba(215,230,255,${0.6 * a})`; g.fillRect(x0 + (i + 0.15) * (x1 - x0) / cols, y0 + (j + 0.2) * (y1 - y0) / rows, (x1 - x0) / cols * 0.7, (y1 - y0) / rows * 0.55); } }
  const Pn = lay(c, 1), [, gy] = Pn(0, H * 0.88); g.fillStyle = '#121016'; g.fillRect(0, gy, W, H - gy);
  if (p.lamp !== false) streetLamp(g, t, Pn, p.lampX || 420, H * 0.92, 1.25, 1, 3);
  const v = g.createRadialGradient(W / 2, H / 2, H * 0.4, W / 2, H / 2, H); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.5)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
} }; };
// ---- phòng hàng ghế nhìn từ sau lưng (tổng đài / phòng đánh máy): p = { variant: 'switchboard'|'typing', rows: 3, per: 7, cam, dim: [t0,t1] (đèn bàn tắt dần), screen: t (màn hình con trỏ/sóng âm hiện) } ----
TPL.rows = (p) => { if (p.variant === 'teller') return TPL.teller(p); const cam = camOf(p), V = p.variant || 'switchboard', R0 = rng(V === 'switchboard' ? 1878 : 1930), JK = Array.from({ length: 400 }, () => [R0(), R0(), R0()]);
  return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z);
    const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#2a2026'); gr.addColorStop(1, '#120e12'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    const dim = p.dim ? pr(t, p.dim[0], p.dim[1]) : 0; if (dim > 0 && dim < 1) LL.act = true;
    // cửa sổ cao phía sau (lớp xa)
    const Pf = lay(c, 3.5); for (let i = 0; i < 5; i++) { const [x0, y0] = Pf(160 + i * 380, H * 0.12), [x1, y1] = Pf(330 + i * 380, H * 0.5); g.fillStyle = 'rgba(120,130,170,0.18)'; g.fillRect(x0, y0, x1 - x0, y1 - y0); }
    const rows = p.rows || 3, per = p.per || 7;
    for (let r = rows - 1; r >= 0; r--) { const d = 1 + r * 0.8, P = lay(c, d), base = H * (0.98 - r * 0.13), sc = 1 / d;
      // bàn/tủ tổng đài
      const [bx0, by0] = P(-100, base - 330 * sc * 1.4), [bx1, by1] = P(W + 100, base - 120 * sc);
      g.fillStyle = mixC('#3a2a22', '#1e1612', r / rows); g.fillRect(bx0, by0, bx1 - bx0, by1 - by0);
      if (V === 'switchboard') { for (let k = 0; k < 140; k++) { const j = JK[(k + r * 140) % 400], x = bx0 + j[0] * (bx1 - bx0), y = by0 + 10 + j[1] * (by1 - by0 - 20);
          const on = (0.5 + 0.5 * Math.sin(t * (0.6 + j[2] * 2.5) + j[0] * 40)) > 0.72 ? 1 : 0.15, a = on * (1 - dim);
          g.fillStyle = `rgba(255,${150 + 60 * j[2]},70,${0.25 + 0.65 * a})`; g.beginPath(); g.arc(x, y, 3.2 * sc + 1, 0, 7); g.fill(); if (a > 0.5) glow(g, x, y, 14 * sc + 4, RGB_AMB, 0.35 * a); }
        g.strokeStyle = 'rgba(20,14,12,0.7)'; g.lineWidth = 2 * sc + 0.5; for (let k = 0; k < 18; k++) { const j = JK[(k * 7 + r * 31) % 400], x = bx0 + j[0] * (bx1 - bx0), y = by0 + 20 + j[1] * (by1 - by0 - 40);
          g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + 30 * sc, by1 + 30 * sc, x + (j[2] - 0.5) * 300 * sc, y + 10); g.stroke(); } }
      else { for (let k = 0; k < per; k++) { const x = bx0 + (k + 0.5) * (bx1 - bx0) / per; glow(g, x, by1 - 60 * sc, 140 * sc, RGB_AMB, 0.4 * (1 - cl(dim * per - k))); } }
      for (let k = 0; k < per; k++) { const x0 = (k + 0.5) * W / per + (r % 2) * W / per / 2 - W / per / 4, [px, py] = P(x0, base), j = JK[k * 3 + r * 29];
        if (V === 'typing' && dim * per - k > 1) continue;
        person(g, px, py, 300 * sc, { seated: true, bun: j[0] < 0.6, headset: V === 'switchboard', armLen: 0.5, arm: 2.0 + 0.25 * Math.sin(t * (1 + j[1]) + j[2] * 9), arm2: -1.9 - 0.2 * Math.sin(t * 1.3 + j[1] * 7), col: '#0d0a0b', rim: 'rgba(255,190,120,0.8)' }); }
      fog(g, base - 150 * sc, 0.12 * r, '60,50,60'); }
    if (p.screen !== undefined) { const a = rv(t, p.screen, 1.2); if (a > 0) { g.save(); g.globalAlpha = a; g.fillStyle = '#0e1622'; g.fillRect(W * 0.32, H * 0.18, W * 0.36, H * 0.4); g.strokeStyle = '#7fa6d8'; g.lineWidth = 3;
      g.beginPath(); for (let x = 0; x <= 600; x += 4) { const y = H * 0.38 + Math.sin(x * 0.05 + t * 6) * 40 * Math.sin(x / 600 * Math.PI) * (0.5 + 0.5 * Math.sin(t * 2.1 + x * 0.01)); x ? g.lineTo(W * 0.34 + x, y) : g.moveTo(W * 0.34 + x, y); } g.stroke();
      g.restore(); text(g, p.screenLabel || 'AUTOMATED VOICE', W / 2, H * 0.53, 30, '#cfe0f5', { align: 'center', a }); LL.act = LL.act || a < 1; } }
    const v = g.createRadialGradient(W / 2, H * 0.55, H * 0.35, W / 2, H * 0.55, H * 1.05); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.6)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
  } }; };
// ---- quầy giao dịch ngân hàng nhìn từ sảnh (tập 3): p = { per: 6 ô cửa, cam, dim: [t0,t1] (đèn ô cửa tắt dần từ trái), screen: t (máy ATM ở tường phải sáng), screenLabel,
//      look: t (giao dịch viên ô giữa ngẩng lên), customer: { at: t, nervous } (khách đứng trước ô giữa, bồn chồn) } — bóng 2.5D, không mặt ----
TPL.teller = (p) => { const cam = camOf(p), per = p.per || 6, R0 = rng(1970), J = Array.from({ length: 64 }, () => [R0(), R0(), R0()]), mid = Math.floor((per - 1) / 2);
  return { kind: 'full', full(g, t) { const c = cam(t); LL.cam(1 - c.z);
    const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#2b2321'); gr.addColorStop(1, '#130f0e'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    const dim = p.dim ? pr(t, p.dim[0], p.dim[1]) : 0; if (dim > 0 && dim < 1) LL.act = true;
    // lớp xa: tường đá có cột và cửa sổ vòm
    const Pb = lay(c, 3.2); for (let i = 0; i < 7; i++) { const [x0, y0] = Pb(-120 + i * 340, H * 0.06), [x1, y1] = Pb(-60 + i * 340, H * 0.62); g.fillStyle = 'rgba(70,58,52,0.55)'; g.fillRect(x0, y0, x1 - x0, y1 - y0);
      const [w0, v0] = Pb(20 + i * 340, H * 0.1), [w1, v1] = Pb(200 + i * 340, H * 0.36); g.fillStyle = 'rgba(110,125,165,0.16)'; g.fillRect(w0, v0, w1 - w0, v1 - v0); }
    // lớp giữa: quầy với các ô cửa, đèn bàn, giao dịch viên
    const P = lay(c, 1.6), sc = 1 / 1.6, [cx0, cy0] = P(-80, H * 0.44), [cx1, cy1] = P(W + 80, H * 0.86);
    for (let k = 0; k < per; k++) { const on = 1 - cl(dim * per - k), xa = cx0 + (k + 0.08) * (cx1 - cx0) / per, xb = cx0 + (k + 0.92) * (cx1 - cx0) / per, wy = cy0 + (cy1 - cy0) * 0.05, wy1 = cy0 + (cy1 - cy0) * 0.52;
      g.fillStyle = mixC('#3b2f26', '#5a4632', on * 0.6); g.fillRect(xa, wy, xb - xa, wy1 - wy);
      if (on > 0.02) glow(g, (xa + xb) / 2, wy1 - 20 * sc, 150 * sc, RGB_AMB, 0.45 * on);
      if (on > 0.3) { const lift = (p.look !== undefined && k === mid) ? pr(t, p.look, p.look + 0.9) : 0; if (lift > 0 && lift < 1) LL.act = true;
        person(g, (xa + xb) / 2 + (J[k][0] - 0.5) * 30 * sc, wy1 + 330 * sc, 560 * sc, { seated: true, bun: J[k][1] < 0.5, lift, arm: 0.55 + 0.12 * Math.sin(t * (0.8 + J[k][2]) + k), arm2: -0.5 - 0.1 * Math.sin(t * 1.1 + k * 3), armLen: 0.8, col: '#0d0a0b', rim: `rgba(255,190,120,${0.8 * on})` }); }
      g.strokeStyle = 'rgba(30,22,16,0.9)'; g.lineWidth = 3 * sc + 1; for (let b = 1; b < 7; b++) { const x = xa + b * (xb - xa) / 7; g.beginPath(); g.moveTo(x, wy); g.lineTo(x, wy1 - 30 * sc); g.stroke(); }
      g.strokeStyle = 'rgba(150,120,80,0.5)'; g.lineWidth = 2; g.strokeRect(xa, wy, xb - xa, wy1 - wy); }
    g.fillStyle = '#2a1e17'; g.fillRect(cx0, cy0 + (cy1 - cy0) * 0.52, cx1 - cx0, (cy1 - cy0) * 0.5); g.fillStyle = 'rgba(190,150,100,0.25)'; g.fillRect(cx0, cy0 + (cy1 - cy0) * 0.52, cx1 - cx0, 4);
    // máy ATM ở tường phải
    if (p.screen !== undefined) { const a = rv(t, p.screen, 1.2), [ax0, ay0] = P(W * 0.86, H * 0.5), [ax1, ay1] = P(W * 0.97, H * 0.74);
      g.fillStyle = '#1d1a1c'; g.fillRect(ax0 - 10, ay0 - 14, ax1 - ax0 + 20, ay1 - ay0 + 60);
      if (a > 0) { g.save(); g.globalAlpha = a * (0.9 + 0.1 * Math.sin(t * 3)); g.fillStyle = '#0c1a2b'; g.fillRect(ax0, ay0, ax1 - ax0, ay1 - ay0); g.restore(); glow(g, (ax0 + ax1) / 2, (ay0 + ay1) / 2, 260 * sc, '120,170,230', 0.2 * a);
        text(g, p.screenLabel || 'ATM', (ax0 + ax1) / 2, (ay0 + ay1) / 2, 30, '#f2f7ff', { align: 'center', base: 'middle', a, bold: true }); LL.act = LL.act || a < 1; } }
    // lớp gần: khách trước ô giữa
    if (p.customer) { const ca = rv(t, p.customer.at, 0.8), P1 = lay(c, 1.0), xm = cx0 + (mid + 0.5) * (cx1 - cx0) / per;
      if (ca > 0) { const nv = p.customer.nervous ? 1 : 0, sway = nv * 6 * Math.sin(t * 2.3), [qx, qy] = P1(W / 2 + (xm - W / 2) / 1.0 + sway, H * 1.04);
        g.save(); g.globalAlpha = ca; person(g, qx, qy, 560, { coat: true, arm: -0.5 + nv * (0.9 + 0.08 * Math.sin(t * 5.1)), arm2: -0.1 - nv * 0.25 * Math.abs(Math.sin(t * 1.7)), step: nv * 0.08 * Math.sin(t * 1.9), flip: true, col: '#0a0809', rim: 'rgba(255,200,140,0.75)' }); g.restore();
        if (ca < 1 || nv) LL.act = true; } }
    fog(g, H * 0.98, 0.18, '60,50,46');
    const v = g.createRadialGradient(W / 2, H * 0.55, H * 0.35, W / 2, H * 0.55, H * 1.05); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.6)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
  } }; };

// ---- thẻ kết (16:9 và 9:16): p = { title, line, next } ----
TPL.endcard = (p) => { const PT = (() => { const R = rng(9090); return Array.from({ length: 40 }, () => [R(), R(), R(), R()]); })();
  return { kind: 'full', full(g, t) { const u = t - p.t0; g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
    const cx = W / 2, cy = LL.fmt === '9x16' ? 640 : 330; const gr = g.createRadialGradient(cx, cy + 200, 0, cx, cy + 200, 700); gr.addColorStop(0, 'rgba(60,70,120,0.35)'); gr.addColorStop(1, 'rgba(20,26,46,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
    for (const [r1, r2, r3, r4] of PT) { const x = W * r1 + 14 * Math.sin(t * (0.5 + r3) + r1 * 7), y = H * ((r2 - 0.02 * t * (0.5 + r4) + 10) % 1); g.fillStyle = `rgba(236,223,190,${0.05 + 0.08 * r3})`; g.beginPath(); g.arc(x, y, 1.4 + 2 * r4, 0, 7); g.fill(); }
    const fl = 0.85 + 0.1 * Math.sin(t * 9.3) + 0.05 * Math.sin(t * 23.1), lit = sm(u / 0.8); glow(g, cx, cy + 10, 150, RGB_AMB, 0.45 * fl * lit); gasLampIcon(g, cx, cy, 1.25, 1, fl * lit, AMBER_L);
    const ty = cy + 320; text(g, p.title || 'Last Lamplighters', cx, ty - 6 * (1 - eo(u / 0.5)), 76, CREAM, { align: 'center', kind: 'serif', a: sm(u / 0.4) });
    g.save(); g.strokeStyle = AMBER_L; g.lineWidth = 3; g.beginPath(); g.moveTo(cx - 160 * sm(u / 0.6), ty + 40); g.lineTo(cx + 160 * sm(u / 0.6), ty + 40); g.stroke(); g.restore();
    if (p.line) text(g, p.line, cx, ty + 110, 44, CREAM, { align: 'center', a: rv(t, p.t0 + 0.4, 0.6) });
    if (p.next) para(g, p.next, cx, ty + 190, W - 240, 34, '#cfd6ee', { align: 'center', a: rv(t, p.t0 + 1.0, 0.6) });
  } }; };

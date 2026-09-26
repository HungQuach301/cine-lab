// Cảnh mẫu M0 — phong cách (a) 2D vector trên Canvas 2D.
// window.setup(scene, sheet) rồi window.renderFrame(f, samples) -> dataURL PNG.
(function () {
  let S, M, W, Hh, cv, ctx, acc, actx, chr, cctx, bg;

  function lcg(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

  // Dựng sẵn hình dạng các lớp nền (xác định, cùng seed -> cùng khung hình).
  function buildLayers() {
    const r = lcg(7);
    const far = [], mid = [], near = [];
    for (let x = -400; x < 5200; x += 90 + r() * 140) far.push({ x, w: 80 + r() * 160, h: 180 + r() * 260, spire: r() < 0.25 });
    for (let x = -400; x < 7000; x += 260 + r() * 120) {
      const w = 220 + r() * 120, h = 300 + r() * 220, wins = [];
      for (let wy = 60; wy < h - 60; wy += 70) for (let wx = 30; wx < w - 40; wx += 60) wins.push({ wx, wy, on: r() < 0.45 });
      mid.push({ x, w, h, wins, roof: r() });
    }
    for (let x = -300; x < 12000; x += 520 + r() * 380) near.push({ x, kind: r() < 0.5 ? 'post' : 'fence', w: 60 + r() * 40 });
    return { far, mid, near };
  }

  function lampGlow(g, lx, ly, rad, strength) {
    const gr = g.createRadialGradient(lx, ly, 0, lx, ly, rad);
    gr.addColorStop(0, `rgba(255,190,110,${0.85 * strength})`);
    gr.addColorStop(0.25, `rgba(255,160,80,${0.35 * strength})`);
    gr.addColorStop(1, 'rgba(255,140,60,0)');
    g.fillStyle = gr; g.fillRect(lx - rad, ly - rad, rad * 2, rad * 2);
  }

  function limb(g, len, w, color) {
    // Bộ phận hướng xuống (+y) từ khớp gốc, bo tròn.
    g.fillStyle = color; g.beginPath();
    g.roundRect(-w / 2, -w / 2, w, len + w / 2, w / 2); g.fill();
  }

  // Vẽ nhân vật theo model sheet. hx, hy = hông; u = px trên 1 H; pose = góc (rad), dương = về phía trước (+x).
  function drawCharacter(g, hx, hy, u, pose, override) {
    const col = (k) => (override ? (M[k].id_color || '#000') : M[k].color);
    const T = M.torso, tl = T.length * u;
    const leg = (a1, a2, back) => {
      g.save(); g.translate(hx, hy); g.rotate(-a1);
      limb(g, M.thigh.length * u, M.thigh.width * u, back && !override ? '#2c2632' : col('thigh'));
      g.translate(0, M.thigh.length * u); g.rotate(-a2);
      limb(g, M.shin.length * u, M.shin.width * u, back && !override ? '#2c2632' : col('shin'));
      if (!override) { g.translate(0, M.shin.length * u); g.rotate(a1 + a2); g.fillStyle = M.foot.color; g.beginPath(); g.roundRect(-0.12 * u, -0.05 * u, M.foot.length * u, M.foot.width * u, 0.08 * u); g.fill(); }
      g.restore();
    };
    const arm = (a1, a2, back) => {
      const sy = hy - tl + M.joints.shoulder_from_torso_top * u;
      g.save(); g.translate(hx, sy); g.rotate(-a1);
      limb(g, M.upper_arm.length * u, M.upper_arm.width * u, back && !override ? '#4a2a1f' : col('upper_arm'));
      g.translate(0, M.upper_arm.length * u); g.rotate(-a2);
      limb(g, M.forearm.length * u, M.forearm.width * u, back && !override ? '#4a2a1f' : col('forearm'));
      if (!override) { g.translate(0, M.forearm.length * u); g.fillStyle = M.hand.color; g.beginPath(); g.arc(0, 0, M.hand.width * u / 2, 0, 7); g.fill(); }
      g.restore();
    };
    leg(pose.thighB, pose.shinB, true); arm(pose.armB, pose.foreB, true);
    // Thân: hình thang (áo khoác).
    g.fillStyle = col('torso'); g.beginPath();
    g.moveTo(hx - T.top_width * u / 2, hy - tl); g.lineTo(hx + T.top_width * u / 2, hy - tl);
    g.lineTo(hx + T.bottom_width * u / 2, hy); g.lineTo(hx - T.bottom_width * u / 2, hy); g.closePath(); g.fill();
    leg(pose.thighF, pose.shinF, false);
    // Cổ, đầu, mũ.
    const ny = hy - tl, nl = M.neck.length * u;
    if (!override) { g.fillStyle = M.neck.color; g.fillRect(hx - M.neck.width * u / 2, ny - nl, M.neck.width * u, nl + 2); }
    const hcY = ny - nl - M.head.length * u / 2;
    g.fillStyle = col('head'); g.beginPath(); g.ellipse(hx, hcY, M.head.width * u / 2, M.head.length * u / 2, 0, 0, 7); g.fill();
    if (!override) {
      g.fillStyle = M.hat.color; const top = hcY - M.head.length * u * 0.35;
      g.fillRect(hx - M.hat.width * u / 2, top - 0.08 * u, M.hat.width * u, 0.1 * u);
      g.beginPath(); g.roundRect(hx - 0.42 * u, top - M.hat.length * u, 0.84 * u, M.hat.length * u - 0.05 * u, 0.1 * u); g.fill();
    }
    arm(pose.armF, pose.foreF, false);
    // Sào thắp đèn trên tay trước.
    if (!override && pose.pole) {
      const sy = hy - tl + M.joints.shoulder_from_torso_top * u;
      const a = pose.armF, b = pose.foreF;
      const ex = hx + Math.sin(a) * M.upper_arm.length * u + Math.sin(a + b) * M.forearm.length * u;
      const ey = sy + Math.cos(a) * M.upper_arm.length * u + Math.cos(a + b) * M.forearm.length * u;
      g.save(); g.translate(ex, ey); g.rotate(0.35); g.fillStyle = M.pole.color;
      g.fillRect(-M.pole.width * u / 2, -M.pole.length * u * 0.75, M.pole.width * u, M.pole.length * u); g.restore();
    }
  }

  function walkPose(ph) {
    const s = Math.sin(ph), c = Math.cos(ph);
    return {
      thighF: 0.42 * s, shinF: -Math.max(0, 0.7 * Math.sin(ph + 1.2)) ,
      thighB: -0.42 * s, shinB: -Math.max(0, -0.7 * Math.sin(ph + 1.2)),
      armF: 0.12 - 0.05 * s, foreF: 0.9, armB: 0.35 * s, foreB: 0.35 + 0.1 * c, pole: true,
    };
  }

  function drawScene(t) {
    const cam = t * S.camera.pan_px_per_s;
    const g = ctx;
    // Trời hoàng hôn.
    const sky = g.createLinearGradient(0, 0, 0, Hh);
    sky.addColorStop(0, '#1b1830'); sky.addColorStop(0.55, '#5a3550'); sky.addColorStop(0.8, '#c0664a'); sky.addColorStop(1, '#2a1a22');
    g.fillStyle = sky; g.fillRect(0, 0, W, Hh);
    // Lớp xa.
    const [Lf, Lm, Ln] = S.layers;
    g.fillStyle = Lf.color;
    for (const b of bg.far) {
      const x = b.x - cam * Lf.parallax; if (x > W || x + b.w < 0) continue;
      g.fillRect(x, 760 - b.h, b.w, b.h + 20);
      if (b.spire) { g.beginPath(); g.moveTo(x, 760 - b.h); g.lineTo(x + b.w / 2, 760 - b.h - 90); g.lineTo(x + b.w, 760 - b.h); g.fill(); }
    }
    g.fillStyle = 'rgba(40,30,55,0.35)'; g.fillRect(0, 520, W, 260); // khói mù
    // Lớp giữa: nhà, cửa sổ ấm.
    const lx = S.light.world_x - cam * Lm.parallax, ly = S.light.y;
    for (const b of bg.mid) {
      const x = b.x - cam * Lm.parallax; if (x > W || x + b.w < 0) continue;
      const top = S.character.ground_y - b.h;
      g.fillStyle = Lm.color; g.fillRect(x, top, b.w, b.h);
      g.beginPath(); g.moveTo(x - 10, top); g.lineTo(x + b.w * (0.3 + 0.4 * b.roof), top - 70); g.lineTo(x + b.w + 10, top); g.fill();
      for (const w of b.wins) { g.fillStyle = w.on ? '#e89a4a' : '#1a1520'; g.fillRect(x + w.wx, top + w.wy, 26, 38); }
    }
    // Mặt đường.
    const road = g.createLinearGradient(0, S.character.ground_y, 0, Hh);
    road.addColorStop(0, '#2b2128'); road.addColorStop(1, '#0d0a0e');
    g.fillStyle = road; g.fillRect(0, S.character.ground_y, W, Hh - S.character.ground_y);
    // Cột đèn khí (nguồn sáng ấm duy nhất).
    g.fillStyle = '#15111a'; g.fillRect(lx - 7, ly, 14, S.character.ground_y - ly);
    g.beginPath(); g.moveTo(lx - 28, ly); g.lineTo(lx + 28, ly); g.lineTo(lx + 18, ly - 50); g.lineTo(lx - 18, ly - 50); g.fill();
    g.fillStyle = '#ffd08a'; g.fillRect(lx - 14, ly - 44, 28, 40);
    // Vũng sáng trên mặt đường.
    g.save(); g.globalCompositeOperation = 'lighter';
    g.translate(lx, S.character.ground_y + 20); g.scale(1, 0.18); lampGlow(g, 0, 0, 480, 0.5); g.restore();

    // Nhân vật.
    const C = S.character, u = C.height_px / M.total_height_H;
    const hx = C.start_x + (C.end_x - C.start_x) * (t / S.duration_s);
    const ph = t * C.step_hz * Math.PI * 2;
    const bob = Math.abs(Math.cos(ph)) * 0.06 * u;
    const hy = C.ground_y - (M.thigh.length + M.shin.length + M.foot.width) * u * 0.97 - bob;
    const sx = hx - cam; // nhân vật ở lớp giữa về chiều sâu, theo máy quay 1:1
    // Bóng đổ ngược phía đèn.
    const dx = sx - lx, dist = Math.abs(dx);
    g.save(); g.fillStyle = `rgba(0,0,0,${Math.max(0.1, 0.55 - dist / 2000)})`;
    g.beginPath(); g.ellipse(sx + Math.sign(dx) * Math.min(160, dist * 0.25), C.ground_y + 4, 70 + Math.min(120, dist * 0.15), 12, 0, 0, 7); g.fill(); g.restore();
    // Vẽ nhân vật lên lớp riêng rồi chiếu sáng theo khoảng cách tới đèn.
    cctx.setTransform(1, 0, 0, 1, 0, 0); cctx.clearRect(0, 0, W, Hh);
    drawCharacter(cctx, sx, hy, u, walkPose(ph), false);
    cctx.globalCompositeOperation = 'source-atop';
    const k = Math.max(0, 1 - dist / 900);
    cctx.fillStyle = `rgba(10,6,20,${0.55 - 0.45 * k})`; cctx.fillRect(0, 0, W, Hh);
    const side = cctx.createLinearGradient(sx - 60, 0, sx + 60, 0);
    const warm = `rgba(255,170,90,${0.55 * k})`;
    if (dx < 0) { side.addColorStop(0, 'rgba(255,170,90,0)'); side.addColorStop(1, warm); } else { side.addColorStop(0, warm); side.addColorStop(1, 'rgba(255,170,90,0)'); }
    cctx.fillStyle = side; cctx.fillRect(0, 0, W, Hh);
    cctx.globalCompositeOperation = 'source-over';
    g.drawImage(chr, 0, 0);

    // Quầng sáng đèn (cộng).
    g.save(); g.globalCompositeOperation = 'lighter'; lampGlow(g, lx, ly - 24, S.light.radius_px, 1); g.restore();
    // Lớp gần: cột, hàng rào tiền cảnh, đi nhanh hơn máy quay.
    g.fillStyle = Ln.color;
    for (const n of bg.near) {
      const x = n.x - cam * Ln.parallax - t * 0; if (x > W + 200 || x < -300) continue;
      if (n.kind === 'post') g.fillRect(x, 180, n.w, Hh);
      else { g.fillRect(x, 930, 280, 24); for (let i = 0; i < 5; i++) g.fillRect(x + i * 60, 890, 16, Hh); }
    }
    // Vignette.
    const v = g.createRadialGradient(W / 2, Hh / 2, Hh * 0.35, W / 2, Hh / 2, Hh * 1.05);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.55)');
    g.fillStyle = v; g.fillRect(0, 0, W, Hh);
  }

  window.setup = function (scene, sheet) {
    S = scene; M = sheet; W = S.width; Hh = S.height; bg = buildLayers();
    cv = document.createElement('canvas'); cv.width = W; cv.height = Hh; ctx = cv.getContext('2d');
    chr = document.createElement('canvas'); chr.width = W; chr.height = Hh; cctx = chr.getContext('2d');
    acc = document.getElementById('c'); acc.width = W; acc.height = Hh; actx = acc.getContext('2d');
  };

  // Siêu lấy mẫu theo thời gian: trung bình cộng `samples` khung con trong khoảng màn trập.
  window.renderFrame = function (f, samples, fmt) {
    const t0 = performance.now();
    const fps = S.fps, sh = S.motion_blur.shutter;
    for (let s = 0; s < samples; s++) {
      const off = samples === 1 ? 0 : sh * ((s + 0.5) / samples - 0.5);
      drawScene((f + off) / fps);
      actx.globalAlpha = 1 / (s + 1); actx.drawImage(cv, 0, 0);
    }
    actx.globalAlpha = 1;
    const t1 = performance.now();
    const url = acc.toDataURL(fmt || 'image/png');
    return { url, draw_ms: t1 - t0, encode_ms: performance.now() - t1 };
  };

  // Dùng cho thử nhất quán: xuất mặt nạ từng bộ phận.
  window.drawCharacter = (...a) => drawCharacter(...a);
})();

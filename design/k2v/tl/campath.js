// K2V tl · NGỮ PHÁP MÁY QUAY (port lab/timelapse camAt + đo): spline Hermite theo thời gian (tiếp tuyến Catmull-Rom không đều) qua mốc
// {t, p:[E,cao,N], l:[E,cao,N], fov}; bay dọc tuyến thật = mốc dày lấy mẫu trên hình học đường/sông (lệch tim tuyến đo lại mỗi khung);
// đo: khoảng cách tới đích (reveal/zoom-in ≥ 5×), tốc độ, quãng đứng yên (≤ 6 s), mỗi chuyển động gắn nhịp thông tin.
// (thuần JS — không import three: test được bằng Node, scripts/k2tl/tests/test_campath.mjs)

export function lineLen(L) { let s = 0; for (let i = 1; i < L.length; i++) s += Math.hypot(L[i][0] - L[i - 1][0], L[i][1] - L[i - 1][1]); return s; }
export function lineAt(L, s) { for (let i = 1; i < L.length; i++) { const l = Math.hypot(L[i][0] - L[i - 1][0], L[i][1] - L[i - 1][1]); if (s <= l || i === L.length - 1) { const u = Math.min(1, s / (l || 1)); return [L[i - 1][0] + (L[i][0] - L[i - 1][0]) * u, L[i - 1][1] + (L[i][1] - L[i - 1][1]) * u]; } s -= l; } return L[L.length - 1]; }
export function distToLine(L, e, n) { let m = Infinity; for (let i = 1; i < L.length; i++) { const [a, b] = [L[i - 1], L[i]], dx = b[0] - a[0], dn = b[1] - a[1], l2 = dx * dx + dn * dn || 1;
  const u = Math.max(0, Math.min(1, ((e - a[0]) * dx + (n - a[1]) * dn) / l2)); m = Math.min(m, Math.hypot(e - a[0] - u * dx, n - a[1] - u * dn)); } return m; }
// mốc dày dọc tuyến: từ quãng s0→s1 (m) trong [t0, t1], cao h (hoặc [h0,h1]), nhìn trước look m, nghiêng xuống dip m
// mốc thời gian chia đều [t0, t1] bước ≤ dt, LUÔN gồm t1 (V5b-2a: vòng t += dt bỏ sót t1 → máy đứng yên cuối cú)
export const times = (t0, t1, dt) => { const n = Math.max(1, Math.ceil((t1 - t0) / dt - 1e-9)); return [...Array(n + 1).keys()].map((i) => t0 + (t1 - t0) * i / n); };
export function alongLine(L, { s0, s1, t0, t1, h, look = 220, dip = 25, dt = 0.2, hAt = () => 0 }) {
  const K = [], H = Array.isArray(h) ? h : [h, h];
  for (const t of times(t0, t1, dt)) { const u = (t - t0) / (t1 - t0), s = s0 + (s1 - s0) * u, [e, n] = lineAt(L, s), [le, ln] = lineAt(L, s + Math.sign(s1 - s0) * look);
    const hh = H[0] + (H[1] - H[0]) * u; K.push({ t: +t.toFixed(4), p: [e, hAt(e, n) + hh, n], l: [le, hAt(le, ln) + hh - dip, ln], line: true }); }
  return K;
}
export function makeCamPath(keys) {
  const K = keys.slice().sort((a, b) => a.t - b.t);
  const val = (k, f, i) => (f === 'fov' ? (k.fov ?? 38) : k[f][i]);
  function at(t) {
    if (t <= K[0].t) t = K[0].t; if (t >= K[K.length - 1].t) t = K[K.length - 1].t;
    let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
    const a = K[i], b = K[i + 1], hh = b.t - a.t, u = (t - a.t) / hh, u2 = u * u, u3 = u2 * u;
    const H = (f, j) => { const p0 = val(a, f, j), p1 = val(b, f, j);
      const m0 = i > 0 ? (p1 - val(K[i - 1], f, j)) / (b.t - K[i - 1].t) : (p1 - p0) / hh, m1 = i + 2 < K.length ? (val(K[i + 2], f, j) - p0) / (K[i + 2].t - a.t) : (p1 - p0) / hh;
      return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * hh * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * hh * m1; };
    return { p: [0, 1, 2].map((j) => H('p', j)), l: [0, 1, 2].map((j) => H('l', j)), fov: H('fov', 0), onLine: !!(a.line && b.line) };
  }
  return { at, keys: K };
}
export function applyCam(cam, c) { cam.position.set(c.p[0], c.p[1], -c.p[2]); cam.up.set(0, 1, 0); cam.lookAt(c.l[0], c.l[1], -c.l[2]); if (Math.abs(cam.fov - c.fov) > 1e-4) { cam.fov = c.fov; cam.updateProjectionMatrix(); } cam.updateMatrixWorld(); }
// nhật ký máy quay cả đoạn (không dựng hình): vị trí, điểm nhìn, năm, lệch tuyến, khoảng cách tới đích, tốc độ (m/s), tốc độ góc (°/s)
export function camLog(path, N, fps, yearAt, opt = {}) {
  const out = []; let prev = null;
  for (let f = 0; f < N; f++) { const t = f / fps, c = path.at(t), r = { f, t: +t.toFixed(3), year: +yearAt(t).toFixed(2), pos: c.p.map((v) => +v.toFixed(2)), look: c.l.map((v) => +v.toFixed(2)), fov: +c.fov.toFixed(2) };
    if (opt.line && c.onLine) r.dev_m = +distToLine(opt.line, c.p[0], c.p[2]).toFixed(2);
    for (const [k, p] of Object.entries(opt.focus || {})) r['d_' + k] = +Math.hypot(c.p[0] - p[0], c.p[1] - p[1], c.p[2] - p[2]).toFixed(1);
    if (prev) { r.v = +(Math.hypot(...c.p.map((v, i) => v - prev.p[i])) * fps).toFixed(2);
      const d0 = prev.l.map((v, i) => v - prev.p[i]), d1 = c.l.map((v, i) => v - c.p[i]), n0 = Math.hypot(...d0), n1 = Math.hypot(...d1);
      r.w = +(Math.acos(Math.min(1, d0.reduce((s, v, i) => s + v * d1[i], 0) / (n0 * n1))) * 180 / Math.PI * fps).toFixed(2); }
    out.push(r); prev = c; }
  let run = 0, maxStill = 0; for (const r of out) { if ((r.v ?? 1) < 0.5 && (r.w ?? 1) < 0.3) { run++; maxStill = Math.max(maxStill, run); } else run = 0; }
  return { frames: out, max_still_s: +(maxStill / fps).toFixed(2) };
}

// ======================================================================================================================================
// V5b-2a · NGỮ PHÁP MÁY (chủ dự án duyệt 16/10: JJ1, KK1, HH2). Mỗi preset trả một "cú" { preset, vai, t:[t0,t1], keys, phases:[{kind, t:[a,b]}], route?, hero?, subject? }.
//  vai ∈ VAI (cơ chế / bước ngoặt / hệ quả) — cú máy phải gắn một vai trong mạch kể, không bay "trôi".
//  phases.kind quyết SPP (sppOf): bay nhanh (fly/ramp/follow/trace) → SPP1 · orbit/pin/hero → SPP4 · còn lại → SPP2.
//  grammarLog() ghi mỗi khung: preset, vai, pha, độ cao so mặt đất (AGL), tốc độ năm (năm/s), tốc độ góc (°/s); tổng kết mỗi cú so LIMITS.
// ======================================================================================================================================
export const VAI = ['co-che', 'buoc-ngoat', 'he-qua'];
// HH2: độ cao bay TUYẾN so mặt đất theo loại tuyến — phố ≤ 120 m; eo đất / sông / đại lộ rộng ≤ 300 m
export const ALT_MAX = { pho: 120, eo_dat: 300, song: 300, dai_lo: 300 };
export const LIMITS = { year_rate: 10, ang_rate: 90, orbit_s: [4, 6], pin_s: [1.5, 2.0], hero_pct: 25 };
const FAST = new Set(['fly', 'ramp', 'follow', 'trace']), HI = new Set(['orbit', 'pin', 'hero']);
export const sppOf = (kind) => (HI.has(kind) ? 4 : FAST.has(kind) ? 1 : 2);
const r4 = (v) => +v.toFixed(4), lerp3 = (a, b, u) => a.map((v, i) => v + (b[i] - v) * u);
const ez = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
function shot(preset, vai, t0, t1, keys, phases, extra = {}) {
  if (!VAI.includes(vai)) throw new Error(`preset ${preset}: vai "${vai}" không thuộc ${VAI.join('/')}`);
  return Object.assign({ preset, vai, t: [t0, t1], keys, phases }, extra);
}
// quãng đường dọc tuyến theo thời gian với hồ sơ tốc độ: 'const' (đều) | 'ramp' (tăng tốc rồi hãm — speed ramp, đỉnh ×k ở giữa)
function sProfile(u, kind, k = 2.4) {
  if (kind !== 'ramp') return u;
  // vận tốc v(u) = 1 + (k−1)·sin²(πu) → tích phân chuẩn hoá; tăng tốc vào giữa, hãm êm ra cuối (vào orbit không giật)
  const F = (x) => x + (k - 1) * (x / 2 - Math.sin(2 * Math.PI * x) / (4 * Math.PI)); return F(u) / F(1);
}
// mốc quỹ đạo tròn quanh tâm c=[E,h,N] (h: điểm nhìn, so mặt đất): bán kính r, cao h (AGL), góc a0→a1 (độ, 0 = Đông, ngược chiều kim đồng hồ nhìn từ trên)
export function orbitKeys({ c, r, h, a0, a1, t0, t1, fov, dt = 0.1, hAt = () => 0, look = 0, prof = 'lin' }) {
  const K = [], gc = hAt(c[0], c[2]);
  for (const t of times(t0, t1, dt)) { const u = (t - t0) / (t1 - t0), w = prof === 'ease' ? 0.5 - 0.5 * Math.cos(Math.PI * u) : u, a = (a0 + (a1 - a0) * w) * Math.PI / 180;
    const e = c[0] + r * Math.cos(a), n = c[2] + r * Math.sin(a); K.push({ t: r4(t), p: [e, hAt(e, n) + (Array.isArray(h) ? h[0] + (h[1] - h[0]) * u : h), n], l: [c[0], gc + c[1] + look, c[2]], fov: Array.isArray(fov) ? fov[0] + (fov[1] - fov[0]) * u : fov }); }
  return K;
}
// 1) LIÊN HOÀN (JJ1): bay thấp dọc tuyến thật → speed ramp → orbit quanh hero (4–6 s, năm dừng 1,5–2 s, hero ≥ 25 % khung) → crane up trung cảnh → rise-and-reveal
//    route: { line:[[E,N]…], type: ALT_MAX khoá, nguon }, fly: {s0, s1, t:[a,b], h (AGL), look, dip}, ramp: {s1, t1, k}, orbit: {c, r, h, a0, a1, t1, fov}, crane: {t1, h}, reveal: {t1, p, l, fov}
export function lienHoan({ vai, route, fly, ramp, orbit, crane, reveal, hAt = () => 0, pin }) {
  const [tf0, tf1] = fly.t, H = Array.isArray(fly.h) ? fly.h : [fly.h, fly.h];
  if (H[1] > ALT_MAX[route.type] || H[0] > ALT_MAX[route.type]) throw new Error(`liên hoàn: bay ${H} m > ${ALT_MAX[route.type]} m (${route.type})`);
  const K = [], dir = Math.sign(fly.s1 - fly.s0), look = fly.look ?? 260, dip = fly.dip ?? 30;
  // điểm nhìn: phía trước dọc tuyến (look m, hạ dip m) hoặc hướng về đích fly.target (TL-Q2: đích lệch trục ≤ 10°) cách máy fly.r m, nghiêng xuống fly.pitch (tỉ lệ)
  const at = (s, hh) => { const [e, n] = lineAt(route.line, s), p = [e, hAt(e, n) + hh, n];
    if (fly.target) { const d = [fly.target[0] - e, fly.target[2] - n], dl = Math.hypot(...d), R = fly.r ?? 520; return { p, l: [e + d[0] / dl * R, p[1] - (fly.pitch ?? 0.25) * R, n + d[1] / dl * R] }; }
    const [le, ln] = lineAt(route.line, s + dir * look); return { p, l: [le, hAt(le, ln) + hh - dip, ln] }; };
  for (const t of times(tf0, tf1, 0.2)) { const u = (t - tf0) / (tf1 - tf0); K.push(Object.assign({ t: r4(t), line: true, fov: fly.fov }, at(fly.s0 + (fly.s1 - fly.s0) * u, H[0] + (H[1] - H[0]) * u))); }
  // speed ramp: tiếp tục dọc tuyến, tăng tốc rồi hãm; điểm nhìn chuyển dần từ "phía trước" sang tâm hero (không quét gắt)
  const tr0 = tf1, tr1 = ramp.t1, sR0 = fly.s1, vFly = (fly.s1 - fly.s0) / (tf1 - tf0), sR1 = ramp.s1 ?? sR0 + vFly * (tr1 - tr0) * 1.6;
  const oc = orbit.c, gc = hAt(oc[0], oc[2]), oL = [oc[0], gc + oc[1] + (orbit.look || 0), oc[2]];
  const o0 = orbitKeys(Object.assign({ hAt, t0: tr1, t1: orbit.t1 }, orbit));
  for (const t of times(tr0, tr1, 0.2).slice(1, -1)) { const u = (t - tr0) / (tr1 - tr0), s = sR0 + (sR1 - sR0) * sProfile(u, 'ramp', ramp.k ?? 2.4), w = ez(u);
    const a = at(s, H[1] + (o0[0].p[1] - hAt(o0[0].p[0], o0[0].p[2]) - H[1]) * w), p = lerp3(a.p, o0[0].p, w * w), l = lerp3(a.l, oL, ez(u * 1.15));
    K.push({ t: r4(t), p, l, fov: fly.fov + (orbit.fov - fly.fov) * w }); }
  K.push(...o0);
  // crane up: giữ tâm nhìn hero, nâng máy thẳng đứng tới trung cảnh (h → crane.h AGL), lùi nhẹ theo bán kính
  const last = o0[o0.length - 1], tc1 = crane.t1, rv = [last.p[0] - oc[0], last.p[2] - oc[2]], rl = Math.hypot(...rv);
  for (const t of times(orbit.t1 + 0.2, tc1, 0.2)) { const u = ez((t - orbit.t1) / (tc1 - orbit.t1)), k = 1 + 0.35 * u, e = oc[0] + rv[0] * k, n = oc[2] + rv[1] * k;
    K.push({ t: r4(t), p: [e, last.p[1] + (hAt(e, n) + crane.h - last.p[1]) * u, n], l: crane.l ? lerp3(last.l, crane.l, u) : last.l.slice(), fov: orbit.fov + ((crane.fov ?? orbit.fov) - orbit.fov) * u }); }
  // rise-and-reveal: kéo lùi + lên, tâm nhìn trượt từ hero sang đích reveal (La Línea / vịnh)
  const cEnd = K[K.length - 1], rvK = reveal.keys || [{ t: reveal.t1, p: reveal.p, l: reveal.l, fov: reveal.fov }];
  K.push(...rvK.map((k) => Object.assign({}, k, { t: r4(k.t) })));
  const phases = [{ kind: 'fly', t: [tf0, tf1] }, { kind: 'ramp', t: [tr0, tr1] }, { kind: 'orbit', t: [tr1, orbit.t1] }, { kind: 'crane', t: [orbit.t1, tc1] }, { kind: 'reveal', t: [tc1, rvK[rvK.length - 1].t] }];
  if (pin) phases.splice(3, 0, { kind: 'pin', t: pin, inside: 'orbit' });
  return shot('lien-hoan', vai, tf0, rvK[rvK.length - 1].t, K, phases, { route, hero: { id: orbit.heroId, c: oL }, orbit_s: +(orbit.t1 - tr1).toFixed(2), crane_from: cEnd.p });
}
// 2) PUSH-IN GIỮ HƠI: tiến chậm vào chủ thể (ease-out), rồi "giữ hơi" — trôi rất chậm (không đứng yên) hold giây cuối
export function pushIn({ vai, from, to, look, t0, t1, hold = 1.2, fov, fov1 }) {
  const K = [], tm = t1 - hold;
  for (const t of times(t0, t1, 0.2)) { const u = t <= tm ? 1 - Math.pow(1 - (t - t0) / (tm - t0), 2) : 1, d = t > tm ? (t - tm) / hold : 0;
    const p = lerp3(from, to, u * 0.99 + d * 0.01); /* giữ hơi: 1 % quãng đường trôi trong hold (không đứng yên) */ K.push({ t: r4(t), p, l: look, fov: fov + ((fov1 ?? fov) - fov) * Math.min(1, (t - t0) / (t1 - t0)) }); }
  return shot('push-in', vai, t0, t1, K, [{ kind: 'push', t: [t0, tm] }, { kind: 'hero', t: [tm, t1] }], { subject: look });
}
// 3) BOUNDARY TRACE: bay dọc RANH GIỚI thật (biên giới/ranh hành chính/bờ cũ), nhìn chéo xuống để thấy hai bên; hai bên tô màu theo số (overlay3d.boundaryRibbons)
export function boundaryTrace({ vai, line, type = 'eo_dat', nguon, s0, s1, t0, t1, h, side = 1, off = 0, look = 200, dip = 70, fov = 34, hAt = () => 0 }) {
  if (h > ALT_MAX[type]) throw new Error(`boundary trace: ${h} m > ${ALT_MAX[type]} m`);
  const K = alongLine(line, { s0, s1, t0, t1, h, look, dip, dt: 0.2, hAt }).map((k) => Object.assign(k, { fov }));
  if (off) for (const k of K) { const s = s0 + (s1 - s0) * (k.t - t0) / (t1 - t0), [a, b] = [lineAt(line, s - 1), lineAt(line, s + 1)], d = [b[0] - a[0], b[1] - a[1]], l = Math.hypot(...d) || 1;
    k.p[0] += -d[1] / l * off * side; k.p[2] += d[0] / l * off * side; }
  return shot('boundary-trace', vai, t0, t1, K, [{ kind: 'trace', t: [t0, t1] }], { route: { line, type, nguon } });
}
// 4) FOLLOW-OBJECT: bám vật thể chuyển động (tàu/xe A-lite) — objAt(t) → {p:[E,y,N], dir:[dE,dN]}; máy sau-trên-bên, nhìn trước vật lookAhead m
export function follow({ vai, objAt, t0, t1, back = 40, up = 18, side = 10, lookAhead = 25, fov = 36, dt = 0.1 }) {
  const K = [];
  for (const t of times(t0, t1, dt)) { const o = objAt(t), [dx, dn] = o.dir, l = Math.hypot(dx, dn) || 1, ux = dx / l, un = dn / l;
    K.push({ t: r4(t), p: [o.p[0] - ux * back - un * side, o.p[1] + up, o.p[2] - un * back + ux * side], l: [o.p[0] + ux * lookAhead, o.p[1] + 1, o.p[2] + un * lookAhead], fov }); }
  return shot('follow-object', vai, t0, t1, K, [{ kind: 'follow', t: [t0, t1] }], { subject: 'objAt' });
}
// 5) LATERAL PARALLAX: máy trượt ngang (vuông góc trục nhìn) trước chủ thể — tiền cảnh trượt nhanh hơn hậu cảnh
export function lateral({ vai, c, yaw, dist, len, h, t0, t1, fov = 30, hAt = () => 0 }) {
  const K = [], a = yaw * Math.PI / 180, f = [Math.cos(a), Math.sin(a)], sd = [-f[1], f[0]], gc = hAt(c[0], c[2]);
  for (const t of times(t0, t1, 0.2)) { const u = (t - t0) / (t1 - t0) - 0.5, e = c[0] - f[0] * dist + sd[0] * len * u, n = c[2] - f[1] * dist + sd[1] * len * u;
    K.push({ t: r4(t), p: [e, hAt(e, n) + h, n], l: [c[0] + sd[0] * len * u * 0.35, gc + c[1], c[2] + sd[1] * len * u * 0.35], fov }); }
  return shot('lateral-parallax', vai, t0, t1, K, [{ kind: 'lateral', t: [t0, t1] }], { subject: c });
}
// 6) TOP-DOWN RISE: nhìn thẳng xuống (lệch 0,5° tránh suy biến lookAt), bay lên h0 → h1 và xoay chậm yaw0 → yaw1 (bản đồ sống)
export function topDownRise({ vai, c, h0, h1, t0, t1, yaw0 = 0, yaw1 = 15, fov = 40, hAt = () => 0 }) {
  const K = [], gc = hAt(c[0], c[2]);
  for (const t of times(t0, t1, 0.2)) { const u = ez((t - t0) / (t1 - t0)), h = h0 * Math.pow(h1 / h0, u), y = (yaw0 + (yaw1 - yaw0) * u) * Math.PI / 180, o = h * Math.tan(0.5 * Math.PI / 180);
    K.push({ t: r4(t), p: [c[0] - Math.cos(y) * o, gc + h, c[2] - Math.sin(y) * o], l: [c[0], gc, c[2]], fov }); }
  return shot('top-down-rise', vai, t0, t1, K, [{ kind: 'rise', t: [t0, t1] }], { subject: c });
}
// 7) VERTIGO (dolly zoom): máy lùi/tiến d0 → d1 dọc trục tới chủ thể, fov đổi để bề rộng chủ thể w (m) giữ nguyên: d·tan(fov/2) = w/2
export function vertigo({ vai, c, yaw, pitch = 12, d0, d1, w, t0, t1, hAt = () => 0 }) {
  const K = [], a = yaw * Math.PI / 180, pt = pitch * Math.PI / 180, gc = hAt(c[0], c[2]), L = [c[0], gc + c[1], c[2]];
  for (const t of times(t0, t1, 0.1)) { const u = ez((t - t0) / (t1 - t0)), d = d0 + (d1 - d0) * u, fov = 2 * Math.atan(w / 2 / d) * 180 / Math.PI;
    K.push({ t: r4(t), p: [L[0] - Math.cos(a) * Math.cos(pt) * d, L[1] + Math.sin(pt) * d, L[2] - Math.sin(a) * Math.cos(pt) * d], l: L.slice(), fov }); }
  return shot('vertigo', vai, t0, t1, K, [{ kind: 'vertigo', t: [t0, t1] }], { subject: L, w });
}
// ghép các cú (và mốc tự do ngoài preset) thành đường máy; phaseAt(t) → {shot, kind}; sppAt(t) theo pha
//  cuts: true → mỗi cú một spline riêng, nối bằng CẮT (cuộn minh hoạ preset; trong phim một cảnh liền dùng cuts: false)
export function grammar(shots, freeKeys = [], { cuts = false } = {}) {
  const keys = freeKeys.concat(...shots.map((s) => s.keys)).sort((a, b) => a.t - b.t);
  for (let i = 1; i < keys.length; i++) if (keys[i].t - keys[i - 1].t < 1e-3) throw new Error(`mốc máy trùng thời điểm ${keys[i].t} s`);
  let path = makeCamPath(keys);
  if (cuts) { const P = shots.map((s) => ({ t: s.t, p: makeCamPath(s.keys) })); path = { keys, at: (t) => { let q = P[0]; for (const x of P) if (t >= x.t[0] - 1e-6) q = x; return q.p.at(t); } }; }
  const phaseAt = (t) => { for (const s of shots) if (t >= s.t[0] - 1e-6 && t <= s.t[1] + 1e-6) { const ph = s.phases.find((p) => p.kind === 'pin' && t >= p.t[0] && t <= p.t[1]) || s.phases.find((p) => t >= p.t[0] - 1e-6 && t <= p.t[1] + 1e-6); return { shot: s, kind: ph ? ph.kind : 'free' }; } return { shot: null, kind: 'free' }; };
  return { path, shots, phaseAt, sppAt: (t, dflt = 2) => { const p = phaseAt(t); return p.shot ? sppOf(p.kind) : dflt; } };
}
// nhật ký ngữ pháp mỗi khung + tổng kết mỗi cú so LIMITS (không dựng hình; test Node được)
export function grammarLog(G, N, fps, yearAt, { hAt = () => 0, focus = {}, line, extra } = {}) {
  const base = camLog(G.path, N, fps, yearAt, { line, focus }), fr = base.frames;
  for (const r of fr) { const t = r.t, ph = G.phaseAt(t); r.preset = ph.shot ? ph.shot.preset : null; r.vai = ph.shot ? ph.shot.vai : null; r.phase = ph.kind; r.spp = ph.shot ? sppOf(ph.kind) : null;
    r.agl = +(r.pos[1] - hAt(r.pos[0], r.pos[2])).toFixed(1);
    r.yr_s = t > 0 ? +(Math.abs(yearAt(t) - yearAt(t - 1 / fps)) * fps).toFixed(2) : 0;   // sai phân lùi một khung (khung đầu cú bỏ khỏi tổng kết: có thể là CẮT)
    if (ph.shot && ph.shot.route && (ph.kind === 'fly' || ph.kind === 'trace')) r.route_dev_m = +distToLine(ph.shot.route.line, r.pos[0], r.pos[2]).toFixed(2);
    if (ph.shot && ph.shot.preset === 'vertigo') { const S = ph.shot.subject, d = Math.hypot(r.pos[0] - S[0], r.pos[1] - S[1], r.pos[2] - S[2]); r.vertigo_w = +(2 * d * Math.tan(r.fov / 2 * Math.PI / 180)).toFixed(2); }
    if (extra) Object.assign(r, extra(r)); }
  const sum = G.shots.map((s) => { const F = fr.filter((r) => r.t >= s.t[0] - 1e-6 && r.t <= s.t[1] + 1e-6), mv = F.slice(1);
    const flyF = F.filter((r) => r.phase === 'fly' || r.phase === 'trace'), alt = s.route ? ALT_MAX[s.route.type] : null;
    const pinF = F.filter((r) => r.phase === 'pin'), o = {
      preset: s.preset, vai: s.vai, t: s.t, frames: F.length,
      year_rate_max: Math.max(0, ...mv.filter((r) => r.phase !== 'pin').map((r) => r.yr_s)), ang_rate_max: Math.max(0, ...mv.map((r) => r.w ?? 0)),
      speed_max_ms: Math.max(0, ...mv.map((r) => r.v ?? 0)), agl_min: Math.min(...F.map((r) => r.agl)), agl_max: Math.max(...F.map((r) => r.agl)) };
    if (s.route) Object.assign(o, { route_type: s.route.type, route_src: s.route.nguon, alt_limit: alt, fly_agl_max: flyF.length ? Math.max(...flyF.map((r) => r.agl)) : null,
      fly_s: +(flyF.length / fps).toFixed(2), fly_dev_max: flyF.length ? Math.max(...flyF.map((r) => r.route_dev_m)) : null });
    if (s.orbit_s != null) o.orbit_s = s.orbit_s;
    if (pinF.length) { o.pin_s = +(pinF.length / fps).toFixed(2); o.pin_year = pinF[0].year; }
    if (s.preset === 'vertigo') { const ws = F.map((r) => r.vertigo_w); o.vertigo_w_dev_pct = +(100 * (Math.max(...ws) - Math.min(...ws)) / s.w).toFixed(2); o.fov = [F[0].fov, F[F.length - 1].fov]; }
    o.spp = [...new Set(F.map((r) => r.spp))];
    o.ok = { year_rate: o.year_rate_max <= LIMITS.year_rate, ang_rate: o.ang_rate_max <= LIMITS.ang_rate };
    if (alt != null && o.fly_agl_max != null) o.ok.alt = o.fly_agl_max <= alt;
    if (o.orbit_s != null) o.ok.orbit_s = o.orbit_s >= LIMITS.orbit_s[0] && o.orbit_s <= LIMITS.orbit_s[1];
    if (o.pin_s != null) o.ok.pin_s = o.pin_s >= LIMITS.pin_s[0] && o.pin_s <= LIMITS.pin_s[1];
    return o; });
  return Object.assign(base, { shots: sum, limits: LIMITS, alt_max: ALT_MAX });
}

// W3 (Cổng 5 v2, mặt Ida A-i) — rãnh rig mặt cho CLIP THỬ 3 s (72 khung, 24 fps): chớp mắt + khẩu hình "Goodnight" (vế cuối thoại L4 của s37).
// In ra JSON: mảng 72 phần tử, mỗi phần tử = trọng số TUYỆT ĐỐI các kênh rig (facerig.js CHANNELS) — page_layout_fl.js cộng vào preset của "expr" (clip: không truyền expr → {}).
// Khoá: [khung, {kênh: trọng số}]; giữa hai khoá nội suy smoothstep từng kênh (kênh vắng = 0).
// Khẩu hình (Cổng 6 dùng cùng bộ VISEMES): G ≈ E hẹp, "oo" = O, d/n/t = L/E nhẹ, "igh" = A → E. Nền: cười buồn dịu (s37).
const base = { smile: 0.5, cheekRaise: 0.35, browInnerUp: 0.55, squint: 0.25 };
const K = (f, w) => [f, { ...base, ...w }];
const KEYS = [
  K(0, {}), K(5, {}), K(6, { blink: 0.55 }), K(7, { blink: 1 }), K(8, { blink: 1 }), K(10, { blink: 0.3 }), K(11, {}),            // chớp 1
  K(15, {}),
  K(18, { smile: 0.3, cheekRaise: 0.3, browInnerUp: 0.6, squint: 0.2, jawOpen: 0.25, wide: 0.25 }),                               // G
  K(21, { smile: 0.1, cheekRaise: 0.2, browInnerUp: 0.6, squint: 0.2, jawOpen: 0.3, pucker: 0.85 }),                               // oo
  K(25, { smile: 0.1, cheekRaise: 0.2, browInnerUp: 0.6, squint: 0.2, jawOpen: 0.28, pucker: 0.8 }),
  K(28, { smile: 0.25, browInnerUp: 0.6, jawOpen: 0.28, wide: 0.2 }),                                                               // d
  K(31, { smile: 0.3, browInnerUp: 0.6, jawOpen: 0.15, wide: 0.3 }),                                                                // n
  K(35, { smile: 0.35, browInnerUp: 0.7, jawOpen: 0.62, wide: 0.25 }),                                                              // igh (A)
  K(39, { smile: 0.35, browInnerUp: 0.7, jawOpen: 0.58, wide: 0.3 }),
  K(42, { smile: 0.4, browInnerUp: 0.7, jawOpen: 0.35, wide: 0.5 }),                                                                // → i (E)
  K(45, { smile: 0.4, browInnerUp: 0.65, jawOpen: 0.18, wide: 0.35 }),                                                              // t
  K(48, { smile: 0.45, press: 0.25 }),                                                                                             // khép môi
  K(56, { smile: 0.6, browInnerUp: 0.7 }), K(62, { smile: 0.6, browInnerUp: 0.7 }),
  K(63, { smile: 0.6, browInnerUp: 0.7, blink: 0.6 }), K(64, { smile: 0.6, browInnerUp: 0.7, blink: 1 }), K(65, { smile: 0.6, browInnerUp: 0.7, blink: 1 }),   // chớp 2
  K(67, { smile: 0.6, browInnerUp: 0.7, blink: 0.35 }), K(68, { smile: 0.6, browInnerUp: 0.7 }), K(71, { smile: 0.6, browInnerUp: 0.7 }),
];
const ss = (t) => t * t * (3 - 2 * t);
const N = +(process.argv[2] || 72), track = [];
for (let f = 0; f < N; f++) {
  let j = 0; while (j < KEYS.length - 2 && KEYS[j + 1][0] <= f) j++;
  const [fa, a] = KEYS[j], [fb, b] = KEYS[Math.min(j + 1, KEYS.length - 1)], t = fb > fa ? ss(Math.max(0, Math.min(1, (f - fa) / (fb - fa)))) : 0;
  const w = {}; for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) { const v = (a[k] || 0) + ((b[k] || 0) - (a[k] || 0)) * t; if (Math.abs(v) > 1e-4) w[k] = +v.toFixed(4); }
  track.push(w);
}
process.stdout.write(JSON.stringify(track));

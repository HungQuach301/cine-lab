// Trang gỡ lỗi (không dùng khi render phim): bày tranh đầu/thân ở nhiều góc — màu, normal, và bản chiếu sáng thử (đèn ấm trái-trên + viền lạnh).
// node shared/render_still.js --page v2/char2d/dbg_sheet.js --frame x --out <dir> --w 1920 --h 1080 --args '{"who":"ida","part":"head"}'
import { paintView, paintRibbon, viewBasis, snap } from './paint2d.js';
import { DESIGNS, ribbonDesigns, prepare } from './designs.js';

let W, H, out;
window.setup = async (cfg) => {
  W = cfg.W; H = cfg.H;
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const g = cv.getContext('2d');
  g.fillStyle = '#404048'; g.fillRect(0, 0, W, H);
  const who = cfg.who || 'ida', part = cfg.part || 'head';
  const yaws = cfg.yaws || [0, 35, 70, 110, 150, 180, -40];
  const pitch = (cfg.pitch || 0) * Math.PI / 180;
  const res = cfg.res || 384;
  const cell = Math.floor(W / yaws.length);
  const toCanvas = (tex, w, h, mode) => {
    const d = tex.image.data, c = document.createElement('canvas'); c.width = w; c.height = h; const cg = c.getContext('2d'); const id = cg.createImageData(w, h);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) { const s = ((h - 1 - j) * w + i) * 4, o = (j * w + i) * 4; // v lên trên
      if (mode === 'rgb') { id.data[o] = d[s]; id.data[o + 1] = d[s + 1]; id.data[o + 2] = d[s + 2]; id.data[o + 3] = d[s + 3]; }
      else { id.data[o] = d[s]; id.data[o + 1] = d[s + 1]; id.data[o + 2] = d[s + 2]; id.data[o + 3] = 255; } }
    cg.putImageData(id, 0, 0); return c;
  };
  const lit = (map, nm, w, h) => {
    const a = map.image.data, n = nm.image.data, c = document.createElement('canvas'); c.width = w; c.height = h; const cg = c.getContext('2d'); const id = cg.createImageData(w, h);
    const L1 = [-0.55, 0.45, 0.7], L2 = [0.8, 0.3, -0.5]; const nl = (v) => { const l = Math.hypot(...v); return v.map((x) => x / l); }; const l1 = nl(L1), l2 = nl(L2);
    const lin = (x) => Math.pow(x / 255, 2.2), gam = (x) => 255 * Math.pow(Math.min(1, x), 1 / 2.2);
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) { const s = ((h - 1 - j) * w + i) * 4, o = (j * w + i) * 4;
      const N = [n[s] / 127.5 - 1, n[s + 1] / 127.5 - 1, n[s + 2] / 127.5 - 1];
      const d1 = Math.max(0, N[0] * l1[0] + N[1] * l1[1] + N[2] * l1[2]), d2 = Math.max(0, N[0] * l2[0] + N[1] * l2[1] + N[2] * l2[2]);
      const E = [1.1 * d1 + 0.25 * d2 * 0.7 + 0.12, 0.85 * d1 + 0.25 * d2 * 0.8 + 0.12, 0.6 * d1 + 0.25 * d2 * 1.1 + 0.16];
      for (let k = 0; k < 3; k++) id.data[o + k] = gam(lin(a[s + k]) * E[k]);
      id.data[o + 3] = a[s + 3]; }
    cg.putImageData(id, 0, 0); return c;
  };
  if (part === 'head' || part === 'torso') {
    const D = prepare(DESIGNS[who][part](), snap);
    yaws.forEach((y, k) => {
      const V = viewBasis(y * Math.PI / 180, pitch);
      const r = paintView(D, V, { c: D.frame.c, size: D.frame.size, W: res });
      if (cfg.big) { g.drawImage(toCanvas(r.map, res, res, 'rgb'), 0, 0, H, H); g.drawImage(lit(r.map, r.nmap, res, res), H, 0, H, H); return; }
      const sz = Math.min(cell, H / 3);
      g.drawImage(toCanvas(r.map, res, res, 'rgb'), k * cell, 0, sz, sz);
      g.drawImage(lit(r.map, r.nmap, res, res), k * cell, sz, sz, sz);
      g.drawImage(toCanvas(r.nmap, res, res, 'n'), k * cell, 2 * sz, sz, sz);
    });
  } else {
    const RD = ribbonDesigns(who === 'ida', false, await fetch('/model-sheet/' + who + '.json').then((r) => r.json()));
    let x = 0;
    for (const [k, o] of Object.entries(RD)) { const t = paintRibbon(o); const sc = Math.min(4, 500 / o.H); g.drawImage(toCanvas(t.map, o.W, o.H, 'rgb'), x, 0, o.W * sc, o.H * sc); g.drawImage(lit(t.map, t.nmap, o.W, o.H), x, 520, o.W * sc, o.H * sc); x += o.W * sc + 10; }
  }
  out = cv;
};
window.renderFrame = async () => ({ accum_ms: 0 });
window.finalize = () => {
  const d = out.getContext('2d').getImageData(0, 0, W, H).data; const rgb = new Uint8Array(W * H * 3);
  for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) { const s = ((H - 1 - j) * W + i) * 4, o = (j * W + i) * 3; rgb[o] = d[s]; rgb[o + 1] = d[s + 1]; rgb[o + 2] = d[s + 2]; }
  let bin = ''; for (let i = 0; i < rgb.length; i += 0x8000) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + 0x8000)); return btoa(bin);
};

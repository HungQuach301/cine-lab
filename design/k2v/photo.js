// KÊNH 2 · module C — ẢNH THẬT / VĂN BẢN / TIÊU ĐỀ BÁO (k2v/photo). Tư liệu thật đặt trong không gian thật: bản in trên bàn lưu trữ, trang văn bản dưới đèn bàn.
// Luật nguồn (channel-k2/QUAN-TRI-RUI-RO.md §6): chỉ ảnh/văn bản đã kiểm giấy phép từng tệp (scripts/k2/k2v_assets.py ghim SHA), không commit media bên thứ ba,
// không tạo mặt người thật bằng AI, giữ màu gốc của ảnh lưu trữ (không tô màu, không "phục chế" mặt). Chú thích (tên + năm + nguồn) do lớp 2D vẽ (p.cap / p.src).
//
// Cảnh và API (opt; thời điểm = giây trong cảnh):
//   photo/print    img:'/cache/<id>.jpg', focus:[u,v] (điểm chính của ảnh, 0..1 từ trên-trái — Ken Burns tiến về đây), push: 0.18 (độ tiến),
//                  mat: true (bìa passe-partout), surface: 'desk'|'wall', cam: [...] (ghi đè Ken Burns tự động)
//                  neo: 'focus', 'print:bl', 'print:br', 'print:top'
//   photo/doc      page: '/cache/<id>-pN.json' (từ k2v_assets.py doc: ảnh trang + khung highlight), hl: [{i, at:[t0,t1], color}] (quét theo dòng),
//                  focus: i (khung highlight máy quay tiến tới), cam: [...]
//                  neo: 'hl<i>' (mép phải dòng cuối của highlight i), 'page:top'
//   photo/headline paper:'Name of paper' (chữ thường, KHÔNG dùng logo/măng-sét), date:'22 Sep 2025', head:'Headline text…' (nguyên văn tít), kicker,
//                  dur ≤ 3 s (QUAN-TRI-RUI-RO §6: báo hiện đại = VÀNG), thân bài là các dòng xám làm mờ (không chữ thật), không ảnh trong bài
//                  neo: 'head'
import { THREE, C, cl, lerp, eo, ease, win, camRig, canvasTex, loadImg, loadJSON, rng } from './common.js';

// Mặt bàn lưu trữ: vải lanh/da sẫm (thủ tục, tất định), vũng sáng đèn bàn ấm
function desk(scene, { tone = '#2a231d', size = 40 } = {}) {
  scene.background = new THREE.Color('#07080b');
  const t = canvasTex(2048, 2048, (g, w, h) => { g.fillStyle = tone; g.fillRect(0, 0, w, h); const R = rng(3);
    for (let i = 0; i < 60000; i++) { const x = R() * w, y = R() * h, l = 2 + R() * 10; g.strokeStyle = `rgba(${R() < 0.5 ? '255,240,220' : '0,0,0'},${0.025 + 0.03 * R()})`; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (R() < 0.5 ? l : 0), y + (R() < 0.5 ? 0 : l)); g.stroke(); } });
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(4, 4);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.MeshPhysicalMaterial({ map: t, roughness: 0.9, specularIntensity: 0.25 })); fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; scene.add(fl);
  scene.add(new THREE.HemisphereLight('#c9d4e6', '#20160e', 0.35));
  const lamp = new THREE.SpotLight('#ffe2bd', 220, 40, 0.75, 0.85, 1.4); lamp.position.set(-3.2, 7.5, 2.6); lamp.target.position.set(0.2, 0, -0.2); lamp.castShadow = true; lamp.shadow.mapSize.set(2048, 2048); lamp.shadow.bias = -0.0004; lamp.shadow.radius = 5;
  scene.add(lamp, lamp.target);
  const fill = new THREE.DirectionalLight('#9fb4d8', 0.35); fill.position.set(6, 5, 6); scene.add(fill);
  return { fl, lamp };
}
// tờ giấy/bản in hơi cong (không phẳng tuyệt đối), dày nhẹ; mặt trên dùng texture
function sheet(w, h, map, { curl = 0.012, rough = 0.62, back = '#e8e1d2' } = {}) {
  const g = new THREE.PlaneGeometry(w, h, 48, 48), P = g.attributes.position;
  for (let i = 0; i < P.count; i++) { const x = P.getX(i) / (w / 2), y = P.getY(i) / (h / 2); P.setZ(i, 0.006 + curl * (x * x * 0.6 + y * y * 0.4) * Math.max(w, h)); }   // +6 mm trên tấm đáy: tránh z-fight (vết đen giữa tờ)
  g.computeVertexNormals(); g.rotateX(-Math.PI / 2);
  const m = new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({ map, roughness: rough, specularIntensity: 0.35, side: THREE.FrontSide })); m.castShadow = false; m.receiveShadow = false;   // tờ cong tự đổ bóng → vết đen (bóng do tấm đáy đổ)
  const b = new THREE.Mesh(new THREE.BoxGeometry(w, 0.008, h), new THREE.MeshStandardMaterial({ color: back, roughness: 0.9 })); b.position.y = -0.006; b.castShadow = true;
  const grp = new THREE.Group(); grp.add(m, b); return grp;
}
// Ken Burns có thị sai: máy quay trên bản in, tiến chậm về điểm chính (focus), lệch ngang nhẹ
function kenburns(W, H, dur, { cx = 0, cz = 0, size = 3, focus = [0, 0], push = 0.18, tilt = 0.32, mm = 50, preset = 'push' }) {
  if (preset !== 'push' && PHOTO_PRESETS[preset]) return PHOTO_PRESETS[preset]({ dur, size, focus, mm });
  const fov = 2 * Math.atan(12 / mm), dist = (size * 0.62) / Math.tan(fov / 2), fx = focus[0], fz = focus[1];
  const k0 = { t: 0, p: [cx - 0.12, dist * Math.cos(tilt), cz + dist * Math.sin(tilt)], l: [cx, 0, cz], mm };
  const d1 = dist * (1 - push), k1 = { t: dur, p: [lerp(cx, fx, 0.5) + 0.1, d1 * Math.cos(tilt * 0.85), lerp(cz, fz, 0.5) + d1 * Math.sin(tilt * 0.85)], l: [lerp(cx, fx, 0.55), 0, lerp(cz, fz, 0.55)], mm };
  return [k0, k1];
}

// Thư viện góc máy cho ảnh/văn bản (camera_id = tên preset; mặc định 'push' = Ken Burns tiến về điểm chính)
const hgt = (size, mm, k = 0.62) => (size * k) / Math.tan(Math.atan(12 / mm));
export const PHOTO_PRESETS = {
  push: null,
  pull: ({ dur, size, focus: [fx, fz], mm }) => { const d = hgt(size, mm); return [{ t: 0, p: [fx, d * 0.62, fz + d * 0.2], l: [fx, 0, fz], mm }, { t: dur, p: [0, d * 0.95, d * 0.31], l: [0, 0, 0], mm }]; },
  'drift-l': ({ dur, size, mm }) => { const d = hgt(size, mm, 0.5); return [{ t: 0, p: [0.35, d, d * 0.3], l: [0.25, 0, 0], mm }, { t: dur, p: [-0.35, d, d * 0.3], l: [-0.25, 0, 0], mm }]; },
  'drift-r': ({ dur, size, mm }) => { const d = hgt(size, mm, 0.5); return [{ t: 0, p: [-0.35, d, d * 0.3], l: [-0.25, 0, 0], mm }, { t: dur, p: [0.35, d, d * 0.3], l: [0.25, 0, 0], mm }]; },
  'tilt-low': ({ dur, size, focus: [fx, fz], mm }) => { const d = hgt(size, mm, 0.55); return [{ t: 0, p: [fx - 0.3, d * 0.42, fz + d * 0.95], l: [fx, 0, fz - 0.2], mm }, { t: dur, p: [fx + 0.2, d * 0.38, fz + d * 0.85], l: [fx, 0, fz - 0.2], mm }]; },
  detail: ({ dur, size, focus: [fx, fz], mm }) => { const d = hgt(size, mm, 0.24); return [{ t: 0, p: [fx - 0.08, d, fz + d * 0.25], l: [fx - 0.05, 0, fz], mm }, { t: dur, p: [fx + 0.08, d * 0.94, fz + d * 0.23], l: [fx + 0.05, 0, fz], mm }]; },
  top: ({ dur, size, mm }) => { const d = hgt(size, mm, 0.56); return [{ t: 0, p: [0, d * 1.04, 0.01], l: [0, 0, 0], mm }, { t: dur, p: [0, d, 0.01], l: [0, 0, 0], mm }]; },
};

export const HEROES = {
  async print({ W, H, dur, opt: o = {} }) {
    const scene = new THREE.Scene(); desk(scene, { tone: o.tone || '#2b241e' });
    const im = await loadImg(o.img), ar = im.naturalWidth / im.naturalHeight, ph = o.h || 2.6, pw = ph * ar;
    const tex = canvasTex(im.naturalWidth, im.naturalHeight, (g, w, h) => { g.drawImage(im, 0, 0, w, h); });
    const mat = o.mat !== false, mw = pw + (mat ? 0.62 : 0), mh = ph + (mat ? 0.62 : 0);
    const board = sheet(mw, mh, canvasTex(1024, Math.round(1024 * mh / mw), (g, w, h) => { g.fillStyle = '#e9e2d1'; g.fillRect(0, 0, w, h); const R = rng(9);
      for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(120,100,70,${0.02 * R()})`; g.fillRect(R() * w, R() * h, 2, 2); }
      const bx = (0.31 / mw) * w, by = (0.31 / mh) * h; g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(bx - 3, by - 3, w - 2 * bx + 6, h - 2 * by + 6); }), { curl: 0.004, back: '#cfc6b2' });
    board.rotation.y = o.rot ?? -0.035; board.position.y = o.lift ?? 0; scene.add(board);   // lift (V2b): nâng bản in khỏi mặt bàn → bóng đổ rõ dưới đèn bàn
    const pr = sheet(pw, ph, tex, { curl: 0.006, rough: 0.55 }); pr.position.y = 0.012; board.add(pr);
    const F = o.focus || [0.5, 0.35], fx = (F[0] - 0.5) * pw, fz = (F[1] - 0.5) * ph;
    const keys = o.cam || kenburns(W, H, dur, { size: mh, focus: [fx, fz], push: o.push ?? 0.2, mm: o.mm || 50, preset: o.preset || 'push' });
    const { cam, at } = camRig(W, H, keys, dur);
    const wp = (x, z) => { const v = new THREE.Vector3(x, 0.03, z); board.localToWorld(v); return v; };
    return { scene, cam, grade: o.grade || 'archive', exposure: o.exposure || 1.05,
      anchors: { focus: () => wp(fx, fz), 'print:bl': () => wp(-pw / 2, ph / 2), 'print:br': () => wp(pw / 2, ph / 2), 'print:top': () => wp(0, -ph / 2) },
      update(t) { at(t); } };
  },
  async doc({ W, H, dur, opt: o = {} }) {
    const scene = new THREE.Scene(); desk(scene, { tone: o.tone || '#23262c' });
    const meta = await loadJSON(o.page), im = await loadImg(o.page.replace(/\.json$/, '.png'));
    const ph = o.h || 3.4, pw = ph * meta.aspect;
    const tex = canvasTex(im.naturalWidth, im.naturalHeight, (g, w, h) => g.drawImage(im, 0, 0, w, h));
    const page = sheet(pw, ph, tex, { curl: 0.008, rough: 0.7, back: '#f2f2ee' }); page.children[0].material.color.set(o.paper || '#e6e2d8');   /* giấy bớt chói dưới đèn bàn */ page.rotation.y = o.rot ?? 0.05; scene.add(page);
    // highlight: dải hổ phách trong suốt sát mặt giấy, quét trái → phải theo từng dòng trong [t0, t1]
    const hls = [], anchors = {};
    const toLocal = (u, v) => [(u - 0.5) * pw, (v - 0.5) * ph];
    for (const h of o.hl || []) { const H2 = meta.hl[h.i]; if (!H2) continue; const rows = [];
      for (const [x0, y0, x1, y1] of H2.rects) { const [a, b] = toLocal(x0 - 0.004, y0 - 0.002), [c, d] = toLocal(x1 + 0.004, y1 + 0.003);
        const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: h.color || C.amber, transparent: true, opacity: 0.62, depthWrite: false }) /* bút dạ quang: phủ thường (Multiply quá nhạt trên giấy trắng) */);
        m.rotation.x = -Math.PI / 2; m.position.set(a, 0.02, (b + d) / 2); m.userData = { a, c, len: c - a, hz: d - b }; m.scale.set(0.0001, d - b, 1); page.add(m); rows.push(m); }
      hls.push({ h, rows }); const last = H2.rects[H2.rects.length - 1], [lx, lz] = toLocal(last[2], (last[1] + last[3]) / 2);
      anchors['hl' + h.i] = () => { const v = new THREE.Vector3(lx, 0.03, lz); page.localToWorld(v); return v; }; }
    anchors['page:top'] = () => { const v = new THREE.Vector3(0, 0.03, -ph / 2); page.localToWorld(v); return v; };
    let keys = o.cam;
    if (!keys) { const fi = o.focus ?? (o.hl && o.hl[0] && o.hl[0].i) ?? 0, R0 = meta.hl[fi] ? meta.hl[fi].rects[0] : [0.3, 0.3, 0.7, 0.32], [fx, fz] = toLocal((R0[0] + R0[2]) / 2, R0[1]);
      keys = kenburns(W, H, dur, { size: ph, focus: [fx, fz], push: o.push ?? 0.45, mm: o.mm || 50, tilt: 0.42, preset: o.preset || 'push' }); }
    const { cam, at } = camRig(W, H, keys, dur);
    return { scene, cam, grade: o.grade || 'info', exposure: o.exposure || 1.0, anchors,
      update(t) { at(t);
        for (const { h, rows } of hls) { const u = win(h.at, t), tot = rows.reduce((s, m) => s + m.userData.len, 0); let acc = 0;
          for (const m of rows) { const f = cl((u * tot - acc) / m.userData.len); acc += m.userData.len; m.scale.x = Math.max(0.0001, f * m.userData.len); m.position.x = m.userData.a + m.scale.x / 2; m.visible = f > 0; } } } };
  },
  async headline({ W, H, dur, opt: o = {} }) {
    const scene = new THREE.Scene(); desk(scene, { tone: o.tone || '#23262c' });
    const TW = 2400, TH = 1600, R = rng(21);
    const tex = canvasTex(TW, TH, (g, w, h) => {
      g.fillStyle = '#f4f1ea'; g.fillRect(0, 0, w, h);
      g.fillStyle = '#1c1c1c'; g.font = '600 46px "Inter", sans-serif'; g.fillText(o.paper || 'Newspaper', 120, 120);   // tên báo: chữ thường, không măng-sét/logo
      g.fillStyle = '#5c5c5c'; g.font = '500 38px "Inter", sans-serif'; g.fillText(o.date || '', 120, 180);
      g.fillStyle = '#1c1c1c'; g.fillRect(120, 214, w - 240, 4);
      if (o.kicker) { g.fillStyle = '#9b3d1a'; g.font = '700 36px "Inter", sans-serif'; g.fillText(o.kicker.toUpperCase(), 120, 290); }
      // tít: ngắt dòng trong khung
      g.fillStyle = '#121212'; g.font = 'bold 92px "DejaVu Serif", serif'; const words = (o.head || '').split(' '); let line = '', y = o.kicker ? 400 : 340;
      for (const wd of words) { const tst = line ? line + ' ' + wd : wd; if (g.measureText(tst).width > w - 240 && line) { g.fillText(line, 120, y); y += 108; line = wd; } else line = tst; } if (line) g.fillText(line, 120, y);
      // thân bài: dòng xám ngẫu nhiên trên canvas nhỏ rồi phóng to → mờ, không có chữ thật
      const s = document.createElement('canvas'); s.width = 300; s.height = 140; const q = s.getContext('2d'); q.fillStyle = '#f4f1ea'; q.fillRect(0, 0, 300, 140);
      for (let c = 0; c < 3; c++) for (let r = 0; r < 18; r++) { q.fillStyle = 'rgba(40,40,40,0.55)'; q.fillRect(8 + c * 98, 6 + r * 7.4, 86 * (r % 6 === 5 ? 0.5 + 0.3 * R() : 0.92 + 0.08 * R()), 2.6); }
      g.imageSmoothingEnabled = true; g.drawImage(s, 0, 0, 300, 140, 120, y + 80, w - 240, h - y - 140); });
    const pw = 4.2, ph = pw * TH / TW, sh = sheet(pw, ph, tex, { curl: 0.01, rough: 0.8, back: '#ecebe6' }); sh.rotation.y = o.rot ?? -0.06; scene.add(sh);
    const keys = o.cam || [{ t: 0, p: [-0.5, 4.4, 2.9], l: [-0.15, 0, -0.45], mm: 50 }, { t: dur, p: [-0.25, 4.0, 2.6], l: [-0.05, 0, -0.5], mm: 50 }];
    const { cam, at } = camRig(W, H, keys, dur);
    return { scene, cam, grade: o.grade || 'info', exposure: o.exposure || 1.0,
      anchors: { head: () => { const v = new THREE.Vector3(0, 0.03, -ph * 0.25); sh.localToWorld(v); return v; } }, update(t) { at(t); } };
  },
};

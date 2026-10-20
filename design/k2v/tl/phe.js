// K2V tl · V7B (19/10/2026, việc 2 — AI GIỮ ROCK đọc được khi tắt tiếng; chủ dự án duyệt V7P-D4) · PHE TRÊN HÌNH:
//  · shipFlags(F, phe, ctx)  — cờ đuôi tàu theo phe cho một hạm đội makeFleet (gb: Red Ensign 1707–1800 · es: cờ hải quân trắng + huy hiệu Bourbon 1701–1785 · fr: cờ trắng);
//                              cỡ thật ước ≈ 8 × 4 m (bậc 4, chưa có nguồn số cỡ cờ từng tàu) × scale ≤ 1,5; soái hạm (flag: true) thêm cờ đỉnh cột chính cùng mẫu.
//  · rims(list, ctx)         — VIỀN MÀU PHE nhẹ quanh khối quân / tàu khi máy > 1 km (màu phe cố định BIBLE §11.1: Anh #b03a2e, TBN #c9a227, Pháp #2e5c8a):
//                              vòng elip mỏng nằm sát mặt đất/nước, mờ dần 800 → 1 200 m theo khoảng cách máy, không vào mặt nạ nội dung (ctx.maskHide).
//  Không chữ, không biểu tượng chế độ làm màu tô; viền là dấu kiểu bản đồ, không phải vật trong cảnh (ghi ở log cảnh + báo cáo).
import { THREE } from './core.js';
import { flagTex } from './props.js';

export const PHE = { gb: '#b03a2e', es: '#c9a227', fr: '#2e5c8a' };
const ENSIGN = { gb: 'red_ensign1707', es: 'es_naval1701', fr: 'fr_white' };

export function shipFlags(F, phe, ctx, { scale = 1.5, w0 = 8, toward = 100 } = {}) {
  const U = { uT: { value: 0 } }, sc = Math.min(1.5, scale), w = w0 * sc, h = w / 2, tex = flagTex(ENSIGN[phe] || 'red_ensign1707');
  const m = new THREE.MeshLambertMaterial({ map: tex, side: THREE.DoubleSide });
  m.onBeforeCompile = (sh) => { sh.uniforms.uT = U.uT; sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float uT;')
    .replace('#include <begin_vertex>', `#include <begin_vertex>\n float fx = clamp(position.x / ${w.toFixed(2)}, 0.0, 1.0); transformed.z += sin(position.x * 0.9 - uT * 5.0) * 0.45 * fx; transformed.y -= 0.35 * fx * fx;`);
    sh.fragmentShader = sh.fragmentShader.replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n totalEmissiveRadiance += diffuseColor.rgb * 0.35;'); };   // vải xuyên sáng: cờ ngược nắng vẫn đọc được màu
  m.customProgramCacheKey = () => 'v7b-ship-flag-' + w.toFixed(2); ctx.maskify(m, ctx.U, 1);
  const geo = new THREE.PlaneGeometry(w, h, 10, 2).translate(w / 2, -h / 2, 0), pm = new THREE.MeshLambertMaterial({ color: 0x3a2a1e }); ctx.maskify(pm, ctx.U, 1);
  let n = 0;
  for (const { sp, g } of F.list) {
    const len = sp.kind === 'line' ? 56 : sp.kind === 'battery' ? 54 : 36, staff = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.16, 9, 4).translate(0, 4.5, 0), pm); staff.position.set(-len / 2 - 0.5, 5, 0); g.add(staff);
    const cl = new THREE.Mesh(geo, m); cl.position.set(-len / 2 - 0.5, 13.8, 0); cl.rotation.y = Math.PI; g.add(cl); n++;   // cờ đuôi bay về phía sau tàu
    if (sp.flag) { const top = new THREE.Mesh(geo, m); top.position.set(0, 2 + 34 + 0.5, 0); top.rotation.y = Math.PI; g.add(top); n++; }   // soái hạm: thêm cờ đỉnh cột chính
  }
  return { n, w, h, scale: sc, update(t) { U.uT.value = t; } };
}

// list: [{phe, at:[E,N] | pos: () => [E,N,hd], a, b (bán trục m), rot (rad, hướng trục a), y0 (cốt), on: () => bool}]
export function rims(list, ctx, { dNear = 800, dFar = 1200, width = 0.32, opacity = 0.8 } = {}) {   // V7B lượt 2: viền dày/đậm hơn (lượt 1 không thấy ở 2,8 km)
  const group = new THREE.Group(), items = [], ring = new THREE.RingGeometry(1 - width, 1, 48).rotateX(-Math.PI / 2), mats = {};
  for (const it of list) {
    const col = PHE[it.phe] || '#a89f8a'; mats[col] = mats[col] || new THREE.MeshBasicMaterial({ color: new THREE.Color(col), transparent: true, opacity, depthWrite: false, fog: false });
    const mat = mats[col].clone(); const o = new THREE.Mesh(ring, mat); o.renderOrder = 3; o.scale.set(it.a, 1, it.b); group.add(o); items.push({ it, o, mat });
  }
  return { group, n: items.length,
    update(camPos) { for (const { it, o, mat } of items) { const on = it.on ? it.on() : true; let e, n, hd = it.rot || 0; if (it.pos) { const p = it.pos(); if (!p) { o.visible = false; continue; } [e, n] = p; if (p[2] != null) hd = p[2]; } else [e, n] = it.at;
      const y = it.y0 != null ? it.y0 : Math.max(0.6, ctx.terr.hAt(e, n) + 0.6), d = Math.hypot(camPos.x - e, camPos.y - y, camPos.z + n), k = Math.max(0, Math.min(1, (d - dNear) / (dFar - dNear)));
      o.visible = on && k > 0.01; if (!o.visible) continue; mat.opacity = opacity * k; o.position.set(e, y, -n); o.rotation.y = hd; } } };
}

// Cine Lab · Cổng 6 (gói W4T) — THÂN Cas "cách A": áo len, quần, da ống chân dựng từ lưới thân MPFB2 (CC0; RIGHTS W4-MPFB-A4), render bằng three.js.
// Dùng: await preloadCasBodyBL() (một lần, TRƯỚC buildCharacter) rồi buildCharacter(cas, { casStyle: 'bl', casBody: 'bl' })
//       hoặc globalThis.CINE_CAS_BODY = 'bl'. Mặc định cast3d giữ thân cũ (CAS_BODY = 'v14').
// Lưới: blender/build_cas_body_bl.py → cas_body_bl.json (toạ độ hệ root cast3d ở TƯ THẾ BIND khai trong tệp, trọng số 16 khớp cast3d).
// GIỮ rig và tư thế: da CPU (LBS) riêng với bind ở tư thế BIND (vai dạng, khuỷu gập nhẹ — ít biến dạng nhất cho tư thế hay dùng).
import * as THREE from '../../../shared/node_modules/three/build/three.module.js';
import { CpuSkin } from '../sdf.js';

export const BODY_URL = new URL('./cas_body_bl.json', import.meta.url).href;
let CACHE = null;
export async function preloadCasBodyBL(url = BODY_URL) {
  if (CACHE && CACHE.url === url) return CACHE;
  CACHE = { url, j: await (await fetch(url)).json() };
  return CACHE;
}
export const casBodyBLReady = () => !!CACHE;
const dec = (b, T) => { const s = atob(b), u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return new T(u.buffer); };

// p = { root, joints, add(parent, geo, role, color, part, texRole) → mesh, colors: {sweater, trousers, skin} }
// Trả về { skin: CpuSkin, meshes, meta }. Gọi khi khung đang ở tư thế nghỉ (mọi khớp 0); hàm tự đặt tư thế BIND, ghi bind, rồi trả về nghỉ.
export function buildCasBodyBL(p) {
  if (!CACHE) throw new Error("casBody 'bl': cần await preloadCasBodyBL() trước buildCharacter");
  const J = CACHE.j, D2R = Math.PI / 180, { root, joints } = p;
  const saved = J.joints.map((n) => joints[n].quaternion.clone());
  for (const [n, e] of Object.entries(J.bind)) joints[n].rotation.set(e[0] * D2R, e[1] * D2R, e[2] * D2R, 'XYZ');
  root.updateMatrixWorld(true);
  const skin = new CpuSkin(root), bi = J.joints.map((n) => skin.bone(joints[n]));
  skin.captureBind();
  const meshes = [];
  for (const m of J.meshes) {
    const n = m.n, pos = dec(m.pos, Float32Array), nrm = dec(m.nrm, Float32Array), col = dec(m.col, Float32Array), uv = dec(m.uv, Float32Array);
    const idx = dec(m.idx, Uint32Array), wj = dec(m.wj, Uint8Array), ww = dec(m.ww, Float32Array);
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(Float32Array.from(pos), 3));
    g.setAttribute('normal', new THREE.BufferAttribute(Float32Array.from(nrm), 3));
    g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    g.setIndex(new THREE.BufferAttribute(idx, 1));
    const color = p.colors[m.role], tex = m.role === 'sweater' ? 'sweater' : undefined;
    const mesh = p.add(root, g, m.role, color, m.part, tex);
    const W = new Array(n);
    for (let v = 0; v < n; v++) { const e = []; for (let k = 0; k < 4; k++) { const w = ww[v * 4 + k]; if (w > 1e-4) e.push([bi[wj[v * 4 + k]], w]); } W[v] = e; }
    skin.add(mesh, W); meshes.push(mesh);
  }
  J.joints.forEach((n, i) => joints[n].quaternion.copy(saved[i]));
  root.updateMatrixWorld(true);
  return { skin, meshes, meta: J.meta || {} };
}

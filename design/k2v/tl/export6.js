// K2V tl · V6 bước 7 (phương án A, bản TỐT NHẤT) · XUẤT CẢNH của một khung sang Blender/Cycles: CÙNG hình học + CÙNG máy + CÙNG mặt trời/trời.
//  Gọi từ page.js (window.exportFrame / window.exportBuf / window.passesFrame) qua scripts/k2tl/export6.js (node). Không ảnh hưởng dựng thường.
//  · Hình học: mọi Mesh/InstancedMesh đang HIỆN (bỏ nước, trời, sprite, khói, vật trong suốt không ghi độ sâu), toạ độ THẾ GIỚI three (x = Đông, y = cao, z = −Bắc);
//    địa hình áp đúng phép hạ đất theo năm của shader (tYears → landK, đọc chính xác bằng GPU); InstancedMesh xuất lưới gốc + ma trận từng bản (người, cây).
//    Lọc tầm: bỏ vật có hình cầu bao xa hơn `far` m tới điểm nhìn (giữ đủ vật đổ bóng vào khung).
//  · Lượt ALBEDO (không chiếu sáng): mọi vật liệu xuất diffuseColor (uMask = 3 — cùng cơ chế mặt nạ) → màu vật liệu k2v (gồm vân thủ tục, cửa sổ, HC7) cho phép nhân
//    với ánh sáng Cycles; lượt KHÓI (RGBA HDR, nền trong suốt) và lượt CUỐI k2v (nước/trời) để ghép.
import { THREE } from './core.js';

const b64 = (ta) => { const u8 = new Uint8Array(ta.buffer, ta.byteOffset, ta.byteLength); let s = ''; const CH = 0x8000; for (let i = 0; i < u8.length; i += CH) s += String.fromCharCode.apply(null, u8.subarray(i, i + CH)); return btoa(s); };

export function makeExporter(G) {   // G = window.__tl(): { scene, cam, ctx, R, pipe, C, SC }
  const { THREE: T = THREE } = {}; let BUF = [];
  // đọc CHÍNH XÁC tYears (RGBA8, lọc nearest) bằng GPU → mảng byte
  function yearsBytes() {
    const tex = G.ctx.terr.uni.tYears.value, img = tex.image, w = img.width, h = img.height, rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.UnsignedByteType, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
    const m = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, uniforms: { t: { value: tex } }, vertexShader: 'in vec3 position; out vec2 v; void main(){ v = position.xy * 0.5 + 0.5; gl_Position = vec4(position.xy, 0.0, 1.0); }',
      fragmentShader: 'precision highp float; uniform sampler2D t; in vec2 v; out vec4 o; void main(){ o = texelFetch(t, ivec2(gl_FragCoord.xy), 0); }' });
    const sc = new THREE.Scene(); sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m)); const R = G.R; R.setRenderTarget(rt); R.render(sc, new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1));
    const px = new Uint8Array(w * h * 4); R.readRenderTargetPixels(rt, 0, 0, w, h, px); R.setRenderTarget(null); return { px, w, h, flipY: tex.flipY };
  }
  function landK(ly, y) { if (ly < 1) return 1; if (ly > 9000) return 0; if (Math.abs(ly - 1941) < 0.5) return Math.max(0, Math.min(1, (y - 1941) / 2)); return Math.max(0, Math.min(1, (y - (ly - 1.5)) / 1.5)); }
  function collect({ far = 6000, year = 1782.7 } = {}) {
    const { scene, cam, ctx } = G, out = [], cp = cam.position, look = new THREE.Vector3(); cam.getWorldDirection(look); const tgt = cp.clone().addScaledVector(look, 1200);
    const skip = new Set([ctx.ws.water, ctx.ws.sky]); let Y = null;
    const terrMat = ctx.terr.mat, ext = ctx.terr.uni.uExt.value;
    scene.updateMatrixWorld(true);
    const visible = (o) => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
    const kindOf = (o) => { let k = 'khac'; for (let p = o; p; p = p.parent) { if (p === ctx.terr.group) return 'dia_hinh'; if (ctx.city && p === ctx.city.group) return 'nha'; if (p.userData && p.userData.k6) return p.userData.k6; } const m = [].concat(o.material)[0];
      if (m && m.customProgramCacheKey && /ppl6/.test(m.customProgramCacheKey())) return 'nguoi'; if (m && m.customProgramCacheKey && /tl-fort/.test(m.customProgramCacheKey())) return 'cong_su'; if (m && m.userData && m.userData.v6n) return 'nha'; return k; };
    scene.traverse((o) => {
      if (!(o.isMesh) || skip.has(o) || !visible(o)) return; const m = [].concat(o.material)[0]; if (!m || m.isRawShaderMaterial || (m.transparent && !m.depthWrite) || m.isSpriteMaterial) return;
      const g = o.geometry; if (!g || !g.attributes.position) return; if (!g.boundingSphere) g.computeBoundingSphere();
      if (!o.isInstancedMesh) { const s = g.boundingSphere.clone().applyMatrix4(o.matrixWorld); if (s.center.distanceTo(tgt) - s.radius > far && s.center.distanceTo(cp) - s.radius > far) return; }
      const pos = g.attributes.position, n = pos.count, P = new Float32Array(n * 3), v = new THREE.Vector3();
      const isTerr = m === terrMat; if (isTerr && !Y) Y = yearsBytes();
      for (let i = 0; i < n; i++) { v.fromBufferAttribute(pos, i);
        if (isTerr) { const u = (v.x - ext.x) / ext.z, w = (-v.z - ext.y) / ext.w; const ix = Math.min(Y.w - 1, Math.max(0, Math.floor(u * Y.w))), iy0 = Math.min(Y.h - 1, Math.max(0, Math.floor(w * Y.h))), iy = Y.flipY ? iy0 : Y.h - 1 - iy0;
          const q = (iy * Y.w + ix) * 4, ly = Y.px[q + 2] * 256 + Y.px[q + 3], k = landK(ly, year); v.y = (1 - k) * Math.min(v.y, -10) + k * v.y; }
        if (!o.isInstancedMesh) v.applyMatrix4(o.matrixWorld); P[i * 3] = v.x; P[i * 3 + 1] = v.y; P[i * 3 + 2] = v.z; }
      let I = g.index ? new Uint32Array(g.index.array) : null; if (o.isInstancedMesh && o.count === 0) return;
      const rec = { name: o.name || o.type, kind: kindOf(o), nv: n, nt: (I ? I.length : n) / 3, buf: {} }; BUF.push(P); rec.buf.P = BUF.length - 1; if (I) { BUF.push(I); rec.buf.I = BUF.length - 1; }
      if (g.attributes.color && m.vertexColors) { const c = g.attributes.color, Cc = new Float32Array(n * 3); for (let i = 0; i < n; i++) { Cc[i * 3] = c.getX(i); Cc[i * 3 + 1] = c.getY(i); Cc[i * 3 + 2] = c.getZ(i); } BUF.push(Cc); rec.buf.C = BUF.length - 1; }
      if (o.isInstancedMesh) { const M = new Float32Array(o.count * 16), mm = new THREE.Matrix4(); for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, mm); mm.premultiply(o.matrixWorld); M.set(mm.elements, i * 16); } BUF.push(M); rec.buf.M = BUF.length - 1; rec.inst = o.count;
        if (o.instanceColor) { BUF.push(new Float32Array(o.instanceColor.array.slice(0, o.count * 3))); rec.buf.IC = BUF.length - 1; } }
      rec.side = m.side === THREE.DoubleSide ? 2 : 0; out.push(rec);
    });
    return out;
  }
  return {
    // khung f (trạng thái đã áp bằng renderFrame trước đó): danh sách vật + máy + ánh sáng; bộ đệm lấy riêng bằng buf(i)
    frame(opt = {}) { BUF = []; const { cam, ctx, C } = G; cam.updateMatrixWorld(); const objs = collect(opt);
      const L = C.look; return { objs, nbuf: BUF.length, bytes: BUF.reduce((a, b) => a + b.byteLength, 0),
        cam: { pos: cam.position.toArray(), quat: cam.quaternion.toArray(), fov: cam.fov, aspect: cam.aspect, near: cam.near, far: cam.far, W: C.W, H: C.H },
        sun: { dir: ctx.sunDir.toArray(), color: ctx.sun.color.toArray(), intensity: ctx.sun.intensity }, hemi: { sky: ctx.hemi.color.toArray(), ground: ctx.hemi.groundColor.toArray(), intensity: ctx.hemi.intensity },
        fog: ctx.scene.fog ? { color: ctx.scene.fog.color.toArray(), density: ctx.scene.fog.density } : null, look: L }; },
    buf(i) { const a = BUF[i]; return { type: a.constructor.name, n: a.length, b64: b64(a) }; },
  };
}

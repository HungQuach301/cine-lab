// Cine Lab · Cổng 5 LAYOUT — CUỐI PHỐ OSTLER (V3): GÓI W2 giữ file này. W1 dùng qua buildStreetSet (x0 < 0), không sửa.
// Bản khởi đầu (P) = đúng hình Cổng 4: tường vôi nhà kho chắn ngang ở x = −5 → "tường trống" (lỗi V3 ở 0:52, 1:04, 1:40).
// W2 thay bằng: phố cong / ngã rẽ, dãy nhà xa nhiều lớp, sương, chiều sâu — vẫn giữ nhà kho, hốc cửa, tường chim theo luật thế giới mục 1.
// Tham số: scene, o = { sky, x0, x1, matC, FT, winKind, emit, houses } (houses = hàm dựng dãy nhà của sets.js). Trả về thông tin tuỳ ý (endInfo).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { limewashTex } from '/cong3/dir-C/common.js';
const lamMat = (o) => new THREE.MeshLambertMaterial(o);
export function buildStreetEnd(scene, o) {
  const wh = new THREE.Mesh(new THREE.PlaneGeometry(24, 11), lamMat({ color: '#ffffff', map: limewashTex(11, { metres: 6, grime: true, brick: 0.05 }) }));
  wh.rotation.y = Math.PI / 2; wh.position.set(-5, 5.5, 0); wh.receiveShadow = true; scene.add(wh);
  return { warehouseWall: wh };
}

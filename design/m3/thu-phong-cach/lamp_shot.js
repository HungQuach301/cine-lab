// Cine Lab · M3 THỬ PHONG CÁCH — đoạn 20 s "người thắp đèn soi số liệu" (shot riêng 'lp20', chỉ nạp khi dbg.style có giá trị).
// Dùng lại tài sản Last Round: bộ phố đêm (buildStreetSet), Ida + đèn lồng cầm tay (holdOut), dáng đi walkPose, nguồn sáng lanternLight.
// Ida thấy TỪ SAU LƯNG (máy ở lòng phố phía nam, Ida quay mặt về mặt tiền phía bắc). Hai tấm giấy dán tường (bản đồ phố cổ + biểu đồ)
// chỉ hiện ra trong vũng sáng đèn lồng (vật liệu Lambert thường: ngoài vũng sáng thì tối như tường) — "ánh đèn làm hiện số liệu".
// Số liệu MINH HOẠ (ghi "Illustrative data" trên tấm biểu đồ); ảnh tấm sinh thủ tục bằng design/m3/thu-phong-cach/data_frame.py.
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { walkPose, WALK } from '/cong3/shared/anim.js';
import { buildStreetSet, LAMP_X } from '/cong5/layout/sets.js';
import { P, camMM, lanternLight } from '/cong5/layout/common.js';
import { makeChar, poseAt, valAt, ease, clamp01, over, camAt, fovOf } from '/cong5/layout/util.js';

const X0 = 60.0, ZI = -1.2, WALL_Z = -5.45;
export const LP = {
  walk: [55.6, X0], tWalk: 3.6, tTurn: [3.6, 4.6], lightI: 34,
  // khoá máy: [t, vị trí, điểm nhìn, fov] — trượt ngang chậm + đẩy vào nhẹ (parallax giữa Ida, cột đèn, mặt tiền)
  cam: [[0, [58.6, 1.55, 4.6], [59.4, 2.05, -5.4], fovOf(32)], [20, [61.0, 1.5, 3.7], [60.6, 2.15, -5.4], fovOf(32)]],
  panels: [{ file: 'panel_map.png', x: 58.1, y: 2.35, w: 3.0, h: 1.95 }, { file: 'panel_chart.png', x: 62.0, y: 2.35, w: 2.7, h: 1.95 }],
};

export const LAMP_SHOT = { id: 'lp20', scene: 0, t0: 0, t1: 20, size: 'MWS', angle: 'sau lưng, ngang vai', mm: 32, move: 'trượt ngang + đẩy nhẹ',
  why: 'Nhận diện kênh Lamplight: người thắp đèn (từ sau lưng) giơ đèn soi bóng tối; vũng sáng làm hiện bản đồ và biểu đồ.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 34, x1: 90, shadowLamps: [] });
    const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 });
    const place = (pose, x, z, yaw) => { ida.root.position.set(x, pose.root_y_m ?? 0, z); ida.root.rotation.y = yaw; ida.root.updateMatrixWorld(true); ida.place(pose, x, z, yaw); };
    const lamp = lanternLight(st.scene, true, LP.lightI);
    // tấm giấy dán tường (Lambert: chỉ sáng khi ánh đèn lồng chạm)
    const loader = new THREE.TextureLoader();
    for (const pn of LP.panels) {
      const tex = await loader.loadAsync('/m3/thu-phong-cach/data/' + pn.file); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(pn.w, pn.h), new THREE.MeshLambertMaterial({ map: tex }));
      m.position.set(pn.x, pn.y, WALL_Z); m.receiveShadow = true; m.userData.tpcData = 1; st.scene.add(m);
    }
    const cam = camMM(32);
    // tư thế: cầm đèn thấp khi đi → giơ đèn cao về tấm trái → lia sang tấm phải
    const low = over(p.holdOut, { joints: { neck: [6, 0, 0], shoulder_R: [-30, 0, -10], elbow_R: [-12, 0, 0] } });
    const up = (yaw, lift) => over(p.holdOut, { joints: { spine: [-2, yaw, 0], neck: [-14, yaw * 0.6, 0], shoulder_R: [-128 - lift, 0, -14], elbow_R: [-14, 0, 0], shoulder_L: [-10, 0, 10], elbow_L: [-20, 0, 0] } });
    const keys = [[4.4, low], [5.0, low], [7.2, up(-22, 0)], [11.2, up(-26, 6)], [13.9, up(24, 4)], [17.6, up(28, 8)], [20, up(26, 2)]];
    return { scene: st.scene, cam, named: { ida }, exposure: 1.6,
      update(t, T, f) {
        st.setState({ gas: (i) => (i === 6 ? 1 : 0), post: () => 0, square: 0, clock: 0, whiteFill: 0 }, f);
        camAt(cam, LP.cam, t);
        if (t < LP.tWalk) {
          const x = LP.walk[0] + (LP.walk[1] - LP.walk[0]) * Math.min(1, t / LP.tWalk) * 1.0;
          const w = walkPose(t, p.holdOut); w.joints.shoulder_R = [-30 + 4 * Math.sin(t * 6.3), 0, -10]; w.joints.elbow_R = [-12, 0, 0];
          place(w, x, ZI, Math.PI / 2);
        } else {
          const yaw = Math.PI / 2 + (Math.PI / 2) * ease(clamp01((t - LP.tTurn[0]) / (LP.tTurn[1] - LP.tTurn[0])));
          place(poseAt(keys, t), LP.walk[1], ZI, yaw);
        }
        lamp(ida, f, 1);
      } };
  } };

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

const X0 = 60.0, ZI = -2.9, WALL_Z = -5.45;
export const LP = {
  walk: [55.6, X0], tWalk: 3.6, tTurn: [3.6, 4.6], lightI: 2, spotI: 46,
  // điểm vũng sáng trên tường theo thời gian (x): theo người đi → tấm bản đồ → tấm biểu đồ
  aim: [[0, 56.2], [3.6, 59.6], [5.0, 59.6], [7.2, 57.7], [11.2, 57.4], [13.9, 61.8], [17.6, 62.1], [20, 62.0]],
  // khoá máy: [t, vị trí, điểm nhìn, fov] — trượt ngang chậm + đẩy vào nhẹ (parallax giữa Ida, cột đèn, mặt tiền)
  cam: [[0, [58.6, 1.35, 2.6], [59.4, 2.7, -5.4], fovOf(28)], [20, [60.9, 1.35, 1.8], [60.4, 2.75, -5.4], fovOf(28)]],
  panels: [{ file: 'panel_map.png', x: 57.5, y: 2.45, w: 3.6, h: 2.34 }, { file: 'panel_chart.png', x: 61.9, y: 2.45, w: 3.24, h: 2.34 }],
};

export const LAMP_SHOT = { id: 'lp20', scene: 0, t0: 0, t1: 20, size: 'MWS', angle: 'sau lưng, ngang vai', mm: 32, move: 'trượt ngang + đẩy nhẹ',
  why: 'Nhận diện kênh Lamplight: người thắp đèn (từ sau lưng) giơ đèn soi bóng tối; vũng sáng làm hiện bản đồ và biểu đồ.',
  async build(ctx) {
    const st = buildStreetSet({ sky: 'night', x0: 34, x1: 90, shadowLamps: [] });
    const p = P(ctx);
    const ida = makeChar(ctx, st.scene, 'ida', { detail: 22 });
    const place = (pose, x, z, yaw) => { ida.root.position.set(x, pose.root_y_m ?? 0, z); ida.root.rotation.y = yaw; ida.root.updateMatrixWorld(true); ida.place(pose, x, z, yaw); };
    const V2 = !!(ctx.dbg && ctx.dbg.style === 'b3v2');   // B3 v2: tấm chữ lớn, vũng sáng mềm từ đèn lồng, đèn lồng đung đưa, thở
    const lamp = lanternLight(st.scene, false, V2 ? 6 : LP.lightI);   // quầng gần (người, đá lát)
    // vũng sáng "soi": đèn rọi từ đèn lồng tới điểm trên tường (cách điệu: đèn lồng có chụp phản quang) — bóng đổ mạnh của cột đèn, người
    const spot = V2 ? new THREE.SpotLight("#ffb060", 0, 0, 0.56, 1.0, 2) : new THREE.SpotLight("#ffb060", 0, 0, 0.38, 0.5, 2); spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -0.0005; spot.shadow.camera.near = 0.1;
    st.scene.add(spot, spot.target); const lp = new THREE.Vector3();
    if (ida.props.lantern) ida.props.lantern.traverse((m) => { if (m.isMesh) m.castShadow = false; });   // nguồn sáng nằm trong đèn lồng: vỏ đèn không được che chính nó

    // tấm giấy dán tường (Lambert: chỉ sáng khi ánh đèn lồng chạm)
    const loader = new THREE.TextureLoader();
    for (const pn of LP.panels) {
      const tex = await loader.loadAsync('/m3/thu-phong-cach/data/' + (V2 ? pn.file.replace('.png', '_v2.png') : pn.file)); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(pn.w, pn.h), new THREE.MeshLambertMaterial({ map: tex, alphaTest: 0.5 }));
      m.position.set(pn.x, pn.y, WALL_Z); m.receiveShadow = true; m.userData.tpcData = 1; st.scene.add(m);
    }
    const cam = camMM(32);
    // tư thế: cầm đèn thấp khi đi → giơ đèn cao về tấm trái → lia sang tấm phải
    const low = over(p.holdOut, { joints: { neck: [6, 0, 0], shoulder_R: [-30, 0, -10], elbow_R: [-12, 0, 0] } });
    const up = (yaw, lift) => over(p.holdOut, { joints: { spine: [-2, yaw, 0], neck: [-14, yaw * 0.6, 0], shoulder_R: [-128 - lift, 0, -14], elbow_R: [-14, 0, 0], shoulder_L: [-10, 0, 10], elbow_L: [-20, 0, 0] } });
    const keys = [[4.4, low], [5.0, low], [7.2, up(-22, 0)], [11.2, up(-26, 6)], [13.9, up(24, 4)], [17.6, up(28, 8)], [20, up(26, 2)]];
    return { scene: st.scene, cam, named: { ida }, exposure: 1.1,
      update(t, T, f) {
        st.setState({ gas: (i) => (i === 6 ? 1 : 0), post: () => 0, square: 0, clock: 0, whiteFill: 0 }, f);
        camAt(cam, LP.cam, t);
        if (t < LP.tWalk) {
          const x = LP.walk[0] + (LP.walk[1] - LP.walk[0]) * Math.min(1, t / LP.tWalk) * 1.0;
          const w = walkPose(t, p.holdOut); w.joints.shoulder_R = [-30 + 4 * Math.sin(t * 6.3), 0, -10]; w.joints.elbow_R = [-12, 0, 0];
          place(w, x, ZI, Math.PI / 2);
        } else {
          const yaw = Math.PI / 2 + (Math.PI / 2) * ease(clamp01((t - LP.tTurn[0]) / (LP.tTurn[1] - LP.tTurn[0])));
          let pz = poseAt(keys, t);
          if (V2) { const b = Math.sin(2 * Math.PI * t / 3.4), sp = pz.joints.spine || [0, 0, 0], sr = pz.joints.shoulder_R || [0, 0, 0];   // thở + tay giữ đèn hơi chao
            pz = over(pz, { joints: { spine: [sp[0] + 1.4 * b, sp[1], sp[2]], shoulder_R: [sr[0] + 1.5 * Math.sin(2 * Math.PI * t / 2.3), sr[1], sr[2]] } }); }
          place(pz, LP.walk[1], ZI, yaw);
        }
        if (V2 && ida.props.lantern) { const L = ida.props.lantern; if (L.userData.rz0 === undefined) { L.userData.rz0 = L.rotation.z; L.userData.rx0 = L.rotation.x; }
          const a = t < LP.tWalk ? 1 : 0.45; L.rotation.z = L.userData.rz0 + 0.10 * a * Math.sin(2 * Math.PI * 0.85 * t); L.rotation.x = L.userData.rx0 + 0.05 * a * Math.sin(2 * Math.PI * 0.85 * t + 1.1); }   // đèn lồng đung đưa
        lamp(ida, f, 1);
        const lan = ida.props.lantern; lan.updateMatrixWorld(true); (lan.userData.lightAnchor || lan).getWorldPosition(lp);
        spot.position.copy(lp); spot.target.position.set(valAt(LP.aim, t), lp.y + 0.35, WALL_Z); spot.target.updateMatrixWorld(true);
        spot.intensity = LP.spotI * ease(clamp01((t - 0.3) / 1.2)) * (1 + 0.03 * Math.sin(f * 0.37));
      } };
  } };

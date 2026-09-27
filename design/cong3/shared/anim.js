// Cine Lab · Cổng 3 v2 — chu kỳ đi của Ida vác thang (dùng chung cho mọi cách làm nhân vật).
// walkPose(t, base) → pose (cùng định dạng model sheet) tại thời điểm t (giây). base = poses.walk_ladder (tay phải giữ thang).
// Nhịp người 74 tuổi, thẳng lưng: 1,6 bước/giây (chu kỳ 2 bước = 1,25 s), sải 0,56 m → 0,90 m/s.
// Mọi kênh là tổ hợp sin/cos (có lấy đà, theo đà) — không đoạn nào tuyến tính theo thời gian (luật H1).
export const WALK = { cycle_s: 1.25, stride_m: 0.56, speed_mps: 0.896 };

export function walkPose(t, base) {
  const p = (t / WALK.cycle_s) % 1, w = 2 * Math.PI * p;
  const s = Math.sin(w), c = Math.cos(w);
  const knee = (ph) => 4 + 48 * Math.pow(Math.max(0, Math.sin(w + ph)), 1.6);        // gối gập mạnh lúc đưa chân
  const joints = JSON.parse(JSON.stringify(base.joints));
  Object.assign(joints, {
    hip_L: [-24 * s - 2, 0, 0], hip_R: [24 * s - 2, 0, 0],
    knee_L: [knee(-0.5), 0, 0], knee_R: [knee(Math.PI - 0.5), 0, 0],
    ankle_L: [10 * Math.sin(w + 1.2), 0, 0], ankle_R: [-10 * Math.sin(w + 1.2), 0, 0],
    spine: [(base.joints.spine?.[0] ?? 6) + 1.5 * Math.cos(2 * w), 3 * s, 0],       // xoay hông–vai ngược nhịp chân
    neck: [(base.joints.neck?.[0] ?? 10) - 1.2 * Math.cos(2 * w), -2 * s, 0],
    shoulder_L: [20 * s + 6, 0, 8], elbow_L: [-16 - 8 * Math.max(0, s), 0, 0],       // tay trái vung ngược chân trái
  });
  const bob = -0.018 * Math.cos(2 * w) - 0.006;                                      // nảy 2 lần mỗi chu kỳ, thấp nhất lúc hai chân dạng
  return { ...base, joints, root_y_m: bob, _phase: p };
}

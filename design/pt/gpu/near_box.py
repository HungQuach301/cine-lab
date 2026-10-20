"""NC-GPU · hộp albedo 0,5 m quanh điểm máy: tâm = giao tia giữa khung với mặt z = 0 (giới hạn 1,5 km phía trước), cạnh 2·R (m), làm tròn 10 m. In 'E0,N0,E1,N1'."""
import sys, json, math
M = json.load(open(sys.argv[1])); R = float(sys.argv[2]) if len(sys.argv) > 2 else 900; c = M['cam']; x, y, z, w = c['quat']; p = c['pos']
# hướng nhìn three = quat · (0, 0, −1)
dx, dy, dz = -(2 * (x * z + w * y)), -(2 * (y * z - w * x)), -(1 - 2 * (x * x + y * y))
t = min(1500.0, p[1] / max(1e-3, -dy)) if dy < 0 else 1500.0
e, n = p[0] + dx * t * 0.6, -(p[2] + dz * t * 0.6)   # tâm lệch về phía máy (60 % đường tới điểm nhìn)
r = lambda v: int(round(v / 10) * 10)
print(f'{r(e - R)},{r(n - R)},{r(e + R)},{r(n + R)}')

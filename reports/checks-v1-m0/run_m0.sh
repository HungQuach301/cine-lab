#!/usr/bin/env bash
# Phiên K — chạy bộ luật v1 trên media M0 (lấy từ origin/main) + các phép minh hoạ trên hình render thật.
# Dùng: bash reports/checks-v1-m0/run_m0.sh   (từ gốc repo, trên nhánh checks/v1)
set -u
ROOT=$(git rev-parse --show-toplevel); cd "$ROOT"
PY=/opt/cine/bin/python
OUT=reports/checks-v1-m0
W=$(mktemp -d)
git fetch -q origin main
for f in b-3d-mb8 a-2d-mb8 SO-SANH-PHONG-CACH; do git show origin/main:reports/m0/media/$f.mp4 > $W/$f.mp4; done
git archive origin/main shots/m0-consistency reports/m0/consistency | tar -x -C $W

# 1) Hai file M0 được giao, profile shot, không file đi kèm (M0 không xuất sidecar).
for f in b-3d-mb8 a-2d-mb8; do $PY checks/run.py $W/$f.mp4 --out $OUT/$f; echo "exit $f: $?"; done

# 2) Minh hoạ P0: video so sánh phong cách M0 có nhãn chữ burn-in, không có matte.
$PY checks/run.py $W/SO-SANH-PHONG-CACH.mp4 --only P0 --out $OUT/minh-hoa/SO-SANH-P0; echo "exit P0: $?"

# 3) Minh hoạ H1/H1b: dữ liệu chuyển động do phiên K DỰNG LẠI từ mã cảnh M0 (không phải render xuất).
$PY $OUT/recon_motion_a2d.py $W/a-2d-mb8.motion.json
$PY checks/run.py $W/a-2d-mb8.mp4 --only H1,H1b --out $OUT/minh-hoa/a-2d-H1b-dung; echo "exit H1b đúng: $?"
$PY $OUT/recon_motion_a2d.py $W/fake.motion.json fake
$PY checks/run.py $W/a-2d-mb8.mp4 --only H1,H1b --motion $W/fake.motion.json --out $OUT/minh-hoa/a-2d-H1b-khai-gia; echo "exit H1b giả: $?"

# 4) Minh hoạ C3: mặt nạ bộ phận và khung render thật của 2 shot nhất quán M0 (1 khung mỗi shot).
for s in A B; do
  d=$W/shots/m0-consistency/shot-$s
  ffmpeg -v error -y -loop 1 -i $d/frame.png -frames:v 1 -r 24 -c:v libx264 -crf 8 -pix_fmt yuv420p \
    -vf scale=out_color_matrix=bt709:out_range=tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
    -color_range tv $W/shot$s.mp4
  mkdir -p $W/shot$s.parts
  printf '{"model_sheet": "reports/m0/consistency/model-sheet.json", "scale": 1, "frames": {"0": {%s}}}' \
    "$(for p in head torso upper_arm forearm thigh shin; do printf '"%s": "../shots/m0-consistency/shot-%s/masks/%s.png",' $p $s $p; done | sed 's/,$//')" \
    > $W/shot$s.parts/parts.json
  $PY checks/run.py $W/shot$s.mp4 --only C3 --repo $W --out $OUT/minh-hoa/C3-shot-$s; echo "exit C3 $s: $?"
done
echo "Thư mục tạm: $W"

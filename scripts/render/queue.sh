#!/bin/bash
# Hàng đợi render nặng Cổng 5 (phiên P giữ). Mỗi lúc CHỈ MỘT render nặng chạy trên máy 4 vCPU.
# Dùng:  bash scripts/render/queue.sh <gói: W1|W2|W3|P> <nhãn ngắn> -- <lệnh...>
# Chạy nền:  nohup bash scripts/render/queue.sh W1 s02-s08 -- node design/cong5/layout/render_film.js --out ... > log 2>&1 & PID=$!
#            while kill -0 $PID 2>/dev/null; do sleep 20; done      (bài học vòng chờ: chờ theo PID, không pgrep -f)
# "Nặng" = render chuỗi khung (≥ 1 shot đầy đủ), still ≥ 1920×1080 hoặc ≥ 2 mẫu, mặt nạ C3 4×, đóng gói 2 pass, luật máy.
# Nhẹ (không cần hàng đợi): --probe ≤ 3 khung/shot ở 960×540, --list/--events, ghép âm.
# Nhật ký thời gian thật (TSV, chung cho mọi worktree): /var/tmp/cine-queue/log.tsv
#   cột: gói  nhãn  xếp_hàng(ISO)  bắt_đầu  kết_thúc  chờ_s  chạy_s  mã_thoát  thư_mục  lệnh
set -u
Q=/var/tmp/cine-queue; mkdir -p "$Q"; touch "$Q/log.tsv"
PKG=${1:?gói}; LABEL=${2:?nhãn}; shift 2; [ "${1:-}" = "--" ] && shift
[ $# -gt 0 ] || { echo "thiếu lệnh" >&2; exit 2; }
enq=$(date +%s.%N); enq_iso=$(date -Is)
echo "[queue] $PKG/$LABEL xếp hàng lúc $enq_iso" >&2
exec 9>"$Q/heavy.lock"
flock 9
st=$(date +%s.%N); st_iso=$(date -Is)
echo "$PKG $LABEL $$ $st_iso" > "$Q/running"
echo "[queue] $PKG/$LABEL bắt đầu $st_iso (chờ $(printf %.0f "$(echo "$st - $enq" | bc)") s)" >&2
"$@"; rc=$?
en=$(date +%s.%N); en_iso=$(date -Is); rm -f "$Q/running"
printf '%s\t%s\t%s\t%s\t%s\t%.1f\t%.1f\t%s\t%s\t%s\n' "$PKG" "$LABEL" "$enq_iso" "$st_iso" "$en_iso" "$(echo "$st - $enq" | bc)" "$(echo "$en - $st" | bc)" "$rc" "$PWD" "$*" >> "$Q/log.tsv"
echo "[queue] $PKG/$LABEL xong $en_iso, chạy $(printf %.0f "$(echo "$en - $st" | bc)") s, mã $rc" >&2
exit $rc

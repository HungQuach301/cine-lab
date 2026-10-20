#!/usr/bin/env bash
# NC-V2V3 · CHẠY TRÊN POD: chạy lần lượt các job (thứ tự ưu tiên) → /w/ra/<nhãn>/, log mỗi job vào /w/jobs/<nhãn>.log, dòng tổng /w/jobs/xong.jsonl
cd /w && . venv/bin/activate
for j in "$@"; do
  l=$(basename $j .json); python3 v2v3/wf_vace.py $j > /w/jobs/$l.log 2>&1; m=$?
  echo "{\"job\": \"$l\", \"ma\": $m, \"so_khung\": $(ls /w/ra/$l 2>/dev/null | wc -l), \"ket\": $(tail -n 1 /w/jobs/$l.log | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read().strip()))')}" >> /w/jobs/xong.jsonl
done
echo BATCH-XONG >> /w/jobs/xong.jsonl

#!/bin/bash
# Last Lamplighters · nhà máy — MỘT LỆNH kiểm một tập: bash scripts/ll/qc.sh <episode.yaml>   (V=v1 mặc định)
# Xuất bảng ĐẠT/TRƯỢT ra màn hình và <out>/qc.md, <out>/qc.json. Mã thoát 0 = mọi mục ĐẠT.
# Luật làm việc của P; luật khoá do K giữ trong checks/ (không sửa ở đây). Chi tiết mục kiểm: đầu tệp qc.py.
exec /opt/cine/bin/python "$(dirname "$0")/qc.py" "$@"

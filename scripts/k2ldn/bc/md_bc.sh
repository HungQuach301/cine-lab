#!/bin/bash
# BAN-CUOI-T4-A · M-d lượt nháp CUỐI 360p (việc 4) — theo md_v3.sh (ANIMATIC-T4-V2) nhưng ẢNH ĐẦU DỰNG TỪ RENDER 3D CÙNG NĂM (look3 cờ d, $BC_R/md-<mã>/00000.png + LUT kênh)
# + OpenAI edits (oai_bc.py; nhân vật có tên → thêm chân dung tham chiếu) — không tạo từ chữ thuần. ≤ 2 lượt mỗi clip (lệnh: C1 (b)); mức ĐỦ cho mọi clip của vòng này.
# Mỗi lượt: ảnh đầu → Flash ảnh (câu hỏi mốc) → Omni 360p → Flash clip → tầng 2 (kiem_minh_hoa gpt + q_thoi_dai) → q_thoi_dai lớp CÔNG TRÌNH MỐC 3 khung.
# Bản ≤ 5 MB vào git ngay (channel-k2/k2c-t4-02/ban-cuoi/omni/{dau,clip,kiem,kiem2,chon}).   bash scripts/k2ldn/bc/md_bc.sh <mã …>
set -o pipefail
cd "$(dirname "$0")/../../.."
export N2P_DIR=$PWD/reports/ban-cuoi-t4-a GEM_DIR=reports/ban-cuoi-t4-a GEM_TRUOC_THEM=reports/animatic-t4/so-ai-gemini.jsonl,reports/animatic-t4-v2/so-ai-gemini.jsonl GEM_NGAN_SACH=55 GEM_MOC=50
PY=/opt/cine/bin/python; G=channel-k2/k2c-t4-02/ban-cuoi/omni; L=$G/lenh; SG=reports/ban-cuoi-t4-a/md-so-giay.jsonl; R=${BC_R:-/var/tmp/bc/r}
LUT=channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube; mkdir -p $G/dau $G/clip $G/kiem $G/kiem2 $G/chon $G/vao
gk() { for t in 1 2 3; do $PY scripts/k2ldn/anim/gem_kiem.py "$@" && return 0; sleep 20; done; return 1; }
j() { $PY -c "import json;d=json.load(open('$L/muc-luc.json'))['$1'];v=d.get('$2','');print(' '.join(v) if isinstance(v,list) else v)"; }
for ma in "$@"; do
  [ -s $G/chon/$ma.txt ] && { echo "ĐÃ CHỌN $ma"; continue; }
  O=/var/tmp/bc/omni/$ma; mkdir -p $O
  nam=$(j $ma nam); canh=$(j $ma canh); moc=$(j $ma cong_trinh_moc); refs=$(j $ma tham_chieu); loi=$(j $ma loi)
  RA=(); for r in $refs; do RA+=(--ref $r); done
  [ -s $G/vao/$ma-render.jpg ] || { ffmpeg -nostdin -loglevel error -y -i $R/md-$ma/00000.png -vf "lut3d=file='$LUT':interp=tetrahedral" $O/render.png && \
      $PY -c "from PIL import Image; Image.open('$O/render.png').convert('RGB').save('$G/vao/$ma-render.jpg', quality=90)"; } || { echo "THIẾU RENDER $ma"; continue; }
  [ -s $O/render.png ] || ffmpeg -nostdin -loglevel error -y -i $R/md-$ma/00000.png -vf "lut3d=file='$LUT':interp=tetrahedral" $O/render.png
  for l in $(seq ${START:-1} ${MAXL:-2}); do
    dau=$G/dau/$ma-l$l-dau.jpg
    if [ ! -s $dau ]; then
      $PY scripts/k2ldn/bc/oai_bc.py --img $O/render.png --prompt-file $L/$ma-anh.txt --tag $ma-a$l --out $O "${RA[@]}" || { echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"LOI-anh\"}" >> $SG; continue; }
      $PY -c "from PIL import Image; Image.open('$O/$ma-a$l.jpg').convert('RGB').resize((1280,720), Image.LANCZOS).save('$O/$ma-a$l-720.jpg', quality=92)"
      gk --anh $O/$ma-a$l-720.jpg --nam $nam --canh "$canh" --loi "$loi" --tag $ma-a$l --out $G/kiem --moc "$moc" || exit 1
      if ! grep -q '"ket_luan": "ĐẠT-T1"' $G/kiem/$ma-a$l-t1.json; then cp $O/$ma-a$l-720.jpg $G/dau/$ma-a$l-LOAI.jpg; echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"anh-dau-LOAI\"}" >> $SG; echo "ẢNH ĐẦU LOẠI $ma-a$l"; continue; fi
      cp $O/$ma-a$l-720.jpg $dau
    fi
    [ -s $O/$ma-l$l-360p.mp4 ] || $PY scripts/k2ldn/anim/omni.py --dau $dau --prompt-file $L/$ma-vid.txt --out $O/$ma-l$l-360p.mp4 --tag $ma-l$l-360p --res 360p || { echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"LOI-omni\"}" >> $SG; [ -f reports/ban-cuoi-t4-a/DUNG-GEMINI ] && exit 9; continue; }
    ffmpeg -nostdin -loglevel error -y -i $O/$ma-l$l-360p.mp4 -c:v libx264 -crf 26 -preset slow -an -movflags +faststart $G/clip/$ma-l$l-360p.mp4
    gk --anh $dau --clip $O/$ma-l$l-360p.mp4 --nam $nam --canh "$canh" --loi "$loi" --tag $ma-l$l-360p --out $G/kiem --moc "$moc" || exit 1
    t1=$(grep -o '"ket_luan": "[^"]*"' $G/kiem/$ma-l$l-360p-t1.json | cut -d'"' -f4)
    if [ "$t1" != "ĐẠT-T1" ]; then echo "{\"ma\":\"$ma\",\"luot\":$l,\"t1\":\"$t1\"}" >> $SG; continue; fi
    $PY -I scripts/k2ldn/ai/kiem_minh_hoa.py --dau $dau --clip $O/$ma-l$l-360p.mp4 --nam $nam --canh "$canh" --noi London --tag $ma-l$l-360p --out /var/tmp/bc/kiem2 --mo-hinh gpt --qtd 1 > $O/t2-$l.txt 2>&1
    cp /var/tmp/bc/kiem2/$ma-l$l-360p-kiem.json $G/kiem2/ 2>/dev/null
    t2=$(tail -1 $O/t2-$l.txt | awk '{print $2}')
    tm=ĐẠT
    for u in 25 55 90; do p=$O/k$u.png
      $PY -c "import cv2;c=cv2.VideoCapture('$O/$ma-l$l-360p.mp4');n=int(c.get(7));c.set(1,int($u/100*(n-1)));ok,im=c.read();cv2.imwrite('$p',im)"
      r=$($PY checks/ll/q_thoi_dai.py --anh $p --nam $nam --noi London --out /var/tmp/bc/qmoc --api --lop-moc --moc "$moc" --json $G/kiem2/qtd-moc-$ma-l$l-k$u.json 2>&1 | tail -1)
      echo "{\"tag\":\"$ma-l$l\",\"khung\":$u,\"nam\":$nam,\"kq\":$($PY -c "import json,sys;print(json.dumps(sys.argv[1]))" "$r")}" >> reports/ban-cuoi-t4-a/qtd-moc.jsonl
      echo "$r" | grep -q "O2 ĐẠT" || tm="TRƯỢT"; done
    echo "{\"ma\":\"$ma\",\"luot\":$l,\"t1\":\"$t1\",\"t2\":\"$t2\",\"moc\":\"$tm\"}" >> $SG
    [ "$t2" = "ĐẠT" ] && [ "$tm" = "ĐẠT" ] && { echo "$ma-l$l-360p" > $G/chon/$ma.txt; echo "CHỌN $ma-l$l-360p"; break; }
    echo "TRƯỢT lượt $l $ma (t2 $t2, mốc $tm)"
  done
  [ -s $G/chon/$ma.txt ] || echo "TRƯỢT HẾT LƯỢT $ma"
done
echo MD-BC-XONG

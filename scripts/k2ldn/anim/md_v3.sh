#!/bin/bash
# ANIMATIC-T4-V2 · M-d v3 cho danh sách shot — kiểm 2 MỨC (lệnh 25/10/2026, gói tiết kiệm):
#   day_du (công trình có tên / nhân vật có tên / chân trời City / dữ kiện): Flash (có câu hỏi mốc bắt buộc) → gpt-6.1-sol 3 khung + q_thoi_dai; ≤ 3 lượt
#   nen (người/phố làm nền): Flash + tờ khung soi bằng mắt (P ghi vào kiem-mat.json); ≤ 2 lượt
# Mỗi lượt: ảnh đầu (OpenAI; có tham chiếu chân dung → edits) → Flash ảnh → Omni 360p → Flash clip → [tầng 2]. Không dự trữ lượt. Bản ≤ 5 MB vào git ngay.
#   bash scripts/k2ldn/anim/md_v3.sh <ma …>
set -o pipefail
cd "$(dirname "$0")/../../.."
export N2P_DIR=$PWD/reports/animatic-t4-v2 GEM_DIR=reports/animatic-t4-v2 GEM_TRUOC_THEM=reports/animatic-t4/so-ai-gemini.jsonl GEM_NGAN_SACH=55 GEM_MOC=50 OAI_CHAN=10 CLAUDE_CHAN=10
PY=/opt/cine/bin/python; G=channel-k2/k2c-t4-02/animatic2/omni; L=$G/lenh; SG=reports/animatic-t4-v2/md-so-giay.jsonl; mkdir -p $G/dau $G/clip $G/kiem $G/kiem2 $G/chon
gk() { for t in 1 2 3; do $PY scripts/k2ldn/anim/gem_kiem.py "$@" && return 0; sleep 20; done; return 1; }   # Flash: thử lại khi 5xx/mạng (≤ 3)
j() { $PY -c "import json,sys;d=json.load(open('$L/muc-luc.json'))['$1'];v=d['$2'];print(' '.join(v) if isinstance(v,list) else v)"; }
for ma in "$@"; do
  [ -s $G/chon/$ma.txt ] && { echo "ĐÃ CHỌN $ma"; continue; }
  O=/var/tmp/anim/omni3/$ma; mkdir -p $O
  nam=$(j $ma nam); canh=$(j $ma canh); muc=$(j $ma muc_kiem); moc=$(j $ma cong_trinh_moc); refs=$(j $ma tham_chieu)
  dur=$($PY -c "import json,math;B=json.load(open('channel-k2/k2c-t4-02/BANG-SHOT-v3.json'));r=[x for x in B['shot'] if x['ma']=='$ma'][0];print(r['dur'])")
  loi=$($PY -c "import json;B=json.load(open('channel-k2/k2c-t4-02/BANG-SHOT-v3.json'));rs=B['shot'];i=[k for k,x in enumerate(rs) if x['ma']=='$ma'][0]
g=rs[i]['nhom_loi'];print(' '.join(c for x in rs if x['nhom_loi']==g for c in x['cau_loi'])[:600])")
  MOCARG=(); [ "$muc" = day_du ] && MOCARG=(--moc "$moc")
  RA=(); for r in $refs; do RA+=(--ref $r); done
  maxl=3; [ "$muc" = nen ] && maxl=2
  for l in $(seq ${START:-1} $maxl); do
    dau=$G/dau/$ma-dau.jpg
    if [ ! -s $dau ]; then
      $PY scripts/k2ldn/anim/oai_anh_v3.py --prompt-file $L/$ma-anh.txt --tag $ma-a$l --out $O "${RA[@]}" || { echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"LOI-anh\"}" >> $SG; continue; }
      $PY -c "from PIL import Image; Image.open('$O/$ma-a$l.jpg').convert('RGB').resize((1280,720), Image.LANCZOS).save('$O/$ma-a$l-720.jpg', quality=92)"
      gk --anh $O/$ma-a$l-720.jpg --nam $nam --canh "$canh" --loi "$loi" --tag $ma-a$l --out $G/kiem "${MOCARG[@]}" || exit 1
      if ! grep -q '"ket_luan": "ĐẠT-T1"' $G/kiem/$ma-a$l-t1.json; then cp $O/$ma-a$l-720.jpg $G/dau/$ma-a$l-LOAI.jpg; echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"anh-dau-LOAI\"}" >> $SG; echo "ẢNH ĐẦU LOẠI $ma-a$l"; continue; fi
      cp $O/$ma-a$l-720.jpg $dau
    fi
    [ -s $O/$ma-l$l-360p.mp4 ] || $PY scripts/k2ldn/anim/omni.py --dau $dau --prompt-file $L/$ma-vid.txt --out $O/$ma-l$l-360p.mp4 --tag $ma-l$l-360p --res 360p || { echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"LOI-omni\"}" >> $SG; grep -q "DỪNG\|CHẶN" $O/*.resp.json 2>/dev/null; [ -f reports/animatic-t4-v2/DUNG-GEMINI ] && exit 9; continue; }
    ffmpeg -nostdin -loglevel error -y -i $O/$ma-l$l-360p.mp4 -c:v libx264 -crf 26 -preset slow -an -movflags +faststart $G/clip/$ma-l$l-360p.mp4
    gk --anh $dau --clip $O/$ma-l$l-360p.mp4 --nam $nam --canh "$canh" --loi "$loi" --tag $ma-l$l-360p --out $G/kiem "${MOCARG[@]}" || exit 1
    t1=$(grep -o '"ket_luan": "[^"]*"' $G/kiem/$ma-l$l-360p-t1.json | cut -d'"' -f4)
    if [ "$t1" != "ĐẠT-T1" ]; then echo "{\"ma\":\"$ma\",\"luot\":$l,\"muc\":\"$muc\",\"t1\":\"$t1\",\"giay_yeu_cau\":$dur}" >> $SG; continue; fi
    if [ "$muc" = day_du ]; then
      $PY -I scripts/k2ldn/ai/kiem_minh_hoa.py --dau $dau --clip $O/$ma-l$l-360p.mp4 --nam $nam --canh "$canh" --noi London --tag $ma-l$l-360p --out /var/tmp/anim/kiem2 --mo-hinh gpt --qtd 1 > $O/t2-$l.txt 2>&1
      cp /var/tmp/anim/kiem2/$ma-l$l-360p-kiem.json $G/kiem2/ 2>/dev/null
      t2=$(tail -1 $O/t2-$l.txt | awk '{print $2}')
      echo "{\"ma\":\"$ma\",\"luot\":$l,\"muc\":\"$muc\",\"t1\":\"$t1\",\"t2\":\"$t2\",\"giay_yeu_cau\":$dur}" >> $SG
      [ "$t2" = "ĐẠT" ] && { echo "$ma-l$l-360p" > $G/chon/$ma.txt; echo "CHỌN $ma-l$l-360p"; break; }
    else
      echo "{\"ma\":\"$ma\",\"luot\":$l,\"muc\":\"$muc\",\"t1\":\"$t1\",\"t2\":\"tờ khung (mắt P)\",\"giay_yeu_cau\":$dur}" >> $SG
      echo "$ma-l$l-360p" > $G/chon/$ma.txt; echo "CHỌN-T1 $ma-l$l-360p (chờ P soi tờ khung)"; break
    fi
  done
  [ -s $G/chon/$ma.txt ] || echo "TRƯỢT $maxl LƯỢT $ma"
done
echo MD-V3-XONG

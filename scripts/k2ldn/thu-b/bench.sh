# THU-B-T4 · đo tốc độ KHÔNG tải chồng (P = 1): khung 1080p spp 24 và timelapse 640×360 spp 4 (12 khung đầu) cho V2 · D · D + vân nướng, M1-rong-hep (1666) và M4-rong-hep (2026)
cd /home/user/cine-lab; export LDN_DATA=/var/tmp/ldn; B=/var/tmp/ldn/thub/bench; mkdir -p $B
for f in M1-rong-hep M4-rong-hep; do for v in v2 d d2; do
  if [ $v = v2 ]; then P=look2; L=look2/; X=""; else P=thu-b/look3; L=look3d/; X="--fac /var/tmp/ldn/thub/fac/fac.json"; fi
  node scripts/k2ldn/thu-b/render_thub.js --shot /var/tmp/ldn/thub/may/$f-$v.json --out $B/$f-$v-1080 --page $P --lk $L $X > $B/$f-$v-1080.log 2>&1
  node scripts/k2ldn/thu-b/render_thub.js --shot /var/tmp/ldn/thub/may/tl-$f-$v.json --out $B/$f-$v-360 --page $P --lk $L $X --to 12 > $B/$f-$v-360.log 2>&1 || true
done; done
echo BENCH-XONG

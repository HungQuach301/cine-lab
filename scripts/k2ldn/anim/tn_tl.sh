#!/bin/bash
# ANIMATIC-T4 · (v) + khung ghép tấm nền cho đúng khoảng của shot: tl/<khung> ← khung 3D thô của shot [p0, p1) → tn.py tl → chép ra /var/tmp/anim/tn/ra/<shot>/
#   bash tn_tl.sh <shot> <khung> <tag> <khung đầu> <số khung>
set -o pipefail
cd "$(dirname "$0")/../../.."
ma=$1; k=$2; tag=$3; a=$4; n=$5; V=/var/tmp/anim/tn; export N2P_DIR=$PWD/reports/animatic-t4 V2_DIR=$V OAI_CHAN=10 CLAUDE_CHAN=15
rm -rf $V/tl/$k; mkdir -p $V/tl/$k
for i in $(seq 0 $((n-1))); do ln -s /var/tmp/anim/r/$ma/$(printf %05d $((a+i))).jpg $V/tl/$k/$(printf %05d $i).jpg; done
/opt/cine/bin/python scripts/k2ldn/anim/tn.py tl $k $tag | tail -1
rm -rf $V/ra/$ma; mkdir -p $V/ra/$ma; cp -r $V/tn/$k/$tag/tl $V/ra/$ma/tl; cp $V/tn/$k/$tag/$tag-v.json $V/ra/$ma/v.json
mkdir -p channel-k2/k2c-t4-02/animatic/tam-nen/chon; echo $V/ra/$ma > channel-k2/k2c-t4-02/animatic/tam-nen/chon/$ma.txt

#!/usr/bin/env bash
# allA.sh <outdir> <W> <H> [nc-json]
S=/tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad
for g in vay-ham cang pho-day hero toan-canh bo-chien-su; do $S/rA.sh $g $1/$g $2 $3 "${4:-{\}}" | grep "tl llvm"; done

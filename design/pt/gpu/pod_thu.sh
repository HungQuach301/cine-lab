#!/usr/bin/env bash
# NC-GPU · lượt THỬ chỉnh (ghi lại để chạy lại): ánh trời khuếch tán SKYDIF 1,0 (như NC-CPU) ↔ 0,277 (khớp three.js), lửa/khói ban ngày, chi phí thể tích
cd /w; until [ -f /w/san.txt ]; do sleep 2; done
for SD in ${SDS:-1.0 0.277}; do GATES="${TG:-vay-ham cang pho-day hero toan-canh}" XOPT="--skydif $SD" bash /w/gpu/pod_gates.sh g64 | grep -E "NC-RENDER|Error|Trace"; mkdir -p out/t_sd$SD; mv out/g64/* out/t_sd$SD/; done
for VB in ${VBS:-0 2}; do GATES=bo-chien-su XOPT="--skydif 0.277 --vbounce $VB" bash /w/gpu/pod_gates.sh g64 | grep -E "NC-RENDER|Error|Trace"; mkdir -p out/t_vb$VB; mv out/g64/* out/t_vb$VB/; done
echo THU-XONG

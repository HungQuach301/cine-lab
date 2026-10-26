#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · sinh trang dựng design/k2v/ldn/bc/look3-b1.js = BẢN SAO design/k2v/ldn/thu-b/look3.js (look3 của THU-B/BAN-CUOI-T4-A, KHÔNG sửa tệp gốc)
+ các chỗ thay có kiểm (mỗi chuỗi gốc phải khớp đúng số lần) theo PHIẾU-A D-A4 (Kinh thánh §19 (d), §14.7 LOOK-T4-9 cập nhật 26/10 10:08, §15 (k) (5)):
  (i)   NIÊN ĐẠI CÔNG TRÌNH MỐC: lịch xây riêng từng phần St Paul's/Monument (bảng LICH, mã tl.x giữ nguyên làm mã mặt nạ 2) — phần đang xây "mọc" bằng
        mặt phẳng cắt dâng dần (không bóp dẹt cả khối như look2): vỏ vòm + đèn lồng hoàn tất 1708,0; thân 1675,5 → 1697; trống 1697 → 1705; tháp tây 1702 → 1708;
        Monument 1671 → 1677,0 (bệ, thân, đầu cột + chóp, bầu lửa); thân Monument có rãnh dọc đọc được (20 rãnh — sọc sáng/tối theo góc quanh tâm cột);
  (ii)  thuyền 2026: sà lan (barge) thân màu gần đen + không boong → đốm elip đen trên mặt nước; nay thân sơn + boong + nắp hầm/công-te-nơ theo thời kỳ (thuyen theo k + y0);
  (iii) nước đêm có lửa: ánh lửa phủ rộng (mờ 12 ô × 8) làm mặt sông thành mảng phẳng màu cát → giảm, điều theo sóng + Fresnel; phản chiếu phẳng giữ phần
        PHÁT SÁNG cộng (lửa, tàn, quầng: alpha 0 trong RT) thay vì bỏ → vệt lửa phản chiếu lăn tăn theo sóng; lửa/khói: quầng rộng + dày hơn (vòng lửa liền),
        khói mép mềm, mật độ đều hơn (không thành cụm bông rời);
  (iv)  vật liệu: đá Portland St Paul's (vỉa đá, ám khói theo thời kỳ, sạch sau 2011), mái chì xám (sáng hơn, ghép tấm + gân + ánh trời), toà kính có tên đa dạng
        theo toà (màu kính/khung/nhịp), toà kính rèm dựng trước 1985 đọc thành văn phòng bê tông (niên đại), đèn pha mái vòm St Paul's + Monument về đêm (từ 1951),
        cửa sổ sáng đêm theo toà/tầng (tỉ lệ sáng, màu ấm/lạnh, độ sáng khác nhau) thay lưới lặp đều;
  (v)   thuộc tính nid.f32 (mã toà OSM có tên, hinh_hoc_b1.py) cho (iv).
  tao_look3_b1.py   → design/k2v/ldn/bc/look3-b1.js (+ in SHA look3.js nguồn)"""
import hashlib, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = os.path.join(REPO, 'design/k2v/ldn/thu-b/look3.js'); DST = os.path.join(REPO, 'design/k2v/ldn/bc/look3-b1.js')
s = open(SRC, encoding='utf-8').read(); sha = hashlib.sha256(s.encode()).hexdigest()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'LỖI vá: chuỗi xuất hiện {c} lần (cần {n}): {old[:90]!r}')
    s = s.replace(old, new)


HEAD = (f"// BAN-CUOI-T4-B1 · TRANG DỰNG look3-b1 = BẢN SAO design/k2v/ldn/thu-b/look3.js (sha256 {sha}, KHÔNG sửa tệp gốc) sinh bằng scripts/k2ldn/bc/tao_look3_b1.py.\n"
        "// Sửa D-A4: (i) lịch xây St Paul's/Monument theo Kinh thánh §19 (d) + rãnh Monument; (ii) sà lan 2026; (iii) nước đêm + lửa/khói 1666; (iv) vật liệu đá Portland/mái chì,\n"
        "// toà kính có tên, niên đại toà kính rèm, đèn pha đêm, cửa sổ đêm theo toà/tầng. Cờ d (uD) như look3. Hình học: $LDN_DATA/look3d (scripts/k2ldn/bc/hinh_hoc_b1.py).\n")
s = HEAD + s

# ---------------------------------------------------------------- (i) lịch xây công trình mốc + (v) nid
LICH = """vec4 lsched(float c){   /* B1 · lịch xây (năm đầu, số năm, đáy, đỉnh phần đang mọc — m trên nền tl.z) theo mã tl.x; Kinh thánh §19 (d) */
        if (abs(c - 1675.5) < 0.05) return vec4(1675.5, 21.5, 0.0, 41.0);    /* St Paul's: thân, hợp xướng, cánh ngang, apse (1675 → hợp xướng mở 1697) */
        if (abs(c - 1697.0) < 0.05) return vec4(1697.0, 8.0, 33.5, 61.8);    /* trống + hàng cột + tầng gác */
        if (abs(c - 1707.0) < 0.05) return vec4(1702.0, 6.0, 0.0, 67.5);     /* mặt tây + hai tháp tây */
        if (abs(c - 1708.5) < 0.05) return vec4(1705.0, 3.0, 61.8, 85.7);    /* vỏ vòm chì — hoàn tất 1708,0 */
        if (abs(c - 1708.8) < 0.05) return vec4(1707.4, 0.6, 85.6, 111.4);   /* Golden Gallery + đèn lồng + quả cầu + thập giá — hoàn tất 1708,0 */
        if (abs(c - 1671.5) < 0.05) return vec4(1671.0, 1.5, 0.0, 13.9);     /* Monument: đế + bệ + rồng */
        if (abs(c - 1672.5) < 0.05) return vec4(1672.5, 3.0, 13.2, 46.5);    /* thân cột có rãnh */
        if (abs(c - 1676.5) < 0.05) return vec4(1675.5, 1.0, 46.4, 58.6);    /* đầu cột, ban công, chóp */
        if (abs(c - 1676.9) < 0.05) return vec4(1676.5, 0.5, 58.5, 61.8);    /* bầu lửa mạ vàng — hoàn tất 1677,0 */
        return vec4(0.0); }"""
rep("attribute float pid; varying float vHid; varying float vPid;",
    "attribute float pid; varying float vHid; varying float vPid; attribute float nid; varying float vNid;\n      " + LICH)
rep("      transformed.y = tl.z + (transformed.y - tl.z) * max(grow, 0.001);\n      vHid = hid; vPid = pid;",
    "      { vec4 S = lsched(tl.x); if (!fireMode && kk > 4.5 && kk < 5.5 && S.y > 0.0) { float g2 = clamp((uYear - S.x) / S.y, 0.0, 1.0);   /* B1: mặt cắt dâng dần */\n"
    "          alive = (uYear >= S.x + 0.02 * S.y && uYear < tl.y) ? 1.0 : 0.0; transformed.y = tl.z + min(transformed.y - tl.z, S.z + (S.w - S.z) * g2); }\n"
    "        else transformed.y = tl.z + (transformed.y - tl.z) * max(grow, 0.001); }\n      vHid = hid; vPid = pid; vNid = nid;")
rep("varying float vHid; varying float vPid; uniform float uProjOn", "varying float vHid; varying float vPid; varying float vNid; uniform float uProjOn")
rep("    g.setAttribute('hid', new THREE.BufferAttribute(await ld32('hid.f32'), 1)); g.setAttribute('pid', new THREE.BufferAttribute(await ld32('pid.f32'), 1)); }",
    "    g.setAttribute('hid', new THREE.BufferAttribute(await ld32('hid.f32'), 1)); g.setAttribute('pid', new THREE.BufferAttribute(await ld32('pid.f32'), 1));\n"
    "    g.setAttribute('nid', new THREE.BufferAttribute(await ld32('nid.f32'), 1)); }   /* B1: mã toà OSM có tên (0 = khác) */")

# ---------------------------------------------------------------- (iv) niên đại toà kính rèm + toà kính có tên đa dạng
rep("int m = int(vMt + 0.5);",
    "int m = int(vMt + 0.5); bool k4 = vK > 3.5 && vK < 4.5;\n"
    "          if (m == 7 && k4 && vTx < 1985.0 && !roof0()) { m = 8; alb = vec3(dot(alb, vec3(0.3, 0.59, 0.11))) * vec3(1.32, 1.28, 1.18); }   /* B1: kính rèm chỉ từ 1985 — trước đó văn phòng bê tông */")
rep("      float glassK = 0.0; vec3 emis = vec3(0.0);",
    "      float glassK = 0.0; vec3 emis = vec3(0.0);\n      bool roof0(){ return mod(floor(vFl / 4.0), 2.0) > 0.5; }\n"
    "      float bidB(){ return vNid > 0.5 ? vNid * 1.37 + 0.5 : (vHid > 0.5 ? vHid * 0.731 : dot(floor(vW.xz / 37.0), vec2(1.0, 57.0))); }   /* B1: mã toà để băm */")
# toà kính rèm (m 7): nhịp/màu/khung theo toà (thay bảng đều 1,5 × 3,9 m)
rep("""            float st = 3.9, bay = 1.5; float y = mod(p.y, st), u = mod(p.x, bay); vec2 cell = floor(vec2(p.x / bay, p.y / st));
            float mull = step(u, 0.07) + step(st - 0.10, y) + step(y, 0.05); float spand = step(3.15, y);
            alb = mix(alb * (0.62 + 0.12 * h21(floor(cell / vec2(6.0, 3.0)) + rnd)), vec3(0.30, 0.32, 0.34), clamp(mull, 0.0, 1.0)); alb = mix(alb, alb * 0.6, spand * 0.6);""",
    """            float bh = bidB(); float b1 = h21(vec2(bh, 1.7)), b2 = h21(vec2(bh, 5.3)), b3 = h21(vec2(bh, 9.1));   /* B1: mỗi toà một loại kính rèm */
            float st = mix(3.6, 4.3, b1), bay = b2 < 0.33 ? 1.2 : (b2 < 0.75 ? 1.5 : 3.0); float y = mod(p.y, st), u = mod(p.x, bay); vec2 cell = floor(vec2(p.x / bay, p.y / st));
            float mw = b3 < 0.3 ? 0.16 : 0.07; float mull = step(u, mw) + step(st - 0.10, y) + step(y, 0.05); float spand = b3 > 0.55 ? step(st - mix(0.6, 1.1, b1), y) : 0.0;
            vec3 tint = b1 < 0.3 ? vec3(0.62, 0.74, 0.80) : (b1 < 0.55 ? vec3(0.66, 0.76, 0.70) : (b1 < 0.8 ? vec3(0.78, 0.80, 0.82) : vec3(0.74, 0.66, 0.56)));
            vec3 frm = b2 < 0.5 ? vec3(0.30, 0.32, 0.34) : (b3 < 0.5 ? vec3(0.62, 0.62, 0.60) : vec3(0.12, 0.13, 0.14));
            alb = mix(alb * tint * 1.25 * (0.62 + 0.12 * h21(floor(cell / vec2(6.0, 3.0)) + rnd)), frm, clamp(mull, 0.0, 1.0)); alb = mix(alb, alb * 0.6, spand * 0.6);""")
# ---------------------------------------------------------------- (iv) đá Portland + Monument rãnh (lớp 5)
rep("            else if (vK > 4.5 && vK < 5.5 || vK > 8.5 && vK < 9.5) { c *= 1.0 - 0.10 * step(fract(p.y / 0.62), 0.06); }",
    """            else if (vK > 4.5 && vK < 5.5 || vK > 8.5 && vK < 9.5) { c *= 1.0 - 0.10 * step(fract(p.y / 0.62), 0.06);
              if (vK > 4.5 && vK < 5.5 && m == 6) {   /* B1: đá Portland — vỉa 0,62 m × khối 1,1–1,6 m sáng/tối lệch, vệt chảy dọc, ám khói than theo thời kỳ (sạch dần 1995 → 2011) */
                float row = floor(p.y / 0.62); float blk = floor((p.x + h21(vec2(row, 2.0)) * 1.6) / mix(1.1, 1.6, h21(vec2(row, 4.0))));
                c *= 0.94 + 0.10 * h21(vec2(blk, row)); c *= 1.0 - 0.08 * step(fract((p.x + h21(vec2(row, 2.0)) * 1.6) / mix(1.1, 1.6, h21(vec2(row, 4.0)))), 0.03);
                float era = smoothstep(1720.0, 1860.0, uYear) * (1.0 - smoothstep(1995.0, 2011.0, uYear)); float sk = fbm3(vec2(p.x * 0.35, p.y * 0.05) + vTx);
                float drip = smoothstep(0.55, 0.85, fbm3(vec2(p.x * 2.2 + vTx * 3.0, p.y * 0.08)));
                c = mix(c, c * vec3(0.34, 0.33, 0.31), era * clamp(0.25 + 0.65 * smoothstep(0.45, 0.75, sk) + 0.35 * drip, 0.0, 0.85));
                c = mix(c, c * vec3(0.93, 0.90, 0.84), 0.6 * drip * (1.0 - era));   /* sau làm sạch: vệt chảy nhạt, ngả kem */
                vec2 mo = vW.xz - vec2(923.0, 39.0); if (abs(vTx - 1672.5) < 0.05 && length(mo) < 3.0) { float an = atan(mo.y, mo.x);   /* thân Monument: 20 rãnh dọc */
                  float fl20 = abs(cos(an * 10.0)); c *= mix(0.62, 1.08, smoothstep(0.15, 0.95, fl20)); } } }""")
# mái chì St Paul's (m 9, lớp 5): sáng hơn, ghép tấm, gân, ánh trời
rep("""          else if (m == 9) { alb = vanC(alb, 8, p, 0.15); vec2 dc = vW.xz - uDomeC; float rr = length(dc); if (vK > 4.5 && vK < 5.5 && rr < 17.0 && rr > 2.0) { float an = atan(dc.y, dc.x); float rib = smoothstep(0.90, 0.985, abs(cos(an * 12.0))); alb = mix(alb, alb * 1.55 + 0.02, rib * 0.85); } }""",
    """          else if (m == 9) { alb = vanC(alb, 8, p, 0.15); vec2 dc = vW.xz - uDomeC; float rr = length(dc);
            if (vK > 4.5 && vK < 5.5) { alb = vanC(vec3(0.255, 0.262, 0.262), 8, p, 0.10) * (0.92 + 0.12 * fbm3(p * vec2(0.6, 0.15)));   /* B1: chì phong hoá xám sáng (không đen) */
              float era = smoothstep(1720.0, 1860.0, uYear) * (1.0 - smoothstep(1995.0, 2011.0, uYear)); alb *= mix(1.0, 0.72, era);
              alb *= 1.0 - 0.10 * step(fract(p.y / 1.9), 0.05);   /* mạch ghép tấm chì ngang */
              alb = mix(alb, vec3(0.40, 0.42, 0.41), 0.25 * smoothstep(0.6, 0.9, fbm3(vec2(p.x * 1.3, p.y * 0.07))));   /* vệt ô-xít trắng chảy dọc */
              glassK = 0.07; }
            if (vK > 4.5 && vK < 5.5 && rr < 17.0 && rr > 2.0) { float an = atan(dc.y, dc.x); float rib = smoothstep(0.90, 0.985, abs(cos(an * 12.0))); alb = mix(alb, alb * 1.45 + 0.02, rib * 0.85); } }""")
# ---------------------------------------------------------------- (iv) đèn pha đêm (St Paul's, Monument) + cửa sổ đêm theo toà/tầng
rep("""        if (uWin > 0.0 && glassK > 0.1 && (vK > 3.5 && vK < 4.5)) { float on = step(0.42, h21(floor(vUvm / vec2(1.5, 3.8)) + floor(vW.xz / 37.0))); gl_FragColor.rgb += vec3(1.0, 0.80, 0.55) * on * uWin * 1.1 * glassK; }""",
    """        if (uWin > 0.0 && glassK > 0.1 && (vK > 3.5 && vK < 4.5)) {   /* B1: cửa sổ đêm theo toà + tầng (thay lưới ô ngẫu nhiên đều 58 %) */
          float bh = bidB(); float occ = mix(0.12, 0.78, h21(vec2(bh, 11.3))); float fy = floor(vUvm.y / 3.9); float fx = floor(vUvm.x / 12.0);
          float flo = step(h21(vec2(bh * 0.71 + fx * 0.13, fy)), occ * 1.15); vec2 cl = floor(vUvm / vec2(1.5, 3.9));
          float on = flo * step(0.28, h21(cl + bh)) + (1.0 - flo) * step(0.93, h21(cl * 1.7 + bh));
          vec3 wc = mix(vec3(1.0, 0.78, 0.50), vec3(0.86, 0.92, 1.0), step(0.55, h21(vec2(bh, 3.3)))) * (0.55 + 0.6 * h21(cl * 0.37 + bh * 0.11));
          float dk = smoothstep(4500.0, 900.0, length(vW - uCam)) * 0.6 + 0.4;   /* xa: bớt nhấp nháy ô nhỏ */
          gl_FragColor.rgb += wc * on * uWin * 1.05 * glassK * dk + wc * 0.035 * uWin * glassK * flo; }
        if (vK > 4.5 && vK < 5.5 && uNight > 0.02 && uYear > 1951.0 && uHour < 0.0 && uH40 < 0.0) {   /* B1: đèn pha mái vòm St Paul's + Monument (đêm, từ 1951) */
          vec2 dc = vW.xz - uDomeC; vec2 mo = vW.xz - vec2(923.0, 39.0); float sp = step(length(dc), 120.0), mn = step(length(mo), 8.0); float hh = vW.y - vBase;
          float fk = sp * (0.55 + 0.55 * smoothstep(30.0, 70.0, hh) * (1.0 - 0.45 * smoothstep(88.0, 112.0, hh))) + mn * 0.75;
          gl_FragColor.rgb += diffuseColor.rgb * vec3(1.0, 0.86, 0.66) * fk * 1.25 * uNight * (0.85 + 0.15 * vn(vW.xz * 0.3 + vW.y * 0.2)); }""")

# ---------------------------------------------------------------- (iii) nước đêm + lửa
rep("          if (ruv.x > 0.0 && ruv.x < 1.0 && ruv.y > 0.0 && ruv.y < 1.0) { vec4 rc = texture2D(uRefl, ruv); env = mix(env, rc.rgb, clamp(rc.a, 0.0, 1.0) * 0.80); } }",
    "          if (ruv.x > 0.0 && ruv.x < 1.0 && ruv.y > 0.0 && ruv.y < 1.0) { vec4 rc = texture2D(uRefl, ruv); float ra = clamp(rc.a, 0.0, 1.0); env = mix(env, rc.rgb, ra * 0.80) + rc.rgb * (1.0 - ra) * 0.85; } }   /* B1: giữ phần phát sáng cộng (lửa) */")
rep("        c += vec3(1.0, 0.45, 0.15) * uFireK * (fg.g * 0.30 + fg.b * 0.12) * (0.25 + F);   // V2: ánh lửa trên mặt sông",
    "        float wl = 0.45 + 0.9 * fbm3(rot * p * vec2(0.09, 0.03) + vec2(uT * 0.08, 0.0));   /* B1: ánh lửa trên mặt sông theo sóng, không phủ phẳng */\n"
    "        c += vec3(1.0, 0.45, 0.15) * uFireK * (fg.g * 0.075 + fg.b * 0.022) * (0.12 + 1.6 * F) * wl;")
rep("        vec3 c = mix(deep, env * vec3(0.92, 0.92, 0.86), F);",
    "        float Fq = min(0.6, F * (1.0 + 1.6 * uNight * max(step(0.0, uHour), step(0.0, uH40))));   /* B1: đêm cháy 1666 + 1940 — vệt phản chiếu lửa đọc được (lửa là nguồn rất sáng) */\n"
    "        vec3 c = mix(deep, env * vec3(0.92, 0.92, 0.86), Fq);")
# lửa: quầng rộng/dày hơn (vòng lửa liền); khói mép mềm + nhiều hạt mỏng hơn
rep("float size = (26.0 + sd.y * 22.0) * step(0.05, I);", "float size = (44.0 + sd.y * 40.0) * step(0.05, I);")
rep("gl_FragColor = vec4(vec3(1.0, 0.40, 0.09) * k * vA * 0.20 * (0.25 + 0.75 * uNight), 0.0); }", "gl_FragColor = vec4(vec3(1.0, 0.40, 0.09) * k * vA * 0.23 * (0.25 + 0.75 * uNight), 0.0); }")
rep("        d = smoothstep(0.04, 0.55, t.r) * vA * 0.85 * smoothstep(0.0, 0.10, vUv.y) * smoothstep(1.0, 0.45, vUv.y) * smoothstep(0.0, 0.24, min(vUv.x, 1.0 - vUv.x));   /* V2: khói đặc khối, mép rõ */",
    "        d = smoothstep(0.04, 0.55, t.r) * vA * 0.85 * smoothstep(0.0, 0.10, vUv.y) * smoothstep(1.0, 0.45, vUv.y) * smoothstep(0.0, 0.24, min(vUv.x, 1.0 - vUv.x));   /* V2: khói đặc khối, mép rõ */\n"
    "        if (uNight > 0.5) d = smoothstep(0.0, 0.85, t.r) * vA * 0.62 * smoothstep(0.0, 0.22, vUv.y) * smoothstep(1.0, 0.30, vUv.y) * smoothstep(0.0, 0.42, min(vUv.x, 1.0 - vUv.x));   /* B1: khói đêm mép mềm, mỏng hơn — cột khói liền */")
rep("  const smoke = new THREE.Mesh(mk(key === '40' ? 2 : 3),", "  const smoke = new THREE.Mesh(mk(key === '40' ? 2 : 4),")

# ---------------------------------------------------------------- (ii) thuyền theo kiểu + thời kỳ (sà lan 2026 có boong + công-te-nơ)
rep("function hullGeo(kind) {", "function hullGeo(kind, y0) {")
rep("  else if (kind === 'barge') { hull(26, 6.5, 1.8, [0.16, 0.14, 0.12]); }",
    """  else if (kind === 'barge') { hull(26, 6.5, 1.8, y0 > 1980 ? [0.20, 0.22, 0.25] : [0.26, 0.19, 0.13]);   /* B1: thân sơn (không gần đen) + boong + nắp hầm / công-te-nơ */
    const dk = new THREE.BoxGeometry(24, 0.25, 5.6); dk.translate(0, 1.45, 0); add(dk, lin([0.42, 0.40, 0.37]));
    if (y0 > 1980) { const cols = [[0.78, 0.62, 0.22], [0.70, 0.72, 0.74], [0.30, 0.42, 0.55]]; for (let i = 0; i < 3; i++) { const c = new THREE.BoxGeometry(6.0, 2.4, 2.4); c.translate(-7.5 + i * 7.5, 2.8, 0); add(c, lin(cols[i])); } }
    else { const tp = new THREE.BoxGeometry(18, 0.9, 5.0); tp.translate(0, 2.0, 0); add(tp, lin([0.34, 0.33, 0.28])); } }""")
rep("  const L = await (await fetch(base + LK + 'thuyen.json')).json(); const kinds = [...new Set(L.map((b) => b.k))]; const M4 = new THREE.Matrix4();\n"
    "  for (const k of kinds) { const list = L.filter((b) => b.k === k); const mat = new THREE.MeshLambertMaterial({ vertexColors: true });",
    "  const L = await (await fetch(base + LK + 'thuyen.json')).json(); const kinds = [...new Set(L.map((b) => b.k + '|' + b.y0))]; const M4 = new THREE.Matrix4();   /* B1: nhóm theo kiểu + thời kỳ */\n"
    "  for (const ky of kinds) { const [k, y0s] = ky.split('|'); const list = L.filter((b) => b.k === k && String(b.y0) === y0s); const mat = new THREE.MeshLambertMaterial({ vertexColors: true });")
rep("    const im = new THREE.InstancedMesh(hullGeo(k), mat, list.length);", "    const im = new THREE.InstancedMesh(hullGeo(k, +y0s), mat, list.length);")

os.makedirs(os.path.dirname(DST), exist_ok=True); open(DST, 'w', encoding='utf-8').write(s)
print(DST, 'nguồn look3.js sha256', sha, '→', hashlib.sha256(s.encode()).hexdigest())

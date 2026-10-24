#!/opt/cine/bin/python
"""THU-B-T4 · sinh trang dựng design/k2v/ldn/thu-b/look3.js = BẢN SAO design/k2v/ldn/look2.js (LOOK-T4-V2, KHÔNG sửa) + các chỗ thay có kiểm (mỗi chuỗi gốc phải khớp đúng số lần).
  tao_look3.py   → design/k2v/ldn/thu-b/look3.js (+ in SHA look2.js nguồn)
Thêm (mọi thứ mặc định TẮT → với uD = uD2 = uProjOn = uBong = 0 và mặt nạ 1/2, ảnh ra trùng look2.js — kiểm bằng so điểm ảnh, xem báo cáo §3):
  · thuộc tính hid/pid (mã nhà thường, mã mặt phẳng — hinh_hoc_thub.py); mặt nạ 1 tô nhà thường (215, 215, 215) = lớp `nha_thuong` (K-1.17.5 §7);
    mặt nạ 3 = mã nhà 24 bit, 4 = mã mặt phẳng 24 bit, 6 = albedo tuyến tính (mã hoá sRGB) — mọi bề mặt khác đen;
  · f.bong: pass bóng (albedo xám đều 0,6, không vân/kính) cùng máy/giờ;
  · f.proj: chiếu ảnh AI đã khử sáng (albedo) lên hình học nhà thường bằng ma trận máy chiếu (camera projection), rồi dựng lại ánh sáng theo giờ khung;
  · f.d (biến thể D): màu/phong hoá/vệt chảy/tiếp đất/rêu/mép mái theo nhà; kính 2026 phản chiếu dải phố + trời theo ô kính;
  · f.d2 (D + vân nướng): vân mặt tiền/mái nướng từ ảnh AI (tFac/tRoof) theo nhà thường, albedo phẳng hiệu chuẩn theo trung bình vân CC0."""
import hashlib, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = os.path.join(REPO, 'design/k2v/ldn/look2.js'); DST = os.path.join(REPO, os.environ.get('LOOK3_DST', 'design/k2v/ldn/thu-b/look3.js'))
s = open(SRC, encoding='utf-8').read(); sha = hashlib.sha256(s.encode()).hexdigest()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'LỖI vá: chuỗi xuất hiện {c} lần (cần {n}): {old[:90]!r}')
    s = s.replace(old, new)


HEAD = ("// THU-B-T4 · TRANG DỰNG look3 = BẢN SAO design/k2v/ldn/look2.js (sha256 %s, KHÔNG sửa tệp gốc) sinh bằng scripts/k2ldn/thu-b/tao_look3.py.\n"
        "// Thêm (mặc định tắt): mã nhà/mặt phẳng + lớp nha_thuong (BE-MAT-NHA, K-1.17.5 §7), pass bóng, albedo, chiếu ảnh AI đã khử sáng lên nhà thường (B cách ii),\n"
        "// biến thể D (nâng 3D bề mặt theo nhà, kính 2026) và D2 (vân nướng mặt tiền/mái từ ảnh AI). Hình học: $LDN_DATA/look3b|look3d (hinh_hoc_thub.py).\n") % sha
s = HEAD + s
# --- uniform mới
rep("uDomeC: { value: new THREE.Vector2(0, 0) }, uToy: { value: 1 } };",
    "uDomeC: { value: new THREE.Vector2(0, 0) }, uToy: { value: 1 },\n"
    "  uProjOn: { value: 0 }, uProj: { value: null }, uProjVP: { value: new THREE.Matrix4() }, uBong: { value: 0 }, uD: { value: 0 }, uD2: { value: 0 },\n"
    "  tFac: { value: null }, tRoof: { value: null }, uFacN: { value: new THREE.Vector4(4, 6, 12, 13.5) }, uFacMean: { value: [V3(0.5, 0.5, 0.5), V3(0.5, 0.5, 0.5), V3(0.5, 0.5, 0.5), V3(0.5, 0.5, 0.5)] } };")
# --- thuộc tính + varying (bóng và màu dùng chung chuỗi đỉnh)
rep("attribute vec4 tl; attribute float kk; attribute vec2 uvm; attribute float mt; attribute float fl; uniform float uYear, uHour;",
    "attribute vec4 tl; attribute float kk; attribute vec2 uvm; attribute float mt; attribute float fl; uniform float uYear, uHour; attribute float hid; attribute float pid; varying float vHid; varying float vPid;")
rep("vAlive = alive; vBurn = fireMode ? burnI(ign, uHour) : 0.0;", "vHid = hid; vPid = pid; vAlive = alive; vBurn = fireMode ? burnI(ign, uHour) : 0.0;")
rep("varying float vAlive; varying float vBurn; varying vec3 vW; varying float vK; varying vec2 vUvm; varying float vMt; varying float vFl; varying float vIgn; varying float vBase; varying float vTx; uniform vec2 uDomeC; uniform float uToy;",
    "varying float vAlive; varying float vBurn; varying vec3 vW; varying float vK; varying vec2 vUvm; varying float vMt; varying float vFl; varying float vIgn; varying float vBase; varying float vTx; uniform vec2 uDomeC; uniform float uToy;\n"
    "      varying float vHid; varying float vPid; uniform float uProjOn, uBong, uD, uD2; uniform sampler2D uProj, tFac, tRoof; uniform mat4 uProjVP; uniform vec4 uFacN; uniform vec3 uFacMean[4];\n"
    "      vec3 enc24(float id){ float r = floor(id / 65536.0); float g = floor((id - r * 65536.0) / 256.0); float b = id - r * 65536.0 - g * 256.0; return vec3(r, g, b) / 255.0; }\n"
    "      vec3 l2s(vec3 c){ c = clamp(c, 0.0, 1.0); return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c)); }")
# --- bề mặt nhà thường: D, D2, chiếu ảnh, bóng (chèn ngay trước diffuseColor.rgb = alb của vật liệu nhà)
NEW_SURF = r"""          if (vK > 1.5 && vK < 2.5) alb *= 0.38 + 0.15 * vn(vW.xz * 0.4);   // phế tích: than, tro, gạch ám (Evelyn 7/9: "the ground under my feet so hot")
          bool nt = vHid > 0.5;
          if (uD > 0.5 && nt) { float hs = h21(vec2(vHid * 0.0137, 3.1)), hs2 = h21(vec2(vHid * 0.0291, 7.7)), hs3 = h21(vec2(vHid * 0.0533, 1.9));   /* THU-B D: mỗi nhà một độ sáng/ngả màu/độ bẩn */
            alb *= mix(0.80, 1.14, hs); alb = mix(alb, alb * vec3(1.07, 0.98, 0.90), hs2 * 0.7); alb = mix(alb, vec3(dot(alb, vec3(0.3, 0.59, 0.11))), 0.18 * hs3);
            if (!roof) { float sk = fbm3(vec2(p.x * 1.6 + vHid * 0.71, p.y * 0.22)); float st2 = smoothstep(0.45, 0.85, fbm3(vec2(p.x * 3.1 + vHid, p.y * 0.05)));
              alb *= mix(1.0, 0.78 + 0.28 * sk, 0.75); alb *= 1.0 - 0.22 * st2 * smoothstep(0.0, 6.0, p.y);   /* vệt chảy dọc dưới bậu/mái */
              alb *= mix(0.50, 1.0, smoothstep(0.0, 2.4, p.y)); }   /* tiếp đất: chân tường ám bẩn + bóng tiếp xúc */
            else { float ms = fbm3(p * 0.55 + vHid * 0.37); alb = mix(alb, alb * vec3(0.74, 0.82, 0.66), 0.40 * smoothstep(0.50, 0.80, ms)); alb *= mix(0.66, 1.0, smoothstep(0.0, 0.7, p.y));
              alb *= 0.90 + 0.18 * vn(p * vec2(0.9, 3.2) + vHid); } }   /* rêu/ám khói loang + mép mái tối + hàng ngói lệch */
          if (uD > 0.5 && !nt && ((vK > 5.5 && vK < 6.5) || (vK > 7.5 && vK < 8.5))) { float hs = h21(floor(vW.xz * 0.05) + 0.7); float sk = fbm3(vec2(p.x * 0.8 + hs * 7.0, p.y * 0.15));   /* THU-B D: đá ám khói than theo khối (nhà thờ giáo xứ, tường) — chỉ bề mặt */
            alb *= mix(0.70, 0.95, hs) * (0.84 + 0.22 * sk); if (!roof) alb *= mix(0.62, 1.0, smoothstep(0.0, 3.0, p.y)); }
          if (uD2 > 0.5 && nt) { float tix = floor(h21(vec2(vHid * 0.0071, 5.3)) * 8.0); float era = vK < 1.5 ? 0.0 : (vK > 2.5 && vK < 3.5) ? 1.0 : (vK > 3.5 && vK < 4.5) ? 2.0 : -1.0;   /* THU-B D2: vân nướng mặt tiền/mái từ ảnh AI (8 mặt tiền/thời kỳ; nhà 1666 gạch và khối Victoria: giữ thủ tục) */
            if (!roof && era >= 0.0 && !(era < 0.5 && m == 2) && m != 14 && m != 7 && m != 13) { float off = h21(vec2(vHid * 0.013, 9.1)) * uFacN.z; vec2 fu = 0.01 + 0.98 * vec2(fract((p.x + off) / uFacN.z), fract(max(p.y, 0.0) / uFacN.w));
              float cl = mod(tix, 4.0), rw = era * 2.0 + floor(tix / 4.0); vec3 fc = texture2D(tFac, vec2((cl + fu.x) / uFacN.x, (rw + 1.0 - fu.y) / uFacN.y)).rgb; int ri = int(era);
              vec3 fm = ri == 0 ? uFacMean[0] : ri == 1 ? uFacMean[1] : uFacMean[2]; alb = mix(alb, fc / max(fm, vec3(0.02)) * dot(alb, vec3(0.333)), 0.92); glassK *= 0.35; }
            else if (roof) { float rr = (m == 3) ? 0.0 : (m == 4) ? 1.0 : 2.0; vec2 ru = 0.01 + 0.98 * fract((p + vec2(h21(vec2(vHid, 2.0)), h21(vec2(vHid, 4.0))) * 8.0) / vec2(8.0, 13.5));
              vec3 rc = texture2D(tRoof, vec2((rr + ru.x) / 3.0, ru.y)).rgb; alb = mix(alb, rc / max(uFacMean[3], vec3(0.02)) * dot(alb, vec3(0.333)), 0.85); } }
          if (uProjOn > 0.5 && nt) { vec4 cp = uProjVP * vec4(vW, 1.0); vec2 q = cp.xy / cp.w * 0.5 + 0.5;   /* THU-B B (ii): ảnh AI đã khử sáng chiếu lên hình học */
            if (cp.w > 0.0 && q.x > 0.0 && q.y > 0.0 && q.x < 1.0 && q.y < 1.0) { vec4 pr = texture2D(uProj, q); if (pr.a > 0.5) { alb = pr.rgb; glassK = 0.0; } } }
          if (uBong > 0.5) { alb = vec3(0.6); glassK = 0.0; }
          diffuseColor.rgb = alb; }`)"""
rep("""          if (vK > 1.5 && vK < 2.5) alb *= 0.38 + 0.15 * vn(vW.xz * 0.4);   // phế tích: than, tro, gạch ám (Evelyn 7/9: "the ground under my feet so hot")
          diffuseColor.rgb = alb; }`)""", NEW_SURF)
# --- kính 2026 (D): phản chiếu dải phố/nhà phía dưới đường chân trời + trời, ô kính lệch nhẹ
rep("if (glassK > 0.01) { vec3 Rf = reflect(Vd, Nw); Rf.y = abs(Rf.y) * 0.7 + 0.02;",
    "if (glassK > 0.01) { vec3 Rf = reflect(Vd, Nw); float ry0 = Rf.y; if (uD > 0.5) { vec2 cl = floor(vUvm / vec2(1.5, 3.9)); Rf = normalize(Rf + vec3(h21(cl) - 0.5, 0.0, h21(cl + 3.3) - 0.5) * 0.06); ry0 = Rf.y; } Rf.y = abs(Rf.y) * 0.7 + 0.02;")
rep("gl_FragColor.rgb = mix(gl_FragColor.rgb, env, clamp(glassK * mix(0.35, 0.95, fr), 0.0, 1.0)); }",
    "if (uD > 0.5) { float bnd = smoothstep(-0.02, 0.10, ry0 + 0.05 * (vn(vW.xz * 0.05 + vW.y * 0.02) - 0.5)); vec3 city = mix(vec3(0.075, 0.072, 0.068), vec3(0.16, 0.15, 0.14), vn(vec2(atan(Rf.x, Rf.z) * 40.0, 1.0))) * (1.0 - 0.85 * uNight);\n"
    "          env = mix(city, env, bnd); }\n"
    "          gl_FragColor.rgb = mix(gl_FragColor.rgb, env, clamp(glassK * mix(0.35, 0.95, fr), 0.0, 1.0)); }")
# --- mặt nạ: mọi bề mặt khác ĐEN ở mặt nạ ≥ 3; nhà: 1 (lớp, nhà thường 215), 2 (mã công trình), 3 (mã nhà), 4 (mã mặt phẳng), 6 (albedo)
n0 = s.count('if (uMask > 0.5) gl_FragColor = vec4(')
s = s.replace('if (uMask > 0.5) gl_FragColor = vec4(', 'if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(')
if n0 < 7: sys.exit(f'LỖI vá: chỉ {n0} chỗ mặt nạ (cần ≥ 7)')
rep("if (uMask > 1.5) { float id = 0.0;", "if (uMask > 1.5 && uMask < 2.5) { float id = 0.0;")
rep("gl_FragColor = (vK > 4.5 && vK < 5.5 && id > 0.5) ? vec4(vec3(id * 20.0, 0.0, 200.0) / 255.0, 1.0) : vec4(0.0, 0.0, 0.0, 1.0); }`);",
    "gl_FragColor = (vK > 4.5 && vK < 5.5 && id > 0.5) ? vec4(vec3(id * 20.0, 0.0, 200.0) / 255.0, 1.0) : vec4(0.0, 0.0, 0.0, 1.0); }\n"
    "        if (uMask > 0.5 && uMask < 1.5 && vHid > 0.5) gl_FragColor = vec4(vec3(215.0) / 255.0, 1.0);   /* THU-B: lớp nha_thuong (K-1.17.5) */\n"
    "        if (uMask > 2.5 && uMask < 3.5) gl_FragColor = vec4(vHid > 0.5 ? enc24(floor(vHid + 0.5)) : vec3(0.0), 1.0);   /* làm tròn: nội suy varying lệch ε dưới số nguyên */\n"
    "        if (uMask > 3.5 && uMask < 4.5) gl_FragColor = vec4(vHid > 0.5 ? enc24(floor(vPid + 0.5)) : vec3(0.0), 1.0);\n"
    "        if (uMask > 5.5) gl_FragColor = vec4(l2s(diffuseColor.rgb), 1.0);`);")
# --- địa hình: pass bóng xám đều
rep("varying vec3 vW; varying float vWet; uniform sampler2D uFire, uFire40, uBake, tC66, tC26;", "uniform float uBong, uD; varying vec3 vW; varying float vWet; uniform sampler2D uFire, uFire40, uBake, tC66, tC26;")
rep("cc = mix(cc, vec3(0.13, 0.115, 0.095), vWet * 0.85);\n        vec4 diffuseColor = vec4(cc, 1.0);`)",
    "cc = mix(cc, vec3(0.13, 0.115, 0.095), vWet * 0.85); if (uD > 0.5) cc *= 0.80 + 0.28 * fbm3(p * 0.31 + 3.3); if (uBong > 0.5) cc = vec3(0.6);\n        vec4 diffuseColor = vec4(cc, 1.0);`)")
rep("reflectedLight.directDiffuse *= mix(1.0, smoothstep(0.05, 0.6, sk) * 0.4 + 0.6, uBakeK * 0.5); } }`)",
    "reflectedLight.directDiffuse *= mix(1.0, smoothstep(0.05, 0.6, sk) * 0.4 + 0.6, uBakeK * 0.5);\n          if (uD > 0.5) { reflectedLight.directDiffuse *= smoothstep(0.15, 0.75, sk) * 0.35 + 0.65; reflectedLight.indirectDiffuse *= mix(1.0, sk, 0.5); } } }`)")
# --- nạp hid/pid (nếu có) cùng các thuộc tính khác (trước khi chia ô 300 m)
rep("  g.computeVertexNormals();\n  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); patchB(m, false);",
    "  { const nv = pos.length / 3; const ld32 = async (nm) => { try { const r = await fetch(base + LK + nm); if (!r.ok) return new Float32Array(nv); const a = new Float32Array(await r.arrayBuffer()); return a.length === nv ? a : new Float32Array(nv); } catch (e) { return new Float32Array(nv); } };\n"
    "    g.setAttribute('hid', new THREE.BufferAttribute(await ld32('hid.f32'), 1)); g.setAttribute('pid', new THREE.BufferAttribute(await ld32('pid.f32'), 1)); }\n"
    "  g.computeVertexNormals();\n  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); patchB(m, false);")
# --- khung: mặt nạ mọi số; bóng; chiếu; D; D2
rep("if (f.mask) { U.uMask.value = f.mask === 2 ? 2 : 1;", "if (f.mask) { U.uMask.value = f.mask;")
rep("  U.uToy.value = f.look && f.look.toy != null ? f.look.toy : 1; CHIM.visible = f.chim !== false;",
    "  U.uToy.value = f.look && f.look.toy != null ? f.look.toy : 1; CHIM.visible = f.chim !== false;\n"
    "  U.uBong.value = f.bong ? 1 : 0; U.uD.value = f.d ? 1 : 0; U.uD2.value = (f.d2 && U.tFac.value) ? 1 : 0;\n"
    "  if (f.proj && PROJ.url !== f.proj.url) { PROJ.url = f.proj.url; U.uProj.value = await new Promise((r) => new THREE.TextureLoader().load(f.proj.url, (t) => { t.colorSpace = THREE.SRGBColorSpace; t.flipY = true; t.minFilter = t.magFilter = THREE.LinearFilter; t.generateMipmaps = false; r(t); }, undefined, () => r(null))); }\n"
    "  if (f.proj && U.uProj.value) { U.uProjVP.value.fromArray(f.proj.vp); U.uProjOn.value = 1; } else U.uProjOn.value = 0;")
rep("window.ready = true;",
    "const PROJ = { url: null };\n"
    "// THU-B D2: nạp atlas vân nướng (mặt tiền 3 hàng × N cột; mái 3 ô) + trung bình tuyến tính từng hàng để hiệu chuẩn albedo\n"
    "window.setFac = async (fac, roof, n) => { const ld = (u) => new Promise((r) => new THREE.TextureLoader().load(u, (t) => { t.colorSpace = THREE.SRGBColorSpace; t.flipY = false; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 1; r(t); }, undefined, () => r(null)));\n"
    "  U.tFac.value = await ld(fac); U.tRoof.value = await ld(roof); U.uFacN.value.set(...n.grid); U.uFacMean.value = n.mean.map((c) => V3(...c)); return !!(U.tFac.value && U.tRoof.value); };\n"
    "window.ready = true;")
os.makedirs(os.path.dirname(DST), exist_ok=True); open(DST, 'w', encoding='utf-8').write(s)
print('look3.js', len(s), 'byte · nguồn look2.js sha256', sha, '· chỗ mặt nạ', n0)

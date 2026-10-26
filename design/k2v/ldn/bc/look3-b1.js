// BAN-CUOI-T4-B1 · TRANG DỰNG look3-b1 = BẢN SAO design/k2v/ldn/thu-b/look3.js (sha256 5b726c5afcea16571418466372527f64437d93dca9bb831c35f22f969cf00146, KHÔNG sửa tệp gốc) sinh bằng scripts/k2ldn/bc/tao_look3_b1.py.
// Sửa D-A4: (i) lịch xây St Paul's/Monument theo Kinh thánh §19 (d) + rãnh Monument; (ii) sà lan 2026; (iii) nước đêm + lửa/khói 1666; (iv) vật liệu đá Portland/mái chì,
// toà kính có tên, niên đại toà kính rèm, đèn pha đêm, cửa sổ đêm theo toà/tầng. Cờ d (uD) như look3. Hình học: $LDN_DATA/look3d (scripts/k2ldn/bc/hinh_hoc_b1.py).
// THU-B-T4 · TRANG DỰNG look3 = BẢN SAO design/k2v/ldn/look2.js (sha256 47de958eb792c60cab8471bea6ff997c21df5ce895e59d6fb18b0c0624eee906, KHÔNG sửa tệp gốc) sinh bằng scripts/k2ldn/thu-b/tao_look3.py.
// Thêm (mặc định tắt): mã nhà/mặt phẳng + lớp nha_thuong (BE-MAT-NHA, K-1.17.5 §7), pass bóng, albedo, chiếu ảnh AI đã khử sáng lên nhà thường (B cách ii),
// biến thể D (nâng 3D bề mặt theo nhà, kính 2026) và D2 (vân nướng mặt tiền/mái từ ảnh AI). Hình học: $LDN_DATA/look3b|look3d (hinh_hoc_thub.py).
// K2V ldn · TRANG DỰNG LOOK LONDON V2 (LOOK-T4-V2, K2C-T4-02) — bản sao look.js (LOOK-T4, giữ nguyên để tái lập) + nâng: lửa có lõi + quầng, tàn lửa theo gió, khói ngày đặc khối/tách tầng,
// mặt dưới cột khói hắt đỏ, ánh lửa mặt tiền/mặt sông mạnh hơn; vật liệu công trình có tên (gân vòm chì St Paul's, lưới 30 St Mary Axe, khung giằng Leadenhall); chống 'đồ chơi' (mái/tường phong hoá, ám khói);
// mặt nạ đo công trình (uMask 2: mã năm tl.x của lớp 5). Hình học: $LDN_DATA/look2/ (hinh_hoc_v2.py).
// (dòng gốc) K2V ldn · TRANG DỰNG LOOK LONDON (LOOK-T4, K2C-T4-02) — cách A chất lượng look: three.js 0.180 + post.js dùng chung, Chromium headless (llvmpipe).
// Hình học v2: scripts/k2ldn/hinh_hoc_look.py (ldn2.bin: pos · col · tl · k · uv mét · mt vật liệu · fl cờ mặt tiền). Không sửa page.js (tiền kỳ) hay design/k2v/tl/* (T3).
// Lớp look (nâng từ tiền kỳ, kỹ thuật theo NC-CPU cách A §2.1): (1) vân ảnh CC0 Poly Haven theo vật liệu (mảng vân 16 lớp, chống lặp ô kiểu Quilez, chuẩn hoá theo trung bình lớp);
//  (2) mặt tiền thủ tục theo uv mét: khung gỗ + cửa sổ chì + cửa hàng tầng trệt (1666), cửa sổ gạch (1667+), Victoria, văn phòng, tường kính phản trời (2026);
//  (3) ánh sáng nướng Cycles theo mốc (bake.png: R = trời có che khuất + nảy) → AO phố/chân tường; (4) nước Thames: sóng nhiều hướng + phản chiếu phẳng + màu nước sông;
//  (5) khí quyển có độ cao (sương + lớp khói than thấp theo biến thể); (6) cây, thuyền theo mốc, khói bếp; (7) lửa/khói 1666 (atlas cách A) và 1940 (lưới ước lượng).
// Biến thể look (A/B/C) chỉ đổi tham số f.look (ánh sáng–màu–khí quyển–mật độ chi tiết); màu cuối (LUT) áp ở bước xuất (scripts/k2ldn/look_lut.py).
import * as THREE from '/cong3/shared/node_modules/three/build/three.module.js';
import { createPipeline, createRenderer } from '/cong3/shared/post.js';
import { sunPos, jdOf, jdJulian } from '/k2v/tl/sun.js';

const LON = { lat: 51.512, lon: -0.098 };
let LK = 'look2/'; let EMB = null, GLOW = {};
let R, pipe, scene, cam, META, BLD, TER, WATER, SKY, FIRE, SMOKE, CHIM, TREES, BOATS = [], FTEX, F40TEX, FMAP, F40, LG = {}, CFG, RT_REFL, RCAM;
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const U = { uYear: { value: 1666.5 }, uHour: { value: -1 }, uH40: { value: -1 }, uT: { value: 0 }, uNight: { value: 0 }, uFire: { value: null }, uFire40: { value: null }, uFireBox: { value: new THREE.Vector4() },
  uSunDir: { value: V3(0, 1, 0) }, uSunCol: { value: new THREE.Color(1, 1, 1) }, uSkyTop: { value: new THREE.Color(0.25, 0.42, 0.75) }, uSkyHor: { value: new THREE.Color(0.65, 0.72, 0.82) },
  uHaze: { value: new THREE.Color(0.7, 0.74, 0.8) }, uHazeS: { value: 1 / 9000 }, uHazeH: { value: 300 }, uCoal: { value: 0 }, uCoalCol: { value: new THREE.Color(0.55, 0.50, 0.44) }, uCoalH: { value: 70 },
  uCam: { value: V3() }, uFireK: { value: 1 }, uWin: { value: 0 }, uTexK: { value: 1 }, uCloud: { value: 0.35 }, uCloudCol: { value: new THREE.Color(1, 1, 1) },
  uWater: { value: new THREE.Color(0.06, 0.07, 0.055) }, uBake: { value: null }, uBakeBox: { value: new THREE.Vector4(0, 0, 1, 1) }, uBakeOn: { value: 0 }, uBakeK: { value: 1 },
  tVanD: { value: null }, uVanMean: { value: [] }, uVanS: { value: [] }, uWind: { value: new THREE.Vector2(-1, 0) }, uRefl: { value: null }, uReflVP: { value: new THREE.Matrix4() }, uReflOn: { value: 0 },
  uMask: { value: 0 }, uWarm: { value: 0 }, uDbg: { value: 0 }, uDomeC: { value: new THREE.Vector2(0, 0) }, uToy: { value: 1 },
  uProjOn: { value: 0 }, uProj: { value: null }, uProjVP: { value: new THREE.Matrix4() }, uBong: { value: 0 }, uD: { value: 0 }, uD2: { value: 0 },
  tFac: { value: null }, tRoof: { value: null }, uFacN: { value: new THREE.Vector4(4, 6, 12, 13.5) }, uFacMean: { value: [V3(0.5, 0.5, 0.5), V3(0.5, 0.5, 0.5), V3(0.5, 0.5, 0.5), V3(0.5, 0.5, 0.5)] } };
// lớp vân (thứ tự = scripts/k2ldn/tai_van.py) + cỡ thật (m)
const VAN = [['plastered_wall_02', 2.23], ['medieval_wood', 2.0], ['brick_wall_02', 2.0], ['clay_roof_tiles_02', 2.5], ['roof_slates_02', 3.0], ['old_stone_wall', 2.0], ['white_sandstone_bricks', 2.0],
  ['concrete_wall_008', 2.71], ['metal_plate', 1.5], ['cobblestone_floor_01', 1.6], ['brown_mud_02', 2.6], ['aerial_asphalt_01', 30.0], ['granite_tile', 2.3], ['leafy_grass', 2.0], ['old_planks_02', 2.0], ['brick_wall_006', 3.0]];
const yearOfHour = (h) => 1666 + (244 + h / 24) / 365;
const burnI = `float burnI(float ign, float h){ if (ign < 0.0 || h < ign) return 0.0; float a = h - ign;
  return smoothstep(0.0, 0.7, a) * (1.0 - smoothstep(4.0, 9.0, a)) + 0.025 * (1.0 - smoothstep(9.0, 48.0, a)) * step(9.0, a); }
  float burnI40(float ign, float h){ if (ign < 0.0 || h < ign) return 0.0; float a = h - ign; return smoothstep(0.0, 0.4, a) * (1.0 - 0.6 * smoothstep(3.0, 8.0, a)); }`;
const GLSL_N = `vec3 s2l(vec3 c){ return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }
  float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f); return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
  float fbm(vec2 p){ float s = 0.0, a = 0.5; for (int i = 0; i < 5; i++){ s += a * vn(p); p = p * 2.03 + 7.1; a *= 0.5; } return s; }
  float fbm3(vec2 p){ float s = 0.0, a = 0.5; for (int i = 0; i < 3; i++){ s += a * vn(p); p = p * 2.03 + 7.1; a *= 0.5; } return s; }`;
// khí quyển có độ cao: độ sâu quang học tích phân mật độ e^(−y/H) dọc tia camera → điểm; + lớp khói than thấp (biến thể B)
const HAZE = `uniform vec3 uHaze, uCam, uSunDir, uSunCol, uCoalCol; uniform float uHazeS, uHazeH, uCoal, uCoalH, uNight;
  float odL(float y0, float y1, float H){ float dy = y1 - y0; if (abs(dy) < 0.5) return exp(-max(y0, 0.0) / H); return (exp(-max(min(y0, y1), 0.0) / H) - exp(-max(max(y0, y1), 0.0) / H)) * H / abs(dy); }
  vec3 hazeApply(vec3 c, vec3 wp){ vec3 d = wp - uCam; float L = length(d); vec3 V = d / max(L, 1e-3);
    float tau = uHazeS * L * odL(uCam.y, wp.y, uHazeH); float tc = uCoal * L * odL(uCam.y, wp.y, uCoalH);
    float sd = max(dot(V, uSunDir), 0.0); vec3 hc = uHaze + uSunCol * 0.18 * pow(sd, 6.0) * (1.0 - uNight);
    c = mix(c, hc, 1.0 - exp(-tau)); c = mix(c, uCoalCol * mix(1.0, 0.04, uNight), 1.0 - exp(-tc)); return c; }`;
const VANG = `uniform highp sampler2DArray tVanD; uniform vec3 uVanMean[16]; uniform float uVanS[16]; uniform float uTexK;
  vec3 van(int L, vec2 p){ vec2 q = p / uVanS[L]; float k = vn(q * 0.37) * 6.0, ia = floor(k), f = fract(k); vec2 oa = sin(vec2(3.0, 7.0) * ia), ob = sin(vec2(3.0, 7.0) * (ia + 1.0));
    vec3 a = texture(tVanD, vec3(q + oa, float(L))).rgb, b = texture(tVanD, vec3(q + ob, float(L))).rgb;
    vec3 t = mix(a, b, smoothstep(0.2, 0.8, f)) / max(uVanMean[L], vec3(0.02)); return clamp(mix(vec3(1.0), t, 0.85 * uTexK), vec3(0.12), vec3(2.6)); }
  vec3 vanC(vec3 alb, int L, vec2 p, float kc){ vec3 t = van(L, p); float lt = dot(t, vec3(0.299, 0.587, 0.114)); return alb * mix(vec3(lt), t, kc); }`;
// bầu trời: dải màu theo biến thể + mây fbm + mặt trời; đêm + ánh lửa
const SKYF = `uniform vec3 uSkyTop, uSkyHor, uCloudCol; uniform float uCloud, uFireK, uT, uH40; uniform float uHour;
  vec3 skyCol(vec3 d){ float h = clamp(d.y, -0.05, 1.0); vec3 c = mix(uSkyHor, uSkyTop, pow(clamp(h, 0.0, 1.0), 0.45));
    float sd = max(dot(d, uSunDir), 0.0); c += uSunCol * (pow(sd, 1200.0) * 40.0 + pow(sd, 24.0) * 0.20 + pow(sd, 4.0) * 0.06) * step(-0.02, uSunDir.y) * (1.0 - uNight);
    if (d.y > 0.0) { vec2 q = d.xz / (d.y + 0.08) * 0.8; float n = fbm(q * 1.2 + vec2(3.7, 1.1) + uT * 0.002), m2 = fbm(q * 3.7 - 2.3);
      float cov = smoothstep(1.0 - uCloud - 0.15, 1.0 - uCloud + 0.20, n * 0.85 + m2 * 0.25) * smoothstep(0.0, 0.10, d.y);
      vec3 lit = mix(uCloudCol * 0.72, uCloudCol, smoothstep(0.4, 0.85, m2)) + uSunCol * 0.12 * pow(sd, 3.0) * (1.0 - uNight);
      c = mix(c, lit, cov * 0.9); }
    float fk = uFireK * (uHour >= 0.0 || uH40 >= 0.0 ? 1.0 : 0.0);
    c += vec3(1.0, 0.30, 0.06) * fk * 0.10 * exp(-h * 14.0) * uNight;
    return c; }`;

// ---------------------------------------------------------------- vật liệu nhà/công trình
function patchB(mat, depth) {
  mat.onBeforeCompile = (s) => {
    Object.assign(s.uniforms, U);
    s.vertexShader = s.vertexShader.replace('#include <common>', `#include <common>
      attribute vec4 tl; attribute float kk; attribute vec2 uvm; attribute float mt; attribute float fl; uniform float uYear, uHour; attribute float hid; attribute float pid; varying float vHid; varying float vPid; attribute float nid; varying float vNid;
      vec4 lsched(float c){   /* B1 · lịch xây (năm đầu, số năm, đáy, đỉnh phần đang mọc — m trên nền tl.z) theo mã tl.x; Kinh thánh §19 (d) */
        if (abs(c - 1675.5) < 0.05) return vec4(1675.5, 21.5, 0.0, 41.0);    /* St Paul's: thân, hợp xướng, cánh ngang, apse (1675 → hợp xướng mở 1697) */
        if (abs(c - 1697.0) < 0.05) return vec4(1697.0, 8.0, 33.5, 61.8);    /* trống + hàng cột + tầng gác */
        if (abs(c - 1707.0) < 0.05) return vec4(1702.0, 6.0, 0.0, 67.5);     /* mặt tây + hai tháp tây */
        if (abs(c - 1708.5) < 0.05) return vec4(1705.0, 3.0, 61.8, 85.7);    /* vỏ vòm chì — hoàn tất 1708,0 */
        if (abs(c - 1708.8) < 0.05) return vec4(1707.4, 0.6, 85.6, 111.4);   /* Golden Gallery + đèn lồng + quả cầu + thập giá — hoàn tất 1708,0 */
        if (abs(c - 1671.5) < 0.05) return vec4(1671.0, 1.5, 0.0, 13.9);     /* Monument: đế + bệ + rồng */
        if (abs(c - 1672.5) < 0.05) return vec4(1672.5, 3.0, 13.2, 46.5);    /* thân cột có rãnh */
        if (abs(c - 1676.5) < 0.05) return vec4(1675.5, 1.0, 46.4, 58.6);    /* đầu cột, ban công, chóp */
        if (abs(c - 1676.9) < 0.05) return vec4(1676.5, 0.5, 58.5, 61.8);    /* bầu lửa mạ vàng — hoàn tất 1677,0 */
        return vec4(0.0); }
      varying float vAlive; varying float vBurn; varying vec3 vW; varying float vK; varying vec2 vUvm; varying float vMt; varying float vFl; varying float vIgn; varying float vBase; varying float vTx;
      ${burnI}`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>
      float alive = 1.0, grow = 1.0; bool fireMode = uHour >= 0.0; float ign = tl.w;
      if (fireMode && ign >= 0.0) { float a = uHour - ign;
        if (kk < 1.5 || (kk > 7.5 && kk < 8.5) || (kk > 4.5 && kk < 5.5) || (kk > 6.5 && kk < 7.5)) { alive = a < 7.0 ? 1.0 : 0.0; grow = a < 2.5 ? 1.0 : mix(1.0, 0.35, smoothstep(2.5, 7.0, a)); }
        else if (kk > 1.5 && kk < 2.5) { alive = a > 5.0 ? 1.0 : 0.0; } else alive = 0.0;
        if (kk > 4.5 && kk < 5.5 && tl.y > 1667.0) alive = a > 6.0 ? 1.0 : 0.0;
      } else {
        alive = (uYear >= tl.x && uYear < tl.y) ? 1.0 : 0.0;
        float gw = kk > 3.5 && kk < 4.5 ? 2.5 : (kk > 4.5 && kk < 5.5 ? 1.5 : 0.6); grow = clamp((uYear - tl.x) / gw, 0.0, 1.0); grow = grow * grow * (3.0 - 2.0 * grow);
        if (fireMode) { alive = (tl.x < 1666.68 && tl.y > 1666.67) ? 1.0 : 0.0; grow = 1.0; }
      }
      { vec4 S = lsched(tl.x); if (!fireMode && kk > 4.5 && kk < 5.5 && S.y > 0.0) { float g2 = clamp((uYear - S.x) / S.y, 0.0, 1.0);   /* B1: mặt cắt dâng dần */
          alive = (uYear >= S.x + 0.02 * S.y && uYear < tl.y) ? 1.0 : 0.0; transformed.y = tl.z + min(transformed.y - tl.z, S.z + (S.w - S.z) * g2); }
        else transformed.y = tl.z + (transformed.y - tl.z) * max(grow, 0.001); }
      vHid = hid; vPid = pid; vNid = nid; vAlive = alive; vBurn = fireMode ? burnI(ign, uHour) : 0.0; vK = kk; vUvm = uvm; vMt = mt; vFl = fl; vIgn = ign; vBase = tl.z; vTx = tl.x;
      vW = (modelMatrix * vec4(transformed, 1.0)).xyz;`);
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>
      varying float vAlive; varying float vBurn; varying vec3 vW; varying float vK; varying vec2 vUvm; varying float vMt; varying float vFl; varying float vIgn; varying float vBase; varying float vTx; uniform vec2 uDomeC; uniform float uToy;
      varying float vHid; varying float vPid; varying float vNid; uniform float uProjOn, uBong, uD, uD2; uniform sampler2D uProj, tFac, tRoof; uniform mat4 uProjVP; uniform vec4 uFacN; uniform vec3 uFacMean[4];
      vec3 enc24(float id){ float r = floor(id / 65536.0); float g = floor((id - r * 65536.0) / 256.0); float b = id - r * 65536.0 - g * 256.0; return vec3(r, g, b) / 255.0; }
      vec3 l2s(vec3 c){ c = clamp(c, 0.0, 1.0); return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c)); }
      uniform sampler2D uFire, uFire40, uBake; uniform vec4 uFireBox, uBakeBox; uniform float uFireK, uWin, uMask, uBakeOn, uBakeK, uYear, uH40, uWarm, uT, uHour; uniform vec3 uSkyTop, uSkyHor;
      ${GLSL_N} ${VANG} ${HAZE} ${burnI}
      bool flag(float f, float b){ return mod(floor(f / b), 2.0) > 0.5; }
      float boxm(vec2 p, vec2 a, vec2 b){ return step(a.x, p.x) * step(p.x, b.x) * step(a.y, p.y) * step(p.y, b.y); }
      float glassK = 0.0; vec3 emis = vec3(0.0);
      bool roof0(){ return mod(floor(vFl / 4.0), 2.0) > 0.5; }
      float bidB(){ return vNid > 0.5 ? vNid * 1.37 + 0.5 : (vHid > 0.5 ? vHid * 0.731 : dot(floor(vW.xz / 37.0), vec2(1.0, 57.0))); }   /* B1: mã toà để băm */`);
    if (depth) { s.fragmentShader = s.fragmentShader.replace('void main() {', 'void main() { if (vAlive < 0.5) discard;'); return; }
    s.fragmentShader = s.fragmentShader.replace('void main() {', 'void main() { if (vAlive < 0.5) discard;')
      .replace('#include <color_fragment>', `#include <color_fragment>
        { vec3 alb = diffuseColor.rgb; int m = int(vMt + 0.5); bool k4 = vK > 3.5 && vK < 4.5;
          if (m == 7 && k4 && vTx < 1985.0 && !roof0()) { m = 8; alb = vec3(dot(alb, vec3(0.3, 0.59, 0.11))) * vec3(1.32, 1.28, 1.18); }   /* B1: kính rèm chỉ từ 1985 — trước đó văn phòng bê tông */ vec2 p = vUvm; bool roof = flag(vFl, 4.0); bool win = flag(vFl, 8.0); bool front = flag(vFl, 1.0); bool shop = flag(vFl, 2.0);
          vec3 TIMB = vec3(0.075, 0.050, 0.034); vec3 GLS = vec3(0.020, 0.024, 0.030); float rnd = h21(floor(vW.xz * 0.21) + vec2(vMt * 3.1, vK));
          if (roof && m != 15 && m != 16) {
            if (m == 3) { alb = vanC(alb, 3, p, 0.45) * mix(0.85, 1.12, rnd); float hh = h21(floor(vW.xz * 0.16) + 3.7); float soot = fbm3(vW.xz * 0.11 + 5.0);   /* V2: mỗi mái một độ cũ, rêu/ám khói than loang, giảm bão hoà cam đồng đều */
              alb = mix(alb, vec3(dot(alb, vec3(0.3, 0.59, 0.11))), 0.30 * uToy) * mix(1.0, mix(0.62, 1.04, hh) * (0.82 + 0.3 * soot), uToy); alb = mix(alb, vec3(0.20, 0.19, 0.16) * 0.55, 0.22 * smoothstep(0.55, 0.85, soot) * uToy); } else if (m == 4) alb = vanC(alb, 4, p, 0.3); else if (m == 9) alb = vanC(alb, 8, p * 0.75, 0.15);
            else if (m == 12) alb = vanC(alb, 7, p, 0.15) * mix(0.8, 1.05, rnd); else if (m == 10) alb = vanC(alb, 10, p, 0.2) * 0.55; else if (m == 14) alb = vanC(alb, 2, p, 0.4) * 0.6;
            else if (m == 7) { alb = vec3(0.10, 0.12, 0.13); } else alb = vanC(alb, 5, p, 0.25);
          } else if (m == 0 || m == 1) {                                             // nhà khung gỗ trát (1666): khung gỗ + cửa sổ chì + cửa hàng tầng trệt
            float st = 2.8; float lv = floor(p.y / st); float y = p.y - lv * st; float bay = 2.4; float u = fract(p.x / bay) * bay;
            vec3 pl = m == 0 ? vanC(alb, 0, p, 0.25) : vanC(alb, 1, p.yx, 0.5);
            vec3 tim = vanC(TIMB * (0.8 + 0.4 * rnd), 1, p.yx, 0.4);
            float stud = step(fract(p.x / 0.78), 0.16) * (1.0 - step(3.0, abs(p.y - 30.0) * 0.0));
            float rail = step(y, 0.22) + step(st - 0.18, y) + step(abs(y - 1.95), 0.07);
            float brace = step(abs(fract((p.x + y * 0.9) / bay) - 0.5), 0.035) * step(1.95, y) * step(y, st - 0.2) * step(0.5, rnd);
            vec3 c = pl; if (m == 0 && win) c = mix(c, tim, clamp(stud * 0.85 + rail + brace, 0.0, 1.0));
            if (win && lv >= 1.0) { float w = boxm(vec2(u, y), vec2(0.35, 0.85), vec2(bay - 0.35, 1.85)); float lead = step(fract(u / 0.28), 0.09) + step(fract(y / 0.34), 0.11);
              vec3 g = mix(GLS * (0.8 + 0.6 * rnd), vec3(0.05, 0.045, 0.04), clamp(lead, 0.0, 1.0)); c = mix(c, g, w); glassK += w * (1.0 - clamp(lead, 0.0, 1.0)) * 0.15; }
            if (win && lv < 1.0 && shop && front) { float o = boxm(vec2(u, y), vec2(0.25, 0.25), vec2(bay - 0.25, 2.15)); c = mix(c, vec3(0.030, 0.022, 0.016), o);
              float sh = step(2.15, y) * step(y, 2.55); c = mix(c, tim * 0.9, sh); float st2 = boxm(vec2(u, y), vec2(0.25, 0.7), vec2(bay - 0.25, 0.85)); c = mix(c, tim * 1.4, st2); }
            else if (win && lv < 1.0) { float dw = boxm(vec2(fract(p.x / 4.8) * 4.8, y), vec2(1.6, 0.0), vec2(2.6, 2.1)); c = mix(c, tim * 0.7, dw); float w2 = boxm(vec2(u, y), vec2(0.5, 0.9), vec2(1.5, 1.7)); c = mix(c, GLS, w2 * step(0.5, 1.0 - dw)); }
            alb = c * (1.0 - 0.25 * smoothstep(0.0, 1.2, 1.2 - p.y));                // vệt bẩn chân tường
            { float sk = fbm3(vec2(p.x * 0.9 + vMt, p.y * 0.12)); float hh = h21(floor(vW.xz * 0.21) + 1.3); alb *= mix(1.0, (0.80 + 0.22 * hh) * (0.86 + 0.18 * sk), uToy); alb = mix(alb, vec3(dot(alb, vec3(0.3, 0.59, 0.11))), 0.15 * uToy); }   // V2: tường trát mỗi nhà một độ bẩn, vệt chảy dọc
          } else if (m == 2 || m == 11 || m == 14) {                                 // gạch: 1667+ (2), Victoria (11), ống khói (14)
            float st = m == 2 ? 3.0 : 3.6; float bay = m == 2 ? 2.3 : 2.6; float lv = floor(p.y / st); float y = p.y - lv * st; float u = fract(p.x / bay) * bay;
            vec3 c = vanC(alb, m == 11 ? 15 : 2, p, 0.55);
            if (win && m != 14) { vec2 wa = m == 2 ? vec2(0.65, 0.75) : vec2(0.70, 0.70), wb = m == 2 ? vec2(bay - 0.65, 2.45) : vec2(bay - 0.70, 2.80);
              float fr = boxm(vec2(u, y), wa - 0.09, wb + 0.09), w = boxm(vec2(u, y), wa, wb); float bar = (step(abs(u - bay * 0.5), 0.035) + step(abs(y - (wa.y + wb.y) * 0.5), 0.035)) * w;
              c = mix(c, m == 2 ? vec3(0.62, 0.58, 0.52) : vec3(0.70, 0.66, 0.58), fr * (1.0 - w)); c = mix(c, mix(GLS * (0.8 + 0.7 * rnd), vec3(0.6, 0.58, 0.54), bar), w); glassK += w * 0.3;
              if (m == 11 && lv < 1.0 && shop) c = mix(c, vec3(0.03, 0.03, 0.035), boxm(vec2(u, y), vec2(0.2, 0.3), vec2(bay - 0.2, 3.0)));
              if (m == 11) c = mix(c, vec3(0.70, 0.67, 0.60), step(st - 0.25, y)); }
            alb = c * (1.0 - 0.2 * smoothstep(0.0, 1.0, 1.0 - p.y));
          } else if (m == 6 || m == 8) {                                             // đá Portland / văn phòng đá-bê tông
            vec3 c = m == 6 ? vanC(alb, 6, p, 0.25) : vanC(alb, 7, p, 0.2);
            if (win && vK > 3.5 && vK < 4.5 || win && vK > 9.5) { float st = 3.8, bay = m == 8 ? 3.0 : 2.4; float y = mod(p.y, st), u = fract(p.x / bay) * bay;
              float w = m == 8 ? step(0.9, y) * step(y, 3.1) * step(0.08, u) * step(u, bay - 0.08) : boxm(vec2(u, y), vec2(0.6, 0.8), vec2(bay - 0.6, 3.0));
              float gl = 0.85 + 0.2 * h21(floor(vec2(p.x / (bay * 4.0), p.y / st)) + rnd); w = max(w - (m == 8 ? step(abs(u - bay * 0.5), 0.05) : 0.0), 0.0); c = mix(c, GLS * gl * 1.3 + vec3(0.012), w); glassK += w * 0.18; }
            else if (vK > 4.5 && vK < 5.5 || vK > 8.5 && vK < 9.5) { c *= 1.0 - 0.10 * step(fract(p.y / 0.62), 0.06);
              if (vK > 4.5 && vK < 5.5 && m == 6) {   /* B1: đá Portland — vỉa 0,62 m × khối 1,1–1,6 m sáng/tối lệch, vệt chảy dọc, ám khói than theo thời kỳ (sạch dần 1995 → 2011) */
                float row = floor(p.y / 0.62); float blk = floor((p.x + h21(vec2(row, 2.0)) * 1.6) / mix(1.1, 1.6, h21(vec2(row, 4.0))));
                c *= 0.94 + 0.10 * h21(vec2(blk, row)); c *= 1.0 - 0.08 * step(fract((p.x + h21(vec2(row, 2.0)) * 1.6) / mix(1.1, 1.6, h21(vec2(row, 4.0)))), 0.03);
                float era = smoothstep(1720.0, 1860.0, uYear) * (1.0 - smoothstep(1995.0, 2011.0, uYear)); float sk = fbm3(vec2(p.x * 0.35, p.y * 0.05) + vTx);
                float drip = smoothstep(0.55, 0.85, fbm3(vec2(p.x * 2.2 + vTx * 3.0, p.y * 0.08)));
                c = mix(c, c * vec3(0.34, 0.33, 0.31), era * clamp(0.25 + 0.65 * smoothstep(0.45, 0.75, sk) + 0.35 * drip, 0.0, 0.85));
                c = mix(c, c * vec3(0.93, 0.90, 0.84), 0.6 * drip * (1.0 - era));   /* sau làm sạch: vệt chảy nhạt, ngả kem */
                vec2 mo = vW.xz - vec2(923.0, 39.0); if (abs(vTx - 1672.5) < 0.05 && length(mo) < 3.0) { float an = atan(mo.y, mo.x);   /* thân Monument: 20 rãnh dọc */
                  float fl20 = abs(cos(an * 10.0)); c *= mix(0.62, 1.08, smoothstep(0.15, 0.95, fl20)); } } }
            alb = c;
          } else if (m == 7) {                                                       // tường kính rèm (2026): khung + kính phản trời
            float bh = bidB(); float b1 = h21(vec2(bh, 1.7)), b2 = h21(vec2(bh, 5.3)), b3 = h21(vec2(bh, 9.1));   /* B1: mỗi toà một loại kính rèm */
            float st = mix(3.6, 4.3, b1), bay = b2 < 0.33 ? 1.2 : (b2 < 0.75 ? 1.5 : 3.0); float y = mod(p.y, st), u = mod(p.x, bay); vec2 cell = floor(vec2(p.x / bay, p.y / st));
            float mw = b3 < 0.3 ? 0.16 : 0.07; float mull = step(u, mw) + step(st - 0.10, y) + step(y, 0.05); float spand = b3 > 0.55 ? step(st - mix(0.6, 1.1, b1), y) : 0.0;
            vec3 tint = b1 < 0.3 ? vec3(0.62, 0.74, 0.80) : (b1 < 0.55 ? vec3(0.66, 0.76, 0.70) : (b1 < 0.8 ? vec3(0.78, 0.80, 0.82) : vec3(0.74, 0.66, 0.56)));
            vec3 frm = b2 < 0.5 ? vec3(0.30, 0.32, 0.34) : (b3 < 0.5 ? vec3(0.62, 0.62, 0.60) : vec3(0.12, 0.13, 0.14));
            alb = mix(alb * tint * 1.25 * (0.62 + 0.12 * h21(floor(cell / vec2(6.0, 3.0)) + rnd)), frm, clamp(mull, 0.0, 1.0)); alb = mix(alb, alb * 0.6, spand * 0.6);
            glassK = (1.0 - clamp(mull + spand, 0.0, 1.0)) * (0.6 + 0.12 * h21(floor(cell / vec2(6.0, 3.0)) * 1.7));
          } else if (m == 5) { alb = vanC(alb, 5, p, 0.3); alb *= 1.0 - 0.18 * smoothstep(0.0, 2.0, 2.0 - p.y); }
          else if (m == 10) { alb = vanC(alb, 5, p, 0.2) * mix(vec3(0.42), vec3(0.75), smoothstep(0.0, 4.0, p.y)) ; }
          else if (m == 9) { alb = vanC(alb, 8, p, 0.15); vec2 dc = vW.xz - uDomeC; float rr = length(dc);
            if (vK > 4.5 && vK < 5.5) { alb = vanC(vec3(0.255, 0.262, 0.262), 8, p, 0.10) * (0.92 + 0.12 * fbm3(p * vec2(0.6, 0.15)));   /* B1: chì phong hoá xám sáng (không đen) */
              float era = smoothstep(1720.0, 1860.0, uYear) * (1.0 - smoothstep(1995.0, 2011.0, uYear)); alb *= mix(1.0, 0.72, era);
              alb *= 1.0 - 0.10 * step(fract(p.y / 1.9), 0.05);   /* mạch ghép tấm chì ngang */
              alb = mix(alb, vec3(0.40, 0.42, 0.41), 0.25 * smoothstep(0.6, 0.9, fbm3(vec2(p.x * 1.3, p.y * 0.07))));   /* vệt ô-xít trắng chảy dọc */
              glassK = 0.07; }
            if (vK > 4.5 && vK < 5.5 && rr < 17.0 && rr > 2.0) { float an = atan(dc.y, dc.x); float rib = smoothstep(0.90, 0.985, abs(cos(an * 12.0))); alb = mix(alb, alb * 1.45 + 0.02, rib * 0.85); } }   // V2: 24 gân vòm chì
          else if (m == 15) { vec2 dc = vW.xz - vec2(1301.0, -452.0); float an = atan(dc.y, dc.x); float band = smoothstep(0.30, 0.36, fract(an / 6.2832 * 6.0 + vW.y / 170.0)) * (1.0 - smoothstep(0.62, 0.68, fract(an / 6.2832 * 6.0 + vW.y / 170.0)));   // V2: 30 St Mary Axe — dải kính tối xoắn + lưới kim cương
            float d1 = fract((p.x + p.y * 0.95) / 8.6), d2 = fract((p.x - p.y * 0.95) / 8.6); float ln = clamp(step(d1, 0.06) + step(d2, 0.06), 0.0, 1.0);
            alb = mix(mix(vec3(0.16, 0.21, 0.24), vec3(0.06, 0.08, 0.10), band), vec3(0.62, 0.64, 0.64), ln); glassK = (1.0 - ln) * 0.55; }
          else if (m == 16) { float st = 28.0; float d1 = fract((p.x + p.y) / st), d2 = fract((p.x - p.y) / st); float ln = clamp(step(abs(d1 - 0.5), 0.022) + step(abs(d2 - 0.5), 0.022) + step(fract(p.y / st), 0.03) + step(fract(p.x / 14.0), 0.025), 0.0, 1.0);   // V2: Leadenhall — khung giằng chéo lộ
            float mull = step(fract(p.x / 1.5), 0.06) + step(fract(p.y / 3.9), 0.04); alb = mix(vec3(0.20, 0.23, 0.25), vec3(0.30, 0.31, 0.32), clamp(mull, 0.0, 1.0)); alb = mix(alb, vec3(0.66, 0.66, 0.62), ln); glassK = (1.0 - clamp(ln + mull, 0.0, 1.0)) * 0.6; }
          else if (m == 13) { alb = GLS * 1.4; glassK = 0.5; }
          if (vK > 1.5 && vK < 2.5) alb *= 0.38 + 0.15 * vn(vW.xz * 0.4);   // phế tích: than, tro, gạch ám (Evelyn 7/9: "the ground under my feet so hot")
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
            if (!roof && era >= 0.0 && !(era < 0.5 && m == 2) && !(era > 1.5 && m == 11) && m != 14 && m != 7 && m != 13) { float off = h21(vec2(vHid * 0.013, 9.1)) * uFacN.z; vec2 fu = 0.01 + 0.98 * vec2(fract((p.x + off) / uFacN.z), fract(max(p.y, 0.0) / uFacN.w));
              float cl = mod(tix, 4.0), rw = era * 2.0 + floor(tix / 4.0); vec3 fc = texture2D(tFac, vec2((cl + fu.x) / uFacN.x, (rw + 1.0 - fu.y) / uFacN.y)).rgb; int ri = int(era);
              vec3 fm = ri == 0 ? uFacMean[0] : ri == 1 ? uFacMean[1] : uFacMean[2]; alb = mix(alb, fc / max(fm, vec3(0.02)) * dot(alb, vec3(0.333)), 0.92); glassK *= 0.35; }
            else if (roof) { float rr = (m == 3) ? 0.0 : (m == 4) ? 1.0 : 2.0; vec2 ru = 0.01 + 0.98 * fract((p + vec2(h21(vec2(vHid, 2.0)), h21(vec2(vHid, 4.0))) * 8.0) / vec2(8.0, 13.5));
              vec3 rc = texture2D(tRoof, vec2((rr + ru.x) / 3.0, ru.y)).rgb; alb = mix(alb, rc / max(uFacMean[3], vec3(0.02)) * dot(alb, vec3(0.333)), 0.85); } }
          if (uProjOn > 0.5 && nt) { vec4 cp = uProjVP * vec4(vW, 1.0); vec2 q = cp.xy / cp.w * 0.5 + 0.5;   /* THU-B B (ii): ảnh AI đã khử sáng chiếu lên hình học */
            if (cp.w > 0.0 && q.x > 0.0 && q.y > 0.0 && q.x < 1.0 && q.y < 1.0) { vec4 pr = texture2D(uProj, q); if (pr.a > 0.5) { alb = pr.rgb; glassK = 0.0; } } }
          if (uBong > 0.5) { alb = vec3(0.6); glassK = 0.0; }
          diffuseColor.rgb = alb; }`)
      .replace('#include <lights_fragment_end>', `#include <lights_fragment_end>
        { vec2 bu = (vec2(vW.x, -vW.z) - uBakeBox.xy) / (uBakeBox.zw - uBakeBox.xy);
          float h = vW.y - vBase; float sky = 1.0;
          if (uBakeOn > 0.5 && bu.x > 0.0 && bu.y > 0.0 && bu.x < 1.0 && bu.y < 1.0) { vec4 bk = texture2D(uBake, bu + normal.xz * 0.0); float ground = bk.r;
            sky = mix(ground, 1.0, smoothstep(0.0, 18.0, h) * 0.75 + (flag(vFl, 4.0) ? 0.35 : 0.0)); }
          else sky = mix(0.55, 1.0, smoothstep(0.0, 12.0, h));
          reflectedLight.indirectDiffuse *= mix(1.0, sky, uBakeK); }`)
      .replace('#include <dithering_fragment>', `#include <dithering_fragment>
        vec3 Vd = normalize(vW - uCam); vec3 Nw = normalize(cross(dFdx(vW), dFdy(vW))); if (dot(Nw, Vd) > 0.0) Nw = -Nw;
        if (glassK > 0.01) { vec3 Rf = reflect(Vd, Nw); float ry0 = Rf.y; if (uD > 0.5) { vec2 cl = floor(vUvm / vec2(1.5, 3.9)); Rf = normalize(Rf + vec3(h21(cl) - 0.5, 0.0, h21(cl + 3.3) - 0.5) * 0.06); ry0 = Rf.y; } Rf.y = abs(Rf.y) * 0.7 + 0.02; float fr = 0.06 + 0.94 * pow(1.0 - max(dot(Nw, -Vd), 0.0), 5.0);
          vec3 env = mix(uSkyHor, uSkyTop, pow(clamp(Rf.y, 0.0, 1.0), 0.5)) * (1.0 - 0.85 * uNight); env = mix(env, vec3(dot(env, vec3(0.3, 0.59, 0.11))), 0.45) * 0.8 + uSunCol * pow(max(dot(Rf, uSunDir), 0.0), 220.0) * 4.0 * (1.0 - uNight);
          if (uD > 0.5) { float bnd = smoothstep(-0.02, 0.10, ry0 + 0.05 * (vn(vW.xz * 0.05 + vW.y * 0.02) - 0.5)); vec3 city = mix(vec3(0.075, 0.072, 0.068), vec3(0.16, 0.15, 0.14), vn(vec2(atan(Rf.x, Rf.z) * 40.0, 1.0))) * (1.0 - 0.85 * uNight);
          env = mix(city, env, bnd); }
          gl_FragColor.rgb = mix(gl_FragColor.rgb, env, clamp(glassK * mix(0.35, 0.95, fr), 0.0, 1.0)); }
        vec2 fu = (vW.xz - uFireBox.xy) / uFireBox.zw; vec3 fg = uHour >= 0.0 ? texture2D(uFire, fu).rgb : texture2D(uFire40, fu).rgb;
        float hfall = exp(-max(vW.y - 5.0, 0.0) / 70.0); vec3 fireCol = vec3(1.0, 0.42, 0.12); vec3 alb = diffuseColor.rgb;
        gl_FragColor.rgb += alb * fireCol * uFireK * (fg.r * 2.4 * hfall + fg.g * 0.85 + fg.b * 0.14);   // V2: ánh lửa trên mặt tiền xa hơn
        float vb = vBurn; if (uH40 >= 0.0) { vec2 c40 = (vW.xz - uFireBox.xy) / uFireBox.zw; vb = fg.r * 1.6 * step(vK, 4.5) + fg.r * 1.2 * step(9.5, vK); }
        if (vb > 0.01) { float flk = fbm(vec2(vW.x * 0.35 + uT * 1.7, vW.y * 0.6 - uT * 3.1));
          gl_FragColor.rgb = mix(gl_FragColor.rgb, gl_FragColor.rgb * 0.15, clamp(vb * 1.6, 0.0, 0.9)); float hot = smoothstep(0.50, 0.80, flk) * (0.35 + 0.65 * step(0.25, glassK + 0.2 * h21(floor(vUvm * 0.7))));   // lửa theo mảng (ô cửa, khe mái), không phủ đều mặt tường
          gl_FragColor.rgb += vec3(1.0, 0.30, 0.05) * vb * (0.10 + 1.5 * hot) * 1.4 * (0.45 + 0.55 * uNight); }
        if (uWin > 0.0 && glassK > 0.1 && (vK > 3.5 && vK < 4.5)) {   /* B1: cửa sổ đêm theo toà + tầng (thay lưới ô ngẫu nhiên đều 58 %) */
          float bh = bidB(); float occ = mix(0.12, 0.78, h21(vec2(bh, 11.3))); float fy = floor(vUvm.y / 3.9); float fx = floor(vUvm.x / 12.0);
          float flo = step(h21(vec2(bh * 0.71 + fx * 0.13, fy)), occ * 1.15); vec2 cl = floor(vUvm / vec2(1.5, 3.9));
          float on = flo * step(0.28, h21(cl + bh)) + (1.0 - flo) * step(0.93, h21(cl * 1.7 + bh));
          vec3 wc = mix(vec3(1.0, 0.78, 0.50), vec3(0.86, 0.92, 1.0), step(0.55, h21(vec2(bh, 3.3)))) * (0.55 + 0.6 * h21(cl * 0.37 + bh * 0.11));
          float dk = smoothstep(4500.0, 900.0, length(vW - uCam)) * 0.6 + 0.4;   /* xa: bớt nhấp nháy ô nhỏ */
          gl_FragColor.rgb += wc * on * uWin * 1.05 * glassK * dk + wc * 0.035 * uWin * glassK * flo; }
        if (vK > 4.5 && vK < 5.5 && uNight > 0.02 && uYear > 1951.0 && uHour < 0.0 && uH40 < 0.0) {   /* B1: đèn pha mái vòm St Paul's + Monument (đêm, từ 1951) */
          vec2 dc = vW.xz - uDomeC; vec2 mo = vW.xz - vec2(923.0, 39.0); float sp = step(length(dc), 120.0), mn = step(length(mo), 8.0); float hh = vW.y - vBase;
          float fk = sp * (0.55 + 0.55 * smoothstep(30.0, 70.0, hh) * (1.0 - 0.45 * smoothstep(88.0, 112.0, hh))) + mn * 0.75;
          gl_FragColor.rgb += diffuseColor.rgb * vec3(1.0, 0.86, 0.66) * fk * 1.25 * uNight * (0.85 + 0.15 * vn(vW.xz * 0.3 + vW.y * 0.2)); }
        gl_FragColor.rgb = hazeApply(gl_FragColor.rgb, vW);
        if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(235.0) / 255.0, 1.0);   /* V2: màu mặt nạ ghi THẲNG (đầu ra sau colorspace_fragment, không mã hoá lại) */
        if (uMask > 1.5 && uMask < 2.5) { float id = 0.0; const float C[12] = float[12](1675.5, 1697.0, 1707.0, 1708.5, 1708.8, 1671.5, 1672.5, 1676.5, 1676.9, 1100.0, 1100.5, 1300.0);   /* mã công trình → chỉ số 1–12 (màu cách nhau 20 mức R) */
          for (int i = 0; i < 12; i++) if (abs(vTx - C[i]) < 0.05) id = float(i + 1);
          gl_FragColor = (vK > 4.5 && vK < 5.5 && id > 0.5) ? vec4(vec3(id * 20.0, 0.0, 200.0) / 255.0, 1.0) : vec4(0.0, 0.0, 0.0, 1.0); }
        if (uMask > 0.5 && uMask < 1.5 && vHid > 0.5) gl_FragColor = vec4(vec3(215.0) / 255.0, 1.0);   /* THU-B: lớp nha_thuong (K-1.17.5) */
        if (uMask > 2.5 && uMask < 3.5) gl_FragColor = vec4(vHid > 0.5 ? enc24(floor(vHid + 0.5)) : vec3(0.0), 1.0);   /* làm tròn: nội suy varying lệch ε dưới số nguyên */
        if (uMask > 3.5 && uMask < 4.5) gl_FragColor = vec4(vHid > 0.5 ? enc24(floor(vPid + 0.5)) : vec3(0.0), 1.0);
        if (uMask > 5.5) gl_FragColor = vec4(l2s(diffuseColor.rgb), 1.0);`);
  };
  mat.customProgramCacheKey = () => (depth ? 'lk-d' : 'lk-c');
}

// ---------------------------------------------------------------- mảng vân
async function decode(url, w) { const b = await (await fetch(url)).blob(), im = await createImageBitmap(b, { colorSpaceConversion: 'none' });
  const cv = new OffscreenCanvas(w, w), g = cv.getContext('2d'); g.drawImage(im, 0, 0, w, w); return g.getImageData(0, 0, w, w).data; }
async function texArray(base) {
  const S = 1024, n = VAN.length, data = new Uint8Array(S * S * 4 * n), mean = [];
  const px = await Promise.all(VAN.map(([id]) => decode(`${base}tex/${id}_diff_1k.jpg`, S)));
  px.forEach((p, i) => { data.set(p, i * S * S * 4); const a = [0, 0, 0]; for (let k = 0; k < p.length; k += 64) for (let c = 0; c < 3; c++) a[c] += Math.pow(p[k + c] / 255, 2.2); mean.push(V3(...a.map((v) => v / (p.length / 64)))); });
  const t = new THREE.DataArrayTexture(data, S, S, n); t.format = THREE.RGBAFormat; t.type = THREE.UnsignedByteType; t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.generateMipmaps = true; t.anisotropy = 1; t.colorSpace = THREE.SRGBColorSpace; t.needsUpdate = true;
  U.tVanD.value = t; U.uVanMean.value = mean; U.uVanS.value = VAN.map((v) => v[1]);
}

// ---------------------------------------------------------------- dựng cảnh
async function build(cfg) {
  const base = cfg.data;
  META = await (await fetch(base + LK + 'ldn2.json')).json(); if (META.st_pauls_EN) U.uDomeC.value.set(META.st_pauls_EN[0] - 532000, -(META.st_pauls_EN[1] - 180800));
  const buf = await (await fetch(base + LK + 'ldn2.bin')).arrayBuffer();
  const A = (nm, T) => { const l = META.bo_cuc[nm]; return new T(buf, l.off, l.len / T.BYTES_PER_ELEMENT); };
  await texArray(base);
  const pos = A('pos', Float32Array), col = A('col', Uint8Array), tl = A('tl', Float32Array), kk = A('k', Uint8Array), uvm = A('uv', Float32Array), mt = A('mt', Uint8Array), fl = A('fl', Uint8Array);
  const g = new THREE.BufferGeometry(); const LUT8 = new Float32Array(256).map((_, i) => Math.pow(i / 255, 2.2)); const colL = new Float32Array(col.length); for (let i = 0; i < col.length; i++) colL[i] = LUT8[col[i]];
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(colL, 3)); g.setAttribute('tl', new THREE.BufferAttribute(tl, 4));
  g.setAttribute('kk', new THREE.BufferAttribute(new Float32Array(kk), 1)); g.setAttribute('uvm', new THREE.BufferAttribute(uvm, 2)); g.setAttribute('mt', new THREE.BufferAttribute(new Float32Array(mt), 1)); g.setAttribute('fl', new THREE.BufferAttribute(new Float32Array(fl), 1));
  { const nv = pos.length / 3; const ld32 = async (nm) => { try { const r = await fetch(base + LK + nm); if (!r.ok) return new Float32Array(nv); const a = new Float32Array(await r.arrayBuffer()); return a.length === nv ? a : new Float32Array(nv); } catch (e) { return new Float32Array(nv); } };
    g.setAttribute('hid', new THREE.BufferAttribute(await ld32('hid.f32'), 1)); g.setAttribute('pid', new THREE.BufferAttribute(await ld32('pid.f32'), 1));
    g.setAttribute('nid', new THREE.BufferAttribute(await ld32('nid.f32'), 1)); }   /* B1: mã toà OSM có tên (0 = khác) */
  g.computeVertexNormals();
  const m = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }); patchB(m, false);
  // chia ô 300 m (gom tam giác theo tâm) → loại theo khung nhìn cho máy chính, gương và bản đồ bóng (llvmpipe nghẽn ở số đỉnh, không ở điểm ảnh)
  const dm = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, side: THREE.DoubleSide }); patchB(dm, true);
  BLD = new THREE.Group(); { const TILE = 300, P_ = g.attributes.position.array, nT = P_.length / 9, key = new Int32Array(nT), cnt = new Map();
    for (let t = 0; t < nT; t++) { const cx = (P_[t * 9] + P_[t * 9 + 3] + P_[t * 9 + 6]) / 3, cz = (P_[t * 9 + 2] + P_[t * 9 + 5] + P_[t * 9 + 8]) / 3; const k = (Math.floor(cx / TILE) + 100) * 1000 + Math.floor(cz / TILE) + 100; key[t] = k; cnt.set(k, (cnt.get(k) || 0) + 1); }
    const names = Object.keys(g.attributes), tiles = new Map();
    for (const [k, c] of cnt) { const at = {}; for (const nm of names) { const A0 = g.attributes[nm]; at[nm] = new A0.array.constructor(c * 3 * A0.itemSize); } tiles.set(k, { at, n: 0 }); }
    for (let t = 0; t < nT; t++) { const T_ = tiles.get(key[t]); for (const nm of names) { const A0 = g.attributes[nm], sz = A0.itemSize * 3; T_.at[nm].set(A0.array.subarray(t * sz, t * sz + sz), T_.n * sz); } T_.n++; }
    for (const [k, T_] of tiles) { const gg = new THREE.BufferGeometry(); for (const nm of names) gg.setAttribute(nm, new THREE.BufferAttribute(T_.at[nm], g.attributes[nm].itemSize)); gg.computeBoundingSphere();
      const ms = new THREE.Mesh(gg, m); ms.castShadow = ms.receiveShadow = true; ms.customDepthMaterial = dm; BLD.add(ms); } }
  g.dispose(); scene.add(BLD);
  // ---- địa hình + lớp phủ mặt đất
  const T = META.dia_hinh, nx = T.nx, nz = T.nz; const h26 = A('h26', Float32Array), h66 = A('h66', Float32Array);
  const tg = new THREE.PlaneGeometry(1, 1, nx - 1, nz - 1); const tp = tg.attributes.position.array, H2 = new Float32Array(nx * nz), H6 = new Float32Array(nx * nz);
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const v = j * nx + i; tp[v * 3] = T.x0 + i * T.step; tp[v * 3 + 1] = 0; tp[v * 3 + 2] = T.z0 + j * T.step; H2[v] = h26[v]; H6[v] = h66[v]; }
  tg.setAttribute('h2', new THREE.BufferAttribute(H2, 1)); tg.setAttribute('h6', new THREE.BufferAttribute(H6, 1));
  const TL = new THREE.TextureLoader(); const ld = (u, nearest) => new Promise((r) => TL.load(u, (t) => { t.colorSpace = THREE.NoColorSpace; t.minFilter = t.magFilter = nearest ? THREE.NearestFilter : THREE.LinearFilter; t.generateMipmaps = false; t.flipY = false; r(t); }, undefined, () => r(null)));
  const C66 = await ld(base + LK + 'cls66.png', true), C26 = await ld(base + LK + 'cls26.png', true); const LD = META.lop_dat;
  const tm = new THREE.MeshLambertMaterial({ color: 0xffffff });
  tm.onBeforeCompile = (s) => { Object.assign(s.uniforms, U, { tC66: { value: C66 }, tC26: { value: C26 }, uLD: { value: new THREE.Vector4(LD.E0, LD.N1, LD.w * LD.buoc, LD.h * LD.buoc) } });
    s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nattribute float h2, h6; uniform float uYear; varying vec3 vW; varying float vWet;')
      .replace('#include <begin_vertex>', `#include <begin_vertex>
        float k = smoothstep(1864.0, 1870.5, uYear); transformed.y = mix(h6, h2, k); vWet = smoothstep(1.2, -0.8, transformed.y); vW = (modelMatrix * vec4(transformed, 1.0)).xyz;`);
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>
      uniform float uBong, uD; varying vec3 vW; varying float vWet; uniform sampler2D uFire, uFire40, uBake, tC66, tC26; uniform vec4 uFireBox, uBakeBox, uLD; uniform float uFireK, uYear, uMask, uBakeOn, uBakeK, uHour, uH40, uDbg; ${GLSL_N} ${VANG} ${HAZE}`)
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', `vec2 en = vec2(vW.x + 532000.0, -vW.z + 180800.0); vec2 cu = vec2((en.x - uLD.x) / uLD.z, (uLD.y - en.y) / uLD.w);
        float c66 = floor(texture2D(tC66, cu).r * 255.0 + 0.5), c26 = floor(texture2D(tC26, cu).r * 255.0 + 0.5); bool modern = uYear > 1850.0; float cl = modern ? c26 : c66;
        vec2 p = vW.xz; float n = fbm3(p * 0.05); vec3 cc;
        if (cl < 0.5) cc = modern ? vanC(vec3(0.42, 0.41, 0.39), 12, p, 0.2) : vanC(mix(vec3(0.33, 0.28, 0.22), vec3(0.40, 0.35, 0.28), n), 10, p, 0.35);
        else if (cl < 1.5) cc = (modern && uYear > 1920.0) ? vanC(vec3(0.20, 0.20, 0.21), 11, p, 0.15) : vanC(mix(vec3(0.36, 0.32, 0.27), vec3(0.30, 0.27, 0.23), n), 9, p, 0.3);
        else if (cl < 2.5) cc = vanC(vec3(0.46, 0.45, 0.43), 12, p, 0.2);
        else if (cl < 3.5) cc = vanC(mix(vec3(0.16, 0.22, 0.10), vec3(0.22, 0.27, 0.12), n), 13, p, 0.45);
        else if (cl < 4.5) cc = vanC(vec3(0.24, 0.21, 0.17), 10, p, 0.3);
        else if (cl < 5.5) { float pl = step(0.55, vn(p * vec2(0.05, 0.3))); cc = mix(vanC(vec3(0.30, 0.27, 0.23), 9, p, 0.3), vanC(vec3(0.26, 0.20, 0.15), 14, p.yx, 0.4), pl * 0.6); }   // bến: sỏi + ván
        else cc = vanC(vec3(0.16, 0.14, 0.11), 10, p, 0.2);
        cc = mix(cc, vec3(0.13, 0.115, 0.095), vWet * 0.85); if (uD > 0.5) cc *= 0.80 + 0.28 * fbm3(p * 0.31 + 3.3); if (uBong > 0.5) cc = vec3(0.6);
        vec4 diffuseColor = vec4(cc, 1.0);`)
      .replace('#include <lights_fragment_end>', `#include <lights_fragment_end>
        { vec2 bu = (en - uBakeBox.xy) / (uBakeBox.zw - uBakeBox.xy); if (uBakeOn > 0.5 && bu.x > 0.0 && bu.y > 0.0 && bu.x < 1.0 && bu.y < 1.0) { float sk = texture2D(uBake, bu).r;
          reflectedLight.indirectDiffuse *= mix(1.0, sk, uBakeK); reflectedLight.directDiffuse *= mix(1.0, smoothstep(0.05, 0.6, sk) * 0.4 + 0.6, uBakeK * 0.5);
          if (uD > 0.5) { reflectedLight.directDiffuse *= smoothstep(0.15, 0.75, sk) * 0.35 + 0.65; reflectedLight.indirectDiffuse *= mix(1.0, sk, 0.5); } } }`)
      .replace('#include <dithering_fragment>', `#include <dithering_fragment>
        vec2 fu = (vW.xz - uFireBox.xy) / uFireBox.zw; vec3 fg = uHour >= 0.0 ? texture2D(uFire, fu).rgb : texture2D(uFire40, fu).rgb;
        if (uHour >= 0.0) { float ash = texture2D(uFire, fu).a; gl_FragColor.rgb *= mix(1.0, 0.20 + 0.10 * vn(vW.xz * 0.3), clamp(ash, 0.0, 1.0)); }
        if (uDbg > 0.5) gl_FragColor = vec4(texture2D(uFire, fu).a, texture2D(uFire, fu).r, uHour >= 0.0 ? 1.0 : 0.0, 1.0);   // tro + than sau cháy
        gl_FragColor.rgb += diffuseColor.rgb * vec3(1.0, 0.42, 0.12) * uFireK * (fg.r * 2.0 + fg.g * 0.6 + fg.b * 0.08);
        gl_FragColor.rgb = hazeApply(gl_FragColor.rgb, vW); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(200.0, 170.0, 90.0) / 255.0, 1.0);`); };
  TER = new THREE.Mesh(tg, tm); TER.receiveShadow = true; TER.frustumCulled = false; scene.add(TER);
  // ---- mặt nước Thames: sóng nhiều hướng + Fresnel + phản chiếu phẳng (vật trên nước) + màu nước sông (không mảng xanh nhạt — LOOK-4 T3)
  const TW = (T.nx - 1) * T.step, TD = (T.nz - 1) * T.step;
  const wm = new THREE.ShaderMaterial({ uniforms: U, vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `varying vec3 vW; uniform float uMask, uReflOn; uniform vec3 uWater; uniform sampler2D uFire, uFire40, uRefl; uniform vec4 uFireBox; uniform mat4 uReflVP; ${GLSL_N} ${HAZE} ${SKYF}
      vec2 wv(vec2 p, vec2 d, float l, float sp){ float k = 6.2832 / l; float ph = dot(p, d) * k + uT * sp; return d * cos(ph) * k; }
      void main(){ vec3 V = normalize(uCam - vW); float dist = length(uCam - vW); float a = smoothstep(5000.0, 150.0, dist);
        vec2 p = vW.xz; mat2 rot = mat2(0.8, -0.6, 0.6, 0.8); vec2 q1 = rot * p * vec2(0.055, 0.11), q2 = rot * rot * p * vec2(0.19, 0.31);
        vec2 gr = vec2(fbm3(q1 + vec2(uT * 0.05, 0.0)) - fbm3(q1 + vec2(0.37, uT * 0.04)), fbm3(q1 * 1.3 - uT * 0.06) - fbm3(q1 * 1.3 + 3.1)) * 0.22
          + vec2(vn(q2 + uT * 0.25) - vn(q2 + 1.7), vn(q2 * 1.2 - 2.3) - vn(q2 * 1.2 + uT * 0.2)) * 0.08 * smoothstep(1500.0, 200.0, dist);
        vec3 N = normalize(vec3(-gr.x * a, 1.0, -gr.y * a)); vec3 Rr = reflect(-V, N); Rr.y = abs(Rr.y);
        float F = 0.02 + 0.6 * pow(1.0 - max(dot(N, V), 0.0), 5.0); vec3 env = skyCol(Rr) * 0.85;
        if (uReflOn > 0.5) { vec4 cp = uReflVP * vec4(vW + vec3(N.x, 0.0, N.z) * 10.0 * min(dist / 150.0, 6.0), 1.0); vec2 ruv = cp.xy / cp.w * 0.5 + 0.5;
          if (ruv.x > 0.0 && ruv.x < 1.0 && ruv.y > 0.0 && ruv.y < 1.0) { vec4 rc = texture2D(uRefl, ruv); float ra = clamp(rc.a, 0.0, 1.0); env = mix(env, rc.rgb, ra * 0.80) + rc.rgb * (1.0 - ra) * 0.85; } }   /* B1: giữ phần phát sáng cộng (lửa) */
        vec3 deep = uWater * (1.0 - 0.85 * uNight) * (0.9 + 0.2 * fbm3(p * 0.02));
        float Fq = min(0.6, F * (1.0 + 1.6 * uNight * max(step(0.0, uHour), step(0.0, uH40))));   /* B1: đêm cháy 1666 + 1940 — vệt phản chiếu lửa đọc được (lửa là nguồn rất sáng) */
        vec3 c = mix(deep, env * vec3(0.92, 0.92, 0.86), Fq);
        c += uSunCol * pow(max(dot(Rr, uSunDir), 0.0), 500.0) * 4.0 * (0.4 + 0.6 * a) * (1.0 - uNight);
        vec2 fu = (vW.xz + vec2(0.0, -110.0) - uFireBox.xy) / uFireBox.zw; vec3 fg = (uHour >= 0.0 ? texture2D(uFire, fu + N.xz * 0.03).rgb : texture2D(uFire40, fu + N.xz * 0.03).rgb);
        float wl = 0.45 + 0.9 * fbm3(rot * p * vec2(0.09, 0.03) + vec2(uT * 0.08, 0.0));   /* B1: ánh lửa trên mặt sông theo sóng, không phủ phẳng */
        c += vec3(1.0, 0.45, 0.15) * uFireK * (fg.g * 0.075 + fg.b * 0.022) * (0.12 + 1.6 * F) * wl;
        c = hazeApply(c, vW); gl_FragColor = vec4(c, 1.0); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(0.0, 170.0, 190.0) / 255.0, 1.0); }` });
  WATER = new THREE.Mesh(new THREE.PlaneGeometry(TW, TD).rotateX(-Math.PI / 2), wm); WATER.position.set(T.x0 + TW / 2, 0.6, T.z0 + TD / 2); scene.add(WATER);
  // ---- đất xa ngoài hộp + trời
  const fm = new THREE.MeshLambertMaterial({ color: new THREE.Color(0.20, 0.19, 0.16) });
  fm.onBeforeCompile = (s) => { Object.assign(s.uniforms, U); s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWf;').replace('#include <begin_vertex>', '#include <begin_vertex>\n vWf = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>\nvarying vec3 vWf; uniform float uYear, uMask; ${GLSL_N} ${HAZE}`)
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', `float n1 = fbm3(vWf.xz * 0.004), n2 = vn(vWf.xz * 0.02); vec3 fld = mix(vec3(0.17, 0.20, 0.09), vec3(0.24, 0.23, 0.12), n1) * (0.85 + 0.3 * step(0.5, n2));
        vec3 urb = mix(vec3(0.20, 0.19, 0.18), vec3(0.26, 0.24, 0.22), n1); float k = smoothstep(1750.0, 1900.0, uYear) * smoothstep(0.2, 0.6, n1 + 0.25 * smoothstep(1900.0, 1950.0, uYear));
        vec4 diffuseColor = vec4(mix(fld, urb, k), 1.0);`)
      .replace('#include <dithering_fragment>', '#include <dithering_fragment>\n gl_FragColor.rgb = hazeApply(gl_FragColor.rgb, vWf); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(150.0, 120.0, 70.0) / 255.0, 1.0);'); };   /* V2: đất xa ngoài hộp = "suon" trong mặt nạ */
  const sh = new THREE.Shape([new THREE.Vector2(-40000, -40000), new THREE.Vector2(40000, -40000), new THREE.Vector2(40000, 40000), new THREE.Vector2(-40000, 40000)]); const m5 = 5;
  sh.holes.push(new THREE.Path([new THREE.Vector2(T.x0 + m5, -(T.z0 + m5)), new THREE.Vector2(T.x0 + m5, -(T.z0 + TD - m5)), new THREE.Vector2(T.x0 + TW - m5, -(T.z0 + TD - m5)), new THREE.Vector2(T.x0 + TW - m5, -(T.z0 + m5))]));
  const fg = new THREE.PlaneGeometry(60000, 60000, 240, 240).rotateX(-Math.PI / 2); { const p = fg.attributes.position; const ss2 = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
    for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i); const inside = x > T.x0 + 40 && x < T.x0 + TW - 40 && z > T.z0 + 40 && z < T.z0 + TD - 40;
      const n = 0.6 + 0.4 * Math.sin(x * 0.0007 + 1.3) * Math.cos(z * 0.0009 - 0.4); const h = 9 + 95 * ss2(3500, 9000, -z) * n + 70 * ss2(4500, 10000, z) * (0.7 + 0.3 * Math.sin(x * 0.0005)) + 25 * ss2(6000, 14000, Math.abs(x)) * n;
      p.setY(i, inside ? -60 : h); } fg.computeVertexNormals(); }
  const FAR = new THREE.Mesh(fg, fm); FAR.receiveShadow = false; scene.add(FAR);
  // dãy nhà xa (thành phố ngoài hộp): hộp thấp thủ tục theo năm — để chân trời không phẳng (bậc 5)
  const ss3 = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };   // cùng hàm cao độ đồi xa
  { const n = 9000, gb = new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0); const ms = new THREE.InstancedMesh(gb, new THREE.MeshLambertMaterial({ color: 0xffffff }), n); let q = 0; const M4 = new THREE.Matrix4();
    const rr = (i) => { const x = Math.sin(i * 12.9898) * 43758.5453; return x - Math.floor(x); };
    for (let i = 0; q < n && i < n * 6; i++) { const a = rr(i) * 6.283, r = 3200 + rr(i + 7) * 5000; const x = Math.cos(a) * r, z = Math.sin(a) * r * 0.8; if (x > T.x0 && x < T.x0 + TW && z > T.z0 && z < T.z0 + TD) continue;
      const w = 18 + rr(i + 3) * 45, h = 6 + rr(i + 5) * 12; const n_ = 0.6 + 0.4 * Math.sin(x * 0.0007 + 1.3) * Math.cos(z * 0.0009 - 0.4); const gy = 9 + 95 * ss3(3500, 9000, -z) * n_ + 70 * ss3(4500, 10000, z) * (0.7 + 0.3 * Math.sin(x * 0.0005)) + 25 * ss3(6000, 14000, Math.abs(x)) * n_; M4.compose(V3(x, gy - 2, z), new THREE.Quaternion().setFromAxisAngle(V3(0, 1, 0), rr(i + 9) * 3), V3(w, h, w * (0.5 + rr(i + 11)))); ms.setMatrixAt(q, M4); ms.setColorAt(q, new THREE.Color(0.10 + rr(i + 13) * 0.05, 0.095 + rr(i + 13) * 0.04, 0.09 + rr(i + 13) * 0.035)); q++; }
    ms.count = q; ms.material.onBeforeCompile = (s) => { Object.assign(s.uniforms, U); s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWf; uniform float uYear;')
        .replace('#include <begin_vertex>', `#include <begin_vertex>
          { vec3 ip = (instanceMatrix * vec4(0.0, 0.0, 0.0, 1.0)).xyz; float r = fract(sin(dot(ip.xz, vec2(12.9898, 78.233))) * 43758.5453); float era = smoothstep(1750.0, 1950.0, uYear);
            float keep = step(r, mix(0.12, 1.0, era)); transformed.y *= mix(0.35, 1.0, era) * keep; transformed.xz *= mix(0.25, 1.0, era) * keep; }`)
        .replace('#include <project_vertex>', '#include <project_vertex>\n vWf = (modelMatrix * instanceMatrix * vec4(transformed, 1.0)).xyz;');
      s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>\nvarying vec3 vWf; uniform float uMask; ${HAZE}`).replace('#include <dithering_fragment>', '#include <dithering_fragment>\n gl_FragColor.rgb = hazeApply(gl_FragColor.rgb, vWf); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(128.0 / 255.0), 1.0);'); };   /* V2: nhà xa ngoài hộp = "khac" */ ms.material.customProgramCacheKey = () => 'far'; LG.farCity = ms; scene.add(ms); }
  const skm = new THREE.ShaderMaterial({ uniforms: U, side: THREE.BackSide, depthWrite: false, vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 p = projectionMatrix * viewMatrix * vec4(position + cameraPosition, 1.0); gl_Position = p.xyww; }`,
    fragmentShader: `varying vec3 vD; uniform float uMask; ${GLSL_N} ${HAZE} ${SKYF} void main(){ vec3 d = normalize(vD); vec3 c = skyCol(d);
      float hz = 1.0 - smoothstep(0.0, 0.10, d.y); c = mix(c, uHaze, hz * 0.35); c = mix(c, uCoalCol * mix(1.0, 0.04, uNight), (1.0 - exp(-uCoal * 900.0)) * (1.0 - smoothstep(0.0, 0.12, d.y)));
      gl_FragColor = vec4(c, 1.0); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(40.0, 80.0, 200.0) / 255.0, 1.0); }` });
  SKY = new THREE.Mesh(new THREE.SphereGeometry(5000, 48, 24), skm); SKY.frustumCulled = false; SKY.renderOrder = -1; scene.add(SKY);
  // ---- đèn
  LG.hemi = new THREE.HemisphereLight(0xbfd2ee, 0x5a4a3a, 0.8); scene.add(LG.hemi);
  LG.sun = new THREE.DirectionalLight(0xffffff, 2.2); LG.sun.castShadow = true; LG.sun.shadow.mapSize.set(cfg.shadow || 6144, cfg.shadow || 6144); LG.sun.shadow.bias = -0.0003; LG.sun.shadow.normalBias = 0.5;
  scene.add(LG.sun); scene.add(LG.sun.target);
  // ---- lưới lửa 1666 + 1940 (20 m) → bản đồ ánh lửa
  const LC = META.luoi_chay; FMAP = { nx: LC.nx, nz: LC.nz, t: new Float32Array(await (await fetch(base + LK + 'luoi_chay.f32')).arrayBuffer()) };
  F40 = new Float32Array(await (await fetch(base + LK + 'luoi_1940.f32')).arrayBuffer());
  const mkT = () => { const t = new THREE.DataTexture(new Float32Array(LC.nx * LC.nz * 4), LC.nx, LC.nz, THREE.RGBAFormat, THREE.FloatType); t.magFilter = t.minFilter = THREE.LinearFilter; t.needsUpdate = true; return t; };
  FTEX = mkT(); F40TEX = mkT(); U.uFire.value = FTEX; U.uFire40.value = F40TEX; U.uFireBox.value.set(LC.E0 - 532000 - 10, -(LC.N0 - 180800) - 10, LC.nx * LC.buoc, LC.nz * LC.buoc);
  const ldc = (u) => new Promise((r) => TL.load(u, (t) => { t.colorSpace = THREE.NoColorSpace; t.minFilter = t.magFilter = THREE.LinearFilter; t.generateMipmaps = false; r(t); }, undefined, () => r(null)));
  U.uAtF = { value: await ldc(base + 'fb/lua.png') }; U.uAtS = { value: await ldc(base + 'fb/khoi.png') }; U.uAtlas = { value: U.uAtF.value ? 1 : 0 };
  FIRE = {}; SMOKE = {};
  for (const [key, grid, h] of [['66', FMAP.t, 'uHour'], ['40', F40, 'uH40']]) { const P = buildParticles(LC, grid, h, key); FIRE[key] = P.fire; SMOKE[key] = P.smoke; GLOW['e' + key] = P.emb; GLOW['g' + key] = P.glow; }
  await buildTrees(base); await buildBoats(base); await buildChimneySmoke(base);
  // ---- phản chiếu phẳng
  RT_REFL = new THREE.WebGLRenderTarget(Math.round(cfg.W / 2), Math.round(cfg.H / 2), { type: THREE.HalfFloatType }); RCAM = new THREE.PerspectiveCamera(); U.uRefl.value = RT_REFL.texture;
}
function blur1(src, nx, nz, r) { const o = new Float32Array(nx * nz), t = new Float32Array(nx * nz);
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { let s = 0, w = 0; for (let k = -r; k <= r; k++) { const ii = i + k; if (ii < 0 || ii >= nx) continue; s += src[j * nx + ii]; w++; } t[j * nx + i] = s / w; }
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { let s = 0, w = 0; for (let k = -r; k <= r; k++) { const jj = j + k; if (jj < 0 || jj >= nz) continue; s += t[jj * nx + i]; w++; } o[j * nx + i] = s / w; }
  return o; }
const ss = (e0, e1, x) => { const t = Math.min(1, Math.max(0, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t); };
function burnIJS(ign, h) { if (ign < 0 || h < ign) return 0; const a = h - ign; return ss(0, 0.7, a) * (1 - ss(4, 9, a)) + (a >= 9 ? 0.025 * (1 - ss(9, 48, a)) : 0); }
function burnI40JS(ign, h) { if (ign < 0 || h < ign) return 0; const a = h - ign; return ss(0, 0.4, a) * (1 - 0.6 * ss(3, 8, a)); }
function updateFire(tex, grid, h, fn, ash = 0) { const { nx, nz } = FMAP, I = new Float32Array(nx * nz), Bn = new Float32Array(nx * nz); if (h >= 0) for (let v = 0; v < nx * nz; v++) { I[v] = fn(grid[v], h); Bn[v] = (ash && grid[v] >= 0 && h - grid[v] > 4) ? 1 : 0; }
  const a = blur1(I, nx, nz, 1), b = blur1(I, nx, nz, 4), c = blur1(I, nx, nz, 12), e = blur1(Bn, nx, nz, 1), d = tex.image.data;
  for (let v = 0; v < nx * nz; v++) { d[v * 4] = a[v]; d[v * 4 + 1] = b[v] * 3; d[v * 4 + 2] = c[v] * 8; d[v * 4 + 3] = e[v]; }   /* A = tro (đã cháy > 4 h) */ tex.needsUpdate = true; let s = 0; for (let v = 0; v < nx * nz; v++) s += I[v]; return s; }
let BUFREF = null;
function groundAt(x, z) { const T = META.dia_hinh; const i = Math.round((x - T.x0) / T.step), j = Math.round((z - T.z0) / T.step); if (i < 0 || j < 0 || i >= T.nx || j >= T.nz) return 5;
  const l = META.bo_cuc.h66; return new Float32Array(BUFREF, l.off + 4 * (j * T.nx + i), 1)[0]; }
const frac = (x) => x - Math.floor(x);
// ---------------------------------------------------------------- hạt lửa + khói (atlas thể tích nướng sẵn — cách A, như tiền kỳ T1; thêm lưới 1940)
function buildParticles(LC, grid, hU, key) {
  const { nx, nz } = FMAP; const cells = [];
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const ig = grid[j * nx + i]; if (ig < 0) continue; cells.push([LC.E0 - 532000 + i * LC.buoc, -(LC.N0 - 180800) + j * LC.buoc, ig]); }
  const mk = (perCell) => { const n = cells.length * perCell, off = new Float32Array(n * 4), sd = new Float32Array(n * 2); let q = 0;
    for (const [x, z, ig] of cells) for (let k = 0; k < perCell; k++) { const r1 = frac(Math.sin((x * 12.9 + z * 78.2 + k * 37.1)) * 43758.5), r2 = frac(Math.sin((x * 3.7 + z * 11.3 + k * 91.7)) * 24634.6);
      const px = x + (r1 - 0.5) * 18, pz = z + (r2 - 0.5) * 18, gy = groundAt(px, pz); off[q * 4] = px; off[q * 4 + 1] = gy + (key === '40' ? 14 : 0); off[q * 4 + 2] = pz; off[q * 4 + 3] = gy < 1.2 ? -1 : ig + r1 * 0.6; sd[q * 2] = r1; sd[q * 2 + 1] = r2; q++; }
    const g = new THREE.InstancedBufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([-0.5, 0, 0, 0.5, 0, 0, 0.5, 1, 0, -0.5, 1, 0]), 3)); g.setIndex([0, 1, 2, 0, 2, 3]);
    g.setAttribute('off', new THREE.InstancedBufferAttribute(off, 4)); g.setAttribute('sd', new THREE.InstancedBufferAttribute(sd, 2)); g.instanceCount = n; return g; };
  const BI = key === '40' ? 'burnI40' : 'burnI';
  const VS = (kind) => `attribute vec4 off; attribute vec2 sd; uniform float uHour, uH40, uT, uAtlas, uSmokeK; uniform vec3 uCam; uniform vec2 uWind; varying vec2 vUv; varying float vA; varying float vH; varying float vSeed; varying float vY; ${burnI}
    void main(){ vUv = position.xy + vec2(0.5, 0.0); float I = ${BI}(off.w, ${hU}); vSeed = sd.x;
      ${kind === 'flame' ? `float life = 2.5 + sd.y * 2.0; float age = mod(uT + sd.x * 17.0, life) / life; float size = (5.0 + sd.y * 9.0) * smoothstep(0.15, 0.6, I) * (1.0 - 0.5 * age);
        vec3 c = off.xyz + vec3(uWind.x * age * 6.0, 6.0 + age * 14.0 * (0.5 + sd.y), uWind.y * age * 6.0); vA = smoothstep(0.15, 0.6, I) * (1.0 - age) * 0.55;`
        : `float life = 40.0 + sd.y * 50.0; float age = mod(uT * 0.9 + sd.x * 97.0, life) / life; float I2 = max(I, 0.0);
        float rise = 18.0 + age * (240.0 + sd.y * 300.0); float cap = 360.0 + sd.y * 340.0; float over = max(rise - cap, 0.0);   /* V2: cột khói bốc tới trần (≈ 0,4–0,7 km) rồi loang ngang theo gió — tách tầng */
        float size = (22.0 + age * 140.0 * (0.6 + sd.y) + over * 0.55) * smoothstep(0.0, 0.08, I2); float drift = (age * 460.0 + over * 1.6) * (0.7 + sd.x * 0.6);
        vec3 c = off.xyz + vec3(uWind.x * drift, min(rise, cap) + over * 0.15, uWind.y * drift + (sd.y - 0.5) * age * 140.0);
        vA = smoothstep(0.0, 0.08, I2) * (1.0 - age) * smoothstep(0.0, 0.05, age) * (0.12 + 0.88 * smoothstep(0.05, 0.35, I2)) * uSmokeK;   // khói âm ỉ trên phế tích mỏng hơn khói đám cháy`}
      vH = clamp(age, 0.0, 1.0); vec3 toC = normalize(uCam - c); vec3 rt = normalize(cross(vec3(0.0, 1.0, 0.0), toC)); vec3 up = ${kind === 'flame' ? 'vec3(0.0, 1.0, 0.0)' : 'normalize(cross(toC, rt))'};
      float ar = uAtlas > 0.5 ? 2.0 : 1.3; float sz = uAtlas > 0.5 ? size * ${kind === 'flame' ? '0.75' : '0.8'} : size;
      float dcam = length(uCam - c); ${kind === 'flame' ? '' : 'vA *= smoothstep(60.0, 220.0, dcam);'}
      vec3 w = c + rt * position.x * sz + up * (position.y - ${kind === 'flame' ? '0.1' : '0.5'}) * sz * ar; if (size < 0.01) w = vec3(0.0, -1000.0, 0.0); vY = c.y - off.y;
      gl_Position = projectionMatrix * viewMatrix * vec4(w, 1.0); }`;
  const ATL = `uniform sampler2D uAtF, uAtS; uniform float uAtlas; vec2 atl(vec2 uv, float age, float seed){ float idx = mod(floor(age * 63.0) + floor(seed * 64.0), 64.0); float c = mod(idx, 8.0), r = floor(idx / 8.0);
      return vec2((c + clamp(uv.x, 0.0, 1.0)) / 8.0, 1.0 - (r + 1.0 - clamp(uv.y, 0.0, 1.0)) / 8.0); }`;
  const FS_FLAME = `varying vec2 vUv; varying float vA; varying float vH; varying float vSeed; uniform float uT, uNight; ${GLSL_N} ${ATL}
    void main(){ if (uAtlas > 0.5) { vec3 t = texture2D(uAtF, atl(vUv, fract(uT * 0.35 + vSeed), vSeed)).rgb; vec3 o = t * t * vec3(1.0, 0.58, 0.28) + vec3(1.0, 0.86, 0.58) * pow(clamp(t.r * 1.2 - 0.45, 0.0, 1.0), 2.0) * 1.8; gl_FragColor = vec4(o * vA * (1.1 + 0.45 * uNight) * 1.7, 0.0); return; }   /* V2: lõi vàng trắng */
      vec2 p = vUv - vec2(0.5, 0.0); float n = fbm(vec2(p.x * 3.0 + vSeed * 9.0, vUv.y * 2.2 - uT * 2.6));
      float sh = smoothstep(0.5, 0.0, abs(p.x) * (1.0 + vUv.y * 1.8) + (vUv.y - 0.25) * 0.45 - n * 0.35) * smoothstep(1.0, 0.25, vUv.y);
      vec3 c = mix(vec3(1.0, 0.85, 0.45), vec3(1.0, 0.32, 0.05), smoothstep(0.1, 0.8, vUv.y + n * 0.3)); gl_FragColor = vec4(c * sh * vA * 1.4 * (0.35 + 0.65 * uNight), 0.0); }`;
  const FS_SMOKE = `varying vec2 vUv; varying float vA; varying float vH; varying float vSeed; varying float vY; uniform float uT, uNight, uFireK; uniform vec3 uSunCol, uHaze; uniform vec3 uSmokeTint; ${GLSL_N} ${ATL}
    void main(){ float d; float tg;
      if (uAtlas > 0.5) { vec3 t = texture2D(uAtS, atl(vUv, vH, vSeed)).rgb; d = t.r * vA * 0.55 * smoothstep(0.0, 0.08, vUv.y) * smoothstep(1.0, 0.6, vUv.y) * smoothstep(0.0, 0.18, min(vUv.x, 1.0 - vUv.x)); tg = t.g;
        d = smoothstep(0.04, 0.55, t.r) * vA * 0.85 * smoothstep(0.0, 0.10, vUv.y) * smoothstep(1.0, 0.45, vUv.y) * smoothstep(0.0, 0.24, min(vUv.x, 1.0 - vUv.x));   /* V2: khói đặc khối, mép rõ */
        if (uNight > 0.5) d = smoothstep(0.0, 0.85, t.r) * vA * 0.62 * smoothstep(0.0, 0.22, vUv.y) * smoothstep(1.0, 0.30, vUv.y) * smoothstep(0.0, 0.42, min(vUv.x, 1.0 - vUv.x));   /* B1: khói đêm mép mềm, mỏng hơn — cột khói liền */
        float young = 1.0 - smoothstep(0.0, 0.45, vH); vec3 dk = mix(vec3(0.042, 0.037, 0.033), vec3(0.13, 0.12, 0.108), vH); d *= mix(1.0, 0.72, smoothstep(0.5, 1.0, vH));
        vec3 day = mix(dk, vec3(0.50, 0.46, 0.41) * (0.55 + 0.45 * uSunCol), pow(tg, 1.25)) * uSmokeTint; day = mix(day, uHaze * 0.8, vH * 0.15);
        day += vec3(0.95, 0.40, 0.10) * t.b * young * young * 0.30 * uFireK;   /* chân cột hắt lửa cả ban ngày */
        float hg = exp(-max(vY - 25.0, 0.0) / 85.0) * (0.45 + 0.55 * (1.0 - smoothstep(0.15, 0.8, vUv.y)));   /* ánh lửa theo độ cao tâm cụm khói trên mặt đất: chỉ chân cột (< ≈ 150 m) hắt đỏ, tầng trên tối */
        vec3 night = vec3(0.016, 0.014, 0.014) + vec3(1.0, 0.34, 0.07) * (0.25 + 0.75 * t.b) * 0.9 * hg;   /* V2: mặt dưới cột khói hắt đỏ mạnh hơn */
        gl_FragColor = vec4(mix(day, night, uNight) * d, d); return; }
      vec2 p = vUv - 0.5; float r = length(p); float n = fbm(p * 3.2 + vec2(vSeed * 13.0, uT * 0.03 + vSeed)); d = smoothstep(0.5, 0.05, r + (n - 0.5) * 0.45) * vA * 0.45;
      vec3 day = mix(vec3(0.16, 0.14, 0.13), vec3(0.50, 0.47, 0.44) * (0.6 + 0.4 * uSunCol), smoothstep(0.35, 0.95, n + vUv.y * 0.35));
      vec3 night = mix(vec3(0.75, 0.28, 0.07) * (1.0 - vH) * (1.0 - vH), vec3(0.025, 0.022, 0.022), clamp(smoothstep(0.0, 0.45, vH) + vUv.y * 0.25, 0.0, 1.0));
      gl_FragColor = vec4(mix(day, night, uNight) * d, d); }`;
  if (!U.uSmokeK) { U.uSmokeK = { value: 1 }; U.uSmokeTint = { value: new THREE.Color(1, 1, 1) }; }
  const fire = new THREE.Mesh(mk(key === '40' ? 1 : 2), new THREE.ShaderMaterial({ uniforms: U, vertexShader: VS('flame'), fragmentShader: FS_FLAME, transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor }));
  const smoke = new THREE.Mesh(mk(key === '40' ? 2 : 4), new THREE.ShaderMaterial({ uniforms: U, vertexShader: VS('smoke'), fragmentShader: FS_SMOKE, transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor }));
  fire.frustumCulled = smoke.frustumCulled = false; smoke.renderOrder = 2; fire.renderOrder = 3; fire.visible = smoke.visible = false; scene.add(smoke); scene.add(fire);
  // V2: TÀN LỬA bay theo gió (điểm sáng ≥ 1,5 px ở mọi khoảng cách) + QUẦNG sáng mềm trên đám cháy (ngọn lửa "phát sáng")
  const VSE = `attribute vec4 off; attribute vec2 sd; uniform float uHour, uH40, uT; uniform vec3 uCam; uniform vec2 uWind; varying vec2 vUv; varying float vA; varying float vF; ${burnI}
    void main(){ vUv = position.xy + vec2(0.5, 0.0); float I = ${BI}(off.w, ${hU}); float life = 5.0 + sd.y * 9.0; float age = mod(uT + sd.x * 31.0, life) / life;
      float rise = 8.0 + age * (60.0 + sd.y * 160.0); float drift = age * age * (160.0 + sd.x * 300.0);
      vec3 c = off.xyz + vec3(uWind.x * drift + sin(age * 19.0 + sd.x * 40.0) * 5.0, rise, uWind.y * drift + cos(age * 17.0 + sd.y * 30.0) * 5.0);
      float dcam = length(uCam - c); float size = max(0.7, dcam * 0.0017) * step(0.3, I);
      vA = smoothstep(0.3, 0.7, I) * (1.0 - age) * smoothstep(0.0, 0.05, age); vF = fract(sd.x * 13.1 + sd.y * 7.3);
      vec3 toC = normalize(uCam - c); vec3 rt = normalize(cross(vec3(0.0, 1.0, 0.0), toC)); vec3 up = normalize(cross(toC, rt));
      vec3 w = c + (rt * position.x + up * (position.y - 0.5)) * size; if (size < 0.01) w = vec3(0.0, -1000.0, 0.0); gl_Position = projectionMatrix * viewMatrix * vec4(w, 1.0); }`;
  const FSE = `varying vec2 vUv; varying float vA; varying float vF; uniform float uT, uNight;
    void main(){ float r = length(vUv - vec2(0.5)) * 2.0; float k = smoothstep(1.0, 0.0, r); float fl = 0.55 + 0.45 * sin(uT * 23.0 + vF * 60.0);
      gl_FragColor = vec4(mix(vec3(1.0, 0.45, 0.10), vec3(1.0, 0.80, 0.45), vF) * k * vA * fl * 2.4 * (0.30 + 0.70 * uNight), 0.0); }`;
  const VSG = `attribute vec4 off; attribute vec2 sd; uniform float uHour, uH40, uT; uniform vec3 uCam; varying vec2 vUv; varying float vA; ${burnI}
    void main(){ vUv = position.xy + vec2(0.5, 0.0); float I = ${BI}(off.w, ${hU}); float size = (44.0 + sd.y * 40.0) * step(0.05, I);
      vec3 c = off.xyz + vec3(0.0, 4.0, 0.0); vA = smoothstep(0.1, 0.7, I) * (0.85 + 0.15 * sin(uT * 3.0 + sd.x * 20.0));
      vec3 toC = normalize(uCam - c); vec3 rt = normalize(cross(vec3(0.0, 1.0, 0.0), toC)); vec3 up = normalize(cross(toC, rt));
      vec3 w = c + (rt * position.x + up * (position.y - 0.35)) * size; if (size < 0.01) w = vec3(0.0, -1000.0, 0.0); gl_Position = projectionMatrix * viewMatrix * vec4(w, 1.0); }`;
  const FSG = `varying vec2 vUv; varying float vA; uniform float uNight;
    void main(){ vec2 q = (vUv - vec2(0.5, 0.35)) * vec2(2.0, 1.6); float k = exp(-dot(q, q) * 3.2); gl_FragColor = vec4(vec3(1.0, 0.40, 0.09) * k * vA * 0.23 * (0.25 + 0.75 * uNight), 0.0); }`;
  const add = { transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor };
  const emb = new THREE.Mesh(mk(key === '40' ? 3 : 5), new THREE.ShaderMaterial(Object.assign({ uniforms: U, vertexShader: VSE, fragmentShader: FSE }, add)));
  const glow = new THREE.Mesh(mk(1), new THREE.ShaderMaterial(Object.assign({ uniforms: U, vertexShader: VSG, fragmentShader: FSG }, add)));
  emb.frustumCulled = glow.frustumCulled = false; emb.renderOrder = 4; glow.renderOrder = 1; emb.visible = glow.visible = false; scene.add(emb); scene.add(glow);
  return { fire, smoke, emb, glow };
}
// ---------------------------------------------------------------- cây (tán + thân; theo năm; lá theo mùa)
async function buildTrees(base) {
  const a = new Float32Array(await (await fetch(base + LK + 'cay.f32')).arrayBuffer()); const n = a.length / 7;
  const crown = new THREE.IcosahedronGeometry(1, 1); { const p = crown.attributes.position; for (let i = 0; i < p.count; i++) { const k = 0.82 + 0.3 * frac(Math.sin(i * 91.7) * 4375.5); p.setXYZ(i, p.getX(i) * k, p.getY(i) * k * 0.85 + 1.0, p.getZ(i) * k); } crown.computeVertexNormals(); }
  const off = new Float32Array(n * 4), yr = new Float32Array(n * 2);
  for (let i = 0; i < n; i++) { off.set([a[i * 7], a[i * 7 + 1], a[i * 7 + 2], a[i * 7 + 3]], i * 4); yr.set([a[i * 7 + 4], a[i * 7 + 5]], i * 2); }
  const g = new THREE.InstancedBufferGeometry().copy(crown); g.instanceCount = n; g.setAttribute('off', new THREE.InstancedBufferAttribute(off, 4)); g.setAttribute('yr', new THREE.InstancedBufferAttribute(yr, 2));
  const mat = new THREE.MeshLambertMaterial({ color: 0xffffff });
  const vs = (s) => s.replace('#include <common>', '#include <common>\nattribute vec4 off; attribute vec2 yr; uniform float uYear, uLeaf; varying vec3 vWt; varying float vSd;')
    .replace('#include <begin_vertex>', `#include <begin_vertex>
      float alive = (uYear >= yr.x && uYear < yr.y) ? 1.0 : 0.0; float r = off.w * mix(0.62, 1.0, uLeaf); transformed = transformed * vec3(r, r * 1.15, r) + vec3(0.0, r * 0.6, 0.0); transformed += off.xyz; transformed *= alive; vWt = transformed; vSd = fract(off.x * 0.37 + off.z * 0.71);`);
  mat.onBeforeCompile = (s) => { Object.assign(s.uniforms, U); if (!U.uLeaf) U.uLeaf = { value: 1 }; s.uniforms.uLeaf = U.uLeaf;
    s.vertexShader = vs(s.vertexShader);
    s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>\nvarying vec3 vWt; varying float vSd; uniform float uLeaf, uMask; ${GLSL_N} ${HAZE}`)
      .replace('vec4 diffuseColor = vec4( diffuse, opacity );', `float nn = vn(vWt.xz * 0.9 + vWt.y * 0.7); vec3 lf = mix(vec3(0.05, 0.085, 0.03), vec3(0.11, 0.15, 0.05), nn) * (0.8 + 0.4 * vSd);
        vec3 br = mix(vec3(0.10, 0.085, 0.07), vec3(0.16, 0.13, 0.10), nn); vec4 diffuseColor = vec4(mix(br, lf, uLeaf), 1.0);`)
      .replace('#include <dithering_fragment>', '#include <dithering_fragment>\n gl_FragColor.rgb = hazeApply(gl_FragColor.rgb, vWt); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(vec3(60.0, 140.0, 60.0) / 255.0, 1.0);'); };
  mat.customProgramCacheKey = () => 'cay';
  const dm = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking }); dm.onBeforeCompile = (s) => { Object.assign(s.uniforms, U); s.uniforms.uLeaf = U.uLeaf || (U.uLeaf = { value: 1 }); s.vertexShader = vs(s.vertexShader); }; dm.customProgramCacheKey = () => 'cay-d';
  TREES = new THREE.Mesh(g, mat); TREES.customDepthMaterial = dm; TREES.castShadow = TREES.receiveShadow = true; TREES.frustumCulled = false; scene.add(TREES);
}
// ---------------------------------------------------------------- thuyền theo mốc
function hullGeo(kind, y0) {
  const parts = []; const add = (g, c) => { const col = new Float32Array(g.attributes.position.count * 3); for (let i = 0; i < col.length; i += 3) col.set(c, i); g.setAttribute('color', new THREE.BufferAttribute(col, 3)); parts.push(g.toNonIndexed ? g.toNonIndexed() : g); };
  const lin = (c) => c.map((v) => Math.pow(v, 2.2));
  const hull = (L, W, H, c) => { const g = new THREE.BoxGeometry(L, H, W, 4, 1, 1); const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i) / (L / 2); const t = 1 - Math.pow(Math.abs(x), 2.5); p.setZ(i, p.getZ(i) * Math.max(0.15, t)); p.setY(i, p.getY(i) + (Math.abs(x) > 0.7 ? H * 0.25 * (Math.abs(x) - 0.7) : 0)); } g.computeVertexNormals(); g.translate(0, H / 2 - 0.4, 0); add(g, lin(c)); };
  const mast = (x, h, r = 0.15) => { const g = new THREE.CylinderGeometry(r * 0.6, r, h, 6); g.translate(x, h / 2, 0); add(g, lin([0.25, 0.18, 0.12])); };
  const sail = (x, y, w, h, c) => { const g = new THREE.PlaneGeometry(0.01 + 0.0, h, 1, 1); const s2 = new THREE.BoxGeometry(0.1, h, w); s2.translate(x, y, 0); add(s2, lin(c)); };
  if (kind === 'wherry') { hull(6.5, 1.5, 0.7, [0.30, 0.22, 0.15]); }
  else if (kind === 'lighter') { hull(14, 4.2, 1.4, [0.22, 0.17, 0.12]); mast(1.0, 9, 0.12); sail(1.2, 5.5, 5, 6, [0.55, 0.36, 0.22]); }
  else if (kind === 'ship') { hull(32, 8.5, 4.5, [0.20, 0.14, 0.09]); const s3 = new THREE.BoxGeometry(7, 3, 7.5); s3.translate(-12, 5.2, 0); add(s3, lin([0.22, 0.15, 0.10]));
    mast(-6, 26, 0.35); mast(4, 30, 0.4); mast(13, 20, 0.3);   // neo ở Pool of London: buồm cuộn trên trục ngang (yard)
    for (const [x, ys] of [[-6, [12, 19, 24]], [4, [14, 22, 28]], [13, [11, 17]]]) for (const y of ys) { const yd = new THREE.CylinderGeometry(0.35, 0.35, 12 - y * 0.2, 6).rotateX(Math.PI / 2); yd.translate(x, y, 0); add(yd, lin([0.62, 0.58, 0.50])); } }
  else if (kind === 'barge') { hull(26, 6.5, 1.8, y0 > 1980 ? [0.20, 0.22, 0.25] : [0.26, 0.19, 0.13]);   /* B1: thân sơn (không gần đen) + boong + nắp hầm / công-te-nơ */
    const dk = new THREE.BoxGeometry(24, 0.25, 5.6); dk.translate(0, 1.45, 0); add(dk, lin([0.42, 0.40, 0.37]));
    if (y0 > 1980) { const cols = [[0.78, 0.62, 0.22], [0.70, 0.72, 0.74], [0.30, 0.42, 0.55]]; for (let i = 0; i < 3; i++) { const c = new THREE.BoxGeometry(6.0, 2.4, 2.4); c.translate(-7.5 + i * 7.5, 2.8, 0); add(c, lin(cols[i])); } }
    else { const tp = new THREE.BoxGeometry(18, 0.9, 5.0); tp.translate(0, 2.0, 0); add(tp, lin([0.34, 0.33, 0.28])); } }
  else if (kind === 'tug') { hull(18, 5, 2.4, [0.10, 0.10, 0.11]); const c = new THREE.BoxGeometry(5, 3, 3.5); c.translate(0, 3.2, 0); add(c, lin([0.55, 0.52, 0.46])); const f = new THREE.CylinderGeometry(0.7, 0.8, 3.5, 8); f.translate(-1, 5.5, 0); add(f, lin([0.12, 0.10, 0.10])); }
  else if (kind === 'cruise') { hull(36, 7, 2.2, [0.85, 0.85, 0.84]); const c = new THREE.BoxGeometry(24, 2.6, 6); c.translate(1, 3.0, 0); add(c, lin([0.25, 0.30, 0.34])); }
  const g = new THREE.BufferGeometry(); const cat = (k) => { const arrs = parts.map((p) => p.attributes[k].array); const n = arrs.reduce((s, a) => s + a.length, 0); const o = new Float32Array(n); let q = 0; for (const a of arrs) { o.set(a, q); q += a.length; } return o; };
  g.setAttribute('position', new THREE.BufferAttribute(cat('position'), 3)); g.setAttribute('color', new THREE.BufferAttribute(cat('color'), 3)); g.computeVertexNormals(); return g;
}
async function buildBoats(base) {
  const L = await (await fetch(base + LK + 'thuyen.json')).json(); const kinds = [...new Set(L.map((b) => b.k + '|' + b.y0))]; const M4 = new THREE.Matrix4();   /* B1: nhóm theo kiểu + thời kỳ */
  for (const ky of kinds) { const [k, y0s] = ky.split('|'); const list = L.filter((b) => b.k === k && String(b.y0) === y0s); const mat = new THREE.MeshLambertMaterial({ vertexColors: true });
    mat.onBeforeCompile = (s) => { Object.assign(s.uniforms, U); s.vertexShader = s.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWb;').replace('#include <project_vertex>', '#include <project_vertex>\n vWb = (modelMatrix * instanceMatrix * vec4(transformed, 1.0)).xyz;');
      s.fragmentShader = s.fragmentShader.replace('#include <common>', `#include <common>\nvarying vec3 vWb; uniform float uMask; ${HAZE}`).replace('#include <dithering_fragment>', '#include <dithering_fragment>\n gl_FragColor.rgb = hazeApply(gl_FragColor.rgb, vWb); if (uMask > 0.5) gl_FragColor = uMask > 2.5 ? vec4(0.0, 0.0, 0.0, 1.0) : vec4(1.0, 0.0, 0.0, 1.0);'); };
    mat.customProgramCacheKey = () => 'thuyen';
    const im = new THREE.InstancedMesh(hullGeo(k, +y0s), mat, list.length); list.forEach((b, i) => { M4.compose(V3(b.x, 0.5, b.z), new THREE.Quaternion().setFromAxisAngle(V3(0, 1, 0), b.a), V3(1, 1, 1)); im.setMatrixAt(i, M4); });
    im.castShadow = true; im.frustumCulled = false; im.userData = { y0: list[0].y0, y1: list[0].y1, list }; BOATS.push(im); scene.add(im); }
}
function updateBoats(year, night, fireOn) { const M4 = new THREE.Matrix4(), Z = new THREE.Matrix4().makeScale(0, 0, 0);
  for (const im of BOATS) { im.userData.list.forEach((b, i) => { const on = year >= b.y0 && year < b.y1 && !(night && b.k === 'cruise' && false); if (on) { M4.compose(V3(b.x, 0.5, b.z), new THREE.Quaternion().setFromAxisAngle(V3(0, 1, 0), b.a), V3(1, 1, 1)); im.setMatrixAt(i, M4); } else im.setMatrixAt(i, Z); }); im.instanceMatrix.needsUpdate = true; } }
// ---------------------------------------------------------------- khói bếp (than/củi) — billboard từ ống khói; mật độ theo biến thể (B: khói than nền dày hơn)
async function buildChimneySmoke(base) {
  const a = new Float32Array(await (await fetch(base + LK + 'khoi_bep.f32')).arrayBuffer()); const n = a.length / 5, P = 5; const off = new Float32Array(n * P * 4), sd = new Float32Array(n * P * 4);
  for (let i = 0; i < n; i++) for (let k = 0; k < P; k++) { const q = i * P + k; off.set([a[i * 5], a[i * 5 + 1], a[i * 5 + 2], k / P], q * 4); sd.set([a[i * 5 + 3], a[i * 5 + 4], frac(Math.sin(i * 17.3) * 4375.85), frac(Math.sin(i * 7.1 + k) * 9375.3)], q * 4); }
  const g = new THREE.InstancedBufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([-0.5, 0, 0, 0.5, 0, 0, 0.5, 1, 0, -0.5, 1, 0]), 3)); g.setIndex([0, 1, 2, 0, 2, 3]);
  g.setAttribute('off', new THREE.InstancedBufferAttribute(off, 4)); g.setAttribute('sd', new THREE.InstancedBufferAttribute(sd, 4)); g.instanceCount = n * P;
  U.uChimK = { value: 0 };
  CHIM = new THREE.Mesh(g, new THREE.ShaderMaterial({ uniforms: U, transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
    vertexShader: `attribute vec4 off; attribute vec4 sd; uniform float uYear, uT, uChimK; uniform vec3 uCam; uniform vec2 uWind; varying vec2 vUv; varying float vA; varying float vS;
      void main(){ vUv = position.xy + vec2(0.5, 0.0); float on = (uYear >= sd.x && uYear < sd.y && sd.z < uChimK) ? 1.0 : 0.0; float age = fract(off.w + uT * 0.02 + sd.w * 0.1);
        vec3 c = off.xyz + vec3(uWind.x * age * 70.0, age * 26.0 + 1.0, uWind.y * age * 70.0); float size = (1.5 + age * 13.0) * on; vA = on * (1.0 - age) * smoothstep(0.0, 0.15, age) * 0.30 * smoothstep(180.0, 520.0, length(uCam - c)) * (1.0 - smoothstep(1500.0, 3000.0, length(uCam - c))); vS = sd.w;   /* V2: khói bếp xa mờ dần (trước đây không áp sương → đốm sáng ở chân trời) */
        vec3 toC = normalize(uCam - c); vec3 rt = normalize(cross(vec3(0.0, 1.0, 0.0), toC)); vec3 up = normalize(cross(toC, rt)); vec3 w = c + (rt * position.x + up * (position.y - 0.5)) * size;
        if (size < 0.01) w = vec3(0.0, -1000.0, 0.0); gl_Position = projectionMatrix * viewMatrix * vec4(w, 1.0); }`,
    fragmentShader: `varying vec2 vUv; varying float vA; varying float vS; uniform vec3 uSunCol, uHaze; uniform float uNight; ${GLSL_N}
      void main(){ vec2 p = vUv - 0.5; float n = fbm3(p * 3.0 + vS * 11.0); float d = smoothstep(0.5, 0.1, length(p) + (n - 0.5) * 0.5) * vA; vec3 c = mix(vec3(0.34, 0.33, 0.32), uHaze, 0.35) * (0.5 + 0.5 * uSunCol) * (1.0 - 0.85 * uNight); gl_FragColor = vec4(c * d, d); }` }));
  CHIM.frustumCulled = false; CHIM.renderOrder = 1; scene.add(CHIM);
}
// ---------------------------------------------------------------- thời điểm + biến thể look
// f.look: {haze:[σ m⁻¹, r,g,b], hazeH, coal:[σ, r,g,b, H], sunK, hemiK, sunTint:[r,g,b], skyTop, skyHor, cloud, cloudCol, water, texK, chim, smokeK, smokeTint, exposure, bakeK}
function setTime(f) {
  const year = f.year, hour = f.hour ?? -1, h40 = f.h40 ?? -1, lk = f.look || {};
  U.uYear.value = hour >= 0 ? yearOfHour(hour) : year; U.uHour.value = hour; U.uH40.value = h40; let jd;
  if (hour >= 0) jd = jdJulian(1666, 9, 2, hour - LON.lon / 15);
  else if (f.date) jd = jdOf(f.date[0], f.date[1], f.date[2], f.date[3] - (f.tz ?? 0));
  else { const y = Math.floor(year), d = (year - y) * 365; jd = jdOf(y, 1, 1, 0) + d; }
  const sp = sunPos(jd, LON.lat, LON.lon); const el = sp.el * Math.PI / 180, az = sp.az * Math.PI / 180;
  const sd = V3(Math.sin(az) * Math.cos(el), Math.sin(el), -Math.cos(az) * Math.cos(el)); U.uSunDir.value.copy(sd);
  const day = THREE.MathUtils.smoothstep(sp.el, -8, 6), night = 1 - day; U.uNight.value = night; const warm = THREE.MathUtils.smoothstep(sp.el, 0, 30);
  const st = lk.sunTint || [1, 1, 1]; U.uSunCol.value.setRGB((1.0) * st[0], (0.70 + 0.27 * warm) * st[1], (0.45 + 0.48 * warm) * st[2]);
  const sky = lk.skyTop || [0.24, 0.40, 0.74], hor = lk.skyHor || [0.66, 0.72, 0.80];
  U.uSkyTop.value.setRGB(sky[0] * day + 0.004, sky[1] * day + 0.006, sky[2] * day + 0.016); U.uSkyHor.value.setRGB(hor[0] * day + 0.010, hor[1] * day + 0.011, hor[2] * day + 0.020);
  const hz = lk.haze || [1 / 9000, 0.66, 0.70, 0.76]; U.uHazeS.value = hz[0]; U.uHaze.value.setRGB(hz[1] * day + 0.012, hz[2] * day + 0.013, hz[3] * day + 0.022); U.uHazeH.value = lk.hazeH || 350;
  const co = lk.coal || [0, 0.5, 0.46, 0.40, 70]; U.uCoal.value = co[0]; U.uCoalCol.value.setRGB(co[1], co[2], co[3]); U.uCoalH.value = co[4];
  U.uCloud.value = lk.cloud ?? 0.35; const cc = lk.cloudCol || [1, 0.99, 0.96]; U.uCloudCol.value.setRGB(cc[0] * day + 0.02, cc[1] * day + 0.02, cc[2] * day + 0.03);
  const wa = lk.water || [0.050, 0.058, 0.045]; U.uWater.value.setRGB(...wa); U.uTexK.value = lk.texK ?? 1; U.uBakeK.value = lk.bakeK ?? 1;
  if (f.smokeSky && (hour >= 0)) { const k = f.smokeSky; U.uSkyTop.value.lerp(new THREE.Color(0.50, 0.42, 0.34), k * day); U.uSkyHor.value.lerp(new THREE.Color(0.62, 0.50, 0.38), k * day); U.uHaze.value.lerp(new THREE.Color(0.58, 0.48, 0.38), k * day); }
  LG.sun.intensity = (lk.sunK ?? 3.0) * day + (f.moon ?? 0.25) * night; LG.sun.color.copy(U.uSunCol.value); if (night > 0.5) LG.sun.color.setRGB(0.55, 0.65, 0.9);
  const dir = night > 0.5 ? V3(-0.3, 0.6, 0.5).normalize() : sd; LG.sun.position.copy(dir).multiplyScalar(3000);
  LG.hemi.intensity = (lk.hemiK ?? 0.6) * day + 0.16 * night; LG.hemi.color.setRGB(0.70 * day + 0.2 * night, 0.80 * day + 0.25 * night, 0.95 * day + 0.4 * night); LG.hemi.groundColor.setRGB(0.36, 0.30, 0.24);
  U.uWin.value = (hour < 0 && h40 < 0 && year > 1950) ? night : 0;
  const w = f.wind || [-1, 0.15]; U.uWind.value.set(w[0], w[1]).normalize();
  const fs = updateFire(FTEX, FMAP.t, hour, burnIJS, 1); const f4 = updateFire(F40TEX, F40, h40, burnI40JS); U.uFireK.value = (hour >= 0 || h40 >= 0) ? (0.5 + 1.2 * night) : 0;
  U.uChimK.value = (U.uYear.value < 1960 && hour < 0 && h40 < 0) ? (lk.chim ?? 0.35) : (hour >= 0 ? (lk.chim ?? 0.35) * 0.3 : 0);
  U.uSmokeK.value = lk.smokeK ?? 1; const stt = lk.smokeTint || [1, 1, 1]; U.uSmokeTint.value.setRGB(...stt);
  if (U.uLeaf) U.uLeaf.value = f.leaf ?? 1;
  updateBoats(U.uYear.value, night > 0.5, hour >= 0);
  return { el: sp.el, az: sp.az, fireSum: fs + f4 };
}
function setCam(c) {
  const P = (e) => V3(e[0] - 532000, e[2], -(e[1] - 180800));
  cam.fov = c.fov; cam.aspect = CFG.W / CFG.H; cam.near = 2; cam.far = 14000; cam.updateProjectionMatrix();
  cam.position.copy(P(c.p)); cam.lookAt(P(c.l)); cam.updateMatrixWorld(); U.uCam.value.copy(cam.position);
  const tgt = P(c.l); const d = cam.position.distanceTo(tgt); const focus = cam.position.clone().lerp(tgt, Math.min(1, 900 / Math.max(d, 1)) * 0.9 + 0.1);
  LG.sun.target.position.copy(focus); LG.sun.position.add(focus);
  const span = Math.min(2400, Math.max(500, d * 1.3)); const sc = LG.sun.shadow.camera; sc.left = sc.bottom = -span; sc.right = sc.top = span; sc.near = 10; sc.far = 7000; sc.updateProjectionMatrix();
}
function renderReflection() {   // gương phẳng y = 0,6: máy đối xứng + mặt phẳng cắt
  const y0 = 0.6; RCAM.copy(cam); RCAM.position.y = 2 * y0 - cam.position.y; const dir = new THREE.Vector3(); cam.getWorldDirection(dir); dir.y = -dir.y;
  RCAM.up.set(0, 1, 0); RCAM.lookAt(RCAM.position.clone().add(dir)); RCAM.updateMatrixWorld(); RCAM.updateProjectionMatrix();
  U.uReflVP.value.multiplyMatrices(RCAM.projectionMatrix, RCAM.matrixWorldInverse);
  WATER.visible = false; const cp = R.clippingPlanes; R.clippingPlanes = [new THREE.Plane(V3(0, 1, 0), -y0 + 0.3)]; const sh = R.shadowMap.autoUpdate;
  U.uCam.value.copy(RCAM.position); R.setRenderTarget(RT_REFL); R.setClearColor(0x000000, 0); R.clear(); R.render(scene, RCAM); R.setRenderTarget(null);
  U.uCam.value.copy(cam.position); R.clippingPlanes = cp; R.shadowMap.autoUpdate = sh; WATER.visible = true; U.uReflOn.value = 1;
}
window.setup = async (cfg) => {
  CFG = cfg; LK = cfg.lk || 'look2/'; R = createRenderer(cfg.W, cfg.H); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap; R.localClippingEnabled = false;
  document.body.appendChild(R.domElement); scene = new THREE.Scene(); cam = new THREE.PerspectiveCamera(40, cfg.W / cfg.H, 2, 14000);
  BUFREF = await (await fetch(cfg.data + LK + 'ldn2.bin')).arrayBuffer();
  await build(cfg);
  pipe = createPipeline(R, cfg.W, cfg.H, { exposure: cfg.exposure || 0.9, uniformDecl: 'uniform float uVig;', gradeGLSL: `vec3 grade(vec3 c, vec2 uv){ vec2 d = (uv - 0.5) * vec2(1.0, 0.82); return c * mix(1.0, 0.86, smoothstep(0.3, 0.85, length(d))); }` });
  const e = R.getContext().getExtension('WEBGL_debug_renderer_info');
  return { renderer: e ? R.getContext().getParameter(e.UNMASKED_RENDERER_WEBGL) : 'unknown', tris: META.tam_giac };
};
window.setBake = async (url, box) => { if (!url) { U.uBakeOn.value = 0; return false; } const t = await new Promise((r) => new THREE.TextureLoader().load(url, r, undefined, () => r(null)));
  if (!t) { U.uBakeOn.value = 0; return false; } t.colorSpace = THREE.NoColorSpace; t.flipY = true; t.minFilter = t.magFilter = THREE.LinearFilter; t.generateMipmaps = false; U.uBake.value = t; U.uBakeBox.value.set(...box); U.uBakeOn.value = 1; return true; };
// f: {cam:{p,l,fov}, year, hour (1666), h40 (1940: giờ kể từ 29/12 18:00), date:[y,m,d,giờ], tz, t, spp, look:{…}, smokeSky, wind, leaf, refl}
window.renderFrame = async (f) => {
  const t0 = performance.now(); setCam(f.cam); const L = setTime(f); U.uT.value = f.t || 0; U.uDbg.value = f.dbg ? 1 : 0;
  pipe.outMat.uniforms.uExp.value = (f.look && f.look.exposure) || CFG.exposure || 0.9;
  const fire66 = (f.hour ?? -1) >= 0, fire40 = (f.h40 ?? -1) >= 0;
  FIRE['66'].visible = fire66 && f.fire !== false; SMOKE['66'].visible = fire66 && f.smoke !== false; FIRE['40'].visible = fire40 && f.fire !== false; SMOKE['40'].visible = fire40 && f.smoke !== false;
  for (const k of ['66', '40']) { const on = (k === '66' ? fire66 : fire40) && f.fire !== false; GLOW['e' + k].visible = on && f.embers !== false; GLOW['g' + k].visible = on && f.glow !== false; }
  U.uToy.value = f.look && f.look.toy != null ? f.look.toy : 1; CHIM.visible = f.chim !== false;
  U.uBong.value = f.bong ? 1 : 0; U.uD.value = f.d ? 1 : 0; U.uD2.value = (f.d2 && U.tFac.value) ? 1 : 0;
  if (f.proj && PROJ.url !== f.proj.url) { PROJ.url = f.proj.url; U.uProj.value = await new Promise((r) => new THREE.TextureLoader().load(f.proj.url, (t) => { t.colorSpace = THREE.SRGBColorSpace; t.flipY = true; t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.generateMipmaps = true; r(t); }, undefined, () => r(null))); }
  if (f.proj && U.uProj.value) { U.uProjVP.value.fromArray(f.proj.vp); U.uProjOn.value = 1; } else U.uProjOn.value = 0;   // V2: chim=false → ảnh vào tấm nền không khói bếp (khói bếp = vật chuyển động, ghép lại từ render)
  LG.farCity.visible = true;
  if (f.mask) { U.uMask.value = f.mask; for (const k in FIRE) { FIRE[k].visible = SMOKE[k].visible = false; } for (const k in GLOW) GLOW[k].visible = false; CHIM.visible = false; R.setRenderTarget(null); R.render(scene, cam); U.uMask.value = 0; CHIM.visible = true;
    const gl = R.getContext(), W = CFG.W, H = CFG.H, px = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const rgb = new Uint8Array(W * H * 3); for (let i = 0, j = 0; i < px.length; i += 4, j += 3) { rgb[j] = px[i]; rgb[j + 1] = px[i + 1]; rgb[j + 2] = px[i + 2]; }
    let bin = ''; for (let i = 0; i < rgb.length; i += 0x8000) bin += String.fromCharCode.apply(null, rgb.subarray(i, i + 0x8000)); return { img: btoa(bin), ms: performance.now() - t0, sun_el: L.el, fire: L.fireSum, mask: true }; }
  R.shadowMap.autoUpdate = false; R.shadowMap.needsUpdate = true;   // bản đồ bóng dựng MỘT lần mỗi khung (không lặp theo mẫu — mặt trời không jitter)
  if (f.refl !== false) renderReflection(); else U.uReflOn.value = 0;
  const spp = f.spp || 4; const tA = performance.now(); pipe.accumulate(scene, cam, spp); const msAcc = performance.now() - tA; const img = pipe.finalize(f.n || 0);
  return { img, ms: performance.now() - t0, ms_acc: msAcc, sun_el: L.el, sun_az: L.az, fire: L.fireSum, view: cam.matrixWorldInverse.elements.slice(), proj: cam.projectionMatrix.elements.slice() };
};
const PROJ = { url: null };
// THU-B D2: nạp atlas vân nướng (mặt tiền 3 hàng × N cột; mái 3 ô) + trung bình tuyến tính từng hàng để hiệu chuẩn albedo
window.setFac = async (fac, roof, n) => { const ld = (u) => new Promise((r) => new THREE.TextureLoader().load(u, (t) => { t.colorSpace = THREE.SRGBColorSpace; t.flipY = false; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 1; r(t); }, undefined, () => r(null)));
  U.tFac.value = await ld(fac); U.tRoof.value = await ld(roof); U.uFacN.value.set(...n.grid); U.uFacMean.value = n.mean.map((c) => V3(...c)); return !!(U.tFac.value && U.tRoof.value); };
window.ready = true;

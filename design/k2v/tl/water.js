// K2V tl · MẶT NƯỚC + TRỜI (lớp 3–4): biển y = 0 (sóng thủ tục, Fresnel phản trời, lấp lánh nắng, sương xa cùng màu chân trời);
// vòm trời chuyển sắc + quầng mặt trời. Không dùng mặt nạ bờ hiện đại → không lộ bờ/kè hiện đại ở năm cũ (đất mới do terrain.js nổi theo năm).
import { THREE, GLSL_NOISE, noiseTex } from './core.js';
// V5b-1b (cổng 16/10 TRƯỢT: trời phẳng, sương trắng đục): trời gradient xanh rõ (chân trời xanh nhạt, KHÔNG trắng) + mây tích thưa thủ tục
// (fbm chiếu lên mặt phẳng mây; mặt sáng ấm theo nắng, đáy xám-xanh), mây nhạt dần về chân trời. Dùng chung cho phản chiếu mặt nước.
export const SKY = `uniform vec3 uSun; uniform vec3 uHor; uniform float uNight; vec3 skyCol(vec3 d){ float h = clamp(d.y, -0.05, 1.0);
  vec3 hor = uHor, zen = vec3(0.13, 0.33, 0.70);   // V5b-2c: màu chân trời là uniform (mặc định như cũ 0,60/0,74/0,90; cảnh khai LOOK.skyHor)
  vec3 c = mix(hor, zen, pow(clamp(h, 0.0, 1.0), 0.50)); float s = max(dot(d, uSun), 0.0);
  c += vec3(1.0, 0.84, 0.58) * (0.16 * pow(s, 10.0) + 0.6 * pow(s, 400.0));
  if (d.y > 0.01) { vec2 q = d.xz / (d.y + 0.06) * 0.9; float n = fbm(q * 1.3 + vec2(3.7, 1.1)), m = fbm(q * 4.1 - 2.3);
    float cov = smoothstep(0.56, 0.74, n * 0.8 + m * 0.25) * smoothstep(0.01, 0.12, d.y);
    vec3 lit = mix(vec3(0.74, 0.79, 0.88), vec3(1.0, 0.97, 0.92), smoothstep(0.45, 0.85, m)) + vec3(0.10, 0.07, 0.02) * pow(s, 4.0);
    c = mix(c, lit, cov * 0.92); }
  c = mix(c, vec3(0.018, 0.030, 0.070) + vec3(0.06, 0.075, 0.11) * pow(1.0 - clamp(h, 0.0, 1.0), 4.0) + vec3(0.02, 0.022, 0.03) * smoothstep(0.62, 0.8, fbm(d.xz / (d.y + 0.06) * 1.3)), uNight);   // V7P: đêm
  return c; }`;
export function makeWaterSky(U, fog, hor = [0.60, 0.74, 0.90], v6 = null) {   // V6: v6 = {refl: true, wave: k} → phản chiếu phẳng (page.js dựng gương) + sóng mạnh hơn
  const sun = { value: U.sunDir }, uHor = { value: new THREE.Vector3(...hor) };
  const water = new THREE.Mesh(new THREE.PlaneGeometry(90000, 90000, 1, 1).rotateX(-Math.PI / 2), new THREE.ShaderMaterial({
    uniforms: { tNoise: { value: noiseTex() }, uBaked: U.uBaked, uSun: sun, uHor, uNight: U.uNight || { value: 0 }, uT: U.uT, uFogD: { value: fog.density }, uFogC: { value: fog.color }, uDim: U.uDim, uExp: { value: 1.0 }, tRefl: { value: null }, uRefl: { value: 0 }, uReflVP: { value: new THREE.Matrix4() }, uWave: { value: v6 ? (v6.wave ?? 1.6) : 1.0 } },
    vertexShader: `varying vec3 vWP; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vWP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform float uT, uFogD, uDim, uBaked, uRefl, uWave; uniform sampler2D tNoise, tRefl; uniform mat4 uReflVP; uniform vec3 uFogC; varying vec3 vWP; ${GLSL_NOISE} ${SKY}
      float fbmT(vec2 p){ if (uBaked < 0.5) return fbm(p); vec2 q = mat2(0.80, -0.60, 0.60, 0.80) * p * 0.173 + 0.37; return 0.6 * texture(tNoise, p * 0.25).g + 0.4 * texture(tNoise, q).a; }
      void main(){ vec3 V = normalize(cameraPosition - vWP); float dist = length(cameraPosition - vWP);
        vec2 p = vWP.xz; float a = smoothstep(4000.0, 200.0, dist);
        vec2 gr = vec2(fbmT(p * 0.045 + vec2(uT * 0.05, 0.0)) - fbmT(p * 0.045 + vec2(0.37, uT * 0.04)), fbmT(p * 0.11 - uT * 0.08) - fbmT(p * 0.11 + 3.1));
        vec3 N = normalize(vec3((gr.x * 0.35 * a + gr.y * 0.12 * a) * uWave, 1.0, (gr.y * 0.35 * a - gr.x * 0.1 * a) * uWave));
        vec3 R = reflect(-V, N); R.y = abs(R.y);
        float F = 0.02 + 0.98 * pow(1.0 - max(dot(N, V), 0.0), 5.0);
        vec3 env = skyCol(R);
        if (uRefl > 0.5) { vec4 cp = uReflVP * vec4(vWP + vec3(N.x, 0.0, N.z) * 14.0 * uWave * min(dist / 120.0, 6.0), 1.0); vec2 ruv = cp.xy / cp.w * 0.5 + 0.5;   // V6: phản chiếu phẳng (vật trên mặt nước), méo theo sóng
          if (ruv.x > 0.0 && ruv.x < 1.0 && ruv.y > 0.0 && ruv.y < 1.0) { vec4 rc = texture2D(tRefl, ruv); env = mix(env, rc.rgb, clamp(rc.a, 0.0, 1.0) * 0.8); } }
        vec3 deep = vec3(0.015, 0.12, 0.22) * (1.0 - 0.85 * uNight), c = mix(deep, env, F);
        c += vec3(1.0, 0.92, 0.75) * pow(max(dot(R, uSun), 0.0), 600.0) * 3.0 * (0.4 + 0.6 * a) * (1.0 - uNight);
        float L = dot(c, vec3(0.299, 0.587, 0.114)); c = mix(c, vec3(L), 0.5 * uDim) * (1.0 - 0.34 * uDim);
        float f = 1.0 - exp(-pow(uFogD * dist, 2.0)); gl_FragColor = vec4(mix(c, uFogC, f), 1.0); }`,
    fog: false }));
  water.renderOrder = 5;   // vẽ SAU địa hình/toà: kiểm tra độ sâu bỏ mảnh nước bị che (bớt vẽ đè)
  const sky = new THREE.Mesh(new THREE.SphereGeometry(60000, 48, 24), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { uSun: sun, uHor, uNight: U.uNight || { value: 0 } }, vertexShader: `varying vec3 vD; void main(){ vD = normalize((modelMatrix * vec4(position, 1.0)).xyz - cameraPosition); gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0); }`,
    fragmentShader: `varying vec3 vD; ${GLSL_NOISE} ${SKY} void main(){ gl_FragColor = vec4(skyCol(normalize(vD)), 1.0); }` }));
  sky.onBeforeRender = (r, s, cam) => sky.position.copy(cam.position);
  sky.renderOrder = 6; sky.material.depthTest = true; sky.frustumCulled = false; water.frustumCulled = false;   // trời vẽ cuối: chỉ lấp điểm ảnh trống
  return { water, sky };
}

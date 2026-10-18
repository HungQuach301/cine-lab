// K2V tl · V6 (V2D-1) · KHÓI GIẢ THỂ TÍCH thay khói sprite phẳng (layers.smoke): cùng vị trí/đường trôi/thời gian/VÙNG KHÓI (luật không người trong khói giữ nguyên),
//  khác ở cách vẽ — mỗi cụm = 2 lớp billboard (lõi đặc nhỏ + vỏ loãng lớn), mật độ = nhiễu fbm cuộn theo tuổi × phẳng dần ở rìa,
//  CHIẾU SÁNG GIẢ THỂ TÍCH: pháp tuyến cầu theo toạ độ trong billboard → mặt hướng nắng sáng (màu nắng của cảnh), mặt khuất nhận ánh trời; tự che đáy cụm;
//  TỐI DẦN theo tuổi và độ cao (khói già dày, xám hơn; khói tàu cháy nâu-đen); lửa: lõi phát sáng HDR (cam → vàng), chỉ ở cụm lửa (≤ 15 % khung đo riêng);
//  sương mù cảnh (FogExp2) áp như vật thể; sắp xếp sau → trước mỗi khung (một lần vẽ instanced). Không vào mặt nạ nội dung / lượt AO (vật liệu không có nhánh uMask).
import { THREE, rng, noiseTex } from './core.js';

const VS = `
  uniform mat4 modelViewMatrix, projectionMatrix, viewMatrix; uniform float uT;
  in vec3 position; in vec2 uv; in vec4 iP; in vec4 iA;   // iP: tâm (thế giới) + cỡ; iA: alpha, tuổi 0..1, loại (0 khói, 1 lửa, 2 khói đen), hạt
  out vec2 vUv; out vec4 vA; out float vDist; out vec3 vWP; out float vRot;
  void main(){ vec4 c = viewMatrix * vec4(iP.xyz, 1.0); float a = iA.w * 6.2831853 + uT * 0.05 * (fract(iA.w * 7.3) - 0.5);
    vec2 q = mat2(cos(a), sin(a), -sin(a), cos(a)) * position.xy; c.xy += q * iP.w; vUv = uv; vA = iA; vDist = -c.z; vWP = iP.xyz; vRot = a;
    gl_Position = projectionMatrix * c; }`;
const FS = `precision highp float;
  uniform sampler2D tNoise; uniform vec3 uSunV, uSunC, uAmb, uFogC; uniform float uFogD, uT; in vec2 vUv; in vec4 vA; in float vDist; in vec3 vWP; in float vRot; out vec4 o;
  void main(){ vec2 p = vUv * 2.0 - 1.0; float r = length(p); if (r > 1.0) discard;
    float age = vA.y, kind = vA.z, sd = vA.w;
    vec2 np = vUv * 0.62 + vec2(sd * 3.7, sd * 1.3) + vec2(0.0, -age * 0.22);
    float nz = 0.56 * texture(tNoise, np).r + 0.3 * texture(tNoise, np * 1.9 + 0.37).g + 0.14 * texture(tNoise, np * 3.6 + 0.71).b;
    // mép "súp lơ": ngưỡng nhiễu theo bán kính (cụm tròn ở tâm, rìa vỡ theo nhiễu); già → loãng và rộng
    float fld = (nz - 0.5) * 1.6 + (1.0 - r) * 1.15 - 0.42 - 0.25 * age;
    float dens = smoothstep(0.0, 0.3, fld) * (0.8 + 0.2 * nz);
    if (dens < 0.004) discard;
    float shape = dens;
    if (kind > 0.5 && kind < 1.5) {   // lửa: lõi phát sáng
      float core = 1.0 - smoothstep(0.0, 0.75, r + (nz - 0.5) * 0.4); vec3 fc = mix(vec3(1.0, 0.32, 0.05), vec3(1.0, 0.78, 0.35), core * core) * (1.2 + 2.2 * core);
      o = vec4(fc, clamp(core * 1.4, 0.0, 1.0) * vA.x); return; }
    // pháp tuyến cầu giả (không gian nhìn; trục billboard đã xoay vRot → xoay ngược để khớp hướng nắng)
    vec2 pr = mat2(cos(-vRot), sin(-vRot), -sin(-vRot), cos(-vRot)) * p; vec2 gN = vec2(dFdx(nz), dFdy(nz)) * 28.0; vec3 n = normalize(vec3(pr * 0.85 - gN, sqrt(max(0.0, 1.0 - r * r)) + 0.2));
    float l = clamp(dot(n, uSunV) * 0.8 + 0.3, 0.0, 1.0), self = 0.7 + 0.3 * clamp(pr.y * 0.5 + 0.5, 0.0, 1.0);
    vec3 alb = kind > 1.5 ? vec3(0.13, 0.115, 0.10) : vec3(0.80, 0.78, 0.74);
    float dark = clamp(age * 0.45 + clamp(vWP.y / 260.0, 0.0, 1.0) * 0.3, 0.0, 0.62); alb *= 1.0 - dark * (kind > 1.5 ? 0.3 : 1.0);
    // tán xạ thuận (khói ngược sáng sáng viền, như khói thật): mạnh khi mặt trời ở phía sau khói (sunV.z < 0), nhiều ở rìa loãng
    float back = pow(max(0.0, -uSunV.z), 2.0), fwd = back * (0.55 + 0.45 * (1.0 - dens));
    vec3 col = alb * (uSunC * (l * self + 1.1 * fwd) + uAmb * 1.5 * (0.75 + 0.25 * n.y));
    float f = 1.0 - exp(-uFogD * uFogD * vDist * vDist); col = mix(col, uFogC, f);
    o = vec4(col, dens * vA.x); }`;

export function smokeV6(specs, ctx) {
  const group = new THREE.Group(), list = [], cap = (specs || []).reduce((a, sp) => a + 2 * (sp.n || 14), 0);
  const geo = new THREE.InstancedBufferGeometry(); const pl = new THREE.PlaneGeometry(1, 1);
  geo.index = pl.index; geo.setAttribute('position', pl.attributes.position); geo.setAttribute('uv', pl.attributes.uv);
  const iP = new THREE.InstancedBufferAttribute(new Float32Array(Math.max(1, cap) * 4), 4), iA = new THREE.InstancedBufferAttribute(new Float32Array(Math.max(1, cap) * 4), 4);
  geo.setAttribute('iP', iP); geo.setAttribute('iA', iA); geo.instanceCount = 0;
  const fog = ctx.scene.fog, U = { tNoise: { value: noiseTex() }, uSunV: { value: new THREE.Vector3(0, 1, 0) }, uSunC: { value: new THREE.Color(1, 1, 1) }, uAmb: { value: new THREE.Color(0.3, 0.32, 0.36) },
    uFogC: { value: fog ? fog.color : new THREE.Color(0.6, 0.7, 0.9) }, uFogD: { value: fog ? fog.density : 0 }, uT: ctx.U.uT };
  const mat = new THREE.RawShaderMaterial({ glslVersion: THREE.GLSL3, vertexShader: VS, fragmentShader: FS, uniforms: U, transparent: true, depthWrite: false, depthTest: true });
  const mesh = new THREE.Mesh(geo, mat); mesh.frustumCulled = false; mesh.renderOrder = 5; group.add(mesh);
  for (const sp of specs || []) { const R = rng(sp.seed || 5), puffs = []; for (let k = 0; k < (sp.n || 14); k++) puffs.push({ ph: R(), fire: !!sp.fire && k < 2, j: [R() - 0.5, R() - 0.5], sd: R(), sd2: R(), k: 0.86 + 0.2 * R() }); list.push({ sp, puffs }); }
  const tmp = [], v = new THREE.Vector3();
  function update(tv) {
    // ánh sáng cảnh → không gian nhìn
    const cam = ctx.cam, sd = ctx.sunDir; if (cam) { cam.updateMatrixWorld(); v.copy(sd).transformDirection(cam.matrixWorldInverse); U.uSunV.value.copy(v); }
    if (ctx.sun) U.uSunC.value.copy(ctx.sun.color).multiplyScalar(ctx.sun.intensity / Math.PI); if (ctx.hemi) U.uAmb.value.copy(ctx.hemi.color).multiplyScalar(ctx.hemi.intensity / Math.PI * 1.1);
    tmp.length = 0;
    for (const { sp, puffs } of list) { const on = tv >= sp.t[0] && tv <= sp.t[1]; if (!on) continue;
      for (const p of puffs) { const per = sp.period || 0.12, age = ((tv - sp.t[0]) / per + p.ph) % 1, sz = (sp.size || 40) * (p.fire ? 0.45 : 0.6 + 1.6 * age), d = sp.drift || [6, 2], life = per * age;
        const x = sp.at[0] + d[0] * life / per * 6 + p.j[0] * sz * 0.6, y = sp.at[1] + (p.fire ? sz * 0.2 : (sp.rise || 60) * age + sz * 0.3), z = -(sp.at[2] + d[1] * life / per * 6 + p.j[1] * sz * 0.6);
        const a = p.fire ? 0.9 * (sp.fire || 0) : Math.min(1, age * 5) * (1 - age) * (sp.alpha ?? 0.85), kind = p.fire ? 1 : sp.dark ? 2 : 0;
        if (p.fire) { tmp.push([x, y, z, sz, a, age, 1, p.sd]); tmp.push([x, y + sz * 0.5, z, sz * 1.3, a * 0.6, Math.min(1, age + 0.3), sp.dark ? 2 : 0, p.sd2]); continue; }
        tmp.push([x, y, z, sz * 1.25, a * 0.45, age, kind, p.sd]);   // vỏ loãng
        tmp.push([x + p.j[1] * sz * 0.2, y - sz * 0.08, z + p.j[0] * sz * 0.2, sz * 0.72, Math.min(1, a * 1.05), age, kind, p.sd2]); } }   // lõi đặc
    if (cam) { const cp = cam.position; tmp.sort((A, B) => ((B[0] - cp.x) ** 2 + (B[1] - cp.y) ** 2 + (B[2] - cp.z) ** 2) - ((A[0] - cp.x) ** 2 + (A[1] - cp.y) ** 2 + (A[2] - cp.z) ** 2)); }
    const n = Math.min(tmp.length, cap); for (let i = 0; i < n; i++) { const q = tmp[i]; iP.setXYZW(i, q[0], q[1], q[2], q[3]); iA.setXYZW(i, q[4], q[5], q[6], q[7]); }
    geo.instanceCount = n; iP.needsUpdate = iA.needsUpdate = true; mesh.visible = n > 0;
  }
  return { group, list, update, v6: true,
    zones(tv) { return list.filter(({ sp }) => tv >= sp.t[0] && tv <= sp.t[1]).flatMap(({ sp }) => {
      if (sp.zone !== 'path') return [{ c: [sp.at[0], sp.at[2]], r: (sp.size || 40) * 2.5 + 30, fire: !!sp.fire }];
      const d = sp.drift || [6, 2], S = sp.size || 40, out = [];
      for (let k = 0; k <= 4; k++) { const a = k / 4, sz = S * (0.6 + 1.6 * a); out.push({ c: [sp.at[0] + d[0] * 6 * a, sp.at[2] + d[1] * 6 * a], r: 0.8 * sz * 1.25 + 2, fire: !!sp.fire && k === 0 }); }   // V6: vỏ loãng 1,25× → vùng nới theo
      if (sp.fire) out.push({ c: [sp.at[0], sp.at[2]], r: S * 0.45 + 2, fire: true });
      return out; }); } };
}

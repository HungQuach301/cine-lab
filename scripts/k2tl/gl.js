// V5b-2b · CHỌN TRÌNH DỰNG WebGL dùng chung cho mọi driver Chromium (scripts/k2tl/render.js, scripts/k2/hero.js, scripts/ll/hero.js) — V5B2A §8 điểm 1 + 8.
//  K2TL_GL = llvmpipe (MẶC ĐỊNH, GG1: Mesa llvmpipe qua ANGLE/EGL) | swiftshader (khung vàng cũ) | vulkan | egl-gpu (công tắc GPU — cờ theo research/gpu/gl_flags.js).
//  Mỗi lượt đọc UNMASKED_RENDERER thật; không đúng trình dựng yêu cầu → in "DỪNG" và thoát MÃ 6 (cờ sai Chromium âm thầm rơi về SwiftShader — GPU-RD §3.2).
//  GPU: renderer phải KHÔNG chứa llvmpipe/SwiftShader (rơi về CPU = dừng, không âm thầm chậm ×10).
//  K2TL_GL_FLAGS='[...]' ghi đè cờ (chỉ để test cơ chế DỪNG).
const CPU = /llvmpipe|SwiftShader/i;
const GLS = {
  llvmpipe: { flags: ['--use-gl=angle', '--use-angle=gl-egl'], ok: (r) => /llvmpipe/i.test(r) },
  swiftshader: { flags: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'], ok: (r) => /SwiftShader/i.test(r) },
  vulkan: { flags: ['--use-angle=vulkan', '--enable-features=Vulkan', '--disable-vulkan-surface', '--enable-gpu-rasterization'], ok: (r) => !!r && !CPU.test(r) },
  'egl-gpu': { flags: ['--use-gl=angle', '--use-angle=gl-egl', '--enable-gpu-rasterization'], ok: (r) => !!r && !CPU.test(r) },
};
function pick(env = process.env) {
  const gl = env.K2TL_GL || 'llvmpipe';
  if (!GLS[gl]) { console.error(`K2TL_GL không hợp lệ: ${gl} (${Object.keys(GLS).join(' | ')})`); process.exit(2); }
  return { gl, flags: env.K2TL_GL_FLAGS ? JSON.parse(env.K2TL_GL_FLAGS) : GLS[gl].flags.slice() };
}
// đọc renderer từ một trang đã có WebGL (canvas tạm, không đụng cảnh)
async function rendererOf(page) {
  return page.evaluate(() => { const c = document.createElement('canvas'), g = c.getContext('webgl2') || c.getContext('webgl'); if (!g) return null;
    const e = g.getExtension('WEBGL_debug_renderer_info'); const r = e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); const lx = g.getExtension('WEBGL_lose_context'); if (lx) lx.loseContext(); return r; });
}
// kiểm; sai → DỪNG mã 6 (đóng trình duyệt trước)
async function assertRenderer(gl, renderer, browser, tag = 'gl') {
  if (GLS[gl].ok(renderer || '')) { console.error(`[${tag}] ${gl} · ${renderer}`); return renderer; }
  console.error(`[${tag}] DỪNG: yêu cầu ${gl} nhưng trình dựng thật là "${renderer}"`); if (browser) await browser.close(); process.exit(6);
}
module.exports = { GLS, pick, rendererOf, assertRenderer, CPU };

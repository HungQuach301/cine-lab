// GPU-RD · in tên trình dựng WebGL thật (UNMASKED_RENDERER) với cờ CINE_GL hiện hành. Thoát 5 nếu vẫn là SwiftShader/llvmpipe khi CINE_GL ≠ swiftshader.
//  CINE_GL=vulkan node -r ./research/gpu/gl_flags.js research/gpu/webgl_probe.js
const { chromium } = require(process.env.CINE_PW || '/opt/pw/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage();
  const r = await p.evaluate(() => { const c = document.createElement('canvas').getContext('webgl2'); if (!c) return { webgl2: false };
    const e = c.getExtension('WEBGL_debug_renderer_info'); return { webgl2: true, vendor: e ? c.getParameter(e.UNMASKED_VENDOR_WEBGL) : c.getParameter(c.VENDOR), renderer: e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER), maxTex: c.getParameter(c.MAX_TEXTURE_SIZE) }; });
  console.log(JSON.stringify(Object.assign({ gl: process.env.CINE_GL || 'swiftshader' }, r)));
  await b.close();
  const soft = !r.webgl2 || /swiftshader|llvmpipe|software|lavapipe/i.test(r.renderer || '');
  if ((process.env.CINE_GL || 'swiftshader') !== 'swiftshader' && soft && !process.env.CINE_ALLOW_SOFT) process.exit(5);
})().catch((e) => { console.error(e); process.exit(1); });

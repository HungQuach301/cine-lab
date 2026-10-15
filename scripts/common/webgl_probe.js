// NỀN TẢNG · dò GPU/WebGL của Chromium headless (Playwright) — phiên Nền tảng 15/10/2026.
//   node scripts/common/webgl_probe.js   → mỗi bộ cờ một dòng: phiên bản WebGL, vendor/renderer thật (WEBGL_debug_renderer_info), MAX_TEXTURE_SIZE
// "SwiftShader" trong renderer = dựng phần mềm trên CPU (không có GPU). GPU thật hiện tên hãng (NVIDIA/AMD/Intel/Apple).
const { chromium } = require('/opt/pw/node_modules/playwright');
(async () => {
  for (const args of [['--disable-gpu'], ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'], ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=vulkan'], ['--enable-gpu', '--ignore-gpu-blocklist', '--use-gl=egl']]) {
    let r; try { const b = await chromium.launch({ args }); const p = await b.newPage();
      r = await p.evaluate(() => { const c = document.createElement('canvas'); const g = c.getContext('webgl2') || c.getContext('webgl'); if (!g) return 'không có WebGL';
        const e = g.getExtension('WEBGL_debug_renderer_info'); return { v: g.getParameter(g.VERSION), vendor: e ? g.getParameter(e.UNMASKED_VENDOR_WEBGL) : '?', renderer: e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : '?', maxTex: g.getParameter(g.MAX_TEXTURE_SIZE) }; });
      await b.close(); } catch (e) { r = 'lỗi: ' + e.message.split('\n')[0]; }
    console.log(JSON.stringify(args), JSON.stringify(r)); }
})();

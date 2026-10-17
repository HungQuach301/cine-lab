// GPU-RD · nạp trước (node -r) để đổi cờ GL của Chromium mà KHÔNG sửa scripts/k2tl/render.js (vùng phiên V).
//  CINE_GL=vulkan|egl|gl|swiftshader  node -r ./research/gpu/gl_flags.js scripts/k2tl/render.js ...
//  CINE_CHANNEL=chromium → dùng Chromium đầy đủ (headless mới) thay headless-shell (đường được Chrome team dùng cho GPU).
// Bọc chromium.launch của đúng bản Playwright mà render.js nạp (/opt/pw/node_modules/playwright, cùng bộ nhớ đệm require).
const PW = process.env.CINE_PW || '/opt/pw/node_modules/playwright';
const { chromium } = require(PW);
const GL = process.env.CINE_GL || 'swiftshader';
const FLAGS = { swiftshader: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  vulkan: ['--use-angle=vulkan', '--enable-features=Vulkan', '--disable-vulkan-surface', '--enable-gpu-rasterization'],
  egl: ['--use-gl=angle', '--use-angle=gl-egl'],
  gl: ['--use-gl=angle', '--use-angle=gl'] };
if (!FLAGS[GL]) throw new Error('CINE_GL không hợp lệ: ' + GL);
const orig = chromium.launch.bind(chromium);
chromium.launch = (opts = {}) => {
  const args = (opts.args || []).filter((a) => !/^--use-angle=|^--use-gl=|^--enable-unsafe-swiftshader/.test(a)).concat(FLAGS[GL]);
  const o = Object.assign({}, opts, { args });
  if (process.env.CINE_CHANNEL) o.channel = process.env.CINE_CHANNEL;
  console.error('[gl_flags]', GL, o.channel || 'headless-shell', args.filter((a) => /angle|gl|Vulkan|swiftshader/.test(a)).join(' '));
  return orig(o);
};

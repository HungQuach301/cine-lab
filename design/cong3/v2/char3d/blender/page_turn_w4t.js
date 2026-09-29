// W4T (Cổng 6, thân Cas): bọc v2/page.js (turnaround/đo C3) với Cas 'bl' + THÂN MPFB + tay MPFB (không sửa trang gốc).
globalThis.CINE_CAS_STYLE = 'bl'; globalThis.CINE_CAS_BODY = 'bl'; globalThis.CINE_HANDS_STYLE = 'bl';
const m = await import('../cast3d.js');
await Promise.all([m.preloadCasBL(), m.preloadCasBodyBL(), m.preloadHandsBL()]);
await import('../../page.js');

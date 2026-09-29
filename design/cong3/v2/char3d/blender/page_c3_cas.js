// W4 · cửa mặt Ida lượt 2 — bọc v2/page.js (turnaround đo C3/B1) với Cas 'bl' (Cổng 6): nạp trước glb rồi mới nạp trang gốc (không sửa trang gốc).
globalThis.CINE_CAS_STYLE = 'bl';
const m = await import('../cast3d.js');
await m.preloadCasBL();
await import('../../page.js');

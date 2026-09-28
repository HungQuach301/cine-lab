// W4 · cửa mặt Ida lượt 2 — bọc design/cong5/mat/page_ai.js (trang studio thử rig của W3) để xem đầu 'bl' dưới đèn studio: nạp trước glb.
// --args như page_ai.js, thêm "idaStyle":"bl".
const m = await import('/cong3/v2/char3d/cast3d.js');
await m.preloadIdaBL();
await import('/cong5/mat/page_ai.js');

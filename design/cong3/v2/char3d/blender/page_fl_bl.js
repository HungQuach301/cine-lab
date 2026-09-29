// W4 · cửa mặt Ida lượt 2 — bọc design/cong5/mat/page_layout_fl.js (khung layout + facelight + phơi sáng của shot, như vòng A-i) với Ida 'bl'.
globalThis.CINE_IDA_STYLE = 'bl';
const m = await import('/cong3/v2/char3d/cast3d.js');
await m.preloadIdaBL();
await import('/cong5/mat/page_layout_fl.js');

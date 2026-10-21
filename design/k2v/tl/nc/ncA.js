// NC-CPU (19/10/2026) · CÁCH A — cảnh t3tl (V7B) + lớp nâng cấp độ thật bề mặt (up.js) + ánh sáng NƯỚNG Cycles (bake.js).
//  Không sửa mã cũ: chỉ import scenes/t3tl.js rồi nâng vật liệu/nội dung sau khi cảnh dựng xong.
//  Gọi: node scripts/k2tl/render.js --scene ../nc/ncA --opt '<opt của shot V7B + nc:{…}>' …   (page.js nạp ./scenes/../nc/ncA.js)
//  opt.nc = { off: true (bỏ lớp nâng cấp; sương e^(−σd) của up.js vẫn nạp) | bake: '<thư mục /cache/nc/bake/…>' | bushes: false | water: false | haze: false | tex: false }
import * as T3 from '../scenes/t3tl.js';
import { preBuild, postBuild } from './up.js';

export const TERRAIN = T3.TERRAIN;
export const GRADE = T3.GRADE;
export const V6 = T3.V6;
export const META = Object.assign({}, T3.META, { nc: 'A' });
export const LOOK = T3.LOOK;   // sương / màu sương đặt trong postBuild (page.js đọc lại scene.fog ở khung đầu)

export async function build(ctx) {
  const P = Object.assign({}, (ctx.opt && ctx.opt.nc) || {});
  if (P.off) { const SC0 = await T3.buildCore(ctx); return SC0; }
  const pre = await preBuild(ctx, P);
  const SC = await T3.buildCore(ctx);   /* V7C: t3tl.build tự bọc khi có opt.nc → gọi lõi để không bọc hai lần */
  const post = await postBuild(ctx, SC, P, pre);
  const apply0 = SC.apply;
  SC.apply = (st, t) => { apply0(st, t); post.update(st, t); };
  SC.meta = Object.assign({}, SC.meta, { nc: post.meta });
  globalThis.NC = { ctx, SC, post };   // tay cầm cho driver NC (design/pt/cpu/nc_topo.js: albedo nhìn thẳng xuống cho Blender)
  return SC;
}

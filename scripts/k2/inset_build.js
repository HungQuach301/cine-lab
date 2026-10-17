// V5b-2b (AD3) · DỮ LIỆU BẢN ĐỒ ĐỊNH VỊ GÓC (inset) — đường bờ Natural Earth 1:50m (world-atlas land-50m, public domain; RIGHTS K2V-MAP-1), KHÔNG có ranh giới quốc gia
// (ranh giới hiện đại sai thời kỳ; ranh giới lịch sử chỉ vẽ khi shot khai inset_bien = GeoJSON có nguồn). Chiếu phương trụ đều, hệ số cos(vĩ độ giữa) → toạ độ 0..1 trong hộp.
//   node scripts/k2/inset_build.js <tên> <lon0> <lat0> <lon1> <lat1>     → design/k2v/inset/<tên>.json
const fs = require('fs'), path = require('path');
const topo = require(path.join(__dirname, '../../design/k2v/node_modules/topojson-client'));
const [name, lo0, la0, lo1, la1] = [process.argv[2], ...process.argv.slice(3, 7).map(Number)];
const T = JSON.parse(fs.readFileSync(path.join(__dirname, '../../design/k2v/node_modules/world-atlas/land-50m.json'), 'utf8'));
const land = topo.feature(T, T.objects.land), k = Math.cos(((la0 + la1) / 2) * Math.PI / 180);
const W = (lo1 - lo0) * k, H = la1 - la0, P = ([lo, la]) => [((lo - lo0) * k) / W, (la1 - la) / H];
const pad = 0.15, inBox = ([x, y]) => x > -pad && x < 1 + pad && y > -pad && y < 1 + pad;
const rings = [];
for (const poly of land.features.flatMap((f) => (f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates))) {
  for (const r of poly) { const q = r.map(P); if (!q.some(inBox)) continue;
    // chỉ giữ đoạn trong hộp nới (ngoài hộp nới thay bằng điểm biên đầu/cuối: canvas cắt theo khung nên không lộ cạnh giả), rồi lược điểm < 0,0015
    const out = []; let last = null; for (const p of q) { const c = [Math.max(-pad, Math.min(1 + pad, p[0])), Math.max(-pad, Math.min(1 + pad, p[1]))];
      if (!last || Math.hypot(c[0] - last[0], c[1] - last[1]) > 0.0015) { out.push([+c[0].toFixed(4), +c[1].toFixed(4)]); last = c; } }
    if (out.length > 3) rings.push(out); }
}
const o = { name, box: [lo0, la0, lo1, la1], aspect: +(W / H).toFixed(4), proj: 'equirect cos(lat_mid)', src: 'Coast: Natural Earth 1:50m (public domain)', rings };
fs.mkdirSync(path.join(__dirname, '../../design/k2v/inset'), { recursive: true });
fs.writeFileSync(path.join(__dirname, `../../design/k2v/inset/${name}.json`), JSON.stringify(o));
console.log(JSON.stringify({ name, aspect: o.aspect, rings: rings.length, pts: rings.reduce((s, r) => s + r.length, 0), bytes: JSON.stringify(o).length }));

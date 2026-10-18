// K2V tl · V5b-2b (M6) · MẶT TRỜI THEO THIÊN VĂN + BỘ ĐẾM NGÀY/GIỜ. Thuần JS (test Node: scripts/k2tl/tests/test_sun.mjs).
//  Vị trí mặt trời: thuật toán NOAA (Meeus rút gọn; sai số < 0,1° trong 1700–2100) — độ cao + phương vị tại vĩ/kinh độ cảnh.
//  Giờ trong nguồn thế kỷ 18 ("09:45", 13/9/1782) là GIỜ ĐỊA PHƯƠNG trung bình (chưa có múi giờ): UTC = giờ địa phương − kinh độ/15.
//  Hiện đại: tz (giờ) khai rõ. Lịch: N.S. (Gregory) mặc định; O.S. (Julius) cho nguồn Anh trước 14/9/1752 — hai lịch hiện cạnh nhau.
export const GIB = { lat: 36.14, lon: -5.35 };   // Gibraltar (36,14° B) — TIEN-KY-VAY-HAM §5 M6
const RAD = Math.PI / 180;
// ngày Julius (JD) của lịch GREGORY (N.S.) lúc UTC
export function jdOf(y, mo, d, hUTC = 0) { if (mo <= 2) { y -= 1; mo += 12; } const A = Math.floor(y / 100), B = 2 - A + Math.floor(A / 4);
  return Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (mo + 1)) + d + B - 1524.5 + hUTC / 24; }
// JD của lịch JULIUS (O.S.)
export function jdJulian(y, mo, d, hUTC = 0) { if (mo <= 2) { y -= 1; mo += 12; } return Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (mo + 1)) + d - 1524.5 + hUTC / 24; }
// JD → ngày lịch (gregory: true → N.S.; false → O.S.)
export function calOf(jd, gregory = true) { const Z = Math.floor(jd + 0.5); let A = Z; if (gregory) { const al = Math.floor((Z - 1867216.25) / 36524.25); A = Z + 1 + al - Math.floor(al / 4); }
  const B = A + 1524, C = Math.floor((B - 122.1) / 365.25), D = Math.floor(365.25 * C), E = Math.floor((B - D) / 30.6001);
  const d = B - D - Math.floor(30.6001 * E), mo = E < 14 ? E - 1 : E - 13, y = mo > 2 ? C - 4716 : C - 4715; return { y, mo, d }; }
// độ cao (°) + phương vị (° từ Bắc, theo chiều kim đồng hồ) của mặt trời
export function sunPos(jd, lat = GIB.lat, lon = GIB.lon) {
  const T = (jd - 2451545) / 36525, L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360, M = 357.52911 + T * (35999.05029 - 0.0001537 * T), e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T);
  const C = Math.sin(M * RAD) * (1.914602 - T * (0.004817 + 0.000014 * T)) + Math.sin(2 * M * RAD) * (0.019993 - 0.000101 * T) + Math.sin(3 * M * RAD) * 0.000289;
  const lam = L0 + C - 0.00569 - 0.00478 * Math.sin((125.04 - 1934.136 * T) * RAD), eps0 = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60, eps = eps0 + 0.00256 * Math.cos((125.04 - 1934.136 * T) * RAD);
  const dec = Math.asin(Math.sin(eps * RAD) * Math.sin(lam * RAD)), y = Math.tan(eps * RAD / 2) ** 2;
  const Et = 4 / RAD * (y * Math.sin(2 * L0 * RAD) - 2 * e * Math.sin(M * RAD) + 4 * e * y * Math.sin(M * RAD) * Math.cos(2 * L0 * RAD) - 0.5 * y * y * Math.sin(4 * L0 * RAD) - 1.25 * e * e * Math.sin(2 * M * RAD));   // phút
  const utcMin = ((jd + 0.5) % 1) * 1440, tst = (utcMin + Et + 4 * lon + 1440) % 1440, ha = tst / 4 - 180;
  const cz = Math.sin(lat * RAD) * Math.sin(dec) + Math.cos(lat * RAD) * Math.cos(dec) * Math.cos(ha * RAD), zen = Math.acos(Math.max(-1, Math.min(1, cz)));
  let az = Math.acos(Math.max(-1, Math.min(1, (Math.sin(lat * RAD) * Math.cos(zen) - Math.sin(dec)) / (Math.cos(lat * RAD) * Math.sin(zen))))) / RAD; az = ha > 0 ? (az + 180) % 360 : (540 - az) % 360;   // NOAA: từ Bắc, chiều kim đồng hồ
  return { el: 90 - zen / RAD, az, dec: dec / RAD, eqt_min: Et };
}
// giờ địa phương (LMT, thế kỷ 18) hoặc giờ theo múi tz → JD UTC
export const jdLocal = (y, mo, d, hLocal, { tz = null, lon = GIB.lon, julian = false } = {}) => (julian ? jdJulian : jdOf)(y, mo, d, hLocal - (tz == null ? lon / 15 : tz));
// hướng mặt trời trong toạ độ cảnh (x = Đông, y = cao, z = −Bắc) — như page.js sunDir
export function sunDirENU(p) { const el = p.el * RAD, az = p.az * RAD; return [Math.sin(az) * Math.cos(el), Math.sin(el), -Math.cos(az) * Math.cos(el)]; }
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const pad = (n) => String(n).padStart(2, '0');
// bộ đếm: JD (UTC) → "13 Sep 1782 · 09:45" theo giờ địa phương; dual: thêm dòng hai lịch "O.S. 24 Jul · N.S. 4 Aug 1704"
export function clockLabel(jdUTC, { tz = null, lon = GIB.lon, dual = false, time = true } = {}) {
  const jl = jdUTC + (tz == null ? lon / 15 : tz) / 24, ns = calOf(jl, true), os = calOf(jl, false), mins = Math.round(((jl + 0.5) % 1) * 1440) % 1440;
  const s = `${ns.d} ${MON[ns.mo - 1]} ${ns.y}` + (time ? ` · ${pad(Math.floor(mins / 60))}:${pad(mins % 60)}` : '');
  return { s, sub: dual ? `O.S. ${os.d} ${MON[os.mo - 1]}${os.y !== ns.y ? ' ' + os.y : ''} · N.S. ${ns.d} ${MON[ns.mo - 1]} ${ns.y}` : null, ns, os, mins };
}

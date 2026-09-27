"""Nhóm N — kỹ thuật file: N1 (24 fps CFR theo PTS), N2 (BT.709, dải limited), N3 (codec, bitrate)."""
import numpy as np

from .common import (FAIL, NA, metric, not_applicable, packets, probe, read_luma, result, stream, frac)

FPS = 24
TOL_S = 0.0005


def check_n1(path, profile):
    info = probe(path)
    v = stream(info, "video")
    if v is None:
        return result("N1", FAIL, notes=["Không có luồng video."])
    r = frac(v.get("r_frame_rate"))
    a = frac(v.get("avg_frame_rate"))
    pts = sorted(p for p, _ in packets(path))
    d = np.diff(np.array(pts)) if len(pts) > 1 else np.array([])
    step = 1.0 / FPS
    dup = int(np.sum(np.abs(d) < 1e-9))
    gaps = int(np.sum(d > 1.5 * step))
    irregular = int(np.sum(np.abs(d - step) > TOL_S))
    ev = {"so_khung": len(pts)}
    if irregular:
        bad = np.where(np.abs(d - step) > TOL_S)[0][:20]
        ev["vi_tri_lech_dau_tien"] = [dict(khung=int(i), pts=round(pts[i], 4), buoc_s=round(float(d[i]), 5))
                                      for i in bad]
    ms = [
        metric("r_frame_rate", round(r, 4) if r else None, "==", float(FPS), "fps"),
        metric("avg_frame_rate", round(a, 4) if a else None, "==", float(FPS), "fps"),
        metric("bước PTS lệch khỏi 1/24 s > 0,5 ms", irregular, "<=", 0, "bước"),
        metric("PTS trùng (lặp khung)", dup, "<=", 0, "khung"),
        metric("khoảng hở PTS (rơi khung)", gaps, "<=", 0, "chỗ"),
    ]
    return result("N1", None, ms, evidence=ev)


def check_n2(path, profile):
    info = probe(path)
    v = stream(info, "video")
    if v is None:
        return result("N2", FAIL, notes=["Không có luồng video."])
    ms = [
        metric("color_primaries", v.get("color_primaries", "(không có)"), "==", "bt709"),
        metric("color_transfer", v.get("color_transfer", "(không có)"), "==", "bt709"),
        metric("color_space", v.get("color_space", "(không có)"), "==", "bt709"),
        metric("color_range", v.get("color_range", "(không có)"), "==", "tv"),
    ]
    frames, depth = read_luma(path)
    scale = 2 ** (depth - 8)
    lo, hi = 16 * scale, 235 * scale
    total = sum(f.size for _, f in frames)
    out = sum(int(np.sum((f < lo) | (f > hi))) for _, f in frames)
    pct = 100.0 * out / total if total else 0.0
    ms.append(metric("luma ngoài dải limited", pct, "<=", 0.5, "%"))
    return result("N2", None, ms, evidence={"khung_lay_mau": len(frames), "bit_depth": depth})


YT_VIDEO = {"h264": {"High", "High 10"}, "hevc": {"Main", "Main 10"}}
ARCH_VIDEO = {"prores": {"HQ", "4444", "4444XQ"}, "dnxhd": {"DNXHR HQ", "DNXHR HQX", "DNXHR 444"},
              "ffv1": None}


def check_n3(path, profile):
    if profile not in ("youtube", "archive"):
        return not_applicable("N3", "N3 chỉ áp cho master (--profile youtube hoặc archive).")
    info = probe(path)
    v = stream(info, "video")
    a = stream(info, "audio")
    if v is None:
        return result("N3", FAIL, notes=["Không có luồng video."])
    w, h = int(v["width"]), int(v["height"])
    sar = v.get("sample_aspect_ratio", "1:1")
    pk = packets(path)
    dur = (max(p for p, _ in pk) - min(p for p, _ in pk) + 1.0 / FPS) if pk else 0
    vbr = sum(s for _, s in pk) * 8 / dur / 1e6 if dur else 0.0
    codec, prof = v.get("codec_name"), v.get("profile", "")
    ms = [
        metric("tỷ lệ khung", round(w / h, 4), "==", round(16 / 9, 4)),
        metric("SAR", sar if sar not in ("0:1", "N/A") else "1:1", "==", "1:1"),
    ]
    notes = []
    if profile == "youtube":
        ok_codec = codec in YT_VIDEO and prof in YT_VIDEO[codec]
        ms.append(metric("codec/profile hình", f"{codec}/{prof}", "==", "h264/High | hevc/Main(10)")
                  | {"ok": ok_codec})
        ms.append(metric("pix_fmt", v.get("pix_fmt"), "==", "yuv420p | yuv420p10le")
                  | {"ok": v.get("pix_fmt") in ("yuv420p", "yuv420p10le")})
        ms.append(metric("kích thước", f"{w}x{h}", "==", "1920x1080 | 3840x2160")
                  | {"ok": (w, h) in ((1920, 1080), (3840, 2160))})
        need = 45.0 if h >= 2160 else 12.0
        ms.append(metric("bitrate hình đo từ gói", vbr, ">=", need, "Mbps"))
        if a is None:
            ms.append(metric("luồng âm", "(không có)", "==", "aac") | {"ok": False})
        else:
            apk = packets(path, "a:0")
            adur = (max(p for p, _ in apk) - min(p for p, _ in apk)) if len(apk) > 1 else 0
            abr = sum(s for _, s in apk) * 8 / adur / 1e3 if adur else 0.0
            ms.append(metric("codec âm", f"{a.get('codec_name')}/{a.get('profile', '')}", "==", "aac/LC")
                      | {"ok": a.get("codec_name") == "aac" and a.get("profile") == "LC"})
            ms.append(metric("tần số lấy mẫu âm", int(a.get("sample_rate", 0)), "==", 48000, "Hz"))
            ms.append(metric("số kênh âm", int(a.get("channels", 0)), "==", 2))
            notes.append(f"Bitrate âm đo từ gói: {abr:.0f} kbps (tham khảo, không làm ngưỡng: bộ mã AAC "
                         "dùng ít bit hơn mức đặt khi nội dung đơn giản, nên con số này không đo chất lượng).")
    else:
        allowed = ARCH_VIDEO.get(codec, "x")
        ok_codec = codec in ARCH_VIDEO and (allowed is None or prof in allowed)
        ms.append(metric("codec/profile hình", f"{codec}/{prof}", "==",
                         "prores HQ/4444/4444XQ | dnxhr HQ/HQX/444 | ffv1") | {"ok": ok_codec})
        ms.append(metric("chiều cao", h, ">=", 1080, "px"))
        if a is None:
            ms.append(metric("luồng âm", "(không có)", "==", "pcm") | {"ok": False})
        else:
            bits = int(a.get("bits_per_raw_sample") or a.get("bits_per_sample") or 0)
            ms.append(metric("codec âm", a.get("codec_name"), "==", "pcm_*")
                      | {"ok": str(a.get("codec_name", "")).startswith("pcm_")})
            ms.append(metric("độ sâu bit âm", bits, ">=", 24, "bit"))
            ms.append(metric("tần số lấy mẫu âm", int(a.get("sample_rate", 0)), ">=", 48000, "Hz"))
        notes.append(f"Bitrate hình đo: {vbr:.1f} Mbps (tham khảo).")
    return result("N3", None, ms, notes)

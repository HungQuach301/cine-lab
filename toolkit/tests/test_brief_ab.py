"""toolkit/market/brief.py ab — brief thumbnail A/B theo mẫu TEARDOWN-FON §9 (V5a, 15/10/2026). Không gọi mạng, không gọi AI.
Chạy: /opt/cine/bin/python -m unittest toolkit/tests/test_brief_ab.py -v"""
import shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "market"))
import brief  # noqa: E402

BASE = ["--ep", "k2x-01", "--title", "Why Did a Rock With No Farmland Get Rich?",
        "--colors", "A=#2e8b57,B=#c0392b",
        "--a-subject", "Gibraltar and La Línea on our relief map, the two sides tinted", "--a-text", "6.8 KM²",
        "--a-contrast", "vạch chia dọc ở hàng rào biên giới", "--a-text-colors", "#ffffff/#111111",
        "--b-subject", "the Rock in cross-section: tunnels and reservoirs inside", "--b-contrast", "mặt cắt lộ đường hầm"]


class BriefAB(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="brief-ab-"))
        self.claims = self.tmp / "claims.txt"; self.claims.write_text("6.8\n")

    def tearDown(self): shutil.rmtree(self.tmp, ignore_errors=True)

    def run_ab(self, *extra, base=BASE):
        rc = brief.main(["ab", *base, "--claims", str(self.claims), "--out", str(self.tmp), *extra])
        p = self.tmp / "THUMBNAIL-BRIEF-AB.md"
        return rc, (p.read_text() if p.exists() else "")

    def test_good_brief(self):
        rc, md = self.run_ab()
        self.assertEqual(rc, 0)
        for s in ("[A] BẢN ĐỒ TƯƠNG PHẢN", "[B] CƠ CHẾ LỘ RA", "| Chủ thể |", "| Chữ (≤ 4 từ) |", "| Tương phản |", "| Tham chiếu ngách |",
                  "KHÔNG CHỮ", "18.88:1", "Test & Compare", "A #2e8b57"):
            self.assertIn(s, md)
        self.assertIn("- Tiêu đề: ĐẠT", md); self.assertIn("- Phương án A: ĐẠT", md); self.assertIn("- Phương án B: ĐẠT", md)

    def test_text_over_4_words(self):
        b = BASE.copy(); b[b.index("--a-text") + 1] = "ONE TWO THREE FOUR FIVE"
        rc, md = self.run_ab(base=b)
        self.assertEqual(rc, 0)                                  # đọc, không chặn
        self.assertIn("chữ 5 từ (> 4)", md)

    def test_low_contrast_and_unclaimed_number(self):
        b = BASE.copy(); b[b.index("--a-text-colors") + 1] = "#777777/#888888"; b[b.index("--a-text") + 1] = "73% RICHER"
        _, md = self.run_ab(base=b)
        self.assertIn("< 4,5:1", md); self.assertIn("số '73%' không có", md)

    def test_b_with_text_and_wrong_device(self):
        _, md = self.run_ab("--b-text", "WHY", "--b-contrast", "màu đẹp")
        self.assertIn("KHÔNG chữ cho ngữ pháp B", md); self.assertIn("thủ pháp tương phản nên là", md)

    def test_title_rules_and_repeat(self):
        b = BASE.copy(); b[b.index("--title") + 1] = "The Secret Story of How Gibraltar Became So Rich While Spain Stayed Poor"
        b[b.index("--a-text") + 1] = "GIBRALTAR RICH"
        _, md = self.run_ab(base=b)
        self.assertIn("> 60", md); self.assertIn("không mở bằng", md); self.assertIn("secret", md); self.assertIn("chữ lặp tiêu đề", md)

    def test_same_subject_stops(self):
        b = BASE.copy(); b[b.index("--b-subject") + 1] = b[b.index("--a-subject") + 1]
        rc, md = self.run_ab(base=b)
        self.assertEqual(rc, 2); self.assertEqual(md, "")

    def test_contrast_ratio(self):
        self.assertEqual(brief.contrast_ratio("#ffffff", "#000000"), 21.0)
        self.assertEqual(brief.contrast_ratio("#000000", "#ffffff"), 21.0)

    def test_legacy_cli_untouched(self):
        # CLI cũ (PACKAGING-BRIEF) vẫn là nhánh mặc định khi không có "ab"; ca đầy đủ ở test_market.TestBrief
        with self.assertRaises(SystemExit):
            brief.main(["--ep", "x"])                        # thiếu tham số bắt buộc của CLI cũ → argparse thoát


if __name__ == "__main__":
    unittest.main()

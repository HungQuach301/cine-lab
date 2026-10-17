"""scripts/common/release_check.py — ca giả (self-test) + chạy thử trên gói thật Steel và T1 (V5a, 15/10/2026).
Chạy: /opt/cine/bin/python -m unittest scripts/common/tests/test_release_check.py -v"""
import io, contextlib, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/common'))
import release_check as rc  # noqa: E402

codes = lambda r: sorted({x['ma'] for x in r['loi']})


class SelfTest(unittest.TestCase):
    def test_self_test(self):
        with contextlib.redirect_stdout(io.StringIO()): self.assertTrue(rc.self_test())

    def test_title_60_ok_61_fail(self):
        d = "Why is it 3?\nThis video explains how the system works. It isn't financial or investment advice.\n"
        self.assertNotIn('R1', {a for a, _ in rc.check(d, [('C', 'x' * 60)], 'https://e.org')[0]})
        self.assertIn('R1', {a for a, _ in rc.check(d, [('C', 'x' * 61)], 'https://e.org')[0]})

    def test_desc_5000_ok(self):
        d = "Why is it 3?\nThis video explains how the system works. It isn't financial or investment advice.\n"
        self.assertNotIn('R2', {a for a, _ in rc.check(d + 'x' * (5000 - len(d)), [('C', 'T')], 'https://e.org')[0]})

    def test_parse_titles_skips_rejected(self):
        t = rc.parse_titles('CHÍNH: A b (3 ký tự)\nDỰ PHÒNG (Test & Compare): C d (3 ký tự)\nLOẠI (x): E\nPHƯƠNG ÁN 3 (không dùng): F\n')
        self.assertEqual(t, [('CHÍNH', 'A b'), ('DỰ PHÒNG (Test & Compare)', 'C d')])

    def test_update_inserted_after_disclaimer(self):
        d = "Hook?\nThis video explains how the system works. It isn't financial or investment advice.\n\nCHAPTERS\n"
        self.assertEqual(rc.insert_update(d, 'UPD').splitlines()[2], 'UPD')


class RealPackages(unittest.TestCase):
    def test_steel_5502_is_error(self):
        r = rc.run(str(ROOT / 'channel-k2/k2g-ep01/phat-hanh'))
        self.assertEqual(r['so_do']['desc_chars'], 5502)
        self.assertTrue(any(x['ma'] == 'R2' and '5502' in x['chi_tiet'] for x in r['loi']))
        self.assertEqual(codes(r), ['R1', 'R2', 'R3', 'R6'])   # R1: tiêu đề dự phòng 70; R3: miễn trừ ở dòng 1; R6: chưa có bình luận ghim
        self.assertEqual(r['ket_qua'], 'TRƯỢT')

    def test_t1(self):
        r = rc.run(str(ROOT / 'channel-k2/k2c-t1-06/phat-hanh'))
        self.assertEqual(codes(r), ['R1', 'R3'])   # tiêu đề chính 63; miễn trừ ở dòng 1 (luật trước 15/10)
        self.assertLessEqual(r['so_do']['desc_chars'], 5000)
        self.assertGreater(r['so_do']['pinned_urls'], 20)


if __name__ == '__main__':
    unittest.main()

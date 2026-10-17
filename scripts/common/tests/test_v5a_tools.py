"""V5a (15/10/2026): lut.py, cc0_fetch.py (phần offline), versions.py (nhóm mới không làm lệch bản ghi cũ).
Chạy: /opt/cine/bin/python -m unittest scripts/common/tests/test_v5a_tools.py -v   (không gọi mạng)"""
import contextlib, hashlib, io, json, os, shutil, sys, tempfile, unittest
from pathlib import Path
import numpy as np

COMMON = Path(__file__).resolve().parents[1]; ROOT = COMMON.parents[1]
sys.path.insert(0, str(COMMON))
import lut, cc0_fetch as cc, versions  # noqa: E402


class Lut(unittest.TestCase):
    def test_self_test(self):
        with contextlib.redirect_stdout(io.StringIO()): self.assertTrue(lut.self_test())

    def test_committed_cubes_match_formula(self):
        """LUT đã commit = đúng công thức trong lut.py (sinh lại so từng giá trị)."""
        for name in lut.CANDIDATES:
            p = ROOT / 'assets/k2/lut' / f'{name}.cube'
            n, T = lut.read_cube(str(p)); rgb, _ = lut.build(name)
            self.assertEqual(n, lut.N); self.assertLess(np.abs(T - rgb).max(), 2e-6, name)

    def test_locked_luts_keep_identity_colours(self):
        for name, (_, lock) in lut.CANDIDATES.items():
            fid, cr = lut.fidelity(str(ROOT / 'assets/k2/lut' / f'{name}.cube'))
            if lock: self.assertLessEqual(max(fid.values()), 1.0, name); self.assertGreaterEqual(cr, 7.0)

    def test_wcag(self):
        self.assertAlmostEqual(lut.wcag(lut.hex2rgb('#EEF1F4'), lut.hex2rgb('#0F1722')), 15.9, delta=0.05)   # NHAN-DIEN §2


class CC0Offline(unittest.TestCase):
    def test_redact(self):
        self.assertEqual(cc.redact('contact a.b' + '@' + 'mail.test now'), 'contact [email đã ẩn] now')

    def test_html_text(self):
        t = cc.html_text(b'<html><head><title>x</title></head><body><p>CC0 <b>1.0</b></p><script>var a=1;</script><p>Public&nbsp;Domain</p></body></html>')
        self.assertIn('CC0 1.0', t); self.assertIn('Public Domain', t); self.assertNotIn('var a', t)

    def test_drive_regex(self):
        page = (r'\x22AAAAAAAAAAAAAAAAAAAAAAAAA\x22,\x5b\x22ROOTROOTROOTROOTROOTROOT1\x22\x5d,\x22OBJ\x22,\x22application\/vnd.google-apps.folder\x22,'
                r'\x22BBBBBBBBBBBBBBBBBBBBBBBBB\x22,\x5b\x22ROOTROOTROOTROOTROOTROOT1\x22\x5d,\x22License.txt\x22,\x22text\/plain\x22')
        orig = cc.http; cc.http = lambda url, out=None, timeout=300: page.encode()
        try: L = cc.drive_ls('ROOTROOTROOTROOTROOTROOT1')
        finally: cc.http = orig
        self.assertEqual([x[1] for x in L], ['OBJ', 'License.txt']); self.assertEqual(L[0][2], 'application/vnd.google-apps.folder')

    def test_gitattributes_and_verify(self):
        d = Path(tempfile.mkdtemp(prefix='cc0-')); self.addCleanup(shutil.rmtree, d, True)
        (d / 'licenses').mkdir(); (d / 'licenses/x.txt').write_text('CC0')
        big, small = d / 'src/a b.bin', d / 'src/s.txt'; big.parent.mkdir(); big.write_bytes(b'\0' * (cc.LFS_MIN + 1)); small.write_text('x')
        f = lambda p: dict(path=str(p.relative_to(d)), url='u', sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size, lfs=p.stat().st_size > cc.LFS_MIN)
        cat = dict(items=[dict(id='t', tep_giay_phep='licenses/x.txt', files=[f(big), f(small)])])
        (d / 'catalog.json').write_text(json.dumps(cat)); cc.gitattributes(str(d), cat)
        ga = (d / '.gitattributes').read_text(); self.assertIn('src/a\\ b.bin filter=lfs', ga); self.assertNotIn('s.txt', ga)
        with contextlib.redirect_stdout(io.StringIO()): self.assertTrue(cc.verify(str(d)))
        small.write_text('y')
        with contextlib.redirect_stdout(io.StringIO()): self.assertFalse(cc.verify(str(d)))

    def test_catalog_committed(self):
        cat = json.loads((ROOT / 'assets/k2/cc0/catalog.json').read_text())
        self.assertTrue(15 <= len(cat['items']) <= 25); self.assertLessEqual(cat['tong_bytes'], cc.MAX_TOTAL); self.assertEqual(cat['chan'], [])
        need = {'tàu', 'cần cẩu', 'container', 'nhà máy', 'nhà ở', 'biên giới', 'xe tải', 'tàu hỏa'}
        self.assertTrue(need <= {i['chu_de'] for i in cat['items']})
        for i in cat['items']:
            self.assertTrue((ROOT / 'assets/k2/cc0' / i['tep_giay_phep']).exists(), i['id'])
            for x in i['files']: self.assertEqual(len(x['sha256']), 64); self.assertGreater(x['bytes'], 0)


class Versions(unittest.TestCase):
    def test_new_groups_do_not_break_old_records(self):
        A = dict(checks=dict(version='1', tree_sha256='t', lock_verify='KHỚP'), tools={'ffmpeg': '6'},
                 toolkit={'k2v': dict(tree_sha256='h', commit='c')})
        B = dict(checks=dict(version='1', tree_sha256='t', lock_verify='KHỚP'), tools={'ffmpeg': '6', 'git_lfs': '3.4.1', 'opencv': '5.0.0'},
                 toolkit={'k2v': dict(tree_sha256='h', commit='c'), 'common': dict(tree_sha256='x', commit='y'), 'assets_k2': dict(tree_sha256='z', commit='w')})
        self.assertEqual(versions.compare(A, B), [])

    def test_groups_present(self):
        for g in ('common', 'market', 'assets_k2'): self.assertIn(g, versions.GROUPS)
        h, n = versions.tree_hash(versions.GROUPS['assets_k2']); self.assertEqual(n, 4)   # catalog.json + 3 LUT


if __name__ == '__main__':
    unittest.main()

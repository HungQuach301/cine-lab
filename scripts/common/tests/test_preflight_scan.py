"""scripts/common/preflight_scan.py — P5 không bắt nhầm licenses/… nằm trong URL (V5a, 15/10/2026).
Chạy: /opt/cine/bin/python -m unittest scripts/common/tests/test_preflight_scan.py -v
Ca tích hợp dựng một repo git tạm (chép preflight_scan.py vào), stage sổ footage rồi chạy --staged; không chạm repo thật."""
import os, shutil, subprocess, sys, tempfile, textwrap, unittest
from pathlib import Path

COMMON = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COMMON))
import preflight_scan as ps  # noqa: E402

PY = sys.executable


class LicenseRefs(unittest.TestCase):
    def test_path_alone(self):
        self.assertEqual(ps.license_refs('licenses/c01.txt'), ['licenses/c01.txt'])

    def test_path_after_text(self):
        self.assertEqual(ps.license_refs('PD; xem licenses/c01.txt, licenses/c01-b.txt'), ['licenses/c01.txt', 'licenses/c01-b.txt'])

    def test_dot_slash(self):
        self.assertEqual(ps.license_refs('./licenses/c01.txt'), ['licenses/c01.txt'])

    def test_url_not_path(self):
        for u in ['http://creativecommons.org/licenses/publicdomain/', 'https://creativecommons.org/licenses/by/4.0/',
                  'CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/legalcode)', 'example.org/licenses/x.txt']:
            self.assertEqual(ps.license_refs(u), [], u)

    def test_url_and_path(self):
        self.assertEqual(ps.license_refs('https://creativecommons.org/licenses/by/4.0/ → licenses/c02.txt'), ['licenses/c02.txt'])

    def test_word_prefix(self):
        self.assertEqual(ps.license_refs('mylicenses/x.txt'), [])


class P5Integration(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix='pf-test-'))
        (self.d / 'scripts/common').mkdir(parents=True)
        shutil.copy(COMMON / 'preflight_scan.py', self.d / 'scripts/common/')
        (self.d / 'tools').mkdir(); (self.d / 'tools/lfs-allow.txt').write_text('*-master.mp4\n')
        self.ep = self.d / 'ep'; (self.ep / 'licenses').mkdir(parents=True)
        g = lambda *a: subprocess.run(['git', *a], cwd=self.d, check=True, capture_output=True)
        g('init', '-q'); g('config', 'user.email', 'noreply@anthropic.com'); g('config', 'user.name', 't')
        self.g = g

    def tearDown(self): shutil.rmtree(self.d, ignore_errors=True)

    def run_scan(self, csv_text):
        (self.ep / 'SOURCES-FOOTAGE.csv').write_text(textwrap.dedent(csv_text))
        self.g('add', '-A')
        return subprocess.run([PY, 'scripts/common/preflight_scan.py', '--staged'], cwd=self.d, capture_output=True, text=True)

    def test_url_only_uses_default_file(self):
        (self.ep / 'licenses/clip01.txt').write_text('public domain')
        r = self.run_scan('clip_id,giay_phep\nCLIP01,http://creativecommons.org/licenses/publicdomain/\n')
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_url_only_missing_default_blocks(self):
        r = self.run_scan('clip_id,giay_phep\nCLIP01,http://creativecommons.org/licenses/publicdomain/\n')
        self.assertEqual(r.returncode, 1)
        self.assertIn('P5 thiếu tệp giấy phép cho CLIP01', r.stdout)
        self.assertIn('ep/licenses/clip01.txt', r.stdout)   # đòi tệp mặc định, không đòi "licenses/publicdomain"
        self.assertNotIn('publicdomain', r.stdout.split('cần')[-1])

    def test_explicit_path_beside_url(self):
        (self.ep / 'licenses/pd-note.txt').write_text('public domain')
        r = self.run_scan('clip_id,giay_phep\nCLIP01,"PD https://creativecommons.org/licenses/publicdomain/ licenses/pd-note.txt"\n')
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_explicit_path_missing_blocks(self):
        r = self.run_scan('clip_id,giay_phep\nCLIP01,licenses/khong-co.txt\n')
        self.assertEqual(r.returncode, 1)
        self.assertIn('ep/licenses/khong-co.txt', r.stdout)


if __name__ == '__main__':
    unittest.main()

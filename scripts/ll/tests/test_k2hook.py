"""scripts/ll/k2hook.py (tuỳ chọn --k2check của qc.py) — V5a, 15/10/2026.
Chạy: /opt/cine/bin/python -m unittest scripts/ll/tests/test_k2hook.py -v
Dùng repo giả trong thư mục tạm với k2check.py GIẢ (không đọc/không chạy mã checks/ thật), cộng một ca trên repo thật."""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

LL = Path(__file__).resolve().parents[1]; REPO = LL.parents[1]
sys.path.insert(0, str(LL))
import k2hook  # noqa: E402

FAKE = '''import json, sys
a = sys.argv[1:]; j = a[a.index('--json') + 1]
json.dump({"ket_qua": "%s", "argv": a}, open(j, "w"))
print("k2check giả: %s"); sys.exit(%d)
'''


class K2Hook(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix='k2hook-')); self.out = self.d / 'out'; (self.out / 'sec').mkdir(parents=True)
        self.ep = self.d / 'episode.yaml'; self.ep.write_text('id: k2x-01\n')

    def tearDown(self): shutil.rmtree(self.d, ignore_errors=True)

    def fake(self, kq, rc):
        (self.d / 'checks/ll').mkdir(parents=True, exist_ok=True)
        (self.d / 'checks/ll/k2check.py').write_text(FAKE % (kq, kq, rc))

    def test_absent_is_silent(self):
        self.assertIsNone(k2hook.run(str(self.d), str(self.ep), str(self.out), ep_id='k2x-01'))

    def test_pass(self):
        self.fake('ĐẠT', 0); r = k2hook.run(str(self.d), str(self.ep), str(self.out), ep_id='k2x-01', py=sys.executable)
        self.assertTrue(r['ok']); self.assertIn('ket_qua=ĐẠT', r['note'])

    def test_fail(self):
        self.fake('TRƯỢT', 1); r = k2hook.run(str(self.d), str(self.ep), str(self.out), ep_id='k2x-01', py=sys.executable)
        self.assertFalse(r['ok']); self.assertEqual(r['val'], 'mã thoát 1')

    def test_args_only_existing_files(self):
        a = k2hook.args_for(str(self.ep), str(self.out), 'v1', 'k2x-01')
        self.assertEqual(a[0], str(self.ep)); self.assertNotIn('--tl', a); self.assertNotIn('--master', a); self.assertNotIn('--logs', a)
        (self.out / 'timeline.json').write_text('{}'); (self.out / 'mix.json').write_text('{}')
        (self.out / 'k2x-01-v1-master.mp4').write_bytes(b''); (self.out / 'sec/a.mkv.log.json').write_text('{}')
        a = k2hook.args_for(str(self.ep), str(self.out), 'v1', 'k2x-01')
        for k in ('--tl', '--master', '--mix', '--logs', '--md', '--json'): self.assertIn(k, a)

    def test_real_repo_state(self):
        """trên nhánh chưa merge 1.11 thì bỏ qua êm; đã merge thì có tệp — chỉ kiểm hành vi khớp trạng thái tệp."""
        has = (REPO / k2hook.K2CHECK).exists()
        if not has: self.assertIsNone(k2hook.run(str(REPO), str(self.ep), str(self.out)))

    def test_qc_compiles_and_strips_flag(self):
        subprocess.run([sys.executable, '-m', 'py_compile', str(LL / 'qc.py')], check=True)
        src = (LL / 'qc.py').read_text()
        self.assertIn("sys.argv = [x for x in sys.argv if x != '--k2check']", src)
        self.assertLess(src.index("x != '--k2check'"), src.index('EP = sys.argv[1]'))


if __name__ == '__main__':
    unittest.main()

#!/opt/cine/bin/python
"""Kiểm thử nhanh phần chống lặp góc máy và trường đặc tả shot (scripts/k2/prep.py) + thư viện góc máy (scripts/k2/cams.yaml).
  /opt/cine/bin/python scripts/k2/test_k2v.py"""
import copy, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep  # noqa: E402


def ep(shots, heroes):
    return {'id': 't', 'heroes': heroes, 'segments': [{'id': '00', 'shots': shots}]}


class T(unittest.TestCase):
    def test_library_min6(self):
        L = prep.cam_lib()
        for scene, P in L.items():
            ok = [k for k, v in P.items() if not v.get('loai')]
            self.assertGreaterEqual(len(ok), 6, f'{scene}: {len(ok)} preset dùng được')

    def test_preset_resolves(self):
        E = ep([], {'a': {'hero': 'k2g01/port', 'cam': 'p_day', 'opt': {'tod': 'day'}}, 'm': {'hero': 'map/globe', 'cam': 'flyto', 'opt': {'focus': 'brussels'}}})
        prep.resolve_cams(E)
        self.assertIsInstance(E['heroes']['a']['opt']['cam'], list); self.assertEqual(E['heroes']['a']['_camera_id'], 'p_day')
        self.assertEqual(E['heroes']['m']['opt']['preset'], 'flyto'); self.assertEqual(E['heroes']['m']['_camera_id'], 'flyto')

    def test_unknown_preset(self):
        with self.assertRaises(SystemExit): prep.resolve_cams(ep([], {'a': {'hero': 'k2g01/port', 'cam': 'khong-co'}}))

    def test_block_third_use(self):
        H = {'a': {'hero': 'k2g01/port', 'cam': 'p_day'}, 'b': {'hero': 'k2g01/port', 'cam': 'p_eu'}}
        two = [{'tpl': 'plate', 'p': {'hero': 'a'}}, {'tpl': 'plate', 'p': {'hero': 'b'}}, {'tpl': 'plate', 'p': {'hero': 'a'}}]
        _, _, bad = prep.repeat_check(ep(copy.deepcopy(two), copy.deepcopy(H))); self.assertEqual(bad, {})
        three = two + [{'tpl': 'plate', 'p': {'hero': 'b'}}, {'tpl': 'plate', 'p': {'hero': 'a'}}]
        _, _, bad = prep.repeat_check(ep(copy.deepcopy(three), copy.deepcopy(H))); self.assertEqual(bad, {('k2g01/port', 'p_day'): 3})

    def test_near_cameras_merge(self):
        # mid-push và orbit-r12-low của furnace lệch ~21° → một góc (K Q33 pHash cũng gộp trên shot mẫu D); orbit-l45 tách
        H = {'a': {'hero': 'k2g01/furnace', 'cam': 'mid-push'}, 'b': {'hero': 'k2g01/furnace', 'cam': 'orbit-r12-low'}, 'c': {'hero': 'k2g01/furnace', 'cam': 'orbit-l45'}}
        sh = [{'tpl': 'plate', 'p': {'hero': k}} for k in 'acbca']
        cnt, _, bad = prep.repeat_check(ep(copy.deepcopy(sh), copy.deepcopy(H)))
        self.assertIn(('k2g01/furnace', 'mid-push'), bad); self.assertEqual(cnt[('k2g01/furnace', 'orbit-l45')], 2)

    def test_adjacent_same_is_one(self):
        H = {'a': {'hero': 'k2g01/port', 'cam': 'p_day'}}
        sh = [{'tpl': 'plate', 'p': {'hero': 'a'}}] * 3
        cnt, _, bad = prep.repeat_check(ep(copy.deepcopy(sh), copy.deepcopy(H))); self.assertEqual(cnt[('k2g01/port', 'p_day')], 1)

    def test_cards_not_counted(self):
        H = {'a': {'hero': 'k2g01/port', 'cam': 'p_day'}}
        sh = [{'tpl': 'plate', 'p': {'hero': 'a', 'card': {'type': 'num'}}}, {'tpl': 'plate', 'p': {'hero': 'a'}}] * 2 + [{'tpl': 'plate', 'p': {'hero': 'a', 'card': {'type': 'num'}}}]
        cnt, _, bad = prep.repeat_check(ep(copy.deepcopy(sh), copy.deepcopy(H))); self.assertEqual(bad, {}); self.assertEqual(cnt[('k2g01/port', 'p_day')], 2)

    def test_inline_same_cam_same_id(self):
        c = [{'u': 0, 'p': [1, 2, 3], 'l': [0, 0, 0]}]
        H = {'a': {'hero': 'k2g01/mill', 'opt': {'cam': c}}, 'b': {'hero': 'k2g01/mill', 'opt': {'cam': copy.deepcopy(c), 'hot': 1}}}
        sh = [{'tpl': 'plate', 'p': {'hero': k}} for k in 'axbxa']; H['x'] = {'hero': 'k2g01/port'}
        _, _, bad = prep.repeat_check(ep(sh, H)); self.assertEqual(len(bad), 1)   # cùng máy quay, khác opt → vẫn là cùng góc

    def test_meta_fields(self):
        E = ep([{'tpl': 'plate', 'p': {'hero': 'm', 'places': [{'a': 'washington'}, {'a': 'brussels'}]}},
                {'tpl': 'plate', 'p': {'hero': 'd'}, 'people': ['Andrew Carnegie'], 'type': 'photo'}],
               {'m': {'hero': 'map/globe', 'cam': 'pair'}, 'd': {'hero': 'photo/print'}})
        prep.resolve_cams(E); M0 = prep.shot_meta(E, E['segments'][0]['shots'][0]); M1 = prep.shot_meta(E, E['segments'][0]['shots'][1])
        self.assertEqual((M0['type'], M0['scene_id'], M0['camera_id'], M0['places']), ('map', 'map/globe', 'pair', ['washington', 'brussels']))
        self.assertEqual((M1['type'], M1['camera_id'], M1['people']), ('photo', 'default', ['Andrew Carnegie']))
        self.assertEqual(prep.shot_type('photo/doc'), 'document'); self.assertEqual(prep.shot_type('k2g01/port'), 'scene3d'); self.assertEqual(prep.shot_type('photo/headline'), 'document'); self.assertEqual(prep.shot_type(None), 'card')

    # ---- V2 (14/10/2026): bản đồ nổi, sticker, đặc tả cuộn mẫu
    def test_v2_relief_type(self):
        self.assertEqual(prep.shot_type('relief/map'), 'map')

    def test_v2_sticker_library(self):
        import hashlib, json
        D = os.path.join(prep.REPO, 'design/k2v/stickers'); man = json.load(open(os.path.join(D, 'stickers.json')))
        items = {k: v for k, v in man.items() if not k.startswith('_')}
        self.assertEqual(sum(1 for v in items.values() if v['kind'] == 'character'), 8)
        self.assertGreaterEqual(sum(1 for v in items.values() if v['kind'] == 'object'), 12)
        for k, v in items.items(): self.assertEqual(hashlib.sha256(open(os.path.join(D, k + '.png'), 'rb').read()).hexdigest(), v['sha256'], k)

    def test_v2_reel_q34c_cols(self):
        """mọi nhãn số bám col:<id> phải có <id> trong heroes.<p.hero>.opt.cols (điều kiện Q34(c) 1.10.2) và num nằm trong anchors"""
        import yaml
        E = yaml.safe_load(open(os.path.join(prep.REPO, 'channel-k2/k2v2-mau/K2V2-reel.yaml'))); seen = set()
        for sg in E['segments']:
            for sh in sg['shots']:
                p = sh['p']; cols = {c['id'] for c in (E['heroes'][p['hero']].get('opt') or {}).get('cols', [])}
                for tg in p.get('tags', []):
                    if str(tg.get('a', '')).startswith('col:'): self.assertIn(tg['a'][4:], cols); seen.add(tg.get('num'))
        self.assertEqual(seen, set(E['anchors']))

    def test_v2_shader_no_line_comment(self):
        """chú thích // trong dòng GLSL có mã phía sau nuốt phần còn lại của main() (lỗi nháp V2): trong chuỗi shader chỉ dùng /* */"""
        import re
        src = open(os.path.join(prep.REPO, 'design/k2v/relief.js')).read()
        for m in re.finditer(r'(?:vertexShader|fragmentShader):\s*`([^`]*)`', src):
            for line in m.group(1).split('\n'): self.assertNotIn('//', line, line[:90])

if __name__ == '__main__':
    unittest.main(verbosity=1)

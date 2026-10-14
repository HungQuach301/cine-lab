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
    # ---- V2b (14/10/2026): sticker vật trong cảnh, shader viền, nhịp thị giác
    def test_v2b_lift_props(self):
        """p.stickers của shot relief → opt.props (vật thư viện = obj, vai = char), mốc giây trừ at của shot; shot không phải relief giữ nguyên"""
        E = ep([{'tpl': 'plate', 'at': 2.0, 'p': {'hero': 'r', 'stickers': [{'a': 'st:b', 'img': 'stk:boat', 'at': 3.0, 'px': 90, 'walk': True}, {'a': 'st:c', 'img': {'role': 'farmer', 'hand': 'wheat'}, 'at': '@wheat'}]}},
                {'tpl': 'plate', 'at': 6.0, 'p': {'hero': 'm', 'stickers': [{'a': 'x', 'img': 'stk:coin'}]}}],
               {'r': {'hero': 'relief/map', 'opt': {}}, 'm': {'hero': 'map/globe', 'opt': {}}})
        prep.lift_props(E); P = E['heroes']['r']['opt']['props']; S0 = E['segments'][0]['shots']
        self.assertEqual((P[0]['obj'], P[0]['t'], P[0]['walk'], P[0]['a']), ('boat', 1.0, True, 'st:b'))
        self.assertEqual((P[1]['char'], P[1]['t']), ({'role': 'farmer', 'hand': 'wheat'}, '@wheat'))
        self.assertNotIn('stickers', S0[0]['p']); self.assertIn('stickers', S0[1]['p'])
        prep.lift_props(E); self.assertEqual(len(E['heroes']['r']['opt']['props']), 2)   # chạy lại không nhân đôi

    def test_v2b_outline_shader(self):
        """viền trắng bằng shader cho vật trong cảnh: mặt nạ layer 1 → quad toàn khung vẽ sau địa hình, trước vật; vật vào hàng trong suốt (renderOrder 9)"""
        src = open(os.path.join(prep.REPO, 'design/k2v/relief.js')).read()
        for k in ('maskRT', 'uniform sampler2D tMask', 'outline.renderOrder = 8', 'm.layers.enable(1)', 'm.renderOrder = 9', 'shCam', 'tShadow', 'shOn'): self.assertIn(k, src)

    def test_v2b_rhythm(self):
        """nhịp thị giác của cuộn mẫu: mọi biến cố khai khớp đặc tả, trung bình ≤ 3,5 s, khoảng dài nhất ≤ 6 s"""
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(prep.REPO, 'scripts/k2/rhythm.py'), os.path.join(prep.REPO, 'channel-k2/k2v2-mau/K2V2-reel.yaml')], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-800:])

    # ---- V3 (14/10/2026): nguồn ngắn ≥ 38 px, thước ×10, bảng điểm gọn, chia đoạn dựng
    def test_v3_source_short(self):
        """Kinh thánh §4 (20:45): dòng nguồn 16:9 ≥ 38 px; nguồn trên hình chỉ tên ngắn (một dòng ≤ 70 ký tự ở cuộn mẫu)"""
        import re, yaml
        src = open(os.path.join(prep.REPO, 'scripts/k2/lib/k2.js')).read(); px = int(re.search(r'const SRCPX = V \? \d+ : (\d+)', src).group(1)); self.assertGreaterEqual(px, 38)
        E = yaml.safe_load(open(os.path.join(prep.REPO, 'channel-k2/k2v2-mau/K2V2-reel.yaml')))
        for sg in E['segments']:
            for sh in sg['shots']:
                p = sh['p']; s1 = [p.get('src')] + [((p.get('score') or {}).get('board') or {}).get('foot')]
                for x in filter(None, s1): self.assertLessEqual(len(x), 70, x)

    def test_v3_ruler_and_chunk(self):
        src = open(os.path.join(prep.REPO, 'design/k2v/relief.js')).read(); vs = open(os.path.join(prep.REPO, 'scripts/k2/vshot.py')).read()
        for k in ("anchors['rul:'", 'c.ruler', 'FAST ? 12 : 24'): self.assertIn(k, src)
        for k in ("arg('chunk'", "'--only'", 'WORK.sort'): self.assertIn(k, vs)

    # ---- V4 (14/10/2026): tách nền chân dung (F2), footage thật ≤ 20 % (F3), zoom nhiều tầng (F4), hàng xu (G2), bảng điểm ≥ 34 px (G3)
    V4 = os.path.join(prep.REPO, 'channel-k2/k2v4-mau/K2V4-reel.yaml')

    def test_v4_footage_share(self):
        """footage ≤ 20 % thời lượng; mỗi clip có p.clip + p.setting + SHA; mỗi clip có tệp giấy phép ghi đúng SHA; clip ≤ 8 s"""
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(prep.REPO, 'scripts/k2/footage_share.py'), self.V4], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-1200:])

    def test_v4_cutout_masks(self):
        """mỗi shot photo/cutout: mặt nạ alpha + nền mờ + sổ JSON tồn tại trong repo, SHA khớp sổ, mặt nạ cùng cỡ ảnh, mô hình có giấy phép mở (không bria/NC)"""
        import hashlib, json, yaml
        from PIL import Image
        E = yaml.safe_load(open(self.V4)); n = 0
        for k, h in E['heroes'].items():
            if h['hero'] != 'photo/cutout': continue
            o = h['opt']; mask = os.path.join(prep.REPO, 'design', o['mask'].lstrip('/')); img = os.path.join(prep.REPO, o['img'].lstrip('/'))
            meta = json.load(open(mask.replace('-mask.png', '.json'))); n += 1
            self.assertTrue(os.path.exists(mask), mask); self.assertEqual(hashlib.sha256(open(mask, 'rb').read()).hexdigest(), meta['mask_sha256'])
            self.assertEqual(hashlib.sha256(open(img, 'rb').read()).hexdigest(), meta['img_sha256'], img)
            self.assertTrue(os.path.exists(os.path.join(prep.REPO, meta['bg'])))
            self.assertEqual(Image.open(mask).size, Image.open(img).size)
            self.assertIn(meta['model'], ('birefnet-portrait', 'birefnet-general', 'isnet-general-use', 'u2net')); self.assertNotIn('NC', meta['model_license'] or '')
            self.assertLessEqual(meta['edge']['lech_p95_px'], 1.5, 'mép răng cưa/gợn')
        self.assertGreaterEqual(n, 2)

    def test_v4_rhythm(self):
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(prep.REPO, 'scripts/k2/rhythm.py'), self.V4], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-800:])

    def test_v4_zoom_api(self):
        """zoom nhiều tầng: ≥ 2 tầng ảnh hàng không có bbox + fade theo khoảng cách (xa > gần, tầng sau gần hơn), tầng gần hoà theo mốc; mỗi tầng có SHA trong sổ"""
        import json, yaml
        E = yaml.safe_load(open(self.V4)); o = E['heroes']['z_dive']['opt']; A = o['aerial']; self.assertGreaterEqual(len(A), 2)
        for a, b in zip(A, A[1:]): self.assertGreater(a['fade'][1], b['fade'][0] * 0.5); self.assertGreater(a['fade'][0], b['fade'][0])
        for a in A: self.assertGreater(a['fade'][0], a['fade'][1]); self.assertEqual(len(a['bbox']), 4)
        M = json.load(open(os.path.join(prep.REPO, 'channel-k2/k2v4-mau/aerial-lockport-meta.json'))); self.assertEqual(len(M['tiers']), len(A))
        for t in M['tiers']: self.assertRegex(t['sha256'], '^[0-9a-f]{64}$')
        self.assertLess(o['close']['at'][0], o['close']['at'][1]); src = open(os.path.join(prep.REPO, 'design/k2v/relief.js')).read()
        for k in ('o.aerial', 'o.close', 'Math.log(camDist)', 'camGround'): self.assertIn(k, src)

    def test_v4_coin_row_and_board(self):
        """G2: hàng 10 xu nằm cạnh 1 xu, bỏ thước ×10; G3: chữ bảng điểm gọn ≥ 34 px, bảng ~40 % khung"""
        import re, yaml
        E = yaml.safe_load(open(self.V4)); C = E['heroes']['h_num']['opt']['cols']
        self.assertEqual(sorted(c['n'] for c in C), [1, 10]); self.assertTrue(all(c.get('layout') == 'row' and not c.get('ruler') for c in C))
        N = [s for s in E['segments'] if s['id'] == 'N'][0]; self.assertFalse(any(t['a'].startswith('rul:') for t in N['shots'][0]['p']['tags']))
        S = [s for s in E['segments'] if s['id'] == 'S'][0]['shots'][0]['p']['score']; self.assertLessEqual(abs(S['board']['w'] / 1920 - 0.40), 0.03)
        k2 = open(os.path.join(prep.REPO, 'scripts/k2/lib/k2.js')).read(); i = k2.index('function score('); j = k2.index('// ---------- thẻ', i); seg = k2[i:j]
        for k in ("(CMP ? 36 : 40) * S, sd.c", "vp = CMP ? (win ? 42 : 40)", "text(g, r.k, bx + 86, y + rh * 0.5 + 13, 36", "text(g, Bd.title, mid, by + 58, 40 * S", "if (r.sub && r.sub[j] && !CMP)", "if (!CMP) text(g, 'vs'"): self.assertIn(k, seg)   # cỡ chữ từng phần tử của bảng gọn ≥ 34 px; bỏ dòng phụ
        self.assertGreaterEqual(seg.count('px = 34 * S'), 2)   # huy hiệu góc 34 px
        for sg in E['segments']:
            for sh in sg['shots']:
                p = sh['p']
                for x in filter(None, [p.get('src'), ((p.get('score') or {}).get('board') or {}).get('foot')]): self.assertLessEqual(len(x), 70, x)

    def test_t2_coin_row_thickness(self):
        """T2 0c (Kinh thánh §4, duyệt 15/10): hàng xu có độ dày (0,42 r), cạnh khía (bumpMap) + gờ mặt; shot số liệu mẫu nghiêng máy thấp (tilt ≥ 55° khỏi phương đứng)"""
        import yaml
        js = open(os.path.join(prep.REPO, 'design/k2v/relief.js')).read()
        for k in ("th = c.th || r * (ROW ? 0.42 : 0.24)", "bumpMap: tx", "ROW ? [edge, gold, gold] : gold", "new THREE.TorusGeometry(r * 0.7"): self.assertIn(k, js)
        E = yaml.safe_load(open(os.path.join(prep.REPO, 'channel-k2/k2c-t2-01/mau/coin-t2.yaml')))
        self.assertTrue(all(k['tilt'] >= 55 for k in E['heroes']['h_num']['opt']['cam']))

    def test_t2_footage_frame_in_frame(self):
        """T2 0c: nguồn < 720p → khung trong khung (tỉ lệ gốc, phóng ≤ 1,5×, viền); nguồn ≥ 720p → phủ kín như cũ"""
        import json, subprocess, tempfile
        with tempfile.TemporaryDirectory() as d:
            for name, size, want in (('lo', '480x360', True), ('hi', '1280x720', False)):
                f = os.path.join(d, name + '.mp4')
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'testsrc2=size={size}:rate=24', '-t', '1.5', '-pix_fmt', 'yuv420p', f], check=True)
                o = os.path.join(d, 'o' + name)
                r = subprocess.run(['node', os.path.join(prep.REPO, 'scripts/k2/hero.js'), '--hero', 'footage/clip', '--out', o, '--dur', '0.5', '--opt', json.dumps({'file': f, 'grade': 'sepia'})], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr[-800:])
                fr = json.load(open(os.path.join(o, 'meta.json')))['footage']['frame']
                if want:
                    self.assertIsNotNone(fr); self.assertLessEqual(fr['scale'], 1.5); self.assertAlmostEqual(fr['box'][0] / fr['box'][1], 480 / 360, places=2); self.assertGreater(fr['border'], 0)
                else:
                    self.assertIsNone(fr)


if __name__ == '__main__':
    unittest.main(verbosity=1)

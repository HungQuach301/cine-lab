#!/opt/cine/bin/python
"""ÂM THANH · kiểm nhanh (≈ 30 s, không mạng): /opt/cine/bin/python scripts/audio/test_audio.py (hoặc pytest nếu có)"""
import os, sys, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, master, measure, phat_am


def test_words_years():
    A = phat_am.apply
    assert A('Over 2,710 Liberty ships') == 'Over two thousand seven hundred ten Liberty ships'
    assert A('In 1943, at the peak') == 'In nineteen forty-three, at the peak'
    assert A('in 2005 and 2026 and 1905 and 1900') == 'in two thousand five and twenty twenty-six and nineteen oh-five and nineteen hundred'
    assert A('the 1970s') == 'the nineteen seventies'
    assert A('$5 billion of investment') == 'five billion dollars of investment'
    assert A('about 5% of') == 'about five percent of'
    assert A('a 500-won banknote') == 'a five-hundred-won banknote'
    assert A('On June 12, 2025,') == 'On June twelfth, twenty twenty-five,'
    assert A('the 21st century') == 'the twenty-first century'
    assert A('4.5 points') == 'four point five points'
    assert A('employed 702,000 people') == 'employed seven hundred two thousand people'
    assert A('built 1200 ships') == 'built one thousand two hundred ships'   # 4 chữ số trước danh từ đếm: không phải năm
    assert phat_am.leftovers(A('In 1943 the USTR said 4,440')) == ([], [])


def test_loudness_matches_ffmpeg():
    rng = np.random.default_rng(1); x = rng.standard_normal((lib.SR * 10, 2)) * 0.05
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'n.wav'); lib.write(p, x, 'pcm_f32le')
        assert abs(lib.integrated(x) - lib.ebur128(p)['I']) < 0.15


def test_master_chain():
    """lời giả (xung dải tiếng nói) trên nền nhạc giả to: chuỗi phải ra −14 LUFS ±0,5, đỉnh thật sau AAC ≤ −1, SMR p10 ≥ 15, loudnorm tuyến tính"""
    SR = lib.SR; T = 40; rng = np.random.default_rng(2); t = np.arange(T * SR) / SR
    vo = np.zeros(T * SR); speech = []
    for a in range(2, 36, 6):   # 4 s lời, 2 s nghỉ
        i0, i1 = a * SR, (a + 4) * SR; env = (np.sin(2 * np.pi * 3.5 * t[i0:i1]) > -0.3).astype(float)
        vo[i0:i1] = (np.sin(2 * np.pi * 180 * t[i0:i1]) + 0.5 * np.sin(2 * np.pi * 900 * t[i0:i1]) + 0.2 * rng.standard_normal(i1 - i0)) * env * 0.2; speech.append([a, a + 4])
    mus = np.stack([np.sin(2 * np.pi * 110 * t), np.sin(2 * np.pi * 165 * t)], 1) * 0.3 + rng.standard_normal((T * SR, 2)) * 0.05
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, 'o.wav')
        R = master.finish(dict(vo=vo[:, None].astype(np.float32), music=mus.astype(np.float32), sfx=None), speech=speech, out_wav=out, fade_in=0.5)
        assert R['dat']['I'] and R['dat']['TP_sau_aac'] and R['dat']['SMR_p10'] and R['dat']['loudnorm_tuyen_tinh'], R['dat']
        assert R['duck']['so_khoang'] == len(speech)


def test_merge_windows():
    assert lib.merge([[0, 1], [1.2, 2], [3, 4]]) == [[0, 2], [3, 4]]
    assert measure.windows_in([[0, 5.5]], 10) == [0.0, 1.0, 2.0]


if __name__ == '__main__':   # không có pytest trong /opt/cine: chạy thẳng
    for k, f in list(globals().items()):
        if k.startswith('test_'): f(); print('ĐẠT', k)

#!/opt/cine/bin/python
"""Tự kiểm luật kênh 2 bản 1.11.0 (phiên K, 15/10/2026). Mỗi luật mới/sửa: ca ĐẠT và ca TRƯỢT tự chứng minh, trên dữ liệu thật khi có
(T1 k2c-t1-06 bản phát hành: đặc tả + timeline dựng lại ngoại tuyến 22 585 khung = master; cuộn K2V4: đặc tả + timeline + số rhythm.py),
còn lại dữ liệu tổng hợp tạo trong thư mục tạm (âm thanh, video nhỏ, sổ footage) — không gọi mạng, không gọi API, không chạy ASR.

  /opt/cine/bin/python checks/ll/selftest_k2.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, csv, gzip, hashlib, json, os, subprocess, sys, tempfile

import numpy as np
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import base, q_amthanh as QA, q_chu as QC, q_nhip as QN, q_footage as QF, q_types as QT, q_rhythm as QR  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
TMP = tempfile.mkdtemp(prefix='k111-')
R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def sh(*a): subprocess.run(a, check=True, capture_output=True)


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


# =============================================================== ÂM THANH A1–A13 (tín hiệu tổng hợp)
SR = QA.SR


def tone(sec, seed=0):
    t = np.arange(int(sec * SR)) / SR
    x = (np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 1000 * t + 1)) * (0.75 + 0.25 * np.sin(2 * np.pi * 3 * t))
    return np.stack([x, x * 0.9], 1).astype(np.float32)


def write(path, x, aac=False):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-'] + (['-c:a', 'aac', '-b:a', '256k'] if aac else ['-c:a', 'pcm_f32le']) + [path]
    subprocess.run(cmd, input=x.astype(np.float32).tobytes(), check=True, capture_output=True); return path


def at_lufs(x, target, name):
    p = write(os.path.join(TMP, name + '-0.wav'), x); I = QA.ebur128(p)[0]; return (x * 10 ** ((target - I) / 20)).astype(np.float32)


base_sig = at_lufs(tone(20), -14.0, 'base')
TLa = dict(tong_s=20.0, segments=[dict(id='00', t0=0.0, t1=20.0, vo_file='x.mp3', vo_offset=0.5, speech=[[0.5, 9.0], [9.5, 19.0]], shots=[])], shorts=[])
Ea = dict(id='k2x', segments=[dict(id='00', vo='In 1943, America launched three cargo ships a day.')])
GOOD_T = {'00': {5: 'In 1943, America launched three cargo ships a day.', 1: 'In 1943, America launched 3 cargo ships a day.'}}
NHAC = [dict(file='a.mp3', bpm=72.0, lech_ranh_gioi_s=0.0, ss_doc=0.0, src_to=100.0),
        dict(file='b.mp3', bpm=90.0, lech_ranh_gioi_s=-3.0, ss_doc=0.0, src_to=80.0)]
MXa = dict(cong_cu=QA.NEW_CHAIN, smr=dict(cua_so=40, trung_vi=19.0, p10=16.0, min=13.0), nhac=NHAC, loudness=[dict(loudnorm=dict(normalization_type='linear'))])
FDUR = lambda f: {'a.mp3': 200.0, 'b.mp3': 200.0}.get(os.path.basename(f), 200.0)


def A(code, master=None, MX=MXa, E=Ea, TL=TLa, tr=GOOD_T, vo=None, bed=None):
    r = QA.check(E, TL, master=master, MX=MX, vo=vo, bed=bed, transcripts=tr, fdur=FDUR)
    x = next(z for z in r['rows'] if z['ma'] == code); return ([] if x['ok'] is True else [f"{code}: {x['gia_tri']}"]), r


m_ok = write(os.path.join(TMP, 'ok.mp4'), base_sig, aac=True)
e, r_ok = A('A1', m_ok)
case('A1', f"master AAC −14,0 LUFS (đo {next(z['gia_tri'] for z in r_ok['rows'] if z['ma'] == 'A1')}) → trong −15,0…−13,8", e, False)
for tgt, nm in ((-15.4, 'thấp'), (-13.4, 'cao')):
    case('A1', f'master AAC {tgt} LUFS ({nm}) → ngoài khoảng', A('A1', write(os.path.join(TMP, f'i{tgt}.mp4'), at_lufs(base_sig, tgt, f'i{tgt}'), aac=True))[0], True)
case('A1', 'master −13,9 LUFS (trong mép trên đã gồm dung sai +0,2) → đạt',
     A('A1', write(os.path.join(TMP, 'i139.mp4'), at_lufs(base_sig, -13.9, 'i139'), aac=True))[0], False)
case('A2', 'đỉnh thật sau AAC thấp (tín hiệu đều) → đạt', A('A2', m_ok)[0], False)
pk = base_sig.copy(); pk[SR * 10:SR * 10 + 48] = 0.97 * np.sign(np.sin(np.arange(48) * 1.3))[:, None]
case('A2', 'xung 0,97 (−0,3 dBFS) giữa phim → đỉnh thật sau AAC > −1,0 dBTP', A('A2', write(os.path.join(TMP, 'pk.mp4'), pk, aac=True))[0], True)
sl = base_sig.copy(); sl[int(SR * 9.0):int(SR * 10.3)] = 0
case('A5', 'lặng tuyệt đối 1,3 s giữa phim → 1 đoạn lặng bất thường', A('A5', write(os.path.join(TMP, 'sl.wav'), sl))[0], True)
sl2 = base_sig.copy(); sl2[int(SR * 9.0):int(SR * 9.6)] = 0
case('A5', 'lặng 0,6 s (ngắt câu) → không tính', A('A5', write(os.path.join(TMP, 'sl2.wav'), sl2))[0], False)
sl3 = base_sig.copy(); sl3[:int(SR * 1.8)] = 0
case('A5', 'lặng 1,8 s ở đầu phim (vùng bỏ 2 s đầu) → không tính', A('A5', write(os.path.join(TMP, 'sl3.wav'), sl3))[0], False)
cp = base_sig.copy(); cp[SR * 5:SR * 5 + 3, 0] = 1.0
case('A7', '3 mẫu liền = 1,0 (wav f32) → 1 lần chạm trần', A('A7', write(os.path.join(TMP, 'cp.wav'), cp))[0], True)
cp2 = base_sig.copy(); cp2[SR * 5:SR * 5 + 2, 0] = 1.0
case('A7', '2 mẫu liền = 1,0 → chưa tính chạm trần (≥ 3)', A('A7', write(os.path.join(TMP, 'cp2.wav'), cp2))[0], False)
case('A1', 'không có master với MIX=audio → TRƯỢT (không đo được)', A('A1', None)[0], True)
# A4
case('A4', 'mix.json smr p10 16,0 · min 13,0 → đạt', A('A4')[0], False)
case('A4', 'mix.json smr p10 14,9 → trượt', A('A4', MX=dict(MXa, smr=dict(MXa['smr'], p10=14.9)))[0], True)
case('A4', 'mix.json smr min 11,9 (p10 vẫn 16) → trượt', A('A4', MX=dict(MXa, smr=dict(MXa['smr'], min=11.9)))[0], True)
case('A4', 'không stem, mix.json không có smr → trượt', A('A4', MX={k: v for k, v in MXa.items() if k != 'smr'})[0], True)
vo_s = write(os.path.join(TMP, 'vo.wav'), at_lufs(tone(20), -20.0, 'vo'))
for bl, exp in ((-38.0, False), (-33.0, True)):
    bed_s = write(os.path.join(TMP, f'bed{bl}.wav'), at_lufs(tone(20)[::-1].copy(), bl, f'bed{bl}'))
    e, r = A('A4', vo=vo_s, bed=bed_s)
    case('A4', f"stem lời −20 / nền {bl} LUFS → K tự tính: {next(z['gia_tri'] for z in r['rows'] if z['ma'] == 'A4').split(' · stem')[0]}", e, exp)
# A8
case('A8', 'hai đoạn lời liền, không chồng → đạt', A('A8')[0], False)
TLo = copy.deepcopy(TLa); TLo['segments'] = [dict(id='00', t0=0.0, t1=10.0, speech=[[0.5, 9.8]], shots=[]), dict(id='01', t0=9.5, t1=20.0, speech=[[0.0, 9.0]], shots=[])]
case('A8', 'đoạn 01 bắt đầu lời ở 9,5 s khi đoạn 00 còn đọc tới 9,8 s → chồng lời', A('A8', TL=TLo, tr={})[0], True)
# A9
case('A9', 'hai cách nghe đủ 1943 + 3 (chữ "three" = số "3") → đạt', A('A9')[0], False)
case('A9', 'tham lam nghe "three cargo ship today" vẫn có 3, beam 5 mất 1943 → trượt',
     A('A9', tr={'00': {5: 'In 1940, America launched three cargo ships a day.', 1: GOOD_T['00'][1]}})[0], True)
case('A9', 'beam 5 đủ, tham lam nghe "tree cargo ships" (mất 3) → trượt (phải đủ CẢ HAI cách)',
     A('A9', tr={'00': {5: GOOD_T['00'][5], 1: 'In 1943, America launched tree cargo ships a day.'}})[0], True)
Ew = dict(id='k2x', segments=[dict(id='00', vo='Chung carried a 500-won banknote showing a turtle ship. Hyundai began in 1972.')])
TRw = {'00': {5: 'Chung carried a 501 banknote showing a turtle ship. Hyundai began in 1972.', 1: 'Chung carried a 501 banknote showing a turtle ship. Hyundai began in 1972.'}}
case('A9', 'câu "500-won" (ASR nghe "501", won/one) KHÔNG khai miễn → trượt', A('A9', E=Ew, tr=TRw)[0], True)
EwM = copy.deepcopy(Ew); EwM['segments'][0]['asr_mo_ho'] = [dict(cau='Chung carried a 500-won banknote showing a turtle ship.', ly_do='"five hundred won" ↔ "501": ASR không tách won/one, chấm bằng tai')]
e, r = A('A9', E=EwM, tr=TRw)
case('A9', 'khai asr_mo_ho đúng nguyên văn + lý do → miễn câu đó (liệt kê chấm tai), câu 1972 vẫn chấm → đạt', e if len(r['mien_asr']) == 1 else ['không liệt kê miễn'], False)
EwS = copy.deepcopy(EwM); EwS['segments'][0]['asr_mo_ho'][0]['ly_do'] = 'won/one'
case('A9', 'khai miễn với lý do < 20 ký tự → trượt', A('A9', E=EwS, tr=TRw)[0], True)
EwX = copy.deepcopy(EwM); EwX['segments'][0]['asr_mo_ho'][0]['cau'] = 'Chung carried a banknote.'
case('A9', 'khai miễn một câu không có trong lời → trượt', A('A9', E=EwX, tr=TRw)[0], True)
TRm = {'00': {5: 'Chung carried a 501 banknote showing a turtle ship. Hyundai began in 1970.', 1: TRw['00'][1]}}
case('A9', 'câu miễn không che câu khác: "1972" nghe thành "1970" ở câu không miễn → trượt', A('A9', E=EwM, tr=TRm)[0], True)
Ef = dict(id='k2x', segments=[dict(id='00', vo='In October 2026, Minneapolis Fed researchers reported it.')])
case('A9', 'T1 đoạn 09 thật: ASR viết "Minneapolis-fed" (gạch nối) → nhận "Fed" (1.11.0 trước sửa: báo nhầm)',
     A('A9', E=Ef, tr={'00': {5: 'In October 2026, Minneapolis-fed researchers reported it.', 1: 'In October, 2026, Minneapolis-fed researchers reported it.'}})[0], False)
case('A9', 'ASR "Minneapolis researchers" (mất hẳn Fed) → vẫn trượt',
     A('A9', E=Ef, tr={'00': {5: 'In October 2026, Minneapolis researchers reported it.', 1: 'In October 2026, Minneapolis researchers reported it.'}})[0], True)
# A11, A12
case('A11', 'giao bài lệch −3,0 s ở 72 bpm (1 ô = 3,33 s) → đạt', A('A11')[0], False)
case('A11', 'giao bài lệch −3,5 s > 1 ô nhịp → trượt', A('A11', MX=dict(MXa, nhac=[NHAC[0], dict(NHAC[1], lech_ranh_gioi_s=-3.5)]))[0], True)
case('A11', 'cue đọc tới 230 s trên bài 200 s (kéo/lặp nhạc) → trượt', A('A11', MX=dict(MXa, nhac=[dict(NHAC[0], src_to=230.0), NHAC[1]]))[0], True)
case('A11', 'cùng bài a.mp3 dùng lại 0–100 s ở cue 3 (> 60 s nguồn) → trượt',
     A('A11', MX=dict(MXa, nhac=NHAC + [dict(file='a.mp3', bpm=72.0, lech_ranh_gioi_s=0.5, ss_doc=20.0, src_to=110.0)]))[0], True)
case('A11', 'cùng bài dùng lại khúc khác (0–100 s rồi 150–190 s) → đạt',
     A('A11', MX=dict(MXa, nhac=NHAC + [dict(file='a.mp3', bpm=72.0, lech_ranh_gioi_s=0.5, ss_doc=150.0, src_to=190.0)]))[0], False)
case('A12', 'loudnorm linear → đạt', A('A12')[0], False)
case('A12', 'loudnorm dynamic (nén động ẩn) → trượt', A('A12', MX=dict(MXa, loudness=[dict(loudnorm=dict(normalization_type='dynamic'))]))[0], True)
# phạm vi áp dụng
lo = write(os.path.join(TMP, 'lo.mp4'), at_lufs(base_sig, -17.0, 'lo'), aac=True)
r_old = QA.check(Ea, TLa, master=lo, MX=dict(music_used=[], master=dict(I=-17.0, TP=-3.0)), transcripts=GOOD_T, fdur=FDUR)
case('A*', f"tập cũ (mix.json của ll/mix.py) −17 LUFS → kết quả {r_old['ket_qua']}, không chặn", [] if r_old['ket_qua'] == 'CHỈ BÁO' and r_old['ok'] else ['chặn tập cũ'], False)
r_new = QA.check(Ea, TLa, master=lo, MX=MXa, transcripts=GOOD_T, fdur=FDUR)
case('A*', f"cùng master với MIX=audio → {r_new['ket_qua']} (A1 chặn)", r_new['loi'], True)
case('A*', 'tập MIX=audio đạt mọi mục chặn → ĐẠT', QA.check(Ea, TLa, master=m_ok, MX=MXa, transcripts=GOOD_T, fdur=FDUR)['loi'], False)

# =============================================================== Q37 nhịp thị giác
FV4 = os.path.join(FX, 'k2v4-mau')
EV4 = base.load(os.path.join(FV4, 'K2V4-reel.yaml')); RV4 = json.load(open(os.path.join(FV4, 'rhythm-v4.json')))
r = QN.q37(EV4)
same = (r['tong_s'], r['bien_co']['n'], r['bien_co']['gop'], r['bien_co']['tb'], r['bien_co']['dai_nhat']) == \
       (RV4['tong_s'], RV4['bien_co_khai'], RV4['bien_co_gop'], RV4['khoang_tb_s'], RV4['khoang_dai_nhat_s'])
case('Q37', f"cuộn K2V4: bản sao K = số rhythm.py đã ghi (TB {r['bien_co']['tb']} s, dài nhất {r['bien_co']['dai_nhat']} s, {r['bien_co']['gop']} biến cố)",
     r['loi'] if same else ['lệch số rhythm.py'], False)
E1 = copy.deepcopy(EV4); E1['segments'][0]['beats'].append(dict(t=1.93, k='label', s='biến cố bịa'))
case('Q37', 'cuộn K2V4 thêm biến cố không có mốc đặc tả (1,93 s) → (a)', [x for x in QN.q37(E1)['loi'] if x.startswith('(a)')], True)
E2 = copy.deepcopy(EV4); E2['segments'][1]['beats'] = [b for b in E2['segments'][1]['beats'] if b['k'] != 'cut']
case('Q37', 'đoạn thiếu biến cố cut ở 0 → (a)', QN.q37(E2)['loi'], True)
E3 = copy.deepcopy(EV4); E3['segments'][0]['dur'] = float(E3['segments'][0]['dur']) + 7.0
case('Q37', 'kéo đoạn đầu thêm 7 s không biến cố → khoảng dài nhất > 6 s (c)', [x for x in QN.q37(E3)['loi'] if x.startswith('(c)')], True)
E4 = copy.deepcopy(EV4)
for sg in E4['segments']: sg['beats'] = [b for b in sg['beats'] if b['k'] == 'cut']
case('Q37', 'chỉ giữ biến cố cut (cắt cảnh) → TB > 3,5 s (b)', [x for x in QN.q37(E4)['loi'] if x.startswith('(b)')], True)
E5 = copy.deepcopy(EV4); E5['segments'][2].pop('beats')
case('Q37', 'một đoạn không khai beats → (a)', QN.q37(E5)['loi'], True)
HZo = dict(c=dict(opt=dict(cam=[dict(t=3.0)])))
To = QN.spec_times(HZo, [dict(at=0.0, p=dict(hero='a')), dict(at=2.0, p=dict(hero='c', off=48, speed=1))], 6.0)
case('Q37', f"cảnh dùng lại từ khung 48 (đặc tả đã giải: ll.load đổi frame0 → off): mốc máy τ = 3 s → giây đoạn 3,0 ({[round(x, 2) for x in To]})",
     [] if 3.0 in To and 5.0 not in To else ['sai quy đổi off'], False)
st7, st5 = os.path.join(TMP, 'st7.mp4'), os.path.join(TMP, 'st5.mp4')
sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=gray:s=320x180:r=24:d=7', '-f', 'lavfi', '-i', 'testsrc=s=320x180:r=24:d=2', '-filter_complex', '[0][1]concat=n=2:v=1', '-c:v', 'libx264', '-crf', '18', st7)
sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=gray:s=320x180:r=24:d=5', '-f', 'lavfi', '-i', 'testsrc=s=320x180:r=24:d=4', '-filter_complex', '[0][1]concat=n=2:v=1', '-c:v', 'libx264', '-crf', '18', st5)
case('Q37', f'video có khung tĩnh 7 s → (d) ({QN.static_run(st7)[0]} s)', [x for x in QN.q37(EV4, mp4=st7)['loi'] if x.startswith('(d)')], True)
case('Q37', f'video có khung tĩnh 5 s → đạt ({QN.static_run(st5)[0]} s)', QN.q37(EV4, mp4=st5)['loi'], False)
E1t = yaml.safe_load(gzip.open(os.path.join(FX, 'k2c106-g2', 'episode.yaml.gz'))); E1t.setdefault('out', '/var/tmp/cine-out/k2c-t1-06')
TL1 = json.load(gzip.open(os.path.join(FX, 'k2c106-g2', 'timeline.json.gz')))
r1 = QN.q37(E1t, TL1)
case('Q37', f"T1 (làm trước luật, không khai beats) → (a); tham khảo mốc đặc tả TB {r1['moc_dac_ta']['tb']} s", r1['loi'], True)

# =============================================================== Q35 nhãn loại số (D5)
NUMS = dict(n_hist=dict(v=3, text='3 a day', kind='actual', year=1943), n_now=dict(v=0.04, text='0.04%', kind='actual', year=2026),
            n_est=dict(v=4, text='≈ 4×', kind='estimate', year=2019), n_proj=dict(v=9, text='9%', kind='projection', period='2025–35'))


def tl1(p, t1=6.0):
    return dict(tong_s=t1, segments=[dict(id='00', t0=0.0, t1=t1, shots=[dict(tpl='plate', t0=0.0, t1=t1, p=p)])], shorts=[])


def q35(p, **kw): E = dict(id='k2x', numbers=NUMS, segments=[dict(id='00', shots=[dict(tpl='plate', type='scene3d')])]); return QC.q35(E, tl1(p), **kw)['loi']


case('Q35', 'số hiện tại (2026) khai kind actual trên tag + nhãn góc → ACTUAL 2 lần (b)', q35(dict(tags=[dict(s='0.04%', num='n_now', kind='actual', at=1.0)])), True)
case('Q35', 'số hiện tại không có nhãn ACTUAL nào, năm 2026 không hiện → (a)', q35(dict(tags=[dict(s='0.04%', num='n_now', at=1.0)])), True)
case('Q35', 'số lịch sử 1943, chip năm "1943" hiện cùng khung, không nhãn ACTUAL → đạt (D5)', q35(dict(year=dict(s='1943', at=0.2), tags=[dict(s='3 a day', num='n_hist', at=1.0)])), False)
case('Q35', 'số lịch sử 1943, năm ở chữ phụ của nhãn → đạt', q35(dict(tags=[dict(s='3 a day', sub='at the 1943 peak', num='n_hist', at=1.0)])), False)
case('Q35', 'số lịch sử khai year nhưng năm không hiện trên khung, không ACTUAL → (a)', q35(dict(tags=[dict(s='3 a day', num='n_hist', at=1.0)])), True)
case('Q35', 'ước tính có nhãn ESTIMATE (tag kind estimate) → đạt', q35(dict(tags=[dict(s='≈ 4×', num='n_est', kind='estimate', at=1.0)])), False)
case('Q35', 'ước tính không khai kind → không có ESTIMATE (c)', q35(dict(tags=[dict(s='≈ 4×', num='n_est', at=1.0)])), True)
case('Q35', 'ước tính khai kind actual → (d) + ACTUAL thay ESTIMATE', q35(dict(tags=[dict(s='≈ 4×', num='n_est', kind='actual', at=1.0)])), True)
case('Q35', 'dự báo có PROJECTION (nhãn góc) → đạt', q35(dict(tags=[dict(s='9%', num='n_proj', kind='projection', at=1.0)])), False)
case('Q35', 'tag khai ESTIMATE cho số không phải ước tính → (d)', q35(dict(year=dict(s='1943', at=0), tags=[dict(s='3 a day', num='n_hist', kind='estimate', at=1.0)])), True)
case('Q35', 'hai tag actual hiện lần lượt (1 s, 3 s) + nhãn góc → (b) ở khung 3 s', q35(dict(tags=[dict(s='0.04%', num='n_now', kind='actual', at=1.0), dict(s='3 a day', sub='1943', num='n_hist', kind='actual', at=3.0)])), True)
lg = os.path.join(TMP, 'logs'); os.makedirs(lg, exist_ok=True)


def mklog(items):
    json.dump(dict(id='00', fmt='16x9', text=[dict(f=48, items=[dict(s=s, cap=27.6, box=[100, 100 + 40 * i, 400, 128 + 40 * i]) for i, s in enumerate(items)])]), open(os.path.join(lg, '00.mkv.log.json'), 'w'))


mklog(['0.04%', 'ACTUAL', 'ACTUAL']); case('Q35', 'log render: khung 48 có 2 chữ "ACTUAL" → (b)', q35(dict(tags=[dict(s='0.04%', num='n_now', at=1.0)]), logdir=lg), True)
mklog(['0.04%', 'ACTUAL']); case('Q35', 'log render: một "ACTUAL" cạnh 0.04% → đạt', q35(dict(tags=[dict(s='0.04%', num='n_now', at=1.0)]), logdir=lg), False)
mklog(['≈ 4×', 'ACTUAL']); case('Q35', 'log render: ước tính ≈ 4× hiện với ACTUAL, thiếu ESTIMATE → (c)', q35(dict(tags=[dict(s='≈ 4×', num='n_est', at=1.0)]), logdir=lg), True)
r1 = QC.q35(E1t, TL1)
case('Q35', f"T1 bản phát hành (làm trước D5): {len(r1['muc']['b'])} shot ACTUAL ≥ 2 lần/khung (chấm mù V2: 'ACTUAL lặp')", r1['muc']['b'], True)

# =============================================================== Q36 chữ trên màn hình
SRCS = dict(LAW=dict(short='Seattle Building Code 2021', loai='luat', hieu_luc=True), LAWD=dict(short='Rule 2027', loai='quy_dinh', hieu_luc='2027-01-01'),
            OLD=dict(short='Act 1926', loai='luat', hieu_luc='1926-01-01', het_hieu_luc='2020-01-01'), DATA=dict(short='Census ACS 2024'))


def q36(p, logdir=None, card=False):
    E = dict(id='k2x', numbers=NUMS, sources=SRCS, segments=[dict(id='00', shots=[dict(tpl='plate', type='card' if card else 'scene3d')])])
    r = QC.q36(E, tl1(p), logdir); return r['loi'], r


s70 = 'Source: ' + 'x' * 62
case('Q36', 'dòng nguồn 70 ký tự → đạt (độ dài)', q36(dict(src=s70))[0], False)
case('Q36', 'dòng nguồn 71 ký tự → (a)', q36(dict(src=s70 + 'y'))[0], True)
case('Q36', 'p.src 50 ký tự + credit "3D illustration" nối khi vẽ = 68 → đạt', q36(dict(src='Source: ' + 'x' * 42, credit='3D illustration'))[0], False)
case('Q36', 'p.src 60 ký tự + credit → 78 ký tự (a)', q36(dict(src='Source: ' + 'x' * 52, credit='3D illustration', cap=[dict(s='a', at=0)]))[0], True)
e, r = q36(dict(src='Source: Census ACS 2024'))
case('Q36', 'không có log render → cỡ chữ THIẾU (không ĐẠT)', r['thieu'], True)
for capv, exp, nm in ((27.6, False, '38,0 px'), (26.0, True, '35,8 px')):
    json.dump(dict(id='00', fmt='16x9', text=[dict(f=24, items=[dict(s='Source: Census ACS 2024', cap=capv, box=[60, 1000, 400, 1028])])]), open(os.path.join(lg, '00.mkv.log.json'), 'w'))
    e, r = q36(dict(src='Source: Census ACS 2024'), logdir=lg)
    case('Q36', f'log render: dòng nguồn {nm}', e + r['thieu'], exp)
L2 = 'Source: Census ACS 2024 · National Zoning Atlas'
json.dump(dict(id='00', fmt='16x9', text=[dict(f=24, items=[dict(s='Source: Census ACS 2024 ·', cap=27.6, box=[60, 952, 400, 980]), dict(s='National Zoning Atlas', cap=27.6, box=[60, 1000, 400, 1028])])]), open(os.path.join(lg, '00.mkv.log.json'), 'w'))
e, r = q36(dict(src=L2), logdir=lg); case('Q36', 'log render: dòng nguồn bị xuống 2 dòng → (a) (log không có dòng nguyên văn)', e + r['thieu'], True)
case('Q36', '"Facts as of" + nguồn Seattle Building Code (loai luat, hieu_luc) → đạt', q36(dict(src='Source: Seattle Building Code 2021', asof='Facts as of 12 Oct 2026'))[1]['muc']['b'], False)
case('Q36', '"Facts as of" trên dữ liệu thống kê (Census) → (b)', q36(dict(src='Source: Census ACS 2024', asof='Facts as of 12 Oct 2026'))[1]['muc']['b'], True)
case('Q36', '"Facts as of" trong câu miễn trừ (cap), shot không dẫn luật → (b)', q36(dict(src='Source: Census ACS 2024', cap=[dict(s="It isn't financial advice. Facts as of 15 Oct 2026.", at=0)]))[1]['muc']['b'], True)
case('Q36', '"Facts as of" + luật đã hết hiệu lực (2020) → (b)', q36(dict(src='Source: Act 1926', asof='Facts as of 12 Oct 2026'))[1]['muc']['b'], True)
case('Q36', '"Facts as of 12 Oct 2026" + quy định hiệu lực từ 2027 → (b)', q36(dict(src='Source: Rule 2027', asof='Facts as of 12 Oct 2026'))[1]['muc']['b'], True)
case('Q36', '"Facts as of" + p.luat: LAW khai trực tiếp → đạt', q36(dict(src='Source: Census ACS 2024', luat='LAW', asof='Facts as of 12 Oct 2026'))[1]['muc']['b'], False)
r1 = QC.q36(E1t, TL1)
case('Q36', f"T1 (trước V3/luật này): {len(r1['muc']['a'])} dòng nguồn > 70 ký tự, {len(r1['muc']['b'])} 'Facts as of' chưa khai luật hiệu lực", r1['loi'], True)

# =============================================================== Q32 (1.11.0): DVIDS, giấy phép, footage 20 %, < 720p
K2D = os.path.join(TMP, 'channel-k2', 'k2x'); os.makedirs(os.path.join(K2D, 'licenses'), exist_ok=True)
LLD = os.path.join(TMP, 'reports', 'm3', 'ep99'); os.makedirs(LLD, exist_ok=True)
vlo, vhi = os.path.join(TMP, 'lo-640x480.mp4'), os.path.join(TMP, 'hi-1920x1080.mp4')
sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=s=640x480:r=24:d=1', '-c:v', 'libx264', vlo)
sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc=s=1920x1080:r=24:d=1', '-c:v', 'libx264', vhi)
SLO, SHI = sha(vlo), sha(vhi)
GOV = 'Video: U.S. Army Corps of Engineers (U.S. government work)'


def q32(T=66.0, rows=None, lic=None, opt_a=None, ep=K2D, desc=None, e2=None):
    ROWS = dict(A1=dict(clip_id='A1', url_trang='https://www.loc.gov/item/x1/', url_tai='https://tile.loc.gov/x1.mp4', ngay_tai_utc='2026-10-14T10:00:00Z',
                        giay_phep='PD — LoC (licenses/a1.txt)', yeu_cau_ghi_cong='khong', sha256=SLO, timecode_dung='0:00.00-0:05.00', nguoi_nhan_dien='khong', logo='khong'),
                B1=dict(clip_id='B1', url_trang='https://www.dvidshub.net/video/978155', url_tai='https://d34w7g4gy10iej.cloudfront.net/x.mp4', ngay_tai_utc='2026-10-14T10:00:00Z',
                        giay_phep='PD — DVIDS "PUBLIC DOMAIN"', yeu_cau_ghi_cong=f'co (ghi "{GOV}")', sha256=SHI, timecode_dung='0:10.00-0:15.00', nguoi_nhan_dien='khong', logo='khong'))
    for k, kv in (rows or {}).items(): ROWS[k].update(kv)
    with open(os.path.join(ep, 'SOURCES-FOOTAGE.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=QF.COLS); w.writeheader(); [w.writerow(r) for r in ROWS.values()]
    L = dict(a1=f'Asset A1\nSHA-256: {SLO}\n', b1=f'DVIDS 978155\nSHA-256: {SHI}\nPUBLIC DOMAIN — This work … identified by DVIDS\n')
    L.update(lic or {})
    for f in os.listdir(os.path.join(ep, 'licenses')) if os.path.isdir(os.path.join(ep, 'licenses')) else []: os.remove(os.path.join(ep, 'licenses', f))
    os.makedirs(os.path.join(ep, 'licenses'), exist_ok=True)
    for k, v in L.items():
        if v is not None: open(os.path.join(ep, 'licenses', k + '.txt'), 'w').write(v)
    HE = dict(fa=dict(hero='footage/clip', opt=dict(file=vlo, sha256=SLO, **(opt_a or {}))), fb=dict(hero='footage/clip', opt=dict(file=vhi, sha256=SHI)), s=dict(hero='k2x/room'))
    sh_ = [dict(tpl='plate', t0=0.0, t1=5.0, p=dict(hero='fa', clip='A1', setting='canal lock', file=vlo)), dict(tpl='plate', t0=5.0, t1=10.0, p=dict(hero='s')),
           dict(tpl='plate', t0=10.0, t1=15.0, p=dict(hero='fb', clip='B1', setting='Black Rock Lock', file=vhi)), dict(tpl='plate', t0=15.0, t1=T, p=dict(hero='s'))]
    TL = dict(tong_s=T, heroes=HE, segments=[dict(id='00', t0=0.0, t1=T, shots=sh_)], shorts=[])
    E = dict(id='k2x' if ep == K2D else 'll-ep99', out=TMP, heroes=HE, segments=[dict(id='00', shots=[dict(tpl='plate', type=t) for t in ('footage', 'scene3d', 'footage', 'scene3d')])])
    if e2: e2(E, TL)
    d = desc
    if d is not None: open(os.path.join(ep, 'desc.txt'), 'w').write(d); d = os.path.join(ep, 'desc.txt')
    return QF.q32(E, TL, ep, desc=d, scan=False)


FRAME = dict(fit='frame', zoom=1.5, border=True)
r = q32(opt_a=FRAME); case('Q32', f"kênh 2: LoC 640×480 trong khung ×1,5 có viền + DVIDS đủ điều kiện → đạt ({r['val'].split(' · ')[-1]})", r['loi'], False)
case('Q32', 'nguồn dvidshub.net được nhận (1.10.2: "ngoài danh sách cho phép")', [x for x in r['loi'] if 'ngoài danh sách' in x], False)
case('Q32i', 'nguồn 640×480 phóng đầy khung (không fit: frame) → (i)', q32()['muc']['i'], True)
case('Q32i', 'nguồn 640×480 trong khung phóng 1,6× → (i)', q32(opt_a=dict(FRAME, zoom=1.6))['muc']['i'], True)
case('Q32i', 'nguồn 640×480 trong khung, không viền → (i)', q32(opt_a=dict(FRAME, border=False))['muc']['i'], True)
case('Q32i', 'nguồn 640×480 trong khung, không khai zoom → (i)', q32(opt_a=dict(fit='frame', border=True))['muc']['i'], True)
r = q32(T=45.0, opt_a=FRAME); case('Q32b2', f"footage 10 s / 45 s = 22,2 % > 20 % (ảnh + footage vẫn < 40 %) → (b2)", r['muc']['b'], True)
r = q32(T=52.0, opt_a=FRAME); case('Q32b2', f"footage 10 s / 52 s = 19,2 % → đạt, nêu sát ngưỡng: {r['sat_nguong'][:1]}", r['muc']['b'] if r['sat_nguong'] else ['không nêu sát ngưỡng'], False)
case('Q32h', 'thiếu tệp giấy phép licenses/b1.txt → (h)', q32(opt_a=FRAME, lic=dict(b1=None))['muc']['h'], True)
case('Q32h', 'tệp giấy phép không ghi SHA của dòng sổ → (h)', q32(opt_a=FRAME, lic=dict(a1='Asset A1, không có SHA'))['muc']['h'], True)
case('Q32h', 'DVIDS: tệp giấy phép thiếu chữ "public domain" → (h)', q32(opt_a=FRAME, lic=dict(b1=f'SHA {SHI}'))['muc']['h'], True)
case('Q32g', 'DVIDS: logo "co: đã làm mờ" (vẫn trong khung) → (g)', q32(opt_a=FRAME, rows=dict(B1=dict(logo='co: huy hiệu đã làm mờ')))['muc']['g'], True)
case('Q32g', 'DVIDS: logo "co: đã cắt khỏi khung" → đạt', q32(opt_a=FRAME, rows=dict(B1=dict(logo='co: huy hiệu đã cắt khỏi khung')))['muc']['g'], False)
case('Q32g', 'DVIDS: người nhận diện được, không ghi "không nổi bật" → (g)', q32(opt_a=FRAME, rows=dict(B1=dict(nguoi_nhan_dien='co (một kỹ sư cận mặt)')))['muc']['g'], True)
case('Q32g', 'DVIDS: người ở xa "không cận mặt" → đạt', q32(opt_a=FRAME, rows=dict(B1=dict(nguoi_nhan_dien='co (xa, không cận mặt)')))['muc']['g'], False)
case('Q32g', 'DVIDS: câu ghi công không có "U.S. government work" (như cuộn K2V4) → (g)', q32(opt_a=FRAME, rows=dict(B1=dict(yeu_cau_ghi_cong='khong (ghi "Video: U.S. Army Corps of Engineers, 2025")')))['muc']['g'], True)
case('Q32g', 'DVIDS: mô tả YouTube có, thiếu câu ghi công → (g)', q32(opt_a=FRAME, desc='Music: … Footage: LoC.')['muc']['g'], True)
case('Q32g', 'DVIDS: mô tả YouTube có nguyên văn câu ghi công → đạt', q32(opt_a=FRAME, desc=f'Credits: {GOV}. Music: …')['muc']['g'], False)
case('Q32g', 'DVIDS giấy phép CC BY (không phải PD) → (a)', [x for x in q32(opt_a=FRAME, rows=dict(B1=dict(giay_phep='CC BY 4.0 (licenses/b1.txt)')))['muc']['a'] if 'không hợp nguồn' in x], True)
r = q32(ep=LLD, lic=dict(a1=None, b1=None))
case('Q32', 'tập LL (ngoài channel-k2/): (b2), (h), (i) không áp — như 1.10.2', r['muc']['b'] + r['muc']['h'] + r['muc']['i'], False)
TV4 = json.load(gzip.open(os.path.join(FV4, 'K2V4-reel.timeline.json.gz')))
FK = os.path.join(TMP, 'channel-k2', 'k2v4-mau'); os.makedirs(FK, exist_ok=True)
open(os.path.join(FK, 'SOURCES-FOOTAGE.csv'), 'w').write(open(os.path.join(FV4, 'so-footage-k2v4.csv.fixture')).read())   # tên khác để preflight P5 không coi bản sao là sổ thật
rv = QF.q32(EV4, TV4, FK, scan=False)
case('Q32', f"cuộn K2V4 (sổ thật): DVIDS hết '(a) ngoài danh sách'; ghi công thiếu 'U.S. government work' → (g)", rv['muc']['g'] if not [x for x in rv['muc']['a'] if 'ngoài danh sách' in x] else ['còn ngoài danh sách'], True)

# =============================================================== Q34(d) ngày chỉ có năm
def q34d(**p):
    TL = dict(tong_s=10.0, heroes={}, segments=[dict(id='00', t0=0.0, t1=10.0, shots=[dict(tpl='plate', t0=0.0, t1=2.5, p=dict(paper='The Times', **p)), dict(tpl='plate', t0=2.5, t1=10.0, p={})])], shorts=[])
    E = dict(id='k2x', segments=[dict(id='00', shots=[dict(tpl='plate', type='document'), dict(tpl='plate', type='scene3d')])])
    return QT.q34(E, TL)['muc']['d']


case('Q34d', 'document ngày đủ 1926-11-22 → đạt', q34d(date='1926-11-22'), False)
case('Q34d', 'document ngày chỉ có năm 1926, không khai lý do → (d)', q34d(date='1926'), True)
case('Q34d', 'document năm 1926 + date_chi_nam (nguồn chỉ ghi năm, ≥ 20 ký tự) → đạt', q34d(date='1926', date_chi_nam="masthead của số báo chỉ in 'Spring 1926'"), False)
case('Q34d', 'document năm 1926 + lý do quá ngắn → (d)', q34d(date='1926', date_chi_nam='chỉ có năm'), True)
case('Q34d', 'document "1926-11" (tháng, không khai) → (d)', q34d(date='1926-11', date_chi_nam="masthead của số báo chỉ in 'Spring 1926'"), True)

# =============================================================== Q14–Q18: khiếu nại P 14/10 (kênh 2 bị áp luật nhịp LL)
E1q = copy.deepcopy(E1t); E1q['_path'] = os.path.join(ROOT, 'channel-k2', 'k2c-t1-06', 'episode.yaml')
m = QR.measure(E1q, TL1)
case('Q14–18', 'T1 k2c-t1-06 (đặc tả dưới channel-k2/) → Q14–Q18 "không áp"', [k for k, v in m.items() if not v['ok'] or 'không áp' not in v['val']], False)
E1l = copy.deepcopy(E1t); E1l['id'] = 'll-ep06x'; E1l['_path'] = os.path.join(ROOT, 'reports', 'm3', 'ep06x', 'episode.yaml')
m = QR.measure(E1l, TL1)
case('Q14–18', f"cùng dữ liệu T1 đội lốt tập LL → vẫn đo như LL (tái hiện hiện tượng khiếu nại: {', '.join(k for k, v in m.items() if not v['ok'])} TRƯỢT)",
     [k for k, v in m.items() if not v['ok']], True)

for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<7} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
n_ok = sum(r[3] for r in R); print(f'\nselftest kênh 2 (1.11.0): {n_ok}/{len(R)} ca đúng kỳ vọng'); sys.exit(0 if n_ok == len(R) else 1)

#!/opt/cine/bin/python
"""G1b T3 · tờ soi nhanh: ghép khung dò (g1b_probe.sh) thành lưới 3 cột 640×360 có nhãn khoá. Dùng: g1b_sheet.py <thư mục dò> <ra.jpg> khoá1 khoá2 …"""
import glob, subprocess, sys
D, OUTF, ks = sys.argv[1], sys.argv[2], sys.argv[3:]
fs = [(k, sorted(glob.glob(f'{D}/{k}/0*.jpg'))) for k in ks]; fs = [(k, f[0]) for k, f in fs if f]
args = sum((['-i', f] for _, f in fs), []); n = len(fs); lay = '|'.join(f'{(i % 3) * 640}_{(i // 3) * 360}' for i in range(n))
fc = ''.join(f'[{i}]scale=640:360,drawtext=text={k[4:]}:fontcolor=yellow:fontsize=28:x=8:y=8:box=1:boxcolor=black@0.5[v{i}];' for i, (k, _) in enumerate(fs))
fc += ''.join(f'[v{i}]' for i in range(n)) + (f'xstack=inputs={n}:layout={lay}' if n > 1 else 'copy')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-filter_complex', fc, OUTF], check=True)

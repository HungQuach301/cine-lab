#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 (bản v3 của xem_cam.py) · việc 8 — XEM CÂM 3 người AI (§13.4) — CHỈ THAM KHẢO, không thay chấm của chủ dự án. Giao thức như scripts/k2tl/anim_cam.py (ANIMATIC-T3; import, không sửa):
`claude -p` claude-sonnet-5-5, chỉ Read, thư mục tạm chỉ có tờ khung; 3 vai nguyên văn T3; 1 khung / 4 s 320×180, không tiếng, không phụ đề; 8 câu cốt truyện T4; chấm từ khoá 0/1/2.
  xem_cam.py to <animatic.mp4> · run · score   (ra reports/animatic-t4-v2/xem-cam/)"""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
os.environ['ANIM_CAM_D'] = 'reports/animatic-t4-v2/xem-cam'
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'k2tl')); import anim_cam as A  # noqa: E402
A.RATERS['R2'] = 'You are a secondary-school history teacher who has never studied London in detail.'
A.Q = ['Q1 What disaster strikes the old city at the start of the story (what kind of event)?',
       'Q2 Where/how does it begin (a big area at once, or one small place)?',
       'Q3 How do ordinary people try to save themselves and their belongings?',
       'Q4 What happens to the great old church on the hill during the disaster?',
       'Q5 Afterwards, how is the city rebuilt (material, and on what street layout)?',
       'Q6 What big new building with a dome (and what tall column) appear after the rebuilding?',
       'Q7 What happens to the city in 1940, and what survives?',
       'Q8 What does the city look like today, and what is still visible among the towers?']
A.KEY = {'Q1': (['fire', 'blaze', 'burn'], ['great', 'city', 'whole', 'spread', '1666']),
         'Q2': (['bakery', 'bake', 'oven', 'one house', 'single house', 'small', 'lane', 'street', 'one building'], ['night', 'spread', 'oven', 'lane']),
         'Q3': (['boat', 'river', 'barge', 'cart', 'carry', 'flee', 'field', 'camp', 'tent'], ['goods', 'belonging', 'furniture', 'chest', 'river', 'boat', 'cart']),
         'Q4': (['burn', 'fire', 'destroy', 'collapse', 'ruin', 'lost', 'melt'], ['church', 'cathedral', 'roof', 'lead']),
         'Q5': (['brick'], ['same street', 'old street', 'same layout', 'same plan', 'same pattern', 'old layout', 'street pattern', 'same lines']),
         'Q6': (['dome', 'cathedral', "st paul", 'st. paul'], ['column', 'monument', 'pillar', 'tower']),
         'Q7': (['bomb', 'blitz', 'air raid', 'war', 'fire'], ['dome', 'cathedral', "st paul", 'surviv', 'stands', 'standing']),
         'Q8': (['tower', 'skyscraper', 'high-rise', 'modern', 'glass'], ['dome', 'cathedral', "st paul", 'visible', 'still'])}
A.PROMPT = A.PROMPT.replace('~12-minute 3D-animated history video', '~12-minute 3D-animated history video about one city')
if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'to':
        import subprocess, shutil
        from PIL import Image, ImageDraw
        tmp = Path('/var/tmp/anim/cam'); shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', sys.argv[2], '-vf', f'fps=1/{A.STEP},scale=320:180:flags=area', str(tmp / '%04d.jpg')], check=True)
        fs = sorted(tmp.glob('*.jpg')); per, cols = 24, 4
        for p in A.D.glob('to-*.jpg'): p.unlink()
        for b in range(0, len(fs), per):
            F = fs[b:b + per]; rows = (len(F) + cols - 1) // cols; S = Image.new('RGB', (320 * cols, 196 * rows), (12, 12, 12)); g = ImageDraw.Draw(S)
            for i, f in enumerate(F):
                k = b + i; x, y = (i % cols) * 320, (i // cols) * 196; S.paste(Image.open(f), (x, y + 16)); g.text((x + 4, y + 2), f'#{k}  {k * A.STEP} s', fill=(255, 230, 120))
            S.save(A.D / f'to-{b // per + 1:02d}.jpg', quality=80)
        print(len(fs), 'khung')
    elif c == 'run':
        env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY']); os.environ.update(env)
        with ThreadPoolExecutor(3) as ex: print(list(ex.map(A.call, list(A.RATERS))))
    elif c == 'score': A.score()

#!/opt/cine/bin/python
"""Sinh mô tả YouTube tập 4 từ timeline (chương = mốc đoạn thật). python make_desc.py <timeline.json> <ra.txt>"""
import json, sys
tl = json.load(open(sys.argv[1]))
CH = {'00': 'What happened to the typing pool?', '01': 'The typing pool', '02': 'A new kind of job', '03': 'A door for women', '04': 'The pool keeps filling', '05': 'The computer, in two waves',
      '06': 'Fewer hands', '07': 'Typists today', '08': 'Secretaries and AI', '09': 'Spoken words, typed pages', '10': 'AI and writing work', '11': 'Same pattern, different technology',
      '12': 'Who gets the next door?', '13': 'The last lamp'}
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
chap = '\n'.join(f"{mm(s['t0'])} {CH[s['id']]}" for s in tl['segments'])
txt = f'''TITLE
The Typewriter Opened a Door for Millions of Women. Who Gets the Next One?

DESCRIPTION
The typewriter built one of the largest workforces in America. By 1970, the census counted about 3.9 million stenographers, typists and secretaries, most of them women. Then the computer came for the office, first for the records, then for the typing.

Today, the Bureau of Labor Statistics projects word processors and typists to shrink 34.4 percent by 2035, and it names AI among the tools that let staff prepare their own documents. This film follows the typing pool from boom to today, and asks who gets the next door.

The street and its lamplighter are fictional. Every number on screen comes from the sources listed below.

Chapters
{chap}

Sources
- U.S. Census Bureau, Historical Statistics of the United States, Colonial Times to 1970, Series D 182–232 and D 233–682
- U.S. Bureau of Labor Statistics, Bulletin 1276, "Adjustments to the Introduction of Office Automation" (1960)
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, 1990–91 Edition (Bulletin 2350)
- U.S. Bureau of Labor Statistics, Employment Projections 2025–35, Table 1.5; Occupational Outlook Handbook, "Secretaries and Administrative Assistants"
- U.S. Bureau of Labor Statistics, Monthly Labor Review, January 2026 (projections 2024–34)
- S. Noy & W. Zhang, "Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence", MIT working paper (2023)
Projections are forecasts, not counts. The MIT experiment measured writing tasks, not jobs.

Music
"Immersed" and "Reawakening" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

How this film was made
Written, animated and edited with AI tools (Claude by Anthropic) under the direction of the channel's human author, who approved every creative decision. Narration is a synthetic voice (ElevenLabs library voice, not a real person). Animation is stylised and not intended to depict real footage.
'''
open(sys.argv[2], 'w').write(txt); print(chap)

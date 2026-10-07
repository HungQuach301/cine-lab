#!/opt/cine/bin/python
"""Sinh mô tả YouTube tập 2 từ timeline (chương = mốc đoạn thật). python make_desc.py <timeline.json> <ra.txt>"""
import json, sys
tl = json.load(open(sys.argv[1]))
CH = {'00': 'Cold open', '01': 'Hello, Central', '02': 'A person in the middle', '03': 'Counting the operators', '04': 'The cutover', '05': 'What happened to the operators',
      '06': 'The next generation', '07': 'Someone, or something, still answers', '08': 'The voice today', '09': 'The 2035 projection', '10': 'Why BLS expects AI to matter',
      '10b': 'AI at the help desk', '10c': 'An early signal', '11': 'Same pattern, different technology', '12': 'Who carries the cost?', '13': 'The last lamp'}
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
chap = '\n'.join(f"{mm(s['t0'])} {CH[s['id']]}" for s in tl['segments'] if s['id'] not in ('07',) or True)
txt = f'''TITLE
Automation Hurt the Phone Operators. Not the Next Generation. What About Us?

DESCRIPTION
Between 1920 and 1940, the dial replaced telephone operators across more than half of the U.S. network. The women already at the switchboards paid the price. The generation after them found other work.

Today, about 2.7 million Americans answer the phone in customer service, and the Bureau of Labor Statistics projects that number to fall about five percent by 2035. This film puts the two stories side by side, on the same scale, and asks who carries the cost this time.

Ostler Street and its lamplighter are fictional. Every number on screen comes from the sources listed below.

Chapters
{chap}

Sources
- J. Feigenbaum & D. Gross, "Answering the Call of Automation: How the Labor Market Adjusted to Mechanizing Telephone Operation", NBER Working Paper 28061 (rev. 2024)
- Federal Reserve Bank of Richmond, Econ Focus Q4 2019, "Goodbye, Operator"
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, "Customer Service Representatives" (projections 2025–35)
- Machovec, Rieley & Rolen, "Incorporating AI impacts in BLS employment projections: occupational case studies", Monthly Labor Review, Feb 2025
- E. Brynjolfsson, D. Li & L. Raymond, "Generative AI at Work", NBER Working Paper 31161 (2023)
- E. Brynjolfsson, B. Chandar & R. Chen, "Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence", Stanford Digital Economy Lab (Aug 2026)
Projections are forecasts, not verdicts. The Stanford findings are early, descriptive signals, not proof that AI caused them. Research estimates for operators compare cities; they are not official counts.

Music
"Immersed" and "Reawakening" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

How this film was made
Written, animated and edited with AI tools (Claude by Anthropic) under the direction of the channel's human author, who approved every creative decision. Narration is a synthetic voice (ElevenLabs library voice, not a real person). Animation is stylised and not intended to depict real footage.
'''
open(sys.argv[2], 'w').write(txt); print(chap)

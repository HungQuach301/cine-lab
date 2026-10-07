#!/opt/cine/bin/python
"""Sinh mô tả YouTube tập 6 từ timeline (chương = mốc đoạn thật). python make_desc.py <timeline.json> <ra.txt>"""
import json, sys
tl = json.load(open(sys.argv[1]))
CH = {'00': 'A hand, or a machine?', '01': 'The print shop', '02': 'Hot type', '03': 'Cold type and paste-up', '04': 'The composing room, 1988',
      '05': 'The work moved', '06': 'A window still lit', '07': 'Can the BLS see it coming?', '08': 'Graphic designers today', '09': 'One freelance platform',
      '10': 'Same pattern, different hands', '11': 'The hand that decides', '12': 'The last lamp'}
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
chap = '\n'.join(f"{mm(s['t0'])} {CH[s['id']]}" for s in tl['segments'])
txt = f'''TITLE
The Computer Replaced the Typesetter and Made the Designer. Now AI Can Draw

DESCRIPTION
For most of a century, every word in a newspaper was set by hand. Then computers took over the typesetting, and in 1990 the Bureau of Labor Statistics wrote that more typesetting jobs were certain to disappear. The work did not vanish: graphic designers took the tool.

Today, the BLS projects that automated design tools, such as AI, will reduce the need for graphic designers: a projected decline of 1.7 percent from 2025 to 2035, while all jobs grow 3.5 percent. This film follows the hand that set the type and the hand that drew the page, and asks what is left for the hand that decides.

The street and its lamplighter are fictional. Every number on screen comes from the sources listed below. Archival photographs are from the Library of Congress (no known restrictions on publication).

Chapters
{chap}

Sources
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, 1990–91 Edition (Bulletin 2350): Compositors and Typesetters; Visual Artists
- James Bessen, "How Computer Automation Affects Occupations: Technology, Jobs, and Skills" (2016)
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, "Graphic Designers" (projections 2025–35); Employment Projections 2025–35
- Monthly Labor Review, February 2025 and January 2026 (BLS)
- Ozge Demirci, Jonas Hannane and Xinrong Zhu, "Who Is AI Replacing? The Impact of Generative AI on Online Freelancing Platforms", CESifo Working Paper 11276 (2024)
Photographs: Library of Congress, Prints & Photographs Division — FSA/OWI Collection (The New York Times composing room, 1942)
Projections are forecasts, not counts. The freelancing study counts job posts on one platform, not jobs.

Music
"Reawakening", "Gymnopedie No. 1" and "Clean Soul" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/
"Gymnopedie No. 1" composed by Erik Satie (1888, public domain), performed by Kevin MacLeod.

Sound effects (Freesound, CC0): simongray, kyles, Yuval, khenshom, artem_uanety, Jess_Weddle_6121, shelbyshark, OwlStorm, clairinski, Atrius1

How this film was made
Written, animated and edited with AI tools (Claude by Anthropic) under the direction of the channel's human author, who approved every creative decision. Narration is a synthetic voice (ElevenLabs library voice, not a real person). Animation is stylised (3D and 2D scenes built for this film); archival photographs are historical and credited on screen.
'''
open(sys.argv[2], 'w').write(txt); print(chap)

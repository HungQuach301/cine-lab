#!/opt/cine/bin/python
"""Sinh mô tả YouTube tập 5 từ timeline (chương = mốc đoạn thật). python make_desc.py <timeline.json> <ra.txt>"""
import json, sys
tl = json.load(open(sys.argv[1]))
CH = {'00': 'Who decides what a damaged car is worth?', '01': 'The claims desk', '02': 'A small army of clerks', '03': 'The computer comes to head office', '04': 'What about the claims desk?',
      '05': 'The line at judgment', '05b': 'The computer reaches the adjuster', '06': 'A person still had to look', '07': 'Claims adjusters today', '08': 'Auto damage appraisers',
      '09': 'How widely is AI used?', '10': 'Same claims desk, different jobs', '11': 'The line is moving', '12': 'The last lamp'}
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
chap = '\n'.join(f"{mm(s['t0'])} {CH[s['id']]}" for s in tl['segments'])
txt = f'''TITLE
In 1966, Computers Couldn't Judge an Insurance Claim. Now Software Prices the Wreck

DESCRIPTION
In the 1950s and 60s, insurance companies brought computers into head office. Routine record keeping went to the machine, but the Bureau of Labor Statistics drew a line: jobs requiring judgment and decision making, it said, could not be computerized.

Today, software can draft a damage estimate from a photo, and the BLS projects auto damage appraisers to shrink 9 percent by 2035. This film follows the claims desk from the clerks of 1964 to the adjusters of today, and asks where the line sits now.

The street and its lamplighter are fictional. Every number on screen comes from the sources listed below. Archival photographs are from the Library of Congress (no known restrictions on publication).

Chapters
{chap}

Sources
- U.S. Bureau of Labor Statistics, Bulletin 1468, "Impact of Office Automation in the Insurance Industry" (1966)
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, 1990–91 Edition (Bulletin 2350)
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, "Claims Adjusters, Appraisers, Examiners, and Investigators" (projections 2025–35); Employment Projections 2025–35
- Monthly Labor Review, February 2025 and January 2026 (BLS)
- National Association of Insurance Commissioners (NAIC), artificial intelligence survey of auto insurers (2022)
Photographs: Library of Congress, Prints & Photographs Division — FSA/OWI Collection (1936, 1941, 1943) and U.S. News & World Report Magazine Collection (1967)
Projections are forecasts, not counts. The NAIC survey counts plans as well as practice.

Music
"Immersed" and "Reawakening" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

How this film was made
Written, animated and edited with AI tools (Claude by Anthropic) under the direction of the channel's human author, who approved every creative decision. Narration is a synthetic voice (ElevenLabs library voice, not a real person). Animation is stylised; archival photographs are historical and credited on screen.
'''
open(sys.argv[2], 'w').write(txt); print(chap)

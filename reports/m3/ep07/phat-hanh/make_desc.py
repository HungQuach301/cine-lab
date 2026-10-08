#!/opt/cine/bin/python
"""Sinh mô tả YouTube tập 7 từ timeline (chương = mốc đoạn thật). python make_desc.py <timeline.json> <ra.txt>
Chỉ dùng năm/số có trong lời hoặc `numbers` (BAI-HOC #53, qc Q13). Số dự báo có chữ "projected" cùng câu."""
import json, sys
tl = json.load(open(sys.argv[1]))
CH = {'00': 'One word, three jobs', '01': 'A window still lit', '02': 'When a computer was a person', '03': 'A door, and a narrow one', '04': 'The war, and the West Area Computers',
      '05': 'The second kind of work', '06': 'Check the machine\'s numbers', '07': 'Where the people went', '08': '1990: a familiar forecast', '09': 'A light across the street',
      '10': 'The third kind of work', '11': 'Two job titles, two directions', '12': 'What the forecasts say', '13': 'The people just starting out', '14': 'The bottom of the ladder',
      '15': 'The name stayed; the work moved on', '16': 'The last lamp'}
mm = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'
chap = '\n'.join(f"{mm(s['t0'])} {CH[s['id']]}" for s in tl['segments'])
txt = f'''TITLE
When Computers Were People: One Word, Three Jobs

DESCRIPTION
Before electronic computers, "computer" was a job title: a person who did mathematical calculations by hand. In 1935, five women formed the first computer pool at the Langley aeronautical laboratory in Virginia; by 1946, about 400 women had been trained there. When electronic computers arrived, the human computers took on programming duties, and many moved on to programming and engineering. By 1988, computer programmers held 519,000 jobs in the United States.

Today the word names a third kind of work: people working beside a machine that can help write the code. The newest BLS projections expect computer programmers to shrink from 2025 to 2035, while software developers are projected to grow from 1.72 million to 1.89 million, 10.2 percent, compared with 3.5 percent projected for all jobs. A Stanford study finds that employment of workers aged 22 to 25 in AI-exposed jobs stands 19 percent below where it would be had it kept pace with less-exposed peers: a relative gap, mostly from fewer young people being hired. The name stayed; the work moved on. Where will the next beginners learn?

The street and its lamplighter are fictional. Every number on screen comes from the sources listed below. Archival photographs are NACA/NASA photographs (U.S. government works); their use does not imply endorsement by NASA.

Chapters
{chap}

Sources
- NASA History, "When the Computer Wore a Skirt: Langley's Computers, 1935–1970"
- NASA JPL, "When Computers Were Human"
- NASA, "From Computers to Leaders: Women at NASA Langley"
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook, 1990–91 Edition (Bulletin 2350): Computer Programmers
- Monthly Labor Review, February 2025 (BLS): "Incorporating AI impacts in BLS employment projections"
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook (projections 2025–35): Software Developers; Computer Programmers; Employment Projections 2025–35
- Erik Brynjolfsson, Bharat Chandar and Ruyu Chen, "Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence" (Stanford Digital Economy Lab, August 2026 update)
Photographs: NACA/NASA, NASA Image and Video Library (Langley Research Center, 1943–1959)
Projections are forecasts, not counts. The Stanford figure is a relative gap, not a count of jobs lost.

Music
"Reawakening", "Wholesome" and "Dreams Become Real" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

Sound effects
"Burroughs accounting machine" (Work With Sounds / Werstas), "Teleprinter: typing" (Work With Sounds / Konrad Gutkowski), "Relay-based interlocking for railway operation" (Work With Sounds / Torsten Nilsson), CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
Clock and projector field recordings: maciej janasik and Frank Schulte (radio aporee, public domain). Other effects: Freesound (CC0).

How this film was made
Written, animated and edited with AI tools (Claude by Anthropic) under the direction of the channel's human author, who approved every creative decision. Narration is a synthetic voice (ElevenLabs library voice, not a real person). Animation is stylised (3D and 2D scenes built for this film); archival photographs are historical and credited on screen.
'''
open(sys.argv[2], 'w').write(txt); print(chap)

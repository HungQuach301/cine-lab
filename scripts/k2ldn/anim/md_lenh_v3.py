#!/opt/cine/bin/python
"""ANIMATIC-T4-V2 · thư viện lệnh M-d v3 (22 clip mới/đổi của BANG-SHOT-v3) → channel-k2/k2c-t4-02/animatic2/omni/lenh/<ma>-anh.txt | -vid.txt + muc-luc.json.
Luật v1 (md_lenh.py: §15 f, cấm chữ/cờ/hiện đại, đúng thời kỳ, ĐÚNG ĐỘ DÀI bằng khung giờ) + nới theo chủ dự án 25/10/2026:
 · 06:56 (3) "đồng ý nới sử dụng Gemini và thêm các cảnh cận, trung để mô tả chân thực các sự kiện, nhân vật, công trình";
 · P2 = (b): nhân vật có tên ở khung TRUNG/XA, KHÔNG cận mặt (mặt ≤ 1/8 chiều cao khung), trang phục/dáng theo chân dung thật (ảnh tham chiếu — chỉ trang phục/dáng), chủ dự án duyệt từng clip;
 · công trình có tên được làm chủ thể (Old St Paul's, Royal Exchange, cầu London, Monument, Guildhall, St Paul's mới) — kiểm ĐỦ 2 tầng + câu bắt buộc
   "công trình mốc của năm đó có mặt chưa / có công trình chưa tồn tại không".
Không chữ/nhãn AI trong hình. Ảnh đầu: OpenAI gpt-image-2.5-sunburst-2026-09-08 (generations; có tham chiếu → edits image[]) — scripts/k2ldn/anim/oai_anh_v3.py."""
import json
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; OUT = REPO / 'channel-k2/k2c-t4-02/animatic2/omni/lenh'; NC = 'channel-k2/k2c-t4-02/nc/anh/'; TL = 'channel-k2/k2c-t4-02/tu-lieu/'
ANH = ("Photorealistic still frame from a high-end historical documentary reconstruction, shot on a 35 mm cinema camera, natural motivated light, "
       "soft atmospheric haze, muted warm palette, 16:9. ")
CAM_ANH = ("Strictly no text, letters, numbers, signs, posters, logos, watermarks or captions anywhere. No flags or banners. "
           "All people are seen full-figure at medium or long distance; every face is small (no face taller than one eighth of the frame height), natural and undistorted; no close-up portraits. "
           "No blood, no injured or dead people, no one inside the flames. Nothing from a later period than the year stated.")
CAM_ANH_1666 = " Nothing modern: no electric lights, wires, glass shopfronts, asphalt, road markings, vehicles with engines, steel structures, top hats, bowler hats or modern clothing."
REF = (" The attached reference portrait(s) are ONLY a guide for the period costume, wig, build and bearing of the named figure(s); do NOT copy the portrait's pose, framing or background, "
       "and do NOT render any face large or in close-up — the figures are small within a wide scene.")
VID = ("[# Sources <FIRST_FRAME>@Image1] Use the supplied image as the first frame and keep its composition, camera height, lighting, season, colours and period. "
       "One continuous unbroken shot, no cuts, no zoom jumps, real-time motion (not time-lapse). Natural documentary look. No dialogue, no music. ")
CAM_VID = ("Do NOT add any text, letters, numbers, signs, logos, watermarks or captions. Do NOT add flags or banners. Do NOT add any building, dome, spire, bridge or ship that is not already in the first frame. "
           "Do NOT add anything modern. Faces stay small, natural and undistorted; no close-ups of faces; the camera never moves closer to a face. No blood, no dead or wounded people, no person inside smoke or flames.")
CHAN = {'charles2': NC + 'met-435943-charles2-cooper.jpg', 'james': NC + 'rijks-200221267-james2-loggan.jpg', 'pepys': NC + 'wellcome-puwvaf8q-pepys.jpg'}
# ma: (năm, cảnh (cho bộ kiểm), ảnh đầu, chuyển động, [tham chiếu], mức kiểm, công trình mốc phải có / không được có)
L = {
 'H1-03b': (1647, "an artist sketching London from the tower of St Saviour's church, Southwark, 1647",
   "Afternoon in 1647, high on the flat lead roof of a church tower on the south bank of the Thames in London: an artist in a 1640s doublet, falling collar and wide-brimmed hat, seen from behind, sits at a drawing board sketching. Beyond him across the river spreads a low city of timber and plaster houses with dozens of church towers, and above them all on a hill the long roof and square crossing tower — with no spire — of a huge Gothic cathedral; the old bridge with houses built along it at the right. No dome anywhere.",
   "[0-6s] The artist's pen moves across the paper, the wind lifts the corner of the sheet, gulls glide over the river; the camera pushes slowly past his shoulder toward the city.", [], 'day_du',
   "must show: Old St Paul's Gothic cathedral with square tower and NO spire, NO dome; old London Bridge with houses; must NOT show any dome, Monument column or modern building"),
 'H1-04b': (1666, "Fish Street Hill, London, morning of Sunday 2 September 1666",
   "Morning, Sunday 2 September 1666: a steep narrow London street of tall timber-framed houses running down toward the river; residents in 17th-century clothes carry chests, bundles, bedding and chairs downhill; thick brown smoke and sparks blow across the rooftops from the right on a strong east wind.",
   "[0-6s] People hurry downhill carrying their goods, a woman drags a chest, a man shoulders a bundle; smoke streams right to left across the roofs; slow handheld drift down the street.", [], 'nen', ''),
 'H1-05a': (1666, "Whitehall Palace, 2 September 1666: the diarist reports the fire to the King",
   "Day, 2 September 1666, a panelled royal chamber at Whitehall Palace seen from across the room: a man in a plain brown coat and long brown periwig bows and speaks urgently to the tall, dark-haired King, who wears a long black curled periwig, lace cravat and dark coat; a courtier stands by the door; through a tall window a distant brown smoke plume rises over rooftops. Both men are full figures in the middle distance.",
   "[0-5s] The diarist gestures toward the window, the King turns toward the smoke and nods, the courtier steps aside; the camera stays at the far side of the room with a very slow drift.", ['charles2', 'pepys'], 'day_du', 'interior: no landmark required'),
 'H1-06x': (1666, "the royal barge on the Thames, afternoon of 2 September 1666",
   "Afternoon, 2 September 1666, on the River Thames in London, seen from another boat at a distance: a long royal barge with a carved, gilded canopy, rowed by oarsmen in red livery, carries a tall dark-haired man in a black curled periwig and a fair-haired man in a lighter periwig, both in rich 1660s coats, standing and pointing toward the north bank where timber riverside houses burn and brown smoke pours across the sky. The figures are small in the frame.",
   "[0-7s] The barge glides upstream, the oars dip in rhythm, the two men point at the burning bank and turn to the boatmen; smoke rolls across the sky; the camera floats low on the water alongside at a distance.", ['charles2', 'james'], 'day_du',
   'no bridge or cathedral needed; must NOT show any dome or modern building'),
 'H1-06b': (1666, "men pulling down a timber house with fire hooks, London, 2 September 1666",
   "Day, September 1666, a London street: a team of men in 17th-century working clothes, seen from behind at a distance, haul on ropes tied to long iron fire hooks hooked into the timber front of a jettied house; the plastered front cracks and leans outward; smoke beyond the rooftops.",
   "[0-5s] The men, seen from behind at a distance, heave together on the ropes; the timber front tears away and crashes into the street in a burst of dust and splinters.", [], 'nen', ''),
 'H1-07b': (1666, "London Bridge on the evening of 2 September 1666: the fire stops at the gap",
   "Evening, 2 September 1666, the old stone London Bridge seen low from the river: tall timber houses are built along the bridge; at the north end the houses burn fiercely, but the flames stop at an open gap in the row where houses were lost in an earlier fire, and the houses beyond the gap toward the south bank stand dark and untouched. The river rushes through the narrow arches.",
   "[0-6s] Flames roar on the northern houses and sparks blow across the open gap, but the houses beyond it stay dark; water rushes through the arches; slow sideways drift on the water.", [], 'day_du',
   'must show: old London Bridge with houses and an open gap; must NOT show any dome or modern bridge'),
 'H1-11b': (1666, "the courtyard of the Royal Exchange burning, 3 September 1666",
   "Afternoon, 3 September 1666, inside the courtyard of the Royal Exchange in London: a two-storey arcaded stone courtyard with a row of niches on the upper storey holding stone statues of English kings; fire burns through the upper gallery and roof, burning timbers fall, smoke fills the courtyard; no people.",
   "[0-6s] Flames run along the arcade roof, a burning beam falls into the courtyard, sparks swirl past the statues in their niches; slow push in.", [], 'day_du', 'must show: arcaded courtyard with statues of kings; must NOT show any dome'),
 'H1-13c': (1666, "Old St Paul's Cathedral catching fire in its scaffolding, night of 4 September 1666",
   "Night, 4 September 1666, London, seen from a street at the foot of a hill: the enormous Gothic Old St Paul's Cathedral — a very long nave and a square crossing tower with no spire — is wrapped in timber scaffolding along its walls; the scaffolding has caught fire and flames climb the poles toward the lead roof; burning houses around it light the scene orange.",
   "[0-6s] Flames race up the scaffolding poles, burning planks fall, fire reaches the edge of the roof; slow tilt up along the wall.", [], 'day_du',
   "must show: Gothic cathedral with square tower and NO spire and NO dome"),
 'H1-14': (1666, "the roof of Old St Paul's collapsing and molten lead running in the street, night of 4 September 1666",
   "Night, 4 September 1666, London: beside the burning Gothic cathedral (stone walls with tall pointed windows), the lead-covered roof of the nave sags and caves inward in fire; streams of glowing molten lead pour from the roof and run down the cobbled street in a bright stream; no people.",
   "[0-6s] A section of the roof caves in with a burst of sparks, molten lead pours down and runs along the street; heat haze shimmers; slow tracking shot along the stream.", [], 'day_du', 'Gothic cathedral walls only; must NOT show any dome'),
 'H1-15m': (1666, "houses blown up with gunpowder to make a firebreak, London, September 1666",
   "Day, September 1666, a London street of timber houses: a house is blown apart by gunpowder to open a firebreak — a burst of grey smoke, flying timbers and tiles; a few men in 17th-century clothes shelter at a safe distance behind a cart; fire glows beyond the rooftops.",
   "[0-6s] A sudden blast tears the house front apart, timbers and dust fly outward, the men duck behind the cart, then smoke drifts across the street; slow push in.", [], 'nen', ''),
 'H1-15b': (1666, "the garden of the Navy Office, London, 4 September 1666: burying wine and a cheese",
   "Evening, 4 September 1666, the small walled garden of the Navy Office in London, seen from across the garden: two men in 1660s coats and periwigs dig a pit in the earth by lantern light; beside them stand wine bottles in a basket and a large round wheel of cheese; a red glow of fire fills the sky above the rooftops. The men are small full figures.",
   "[0-7s] The two men shovel earth, one lowers the basket of bottles into the pit, the other carries the cheese over; the red sky flickers; very slow push in, staying at a distance.", ['pepys'], 'day_du', 'no landmark required; must NOT show any dome'),
 'H1-15x': (1666, "the King and the Duke of York working the fire-lines, London, 5 September 1666",
   "Day, 5 September 1666, a smoky London street: a tall dark-haired man in a black curled periwig and a fair-haired man in a lighter periwig, both in 1660s coats with sashes, work in a line of ordinary people passing leather buckets of water hand to hand toward burning timber houses; mounted guards in the background. Everyone is seen at a distance, full figure; faces small.",
   "[0-7s] Buckets pass along the line, the tall man hands a bucket on and points ahead, water splashes, the guards' horses shift; smoke drifts; slow lateral tracking shot at a distance.", ['charles2', 'james'], 'day_du', 'no landmark required; must NOT show any dome'),
 'H2-01b': (1666, "the fallen statue of Thomas Gresham in the ruins of the Royal Exchange, September 1666",
   "Day, September 1666, the ash-strewn ruin of an arcaded stone courtyard in London: broken arcades and empty niches; on the ground among the rubble lies one stone statue of a bearded man in Tudor merchant's gown and flat cap, fallen from its niche yet intact; thin smoke; no people.",
   "[0-5s] Thin smoke drifts across the fallen statue, flakes of ash fall; slow push in toward it.", [], 'day_du', 'ruined Royal Exchange courtyard; must NOT show any dome'),
 'H2-02b': (1666, "a new city plan unrolled on a table, September 1666",
   "Day, September 1666, close view of a wooden table by a window: a large hand-drawn plan of a city in brown ink, with straight avenues meeting at round open places, absolutely no readable writing or letters; a man's hands in lace cuffs of the 1660s unroll it and point along an avenue; a quill, an inkpot and brass dividers lie beside it.",
   "[0-5s] The hands smooth the plan flat and a finger traces a long straight avenue to a round open place; daylight; very slow push.", [], 'day_du', 'no landmark; the plan has no text'),
 'H2-06b': (1675, "the Monument column under construction, London, 1670s, Portland stone hoisted",
   "Day, 1675, London: a tall fluted stone column, half built, rises inside timber scaffolding next to a street of new brick houses; a large wooden treadwheel crane hoists a block of pale Portland stone up the side of the column; workmen in 1670s clothes guide it with ropes.",
   "[0-6s] The stone block rises slowly on the rope, the workmen guide it, the treadwheel turns; slow tilt up the column.", [], 'day_du', 'must show: an unfinished fluted column (the Monument); must NOT show any dome or modern building'),
 'H2-09x': (1675, "masons laying the first stone of the new cathedral on Ludgate Hill, 1675",
   "Day, 1675, on Ludgate Hill in London: masons in 1670s working clothes lower a large squared block of pale stone into a foundation trench with a wooden crane; behind them, the last broken walls of the old Gothic cathedral are being cleared; no dome yet.",
   "[0-6s] The stone block is lowered into the trench and settled, a mason checks it with a level and taps it; dust in the sunlight; slow push in.", [], 'day_du', 'must NOT show any dome (the new cathedral is not built yet)'),
 'H2-10b': (1708, "the last stone set on top of the lantern of St Paul's Cathedral, October 1708",
   "Day, October 1708, very high above London: two men in early 18th-century coats and periwigs stand on the narrow stone platform at the top of a lantern crowning a great dome, setting the last stone in place with mason's tools; far below spread the rooftops and church spires of London and the river; the men are small in the frame.",
   "[0-6s] One man lowers the last stone into place and taps it level, the other steadies it; wind tugs at their coats; slow orbit around them at a distance.", [], 'day_du', "must show: top of St Paul's lantern; no modern building below"),
 'H2-13': (1711, "the River Thames in 1711, wherries carrying passengers, the new dome of St Paul's on the skyline",
   "Day, 1711, low on the River Thames in London: small wooden wherries rowed by watermen carry passengers in early 18th-century clothes across the river; on the north bank beyond rises a low city of red brick houses and slender white church steeples, and above them the great new dome of St Paul's Cathedral with its lantern and cross, complete. There is no Gothic spire anywhere. No bridge in frame.",
   "[0-6s] The wherries cross slowly, oars dipping in rhythm, ripples catching the light; slow drift with the current.", [], 'day_du',
   "F1: skyline MUST show St Paul's new DOME with lantern; MUST NOT show any Gothic spire on a cathedral or any modern building"),
 'H3-05b': (1937, "a surveyor on a City rooftop sighting the dome of St Paul's, 1937",
   "Afternoon, 1937, on the flat roof of an office building in the City of London: a surveyor in a 1930s suit and trilby stands behind a brass theodolite on a wooden tripod, sighting toward the great dome of St Paul's Cathedral nearby; an assistant holds a striped measuring staff; seen from behind at a distance.",
   "[0-6s] The surveyor adjusts the theodolite and notes something in a small book, the assistant shifts the staff; clouds drift behind the dome; slow push in.", [], 'day_du', "must show St Paul's dome; no building later than 1937"),
 'H4-02b': (1940, "incendiary bombs falling on City rooftops at dusk, Sunday 29 December 1940",
   "Dusk, Sunday 29 December 1940, slate rooftops and a narrow street in the City of London: small incendiary bombs land and sputter on the roofs and pavement with white-hot flames and sparks; one rooftop begins to burn; smoke; no people close.",
   "[0-5s] Incendiaries clatter onto the roofs and burst into sputtering white flame, sparks fly, a roof catches; slow tilt down to the street.", [], 'nen', ''),
 'H4-04d': (1940, "the Guildhall roof burning, night of 29 December 1940",
   "Night, 29 December 1940: the medieval stone Guildhall in the City of London, its tall Gothic windows and pinnacled front lit by fire, while its timber roof burns; flames burst through the roof; firefighters in 1940s helmets spray hoses from the street below; orange sky.",
   "[0-5s] Flames roar through the roof, a section collapses in a shower of sparks, water arcs from the hoses; slow push in.", [], 'day_du', 'must show the Guildhall (Gothic front); no modern building'),
 'H5-01b': (1946, "two planners at a table with a plan and model of the bombed City, 1946",
   "Day, 1946, a drawing office with tall windows: two men in 1940s suits lean over a large table holding a hand-drawn town plan of a bombed city and a white card model of building blocks; seen at mid distance, faces not in close-up; no readable writing anywhere.",
   "[0-6s] One man moves a small card block on the model, the other points at the plan and nods; daylight; slow push.", [], 'day_du', 'interior: no landmark required'),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for k, (nam, canh, anh, vid, refs, muc, cm) in L.items():
        (OUT / f'{k}-anh.txt').write_text(ANH + anh + ' ' + CAM_ANH + (CAM_ANH_1666 if nam < 1850 else '') + (REF if refs else '') + '\n')
        (OUT / f'{k}-vid.txt').write_text(VID + vid + ' ' + CAM_VID + '\n')
    (OUT / 'muc-luc.json').write_text(json.dumps({k: {'nam': v[0], 'canh': v[1], 'tham_chieu': [CHAN[x] for x in v[4]], 'muc_kiem': v[5], 'cong_trinh_moc': v[6]} for k, v in L.items()}, ensure_ascii=False, indent=1))
    print(len(L))


if __name__ == '__main__': main()

#!/opt/cine/bin/python
"""ANIMATIC-T4 · thư viện lệnh minh hoạ M-d (Q3 điểm 4: thư viện lệnh + danh sách cấm) → channel-k2/k2c-t4-02/animatic/omni/lenh/<ma>-anh.txt (ảnh đầu, OpenAI) và <ma>-vid.txt (Omni).
Luật chung (§15 f, §14.1 c/f, §10.6 WW7): máy tầm người 0–40 m; không công trình có tên làm chủ thể; không nhân vật lịch sử có tên (người vô danh, nhìn từ xa/sau);
không chữ/nhãn/biển/cờ; không thi thể/máu/người trong lửa ở cận; đúng thời kỳ (danh sách cấm: scripts/k2ldn/ai/cam_thoi_dai.json). Clip ĐÚNG ĐỘ DÀI bằng khung giờ [0-Ns] (Q3 điểm 1)."""
import json
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; OUT = REPO / 'channel-k2/k2c-t4-02/animatic/omni/lenh'
ANH = ("Photorealistic still frame from a high-end historical documentary reconstruction, shot on a 35 mm cinema camera at eye level (about 1.7 metres), natural motivated light, "
       "soft atmospheric haze, muted warm palette, shallow depth of field, 16:9. ")
CAM_ANH = ("Strictly no text, letters, numbers, signs, posters, logos, watermarks or captions anywhere. No flags or banners. No famous or named landmark as the subject. "
           "People are anonymous ordinary residents seen at a distance or from behind or in profile, faces small and natural; no close-up portraits. No blood, no injured or dead people, no one inside the flames. "
           "Nothing modern: no electric lights, wires, poles, glass shopfronts, asphalt, road markings, vehicles with engines, steel structures or modern clothing.")
VID = ("[# Sources <FIRST_FRAME>@Image1] Use the supplied image as the first frame and keep its composition, camera height, lighting, season, colours and period. "
       "One continuous unbroken shot, no cuts, no zoom jumps, real-time motion (not time-lapse). Natural documentary look. No dialogue, no music. ")
CAM_VID = ("Do NOT add any text, letters, numbers, signs, logos, watermarks or captions. Do NOT add flags, banners, named or famous buildings, domes, spires, bridges or ships. "
           "Do NOT add anything modern. Faces stay small, natural and undistorted; no close-ups of faces. No blood, no dead or wounded people, no person inside smoke or flames.")
# ma: (năm, cảnh, ảnh đầu (chỉ phần riêng), chuyển động theo giây)
L = {
 'H1-01a': (1666, "Pudding Lane, London, 01:00 on Sunday 2 September 1666, a baker's shop",
   "Night, about one in the morning, September 1666, London. Inside a small 17th-century timber bakery: a brick bread oven with a glowing mouth, wooden peels, flour sacks and stacked faggots of firewood; a first small tongue of flame has caught the dry firewood beside the oven, orange light flickering on rough plastered walls; no people visible.",
   "[0-6s] The small flames beside the oven slowly spread along the stacked firewood, sparks lift, smoke curls along the low beamed ceiling; the camera drifts slowly closer."),
 'H1-01b': (1666, "a narrow lane outside the bakery in Pudding Lane, 1666, at night",
   "Night, September 1666, a very narrow London lane between tall timber-framed houses with overhanging upper storeys; orange firelight glows from the ground-floor window of one house, sparks drift upward; two or three neighbours in nightclothes and shawls, seen from behind, hold small candle lanterns and look up.",
   "[0-6s] Sparks rise from the lit window and drift left on a light east wind; the neighbours step back slowly, one points upward; firelight flickers on the timber beams; slow handheld drift backward."),
 'H1-02': (1666, "a London lane of timber houses whose upper storeys almost touch, night of 2 September 1666",
   "Night, September 1666, London: looking up a narrow lane where the jettied upper storeys of tall timber-framed houses almost touch overhead, leaving only a thin strip of dark sky; the first flames run along the eaves of one house and lick the overhang of the house opposite; no people.",
   "[0-8s] Flames creep along the eaves and jump across the narrow gap to the overhanging house opposite; embers fall into the lane; smoke thickens in the strip of sky; the camera tilts slowly up."),
 'H1-05a': (1666, "riverside stairs near the bridge, London, morning of 2 September 1666",
   "Morning, September 1666, the River Thames in London: wooden riverside stairs and a timber wharf crowded with ordinary people in 17th-century clothes passing bundles, chests and furniture down into flat wooden lighters; thick brown smoke rises behind the riverside houses; a light east wind.",
   "[0-6s] People hand chests and bundles down into the boats, one man throws a bundle of bedding into a lighter, a boatman steadies the boat with a pole; smoke drifts left across the sky."),
 'H1-05b': (1666, "loaded lighters pushing off from the riverbank, London, morning of 2 September 1666",
   "Morning, September 1666, low over the water of the Thames: two flat wooden lighters piled with furniture, chests and bedding, each rowed by a boatman, pull away from a timber wharf; brown smoke rises over the roofs of the riverside houses behind.",
   "[0-5s] The loaded lighters glide slowly away from the wharf, oars dip, small ripples; smoke rolls over the roofs and drifts left; the camera floats low on the water."),
 'H1-08a': (1666, "Bankside, south bank of the Thames, dusk on 2 September 1666, outside a small ale-house",
   "Dusk, September 1666, on the south bank of the Thames: a few ordinary people in 17th-century clothes, seen from behind, stand by the low river wall outside a small timber ale-house with a lantern over its door, watching an orange glow and smoke rising above the far bank across the dark water.",
   "[0-6s] The onlookers stand still, one pulls a shawl tighter; the glow across the river pulses brighter as dusk deepens; the lantern flame flickers; very slow push toward the river."),
 'H1-10': (1666, "Watling Street and Cheapside, London, Monday 3 September 1666",
   "Daytime, September 1666, a London street of timber houses jammed with hand carts and horse carts piled with goods, chests, bedding and furniture; people carry bundles, and two men carry a sick person in a chair; a pall of brown smoke dims the sun in the background.",
   "[0-7s] The carts edge forward slowly through the crowd, a horse tosses its head, the two men carry the chair through the press of people; smoke drifts across the hazy sun."),
 'H1-12': (1666, "the River Thames at night, 3 September 1666, the north bank on fire",
   "Night, September 1666, low on the River Thames: small wooden rowing boats and flat barges loaded with household goods, chests and bundles floating on the water; on the far north bank a long line of burning timber houses throws orange reflections across the river; no bridge visible.",
   "[0-6s] Boatmen row slowly through floating chests and bundles, the reflections of the fire shimmer on the water, sparks drift down to the river; slow drift sideways."),
 'H1-14': (1666, "a street near the great church, night of 4 September 1666, molten lead running in the gutter",
   "Night, September 1666, London: a cobbled street lit red by a huge fire out of frame; a stream of glowing molten lead runs down the central gutter of the street; scattered broken roof tiles and smoking debris; no people.",
   "[0-6s] The glowing molten lead flows slowly down the gutter, small droplets fall from above and hiss, heat haze shimmers, embers drift; the camera tracks slowly along the stream."),
 'H1-17a': (1666, "Moorfields, the open fields outside the London wall, 5 September 1666",
   "Day, September 1666, open grassy fields outside the old London city wall: crowds of homeless Londoners in 17th-century clothes camp among piles of rescued furniture, chests and bedding, with makeshift tents of sheets and simple shelters; smoke rises from the city beyond the wall.",
   "[0-6s] People sort their belongings, a woman shakes out a blanket, children sit on a chest, smoke drifts over the distant wall; slow lateral drift."),
 'H1-17b': (1666, "Moorfields at dusk, 5 September 1666, families at cooking fires",
   "Dusk, September 1666, Moorfields outside the London wall: families sit around small cooking fires among makeshift shelters made of sheets, poles and rescued furniture; a faint red glow in the sky over the city.",
   "[0-6s] Families warm their hands at the small fires, a pot steams, smoke from the cooking fires rises gently; the red glow in the sky pulses faintly; slow push in."),
 'H1-19': (1666, "the burnt City of London, 7 September 1666, smoking ruins",
   "Morning, 7 September 1666, inside the burnt City of London: a wide field of smoking ash and rubble, standing brick chimney stacks and fragments of stone walls, thin smoke rising everywhere under a pale sky; no people.",
   "[0-6s] Thin smoke rises and drifts from the ash; a fragment of wall crumbles; very slow push forward over the ruins."),
 'H2-01a': (1666, "a path through the still-warm ruins of London, September 1666",
   "Day, September 1666: a rough path picked through the warm ash and rubble of a burnt city, broken walls on either side, and in the distance the burnt-out shells of two church towers standing alone as landmarks; wisps of smoke; no people.",
   "[0-6s] Wisps of smoke rise from the ash, the camera walks slowly forward along the path toward the distant ruined towers."),
 'H2-01b': (1666, "Londoners searching the ruins, September 1666",
   "Day, September 1666: a few ordinary Londoners in 17th-century clothes, seen from a distance, pick through the rubble of burnt houses with sticks, looking for the lines of their old streets; thin smoke in the air.",
   "[0-6s] The people move slowly over the rubble, one lifts a blackened beam, another points along a line of foundations; smoke drifts; slow pan."),
 'H2-03a': (1667, "surveyors marking plots in the ashes of London, spring 1667",
   "Day, spring 1667, a cleared field of ash and old foundations in the burnt City of London: surveyors in 17th-century coats stretch measuring chains and drive wooden stakes to mark plot boundaries while two owners argue beside them; heaps of rubble and bricks.",
   "[0-8s] A surveyor pulls the chain taut, another hammers a stake into the ground, the two owners gesture and argue; a cart of rubble passes in the background."),
 'H2-04a': (1667, "bricklayers rebuilding London in brick, 1667-68",
   "Day, 1668, London: bricklayers on wooden scaffolding raise the new red-brick front wall of a house on an old street, hods of bricks and lime mortar, timber scaffold poles lashed with rope; neighbouring houses also rising in brick.",
   "[0-6s] A bricklayer lays a brick and taps it level, another climbs the ladder with a hod of bricks, mortar is spread; slow upward tilt."),
 'H2-04b': (1668, "a London street being rebuilt, 1668",
   "Day, 1668, a London street being rebuilt: horse carts unloading bricks, timber scaffolding on half-built brick houses, labourers carrying timber and mortar along the old line of the street.",
   "[0-6s] A cart rolls in and labourers unload bricks into a stack, others carry beams past; dust in the sunlight; slow lateral drift."),
 'H2-07': (1680, "a rebuilt London street in 1680 with an insurance fire mark on a house",
   "Day, 1680, a street of new red-brick houses with sash-less casement windows in London: a small plain metal plaque in the shape of a simple emblem, with no lettering, is fixed high on the front of one house above the door; a few passers-by in 1680s clothes.",
   "[0-7s] Passers-by walk past, a woman opens a door below the metal plaque, sunlight moves across the brick front; slow push in toward the plaque."),
 'H2-13': (1711, "the River Thames in 1711, wherries carrying passengers",
   "Day, 1711, low on the River Thames in London: small wooden wherries rowed by watermen carry passengers in early 18th-century clothes across the river; beyond, a low city of brick houses and slender church steeples along the bank under a soft sky; no bridge in frame.",
   "[0-6s] The wherries cross slowly, oars dipping in rhythm, ripples catching the light; slow drift with the current."),
 'H3-04b': (1935, "a narrow lane in the City of London in the 1930s",
   "Morning, 1935, a narrow old lane in the City of London between tall stone and brick office buildings of the 1900s-1930s: office workers in dark suits, bowler hats and overcoats walk to work; no shop signs or lettering visible.",
   "[0-7s] Office workers walk briskly along the lane, one lifts his hat, a messenger boy hurries past; morning light slants across the stone; slow forward drift."),
 'H4-01b': (1940, "an empty City of London street on Sunday afternoon, 29 December 1940",
   "Late afternoon in winter, Sunday 29 December 1940: an empty street of stone and brick office buildings in the City of London, locked doors, blacked-out windows, sandbags at a doorway; silver barrage balloons float in the cold sky; no lettering visible.",
   "[0-6s] A few dry leaves blow along the empty pavement, the barrage balloons sway slowly in the dusk sky, the light fades; very slow pan."),
 'H4-03': (1940, "firefighters on the Thames foreshore at low tide, night of 29 December 1940",
   "Night, 29 December 1940, London: firefighters in 1940s helmets and dark tunics drag canvas hoses across the wide mud of the Thames foreshore at low tide toward the distant water, the river barely reachable; the sky above the city glows orange with fires.",
   "[0-8s] The firefighters haul the heavy hose across the mud, boots sinking, one kneels at the hose coupling; the orange glow flickers on the wet mud; slow tracking shot."),
 'H4-04b': (1940, "volunteer fire-watchers on a lead roof at night, 29 December 1940",
   "Night, 29 December 1940: volunteer fire-watchers in 1940s helmets on a large lead-covered roof put out a sputtering incendiary bomb with a stirrup pump and a bucket of sand; the sky glows orange and smoke drifts past; the camera looks across the roof, not at any dome or tower.",
   "[0-6s] One volunteer pumps the stirrup pump, another tips sand onto the sputtering bomb, which dies down in smoke; sparks blow across the roof; slow push in."),
 'H5-07a': (2026, "people at the river wall on Bankside at night, 2026",
   "Night, 2026, the south bank of the Thames in London: a few people seen from behind lean on a stone river wall, looking across the dark river at the lights of the city on the far bank; soft reflections on the water; no readable signs.",
   "[0-6s] The people stand quietly, one points across the river, lights shimmer on the water, a small boat passes; very slow push toward the river."),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for k, (nam, canh, anh, vid) in L.items():
        (OUT / f'{k}-anh.txt').write_text(ANH + anh + ' ' + CAM_ANH + '\n')
        (OUT / f'{k}-vid.txt').write_text(VID + vid + ' ' + CAM_VID + '\n')
    (OUT / 'muc-luc.json').write_text(json.dumps({k: {'nam': v[0], 'canh': v[1]} for k, v in L.items()}, ensure_ascii=False, indent=1))
    print(len(L))


if __name__ == '__main__': main()

# Gibraltar town streets WWII: PD photo research (result: NEGATIVE for street level)

Date of research: 2026-10-18. Tools: Commons API, LoC JSON API. Raw wikitext in `wikitext/`, thumbnails in `img/`, API metadata in `meta.json`, scripts in `tools/`.

## 0. Headline findings
1. **No Commons file found that shows a Gibraltar TOWN street 1940-44 (Main Street, Commercial Sq) in PD wartime photography.** Searches in namespace 6 and categories (Gibraltar in WWII; Main Street; Air raid shelters in Gibraltar; Evacuation of Gibraltar; 1941/42/43/44 photographs of Gibraltar) return only: IWM military/naval/air photos, modern (2007+) street photos, stamps, and the Jamaica evacuee camp.
2. **The IWM "GM" and "A" files on Commons carry `{{PD-Scan|1=PD-UKGov}}` BUT the `permission` field verbatim says they were released "on the IWM Non Commercial Licence ... considered expired 50 years after their creation".** Commons treats them as PD (Crown copyright expiry), yet the source statement mentions the NC licence. Project rule (CLAUDE.md) forbids NC/ND for music/SFX; for reference photos used only as visual reference this is a RIGHTS.md judgement call for the project owner. Flag it.
3. **The only town-centre wartime images found are three 1939 shelter-construction photos in Commercial Square (= John Mackintosh Sq.)**: source is a Facebook page ("Gibraltar Old Photo"), author unknown, licence `{{PD-old}}` (weak provenance: unknown author, date "1939"). I could NOT view them: upload.wikimedia.org returned HTTP 429 (retry-after 600 s, persisting across ~45 min) after my bulk thumbnail downloads. Their stated pixel sizes: 494x304, 604x442, 555x475. Description verbatim: "Construction of an air raid shelter under John Mackintosh Square (then known as Commercial Square) in Gibraltar." Content therefore UNVERIFIED by eye. They should be opened by hand: https://commons.wikimedia.org/wiki/File:Commercial_Square_shelter_construction_2.jpg (also _3, and File:John_Mackintosh_Square_shelter_construction.jpg).
4. LoC JSON API reachable; "gibraltar" 1939-45 returned only Veterans History Project collections (afc2001001.*), not street photos. One LoC/NARA Signal Corps photo found (cemetery funeral, below). NARA not queried (budget/rate limit).

## 1. Photos examined (all downloaded thumbnails VIEWED unless marked NOT VIEWED)

| # | File title | Date | Id | Licence (verbatim) | Commons SHA-1 | Size | Visible |
|---|---|---|---|---|---|---|---|
| 1 | File:The British Army on Gibraltar 1941 GM63.jpg | 1 Nov 1941 | IWM GM 63 | `{{PD-Scan\|1=PD-UKGov\|category=}}` | 8faf7f87036100592c1c6a030f73b67a052c4207 | see meta.json | Soldiers drilling/quarrying inside a rock tunnel (compressor drill, hoses, rail, rubble, pickaxe). NOT street. Shirtless workers in trousers, field caps. |
| 2 | File:The British Army on Gibraltar 1941 GM121.jpg | Nov 1941 | IWM GM 121 | same | c5a05558324575c57148c429dae9421961990aab | | Airfield construction: caterpillar bulldozer, steam roller with canopy, gravel piles, Rock behind. Not town. |
| 3 | File:The British Army on Gibraltar 1941 GM20.jpg | 1939-45 | IWM GM 20 | same | 6e87f8f9fd643e67415445f316128451613cacea | | Interior: soldiers with stretcher on trestles (casualty post), steel helmets, khaki shorts, cable runs on ceiling. Not street. |
| 4 | File:The British Army on Gibraltar 1941 GM28.jpg | 1939-45 | IWM GM 28 | same | 826cdcf51641959b8e06e80b4372fb03454d1049 | | Tunnel hospital ward: wooden bunk beds, bandaged patients. Not street. |
| 5 | File:The British Army on Gibraltar 1941 GM90.jpg | 1939-45 | IWM GM 90 | same | a569cabc688743dc6ecc001f88d903dffd44697c | | Bofors-type AA gun pit on Rock above North Front, barbed wire, sentries, view of La Linea and beach. Not street. |
| 6 | File:The British Army on Gibraltar 1942 GM278.jpg | 4 Jan 1942 | IWM GM 278 | same | 5baadae05c0990574bcf8a66bfde84aa40dc7c34 | | 9.2-inch camouflaged coastal gun; harbour with ships (left), dockyard timber/structures (right). Not street. |
| 7 | File:The British Army on Gibraltar 1942 GM2015.jpg | 30 Nov 1942 | IWM GM 2015 | same | 38d724615c43489a1a648b70ec666aa52286883e | | Valentine tank marked "WELLINGTON" T27632 on unpaved road, lorry behind (Austin/Bedford-type, uncertain make), dry-stone wall, concrete marker post. Outside town (Europa/east side, uncertain). |
| 8 | File:The British Army on Gibraltar 1942 GM424.jpg | 1939-45 | IWM GM 424 | same | 79d46e07f22379d068201bde85757530c27d3457 | | Interior HQ/ops room cut in rock: officers, field telephone, "IN" tray, wooden table, Windsor chair, wire waste basket. Not street. |
| 9 | File:The British Army on Gibraltar 1942 GM428.jpg | 1939-45 | IWM GM 428 | same | bcc0225d23224c14732f9aab3cde6aeb1640ef96 | | Vickers MG in concrete pillbox, "No. 2 GUN" painted. Not street. |
| 10 | File:Gibraltar during the Second World War GM4392.jpg | 1939-45 | IWM GM 4392 | same | 524f3621f66a8d988f0377062894976473db3ace | 800x774 | 3.7-inch AA gun on Rock with sentry; view of La Linea (bullring visible), beach, barbed wire. Seen earlier in first batch (the 429-failed re-download did not complete; first Read failed, then I only saw it as the IWM-watermarked image). Not street. |
| 11 | File:Fleet Air Arm Personnel at Gibraltar. February 1944. A21819.jpg | Feb 1944 | IWM A 21819 | same | cbcc7d89a4183257291d2467281e0917ba55a133 | 768x800 | Portrait of RN officer with white-topped cap at an airfield (aircraft behind). Not street. |
| 12 | File:Funeral services for second Lieutenant Paul B. Bateman, American pilot, in Gibraltar.jpg | 1942-45 | LoC fsa.8e01069 (Signal Corps) | Permission=`{{PD-USGov}}` | 5e63017c60893f3be4c44365ebd6a67a8b3c3b02 | | Gibraltar North Front cemetery: gravel path, white headstones/crosses, trees, palm, flag-draped coffin, bearers, chaplain, cable coil. Not street; shows palm/trees, gravel paths, graves. |
| 13 | File:Sailors surround the ship's cat "Convoy" ... HMS HERMIONE ... A6410.jpg | 26 Nov 1941 | IWM A 6410 | `{{PD-Scan\|1=PD-UKGov\|category=}}` | 70e44fbfd8dec07c4d716226d27aa7fc635b8620 | | Shipboard (not viewed in detail; downloaded 187 KB, not used). Not street. |
| 14 | File:Commercial Square shelter construction 2.jpg | 1939 (claimed) | none (Facebook "Gibraltar Old Photo") | `{{PD-old}}` | 13ca1293417f2e78cc4328f5a64c8b1ede5d1a8e | 494x304 | NOT VIEWED (HTTP 429). Description only. |
| 15 | File:Commercial Square shelter construction 3.jpg | 1939 | Facebook | `{{PD-old}}` | b69ea6c4fe6dc5299c074fee14fd6c56fde96b61 | 604x442 | NOT VIEWED. |
| 16 | File:John Mackintosh Square shelter construction.jpg | 1939 | Facebook | `{{PD-old}}` | 2d63d3108ec14e9aafcb99871d312030e04f4739 | 555x475 | NOT VIEWED. |

Not viewed (429), IWM, same PD-Scan template: Leisure and Entertainment during the Second World War A14189 (sha1 87fe5ff6...), Captain J. Fitzgerald ... macaque GM 4452 (`{{PD-UKGov}}`, sha1 15de69c9...; Upper Rock apes, not street), GM93 (95dc2cce...), GM256 (004793e7...).
Excluded: "A.R.P Shelter, Gibraltar" (CC BY 2.0, 2011) and "ARP Shelter" (CC BY 2.0, 2007): modern, not PD.

Original URLs: see `meta.json` (field `url`, `page`, `sha1`). Wikitext of each: `wikitext/<name>.txt`.

## 2. Consolidated list: objects documented in TOWN STREETS 1940-44 from PD photos found
**None can be certified.** Nothing street-level was seen. Items visible in non-street context only (usable as period references, NOT as street furniture):
- Steel Brodie helmets, khaki shorts uniforms, web gear: #3, #8, #9.
- Wooden trestles, wooden bunks, Windsor chair, wire wastebasket (interior): #3, #4, #8.
- Dry-stone/whitewashed rubble walls, unpaved dusty road, military lorry (Valentine tank + lorry): #7.
- Barbed wire coils, concrete gun pits, sentries: #5, #10.
- Gravel paths, palm and trees, white headstones: #12.
- Corrugated/sheeted rock-cut structures, harbour dockyard timbers: #6.
Provisional only (UNVERIFIED, from description text, 1939): air-raid shelter works beneath Commercial Square, so the square was an excavation site in 1939; later state in 1943 is not documented here.

## 3. Searched for but NOT found
No PD photo found showing: sandbag walls at doorways/windows, blast walls, shelter entrances in streets, street signs, street lamps, kerbs, trams/buses/gharries/handcarts/bicycles, market stalls, shop awnings/shutters, balconies with plants, laundry, chickens/dogs/horses/mules/donkeys/goats, military police posts, water tanks, fire buckets, civilians/women/children in town streets, Main Street or Casemates Square in 1939-45. Searches "Gibraltar sandbags", "Gibraltar civilians IWM 1940 street", "Gibraltar Main Street soldiers sailors wartime", "Gibraltar harbour dockside 1943", "Gibraltarian evacuees quay 1940" returned zero files. Evacuation results are only the 1940s Jamaica camp (not Gibraltar streets). "Category:Main Street, Gibraltar" is modern/19th-c. only (e.g. "1870s - G Washington Wilson - Main Street", "1793 Main Street after the Siege"). Category:1944/1941 photographs of Gibraltar: empty.

## 4. Leads not completed (rate limit 429 from Wikimedia shared proxy IP)
- IWM Jan 1943 series "West End Stars at 'gib' Give Matinees For the Navy" (7 Jan 1943, Gibraltar, ENSA): 8 files in Category:1943 photographs of Gibraltar; may include harbour/quay. Not fetched.
- "Leisure and Entertainment ... A14189", "Beatrice Lillie ... Christmas party", "Vice Admiral Syfret ... A14161-3": navy, probably not street.
- Better sources probably outside Commons: Gibraltar Heritage Trust / GibraltarpediA, Gibraltar National Archives, IWM collections (blocked), Gibraltar-themed Pathe/IWM films (frames), Spanish archives, Wikimedia "Category:Evacuation of the Gibraltarians monument". Suggest owner uses hand-found photos with a clear source and adds to RIGHTS.md.

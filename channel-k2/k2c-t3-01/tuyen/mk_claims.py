"""T3 · gói TUYẾN · claim tuyến đường (T001…), cùng schema claims-vay-ham.json + trường `nguon_doi_chieu` (≥ 1 nguồn độc lập thứ hai).
Mọi câu trích là nguyên văn từ tệp tải bằng curl (ngoài git: /var/tmp/cine-out/tuyen/{src,web}/), SHA-256 tính lại lúc dựng.
Lỗi OCR giữ nguyên trong trích ("ſ"/"f" của bản in thế kỷ 18 giữ như OCR); "…" = bỏ một đoạn giữa (mỗi mảnh phải khớp tệp).
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/mk_claims.py  → tuyen/claims-tuyen.json, tuyen/claims-tuyen.md
Kiểm: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/verify_quotes_tuyen.py"""
import hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path('/var/tmp/cine-out/tuyen')
IA = 'https://archive.org/download/{0}/{0}_djvu.txt'

# Nguồn: khoá → (tệp thô, URL, mô tả, loại, phía, ngôn ngữ)
SRC = {
 'sayer':   ('src/historyofgibralt00sayeuoft_djvu.txt', IA.format('historyofgibralt00sayeuoft'), 'Capt. Frederick Sayer, The History of Gibraltar (London, 1862)', 'thu-cap', 'Anh', 'en'),
 'drink':   ('src/historysiegegibr00drin_djvu.txt', IA.format('historysiegegibr00drin'), 'John Drinkwater, A History of the Siege of Gibraltar 1779–1783, new ed. (London: John Murray, 1905; text of 1785)', 'so-cap', 'Anh', 'en'),
 'montero': ('src/historiadegibra00montgoog_djvu.txt', IA.format('historiadegibra00montgoog'), 'Francisco María Montero, Historia de Gibraltar y de su campo (Cádiz, 1860)', 'thu-cap', 'Tây Ban Nha', 'es'),
 'ancell':  ('src/acircumstantial00ancegoog_djvu.txt', IA.format('acircumstantial00ancegoog'), 'Samuel Ancell, A Circumstantial Journal of the Long and Tedious Blockade and Siege of Gibraltar (Liverpool, 1784)', 'so-cap', 'Anh', 'en'),
 'stephens':('src/historyofgibralt00step_djvu.txt', IA.format('historyofgibralt00step'), '[F. G. Stephens], A History of Gibraltar and its Sieges (London, 1870)', 'thu-cap', 'Anh', 'en'),
 'beatson5':('src/navalmilitarymem05beatuoft_djvu.txt', IA.format('navalmilitarymem05beatuoft'), 'Robert Beatson, Naval and Military Memoirs of Great Britain, from 1727 to 1783, vol. V (London, 1804)', 'thu-cap (gần đương thời)', 'Anh', 'en'),
 'clowes2': ('src/royalnavyhistory02clowuoft_djvu.txt', IA.format('royalnavyhistory02clowuoft'), 'W. Laird Clowes et al., The Royal Navy: A History, vol. II (London, 1898)', 'thu-cap (học thuật)', 'Anh', 'en'),
 'clowes3': ('src/royalnavyhistor03clow_djvu.txt', IA.format('royalnavyhistor03clow'), 'W. Laird Clowes et al., The Royal Navy: A History, vol. III (London, 1898; ch. "Major Operations 1762–1783" by A. T. Mahan)', 'thu-cap (học thuật)', 'Anh/Mỹ', 'en'),
 'schomb':  ('src/10281675bsb_djvu.txt', IA.format('10281675bsb'), 'Isaac Schomberg, Naval Chronology, vol. II (London, 1802)', 'thu-cap (gần đương thời)', 'Anh', 'en'),
 'fd6':     ('src/armadaespaolade00durogoog_djvu.txt', IA.format('armadaespaolade00durogoog'), 'Cesáreo Fernández Duro, Armada española desde la unión de los reinos de Castilla y de Aragón, tomo VI (Madrid, 1900)', 'thu-cap (học thuật)', 'Tây Ban Nha', 'es'),
 'fd7':     ('src/bub_gb_G1y3VAtRHTIC_djvu.txt', IA.format('bub_gb_G1y3VAtRHTIC'), 'Cesáreo Fernández Duro, Armada española desde la unión de los reinos de Castilla y de Aragón, tomo VII (Madrid, 1901)', 'thu-cap (học thuật)', 'Tây Ban Nha', 'es'),
 'mahon':   ('src/historyofwarofsu00stan_djvu.txt', IA.format('historyofwarofsu00stan'), 'Lord Mahon [P. H. Stanhope], History of the War of the Succession in Spain (London, 1836)', 'thu-cap (học thuật)', 'Anh', 'en'),
 'frus919': ('web/frus_d919.html', 'https://history.state.gov/historicaldocuments/frus1940v02/d919', 'FRUS 1940, vol. II, doc. 919 — Weddell (Madrid) to Secretary of State, 12 June 1940', 'so-cap (công văn ngoại giao)', 'Mỹ (bên thứ ba)', 'en'),
 'frus920': ('web/frus_d920.html', 'https://history.state.gov/historicaldocuments/frus1940v02/d920', 'FRUS 1940, vol. II, doc. 920 — Weddell (Madrid) to Secretary of State, 13 June 1940 (dịch sắc lệnh TBN ngày 12/6/1940)', 'so-cap (công văn ngoại giao, dẫn văn bản TBN)', 'Mỹ dẫn TBN', 'en'),
 'frus712': ('web/frus3_d712.html', 'https://history.state.gov/historicaldocuments/frus1940v03/d712', 'FRUS 1940, vol. III, doc. 712 — Weddell (Madrid) to Secretary of State, 14 June 1940 (dịch công hàm của Bộ Ngoại giao TBN)', 'so-cap (công văn ngoại giao, dẫn văn bản TBN)', 'Mỹ dẫn TBN', 'en'),
 'hs400619':('web/hd_fcaddc7c-5070-48da-a185-ee988eeb1e44.json', 'https://hansard-api.parliament.uk/debates/debate/fcaddc7c-5070-48da-a185-ee988eeb1e44.json', 'UK Hansard, Commons, "Tangier International Zone", 19 June 1940 — R. A. Butler (Under-Secretary, Foreign Office)', 'chinh-thuc', 'Anh', 'en'),
 'hs401113':('web/hd_cdba6c00-3f06-4eb0-b08b-587c14c8151f.json', 'https://hansard-api.parliament.uk/debates/debate/cdba6c00-3f06-4eb0-b08b-587c14c8151f.json', 'UK Hansard, Commons, "Tangier", 13 November 1940 — R. A. Butler', 'chinh-thuc', 'Anh', 'en'),
 'hs400820':('web/hs_ebe6c652.json', 'https://hansard-api.parliament.uk/debates/debate/ebe6c652-0e92-46d7-978c-7a49003c589e.json', 'UK Hansard, Commons, "War Situation", 20 August 1940 — Mr Cocks (Broxtowe)', 'chinh-thuc (phát biểu nghị sĩ)', 'Anh', 'en'),
 'hs421111':('web/hs_6460ce17.json', 'https://hansard-api.parliament.uk/debates/debate/6460ce17-cab4-4653-a83d-014ee1c5ee97.json', 'UK Hansard, Lords, Address in Reply, 11 November 1942 — Viscount Cranborne (Secretary of State for the Colonies)', 'chinh-thuc', 'Anh', 'en'),
 'hs410514':('web/hd_c57585b5.json', 'https://hansard-api.parliament.uk/debates/debate/c57585b5-6078-41c5-be4c-bc7b8433ace4.json', 'UK Hansard, Commons, "France and Germany (Agreement)", 14 May 1941 — Anthony Eden (Foreign Secretary)', 'chinh-thuc', 'Anh', 'en'),
 'frus41_109': ('web/frus41_d109.html', 'https://history.state.gov/historicaldocuments/frus1941v02/d109', 'FRUS 1941, vol. II, doc. 109 — French Ambassador (Henry-Haye) to the Secretary of State (công hàm phía Pháp, 1941)', 'so-cap (công hàm của chính phủ Vichy)', 'Pháp (Vichy)', 'en'),
 'frus41_90': ('web/frus41_d90.html', 'https://history.state.gov/historicaldocuments/frus1941v02/d90', 'FRUS 1941, vol. II, doc. 90 — Leahy (Vichy) to Secretary of State, 6 Feb 1941 (thuật lời Pétain)', 'so-cap (công văn ngoại giao)', 'Mỹ (thuật lời phía Pháp)', 'en'),
 'hmgog838': ('web/hmgog_838-2022.html', 'https://www.gibraltar.gov.gi/press-releases/exhibition-opened-to-mark-80-years-since-operation-torch-8382022-8438', 'HM Government of Gibraltar, Press Release 838/2022 (9 Nov 2022) — tải lại 17/10/2026 (SHA khác bản T3b: trang động; câu trích giống S122)', 'chinh-thuc', 'Gibraltar', 'en'),
 'howe4':   ('web/hw_nwa_4.html', 'https://www.ibiblio.org/hyperwar/USA/USA-MTO-NWA/USA-MTO-NWA-4.html', 'George F. Howe, Northwest Africa: Seizing the Initiative in the West (US Army in WWII, CMH, 1957), ch. IV (HyperWar transcription)', 'chinh-thuc (sử quân đội Mỹ)', 'Mỹ', 'en'),
 'howe11':  ('web/hw_nwa_11.html', 'https://www.ibiblio.org/hyperwar/USA/USA-MTO-NWA/USA-MTO-NWA-11.html', 'George F. Howe, Northwest Africa (CMH, 1957), ch. XI "The First Day\'s Operations Against Oran"', 'chinh-thuc (sử quân đội Mỹ)', 'Mỹ', 'en'),
 'howe13':  ('web/hw_nwa_13.html', 'https://www.ibiblio.org/hyperwar/USA/USA-MTO-NWA/USA-MTO-NWA-13.html', 'George F. Howe, Northwest Africa (CMH, 1957), ch. XIII "The Occupation of Algiers"', 'chinh-thuc (sử quân đội Mỹ)', 'Mỹ', 'en'),
}


def q(src, trich, vi_tri):
    return {'src': src, 'trich': trich, 'vi_tri': vi_tri}


# (id, nhóm, mục lệnh, claim_en, status, nguồn chính, [nguồn đối chiếu], phia, nhay_cam, ghi_chu)
C = [
 ('T001', 'tuyen-1704', 'a', 'The Anglo-Dutch fleet carrying the Habsburg claimant "Charles III" sailed from the Solent (St Helens, off Portsmouth) on 12 February 1704 (Old Style) and reached Lisbon on 25 February (O.S.) — the Spanish count gives the Tagus bar on 6 March (New Style).',
  'XÁC MINH',
  q('sayer', 'On the 12th of February the fleet set sail from St. Helens, and arrived at Lisbon on the 25th, after a favourable passage.', 'Ch. VI, tr. 100'),
  [q('clowes2', 'Sailing again on February 12th, with a very large convoy, it reached Lisbon on the 25th ; and King Charles landed a few days afterwards.', 'tr. 389–390'),
   q('fd6', 'franqueada la boca del puerto de Portsmouth el 1 6 de Enero de 1704, una y otra vez tuvo que arribar la escuadra en dispersión, tardando en alcanzar la barra del Tajo hasta el 6 de Marzo', 'cap. "1704-1705", tr. 48')],
  'Anh + TBN', 'THẤP',
  'Hai nguồn Anh dùng lịch cũ (O.S.); Fernández Duro dùng lịch mới (N.S.). 25/2 O.S. = 7/3 N.S. → lệch 1 ngày với "6 de Marzo" (barra del Tajo ≠ neo trong cảng); 16/1 N.S. (Fernández Duro) = 5/1 O.S. ≈ lần ra khơi đầu bị gió đẩy về (Clowes: "sailed on January 6th, but was driven back"). Cách nói an toàn: "sailed from England in February 1704 and reached Lisbon within two weeks". Không vẽ vòng Lisbon → Barcelona → quay lại (5–6/1704) trong SM1 (6 s); chỉ nêu ở mô tả.'),
 ('T002', 'tuyen-1704', 'a', 'In June 1704 Rooke, back from the Mediterranean, was joined off the Algarve coast (off Lagos, 16 June O.S.) by Sir Cloudesley Shovell\'s squadron.',
  'XÁC MINH',
  q('clowes2', 'Off Lagos, on the 16th, Admiral Sir Clowdisley Shovell\'s squadron joined.', 'tr. 391 (tháng 6/1704)'),
  [q('fd6', 'Por ello volvió á la costa de Portugal é hizo incorporar al almirante Shovel', 'tr. 51')],
  'Anh + TBN', 'THẤP',
  'Tên điểm "Lagos" chỉ Clowes nêu; Fernández Duro chỉ nói "costa de Portugal" → điểm mốc vẽ là "ngoài khơi Algarve gần Lagos", `approx: true`.'),
 ('T003', 'tuyen-1704', 'a', 'On 17 July 1704 (O.S.), with the fleet off Tetuan on the African shore, Rooke held a council of war on the Royal Catherine that decided on a sudden attack on Gibraltar; the fleet then crossed the Strait and anchored in the bay (S012).',
  'XÁC MINH',
  q('sayer', 'the admiral, on the 17th July, when within a few leagues of Tetuan, hove to the squadron and called a Council of War on board the flag-ship', 'Ch. VI, tr. 101'),
  [q('montero', 'Estando, pues, la -escuadra á la vista de las costas de Tetuan se celebró un consejo de guerra á bordo de la Real Catalina', 'tr. ~272'),
   q('clowes2', 'delayed the fleet, which, by July 17th, had not advanced eastward of Tetuan.', 'tr. 391'),
   q('fd6', 'hechos los preparativos en el fondeadero de Tetuán, pusiéronse á la vela para atravesar el Estrecho', 'tr. 52')],
  'Anh + TBN', 'THẤP', 'Bốn nguồn (2 Anh, 2 TBN) khớp. Điểm "off Tetuan" = ngoài khơi Martil (cảng của Tétouan), `approx: true`.'),
 ('T004', 'lien-minh-1704', 'b', 'The war of 1704 pitted the Grand Alliance — England, the Emperor (Austria) and the Dutch Republic — against France and the Spain of Philip V.',
  'XÁC MINH',
  q('sayer', 'was followed by the conclusion of the Grand Alliance, signed on September 7th, between England, the Emperor, and the Dutch. The alliance against Erance and Spain had scarcely been entered into when William III. died', 'Ch. VI, tr. 99'),
  [q('mahon', 'the basis of the “ Grand Alliance” between Eng- land, Austria, and the States General.', 'ch. I, tr. ~40'),
   q('fd6', 'Su defección alegró á los aliados contra la casa de Borbón', 'tr. 37')],
  'Anh + TBN', 'TRUNG BÌNH — chú giải phe: không gọi một bên là "Spain" chung chung; dùng "Spain (Philip V)" và "Grand Alliance".',
  'Đại Liên minh ký 7/9/1701 (Sayer). Fernández Duro gọi phe này là "los aliados contra la casa de Borbón" (đúng cách nhìn TBN). Gibraltar bị chiếm nhân danh "Charles III" (S012/S017) — chú giải SM1 phải giữ sắc thái này.'),
 ('T005', 'lien-minh-1704', 'b', 'Portugal joined the Grand Alliance in May 1703, recognising the Archduke Charles as King of Spain.',
  'XÁC MINH',
  q('mahon', 'A treaty between Portugal and the 3 allied powers was signed at Lisbon on the 6th of May acknowledging Charles as King of Spain, and - undertaking to vindicate his rights.', 'ch. II, tr. 69 (lề: "Portugal accedes to the Grand Alliance")'),
  [q('fd6', 'Alcanzó la influencia del procer castellano á mover el espíritu vacilante del Rey de Portugal y á entrarle en la gran liga contra España', 'tr. 33'),
   q('fd6', 'Firmóse el tratado en Londres el 10 de Mayo de 1703', 'tr. 33, chú thích')],
  'Anh + TBN', 'THẤP',
  'Khớp tháng (5/1703) và nội dung (nhượng Badajoz, Alburquerque, Tuy, Bayona, Vigo — cả hai nguồn). LỆCH ngày/nơi: Mahon "Lisbon, 6 May" ↔ Fernández Duro "Londres, 10 de Mayo" (có thể khác lịch O.S./N.S. và nơi phê chuẩn) → chỉ nói "May 1703". Bồ Đào Nha tuyên chiến TBN năm 1704 (Fernández Duro, mục lục chương 1704–05) — không cần cho SM1.'),
 ('T006', 'phong-toa-1779', 'c', 'From July 1779 the Spanish blockade squadron under Admiral Antonio Barceló was based at the anchorage off Algeciras, across the bay from Gibraltar; its aim was to cut the supplies reaching the Rock from the African shore.',
  'XÁC MINH',
  q('drink', 'they anchored in the bay, off Algeziras, and being judiciously arranged, and keeping a vigilant lookout, the garrison became closely blockaded.', 'Ch. III, tr. 58–59 (= S042)'),
  [q('drink', 'Admiral Barcelo returned from Ceuta to his old anchorage off Algeziras, and the port again became closely blockaded.', 'Ch. III, tr. ~79 (1779)'),
   q('montero', 'Mandaba las fuerzas sutiles marítimas Don Antonio Barceló, general acreditado y aptísimo para este intere- sante servicio del que dependía casi el éxito del bloqueo, encaminado principalmente á privar a la plaza de los vi- veres que le llegaban de las costas de África', 'tr. 338'),
   q('beatson5', 'retired to Algefiras, where Don Antonio Barcelo, with his line of battle {hips and frigates, hauled as clofe to the fhore', 'tr. 105 (1/1780)')],
  'Anh + TBN', 'THẤP', 'Căn cứ = Algeciras (cả hai phía). Barceló cũng dùng Ceuta (Drinkwater) → vòng phong toả vẽ bao cả Ceuta–Algeciras, nét đứt, không vẽ đường tàu cụ thể.'),
 ('T007', 'phong-toa-1779', 'c', 'Spanish lookouts and gunboats were stationed at Cabrita Point (Punta Carnero), the western horn of the bay, to signal and intercept ships entering from the Strait.',
  'XÁC MINH',
  q('drink', 'The usual signal for seeing an enemy was made by the Spaniards at Cabrita Point', 'Ch. III, tr. ~77 (1779)'),
  [q('montero', 'Cuando esta dobló la punta de Carnero (de cabrita la llaman loa in- gleses) salieron á impedirle el paso quince lanchas ca- ñoneras', 'tr. 346 (4/1781)'),
   q('fd7', 'las cañoneras de Barceló, situadas sobre Punta Carnero', 'tr. 330 (10/1782)')],
  'Anh + TBN', 'THẤP', 'Vị trí tuần tra cố định có nguồn: Punta Carnero/Cabrita Point (1779–82). Không có nguồn cho "đường tuần tra" ngoài eo → không vẽ.'),
 ('T008', 'phong-toa-1779', 'c', 'In January 1780 a Spanish squadron under Juan de Lángara cruised between the Strait and Cape St Vincent to stop relief reaching Gibraltar.',
  'XÁC MINH',
  q('montero', 'que al mando del general Don Juan de Lángara y Huarte cruzaba desde el Estrecho al cabo de San Vicente para impedir los socorros á la plaza bloqueada.', 'tr. 341'),
  [q('beatson5', 'a Spanifh fquadron, faid to confift of fourteen fail of the line, was cruifing off Cape St. Vincent', 'tr. 106')],
  'TBN + Anh', 'THẤP', 'Số tàu khác nhau: Beatson "said to consist of fourteen" (tin tình báo), Montero/Fernández Duro 9 tàu chiến tuyến + 2 frigate → không nói số tàu trong lời SM2.'),
 ('T009', 'tiep-te-1780', 'd', 'Rodney\'s relief fleet put to sea from England on 27 December 1779.',
  'XÁC MINH',
  q('beatson5', 'On the 27th of December, 1779, Sir George Rodney put to fea, with twenty fail of the line and nine fri- gates', 'tr. ~13 (mục Home 1780)'),
  [q('fd7', 'Rodney se hizo á la mar el 27 de Diciembre, escoltando con 22 navios de línea y 10 fragatas el convoy de 200 velas', 'tr. 253–254'),
   q('drink', 'she was one of a large convoy which had sailed the latter end of the preceding month for our relief', 'Ch. III, tr. 89')],
  'Anh + TBN', 'THẤP',
  'Cảng đi KHÔNG có nguồn nêu thẳng (Drinkwater chỉ ngầm: tàu than "too late … to join at Spithead"; Montero viết "Entrado el de 1780 salió de Londres" — sai rõ về ngày, coi là ngoại lệ). → Tuyến Rodney vẽ `vao_tu_mep: true`, nhãn "from England". Số tàu lệch (20–22 chiến tuyến) → không nói.'),
 ('T010', 'tiep-te-1780', 'd', 'Rodney captured a Spanish Caracas Company convoy (San Sebastián → Cádiz) on 8 January 1780; where it happened is disputed — "off the coast of Portugal" (Drinkwater, Fernández Duro) or "one hundred leagues E.N.E. of Cape Finisterre" (Beatson).',
  'MÂU THUẪN',
  q('drink', 'on the 8th of January Admiral Sir George Brydges Rodney had captured off the coast of Portugal, a Spanish 64-gun ship', 'Ch. III, tr. 90 (= S054)'),
  [q('fd7', 'descendió por la costa de Francia y golfo de Gascuña, sin encuentro de ene- migos, y continuando por la de Portugal, lo tuvo el 8 de Enero con otro convoy español', 'tr. 254'),
   q('beatson5', 'At day-break on the 8th, about one hun- dred leagues E. N. E. of Cape Finefterre', 'tr. 105')],
  'Anh + TBN', 'THẤP',
  'Ngày 8/1 khớp 3 nguồn. VỊ TRÍ mâu thuẫn: "E.N.E. of Finisterre" đặt điểm trong vịnh Biscay, "off Portugal" đặt điểm ngoài khơi Bồ Đào Nha. → KHÔNG vẽ điểm bắt đoàn tàu; tuyến chỉ đi "dọc bờ Bồ Đào Nha" (Fernández Duro) với `approx: true`.'),
 ('T011', 'tiep-te-1780', 'd', 'On 16 January 1780 Rodney\'s fleet rounded Cape St Vincent.',
  'XÁC MINH',
  q('beatson5', 'On the i6th in the morm\'ng, he paiTed that Cape with his whole fleet.', 'tr. 106'),
  [q('fd7', 'El 16 de Enero montó el cabo de San Vicente', 'tr. 254')],
  'Anh + TBN', 'THẤP', 'Điểm mốc chắc nhất của tuyến Rodney trước eo biển.'),
 ('T012', 'tran-1780', 'e', 'The "Moonlight Battle" of 16 January 1780 began south-east of Cape St Vincent; British accounts name it after Cape St Vincent, Spanish accounts (and the Gibraltar diarist Ancell) place the Spanish squadron off Cape Santa María, some 100 km further east.',
  'MÂU THUẪN',
  q('beatson5', 'About one in the afternoon, Cape St. Vincent bearing north, diftant four leagues, the Bedford -made the fignal for feeing a fleet in the fouth-eaft quarter.', 'tr. 106'),
  [q('fd7', 'allá por el cabo de Santa María avistaron sus descubridores velas sospechosas.', 'tr. 254'),
   q('ancell', 'which Admiral Rodney fell in with off Cape St. Mary\'s', 'thư tháng 1/1780, tr. 32'),
   q('montero', 'sin saber, por la niebla, que se encontraba en el cabo de \' Santa María.', 'tr. 341'),
   q('stephens', 'news of a fight off Cape St. Vincent between Rodney and Langara', 'tr. 257')],
  'Anh + TBN', 'TRUNG BÌNH — tên trận là của phía Anh ("Battle of Cape St Vincent"); TBN gọi theo Santa María.',
  'Hai cách gọi hoà giải được: Anh thấy địch lúc ~13:00 khi mũi St Vincent ở phía bắc 4 league (≈ 22 km) và đuổi về đông nam; TBN đang ở ngoài Santa María. Cuộc đuổi kéo tới đêm. → Vẽ VÙNG trận (elip) giữa hai mũi, nhãn "Moonlight Battle, 16 Jan 1780 (approx.)", không vẽ điểm đơn.'),
 ('T013', 'tiep-te-1781', 'd', 'Darby\'s relief fleet sailed in March 1781 — 13 March from St Helens/Spithead by the British count; the Spanish naval historian puts the sailing six days after 22 March.',
  'MÂU THUẪN',
  q('beatson5', 'On the 1 3th of March, Vice- Admiral Darby, with the fleet and the great convoys under his efcort, put to fea from St. Helen\'s.', 'tr. 325'),
  [q('clowes3', 'Admiral George Darby, sailed from St. Helen\'s on the 13th of INIarch, 1781, with a large convoy.', 'tr. 502'),
   q('schomb', 'On the 13th of March, Vice-Admiral Darby failed from Spithead with the channel fleet', 'tr. ~80 (1781)'),
   q('fd7', 'Con rumbo á las Occidentales partió la armada francesa el 22 de Marzo de 1781, y con ello desaparecía uno de los cuidados de los britanos; zarparon ellos con 400 velas seis días después', 'tr. 280')],
  'Anh + TBN', 'THẤP',
  'Ba nguồn Anh: 13/3 (St Helens/Spithead) — Clowes dẫn Beatson ở đoạn này, không hẳn độc lập. Fernández Duro: ~28/3 (có thể là ngày rời Cork). Drinkwater: tàu cutter rời Plymouth ~5/3 đã thấy hạm đội "at anchor in Torbay" → thêm một chặng dừng không khớp lịch → không vẽ Torbay. Cảng đi Spithead/St Helens có 3 nguồn Anh → vẽ được; bộ đếm SM2 ghi "Mar 1781", không ghi ngày.'),
 ('T014', 'tiep-te-1781', 'd', 'Darby went first to the coast of Ireland to pick up victuallers from Cork, then made for Gibraltar, passing Cape St Vincent and bringing-to off Cape Spartel on the evening of 11 April 1781 before entering the bay on the 12th.',
  'XÁC MINH',
  q('beatson5', 'His firft courfe was for the coaft of Ireland, where he met with fome little delay, before the fleet of victuallers joined him from Corke.', 'tr. 325'),
  [q('clowes3', 'Off Cork a number of victuallers joined', 'tr. 502'),
   q('beatson5', 'In the evening of the nth, Admiral Darby with the fleet, brought to off Cape Spartel', 'tr. 327'),
   q('clowes3', 'on the 11th of April the main expedition sighted Cape Spartel.', 'tr. 503'),
   q('drink', 'Captain Trollop, with the joyful news that the convoy was at the entrance of the Straits, under charge of Admiral Darby', 'Ch. IV, tr. 146')],
  'Anh', 'THẤP', 'Chặng Cork: Clowes dẫn Beatson (không độc lập hoàn toàn) → điểm "off Cork" `approx: true`. Chặng Spartel → vịnh: Beatson + Clowes + Drinkwater (độc lập) + Montero (đến 12/4, S055).'),
 ('T015', 'tiep-te-1782', 'd', 'Howe\'s relief expedition sailed from Spithead on 11 September 1782.',
  'XÁC MINH',
  q('clowes3', 'On the 11th of September the expedition started, 183 sail in all; thirty-four being ships of the line', 'tr. 540'),
  [q('schomb', 'Admiral Lord Howe failed', 'tr. ~84 (1782)'),
   q('schomb', 'from Spithead with a powerful fleet for the', 'tr. ~84 (1782)'),
   q('clowes3', 'it was determined to concentrate the whole Channel Fleet at Spithead, where also the transports and sup[)ly-ships were directed to rendez- vous.', 'tr. 540')],
  'Anh', 'THẤP', 'Schomberg OCR vỡ ngày ("r1ith") → trích hai mảnh; Clowes cho ngày 11/9. Không có nguồn TBN cho ngày đi (Fernández Duro chỉ nói "procedían de Occidente").'),
 ('T016', 'tiep-te-1782', 'd', 'Howe was off Cape St Vincent on 8 October 1782, entered the Strait on 11 October, but most transports missed the bay and were carried east into the Mediterranean; on 13 October the fleet lay off the Spanish coast near Fuengirola–Marbella before working back to land the stores (18 October).',
  'XÁC MINH',
  q('clowes3', 'On the 8th of October, oft" Cape St. Vincent, a frigate, the Latona, 38, was sent ahead for information.', 'tr. 540'),
  [q('schomb', 'difcovered by the Bri- tith fleet then off Fungarola', 'tr. ~85 (1782)'),
   q('montero', 'pero el fuerte poniente lo arrastro hasta las aguas de Marbella', 'tr. 368'),
   q('fd7', 'propasaron la punta de Europa, yendo adentro del Mediterráneo.', 'tr. 330'),
   q('clowes3', 'During the forenoon of the same da}\' the British were off the Spanish coast, fifty miles east of Gibraltar.', 'tr. 541')],
  'Anh + TBN', 'THẤP', 'Vị trí 13/10: Schomberg "off Fungarola" (≈ 70 km ĐĐB Gibraltar), Clowes "fifty miles east", Montero "aguas de Marbella" → khớp vùng; điểm mốc `approx: true`. Montero ghi thấy Gibraltar 12/10 (Anh: tối 11/10, S056) → bộ đếm ghi "11–12 Oct".'),
 ('T017', 'tran-1782', 'f', 'The fleet action of 20 October 1782 (British name: Cape Spartel) was fought west of the Strait towards evening; the Spanish naval historian places it in sight of Cape Spartel, while Montero and Córdoba\'s own report place it near Cádiz.',
  'MÂU THUẪN',
  q('fd7', 'A 20 de Octubre salían también de la estrechura los aliados', 'tr. 331'),
  [q('fd7', 'lo cual lograron al- gunos navios hacia las cinco de la tarde, estando á la vista de 1', 'tr. 331'),
   q('clowes3', 'On the following day, the 20th, towards sunset they bore down, and a partial engagement ensued; but it was wholly indecisive', 'tr. 542'),
   q('montero', 'Logró esta alcanzarla oí oeste de Cádiz y se empeñó una refriega entre ellas', 'tr. 369'),
   q('montero', 'El general Córdoba decia en su parte sobre el com- bate junto á Cádiz.', 'tr. 370')],
  'Anh + TBN', 'TRUNG BÌNH — kết quả trận "indecisive" theo cả hai phía; không nói "victory".',
  'Ngày 20/10 khớp (Clowes; Fernández Duro; Schomberg: rời eo 19/10, "the next morning" địch đuổi tới). Vị trí: Fernández Duro "á la vista de Cabo Espartel" (câu nối sang trang sau: "…estando á la vista de | Cabo Espartel") ↔ Montero/Córdoba "al oeste de Cádiz/junto á Cádiz". Clowes chỉ nói "outside" eo. → vẽ VÙNG (elip phủ từ ngoài Spartel tới ngoài Cádiz), nhãn "Cape Spartel, 20 Oct 1782 (approx.)".'),
 ('T018', 'ham-doi-1782', 'g', 'The combined French–Spanish fleet came in through the Strait from the west on the morning of 12 September 1782 and by afternoon lay at anchor between the Orange Grove and Algeciras — about fifty ships of the line by the Spanish count, 47 by the British.',
  'XÁC MINH',
  q('drink', 'that a large fleet had appeared in the Straits from the westward.', 'Ch. VII, tr. 291–292 (= S065)'),
  [q('drink', 'In the afternoon, they were all at anchor in the bay between the Orange Grove and Algeziras.', 'Ch. VII, tr. 292'),
   q('fd7', 'hasta el 12 no entró en la bahía la armada, alegrando la vista los 50 navios que se juntaron en Algeciras', 'tr. 328')],
  'Anh + TBN', 'THẤP', 'Hướng đến: "from the westward" (Drinkwater) → mũi tên vào từ cửa tây eo biển. Số tàu: 47 (Drinkwater) ↔ 50 (Fernández Duro, gồm tàu đã ở Algeciras).'),
 ('T019', 'ham-doi-1782', 'g', 'The date on which the combined fleet left Cádiz for Algeciras in September 1782 is not established in the sources read.',
  'CHƯA XÁC MINH',
  q('clowes3', 'an allied fleet of thirty-two ships of the line, five only of which were French, had sailed from Cadiz eai-ly in .June, to cruise between Ushant and Scilly.', 'tr. 539 (bối cảnh: tháng 6, KHÔNG phải chặng Cádiz → Algeciras)'),
  [],
  'Anh', 'THẤP',
  'Đã tìm: Drinkwater, Montero (chỉ nói các pin nổi đóng ở Cádiz "llegadas que fueron de Cádiz"), Fernández Duro t. VII, Clowes t. III, Schomberg t. II — không nguồn nào cho ngày rời Cádiz. → SM2 chỉ vẽ đoạn cuối "từ cửa tây eo → Algeciras" (T018), KHÔNG vẽ Cádiz → eo. Việc chờ: tra Gaceta de Madrid 9/1782 hoặc nhật ký Córdoba.'),
 ('T020', 'minorca-1782', 'h', 'Fort St Philip on Minorca hoisted the white flag on 4 February 1782; the capitulation was agreed and the garrison marched out on 5 February 1782, and the island passed to Spain.',
  'XÁC MINH',
  q('fd7', 'hasta ver ondear sobre ellas bandera blanca el 4 de Febrero de 1782. La capitulación quedó acordada el siguiente día', 'tr. 303'),
  [q('schomb', 'General Murray was under the neceflity of fur- rendering by capitulation, and the whole ifland fell under the dominion of Spain.', 'tr. ~82 (1782; ngày ghi ngay trước: "On the’sth of Fe- bruary")'),
   q('clowes3', 'Minorca, after a six moirths\' siege, capitulated in February, 1782.', 'tr. 504')],
  'TBN + Anh', 'THẤP',
  'Ngày chuẩn để đổi màu Minorca: **1782-02-05** (Fernández Duro + Schomberg; Clowes "February 1782"). OHM ghi 1782-01-05 (sai một tháng — có thể nhầm với ngày 6/1/1782 bắt đầu pháo kích, Fernández Duro tr. 303) và Cliopatria ghi 1781 (khoảng năm thô) → cả hai phải chỉnh tay. Montero tr. 352–353 lẫn sự kiện 1756 (Byng, Blakeney) vào 1781–82 → không dùng Montero cho Minorca.'),
 ('T021', 'wwii-1940', 'i', 'On 12 June 1940, two days after Italy entered the war, Franco\'s government declared Spain "non-belligerent" in place of neutral; the decree appeared in the Boletín Oficial on 13 June.',
  'XÁC MINH',
  q('frus920', 'The hostilities having extended to the Mediterranean by the entrance of Italy into war against France and England the Government has decided upon the non-belligerency of Spain in the conflict. Done in the Pardo the 12th of June, 1940.', 'tel. 186, 13/6/1940'),
  [q('hs400820', 'Spain at present under Nazi influence has ceased to be neutral and has become non-belligerent', 'cột Hansard 20/8/1940'),
   q('frus919', 'this might in the first phase at least, be manifest in an attitude of “non-belligerency” in place of the present “neutrality”', 'tel. 182, 12/6/1940 (bối cảnh trước sắc lệnh)')],
  'Mỹ dẫn văn bản TBN + Anh', 'TRUNG BÌNH — gọi đúng "non-belligerent", không gọi "Axis ally".',
  'Văn bản TBN gốc (BOE 13/6/1940) chưa tải được: bộ tìm Gazeta của BOE không nhận tham số qua curl (thử 2 lần, dừng theo BAI-HOC #12). FRUS dịch nguyên văn sắc lệnh. Nhãn bản đồ 1941: "Spain (non-belligerent)".'),
 ('T022', 'wwii-1940', 'j', 'On 14 June 1940 Spanish-commanded Moroccan (Khalifan) troops occupied the Tangier international zone, officially "provisionally" and in the Sultan\'s name; on 3 November 1940 the Spanish commander took over the zone\'s administration as Governor.',
  'XÁC MINH',
  q('hs400619', 'On 14th June, the Spanish High Commissioner at Tetuan notified the French Consul-General that, in agreement with the French Government, the Spanish Government intended to occupy Tangier at once.', 'Commons 19/6/1940'),
  [q('frus712', 'the High Commissioner of Tetuan was authorized to order Moorish [ Khalifan ] 16c troops, in the name of the Sultan, to occupy Tangier with that view. Said forces have orders to enter the Tangier Zone this morning.', 'tel. 192, 14/6/1940 (dịch công hàm Bộ Ngoại giao TBN)'),
   q('hs401113', 'On 3rd November the Officer Commanding the Spanish troops in Tangier published a notice stating that by reason of the present situation the Committee of Control, the Legislative Assembly, and the Mixed Bureau of Information would cease to function', 'Commons 13/11/1940')],
  'Anh + TBN (qua FRUS)', 'TRUNG BÌNH — "occupied" là chữ của cả Anh lẫn văn bản TBN; không nói "annexed".',
  'Bản đồ 1941: Tangier đổi từ "International Zone" (Cliopatria) sang "Spanish-occupied (from June 1940)" — tô màu TBN có gạch, nhãn chữ. Thời điểm kết thúc 1945 KHÔNG có claim → không ghi.'),
 ('T023', 'wwii-1942', 'k', 'On 8 November 1942 Allied forces landed in French North Africa — at and around Casablanca (French Morocco), Oran and Algiers (Algeria).',
  'XÁC MINH',
  q('hs421111', 'The Allied landings had been successfully effected, and effected with no very substantial losses, at Casablanca in French Morocco, at Oran, which is now in Allied hands, and at Algiers', 'Lords 11/11/1942'),
  [q('howe13', 'Landings at Algiers 8 November 1942', 'ch. XIII, bản đồ 3'),
   q('howe11', 'Operation RESERVIST was instead allowed to begin at 0245, 8 November', 'ch. XI (Oran)')],
  'Anh + Mỹ', 'THẤP', 'Bãi đổ bộ chi tiết (Safi, Fedala, Mehdia; Arzew, Les Andalouses; Castiglione, Sidi Ferruch, Surcouf) có trong Howe 1957 nhưng chưa có nguồn thứ hai từng bãi → SM3 chỉ vẽ ba KHU (Casablanca, Oran, Algiers), mũi tên vào bờ `approx: true`.'),
 ('T024', 'wwii-1942', 'k', 'Gibraltar was the command post and air base for Torch: Eisenhower and his staff flew in on 5–6 November 1942 and set up an advanced command post inside the Rock, and the first Twelfth Air Force Spitfires flew from Gibraltar to Tafaraoui (Oran) on 8 November.',
  'XÁC MINH',
  q('howe4', 'Deep within the Rock, in damp and limited quarters excavated during the previous year, General Eisenhower, Commander in Chief, Allied Force, and his principal staff, who flew from the United Kingdom to Gibraltar on 5 and 6 November in B-17\'s, set up an advanced command post.', 'ch. IV, tr. 76'),
  [q('hmgog838', 'General Eisenhower, who was the overall commander of Operation Torch, based his headquarters in tunnels deep inside the actual Rock itself.', 'đoạn 1–3 (= S122)'),
   q('howe11', 'When the first two squadrons of Twelfth Air Force Spitfires from Gibraltar were landed at 1630 at Tafaraoui', 'ch. XI, tr. ~211')],
  'Mỹ + Gibraltar (S122, S123)', 'THẤP',
  'Đối chiếu Gibraltar: HMGoG 838/2022 (= S122, độc lập với Howe) + S123 (Nghị viện Gibraltar: 650 máy bay đỗ dọc đường băng đêm 7/8/11/1942). Chuyến bay Gibraltar → Tafaraoui chỉ Howe nêu → mũi tên KHÔNG (air) `approx: true`, nhãn "Spitfires to Oran, 8 Nov".'),
 ('T025', 'wwii-1942', 'k', 'The Torch assault convoys did not start from Gibraltar: the Western Task Force sailed from Hampton Roads (USA) and the Centre and Eastern forces from the Clyde (Britain), entering the Mediterranean through the Strait.',
  'CHƯA XÁC MINH',
  q('howe4', 'all combat-loaded ships from the United States departed from the Hampton Roads Port of Embarkation.', 'ch. IV'),
  [],
  'Mỹ', 'THẤP',
  'MỘT nguồn (Howe 1957, cũng nêu "returned to the Clyde" cho lực lượng Anh). Chưa tìm nguồn thứ hai (công văn Cunningham, London Gazette 38204 — chưa tải). Hệ quả cho SM3: KHÔNG vẽ tuyến đoàn tàu "từ Gibraltar" (sẽ sai); tuyến biển Torch chỉ vẽ đoạn cuối qua eo, `vao_tu_mep: true`, không nhãn nơi đi.'),
 ('T026', 'wwii-1941', 'ranh-1941', 'In 1941 metropolitan France was divided by a "line of demarcation" into a German-occupied zone and an unoccupied zone administered by the government at Vichy.',
  'XÁC MINH',
  q('hs410514', 'for the alleviation of the restrictive measures regarding the line of demarcation between occupied and unoccupied France', 'Commons 14/5/1941'),
  [q('frus41_109', 'despite the line of demarcation, the economic unity of France', 'công hàm Đại sứ Pháp, 1941'),
   q('frus41_90', 'The Germans, said the Marshal, are using the line of demarcation as a bit in the horse’s mouth', 'tel. 164, Vichy 6/2/1941')],
  'Anh + Pháp (Vichy, qua FRUS)', 'CAO — không dùng biểu tượng chế độ; nhãn chữ "German-occupied France" / "Vichy France"; vùng chiếm đóng tô xám-nâu gạch (NC-BD §3.3.7).',
  'Claim bổ sung (không có trong a–k của lệnh) vì ranh-gioi.json 1941 dùng nhãn "German-occupied France"/"Vichy France". Đường phân giới lấy theo Cliopatria 1941 (có vùng chiếm đóng); OHM 1941 tô cả nước là "French State" → không dùng OHM cho đường này. Hình dạng đường phân giới KHÔNG được claim kiểm (chỉ sự tồn tại hai vùng) → nhãn "approx. borders c. 1941".'),
]


def vitri(d):
    import tim
    ok, fr, L, pg = tim.locate(RAW / SRC[d['src']][0], d['trich'])
    assert ok, (d['src'], d['trich'][:60])
    base = re.sub(r'(,\s*)?tr\.\s*~?[\d–-]+(\s*\([^)]*\))?', lambda m: (' ' + m.group(2).strip()) if m.group(2) else '', d['vi_tri']).strip(' ,;')
    return (base + ' · ' if base else '') + f'tệp dòng {L}' + (f' · tr. in theo đầu trang OCR gần nhất: {pg}' if pg else ''), ('khớp nguyên khối' if '…' not in d['trich'] else f'khớp theo mảnh {fr}')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sys.path.insert(0, str(HERE))
    shas = {k: sha(RAW / v[0]) for k, v in SRC.items()}
    out = []
    for cid, nhom, muc, en, st, chinh, doi, phia, nhay, ghi in C:
        f, url, ten, loai, ph, lang = SRC[chinh['src']]
        vt, kd = vitri(chinh)
        out.append({
            'id': cid, 'id_goc': f'TUYEN-{muc}', 'nhom': nhom, 'claim_en': en, 'trich_nguyen_van': chinh['trich'], 'lang': lang,
            'nguon': ten, 'loai_nguon': loai, 'url': url, 'file_sha256': shas[chinh['src']], 'vi_tri': vt,
            'as_of': 'đọc 2026-10-17', 'phia': phia, 'status': st, 'nhay_cam': nhay, 'ghi_chu': ghi, 'kiem_doc_lap': kd + ' (tim.py, tệp có đúng SHA)',
            'nguon_doi_chieu': [{'nguon': SRC[d['src']][2], 'loai_nguon': SRC[d['src']][3], 'phia': SRC[d['src']][4], 'lang': SRC[d['src']][5],
                                 'url': SRC[d['src']][1], 'file_sha256': shas[d['src']], 'vi_tri': vitri(d)[0], 'trich_nguyen_van': d['trich']} for d in doi],
            'muc_lenh': muc,
        })
    nguon = [{'key': k, 'url': v[1], 'file': str(RAW / v[0]), 'sha256': shas[k], 'bytes': (RAW / v[0]).stat().st_size, 'note': v[2]} for k, v in SRC.items()]
    doc = {'note': 'Claim tuyến đường T3 (gói TUYẾN, 17/10/2026). Schema = claims-vay-ham.json + `nguon_doi_chieu` (nguồn độc lập thứ hai trở đi) + `muc_lenh` (a–k của lệnh). Tệp thô ngoài git, SHA ở `nguon_da_tai`.',
           'claims': out, 'nguon_da_tai': nguon}
    (HERE / 'claims-tuyen.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
    from collections import Counter
    print(len(out), dict(Counter(c['status'] for c in out)))


if __name__ == '__main__':
    sys.exit(main())

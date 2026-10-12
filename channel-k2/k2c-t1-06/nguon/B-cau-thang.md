# Cluster B: Building codes (stairs, exits, elevators) and single-stair reform

Researcher notes for "Why US Cities Stopped Building the Corner Apartment Block".
Access date for every source: **2026-10-12**. All raw files are in this folder (`src/B/`).
How read: "curl" means curl with `-A 'Mozilla/5.0 (research)'` unless noted, then pdftotext/HTML-to-text. "curl-UA2" means the research UA returned 403 and a plain Chrome UA string was used instead. "WebFetch" is noted where used.
Quotes are verbatim from the saved files (line-wrap hyphens removed only).

**Access problems (honest log)**
- codes.iccsafe.org: research UA got **403 (CloudFront)**, and WebFetch also got 403. A Chrome UA got HTTP 200, but the page is a **reCAPTCHA wall** (`icc_captcha_page.html`). **I could not read the ICC site directly.** The model IBC text below comes from official government adoptions that reprint the IBC (Seattle SBC 2021, WA WAC, an ICC proposal reprinted by WA SBCC).
- pew.org report page and full-report PDF: 403 by curl and WebFetch. I read Pew's own **summary PDF** (it opened).
- leginfo.legislature.ca.gov (AB 835): 403 by curl and WebFetch. AB 835 facts are taken from the CAL FIRE/OSFM report instead.
- Montana SB 213 (2025) and NH SB 282 (2025): I could not reach an official page (legmt archive 404s, gc.nh.gov sent an empty reply). Only the CBNA tracker covers them (advocacy source).
- centerforbuilding.org: one connection reset; it worked on retry.

---

## B01 Seattle Building Code 2021, Chapter 10 (reprints IBC 2021 with Seattle [S] and Washington [W] amendments)
- Citation: City of Seattle SDCI, *2021 Seattle Building Code*, Chapter 10 Means of Egress.
- URL: https://www.seattle.gov/documents/Departments/SDCI/Codes/SeattleBuildingCode/2021SBCChapter10.pdf
- File: `seattle_sbc2021_ch10.pdf/.txt`. How read: curl, pdftotext.
- **Model IBC 2021 base text.** Table 1006.3.4(1) carries no [S]/[W] marker, so it is unamended IBC 2021 text:
  > "TABLE 1006.3.4(1) STORIES WITH ONE EXIT OR ACCESS TO ONE EXIT FOR R-2 OCCUPANCIES ... Basement, first, second or third story above grade plane | R-2a, b | 4 dwelling units | 125 feet ... Fourth story above grade plane and higher | NP | NA | NA"
  > "a. Buildings classified as Group R-2 equipped throughout with an automatic sprinkler system in accordance with Section 903.3.1.1 or 903.3.1.2 and provided with emergency escape and rescue openings in accordance with Section 1031."
  > "1006.3.3 Egress based on occupant load. Each story and occupied roof shall have the minimum number of separate and distinct exits, or access to exits, as specified in Table 1006.3.3 ... 1-500 | 2"
  > "1006.3.4 Single exits. A single exit or access to a single exit shall be permitted from any story or occupied roof where one of the following conditions exists: 1. The occupant load, number of dwelling units and exit access travel distance within the portion of the building served by the single exit do not exceed the values in Table 1006.3.4(1) or 1006.3.4(2)."
- **Seattle's 6-story allowance** (item 7 of [W][S] 1006.3.4):
  > "7. Not more than 5 stories of Group R-2 occupancy are permitted to be served by a single exit under the following conditions: 7.1. The building has not more than six stories above grade plane. 7.2. The building does not contain a boarding house. 7.3. There shall be no more than four dwelling units on any floor. 7.4. The building shall be of not less than one hour fire-resistive construction and shall also be equipped throughout with an automatic sprinkler system in accordance with Section 903.3.1.1. ... 7.5. There shall be no more than two single exit stairway conditions on the same property. 7.6. An exterior stairway or interior exit stairway shall be provided. The interior exit stairway ... shall be pressurized in accordance with Section 909.20.6. ... 7.8. There shall be no more than 20 feet (6096 mm) of travel to the exit stairway from the entry/exit door of any dwelling unit. 7.9. Travel distance measured in accordance with Section 1017 shall not exceed 125 feet."
- Elevator trigger (marked [W][S], so possibly amended):
  > "1009.2.1 Elevators required. In buildings where a required accessible floor or accessible occupied roof is four or more stories above or below a level of exit discharge, not less than one required accessible means of egress shall be an elevator complying with Section 1009.4."

## B02 Seattle Building Code 2021, Chapter 30 (elevators); Seattle-specific stretcher rule
- URL: https://www.seattle.gov/documents/Departments/SDCI/Codes/SeattleBuildingCode/2021SBCChapter30.pdf. File: `seattle_sbc2021_ch30.*`. How read: curl.
  > "3016.15 Elevator car to accommodate ambulance stretcher. In buildings provided with an elevator, at least one elevator shall provide fire department emergency access to all floors served in: 1. Buildings four or more stories above or below grade plane, and 2. Any R-1, R-2 or I occupancy building regardless of the number of stories. The elevator car shall be of a size and arrangement to accommodate a 24-inch by 84-inch (610 mm by 2134 mm) ambulance stretcher with not less than 5-inch (127 mm) radius corners, in the horizontal, open position."
- Caveat: this is Seattle's own section number and wording, not the model IBC (in the IBC the equivalent is 3002.4, which I did not read).

## B03 Washington WAC 51-50-1006, 2021 archive version (WA adoption of the IBC 2018-based state code; numbering 1006.3.3)
- URL: https://lawfilesext.leg.wa.gov/Law/WACArchive/2021/htm/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2050%20%20CHAPTER/WAC%20%2051%20-%2050%20-1006.htm
- File: `wac51-50-1006_2021.*`. How read: curl.
  > "Table 1006.3.3(1) Stories with One Exit or Access to One Exit for R-2 Occupancies ... Basement, first, second, or third story above grade plane | R-2 a,b | 4 dwelling units | 125 feet | Fourth story above grade plane and higher | NP | NA | NA"
- Current WAC 51-50-1006 (`wac51-50-1006_current.*`, https://app.leg.wa.gov/WAC/default.aspx?cite=51-50-1006, curl 200) uses the IBC 2021 numbering "1006.3.4 Single exits" ... "Table 1006.3.4(1)". History line: "effective 3/15/24".

## B04 NYC Building Code 2022, Chapter 10 (official NYC DOB)
- URL: https://www.nyc.gov/assets/buildings/codes-pdf/cons_codes_2022/2022BC_Chapter10_EgressWBwm.pdf (found through the DOB pdf_viewer's JS path map).
- File: `nyc_bc2022_ch10.*`. How read: curl. Header: "Chapter 10 was amended by Local Law 77 of 2023. This law has an effective date of June 10, 2023."
  > "6. Buildings of Occupancy Group R-2 where all of the following conditions are met: 6.1. The building does not exceed four stories; 6.2. The building contains not more than three dwelling units per story; 6.3. The building is of construction Type I or II; 6.4. The building does not exceed 2,500 square feet (232.3 m2) per story; ... 6.8. The building is equipped throughout with an automatic sprinkler system in accordance with Section 903.3.1.2."
  > "7. Buildings of Occupancy Group R-2 of construction Type I or II not exceeding six stories and not exceeding 2,000 square feet (185.8 m2) per story."
- Table 1006.3.2 (NYC): R-2 on the second and third stories, max travel distance "50" ft; footnote "d. Maximum four dwelling units per floor."
- "Since 1938" appears only in the CBNA tracker (B16). I have no official source for that date.

## B05 WABO proposal 24-SEP-001 to WA State Building Code Council (Aug 28, 2024), "Appendix Q: Single Exit Provisions for Multifamily up to 6 stories"
- URL: https://sbcc.wa.gov/sites/default/files/2025-03/24-SEP-001.pdf. File: `sbcc_24-SEP-001.*`. How read: curl. Proponent: Washington Association of Building Officials. Contact: Ardel Jala, Seattle building official.
  > "The 2021 Washington State Building Code Table 1006.3.4(1) permits a single exit R-2 occupancy building up to 3 stories in height."
  > "A version of these provisions has been in the Seattle codes for quite some time dating back to the 1977 Seattle Building code, driven by the development happening at the time. There were many small lots being developed in the city and two exits took up a significant portion of the floor plate. The 'Seattle Special' as it came to be known, was developed with a reliance on the Seattle fire department's quick response times and the reliability of the municipal water supply."
  > "Since there is no redundancy with the single stair, these provisions offset this by limiting the amount of time it takes to get out of the building, and by providing a well-protected egress environment from the point you leave your unit to the street."
  > (user note) "Not all agencies will have the appropriate aerial apparatus, personnel, or water supply to adequately respond to a structure designed using this appendix."

## B06 Washington SSB 5491, Chapter 372, Laws of 2023 (session law PDF)
- URL: https://lawfilesext.leg.wa.gov/biennium/2023-24/Pdf/Bills/Session%20Laws/Senate/5491-S.SL.pdf. File: `wa_sb5491_sl_2023.*`. How read: curl. The bill summary page (app.leg.wa.gov/billsummary) also returned 200 by curl: `wa_sb5491_billsummary.*` ("Governor signed. Chapter 372, 2023 Laws. Effective date 7/23/2023.").
  > "Approved May 9, 2023 11:14 AM" ... "EFFECTIVE DATE: July 23, 2023" ... "Passed by the Senate April 18, 2023 Yeas 48 Nays 1" ... "Passed by the House April 10, 2023 Yeas 96 Nays 1"
  > "(1) The state building code council shall convene a technical advisory group for the purpose of recommending modifications and limitations to the international building code that would allow for a single exit stairway to serve multifamily residential structures up to six stories above grade plane. The recommendations must include considerations for adequate and available water supply, the presence and response time of a professional fire department, and any other provisions necessary to ensure public health, safety, and general welfare."
  > "(2) ... The council shall take action to adopt additions and amendments to rules or codes as necessary by July 1, 2026."

## B07 WA SBCC CR-102 proposed rule, WSR 26-10-068 (2024 IBC adoption), filed May 2026, with new Appendix T (single exit)
- URL: https://sbcc.wa.gov/sites/default/files/2026-05/CR-102_WSR%2026-10-068_RDS-7071.3_Combined.pdf. File: `wa_cr102_ibc_wsr26-10-068.*`. How read: curl.
  > "51-50-5500 IBC Appendix T | New Washington Appendix | Single Exit Appendix created to respond to SB 5491 of the 2023 Legislature"
  > "Appendix T developed by the state of Washington is included in the adoption of the International Building Code."
  > "T101.1 Scope. Appendix T applies statewide to structures served by a professional fire department meeting the requirements of Section T102.1."
  > "T102.2 ... not more than five stories of Group R-2 apartment houses are permitted to be served by a single exit under the following conditions: 1. The building has not more than six stories above grade plane. ... 5. There shall be no more than 20 units served by the single exit. ... 7. The building shall be equipped throughout with an automatic sprinkler system in accordance with Section 903.3.1.1."
  > "Date of intended adoption: August 28, 2026 (Note: This is NOT the effective date)"
- **Status as of 2026-10-12** (SBCC homepage `sbcc_home.*`, curl): "The SBCC filed CR-102 for the International Building Code ... on May 6, 2026 ... Final adoption for these codes is targeted for October 16, 2026 ... The effective date of the 2024 codes will be May 3, 2027." **So it is proposed, not yet finally adopted.**
- Supporting: TAG final draft (Feb 2026) `sbcc_SingleExitAppendix_TAGFinal_20260203.*`. TAG page `sbcc_semh_tag.*` lists "Single Exit Appendix: Recommendation for CR-102".

## B08 ICC code change proposal E24-24 (Center for Building in North America et al.), reprinted by WA SBCC
- URL: https://sbcc.wa.gov/sites/default/files/2026-01/E24-24.pdf. File: `sbcc_E24-24.*`. How read: curl, pdftotext. **Caution: underline and strikethrough formatting is lost in the text extraction.**
  > "Proponents: Stephen Smith, Center for Building in North America ..."
  > "The 2024 International Building Code allows buildings up to three stories of R-2 occupancy to have up to four dwelling units at each story served by a single exit."
  > "Our language is adapted from codes in Seattle, Honolulu, New York City, and Western European countries ..."
  > "Estimated Immediate Cost Impact: We believe the cost of constructing multifamily buildings on small lots will decrease by roughly 7 percent, in line with the reduction in circulation area required."
  > New text (as modified, 4 stories): "1006.3.4.2 Single exit four-story buildings with Group R-2 dwelling units ... 1. The net floor area of each floor shall not exceed 4,000 square feet ... 3. A manual fire alarm system and automatic smoke detection system ... 4. ... automatic sprinkler locations in interior exit stairways shall comply with the requirements of NFPA 13 for combustible stairways. 5. Electrical receptacles shall be prohibited in an interior exit stairway."

## B09 ICC Building Safety Journal, "Middle Housing: Updates, Resources and the Road to 2030," Gabe Maser, June 2, 2026 (ICC official)
- URL: https://www.iccsafe.org/building-safety-journal/bsj-hits/middle-housing-updates-resources-and-the-road-to-2030/. File: `icc_bsj_middle_housing.*`. How read: curl (the article text was in the HTML despite the member banner).
  > "during the April 2026 Public Comment Hearings (PCH) held in Hartford, Connecticut. For instance, governmental members voted 86 to 34 in favor of the IBC – Means of Egress Code Development Committee -approved proposal that would permit single exit up to four stories (see E24-24). The proposal has moved to 'Approved as Modified at the Committee Action Hearing 2 (AMC2)' status through the preliminary 2026 Group A&B online governmental consensus vote (OGCV)."
  > "The online posting of the final action 2027 Code Development Cycle Group A & B results ... will occur following the Validation Committee's certification of the OGCV and report to the ICC Board of Directors"

## B10 CBNA, "2027 IBC single-exit height limit to be raised to four stories," William Skudlarek, June 19, 2026 (advocacy/research nonprofit; it is the E24-24 proponent)
- URL: https://centerforbuilding.org/article/2027-ibc-single-exit-height-limit-to-be-raised-to-four-stories. File: `cbna_2027ibc_four_stories.*`. How read: curl.
  > "On May 29, 2026, the International Code Council (ICC) announced that the Center for Building's single-stair proposal, E24-24, won the support of a majority of the ICC's governmental membership in its Online Governmental Consensus Vote."
  > "Our original proposal in 2024 would have allowed up to six stories ... After the original proposal was voted down by the IBC Means of Egress committee, we reached a compromise with other stakeholders to reduce the story limit from six stories to four"
  > "the new code section allows single-stair apartment buildings to be four stories, rather than the previous three, as long as each story is limited to 4,000 square feet of net floor area (this does not include common circulation space)."
  > "The stairway width requirement has been left unchanged, in effect requiring a minimum of 36 inches."

## B11 CAL FIRE / Office of the State Fire Marshal, *Single-Exit, Single Stairway Report to the Legislature, Pursuant to AB 835 (Chapter 345, Statutes of 2023)* (PDF created Mar 2, 2026; 34 pp.)
- URL: https://34c031f8-c9fd-4018-8c5a-4159cdff6b0d-cdn-endpoint.azureedge.net/-/media/calfire-website/about/resources/legislatively-mandated-reports/single-stair-single-exit-final-report.pdf?rev=2c31e9c6f3204add8419d7aeca70f0d8 (CAL FIRE's CDN)
- File: `calfire_single_stair_report.*`. How read: curl, pdftotext.
  > "Assembly Bill 835 (Lee, Chapter 345, Statutes of 2023) directed the State Fire Marshal to research safety standards for single-exit, single stairway apartment houses, with more than two dwelling units, in buildings above three stories."
  > "California currently does not allow single-stair, single-exit buildings that exceed three stories."
  > "These measures, however, do not fully substitute for the redundancy of two independent stairways."
  > "California's fire departments, drawing on direct experience in emergency response, have expressed near-unanimous opposition to single-stair buildings above three stories. Firefighters emphasize that a single stairwell forces evacuees and first responders into direct conflict, slowing both egress and suppression efforts."
  > "stairways as a construction element generally account for 7.5% to 12.5% of the total building cost in mid-rise residential projects."
  > "For these reasons, the fire service community strongly recommends maintaining the requirement for multiple exit stairs in residential and mixed-use buildings exceeding three stories."
  > History: "When the first IBC was published in 2000, the baseline allowance (section 1005.2.2, titled 'Buildings with one exit') was for two stories of R-2 occupancies served by a single-exit, with a maximum of four dwelling units per floor and a 50-ft. maximum 'travel distance' ... There was, however, a footnote allowing three stories above grade if served by an automatic sprinkler system" ... "In 2012 ... the exit access travel distance raised from 50 feet to 125 feet."
  > "Both the first and last editions [of the Uniform Building Code, 1927 and 1997] contain a hard limit on single-exit apartment buildings at two stories."
  > "Huge numbers of single-stair two-story apartment buildings – now colloquially known as 'dingbats,' ... were built around the middle of the century"
  > "In 1991, NFPA 101 and its companion building code, NFPA 5000, modified their limited-height single-exit exception to allow four stories (with four units per floor) if an apartment building is outfitted with automatic sprinklers"
  > Seattle: "In 1985, the height limit was reduced to six stories ... The city likely has 'hundreds' of single-stair apartment buildings above three stories, although the exact number has not been verified as part of this work."
  > E24-24: "That proposal was voted down unanimously during the first Committee Action Hearing in the spring, but a modified proposal based on NFPA 101's conditions was approved by the Egress Committee in the fall."
  > AB 130 (2025): "The bill prohibits the adoption of new residential unit building standards until June 1, 2031, unless certain conditions are met"

## B12 Pew Charitable Trusts, "Small Single-Stairway Apartment Buildings Have Strong Safety Record" (synopsis PDF dated February 2025; with CBNA)
- URL: https://www.pew.org/-/media/assets/2025/05/single-stair_report_summary.pdf. File: `pew_2025-05_single_stair_summary.*`. How read: curl (the full report and web page returned 403).
- Authors: "Seva Rodnyansky, Ph.D, Alex Horowitz, Liz Clifford, and Dennis Su, in collaboration with the Center for Building in North America's Stephen Smith and Sandip Trivedi."
  > "In New York City, the overall rate of fire deaths in its 4,440 modern single-stair buildings since 2012 was the same as in other residential buildings."
  > "We were able to find a total of four fire-related deaths in New York City and Seattle's modern single-stairway buildings from 2012 to 2024. The lack of a second stairway did not play a role in any of those fatalities."
  > "This report's first-ever analysis of 347 fires involving 468 deaths over a 12-year period in New York City demonstrated that fire fatality rates were no higher in four-to-six-story single-stair buildings than in other types of residential buildings in New York."
  > "For a four-to-six-story building on a small lot, the typical cost of building a second stairway and connecting the two via a central corridor on every level is equal to approximately 6%-13% of the total construction costs. The additional stairway and corridor consume around 7% of the building's floor area."
  > "Current U.S. building codes in all but three major cities (New York City, Seattle, and Honolulu) stipulate that apartment buildings four to six stories must have two stairways."
  > "Vermont, Georgia, and Puerto Rico have adopted the NFPA rules."
  > "Overall, residential fire-related death rates in the Netherlands are one-third those of the U.S."
  > "As of fall 2024 at least 11 states and five cities have enacted laws or amended regulations to explore or allow single-stairway designs for four-to-six-story buildings."
  > "Only 21% of all housing units built since 2000 in the U.S. have been in apartment buildings with two to 19 units"
  > "Small- and medium-sized apartment buildings with two to 19 units ... make up 40% of the rental stock in the United States today"
  > "A study of the Boston area estimated that such a building code change had the potential to create 130,000 new homes simply by developing the vacant parcels within walking distance of transit."
  > Caveat stated by Pew: "Fire data quality varies greatly ... In Seattle and Honolulu, identifying specific single-stairway buildings is difficult."

## B13 CBNA, "Why we can't build family-sized apartments in North America," Stephen Smith, May 4, 2023 (advocacy)
- URL: https://centerforbuilding.org/article/why-we-cant-build. File: `cbna_why-we-cant-build.*`. How read: curl (worked on retry).
  > "In North America, apartments are typically laid out off of a double-loaded corridor – lots of apartments arrayed on either side of a single long hallway, like in a hotel."
  > "in the rest of the world, including in Europe, most new buildings are designed as what Mike Eliason calls point access blocks ... anywhere between one and generally around six apartments per floor arrayed around a central staircase and, usually, an elevator."
  > "The German point access block layouts ... can offer a much more affordable two-bed, one-bath unit that's a full 36 percent smaller than the American version"
  > "you can fit four bedrooms in Europe in the space of three bedrooms in America."

## B14 CBNA, *Elevators: Executive Summary* (Stephen Smith; PDF uploaded Dec 2024) (advocacy/research)
- URL: https://admin.centerforbuilding.org/wp-content/uploads/2024/12/Elevatorsexecutivesummary.pdf. File: `cbna_elevators_exec_summary.*`. How read: curl. Full report (not read): .../2024/12/Elevators.pdf
  > "The United States and Canada have the most expensive elevators in the world. Prices charged in North America ... are at least three times those charged by the same manufacturers in comparable mid-rise buildings in high-income countries in Western Europe."
  > Price chart: "New York, USA (2023) Kone MonoSpace 300 DX MRL electric traction $158,000" vs "Vaud, Switzerland (2020) Schindler 3300 ... $35,348 **" (** = nominal price) and "Lombardy, Italy (2022) Kone MonoSpace 300 DX ... $49,393 **"
  > "New walk-up apartment buildings in major U.S. cities can reach four, five, and even six stories in height – unheard of nowadays in new buildings in Western Europe"
  > "elevator cabins in new buildings in North America are often around twice the size of those in Europe. If North America allowed European-sized elevators in new mid-rise buildings, then elevators would likely be between 13 and 44 percent cheaper"
  > "The Netherlands has a significantly higher share of its population living in single-family houses than the United States, but the U.S. has 40 percent fewer elevators per capita."

## B15 CBNA, "NFPA's single-stair symposium," Stephen Smith, Sept 28, 2024 (advocacy)
- URL: https://centerforbuilding.org/article/nfpa-single-stair-symposium. File: `cbna_nfpa-single-stair-symposium.*`.
  > "Earlier this month, British Columbia formally amended its building code to allow single-stair buildings up to six stories, up from the current two-story allowance."
  > "has provoked an equal amount of opposition from fire service organizations"

## B16 CBNA single-stair legislative tracker (site data extract), state of the tracker on 2026-10-12 (ADVOCACY; secondary, use only to find leads)
- URL: https://centerforbuilding.org/_payload.json. Files: `cbna_payload.json`, `cbna_tracker_extract.txt`. How read: curl, JSON parse.
- I checked these entries against official sources: WA SB 5491, TN PC 820, TX SB 2835, CO HB25-1273, MI HB 5570 (PA 28 of 2026), CA AB 835, MN study, E24-24.
- Tracker-only claims I did NOT check against an official source (attribute them to CBNA if used):
  > Montana: "Sen. Daniel Zolnikov introduced SB 213 ... signed into law by Gov. Greg Gianforte in May 2025, and took effect on Oct. 1, 2025."
  > New Hampshire: SB 282 "allows single-stair residential buildings up to four stories ... signed into law by Gov. Kelly Ayotte on July 15, 2025 ... The code text took effect on Oct. 15, 2025."
  > Idaho: "In April 2026, Gov. Brad Little signed into law H0706 ... option to permit single-stair buildings up to six stories ... took effect on July 1, 2026."
  > Connecticut: "in March 2026 lawmakers passed an omnibus bill that repealed the provisions passed in 2024."
  > Maryland: HB 489 / SB 436 "signed into law by Gov. Wes Moore on May 13, 2025" (study, report due Dec. 1, 2026).
  > New York State: study in the 2024 budget; "awarded to Jensen Hughes in the amount of $331,000"
  > Virginia: SB 195 / HB 368 (2024) advisory group (confirmed by B19).
  > Oregon: HB 3395 (2023) "review and consider"; Portland adopted the 4-story appendix in Oct. 2025.
  > Hawaii: HCR66 passed April 2025. Honolulu "in 2023 watered down the provision to only allow single-stair up to three stories."
  > Cities: Memphis/Shelby County (Apr 1, 2025, 6 stories), Knoxville (eff. Jan 1, 2025), Nashville (BL2025-898), Chattanooga (eff. Aug 5, 2025), Austin (5 stories, elevator required), Baltimore (Ord. 25-061, eff. Dec 3, 2025), Denver (Nov 24, 2025), Anchorage (eff. May 18, 2026), Washington DC (B26-0227 signed June 2, 2026; rules by July 1, 2027), Culver City (Sep 29, 2025).
  > Also: "Chicago is currently the only major U.S. city that does not allow three story single-stair buildings."
  > NYC: "permitted single-stair buildings up to six stories since 1938 ... Over 4,000 single-stair buildings above the IBC's three-story height limit have been built"

## B17 Tennessee Public Chapter No. 820 (2024), SB 2834 / HB 2925 (official TN Secretary of State PDF)
- URL: https://publications.tnsosfiles.com/acts/113/pub/pc0820.pdf (curl-UA2). Status page: https://wapp.capitol.tn.gov/apps/BillInfo/Default.aspx?BillNumber=HB2925&GA=113 (curl-UA2). Files: `tn_pc820_2024.*`, `tn_hb2925_info.*`.
  > "(11)(A) Shall not prohibit less than six (6) stories of Group R-2 occupancy ... to be served by a single exit if: (i) The building has not more than six (6) stories above grade plane; (ii) The building does not contain more than four (4) dwelling units on any floor; ... (v) There is no more than twenty feet (20') of travel to the exit stairway from the entry/exit door of any dwelling unit; (vi) Travel distance ... does not exceed one hundred twenty-five feet (125')"
  > "(B) A local government may adopt the exception set out in this subdivision (a)(11) by resolution or ordinance"
  > "PASSED: April 11, 2024". Status page: "Signed by Governor. 04/29/2024" ... "Pub. Ch. 820 05/09/2024"

## B18 Texas SB 2835 (89th Leg., 2025), enrolled text and history (capitol.texas.gov)
- URLs: https://capitol.texas.gov/tlodocs/89R/billtext/html/SB02835F.htm and https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=SB2835 (curl). Files: `tx_sb2835_*`.
  > "SUBCHAPTER I. SINGLE STAIRWAY IN CERTAIN APARTMENT BUILDINGS ... (b) A municipality may authorize an apartment building to have a single stairway only if the building: (1) does not have more than six stories above grade plane and is not a high-rise ... (2) does not have more than four dwelling units on any floor; ... (7) does not have more than 20 feet between the entry or exit door of a dwelling unit and an exit stairway; (8) does not have more than 125 feet of exit access travel distance; ... (13) does not have an electrical receptacle in an interior exit stairway"
  > "SECTION 2. This Act takes effect September 1, 2025." Senate vote "Yeas 29, Nays 2"; House "Yeas 81, Nays 57"
  > History: "Filed without the Governor's signature" ... "06/20/2025 ... Effective on 9/1/25"

## B19 Virginia DHCD Single-staircase Advisory Group, Findings and Recommendations, Nov 27, 2024 (RD845, official)
- URL: https://rga.lis.virginia.gov/Published/2024/RD845/PDF. File: `va_rd845_2024.*`. How read: curl-UA2.
  > "House Bill 368 and Senate Bill 195 (2024) ... directed the Board of Housing and Community Development (the Board) to convene a workgroup to provide recommendations for allowing a single stair exit for Group R-2 (multifamily residential) structures up to six stories in height"
  > "At four stories and above, Emergency Escape and Rescue Openings (EEROs) start to become technically and functionally infeasible."
  > "Advisory Group members found that performing emergency response operations in a single stairwell, that is simultaneously being used for occupant escape, negatively impacts rescue and fire suppression efforts."
  > "Advisory Group members found that projects on these small lots would otherwise be financially infeasible if sellable living space was taken up by a second staircase."
  > "The Advisory Group recommends that any proposal to allow a single stair exit above current limits should be considered by the Board during the normal building code development process."

## B20 Colorado HB25-1273 (leg.colorado.gov, enacted summary and history)
- URL: https://leg.colorado.gov/bills/hb25-1273 (curl-UA2; the research UA got 406). File: `co_hb25-1273.*`.
  > "Concerning requiring certain municipalities to modify building codes to allow five stories of a multifamily residential building to be served by a single exit."
  > "The act defines a subject jurisdiction as a municipality with a population of 100,000 or more that is served by a fire protection district, fire authority, or fire department that is or was accredited by a specified organization."
  > "On or before December 1, 2027, the act requires the governing body of a subject jurisdiction to adopt a building code, or amend an existing building code, to allow up to 5 stories of a multifamily residential building that satisfies certain conditions to be served by a single exit."
  > History: "05/13/2025 Governor Governor Signed". Status: "Became Law"

## B21 Michigan HB 5570 of 2026, Public Act 28 of 2026 (legislature.mi.gov)
- URLs: https://legislature.mi.gov/Bills/Bill?ObjectName=2026-HB-5570 and https://legislature.mi.gov/documents/2025-2026/publicact/htm/2026-PA-0028.htm (curl-UA2). Files: `mi_hb5570.*`, `mi_pa28_2026.*`.
  > "Act No. 28 Public Acts of 2026 Approved by the Governor July 21, 2026 ... EFFECTIVE DATE: July 21, 2026"
  > "Sec. 4j. Subject to section 4k, a multiple-family dwelling that has not more than 4 levels above grade plane may have a single interior exit stairway if all of the following conditions are met: (a) The dwelling has not more than 4 units on each level. (b) The net floor area of each level of the dwelling is not more than 4,000 square feet. (c) The exit access travel distance is not more than 125 feet"
- I did not read HB 5571 (the 5–6 story companion).

## B22 Minnesota Single-Exit Stairway Apartment Building Study, WJE with Crux Consulting, for MN Dept. of Labor and Industry, Dec 30, 2025 (legislatively mandated report)
- URL: https://www.lrl.mn.gov/docs/2025/mandated/251989.pdf. File: `mn_dli_single_exit_study_2025-12-30.*` (first 20 of 127 pages extracted). How read: curl.
  > "The Minnesota Legislature mandated a data-driven study to evaluate taller and/or larger MFD buildings with a single-exit stairway that could be up to seventy-five feet in height."
  > "4. The number of exit stairways factors into the comparative building risk evaluation only when the sprinkler system has failed to control the fire, AND when the door to the dwelling unit of fire origin is open, AND when the exit stairway door on the floor of fire origin is also open."
  > "5. Almost 97 percent of the building risk for each analyzed scenario can be attributed to the sprinkler system failing to flow on demand."
  > "Based on the Minnesota fire data (MFIRS), the current observed mean reliability of a sprinkler system flowing on demand is approximately 88 percent."
  > "7. ... the exit stairway quickly fills with smoke and becomes untenable before occupants are anticipated to make the decision to evacuate. However, occupants in multiple-exit stairway MFD buildings on floors other than where the fire originated can use the unaffected exit stairway to egress."
  > "10. ... tactical response questions remain for effectively fighting fires in single-exit stairway buildings more than four stories in height."
  > "this report does not define acceptable risk or safety levels or propose direct building code language"

## B23 IAFC position statement, "Reducing Stairs in Residential Buildings Higher Than Three Stories Creates Escape Hazards for Occupants and Inhibits Vital Emergency Response Operations," adopted by the IAFC Board March 15, 2024
- URL: https://www.iafc.org/blogs/blog/iafc/2024/03/15/reducing-stairs-in-residential-buildings-higher-than-three-stories-creates-escape-hazards-for-occupants-and-inhibits-vital-emergency-response-operations. File: `iafc_position_2024-03-15.*`. How read: curl.
  > "The International Association of Fire Chiefs, represented by its Fire & Life Safety Section (FLSS), hereby declares its unwavering support for the retention of the requirement for a second stairway in R-2 residential structures exceeding three stories."
  > "This provision ensures vital redundancy in egress options, crucial for occupant evacuation and firefighter access during emergencies."
  > "Modern hazards, such as those posed by lithium-ion battery-powered devices, underscore the need to be able to exit a building quickly and safely in an emergency."
  > "The IAFC urges fire service leaders to vehemently oppose legislative attempts to amend out the second stairway requirement."
  > "These proposals, backed by developers, builders, and urban planners, bypass the established National Code Consensus process"
- IAFC blog, Sept 4, 2024 (`iafc_blog_rogers_2024-09-04.*`): "they almost unilaterally oppose the allowance of single-exit stairwells (as opposed to multiple) in buildings over 4 or 5 stories."

## B24 IAFF and Metropolitan Fire Chiefs Association, Joint Statement Regarding Single Stairways in Multifamily Buildings (June 2024), plus press release of June 20, 2024
- URLs: https://iaff.org/wp-content/uploads/2024/06/JointStatement.pdf and https://www.iaff.org/wp-content/uploads/2024/09/Stairwells-Release-June-2024.pdf. Files: `iaff_*`. How read: curl.
  > "These legislative actions are an attempt to supersede the model safety codes, placing occupants and fire fighters at greater risk of injury and death. We must do all we can to defeat these misguided efforts."
  > "Put simply, lives will be endangered."
  > "This removes the responder's ability to utilize one stairwell for occupant egress and establish suppression operations in the second stairwell"
  > Release: "Multiple stairwells allow occupants to safely exit in one direction while fire fighters set up suppression operations in the other." ... "We cannot compromise on safety for the sake of cost savings."

## B25 National Association of State Fire Marshals, "Position in Opposition of Single-Exit Stairway in Multifamily Structures" (adopted 3-1-2024)
- URL: https://www.firemarshals.org/resources/Documents/2024%20Newsletters/Single-Exit%20Stairway%20Position%202_28_24%20Final.pdf. File: `nasfm_*`. How read: curl.
  > "NASFM strongly opposes any changes that are below the minimal requirements found in the national consensus codes and standards. To be more specific, we do not support reducing the required number of exit passage ways in multifamily dwellings as required by codes."

## B26 National Fallen Firefighters Foundation release, July 1, 2024
- URL: https://firehero.org/wp-content/uploads/2024/07/single-stairway-exits-release-070124.pdf. File: `nfff_*`.
  > "'The practice of a jurisdiction opting out of a portion of a code is not just a matter of choice, it's a decision that nullifies the whole process—and endangers the public and those who are responsible for responding to fires and other life safety hazards,' said Victor Stagnaro, NFFF's CEO."

## B27 NFPA blogs by Valerie Ziavras, NFPA Technical Services Engineer
- (a) "Single exit stair debate knowledge gaps," published 2025-01-07: https://www.nfpa.org/en/news-blogs-and-articles/blogs/2025/01/07/single-exit-stair-debate-knowledge-gaps
- (b) "Single Exit Stair Doesn't Tell Whole Story in May 2026 Manhattan Fire," published 2026-05-21: https://www.nfpa.org/en/news-blogs-and-articles/blogs/2026/05/25/single-exit-stair-2026-manhattan-fire
- Files: `nfpa_blog_*`. How read: curl, then the article body taken from the page's embedded __NEXT_DATA__ JSON (the page renders with JS; WebFetch returned only the title).
  > (a) "While NFPA® has remained neutral on the technical issue, we have taken a firm stance that this—and all matters related to fire and life safety—should be discussed in an open, balanced, consensus-based standards development process."
  > (b) "NFPA firmly believes that changes to the allowable height of SES apartment buildings need to be evaluated in balanced, open, consensus-based standards development processes."
  > (b) "We now know that the fire started because a cigarette was carelessly discarded onto cardboard boxes located in the lobby of the first floor. The smoke and fire then spread up the stairwell. It has been reported that at least two of the victims were found near the top of the stairwell by the roof."
  > (b) "To draw premature conclusion about the recent fire in Manhattan and to imply that this incident in an existing building is representative of the risks associated with the proposed SES buildings is misleading."
  > (b) Mentions that NFPA "highlighted the risks associated with certain conclusions drawn by the Pew Report, 'Modern Multifamily Buildings Provide the Most Fire Protection'" (I did not read that Pew report.)
- NFPA Xchange podcast page (`nfpa_community_debate.*`): "Nearly all jurisdictions in the United States enforce codes that require two exit stairwells in residential buildings above three or four stories."

## B28 Los Angeles DBS, Revised Report on single-exit amendments (CF 25-0247), Aug 7, 2025
- URL: https://cityclerk.lacity.org/onlinedocs/2025/25-0247_rpt_dbs_8-07-25.pdf. File: `la_dbs_25-0247.*`.
  > "These model codes, which the State of California adopts and modifies, currently allow for single-exit buildings up to three stories (California Building Code (CBC) 1006.3.4) with a maximum of four dwelling units per story."

## Other files saved, not quoted
`austin_E24-24-SHAPIRO-MC1.*` (floor modification text), `va_dhcd_sg_20250624.*` (VA study group agenda 2025), `sbcc_SEP_baseline_edited_20250812.*`, `sbcc_semh_tag_legislation.pdf`, `wa_sb5491_fbr.*`, `cbna_hud-cityscape-publishes-our-article.*`, `nfpa_debate_page.html`, `icc_captcha_page.html` (proof of the ICC block).

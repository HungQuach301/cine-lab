# Cluster D: Project financing and lending rules (how the mechanism works, not consumer advice)
Accessed 2026-10-12. Every source was fetched with `curl -A 'Mozilla/5.0 (research)'` unless a note says otherwise. HTML was converted to text with a local html-to-text script, and PDFs with `pdftotext -layout`. Raw files sit in this folder. Quotes are copied word for word from the extracted text, with line wrapping removed.
Blocked (403): multifamily.fanniemae.com (small-loans pages), and jchs.harvard.edu landing page (also 403 through WebFetch). The JCHS PDF itself downloaded fine.

---
## D1. Fannie Mae Selling Guide B2-3-01, General Property Eligibility (09/03/2025)
URL: https://selling-guide.fanniemae.com/sel/b2-3-01/general-property-eligibility. Page says "Published: October 07 2026". File: b2-3-01_general-property-eligibility.html/.txt
- "Fannie Mae purchases or securitizes first-lien mortgages that are secured by residential properties when the dwelling consists of one to four units."
- "A Loan-Level Price Adjustment (LLPA) applies to certain property types, including multiple-unit properties and units in an attached condo project."
- Ineligible list includes "boarding houses;" and "bed and breakfast properties;"

## D2. Fannie Mae Selling Guide B2-3-04, Special Property Eligibility Considerations (10/08/2025), "Mixed-Use Properties"
URL: https://selling-guide.fanniemae.com/sel/b2-3-04/special-property-eligibility-considerations. File: b2-3-04_*.html/.txt
- "Fannie Mae purchases or securitizes mortgages that are secured by properties that have a business use in addition to their residential use, such as a property with space set aside for a day care facility, a beauty or barber shop, or a doctor's office."
- "The following special eligibility criteria must be met: The property must be a one-unit dwelling that the borrower occupies as a principal residence. The borrower must be both the owner and the operator of the business. The property must be primarily residential in nature. The dwelling may not be modified in a manner that has an adverse impact on its marketability as a residential property."
- What this means (my reading, not a quote): a building with a shop downstairs and several flats above does not qualify as Fannie Mae single-family mixed-use collateral.

## D3. Fannie Mae Selling Guide B4-1.4-07, Mixed-Use Property Appraisal Requirements (06/04/2025)
URL: https://selling-guide.fanniemae.com/sel/b4-1.4-07/mixed-use-property-appraisal-requirements. File: b4-1.4-07_*.html/.txt
- Appraisal must "report any adverse impact on marketability and market resistance to the commercial use of the property; and report the market value of the property based on the residential characteristics, rather than of the business use or any special business-use modifications that were made."
(The section number in the brief, B4-1.3-04, is wrong: that section is "Site Section of the Appraisal Report". The mixed-use rules are at B2-3-04 and B4-1.4-07.)

## D4. FHFA regulation, 12 CFR 1282.1 Definitions (Enterprise housing goals and mission)
URL: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-12?part=1282&section=1282.1 (eCFR current text). File: ecfr_12cfr1282.1.json/.txt. Last amendment cited: 89 FR 106275, Dec. 30, 2024.
- "Single-family housing means a residence consisting of one to four dwelling units. Single-family housing includes condominium dwelling units and dwelling units in cooperative housing projects."
- "Multifamily housing means a residence consisting of more than four dwelling units. The term includes cooperative buildings and condominium projects."
- "Small multifamily property means any multifamily property with at least 5 dwelling units but no more than 50 dwelling units."
- "Owner-occupied housing means single-family housing in which a mortgagor resides, including two- to four-unit owner-occupied properties where one or more units are used for rental purposes."
- "Dwelling unit ... includes a dwelling unit in a single-family property, multifamily property, or other residential or mixed-use property."

## D5. National Housing Act sec. 203(b), 12 U.S.C. 1709 (FHA single-family)
URL: https://www.law.cornell.edu/uscode/text/12/1709 (LII mirror of the US Code). File: usc12_1709.html/.txt
- 1709(b)(2)(A)(i) loan limit: "in the case of a 1-family residence, 115 percent of the median 1-family house price in the area, as determined by the Secretary; and in the case of a 2-, 3-, or 4-family residence, the percentage of such median price that bears the same ratio ..."
- 1709(d): "...maximum mortgage amounts for insuring a mortgage secured by a one- to four-family dwelling..."
- 1709(k) heading: "Rehabilitation of one- to four-family structures"

## D6. National Housing Act sec. 221, 12 U.S.C. 1715l (221(d)(4) multifamily)
URL: https://www.law.cornell.edu/uscode/text/12/1715l. File: usc12_1715l.html/.txt
- "The property or project ... may include such commercial and community facilities as the Secretary deems adequate to serve the occupants"
- "A property or project covered by a mortgage insured under the provisions of subsection (d)(3) or (d)(4) shall include five or more family units"

## D7. HUD Handbook 4000.1, FHA Single Family Housing Policy Handbook, Update 18 (Issued August 12, 2026)
URL: https://www.hud.gov/sites/default/files/Housing/documents/40001-hsgh-Update-18.pdf (linked from HUDCLIPS Housing Handbooks page). File: hud_4000.1_U18.pdf/.txt
- II.A intro (p. 126): "...standards and procedures applicable to all Single Family (one- to four-units) Mortgages insured under Title II of the National Housing Act, except for Home Equity Conversion Mortgages (HECM)."
- II.A.1.b.iv, Property Eligibility and Acceptability Criteria, "(5) Mixed Use of Property" (p. 168): "Mixed Use refers to a Property suitable for a combination of uses including any of the following: commercial, residential, retail, office, or parking space. Mixed Use one- to four-unit Single Family Properties are eligible for FHA insurance, provided: a minimum of 51 percent of the entire building square footage is for residential use; and the commercial use will not affect the health and safety of the occupants of the residential Property."
- II.D.3 ... ii. Legal and Land Use Considerations, "(B) Nonresidential Use of Property" (p. 807-808): "The nonresidential portion of the Total Floor Area may not exceed 49 percent. Any nonresidential use of the Property must be subordinate to its residential use, character and appearance. Nonresidential use may not impair the residential character or marketability of the Property." and "The Appraiser must contact the Mortgagee if the nonresidential portion of the Property exceeds 49 percent."
- II.A.8 203(k) Rehabilitation (p. 392): "a Mixed Use Property with one- to four-residential units, provided: 51 percent of the Gross Building Area (GBA) is for residential use; and commercial use will not affect the health and safety of the occupants of the residential Property"
- II.D.12 "Mixed Use One- to Four-Unit Single Family Properties" (p. 870): "The Appraiser must not include business valuation or the value of Personal Property or business fixtures in the appraisal."

## D8. HUD MAP Guide 4430.G (Multifamily Accelerated Processing), Revision March 19, 2021
URL: https://www.hud.gov/sites/dfiles/OCHCO/documents/4430GHSGG.pdf (linked from HUDCLIPS Guidebooks page as current). File: hud_MAP_Guide_4430G.pdf/.txt
- 3.2.1 Properties (NC/SR programs 220, 221(d)(4), 231, 241(a)): "Properties must have 5 or more residential units with individual full kitchens and baths for each unit. (Section 231 requires at least 8 units.)"
- 3.1.30: "FHA insured multifamily properties may be traditional multifamily structures on one site, or may be detached, semi-detached, or row houses. Each property must consist of five or more dwelling units."
- 7.7.12.9 table "Commercial Space and Income Limitations" (p. 7-28): 221(d)(4) and 231 = 25% of total net rentable area / 15% of effective gross income; 220 = 25% / 30%; 223(f) = 25% / 20%.
- 7.7.12.9.E: "For all programs except Section 223(f), the maximum underwritten commercial occupancy rate shall be the lesser of: a) that indicated by the market, or b) 80 percent."
- 7.7.13: "Regional Center Directors may issue waivers of the commercial income limits in Section 7.7.12.9, so long as the amount does not reflect a property that is primarily commercial rather than residential."
- 3.4.2 (Section 220): "Commercial space is limited to 25% of total net rentable area and commercial income to 30% of effective gross project income." 3.7.18 (223(f)): "...25% of total net rentable area and commercial income to 20% of effective gross project income."
- Caveat: HUD Notice 11-23 (2011), found only in a search result and not fetched, gave 10% NRA. The 2021 MAP Guide is the version currently linked on HUDCLIPS. Later Housing Notices may have changed these figures and were not checked.

---
## D9. Freddie Mac Multifamily, "Small Balance Loans" (Research Perspectives), July 2015
URL: https://mf.freddiemac.com/docs/research_perspectives_small_balance_loans.pdf. File: freddie_sbl_research.pdf/.txt
- "Thirty-one percent of U.S. renter households live in small properties that comprise five to 50 units."
- "renter households living in five- to 49-unit properties account for 31 percent of all renter-occupied housing, compared to just 12 percent in 50-plus-unit properties." (ACS 2013)
- "the secondary market, including the GSEs, disproportionately serves larger properties. The total small loan volume purchased by the two GSEs in 2013 was $2.6 billion of $56 billion in total business."
- "In non-major markets ... small properties make up only 16 percent of multifamily CMBS loans, whereas large properties represent 84 percent."
- "In 2013, loans originated of less than $3 million made up 26 percent of the total multifamily dollar volume but composed 92 percent of all lenders and 70 percent of all loans originated"
- "default rates for small and large properties are similar, whereas losses in the event of a default are higher for small properties."

## D10. JCHS Harvard RR07-8, Apgar & Narasimhan, "Enhancing Access to Capital for Smaller Unsubsidized Multifamily Rental Properties," March 2007
URL: https://jchs.harvard.edu/sites/default/files/media/imp/rr07-8_apgar.pdf. File: jchs_rr07-8_apgar.pdf/.txt (copyright allows short quotes with credit)
- "Nearly one-fifth of the rental housing stock is in smaller, multifamily apartment buildings with between 5 and 49 units."
- "...difficult for the current owners to achieve economies in property management and to absorb the high fixed cost of gaining access to debt or equity capital"
- Quoting the Millennial Housing Commission Housing Finance Task Force: "financing for small multifamily properties (defined here as 5 to 49 unit properties) is one of the most significant gaps in the mortgage industry."
- "Most securitized lending is fixed-rate, non-recourse, and intermediate to long term (10 to 30 years). For example, some 86 percent of all 200 unit apartment buildings have a mortgage, and some 79 percent of these mortgaged properties have longer term fixed-rate financing. In contrast, only 58 percent of the 5 to 9 unit apartments have a mortgage, and of these just 59 percent have longer-term fixed rate financing."
- "between 1999 and 2004 alone, the share of rental construction in apartments with 50 or more units grew from 13 to 24 percent."
- "HUD reports that the average project size of tax credit developments has increased steadily since the program's inception and now stands close to 80 units."
- "the per unit costs associated with accessing equity investment through the Tax Credit program are prohibitively high"

## D11. Brookings, Shekar Narasimhan, "Why Do Small Multifamily Properties Bedevil Us?" November 1, 2001
URL: https://www.brookings.edu/articles/why-do-small-multifamily-properties-bedevil-us/. File: brookings_small_mf.html/.txt
- "Multifamily properties typically are defined as properties containing five or more dwelling units."
- "The explosion of securitized multifamily lending seems to have bypassed the 5- to 49-unit sector ... smaller multifamily property financing typically is variable rate, recourse, and shorter-term maturity (5 years)."
- "loans of under $2 million have a 17.34% loss rate compared to a 4.6% rate for loans of over $10 million (UNC/ACLI, June 2001)."
- "the S&L debacle and extensive bank consolidation over the last decade have removed this market's primary communitybased financing source."
- Due diligence costs (appraisal, environmental review, condition report) are cited as a fixed cost that "never will make due diligence requirements for this segment of the market cheap on a relative basis."

## D12. DePaul Institute for Housing Studies, "Credit constraints for small multifamily rental properties," March 27, 2012 (Cook County, IL)
URL: https://housingstudies.org/releases/credit-constraints-multifamily-rental-properties/. File: ihs_credit_constraints.html/.txt
- "these types of properties are often more expensive to finance than larger multifamily properties. Additionally, the market for loans to smaller multifamily properties is primarily served by community banks that have tightened underwriting criteria and reduced lending volume in recent years."
- "Nearly 93 percent of smaller multifamily properties that received a mortgage between 2005 and 2010 were considered credit constrained. Conversely, only 34 percent of buildings with 100 or more units were considered credit constrained."
- "The credit available to the typical constrained 10 to 49 unit property ... would be 19.8 percent less than the expected demand ... 50 to 99 unit ... about 8.5 percent less ... over 100 units ... 3.9 percent less"

## D13. Terner Center (UC Berkeley), David Garcia, "Making Missing Middle Pencil: The Math Behind Small-Scale Housing Development," June 2024
URL: https://ternercenter.berkeley.edu/wp-content/uploads/2024/06/Missing-Middle-Development-Math-Final-June-2024.pdf. File: terner_mm_math_2024.pdf/.txt
- "conventional institutional investors typical of larger multifamily projects are generally less interested in this product type."
- "debt-underwriting standards for these products can be more conservative ... This means lenders often require completion guarantees and recourse to the developer's personal assets as collateral."
- "The 'global pool of capital' for larger developments ... is generally not accessible at the missing middle scale"
- "investment came primarily from friends, family, and other investors close to them"
- Table 5 hard costs (2023, CA): fourplex rental $284-$372/sf; ten-unit "Multiplex rental" $301-$394/sf (Sacramento to East Bay); excludes land, fees, reserves, financing.
- Table 6 finance assumptions: "60%" loan to cost; "9.5% for construction loan, 6.5% for permanent loan"; DSCR "1.30"; equity IRR target "15%".
- "in most cases we found that our missing middle prototypes would not be built under recent market conditions given costs, rental comps, lack of financing options, and generally unfavorable market conditions."
- "projects with three or more units are subject to more stringent commercial building code requirements ... We estimate a roughly ten percent premium in cost to build to the commercial building code"
(Also downloaded: Terner "Missing Middle" brief, Dec 2022, terner_mm_brief_2022.pdf. Not mined.)

---
## D14 (optional, historical, weak for walk-ups). NBER WP 15650, Goetzmann & Newman, "Securitization in the 1920's," January 2010
URL: https://www.nber.org/system/files/working_papers/w15650/w15650.pdf. File: nber_w15650.pdf/.txt
- Abstract: "quantifies the scale and scope of the commercial real estate mortgage bond market in the period surrounding the 1920s ... A substantial retail appetite for real estate securities during this period may have significantly contributed to a real construction boom"
- "all of the bonds were issued in denominations of at least $1,000 and $500, though many were issued in denominations as small as $100. Interest rates varied between 4-7%"
- "Johnson estimated the total issuance to have exceeded $4.1 billion across 1090 individual issues between 1919 and 1931."
- Caveat: covers large commercial and apartment-house bond issues, not small walk-up finance. Use only as background.

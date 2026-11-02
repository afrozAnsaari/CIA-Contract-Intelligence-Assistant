# Error analysis (iter03_question_only_fullquery_abstention, split=train, k=5)

Counts: chunk_boundary=23, correct_abstention=28, false_abstention=5, irrelevant_extra=19, low_rank=20, ok=4, partial_span=12, wrong_section=57

## false_abstention (5)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=13.334 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33128:34034] score=7.521 "employee skills; and (f) any other non-public information which a competitor of the Company could us..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [49131:50011] score=7.107 "and oral form, and providing such other assistance that the Company or any Group Companies' legal ad..."
  - P@5=0.099 R@5=1.000 signal=0.20938520209867387
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [29338:30329] score=8.391 "12.1 A copy of the Company's disciplinary, dismissal and grievance procedures are set out in its emp..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [815:1813] score=7.065 "other in accordance with paragraph 11 below. No employment with a previous employer is deemed to be ..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [25288:26278] score=5.929 "if such termination of employment occurs within 12 months after the occurrence of the first event co..."
  - P@5=0.000 R@5=0.000 signal=0.19836921677372252
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42096:43091] score=10.000 "Leave under paragraph 10 above then the Restricted Period shall be reduced by any period/s spent by ..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [48320:49276] score=9.378 "of, restricting your rights under sections 39 to 43 (inclusive) of the Patents Act 1977 (as amended ..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [46832:47754] score=5.959 "and to defend any proceedings or claims made by any third party that the use or exploitation of any ..."
  - P@5=0.000 R@5=0.000 signal=0.2236889388569866
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [90202:91188] score=9.493 "of the Commission pursuant to the Company's application requesting confidential treatment under Rule..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [153838:154649] score=6.802 "of the enforceable portion of any such provision and the remaining provisions will not be adversely ..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [20043:20968] score=6.400 "Section 8.2(a)(i).

Section 1.72 "PDMA" means the Prescription Drug Marketing Act, as amended, and t..."
  - P@5=0.000 R@5=0.000 signal=0.20563377680041858

## wrong_section (57)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [49861:50747] score=9.827 "collective agreements which directly affect your terms and conditions of employment.

18 DATA PROTEC..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=7.604 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [45210:46129] score=4.870 "remedies for past infringement and all materials embodying these rights to the fullest extent permit..."
  - P@5=0.000 R@5=0.000 signal=0.24448066439672117
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8594:9480] score=4.553 "writ, decree or contract known to GINARES, or an event that results in the creation of any lien, cha..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=4.372 "8 21. Early Termination................................................................................"
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10019:10980] score=4.247 "writ, decree or contract known to HPIL ET, or an event that results in the creation of any lien, cha..."
  - P@5=0.000 R@5=0.000 signal=0.3210800636854513
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8594:9480] score=9.666 "writ, decree or contract known to GINARES, or an event that results in the creation of any lien, cha..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10019:10980] score=9.196 "writ, decree or contract known to HPIL ET, or an event that results in the creation of any lien, cha..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7028:8024] score=5.592 "Of The Parties   The nature of relationship between the Parties is that of two independent contracto..."
  - P@5=0.000 R@5=0.000 signal=0.28186154727032986
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [2957:3811] score=6.258 "or entity, whether directly or by affiliation, cooperation, co-sponsorship, or any joint programs or..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [6428:7423] score=4.953 "to them on Exhibit B (as it may be amended or otherwise modified from time to time, the "Terms and C..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4433:5133] score=4.354 "Sponsor shall deliver the food (the cost of which is included in the Annual Trade Value) to the Stad..."
  - P@5=0.000 R@5=0.000 signal=0.3179904980009135

## chunk_boundary (23)
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10019:10980] score=10.026 "writ, decree or contract known to HPIL ET, or an event that results in the creation of any lien, cha..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8594:9480] score=8.286 "writ, decree or contract known to GINARES, or an event that results in the creation of any lien, cha..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17697:18522] score=7.073 "in two or more counterparts, each of which shall be deemed an original, but all of which together sh..."
  - P@5=0.023 R@5=0.265 signal=0.3073688470860299
- **cuad-d7d4d28180**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; Is there a cap on liability under this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [53891:54600] "EXCEPT UNDER SECTIONS 13(a) AND 13(b), IN NO EVENT WILL EITHER                  PARTY BE LIABLE TO T..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [54125:55003] score=12.840 "TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, WHETHER OR NOT THAT                  PARTY HAS BEEN ADVISE..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [50129:51106] score=5.510 "Client's Impression Material on                                   the Excite Network or links to the..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [51776:52776] score=4.658 "arising from:

                       i)      Its breach of any representation or covenant          ..."
  - P@5=0.104 R@5=0.670 signal=0.24840843580539426
- **cuad-b5f75eaf50**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the notice period required to terminate the renewal?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18727:19214] "Unless terminated sooner, the term of this Agreement shall begin on the Effective Date and continue ..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [19109:20065] score=13.717 "to terminate this Agreement ninety  (90) days before the end of the Initial Term or Renewal Term, if..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [38046:38848] score=5.963 "of the other, or to represent that it is in any way  responsible for the acts, debts, liabilities or..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22237:23093] score=4.118 "Period")  and in the Rubicon  Geographic Area, as defined below, ISA agrees not to in any capacity, ..."
  - P@5=0.026 R@5=0.216 signal=0.33677104897289944
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [37235:38194] score=6.591 "shall inure to the benefit of, and shall  be binding upon, the Parties and their respective successo..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [10719:11712] score=5.844 "the Day Rate for the software development the Parties shall use all  reasonable endeavours to agree ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [9037:10016] score=5.783 "such Contract Services shall be executed  under the terms and conditions of this Agreement and the a..."
  - P@5=0.065 R@5=0.318 signal=0.3474284424326055

## partial_span (12)
- **cuad-817f88727e**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; What licenses are granted under this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [38021:38280] "c)       Each party hereby grants to the other a                           non-exclusive, limited li..."
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [44306:44581] "g)       User Data will be owned by Client, and subject to the                           limitations..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [37307:38280] score=6.075 "COMMISSION.                                                      ASTERISKS DENOTE OMISSIONS.

10.   ..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [78084:79066] score=5.679 "WITH THE SECURITIES AND EXCHANGE COMMISSION.                                                      AS..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [53422:54261] score=4.556 "WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A                           PARTICULAR PURPOSE REGARDI..."
  - P@5=0.054 R@5=0.485 signal=0.2522990418764336
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11281:12173] score=7.509 "Payments.   1. Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amo..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [17469:18454] score=6.819 "agreements with third parties, Intellectual Property (as defined below) or other data provided by or..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [9951:10677] score=6.475 "is to be made by Marv. Marv shall have no duty to pay an IP Cost, whether affirmed or not affirmed, ..."
  - P@5=0.030 R@5=0.071 signal=0.34512930935808067
- **cuad-7c4a7a2903**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11296:11663] "Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amount of 5% of th..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12407:12824] "In addition to the 5% amount calculated pursuant to the preceding paragraph, there shall be an ident..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11281:12173] score=7.301 "Payments.   1. Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amo..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [17469:18454] score=7.173 "agreements with third parties, Intellectual Property (as defined below) or other data provided by or..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [21240:22239] score=6.567 "partners, employees, agents, servants, heirs, administrators, executors, successors, representatives..."
  - P@5=0.082 R@5=0.468 signal=0.2963638979565589
- **cuad-ba8c34eccc**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; What licenses are granted under this contract?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3264:3378] "THI is granted the following rights to the Applications in Appendix A and the Licensed Products deri..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4750:5144] "Licenses granted herein are solely for products in the form sold by the Licensee and are not to be c..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [5150:5453] "The grant of each license hereunder includes the right to grant sublicenses to Related Companies for..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3102:4032] score=13.798 "remain in full effect, are controlling, and apply to THI licensing of the Applications in Appendix A..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4591:5453] score=12.522 "or leased), or (iii) a method or process involving the use of a Licensed Product to manufacture (inc..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [10528:11424] score=2.766 "to pursue protection for the reverted Application or Patent. Marv has no further duty to THI for a r..."
  - P@5=0.350 R@5=0.741 signal=0.34260504646091333

## low_rank (20)
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2307:3174] score=9.832 "Arbitration............................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16203:17123] score=8.333 "Section 16. Each Party shall appoint one arbitrator who shall mutually appoint a third arbitrator wh..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8594:9480] score=4.445 "writ, decree or contract known to GINARES, or an event that results in the creation of any lien, cha..."
  - P@5=0.055 R@5=1.000 signal=0.30542601540067393
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4433:5133] score=9.627 "Sponsor shall deliver the food (the cost of which is included in the Annual Trade Value) to the Stad..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [784:1696] score=8.391 "with respect to the Team, including at the football- based stadium in Jacksonville, Florida currentl..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [2957:3811] score=6.435 "or entity, whether directly or by affiliation, cooperation, co-sponsorship, or any joint programs or..."
  - P@5=0.079 R@5=1.000 signal=0.3690994135100757
- **cuad-5e23c5d8ad**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a covenant not to sue included in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [27816:28397] "If the Executive's employment is terminated at any time by reason of any reconstruction or amalgamat..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25910:26908] score=9.280 "to deviate from these procedures in light of the Executive's seniority). These procedures do not for..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [1994:2875] score=7.627 "other way of representing or recording and recalling information which contains, reflects or is deri..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [27611:28397] score=5.980 "any reasonable expenses for which receipts and other supporting documents are provided to the reason..."
  - P@5=0.135 R@5=1.000 signal=0.3621234018945793
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7536:8468] score=6.027 "inducements, promises, or agreements, orally or otherwise, have  been made by any party, or anyone a..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [4339:5328] score=2.571 "Tarrant County, Texas and venue for any action brought in federal court shall  lie exclusively in th..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [0:912] score=2.547 "QuickLinks -- Click here to rapidly navigate through this document

    EXHIBIT 10.1

Sponsorship Ag..."
  - P@5=0.023 R@5=1.000 signal=0.35862475705593055

## irrelevant_extra (19)
- **cuad-28945a8ec1**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; Is there an anti-assignment clause in this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7079:7183] "This Agreement may not be assigned by either party without the prior written consent of the other pa..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [6781:7677] score=7.873 "its employees, independent contractors, invitees or any other third party while preparing for, filmi..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [4339:5328] score=6.080 "Tarrant County, Texas and venue for any action brought in federal court shall  lie exclusively in th..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [0:912] score=4.075 "QuickLinks -- Click here to rapidly navigate through this document

    EXHIBIT 10.1

Sponsorship Ag..."
  - P@5=0.024 R@5=1.000 signal=0.33270721053577196
- **cuad-ef501e4d8a**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; What is the governing law for this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [58417:58720] "This Agreement will be governed by                           and construed in accordance with the la..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [58235:59235] score=7.918 "Any attempt to                           assign this Agreement other than as permitted above        ..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [54125:55003] score=7.372 "TORT (INCLUDING NEGLIGENCE) OR OTHERWISE, WHETHER OR NOT THAT                  PARTY HAS BEEN ADVISE..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [32012:32887] score=3.756 "percent (95%) of the payments actually                           owed to Excite, in which case Clien..."
  - P@5=0.065 R@5=1.000 signal=0.2521295746190648
- **cuad-4b9fe1892d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the governing law for this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36019:36116] "This Agreement shall be governed by and interpreted under the laws of the State of Florida, USA,...."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [35543:36536] score=8.233 "prior written approval of such Indemnitee, such approval not to be unreasonably withheld, conditione..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [8253:9184] score=5.233 "location reasonably  designated by ISA (with appropriate agreements in place to ensure reasonable re..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [27728:28725] score=5.215 "confidentiality  obligations contained in this Section 8 shall survive termination of this Agreement..."
  - P@5=0.022 R@5=1.000 signal=0.36486593470553447
- **cuad-939bacbae2**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the governing law for this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [17415:17518] "This Agreement shall be governed by and construed in accordance with the laws of the state of Delawa..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [16595:17521] score=7.424 "and any assignment shall not diminish the liability or obligation of the assignor under the terms of..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [14275:15207] score=4.651 "materials and packaging; and

(b) it shall convey to Flotek good title to the Terpene Product free o..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [11875:12867] score=3.866 "losses, claims, demands, assessments, fines, costs or expenses (including, without limitation, reaso..."
  - P@5=0.021 R@5=1.000 signal=0.3281044275404185

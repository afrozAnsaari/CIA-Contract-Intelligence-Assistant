# Error analysis (iter04_v4_chunk_600, split=train, k=5)

Counts: chunk_boundary=27, correct_abstention=27, failure_to_abstain=1, false_abstention=12, irrelevant_extra=15, low_rank=14, ok=24, partial_span=16, wrong_section=32

## false_abstention (12)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [12290:12713] score=5.300 "on the first day of absence (and in any event not later than 11.00 am on the first day of absence) a..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [11808:12290] score=5.002 "your final remuneration on the basis that one day's holiday will be calculated as 1/260ths of your b..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [35883:36483] score=4.750 "COVENANTS

14.1 For the purpose of this paragraph 14 the following expressions shall have the follow..."
  - P@5=0.000 R@5=0.000 signal=0.24048627423572283
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42921:43515] score=10.139 "discoveries, developments and improvements, drug formulations, technology, rights in domain names, r..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [48348:48947] score=8.922 "under sections 39 to 43 (inclusive) of the Patents Act 1977 (as amended from time to time).

16 LITI..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [48947:49276] score=7.095 " become a party. This obligation on you shall include, without limitation, meeting with the Company ..."
  - P@5=0.000 R@5=0.000 signal=0.24572907288332177
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - P@5=0.000 R@5=0.000 signal=0.25964475765079537
- **cuad-28945a8ec1**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; Is there an anti-assignment clause in this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7079:7183] "This Agreement may not be assigned by either party without the prior written consent of the other pa..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [6942:7469] score=4.191 "of Performance. All sums payable under this Agreement shall be paid to the Company at Southlake, Tar..."
  - P@5=0.197 R@5=1.000 signal=0.2332307252370288

## wrong_section (32)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38359:38957] score=14.252 "or commercial activities competitive with the Restricted Business to Restricted Customers or Prospec..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40706:41304] score=12.849 "Company but would be adjudged reasonable if any particular restriction or restrictions were deleted ..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38001:38359] score=12.712 "that you will not during the Restricted Period (and in respect of sub-paragraph 14.2(f) below only, ..."
  - P@5=0.000 R@5=0.000 signal=0.2744020899529712
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3169:3769] score=1.995 "8 22. Captions........................................................................................."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10862:11379] score=1.788 "any kind or character (collectively, "Losses") arising out of or in any manner, incident, relating o..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12222:12774] score=1.772 "of HPIL ET contained in this Agreement and (ii) any failure by GINARES to perform or observe, or to ..."
  - P@5=0.000 R@5=0.000 signal=0.2945985293322439
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9990:10589] score=2.916 "the bonus is paid. Bonus entitlement does not accrue in the course of a year, and the Executive is n..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3032:3583] score=2.542 "or equivalent rights or forms of protection which subsist or will subsist now or in the future in an..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3583:4032] score=2.466 " 1.2 In this Agreement, unless the context otherwise requires: 1.2.1 words in the singular include t..."
  - P@5=0.000 R@5=0.000 signal=0.42340148237427805
- **cuad-51b4e44436**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [18678:18997] "The Company may, in its sole and absolute discretion, terminate the Executive's employment under thi..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3470:4032] score=7.808 "under this Agreement however caused, whether lawful or not, and "Termination Date" means the date of..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [11678:12251] score=7.426 "convenient to the Company and authorised in advance. 12.2 The Company's holiday year runs from 1 Jan..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [11253:11678] score=6.958 "The Executive's participation in any such benefit plans are subject to the terms and conditions of a..."
  - P@5=0.000 R@5=0.000 signal=0.39220948106236153

## chunk_boundary (27)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53642:54241] score=6.814 "by the Companies Act 2006 (as amended) and "Group Companies" will be interpreted accordingly.

21 EN..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [45196:45796] score=3.477 "sue and claim remedies for past infringement and all materials embodying these rights to the fullest..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [43759:44355] score=2.929 "a work of authorship (as a literary, musical, or artistic work) recognized by the laws of any jurisd..."
  - P@5=0.102 R@5=0.963 signal=0.31329085879019924
- **cuad-c007d50c97**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16945:17247] "To the extent that the Company IP does not vest automatically in the Company the Executive hereby as..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2604:3152] score=10.478 "or to sue for passing off, unfair competition rights, rights in designs, rights in computer software..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16631:17230] score=10.168 "or not in the course of their ordinary duties and whether or not made in working time (together, the..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16186:16631] score=8.551 "Company or any Group Companies' current or former employees or directors to the media (including on ..."
  - P@5=0.104 R@5=0.944 signal=0.34114648902615025
- **cuad-ef501e4d8a**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; What is the governing law for this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [58417:58720] "This Agreement will be governed by                           and construed in accordance with the la..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [58119:58686] score=9.535 "subsidiary or affiliate or joint venture in which the                           assigning party hold..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [47523:47994] score=2.728 "to                           the extent required by a court of competent                           j..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [54518:55003] score=2.613 "NOT EXCEED, THE AMOUNTS TO BE PAID BY CLIENT TO EXCITE                  HEREUNDER.

15.             ..."
  - P@5=0.103 R@5=0.888 signal=0.2644949069839635
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6246:6845] score=4.584 "to an End  User pursuant to which the End User may use, perform and display the Rubicon Offerings an..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5371:5959] score=4.378 "to time; and (ii) software development services.     1.13 Term shall have the meaning ascribed there..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [25810:26323] score=3.306 "the receiving Party uses to  protect its own Confidential Information, and, in any event, no less th..."
  - P@5=0.201 R@5=0.619 signal=0.3505171725122022

## partial_span (16)
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17726:18151] score=3.235 "each of which shall be deemed an original, but all of which together shall constitute one and the sa..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10518:10980] score=2.999 "respect to any claim, liability, obligations, loss, damage, assessment, judgment, cost and expense (..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10044:10518] score=2.617 "known to HPIL ET, or an event that results in the creation of any lien, charge or encumbrance upon t..."
  - P@5=0.104 R@5=0.499 signal=0.2772721639935987
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [2368:2967] score=7.070 "a writing from time to time (collectively, the "Official Designations"), solely in connection with t..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1578:2170] score=5.832 "Expiration Date"), unless sooner terminated pursuant to the terms of this Agreement.   2. Sponsor Ri..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [432:928] score=3.349 "A and B hereto, each of which is incorporated into and forms a part of this Agreement by this refere..."
  - P@5=0.211 R@5=0.750 signal=0.36686118243403426
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [1838:2395] score=4.724 "as starred in Appendix A (Covid-19 Applications) to which Premier has an exclusive license via the 2..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [1372:1838] score=4.557 "filed numerous patent applications on subject matter related to the Issued Patents which are listed ..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3129:3660] score=3.452 "controlling, and apply to THI licensing of the Applications in Appendix A and the Licensed Products ..."
  - P@5=0.271 R@5=0.360 signal=0.32036176628105567
- **cuad-be7e4dcf80**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a non-compete clause in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47554:47970] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 17, then t..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47980:48417] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 19.2, then..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [19763:20201] score=5.163 "of bodily                injury and property damage for any one occurrence arising out of           ..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43824:44409] score=4.713 "36.1    This Agreement shall be governed and construed in accordance with the         laws of the Pr..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [46948:47544] score=4.687 "age or gender group, or         reflecting unfavourably on either Party's reputation or their produc..."
  - P@5=0.174 R@5=0.488 signal=0.3596230820943985

## low_rank (14)
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22525:23093] score=11.195 "Competing Business, including  making available any information or funding to any such Rubicon Compe..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [20780:21371] score=8.568 "or have a financial interest in any ISA Competing Business, as defined  below, or provide managerial..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23428:24028] score=7.142 "engaged in the business of providing software development services for clients. "Rubicon Geographic ..."
  - P@5=0.077 R@5=1.000 signal=0.3158469412460579
- **cuad-92c250e51b**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the duration of any warranties provided in this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3021:3209] "FCC shall promptly, but in no event later than three (3) days after the date of such purchase order,..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13229:13775] score=4.042 "delivery of the Terpene Product pursuant to Section 11 of this Agreement, shall not be a cause for t..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13775:14220] score=3.389 "

(i) conform to the specifications set forth in Section 1;

3





(ii) comply with all relevant la..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [10744:11166] score=2.655 "arising out of or in any way associated with the operation of the Facility or any other facility of ..."
  - P@5=0.084 R@5=1.000 signal=0.30134816130812025
- **cuad-a53e2977ba**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does the licensee's affiliates have any licensing rights under this contract?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [5150:5292] "The grant of each license hereunder includes the right to grant sublicenses to Related Companies for..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [5294:5453] "Any such sublicense may be made effective retroactively, but not prior to the effective date hereof,..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3912:4512] score=16.769 "repair of Licensed Products which are or have been made, used, leased, owned, sold or imported by th..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4881:5453] score=15.457 "by the Marv to any act which may be performed by the Licensee, except to the extent impacted by a pa..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4512:4881] score=13.388 " which is other than the inherent use of such Licensed Product itself (as sold or leased), or (iii) ..."
  - P@5=0.115 R@5=1.000 signal=0.2845034443185936
- **cuad-89fe5271a7**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); What is the governing law for this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43832:43942] "This Agreement shall be governed and construed in accordance with the         laws of the Province o..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [36259:36853] score=7.421 "this Agreement and to fulfill any and all covenants set forth in                 this Agreement to b..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [34991:35579] score=7.303 "this Agreement and to fulfill any and all covenants set forth                  in this Agreement to ..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43453:43942] score=7.188 "exclusive property of each Party and any benefit associated with such         use shall accrue solel..."
  - P@5=0.040 R@5=1.000 signal=0.39528506837838945

## irrelevant_extra (15)
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16562:17123] score=9.509 "reasonable attorney fees) to the prevailing Party or a portion of such costs as determined by the ar..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2062:2596] score=9.048 "6   15. Compliance With The Foreign Corrupt Practices Act And Export Control And Antiboycott Laws......"
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17123:17432] score=3.409 " Binding Effect   All of the terms and provisions of this Agreement by or for the benefit of the Par..."
  - P@5=0.098 R@5=1.000 signal=0.2860135314541952
- **cuad-4b9fe1892d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the governing law for this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36019:36116] "This Agreement shall be governed by and interpreted under the laws of the State of Florida, USA,...."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [35574:36116] score=8.923 "Indemnitee, such approval not to be unreasonably withheld, conditioned or  delayed.     10.6 Essenti..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [44509:44933] score=7.421 "provided the non-performing Party takes all reasonable steps to resume full performance.     11.16 C..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36116:36594] score=6.814 "  The state and federal courts in the jurisdiction in which Palm City, Florida is located shall have..."
  - P@5=0.038 R@5=1.000 signal=0.35793658537434664
- **cuad-5b2f8a1f44**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21193] "Further, during the Non-Competition Period, Rubicon shall not solicit any





employee of ISA or an..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22525:23093] score=9.413 "Competing Business, including  making available any information or funding to any such Rubicon Compe..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [20780:21371] score=9.082 "or have a financial interest in any ISA Competing Business, as defined  below, or provide managerial..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [24862:25460] score=4.430 "other than to perform its obligations, or the exercise of such Party's rights and licenses, under th..."
  - P@5=0.093 R@5=1.000 signal=0.2888576643585683
- **cuad-cc1f3753ad**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any third-party beneficiaries designated in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41767:41984] "Except as set forth in Sections 10.3 and 10.4, nothing in this Agreement is intended to confer  bene..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41649:42237] score=13.352 "termination of this Agreement will survive the termination of this Agreement.     11.11 No Third Par..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41253:41649] score=10.619 "is in writing and signed by the Party  against whom enforcement of such waiver or excuse is sought. ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [42237:42707] score=7.436 "     11.12 Captions and Construction. The headings appearing at the beginning of the Sections contai..."
  - P@5=0.091 R@5=1.000 signal=0.30847881895882007

## failure_to_abstain (1)
- **unans-025**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is Nigel Crockett's passport number and date of birth?
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56646:57041] score=26.552 "of the parties on the date written at the top of page 1.

Executed as a Deed by BICYCLETX LIMITED ac..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:575] score=24.796 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [575:964] score=15.531 "

1. COMMENCEMENT OF EMPLOYMENT

1.1 This Agreement shall take effect 26  September 2019 (the "Effec..."

# Error analysis (iter03_v4_refine_400, split=train, k=5)

Counts: chunk_boundary=31, correct_abstention=28, false_abstention=5, irrelevant_extra=1, low_rank=6, ok=14, partial_span=13, wrong_section=70

## false_abstention (5)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [29481:29588] score=4.448 "12.2 Any grievance concerning your employment should be taken up orally in the first instance with t..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [12143:12542] score=4.301 "9.1 If you are unable to attend at work by reason of sickness or injury or any unauthorised reason y..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [35998:36256] score=4.294 ""Prospective Customer" shall mean any person, firm, company or other business who was to your knowle..."
  - P@5=0.000 R@5=0.000 signal=0.24510332346061733
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44251:44545] score=9.356 "and/or records, reports, papers, databases, data, information, know how, literature, drawings, graph..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42947:43877] score=9.074 "and improvements, drug formulations, technology, rights in domain names, rights in inventions, utili..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42529:42553] score=8.554 "15 INTELLECTUAL PROPERTY..."
  - P@5=0.000 R@5=0.000 signal=0.24849566176340612
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - P@5=0.000 R@5=0.000 signal=0.3830542323226611
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [89428:89747] score=6.209 "in the Territory and shall be responsible for entering into any contracts and other arrangements wit..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [95164:95548] score=5.757 "Any fixed and determinable savings in Product manufacturing cost to Depomed realized during the Term..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [91042:91166] score=5.423 "For purposes of clarity, all such contracts and arrangements supported by King must be executed and ..."
  - P@5=0.000 R@5=0.000 signal=0.25001251670406693

## wrong_section (70)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38476:38817] score=12.790 "(b) in the Restricted Territory, compete with the business of the Company or any Group Company eithe..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38818:38979] score=12.750 "whom you personally dealt in respect of Restricted Business in the pursuance of the employment hereu..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=11.681 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - P@5=0.000 R@5=0.000 signal=0.276970773053739
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3480:3781] score=1.615 "COOPERATION AGREEMENT   THIS COOPERATION AGREEMENT ("Agreement") is signed this 5th day of January, ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19610:19696] score=1.588 "THIS COOPERATION AGREEMENT has been entered into as of the date first set forth above...."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10981:11372] score=1.486 "any inaccuracy in any representation or breach of warranty of GINARES contained in this Agreement an..."
  - P@5=0.000 R@5=0.000 signal=0.3539153083225203
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9941:10008] score=2.672 "under notice, given or received on the date that the bonus is paid...."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9531:9941] score=2.223 "time (whether generally or in relation to the Executive only) at its absolute discretion. If the Exe..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3400:3583] score=2.028 "and "Termination" means the termination of the Executive's employment under this Agreement however c..."
  - P@5=0.000 R@5=0.000 signal=0.45104099617805377
- **cuad-51b4e44436**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [18678:18997] "The Company may, in its sole and absolute discretion, terminate the Executive's employment under thi..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [11532:11730] score=7.870 "Holidays 12.1 The Executive shall be entitled to 28 days' paid holiday in each holiday year (which i..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3941:4032] score=7.786 "1.2.3 the headings are inserted for convenience only and shall not affect its construction;..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4359:4630] score=5.721 "Term of Employment 2.1 The Executive's employment with the Company will commence on the Commencement..."
  - P@5=0.000 R@5=0.000 signal=0.40898983968169494

## chunk_boundary (31)
- **cuad-4dce24ac12**: Consider the Amendment No. 3 to Wireless Content License Agreement between Fox Mobile Entertainment, Inc. and Glu Mobile Inc.; What is the expiration date of this contract?
  - gold: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:989] "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #1: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:722] score=5.336 "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #2: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1855:1860] score=2.306 "Date:..."
  - P@5=0.961 R@5=0.317 signal=0.3978603073180332
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1455] score=8.636 "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [631:1160] score=5.873 "Jacksonville Jaguars (the "Team") and has the right to grant sponsorship rights and to exploit certa..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4734:4926] score=3.057 "If any portion of the Annual Trade Value is not used at the end of the Term, Club shall be permitted..."
  - P@5=0.076 R@5=0.391 signal=0.41798391757194747
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [2489:2770] score=6.548 "No license or right is granted for the use of any other Club intellectual property for any other pur..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:1937] score=5.678 "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [631:923] score=3.007 "Jacksonville Jaguars (the "Team") and has the right to grant sponsorship rights and to exploit certa..."
  - P@5=0.193 R@5=0.303 signal=0.42501752872573356
- **cuad-3ee0ba809a**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25311:25713] "During the term of employment and for one (1) year thereafter, the Executive will not directly or in..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25281:25543] score=9.162 "Post Termination Restrictions During the term of employment and for one (1) year thereafter, the Exe..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25717:26306] score=8.822 " Statutory Particulars 22.1 The Executive is subject to the Company's disciplinary and grievance pro..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [15673:15870] score=6.045 "15.2 The Executive shall be responsible for protecting the confidentiality of the Confidential Infor..."
  - P@5=0.155 R@5=0.577 signal=0.38365549601525595

## partial_span (13)
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17992:18145] score=2.473 "The Parties assume no liability to any third party because of any reliance on the representations, w..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9855:10850] score=2.302 "The execution, delivery and performance of this Agreement contemplated hereby will not result in a v..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11079:12065] score=2.258 "and (ii) any failure by HPIL ET to perform or observe, or to have performed or observed in full any ..."
  - P@5=0.095 R@5=0.499 signal=0.32864641586123483
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17453:17752] score=15.629 "any other Intellectual Property of Rubicon, including, without limitation, as used by Rubicon or ISA..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13454:13843] score=15.189 "Rubicon acknowledges that neither it nor any other persons or entities will by virtue of  this Agree..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17278:17314] score=12.611 "5.3 Rubicon's Intellectual Property...."
  - P@5=0.212 R@5=0.112 signal=0.32058171918315076
- **cuad-63b249d2e3**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What are the audit rights under this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5099:5340] "Flotek shall have the right at any time to (i) inspect the facility of FCC in Winter Haven, Florida ..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5342:5467] "Any such inspection or audit shall be upon reasonable notice and shall not unreasonably interfere wi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5099:5341] score=9.335 "Flotek shall have the right at any time to (i) inspect the facility of FCC in Winter Haven, Florida ..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5467:6101] score=6.619 "

9. Capacity. FCC will throughout the Term maintain adequate manufacturing capacity and staffing to..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [7014:7262] score=2.357 "Nothing in this Agreement shall obligate FCC to indemnify or save harmless Flotek or its Affiliates ..."
  - P@5=0.128 R@5=0.658 signal=0.3666704430790533
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [1193:1338] score=4.473 "WHEREAS, Premier has an Exclusive License to the Issued Patents via an Agreement executed by Marv an..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [2135:2395] score=3.877 "WHEREAS, the Parties are desirous of collaborating for the creation and distribution of products des..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:3452] score=2.892 "The licenses granted herein are exclusive worldwide licenses to:..."
  - P@5=0.048 R@5=0.034 signal=0.3932232730070666

## low_rank (6)
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21137] score=11.115 "Further, during the Non-Competition Period, Rubicon shall not solicit any..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] score=10.490 "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23552:23770] score=9.635 "7.3 In the event that ISA wishes to carry out any software development work of any nature during the..."
  - P@5=0.166 R@5=1.000 signal=0.3588590377257409
- **cuad-89fe5271a7**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); What is the governing law for this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43832:43942] "This Agreement shall be governed and construed in accordance with the         laws of the Province o..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [35117:35313] score=7.023 "(b)     the terms of this Agreement are not in breach of any law,                 regulation, by-law..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [36384:36582] score=6.859 "(b)     the terms of this Agreement are not in breach of any law,                 regulation, by-law..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [36173:36288] score=6.827 "(a)     it has the capacity, power and lawful authority to enter into                 this Agreement..."
  - P@5=0.108 R@5=1.000 signal=0.4440436315792971
- **cuad-6c078c960e**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); What are the audit rights under this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [27110:27294] "Either Party shall have the right to request the other to provide,        through an auditor agreed ..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [31639:31871] score=2.550 "17.4    In the event the Defaulting Party fails to pay any amount due pursuant         to paragraph ..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [30527:30780] score=1.525 "17.2    Upon the occurrence of an Event of Default and in addition to any         rights or remedies..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [27103:27294] score=1.491 "14.4   Either Party shall have the right to request the other to provide,        through an auditor ..."
  - P@5=0.115 R@5=1.000 signal=0.4355686982561224
- **cuad-427f94f488**: Consider the Business Affiliate Agreement between Dr. George D. Green and UNION DENTAL CORP.; What is the expiration date of this contract?
  - gold: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [6029:6252] "This Agreement  shall become  effective on the Effective Date      and shall  continue in effect unt..."
  - got #1: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [70:243] score=2.241 "This  Business  Affiliate  Agreement   ("Agreement")  dated  January  28,  2005, effective  as of Oc..."
  - got #2: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [12928:13055] score=1.958 "IN WITNESS  WHEREOF,  the Parties  hereto have caused this  Agreement to be signed as of the date an..."
  - got #3: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [12338:12888] score=1.684 "the      right to participate in any discussions or negotiations

Source: UNION DENTAL HOLDINGS, INC..."
  - P@5=0.208 R@5=1.000 signal=0.44545136507980587

## irrelevant_extra (1)
- **cuad-ee6df069ac**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What are the insurance requirements under this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [11001:11165] "FCC agrees to provide $5,000,000 of commercial liability insurance in support of this indemnity whic..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [11001:11166] score=5.239 "FCC agrees to provide $5,000,000 of commercial liability insurance in support of this indemnity whic..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [10183:10868] score=4.896 "but not be limited to, such things as proper control of ventilation, the wearing of adequate protect..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [8146:8180] score=2.138 "Fulfilling Production Requirement...."
  - P@5=0.084 R@5=1.000 signal=0.3737244854631984

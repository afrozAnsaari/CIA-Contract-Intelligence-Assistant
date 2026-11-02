# Error analysis (iter11_bm25_params, split=train, k=5)

Counts: chunk_boundary=9, correct_abstention=28, false_abstention=4, irrelevant_extra=36, low_rank=14, ok=23, partial_span=10, wrong_section=44

## false_abstention (4)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32293:33277] score=7.826 "numbers and contact names, representatives, their needs or desires with respect to the types of prod..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [31586:32293] score=6.741 "commissions, commission charges, other price sensitive information, methods of obtaining business an..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1117:2006] score=6.155 "or implied terms of any contract with, or other obligation to, any third party binding on you, inclu..."
  - P@5=0.000 R@5=0.000 signal=0.2724901666661458
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44251:45248] score=9.437 "and/or records, reports, papers, databases, data, information, know how, literature, drawings, graph..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42947:43877] score=9.177 "and improvements, drug formulations, technology, rights in domain names, rights in inventions, utili..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42253:42947] score=8.848 "During the Restricted Period you shall provide a copy of the restrictions contained at paragraph 13 ..."
  - P@5=0.096 R@5=0.786 signal=0.27626155098057925
- **cuad-cf1dc4da1d**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Is there an anti-assignment clause in this contract?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [28504:28839] "Except pursuant to Section 16.9 or in connection with the use of Third Party Sales Representatives, ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [157751:157952] "This Agreement and the rights granted herein shall not be assignable by either party hereto without ..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [77122:77926] score=6.401 "Office of the Inspector General Compliance Program Guidance for Pharmaceutical Manufacturers, the Am..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [160651:161516] score=5.104 "party was generally responsible for the preparation or drafting of this Agreement. Unless the contex..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [157653:158512] score=4.704 "their respective successors and assigns permitted under this Agreement.

Section 16.9 Assignment. Th..."
  - P@5=0.051 R@5=0.375 signal=0.29880753242047126
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [89428:90352] score=10.894 "in the Territory and shall be responsible for entering into any contracts and other arrangements wit..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [90512:91471] score=9.318 "forth in the definition of "Net Sales" in Article I. The parties have reviewed the initial pricing a..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [90352:90512] score=8.441 "







deductions from gross amounts invoiced pursuant to any such contract or arrangement shall co..."
  - P@5=0.000 R@5=0.000 signal=0.26789635497010944

## wrong_section (44)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [37817:38817] score=11.990 "agree with the Company that to protect the Company's and any and all Group Company's business intere..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38817:39508] score=11.929 " whom you personally dealt in respect of Restricted Business in the pursuance of the employment here..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=10.882 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - P@5=0.000 R@5=0.000 signal=0.3079183547798414
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7739:8739] score=2.391 "as limited by applicable bankruptcy, insolvency, reorganization, moratorium and other laws of genera..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8739:9444] score=2.391 " Litigation   There is no action, suit, proceeding or investigation pending or, to GINARES's knowled..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9444:10146] score=2.384 " or other equitable remedies.   8.2. Consents   To HPIL ET's knowledge, no consent, approval, order ..."
  - P@5=0.000 R@5=0.000 signal=0.3790616009494127
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9855:10850] score=4.691 "The execution, delivery and performance of this Agreement contemplated hereby will not result in a v..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17547:18522] score=2.456 "and their successors, any rights or remedies under or by reason of this Agreement.   19. Counterpart..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7739:8739] score=2.391 "as limited by applicable bankruptcy, insolvency, reorganization, moratorium and other laws of genera..."
  - P@5=0.000 R@5=0.000 signal=0.3518373168671787
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31414:32250] score=2.517 "any benefit from the Company which is not expressly provided for by this Agreement. 24.9 This Agreem..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9941:10787] score=2.468 "under notice, given or received on the date that the bonus is paid. Bonus entitlement does not accru..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25421:26306] score=2.445 "either themselves or through others, encourage or solicit any employee of the Company to leave the C..."
  - P@5=0.000 R@5=0.000 signal=0.49260672963794505

## chunk_boundary (9)
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [7377:8189] score=7.228 "2.4 The exclusive licenses described in Sections 2.1 and 2.2 shall not include customer agreements, ..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6776:7377] score=5.339 "and the Documentation to other  resellers, including, but not limited to, distributors, Original Equ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:6776] score=5.267 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - P@5=0.165 R@5=0.592 signal=0.46888065504849497
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=10.464 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:7069] score=8.703 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18145:19143] score=8.682 "granted in this  Agreement. ISA shall not contest ownership by Rubicon of any of the foregoing. No l..."
  - P@5=0.131 R@5=0.581 signal=0.43050660438221017
- **cuad-72c36b3768**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:7069] score=14.117 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5380:6070] score=11.367 "and (ii) software development services.     1.13 Term shall have the meaning ascribed thereto in Sec..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=10.464 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - P@5=0.223 R@5=0.988 signal=0.3876439948852576
- **cuad-c7ebebcdaa**: Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [6502:7242] "Except as otherwise provided herein, all the results of ABG's provision of CELEBRITY'S Services here..."
  - got #1: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [6620:7514] score=8.617 "but not limited to, Materials (but in all cases specifically excluding the Celebrity Endorsement and..."
  - got #2: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [7514:8030] score=7.828 " PAPA JOHN'S hereby acknowledges that PAPA JOHN'S exercise of the Celebrity Endorsement (including, ..."
  - got #3: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [15911:16680] score=7.594 "the Term or at any time thereafter, attack or challenge, or lend assistance to any third party in co..."
  - P@5=0.170 R@5=0.841 signal=0.3170251284135392

## partial_span (10)
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=16.790 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17453:18445] score=14.775 "any other Intellectual Property of Rubicon, including, without limitation, as used by Rubicon or ISA..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [16774:17453] score=12.024 "limitation, the execution and delivery of  copyright applications, patent applications, declarations..."
  - P@5=0.055 R@5=0.112 signal=0.3563993286252448
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [1193:2132] score=6.276 "WHEREAS, Premier has an Exclusive License to the Issued Patents via an Agreement executed by Marv an..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4995:5933] score=4.724 "herein to the Licensee, or (ii) to include licenses to contributorily infringe or induce infringemen..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [2132:2793] score=4.687 "   WHEREAS, the Parties are desirous of collaborating for the creation and distribution of products ..."
  - P@5=0.049 R@5=0.107 signal=0.44369991128127195
- **cuad-7c4a7a2903**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11296:11663] "Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amount of 5% of th..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12407:12824] "In addition to the 5% amount calculated pursuant to the preceding paragraph, there shall be an ident..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [21083:22082] score=4.367 "Parties to be charged with such modification. This Agreement shall be binding upon and shall inure t..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [16613:17610] score=2.535 "such confidential information, for its or another's benefit, in any way acquired in the course of an..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4427:5293] score=2.402 "Licensed Product (as sold or leased) with any other product, (ii) a method or process which is other..."
  - P@5=0.080 R@5=0.468 signal=0.36980030279703247
- **cuad-be7e4dcf80**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a non-compete clause in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47554:47970] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 17, then t..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47980:48417] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 19.2, then..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [19099:20060] score=8.104 "9.1    Each Party shall purchase and maintain, at its own expense, the        following insurance co..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [20060:20643] score=7.798 " The other party shall                be named as an additional insured and the policy shall contain..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43531:44438] score=4.128 "use shall accrue solely to that Party. Each Party shall use the other         Party's trade-mark, di..."
  - P@5=0.115 R@5=0.488 signal=0.43035901646633135

## low_rank (14)
- **cuad-c007d50c97**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16945:17247] "To the extent that the Company IP does not vest automatically in the Company the Executive hereby as..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2525:3399] score=9.293 "trademarks, trade names and domain names, rights in get-up, rights in goodwill or to sue for passing..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16645:17435] score=9.213 "course of their ordinary duties and whether or not made in working time (together, the "Company IP")..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [1821:2525] score=8.874 "or electronic form or on any magnetic or optical disk or memory and wherever located) including, wit..."
  - P@5=0.080 R@5=1.000 signal=0.3912332470938879
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [20522:21517] score=10.744 "Initial Term and (ii) the date falling two  years after completion of the most recent services provi..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22344:23093] score=9.872 "or have a financial interest in any Rubicon Competing Business, as  defined below, or provide manage..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23093:23797] score=9.370 " ISA acknowledges, however, that the Parties have negotiated this Section and that the time limitati..."
  - P@5=0.052 R@5=1.000 signal=0.3989532542355819
- **cuad-92c250e51b**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the duration of any warranties provided in this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3021:3209] "FCC shall promptly, but in no event later than three (3) days after the date of such purchase order,..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13245:14220] score=3.330 "Terpene Product pursuant to Section 11 of this Agreement, shall not be a cause for termination of th..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [10183:11166] score=1.739 "but not be limited to, such things as proper control of ventilation, the wearing of adequate protect..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2383:3209] score=1.695 "for Terpene Product shall be the Product Price of that Terpene Product.

5. Forecasts; Terpene Cost ..."
  - P@5=0.046 R@5=1.000 signal=0.38778006216136324
- **cuad-89fe5271a7**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); What is the governing law for this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43832:43942] "This Agreement shall be governed and construed in accordance with the         laws of the Province o..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [34599:35313] score=6.456 "mailed shall be deemed to have         been received five (5) business days after being mailed. In t..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [35704:36582] score=6.354 "are no pending or threatened actions or proceedings to                 Dynamex is a Party, or which ..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [36582:37025] score=6.246 "

     (c)     all necessary licenses, permits, consents or approvals of,                 notices to..."
  - P@5=0.033 R@5=1.000 signal=0.474700945408527

## irrelevant_extra (36)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53459:54272] score=5.820 "a subsidiary or affiliate and any other company which is for the time being a holding company of the..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [54272:54730] score=5.300 "

Any notices with respect to this Agreement shall be in writing and shall be deemed given if delive..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32293:33277] score=3.300 "numbers and contact names, representatives, their needs or desires with respect to the types of prod..."
  - P@5=0.074 R@5=1.000 signal=0.34930454951636003
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16376:17340] score=7.468 "be held, and any award shall be rendered, in Paris (France), in the English language. The award may ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [1775:2741] score=6.632 "5 13. Notices.........................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2741:3322] score=6.200 " Counterparts.........................................................................................."
  - P@5=0.059 R@5=1.000 signal=0.366016242422265
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17041:17843] score=3.658 "provisions which would require the application of any law other than Nevada.   18. Binding Effect   ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [6086:7018] score=3.651 "HPIL ET's obligations under this Agreement are to: (i) Follow up on developments regarding GINARES; ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16376:17041] score=2.595 "be held, and any award shall be rendered, in Paris (France), in the English language. The award may ..."
  - P@5=0.022 R@5=1.000 signal=0.3237788775370951
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1160:1937] score=7.980 "covenants contained herein, the parties agree as follows:   1. Term of Agreement. This Agreement sha..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [3966:4926] score=7.647 "Dicks' Wings restaurant with values equal to the following (each, an "Annual Trade Value"):   First ..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4926:5622] score=6.793 " The parties acknowledge that the Annual Trade Value is inclusive of any taxes, surcharges or relate..."
  - P@5=0.094 R@5=1.000 signal=0.4568385282920873

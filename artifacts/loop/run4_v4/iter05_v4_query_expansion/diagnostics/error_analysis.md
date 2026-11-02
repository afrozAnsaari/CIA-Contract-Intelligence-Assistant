# Error analysis (iter05_v4_query_expansion, split=train, k=5)

Counts: chunk_boundary=16, correct_abstention=28, false_abstention=3, irrelevant_extra=44, low_rank=16, ok=37, partial_span=10, wrong_section=14

## false_abstention (3)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [29036:30019] score=4.448 "hereunder terminates.

"Time-Based Equity Awards" means all time-based stock options and other stock..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [11845:12713] score=4.301 "that one day's holiday will be calculated as 1/260ths of your basic annual salary.

8.5 In the event..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [35511:36256] score=4.294 "mobile telephones, computer and related equipment, PDA or similar device, security passes, accounts,..."
  - P@5=0.000 R@5=0.000 signal=0.24510332346061733
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44251:45248] score=15.770 "and/or records, reports, papers, databases, data, information, know how, literature, drawings, graph..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42947:43877] score=11.219 "and improvements, drug formulations, technology, rights in domain names, rights in inventions, utili..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [46688:47688] score=10.720 "commence and prosecute legal and other proceedings against any third party for infringement of any I..."
  - P@5=0.088 R@5=0.786 signal=0.24849566176340612
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [9995:10754] score=8.094 "and distributors for the 1000mg Formulation equal to or in excess of (i) [***] percent of the aggreg..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [89428:90352] score=7.471 "in the Territory and shall be responsible for entering into any contracts and other arrangements wit..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [90352:90810] score=6.057 "







deductions from gross amounts invoiced pursuant to any such contract or arrangement shall co..."
  - P@5=0.000 R@5=0.000 signal=0.25001251670406693

## wrong_section (14)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [37817:38817] score=18.707 "agree with the Company that to protect the Company's and any and all Group Company's business intere..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=15.374 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38817:39508] score=14.755 " whom you personally dealt in respect of Restricted Business in the pursuance of the employment here..."
  - P@5=0.000 R@5=0.000 signal=0.276970773053739
- **cuad-51b4e44436**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [18678:18997] "The Company may, in its sole and absolute discretion, terminate the Executive's employment under thi..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [11073:12015] score=10.333 "the charging structure and the default fund from time to time. 11. Benefits During the course of emp..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3106:4032] score=9.318 "now or in the future in any part of the world; "Invention" means any invention, idea, discovery, dev..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4032:4705] score=8.267 " 1.2.4 reference to a particular law is a reference to it as it is in force for the time being takin..."
  - P@5=0.000 R@5=0.000 signal=0.40898983968169494
- **cuad-99d88902f8**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; What is the expiration date of this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [33237:33842] "Unless terminated earlier in accordance with the                           specific terms of this Ag..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [33913:34766] score=10.481 "impressions, the term of this Agreement will not be                           shorter than [*****]  ..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [34766:35255] score=7.340 "

              d)       The provisions of Section 12 (Confidentiality and                          ..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [60229:61222] score=6.880 "and will                           be excused to the extent caused by any occurrence                ..."
  - P@5=0.000 R@5=0.000 signal=0.32038511084049665
- **cuad-188e3e6478**: Consider the Co-Branding Agreement between PC Quote, Inc. and A.B. Watley, Inc. for Market Data Software; What licenses are granted under this contract?
  - gold: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [1881:2005] "PCQ agrees to allow ABW to co-brand the PCQ SOFTWARE in order to provide a value added service on AB..."
  - got #1: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [14471:15470] score=3.335 "cooperates with PCQ so that PCQ will not be      prejudiced in the defense, settlement or other hand..."
  - got #2: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [17545:18543] score=1.833 "paragraph of this Agreement.  Either party may change its address specified above by giving the othe..."
  - got #3: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [6258:7065] score=1.505 "is not paid by ABW within forty-five (45) days after receipt, and when no discrepancy issues have be..."
  - P@5=0.000 R@5=0.000 signal=0.3921952557323418

## chunk_boundary (16)
- **cuad-5e23c5d8ad**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a covenant not to sue included in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [27816:28397] "If the Executive's employment is terminated at any time by reason of any reconstruction or amalgamat..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2525:3399] score=5.552 "trademarks, trade names and domain names, rights in get-up, rights in goodwill or to sue for passing..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [1821:2525] score=5.153 "or electronic form or on any magnetic or optical disk or memory and wherever located) including, wit..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31950:32861] score=2.103 "not be enforceable by any person other than those parties. 24.11 This Agreement and any dispute or c..."
  - P@5=0.099 R@5=0.644 signal=0.3999536524258994
- **cuad-3f772ec774**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the expiration date of this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18727:19214] "Unless terminated sooner, the term of this Agreement shall begin on the Effective Date and continue ..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18145:19143] score=6.304 "granted in this  Agreement. ISA shall not contest ownership by Rubicon of any of the foregoing. No l..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [43617:44597] score=5.611 "to this Agreement shall be in the English language. All words used in this Agreement will be constru..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21687:22639] score=4.552 "are reasonable in light of the circumstances  pertaining to ISA and this transaction. "ISA Competing..."
  - P@5=0.088 R@5=0.854 signal=0.40275430137100987
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:7069] score=3.767 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5380:6070] score=3.650 "and (ii) software development services.     1.13 Term shall have the meaning ascribed thereto in Sec..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13828:14604] score=2.876 "this Agreement. Rubicon shall not contest ownership by ISA of any of the foregoing. No right, licens..."
  - P@5=0.241 R@5=0.988 signal=0.42098451940644627
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13828:14604] score=10.736 "this Agreement. Rubicon shall not contest ownership by ISA of any of the foregoing. No right, licens..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:7069] score=10.648 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:13828] score=10.624 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - P@5=0.131 R@5=0.581 signal=0.38724132249325915

## partial_span (10)
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11079:12065] score=5.116 "and (ii) any failure by HPIL ET to perform or observe, or to have performed or observed in full any ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9855:10850] score=4.540 "The execution, delivery and performance of this Agreement contemplated hereby will not result in a v..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17547:18522] score=2.473 "and their successors, any rights or remedies under or by reason of this Agreement.   19. Counterpart..."
  - P@5=0.050 R@5=0.499 signal=0.32864641586123483
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17453:18445] score=15.629 "any other Intellectual Property of Rubicon, including, without limitation, as used by Rubicon or ISA..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=15.189 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36382:37381] score=14.874 "or performance or  nonperformance of any obligation under this Agreement, save that the parties agre..."
  - P@5=0.049 R@5=0.112 signal=0.32058171918315076
- **cuad-be7e4dcf80**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a non-compete clause in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47554:47970] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 17, then t..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47980:48417] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 19.2, then..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [46811:47544] score=6.591 "or         ridicule, or shocking, insulting or offending potential customers of         either Party..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47544:47970] score=5.490 "

32.1    In the event this Agreement is terminated pursuant to the provisions of         paragraph ..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [19099:20060] score=4.683 "9.1    Each Party shall purchase and maintain, at its own expense, the        following insurance co..."
  - P@5=0.115 R@5=0.488 signal=0.4025654096604873
- **cuad-31e7123c70**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; What licenses are granted under this contract?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [27994:28354] "During the Term, subject to the terms and conditions of this Agreement, Depomed hereby grants to Kin..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [53731:53951] "Depomed hereby grants to King the non-exclusive right, during the Term, to use the Launch Promotiona..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65962:66236] "Subject to this Section 4.8 and to applicable Legal Requirements, Depomed shall have the right to us..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [144427:144889] "Depomed agrees to grant and hereby grants to King an exclusive option (exercisable at King's sole di..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [132643:133640] score=11.106 "of any pending, threatened or contemplated patent litigation with respect to extended release metfor..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65292:66236] score=10.167 "adverse to Depomed by virtue of the rights granted under this Agreement or through King's use of the..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [122675:123536] score=9.246 "enforcement of creditors' rights in general and to general principles of equity (regardless of wheth..."
  - P@5=0.230 R@5=0.452 signal=0.3373522019222154

## low_rank (16)
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7377:8122] score=6.732 "all of the covenants and agreements between the parties with respect to the subject  matter. Each pa..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [8122:8818] score=5.825 "

21. Government Regulation. This Agreement is subject to all applicable federal, state and municipa..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3358:4138] score=3.894 "change the address at which notice may be sent to that party by giving notice  of such change to the..."
  - P@5=0.030 R@5=1.000 signal=0.3830542323226611
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [20522:21517] score=16.818 "Initial Term and (ii) the date falling two  years after completion of the most recent services provi..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22344:23093] score=14.592 "or have a financial interest in any Rubicon Competing Business, as  defined below, or provide manage..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23093:23797] score=13.919 " ISA acknowledges, however, that the Parties have negotiated this Section and that the time limitati..."
  - P@5=0.065 R@5=1.000 signal=0.3588590377257409
- **cuad-d0144819a9**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; Does this contract include any volume restrictions?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [958:1076] ""Maximum Quantity" means [***] pounds of Terpene Product per Year, prorated for any partial Year inc..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3210:3809] "FCC shall be obligated to accept all such purchase orders unless the amount ordered for a Year excee..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [4600:5467] score=6.682 "Representatives of Flotek and FCC shall consult with each other from time to time during the Term to..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [4057:4600] score=5.409 "All sales of Terpene Product subject to this Agreement shall be pursuant to the terms and conditions..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [659:1513] score=5.092 "covenants and agreements contained herein, the parties do hereby agree as follows:

1. Definitions. ..."
  - P@5=0.179 R@5=1.000 signal=0.34802074597634886
- **cuad-92c250e51b**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the duration of any warranties provided in this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3021:3209] "FCC shall promptly, but in no event later than three (3) days after the date of such purchase order,..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13245:14220] score=5.052 "Terpene Product pursuant to Section 11 of this Agreement, shall not be a cause for termination of th..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5809:6801] score=3.438 "or Flotek from receiving and/or using the Terpene Product, shall operate to reduce or suspend delive..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2909:3809] score=3.194 "shall order Terpene Product by sending to FCC written purchase orders in the form attached hereto as..."
  - P@5=0.048 R@5=1.000 signal=0.3476804850391368

## irrelevant_extra (44)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53459:54272] score=8.413 "a subsidiary or affiliate and any other company which is for the time being a holding company of the..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [54272:54730] score=7.306 "

Any notices with respect to this Agreement shall be in writing and shall be deemed given if delive..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42947:43877] score=4.675 "and improvements, drug formulations, technology, rights in domain names, rights in inventions, utili..."
  - P@5=0.077 R@5=1.000 signal=0.3138046886065981
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [4790:5744] score=3.765 "fuel energy (such as kerosene and/or diesel) as well as the further production of electricity, that ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19307:20008] score=3.047 "modification, waiver or termination is asserted. No waiver of any of the provisions of this Agreemen..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10551:11379] score=3.016 "obligations, loss, damage, assessment, judgment, cost and expense (including, without limitation, re..."
  - P@5=0.035 R@5=1.000 signal=0.3539153083225203
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16376:17340] score=9.560 "be held, and any award shall be rendered, in Paris (France), in the English language. The award may ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [1775:2741] score=7.667 "5 13. Notices.........................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2741:3322] score=7.404 " Counterparts.........................................................................................."
  - P@5=0.057 R@5=1.000 signal=0.34189075590433926
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17041:17843] score=3.930 "provisions which would require the application of any law other than Nevada.   18. Binding Effect   ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16376:17041] score=2.630 "be held, and any award shall be rendered, in Paris (France), in the English language. The award may ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [18225:18961] score=2.440 "obligations under this Agreement within thirty (30) days of receipt by the Party of written terminat..."
  - P@5=0.025 R@5=1.000 signal=0.302437412215459

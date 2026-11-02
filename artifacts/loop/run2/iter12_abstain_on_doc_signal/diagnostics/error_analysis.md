# Error analysis (iter12_abstain_on_doc_signal, split=train, k=5)

Counts: chunk_boundary=8, correct_abstention=23, failure_to_abstain=5, false_abstention=9, irrelevant_extra=33, low_rank=14, ok=23, partial_span=11, wrong_section=42

## false_abstention (9)
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7739:8739] score=2.374 "as limited by applicable bankruptcy, insolvency, reorganization, moratorium and other laws of genera..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8739:9444] score=2.374 " Litigation   There is no action, suit, proceeding or investigation pending or, to GINARES's knowled..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9444:10146] score=2.362 " or other equitable remedies.   8.2. Consents   To HPIL ET's knowledge, no consent, approval, order ..."
  - P@5=0.000 R@5=0.000 signal=0.42494157504916047
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16376:17340] score=7.934 "be held, and any award shall be rendered, in Paris (France), in the English language. The award may ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [1775:2741] score=7.667 "5 13. Notices.........................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2741:3322] score=7.404 " Counterparts.........................................................................................."
  - P@5=0.059 R@5=1.000 signal=0.42494157504916047
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17041:17843] score=3.930 "provisions which would require the application of any law other than Nevada.   18. Binding Effect   ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [6086:7018] score=3.624 "HPIL ET's obligations under this Agreement are to: (i) Follow up on developments regarding GINARES; ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16376:17041] score=2.630 "be held, and any award shall be rendered, in Paris (France), in the English language. The award may ..."
  - P@5=0.022 R@5=1.000 signal=0.42494157504916047
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9855:10850] score=4.594 "The execution, delivery and performance of this Agreement contemplated hereby will not result in a v..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17547:18522] score=2.473 "and their successors, any rights or remedies under or by reason of this Agreement.   19. Counterpart..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7739:8739] score=2.374 "as limited by applicable bankruptcy, insolvency, reorganization, moratorium and other laws of genera..."
  - P@5=0.000 R@5=0.000 signal=0.42494157504916047

## wrong_section (42)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [37817:38817] score=12.790 "agree with the Company that to protect the Company's and any and all Group Company's business intere..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38817:39508] score=12.750 " whom you personally dealt in respect of Restricted Business in the pursuance of the employment here..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=11.681 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - P@5=0.000 R@5=0.000 signal=0.5444497275765091
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32293:33277] score=7.924 "numbers and contact names, representatives, their needs or desires with respect to the types of prod..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [31586:32293] score=6.704 "commissions, commission charges, other price sensitive information, methods of obtaining business an..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1117:2006] score=6.291 "or implied terms of any contract with, or other obligation to, any third party binding on you, inclu..."
  - P@5=0.000 R@5=0.000 signal=0.5444497275765091
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9941:10787] score=2.672 "under notice, given or received on the date that the bonus is paid. Bonus entitlement does not accru..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31414:32250] score=2.585 "any benefit from the Company which is not expressly provided for by this Agreement. 24.9 This Agreem..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25421:26306] score=2.462 "either themselves or through others, encourage or solicit any employee of the Company to leave the C..."
  - P@5=0.000 R@5=0.000 signal=0.5648301258441157
- **cuad-51b4e44436**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [18678:18997] "The Company may, in its sole and absolute discretion, terminate the Executive's employment under thi..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [11073:12015] score=7.870 "the charging structure and the default fund from time to time. 11. Benefits During the course of emp..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3106:4032] score=7.786 "now or in the future in any part of the world; "Invention" means any invention, idea, discovery, dev..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [21894:22801] score=7.105 "Executive from any or all of the Executive's duties during any period in which the Company is invest..."
  - P@5=0.000 R@5=0.000 signal=0.5648301258441157

## chunk_boundary (8)
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44251:45248] score=9.356 "and/or records, reports, papers, databases, data, information, know how, literature, drawings, graph..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42947:43877] score=9.074 "and improvements, drug formulations, technology, rights in domain names, rights in inventions, utili..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42253:42947] score=8.554 "During the Restricted Period you shall provide a copy of the restrictions contained at paragraph 13 ..."
  - P@5=0.096 R@5=0.786 signal=0.5444497275765091
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [7377:8189] score=7.370 "2.4 The exclusive licenses described in Sections 2.1 and 2.2 shall not include customer agreements, ..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6776:7377] score=5.508 "and the Documentation to other  resellers, including, but not limited to, distributors, Original Equ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:6776] score=5.309 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - P@5=0.165 R@5=0.592 signal=0.6136295505946907
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=10.894 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14127:14604] score=9.276 " Except for  the rights and licenses expressly granted under this Agreement, ISA reserves all rights..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:7069] score=9.172 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - P@5=0.131 R@5=0.581 signal=0.6136295505946907
- **cuad-72c36b3768**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6070:7069] score=14.464 "Agreement. As used in this Section  2.1, the terms "market," "sale," "sell," "distribute," and "subl..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5380:6070] score=11.093 "and (ii) software development services.     1.13 Term shall have the meaning ascribed thereto in Sec..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=10.894 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - P@5=0.223 R@5=0.988 signal=0.6136295505946907

## partial_span (11)
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13158:14127] score=17.625 "as they may be part of or incorporated into any Contract Service or otherwise used by  Rubicon, all ..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17453:18445] score=15.629 "any other Intellectual Property of Rubicon, including, without limitation, as used by Rubicon or ISA..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [12629:13158] score=12.684 "retain the financial records relating to all payments owed and/or paid under this Agreement for a pe..."
  - P@5=0.055 R@5=0.112 signal=0.6136295505946907
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [1193:2132] score=6.544 "WHEREAS, Premier has an Exclusive License to the Issued Patents via an Agreement executed by Marv an..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [2132:2793] score=4.899 "   WHEREAS, the Parties are desirous of collaborating for the creation and distribution of products ..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4995:5933] score=4.726 "herein to the Licensee, or (ii) to include licenses to contributorily infringe or induce infringemen..."
  - P@5=0.049 R@5=0.107 signal=0.6364652422298435
- **cuad-7c4a7a2903**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11296:11663] "Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amount of 5% of th..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12407:12824] "In addition to the 5% amount calculated pursuant to the preceding paragraph, there shall be an ident..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [21083:22082] score=4.400 "Parties to be charged with such modification. This Agreement shall be binding upon and shall inure t..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [16613:17610] score=2.719 "such confidential information, for its or another's benefit, in any way acquired in the course of an..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4427:5293] score=2.555 "Licensed Product (as sold or leased) with any other product, (ii) a method or process which is other..."
  - P@5=0.087 R@5=0.468 signal=0.6364652422298435
- **cuad-be7e4dcf80**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a non-compete clause in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47554:47970] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 17, then t..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47980:48417] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 19.2, then..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [19099:20060] score=8.363 "9.1    Each Party shall purchase and maintain, at its own expense, the        following insurance co..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [20060:20643] score=8.124 " The other party shall                be named as an additional insured and the policy shall contain..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [46811:47544] score=4.404 "or         ridicule, or shocking, insulting or offending potential customers of         either Party..."
  - P@5=0.115 R@5=0.488 signal=0.6755824266002425

## low_rank (14)
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [20522:21517] score=11.115 "Initial Term and (ii) the date falling two  years after completion of the most recent services provi..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22344:23093] score=10.490 "or have a financial interest in any Rubicon Competing Business, as  defined below, or provide manage..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23093:23797] score=9.635 " ISA acknowledges, however, that the Parties have negotiated this Section and that the time limitati..."
  - P@5=0.059 R@5=1.000 signal=0.6136295505946907
- **cuad-92c250e51b**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the duration of any warranties provided in this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3021:3209] "FCC shall promptly, but in no event later than three (3) days after the date of such purchase order,..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13245:14220] score=3.286 "Terpene Product pursuant to Section 11 of this Agreement, shall not be a cause for termination of th..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2383:3209] score=1.792 "for Terpene Product shall be the Product Price of that Terpene Product.

5. Forecasts; Terpene Cost ..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [10183:11166] score=1.778 "but not be limited to, such things as proper control of ventilation, the wearing of adequate protect..."
  - P@5=0.046 R@5=1.000 signal=0.6312910966991221
- **cuad-89fe5271a7**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); What is the governing law for this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43832:43942] "This Agreement shall be governed and construed in accordance with the         laws of the Province o..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [34599:35313] score=7.023 "mailed shall be deemed to have         been received five (5) business days after being mailed. In t..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [36289:37025] score=6.859 "any and all covenants set forth in                 this Agreement to be fulfilled by it;

     (b)  ..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [35704:36289] score=6.827 "are no pending or threatened actions or proceedings to                 Dynamex is a Party, or which ..."
  - P@5=0.033 R@5=1.000 signal=0.6755824266002425
- **cuad-6c078c960e**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); What are the audit rights under this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [27110:27294] "Either Party shall have the right to request the other to provide,        through an auditor agreed ..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [21548:22284] score=2.838 "insurance coverages, if any, are necessary and advisable for its own        protection

9           ..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [31090:31952] score=2.550 "and

     (c)     take possession, immediately, without demand or notice, without                 an..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [15964:16943] score=2.411 "with such investigation shall be the responsibility of such Party if the        loss, damage or dela..."
  - P@5=0.044 R@5=1.000 signal=0.6755824266002425

## irrelevant_extra (33)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53459:54272] score=6.059 "a subsidiary or affiliate and any other company which is for the time being a holding company of the..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [54272:54730] score=5.548 "

Any notices with respect to this Agreement shall be in writing and shall be deemed given if delive..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32293:33277] score=3.409 "numbers and contact names, representatives, their needs or desires with respect to the types of prod..."
  - P@5=0.071 R@5=1.000 signal=0.5444497275765091
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1160:1937] score=8.636 "covenants contained herein, the parties agree as follows:   1. Term of Agreement. This Agreement sha..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [3966:4926] score=7.870 "Dicks' Wings restaurant with values equal to the following (each, an "Annual Trade Value"):   First ..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4926:5622] score=6.744 " The parties acknowledge that the Annual Trade Value is inclusive of any taxes, surcharges or relate..."
  - P@5=0.094 R@5=1.000 signal=0.6110345924158768
- **cuad-c007d50c97**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16945:17247] "To the extent that the Company IP does not vest automatically in the Company the Executive hereby as..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16645:17435] score=9.621 "course of their ordinary duties and whether or not made in working time (together, the "Company IP")..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2525:3399] score=9.261 "trademarks, trade names and domain names, rights in get-up, rights in goodwill or to sue for passing..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16005:16645] score=8.799 "the proper course of their employment. 15.4 Save as authorised by the Company, the Executive shall n..."
  - P@5=0.080 R@5=1.000 signal=0.5648301258441157
- **cuad-28945a8ec1**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; Is there an anti-assignment clause in this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7079:7183] "This Agreement may not be assigned by either party without the prior written consent of the other pa..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [6764:7677] score=7.071 "by the  Company, its employees, independent contractors, invitees or any other third party while pre..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7677:8122] score=4.338 "







  not set forth in this contract, and that no agreement, statement, or promise not contained..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [5028:5763] score=4.255 "may be awarded. For  the purposes of this clause, the prevailing party is the party in whose favor f..."
  - P@5=0.031 R@5=1.000 signal=0.5593346845754873

## failure_to_abstain (5)
- **unans-025**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is Nigel Crockett's passport number and date of birth?
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56466:57041] score=26.734 "or

(d) obtains Control of BTL in any other way, including but not limited to by way of a merger.

1..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=24.013 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [7106:7937] score=5.927 "22,378 Shares (representing approximately 0.125% of the Company's issued share capital as at the Eff..."
- **unans-026**: Consider the Cooperation Agreement of HPIL Holding; What was HPIL Holding's closing share price on NASDAQ on the signing date?
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=17.266 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11079:12065] score=15.547 "and (ii) any failure by HPIL ET to perform or observe, or to have performed or observed in full any ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3970:4448] score=14.877 " HPIL ET does not restrict its potential candidate target companies to any specific geographical loc..."
- **unans-027**: Consider the Sponsorship Agreement of Vitamin Shoppe; What is the sponsored athlete's marathon personal-best time?
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [77159:77921] score=6.333 "12 Exclusive Offer       2 e-mail offer tests          [*****] Tests                          Push a..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [76467:77159] score=5.772 "Target model creation         [*****]

                      Model role-out                [*****] -..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [75813:76467] score=5.709 "facilitation of the Client's program. Performance results for these campaigns will be provided to Cl..."
- **unans-028**: Consider the Transportation Services Agreement of Dynamex; What is the average fuel efficiency of the delivery trucks in miles per gallon?
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [32303:33217] score=7.867 "Monthly Performance Failure ("Default Month").

     For each Default Month, the Party in default sh..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [48335:49218] score=6.633 "for a period of twelve (12)         months from the effective date of termination.

The Parties have..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [33217:33774] score=4.795 "

19.1    Either Party may terminate this Agreement, without cause, by giving two         (2) years ..."

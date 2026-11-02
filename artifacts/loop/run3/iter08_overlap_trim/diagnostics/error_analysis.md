# Error analysis (iter08_overlap_trim, split=train, k=5)

Counts: chunk_boundary=5, correct_abstention=28, false_abstention=3, irrelevant_extra=31, low_rank=18, ok=27, partial_span=12, wrong_section=44

## false_abstention (3)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [31888:32705] score=7.409 "and agreements, internal services and operational manuals, methods of conducting Company business, c..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [815:1813] score=6.154 "other in accordance with paragraph 11 below. No employment with a previous employer is deemed to be ..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [29338:30329] score=5.725 "12.1 A copy of the Company's disciplinary, dismissal and grievance procedures are set out in its emp..."
  - P@5=0.000 R@5=0.000 signal=0.2396526687932834
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42947:43877] score=9.305 "and improvements, drug formulations, technology, rights in domain names, rights in inventions, utili..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42096:42947] score=8.691 "Leave under paragraph 10 above then the Restricted Period shall be reduced by any period/s spent by ..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [48320:49276] score=7.960 "of, restricting your rights under sections 39 to 43 (inclusive) of the Patents Act 1977 (as amended ..."
  - P@5=0.112 R@5=1.000 signal=0.24319460535670287
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [90202:91188] score=11.099 "of the Commission pursuant to the Company's application requesting confidential treatment under Rule..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [89597:90202] score=9.619 "and approving the form, content and terms and conditions thereof, including any discount, allowance,..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [88906:89597] score=8.144 "Third Party supply agreement relating to the Product (as so modified and approved for the applicable..."
  - P@5=0.000 R@5=0.000 signal=0.2489437617039298

## wrong_section (44)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [37964:38961] score=12.943 "stability of its or their workforce, that you will not during the Restricted Period (and in respect ..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40505:41502] score=11.624 "more of such restrictions shall either taken by itself or themselves together be adjudged to go beyo..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38961:39806] score=10.528 " Termination Date;

12





(c) in the Restricted Territory, compete with the business of the Compan..."
  - P@5=0.000 R@5=0.000 signal=0.2722828510467912
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7875:8739] score=2.525 "of creditors' rights generally and (ii) as limited by laws relating to the availability of specific ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9335:10164] score=2.525 "generally and (ii) as limited by laws relating to the availability of specific performance, injuncti..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8739:9335] score=2.458 " Litigation   There is no action, suit, proceeding or investigation pending or, to GINARES's knowled..."
  - P@5=0.000 R@5=0.000 signal=0.35433040540580063
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [10019:10980] score=4.600 "writ, decree or contract known to HPIL ET, or an event that results in the creation of any lien, cha..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17697:18522] score=2.610 "in two or more counterparts, each of which shall be deemed an original, but all of which together sh..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7875:8739] score=2.525 "of creditors' rights generally and (ii) as limited by laws relating to the availability of specific ..."
  - P@5=0.000 R@5=0.000 signal=0.32781903229278236
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31348:32250] score=2.498 "24.8 The Executive shall not be contractually entitled to receive any benefit from the Company which..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [22150:22976] score=2.420 "shall not constitute disciplinary action. During any period of suspension, the Company may impose th..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25132:26059] score=2.395 "compliance with the obligations under clauses 20.1.1 and 20.1.2 together with such reasonable eviden..."
  - P@5=0.000 R@5=0.000 signal=0.4508216947720841

## chunk_boundary (5)
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13694:14604] score=9.305 "any of the foregoing, or any associated goodwill and that its rights thereunder are strictly limited..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5933:6932] score=9.049 "the Rubicon Offerings, the  Documentation and, subject to Section 2.2, any upgrades thereto, subject..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17604:18445] score=8.651 "the copyright and all other Intellectual Property rights inherent in or appurtenant to the foregoing..."
  - P@5=0.161 R@5=0.740 signal=0.3870514292798722
- **cuad-72c36b3768**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5933:6932] score=14.316 "the Rubicon Offerings, the  Documentation and, subject to Section 2.2, any upgrades thereto, subject..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5342:5933] score=11.246 "to ISA by Rubicon from  time to time; and (ii) software development services.     1.13 Term shall ha..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13694:14604] score=9.305 "any of the foregoing, or any associated goodwill and that its rights thereunder are strictly limited..."
  - P@5=0.189 R@5=0.841 signal=0.3480525313845277
- **cuad-8de4da2e35**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65030:65961] score=12.215 "after the Term, do or knowingly suffer to be done any act or thing which will in any way impair the ..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54210:54954] score=10.103 "to obtain such assignments from the authors and creators of such materials as may be necessary to ve..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [62951:63887] score=9.919 "party with (i) copies of all written materials and (ii) written summaries of all oral advice, provid..."
  - P@5=0.186 R@5=0.898 signal=0.28726893053972197
- **cuad-af59222177**: Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [3851:4268] "In consideration of the remuneration to be paid to ABG pursuant hereto and subject to the conditions..."
  - got #1: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [27929:28889] score=11.131 "Shaq Rights and would therefore require the prior written consent of ABG in each instance.

9

Sourc..."
  - got #2: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [3228:4227] score=10.631 "bars, 'energy' frozen ice bars, and 'recovery' frozen ice bars), in each case produced and sold by P..."
  - got #3: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [30214:31140] score=9.068 "Effective Date for the First Contract Year, and March 1 for subsequent Contract Years;

(B) The seco..."
  - P@5=0.084 R@5=0.902 signal=0.3227351435407131

## partial_span (12)
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [12847:13843] score=17.538 "conditional upon ISA and Rubicon entering into the Share Subscription Agreement.





5. INTELLECTUA..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17604:18445] score=15.940 "the copyright and all other Intellectual Property rights inherent in or appurtenant to the foregoing..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13843:14604] score=11.845 " Rubicon shall not contest ownership by ISA of any of the foregoing. No right, license, release or o..."
  - P@5=0.047 R@5=0.112 signal=0.3184337883887126
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [843:1718] score=5.817 "is a single member LLC with Dr. Mitchell Felder as the sole member.   WHEREAS, Premier is publicly t..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [1718:2484] score=4.988 "   WHEREAS, Marv has filed US provisional patent applications specifically related to methods of tre..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [2484:3247] score=3.969 "   WHEREAS, Marv in this Agreement gives its written consent for Premier to assign its rights in the..."
  - P@5=0.100 R@5=0.216 signal=0.393208837275882
- **cuad-7c4a7a2903**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11296:11663] "Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amount of 5% of th..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12407:12824] "In addition to the 5% amount calculated pursuant to the preceding paragraph, there shall be an ident..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [21240:22239] score=4.401 "partners, employees, agents, servants, heirs, administrators, executors, successors, representatives..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [16613:17610] score=2.740 "such confidential information, for its or another's benefit, in any way acquired in the course of an..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4591:5453] score=2.589 "or leased), or (iii) a method or process involving the use of a Licensed Product to manufacture (inc..."
  - P@5=0.082 R@5=0.468 signal=0.32765590483966117
- **cuad-be7e4dcf80**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a non-compete clause in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47554:47970] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 17, then t..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47980:48417] "In the event this Agreement is terminated pursuant to the provisions of         paragraph 19.2, then..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [19399:20201] score=10.541 "The other Party shall be named as an                additional insured and the policy shall contain ..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [43683:44438] score=4.469 "prior written consent of the other Party and only in connection with the         services provided h..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [47033:47970] score=4.165 "or their products         or services, then the other Party may terminate this Agreement upon       ..."
  - P@5=0.107 R@5=0.488 signal=0.4021381055820755

## low_rank (18)
- **cuad-c007d50c97**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16945:17247] "To the extent that the Company IP does not vest automatically in the Company the Executive hereby as..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [1994:2875] score=11.616 "other way of representing or recording and recalling information which contains, reflects or is deri..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16162:16944] score=9.485 "or affairs of any Group Company or any Group Companies' current or former employees or directors to ..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2875:3732] score=9.032 "





whether registered or unregistered and including all applications (or rights to apply) for, an..."
  - P@5=0.074 R@5=1.000 signal=0.35478182403706277
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [20763:21517] score=10.376 "capacity, engage or have a financial interest in any ISA Competing Business, as defined  below, or p..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22237:23093] score=10.043 "Period")  and in the Rubicon  Geographic Area, as defined below, ISA agrees not to in any capacity, ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23093:23834] score=9.236 " ISA acknowledges, however, that the Parties have negotiated this Section and that the time limitati..."
  - P@5=0.057 R@5=1.000 signal=0.3576924792786762
- **cuad-cc1f3753ad**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any third-party beneficiaries designated in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41767:41984] "Except as set forth in Sections 10.3 and 10.4, nothing in this Agreement is intended to confer  bene..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [7526:8403] score=10.889 "which arise through customer marketing and distribution arrangements which are in place between Rubi..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41224:41984] score=9.469 "unless such waiver or excuse is in writing and signed by the Party  against whom enforcement of such..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41984:42747] score=9.325 " Without limiting the  generality of the foregoing, the clients, customers, shareholders or End User..."
  - P@5=0.054 R@5=1.000 signal=0.3498890296927811
- **cuad-92c250e51b**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the duration of any warranties provided in this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3021:3209] "FCC shall promptly, but in no event later than three (3) days after the date of such purchase order,..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13571:14420] score=3.510 "of the parties hereto pursuant to Sections 12, 13, 15, 16, 18, and 19 shall survive the Term.

19. W..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [12719:13571] score=3.230 "(a) Either Flotek or FCC may terminate the Term immediately, upon a written notice to the other such..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [10337:11166] score=1.853 "of appropriate environmental control equipment. FCC will supply Flotek with its Materials Safety Dat..."
  - P@5=0.044 R@5=1.000 signal=0.3471295888095751

## irrelevant_extra (31)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53606:54604] score=5.661 "any such holding company as defined by the Companies Act 2006 (as amended) and "Group Companies" wil..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [45210:46129] score=3.096 "remedies for past infringement and all materials embodying these rights to the fullest extent permit..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32559:33277] score=2.685 "to be provided to customers and potential customers of the Company and other non-public information ..."
  - P@5=0.071 R@5=1.000 signal=0.3090450982136398
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16203:17123] score=8.023 "Section 16. Each Party shall appoint one arbitrator who shall mutually appoint a third arbitrator wh..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2307:3174] score=7.605 "Arbitration............................................................................................"
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8594:9480] score=4.933 "writ, decree or contract known to GINARES, or an event that results in the creation of any lien, cha..."
  - P@5=0.061 R@5=1.000 signal=0.34094267315323074
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16976:17843] score=3.768 "of the State of Nevada (USA), and excluding any conflicts of law provisions which would require the ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [6242:7173] score=3.619 "obligations under this Agreement are to: (i) Keep HPIL ET aware of developments regarding GINARES; (..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [7875:8739] score=2.525 "of creditors' rights generally and (ii) as limited by laws relating to the availability of specific ..."
  - P@5=0.022 R@5=1.000 signal=0.3032800852290333
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [784:1696] score=8.075 "with respect to the Team, including at the football- based stadium in Jacksonville, Florida currentl..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4433:5133] score=7.034 "Sponsor shall deliver the food (the cost of which is included in the Annual Trade Value) to the Stad..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1696:2488] score=6.680 " Subject to the terms and conditions of this Agreement, as part of the consideration of the full and..."
  - P@5=0.088 R@5=1.000 signal=0.42419047137027216

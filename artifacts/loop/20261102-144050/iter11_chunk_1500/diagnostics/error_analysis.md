# Error analysis (iter11_chunk_1500, split=train, k=5)

Counts: chunk_boundary=13, correct_abstention=28, false_abstention=3, irrelevant_extra=4, low_rank=30, ok=2, partial_span=9, wrong_section=79

## false_abstention (3)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:1412] score=39.090 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56482:57041] score=33.851 "Control of BTL in any other way, including but not limited to by way of a merger.

19





THIS AGRE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [2393:3732] score=12.781 "devote the whole of your working time, skills, ability and attention to the business of the Company ..."
  - P@5=0.000 R@5=0.000 signal=0.27594692028363094
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:1412] score=37.695 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56482:57041] score=32.422 "Control of BTL in any other way, including but not limited to by way of a merger.

19





THIS AGRE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42337:43633] score=14.163 "at paragraph 13 above and this paragraph 14 to any employer or prospective employer or any other par..."
  - P@5=0.000 R@5=0.000 signal=0.2684616260050556
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168086:169497] score=25.656 "[***] that are [***] that is [***].

[***]: While Glumetza[***] have data that [***], where appropri..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [164444:165864] score=23.257 "omitted and have been filed separately with the Secretary of the Commission pursuant to the Company'..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:1338] score=22.275 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - P@5=0.000 R@5=0.000 signal=0.2688560082115764

## wrong_section (79)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:1412] score=41.062 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56482:57041] score=32.758 "Control of BTL in any other way, including but not limited to by way of a merger.

19





THIS AGRE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40116:41562] score=17.328 "the Termination Date carry on any trade or business whose name incorporates the word Bicycle or any ..."
  - P@5=0.000 R@5=0.000 signal=0.32862239032368123
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2591:3970] score=45.801 "7 18. Binding Effect..................................................................................."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:1497] score=42.079 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [18738:20008] score=33.206 "discussions, whether oral or written, of the Parties and there are no warranties, representations or..."
  - P@5=0.000 R@5=0.000 signal=0.3680498372777659
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2591:3970] score=45.801 "7 18. Binding Effect..................................................................................."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:1497] score=42.079 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [18738:20008] score=33.206 "discussions, whether oral or written, of the Parties and there are no warranties, representations or..."
  - P@5=0.000 R@5=0.000 signal=0.32205045881274685
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2591:3970] score=45.801 "7 18. Binding Effect..................................................................................."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:1497] score=42.079 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [18738:20008] score=33.206 "discussions, whether oral or written, of the Parties and there are no warranties, representations or..."
  - P@5=0.000 R@5=0.000 signal=0.35142512321589353

## chunk_boundary (13)
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [0:1455] score=39.373 "Exhibit 10.1   JACKSONVILLE JAGUARS SPONSORSHIP AGREEMENT   This Sponsorship Agreement (this "Agreem..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [6615:8050] score=35.348 "Sponsorship Agreement or Exhibit A, all Benefits granted by Club to Sponsor hereunder shall be subje..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [9118:10616] score=31.427 "IN WITNESS WHEREOF, each party has caused this Agreement to be executed in Jacksonville, Florida, by..."
  - P@5=0.019 R@5=0.391 signal=0.4550481037769986
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [6615:8050] score=37.634 "Sponsorship Agreement or Exhibit A, all Benefits granted by Club to Sponsor hereunder shall be subje..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [0:1455] score=36.956 "Exhibit 10.1   JACKSONVILLE JAGUARS SPONSORSHIP AGREEMENT   This Sponsorship Agreement (this "Agreem..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [9118:10616] score=30.449 "IN WITNESS WHEREOF, each party has caused this Agreement to be executed in Jacksonville, Florida, by..."
  - P@5=0.032 R@5=0.277 signal=0.4273340944747642
- **cuad-d0144819a9**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; Does this contract include any volume restrictions?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [958:1076] ""Maximum Quantity" means [***] pounds of Terpene Product per Year, prorated for any partial Year inc..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3210:3809] "FCC shall be obligated to accept all such purchase orders unless the amount ordered for a Year excee..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [0:1321] score=48.695 "Exhibit 10.1

Information identified with "[***]" has been excluded from this exhibit because it is ..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [18744:19355] score=37.598 "relating to the subject matter hereof and thereof and supersede all prior agreements and understandi..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [15509:16735] score=29.508 "thereof by United States first class, registered or certified mail, return receipt requested, with p..."
  - P@5=0.063 R@5=0.529 signal=0.41477317936999974
- **cuad-9d8033e4f6**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include an exclusivity agreement?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12938:13072] "If THI does not make the obligatory payments as stated in 2(b) by the dates stated, the Exclusive Li..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [14754:15163] "If THI does not make the obligatory payments as stated in 3(a) by the dates stated, the Exclusive Li..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [0:1486] score=60.939 "Exhibit 10.2   INTELLECTUAL PROPERTY AGREEMENT   This Intellectual Property Agreement (this "Agreeme..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [13840:15193] score=52.317 "Kingdom, by and at the direction of Mohammed Zulfiquar and/or Datatechnics Inc. as invoiced by Moham..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [22035:23282] score=39.171 "or other documents delivered pursuant hereto or in connection with the transactions contemplated her..."
  - P@5=0.102 R@5=0.360 signal=0.4282258553113916

## partial_span (9)
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:1167] score=42.686 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45244:46298] score=33.138 "consultations will be constrained by applicable requirements relating to  the disclosure of material..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [8575:10016] score=24.824 "and the progress expected to be made in the next succeeding period.     3.2 ISA may, at any time, re..."
  - P@5=0.084 R@5=0.583 signal=0.4458903990216801
- **cuad-5b2f8a1f44**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21193] "Further, during the Non-Competition Period, Rubicon shall not solicit any





employee of ISA or an..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:1167] score=40.233 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45244:46298] score=32.197 "consultations will be constrained by applicable requirements relating to  the disclosure of material..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22545:23834] score=27.568 "including  making available any information or funding to any such Rubicon Competing Business. Furth..."
  - P@5=0.020 R@5=0.500 signal=0.33323395041469683
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:1167] score=40.233 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [16848:18240] score=35.975 "applications, declarations, oaths, formal assignments, assignments of priority rights, and powers of..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45244:46298] score=32.197 "consultations will be constrained by applicable requirements relating to  the disclosure of material..."
  - P@5=0.032 R@5=0.112 signal=0.3264931368367961
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:1167] score=42.675 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45244:46298] score=32.197 "consultations will be constrained by applicable requirements relating to  the disclosure of material..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6310:7668] score=27.119 "and display the Rubicon Offerings and the Documentation. This license is granted to ISA  for the mar..."
  - P@5=0.085 R@5=0.582 signal=0.42942790334647474

## low_rank (30)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:1412] score=39.141 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56482:57041] score=32.422 "Control of BTL in any other way, including but not limited to by way of a merger.

19





THIS AGRE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [52876:54272] score=10.147 "Agreeing the terms of this Agreement will not constitute your giving consent to our processing of yo..."
  - P@5=0.048 R@5=1.000 signal=0.3391038000193986
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2591:3970] score=47.150 "7 18. Binding Effect..................................................................................."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:1497] score=42.079 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [18738:20008] score=34.354 "discussions, whether oral or written, of the Parties and there are no warranties, representations or..."
  - P@5=0.020 R@5=1.000 signal=0.38012034118020577
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:1417] score=47.285 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [32030:32861] score=44.993 "and any dispute or claim arising out of or in connection with it or its subject matter or formation ..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9176:10630] score=7.426 "Company shall be entitled to determine whether such targets have been met and where such targets hav..."
  - P@5=0.053 R@5=1.000 signal=0.43593639015028274
- **cuad-3ee0ba809a**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25311:25713] "During the term of employment and for one (1) year thereafter, the Executive will not directly or in..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:1417] score=48.370 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [32030:32861] score=44.993 "and any dispute or claim arising out of or in connection with it or its subject matter or formation ..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [24402:25717] score=14.910 "whatever media and wherever located) relating to the business or affairs of any Group Company or its..."
  - P@5=0.065 R@5=1.000 signal=0.3682081983017923

## irrelevant_extra (4)
- **cuad-eb7f865b0f**: Consider the Gas Franchise Agreement between the Town of Vinton and Roanoke Gas Company; What is the expiration date of this contract?
  - gold: `cuad/RgcResourcesInc_20151216_8-K_EX-10.3_9372751_EX-10.3_Franchise Agreement.txt` [1173:1257] "The term of the Franchise shall be twenty (20) years, commencing on January 1, 2016...."
  - got #1: `cuad/RgcResourcesInc_20151216_8-K_EX-10.3_9372751_EX-10.3_Franchise Agreement.txt` [0:1276] score=39.200 "Exhibit 10.3

GAS FRANCHISE AGREEMENT

THIS AGREEMENT ("Agreement"), made and entered into this 17th..."
  - got #2: `cuad/RgcResourcesInc_20151216_8-K_EX-10.3_9372751_EX-10.3_Franchise Agreement.txt` [3500:4971] score=38.651 "age, disability, or any other basis prohibited by state law relating to discrimination in employment..."
  - P@5=0.031 R@5=1.000 signal=0.43083181220535366
- **cuad-03f9d6dab2**: Consider the Gas Transportation Agreement between PennTex North Louisiana Operating, LLC and MRD Operating LLC; What is the expiration date of this contract?
  - gold: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [49279:49722] "This Agreement shall commence on the Effective Date and continue in full force and effect until the ..."
  - got #1: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [49030:50522] score=43.368 "number of counterparts, each of which shall be considered an original, and all of which shall be con..."
  - got #2: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [0:1108] score=41.946 "Exhibit 10.4

Execution Version

GAS TRANSPORTATION AGREEMENT

This Gas Transportation Agreement (th..."
  - got #3: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [2079:3573] score=38.488 "Agreement dated April 14, 2015 among PennTex North Louisiana, LLC, Customer, PennTex NLA Holdings, L..."
  - P@5=0.063 R@5=1.000 signal=0.44007992596219125
- **cuad-9c6ff300a3**: Consider the Gas Transportation Agreement between PennTex North Louisiana Operating, LLC and MRD Operating LLC; What is the notice period required to terminate the renewal?
  - gold: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [49279:49722] "This Agreement shall commence on the Effective Date and continue in full force and effect until the ..."
  - got #1: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [49030:50522] score=42.031 "number of counterparts, each of which shall be considered an original, and all of which shall be con..."
  - got #2: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [0:1108] score=40.730 "Exhibit 10.4

Execution Version

GAS TRANSPORTATION AGREEMENT

This Gas Transportation Agreement (th..."
  - got #3: `cuad/PenntexMidstreamPartnersLp_20150416_S-1A_EX-10.4_9042833_EX-10.4_Transportation Agreement.txt` [31365:32813] score=40.467 "in the oil and gas industry. Each invoice and statement shall be final as to both Parties unless que..."
  - P@5=0.064 R@5=1.000 signal=0.39141812010431287
- **cuad-591e829eea**: Consider the Joint Venture Agreement between MJ Syndicated, Inc. and Simply Herbals for Manufacturing and Selling Health-Related Products; What is the governing law for this contract?
  - gold: `cuad/MJBIOTECH,INC_12_06_2018-EX-99.01-JOINT VENTURE AGREEMENT.txt` [863:1007] "By this Agreement the Participants enter into a general Joint Venture (the "Joint Venture") in accor..."
  - got #1: `cuad/MJBIOTECH,INC_12_06_2018-EX-99.01-JOINT VENTURE AGREEMENT.txt` [0:1339] score=58.618 "Exhibit 99.01 JOINT VENTURE AGREEMENT THIS JOINT VENTURE AGREEMENT (the "Agreement") made and entere..."
  - got #2: `cuad/MJBIOTECH,INC_12_06_2018-EX-99.01-JOINT VENTURE AGREEMENT.txt` [22603:23582] score=43.121 "bind the parties.

This Agreement and the terms and conditions contained in this Agreement apply to ..."
  - got #3: `cuad/MJBIOTECH,INC_12_06_2018-EX-99.01-JOINT VENTURE AGREEMENT.txt` [6522:7838] score=25.142 "Joint Venture funds will be held in the name of the Joint Venture and will not be commingled with th..."
  - P@5=0.022 R@5=1.000 signal=0.4642152009983238

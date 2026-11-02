# Error analysis (iter11_abstain_on_doc_signal, split=train, k=5)

Counts: chunk_boundary=17, correct_abstention=22, failure_to_abstain=6, false_abstention=4, low_rank=27, ok=2, partial_span=5, wrong_section=85

## false_abstention (4)
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=47.514 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.023 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=35.547 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.030 R@5=1.000 signal=0.42494157504916047
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=45.928 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.023 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=34.054 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.000 R@5=0.000 signal=0.42494157504916047
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=45.928 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.023 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=34.054 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.000 R@5=0.000 signal=0.42494157504916047
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=45.928 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.023 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=34.054 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.000 R@5=0.000 signal=0.42494157504916047

## wrong_section (85)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=37.401 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=25.576 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [37964:38961] score=17.204 "stability of its or their workforce, that you will not during the Restricted Period (and in respect ..."
  - P@5=0.000 R@5=0.000 signal=0.5444497275765091
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=37.401 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=25.576 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1665:2618] score=17.514 "to have the right to work in the United Kingdom the Company may immediately terminate your employmen..."
  - P@5=0.000 R@5=0.000 signal=0.5444497275765091
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=37.401 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=25.576 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1665:2618] score=15.772 "to have the right to work in the United Kingdom the Company may immediately terminate your employmen..."
  - P@5=0.000 R@5=0.000 signal=0.5444497275765091
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:732] score=53.792 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [32102:32861] score=43.730 "subject matter or formation (including non-contractual disputes or claims) shall be governed by and ..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [10093:10975] score=8.687 "entitled to

5





payment of a bonus, or any pro rata portion of it, if the Executive leaves emplo..."
  - P@5=0.000 R@5=0.000 signal=0.5648301258441157

## chunk_boundary (17)
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [0:928] score=38.883 "Exhibit 10.1   JACKSONVILLE JAGUARS SPONSORSHIP AGREEMENT   This Sponsorship Agreement (this "Agreem..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [7274:8268] score=34.858 "to the parties at the following addresses (or at such other address as a party may specify by notice..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [8971:9843] score=33.569 "agreement. Delivery of an executed counterpart by electronic transmission shall have the same effect..."
  - P@5=0.025 R@5=0.341 signal=0.6110345924158768
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=43.595 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=31.109 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6784:7668] score=23.350 "Documentation to other  resellers, including, but not limited to, distributors, Original Equipment M..."
  - P@5=0.154 R@5=0.735 signal=0.6136295505946907
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=40.875 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [12847:13843] score=35.511 "conditional upon ISA and Rubicon entering into the Share Subscription Agreement.





5. INTELLECTUA..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17604:18445] score=30.703 "the copyright and all other Intellectual Property rights inherent in or appurtenant to the foregoing..."
  - P@5=0.166 R@5=0.429 signal=0.6136295505946907
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=40.875 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=29.999 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6784:7668] score=25.100 "Documentation to other  resellers, including, but not limited to, distributors, Original Equipment M..."
  - P@5=0.157 R@5=0.735 signal=0.6136295505946907

## partial_span (5)
- **cuad-5b2f8a1f44**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21193] "Further, during the Non-Competition Period, Rubicon shall not solicit any





employee of ISA or an..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=40.875 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=29.999 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14454:15442] score=26.196 "Rubicon acknowledges and agrees that those Works, as defined below,  shall belong exclusively to ISA..."
  - P@5=0.029 R@5=0.500 signal=0.6136295505946907
- **cuad-63b249d2e3**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What are the audit rights under this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5099:5340] "Flotek shall have the right at any time to (i) inspect the facility of FCC in Winter Haven, Florida ..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5342:5467] "Any such inspection or audit shall be upon reasonable notice and shall not unreasonably interfere wi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [0:956] score=44.084 "Exhibit 10.1

Information identified with "[***]" has been excluded from this exhibit because it is ..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [18962:19355] score=36.765 "5





IN WITNESS WHEREOF, the parties have executed this Agreement as of the date and year first se..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [4432:5341] score=34.320 "Year, FCC may ship to Flotek the remaining quantity of Terpene Product prior to the end of such Year..."
  - P@5=0.061 R@5=0.658 signal=0.6312910966991221
- **cuad-8de4da2e35**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168405:169356] score=25.940 "for which [***].

2. Point of Sale

[***]: Glumetza currently has [***]. We anticipate [***], which ..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65030:65961] score=23.985 "after the Term, do or knowingly suffer to be done any act or thing which will in any way impair the ..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:981] score=23.605 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - P@5=0.060 R@5=0.301 signal=0.547221022987388
- **cuad-22ec95e49b**: Consider the Co-Branding and Services Agreement between RSL COM PrimeCall, Inc. and deltathree.com, Inc.; Is there a cap on liability under this contract?
  - gold: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [15192:15684] "IN NO EVENT SHALL PRIMECALL BE LIABLE TO DELTATHREE FOR ANY SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DA..."
  - gold: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [16101:16592] "IN NO EVENT SHALL DELTATHREE BE LIABLE TO PRIMECALL FOR ANY SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DA..."
  - got #1: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [0:977] score=41.400 "Execution Copy

                       CO-BRANDING AND SERVICES AGREEMENT

         Co-Branding and ..."
  - got #2: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [27605:28526] score=30.217 "of convenience and for reference and in no way define, limit or describe the scope and intent of thi..."
  - got #3: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [14723:15684] score=26.986 "in full force and effect.

                                   ARTICLE VII  [Limited Warranty]

     ..."
  - P@5=0.107 R@5=0.501 signal=0.7630857252716308

## low_rank (27)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=39.092 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=25.576 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1665:2618] score=15.772 "to have the right to work in the United Kingdom the Company may immediately terminate your employmen..."
  - P@5=0.072 R@5=1.000 signal=0.5444497275765091
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [0:928] score=40.190 "Exhibit 10.1   JACKSONVILLE JAGUARS SPONSORSHIP AGREEMENT   This Sponsorship Agreement (this "Agreem..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [7274:8268] score=34.858 "to the parties at the following addresses (or at such other address as a party may specify by notice..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [8971:9843] score=32.177 "agreement. Delivery of an executed counterpart by electronic transmission shall have the same effect..."
  - P@5=0.167 R@5=1.000 signal=0.6110345924158768
- **cuad-3ee0ba809a**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25311:25713] "During the term of employment and for one (1) year thereafter, the Executive will not directly or in..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:732] score=54.954 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [32102:32861] score=43.730 "subject matter or formation (including non-contractual disputes or claims) shall be governed by and ..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25132:26059] score=15.789 "compliance with the obligations under clauses 20.1.1 and 20.1.2 together with such reasonable eviden..."
  - P@5=0.091 R@5=1.000 signal=0.5648301258441157
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [0:912] score=59.170 "QuickLinks -- Click here to rapidly navigate through this document

    EXHIBIT 10.1

Sponsorship Ag..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [8318:8852] score=48.063 "and regulations of all governmental agencies or commissions having jurisdiction  in matters covered ..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [1603:2302] score=26.209 "feet × 10 feet at each public  appearance made by Honey Hole, including four (4) "Kids Corner" child..."
  - P@5=0.027 R@5=1.000 signal=0.5593346845754873

## failure_to_abstain (6)
- **unans-025**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is Nigel Crockett's passport number and date of birth?
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=42.584 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=26.678 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1665:2618] score=16.349 "to have the right to work in the United Kingdom the Company may immediately terminate your employmen..."
- **unans-026**: Consider the Cooperation Agreement of HPIL Holding; What was HPIL Holding's closing share price on NASDAQ on the signing date?
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=22.435 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5449:6384] score=17.467 "to cooperate together to expand the GINARES projects and bind themselves to undertake this Agreement..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=17.195 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
- **unans-027**: Consider the Sponsorship Agreement of Vitamin Shoppe; What is the sponsored athlete's marathon personal-best time?
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [86542:87535] score=20.100 "Reach4life B-Vital                                      Realtime Chayas Chemical-Free               ..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [78084:79066] score=17.422 "WITH THE SECURITIES AND EXCHANGE COMMISSION.                                                      AS..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [61458:62320] score=15.538 "be executed in                           counterparts, each of which will serve to evidence         ..."
- **unans-028**: Consider the Transportation Services Agreement of Dynamex; What is the average fuel efficiency of the delivery trucks in miles per gallon?
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7952:8856] score=20.573 "delivery.

3.9    Dynamex agrees not to provide sameday delivery services for any other        provi..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [4549:5391] score=16.162 "Schedule "A" attached hereto, which                service standards may be amended from time to tim..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [0:970] score=13.522 "1                                                                     EXHIBIT 10.4

             MAR..."

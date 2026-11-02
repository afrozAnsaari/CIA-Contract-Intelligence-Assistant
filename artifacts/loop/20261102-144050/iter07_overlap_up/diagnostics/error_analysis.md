# Error analysis (iter07_overlap_up, split=train, k=5)

Counts: chunk_boundary=26, correct_abstention=28, false_abstention=3, low_rank=18, ok=1, partial_span=5, wrong_section=87

## false_abstention (3)
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=39.017 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56466:57041] score=34.141 "or

(d) obtains Control of BTL in any other way, including but not limited to by way of a merger.

1..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1117:2006] score=17.373 "or implied terms of any contract with, or other obligation to, any third party binding on you, inclu..."
  - P@5=0.000 R@5=0.000 signal=0.24570866783667103
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=39.017 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56466:57041] score=32.432 "or

(d) obtains Control of BTL in any other way, including but not limited to by way of a merger.

1..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1713:2618] score=16.179 "the Company may immediately terminate your employment without payment of compensation.

2. JOB TITLE..."
  - P@5=0.000 R@5=0.000 signal=0.25076048225821795
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168616:169497] score=26.660 "the [***] [***] — particularly in [***].

Depomed has [***] with the [***].

[***]: Glumetza[***]. T..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:981] score=23.803 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [94866:95865] score=20.796 "the 500mg formulation of the Product at King's Bristol facility that would result in a reduction in ..."
  - P@5=0.000 R@5=0.000 signal=0.2529500029060047

## wrong_section (87)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=39.017 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56466:57041] score=32.865 "or

(d) obtains Control of BTL in any other way, including but not limited to by way of a merger.

1..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1117:2006] score=17.456 "or implied terms of any contract with, or other obligation to, any third party binding on you, inclu..."
  - P@5=0.000 R@5=0.000 signal=0.28018380899628015
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=47.687 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.402 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19307:20008] score=37.179 "modification, waiver or termination is asserted. No waiver of any of the provisions of this Agreemen..."
  - P@5=0.000 R@5=0.000 signal=0.34950972076438885
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=46.082 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.402 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19307:20008] score=35.599 "modification, waiver or termination is asserted. No waiver of any of the provisions of this Agreemen..."
  - P@5=0.000 R@5=0.000 signal=0.3371424795748887
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=46.082 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=41.402 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19307:20008] score=35.599 "modification, waiver or termination is asserted. No waiver of any of the provisions of this Agreemen..."
  - P@5=0.000 R@5=0.000 signal=0.2970150348334493

## chunk_boundary (26)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=40.766 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56466:57041] score=32.432 "or

(d) obtains Control of BTL in any other way, including but not limited to by way of a merger.

1..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1713:2618] score=16.179 "the Company may immediately terminate your employment without payment of compensation.

2. JOB TITLE..."
  - P@5=0.069 R@5=0.929 signal=0.3159574889461242
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [0:928] score=39.587 "Exhibit 10.1   JACKSONVILLE JAGUARS SPONSORSHIP AGREEMENT   This Sponsorship Agreement (this "Agreem..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [7188:8050] score=34.471 "mailed by registered or certified mail, postage prepaid and return receipt requested, to the parties..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [9018:9843] score=32.459 "by electronic transmission shall have the same effect as delivery of an original ink counterpart.   ..."
  - P@5=0.066 R@5=0.369 signal=0.4079003970449948
- **cuad-5e23c5d8ad**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a covenant not to sue included in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [27816:28397] "If the Executive's employment is terminated at any time by reason of any reconstruction or amalgamat..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:732] score=53.634 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31950:32861] score=44.404 "not be enforceable by any person other than those parties. 24.11 This Agreement and any dispute or c..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [1821:2819] score=9.477 "or electronic form or on any magnetic or optical disk or memory and wherever located) including, wit..."
  - P@5=0.110 R@5=0.866 signal=0.4021620895514995
- **cuad-b5f75eaf50**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the notice period required to terminate the renewal?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18727:19214] "Unless terminated sooner, the term of this Agreement shall begin on the Effective Date and continue ..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=41.424 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45497:46298] score=31.636 "in one or more counterparts, each of which shall be  deemed an original and all of which together sh..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18145:19143] score=22.460 "granted in this  Agreement. ISA shall not contest ownership by Rubicon of any of the foregoing. No l..."
  - P@5=0.094 R@5=0.854 signal=0.3507328499253463

## partial_span (5)
- **cuad-aa326edf12**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a clause preventing the solicitation of customers in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7291:7515] "Except for the joint marketing efforts referred to in Section 3.1 (v)         above, Purolator agree..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7537:7727] "Except for the joint marketing efforts referred to in Section 3.1 (v)        above, Dynamex agrees n..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [0:970] score=57.278 "1                                                                     EXHIBIT 10.4

             MAR..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [48335:49218] score=41.303 "for a period of twelve (12)         months from the effective date of termination.

The Parties have..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7528:8527] score=37.110 "4 3.6    Except for the joint marketing efforts referred to in Section 3.1 (v)        above, Dynamex..."
  - P@5=0.042 R@5=0.459 signal=0.37733399653721844
- **cuad-31e7123c70**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; What licenses are granted under this contract?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [27994:28354] "During the Term, subject to the terms and conditions of this Agreement, Depomed hereby grants to Kin..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [53731:53951] "Depomed hereby grants to King the non-exclusive right, during the Term, to use the Launch Promotiona..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65962:66236] "Subject to this Section 4.8 and to applicable Legal Requirements, Depomed shall have the right to us..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [144427:144889] "Depomed agrees to grant and hereby grants to King an exclusive option (exercisable at King's sole di..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168616:169497] score=26.660 "the [***] [***] — particularly in [***].

Depomed has [***] with the [***].

[***]: Glumetza[***]. T..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:981] score=23.803 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [122675:123536] score=22.102 "enforcement of creditors' rights in general and to general principles of equity (regardless of wheth..."
  - P@5=0.229 R@5=0.452 signal=0.34810703150790756
- **cuad-8de4da2e35**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168616:169497] score=26.660 "the [***] [***] — particularly in [***].

Depomed has [***] with the [***].

[***]: Glumetza[***]. T..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65292:66236] score=24.313 "adverse to Depomed by virtue of the rights granted under this Agreement or through King's use of the..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:981] score=23.803 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - P@5=0.060 R@5=0.301 signal=0.2953820981909529
- **cuad-22ec95e49b**: Consider the Co-Branding and Services Agreement between RSL COM PrimeCall, Inc. and deltathree.com, Inc.; Is there a cap on liability under this contract?
  - gold: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [15192:15684] "IN NO EVENT SHALL PRIMECALL BE LIABLE TO DELTATHREE FOR ANY SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DA..."
  - gold: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [16101:16592] "IN NO EVENT SHALL DELTATHREE BE LIABLE TO PRIMECALL FOR ANY SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DA..."
  - got #1: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [0:977] score=41.442 "Execution Copy

                       CO-BRANDING AND SERVICES AGREEMENT

         Co-Branding and ..."
  - got #2: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [27774:28740] score=31.621 "[Third Parties]. Third Parties. There are no intended third party beneficiaries to this Agreement.

..."
  - got #3: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [1747:2636] score=30.414 "however, that PrimeCall may elect to terminate this Agreement, upon thirty (30) days' written notice..."
  - P@5=0.110 R@5=0.501 signal=0.4041647777537621

## low_rank (18)
- **cuad-3ee0ba809a**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25311:25713] "During the term of employment and for one (1) year thereafter, the Executive will not directly or in..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:732] score=56.347 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31950:32861] score=42.814 "not be enforceable by any person other than those parties. 24.11 This Agreement and any dispute or c..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [24981:25717] score=18.050 "Company; 20.1.3 provide such handover of their duties as the Company shall consider appropriate; and..."
  - P@5=0.103 R@5=1.000 signal=0.3853698828999655
- **cuad-c007d50c97**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16945:17247] "To the extent that the Company IP does not vest automatically in the Company the Executive hereby as..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:732] score=53.634 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31950:32861] score=42.814 "not be enforceable by any person other than those parties. 24.11 This Agreement and any dispute or c..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [1821:2819] score=11.040 "or electronic form or on any magnetic or optical disk or memory and wherever located) including, wit..."
  - P@5=0.068 R@5=1.000 signal=0.36225972050831945
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [0:912] score=59.461 "QuickLinks -- Click here to rapidly navigate through this document

    EXHIBIT 10.1

Sponsorship Ag..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [8521:8852] score=51.373 "day of December, 2007, in Fort Worth, Tarrant County, Texas, to be effective January 1, 2008.

3

  ..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [1196:2138] score=25.702 "per year;

2. Lead Sponsorship. The Company agrees that Cano shall be identified as the lead sponsor..."
  - P@5=0.028 R@5=1.000 signal=0.3922252742343041
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=41.424 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45497:46298] score=32.033 "in one or more counterparts, each of which shall be  deemed an original and all of which together sh..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22797:23797] score=26.965 "the foregoing restrictions are too broad or  otherwise unreasonable under applicable law, including ..."
  - P@5=0.046 R@5=1.000 signal=0.3496360265738108

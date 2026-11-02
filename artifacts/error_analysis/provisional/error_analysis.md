# Error analysis (provisional, split=train, k=5)

Counts: chunk_boundary=13, correct_abstention=28, false_abstention=5, irrelevant_extra=1, low_rank=13, partial_span=4, wrong_section=104

## false_abstention (5)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=38.429 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=25.026 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [11260:12156] score=22.937 "face-to-face sales presentation of the Product made by a Sales Representative to a Professional, inc..."
  - P@5=0.000 R@5=0.000 signal=0.20938520209867387
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=38.265 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=24.878 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/IGENEBIOTECHNOLOGYINC_05_13_2003-EX-1-JOINT VENTURE AGREEMENT.txt` [39389:40244] score=23.809 "shall be required to provide the services set forth in Article 11.1.4 for a period not to exceed 24 ..."
  - P@5=0.000 R@5=0.000 signal=0.19836921677372252
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=39.890 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [12847:13843] score=25.060 "conditional upon ISA and Rubicon entering into the Share Subscription Agreement.





5. INTELLECTUA..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=25.026 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - P@5=0.000 R@5=0.000 signal=0.2236889388569866
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:981] score=30.136 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168405:169356] score=24.306 "for which [***].

2. Point of Sale

[***]: Glumetza currently has [***]. We anticipate [***], which ..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [164520:165356] score=23.111 "pursuant to the Company's application requesting confidential treatment under Rule 24b-2 of the Secu..."
  - P@5=0.062 R@5=0.391 signal=0.20563377680041858

## wrong_section (104)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:964] score=39.756 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56771:57041] score=24.784 "Kevin Lee (Director) in the presence of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address..."
  - got #3: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [20683:21653] score=19.759 "under this Agreement, including but not limited to in connection with the sale, resale, import, expo..."
  - P@5=0.000 R@5=0.000 signal=0.24448066439672117
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=55.175 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=48.128 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=38.685 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.000 R@5=0.000 signal=0.30542601540067393
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=55.415 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=48.128 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=38.881 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.000 R@5=0.000 signal=0.28186154727032986
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=56.960 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=48.128 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=39.321 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.000 R@5=0.000 signal=0.3073688470860299

## chunk_boundary (13)
- **cuad-eb238d491d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Does this contract include an exclusivity agreement?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6079] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=56.348 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=30.251 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.txt` [20197:21196] score=27.055 "be amended from time to time, or to such statute's successor, and shall be deemed also to refer to a..."
  - P@5=0.063 R@5=0.318 signal=0.3474284424326055
- **cuad-72c36b3768**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=57.567 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=29.281 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5933:6932] score=26.712 "the Rubicon Offerings, the  Documentation and, subject to Section 2.2, any upgrades thereto, subject..."
  - P@5=0.114 R@5=0.581 signal=0.3293728353776375
- **cuad-d0144819a9**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; Does this contract include any volume restrictions?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [958:1076] ""Maximum Quantity" means [***] pounds of Terpene Product per Year, prorated for any partial Year inc..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3210:3809] "FCC shall be obligated to accept all such purchase orders unless the amount ordered for a Year excee..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [0:956] score=47.902 "Exhibit 10.1

Information identified with "[***]" has been excluded from this exhibit because it is ..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [18962:19355] score=41.623 "5





IN WITNESS WHEREOF, the parties have executed this Agreement as of the date and year first se..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3660:4582] score=25.658 "Flotek shall inform FCC within ten (10) days of such communication whether it will order such Terpen..."
  - P@5=0.037 R@5=0.208 signal=0.3092175715372061
- **cuad-ba8c34eccc**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; What licenses are granted under this contract?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3264:3378] "THI is granted the following rights to the Applications in Appendix A and the Licensed Products deri..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [3388:4736] "The licenses granted herein are exclusive worldwide licenses to:   1.         make, have made, use, ..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [4750:5144] "Licenses granted herein are solely for products in the form sold by the Licensee and are not to be c..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [5150:5453] "The grant of each license hereunder includes the right to grant sublicenses to Related Companies for..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [0:989] score=69.129 "Exhibit 10.2   INTELLECTUAL PROPERTY AGREEMENT   This Intellectual Property Agreement (this "Agreeme..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [13554:14553] score=46.108 "to THI  in total by no later than July 30, 2020.     The payment will be for development of laser te..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [22944:23282] score=44.087 "Biomedical, Inc.:     /s/ William Hartman                                Date__________ By: William ..."
  - P@5=0.036 R@5=0.069 signal=0.34260504646091333

## partial_span (4)
- **cuad-63b249d2e3**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What are the audit rights under this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5099:5340] "Flotek shall have the right at any time to (i) inspect the facility of FCC in Winter Haven, Florida ..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5342:5467] "Any such inspection or audit shall be upon reasonable notice and shall not unreasonably interfere wi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [0:956] score=48.679 "Exhibit 10.1

Information identified with "[***]" has been excluded from this exhibit because it is ..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [18962:19355] score=41.623 "5





IN WITNESS WHEREOF, the parties have executed this Agreement as of the date and year first se..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [4432:5341] score=28.013 "Year, FCC may ship to Flotek the remaining quantity of Terpene Product prior to the end of such Year..."
  - P@5=0.062 R@5=0.658 signal=0.3147323471223396
- **cuad-8de4da2e35**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [0:981] score=31.264 "Exhibit 10.1



PROMOTION AGREEMENT

by and between

DEPOMED, INC.

and

KING PHARMACEUTICALS, INC.
..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [168405:169356] score=27.051 "for which [***].

2. Point of Sale

[***]: Glumetza currently has [***]. We anticipate [***], which ..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [164520:165356] score=24.856 "pursuant to the Company's application requesting confidential treatment under Rule 24b-2 of the Secu..."
  - P@5=0.064 R@5=0.301 signal=0.24668863719477696
- **cuad-22ec95e49b**: Consider the Co-Branding and Services Agreement between RSL COM PrimeCall, Inc. and deltathree.com, Inc.; Is there a cap on liability under this contract?
  - gold: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [15192:15684] "IN NO EVENT SHALL PRIMECALL BE LIABLE TO DELTATHREE FOR ANY SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DA..."
  - gold: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [16101:16592] "IN NO EVENT SHALL DELTATHREE BE LIABLE TO PRIMECALL FOR ANY SPECIAL, INCIDENTIAL OR CONSEQUENTIAL DA..."
  - got #1: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [0:977] score=54.335 "Execution Copy

                       CO-BRANDING AND SERVICES AGREEMENT

         Co-Branding and ..."
  - got #2: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [2253:3152] score=32.235 "ARTICLE II  [Co-Branding of Calling Card and Joint Marketing]

                 Co-Branding of Calli..."
  - got #3: `cuad/DeltathreeInc_19991102_S-1A_EX-10.19_6227850_EX-10.19_Co-Branding Agreement_ Service Agreement.txt` [27605:28526] score=31.218 "of convenience and for reference and in no way define, limit or describe the scope and intent of thi..."
  - P@5=0.110 R@5=0.501 signal=0.3924002032377054
- **cuad-f718e4b4a2**: Consider the Non-Competition Agreement and Right of First Offer between Glamis Gold Ltd. and Western Copper Corporation; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [6475:8155] "Glamis covenants and agrees with Western Copper that if at any time it intends to dispose of a Desig..."
  - got #1: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [0:959] score=59.719 "NON COMPETITION AGREEMENT AND RIGHT OF FIRST OFFER

THIS AGREEMENT is dated May 3,2006.

BETWEEN:

G..."
  - got #2: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [5511:6469] score=53.467 "the names of Glamis and Western Copper will herein be deemed to  refer collectively to Glamis and al..."
  - got #3: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [15777:16402] score=37.836 "I62W.3





Termination

- 8 -

4.10 This Agreement may be terminated at any time by agreement in wr..."
  - P@5=0.206 R@5=0.501 signal=0.3379188670076479

## low_rank (13)
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3027:3970] score=57.004 "8 21. Early Termination................................................................................"
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:858] score=48.231 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19205:20008] score=40.357 "contained herein) unless in writing and signed by the Party against which such amendment, supplement..."
  - P@5=0.030 R@5=1.000 signal=0.3210800636854513
- **cuad-197aa5070a**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; What is the expiration date of this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [3546:3655] "The term of this Agreement shall be one (1) year, commencing January 1, 2008 and ending on December ..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [0:912] score=65.586 "QuickLinks -- Click here to rapidly navigate through this document

    EXHIBIT 10.1

Sponsorship Ag..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [8318:8852] score=52.558 "and regulations of all governmental agencies or commissions having jurisdiction  in matters covered ..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [1603:2302] score=24.034 "feet × 10 feet at each public  appearance made by Honey Hole, including four (4) "Kids Corner" child..."
  - P@5=0.027 R@5=1.000 signal=0.35862475705593055
- **cuad-1c1837f70a**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the renewal term for this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [18727:19214] "Unless terminated sooner, the term of this Agreement shall begin on the Effective Date and continue ..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=58.350 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=28.650 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.txt` [20197:21196] score=24.980 "be amended from time to time, or to such statute's successor, and shall be deemed also to refer to a..."
  - P@5=0.102 R@5=1.000 signal=0.36286062311674744
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:849] score=56.678 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45318:46298] score=28.815 "the disclosure of material information on the part of such party under applicable securities laws.  ..."
  - got #3: `cuad/SUCAMPOPHARMACEUTICALS,INC_11_04_2015-EX-10.2-STRATEGIC ALLIANCE AGREEMENT.txt` [20197:21196] score=25.206 "be amended from time to time, or to such statute's successor, and shall be deemed also to refer to a..."
  - P@5=0.046 R@5=1.000 signal=0.3156448087706891

## irrelevant_extra (1)
- **cuad-4dce24ac12**: Consider the Amendment No. 3 to Wireless Content License Agreement between Fox Mobile Entertainment, Inc. and Glu Mobile Inc.; What is the expiration date of this contract?
  - gold: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:989] "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #1: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [0:989] score=56.159 "AMENDMENT NO. 3

Dated as of February 19, 2007

Reference is hereby made to that certain fully execu..."
  - got #2: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1563:1902] score=50.176 "Glu Mobile Inc. ("Licensee")       Fox Mobile Entertainment, Inc. ("Fox")



By:   /s/ Albert A. Pim..."
  - got #3: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [18396:19306] score=16.144 "in accordance herewith.

    B.   ABW and PCQ acknowledge that they have read this Agreement, unders..."
  - P@5=0.099 R@5=1.000 signal=0.328248682745239

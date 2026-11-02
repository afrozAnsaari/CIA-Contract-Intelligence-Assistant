# Error analysis (iter05_chunk_500, split=train, k=5)

Counts: chunk_boundary=19, correct_abstention=28, false_abstention=10, low_rank=5, partial_span=12, wrong_section=94

## false_abstention (10)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:491] score=37.188 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56808:57041] score=26.174 "of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address:

20





Executed as a Deed by NIGE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38401:38901] score=18.267 "the Restricted Business to Restricted Customers or Prospective Customers;

(b) in the Restricted Ter..."
  - P@5=0.000 R@5=0.000 signal=0.23605261921257684
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:491] score=37.188 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56808:57041] score=26.174 "of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address:

20





Executed as a Deed by NIGE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [1531:2006] score=15.682 "of all relevant documents in this respect at the request of the Company. If at any time during the c..."
  - P@5=0.000 R@5=0.000 signal=0.20428786619687964
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:491] score=37.188 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56808:57041] score=26.174 "of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address:

20





Executed as a Deed by NIGE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [10341:10690] score=13.846 "you to perform your duties for which no further remuneration is payable.

7.2 By entering into this ..."
  - P@5=0.000 R@5=0.000 signal=0.21132303050374274
- **cuad-7c4a7a2903**: Consider the Intellectual Property Agreement for COVID-19 Treatment Development between Marv Enterprises, LLC, Premier Biomedical, Inc., and Technology Health, Inc.; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [11296:11663] "Royalty payments are payable from THI to Marv Enterprises, LLC and will be in the amount of 5% of th..."
  - gold: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [12407:12824] "In addition to the 5% amount calculated pursuant to the preceding paragraph, there shall be an ident..."
  - got #1: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [349:814] score=48.137 "(collectively referred to herein as the "Joint Venture") by and between:   Marv Enterprises, LLC, a ..."
  - got #2: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [13993:14493] score=47.964 "and at an hourly rate to Mohammed Zulfiquar and his designees.   (b).     Premier may partner with o..."
  - got #3: `cuad/PREMIERBIOMEDICALINC_05_14_2020-EX-10.2-INTELLECTUAL PROPERTY AGREEMENT.txt` [22895:23282] score=45.098 "upon the date first set forth above.     Premier Biomedical, Inc.:     /s/ William Hartman          ..."
  - P@5=0.000 R@5=0.000 signal=0.2248624237131048

## wrong_section (94)
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3317:3800] score=42.114 "8 23. Entire Agreement................................................................................."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:440] score=42.072 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19707:20008] score=35.443 ":   GINARES GROUP AG, a private company domiciled in Switzerland.       By: /s/  Peter Zu Sayn-Wittg..."
  - P@5=0.000 R@5=0.000 signal=0.2739152160186037
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:440] score=42.072 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3317:3800] score=40.171 "8 23. Entire Agreement................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19707:20008] score=35.443 ":   GINARES GROUP AG, a private company domiciled in Switzerland.       By: /s/  Peter Zu Sayn-Wittg..."
  - P@5=0.000 R@5=0.000 signal=0.27213308789671997
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:440] score=42.072 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3317:3800] score=40.171 "8 23. Entire Agreement................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19707:20008] score=35.443 ":   GINARES GROUP AG, a private company domiciled in Switzerland.       By: /s/  Peter Zu Sayn-Wittg..."
  - P@5=0.000 R@5=0.000 signal=0.24173888771155896
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [0:440] score=42.072 "COOPERATION AGREEMENT     made by and between     HPIL ENERGYTECH Inc.   and   GINARES GROUP AG     ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [3317:3800] score=40.171 "8 23. Entire Agreement................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [19707:20008] score=35.443 ":   GINARES GROUP AG, a private company domiciled in Switzerland.       By: /s/  Peter Zu Sayn-Wittg..."
  - P@5=0.000 R@5=0.000 signal=0.26327556676242353

## chunk_boundary (19)
- **cuad-4dce24ac12**: Consider the Amendment No. 3 to Wireless Content License Agreement between Fox Mobile Entertainment, Inc. and Glu Mobile Inc.; What is the expiration date of this contract?
  - gold: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:989] "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #1: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [0:447] score=58.944 "AMENDMENT NO. 3

Dated as of February 19, 2007

Reference is hereby made to that certain fully execu..."
  - got #2: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1563:1902] score=49.238 "Glu Mobile Inc. ("Licensee")       Fox Mobile Entertainment, Inc. ("Fox")



By:   /s/ Albert A. Pim..."
  - got #3: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [752:1230] score=10.820 "respect to each Property, including Robots, Kingdom of Heaven, Mr. and Mrs. Smith, In Her Shoes, Idi..."
  - P@5=0.188 R@5=0.606 signal=0.38492619643163856
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:491] score=39.460 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56808:57041] score=26.174 "of: /s/ Phil Jeffrey Witness Name: Phil Jeffrey Witness Address:

20





Executed as a Deed by NIGE..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [10341:10690] score=13.846 "you to perform your duties for which no further remuneration is payable.

7.2 By entering into this ..."
  - P@5=0.092 R@5=0.635 signal=0.27034206003323513
- **cuad-3ee0ba809a**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25311:25713] "During the term of employment and for one (1) year thereafter, the Executive will not directly or in..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:464] score=53.119 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [32551:32861] score=47.913 "for and on behalf of Theravance Biopharma UK Limited

/s/ Rick E Winningham

Signature Signed as a d..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25205:25702] score=11.273 "with such reasonable evidence of compliance as the Company may request. 21. Post Termination Restric..."
  - P@5=0.172 R@5=0.973 signal=0.3322886783784235
- **cuad-c007d50c97**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [16945:17247] "To the extent that the Company IP does not vest automatically in the Company the Executive hereby as..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [0:464] score=53.119 "Exhibit 10.2

STRICTLY PRIVATE AND CONFIDENTIAL

1 April, 2020

THERAVANCE BIOPHARMA UK LIMITED and ..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [32551:32861] score=47.913 "for and on behalf of Theravance Biopharma UK Limited

/s/ Rick E Winningham

Signature Signed as a d..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2353:2851] score=13.411 "Companies Act 2006) of the Company in any jurisdiction from time to time; "Intellectual Property Rig..."
  - P@5=0.086 R@5=0.642 signal=0.3269617082656829

## partial_span (12)
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [0:364] score=37.951 "Exhibit 10.1   JACKSONVILLE JAGUARS SPONSORSHIP AGREEMENT   This Sponsorship Agreement (this "Agreem..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [7353:7784] score=32.152 "may specify by notice to the other):   To Sponsor: The ARC Group, Inc.  To Club: Jacksonville Jaguar..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [8911:9409] score=29.358 "but all of which taken together shall constitute one single agreement. Delivery of an executed count..."
  - P@5=0.155 R@5=0.434 signal=0.34767795125350726
- **cuad-5b2f8a1f44**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21193] "Further, during the Non-Competition Period, Rubicon shall not solicit any





employee of ISA or an..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:440] score=38.630 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45712:46209] score=32.395 "hereof, individually or taken together, bear the signatures of both Parties hereto. For the purposes..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22302:22769] score=24.769 "ISA agrees not to in any capacity, engage or have a financial interest in any Rubicon Competing Busi..."
  - P@5=0.057 R@5=0.500 signal=0.25679956912560153
- **cuad-dd123231af**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What licenses are granted under this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:440] score=38.630 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45712:46209] score=32.395 "hereof, individually or taken together, bear the signatures of both Parties hereto. For the purposes..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13716:14127] score=26.906 "or any associated goodwill and that its rights thereunder are strictly limited to those specifically..."
  - P@5=0.112 R@5=0.264 signal=0.3126495279657882
- **cuad-72c36b3768**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:440] score=38.630 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45712:46209] score=32.395 "hereof, individually or taken together, bear the signatures of both Parties hereto. For the purposes..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6293:6783] score=29.182 "may use, perform and display the Rubicon Offerings and the Documentation. This license is granted to..."
  - P@5=0.275 R@5=0.682 signal=0.27665201684433754

## low_rank (5)
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [0:440] score=38.630 "Exhibit 10.1    STRATEGIC ALLIANCE AGREEMENT    This Strategic Alliance Agreement (this "Agreement")..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [45712:46209] score=32.395 "hereof, individually or taken together, bear the signatures of both Parties hereto. For the purposes..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23436:23834] score=23.111 "in the business of providing software development services for clients. "Rubicon Geographic Area" me..."
  - P@5=0.097 R@5=1.000 signal=0.2870049702139795
- **cuad-e9a04a00ab**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the expiration date of this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2050:2326] "The "Term" shall begin on the date hereof and shall expire December 31, 2023, subject to early termi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [0:465] score=41.649 "Exhibit 10.1

Information identified with "[***]" has been excluded from this exhibit because it is ..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [18893:19355] score=33.862 "to the subject matter hereof and thereof.

[Signature page follows]

5





IN WITNESS WHEREOF, the ..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3735:4187] score=27.963 "it will order such Terpene Product pursuant to the revised delivery terms.

(b) Shipments of Terpene..."
  - P@5=0.116 R@5=1.000 signal=0.31046148874804635
- **cuad-188e3e6478**: Consider the Co-Branding Agreement between PC Quote, Inc. and A.B. Watley, Inc. for Market Data Software; What licenses are granted under this contract?
  - gold: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [1881:2005] "PCQ agrees to allow ABW to co-brand the PCQ SOFTWARE in order to provide a value added service on AB..."
  - got #1: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [19186:19655] score=36.605 "Name:   Richard F. Chappeto Title:  Vice President Date:   10-11-96      ---------------------------..."
  - got #2: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [3349:3834] score=36.003 "the following disclaimer on the access page to the co-branded service:

         "PC Quote is not su..."
  - got #3: `cuad/PcquoteComInc_19990721_S-1A_EX-10.11_6377149_EX-10.11_Co-Branding Agreement1.txt` [892:1389] score=34.623 "said ABW and all of its subsidiaries and related companies.

Definitions:

SOFTWARE

PC QUOTE 6.0-TM..."
  - P@5=0.051 R@5=1.000 signal=0.273780318547351
- **cuad-c843372972**: Consider the Walabot HOME Reseller Agreement between Vayyar Imaging Ltd. and Inde Living Holdings, Inc.; What is the renewal term for this contract?
  - gold: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [13434:13592] "Thereafter, this Agreement shall automatically be renewed for successive 1-year terms (each a "Renew..."
  - got #1: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [0:428] score=57.190 "WALABOT-HOME RESELLER AGREEMENT This Walabot-HOME Reseller Agreement ("Agreement") is made and enter..."
  - got #2: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [21903:22288] score=42.340 "should be sent Supplier's Ordering Email address: logistics@walabot.com

Address for Notices to the ..."
  - got #3: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [21181:21653] score=22.633 "businesses or persons acting on behalf of any of the foregoing, that would constitute a violation of..."
  - P@5=0.073 R@5=1.000 signal=0.34619825155380013

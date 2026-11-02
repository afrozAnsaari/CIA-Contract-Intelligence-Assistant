# Error analysis (iter07_chunk_500, split=train, k=5)

Counts: chunk_boundary=33, correct_abstention=28, false_abstention=11, irrelevant_extra=13, low_rank=7, ok=7, partial_span=26, wrong_section=43

## false_abstention (11)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38401:38901] score=13.089 "the Restricted Business to Restricted Customers or Prospective Customers;

(b) in the Restricted Ter..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [40881:41378] score=12.987 "limited in a particular manner, then the restrictions set out in paragraph 14.2 above shall apply wi..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [36606:37029] score=6.543 "cancer that targets the same target as a drug conjugate compound in development by any Group Company..."
  - P@5=0.000 R@5=0.000 signal=0.23375909762222505
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32313:32705] score=6.964 "names, representatives, their needs or desires with respect to the types of products or services off..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42898:43396] score=6.765 "concepts, innovations, discoveries, developments and improvements, drug formulations, technology, ri..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [3413:3907] score=6.410 "of England daily spot exchange rate applicable on 1 January of each year. Your Salary will be review..."
  - P@5=0.000 R@5=0.000 signal=0.20515654960187651
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [42898:43396] score=10.355 "concepts, innovations, discoveries, developments and improvements, drug formulations, technology, ri..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [48391:48886] score=9.192 "Patents Act 1977 (as amended from time to time).

16 LITIGATION ASSISTANCE

During the term of your ..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44762:45258] score=6.996 "subsisting in any Works shall be the exclusive property of the Company.

15.5 To the extent that suc..."
  - P@5=0.177 R@5=0.805 signal=0.20992703829029485
- **cuad-28945a8ec1**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; Is there an anti-assignment clause in this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7079:7183] "This Agreement may not be assigned by either party without the prior written consent of the other pa..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [6855:7206] score=4.684 "while preparing for, filming or working on post  production of any episode.

17. Place of Performanc..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [4704:5153] score=4.298 "right or remedy authorized by law or this agreement.

13. Attorneys' Fees. If any legal action is br..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7559:8055] score=4.174 "or agreements, orally or otherwise, have  been made by any party, or anyone acting on behalf of any ..."
  - P@5=0.080 R@5=1.000 signal=0.22230661295474088

## wrong_section (43)
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9743:10164] score=3.070 "the consummation of the transactions contemplated by this Agreement.   8.3. Compliance With Other In..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8211:8700] score=2.912 "any federal, state or local governmental authority on the part of  GINARES  is required in connectio..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12489:12924] score=1.970 "instruments executed and delivered by GINARES on the Closing Date.   10.2. HPIL ET agrees that the s..."
  - P@5=0.000 R@5=0.000 signal=0.2854726032793446
- **cuad-e69f659dd1**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; What is the expiration date of this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [4382:4705] "The Executive's employment with the Company will commence on the Commencement Date and shall continu..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [9933:10433] score=3.143 "and not under notice, given or received on the date that the bonus is paid. Bonus entitlement does n..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31426:31833] score=3.103 "from the Company which is not expressly provided for by this Agreement. 24.9 This Agreement may be e..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25629:26059] score=3.004 "of the Company with respect to the bona fide hiring and firing of Company personnel. 22. Statutory P..."
  - P@5=0.000 R@5=0.000 signal=0.39572996811893013
- **cuad-51b4e44436**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [18678:18997] "The Company may, in its sole and absolute discretion, terminate the Executive's employment under thi..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [22117:22598] score=8.855 "outstanding. Any such suspension shall not constitute disciplinary action. During any period of susp..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [11457:11947] score=6.737 "the level of cover) at any time on reasonable notice to the Executive. 12. Holidays 12.1 The Executi..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3875:4358] score=4.818 "and shall not limit the sense of the words preceding those terms; 1.2.3 the headings are inserted fo..."
  - P@5=0.000 R@5=0.000 signal=0.36519361438578074
- **cuad-5e23c5d8ad**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a covenant not to sue included in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [27816:28397] "If the Executive's employment is terminated at any time by reason of any reconstruction or amalgamat..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [2353:2851] score=7.303 "Companies Act 2006) of the Company in any jurisdiction from time to time; "Intellectual Property Rig..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [31426:31833] score=3.103 "from the Company which is not expressly provided for by this Agreement. 24.9 This Agreement may be e..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [3499:3940] score=3.027 "caused, whether lawful or not, and "Termination Date" means the date of Termination. 1.2 In this Agr..."
  - P@5=0.000 R@5=0.000 signal=0.357488245863759

## chunk_boundary (33)
- **cuad-4dce24ac12**: Consider the Amendment No. 3 to Wireless Content License Agreement between Fox Mobile Entertainment, Inc. and Glu Mobile Inc.; What is the expiration date of this contract?
  - gold: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:989] "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #1: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [374:827] score=5.857 "Inc. ("Licensee").

The parties agree to modify the Agreement as follows:

1. EXTENSION OF TERM: The..."
  - got #2: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1563:1902] score=2.872 "Glu Mobile Inc. ("Licensee")       Fox Mobile Entertainment, Inc. ("Fox")



By:   /s/ Albert A. Pim..."
  - P@5=0.289 R@5=0.586 signal=0.378093098729304
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53649:54144] score=7.102 "Companies Act 2006 (as amended) and "Group Companies" will be interpreted accordingly.

21 ENTIRE AG..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [45183:45541] score=3.494 "the right to sue and claim remedies for past infringement and all materials embodying these rights t..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32313:32705] score=3.209 "names, representatives, their needs or desires with respect to the types of products or services off..."
  - P@5=0.086 R@5=0.635 signal=0.2695879454094961
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16606:17104] score=9.757 "Party or a portion of such costs as determined by the arbitrator. An award of the arbitrator shall b..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2449:2887] score=8.975 "7 17. Governing Law...................................................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [14810:15217] score=3.361 "or shall occur as a result of or in connection with this transaction.   6





    15. Compliance Wi..."
  - P@5=0.101 R@5=0.948 signal=0.2839686122656
- **cuad-9c581e5f19**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What is the expiration date of this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1322:1662] "The term of this Agreement (the "Term") shall commence as of April 1, 2018 (the "Effective Date") an..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1380:1875] score=9.436 "of April 1, 2018 (the "Effective Date") and shall expire upon the later of: (a) the conclusion of th..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [4509:4926] score=8.001 "Trade Value) to the Stadium at the time and location specified by Club. If any portion of the Annual..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [3421:3811] score=5.582 "Second Contract Year (2019/20):  $ 204,000  Third Contract Year (2020/21):  $ 208,080  Fourth Contra..."
  - P@5=0.126 R@5=0.829 signal=0.3948006083627608

## partial_span (26)
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17769:18151] score=3.222 "but all of which together shall constitute one and the same Agreement.   7





    20. No Reliance ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9743:10164] score=3.070 "the consummation of the transactions contemplated by this Agreement.   8.3. Compliance With Other In..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8211:8700] score=2.912 "any federal, state or local governmental authority on the part of  GINARES  is required in connectio..."
  - P@5=0.090 R@5=0.499 signal=0.2751289960806808
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1804:2216] score=6.578 "payment of the Sponsor Fees, Club hereby grants to Sponsor, and Sponsor hereby accepts, solely in th..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [3421:3811] score=5.582 "Second Contract Year (2019/20):  $ 204,000  Third Contract Year (2020/21):  $ 208,080  Fourth Contra..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [5287:5782] score=5.468 "conference championship, or Super Bowl (each, a "Playoff Game"), to the extent Club has the necessar..."
  - P@5=0.186 R@5=0.521 signal=0.37293958190005816
- **cuad-817f88727e**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; What licenses are granted under this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [38021:38280] "c)       Each party hereby grants to the other a                           non-exclusive, limited li..."
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [44306:44581] "g)       User Data will be owned by Client, and subject to the                           limitations..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [37653:38005] score=10.651 "the limited license granted to                           Excite hereunder.

              b)       E..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [44092:44581] score=7.265 "Agreement, even from individuals who are users of                           both parties' services, ..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [78702:79198] score=3.867 "in         IMPS                IMPS                                                                 ..."
  - P@5=0.152 R@5=0.515 signal=0.26465918045556436
- **cuad-d7d4d28180**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; Is there a cap on liability under this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [53891:54600] "EXCEPT UNDER SECTIONS 13(a) AND 13(b), IN NO EVENT WILL EITHER                  PARTY BE LIABLE TO T..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [53708:54186] score=6.504 "WITH THE SECURITIES AND EXCHANGE COMMISSION.                                                      AS..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [50763:51260] score=4.598 "in any ongoing liability to or                           prejudices or detrimentally impacts Excite ..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [52472:52969] score=4.598 "in any ongoing liability to or                           prejudices or detrimentally impacts Client ..."
  - P@5=0.120 R@5=0.416 signal=0.2560573228235186

## low_rank (7)
- **cuad-ca548f2c93**: Consider the Agency Agreement between General Electric Capital Corporation and Duckwall-Alco Stores, Inc. for Equipment Leasing; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [9172:9484] "So long as no default exists and is continuing hereunder or under the Lease, either party may termin..."
  - got #1: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [10980:11355] score=6.165 "should reference the appropriate Purchase Order/Sales Agreement Number.

General Electric Capital Co..."
  - got #2: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [9091:9484] score=4.619 "Date:  October 31, 2006

ARTICLE III TERMINATION

Section 3.01 Termination.

(a) So long as no defau..."
  - got #3: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [3401:3879] score=4.247 "in accordance with the Economic Terms (as hereafter defined and described).

Upon and as of the date..."
  - P@5=0.145 R@5=1.000 signal=0.3175579539599428
- **cuad-427f94f488**: Consider the Business Affiliate Agreement between Dr. George D. Green and UNION DENTAL CORP.; What is the expiration date of this contract?
  - gold: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [6029:6252] "This Agreement  shall become  effective on the Effective Date      and shall  continue in effect unt..."
  - got #1: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [0:466] score=2.746 "EXHIBIT 10.1

                          BUSINESS AFFILIATE AGREEMENT

This  Business  Affiliate  Agr..."
  - got #2: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [12807:13175] score=2.462 "Affiliate manual, the terms and conditions of which are hereby incorporated      into this agreement..."
  - got #3: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [5907:6279] score=2.151 "obligation  to  comply  fully  with  all provisions of this Agreement.

     5. Term and Termination..."
  - P@5=0.185 R@5=1.000 signal=0.3692433705090847
- **cuad-622128c2b4**: Consider the Walabot HOME Reseller Agreement between Vayyar Imaging Ltd. and Inde Living Holdings, Inc.; What is the expiration date of this contract?
  - gold: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [13297:13433] "This Agreement shall become effective on the Effective Date and shall remain in effect for an initia..."
  - got #1: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [12447:12862] score=3.173 "***; AND (ii) ***. THE FOREGOING EXCLUSIONS AND LIMITATIONS SHALL APPLY: (A) EVEN IF SUPPLIER HAS BE..."
  - got #2: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [13200:13592] score=2.034 "and/or relationship with any Customer and/or End User or other third party. Term and Termination Thi..."
  - got #3: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [15818:16290] score=1.950 "last Product in Reseller's inventory is sold to a Customer and/or End User, or (ii) 1 year from the ..."
  - P@5=0.060 R@5=1.000 signal=0.36662446884701544
- **cuad-43e73216bf**: Consider the Walabot HOME Reseller Agreement between Vayyar Imaging Ltd. and Inde Living Holdings, Inc.; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [15974:16290] "Supplier and/or Reseller may assign or novate this Agreement and the rights and obligations under it..."
  - got #1: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [20370:20831] score=9.248 "or by any independent contractors on its behalf or for its benefit, shall comply with the United Sta..."
  - got #2: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [15818:16290] score=4.442 "last Product in Reseller's inventory is sold to a Customer and/or End User, or (ii) 1 year from the ..."
  - got #3: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [13895:14321] score=3.266 "this Agreement forthwith upon the occurrence of any of the following: (i) the other Party is in mate..."
  - P@5=0.178 R@5=1.000 signal=0.3181236210218944

## irrelevant_extra (13)
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17034:17432] score=4.796 "of law provisions which would require the application of any law other than Nevada.   18. Binding Ef..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [6309:6727] score=4.529 "developments regarding GINARES; (ii) Work with HPIL ET as appropriate.   4. Confidentiality   Subjec..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9743:10164] score=3.070 "the consummation of the transactions contemplated by this Agreement.   8.3. Compliance With Other In..."
  - P@5=0.053 R@5=1.000 signal=0.25352723959037
- **cuad-4b9fe1892d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the governing law for this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36019:36116] "This Agreement shall be governed by and interpreted under the laws of the State of Florida, USA,...."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [35852:36348] score=8.959 "that the Parties would not have entered into this Agreement without such disclaimers and  limitation..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [44443:44933] score=6.918 "so long as such event  continues to prevent such performance, and provided the non-performing Party ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [8727:9184] score=4.908 "in the Contract Services by delivering a change order to  Rubicon. Upon receipt of a change order fr..."
  - P@5=0.042 R@5=1.000 signal=0.3518076228652276
- **cuad-cc1f3753ad**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any third-party beneficiaries designated in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41767:41984] "Except as set forth in Sections 10.3 and 10.4, nothing in this Agreement is intended to confer  bene..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [41692:42186] score=13.804 "the termination of this Agreement.     11.11 No Third Party Beneficiaries. Except as set forth in Se..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [7921:8403] score=7.298 "approval shall not be  unreasonably withheld.     3. RUBICON SERVICES.      3.1 Subject to the terms..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [8727:9184] score=6.645 "in the Contract Services by delivering a change order to  Rubicon. Upon receipt of a change order fr..."
  - P@5=0.091 R@5=1.000 signal=0.3019903924169803
- **cuad-939bacbae2**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the governing law for this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [17415:17518] "This Agreement shall be governed by and construed in accordance with the laws of the state of Delawa..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [17164:17521] score=9.757 "are descriptive only and shall have no legal force or effect whatsoever.

26. Gender. Whenever the c..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [11970:12319] score=3.550 "reasonable attorneys' and consultants' fees and expenses) of every kind, nature or description arisi..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13762:14220] score=3.238 "Flotek shall:

(i) conform to the specifications set forth in Section 1;

3





(ii) comply with al..."
  - P@5=0.048 R@5=1.000 signal=0.3085289736703102

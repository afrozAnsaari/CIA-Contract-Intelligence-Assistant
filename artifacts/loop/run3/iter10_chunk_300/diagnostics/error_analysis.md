# Error analysis (iter10_chunk_300, split=train, k=5)

Counts: chunk_boundary=13, correct_abstention=25, failure_to_abstain=3, false_abstention=6, irrelevant_extra=3, low_rank=7, ok=23, partial_span=32, wrong_section=56

## false_abstention (6)
- **cuad-5b2f8a1f44**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21193] "Further, during the Non-Competition Period, Rubicon shall not solicit any





employee of ISA or an..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21100:21399] score=10.552 "Period, Rubicon shall not solicit any





employee of ISA or any employee of any ISA Client. If a c..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22600:22896] score=10.407 "to any such Rubicon Competing Business. Further, during the Non-Competition Period, ISA shall not  s..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36493:36710] score=7.221 "dispute or claim concerning either clause 8  Confidentiality or clause 5 Intellectual Property may b..."
  - P@5=0.197 R@5=1.000 signal=0.17962758514338845
- **cuad-e568fcd380**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14401:14603] "As regards Intellectual Property created by Rubicon, Rubicon acknowledges and agrees that those Work..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [14605:15442] "Works means, collectively, any work product (of any type),  software, developments, processes, impro..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [15667:16433] "Rubicon shall make full and prompt disclosure to ISA of all Works as they are made (whether or not c..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [17709:18005] score=16.244 "and shall  be the sole property of Rubicon. ISA acknowledges that, except as otherwise set forth her..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13559:13843] score=16.134 "acquire any ownership interest in the Intellectual Property of ISA, or the Intellectual Property rig..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [13296:13559] score=13.972 "copyright and all other Intellectual Property rights inherent in or appurtenant to the foregoing  ar..."
  - P@5=0.000 R@5=0.000 signal=0.17497831596607122
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [89832:90112] score=10.159 "pricing established by the JCC in accordance with Section 3.3 hereof, (ii) the terms of such contrac..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [91002:91302] score=9.916 "and other arrangements described above. For purposes of clarity, all such contracts and arrangements..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [90309:90564] score=9.581 "of the Securities Exchange Act of 1934.

26







deductions from gross amounts invoiced pursuant t..."
  - P@5=0.000 R@5=0.000 signal=0.17042807083132838
- **cuad-c7ebebcdaa**: Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [6502:7242] "Except as otherwise provided herein, all the results of ABG's provision of CELEBRITY'S Services here..."
  - got #1: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [16176:16471] score=10.465 "and/or patents), whether by way of: (i) an application for and/or an opposition against any intellec..."
  - got #2: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [40865:41103] score=7.629 "distribution, delivery, advertisement, marketing, promotion, offering for sale, sale, or other explo..."
  - got #3: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [912:1204] score=7.250 "and has the authority to exploit such rights;

WHEREAS, PJMF is a corporation that pays for the nati..."
  - P@5=0.000 R@5=0.000 signal=0.1740433051372111

## wrong_section (56)
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [41271:41562] score=13.965 "and which is not competitive with the Restricted Business, nor from continuing to deal with any Pros..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38327:38624] score=13.742 "or provides Restricted Business or commercial activities competitive with the Restricted Business to..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [38624:38880] score=13.290 " company directly or indirectly by transacting business in competition with the Restricted Business ..."
  - P@5=0.000 R@5=0.000 signal=0.22034801006313678
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [32161:32460] score=9.435 "Company, including customer lists, client

10





lists, names, addresses (including email), teleph..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53054:53353] score=8.100 "from time to time.

19 THIRD PARTY RIGHTS

Save in respect of any rights conferred by this Agreement..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [36102:36401] score=7.952 "at the Termination Date negotiating with the Company or with any Group Company with a view to dealin..."
  - P@5=0.000 R@5=0.000 signal=0.19237338820465127
- **cuad-0b7b50dadf**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the expiration date of this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [5604:5739] "The term of this Agreement shall be one (1) year unless terminated earlier in accordance with the te..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8355:8653] score=3.241 "contemplated by this Agreement.   7.3. Compliance With Other Instruments   The execution, delivery a..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8653:8910] score=3.187 " results in the creation of any lien, charge or encumbrance upon the Agreement.   7.4. Litigation   ..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [9870:10164] score=3.135 "delivery and performance of this Agreement contemplated hereby will not result in a violation of, or..."
  - P@5=0.000 R@5=0.000 signal=0.26938708613418266
- **cuad-62566bdc83**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there a cap on liability under this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [11380:11583] "GINARES  agrees that the sole and exclusive remedy for money damages related to this Agreement and t..."
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [12564:12768] "HPIL ET agrees that the sole and exclusive remedy for money damages relating to this Agreement and t..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17801:18101] score=3.312 "constitute one and the same Agreement.   7





    20. No Reliance   No third party is entitled to ..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8355:8653] score=3.241 "contemplated by this Agreement.   7.3. Compliance With Other Instruments   The execution, delivery a..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [8653:8910] score=3.187 " results in the creation of any lien, charge or encumbrance upon the Agreement.   7.4. Litigation   ..."
  - P@5=0.000 R@5=0.000 signal=0.26015440718256805

## chunk_boundary (13)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53825:54114] score=8.398 "the parties and supersede any other agreement whether written or oral previously entered into.

22 J..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [45219:45518] score=3.827 "for past infringement and all materials embodying these rights to the fullest extent permitted by la..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56267:56563] score=3.535 "other similar law of another jurisdiction; or

(c) becomes bound or entitled under Sections 979 to 9..."
  - P@5=0.110 R@5=0.534 signal=0.24065992461853178
- **cuad-cc22d5d0ab**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; What is the governing law for this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16867:17117] "This Agreement and its application and interpretation will be governed exclusively by its terms and ..."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [16811:17109] score=11.041 "by any court having jurisdiction.   17. Governing Law   This Agreement and its application and inter..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2416:2716] score=10.233 "................................ 7 17. Governing Law..................................................."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [2116:2416] score=3.915 "Act And Export Control And Antiboycott Laws............................................................"
  - P@5=0.163 R@5=0.968 signal=0.2677836605341508
- **cuad-817f88727e**: Consider the Sponsorship Agreement between Excite, Inc. and Vitamin Shoppe Industries Inc. for Promotion on WebCrawler Channels; What licenses are granted under this contract?
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [38021:38280] "c)       Each party hereby grants to the other a                           non-exclusive, limited li..."
  - gold: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [44306:44581] "g)       User Data will be owned by Client, and subject to the                           limitations..."
  - got #1: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [37830:38129] score=10.825 "and to its trademarks, service marks and trade names                           worldwide, subject to..."
  - got #2: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [37552:37830] score=8.077 "and to its trademarks, service marks and trade names                           worldwide, subject to..."
  - got #3: `cuad/VITAMINSHOPPECOMINC_09_13_1999-EX-10.26-SPONSORSHIP AGREEMENT.txt` [44249:44527] score=7.928 "Data" for the purposes of this Agreement.

              g)       User Data will be owned by Client,..."
  - P@5=0.235 R@5=0.616 signal=0.21028125024945843
- **cuad-e9a04a00ab**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the expiration date of this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2050:2326] "The "Term" shall begin on the date hereof and shall expire December 31, 2023, subject to early termi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [1864:2156] score=5.989 "Agreement.

"Year" means a calendar year.

2. Purchase and Sale. Flotek will from time to time durin..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2979:3209] score=2.429 "in the form attached hereto as Exhibit A. FCC shall promptly, but in no event later than three (3) d..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [4143:4354] score=2.387 "and conditions attached hereto as Exhibit B.

(c) FCC shall invoice Flotek for Terpene Product at th..."
  - P@5=0.087 R@5=0.384 signal=0.30229128768654556

## partial_span (32)
- **cuad-4dce24ac12**: Consider the Amendment No. 3 to Wireless Content License Agreement between Fox Mobile Entertainment, Inc. and Glu Mobile Inc.; What is the expiration date of this contract?
  - gold: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:989] "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #1: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [426:722] score=6.584 "Agreement as follows:

1. EXTENSION OF TERM: The first paragraph of Section 4 of the Agreement is he..."
  - got #2: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1841:1902] score=3.990 "Date:         Date:

Source: GLU MOBILE INC, S-1/A, 3/19/2007..."
  - got #3: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [722:978] score=3.811 " provided, however, that with respect to each Property, including Robots, Kingdom of Heaven, Mr. and..."
  - P@5=0.332 R@5=0.972 signal=0.2749349107718941
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [47141:47367] score=8.357 "without the prior consent of the Company. You acknowledge that any unauthorised disclosure of such s..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44704:45002] score=7.770 "as the Company from time to time requests.

15.4 All IPRs subsisting in any Works shall be the exclu..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [48814:49114] score=7.764 "defending, maintaining and protecting such intellectual property) and in connection with litigation ..."
  - P@5=0.118 R@5=0.312 signal=0.19874729438452604
- **cuad-e651314c2d**: Consider the Sponsorship Agreement between Jacksonville Jaguars, LLC and The ARC Group, Inc.; What licenses are granted under this contract?
  - gold: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [1697:2488] "Subject to the terms and conditions of this Agreement, as part of the consideration of the full and ..."
  - got #1: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [2396:2686] score=7.024 "(collectively, the "Official Designations"), solely in connection with the Sponsor Business. No lice..."
  - got #2: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [5344:5622] score=6.582 "Game"), to the extent Club has the necessary rights to grant the Benefits identified on Exhibit A fo..."
  - got #3: `cuad/ArcGroupInc_20171211_8-K_EX-10.1_10976103_EX-10.1_Sponsorship Agreement.txt` [3410:3706] score=5.546 "$ 200,000  Second Contract Year (2019/20):  $ 204,000  Third Contract Year (2020/21):  $ 208,080  Fo..."
  - P@5=0.066 R@5=0.116 signal=0.34052034237685785
- **cuad-3ee0ba809a**: Consider the Service Agreement between Theravance Biopharma UK Limited and Brett Haumann; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25311:25713] "During the term of employment and for one (1) year thereafter, the Executive will not directly or in..."
  - got #1: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [25235:25535] score=9.071 "of compliance as the Company may request. 21. Post Termination Restrictions During the term of emplo..."
  - got #2: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [19567:19850] score=7.849 "has exercised its discretion in clause 17.1. 17.3 Notwithstanding clause 17.1, the Executive shall n..."
  - got #3: `cuad/THERAVANCEBIOPHARMA,INC_05_08_2020-EX-10.2-SERVICE AGREEMENT.txt` [19326:19567] score=6.563 "during the notice period referred to at clause 2 (or, if notice has already been given, during the r..."
  - P@5=0.169 R@5=0.557 signal=0.28828867153792753

## low_rank (7)
- **cuad-28945a8ec1**: Consider the Sponsorship Agreement between R. C. Boyd Enterprises, LLC and Cano Petroleum, Inc. for 'Honey Hole'; Is there an anti-assignment clause in this contract?
  - gold: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7079:7183] "This Agreement may not be assigned by either party without the prior written consent of the other pa..."
  - got #1: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [7635:7846] score=5.087 "acting on behalf of any party, that are

2







  not set forth in this contract, and that no agre..."
  - got #2: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [6460:6753] score=4.764 "of the Agreement, Cano shall remain liable for all unpaid installments for the then current term of ..."
  - got #3: `cuad/CANOPETROLEUM,INC_12_13_2007-EX-10.1-Sponsorship Agreement.txt` [6887:7183] score=4.710 "working on post  production of any episode.

17. Place of Performance. All sums payable under this A..."
  - P@5=0.078 R@5=1.000 signal=0.2012855385077865
- **cuad-af59222177**: Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [3851:4268] "In consideration of the remuneration to be paid to ABG pursuant hereto and subject to the conditions..."
  - got #1: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [27969:28263] score=10.547 "the prior written consent of ABG in each instance.

9

Source: PAPA JOHNS INTERNATIONAL INC, 8-K, 6/..."
  - got #2: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [3751:4050] score=10.537 "to ABG in connection with the same shall be negotiated in good faith.

3. Grant of Endorsement.

A. ..."
  - got #3: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [4050:4268] score=9.691 " non-sublicensable, indivisible right and license solely during the Term of the Agreement and within..."
  - P@5=0.297 R@5=1.000 signal=0.2043641791109286
- **cuad-ca548f2c93**: Consider the Agency Agreement between General Electric Capital Corporation and Duckwall-Alco Stores, Inc. for Equipment Leasing; Can this contract be terminated for convenience, and under what conditions?
  - gold: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [9172:9484] "So long as no default exists and is continuing hereunder or under the Lease, either party may termin..."
  - got #1: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [11192:11355] score=8.060 "a Schedule and a Certificate of Acceptance. The full terms and conditions of the lease contract are ..."
  - got #2: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [3776:4059] score=4.958 "to the Company pursuant to the terms and conditions of the Lease and the applicable completed Schedu..."
  - got #3: `cuad/ALCOSTORESINC_12_14_2005-EX-10.26-AGENCY AGREEMENT.txt` [9249:9484] score=4.747 "either party may terminate this Agreement at any time upon ____________ (______30________) days writ..."
  - P@5=0.262 R@5=1.000 signal=0.2656238798786322
- **cuad-427f94f488**: Consider the Business Affiliate Agreement between Dr. George D. Green and UNION DENTAL CORP.; What is the expiration date of this contract?
  - gold: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [6029:6252] "This Agreement  shall become  effective on the Effective Date      and shall  continue in effect unt..."
  - got #1: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [0:253] score=3.314 "EXHIBIT 10.1

                          BUSINESS AFFILIATE AGREEMENT

This  Business  Affiliate  Agr..."
  - got #2: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [13011:13227] score=3.157 "as of the date and year first above written.

                                 Business Affiliate

 ..."
  - got #3: `cuad/UnionDentalHoldingsInc_20050204_8-KA_EX-10_3345577_EX-10_Affiliate Agreement.txt` [12758:13011] score=2.346 "the terms and  conditions in UDC's Business      Affiliate manual, the terms and conditions of which..."
  - P@5=0.221 R@5=1.000 signal=0.34487798703225364

## irrelevant_extra (3)
- **cuad-b3466ca2cd**: Consider the Cooperation Agreement between HPIL ENERGYTECH Inc. and GINARES GROUP AG for Renewable Energy Projects; Is there an anti-assignment clause in this contract?
  - gold: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17341:17432] "The rights and obligations provided by this Agreement shall not be assignable by any Party...."
  - got #1: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17296:17591] score=4.877 "assigns, heirs and personal representatives. The rights and obligations provided by this Agreement s..."
  - got #2: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [6242:6540] score=4.468 "obligations under this Agreement are to: (i) Keep HPIL ET aware of developments regarding GINARES; (..."
  - got #3: `cuad/HPILHOLDING_01_07_2015-EX-99.1-COOPERATION AGREEMENT.txt` [17064:17296] score=3.662 "require the application of any law other than Nevada.   18. Binding Effect   All of the terms and pr..."
  - P@5=0.066 R@5=1.000 signal=0.24033528353031347
- **cuad-4b9fe1892d**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; What is the governing law for this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [36019:36116] "This Agreement shall be governed by and interpreted under the laws of the State of Florida, USA,...."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [35982:36282] score=10.124 "11.1 Governing Law and Jurisdiction. This Agreement shall be governed by and interpreted under the l..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [35802:35982] score=8.405 "element of this Agreement between the Parties and that the Parties would not have entered into this ..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [8849:9146] score=4.656 "notify ISA of any price revisions which are associated with the change order and  if ISA agree to th..."
  - P@5=0.074 R@5=1.000 signal=0.21252543266032448
- **cuad-939bacbae2**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the governing law for this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [17415:17518] "This Agreement shall be governed by and construed in accordance with the laws of the state of Delawa..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [17337:17564] score=10.906 "and the singular shall include the plural and conversely.

27. Governing Law. This Agreement shall b..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [12065:12319] score=4.068 "arising under common law or any applicable environmental law resulting from, arising out of or relat..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [13735:14033] score=3.783 "Product supplied by FCC to Flotek shall:

(i) conform to the specifications set forth in Section 1;
..."
  - P@5=0.079 R@5=1.000 signal=0.3001743611460907

## failure_to_abstain (3)
- **unans-025**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is Nigel Crockett's passport number and date of birth?
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56723:57007] score=25.266 "by BICYCLETX LIMITED acting by a director:

/s/ Kevin Lee (Director) in the presence of: /s/ Phil Je..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:258] score=19.490 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [462:687] score=17.792 "CB22 3AT, United Kingdom (the "Company"); and

(2) NIGEL CROCKETT of (the ''Employee").

IT IS AGREE..."
- **unans-029**: Consider the Endorsement Agreement of Holiday RV Superstores; What is the endorser's childhood hometown?
  - got #1: `cuad/HOLIDAYRVSUPERSTORESINC_04_15_2002-EX-10.13-ENDORSEMENT AGREEMENT.txt` [9265:9542] score=7.201 "pursuant to the terms of Section 3B. In the event of such withdrawal, the Company agrees forthwith t..."
  - got #2: `cuad/HOLIDAYRVSUPERSTORESINC_04_15_2002-EX-10.13-ENDORSEMENT AGREEMENT.txt` [4614:4865] score=6.943 "the Good Sam logo and name in any fashion.

        2. Endorsement. Subject to the Terms of Section ..."
  - got #3: `cuad/HOLIDAYRVSUPERSTORESINC_04_15_2002-EX-10.13-ENDORSEMENT AGREEMENT.txt` [931:1230] score=6.861 "vehicles with the Good Sam endorsement; and

               WHEREAS, the Company has raised capital ..."
- **unans-030**: Consider the Non-Competition Agreement of Western Copper; What is the current copper price on the London Metal Exchange?
  - got #1: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [5669:5961] score=8.476 "Copper  and all of its subsidiaries and other Affiliates, respectively.

PART 2

NON COMPETITION AND..."
  - got #2: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [441:739] score=8.402 "B.C. V6E 4M3

("Western Copper")

WHEREAS:

(A) Glamis, Western Copper and Western Silver Corporatio..."
  - got #3: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [9114:9348] score=7.912 "Western Copper's Remedies for Breach

3.2 Glamis acknowledges and agrees that a breach of its covena..."

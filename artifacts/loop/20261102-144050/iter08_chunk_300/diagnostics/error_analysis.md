# Error analysis (iter08_chunk_300, split=train, k=5)

Counts: chunk_boundary=6, correct_abstention=25, failure_to_abstain=3, false_abstention=1, low_rank=3, partial_span=16, wrong_section=114

## false_abstention (1)
- **cuad-4973cd8a76**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; Does this contract include any revenue or profit-sharing arrangements?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [98802:99086] "In consideration for King's performance of its obligations under this Agreement, Depomed shall pay p..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [105475:105918] "Following the termination of this Agreement at the conclusion of the initial five year term or any a..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [505:746] score=23.296 "by and between Depomed, Inc., a California corporation ("Depomed"), and King Pharmaceuticals, Inc., ..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [169196:169465] score=20.163 "Pharmaceuticals [***] to have [***] upon the [***]Glumetza.

[***]: We are preparing a Glumetza[***]..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [91002:91302] score=20.062 "and other arrangements described above. For purposes of clarity, all such contracts and arrangements..."
  - P@5=0.000 R@5=0.000 signal=0.17576219432747361

## wrong_section (114)
- **cuad-e5b265c6b3**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is the governing law for this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [53956:54252] "This Agreement shall be governed by and interpreted in accordance with the laws of England and Wales..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:258] score=36.206 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56723:57007] score=31.532 "by BICYCLETX LIMITED acting by a director:

/s/ Kevin Lee (Director) in the presence of: /s/ Phil Je..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [462:687] score=17.126 "CB22 3AT, United Kingdom (the "Company"); and

(2) NIGEL CROCKETT of (the ''Employee").

IT IS AGREE..."
  - P@5=0.000 R@5=0.000 signal=0.228830768988053
- **cuad-551a572623**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [33572:34034] "save that nothing in this paragraph 13.2 shall prevent you from holding (with the prior written cons..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:258] score=36.206 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56723:57007] score=31.532 "by BICYCLETX LIMITED acting by a director:

/s/ Kevin Lee (Director) in the presence of: /s/ Phil Je..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [41271:41562] score=19.018 "and which is not competitive with the Restricted Business, nor from continuing to deal with any Pros..."
  - P@5=0.000 R@5=0.000 signal=0.2120482726252483
- **cuad-2f7d42bc6c**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; Does this contract include any right of first refusal, right of first offer, or right of first negotiation?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6235:6531] "On or as soon as practicable following the Effective Date, it is intended that you will be granted a..."
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [6533:7937] "In addition, and conditional on completion of a transaction on terms set out below, you will be gran..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:258] score=36.206 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56723:57007] score=31.532 "by BICYCLETX LIMITED acting by a director:

/s/ Kevin Lee (Director) in the presence of: /s/ Phil Je..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [462:687] score=17.126 "CB22 3AT, United Kingdom (the "Company"); and

(2) NIGEL CROCKETT of (the ''Employee").

IT IS AGREE..."
  - P@5=0.000 R@5=0.000 signal=0.18174389575216057
- **cuad-7646cba011**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; How is intellectual property ownership assigned in this contract?
  - gold: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [44840:45359] "To the extent that such IPRs do not vest automatically in the Company by operation of law, you hereb..."
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:258] score=36.206 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56723:57007] score=31.532 "by BICYCLETX LIMITED acting by a director:

/s/ Kevin Lee (Director) in the presence of: /s/ Phil Je..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [462:687] score=17.126 "CB22 3AT, United Kingdom (the "Company"); and

(2) NIGEL CROCKETT of (the ''Employee").

IT IS AGREE..."
  - P@5=0.000 R@5=0.000 signal=0.19057110341950645

## chunk_boundary (6)
- **cuad-5b2f8a1f44**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Is there a clause preventing the solicitation of employees in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [21064:21193] "Further, during the Non-Competition Period, Rubicon shall not solicit any





employee of ISA or an..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22640:22769] "Further, during the Non-Competition Period, ISA shall not  solicit any employee of Rubicon or any em..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [46020:46298] score=33.331 "have executed this Agreement as of the date first  written above.     Information Systems Associates..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [259:547] score=25.279 "is 1151 Southwest 30th Street, Suite E, Palm City FL, 34990 ("ISA") and  Rubicon Software Group plc,..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22600:22896] score=22.845 "to any such Rubicon Competing Business. Further, during the Non-Competition Period, ISA shall not  s..."
  - P@5=0.152 R@5=0.860 signal=0.20229190767384128
- **cuad-e9a04a00ab**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What is the expiration date of this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [2050:2326] "The "Term" shall begin on the date hereof and shall expire December 31, 2023, subject to early termi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [176:465] score=44.539 "if publicly disclosed.

SUPPLY AGREEMENT

This Supply Agreement (the "Agreement") is entered into as..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [19064:19355] score=33.658 "forth above.

FLORIDA CHEMICAL COMPANY, LLC:

By: /s/ Elizabeth T. Wilkinson Name: Elizabeth T. Wilk..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [3916:4187] score=24.088 "of the date of the applicable purchase order. Delivery terms shall be FOB Winter Haven, Florida. Tra..."
  - P@5=0.074 R@5=0.384 signal=0.3033671546998351
- **cuad-63b249d2e3**: Consider the Supply Agreement between Florida Chemical Company, LLC and Flotek Chemistry, LLC for Terpene Products; What are the audit rights under this contract?
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5099:5340] "Flotek shall have the right at any time to (i) inspect the facility of FCC in Winter Haven, Florida ..."
  - gold: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [5342:5467] "Any such inspection or audit shall be upon reasonable notice and shall not unreasonably interfere wi..."
  - got #1: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [176:465] score=44.539 "if publicly disclosed.

SUPPLY AGREEMENT

This Supply Agreement (the "Agreement") is entered into as..."
  - got #2: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [19064:19355] score=33.658 "forth above.

FLORIDA CHEMICAL COMPANY, LLC:

By: /s/ Elizabeth T. Wilkinson Name: Elizabeth T. Wilk..."
  - got #3: `cuad/FLOTEKINDUSTRIESINCCN_05_09_2019-EX-10.1-SUPPLY AGREEMENT.txt` [4995:5287] score=31.358 "the Maximum Quantity shall be purchased by Flotek pursuant to this Agreement.

8. Inspection and Aud..."
  - P@5=0.131 R@5=0.514 signal=0.29786266612311274
- **cuad-aa326edf12**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Is there a clause preventing the solicitation of customers in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7291:7515] "Except for the joint marketing efforts referred to in Section 3.1 (v)         above, Purolator agree..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7537:7727] "Except for the joint marketing efforts referred to in Section 3.1 (v)        above, Dynamex agrees n..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [464:738] score=52.021 "PARCELWAY COURIER SYSTEMS CANADA LTD.                          a subsidiary of Dynamex Inc.         ..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [48597:48834] score=36.327 "PARCELWAY COURIER SYSTEMS CANADA LTD.

                             Per:  (ILLEGIBLE)  11/20/95     ..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [7472:7727] score=29.562 "from existing sameday customers of Dynamex.             4 3.6    Except for the joint marketing effo..."
  - P@5=0.180 R@5=0.563 signal=0.2803939272204843

## partial_span (16)
- **cuad-4dce24ac12**: Consider the Amendment No. 3 to Wireless Content License Agreement between Fox Mobile Entertainment, Inc. and Glu Mobile Inc.; What is the expiration date of this contract?
  - gold: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [598:989] "The rights granted hereunder shall be effective as of the Effective Date and shall expire on Decembe..."
  - got #1: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [0:288] score=47.338 "AMENDMENT NO. 3

Dated as of February 19, 2007

Reference is hereby made to that certain fully execu..."
  - got #2: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1378:1636] score=41.349 "and shall continue in full force and effect.

By signing in the places indicated below, the parties ..."
  - got #3: `cuad/GluMobileInc_20070319_S-1A_EX-10.09_436630_EX-10.09_Content License Agreement4.txt` [1841:1902] score=32.258 "Date:         Date:

Source: GLU MOBILE INC, S-1/A, 3/19/2007..."
  - P@5=0.150 R@5=0.460 signal=0.2843441393040446
- **cuad-72c36b3768**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are the licenses granted under this contract non-transferable?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [5690:6080] "Rubicon hereby grants to ISA during the Term (as defined below) and subject to the exclusions descri..."
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6537:7080] "Rubicon hereby grants to ISA during the Term and subject to the exclusions described in 2.4 below an..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [46020:46298] score=33.331 "have executed this Agreement as of the date first  written above.     Information Systems Associates..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [6487:6783] score=27.157 "to End Users for their internal use only.     2.2 Rubicon hereby grants to ISA during the Term and s..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [259:547] score=25.279 "is 1151 Southwest 30th Street, Suite E, Palm City FL, 34990 ("ISA") and  Rubicon Software Group plc,..."
  - P@5=0.318 R@5=0.495 signal=0.21773365858038188
- **cuad-e4aa9024a2**: Consider the Marketing and Transportation Services Agreement between Purolator Courier Ltd. and Parcelway Courier Systems Canada Ltd. (Dynamex Inc.); Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [8102:8548] "It is understood        and agreed that Dynamex, from time to time and upon request, may provide    ..."
  - gold: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [8558:8856] "Dynamex may continue to provide the same day service it currently        provides to Alltours custom..."
  - got #1: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [464:738] score=52.021 "PARCELWAY COURIER SYSTEMS CANADA LTD.                          a subsidiary of Dynamex Inc.         ..."
  - got #2: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [48597:48834] score=36.327 "PARCELWAY COURIER SYSTEMS CANADA LTD.

                             Per:  (ILLEGIBLE)  11/20/95     ..."
  - got #3: `cuad/DYNAMEXINC_06_06_1996-EX-10.4-TRANSPORTATION SERVICES AGREEMENT.txt` [5126:5391] score=26.041 "Dynamex agrees         to do the following:

     i)     Offer overnight courier services to its cus..."
  - P@5=0.088 R@5=0.159 signal=0.30665436810297614
- **cuad-31e7123c70**: Consider the Promotion Agreement between Depomed, Inc. and King Pharmaceuticals, Inc. for Glumetza; What licenses are granted under this contract?
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [27994:28354] "During the Term, subject to the terms and conditions of this Agreement, Depomed hereby grants to Kin..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [53731:53951] "Depomed hereby grants to King the non-exclusive right, during the Term, to use the Launch Promotiona..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [54352:54655] "Depomed shall, and does hereby, grant to King a royalty-free license to use and reproduce such mater..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [63634:63982] "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free righ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65589:65869] "King hereby grants to Depomed a non-assignable, non-sublicensable (except to any Third Party acting ..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [65962:66236] "Subject to this Section 4.8 and to applicable Legal Requirements, Depomed shall have the right to us..."
  - gold: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [144427:144889] "Depomed agrees to grant and hereby grants to King an exclusive option (exercisable at King's sole di..."
  - got #1: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [505:746] score=23.296 "by and between Depomed, Inc., a California corporation ("Depomed"), and King Pharmaceuticals, Inc., ..."
  - got #2: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [169196:169465] score=20.163 "Pharmaceuticals [***] to have [***] upon the [***]Glumetza.

[***]: We are preparing a Glumetza[***]..."
  - got #3: `cuad/KINGPHARMACEUTICALSINC_08_09_2006-EX-10.1-PROMOTION AGREEMENT.txt` [123190:123490] score=19.616 "property rights of any Third Party; provided, that Depomed makes no representation as to the King Tr..."
  - P@5=0.163 R@5=0.102 signal=0.2470061588162495

## low_rank (3)
- **cuad-5c06b5a634**: Consider the Strategic Alliance Agreement between Information System Associates, Inc. and Rubicon Software Group plc; Are there any exceptions to competitive restrictions in this contract?
  - gold: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [23556:23770] "In the event that ISA wishes to carry out any software development work of any nature during the Non..."
  - got #1: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [46020:46298] score=33.331 "have executed this Agreement as of the date first  written above.     Information Systems Associates..."
  - got #2: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [259:547] score=25.279 "is 1151 Southwest 30th Street, Suite E, Palm City FL, 34990 ("ISA") and  Rubicon Software Group plc,..."
  - got #3: `cuad/DUOSTECHNOLOGIESGROUP,INC_04_21_2009-EX-10.1-STRATEGIC ALLIANCE AGREEMENT.txt` [22600:22896] score=21.780 "to any such Rubicon Competing Business. Further, during the Non-Competition Period, ISA shall not  s..."
  - P@5=0.148 R@5=1.000 signal=0.22537039468608516
- **cuad-571490d88d**: Consider the Endorsement Agreement between ABG-Shaq, LLC and Papa John's International, Inc.; What is the governing law for this contract?
  - gold: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [63649:63806] "This Agreement shall be governed by and construed in accordance with the laws of the State of Delawa..."
  - got #1: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [67846:68130] score=28.763 "effective the date first above written.

Papa John's Marketing Fund, Inc. ABG-Shaq, LLC  Date: 6/6/1..."
  - got #2: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [12907:13207] score=25.366 "the submission shall be deemed disapproved. ABG shall have the right, but not the obligation, to inc..."
  - got #3: `cuad/PapaJohnsInternationalInc_20190617_8-K_EX-10.1_11707365_EX-10.1_Endorsement Agreement.txt` [63582:63864] score=24.426 "or amendment in writing, signed by all parties.

C. Governing Law. This Agreement shall be governed ..."
  - P@5=0.111 R@5=1.000 signal=0.23568251567557685
- **cuad-c843372972**: Consider the Walabot HOME Reseller Agreement between Vayyar Imaging Ltd. and Inde Living Holdings, Inc.; What is the renewal term for this contract?
  - gold: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [13434:13592] "Thereafter, this Agreement shall automatically be renewed for successive 1-year terms (each a "Renew..."
  - got #1: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [0:261] score=42.890 "WALABOT-HOME RESELLER AGREEMENT This Walabot-HOME Reseller Agreement ("Agreement") is made and enter..."
  - got #2: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [21929:22223] score=41.866 "Ordering Email address: logistics@walabot.com

Address for Notices to the Supplier Vayyar Ltd. 3 Avr..."
  - got #3: `cuad/HealthcareIntegratedTechnologiesInc_20190812_8-K_EX-10.1_11776966_EX-10.1_Reseller Agreement.txt` [21267:21560] score=23.980 "a violation of any law, rule, or regulation. IN WITNESS WHEREOF, the Parties have executed this Agre..."
  - P@5=0.116 R@5=1.000 signal=0.23938544407713677

## failure_to_abstain (3)
- **unans-025**: Consider the Service Agreement between BicycleTX Ltd and Nigel Crockett for Chief Business Officer Position; What is Nigel Crockett's passport number and date of birth?
  - got #1: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [0:258] score=38.751 "Exhibit 10.11

DATED 26 September 2019

BicycleTX Ltd

and

Nigel Crockett

________________________..."
  - got #2: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [56723:57007] score=33.606 "by BICYCLETX LIMITED acting by a director:

/s/ Kevin Lee (Director) in the presence of: /s/ Phil Je..."
  - got #3: `cuad/BICYCLETHERAPEUTICSPLC_03_10_2020-EX-10.11-SERVICE AGREEMENT.txt` [462:687] score=19.509 "CB22 3AT, United Kingdom (the "Company"); and

(2) NIGEL CROCKETT of (the ''Employee").

IT IS AGREE..."
- **unans-029**: Consider the Endorsement Agreement of Holiday RV Superstores; What is the endorser's childhood hometown?
  - got #1: `cuad/HOLIDAYRVSUPERSTORESINC_04_15_2002-EX-10.13-ENDORSEMENT AGREEMENT.txt` [13796:14089] score=24.302 "the day and year first above written.

Affinity Group, Inc.

By:  /s/ Paul E. Schedler     ---------..."
  - got #2: `cuad/HOLIDAYRVSUPERSTORESINC_04_15_2002-EX-10.13-ENDORSEMENT AGREEMENT.txt` [0:292] score=24.071 "EXHIBIT 10.13

                             ENDORSEMENT AGREEMENT

               This Agreement is ..."
  - got #3: `cuad/HOLIDAYRVSUPERSTORESINC_04_15_2002-EX-10.13-ENDORSEMENT AGREEMENT.txt` [9265:9542] score=4.653 "pursuant to the terms of Section 3B. In the event of such withdrawal, the Company agrees forthwith t..."
- **unans-030**: Consider the Non-Competition Agreement of Western Copper; What is the current copper price on the London Metal Exchange?
  - got #1: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [5669:5961] score=27.374 "Copper  and all of its subsidiaries and other Affiliates, respectively.

PART 2

NON COMPETITION AND..."
  - got #2: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [6376:6675] score=25.195 "on or is engaged in Mining Activities,

in the Area of Non-Competition.

Right of First Offer

2.2 G..."
  - got #3: `cuad/WESTERN COPPER - NON-COMPETITION AGREEMENT.txt` [441:739] score=23.764 "B.C. V6E 4M3

("Western Copper")

WHEREAS:

(A) Glamis, Western Copper and Western Silver Corporatio..."

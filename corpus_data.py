"""
Official Corpus Data Source for IP-SAKTI Sahayak
Contains Tier 1 statutory acts, rules, guidelines, case law, international treaties, and TK demonstration corpus.
Every chunk strictly tagged with Level A/B/C/D authority metadata.
"""

CORPUS_DOCUMENTS = [
    # ----------------------------------------------------
    # 1. THE PATENTS ACT, 1970 & 2024 RULES (India - Level A)
    # ----------------------------------------------------
    {
        "document_id": "PAT_ACT_SEC3P",
        "act": "The Patents Act, 1970",
        "section": "Section 3(p)",
        "domain": "Patent",
        "jurisdiction": "India",
        "source_type": "official_law",
        "authority_level": "A",
        "authority": "Government of India / CGPDTM",
        "topic": "Traditional Knowledge Patent Bar",
        "source_url": "file:///official_corpus/patents_act_1970.pdf#Section3p",
        "header": "Section 3(p) — Inventions Relating to Traditional Knowledge Excluded from Patentability",
        "text": """Section 3(p) of The Patents Act, 1970 specifies that an invention which, in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not an invention within the meaning of this Act. 
        Traditional knowledge, whether codified in classical Ayurvedic texts (such as Ayurvedic Pharmacopoeia of India, Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya) or orally transmitted, cannot be claimed as a patentable technical invention. 
        Aggregation of known traditional herbs without proven synergistic technical effect beyond additive individual properties fails statutory patentability criteria."""
    },
    {
        "document_id": "PAT_MANUAL_CHAP8",
        "act": "Manual of Patent Office Practice and Procedure",
        "section": "Chapter 08.03.02",
        "domain": "Patent",
        "jurisdiction": "India",
        "source_type": "official_guideline",
        "authority_level": "B",
        "authority": "CGPDTM / Patent Office India",
        "topic": "Section 3(p) Examination Guidelines",
        "source_url": "file:///official_corpus/patent_office_manual.pdf#Chap08",
        "header": "Chapter 08.03.02 — Examination Practice for Traditional Knowledge and Biological Inventions",
        "text": """Examiners shall consult available traditional knowledge databases and literature to evaluate Section 3(p) objections. 
        Where a claimed product formulation contains known traditional herbs (e.g., Ashwagandha, Haridra, Tulsi, Neem) used for traditionally documented therapeutic indications, the examiner shall raise an objection under Section 3(p). 
        To overcome Section 3(p), the applicant must demonstrate a novel technical intervention, such as a novel non-obvious extraction process, a novel standardized fraction, or experimental evidence establishing unexpected synergistic technical interaction beyond simple admixture."""
    },
    {
        "document_id": "PAT_RULES_2024",
        "act": "The Patent Rules, 2003 (Amended 2024)",
        "section": "Rule 13(d) & Form 1",
        "domain": "Patent",
        "jurisdiction": "India",
        "source_type": "official_law",
        "authority_level": "A",
        "authority": "Government of India",
        "topic": "Biological Material & Source Disclosure",
        "source_url": "file:///official_corpus/patent_rules_2024.pdf#Rule13d",
        "header": "Rule 13(d) — Declaration of Source and Geographical Origin of Biological Material",
        "text": """If the specification mentions biological material used in an invention, the applicant shall disclose the source and geographical origin of such biological material in India. 
        Where the biological resource is obtained from India, mandatory approval from the National Biodiversity Authority (NBA) under Section 6 of the Biological Diversity Act, 2002 must be submitted prior to the grant of the patent."""
    },

    # ----------------------------------------------------
    # 2. DRUGS AND COSMETICS ACT, 1940 & RULES, 1945 (India - Level A)
    # ----------------------------------------------------
    {
        "document_id": "DC_ACT_SEC3A",
        "act": "Drugs and Cosmetics Act, 1940",
        "section": "Section 3(a)",
        "domain": "Regulatory",
        "jurisdiction": "India",
        "source_type": "official_law",
        "authority_level": "A",
        "authority": "CDSCO / Ministry of Ayush",
        "topic": "Ayurvedic, Siddha or Unani (ASU) Drug Definition",
        "source_url": "file:///official_corpus/dc_act_1940.pdf#Section3a",
        "header": "Section 3(a) — Definition of Ayurvedic, Siddha or Unani (ASU) Drugs",
        "text": """Ayurvedic, Siddha or Unani (ASU) drug includes all medicines intended for internal or external use for or in the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, and manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurvedic, Siddha and Unani medicine systems specified in the First Schedule."""
    },
    {
        "document_id": "DC_RULES_RULE158B",
        "act": "Drugs and Cosmetics Rules, 1945",
        "section": "Rule 158B",
        "domain": "Regulatory",
        "jurisdiction": "India",
        "source_type": "official_law",
        "authority_level": "A",
        "authority": "Ministry of Ayush / State Licensing Authority",
        "topic": "Licensing Requirements for Patent or Proprietary ASU Medicines",
        "source_url": "file:///official_corpus/dc_rules_1945.pdf#Rule158B",
        "header": "Rule 158B — Licensing Criteria for Patent or Proprietary Ayurvedic Medicines",
        "text": """For the grant of a license to manufacture Patent or Proprietary Ayurvedic, Siddha or Unani drugs:
        (1) Classical Medicine: Manufactured strictly according to First Schedule texts using ingredients specified therein.
        (2) Patent or Proprietary Medicine: Formulations containing ingredients mentioned in First Schedule texts but prepared in non-classical ratios, novel dosage forms (capsules, syrups, extracts), or novel combinations. Proof of safety and efficacy via textual rationale, safety study, or clinical pilot trial data as specified in Schedule IV is required."""
    },

    # ----------------------------------------------------
    # 3. BIOLOGICAL DIVERSITY ACT, 2002 (AMENDED 2023) & ABS (India - Level A)
    # ----------------------------------------------------
    {
        "document_id": "BD_ACT_SEC6",
        "act": "Biological Diversity Act, 2002 (Amended 2023)",
        "section": "Section 6",
        "domain": "ABS",
        "jurisdiction": "India",
        "source_type": "official_law",
        "authority_level": "A",
        "authority": "National Biodiversity Authority (NBA)",
        "topic": "Access and Benefit Sharing (ABS) for IP Protection",
        "source_url": "file:///official_corpus/biological_diversity_act_2023.pdf#Section6",
        "header": "Section 6 — Application for Intellectual Property Rights for Inventions Based on Biological Resources",
        "text": """No person shall apply for any intellectual property right, in or outside India, for any invention based on any research or information on a biological resource obtained from India, without obtaining prior approval of the National Biodiversity Authority (NBA). 
        The 2023 Amendment streamlines benefit sharing for registered AYUSH practitioners and domestic traditional knowledge holders while maintaining mandatory reporting for commercial utilization and international IP filings."""
    },

    # ----------------------------------------------------
    # 4. FSSAI AYURVEDA-AAHAR REGULATIONS, 2022 (India - Level A)
    # ----------------------------------------------------
    {
        "document_id": "FSSAI_AYU_AAHAR",
        "act": "FSSAI Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
        "section": "Regulation 3 & Schedule A",
        "domain": "Food / Dietary",
        "jurisdiction": "India",
        "source_type": "official_law",
        "authority_level": "A",
        "authority": "Food Safety and Standards Authority of India (FSSAI)",
        "topic": "Ayurveda Aahara Regulatory Classification",
        "source_url": "file:///official_corpus/fssai_ayurveda_aahara_2022.pdf#Reg3",
        "header": "Regulation 3 — Definition and General Requirements for Ayurveda Aahara",
        "text": """Ayurveda Aahara means food prepared in accordance with the recipes or ingredients or processes described in the authoritative books of Ayurveda listed in Schedule A. 
        It shall not include Ayurvedic drugs, synthetic APIs, or parenteral products. 
        Products positioned as Ayurveda Aahara shall not carry therapeutic or disease-curing claims; only general health maintenance or dietary wellness claims permitted under FSSAI regulations are authorized."""
    },

    # ----------------------------------------------------
    # 5. INTERNATIONAL TREATIES: WIPO GRATK & TRIPS (International - Level A)
    # ----------------------------------------------------
    {
        "document_id": "WIPO_GRATK_ART3",
        "act": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024)",
        "section": "Article 3",
        "domain": "Patent",
        "jurisdiction": "International",
        "source_type": "official_treaty",
        "authority_level": "A",
        "authority": "World Intellectual Property Organization (WIPO)",
        "topic": "Mandatory Disclosure of Origin for Traditional Knowledge",
        "source_url": "file:///official_corpus/wipo_gratk_treaty_2024.pdf#Article3",
        "header": "Article 3 — Mandatory Disclosure Requirement for Genetic Resources and Associated TK",
        "text": """Where a claimed invention in a patent application is materially/directly based on genetic resources or associated traditional knowledge, each Contracting Party shall require applicants to disclose:
        (a) The country of origin of the genetic resources; and/or
        (b) The indigenous community or traditional source providing the associated traditional knowledge.
        Failure to comply triggers administrative review and mandatory correction protocols prior to grant across international patent offices."""
    },
    {
        "document_id": "TRIPS_ART27",
        "act": "WTO TRIPS Agreement",
        "section": "Article 27",
        "domain": "Patent",
        "jurisdiction": "International",
        "source_type": "official_treaty",
        "authority_level": "A",
        "authority": "World Trade Organization (WTO)",
        "topic": "Patentable Subject Matter and Exclusions",
        "source_url": "file:///official_corpus/trips_agreement.pdf#Article27",
        "header": "Article 27 — Patentable Subject Matter",
        "text": """Patents shall be available for any inventions, whether products or processes, in all fields of technology, provided that they are new, involve an inventive step and are capable of industrial application. 
        Members may exclude from patentability inventions the prevention within their territory of the commercial exploitation of which is necessary to protect ordre public or morality, including to protect human, animal or plant life or health."""
    },

    # ----------------------------------------------------
    # 6. TRADITIONAL KNOWLEDGE DEMONSTRATION CORPUS (Level B / C)
    # ----------------------------------------------------
    {
        "document_id": "TK_API_ASHWAGANDHA",
        "act": "Ayurvedic Pharmacopoeia of India (API)",
        "section": "Part I, Vol I, Monograph 12 (Ashwagandha)",
        "domain": "Traditional Knowledge",
        "jurisdiction": "India",
        "source_type": "official_pharmacopoeia",
        "authority_level": "B",
        "authority": "Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIMH)",
        "topic": "Ashwagandha (Withania somnifera) Monograph",
        "source_url": "file:///official_corpus/api_vol1.pdf#Ashwagandha",
        "header": "Monograph 12 — Ashwagandha (Withania somnifera Dunal. Root)",
        "text": """Ashwagandha consists of dried mature roots of Withania somnifera Dunal. (Family Solanaceae). 
        Traditional Therapeutic Uses: Balya (tonifying/strengthening), Rasayana (rejuvenative), Vata-vyadhi hara (pacifying Vata nervous disorders), Kshayahara (anti-wasting), Unmada-hara (alleviating mental stress/anxiety). 
        Classical Dosage Form: Churna (3-6g), Kwatha (decoction), Ghrita. 
        Status: Codified Traditional Knowledge Demonstration Corpus item."""
    },
    {
        "document_id": "TK_API_HARIDRA",
        "act": "Ayurvedic Pharmacopoeia of India (API)",
        "section": "Part I, Vol I, Monograph 24 (Haridra/Turmeric)",
        "domain": "Traditional Knowledge",
        "jurisdiction": "India",
        "source_type": "official_pharmacopoeia",
        "authority_level": "B",
        "authority": "PCIMH",
        "topic": "Haridra / Turmeric (Curcuma longa) Monograph",
        "source_url": "file:///official_corpus/api_vol1.pdf#Haridra",
        "header": "Monograph 24 — Haridra (Curcuma longa L. Rhizome)",
        "text": """Haridra consists of dried rhizomes of Curcuma longa L. (Family Zingiberaceae). 
        Traditional Therapeutic Uses: Vrana-ropana (wound healing), Kustha-hara (skin disorders), Sotha-hara (anti-inflammatory), Mehahara (anti-diabetic). 
        Classical Dosage Form: Churna, Svarasa, Taila. 
        Status: Codified Traditional Knowledge Demonstration Corpus item. (Historic prior-art precedent: US Patent 5,401,504 for turmeric wound healing was revoked based on API & traditional Indian texts)."""
    },

    # ----------------------------------------------------
    # 7. LANDMARK CASE LAW (India - Level C)
    # ----------------------------------------------------
    {
        "document_id": "CASE_TURMERIC_REVOCATION",
        "act": "Landmark IP Revocation Precedent",
        "section": "USPTO Re-examination No. 90/004,390 (Turmeric Patent Revocation)",
        "domain": "Patent / TK",
        "jurisdiction": "India",
        "source_type": "case_law",
        "authority_level": "C",
        "authority": "US Patent Office Re-examination / CSIR India",
        "topic": "Turmeric Patent Revocation Prior-Art Precedent",
        "source_url": "file:///official_corpus/turmeric_case_1997.pdf",
        "header": "CSIR vs USPTO — Re-examination of US Patent 5,401,504 (Use of Turmeric in Wound Healing)",
        "text": """In 1997, the Council of Scientific & Industrial Research (CSIR), India, successfully challenged US Patent 5,401,504 granted for the use of turmeric in wound healing. 
        CSIR produced ancient Sanskrit texts, Ayurvedic Pharmacopoeia citations, and published Indian medical papers establishing that turmeric rhizome paste for wound healing was public domain Traditional Knowledge in India. 
        The US Patent Office cancelled all 6 claims for lack of novelty under prior art, establishing a landmark international precedent for defensive TK protection."""
    }
]

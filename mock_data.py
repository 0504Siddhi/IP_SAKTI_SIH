"""
Mock data module for IP-SAKTI Sahayak (Step 0 UI Scaffold)
Strictly adheres to Section 6 JSON Output Contract:
{
  "module": "string",
  "status": "🔴 Evidence Found | 🟡 Requires Review | 🔵 No Direct Match in Searched Corpus",
  "evidence": "string",
  "citation": { "document": "string", "section": "string", "source_url": "string", "exact_text": "string" },
  "jurisdiction": "India | International",
  "sufficiency": "HIGH | MEDIUM | LOW"
}
"""

MOCK_EXTRACTED_INTAKE = {
    "product_name": "Ashwagandha Stress Relief Capsules",
    "main_ingredient": "Ashwagandha",
    "scientific_name": "Withania somnifera",
    "plant_part": "Root",
    "product_form": "Capsule",
    "intended_purpose": "Stress & anxiety support",
    "route_of_use": "Oral",
    "target_user": "General adults",
    "recipe_origin": "Modified formulation (Extract 10:1)",
    "manufacturing_process": "Hydro-alcoholic solvent extraction",
    "missing_fields": ["Manufacturing process details"]
}

MOCK_CLASSIFICATION_RESULT = {
    "category": "Patent / Proprietary Ayurvedic Medicine",
    "confidence": "MEDIUM",
    "reasons": [
        "Uses known traditional botanical ingredient (Ashwagandha / Withania somnifera)",
        "Not an exact match to an unchanged classical text formulation (uses 10:1 extract in capsule form)",
        "Therapeutic / wellness claim detected for stress support"
    ],
    "disclaimer": "This is a preliminary classification generated for decision-support only and must be verified against applicable official regulations."
}

MOCK_SECTION_3P_INDIA = {
    "module": "section_3p",
    "status": "🔴 Evidence Found",
    "evidence": "The core ingredient (Ashwagandha / Withania somnifera) for stress and nervous system support is extensively documented in classical Ayurvedic texts including Ayurvedic Pharmacopoeia of India (API Part I, Vol 1). Section 3(p) excludes inventions that duplicate or aggregate known properties of traditionally known components.",
    "citation": {
        "document": "The Patents Act, 1970",
        "section": "Section 3(p)",
        "source_url": "file:///official_corpus/patents_act_1970.pdf#Section3p",
        "exact_text": "An invention which, in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable."
    },
    "jurisdiction": "India",
    "sufficiency": "HIGH",
    "recommended_action": "The Traditional Knowledge Demonstration Corpus confirms traditional documentation. Innovators should consider non-patent commercialization or defensive publication."
}

MOCK_SECTION_3P_INTERNATIONAL = {
    "module": "international_gratk",
    "status": "🟡 Requires Review",
    "evidence": "Under WIPO GRATK Treaty (2024) Article 3 and Nagoya Protocol, patent applications claiming inventions based on traditional knowledge or biological resources require mandatory disclosure of origin and evidence of prior informed consent.",
    "citation": {
        "document": "WIPO Treaty on IP, Genetic Resources and Associated Traditional Knowledge (2024)",
        "section": "Article 3 (Mandatory Disclosure Requirement)",
        "source_url": "file:///official_corpus/wipo_gratk_2024.pdf#Article3",
        "exact_text": "Each Contracting Party shall require applicants to disclose the country of origin of genetic resources and/or the indigenous community providing traditional knowledge associated with genetic resources."
    },
    "jurisdiction": "International",
    "sufficiency": "HIGH",
    "recommended_action": "Review international PCT and export market disclosure requirements before filing abroad."
}

MOCK_GAP_NAVIGATOR_ITEMS = [
    {
        "module": "gap_navigator_item",
        "feature_name": "Ashwagandha root ingredient",
        "status": "🔴 Evidence Found",
        "evidence": "Documented in Ayurvedic Pharmacopoeia of India (API) Vol 1, p. 15 for Vata-hara and Rasayana properties.",
        "citation": {
            "document": "Ayurvedic Pharmacopoeia of India",
            "section": "Part I, Vol I, Monograph 12",
            "source_url": "file:///official_corpus/api_vol1.pdf#Mono12",
            "exact_text": "Withania somnifera Dunal. (Root) is indicated for Balya, Rasayana, and Vata-vyadhi management."
        },
        "jurisdiction": "India",
        "sufficiency": "HIGH"
    },
    {
        "module": "gap_navigator_item",
        "feature_name": "Stress & anxiety support claim",
        "status": "🟡 Requires Review",
        "evidence": "Traditional texts document general vitality and nervous system support; modern therapeutic anxiety claims require clinical safety and regulatory review under Drugs & Cosmetics Rules.",
        "citation": {
            "document": "Drugs and Cosmetics Rules, 1945",
            "section": "Rule 158B (Ayurvedic Patent/Proprietary Licensing)",
            "source_url": "file:///official_corpus/dc_rules_1945.pdf#Rule158B",
            "exact_text": "For proof of effectiveness of Patent or Proprietary ASU drugs, textual rationale or pilot clinical trial data as specified in Schedule IV is required."
        },
        "jurisdiction": "India",
        "sufficiency": "MEDIUM"
    },
    {
        "module": "gap_navigator_item",
        "feature_name": "Hydro-alcoholic 10:1 ratio process",
        "status": "🔵 No Direct Match in Searched Corpus",
        "evidence": "No direct textual match for hydro-alcoholic extract ratio 10:1 found in the searched traditional Ayurvedic corpus.",
        "citation": {
            "document": "Manual of Patent Office Practice and Procedure",
            "section": "Chapter 08.03.02 (Section 3(p) Examination)",
            "source_url": "file:///official_corpus/patent_office_manual.pdf#Chap08",
            "exact_text": "Extraction procedures isolating known active principles using standard solvent techniques require evaluation for technical contribution beyond routine laboratory practice."
        },
        "jurisdiction": "India",
        "sufficiency": "MEDIUM"
    }
]

MOCK_IP_MAP = [
    {
        "ip_type": "Patent",
        "status": "🟡 Requires Review",
        "description": "Section 3(p) Traditional Knowledge concern flagged. Only eligible if distinct technical process or non-obvious synergy is proven."
    },
    {
        "ip_type": "Trademark",
        "status": "🟢 Recommended",
        "description": "Recommended for protecting product and brand name (e.g., 'AshwaCalm'). Prevents commercial brand infringement."
    },
    {
        "ip_type": "Design",
        "status": "🟡 Requires Review",
        "description": "May apply to novel, non-functional visual bottle or packaging design elements."
    },
    {
        "ip_type": "Trade Secret",
        "status": "🟡 Requires Review",
        "description": "May protect confidential manufacturing know-how, extraction parameters, or proprietary ratios."
    }
]

MOCK_ABS_DATA = {
    "module": "abs_compliance",
    "status": "🔴 Evidence Found",
    "evidence": "Biological resources (Withania somnifera) sourced from India trigger National Biodiversity Authority (NBA) approval requirements under Biological Diversity Act, 2002 (amended 2023).",
    "citation": {
        "document": "Biological Diversity Act, 2002 (Amended 2023)",
        "section": "Section 3 & Section 6",
        "source_url": "file:///official_corpus/biological_diversity_act_2023.pdf#Section6",
        "exact_text": "Any person obtaining Indian biological resources for commercial utilization or IP protection must comply with access and benefit sharing (ABS) regulations."
    },
    "jurisdiction": "India",
    "sufficiency": "HIGH"
}

MOCK_ABSTENTION_CASE = {
    "module": "safe_abstention",
    "status": "🔵 No Direct Match in Searched Corpus",
    "evidence": "We couldn't find sufficient grounded evidence in our currently available official sources to provide a reliable answer for this query.",
    "citation": {
        "document": "IP-SAKTI Knowledge Base",
        "section": "Safe Abstention Protocol",
        "source_url": "file:///official_corpus/abstention_policy.pdf",
        "exact_text": "When search results fail to meet the minimum threshold of official statutory support, the assistant must safely abstain from outputting speculative advice."
    },
    "jurisdiction": "India",
    "sufficiency": "LOW",
    "user_options": [
        "Try rephrasing your query using common or botanical ingredient names",
        "Provide specific dosage form and administration route details",
        "Consult an official regulatory authority or registered IP practitioner"
    ]
}

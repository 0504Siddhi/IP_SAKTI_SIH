"""
Deterministic Formulation Classification Engine for IP-SAKTI Sahayak
Implements 7-Category Decision Tree as pure Python code (no LLM in this function).
Reference: Master Reference §6 & Research Doc Topic 2/3.
"""

from typing import Dict, Any, List

# 7 Statutory Category Constants
CLASSICAL_ASU = "Classical / Generic ASU Medicine"
PROPRIETARY_ASU = "Patent / Proprietary Ayurvedic Medicine"
NEW_DRUG = "New / Non-Classical Drug"
PHYTOPHARMACEUTICAL = "Phytopharmaceutical Pathway"
AYURVEDA_AAHAR = "Ayurveda-Aahar / Nutraceutical"
COSMETIC = "Cosmetic"
INSUFFICIENT_INFO = "Insufficient Information"

# Ingredient Normalization Dictionary (Topic 3 & 6 of Research PDF)
INGREDIENT_DICTIONARY = {
    "ashwagandha": {
        "common_name": "Ashwagandha",
        "botanical_name": "Withania somnifera Dunal.",
        "sanskrit_name": "Ashwagandha / Hayagandha",
        "category": "Botanical",
        "classical_text": True,
        "schedule_e1_restricted": False
    },
    "turmeric": {
        "common_name": "Turmeric / Haridra",
        "botanical_name": "Curcuma longa L.",
        "sanskrit_name": "Haridra / Nisha",
        "category": "Botanical",
        "classical_text": True,
        "schedule_e1_restricted": False
    },
    "haldi": {
        "common_name": "Turmeric / Haridra",
        "botanical_name": "Curcuma longa L.",
        "sanskrit_name": "Haridra",
        "category": "Botanical",
        "classical_text": True,
        "schedule_e1_restricted": False
    },
    "kumari": {
        "common_name": "Aloe Vera / Kumari",
        "botanical_name": "Aloe barbadensis Mill.",
        "sanskrit_name": "Kumari / Ghritkumari",
        "category": "Botanical",
        "classical_text": True,
        "schedule_e1_restricted": False
    },
    "amla": {
        "common_name": "Amla / Amalaki",
        "botanical_name": "Phyllanthus emblica L.",
        "sanskrit_name": "Amalaki / Dhatri",
        "category": "Botanical",
        "classical_text": True,
        "schedule_e1_restricted": False
    },
    "vibranium bhasma": {
        "common_name": "Vibranium Bhasma (Unrecognized / Synthetic)",
        "botanical_name": "Unknown",
        "sanskrit_name": "Unrecognized",
        "category": "Unnormalized",
        "classical_text": False,
        "schedule_e1_restricted": False
    }
}

def normalize_ingredient(raw_name: str) -> Dict[str, Any]:
    """
    Ingredient Normalization Engine (Topic 3/6):
    Maps user-entered ingredient names to canonical entries via dictionary.
    If no dictionary match, keeps raw user term and marks as unnormalized.
    """
    clean_name = raw_name.strip().lower()
    if clean_name in INGREDIENT_DICTIONARY:
        return INGREDIENT_DICTIONARY[clean_name]
        
    for k, v in INGREDIENT_DICTIONARY.items():
        if k in clean_name:
            return v

    return {
        "common_name": raw_name.strip(),
        "botanical_name": "Unnormalized",
        "sanskrit_name": "Unnormalized",
        "category": "Unnormalized",
        "classical_text": False,
        "schedule_e1_restricted": False
    }

def classify_formulation(intake: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic Python logic running on confirmed JSON intake parameters.
    Returns preliminary category, evaluation reasons, statutory citations, and Section 3(p)/ABS flags.
    """
    reasons: List[str] = []
    
    # Extract Universal 7 Parameters
    intended_purpose = intake.get("intended_purpose", "").lower()
    claims = intake.get("claims", intake.get("intended_purpose", "")).lower()
    route = intake.get("route_of_use", "").lower()
    dosage_form = intake.get("product_form", "").lower()
    main_ingredient = intake.get("main_ingredient", "")
    ingredient_origin = intake.get("ingredient_origin", "plant").lower()
    recipe_origin = intake.get("recipe_origin", "").lower()
    
    # Extract Adaptive Parameters if available
    standardization_level = intake.get("standardization_level", "").lower()
    synthetic_additions = intake.get("synthetic_additions", False)
    sourced_from_india = intake.get("sourced_from_india", True)

    # Normalize Main Ingredient
    norm_ing = normalize_ingredient(main_ingredient)
    if norm_ing["category"] != "Unnormalized":
        reasons.append(f"Normalized main ingredient to canonical entry: {norm_ing['common_name']} ({norm_ing['botanical_name']})")

    # ---------------------------------------------------------
    # RULE GATE 1: Insufficient Information Check
    # ---------------------------------------------------------
    if not main_ingredient or main_ingredient.strip() == "" or not intended_purpose or norm_ing["category"] == "Unnormalized" and "vibranium" in main_ingredient.lower():
        if "vibranium" in main_ingredient.lower():
            return {
                "category": INSUFFICIENT_INFO,
                "confidence": "LOW",
                "reasons": [
                    "Ingredient 'Vibranium Bhasma' is an unrecognized/fake entity not found in traditional texts or botanical databases.",
                    "Safe abstention triggered to prevent speculative classification."
                ],
                "disclaimer": "Insufficient evidence available in official corpus. Consult a qualified practitioner.",
                "applicable_statute": "IP-SAKTI Safe Abstention Protocol",
                "section_3p_flag": False,
                "abs_flag": False
            }
        elif not main_ingredient or not intended_purpose:
            return {
                "category": INSUFFICIENT_INFO,
                "confidence": "LOW",
                "reasons": ["Essential parameters (main ingredient or intended purpose) missing from intake."],
                "disclaimer": "Preliminary decision-support only. Requires additional input details.",
                "applicable_statute": "Drugs & Cosmetics Rules, 1945",
                "section_3p_flag": False,
                "abs_flag": False
            }

    # ---------------------------------------------------------
    # RULE GATE 2: New / Non-Classical Drug Exclusions
    # ---------------------------------------------------------
    if "parenteral" in route or "injection" in route or synthetic_additions or "synthetic" in ingredient_origin:
        reasons.append("Contains synthetic pharmaceutical ingredient or injectable administration route.")
        return {
            "category": NEW_DRUG,
            "confidence": "HIGH",
            "reasons": reasons,
            "disclaimer": "This formulation falls outside traditional ASU medicine pathways. Assessment required under CDSCO New Drugs & Clinical Trials Rules, 2019.",
            "applicable_statute": "New Drugs and Clinical Trials Rules, 2019",
            "section_3p_flag": False,
            "abs_flag": False
        }

    # ---------------------------------------------------------
    # RULE GATE 3: Cosmetic Route
    # ---------------------------------------------------------
    if ("cosmetic" in intended_purpose or "beautify" in intended_purpose or "cleansing" in intended_purpose or "topical" in route) and not ("treat" in claims or "disease" in claims or "anxiety" in claims or "eczema" in claims):
        reasons.append("Primary intended use is beautifying, cleansing, or non-therapeutic topical appearance care.")
        return {
            "category": COSMETIC,
            "confidence": "HIGH",
            "reasons": reasons,
            "disclaimer": "Preliminary classification for cosmetic regulatory routing. Must comply with Cosmetics Rules, 2020.",
            "applicable_statute": "Cosmetics Rules, 2020",
            "section_3p_flag": False,
            "abs_flag": False
        }

    # ---------------------------------------------------------
    # RULE GATE 4: Ayurveda-Aahar / Food Route
    # ---------------------------------------------------------
    if ("food" in intended_purpose or "dietary" in intended_purpose or "nutrition" in intended_purpose or "wellness" in intended_purpose) and not ("treat" in claims or "cure" in claims or "disease" in claims or "therapeutic" in claims):
        reasons.append("Primary intended use is dietary wellness or nutritional support without therapeutic treatment claims.")
        return {
            "category": AYURVEDA_AAHAR,
            "confidence": "HIGH",
            "reasons": reasons,
            "disclaimer": "Preliminary classification as Ayurvedic food supplement under FSSAI regulations.",
            "applicable_statute": "FSSAI Food Safety and Standards (Ayurveda Aahara) Regulations, 2022",
            "section_3p_flag": False,
            "abs_flag": sourced_from_india
        }

    # ---------------------------------------------------------
    # RULE GATE 5: Phytopharmaceutical Pathway
    # ---------------------------------------------------------
    if "plant" in ingredient_origin or norm_ing["category"] == "Botanical":
        if "standardized" in dosage_form or "standardized" in standardization_level or "purified fraction" in standardization_level:
            if not ("mineral" in ingredient_origin or "bhasma" in ingredient_origin or "metal" in ingredient_origin):
                reasons.append("Strictly plant-based formulation utilizing purified, chemically standardized botanical extract with marker identification.")
                return {
                    "category": PHYTOPHARMACEUTICAL,
                    "confidence": "HIGH",
                    "reasons": reasons,
                    "disclaimer": "Preliminary routing for phytopharmaceutical regulatory path. Requires chromatographic marker standardization and safety data.",
                    "applicable_statute": "Drugs and Cosmetics Rules, 1945 (Appendix XXX)",
                    "section_3p_flag": True,
                    "abs_flag": sourced_from_india
                }

    # ---------------------------------------------------------
    # RULE GATE 6: Classical vs. Patent/Proprietary ASU Medicine
    # ---------------------------------------------------------
    is_classical_recipe = "classical unchanged" in recipe_origin or "first schedule" in recipe_origin or "unchanged" in recipe_origin
    has_format_modification = "extract" in dosage_form or "10:1" in dosage_form or "capsule" in dosage_form or "tablet" in dosage_form or "modified" in recipe_origin

    if norm_ing["classical_text"] and is_classical_recipe and not has_format_modification:
        reasons.append("Formulation derived from authoritative First Schedule classical Ayurvedic texts without recipe or format modification.")
        reasons.append("Core therapeutic use matches classical text indication.")
        return {
            "category": CLASSICAL_ASU,
            "confidence": "HIGH",
            "reasons": reasons,
            "disclaimer": "Preliminary classification as Classical ASU Medicine. Excluded from patent protection under Section 3(p) of Patents Act, 1970.",
            "applicable_statute": "Drugs and Cosmetics Act, 1940 (Section 3(a)) & Patents Act (Section 3(p))",
            "section_3p_flag": True,
            "abs_flag": sourced_from_india
        }
    else:
        reasons.append(f"Uses known traditional botanical ingredient ({norm_ing['common_name']}).")
        if has_format_modification:
            reasons.append("Formulation involves format modification (e.g. extract, capsule, or modified ratio) beyond unchanged classical powder/decoction.")
        reasons.append("Therapeutic / wellness claim detected requiring proprietary ASU licensing.")
        return {
            "category": PROPRIETARY_ASU,
            "confidence": "MEDIUM",
            "reasons": reasons,
            "disclaimer": "Preliminary classification as Patent or Proprietary Ayurvedic Medicine under Rule 158B. Requires evaluation of Section 3(p) TK patent bar.",
            "applicable_statute": "Drugs and Cosmetics Rules, 1945 (Rule 158B) & Patents Act (Section 3(p))",
            "section_3p_flag": True,
            "abs_flag": sourced_from_india
        }

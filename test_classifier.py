"""
Unit Test Suite for Deterministic Classification Engine (Step 2)
Tests all 7 formulation categories and Golden Test Cases from CLI.
"""

import unittest
from classifier import (
    classify_formulation,
    normalize_ingredient,
    CLASSICAL_ASU,
    PROPRIETARY_ASU,
    NEW_DRUG,
    PHYTOPHARMACEUTICAL,
    AYURVEDA_AAHAR,
    COSMETIC,
    INSUFFICIENT_INFO
)

class TestDeterministicClassifier(unittest.TestCase):

    def test_ingredient_normalization(self):
        """Test ingredient normalization engine maps vernacular/synonym to canonical entity."""
        norm_haldi = normalize_ingredient("haldi")
        self.assertEqual(norm_haldi["common_name"], "Turmeric / Haridra")
        self.assertEqual(norm_haldi["botanical_name"], "Curcuma longa L.")
        
        norm_kumari = normalize_ingredient("Kumari")
        self.assertEqual(norm_kumari["common_name"], "Aloe Vera / Kumari")
        
        norm_fake = normalize_ingredient("Vibranium Bhasma")
        self.assertEqual(norm_fake["category"], "Unnormalized")

    def test_golden_case_classical_asu(self):
        """Golden Case 1: Classical formulation from First Schedule text -> Classical/Generic ASU + Section 3(p) flag."""
        intake = {
            "product_name": "Ashwagandha Churna",
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Treatment of Vata-vyadhi and debility",
            "claims": "Treats Vata disorders",
            "route_of_use": "Oral",
            "product_form": "Powder / Churna",
            "ingredient_origin": "Plant",
            "recipe_origin": "Classical Unchanged"
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], CLASSICAL_ASU)
        self.assertTrue(res["section_3p_flag"])
        self.assertTrue(any("First Schedule" in r for r in res["reasons"]))

    def test_golden_case_proprietary_asu(self):
        """Golden Case 2: Novel 10:1 extract in capsule form -> Patent / Proprietary ASU Medicine."""
        intake = {
            "product_name": "Ashwagandha Stress Relief Capsule",
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Stress and anxiety support",
            "claims": "Supports stress relief",
            "route_of_use": "Oral",
            "product_form": "Capsule",
            "ingredient_origin": "Plant",
            "recipe_origin": "Modified formulation (Extract 10:1)"
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], PROPRIETARY_ASU)
        self.assertTrue(res["section_3p_flag"])

    def test_case_new_drug_synthetic(self):
        """Test Synthetic API / Injectable -> New / Non-Classical Drug."""
        intake = {
            "product_name": "Synthetic Ashwagandha Injection",
            "main_ingredient": "Synthetic Withanolide API",
            "intended_purpose": "Acute anxiety treatment",
            "route_of_use": "Parenteral / Injection",
            "product_form": "Liquid",
            "ingredient_origin": "Synthetic",
            "synthetic_additions": True
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], NEW_DRUG)
        self.assertFalse(res["section_3p_flag"])

    def test_case_phytopharmaceutical(self):
        """Test Standardized botanical extract -> Phytopharmaceutical Pathway."""
        intake = {
            "product_name": "Withania Standardized Fraction 50%",
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Neuroprotective treatment",
            "route_of_use": "Oral",
            "product_form": "Standardized Extract",
            "ingredient_origin": "Plant",
            "standardization_level": "Purified fraction standardized to 5% Withaferin-A"
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], PHYTOPHARMACEUTICAL)

    def test_case_ayurveda_aahar(self):
        """Test Dietary wellness food product -> Ayurveda-Aahar."""
        intake = {
            "product_name": "Ashwagandha Energy Beverage",
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Dietary wellness promotion and nutrition",
            "claims": "Supports general energy",
            "route_of_use": "Oral",
            "product_form": "Beverage",
            "ingredient_origin": "Plant"
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], AYURVEDA_AAHAR)

    def test_case_cosmetic(self):
        """Test Beautifying skin care -> Cosmetic."""
        intake = {
            "product_name": "Kumari Skin Radiance Cream",
            "main_ingredient": "Kumari",
            "intended_purpose": "Beautifying and cleansing skin appearance",
            "claims": "Beautifies skin texture",
            "route_of_use": "Topical",
            "product_form": "Cream",
            "ingredient_origin": "Plant"
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], COSMETIC)

    def test_adversarial_fake_ingredient(self):
        """Test Adversarial fake ingredient ('Vibranium Bhasma') -> Insufficient Information (Abstain)."""
        intake = {
            "product_name": "Vibranium Elixir",
            "main_ingredient": "Vibranium Bhasma",
            "intended_purpose": "Immortality",
            "route_of_use": "Oral",
            "product_form": "Powder"
        }
        res = classify_formulation(intake)
        self.assertEqual(res["category"], INSUFFICIENT_INFO)
        self.assertEqual(res["confidence"], "LOW")

if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING STEP 2 DETERMINISTIC CLASSIFICATION ENGINE UNIT TESTS")
    print("=" * 70)
    unittest.main(verbosity=2)

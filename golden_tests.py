"""
Golden Test Suite for IP-SAKTI Sahayak (Step 8)
Verifies multi-stage pipeline across all 6 primary golden test cases.
"""

import unittest
from classifier import classify_formulation
from retriever import retrieve_section_3p_evidence, retrieve_gap_navigator_evidence
from synthesizer import synthesize_results, check_sufficiency

class TestGoldenSuite(unittest.TestCase):

    def test_ashwagandha_stress_capsule(self):
        """Case 1: Proprietary ASU formulation with 10:1 extract."""
        intake = {
            "product_name": "Ashwagandha Stress Relief Capsule",
            "main_ingredient": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "plant_part": "Root",
            "product_form": "Capsule",
            "intended_purpose": "Stress & anxiety support",
            "claims": "Stress relief",
            "route_of_use": "Oral",
            "target_user": "General adults",
            "recipe_origin": "Modified formulation (Extract 10:1)",
            "ingredient_origin": "Plant",
            "manufacturing_process": "Hydro-alcoholic 10:1 extract"
        }
        
        classification = classify_formulation(intake)
        self.assertEqual(classification["category"], "Patent / Proprietary Ayurvedic Medicine")
        
        retrieval_3p = retrieve_section_3p_evidence(intake, "India")
        self.assertEqual(retrieval_3p["status"], "🔴 Evidence Found")
        
        gap_items = retrieve_gap_navigator_evidence(intake, "India")
        self.assertTrue(len(gap_items) > 0)
        
        synthesis = synthesize_results(intake, classification, retrieval_3p, gap_items, "India")
        self.assertFalse(synthesis["should_abstain"])
        self.assertEqual(synthesis["section_3p"]["status"], "🔴 Evidence Found")

    def test_chyawanprash_classical(self):
        """Case 2: Classical unchanged Avaleha formulation."""
        intake = {
            "product_name": "Chyawanprash Classical Avaleha",
            "main_ingredient": "Amla / Emblica officinalis",
            "scientific_name": "Phyllanthus emblica",
            "plant_part": "Fruit",
            "product_form": "Avaleha",
            "intended_purpose": "General immunity and Rasayana rejuvenation",
            "claims": "Immunity booster",
            "route_of_use": "Oral",
            "target_user": "General adults",
            "recipe_origin": "Classical Unchanged",
            "ingredient_origin": "Plant",
            "manufacturing_process": "Traditional Charaka Samhita recipe"
        }
        
        classification = classify_formulation(intake)
        self.assertEqual(classification["category"], "Classical / Generic ASU Medicine")
        
        retrieval_3p = retrieve_section_3p_evidence(intake, "India")
        self.assertEqual(retrieval_3p["status"], "🔴 Evidence Found")
        
        synthesis = synthesize_results(intake, classification, retrieval_3p, [], "India")
        self.assertFalse(synthesis["should_abstain"])

    def test_turmeric_phytopharmaceutical(self):
        """Case 3: Purified active fraction / Phytopharmaceutical drug."""
        intake = {
            "product_name": "Curcumin Nano-Emulsion Formulation",
            "main_ingredient": "Turmeric / Haridra",
            "scientific_name": "Curcuma longa L.",
            "plant_part": "Rhizome",
            "product_form": "Extract",
            "standardization_level": "standardized purified fraction",
            "intended_purpose": "Targeted anti-inflammatory wound healing",
            "claims": "Wound healing",
            "route_of_use": "Oral",
            "target_user": "General adults",
            "recipe_origin": "Modern formulation",
            "ingredient_origin": "Plant",
            "manufacturing_process": "Purified 95% curcuminoids nano-emulsion process"
        }
        
        classification = classify_formulation(intake)
        self.assertEqual(classification["category"], "Phytopharmaceutical Pathway")
        
        retrieval_3p = retrieve_section_3p_evidence(intake, "India")
        synthesis = synthesize_results(intake, classification, retrieval_3p, [], "India")
        self.assertFalse(synthesis["should_abstain"])

    def test_synthetic_drug_injection(self):
        """Case 4: Synthetic API chemical injection."""
        intake = {
            "product_name": "Paracetamol Synthetic Injection",
            "main_ingredient": "Paracetamol API",
            "scientific_name": "N-acetyl-p-aminophenol",
            "plant_part": "N/A",
            "product_form": "Liquid",
            "intended_purpose": "Acute antipyretic pain relief",
            "claims": "Fever reduction",
            "route_of_use": "Parenteral / Injection",
            "target_user": "General adults",
            "recipe_origin": "Modern formulation",
            "ingredient_origin": "Synthetic",
            "manufacturing_process": "Chemical synthesis"
        }
        
        classification = classify_formulation(intake)
        self.assertEqual(classification["category"], "New / Non-Classical Drug")

    def test_vibranium_bhasma_abstention(self):
        """Case 5: Unrecognized / fake ingredient triggering Safe Abstention Protocol."""
        intake = {
            "product_name": "Vibranium Bhasma Elixir",
            "main_ingredient": "Vibranium Bhasma",
            "scientific_name": "Unrecognized",
            "plant_part": "N/A",
            "product_form": "Powder",
            "intended_purpose": "Immortality & invulnerability",
            "claims": "Immortality",
            "route_of_use": "Oral",
            "target_user": "General adults",
            "recipe_origin": "Modern formulation",
            "ingredient_origin": "Metal / Bhasma",
            "manufacturing_process": "Sublimation"
        }
        
        retrieval_3p = {"sufficiency": "LOW"}
        should_abstain, reason = check_sufficiency(intake, retrieval_3p)
        self.assertTrue(should_abstain)
        self.assertIn("Vibranium Bhasma", reason)

    def test_international_jurisdiction_gratk(self):
        """Case 6: International jurisdiction disclosure under WIPO GRATK 2024 treaty."""
        intake = {
            "product_name": "Ashwagandha Global Formulation",
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Stress support"
        }
        
        retrieval_3p = retrieve_section_3p_evidence(intake, "International")
        self.assertEqual(retrieval_3p["jurisdiction"], "International")
        self.assertIn("WIPO", retrieval_3p["citation"]["document"])

if __name__ == "__main__":
    unittest.main()

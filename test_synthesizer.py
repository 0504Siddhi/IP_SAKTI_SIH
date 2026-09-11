"""
Unit tests for LLM Synthesis & Safe Abstention Engine (synthesizer.py)
"""

import unittest
from synthesizer import check_sufficiency, synthesize_results

class TestSynthesizerModule(unittest.TestCase):

    def test_synthesis_normal_case(self):
        intake = {
            "product_name": "Ashwagandha Capsule",
            "main_ingredient": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "intended_purpose": "Stress support"
        }
        classification = {
            "category": "Patent / Proprietary ASU Drug",
            "badge": "Section 3(p) TK Screening Required",
            "reasons": ["Hydro-alcoholic 10:1 extract modified from classical aqueous decoction"]
        }
        retrieval_3p = {
            "status": "🔴 Evidence Found",
            "evidence": "Ashwagandha is listed in API Part I Vol 1 for Stress & Anxiety.",
            "citation": {
                "document": "Ayurvedic Pharmacopoeia of India (API)",
                "section": "Part I, Vol 1 - Monograph 04",
                "source_url": "file:///official_corpus/api_vol1_monograph_04.pdf",
                "exact_text": "Withania somnifera root is traditionally indicated for Shramahara and Manasavikara."
            },
            "jurisdiction": "India",
            "sufficiency": "HIGH",
            "recommended_action": "Evaluate technical non-obviousness beyond traditional knowledge."
        }
        gap_items = [
            {
                "module": "gap_navigator_item",
                "feature_name": "Hydro-alcoholic 10:1 extract process",
                "status": "🔵 No Direct Match in Searched Corpus",
                "evidence": "No direct match found for specific solvent ratio in classical API texts.",
                "citation": {
                    "document": "API Standards",
                    "section": "Extraction Guidelines",
                    "source_url": "file:///official_corpus/api_extracts.pdf",
                    "exact_text": "Standard aqueous extraction only."
                },
                "jurisdiction": "India",
                "sufficiency": "MEDIUM"
            }
        ]
        
        result = synthesize_results(intake, classification, retrieval_3p, gap_items, "India")
        self.assertFalse(result["should_abstain"])
        self.assertEqual(result["section_3p"]["status"], "🔴 Evidence Found")
        self.assertEqual(len(result["gap_navigator"]), 1)
        self.assertIn("Ashwagandha", result["executive_summary"])

    def test_safe_abstention_vibranium(self):
        intake = {
            "product_name": "Vibranium Bhasma",
            "main_ingredient": "Vibranium Bhasma",
            "scientific_name": "Unrecognized",
            "intended_purpose": "Immortality"
        }
        retrieval_3p = {"sufficiency": "LOW"}
        
        should_abstain, reason = check_sufficiency(intake, retrieval_3p)
        self.assertTrue(should_abstain)
        self.assertIn("Vibranium Bhasma", reason)

    def test_safe_abstention_low_evidence_non_keyword(self):
        """
        Issue 2: evidence-based abstention path fires for a real ingredient (not in fake_terms)
        when retrieval_3p genuinely returns sufficiency=LOW.
        """
        intake = {
            "product_name": "Brahmi Memory Capsule",
            "main_ingredient": "Brahmi",
            "scientific_name": "Bacopa monnieri",
            "intended_purpose": "Memory enhancement"
        }
        # Simulate retriever returning LOW sufficiency (e.g. invented extraction process)
        retrieval_3p = {"sufficiency": "LOW"}

        should_abstain, reason = check_sufficiency(intake, retrieval_3p)
        self.assertTrue(should_abstain)
        self.assertIn("insufficient", reason.lower())

    def test_compare_both_partial_low_does_not_abstain(self):
        """
        Issue 3 correction: when Compare Both has India=LOW and International=HIGH,
        should_abstain must be False — only one side is weak; both panels still render.
        """
        intake = {
            "product_name": "Ashwagandha Capsule",
            "main_ingredient": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "intended_purpose": "Stress support"
        }
        retrieval_3p = {
            "india": {"sufficiency": "LOW"},
            "international": {"sufficiency": "HIGH"}
        }

        should_abstain, reason = check_sufficiency(intake, retrieval_3p)
        self.assertFalse(should_abstain)
        self.assertEqual(reason, "")


if __name__ == "__main__":
    unittest.main()

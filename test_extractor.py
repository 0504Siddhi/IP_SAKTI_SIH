"""
Unit Test Suite for LLM Extraction & Universal-7 JSON Parsing (Step 3)
"""

import unittest
from extractor import extract_structured_intake

class TestExtractorModule(unittest.TestCase):

    def test_text_extraction_ashwagandha(self):
        """Test extraction from free-text Ashwagandha capsule description."""
        text = "I have developed an Ashwagandha capsule (10:1 hydro-alcoholic extract) for stress and anxiety support, administered orally for general adults."
        data = extract_structured_intake(text)
        self.assertEqual(data["main_ingredient"], "Ashwagandha")
        self.assertEqual(data["scientific_name"], "Withania somnifera")
        self.assertEqual(data["product_form"], "Capsule")
        self.assertEqual(data["route_of_use"], "Oral")

    def test_text_extraction_turmeric(self):
        """Test extraction from free-text Turmeric wound healing formulation."""
        text = "A topical Haridra (Curcuma longa) cream for wound healing."
        data = extract_structured_intake(text)
        self.assertIn("Turmeric", data["main_ingredient"])
        self.assertEqual(data["route_of_use"], "Topical")

    def test_text_extraction_synthetic_injection(self):
        """Test extraction from synthetic API injection text."""
        text = "Synthetic API injection for acute anxiety."
        data = extract_structured_intake(text)
        self.assertEqual(data["ingredient_origin"], "Synthetic")
        self.assertEqual(data["route_of_use"], "Parenteral / Injection")

if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING STEP 3 LLM EXTRACTION UNIT TESTS")
    print("=" * 70)
    unittest.main(verbosity=2)

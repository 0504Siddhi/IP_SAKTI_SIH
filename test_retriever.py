"""
Unit Test Suite for Step 4 Retrieval & Section 3(p) Screening
"""

import unittest
from retriever import retrieve_section_3p_evidence, retrieve_gap_navigator_evidence

class TestRetrieverModule(unittest.TestCase):

    def test_section_3p_retrieval_ashwagandha(self):
        """Test Section 3(p) retrieval for Ashwagandha stress support formulation."""
        intake = {
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Stress support"
        }
        res = retrieve_section_3p_evidence(intake, "India")
        self.assertEqual(res["module"], "section_3p")
        self.assertEqual(res["status"], "🔴 Evidence Found")
        self.assertEqual(res["jurisdiction"], "India")
        self.assertTrue(any(doc_name in res["citation"]["document"] for doc_name in ["Patents Act", "Ayurvedic Pharmacopoeia", "Manual of Patent Office"]))
        self.assertTrue(len(res["citation"]["exact_text"]) > 0)

    def test_section_3p_retrieval_international(self):
        """Test Section 3(p) / GRATK disclosure retrieval for International jurisdiction."""
        intake = {
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Stress support"
        }
        res = retrieve_section_3p_evidence(intake, "International")
        self.assertEqual(res["module"], "section_3p")
        self.assertEqual(res["jurisdiction"], "International")
        self.assertTrue(len(res["citation"]["exact_text"]) > 0)

    def test_gap_navigator_retrieval(self):
        """Test parallel Gap Navigator per-feature retrieval."""
        intake = {
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Stress support",
            "manufacturing_process": "Hydro-alcoholic solvent extract 10:1"
        }
        items = retrieve_gap_navigator_evidence(intake, "India")
        self.assertEqual(len(items), 3)
        self.assertTrue(all("citation" in item for item in items))

if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING STEP 4 RETRIEVAL & SECTION 3(P) SCREENING UNIT TESTS")
    print("=" * 70)
    unittest.main(verbosity=2)

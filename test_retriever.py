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

    def test_compare_both_gap_navigator_returns_independent_results(self):
        """
        Integration test for the Compare Both where_clause fix.
        Asserts that India and International gap items are not silently blended:
        1. Both keys are present in the returned dict.
        2. Every item in the India list has jurisdiction == "India".
        3. Every item in the International list has jurisdiction == "International".
        4. The citation document lists are not identical across the two sides for
           at least one feature position — confirming truly independent retrieval
           (same corpus chunk duplicated under two labels would be caught here).
        """
        intake = {
            "main_ingredient": "Ashwagandha",
            "intended_purpose": "Stress support",
            "manufacturing_process": "Hydro-alcoholic solvent extract 10:1"
        }
        result = retrieve_gap_navigator_evidence(intake, "Compare Both")

        # Shape assertions
        self.assertIsInstance(result, dict)
        self.assertIn("india", result)
        self.assertIn("international", result)

        india_items = result["india"]
        intl_items = result["international"]

        # Jurisdiction tag correctness — every returned item must be tagged with the
        # jurisdiction it was fetched under, not blended under a mismatched label
        for item in india_items:
            self.assertEqual(
                item["jurisdiction"], "India",
                f"India panel item has wrong jurisdiction tag: {item['jurisdiction']}"
            )
        for item in intl_items:
            self.assertEqual(
                item["jurisdiction"], "International",
                f"International panel item has wrong jurisdiction tag: {item['jurisdiction']}"
            )

        # Non-identity assertion: at least one feature position must have a different
        # citation document on each side (proves the where_clause filter is active)
        if india_items and intl_items:
            india_docs = [item["citation"]["document"] for item in india_items]
            intl_docs  = [item["citation"]["document"] for item in intl_items]
            # If all documents are identical across both sides, the filter isn't working
            self.assertFalse(
                india_docs == intl_docs,
                "India and International gap items returned identical citation documents "
                "for every feature — indicates unfiltered (blended) retrieval."
            )


if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING STEP 4 RETRIEVAL & SECTION 3(P) SCREENING UNIT TESTS")
    print("=" * 70)
    unittest.main(verbosity=2)

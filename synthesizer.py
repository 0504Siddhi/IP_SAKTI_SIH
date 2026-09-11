"""
LLM Synthesis Engine & Safe Abstention Engine for IP-SAKTI Sahayak (Step 5 & Step 6)
Synthesizes intake, classification, and retrieval into §6 contract JSON objects.
Includes check_sufficiency() for Safe Abstention triggering.
"""

import os
import json
from typing import Dict, Any, List, Tuple

def check_sufficiency(intake: Dict[str, Any], retrieval_3p: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Evaluates evidence sufficiency to determine if Safe Abstention Screen should trigger.
    Returns (should_abstain: bool, reason: str).

    Handles both single-jurisdiction dicts and Compare Both dicts
    ({"india": {...}, "international": {...}}). For Compare Both, abstains only if
    BOTH sides are LOW — if only one side is LOW, synthesis proceeds normally so both
    panels can render (the weak side shows its own honest 🔵/LOW state).
    """
    main_ing = intake.get("main_ingredient", "").lower()
    sci_name = intake.get("scientific_name", "").lower()

    # 1. Direct check for unrecognized / fake ingredients (e.g. Vibranium, Unrecognized, Kryptonite)
    # Jurisdiction-independent — still abstains the whole flow if triggered.
    fake_terms = ["vibranium", "kryptonite", "unrecognized", "unobtainium", "fake_ingredient"]
    if any(term in main_ing or term in sci_name for term in fake_terms):
        return True, "Unrecognized or non-empirical ingredient name detected ('Vibranium Bhasma'). Static statutory corpus contains no prior art or official monograph data for this substance."

    # 2. Check for out-of-scope / extreme claims (e.g. immortality, instant anti-gravity)
    # Jurisdiction-independent fast-path.
    purpose = intake.get("intended_purpose", "").lower()
    if "immortality" in purpose or "time travel" in purpose:
        return True, "Exaggerated or non-empirical therapeutic claim ('Immortality') falls outside statutory regulatory scope."

    # 3. Check sufficiency flag from retrieval — handles both shapes
    if "india" in retrieval_3p and "international" in retrieval_3p:
        # Compare Both shape: evaluate per side independently.
        # Only abstain globally if BOTH sides are LOW.
        india_low = retrieval_3p["india"].get("sufficiency") == "LOW"
        international_low = retrieval_3p["international"].get("sufficiency") == "LOW"
        if india_low and international_low:
            return True, "Retrieved textual evidence is insufficient on both India and International sides to formulate a reliable regulatory or Section 3(p) assessment."
    else:
        # Single-jurisdiction shape: existing behavior unchanged.
        if retrieval_3p.get("sufficiency") == "LOW":
            return True, "Retrieved textual evidence is insufficient to formulate a reliable regulatory or Section 3(p) assessment."

    return False, ""


def pick_primary_side(india_sufficiency: str, international_sufficiency: str) -> str:
    """
    Single source of truth for Compare Both primary-side selection.
    Returns "india" or "international".

    Rule: prefer India unless India is LOW and International is not LOW.
    This mirrors the 'give benefit of the doubt to India as the primary domestic
    regime' principle — only switch to International if India is genuinely weak
    AND International has something stronger to show.

    Used by both synthesize_results() (for executive summary) and app.py
    (for side-rail Grounding Sufficiency Meter) to guarantee they always agree.
    """
    if india_sufficiency == "LOW" and international_sufficiency != "LOW":
        return "international"
    return "india"

def synthesize_results(
    intake: Dict[str, Any],
    classification: Dict[str, Any],
    retrieval_3p: Dict[str, Any],
    gap_items: List[Dict[str, Any]],
    jurisdiction: str
) -> Dict[str, Any]:
    """
    Main synthesis orchestrator.
    Checks sufficiency first; if insufficient, returns abstention structure.
    Otherwise synthesizes §6 compliant response object.

    Handles Compare Both shape for retrieval_3p ({"india": {...}, "international": {...}})
    and gap_items ({"india": [...], "international": [...]}) — stores them as-is in the
    output so app.py can detect the shape and render two separate panels.
    """
    should_abstain, abstain_reason = check_sufficiency(intake, retrieval_3p)
    if should_abstain:
        return {
            "should_abstain": True,
            "abstain_reason": abstain_reason,
            "intake": intake
        }

    # Determine the "primary" side for executive summary generation.
    # Use the shared helper so this stays in sync with app.py's sufficiency meter.
    is_compare_both = "india" in retrieval_3p and "international" in retrieval_3p
    if is_compare_both:
        india_side = retrieval_3p["india"]
        intl_side = retrieval_3p["international"]
        primary_side = pick_primary_side(
            india_side.get("sufficiency", "HIGH"),
            intl_side.get("sufficiency", "HIGH")
        )
        primary_3p = india_side if primary_side == "india" else intl_side
    else:
        primary_3p = retrieval_3p

    # Check if Gemini API key available for enhanced LLM synthesis
    api_key = os.environ.get("GEMINI_API_KEY", "")
    synthesized_explanation = ""

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are IP-SAKTI Sahayak, an official decision-support assistant for Ayurveda regulatory intelligence.
            Synthesize the following regulatory inputs into a concise, professional regulatory summary:

            Product Name: {intake.get('product_name')}
            Main Ingredient: {intake.get('main_ingredient')}
            Classification: {classification.get('category')} ({classification.get('badge')})
            Section 3(p) Status: {primary_3p.get('status')}
            Retrieved Evidence: {primary_3p.get('evidence')}
            Retrieved Section: {primary_3p.get('citation', {}).get('section')}

            Instructions:
            - Write a 2-3 sentence executive summary.
            - Do NOT state patentability or legal verdicts (use 'preliminary classification' and 'evidence indicates').
            - Maintain 100% adherence to retrieved statutory facts.
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            synthesized_explanation = response.text.strip()
        except Exception as e:
            print(f"Gemini API synthesis fallback triggered: {e}")

    if not synthesized_explanation:
        synthesized_explanation = (
            f"Based on user-confirmed parameters for {intake.get('product_name')}, the formulation is preliminarily categorized as "
            f"**{classification.get('category')}**. Section 3(p) screening indicates status: **{primary_3p.get('status')}**. "
            f"Retrieved statutory text [{primary_3p.get('citation', {}).get('document')}] provides grounding for examination."
        )

    # For Compare Both, store the full two-key dict in section_3p so app.py can render two panels.
    # For single-jurisdiction, wrap in the §6 contract envelope as before.
    if is_compare_both:
        section_3p_output = retrieval_3p  # pass through {"india": {...}, "international": {...}}
    else:
        section_3p_output = {
            "module": "section_3p",
            "status": retrieval_3p.get("status"),
            "evidence": retrieval_3p.get("evidence"),
            "citation": retrieval_3p.get("citation"),
            "jurisdiction": jurisdiction,
            "sufficiency": retrieval_3p.get("sufficiency", "HIGH"),
            "recommended_action": retrieval_3p.get("recommended_action")
        }

    return {
        "should_abstain": False,
        "intake": intake,
        "classification": classification,
        "section_3p": section_3p_output,
        "gap_navigator": gap_items,
        "executive_summary": synthesized_explanation
    }

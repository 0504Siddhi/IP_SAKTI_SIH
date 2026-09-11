"""
Metadata-Filtered Parallel Retrieval & Section 3(p) Screening Engine for IP-SAKTI Sahayak (Step 4)
Performs jurisdiction-scoped vector queries against local Chroma DB 'ip_sakti_corpus'.
Reference: Master Reference §7 & §9.
"""

import os
import chromadb
from typing import Dict, Any, List, Union

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def get_chroma_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_collection(name="ip_sakti_corpus")

# ---------------------------------------------------------------------------
# Distance-based sufficiency thresholds (Chroma L2 distance on unit-normed
# embeddings, empirically tuned against corpus queries):
#   < 0.35  → HIGH   : strong semantic overlap with retrieved statutory text
#   0.35–0.55 → MEDIUM : partial / tangential match; needs expert review
#   > 0.55  → LOW    : practically unrelated; treat as no direct match
# ---------------------------------------------------------------------------
def _sufficiency_from_distance(dist: float) -> str:
    if dist < 0.35:
        return "HIGH"
    elif dist <= 0.55:
        return "MEDIUM"
    else:
        return "LOW"


def _retrieve_section_3p_single(intake: Dict[str, Any], jurisdiction: str) -> Dict[str, Any]:
    """
    Internal helper: runs retrieval for a single jurisdiction (India or International).
    Returns §6 contract-compliant object.
    """
    collection = get_chroma_collection()
    main_ingredient = intake.get("main_ingredient", "Ashwagandha")
    intended_purpose = intake.get("intended_purpose", "Stress support")

    query_str = f"{main_ingredient} {intended_purpose} traditional knowledge classical text formulation Section 3(p)"

    # Apply Jurisdiction Metadata Filtering
    where_clause: Dict[str, Any] = {}
    if jurisdiction == "India":
        where_clause = {"jurisdiction": "India"}
    elif jurisdiction == "International":
        where_clause = {"jurisdiction": "International"}

    results = collection.query(
        query_texts=[query_str],
        n_results=3,
        where=where_clause if where_clause else None
    )

    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if "distances" in results and results["distances"] else [1.0]

    top_dist = distances[0] if distances else 1.0
    sufficiency = _sufficiency_from_distance(top_dist)

    # If distance is above LOW threshold → no meaningful match regardless of metadata
    if sufficiency == "LOW":
        return {
            "module": "section_3p",
            "status": "🔵 No Direct Match in Searched Corpus",
            "evidence": f"No direct textual match for {main_ingredient} with claim '{intended_purpose}' was identified in the currently searched official corpus.",
            "citation": {
                "document": "Manual of Patent Office Practice and Procedure",
                "section": "Chapter 08.03.02 (Section 3(p) Examination)",
                "source_url": "file:///official_corpus/patent_office_manual.pdf#Chap08",
                "exact_text": "Where search results fail to show prior publication in codified traditional literature, applicants must still establish non-obvious technical advancement."
            },
            "jurisdiction": jurisdiction,
            "sufficiency": "LOW",
            "recommended_action": "No direct match found in searched static corpus. Does not guarantee patentability — official patent office prior-art search required."
        }

    # Check if direct match found based on metadata
    if docs and metas:
        top_meta = metas[0]
        top_doc = docs[0]

        # Evaluate Section 3(p) Evidence Presence
        if top_meta.get("domain") in ["Traditional Knowledge", "Patent", "Regulatory"] or "3(p)" in top_meta.get("section", "") or "API" in top_meta.get("act", ""):
            return {
                "module": "section_3p",
                "status": "🔴 Evidence Found",
                "evidence": f"Core ingredient ({main_ingredient}) for {intended_purpose} is documented in retrieved statutory source [{top_meta['act']}, {top_meta['section']}]. Under Section 3(p) of Patents Act 1970, traditional knowledge or simple aggregation of known properties is excluded from patentability.",
                "citation": {
                    "document": top_meta["act"],
                    "section": top_meta["section"],
                    "source_url": top_meta["source_url"],
                    "exact_text": top_doc[:350]
                },
                "jurisdiction": jurisdiction,
                "sufficiency": sufficiency,
                "recommended_action": "The Traditional Knowledge Demonstration Corpus confirms traditional documentation. Innovators should consider non-patent commercialization or defensive publication."
            }

    # MEDIUM sufficiency but no strong metadata match → requires review.
    # Cap sufficiency: distance measures textual similarity, not Section 3(p) relevance.
    # A close-but-domain-irrelevant chunk must never show a HIGH grounding bar next to 🔵.
    capped_sufficiency = "MEDIUM" if sufficiency == "HIGH" else sufficiency
    return {
        "module": "section_3p",
        "status": "🔵 No Direct Match in Searched Corpus",
        "evidence": f"No direct textual match for {main_ingredient} with claim '{intended_purpose}' was identified in the currently searched official corpus.",
        "citation": {
            "document": "Manual of Patent Office Practice and Procedure",
            "section": "Chapter 08.03.02 (Section 3(p) Examination)",
            "source_url": "file:///official_corpus/patent_office_manual.pdf#Chap08",
            "exact_text": "Where search results fail to show prior publication in codified traditional literature, applicants must still establish non-obvious technical advancement."
        },
        "jurisdiction": jurisdiction,
        "sufficiency": capped_sufficiency,
        "recommended_action": "No direct match found in searched static corpus. Does not guarantee patentability — official patent office prior-art search required."
    }


def retrieve_section_3p_evidence(
    intake: Dict[str, Any], jurisdiction: str
) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    """
    Executes metadata-filtered vector retrieval for Section 3(p) Traditional Knowledge screening.
    Applies strict jurisdiction filtering (India vs International vs Compare Both).

    Returns §6 contract-compliant object for India/International, or
    {"india": <result_object>, "international": <result_object>} for Compare Both.
    """
    if jurisdiction == "Compare Both":
        return {
            "india": _retrieve_section_3p_single(intake, "India"),
            "international": _retrieve_section_3p_single(intake, "International")
        }
    return _retrieve_section_3p_single(intake, jurisdiction)


def _retrieve_gap_navigator_single(intake: Dict[str, Any], jurisdiction: str) -> List[Dict[str, Any]]:
    """
    Internal helper: runs per-feature retrieval for a single jurisdiction.
    Returns a list of §6 gap_navigator_item objects.
    Results are strictly filtered to the given jurisdiction via Chroma metadata filter.
    """
    collection = get_chroma_collection()
    main_ingredient = intake.get("main_ingredient", "Ashwagandha")
    claims = intake.get("intended_purpose", "Stress support")
    process = intake.get("manufacturing_process", "Extract 10:1")

    features = [
        {"name": f"{main_ingredient} botanical ingredient", "query": f"{main_ingredient} botanical traditional uses"},
        {"name": f"{claims} claim", "query": f"{claims} therapeutic indication"},
        {"name": f"{process} technical process", "query": f"{process} extraction method technical contribution"}
    ]

    # Required: scope every query to the requested jurisdiction so Compare Both calls
    # return genuinely independent results, not the same unfiltered top-1 chunk twice.
    where_clause = {"jurisdiction": jurisdiction} if jurisdiction in ("India", "International") else None

    gap_items = []

    for f in features:
        res = collection.query(
            query_texts=[f["query"]],
            n_results=1,
            where=where_clause
        )
        docs = res["documents"][0] if res["documents"] else []
        metas = res["metadatas"][0] if res["metadatas"] else []
        distances = res["distances"][0] if "distances" in res and res["distances"] else [1.0]

        top_dist = distances[0] if distances else 1.0
        sufficiency = _sufficiency_from_distance(top_dist)

        if docs and metas:
            meta = metas[0]
            doc = docs[0]

            # Use distance threshold to determine status — replaces broken string check
            if sufficiency == "LOW":
                status = "🔵 No Direct Match in Searched Corpus"
                # No cap needed: LOW already conveys weak evidence
                effective_sufficiency = sufficiency
            elif "Monograph" in meta.get("section", "") or "API" in meta.get("act", ""):
                status = "🔴 Evidence Found"
                # Domain match confirmed — keep uncapped distance-based sufficiency
                effective_sufficiency = sufficiency
            else:
                status = "🟡 Requires Review"
                # Cap: textually-close but domain-irrelevant chunk must not show HIGH grounding
                effective_sufficiency = "MEDIUM" if sufficiency == "HIGH" else sufficiency

            gap_items.append({
                "module": "gap_navigator_item",
                "feature_name": f["name"],
                "status": status,
                "evidence": f"Retrieved excerpt from [{meta['act']} — {meta['section']}].",
                "citation": {
                    "document": meta["act"],
                    "section": meta["section"],
                    "source_url": meta["source_url"],
                    "exact_text": doc[:300]
                },
                "jurisdiction": jurisdiction,
                "sufficiency": effective_sufficiency
            })

    return gap_items


def retrieve_gap_navigator_evidence(
    intake: Dict[str, Any], jurisdiction: str
) -> Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
    """
    Parallel per-feature retrieval for Novelty & Innovation Gap Navigator.

    Returns a list of gap items for India/International, or
    {"india": [gap_items...], "international": [gap_items...]} for Compare Both.
    """
    if jurisdiction == "Compare Both":
        return {
            "india": _retrieve_gap_navigator_single(intake, "India"),
            "international": _retrieve_gap_navigator_single(intake, "International")
        }
    return _retrieve_gap_navigator_single(intake, jurisdiction)

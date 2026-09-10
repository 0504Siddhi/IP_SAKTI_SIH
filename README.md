# 🏛️ IP-SAKTI Sahayak

### Ayurveda Regulatory Intelligence & Intellectual Property Decision-Support Platform

> ⚠️ **Legal Disclaimer:** This prototype provides information, not legal advice. Verify outputs with official sources or a qualified professional before acting.

## 🎯 Overview

**IP-SAKTI Sahayak** is a citation-grounded decision-support prototype for Ayurveda product innovators, practitioners, and researchers.

It helps with:

- Regulatory classification across 7 product categories
- **Patents Act Section 3(p)** Traditional Knowledge screening
- Novelty & Innovation Gap analysis
- IPR route recommendations
- India / International jurisdiction-aware evidence retrieval
- Safe abstention when evidence is insufficient

## 🚨 Problem

Ayurveda innovators face:

- Complex and overlapping regulatory frameworks
- Difficulty identifying the correct regulatory pathway
- Traditional Knowledge and Section 3(p) patent concerns
- Limited access to structured, citation-backed regulatory intelligence

## 💡 Solution

IP-SAKTI combines **deterministic rule-based logic + LLM assistance + RAG** over a curated local statutory corpus.

```text
User Input
    ↓
LLM / Heuristic Structured Extraction
    ↓
Mandatory User Confirmation
    ↓
Deterministic Classification
    ↓
Jurisdiction-Filtered Chroma Retrieval
    ↓
Evidence + Gap Analysis
    ↓
LLM / Template Synthesis
    ↓
Safe Abstention Check
    ↓
Results Dashboard
```

### Core principle

> **Rules decide. Evidence supports. LLM explains.**

The LLM is not used to make the regulatory classification decision.

---

## ✨ Key Features

### 1. Deterministic Regulatory Classification

Pure Python decision tree with 7 output categories:

1. Classical / Generic ASU Medicine
2. Patent / Proprietary Ayurvedic Medicine
3. New / Non-Classical Drug
4. Phytopharmaceutical
5. Ayurveda-Aahar / Nutraceutical
6. Cosmetic
7. Insufficient Information

### 2. Section 3(p) Traditional Knowledge Screening

Retrieves jurisdiction-filtered evidence related to the Traditional Knowledge patent bar and returns:

- Evidence status
- Document
- Section
- Exact retrieved text
- Source URL
- Evidence sufficiency

### 3. Innovation Gap Navigator

Checks three independent dimensions:

- 🌿 Botanical ingredient
- 💊 Therapeutic claim
- ⚙️ Manufacturing process

### 4. Citation-Grounded RAG

A local **ChromaDB** knowledge base stores curated statutory and reference documents with metadata such as:

`act · section · jurisdiction · authority · topic · source_url`

The current corpus contains **12 documents** covering India and international sources.

### 5. Safe Abstention

The system avoids speculative answers when:

- An ingredient is unrecognized
- A claim is unsupported/non-empirical
- Retrieved evidence has low sufficiency

### 6. Human Confirmation Gate

Extracted product information is shown in an editable form before classification and retrieval.

### 7. IPR Recommendation Map

Provides preliminary routes for:

- Patent
- Trademark
- Design
- Trade Secret

### 8. Multi-language UI

English, Hindi, and Marathi selection is supported.

---

## 🧠 Technology Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Language | Python 3.9+ |
| LLM | Google Gemini 2.5 Flash |
| Vector DB | ChromaDB |
| Classification | Pure Python |
| Styling | Vanilla CSS |
| Image Handling | Pillow |
| Data Processing | Pandas |
| Testing | Python unittest / pytest commands |

---

## 🏗️ Architecture

```text
ip_sakti_sahayak/
│
├── app.py            # Streamlit UI and workflow
├── classifier.py     # Deterministic classification + normalization
├── extractor.py      # Gemini / heuristic extraction
├── retriever.py      # RAG retrieval + Section 3(p) + gap analysis
├── synthesizer.py    # Synthesis + safe abstention
├── corpus_data.py    # Curated statutory corpus
├── chunker.py        # Metadata-aware document chunking
├── ingest.py         # ChromaDB ingestion
├── mock_data.py      # Offline/mock data
├── styles.css        # UI styling
├── requirements.txt
│
└── tests/
    ├── golden_tests.py
    ├── test_classifier.py
    ├── test_extractor.py
    ├── test_retriever.py
    ├── test_synthesizer.py
    └── test_retrieval.py
```

---

## 📚 Knowledge Base

The prototype currently uses a curated corpus including:

- Patents Act, 1970 — Section 3(p)
- Patent Rules, 2003
- Patent Office Practice and Procedure Manual
- Drugs and Cosmetics Act, 1940
- Drugs and Cosmetics Rules, 1945
- Biological Diversity Act, 2002
- FSSAI Ayurveda Aahara Regulations, 2022
- WIPO GRATK Treaty 2024
- WTO TRIPS Agreement
- Ayurvedic Pharmacopoeia of India monographs
- CSIR vs USPTO turmeric patent case

Retrieval is **jurisdiction-scoped** to prevent unintended India/International evidence mixing.

---

## 🚀 Setup & Run

### 1. Clone

```bash
git clone https://github.com/0504Siddhi/IP_SAKTI_SIH.git
cd IP_SAKTI_SIH
```

### 2. Create environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Optional: Gemini API

Set `GEMINI_API_KEY` to enable Gemini-powered extraction and synthesis.

Without the key, the prototype uses its built-in heuristic/template fallbacks.

### 5. Build the local knowledge base

```bash
python ingest.py
```

### 6. Start the application

```bash
streamlit run app.py
```

The app runs locally at:

```text
http://localhost:8501
```

---

## 🧪 Testing

Run the main test suites with:

```bash
python -m pytest test_classifier.py -v
python -m pytest test_extractor.py -v
python -m pytest test_retriever.py -v
python -m pytest test_synthesizer.py -v
python -m pytest golden_tests.py -v
```

The golden tests cover examples such as:

- Ashwagandha formulation
- Classical Chyawanprash
- Purified botanical fraction
- Synthetic drug
- Unrecognized ingredient → Safe Abstention
- International jurisdiction retrieval

---

## 🔐 Important Design Decisions

### No speculative LLM classification

Regulatory classification is deterministic and auditable.

### Mandatory confirmation

Users can review and correct extracted parameters before analysis.

### Safe Abstention

The system can explicitly say that available evidence is insufficient instead of generating a confident unsupported answer.

### Citation traceability

Evidence carries document, section, source URL, and retrieved text.

### Offline-first

Core classification and local retrieval work without an external LLM API.

---

## 🔮 Future Scope

The current architecture can be extended with:

- Real OCR / vision integration for product labels
- Larger statutory and Ayurvedic corpus
- Full ABS compliance workflow
- Side-by-side India vs International comparison
- Expanded ingredient normalization
- Structured PDF/report export

These are **future extensions, not current implemented features**.

---

## 🏆 Smart India Hackathon

**Problem Statement:** 26045  
**Project:** IP-SAKTI Sahayak  
**Focus:** Multilingual, RAG-based, source-cited AI assistance for Intellectual Property and regulatory guidance in Ayurveda.

---

## ⚖️ Disclaimer

IP-SAKTI Sahayak is a **prototype decision-support system**, not a substitute for legal, regulatory, or professional advice.

Always verify important conclusions against the relevant official source or consult a qualified professional.

---

<div align="center">

**IP-SAKTI Sahayak**  
*Regulatory & IPR Decision-Support Infrastructure for Ayurveda*

**Built for Smart India Hackathon (SIH)**

</div>

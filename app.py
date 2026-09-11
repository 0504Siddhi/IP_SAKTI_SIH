import streamlit as st
import os
import mock_data

# Import Deterministic Classification Engine & Normalization (Step 2)
from classifier import classify_formulation, normalize_ingredient

# Import LLM Structured Extraction Module (Step 3)
from extractor import extract_structured_intake

# Import Retrieval Engine (Step 4)
from retriever import retrieve_section_3p_evidence, retrieve_gap_navigator_evidence

# Import LLM Synthesis & Safe Abstention Engine (Step 5 & Step 6)
from synthesizer import synthesize_results, check_sufficiency, pick_primary_side

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="IP-SAKTI Sahayak — Regulatory & IPR Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "welcome"
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "EN"
if "jurisdiction" not in st.session_state:
    st.session_state.jurisdiction = "India"
if "intake_data" not in st.session_state:
    st.session_state.intake_data = dict(mock_data.MOCK_EXTRACTED_INTAKE)
if "active_citation" not in st.session_state:
    st.session_state.active_citation = None
if "qa_query" not in st.session_state:
    st.session_state.qa_query = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "screen_history" not in st.session_state:
    st.session_state.screen_history = []

# Load Custom CSS System & Theme Overrides
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # Inject Light Mode Overrides
    if not st.session_state.dark_mode:
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #F7F8FA !important;
                    color: #1A2332 !important;
                }
                .sakti-card, .top-header-bar, .hero-gradient-container {
                    background: #FFFFFF !important;
                    color: #1A2332 !important;
                    border-color: rgba(0, 0, 0, 0.1) !important;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
                }
                .brand-title, .sakti-card-title, h1, h2, h3, h4, h5, h6 {
                    color: #1A2332 !important;
                }
                .brand-subtitle, p, li, caption {
                    color: #5A6472 !important;
                }
                .stat-item {
                    background: #F0F4F8 !important;
                    border-color: rgba(0, 0, 0, 0.08) !important;
                }
                .sufficiency-widget {
                    background: #EDF1F7 !important;
                }
                .glassmorphism-side-panel {
                    background: rgba(255, 255, 255, 0.95) !important;
                    border-color: #2B5C8A !important;
                    color: #1A2332 !important;
                }
            </style>
            """, unsafe_allow_html=True
        )

load_css()

def navigate_to(screen_name, track_history=True):
    if "draft_product_text" in st.session_state and st.session_state.draft_product_text:
        st.session_state["_saved_draft_product_text"] = st.session_state.draft_product_text
    if "draft_innovation_text" in st.session_state and st.session_state.draft_innovation_text:
        st.session_state["_saved_draft_innovation_text"] = st.session_state.draft_innovation_text
    if track_history and st.session_state.current_screen != screen_name:
        st.session_state.screen_history.append(st.session_state.current_screen)
    st.session_state.current_screen = screen_name
    st.rerun()

def navigate_back():
    if st.session_state.screen_history:
        prev = st.session_state.screen_history.pop()
        navigate_to(prev, track_history=False)

def render_back_button():
    if st.session_state.screen_history:
        if st.button("← Back", key=f"btn_back_{st.session_state.current_screen}"):
            navigate_back()

# Screen 0 Header with Monogram, Devanagari Language Selector, and Light/Dark Mode Toggle
def render_screen_0_header():
    col1, col2, col3 = st.columns([3.2, 1.2, 0.8])
    with col1:
        st.markdown(
            '<div class="top-header-bar"><div class="brand-container"><div class="brand-monogram"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#B8703C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.4 19 2c1 2 2 4.1 2 7 0 6-4.5 11-10 11z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12" stroke="#388BFD"/></svg></div><div><div class="brand-title">IP-SAKTI Sahayak</div><div class="brand-subtitle">Regulatory &amp; Intellectual Property Decision-Support Infrastructure</div></div></div><div class="corpus-status-pill"><div class="corpus-pulse-dot"></div>CORPUS INDEXED · STATIC v1</div></div>',
            unsafe_allow_html=True
        )
    with col2:
        lang = st.selectbox(
            "Language",
            ["English (EN)", "हिंदी (Hindi)", "मराठी (Marathi)"],
            index=0,
            key="lang_select_dropdown"
        )
        if "हिंदी" in lang:
            st.session_state.selected_language = "HI"
        elif "मराठी" in lang:
            st.session_state.selected_language = "MR"
        else:
            st.session_state.selected_language = "EN"
            
    with col3:
        st.markdown("<div style='margin-top: 1.6rem;'>", unsafe_allow_html=True)
        theme_label = "🌙 Dark Mode" if st.session_state.dark_mode else "☀️ Light Mode"
        if st.button(theme_label, key="btn_theme_toggle", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Screen 0 Permanent Non-Dismissible Legal Disclaimer Banner (#F4F1E8 bg / #5A5548 text)
def render_screen_0_bottom_banner():
    st.markdown(
        '<div class="persistent-disclaimer-banner"><span>⚠️ <strong>Legal Disclaimer:</strong> This tool provides information, not legal advice. Verify with an official source or a qualified professional before acting.</span></div>',
        unsafe_allow_html=True
    )

# Evidence Status Badge Generator (🟢 · 🔴 #C0392B · 🟡 #B7860B · 🔵 #2874A6)
def render_status_badge(status_str):
    """Renders a coloured badge whose visible text matches the actual status_str."""
    if "🟢" in status_str or "Recommended" in status_str:
        return f'<span class="badge-green">{status_str}</span>'
    elif "🔴" in status_str or "Evidence Found" in status_str:
        return f'<span class="badge-red">{status_str}</span>'
    elif "🟡" in status_str or "Requires Review" in status_str:
        return f'<span class="badge-yellow">{status_str}</span>'
    else:
        return f'<span class="badge-blue">{status_str}</span>'

# Evidence Sufficiency Meter Widget Component with Animation
def render_sufficiency_meter(level_str):
    level = level_str.upper()
    if level == "HIGH":
        segments = '<div class="sufficiency-segment segment-active-high"></div><div class="sufficiency-segment segment-active-high"></div><div class="sufficiency-segment segment-active-high"></div>'
        color = "#27AE60"
    elif level == "MEDIUM":
        segments = '<div class="sufficiency-segment segment-active-med"></div><div class="sufficiency-segment segment-active-med"></div><div class="sufficiency-segment"></div>'
        color = "#F39C12"
    else:
        segments = '<div class="sufficiency-segment segment-active-low"></div><div class="sufficiency-segment"></div><div class="sufficiency-segment"></div>'
        color = "#E74C3C"
        
    return f'<div class="sufficiency-widget"><div class="sufficiency-header"><span>GROUNDING SUFFICIENCY</span><span style="color: {color}; font-weight: 700;">{level}</span></div><div class="sufficiency-track">{segments}</div></div>'

# Evidence Confidence Bar — thin progress bar for Gap Navigator items
# Uses existing fixed status hex colors (#C0392B / #B7860B / #2874A6)
def render_confidence_bar(sufficiency: str, status_str: str) -> str:
    level = sufficiency.upper() if sufficiency else "MEDIUM"
    # Pick fill % by sufficiency level
    if level == "HIGH":
        pct = 92
    elif level == "MEDIUM":
        pct = 58
    else:
        pct = 15

    # Pick color from existing fixed status hex values
    if "🔴" in status_str or "Evidence Found" in status_str:
        bar_color = "#C0392B"
    elif "🟡" in status_str or "Requires Review" in status_str:
        bar_color = "#B7860B"
    else:
        bar_color = "#2874A6"

    return (
        f'<div class="evidence-confidence-wrap">'
        f'<span class="evidence-confidence-label">Evidence Confidence</span>'
        f'<div class="evidence-confidence-track">'
        f'<div class="evidence-confidence-fill" style="width:{pct}%; background-color:{bar_color};"></div>'
        f'</div>'
        f'</div>'
    )

# ==========================================
# SCREEN 1: Welcome / Home Screen
# ==========================================
def render_screen_1_welcome():
    render_screen_0_header()
    render_back_button()
    
    st.markdown(
        '<div class="hero-gradient-container"><div class="hero-content"><div style="font-size: 0.8rem; font-weight: 700; color: var(--accent-terracotta); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem;">AYURVEDA REGULATORY INTELLIGENCE PLATFORM</div><div class="gradient-headline">Ayurveda IP & Regulatory Decision Support</div><p style="color: var(--text-muted); font-size: 1rem; max-width: 780px; line-height: 1.55; margin-bottom: 0;">Evaluate traditional product pathways, analyze Section 3(p) Traditional Knowledge patent-bar exposure, and verify statutory evidence across national and international legal regimes.</p><div class="stat-strip-container"><div class="stat-item"><div class="stat-number">7 Core Statutes</div><div class="stat-label">Tier-1 Acts & Regulations Scope</div></div><div class="stat-item"><div class="stat-number">2 Regimes</div><div class="stat-label">India & International Separation</div></div><div class="stat-item"><div class="stat-number">Citation-Verified</div><div class="stat-label">Every Answer Traceable to Source</div></div></div></div></div>',
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="sakti-card sakti-card-interactive" style="height: 100%;"><div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;"><div style="background: rgba(56, 139, 253, 0.15); border: 1px solid rgba(56, 139, 253, 0.3); border-radius: 6px; padding: 0.4rem; display: flex;"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#388BFD" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div><div style="font-size: 0.78rem; font-weight: 700; color: var(--accent-blue-bright); text-transform: uppercase; letter-spacing: 0.05em;">PATHWAY A — FORMULATION ANALYSIS</div></div><div class="sakti-card-title">I Have a Product / Innovation</div><p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.5rem;">Perform multi-parameter formulation classification, route regulatory domain, and execute metadata-filtered Section 3(p) prior-art risk screening.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Proceed with Product Analysis →", key="btn_path_a", use_container_width=True, type="primary"):
            navigate_to("jurisdiction")
            
    with col2:
        st.markdown(
            '<div class="sakti-card sakti-card-interactive" style="height: 100%;"><div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;"><div style="background: rgba(226, 155, 99, 0.15); border: 1px solid rgba(226, 155, 99, 0.3); border-radius: 6px; padding: 0.4rem; display: flex;"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E29B63" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div><div style="font-size: 0.78rem; font-weight: 700; color: var(--accent-terracotta-bright); text-transform: uppercase; letter-spacing: 0.05em;">PATHWAY B — DIRECT Q&A</div></div><div class="sakti-card-title">I Have a Question</div><p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.5rem;">Query official statutory provisions, Patent Office Practice Manuals, FSSAI Ayurveda-Aahar regulations, or international WIPO/TRIPS treaties directly.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Query Statutory Knowledge Base →", key="btn_path_b", use_container_width=True):
            navigate_to("direct_qa")

    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 2: Jurisdiction Selection
# ==========================================
def render_screen_2_jurisdiction():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Jurisdiction Selection")
    st.write("Select legal jurisdiction for search space scoping:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("India Jurisdiction", use_container_width=True, type="primary" if st.session_state.jurisdiction == "India" else "secondary"):
            st.session_state.jurisdiction = "India"
            navigate_to("entry_mode")
    with col2:
        if st.button("International Jurisdiction", use_container_width=True, type="primary" if st.session_state.jurisdiction == "International" else "secondary"):
            st.session_state.jurisdiction = "International"
            navigate_to("entry_mode")
    with col3:
        if st.button("Compare Both Regimes", use_container_width=True, type="primary" if st.session_state.jurisdiction == "Compare Both" else "secondary"):
            st.session_state.jurisdiction = "Compare Both"
            navigate_to("entry_mode")
            
    st.caption("Jurisdiction filter restricts document retrieval to national vs international legal sources without cross-blending.")
    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 3: Entry Mode Selection
# ==========================================
def render_screen_3_entry_mode():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Product Intake Method")
    st.write("Select product or innovation input method:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="sakti-card sakti-card-interactive"><div class="sakti-card-title">Describe Product (Text)</div><p style="color: var(--text-muted); font-size: 0.85rem;">Input product composition, ingredients, administration route, and therapeutic claims.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Text Entry →", key="btn_describe_text", use_container_width=True):
            navigate_to("describe_product")
            
    with col2:
        st.markdown(
            '<div class="sakti-card sakti-card-interactive"><div class="sakti-card-title">Scan Product Label <span style="font-size:0.75rem; color: var(--text-muted);">(Optional)</span></div><p style="color: var(--text-muted); font-size: 0.85rem;">Upload product packaging or label image for vision-OCR extraction.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Photo Scan →", key="btn_scan_photo", use_container_width=True):
            navigate_to("scan_product")
            
    with col3:
        st.markdown(
            '<div class="sakti-card sakti-card-interactive"><div class="sakti-card-title">Describe Innovation</div><p style="color: var(--text-muted); font-size: 0.85rem;">Specify technical process modifications, novel extraction methods, or novel ratios.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Innovation Entry →", key="btn_describe_innov", use_container_width=True):
            navigate_to("describe_innovation")

    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 4A: Describe Product (Step 3 Structured Extraction)
# ==========================================
def render_screen_4a_describe_product():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Product Formulation Specification")
    st.write("Enter product details for LLM parameter extraction:")
    
    user_text = st.text_area(
        "Product Description",
        value=st.session_state.get("draft_product_text") or st.session_state.get("_saved_draft_product_text", ""),
        key="draft_product_text",
        height=140
    )
    
    if st.button("Execute LLM Extraction →", type="primary"):
        with st.spinner("Extracting Universal-7 parameters into strict JSON..."):
            extracted = extract_structured_intake(user_text)
            st.session_state.intake_data.update(extracted)
            navigate_to("confirm_intake")
        
    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 4B: Scan Product
# ==========================================
def render_screen_4b_scan_product():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Product Label OCR Scan")
    st.write("Upload product label image for entity extraction:")
    
    uploaded_file = st.file_uploader("Upload Product Label Image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    st.info("Label text will be extracted into structured JSON. Mandatory confirmation required before rule execution.")
    
    if st.button("Run OCR & Extract JSON →", type="primary"):
        ocr_simulated_text = "Ashwagandha capsule 10:1 hydro-alcoholic extract for stress support oral administration"
        extracted = extract_structured_intake(ocr_simulated_text)
        st.session_state.intake_data.update(extracted)
        navigate_to("confirm_intake")
        
    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 4C: Describe Innovation
# ==========================================
def render_screen_4c_describe_innovation():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Describe My Innovation")
    st.write("Tell us about your idea in your own words — our system will analyse it for regulatory classification and IP risk screening.")
    
    user_text = st.text_area(
        "Describe your innovation",
        value=st.session_state.get("draft_innovation_text") or st.session_state.get("_saved_draft_innovation_text", ""),
        key="draft_innovation_text",
        placeholder="e.g. A new extraction process for Ashwagandha to improve absorption.",
        height=140
    )
    
    if st.button("Extract & Continue →", type="primary"):
        with st.spinner("Extracting parameters into structured JSON..."):
            extracted = extract_structured_intake(user_text)
            st.session_state.intake_data.update(extracted)
            navigate_to("confirm_intake")
        
    render_screen_0_bottom_banner()


# ==========================================
# SCREEN 5: Mandatory User Confirmation Form (Step 3 Mandatory Gate)
# ==========================================
def render_screen_5_confirm_intake():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Structured Data Confirmation (Mandatory Confirmation Screen)")
    st.info("Mandatory Gate: Confirm or edit AI-extracted formulation parameters before deterministic rule evaluation.")
    
    intake = st.session_state.intake_data
    
    with st.form("intake_confirmation_form"):
        col1, col2 = st.columns(2)
        with col1:
            prod_name = st.text_input("Product Name", value=intake.get("product_name", "Ashwagandha Formulation"))
            main_ing = st.text_input("Main Ingredient", value=intake.get("main_ingredient", "Ashwagandha"))
            sci_name = st.text_input("Botanical / Scientific Name", value=intake.get("scientific_name", "Withania somnifera"))
            plant_part = st.text_input("Plant Part Used", value=intake.get("plant_part", "Root"))
        with col2:
            form_opt = ["Capsule", "Tablet", "Powder / Churna", "Oil", "Extract", "Liquid", "Beverage", "Other"]
            current_form = intake.get("product_form", "Capsule")
            form_idx = form_opt.index(current_form) if current_form in form_opt else 0
            prod_form = st.selectbox("Product Dosage Form", form_opt, index=form_idx)
            
            intended_purp = st.text_input("Intended Purpose / Claim", value=intake.get("intended_purpose", "Stress support"))
            
            route_opt = ["Oral", "Topical", "External", "Parenteral / Injection", "Other"]
            current_route = intake.get("route_of_use", "Oral")
            route_idx = route_opt.index(current_route) if current_route in route_opt else 0
            route_use = st.selectbox("Route of Administration", route_opt, index=route_idx)
            
            target_opt = ["General adults", "Children", "Elderly", "Pregnant/lactating", "Specific"]
            current_target = intake.get("target_user", "General adults")
            target_idx = target_opt.index(current_target) if current_target in target_opt else 0
            user_target = st.selectbox("Target User Population", target_opt, index=target_idx)
            
        st.markdown("##### Missing Field Resolution")
        st.write("Manufacturing process details status: " + intake.get("manufacturing_process", "Hydro-alcoholic solvent extraction"))
        missing_choice = st.radio("Resolve missing parameter:", ["I know it → fill in", "I'm not sure", "I don't know (Proceed with reduced confidence)"], index=2)
        
        btn_confirm = st.form_submit_button("✅ Confirm Data & Run Classification Engine →", type="primary")
        
        if btn_confirm:
            st.session_state.intake_data["product_name"] = prod_name
            st.session_state.intake_data["main_ingredient"] = main_ing
            st.session_state.intake_data["scientific_name"] = sci_name
            st.session_state.intake_data["product_form"] = prod_form
            st.session_state.intake_data["intended_purpose"] = intended_purp
            st.session_state.intake_data["route_of_use"] = route_use
            st.session_state.intake_data["target_user"] = user_target
            navigate_to("processing")

    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 6: Processing Screen
# ==========================================
def render_screen_6_processing():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Execution Pipeline")
    
    with st.spinner("Evaluating formulation matrix & executing parallel vector search..."):
        st.markdown(
            '<div class="sakti-card"><div style="color: var(--accent-primary); font-weight: 700;">Deterministic Rule Engine & Retrieval Pipeline</div><ol style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.8; margin-top: 0.5rem;"><li>Running Python formulation classification tree (7 categories)</li><li>Applying Jurisdiction & Authority-level metadata filters</li><li>Retrieving parallel batched contexts from local Chroma DB</li><li>Validating citation grounding and safe abstention threshold</li></ol></div>',
            unsafe_allow_html=True
        )
        
        # Run real multi-stage engine pipeline
        classification = classify_formulation(st.session_state.intake_data)
        retrieval_3p = retrieve_section_3p_evidence(st.session_state.intake_data, st.session_state.jurisdiction)
        gap_items = retrieve_gap_navigator_evidence(st.session_state.intake_data, st.session_state.jurisdiction)
        synthesis = synthesize_results(st.session_state.intake_data, classification, retrieval_3p, gap_items, st.session_state.jurisdiction)
        
        st.session_state.synthesis_result = synthesis
        
        if synthesis.get("should_abstain"):
            st.session_state.abstention_reason = synthesis.get("abstain_reason")
            if st.button("⚠️ Evidence Insufficient — View Safe Abstention Screen →", type="primary", use_container_width=True):
                navigate_to("abstention")
        else:
            if st.button("View Classification & Statutory Evidence Result →", type="primary", use_container_width=True):
                navigate_to("classification_result")
            
    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 7: Classification Result (Terracotta Top Accent & Step 2 Deterministic Logic)
# ==========================================
def render_screen_7_classification_result():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Preliminary Regulatory Classification")
    
    # Step 2 Real Deterministic Evaluation Call
    res = classify_formulation(st.session_state.intake_data)
    
    reasons_html = "".join([f"<li>{r}</li>" for r in res['reasons']])
    st.markdown(
        f'<div class="sakti-card sakti-card-terracotta-accent"><div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-terracotta); font-weight: 700;">PRELIMINARY ROUTING RESULT (DETERMINISTIC PYTHON ENGINE)</div><h2 style="font-size: 1.6rem; margin-top: 0.25rem;">Category: {res["category"]}</h2><div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem; font-weight: 500;">Deterministic Rule Basis:</div><ul style="color: var(--text-primary); font-size: 0.9rem; line-height: 1.6; margin-top: 0.25rem;">{reasons_html}</ul><div style="margin-top: 1rem; font-size: 0.82rem; color: #F1C40F; background: rgba(183, 134, 11, 0.12); padding: 0.65rem; border-radius: 4px; border: 1px solid rgba(183, 134, 11, 0.3);">⚠️ {res["disclaimer"]}</div></div>',
        unsafe_allow_html=True
    )
    
    if st.button("View Full Guidance & Section 3(p) Evidence →", type="primary", use_container_width=True):
        navigate_to("main_results")

    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 8 & 8b: Main Results & Citation Rail (Asymmetric Layout)
# ==========================================
def _render_jurisdiction_panel(sec_3p: dict, gap_items: list, label: str, panel_key_prefix: str):
    """
    Helper: renders a single-jurisdiction Section 3(p) + Gap Navigator block.
    Called twice for Compare Both, once for single-jurisdiction mode.
    """
    if label:
        st.markdown(f"**{label}**")

    badge_html = render_status_badge(sec_3p["status"])
    st.markdown(
        f'<div class="sakti-card"><div class="sakti-card-title">Status: {badge_html}</div>'
        f'<p style="color: var(--text-primary); font-size: 0.92rem; line-height: 1.55;">{sec_3p["evidence"]}</p>'
        f'<div style="margin-top: 0.75rem;"><span style="font-size: 0.8rem; color: var(--text-muted);">Traceable Citation:</span></div></div>',
        unsafe_allow_html=True
    )
    cit = sec_3p["citation"]
    if st.button(f"📑 [{cit['document']} — {cit['section']}]", key=f"btn_cit_3p_{panel_key_prefix}"):
        st.session_state.active_citation = cit

    st.markdown("<div class='tkdl-note'>🟡 Traditional Knowledge Demonstration Corpus — illustrative, not TKDL. Disclosed sample database.</div>", unsafe_allow_html=True)

    if gap_items:
        st.markdown("**Novelty & Innovation Gap Navigator**")
        for idx, item in enumerate(gap_items):
            col_a, col_b, col_c = st.columns([2, 2.4, 0.7])
            with col_a:
                st.markdown(f"**{item['feature_name']}**")
            with col_b:
                item_status = item["status"]
                item_sufficiency = item.get("sufficiency", "MEDIUM")
                st.markdown(
                    render_status_badge(item_status) + render_confidence_bar(item_sufficiency, item_status),
                    unsafe_allow_html=True
                )
            with col_c:
                if st.button("Evidence", key=f"btn_gap_{panel_key_prefix}_{idx}"):
                    st.session_state.active_citation = item["citation"]
            st.caption(item["evidence"])
            st.markdown("<hr style='margin: 0.4rem 0; border-color: var(--border-subtle);'>", unsafe_allow_html=True)


def render_screen_8_main_results():
    render_screen_0_header()
    render_back_button()

    st.markdown("### Statutory Evidence & Compliance Dashboard")

    # Check if real synthesis result exists in session state
    synth = st.session_state.get("synthesis_result")
    classification = {}
    if synth and not synth.get("should_abstain"):
        sec_3p_raw = synth["section_3p"]
        gap_items_raw = synth["gap_navigator"]
        exec_summary = synth.get("executive_summary", "")
        classification = synth.get("classification", {})
    else:
        sec_3p_raw = mock_data.MOCK_SECTION_3P_INDIA if "International" not in st.session_state.jurisdiction else mock_data.MOCK_SECTION_3P_INTERNATIONAL
        gap_items_raw = mock_data.MOCK_GAP_NAVIGATOR_ITEMS
        exec_summary = ""

    # Detect Compare Both shape: {"india": {...}, "international": {...}}
    is_compare_both = isinstance(sec_3p_raw, dict) and "india" in sec_3p_raw and "international" in sec_3p_raw

    if exec_summary:
        st.markdown(
            f'<div class="sakti-card" style="border-left: 4px solid var(--accent-blue); background: rgba(43, 92, 138, 0.08); margin-bottom: 1rem;">'
            f'<div style="font-weight: 700; color: var(--accent-blue-bright); font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">EXECUTIVE REGULATORY SUMMARY</div>'
            f'<p style="color: var(--text-primary); font-size: 0.92rem; margin-top: 0.3rem; margin-bottom: 0;">{exec_summary}</p></div>',
            unsafe_allow_html=True
        )

    # Asymmetric 2-Column Layout (Wider Content + Side Rail)
    main_col, side_rail = st.columns([2.3, 1.1])

    with main_col:
        # ----------------------------------------------------------------
        # Section 1: Section 3(p) Check
        # ----------------------------------------------------------------
        st.markdown("#### 1. Section 3(p) Traditional Knowledge Patent-Bar Check")

        if is_compare_both:
            # Compare Both: two clearly separate India | International panels
            india_gap = gap_items_raw.get("india", []) if isinstance(gap_items_raw, dict) else []
            intl_gap = gap_items_raw.get("international", []) if isinstance(gap_items_raw, dict) else []
            india_col, intl_col = st.columns(2)
            with india_col:
                _render_jurisdiction_panel(sec_3p_raw["india"], india_gap, "🇮🇳 India", "india")
            with intl_col:
                _render_jurisdiction_panel(sec_3p_raw["international"], intl_gap, "🌍 International", "intl")
            # Primary side for the side-rail Grounding Sufficiency Meter.
            # MUST use pick_primary_side() to stay in sync with synthesize_results()
            # executive summary selection — hardcoding India here would show a contradictory
            # sufficiency level when International is stronger.
            _india_suff = sec_3p_raw["india"].get("sufficiency", "HIGH")
            _intl_suff  = sec_3p_raw["international"].get("sufficiency", "HIGH")
            _primary    = pick_primary_side(_india_suff, _intl_suff)
            primary_sufficiency = _india_suff if _primary == "india" else _intl_suff
        else:
            # Single jurisdiction
            _render_jurisdiction_panel(sec_3p_raw, [], "", "single")
            # Section 2: Innovation Gap Navigator (single-jurisdiction only; Compare Both embeds it above)
            st.markdown("---")
            st.markdown("#### 2. Novelty & Innovation Gap Navigator")
            gap_items_list = gap_items_raw if isinstance(gap_items_raw, list) else []
            for idx, item in enumerate(gap_items_list):
                col_a, col_b, col_c = st.columns([2, 2.4, 0.7])
                with col_a:
                    st.markdown(f"**{item['feature_name']}**")
                with col_b:
                    item_status = item["status"]
                    item_sufficiency = item.get("sufficiency", "MEDIUM")
                    st.markdown(
                        render_status_badge(item_status) + render_confidence_bar(item_sufficiency, item_status),
                        unsafe_allow_html=True
                    )
                with col_c:
                    if st.button("Evidence", key=f"btn_gap_main_{idx}"):
                        st.session_state.active_citation = item["citation"]
                st.caption(item["evidence"])
                st.markdown("<hr style='margin: 0.4rem 0; border-color: var(--border-subtle);'>", unsafe_allow_html=True)
            primary_sufficiency = sec_3p_raw.get("sufficiency", "HIGH") if isinstance(sec_3p_raw, dict) else "HIGH"

        # ----------------------------------------------------------------
        # Section 3: Core IPR Recommendation Map
        # ----------------------------------------------------------------
        st.markdown("---")
        st.markdown("#### 3. Core IPR Recommendation Map")

        # Build display map — overlay Patent row dynamically based on real classification result
        display_ip_map = [dict(entry) for entry in mock_data.MOCK_IP_MAP]
        if classification.get("section_3p_flag") and not is_compare_both:
            # Determine real 3(p) status from single-jurisdiction result
            real_status = sec_3p_raw.get("status", "") if isinstance(sec_3p_raw, dict) else ""
            if real_status == "🔴 Evidence Found":
                for entry in display_ip_map:
                    if entry["ip_type"] == "Patent":
                        entry["status"] = "🔴 Evidence Found"
                        entry["description"] = (
                            "Section 3(p) Traditional Knowledge evidence confirmed in corpus. "
                            "This formulation is likely excluded from patent protection under Section 3(p) of Patents Act, 1970."
                        )

        grid_a, grid_b = st.columns(2)
        for idx, ip in enumerate(display_ip_map):
            target_col = grid_a if idx % 2 == 0 else grid_b
            with target_col:
                st.markdown(
                    f'<div class="sakti-card sakti-card-interactive">'
                    f'<div style="font-weight: 700; color: var(--text-primary); font-size: 0.95rem;">{ip["ip_type"]}</div>'
                    f'<div style="margin: 0.3rem 0;">{render_status_badge(ip["status"])}</div>'
                    f'<p style="color: var(--text-muted); font-size: 0.82rem; margin-top: 0.3rem;">{ip["description"]}</p></div>',
                    unsafe_allow_html=True
                )

        # ----------------------------------------------------------------
        # Issue 5 — ABS Compliance Flag Card
        # ----------------------------------------------------------------
        if classification.get("abs_flag"):
            st.markdown(
                '<div class="sakti-card" style="border-left: 4px solid #F39C12; background: rgba(243,156,18,0.07); margin-top: 0.5rem;">'
                '<div style="font-weight: 700; color: #F39C12; font-size: 0.9rem;">'
                '⚠️ Biological Resource / ABS Compliance Flag</div>'
                '<p style="color: var(--text-primary); font-size: 0.88rem; line-height: 1.55; margin-top: 0.4rem; margin-bottom: 0;">'
                "This product's ingredients may be sourced from Indian biological resources, which can trigger "
                'Access-and-Benefit-Sharing considerations under the Biological Diversity Act. '
                'This is a compliance-routing flag, not a final determination.</p></div>',
                unsafe_allow_html=True
            )

    with side_rail:
        st.markdown("#### Evidence & Action Rail")

        # Evidence Sufficiency Meter Widget
        st.markdown(render_sufficiency_meter(primary_sufficiency), unsafe_allow_html=True)

        # Next Steps Box
        st.markdown(
            '<div class="sakti-card"><div class="sakti-card-title" style="font-size: 0.95rem;">Required Next Actions</div>'
            '<ul style="color: var(--text-primary); font-size: 0.85rem; padding-left: 1rem; line-height: 1.5;">'
            '<li>Verify Section 3(p) prior-art evidence against official patent office manuals</li>'
            '<li>File trademark application for brand protection</li>'
            '<li>Consult registered patent practitioner for specification drafting</li></ul></div>',
            unsafe_allow_html=True
        )

        # Terracotta Accent Escalation Button
        st.markdown("<div style='margin-bottom: 0.75rem;'>", unsafe_allow_html=True)
        if st.button("Talk to a Human Expert →", key="btn_escalate_rail", use_container_width=True):
            navigate_to("escalation")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🛡️ Demonstrate Safe Abstention View", key="btn_abstain_rail", use_container_width=True):
            navigate_to("abstention")

        # SCREEN 8B: Reserved Glassmorphism Citation Panel Overlay (With Glow & Sweep Animation)
        if st.session_state.active_citation:
            st.markdown("---")
            active_cit = st.session_state.active_citation
            st.markdown(
                f'<div class="glassmorphism-side-panel"><div style="color: #58A6FF; font-weight: 700; font-size: 0.95rem; font-family: \'Space Grotesk\', sans-serif;">📑 RETRIEVED STATUTORY EXCERPT</div>'
                f'<div style="color: var(--text-primary); font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.4;"><strong>Document:</strong> {active_cit["document"]}<br><strong>Section:</strong> {active_cit["section"]}</div>'
                f'<div class="exact-source-highlight">"{active_cit["exact_text"]}"</div>'
                f'<div style="color: var(--text-muted); font-size: 0.75rem;">Level A — Primary Statutory Authority</div></div>',
                unsafe_allow_html=True
            )
            if st.button("Close Citation Panel", key="btn_close_panel", use_container_width=True):
                st.session_state.active_citation = None
                st.rerun()

    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 9: Direct Q&A Path
# ==========================================
def render_screen_9_direct_qa():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Statutory Knowledge Base Query")
    st.write("Query official Indian or International legal sources directly:")
    
    user_query = st.text_input(
        "Enter statutory question:",
        value=st.session_state.qa_query,
        placeholder="e.g. Can traditional Ayurvedic knowledge be patented under Section 3(p)?"
    )
    
    st.write("Sample Query Prompts:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Section 3(p) Patent Exclusions", use_container_width=True):
            st.session_state.qa_query = "Can I patent a classical formulation?"
            st.rerun()
    with col2:
        if st.button("FSSAI Ayurveda-Aahar Rules", use_container_width=True):
            st.session_state.qa_query = "What is Ayurveda-Aahar?"
            st.rerun()
    with col3:
        if st.button("Biological Diversity ABS Rules", use_container_width=True):
            st.session_state.qa_query = "Do I need ABS approval?"
            st.rerun()

    if st.button("Execute Statutory Search →", type="primary") or user_query:
        st.markdown("---")
        st.markdown("#### Citation-Grounded Answer")
        st.markdown(render_status_badge(mock_data.MOCK_SECTION_3P_INDIA["status"]), unsafe_allow_html=True)
        st.markdown(render_sufficiency_meter(mock_data.MOCK_SECTION_3P_INDIA["sufficiency"]), unsafe_allow_html=True)
        st.write(mock_data.MOCK_SECTION_3P_INDIA["evidence"])
        
        cit = mock_data.MOCK_SECTION_3P_INDIA["citation"]
        if st.button(f"📑 [{cit['document']} — {cit['section']}]", key="btn_qa_cit"):
            st.session_state.active_citation = cit
            
        if st.session_state.active_citation:
            st.markdown(
                f'<div class="glassmorphism-side-panel"><div style="color: #58A6FF; font-weight: 700;">📑 EXACT SOURCE TEXT</div><div class="exact-source-highlight">"{cit["exact_text"]}"</div></div>',
                unsafe_allow_html=True
            )

    render_screen_0_bottom_banner()

# ==========================================
# SPECIAL SCREEN: Safe Abstention Screen
# ==========================================
def render_screen_abstention():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Safe Abstention Protocol")
    ab = dict(mock_data.MOCK_ABSTENTION_CASE)
    
    if st.session_state.get("abstention_reason"):
        ab["evidence"] = st.session_state.get("abstention_reason")
    
    options_html = "".join([f"<li>{opt}</li>" for opt in ab['user_options']])
    st.markdown(
        f'<div class="abstention-card"><h2 style="color: #58A6FF; font-family: \'Space Grotesk\', sans-serif;">🛡️ WE CAN\'T RELIABLY ANSWER THIS</h2><div style="margin: 0.75rem 0;">{render_status_badge(ab["status"])}</div>{render_sufficiency_meter(ab["sufficiency"])}<p style="color: var(--text-primary); font-size: 0.95rem; max-width: 650px; margin: 1rem auto;">{ab["evidence"]}</p><div style="text-align: left; background: var(--bg-base); padding: 1rem; border-radius: 6px; border: 1px solid var(--border-subtle);"><strong style="color: var(--text-primary);">Recommended Next Steps:</strong><ul style="color: var(--text-muted); margin-top: 0.5rem; font-size: 0.88rem;">{options_html}</ul></div></div>',
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Talk to a Human Expert →", type="primary", use_container_width=True):
            navigate_to("escalation")
    with col2:
        if st.button("← Return to Welcome Screen", use_container_width=True):
            navigate_to("welcome")

    render_screen_0_bottom_banner()

# ==========================================
# SCREEN 10: Human Expert Escalation
# ==========================================
def render_screen_10_escalation():
    render_screen_0_header()
    render_back_button()
    
    st.markdown("### Human Expert Escalation Protocol")
    
    st.markdown(
        '<div class="sakti-card"><div class="sakti-card-title" style="color: var(--accent-terracotta);">⚠️ Professional Legal Review Required</div><p style="color: var(--text-primary); font-size: 0.9rem;">Your query involves complex statutory interpretations, non-obvious technical contributions, or specific biological resource compliance that requires direct expert verification.</p><div style="font-weight: 600; margin-top: 1rem; font-size: 0.9rem;">Competent Authorities & Portals:</div><ul style="color: var(--text-muted); font-size: 0.88rem; line-height: 1.6;"><li><strong>Ministry of Ayush IPR Cell:</strong> Official advisory portal for traditional medicine innovations</li><li><strong>Controller General of Patents, Designs and Trade Marks (CGPDTM):</strong> <a href="https://ipindia.gov.in" target="_blank" style="color: #58A6FF;">ipindia.gov.in</a></li><li><strong>National Biodiversity Authority (NBA):</strong> ABS clearance portal for Indian biological resources</li><li><strong>Registered Patent Agent / IP Practitioner:</strong> For formal prior-art search & patent specification drafting</li></ul></div>',
        unsafe_allow_html=True
    )
    
    if st.button("← Return to Welcome Screen", type="primary"):
        navigate_to("welcome")

    render_screen_0_bottom_banner()

# ==========================================
# MAIN APP ROUTER
# ==========================================
def main():
    screen = st.session_state.current_screen
    
    if screen == "welcome":
        render_screen_1_welcome()
    elif screen == "jurisdiction":
        render_screen_2_jurisdiction()
    elif screen == "entry_mode":
        render_screen_3_entry_mode()
    elif screen == "describe_product":
        render_screen_4a_describe_product()
    elif screen == "scan_product":
        render_screen_4b_scan_product()
    elif screen == "describe_innovation":
        render_screen_4c_describe_innovation()
    elif screen == "confirm_intake":
        render_screen_5_confirm_intake()
    elif screen == "processing":
        render_screen_6_processing()
    elif screen == "classification_result":
        render_screen_7_classification_result()
    elif screen == "main_results":
        render_screen_8_main_results()
    elif screen == "direct_qa":
        render_screen_9_direct_qa()
    elif screen == "abstention":
        render_screen_abstention()
    elif screen == "escalation":
        render_screen_10_escalation()
    else:
        render_screen_1_welcome()

if __name__ == "__main__":
    main()

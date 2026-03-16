import streamlit as st
from PIL import Image
from utils.analyzer import analyze_xray
from utils.analyzer_g import analyze_xray_g
from utils.pdf_generator import generate_pdf
from datetime import datetime

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="DentalAI — OPG Analyzer",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Main header ── */
    .main-header {
        background: linear-gradient(135deg, #1a1a3e 0%, #0f0f1a 100%);
        border: 1px solid #2d2d5e;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: #ffffff !important; margin: 0; font-size: 1.8rem; }
    .main-header p  { color: #7b8cde !important; margin: 0.3rem 0 0; font-size: 0.9rem; }

    /* ── Disclaimer banner ── */
    .disclaimer-banner {
        background: #2d2200;
        border: 1px solid #7a5c00;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.85rem;
        color: #ffc947 !important;
    }

    /* ── Report output box ── */
    .report-box {
        background: #1a1a2e;
        border: 1px solid #2d2d5e;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        line-height: 1.6;
        white-space: pre-wrap;
        max-height: 600px;
        overflow-y: auto;
        color: #e2e8f0 !important;
    }

    /* ── Input fields ── */
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d2d5e !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus {
        border-color: #4f8ef7 !important;
        box-shadow: 0 0 0 2px rgba(79,142,247,0.2) !important;
    }
    .stTextArea textarea {
        background-color: #1a1a2e !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d2d5e !important;
        border-radius: 8px !important;
    }
    .stTextInput label, .stTextArea label, .stFileUploader label {
        color: #a0b0d0 !important;
        font-weight: 600 !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #1a1a2e !important;
        border: 2px dashed #2d2d5e !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploaderDropzone"] * { color: #a0b0d0 !important; }

    /* ── Analyze button ── */
    .stButton > button {
        background-color: #4f8ef7 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: background-color 0.2s !important;
    }
    .stButton > button:disabled {
        background-color: #2d2d5e !important;
        color: #6b7db3 !important;
        opacity: 1 !important;
    }
    .stButton > button:hover:not(:disabled) {
        background-color: #3a7de8 !important;
    }

    /* ── Download buttons ── */
    .stDownloadButton > button {
        background-color: #1a472a !important;
        color: #ffffff !important;
        border: 1px solid #2d6a4f !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stDownloadButton > button:hover {
        background-color: #2d6a4f !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #0f0f1a !important;
        border-right: 1px solid #2d2d5e !important;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stCaption { color: #6b7db3 !important; }

    /* ── Metrics ── */
    [data-testid="stMetricValue"] { color: #4f8ef7 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #a0b0d0 !important; }

    /* ── Misc ── */
    .stCaption { color: #6b7db3 !important; }
    .streamlit-expanderHeader { color: #e2e8f0 !important; }

    /* ── Empty state placeholder ── */
    .empty-state {
        border: 2px dashed #2d2d5e;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        background: #1a1a2e;
        margin-top: 1rem;
    }

    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "analysis_history"    not in st.session_state: st.session_state.analysis_history    = []
if "current_report"      not in st.session_state: st.session_state.current_report      = None
if "current_patient_id"  not in st.session_state: st.session_state.current_patient_id  = None
if "total_analyses"      not in st.session_state: st.session_state.total_analyses      = 0

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦷 DentalAI")
    st.markdown("---")
    st.markdown("### This Session")
    st.metric("Analyses run", st.session_state.total_analyses)
    st.markdown("---")
    st.markdown("### Recent Analyses")
    if not st.session_state.analysis_history:
        st.caption("No analyses yet this session.")
    else:
        for item in reversed(st.session_state.analysis_history[-10:]):
            st.markdown(f"**{item['patient_id']}** — {item['time']}")
    st.markdown("---")
    st.caption("⚠️ AI-generated drafts only. All reports must be reviewed by a licensed dental professional.")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🦷 DentalAI — OPG Analysis</h1>
    <p>AI-assisted panoramic X-ray analysis for dental students and practitioners</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-banner">
    ⚠️ <strong>Important:</strong> This tool generates AI-assisted preliminary drafts
    for educational and workflow purposes only. All outputs must be reviewed and
    approved by a licensed dental professional before any clinical use.
    Not FDA-cleared for diagnostic use.
</div>
""", unsafe_allow_html=True)

# ─── Layout ───────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### Upload X-Ray")

    patient_id = st.text_input(
        "Patient ID",
        placeholder="e.g. PT-2024-001",
        help="Enter a patient identifier. Do not use real patient names.",
    )

    uploaded_file = st.file_uploader(
        "Upload panoramic X-ray (OPG)",
        type=["jpg", "jpeg", "png", "webp"],
    )

    clinical_notes = st.text_area(
        "Additional clinical notes (optional)",
        placeholder="e.g. Patient reports pain in lower left quadrant.",
        height=80,
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-ray", use_container_width=True)
        st.caption(f"File: {uploaded_file.name} | Size: {uploaded_file.size / 1024:.1f} KB")

    st.markdown("---")

    analyze_ready = uploaded_file is not None and patient_id.strip() != ""

    if not analyze_ready:
        st.info("👆 Enter a Patient ID and upload an X-ray to enable analysis.")

    analyze_btn = st.button(
        "🔍 Analyze X-Ray",
        type="primary",
        use_container_width=True,
        disabled=not analyze_ready,
    )

with col_right:
    st.markdown("### Analysis Report")

    if analyze_btn and analyze_ready:
        with st.spinner("Analyzing X-ray with Claude Vision... this takes 15–30 seconds."):
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()

            # result = analyze_xray(                    # For Claude
            #     image_bytes=image_bytes,
            #     file_name=uploaded_file.name,
            #     patient_id=patient_id.strip(),
            #     notes=clinical_notes.strip(),
            # )
            result = analyze_xray_g(                    # For Gemini
                image_bytes=image_bytes,
                file_name=uploaded_file.name,
                patient_id=patient_id.strip(),
                notes=clinical_notes.strip(),
            )

        if result["success"]:
            st.session_state.current_report     = result["report"]
            st.session_state.current_patient_id = patient_id.strip()
            st.session_state.total_analyses     += 1
            st.session_state.analysis_history.append({
                "patient_id": patient_id.strip(),
                "time":       datetime.now().strftime("%I:%M %p"),
                "report":     result["report"],
            })
            st.success("✅ Analysis complete!")
            input_tokens  = result.get("input_tokens", 0)
            output_tokens = result.get("output_tokens", 0)
            est_cost      = (input_tokens * 0.075 + output_tokens * 0.30) / 1_000_000  # Gemini 2.0 Flash pricing
            st.caption(f"Tokens — Input: {input_tokens:,} | Output: {output_tokens:,} | Est. cost: ${est_cost:.4f}")
        else:
            st.error(f"❌ {result['error']}")

    if st.session_state.current_report:
        report = st.session_state.current_report
        pid    = st.session_state.current_patient_id

        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
        st.markdown("---")

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="📄 Download TXT",
                data=report,
                file_name=f"dental_report_{pid}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with dl2:
            pdf_bytes = generate_pdf(report_text=report, patient_id=pid)
            st.download_button(
                label="📑 Download PDF",
                data=pdf_bytes,
                file_name=f"dental_report_{pid}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:3rem;margin-bottom:1rem;">🦷</div>
            <div style="font-size:1rem;font-weight:600;color:#a0b0d0;">No report yet</div>
            <div style="font-size:0.85rem;margin-top:0.5rem;color:#6b7db3;">
                Upload an X-ray and click Analyze to generate a report
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── History ──────────────────────────────────────────────────────────────────
if len(st.session_state.analysis_history) > 1:
    st.markdown("---")
    st.markdown("### Session History")
    st.caption("All analyses from this session. Clears when you close the browser tab.")
    for i, item in enumerate(reversed(st.session_state.analysis_history)):
        with st.expander(f"🦷 Patient {item['patient_id']} — {item['time']}"):
            st.markdown(f'<div class="report-box">{item["report"]}</div>', unsafe_allow_html=True)
            pdf = generate_pdf(item["report"], item["patient_id"])
            st.download_button(
                label="📑 Download PDF",
                data=pdf,
                file_name=f"dental_report_{item['patient_id']}.pdf",
                mime="application/pdf",
                key=f"pdf_history_{i}",
            )
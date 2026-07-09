import streamlit as st
import pandas as pd

from parser.extract_text import extract_text
from parser.resume_parser import parse_resume
from jd_analyser.jd_parser import parse_job_description
from db.database import (
    init_db,
    save_candidate,
    save_job_description,
    get_all_candidates,
    get_all_job_descriptions,
)

st.set_page_config(
    page_title="AI Recruitment Copilot",
    layout="wide",
    initial_sidebar_state="collapsed"
)
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1rem;
    letter-spacing: 0.05em;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid rgba(167,139,250,0.2);
    padding-bottom: 0.5rem;
}
.info-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.4rem;
}
.info-label {
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 500;
    min-width: 70px;
}
.info-value {
    color: #e2e8f0;
    font-size: 0.9rem;
}
.skill-badge {
    display: inline-block;
    background: rgba(96,165,250,0.15);
    border: 1px solid rgba(96,165,250,0.3);
    color: #60a5fa;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.2rem;
}
.list-item {
    color: #cbd5e1;
    font-size: 0.88rem;
    padding: 0.3rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    padding-left: 0.5rem;
}
.list-item::before {
    content: "▸ ";
    color: #a78bfa;
}
.success-banner {
    background: linear-gradient(90deg, rgba(52,211,153,0.15), rgba(52,211,153,0.05));
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #34d399;
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 1.2rem;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #94a3b8;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    color: white !important;
}

.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 2rem;
    font-weight: 600;
    font-size: 0.95rem;
    width: 100%;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>⚡ AI Recruitment & Talent Management Copilot</h1>
    <p>MILESTONE 1 — Resume Parsing & Job Description Analyser</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄  Resume Parser", "📋  Job Description Analyser", "🗂️  Stored Records"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_upload, col_gap = st.columns([2, 1])
    with col_upload:
        st.markdown('<div class="card-title">Upload Candidate Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag and drop or browse — PDF & DOCX supported",
            type=["pdf", "docx"],
            label_visibility="visible"
        )

    if uploaded_file is not None:
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
            with st.spinner("Analysing resume..."):
                raw_text = extract_text(uploaded_file, uploaded_file.name)
                profile = parse_resume(raw_text)
                candidate_id = save_candidate(profile, uploaded_file.name, raw_text)
                st.session_state.last_uploaded = uploaded_file.name
                st.session_state.profile = profile
                st.session_state.candidate_id = candidate_id
                st.session_state.raw_text = raw_text
        else:
            profile = st.session_state.profile
            candidate_id = st.session_state.candidate_id
            raw_text = st.session_state.raw_text

        st.markdown(f"""
        <div class="success-banner">
            ✅ Resume parsed successfully — Candidate ID: <strong>{candidate_id}</strong>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">👤 Candidate Profile</div>
                <div class="info-row">
                    <span class="info-label">Name</span>
                    <span class="info-value">{profile['name'] or 'Not found'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Email</span>
                    <span class="info-value">{profile['email'] or 'Not found'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Phone</span>
                    <span class="info-value">{profile['phone'] or 'Not found'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            skills_html = ""
            if profile["skills"]:
                for skill in profile["skills"][:15]:
                    skills_html += f'<span class="skill-badge">{skill}</span>'
            else:
                skills_html = '<span class="info-value">Not found</span>'

            st.markdown(f"""
            <div class="card">
                <div class="card-title">🛠️ Skills</div>
                {skills_html}
            </div>
            """, unsafe_allow_html=True)

            edu_html = "".join([f'<div class="list-item">{item}</div>' for item in profile["education"]]) or '<div class="info-value">Not found</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🎓 Education</div>
                {edu_html}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            exp_html = "".join([f'<div class="list-item">{item}</div>' for item in profile["experience"]]) or '<div class="info-value">Not found</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">💼 Work Experience</div>
                {exp_html}
            </div>
            """, unsafe_allow_html=True)

            cert_html = "".join([f'<div class="list-item">{item}</div>' for item in profile["certifications"]]) or '<div class="info-value">Not found</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🏆 Certifications</div>
                {cert_html}
            </div>
            """, unsafe_allow_html=True)

            proj_html = "".join([f'<div class="list-item">{item}</div>' for item in profile["projects"]]) or '<div class="info-value">Not found</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🚀 Projects</div>
                {proj_html}
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📃 View Raw Extracted Text"):
            st.code(raw_text, language=None)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_jd, col_gap2 = st.columns([2, 1])
    with col_jd:
        st.markdown('<div class="card-title">Paste or Upload Job Description</div>', unsafe_allow_html=True)
        jd_text_input = st.text_area("Paste the job description here", height=220, placeholder="e.g. Software Engineer - Python Developer...")
        jd_file = st.file_uploader("Or upload a JD file (PDF/DOCX)", type=["pdf", "docx"], key="jd_upload")
        analyse_btn = st.button("🔍  Analyse Job Description")

    raw_jd_text = ""
    if jd_file is not None:
        raw_jd_text = extract_text(jd_file, jd_file.name)
    elif jd_text_input.strip():
        raw_jd_text = jd_text_input

    if analyse_btn and raw_jd_text.strip():
        with st.spinner("Analysing job description..."):
            jd_profile = parse_job_description(raw_jd_text)
            jd_id = save_job_description(jd_profile, raw_jd_text)

        st.markdown(f"""
        <div class="success-banner">
            ✅ Job Description analysed successfully — JD ID: <strong>{jd_id}</strong>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📌 Job Overview</div>
                <div class="info-row">
                    <span class="info-label">Job Title</span>
                    <span class="info-value">{jd_profile['job_title'] or 'Not found'}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Experience</span>
                    <span class="info-value">{jd_profile['experience_level']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            skills_html = ""
            if jd_profile["required_skills"]:
                for skill in jd_profile["required_skills"]:
                    skills_html += f'<span class="skill-badge">{skill}</span>'
            else:
                skills_html = '<span class="info-value">Not found</span>'

            st.markdown(f"""
            <div class="card">
                <div class="card-title">🛠️ Required Skills</div>
                {skills_html}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            qual_html = "".join([f'<div class="list-item">{item}</div>' for item in jd_profile["qualifications"]]) or '<div class="info-value">Not found</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🎓 Qualifications</div>
                {qual_html}
            </div>
            """, unsafe_allow_html=True)

            resp_html = "".join([f'<div class="list-item">{item}</div>' for item in jd_profile["responsibilities"]]) or '<div class="info-value">Not found</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📋 Responsibilities</div>
                {resp_html}
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">📁 All Parsed Candidates</div>', unsafe_allow_html=True)
    candidates = get_all_candidates()
    if candidates:
        df_candidates = pd.DataFrame(candidates)[["id", "file_name", "name", "email", "phone", "created_at"]]
        st.dataframe(df_candidates, use_container_width=True, hide_index=True)
    else:
        st.info("No candidates parsed yet. Upload a resume in the Resume Parser tab.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">📁 All Analysed Job Descriptions</div>', unsafe_allow_html=True)
    jds = get_all_job_descriptions()
    if jds:
        df_jds = pd.DataFrame(jds)[["id", "job_title", "experience_level", "created_at"]]
        st.dataframe(df_jds, use_container_width=True, hide_index=True)
    else:
        st.info("No job descriptions analysed yet. Go to the Job Description Analyser tab.")
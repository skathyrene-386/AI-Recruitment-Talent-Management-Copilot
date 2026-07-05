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

st.set_page_config(page_title="AI Recruitment Copilot", layout="wide")
init_db()

st.title("AI Recruitment & Talent Management Copilot")
st.caption("Milestone 1: Resume Parsing & Job Description Analyser")

tab1, tab2, tab3 = st.tabs(["📄 Resume Parser", "📋 Job Description Analyser", "🗂️ Stored Records"])

with tab1:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF or DOCX resume", type=["pdf", "docx"])

    if uploaded_file is not None:
        with st.spinner("Extracting and parsing resume..."):
            raw_text = extract_text(uploaded_file, uploaded_file.name)
            profile = parse_resume(raw_text)
            candidate_id = save_candidate(profile, uploaded_file.name, raw_text)

        st.success(f"Resume parsed and saved! Candidate ID: {candidate_id}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Candidate Profile")
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Email:** {profile['email']}")
            st.write(f"**Phone:** {profile['phone']}")
            st.markdown("**Skills**")
            st.write(", ".join(profile["skills"]) if profile["skills"] else "Not found")
            st.markdown("**Education**")
            for item in profile["education"]:
                st.write(f"- {item}")

        with col2:
            st.markdown("**Work Experience**")
            for item in profile["experience"]:
                st.write(f"- {item}")
            st.markdown("**Certifications**")
            for item in profile["certifications"]:
                st.write(f"- {item}")
            st.markdown("**Projects**")
            for item in profile["projects"]:
                st.write(f"- {item}")

        with st.expander("Raw extracted text"):
            st.text(raw_text)

with tab2:
    st.subheader("Paste or Upload Job Description")
    jd_text_input = st.text_area("Paste job description text here", height=250)
    jd_file = st.file_uploader("Or upload a JD file (PDF/DOCX)", type=["pdf", "docx"], key="jd_upload")

    raw_jd_text = ""
    if jd_file is not None:
        raw_jd_text = extract_text(jd_file, jd_file.name)
    elif jd_text_input.strip():
        raw_jd_text = jd_text_input

    if st.button("Analyse Job Description") and raw_jd_text.strip():
        with st.spinner("Analysing job description..."):
            jd_profile = parse_job_description(raw_jd_text)
            jd_id = save_job_description(jd_profile, raw_jd_text)

        st.success(f"Job description analysed and saved! JD ID: {jd_id}")

        st.markdown("### Parsed Job Description")
        st.write(f"**Job Title:** {jd_profile['job_title']}")
        st.write(f"**Experience Level:** {jd_profile['experience_level']}")
        st.markdown("**Required Skills**")
        st.write(", ".join(jd_profile["required_skills"]) if jd_profile["required_skills"] else "Not found")
        st.markdown("**Qualifications**")
        for item in jd_profile["qualifications"]:
            st.write(f"- {item}")
        st.markdown("**Responsibilities**")
        for item in jd_profile["responsibilities"]:
            st.write(f"- {item}")

with tab3:
    st.subheader("All Parsed Candidates")
    candidates = get_all_candidates()
    if candidates:
        df_candidates = pd.DataFrame(candidates)[["id", "file_name", "name", "email", "phone", "created_at"]]
        st.dataframe(df_candidates, use_container_width=True)
    else:
        st.info("No candidates parsed yet.")

    st.subheader("All Analysed Job Descriptions")
    jds = get_all_job_descriptions()
    if jds:
        df_jds = pd.DataFrame(jds)[["id", "job_title", "experience_level", "created_at"]]
        st.dataframe(df_jds, use_container_width=True)
    else:
        st.info("No job descriptions analysed yet.")
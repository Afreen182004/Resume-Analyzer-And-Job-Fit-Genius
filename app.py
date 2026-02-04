import streamlit as st
import PyPDF2
from logic import *

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("🚀 Resume Analyzer & Job Fit Genius")
st.write("Upload your resume and paste the Job Description to get a complete analysis")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

with right_col:
    st.subheader("🧾 Job Description")
    job_description = st.text_area("Paste Job Description here", height=250)

if st.button("🔍 Analyse Resume"):

    if resume_file is None or job_description.strip() == "":
        st.warning("Please upload resume and paste job description")

    else:
        reader = PyPDF2.PdfReader(resume_file)
        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text()

        st.divider()
        st.header("📊 Analysis Results")

        st.subheader("🧠 Skill Confidence")
        skill_list = [
            "python", "sql", "machine learning", "deep learning",
            "excel", "powerbi", "nlp", "statistics",
            "tensorflow", "pandas", "numpy"
        ]

        skill_conf = calculate_skill_confidence(resume_text, skill_list)
        for skill, score in skill_conf.items():
            st.write(f"{skill.upper()} : {score}%")

        st.subheader("⚠️ Skill Gap Analysis")
        gap_score, total_gap = calculate_skill_gap(resume_text)
        for skill, gap in gap_score.items():
            if gap == 0:
                st.success(f"{skill} → Present")
            else:
                st.error(f"{skill} → Missing (-{gap}%)")
        st.warning(f"Total Skill Gap Penalty: -{total_gap}%")


        st.subheader("🚩 Resume Red Flags")
        flags = detect_red_flags(resume_text)

        if len(flags) == 0:
            st.success("No major red flags detected")
        else:
            for f in flags:
                st.error(f)


        st.subheader("💪 Strength Summary")
        st.success(generate_strength_summary(resume_text))

        st.subheader("⚠️ Weakness Summary")
        st.warning(generate_weakness_summary(resume_text))

        st.subheader("📊 Resume Consistency")
        consistency = calculate_consistency(resume_text)
        st.metric("Consistency Score", f"{consistency}%")

        st.subheader("📄 ATS Resume Score")
        ats_score, ats_detail = calculate_ats_score(resume_text)
        st.metric("ATS Score", f"{ats_score}%")
        for category, status in ats_detail.items():
            if status == "Matched":
                st.success(f"{category} → Matched")
            else:
                st.error(f"{category} → Missing")

        st.subheader("📝 Job Description vs Resume Match")
        matched_skills, missing_skills, jd_fit = jd_resume_match(resume_text, job_description)
        st.success(f"JD Fit Score: {jd_fit}%")
        st.write("✅ Matching Skills:")
        st.write(", ".join(matched_skills) if matched_skills else "None")
        st.write("❌ Missing Skills:")
        st.write(", ".join(missing_skills) if missing_skills else "None")

        st.subheader("🧑‍💼 Recommended Job Roles (Based on Job Description)")
        jd_jobs = recommend_jobs_from_jd(job_description)
        if len(jd_jobs) == 0:
            st.warning("No matching job roles found from the job description")
        else:
            for role, score in jd_jobs.items():
                st.write(f"{role} → {score}% match")
                st.progress(score / 100)

        st.subheader("🧑‍⚖️ Final Candidate Decision")

        decision = final_candidate_decision(
            ats_score,
            jd_fit,
            consistency
        )

        if decision == "SELECT":
            st.success("✅ Candidate SELECTED for the Job")
        elif decision == "WAITING":
            st.warning("🟡 Candidate kept in WAITING LIST")
        else:
            st.error("❌ Candidate REJECTED for this Job")






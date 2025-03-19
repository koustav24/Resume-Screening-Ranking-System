import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import time


def check_and_install_packages():
    import importlib

    required_packages = {
        "PyPDF2": "PyPDF2",
        "streamlit": "streamlit",
        "pandas": "pandas",
        "sklearn": "scikit-learn",
        "plotly": "plotly"
    }

    missing_packages = []

    for package, pip_name in required_packages.items():
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(pip_name)

    if missing_packages:
        st.warning(f"Missing required packages: {', '.join(missing_packages)}")
        st.info("Installing missing packages...")

        import subprocess
        for package in missing_packages:
            try:
                subprocess.check_call(["pip", "install", package])
                st.success(f"Successfully installed {package}")
            except:
                st.error(f"Failed to install {package}")

        st.info("Please restart the application")
        st.stop()


def extract_text_from_pdf(file):
    try:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    except Exception as e:
        st.error(f"Error processing {file.name}: {str(e)}")
        return ""


def rank_resumes(job_description, resumes):
    # Combine job description with resumes
    documents = [job_description] + resumes

    # Configure TF-IDF with domain-specific parameters
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # Consider both unigrams and bigrams
        max_df=0.85,  # Ignore terms that appear in more than 85% of documents
        min_df=0.01,  # Ignore terms that appear in less than 1% of documents
        max_features=5000  # Limit features to prevent overfitting
    )

    tfidf_matrix = vectorizer.fit_transform(documents)
    vectors = tfidf_matrix.toarray()

    # Calculate cosine similarity
    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()

    return cosine_similarities


def validate_job_description(text):
    if not text.strip():
        return False, "Job description cannot be empty"

    if len(text.split()) < 20:
        return False, "Job description is too short. Please provide a detailed description."

    return True, ""


def validate_resume(text, filename):
    if not text.strip():
        return False, f"{filename}: Could not extract text. Check if the PDF contains actual text."

    if len(text.split()) < 10:
        return False, f"{filename}: Extracted text is too short. Check if the PDF contains actual text."

    return True, ""


def process_resumes(job_description, uploaded_files):
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Process in batches of 5 files
    batch_size = 5
    for i in range(0, len(uploaded_files), batch_size):
        batch_files = uploaded_files[i:i + batch_size]
        batch_texts = []
        batch_names = []

        # Extract text from each file in the batch
        for j, file in enumerate(batch_files):
            status_text.text(f"Processing file {i + j + 1}/{len(uploaded_files)}: {file.name}")
            text = extract_text_from_pdf(file)
            is_valid, error_msg = validate_resume(text, file.name)

            if is_valid:
                batch_texts.append(text)
                batch_names.append(file.name)
            else:
                st.warning(error_msg)

        # Rank batch if there are valid resumes
        if batch_texts:
            batch_scores = rank_resumes(job_description, batch_texts)
            for name, score in zip(batch_names, batch_scores):
                results.append({"Resume": name, "Score": score})

        # Update progress
        progress_bar.progress((i + len(batch_files)) / len(uploaded_files))

    progress_bar.progress(1.0)
    status_text.text("Processing complete!")
    return results


def analyze_key_skills(job_description, resume_text):
    """Extract and match key skills from job description and resume"""
    # Simple keyword extraction (in real app, use NER or keyword extraction libraries)
    job_keywords = set(job_description.lower().split())
    resume_keywords = set(resume_text.lower().split())

    # Calculate keyword match score
    common_keywords = job_keywords.intersection(resume_keywords)
    skill_match_score = len(common_keywords) / max(len(job_keywords), 1)

    return skill_match_score, list(common_keywords)


def enhanced_resume_ranking(job_description, resumes, resume_names):
    # Get basic TF-IDF similarity scores
    cosine_scores = rank_resumes(job_description, resumes)

    results = []
    for i, (resume_text, name) in enumerate(zip(resumes, resume_names)):
        # Get additional scores
        skill_score, matched_skills = analyze_key_skills(job_description, resume_text)

        # Calculate weighted final score
        final_score = 0.7 * cosine_scores[i] + 0.3 * skill_score

        results.append({
            "Resume": name,
            "Overall Score": final_score,
            "TF-IDF Score": cosine_scores[i],
            "Skill Match Score": skill_score,
            "Matched Keywords": ", ".join(list(matched_skills)[:10])  # Show top 10 matched keywords
        })

    return results


# Streamlit app
st.title("AI Resume Screening & Candidate Ranking System")

# Check required packages
check_and_install_packages()

# Job description input
st.header("Job Description")
job_description = st.text_area("Enter the job description")

# File uploader
st.header("Upload Resumes")
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files and job_description:
    # Validate job description
    is_valid_job, error_msg = validate_job_description(job_description)
    if not is_valid_job:
        st.error(error_msg)
    else:
        st.header("Ranking Resumes")

        with st.spinner("Processing resumes..."):
            # Process resumes in batches with progress tracking
            processed_results = process_resumes(job_description, uploaded_files)

            if processed_results:
                # Create DataFrame and sort by score
                results_df = pd.DataFrame(processed_results)
                results_df = results_df.sort_values(by="Score", ascending=False)

                # Display results
                st.subheader("Resume Rankings")
                st.dataframe(results_df)

                # Visualize top resumes
                st.subheader("Top Candidates")
                top_n = min(5, len(results_df))
                fig = px.bar(
                    results_df.head(top_n),
                    x="Resume",
                    y="Score",
                    title=f"Top {top_n} Candidate Matches"
                )
                st.plotly_chart(fig)

                # Get enhanced rankings with skill matching
                st.subheader("Enhanced Analysis")
                valid_resumes = []
                valid_names = []

                for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    is_valid, _ = validate_resume(text, file.name)
                    if is_valid:
                        valid_resumes.append(text)
                        valid_names.append(file.name)

                enhanced_results = enhanced_resume_ranking(job_description, valid_resumes, valid_names)
                enhanced_df = pd.DataFrame(enhanced_results)
                enhanced_df = enhanced_df.sort_values(by="Overall Score", ascending=False)

                st.dataframe(enhanced_df)
            else:
                st.warning("No valid resumes found for analysis.")
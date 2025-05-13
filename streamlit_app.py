import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime
import pdfplumber
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import json
import requests
from streamlit_lottie import st_lottie

# -------------------- SET PAGE CONFIG FIRST --------------------
st.set_page_config(page_title="Smart Internship Recommender", layout="wide")

# -------------------- ADD BACKGROUND COLOR --------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #e6f2ff;
        padding: 2rem;
    }
    h1, h2, h3, h4 {
        color: #003366;
    }
    .stButton>button {
        background-color: #4da6ff;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #1a8cff;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- LOTTIE ANIMATION LOADER --------------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_tno6cg2w.json")  # internship animation

# -------------------- NLTK SETUP --------------------
nltk.download('punkt')
nltk.download('stopwords')

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    return pd.read_csv("python_internships.csv")

df = load_data()

# -------------------- APP TITLE --------------------
st_lottie(lottie_animation, height=250, key="recommender")
st.title("🤖 Smart Internship Recommender")
st.markdown("Get personalized internship recommendations by uploading your resume! 📄🔍")

# -------------------- LOCATION FILTER --------------------
# Get unique locations for the dropdown
locations = df['Location'].unique().tolist()
locations.insert(0, 'All Locations')  # Add 'All Locations' as the default option

location_filter = st.selectbox("🔍 Select Internship Location", locations)

# -------------------- PDF UPLOAD --------------------
st.subheader("📄 Upload Your Resume (PDF)")
resume_file = st.file_uploader("Choose a PDF file", type="pdf")

# -------------------- SKILL EXTRACTOR --------------------
def extract_skills_from_pdf(file):
    try:
        skills = set()
        stop_words = set(stopwords.words("english"))

        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            text = text.lower()

            skill_section = re.search(r"skills[:\s]*([\s\S]*?)(?:\n[A-Z]|$)", text)
            if skill_section:
                extracted_skills = word_tokenize(skill_section.group(1))
                meaningful_skills = [
                    word for word in extracted_skills
                    if word.isalpha() and word not in stop_words
                ]
                skills = set(meaningful_skills)

        return skills
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return set()

user_skills = set()
if resume_file is not None:
    user_skills = extract_skills_from_pdf(resume_file)
    if user_skills:
        st.success(f"✅ Extracted Skills: {', '.join(user_skills)}")
    else:
        st.warning("⚠️ No skills found. Please ensure your resume has a 'Skills' section.")

# -------------------- MATCHING FUNCTION --------------------
def match_jobs(skills, data, location):
    matches = []
    for _, row in data.iterrows():
        job_skills = set(str(row['Skills']).lower().split(", "))
        common_skills = skills & job_skills
        if common_skills:
            row['Matched Skills'] = len(common_skills)
            # Filter by location if selected
            if location == 'All Locations' or row['Location'] == location:
                matches.append(row)
    return pd.DataFrame(matches).sort_values(by='Matched Skills', ascending=False)

# -------------------- DISPLAY INTERNSHIPS --------------------
def display_internships(internships, title, top_only=False):
    st.subheader(title)
    if top_only:
        internships = internships.head(5)
    for index, row in internships.iterrows():
        st.markdown(f"**{row['Title']}** at **{row['Company']}**")
        st.markdown(f"- 📍 Location: {row['Location']}")
        st.markdown(f"- 💰 Stipend: {row['Stipend']}")
        st.markdown(f"- ✅ Matched Skills: {row['Matched Skills']}")
        st.markdown(f"[🔗 Apply Here]({row['Link']})")
        st.markdown("---")

# -------------------- GRAPH: TOP 10 SKILLS --------------------
def plot_top_skills(data):
    # Flatten the skills column into a list of skills for the graph
    all_skills = []
    for skills in data['Skills']:
        all_skills.extend(str(skills).lower().split(", "))

    # Get the frequency of each skill
    skill_counts = pd.Series(all_skills).value_counts().head(10)

    # Plot the top 10 skills
    plt.figure(figsize=(10, 6))
    sns.barplot(x=skill_counts.index, y=skill_counts.values, palette='viridis')
    plt.title('Top 10 Skills in Internship Listings', fontsize=16)
    plt.xlabel('Skills', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

# -------------------- MAIN DISPLAY --------------------
if user_skills:
    matched_jobs = match_jobs(user_skills, df, location_filter)
    if not matched_jobs.empty:
        display_internships(matched_jobs, "🌟 Top 5 Recommended Internships", top_only=True)

        with st.expander("🔎 Show More Matching Internships"):
            display_internships(matched_jobs.iloc[5:], "📋 More Internship Matches")

        # Display the graph of top 10 skills in internship listings
        plot_top_skills(df)
    else:
        st.info("😕 No matching internships found. Try uploading a resume with more technical skills.")
else:
    st.info("📄 Upload your resume above to get personalized internship suggestions.")

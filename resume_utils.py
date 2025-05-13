import fitz  # PyMuPDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract skills from the resume text
def extract_skills(resume_text):
    # Define a set of skills that we will look for in the resume
    skill_keywords = [
        "python", "java", "sql", "javascript", "html", "css", "react", "data analysis", "machine learning", "deep learning", 
        "nodejs", "django", "flask", "c++", "docker", "aws", "azure", "tensorflow", "pandas", "numpy", "matplotlib", "git"
    ]
    
    # Find matching skills in the resume text
    skills = [skill for skill in skill_keywords if skill.lower() in resume_text.lower()]
    return skills

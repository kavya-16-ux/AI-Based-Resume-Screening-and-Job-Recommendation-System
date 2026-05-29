# 🤖 AI-Based Resume Screening & Job Recommendation System
An intelligent recruitment platform that automates resume screening, candidate ranking, and job recommendations using Sentence-BERT and Cosine Similarity.

---

# 📌 Table of Contents

* About the Project
* Features
* Tech Stack
* System Architecture
* Project Workflow
* Screenshots
* Installation
* How It Works
* Algorithms Used
* Database Structure
* Project Structure
* Author

---

# 📖 About the Project

Companies receive hundreds of resumes for every job opening.
Manually reading and screening all of them is:

* Time consuming
* Prone to human bias and errors
* Inefficient

**Project** solves this by:

* Automatically reading PDF resumes using PyMuPDF
* Extracting technical skills using spaCy NLP
* Calculating match scores using Sentence-BERT + Cosine Similarity
* Ranking candidates from highest to lowest score
* Recommending best matching jobs to candidates


---

# ✨ Features

## For Candidates

* ✅ Upload PDF resume
* ✅ AI-based skill extraction
* ✅ Smart job recommendations
* ✅ Match score calculation
* ✅ Missing skills analysis
* ✅ AI interview system

## For Recruiters

* ✅ Post jobs
* ✅ View ranked candidates
* ✅ Candidate skill analysis
* ✅ Accept or reject applicants
* ✅ Recruiter dashboard management

---

# 🛠️ Tech Stack

| Category             | Technology             |
| -------------------- | ---------------------- |
| Programming Language | Python 3.10            |
| Framework            | Django                 |
| NLP                  | spaCy                  |
| AI Model             | Sentence-BERT          |
| Similarity Algorithm | Cosine Similarity      |
| Database             | PostgreSQL             |
| Frontend             | HTML, CSS, Bootstrap 5 |
| PDF Parser           | PyMuPDF                |
| Deep Learning        | PyTorch, Transformers  |
| IDE                  | VS Code                |

---

# 🏗️ System Architecture

CLIENT TIER
→ Bootstrap UI / Browser

APPLICATION TIER
→ Django Backend
→ Resume Parsing
→ NLP Processing
→ Skill Extraction
→ Similarity Matching
→ Candidate Ranking

DATA TIER
→ PostgreSQL Database

---

# 🔄 Project Workflow

1. User Login (Candidate / Recruiter)
2. Resume Upload or Job Posting
3. Resume Text Extraction
4. Skill Extraction using NLP
5. Sentence-BERT Vectorization
6. Cosine Similarity Calculation
7. Candidate Ranking
8. Job Recommendation


---

# 📸 Screenshots

## Register Page

![Register Page]

## Login Page

![Login Page]

## Candidate Dashboard

![Candidate Dashboard]

## AI Job Matches

![Job Matches]

## Recruiter Dashboard

![Recruiter Dashboard]

## Create Job

![Create Job]

## Applicant Ranking

![Applicant Ranking]


---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-resume-screening.git
cd ai-resume-screening
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Server

```bash
python manage.py runserver
```

---

# 🤖 How It Works

## Resume Matching Process

1. Extract text from PDF resume
2. Extract skills using spaCy NLP
3. Convert text into embeddings using Sentence-BERT
4. Calculate similarity score using Cosine Similarity
5. Rank candidates and recommend jobs

---

# 🧠 Algorithms Used

## Sentence-BERT (SBERT)

* Sentence-BERT is a transformer-based NLP model built on top of BERT.
* It converts resumes and job descriptions into dense semantic vector embeddings.
* Unlike TF-IDF, Sentence-BERT understands contextual meaning and semantic similarity.
* Example:
* “ML Engineer” and “Machine Learning Engineer” are understood as similar meanings.
* The generated embeddings are compared using Cosine Similarity to calculate the final match score.
* This improves recommendation accuracy and candidate ranking quality.

## Why I Used Sentence-BERT Instead of TF-IDF

* TF-IDF only performs keyword matching.
* It cannot understand semantic meaning or context.
* Sentence-BERT generates contextual embeddings that capture the meaning of entire sentences.
* This improves matching accuracy even when different words express similar skills.
* It provides more intelligent resume-job matching compared to traditional NLP methods.


## Cosine Similarity

* Measures similarity between vectors
* Produces final match percentage

## spaCy NLP

* Extracts technical skills from resumes
* Identifies missing skills

## Mean Pooling

* Generates sentence-level embeddings

## Frequency Analysis

* Finds most required missing skills

---

# 🗄️ Database Structure

## accounts_user

* id
* username
* email
* password
* role

## jobs_job

* id
* title
* company
* location
* description

## resumes_resume

* id
* file
* extracted_text
* extracted_skills

## applications_application

* id
* match_score
* status
* missing_skills

---

# 📁 Project Structure

```text
RESUME_SCREENING_PROJECT/
│
├── accounts/
├── applications/
├── jobs/
├── ml/
├── resumes/
├── static/
├── templates/
├── media/
├── screenshots/
├── manage.py
├── requirements.txt
└── README.md
```

---

# 📦 Requirements

* Django
* djangorestframework
* psycopg2-binary
* sentence-transformers
* transformers
* torch
* spacy
* scikit-learn
* PyMuPDF
* python-dotenv

---


# 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project helpful, please give it a star on GitHub!

# 🎓 AI-Powered College Recommendation System

An intelligent hybrid college recommendation system that recommends colleges based on:

- Academic performance
- Budget
- Preferred branch
- Preferred location
- Career goals
- Placement performance
- College profile similarity

## 🚀 Features

- Student profile based recommendations
- Eligibility filtering
- Budget filtering
- Hybrid weighted recommendation
- Content-based ML recommendation
- TF-IDF
- Cosine similarity
- Top-K ranking
- Explainable recommendations
- College comparison
- CSV download

## 🧠 Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- TF-IDF
- Cosine Similarity

## 🏗️ Architecture

Student Profile
↓
Data Preprocessing
↓
Eligibility & Budget Filtering
↓
Multi-Criteria Scoring
↓
TF-IDF Content Similarity
↓
Hybrid Ranking
↓
Top-K Recommendations
↓
Explanation

## ⚙️ Installation

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run:

streamlit run app.py

## 📊 Recommendation Factors

Academic Fit: 25%

Affordability: 20%

Location: 10%

Placement: 20%

Branch Preference: 15%

Career Goal: 10%

The final score is further combined with ML-based content similarity.

## 🔮 Future Improvements

- Collaborative filtering
- Real-time cutoff data
- Scholarship information
- Review sentiment analysis
- Knowledge graphs
- Learning-to-rank
- Personalized chatbot
- Real-time college information
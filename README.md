# 📺 IMDB TV Intelligence — Top 250 TV Shows Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.5.2-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-4AA564?style=for-the-badge)

**Interactive Analytics & Recommendation Engine for the Top Rated TV Shows in History**

</div>

---

## 📈 Project Overview

This **IMDB TV Intelligence Dashboard** provides a deep dive into the IMDB Top 250 TV Shows dataset. Built with **Streamlit** and **Plotly**, it combines data visualization with a machine learning-based recommendation system and AI-powered insights to help users find their next favorite show.

The dashboard analyzes 250 shows across various dimensions including ratings, votes, genre/type, and air dates spanning several decades.

### 🎯 Key Features
- **Interactive Visualizations**: 10 dynamic charts exploring ratings, popularity, and trends.
- **Advanced Filtering**: Filter by show type, decade, age rating, and popularity metrics.
- **Smart Recommendations**: A Content-Based Filtering system using TF-IDF and Cosine Similarity to suggest similar shows.
- **AI-Powered Insights**: Automated data analysis using LLMs via the OpenRouter API.
- **Search Engine**: Real-time search for quick access to specific shows.

---

## 🔍 Key Insights from the Data

### 📊 Global Metrics
- **Total Catalog**: 250 legendary shows
- **Average Rating**: ~8.92/10
- **Total Votes**: Over 150 Million community ratings
- **Decade Leader**: The 2010s produced more Top 250 shows than any other era.

### 🎬 Genre & Format Insights
- **TV Series vs. Mini Series**: Traditional TV series dominate the list, but high-budget Mini Series (like *Chernobyl* and *Band of Brothers*) frequently take the top-rated spots.
- **Hidden Gems**: Several highly-rated shows (Rating ≥ 9.0) have fewer than 200k votes, making them excellent candidates for new viewers seeking underrated masterpieces.

---

## 📂 Project Structure

```
imdb-tv-analytics/
│
├── 📄 app.py                  # Main Streamlit application
├── 📄 charts.py               # Plotly visualization engine
├── 📄 ai_insights.py          # AI analysis via OpenRouter
├── 📄 clean_data.py           # Data processing & ETL script
│
├── 📊 Data Files
│   ├── IMDB_cleaned.csv       # Processed dataset
│   └── IMDB_Top250_Tvshows.csv # Original raw dataset
│
├── 📦 Configuration
│   ├── requirements.txt       # Python dependencies
│   └── .gitignore             # Git ignore patterns
│
└── 📝 Documentation
    └── README.md              # Project documentation
```

---

## 🚀 How to Run Locally

### Step 1: Clone and Navigate
```bash
git clone https://github.com/pshreyas77/imdb-tv-analytics.git
cd imdb-tv-analytics
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch the App
```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack
- **Core**: Python 3.10+
- **Data**: Pandas
- **Visualization**: Plotly Express & Graph Objects
- **Frontend**: Streamlit
- **ML**: Scikit-Learn (TF-IDF Vectorization)
- **AI**: OpenAI/OpenRouter API

---

## 🤝 Connect
Built with ❤️ for TV enthusiasts. If you find this project useful, feel free to ⭐ star it on GitHub!

**[LinkedIn](https://linkedin.com/in/shreyas-patel) | [GitHub](https://github.com/pshreyas77)**

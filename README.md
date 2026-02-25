# 🎬 IMDB Top 250 TV Shows Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.5.2-3F4F75?style=for-the-badge&logo=plotly&logoColor=FF6F61)](https://plotly.com/)
[![Dash](https://img.shields.io/badge/Dash-4.0.0-FF6F61?style=for-the-badge&logo=dash&logoColor=FFFFFF)](https://dash.plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-4AA564?style=for-the-badge)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-February%202026-4AA564?style=for-the-badge)](https://github.com/pshreyas77/imdb-tv-analytics)

**Interactive Python Dashboard for Analyzing IMDB Top 250 TV Shows | Built with Plotly Dash**

---

## 📈 Project Overview

This project is a comprehensive **IMDB TV Shows Analytics Dashboard** that analyzes and visualizes trends, ratings, and patterns from the IMDB Top 250 TV Shows dataset. The dashboard provides interactive data visualizations that help viewers discover shows, understand rating distributions, identify trends by decade, and analyze relationships between ratings and popularity.

With detailed show data spanning multiple decades, genres, and ratings, this analysis uncovers insights about what makes top-rated television shows successful.

### 🎯 Project Goals
- Analyze IMDB Top 250 TV Shows data across multiple dimensions
- Build an interactive dashboard for real-time TV show analytics
- Generate actionable insights about show ratings, trends, and patterns
- Demonstrate end-to-end data science and web development skills
- Create reusable visualization components

---

## 🖥️ Dashboard Features

The interactive dashboard includes:
- **Top Rated Shows Chart** - Visualization of highest-rated TV shows
- **Rating Distribution** - Histogram showing rating spread
- **Shows Per Decade** - Trend analysis over time
- **Rating vs Votes** - Correlation between votes and ratings
- **Type Comparison** - Analysis by show type/genre
- **Age Distribution** - Show premiere year distribution
- **Average Ratings by Decade** - Historical rating trends
- **Rating Tier Analysis** - Categorization of show quality tiers
- **Episodes vs Rating** - Relationship between episode count and ratings

---

## 🚠 Tech Stack

### Core Technologies
| Technology | Purpose | Version |
|------------|---------|----------|
| **Python** | Programming Language | 3.10+ |
| **Pandas** | Data Manipulation & Cleaning | 2.3.3 |
| **Plotly** | Interactive Visualizations | 6.5.2 |
| **Dash** | Web Application Framework | 4.0.0 |
| **Gunicorn** | Production WSGI Server | 21.2.0 |
| **Scikit-learn** | Machine Learning & Text Analysis | 1.7.2 |
| **OpenAI** | AI Insights Generation | 1.12.0 |

### Deployment
| Platform | Service |
|----------|----------|
| **Render** | Cloud Hosting |
| **GitHub** | Version Control |

---

## 📂 Project Structure

```
imdb-tv-analytics/
│
├── 📄 app.py                    # Main Dash application (production-ready)
├── 📄 charts.py                 # Chart creation and visualization functions
├── 📄 ai_insights.py            # AI-powered insights generation
│
├── 📈 Data Files
│   ├── IMDB_cleaned.csv         # Cleaned IMDB Top 250 dataset
│   ├── kpi_summary.csv          # Pre-calculated KPIs
│   └── hr_data_cleaned.csv      # Auxiliary HR reference data
│
├── 🔄 Data Processing Phases
│   ├── phase1_explore.py        # Phase 1: EDA & Data Profiling
│   ├── phase2_cleaning.py       # Phase 2: Data Cleaning & Feature Engineering
│   ├── phase3_kpis.py           # Phase 3: KPI Calculations
│   └── phase4_dashboard.py      # Phase 4: Dashboard Building
│
├── 📋 Configuration Files
│   ├── requirements.txt          # Python dependencies
│   ├── .gitignore               # Git ignore patterns
│   └── Procfile                 # Deployment configuration
│
└── 📝 Documentation
    └── README.md                # This file
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- Git installed
- Terminal/Command Prompt

### Step 1: Clone the Repository
```bash
git clone https://github.com/pshreyas77/imdb-tv-analytics.git
cd imdb-tv-analytics
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard
```bash
python app.py
```

### Step 5: Access Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:8050
```

---

## 🔍 Key Insights & Findings

### 📈 Dataset Overview
- **Total Shows Analyzed**: 250+ (IMDB Top 250 TV Shows)
- **Data Spans**: Multiple decades of television history
- **Key Metrics**: Ratings, Votes, Episode Counts, Premiere Years, Genres

### 🎯 Dashboard Analytics Include:
- **Rating Distribution Analysis** - Shows are predominantly highly-rated (8.0+)
- **Temporal Trends** - How show quality has evolved over decades
- **Vote-Rating Correlation** - Popular shows aren't always the highest-rated
- **Genre Performance** - Which genres dominate the top 250
- **Episode Length Impact** - How episode count affects ratings

---

## 💼 Skills Demonstrated

### Technical Skills
- ✅ Python Programming (Advanced)
- ✅ Data Cleaning & Preprocessing
- ✅ Exploratory Data Analysis (EDA)
- ✅ Interactive Dashboard Development
- ✅ Data Visualization (Plotly)
- ✅ Web Application Development (Dash)
- ✅ Machine Learning Text Analysis (scikit-learn)
- ✅ AI Integration (OpenAI API)

### Data Science Skills
- ✅ Feature Engineering
- ✅ Data Aggregation & Grouping
- ✅ Statistical Analysis
- ✅ Insight Generation
- ✅ KPI Calculation

### DevOps & Deployment
- ✅ Git Version Control
- ✅ Cloud Deployment (Render)
- ✅ Environment Management
- ✅ Production Setup

---

## 📈 Dataset Details

| Attribute | Description |
|-----------|-------------|
| **Source** | IMDB Top 250 TV Shows |
| **Records** | 250+ television shows |
| **Features** | Show titles, ratings, vote counts, year, genre, episode info |
| **Time Period** | Multiple decades of TV history |
| **Target Analysis** | Rating trends, popularity metrics, temporal patterns |

---

## 🚀 Deployment

The dashboard can be deployed to Render Cloud Platform:

### Deployment Steps:
1. Push code to GitHub repository
2. Connect repository to Render.com
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:server`
5. Deploy and access via provided URL

---

## 🤝 Connect With Me

**Let's collaborate and build amazing data projects!**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/shreyas-patel)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/pshreyas77)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:shreyas@example.com)

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If you found this project helpful or inspiring, please give it a ⭐ star on GitHub!

---

**Built with ❤️ using Python, Pandas, Plotly & Dash**

*Transforming IMDB Data into Interactive Visualizations*

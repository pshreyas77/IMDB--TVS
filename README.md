# 📊 HR Analytics Dashboard — Employee Attrition Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B)
![Pandas](https://img.shields.io/badge/Pandas-2.3.3-150458?style=for-the-badge&logo=pandas&logoColor==white)
![Plotly](https://img.shields.io/badge/Plotly-6.5.2-3F4F75?style=for-the-badge&logo=plotly&logoColor=FF6F61)
![Dash](httpsx://img.shields.io/badge/Dash-4.0.0-FF6F61?style=for-the-badge&logo=dash&logoColor=FFFFFF)
![License](https://img.shields.io/badge/License-MIT-4AA564?style=for-the-badge)
![Last Updated](https://img.shields.io/badge/Last%20Updated-February%202026-4AA564?style=for-the-badge)

**Interactive Python Dashboard for Analyzing Employee Attrition | Built with Plotly Dash**

🔴 **[LIVE DEMO: View Dashboard](https://your-app-name.onrender.com)**

</div>

---

## 📈 Project Overview

This project is a comprehensive **HR Analytics Dashboard** that analyzes employee attrition patterns using the IBM HR Analytics Employee Attrition dataset. The dashboard provides interactive data visualizations and KPIs that help HR professionals identify turnover risks and make data-driven retention decisions.

With **1,470 employee records** and **35 features** spanning demographics, job satisfaction, compensation, and tenure, this analysis uncovers critical insights about what drives employees to leave the organization.

### 🎯 Project Goals
- Analyze employee attrition patterns across multiple dimensions
- Build an interactive dashboard for real-time HR analytics
- Generate actionable business recommendations
- Demonstrate end-to-end data science and BI skills

---

## 🖥️ Dashboard Preview

<div align="center">

*Interactive HR Analytics Dashboard with real-time filtering and visualizations*

![Dashboard Screenshot](https://via.placeholder.com/900x600.png?text=HR+Analytics+Dashboard+Screenshot)

**Figure 1:** Main dashboard view showing KPIs, filters, and attrition analysis

</div>

---

## 🔍 Key Insights Discovered

### 📊 Overall Metrics

| Metric | Value |
|--------|-------|
| Total Employees | 1,470 |
| Attrition Rate | 18.18% |
| Active Employees | 1,204 |
| Average Age | 35.9 years |
| Average Monthly Income | $6,500 |
| Average Tenure | 7.0 years |

### 🚨 Critical Findings

#### 1. **Department Analysis**
- **Sales** has the highest attrition at **40%** — nearly 3x the company average
- **Research & Development** attrition is **14.29%** — relatively stable
- **Human Resources** has the lowest attrition at **10%**

#### 2. **Age Group Risk Assessment**
| Age Group | Attrition Rate | Risk Level |
|-----------|---------------|------------|
| 18-30 | 11.11% | 🟢 Low |
| 31-40 | 26.67% | 🔴 High |
| 41-50 | 16.67% | 🟡 Medium |
| 50+ | 0% | 🟢 Stable |

**Insight:** Employees aged 31-40 are the most at-risk group

#### 3. **Overtime Impact — Major Finding**
- **With Overtime:** 36.36% attrition rate
- **Without Overtime:** 9.09% attrition rate

> 💡 **Employees working overtime are 4x more likely to leave!**

#### 4. **Compensation Correlation**
- Low salary (≤$5K/month): 23.81% attrition
- Medium salary ($5K-$10K/month): 14.29% attrition  
- High salary ($10K-$15K/month): 8% attrition
- Very High salary (>$15K/month): 0% attrition

#### 5. **Job Role Risk Matrix**
- 🔴 Sales Representatives: 100% attrition (critical!)
- 🔴 Research Scientists: 25% attrition
- 🟡 Laboratory Technicians: 16.67% attrition
- 🟢 Managers: 0% attrition
- 🟢 Healthcare Representatives: 0% attrition

#### 6. **Gender Analysis**
- Male: 19.05% attrition rate
- Female: 16.67% attrition rate

---

## 🛠️ Tech Stack

### Core Technologies
| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Programming Language | 3.10+ |
| **Pandas** | Data Manipulation & Cleaning | 2.3.3 |
| **Plotly** | Interactive Visualizations | 6.5.2 |
| **Dash** | Web Application Framework | 4.0.0 |
| **Gunicorn** | Production WSGI Server | 21.2.0 |

### Deployment
| Platform | Service |
|----------|---------|
| **Render** | Cloud Hosting (Free Tier) |
| **GitHub** | Version Control & Repository |

---

## 📂 Project Structure

```
hr-analytics-dashboard/
│
├── 📄 app.py                          # Main Dash application (production-ready)
├── 📄 phase1_explore.py               # Phase 1: Data exploration & profiling
├── 📄 phase2_cleaning.py               # Phase 2: Data cleaning & feature engineering
├── 📄 phase3_kpis.py                   # Phase 3: KPI calculations & metrics
│
├── 📊 Data Files
│   ├── WA_Fn-UseC_-HR-Employee-Attrition.csv    # Original IBM dataset
│   ├── hr_data_cleaned.csv            # Cleaned dataset
│   └── kpi_summary.csv                # Pre-calculated KPIs
│
├── 📦 Configuration Files
│   ├── requirements.txt                # Python dependencies
│   ├── Procfile                       # Deployment configuration
│   └── .gitignore                     # Git ignore patterns
│
└── 📝 Documentation
    └── README.md                      # This file
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- Git installed
- Terminal/Command Prompt

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/hr-analytics-dashboard.git
cd hr-analytics-dashboard
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

### Step 4: Launch the Dashboard
```bash
python app.py
```

### Step 5: View in Browser
```
http://127.0.0.1:8050
```

---

## 💼 Business Recommendations

Based on the analysis, here are **actionable recommendations** for HR leadership:

### 🔴 Immediate Actions (This Month)

1. **Sales Team Retention Program**
   - Implement immediate retention bonuses for sales staff
   - Review sales quota workload and compensation structure
   - Conduct 1:1 meetings with all sales representatives

2. **Overtime Reduction Initiative**
   - Audit current overtime practices
   - Implement stricter overtime approval process
   - Hire additional staff to distribute workload

3. **Compensation Analysis**
   - Review salary bands for high-risk roles
   - Conduct market rate analysis for sales positions

### 🟡 Short-Term (1-3 Months)

4. **Targeted Retention for Ages 31-40**
   - Create mid-career development programs
   - Offer career path clarity and promotion opportunities
   - Implement mentorship programs

5. **Manager Training**
   - Train managers on early warning signs of attrition
   - Implement regular check-ins with at-risk employees
   - Focus on work-life balance initiatives

### 🟢 Long-Term Strategy (3-12 Months)

6. **Predictive Analytics**
   - Build ML model to predict at-risk employees
   - Create early intervention program
   - Implement retention scorecards

7. **Employee Engagement**
   - Quarterly satisfaction surveys
   - Anonymous feedback channels
   - Continuous improvement based on feedback

---

## 🎯 Skills Demonstrated

### Technical Skills
- ✅ Python Programming
- ✅ Data Cleaning & Preprocessing
- ✅ Exploratory Data Analysis (EDA)
- ✅ Interactive Dashboard Development
- ✅ KPI Design & Calculation
- ✅ Data Visualization

### Business Skills
- ✅ Insight Generation
- ✅ Data-Driven Decision Making
- ✅ Business Recommendations
- ✅ Stakeholder Communication
- ✅ Problem-Solving

### DevOps Skills
- ✅ Git Version Control
- ✅ Cloud Deployment (Render)
- ✅ Production Environment Setup
- ✅ Documentation

---

## 📊 Dataset Details

| Attribute | Description |
|-----------|-------------|
| **Source** | IBM HR Analytics Employee Attrition Dataset (Kaggle) |
| **Records** | 1,470 employees |
| **Features** | 35 variables |
| **Target** | Attrition (Yes/No) |
| **Categories** | Demographics, Job Satisfaction, Compensation, Tenure |

---

## 🚀 Deployment

The dashboard is deployed on **Render** (free tier) and accessible 24/7.

### Live URL
```
https://your-app-name.onrender.com
```

### Deployment Process
1. Push code to GitHub
2. Connect repository to Render.com
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:server`
5. Deploy and share the URL!

---

## 🤝 Connect With Me

<div align="center">

**Let's build something great together!**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.email@example.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://your-portfolio.com)

</div>

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If this project helped you learn something new or you're inspired, give it a ⭐ star on GitHub!

---

<div align="center">

**Built with ❤️ using Python, Pandas, Plotly & Dash**

*Transforming HR Data into Actionable Insights*

</div>
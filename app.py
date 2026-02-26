# ── IMPORTS ──
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from charts import (
    create_top_rated_chart, create_top_voted_chart, 
    create_rating_distribution, create_shows_per_decade, 
    create_rating_vs_votes, create_type_comparison, 
    create_age_distribution, create_avg_rating_decade, 
    create_rating_tier, create_episodes_vs_rating
)
from ai_insights import generate_insights

# ── RECOMMENDATION SYSTEM ──
@st.cache_data
def build_recommendation_model(df):
    df_rec = df.copy()
    df_rec = df_rec.fillna('')
    df_rec['features'] = (
        df_rec['Type'].astype(str) + ' ' + 
        df_rec['Decade'].astype(str) + ' ' + 
        df_rec['Age'].astype(str) + ' ' +
        df_rec['Rating_Tier'].astype(str)
    )
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_rec['features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim, df_rec

def get_recommendations(title, df, cosine_sim, df_rec, n=5):
    if title not in df_rec['Title'].values:
        return []
    idx = df_rec[df_rec['Title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [(i, score) for i, score in sim_scores if i != idx]
    show_indices = [i[0] for i in sim_scores[:n]]
    return df.iloc[show_indices][['Title','Rating','Votes','Type','Decade','Age']]

# ── SESSION STATE ──
if 'insights' not in st.session_state:
    st.session_state['insights'] = None

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="IMDB Top 250 TV Shows · Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #050505 !important;
    color: #C0C0C0 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.main .block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 100% !important;
}

/* ── KPI METRIC CARDS ── */
[data-testid="metric-container"] {
    background: linear-gradient(160deg, #0C0C0C 0%, #111 100%) !important;
    border: 1px solid #1A1A1A !important;
    border-left: 3px solid #E50914 !important;
    border-radius: 6px !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(229,9,20,0.15) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #888 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2.6rem !important;
    color: #FFF !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #000 !important;
    border-right: 1px solid #111 !important;
}
[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #777 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSlider > div {
    background: transparent !important;
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1A1A1A !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #555 !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.9rem 1.4rem !important;
    transition: color 0.2s !important;
}
[data-baseweb="tab"]:hover { color: #AAA !important; }
[aria-selected="true"] {
    color: #E50914 !important;
    border-bottom: 2px solid #E50914 !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input {
    background: #0A0A0A !important;
    border: 1px solid #222 !important;
    border-radius: 4px !important;
    color: #E0E0E0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #E50914 !important;
    box-shadow: 0 0 0 1px rgba(229,9,20,0.3) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1A1A1A !important;
    border-radius: 6px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #444; }

/* ── PLOTLY MODEBAR ── */
.modebar { display: none !important; }

/* ── BUTTONS ── */
.stButton > button,
.stDownloadButton > button {
    background: #E50914 !important;
    border: none !important;
    color: #FFFFFF !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 0.5rem 2rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 10px rgba(229,9,20,0.3) !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #B20710 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(229,9,20,0.4) !important;
}

/* ── DIVIDERS ── */
hr { border-color: #1A1A1A !important; }

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {
    background: #0A0A0A !important;
    border-color: #222 !important;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    return pd.read_csv(
        'IMDB_cleaned.csv', 
        encoding='latin-1'
    )

df = load_data()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 1rem; border-bottom:1px solid #141414; margin-bottom:1.2rem;">
        <div style="font-family:'Bebas Neue',sans-serif;
             font-size:1.8rem; letter-spacing:0.15em;
             color:#E50914; line-height:1;">
             🎬 IMDB
        </div>
        <div style="font-family:'DM Mono',monospace;
             font-size:0.55rem; letter-spacing:0.2em;
             color:#555; margin-top:0.3rem; text-transform:uppercase;">
             TV Intelligence Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    type_filter = st.selectbox(
        "Show Type",
        ["All", "TV Series", "TV Mini Series"]
    )
    
    # Build decade list dynamically from data
    all_decades = sorted([d for d in df['Decade'].dropna().unique() if d != 'Unknown'])
    decade_filter = st.selectbox(
        "Decade",
        ["All"] + all_decades + ["Unknown"]
    )
    
    age_filter = st.selectbox(
        "Age Rating",
        ["All"] + sorted(df['Age'].dropna().unique().tolist())
    )
    min_rating = st.slider(
        "Min Rating", 8.5, 9.5, 8.5, 0.1,
        format="%.1f"
    )
    min_votes = st.slider(
        "Min Votes", 0, int(df['Votes'].max()),
        0, 10000
    )

# ── FILTER DATA ──
df_f = df.copy()
if type_filter != "All":
    df_f = df_f[df_f['Type'] == type_filter]
if decade_filter != "All":
    df_f = df_f[df_f['Decade'] == decade_filter]
if age_filter != "All":
    df_f = df_f[df_f['Age'] == age_filter]
df_f = df_f[df_f['Rating'] >= min_rating]
df_f = df_f[df_f['Votes'] >= min_votes]

# ── EMPTY STATE ──
if len(df_f) == 0:
    st.markdown("""
    <div style="padding:4rem 2rem; text-align:center; background:#0A0A0A;
         border:1px solid #1A1A1A; border-radius:8px; margin:3rem auto; max-width:500px;">
      <div style="font-size:3rem; margin-bottom:1rem;">🎬</div>
      <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem;
           color:#E50914; letter-spacing:0.1em;">
           NO SHOWS FOUND
      </div>
      <p style="font-family:'DM Mono',monospace; font-size:0.72rem;
           color:#555; margin-top:0.8rem; line-height:1.6;">
           No shows match your current filters.<br>
           Try adjusting the criteria in the sidebar.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── HEADER ──
st.markdown(f"""
<div style="padding:1.2rem 0 0.8rem; border-bottom:1px solid #1A1A1A;
     margin-bottom:1.5rem; display:flex; align-items:flex-end;
     justify-content:space-between;">
  <div>
    <div style="font-family:'DM Mono',monospace;
         font-size:0.55rem; letter-spacing:0.25em;
         text-transform:uppercase; color:#E50914;
         margin-bottom:0.3rem;">
         IMDB · TOP 250 · TV INTELLIGENCE
    </div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:2.2rem; letter-spacing:0.08em;
         color:#FFF; line-height:1;">
         TV Shows Dashboard
    </div>
  </div>
  <div style="text-align:right;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.6rem; color:#555;
         letter-spacing:0.1em;">
         {len(df_f)} <span style="color:#333">of</span> 250 <span style="color:#333">shows</span>
         <span style="color:#222; margin:0 0.5rem;">·</span>
         AVG <span style="color:#E50914">{df_f['Rating'].mean():.2f}</span>
         <span style="color:#222; margin:0 0.5rem;">·</span>
         {df_f['Votes'].sum()/1e6:.1f}M <span style="color:#333">votes</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ──
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("📺 Total Shows", f"{len(df_f):,}")
with k2:
    st.metric("⭐ Avg Rating", 
              f"{df_f['Rating'].mean():.2f}" if len(df_f) > 0 else "N/A")
with k3:
    st.metric("🗳️ Total Votes", 
              f"{df_f['Votes'].sum()/1e6:.1f}M")
with k4:
    st.metric("🎞️ Avg Episodes",
              f"{int(df_f['Episodes'].mean())}"
              if len(df_f) > 0 else "N/A")

st.markdown("<div style='margin:0.8rem 0'></div>", unsafe_allow_html=True)

# ── SUMMARY STATS ──
best_decade = "N/A"
if len(df_f) > 0:
    valid_decades = df_f[df_f['Decade'].notna() & (df_f['Decade'] != 'Unknown')]['Decade']
    if len(valid_decades) > 0:
        best_decade = valid_decades.value_counts().index[0]

top_show = df_f.nlargest(1,'Rating').iloc[0] if len(df_f) > 0 else None
top_voted = df_f.nlargest(1,'Votes').iloc[0] if len(df_f) > 0 else None
common_age = df_f['Age'].value_counts().index[0] if len(df_f) > 0 else "N/A"

st.markdown(f"""
<div style="display:grid; grid-template-columns:repeat(4,1fr);
     gap:0; background:#080808; border:1px solid #141414;
     border-radius:6px; margin-bottom:1.5rem; overflow:hidden;">
  <div style="padding:1rem 1.4rem; border-right:1px solid #141414;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.55rem; letter-spacing:0.18em;
         text-transform:uppercase; color:#666;
         margin-bottom:0.4rem;">🏆 Highest Rated</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:1rem; letter-spacing:0.05em;
         color:#CCC; line-height:1.3;">
         {top_show['Title'] if top_show is not None else 'N/A'}
    </div>
    <div style="font-family:'DM Mono',monospace;
         font-size:0.65rem; color:#E50914; margin-top:0.2rem;">
         {top_show['Rating'] if top_show is not None else ''}
    </div>
  </div>
  <div style="padding:1rem 1.4rem; border-right:1px solid #141414;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.55rem; letter-spacing:0.18em;
         text-transform:uppercase; color:#666;
         margin-bottom:0.4rem;">🔥 Most Popular</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:1rem; letter-spacing:0.05em;
         color:#CCC; line-height:1.3;">
         {top_voted['Title'] if top_voted is not None else 'N/A'}
    </div>
    <div style="font-family:'DM Mono',monospace;
         font-size:0.65rem; color:#E50914; margin-top:0.2rem;">
         {f"{top_voted['Votes']/1e6:.1f}M votes" if top_voted is not None else ''}
    </div>
  </div>
  <div style="padding:1rem 1.4rem; border-right:1px solid #141414;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.55rem; letter-spacing:0.18em;
         text-transform:uppercase; color:#666;
         margin-bottom:0.4rem;">📅 Best Decade</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:1.3rem; letter-spacing:0.05em;
         color:#CCC;">{best_decade}</div>
  </div>
  <div style="padding:1rem 1.4rem;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.55rem; letter-spacing:0.18em;
         text-transform:uppercase; color:#666;
         margin-bottom:0.4rem;">🎭 Common Rating</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:1.3rem; letter-spacing:0.05em;
         color:#CCC;">{common_age}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── EXPORT BUTTON ──
_, _, _, _, _, export_col = st.columns([1,1,1,1,1,1])
with export_col:
    csv_data = df_f.to_csv(index=False)
    st.download_button(
        "↓ Export CSV",
        data=csv_data,
        file_name="imdb_top250_filtered.csv",
        mime="text/csv",
        key="export_btn",
        width='stretch'
    )

# ── TABS ──
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Trends", "Deep Dive", 
    "Data Explorer", "AI Insights", "Search"
])

# ━━ TAB 1 — OVERVIEW ━━
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_top_rated_chart(df_f), width='stretch')
    with c2:
        st.plotly_chart(create_rating_distribution(df_f), width='stretch')
    
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(create_type_comparison(df_f), width='stretch')
    with c4:
        st.plotly_chart(create_age_distribution(df_f), width='stretch')

# ━━ TAB 2 — TRENDS ━━
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_shows_per_decade(df_f), width='stretch')
    with c2:
        st.plotly_chart(create_avg_rating_decade(df_f), width='stretch')
    
    st.plotly_chart(create_rating_tier(df_f), width='stretch')

# ━━ TAB 3 — DEEP DIVE ━━
with tab3:
    st.plotly_chart(create_rating_vs_votes(df_f), width='stretch')
    
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_episodes_vs_rating(df_f), width='stretch')
    with c2:
        st.plotly_chart(create_top_voted_chart(df_f), width='stretch')
    
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin:1.5rem 0 0.8rem; padding-bottom:0.5rem;
         border-bottom:1px solid #1A1A1A;">
         📋 TOP 20 SHOWS BY RATING
    </div>
    """, unsafe_allow_html=True)
    top20 = df_f.nlargest(20, 'Rating')[['Title','Rating','Votes','Episodes','Type','Decade','Age']]
    st.dataframe(top20, width='stretch', hide_index=True)

# ━━ TAB 4 — DATA EXPLORER ━━
with tab4:
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin-bottom:1rem;">
         📊 DATASET OVERVIEW
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset stats
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.metric("Rows", f"{len(df_f):,}")
    with d2:
        st.metric("Columns", f"{len(df_f.columns)}")
    with d3:
        st.metric("Rating Range", f"{df_f['Rating'].min():.1f} – {df_f['Rating'].max():.1f}")
    with d4:
        st.metric("Vote Range", f"{df_f['Votes'].min():,} – {df_f['Votes'].max():,}")
    
    st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)
    
    # Column descriptions
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin:1rem 0 0.5rem;">
         📑 COLUMN REFERENCE
    </div>
    """, unsafe_allow_html=True)
    
    col_desc = {
        'Title': 'Show name', 'Rating': 'IMDB score (8.5–9.5)',
        'Votes': 'Total community votes', 'Episodes': 'Episode count',
        'Type': 'TV Series or Mini Series', 'Decade': 'Premiere decade',
        'Age': 'Age rating (PG, 15, 18, etc.)', 'Rating_Tier': 'Elite / Excellent / Great / Good',
    }
    cols_html = ""
    for col, desc in col_desc.items():
        cols_html += f"""
        <div style="display:flex; justify-content:space-between; padding:0.4rem 0.8rem;
             border-bottom:1px solid #111; font-size:0.78rem;">
            <span style="font-family:'DM Mono',monospace; color:#E50914;">{col}</span>
            <span style="color:#666;">{desc}</span>
        </div>"""
    st.markdown(f'<div style="background:#080808; border:1px solid #1A1A1A; border-radius:6px; overflow:hidden; margin-bottom:1.5rem;">{cols_html}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin:1rem 0 0.5rem;">
         🗂️ FULL DATASET
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_f, width='stretch', hide_index=True)

# ━━ TAB 5 — AI INSIGHTS ━━
with tab5:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:1.2rem;">
        <div style="font-family:'Bebas Neue',sans-serif;
             font-size:1.4rem; letter-spacing:0.1em; color:#E50914;">
             🤖 AI ANALYSIS ENGINE
        </div>
        <div style="font-family:'DM Mono',monospace;
             font-size:0.55rem; letter-spacing:0.12em;
             color:#444; text-transform:uppercase; padding-top:0.2rem;">
             Powered by OpenRouter API
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    api_key = st.text_input(
        "Enter OpenRouter API Key",
        type="password",
        placeholder="sk-or-v1-..."
    )
    
    generate_btn = st.button(
        "Generate AI Insights",
        key="ai_btn"
    )
    
    if generate_btn:
        if not api_key:
            st.error("Please enter your OpenRouter API key first.")
        else:
            with st.spinner("Generating insights..."):
                try:
                    insights = generate_insights(df_f, api_key)
                    st.session_state['insights'] = insights
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if 'insights' in st.session_state and st.session_state['insights']:
        items = [
            i.strip().lstrip("•-▸0123456789. ")
            for i in st.session_state['insights'].split("\n")
            if i.strip()
        ]
        for i, item in enumerate(items[:5]):
            st.markdown(f"""
            <div style="padding:1rem 1.2rem;
                 margin-bottom:0.6rem;
                 background:linear-gradient(135deg, #0A0A0A, #0E0E0E);
                 border:1px solid #1A1A1A;
                 border-left:3px solid #E50914;
                 border-radius:6px;
                 font-family:'DM Sans',sans-serif;
                 font-size:0.85rem;
                 color:#AAA;
                 line-height:1.6;">
                <span style="font-family:'Bebas Neue',sans-serif;
                     font-size:1.2rem; color:#E50914;
                     margin-right:0.8rem;">
                     {str(i+1).zfill(2)}
                </span>
                {item}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin:1.5rem 0'></div>", unsafe_allow_html=True)
    
    # Hidden Gems
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin-bottom:0.8rem; padding-bottom:0.5rem;
         border-bottom:1px solid #1A1A1A;">
         💎 HIDDEN GEMS — Rating ≥ 9.0 · Votes < 200K
    </div>
    """, unsafe_allow_html=True)
    
    gems = df_f[
        (df_f['Rating'] >= 9.0) &
        (df_f['Votes'] < 200000)
    ][['Title','Rating','Votes','Type','Decade']]
    
    if len(gems) > 0:
        st.dataframe(gems, width='stretch', hide_index=True)
    else:
        st.info("No hidden gems match the current filter.")

# ━━ TAB 6 — SEARCH & RECOMMENDATIONS ━━
with tab6:
    # Search section
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin-bottom:0.8rem;">
         🔍 SEARCH SHOWS
    </div>
    """, unsafe_allow_html=True)
    
    query = st.text_input(
        "Search by title",
        placeholder="e.g. Breaking Bad, Game of Thrones...",
        label_visibility="collapsed"
    )
    
    if query and len(query) > 0:
        results = df_f[
            df_f['Title'].str.contains(query, case=False, na=False)
        ].sort_values('Rating', ascending=False)
        
        if len(results) == 0:
            st.markdown(f"""
            <div style="padding:2rem; text-align:center; background:#0A0A0A;
                 border:1px solid #1A1A1A; border-radius:6px; margin:1rem 0;">
                <div style="font-size:1.5rem; margin-bottom:0.5rem;">🔍</div>
                <div style="font-family:'DM Mono',monospace; font-size:0.75rem;
                     color:#555;">No shows found for "<span style="color:#E50914">{query}</span>"</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-family:'DM Mono',monospace; font-size:0.7rem;
                 color:#666; margin:0.6rem 0 1rem;">
                 Found <span style="color:#E50914; font-weight:600;">{len(results)}</span> result{'s' if len(results) != 1 else ''}
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(
                results[['Title','Rating','Votes','Episodes','Type','Decade']],
                width='stretch', hide_index=True
            )
    
    st.markdown("<div style='margin:1.5rem 0; border-top:1px solid #141414;'></div>", unsafe_allow_html=True)
    
    # Recommender section
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
         letter-spacing:0.15em; text-transform:uppercase; color:#666;
         margin-bottom:0.8rem;">
         🎯 SIMILAR SHOWS RECOMMENDER
    </div>
    """, unsafe_allow_html=True)
    
    cosine_sim, df_rec = build_recommendation_model(df)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_show = st.selectbox(
            "Select a show:",
            options=sorted(df['Title'].tolist()),
            label_visibility="collapsed"
        )
    with col2:
        num_recs = st.selectbox(
            "Results:",
            options=[3, 5, 10],
            index=1
        )
    
    if selected_show:
        recommendations = get_recommendations(
            selected_show, df, cosine_sim, df_rec, n=num_recs
        )
        
        # Show card for selected show
        show_info = df[df['Title'] == selected_show].iloc[0]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #0A0A0A, #111);
             border:1px solid #1A1A1A; border-left:3px solid #E50914;
             border-radius:6px; padding:1rem 1.4rem; margin:0.8rem 0 1.2rem;">
            <div style="font-family:'DM Mono',monospace; font-size:0.55rem;
                 color:#555; text-transform:uppercase; letter-spacing:0.15em;
                 margin-bottom:0.4rem;">SHOWING SIMILAR TO</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:1.4rem;
                 color:#FFF; letter-spacing:0.05em;">{selected_show}</div>
            <div style="font-family:'DM Mono',monospace; font-size:0.7rem;
                 color:#888; margin-top:0.3rem;">
                 ⭐ {show_info['Rating']}
                 <span style="color:#333; margin:0 0.5rem;">·</span>
                 {show_info['Type']}
                 <span style="color:#333; margin:0 0.5rem;">·</span>
                 {show_info['Episodes']} eps
                 <span style="color:#333; margin:0 0.5rem;">·</span>
                 {show_info['Votes']:,} votes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if len(recommendations) > 0:
            st.dataframe(recommendations, width='stretch', hide_index=True)
        else:
            st.info("No recommendations available for this show.")

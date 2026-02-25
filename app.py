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
    page_title="IMDB Top 250 TV Shows",
    page_icon="▣",
    layout="wide"
)

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #000 !important;
    color: #E0E0E0 !important;
}
#MainMenu, footer, header { visibility: hidden; }

.main .block-container {
    padding-top: 0.5rem !important;
    padding: 0.5rem 2rem !important;
    max-width: 100% !important;
}

[data-testid="metric-container"] {
    background: #0A0A0A !important;
    border: 1px solid #1A1A1A !important;
    border-top: 1px solid #333 !important;
    border-radius: 4px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #333 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2.2rem !important;
    color: #E8E8E8 !important;
}
[data-testid="stMetricDelta"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid #141414 !important;
}
[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #333 !important;
}

[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1A1A1A !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #333 !important;
    background: transparent !important;
    border-bottom: 1px solid transparent !important;
    padding: 0.6rem 1.2rem !important;
}
[aria-selected="true"] {
    color: #E0E0E0 !important;
    border-bottom: 1px solid #E0E0E0 !important;
}

.stTextInput > div > div > input {
    background: #0A0A0A !important;
    border: 1px solid #1A1A1A !important;
    border-radius: 3px !important;
    color: #CCC !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #444 !important;
    box-shadow: none !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #141414 !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #1A1A1A; }
::-webkit-scrollbar-thumb:hover { background: #333; }

.modebar { display: none !important; }

.stButton > button,
.stDownloadButton > button {
    background: #1A1A1A !important;
    border: 1px solid #444444 !important;
    color: #FFFFFF !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #2A2A2A !important;
    border-color: #666666 !important;
    color: #FFFFFF !important;
}
.stButton > button:active,
.stDownloadButton > button:active {
    background: #333333 !important;
    border-color: #888888 !important;
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    return pd.read_csv(
        '/home/sunny77/IMDB_cleaned.csv', 
        encoding='latin-1'
    )

df = load_data()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:1rem;letter-spacing:0.2em;
         color:#222;padding:1rem 0 0.8rem;
         border-bottom:1px solid #141414;
         margin-bottom:1rem;">
         FILTERS
    </div>
    """, unsafe_allow_html=True)
    
    type_filter = st.selectbox(
        "Show Type",
        ["All", "TV Series", "TV Mini Series"]
    )
    decade_filter = st.selectbox(
        "Decade",
        ["All", "1990s", "2000s", "2010s", "2020s"]
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
    <div style="padding:3rem;text-align:center;background:#0A0A0A;
         border:1px solid #1A1A1A;border-radius:4px;margin:2rem 0;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#333;">
          NO SHOWS FOUND
      </div>
      <p style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#444;margin-top:1rem;">
          No shows match your filters. Try adjusting the criteria.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── HEADER ──
st.markdown("""
<div style="padding:1rem 0 0.5rem;
     border-bottom:1px solid #1A1A1A;
     margin-bottom:1rem;
     display:flex;
     align-items:center;
     justify-content:space-between;">
  <div>
    <div style="font-family:'DM Mono',monospace;
         font-size:0.52rem;letter-spacing:0.2em;
         text-transform:uppercase;color:#2A2A2A;
         margin-bottom:0.2rem;">
         IMDB · TV Intelligence
    </div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:1.6rem;letter-spacing:0.12em;
         color:#FFF;line-height:1;">
         Top 250 TV Shows
    </div>
  </div>
  <div style="font-family:'DM Mono',monospace;
       font-size:0.55rem;color:#222;
       letter-spacing:0.1em;text-align:right;">
       250 SHOWS · IMDB DATA
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
        use_container_width=True
    )

# ── FILTER FEEDBACK ──
st.markdown(f"""
<div style="font-family:'DM Mono',monospace;
     font-size:0.58rem;color:#2A2A2A;
     letter-spacing:0.08em;padding:0.5rem 0 1rem;
     border-bottom:1px solid #0F0F0F;">
  Showing {len(df_f)} of 250 shows
  <span style="margin:0 1rem;color:#141414">·</span>
  Avg Rating {df_f['Rating'].mean():.2f}
  <span style="margin:0 1rem;color:#141414">·</span>
  {df_f['Votes'].sum()/1e6:.1f}M total votes
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ──
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Total Shows", f"{len(df_f):,}")
with k2:
    avg = df_f['Rating'].mean()
    st.metric("Avg Rating", 
              f"{avg:.2f}" if len(df_f) > 0 else "N/A")
with k3:
    st.metric("Total Votes", 
              f"{df_f['Votes'].sum()/1e6:.1f}M")
with k4:
    st.metric("Avg Episodes",
              f"{int(df_f['Episodes'].mean())}"
              if len(df_f) > 0 else "N/A")

st.markdown("<div style='margin:1rem 0'></div>",
            unsafe_allow_html=True)

# ── SUMMARY STATS ──
best_decade = df_f[
    df_f['Decade'].notna() &
    (df_f['Decade'] != 'Unknown')
]['Decade'].value_counts().index[0] \
if len(df_f) > 0 else "N/A"

top_show = df_f.nlargest(1,'Rating').iloc[0] \
if len(df_f) > 0 else None

top_voted = df_f.nlargest(1,'Votes').iloc[0] \
if len(df_f) > 0 else None

common_age = df_f['Age'].value_counts().index[0] \
if len(df_f) > 0 else "N/A"

st.markdown(f"""
<div style="display:grid;
     grid-template-columns:repeat(4,1fr);
     gap:0;background:#080808;
     border:1px solid #141414;
     border-radius:4px;
     margin-bottom:1.5rem;">
  <div style="padding:0.8rem 1.2rem;
       border-right:1px solid #141414;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.5rem;letter-spacing:0.16em;
         text-transform:uppercase;color:#2A2A2A;
         margin-bottom:0.3rem;">Highest Rated</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:0.95rem;letter-spacing:0.06em;
         color:#888;">
         {top_show['Title'] if top_show is not None 
          else 'N/A'} 
         ({top_show['Rating'] if top_show is not None 
           else ''})
    </div>
  </div>
  <div style="padding:0.8rem 1.2rem;
       border-right:1px solid #141414;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.5rem;letter-spacing:0.16em;
         text-transform:uppercase;color:#2A2A2A;
         margin-bottom:0.3rem;">Most Popular</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:0.95rem;letter-spacing:0.06em;
         color:#888;">
         {top_voted['Title'] if top_voted is not None 
          else 'N/A'}
         ({top_voted['Votes']/1e6:.1f}M)
    </div>
  </div>
  <div style="padding:0.8rem 1.2rem;
       border-right:1px solid #141414;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.5rem;letter-spacing:0.16em;
         text-transform:uppercase;color:#2A2A2A;
         margin-bottom:0.3rem;">Best Decade</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:0.95rem;letter-spacing:0.06em;
         color:#888;">{best_decade}</div>
  </div>
  <div style="padding:0.8rem 1.2rem;">
    <div style="font-family:'DM Mono',monospace;
         font-size:0.5rem;letter-spacing:0.16em;
         text-transform:uppercase;color:#2A2A2A;
         margin-bottom:0.3rem;">Common Age</div>
    <div style="font-family:'Bebas Neue',sans-serif;
         font-size:0.95rem;letter-spacing:0.06em;
         color:#888;">{common_age}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Trends",
    "Deep Dive", "AI Insights", "Search"
])

# TAB 1 — OVERVIEW
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_top_rated_chart(df_f), use_container_width=True)
    with c2:
        st.plotly_chart(create_rating_distribution(df_f), use_container_width=True)
    
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(create_type_comparison(df_f), use_container_width=True)
    with c4:
        st.plotly_chart(create_age_distribution(df_f), use_container_width=True)

# TAB 2 — TRENDS
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_shows_per_decade(df_f), use_container_width=True)
    with c2:
        st.plotly_chart(create_avg_rating_decade(df_f), use_container_width=True)
    
    st.plotly_chart(create_rating_tier(df_f), use_container_width=True)

# TAB 3 — DEEP DIVE
with tab3:
    st.plotly_chart(create_rating_vs_votes(df_f), use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_episodes_vs_rating(df_f), use_container_width=True)
    with c2:
        st.plotly_chart(create_top_voted_chart(df_f), use_container_width=True)
    
    st.markdown("**Top 20 Shows**")
    top20 = df_f.nlargest(20, 'Rating')[['Title','Rating','Votes','Episodes','Type','Decade','Age']]
    st.dataframe(top20, use_container_width=True)

# TAB 4 — AI INSIGHTS
with tab4:
    st.markdown("""
    <div style="font-family:'DM Mono',monospace;
         font-size:0.6rem;letter-spacing:0.14em;
         text-transform:uppercase;color:#333;
         margin-bottom:1rem;">
         AI Analysis Engine · OpenRouter API
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
            <div style="padding:0.8rem;
                 margin-bottom:0.5rem;
                 background:#0A0A0A;
                 border:1px solid #1A1A1A;
                 border-left:2px solid #FFF;
                 border-radius:4px;
                 font-family:'DM Sans',sans-serif;
                 font-size:0.82rem;
                 color:#888;
                 line-height:1.5;">
                <span style="font-family:'Bebas Neue',
                     sans-serif;font-size:1rem;
                     color:#333;margin-right:0.8rem;">
                     {str(i+1).zfill(2)}
                </span>
                {item}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Hidden Gems** — Rating ≥ 9.0, Votes < 200K")
    gems = df_f[
        (df_f['Rating'] >= 9.0) &
        (df_f['Votes'] < 200000)
    ][['Title','Rating','Votes','Type','Decade']]
    
    if len(gems) > 0:
        st.dataframe(gems, use_container_width=True)
    else:
        st.info("No hidden gems in current filter.")

# TAB 5 — SEARCH & RECOMMENDATIONS
with tab5:
    st.markdown("### Search Shows")
    query = st.text_input(
        "Search by title",
        placeholder="e.g. Breaking Bad, Game of Thrones"
    )
    if query and len(query) > 0:
        results = df_f[
            df_f['Title'].str.contains(
                query, case=False, na=False
            )
        ].sort_values('Rating', ascending=False)
        
        st.write(f"Found {len(results)} results")
        
        if len(results) == 0:
            st.warning("No shows found. Try different keywords.")
        else:
            st.dataframe(
                results[['Title','Rating','Votes',
                         'Episodes','Type','Decade']],
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown("### Similar Shows Recommender")
    
    cosine_sim, df_rec = build_recommendation_model(df)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_show = st.selectbox(
            "Select a show to get recommendations:",
            options=sorted(df['Title'].tolist())
        )
    with col2:
        num_recs = st.selectbox(
            "Number of recommendations:",
            options=[3, 5, 10],
            index=1
        )
    
    if selected_show:
        recommendations = get_recommendations(
            selected_show, df, cosine_sim, df_rec, n=num_recs
        )
        
        st.markdown(f"**Shows similar to:**")
        st.markdown(f"##### {selected_show}")
        
        if len(recommendations) > 0:
            st.dataframe(recommendations, use_container_width=True)
        else:
            st.info("No recommendations available.")

# IMDB Top 250 TV Shows — Cinematic Visualization Engine
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    try:
        return pd.read_csv('IMDB_cleaned.csv', encoding='latin-1')
    except FileNotFoundError:
        return pd.read_csv('data/IMDB_cleaned.csv', encoding='latin-1')

# ── CINEMATIC THEME ──
THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#777", size=10),
    title=dict(font=dict(family="Bebas Neue, sans-serif", size=18, color="#AAA"),
               x=0, xanchor="left", y=0.98),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.03)", linecolor="#1A1A1A",
        tickfont=dict(color="#555", size=9),
        showgrid=True, zeroline=False
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.03)", linecolor="#1A1A1A",
        tickfont=dict(color="#555", size=9),
        showgrid=True, zeroline=False
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#888", size=9)
    ),
    margin=dict(l=30, r=15, t=50, b=50),
    hoverlabel=dict(bgcolor="#111", font_size=12, font_color="#FFF",
                    bordercolor="#E50914"),
)

# Color palette
RED = "#E50914"
RED_DARK = "#8B0000"
WHITE = "#E0E0E0"
GRAY = "#666666"
DARK = "#333333"

# ── CHART 1: Top 10 by Rating ──
def create_top_rated_chart(df):
    top10 = df.nlargest(10, 'Rating').sort_values('Rating')
    fig = go.Figure(go.Bar(
        y=top10['Title'], x=top10['Rating'], orientation='h',
        marker=dict(
            color=top10['Rating'],
            colorscale=[[0, '#1a0000'], [0.5, '#8B0000'], [1, RED]],
            line=dict(width=0),
        ),
        text=top10['Rating'].apply(lambda x: f"  {x}"),
        textposition='outside', textfont=dict(color='#AAA', size=11),
        hovertemplate="<b>%{y}</b><br>Rating: %{x}<extra></extra>"
    ))
    fig.update_layout(**THEME, height=380, title_text="TOP 10 BY RATING")
    fig.update_xaxes(range=[8.0, 9.7])
    return fig

# ── CHART 2: Top 10 by Votes ──
def create_top_voted_chart(df):
    top10 = df.nlargest(10, 'Votes').sort_values('Votes')
    fig = go.Figure(go.Bar(
        y=top10['Title'], x=top10['Votes'], orientation='h',
        marker=dict(
            color=top10['Votes'],
            colorscale=[[0, '#111'], [0.5, '#555'], [1, WHITE]],
            line=dict(width=0),
        ),
        text=top10['Votes'].apply(lambda x: f"  {x/1e6:.1f}M"),
        textposition='outside', textfont=dict(color='#AAA', size=11),
        hovertemplate="<b>%{y}</b><br>Votes: %{x:,}<extra></extra>"
    ))
    fig.update_layout(**THEME, height=380, title_text="TOP 10 BY POPULARITY")
    return fig

# ── CHART 3: Rating Distribution ──
def create_rating_distribution(df):
    fig = px.histogram(df, x='Rating', nbins=20,
                       color_discrete_sequence=[RED])
    fig.update_traces(marker_line_color='#000', marker_line_width=1,
                      opacity=0.85,
                      hovertemplate="Rating: %{x}<br>Count: %{y}<extra></extra>")
    fig.update_layout(**THEME, height=320, bargap=0.08,
                      title_text="RATING DISTRIBUTION")
    return fig

# ── CHART 4: Shows per Decade ──
def create_shows_per_decade(df):
    decade_order = ['1970s', '1980s', '1990s', '2000s', '2010s', '2020s', 'Unknown']
    decade_counts = df['Decade'].value_counts().reindex(decade_order).fillna(0)
    colors = [RED if d != 'Unknown' else DARK for d in decade_counts.index]
    fig = go.Figure(go.Bar(
        x=decade_counts.index, y=decade_counts.values,
        marker=dict(color=colors, line=dict(width=0)),
        text=decade_counts.values.astype(int),
        textposition='outside', textfont=dict(color='#AAA', size=11),
        hovertemplate="Decade: %{x}<br>Shows: %{y}<extra></extra>"
    ))
    fig.update_layout(**THEME, height=320, title_text="SHOWS PER DECADE")
    return fig

# ── CHART 5: Rating vs Votes (Scatter) ──
def create_rating_vs_votes(df):
    fig = px.scatter(df, x='Votes', y='Rating', size='Episodes', color='Type',
                     hover_name='Title',
                     color_discrete_map={'TV Series': RED, 'TV Mini Series': WHITE})
    fig.update_traces(marker=dict(line=dict(width=0.5, color='#000'), opacity=0.8),
                      hovertemplate="<b>%{hovertext}</b><br>Rating: %{y}<br>Votes: %{x:,}<extra></extra>")
    fig.update_layout(**THEME, height=420, title_text="RATING VS POPULARITY")
    return fig

# ── CHART 6: Type Comparison (Donut) ──
def create_type_comparison(df):
    type_counts = df['Type'].value_counts()
    fig = go.Figure(data=[go.Pie(
        labels=type_counts.index, values=type_counts.values,
        hole=0.65,
        marker=dict(colors=[RED, DARK], line=dict(color='#000', width=2)),
        textposition='outside',
        textfont=dict(color='#AAA', size=11),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
    )])
    fig.update_layout(**THEME, height=320, showlegend=True,
                      title_text="SERIES TYPE SPLIT",
                      annotations=[dict(text=f"{len(df)}", x=0.5, y=0.5,
                                        font=dict(size=28, color=WHITE,
                                                  family="Bebas Neue"),
                                        showarrow=False)])
    return fig

# ── CHART 7: Age Rating Distribution ──
def create_age_distribution(df):
    age_counts = df['Age'].value_counts().sort_values(ascending=False)
    colors = [RED if i == 0 else f"rgba(229,9,20,{max(0.2, 1 - i*0.12):.2f})"
              for i in range(len(age_counts))]
    fig = go.Figure(go.Bar(
        x=age_counts.index, y=age_counts.values,
        marker=dict(color=colors, line=dict(width=0)),
        text=age_counts.values,
        textposition='outside', textfont=dict(color='#AAA', size=10),
        hovertemplate="Age Rating: %{x}<br>Shows: %{y}<extra></extra>"
    ))
    fig.update_layout(**THEME, height=320, title_text="AGE RATING BREAKDOWN")
    return fig

# ── CHART 8: Avg Rating by Decade (Line) ──
def create_avg_rating_decade(df):
    decade_order = ['1990s', '2000s', '2010s', '2020s']
    rating_by_decade = df.groupby('Decade')['Rating'].mean().reindex(decade_order)
    fig = go.Figure(go.Scatter(
        x=rating_by_decade.index, y=rating_by_decade.values,
        mode='lines+markers+text',
        line=dict(color=RED, width=3),
        marker=dict(size=10, color=RED, line=dict(color='#000', width=2)),
        text=[f"{v:.2f}" for v in rating_by_decade.values],
        textposition='top center', textfont=dict(color='#AAA', size=11),
        hovertemplate="Decade: %{x}<br>Avg Rating: %{y:.2f}<extra></extra>"
    ))
    fig.update_layout(**THEME, height=320, title_text="AVG RATING BY DECADE")
    fig.update_yaxes(range=[8.4, 9.2])
    return fig

# ── CHART 9: Rating Tier Breakdown ──
def create_rating_tier(df):
    tier_order = ['Elite', 'Excellent', 'Great', 'Good']
    tier_counts = df['Rating_Tier'].value_counts().reindex(tier_order).fillna(0)
    tier_colors = {'Elite': RED, 'Excellent': WHITE, 'Great': GRAY, 'Good': DARK}
    colors = [tier_colors.get(t, GRAY) for t in tier_order]
    fig = go.Figure(go.Bar(
        x=tier_counts.index, y=tier_counts.values,
        marker=dict(color=colors, line=dict(width=0)),
        text=tier_counts.values.astype(int),
        textposition='outside', textfont=dict(color='#AAA', size=11),
        hovertemplate="Tier: %{x}<br>Shows: %{y}<extra></extra>"
    ))
    fig.update_layout(**THEME, height=320, title_text="RATING TIER BREAKDOWN")
    return fig

# ── CHART 10: Episodes vs Rating (Scatter) ──
def create_episodes_vs_rating(df):
    fig = px.scatter(df, x='Episodes', y='Rating',
                     hover_name='Title', hover_data={'Start_Year': True},
                     color_discrete_sequence=[WHITE])
    fig.update_traces(marker=dict(size=7, opacity=0.7,
                                  line=dict(width=0.5, color=RED)),
                      hovertemplate="<b>%{hovertext}</b><br>Episodes: %{x}<br>Rating: %{y}<extra></extra>")
    fig.update_layout(**THEME, height=420, title_text="EPISODES VS RATING")
    return fig

# ── TEST ──
if __name__ == "__main__":
    print("Testing charts...")
    df = load_data()
    for fn in [create_top_rated_chart, create_top_voted_chart,
               create_rating_distribution, create_shows_per_decade,
               create_rating_vs_votes, create_type_comparison,
               create_age_distribution, create_avg_rating_decade,
               create_rating_tier, create_episodes_vs_rating]:
        fn(df)
    print("All 10 charts generated successfully!")
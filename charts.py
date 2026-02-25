# IMDB Top 250 TV Shows - Visualizations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    try:
        return pd.read_csv('IMDB_cleaned.csv', encoding='latin-1')
    except FileNotFoundError:
        return pd.read_csv('/home/sunny77/IMDB_cleaned.csv')

# Black & White Plotly Theme
BW_CHART = dict(
    paper_bgcolor="#111111",
    plot_bgcolor="#111111",
    font=dict(family="DM Mono, monospace", color="#555555", size=10),
    xaxis=dict(
        gridcolor="#1A1A1A", linecolor="#1A1A1A",
        tickfont=dict(color="#444444", size=9),
        showgrid=True, zeroline=False
    ),
    yaxis=dict(
        gridcolor="#1A1A1A", linecolor="#1A1A1A",
        tickfont=dict(color="#444444", size=9),
        showgrid=True, zeroline=False
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#555555", size=9)
    ),
    margin=dict(l=30, r=15, t=35, b=50),
    colorway=["#FFFFFF","#888888","#555555","#333333","#CCCCCC"]
)

# Chart 1 — Top 10 Shows by Rating (Horizontal Bar)
def create_top_rated_chart(df):
    top10_rating = df.nlargest(10, 'Rating').sort_values('Rating')
    fig = px.bar(top10_rating, y='Title', x='Rating', orientation='h',
                 title="Top 10 Shows by Rating", color='Rating',
                 color_continuous_scale=['#444444', '#FFFFFF'])
    fig.update_layout(**BW_CHART, height=350, coloraxis_showscale=False)
    fig.update_xaxes(range=[8.0, 9.6])
    return fig

# Chart 2 — Top 10 Shows by Votes (Horizontal Bar)
def create_top_voted_chart(df):
    top10_votes = df.nlargest(10, 'Votes').sort_values('Votes')
    fig = px.bar(top10_votes, y='Title', x='Votes', orientation='h',
                 title="Top 10 Shows by Votes", color='Votes',
                 color_continuous_scale=['#444444', '#FFFFFF'])
    fig.update_layout(**BW_CHART, height=350, coloraxis_showscale=False)
    fig.update_xaxes(tickformat=',')
    return fig

# Chart 3 — Rating Distribution (Histogram)
def create_rating_distribution(df):
    fig = px.histogram(df, x='Rating', nbins=20, title="Rating Distribution",
                       color_discrete_sequence=['#FFFFFF'])
    fig.update_layout(**BW_CHART, height=300, bargap=0.1)
    return fig

# Chart 4 — Shows per Decade (Bar chart)
def create_shows_per_decade(df):
    decade_order = ['1990s', '2000s', '2010s', '2020s', 'Unknown']
    decade_counts = df['Decade'].value_counts().reindex(decade_order).fillna(0)
    fig = px.bar(x=decade_counts.index, y=decade_counts.values, title="Shows per Decade",
                 labels={'x': 'Decade', 'y': 'Count'}, color_discrete_sequence=['#FFFFFF'])
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    fig.update_layout(**BW_CHART, height=300)
    return fig

# Chart 5 — Rating vs Votes (Scatter plot)
def create_rating_vs_votes(df):
    fig = px.scatter(df, x='Votes', y='Rating', size='Episodes', color='Type',
                     title="Rating vs Votes", hover_name='Title',
                     color_discrete_map={'TV Series': '#FFFFFF', 'TV Mini Series': '#888888'})
    fig.update_layout(**BW_CHART, height=400)
    return fig

# Chart 6 — Type Comparison (Donut chart)
def create_type_comparison(df):
    type_counts = df['Type'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=type_counts.index, values=type_counts.values,
                                  hole=0.6, marker=dict(colors=['#FFFFFF', '#555555']),
                                  textposition='outside')])
    fig.update_layout(**BW_CHART, height=300, showlegend=True, annotations=[])
    return fig

# Chart 7 — Age Rating Distribution (Bar)
def create_age_distribution(df):
    age_counts = df['Age'].value_counts().sort_values(ascending=False)
    fig = px.bar(x=age_counts.index, y=age_counts.values, title="Age Rating Distribution",
                 labels={'x': 'Age Rating', 'y': 'Count'}, color_discrete_sequence=['#FFFFFF'])
    fig.update_layout(**BW_CHART, height=300)
    return fig

# Chart 8 — Avg Rating by Decade (Line chart)
def create_avg_rating_decade(df):
    decade_order = ['1990s', '2000s', '2010s', '2020s']
    rating_by_decade = df.groupby('Decade')['Rating'].mean().reindex(decade_order)
    fig = px.line(x=rating_by_decade.index, y=rating_by_decade.values,
                  title="Avg Rating by Decade", markers=True,
                  labels={'x': 'Decade', 'y': 'Avg Rating'}, color_discrete_sequence=['#FFFFFF'])
    fig.update_traces(line_width=3, marker_size=8)
    fig.update_layout(**BW_CHART, height=300)
    fig.update_yaxes(range=[8.5, 9.1])
    return fig

# Chart 9 — Rating Tier Breakdown (Bar)
def create_rating_tier(df):
    tier_order = ['Elite', 'Excellent', 'Great', 'Good']
    tier_counts = df['Rating_Tier'].value_counts().reindex(tier_order).fillna(0)
    fig = px.bar(x=tier_counts.index, y=tier_counts.values, title="Rating Tier Breakdown",
                 labels={'x': 'Rating Tier', 'y': 'Count'}, color_discrete_sequence=['#FFFFFF'])
    fig.update_layout(**BW_CHART, height=300)
    return fig

# Chart 10 — Episodes vs Rating (Scatter)
def create_episodes_vs_rating(df):
    fig = px.scatter(df, x='Episodes', y='Rating', title="Episodes vs Rating",
                     hover_name='Title', hover_data={'Start_Year': True},
                     color_discrete_sequence=['#FFFFFF'])
    fig.update_layout(**BW_CHART, height=400)
    return fig

# Test function
if __name__ == "__main__":
    print("Testing charts...")
    df = load_data()
    create_top_rated_chart(df).show()
    create_top_voted_chart(df).show()
    create_rating_distribution(df).show()
    create_shows_per_decade(df).show()
    create_rating_vs_votes(df).show()
    create_type_comparison(df).show()
    create_age_distribution(df).show()
    create_avg_rating_decade(df).show()
    create_rating_tier(df).show()
    create_episodes_vs_rating(df).show()
    print("All 10 charts generated successfully!")
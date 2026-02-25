import pandas as pd
from openai import OpenAI

def generate_insights(df: pd.DataFrame, api_key: str = None) -> str:
    # Calculate summary stats
    avg_rating = df['Rating'].mean()
    top_show = df.loc[df['Rating'].idxmax(), 'Title']
    top_rating = df['Rating'].max()
    top_votes_show = df.loc[df['Votes'].idxmax(), 'Title']
    top_votes = df['Votes'].max()
    type_counts = df['Type'].value_counts()
    top_type = type_counts.idxmax()
    hidden_gems = len(df[(df['Rating'] >= 9.0) & (df['Votes'] < 200000)])
    decade_counts = df['Decade'].value_counts()
    top_decade = decade_counts.idxmax()
    avg_episodes = df['Episodes'].mean()
    age_counts = df['Age'].value_counts()
    top_age = age_counts.idxmax()
    
    stats = f"""
    - Total shows: {len(df)}
    - Average rating: {avg_rating:.2f}
    - Top rated: {top_show} ({top_rating})
    - Most voted: {top_votes_show} ({top_votes:,} votes)
    - Most common type: {top_type} ({type_counts[top_type]} shows)
    - Hidden gems (rating >=9.0, votes <200K): {hidden_gems}
    - Top decade: {top_decade} ({decade_counts[top_decade]} shows)
    - Most common age rating: {top_age}
    - Average episodes: {avg_episodes:.1f}
    """
    
    # If no API key, return fallback insights
    if not api_key:
        return f"""Fallback Insights:
• {top_show} leads with {top_rating} rating - the standout show in this dataset.
• {top_type} dominates with {type_counts[top_type]} shows, showing audience preference.
• The {top_decade} produced the most top shows ({decade_counts[top_decade]}), indicating TV's golden era.
• {hidden_gems} hidden gems await discovery - high quality with relatively low votes.
• Age rating {top_age} is most common, reflecting content targeting trends."""
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        prompt = f"""You are a TV industry analyst. Based on IMDB Top 250 TV Shows data:
{stats}
Give 5 sharp, specific insights about trends, patterns, and recommendations. 
Be data-specific. Each insight max 2 sentences."""
        
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}\n\n{stats}"

# Test
if __name__ == "__main__":
    df = pd.read_csv('IMDB_cleaned.csv')
    print("Generating AI insights...")
    insights = generate_insights(df)
    print("\n=== AI INSIGHTS ===")
    print(insights)

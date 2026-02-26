# IMDB Top 250 TV Shows - Data Cleaning
import pandas as pd
import numpy as np

# Load CSV with latin-1 encoding
df = pd.read_csv('IMDB_Top250_Tvshows.csv', encoding='latin-1')

# 1. Clean "Titile" column → rename to "Title"
df['Title'] = df['Titile'].str.replace(r'^\d+\.\s*', '', regex=True).str.strip()
df = df.drop(columns=['Titile']).rename(columns={'Title': 'Title'})

# 2. Clean "Year" column
# Extract start and end years
def clean_year(year_str):
    if pd.isna(year_str):
        return pd.Series({'Start_Year': np.nan, 'End_Year': np.nan})
    
    # Remove any non-digit characters
    year_str = ''.join(filter(str.isdigit, str(year_str)))
    
    if len(year_str) == 4:
        return pd.Series({'Start_Year': int(year_str), 'End_Year': int(year_str)})
    elif len(year_str) == 8:
        return pd.Series({'Start_Year': int(year_str[:4]), 'End_Year': int(year_str[4:])})
    else:
        return pd.Series({'Start_Year': np.nan, 'End_Year': np.nan})

df[['Start_Year', 'End_Year']] = df['Year'].apply(clean_year)
df['Duration'] = df['End_Year'] - df['Start_Year']
df['Decade'] = df['Start_Year'].apply(
    lambda y: f"{int(y // 10 * 10)}s" if pd.notna(y) else 'Unknown'
)

# 3. Clean "Total_episodes" → rename to "Episodes"
df['Episodes'] = df['Total_episodes'].str.replace(' eps', '').astype(int)
df = df.drop(columns=['Total_episodes'])

# 4. Clean "Age" column
df['Age'] = df['Age'].fillna('Unknown').astype('category')

# 5. Clean "Vote_count" → rename to "Votes"
def clean_votes(vote_str):
    if pd.isna(vote_str):
        return 0
    
    vote_str = vote_str.strip('()')
    if 'M' in vote_str:
        return float(vote_str.replace('M', '')) * 1_000_000
    elif 'K' in vote_str:
        return float(vote_str.replace('K', '')) * 1_000
    else:
        return float(vote_str)

df['Votes'] = df['Vote_count'].apply(clean_votes).astype(int)
df = df.drop(columns=['Vote_count'])

# 6. Rename "Category" → "Type"
df = df.rename(columns={'Category': 'Type'})

# 7. Create calculated columns
# Rating_Tier
def get_rating_tier(rating):
    if rating >= 9.3:
        return 'Elite'
    elif 9.0 <= rating <= 9.2:
        return 'Excellent'
    elif 8.7 <= rating <= 8.9:
        return 'Great'
    else:
        return 'Good'

df['Rating_Tier'] = df['Rating'].apply(get_rating_tier)

# Popularity_Score
df['Popularity_Score'] = (df['Votes'] / df['Votes'].max()) * 10

# Is_Miniseries
df['Is_Miniseries'] = df['Type'] == 'TV Mini Series'

# Print cleaned dataframe info and first 5 rows
print("Cleaned DataFrame Info:")
print(df.info())
print("\nFirst 5 Rows:")
print(df.head())

# Save cleaned data
output_path = 'IMDB_cleaned.csv'
df.to_csv(output_path, index=False)
print(f"\nCleaned data saved to: {output_path}")
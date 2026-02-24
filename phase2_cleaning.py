# Import necessary libraries
import pandas as pd
import numpy as np

# Phase 2: Data Cleaning and Preprocessing
print("=== Phase 2: Data Cleaning and Preprocessing ===\n")

# Load the dataset from CSV file
# This reads the file and creates a DataFrame (table-like structure)
# The dataset should be in the same directory as this script
print("1. Loading the dataset...")
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
print(f"   Initial shape: {df.shape[0]} rows, {df.shape[1]} columns\n")

# Verify the dataset loaded correctly
print("   First few rows:")
print(df.head(3))
print(f"\n   Columns: {list(df.columns)}")

# Remove useless columns that don't provide analytical value
# EmployeeCount: Always equals 1 for all employees - no variation
# Over18: Always "Yes" - constant value adds no information
# StandardHours: Always 80 - constant value
# EmployeeNumber: Just an ID - used only for identification, not analysis
print("\n2. Removing useless columns...")
columns_to_remove = ['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber']
df = df.drop(columns=columns_to_remove)
print(f"   Removed {len(columns_to_remove)} columns")
print(f"   New shape: {df.shape[0]} rows, {df.shape[1]} columns\n")

# Create AgeGroup column to categorize employees by age
# This groups ages into meaningful brackets for analysis
# pd.cut() function divides a continuous variable into discrete intervals
print("3. Creating AgeGroup column...")
df['AgeGroup'] = pd.cut(df['Age'], 
                        bins=[17, 30, 40, 50, 100],  # Define age ranges: 18-30, 31-40, 41-50, 51+
                        labels=['18-30', '31-40', '41-50', '50+'],  # Labels for each group
                        right=True)  # Include right boundary in each bin
print("   Age groups created: 18-30, 31-40, 41-50, 50+\n")

# Create SalarySlab column to categorize employees by monthly income
# This helps analyze attrition patterns across salary levels
print("4. Creating SalarySlab column...")
df['SalarySlab'] = pd.cut(df['MonthlyIncome'],
                         bins=[0, 5000, 10000, 15000, float('inf')],  # Define salary ranges
                         labels=['Low (<=5K)', 'Medium (5K-10K)', 'High (10K-15K)', 'Very High (>15K)'],
                         right=True)
print("   Salary slabs created: Low, Medium, High, Very High\n")

# Create TenureCategory based on years at company
# This categorizes employees by their tenure/seniority level
print("5. Creating TenureCategory column...")
df['TenureCategory'] = pd.cut(df['YearsAtCompany'],
                             bins=[-1, 2, 5, 10, float('inf')],  # Define tenure ranges
                             labels=['New (0-2)', 'Mid (3-5)', 'Senior (6-10)', 'Veteran (>10)'],
                             right=True)
print("   Tenure categories created: New, Mid, Senior, Veteran\n")

# Convert Attrition from Yes/No to 1/0 for numerical calculations
# This makes it easier to compute metrics like attrition rate
# .map() creates a dictionary mapping from old values to new values
print("6. Converting Attrition to numeric (1/0)...")
df['Attrition_Num'] = df['Attrition'].map({'Yes': 1, 'No': 0})
print("   'Yes' → 1, 'No' → 0\n")

# Display the cleaned dataframe information
print("7. Cleaned dataframe summary:")
print(f"   Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
print("   Final columns:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")

# Show sample of the cleaned dataframe
print("\n8. Sample of cleaned data (first 10 rows):")
print(df[['Age', 'AgeGroup', 'MonthlyIncome', 'SalarySlab', 'YearsAtCompany', 'TenureCategory', 'Attrition', 'Attrition_Num']].head(10))

# Save the cleaned dataframe to CSV for future use
print("\n9. Saving cleaned dataset...")
df.to_csv('hr_data_cleaned.csv', index=False)
print("   Saved as 'hr_data_cleaned.csv'")

# Show value counts for the new columns to verify they were created correctly
print("\n10. Verification of new columns:")
print("\nAgeGroup distribution:")
print(df['AgeGroup'].value_counts())
print("\nSalarySlab distribution:")
print(df['SalarySlab'].value_counts())
print("\nTenureCategory distribution:")
print(df['TenureCategory'].value_counts())
print("\nAttrition distribution:")
print(df['Attrition'].value_counts())
print("Attrition_Num distribution:")
print(df['Attrition_Num'].value_counts())

print("\n=== Phase 2 Complete! ===")
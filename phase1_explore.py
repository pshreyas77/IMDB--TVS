# Import necessary libraries
import pandas as pd
import numpy as np

# Load the dataset from CSV file
# This reads the file and creates a DataFrame (table-like structure)
# WA_Fn-UseC_-HR-Employee-Attrition.csv should be in the same folder
# If you downloaded it from Kaggle, place it in this directory
print("=== Loading the IBM HR Analytics Dataset ===")
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# Show basic information about the dataset
print("\n=== Dataset Shape ===")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

# Show all column names
print("\n=== Column Names ===")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# Show data types of each column
print("\n=== Data Types ===")
print(df.dtypes)

# Show first 5 rows of the dataset
print("\n=== First 5 Rows ===")
print(df.head())

# Check for missing values (null/NaN)
print("\n=== Missing Values ===")
print(df.isnull().sum())

# Show basic statistics for numerical columns
print("\n=== Basic Statistics ===")
print(df.describe())

# Show value counts for categorical columns (like Attrition)
print("\n=== Value Counts for Key Columns ===")
for col in ['Attrition', 'BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']:
    if col in df.columns:
        print(f"\n{col}:")
        print(df[col].value_counts())

# Show memory usage
print("\n=== Memory Usage ===")
print(df.memory_usage(deep=True))
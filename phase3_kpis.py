# Import necessary libraries
import pandas as pd
import numpy as np

# Phase 3: KPI Calculations and Metrics
print("=== Phase 3: KPI Calculations and Metrics ===\n")

# Load the cleaned dataset that was saved in Phase 2
# This reads the CSV file into a pandas DataFrame
df = pd.read_csv('hr_data_cleaned.csv')

# Verify the dataset loaded correctly
print("1. Dataset loaded successfully:")
print(f"   Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")

# KPI 1: Total Employees
# Count the total number of rows in the dataset, which equals total employees
total_employees = len(df)
print("KPI 1: Total Employees")
print(f"   {total_employees} employees\n")

# KPI 2: Total Attrition
# Sum the Attrition_Num column (1 = left, 0 = stayed) to count how many left
total_attrition = df['Attrition_Num'].sum()
print("KPI 2: Total Attrition")
print(f"   {total_attrition} employees left the company\n")

# KPI 3: Attrition Rate %
# Calculate percentage by dividing attrition by total employees and multiplying by 100
# Using round() to limit to 2 decimal places
attrition_rate = round((total_attrition / total_employees) * 100, 2)
print("KPI 3: Overall Attrition Rate")
print(f"   {attrition_rate}%\n")

# KPI 4: Active Employees
# Subtract attrition from total to get active employees
active_employees = total_employees - total_attrition
print("KPI 4: Active Employees")
print(f"   {active_employees} employees currently active\n")

# KPI 5: Average Age
# Mean() calculates the average value of the Age column
avg_age = round(df['Age'].mean(), 1)
print("KPI 5: Average Age")
print(f"   {avg_age} years\n")

# KPI 6: Average Monthly Income
# Mean() calculates average salary across all employees
avg_monthly_income = round(df['MonthlyIncome'].mean(), 2)
print("KPI 6: Average Monthly Income")
print(f"   ${avg_monthly_income:,.2f}\n")

# KPI 7: Average Years at Company
# Mean() calculates average tenure
avg_tenure = round(df['YearsAtCompany'].mean(), 2)
print("KPI 7: Average Years at Company")
print(f"   {avg_tenure} years\n")

# KPI 8: Attrition by Department
# Group by Department and calculate:
# - Count of employees in each department
# - Sum of Attrition_Num to get attrition count
# - Calculate percentage for each department
dept_stats = df.groupby('Department').agg({
    'Attrition_Num': ['count', 'sum']
}).round(2)
# Flatten the column names for easier access
dept_stats.columns = ['Total_Employees', 'Attrition_Count']
# Calculate attrition rate for each department
dept_stats['Attrition_Rate_%'] = round((dept_stats['Attrition_Count'] / dept_stats['Total_Employees']) * 100, 2)
print("KPI 8: Attrition by Department")
print(dept_stats)
print()

# KPI 9: Attrition by Age Group
# Group by AgeGroup and calculate attrition rate
age_group_stats = df.groupby('AgeGroup').agg({
    'Attrition_Num': ['count', 'sum']
}).round(2)
age_group_stats.columns = ['Total_Employees', 'Attrition_Count']
age_group_stats['Attrition_Rate_%'] = round((age_group_stats['Attrition_Count'] / age_group_stats['Total_Employees']) * 100, 2)
print("KPI 9: Attrition by Age Group")
print(age_group_stats)
print()

# KPI 10: Attrition by Gender
# Group by Gender and calculate attrition rate
gender_stats = df.groupby('Gender').agg({
    'Attrition_Num': ['count', 'sum']
}).round(2)
gender_stats.columns = ['Total_Employees', 'Attrition_Count']
gender_stats['Attrition_Rate_%'] = round((gender_stats['Attrition_Count'] / gender_stats['Total_Employees']) * 100, 2)
print("KPI 10: Attrition by Gender")
print(gender_stats)
print()

# KPI 11: Attrition by Salary Slab
# Group by SalarySlab and calculate attrition rate
salary_stats = df.groupby('SalarySlab').agg({
    'Attrition_Num': ['count', 'sum']
}).round(2)
salary_stats.columns = ['Total_Employees', 'Attrition_Count']
salary_stats['Attrition_Rate_%'] = round((salary_stats['Attrition_Count'] / salary_stats['Total_Employees']) * 100, 2)
print("KPI 11: Attrition by Salary Slab")
print(salary_stats)
print()

# KPI 12: Attrition by Job Role
# Group by JobRole and calculate attrition rate
jobrole_stats = df.groupby('JobRole').agg({
    'Attrition_Num': ['count', 'sum']
}).round(2)
jobrole_stats.columns = ['Total_Employees', 'Attrition_Count']
jobrole_stats['Attrition_Rate_%'] = round((jobrole_stats['Attrition_Count'] / jobrole_stats['Total_Employees']) * 100, 2)
print("KPI 12: Attrition by Job Role")
print(jobrole_stats)
print()

# KPI 13: Overtime Impact on Attrition
# Compare attrition rates between employees who work overtime vs those who don't
overtime_stats = df.groupby('OverTime').agg({
    'Attrition_Num': ['count', 'sum']
}).round(2)
overtime_stats.columns = ['Total_Employees', 'Attrition_Count']
overtime_stats['Attrition_Rate_%'] = round((overtime_stats['Attrition_Count'] / overtime_stats['Total_Employees']) * 100, 2)
print("KPI 13: Overtime Impact on Attrition")
print(overtime_stats)
print()

# Save KPIs to a summary file for later use
print("14. Saving KPI summary to file...")

# Create a summary dictionary with key metrics
summary_kpis = {
    'Total_Employees': total_employees,
    'Total_Attrition': total_attrition,
    'Attrition_Rate_%': attrition_rate,
    'Active_Employees': active_employees,
    'Average_Age': avg_age,
    'Average_Monthly_Income': avg_monthly_income,
    'Average_Years_at_Company': avg_tenure
}

# Convert dictionary to DataFrame for easy export
summary_df = pd.DataFrame([summary_kpis])

# Save to CSV
summary_df.to_csv('kpi_summary.csv', index=False)
print("   KPI summary saved as 'kpi_summary.csv'")

print("\n=== Phase 3 Complete! ===")
print("\nKey Insights from the Analysis:")
print(f"- Overall attrition rate: {attrition_rate}%")
print(f"- Average employee age: {avg_age} years")
print(f"- Average salary: ${avg_monthly_income:,.2f}")
print(f"- Average tenure: {avg_tenure} years")
print("- Check detailed breakdowns above for patterns!")
# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

# Initialize the Dash app
app = Dash(__name__)
app.title = "HR Analytics Dashboard"

# Load the cleaned dataset from Phase 2
df = pd.read_csv('hr_data_cleaned.csv')

# Load the KPI summary from Phase 3
kpi_df = pd.read_csv('kpi_summary.csv')

# Define layout for the dashboard
app.layout = html.Div([
    # Header with title
    html.Div([
        html.H1("HR Analytics Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'fontFamily': 'Arial'}),
        html.H3("Employee Attrition Analysis", 
                style={'textAlign': 'center', 'color': '#34495e', 'fontFamily': 'Arial'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px'}),
    
    # KPI Cards (Summary metrics)
    html.Div([
        html.Div([
            html.H3(f"{kpi_df['Total_Employees'].iloc[0]:,}", style={'color': '#27ae60', 'margin': '5px'}),
            html.P("Total Employees", style={'margin': '5px'})
        ], style={'display': 'inline-block', 'width': '24%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
                  'margin': '5px', 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3(f"{kpi_df['Total_Attrition'].iloc[0]:,}", style={'color': '#e74c3c', 'margin': '5px'}),
            html.P("Total Attrition", style={'margin': '5px'})
        ], style={'display': 'inline-block', 'width': '24%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
                  'margin': '5px', 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3(f"{kpi_df['Attrition_Rate_%'].iloc[0]}%", style={'color': '#e67e22', 'margin': '5px'}),
            html.P("Attrition Rate", style={'margin': '5px'})
        ], style={'display': 'inline-block', 'width': '24%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
                  'margin': '5px', 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3(f"${kpi_df['Average_Monthly_Income'].iloc[0]:,.0f}", style={'color': '#3498db', 'margin': '5px'}),
            html.P("Avg Monthly Income", style={'margin': '5px'})
        ], style={'display': 'inline-block', 'width': '24%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
                  'margin': '5px', 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
    ], style={'marginTop': '20px', 'marginBottom': '20px'}),
    
    # Department Filter
    html.Div([
        html.Label("Filter by Department:", style={'fontWeight': 'bold', 'fontFamily': 'Arial'}),
        dcc.Dropdown(
            id='dept-filter',
            options=[{'label': dept, 'value': dept} for dept in df['Department'].unique()] + 
                    [{'label': 'All', 'value': 'All'}],
            value='All',
            clearable=False,
            style={'width': '50%', 'marginTop': '10px'}
        )
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
              'marginBottom': '20px', 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
    
    # First row of charts
    html.Div([
        # Attrition by Department
        html.Div([
            html.H3("Attrition by Department", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Graph(id='dept-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'margin': '5px',
                  'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
        
        # Attrition by Age Group
        html.Div([
            html.H3("Attrition by Age Group", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Graph(id='age-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'margin': '5px',
                  'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'})
    ], style={'marginBottom': '20px'}),
    
    # Second row of charts
    html.Div([
        # Attrition by Gender
        html.Div([
            html.H3("Attrition by Gender", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Graph(id='gender-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'margin': '5px',
                  'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
        
        # Attrition by Salary Slab
        html.Div([
            html.H3("Attrition by Salary Slab", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Graph(id='salary-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'margin': '5px',
                  'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'})
    ], style={'marginBottom': '20px'}),
    
    # Third row of charts
    html.Div([
        # Attrition by Job Role
        html.Div([
            html.H3("Attrition by Job Role", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Graph(id='jobrole-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'margin': '5px',
                  'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'}),
        
        # Overtime Impact
        html.Div([
            html.H3("Overtime Impact on Attrition", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dcc.Graph(id='overtime-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'backgroundColor': 'white', 
                  'padding': '20px', 'borderRadius': '10px', 'margin': '5px',
                  'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'})
    ], style={'marginBottom': '20px'}),
    
    # Age vs Attrition Scatter Plot
    html.Div([
        html.H3("Age vs Attrition Distribution", style={'textAlign': 'center', 'color': '#2c3e50'}),
        dcc.Graph(id='age-scatter', 
                  figure=px.box(df, x='Attrition', y='Age', 
                                color='Attrition',
                                color_discrete_map={'Yes': '#e74c3c', 'No': '#27ae60'},
                                title="Age Distribution by Attrition Status"))
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
              'marginBottom': '20px', 'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)'})
])

# Callback to update charts based on department filter
@callback(
    [Output('dept-chart', 'figure'),
     Output('age-chart', 'figure'),
     Output('gender-chart', 'figure'),
     Output('salary-chart', 'figure'),
     Output('jobrole-chart', 'figure'),
     Output('overtime-chart', 'figure')],
    [Input('dept-filter', 'value')]
)
def update_charts(selected_dept):
    # Filter data based on selected department
    if selected_dept == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Department'] == selected_dept]
    
    # Calculate statistics for filtered data
    # Department chart
    dept_stats = filtered_df.groupby('Department').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    dept_stats.columns = ['Total_Employees', 'Attrition_Count']
    dept_stats['Attrition_Rate_%'] = round((dept_stats['Attrition_Count'] / dept_stats['Total_Employees']) * 100, 2)
    dept_stats = dept_stats.reset_index()
    
    dept_fig = px.bar(dept_stats, x='Department', y='Attrition_Rate_%',
                      title=f"Attrition Rate by Department ({'All' if selected_dept == 'All' else selected_dept})",
                      color='Attrition_Rate_%',
                      color_continuous_scale='Reds',
                      labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    
    # Age Group chart
    age_stats = filtered_df.groupby('AgeGroup').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    age_stats.columns = ['Total_Employees', 'Attrition_Count']
    age_stats['Attrition_Rate_%'] = round((age_stats['Attrition_Count'] / age_stats['Total_Employees']) * 100, 2)
    age_stats = age_stats.reset_index()
    
    age_fig = px.bar(age_stats, x='AgeGroup', y='Attrition_Rate_%',
                     title="Attrition Rate by Age Group",
                     color='Attrition_Rate_%',
                     color_continuous_scale='Oranges',
                     labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    
    # Gender chart
    gender_stats = filtered_df.groupby('Gender').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    gender_stats.columns = ['Total_Employees', 'Attrition_Count']
    gender_stats['Attrition_Rate_%'] = round((gender_stats['Attrition_Count'] / gender_stats['Total_Employees']) * 100, 2)
    gender_stats = gender_stats.reset_index()
    
    gender_fig = px.pie(gender_stats, values='Total_Employees', names='Gender',
                        title="Employee Distribution by Gender",
                        color_discrete_sequence=['#3498db', '#e74c3c'])
    
    # Salary Slab chart
    salary_stats = filtered_df.groupby('SalarySlab').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    salary_stats.columns = ['Total_Employees', 'Attrition_Count']
    salary_stats['Attrition_Rate_%'] = round((salary_stats['Attrition_Count'] / salary_stats['Total_Employees']) * 100, 2)
    salary_stats = salary_stats.reset_index()
    
    salary_fig = px.bar(salary_stats, x='SalarySlab', y='Attrition_Rate_%',
                        title="Attrition Rate by Salary Slab",
                        color='Attrition_Rate_%',
                        color_continuous_scale='Greens',
                        labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    
    # Job Role chart
    jobrole_stats = filtered_df.groupby('JobRole').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    jobrole_stats.columns = ['Total_Employees', 'Attrition_Count']
    jobrole_stats['Attrition_Rate_%'] = round((jobrole_stats['Attrition_Count'] / jobrole_stats['Total_Employees']) * 100, 2)
    jobrole_stats = jobrole_stats.reset_index()
    
    jobrole_fig = px.bar(jobrole_stats, x='JobRole', y='Attrition_Rate_%',
                         title="Attrition Rate by Job Role",
                         color='Attrition_Rate_%',
                         color_continuous_scale='Blues',
                         labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    jobrole_fig.update_layout(xaxis_tickangle=-45)
    
    # Overtime chart
    overtime_stats = filtered_df.groupby('OverTime').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    overtime_stats.columns = ['Total_Employees', 'Attrition_Count']
    overtime_stats['Attrition_Rate_%'] = round((overtime_stats['Attrition_Count'] / overtime_stats['Total_Employees']) * 100, 2)
    overtime_stats = overtime_stats.reset_index()
    
    overtime_fig = px.bar(overtime_stats, x='OverTime', y='Attrition_Rate_%',
                          title="Attrition Rate by Overtime Status",
                          color='Attrition_Rate_%',
                          color_discrete_map={'Yes': '#e74c3c', 'No': '#27ae60'},
                          labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    
    return dept_fig, age_fig, gender_fig, salary_fig, jobrole_fig, overtime_fig

# Run the app
if __name__ == '__main__':
    print("Starting HR Analytics Dashboard...")
    print("Dashboard will be available at http://127.0.0.1:8050")
    app.run_server(debug=True)
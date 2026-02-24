# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

# Initialize the Dash app
app = Dash(__name__)
app.title = "HR Analytics Dashboard - Attrition Analysis"

# Load the cleaned dataset from Phase 2
df = pd.read_csv('hr_data_cleaned.csv')

# Define the color scheme matching the requirements
COLORS = {
    'background': '#F8F9FA',
    'primary': '#2E5C8A',
    'attrition_highlight': '#E07A5F',
    'positive': '#81B29A',
    'text': '#2C3E50'
}

# Calculate KPIs for the cards
total_employees = len(df)
attrition_rate = round((df['Attrition_Num'].sum() / total_employees) * 100, 2)
active_employees = total_employees - df['Attrition_Num'].sum()
avg_tenure = round(df['YearsAtCompany'].mean(), 1)

# Define the app layout
app.layout = html.Div([
    # 1. Header Section
    html.Div([
        html.H1("HR Analytics Dashboard", 
                style={'textAlign': 'center', 
                       'color': COLORS['text'], 
                       'fontFamily': 'Arial, sans-serif',
                       'fontSize': '36px',
                       'marginBottom': '5px',
                       'fontWeight': 'bold'}),
        html.H3("Attrition Analysis", 
                style={'textAlign': 'center', 
                       'color': COLORS['primary'], 
                       'fontFamily': 'Arial, sans-serif',
                       'fontSize': '20px',
                       'marginTop': '0px',
                       'fontWeight': 'normal'})
    ], style={'backgroundColor': 'white', 
              'padding': '30px', 
              'borderRadius': '10px', 
              'margin': '20px',
              'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # 2. KPI Cards Row
    html.Div([
        # Total Employees Card
        html.Div([
            html.H2(f"{total_employees:,}", 
                    style={'color': COLORS['primary'], 
                           'fontSize': '36px',
                           'margin': '10px 0',
                           'fontWeight': 'bold'}),
            html.P("Total Employees", 
                   style={'color': COLORS['text'],
                          'fontSize': '16px',
                          'margin': '5px 0'})
        ], style={'display': 'inline-block', 
                  'width': '24%', 
                  'textAlign': 'center', 
                  'backgroundColor': 'white', 
                  'padding': '30px 20px', 
                  'borderRadius': '10px', 
                  'margin': '0 0.5%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                  'verticalAlign': 'top'}),
        
        # Attrition Rate Card
        html.Div([
            html.H2(f"{attrition_rate}%", 
                    style={'color': COLORS['attrition_highlight'], 
                           'fontSize': '36px',
                           'margin': '10px 0',
                           'fontWeight': 'bold'}),
            html.P("Attrition Rate (%)", 
                   style={'color': COLORS['text'],
                          'fontSize': '16px',
                          'margin': '5px 0'})
        ], style={'display': 'inline-block', 
                  'width': '24%', 
                  'textAlign': 'center', 
                  'backgroundColor': 'white', 
                  'padding': '30px 20px', 
                  'borderRadius': '10px', 
                  'margin': '0 0.5%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                  'verticalAlign': 'top'}),
        
        # Active Employees Card
        html.Div([
            html.H2(f"{active_employees:,}", 
                    style={'color': COLORS['positive'], 
                           'fontSize': '36px',
                           'margin': '10px 0',
                           'fontWeight': 'bold'}),
            html.P("Active Employees", 
                   style={'color': COLORS['text'],
                          'fontSize': '16px',
                          'margin': '5px 0'})
        ], style={'display': 'inline-block', 
                  'width': '24%', 
                  'textAlign': 'center', 
                  'backgroundColor': 'white', 
                  'padding': '30px 20px', 
                  'borderRadius': '10px', 
                  'margin': '0 0.5%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                  'verticalAlign': 'top'}),
        
        # Average Tenure Card
        html.Div([
            html.H2(f"{avg_tenure}", 
                    style={'color': COLORS['primary'], 
                           'fontSize': '36px',
                           'margin': '10px 0',
                           'fontWeight': 'bold'}),
            html.P("Average Tenure (Years)", 
                   style={'color': COLORS['text'],
                          'fontSize': '16px',
                          'margin': '5px 0'})
        ], style={'display': 'inline-block', 
                  'width': '24%', 
                  'textAlign': 'center', 
                  'backgroundColor': 'white', 
                  'padding': '30px 20px', 
                  'borderRadius': '10px', 
                  'margin': '0 0.5%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                  'verticalAlign': 'top'})
    ], style={'margin': '20px', 'textAlign': 'center'}),
    
    # 3. Filters Section
    html.Div([
        html.H3("Filters", style={'color': COLORS['text'], 'marginBottom': '15px'}),
        
        # Department Filter
        html.Div([
            html.Label("Department:", 
                       style={'fontWeight': 'bold', 
                              'fontFamily': 'Arial, sans-serif',
                              'marginRight': '10px'}),
            dcc.Dropdown(
                id='dept-filter',
                options=[{'label': 'All Departments', 'value': 'All'}] + 
                        [{'label': dept, 'value': dept} for dept in sorted(df['Department'].unique())],
                value='All',
                clearable=False,
                style={'width': '300px', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block', 'marginRight': '30px'}),
        
        # Gender Filter
        html.Div([
            html.Label("Gender:", 
                       style={'fontWeight': 'bold', 
                              'fontFamily': 'Arial, sans-serif',
                              'marginRight': '10px'}),
            dcc.Dropdown(
                id='gender-filter',
                options=[{'label': 'All Genders', 'value': 'All'}] + 
                        [{'label': gender, 'value': gender} for gender in sorted(df['Gender'].unique())],
                value='All',
                clearable=False,
                style={'width': '200px', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block', 'marginRight': '30px'}),
        
        # Age Group Filter
        html.Div([
            html.Label("Age Group:", 
                       style={'fontWeight': 'bold', 
                              'fontFamily': 'Arial, sans-serif',
                              'marginRight': '10px'}),
            dcc.Dropdown(
                id='age-filter',
                options=[{'label': 'All Age Groups', 'value': 'All'}] + 
                        [{'label': age_group, 'value': age_group} for age_group in sorted(df['AgeGroup'].unique())],
                value='All',
                clearable=False,
                style={'width': '200px', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block'})
    ], style={'backgroundColor': 'white', 
              'padding': '25px', 
              'borderRadius': '10px', 
              'margin': '20px',
              'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    
    # 4. Charts Section
    # First row - 2 charts
    html.Div([
        # Bar Chart: Attrition by Department
        html.Div([
            html.H3("Attrition Rate by Department", 
                    style={'textAlign': 'center', 
                           'color': COLORS['text'],
                           'fontFamily': 'Arial, sans-serif'}),
            dcc.Graph(id='dept-chart')
        ], style={'display': 'inline-block', 
                  'width': '48%', 
                  'backgroundColor': 'white', 
                  'padding': '25px', 
                  'borderRadius': '10px', 
                  'margin': '20px 1%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # Column Chart: Attrition by Age Group
        html.Div([
            html.H3("Attrition Rate by Age Group", 
                    style={'textAlign': 'center', 
                           'color': COLORS['text'],
                           'fontFamily': 'Arial, sans-serif'}),
            dcc.Graph(id='age-chart')
        ], style={'display': 'inline-block', 
                  'width': '48%', 
                  'backgroundColor': 'white', 
                  'padding': '25px', 
                  'borderRadius': '10px', 
                  'margin': '20px 1%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
    ], style={'textAlign': 'center'}),
    
    # Second row - 2 charts
    html.Div([
        # Donut Chart: Attrition by Gender
        html.Div([
            html.H3("Employee Distribution by Gender", 
                    style={'textAlign': 'center', 
                           'color': COLORS['text'],
                           'fontFamily': 'Arial, sans-serif'}),
            dcc.Graph(id='gender-chart')
        ], style={'display': 'inline-block', 
                  'width': '48%', 
                  'backgroundColor': 'white', 
                  'padding': '25px', 
                  'borderRadius': '10px', 
                  'margin': '20px 1%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # Bar Chart: Attrition by Salary Slab
        html.Div([
            html.H3("Attrition Rate by Salary Slab", 
                    style={'textAlign': 'center', 
                           'color': COLORS['text'],
                           'fontFamily': 'Arial, sans-serif'}),
            dcc.Graph(id='salary-chart')
        ], style={'display': 'inline-block', 
                  'width': '48%', 
                  'backgroundColor': 'white', 
                  'padding': '25px', 
                  'borderRadius': '10px', 
                  'margin': '20px 1%',
                  'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
    ], style={'textAlign': 'center'}),
    
    # Third row - Horizontal Bar Chart: Attrition by Job Role
    html.Div([
        html.H3("Attrition Rate by Job Role", 
                style={'textAlign': 'center', 
                       'color': COLORS['text'],
                       'fontFamily': 'Arial, sans-serif'}),
        dcc.Graph(id='jobrole-chart')
    ], style={'backgroundColor': 'white', 
              'padding': '25px', 
              'borderRadius': '10px', 
              'margin': '20px',
              'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
], style={'backgroundColor': COLORS['background'], 
          'padding': '20px', 
          'fontFamily': 'Arial, sans-serif',
          'minHeight': '100vh'})

# Callback to update all charts based on filter selections
@callback(
    [Output('dept-chart', 'figure'),
     Output('age-chart', 'figure'),
     Output('gender-chart', 'figure'),
     Output('salary-chart', 'figure'),
     Output('jobrole-chart', 'figure')],
    [Input('dept-filter', 'value'),
     Input('gender-filter', 'value'),
     Input('age-filter', 'value')]
)
def update_charts(dept_value, gender_value, age_value):
    """
    This function filters the data based on user selections and updates all charts.
    It's called automatically whenever any filter changes.
    """
    # Start with full dataset and filter based on selections
    filtered_df = df.copy()
    
    # Apply department filter if not "All"
    if dept_value != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == dept_value]
    
    # Apply gender filter if not "All"
    if gender_value != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == gender_value]
    
    # Apply age group filter if not "All"
    if age_value != 'All':
        filtered_df = filtered_df[filtered_df['AgeGroup'] == age_value]
    
    # If no data after filtering, return empty charts with message
    if filtered_df.empty:
        empty_fig = px.bar(title="No data available for selected filters")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
    
    # Create Department Chart (Bar Chart)
    dept_stats = filtered_df.groupby('Department').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    dept_stats.columns = ['Total_Employees', 'Attrition_Count']
    dept_stats['Attrition_Rate_%'] = round((dept_stats['Attrition_Count'] / dept_stats['Total_Employees']) * 100, 2)
    dept_stats = dept_stats.reset_index()
    
    dept_fig = px.bar(dept_stats, 
                      x='Department', 
                      y='Attrition_Rate_%',
                      title="Attrition Rate by Department",
                      color='Attrition_Rate_%',
                      color_continuous_scale=[[0, COLORS['positive']], 
                                               [0.5, COLORS['primary']], 
                                               [1, COLORS['attrition_highlight']]],
                      labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    dept_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family="Arial, sans-serif",
        title_font_size=16
    )
    
    # Create Age Group Chart (Column Chart)
    age_stats = filtered_df.groupby('AgeGroup').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    age_stats.columns = ['Total_Employees', 'Attrition_Count']
    age_stats['Attrition_Rate_%'] = round((age_stats['Attrition_Count'] / age_stats['Total_Employees']) * 100, 2)
    age_stats = age_stats.reset_index()
    
    age_fig = px.bar(age_stats, 
                     x='AgeGroup', 
                     y='Attrition_Rate_%',
                     title="Attrition Rate by Age Group",
                     color='Attrition_Rate_%',
                     color_continuous_scale=[[0, COLORS['positive']], 
                                              [0.5, COLORS['primary']], 
                                              [1, COLORS['attrition_highlight']]],
                     labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    age_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family="Arial, sans-serif",
        title_font_size=16
    )
    
    # Create Gender Chart (Donut Chart)
    gender_stats = filtered_df.groupby('Gender').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    gender_stats.columns = ['Total_Employees', 'Attrition_Count']
    gender_stats = gender_stats.reset_index()
    
    gender_fig = px.pie(gender_stats, 
                        values='Total_Employees', 
                        names='Gender',
                        title="Employee Distribution by Gender",
                        hole=0.4,
                        color_discrete_map={'Male': COLORS['primary'], 
                                           'Female': COLORS['attrition_highlight']})
    gender_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family="Arial, sans-serif",
        title_font_size=16
    )
    
    # Create Salary Slab Chart (Bar Chart)
    salary_stats = filtered_df.groupby('SalarySlab').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    salary_stats.columns = ['Total_Employees', 'Attrition_Count']
    salary_stats['Attrition_Rate_%'] = round((salary_stats['Attrition_Count'] / salary_stats['Total_Employees']) * 100, 2)
    salary_stats = salary_stats.reset_index()
    
    salary_fig = px.bar(salary_stats, 
                        x='SalarySlab', 
                        y='Attrition_Rate_%',
                        title="Attrition Rate by Salary Slab",
                        color='Attrition_Rate_%',
                        color_continuous_scale=[[0, COLORS['positive']], 
                                                 [0.5, COLORS['primary']], 
                                                 [1, COLORS['attrition_highlight']]],
                        labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    salary_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family="Arial, sans-serif",
        title_font_size=16
    )
    
    # Create Job Role Chart (Horizontal Bar Chart)
    jobrole_stats = filtered_df.groupby('JobRole').agg({
        'Attrition_Num': ['count', 'sum']
    }).round(2)
    jobrole_stats.columns = ['Total_Employees', 'Attrition_Count']
    jobrole_stats['Attrition_Rate_%'] = round((jobrole_stats['Attrition_Count'] / jobrole_stats['Total_Employees']) * 100, 2)
    jobrole_stats = jobrole_stats.reset_index()
    
    jobrole_fig = px.bar(jobrole_stats, 
                         y='JobRole', 
                         x='Attrition_Rate_%',
                         title="Attrition Rate by Job Role",
                         color='Attrition_Rate_%',
                         orientation='h',
                         color_continuous_scale=[[0, COLORS['positive']], 
                                                  [0.5, COLORS['primary']], 
                                                  [1, COLORS['attrition_highlight']]],
                         labels={'Attrition_Rate_%': 'Attrition Rate (%)'})
    jobrole_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family="Arial, sans-serif",
        title_font_size=16,
        height=max(400, len(jobrole_stats) * 30)  # Dynamic height based on number of roles
    )
    
    return dept_fig, age_fig, gender_fig, salary_fig, jobrole_fig

# Run the app
if __name__ == '__main__':
    print("=" * 60)
    print("Starting HR Analytics Dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, port=8050)
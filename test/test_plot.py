import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('toeslagen_c.csv')

# Extract the 'inkomen' column for the x-axis
x = df['inkomen']

# Create the figure
fig = go.Figure()

# Add traces for each toeslag
fig.add_trace(go.Scatter(
    x=x,
    y=df['huurtoeslag'],
    mode='lines+markers',
    name='Huurtoeslag',
    hovertemplate='€%{y}'
))

fig.add_trace(go.Scatter(
    x=x,
    y=df['zorgtoeslag'],
    mode='lines+markers',
    name='Zorgtoeslag',
    hovertemplate='€%{y}'
))

fig.add_trace(go.Scatter(
    x=x,
    y=df['kinderopvangtoeslag'],
    mode='lines+markers',
    name='Kinderopvangtoeslag',
    hovertemplate='€%{y}'
))

fig.add_trace(go.Scatter(
    x=x,
    y=df['kindergevonden_budget'],
    mode='lines+markers',
    name='Kindergevonden Budget',
    hovertemplate='€%{y}',
))

# Customize the layout
fig.update_layout(
    title='Toeslagen vs Inkomen',
    xaxis_title='Inkomen (€)',
    yaxis_title='Toeslag (€)',
    hovermode='x unified',
)

# Display the figure
fig.show()

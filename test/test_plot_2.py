import pandas as pd
import plotly.express as px

# Load CSV file
csv_file = "toeslagen2.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Function to format the variable names by removing underscores and capitalizing
def format_name(name):
    return name.replace("_", " ").capitalize()

# Create a plot
fig = px.line(df,
              x='inkomen',
              y=['huurtoeslag', 'zorgtoeslag', 'kinderopvangtoeslag', 'kindergevonden_budget'],
              labels={"value": "Toeslagen Amount", "inkomen": "Inkomen"},
              title="Toeslagen vs Inkomen")

# Update hover template to format variable names and hide the variable name outside of the popup
for trace in fig.data:
    trace.name = format_name(trace.name)  # Format the name inside the hover popup
    trace.hovertemplate = '<b>%{fullData.name}</b><br>Inkomen: %{x}<br>Amount: %{y}'
    trace.hoverinfo = 'skip'  # This hides the variable name outside the popup

# Update layout
fig.update_layout(
    xaxis_title="Inkomen",
    yaxis_title="Amount",
    showlegend=False  # Keep the legend hidden as before
)

# Export to HTML
fig.write_html("toeslagen_plot.html")

print("Plot successfully exported to toeslagen_plot.html")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Load the data
futures_data = pd.read_excel('NCAAFutures.xlsx')
color_data = pd.read_excel('color_teams.xlsx')

# Merge the futures data with the team colors
merged_data = pd.merge(futures_data, color_data, on='TEAM')

# Function to get team logo file path
def get_team_logo_path(team_name):
    logo_path = os.path.join('NCAAF Logos', f'{team_name}.png')
    if os.path.exists(logo_path):
        return logo_path
    else:
        st.warning(f"Logo not found for team: {team_name}")
    return None

# Set up the Streamlit page
st.title('Interactive NCAA Futures Odds Over Time')

# Initialize plotly figure
fig = go.Figure()

# Get unique teams
teams = merged_data['TEAM'].unique()

# Add a line for each team
for team in teams:
    team_data = merged_data[merged_data['TEAM'] == team]
    color = team_data['Color'].iloc[0]

    # Add the line for the team
    fig.add_trace(go.Scatter(
        x=team_data['Week'],
        y=team_data['Odds'],
        mode='lines+markers',
        name=team,
        line=dict(color=color),
        hoverinfo='text',
        text=[f'Team: {team}<br>Odds: {odds}<br>Week: {week}'
              for odds, week in zip(team_data['Odds'], team_data['Week'])]
    ))

    # Add logos as custom data points
    for _, row in team_data.iterrows():
        week = row['Week']
        odds = row['Odds']
        logo_path = get_team_logo_path(team)
        print(logo_path)

        if logo_path:
            fig.add_layout_image(
                dict(
                    source=logo_path,  # Use the file path directly
                    x=week,  # x position
                    y=odds,  # y position
                    xref="x",  # reference to x axis
                    yref="y",  # reference to y axis
                    sizex=0.3,  # Small size for better alignment
                    sizey=0.3,
                    xanchor="center",
                    yanchor="middle",
                    opacity=1,
                    layer="above"
                )
            )
fig.add_layout_image(
    dict(
        source="NCAAF Logos\Alabama.png",  # Use the file path directly
        x=1,  # x position
        y=0,  # y position 
        xanchor="center",
        yanchor="middle",
        opacity=1,
        sizing="stretch",
        layer="above"
    )
)        

# Customize layout for interactivity
fig.update_layout(
    title='NCAA Futures Odds by Team',
    xaxis_title='Week',
    yaxis_title='Odds',
    hovermode='closest',
    showlegend=False  # Removes legend
)

# Display the interactive plot
st.plotly_chart(fig)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from datetime import datetime
# Load the Excel file
file_path = 'NCAAFutures.xlsx'# Replace with your actual file path
df = pd.read_excel(file_path)

#Load colors file
file_path_teams = 'color_teams.xlsx'# Replace with your actual file path
df_teams = pd.read_excel(file_path_teams)

#Join to colors
df = pd.merge(df, df_teams, on='TEAM', how='left')

# Clean the Color column (optional)
df['Color'] = df['Color'].str.strip().str.upper()

# Group the data by team
teams = df['TEAM'].unique()

#Add Ranks to offset logos when same odds for multiple teams later on
df['rank'] = df.groupby('Odds')['TEAM'].rank(method='dense')

df['rank_value'] = df['rank']-1

# Create the plot
plt.figure(figsize=(5,20))
 
# Define the path to the logos folder
logo_folder = 'NCAAF Logos'# Replace with your actual logos folder path# Plot each team's odds over the weeks and add logos
offset_increment = .02# Adjust as needed# Track the last position used to detect overlaps
last_positions = {}

for team in teams:
    team_data = df[df['TEAM'] == team]
    team_color = df[df['TEAM'] == team]['Color'].values[0]
    plt.plot(team_data['Week'], team_data['Odds'], label=team, color=team_color)
    

    # Get the corresponding logo from the TEAM NAME AND ASSUME THE NAME OF THE .PNG FILE IS THE NAME OF THE TEAM
    team_logo = team_data['TEAM'].iloc[0]  # Assuming the logo name is consistent for each team
    logo_path = os.path.join(logo_folder, f'{team_logo}.png')    

    if os.path.exists(logo_path):
        for (x, y, rank) in zip(team_data['Week'], team_data['Odds'], team_data['rank_value']):
            if rank > 0:
                #if rank % 2 == 0:
                #    x = x + ((rank-1) * (offset_increment * -1))
                #else:
                x = x + (rank * (offset_increment))
            img = mpimg.imread(logo_path)
            imagebox = OffsetImage(img, zoom=0.1)  # Adjust zoom to control the size of logos
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            plt.gca().add_artist(ab)
    else:
        print(logo_path)

# Add labels and title
plt.xlabel('Week')
plt.ylabel('Odds')
plt.title('NCAA Futures 2024: Week 2')
#plt.legend(title='Teams', bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.ylim(0,8100)

# Set x-axis to show only the numbers we have
plt.xticks([1])

# Save the plot with date and time in the filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
plt.tight_layout()
plt.savefig(f'NCAA_Futures_Odds{timestamp}.png', dpi=300)

# Show the plot
plt.tight_layout()
plt.show()
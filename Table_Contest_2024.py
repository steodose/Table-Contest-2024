import pandas as pd
import numpy as np
from great_tables import GT, md, html
from importlib_resources import files

# load data
dg_performance = pd.read_csv('/Users/Stephan/Desktop/Python/Table-Contest/dg_performance_2024.csv')
#print(dg_performance)

# setting up img file paths for flag icons
flags_path = '/Users/Stephan/Desktop/Python/Table-Contest/flags/'


#### Data preparation ####
selected_columns = [
    'country','player_name', 'tour', 'wins', 'x_wins', 'putt_true', 'arg_true', 
    'app_true', 'ott_true', 't2g_true', 'total_true'
]


dg_clean = dg_performance[selected_columns].replace(-9999, 0) # replace LIV values with 0 values for formatting purposes
#dg_clean.rename(columns=column_renames, inplace=True) # rename columns in place
dg_clean['player_name'] = dg_clean['player_name'].apply(lambda name: ' '.join(name.split(', ')[::-1])) # fix player naming conventions
dg_top20 = dg_clean.head(20) # cut off at Top 20
dg_top20.insert(0, 'rank', range(1, 21)) # adding a new column 'rank' which is a simple index + 1 (since index starts at 0)

# Displaying the top 20 in the terminal
print(dg_top20)

# make dataframe with player headshots
player_names = ["Jon Rahm", "Collin Morikawa", "Tom Hoge", "Max Homa", "Tom Kim", "J.J. Spaun", "Tony Finau", "K.H. Lee", "Scottie Scheffler", "Matt Fitzpatrick", "Will Zalatoris", "Luke List"]
image_urls = ['https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_350,q_auto,w_280/headshots_46970.png', 
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_350,q_auto,w_280/headshots_50525.png', 
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_350,q_auto,w_280/headshots_35532.png', 
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_350,q_auto,w_280/headshots_39977.png', 
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_55182.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_39324.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_29725.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_32791.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_46046.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_40098.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_47483.png',
                         'https://pga-tour-res.cloudinary.com/image/upload/c_fill,d_headshots_default.png,f_auto,g_face:center,h_268,q_auto,w_201/headshots_27129.png']


# Create a DataFrame with the player names and image URLs
headshots = pd.DataFrame({
    'player': player_names,
    'player_url': image_urls
})

#print(headshots)


#### ---------- Make GT table ------------- ####
table = GT(dg_top20)
table = table.tab_header(
    title=md("**Kings of Strokes-Gained**"),
    subtitle="Evaluating 2024 performance among top professional golfers using Data Golf's true strokes-gained and expected wins (xWins)."
    )
table = table.tab_source_note(
    source_note="Total Strokes-Gained (SG) is a measure of a player's performance relative to the field average."
    )
table = table.tab_source_note(
    source_note=md("**Source:** Data Golf | **Table:** Stephan Teodosescu (@steodosescu)")
    )
table = table.fmt_image(
    columns='country', 
    path=flags_path, 
    file_pattern='{}.png'  # {} will be replaced by the country code
)
table = table.cols_label(
        rank = "Rank",
        country = "Country",
        player_name = "Player",
        tour= "Tour",
        wins = 'Wins', 
        x_wins = 'xWins', 
        putt_true = 'Putt SG', 
        arg_true = 'ATG SG',
        app_true = 'App SG', 
        ott_true = 'OTT SG', 
    t2g_true = 'TTG SG', 
    total_true = 'Total SG'
    )
table = table.fmt_number(
    columns=['putt_true', 'arg_true', 'app_true', 'ott_true', 't2g_true', 'total_true'],
    decimals=2
    )
table = table.fmt_number(
    columns=["x_wins"],
    decimals=1
    )
table = table.fmt_number(
    columns=["wins"],
    decimals=0
    )
table = table.data_color(
        columns="x_wins",
        palette=["white", "blue"],
        domain=[0,8]
    )
table = table.data_color(
        columns=['putt_true', 'arg_true', 'app_true', 'ott_true', 't2g_true', 'total_true'],
        palette=["white", "orange"],
        domain=[-2,4]
    )


# Save the table as a PNG
table.save("/Users/Stephan/Desktop/Python/Table-Contest/sg_table.png", window_size=(800, 1200), scale=1, expand = 1)


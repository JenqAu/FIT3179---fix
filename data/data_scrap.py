from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd

# Function to get league-wide totals for a season
def get_3pt_stats(season):
    """
    season: e.g. '2018-19'
    """
    stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        season_type_all_star='Regular Season',
        measure_type_detailed_defense='Base'
    ).get_data_frames()[0]

    # Aggregate across all teams
    total_3pa = stats['FG3A'].sum()
    avg_3p_pct = (stats['FG3M'].sum() / stats['FG3A'].sum())  # league average
    return {'Season': season, 'Year': int(season[:4]), 'Total_3PA': total_3pa, 'Avg_3P%': avg_3p_pct}

# Seasons you’re missing
seasons = ['2017-18', '2018-19', '2019-20', '2020-21']

# Collect data
data = [get_3pt_stats(season) for season in seasons]
df_new = pd.DataFrame(data)

# Load your existing CSV (1980–2017)
df_old = pd.read_csv('data/nba_3pt_by_decade.csv')

# Combine and save
df_combined = pd.concat([df_old, df_new], ignore_index=True).sort_values('Year')
df_combined.to_csv('data/nba_3pt_extended.csv', index=False)

print("✅ Updated file saved as data/nba_3pt_extended.csv")
print(df_combined.tail())

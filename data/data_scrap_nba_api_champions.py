from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.static import teams
import pandas as pd
import time

print("Fetching NBA team year-by-year stats...")

all_teams = teams.get_teams()
records = []

for team in all_teams:
    tid = team["id"]
    tname = team["full_name"]

    try:
        df = teamyearbyyearstats.TeamYearByYearStats(team_id=tid).get_data_frames()[0]

        # Some historical teams have missing columns
        for col in ["PLAYOFF_SEED", "CHAMPION"]:
            if col not in df.columns:
                df[col] = 0  # assume default (no playoffs / not champion)

        df = df[["TEAM_ID", "TEAM_CITY", "TEAM_NAME", "YEAR", "WINS", "LOSSES", "PLAYOFF_SEED", "CHAMPION"]]
        df["FullName"] = tname
        records.append(df)

        print(f"✅ {tname} ({len(df)} seasons)")
        time.sleep(0.6)

    except Exception as e:
        print(f"⚠️ Skipped {tname}: {e}")

# Combine all data
full = pd.concat(records, ignore_index=True)

# Keep only champion seasons
champions = full[full["CHAMPION"] == 1]

# Count championships per team
team_titles = (
    champions.groupby("FullName")
    .size()
    .reset_index(name="Championships")
    .sort_values("Championships", ascending=False)
)

# Roughly assign dynasty era
def assign_peak_era(team):
    if "Celtic" in team: return "1960s"
    if "Laker" in team: return "1980s"
    if "Warrior" in team: return "2010s"
    if "Bull" in team: return "1990s"
    if "Spur" in team: return "2000s"
    if "Heat" in team: return "2010s"
    if "Piston" in team: return "1990s"
    if "76er" in team or "Sixers" in team: return "1980s"
    if "Knicks" in team: return "1970s"
    if "Bucks" in team: return "1970s"
    return "Modern"

team_titles["PeakEra"] = team_titles["FullName"].apply(assign_peak_era)

# Add abbreviation
team_lookup = {t["full_name"]: t["abbreviation"] for t in all_teams}
team_titles["Abbrev"] = team_titles["FullName"].map(team_lookup)

# Save output
output_path = "nba_team_championships.csv"
team_titles.to_csv(output_path, index=False)

print(f"\n✅ Saved: {output_path}")
print(team_titles.head(10))

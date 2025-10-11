import pandas as pd

# === 1. Load the dataset ===
input_file = "data/all_seasons.csv"     # raw Kaggle file
df = pd.read_csv(input_file)

print("✅ Loaded:", df.shape, "rows and columns")

# === 2. Keep relevant columns only ===
keep_cols = [
    "player_name",
    "team_abbreviation",
    "player_height",
    "player_weight"
    # Note: player_position not available in this dataset
]
df = df[keep_cols].rename(columns={
    "player_name": "player",
    "team_abbreviation": "team",
    "player_height": "height",
    "player_weight": "weight"
})

# === 3. Clean missing values ===
df = df.dropna(subset=["height", "weight"])

# === 4. Remove invalid or zero values ===
df = df[(df["height"] > 0) & (df["weight"] > 0)]

# === 5. Remove duplicate players (keep latest record) ===
# Some players appear multiple times across seasons — keep only the last season's entry
df = df.drop_duplicates(subset=["player"], keep="last")

# === 6. Reset index and sort alphabetically ===
df = df.sort_values("player").reset_index(drop=True)

# === 7. Save cleaned dataset ===
output_file = "nba_players_cleaned.csv"
df.to_csv(output_file, index=False)

print("✅ Cleaned dataset saved to:", output_file)
print("Rows:", len(df))
print("Columns:", list(df.columns))
print(df.head())
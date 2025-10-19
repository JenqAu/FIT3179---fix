import pandas as pd

df = pd.read_csv("C:\\Users\\User\\OneDrive\\Documents\\Monash\\Year 3\\Sem 1\\FIT3179\\FIT3179\\data\\shots_log.csv")

clean = df[[
    "PLAYER_NAME", "LOC_X", "LOC_Y", "SHOT_MADE_FLAG", "SHOT_TYPE", "SHOT_DISTANCE", "TEAM_NAME", "SEASON"
]]

clean = clean.dropna(subset=["LOC_X", "LOC_Y", "SHOT_MADE_FLAG"])
clean["SHOT_MADE_FLAG"] = clean["SHOT_MADE_FLAG"].astype(int)

# Optional: filter 1–2 players for testing
# clean = clean[clean["PLAYER_NAME"].isin(["Michael Jordan", "Scottie Pippen"])]

clean.to_csv("data/shot_data.csv", index=False)
print("✅ Saved cleaned dataset → data/shot_data.csv")

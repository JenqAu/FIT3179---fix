import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEASONS_PATH = ROOT / "Seasons_Stats.csv"
OUTPUT_PATH = ROOT / "top20_player_radar.csv"

METRICS = ["2P", "3P", "AST", "TRB", "STL", "BLK"]


def load_season_stats() -> pd.DataFrame:
    df = pd.read_csv(SEASONS_PATH)
    df = df.rename(columns={"Player": "player"})
    df["player"] = df["player"].astype(str).str.strip()
    df["Year"] = pd.to_numeric(df.get("Year"), errors="coerce")
    df = df[df["player"].notna() & (df["player"] != "")]

    numeric_columns = ["G", "PTS", *METRICS]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df.get(column), errors="coerce").fillna(0)

    # Prefer aggregated TOT rows when available for a player-season.
    has_tot = df.groupby(["player", "Year"])["Tm"].transform(lambda teams: "TOT" in set(teams.dropna()))
    df = df[~((df["Tm"] != "TOT") & has_tot)]
    return df


def build_career_totals(df: pd.DataFrame) -> pd.DataFrame:
    aggregated = (
        df.groupby("player", as_index=False)[["G", "PTS", *METRICS]]
        .sum(min_count=1)
    )
    aggregated = aggregated[aggregated["G"] > 0]
    return aggregated


def select_top_players(aggregated: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    top_players = aggregated.sort_values("PTS", ascending=False).head(top_n)
    metric_per_game = top_players.copy()
    for metric in METRICS:
        metric_per_game[metric] = metric_per_game[metric] / metric_per_game["G"]
    metric_per_game = metric_per_game.drop(columns=["PTS", "G"])
    return metric_per_game


def min_max_scale(values: pd.Series) -> pd.Series:
    minimum = values.min()
    maximum = values.max()
    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series(0.5, index=values.index)
    return (values - minimum) / (maximum - minimum)


def build_long_form(metric_per_game: pd.DataFrame) -> pd.DataFrame:
    records = []
    for metric in METRICS:
        normalized = min_max_scale(metric_per_game[metric])
        for player, raw_value, scaled_value in zip(
            metric_per_game["player"], metric_per_game[metric], normalized
        ):
            records.append(
                {
                    "Player": player,
                    "Metric": metric,
                    "Value": float(scaled_value),
                    "PerGame": float(raw_value),
                }
            )
    return pd.DataFrame.from_records(records)


if __name__ == "__main__":
    season_stats = load_season_stats()
    career_totals = build_career_totals(season_stats)
    per_game_metrics = select_top_players(career_totals)
    long_form = build_long_form(per_game_metrics)
    long_form.to_csv(OUTPUT_PATH, index=False)

    player_list = per_game_metrics["player"].tolist()
    print(f"Wrote {len(long_form)} rows to {OUTPUT_PATH}")
    print("Top 20 players (career points):")
    for name in player_list:
        print(f" - {name}")
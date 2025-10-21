#!/usr/bin/env python3
"""Fetch LeBron James shot chart data for a selected NBA season.

This script uses the nba_api ShotChartDetail endpoint to pull all field goal
attempts for LeBron James in a specific season and writes the results to a CSV
mirroring the columns used by the existing shot chart visuals in this project.

The output CSV can be plugged directly into a Vega-Lite shot scatter spec like
`js/shot_scatter_joint.vg.json` by updating the data URL to point at the new
file.
"""

from __future__ import annotations

import pathlib

import pandas as pd
from nba_api.stats.endpoints import ShotChartDetail

# --- Configuration --------------------------------------------------------
PLAYER_ID = 2544  # LeBron James
SEASON = "2012-13"  # Regular season format expected by nba_api
SEASON_TYPE = "Regular Season"
OUTPUT_CSV = pathlib.Path(__file__).with_name("shot_data_lebron_2012_13.csv")

# Miami Heat team ID for the 2012-13 season. Setting this to 0 would include
# whichever team the player was on, but keeping it explicit makes the query
# reproducible if the player is traded mid-season.
TEAM_ID = 1610612748  # Miami Heat


def fetch_shot_data() -> pd.DataFrame:
    """Return a DataFrame with shot chart data for the configured season."""

    shotchart = ShotChartDetail(
        team_id=TEAM_ID,
        player_id=PLAYER_ID,
        season_nullable=SEASON,
        season_type_all_star=SEASON_TYPE,
        context_measure_simple="FGA",
    )

    data = shotchart.get_data_frames()[0]

    data = data.copy()
    data["SEASON"] = f"{SEASON} Season"

    keep_cols = [
        "PLAYER_NAME",
        "LOC_X",
        "LOC_Y",
        "SHOT_MADE_FLAG",
        "SHOT_TYPE",
        "SHOT_DISTANCE",
        "TEAM_NAME",
        "SEASON",
    ]

    return data.loc[:, keep_cols]


def main() -> None:
    df = fetch_shot_data()
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Saved {len(df):,} shots to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

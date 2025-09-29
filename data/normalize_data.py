import pandas as pd

# Load NBA players data
nba_df = pd.read_csv('nba_players_per_state.csv')

# Fix common typos in the data
nba_df['State'] = nba_df['State'].replace({
    'DC': 'District of Columbia',
    'Washingon': 'Washington'  # Fix the typo
})

# Load population data
pop_df = pd.read_csv('NST-EST2024-ALLDATA.csv')

# Filter to states and DC (SUMLEV == 40) and get population data with STATE codes for FIPS
states_pop = pop_df[pop_df['SUMLEV'] == 40][['STATE', 'NAME', 'POPESTIMATE2024']].copy()

# Rename columns
states_pop = states_pop.rename(columns={'NAME': 'State', 'POPESTIMATE2024': 'Population'})

# Create FIPS codes with proper zero-padding
states_pop['FIPS'] = states_pop['STATE'].astype(str).str.zfill(2)

# Use right join to ensure ALL states are included, even if they have 0 NBA players
merged = pd.merge(nba_df, states_pop, on='State', how='right', validate='one_to_one')

# Fill missing player counts with 0 for states with no NBA players
merged['Players'] = merged['Players'].fillna(0).astype(int)

# Calculate per 100k residents
merged['Players_per_100k'] = (merged['Players'] / merged['Population']) * 100000

# Reorder columns to put FIPS first
merged = merged[['FIPS', 'State', 'Players', 'Population', 'Players_per_100k']]

# Sort by FIPS code for consistent ordering
merged = merged.sort_values('FIPS')

# Save the normalized data
merged.to_csv('nba_players_per_state_normalized.csv', index=False)

print("Normalized data saved with all 50 states + DC included.")
print(f"Total states/territories: {len(merged)}")
print(f"States with 0 players: {len(merged[merged['Players'] == 0])}")

# Show states with 0 players for verification
if zero_player_states := merged[merged['Players'] == 0]['State'].tolist():
    print(f"States with 0 NBA players: {', '.join(zero_player_states)}")
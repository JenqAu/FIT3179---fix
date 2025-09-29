import pandas as pd

# Load NBA players data
nba_df = pd.read_csv('nba_players_per_state.csv')

# Load population data
pop_df = pd.read_csv('NST-EST2024-ALLDATA.csv')

# Filter to states (SUMLEV == 40)
states_pop = pop_df[pop_df['SUMLEV'] == 40][['NAME', 'POPESTIMATE2024']]

# Rename columns
import pandas as pd

# Load NBA players data
nba_df = pd.read_csv('nba_players_per_state.csv')

# Mapping abbreviations to full names
state_abbrev = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    'DC': 'District of Columbia'
}

# But the CSV has full names like Alabama, not AL.

# Looking at the CSV, it's full names: Alabama, Alaska, etc., and DC.

# DC is "DC", but should be "District of Columbia"

# So I need to replace "DC" with "District of Columbia"

nba_df['State'] = nba_df['State'].replace({'DC': 'District of Columbia'})

# Load population data
pop_df = pd.read_csv('NST-EST2024-ALLDATA.csv')

# Filter to states (SUMLEV == 40)
states_pop = pop_df[pop_df['SUMLEV'] == 40][['NAME', 'POPESTIMATE2024']]

# Rename columns
states_pop = states_pop.rename(columns={'NAME': 'State', 'POPESTIMATE2024': 'Population'})

# Merge
merged = pd.merge(nba_df, states_pop, on='State', how='left')

# Calculate per 100k
merged['Players_per_100k'] = (merged['Players'] / merged['Population']) * 100000

# Save
merged.to_csv('nba_birthplaces_map/data/nba_players_per_state_normalized.csv', index=False)

print("Normalized data saved.")

# Merge
merged = pd.merge(nba_df, states_pop, on='State', how='left')

# Calculate per 100k
merged['Players_per_100k'] = (merged['Players'] / merged['Population']) * 100000

# Save
merged.to_csv('nba_birthplaces_map/data/nba_players_per_state_normalized.csv', index=False)

print("Normalized data saved.")
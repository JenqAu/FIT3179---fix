import pandas as pd
import h3
import json

# Read the geocoded data
df = pd.read_csv('NBA_Players_sample_coords.csv')

# Filter valid coordinates
df = df.dropna(subset=['latitude', 'longitude'])

print(f'Valid coordinates: {len(df)}')

# Function to get h3 index
def lat_lng_to_h3(lat, lng, resolution=4):
    return h3.latlng_to_cell(lat, lng, resolution)

# Add h3 index
df['h3_index'] = df.apply(lambda row: lat_lng_to_h3(row['latitude'], row['longitude']), axis=1)

# Group by h3 index and count
hex_counts = df.groupby('h3_index').size().reset_index(name='count')

print(f'Unique hexagons: {len(hex_counts)}')

# Get hexagon boundaries
hexagons = []
for _, row in hex_counts.iterrows():
    h3_index = row['h3_index']
    count = row['count']
    # Get hexagon boundary
    boundary = h3.cell_to_boundary(h3_index)
    # Convert to geojson-like format
    coords = [[lng, lat] for lat, lng in boundary]
    coords.append(coords[0])  # Close the polygon
    hexagons.append({
        'h3_index': h3_index,
        'count': count,
        'coordinates': coords
    })

# Save as JSON for Vega-Lite
with open('hex_bins.json', 'w') as f:
    json.dump(hexagons, f)

print('Hexagonal bins computed and saved!')
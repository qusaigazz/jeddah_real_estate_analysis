import json

# Load the GeoJSON file
with open("districts.geojson", "r", encoding="utf-8") as file:
    geo_data = json.load(file)

# Loop through features and filter by city_id
jeddah_districts = []

for feature in geo_data["features"]:
    if feature["properties"].get("city_id") == 18:
        name = feature["properties"]["name_en"].strip().lower().replace(" dist.", "")
        jeddah_districts.append(name)

# Optional: remove duplicates
jeddah_districts = list(set(jeddah_districts))

# Print results
print(f"Total Jeddah districts found: {len(jeddah_districts)}")
print(sorted(jeddah_districts))

import folium 
import json
from process_data import main 
import pandas as pd

city_mean, neighborhood_means = main()

# Step 1: Create neighborhood means DataFrame
neighborhood_df = pd.DataFrame(
    list(neighborhood_means.items()),
    columns=["neighborhood", "price_per_m2"]
)

# Step 2: Load GeoJSON file
with open("districts.geojson", "r", encoding="utf-8") as file:
    geo_data = json.load(file)

# Step 3: Filter full features for Jeddah
jeddah_features = [
    feature for feature in geo_data["features"]
    if feature["properties"].get("city_id") == 18
]

# Step 4: Normalize GeoJSON names
for feature in jeddah_features:
    name = feature["properties"].get("name_en", "").strip().lower()
    if name.endswith(" dist."):
        name = name.replace(" dist.", "")
    feature["properties"]["name_en"] = name

# Step 5: Normalize your DataFrame names
neighborhood_df["neighborhood"] = neighborhood_df["neighborhood"].str.strip().str.lower()

# Step 6: Map to GeoJSON-compatible names (optional but safer)
# Example mapping from your CSV to GeoJSON-compatible names
neighborhood_name_map = {
    "al zahraa": "az zahra",
    "al manar": "al manar",
    "al salamah": "as salamah",
    "al naseem": "al naseem",
    "al mraikh": "mraykh",
    "al nuzhah": "an nuzhah",
    "al waha": "al wahah",
    "al rawdah": "ar rawdah",
    "mishrifah": "mishrifah",
    "al aziziyah": "al aziziyah",
    "al marwah": "al marwah",
    "al rayaan": "ar rayaan",
    "al faisaliyah": "al faisaliyah",
    "al nahdah": "an nahdah",
    "al shati": "ash shati",
    "governmental1": "governmental",  # guess
    "al safa": "as safa",
    "al fayhaa": "al fayha",
    "al hamdaniyah": "al hamadaniyah",
    "al rawabi": "ar rawabi",
    "abruq al rughamah": "abruq ar rughamah",
    "al rehab": "al rehab",
    "al naim": "an naim",
    "al woroud": "al wurud",
    "al sawari": "as swaryee",
    "al bawadi": "al bawadi",
    "bani malik": "bani malik",
    "al jameah district": "al jamiah",
    "al rabwa": "ar rabwah",
    "prince abdulmajeed": "prince abdul majeed",
    "al hamraa": "al hamra",
    "al sulaymaniyah": "as sulaymaniyah",
    "al rahmanyah": "ar rahmaniyah",
    "al ajwad": "al ajwad",
    "umm hablain al gharbia": "um hableen al gharbiyyah",
    "ar rabiyah": "al rabiyah",
    "al nakheel": "al nakhil",
    "al sharafeyah": "ash sharafiyah",
    "quba": "quba",
    "obhur al janoubiyah": "abhur al janubiyah",
    "bryman": "bryman",
    "um assalum": "um asalam",
    "al rowais": "ar ruwais",
    "madeen al fahd": "madain al fahd",

}

# Step 6: Map to geojson-compatible names
neighborhood_df["geojson_name"] = neighborhood_df["neighborhood"].map(neighborhood_name_map)
neighborhood_df = neighborhood_df.dropna(subset=["geojson_name"])

print(neighborhood_df)

# Step 6.5: Update filtered GeoJSON
geo_data = {"type": "FeatureCollection", "features": jeddah_features}

# Create a mapping from geojson_name to price_per_m2
price_map = dict(zip(neighborhood_df["geojson_name"], neighborhood_df["price_per_m2"]))

for feature in geo_data["features"]:
    name = feature["properties"]["name_en"]
    price = price_map.get(name)

    if price is not None:
        feature["properties"]["price_per_m2"] = price
        feature["properties"]["comparison"] = (
            "Above Average" if price > city_mean else "Below Average"
        )
    else:
        feature["properties"]["price_per_m2"] = "N/A"
        feature["properties"]["comparison"] = "N/A"


# Step 7: Create map
m = folium.Map(location=[21.5433, 39.1728], zoom_start=11)

folium.Choropleth(
    geo_data=geo_data,
    data=neighborhood_df,
    columns=["geojson_name", "price_per_m2"],
    key_on="feature.properties.name_en",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Price per m²"
).add_to(m)


# adding interactive features to map 
folium.GeoJson(
    geo_data,
    name="Neighborhoods",
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': 'black',
        'weight': 0.3,
        'fillOpacity': 0
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=["name_en", "price_per_m2", "comparison"],
        aliases=["Neighborhood:", "Price per m²:", "Compared to City Avg:"],
        sticky=False,
        labels=True,
        style=(
            "background-color: white; color: #333; "
            "font-family: Arial; font-size: 12px; padding: 5px;"
        )
    )
).add_to(m)


# step 9: hardcode html city mean legend
legend_html = f'''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 90px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     padding: 10px;">
     <b>Legend</b><br>
     <span style="color:gray;">City-wide mean: {city_mean:.0f} SAR/m²</span>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))



# Step 10: Save map
m.save("jeddah_heatmap.html")
print("Map saved as jeddah_heatmap.html")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL of the website with page number placeholder
base_url = "https://www.bayut.sa/en/for-sale/apartments/jeddah/?page={}"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Empty list to store extracted data
all_apartments = []

# Loop through multiple pages
for page in range(1, 80):  # Try 3 pages for now
    url = base_url.format(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")


    listings = soup.find_all("li", class_="a37d52f0")

    for listing in listings:
        try:
            # Initialize values
            property_type = "Apartment"
            price = area = bedrooms = bathrooms = neighborhood = furnishing = latitude = longitude = None
            city = "Jeddah"

            # Price
            price_tag = listing.find("span", attrs={"aria-label": "Price"})
            if price_tag:
                price = price_tag.text.strip()

            # SPECS
            spec_tags = listing.find_all("span", class_="_19e94678")
            for tag in spec_tags:
                label = tag.get("aria-label", "").lower().strip()
                if "area" in label:
                    h4 = tag.find("h4")
                    area = h4.text.strip() if h4 else tag.text.strip()
                elif "bed" in label:
                    bedrooms = tag.text.strip()
                elif "bath" in label:
                    bathrooms = tag.text.strip()

            # Location (neighborhood)
            location_tag = listing.find("h3", class_="_4402bd70")
            if location_tag:
                full_location = location_tag.text.strip()
                parts = full_location.split(",")
                neighborhood = parts[0].strip() if len(parts) > 0 else None
                city = parts[-1].strip() if len(parts) > 1 else "Jeddah"

            # Furnishing status (requires entering each listing) 
            # Listing URL (to get to detail page)
            link_tag = listing.find("a", class_="d40f2294")
            listing_url = "https://www.bayut.sa" + link_tag.get("href") if link_tag else None

            # Visit detail page to extract furnishing info
            if listing_url:
                detail_response = requests.get(listing_url, headers=headers)
                detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                furnishing_tag = detail_soup.find("span", attrs={"aria-label": "Furnishing"})
                if furnishing_tag:
                    furnishing = furnishing_tag.text.strip()

                # Latitude and Longitude 

                # Find all <li> tags that might contain the data
                info_items = detail_soup.find_all("li", class_="_83bd8fa5")

                for item in info_items:
                    label_tag = item.find("span", class_="d0536c07")  # This contains the label
                    value_tag = item.find("span", class_="c24b8dde")  # This contains the value

                    if label_tag and value_tag:
                        label = label_tag.text.strip().lower()
                        value = value_tag.text.strip()

                        if "latitude" in label:
                            latitude = float(value)
                        elif "longitude" in label:
                            longitude = float(value)

                time.sleep(0.5)  #to not overwhelm their server 
            

            # Add to list
            all_apartments.append({
                "property_type": property_type,
                "furnishing": furnishing,
                "price": price,
                "area": area,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "neighborhood": neighborhood,
                "latitude": latitude,
                "longitude": longitude,
                "city": city
            })

        except Exception as e:
            print("Error with one listing:", e)

    time.sleep(1)

# Save to CSV
df = pd.DataFrame(all_apartments)
df.to_csv("jeddah_apartments.csv", index=False)
print(f"Saved {len(df)} rows to jeddah_apartments.csv")



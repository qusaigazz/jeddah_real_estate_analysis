import csv 
from collections import defaultdict

filename = "jeddah_apartments.csv"

# Read the data
with open(filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = list(reader)
    

def add_price_per_m2(data):
    for listing in data:
        try:
            price = float(listing["price"].replace(",", ""))
            area_text = listing["area"].split()[0].replace(",", "")  # <== clean area value
            area = float(area_text)
            price_per_m2 = price / area
            listing["price_per_m2"] = price_per_m2  # Add to original dictionary

        except (ValueError, ZeroDivisionError):
            listing["price_per_m2"] = None  # Add None if bad data

    return data  # Optional: return updated list if you want to use it directly

def neighborhood_analysis(data):
    #extract price per m2 and neighborhood from each listing
    all_prices = []
    neighborhoods = defaultdict(list)

    for listing in data:
        neighborhood = listing.get("neighborhood")
        ppm = listing.get("price_per_m2")
        all_prices.append(ppm)

        # Skip listings with invalid or generic neighborhood names
        if neighborhood.lower() == "jeddah":
            continue

        if neighborhood and ppm is not None:
           neighborhoods[neighborhood].append(float(ppm))

    # Now calculate the mean for each neighborhood
    neighborhood_means = {}
    for name, ppms in neighborhoods.items():
        mean = sum(ppms) / len(ppms)
        neighborhood_means[name] = mean

    #city mean
    city_mean = sum(all_prices) / len(all_prices) if all_prices else 0

    return city_mean, neighborhood_means

def main():
    data_with_ppm = add_price_per_m2(data)
    city_mean, neighborhood_means = neighborhood_analysis(data_with_ppm)
    return city_mean, neighborhood_means

if __name__ == "__main__":
    print(main())

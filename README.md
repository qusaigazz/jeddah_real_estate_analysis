# Jeddah Real Estate Analysis

[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Map](https://img.shields.io/badge/Mapping-Folium-yellowgreen)]()
[![Data](https://img.shields.io/badge/Data-Bayut.sa-orange)]()
[![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)]()
[![Focus](https://img.shields.io/badge/Focus-Geospatial%20Analysis-blue)]()
[![Domain](https://img.shields.io/badge/Domain-Data%20Science-purple)]()


Identifying potential undervalued apartments in Jeddah

## **Table of Contents**
---
- [About](#about)
- [Methodology](#methodology)
- [Macro](#Macro)


## **About**
---
In May 2025, the Saudi Cabinet approved a decision allowing the Ministry of Housing to sell residential units from its projects to individuals who are not beneficiaries of government housing support.

This new legislation presents an opportunity for non-beneficiaries to invest in real estate. This project aims to identify potentially undervalued apartment properties—given the increase in supply—with the goal of aiding prospective investors in finding promising opportunities.

## **Methodology**
---
This project takes inspiration from Steve Ash's methodology [How to Spot Under-Valued Properties—With Steve Ash](https://www.youtube.com/watch?v=PqNe_3cOHe4), which outlines a three-stage process that progressively zones in on potentially undervalued properties.

### **Macro**
Stage 1 consists of finding areas within the city that have properties below the city average, this filters out non-undervalued properties from our search. 

### **Miso**
During Stage 2 we focus on neighborhoods that show a significant price gap compared to their immediate neighbors. These localized low-price zones may indicate potential undervaluation irrespective of natural factors like location or amenities.

### **Micro**
At the final stage, we examine individual property listings situated between high- and low-priced neighborhoods. By analyzing listings in these transitional zones, we assess whether certain properties may be undervalued relative to their surroundings, and whether they have potential for value appreciation.

## **Macro**
---
## Data Scraping and Collection

I scraped apartment listings from [Bayut.sa](https://www.bayut.sa/en/), one of the leading real estate platforms in Saudi Arabia.
I then used Python libraries `requests` and `BeautifulSoup` to extract key fields such as price, area, apartment specs, district, furnishing, and coordinates.
The script loops over multiple pages and visits each listing individually to retrieve metadata such as latitude/longitude and furnishing type.
I implemented polite scraping by adding `time.sleep()` between requests to avoid overloading the server.

## Data Processing 

After scraping, I processed the raw CSV file using `pandas`. This included:

- Cleaning price and area fields (removing commas, extracting numerical values)

- Calculating price per square meter (price ÷ area)

- Normalizing neighborhood names to ensure consistent matching with GeoJSON district names

- Removing listings with missing or generic data (e.g., listings labeled simply as “Jeddah”)

- Calculating mean price per m² per neighborhood to support heatmap visualization


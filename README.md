# Jeddah Real Estate Analysis

[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Map](https://img.shields.io/badge/Mapping-Folium-yellowgreen)]()
[![Data](https://img.shields.io/badge/Data-Bayut.sa-orange)]()
[![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)]()
[![Focus](https://img.shields.io/badge/Focus-Geospatial%20Analysis-blue)]()
[![Domain](https://img.shields.io/badge/Domain-Data%20Science-purple)]()

# 📌 Summary
This project identifies undervalued properties in Jeddah by scraping and analyzing real estate data (geospatially) from Bayut.

- Scraped real estate listings in Jeddah from [Bayut.sa](https://www.bayut.sa/en/) using Python (`requests`, `BeautifulSoup`, `time.sleep()`).

- Cleaned and processed the data to calculate a new feature (price per square meter) for each listing.

- Aggregated data by neighborhood to compute and visualize neighborhood-level averages.

- Created a choropleth map to highlight pricing discrepancies across districts.

- Incorporated additional contextual layers including:

  - School locations and quality

  - Infrastructure development

  - Proximity to main highways

- Narrowed focus to individual listings within undervalued neighborhoods to assess standout opportunities.

## **Table of Contents**
---
- [About](#about)
- [Methodology](#methodology)
- [Macro](#Macro)


## 🧠 **About**
---
In May 2025, the Saudi Cabinet approved a decision allowing the Ministry of Housing to sell residential units from its projects to individuals who are not beneficiaries of government housing support.

This new legislation presents an opportunity for non-beneficiaries to invest in real estate. This project aims to identify potentially undervalued apartment properties—given the increase in supply—with the goal of aiding prospective investors in finding promising opportunities.

## 🔧 **Methodology**
---
This project takes inspiration from Steve Ash's methodology [How to Spot Under-Valued Properties—With Steve Ash](https://www.youtube.com/watch?v=PqNe_3cOHe4), which outlines a three-stage process that progressively zones in on potentially undervalued properties.

### **Macro**
Stage 1 consists of finding areas within the city that have properties below the city average, this filters out non-undervalued properties from our search. 

### **Miso**
During Stage 2 we focus on neighborhoods that show a significant price gap compared to their immediate neighbors. These localized low-price zones may indicate potential undervaluation irrespective of natural factors like location or amenities.

### **Micro**
At the final stage, we examine individual property listings situated between high- and low-priced neighborhoods. By analyzing listings in these transitional zones, we assess whether certain properties may be undervalued relative to their surroundings, and whether they have potential for value appreciation.

## 🌍 **Macro**
---
## Data Scraping and Collection

I scraped 1900+ apartment listings from [Bayut.sa](https://www.bayut.sa/en/), one of the leading real estate platforms in Saudi Arabia.
I then used Python libraries `requests` and `BeautifulSoup` to extract key fields such as price, area, apartment specs, district, furnishing, and coordinates.
The script loops over multiple pages and visits each listing individually to retrieve metadata such as latitude/longitude and furnishing type.
I implemented polite scraping by adding `time.sleep()` between requests to avoid overloading the server.

## Data Processing 

After scraping, I processed the raw CSV file using `pandas`. This included:

- Cleaning price and area fields (removing commas, extracting numerical values)

- Calculating price per square meter (price ÷ area) feature

- Normalizing neighborhood names to ensure consistent matching with GeoJSON district names

- Removing listings with missing or generic data (e.g., listings labeled simply as “Jeddah”)

- Calculating mean price per m² per neighborhood to support heatmap visualization

## Data Visulaization

I used Folium, a Python library for interactive maps, to create a choropleth heatmap of property prices across Jeddah’s neighborhoods.
The map integrates processed real estate data with a publicly available GeoJSON file of Saudi Arabia’s districts, filtered for city_id = 18 (Jeddah), with neighborhood names normalized for matching.
Color gradients represent relative property values, visually highlighting undervalued or overpriced districts.
Interactive features allow users to hover over each district to see:

The district name

Its average price per square meter

Whether it's above or below the city-wide average

The final map was saved as an HTML file and can be viewed interactively in any browser.

![Interactive Heatmap](images/heatmap_preview.png)







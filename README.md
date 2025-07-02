# AI-Powered Public Health Surveillance: Predicting and Visualizing Foodborne Illness Outbreaks Using Geospatial & Epidemiological Data

## Goal

To develop an interactive geospatial dashboard and ML-driven analytics pipeline that can:

- Detect regional hotspots of foodborne illness
- Prioritize inspection efforts based on food-linked severity
- Provide actionable insights into public health response strategies

## Intended Audience

- Public Health Agencies (e.g., CDC, CFIA, local health units)
- Food Safety Inspectors
- Epidemiologists
- Healthcare Data Scientists
- Policy Makers for food recalls and safety campaigns

## Strategy & Pipeline Steps

### Step 1: Data Cleaning & Inspection

```python
import pandas as pd
df = pd.read_csv('/content/outbreaks.csv')
df.fillna({'Illnesses': 0, 'Hospitalizations': 0, 'Fatalities': 0}, inplace=True)
```

### Step 2: Simulate Missing Coordinates

```python
import numpy as np
states = df['State'].dropna().unique()
coords = {state: (np.random.uniform(25, 49), np.random.uniform(-125, -66)) for state in states}
df['Latitude'] = df['State'].map(lambda x: coords.get(x, (np.nan, np.nan))[0])
df['Longitude'] = df['State'].map(lambda x: coords.get(x, (np.nan, np.nan))[1])
```

### Step 3: Create Geospatial Heatmap

```python
import folium
from folium.plugins import HeatMap

m = folium.Map(location=[37.8, -96], zoom_start=4)
heat_data = [[row['Latitude'], row['Longitude']] for _, row in df.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('/content/heatmap_outbreaks.html')
```

### Step 4: Temporal Trend of Outbreaks

```python
df['Year'] = df['Year'].fillna(0).astype(int)
outbreaks_per_year = df.groupby('Year').size()
outbreaks_per_year.plot(kind='bar', title='Outbreaks per Year', color='tomato')
```

**Insight:**

- Title: "Outbreaks per Year" – displays annual outbreak counts from 1998 to 2015.
- Trend: Peaks between 1999–2005; steady decline post-2006; lowest point around 2009.
- Public Health Significance: Reflects possible improvements in outbreak control and policy.

### Step 5: Root Cause Identification

```python
most_severe = df.sort_values(by='Fatalities', ascending=False).head(5)
print(most_severe[['Year', 'State', 'Food', 'Species', 'Fatalities']])
```

**Insight:**

- Years: Major incidents occurred in 1998, 2002, 2008, 2011, and 2014.
- Foods: Cantaloupe, peanut butter, deli meat, caramel apples, and hot dogs.
- Pathogen: Listeria monocytogenes is dominant in 4 of 5.
- Significance: Critical for guiding interventions.

### Step 6: Prioritize Food Items for Inspection

```python
top_foods = df.groupby('Food')['Hospitalizations'].sum().sort_values(ascending=False).head(10)
print(top_foods)
```

**Insight:**

- Top Offender: Cantaloupe ranks first with 317 hospitalizations.
- Sources: Both animal (ground beef, pork) and plant (cucumber, tomato) foods.
- Recurrent Risk: Peanut butter appears twice.
- Regulatory Value: Assists in targeting food inspections.

## Challenges Addressed

- Data sparsity (missing coordinates)
- Unstructured ingredient naming
- Coarse spatial resolution (state-level only)
- Limited labeled outcomes for predictive modeling

## Problem Statement

How can public health authorities detect, monitor, and act upon clusters of foodborne illness outbreaks using open data and geospatial analysis?

## Dataset

**CDC’s Foodborne Illness Outbreak Dataset** Kaggle mirror: [https://www.kaggle.com/datasets/cdc/foodborne-illness-outbreak-dataset](https://www.kaggle.com/datasets/cdc/foodborne-illness-outbreak-dataset)

Contains 1000+ outbreaks with: `['Year', 'State', 'Food', 'Illnesses', 'Hospitalizations', 'Fatalities', 'Latitude', 'Longitude']`

## Machine Learning Prediction

- Classification: Will an outbreak cause hospitalization?
- Regression: Predict number of hospitalizations/fatalities
- Clustering: KMeans for regional risk zones

## Trailer Documentation

- Geospatial risk map (HTML + screenshot)
- Time trend bar chart
- Top foods bar chart
- Root cause table
- Exportable dashboard via Streamlit

## Conceptual Enhancement – AGI Tie-In

Prototype can evolve into an Autonomous Epidemiology Assistant via:

- Real-time food recall ingestion using NLP
- Social media + outbreak data fusion
- Predictive outbreak alerts using historical & live data

---

**Developed by Ronald Kalani** | [LinkedIn](https://www.linkedin.com/in/ronaldkalani)

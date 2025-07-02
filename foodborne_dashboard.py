import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI-Powered Foodborne Outbreak Surveillance", layout="wide")

# --- Step 1: Load and Clean Data ---
file_path = "G:/My Drive/Public Health/outbreaks.csv"
try:
    df = pd.read_csv(file_path)
    st.success("✅ Data loaded successfully.")
except Exception as e:
    st.error(f"❌ Could not load file: {e}")
    st.stop()

# Fill missing outcome values
df.fillna({'Illnesses': 0, 'Hospitalizations': 0, 'Fatalities': 0}, inplace=True)

# Simulate missing geocoordinates based on State
states = df['State'].dropna().unique()
coords = {state: (np.random.uniform(25, 49), np.random.uniform(-125, -66)) for state in states}
df['Latitude'] = df['State'].map(lambda x: coords.get(x, (np.nan, np.nan))[0])
df['Longitude'] = df['State'].map(lambda x: coords.get(x, (np.nan, np.nan))[1])

# --- Dashboard Title ---
st.title("🌍 AI-Powered Foodborne Illness Surveillance")
st.markdown("**Goal:** Detect hotspots, prioritize inspections, and visualize outbreak trends using open data.")

# --- Step 2: Heatmap of Outbreaks ---
st.subheader("📍 Simulated Geospatial Heatmap")

geo_df = df.dropna(subset=['Latitude', 'Longitude'])
m = folium.Map(location=[geo_df['Latitude'].mean(), geo_df['Longitude'].mean()], zoom_start=4)
heat_data = [[row['Latitude'], row['Longitude']] for _, row in geo_df.iterrows()]
HeatMap(heat_data).add_to(m)
st_folium(m, height=500)

# --- Step 3: Temporal Trends ---
st.subheader("📈 Outbreaks Over Time")

df['Year'] = df['Year'].fillna(0).astype(int)
yearly_counts = df.groupby('Year').size()

fig, ax = plt.subplots()
yearly_counts.plot(kind='bar', ax=ax, color='tomato')
ax.set_title("Outbreaks per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Outbreaks")
st.pyplot(fig)

st.markdown("""
**Insight:**  
- Spike in outbreaks between 1999–2005  
- Drop after 2006, possibly due to improved food safety policies  
""")

# --- Step 4: Root Cause Analysis ---
st.subheader("🦠 Top 5 Most Fatal Outbreaks")

most_fatal = df.sort_values(by='Fatalities', ascending=False).head(5)
st.dataframe(most_fatal[['Year', 'State', 'Food', 'Species', 'Fatalities']])

st.markdown("""
**Observation:**  
- *Listeria monocytogenes* involved in 4 out of 5 deadliest outbreaks  
- Foods: Cantaloupe, Hot Dogs, Peanut Butter  
""")

# --- Step 5: High-Risk Foods for Inspection ---
st.subheader("🍽️ Top 10 Foods by Hospitalizations")

if 'Food' in df.columns and 'Hospitalizations' in df.columns:
    top_foods = (
        df.groupby('Food')['Hospitalizations']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_foods)
    st.markdown("""
    **Inspection Targeting:**  
    - Prioritize foods like Cantaloupe, Peppers, and Cucumber  
    - Both meat and produce categories appear  
    """)
else:
    st.warning("Missing 'Food' or 'Hospitalizations' column.")

# --- Step 6: Summary Metrics ---
st.subheader("📊 Outbreak Totals")

col1, col2, col3 = st.columns(3)
col1.metric("🤒 Illnesses", int(df['Illnesses'].sum()))
col2.metric("🏥 Hospitalizations", int(df['Hospitalizations'].sum()))
col3.metric("🕊️ Fatalities", int(df['Fatalities'].sum()))

# --- Footer ---
st.markdown("---")
st.caption("Built by Ronald Kalani | Data: CDC via Kaggle | Intended for CFIA, CDC, Public Health Agencies")


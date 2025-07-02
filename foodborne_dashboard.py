import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# File path to CSV
file_path = "G:/My Drive/Public Health/outbreaks.csv"

# Load data
try:
    df = pd.read_csv(file_path)
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# Show raw data and columns
with st.expander("📄 Preview Raw Data"):
    st.dataframe(df.head())
st.sidebar.write("🧾 Available columns:")
st.sidebar.write(df.columns.tolist())

# Detect latitude/longitude column names
lat_col = next((c for c in df.columns if 'lat' in c.lower()), None)
lon_col = next((c for c in df.columns if 'lon' in c.lower()), None)

if lat_col and lon_col:
    st.info(f"📍 Found latitude column: `{lat_col}`, longitude column: `{lon_col}`")
    geo_df = df.dropna(subset=[lat_col, lon_col])

    m = folium.Map(location=[geo_df[lat_col].astype(float).mean(), geo_df[lon_col].astype(float).mean()], zoom_start=5)
    heat_data = [[row[lat_col], row[lon_col]] for _, row in geo_df.iterrows()]
    HeatMap(heat_data).add_to(m)

    st.subheader("🌍 Heatmap of Outbreaks")
    st_folium(m, width=700, height=500)
else:
    st.warning("⚠️ Latitude and Longitude columns not found. Heatmap skipped.")

# Top 5 foods by hospitalizations
if 'Food' in df.columns and 'Hospitalizations' in df.columns:
    top_foods = (
        df.groupby('Food')['Hospitalizations']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.subheader("🍽️ Top 5 Foods by Hospitalizations")
    st.bar_chart(top_foods)
else:
    st.warning("⚠️ Missing 'Food' or 'Hospitalizations' column.")

# Summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🤒 Total Illnesses", df['Illnesses'].sum() if 'Illnesses' in df.columns else "N/A")

with col2:
    st.metric("🏥 Hospitalizations", df['Hospitalizations'].sum() if 'Hospitalizations' in df.columns else "N/A")

with col3:
    st.metric("🕊️ Fatalities", df['Fatalities'].sum() if 'Fatalities' in df.columns else "N/A")

st.caption("Built with Streamlit + Folium | Public Health Dashboard")


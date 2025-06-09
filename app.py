import streamlit as st
import pandas as pd
import altair as alt
from carbon_tracker import calculate_emissions

st.set_page_config("GreenRoute CO₂ Tracker", layout="centered")
st.title("🌿 GreenRoute – Carbon Emission Tracker")

# --------- File Configuration ---------
DATA_PATH = "emissions_data.csv"

@st.cache_data

def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except:
        return pd.DataFrame(columns=[
            "order_id", "artisan", "distance_km", "mode", "co2_emitted_kg", "co2_saved_kg"
        ])

data = load_data()

# --------- Form Input ---------
with st.form("add_order_form"):
    st.subheader("📦 Add New Delivery Record")
    order_id = st.text_input("Order ID")
    artisan = st.text_input("Artisan Name")
    distance = st.number_input("Distance (km)", min_value=0.1, step=0.1)

    submitted = st.form_submit_button("Track Delivery")
    if submitted:
        result = calculate_emissions(order_id, artisan, distance)
        existing = load_data()
        updated = pd.concat([existing, pd.DataFrame([result])], ignore_index=True)
        updated.to_csv(DATA_PATH, index=False)
        st.success(f"✅ Recorded: {result['co2_saved_kg']} kg CO₂ saved via {result['mode']}.")

# --------- Dashboard Metrics ---------
st.divider()
st.subheader("📊 Emission Tracking Summary")

total_saved = data["co2_saved_kg"].sum()
col1, col2, col3 = st.columns(3)
col1.metric("🌍 Total CO₂ Saved", f"{total_saved:.2f} kg")
col2.metric("📦 Deliveries", len(data))
col3.metric("🚚 Avg Distance", f"{data['distance_km'].mean():.2f} km")

st.dataframe(data)

# --------- Delivery Modes Chart ---------
MODES = ['bicycle', 'ev', 'truck']
MODE_LABELS = {
    'bicycle': '🚲 Bicycle',
    'ev': '⚡ EV',
    'truck': '🚛 Truck'
}

if not data.empty:
    actual_counts = data['mode'].value_counts().reset_index()
    actual_counts.columns = ['mode', 'count']

    # Ensure all modes are shown even with 0 values
    full_mode_df = pd.DataFrame({'mode': MODES})
    mode_counts = pd.merge(full_mode_df, actual_counts, on='mode', how='left').fillna(0)
    mode_counts['count'] = mode_counts['count'].astype(int)
    mode_counts['label'] = mode_counts['mode'].map(MODE_LABELS)

    st.subheader("🚗 Delivery Modes Used")

    bar_chart = alt.Chart(mode_counts).mark_bar(color='pink').encode(
        x=alt.X('count:Q', title='Number of Deliveries'),
        y=alt.Y('label:N', title='Delivery Mode', sort='-x'),
        tooltip=['label', 'count']
    ).properties(
        width=600,
        height=300
    )

    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.info("No data yet. Add a delivery to get started!")

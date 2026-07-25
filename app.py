import streamlit as st
from supabase import create_client
import pandas as pd
from Risk_classer import Risk
from streamlit_autorefresh import st_autorefresh



url = st.secrets['SUPABASE_URL']
key = st.secrets['SUPABASE_KEY']

supabase = create_client(url, key)
st_autorefresh(interval=120000, key='datarefresh')

st.set_page_config('SOLAR INVERTER MAINTENANCE SYSTEM', layout='wide')
st.title('SOLAR INVERTER MAINTENANCE SYSTEM')

response = (
    supabase
    .table("mins5_solar_reading")
    .select("*")
    .order("timestamp", desc=True)
    .limit(1)
    .execute()
)


response1 = (
    supabase
        .table("mins5_solar_reading")
        .select("*")
        .order("timestamp", desc=True)
        .limit(15)
        .execute()
)


reading = response.data
row = reading[0]

df = pd.DataFrame(response.data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

#   st.metric("Voltage", f"{row['voltage']} V")
#   st.metric("Current", f"{row['current']} A")
#   st.metric("Power", f"{row['power']} W")

#Due to lack of historical data, we will be using Rule based metrics (Risk scoring model)
#Max risk score = 11

#Each feature has a max score
#current = 3
#voltage = 2
#temperature = 2
#powerfactor = 2
#frequency = 1
#humidity = 1

scorer = Risk(rated_current=6.5, max_score = 11)

result = scorer.risk_scorer(
    current = row['current'],
    voltage = row['voltage'],
    frequency = row['frequency'],
    powerfactor = row['powerfactor'],
    temperature = row['temperature'],
    humidity = row['humidity']
)



risk_colors = {
    "Healthy": "🟢",
    "Low Risk": "🟡",
    "Caution(Moderate Risk)": "🟠",
    "Critical": "🔴",
}

st.subheader(f"{risk_colors.get(result['risk_severity'], '⚪')} Current status: {result['risk_severity']}  "
)
st.caption(f"Last reading: {df['timestamp'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')}")


cols = st.columns(6)
cols[0].metric("Voltage (V)", f"{row['voltage']:.1f}")
cols[1].metric("Current (A)", f"{row['current']:.2f}")
cols[2].metric("Temperature (°C)", f"{row['temperature']:.1f}")
cols[3].metric("Power Factor", f"{row['powerfactor']:.2f}")
cols[4].metric("Frequency (Hz)", f"{row['frequency']:.2f}")
cols[5].metric("Humidity (%)", f"{row['humidity']:.1f}")
 

df1 = pd.DataFrame(response1.data)
df1['timestamp'] = pd.to_datetime(df['timestamp'])
# --- Raw sensor values over time ---
st.subheader("Sensors Performance over time")
st.line_chart(df1[["voltage", "current", "temperature", "powerfactor"]])

# --- Raw data table ---
with st.expander("Raw data (most recent rows)"):
    st.dataframe(df1.sort_values("timestamp", ascending=True), use_container_width=True)
 

import streamlit as st
from supabase import create_client
import pandas as pd
from groq import Groq
import hashlib
import json
from Risk_classer import Risk
from streamlit_autorefresh import st_autorefresh



url = st.secrets['SUPABASE_URL']
key = st.secrets['SUPABASE_KEY']

supabase = create_client(url, key)

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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


 # ---------------- AI Status Report (Gemini free tier) ----------------
 
def snapshot_key(row: dict, result: dict) -> str:
    raw = json.dumps(row, sort_keys=True, default=str) + str(result["risk_score"])
    return hashlib.sha256(raw.encode()).hexdigest()
 
 
@st.cache_data(show_spinner=False)
def get_ai_report(_key: str, row: dict, result: dict) -> str:
    prompt = f"""You are a solar inverter maintenance advisor.
 
Current readings:
- Voltage: {row['voltage']} V
- Current: {row['current']} A
- Temperature: {row['temperature']} degC
- Power factor: {row['powerfactor']}
- Frequency: {row['frequency']} Hz
- Humidity: {row['humidity']} %
 
Risk score: {result['risk_score']} / 11 ({result['risk_severity']})
 
In under 80 words: explain the current status in plain language, name
which parameter(s) are pushing the score toward this tier, and give
one concrete next action (monitor, inspect, or urgent shutdown).
"""
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"AI report unavailable right now ({e})."
 
 
st.subheader("🤖 AI Maintenance Advisor")
ai_key = snapshot_key(row, result)
report = get_ai_report(ai_key, row, result)
st.info(report)


df1 = pd.DataFrame(response1.data)
df1['timestamp'] = pd.to_datetime(df['timestamp'])
# --- Raw sensor values over time ---
st.subheader("Sensors Performance Over Time")
st.line_chart(df1[["voltage", "current", "temperature", "powerfactor"]])

# --- Raw data table ---
with st.expander("Raw data (most recent rows)"):
    st.dataframe(df1.sort_values("timestamp", ascending=True), use_container_width=True)
 
